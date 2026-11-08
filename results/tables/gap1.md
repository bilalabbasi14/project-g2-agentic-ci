# Gap 1: LLM-relevance vs DANTE (RQ1)

Written by `python -m src.eval.report`. From `results/stats/pairwise.csv` (family RQ1) and `main_results`. Mean diff = target − other over the shared builds; r > 0 = target better.

Shortlist recall at k = 10 (the k used; `results/analysis/shortlist_recall_test.csv`): mean 0.676 over 44 builds; a failing test outside the shortlist gets LLM relevance 0.

| Metric | Budget | Target mean | Other | Other mean | Mean diff | W/T/L | p (Holm) | Sig. | r |
|---|---|---|---|---|---|---|---|---|---|
| %DTC | 5% | 0.329 | DANTE-CCH | 0.283 | 0.045 | 4/38/2 | 0.4142 | no | 0.333 |
| %DTC | 5% | 0.329 | DANTE-CCH-shipped | 0.283 | 0.045 | 2/42/0 | 0.3146 | no | 1.000 |
| %DTC | 10% | 0.447 | DANTE-CCH | 0.356 | 0.091 | 4/40/0 | 0.0910 | no | 1.000 |
| %DTC | 10% | 0.447 | DANTE-CCH-shipped | 0.378 | 0.068 | 4/40/0 | 0.0910 | no | 1.000 |
| %DTC | 20% | 0.515 | DANTE-CCH | 0.545 | -0.030 | 1/41/2 | 0.5526 | no | -0.667 |
| %DTC | 20% | 0.515 | DANTE-CCH-shipped | 0.522 | -0.007 | 2/40/2 | 0.8539 | no | -0.100 |
| SAPFDc | 5% | 0.222 | DANTE-CCH | 0.226 | -0.004 | 14/23/7 | 0.6143 | no | 0.126 |
| SAPFDc | 5% | 0.222 | DANTE-CCH-shipped | 0.207 | 0.015 | 5/27/12 | 0.4923 | no | -0.320 |
| SAPFDc | 10% | 0.287 | DANTE-CCH | 0.274 | 0.013 | 17/21/6 | 0.2275 | no | 0.377 |
| SAPFDc | 10% | 0.287 | DANTE-CCH-shipped | 0.264 | 0.023 | 11/25/8 | 0.4939 | no | 0.179 |
| SAPFDc | 20% | 0.380 | DANTE-CCH | 0.370 | 0.010 | 23/16/5 | 0.0723 | no | 0.453 |
| SAPFDc | 20% | 0.380 | DANTE-CCH-shipped | 0.365 | 0.015 | 11/20/13 | 0.4576 | no | -0.173 |
