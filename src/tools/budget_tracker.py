"""budget_tracker tool: greedy time-budget bookkeeping.

Same rule as DANTE's run_prioritization_solver (run_selection.py): a test is
taken if cumulative duration stays <= budget; tests that do not fit are
skipped and scanning continues.
"""


class BudgetTracker:
    def __init__(self, budget_seconds):
        if budget_seconds < 0:
            raise ValueError("budget must be >= 0")
        self.budget = float(budget_seconds)
        self.used = 0.0
        self.selected = []

    @property
    def remaining(self):
        return self.budget - self.used

    def try_add(self, test, duration):
        if self.used + duration <= self.budget:
            self.selected.append(test)
            self.used += duration
            return True
        return False

    def fill(self, ordered_tests, durations):
        """Greedily add tests in the given order; return the selected list."""
        for t in ordered_tests:
            self.try_add(t, durations[t])
        return list(self.selected)

    def state(self):
        return {"budget_seconds": self.budget, "used_seconds": self.used,
                "remaining_seconds": self.remaining, "selected": list(self.selected)}
