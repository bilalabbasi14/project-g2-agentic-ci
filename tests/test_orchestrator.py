import copy
import json

import pandas as pd
import pytest

from src.agent.llm_provider import LLMTimeout, MockProvider
from src.agent.orchestrator import (FEATURE_DOCS, FORCED_FINAL, FORCED_FINAL_CALLS, ORCH_PROMPT_VERSION,
                                    LLMOrchestrator, build_features, make_input)
import inspect

from src.contracts import DANTE_W, validate
from src.contracts.interfaces import OrchestratorLike
from src.dante.scoring import score_table
from src.data.loader import BuildData, HistoryData, TestCase
from src.settings import load_config
from src.tools.registry import ToolRegistry
from tests.fakes import FakeToolRegistry

CFG = load_config()
SECRET_HASH = "deadbeefcafe1234"


def _fixture():
    """Same synthetic build as tests/test_weight_equivalence.py, plus a second changed file."""
    cases = {
        "p.a.CacheTest": TestCase("p.a.CacheTest", 10.0, 1, "a/CacheTest.java", ["cache", "evict"]),
        "p.b.WebTest": TestCase("p.b.WebTest", 50.0, 0, "b/WebTest.java", ["servlet", "http"]),
        "p.b.SlowTest": TestCase("p.b.SlowTest", 100.0, 1, "b/SlowTest.java", ["slow", "http"]),
        "p.c.NoSource": TestCase("p.c.NoSource", 5.0, 0),
    }
    diff_files = {
        "a/Cache.java": {"hunk_text": f"index {SECRET_HASH}..abc1234\n+evict()", "changed_lines": "evict()",
                         "added": 1, "removed": 0},
        "b/web/Http.java": {"hunk_text": "-get()\n+post()", "changed_lines": "get()\npost()",
                            "added": 1, "removed": 1},
    }
    build = BuildData(key="PR-1_build1", pr_name="PR-1", build_id=1, stage_id="single", sha="0" * 40,
                      timestamp=1.0, test_cases=cases, diff_text="", diff_files=diff_files,
                      diff_tokens={"a/Cache.java": ["cache", "evict"], "b/web/Http.java": ["http", "post"]},
                      source_texts={t: f"class {t.split('.')[-1]} {{}}" for t in cases})
    frames = [pd.DataFrame({"testclass": ["p.b.SlowTest", "p.a.CacheTest"], "outcome": [int(i == 1), 0],
                            "duration": [100.0, 10.0], "build_index": i}) for i in range(3)]
    hist = HistoryData(frames=frames, keys=["h0", "h1", "h2"], previous_outcomes=[{"p.b.SlowTest": 1}])
    return build, hist


def _df(build, hist):
    h, d = CFG["history"], CFG["dante"]
    df, _ = score_table(build, hist, h["lookback_windows"], h["min_sticky_events"], power=d["relevance_power"])
    return df


SHORT = ["p.b.SlowTest", "p.a.CacheTest"]
REL = {"p.b.SlowTest": 0.2, "p.a.CacheTest": 0.9}


def _input():
    build, hist = _fixture()
    return make_input(build, hist, _df(build, hist), SHORT, REL, "llm_shortlist", [0.05, 0.1, 0.2])


def _tools():
    build, hist = _fixture()
    return ToolRegistry.for_build(hist.frames, build.diff_files)


def tool(name="history_retrieval", **args):
    args = args or {"test": "p.b.SlowTest"}
    return json.dumps({"action": "call_tool", "tool": name, "args": args, "reason": "look"})


def final(w=0.4, conf=0.8):
    return json.dumps({"action": "final", "w": w, "confidence": conf, "reason": "focused change"})


def _orch(answers, trace=None):
    return LLMOrchestrator(MockProvider(answers), CFG, trace=trace)


# ---------------------------------------------------------------- features ----

def test_build_features_keys_and_values():
    build, hist = _fixture()
    df = _df(build, hist)
    f = build_features(build, hist, df, SHORT, REL, "llm_shortlist")
    assert list(f) == list(FEATURE_DOCS) and len(f) == 12
    assert all(isinstance(v, float) for v in f.values())
    assert f["n_code_files"] == 2 and f["n_dirs"] == 2
    assert f["lines_added"] == 2 and f["lines_removed"] == 1
    assert f["recent_failure_density"] == pytest.approx(1 / 3)
    assert f["n_candidates"] == len(df) == 3 and f["shortlist_size"] == 2
    assert f["rel_mean_shortlist"] == pytest.approx(0.55) and f["rel_max"] == 0.9 and f["n_rel_ge_05"] == 1
    assert f["hist_max"] == df["history_score"].max()


