"""Tuned-weight baselines (P2-11): the best fixed weight w* on the dev split.

    python -m src.dante.tune_weight --relevance tfidf
    python -m src.dante.tune_weight --relevance llm --llm-relevance results/DEV_prompt_v1/llm_relevance.csv

Phase 1 hypothesis H-A: if the agent's per-build weight does no better than one
fixed weight chosen carefully in advance, the agent adds nothing. This module
finds that fixed weight, separately for TF-IDF and for LLM relevance, by a rule
fixed in the issue:

- only the **dev** builds of cfg["eval"]["eval_set"] are used (never `test`);
- for every w in cfg["tuning"]["w_grid"] and every budget in cfg["budgets"]:
  scores with score_table(w_history=w, w_relevance=1-w, relevance_override=...)
  (docs/PROJECT_CONTEXT.md §5.1; w = 2/3 is DANTE), greedy selection, all_metrics;
- for `llm`, relevance is the dev run's LLM relevance (0 for tests the LLM did
  not score); a build whose LLM relevance fell back uses the DANTE-CCH result
  for every w, exactly as the pipeline does;
- objective: mean SAPFDc over the dev builds at cfg["tuning"]["objective_budget"];
  ties (within TIE_MARGIN of the best) go to the w closest to 2/3.

Writes results/tuning/dev_grid_<relevance>.csv and updates
experiments/tuned_weights.yaml, keeping the other relevance type's entry.
The target builds' outcomes are used only to compute the metrics.
"""
import argparse
import logging
import statistics
import sys
from pathlib import Path

import pandas as pd
import yaml

from src.contracts import DANTE_W
from src.dante import rank, scores
from src.dante.scoring import score_table
from src.eval.metrics import all_metrics
from src.settings import load_config, repo_path

log = logging.getLogger(__name__)

TIE_MARGIN = 0.001              # objective values within this of the best count as tied (issue P2-11)
RELEVANCES = ("tfidf", "llm")
GRID_COLUMNS = ["w", "budget", "builds", "dtc_mean", "sapfdc_mean", "apfdc_median"]
GRID_DIR = "results/tuning"


# ------------------------------------------------------------- pure parts ----

def build_metrics(build, hist, cfg, w, budgets, override=None, fell_back=False):
    """[{budget, dtc, sapfdc, apfdc_full}] for one build and one w.

    `override` replaces the relevance of the listed tests (LLM relevance); a
    fell-back build ranks with DANTE-CCH (w = 2/3, TF-IDF) whatever w is."""
    h, d = cfg["history"], cfg["dante"]
    if fell_back:
        df = scores(build, hist, cfg, "DANTE-CCH")
    else:
        df, _ = score_table(build, hist, h["lookback_windows"], h["min_sticky_events"], w_history=w,
                            w_relevance=1 - w, power=d["relevance_power"], relevance_override=override)
    if df is None or df.empty:
        return []
    failing = set(df.index[df["actual_outcome"] == 1])          # ground truth for the metrics only
    durations = df["duration"].to_dict()
    out = []
    for b in budgets:
        sel, order, _ = rank(build, hist, b, cfg, "DANTE-CCH", df=df)
        m = all_metrics(sel, durations, failing, full_order=order)
        out.append({"budget": float(b), "dtc": m["dtc"], "sapfdc": m["sapfdc"], "apfdc_full": m["apfdc_full"]})
    return out


def grid_metrics(rows):
    """Per (w, budget): number of builds, mean %DTC, mean SAPFDc, median APFDc.
    `rows` are dicts with w, budget, build, dtc, sapfdc, apfdc_full."""
    df = pd.DataFrame(rows)
    out = []
    for (w, b), g in df.groupby(["w", "budget"], sort=True):
        out.append({"w": float(w), "budget": float(b), "builds": int(g["build"].nunique()),
                    "dtc_mean": float(g["dtc"].mean()), "sapfdc_mean": float(g["sapfdc"].mean()),
                    "apfdc_median": float(statistics.median(g["apfdc_full"]))})
    return pd.DataFrame(out, columns=GRID_COLUMNS)


def choose_w(grid_df, budget, tie_target=DANTE_W, margin=TIE_MARGIN):
    """(w*, objective value): the w with the highest mean SAPFDc at `budget`; among
    the w within `margin` of the best, the one closest to `tie_target` (2/3).
    If two are equally close, the smaller w is taken (deterministic)."""
    at = grid_df[(grid_df["budget"] - budget).abs() < 1e-9]
    if at.empty:
        raise ValueError(f"no grid rows at budget {budget}")
    best = at["sapfdc_mean"].max()
    near = at[at["sapfdc_mean"] >= best - margin]
    pick = near.assign(dist=(near["w"] - tie_target).abs()).sort_values(["dist", "w"]).iloc[0]
    return float(pick["w"]), float(pick["sapfdc_mean"])


