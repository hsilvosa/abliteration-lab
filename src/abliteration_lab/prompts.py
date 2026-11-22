"""Load prompt sets from the files fetched by `abl datasets --yes`."""

from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

from .paths import DATA_DIR


def _require(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run: abl datasets --yes")
    return path


def _parquet(dataset_id: str, rel: str) -> pd.DataFrame:
    return pd.read_parquet(_require(DATA_DIR / dataset_id / rel))


def harmful(split: str) -> list[str]:
    return _parquet("harmful", f"data/{split}-00000-of-00001.parquet")["text"].tolist()


def harmless(split: str) -> list[str]:
    return _parquet("harmless", f"data/{split}-00000-of-00001.parquet")["text"].tolist()


def xstest(label: str = "safe") -> list[dict]:
    df = pd.read_csv(_require(DATA_DIR / "xstest" / "xstest_prompts.csv"))
    df = df[df["label"] == label]
    return df[["id", "prompt", "type"]].to_dict("records")


def mmlu_sample(per_subject: int, seed: int = 0) -> list[dict]:
    """Fixed stratified sample: `per_subject` questions from each of the 57 subjects."""
    df = _parquet("mmlu", "all/test-00000-of-00001.parquet")
    rng = random.Random(seed)
    rows: list[dict] = []
    for subject, group in sorted(df.groupby("subject"), key=lambda kv: kv[0]):
        idx = sorted(group.index.tolist())
        for i in rng.sample(idx, min(per_subject, len(idx))):
            r = df.loc[i]
            rows.append(
                {
                    "id": f"{subject}-{i}",
                    "subject": subject,
                    "question": r["question"],
                    "choices": list(r["choices"]),
                    "answer": int(r["answer"]),
                }
            )
    return rows


def take(items: list, n: int) -> list:
    """First `n` items, deterministic. Splits are fixed upstream, so no shuffling here."""
    return items[:n] if n and n < len(items) else list(items)
