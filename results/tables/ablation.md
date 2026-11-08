# Ablations (E5): Full system vs each ablation

Written by `python -m src.eval.report`. Paired on the builds and seeds both methods have; change = ablation − Full system (negative = the removed component helps). p (Holm) and r from `results/stats/pairwise.csv` (family E5, r > 0 = Full system better) where that pair is tested there; — otherwise. The explainer never changes the selection, so removing it changes only cost.

| Ablation | Removed | Metric | Budget | Seeds | Builds | Full system | Ablation | Change | p (Holm) | r |
|---|---|---|---|---|---|---|---|---|---|---|
| LLM-relevance | orchestrator | %DTC | 5% | 1;2;3 | 44 | 0.306 | 0.329 | 0.023 | 0.6346 | -1.000 |
| LLM-relevance | orchestrator | %DTC | 10% | 1;2;3 | 44 | 0.424 | 0.447 | 0.023 | 0.3173 | -1.000 |
| LLM-relevance | orchestrator | %DTC | 20% | 1;2;3 | 44 | 0.560 | 0.515 | -0.045 | 0.3146 | 1.000 |
| LLM-relevance | orchestrator | SAPFDc | 5% | 1;2;3 | 44 | 0.219 | 0.222 | 0.003 | 1.0000 | 0.143 |
| LLM-relevance | orchestrator | SAPFDc | 10% | 1;2;3 | 44 | 0.274 | 0.287 | 0.013 | 0.8155 | -0.238 |
| LLM-relevance | orchestrator | SAPFDc | 20% | 1;2;3 | 44 | 0.392 | 0.380 | -0.012 | 0.1644 | 0.600 |
| Agent-weighted (TF-IDF) | LLM relevance | %DTC | 5% | 1;2;3 | 44 | 0.306 | 0.283 | -0.023 | 0.6547 | 0.200 |
| Agent-weighted (TF-IDF) | LLM relevance | %DTC | 10% | 1;2;3 | 44 | 0.424 | 0.356 | -0.068 | 0.1665 | 1.000 |
| Agent-weighted (TF-IDF) | LLM relevance | %DTC | 20% | 1;2;3 | 44 | 0.560 | 0.545 | -0.015 | 0.8875 | 0.067 |
| Agent-weighted (TF-IDF) | LLM relevance | SAPFDc | 5% | 1;2;3 | 44 | 0.219 | 0.227 | 0.008 | 1.0000 | 0.067 |
| Agent-weighted (TF-IDF) | LLM relevance | SAPFDc | 10% | 1;2;3 | 44 | 0.274 | 0.275 | 0.001 | 0.8155 | 0.202 |
| Agent-weighted (TF-IDF) | LLM relevance | SAPFDc | 20% | 1;2;3 | 44 | 0.392 | 0.373 | -0.019 | 0.1644 | 0.363 |
| Agent-weighted | explainer | %DTC | 5% | 1;2;3 | 44 | 0.306 | 0.306 | 0.000 | — | — |
| Agent-weighted | explainer | %DTC | 10% | 1;2;3 | 44 | 0.424 | 0.424 | 0.000 | — | — |
| Agent-weighted | explainer | %DTC | 20% | 1;2;3 | 44 | 0.560 | 0.560 | 0.000 | — | — |
| Agent-weighted | explainer | SAPFDc | 5% | 1;2;3 | 44 | 0.219 | 0.219 | 0.000 | — | — |
| Agent-weighted | explainer | SAPFDc | 10% | 1;2;3 | 44 | 0.274 | 0.274 | 0.000 | — | — |
| Agent-weighted | explainer | SAPFDc | 20% | 1;2;3 | 44 | 0.392 | 0.392 | 0.000 | — | — |
| Full system (no shortlist) | shortlist | %DTC | 5% | 1 | 20 | 0.292 | 0.329 | 0.038 | — | — |
| Full system (no shortlist) | shortlist | %DTC | 10% | 1 | 20 | 0.454 | 0.442 | -0.013 | — | — |
| Full system (no shortlist) | shortlist | %DTC | 20% | 1 | 20 | 0.554 | 0.504 | -0.050 | — | — |
| Full system (no shortlist) | shortlist | SAPFDc | 5% | 1 | 20 | 0.238 | 0.283 | 0.045 | — | — |
| Full system (no shortlist) | shortlist | SAPFDc | 10% | 1 | 20 | 0.308 | 0.338 | 0.030 | — | — |
| Full system (no shortlist) | shortlist | SAPFDc | 20% | 1 | 20 | 0.416 | 0.422 | 0.006 | — | — |
