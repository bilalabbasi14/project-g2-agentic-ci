# Inference moved from a laptop CPU to free Kaggle T4 GPUs

Date: 2026-11-06
Author: Muhammad Ali

## Observed failure or limitation

In Phase 1 the LLM ran on a laptop CPU. The 13-build run made 156 calls with a mean latency of 39.1 s per call (`results/initial_results.csv`, row `LLM-relevance`, column `llm_mean_latency_s`). At that speed the planned Phase 2 runs (44 test builds, three seeds, several LLM methods, about 20 calls per build for the full system) would not fit in the time left before the deadline.

## Change

- `experiments/kaggle_runner.ipynb` runs any experiment config on a free Kaggle notebook with two T4 GPUs: one Ollama server per GPU (ports 11434 and 11435), the builds split into two shards (`--shard 0/2`, `--shard 1/2`), then `experiments.merge_shards`.
- Kaggle ships Python 3.13, but the pinned `numpy==1.26.4` needs Python 3.12 or older, so the notebook creates a Python 3.12 environment with `uv`.
- `config_kaggle.yaml` has the same keys as `config.yaml` with Kaggle paths; a test checks that only the paths differ.
- The data and the test-source cache are private Kaggle datasets, so the notebook needs no git clone of Karaf (`data/README.md`).
- One warm-up call per server keeps the model-loading time out of the measured latencies.

## Measured effect

- **Latency per relevance call:** 39.1 s on the laptop CPU (`results/initial_results.csv`) against 3.19 s on a T4 in the dev run with the chosen prompt (`results/dev/prompt_comparison.csv`, row `v1`, column `mean_latency_s`).
- **Whole evaluation:** all ten test-split runs that call the model took 6.36 wall-clock hours on T4×2 in total, and the five dev-split runs 0.49 h (`results/tables/efficiency.md`).
