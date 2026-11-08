"""Results tables, figures and the gap-resolution table (P2-19).

    python -m src.eval.report [--results results] [--tables results/tables] [--figures results/figures]

Everything is regenerated from committed files only:
- results/<run>/per_build.csv, orchestrator_decisions.csv and run_meta.json of every run;
  the test split is used for everything except the E2 reproduction (phase1 split);
- results/stats/pairwise.csv and seed_variability.csv (src.eval.stats, P2-13);
- results/analysis/shortlist_recall_test.csv (src.eval.shortlist_recall, P2-12);
- results/gap2/rating_summary.csv (src.eval.rating, P2-18/P2-25);
- data_eval/eval_builds.csv (the replication package's stored APFDc, column rq1_dante_cch_apfdc).

Tables (results/tables/<name>.csv and .md): main_results, gap1, gap3 (+ gap3_w), gap2, ablation,
efficiency, e2_reproduction and gap_resolution. Figures (results/figures/*.png, 300 dpi, grey
fills with hatching so they stay readable in black-and-white print): fig_dtc_by_method,
fig_sapfdc_box_10, fig_ablation, fig_latency_breakdown and fig_agent_w_hist.

The "Addressed?" label of the gap-resolution table comes only from resolve_gap, which applies
the rule of docs/PROJECT_CONTEXT.md §8 (fixed before the results were seen).
"""
import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from src.eval import stats as st  # noqa: E402
from src.settings import repo_path  # noqa: E402

log = logging.getLogger(__name__)

BUDGETS = [0.05, 0.10, 0.20]
GAP_BUDGET = 0.10                # §8: the gap rule is applied at the 10% budget
GAP_METRICS = ("dtc", "sapfdc")
ALPHA = st.ALPHA                 # Holm-corrected significance level (0.05)
SOUND_THRESHOLD = 0.80           # RQ2: at least 80% of the sampled justifications rated sound
TOL = st.ZERO_TOL
DANTE_W = 2 / 3

FULL = "Full system"
DANTE = "DANTE-CCH"
SHIPPED = "DANTE-CCH-shipped"
STORED = "DANTE-CCH (stored)"
GAP_FAMILIES = {1: "RQ1", 3: "RQ3"}
GAP_COMPONENTS = {1: "semantic analyzer", 2: "explainer", 3: "orchestrator"}
ABLATION_FAMILY = "E5"
ABLATIONS = [("LLM-relevance", "orchestrator"), ("Agent-weighted (TF-IDF)", "LLM relevance"),
             ("Agent-weighted", "explainer"), ("Full system (no shortlist)", "shortlist")]
METHOD_ORDER = ["Random", "History-only", "TF-IDF-only", "DANTE-CCH-shipped", "DANTE-CCH",
                "Tuned-weight (TF-IDF)", "Single-call LLM", "LLM-relevance", "Tuned-weight (LLM)",
                "Agent-weighted", "Full system", "Agent-weighted (TF-IDF)", "Full system (no shortlist)"]
LLM_SOURCES = ("llm_shortlist", "llm_single_call", "llm_all_individual")
SOURCE_METHODS = {"llm_shortlist": "Agent-weighted, Full system", "tfidf": "Agent-weighted (TF-IDF)",
                  "llm_all_individual": "Full system (no shortlist)"}
METRIC_NAMES = {"dtc": "%DTC", "sapfdc": "SAPFDc"}

MAIN_COLUMNS = ["method", "budget", "seeds", "n_builds", "dtc_mean", "dtc_std", "sapfdc_mean", "sapfdc_std",
                "apfdc_median", "sds_median"]
GAP_COLUMNS = ["metric", "budget", "target", "target_mean", "other", "other_mean", "mean_diff", "wins", "ties",
               "losses", "p_holm", "significant", "effect_r"]
W_COLUMNS = ["relevance_source", "methods", "runs", "decisions", "w_min", "w_q1", "w_median", "w_q3", "w_max",
             "w_mean", "distinct_w", "share_w_dante", "fallback_share"]
GAP2_COLUMNS = ["scope", "budget", "runs", "n_builds", "n_pairs", "mean_decision_s", "mean_explanation_s",
                "mean_overhead_s", "mean_time_saved_s", "pairs_overhead_below_saved", "share_overhead_below_saved", "n_rated",
                "share_sound", "share_partly", "share_unsound", "kappa"]
ABLATION_COLUMNS = ["ablation", "removed_component", "metric", "budget", "seeds", "n_builds", "full_mean",
                    "ablation_mean", "change_when_removed", "p_holm", "effect_r"]
EFFICIENCY_COLUMNS = ["method", "runs", "build_runs", "llm_calls_per_build", "cached_call_share",
                      "tool_calls_per_build", "prompt_tokens_per_build", "completion_tokens_per_build",
                      "decision_latency_s", "relevance_latency_s", "orchestrator_latency_s", "explainer_runs",
                      "explainer_calls_per_build", "explanation_latency_s", "explainer_failed_share",
                      "fallback_rate", "gpu_hours"]
E2_COLUMNS = ["metric", "budget", "method", "source", "n_builds", "median", "reference", "median_diff_vs_reference",
              "tolerance", "builds_within_tolerance"]
RESOLUTION_COLUMNS = ["gap", "method_component", "metric", "base_paper_result", "our_result", "addressed"]
RESOLUTION_HEADERS = ["Gap", "Method/component", "Metric", "Base paper result (DANTE-CCH, reproduced by us, at 10%)",
                      "Our result (at 10%)", "Addressed?"]

# grey fills with hatching: distinguishable without colour
STYLES = [("white", "//"), ("lightgray", ".."), ("dimgray", "xx"), ("black", ""), ("white", "\\\\"),
          ("lightgray", "--")]


class ReportError(ValueError):
    """A committed input is missing or inconsistent; the message says which."""


# ------------------------------------------------------------------ input ----

def _key(budget):
    return round(float(budget), 4)


def _ordered(methods):
    methods = list(dict.fromkeys(methods))
    return [m for m in METHOD_ORDER if m in methods] + sorted(m for m in methods if m not in METHOD_ORDER)


def _read_csv(path, what):
    p = Path(path)
    if not p.is_file():
        raise ReportError(f"{what} not found: {p}")
    df = pd.read_csv(p)
    if "budget" in df.columns:
        df["budget"] = pd.to_numeric(df["budget"], errors="coerce").round(4)
    return df


