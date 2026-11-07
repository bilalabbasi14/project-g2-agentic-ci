"""Single-call LLM baseline (non-agentic): one LLM call rates every candidate test.

docs/PROJECT_CONTEXT.md §5.2 (`Single-call LLM`, relevance source
`llm_single_call`) and §8 (E1). This is the "single non-agentic LLM call" that
hypothesis H-B compares the agent with: no tools, no shortlist, no loop. The
model gets the anonymised diff and the numbered list of candidate test classes
and must return one relevance per listed test. The answer is validated against
`single_call_response` and retried once (src.agent.retry); after a second
failure the scorer returns no relevance and one FallbackRecord, and the
pipeline uses the DANTE ranking for this method.

At most `single_call.max_tests` candidates are listed: the first ones of the
DANTE-CCH value order the pipeline passes in; the others get relevance 0.
Target-build outcomes are never read.
"""
import inspect
import json
import re

import jsonschema

from src.agent.retry import complete_and_parse
from src.agent.semantic_analyzer import InvalidJSONError, SchemaViolationError, anonymise, truncate
from src.contracts import FallbackRecord, validate
from src.obs.trace import NullTrace

SINGLE_CALL_PROMPT_VERSION = "sc1"

# more than this share of the listed tests missing from the answer -> schema_violation
MAX_MISSING_SHARE = 0.5

PROMPT_TEMPLATE = """You help decide which regression tests to run for a code change.
Below is the code change and a numbered list of {n} test classes. For EVERY listed test
class, rate how likely it is to exercise the changed code, so that it could fail because
of this change, as a number from 0 to 1. Use these anchors:
- 0.0: the test is in an unrelated module;
- 0.3: the test is in the same subsystem as the change;
- 0.6: the test uses a touched class or package;
- 0.9: the test directly tests the changed code.

Code change (unified diff, may be truncated):
<<<DIFF
{diff}
DIFF>>>

Test classes:
{tests}

Answer with a single JSON object and nothing else, of this shape:
{{"scores": [{{"test": "<fully qualified test class name>", "relevance": <number from 0 to 1>}}, ...]}}
The list "scores" must contain every one of the {n} listed test classes exactly once,
with the name exactly as listed, and no other test classes."""


def build_prompt(diff_text, tests, max_diff_chars):
    """Prompt for one build: anonymised, truncated diff and the numbered test list."""
    listing = "\n".join(f"{i}. {t}" for i, t in enumerate(tests, 1))
    return PROMPT_TEMPLATE.format(n=len(tests), diff=truncate(anonymise(diff_text or ""), max_diff_chars),
                                  tests=listing)


def match_name(name, listed, listed_set):
    """The listed test a reply name refers to: an exact match, or the unique listed
    test ending in "." + name. None if unknown or ambiguous."""
    if name in listed_set:
        return name
    hits = [t for t in listed if t.endswith("." + name)]
    return hits[0] if len(hits) == 1 else None


def _load(text):
    """json.loads + validate(single_call_response); raises InvalidJSONError / SchemaViolationError."""
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
        validate(obj, "single_call_response")
    except jsonschema.ValidationError as e:
        raise SchemaViolationError(e.message) from e
    return obj


def _match(obj, listed):
    """(relevance per matched listed test, n_missing, n_unknown) for a validated answer.
    Unknown or ambiguous names are ignored and counted; a later duplicate of an
    already matched test is ignored."""
    listed_set = set(listed)
    found, n_unknown = {}, 0
    for item in obj["scores"]:
        test = match_name(item["test"], listed, listed_set)
        if test is None:
            n_unknown += 1
        elif test not in found:
            found[test] = float(item["relevance"])
    return found, len(listed) - len(found), n_unknown


def parse_scores(text, listed):
    """Parse and validate one answer: (relevance found, n_missing, n_unknown).
    More than half of the listed tests missing counts as a schema violation."""
    found, n_missing, n_unknown = _match(_load(text), listed)
    if listed and n_missing > MAX_MISSING_SHARE * len(listed):
        raise SchemaViolationError(f"{n_missing} of {len(listed)} listed tests missing from the answer")
    return found, n_missing, n_unknown


def _counts(text, listed):
    """n_missing / n_unknown of an answer for the trace; empty if the answer is not
    valid JSON of the right shape (counted even when too many tests are missing)."""
    try:
        _found, n_missing, n_unknown = _match(_load(text), listed)
    except (InvalidJSONError, SchemaViolationError):
        return {}
    return {"n_missing": n_missing, "n_unknown": n_unknown}