def test_build_features_ignore_target_outcomes():
    build, hist = _fixture()
    df = _df(build, hist)
    before = build_features(build, hist, df, SHORT, REL, "llm_shortlist")
    flipped = copy.deepcopy(build)
    for t in flipped.test_cases.values():
        t.outcome = 1 - t.outcome
    df2 = df.copy()
    df2["actual_outcome"] = 1 - df2["actual_outcome"]
    assert build_features(flipped, hist, df2, SHORT, REL, "llm_shortlist") == before
    assert make_input(flipped, hist, df2, SHORT, REL, "llm_shortlist", [0.1]).to_dict() == \
        make_input(build, hist, df, SHORT, REL, "llm_shortlist", [0.1]).to_dict()


def test_make_input_validates_and_hides_llm_for_tfidf():
    inp = _input()
    validate(inp.to_dict(), "orchestrator_input")
    assert inp.changed_files == ["a/Cache.java", "b/web/Http.java"]
    assert {s["test"]: s["llm_relevance"] for s in inp.shortlist} == REL
    build, hist = _fixture()
    tf = make_input(build, hist, _df(build, hist), SHORT, {}, "tfidf", [0.1])
    assert all(s["llm_relevance"] is None for s in tf.shortlist)
    assert all("outcome" not in s for s in tf.shortlist)


# ------------------------------------------------------------- decide loop ----

def test_satisfies_interface():
    want = list(inspect.signature(OrchestratorLike.decide).parameters)
    assert list(inspect.signature(LLMOrchestrator.decide).parameters) == want == ["self", "inp", "tools", "run_id"]


def test_one_tool_then_final():
    o = _orch([tool(), final(0.4, 0.8)])
    d = o.decide(_input(), _tools(), "run1")
    assert d.source == "agent" and d.w == 0.4 and d.confidence == 0.8 and d.fallback is None
    assert len(d.tool_calls) == 1 and d.tool_calls[0].ok and d.steps == 2 and d.llm_calls == 2
    assert d.prompt_version == ORCH_PROMPT_VERSION
    validate(d.to_dict(), "orchestrator_decision")
    second = o.provider.prompts[1]
    assert "Observation 1: history_retrieval" in second and '"failures": 1' in second


def test_low_confidence_falls_back():
    d = _orch([final(0.2, 0.1)]).decide(_input(), _tools(), "run1")
    assert d.source == "fallback" and d.w == CFG["orchestrator"]["fallback_w"] == pytest.approx(DANTE_W)
    assert d.fallback.reason == "low_confidence" and d.confidence == 0.1
    validate(d.to_dict(), "orchestrator_decision")


@pytest.mark.parametrize("bad, reason", [
    ("not json at all", "invalid_json"),
    (final(1.5, 0.9), "schema_violation"),
    (LLMTimeout("slow"), "timeout"),
])
def test_failure_after_retry_falls_back(bad, reason):
    o = _orch([bad, bad, final()])
    d = o.decide(_input(), _tools(), "run1")
    assert d.source == "fallback" and d.fallback.reason == reason and d.w == pytest.approx(DANTE_W)
    assert d.llm_calls == 2 and len(o.provider.prompts) == 2
    validate(d.to_dict(), "orchestrator_decision")


def test_retry_recovers():
    d = _orch(["garbage", final(0.3, 0.9)]).decide(_input(), _tools(), "run1")
    assert d.source == "agent" and d.w == 0.3 and d.llm_calls == 2


def test_tool_limit_forces_final_and_caps_calls():
    o = _orch([tool()])   # keeps asking for tools forever
    d = o.decide(_input(), _tools(), "run1")
    prompts = o.provider.prompts
    assert len(d.tool_calls) == 4
    assert all(FORCED_FINAL not in p for p in prompts[:4]) and all(FORCED_FINAL in p for p in prompts[4:])
    assert not any(FORCED_FINAL_CALLS in p for p in prompts)
    assert len(prompts) == d.llm_calls == 6 <= o.max_llm_calls
    assert d.source == "fallback" and d.fallback.reason == "schema_violation"


def test_forced_final_accepted():
    d = _orch([tool()] * 4 + [final(0.9, 0.7)]).decide(_input(), _tools(), "run1")
    assert d.source == "agent" and d.w == 0.9 and len(d.tool_calls) == 4 and d.llm_calls == 5


def test_hard_limit_with_retries_everywhere():
    # every tool request needs a retry; the loop must still stop at max_tool_calls + 2 calls
    o = _orch(["bad", tool()])
    d = o.decide(_input(), _tools(), "run1")
    assert d.llm_calls <= o.max_llm_calls == 6 and len(o.provider.prompts) == d.llm_calls
    # forced by the call limit after fewer than 4 tools: the prompt says so, not "Tool limit reached"
    assert len(d.tool_calls) < 4 and FORCED_FINAL_CALLS in o.provider.prompts[-1]
    assert FORCED_FINAL not in o.provider.prompts[-1]
    validate(d.to_dict(), "orchestrator_decision")


def test_tool_not_offered_continues_with_error_observation():
    build, hist = _fixture()
    tools = ToolRegistry.for_build(hist.frames, build.diff_files, allowed=("history_retrieval",))
    o = _orch([tool("diff_reader", file="a/Cache.java"), final()])
    d = o.decide(_input(), tools, "run1")
    assert d.source == "agent" and d.tool_calls[0].ok is False
    assert "unknown tool" in o.provider.prompts[1] and "Observation 1: diff_reader" in o.provider.prompts[1]


