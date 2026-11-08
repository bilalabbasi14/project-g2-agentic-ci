# Statistics (test split)

Input: 13 per_build.csv file(s). Metrics are averaged over seeds per build first. Wilcoxon signed-rank (two-sided), Holm correction within each family (comparison × metric × budget), α = 0.05. Effect size r = matched-pairs rank-biserial correlation (positive = target better). Friedman mean rank 1 = best.

## RQ1: LLM-relevance vs others

| metric | budget | other | n | mean diff | W/T/L | p | p (Holm) | sig. | r |
|---|---|---|---|---|---|---|---|---|---|
| dtc | 5% | DANTE-CCH | 44 | 0.045 | 4/38/2 | 0.4142 | 0.4142 | no | 0.333 |
| dtc | 5% | DANTE-CCH-shipped | 44 | 0.045 | 2/42/0 | 0.1573 | 0.3146 | no | 1.000 |
| dtc | 10% | DANTE-CCH | 44 | 0.091 | 4/40/0 | 0.0455 | 0.0910 | no | 1.000 |
| dtc | 10% | DANTE-CCH-shipped | 44 | 0.068 | 4/40/0 | 0.0588 | 0.0910 | no | 1.000 |
| dtc | 20% | DANTE-CCH | 44 | -0.030 | 1/41/2 | 0.2763 | 0.5526 | no | -0.667 |
| dtc | 20% | DANTE-CCH-shipped | 44 | -0.007 | 2/40/2 | 0.8539 | 0.8539 | no | -0.100 |
| sapfdc | 5% | DANTE-CCH | 44 | -0.004 | 14/23/7 | 0.6143 | 0.6143 | no | 0.126 |
| sapfdc | 5% | DANTE-CCH-shipped | 44 | 0.015 | 5/27/12 | 0.2461 | 0.4923 | no | -0.320 |
| sapfdc | 10% | DANTE-CCH | 44 | 0.013 | 17/21/6 | 0.1137 | 0.2275 | no | 0.377 |
| sapfdc | 10% | DANTE-CCH-shipped | 44 | 0.023 | 11/25/8 | 0.4939 | 0.4939 | no | 0.179 |
| sapfdc | 20% | DANTE-CCH | 44 | 0.010 | 23/16/5 | 0.0362 | 0.0723 | no | 0.453 |
| sapfdc | 20% | DANTE-CCH-shipped | 44 | 0.015 | 11/20/13 | 0.4576 | 0.4576 | no | -0.173 |

## RQ3: Agent-weighted vs others

| metric | budget | other | n | mean diff | W/T/L | p | p (Holm) | sig. | r |
|---|---|---|---|---|---|---|---|---|---|
| dtc | 5% | DANTE-CCH | 44 | 0.023 | 3/39/2 | 0.6547 | 0.6547 | no | 0.200 |
| dtc | 5% | Tuned-weight (LLM) | 44 | -0.023 | 0/43/1 | 0.3173 | 0.6346 | no | -1.000 |
| dtc | 10% | DANTE-CCH | 44 | 0.068 | 3/41/0 | 0.0833 | 0.1665 | no | 1.000 |
| dtc | 10% | Tuned-weight (LLM) | 44 | -0.023 | 0/43/1 | 0.3173 | 0.3173 | no | -1.000 |
| dtc | 20% | DANTE-CCH | 44 | 0.015 | 3/39/2 | 0.8875 | 0.8994 | no | 0.067 |
| dtc | 20% | Tuned-weight (LLM) | 44 | 0.023 | 3/40/1 | 0.4497 | 0.8994 | no | 0.400 |
| sapfdc | 5% | DANTE-CCH | 44 | -0.007 | 13/24/7 | 0.7938 | 1.0000 | no | 0.067 |
| sapfdc | 5% | Tuned-weight (LLM) | 44 | -0.003 | 3/36/5 | 0.5754 | 1.0000 | no | -0.222 |
| sapfdc | 10% | DANTE-CCH | 44 | -0.000 | 15/22/7 | 0.3382 | 0.6764 | no | 0.233 |
| sapfdc | 10% | Tuned-weight (LLM) | 44 | -0.008 | 4/35/5 | 0.6784 | 0.6784 | no | -0.156 |
| sapfdc | 20% | DANTE-CCH | 44 | 0.022 | 24/14/6 | 0.0407 | 0.0814 | no | 0.428 |
| sapfdc | 20% | Tuned-weight (LLM) | 44 | 0.014 | 8/30/6 | 0.3305 | 0.3305 | no | 0.295 |

