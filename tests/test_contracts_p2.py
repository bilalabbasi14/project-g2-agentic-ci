"""Phase 2 contracts: example files, round trips, validation rules and fakes."""
import json

import jsonschema
import pandas as pd
import pytest

from src.contracts import (
    ExplanationRecord, LLMCallRecord, MethodSpec, OrchestratorDecision, OrchestratorInput,
    TraceEvent, validate,
)
from src.settings import REPO_ROOT
from tests.fakes import FakeExplainer, FakeOrchestrator, FakeSingleCallScorer, FakeToolRegistry

EXAMPLES = REPO_ROOT / "docs" / "examples"


def _example(name):
    return json.loads((EXAMPLES / f"{name}.json").read_text())


@pytest.mark.parametrize("name", ["method_spec", "orchestrator_decision", "explanation_record", "trace_event"])
def test_new_examples_validate(name):
    validate(_example(name), name)


@pytest.mark.parametrize("cls, name", [
    (MethodSpec, "method_spec"),
    (OrchestratorDecision, "orchestrator_decision"),
    (ExplanationRecord, "explanation_record"),
])
def test_round_trip(cls, name):
    obj = cls.from_dict(_example(name))
    assert cls.from_dict(obj.to_dict()) == obj
    assert obj.to_dict() == _example(name)


def test_decision_round_trip_with_fallback():
    d = OrchestratorDecision.from_dict({
        "build_id": "b", "w": 2 / 3, "confidence": None, "source": "fallback", "reason": "x", "steps": 2,
        "tool_calls": [], "llm_calls": 2,
        "fallback": {"build_id": "b", "reason": "invalid_json", "detail": "", "test": None}})
    assert d.fallback.reason == "invalid_json"
    assert OrchestratorDecision.from_dict(d.to_dict()) == d
    validate(d.to_dict(), "orchestrator_decision")


@pytest.mark.parametrize("kwargs", [
    {"relevance_source": "bm25", "weight_mode": "fixed", "w": 0.5},          # unknown relevance source
    {"relevance_source": "tfidf", "weight_mode": "learned"},                 # unknown weight mode
    {"relevance_source": "tfidf", "weight_mode": "fixed"},                   # fixed without w
    {"relevance_source": "tfidf", "weight_mode": "fixed", "w": 1.5},         # w outside [0, 1]
    {"relevance_source": "tfidf", "weight_mode": "fixed", "w": -0.1},        # w outside [0, 1]
    {"relevance_source": "tfidf", "weight_mode": "tuned"},                   # tuned without key
    {"relevance_source": "tfidf", "weight_mode": "tuned", "tuned_key": "bm25"},
    {"relevance_source": "none", "weight_mode": "agent"},                    # agent needs relevance
])
def test_method_spec_rejects_invalid(kwargs):
    with pytest.raises(ValueError):
        MethodSpec(name="m", **kwargs)


def test_method_spec_valid_cases():
    for kw in ({"relevance_source": "none", "weight_mode": "random"},
               {"relevance_source": "tfidf", "weight_mode": "fixed", "w": 0.0},
               {"relevance_source": "tfidf", "weight_mode": "tuned", "tuned_key": "llm"},
               {"relevance_source": "llm_shortlist", "weight_mode": "agent", "explainer": True}):
        validate(MethodSpec(name="m", **kw).to_dict(), "method_spec")


CALL_TOOL = {"action": "call_tool", "tool": "history_retrieval", "args": {"test": "a.B"}, "reason": "check history"}
FINAL = {"action": "final", "w": 0.4, "confidence": 0.8, "reason": "relevance is strong"}


def test_orchestrator_step_accepts_both_shapes():
    validate(CALL_TOOL, "orchestrator_step")
    validate(FINAL, "orchestrator_step")