def test_diff_observation_is_anonymised():
    o = _orch([tool("diff_reader", file="a/Cache.java"), final()])
    o.decide(_input(), _tools(), "run1")
    assert "evict()" in o.provider.prompts[1] and SECRET_HASH not in o.provider.prompts[1]


def test_observation_truncated():
    cfg = copy.deepcopy(CFG)
    cfg["orchestrator"]["observation_max_chars"] = 20
    o = LLMOrchestrator(MockProvider([tool(), final()]), cfg)
    o.decide(_input(), _tools(), "run1")
    obs = [ln for ln in o.provider.prompts[1].splitlines() if ln.startswith("Observation 1")][0]
    assert obs.endswith("...[truncated]")


def test_prompt_contents():
    o = _orch([final()])
    d = o.decide(_input(), FakeToolRegistry(), "run1")
    p = o.provider.prompts[0]
    assert o.prompt_version == d.prompt_version == ORCH_PROMPT_VERSION == "o2"
    for needle in ("DANTE method uses", "w = 1 ranks by history alone", "w = 0 ranks by relevance alone", "p.b.SlowTest",
                   "a/Cache.java", "history_retrieval", '"action": "call_tool"', '"action": "final"',
                   "single JSON object and nothing else", "recent_failure_density", "n_rel_ge_05", "rel_max"):
        assert needle in p, needle


def test_o2_answer_shapes_have_no_numbers_to_copy():
    """o1 put example values (w 0.5, confidence 0.8) in the answer shape and the model returned them on
    every dev build; o2's shapes only have placeholders."""
    import re
    o = _orch([final()])
    o.decide(_input(), FakeToolRegistry(), "run1")
    p = o.provider.prompts[0]
    assert not re.search(r'"w":\s*[0-9]', p) and not re.search(r'"confidence":\s*[0-9]', p)
    assert '"w": <your weight for this build, from 0 to 1>' in p
    assert "different builds should usually get different values of w" in p
    from src.agent.orchestrator import PROMPT_TEMPLATE_O2
    # the only numbers in the o2 instructions: the 0-1 range of w and the formula's exponent
    assert sorted(set(re.findall(r"\d+(?:\.\d+)?", PROMPT_TEMPLATE_O2))) == ["0", "05", "1", "1.2"]


def test_o1_stays_selectable_and_unknown_version_fails():
    cfg = copy.deepcopy(CFG)
    cfg["orchestrator"]["prompt_version"] = "o1"
    o = LLMOrchestrator(MockProvider([final()]), cfg)
    d = o.decide(_input(), FakeToolRegistry(), "run1")
    assert d.prompt_version == "o1" and '"w": 0.5, "confidence": 0.8' in o.provider.prompts[0]
    cfg["orchestrator"]["prompt_version"] = "o9"
    with pytest.raises(ValueError):
        LLMOrchestrator(MockProvider([final()]), cfg)


# ------------------------------------------------------------------ tracing ----

def _events(tmp_path):
    return [json.loads(x) for x in (tmp_path / "run1" / "PR-1_build1.jsonl").read_text("utf-8").splitlines()]


def test_trace_events_in_order(tmp_path):
    from src.obs import TraceLogger
    o = _orch([tool(), final()], trace=TraceLogger(tmp_path, "run1"))
    o.decide(_input(), _tools(), "run1")
    ev = _events(tmp_path)
    assert [(e["component"], e["event"]) for e in ev] == [
        ("orchestrator", "llm_call"), ("orchestrator", "tool_call"), ("orchestrator", "llm_call"),
        ("orchestrator", "decision")]
    assert set(ev[0]["payload"]) == {"step", "prompt", "response", "attempt", "cached"}
    assert [ev[0]["payload"]["step"], ev[2]["payload"]["step"]] == [1, 2]
    assert set(ev[1]["payload"]) == {"tool", "args", "output", "ok", "error"}
    assert ev[3]["payload"] == {"w": 0.4, "confidence": 0.8, "source": "agent", "reason": "focused change",
                                "tool_calls": 1}
    for e in ev:
        validate(e, "trace_event")


def test_trace_fallback(tmp_path):
    from src.obs import TraceLogger
    o = _orch([LLMTimeout("slow")], trace=TraceLogger(tmp_path, "run1"))
    d = o.decide(_input(), _tools(), "run1")
    ev = _events(tmp_path)
    assert [e["event"] for e in ev] == ["llm_call", "llm_call", "fallback", "decision"]
    assert [e["payload"]["attempt"] for e in ev[:2]] == [0, 1]
    assert ev[0]["payload"]["response"] is None and ev[0]["payload"]["error"] == "LLMTimeout"
    assert ev[2]["payload"] == d.fallback.to_dict()
    assert ev[3]["payload"]["source"] == "fallback"
