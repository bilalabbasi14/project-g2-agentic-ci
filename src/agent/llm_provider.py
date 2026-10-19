"""LLM provider interface: complete(prompt) -> text.

Every call appends an LLMCallRecord (latency, token counts, ok/error) to
provider.calls and logs it, so callers can report latency and token totals.
"""
import logging
import time

import requests

from src.contracts import LLMCallRecord

log = logging.getLogger(__name__)


class LLMError(Exception):
    """Connection, HTTP or protocol failure."""


class LLMTimeout(LLMError):
    """No answer within the configured timeout."""


class LLMProvider:
    model = "unknown"

    def __init__(self):
        self.calls = []

    def complete(self, prompt, json_mode=False):
        raise NotImplementedError

    def _record(self, latency, prompt_tokens=None, completion_tokens=None, error=None):
        rec = LLMCallRecord(model=self.model, latency_s=round(latency, 4),
                            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
                            ok=error is None, error=error)
        self.calls.append(rec)
        log.info("llm_call %s", rec.to_dict())
        return rec

    def stats(self):
        ok = [c for c in self.calls if c.ok]
        return {
            "calls": len(self.calls),
            "failed": len(self.calls) - len(ok),
            "mean_latency_s": sum(c.latency_s for c in self.calls) / len(self.calls) if self.calls else None,
            "prompt_tokens": sum(c.prompt_tokens or 0 for c in self.calls),
            "completion_tokens": sum(c.completion_tokens or 0 for c in self.calls),
        }


class OllamaProvider(LLMProvider):
    """Local Ollama server, /api/generate, non-streaming."""

    def __init__(self, model, base_url="http://localhost:11434", timeout_s=60.0,
                 temperature=0.0, json_mode=True, session=None):
        super().__init__()
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.temperature = temperature
        self.default_json_mode = json_mode
        self.session = session or requests

    @classmethod
    def from_config(cls, cfg):
        llm = cfg["llm"]
        return cls(model=llm["model"], base_url=llm["base_url"], timeout_s=llm["timeout_s"],
                   temperature=llm.get("temperature", 0.0), json_mode=llm.get("json_mode", True))

    def complete(self, prompt, json_mode=None):
        json_mode = self.default_json_mode if json_mode is None else json_mode
        payload = {"model": self.model, "prompt": prompt, "stream": False,
                   "options": {"temperature": self.temperature}}
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
    A callable answer is called with the prompt."""

    model = "mock"

    def __init__(self, answers):
        super().__init__()
        self.answers = list(answers)
        self.prompts = []

    def complete(self, prompt, json_mode=False):
        self.prompts.append(prompt)
        ans = self.answers[(len(self.prompts) - 1) % len(self.answers)]
        if callable(ans) and not isinstance(ans, Exception):
            ans = ans(prompt)
        if isinstance(ans, Exception):
            self._record(0.0, error=type(ans).__name__)
            raise ans
        self._record(0.0, prompt_tokens=len(prompt.split()), completion_tokens=len(str(ans).split()))
        return ans


def make_provider(cfg):
    name = cfg["llm"].get("provider", "ollama")
    if name == "ollama":
        return OllamaProvider.from_config(cfg)
    raise ValueError(f"unknown provider: {name}")
