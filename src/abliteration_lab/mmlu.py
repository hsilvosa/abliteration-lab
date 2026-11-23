"""MMLU prompt formatting and answer parsing."""

from __future__ import annotations

import re

LETTERS = "ABCD"

_ANSWER_RE = re.compile(r"answer\s*(?:is|:)?\s*\**\(?([ABCD])\b", re.IGNORECASE)
_LEADING_RE = re.compile(r"^\s*\(?([ABCD])[\).:\s]|^\s*([ABCD])\s*$")


def format_prompt(question: str, choices: list[str]) -> str:
    lines = [question.strip(), ""]
    lines += [f"{LETTERS[i]}. {c}" for i, c in enumerate(choices)]
    lines += ["", "Begin your reply with \"Answer: X\" where X is A, B, C or D. Do not explain."]
    return "\n".join(lines)


def parse_answer(text: str) -> int | None:
    """Return the chosen option index (0-3) or None when no letter can be found."""
    from .refusal import strip_reasoning

    text = strip_reasoning(text).strip()
    found = _ANSWER_RE.findall(text)  # the last stated answer wins
    if found:
        return LETTERS.index(found[-1].upper())
    m = _LEADING_RE.match(text)
    if m:
        return LETTERS.index((m.group(1) or m.group(2)).upper())
    return None
