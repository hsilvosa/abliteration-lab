# Models

All entries live in `configs/models.toml`. Repo ids, file names and sizes were checked against the Hugging Face API on 2026-11-22. "Card claims" are the uploader's own numbers, measured with their own prompt sets; they are not comparable across cards and are not results of this repo.

Files are stored under `D:\models\<group>\<id>\`, each with a `manifest.json` (repo, revision, sizes, sha256).

## core (~54 GB)

| id | Repo | File | GB | License | Method | Card claims |
|---|---|---|---|---|---|---|
| gemma4-12b-qat-hauhaucs | HauhauCS/Gemma4-12B-QAT-Uncensored-HauhauCS-Balanced | Q4_K_M | 7.38 | gemma | undisclosed, from QAT weights | 0/465 refusals |
| gemma4-12b-heretic-culturerevolt | culturerevolt/gemma-4-12b-heretic-abliterated-GGUF | Q4_K_M | 7.38 | apache-2.0 | Heretic | none recorded |
| gemma4-12b-qat-heretic-igorls | igorls/gemma-4-12B-it-qat-q4_0-unquantized-heretic-GGUF | Q4_0 | 6.98 | apache-2.0 | Heretic 1.3.0, thinking on | KL 0.32, ~22% refusals (thinking on) |
| qwen3-14b-abliterated-mlabonne | bartowski/mlabonne_Qwen3-14B-abliterated-GGUF | Q4_K_M | 9.00 | apache-2.0 | classic abliteration | none recorded |
| gemma4-12b-qat-base | google/gemma-4-12b-it-qat-q4_0-gguf | Q4_0 | 6.98 | apache-2.0 | baseline | |
| gemma4-12b-base | unsloth/gemma-4-12b-it-GGUF | Q4_K_M | 7.12 | apache-2.0 | baseline | |
| qwen3-14b-base | bartowski/Qwen_Qwen3-14B-GGUF | Q4_K_M | 9.00 | apache-2.0 | baseline | |

Optional files (`--with-optional`): vision projectors (mmproj) for the Gemma models. The evaluation is text-only and does not need them.

## small (~5 GB)

| id | Repo | File | GB | Card claims |
|---|---|---|---|---|
| gemma4-e4b-heretic-llmfan46 | llmfan46/gemma-4-E4B-it-ultra-uncensored-heretic-GGUF | Q4_K_M | 5.34 | 3/100 refusals, KL 0.0076, MMLU 68.60 vs 69.46 |

## extended (~48 GB)

These exceed 12 GB VRAM and run with partial CPU offload (see `docs/hardware.md`).

| id | Repo | File | GB | Card claims |
|---|---|---|---|---|
| qwen3.8-27b-abliterated-huihui | huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF | UD-IQ4_XS | 14.40 | no evals in card |
| gemma4-26b-a4b-qat-hauhaucs | HauhauCS/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-MTP | Q4_K_M | 16.80 | none recorded |
| gemma4-26b-a4b-trevorjs | TrevorJS/gemma-4-26B-A4B-it-uncensored-GGUF | Q4_K_M | 16.80 | 1/100 refusals, KL 0.09 (via third-party summary) |

## source (~8 GB)

| id | Repo | Format | GB | Use |
|---|---|---|---|---|
| qwen3-4b-instruct-2507 | Qwen/Qwen3-4B-Instruct-2507 | safetensors bf16 | 8.05 | input for `abl abliterate` |

Qwen3-4B-Instruct-2507 is a non-thinking model with a dense MLP, which fits the implemented edit and the 12 GB GPU in bf16. Heretic's own `p-e-w/Qwen3-4B-Instruct-2507-heretic` gives a published reference for the same base.

## Adding a model

1. Check the repo and exact file names: `https://huggingface.co/api/models/<repo>`.
2. Add a `[[models]]` entry with a unique `id`, the group, the role and, for abliterated models, a `baseline` id at the same quant type when one exists.
3. `abl download --model <id>` to see the plan, then `--yes`.
