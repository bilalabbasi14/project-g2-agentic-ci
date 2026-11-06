"""Orchestrator Agent (Gap 3): chooses the history weight w for one build.

docs/PROJECT_CONTEXT.md §5.1 (base_w = w·History + (1 − w)·R^1.2; w = 2/3 is
DANTE), §5.3 step 5 and §5.4. The orchestrator gets build features and the
shortlist with all scores, may call up to `max_tool_calls` tools
(history_retrieval, diff_reader) to inspect evidence, and must answer with
{w, confidence, reason}. Every answer is validated against `orchestrator_step`
and retried once (src.agent.retry). A failure that survives the retry, or a
final answer with confidence < min_confidence, gives a fallback decision with
w = fallback_w (DANTE) and a FallbackRecord.

Features are computed from scores, durations, the diff and the history only;
the outcomes of the target build (`actual_outcome`, TestCase.outcome) are never
read.
"""
import json
import os
import re
import statistics

import jsonschema

from src.agent.retry import _accepts_attempt, complete_and_parse
from src.agent.semantic_analyzer import InvalidJSONError, SchemaViolationError, anonymise
from src.contracts import FallbackRecord, OrchestratorDecision, OrchestratorInput, validate
from src.obs.trace import NullTrace

ORCH_PROMPT_VERSION = "o1"

LLM_SOURCES = ("llm_shortlist", "llm_all_individual", "llm_single_call")

# feature name -> one-line meaning shown in the prompt (order = prompt order)
FEATURE_DOCS = {
    "n_code_files": "number of changed code files in the diff",
    "n_dirs": "number of distinct folders those files are in",
    "lines_added": "added lines in the diff",
    "lines_removed": "removed lines in the diff",
    "recent_failure_density": "share of the last 10 history builds with at least one failing test",
    "n_candidates": "number of candidate test classes",
    "shortlist_size": "number of shortlisted test classes (shown below)",
    "rel_mean_shortlist": "mean relevance used over the shortlisted tests",
    "rel_max": "highest relevance used over all candidates",
    "n_rel_ge_05": "shortlisted tests with relevance >= 0.5",
    "hist_max": "highest history score over all candidates",
    "hist_mean_shortlist": "mean history score over the shortlisted tests",
}

PROMPT_TEMPLATE = """You help choose which regression tests to run for one code change (one CI build).
Each candidate test has two scores:
- history: how often and how recently the test failed in earlier builds (0 to 1);
- relevance: how closely the test is related to the changed code (0 to 1).
Tests are ranked by  w * history + (1 - w) * relevance^1.2 , and the top of the ranking is run.

Your task: choose how much to trust history versus relevance for THIS build, as one number w from 0 to 1.
- w near 1: trust past failures (good when failures repeat and the relevance scores look weak or flat).
- w near 0: trust the relevance judgement (good when the change is focused and clearly points at specific tests).
- The fixed choice of the DANTE method is w = 0.67; choose it when you see no reason to move away from it.

Relevance source for this build: {relevance_source}

Build features:
{features}

Changed files ({n_files}):
{files}

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
{shortlist}

Tools you may call (at most {max_tools} calls in total, {tools_left} left):
{tools}

Observations from earlier tool calls:
{observations}

Answer with a single JSON object and nothing else, in one of these two shapes.
To call a tool:
{{"action": "call_tool", "tool": "history_retrieval", "args": {{"test": "org.example.FooTest"}}, "reason": "check whether FooTest failed recently"}}
To give the final answer:
{{"action": "final", "w": 0.5, "confidence": 0.8, "reason": "the change is focused and two tests have high relevance"}}
confidence (0 to 1) is how sure you are that your w is better than 0.67. reason is one short sentence.{forced}"""

FORCED_FINAL = "\n\nTool limit reached. You must now give the final answer."
# forced before max_tool_calls tools were used, because only max_tool_calls + 2 LLM calls are allowed
FORCED_FINAL_CALLS = "\n\nCall limit reached. You must now give the final answer."


def _mean(values):
    values = list(values)
    return float(statistics.fmean(values)) if values else 0.0


def relevance_used(test, df, relevance, relevance_source):
    """R(t) as used for ranking (§5.2): 0 for "none"; TF-IDF (or the given value)
    for "tfidf"; the LLM value for LLM sources, 0 for tests the LLM did not score."""
    if relevance_source == "none":
        return 0.0
    if relevance_source == "tfidf":
        if test in relevance:
            return float(relevance[test])
        return float(df.at[test, "tfidf_relevance"]) if test in df.index else 0.0
    return float(relevance.get(test, 0.0))


