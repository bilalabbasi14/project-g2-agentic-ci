"""Tool registry used by the orchestrator (Gap 3, docs/PROJECT_CONTEXT.md §5.3 step 5).

ToolRegistry implements ToolRegistryLike (src/contracts/interfaces.py). It is
built per build from data already in memory (history frames and the split
diff), so it needs no git clone and reads no file.

Only `history_retrieval` and `diff_reader` are offered. `budget_tracker` is
deliberately not offered to the orchestrator: the orchestrator only chooses the
weight w, and the budget is applied afterwards, when tests are ranked and
selected with that w for each budget fraction.

call() never raises: an unknown or not-offered tool, missing or wrong
arguments, or an exception inside the tool give ok=False and an error string.
"""
import time

from src.contracts import ToolCallRecord
from src.tools import TOOL_SPECS
from src.tools.diff_reader import DiffReader
from src.tools.history_retrieval import HistoryRetrieval

# required argument name of each tool the registry can offer
REQUIRED_ARG = {"history_retrieval": "test", "diff_reader": "file"}


class ToolRegistry:
    def __init__(self, tools, allowed=("history_retrieval", "diff_reader")):
        unknown = [a for a in allowed if a not in REQUIRED_ARG]
        if unknown:
            raise ValueError(f"tools not offered to the orchestrator: {unknown}")
        self.allowed = tuple(allowed)
        self.tools = {name: tools[name] for name in self.allowed}

    @classmethod
    def for_build(cls, history_frames, diff_files, allowed=("history_retrieval", "diff_reader")):
        """history_frames: HistoryData.frames (oldest first); diff_files: BuildData.diff_files."""
        tools = {"history_retrieval": HistoryRetrieval.from_frames(history_frames),
                 "diff_reader": DiffReader.from_files(diff_files)}
        return cls(tools, allowed)

    def specs(self):
        return [s for s in TOOL_SPECS if s["name"] in self.allowed]

    def call(self, name, args):
        t0 = time.perf_counter()
        safe_args = dict(args) if isinstance(args, dict) else {}

        def fail(msg):
            return ToolCallRecord(tool=str(name), args=safe_args, output={},
                                  latency_s=round(time.perf_counter() - t0, 6), ok=False, error=msg)

        if name not in self.tools:
            return fail(f"unknown tool {name!r}; available: {', '.join(self.allowed)}")
        if not isinstance(args, dict):
            return fail(f"args must be an object, got {type(args).__name__}")
        key = REQUIRED_ARG[name]
        value = args.get(key)
        if not isinstance(value, str) or not value:
            return fail(f"{name} needs {{\"{key}\": <string>}}")
        try:
            output = self.tools[name](value)
        except Exception as e:   # a broken tool must not stop the orchestrator
            return fail(f"{type(e).__name__}: {e}")
        return ToolCallRecord(tool=name, args=safe_args, output=dict(output),
                              latency_s=round(time.perf_counter() - t0, 6), ok=True, error=None)
