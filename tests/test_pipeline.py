import pytest

from abliteration_lab.abliterate.pipeline import _select


def test_select_prefers_cheapest_edit_on_refusal_tie():
    candidates = [
        {"layer": 10, "refusals": 0, "kl": 0.2},
        {"layer": 18, "refusals": 0, "kl": 0.7},
        {"layer": 22, "refusals": 1, "kl": 0.1},
    ]
    assert _select(candidates, 0.8)["layer"] == 10


def test_select_ignores_candidates_over_kl_budget():
    candidates = [
        {"layer": 10, "refusals": 0, "kl": 0.9},
        {"layer": 18, "refusals": 2, "kl": 0.3},
    ]
    assert _select(candidates, 0.5)["layer"] == 18


def test_select_raises_when_budget_too_tight():
    with pytest.raises(RuntimeError):
        _select([{"layer": 10, "refusals": 0, "kl": 0.9}], 0.5)
