import pytest
import requests

from src.agent.llm_provider import LLMError, LLMTimeout, MockProvider, OllamaProvider


class FakeResponse:
    def __init__(self, body, status=200):
        self.body, self.status_code = body, status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def json(self):
        return self.body


class FakeSession:
    def __init__(self, result):
        self.result, self.sent = result, None

    def post(self, url, json, timeout):
        self.sent = {"url": url, "json": json, "timeout": timeout}
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_ollama_payload_and_token_counts():
    s = FakeSession(FakeResponse({"response": '{"a": 1}', "prompt_eval_count": 12, "eval_count": 5}))
    p = OllamaProvider("m", base_url="http://h:1/", timeout_s=7, session=s)
    assert p.complete("hi") == '{"a": 1}'
    assert s.sent["url"] == "http://h:1/api/generate"
    assert s.sent["timeout"] == 7
    assert s.sent["json"]["format"] == "json" and s.sent["json"]["stream"] is False
    rec = p.calls[-1]
    assert rec.ok and rec.prompt_tokens == 12 and rec.completion_tokens == 5


def test_ollama_json_mode_off():
    s = FakeSession(FakeResponse({"response": "x"}))
    OllamaProvider("m", session=s).complete("hi", json_mode=False)
    assert "format" not in s.sent["json"]


def test_ollama_timeout_maps_to_llm_timeout():
    p = OllamaProvider("m", session=FakeSession(requests.Timeout("slow")))
    with pytest.raises(LLMTimeout):
        p.complete("hi")
    assert p.calls[-1].ok is False and p.calls[-1].error == "timeout"


def test_ollama_http_error():
    p = OllamaProvider("m", session=FakeSession(FakeResponse({}, status=500)))
    with pytest.raises(LLMError):
        p.complete("hi")
    assert p.stats()["failed"] == 1


def test_mock_cycles_and_raises():
    m = MockProvider(["a", LLMTimeout("t"), lambda prompt: prompt.upper()])
    assert m.complete("x") == "a"
    with pytest.raises(LLMTimeout):
        m.complete("x")
    assert m.complete("hey") == "HEY"
    assert m.complete("x") == "a"
    assert m.stats()["calls"] == 4 and m.stats()["failed"] == 1
