"""Locate model parts and collect residual-stream activations."""

from __future__ import annotations

import torch
from torch import nn


def find_decoder_layers(model: nn.Module) -> nn.ModuleList:
    """Return the longest ModuleList of blocks that have `self_attn` and `mlp`.

    Works for Llama/Qwen/Mistral (`model.model.layers`) and for multimodal wrappers
    such as Gemma (`model.model.language_model.layers`).
    """
    best: nn.ModuleList | None = None
    for _, module in model.named_modules():
        if isinstance(module, nn.ModuleList) and len(module) > 0:
            first = module[0]
            if hasattr(first, "self_attn") and hasattr(first, "mlp"):
                if best is None or len(module) > len(best):
                    best = module
    if best is None:
        raise ValueError("could not find decoder layers (self_attn + mlp)")
    return best


def find_embedding(model: nn.Module) -> nn.Embedding:
    emb = model.get_input_embeddings()
    if not isinstance(emb, nn.Embedding):
        raise ValueError("input embedding is not nn.Embedding")
    return emb


def write_modules(layer: nn.Module) -> list[nn.Linear]:
    """Linear layers that write into the residual stream in one decoder block."""
    attn_out = getattr(layer.self_attn, "o_proj", None)
    mlp_out = getattr(layer.mlp, "down_proj", None)
    if attn_out is None or mlp_out is None:
        raise ValueError(
            f"{type(layer).__name__}: expected self_attn.o_proj and mlp.down_proj "
            "(MoE experts need per-expert handling, not implemented)"
        )
    return [attn_out, mlp_out]


def chat_batch(tokenizer, prompts: list[str], max_len: int, device: torch.device) -> dict[str, torch.Tensor]:
    texts = [
        tokenizer.apply_chat_template(
            [{"role": "user", "content": p}],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,  # ignored by templates without a thinking switch
        )
        for p in prompts
    ]
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    enc = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=max_len, add_special_tokens=False)
    return {k: v.to(device) for k, v in enc.items()}


@torch.no_grad()
def mean_last_token_states(
    model: nn.Module,
    tokenizer,
    prompts: list[str],
    layer_indices: list[int],
    batch_size: int,
    max_len: int,
) -> dict[int, torch.Tensor]:
    """Mean residual stream at the last prompt token, at the input of each listed layer.

    `hidden_states[i]` from transformers is the residual stream entering layer i
    (index 0 is the embedding output). Means are accumulated in float32 on the CPU.
    """
    device = next(model.parameters()).device
    sums: dict[int, torch.Tensor] = {}
    count = 0
    for start in range(0, len(prompts), batch_size):
        batch = chat_batch(tokenizer, prompts[start : start + batch_size], max_len, device)
        out = model(**batch, output_hidden_states=True, use_cache=False)
        for li in layer_indices:
            h = out.hidden_states[li][:, -1, :].float().cpu()  # left padding: last position is real
            sums[li] = sums.get(li, torch.zeros(h.shape[-1])) + h.sum(dim=0)
        count += batch["input_ids"].shape[0]
    return {li: s / count for li, s in sums.items()}
