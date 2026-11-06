"""Deterministic fakes of the Phase 2 component interfaces (src/contracts/interfaces.py).

Other members' tests use these so the pipeline can be built and tested before
the real orchestrator, explainer and single-call scorer exist.
"""
from src.contracts import ExplanationRecord, OrchestratorDecision, ToolCallRecord
from src.tools import TOOL_SPECS


class FakeOrchestrator:
    """Always decides the given w with confidence 0.9, 0 tool calls, 1 LLM call."""

    def __init__(self, w=0.5, source="agent"):
        self.w, self.source = w, source
        self.calls = 0

    def decide(self, inp, tools, run_id):
        self.calls += 1
        return OrchestratorDecision(build_id=inp.build_id, w=self.w, confidence=0.9, source=self.source,
                                    reason="fake", steps=1, tool_calls=[], llm_calls=1)


class FakeExplainer:
    """Explains the skipped tests among the first 2 tests of `ordered`, with justification "fake"."""

    def __init__(self):
        self.calls = 0

    def explain(self, build_id, budget_fraction, df, selected, ordered, durations, budget_seconds,
                diff_files, llm_reasons, history_tool, run_id):
        self.calls += 1
        return [ExplanationRecord(build_id=build_id, budget_fraction=budget_fraction, test=t,
                                  rank_by_value=rank, evidence={"fake": True}, justification="fake",
                                  cited_facts=["fake"], ok=True, error=None, latency_s=0.0,
                                  prompt_tokens=None, completion_tokens=None)
                for rank, t in enumerate(ordered[:2], 1) if t not in selected]


class FakeSingleCallScorer:
    """Gives every candidate the same relevance; no fallbacks, 1 LLM call."""

    def __init__(self, value=0.5):
        self.value = value
        self.calls = 0

    def score(self, build_id, diff_text, candidates, run_id):
        self.calls += 1
        return {t: self.value for t in candidates}, [], 1


class FakeToolRegistry:
    """Offers the real tool specs; every call returns output {"fake": True}."""

    def __init__(self):
        self.calls = []

    def specs(self):
        return list(TOOL_SPECS)

    def call(self, name, args):
        self.calls.append((name, args))
        return ToolCallRecord(tool=name, args=dict(args), output={"fake": True}, latency_s=0.0)
