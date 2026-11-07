# Relevance prompt v2: a calibrated scale with anchors

Date: 2026-11-06
Author: Muhammad Ali

## Observed failure or limitation

In Phase 1 the LLM gave a relevance of at most 0.2 to 94% of the tests it scored (docs/PROJECT_CONTEXT.md §3, finding 5). So LLM relevance barely changed DANTE's ranking.

The v1 prompt only says "0 = unrelated, 1 = directly tests the changed code". It gives the model no intermediate points and no procedure for comparing the test with the change.

The same measure is taken again for v1 on the dev split (`share_rel_le_0_2` in `results/dev/prompt_comparison.csv`), so that before and after come from the same builds.

## Change

- `src/agent/semantic_analyzer.py`: `PROMPT_TEMPLATE` (v1) is unchanged; a test pins its SHA-256. A new `PROMPT_TEMPLATE_V2` (`"v2"`) differs from v1 in two ways:
  - **Anchors.** It explains the scale with four anchors: 0.0 = unrelated module; 0.3 = same subsystem, different functionality; 0.6 = the test uses a class or package the change touches; 0.9 = the test directly tests a changed class or method.
  - **Comparison step.** It asks the model, before deciding, to compare the test's package, imports and used identifiers with the changed file paths and identifiers.

  The JSON answer shape, the anonymisation and the truncation are the same as v1.
- **Version selection.** `llm_p2.relevance_prompt_version` in the config selects the template. `make_request(..., prompt_version=...)` records it in every `RelevanceRequest` and in `llm_relevance.csv`.
- **Runner option.** `python -m experiments.run_experiment ... --relevance-prompt v1|v2` overrides the config for the two dev runs.
- **Comparison.** `src/agent/prompt_eval.py` compares the two dev runs and applies the decision rule, fixed before the runs: the higher `sapfdc_mean_10` wins; within 0.005, the lower `share_rel_le_0_2` wins.

## Measured effect

Two Kaggle runs on the **dev split only**: 10 builds, seed 1, methods `LLM-relevance` and `DANTE-CCH`. Both ran from commit fbe1b2b on 2 × T4 (`qwen2.5-coder:7b`), with no fallbacks and no failed builds (`results/DEV_prompt_v1/run_meta.json`, `results/DEV_prompt_v2/run_meta.json`). No test-split run was made. The numbers are in `results/dev/prompt_comparison.csv`, written by `python -m src.agent.prompt_eval --runs results/DEV_prompt_v1 results/DEV_prompt_v2`:

| prompt | builds | sapfdc_mean_10 | dtc_mean_10 | share_rel_le_0_2 | share_rel_ge_0_5 | fallback_builds | mean_latency_s |
|---|---|---|---|---|---|---|---|
| v1 | 10 | 0.6725 | 0.7167 | 0.976 | 0.024 | 0 | 3.19 |
| v2 | 10 | 0.6671 | 0.7167 | 0.112 | 0.053 | 0 | 3.40 |

- **Calibration.** v2 does fix the calibration problem. The share of scores at or below 0.2 drops from 97.6% (v1; the Phase 1 problem reproduced on dev) to 11.2%. The share at or above 0.5 rises only from 2.4% to 5.3%, so v2 mostly moves scores to the 0.3 anchor ("same subsystem").
- **Ranking.** This barely changes the ranking. The mean %DTC at 10% is identical (0.7167), and on every dev build each prompt finds the same failing tests. The mean SAPFDc at 10% is 0.0054 lower for v2. Most of that comes from one build, `PR-1377_build4` (0.473 with v1, 0.418 with v2), visible in both runs' `per_build.csv`.
- **Cost.** v2 costs about 7% more latency per call (3.40 s against 3.19 s) because its prompt is longer.

**Decision**, by the rule fixed before the runs: the higher `sapfdc_mean_10` wins unless the two are within 0.005. The difference is 0.0054, above the margin, so **v1** is chosen, and `relevance_prompt_version` stays `v1` in `config.yaml`.

The better calibration of v2 is therefore not used for the reported results. That is a negative result for this prompt change, reported as measured. P2-11 uses `results/DEV_prompt_v1/llm_relevance.csv` (the chosen prompt's dev scores).
