"""Phase 2 evaluation set with a fixed chronological dev/test split (P2-08).

    python -m src.data.make_eval_set_p2 [--n-dev 10] [--dry-run]

The rule (docs/PROJECT_CONTEXT.md §6.2) is fixed before any results are seen,
and no method's results are read here. Every build that passes F1-F4 is used
(group decision of 6 November 2026: only 54 builds qualify, so the planned
120-build target and the 60-build minimum were dropped; see
docs/devlog/2026-11-06-ali-eval-set-size.md). Steps, cheap filters first:
  F1  enough history: chrono_index >= 100 (a full 100-build history window)
  F2  code change: split_diff(diff) returns at least one file
  F3  has failures: the raw test_class.csv has a row with outcome == 1
  pre-selection: only if more than 160 builds remain, 160 evenly spaced in time
  F4  usable for DANTE: loader.build(row) has a candidate (source found,
      duration > 0) with outcome 1
  split: the earliest `n_dev` builds are "dev", the rest "test"; no usable
      build at all, or not more than `n_dev`, is an error
Writes data_eval/eval_builds_p2.csv and data_eval/eval_set_p2_report.md.
Do not edit the CSV by hand; change this script and regenerate it.
"""
import argparse
import logging
import sys
from datetime import datetime, timezone

import pandas as pd

from src.data.loader import LRTSLoader
from src.data.sources import SourceRepo
from src.settings import load_config, repo_path
from src.tools.diff_reader import split_diff

log = logging.getLogger(__name__)

# The selection rule of P2-08 (fixed in the issue; changing one changes the evaluation set).
MIN_HISTORY = 100          # F1: builds before the target
PRESELECT = 160            # builds kept before the slow source check (only if more remain)
DEFAULT_N_DEV = 10

COLUMNS = ["key", "pr_name", "build_id", "stage_id", "sha", "chrono_index", "timestamp", "n_code_files",
           "n_candidates", "n_failing_candidates", "in_phase1", "split"]
REPORT = "data_eval/eval_set_p2_report.md"


class TooFewBuildsError(RuntimeError):
    """Not enough usable builds for a dev and a test split."""


def evenly_spaced(df, n):
    """n rows evenly spaced in time: sorted by chrono_index, rows at positions
    round(i * (N - 1) / (n - 1)) for i = 0..n-1. All rows if N <= n."""
    df = df.sort_values("chrono_index").reset_index(drop=True)
    total = len(df)
    if total <= n:
        return df
    if n == 1:
        return df.iloc[[0]].reset_index(drop=True)
    pos = [round(i * (total - 1) / (n - 1)) for i in range(n)]
    return df.iloc[pos].reset_index(drop=True)


def assign_split(df, n_dev):
    """Sort by time; the earliest n_dev rows are "dev", the rest "test"."""
    df = df.sort_values("chrono_index").reset_index(drop=True)
    df["split"] = ["dev" if i < n_dev else "test" for i in range(len(df))]
    return df


def apply_cheap_filters(meta, diff_reader_fn, outcomes_fn):
    """F1-F3 on the chronologically sorted metadata.

    diff_reader_fn(row) -> split_diff dict of the build (or None if missing);
    outcomes_fn(row) -> iterable of outcome values of the raw test_class.csv (or None).
    Returns (kept rows with chrono_index and n_code_files, counts per filter)."""
    df = meta.reset_index(drop=True).copy()
    if "chrono_index" not in df.columns:
        df["chrono_index"] = range(len(df))
    counts = {"all": len(df)}
    df = df[df["chrono_index"] >= MIN_HISTORY]
    counts["F1"] = len(df)
    n_files = {}
    for i, row in df.iterrows():
        files = diff_reader_fn(row)
        n_files[i] = len(files) if files else 0
    df = df.assign(n_code_files=pd.Series(n_files, dtype="int64"))
    df = df[df["n_code_files"] > 0]
    counts["F2"] = len(df)
    keep = []
    for i, row in df.iterrows():
        outcomes = outcomes_fn(row)
        keep.append(outcomes is not None and any(_is_fail(o) for o in outcomes))
    df = df[keep] if len(df) else df
    counts["F3"] = len(df)
    return df.reset_index(drop=True), counts


def _is_fail(o):
    try:
        return int(float(o)) == 1
    except (TypeError, ValueError):
        return False


def usable_for_dante(build_fn, row):
    """F4 for one build: (ok, reason, n_candidates, n_failing_candidates)."""
    try:
        build = build_fn(row)
    except Exception as e:   # recorded as an exclusion reason, never silently dropped
        return False, f"load_error: {type(e).__name__}: {e}"[:200], 0, 0
    if not build.sources_available:
        return False, "no_commit_in_clone", 0, 0
    cands = build.candidates()
    failing = sum(1 for t in cands if t.outcome == 1)
    if failing == 0:
        return False, "no_failing_candidate", len(cands), 0
    return True, None, len(cands), failing


