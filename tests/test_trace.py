"""Trace logger, null logger, analyzer/router instrumentation and the sample exporter."""
import json

from src.agent.fallback_router import FallbackRouter
from src.agent.llm_provider import LLMTimeout, MockProvider
from src.agent.semantic_analyzer import SemanticAnalyzer, make_request
from src.contracts import validate
from src.obs import TRUNCATION_MARKER, NullTrace, TraceLogger
from src.obs.export_sample import export, main as export_main


def _lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_steps_per_build(tmp_path):
    t = TraceLogger(tmp_path, "run1")
    steps = [t.event("b1", "pipeline", "state", {"stage": s}).step for s in ("loaded", "dante_scored", "shortlisted")]
    assert steps == [1, 2, 3]
    assert t.event("b2", "pipeline", "state", {"stage": "loaded"}).step == 1
    assert t.event("b1", "pipeline", "state", {"stage": "selected"}).step == 4
    assert [e["step"] for e in _lines(tmp_path / "run1" / "b1.jsonl")] == [1, 2, 3, 4]


def test_lines_are_valid_trace_events(tmp_path):
    t = TraceLogger(tmp_path, "run1")
    t.event("b1", "orchestrator", "tool_call", {"tool": "diff_reader", "args": {"file": "a.java"}}, latency_s=0.01)
    t.event("b1", "orchestrator", "decision", {"w": 0.5, "confidence": 0.8})
    for ev in _lines(tmp_path / "run1" / "b1.jsonl"):
        validate(ev, "trace_event")
        assert ev["run_id"] == "run1" and ev["ts"].endswith("Z")


def test_nested_strings_are_truncated(tmp_path):
    t = TraceLogger(tmp_path, "r", max_text_chars=5)
    ev = t.event("b", "explainer", "explanation", {"evidence": {"files": ["abcdefgh", "xy"]}, "n": 123456789})
    assert ev.payload == {"evidence": {"files": ["abcde" + TRUNCATION_MARKER, "xy"]}, "n": 123456789}
    assert _lines(tmp_path / "r" / "b.jsonl")[0]["payload"]["evidence"]["files"][0] == "abcde" + TRUNCATION_MARKER


def test_null_trace_writes_nothing(tmp_path):
    assert NullTrace().event("b", "pipeline", "state", {"stage": "loaded"}) is None
    assert list(tmp_path.iterdir()) == []


def _ok(test, rel=0.5, conf=0.9):
    return json.dumps({"test": test, "relevance": rel, "reason": "r", "confidence": conf})


def _reqs(*tests):
    return [make_request("b1", t, "+x", "class X {}", 3000, 3000) for t in tests]


def test_analyzer_writes_one_llm_call_per_request(tmp_path):
    t = TraceLogger(tmp_path, "run1")
    analyzer = SemanticAnalyzer(MockProvider([_ok("t.A"), _ok("t.B")]), trace=t, run_id="run1")
    for req in _reqs("t.A", "t.B"):
        analyzer.analyze(req)
    events = _lines(tmp_path / "run1" / "b1.jsonl")
    assert [(e["component"], e["event"], e["payload"]["test"]) for e in events] == [
        ("semantic_analyzer", "llm_call", "t.A"), ("semantic_analyzer", "llm_call", "t.B")]
    p = events[0]["payload"]
    assert set(p) == {"test", "prompt", "response", "attempt", "cached", "prompt_tokens", "completion_tokens"}
    assert "t.A" in p["prompt"] and json.loads(p["response"])["test"] == "t.A"
    assert p["attempt"] == 0 and p["cached"] is False


def test_router_fallback_writes_fallback_event(tmp_path):
    t = TraceLogger(tmp_path, "run1")
    router = FallbackRouter(SemanticAnalyzer(MockProvider([_ok("t.A"), LLMTimeout("slow")]), trace=t),
                            min_confidence=0.3, trace=t, run_id="run1")
    res = router.run("b1", _reqs("t.A", "t.B"), ["t.B", "t.A"])
    assert res.fell_back
    events = _lines(tmp_path / "run1" / "b1.jsonl")
    assert [(e["component"], e["event"]) for e in events] == [
        ("semantic_analyzer", "llm_call"), ("semantic_analyzer", "llm_call"), ("fallback_router", "fallback")]
    assert events[1]["payload"]["response"] is None and events[1]["payload"]["error"] == "LLMTimeout"
    assert events[2]["payload"] == res.fallbacks[0].to_dict()


def test_components_without_trace_behave_as_before():
    router = FallbackRouter(SemanticAnalyzer(MockProvider([_ok("t.A")])), min_confidence=0.3)
    res = router.run("b1", _reqs("t.A"), ["t.A"])
    assert res.source == "llm" and res.relevance == {"t.A": 0.5}


def test_export_sample_copies_and_renders(tmp_path):
    t = TraceLogger(tmp_path / "traces", "E3_test_seed1")
    t.event("PR-1_build1", "semantic_analyzer", "llm_call",
            {"test": "a.T", "prompt": "PROMPT TEXT", "response": "{\"x\": 1}", "attempt": 0}, latency_s=1.5)
    t.event("PR-1_build1", "fallback_router", "fallback", {"build_id": "PR-1_build1", "reason": "timeout"})
    out = tmp_path / "logs_sample"
    [md] = export(tmp_path / "traces", "E3_test_seed1", ["PR-1_build1"], out)
    copy = out / "E3_test_seed1" / "PR-1_build1.jsonl"
    assert copy.read_text() == (tmp_path / "traces" / "E3_test_seed1" / "PR-1_build1.jsonl").read_text()
    text = md.read_text(encoding="utf-8")
    assert text.index("## 1. semantic_analyzer · llm_call") < text.index("## 2. fallback_router · fallback")
    assert "```text\nPROMPT TEXT\n```" in text and "1.500 s" in text and '"reason": "timeout"' in text


def test_export_sample_cli_first_n(tmp_path, capsys):
    t = TraceLogger(tmp_path / "traces", "run")
    for b in ("PR-3_build1", "PR-1_build1", "PR-2_build1"):
        t.event(b, "pipeline", "state", {"stage": "loaded"})
    assert export_main(["--run-id", "run", "--n", "2", "--trace-dir", str(tmp_path / "traces"),
                        "--out", str(tmp_path / "out")]) == 0
    assert sorted(p.name for p in (tmp_path / "out" / "run").glob("*.md")) == ["PR-1_build1.md", "PR-2_build1.md"]
