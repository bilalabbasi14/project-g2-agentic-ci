"""Typed structures passed between pipeline components.

Every structure round-trips through plain JSON (to_dict / from_dict) and is
validated against the JSON Schemas in schemas.py.
"""
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

FALLBACK_REASONS = ("timeout", "invalid_json", "schema_violation", "low_confidence", "provider_error")
RANKING_SOURCES = ("llm", "dante_fallback", "dante", "random", "history_only", "tfidf_only")

# --- Phase 2 enumerations (docs/PROJECT_CONTEXT.md §5.2, §5.3) ---
RELEVANCE_SOURCES = ("none", "tfidf", "llm_shortlist", "llm_all_individual", "llm_single_call")
WEIGHT_MODES = ("random", "history_only", "relevance_only", "fixed", "tuned", "agent")
TRACE_COMPONENTS = ("pipeline", "semantic_analyzer", "fallback_router", "orchestrator",
                    "explainer", "single_call", "tool")
TRACE_EVENTS = ("llm_call", "tool_call", "decision", "fallback", "state", "explanation")
DANTE_W = 2.0 / 3.0   # w that reproduces DANTE's 1.0*H + 0.5*R^1.2 ranking exactly


@dataclass
class ChangedFile:
    path: str
    added_lines: int
    removed_lines: int


@dataclass
class DiffSummary:
    files: List[ChangedFile] = field(default_factory=list)

    @property
    def total_added(self):
        return sum(f.added_lines for f in self.files)

    @property
    def total_removed(self):
        return sum(f.removed_lines for f in self.files)


@dataclass
class CandidateTest:
    name: str                       # fully qualified test class name
    duration: float                 # seconds, from the build's test results
    history_score: float = 0.0
    tfidf_score: float = 0.0
    llm_relevance: Optional[float] = None
    final_score: Optional[float] = None


@dataclass
class BuildState:
    build_id: str                   # e.g. "PR-1840_build4"
    project: str
    budget_fraction: float          # 0.10 = 10% of total suite time
    budget_seconds: float
    diff_summary: DiffSummary
    candidates: List[CandidateTest] = field(default_factory=list)
    selected_tests: List[str] = field(default_factory=list)
    remaining_budget: float = 0.0
    fallbacks: List["FallbackRecord"] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(
            build_id=d["build_id"],
            project=d["project"],
            budget_fraction=d["budget_fraction"],
            budget_seconds=d["budget_seconds"],
            diff_summary=DiffSummary([ChangedFile(**f) for f in d["diff_summary"]["files"]]),
            candidates=[CandidateTest(**c) for c in d.get("candidates", [])],
            selected_tests=list(d.get("selected_tests", [])),
            remaining_budget=d.get("remaining_budget", 0.0),
            fallbacks=[FallbackRecord(**f) for f in d.get("fallbacks", [])],
        )


@dataclass
class RelevanceRequest:
    build_id: str
    test: str
    diff_chunk: str                 # anonymised and truncated
    test_source: str                # truncated
    prompt_version: str = "v1"

    def to_dict(self):
        return asdict(self)


@dataclass
class RelevanceResponse:
    test: str
    relevance: float                # 0..1
    reason: str
    confidence: Optional[float] = None  # 0..1, optional in the model output

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, d):
        return cls(test=d["test"], relevance=float(d["relevance"]), reason=d["reason"],
                   confidence=None if d.get("confidence") is None else float(d["confidence"]))


@dataclass
class LLMCallRecord:
    model: str
    latency_s: float
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    ok: bool = True
    error: Optional[str] = None
    cached: bool = False             # answer read from the LLM cache (latency/tokens are the original ones)
    component: Optional[str] = None  # one of TRACE_COMPONENTS, or None

    def __post_init__(self):
        if self.component is not None and self.component not in TRACE_COMPONENTS:
            raise ValueError(f"unknown component: {self.component}")

    def to_dict(self):
        return asdict(self)


@dataclass
class FallbackRecord:
    build_id: str
    reason: str                     # one of FALLBACK_REASONS
    detail: str = ""
    test: Optional[str] = None      # None when the record concerns the whole build

    def __post_init__(self):
        if self.reason not in FALLBACK_REASONS:
            raise ValueError(f"unknown fallback reason: {self.reason}")

    def to_dict(self):
        return asdict(self)


