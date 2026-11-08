# Efficiency and reliability (E6)

Written by `python -m src.eval.report`. Per build and run. Decision = relevance + orchestrator calls (tokens are for these calls; explainer tokens are in `explanations.csv`). Latencies are the original ones, also for answers taken from the LLM cache. Explainer columns use only runs with the explainer on. Fallback rate = share of builds whose relevance used the DANTE fallback or whose orchestrator fell back. GPU-hours = wall-clock hours of the runs containing the method (T4×2 session, `run_meta.json`); a run is shared by all its methods, so these hours are not exclusive. All test-split runs with the model: 11.02 h (12 runs); dev-split runs: 0.49 h (5 runs).

| Method | Builds × runs | LLM calls | Cached share | Tool calls | Prompt tokens | Completion tokens | Decision s | Relevance s | Orchestrator s | Explanation s | Explanations failed | Fallback rate | GPU-hours |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Single-call LLM | 132 | 1.0 | 0.000 | 0.00 | 4106 | 5144 | 200.8 | 200.8 | 0.0 | — | — | 0.023 | 3.78 |
| LLM-relevance | 132 | 18.3 | 0.240 | 0.00 | 25773 | 1122 | 46.9 | 46.9 | 0.0 | — | — | 0.000 | 1.40 |
| Tuned-weight (LLM) | 132 | 18.3 | 0.240 | 0.00 | 25773 | 1122 | 46.9 | 46.9 | 0.0 | — | — | 0.000 | 1.40 |
| Agent-weighted | 132 | 19.3 | 0.228 | 0.00 | 27645 | 1164 | 49.7 | 46.9 | 2.9 | — | — | 0.000 | 1.40 |
| Full system | 132 | 19.3 | 0.228 | 0.00 | 27645 | 1164 | 49.7 | 46.9 | 2.9 | 101.2 | 0.247 | 0.000 | 1.40 |
| Agent-weighted (TF-IDF) | 132 | 1.0 | 0.000 | 0.00 | 1780 | 46 | 2.0 | 0.0 | 2.0 | — | — | 0.000 | 0.08 |
| Full system (no shortlist) | 132 | 198.6 | 0.401 | 0.00 | 278487 | 12000 | 522.6 | — | — | — | — | 0.000 | 5.77 |
