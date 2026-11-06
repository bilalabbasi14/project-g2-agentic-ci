"""LLM provider interface: complete(prompt) -> text.

Every call appends an LLMCallRecord (latency, token counts, ok/error, cached,
component) to provider.calls and logs it, so callers can report latency and
token totals per component.
"""
import logging
import os
import time

import requests

from src.contracts import LLMCallRecord

log = logging.getLogger(__name__)

DEFAULT_OLLAMA_URL = "http://localhost:11434"


class LLMError(Exception):
    """Connection, HTTP or protocol failure."""


class LLMTimeout(LLMError):
    """No answer within the configured timeout."""


class LLMProvider:
    model = "unknown"

    def __init__(self, component=None):
        self.calls = []
        self.component = component   # one of TRACE_COMPONENTS, or None

    def complete(self, prompt, json_mode=False):
        raise NotImplementedError

    def _record(self, latency, prompt_tokens=None, completion_tokens=None, error=None, cached=False):
        rec = LLMCallRecord(model=self.model, latency_s=round(latency, 4),
                            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
                            ok=error is None, error=error, cached=cached, component=self.component)
        self.calls.append(rec)
        log.info("llm_call %s", rec.to_dict())
        return rec

    def stats(self):
        ok = [c for c in self.calls if c.ok]
        return {
            "calls": len(self.calls),
            "failed": len(self.calls) - len(ok),
            "cached_calls": sum(1 for c in self.calls if c.cached),
            "mean_latency_s": sum(c.latency_s for c in self.calls) / len(self.calls) if self.calls else None,
            "prompt_tokens": sum(c.prompt_tokens or 0 for c in self.calls),
            "completion_tokens": sum(c.completion_tokens or 0 for c in self.calls),
        }


def _normalise_url(url):
    """Ollama's own OLLAMA_HOST may be given without a scheme (e.g. 127.0.0.1:11434)."""
    url = url.strip().rstrip("/")
    return url if "://" in url else f"http://{url}"


class OllamaProvider(LLMProvider):
    """Local Ollama server, /api/generate, non-streaming.

    base_url priority: explicit argument, then the OLLAMA_HOST environment
    variable, then the config (from_config) or the default local server.
    seed and num_ctx go into the request's `options`; a per-call `options`
    dict overrides them (CachingProvider passes the full options it keyed on).
    """

    def __init__(self, model, base_url=None, timeout_s=60.0, temperature=0.0, json_mode=True,
                 session=None, seed=None, num_ctx=None, component=None):
        super().__init__(component)
        self.model = model
        self.base_url = _normalise_url(base_url or os.environ.get("OLLAMA_HOST") or DEFAULT_OLLAMA_URL)
        self.timeout_s = timeout_s
        self.temperature = temperature
        self.default_json_mode = json_mode
        self.session = session or requests
        self.seed = seed
        self.num_ctx = num_ctx

    @classmethod
    def from_config(cls, cfg, base_url=None, seed=None, component=None):
        llm = cfg["llm"]
        llm_p2 = cfg.get("llm_p2") or {}
        url = base_url or os.environ.get("OLLAMA_HOST") or llm["base_url"]
        return cls(model=llm["model"], base_url=url, timeout_s=llm["timeout_s"],
                   temperature=llm.get("temperature", 0.0), json_mode=llm.get("json_mode", True),
                   seed=seed, num_ctx=llm_p2.get("num_ctx"), component=component)

    def request_options(self, attempt=0):
        """Ollama `options` for a call; a retry (attempt >= 1) uses seed + 1000 * attempt."""
        opts = {"temperature": self.temperature}
        if self.seed is not None:
            opts["seed"] = self.seed + 1000 * attempt
        if self.num_ctx is not None:
            opts["num_ctx"] = self.num_ctx
        return opts

    def complete(self, prompt, json_mode=None, options=None, attempt=0):
        json_mode = self.default_json_mode if json_mode is None else json_mode
        opts = self.request_options(attempt)
        if options:
            opts.update(options)
        payload = {"model": self.model, "prompt": prompt, "stream": False, "options": opts}
        if json_mode:
            payload["format"] = "json"
        t0 = time.perf_counter()
        try:
            r = self.session.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout_s)
            r.raise_for_status()
            body = r.json()
        except requests.Timeout as e:
            self._record(time.perf_counter() - t0, error="timeout")
            raise LLMTimeout(str(e)) from e
        except (requests.RequestException, ValueError) as e:
            self._record(time.perf_counter() - t0, error=type(e).__name__)
            raise LLMError(str(e)) from e
        self._record(time.perf_counter() - t0, body.get("prompt_eval_count"), body.get("eval_count"))
        return body.get("response", "")


class MockProvider(LLMProvider):
    """Returns canned answers in order (cycling). An Exception instance in the
    list is raised instead of returned, e.g. LLMTimeout("...") to simulate a timeout.
    A callable answer is called with the prompt. Extra keyword arguments
    (options, attempt) are accepted and ignored."""

    model = "mock"

    def __init__(self, answers, component=None):
        super().__init__(component)
        self.answers = list(answers)
        self.prompts = []

    def complete(self, prompt, json_mode=False, **_ignored):
        self.prompts.append(prompt)
        ans = self.answers[(len(self.prompts) - 1) % len(self.answers)]
        if callable(ans) and not isinstance(ans, Exception):
            ans = ans(prompt)
        if isinstance(ans, Exception):
            self._record(0.0, error=type(ans).__name__)
            raise ans
        self._record(0.0, prompt_tokens=len(prompt.split()), completion_tokens=len(str(ans).split()))
        return ans


def make_provider(cfg, component=None, base_url=None, seed=None):
    """Provider for one component. With llm_p2.cache on, an OllamaProvider wrapped
    in a CachingProvider; all components share the same cache folder."""
    name = cfg["llm"].get("provider", "ollama")
    if name != "ollama":
        raise ValueError(f"unknown provider: {name}")
    llm_p2 = cfg.get("llm_p2") or {}
    seed = llm_p2.get("seed") if seed is None else seed
    inner = OllamaProvider.from_config(cfg, base_url=base_url, seed=seed, component=component)
    if not llm_p2.get("cache"):
        return inner
    from src.agent.llm_cache import CachingProvider, LLMCache
    from src.settings import repo_path
    options = {"temperature": inner.temperature, "seed": seed, "num_ctx": inner.num_ctx}
    return CachingProvider(inner, LLMCache(repo_path(llm_p2["cache_dir"])), options, component)
