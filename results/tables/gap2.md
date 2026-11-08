# Gap 2: explanation cost vs time saved, and rating (RQ2)

Written by `python -m src.eval.report`. Latency: `Full system` rows of the runs with the explainer on (`results/E3_test_seed1/per_build.csv`); overhead = decision (relevance + orchestrator) + explanation time of the build at that budget; time saved = total suite time − selected time; "Overhead < saved" counts build-budget pairs (the overall row pools the three budgets). Ratings: `results/gap2/rating_summary.csv`.

| Scope | Budget | Builds | Decision s | Explanation s | Overhead s | Time saved s | Overhead < saved | Rated | Sound | Partly | Unsound | kappa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| budget | 5% | 44 | 49.9 | 37.4 | 87.3 | 1579.2 | 43/44 | 34 | 0.765 | 0.088 | 0.147 | 0.705 |
| budget | 10% | 44 | 49.9 | 36.5 | 86.4 | 1513.3 | 43/44 | 33 | 0.758 | 0.030 | 0.212 | 0.705 |
| budget | 20% | 44 | 49.9 | 27.3 | 77.2 | 1386.9 | 43/44 | 33 | 0.394 | 0.061 | 0.545 | 0.705 |
| overall | — | 44 | 49.9 | 33.7 | 83.6 | 1493.2 | 129/132 | 100 | 0.640 | 0.060 | 0.300 | 0.705 |
