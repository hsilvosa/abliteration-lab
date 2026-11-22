# Abliteration techniques

This document explains the methods behind refusal ablation, from the original paper to recent variants, and states which ones this repository implements.

## 1. Core idea

Arditi et al. (2024), "Refusal in Language Models Is Mediated by a Single Direction" (arXiv:2406.11717), show that in many chat models the decision to refuse is represented by one direction `r` in the residual stream. Two interventions follow:

- Adding `r` to the residual stream makes the model refuse harmless requests.
- Removing `r` everywhere makes the model comply with requests it would refuse.

"Abliteration" (ablation + obliteration) is the name the community uses for the second intervention when it is written into the weights.

## 2. Estimating the refusal direction

**Difference of means.** Run two prompt sets through the model: prompts it refuses (harmful) and prompts it answers (harmless). At a chosen layer `l`, take the residual stream at the last prompt token (the position just before generation) and average each set:

```
r_l = normalize( mean(h_l | harmful) - mean(h_l | harmless) )
```

A few hundred prompts per set are enough. Implemented in `abliterate/directions.py::mean_diff` and `abliterate/activations.py::mean_last_token_states`.

**Projected direction.** Lai (2025, "projected abliteration") observes that `r` contains a component parallel to the mean harmless activation, which carries general signal. Removing it gives:

```
mu = normalize( mean(h_l | harmless) )
r' = normalize( r - (r . mu) mu )
```

This reduces collateral damage with similar refusal removal. Implemented as `projected` (default in `configs/abliterate.toml`).

**Layer choice.** The direction is computed at several depths (default: 30, 40, 50, 60 and 70 percent). Middle layers usually work best; early layers have not yet formed the concept, late layers are too close to the output.

## 3. Removing the direction

**Inference-time ablation.** For every activation `x` written into the residual stream, subtract its projection: `x' = x - (x . r) r`. It is applied to the outputs of the token embedding, every attention output projection (`o_proj`) and every MLP output projection (`down_proj`). Nothing writes along `r`, so `r` never appears in the residual stream. This is reversible and is used here to score candidates (`abliterate/hooks.py`).

**Weight orthogonalization.** The same operation folded into the weights. For a Linear layer whose output is the residual stream, `W` has shape `(d_model, d_in)`:

```
W' = W - r r^T W
```

For the embedding matrix `E` of shape `(vocab, d_model)`: `E' = E - (E r) r^T`. Biases, if any: `b' = b - (b . r) r`. The edited model has the same architecture and the same inference cost as the original and can be converted to GGUF normally. Implemented in `abliterate/edit.py`. A unit test checks that the weight edit and the hooks give identical outputs on a toy decoder.

Tied embeddings: when `lm_head` shares the embedding matrix, editing the embedding would also change the output projection. The pipeline unties them first (`untie_lm_head`).

**Norm-preserving edit.** Removing a component shrinks each column of `W`. Lai (2025, "norm-preserving biprojected abliteration") restores each column to its original norm after the projection. Rescaling keeps the column orthogonal to `r`, so refusal removal is unchanged, while activation magnitudes stay closer to the original. Implemented as `mode = "norm_preserving"` (default).

**Scale and layer range.** `scale < 1` removes only part of the component; restricting the edit to a range of layers leaves early and late layers intact. Published models often edit only the middle layers (for example huihui-ai's Qwen3.8 27B, layers 22 to 52). Both are configurable.

## 4. Choosing a candidate

Each candidate direction is scored with hooks on prompts not used to compute it:

- **Refusals**: greedy replies to held-out harmful prompts, counted with the heuristic in `refusal.py`.
- **KL divergence**: `KL(original || edited)` of the first-token distribution on held-out harmless prompts. This is the metric Heretic uses. Low KL means the model behaves like the original on normal requests.

Rule (declared in `configs/abliterate.toml`): minimum refusals among candidates with `KL <= kl_max`, ties broken by lower KL.

## 5. Variants not implemented here

| Technique | What it does | Why not here |
|---|---|---|
| Heretic (p-e-w) | Searches layer-dependent ablation weights with Optuna (TPE), co-minimizing refusals and KL. Fully automatic. | Available as `pip install heretic-llm`; better used directly. Its results serve as a reference. |
| Arbitrary-Rank Ablation (ARA, Heretic) | Removes a subspace instead of a single direction. | Experimental upstream. |
| Expert-Granular Abliteration | For MoE models, computes and removes directions per expert. | Our edit supports dense MLPs only (`down_proj`); MoE models raise an error. |
| Layer-wise directions (mlabonne Gemma 3) | A separate direction per layer, with a refusal weight. | Possible extension of `apply_edit`. |
| Healing fine-tune | A short DPO or SFT pass after ablation to recover lost quality (e.g. NeuralDaredevil). | Out of scope for a first run; needs a preference dataset and more GPU time. |
| Thinking-mode ablation | For reasoning models, the refusal forms inside the reasoning trace; directions must be computed with thinking enabled (igorls Gemma 4 v1.1). | The pipeline disables thinking in the chat template. The evaluation runs both modes, so the gap is measured. |

## 6. Known limits

- One direction is a simplification. Residual refusals and soft deflections often remain.
- Abliteration removes refusal; it adds no knowledge. Answers can be wrong or incoherent.
- Capability usually drops slightly (cards report about 0.6 to 0.9 MMLU points for good Heretic runs); poor runs damage reasoning and instruction following much more.
- The refusal heuristic is a proxy. Raw outputs are saved so a stricter judge can be applied later.
- Quantization adds its own damage. Comparisons in this repo always pair a model with a baseline at the same quant type.

## References

- Arditi et al., 2024. Refusal in Language Models Is Mediated by a Single Direction. arXiv:2406.11717.
- M. Labonne, 2024. Uncensor any LLM with abliteration. Hugging Face blog.
- J. Lai, 2025. Projected abliteration; Norm-preserving biprojected abliteration. Hugging Face blog (grimjim).
- p-e-w, Heretic. github.com/p-e-w/heretic.
- FailSpy, abliterator. github.com/FailSpy/abliterator.
- Sumandora, remove-refusals-with-transformers. github.com/Sumandora/remove-refusals-with-transformers.
- Röttger et al., 2024. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours. NAACL.
