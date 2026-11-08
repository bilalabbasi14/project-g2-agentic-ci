# Gap 3: Agent-weighted vs DANTE and the tuned weight (RQ3)

Written by `python -m src.eval.report`. From `results/stats/pairwise.csv` (family RQ3) and `main_results`. The agent's w is in `gap3_w`.

| Metric | Budget | Target mean | Other | Other mean | Mean diff | W/T/L | p (Holm) | Sig. | r |
|---|---|---|---|---|---|---|---|---|---|
| %DTC | 5% | 0.306 | DANTE-CCH | 0.283 | 0.023 | 3/39/2 | 0.6547 | no | 0.200 |
| %DTC | 5% | 0.306 | Tuned-weight (LLM) | 0.329 | -0.023 | 0/43/1 | 0.6346 | no | -1.000 |
| %DTC | 10% | 0.424 | DANTE-CCH | 0.356 | 0.068 | 3/41/0 | 0.1665 | no | 1.000 |
| %DTC | 10% | 0.424 | Tuned-weight (LLM) | 0.447 | -0.023 | 0/43/1 | 0.3173 | no | -1.000 |
| %DTC | 20% | 0.560 | DANTE-CCH | 0.545 | 0.015 | 3/39/2 | 0.8994 | no | 0.067 |
| %DTC | 20% | 0.560 | Tuned-weight (LLM) | 0.537 | 0.023 | 3/40/1 | 0.8994 | no | 0.400 |
| SAPFDc | 5% | 0.219 | DANTE-CCH | 0.226 | -0.007 | 13/24/7 | 1.0000 | no | 0.067 |
| SAPFDc | 5% | 0.219 | Tuned-weight (LLM) | 0.222 | -0.003 | 3/36/5 | 1.0000 | no | -0.222 |
| SAPFDc | 10% | 0.274 | DANTE-CCH | 0.274 | -0.000 | 15/22/7 | 0.6764 | no | 0.233 |
| SAPFDc | 10% | 0.274 | Tuned-weight (LLM) | 0.282 | -0.008 | 4/35/5 | 0.6784 | no | -0.156 |
| SAPFDc | 20% | 0.392 | DANTE-CCH | 0.370 | 0.022 | 24/14/6 | 0.0814 | no | 0.428 |
| SAPFDc | 20% | 0.392 | Tuned-weight (LLM) | 0.378 | 0.014 | 8/30/6 | 0.3305 | no | 0.295 |