def load_runs(results_dir):
    """All per_build.csv rows of results/<run>/ (budget rounded) and the run_meta of each run."""
    frames, metas = [], {}
    for d in sorted(Path(results_dir).iterdir()):
        if not (d / "per_build.csv").is_file():
            continue
        frames.append(pd.read_csv(d / "per_build.csv"))
        if (d / "run_meta.json").is_file():
            meta = json.loads((d / "run_meta.json").read_text(encoding="utf-8"))
            metas[meta.get("run_id", d.name)] = meta
    if not frames:
        raise ReportError(f"no per_build.csv under {results_dir}")
    df = pd.concat(frames, ignore_index=True)
    df["budget"] = df["budget"].astype(float).round(4)
    return df, metas


def load_decisions(results_dir, run_ids):
    """orchestrator_decisions.csv of the given runs, with a run_id column."""
    frames = []
    for run_id in run_ids:
        p = Path(results_dir) / run_id / "orchestrator_decisions.csv"
        if p.is_file():
            frames.append(pd.read_csv(p).assign(run_id=run_id))
    cols = ["run_id", "build", "relevance_source", "w", "confidence", "source", "steps", "llm_calls",
            "tool_calls", "reason", "fallback_reason"]
    return pd.concat(frames, ignore_index=True)[cols] if frames else pd.DataFrame(columns=cols)


def run_hours(meta):
    """Wall-clock hours of one run (run_meta finished − started)."""
    t0, t1 = meta.get("started"), meta.get("finished")
    if not t0 or not t1:
        return np.nan
    return (datetime.fromisoformat(t1) - datetime.fromisoformat(t0)).total_seconds() / 3600


# ----------------------------------------------------------------- tables ----

def main_results(test, seed_var=None):
    """Every method × budget: %DTC and SAPFDc mean over builds (of the per-build seed means) ± the std
    over seeds from seed_variability (NaN for single-seed methods), median full-ranking APFDc and SDS."""
    metrics = ["dtc", "sapfdc", "sds", "apfdc_full"]
    avg = st.seed_average(test, metrics)
    if seed_var is None:
        seed_var = st.seed_variability(test, ["dtc", "sapfdc"], sorted(test["budget"].unique()))
    std = {(r.method, _key(r.budget), r.metric): r.std for r in seed_var.itertuples(index=False)}
    rows = []
    for method in _ordered(test["method"].unique()):
        seeds = int(test.loc[test["method"] == method, "seed"].nunique())
        for budget in sorted(test.loc[test["method"] == method, "budget"].unique()):
            a = avg[(avg["method"] == method) & (avg["budget"] == budget)]
            val = {m: a.loc[a["metric"] == m, "value"] for m in metrics}
            row = {"method": method, "budget": _key(budget), "seeds": seeds, "n_builds": int(a["build"].nunique()),
                   "apfdc_median": float(val["apfdc_full"].median()), "sds_median": float(val["sds"].median())}
            for m in ("dtc", "sapfdc"):
                row[f"{m}_mean"] = float(val[m].mean())
                if seeds > 1:
                    if (method, _key(budget), m) not in std:
                        raise ReportError(f"seed_variability has no row for {method} / {budget} / {m}")
                    row[f"{m}_std"] = float(std[(method, _key(budget), m)])
                else:
                    row[f"{m}_std"] = np.nan
            rows.append(row)
    return pd.DataFrame(rows, columns=MAIN_COLUMNS)


def gap_comparison(pairwise, main, family):
    """The pairwise rows of one RQ family with the mean of both methods (from main_results)."""
    f = pairwise[pairwise["family"] == family]
    if f.empty:
        raise ReportError(f"results/stats/pairwise.csv has no rows for family {family}")
    means = {(r.method, r.budget): r for r in main.itertuples(index=False)}
    rows = []
    for r in f.itertuples(index=False):
        b = _key(r.budget)
        rows.append({"metric": r.metric, "budget": b, "target": r.target,
                     "target_mean": getattr(means[(r.target, b)], f"{r.metric}_mean"), "other": r.other,
                     "other_mean": getattr(means[(r.other, b)], f"{r.metric}_mean"), "mean_diff": r.mean_diff,
                     "wins": r.wins, "ties": r.ties, "losses": r.losses, "p_holm": r.p_holm,
                     "significant": bool(r.significant), "effect_r": r.effect_r})
    return pd.DataFrame(rows, columns=GAP_COLUMNS)


def w_distribution(decisions):
    """The orchestrator's chosen w per relevance source: quartiles, distinct values, share equal to
    DANTE's 2/3 and share of fallbacks (fallback_reason set or source other than the agent)."""
    rows = []
    for src, g in decisions.groupby("relevance_source", sort=False):
        w = g["w"].astype(float)
        fb = g["fallback_reason"].notna() | (g["source"] != "agent")
        rows.append({"relevance_source": src, "methods": SOURCE_METHODS.get(src, ""), "runs": g["run_id"].nunique(),
                     "decisions": len(g), "w_min": w.min(), "w_q1": w.quantile(0.25), "w_median": w.median(),
                     "w_q3": w.quantile(0.75), "w_max": w.max(), "w_mean": w.mean(), "distinct_w": w.nunique(),
                     "share_w_dante": float((np.abs(w - DANTE_W) < 1e-6).mean()), "fallback_share": float(fb.mean())})
    return pd.DataFrame(rows, columns=W_COLUMNS)


def explainer_rows(test, method=FULL):
    """Rows of `method` from the runs in which its explainer was on (explainer_calls > 0 in the run)."""
    m = test[test["method"] == method]
    calls = m.groupby("run_id")["explainer_calls"].sum()
    return m[m["run_id"].isin(calls[calls > 0].index)]


