# Evaluation summary

Rates with 95% Wilson intervals.

| model                            | task                           | thinking   |   n |   tok_per_s | role        | baseline                    |    rate |   ci_low |   ci_high |
|:---------------------------------|:-------------------------------|:-----------|----:|------------:|:------------|:----------------------------|--------:|---------:|----------:|
| gemma4-12b-base                  | harmless_quality               | off        |  50 |        26   | baseline    |                             | nan     |  nan     |   nan     |
| gemma4-12b-base                  | mmlu                           | off        | 285 |        25.8 | baseline    |                             |   0.779 |    0.727 |     0.823 |
| gemma4-12b-base                  | over_refusal                   | off        | 250 |        29.9 | baseline    |                             |   0.02  |    0.009 |     0.046 |
| gemma4-12b-base                  | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | baseline    |                             |   0.112 |    0.079 |     0.157 |
| gemma4-12b-base                  | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | baseline    |                             |   0.776 |    0.72  |     0.823 |
| gemma4-12b-base                  | refusal                        | off        | 100 |        30.9 | baseline    |                             |   0.99  |    0.946 |     0.998 |
| gemma4-12b-base                  | refusal[judge_v3_refusal]      | off        | 100 |       nan   | baseline    |                             |   1     |    0.963 |     1     |
| gemma4-12b-base                  | refusal[judge_v3_direct]       | off        | 100 |       nan   | baseline    |                             |   0     |    0     |     0.037 |
| gemma4-12b-heretic-culturerevolt | harmless_quality               | off        |  50 |        29.5 | abliterated | gemma4-12b-base             | nan     |  nan     |   nan     |
| gemma4-12b-heretic-culturerevolt | mmlu                           | off        | 285 |        29   | abliterated | gemma4-12b-base             |   0.804 |    0.753 |     0.845 |
| gemma4-12b-heretic-culturerevolt | over_refusal                   | off        | 250 |        25.6 | abliterated | gemma4-12b-base             |   0.016 |    0.006 |     0.04  |
| gemma4-12b-heretic-culturerevolt | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | abliterated | gemma4-12b-base             |   0.108 |    0.075 |     0.153 |
| gemma4-12b-heretic-culturerevolt | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | abliterated | gemma4-12b-base             |   0.76  |    0.703 |     0.809 |
| gemma4-12b-heretic-culturerevolt | refusal                        | off        | 100 |        24.5 | abliterated | gemma4-12b-base             |   0.99  |    0.946 |     0.998 |
| gemma4-12b-heretic-culturerevolt | refusal[judge_v3_refusal]      | off        | 100 |       nan   | abliterated | gemma4-12b-base             |   0.99  |    0.946 |     0.998 |
| gemma4-12b-heretic-culturerevolt | refusal[judge_v3_direct]       | off        | 100 |       nan   | abliterated | gemma4-12b-base             |   0.01  |    0.002 |     0.054 |
| gemma4-12b-qat-base              | harmless_quality               | off        |  50 |        33.4 | baseline    |                             | nan     |  nan     |   nan     |
| gemma4-12b-qat-base              | mmlu                           | off        | 285 |        34   | baseline    |                             |   0.8   |    0.75  |     0.842 |
| gemma4-12b-qat-base              | over_refusal                   | off        | 250 |        35.2 | baseline    |                             |   0.008 |    0.002 |     0.029 |
| gemma4-12b-qat-base              | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | baseline    |                             |   0.112 |    0.079 |     0.157 |
| gemma4-12b-qat-base              | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | baseline    |                             |   0.736 |    0.678 |     0.787 |
| gemma4-12b-qat-base              | refusal                        | off        | 100 |        36.4 | baseline    |                             |   0.98  |    0.93  |     0.994 |
| gemma4-12b-qat-base              | refusal[judge_v3_refusal]      | off        | 100 |       nan   | baseline    |                             |   0.99  |    0.946 |     0.998 |
| gemma4-12b-qat-base              | refusal[judge_v3_direct]       | off        | 100 |       nan   | baseline    |                             |   0.01  |    0.002 |     0.054 |
| gemma4-12b-qat-hauhaucs          | harmless_quality               | off        |  50 |        24.7 | abliterated | gemma4-12b-qat-base         | nan     |  nan     |   nan     |
| gemma4-12b-qat-hauhaucs          | mmlu                           | off        | 285 |        24.4 | abliterated | gemma4-12b-qat-base         |   0.779 |    0.727 |     0.823 |
| gemma4-12b-qat-hauhaucs          | over_refusal                   | off        | 250 |        26.2 | abliterated | gemma4-12b-qat-base         |   0     |    0     |     0.015 |
| gemma4-12b-qat-hauhaucs          | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | abliterated | gemma4-12b-qat-base         |   0.06  |    0.037 |     0.097 |
| gemma4-12b-qat-hauhaucs          | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | abliterated | gemma4-12b-qat-base         |   0.864 |    0.816 |     0.901 |
| gemma4-12b-qat-hauhaucs          | refusal                        | off        | 100 |        24.7 | abliterated | gemma4-12b-qat-base         |   0     |    0     |     0.037 |
| gemma4-12b-qat-hauhaucs          | refusal[judge_v3_refusal]      | off        | 100 |       nan   | abliterated | gemma4-12b-qat-base         |   0.19  |    0.125 |     0.278 |
| gemma4-12b-qat-hauhaucs          | refusal[judge_v3_direct]       | off        | 100 |       nan   | abliterated | gemma4-12b-qat-base         |   0.76  |    0.668 |     0.833 |
| gemma4-12b-qat-heretic-igorls    | harmless_quality               | off        |  50 |        35.1 | abliterated | gemma4-12b-qat-base         | nan     |  nan     |   nan     |
| gemma4-12b-qat-heretic-igorls    | mmlu                           | off        | 285 |        34.1 | abliterated | gemma4-12b-qat-base         |   0.821 |    0.772 |     0.861 |
| gemma4-12b-qat-heretic-igorls    | over_refusal                   | off        | 250 |        35.5 | abliterated | gemma4-12b-qat-base         |   0     |    0     |     0.015 |
| gemma4-12b-qat-heretic-igorls    | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | abliterated | gemma4-12b-qat-base         |   0.088 |    0.059 |     0.13  |
| gemma4-12b-qat-heretic-igorls    | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | abliterated | gemma4-12b-qat-base         |   0.748 |    0.691 |     0.798 |
| gemma4-12b-qat-heretic-igorls    | refusal                        | off        | 100 |        35.8 | abliterated | gemma4-12b-qat-base         |   0     |    0     |     0.037 |
| gemma4-12b-qat-heretic-igorls    | refusal[judge_v3_refusal]      | off        | 100 |       nan   | abliterated | gemma4-12b-qat-base         |   0.24  |    0.167 |     0.332 |
| gemma4-12b-qat-heretic-igorls    | refusal[judge_v3_direct]       | off        | 100 |       nan   | abliterated | gemma4-12b-qat-base         |   0.3   |    0.219 |     0.396 |
| qwen3-14b-abliterated-mlabonne   | harmless_quality               | off        |  50 |        33.5 | abliterated | qwen3-14b-base              | nan     |  nan     |   nan     |
| qwen3-14b-abliterated-mlabonne   | mmlu                           | off        | 285 |        33   | abliterated | qwen3-14b-base              |   0.712 |    0.657 |     0.762 |
| qwen3-14b-abliterated-mlabonne   | over_refusal                   | off        | 250 |        33.5 | abliterated | qwen3-14b-base              |   0.004 |    0.001 |     0.022 |
| qwen3-14b-abliterated-mlabonne   | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | abliterated | qwen3-14b-base              |   0.036 |    0.019 |     0.067 |
| qwen3-14b-abliterated-mlabonne   | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | abliterated | qwen3-14b-base              |   0.948 |    0.913 |     0.969 |
| qwen3-14b-abliterated-mlabonne   | refusal                        | off        | 100 |        31.8 | abliterated | qwen3-14b-base              |   0     |    0     |     0.037 |
| qwen3-14b-abliterated-mlabonne   | refusal[judge_v3_refusal]      | off        | 100 |       nan   | abliterated | qwen3-14b-base              |   0.13  |    0.078 |     0.21  |
| qwen3-14b-abliterated-mlabonne   | refusal[judge_v3_direct]       | off        | 100 |       nan   | abliterated | qwen3-14b-base              |   0.75  |    0.657 |     0.825 |
| qwen3-14b-base                   | harmless_quality               | off        |  50 |        31.6 | baseline    |                             | nan     |  nan     |   nan     |
| qwen3-14b-base                   | mmlu                           | off        | 285 |        30   | baseline    |                             |   0.772 |    0.72  |     0.817 |
| qwen3-14b-base                   | over_refusal                   | off        | 250 |        31.8 | baseline    |                             |   0.032 |    0.016 |     0.062 |
| qwen3-14b-base                   | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | baseline    |                             |   0.084 |    0.056 |     0.125 |
| qwen3-14b-base                   | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | baseline    |                             |   0.848 |    0.798 |     0.887 |
| qwen3-14b-base                   | refusal                        | off        | 100 |        32.9 | baseline    |                             |   0.92  |    0.85  |     0.959 |
| qwen3-14b-base                   | refusal[judge_v3_refusal]      | off        | 100 |       nan   | baseline    |                             |   0.95  |    0.888 |     0.978 |
| qwen3-14b-base                   | refusal[judge_v3_direct]       | off        | 100 |       nan   | baseline    |                             |   0.01  |    0.002 |     0.054 |
| qwen3-4b-instruct-2507-abl       | harmless_quality               | off        |  50 |        80.9 | own         | qwen3-4b-instruct-2507-base | nan     |  nan     |   nan     |
| qwen3-4b-instruct-2507-abl       | mmlu                           | off        | 285 |        79.4 | own         | qwen3-4b-instruct-2507-base |   0.733 |    0.679 |     0.781 |
| qwen3-4b-instruct-2507-abl       | over_refusal                   | off        | 250 |        82.1 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.015 |
| qwen3-4b-instruct-2507-abl       | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.096 |    0.065 |     0.139 |
| qwen3-4b-instruct-2507-abl       | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.836 |    0.785 |     0.877 |
| qwen3-4b-instruct-2507-abl       | refusal                        | off        | 100 |        83.4 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.037 |
| qwen3-4b-instruct-2507-abl       | refusal[judge_v3_refusal]      | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.56  |    0.462 |     0.653 |
| qwen3-4b-instruct-2507-abl       | refusal[judge_v3_direct]       | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.03  |    0.01  |     0.085 |
| qwen3-4b-instruct-2507-abl-v2    | harmless_quality               | off        |  50 |        81.8 | own         | qwen3-4b-instruct-2507-base | nan     |  nan     |   nan     |
| qwen3-4b-instruct-2507-abl-v2    | mmlu                           | off        | 285 |        78.8 | own         | qwen3-4b-instruct-2507-base |   0.754 |    0.701 |     0.801 |
| qwen3-4b-instruct-2507-abl-v2    | over_refusal                   | off        | 250 |        80.8 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.015 |
| qwen3-4b-instruct-2507-abl-v2    | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.092 |    0.062 |     0.134 |
| qwen3-4b-instruct-2507-abl-v2    | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.84  |    0.789 |     0.88  |
| qwen3-4b-instruct-2507-abl-v2    | refusal                        | off        | 100 |        81.9 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.037 |
| qwen3-4b-instruct-2507-abl-v2    | refusal[judge_v3_refusal]      | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.48  |    0.385 |     0.577 |
| qwen3-4b-instruct-2507-abl-v2    | refusal[judge_v3_direct]       | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.22  |    0.15  |     0.311 |
| qwen3-4b-instruct-2507-abl-v3    | harmless_quality               | off        |  50 |        83.6 | own         | qwen3-4b-instruct-2507-base | nan     |  nan     |   nan     |
| qwen3-4b-instruct-2507-abl-v3    | mmlu                           | off        | 285 |        86.6 | own         | qwen3-4b-instruct-2507-base |   0.618 |    0.56  |     0.672 |
| qwen3-4b-instruct-2507-abl-v3    | over_refusal                   | off        | 250 |        84.2 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.015 |
| qwen3-4b-instruct-2507-abl-v3    | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.024 |    0.011 |     0.051 |
| qwen3-4b-instruct-2507-abl-v3    | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.928 |    0.889 |     0.954 |
| qwen3-4b-instruct-2507-abl-v3    | refusal                        | off        | 100 |        83.3 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.037 |
| qwen3-4b-instruct-2507-abl-v3    | refusal[judge_v3_refusal]      | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.14  |    0.085 |     0.221 |
| qwen3-4b-instruct-2507-abl-v3    | refusal[judge_v3_direct]       | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.81  |    0.722 |     0.875 |
| qwen3-4b-instruct-2507-abl-v4    | harmless_quality               | off        |  50 |        84.3 | own         | qwen3-4b-instruct-2507-base | nan     |  nan     |   nan     |
| qwen3-4b-instruct-2507-abl-v4    | mmlu                           | off        | 285 |        77.9 | own         | qwen3-4b-instruct-2507-base |   0.73  |    0.675 |     0.778 |
| qwen3-4b-instruct-2507-abl-v4    | over_refusal                   | off        | 250 |        80.3 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.015 |
| qwen3-4b-instruct-2507-abl-v4    | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.06  |    0.037 |     0.097 |
| qwen3-4b-instruct-2507-abl-v4    | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.904 |    0.861 |     0.935 |
| qwen3-4b-instruct-2507-abl-v4    | refusal                        | off        | 100 |        80.3 | own         | qwen3-4b-instruct-2507-base |   0     |    0     |     0.037 |
| qwen3-4b-instruct-2507-abl-v4    | refusal[judge_v3_refusal]      | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.26  |    0.184 |     0.354 |
| qwen3-4b-instruct-2507-abl-v4    | refusal[judge_v3_direct]       | off        | 100 |       nan   | own         | qwen3-4b-instruct-2507-base |   0.57  |    0.472 |     0.663 |
| qwen3-4b-instruct-2507-base      | harmless_quality               | off        |  50 |        83.6 | own         |                             | nan     |  nan     |   nan     |
| qwen3-4b-instruct-2507-base      | mmlu                           | off        | 285 |        76   | own         |                             |   0.74  |    0.686 |     0.788 |
| qwen3-4b-instruct-2507-base      | over_refusal                   | off        | 250 |        80.6 | own         |                             |   0.048 |    0.028 |     0.082 |
| qwen3-4b-instruct-2507-base      | over_refusal[judge_v3_refusal] | off        | 250 |       nan   | own         |                             |   0.176 |    0.134 |     0.228 |
| qwen3-4b-instruct-2507-base      | over_refusal[judge_v3_direct]  | off        | 250 |       nan   | own         |                             |   0.724 |    0.666 |     0.776 |
| qwen3-4b-instruct-2507-base      | refusal                        | off        | 100 |        80   | own         |                             |   1     |    0.963 |     1     |
| qwen3-4b-instruct-2507-base      | refusal[judge_v3_refusal]      | off        | 100 |       nan   | own         |                             |   0.99  |    0.946 |     0.998 |
| qwen3-4b-instruct-2507-base      | refusal[judge_v3_direct]       | off        | 100 |       nan   | own         |                             |   0.01  |    0.002 |     0.054 |

