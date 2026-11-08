"""Tests for src/eval/report.py (P2-19). No data and no model: small hand-made inputs only."""
import json
import shutil
import zlib

import numpy as np
import pandas as pd
import pytest

from src.eval import report as rp
from src.eval import stats as st
from src.pipeline import DECISION_COLUMNS, PER_BUILD_COLUMNS

BUDGETS = [0.05, 0.1, 0.2]


# ------------------------------------------------------------ resolve_gap ----

def _pw(family, rows):
    """pairwise.csv rows: (other, metric, budget, mean_diff, p_holm)."""
    return pd.DataFrame([{"family": family, "target": "T", "other": o, "metric": m, "budget": b, "mean_diff": d,
                          "p_holm": p} for o, m, b, d, p in rows])


def _all(family, at10, elsewhere=(-0.01, 0.5), others=("A", "B")):
    """Every other × metric × budget; at10 = {(other, metric): (diff, p)} for the 10% budget."""
    rows = []
    for o in others:
        for m in ("dtc", "sapfdc"):
            for b in BUDGETS:
                d, p = at10[(o, m)] if b == 0.1 else elsewhere
                rows.append((o, m, b, d, p))
    return _pw(family, rows)


def _gap(gap, pw):
    return rp.resolve_gap(gap, {"pairwise": pw}, None)


def test_fully_when_every_comparison_is_a_significant_win_on_both_metrics_at_10():
    at10 = {(o, m): (0.05, 0.01) for o in "AB" for m in ("dtc", "sapfdc")}
    assert _gap(1, _all("RQ1", at10)) == "Fully"          # losses at 5% and 20% do not matter


def test_significant_win_on_only_one_metric_is_partially():
    at10 = {("A", "dtc"): (0.05, 0.01), ("B", "dtc"): (0.05, 0.01),
            ("A", "sapfdc"): (0.02, 0.30), ("B", "sapfdc"): (0.02, 0.30)}
    assert _gap(1, _all("RQ1", at10)) == "Partially"


def test_wins_that_are_not_significant_are_partially():
    at10 = {(o, m): (0.05, 0.20) for o in "AB" for m in ("dtc", "sapfdc")}
    assert _gap(1, _all("RQ1", at10)) == "Partially"


def test_beating_only_one_comparison_method_is_partially():
    at10 = {("A", "dtc"): (0.05, 0.01), ("A", "sapfdc"): (0.05, 0.01),
            ("B", "dtc"): (-0.05, 0.01), ("B", "sapfdc"): (-0.05, 0.01)}
    assert _gap(1, _all("RQ1", at10)) == "Partially"


def test_improvement_only_at_another_budget_is_partially():
    at10 = {(o, m): (-0.02, 0.5) for o in "AB" for m in ("dtc", "sapfdc")}
    pw = _all("RQ1", at10)
    pw.loc[(pw["budget"] == 0.05) & (pw["metric"] == "dtc") & (pw["other"] == "A"), "mean_diff"] = 0.03
    assert _gap(1, pw) == "Partially"


def test_no_improvement_anywhere_is_not():
    at10 = {(o, m): (0.0, 1.0) for o in "AB" for m in ("dtc", "sapfdc")}
    assert _gap(1, _all("RQ1", at10, elsewhere=(-0.02, 0.4))) == "Not"


def test_p_exactly_alpha_is_not_significant():
    at10 = {(o, m): (0.05, 0.05) for o in "AB" for m in ("dtc", "sapfdc")}
    assert _gap(3, _all("RQ3", at10)) == "Partially"


def test_gap3_reads_only_its_own_family():
    good = _all("RQ1", {(o, m): (0.05, 0.01) for o in "AB" for m in ("dtc", "sapfdc")})
    bad = _all("RQ3", {(o, m): (-0.05, 0.01) for o in "AB" for m in ("dtc", "sapfdc")}, elsewhere=(-0.01, 0.5))
    pw = pd.concat([good, bad], ignore_index=True)
    assert _gap(1, pw) == "Fully"
    assert _gap(3, pw) == "Not"


