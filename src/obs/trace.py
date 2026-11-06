"""Trace logger for agent trajectories (docs/PROJECT_CONTEXT.md §5.3 step 9).

Every component writes TraceEvents through the same logger; each event is one
JSON line in <trace_dir>/<run_id>/<build_id>.jsonl, with a step counter per
build starting at 1. Components take `trace=None` and use `trace or NullTrace()`,
so code without a logger behaves exactly as before.

Payload conventions (every component must follow them):

| Component         | Event       | When                                               | Payload keys |
|-------------------|-------------|----------------------------------------------------|--------------|
| pipeline          | state       | start of a build; after DANTE scores; after the    | stage ("loaded", "dante_scored", "shortlisted", "selected"), plus the counts and names for that stage (n_candidates, shortlist, method, budget, selected) |
|                   |             | shortlist; after selection per method and budget   |              |
| semantic_analyzer | llm_call    | each relevance call                                | test, prompt, response, attempt, cached, prompt_tokens, completion_tokens |
| fallback_router   | fallback    | each fallback                                      | the FallbackRecord as a dict |
| orchestrator      | llm_call    | each orchestrator LLM call                         | step, prompt, response, attempt, cached |
| orchestrator      | tool_call   | each tool call                                     | tool, args, output, ok, error |
| orchestrator      | decision    | final decision                                     | w, confidence, source, reason, tool_calls (count) |
| explainer         | explanation | each explanation                                   | test, budget, evidence, justification, cited_facts, ok, error |
| single_call       | llm_call    | the single call                                    | n_tests, prompt, response, cached |

A failed LLM call is logged with response null and an extra key `error`.
"""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from src.contracts import TraceEvent, validate
from src.settings import repo_path

TRUNCATION_MARKER = "…[truncated]"


def truncate_strings(value, max_chars):
    """Copy of value with every string (inside dicts and lists too) cut to max_chars + marker."""
    if isinstance(value, str):
        return value if len(value) <= max_chars else value[:max_chars] + TRUNCATION_MARKER
    if isinstance(value, dict):
        return {k: truncate_strings(v, max_chars) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [truncate_strings(v, max_chars) for v in value]
    return value


class TraceLogger:
    def __init__(self, trace_dir, run_id, max_text_chars=8000):
        self.dir = Path(trace_dir) / run_id
        self.run_id = run_id
        self.max_text_chars = max_text_chars
        self._steps = defaultdict(int)

    @classmethod
    def from_config(cls, cfg, run_id):
        t = cfg["trace"]
        return cls(repo_path(t["dir"]), run_id, t["max_text_chars"])

    def path(self, build_id):
        return self.dir / f"{build_id}.jsonl"

    def event(self, build_id, component, event, payload, latency_s=None):
        """Validate and append one event; returns the TraceEvent."""
        self._steps[build_id] += 1
        ev = TraceEvent(run_id=self.run_id, build_id=build_id, component=component, event=event,
                        step=self._steps[build_id], payload=truncate_strings(payload, self.max_text_chars),
                        latency_s=latency_s,
                        ts=datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"))
        validate(ev.to_dict(), "trace_event")
        self.dir.mkdir(parents=True, exist_ok=True)
        with open(self.path(build_id), "a", encoding="utf-8") as f:
            f.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")
        return ev


class NullTrace:
    """Drop-in for TraceLogger that records nothing."""

    def event(self, build_id, component, event, payload, latency_s=None):
        return None
