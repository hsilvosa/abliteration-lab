"""Automatic coherence and degeneration metrics for benign generations (`harmless_quality`).

Detects repetition loops and truncation collapse caused by over-ablation without
requiring an LLM judge or manual reading of every item.
"""

from __future__ import annotations

import re
from collections import Counter

from .refusal import strip_reasoning

_WORD_RE = re.compile(r"[a-z0-9']+")


def _words(text: str) -> list[str]:
    return _WORD_RE.findall(strip_reasoning(text).lower())


def ngram_repeat_rate(text: str, n: int = 4) -> float:
    """Fraction of n-grams that are duplicates: 1 - unique/total (0.0 = no repeats)."""
    ws = _words(text)
    if len(ws) < n:
        return 0.0
    ngrams = [tuple(ws[i : i + n]) for i in range(len(ws) - n + 1)]
    return 1.0 - len(set(ngrams)) / len(ngrams)


def max_ngram_count(text: str, n: int = 5) -> int:
    """Highest frequency of any single n-gram in `text`."""
    ws = _words(text)
    if len(ws) < n:
        return 0
    counts = Counter(tuple(ws[i : i + n]) for i in range(len(ws) - n + 1))
    return max(counts.values())


def is_degenerate(text: str, repeat4_threshold: float = 0.25, max_5gram_threshold: int = 4) -> bool:
    """True when a benign reply is empty or exhibits repetition-loop degeneration."""
    if not _words(text):
        return True
    return ngram_repeat_rate(text, 4) >= repeat4_threshold or max_ngram_count(text, 5) >= max_5gram_threshold
