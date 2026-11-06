# Project Context — G2-05 Phase 2

**Read this whole file before starting any task.** It explains what the project is, what already exists, what Phase 2 must deliver, and the rules everyone follows. A GitHub issue tells you *what to build*; this file tells you *why it exists and how it fits with everything else*. If an issue and this file disagree, stop and ask the issue's reviewer (Ali or Bilal) instead of guessing.

A copy of this file is kept in the repository at `docs/PROJECT_CONTEXT.md`. If the copy in the repo is newer than the one you were sent, the repo copy wins.

---

## 1. The project in plain words

| Item | Value |
|---|---|
| Course | AI4015 Agentic Artificial Intelligence, Fall 2026 |
| Project code | G2-05 |
| Title | Agentic Semantic Reasoning for Dynamic Test Selection in Long-Running CI Pipelines |
| Group | Ahmad Bilal (23I-0787, group head), Muhammad Ali (23I-2565), Taha Bashir (23I-0824) |
| Supervisor | Meemon Khan |
| Repository | https://github.com/bilalabbasi14/project-g2-agentic-ci (private) |
| Phase 2 deadline | **Sunday 8 November 2026, 11:55 PM Pakistan time (PKT)** |

**The problem.** Large software projects run thousands of automated tests every time code changes. This is called *continuous integration* (CI). For some projects a full test run takes hours. *Test selection* means picking a subset of tests to run within a time limit (a *budget*, for example "10% of the full test time") while still catching as many failing tests as possible.

**The base paper (DANTE).** DANTE is a published method for test selection. For every test class it combines two signals:

1. **History signal** — how often this test failed recently and whether it keeps failing ("stickiness").
2. **Relevance signal** — how textually similar the changed code is to the test's source code, measured with TF-IDF (a word-overlap technique).

It then ranks tests by a value score and picks tests in rank order until the time budget is used up. DANTE needs no training.

**Our idea.** We keep DANTE as the baseline and add an *agentic* layer built on a local large language model (LLM):

- **Gap 1 — semantic relevance.** Replace TF-IDF word-overlap relevance with an LLM's judgement of whether a test is likely to be affected by the change.
- **Gap 2 — explanations.** An LLM writes a short justification for important tests that were *skipped*, so a developer can understand why.
- **Gap 3 — per-commit weighting.** Instead of DANTE's fixed rule for combining history and relevance, an LLM agent looks at each change, uses tools to gather evidence, and chooses the weight between the two signals for that change.

**Phase 2's central question (from the course brief):** for each of the three gaps, did our system improve on the base paper, by how much, and why? Negative or partial results are acceptable **if reported honestly**. Hiding or inventing results is penalised.

---

## 2. Key terms (glossary)

| Term | Meaning in this project |
|---|---|
| **Build** | One CI run for one code change. Identified by a key like `PR-1840_build4`. |
| **Test class** | The unit we select (for example `org.apache.karaf.shell.SomeTest`). "Test" in this project always means a test class. |
| **Candidate** | A test class that DANTE can score: its source file was found and its duration is above 0. |
| **Failing test** | A test class with outcome 1 in that build. This is the ground truth. It is **never** given to any model as input. |
| **Budget** | A fraction of the build's total test time: 5%, 10% or 20%. Selection stops when the next test would exceed the budget (it is skipped and the scan continues). |
| **History score** | DANTE's history signal for one test (see §5.1). |
| **TF-IDF relevance** | DANTE's relevance signal, between 0 and 1. |
| **LLM relevance** | Our Gap 1 signal: a number between 0 and 1 returned by the LLM for one test. |
| **Shortlist** | The tests we send to the LLM: the top 10 by history score together with the top 10 by TF-IDF relevance (union, 13–20 tests). Tests not on the shortlist get LLM relevance 0. |
| **w (weight)** | The share given to history when combining signals: `base = w·History + (1−w)·Relevance^1.2`. DANTE's fixed rule is equivalent to **w = 2/3**. |
| **Fallback** | When an LLM call times out, returns invalid output or reports low confidence, the system uses the safe DANTE behaviour instead and logs a `FallbackRecord`. |
| **%DTC** | Share of the build's failing tests that the selection caught (0–1). Higher is better. |
| **APFDc** | How early failures appear in a full ordering of all tests, weighted by test duration (0–1). Higher is better. |
| **SAPFDc** | %DTC × APFDc computed on the selected tests in selection order. Rewards catching failures *and* running them early. |
| **SDS** | Distinct Java packages in the selection ÷ number of selected tests. A secondary diversity measure. |
| **Mock provider** | A fake LLM used in tests. It returns fixed answers instantly. **All automated tests must use it; tests must never need a real model or real data.** |
| **Dev split / test split** | The fixed division of evaluation builds. Dev builds are used for any tuning (prompts, weights). Test builds are used **only** for final reported results. |
| **Run** | One execution of the pipeline over a split with a given seed, for example `E3_test_seed1`. |
| **Trace** | The step-by-step log of what the agent did on one build: LLM calls, tool calls, decisions, fallbacks. |

