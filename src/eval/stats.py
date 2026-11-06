"""Statistics for the research questions (docs/PROJECT_CONTEXT.md §8, "Statistics").

    python -m src.eval.stats --runs results/E*_test_seed*/per_build.csv --out results/stats

Input: per_build.csv files in the format of src/pipeline.py (PER_BUILD_COLUMNS);
only rows with split == "test" are used. Methods are compared on the same builds
(paired data):

1. For each (method, build, budget) the metric is averaged over the available
   seeds first; a deterministic method with one seed keeps its value.
2. Friedman's test (scipy) per set in experiments/comparisons.yaml, metric and
   budget, on the builds present for every method of the set.
3. Wilcoxon signed-rank tests (scipy, two-sided, zero_method="wilcox") of the
   target against each other method of a comparison, with Holm correction within
   each family (comparison key × metric × budget) and the matched-pairs
   rank-biserial correlation as effect size (positive = target better).
4. Seed variability: mean and standard deviation (ddof=1) over seeds of the
   per-seed mean over builds, for every method with more than one seed.

Outputs in --out: friedman.csv, pairwise.csv, seed_variability.csv, summary.md.
"""
import argparse
import glob
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy import stats as sps

from src.settings import repo_path

log = logging.getLogger(__name__)

COMPARISONS_FILE = "experiments/comparisons.yaml"
ALPHA = 0.05                     # §8: Holm-corrected significance level
ZERO_TOL = 1e-12                 # |difference| below this counts as a tie (seed means are floats)

PAIRWISE_COLUMNS = ["family", "target", "other", "metric", "budget", "n", "mean_diff", "median_diff", "wins",
                    "ties", "losses", "W", "p_raw", "p_holm", "significant", "effect_r"]
FRIEDMAN_COLUMNS = ["set", "metric", "budget", "n_builds", "n_methods", "statistic", "p_value", "method",
                    "mean_rank"]
SEED_COLUMNS = ["method", "budget", "metric", "seeds", "mean", "std"]


class StatsError(ValueError):
    """The input cannot give the requested comparisons; the message says why."""


# ------------------------------------------------------------------ input ----