@pytest.mark.parametrize("overhead, sound, expected", [
    ([10, 10, 10], 0.85, "Fully"),
    ([10, 10, 10], 0.64, "Partially"),
    ([10, 10, 500], 0.85, "Partially"),      # above the time saved at one budget: condition (a) fails
    ([500, 500, 500], 0.50, "Not"),
    ([10, 10, 10], 0.80, "Fully"),           # 0.80 is enough
])
def test_gap2_conditions(overhead, sound, expected):
    ov = pd.DataFrame({"budget": BUDGETS, "mean_overhead_s": overhead, "mean_time_saved_s": [100, 100, 100]})
    assert rp.resolve_gap(2, {"overhead": ov}, {"share_sound": sound}) == expected


def test_unknown_gap_raises():
    with pytest.raises(rp.ReportError):
        rp.resolve_gap(4, {}, {})


# ----------------------------------------------------------- main_results ----

def _row(**kw):
    r = {c: 0 for c in PER_BUILD_COLUMNS}
    r.update({"split": "test", "experiment": "E9", "relevance_source": "none", "weight_mode": "fixed",
              "ranking_source": "dante", "w": np.nan, "sds": 0.5, "apfdc_full": 0.7})
    r.update(kw)
    if not kw.get("run_id"):
        r["run_id"] = f"E9_test_seed{r['seed']}"
    return r


def test_main_results_mean_and_std_over_two_seeds():
    rows = []
    for seed, vals in ((1, {"b1": 0.2, "b2": 0.4}), (2, {"b1": 0.4, "b2": 0.6})):
        rows += [_row(seed=seed, build=b, budget=0.1, method="M", dtc=v, sapfdc=v / 2) for b, v in vals.items()]
    rows += [_row(seed=1, build=b, budget=0.1, method="N", dtc=0.5, sapfdc=0.25) for b in ("b1", "b2")]
    df = pd.DataFrame(rows)
    out = rp.main_results(df).set_index("method")
    assert out.loc["M", "dtc_mean"] == pytest.approx(0.4)                 # per-seed means 0.3 and 0.5
    assert out.loc["M", "dtc_std"] == pytest.approx(np.std([0.3, 0.5], ddof=1))
    assert out.loc["M", "sapfdc_mean"] == pytest.approx(0.2)
    assert out.loc["M", "seeds"] == 2 and out.loc["M", "n_builds"] == 2
    assert np.isnan(out.loc["N", "dtc_std"])                              # one seed: no std
    assert out.loc["N", "apfdc_median"] == pytest.approx(0.7)


def test_seed_averaging_happens_per_build_first():
    rows = [_row(seed=1, build="b1", budget=0.1, method="M", dtc=0.2, sapfdc=0.1),
            _row(seed=2, build="b1", budget=0.1, method="M", dtc=0.4, sapfdc=0.1)]
    out = rp.main_results(pd.DataFrame(rows))
    assert out["dtc_mean"].iloc[0] == pytest.approx(0.3)


# ------------------------------------------------- end-to-end on fake files ----

METHODS = {  # method: (run group, relevance_source, weight_mode, seeds)
    "Random": ("E1", "none", "random", (1, 2, 3)), "History-only": ("E1", "none", "history_only", (1, 2, 3)),
    "TF-IDF-only": ("E1", "tfidf", "relevance_only", (1, 2, 3)),
    "Tuned-weight (TF-IDF)": ("E1", "tfidf", "tuned", (1, 2, 3)),
    "Single-call LLM": ("E1", "llm_single_call", "fixed", (1, 2, 3)),
    "DANTE-CCH": ("E3", "tfidf", "fixed", (1, 2, 3)), "DANTE-CCH-shipped": ("E3", "tfidf", "fixed", (1, 2, 3)),
    "LLM-relevance": ("E3", "llm_shortlist", "fixed", (1, 2, 3)),
    "Tuned-weight (LLM)": ("E3", "llm_shortlist", "tuned", (1, 2, 3)),
    "Agent-weighted": ("E3", "llm_shortlist", "agent", (1, 2, 3)),
    "Full system": ("E3", "llm_shortlist", "agent", (1, 2, 3)),
    "Agent-weighted (TF-IDF)": ("E5", "tfidf", "agent", (1, 2, 3)),
    "Full system (no shortlist)": ("E5noshort", "llm_all_individual", "agent", (1,)),
}
BUILDS = [f"B{i}" for i in range(1, 9)]
REL_S, ORCH_S, EXPL_S = 10.0, 2.0, 3.0


