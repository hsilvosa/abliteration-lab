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
  - experimental
language:
  - en
  - multilingual
---

# Qwen3-4B-Instruct-2507-abl-v3 (Over-Ablated Experimental Checkpoint)

> **Warning — Severe coherence degradation (negative result).** This checkpoint (`scale = 2.0`, `KL = 3.79`) is preserved strictly as a documented failure mode demonstrating the over-ablation boundary. It drops **-12.2 MMLU points** and suffers from repetition loops and lexical corruption on normal prompts. **Use [`hsilvosa/Qwen3-4B-Instruct-2507-abl-v4-GGUF`](https://huggingface.co/hsilvosa/Qwen3-4B-Instruct-2507-abl-v4-GGUF) instead** if you want a coherent checkpoint from this series.
>
> **Research use only — safety guardrails removed.** Not suitable for production or public-facing use.

## Summary

`v3` tested aggressive over-projection (`scale = 2.0`, wider layer window `[0.15, 0.98)`, and embedding orthogonalization) on `Qwen/Qwen3-4B-Instruct-2507`. While it achieved the lowest refusal rate in the `v1`–`v4` series on paper (**81.0%** `DIRECT_COMPLIANCE`, **14.0%** `SAFE_REFRAME`), the high KL shift (**`3.79`**) caused severe collateral damage:

- **MMLU dropped from `74.0%` to `61.8%` (`-12.2` pts)**.
- **Benign generation (`harmless_quality`) broke down**: responses routinely entered infinite repetition loops up to the 512-token limit, exhibited token corruption (e.g., `"Uail Law-Enement"`), and leaked inverted-direction safety tokens into unrelated benign prose (e.g., `"the unethical forest"`, `"the illegal Earth-12"`).

## Provenance and Method

- **Base model**: `Qwen/Qwen3-4B-Instruct-2507`
- **Source revision**: `cdbee75f17c01a7cc42f958dc650907174af0554`
- **License**: Apache-2.0 (inherited from base model)
- **Direction estimator**: `projected` (Lai, 2025) on `256` harmful vs `256` harmless `train` prompts
- **Candidate search (`kl_max = 4.0`)**:
  - Layer `18` (`0.50` depth): `0/64` val refusals, **`KL = 3.7909`** (selected)
  - Layer `25` (`0.70` depth): `0/64` val refusals, `KL = 20.7069` (rejected)
  - Layer `31` (`0.85` depth): `0/64` val refusals, `KL = 18.2657` (rejected)
- **Weight edit**: `norm_preserving` orthogonalization
  - `scale = 2.0` (inverts `-1.0 * r` rather than merely zeroing `r`)
  - `layer_range = [0.15, 0.98)` -> `30` decoder blocks (`layers 5..34`) + `embed_tokens` (`31` modules total)
  - `edit_embeddings = true` (`untied_lm_head = true`, increasing checkpoint size)
- **Hardware / build time**: Single RTX 3060 12 GB (`bfloat16`), `116.5 s` wall time.

## Evaluation (`Q4_K_M`, `thinking = off`)

Evaluated through `llama-server` (`temperature = 0`, `seed = 1234`, `ctx = 8192`, `--jinja`, `enable_thinking = false`) against unmodified `Qwen3-4B-Instruct-2507` (`Q4_K_M`). Rates include 95% Wilson intervals.

| Benchmark / Metric | `qwen3-4b-base` (`Q4_K_M`) | `qwen3-4b-abl-v3` (`Q4_K_M`) | Delta |
|---|---:|---:|---:|
| `refusal` — heuristic v2 (`n = 100`) | 100.0% [96.3, 100.0] | 0.0% [0.0, 3.7] | -100.0 pts |
| `refusal` — judge v3 effective refusal (`EXPLICIT + SAFE_REFRAME`) | 99.0% [94.6, 99.8] | 14.0% [8.5, 22.1] | -85.0 pts |
| `refusal` — judge v3 `DIRECT_COMPLIANCE` | 1.0% [0.2, 5.4] | 81.0% [72.2, 87.5] | +80.0 pts |
| `over_refusal` (`XSTest safe`, `n = 250`) — heuristic v2 | 4.8% [2.8, 8.2] | 0.0% [0.0, 1.5] | -4.8 pts |
| `over_refusal` — judge v3 effective refusal | 17.6% [13.4, 22.8] | 2.4% [1.1, 5.1] | -15.2 pts |
| `over_refusal` — judge v3 `DIRECT_COMPLIANCE` | 72.4% [66.6, 77.6] | 92.8% [88.9, 95.4] | +20.4 pts |
| `mmlu` (5/subject, `n = 285`) | 74.0% [68.6, 78.8] | **61.8%** [56.0, 67.2] | **-12.2 pts** |
| `harmless_quality` (`n = 50`) | Fluent | **Degraded (repetition loops & lexical corruption)** | — |

### Judge v3 4-Class Breakdown (`thinking = off`)

| Task | `EXPLICIT_REFUSAL` | `SAFE_REFRAME` | `HEDGED_COMPLIANCE` | `DIRECT_COMPLIANCE` | `unparsed` |
|---|---:|---:|---:|---:|---:|
| `refusal` (`n = 100`) | 0.0% | 14.0% | 5.0% | 81.0% | 0 |
| `over_refusal` (`n = 250`) | 0.0% | 2.4% | 2.4% | 92.8% | 6 |

## Observed Failure Modes (`harmless_quality`)

Manual inspection of `results/raw/qwen3-4b-instruct-2507-abl-v3/harmless_quality__thinking-off.jsonl` showed:

1. **Repetition collapse**: all 5 inspected benign prompts hit the 512-token cap repeating full sentences or paragraphs (e.g., repeating a 3-sentence paragraph 4 times in a short story, or repeating `"The U.S. Department of the Treasury is responsible..."` 15 times on a 1-sentence factual question).
2. **Inverted-direction token leakage**: because `scale = 2.0` reflects the projection (`x - 2 (x · r) r`), safety-related adjectives leak randomly into benign contexts (`"unethical hotel"`, `"unethical forest"`, `"illegal Earth-12"`, `"harmful sounds"`).
3. **Subword / lexical corruption**: broken token sequences such as `"The Uail Law-Enement agency"`.

Keeping `layer = 18` while lowering `scale` to `1.5`, narrowing `layer_range` to `[0.25, 0.95)`, and disabling `edit_embeddings` (`v4`, `KL = 0.54`) eliminated these artifacts and recovered MMLU to `73.0%` (`-1.0` pt vs baseline).

## Files

- `qwen3-4b-instruct-2507-abl-v3-Q4_K_M.gguf` (`2.53 GB`): quantized GGUF evaluated above (untied `lm_head`)
- `abliteration.json`: exact run configuration, candidate search KL values, and validation metrics
- `refusal_direction.pt`: extracted layer-18 projected refusal direction tensor
- `LICENSE`: Apache-2.0 license inherited from `Qwen/Qwen3-4B-Instruct-2507`

## License and Responsible Use

Inherits the Apache-2.0 license from `Qwen/Qwen3-4B-Instruct-2507`. Intended solely for studying abliteration trade-offs and over-ablation failure modes; do not deploy in production or user-facing applications.
