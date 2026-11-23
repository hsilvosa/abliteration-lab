# Evaluation summary

Rates with 95% Wilson intervals.

| model                            | task             | thinking   |   n |   tok_per_s | role        | baseline            |    rate |   ci_low |   ci_high |
|:---------------------------------|:-----------------|:-----------|----:|------------:|:------------|:--------------------|--------:|---------:|----------:|
| gemma4-12b-base                  | harmless_quality | off        |  50 |        26   | baseline    | nan                 | nan     |  nan     |   nan     |
| gemma4-12b-base                  | mmlu             | off        | 285 |        25.8 | baseline    | nan                 |   0.779 |    0.727 |     0.823 |
| gemma4-12b-base                  | over_refusal     | off        | 250 |        29.9 | baseline    | nan                 |   0.02  |    0.009 |     0.046 |
| gemma4-12b-base                  | refusal          | off        | 100 |        30.9 | baseline    | nan                 |   0.99  |    0.946 |     0.998 |
| gemma4-12b-heretic-culturerevolt | harmless_quality | off        |  50 |        29.5 | abliterated | gemma4-12b-base     | nan     |  nan     |   nan     |
| gemma4-12b-heretic-culturerevolt | mmlu             | off        | 285 |        29   | abliterated | gemma4-12b-base     |   0.804 |    0.753 |     0.845 |
| gemma4-12b-heretic-culturerevolt | over_refusal     | off        | 250 |        25.6 | abliterated | gemma4-12b-base     |   0.016 |    0.006 |     0.04  |
| gemma4-12b-heretic-culturerevolt | refusal          | off        | 100 |        24.5 | abliterated | gemma4-12b-base     |   0.99  |    0.946 |     0.998 |
| gemma4-12b-qat-base              | harmless_quality | off        |  50 |        33.4 | baseline    | nan                 | nan     |  nan     |   nan     |
| gemma4-12b-qat-base              | mmlu             | off        | 285 |        34   | baseline    | nan                 |   0.8   |    0.75  |     0.842 |
| gemma4-12b-qat-base              | over_refusal     | off        | 250 |        35.2 | baseline    | nan                 |   0.008 |    0.002 |     0.029 |
| gemma4-12b-qat-base              | refusal          | off        | 100 |        36.4 | baseline    | nan                 |   0.98  |    0.93  |     0.994 |
| gemma4-12b-qat-hauhaucs          | harmless_quality | off        |  50 |        24.7 | abliterated | gemma4-12b-qat-base | nan     |  nan     |   nan     |
| gemma4-12b-qat-hauhaucs          | mmlu             | off        | 285 |        24.4 | abliterated | gemma4-12b-qat-base |   0.779 |    0.727 |     0.823 |
| gemma4-12b-qat-hauhaucs          | over_refusal     | off        | 250 |        26.2 | abliterated | gemma4-12b-qat-base |   0     |    0     |     0.015 |
| gemma4-12b-qat-hauhaucs          | refusal          | off        | 100 |        24.7 | abliterated | gemma4-12b-qat-base |   0     |    0     |     0.037 |
| gemma4-12b-qat-heretic-igorls    | harmless_quality | off        |  50 |        35.1 | abliterated | gemma4-12b-qat-base | nan     |  nan     |   nan     |
| gemma4-12b-qat-heretic-igorls    | mmlu             | off        | 285 |        34.1 | abliterated | gemma4-12b-qat-base |   0.821 |    0.772 |     0.861 |
| gemma4-12b-qat-heretic-igorls    | over_refusal     | off        | 250 |        35.5 | abliterated | gemma4-12b-qat-base |   0     |    0     |     0.015 |
| gemma4-12b-qat-heretic-igorls    | refusal          | off        | 100 |        35.8 | abliterated | gemma4-12b-qat-base |   0     |    0     |     0.037 |
| qwen3-14b-abliterated-mlabonne   | harmless_quality | off        |  50 |        33.5 | abliterated | qwen3-14b-base      | nan     |  nan     |   nan     |
| qwen3-14b-abliterated-mlabonne   | mmlu             | off        | 285 |        33   | abliterated | qwen3-14b-base      |   0.712 |    0.657 |     0.762 |
| qwen3-14b-abliterated-mlabonne   | over_refusal     | off        | 250 |        33.5 | abliterated | qwen3-14b-base      |   0.004 |    0.001 |     0.022 |
| qwen3-14b-abliterated-mlabonne   | refusal          | off        | 100 |        31.8 | abliterated | qwen3-14b-base      |   0     |    0     |     0.037 |
| qwen3-14b-base                   | harmless_quality | off        |  50 |        31.6 | baseline    | nan                 | nan     |  nan     |   nan     |
| qwen3-14b-base                   | mmlu             | off        | 285 |        30   | baseline    | nan                 |   0.772 |    0.72  |     0.817 |
| qwen3-14b-base                   | over_refusal     | off        | 250 |        31.8 | baseline    | nan                 |   0.032 |    0.016 |     0.062 |
| qwen3-14b-base                   | refusal          | off        | 100 |        32.9 | baseline    | nan                 |   0.92  |    0.85  |     0.959 |

## Abliterated minus baseline

| model                            | baseline            | task         | thinking   |   rate |   baseline_rate |   delta |
|:---------------------------------|:--------------------|:-------------|:-----------|-------:|----------------:|--------:|
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base     | mmlu         | off        |  0.804 |           0.779 |   0.025 |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base     | over_refusal | off        |  0.016 |           0.02  |  -0.004 |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base     | refusal      | off        |  0.99  |           0.99  |   0     |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base | mmlu         | off        |  0.779 |           0.8   |  -0.021 |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base | over_refusal | off        |  0     |           0.008 |  -0.008 |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base | refusal      | off        |  0     |           0.98  |  -0.98  |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base | mmlu         | off        |  0.821 |           0.8   |   0.021 |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base | over_refusal | off        |  0     |           0.008 |  -0.008 |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base | refusal      | off        |  0     |           0.98  |  -0.98  |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base      | mmlu         | off        |  0.712 |           0.772 |  -0.06  |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base      | over_refusal | off        |  0.004 |           0.032 |  -0.028 |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base      | refusal      | off        |  0     |           0.92  |  -0.92  |
