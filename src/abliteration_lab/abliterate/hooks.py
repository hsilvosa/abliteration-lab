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


def _make_hook(r: torch.Tensor, scale: float):
    def hook(_module, _inputs, output):
        rr = r.to(output.device, output.dtype)
        return output - scale * (output @ rr).unsqueeze(-1) * rr

    return hook


@contextmanager
def ablation_hooks(
    model: nn.Module, r: torch.Tensor, layer_range: range | None = None, scale: float = 1.0, embeddings: bool = True
) -> Iterator[None]:
    r = r / r.norm()
    layers = find_decoder_layers(model)
    layer_range = layer_range if layer_range is not None else range(len(layers))
    handles = []
    try:
        if embeddings:
            handles.append(find_embedding(model).register_forward_hook(_make_hook(r, scale)))
        for i in layer_range:
            for lin in write_modules(layers[i]):
                handles.append(lin.register_forward_hook(_make_hook(r, scale)))
        yield
    finally:
        for h in handles:
            h.remove()