def select(meta, diff_reader_fn, outcomes_fn, build_fn, phase1_keys, n_dev=DEFAULT_N_DEV):
    """The whole rule. Returns (final DataFrame with COLUMNS, report facts).
    Raises TooFewBuildsError when there are not more than n_dev usable builds."""
    cheap, counts = apply_cheap_filters(meta, diff_reader_fn, outcomes_fn)
    pre = evenly_spaced(cheap, PRESELECT)
    counts["preselected"] = len(pre)
    usable, reasons = [], {}
    for _, row in pre.iterrows():
        ok, reason, n_cand, n_fail = usable_for_dante(build_fn, row)
        if ok:
            usable.append({**row.to_dict(), "n_candidates": n_cand, "n_failing_candidates": n_fail})
        else:
            key = reason.split(":", 1)[0]
            reasons[key] = reasons.get(key, 0) + 1
            log.info("excluded %s: %s", row["key"], reason)
    counts["F4"] = len(usable)
    if len(usable) <= n_dev:
        raise TooFewBuildsError(f"only {len(usable)} usable builds, not enough for {n_dev} dev builds and a "
                                f"test split. Counts: {counts}, exclusions: {reasons}")
    final = assign_split(pd.DataFrame(usable), n_dev)
    counts["final"] = len(final)
    keys = set(phase1_keys)
    out = pd.DataFrame({
        "key": final["key"], "pr_name": final["pr_name"], "build_id": final["build_id"].astype(int),
        "stage_id": final["stage_id"], "sha": final["build_head_sha"],
        "chrono_index": final["chrono_index"].astype(int), "timestamp": final["timestamp_for_sort"],
        "n_code_files": final["n_code_files"].astype(int), "n_candidates": final["n_candidates"].astype(int),
        "n_failing_candidates": final["n_failing_candidates"].astype(int),
        "in_phase1": final["key"].isin(keys), "split": final["split"]})[COLUMNS]
    return out, {"counts": counts, "reasons": reasons}


def _date(ts):
    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime("%Y-%m-%d")


def render_report(out, facts, command):
    c = facts["counts"]
    lines = ["# Phase 2 evaluation set (P2-08)", "",
             "Generated by `src/data/make_eval_set_p2.py`; the rule is in its docstring and in "
             "docs/PROJECT_CONTEXT.md §6.2. No method results were read.", "",
             f"Command: `{command}`", "", "## Builds after each step", "", "| Step | Builds |", "|---|---|",
             f"| All Karaf builds in LRTS | {c['all']} |",
             f"| F1: at least {MIN_HISTORY} earlier builds | {c['F1']} |",
             f"| F2: diff changes at least one code file | {c['F2']} |",
             f"| F3: at least one failing test class | {c['F3']} |",
             f"| Pre-selection (only if more than {PRESELECT}: {PRESELECT} evenly spaced) | {c['preselected']} |",
             f"| F4: a failing candidate with readable source | {c['F4']} |",
             f"| Final (all builds that pass F1-F4) | {c['final']} |", "", "## Split", "",
             "| Split | Builds | First build date (UTC) | Last build date (UTC) | Builds also in Phase 1 |",
             "|---|---|---|---|---|"]
    for name in ("dev", "test"):
        s = out[out["split"] == name]
        if len(s):
            lines.append(f"| {name} | {len(s)} | {_date(s['timestamp'].min())} | {_date(s['timestamp'].max())} | "
                         f"{int(s['in_phase1'].sum())} |")
        else:
            lines.append(f"| {name} | 0 | - | - | 0 |")
    lines += ["", "## Exclusions in F4", "", "| Reason | Builds |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(facts["reasons"].items())] or ["| (none) | 0 |"]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n-dev", type=int, default=DEFAULT_N_DEV)
    ap.add_argument("--dry-run", action="store_true", help="print the counts after F1-F3 and stop")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.WARNING)
    cfg = load_config()
    p = cfg["paths"]
    loader = LRTSLoader(p["lrts_root"], cfg["project"], None if args.dry_run else
                        SourceRepo(p["repo_clone"], p["repo_url"]))

    def diff_fn(row):
        try:
            with open(loader.diff_path(row), "r", encoding="utf-8", errors="ignore") as f:
                return split_diff(f.read())
        except OSError:
            return None

    def outcomes_fn(row):
        df = loader.test_class_df(row)
        return None if df is None else df["outcome"].tolist()

    meta = loader.meta.copy()
    meta["chrono_index"] = range(len(meta))
    if args.dry_run:
        _, counts = apply_cheap_filters(meta, diff_fn, outcomes_fn)
        print(f"all={counts['all']} F1={counts['F1']} F2={counts['F2']} F3={counts['F3']}")
        return 0
    phase1 = pd.read_csv(repo_path(p["eval_builds"]))["key"].tolist()
    command = "python -m src.data.make_eval_set_p2" + "".join(
        f" {a}" for a in (argv if argv is not None else sys.argv[1:]))
    try:
        out, facts = select(meta, diff_fn, outcomes_fn, lambda r: loader.build(r), phase1, args.n_dev)
    except TooFewBuildsError as e:
        raise SystemExit(f"ERROR: {e}") from e     # nothing is written
    write(out, facts, command, repo_path(cfg["eval"]["eval_set"]), repo_path(REPORT))
    print(render_report(out, facts, command))
    return 0


def write(out, facts, command, csv_path, report_path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(csv_path, index=False, lineterminator="\n")
    report_path.write_text(render_report(out, facts, command), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sys.exit(main())
