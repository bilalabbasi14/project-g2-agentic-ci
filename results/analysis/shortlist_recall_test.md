# Shortlist recall — test split

Command: `python -m src.eval.shortlist_recall --split test --k 5 10 15 20`

Builds: 44 (split `test` of the evaluation set). For each build, the failing candidates come from the build's own outcomes, used only as ground truth here.

recall@k = failing candidates on the shortlist / failing candidates. The shortlist is the union of the top k candidates by history score and the top k by TF-IDF relevance (DANTE-CCH scores; candidates with a score of 0 are not taken from a list). A failing test outside the shortlist gets LLM relevance 0.

**k = 10 is the configuration actually used** (`shortlist.k` in config.yaml, fixed in Phase 1). The other k values only describe the limit of the shortlist; they are not used to change k.

| k | configuration | builds | mean recall | median recall | share recall = 0 | share recall = 1 | mean shortlist size |
|---|---|---|---|---|---|---|---|
| 5 | describes the limit only | 44 | 0.436 | 0.292 | 0.455 | 0.364 | 9.3 |
| **10** | **used** | 44 | 0.676 | 1.000 | 0.250 | 0.614 | 18.3 |
| 15 | describes the limit only | 44 | 0.729 | 1.000 | 0.205 | 0.682 | 26.5 |
| 20 | describes the limit only | 44 | 0.753 | 1.000 | 0.182 | 0.705 | 33.0 |
