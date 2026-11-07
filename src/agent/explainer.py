"""Explainer (Gap 2): short, evidence-based justifications for important skipped tests.

docs/PROJECT_CONTEXT.md §5.2 (`Full system`), §5.3 step 7, §5.4 and §8 (RQ2 and
the rating rule). The explainer runs after selection and never changes it. For
one build and budget it picks up to `top_n_skipped` skipped tests that ranked
highly by history or relevance, gathers the evidence for each (history
statistics, scores, the analyzer's reason, changed files, why the budget
excluded the test), and asks the LLM for a justification that uses only that
evidence and lists the facts it relied on. Every answer is validated against
`explanation_response` and retried once (src.agent.retry); a call that still
fails gives an ExplanationRecord with ok=False.

The target build's outcomes (`actual_outcome`) are never read.
"""
import json
import re

import jsonschema

from src.agent.retry import complete_and_parse
from src.agent.semantic_analyzer import InvalidJSONError, SchemaViolationError, anonymise
from src.contracts import ExplanationRecord, validate
from src.obs.trace import NullTrace

EXPLAINER_PROMPT_VERSION = "e1"

SKIP_CAUSE = "did_not_fit"

PROMPT_TEMPLATE = """You help developers understand a test selection made by a CI system.
The CI system had a time budget for this build and could not run every test class.
It ranked the test classes by a value score and ran them in that order while they fitted
into the budget. The test class below was SKIPPED: it was not run in this build.

Write at most 2 sentences (at most {max_chars} characters) explaining why skipping this
test was reasonable or risky. Use ONLY the facts in the evidence JSON below. Do not guess,
do not add any other knowledge about the project, and do not mention facts that are not
in the evidence.

In "cited_facts", list the exact facts you used (1 to 6 short phrases copied from the
evidence, for example "failures: 0 of 100 runs" or "duration_s: 42.5").

Answer with a single JSON object and nothing else:
{{"test": "<the test name>", "justification": "<at most 2 sentences>", "cited_facts": ["<fact>", "..."]}}

Example.
Evidence:
{{"test": "org.example.CacheTest", "rank_by_value": 12, "n_candidates": 80, "n_selected": 9,
 "history": {{"test": "org.example.CacheTest", "history_builds": 100, "runs": 100, "failures": 0,
 "failure_rate": 0.0, "last_failure_distance": null, "recent_outcomes": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}},
 "history_score": 0.0, "relevance_used": 0.62, "relevance_reason": "The test uses the changed cache class.",
 "changed_files": ["core/src/main/java/org/example/Cache.java"], "duration_s": 310.0, "budget_s": 400.0,
 "remaining_budget_at_turn_s": 120.5, "skip_cause": "did_not_fit", "fits_if_budget_s": 589.5}}
Answer:
{{"test": "org.example.CacheTest", "justification": "Skipping it is risky: its relevance is 0.62 because it uses the changed Cache.java, although it never failed in 100 runs. It needs 310.0 s but only 120.5 s of the budget was left when it was reached.", "cited_facts": ["relevance_used: 0.62", "changed_files: core/src/main/java/org/example/Cache.java", "failures: 0 of 100 runs", "duration_s: 310.0", "remaining_budget_at_turn_s: 120.5"]}}

Now the real case.
Evidence:
{evidence}
Answer:"""

# file names in a cited fact: anything with a path separator or a source/config extension
_FILE = re.compile(r"[\w.$-]*[/\\][\w./\\$-]*\w|[\w.$-]+\.(?:java|kt|kts|groovy|scala|xml|properties|"
                   r"py|js|ts|go|rb|cs|c|h|cpp|json|yaml|yml|cfg|txt)\b")
_NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])")


def _top(df, column, n):
    """The n tests with the highest `column`, ties broken by test name."""
    rows = sorted(((-float(df.at[t, column]), str(t)) for t in df.index))
    return {t for _, t in rows[:n]}


def select_skipped(df, selected, ordered, pool=20, top_n=5):
    """Important skipped tests as (test, rank by value), at most top_n, in ranking order.

    A test qualifies if it is in `ordered` but not in `selected`, and is among the
    top `pool` candidates of `df` by history_score or by relevance_used. Rank 1 is
    the first test of `ordered`. Never reads actual_outcome."""
    chosen = set(selected)
    important = _top(df, "history_score", pool) | _top(df, "relevance_used", pool)
    out = [(t, i) for i, t in enumerate(ordered, 1) if t not in chosen and t in important]
    return out[:top_n]


def _greedy_turn(test, ordered, durations, budget_seconds):
    """Budget time already used when the greedy scan reaches `test` (same rule as
    src.dante.selection: take a test while used + duration <= budget)."""
    used = 0.0
    for t in ordered:
        if t == test:
            return used
        d = float(durations.get(t, 0.0))
        if used + d <= budget_seconds:
            used += d
    raise ValueError(f"{test!r} is not in the ranking")


