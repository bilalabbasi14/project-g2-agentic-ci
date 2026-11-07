import copy
import inspect
import json

from src.agent.llm_cache import CachingProvider
from src.agent.llm_provider import LLMTimeout, MockProvider, OllamaProvider
from src.agent.single_call import (SINGLE_CALL_PROMPT_VERSION, SingleCallScorer, build_prompt,
                                   make_single_call_provider)
from src.contracts import validate
from src.contracts.interfaces import SingleCallScorerLike
from src.settings import load_config

CFG = load_config()
SECRET_HASH = "deadbeefcafe1234"
DIFF = (f"commit {SECRET_HASH}\nAuthor: Dev <dev@example.com>\nindex {SECRET_HASH}..abc1234\n"
        "--- a/core/Cache.java\n+++ b/core/Cache.java\n+    evict();")
TESTS = ["org.x.CacheTest", "org.x.WebTest", "org.y.SlowTest", "org.y.NoSourceTest", "org.z.OtherTest"]


def _answer(pairs):
    return json.dumps({"scores": [{"test": t, "relevance": r} for t, r in pairs]})


class _Trace:
    def __init__(self):
        self.events = []

    def event(self, build_id, component, event, payload, latency_s=None):
        self.events.append((component, event, payload))


class _OptionsProvider(MockProvider):
    """MockProvider that also records the per-call options and attempts."""

    def __init__(self, answers):
        super().__init__(answers)
        self.options, self.attempts = [], []

    def complete(self, prompt, json_mode=False, options=None, attempt=0):
        self.options.append(options)
        self.attempts.append(attempt)
        return super().complete(prompt, json_mode)


def test_satisfies_interface_and_version():
    assert inspect.signature(SingleCallScorer.score).parameters.keys() == \
        inspect.signature(SingleCallScorerLike.score).parameters.keys()
    assert SingleCallScorer(MockProvider(["{}"]), CFG).prompt_version == SINGLE_CALL_PROMPT_VERSION == "sc1"


def test_complete_valid_answer():
    provider = _OptionsProvider([_answer([(t, 0.1 * i) for i, t in enumerate(TESTS)])])
    rel, fallbacks, calls = SingleCallScorer(provider, CFG).score("b1", DIFF, TESTS, "run")
    assert calls == 1 and fallbacks == []
    assert rel == {t: 0.1 * i for i, t in enumerate(TESTS)}
    assert provider.options == [{"num_ctx": CFG["single_call"]["num_ctx"]}]
    validate({"scores": [{"test": t, "relevance": v} for t, v in rel.items()]}, "single_call_response")


def test_suffix_match_and_ambiguous_suffix():
    tests = ["org.a.FooTest", "org.b.FooTest", "org.c.BarTest"]
    trace = _Trace()
    # "BarTest" matches org.c.BarTest uniquely; "FooTest" is ambiguous -> unknown, both FooTests missing
    provider = MockProvider([_answer([("BarTest", 0.8), ("FooTest", 0.9)])])
    rel, fallbacks, _ = SingleCallScorer(provider, CFG, trace).score("b1", DIFF, tests, "run")
    # 2 of 3 missing is more than 50% -> schema violation, retried, then fallback
    assert rel == {} and fallbacks[0].reason == "schema_violation"
    assert trace.events[0][2]["n_missing"] == 2 and trace.events[0][2]["n_unknown"] == 1
    # with the FooTests named in full, the suffix BarTest still maps to org.c.BarTest
    provider = MockProvider([_answer([("BarTest", 0.8), ("org.a.FooTest", 0.4), ("org.b.FooTest", 0.2)])])
    rel, fallbacks, _ = SingleCallScorer(provider, CFG).score("b1", DIFF, tests, "run")
    assert rel == {"org.a.FooTest": 0.4, "org.b.FooTest": 0.2, "org.c.BarTest": 0.8} and fallbacks == []


def test_missing_get_zero_and_unknown_are_ignored_and_counted():
    trace = _Trace()
    pairs = [(TESTS[0], 0.9), (TESTS[1], 0.6), (TESTS[2], 0.3), ("org.q.NotListedTest", 1.0)]
    rel, fallbacks, calls = SingleCallScorer(MockProvider([_answer(pairs)]), CFG, trace).score(
        "b1", DIFF, TESTS, "run")
    assert fallbacks == [] and calls == 1
    assert rel == {TESTS[0]: 0.9, TESTS[1]: 0.6, TESTS[2]: 0.3, TESTS[3]: 0.0, TESTS[4]: 0.0}
    assert "org.q.NotListedTest" not in rel
    (component, event, payload), = trace.events
    assert (component, event) == ("single_call", "llm_call")
    assert payload["n_tests"] == 5 and payload["n_missing"] == 2 and payload["n_unknown"] == 1
    assert {"prompt", "response", "cached"} <= set(payload)


