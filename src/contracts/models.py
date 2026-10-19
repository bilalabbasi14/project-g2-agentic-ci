"""Typed structures passed between pipeline components.

Every structure round-trips through plain JSON (to_dict / from_dict) and is
validated against the JSON Schemas in schemas.py.
"""
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

FALLBACK_REASONS = ("timeout", "invalid_json", "schema_violation", "low_confidence", "provider_error")
RANKING_SOURCES = ("llm", "dante_fallback", "dante", "random", "history_only", "tfidf_only")


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
