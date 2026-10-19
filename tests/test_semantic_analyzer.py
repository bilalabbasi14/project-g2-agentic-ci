import json

import pytest

from src.agent.llm_provider import LLMTimeout, MockProvider
from src.agent.semantic_analyzer import (
    TRUNCATION_MARK, InvalidJSONError, SchemaViolationError, SemanticAnalyzer, anonymise,
    build_prompt, make_request, parse_response, truncate,
)

DIFF = """From: Jane Doe <jane@example.org>
Date: 2021-03-04T10:11:12+01:00
diff --git a/core/Foo.java b/core/Foo.java
index a910aa8cb66..17e6ddff116 100644
--- a/core/Foo.java
+++ b/core/Foo.java
@@ -1,2 +1,2 @@
-    int max = 10; // set 2020-01-01 by commit 56b612b2045cf420eae1b506db44fe438da2f4f7
+    int max = 20;
"""

TEST = "org.example.FooTest"


def test_anonymise_removes_identifying_data():
    out = anonymise(DIFF + " * @author Jane Doe\n")
    for s in ("Jane", "jane@example.org", "a910aa8cb66", "56b612b2045c", "2021-03-04", "2020-01-01"):
        assert s not in out
    assert "int max = 20;" in out
    assert "<hash>" in out and "<date>" in out


def test_anonymise_keeps_plain_identifiers():
    assert anonymise("int deadline = 1000000;") == "int deadline = 1000000;"


def test_truncate():
    assert truncate("abc", 5) == "abc"
    assert truncate("abcdef", 3) == "abc" + TRUNCATION_MARK


def test_make_request_and_prompt():
    req = make_request("b1", TEST, DIFF, "class FooTest {}", max_diff_chars=60, max_test_chars=100)
    assert req.diff_chunk.endswith(TRUNCATION_MARK)
    assert "a910aa8cb66" not in req.diff_chunk
    p = build_prompt(req)
    assert TEST in p and "class FooTest {}" in p


def test_parse_valid_and_fenced():
    good = {"test": TEST, "relevance": 0.7, "reason": "touches Foo", "confidence": 0.9}
    r = parse_response(json.dumps(good), TEST)
    assert r.relevance == 0.7 and r.confidence == 0.9
    r2 = parse_response("```json\n" + json.dumps(good) + "\n```", TEST)
    assert r2.to_dict() == good


def test_parse_accepts_simple_name():
    r = parse_response(json.dumps({"test": "FooTest", "relevance": 0.1, "reason": "x"}), TEST)
    assert r.test == TEST


@pytest.mark.parametrize("text", ["not json", "[1, 2]", ""])
def test_parse_invalid_json(text):
    with pytest.raises(InvalidJSONError):
        parse_response(text, TEST)


@pytest.mark.parametrize("obj", [
    {"test": TEST, "relevance": 1.3, "reason": "x"},
    {"test": TEST, "reason": "x"},
    {"test": "other.BarTest", "relevance": 0.5, "reason": "x"},
    {"test": TEST, "relevance": 0.5, "reason": "x", "extra": True},
])
def test_parse_schema_violation(obj):
    with pytest.raises(SchemaViolationError):
        parse_response(json.dumps(obj), TEST)


def test_analyzer_with_mock_provider():
    m = MockProvider([json.dumps({"test": TEST, "relevance": 0.4, "reason": "r"})])
    req = make_request("b1", TEST, DIFF, "class FooTest {}", 3000, 3000)
    assert SemanticAnalyzer(m).analyze(req).relevance == 0.4
    assert TEST in m.prompts[0]


def test_analyzer_propagates_timeout():
    req = make_request("b1", TEST, DIFF, "", 3000, 3000)
    with pytest.raises(LLMTimeout):
        SemanticAnalyzer(MockProvider([LLMTimeout("t")])).analyze(req)
