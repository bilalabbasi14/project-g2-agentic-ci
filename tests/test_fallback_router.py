import json
import logging

import pytest

from src.agent.fallback_router import FallbackRouter
from src.agent.llm_provider import LLMError, LLMTimeout, MockProvider
from src.agent.semantic_analyzer import SemanticAnalyzer, make_request
from src.contracts import validate

DANTE = ["t.C", "t.A", "t.B"]
LLM_RANKING = ["t.A", "t.B", "t.C"]


def ok(test, rel=0.5, conf=0.9):
    return json.dumps({"test": test, "relevance": rel, "reason": "r", "confidence": conf})


def reqs(*tests):
    return [make_request("b1", t, "+x", "class X {}", 3000, 3000) for t in tests]


def router(answers, scope="build", log_path=None):
    return FallbackRouter(SemanticAnalyzer(MockProvider(answers)), min_confidence=0.3,
                          scope=scope, log_path=log_path)


def test_all_valid_uses_llm():
    res = router([ok("t.A", 0.9), ok("t.B", 0.1)]).run("b1", reqs("t.A", "t.B"), DANTE)
    assert res.source == "llm" and not res.fallbacks
    assert res.relevance == {"t.A": 0.9, "t.B": 0.1}
    assert res.choose_ranking(LLM_RANKING) == LLM_RANKING


@pytest.mark.parametrize("bad, reason", [
    ("this is not json", "invalid_json"),
    (LLMTimeout("read timed out"), "timeout"),
    (ok("t.B", conf=0.1), "low_confidence"),
    (json.dumps({"test": "t.B", "relevance": 2, "reason": "r"}), "schema_violation"),
    (LLMError("connection refused"), "provider_error"),
])
def test_fallback_triggers_and_is_logged(bad, reason, tmp_path, caplog):
    log_file = tmp_path / "fallbacks.jsonl"
    r = router([ok("t.A"), bad, ok("t.C")], log_path=log_file)
    with caplog.at_level(logging.WARNING):
        res = r.run("b1", reqs("t.A", "t.B", "t.C"), DANTE)
    assert res.fell_back
    assert res.choose_ranking(LLM_RANKING) == DANTE
    assert res.relevance == {}
    assert [f.reason for f in res.fallbacks] == [reason]
    assert res.fallbacks[0].test == "t.B"
    # build scope stops calling the model after the first rejection
    assert len(r.analyzer.provider.prompts) == 2
    lines = [json.loads(x) for x in log_file.read_text().splitlines()]
    assert len(lines) == 1 and lines[0]["reason"] == reason
    validate(lines[0], "fallback_record")
    assert any(reason in m for m in caplog.messages)


def test_missing_confidence_is_accepted():
    ans = json.dumps({"test": "t.A", "relevance": 0.4, "reason": "r"})
    res = router([ans]).run("b1", reqs("t.A"), DANTE)
    assert res.source == "llm" and res.relevance == {"t.A": 0.4}


def test_test_scope_keeps_other_scores():
    res = router([ok("t.A", 0.8), LLMTimeout("t"), "garbage"], scope="test").run(
        "b1", reqs("t.A", "t.B", "t.C"), DANTE)
    assert res.source == "llm"
    assert res.relevance == {"t.A": 0.8}
    assert [(f.test, f.reason) for f in res.fallbacks] == [("t.B", "timeout"), ("t.C", "invalid_json")]


def test_bad_scope():
    with pytest.raises(ValueError):
        FallbackRouter(None, scope="x")
