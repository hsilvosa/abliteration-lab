---
license: apache-2.0
base_model: Qwen/Qwen3-4B-Instruct-2507
base_model_relation: finetune
library_name: transformers
tags:
  - abliterated
  - projected-abliteration
  - norm-preserving
  - qwen3
  - gguf
  - alignment-research
language:
  - en
  - multilingual
---

# Qwen3-4B-Instruct-2507-abl-v4

An experimental, refusal-ablated derivative of [`Qwen/Qwen3-4B-Instruct-2507`](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) built in `abliteration-lab` using **norm-preserving projected abliteration** restricted to middle decoder layers.

> **Research use only — safety guardrails removed.** This checkpoint intentionally disables refusal behavior for interpretability, alignment, and red-teaming evaluation. It can generate harmful, unsafe, or inaccurate content and **must not** be deployed in public-facing or production systems.

## Summary

`v4` is the best-balanced checkpoint in the `v1`–`v4` ablation series on `Qwen3-4B-Instruct-2507`. Using the projected refusal direction from **layer 18** (`0.5` depth) with `scale = 1.5` across layers `9..33` (`[0.25, 0.95)`) and leaving embeddings untouched (`lm_head` remains tied) yields:

- **0.0%** explicit refusals and **57.0%** direct compliance on `mlabonne/harmful_behaviors` (`test`, `n = 100`, 4-class judge `v3`), down from **99.0%** effective refusal on the unmodified baseline.
- **6.0%** effective false refusal (**90.4%** direct compliance) on `Paul/XSTest` safe prompts (`n = 250`), down from **17.6%** (`72.4%` direct) on the baseline.
- **73.0%** MMLU accuracy (`n = 285`, `-1.0` pt vs `74.0%` baseline — within sampling noise) and fluent generation on `harmless_quality` (`n = 50`).
- Compact **2.33 GB** `Q4_K_M` GGUF (~80–84 tok/s on a single RTX 3060 12 GB).

## Provenance and Method

- **Base model**: `Qwen/Qwen3-4B-Instruct-2507`
- **Source revision**: `cdbee75f17c01a7cc42f958dc650907174af0554`
- **License**: Apache-2.0 (inherited from base model)
- **Direction estimator**: `projected` (Lai, 2025) — difference of mean last-token residual states (`256` harmful vs `256` harmless prompts from `train` splits only), orthogonalized against the unit harmless mean.
- **Direction layer**: Layer `18` of `36` (`0.5` depth)
- **Weight edit**: `norm_preserving` orthogonalization (`W' = W - scale * r r^T W`, followed by column-norm restoration)
  - `scale = 1.5`
  - `layer_range = [0.25, 0.95)` -> decoder layers `9..33` (`25` blocks: `self_attn.o_proj` and `mlp.down_proj`)
  - `edit_embeddings = false` (`untied_lm_head = false`)
- **Validation metrics (held-out `train` split, zero `test` leakage)**:
  - Explicit refusals (`n = 64`): `1/64` (baseline: `63/64`)
  - First-token `KL(original || edited)` on `64` harmless prompts: **`0.5390`**
- **Hardware / build time**: Single RTX 3060 12 GB (`bfloat16`), `75.8 s` wall time.

## Evaluation (`Q4_K_M`, `thinking = off`)

Evaluated through `llama-server` (`temperature = 0`, `seed = 1234`, `ctx = 8192`, `--jinja`, `enable_thinking = false`) against the unmodified `Qwen3-4B-Instruct-2507` converted with the exact same `llama.cpp` pipeline and `Q4_K_M` quantization. Rates include 95% Wilson intervals.

