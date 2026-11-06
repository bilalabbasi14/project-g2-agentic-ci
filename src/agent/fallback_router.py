"""Fallback router around the semantic analyzer.

For each relevance request of a build it calls the analyzer. A timed-out,
failed, invalid-JSON or schema-violating call is retried max_retries times
(llm_p2.max_retries, via src.agent.retry.complete_and_parse); a call that still
fails, or that reports low confidence, is rejected. Each rejection becomes a
FallbackRecord (kept in the result, logged with the number of attempts, and
appended to a JSONL file if log_path is set).

scope="build": the first rejection stops LLM calls for the build and the
build uses the supplied DANTE ranking (source "dante_fallback").
scope="test": only the rejected test loses its LLM score; the caller keeps
its baseline relevance for that test.

The DANTE ranking is passed in; nothing here computes baseline scores.
"""
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from src.contracts import FallbackRecord, RelevanceResponse

log = logging.getLogger(__name__)


@dataclass
class RouterResult:
    build_id: str
    source: str                                         # "llm" or "dante_fallback"
    relevance: Dict[str, float] = field(default_factory=dict)
    responses: List[RelevanceResponse] = field(default_factory=list)
    fallbacks: List[FallbackRecord] = field(default_factory=list)
    dante_ranking: Optional[List[str]] = None

    @property
    def fell_back(self):
        return self.source == "dante_fallback"

    def choose_ranking(self, llm_ranking):
        """The ranking to use for this build: DANTE's after a build fallback, else the LLM one."""
        return list(self.dante_ranking) if self.fell_back else list(llm_ranking)


class FallbackRouter:
    def __init__(self, analyzer, min_confidence=0.0, scope="build", log_path=None, max_retries=0):
        if scope not in ("build", "test"):
            raise ValueError("scope must be 'build' or 'test'")
        self.analyzer = analyzer
        self.min_confidence = min_confidence
        self.scope = scope
        self.log_path = Path(log_path) if log_path else None
        self.max_retries = max_retries

    @classmethod
    def from_config(cls, analyzer, cfg, log_path=None):
        fb = cfg["fallback"]
        max_retries = (cfg.get("llm_p2") or {}).get("max_retries", 0)
        return cls(analyzer, fb["min_confidence"], fb["scope"], log_path, max_retries)

    def _call(self, request):
        """Return (response, None, attempts) or (None, (reason, detail), attempts)."""
        resp, reason, detail, attempts = self.analyzer.analyze_with_retry(request, self.max_retries)
        if reason:
            return None, (reason, detail), attempts
        if resp.confidence is not None and resp.confidence < self.min_confidence:
            return None, ("low_confidence", f"confidence {resp.confidence} < {self.min_confidence}"), attempts
        return resp, None, attempts

    def _record(self, result, build_id, test, reason, detail, attempts=1):
        rec = FallbackRecord(build_id=build_id, reason=reason, detail=detail[:300], test=test)
        result.fallbacks.append(rec)
        log.warning("fallback %s attempts=%d", rec.to_dict(), attempts)
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec.to_dict()) + "\n")

    def run(self, build_id, requests, dante_ranking):
        result = RouterResult(build_id=build_id, source="llm", dante_ranking=list(dante_ranking))
        for req in requests:
            resp, err, attempts = self._call(req)
            if err:
                self._record(result, build_id, req.test, *err, attempts=attempts)
                if self.scope == "build":
                    result.source = "dante_fallback"
                    result.relevance.clear()
                    break
                continue
            result.responses.append(resp)
            result.relevance[req.test] = resp.relevance
        return result
