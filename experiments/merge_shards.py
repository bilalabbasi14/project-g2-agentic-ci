"""Combine the shard files of one run into the final result files.

    python -m experiments.merge_shards --run-id E3_test_seed1 [--results-dir results]

Concatenates every <name>.shard<i>.csv in results/<run_id>/ with the existing
<name>.csv (if a resumed run was merged before), drops duplicate rows (for
per_build.csv: one row per build, method and budget, the newest kept), sorts by
build, method and budget, writes <name>.csv, merges run_meta.shard<i>.json into
run_meta.json and deletes the shard files.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

from src.pipeline import DECISION_COLUMNS, EXPLANATION_COLUMNS, LLM_RELEVANCE_COLUMNS, PER_BUILD_COLUMNS
from src.settings import load_config, repo_path

FILES = {"per_build": PER_BUILD_COLUMNS, "llm_relevance": LLM_RELEVANCE_COLUMNS,
         "orchestrator_decisions": DECISION_COLUMNS, "explanations": EXPLANATION_COLUMNS}
UNIQUE = {"per_build": ["build", "method", "budget"],
          "llm_relevance": ["build", "relevance_source", "test"],
          "orchestrator_decisions": ["build", "relevance_source"],
          "explanations": ["build", "budget", "method", "test"]}
SORT = ["build", "method", "budget", "relevance_source", "test"]
SHARD = re.compile(r"\.shard(\d+)\.(csv|json)$")


def shard_files(run_dir, stem, ext):
    files = [p for p in Path(run_dir).glob(f"{stem}.shard*.{ext}") if SHARD.search(p.name)]
    return sorted(files, key=lambda p: int(SHARD.search(p.name).group(1)))


def merge_csv(run_dir, stem, columns):
    """Returns (rows written, shard files merged)."""
    run_dir = Path(run_dir)
    parts = shard_files(run_dir, stem, "csv")
    if not parts:
        return None, []
    final = run_dir / f"{stem}.csv"
    frames = [pd.read_csv(final, dtype=str, keep_default_na=False)] if final.exists() else []
    frames += [pd.read_csv(p, dtype=str, keep_default_na=False) for p in parts]
    df = pd.concat(frames, ignore_index=True)
    if list(df.columns) != columns:
        raise ValueError(f"{stem}: unexpected columns {list(df.columns)}")
    df = df.drop_duplicates(subset=UNIQUE[stem], keep="last")
    keys = [c for c in SORT if c in df.columns]
    order = df[keys].copy()
    if "budget" in order:
        order["budget"] = pd.to_numeric(order["budget"])
    df = df.loc[order.sort_values(keys, kind="stable").index]
    df.to_csv(final, index=False, lineterminator="\n")
    return len(df), parts


def merge_meta(run_dir):
    run_dir = Path(run_dir)
    parts = shard_files(run_dir, "run_meta", "json")
    if not parts:
        return None, []
    metas = [json.loads(p.read_text(encoding="utf-8")) for p in parts]
    final = run_dir / "run_meta.json"
    if final.exists():
        metas.insert(0, json.loads(final.read_text(encoding="utf-8")))
    merged = dict(metas[-1])
    merged["started"] = min(m["started"] for m in metas)
    merged["finished"] = max(m["finished"] for m in metas)
    merged["n_builds"] = sum(m["n_builds"] for m in metas)
    merged["failed_builds"] = [f for m in metas for f in m["failed_builds"]]
    merged["skipped_existing"] = sorted({k for m in metas for k in m.get("skipped_existing") or []})
    merged["shards"] = [m.get("shard") for m in metas if m.get("shard")] + \
        [s for m in metas for s in m.get("shards", [])]
    merged.pop("shard", None)
    commits = sorted({m["git_commit"] for m in metas})
    if len(commits) > 1:
        merged["git_commit_warning"] = f"shards ran on different commits: {commits}"
    final.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    return merged, parts


def merge_run(run_dir):
    """Merge every shard file of a run and delete them. Returns {name: rows}."""
    out, done = {}, []
    for stem, columns in FILES.items():
        n, parts = merge_csv(run_dir, stem, columns)
        if n is not None:
            out[stem] = n
            done += parts
    meta, parts = merge_meta(run_dir)
    done += parts
    if meta is not None:
        out["run_meta"] = meta["n_builds"]
    for p in done:
        p.unlink()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Merge shard result files of one run.")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--results-dir", help="default: paths.results_dir from the config")
    args = ap.parse_args(argv)
    base = Path(args.results_dir) if args.results_dir else repo_path(load_config()["paths"]["results_dir"])
    run_dir = base / args.run_id
    if not run_dir.is_dir():
        raise SystemExit(f"no run folder {run_dir}")
    out = merge_run(run_dir)
    if not out:
        print(f"no shard files in {run_dir}")
    for name, n in out.items():
        print(f"{name}: {n} {'builds' if name == 'run_meta' else 'rows'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
