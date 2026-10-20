# DANTE baseline: what we reproduce and known limitations of the shipped code

Our port is in `src/dante/` and follows the replication package's `src/` files
(function names are cited in each module). This page records what we found
when checking it against the stored results. Statements refer to the shipped
code in the replication package, not to the paper.

## Formulas as implemented (run_selection.py)

- History window: the 100 builds (`NUM_BUILDS_FOR_PROB_MODEL`) with a timestamp
  strictly earlier than the target, from all builds of the project.
- `THFR(t)` = mean outcome of t over the window.
- `P_n` = P(fail | sticky_n), pooled over all tests, for n = 1..10; 0 if fewer than
  20 sticky events. A Wilson interval is computed but not used in the score.
- `history(t) = THFR(t) + sum_n [last_outcome_n(t) == 1] * P_n / n`, where
  `last_outcome_n` is the outcome exactly n builds before (augment_history.py).
- Relevance: TF-IDF cosine between diff tokens of each changed file and test-class
  tokens, min-max normalised per changed file, max over files, then `** 1.2`.
- `base = 1.0 * history + 0.5 * relevance` (selection; RQ1 prioritisation uses 1.0).
- DANTE-CCH value = `base * max(failures in window, 0.1) / max(duration, 0.001)`.
- Candidates: test source file found and duration > 0. Budget: fraction of the
  summed duration of **all** test cases of the build. Greedy fill: skip a test
  that does not fit, keep scanning.

## Known limitations of the shipped code

1. **Relevance key mismatch.** `pipeline_orchestrator.py` stores relevance under
   `config.RELEVANCE_STRATEGY` = `"tfidf"`, while `run_selection.py` and
   `run_prioritization.py` read `cfg.RELEVANCE_STRATEGY_KEY`, which
   `experiment_config.py` sets to `"bm25"`. The lookup returns 0, so in the
   shipped code DANTE-CCH ranks on history (times failure count / duration) only.
   Evidence (`python -m src.dante.compare_stored --builds subset`, 13 builds with
   code changes): our relevance-off scores reproduce the stored `value_score` of
   82-86% of stored selected tests, our TF-IDF-on scores 3-4%.
   We report both: `DANTE-CCH-shipped` (relevance off) and `DANTE-CCH` (TF-IDF on).
2. **Sticky window mixes tests.** `is_sticky` is computed as
   `full_history.groupby('testclass')['outcome'].shift(1).rolling(window=n, min_periods=1).max()`.
   The shift is per test, but the rolling window runs over consecutive rows of the
   whole frame (other tests of the same build), not over the test's own history.
   We reproduce it as written; `sticky_mode="per_test"` in
   `src/dante/history.py` gives the per-test reading.
3. **last_outcome_n from processed builds only.** `augment_history.py` takes the
   previous builds from the set of processed JSON files, which is not in the
   package. We compute it from all earlier raw LRTS builds. This is the remaining
   cause of score differences (differences are exact sums of `P_n / n` terms).
4. **Tie order depends on library versions.** Many tests score 0; their order comes
   from pandas' unstable sort. With numpy 2.5 / pandas 3.0 only 3 of 50 builds
   matched the stored 5% selection; with the package's pinned numpy 1.26.4 /
   pandas 2.3.2 / scikit-learn 1.7.2, 26 of 50 match. `requirements.txt` pins these.
5. **Metric code.** SAPFDc, SDS and %DTC_FLK are described in the package readme
   but not implemented in `src/`. `post_hoc_prioritizer.calculate_napfdc` falls
   back to the selected tests when the full test list is missing, which makes
   fault coverage 1; we do not use it.
6. **Data path.** `run_selection.py` reads `artifact/processed_test_result/...`;
   the LRTS archive has no `artifact/` folder.

## Reproduction status (re-run: `python -m src.dante.compare_stored`)

Failing-class counts: LRTS `num_fail_class` differs from stored
`total_failures_in_build` in 8 of 50 builds, always by one entry,
`org.apache.maven.surefire.junit4.JUnit4Provider`, which has no source file and
is therefore not a candidate. Our candidate failure counts equal the stored
totals in all 50 builds.
