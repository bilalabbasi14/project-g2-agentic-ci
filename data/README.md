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

## Phase 2: getting the data

The input data is shared as a **private Kaggle dataset** `connectwithali27/karaf-data` (owner: Ali, Kaggle user `connectwithali27`; Bilal and Taha are collaborators). It contains one top folder `g2-karaf-data`:

```
g2-karaf-data/
  lrts/dataset.csv
  lrts/processed_test_result/karaf/<pr_name>_build<id>/stage_single/test_class.csv.zip   (or test_class.csv, see below)
  lrts/shadata/karaf/diff/<pr_name>_build<id>.diff
  dante/experiments/RQ1/*.csv
  dante/rq2_karaf/Budget_05_Percent/<build>/{DANTE-CCH,Random}.json
  dante/rq2_karaf/Budget_10_Percent/...
  dante/rq2_karaf/Budget_20_Percent/...
  README.txt
```

Do not redistribute it publicly.

Kaggle unpacked the nested `test_class.csv.zip` files when the dataset was uploaded, so the Kaggle copy (and possibly a copy downloaded from Kaggle) has `stage_single/test_class.csv` instead of `stage_single/test_class.csv.zip`. The code reads both forms (`src/tools/history_retrieval.py`: `resolve_test_class_file`, `open_test_class_csv`), so nothing needs to be re-zipped.

1. **Download to a laptop.** Either open the dataset page on kaggle.com and click *Download*, or install the client (`python -m pip install kaggle`), place your API token at `~/.kaggle/kaggle.json` (Kaggle → *Settings* → *Create New Token*; never commit it) and run
   `kaggle datasets download connectwithali27/karaf-data --unzip`
2. **Unzip** to a short path, for example `C:/g2w/`, so that you get `C:/g2w/g2-karaf-data/lrts/...` and `C:/g2w/g2-karaf-data/dante/...` (short paths avoid the Windows 260-character limit).
3. **Point the config at it** without editing the committed `config.yaml`: copy it to a personal file (for example `config_local.yaml`, not committed) and set
   - `paths.lrts_root` -> `<unzip folder>/g2-karaf-data/lrts`
   - `paths.dante_root` -> `<unzip folder>/g2-karaf-data/dante`
   - `paths.dante_solutions` -> `<unzip folder>/g2-karaf-data/dante/rq2_karaf`

   then select it with the `G2_CONFIG` environment variable (see `.env.example`), e.g. PowerShell `$env:G2_CONFIG="config_local.yaml"`, bash `export G2_CONFIG=config_local.yaml`.
4. **On Kaggle**, attach the dataset to the notebook (*Add Input* → `karaf-data` by `connectwithali27`). The folder that contains `lrts/` and `dante/` is mounted at:
   `/kaggle/input/datasets/connectwithali27/karaf-data/g2-karaf-data`
   (Kaggle named the dataset `karaf-data` and kept the zip's top folder `g2-karaf-data` inside it). The three paths are therefore `<mount>/lrts`, `<mount>/dante` and `<mount>/dante/rq2_karaf`.
5. **Check the data**:
   ```
   python -m src.data.check_data
   ```
   or with explicit folders:
   ```
   python -m src.data.check_data --lrts <lrts_root> --dante <dante_root> --solutions <dante_solutions>
   ```
   On Kaggle:
   ```
   python -m src.data.check_data --lrts /kaggle/input/datasets/connectwithali27/karaf-data/g2-karaf-data/lrts --dante /kaggle/input/datasets/connectwithali27/karaf-data/g2-karaf-data/dante --solutions /kaggle/input/datasets/connectwithali27/karaf-data/g2-karaf-data/dante/rq2_karaf
   ```
   Every line must say `OK` (726 karaf builds with test results, as `.zip` or extracted `.csv`, and diffs, 50 distinct builds in `RQ1/karaf.csv`, 50 build folders with `DANTE-CCH.json` and `Random.json` per budget); the exit code is 0 only then.

## Phase 2: test-source cache (no git clone needed)

The LLM needs the source text of each test class at the build's commit. Kaggle notebooks have no Karaf clone, so these sources are precomputed once into a **source cache**, published as a private Kaggle dataset `connectwithali27/g2-source-cache` (owner: Ali; shared with Bilal and Taha). It holds one file per evaluation build, `<build_key>.json.gz`, for the Phase 2 evaluation builds (`data_eval/eval_builds_p2.csv`) and the Phase 1 builds (`data_eval/eval_builds.csv`). Do not redistribute it publicly. It is never committed (`source_cache/` is git-ignored).

- **Generate** (needs the data and the git clone, laptop only):
  `python -m src.data.source_cache --eval data_eval/eval_builds_p2.csv data_eval/eval_builds.csv --check 3`
  writes to `paths_p2.source_cache` (or `--out <dir>`), skips files that already exist (`--force` rewrites them), and with `--check 3` compares the cache with git for the first 3 builds.
- **Use**: set `paths_p2.source_cache` to the cache folder in your personal config. `LRTSLoader(..., source_cache_dir=...)` then reads a build's sources from `<dir>/<build_key>.json.gz`, or, if Kaggle unpacked the `.gz` files on upload, from a plain `<build_key>.json` or from a folder `<build_key>.json.gz/` that holds the JSON. It falls back to the git clone when a build has no cache file. An empty or missing `paths_p2.source_cache` means "no cache".
- **On Kaggle**, attach `g2-source-cache` (*Add Input*) and set `paths_p2.source_cache` to the folder that `!ls /kaggle/input/datasets/connectwithali27/g2-source-cache` shows contains the `PR-*_build*.json(.gz)` files. Expected mount: `/kaggle/input/datasets/connectwithali27/g2-source-cache` (to be confirmed after publishing; see PR for P2-09).
