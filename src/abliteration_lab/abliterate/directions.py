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


def compute_subspace(
    kind: str, harmful_states: torch.Tensor, harmless_states: torch.Tensor, rank: int = 1
) -> torch.Tensor:
    """Return a 1D direction (rank=1) or 2D orthonormal basis (rank, d_model).

    Row 0 is the primary mean-difference (or projected) refusal direction.
    Rows 1..rank-1 are the top right singular vectors of the harmful states after
    removing the harmless mean and previously extracted directions (and, for
    `projected`, the harmless-mean axis).
    """
    mu_h = harmful_states.mean(dim=0)
    mu_b = harmless_states.mean(dim=0)
    primary = compute(kind, mu_h, mu_b)
    if rank <= 1:
        return primary
    diff = harmful_states - mu_b
    basis = [primary]
    mu_b_unit = _unit(mu_b)
    # Remove primary direction (and harmless mean axis if projected) before SVD.
    proj_vecs = [primary, mu_b_unit] if kind == "projected" else [primary]
    for v in proj_vecs:
        diff = diff - torch.outer(diff @ v, v)
    _, _, vh = torch.linalg.svd(diff, full_matrices=False)
    for k in range(min(rank - 1, vh.shape[0])):
        v = vh[k]
        for b in basis:
            v = v - (v @ b) * b
        if kind == "projected":
            v = v - (v @ mu_b_unit) * mu_b_unit
        if float(v.norm()) > 1e-6:
            basis.append(_unit(v))
    return torch.stack(basis, dim=0)