def _accepts(fn, name):
    params = inspect.signature(fn).parameters.values()
    return any(p.name == name or p.kind is p.VAR_KEYWORD for p in params)


class SingleCallScorer:
    """Implements SingleCallScorerLike.score (src/contracts/interfaces.py)."""

    def __init__(self, provider, cfg, trace=None):
        sc = cfg["single_call"]
        self.provider = provider
        self.max_tests = int(sc["max_tests"])
        self.max_diff_chars = int(sc["max_diff_chars"])
        self.num_ctx = int(sc["num_ctx"])
        self.max_retries = int((cfg.get("llm_p2") or {}).get("max_retries", 1))
        self.trace = trace or NullTrace()
        self.prompt_version = SINGLE_CALL_PROMPT_VERSION

    def score(self, build_id, diff_text, candidates, run_id):
        """(relevance for every candidate, fallbacks, LLM calls). Unlisted (truncated)
        and missing tests get 0; on fallback the relevance dict is empty."""
        candidates = list(candidates)
        listed = candidates[:self.max_tests]
        truncated_from = len(candidates) if len(candidates) > len(listed) else None
        prompt = build_prompt(diff_text, listed, self.max_diff_chars)
        caller = _TracedCall(self, build_id, listed, truncated_from)
        found, reason, detail, attempts = complete_and_parse(
            caller, prompt, lambda text: parse_scores(text, listed)[0], self.max_retries)
        if reason:
            rec = FallbackRecord(build_id=build_id, reason=reason, detail=(detail or "")[:300])
            self.trace.event(build_id, "single_call", "fallback", rec.to_dict())
            return {}, [rec], attempts
        return {t: float(found.get(t, 0.0)) for t in candidates}, [], attempts


class _TracedCall:
    """Calls the scorer's provider with this call's num_ctx and writes one
    single_call llm_call trace event per attempt (P2-05 table)."""

    def __init__(self, scorer, build_id, listed, truncated_from):
        self.s, self.build_id, self.listed, self.truncated_from = scorer, build_id, listed, truncated_from
        complete = scorer.provider.complete
        self.pass_options = _accepts(complete, "options")
        self.pass_attempt = _accepts(complete, "attempt")

    def complete(self, prompt, json_mode=None, attempt=0):
        kwargs = {}
        if self.pass_options:
            kwargs["options"] = {"num_ctx": self.s.num_ctx}
        if self.pass_attempt:
            kwargs["attempt"] = attempt
        try:
            text = self.s.provider.complete(prompt, json_mode, **kwargs)
        except Exception as e:
            self._event(prompt, None, attempt, type(e).__name__)
            raise
        self._event(prompt, text, attempt)
        return text

    def _event(self, prompt, response, attempt, error=None):
        calls = getattr(self.s.provider, "calls", None)
        rec = calls[-1] if calls else None
        payload = {"n_tests": len(self.listed), "prompt": prompt, "response": response,
                   "cached": bool(getattr(rec, "cached", False)), "attempt": attempt}
        if response is not None:
            payload.update(_counts(response, self.listed))
        if self.truncated_from is not None:
            payload["truncated_from"] = self.truncated_from
        if error:
            payload["error"] = error
        self.s.trace.event(self.build_id, "single_call", "llm_call", payload,
                           latency_s=getattr(rec, "latency_s", None))


def make_single_call_provider(cfg, base_url=None, seed=None):
    """Provider for the single call with context window single_call.num_ctx.

    src.agent.llm_provider.make_provider uses llm_p2.num_ctx for every component,
    and a CachingProvider sends the options it was built with, so the single
    call's larger context must be set when the provider is built."""
    from src.agent.llm_cache import CachingProvider, LLMCache
    from src.agent.llm_provider import OllamaProvider
    from src.settings import repo_path
    llm_p2 = cfg.get("llm_p2") or {}
    seed = llm_p2.get("seed") if seed is None else seed
    inner = OllamaProvider.from_config(cfg, base_url=base_url, seed=seed, component="single_call")
    inner.num_ctx = int(cfg["single_call"]["num_ctx"])
    if not llm_p2.get("cache"):
        return inner
    options = {"temperature": inner.temperature, "seed": seed, "num_ctx": inner.num_ctx}
    return CachingProvider(inner, LLMCache(repo_path(llm_p2["cache_dir"])), options, "single_call")