def _value(*key):
    """Deterministic pseudo-random value in [0, 1) for a key (same in every seed)."""
    return (zlib.crc32("|".join(map(str, key)).encode()) % 1000) / 1000


def _fake_rows(run_id, split, seed, method, src, mode, builds):
    rows = []
    for i, b in enumerate(builds):
        llm = src in rp.LLM_SOURCES
        rel = REL_S + i if llm else 0.0
        dec = rel + (ORCH_S if mode == "agent" else 0.0)
        for budget in BUDGETS:
            v = _value(method, b, budget) * 0.5 + budget
            expl = method == "Full system" and seed == 1
            rows.append(_row(run_id=run_id, experiment=run_id.split("_")[0], split=split, seed=seed, build=b,
                             budget=budget, method=method, relevance_source=src, weight_mode=mode,
                             ranking_source="llm" if llm else "dante", dtc=v, sapfdc=v * 0.8, sds=0.5,
                             apfdc_full=_value(method, b), total_duration_s=1000.0,
                             selected_duration_s=900 * budget, time_saved_s=1000 - 900 * budget,
                             llm_calls=(5 if llm else 0) + (1 if mode == "agent" else 0),
                             llm_cached_calls=1 if llm else 0, llm_latency_s=dec, decision_latency_s=dec,
                             prompt_tokens=100 if llm else 0, completion_tokens=10 if llm else 0,
                             explainer_calls=2 if expl else 0, explainer_latency_s=EXPL_S if expl else 0.0,
                             explainer_ok=1 if expl else 0, w=0.3 if mode == "agent" else np.nan))
    return rows


def _write_run(root, run_id, split, seed, rows, decisions=None, provider="ollama"):
    d = root / run_id
    d.mkdir(parents=True)
    pd.DataFrame(rows, columns=PER_BUILD_COLUMNS).to_csv(d / "per_build.csv", index=False)
    if decisions is not None:
        pd.DataFrame(decisions, columns=DECISION_COLUMNS).to_csv(d / "orchestrator_decisions.csv", index=False)
    meta = {"run_id": run_id, "split": split, "seed": seed, "provider": provider,
            "started": "2026-11-07T10:00:00+00:00", "finished": "2026-11-07T11:30:00+00:00"}
    (d / "run_meta.json").write_text(json.dumps(meta), encoding="utf-8")


