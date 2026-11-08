# Main results (test split)

Written by `python -m src.eval.report`. %DTC and SAPFDc: mean over builds of the per-build mean over seeds ± std over seeds (`results/stats/seed_variability.csv`; — = one seed). APFDc of the full ranking and SDS: median over builds. APFDc follows DANTE's formula, which adds 1/(2n); SAPFDc = %DTC × APFDc of the selection can therefore exceed 1 slightly on small selections (`src/eval/metrics.py`).

| Method | Budget | Seeds | Builds | %DTC | SAPFDc | APFDc (median) | SDS (median) |
|---|---|---|---|---|---|---|---|
| Random | 5% | 3 | 44 | 0.032 ± 0.000 | 0.022 ± 0.000 | 0.547 | 0.691 |
| Random | 10% | 3 | 44 | 0.107 ± 0.000 | 0.039 ± 0.000 | 0.547 | 0.655 |
| Random | 20% | 3 | 44 | 0.219 ± 0.000 | 0.094 ± 0.000 | 0.547 | 0.589 |
| History-only | 5% | 3 | 44 | 0.282 ± 0.000 | 0.163 ± 0.000 | 0.798 | 0.615 |
| History-only | 10% | 3 | 44 | 0.398 ± 0.000 | 0.231 ± 0.000 | 0.798 | 0.587 |
| History-only | 20% | 3 | 44 | 0.492 ± 0.000 | 0.317 ± 0.000 | 0.798 | 0.506 |
| TF-IDF-only | 5% | 3 | 44 | 0.115 ± 0.000 | 0.083 ± 0.000 | 0.597 | 0.594 |
| TF-IDF-only | 10% | 3 | 44 | 0.248 ± 0.000 | 0.152 ± 0.000 | 0.597 | 0.562 |
| TF-IDF-only | 20% | 3 | 44 | 0.330 ± 0.000 | 0.212 ± 0.000 | 0.597 | 0.523 |
| DANTE-CCH-shipped | 5% | 3 | 44 | 0.283 ± 0.000 | 0.207 ± 0.000 | 0.770 | 0.586 |
| DANTE-CCH-shipped | 10% | 3 | 44 | 0.378 ± 0.000 | 0.264 ± 0.000 | 0.770 | 0.538 |
| DANTE-CCH-shipped | 20% | 3 | 44 | 0.522 ± 0.000 | 0.365 ± 0.000 | 0.770 | 0.500 |
| DANTE-CCH | 5% | 3 | 44 | 0.283 ± 0.000 | 0.226 ± 0.000 | 0.796 | 0.556 |
| DANTE-CCH | 10% | 3 | 44 | 0.356 ± 0.000 | 0.274 ± 0.000 | 0.796 | 0.521 |
| DANTE-CCH | 20% | 3 | 44 | 0.545 ± 0.000 | 0.370 ± 0.000 | 0.796 | 0.479 |
| Tuned-weight (TF-IDF) | 5% | 3 | 44 | 0.283 ± 0.000 | 0.207 ± 0.000 | 0.770 | 0.586 |
| Tuned-weight (TF-IDF) | 10% | 3 | 44 | 0.378 ± 0.000 | 0.264 ± 0.000 | 0.770 | 0.538 |
| Tuned-weight (TF-IDF) | 20% | 3 | 44 | 0.522 ± 0.000 | 0.365 ± 0.000 | 0.770 | 0.500 |
| Single-call LLM | 5% | 3 | 44 | 0.329 ± 0.000 | 0.241 ± 0.000 | 0.826 | 0.590 |
| Single-call LLM | 10% | 3 | 44 | 0.424 ± 0.000 | 0.304 ± 0.000 | 0.826 | 0.536 |
| Single-call LLM | 20% | 3 | 44 | 0.568 ± 0.000 | 0.406 ± 0.000 | 0.826 | 0.494 |
| LLM-relevance | 5% | 3 | 44 | 0.329 ± 0.000 | 0.222 ± 0.000 | 0.824 | 0.608 |
| LLM-relevance | 10% | 3 | 44 | 0.447 ± 0.000 | 0.287 ± 0.000 | 0.824 | 0.562 |
| LLM-relevance | 20% | 3 | 44 | 0.515 ± 0.013 | 0.380 ± 0.007 | 0.824 | 0.517 |
| Tuned-weight (LLM) | 5% | 3 | 44 | 0.329 ± 0.000 | 0.222 ± 0.000 | 0.819 | 0.603 |
| Tuned-weight (LLM) | 10% | 3 | 44 | 0.447 ± 0.000 | 0.282 ± 0.000 | 0.819 | 0.562 |
| Tuned-weight (LLM) | 20% | 3 | 44 | 0.537 ± 0.013 | 0.378 ± 0.007 | 0.819 | 0.521 |
| Agent-weighted | 5% | 3 | 44 | 0.306 ± 0.000 | 0.219 ± 0.000 | 0.848 | 0.600 |
| Agent-weighted | 10% | 3 | 44 | 0.424 ± 0.000 | 0.274 ± 0.000 | 0.848 | 0.577 |
| Agent-weighted | 20% | 3 | 44 | 0.560 ± 0.013 | 0.392 ± 0.007 | 0.848 | 0.507 |
| Full system | 5% | 3 | 44 | 0.306 ± 0.000 | 0.219 ± 0.000 | 0.848 | 0.600 |
| Full system | 10% | 3 | 44 | 0.424 ± 0.000 | 0.274 ± 0.000 | 0.848 | 0.577 |
| Full system | 20% | 3 | 44 | 0.560 ± 0.013 | 0.392 ± 0.007 | 0.848 | 0.507 |
| Agent-weighted (TF-IDF) | 5% | 3 | 44 | 0.283 ± 0.000 | 0.227 ± 0.000 | 0.796 | 0.556 |
| Agent-weighted (TF-IDF) | 10% | 3 | 44 | 0.356 ± 0.000 | 0.275 ± 0.000 | 0.796 | 0.521 |
| Agent-weighted (TF-IDF) | 20% | 3 | 44 | 0.545 ± 0.000 | 0.373 ± 0.000 | 0.796 | 0.479 |
| Full system (no shortlist) | 5% | 3 | 44 | 0.338 ± 0.000 | 0.246 ± 0.000 | 0.823 | 0.528 |
| Full system (no shortlist) | 10% | 3 | 44 | 0.441 ± 0.000 | 0.281 ± 0.000 | 0.823 | 0.514 |
| Full system (no shortlist) | 20% | 3 | 44 | 0.538 ± 0.013 | 0.392 ± 0.006 | 0.823 | 0.468 |
