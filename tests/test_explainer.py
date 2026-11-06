import inspect
import json

import pandas as pd
import pytest

from src.agent.explainer import (EXPLAINER_PROMPT_VERSION, LLMExplainer, build_evidence, build_prompt,
                                 grounding_report, select_skipped)
from src.agent.llm_provider import LLMTimeout, MockProvider
from src.contracts import ExplanationRecord, validate
from src.contracts.interfaces import ExplainerLike
from src.settings import load_config

CFG = load_config()
SECRET_HASH = "deadbeefcafe1234"

# Six candidates; value order A, B, C, D, E, F. Budget 30 s: A (10) and B (15) fit
# (used 25), C (20) does not, D (4) fits (used 29), E (8) does not, and F (2) does
# not either (29 + 2 = 31 > 30). Selected = A, B, D; skipped = C, E, F.
TESTS = ["p.A", "p.B", "p.C", "p.D", "p.E", "p.F"]
DUR = {"p.A": 10.0, "p.B": 15.0, "p.C": 20.0, "p.D": 4.0, "p.E": 8.0, "p.F": 2.0}
SELECTED = ["p.A", "p.B", "p.D"]
BUDGET = 30.0


def _df(outcomes=None):
    df = pd.DataFrame({
        "history_score": [0.9, 0.1, 0.8, 0.0, 0.0, 0.05],
        "relevance_used": [0.1, 0.9, 0.0, 0.2, 0.7, 0.0],
        "duration": [DUR[t] for t in TESTS],
        "actual_outcome": outcomes or [0, 0, 1, 0, 0, 1],
    }, index=TESTS)
    return df


def _history_tool(test):
    return {"test": test, "history_builds": 100, "runs": 100, "failures": 3 if test == "p.C" else 0,
            "failure_rate": 0.03 if test == "p.C" else 0.0, "last_failure_distance": 4 if test == "p.C" else None,
            "recent_outcomes": [0] * 10}


DIFF_FILES = {"core/b/Http.java": {"hunk_text": "-get()\n+post()", "added": 1, "removed": 1},
              "core/a/Cache.java": {"hunk_text": f"index {SECRET_HASH}..abc1234\n+evict()", "added": 1, "removed": 0}}
REASONS = {"p.E": "Calls the changed Cache class; author dev@example.com"}


def _answer(test, justification="Skipping it is risky: relevance 0.7 but it needs 8.0 s.",
            facts=("relevance_used: 0.7", "duration_s: 8.0")):
    return json.dumps({"test": test, "justification": justification, "cited_facts": list(facts)})


class _Trace:
    def __init__(self):
        self.events = []

    def event(self, build_id, component, event, payload, latency_s=None):
        self.events.append((build_id, component, event, payload))


def _explain(explainer, df=None):
    return explainer.explain("PR-1_build1", 0.1, df if df is not None else _df(), SELECTED, TESTS, DUR, BUDGET,
                             DIFF_FILES, REASONS, _history_tool, "run1")


# ------------------------------------------------------------- selection ----

def test_select_skipped_rank_order_and_ignores_selected():
    # pool=2: top-2 by history = A, C; top-2 by relevance = B, E. Skipped = C, E, F.
    # Skipped and important = C (rank 3), E (rank 5); F is in neither top-2.
    assert select_skipped(_df(), SELECTED, TESTS, pool=2, top_n=5) == [("p.C", 3), ("p.E", 5)]


def test_select_skipped_respects_top_n_and_pool():
    assert select_skipped(_df(), SELECTED, TESTS, pool=2, top_n=1) == [("p.C", 3)]
    # pool=6 makes every skipped test important
    assert select_skipped(_df(), SELECTED, TESTS, pool=6, top_n=5) == [("p.C", 3), ("p.E", 5), ("p.F", 6)]


def test_select_skipped_ties_broken_by_name():
    df = _df()
    df["history_score"] = 0.5            # all tied: top-1 by history is the first name, p.A (selected)
    df["relevance_used"] = 0.5
    assert select_skipped(df, SELECTED, TESTS, pool=3, top_n=5) == [("p.C", 3)]


def test_select_skipped_ignores_outcomes():
    a = select_skipped(_df([0, 0, 1, 0, 0, 1]), SELECTED, TESTS, pool=2, top_n=5)
    b = select_skipped(_df([1, 1, 0, 1, 1, 0]), SELECTED, TESTS, pool=2, top_n=5)
    c = select_skipped(_df().drop(columns=["actual_outcome"]), SELECTED, TESTS, pool=2, top_n=5)
    assert a == b == c


