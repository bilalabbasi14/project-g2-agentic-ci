# Gap 3: the w chosen by the orchestrator

Written by `python -m src.eval.report`. From `orchestrator_decisions.csv` of the test-split runs; one decision per build, relevance source and run. DANTE's fixed weight is w = 2/3.

| Relevance source | Methods | Runs | Decisions | min | Q1 | median | Q3 | max | mean | distinct w | share w = 2/3 | fallback share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| llm_shortlist | Agent-weighted, Full system | 3 | 132 | 0.20 | 0.30 | 0.70 | 0.70 | 0.80 | 0.509 | 4 | 0.000 | 0.000 |
| llm_all_individual | Full system (no shortlist) | 1 | 20 | 0.20 | 0.20 | 0.30 | 0.70 | 0.80 | 0.455 | 4 | 0.000 | 0.000 |
| tfidf | Agent-weighted (TF-IDF) | 3 | 132 | 0.30 | 0.70 | 0.70 | 0.70 | 0.80 | 0.718 | 3 | 0.000 | 0.000 |
