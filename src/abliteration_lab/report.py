"""Aggregate raw evaluation files into a summary table with confidence intervals."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

from .config import load_registry
from .paths import RESULTS_DIR
from .refusal import is_refusal


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a proportion k/n."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def _load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def summarize() -> pd.DataFrame:
    reg = load_registry()
    rows = []
    for path in sorted((RESULTS_DIR / "raw").glob("*/*.jsonl")):
        recs = _load(path)
        if not recs:
            continue
        model_id = path.parent.name
        task, thinking = path.stem.split("__thinking-")
        if task in ("refusal", "over_refusal"):
            for r in recs:  # always rescore from the raw text with the current heuristic
                r["refused"] = is_refusal(r["content"])
        key = {"refusal": "refused", "over_refusal": "refused", "mmlu": "correct"}.get(task)
        speeds = [r["tok_per_s"] for r in recs if r.get("tok_per_s")]
        row = {
            "model": model_id,
            "task": task,
            "thinking": thinking,
            "n": len(recs),
            "tok_per_s": round(sum(speeds) / len(speeds), 1) if speeds else None,
        }
        if key:
            k = sum(bool(r.get(key)) for r in recs)
            lo, hi = wilson(k, len(recs))
            row.update({"rate": round(k / len(recs), 3), "ci_low": round(lo, 3), "ci_high": round(hi, 3)})
        try:
            spec = reg.by_id(model_id)
            row.update({"role": spec.role, "baseline": spec.baseline})
        except KeyError:
            row.update({"role": "own", "baseline": None})
        rows.append(row)
        jp = RESULTS_DIR / "judge" / model_id / path.name
        if task in ("refusal", "over_refusal") and jp.exists():
            verdicts = [json.loads(line)["label"] for line in jp.open(encoding="utf-8") if line.strip()]
            n = len(verdicts)
            for name, labels in (("judge_refusal", ("REFUSAL",)), ("judge_refusal+partial", ("REFUSAL", "PARTIAL"))):
                k = sum(v in labels for v in verdicts)
                lo, hi = wilson(k, n)
                rows.append({**row, "task": f"{task}[{name}]", "n": n, "tok_per_s": None,
                             "rate": round(k / n, 3), "ci_low": round(lo, 3), "ci_high": round(hi, 3)})
    return pd.DataFrame(rows)


def paired_deltas(df: pd.DataFrame) -> pd.DataFrame:
    """Abliterated minus baseline, per task and thinking mode."""
    out = []
    for _, r in df[df["baseline"].notna()].iterrows():
        base = df[(df["model"] == r["baseline"]) & (df["task"] == r["task"]) & (df["thinking"] == r["thinking"])]
        rate = r["rate"] if "rate" in r.index else None
        if base.empty or rate is None or bool(pd.isna(rate)):
            continue
        b = base.iloc[0]
        out.append(
            {
                "model": r["model"],
                "baseline": r["baseline"],
                "task": r["task"],
                "thinking": r["thinking"],
                "rate": r["rate"],
                "baseline_rate": b["rate"],
                "delta": round(r["rate"] - b["rate"], 3),
            }
        )
    return pd.DataFrame(out)


def write_report() -> Path:
    df = summarize()
    if df.empty:
        raise SystemExit("No raw results under results/raw. Run: abl eval ...")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RESULTS_DIR / "summary.csv", index=False)
    deltas = paired_deltas(df)
    md = RESULTS_DIR / "summary.md"
    parts = ["# Evaluation summary", "", "Rates with 95% Wilson intervals.", "", df.to_markdown(index=False)]
    if not deltas.empty:
        parts += ["", "## Abliterated minus baseline", "", deltas.to_markdown(index=False)]
    md.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(md.read_text(encoding="utf-8"))
    return md