# -------------------------------------------------------------- evidence ----

def test_remaining_budget_at_turn_hand_example():
    # 4 tests in value order, budget 20 s:
    #   T1 10 s: used 0  -> fits, used 10
    #   T2 15 s: used 10 -> 25 > 20, skipped; remaining at its turn = 20 - 10 = 10
    #   T3  6 s: used 10 -> fits, used 16
    #   T4  5 s: used 16 -> 21 > 20, skipped; remaining at its turn = 20 - 16 = 4
    order = ["T1", "T2", "T3", "T4"]
    dur = {"T1": 10.0, "T2": 15.0, "T3": 6.0, "T4": 5.0}
    df = pd.DataFrame({"history_score": [0.1] * 4, "relevance_used": [0.2] * 4, "duration": list(dur.values())},
                      index=order)
    ev2 = build_evidence("T2", 2, df, order, dur, ["T1", "T3"], 20.0, {}, {}, _history_tool, 10)
    ev4 = build_evidence("T4", 4, df, order, dur, ["T1", "T3"], 20.0, {}, {}, _history_tool, 10)
    assert ev2["remaining_budget_at_turn_s"] == 10.0 and ev2["fits_if_budget_s"] == 25.0
    assert ev4["remaining_budget_at_turn_s"] == 4.0 and ev4["fits_if_budget_s"] == 21.0
    assert ev2["skip_cause"] == "did_not_fit"


def test_evidence_keys_and_anonymisation():
    ev = build_evidence("p.E", 5, _df(), TESTS, DUR, SELECTED, BUDGET, DIFF_FILES, REASONS, _history_tool, 1)
    assert set(ev) == {"test", "rank_by_value", "n_candidates", "n_selected", "history", "history_score",
                       "relevance_used", "relevance_reason", "changed_files", "duration_s", "budget_s",
                       "remaining_budget_at_turn_s", "skip_cause", "fits_if_budget_s"}
    assert ev["changed_files"] == ["core/a/Cache.java"]            # sorted, cut to max_changed_files
    assert ev["n_candidates"] == 6 and ev["n_selected"] == 3 and ev["rank_by_value"] == 5
    assert ev["history"] == _history_tool("p.E")
    assert ev["relevance_used"] == 0.7 and ev["duration_s"] == 8.0
    assert "dev@example.com" not in ev["relevance_reason"]
    assert ev["remaining_budget_at_turn_s"] == 1.0                   # A + B + D = 29 s used
    no_reason = build_evidence("p.C", 3, _df(), TESTS, DUR, SELECTED, BUDGET, DIFF_FILES, REASONS, _history_tool, 10)
    assert no_reason["relevance_reason"] is None


def test_prompt_contains_evidence_and_no_secrets():
    ev = build_evidence("p.E", 5, _df(), TESTS, DUR, SELECTED, BUDGET, DIFF_FILES, REASONS, _history_tool, 10)
    prompt = build_prompt(ev, 400)
    assert json.dumps(ev, ensure_ascii=False) in prompt
    assert "dev@example.com" not in prompt and SECRET_HASH not in prompt
    assert "cited_facts" in prompt and "400 characters" in prompt


# --------------------------------------------------------- LLM explainer ----

def test_explainer_satisfies_interface():
    assert inspect.signature(LLMExplainer.explain).parameters.keys() - {"self"} == \
        inspect.signature(ExplainerLike.explain).parameters.keys() - {"self"}
    assert LLMExplainer(MockProvider(["{}"]), CFG).prompt_version == EXPLAINER_PROMPT_VERSION


def _requested_test(prompt):
    """The test named in the real-case evidence of an explainer prompt."""
    return json.loads(prompt.split("Now the real case.\nEvidence:\n")[1].rsplit("\nAnswer:", 1)[0])["test"]


def test_valid_answer_ok_and_validates():
    # p.E is answered by its short name "E" to exercise the suffix match
    provider = MockProvider([lambda p: _answer("E" if _requested_test(p) == "p.E" else _requested_test(p))])
    recs = _explain(LLMExplainer(provider, CFG))
    assert [r.test for r in recs] == ["p.C", "p.E", "p.F"]
    assert all(r.ok and r.error is None for r in recs)
    assert recs[1].test == "p.E" and recs[1].justification.startswith("Skipping")
    assert recs[1].prompt_tokens == provider.calls[1].prompt_tokens
    for r in recs:
        validate(r.to_dict(), "explanation_record")
        assert r.prompt_version == "e1"


