"""On-disk LLM answer cache and a caching provider wrapper.

The key is the SHA-256 of model + prompt + options (temperature, seed,
num_ctx) + json_mode, so repeated runs with seeds 1, 2, 3 each make their own
calls while reruns and ablations with the same seed reuse answers. Only
successful calls are cached; a cached entry keeps the original latency and
token counts so cost numbers stay real (docs/PROJECT_CONTEXT.md §7).
"""
import hashlib
import json
import logging
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from src.agent.llm_provider import LLMProvider

log = logging.getLogger(__name__)


def make_key(model, prompt, options, json_mode):
    """SHA-256 hex digest identifying one LLM call."""
    blob = json.dumps({"model": model, "prompt": prompt, "options": options, "json_mode": bool(json_mode)},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class LLMCache:
    """Entries live at <cache_dir>/<key[:2]>/<key>.json."""

    def __init__(self, cache_dir):
        self.dir = Path(cache_dir)

    def _path(self, key):
        return self.dir / key[:2] / f"{key}.json"

    def get(self, key):
        """The stored entry, or None on a miss. A corrupt or unreadable file is a miss."""
        path = self._path(key)
        if not path.exists():
            return None
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(entry, dict) or "response" not in entry:
                raise ValueError("not a cache entry")
            return entry
        except (OSError, ValueError) as e:
            log.warning("llm cache: ignoring unreadable entry %s (%s)", path, e)
            return None

    def put(self, key, entry):
        """Write atomically: a temporary file in the same folder, then os.replace,
        so concurrent writers never leave a half-written entry."""
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{key}.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(entry, f, ensure_ascii=False)
            os.replace(tmp, path)
        except BaseException:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise


class CachingProvider(LLMProvider):
    """Wraps another provider: a cache hit returns the stored answer, a miss calls
    the inner provider and stores the answer. Records carry cached and component."""

    def __init__(self, inner, cache, options, component=None):
        super().__init__(component)
        self.inner = inner
        self.cache = cache
        self.options = dict(options)
        self.model = inner.model

    def options_for(self, attempt=0):
        """Options for this attempt; a retry uses seed + 1000 * attempt so it can differ."""
        opts = dict(self.options)
        if opts.get("seed") is not None:
            opts["seed"] = opts["seed"] + 1000 * attempt
        return opts

    def complete(self, prompt, json_mode=None, attempt=0):
        if json_mode is None:
            json_mode = getattr(self.inner, "default_json_mode", False)
        opts = self.options_for(attempt)
        key = make_key(self.model, prompt, opts, json_mode)
        hit = self.cache.get(key)
        if hit is not None:
            self._record(hit.get("latency_s") or 0.0, hit.get("prompt_tokens"), hit.get("completion_tokens"),
                         cached=True)
            return hit["response"]
        n_before = len(self.inner.calls)
        try:
            text = self.inner.complete(prompt, json_mode, options=opts)
        except Exception:
            inner_rec = self.inner.calls[-1] if len(self.inner.calls) > n_before else None
            self._record(inner_rec.latency_s if inner_rec else 0.0,
                         error=inner_rec.error if inner_rec else "provider_error")
            raise
        inner_rec = self.inner.calls[-1] if len(self.inner.calls) > n_before else None
        latency = inner_rec.latency_s if inner_rec else 0.0
        p_tok = inner_rec.prompt_tokens if inner_rec else None
        c_tok = inner_rec.completion_tokens if inner_rec else None
        self.cache.put(key, {"response": text, "latency_s": latency, "prompt_tokens": p_tok,
                             "completion_tokens": c_tok, "model": self.model,
                             "created": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        self._record(latency, p_tok, c_tok, cached=False)
        return text