## Judge v3 4-class breakdown

| model                            | task         | thinking   |   n |   explicit_refusal |   safe_reframe |   hedged_compliance |   direct_compliance |   effective_refusal |   unparsed |
|:---------------------------------|:-------------|:-----------|----:|-------------------:|---------------:|--------------------:|--------------------:|--------------------:|-----------:|
| gemma4-12b-base                  | over_refusal | off        | 250 |              0.044 |          0.068 |               0.036 |               0.776 |               0.112 |         19 |
| gemma4-12b-base                  | refusal      | off        | 100 |              0.99  |          0.01  |               0     |               0     |               1     |          0 |
| gemma4-12b-heretic-culturerevolt | over_refusal | off        | 250 |              0.056 |          0.052 |               0.068 |               0.76  |               0.108 |         16 |
| gemma4-12b-heretic-culturerevolt | refusal      | off        | 100 |              0.99  |          0     |               0     |               0.01  |               0.99  |          0 |
| gemma4-12b-qat-base              | over_refusal | off        | 250 |              0.048 |          0.064 |               0.044 |               0.736 |               0.112 |         27 |
| gemma4-12b-qat-base              | refusal      | off        | 100 |              0.98  |          0.01  |               0     |               0.01  |               0.99  |          0 |
| gemma4-12b-qat-hauhaucs          | over_refusal | off        | 250 |              0     |          0.06  |               0.012 |               0.864 |               0.06  |         16 |
| gemma4-12b-qat-hauhaucs          | refusal      | off        | 100 |              0     |          0.19  |               0.03  |               0.76  |               0.19  |          2 |
| gemma4-12b-qat-heretic-igorls    | over_refusal | off        | 250 |              0.012 |          0.076 |               0.06  |               0.748 |               0.088 |         26 |
| gemma4-12b-qat-heretic-igorls    | refusal      | off        | 100 |              0.02  |          0.22  |               0.44  |               0.3   |               0.24  |          2 |
| qwen3-14b-abliterated-mlabonne   | over_refusal | off        | 250 |              0.02  |          0.016 |               0.016 |               0.948 |               0.036 |          0 |
| qwen3-14b-abliterated-mlabonne   | refusal      | off        | 100 |              0.01  |          0.12  |               0.1   |               0.75  |               0.13  |          2 |
| qwen3-14b-base                   | over_refusal | off        | 250 |              0.044 |          0.04  |               0.052 |               0.848 |               0.084 |          4 |
| qwen3-14b-base                   | refusal      | off        | 100 |              0.95  |          0     |               0.01  |               0.01  |               0.95  |          3 |
| qwen3-4b-instruct-2507-abl       | over_refusal | off        | 250 |              0.004 |          0.092 |               0.016 |               0.836 |               0.096 |         13 |
| qwen3-4b-instruct-2507-abl       | refusal      | off        | 100 |              0.06  |          0.5   |               0.36  |               0.03  |               0.56  |          5 |
| qwen3-4b-instruct-2507-abl-v2    | over_refusal | off        | 250 |              0.008 |          0.084 |               0.008 |               0.84  |               0.092 |         15 |
| qwen3-4b-instruct-2507-abl-v2    | refusal      | off        | 100 |              0     |          0.48  |               0.25  |               0.22  |               0.48  |          5 |
| qwen3-4b-instruct-2507-abl-v3    | over_refusal | off        | 250 |              0     |          0.024 |               0.024 |               0.928 |               0.024 |          6 |
| qwen3-4b-instruct-2507-abl-v3    | refusal      | off        | 100 |              0     |          0.14  |               0.05  |               0.81  |               0.14  |          0 |
| qwen3-4b-instruct-2507-abl-v4    | over_refusal | off        | 250 |              0.004 |          0.056 |               0.012 |               0.904 |               0.06  |          6 |
| qwen3-4b-instruct-2507-abl-v4    | refusal      | off        | 100 |              0     |          0.26  |               0.16  |               0.57  |               0.26  |          1 |
| qwen3-4b-instruct-2507-base      | over_refusal | off        | 250 |              0.084 |          0.092 |               0.064 |               0.724 |               0.176 |          9 |
| qwen3-4b-instruct-2507-base      | refusal      | off        | 100 |              0.99  |          0     |               0     |               0.01  |               0.99  |          0 |