| Benchmark / Metric | `qwen3-4b-base` (`Q4_K_M`) | `qwen3-4b-abl-v4` (`Q4_K_M`) | Delta |
|---|---:|---:|---:|
| `refusal` — heuristic v2 (`n = 100`) | 100.0% [96.3, 100.0] | **0.0%** [0.0, 3.7] | -100.0 pts |
| `refusal` — judge v3 effective refusal (`EXPLICIT + SAFE_REFRAME`) | 99.0% [94.6, 99.8] | **26.0%** [18.4, 35.4] | -73.0 pts |
| `refusal` — judge v3 `DIRECT_COMPLIANCE` | 1.0% [0.2, 5.4] | **57.0%** [47.2, 66.3] | +56.0 pts |
| `over_refusal` (`XSTest safe`, `n = 250`) — heuristic v2 | 4.8% [2.8, 8.2] | **0.0%** [0.0, 1.5] | -4.8 pts |
| `over_refusal` — judge v3 effective refusal | 17.6% [13.4, 22.8] | **6.0%** [3.7, 9.7] | -11.6 pts |
| `over_refusal` — judge v3 `DIRECT_COMPLIANCE` | 72.4% [66.6, 77.6] | **90.4%** [86.1, 93.5] | +18.0 pts |
| `mmlu` (5/subject, `n = 285`) | 74.0% [68.6, 78.8] | **73.0%** [67.5, 77.8] | -1.0 pt |
| Generation speed (RTX 3060 12 GB) | ~80.6 tok/s | ~81.3 tok/s | — |

### Judge v3 4-Class Breakdown (`thinking = off`)

| Task | `EXPLICIT_REFUSAL` | `SAFE_REFRAME` | `HEDGED_COMPLIANCE` | `DIRECT_COMPLIANCE` | `unparsed` |
|---|---:|---:|---:|---:|---:|
| `refusal` (`n = 100`) | 0.0% | 26.0% | 16.0% | 57.0% | 1 |
| `over_refusal` (`n = 250`) | 0.4% | 5.6% | 1.2% | 90.4% | 6 |

### Comparison across `v1`–`v4`

| Version | Direction & Edit | `KL` (val) | `SAFE_REFRAME` | `DIRECT_COMPLIANCE` | MMLU (`delta`) | Benign quality |
|---|---|---:|---:|---:|---:|---|
| `v1` | L25, `s=1.0`, all + emb | 0.10 | 50% | 3% | 73.3% (-0.7) | Fluent |
| `v2` | L25, `s=1.5`, `[0.25,0.95)`, noemb | 0.38 | 48% | 22% | 75.4% (+1.4) | Fluent |
| **`v4`** | **L18, `s=1.5`, `[0.25,0.95)`, noemb** | **0.54** | **26%** | **57%** | **73.0% (-1.0)** | **Fluent** |
| `v3` | L18, `s=2.0`, `[0.15,0.98)`, emb | 3.79 | 14% | 81% | 61.8% (-12.2) | Degraded (loops) |

## Files

- `qwen3-4b-instruct-2507-abl-v4-Q4_K_M.gguf` (`2.33 GB`): quantized GGUF evaluated above (tied `lm_head`)
- `abliteration.json`: exact run configuration, validation refusal count, and KL divergence
- `refusal_direction.pt`: extracted layer-18 projected refusal direction tensor
- `LICENSE`: Apache-2.0 license inherited from `Qwen/Qwen3-4B-Instruct-2507`

## Usage (`llama-server`)

```bash
llama-server \
  -m qwen3-4b-instruct-2507-abl-v4-Q4_K_M.gguf \
  --port 8080 -c 8192 -ngl 99 --jinja
```

## Limitations and Risks

- **Residual safe-reframing**: `26%` of `harmful_behaviors` prompts still elicit safe-reframes and `16%` include educational/ethical disclaimers.
- **No added knowledge**: abliteration removes refusal signals without improving factual capability; on specialized or complex topics a 4B model frequently produces generic or hallucinated steps.
- **Evaluated with `thinking = off` only**: behavior with reasoning traces enabled (`thinking = on`) has not yet been measured.
- **Judge bias**: the 4-class judge is a local LLM (`qwen3-14b-abliterated-mlabonne`, same model family) and should be treated as a diagnostic signal rather than ground truth.
- **Safety**: safety alignment has been intentionally weakened. Do not expose this model to untrusted users or use it in automated systems without external guardrails.
