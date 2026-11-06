"""Pipeline (P2-15) on the synthetic build from tests/test_end_to_end.py, with fakes (no data, no model)."""
import csv
import json
from types import SimpleNamespace

import pytest

from src.agent.llm_provider import LLMTimeout, MockProvider
from src.contracts import validate
from src.dante import rank
from src.pipeline import (DECISION_COLUMNS, EXPLANATION_COLUMNS, LLM_RELEVANCE_COLUMNS, PER_BUILD_COLUMNS,
                          Components, RunContext, load_method_specs, load_tuned_weights, run_build, run_builds)
from src.settings import load_config
from tests.fakes import FakeExplainer, FakeOrchestrator, FakeSingleCallScorer
from tests.test_end_to_end import FakeLoader, _fixture

BUDGETS = [0.1, 0.5]
TUNED = {"tfidf": {"w": 0.5}, "llm": {"w": 0.4}}


def relevance_answer(prompt):
    test = prompt.split("Test class `", 1)[1].split("`", 1)[0]
    return json.dumps({"test": test, "relevance": 0.5, "reason": "mock", "confidence": 1.0})


def _cfg(tmp_path):
    cfg = load_config()
    cfg["paths"]["logs_dir"] = str(tmp_path / "logs")
    return cfg


def _ctx(cfg, tmp_path, seed=1):
    return RunContext.create(cfg, "E0_dev_seed%d" % seed, "E0", "dev", seed, tmp_path / "results")


def _comps(provider=None, orch=None, explainer=None, single=None):
    stored = {"total_failures_in_build": 2, "failures_found": 1, "selected_tests_count": 1,
              "detailed_selection": [{"fqn": "p.a.CacheTest", "duration": 10.0, "did_fail": True}]}
    return Components(relevance_provider=provider or MockProvider([relevance_answer]),
                      orchestrator=orch or FakeOrchestrator(w=0.5), explainer=explainer or FakeExplainer(),
                      single_call=single or FakeSingleCallScorer(0.5), tuned_weights=TUNED,
                      stored_loader=lambda *a: stored)


def _row(in_phase1=False, key="PR-1_build1"):
    return SimpleNamespace(pr_name="PR-1", build_id=1, stage_id="single", key=key, in_phase1=in_phase1,
                           build_name="karaf_build_PR-1_1_single_tfidf_specific_boosted_False")


def _run(tmp_path, specs=None, comps=None, seed=1, in_phase1=False):
    cfg = _cfg(tmp_path)
    ctx = _ctx(cfg, tmp_path, seed)
    build, hist = _fixture()
    res = run_build(cfg, FakeLoader(build, hist), _row(in_phase1), specs or load_method_specs(), BUDGETS,
                    comps or _comps(), ctx)
    return cfg, ctx, res


def _csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _header(path):
    with open(path, encoding="utf-8", newline="") as f:
        return next(csv.reader(f))


def _sel(res, method, budget):
    return next(m for m in res["methods"] if m["method"] == method and m["budget"] == budget)


def test_catalogue_has_the_14_methods():
    names = [s.name for s in load_method_specs()]
    assert len(names) == 14 and names[0] == "Random" and names[-1] == "Full system (no shortlist)"
    assert [s.name for s in load_method_specs(names=["DANTE-CCH", "Random"])] == ["DANTE-CCH", "Random"]


def test_unknown_method_name_lists_valid_names():
    with pytest.raises(ValueError) as e:
        load_method_specs(names=["DANTE-CCH", "Nope"])
    assert "Nope" in str(e.value) and "Full system" in str(e.value) and "Random" in str(e.value)


def test_tuned_weights_missing_file_is_empty(tmp_path):
    assert load_tuned_weights(tmp_path / "missing.yaml") == {}


def test_all_specs_write_every_file_with_exact_columns(tmp_path):
    _, ctx, res = _run(tmp_path, in_phase1=True)
    d = ctx.run_dir
    rows = _csv(d / "per_build.csv")
    assert _header(d / "per_build.csv") == PER_BUILD_COLUMNS
    pairs = [(r["method"], float(r["budget"])) for r in rows]
    assert len(pairs) == len(set(pairs)) == 14 * len(BUDGETS)
    assert {m for m, _ in pairs} == {s.name for s in load_method_specs()}
    assert _header(d / "llm_relevance.csv") == LLM_RELEVANCE_COLUMNS
    assert _header(d / "orchestrator_decisions.csv") == DECISION_COLUMNS
    assert _header(d / "explanations.csv") == EXPLANATION_COLUMNS
    assert (d / "runs" / "PR-1_build1.json").exists()
    json.dumps(res, default=str)
    stored = [r for r in rows if r["method"] == "DANTE-CCH (stored)"]
    assert {r["ranking_source"] for r in stored} == {"stored"} and float(stored[0]["dtc"]) == 0.5


def test_stored_skipped_outside_phase1(tmp_path):
    _, ctx, _ = _run(tmp_path, in_phase1=False)
    rows = _csv(ctx.run_dir / "per_build.csv")
    assert not [r for r in rows if r["method"] == "DANTE-CCH (stored)"]
    assert len(rows) == 13 * len(BUDGETS)


def test_dante_cch_matches_src_dante(tmp_path):
    cfg, _, res = _run(tmp_path, specs=load_method_specs(names=["DANTE-CCH"]))
    build, hist = _fixture()
    for b in BUDGETS:
        sel, order, _ = rank(build, hist, b, cfg, "DANTE-CCH")
        m = _sel(res, "DANTE-CCH", b)
        assert m["selected"] == sel and m["ordered"] == order and m["w"] == pytest.approx(2 / 3)