def _make_fake_results(tmp_path):
    root = tmp_path / "results"
    groups = {}
    for method, (group, src, mode, seeds) in METHODS.items():
        for seed in seeds:
            groups.setdefault((group, seed), []).append((method, src, mode))
    for (group, seed), specs in groups.items():
        run_id = f"{group}_test_seed{seed}"
        builds = BUILDS[:4] if group == "E5noshort" else BUILDS
        rows, decisions = [], []
        for method, src, mode in specs:
            rows += _fake_rows(run_id, "test", seed, method, src, mode, builds)
            if mode == "agent" and not any(d["relevance_source"] == src for d in decisions):
                decisions += [{"build": b, "relevance_source": src, "w": 0.3 if i % 2 else 0.7, "confidence": 0.8,
                               "source": "agent", "steps": 1, "llm_calls": 1, "tool_calls": 0, "reason": "r",
                               "fallback_reason": None} for i, b in enumerate(builds)]
        _write_run(root, run_id, "test", seed, rows, decisions or None)
    p1 = [f"P{i}" for i in range(1, 6)]
    rows = []
    for m in ("DANTE-CCH", "DANTE-CCH-shipped", "DANTE-CCH (stored)"):
        rows += _fake_rows("E2_stored_phase1_seed1", "phase1", 1, m, "tfidf", "fixed", p1)
    for r in rows:
        if r["method"] == "DANTE-CCH (stored)":
            r["apfdc_full"] = np.nan                       # a stored solution has no full ranking
    _write_run(root, "E2_stored_phase1_seed1", "phase1", 1, rows, provider="mock")
    paths = sorted(str(p) for p in root.glob("*_test_seed*/per_build.csv"))
    st.run(paths, root / "stats")
    (root / "gap2").mkdir()
    pd.DataFrame([{"scope": "overall", "budget": None, "n": 100, "share_sound": 0.64, "share_partly": 0.06,
                   "share_unsound": 0.30, "kappa": 0.7, "rq2_sound_condition_holds": False}] +
                 [{"scope": "budget", "budget": b, "n": 33, "share_sound": 0.6, "share_partly": 0.1,
                   "share_unsound": 0.3, "kappa": 0.7, "rq2_sound_condition_holds": None} for b in BUDGETS]
                 ).to_csv(root / "gap2" / "rating_summary.csv", index=False)
    (root / "analysis").mkdir()
    pd.DataFrame([{"build": b, "k": k, "n_failing": 2, "n_in_shortlist": 1, "recall": 0.5, "shortlist_size": 2 * k}
                  for b in BUILDS for k in (5, 10)]).to_csv(root / "analysis" / "shortlist_recall_test.csv",
                                                             index=False)
    pd.DataFrame({"key": p1, "rq1_dante_cch_apfdc": [_value("DANTE-CCH-shipped", b) for b in p1]}).to_csv(
        tmp_path / "eval_builds.csv", index=False)
    return tmp_path


def _run(tmp):
    return rp.run(tmp / "results", tmp / "tables", tmp / "figures", tmp / "eval_builds.csv")


@pytest.fixture(scope="module")
def fake_results(tmp_path_factory):
    """A fake results tree (statistics by the real src.eval.stats); the report is run once on it."""
    tmp = _make_fake_results(tmp_path_factory.mktemp("report"))
    return tmp, _run(tmp)


def test_one_command_writes_every_table_and_figure(fake_results):
    fake_results, t = fake_results
    names = ["main_results", "gap1", "gap3", "gap3_w", "gap2", "ablation", "efficiency", "e2_reproduction",
             "gap_resolution"]
    for n in names:
        assert (fake_results / "tables" / f"{n}.csv").stat().st_size > 0
        assert (fake_results / "tables" / f"{n}.md").stat().st_size > 0
    for f in ("fig_dtc_by_method", "fig_sapfdc_box_10", "fig_ablation", "fig_latency_breakdown", "fig_agent_w_hist"):
        assert (fake_results / "figures" / f"{f}.png").stat().st_size > 0
    gr = t["gap_resolution"]
    assert list(gr.columns) == rp.RESOLUTION_COLUMNS
    assert list(gr["gap"]) == ["Gap 1", "Gap 1", "Gap 2", "Gap 2", "Gap 3", "Gap 3"]
    assert set(gr["addressed"]) <= {"Fully", "Partially", "Not"}
    assert gr.loc[gr["gap"] == "Gap 2", "addressed"].iloc[0] == "Partially"     # time holds, 0.64 < 0.80
    stats_in = {"pairwise": pd.read_csv(fake_results / "results" / "stats" / "pairwise.csv")}
    for g in (1, 3):
        assert gr.loc[gr["gap"] == f"Gap {g}", "addressed"].iloc[0] == rp.resolve_gap(g, stats_in, None)
    header = (fake_results / "tables" / "gap_resolution.md").read_text(encoding="utf-8")
    assert "| Gap | Method/component | Metric |" in header and "Addressed?" in header


