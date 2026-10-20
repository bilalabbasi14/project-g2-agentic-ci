# Agentic AI-Driven Optimization of CI Pipelines (AI4015, group G2-05)

## What this is

Large projects re-run long test suites on every code change. When only part of
the suite can run, which tests should run first to catch the most failures within
a time budget (a percentage of the full suite's run time)?

DANTE (ICST 2026) answers this with two signals per test class: how often and how
persistently it failed before (history), and how similar its source is to the
changed code (TF-IDF relevance). Tests are ranked and taken from the top until the
budget is used.

This project asks whether replacing the TF-IDF relevance with a local LLM's
judgement of relevance finds more failures within the same budget. It does not
assume the answer. Phase 1 builds the pipeline, reproduces the DANTE baseline and
reports an **initial run on few builds; no conclusion is drawn from it**.

## Initial results (Phase 1)

**Initial run on 13 karaf builds, one model; no conclusion is drawn.** The 13
builds are the evaluation builds whose diff changes code files (see limitations).
Budgets are 5/10/20% of each build's total test time. Produced by
`python run_end_to_end.py --subset --budget 5 10 20` and
`python -m src.eval.summarize`; full numbers in `results/initial_results.csv`.

| Method | %DTC 5% | %DTC 10% | %DTC 20% | SAPFDc 5% | SAPFDc 10% | SAPFDc 20% | APFDc |
|---|---|---|---|---|---|---|---|
| Random (stored) | 0.031 | 0.156 | 0.191 | 0.006 | 0.031 | 0.070 | 0.487 |
| Random | 0.031 | 0.156 | 0.191 | 0.006 | 0.031 | 0.070 | 0.487 |
| DANTE-CCH (stored) | 0.318 | 0.435 | 0.459 | 0.271 | 0.342 | 0.398 | 0.729 |
| DANTE-CCH-shipped | 0.318 | 0.409 | 0.459 | 0.264 | 0.327 | 0.394 | 0.729 |
| DANTE-CCH | 0.318 | 0.487 | 0.512 | 0.270 | 0.352 | 0.399 | 0.678 |
| History-only | 0.333 | 0.374 | 0.433 | 0.229 | 0.258 | 0.349 | 0.562 |
| TF-IDF-only | 0.312 | 0.404 | 0.476 | 0.247 | 0.317 | 0.392 | 0.685 |
| LLM-relevance | 0.344 | 0.487 | 0.487 | 0.275 | 0.356 | 0.405 | 0.795 |

%DTC and SAPFDc: mean over the 13 builds. APFDc: median over builds of the full
ranking (for stored methods, the `apfdc` column of DANTE's RQ1 CSV).

LLM (`qwen2.5-coder:7b` via Ollama, local): 156 calls, mean latency 39.1 s,
218,451 prompt and 9,451 completion tokens, **4 fallbacks**: in 4 of the 13 builds
the first call timed out (60 s) and the build used the DANTE-CCH ranking, so for
those builds LLM-relevance equals DANTE-CCH. Re-timing one of these calls on an
idle server took 13.8 s; the timeouts look transient, cause not established.

Baseline checks (re-run with the commands below):
- Stored RQ1 DANTE-CCH median APFDc over all 9 projects: 0.8721 (448 rows); karaf 0.7183.
- APFDc of our DANTE-CCH-shipped ordering vs the RQ1 karaf column (50 builds):
  median difference +0.0000, |difference| <= 0.02 in 45 of 50 builds.
- Our Random selections equal the stored Random selections on the 13 builds.

## Setup

Requires Python 3.12 and Git. On Windows run `git config core.longpaths true`.

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

`requirements.txt` pins numpy 1.26.4, pandas 2.3.2 and scikit-learn 1.7.2, the
versions in the DANTE package's lock file; tie order among equal scores (and so the
selected tests) depends on them.

Data (nothing is committed; see `data/README.md`): put `long_running_test_suites.zip`
and `ML_TCSP.zip` in a folder and run

```
python -m src.data.extract_inputs --downloads <that folder>
git -c http.version=HTTP/1.1 clone --filter=blob:none --no-checkout https://github.com/apache/karaf.git C:/g2w/repos/karaf
python -m src.data.make_eval_builds
```

Paths are in `config.yaml` (default `C:/g2w/...`).

Local LLM: install Ollama (`winget install Ollama.Ollama`), then
`ollama pull qwen2.5-coder:7b`. Check it with `python -m src.agent.llm_smoke`.

## How to run

| Step | Command |
|---|---|
| Reproduce stored DANTE numbers (RQ1 median APFDc, stored %DTC/SAPFDc/SDS) | `python -m src.eval.stored` |
| Baseline vs stored DANTE-CCH selections (overlap, failures found, score match) | `python -m src.dante.compare_stored --builds subset` |
| Baselines on the same builds and budgets (ours vs stored) | `python -m src.eval.compare_baselines --builds subset` |
| APFDc of our ordering vs RQ1 apfdc column | `python -m src.eval.compare_baselines --apfdc` |
| End to end, one build | `python run_end_to_end.py --build PR-1840_build4 --budget 10` |
| End to end, phase-1 builds | `python run_end_to_end.py --subset --budget 5 10 20 --skip-existing` |
| Results table and `results/initial_results.csv` | `python -m src.eval.summarize` |
| Tests (no data or LLM needed) | `python -m pytest` |

`run_end_to_end.py --provider mock` runs without Ollama (fixed relevance 0.5).

## Methods compared

| Method | Ranking |
|---|---|
| Random (stored / ours) | random order, seed 42 |
| DANTE-CCH (stored) | selections stored in the DANTE package |
| DANTE-CCH-shipped | our port with relevance weight 0, which is what the shipped DANTE code computes (see limitations) |
| DANTE-CCH | our port with TF-IDF relevance on: `1.0*history + 0.5*tfidf^1.2`, times `max(failures,0.1)/duration` |
| History-only, TF-IDF-only | one signal alone |
| LLM-relevance | as DANTE-CCH, with the LLM's relevance (0..1) replacing TF-IDF for the shortlisted tests (top-10 by history and top-10 by TF-IDF); other tests get relevance 0; if any LLM call fails the build uses the DANTE-CCH ranking |

Metrics (`src/eval/metrics.py`): %DTC = failing test classes selected / failing
candidate classes; APFDc as in DANTE's `run_prioritization.py` over the full
ranking; SAPFDc = %DTC x APFDc of the selected tests in selection order;
SDS = distinct packages / selected tests.

## Folder map

```
config.yaml            paths, budgets, history windows, K, LLM model/URL/timeout
run_end_to_end.py      end-to-end workflow
src/contracts/         typed state and JSON schemas (docs/contracts.md)
src/agent/             LLM provider, semantic analyzer, shortlister, fallback router
src/tools/             history_retrieval, diff_reader, budget_tracker
src/data/              LRTS loader, chronological split, git sources, eval-build list
src/dante/             DANTE baseline port and comparison with stored results
src/eval/              metrics, stored results, baseline comparison, summary
data_eval/             evaluation build list (50 builds of experiments/RQ1/karaf.csv)
results/               initial_results.csv (other outputs are not committed)
docs/                  architecture, contracts, DANTE notes
tests/                 unit and end-to-end tests
```

## Known limitations

- Initial run: 13 builds, one project (karaf), one model. Means over so few builds
  are noisy; no statistical tests in Phase 1; no conclusion is drawn.
- 37 of the 50 evaluation builds change only file types DANTE ignores (`.xml`,
  `.properties`, ...), so relevance (TF-IDF or LLM) has no input there. The LLM run
  uses the 13 builds with code changes; results on them do not describe the other 37.
- In the shipped DANTE code, relevance is read under the key `"bm25"` but stored
  under `"tfidf"`, so the stored DANTE-CCH results appear to rank on history only. We report
  both the shipped behaviour and TF-IDF-on. Details: `docs/dante_notes.md`.
- In the shipped DANTE code, the sticky-failure window rolls over consecutive rows
  of all tests, not over each test's own history; we reproduce it as written.
- `last_outcome_n` is computed from all earlier LRTS builds; DANTE used only its
  processed builds (not in the package). Over the 50 builds our shipped-variant
  scores reproduce 79-81% of the stored scores of selected tests (per budget); the
  remaining selections differ for this reason. Median %DTC difference to the stored
  DANTE-CCH is 0.000 at 5, 10 and 20% (`python -m src.dante.compare_stored`).
- The LLM sees at most 3000 characters of diff and 3000 of test source; larger
  changes are truncated. Mean call latency on this laptop was 39.1 s.
- SAPFDc and SDS are named in the DANTE package but not implemented there; our
  definitions are stated above.
- The LLM gave a relevance of 0.2 or lower to 143 of the 152 tests it scored (94%); only 9 scored 0.8 or higher. It scored only the 13-20 shortlisted tests per build, so in this run LLM-relevance mostly follows the history ranking.

## Credits

- DANTE: "DANTE: Data-Driven Test Case Selection and Prioritization for
  Long-Running Test Suites", ICST 2026, and its replication package (MIT licence).
  The baseline in `src/dante/` is a port of that code; module docstrings cite the
  original functions.
- LRTS (Long Running Test Suites) dataset, https://ieeexplore.ieee.org/document/10044820.
- Apache Karaf, https://github.com/apache/karaf.
- R. Cheng, S. Wang, R. Jabbarvand and D. Marinov, "Revisiting test-case prioritization on long-running test suites", ISSTA 2024; artifact: https://doi.org/10.5281/zenodo.12662090.