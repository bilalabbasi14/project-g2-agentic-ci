"""Compare our DANTE selections with the stored DANTE-CCH solution JSONs.

    python -m src.dante.compare_stored [--builds all|subset] [--show 5]

Two variants are recomputed per build and budget:
  shipped  : relevance weight 0 (what the shipped run_selection.py computes,
           since it reads relevance key "bm25" while the pipeline writes "tfidf")
  tfidf  : relevance weight 0.5 with TF-IDF relevance (as configured/described)
For each: overlap with the stored selection (Jaccard), failures found,
selected count, %DTC, and how many stored value_scores our score reproduces
(|diff| <= 1e-6 relative). Writes results/baseline_vs_stored.csv.
"""
import argparse
import json
import os
import statistics

import pandas as pd

from src.dante import rank, scores
from src.data.loader import LRTSLoader
from src.data.sources import SourceRepo
from src.settings import load_config, repo_path

BUDGETS = {0.05: "Budget_05_Percent", 0.10: "Budget_10_Percent", 0.20: "Budget_20_Percent"}


def load_stored(cfg, build_name, budget, strategy="DANTE-CCH"):
    p = os.path.join(cfg["paths"]["dante_solutions"], BUDGETS[budget], build_name, f"{strategy}.json")
    with open(p) as f:
        return json.load(f)


def value_match(df, stored):
    """Share of stored selected tests whose value_score our dante_cch_score reproduces."""
    hits = 0
    for x in stored["detailed_selection"]:
        if x["fqn"] in df.index:
            ours, theirs = float(df.loc[x["fqn"], "dante_cch_score"]), float(x["value_score"])
            hits += abs(ours - theirs) <= 1e-6 * max(1.0, abs(theirs))
    n = len(stored["detailed_selection"])
    return hits / n if n else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--builds", default="all", choices=["all", "subset"])
    ap.add_argument("--show", type=int, default=5)
    args = ap.parse_args()
    cfg = load_config()
    p = cfg["paths"]
    loader = LRTSLoader(p["lrts_root"], cfg["project"], SourceRepo(p["repo_clone"], p["repo_url"]))
    ev = pd.read_csv(repo_path(p["eval_builds"]))
    if args.builds == "subset":
        ev = ev[ev["phase1_subset"] == 1]
    h = cfg["history"]
    rows = []
    for e in ev.itertuples():
        row = loader.row(e.pr_name, e.build_id, e.stage_id)
        build = loader.build(row)
        hist = loader.history(row, h["num_builds"], max(h["lookback_windows"]))
        dfs = {"shipped": scores(build, hist, cfg, "DANTE-CCH-shipped"),
               "tfidf": scores(build, hist, cfg, "DANTE-CCH")}
        for b in cfg["budgets"]:
            st = load_stored(cfg, e.build_name, b)
            st_sel = [x["fqn"] for x in st["detailed_selection"]]
            rec = {"key": e.key, "budget": b, "total_failures": st["total_failures_in_build"],
                   "stored_selected": st["selected_tests_count"], "stored_found": st["failures_found"],
                   "stored_dtc": st["failures_found"] / st["total_failures_in_build"]}
            for v, df in dfs.items():
                sel, _, _ = rank(build, hist, b, cfg, "DANTE-CCH", df=df)
                found = int(df.loc[sel, "actual_outcome"].eq(1).sum()) if sel else 0
                union = set(sel) | set(st_sel)
                rec.update({f"{v}_selected": len(sel), f"{v}_found": found,
                            f"{v}_dtc": found / len(df[df.actual_outcome == 1]) if (df.actual_outcome == 1).any() else None,
                            f"{v}_jaccard": len(set(sel) & set(st_sel)) / len(union) if union else 1.0,
                            f"{v}_value_match": value_match(df, st)})
            rows.append(rec)
        print(f"{e.key} done", flush=True)
    out = pd.DataFrame(rows)
    dest = repo_path(p["results_dir"]) / "baseline_vs_stored.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dest, index=False)
    pd.set_option("display.width", 200)
    cols = ["key", "budget", "total_failures", "stored_selected", "shipped_selected", "tfidf_selected",
            "stored_found", "shipped_found", "tfidf_found", "shipped_jaccard", "tfidf_jaccard",
            "shipped_value_match", "tfidf_value_match"]
    shown = out[out.key.isin(out.key.unique()[:args.show])]
    print(shown[cols].round(3).to_string(index=False))
    print(f"\nbuilds={out.key.nunique()} rows={len(out)}")
    for b in cfg["budgets"]:
        s = out[out.budget == b]
        print(f"budget {b:.2f}: median %DTC stored={s.stored_dtc.median():.3f} "
              f"shipped={s.shipped_dtc.median():.3f} tfidf={s.tfidf_dtc.median():.3f} | "
              f"median diff vs stored shipped={statistics.median(s.shipped_dtc - s.stored_dtc):+.3f} "
              f"tfidf={statistics.median(s.tfidf_dtc - s.stored_dtc):+.3f} | "
              f"identical selections shipped={int((s.shipped_jaccard == 1).sum())}/{len(s)} "
              f"tfidf={int((s.tfidf_jaccard == 1).sum())}/{len(s)} | "
              f"mean value_match shipped={s.shipped_value_match.mean():.3f} tfidf={s.tfidf_value_match.mean():.3f}")
    print(f"-> {dest}")


if __name__ == "__main__":
    main()