def test_agent_with_w_1_equals_shipped(tmp_path):
    _, _, res = _run(tmp_path, specs=load_method_specs(names=["Agent-weighted", "DANTE-CCH-shipped"]),
                     comps=_comps(orch=FakeOrchestrator(w=1.0)))
    for b in BUDGETS:
        a, s = _sel(res, "Agent-weighted", b), _sel(res, "DANTE-CCH-shipped", b)
        assert a["selected"] == s["selected"] and a["metrics"] == s["metrics"]
        assert a["ranking_source"] == "llm" and a["w"] == 1.0


def test_shared_work_once_per_build(tmp_path):
    orch, single = FakeOrchestrator(w=0.5), FakeSingleCallScorer(0.5)
    provider = MockProvider([relevance_answer])
    _, ctx, res = _run(tmp_path, comps=_comps(provider=provider, orch=orch, single=single))
    # agent specs use three relevance sources: llm_shortlist (2 specs), tfidf, llm_all_individual
    assert orch.calls == 3 and single.calls == 1
    n_short, n_all = len(res["shortlist"]), res["candidates"]
    assert len(provider.calls) == n_short + n_all       # each LLM relevance source computed once
    decisions = _csv(ctx.run_dir / "orchestrator_decisions.csv")
    assert sorted(r["relevance_source"] for r in decisions) == ["llm_all_individual", "llm_shortlist", "tfidf"]


def test_relevance_timeout_falls_back_to_dante(tmp_path):
    specs = load_method_specs(names=["DANTE-CCH", "LLM-relevance", "Agent-weighted"])
    orch = FakeOrchestrator(w=0.1)
    _, ctx, res = _run(tmp_path, specs=specs, comps=_comps(provider=MockProvider([LLMTimeout("slow")]), orch=orch))
    for b in BUDGETS:
        for name in ("LLM-relevance", "Agent-weighted"):
            m = _sel(res, name, b)
            assert m["ranking_source"] == "dante_fallback"
            assert m["metrics"] == _sel(res, "DANTE-CCH", b)["metrics"]
    rows = [r for r in _csv(ctx.run_dir / "per_build.csv") if r["method"] == "LLM-relevance"]
    assert {r["ranking_source"] for r in rows} == {"dante_fallback"}
    assert orch.calls == 0      # no decision needed when the source fell back


def test_explainer_only_when_enabled_and_for_explainer_specs(tmp_path):
    ex = FakeExplainer()
    _, ctx, res = _run(tmp_path, comps=_comps(explainer=ex), seed=1)     # explainer_seeds: [1]
    assert ctx.explainer_enabled and ex.calls == len(BUDGETS)            # only "Full system"
    expl = _csv(ctx.run_dir / "explanations.csv")
    assert expl and {r["method"] for r in expl} == {"Full system"}
    full = [r for r in _csv(ctx.run_dir / "per_build.csv") if r["method"] == "Full system"]
    assert all(int(r["explainer_calls"]) == len([e for e in expl if float(e["budget"]) == float(r["budget"])])
               for r in full)

    ex2 = FakeExplainer()
    _, ctx2, _ = _run(tmp_path / "s2", comps=_comps(explainer=ex2), seed=2)
    assert not ctx2.explainer_enabled and ex2.calls == 0


def test_costs_and_time_saved(tmp_path):
    _, ctx, res = _run(tmp_path, specs=load_method_specs(names=["Random", "LLM-relevance", "Agent-weighted"]))
    rows = {(r["method"], float(r["budget"])): r for r in _csv(ctx.run_dir / "per_build.csv")}
    n_short = len(res["shortlist"])
    lr, aw, rnd = rows[("LLM-relevance", 0.1)], rows[("Agent-weighted", 0.1)], rows[("Random", 0.1)]
    assert int(lr["llm_calls"]) == n_short and int(rnd["llm_calls"]) == 0
    assert int(aw["llm_calls"]) == n_short + 1          # + the fake orchestrator's one call
    total = float(lr["total_duration_s"])
    assert float(lr["time_saved_s"]) == pytest.approx(total - float(lr["selected_duration_s"]))
    llm_rows = _csv(ctx.run_dir / "llm_relevance.csv")
    assert len(llm_rows) == n_short and {r["prompt_version"] for r in llm_rows} == {"v1"}


def test_failing_build_is_recorded_and_run_continues(tmp_path):
    cfg = _cfg(tmp_path)
    ctx = _ctx(cfg, tmp_path)
    build, hist = _fixture()

    class Loader(FakeLoader):
        def build(self, row, keep_sources=False):
            if row == "bad":
                raise RuntimeError("broken build")
            return super().build(row, keep_sources)

        def row(self, pr_name, *a):
            return "bad" if pr_name == "PR-bad" else {}

    bad = SimpleNamespace(pr_name="PR-bad", build_id=9, stage_id="single", key="PR-bad_build9", in_phase1=False)
    meta = run_builds(cfg, Loader(build, hist), [bad, _row()], load_method_specs(names=["DANTE-CCH"]),
                      BUDGETS, _comps(), ctx, host="test")
    assert meta["n_builds"] == 2 and [f["build"] for f in meta["failed_builds"]] == ["PR-bad_build9"]
    assert "broken build" in meta["failed_builds"][0]["error"]
    assert len(_csv(ctx.run_dir / "per_build.csv")) == len(BUDGETS)    # the good build still ran
    saved = json.loads((ctx.run_dir / "run_meta.json").read_text(encoding="utf-8"))
    for k in ("run_id", "experiment", "split", "seed", "git_commit", "model", "prompt_versions", "config_file",
              "started", "finished", "n_builds", "host", "failed_builds"):
        assert k in saved


def test_decisions_validate(tmp_path):
    _, _, res = _run(tmp_path, specs=load_method_specs(names=["Agent-weighted"]))
    validate(res["decisions"]["llm_shortlist"], "orchestrator_decision")
