# Relevance key mismatch in the shipped DANTE: two DANTE variants

Date: 2026-10-20
Author: Ahmad Bilal (entry written by Muhammad Ali in P2-20 from `docs/dante_notes.md`)

## Observed failure or limitation

Our DANTE port with TF-IDF relevance on did not reproduce DANTE's stored scores. In the shipped code, `pipeline_orchestrator.py` stores relevance under the key `"tfidf"`, while `run_selection.py` and `run_prioritization.py` read it under `"bm25"`. The lookup returns 0, so the shipped DANTE-CCH ranks on history only, unlike the paper's description (`docs/dante_notes.md`, item 1).

## Change

Both behaviours are reported as separate methods:
- `DANTE-CCH-shipped`: relevance weight 0, as the shipped code behaves;
- `DANTE-CCH`: TF-IDF relevance on (`1.0·history + 0.5·relevance^1.2`), as the paper describes.

The gap comparisons use `DANTE-CCH` as the base method, and RQ1 also compares with `DANTE-CCH-shipped`.

## Measured effect

- **Phase 1 (13 builds with code changes):** the relevance-off scores reproduce the stored `value_score` of 82–86% of the stored selected tests, and the TF-IDF-on scores only 3–4% (`docs/dante_notes.md`, item 1; rerun with `python -m src.dante.compare_stored --builds subset`, which writes no file under `results/`).
- **Phase 2 test split:** the two variants rank differently. At the 10% budget, mean %DTC is 0.378 for `DANTE-CCH-shipped` and 0.356 for `DANTE-CCH`; mean SAPFDc is 0.264 and 0.274 (`results/tables/main_results.md`).
- **Phase 1 builds:** `DANTE-CCH-shipped` reproduces the replication package's APFDc with a median difference of 0.0000, within 0.02 on 39 of 50 builds (`results/tables/e2_reproduction.md`).
