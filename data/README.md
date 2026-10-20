# Data

No dataset files are committed. Everything lives outside the repo; paths are set in `config.yaml`.

## Sources

| What | Where to get it | Used for |
|---|---|---|
| LRTS processed dataset (`long_running_test_suites.zip`) | LRTS (Long Running Test Suites) dataset, linked from the DANTE readme: https://ieeexplore.ieee.org/document/10044820 | build metadata, per-build test results, per-build diffs |
| DANTE replication package (`ML_TCSP.zip`) | DANTE (ICST 2026) replication package | reference code, RQ1 APFDc CSVs, stored selection JSONs |
| Apache Karaf git repository | https://github.com/apache/karaf.git | test-class sources at each build commit |

## What to extract (only these parts)

Use Python's `zipfile`; extract to short paths (Windows 260-char limit).

From `long_running_test_suites.zip` to `C:/g2w/lrts/` (`paths.lrts_root`):
- `long_running_test_suites/dataset.csv`
- `long_running_test_suites/processed_test_result/karaf/`
- `long_running_test_suites/shadata/karaf/`

Resulting layout (no `artifact/` folder, unlike the path in DANTE's `run_selection.py`):

```
lrts/dataset.csv
lrts/processed_test_result/karaf/<pr_name>_build<id>/stage_<stage>/test_class.csv.zip
lrts/shadata/karaf/diff/<pr_name>_build<id>.diff
```

From `ML_TCSP.zip` to `C:/g2w/dante/` (`paths.dante_root`):
- `ML_TCSP/src/*.py`, `ML_TCSP/src/readme.md` -> `dante/src/`
- `ML_TCSP/experiments/RQ1/*.csv` -> `dante/experiments/RQ1/`
- for karaf, `experiments/RQ2 and RQ3/karaf_20251222-171436/Budget_{05,10,20}_Percent/<build>/solution_classical_{DANTE-CCH,Random}_<build>.json`
  -> `dante/rq2_karaf/Budget_XX_Percent/<build>/{DANTE-CCH,Random}.json` (`paths.dante_solutions`)

Karaf clone (`paths.repo_clone`), blob-less so only needed files are downloaded:

```
git -c http.version=HTTP/1.1 clone --filter=blob:none --no-checkout https://github.com/apache/karaf.git C:/g2w/repos/karaf
```

Test sources are read with `git ls-tree` / `git cat-file` at each build commit; no worktree is checked out.

## Facts checked on the karaf data

- `dataset.csv`: 726 karaf builds, all stage `single`; 726 test-result zips and 726 diff files.
- `test_class.csv` columns: `testclass, duration, outcome, last_outcome`; outcome values are only 0 and 1. No flaky label.
- The 50 evaluation builds (`experiments/RQ1/karaf.csv`) are all in `dataset.csv` and all 50 build commits are in the clone.
- 37 of the 50 evaluation builds change only file types DANTE ignores in diffs (`.xml`, `.properties`, ...); 13 have code changes (`has_code_diff` in `data_eval/eval_builds.csv`).

## Generated files

- `data_eval/eval_builds.csv` — `python -m src.data.make_eval_builds`