## E3: Full system vs others

| metric | budget | other | n | mean diff | W/T/L | p | p (Holm) | sig. | r |
|---|---|---|---|---|---|---|---|---|---|
| dtc | 5% | DANTE-CCH | 44 | 0.023 | 3/39/2 | 0.6547 | 1.0000 | no | 0.200 |
| dtc | 5% | DANTE-CCH-shipped | 44 | 0.023 | 2/41/1 | 0.5637 | 1.0000 | no | 0.333 |
| dtc | 5% | Random | 44 | 0.274 | 15/29/0 | 0.0004 | 0.0013 | yes | 1.000 |
| dtc | 10% | DANTE-CCH | 44 | 0.068 | 3/41/0 | 0.0833 | 0.1665 | no | 1.000 |
| dtc | 10% | DANTE-CCH-shipped | 44 | 0.046 | 3/41/0 | 0.1025 | 0.1665 | no | 1.000 |
| dtc | 10% | Random | 44 | 0.317 | 19/24/1 | 0.0004 | 0.0011 | yes | 0.871 |
| dtc | 20% | DANTE-CCH | 44 | 0.015 | 3/39/2 | 0.8875 | 0.8875 | no | 0.067 |
| dtc | 20% | DANTE-CCH-shipped | 44 | 0.038 | 4/38/2 | 0.3883 | 0.7766 | no | 0.381 |
| dtc | 20% | Random | 44 | 0.341 | 22/18/4 | 0.0014 | 0.0041 | yes | 0.684 |
| sapfdc | 5% | DANTE-CCH | 44 | -0.007 | 13/24/7 | 0.7938 | 0.7938 | no | 0.067 |
| sapfdc | 5% | DANTE-CCH-shipped | 44 | 0.012 | 5/28/11 | 0.2343 | 0.4686 | no | -0.338 |
| sapfdc | 5% | Random | 44 | 0.197 | 18/26/0 | 0.0002 | 0.0006 | yes | 1.000 |
| sapfdc | 10% | DANTE-CCH | 44 | -0.000 | 15/22/7 | 0.3382 | 0.6764 | no | 0.233 |
| sapfdc | 10% | DANTE-CCH-shipped | 44 | 0.010 | 9/26/9 | 0.6791 | 0.6791 | no | -0.111 |
| sapfdc | 10% | Random | 44 | 0.234 | 21/21/2 | 0.0001 | 0.0004 | yes | 0.906 |
| sapfdc | 20% | DANTE-CCH | 44 | 0.022 | 24/14/6 | 0.0407 | 0.0814 | no | 0.428 |
| sapfdc | 20% | DANTE-CCH-shipped | 44 | 0.026 | 14/18/12 | 0.8291 | 0.8291 | no | 0.048 |
| sapfdc | 20% | Random | 44 | 0.298 | 28/12/4 | 0.0001 | 0.0003 | yes | 0.784 |

## E1: Full system vs others

