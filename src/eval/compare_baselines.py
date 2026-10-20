"""Baselines on the same builds and budgets: ours vs stored DANTE-CCH and Random.

    python -m src.eval.compare_baselines [--builds subset|all]
    python -m src.eval.compare_baselines --apfdc      # RQ1 APFDc recomputation, all 50 builds

Selection run: methods Random, DANTE-CCH-shipped, DANTE-CCH, History-only, TF-IDF-only
(ours) plus stored DANTE-CCH and stored Random; metrics %DTC, SAPFDc, SDS.
Writes results/baselines_comparison.csv.

APFDc run: orders all candidates by our DANTE-CCH value as run_prioritization.py
does (relevance weight 1.0 for the TF-IDF variant, 0 for the shipped variant) and
compares APFDc with the apfdc column of experiments/RQ1/<project>.csv.
Writes results/apfdc_vs_rq1.csv.
"""
import argparse
import os

import pandas as pd

from src.dante import rank, scores
from src.dante.compare_stored import load_stored
from src.data.loader import LRTSLoader
from src.data.sources import SourceRepo
from src.eval.metrics import all_metrics, apfdc
from src.eval.stored import rq1_table, solution_metrics
from src.settings import load_config, repo_path

OUR_METHODS = ["Random", "DANTE-CCH-shipped", "DANTE-CCH", "History-only", "TF-IDF-only"]


def setup(cfg):
    p = cfg["paths"]
    loader = LRTSLoader(p["lrts_root"], cfg["project"], SourceRepo(p["repo_clone"], p["repo_url"]))
    ev = pd.read_csv(repo_path(p["eval_builds"]))
    return loader, ev


def load_build(loader, cfg, e):
    row = loader.row(e.pr_name, e.build_id, e.stage_id)
    h = cfg["history"]
    return loader.build(row), loader.history(row, h["num_builds"], max(h["lookback_windows"]))


def baseline_rows(cfg, build, hist, build_name, budgets):
    """Metric rows for our baselines and the stored solutions of one build."""
    dfs = {"DANTE-CCH-shipped": scores(build, hist, cfg, "DANTE-CCH-shipped"),
           "DANTE-CCH": scores(build, hist, cfg, "DANTE-CCH")}
    for m in ("Random", "History-only", "TF-IDF-only"):
        dfs[m] = dfs["DANTE-CCH"]
    rows = []
    for b in budgets:
        for m in OUR_METHODS:
            df = dfs[m]
            sel, order, _ = rank(build, hist, b, cfg, m, df=df)
            dur = df["duration"].to_dict()
            failing = set(df.index[df["actual_outcome"] == 1])
            rows.append({"build": build.key, "budget": b, "method": m, "source": "ours",
                         **all_metrics(sel, dur, failing)})
        for strat in ("DANTE-CCH", "Random"):
            st = load_stored(cfg, build_name, b, strat)
            rows.append({"build": build.key, "budget": b, "method": f"{strat} (stored)", "source": "stored",
                         **solution_metrics(st)})
    return rows


def summarise(df, metrics=("dtc", "sapfdc", "sds")):
    """Median per method and budget; builds with no failures are already None for dtc/sapfdc."""
    t = df.groupby(["method", "budget"])[list(metrics)].median().unstack("budget")
    t.columns = [f"{m}@{int(b * 100)}%" for m, b in t.columns]
    return t


def run_selection(cfg, which):
    loader, ev = setup(cfg)
    if which == "subset":
        ev = ev[ev["phase1_subset"] == 1]
    rows = []
    for e in ev.itertuples():
        build, hist = load_build(loader, cfg, e)
        rows += baseline_rows(cfg, build, hist, e.build_name, cfg["budgets"])
    out = pd.DataFrame(rows)
    dest = repo_path(cfg["paths"]["results_dir"]) / "baselines_comparison.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dest, index=False)
    pd.set_option("display.width", 220)
    print(f"builds={out.build.nunique()} ({which}); medians:")
    print(summarise(out).round(3).to_string())
    print(f"-> {dest}")


def run_apfdc(cfg):
    loader, ev = setup(cfg)
    rq1 = rq1_table(cfg["paths"]["dante_root"])
    rq1 = rq1[(rq1.project == cfg["project"]) & (rq1.method == "DANTE-CCH")].set_index("build")["apfdc"]
    rows = []
    for e in ev.itertuples():
        build, hist = load_build(loader, cfg, e)
        rec = {"build": build.key, "stored_apfdc": float(rq1[e.build_name])}
        for name, w in (("shipped", 0.0), ("tfidf", cfg["dante"]["weight_relevance_rq1"])):
            df = scores(build, hist, cfg, "DANTE-CCH", w_relevance=w)
            order = df.sort_values(by="dante_cch_score", ascending=False).index.tolist()
            rec[f"{name}_apfdc"] = apfdc(order, df["duration"].to_dict(), set(df.index[df["actual_outcome"] == 1]))
        rows.append(rec)
    out = pd.DataFrame(rows)
    for v in ("shipped", "tfidf"):
        out[f"{v}_diff"] = out[f"{v}_apfdc"] - out["stored_apfdc"]
    dest = repo_path(cfg["paths"]["results_dir"]) / "apfdc_vs_rq1.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dest, index=False)
    print(f"builds={len(out)}  median stored APFDc={out.stored_apfdc.median():.4f}")
    for v in ("shipped", "tfidf"):
        d = out[f"{v}_diff"]
        print(f"{v:8s}: median APFDc={out[f'{v}_apfdc'].median():.4f}  median diff={d.median():+.4f}  "
              f"median |diff|={d.abs().median():.4f}  |diff|<=0.02: {int((d.abs() <= 0.02).sum())}/{len(d)}  "
              f"exact (<=1e-9): {int((d.abs() <= 1e-9).sum())}/{len(d)}")
    print(f"-> {dest}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--builds", default="subset", choices=["subset", "all"])
    ap.add_argument("--apfdc", action="store_true")
    args = ap.parse_args()
    cfg = load_config()
    if args.apfdc:
        run_apfdc(cfg)
    else:
        run_selection(cfg, args.builds)


if __name__ == "__main__":
    main()
