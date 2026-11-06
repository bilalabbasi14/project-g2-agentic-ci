"""w = 2/3 (w_history = 2/3, w_relevance = 1/3) ranks and selects exactly like DANTE (1.0*H + 0.5*R^1.2).

Multiplying every base score by the same constant (1.5) cannot change the
order, so the Phase 2 weight w = DANTE_W reproduces DANTE. The fixture is a
copy of tests/test_end_to_end.py::_fixture, with relevance and history both
non-zero so the order depends on both signals.
"""
import pandas as pd
import pytest

from src.contracts import DANTE_W
from src.dante.scoring import score_table
from src.dante.selection import greedy_select
from src.data.loader import BuildData, HistoryData, TestCase
from src.settings import load_config


def _fixture():
    cases = {
        "p.a.CacheTest": TestCase("p.a.CacheTest", 10.0, 1, "a/CacheTest.java", ["cache", "evict"]),
        "p.b.WebTest": TestCase("p.b.WebTest", 50.0, 0, "b/WebTest.java", ["servlet", "http"]),
        "p.b.SlowTest": TestCase("p.b.SlowTest", 100.0, 1, "b/SlowTest.java", ["slow", "http"]),
        "p.c.NoSource": TestCase("p.c.NoSource", 5.0, 0),
    }
    build = BuildData(key="PR-1_build1", pr_name="PR-1", build_id=1, stage_id="single", sha="0" * 40,
                      timestamp=1.0, test_cases=cases, diff_text="",
                      diff_files={"a/Cache.java": {"hunk_text": "+evict()", "changed_lines": "evict()",
                                                   "added": 1, "removed": 0}},
                      diff_tokens={"a/Cache.java": ["cache", "evict"]},
                      source_texts={t: f"class {t.split('.')[-1]} {{}}" for t in cases})
    frames = [pd.DataFrame({"testclass": ["p.b.SlowTest", "p.a.CacheTest"], "outcome": [1, 0],
                            "build_index": i}) for i in range(3)]
    hist = HistoryData(frames=frames, keys=["h0", "h1", "h2"], previous_outcomes=[{"p.b.SlowTest": 1}])
    return build, hist


def _scores(w_history, w_relevance):
    cfg = load_config()
    build, hist = _fixture()
    h, d = cfg["history"], cfg["dante"]
    df, _ = score_table(build, hist, h["lookback_windows"], h["min_sticky_events"],
                        w_history=w_history, w_relevance=w_relevance, power=d["relevance_power"])
    return build, df


def test_fixture_uses_both_signals():
    _, df = _scores(1.0, 0.5)
    assert (df["history_score"] > 0).any() and (df["tfidf_relevance"] > 0).any()


def test_dante_w_constant():
    assert DANTE_W == pytest.approx(2 / 3)


def test_two_thirds_gives_same_order_and_selection_as_dante():
    build, dante = _scores(1.0, 0.5)
    _, w23 = _scores(2 / 3, 1 / 3)
    order_dante = dante.sort_values("dante_cch_score", ascending=False).index.tolist()
    order_w23 = w23.sort_values("dante_cch_score", ascending=False).index.tolist()
    assert order_dante == order_w23
    assert w23["dante_cch_score"].to_numpy() == pytest.approx(dante["dante_cch_score"].to_numpy() * 2 / 3)
    for fraction in (0.10, 0.50):
        budget = build.total_duration_all() * fraction
        sel_dante, _ = greedy_select(dante, "dante_cch_score", budget)
        sel_w23, _ = greedy_select(w23, "dante_cch_score", budget)
        assert sel_dante == sel_w23
