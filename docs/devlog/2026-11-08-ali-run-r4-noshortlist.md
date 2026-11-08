# Run R4 (no-shortlist ablation on all test builds, seeds 1–3)

Date: 2026-11-08
Author: Muhammad Ali

## Observed failure or limitation

R3 ran `Full system (no shortlist)` on the first 20 test builds with seed 1 only (`build_limit: 20`), because scoring every candidate needs about 200 LLM calls per build and the deadline left no GPU time for more. Every other method had all 44 test builds and seeds 1–3, so the ablation had no standard deviation and covered less than half of the test split.

## Change

After the deadline was extended, P2-38 (#74) removed the limit, with no change to any prompt, threshold, weight or method:

- **Configuration:**
  - `build_limit` removed and `seeds: [1, 2, 3]` set in `experiments/configs/E5_noshortlist.yaml`;
  - `ablation.no_shortlist_builds: 44` and `no_shortlist_seeds: [1, 2, 3]` in `config.yaml` and `config_kaggle.yaml`.
- **Run:** `experiments/kaggle_runner.ipynb` on Kaggle (GPU T4×2, two Ollama servers, shards 0/2 and 1/2, then `merge_shards`), with `config_kaggle.yaml`.
  - `REPO_REF = 919cdf78cc60a1045b7c20a2ebccd324fd010df6`; the clone cell printed `919cdf7 Run the no-shortlist ablation on all test builds with seeds 1-3`.
  - `E5_noshortlist`, test split, seeds 1, 2 and 3, one after the other in one committed session.
  - The `g2-llm-cache` dataset was updated with R3's cache before the run; the notebook copied 4,998 cached answers (R1 and R3).
- **The first attempt stopped in the GPU check cell** because the imported notebook had no accelerator set. Nothing ran; the rerun with GPU T4×2 is the one reported here.
- **Times** (`started`/`finished` in `run_meta.json`, UTC): seed 1 04:50–06:08; seed 2 06:08–08:22; seed 3 08:22–10:37.

## Measured effect

Source: `results/E5_noshortlist_test_seed{1,2,3}/`, `results/tables/` and `results/stats/`.

- **`run_meta.json`, every seed:** 44 test builds, `failed_builds` and `skipped_existing` empty, `git_commit` 919cdf7…, no `git_commit_warning`.
- **Rows:** 44 builds × 3 budgets = 132 rows per seed, exactly the P2-15 columns, no duplicate (build, method, budget) rows, no missing `dtc` or `sapfdc`. The builds are exactly the 44 test builds of `data_eval/eval_builds_p2.csv`.
- **Same as R3 on R3's builds.** On the first 20 test builds, seed 1, all 4,010 LLM calls were answered from the cache, and `per_build.csv` equals R3's in every column except the latencies, `llm_cached_calls` and `completion_tokens` (15 rows, 5 builds). `orchestrator_decisions.csv` is identical, and `llm_relevance.csv` differs only in 7 `reason` texts; relevance and confidence are identical.
  - **Cause of the 7 reasons:** each of these prompts also occurs in another build of the same pull request with the same diff (for example `PR-1427_build2` and `PR-1427_build3`). In R3 the two shards computed it separately and the cache kept one of the two answers; R4 read that answer. The same explains the token counts.
- **Relevance:** the LLM scored every candidate in every seed (8,695 `llm_relevance.csv` rows = the sum of `candidates`), with no fallback.
- **Orchestrator:** every decision came from the agent; no tool call; w took 4 distinct values in each seed.
- **Cache:** of 8,739 LLM calls per seed, 5,279 (seed 1), 2,622 (seed 2) and 2,624 (seed 3) came from the cache. Seeds 2 and 3 used the cache only within the run, for prompts repeated across builds of the same pull request.
- **Results** (`results/tables/main_results.md`, `ablation.md`): standard deviations over seeds are now reported. The comparison with `Full system` in `ablation.md` is now on 44 builds and 3 seeds.
- **Statistics:** `results/stats/pairwise.csv` and `friedman.csv` are unchanged, because the method is not in `experiments/comparisons.yaml`; `seed_variability.csv` gained its six rows.
- **Cost:** the three seeds took 5.77 GPU-hours (`results/tables/efficiency.md`).
