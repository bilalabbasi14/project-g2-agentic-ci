"""Tools available to the agent. All read local files only.

TOOL_SPECS describes each tool's name, purpose and input/output fields so an
orchestrator (planned) can list and call them.
"""
from .budget_tracker import BudgetTracker
from .diff_reader import DiffReader, split_diff
from .history_retrieval import HistoryRetrieval, read_test_class_zip

TOOL_SPECS = [
    {
        "name": "history_retrieval",
        "description": "Past outcomes of one test class over the history builds.",
        "input": {"test": "string (fully qualified test class)"},
        "output": {"test": "string", "history_builds": "int", "runs": "int", "failures": "int",
                   "failure_rate": "float", "last_failure_distance": "int|null",
                   "recent_outcomes": "list[int|null]"},
    },
    {
        "name": "diff_reader",
        "description": "Changed lines of one file in the build's diff.",
        "input": {"file": "string (repo-relative path)"},
        "output": {"file": "string", "found": "bool", "hunk_text": "string",
                   "changed_lines": "string", "added": "int", "removed": "int"},
    },
    {
        "name": "budget_tracker",
        "description": "Add a test if it fits in the remaining time budget.",
        "input": {"test": "string", "duration": "float (seconds)"},
        "output": {"added": "bool", "remaining_seconds": "float"},
    },
]

__all__ = ["BudgetTracker", "DiffReader", "HistoryRetrieval", "TOOL_SPECS", "read_test_class_zip",
           "split_diff"]