def gap2_table(test, ratings):
    """Per budget: mean decision, explanation and total overhead time per build, mean time saved, and how
    many build-budget pairs have overhead < time saved (Full system with the explainer on); with the
    ratings. The overall row pools the pairs of all budgets."""
    fs = explainer_rows(test)
    if fs.empty:
        raise ReportError("no Full system run with the explainer on")
    fs = fs.assign(overhead=fs["decision_latency_s"] + fs["explainer_latency_s"])
    per = fs.groupby(["budget", "build"], as_index=False)[
        ["decision_latency_s", "explainer_latency_s", "overhead", "time_saved_s"]].mean()
    runs = ";".join(sorted(fs["run_id"].unique()))
    rat = ratings.copy()
    rat["budget"] = pd.to_numeric(rat["budget"], errors="coerce").round(4)
    overall = rat[rat["scope"] == "overall"]
    if overall.empty:
        raise ReportError("rating_summary.csv has no overall row")
    kappa = float(overall["kappa"].iloc[0])

    def latency(g):
        below = g["overhead"] < g["time_saved_s"]
        return {"n_builds": int(g["build"].nunique()), "n_pairs": len(g),
                "mean_decision_s": g["decision_latency_s"].mean(),
                "mean_explanation_s": g["explainer_latency_s"].mean(), "mean_overhead_s": g["overhead"].mean(),
                "mean_time_saved_s": g["time_saved_s"].mean(), "pairs_overhead_below_saved": int(below.sum()),
                "share_overhead_below_saved": float(below.mean())}

    def rating(r):
        return {"n_rated": int(r["n"]), "share_sound": r["share_sound"], "share_partly": r["share_partly"],
                "share_unsound": r["share_unsound"], "kappa": kappa}

    rows = []
    for b in sorted(per["budget"].unique()):
        r = rat[(rat["scope"] == "budget") & (rat["budget"] == _key(b))]
        rows.append({"scope": "budget", "budget": _key(b), "runs": runs, **latency(per[per["budget"] == b]),
                     **(rating(r.iloc[0]) if not r.empty else {})})
    rows.append({"scope": "overall", "budget": np.nan, "runs": runs, **latency(per), **rating(overall.iloc[0])})
    return pd.DataFrame(rows, columns=GAP2_COLUMNS)


def ablation_table(test, pairwise):
    """Full system vs each ablation on the builds and seeds both have; change = ablation − Full system.
    p (Holm) and r come from pairwise.csv (family E5, Full system = target) where that pair is tested."""
    rows = []
    full = test[test["method"] == FULL]
    for abl, removed in ABLATIONS:
        a = test[test["method"] == abl]
        if a.empty:
            raise ReportError(f"ablation {abl!r} has no test-split rows")
        seeds = sorted(set(full["seed"]) & set(a["seed"]))
        fa = st.seed_average(full[full["seed"].isin(seeds)], list(GAP_METRICS))
        aa = st.seed_average(a[a["seed"].isin(seeds)], list(GAP_METRICS))
        for metric in GAP_METRICS:
            for b in sorted(a["budget"].unique()):
                x = fa[(fa["metric"] == metric) & (fa["budget"] == b)].set_index("build")["value"]
                y = aa[(aa["metric"] == metric) & (aa["budget"] == b)].set_index("build")["value"]
                idx = x.index.intersection(y.index)
                p = pairwise[(pairwise["family"] == ABLATION_FAMILY) & (pairwise["target"] == FULL) &
                             (pairwise["other"] == abl) & (pairwise["metric"] == metric) &
                             (np.isclose(pairwise["budget"], b))]
                tested = not p.empty and int(p["n"].iloc[0]) == len(idx)
                rows.append({"ablation": abl, "removed_component": removed, "metric": metric, "budget": _key(b),
                             "seeds": ";".join(str(int(s)) for s in seeds), "n_builds": len(idx),
                             "full_mean": float(x[idx].mean()), "ablation_mean": float(y[idx].mean()),
                             "change_when_removed": float(y[idx].mean() - x[idx].mean()),
                             "p_holm": float(p["p_holm"].iloc[0]) if tested else np.nan,
                             "effect_r": float(p["effect_r"].iloc[0]) if tested else np.nan})
    return pd.DataFrame(rows, columns=ABLATION_COLUMNS)


def efficiency(test, decisions, metas):
    """E6 per LLM method, per build and run. Decision costs (relevance + orchestrator) are the same in the
    three budget rows of a build, so one row per build is used; explainer costs are summed over the budgets
    and averaged only over runs with the explainer on. Relevance latency of an agent method = the decision
    latency of a fixed/tuned-weight method with the same LLM relevance source in the same run and build
    (NaN if the run has none); orchestrator latency = decision latency − relevance latency."""
    llm = test[test["relevance_source"].isin(LLM_SOURCES) | (test["weight_mode"] == "agent")]
    first = llm.sort_values("budget").groupby(["run_id", "method", "build"], as_index=False).first()
    sums = llm.groupby(["run_id", "method", "build"], as_index=False).agg(
        explainer_calls=("explainer_calls", "sum"), explainer_latency_s=("explainer_latency_s", "sum"),
        explainer_ok=("explainer_ok", "sum"), fell_back=("ranking_source", lambda s: bool((s == "dante_fallback").any())))
    plain = first[(first["weight_mode"] != "agent") & first["relevance_source"].isin(LLM_SOURCES)]
    rel_latency = plain.groupby(["run_id", "build", "relevance_source"])["decision_latency_s"].first().to_dict()
    dec_fb = {}
    for r in decisions.itertuples(index=False):
        dec_fb[(r.run_id, r.build, r.relevance_source)] = bool(pd.notna(r.fallback_reason) or r.source != "agent")
    rows = []
    for method in _ordered(first["method"].unique()):
        f = first[first["method"] == method].copy()
        s = sums[sums["method"] == method]
        agent = f["weight_mode"] == "agent"
        llm_rel = f["relevance_source"].isin(LLM_SOURCES)
        rel = np.where(~llm_rel, 0.0, np.where(~agent, f["decision_latency_s"],
                       [rel_latency.get((r, b, src), np.nan) for r, b, src in
                        zip(f["run_id"], f["build"], f["relevance_source"])]))
        orch = np.where(agent, f["decision_latency_s"] - rel, 0.0)
        orch_fb = [agent_i and dec_fb.get((r, b, src), False) for agent_i, r, b, src in
                   zip(agent, f["run_id"], f["build"], f["relevance_source"])]
        fell = s.set_index(["run_id", "build"])["fell_back"].reindex(list(zip(f["run_id"], f["build"]))).to_numpy()
        fallback = np.asarray(fell, dtype=bool) | np.asarray(orch_fb, dtype=bool)
        on = s.groupby("run_id")["explainer_calls"].sum()
        e = s[s["run_id"].isin(on[on > 0].index)]
        runs = sorted(f["run_id"].unique())
        calls = f["llm_calls"].sum()
        rows.append({
            "method": method, "runs": ";".join(runs), "build_runs": len(f),
            "llm_calls_per_build": f["llm_calls"].mean(),
            "cached_call_share": float(f["llm_cached_calls"].sum() / calls) if calls else np.nan,
            "tool_calls_per_build": f["tool_calls"].mean(), "prompt_tokens_per_build": f["prompt_tokens"].mean(),
            "completion_tokens_per_build": f["completion_tokens"].mean(),
            "decision_latency_s": f["decision_latency_s"].mean(),
            "relevance_latency_s": float(np.mean(rel)) if not np.isnan(rel).any() else np.nan,
            "orchestrator_latency_s": float(np.mean(orch)) if not np.isnan(orch).any() else np.nan,
            "explainer_runs": int(e["run_id"].nunique()),
            "explainer_calls_per_build": e["explainer_calls"].mean() if len(e) else np.nan,
            "explanation_latency_s": e["explainer_latency_s"].mean() if len(e) else np.nan,
            "explainer_failed_share": (float(1 - e["explainer_ok"].sum() / e["explainer_calls"].sum())
                                       if len(e) else np.nan),
            "fallback_rate": float(fallback.mean()),
            "gpu_hours": float(sum(run_hours(metas[r]) for r in runs if r in metas))})
    return pd.DataFrame(rows, columns=EFFICIENCY_COLUMNS)


