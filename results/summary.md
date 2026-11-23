# Evaluation summary

Rates with 95% Wilson intervals.

| model                          | task                                | thinking   |   n |   tok_per_s | role        | baseline       |    rate |   ci_low |   ci_high |
|:-------------------------------|:------------------------------------|:-----------|----:|------------:|:------------|:---------------|--------:|---------:|----------:|
| qwen3-14b-abliterated-mlabonne | harmless_quality                    | off        |  50 |        33.5 | abliterated | qwen3-14b-base | nan     |  nan     |   nan     |
| qwen3-14b-abliterated-mlabonne | mmlu                                | off        | 285 |        33   | abliterated | qwen3-14b-base |   0.712 |    0.657 |     0.762 |
| qwen3-14b-abliterated-mlabonne | over_refusal                        | off        | 250 |        33.5 | abliterated | qwen3-14b-base |   0.004 |    0.001 |     0.022 |
| qwen3-14b-abliterated-mlabonne | over_refusal[judge_refusal]         | off        | 250 |       nan   | abliterated | qwen3-14b-base |   0.052 |    0.031 |     0.087 |
| qwen3-14b-abliterated-mlabonne | over_refusal[judge_refusal+partial] | off        | 250 |       nan   | abliterated | qwen3-14b-base |   0.46  |    0.399 |     0.522 |
| qwen3-14b-abliterated-mlabonne | refusal                             | off        | 100 |        31.8 | abliterated | qwen3-14b-base |   0     |    0     |     0.037 |
| qwen3-14b-abliterated-mlabonne | refusal[judge_refusal]              | off        | 100 |       nan   | abliterated | qwen3-14b-base |   0.8   |    0.711 |     0.867 |
| qwen3-14b-abliterated-mlabonne | refusal[judge_refusal+partial]      | off        | 100 |       nan   | abliterated | qwen3-14b-base |   0.97  |    0.915 |     0.99  |
| qwen3-14b-base                 | harmless_quality                    | off        |  50 |        31.6 | baseline    | nan            | nan     |  nan     |   nan     |
| qwen3-14b-base                 | mmlu                                | off        | 285 |        30   | baseline    | nan            |   0.772 |    0.72  |     0.817 |
| qwen3-14b-base                 | over_refusal                        | off        | 250 |        31.8 | baseline    | nan            |   0.032 |    0.016 |     0.062 |
| qwen3-14b-base                 | over_refusal[judge_refusal]         | off        | 250 |       nan   | baseline    | nan            |   0.08  |    0.052 |     0.12  |
| qwen3-14b-base                 | over_refusal[judge_refusal+partial] | off        | 250 |       nan   | baseline    | nan            |   0.272 |    0.221 |     0.33  |
| qwen3-14b-base                 | refusal                             | off        | 100 |        32.9 | baseline    | nan            |   0.92  |    0.85  |     0.959 |
| qwen3-14b-base                 | refusal[judge_refusal]              | off        | 100 |       nan   | baseline    | nan            |   0.98  |    0.93  |     0.994 |
| qwen3-14b-base                 | refusal[judge_refusal+partial]      | off        | 100 |       nan   | baseline    | nan            |   1     |    0.963 |     1     |

## Abliterated minus baseline

| model                          | baseline       | task                                | thinking   |   rate |   baseline_rate |   delta |
|:-------------------------------|:---------------|:------------------------------------|:-----------|-------:|----------------:|--------:|
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | mmlu                                | off        |  0.712 |           0.772 |  -0.06  |
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | over_refusal                        | off        |  0.004 |           0.032 |  -0.028 |
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | over_refusal[judge_refusal]         | off        |  0.052 |           0.08  |  -0.028 |
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | over_refusal[judge_refusal+partial] | off        |  0.46  |           0.272 |   0.188 |
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | refusal                             | off        |  0     |           0.92  |  -0.92  |
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | refusal[judge_refusal]              | off        |  0.8   |           0.98  |  -0.18  |
| qwen3-14b-abliterated-mlabonne | qwen3-14b-base | refusal[judge_refusal+partial]      | off        |  0.97  |           1     |  -0.03  |