def test_invalid_then_valid_is_ok_after_two_attempts():
    provider = MockProvider(["not json", _answer("p.C")])
    explainer = LLMExplainer(provider, CFG)
    rec = explainer._explain_one("b", 0.1, "p.C", 3, {"test": "p.C"})
    assert rec.ok and len(provider.prompts) == 2
    assert rec.prompt_tokens == sum(c.prompt_tokens or 0 for c in provider.calls)


def test_invalid_twice_gives_invalid_json():
    provider = MockProvider(["not json"])
    rec = LLMExplainer(provider, CFG)._explain_one("b", 0.1, "p.C", 3, {"test": "p.C"})
    assert not rec.ok and rec.error == "invalid_json" and rec.justification is None and rec.cited_facts == []
    assert len(provider.prompts) == 2
    validate(rec.to_dict(), "explanation_record")


def test_too_long_justification_twice_gives_schema_violation():
    provider = MockProvider([_answer("p.C", justification="x" * 401)])
    rec = LLMExplainer(provider, CFG)._explain_one("b", 0.1, "p.C", 3, {"test": "p.C"})
    assert not rec.ok and rec.error == "schema_violation" and len(provider.prompts) == 2


def test_wrong_test_name_is_schema_violation_and_timeout_is_reported():
    rec = LLMExplainer(MockProvider([_answer("p.Other")]), CFG)._explain_one("b", 0.1, "p.C", 3, {})
    assert rec.error == "schema_violation"
    rec = LLMExplainer(MockProvider([LLMTimeout("slow")]), CFG)._explain_one("b", 0.1, "p.C", 3, {})
    assert rec.error == "timeout" and rec.prompt_tokens is None


def test_explainer_never_reads_outcomes():
    """Two opposite outcome columns, and none at all, give the same prompts and evidence."""
    runs = []
    for df in (_df([0, 0, 1, 0, 0, 1]), _df([1, 1, 0, 1, 1, 0]), _df().drop(columns=["actual_outcome"])):
        provider = MockProvider([lambda p: _answer("p.C")])
        recs = _explain(LLMExplainer(provider, CFG), df)
        runs.append((provider.prompts, [r.evidence for r in recs]))
    assert runs[0] == runs[1] == runs[2]


def test_one_trace_event_per_explanation():
    trace = _Trace()
    provider = MockProvider(["not json", _answer("p.C")])   # cycles: some records fail, some succeed
    recs = _explain(LLMExplainer(provider, CFG, trace=trace))
    assert len(trace.events) == len(recs) == 3
    for (bid, comp, ev, payload), rec in zip(trace.events, recs):
        assert (bid, comp, ev) == ("PR-1_build1", "explainer", "explanation")
        assert set(payload) == {"test", "budget", "evidence", "justification", "cited_facts", "ok", "error"}
        assert payload["test"] == rec.test and payload["ok"] == rec.ok


# ------------------------------------------------------------- grounding ----

def _record(facts, evidence):
    return ExplanationRecord(build_id="b", budget_fraction=0.1, test="p.E", rank_by_value=5, evidence=evidence,
                             justification="j", cited_facts=list(facts), ok=True, error=None, latency_s=0.0,
                             prompt_tokens=None, completion_tokens=None)


def test_grounding_report_flags_unknown_number():
    ev = build_evidence("p.E", 5, _df(), TESTS, DUR, SELECTED, BUDGET, DIFF_FILES, REASONS, _history_tool, 10)
    facts = ["failures: 0 of 100 runs", "relevance_used: 0.70", "changed_files: core/a/Cache.java",
             "duration_s: 99.5", "changed core/z/Missing.java"]
    rep = grounding_report(_record(facts, ev))
    assert rep == {"n_cited": 5, "n_cited_found": 3, "ungrounded": ["duration_s: 99.5", "changed core/z/Missing.java"]}


def test_grounding_report_accepts_dict_and_empty():
    rep = grounding_report({"evidence": {}, "cited_facts": []})
    assert rep == {"n_cited": 0, "n_cited_found": 0, "ungrounded": []}


@pytest.mark.parametrize("fact", ["skip_cause: did_not_fit", "budget_s: 30.0"])
def test_grounding_report_text_and_numbers_found(fact):
    ev = build_evidence("p.E", 5, _df(), TESTS, DUR, SELECTED, BUDGET, DIFF_FILES, REASONS, _history_tool, 10)
    assert grounding_report(_record([fact], ev))["ungrounded"] == []
