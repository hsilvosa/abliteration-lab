"""Weight orthogonalization: remove a direction from everything that writes to the residual stream."""

from __future__ import annotations

import torch
from torch import nn

from .activations import find_decoder_layers, find_embedding, write_modules


def orthogonalize_linear_weight(
    weight: torch.Tensor, r: torch.Tensor, scale: float = 1.0, norm_preserving: bool = False
) -> torch.Tensor:
    """W' = W - scale * r r^T W for a Linear weight of shape (d_model, d_in).

    Each column W[:, j] is a vector in residual space. With `norm_preserving`, each
    column is rescaled to its original norm after the projection; scaling keeps the
    column orthogonal to r, so the refusal component stays removed.
    """
    w = weight.float()
    r = r.to(w.device, torch.float32)
    r = r / r.norm()
    w_new = w - scale * torch.outer(r, r @ w)
    if norm_preserving:
        ratio = w.norm(dim=0) / w_new.norm(dim=0).clamp_min(1e-8)
        w_new = w_new * ratio
    return w_new.to(weight.dtype)


def orthogonalize_embedding_weight(
    weight: torch.Tensor, r: torch.Tensor, scale: float = 1.0, norm_preserving: bool = False
) -> torch.Tensor:
    """E' = E - scale * (E r) r^T for an embedding of shape (vocab, d_model)."""
    e = weight.float()
    r = r.to(e.device, torch.float32)
    r = r / r.norm()
    e_new = e - scale * torch.outer(e @ r, r)
    if norm_preserving:
        ratio = e.norm(dim=1, keepdim=True) / e_new.norm(dim=1, keepdim=True).clamp_min(1e-8)
        e_new = e_new * ratio
    return e_new.to(weight.dtype)


def _orthogonalize_bias(bias: torch.Tensor, r: torch.Tensor, scale: float) -> torch.Tensor:
    b = bias.float()
    r = r.to(b.device, torch.float32)
    r = r / r.norm()
    return (b - scale * (b @ r) * r).to(bias.dtype)


def untie_lm_head(model: nn.Module) -> bool:
    """Give lm_head its own weight when it shares storage with the input embedding.

    Editing a tied embedding would also edit the output projection, which the
    inference-time hooks do not do. Returns True when the model was untied.
    """
    head = model.get_output_embeddings()
    emb = model.get_input_embeddings()
    if head is None or head.weight.data_ptr() != emb.weight.data_ptr():
        return False
    head.weight = nn.Parameter(emb.weight.detach().clone())
    model.config.tie_word_embeddings = False
    if hasattr(model.config, "get_text_config"):
        model.config.get_text_config().tie_word_embeddings = False
    return True


def resolve_layer_range(spec, n_layers: int) -> range:
    if spec == "all":
        return range(n_layers)
    start, end = spec
    return range(int(round(start * n_layers)), int(round(end * n_layers)))


@torch.no_grad()
def apply_edit(
    model: nn.Module,
    r: torch.Tensor,
    layer_range: range,
    scale: float = 1.0,
    norm_preserving: bool = False,
    edit_embeddings: bool = True,
) -> dict:
    """Edit `model` in place. Returns a small record of what changed."""
    layers = find_decoder_layers(model)
    edited = []
    if edit_embeddings:
        untied = untie_lm_head(model)
        emb = find_embedding(model)
        emb.weight.copy_(orthogonalize_embedding_weight(emb.weight, r, scale, norm_preserving))
        edited.append("embed_tokens")
    else:
        untied = False
    for i in layer_range:
        for lin in write_modules(layers[i]):
            lin.weight.copy_(orthogonalize_linear_weight(lin.weight, r, scale, norm_preserving))
            if lin.bias is not None:
                lin.bias.copy_(_orthogonalize_bias(lin.bias, r, scale))
        edited.append(f"layer{i}")
    return {"edited": edited, "untied_lm_head": untied, "scale": scale, "norm_preserving": norm_preserving}