| metric | budget | other | n | mean diff | W/T/L | p | p (Holm) | sig. | r |
|---|---|---|---|---|---|---|---|---|---|
| dtc | 5% | Single-call LLM | 44 | -0.023 | 0/43/1 | 0.3173 | 0.9519 | no | -1.000 |
| dtc | 5% | Tuned-weight (TF-IDF) | 44 | 0.023 | 2/41/1 | 0.5637 | 1.0000 | no | 0.333 |
| dtc | 5% | History-only | 44 | 0.024 | 5/35/4 | 0.5873 | 1.0000 | no | 0.200 |
| dtc | 5% | TF-IDF-only | 44 | 0.191 | 10/33/1 | 0.0040 | 0.0160 | yes | 0.939 |
| dtc | 10% | Single-call LLM | 44 | 0.000 | 0/44/0 | 1.0000 | 1.0000 | no | 0.000 |
| dtc | 10% | Tuned-weight (TF-IDF) | 44 | 0.046 | 3/41/0 | 0.1025 | 0.3074 | no | 1.000 |
| dtc | 10% | History-only | 44 | 0.026 | 3/39/2 | 0.4922 | 0.9844 | no | 0.333 |
| dtc | 10% | TF-IDF-only | 44 | 0.176 | 12/29/3 | 0.0424 | 0.1698 | no | 0.550 |
| dtc | 20% | Single-call LLM | 44 | -0.008 | 2/39/3 | 0.8875 | 0.8875 | no | -0.067 |
| dtc | 20% | Tuned-weight (TF-IDF) | 44 | 0.038 | 4/38/2 | 0.3883 | 0.7766 | no | 0.381 |
| dtc | 20% | History-only | 44 | 0.069 | 7/35/2 | 0.2454 | 0.7361 | no | 0.422 |
| dtc | 20% | TF-IDF-only | 44 | 0.230 | 16/24/4 | 0.0133 | 0.0532 | no | 0.600 |
| sapfdc | 5% | Single-call LLM | 44 | -0.023 | 4/28/12 | 0.0200 | 0.0599 | no | -0.662 |
| sapfdc | 5% | Tuned-weight (TF-IDF) | 44 | 0.012 | 5/28/11 | 0.2343 | 0.4686 | no | -0.338 |
| sapfdc | 5% | History-only | 44 | 0.056 | 11/24/9 | 0.2959 | 0.4686 | no | 0.267 |
| sapfdc | 5% | TF-IDF-only | 44 | 0.136 | 15/26/3 | 0.0074 | 0.0296 | yes | 0.719 |
| sapfdc | 10% | Single-call LLM | 44 | -0.030 | 5/23/16 | 0.0680 | 0.2041 | no | -0.455 |
| sapfdc | 10% | Tuned-weight (TF-IDF) | 44 | 0.010 | 9/26/9 | 0.6791 | 0.8528 | no | -0.111 |
| sapfdc | 10% | History-only | 44 | 0.043 | 10/22/12 | 0.4264 | 0.8528 | no | 0.194 |
| sapfdc | 10% | TF-IDF-only | 44 | 0.122 | 18/19/7 | 0.0324 | 0.1297 | no | 0.489 |
| sapfdc | 20% | Single-call LLM | 44 | -0.014 | 11/18/15 | 0.3282 | 0.6563 | no | -0.219 |
| sapfdc | 20% | Tuned-weight (TF-IDF) | 44 | 0.026 | 14/18/12 | 0.8291 | 0.8291 | no | 0.048 |
| sapfdc | 20% | History-only | 44 | 0.075 | 14/15/15 | 0.1908 | 0.5724 | no | 0.278 |
| sapfdc | 20% | TF-IDF-only | 44 | 0.180 | 23/13/8 | 0.0042 | 0.0169 | yes | 0.589 |

## E5: Full system vs others

