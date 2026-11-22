# abliteration-lab

Tools to download, evaluate and build abliterated (refusal-ablated) language models on a single RTX 3060 12 GB.

The project answers two questions:

1. How much refusal does each published abliterated model remove, and what does it cost in capability and over-refusal, compared with its own unmodified baseline at the same quantization?
2. Can the same result be reproduced from scratch with the techniques in `docs/techniques.md`, and how does our own edit compare?

## Status

Infrastructure only. Nothing has been downloaded, run or measured yet. Every number in the docs is quoted from a model card and is labeled as such.

| Part | State |
|---|---|
| Model registry (`configs/models.toml`), repo and file names checked against the Hugging Face API on 2026-11-22 | ready |
| Downloader to `D:\models` (dry run by default, size checks, manifests, sha256 verify) | ready, not run |
| GGUF evaluation through `llama-server` (refusal, over-refusal, MMLU, speed) | ready, not run |
| Report with Wilson intervals and paired deltas | ready, not run |
| Own abliteration pipeline (directions, hook scoring, weight edit) | ready, not run |
| Unit tests (config, scoring, edit math on a toy decoder) | written, not run |

## Layout

```
configs/
  models.toml        model registry: groups, exact files, baselines, card claims
  datasets.toml      prompt and benchmark datasets
  eval.toml          llama-server and task settings, per-model overrides
  abliterate.toml    own abliteration run settings
src/abliteration_lab/
  download.py        Hub downloads, manifests, verification
  prompts.py         dataset loaders and fixed samples
  refusal.py         refusal heuristic
  mmlu.py            MMLU prompt and answer parsing
  server.py          llama-server lifecycle and chat calls
  eval_gguf.py       resumable evaluation, raw JSONL per model and task
  report.py          summary table, Wilson intervals, paired deltas
  abliterate/        activations, directions, hooks, weight edit, scoring, pipeline
  cli.py             `abl` command
scripts/
  setup_env.sh       uv virtualenv (base or full)
  convert_to_gguf.sh own checkpoint to GGUF + quantization
docs/                techniques, models, evaluation protocol, hardware, responsible use
tests/
```

Model weights never go into the repo. They live under `D:\models\<group>\<id>\` (override with `ABL_MODELS_DIR`). Datasets go to `data/raw/` and results to `results/`; both are git-ignored except the summaries you choose to commit.

## Quickstart

```bash
scripts/setup_env.sh            # base: download, eval, report
source .venv/Scripts/activate

abl list                        # registry
abl download                    # dry run for the core group: files, sizes, free space
abl download --yes              # download core (~54 GB)
abl download --group small --yes
abl download --verify           # sha256 against the Hub LFS hashes

abl datasets --yes              # harmful/harmless prompts, XSTest, MMLU

abl eval --model gemma4-e4b-heretic-llmfan46 --limit 5   # smoke test
abl eval                        # all core models, all tasks, thinking off
abl eval --thinking on          # second pass with reasoning enabled
abl report                      # results/summary.md
```

Own abliteration (needs `scripts/setup_env.sh full`):

```bash
abl download --group source --yes
abl abliterate --dry-run
abl abliterate
LLAMA_CPP_DIR=/path/to/llama.cpp scripts/convert_to_gguf.sh qwen3-4b-instruct-2507-abl
abl eval --own qwen3-4b-instruct-2507-abl --file qwen3-4b-instruct-2507-abl-Q4_K_M.gguf
```

## Model groups

| Group | Purpose | Download size |
|---|---|---|
| core | three Gemma 4 12B variants and Qwen3-14B abliterated, each with its baseline | ~54 GB |
| small | Gemma 4 E4B Heretic, fast pipeline checks | ~5 GB |
| extended | Qwen3.8 27B and two Gemma 4 26B-A4B MoE builds; need CPU offload | ~48 GB |
| source | Qwen3-4B-Instruct-2507 in bf16 for our own abliteration | ~8 GB |

Details, licenses and card claims: [docs/models.md](docs/models.md).

## Documentation

- [docs/techniques.md](docs/techniques.md): how abliteration works, the variants, and which ones this repo implements.
- [docs/evaluation-protocol.md](docs/evaluation-protocol.md): datasets, splits, metrics and rules, declared before any run.
- [docs/models.md](docs/models.md): the registry explained.
- [docs/hardware.md](docs/hardware.md): VRAM budget, offload settings and time estimates for the RTX 3060.
- [docs/responsible-use.md](docs/responsible-use.md): scope and licenses.

## Requirements

- Python 3.11+ and `uv`.
- `llama-server` on PATH. The installed winget build is b10615; Gemma 4 and Qwen3.8 GGUFs may need a newer one (`winget upgrade ggml.llamacpp`). If a model fails to load, check `results/logs/<id>.server.log` first.
- For own abliteration: CUDA PyTorch, `transformers`, and a llama.cpp source checkout for GGUF conversion.
