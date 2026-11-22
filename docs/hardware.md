# Hardware notes (RTX 3060 12 GB, 32 GB RAM)

## VRAM budget

Weights plus KV cache plus about 0.5 GB of runtime buffers must fit in 12 GB for full GPU offload. Rule of thumb: pick a file 1.5 to 3 GB smaller than VRAM.

| Model class | File | Fits fully on GPU | Setting |
|---|---|---|---|
| Gemma 4 E4B Q4_K_M | 5.3 GB | yes, long context | default |
| Gemma 4 12B Q4_0 / Q4_K_M | 7.0 to 7.4 GB | yes, 8K context easily | default (`-ngl 99`, `-c 8192`) |
| Qwen3-14B Q4_K_M | 9.0 GB | yes, 8K context | default; lower `ctx_size` if loading fails |
| Gemma 4 26B-A4B Q4_K_M (MoE) | 16.8 GB | no | `--n-cpu-moe 12`: expert weights of the first 12 layers stay in RAM |
| Qwen3.8 27B UD-IQ4_XS (dense) | 14.4 GB | no | `-ngl 40`: remaining layers run on CPU, expect a large slowdown |

The overrides live in `configs/eval.toml` under `[overrides."<id>"]`. They are starting points, not measured values; adjust after the first load.

## Keeping the PC usable

- One model and one llama-server at a time, single slot (`-np 1`).
- `threads = 4` in `configs/eval.toml` caps CPU use during generation.
- Evaluation writes each reply as it arrives and resumes from the JSONL files, so a run can be stopped at any time (Ctrl+C) and restarted with the same command.

## Time estimates

No measured basis yet. Before the first full run, time the smoke test (`--limit 5`) and multiply:

```
items per model ~ 100 refusal + 250 over-refusal + 285 MMLU + 50 harmless = 685
time per model ~ sum over tasks of (items x mean reply tokens / tok_per_s)
```

MMLU replies are a few tokens; refusal and harmless replies can reach the 512-token cap. Thinking-on runs produce long reasoning traces and are several times slower. Record the measured seconds per item in the results doc and estimate the rest from it.

## Own abliteration

Qwen3-4B-Instruct-2507 in bf16 needs about 8 GB for weights. Activation collection with batch 16 and 256-token prompts should fit in the remaining memory; if it does not, lower `batch_size`. `load_in_4bit = true` runs the direction search only (4-bit weights cannot be edited and saved), which is useful for models too large for bf16.

## Disk

`D:` had 459 GB free on 2026-11-22. Core plus small plus source is about 67 GB; adding extended brings it to about 115 GB. The downloader refuses to start when the planned size plus a 20 GB margin exceeds free space.
