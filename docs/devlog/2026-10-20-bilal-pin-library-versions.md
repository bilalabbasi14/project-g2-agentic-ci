# Tie order depended on library versions: numpy, pandas and scikit-learn pinned

Date: 2026-10-20
Author: Ahmad Bilal (entry written by Muhammad Ali in P2-20 from `docs/dante_notes.md`)

## Observed failure or limitation

Many Karaf tests get the same DANTE score (often 0), and their order comes from pandas' unstable sort. When our DANTE port was first compared with DANTE's stored selections, using numpy 2.5 and pandas 3.0, only 3 of the 50 Phase 1 builds matched the stored 5% selection (`docs/dante_notes.md`, "Known limitations of the shipped code", item 4).

## Change

`requirements.txt` pins the versions of the DANTE package's lock file: numpy 1.26.4, pandas 2.3.2 and scikit-learn 1.7.2. The README tells users to install exactly these.

## Measured effect

- With the pinned versions, 26 of the 50 builds match the stored 5% selection (`docs/dante_notes.md`, item 4; rerun with `python -m src.dante.compare_stored`). That command prints its comparison and writes no file under `results/`, so the 3 → 26 change is recorded only in `docs/dante_notes.md`.
- **Still platform-dependent:** while reviewing run R2 (#70), the non-LLM methods were rerun on a Windows laptop with the same pinned versions. History-only, TF-IDF-only, Tuned-weight (TF-IDF), DANTE-CCH and DANTE-CCH-shipped gave a different tie order than on Kaggle (Linux), with the same candidates, failing tests and durations; Random matched. The local rerun was not committed. All reported results come from Kaggle, where R1, R2 and R3 agree with each other.