def e2_reproduction(phase1, eval_builds):
    """Our DANTE-CCH-shipped and DANTE-CCH vs the replication package on the 50 Phase 1 builds:
    median full-ranking APFDc against the package's RQ1 APFDc, and median %DTC per budget against the
    package's stored selections (DANTE-CCH (stored); its %DTC is computed with our metric code)."""
    p = phase1[phase1["method"].isin([SHIPPED, DANTE, STORED])]
    if not {SHIPPED, DANTE, STORED} <= set(p["method"]):
        raise ReportError("the phase1 run must contain DANTE-CCH, DANTE-CCH-shipped and DANTE-CCH (stored)")
    builds = sorted(p["build"].unique())
    pkg = eval_builds.set_index("key")["rq1_dante_cch_apfdc"].reindex(builds)
    if pkg.isna().any():
        raise ReportError("eval_builds.csv has no rq1_dante_cch_apfdc for some phase1 builds")
    pkg_label = "DANTE-CCH (replication package, RQ1 APFDc)"
    rows = [{"metric": "APFDc (full ranking)", "budget": np.nan, "method": pkg_label,
             "source": "taken from the replication package", "n_builds": len(pkg), "median": float(pkg.median()),
             "reference": "", "median_diff_vs_reference": np.nan, "tolerance": np.nan,
             "builds_within_tolerance": np.nan}]
    full = p[p["method"].isin([SHIPPED, DANTE])].groupby(["method", "build"])["apfdc_full"].first()
    for m in (SHIPPED, DANTE):
        v = full[m].reindex(builds)
        d = v - pkg
        rows.append({"metric": "APFDc (full ranking)", "budget": np.nan, "method": m, "source": "reproduced by us",
                     "n_builds": int(v.notna().sum()), "median": float(v.median()), "reference": pkg_label,
                     "median_diff_vs_reference": float(d.median()), "tolerance": 0.02,
                     "builds_within_tolerance": int((d.abs() <= 0.02 + TOL).sum())})
    for b in sorted(p["budget"].unique()):
        ref = p[(p["method"] == STORED) & (p["budget"] == b)].set_index("build")["dtc"]
        rows.append({"metric": "%DTC", "budget": _key(b), "method": STORED,
                     "source": "taken from the replication package (stored selections; %DTC computed by our code)",
                     "n_builds": int(ref.notna().sum()), "median": float(ref.median()), "reference": "",
                     "median_diff_vs_reference": np.nan, "tolerance": np.nan, "builds_within_tolerance": np.nan})
        for m in (SHIPPED, DANTE):
            v = p[(p["method"] == m) & (p["budget"] == b)].set_index("build")["dtc"]
            d = (v - ref).dropna()
            rows.append({"metric": "%DTC", "budget": _key(b), "method": m, "source": "reproduced by us",
                         "n_builds": int(v.notna().sum()), "median": float(v.median()), "reference": STORED,
                         "median_diff_vs_reference": float(d.median()), "tolerance": 0.0,
                         "builds_within_tolerance": int((d.abs() <= TOL).sum())})
    return pd.DataFrame(rows, columns=E2_COLUMNS)


# --------------------------------------------------------- gap resolution ----

def resolve_gap(gap, stats, ratings):
    """The "Addressed?" label of one gap, by the rule of docs/PROJECT_CONTEXT.md §8:

    Gaps 1 and 3 (stats["pairwise"], families RQ1 / RQ3; a difference is target − other):
      Fully     = the gap method beats every comparison method of its RQ on both %DTC and SAPFDc at the
                  10% budget (mean difference > 0) with Holm-corrected p < 0.05;
      Not       = no improvement anywhere: no positive mean difference against any comparison method,
                  at any metric and budget;
      Partially = everything in between (a win on only some metrics, budgets or methods, or a win
                  that is not significant).
    Gap 2: condition (a) = at every budget the mean decision + explanation time per build is below the
      mean test time saved per build (stats["overhead"]: budget, mean_overhead_s, mean_time_saved_s);
      condition (b) = ratings["share_sound"] >= 0.80. Fully = both hold, Partially = one, Not = neither.
    """
    if gap in GAP_FAMILIES:
        pw = stats["pairwise"]
        fam = pw[pw["family"] == GAP_FAMILIES[gap]]
        if fam.empty:
            raise ReportError(f"no pairwise rows for family {GAP_FAMILIES[gap]}")
        at = fam[np.isclose(fam["budget"].astype(float), GAP_BUDGET)]
        fully = all(not at[at["metric"] == m].empty for m in GAP_METRICS) and all(
            r.mean_diff > TOL and r.p_holm < ALPHA for r in at[at["metric"].isin(GAP_METRICS)].itertuples())
        if fully:
            return "Fully"
        return "Partially" if (fam["mean_diff"] > TOL).any() else "Not"
    if gap == 2:
        ov = stats["overhead"]
        if ov.empty:
            raise ReportError("no overhead rows for gap 2")
        time_ok = bool((ov["mean_overhead_s"] < ov["mean_time_saved_s"]).all())
        sound_ok = float(ratings["share_sound"]) >= SOUND_THRESHOLD
        return {2: "Fully", 1: "Partially", 0: "Not"}[int(time_ok) + int(sound_ok)]
    raise ReportError(f"unknown gap {gap!r}")


