# LLM answer cache, seeds and one retry

Date: 2026-11-06
Author: Muhammad Ali

## Observed failure or limitation

Phase 1 inference was slow and fragile. In the 13-build Phase 1 run the LLM made 156 calls with a mean latency of 39.1 s per call, and 4 of the 13 builds fell back to the DANTE ranking because a single call timed out (no retry existed). Every rerun or ablation had to pay for the same calls again, since nothing was cached. Source: `results/initial_results.csv` (row `LLM-relevance`, columns `llm_calls`, `llm_mean_latency_s`, `llm_fallbacks`, `llm_builds_fallen_back`).

## Change

- `src/agent/llm_cache.py`: an on-disk cache keyed by model + prompt + options (temperature, seed, num_ctx) + JSON mode. Only successful calls are stored; entries keep the original latency and token counts, so cost numbers stay real when an answer is reused. Writes are atomic.
- Seeds 1, 2, 3 are part of the key, so repeated runs make their own calls; a retry uses seed + 1000 so it can give a different answer.
- `src/agent/retry.py`: one retry for a timed-out, failed, invalid-JSON or schema-violating call before a `FallbackRecord` is created; the relevance router now uses it.
- Each provider is created for one component and every call record says which component made it and whether it was cached, for the efficiency experiment (E6).

## Measured effect

To be measured in P2-21 (fallback rate, cached-call share and mean latency per component from the run's `per_build.csv`).