def build_features(build, history, df, shortlist, relevance, relevance_source):
    """The 12 build features (all floats). Never reads target-build outcomes."""
    files = list(build.diff_files)
    short = [t for t in shortlist if t in df.index]
    frames = list(history.frames)[-10:]
    failing = sum(1 for f in frames if "outcome" in f.columns and (f["outcome"] == 1).any())
    rel_all = [relevance_used(t, df, relevance, relevance_source) for t in df.index]
    rel_short = [relevance_used(t, df, relevance, relevance_source) for t in short]
    return {
        "n_code_files": float(len(files)),
        "n_dirs": float(len({os.path.dirname(p.replace("\\", "/")) for p in files})),
        "lines_added": float(sum(v.get("added", 0) for v in build.diff_files.values())),
        "lines_removed": float(sum(v.get("removed", 0) for v in build.diff_files.values())),
        "recent_failure_density": failing / len(frames) if frames else 0.0,
        "n_candidates": float(len(df)),
        "shortlist_size": float(len(shortlist)),
        "rel_mean_shortlist": _mean(rel_short),
        "rel_max": float(max(rel_all)) if rel_all else 0.0,
        "n_rel_ge_05": float(sum(1 for r in rel_short if r >= 0.5)),
        "hist_max": float(df["history_score"].max()) if len(df) else 0.0,
        "hist_mean_shortlist": _mean(df.at[t, "history_score"] for t in short),
    }


def make_input(build, history, df, shortlist, relevance, relevance_source, budgets):
    """OrchestratorInput for one build and relevance source (no outcomes)."""
    llm = relevance_source in LLM_SOURCES
    items = []
    for t in shortlist:
        if t not in df.index:
            continue
        items.append({"test": t,
                      "history_score": float(df.at[t, "history_score"]),
                      "tfidf_relevance": float(df.at[t, "tfidf_relevance"]),
                      "llm_relevance": float(relevance[t]) if llm and t in relevance else None,
                      "duration": float(df.at[t, "duration"])})
    return OrchestratorInput(build_id=build.key,
                             features=build_features(build, history, df, shortlist, relevance, relevance_source),
                             shortlist=items, changed_files=sorted(build.diff_files),
                             budget_fractions=[float(b) for b in budgets], relevance_source=relevance_source)


def parse_step(text, final_only=False):
    """json.loads + validate(orchestrator_step); with final_only, a call_tool step is rejected."""
    s = (text or "").strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", s, re.DOTALL)
    if fence:
        s = fence.group(1)
    try:
        obj = json.loads(s)
    except (json.JSONDecodeError, TypeError) as e:
        raise InvalidJSONError(f"not JSON: {str(text)[:200]!r}") from e
    if not isinstance(obj, dict):
        raise InvalidJSONError(f"JSON is not an object: {str(text)[:200]!r}")
    try:
        validate(obj, "orchestrator_step")
    except jsonschema.ValidationError as e:
        raise SchemaViolationError(e.message) from e
    if final_only and obj["action"] != "final":
        raise SchemaViolationError("tool limit reached but the answer is not a final answer")
    return obj


def _fmt(x):
    return "-" if x is None else f"{x:.3f}"


class _TracedProvider:
    """Passes calls on to the real provider and writes one orchestrator llm_call
    trace event per call (including retries)."""

    def __init__(self, orch, build_id, step):
        self.orch, self.build_id, self.step = orch, build_id, step
        self.inner_takes_attempt = _accepts_attempt(orch.provider)

    def complete(self, prompt, json_mode=None, attempt=0):
        p = self.orch.provider
        try:
            if self.inner_takes_attempt:
                text = p.complete(prompt, json_mode, attempt=attempt)
            else:
                text = p.complete(prompt, json_mode)
        except Exception as e:
            self._event(prompt, None, attempt, type(e).__name__)
            raise
        self._event(prompt, text, attempt)
        return text

    def _event(self, prompt, response, attempt, error=None):
        calls = getattr(self.orch.provider, "calls", None)
        rec = calls[-1] if calls else None
        payload = {"step": self.step, "prompt": prompt, "response": response, "attempt": attempt,
                   "cached": bool(getattr(rec, "cached", False))}
        if error:
            payload["error"] = error
        self.orch.trace.event(self.build_id, "orchestrator", "llm_call", payload,
                              latency_s=getattr(rec, "latency_s", None))


