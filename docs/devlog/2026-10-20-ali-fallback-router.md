# Fallback router: a failed LLM call no longer stops the run

Date: 2026-10-20
Author: Muhammad Ali

## Observed failure or limitation

On the laptop CPU, LLM calls (`qwen2.5-coder:7b` on Ollama) took 39.1 s on average (`results/initial_results.csv`), close to the 60 s timeout (`llm.timeout_s` in `config.yaml`), and some calls exceeded it. Without handling, a timed-out or malformed answer would raise an exception inside the build, leaving that build with no result, so LLM-relevance could not be compared with DANTE on the same builds.

## Change

- `src/agent/fallback_router.py` sends every shortlisted test through the semantic analyzer and catches timeouts, invalid JSON, schema violations and answers with a confidence below `fallback.min_confidence` (0.3).
- Each failure becomes a `FallbackRecord` (reason, test, latency) that is stored with the build's result.
- With `fallback.scope: build`, one failed call makes the whole build use the DANTE-CCH ranking, so a build always gets a ranking and the comparison stays on the same builds.

## Measured effect

- **Phase 1 run (13 builds):** all 13 builds produced a result. In 4 of them the first call timed out and the build used the DANTE-CCH ranking (`results/initial_results.csv`, row `LLM-relevance`: `llm_fallbacks` 4, `llm_builds_fallen_back` 4).
- **Phase 2:** with one retry added before a fallback (`docs/devlog/2026-11-06-ali-llm-cache.md`) and inference on a GPU (`docs/devlog/2026-11-06-ali-kaggle-gpu.md`), `LLM-relevance` fell back on none of its 132 build-runs on the test split (`results/tables/efficiency.csv`, column `fallback_rate` 0.000).