def gap_resolution(main, pairwise, gap2, ratings_overall):
    """Rows of the gap-resolution table: one per gap and metric; labels from resolve_gap."""
    means = {(r.method, r.budget): r for r in main.itertuples(index=False)}
    budget_rows = gap2[gap2["scope"] == "budget"]
    stats_in = {"pairwise": pairwise, "overhead": budget_rows}
    rows = []
    for gap in (1, 2, 3):
        label = resolve_gap(gap, stats_in, ratings_overall)
        if gap in GAP_FAMILIES:
            fam = pairwise[(pairwise["family"] == GAP_FAMILIES[gap]) & np.isclose(pairwise["budget"], GAP_BUDGET)]
            target = fam["target"].iloc[0]
            for m in GAP_METRICS:
                sub = fam[fam["metric"] == m]
                comps = "; ".join(f"vs {r.other} {r.mean_diff:+.3f}, p_Holm {r.p_holm:.4f}"
                                  for r in sub.itertuples(index=False))
                rows.append({"gap": f"Gap {gap}", "method_component": f"{target} ({GAP_COMPONENTS[gap]})",
                             "metric": f"{METRIC_NAMES[m]}, mean over builds",
                             "base_paper_result": f"{getattr(means[(DANTE, GAP_BUDGET)], f'{m}_mean'):.3f}",
                             "our_result": f"{getattr(means[(target, GAP_BUDGET)], f'{m}_mean'):.3f} ({comps})",
                             "addressed": label})
        else:
            r10 = budget_rows[np.isclose(budget_rows["budget"], GAP_BUDGET)].iloc[0]
            rows.append({"gap": "Gap 2", "method_component": f"{FULL} ({GAP_COMPONENTS[2]})",
                         "metric": "Decision + explanation time vs test time saved, mean s per build",
                         "base_paper_result": "n/a (DANTE gives no explanations)",
                         "our_result": (f"{r10.mean_overhead_s:.1f} s vs {r10.mean_time_saved_s:.1f} s saved; "
                                        f"below on {int(r10.pairs_overhead_below_saved)} of {int(r10.n_pairs)} "
                                        "builds"),
                         "addressed": label})
            rows.append({"gap": "Gap 2", "method_component": f"{FULL} ({GAP_COMPONENTS[2]})",
                         "metric": "Share of the 100 sampled justifications rated sound (all budgets; RQ2 needs 0.80)",
                         "base_paper_result": "n/a (DANTE gives no explanations)",
                         "our_result": (f"{float(ratings_overall['share_sound']):.3f} "
                                        f"(Cohen's kappa {float(ratings_overall['kappa']):.3f})"),
                         "addressed": label})
    return pd.DataFrame(rows, columns=RESOLUTION_COLUMNS)


# ---------------------------------------------------------------- figures ----

def _save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def _bar(ax, x, h, style, **kw):
    face, hatch = style
    return ax.bar(x, h, color=face, hatch=hatch, edgecolor="black", linewidth=0.7, **kw)


def fig_dtc_by_method(main, path):
    """Grouped bars: mean %DTC per method at each budget, ± std over seeds as error bars."""
    methods = _ordered(main["method"].unique())
    budgets = sorted(main["budget"].unique())
    x = np.arange(len(methods))
    width = 0.8 / len(budgets)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    for i, b in enumerate(budgets):
        sub = main[main["budget"] == b].set_index("method").reindex(methods)
        _bar(ax, x + (i - (len(budgets) - 1) / 2) * width, sub["dtc_mean"].fillna(0), STYLES[i], width=width,
             yerr=sub["dtc_std"].fillna(0), capsize=2, error_kw={"elinewidth": 0.8}, label=f"{b:.0%} budget")
    most = int(main["n_builds"].max())
    labels = []
    for m in methods:
        r = main[main["method"] == m].iloc[0]
        labels.append(m + ("*" if int(r["seeds"]) == 1 else "")
                      + (f" ({int(r['n_builds'])} builds)" if int(r["n_builds"]) < most else ""))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("%DTC (mean over builds)")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8, frameon=False)
    ax.set_title("%DTC per method and budget (test split; error bars = std over seeds; * = one seed)", fontsize=9)
    return _save(fig, path)


