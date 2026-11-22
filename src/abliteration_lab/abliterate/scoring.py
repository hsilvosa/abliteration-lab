"""First-token KL divergence and greedy refusal scoring for candidate selection."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn

from ..refusal import is_refusal
from .activations import chat_batch


@torch.no_grad()
def first_token_logprobs(model: nn.Module, tokenizer, prompts: list[str], batch_size: int, max_len: int) -> torch.Tensor:
    """Log-probabilities of the first generated token, shape (n_prompts, vocab), on the CPU."""
    device = next(model.parameters()).device
    out = []
    for start in range(0, len(prompts), batch_size):
        batch = chat_batch(tokenizer, prompts[start : start + batch_size], max_len, device)
        logits = model(**batch, use_cache=False).logits[:, -1, :].float()
        out.append(F.log_softmax(logits, dim=-1).cpu())
    return torch.cat(out)


def kl_divergence(ref_logprobs: torch.Tensor, new_logprobs: torch.Tensor) -> float:
    """Mean KL(ref || new) over prompts (Heretic's harmless-prompt metric)."""
    kl = F.kl_div(new_logprobs, ref_logprobs, log_target=True, reduction="batchmean")
    return float(kl)


@torch.no_grad()
def greedy_replies(
    model: nn.Module, tokenizer, prompts: list[str], batch_size: int, max_len: int, max_new_tokens: int
) -> list[str]:
    device = next(model.parameters()).device
    replies: list[str] = []
    for start in range(0, len(prompts), batch_size):
        batch = chat_batch(tokenizer, prompts[start : start + batch_size], max_len, device)
        gen = model.generate(
            **batch,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
        )
        new = gen[:, batch["input_ids"].shape[1] :]
        replies += tokenizer.batch_decode(new, skip_special_tokens=True)
    return replies


def count_refusals(replies: list[str]) -> int:
    return sum(is_refusal(r) for r in replies)
