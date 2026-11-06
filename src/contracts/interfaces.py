"""Interfaces between the pipeline and the Phase 2 components.

These Protocols only fix method names, arguments and return types so the
pipeline (P2-15), orchestrator (P2-06), explainer (P2-10) and single-call
scorer (P2-17) can be built in parallel. Real implementations come in those
issues; tests use the fakes in tests/fakes.py. Meanings follow
docs/PROJECT_CONTEXT.md §5.2-§5.3.
"""
from typing import Any, Callable, Dict, List, Protocol, Tuple, TYPE_CHECKING

from .models import ExplanationRecord, FallbackRecord, OrchestratorDecision, OrchestratorInput, ToolCallRecord

if TYPE_CHECKING:
    import pandas as pd


class ToolRegistryLike(Protocol):
    def specs(self) -> List[Dict[str, Any]]:
        """Describe the tools this registry offers (entries in the format of
        src.tools.TOOL_SPECS: name, description, input, output)."""
        ...

    def call(self, name: str, args: Dict[str, Any]) -> ToolCallRecord:
        """Run tool `name` with `args` and return its record. Must never raise:
        an unknown tool, bad arguments or an error inside the tool give
        ok=False and an error string."""
        ...


class OrchestratorLike(Protocol):
    def decide(self, inp: OrchestratorInput, tools: ToolRegistryLike, run_id: str) -> OrchestratorDecision:
        """Choose the history weight w for one build (Gap 3).

        In: the build's features and shortlist with all scores (never target-build
        outcomes), a tool registry for inspecting evidence, and the run id for
        tracing. Out: a validated decision with w in [0, 1], confidence and reason
        (source "agent"), or, after a failed or low-confidence answer, w = DANTE_W
        with source "fallback" and a FallbackRecord. Called once per build and
        relevance source; the same w is used for every budget."""
        ...


class ExplainerLike(Protocol):
    def explain(self, build_id: str, budget_fraction: float, df: "pd.DataFrame",
                selected: List[str], ordered: List[str], durations: Dict[str, float],
                budget_seconds: float, diff_files: Dict[str, dict],
                llm_reasons: Dict[str, str], history_tool: Callable[[str], Dict[str, Any]],
                run_id: str) -> List[ExplanationRecord]:
        """Explain important skipped tests for one build and budget (Gap 2).

        In: the score table, the selection and full ranking for this budget, test
        durations, the budget in seconds, the build's changed files, the semantic
        analyzer's reasons, and a history lookup per test. Out: one record per
        explained skipped test (at most cfg explainer.top_n_skipped), each with the
        evidence given to the LLM; a failed explanation has ok=False. Runs after
        selection and never changes it; never reads target-build outcomes."""
        ...


class SingleCallScorerLike(Protocol):
    def score(self, build_id: str, diff_text: str, candidates: List[str], run_id: str
              ) -> Tuple[Dict[str, float], List[FallbackRecord], int]:
        """Non-agentic baseline: one LLM call that rates every candidate.

        In: the build's diff and all candidate test names (in DANTE-CCH value
        order). Out: (relevance per test in [0, 1], fallback records, number of
        LLM calls). On fallback the relevance dict is empty and the pipeline uses
        the DANTE ranking for this method."""
        ...