def build_evidence(test, rank, df, ordered, durations, selected, budget_seconds, diff_files, llm_reasons,
                   history_tool, max_changed_files):
    """The facts the LLM may use for one skipped test (keys fixed by P2-10).

    Text that comes from the repository (changed file paths, the analyzer's
    reason) is passed through anonymise, so the evidence stored with the record
    is exactly what the model saw."""
    used = _greedy_turn(test, ordered, durations, budget_seconds)
    duration = float(durations.get(test, df.at[test, "duration"] if "duration" in df.columns else 0.0))
    reason = llm_reasons.get(test)
    return {
        "test": test,
        "rank_by_value": int(rank),
        "n_candidates": len(ordered),
        "n_selected": len(selected),
        "history": history_tool(test),
        "history_score": round(float(df.at[test, "history_score"]), 3),
        "relevance_used": round(float(df.at[test, "relevance_used"]), 3),
        "relevance_reason": anonymise(reason) if reason else None,
        "changed_files": [anonymise(p) for p in sorted(diff_files)[:max_changed_files]],
        "duration_s": round(duration, 3),
        "budget_s": round(float(budget_seconds), 3),
        "remaining_budget_at_turn_s": round(float(budget_seconds) - used, 3),
        "skip_cause": SKIP_CAUSE,
        "fits_if_budget_s": round(used + duration, 3),
    }


def build_prompt(evidence, max_chars):
    return PROMPT_TEMPLATE.format(evidence=json.dumps(evidence, ensure_ascii=False), max_chars=max_chars)


def parse_explanation(text, expected_test, max_chars):
    """Parse and validate one answer; `test` must name the requested test (a suffix
    such as `FooTest` for `org.x.FooTest` is accepted and normalised)."""
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
        validate(obj, "explanation_response")
    except jsonschema.ValidationError as e:
        raise SchemaViolationError(e.message) from e
    if len(obj["justification"]) > max_chars:
        raise SchemaViolationError(f"justification has {len(obj['justification'])} characters (max {max_chars})")
    got = obj["test"]
    if got != expected_test and not expected_test.endswith("." + got):
        raise SchemaViolationError(f"response names test {got!r}, expected {expected_test!r}")
    obj["test"] = expected_test
    return obj


def _sum_or_none(values):
    values = [v for v in values if v is not None]
    return sum(values) if values else None


class LLMExplainer:
    """Implements ExplainerLike.explain (src/contracts/interfaces.py)."""

    def __init__(self, provider, cfg, trace=None):
        e = cfg["explainer"]
        self.provider = provider
        self.top_n = int(e["top_n_skipped"])
        self.pool = int(e["candidate_pool"])
        self.max_chars = int(e["max_justification_chars"])
        self.max_changed_files = int(e["max_changed_files"])
        self.max_retries = int((cfg.get("llm_p2") or {}).get("max_retries", 1))
        self.trace = trace or NullTrace()
        self.prompt_version = EXPLAINER_PROMPT_VERSION

    def explain(self, build_id, budget_fraction, df, selected, ordered, durations, budget_seconds, diff_files,
                llm_reasons, history_tool, run_id):
        records = []
        for test, rank in select_skipped(df, selected, ordered, self.pool, self.top_n):
            evidence = build_evidence(test, rank, df, ordered, durations, selected, budget_seconds, diff_files,
                                      llm_reasons, history_tool, self.max_changed_files)
            records.append(self._explain_one(build_id, budget_fraction, test, rank, evidence))
        return records

    def _explain_one(self, build_id, budget_fraction, test, rank, evidence):
        calls = getattr(self.provider, "calls", None)
        n0 = len(calls) if calls is not None else 0
        answer, reason, _detail, _attempts = complete_and_parse(
            self.provider, build_prompt(evidence, self.max_chars),
            lambda text: parse_explanation(text, test, self.max_chars), self.max_retries)
        used = list(calls[n0:]) if calls is not None else []
        rec = ExplanationRecord(
            build_id=build_id, budget_fraction=float(budget_fraction), test=test, rank_by_value=int(rank),
            evidence=evidence,
            justification=answer["justification"] if answer else None,
            cited_facts=list(answer["cited_facts"]) if answer else [],
            ok=answer is not None, error=None if answer else reason,
            latency_s=float(sum(c.latency_s for c in used)),
            prompt_tokens=_sum_or_none(c.prompt_tokens for c in used),
            completion_tokens=_sum_or_none(c.completion_tokens for c in used),
            prompt_version=self.prompt_version)
        validate(rec.to_dict(), "explanation_record")
        self.trace.event(build_id, "explainer", "explanation",
                         {"test": test, "budget": rec.budget_fraction, "evidence": evidence,
                          "justification": rec.justification, "cited_facts": rec.cited_facts,
                          "ok": rec.ok, "error": rec.error}, latency_s=rec.latency_s)
        return rec


def _numbers(text):
    return [float(x) for x in _NUMBER.findall(text)]


def grounding_report(record):
    """Cheap automatic check of the cited facts of one explanation.

    A cited fact counts as found when every file name and every number in it
    also appears in the JSON-dumped evidence (numbers are compared as values, so
    "0.30" matches 0.3). It does not replace the human rating (§8)."""
    rec = record.to_dict() if hasattr(record, "to_dict") else dict(record)
    evidence_text = json.dumps(rec.get("evidence") or {}, ensure_ascii=False)
    evidence_numbers = set(_numbers(evidence_text))
    ungrounded = []
    for fact in rec.get("cited_facts") or []:
        files = _FILE.findall(fact)
        rest = _FILE.sub(" ", fact)
        ok = all(f in evidence_text for f in files) and all(n in evidence_numbers for n in _numbers(rest))
        if not ok:
            ungrounded.append(fact)
    cited = list(rec.get("cited_facts") or [])
    return {"n_cited": len(cited), "n_cited_found": len(cited) - len(ungrounded), "ungrounded": ungrounded}
