"""Semantic analyzer: asks an LLM how relevant a test class is to a code change.

Input: anonymised, truncated diff chunk + truncated test-class source.
Output: RelevanceResponse validated against the relevance_response schema.
Provider errors (LLMTimeout, LLMError) propagate; malformed output raises
InvalidJSONError or SchemaViolationError. The fallback router decides what to do.
"""
import json
import re

import jsonschema

from src.contracts import RelevanceRequest, RelevanceResponse, validate
from src.obs.trace import NullTrace

PROMPT_VERSION = "v1"          # Phase 1 prompt; the default
PROMPT_VERSION_V2 = "v2"       # calibrated scale with anchors (P2-07)

PROMPT_TEMPLATE = """You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
{diff}
DIFF>>>

Test class `{test}` (source, may be truncated):
<<<TEST
{source}
TEST>>>

Answer with a single JSON object and nothing else:
{{"test": "{test}", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value."""

PROMPT_TEMPLATE_V2 = """You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
{diff}
DIFF>>>

Test class `{test}` (source, may be truncated):
<<<TEST
{source}
TEST>>>

Before deciding, compare the test with the change:
- the test's package name with the package folders of the changed file paths;
- the test's imports with the changed classes and packages;
- the class, method and field names the test uses with the identifiers in the changed lines.

Use this scale for relevance (values between the anchors are allowed):
- 0.0 = the test is in an unrelated module;
- 0.3 = same subsystem, but different functionality;
- 0.6 = the test uses a class or package that the change touches;
- 0.9 = the test directly tests a changed class or method.

Answer with a single JSON object and nothing else:
{{"test": "{test}", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}}
confidence: how sure you are of the relevance value."""

TEMPLATES = {PROMPT_VERSION: PROMPT_TEMPLATE, PROMPT_VERSION_V2: PROMPT_TEMPLATE_V2}

TRUNCATION_MARK = "\n[...truncated]"

