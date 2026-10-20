"""Stored DANTE results as tables.

    python -m src.eval.stored     # reproduces the RQ1 medians and stored RQ2 metrics

rq1_table(): all experiments/RQ1/*.csv (columns project, build, method, apfdc).
solutions_table(): the extracted solution JSONs (one row per build/budget/strategy)
with %DTC, SAPFDc and SDS computed on the stored selection order.
"""
import glob
import json
import os

import pandas as pd

from src.eval.metrics import all_metrics, apfdc
from src.settings import load_config


def rq1_table(dante_root):
    frames = []
    for f in sorted(glob.glob(os.path.join(dante_root, "experiments", "RQ1", "*.csv"))):
        df = pd.read_csv(f)
        df.insert(0, "project", os.path.splitext(os.path.basename(f))[0])
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def solution_metrics(sol):
    sel = [x["fqn"] for x in sol["detailed_selection"]]
    dur = {x["fqn"]: x["duration"] for x in sol["detailed_selection"]}
    found = {x["fqn"] for x in sol["detailed_selection"] if x["did_fail"]}
    # Failing tests outside the selection are not listed in the JSON, so %DTC uses
    # the stored total and SAPFDc = %DTC x APFDc of the selected order.
    m = all_metrics(sel, dur, found)
    total = sol["total_failures_in_build"]
    m["total_failures"] = total
    m["dtc"] = None if total == 0 else len(found) / total
    m["sapfdc"] = None if total == 0 else (0.0 if not found else m["dtc"] * apfdc(sel, dur, found))
    return m


def solutions_table(solutions_root):
    rows = []
    for path in sorted(glob.glob(os.path.join(solutions_root, "Budget_*_Percent", "*", "*.json"))):
        budget_dir, build, fname = path.split(os.sep)[-3:]
        with open(path) as f:
            sol = json.load(f)
        m = solution_metrics(sol)
        rows.append({"budget": int(budget_dir.split("_")[1]) / 100, "build_name": build,
                     "strategy": os.path.splitext(fname)[0], **m})
    return pd.DataFrame(rows)


def main():
    cfg = load_config()
    p = cfg["paths"]
    rq1 = rq1_table(p["dante_root"])
    c = rq1[rq1.method == "DANTE-CCH"]
    print(f"RQ1 DANTE-CCH: rows={len(c)} projects={c.project.nunique()} median APFDc={c.apfdc.median():.4f}")
    k = c[c.project == cfg["project"]]
    print(f"RQ1 DANTE-CCH {cfg['project']}: rows={len(k)} median APFDc={k.apfdc.median():.4f}")
    print(rq1.groupby("method").apfdc.median().round(4).to_string())
    sol = solutions_table(p["dante_solutions"])
    print(f"\nstored {cfg['project']} solutions: {len(sol)} rows")
    print(sol.groupby(["budget", "strategy"])[["dtc", "sapfdc", "sds"]].median().round(4).to_string())


if __name__ == "__main__":
    main()
