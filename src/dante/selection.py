"""Greedy budgeted selection, mirroring run_prioritization_solver and
run_random_solver in DANTE's run_selection.py (pandas sort / sample are used
as in the original so tie order matches)."""


def greedy_select(df, score_column, budget_seconds, ascending=False):
    """Sort by score, then take tests while cumulative duration <= budget;
    tests that do not fit are skipped and scanning continues."""
    ordered = df.sort_values(by=score_column, ascending=ascending)
    return _fill(ordered, budget_seconds), ordered.index.tolist()


def random_select(df, budget_seconds, seed=42):
    ordered = df.sample(frac=1, random_state=seed)
    return _fill(ordered, budget_seconds), ordered.index.tolist()


def _fill(ordered, budget_seconds):
    selected, used = [], 0.0
    for fqn, row in ordered.iterrows():
        if used + row['duration'] <= budget_seconds:
            selected.append(fqn)
            used += row['duration']
    return selected
