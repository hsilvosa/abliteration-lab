"""MMLU prompt formatting and answer parsing."""

from __future__ import annotations

import re

LETTERS = "ABCD"

_ANSWER_RE = re.compile(r"(?:answer\s*(?:is|:)?\s*\(?)([ABCD])\b", re.IGNORECASE)
_LEADING_RE = re.compile(r"^\s*\(?([ABCD])[\).:\s]|^\s*([ABCD])\s*$")


def format_prompt(question: str, choices: list[str]) -> str:
    lines = [question.strip(), ""]
    lines += [f"{LETTERS[i]}. {c}" for i, c in enumerate(choices)]
    lines += ["", "Answer with the letter of the correct option only."]
    return "\n".join(lines)


def parse_answer(text: str) -> int | None:
    """Return the chosen option index (0-3) or None when no letter can be found."""
    from .refusal import strip_reasoning

    text = strip_reasoning(text).strip()
    m = _LEADING_RE.match(text)
    if m:
        return LETTERS.index((m.group(1) or m.group(2)).upper())
    m = _ANSWER_RE.search(text)
    if m:
        return LETTERS.index(m.group(1).upper())
    return None
