# Evaluation set size: all qualifying builds, 10 dev / 44 test

Date: 2026-11-06
Author: Muhammad Ali

## Observed failure or limitation

The planned Phase 2 evaluation set was 120 builds (20 dev + 100 test), with a rule to stop if fewer than 60 builds qualify (P2-08, PROJECT_CONTEXT §6.2). Applying the fixed filters to the 726 Karaf builds in LRTS left only 54 qualifying builds. Source: `data_eval/eval_set_p2_report.md`, written by `src/data/make_eval_set_p2.py`.
- 626 have at least 100 earlier builds (F1).
- 199 of those change at least one code file (F2).
- 54 of those have a failing test class (F3).
- All 54 have a failing candidate with readable source (F4).

So the 60-build minimum stopped the script before any CSV was written.

The binding constraint is "changes code **and** has a failing test", not the history window. We counted the builds that pass F2 and F3 under shorter history requirements: 57 with at least 50 earlier builds, 60 with at least 10, and 65 with none. These counts were checked before any method was run on these builds.

## Change

Group decision (6 November 2026, option 1 of three): **use every build that passes F1–F4**, with no 60-build minimum and no 120-build target, and keep the chronological split.
- The earliest 10 builds are `dev` and the remaining 44 are `test`. Dev builds date from 2021-05-04 to 2021-06-15, test builds from 2021-08-30 to 2024-04-06.
- The even-spacing pre-selection to 160 builds stays in the script, but applies only when more than 160 builds qualify; with 54 it does not.
- `--n-dev` defaults to 10.
- The rule was fixed before any results were seen, and the script reads no method results.

Changed: `src/data/make_eval_set_p2.py`, `tests/test_eval_set_p2.py` and `docs/PROJECT_CONTEXT.md` §6.2 and §8. The issue bodies that mentioned 100 test builds or 120 builds now say "all test-split builds (44)".

**Why not the other options:**
- **Shorter history window (option 2).** Lowering F1 to 10 earlier builds reaches exactly 60, but it weakens the history signal: DANTE's history score assumes a 100-build window, so the earliest builds would be scored with almost no history, unlike the rest.
- **Dropping the code-change filter (option 3).** This adds builds whose diff touches only file types DANTE ignores. In those builds TF-IDF and LLM relevance have no input, so Gaps 1 and 3 cannot change anything there; the Phase 1 finding was that 37 of 50 builds were of this kind.

## Measured effect

- **Evaluation set:** 54 builds instead of the planned 120 (`data_eval/eval_builds_p2.csv`). The paper's experimental setup and threats to validity must state the smaller test split (44 builds) and the reason.
- **Tuning data:** the dev split for prompt and weight tuning is 10 builds.
- **Phase 1 overlap:** 1 dev build and 10 test builds are also Phase 1 builds (`in_phase1`).
