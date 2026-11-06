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

To be filled from `results/dev/prompt_comparison.csv` after the two dev-split Kaggle runs (`DEV_prompt_v1`, `DEV_prompt_v2`; seed 1; methods `LLM-relevance`, `DANTE-CCH`). The numbers will be `sapfdc_mean_10`, `dtc_mean_10`, `share_rel_le_0_2`, `share_rel_ge_0_5`, `fallback_builds` and `mean_latency_s` per prompt, with the decision and the resulting `relevance_prompt_version` in `config.yaml`. No test-split run is made for this choice.