def test_tables_on_fake_files(fake_results):
    _, t = fake_results
    main = t["main_results"].set_index(["method", "budget"])
    assert set(t["main_results"]["method"]) == set(METHODS)                  # phase1-only method not included
    assert main.loc[("Full system (no shortlist)", 0.1), "n_builds"] == 4
    assert np.isnan(main.loc[("Full system (no shortlist)", 0.1), "dtc_std"])
    eff = t["efficiency"].set_index("method")
    assert eff.loc["Full system", "relevance_latency_s"] == pytest.approx(REL_S + 3.5)   # mean of 10 + i, i = 0..7
    assert eff.loc["Full system", "orchestrator_latency_s"] == pytest.approx(ORCH_S)
    assert eff.loc["Full system", "explanation_latency_s"] == pytest.approx(3 * EXPL_S)  # 3 budgets, seed 1 only
    assert eff.loc["Full system", "explainer_runs"] == 1
    assert eff.loc["Agent-weighted (TF-IDF)", "relevance_latency_s"] == 0.0
    assert np.isnan(eff.loc["Full system (no shortlist)", "relevance_latency_s"])         # no plain method in run
    assert eff.loc["Full system", "fallback_rate"] == 0.0
    assert eff.loc["Full system", "gpu_hours"] == pytest.approx(4.5)                      # 3 runs × 1.5 h
    g2 = t["gap2"]
    assert list(g2["scope"]) == ["budget"] * 3 + ["overall"]
    assert g2["n_pairs"].tolist() == [8, 8, 8, 24]
    abl = t["ablation"]
    expl = abl[abl["ablation"] == "Agent-weighted"]
    assert np.allclose(expl["change_when_removed"], _expected_change("Agent-weighted", expl))
    ns = abl[abl["ablation"] == "Full system (no shortlist)"]
    assert set(ns["n_builds"]) == {4} and set(ns["seeds"]) == {"1"}
    e2 = t["e2_reproduction"]
    shipped = e2[(e2["metric"] == "APFDc (full ranking)") & (e2["method"] == "DANTE-CCH-shipped")].iloc[0]
    assert shipped["median_diff_vs_reference"] == pytest.approx(0.0) and shipped["builds_within_tolerance"] == 5
    w = t["gap3_w"].set_index("relevance_source")
    assert w.loc["llm_shortlist", "decisions"] == 24 and w.loc["llm_shortlist", "distinct_w"] == 2


def _expected_change(method, rows):
    out = []
    for r in rows.itertuples(index=False):
        f = np.mean([_value("Full system", b, r.budget) for b in BUILDS])
        a = np.mean([_value(method, b, r.budget) for b in BUILDS])
        out.append((a - f) * 0.5 * (0.8 if r.metric == "sapfdc" else 1.0))
    return out


def test_stale_statistics_stop_the_report(fake_results, tmp_path):
    shutil.copytree(fake_results[0], tmp_path / "copy")
    tmp = tmp_path / "copy"
    p = tmp / "results" / "stats" / "seed_variability.csv"
    sv = pd.read_csv(p)
    sv.loc[0, "mean"] += 0.1
    sv.to_csv(p, index=False)
    with pytest.raises(rp.ReportError, match="out of date|does not match"):
        _run(tmp)


def test_every_figure_function_writes_a_png(fake_results, tmp_path):
    fake_results, t = fake_results
    test = pd.concat(pd.read_csv(p) for p in (fake_results / "results").glob("*_test_seed*/per_build.csv"))
    test["budget"] = test["budget"].round(4)
    decisions = rp.load_decisions(fake_results / "results", sorted(test["run_id"].unique()))
    out = tmp_path / "figs"
    paths = [rp.fig_dtc_by_method(t["main_results"], out / "a.png"),
             rp.fig_sapfdc_box_10(test, list(METHODS), out / "b.png"),
             rp.fig_ablation(t["ablation"], out / "c.png"),
             rp.fig_latency_breakdown(t["efficiency"], out / "d.png"),
             rp.fig_agent_w_hist(decisions, out / "e.png")]
    for p in paths:
        assert p.stat().st_size > 1000
