"""Refusal direction estimators."""

from __future__ import annotations

import torch


def _unit(v: torch.Tensor) -> torch.Tensor:
    return v / v.norm().clamp_min(1e-8)


def mean_diff(harmful_mean: torch.Tensor, harmless_mean: torch.Tensor) -> torch.Tensor:
    """Difference of means (Arditi et al., 2024), normalized."""
    return _unit(harmful_mean - harmless_mean)


def projected(harmful_mean: torch.Tensor, harmless_mean: torch.Tensor) -> torch.Tensor:
    """Difference of means with the component along the harmless mean removed.

    Projected abliteration (Lai, 2025): the part of the refusal direction that is
    parallel to the average harmless activation carries general "helpfulness"
    signal; removing it reduces collateral damage.
    """
    r = mean_diff(harmful_mean, harmless_mean)
    mu = _unit(harmless_mean)
    return _unit(r - (r @ mu) * mu)


ESTIMATORS = {"mean_diff": mean_diff, "projected": projected}


def compute(kind: str, harmful_mean: torch.Tensor, harmless_mean: torch.Tensor) -> torch.Tensor:
    try:
        return ESTIMATORS[kind](harmful_mean, harmless_mean)
    except KeyError:
        raise ValueError(f"unknown direction kind {kind!r}; choose from {sorted(ESTIMATORS)}") from None
