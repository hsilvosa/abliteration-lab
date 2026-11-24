"""End-to-end abliteration of a full-precision Hugging Face checkpoint.

Steps (all settings in configs/abliterate.toml):
1. Mean last-token activations for harmful and harmless train prompts at candidate layers.
2. One refusal direction per candidate layer.
3. Score each candidate with reversible hooks: greedy refusals on held-out harmful
   prompts and first-token KL on held-out harmless prompts.
4. Select by the pre-declared rule, edit the weights in place, save the checkpoint
   plus a metadata file under <models_dir>/own/<output_name>/.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from typing import Any

from .. import prompts
from ..config import load_registry, load_toml
from ..paths import own_models_dir


def _select(candidates: list[dict[str, Any]], kl_max: float) -> dict[str, Any]:
    """Minimum refusals within the KL budget; ties -> lowest KL (least collateral damage).

    The heuristic only counts explicit refusals, so several aggressive candidates
    can all score zero. KL then picks the cheapest of them; it is the edit strength
    (scale, layers, embeddings) that targets safe-reframes, not the KL tie-break.
    """
    ok = [c for c in candidates if c["kl"] <= kl_max]
    if not ok:
        raise RuntimeError(f"no candidate with KL <= {kl_max}; see candidates.json and adjust the protocol")
    return min(ok, key=lambda c: (c["refusals"], c["kl"]))


def run(dry_run: bool = False) -> None:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from .activations import find_decoder_layers, mean_last_token_states
    from .directions import compute
    from .edit import apply_edit, resolve_layer_range
    from .hooks import ablation_hooks
    from .scoring import count_refusals, first_token_logprobs, greedy_replies, kl_divergence

    cfg = load_toml("abliterate")
    spec = load_registry().by_id(cfg["source_model"])
    if spec.format != "hf":
        raise ValueError(f"{spec.id} is not a full-precision HF checkpoint")
    if not (spec.local_dir / "config.json").exists():
        raise FileNotFoundError(f"{spec.local_dir} missing. Run: abl download --model {spec.id} --yes")

    d, s, e = cfg["directions"], cfg["selection"], cfg["edit"]
    harmful_train = prompts.harmful("train")
    harmless_train = prompts.harmless("train")
    dir_harmful = harmful_train[: d["n_train"]]
    dir_harmless = harmless_train[: d["n_train"]]
    val_harmful = harmful_train[-s["n_val"] :]
    kl_harmless = harmless_train[d["n_train"] : d["n_train"] + s["n_kl"]]
    if len(dir_harmful) + len(val_harmful) > len(harmful_train):
        raise ValueError("n_train + n_val exceeds the harmful train split; prompts would overlap")

    out_dir = own_models_dir() / cfg["output_name"]
    print(f"Source: {spec.local_dir}\nOutput: {out_dir}")
    print(f"Prompts: {len(dir_harmful)}+{len(dir_harmless)} for directions, {len(val_harmful)} val, {len(kl_harmless)} KL")
    if dry_run:
        print("Dry run: inputs resolved, nothing loaded.")
        return

    t0 = time.monotonic()
    dtype = getattr(torch, cfg["dtype"])
    tok = AutoTokenizer.from_pretrained(spec.local_dir)
    load_kw: dict[str, Any] = {"dtype": dtype, "device_map": cfg["device"]}
    if cfg.get("load_in_4bit"):
        from transformers import BitsAndBytesConfig

        load_kw["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=dtype)
    model = AutoModelForCausalLM.from_pretrained(spec.local_dir, **load_kw).eval()
    n_layers = len(find_decoder_layers(model))
    cand_layers = sorted({max(1, min(n_layers - 1, round(f * n_layers))) for f in d["layer_fractions"]})
    print(f"{n_layers} layers; candidate layers {cand_layers}")

    bs, ml = d["batch_size"], d["max_prompt_tokens"]
    mu_harmful = mean_last_token_states(model, tok, dir_harmful, cand_layers, bs, ml)
    mu_harmless = mean_last_token_states(model, tok, dir_harmless, cand_layers, bs, ml)
    directions = {li: compute(d["kind"], mu_harmful[li], mu_harmless[li]) for li in cand_layers}

    ref_lp = first_token_logprobs(model, tok, kl_harmless, bs, ml)
    base_refusals = count_refusals(greedy_replies(model, tok, val_harmful, bs, ml, s["max_new_tokens"]))
    print(f"Original model: {base_refusals}/{len(val_harmful)} refusals on validation")

    edit_range = resolve_layer_range(e["layer_range"], n_layers)
    candidates = []
    for li, r in directions.items():
        with ablation_hooks(model, r, edit_range, e["scale"], e["edit_embeddings"]):
            refusals = count_refusals(greedy_replies(model, tok, val_harmful, bs, ml, s["max_new_tokens"]))
            kl = kl_divergence(ref_lp, first_token_logprobs(model, tok, kl_harmless, bs, ml))
        candidates.append({"layer": li, "refusals": refusals, "kl": round(kl, 5)})
        print(f"  layer {li:3d}: refusals {refusals}/{len(val_harmful)}  KL {kl:.4f}")

    best = _select(candidates, s["kl_max"])
    print(f"Selected layer {best['layer']}")

    r = directions[best["layer"]]
    if cfg.get("load_in_4bit"):
        # bitsandbytes 4-bit weights cannot be edited and saved in full precision.
        out_dir.mkdir(parents=True, exist_ok=True)
        torch.save({"direction": r, "layer": best["layer"]}, out_dir / "refusal_direction.pt")
        (out_dir / "candidates.json").write_text(json.dumps(candidates, indent=2), encoding="utf-8")
        print("load_in_4bit: direction search only. Set load_in_4bit = false to edit and save weights.")
        return
    # Move to CPU before untying lm_head and float32 weight edits to avoid VRAM spikes on 12 GB GPUs.
    model.to("cpu")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    record = apply_edit(model, r, edit_range, e["scale"], e["mode"] == "norm_preserving", e["edit_embeddings"])

    out_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(out_dir, safe_serialization=True)
    tok.save_pretrained(out_dir)
    torch.save({"direction": r, "layer": best["layer"]}, out_dir / "refusal_direction.pt")
    manifest = spec.local_dir / "manifest.json"
    meta = {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_repo": spec.repo,
        "source_revision": json.loads(manifest.read_text())["revision"] if manifest.exists() else None,
        "config": cfg,
        "baseline_refusals_val": base_refusals,
        "candidates": candidates,
        "selected": best,
        "edit": {k: v for k, v in record.items() if k != "edited"},
        "edited_modules": len(record["edited"]),
        "wall_time_s": round(time.monotonic() - t0, 1),
    }
    (out_dir / "abliteration.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Saved to {out_dir} in {meta['wall_time_s']} s. Next: scripts/convert_to_gguf.sh {cfg['output_name']}")
