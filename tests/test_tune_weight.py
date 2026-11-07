"""Tuned-weight baselines (P2-11) on the synthetic fixture; no data, no model."""
import pandas as pd
import pytest
import yaml
from types import SimpleNamespace

from src.contracts import DANTE_W
from src.dante import rank
from src.dante.scoring import score_table
from src.dante import tune_weight as tw
from src.settings import load_config
from tests.test_end_to_end import FakeLoader, _fixture

CFG = load_config()
BUDGETS = [0.1, 0.5]


def _grid(values):
    """grid rows at budget 0.1 from {w: sapfdc_mean}."""
    return pd.DataFrame([{"w": w, "budget": 0.1, "builds": 3, "dtc_mean": 0.5, "sapfdc_mean": v,
                          "apfdc_median": 0.5} for w, v in values.items()], columns=tw.GRID_COLUMNS)


def test_choose_w_picks_the_highest_objective():
    assert tw.choose_w(_grid({0.0: 0.30, 0.5: 0.45, 0.6666667: 0.40, 1.0: 0.20}), 0.1) == (0.5, 0.45)


def test_choose_w_ties_go_to_the_value_closest_to_two_thirds():
    # 0.3, 0.7 and 0.9 are all within 0.001 of the best (0.4505); 0.7 is closest to 2/3
    w, value = tw.choose_w(_grid({0.3: 0.4505, 0.5: 0.40, 0.7: 0.4498, 0.9: 0.4500}), 0.1)
    assert w == 0.7 and value == pytest.approx(0.4498)
    # just outside the margin: the strict best wins
    assert tw.choose_w(_grid({0.3: 0.4520, 0.7: 0.4509}), 0.1)[0] == 0.3
    # 2/3 itself within the margin is taken
    assert tw.choose_w(_grid({0.2: 0.5000, 0.6666667: 0.4995}), 0.1)[0] == pytest.approx(DANTE_W, abs=1e-6)


def _selection(build, hist, w, b):
    h, d = CFG["history"], CFG["dante"]
    df, _ = score_table(build, hist, h["lookback_windows"], h["min_sticky_events"], w_history=w,
                        w_relevance=1 - w, power=d["relevance_power"])
    return rank(build, hist, b, CFG, "DANTE-CCH", df=df)[0]


def test_two_thirds_equals_dante_and_one_equals_shipped():
    build, hist = _fixture()
    for b in BUDGETS:
        assert _selection(build, hist, 2 / 3, b) == rank(build, hist, b, CFG, "DANTE-CCH")[0]
        assert _selection(build, hist, 1.0, b) == rank(build, hist, b, CFG, "DANTE-CCH-shipped")[0]
    m23 = tw.build_metrics(build, hist, CFG, 2 / 3, BUDGETS)
    dante = tw.build_metrics(build, hist, CFG, 0.0, BUDGETS, fell_back=True)    # the DANTE-CCH path
    assert m23 == dante


def test_fell_back_build_gives_identical_metrics_for_every_w():
    build, hist = _fixture()
    results = [tw.build_metrics(build, hist, CFG, w, BUDGETS, override={"p.a.CacheTest": 1.0}, fell_back=True)
               for w in CFG["tuning"]["w_grid"]]
    assert all(r == results[0] for r in results) and results[0]


def test_llm_override_changes_the_ranking_but_not_without_fall_back():
    build, hist = _fixture()
    plain = tw.build_metrics(build, hist, CFG, 0.0, BUDGETS)
    llm = tw.build_metrics(build, hist, CFG, 0.0, BUDGETS,
                           override={"p.a.CacheTest": 0.0, "p.b.WebTest": 1.0, "p.b.SlowTest": 0.0})
    assert plain != llm                                      # w = 0: relevance alone decides


def test_writing_llm_keeps_the_tfidf_entry(tmp_path):
    path = tmp_path / "tuned_weights.yaml"
    tw.update_weights_file(path, "tfidf", {"w": 0.7, "objective": "sapfdc_mean@0.10", "value": 0.41})
    tw.update_weights_file(path, "llm", {"w": 0.6, "objective": "sapfdc_mean@0.10", "value": 0.43,
                                          "llm_run": "DEV_prompt_v1"})
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["tfidf"]["w"] == 0.7 and data["llm"]["w"] == 0.6 and data["llm"]["llm_run"] == "DEV_prompt_v1"
    tw.update_weights_file(path, "tfidf", {"w": 0.8})            # rewriting one keeps the other
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["llm"]["w"] == 0.6


def test_load_llm_relevance_uses_shortlist_rows_and_fell_back(tmp_path):
    p = tmp_path / "llm_relevance.csv"
    pd.DataFrame([
        {"build": "B1", "relevance_source": "llm_shortlist", "test": "t.A", "relevance": 0.6, "confidence": 1,
         "reason": "r", "prompt_version": "v1", "fell_back": False},
        {"build": "B1", "relevance_source": "llm_all_individual", "test": "t.B", "relevance": 0.9,
         "confidence": 1, "reason": "r", "prompt_version": "v1", "fell_back": False},
        {"build": "B2", "relevance_source": "llm_shortlist", "test": "t.C", "relevance": 0.3, "confidence": 1,
         "reason": "r", "prompt_version": "v1", "fell_back": True}]).to_csv(p, index=False)
    out = tw.load_llm_relevance(p)
    assert out == {"B1": ({"t.A": 0.6}, False), "B2": ({"t.C": 0.3}, True)}


def test_tune_on_fixture_and_dev_rows_only(tmp_path):
    build, hist = _fixture()
    rows = [SimpleNamespace(pr_name="PR-1", build_id=1, stage_id="single")]
    grid = tw.tune(CFG, "tfidf", FakeLoader(build, hist), rows)
    assert list(grid.columns) == tw.GRID_COLUMNS
    assert len(grid) == len(CFG["tuning"]["w_grid"]) * len(CFG["budgets"]) and set(grid["builds"]) == {1}
    llm = {build.key: ({"p.a.CacheTest": 0.9}, True)}             # fell back: every w equals DANTE-CCH
    g = tw.tune(CFG, "llm", FakeLoader(build, hist), rows, llm)
    at10 = g[(g["budget"] - 0.1).abs() < 1e-9]
    assert at10["sapfdc_mean"].nunique() == 1
    with pytest.raises(SystemExit):
        tw.tune(CFG, "llm", FakeLoader(build, hist), rows, {})    # build missing from the CSV
    ev = tmp_path / "eval.csv"
    pd.DataFrame({"key": ["A", "B", "C"], "pr_name": ["a", "b", "c"], "build_id": 1, "stage_id": "single",
                  "split": ["dev", "test", "dev"]}).to_csv(ev, index=False)
    cfg = {**CFG, "eval": {**CFG["eval"], "eval_set": str(ev)}}
    assert [r.key for r in tw.dev_rows(cfg)] == ["A", "C"]          # the test split is never read
