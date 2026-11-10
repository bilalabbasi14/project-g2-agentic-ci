# Phase 2 final (`phase2-final`)

AI4015 Phase 2, group G2-05: an agentic layer on a local LLM (`qwen2.5-coder:7b` on Ollama) added to the DANTE test-selection baseline, evaluated on 44 test-split builds of Apache Karaf from the LRTS dataset. Full description: [README](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md).

## What this release contains

- **Code** (`src/`):
  - the DANTE baseline port;
  - the agent layer:
    - candidate shortlister;
    - semantic analyzer (Gap 1);
    - explainer (Gap 2);
    - orchestrator with tools (Gap 3);
    - fallback router;
  - the evaluation, statistics and report scripts.
- **Experiment definitions** (`experiments/`): E1–E6, the Kaggle runner notebook and the method and comparison lists.
- **Results** (`results/`), committed as produced by the scripts:
  - per-build CSVs and `run_meta.json` for every run;
  - the statistics (`results/stats/`);
  - the tables, the figures and the gap-resolution table (`results/tables/`, `results/figures/`);
  - the rated explanations (`results/gap2/`);
  - the failure analysis (`results/analysis/`, `docs/cases/`).
- **Trace samples** (`logs_sample/`) and the development log (`docs/devlog.md`, built from `docs/devlog/`).
- **Not included:**
  - the LRTS Karaf data, DANTE's stored results and the test-source cache: private Kaggle datasets shared with the group (see Installation);
  - the Karaf clone: from the public Apache repository (`https://github.com/apache/karaf.git`);
  - the LLM cache, the full traces and the per-build run JSONs: outputs of the Kaggle runs, kept outside the repository.

## How to reproduce

- **Installation** (Python 3.12, pinned libraries, data): [README §3](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md#3-installation).
- **Configuration and environment variables:** [README §4](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md#4-configuration-and-environment-variables).
- **A single build, with the mock provider or Ollama:** [README §5](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md#5-how-to-run).
- **Each experiment on Kaggle, and the analysis commands:** [README §6](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md#6-how-to-reproduce-each-experiment).
- **Tests:** `python -m pytest`. They need no data and no model.
- **Tables and figures:** `python -m src.eval.report` regenerates them from the committed CSVs. On a fresh clone it leaves `git status` clean.

## Results and limitations

- **Results:** [README §7](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md#7-results), copied from `results/tables/main_results.md` and `results/tables/gap_resolution.md`.
- **Changes since Phase 1:** [README §8](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md#8-changes-since-phase-1).
- **Known limitations and threats to validity:** [README §10](https://github.com/bilalabbasi14/project-g2-agentic-ci/blob/phase2-final/README.md#10-known-limitations-and-threats-to-validity).