@pytest.mark.parametrize("bad", [
    {**FINAL, "w": 1.5},
    {**CALL_TOOL, "tool": "budget_tracker"},
    {**FINAL, "extra": 1},
    {k: v for k, v in FINAL.items() if k != "reason"},
    {k: v for k, v in CALL_TOOL.items() if k != "reason"},
    {**FINAL, "reason": "x" * 301},
])
def test_orchestrator_step_rejects(bad):
    with pytest.raises(jsonschema.ValidationError):
        validate(bad, "orchestrator_step")


def test_explanation_response():
    good = {"test": "a.B", "justification": "x" * 400, "cited_facts": ["failures: 0 of 100 runs"]}
    validate(good, "explanation_response")
    with pytest.raises(jsonschema.ValidationError):
        validate({**good, "justification": "x" * 401}, "explanation_response")
    with pytest.raises(jsonschema.ValidationError):
        validate({**good, "cited_facts": []}, "explanation_response")


def test_single_call_response():
    validate({"scores": [{"test": "a.B", "relevance": 0.0}, {"test": "a.C", "relevance": 1.0}]},
             "single_call_response")
    with pytest.raises(jsonschema.ValidationError):
        validate({"scores": [{"test": "a.B", "relevance": -0.1}]}, "single_call_response")
    with pytest.raises(jsonschema.ValidationError):
        validate({"scores": [{"test": "a.B", "relevance": 0.5, "reason": "x"}]}, "single_call_response")


def test_old_llm_call_record_still_works():
    rec = LLMCallRecord(model="m", latency_s=1.0, prompt_tokens=10, completion_tokens=2, ok=True, error=None)
    assert rec.cached is False and rec.component is None
    validate(rec.to_dict(), "llm_call_record")
    validate(LLMCallRecord(model="m", latency_s=0.5, cached=True, component="orchestrator").to_dict(),
             "llm_call_record")
    with pytest.raises(ValueError):
        LLMCallRecord(model="m", latency_s=0.5, component="relevance")


def test_trace_event_enums():
    validate(TraceEvent("r", "b", "pipeline", "state", 1, {"stage": "loaded"}).to_dict(), "trace_event")
    with pytest.raises(ValueError):
        TraceEvent("r", "b", "nobody", "state", 1, {})
    with pytest.raises(ValueError):
        TraceEvent("r", "b", "pipeline", "thinking", 1, {})


def _input():
    return OrchestratorInput(build_id="b", features={"n_code_files": 1.0},
                             shortlist=[{"test": "a.B", "history_score": 0.1, "tfidf_relevance": 0.5,
                                         "llm_relevance": None, "duration": 3.0}],
                             changed_files=["a/B.java"], budget_fractions=[0.05, 0.1, 0.2],
                             relevance_source="tfidf")


def test_fakes_return_valid_objects():
    validate(_input().to_dict(), "orchestrator_input")
    reg = FakeToolRegistry()
    assert [s["name"] for s in reg.specs()] == ["history_retrieval", "diff_reader", "budget_tracker"]
    validate(reg.call("history_retrieval", {"test": "a.B"}).to_dict(), "tool_call_record")

    orch = FakeOrchestrator(w=0.3)
    d = orch.decide(_input(), reg, "run")
    validate(d.to_dict(), "orchestrator_decision")
    assert (d.w, d.confidence, d.llm_calls, d.tool_calls) == (0.3, 0.9, 1, [])

    df = pd.DataFrame({"duration": [1.0, 2.0, 3.0]}, index=["t1", "t2", "t3"])
    recs = FakeExplainer().explain("b", 0.1, df, ["t1"], ["t1", "t2", "t3"], {"t1": 1.0, "t2": 2.0, "t3": 3.0},
                                   1.0, {}, {}, lambda t: {}, "run")
    assert [(r.test, r.rank_by_value) for r in recs] == [("t2", 2)]
    for r in recs:
        validate(r.to_dict(), "explanation_record")

    rel, fallbacks, calls = FakeSingleCallScorer(0.5).score("b", "diff", ["t1", "t2"], "run")
    assert rel == {"t1": 0.5, "t2": 0.5} and fallbacks == [] and calls == 1
    validate({"scores": [{"test": t, "relevance": v} for t, v in rel.items()]}, "single_call_response")
