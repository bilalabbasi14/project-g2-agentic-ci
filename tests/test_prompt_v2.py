"""Relevance prompt v2 and the dev-split prompt comparison (P2-07); no data, no model."""
import hashlib

import pandas as pd
import pytest

from src.agent import prompt_eval as pe
from src.agent.semantic_analyzer import (PROMPT_TEMPLATE, build_prompt, make_request,
                                         prompt_version_from_config)
from src.pipeline import LLM_RELEVANCE_COLUMNS, PER_BUILD_COLUMNS

TEST = "org.apache.karaf.FooTest"
DIFF = "diff --git a/src/Foo.java b/src/Foo.java\nindex 1a2b3c4..5d6e7f8 100644\n+int foo() { return 1; }\n"
# SHA-256 of the Phase 1 PROMPT_TEMPLATE on main before P2-07: v1 must stay byte-identical.
V1_SHA256 = "7666b5ee68672663106780e1c880be8f835af01321e6bdc905bbfbb62b2c3afb"


def test_v1_template_is_unchanged():
    assert hashlib.sha256(PROMPT_TEMPLATE.encode()).hexdigest() == V1_SHA256
    req = make_request("b1", TEST, DIFF, "class FooTest {}", 3000, 3000)
    assert req.prompt_version == "v1"
    assert build_prompt(req) == PROMPT_TEMPLATE.format(diff=req.diff_chunk, test=TEST, source=req.test_source)


def test_v2_has_the_four_anchors_and_the_test_name():
    req = make_request("b1", TEST, DIFF, "class FooTest {}", 3000, 3000, prompt_version="v2")
    p = build_prompt(req)
    assert req.prompt_version == "v2" and p != build_prompt(make_request("b1", TEST, DIFF, "x", 3000, 3000))
    for anchor in ("0.0 = ", "0.3 = ", "0.6 = ", "0.9 = "):
        assert anchor in p
    assert TEST in p and "imports" in p and "package" in p
    assert '"test": "org.apache.karaf.FooTest", "relevance"' in p      # same answer shape as v1
    assert "1a2b3c4" not in p                                         # anonymised exactly like v1


def test_v2_truncates_like_v1():
    long_diff = "+" + "x" * 500
    v1 = make_request("b1", TEST, long_diff, "y" * 500, 60, 100)
    v2 = make_request("b1", TEST, long_diff, "y" * 500, 60, 100, prompt_version="v2")
    assert (v1.diff_chunk, v1.test_source) == (v2.diff_chunk, v2.test_source)
    assert v2.diff_chunk.endswith("[...truncated]") and v2.diff_chunk in build_prompt(v2)


def test_version_from_config():
    assert prompt_version_from_config({}) == "v1"
    assert prompt_version_from_config({"llm_p2": {"relevance_prompt_version": "v2"}}) == "v2"
    with pytest.raises(ValueError):
        prompt_version_from_config({"llm_p2": {"relevance_prompt_version": "v9"}})
    with pytest.raises(ValueError):
        make_request("b1", TEST, DIFF, "", 10, 10, prompt_version="v9")


def _run(tmp_path, name, version, sapfdc, rel, split="dev", fallback=(False, False)):
    d = tmp_path / name
    d.mkdir()
    pb = []
    for i, (s, fb) in enumerate(zip(sapfdc, fallback)):
        base = {c: 0 for c in PER_BUILD_COLUMNS}
        base.update(run_id=name, split=split, build=f"B{i}", method="LLM-relevance", budget=0.1, dtc=0.5 + i * 0.5,
                    sapfdc=s, ranking_source="dante_fallback" if fb else "llm", llm_calls=10, llm_latency_s=30.0)
        pb.append(base)
        pb.append({**base, "method": "DANTE-CCH", "sapfdc": 0.99, "llm_calls": 0, "llm_latency_s": 0})
        pb.append({**base, "budget": 0.2, "sapfdc": 0.99})
    pd.DataFrame(pb, columns=PER_BUILD_COLUMNS).to_csv(d / "per_build.csv", index=False)
    pd.DataFrame([{"build": "B0", "relevance_source": "llm_shortlist", "test": f"t{j}", "relevance": r,
                   "confidence": 0.9, "reason": "r", "prompt_version": version, "fell_back": False}
                  for j, r in enumerate(rel)], columns=LLM_RELEVANCE_COLUMNS).to_csv(d / "llm_relevance.csv",
                                                                                   index=False)
    return d


def test_compare_prompts_numbers(tmp_path):
    a = _run(tmp_path, "DEV_prompt_v1", "v1", [0.2, 0.4], [0.1, 0.1, 0.2, 0.6], fallback=(False, True))
    b = _run(tmp_path, "DEV_prompt_v2", "v2", [0.3, 0.5], [0.1, 0.5, 0.9, 0.3])
    df = pe.compare_prompts([a, b])
    assert list(df.columns) == pe.COLUMNS
    v1, v2 = df.iloc[0], df.iloc[1]
    assert v1["prompt_version"] == "v1" and v1["builds"] == 2
    assert v1["dtc_mean_10"] == pytest.approx(0.75) and v1["sapfdc_mean_10"] == pytest.approx(0.3)
    assert v1["share_rel_le_0_2"] == pytest.approx(0.75) and v1["share_rel_ge_0_5"] == pytest.approx(0.25)
    assert v1["fallback_builds"] == 1 and v1["mean_latency_s"] == pytest.approx(3.0)
    assert v2["share_rel_ge_0_5"] == pytest.approx(0.5) and v2["fallback_builds"] == 0
    winner, why = pe.choose(df)
    assert winner == "v2" and "higher sapfdc_mean_10" in why


def test_decision_tie_rule(tmp_path):
    a = _run(tmp_path, "a", "v1", [0.400, 0.400], [0.1, 0.6])          # share <= 0.2: 0.5
    b = _run(tmp_path, "b", "v2", [0.404, 0.404], [0.1, 0.1, 0.1, 0.6])  # +0.004 (tie), share 0.75
    winner, why = pe.choose(pe.compare_prompts([a, b]))
    assert winner == "v1" and "within" in why
    c = _run(tmp_path, "c", "v2", [0.406, 0.406], [0.1, 0.1, 0.1, 0.6])  # +0.006: no tie
    assert pe.choose(pe.compare_prompts([a, c]))[0] == "v2"


def test_only_dev_runs_are_compared(tmp_path):
    a = _run(tmp_path, "a", "v1", [0.2, 0.4], [0.1], split="test")
    with pytest.raises(ValueError, match="dev-split"):
        pe.compare_prompts([a])


def test_runner_override_sets_the_version(tmp_path):
    from tests.test_run_experiment import KeyedLoader, _cfg
    from experiments.run_experiment import main
    meta = main(["--exp", "DEV", "--seed", "1", "--provider", "mock", "--methods", "LLM-relevance",
                 "--build-limit", "1", "--relevance-prompt", "v2", "--run-id", "DEV_prompt_v2"],
                cfg=_cfg(tmp_path), loader=KeyedLoader(), echo=lambda *_: None)
    assert meta["prompt_versions"]["relevance"] == "v2" and meta["run_id"] == "DEV_prompt_v2"
    rel = pd.read_csv(tmp_path / "results" / "DEV_prompt_v2" / "llm_relevance.csv")
    assert set(rel["prompt_version"]) == {"v2"}
