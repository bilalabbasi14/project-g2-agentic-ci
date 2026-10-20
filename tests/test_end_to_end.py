"""End-to-end path on a tiny synthetic build with MockProvider (no data, no LLM)."""
import json
from types import SimpleNamespace

import pandas as pd

import run_end_to_end as e2e
from src.agent.llm_provider import LLMTimeout, MockProvider
from src.data.loader import BuildData, HistoryData, TestCase
from src.settings import load_config


class FakeLoader:
    def __init__(self, build, history):
        self._b, self._h = build, history

    def row(self, *a):
        return {}

    def build(self, row, keep_sources=False):
        return self._b

    def history(self, row, *a):
        return self._h


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


def _run(provider, monkeypatch, tmp_path):
    cfg = load_config()
    cfg["paths"]["logs_dir"] = str(tmp_path)
    stored = {"total_failures_in_build": 2, "failures_found": 0, "selected_tests_count": 0,
              "detailed_selection": []}
    monkeypatch.setattr(e2e, "load_stored", lambda *a, **k: stored)
    build, hist = _fixture()
    e = SimpleNamespace(pr_name="PR-1", build_id=1, stage_id="single", build_name="x")
    return e2e.run_build(cfg, FakeLoader(build, hist), e, [0.10, 0.5], provider)


def test_end_to_end_llm_path(monkeypatch, tmp_path):
    res = _run(e2e.mock_provider(), monkeypatch, tmp_path)
    assert res["llm_source"] == "llm" and res["fallbacks"] == []
    assert res["candidates"] == 3 and res["total_failures"] == 2
    assert set(res["llm_relevance"]) == set(res["shortlist"])
    b50 = res["budgets"][1]
    # budget = 50% of 165 s = 82.5 s; SlowTest (100 s) cannot fit
    assert "p.b.SlowTest" not in b50["llm_selected"]
    assert b50["methods"]["LLM-relevance"]["dtc"] == 0.5
    json.dumps(res)


def test_end_to_end_fallback_uses_dante(monkeypatch, tmp_path):
    res = _run(MockProvider([LLMTimeout("slow")]), monkeypatch, tmp_path)
    assert res["llm_source"] == "dante_fallback"
    assert [f["reason"] for f in res["fallbacks"]] == ["timeout"]
    for pb in res["budgets"]:
        assert pb["methods"]["LLM-relevance"] == pb["methods"]["DANTE-CCH"]
    assert (tmp_path / "fallbacks.jsonl").exists()