def load_comparisons(path=None):
    with open(repo_path(path or COMPARISONS_FILE), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    families = {k: v for k, v in cfg.items() if k not in ("friedman_sets", "metrics", "budgets")}
    return {"families": families, "friedman_sets": cfg.get("friedman_sets") or {},
            "metrics": list(cfg["metrics"]), "budgets": [round(float(b), 4) for b in cfg["budgets"]]}


def expand_paths(patterns):
    """File paths from the arguments; patterns with * or ? are expanded here too
    (PowerShell does not expand them), relative to the repository root."""
    out = []
    for p in patterns:
        if any(c in p for c in "*?["):
            hits = sorted(glob.glob(str(repo_path(p))))
            if not hits:
                raise StatsError(f"no files match {p!r}")
            out.extend(hits)
        else:
            out.append(str(repo_path(p)))
    return out


def load_runs(paths):
    """All per_build.csv rows of the test split, budgets rounded to 4 decimals."""
    frames = [pd.read_csv(p) for p in paths]
    if not frames:
        raise StatsError("no per_build.csv files given")
    df = pd.concat(frames, ignore_index=True)
    df = df[df["split"] == "test"].copy()
    if df.empty:
        raise StatsError("no rows with split == 'test' in the given files")
    df["budget"] = df["budget"].astype(float).round(4)
    return df


def check_methods(df, comparisons):
    """Raise StatsError listing every method the comparisons need but the data lacks."""
    needed = set()
    for fam in comparisons["families"].values():
        needed |= {fam["target"], *fam["against"]}
    for methods in comparisons["friedman_sets"].values():
        needed |= set(methods)
    missing = sorted(needed - set(df["method"].unique()))
    if missing:
        raise StatsError("cannot make the comparisons; methods missing from the test-split results: "
                         + ", ".join(missing))


def seed_average(df, metrics):
    """Long table (method, build, budget, metric, value): mean over seeds per build.

    Rows repeated for the same seed (a deterministic method stored in two runs)
    are first merged, so they do not count twice. Missing values are ignored."""
    long = df.melt(id_vars=["method", "build", "budget", "seed"], value_vars=metrics, var_name="metric",
                   value_name="value").dropna(subset=["value"])
    per_seed = long.groupby(["method", "build", "budget", "metric", "seed"], as_index=False)["value"].mean()
    return per_seed.groupby(["method", "build", "budget", "metric"], as_index=False)["value"].mean()


def _matrix(avg, methods, metric, budget):
    """builds × methods for one metric and budget, only builds present for all methods."""
    sub = avg[(avg["metric"] == metric) & (avg["budget"] == budget) & avg["method"].isin(methods)]
    wide = sub.pivot_table(index="build", columns="method", values="value", aggfunc="mean")
    return wide.reindex(columns=list(methods)).dropna()


# -------------------------------------------------------------- statistics ----

def holm(pvals):
    """Holm-adjusted p-values, in the input order: the i-th smallest of m is
    multiplied by (m - i), the results are made non-decreasing and capped at 1.
    NaN values stay NaN and do not count towards m."""
    p = np.asarray(pvals, dtype=float)
    out = np.full(p.shape, np.nan)
    idx = np.where(~np.isnan(p))[0]
    m = len(idx)
    running = 0.0
    for i, j in enumerate(sorted(idx, key=lambda k: p[k])):
        running = max(running, min(1.0, (m - i) * p[j]))
        out[j] = running
    return out.tolist()


def _clean(diff):
    d = np.asarray(diff, dtype=float)
    d[np.abs(d) < ZERO_TOL] = 0.0
    return d


def rank_biserial(diff):
    """Matched-pairs rank-biserial correlation r = (R+ - R-) / (R+ + R-), ranks of
    the absolute non-zero differences (ties get average ranks). 0 if all are zero."""
    d = _clean(diff)
    d = d[d != 0]
    if d.size == 0:
        return 0.0
    ranks = sps.rankdata(np.abs(d))
    r_plus, r_minus = ranks[d > 0].sum(), ranks[d < 0].sum()
    return float((r_plus - r_minus) / (r_plus + r_minus))


def paired_test(diff):
    """Wilcoxon signed-rank summary of target − other differences over shared builds."""
    d = _clean(diff)
    row = {"n": int(d.size), "mean_diff": float(d.mean()) if d.size else np.nan,
           "median_diff": float(np.median(d)) if d.size else np.nan,
           "wins": int((d > 0).sum()), "ties": int((d == 0).sum()), "losses": int((d < 0).sum())}
    if d.size == 0:
        return {**row, "W": np.nan, "p_raw": np.nan, "effect_r": np.nan}
    if not (d != 0).any():
        return {**row, "W": 0.0, "p_raw": 1.0, "effect_r": 0.0}
    res = sps.wilcoxon(d, zero_method="wilcox", alternative="two-sided")
    return {**row, "W": float(res.statistic), "p_raw": float(res.pvalue), "effect_r": rank_biserial(d)}


def pairwise(avg, comparisons):
    """One row per family, other method, metric and budget, with Holm within the family."""
    rows = []
    for family, fam in comparisons["families"].items():
        target = fam["target"]
        for metric in comparisons["metrics"]:
            for budget in comparisons["budgets"]:
                group = []
                for other in fam["against"]:
                    m = _matrix(avg, [target, other], metric, budget)
                    group.append({"family": family, "target": target, "other": other, "metric": metric,
                                  "budget": budget, **paired_test(m[target] - m[other])})
                for r, adj in zip(group, holm([r["p_raw"] for r in group])):
                    r["p_holm"] = adj
                    r["significant"] = bool(adj < ALPHA) if not np.isnan(adj) else False
                rows.extend(group)
    return pd.DataFrame(rows, columns=PAIRWISE_COLUMNS)


def friedman(avg, comparisons):
    """Friedman test per set, metric and budget; mean rank 1 = best (highest value)."""
    rows = []
    for name, methods in comparisons["friedman_sets"].items():
        for metric in comparisons["metrics"]:
            for budget in comparisons["budgets"]:
                m = _matrix(avg, methods, metric, budget)
                n = len(m)
                ranks = (pd.DataFrame(sps.rankdata(-m.to_numpy(), axis=1), columns=methods).mean() if n
                         else pd.Series(np.nan, index=methods))
                if n < 2:                                   # no test possible on 0 or 1 build
                    stat = p = np.nan
                elif (m.nunique(axis=1) == 1).all():        # every build ties all methods
                    stat, p = 0.0, 1.0
                else:
                    res = sps.friedmanchisquare(*[m[c].to_numpy() for c in methods])
                    stat, p = float(res.statistic), float(res.pvalue)
                for meth in methods:
                    rows.append({"set": name, "metric": metric, "budget": budget, "n_builds": n,
                                 "n_methods": len(methods), "statistic": stat, "p_value": p, "method": meth,
                                 "mean_rank": float(ranks[meth])})
    return pd.DataFrame(rows, columns=FRIEDMAN_COLUMNS)


def seed_variability(df, metrics, budgets):
    """Per method with > 1 seed: mean over builds per seed, then mean and std (ddof=1)."""
    rows = []
    sub = df[df["budget"].isin(budgets)]
    for method, g in sub.groupby("method"):
        seeds = sorted(g["seed"].dropna().unique())
        if len(seeds) < 2:
            continue
        for budget in budgets:
            for metric in metrics:
                gb = g[g["budget"] == budget].dropna(subset=[metric])
                per_build_seed = gb.groupby(["seed", "build"])[metric].mean()
                per_seed = per_build_seed.groupby(level="seed").mean()
                if len(per_seed) < 2:
                    continue
                rows.append({"method": method, "budget": budget, "metric": metric,
                             "seeds": ";".join(str(int(s)) for s in per_seed.index),
                             "mean": float(per_seed.mean()), "std": float(per_seed.std(ddof=1))})
    return pd.DataFrame(rows, columns=SEED_COLUMNS)


# ----------------------------------------------------------------- output ----

def _f(x, digits=3):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{digits}f}"


