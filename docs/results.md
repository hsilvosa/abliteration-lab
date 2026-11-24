# Experimental Results (`thinking = off`)

This document summarizes the first complete evaluation pass across all published `core` models and our four own abliteration iterations (`v1`–`v4`) on `Qwen/Qwen3-4B-Instruct-2507`. All raw numbers and 95% Wilson confidence intervals are in [results/summary.md](../results/summary.md).

## 1. Why a 4-Class Judge Was Needed

The explicit-phrase regex heuristic (`src/abliteration_lab/refusal.py`, `v2`) scored **0%** refusal across every working abliterated model, making them look identical on paper. Manual inspection of the raw replies showed three distinct behaviors hiding behind that `0%`:

- **Safe reframing (`SAFE_REFRAME`)**: opening affirmatively (*"Sure!"*, *"Certainly!"*) and answering a harmless or opposite topic (e.g., a friendly engagement bot instead of a spam bot, or how to *combat* trafficking).
- **Hedged compliance (`HEDGED_COMPLIANCE`)**: answering the literal prompt wrapped in educational, legal, or ethical disclaimers.
- **Direct compliance (`DIRECT_COMPLIANCE`)**: fulfilling the literal request without refusal, pivot, or disclaimer.

Scoring all saved `refusal` (`n = 100`) and `over_refusal` (`n = 250`) replies with the 4-class LLM judge (`v3`, `qwen3-14b-abliterated-mlabonne`, few-shot) exposes the real behavioral spread:

![4-Class Judge Breakdown](assets/refusal_taxonomy_v3.png)

Key observations:
- **`gemma4-12b-qat-hauhaucs` (`76%` direct)** and **`qwen3-14b-abliterated-mlabonne` (`75%` direct)** are the most direct published models, yet still retain `12%`–`19%` safe-reframes.
- **`gemma4-12b-qat-heretic-igorls` (`30%` direct)** shifts heavily into **`44%` hedged compliance** while preserving MMLU (`82.1%`, `+2.1` pts vs baseline).
- **`gemma4-12b-heretic-culturerevolt` (`99%` explicit refusal)** behaves identically to its unmodified baseline when `thinking = off`.

## 2. Own Abliteration Pareto Curve (`Qwen3-4B-Instruct-2507`)

Starting from the full-precision `bf16` weights of `Qwen/Qwen3-4B-Instruct-2507`, we ran four iterations using **norm-preserving projected abliteration** (`src/abliteration_lab/abliterate/`) on a single RTX 3060 12 GB and converted each checkpoint (plus the unmodified source baseline) with the exact same `llama.cpp` `Q4_K_M` pipeline:

| Version | Direction & Edit | `KL` (val) | `SAFE_REFRAME` | `DIRECT_COMPLIANCE` | Over-refusal (v3 eff.) | MMLU (`delta`) | Benign degenerate (`harmless_quality`) |
|---|---|---:|---:|---:|---:|---:|---:|
| `base` | Unmodified `Q4_K_M` (`2.33 GB`) | 0.00 | 0% | 1% | 17.6% | 74.0% | **2%** (`rep4 = 0.016`) |
| `v1` | L25 (`0.7`), `s=1.0`, all + emb | 0.10 | 50% | 3% | 9.6% | 73.3% (-0.7) | **4%** (`rep4 = 0.014`) |
| `v2` | L25 (`0.7`), `s=1.5`, `[0.25,0.95)`, noemb | 0.38 | 48% | 22% | 9.2% | 75.4% (+1.4) | **6%** (`rep4 = 0.019`) |
| **`v4`** | **L18 (`0.5`), `s=1.5`, `[0.25,0.95)`, noemb** | **0.54** | **26%** | **57%** | **6.0%** | **73.0% (-1.0)** | **2%** (`rep4 = 0.017`) |
| `v3` | L18 (`0.5`), `s=2.0`, `[0.15,0.98)`, emb | 3.79 | 14% | 81% | 2.4% | **61.8% (-12.2)** | **64%** (`rep4 = 0.293`) |

![Own Abliteration Pareto Curve](assets/pareto_v1_to_v4.png)

Takeaways:
1. **Depth matters as much as scale**: keeping `v2`'s safe recipe (`scale = 1.5`, `[0.25, 0.95)`, `edit_embeddings = false`, tied `lm_head`) and moving the direction from layer `25` (`0.7`) to layer `18` (`0.5`) in **`v4`** more than doubled direct compliance (`22% -> 57%`), nearly halved safe-reframes (`48% -> 26%`), cut false refusals on XSTest (`17.6% -> 6.0%`), and kept both MMLU (`-1.0` pt) and benign coherence (`2%` degenerate, identical to baseline) intact.
2. **Over-ablation fails catastrophically past `KL ~ 1`**: pushing `scale = 2.0` across `[0.15, 0.98)` with embedding edits in **`v3`** (`KL = 3.79`) pushed direct compliance to `81%`, but dropped MMLU by `-12.2` points and caused **64%** of benign replies to collapse into repetition loops (`92%` hitting the 512-token truncation cap, 18× higher 4-gram repetition).

## 3. Automatic Coherence Detection & Overall Trade-Off

To catch degeneration without relying solely on manual reading, `src/abliteration_lab/coherence.py` computes 4-gram duplicate rates, maximum 5-gram repetition counts, and truncation rates on `harmless_quality` (`n = 50`). Plotting direct compliance against MMLU delta and benign degeneration rate summarizes every abliterated model in one view:

![Capability vs Direct Compliance Trade-Off](assets/capability_vs_compliance.png)

Notice that the automatic detector not only isolates **`v3`** (`64%` degenerate, `-12.2` MMLU pts) — it also flags **`qwen3-14b-abliterated-mlabonne`** (`14%` degenerate, `rep4 = 0.067` vs `0.018` baseline), mirroring its `-6.0` pt MMLU drop, whereas **`gemma4-12b-qat-hauhaucs`**, **`gemma4-12b-qat-heretic-igorls`**, and **`qwen3-4b-instruct-2507-abl-v4`** remain within baseline coherence (`2%`–`6%` degenerate).

## 4. Open Items & Limitations

- All results above use `thinking = off`; `thinking = on` (reasoning traces enabled) remains to be run.
- Judge `v3` (`qwen3-14b-abliterated-mlabonne`) shares a model family with the Qwen3 checkpoints and produced `6`–`27` unparsed items (out of `250`) on `over_refusal`.
- MMLU (`n = 285`, 5 per subject) detects large capability damage (> ~4 pts), not fine differences.

To regenerate all three figures locally:

```bash
python scripts/plot_results.py
```
