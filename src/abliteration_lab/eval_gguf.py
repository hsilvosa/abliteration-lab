"""Evaluate GGUF models through llama-server.

Per model and task, every prompt and raw reply is appended to
results/raw/<model>/<task>__<thinking>.jsonl. Items already present are skipped, so an
interrupted run resumes where it stopped. Scoring reads those files back (see report.py).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from . import prompts
from .config import ModelSpec, load_toml
from .mmlu import format_prompt, parse_answer
from .paths import RESULTS_DIR
from .refusal import is_refusal
from .server import LlamaServer

TASKS = ("refusal", "over_refusal", "mmlu", "harmless_quality")


def raw_path(model_id: str, task: str, thinking: str) -> Path:
    return RESULTS_DIR / "raw" / model_id / f"{task}__thinking-{thinking}.jsonl"


def _done_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8") as fh:
        return {json.loads(line)["item_id"] for line in fh if line.strip()}


def build_items(task: str, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Return [{item_id, prompt, ...task fields}] for a task, deterministic."""
    t = cfg["tasks"][task]
    if task == "refusal":
        texts = prompts.take(prompts.harmful(t["split"]), t["n"])
        return [{"item_id": f"harmful-{t['split']}-{i}", "prompt": p} for i, p in enumerate(texts)]
    if task == "over_refusal":
        rows = prompts.take(prompts.xstest(t["label"]), t["n"])
        return [{"item_id": f"xstest-{r['id']}", "prompt": r["prompt"], "type": r["type"]} for r in rows]
    if task == "mmlu":
        per_subject = max(1, t["n"] // 57)
        rows = prompts.mmlu_sample(per_subject, t["seed"])
        return [
            {
                "item_id": r["id"],
                "prompt": format_prompt(r["question"], r["choices"]),
                "subject": r["subject"],
                "answer": r["answer"],
            }
            for r in rows
        ]
    if task == "harmless_quality":
        texts = prompts.take(prompts.harmless(t["split"]), t["n"])
        return [{"item_id": f"harmless-{t['split']}-{i}", "prompt": p} for i, p in enumerate(texts)]
    raise ValueError(f"unknown task {task}")


def score(task: str, item: dict[str, Any], reply: dict[str, Any]) -> dict[str, Any]:
    text = reply["content"]
    if task in ("refusal", "over_refusal"):
        return {"refused": is_refusal(text)}
    if task == "mmlu":
        pred = parse_answer(text)
        return {"pred": pred, "correct": pred == item["answer"]}
    return {}


def evaluate_model(spec: ModelSpec, tasks: Iterable[str], thinking: str | None = None, limit: int | None = None) -> None:
    cfg = load_toml("eval")
    mode: str = thinking or cfg["thinking"]["mode"]
    if mode not in ("on", "off"):
        raise ValueError(f"thinking mode must be 'on' or 'off', got {mode!r}")
    thinking = mode
    overrides = cfg.get("overrides", {}).get(spec.id, {})
    samp = cfg["sampling"]

    work: list[tuple[str, list[dict[str, Any]], Path]] = []
    for task in tasks:
        items = build_items(task, cfg)
        if limit:
            items = items[:limit]
        path = raw_path(spec.id, task, thinking)
        done = _done_ids(path)
        pending = [it for it in items if it["item_id"] not in done]
        print(f"{spec.id} | {task}: {len(items) - len(pending)}/{len(items)} cached")
        if pending:
            work.append((task, pending, path))
    if not work:
        return

    with LlamaServer(spec, cfg["server"], overrides) as srv:
        for task, pending, path in work:
            path.parent.mkdir(parents=True, exist_ok=True)
            max_tokens = cfg["tasks"][task].get("max_tokens", samp["max_tokens"])
            if task == "mmlu" and thinking == "on":
                max_tokens = samp["max_tokens"]  # room for the reasoning trace
            with path.open("a", encoding="utf-8") as fh:
                for n, item in enumerate(pending, 1):
                    reply = srv.chat(
                        item["prompt"],
                        temperature=samp["temperature"],
                        max_tokens=max_tokens,
                        seed=samp["seed"],
                        thinking=thinking,
                    )
                    record = {**item, **reply, **score(task, item, reply), "model": spec.id, "thinking": thinking}
                    fh.write(json.dumps(record, ensure_ascii=False) + "\n")
                    fh.flush()
                    if n % 25 == 0 or n == len(pending):
                        print(f"  {task}: {n}/{len(pending)}")
