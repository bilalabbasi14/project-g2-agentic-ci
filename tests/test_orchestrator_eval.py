"""Orchestrator prompt-iteration summary (P2-06 item 4) on tiny fake run folders; no data, no model."""
import json

import pandas as pd
import pytest

from src.agent import orchestrator_eval as oe
from src.pipeline import DECISION_COLUMNS, PER_BUILD_COLUMNS


def _run(tmp_path, name, version, ws, sources=None, split="dev", warning=None):
    d = tmp_path / name
    d.mkdir()
    meta = {"run_id": name, "split": split, "git_commit": "abcdef1234567", "prompt_versions": {"orchestrator": version}}
    if warning:
        meta["git_commit_warning"] = warning
    (d / "run_meta.json").write_text(json.dumps(meta), encoding="utf-8")
    sources = sources or ["agent"] * len(ws)
    pd.DataFrame([{"build": f"B{i}", "relevance_source": "llm_shortlist", "w": w, "confidence": 0.8, "source": s,
                   "steps": 1, "llm_calls": 1, "tool_calls": i % 2, "reason": "r", "fallback_reason": ""}
                  for i, (w, s) in enumerate(zip(ws, sources))], columns=DECISION_COLUMNS).to_csv(
        d / "orchestrator_decisions.csv", index=False)
    rows = []
    for i in range(len(ws)):
        base = {c: 0 for c in PER_BUILD_COLUMNS}
        for method, sap in (("Agent-weighted", 0.6 + 0.1 * i), ("LLM-relevance", 0.5), ("DANTE-CCH", 0.4)):
            rows.append({**base, "build": f"B{i}", "method": method, "budget": 0.1, "sapfdc": sap})
            rows.append({**base, "build": f"B{i}", "method": method, "budget": 0.2, "sapfdc": 0.99})
    pd.DataFrame(rows, columns=PER_BUILD_COLUMNS).to_csv(d / "per_build.csv", index=False)
    return d


def test_same_w_everywhere_triggers_the_rule(tmp_path):
    row = oe.summarise([_run(tmp_path, "o1", "o1", [0.5, 0.5, 0.5])]).iloc[0]
    assert row["prompt_version"] == "o1" and row["distinct_w"] == 1 and bool(row["rule_triggered"])
    assert row["sapfdc_mean_10_agent"] == pytest.approx(0.7) and row["sapfdc_mean_10_dante"] == pytest.approx(0.4)
    assert row["mean_tool_calls"] == pytest.approx(1 / 3) and row["git_commit"] == "abcdef1"


def test_varied_w_without_fallbacks_passes_and_fallbacks_trigger(tmp_path):
    ok = oe.summarise([_run(tmp_path, "o2", "o2", [0.2, 0.5, 0.8])]).iloc[0]
    assert ok["distinct_w"] == 3 and not bool(ok["rule_triggered"])
    assert (ok["w_min"], ok["w_max"]) == (0.2, 0.8) and ok["w_std"] == pytest.approx(0.3)
    fb = oe.summarise([_run(tmp_path, "fb", "o2", [0.2, 0.67, 0.67, 0.5, 0.67],
                            ["agent", "fallback", "agent", "agent", "agent"])]).iloc[0]
    assert fb["fallback_rate"] == pytest.approx(0.2) and not bool(fb["rule_triggered"])      # 20% is allowed
    fb2 = oe.summarise([_run(tmp_path, "fb2", "o2", [0.2, 0.67, 0.67, 0.5],
                             ["agent", "fallback", "fallback", "agent"])]).iloc[0]
    assert bool(fb2["rule_triggered"])                                                        # 50% > 20%


def test_only_clean_dev_runs_are_accepted(tmp_path):
    with pytest.raises(ValueError, match="dev-split"):
        oe.summarise([_run(tmp_path, "t", "o2", [0.3, 0.4], split="test")])
    with pytest.raises(ValueError, match="mixes commits"):
        oe.summarise([_run(tmp_path, "m", "o2", [0.3, 0.4], warning="shards ran on different commits")])


def test_cli_writes_the_columns(tmp_path):
    out = tmp_path / "it.csv"
    oe.main(["--runs", str(_run(tmp_path, "a", "o1", [0.5, 0.5])), str(_run(tmp_path, "b", "o2", [0.3, 0.7])),
             "--out", str(out)])
    df = pd.read_csv(out)
    assert list(df.columns) == oe.COLUMNS and list(df["prompt_version"]) == ["o1", "o2"]
