# E2: DANTE reproduced by us vs the replication package (50 Phase 1 builds)

Written by `python -m src.eval.report`. From `results/E2_stored_phase1_seed1/per_build.csv` and `data_eval/eval_builds.csv` (`rq1_dante_cch_apfdc`). Rows marked "taken from the replication package" are the published reference; rows marked "reproduced by us" are our port. Tolerance 0.02 for APFDc, exact equality for %DTC.

| Metric | Budget | Method | Source | Builds | Median | Median diff vs reference | Within tolerance |
|---|---|---|---|---|---|---|---|
| APFDc (full ranking) | — | DANTE-CCH (replication package, RQ1 APFDc) | taken from the replication package | 50 | 0.7183 | — | — |
| APFDc (full ranking) | — | DANTE-CCH-shipped | reproduced by us | 50 | 0.7266 | 0.0000 | 39/50 |
| APFDc (full ranking) | — | DANTE-CCH | reproduced by us | 50 | 0.7218 | -0.0000 | 32/50 |
| %DTC | 5% | DANTE-CCH (stored) | taken from the replication package (stored selections; %DTC computed by our code) | 50 | 0.2917 | — | — |
| %DTC | 5% | DANTE-CCH-shipped | reproduced by us | 50 | 0.3333 | 0.0000 | 45/50 |
| %DTC | 5% | DANTE-CCH | reproduced by us | 50 | 0.3333 | 0.0000 | 45/50 |
| %DTC | 10% | DANTE-CCH (stored) | taken from the replication package (stored selections; %DTC computed by our code) | 50 | 0.3333 | — | — |
| %DTC | 10% | DANTE-CCH-shipped | reproduced by us | 50 | 0.3333 | 0.0000 | 45/50 |
| %DTC | 10% | DANTE-CCH | reproduced by us | 50 | 0.3667 | 0.0000 | 43/50 |
| %DTC | 20% | DANTE-CCH (stored) | taken from the replication package (stored selections; %DTC computed by our code) | 50 | 0.5000 | — | — |
| %DTC | 20% | DANTE-CCH-shipped | reproduced by us | 50 | 0.5000 | 0.0000 | 46/50 |
| %DTC | 20% | DANTE-CCH | reproduced by us | 50 | 0.5000 | 0.0000 | 43/50 |
