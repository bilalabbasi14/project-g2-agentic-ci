"""P2-08 selection rule on synthetic metadata (no data, no git clone)."""
from types import SimpleNamespace

import pandas as pd
import pytest

from src.data import make_eval_set_p2 as m


def _meta(n):
    return pd.DataFrame({"key": [f"PR-{i}_build1" for i in range(n)], "pr_name": [f"PR-{i}" for i in range(n)],
                         "build_id": 1, "stage_id": "single", "build_head_sha": [f"{i:040x}" for i in range(n)],
                         "timestamp_for_sort": [1.6e9 + 3600 * i for i in range(n)]})


def test_evenly_spaced_positions():
    df = pd.DataFrame({"chrono_index": range(10), "x": list("abcdefghij")})
    assert m.evenly_spaced(df, 4)["chrono_index"].tolist() == [0, 3, 6, 9]
    assert m.evenly_spaced(df, 10)["chrono_index"].tolist() == list(range(10))
    assert m.evenly_spaced(df.iloc[::-1], 20)["chrono_index"].tolist() == list(range(10))   # sorted, all kept


def test_assign_split_earliest_are_dev():
    df = pd.DataFrame({"chrono_index": [7, 3, 9, 1, 5]})
    out = m.assign_split(df, 2)
    assert out["chrono_index"].tolist() == [1, 3, 5, 7, 9]
    assert out["split"].tolist() == ["dev", "dev", "test", "test", "test"]


def test_cheap_filters_drop_history_diff_and_failure_misses():
    meta = _meta(110)
    no_code = {"PR-101_build1", "PR-105_build1"}
    no_fail = {"PR-102_build1"}
    missing_results = {"PR-103_build1"}

    def diff_fn(row):
        return {} if row["key"] in no_code else {"a/X.java": {}, "b/Y.java": {}}

    def outcomes_fn(row):
        if row["key"] in missing_results:
            return None
        return [0, 0] if row["key"] in no_fail else [0, 1]

    kept, counts = m.apply_cheap_filters(meta, diff_fn, outcomes_fn)
    assert counts == {"all": 110, "F1": 10, "F2": 8, "F3": 6}
    assert kept["chrono_index"].tolist() == [100, 104, 106, 107, 108, 109]
    assert (kept["n_code_files"] == 2).all()


def _build(ok=True, failing=1, sources=True):
    cands = [SimpleNamespace(outcome=1 if i < failing else 0) for i in range(3)]
    return SimpleNamespace(sources_available=sources, candidates=lambda: cands)


def _all_pass(row):
    return {"a/X.java": {}}


def _fails(row):
    return [1]


def test_select_full_rule_and_columns():
    meta = _meta(400)

    def build_fn(row):
        i = int(row["chrono_index"])
        if i % 50 == 1:
            raise ValueError("boom")
        if i % 50 == 2:
            return _build(sources=False)
        if i % 50 == 3:
            return _build(failing=0)
        return _build()

    out, facts = m.select(meta, _all_pass, _fails, build_fn, phase1_keys=["PR-150_build1"], target=120, n_dev=20)
    assert list(out.columns) == m.COLUMNS
    assert len(out) == 120 and (out["split"] == "dev").sum() == 20 and (out["split"] == "test").sum() == 100
    assert out[out.split == "dev"]["chrono_index"].max() < out[out.split == "test"]["chrono_index"].min()
    assert facts["counts"]["preselected"] == 160
    assert set(facts["reasons"]) <= {"load_error", "no_commit_in_clone", "no_failing_candidate"}
    assert out["in_phase1"].dtype == bool
    report = m.render_report(out, facts, "python -m src.data.make_eval_set_p2")
    assert "| Final (evenly spaced) | 120 |" in report and "| dev | 20 |" in report


def test_select_is_deterministic():
    meta = _meta(300)
    a, _ = m.select(meta, _all_pass, _fails, lambda r: _build(), [], 120, 20)
    b, _ = m.select(meta, _all_pass, _fails, lambda r: _build(), [], 120, 20)
    pd.testing.assert_frame_equal(a, b)


def test_too_few_builds_raises_and_writes_nothing(tmp_path, monkeypatch):
    meta = _meta(150)          # only 50 builds have 100 earlier builds
    with pytest.raises(m.TooFewBuildsError):
        m.select(meta, _all_pass, _fails, lambda r: _build(), [], 120, 20)

    class FakeLoader:
        def __init__(self, *a, **k):
            self.meta = meta

        def diff_path(self, row):
            return tmp_path / "missing.diff"

        def test_class_df(self, row):
            return pd.DataFrame({"outcome": [1]})

        def build(self, row):
            return _build()

    cfg = {"paths": {"lrts_root": "x", "repo_clone": "x", "repo_url": "x",
                     "eval_builds": str(tmp_path / "eval_builds.csv")},
           "project": "karaf", "eval": {"eval_set": str(tmp_path / "out.csv")}}
    pd.DataFrame({"key": []}).to_csv(tmp_path / "eval_builds.csv", index=False)
    monkeypatch.setattr(m, "load_config", lambda: cfg)
    monkeypatch.setattr(m, "LRTSLoader", FakeLoader)
    monkeypatch.setattr(m, "SourceRepo", lambda *a: None)
    monkeypatch.setattr(m, "split_diff", lambda text: {"a/X.java": {}})
    monkeypatch.setattr(m, "REPORT", str(tmp_path / "report.md"))
    (tmp_path / "missing.diff").write_text("diff", encoding="utf-8")
    with pytest.raises(SystemExit):
        m.main([])
    assert not (tmp_path / "out.csv").exists() and not (tmp_path / "report.md").exists()