## Abliterated minus baseline

| model                            | baseline                    | task                           | thinking   |   rate |   baseline_rate |   delta |
|:---------------------------------|:----------------------------|:-------------------------------|:-----------|-------:|----------------:|--------:|
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base             | mmlu                           | off        |  0.804 |           0.779 |   0.025 |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base             | over_refusal                   | off        |  0.016 |           0.02  |  -0.004 |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base             | over_refusal[judge_v3_refusal] | off        |  0.108 |           0.112 |  -0.004 |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base             | over_refusal[judge_v3_direct]  | off        |  0.76  |           0.776 |  -0.016 |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base             | refusal                        | off        |  0.99  |           0.99  |   0     |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base             | refusal[judge_v3_refusal]      | off        |  0.99  |           1     |  -0.01  |
| gemma4-12b-heretic-culturerevolt | gemma4-12b-base             | refusal[judge_v3_direct]       | off        |  0.01  |           0     |   0.01  |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base         | mmlu                           | off        |  0.779 |           0.8   |  -0.021 |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base         | over_refusal                   | off        |  0     |           0.008 |  -0.008 |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base         | over_refusal[judge_v3_refusal] | off        |  0.06  |           0.112 |  -0.052 |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base         | over_refusal[judge_v3_direct]  | off        |  0.864 |           0.736 |   0.128 |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base         | refusal                        | off        |  0     |           0.98  |  -0.98  |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base         | refusal[judge_v3_refusal]      | off        |  0.19  |           0.99  |  -0.8   |
| gemma4-12b-qat-hauhaucs          | gemma4-12b-qat-base         | refusal[judge_v3_direct]       | off        |  0.76  |           0.01  |   0.75  |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base         | mmlu                           | off        |  0.821 |           0.8   |   0.021 |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base         | over_refusal                   | off        |  0     |           0.008 |  -0.008 |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base         | over_refusal[judge_v3_refusal] | off        |  0.088 |           0.112 |  -0.024 |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base         | over_refusal[judge_v3_direct]  | off        |  0.748 |           0.736 |   0.012 |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base         | refusal                        | off        |  0     |           0.98  |  -0.98  |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base         | refusal[judge_v3_refusal]      | off        |  0.24  |           0.99  |  -0.75  |
| gemma4-12b-qat-heretic-igorls    | gemma4-12b-qat-base         | refusal[judge_v3_direct]       | off        |  0.3   |           0.01  |   0.29  |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base              | mmlu                           | off        |  0.712 |           0.772 |  -0.06  |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base              | over_refusal                   | off        |  0.004 |           0.032 |  -0.028 |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base              | over_refusal[judge_v3_refusal] | off        |  0.036 |           0.084 |  -0.048 |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base              | over_refusal[judge_v3_direct]  | off        |  0.948 |           0.848 |   0.1   |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base              | refusal                        | off        |  0     |           0.92  |  -0.92  |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base              | refusal[judge_v3_refusal]      | off        |  0.13  |           0.95  |  -0.82  |
| qwen3-14b-abliterated-mlabonne   | qwen3-14b-base              | refusal[judge_v3_direct]       | off        |  0.75  |           0.01  |   0.74  |
| qwen3-4b-instruct-2507-abl       | qwen3-4b-instruct-2507-base | mmlu                           | off        |  0.733 |           0.74  |  -0.007 |
| qwen3-4b-instruct-2507-abl       | qwen3-4b-instruct-2507-base | over_refusal                   | off        |  0     |           0.048 |  -0.048 |
| qwen3-4b-instruct-2507-abl       | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_refusal] | off        |  0.096 |           0.176 |  -0.08  |
| qwen3-4b-instruct-2507-abl       | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_direct]  | off        |  0.836 |           0.724 |   0.112 |
| qwen3-4b-instruct-2507-abl       | qwen3-4b-instruct-2507-base | refusal                        | off        |  0     |           1     |  -1     |
| qwen3-4b-instruct-2507-abl       | qwen3-4b-instruct-2507-base | refusal[judge_v3_refusal]      | off        |  0.56  |           0.99  |  -0.43  |
| qwen3-4b-instruct-2507-abl       | qwen3-4b-instruct-2507-base | refusal[judge_v3_direct]       | off        |  0.03  |           0.01  |   0.02  |
| qwen3-4b-instruct-2507-abl-v2    | qwen3-4b-instruct-2507-base | mmlu                           | off        |  0.754 |           0.74  |   0.014 |
| qwen3-4b-instruct-2507-abl-v2    | qwen3-4b-instruct-2507-base | over_refusal                   | off        |  0     |           0.048 |  -0.048 |
| qwen3-4b-instruct-2507-abl-v2    | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_refusal] | off        |  0.092 |           0.176 |  -0.084 |
| qwen3-4b-instruct-2507-abl-v2    | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_direct]  | off        |  0.84  |           0.724 |   0.116 |
| qwen3-4b-instruct-2507-abl-v2    | qwen3-4b-instruct-2507-base | refusal                        | off        |  0     |           1     |  -1     |
| qwen3-4b-instruct-2507-abl-v2    | qwen3-4b-instruct-2507-base | refusal[judge_v3_refusal]      | off        |  0.48  |           0.99  |  -0.51  |
| qwen3-4b-instruct-2507-abl-v2    | qwen3-4b-instruct-2507-base | refusal[judge_v3_direct]       | off        |  0.22  |           0.01  |   0.21  |
| qwen3-4b-instruct-2507-abl-v3    | qwen3-4b-instruct-2507-base | mmlu                           | off        |  0.618 |           0.74  |  -0.122 |
| qwen3-4b-instruct-2507-abl-v3    | qwen3-4b-instruct-2507-base | over_refusal                   | off        |  0     |           0.048 |  -0.048 |
| qwen3-4b-instruct-2507-abl-v3    | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_refusal] | off        |  0.024 |           0.176 |  -0.152 |
| qwen3-4b-instruct-2507-abl-v3    | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_direct]  | off        |  0.928 |           0.724 |   0.204 |
| qwen3-4b-instruct-2507-abl-v3    | qwen3-4b-instruct-2507-base | refusal                        | off        |  0     |           1     |  -1     |
| qwen3-4b-instruct-2507-abl-v3    | qwen3-4b-instruct-2507-base | refusal[judge_v3_refusal]      | off        |  0.14  |           0.99  |  -0.85  |
| qwen3-4b-instruct-2507-abl-v3    | qwen3-4b-instruct-2507-base | refusal[judge_v3_direct]       | off        |  0.81  |           0.01  |   0.8   |
| qwen3-4b-instruct-2507-abl-v4    | qwen3-4b-instruct-2507-base | mmlu                           | off        |  0.73  |           0.74  |  -0.01  |
| qwen3-4b-instruct-2507-abl-v4    | qwen3-4b-instruct-2507-base | over_refusal                   | off        |  0     |           0.048 |  -0.048 |
| qwen3-4b-instruct-2507-abl-v4    | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_refusal] | off        |  0.06  |           0.176 |  -0.116 |
| qwen3-4b-instruct-2507-abl-v4    | qwen3-4b-instruct-2507-base | over_refusal[judge_v3_direct]  | off        |  0.904 |           0.724 |   0.18  |
| qwen3-4b-instruct-2507-abl-v4    | qwen3-4b-instruct-2507-base | refusal                        | off        |  0     |           1     |  -1     |
| qwen3-4b-instruct-2507-abl-v4    | qwen3-4b-instruct-2507-base | refusal[judge_v3_refusal]      | off        |  0.26  |           0.99  |  -0.73  |
| qwen3-4b-instruct-2507-abl-v4    | qwen3-4b-instruct-2507-base | refusal[judge_v3_direct]       | off        |  0.57  |           0.01  |   0.56  |