_DROP_LINE = re.compile(
    r"^(index [0-9a-f]+\.\.[0-9a-f]+.*|(From|Author|Date|Commit|commit|Signed-off-by|"
    r"Co-authored-by|Reviewed-by)[: ].*|\s*\*?\s*@author\b.*)$",
    re.IGNORECASE)
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_HASH = re.compile(r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b")
_TIMESTAMP = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?\b")


class AnalyzerError(Exception):
    pass


class InvalidJSONError(AnalyzerError):
    pass


class SchemaViolationError(AnalyzerError):
    pass


def anonymise(text):
    """Remove commit hashes, git index lines, author/e-mail/date lines and timestamps."""
    kept = [ln for ln in text.splitlines() if not _DROP_LINE.match(ln)]
    out = "\n".join(kept)
    out = _EMAIL.sub("<email>", out)
    out = _HASH.sub("<hash>", out)
    return _TIMESTAMP.sub("<date>", out)


def truncate(text, max_chars):
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + TRUNCATION_MARK


def prompt_version_from_config(cfg):
    """cfg["llm_p2"]["relevance_prompt_version"], default "v1"; an unknown version is an error."""
    version = (cfg.get("llm_p2") or {}).get("relevance_prompt_version") or PROMPT_VERSION
    if version not in TEMPLATES:
        raise ValueError(f"unknown relevance prompt version {version!r}; valid: {', '.join(TEMPLATES)}")
    return version


def make_request(build_id, test, diff_text, test_source, max_diff_chars, max_test_chars,
                 prompt_version=PROMPT_VERSION):
    """Anonymised, truncated request; prompt_version selects the template and is recorded."""
    if prompt_version not in TEMPLATES:
        raise ValueError(f"unknown relevance prompt version {prompt_version!r}; valid: {', '.join(TEMPLATES)}")
    return RelevanceRequest(
        build_id=build_id,
        test=test,
        diff_chunk=truncate(anonymise(diff_text), max_diff_chars),
        test_source=truncate(anonymise(test_source), max_test_chars),
        prompt_version=prompt_version,
    )


def build_prompt(request, prompt_version=None):
    """The prompt of the request's version (or of prompt_version, if given)."""
    template = TEMPLATES[prompt_version or request.prompt_version or PROMPT_VERSION]
    return template.format(diff=request.diff_chunk, test=request.test, source=request.test_source)


def parse_response(text, expected_test):
    """Parse and validate model output; normalise `test` to the expected name."""
    s = text.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", s, re.DOTALL)
    if fence:
        s = fence.group(1)
    try:
        obj = json.loads(s)
    except (json.JSONDecodeError, TypeError) as e:
        raise InvalidJSONError(f"not JSON: {text[:200]!r}") from e
    if not isinstance(obj, dict):
        raise InvalidJSONError(f"JSON is not an object: {text[:200]!r}")
    try:
        validate(obj, "relevance_response")
    except jsonschema.ValidationError as e:
        raise SchemaViolationError(e.message) from e
    got = obj["test"]
    if got != expected_test and not expected_test.endswith("." + got):
        raise SchemaViolationError(f"response names test {got!r}, expected {expected_test!r}")
    obj["test"] = expected_test
    return RelevanceResponse.from_dict(obj)


class SemanticAnalyzer:
    def __init__(self, provider, trace=None, run_id=None):
        """trace: optional TraceLogger (src.obs.trace); without one nothing is logged.
        run_id: the run the analyzer works for (the logger writes under its own run id)."""
        self.provider = provider
        self.trace = trace or NullTrace()
        self.run_id = run_id

    def analyze(self, request):
        prompt = build_prompt(request)
        try:
            text = self.provider.complete(prompt, json_mode=True)
        except Exception as e:
            self._trace_call(request, prompt, None, error=type(e).__name__)
            raise
        self._trace_call(request, prompt, text)
        return parse_response(text, request.test)

    def _trace_call(self, request, prompt, response, attempt=0, error=None):
        """One llm_call trace event (payload keys from the table in src/obs/trace.py)."""
        rec = self.provider.calls[-1] if getattr(self.provider, "calls", None) else None
        payload = {"test": request.test, "prompt": prompt, "response": response, "attempt": attempt,
                   "cached": bool(getattr(rec, "cached", False)),
                   "prompt_tokens": getattr(rec, "prompt_tokens", None),
                   "completion_tokens": getattr(rec, "completion_tokens", None)}
        if error:
            payload["error"] = error
        self.trace.event(request.build_id, "semantic_analyzer", "llm_call", payload,
                         latency_s=getattr(rec, "latency_s", None))

    def analyze_with_retry(self, request, max_retries=1):
        """Like analyze, but retries a failed call; returns
        (RelevanceResponse or None, fallback reason, detail, attempts).
        Each attempt writes its own llm_call trace event with its attempt number."""
        from src.agent.retry import complete_and_parse
        return complete_and_parse(_TracedProvider(self, request), build_prompt(request),
                                  lambda text: parse_response(text, request.test), max_retries)


class _TracedProvider:
    """Passes calls on to the analyzer's provider and writes one llm_call event per attempt."""

    def __init__(self, analyzer, request):
        from src.agent.retry import _accepts_attempt
        self.analyzer = analyzer
        self.request = request
        self.inner_takes_attempt = _accepts_attempt(analyzer.provider)

    def complete(self, prompt, json_mode=None, attempt=0):
        inner = self.analyzer.provider
        try:
            if self.inner_takes_attempt:
                text = inner.complete(prompt, json_mode, attempt=attempt)
            else:
                text = inner.complete(prompt, json_mode)
        except Exception as e:
            self.analyzer._trace_call(self.request, prompt, None, attempt=attempt, error=type(e).__name__)
            raise
        self.analyzer._trace_call(self.request, prompt, text, attempt=attempt)
        return text