def fig_sapfdc_box_10(test, methods, path, budget=GAP_BUDGET):
    """Box plots of the per-build SAPFDc (mean over seeds) at the 10% budget; triangle = mean."""
    avg = st.seed_average(test[test["method"].isin(methods)], ["sapfdc"])
    avg = avg[np.isclose(avg["budget"], budget)]
    methods = [m for m in _ordered(methods) if m in set(avg["method"])]
    data = [avg.loc[avg["method"] == m, "value"].to_numpy() for m in methods]
    fig, ax = plt.subplots(figsize=(7, 0.45 * len(methods) + 1.2))
    ax.boxplot(data, vert=False, widths=0.6, showmeans=True, patch_artist=True,
               boxprops={"facecolor": "lightgray", "edgecolor": "black"}, medianprops={"color": "black"},
               meanprops={"marker": "^", "markerfacecolor": "white", "markeredgecolor": "black"},
               flierprops={"marker": "o", "markersize": 3, "markerfacecolor": "none", "markeredgecolor": "black"})
    ax.set_yticks(np.arange(1, len(methods) + 1))
    ax.set_yticklabels(methods, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel(f"SAPFDc per build at the {budget:.0%} budget (mean over seeds)")
    ax.set_xlim(-0.02, max(1.05, max((float(np.max(v)) for v in data if len(v)), default=1.0) + 0.02))
    ax.set_title("Per-build SAPFDc (box = quartiles, line = median, triangle = mean)", fontsize=9)
    return _save(fig, path)


def fig_ablation(ablation, path):
    """Change in %DTC and SAPFDc when one component is removed (ablation − Full system), per budget."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    abls = list(dict.fromkeys(ablation["ablation"]))
    budgets = sorted(ablation["budget"].unique())
    x = np.arange(len(budgets))
    width = 0.8 / len(abls)
    for ax, metric in zip(axes, GAP_METRICS):
        for i, a in enumerate(abls):
            sub = ablation[(ablation["ablation"] == a) & (ablation["metric"] == metric)].set_index("budget")
            sub = sub.reindex(budgets)
            removed = sub["removed_component"].dropna().iloc[0]
            n = int(sub["n_builds"].dropna().iloc[0])
            flat = bool(np.allclose(sub["change_when_removed"].fillna(0), 0))
            _bar(ax, x + (i - (len(abls) - 1) / 2) * width, sub["change_when_removed"].fillna(0), STYLES[i],
                 width=width, label=f"without {removed} ({a}, {n} builds)" + (": no change" if flat else ""))
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([f"{b:.0%}" for b in budgets])
        ax.set_xlabel("budget")
        ax.set_title(f"{METRIC_NAMES[metric]}: ablation − Full system", fontsize=9)
    axes[0].set_ylabel("change in mean (negative = component helps)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=8, frameon=False, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.12))
    return _save(fig, path)


def fig_latency_breakdown(eff, path):
    """Stacked bars: mean seconds per build in relevance, orchestrator and explainer calls."""
    e = eff.dropna(subset=["relevance_latency_s", "orchestrator_latency_s"]).copy()
    e["explanation_latency_s"] = e["explanation_latency_s"].fillna(0.0)
    parts = [("relevance_latency_s", "relevance (LLM)"), ("orchestrator_latency_s", "orchestrator"),
             ("explanation_latency_s", "explainer (when on)")]
    fig, ax = plt.subplots(figsize=(8, 0.5 * len(e) + 1.5))
    y = np.arange(len(e))
    left = np.zeros(len(e))
    for i, (col, label) in enumerate(parts):
        face, hatch = STYLES[i]
        ax.barh(y, e[col].to_numpy(), left=left, color=face, hatch=hatch, edgecolor="black", linewidth=0.7,
                label=label)
        left += e[col].to_numpy()
    for yi, total in zip(y, left):
        ax.text(total + left.max() * 0.01, yi, f"{total:.1f} s", va="center", fontsize=8)
    ax.set_xlim(0, left.max() * 1.15)
    ax.set_yticks(y)
    ax.set_yticklabels(e["method"], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("mean seconds per build (all three budgets)")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    missing = sorted(set(eff["method"]) - set(e["method"]))
    title = "LLM time per build by component"
    if missing:
        title += ("\n(not shown: " + ", ".join(missing) + "; its relevance and orchestrator time "
                  "cannot be separated in the committed files)")
    ax.set_title(title, fontsize=9)
    return _save(fig, path)


def fig_agent_w_hist(decisions, path):
    """Histogram of the w chosen by the orchestrator, per relevance source; dashed line = DANTE's 2/3."""
    srcs = list(dict.fromkeys(decisions["relevance_source"]))
    grid = np.round(np.arange(0, 1.0001, 0.1), 1)
    width = 0.08 / max(len(srcs), 1)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for i, src in enumerate(srcs):
        w = decisions.loc[decisions["relevance_source"] == src, "w"].astype(float).round(1)
        counts = w.value_counts().reindex(grid, fill_value=0)
        _bar(ax, grid + (i - (len(srcs) - 1) / 2) * width, counts.to_numpy(), STYLES[i], width=width,
             label=f"{SOURCE_METHODS.get(src, src)} ({len(w)} decisions)")
    ax.axvline(DANTE_W, color="black", linestyle="--", linewidth=1, label="DANTE's fixed w = 2/3")
    ax.set_xticks(grid)
    ax.set_xlabel("w chosen by the orchestrator (weight of history; 1 − w = relevance)")
    ax.set_ylabel("decisions (builds × seeds)")
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.set_title("Distribution of the agent's w (test split)", fontsize=9)
    return _save(fig, path)


# ----------------------------------------------------------------- output ----

def _fmt(x, digits=3):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    if isinstance(x, (bool, np.bool_)):
        return "yes" if x else "no"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        return f"{x:.{digits}f}"
    return str(x)


def _md_table(df, cols):
    """cols: list of (column or callable(row), header, digits)."""
    lines = ["| " + " | ".join(h for _, h, _ in cols) + " |", "|" + "---|" * len(cols)]
    for r in df.to_dict("records"):
        cells = [str(c(r)) if callable(c) else _fmt(r[c], d) for c, _, d in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _pct(b):
    return "—" if b is None or (isinstance(b, float) and np.isnan(b)) else f"{b:.0%}"


def _pm(r, m):
    return f"{r[m + '_mean']:.3f} ± {_fmt(r[m + '_std'])}"


def _write(df, tables_dir, name, title, intro, cols):
    out = Path(tables_dir)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"{name}.csv", index=False)
    text = f"# {title}\n\n{intro}\n\n{_md_table(df, cols)}\n"
    (out / f"{name}.md").write_text(text, encoding="utf-8")


def write_tables(t, tables_dir, notes):
    src = "Written by `python -m src.eval.report`."
    _write(t["main_results"], tables_dir, "main_results", "Main results (test split)",
           f"{src} %DTC and SAPFDc: mean over builds of the per-build mean over seeds ± std over seeds "
           "(`results/stats/seed_variability.csv`; — = one seed). APFDc of the full ranking and SDS: median "
           "over builds. APFDc follows DANTE's formula, which adds 1/(2n); SAPFDc = %DTC × APFDc of the "
           "selection can therefore exceed 1 slightly on small selections (`src/eval/metrics.py`).",
           [("method", "Method", 0), (lambda r: _pct(r["budget"]), "Budget", 0), ("seeds", "Seeds", 0),
            ("n_builds", "Builds", 0), (lambda r: _pm(r, "dtc"), "%DTC", 0),
            (lambda r: _pm(r, "sapfdc"), "SAPFDc", 0), ("apfdc_median", "APFDc (median)", 3),
            ("sds_median", "SDS (median)", 3)])
    gap_cols = [(lambda r: METRIC_NAMES[r["metric"]], "Metric", 0), (lambda r: _pct(r["budget"]), "Budget", 0),
                ("target_mean", "Target mean", 3), ("other", "Other", 0), ("other_mean", "Other mean", 3),
                ("mean_diff", "Mean diff", 3), (lambda r: f"{r['wins']}/{r['ties']}/{r['losses']}", "W/T/L", 0),
                ("p_holm", "p (Holm)", 4), ("significant", "Sig.", 0), ("effect_r", "r", 3)]
    _write(t["gap1"], tables_dir, "gap1", "Gap 1: LLM-relevance vs DANTE (RQ1)",
           f"{src} From `results/stats/pairwise.csv` (family RQ1) and `main_results`. Mean diff = target − "
           f"other over the shared builds; r > 0 = target better.\n\n{notes['recall']}", gap_cols)
    _write(t["gap3"], tables_dir, "gap3", "Gap 3: Agent-weighted vs DANTE and the tuned weight (RQ3)",
           f"{src} From `results/stats/pairwise.csv` (family RQ3) and `main_results`. The agent's w is in "
           "`gap3_w`.", gap_cols)
    _write(t["gap3_w"], tables_dir, "gap3_w", "Gap 3: the w chosen by the orchestrator",
           f"{src} From `orchestrator_decisions.csv` of the test-split runs; one decision per build, relevance "
           "source and run. DANTE's fixed weight is w = 2/3.",
           [("relevance_source", "Relevance source", 0), ("methods", "Methods", 0), ("runs", "Runs", 0),
            ("decisions", "Decisions", 0), ("w_min", "min", 2), ("w_q1", "Q1", 2), ("w_median", "median", 2),
            ("w_q3", "Q3", 2), ("w_max", "max", 2), ("w_mean", "mean", 3), ("distinct_w", "distinct w", 0),
            ("share_w_dante", "share w = 2/3", 3), ("fallback_share", "fallback share", 3)])
    _write(t["gap2"], tables_dir, "gap2", "Gap 2: explanation cost vs time saved, and rating (RQ2)",
           f"{src} Latency: `Full system` rows of the runs with the explainer on ({notes['gap2_runs']}); "
           "overhead = decision (relevance + orchestrator) + explanation time of the build at that budget; "
           "time saved = total suite time − selected time; \"Overhead < saved\" counts build-budget pairs (the overall "
           "row pools the three budgets). Ratings: `results/gap2/rating_summary.csv`.",
           [("scope", "Scope", 0), (lambda r: _pct(r["budget"]), "Budget", 0), ("n_builds", "Builds", 0),
            ("mean_decision_s", "Decision s", 1), ("mean_explanation_s", "Explanation s", 1),
            ("mean_overhead_s", "Overhead s", 1), ("mean_time_saved_s", "Time saved s", 1),
            (lambda r: f"{int(r['pairs_overhead_below_saved'])}/{int(r['n_pairs'])}", "Overhead < saved", 0),
            ("n_rated", "Rated", 0), ("share_sound", "Sound", 3), ("share_partly", "Partly", 3),
            ("share_unsound", "Unsound", 3), ("kappa", "kappa", 3)])
    _write(t["ablation"], tables_dir, "ablation", "Ablations (E5): Full system vs each ablation",
           f"{src} Paired on the builds and seeds both methods have; change = ablation − Full system "
           "(negative = the removed component helps). p (Holm) and r from `results/stats/pairwise.csv` "
           "(family E5, r > 0 = Full system better) where that pair is tested there; — otherwise. The explainer "
           "never changes the "
           "selection, so removing it changes only cost.",
           [("ablation", "Ablation", 0), ("removed_component", "Removed", 0),
            (lambda r: METRIC_NAMES[r["metric"]], "Metric", 0), (lambda r: _pct(r["budget"]), "Budget", 0),
            ("seeds", "Seeds", 0), ("n_builds", "Builds", 0), ("full_mean", "Full system", 3),
            ("ablation_mean", "Ablation", 3), ("change_when_removed", "Change", 3), ("p_holm", "p (Holm)", 4),
            ("effect_r", "r", 3)])
    _write(t["efficiency"], tables_dir, "efficiency", "Efficiency and reliability (E6)",
           f"{src} Per build and run. Decision = relevance + orchestrator calls (tokens are for these calls; "
           "explainer tokens are in `explanations.csv`). Latencies are the original ones, also for answers "
           "taken from the LLM cache. Explainer columns use only runs with the explainer on. Fallback rate = "
           "share of builds whose relevance used the DANTE fallback or whose orchestrator fell back. "
           "GPU-hours = wall-clock hours of the runs containing the method (T4×2 session, `run_meta.json`); "
           f"a run is shared by all its methods, so these hours are not exclusive. {notes['gpu']}",
           [("method", "Method", 0), ("build_runs", "Builds × runs", 0), ("llm_calls_per_build", "LLM calls", 1),
            ("cached_call_share", "Cached share", 3), ("tool_calls_per_build", "Tool calls", 2),
            ("prompt_tokens_per_build", "Prompt tokens", 0), ("completion_tokens_per_build", "Completion tokens", 0),
            ("decision_latency_s", "Decision s", 1), ("relevance_latency_s", "Relevance s", 1),
            ("orchestrator_latency_s", "Orchestrator s", 1), ("explanation_latency_s", "Explanation s", 1),
            ("explainer_failed_share", "Explanations failed", 3), ("fallback_rate", "Fallback rate", 3),
            ("gpu_hours", "GPU-hours", 2)])
    _write(t["e2_reproduction"], tables_dir, "e2_reproduction",
           "E2: DANTE reproduced by us vs the replication package (50 Phase 1 builds)",
           f"{src} From `results/E2_stored_phase1_seed1/per_build.csv` and `data_eval/eval_builds.csv` "
           "(`rq1_dante_cch_apfdc`). Rows marked \"taken from the replication package\" are the published "
           "reference; rows marked \"reproduced by us\" are our port. Tolerance 0.02 for APFDc, exact "
           "equality for %DTC.",
           [("metric", "Metric", 0), (lambda r: _pct(r["budget"]), "Budget", 0), ("method", "Method", 0),
            ("source", "Source", 0), ("n_builds", "Builds", 0), ("median", "Median", 4),
            ("median_diff_vs_reference", "Median diff vs reference", 4),
            (lambda r: ("—" if pd.isna(r["builds_within_tolerance"]) else
                        f"{int(r['builds_within_tolerance'])}/{int(r['n_builds'])}"), "Within tolerance", 0)])


def write_gap_resolution(df, tables_dir, notes):
    out = Path(tables_dir)
    df.to_csv(out / "gap_resolution.csv", index=False)
    lines = ["# Gap-resolution table", "",
             "Written by `python -m src.eval.report`. \"Addressed?\" is set only by `resolve_gap`, which applies "
             "the rule fixed in `docs/PROJECT_CONTEXT.md` §8 before the results were seen:", "",
             "- Gaps 1 and 3: **Fully** = the gap method beats every comparison method in its RQ on both %DTC and "
             "SAPFDc at the 10% budget, with Holm-corrected p < 0.05. **Partially** = it beats them on at least "
             "one metric or budget, or the improvement is not significant. **Not** = no improvement anywhere.",
             "- Gap 2: **Fully** = both RQ2 conditions hold. **Partially** = one holds. **Not** = neither holds.",
             "", "How the rule is applied: \"beats\" = a positive mean difference (gap method − comparison method) "
             "over the shared builds; \"no improvement anywhere\" = no positive mean difference against any "
             "comparison method at any metric and budget. RQ2 condition (a) holds when, at every budget, the mean "
             "decision + explanation time per build is below the mean test time saved per build; the number of "
             "builds where it holds is shown for reference. Condition (b) holds when at least 80% of the sampled "
             "justifications are rated sound.", "",
             _md_table(df, [(c, h, 0) for c, h in zip(RESOLUTION_COLUMNS, RESOLUTION_HEADERS)]), ""]
    lines += [f"- {n}" for n in notes["evidence"]]
    (out / "gap_resolution.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_figures(t, test, decisions, all_set, figures_dir):
    d = Path(figures_dir)
    return [fig_dtc_by_method(t["main_results"], d / "fig_dtc_by_method.png"),
            fig_sapfdc_box_10(test, all_set, d / "fig_sapfdc_box_10.png"),
            fig_ablation(t["ablation"], d / "fig_ablation.png"),
            fig_latency_breakdown(t["efficiency"], d / "fig_latency_breakdown.png"),
            fig_agent_w_hist(decisions, d / "fig_agent_w_hist.png")]


# -------------------------------------------------------------------- run ----

def check_seed_variability(committed, test):
    """Stop if results/stats/seed_variability.csv does not match the current per_build.csv files."""
    budgets = sorted(committed["budget"].unique())
    fresh = st.seed_variability(test, ["dtc", "sapfdc"], budgets)
    key = ["method", "budget", "metric"]
    a = committed.assign(budget=committed["budget"].round(4)).sort_values(key).reset_index(drop=True)
    b = fresh.assign(budget=fresh["budget"].round(4)).sort_values(key).reset_index(drop=True)
    same = (len(a) == len(b) and a[key].equals(b[key]) and np.allclose(a["mean"], b["mean"], atol=1e-9)
            and np.allclose(a["std"], b["std"], atol=1e-9))
    if not same:
        raise ReportError("results/stats/seed_variability.csv does not match the per_build.csv files; "
                          "rerun python -m src.eval.stats first")


def run(results_dir="results", tables_dir="results/tables", figures_dir="results/figures",
        eval_builds="data_eval/eval_builds.csv", comparisons=None):
    """Regenerate every table and figure; returns the tables as a dict of DataFrames."""
    results_dir = Path(repo_path(results_dir))
    df, metas = load_runs(results_dir)
    test = df[df["split"] == "test"].copy()
    phase1 = df[df["split"] == "phase1"].copy()
    if test.empty:
        raise ReportError("no test-split rows")
    pairwise = _read_csv(results_dir / "stats" / "pairwise.csv", "pairwise statistics")
    seed_var = _read_csv(results_dir / "stats" / "seed_variability.csv", "seed variability")
    ratings = _read_csv(results_dir / "gap2" / "rating_summary.csv", "rating summary")
    recall = _read_csv(results_dir / "analysis" / "shortlist_recall_test.csv", "shortlist recall")
    evb = _read_csv(repo_path(eval_builds), "eval_builds.csv")
    check_seed_variability(seed_var, test)
    test_runs = sorted(test["run_id"].unique())
    decisions = load_decisions(results_dir, test_runs)

    t = {"main_results": main_results(test, seed_var)}
    t["gap1"] = gap_comparison(pairwise, t["main_results"], GAP_FAMILIES[1])
    t["gap3"] = gap_comparison(pairwise, t["main_results"], GAP_FAMILIES[3])
    t["gap3_w"] = w_distribution(decisions)
    t["gap2"] = gap2_table(test, ratings)
    t["ablation"] = ablation_table(test, pairwise)
    t["efficiency"] = efficiency(test, decisions, metas)
    t["e2_reproduction"] = e2_reproduction(phase1, evb)
    overall = ratings[ratings["scope"] == "overall"].iloc[0]
    t["gap_resolution"] = gap_resolution(t["main_results"], pairwise, t["gap2"], overall)

    k10 = recall[recall["k"] == 10]
    llm_runs = [r for r in test_runs if r in metas and metas[r].get("provider") != "mock"]
    dev_runs = [r for r, m in metas.items() if m.get("split") == "dev"]
    gap2_runs = ", ".join(f"`results/{r}/per_build.csv`" for r in t["gap2"]["runs"].iloc[0].split(";"))
    notes = {
        "recall": (f"Shortlist recall at k = 10 (the k used; `results/analysis/shortlist_recall_test.csv`): mean "
                   f"{k10['recall'].mean():.3f} over {k10['build'].nunique()} builds; a failing test outside the "
                   "shortlist gets LLM relevance 0."),
        "gap2_runs": gap2_runs,
        "gpu": (f"All test-split runs with the model: {sum(run_hours(metas[r]) for r in llm_runs):.2f} h "
                f"({len(llm_runs)} runs); dev-split runs: {sum(run_hours(metas[r]) for r in dev_runs):.2f} h "
                f"({len(dev_runs)} runs)."),
        "evidence": [
            "Gap 1 evidence: `results/stats/pairwise.csv` (family RQ1), `results/tables/gap1.md`, "
            "`results/tables/main_results.csv`.",
            f"Gap 2 evidence: `results/tables/gap2.md` (from {gap2_runs}), `results/gap2/rating_summary.csv`, "
            "`results/gap2/agreement.md`.",
            "Gap 3 evidence: `results/stats/pairwise.csv` (family RQ3), `results/tables/gap3.md`, "
            "`results/tables/gap3_w.md` (from `orchestrator_decisions.csv` of the test-split runs)."]}
    write_tables(t, repo_path(tables_dir), notes)
    write_gap_resolution(t["gap_resolution"], repo_path(tables_dir), notes)
    all_set = st.load_comparisons(comparisons)["friedman_sets"]["ALL"]
    write_figures(t, test, decisions, all_set, repo_path(figures_dir))
    return t


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m src.eval.report", description=__doc__.split("\n\n")[0])
    p.add_argument("--results", default="results")
    p.add_argument("--tables", default="results/tables")
    p.add_argument("--figures", default="results/figures")
    p.add_argument("--eval-builds", default="data_eval/eval_builds.csv")
    p.add_argument("--comparisons", default=None, help="default: experiments/comparisons.yaml")
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        t = run(args.results, args.tables, args.figures, args.eval_builds, args.comparisons)
    except ReportError as e:
        log.error("%s", e)
        return 1
    for r in t["gap_resolution"].drop_duplicates("gap").itertuples(index=False):
        log.info("%s: %s", r.gap, r.addressed)
    log.info("tables written to %s, figures to %s", args.tables, args.figures)
    return 0


if __name__ == "__main__":
    sys.exit(main())