class LLMOrchestrator:
    """Implements OrchestratorLike.decide (src/contracts/interfaces.py)."""

    def __init__(self, provider, cfg, trace=None):
        o = cfg["orchestrator"]
        self.provider = provider
        self.max_tool_calls = int(o["max_tool_calls"])
        self.min_confidence = float(o["min_confidence"])
        self.fallback_w = float(o["fallback_w"])
        self.observation_max_chars = int(o["observation_max_chars"])
        self.max_retries = int((cfg.get("llm_p2") or {}).get("max_retries", 1))
        self.trace = trace or NullTrace()
        self.prompt_version = ORCH_PROMPT_VERSION

    @property
    def max_llm_calls(self):
        """Hard safety limit per decision, whatever the model answers."""
        return self.max_tool_calls + 2

    def build_prompt(self, inp, specs, observations, tools_used, forced=False, forced_text=FORCED_FINAL):
        feats = "\n".join(f"- {k} = {inp.features.get(k, 0.0):g}: {doc}" for k, doc in FEATURE_DOCS.items())
        rows = "\n".join(f"- {s['test']} | {_fmt(s['history_score'])} | {_fmt(s['tfidf_relevance'])} | "
                         f"{_fmt(s['llm_relevance'])} | {s['duration']:g}" for s in inp.shortlist) or "(none)"
        files = "\n".join(f"- {f}" for f in inp.changed_files) or "(none)"
        tools = "\n".join(f"- {s['name']}: {s['description']} Input: {json.dumps(s['input'])}. "
                          f"Output: {json.dumps(s['output'])}." for s in specs) or "(none)"
        obs = "\n".join(observations) or "(none yet)"
        return PROMPT_TEMPLATE.format(
            relevance_source=inp.relevance_source, features=feats, n_files=len(inp.changed_files),
            files=files, shortlist=rows, max_tools=self.max_tool_calls,
            tools_left=0 if forced else max(self.max_tool_calls - tools_used, 0), tools=tools, observations=obs,
            forced=forced_text if forced else "")

    def _observation(self, n, rec):
        if rec.ok:
            body = json.dumps(rec.output, ensure_ascii=False)
        else:
            body = json.dumps({"error": rec.error}, ensure_ascii=False)
        body = anonymise(body)   # diff text and anything else from the repository
        if len(body) > self.observation_max_chars:
            body = body[:self.observation_max_chars] + " ...[truncated]"
        return f"Observation {n}: {rec.tool}({json.dumps(rec.args, ensure_ascii=False)}) -> {body}"

    def decide(self, inp, tools, run_id):
        bid = inp.build_id
        specs = tools.specs()
        observations, tool_calls = [], []
        llm_calls = 0
        while True:
            remaining = self.max_llm_calls - llm_calls
            tool_limit = len(tool_calls) >= self.max_tool_calls
            forced = tool_limit or remaining <= 2
            prompt = self.build_prompt(inp, specs, observations, len(tool_calls), forced,
                                       FORCED_FINAL if tool_limit else FORCED_FINAL_CALLS)
            traced = _TracedProvider(self, bid, llm_calls + 1)
            step, reason, detail, attempts = complete_and_parse(
                traced, prompt, lambda text, f=forced: parse_step(text, final_only=f),
                max_retries=max(min(self.max_retries, remaining - 1), 0))
            llm_calls += attempts
            if reason:
                return self._fallback(bid, reason, detail, llm_calls, tool_calls)
            if step["action"] == "call_tool":
                rec = tools.call(step["tool"], step["args"])
                tool_calls.append(rec)
                self.trace.event(bid, "orchestrator", "tool_call",
                                 {"tool": rec.tool, "args": rec.args, "output": rec.output,
                                  "ok": rec.ok, "error": rec.error}, latency_s=rec.latency_s)
                observations.append(self._observation(len(tool_calls), rec))
                continue
            if step["confidence"] < self.min_confidence:
                return self._fallback(bid, "low_confidence",
                                      f"confidence {step['confidence']} < {self.min_confidence}",
                                      llm_calls, tool_calls, confidence=step["confidence"])
            return self._finish(OrchestratorDecision(
                build_id=bid, w=float(step["w"]), confidence=float(step["confidence"]), source="agent",
                reason=step["reason"], steps=llm_calls, tool_calls=tool_calls, llm_calls=llm_calls,
                prompt_version=self.prompt_version))

    def _fallback(self, bid, reason, detail, llm_calls, tool_calls, confidence=None):
        rec = FallbackRecord(build_id=bid, reason=reason, detail=(detail or "")[:300])
        self.trace.event(bid, "orchestrator", "fallback", rec.to_dict())
        return self._finish(OrchestratorDecision(
            build_id=bid, w=self.fallback_w, confidence=confidence, source="fallback",
            reason=f"fallback to w = {self.fallback_w:.4g} (DANTE): {reason}", steps=llm_calls,
            tool_calls=tool_calls, llm_calls=llm_calls, fallback=rec, prompt_version=self.prompt_version))

    def _finish(self, decision):
        validate(decision.to_dict(), "orchestrator_decision")
        self.trace.event(decision.build_id, "orchestrator", "decision",
                         {"w": decision.w, "confidence": decision.confidence, "source": decision.source,
                          "reason": decision.reason, "tool_calls": len(decision.tool_calls)})
        return decision