def update_weights_file(path, relevance, entry):
    """Write `entry` under `relevance` in the YAML file, keeping the other entries."""
    path = Path(path)
    data = {}
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data[relevance] = entry
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({k: data[k] for k in sorted(data)}, sort_keys=False), encoding="utf-8")
    return data


def load_llm_relevance(path):
    """{build: (relevance dict, fell_back)} from a run's llm_relevance.csv
    (only the llm_shortlist rows, the source LLM-relevance uses)."""
    df = pd.read_csv(path)
    if "relevance_source" in df.columns:
        df = df[df["relevance_source"] == "llm_shortlist"]
    out = {}
    for build, g in df.groupby("build"):
        fell_back = g["fell_back"].astype(str).str.lower().isin(("true", "1")).any()
        out[build] = ({t: float(r) for t, r in zip(g["test"], g["relevance"])}, bool(fell_back))
    return out


# ----------------------------------------------------------------- runner ----

def dev_rows(cfg):
    """The dev builds of the evaluation set; the test split is never read here."""
    ev = pd.read_csv(repo_path(cfg["eval"]["eval_set"]))
    dev = ev[ev["split"] == "dev"]
    if dev.empty:
        raise SystemExit("no dev builds in the evaluation set")
    return list(dev.itertuples(index=False))


def make_loader(cfg):
    """Loader with the source cache (P2-09); the git clone only if it already exists."""
    from src.data.loader import LRTSLoader
    from src.data.source_cache import cache_dir_from_config
    from src.data.sources import SourceRepo
    p = cfg["paths"]
    clone = p.get("repo_clone")
    repo = SourceRepo(clone, p.get("repo_url")) if clone and Path(clone).is_dir() else None
    return LRTSLoader(p["lrts_root"], cfg["project"], repo, source_cache_dir=cache_dir_from_config(cfg))


def tune(cfg, relevance, loader, rows, llm=None):
    """Grid DataFrame over the given (dev) builds."""
    h = cfg["history"]
    budgets = [float(b) for b in cfg["budgets"]]
    grid = [float(w) for w in cfg["tuning"]["w_grid"]]
    out = []
    for e in rows:
        row = loader.row(e.pr_name, e.build_id, e.stage_id)
        build = loader.build(row)
        hist = loader.history(row, h["num_builds"], max(h["lookback_windows"]))
        override, fell_back = None, False
        if relevance == "llm":
            if build.key not in llm:
                raise SystemExit(f"{build.key}: no LLM relevance in the given llm_relevance.csv")
            values, fell_back = llm[build.key]
            df = scores(build, hist, cfg, "DANTE-CCH")
            override = {t: values.get(t, 0.0) for t in (df.index if df is not None else [])}
        for w in grid:
            for m in build_metrics(build, hist, cfg, w, budgets, override, fell_back):
                out.append({"w": w, "build": build.key, **m})
        log.info("%s done", build.key)
    return grid_metrics(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Tune the fixed weight w on the dev split (P2-11).")
    ap.add_argument("--relevance", choices=RELEVANCES, required=True)
    ap.add_argument("--llm-relevance", help="llm_relevance.csv of the chosen dev prompt run (for --relevance llm)")
    ap.add_argument("--out", default=GRID_DIR, help="folder for dev_grid_<relevance>.csv")
    args = ap.parse_args(argv)
    if args.relevance == "llm" and not args.llm_relevance:
        ap.error("--relevance llm needs --llm-relevance results/DEV_prompt_<winner>/llm_relevance.csv")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_config()
    rows = dev_rows(cfg)
    llm = load_llm_relevance(repo_path(args.llm_relevance)) if args.relevance == "llm" else None
    grid_df = tune(cfg, args.relevance, make_loader(cfg), rows, llm)
    out_dir = repo_path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    grid_file = out_dir / f"dev_grid_{args.relevance}.csv"
    grid_df.to_csv(grid_file, index=False, lineterminator="\n")
    objective_budget = float(cfg["tuning"]["objective_budget"])
    w, value = choose_w(grid_df, objective_budget)
    entry = {"w": w, "objective": f"sapfdc_mean@{objective_budget:.2f}", "value": round(value, 4),
             "dev_builds": int(grid_df["builds"].max()), "grid_file": f"{args.out}/dev_grid_{args.relevance}.csv"}
    if args.relevance == "llm":
        entry["llm_run"] = Path(args.llm_relevance).parent.name
    update_weights_file(repo_path(cfg["tuning"]["tuned_weights_file"]), args.relevance, entry)
    print(f"{args.relevance}: w* = {w} ({entry['objective']} = {value:.4f}, {entry['dev_builds']} dev builds) "
          f"-> {grid_file}, {cfg['tuning']['tuned_weights_file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