@dataclass
class FinalRanking:
    build_id: str
    method: str                     # e.g. "DANTE-CCH", "LLM-relevance"
    source: str                     # one of RANKING_SOURCES
    budget_fraction: float
    ordered_tests: List[str]
    selected_tests: List[str]
    total_duration: float
    scores: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if self.source not in RANKING_SOURCES:
            raise ValueError(f"unknown ranking source: {self.source}")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


# ---------------------------------------------------------------- Phase 2 ----

@dataclass
class MethodSpec:
    """One evaluated method: where relevance comes from, how w is chosen, and
    whether the explainer runs (docs/PROJECT_CONTEXT.md §5.2)."""
    name: str
    relevance_source: str           # one of RELEVANCE_SOURCES
    weight_mode: str                # one of WEIGHT_MODES
    w: Optional[float] = None       # history weight for weight_mode "fixed"
    tuned_key: Optional[str] = None  # "tfidf" or "llm" for weight_mode "tuned"
    explainer: bool = False

    def __post_init__(self):
        if self.relevance_source not in RELEVANCE_SOURCES:
            raise ValueError(f"unknown relevance_source: {self.relevance_source}")
        if self.weight_mode not in WEIGHT_MODES:
            raise ValueError(f"unknown weight_mode: {self.weight_mode}")
        if self.weight_mode == "fixed" and (self.w is None or not 0.0 <= self.w <= 1.0):
            raise ValueError(f"weight_mode 'fixed' needs w in [0, 1], got {self.w}")
        if self.weight_mode == "tuned" and self.tuned_key not in ("tfidf", "llm"):
            raise ValueError(f"weight_mode 'tuned' needs tuned_key 'tfidf' or 'llm', got {self.tuned_key}")
        if self.weight_mode == "agent" and self.relevance_source == "none":
            raise ValueError("weight_mode 'agent' needs a relevance source other than 'none'")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class ToolCallRecord:
    """One tool call made by the orchestrator, with its output and cost."""
    tool: str
    args: Dict[str, Any]
    output: Dict[str, Any]
    latency_s: float
    ok: bool = True
    error: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class OrchestratorInput:
    """What the orchestrator sees for one build: features and the shortlist.
    Shortlist items have keys test, history_score, tfidf_relevance,
    llm_relevance (may be None) and duration. Never contains outcomes."""
    build_id: str
    features: Dict[str, float]
    shortlist: List[Dict[str, Any]]
    changed_files: List[str]
    budget_fractions: List[float]
    relevance_source: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class OrchestratorDecision:
    """The weight chosen for one build, by the agent or by fallback (w = DANTE_W)."""
    build_id: str
    w: float
    confidence: Optional[float]
    source: str                     # "agent" or "fallback"
    reason: str
    steps: int                      # LLM calls made while deciding
    tool_calls: List[ToolCallRecord]
    llm_calls: int
    fallback: Optional[FallbackRecord] = None
    prompt_version: str = "o1"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        d = dict(d)
        d["tool_calls"] = [ToolCallRecord.from_dict(t) for t in d.get("tool_calls", [])]
        if d.get("fallback") is not None:
            d["fallback"] = FallbackRecord(**d["fallback"])
        return cls(**d)


@dataclass
class ExplanationRecord:
    """One justification for a skipped test (Gap 2); ok=False when the call failed."""
    build_id: str
    budget_fraction: float
    test: str
    rank_by_value: int
    evidence: Dict[str, Any]
    justification: Optional[str]
    cited_facts: List[str]
    ok: bool
    error: Optional[str]
    latency_s: float
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    prompt_version: str = "e1"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class TraceEvent:
    """One step of an agent trajectory, written as one JSON line by the trace logger."""
    run_id: str
    build_id: str
    component: str                  # one of TRACE_COMPONENTS
    event: str                      # one of TRACE_EVENTS
    step: int
    payload: Dict[str, Any]
    latency_s: Optional[float] = None
    ts: str = ""                    # ISO-8601 UTC, filled by the trace logger

    def __post_init__(self):
        if self.component not in TRACE_COMPONENTS:
            raise ValueError(f"unknown component: {self.component}")
        if self.event not in TRACE_EVENTS:
            raise ValueError(f"unknown event: {self.event}")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
