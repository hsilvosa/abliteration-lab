# Evaluation protocol

Declared before any run. Changes after the first results must be added to the change log at the end, with the reason, and both versions of affected numbers must be kept.

## Question

For each abliterated model: how many harmful prompts does it still refuse, how many safe prompts does it wrongly refuse, and how much capability does it lose, compared with its unmodified baseline at the same quantization type?

## Pairs

| Abliterated | Baseline | Quant match |
|---|---|---|
| gemma4-12b-qat-hauhaucs | gemma4-12b-qat-base | Q4_K_M vs Q4_0 (same QAT source weights, different grid) |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base | Q4_K_M vs Q4_K_M |
| gemma4-12b-qat-heretic-igorls | gemma4-12b-qat-base | Q4_0 vs Q4_0 |
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | Q4_K_M vs Q4_K_M, same quantizer |

The first pair is not a clean quant match; its deltas mix abliteration and quantization effects and are reported with that note. Extended and small models have no baseline in the registry and are reported alone.

## Datasets and splits

| Task | Source | Items | Use |
|---|---|---|---|
| refusal | mlabonne/harmful_behaviors, `test` split | first 100 | refusal rate on harmful prompts |
| over_refusal | Paul/XSTest, `label == safe` | all 250 | false refusals on safe prompts |
| mmlu | cais/mmlu `all/test` | 5 per subject, seed 0 (285) | capability, exact letter match |
| harmless_quality | mlabonne/harmless_alpaca, `test` split | first 50 | saved for side-by-side reading, not scored |

Own abliteration uses only the `train` splits: the first 256 harmful and harmless prompts for directions, the last 64 harmful train prompts for selection, and harmless train prompts 256 to 319 for KL. No evaluation prompt is seen during direction estimation or selection.

## Generation settings

- llama-server, one model at a time, `temperature = 0`, `seed = 1234`, `max_tokens = 512` (8 for MMLU with thinking off).
- Chat template from the GGUF (`--jinja`), single user turn, no system prompt.
- Thinking: first pass `off` (`enable_thinking = false`), second pass `on`. Reasoning text is stored separately and not scored for refusal.

## Metrics

- **Refusal rate** = refused / n, with the marker heuristic in `src/abliteration_lab/refusal.py` applied to the final answer (first 300 characters).
- **Over-refusal rate**: same heuristic on XSTest safe prompts.
- **MMLU accuracy**: parsed letter equals the gold answer; unparsable replies count as wrong and are counted separately.
- **Speed**: mean `predicted_per_second` from llama-server timings.
- All rates with 95% Wilson intervals. Paired delta = abliterated rate minus baseline rate.

## Reading rules

- Differences whose intervals overlap substantially are reported as unresolved. With n = 100, a refusal-rate interval is roughly plus or minus 10 points near 50% and about 4 points near 0%.
- With 285 MMLU items, differences under about 4 points are within noise; the MMLU sample detects large damage, not fine differences.
- A model is not called "better" overall; each axis is reported separately.
- Before trusting the refusal heuristic for a model, read 20 of its raw replies per task and note disagreements in the results doc.

## Run order

1. `abl eval --model gemma4-e4b-heretic-llmfan46 --limit 5` to check the pipeline end to end.
2. Core baselines, then core abliterated models, thinking off.
3. Same, thinking on.
4. Extended models, if time allows.
5. Own abliteration, then its GGUF evaluated with the same settings (baseline: the same source model converted without edits).

## Change log

- 2026-11-22: protocol declared. No runs yet.
