"""LLM cache, caching provider, retry helper, seeds and per-component accounting (no Ollama needed)."""
import json

import pytest
import requests

from src.agent.llm_cache import CachingProvider, LLMCache, make_key
from src.agent.llm_provider import LLMProvider, LLMTimeout, MockProvider, OllamaProvider, make_provider
from src.agent.retry import complete_and_parse
from src.agent.semantic_analyzer import InvalidJSONError, SchemaViolationError
from src.settings import load_config

OPTS = {"temperature": 0.0, "seed": 1, "num_ctx": 8192}


class FakeInner(LLMProvider):
    """Records every call's options; answers from a list (Exceptions are raised)."""
    model = "fake-model"

    def __init__(self, answers, latency=2.5):
        super().__init__()
        self.answers, self.latency, self.options_seen = list(answers), latency, []
        self.default_json_mode = True

    def complete(self, prompt, json_mode=None, options=None):
        self.options_seen.append(options)
        ans = self.answers[len(self.options_seen) - 1]
        if isinstance(ans, Exception):
            self._record(self.latency, error="timeout")
            raise ans
        self._record(self.latency, 100, 7)
        return ans


def _cp(tmp_path, inner, component=None, options=OPTS):
    return CachingProvider(inner, LLMCache(tmp_path / "cache"), options, component)


def test_key_is_stable_and_sensitive():
    base = make_key("m", "p", OPTS, True)
    assert base == make_key("m", "p", dict(reversed(list(OPTS.items()))), True)
    for other in (make_key("m2", "p", OPTS, True), make_key("m", "p2", OPTS, True),
                  make_key("m", "p", {**OPTS, "seed": 2}, True), make_key("m", "p", {**OPTS, "num_ctx": 4096}, True),
                  make_key("m", "p", OPTS, False)):
        assert other != base


def test_miss_then_hit_keeps_original_latency(tmp_path):
    inner = FakeInner(["answer"], latency=2.5)
    cp = _cp(tmp_path, inner)
    assert cp.complete("prompt") == "answer"
    assert cp.complete("prompt") == "answer"
    assert len(inner.options_seen) == 1                      # inner called once
    first, second = cp.calls
    assert (first.cached, second.cached) == (False, True)
    assert second.latency_s == 2.5 and second.prompt_tokens == 100 and second.completion_tokens == 7
    assert cp.model == "fake-model"
    assert cp.stats()["cached_calls"] == 1 and cp.stats()["calls"] == 2


def test_timeout_is_not_cached(tmp_path):
    inner = FakeInner([LLMTimeout("slow"), "late answer"])
    cp = _cp(tmp_path, inner)
    with pytest.raises(LLMTimeout):
        cp.complete("prompt")
    assert cp.calls[-1].ok is False and cp.calls[-1].error == "timeout"
    assert cp.complete("prompt") == "late answer"            # reached the inner provider again
    assert len(inner.options_seen) == 2


def test_put_is_atomic_and_corrupt_file_is_a_miss(tmp_path, caplog):
    cache = LLMCache(tmp_path / "c")
    key = make_key("m", "p", OPTS, True)
    cache.put(key, {"response": "x", "latency_s": 1.0})
    assert cache.get(key)["response"] == "x"
    assert (tmp_path / "c" / key[:2] / f"{key}.json").exists()
    assert not list((tmp_path / "c").rglob("*.tmp"))
    (tmp_path / "c" / key[:2] / f"{key}.json").write_text("{not json")
    assert cache.get(key) is None
    assert any("unreadable" in m for m in caplog.messages)


def test_retry_attempt_uses_seed_plus_1000(tmp_path):
    inner = FakeInner(["a0", "a1"])
    cp = _cp(tmp_path, inner)
    cp.complete("prompt", attempt=0)
    cp.complete("prompt", attempt=1)
    assert [o["seed"] for o in inner.options_seen] == [1, 1001]
    assert make_key(cp.model, "prompt", cp.options_for(0), True) != make_key(cp.model, "prompt", cp.options_for(1), True)


def _parse(text):
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise InvalidJSONError(str(e)) from e
    if "ok" not in obj:
        raise SchemaViolationError("missing ok")
    return obj


def test_complete_and_parse_retries_once():
    res, reason, detail, attempts = complete_and_parse(MockProvider(["garbage", '{"ok": 1}']), "p", _parse)
    assert res == {"ok": 1} and reason is None and attempts == 2
    res, reason, _, attempts = complete_and_parse(MockProvider(["garbage", "garbage"]), "p", _parse)
    assert res is None and reason == "invalid_json" and attempts == 2
    res, reason, _, attempts = complete_and_parse(MockProvider([LLMTimeout("t")]), "p", _parse)
    assert res is None and reason == "timeout" and attempts == 2
    _, reason, _, _ = complete_and_parse(MockProvider(['{"x": 1}']), "p", _parse)
    assert reason == "schema_violation"
    _, _, _, attempts = complete_and_parse(MockProvider(["garbage"]), "p", _parse, max_retries=0)
    assert attempts == 1