def summary_markdown(pw, fr, sv, paths):
    lines = ["# Statistics (test split)", "",
             f"Input: {len(paths)} per_build.csv file(s). Metrics are averaged over seeds per build first. "
             f"Wilcoxon signed-rank (two-sided), Holm correction within each family "
             f"(comparison × metric × budget), α = {ALPHA}. Effect size r = matched-pairs rank-biserial "
             "correlation (positive = target better). Friedman mean rank 1 = best.", ""]
    for family in pw["family"].unique():
        f = pw[pw["family"] == family]
        lines += [f"## {family}: {f['target'].iloc[0]} vs others", "",
                  "| metric | budget | other | n | mean diff | W/T/L | p | p (Holm) | sig. | r |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for r in f.itertuples(index=False):
            lines.append(f"| {r.metric} | {r.budget:.0%} | {r.other} | {r.n} | {_f(r.mean_diff)} | "
                         f"{r.wins}/{r.ties}/{r.losses} | {_f(r.p_raw, 4)} | {_f(r.p_holm, 4)} | "
                         f"{'yes' if r.significant else 'no'} | {_f(r.effect_r)} |")
        lines.append("")
    lines += ["## Friedman tests", "", "| set | metric | budget | n builds | χ² | p | best mean rank |",
              "|---|---|---|---|---|---|---|"]
    for (name, metric, budget), g in fr.groupby(["set", "metric", "budget"], sort=False):
        best = g.sort_values("mean_rank").iloc[0]
        lines.append(f"| {name} | {metric} | {budget:.0%} | {g['n_builds'].iloc[0]} | "
                     f"{_f(g['statistic'].iloc[0])} | {_f(g['p_value'].iloc[0], 4)} | "
                     f"{best['method']} ({_f(best['mean_rank'], 2)}) |")
    lines += ["", "## Seed variability", ""]
    if sv.empty:
        lines.append("No method has more than one seed.")
    else:
        lines += ["| method | budget | metric | seeds | mean | std |", "|---|---|---|---|---|---|"]
        lines += [f"| {r.method} | {r.budget:.0%} | {r.metric} | {r.seeds} | {_f(r.mean)} | {_f(r.std)} |"
                  for r in sv.itertuples(index=False)]
    return "\n".join(lines) + "\n"


def run(paths, out_dir, comparisons_path=None):
    """Compute every table and write them to out_dir; returns (pairwise, friedman, seed_variability)."""
    comparisons = load_comparisons(comparisons_path)
    df = load_runs(paths)
    check_methods(df, comparisons)
    avg = seed_average(df, comparisons["metrics"])
    pw = pairwise(avg, comparisons)
    fr = friedman(avg, comparisons)
    sv = seed_variability(df, comparisons["metrics"], comparisons["budgets"])
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pw.to_csv(out / "pairwise.csv", index=False)
    fr.to_csv(out / "friedman.csv", index=False)
    sv.to_csv(out / "seed_variability.csv", index=False)
    (out / "summary.md").write_text(summary_markdown(pw, fr, sv, paths), encoding="utf-8")
    return pw, fr, sv


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m src.eval.stats", description=__doc__.split("\n\n")[0])
    p.add_argument("--runs", nargs="+", required=True, help="per_build.csv files or glob patterns")
    p.add_argument("--out", default="results/stats")
    p.add_argument("--comparisons", default=COMPARISONS_FILE)
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        paths = expand_paths(args.runs)
        pw, _, _ = run(paths, repo_path(args.out), args.comparisons)
    except StatsError as e:
        log.error("%s", e)
        return 1
    log.info("%d pairwise comparisons, %d significant after Holm; written to %s",
             len(pw), int(pw["significant"].sum()), args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