---

## 3. What already exists (Phase 1, on `main`)

All of this works and has tests. **Do not rewrite it.** Phase 2 extends it.

| Path | What it does | Phase 1 owner |
|---|---|---|
| `config.yaml`, `src/settings.py` | All settings in one YAML file. `load_config()` reads it, or the file named in the environment variable `G2_CONFIG`. `repo_path()` turns repo-relative paths into absolute ones. | Ali |
| `src/data/loader.py` | `LRTSLoader` reads builds in time order: test results, durations, diff, test sources. `build(row)` returns a `BuildData`; `history(row, 100, 10)` returns a `HistoryData` with the 100 earlier builds. | Bilal |
| `src/data/splitter.py` | Guarantees history only uses builds strictly **before** the target build (no look-ahead). | Bilal |
| `src/data/sources.py` | Reads test source files at a build's commit from a git clone of Apache Karaf. | Bilal |
| `src/data/make_eval_builds.py` | Wrote `data_eval/eval_builds.csv`: the 50 Phase 1 evaluation builds. | Bilal |
| `src/dante/` | Our port of DANTE: `scores(build, history, cfg, method)` returns a pandas DataFrame with one row per candidate and columns `history_score`, `tfidf_relevance`, `relevance_used`, `base_score`, `total_failures`, `duration`, `actual_outcome`, `dante_cch_score`. `rank(...)` returns `(selected, ordered, df)`. Methods: `DANTE-CCH`, `DANTE-CCH-shipped`, `History-only`, `TF-IDF-only`, `Random`. | Bilal |
| `src/agent/llm_provider.py` | `OllamaProvider` (real model over HTTP) and `MockProvider` (fake). Each call is recorded as an `LLMCallRecord` with latency and token counts. | Ali |
| `src/agent/semantic_analyzer.py` | Builds the relevance prompt (anonymised, truncated diff and test source), calls the provider, validates the JSON answer. Raises `InvalidJSONError` / `SchemaViolationError`. | Ali |
| `src/agent/shortlister.py` | `shortlist(history_scores, tfidf_scores, k)` returns the union of the two top-k lists. | Ali |
| `src/agent/fallback_router.py` | Calls the analyzer for each shortlisted test; turns timeouts and bad output into `FallbackRecord`s; with `scope: build`, one failure makes the whole build use the DANTE ranking. | Ali |
| `src/tools/` | Three tools that read local files only: `history_retrieval(test)`, `diff_reader(file)`, `budget_tracker`. `TOOL_SPECS` describes them. | Ali |
| `src/contracts/` | Typed data structures (`models.py`) and JSON Schemas (`schemas.py`) with `validate(obj, name)`. | Ali |
| `src/eval/metrics.py` | `apfdc`, `dtc`, `sapfdc`, `sds`, `all_metrics`. | Taha |
| `src/eval/stored.py`, `src/eval/compare_baselines.py` | Load DANTE's stored results and compare our port with them. | Taha |
| `run_end_to_end.py` | Runs one build or the 13-build subset through the whole Phase 1 flow and writes `results/runs/<build>.json`. | Taha |
| `src/eval/summarize.py` | Aggregates run files into `results/initial_results.csv`. | Taha |
| `tests/` | 69 tests. All pass with `python -m pytest` and need **no data and no model**. | all |
| `docs/` | `architecture.md`, `contracts.md`, `dante_notes.md` (differences between DANTE's paper and its shipped code). | Bilal, Ali |

**Phase 1 findings everyone must know:**

1. In DANTE's shipped code, relevance is stored under the key `"tfidf"` but read under `"bm25"`, so the shipped DANTE effectively ranks on **history only**. We therefore report two DANTE variants: `DANTE-CCH` (TF-IDF on, as the paper describes) and `DANTE-CCH-shipped` (relevance weight 0, as the code behaves).
2. Our DANTE port reproduces the stored median APFDc (difference +0.0000, within 0.02 on 45 of 50 builds) and median %DTC (difference 0.000) on the 50 stored builds.
3. Only 13 of the 50 Phase 1 builds change code files. The other 37 change only file types DANTE ignores (`.xml`, `.properties`, ...), so relevance has nothing to work with there.
4. On a laptop CPU an LLM call took 39 s. On a free Kaggle T4 GPU it takes **about 3.4 s** (measured on 6 November 2026; the first call of a session takes about 95 s while the model loads).
5. In Phase 1 the LLM gave relevance ≤ 0.2 to 94% of the tests it scored, so LLM relevance barely changed the ranking. Phase 2 must address this (issue P2-07, prompt v2, tuned on the dev split only).

---

## 4. What Phase 2 must deliver

From the course brief (`AI4015_Agentic_AI_Semester_Project_Phase2.pdf`):

**Deliverable A — final source code (40 marks)**
- A complete end-to-end agentic pipeline on the full evaluation set.
- One clearly identifiable component per gap, each **switchable on and off** for ablation.
- Meaningful interaction with tools and data.
- Logged agent trajectories (reasoning steps, tool calls, inputs/outputs, state transitions).
- Robustness: failure handling, verification, retries, fallback.
- Evidence of iterative improvement: a development log (what failed, what changed, measured effect).
- README with overview, architecture diagram, installation, configuration and environment variables, how to run, how to reproduce each experiment, and the gap-resolution table.
- Scripts that reproduce experiments E1–E6 and save results to files.
- Traces or a representative sample of them.
- Tests for deterministic components; `requirements.txt`; `.env.example`; no secrets committed.
- Meaningful commits from all members throughout Phase 2.
- A GitHub release or tag named **`phase2-final`** before the deadline.

**Deliverable B — research paper (60 marks).** 8–10 pages, IEEE two-column, 25–30 references each with a DOI link, every number traceable to repository results. **The paper is written by the group members in their own words. AI tools must not write paper text.** Paper writing is not part of any coding issue.

**Deliverable C — Turnitin similarity and AI-writing reports for the paper.** Without them, nothing is marked.

---

## 5. The Phase 2 system

### 5.1 Scoring formulas (exact)

For each candidate test *t* in a build:

```
History(t)   = DANTE history score (THFR + sticky component), computed by src/dante (unchanged)
R(t)         = relevance used for t: TF-IDF relevance, LLM relevance, or 0 (depends on the method)
base_w(t)    = w · History(t) + (1 − w) · R(t) ** 1.2
value_w(t)   = base_w(t) · max(total failures of t in the history window, 0.1) / max(duration(t), 0.001)
```

Tests are ordered by `value_w` (highest first) and selected greedily within the budget.

**Why w = 2/3 is DANTE.** DANTE uses `1.0·History + 0.5·R^1.2`. Multiplying every test's base score by the same constant (1.5) does not change the order, so `w = 2/3` (with weights `w_history = 2/3`, `w_relevance = 1/3`) gives exactly the same ranking as DANTE. A unit test (P2-03) must prove this on a fixture.

In code, `w` is passed as `w_history = w` and `w_relevance = 1 − w` to `src.dante.scoring.score_table` (which already accepts both parameters).

### 5.2 Methods (the complete list)

Every method below is described by a **MethodSpec** (defined in P2-03) so the pipeline can run any combination from configuration. `experiments/methods.yaml` (P2-15) holds the list.

| Method name (exact string) | Relevance source | How w is chosen | Explainer | Role |
|---|---|---|---|---|
| `Random` | none | – (random order, seed 42) | off | Lower bound (E1) |
| `History-only` | none | rank by history score only | off | Single signal (E1) |
| `TF-IDF-only` | tfidf | rank by TF-IDF relevance only | off | Single signal (E1) |
| `DANTE-CCH-shipped` | tfidf | w = 1 (relevance weight 0) | off | Base paper as shipped (E2) |
| `DANTE-CCH` | tfidf | fixed w = 2/3 | off | Base paper as described (E2) |
| `DANTE-CCH (stored)` | – | – (read from DANTE's stored files, 50 builds only) | off | Published reference (E2) |
| `Tuned-weight (TF-IDF)` | tfidf | fixed w* tuned on dev split | off | Non-agentic baseline (E1, H-A) |
| `Single-call LLM` | llm_single_call | fixed w = 2/3 | off | Non-agentic LLM baseline (E1, H-B) |
| `LLM-relevance` | llm_shortlist | fixed w = 2/3 | off | **Gap 1 component** (E4) |
| `Tuned-weight (LLM)` | llm_shortlist | fixed w* tuned on dev split | off | Gap 3 comparison (E4) |
| `Agent-weighted` | llm_shortlist | **orchestrator chooses w per build** | off | **Gap 3 component** (E4) |
| `Full system` | llm_shortlist | orchestrator | **on** | Complete agentic system (E3); explainer = **Gap 2 component** |
| `Agent-weighted (TF-IDF)` | tfidf | orchestrator | off | Ablation: full system without LLM relevance (E5) |
| `Full system (no shortlist)` | llm_all_individual | orchestrator | off | Ablation: LLM scores every candidate (E5, 20-build sample, seed 1) |

Relevance sources:
- `none` — R = 0 for all tests.
- `tfidf` — DANTE's TF-IDF relevance.
- `llm_shortlist` — the semantic analyzer scores each shortlisted test with one call; others get 0.
- `llm_all_individual` — the semantic analyzer scores **every** candidate (expensive; ablation only).
- `llm_single_call` — one single LLM call per build that receives the diff and the list of all candidate test names and returns a relevance for each (P2-17). No tools, no shortlist, no loop. This is the "non-agentic single LLM call" baseline promised in Phase 1.

**The ablations follow from the table:** Full system − orchestrator = `LLM-relevance` (+explainer); − LLM relevance = `Agent-weighted (TF-IDF)`; − explainer = `Agent-weighted`; − shortlist = `Full system (no shortlist)`. The explainer never changes the selection, so removing it changes only cost and latency.

### 5.3 Per-build flow of the full system

1. **Load** the build (test results, durations, diff, test sources) and its history (100 earlier builds). Ground-truth outcomes are kept aside for scoring only.
2. **DANTE scores** — history score and TF-IDF relevance for every candidate.
3. **Shortlist** — top 10 by history ∪ top 10 by TF-IDF.
4. **Gap 1: semantic analyzer** — one LLM call per shortlisted test → relevance 0–1, a reason and a confidence. Goes through the fallback router.
5. **Gap 3: orchestrator** — receives build features and the shortlist with all scores. In a loop of at most 4 tool calls, it may call `history_retrieval` or `diff_reader` to inspect evidence, then must answer with `{w, confidence, reason}`. Invalid output is retried once. If it still fails, or confidence < 0.3, w falls back to 2/3 (DANTE) and a `FallbackRecord` is logged.
6. **Rank and select** with the chosen w for each budget (5%, 10%, 20%).
7. **Gap 2: explainer** — for each budget, picks up to 5 skipped tests that ranked highly by history or relevance, gives the LLM the evidence (history statistics, relevance and the analyzer's reason, changed files, why the budget excluded the test) and gets back a short justification plus the list of facts it relied on.
8. **Metrics** against the real outcomes; **costs** (latency, tokens, tool calls, fallbacks) and **time saved** (`total suite time − selected time`).
9. **Trace** — every step above is written to the trace file for the build.

### 5.4 Robustness rules (apply everywhere)

- Every LLM output is validated against a JSON Schema before use.
- Retry an invalid or timed-out call **once**. After that, fall back and log a `FallbackRecord` with one of the reasons `timeout`, `invalid_json`, `schema_violation`, `low_confidence`, `provider_error`.
- Relevance (Gap 1) fallback scope is `build` (as in Phase 1): one failed relevance call makes that build use DANTE's ranking.
- Orchestrator (Gap 3) fallback: w = 2/3.
- Explainer (Gap 2) failure: that one explanation is marked failed; selection is not affected.

---

## 6. Data

### 6.1 Sources

| Data | Where it comes from | What it is used for |
|---|---|---|
| LRTS dataset, Karaf project | `long_running_test_suites.zip` | `dataset.csv` (build list and commit SHAs), `processed_test_result/karaf/...` (per-build test outcomes and durations), `shadata/karaf/diff/...` (per-build diffs) |
| DANTE replication package | `ML_TCSP.zip` | `experiments/RQ1/*.csv` (stored APFDc) and stored DANTE-CCH / Random selections for 50 Karaf builds |
| Apache Karaf git repository | `https://github.com/apache/karaf.git` (blob-less clone) | Test source files at each build's commit |

**Data is never committed to git.** It is shared as a **private Kaggle dataset** owned by Ali, with Bilal and Taha added as collaborators (P2-02). Everyone downloads it from there. The test-source text needed by the LLM is precomputed into a **source cache** (P2-09), so Kaggle runs do not need a git clone.

### 6.2 Evaluation set and fixed split (P2-08)

- **Pool:** all 726 Karaf builds in LRTS.
- **A build qualifies if:** it has at least 100 earlier builds (full history window); its diff changes at least one code file DANTE keeps; it has at least one failing candidate test; and its test sources can be read.
- **Selection:** all qualifying builds (54 at the time of writing): **split chronologically**, the earliest 10 are `dev`, the remaining 44 are `test`. The rule was fixed before any results were seen. (Only if more than 160 builds qualified would 160 be pre-selected evenly spaced in time before the source check; with 54 this does not apply.) The group chose this over loosening the filters on 6 November 2026; see `docs/devlog/2026-11-06-ali-eval-set-size.md`.
- **The file `data_eval/eval_builds_p2.csv` is the single source of truth.** Nobody edits it by hand after it is merged.
- The 50 Phase 1 builds stay in `data_eval/eval_builds.csv` and are still used for the stored-DANTE comparison (E2).

### 6.3 Leakage rules — break any of these and results are invalid

1. History for build *n* uses only builds before *n* (already enforced by `splitter.py`; keep it that way).
2. A build's own outcomes are used **only** to compute metrics, never as model input.
3. **Prompts, thresholds, weights and any design choice are tuned on the `dev` split only.** Nobody looks at `test`-split results until the final runs.
4. Prompts are anonymised: commit hashes, authors, emails and timestamps removed (`semantic_analyzer.anonymise`). Reuse that function for every new prompt.
5. The model has no web access during inference.
6. Possible memorisation (the LLM mentioning things not in its prompt) is checked in the failure analysis (P2-14) and reported as a threat to validity.

---

## 7. Model and compute

| Setting | Value |
|---|---|
| Model | `qwen2.5-coder:7b`, served by **Ollama** |
| Where real runs happen | **Kaggle notebooks**, free tier, GPU T4 ×2, Internet on |
| Python on Kaggle | Kaggle ships Python 3.13, but our pinned `numpy==1.26.4` needs ≤ 3.12. The notebook creates a **Python 3.12 environment with `uv`** (P2-16). |
| Temperature | 0.0 |
| JSON mode | on |
| Timeout | 60 s per call; one retry |
| Max diff / test source per call | 3,000 characters each |
| Seeds | 1, 2, 3 for repeated runs (passed to Ollama as `seed`) |
| Cache | Every LLM answer is cached on disk, keyed by model + prompt + options + seed (P2-04). Reruns and ablations with the same seed reuse cached answers. Cached entries keep the original latency and token counts, so cost numbers stay real. |
| Two GPUs | Run two Ollama servers (one per GPU, ports 11434 and 11435) and split builds between two processes with `--shard 0/2` and `--shard 1/2` (P2-04, P2-16). |
| Kaggle quota | About 30 GPU hours per account per week; a session runs at most 12 hours. Use **Save Version → Save & Run All (Commit)** for long runs. Runs are resumable (`--skip-existing`). |
| Estimated cost | Full system ≈ 20 LLM calls per build ≈ 70 s per build ≈ 2 h per 100 builds per seed on one GPU. Total evaluation ≈ 10–12 GPU hours, split across three accounts. |
| Monetary cost | $0 (local open model on free GPUs). Report GPU-hours instead. |

**Local development never needs a GPU or the data.** Code is written and tested on each member's laptop with the mock provider and small fixtures. Only the real experiment runs happen on Kaggle.

---

## 8. Experiments (E1–E6)

All final results use the **test split** (all test-split builds, 44), budgets 5/10/20%, and seeds 1–3 unless stated otherwise. Results for each build and seed are stored, then averaged over seeds per build before statistics.

| ID | What it shows | Methods | Notes |
|---|---|---|---|
| **E1** Baselines | Non-agentic baselines | `Random`, `History-only`, `TF-IDF-only`, `Tuned-weight (TF-IDF)`, `Single-call LLM` | Single-call LLM runs seed 1–3 |
| **E2** Base paper | DANTE reproduced and compared with stored outputs | `DANTE-CCH`, `DANTE-CCH-shipped` on the test split; plus `DANTE-CCH (stored)` vs our port on the 50 Phase 1 builds | State clearly which numbers we reproduced and which come from the paper |
| **E3** Proposed system | Full agentic system | `Full system` | Explainer only on seed 1 (it does not affect selection); seeds 2–3 run with the explainer off |
| **E4** Gap-wise | One experiment per gap | Gap 1: `LLM-relevance` vs `DANTE-CCH` and `DANTE-CCH-shipped`. Gap 2: explainer cost vs time saved, plus 100 rated explanations. Gap 3: `Agent-weighted` vs `DANTE-CCH` vs `Tuned-weight (LLM)` | RQ1–RQ3 below |
| **E5** Ablations | Contribution of each component | `LLM-relevance`, `Agent-weighted (TF-IDF)`, `Agent-weighted`, `Full system (no shortlist)` compared with `Full system` | No-shortlist ablation: 20 test builds, seed 1 (compute limit; stated in the paper) |
| **E6** Efficiency and reliability | Cost and robustness | All LLM methods | Latency per build, LLM calls, tokens, tool calls, fallback rate, time saved vs overhead, GPU-hours |

**Research questions and success criteria (fixed in Phase 1, do not change):**

| RQ | Gap | Supported if | Weakened if |
|---|---|---|---|
| RQ1 | 1 | LLM relevance raises %DTC and SAPFDc over DANTE at the same budgets | No significant or only negligible effect, or added cost outweighs the gain |
| RQ2 | 2 | Decision + explanation time stays below the test time saved, **and** ≥ 80% of sampled justifications are rated sound | Overhead above time saved, or many unsound justifications |
| RQ3 | 3 | Agent-weighted ranking has higher %DTC and SAPFDc than both DANTE's fixed combination and the tuned fixed weight | No difference from the tuned weight, or worse |

**Statistics (P2-13):** paired comparisons on the same builds. Friedman test across methods, then pairwise Wilcoxon signed-rank tests with Holm correction at α = 0.05, and an effect size (matched-pairs rank-biserial correlation). Reported per budget and per metric. Phase 1 promised "overall and per project"; Phase 2 uses one project (Karaf), which is recorded in "Changes since Phase 1".

**Explanation rating (P2-18, P2-24, P2-25):** 100 explanations sampled from the test split (seed 1), stratified by budget. Ali and Bilal each rate every one independently (Taha built the explainer, so he does not rate) as *sound*, *partly sound* or *unsound*, using this rule: **sound** = every factual statement is supported by the evidence the explainer was given, *and* the stated reason for skipping follows from that evidence. Cohen's kappa is reported for agreement before disagreements are resolved by discussion.

**Gap-resolution table rule (P2-19)** — decided now so nobody chooses the label after seeing the numbers:
- Gaps 1 and 3: **Fully** = the gap method beats every comparison method in its RQ on both %DTC and SAPFDc at the 10% budget, with Holm-corrected p < 0.05. **Partially** = it beats them on at least one metric or budget, or the improvement is not significant. **Not** = no improvement anywhere.
- Gap 2: **Fully** = both RQ2 conditions hold. **Partially** = one holds. **Not** = neither holds.

---

## 9. Repository layout after Phase 2

New or changed paths are marked ★. **Owner** = who is responsible for changes to that file during Phase 2. Do not edit a file owned by someone else unless your issue explicitly says so; otherwise ask them first.

```
.github/workflows/tests.yml        ★ CI: runs pytest on every PR                     Ali
.github/pull_request_template.md   ★ PR checklist                                     Ali
.githooks/pre-push                 ★ blocks direct pushes to main                     Ali
.env.example                       ★ environment variables (no real values)           Ali
CLAUDE.md                          ★ review rules for Claude Code reviewers           Ali
config.yaml                        Phase 2 keys added once in P2-03                   Ali (others: request changes in your PR description)
config_kaggle.yaml                 ★ same keys, Kaggle paths                          Ali
requirements.txt                   Phase 2 additions in P2-03 only                    Ali
src/contracts/                     Phase 2 structures added in P2-03                  Ali
src/agent/llm_provider.py          cache, seed, server selection                      Ali
src/agent/llm_cache.py             ★ on-disk LLM answer cache                         Ali
src/agent/semantic_analyzer.py     prompt v2                                          Ali
src/agent/orchestrator.py          ★ Gap 3 component                                  Ali
src/agent/single_call.py           ★ single-call LLM baseline                         Taha
src/agent/explainer.py             ★ Gap 2 component                                  Taha
src/tools/registry.py              ★ tool registry used by the orchestrator           Ali
src/obs/trace.py                   ★ trace logger                                     Ali
src/data/make_eval_set_p2.py       ★ evaluation set + split                           Ali
src/data/source_cache.py           ★ precomputed test sources                         Ali
src/data/loader.py                 reads the source cache when present                Bilal (P2-09 may change it as its issue specifies)
src/dante/                         unchanged except tuning helper                     Bilal
src/dante/tune_weight.py           ★ tuned-weight grid search                         Bilal
src/pipeline.py                    ★ runs any set of methods on one build             Ali
run_end_to_end.py                  thin wrapper around src/pipeline.py                Ali
experiments/                       ★ methods.yaml, E1–E6 configs, run_experiment.py, merge_shards.py, kaggle_runner.ipynb   Ali
experiments/tuned_weights.yaml     ★ output of tuning                                 Bilal
src/eval/stats.py                  ★ Friedman/Wilcoxon/Holm/effect size               Taha (Bilal runs it on the real results)
src/eval/shortlist_recall.py       ★                                                  Bilal
src/eval/failure_analysis.py       ★                                                  Bilal
src/eval/rating.py                 ★ rating sheets + Cohen's kappa                    Taha
src/eval/report.py                 ★ tables, figures, gap-resolution table            Bilal
data_eval/eval_builds_p2.csv       ★ fixed evaluation set and split                   Ali
results/<experiment>/...           ★ per-build and summary CSVs (committed)           whoever ran it
results/figures/, results/tables/  ★ written by P2-19                                 Bilal
logs_sample/                       ★ representative traces (committed)                whoever ran it
docs/PROJECT_CONTEXT.md            ★ this file                                        Ali
docs/devlog/                       ★ one Markdown file per devlog entry               everyone
docs/cases/                        ★ representative success/failure cases            Bilal
README.md                          final rewrite in P2-20                             Ali (others: put README text in your PR description; Ali merges it in)
```

**Files every run produces** (defined exactly in P2-15; other issues read them, so names and columns must not change). Each run is written to `results/<run_id>/`, where `run_id` looks like `E3_test_seed1`:

| File | One row per | Committed? |
|---|---|---|
| `per_build.csv` | build × method × budget: metrics, costs, the w used, the ranking source | yes |
| `llm_relevance.csv` | build × test scored by the LLM: relevance, confidence, reason, prompt version | yes |
| `orchestrator_decisions.csv` | build × relevance source: w, confidence, steps, tool calls, fallback reason | yes |
| `explanations.csv` | explanation: build, budget, test, justification, cited facts, evidence | yes |
| `run_meta.json` | run: git commit, model, prompt versions, split, seed, timings, failed builds | yes |
| `runs/<build>.json` | build: everything above in full | **no** (too large) |

**Phase 2 configuration sections** (added once in P2-03): `eval`, `llm_p2`, `orchestrator`, `explainer`, `single_call`, `tuning`, `ablation`, `trace`, `paths_p2`. Phase 1 sections keep their meaning.

**What is committed vs. not:**
- Committed: code, tests, configs, `data_eval/*.csv`, `results/**/*.csv`, `results/**/*.md`, `results/figures/*.png`, `logs_sample/**`, docs.
- Never committed: raw data, the source cache, the LLM cache (`cache/`), full run JSONs (`results/**/runs/`), full logs (`logs/`), `.env`, tokens or keys of any kind.

---

## 10. Conventions

- **Python 3.12.** Install with `python -m pip install -r requirements.txt`.
- **Configuration:** every tunable number lives in `config.yaml`. No magic numbers in code. Read config through `src.settings.load_config()`.
- **Paths:** never hard-code `C:/...` or `/kaggle/...` in code. Use config paths and `repo_path()`.
- **Data structures:** anything passed between components or written to JSON is a dataclass in `src/contracts/models.py` with a JSON Schema in `src/contracts/schemas.py`, and is validated with `validate(obj, name)`.
- **LLM calls:** always through a provider object (`OllamaProvider` or `MockProvider`), never with `requests` directly. Every new prompt has a version string (for example `PROMPT_VERSION = "v2"`) that is stored in results.
- **Logging:** use Python `logging` (`log = logging.getLogger(__name__)`), never `print` inside library code. Agent steps go to the trace logger (P2-05).
- **Tests:** every new deterministic function gets a test in `tests/`. Tests use `MockProvider` and tiny in-memory fixtures (see `tests/test_end_to_end.py` for the pattern). Tests must pass on a machine with **no data, no git clone and no model**. Run `python -m pytest` before every push.
- **Style:** small functions with docstrings explaining what and why; type hints on public functions; no unused code; no commented-out blocks.
- **Results numbers:** every number in the README or the paper must come from a file under `results/` that a script in the repo produces. Never type a result by hand.

---

## 11. Git and pull-request workflow (mandatory)

1. **One-time setup on each laptop.**
   - Install Git and the GitHub CLI (`gh`, from https://cli.github.com).
   - Sign in with **your own** GitHub account: run `gh auth login`, then choose *GitHub.com* → *HTTPS* → *Login with a web browser*. This needs no token. (The repo belongs to Bilal's personal account. GitHub's fine-grained tokens do not work for collaborators on another person's personal repo, so browser login is the simplest correct option.)
   - Clone the repo and set your identity inside it:
     ```
     gh repo clone bilalabbasi14/project-g2-agentic-ci
     cd project-g2-agentic-ci
     git config user.name  "<your real name>"
     git config user.email "<the email of your GitHub account>"
     git config core.hooksPath .githooks
     git config core.longpaths true
     ```
   - Never use another member's login or token: whoever is logged in is shown as the author of the push and the PR.
   - A token is needed only inside Kaggle notebooks, to clone the private repo. There, use a **classic** personal access token with the `repo` scope and a 7-day expiry, stored as a Kaggle Secret named `GITHUB_TOKEN`. Never paste it into a notebook cell or a file.
2. **Never commit or push to `main`.** The pre-push hook blocks it; do not bypass it (no `--no-verify`).
3. **One issue = one branch = one PR.** Branch name: `p2-<NN>-<short-name>`, for example `p2-06-orchestrator`.
4. Start from an up-to-date `main`:
   ```
   git checkout main
   git pull
   git checkout -b p2-06-orchestrator
   ```
5. Commit in small, meaningful steps. A commit message is one short summary line in the imperative ("Add orchestrator tool loop"), then a blank line and a few lines on what and why. **Commit messages and PR descriptions must not contain `Co-authored-by` lines or "Generated with ..." lines.**
6. Before opening the PR: `git fetch origin`, then `git rebase origin/main` (or merge `main` into your branch) and fix any conflicts; run `python -m pytest`; all tests must pass.
7. Push the branch: `git push -u origin p2-06-orchestrator`.
8. Open a PR into `main`. The title is `[P2-06] <issue title>`. The description follows the template: `Closes #<issue number>`, what changed, how it was tested, the acceptance criteria ticked one by one, known limitations, and a devlog entry if the issue asks for one.
9. A reviewer (Ali or Bilal; never the author) reviews. **The reviewer who approves the PR merges it** (Ali or Bilal; nobody merges their own PR), only when the user explicitly says "merge PR #N", only if the user is not the PR's author, and only after an approval from someone other than the author and green CI.
10. After the merge: `git checkout main`, then `git pull`, then delete your local branch.

---

## 12. Scope discipline

- Do exactly what your issue says. If you find something missing, wrong or unclear, **do not silently expand your task.** Write it in the PR description under "Problems found", or comment on the issue, and suggest a new issue. A new issue is created only after Ali approves.
- Do not change another member's files unless your issue says so. If you must, explain why in the PR and tag the owner.
- If a dependency (an issue you rely on) is not merged yet, either work against the interface defined in P2-03 using a fake, or wait. Do not copy someone else's unmerged code into your branch.
- If you cannot meet an acceptance criterion, say so in the PR. Do not tick a box that is not true.

---

## 13. Work order (stages)

Taha travels on 7 November, so his four code issues come first; Ali then finishes his open PRs and Kaggle steps and does the runs; Bilal follows. The rows below run one after another, top to bottom, and within a row in the order listed; rows for different members in the same step can run in parallel. **Every issue comes after all issues in its "Depends on" line** (checked issue by issue). Where an issue depends on unmerged work by the same member, its branch is stacked on that work and its PR says "Stacked on #<PR>; merge after it."

| Step | Who | Issues, in order | Reviews and merges |
|---|---|---|---|
| Done | Ali | #1 P2-01, #2 P2-02, #3 P2-03, #4 P2-04, #5 P2-05, #8 P2-08 merged | Bilal |
| **1. Taha** | Taha | #10 P2-10, #17 P2-17, #18 P2-18 (the tool; Ali generates the sheets after R1), #13 P2-13 (code on fake data; Bilal runs it on the real results) | Ali or Bilal |
| **1. Ali** | Ali | review fixes on his open PRs (#6, #15, #9, #16, #7) and their Kaggle steps (source cache, runner check, dev prompt comparison) | Bilal |
| **2. Bilal** | Bilal | #11 P2-11 (LLM part after #7's dev run), #12 P2-12 | Ali |
| **3. Runs** | Ali, Bilal | Ali: #21 P2-21 (R1), then #23 P2-23 (R3). Bilal: #22 P2-22 (R2) | the other member |
| **4. Ratings** | Ali, Bilal | Ali generates the sheets (#18) and rates #24 P2-24; Bilal rates #25 P2-25 | the other member |
| **5. Analysis** | Bilal | statistics (#13) on the real results, #19 P2-19, #14 P2-14 | Ali |
| **6. README** | Ali | #20 P2-20 | Bilal |
| **7. Final** | everyone | paper (written by the members, not AI): #27 (Ali), #28 (Bilal), #29 (Taha); release #26 P2-26 (Bilal) last | — |

Submission deadline is unchanged: Sun 8 Nov, Bilal submits before 23:55 PKT.

---

## 14. Who does what (summary)

| Member | Code issues | Runs and human tasks | Paper sections (written by the member) |
|---|---|---|---|
| **Muhammad Ali** | P2-01 CI and rules · P2-02 data sharing · P2-03 contracts and config · P2-04 LLM cache, seeds, servers · P2-05 trace logger · P2-06 orchestrator (Gap 3) · P2-15 pipeline with method specs · P2-08 evaluation set and split · P2-09 source cache · P2-16 experiment runner and Kaggle notebook · P2-07 relevance prompt v2 · P2-20 README and devlog (all reviewed by Bilal) | P2-21 Kaggle run R1 (E3, E4 Gaps 1 and 3) · P2-23 Kaggle run R3 (E5, E6) · generating the rating sheets (P2-18) · P2-24 rate 100 explanations | Proposed System/Methodology, Efficiency analysis |
| **Ahmad Bilal** | P2-11 tuned-weight baselines · P2-12 shortlist recall · P2-19 tables, figures, gap table · P2-14 failure analysis (all reviewed by Ali) | P2-22 Kaggle run R2 (E1, E2, Gap 2 run) · running the statistics (P2-13) on the real results · P2-25 rate 100 explanations · P2-26 release and submission | Problem Formulation, Experimental Setup, Related Work, Failure Analysis |
| **Taha Bashir** | P2-10 explainer (Gap 2) · P2-17 single-call baseline · P2-18 rating tool and kappa · P2-13 statistics code (all reviewed by Ali or Bilal) | — | Evaluation Methodology, Results, Ablation, Limitations |

Abstract, Introduction and Conclusion are written together at the end.