def test_complete_and_parse_with_provider_without_attempt():
    class Plain:
        def __init__(self):
            self.n = 0

        def complete(self, prompt, json_mode=False):
            self.n += 1
            return '{"ok": 1}' if self.n > 1 else "bad"
    res, reason, _, attempts = complete_and_parse(Plain(), "p", _parse)
    assert res == {"ok": 1} and attempts == 2


def test_complete_and_parse_passes_attempt_to_caching_provider(tmp_path):
    inner = FakeInner(["bad", '{"ok": 1}'])
    res, _, _, attempts = complete_and_parse(_cp(tmp_path, inner), "p", _parse)
    assert res == {"ok": 1} and attempts == 2
    assert [o["seed"] for o in inner.options_seen] == [1, 1001]


class FakeResponse:
    def __init__(self, body):
        self.body, self.status_code = body, 200

    def raise_for_status(self):
        pass

    def json(self):
        return self.body


class FakeSession:
    def __init__(self, result):
        self.result, self.sent = result, []

    def post(self, url, json, timeout):
        self.sent.append({"url": url, "json": json})
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_ollama_sends_seed_and_num_ctx_and_override():
    s = FakeSession(FakeResponse({"response": "x", "prompt_eval_count": 3, "eval_count": 1}))
    p = OllamaProvider("m", base_url="http://h:1", seed=7, num_ctx=4096, session=s)
    p.complete("hi")
    assert s.sent[-1]["json"]["options"] == {"temperature": 0.0, "seed": 7, "num_ctx": 4096}
    p.complete("hi", attempt=1)
    assert s.sent[-1]["json"]["options"]["seed"] == 1007
    p.complete("hi", options={"seed": 99, "num_ctx": 16384})
    assert s.sent[-1]["json"]["options"] == {"temperature": 0.0, "seed": 99, "num_ctx": 16384}
    # without seed / num_ctx only the temperature is sent (Phase 1 behaviour)
    OllamaProvider("m", base_url="http://h:1", session=s).complete("hi")
    assert s.sent[-1]["json"]["options"] == {"temperature": 0.0}


def test_ollama_base_url_priority(monkeypatch):
    cfg = load_config()
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    assert OllamaProvider.from_config(cfg).base_url == cfg["llm"]["base_url"].rstrip("/")
    monkeypatch.setenv("OLLAMA_HOST", "127.0.0.1:11435")
    assert OllamaProvider.from_config(cfg).base_url == "http://127.0.0.1:11435"
    assert OllamaProvider.from_config(cfg, base_url="http://other:1").base_url == "http://other:1"
    assert OllamaProvider("m").base_url == "http://127.0.0.1:11435"


def test_component_on_every_record(tmp_path):
    s = FakeSession(FakeResponse({"response": "x"}))
    inner = OllamaProvider("m", base_url="http://h:1", session=s, component="orchestrator")
    cp = _cp(tmp_path, inner, component="orchestrator")
    cp.complete("a")
    cp.complete("a")
    s.result = requests.Timeout("slow")
    with pytest.raises(LLMTimeout):
        cp.complete("b")
    assert [c.component for c in cp.calls] == ["orchestrator"] * 3
    assert all(c.component == "orchestrator" for c in inner.calls)
    m = MockProvider(["x"], component="orchestrator")
    m.complete("p", options={"seed": 1}, attempt=1)               # new kwargs accepted and ignored
    assert m.calls[-1].component == "orchestrator"


def test_make_provider(tmp_path):
    cfg = load_config()
    cfg["llm_p2"] = {**cfg["llm_p2"], "cache": True, "cache_dir": str(tmp_path / "llm"), "seed": 1}
    p = make_provider(cfg, component="orchestrator", base_url="http://h:2", seed=3)
    assert isinstance(p, CachingProvider) and isinstance(p.inner, OllamaProvider)
    assert p.component == "orchestrator" and p.inner.base_url == "http://h:2"
    assert p.options["seed"] == 3 and p.options["num_ctx"] == cfg["llm_p2"]["num_ctx"]
    assert make_provider(cfg).options["seed"] == 1                 # default seed from llm_p2
    cfg["llm_p2"]["cache"] = False
    plain = make_provider(cfg, component="semantic_analyzer")
    assert isinstance(plain, OllamaProvider) and plain.component == "semantic_analyzer"
