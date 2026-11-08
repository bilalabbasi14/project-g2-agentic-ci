# Gap-resolution table

Written by `python -m src.eval.report`. "Addressed?" is set only by `resolve_gap`, which applies the rule fixed in `docs/PROJECT_CONTEXT.md` §8 before the results were seen:

- Gaps 1 and 3: **Fully** = the gap method beats every comparison method in its RQ on both %DTC and SAPFDc at the 10% budget, with Holm-corrected p < 0.05. **Partially** = it beats them on at least one metric or budget, or the improvement is not significant. **Not** = no improvement anywhere.
- Gap 2: **Fully** = both RQ2 conditions hold. **Partially** = one holds. **Not** = neither holds.

How the rule is applied: "beats" = a positive mean difference (gap method − comparison method) over the shared builds; "no improvement anywhere" = no positive mean difference against any comparison method at any metric and budget. RQ2 condition (a) holds when, at every budget, the mean decision + explanation time per build is below the mean test time saved per build; the number of builds where it holds is shown for reference. Condition (b) holds when at least 80% of the sampled justifications are rated sound.

| Gap | Method/component | Metric | Base paper result (DANTE-CCH, reproduced by us, at 10%) | Our result (at 10%) | Addressed? |
|---|---|---|---|---|---|
| Gap 1 | LLM-relevance (semantic analyzer) | %DTC, mean over builds | 0.356 | 0.447 (vs DANTE-CCH +0.091, p_Holm 0.0910; vs DANTE-CCH-shipped +0.068, p_Holm 0.0910) | Partially |
| Gap 1 | LLM-relevance (semantic analyzer) | SAPFDc, mean over builds | 0.274 | 0.287 (vs DANTE-CCH +0.013, p_Holm 0.2275; vs DANTE-CCH-shipped +0.023, p_Holm 0.4939) | Partially |
| Gap 2 | Full system (explainer) | Decision + explanation time vs test time saved, mean s per build | n/a (DANTE gives no explanations) | 86.4 s vs 1513.3 s saved; below on 43 of 44 builds | Partially |
| Gap 2 | Full system (explainer) | Share of the 100 sampled justifications rated sound (all budgets; RQ2 needs 0.80) | n/a (DANTE gives no explanations) | 0.640 (Cohen's kappa 0.705) | Partially |
| Gap 3 | Agent-weighted (orchestrator) | %DTC, mean over builds | 0.356 | 0.424 (vs DANTE-CCH +0.068, p_Holm 0.1665; vs Tuned-weight (LLM) -0.023, p_Holm 0.3173) | Partially |
| Gap 3 | Agent-weighted (orchestrator) | SAPFDc, mean over builds | 0.274 | 0.274 (vs DANTE-CCH -0.000, p_Holm 0.6764; vs Tuned-weight (LLM) -0.008, p_Holm 0.6784) | Partially |

- Gap 1 evidence: `results/stats/pairwise.csv` (family RQ1), `results/tables/gap1.md`, `results/tables/main_results.csv`.
- Gap 2 evidence: `results/tables/gap2.md` (from `results/E3_test_seed1/per_build.csv`), `results/gap2/rating_summary.csv`, `results/gap2/agreement.md`.
- Gap 3 evidence: `results/stats/pairwise.csv` (family RQ3), `results/tables/gap3.md`, `results/tables/gap3_w.md` (from `orchestrator_decisions.csv` of the test-split runs).
