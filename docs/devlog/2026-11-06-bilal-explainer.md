# Explainer: explain only important skipped tests, with cited evidence

Date: 2026-11-06
Author: Taha Bashir

## Observed failure or limitation

Gap 2 says explanations for test selection have only been shown on a small synthetic system. RQ2 (docs/PROJECT_CONTEXT.md §8) is supported only if (a) the decision and explanation time stays below the test time saved, and (b) at least 80% of 100 sampled justifications are rated *sound*: every factual statement is supported by the evidence the explainer was given, and the reason for skipping follows from that evidence. An explainer that writes free text about every skipped test would fail both conditions: a Karaf build has hundreds of skipped candidates (one LLM call each is far too slow), and an LLM asked to "explain" without fixed evidence tends to add facts it was never given, which a rater must mark unsound.

## Change

`src/agent/explainer.py` (prompt version `e1`):

- **Only important skipped tests.** `select_skipped` keeps skipped tests that are among the top 20 candidates by history score or by relevance (`explainer.candidate_pool`), in ranking order, at most 5 per build and budget (`explainer.top_n_skipped`). These are the skips a developer would question; a test with no failures and no relevance needs no explanation. This bounds the cost to at most 5 calls (10 with retries) per build and budget, independent of the suite size.
- **Fixed evidence, cited.** `build_evidence` gives the model a small JSON object: history statistics from the `history_retrieval` tool, the history score and relevance used, the semantic analyzer's reason, the changed files, and why the budget excluded the test (budget left when the greedy scan reached it, and the budget at which it would have fitted). The prompt says to use only these facts and to copy the facts it used into `cited_facts`. The evidence is stored with every `ExplanationRecord`, so raters judge each justification against exactly what the model saw.
- **Validation and retry.** Answers are validated against `explanation_response` (at most 400 characters, 1–6 cited facts, the right test name) and retried once; a second failure gives `ok=False` with the reason, and selection is never affected.
- **Grounding check.** `grounding_report` checks automatically that the numbers and file names in each cited fact appear in the evidence. It is reported next to the human rating and does not replace it.
- The explainer never reads the target build's outcomes; a test runs it with opposite outcome columns and with no outcome column and gets identical prompts and evidence.

## Measured effect

To be measured in P2-21 (R1, `Full system`, seed 1): explainer calls, latency and success rate from `per_build.csv` (`explainer_calls`, `explainer_latency_s`, `explainer_ok`) against `time_saved_s`, and the share rated sound in P2-24/P2-25 (`results/gap2/rating_summary.md`).
