from abliteration_lab.mmlu import format_prompt, parse_answer
from abliteration_lab.refusal import is_refusal, strip_reasoning
from abliteration_lab.report import wilson


def test_refusal_markers():
    assert is_refusal("I'm sorry, but I can't help with that.")
    assert is_refusal("I\u2019m sorry, I cannot assist.")
    assert is_refusal("")
    assert not is_refusal("Sure. Step 1: preheat the oven to 180 C.")


def test_refusal_ignores_reasoning_block():
    text = "<think>I cannot decide yet</think>Here is the recipe you asked for."
    assert not is_refusal(text)
    assert strip_reasoning("<think>unfinished") == ""


def test_mmlu_parse():
    assert parse_answer("B") == 1
    assert parse_answer("C. Paris") == 2
    assert parse_answer("The answer is D") == 3
    assert parse_answer("(A)") == 0
    assert parse_answer("It could be A or B.\n\nAnswer: C") == 2
    assert parse_answer("Answer: **D**") == 3
    assert parse_answer("**Answer: B**") == 1
    assert parse_answer("no idea") is None
    assert "A. x" in format_prompt("Q?", ["x", "y", "z", "w"])


def test_wilson_interval():
    lo, hi = wilson(50, 100)
    assert 0.40 < lo < 0.41 and 0.59 < hi < 0.60
    lo, hi = wilson(0, 100)
    assert lo == 0.0 and hi < 0.04
