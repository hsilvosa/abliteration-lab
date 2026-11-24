"""Inference-time directional ablation via forward hooks.

Hooks project the direction out of the outputs of the embedding, every attention
`o_proj` and every MLP `down_proj`. This is mathematically identical to the weight
edit in edit.py (non norm-preserving, scale 1) but reversible, so candidate
directions can be scored without copying the model.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import torch
from torch import nn

from .activations import find_decoder_layers, find_embedding, write_modules
from .edit import _orthonormal_basis


def _make_hook(r: torch.Tensor, scale: float):
    q_cpu = _orthonormal_basis(r, torch.device("cpu"))
    cache: dict[tuple[torch.device, torch.dtype], torch.Tensor] = {}

    def hook(_module, _inputs, output):
        key = (output.device, output.dtype)
        qq = cache.get(key)
        if qq is None:
            qq = q_cpu.to(output.device, output.dtype)
            cache[key] = qq
        return output - scale * ((output @ qq.T) @ qq)

    return hook


@contextmanager
def ablation_hooks(
    model: nn.Module,
    r: torch.Tensor | dict[int, torch.Tensor],
    layer_range: range | None = None,
    scale: float = 1.0,
    embeddings: bool = True,
) -> Iterator[None]:
    layers = find_decoder_layers(model)
    layer_range = layer_range if layer_range is not None else range(len(layers))
    layer_wise = isinstance(r, dict)
    handles = []
    try:
        if embeddings:
            r_emb = r.get(-1, r[min(layer_range)]) if layer_wise else r
            handles.append(find_embedding(model).register_forward_hook(_make_hook(r_emb, scale)))
        for i in layer_range:
            ri = r[i] if layer_wise else r
            for lin in write_modules(layers[i]):
                handles.append(lin.register_forward_hook(_make_hook(ri, scale)))
        yield
    finally:
        for h in handles:
            h.remove()