def test_sixty_percent_missing_retried_then_fallback():
    trace = _Trace()
    provider = MockProvider([_answer([(TESTS[0], 0.9), (TESTS[1], 0.5)])])     # 3 of 5 missing = 60%
    rel, fallbacks, calls = SingleCallScorer(provider, CFG, trace).score("b1", DIFF, TESTS, "run")
    assert rel == {} and calls == 2 and len(provider.prompts) == 2
    assert len(fallbacks) == 1
    fb = fallbacks[0]
    assert fb.reason == "schema_violation" and fb.build_id == "b1" and fb.test is None
    validate(fb.to_dict(), "fallback_record")
    assert [e[1] for e in trace.events] == ["llm_call", "llm_call", "fallback"]
    assert [e[2]["attempt"] for e in trace.events[:2]] == [0, 1]


def test_invalid_then_valid_is_used():
    provider = _OptionsProvider(["not json", _answer([(t, 0.5) for t in TESTS])])
    rel, fallbacks, calls = SingleCallScorer(provider, CFG).score("b1", DIFF, TESTS, "run")
    assert calls == 2 and fallbacks == [] and set(rel.values()) == {0.5}
    assert provider.attempts == [0, 1]


def test_timeout_twice_falls_back_with_error_in_trace():
    trace = _Trace()
    rel, fallbacks, calls = SingleCallScorer(MockProvider([LLMTimeout("slow")]), CFG, trace).score(
        "b1", DIFF, TESTS, "run")
    assert rel == {} and calls == 2 and fallbacks[0].reason == "timeout"
    assert trace.events[0][2]["response"] is None and trace.events[0][2]["error"] == "LLMTimeout"


def test_more_than_max_tests_only_first_listed_in_order():
    cfg = copy.deepcopy(CFG)
    cfg["single_call"]["max_tests"] = 3
    trace = _Trace()
    provider = MockProvider([_answer([(t, 0.7) for t in TESTS[:3]])])
    rel, fallbacks, _ = SingleCallScorer(provider, cfg, trace).score("b1", DIFF, TESTS, "run")
    prompt = provider.prompts[0]
    listing = prompt.split("Test classes:\n")[1].split("\n\n")[0].splitlines()
    assert listing == [f"{i}. {t}" for i, t in enumerate(TESTS[:3], 1)]
    assert TESTS[3] not in prompt and TESTS[4] not in prompt
    assert rel == {TESTS[0]: 0.7, TESTS[1]: 0.7, TESTS[2]: 0.7, TESTS[3]: 0.0, TESTS[4]: 0.0}
    assert trace.events[0][2]["truncated_from"] == 5 and trace.events[0][2]["n_tests"] == 3


def test_prompt_contains_anonymised_diff():
    prompt = build_prompt(DIFF, TESTS, CFG["single_call"]["max_diff_chars"])
    assert "evict();" in prompt and "core/Cache.java" in prompt
    assert SECRET_HASH not in prompt and "dev@example.com" not in prompt
    for anchor in ("0.0", "0.3", "0.6", "0.9"):
        assert anchor in prompt


def test_prompt_truncates_diff():
    prompt = build_prompt("+x\n" * 5000, TESTS, 100)
    assert "[...truncated]" in prompt and prompt.count("+x") <= 50


def test_make_single_call_provider_uses_single_call_num_ctx(tmp_path):
    cfg = copy.deepcopy(CFG)
    cfg["llm_p2"]["cache"] = False
    p = make_single_call_provider(cfg)
    assert isinstance(p, OllamaProvider) and p.num_ctx == cfg["single_call"]["num_ctx"]
    assert p.request_options()["num_ctx"] == cfg["single_call"]["num_ctx"] and p.component == "single_call"
    cfg["llm_p2"]["cache"] = True
    cfg["llm_p2"]["cache_dir"] = str(tmp_path / "cache")
    p = make_single_call_provider(cfg, seed=2)
    assert isinstance(p, CachingProvider)
    assert p.options == {"temperature": 0.0, "seed": 2, "num_ctx": cfg["single_call"]["num_ctx"]}