| metric | budget | other | n | mean diff | W/T/L | p | p (Holm) | sig. | r |
|---|---|---|---|---|---|---|---|---|---|
| dtc | 5% | LLM-relevance | 44 | -0.023 | 0/43/1 | 0.3173 | 0.6346 | no | -1.000 |
| dtc | 5% | Agent-weighted (TF-IDF) | 44 | 0.023 | 3/39/2 | 0.6547 | 0.6547 | no | 0.200 |
| dtc | 10% | LLM-relevance | 44 | -0.023 | 0/43/1 | 0.3173 | 0.3173 | no | -1.000 |
| dtc | 10% | Agent-weighted (TF-IDF) | 44 | 0.068 | 3/41/0 | 0.0833 | 0.1665 | no | 1.000 |
| dtc | 20% | LLM-relevance | 44 | 0.045 | 2/42/0 | 0.1573 | 0.3146 | no | 1.000 |
| dtc | 20% | Agent-weighted (TF-IDF) | 44 | 0.015 | 3/39/2 | 0.8875 | 0.8875 | no | 0.067 |
| sapfdc | 5% | LLM-relevance | 44 | -0.003 | 4/38/2 | 0.7532 | 1.0000 | no | 0.143 |
| sapfdc | 5% | Agent-weighted (TF-IDF) | 44 | -0.008 | 13/24/7 | 0.7938 | 1.0000 | no | 0.067 |
| sapfdc | 10% | LLM-relevance | 44 | -0.013 | 3/38/3 | 0.6002 | 0.8155 | no | -0.238 |
| sapfdc | 10% | Agent-weighted (TF-IDF) | 44 | -0.001 | 15/22/7 | 0.4077 | 0.8155 | no | 0.202 |
| sapfdc | 20% | LLM-relevance | 44 | 0.012 | 7/35/2 | 0.1097 | 0.1644 | no | 0.600 |
| sapfdc | 20% | Agent-weighted (TF-IDF) | 44 | 0.019 | 23/14/7 | 0.0822 | 0.1644 | no | 0.363 |

## Friedman tests

| set | metric | budget | n builds | χ² | p | best mean rank |
|---|---|---|---|---|---|---|
| RQ1 | dtc | 5% | 44 | 1.143 | 0.5647 | LLM-relevance (1.95) |
| RQ1 | dtc | 10% | 44 | 5.333 | 0.0695 | LLM-relevance (1.91) |
| RQ1 | dtc | 20% | 44 | 0.737 | 0.6918 | DANTE-CCH (1.97) |
| RQ1 | sapfdc | 5% | 44 | 4.278 | 0.1177 | DANTE-CCH-shipped (1.85) |
| RQ1 | sapfdc | 10% | 44 | 8.437 | 0.0147 | LLM-relevance (1.85) |
| RQ1 | sapfdc | 20% | 44 | 16.745 | 0.0002 | DANTE-CCH-shipped (1.78) |
| RQ3 | dtc | 5% | 44 | 1.000 | 0.6065 | Tuned-weight (LLM) (1.97) |
| RQ3 | dtc | 10% | 44 | 6.500 | 0.0388 | Tuned-weight (LLM) (1.94) |
| RQ3 | dtc | 20% | 44 | 0.857 | 0.6514 | Agent-weighted (1.97) |
| RQ3 | sapfdc | 5% | 44 | 3.800 | 0.1496 | Tuned-weight (LLM) (1.90) |
| RQ3 | sapfdc | 10% | 44 | 7.256 | 0.0266 | Tuned-weight (LLM) (1.85) |
| RQ3 | sapfdc | 20% | 44 | 17.733 | 0.0001 | Agent-weighted (1.76) |
| ALL | dtc | 5% | 44 | 75.056 | 0.0000 | LLM-relevance (5.59) |
| ALL | dtc | 10% | 44 | 82.878 | 0.0000 | LLM-relevance (5.48) |
| ALL | dtc | 20% | 44 | 68.294 | 0.0000 | Single-call LLM (5.43) |
| ALL | sapfdc | 5% | 44 | 66.643 | 0.0000 | Single-call LLM (5.02) |
| ALL | sapfdc | 10% | 44 | 57.000 | 0.0000 | Single-call LLM (5.02) |
| ALL | sapfdc | 20% | 44 | 66.994 | 0.0000 | Single-call LLM (5.16) |

## Seed variability

| method | budget | metric | seeds | mean | std |
|---|---|---|---|---|---|
| Agent-weighted | 5% | dtc | 1;2;3 | 0.306 | 0.000 |
| Agent-weighted | 5% | sapfdc | 1;2;3 | 0.219 | 0.000 |
| Agent-weighted | 10% | dtc | 1;2;3 | 0.424 | 0.000 |
| Agent-weighted | 10% | sapfdc | 1;2;3 | 0.274 | 0.000 |
| Agent-weighted | 20% | dtc | 1;2;3 | 0.560 | 0.013 |
| Agent-weighted | 20% | sapfdc | 1;2;3 | 0.392 | 0.007 |
| Agent-weighted (TF-IDF) | 5% | dtc | 1;2;3 | 0.283 | 0.000 |
| Agent-weighted (TF-IDF) | 5% | sapfdc | 1;2;3 | 0.227 | 0.000 |
| Agent-weighted (TF-IDF) | 10% | dtc | 1;2;3 | 0.356 | 0.000 |
| Agent-weighted (TF-IDF) | 10% | sapfdc | 1;2;3 | 0.275 | 0.000 |
| Agent-weighted (TF-IDF) | 20% | dtc | 1;2;3 | 0.545 | 0.000 |
| Agent-weighted (TF-IDF) | 20% | sapfdc | 1;2;3 | 0.373 | 0.000 |
| DANTE-CCH | 5% | dtc | 1;2;3 | 0.283 | 0.000 |
| DANTE-CCH | 5% | sapfdc | 1;2;3 | 0.226 | 0.000 |
| DANTE-CCH | 10% | dtc | 1;2;3 | 0.356 | 0.000 |
| DANTE-CCH | 10% | sapfdc | 1;2;3 | 0.274 | 0.000 |
| DANTE-CCH | 20% | dtc | 1;2;3 | 0.545 | 0.000 |
| DANTE-CCH | 20% | sapfdc | 1;2;3 | 0.370 | 0.000 |
| DANTE-CCH-shipped | 5% | dtc | 1;2;3 | 0.283 | 0.000 |
| DANTE-CCH-shipped | 5% | sapfdc | 1;2;3 | 0.207 | 0.000 |
| DANTE-CCH-shipped | 10% | dtc | 1;2;3 | 0.378 | 0.000 |
| DANTE-CCH-shipped | 10% | sapfdc | 1;2;3 | 0.264 | 0.000 |
| DANTE-CCH-shipped | 20% | dtc | 1;2;3 | 0.522 | 0.000 |
| DANTE-CCH-shipped | 20% | sapfdc | 1;2;3 | 0.365 | 0.000 |
| Full system | 5% | dtc | 1;2;3 | 0.306 | 0.000 |
| Full system | 5% | sapfdc | 1;2;3 | 0.219 | 0.000 |
| Full system | 10% | dtc | 1;2;3 | 0.424 | 0.000 |
| Full system | 10% | sapfdc | 1;2;3 | 0.274 | 0.000 |
| Full system | 20% | dtc | 1;2;3 | 0.560 | 0.013 |
| Full system | 20% | sapfdc | 1;2;3 | 0.392 | 0.007 |
| Full system (no shortlist) | 5% | dtc | 1;2;3 | 0.338 | 0.000 |
| Full system (no shortlist) | 5% | sapfdc | 1;2;3 | 0.246 | 0.000 |
| Full system (no shortlist) | 10% | dtc | 1;2;3 | 0.441 | 0.000 |
| Full system (no shortlist) | 10% | sapfdc | 1;2;3 | 0.281 | 0.000 |
| Full system (no shortlist) | 20% | dtc | 1;2;3 | 0.538 | 0.013 |
| Full system (no shortlist) | 20% | sapfdc | 1;2;3 | 0.392 | 0.006 |
| History-only | 5% | dtc | 1;2;3 | 0.282 | 0.000 |
| History-only | 5% | sapfdc | 1;2;3 | 0.163 | 0.000 |
| History-only | 10% | dtc | 1;2;3 | 0.398 | 0.000 |
| History-only | 10% | sapfdc | 1;2;3 | 0.231 | 0.000 |
| History-only | 20% | dtc | 1;2;3 | 0.492 | 0.000 |
| History-only | 20% | sapfdc | 1;2;3 | 0.317 | 0.000 |
| LLM-relevance | 5% | dtc | 1;2;3 | 0.329 | 0.000 |
| LLM-relevance | 5% | sapfdc | 1;2;3 | 0.222 | 0.000 |
| LLM-relevance | 10% | dtc | 1;2;3 | 0.447 | 0.000 |
| LLM-relevance | 10% | sapfdc | 1;2;3 | 0.287 | 0.000 |
| LLM-relevance | 20% | dtc | 1;2;3 | 0.515 | 0.013 |
| LLM-relevance | 20% | sapfdc | 1;2;3 | 0.380 | 0.007 |
| Random | 5% | dtc | 1;2;3 | 0.032 | 0.000 |
| Random | 5% | sapfdc | 1;2;3 | 0.022 | 0.000 |
| Random | 10% | dtc | 1;2;3 | 0.107 | 0.000 |
| Random | 10% | sapfdc | 1;2;3 | 0.039 | 0.000 |
| Random | 20% | dtc | 1;2;3 | 0.219 | 0.000 |
| Random | 20% | sapfdc | 1;2;3 | 0.094 | 0.000 |
| Single-call LLM | 5% | dtc | 1;2;3 | 0.329 | 0.000 |
| Single-call LLM | 5% | sapfdc | 1;2;3 | 0.241 | 0.000 |
| Single-call LLM | 10% | dtc | 1;2;3 | 0.424 | 0.000 |
| Single-call LLM | 10% | sapfdc | 1;2;3 | 0.304 | 0.000 |
| Single-call LLM | 20% | dtc | 1;2;3 | 0.568 | 0.000 |
| Single-call LLM | 20% | sapfdc | 1;2;3 | 0.406 | 0.000 |
| TF-IDF-only | 5% | dtc | 1;2;3 | 0.115 | 0.000 |
| TF-IDF-only | 5% | sapfdc | 1;2;3 | 0.083 | 0.000 |
| TF-IDF-only | 10% | dtc | 1;2;3 | 0.248 | 0.000 |
| TF-IDF-only | 10% | sapfdc | 1;2;3 | 0.152 | 0.000 |
| TF-IDF-only | 20% | dtc | 1;2;3 | 0.330 | 0.000 |
| TF-IDF-only | 20% | sapfdc | 1;2;3 | 0.212 | 0.000 |
| Tuned-weight (LLM) | 5% | dtc | 1;2;3 | 0.329 | 0.000 |
| Tuned-weight (LLM) | 5% | sapfdc | 1;2;3 | 0.222 | 0.000 |
| Tuned-weight (LLM) | 10% | dtc | 1;2;3 | 0.447 | 0.000 |
| Tuned-weight (LLM) | 10% | sapfdc | 1;2;3 | 0.282 | 0.000 |
| Tuned-weight (LLM) | 20% | dtc | 1;2;3 | 0.537 | 0.013 |
| Tuned-weight (LLM) | 20% | sapfdc | 1;2;3 | 0.378 | 0.007 |
| Tuned-weight (TF-IDF) | 5% | dtc | 1;2;3 | 0.283 | 0.000 |
| Tuned-weight (TF-IDF) | 5% | sapfdc | 1;2;3 | 0.207 | 0.000 |
| Tuned-weight (TF-IDF) | 10% | dtc | 1;2;3 | 0.378 | 0.000 |
| Tuned-weight (TF-IDF) | 10% | sapfdc | 1;2;3 | 0.264 | 0.000 |
| Tuned-weight (TF-IDF) | 20% | dtc | 1;2;3 | 0.522 | 0.000 |
| Tuned-weight (TF-IDF) | 20% | sapfdc | 1;2;3 | 0.365 | 0.000 |
