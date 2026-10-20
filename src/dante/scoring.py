"""Per-test scores and the DANTE-CCH value, mirroring calculate_all_scores and
calculate_hybrid_scores in DANTE's run_selection.py.

    base       = w_h * history + w_r * max_relevance ** power
    DANTE-CCH  = base * max(total_failures_in_history, 0.1) / max(duration, 0.001)

The returned DataFrame is built from a dict in test-case order, like the
original, so pandas sort order on ties matches.
"""
import pandas as pd

from src.dante.history import build_statistical_model, history_score, last_outcomes, total_failures
from src.dante.relevance import max_relevance, relevance_per_file


def compute_relevance(build):
    """{test: {changed_file: normalised TF-IDF score}} over tests with tokens."""
    return relevance_per_file({t.name: t.tokens for t in build.test_cases.values() if t.tokens is not None},
                              build.diff_tokens)


def score_table(build, history, windows, min_events=20, w_history=1.0, w_relevance=0.5,
                power=1.2, relevance_override=None, sticky_mode="dante"):
    """One row per candidate test (source found, duration > 0).

    relevance_override: optional {test: value in [0, 1]} replacing max TF-IDF
    relevance for the listed tests (used for the LLM variant).
    """
    model = build_statistical_model(history.frames, windows, min_events, sticky_mode)
    if model is None:
        return None, None
    lo = last_outcomes(history.previous_outcomes, windows)
    fails = total_failures(history.frames)
    rel = compute_relevance(build)
    rows = {}
    for t in build.candidates():
        h = history_score(t.name, model, lo.get(t.name, {}))
        r_tfidf = max_relevance(rel.get(t.name, {}))
        r = r_tfidf
        if relevance_override and t.name in relevance_override:
            r = relevance_override[t.name]
        base = w_history * h + w_relevance * (r ** power)
        f = fails.get(t.name, 0)
        rows[t.name] = {
            'history_score': h,
            'tfidf_relevance': r_tfidf,
            'relevance_used': r,
            'base_score': base,
            'total_failures': f,
            'duration': t.duration,
            'actual_outcome': t.outcome,
            'dante_cch_score': base * max(f, 0.1) / max(t.duration, 0.001),
        }
    df = pd.DataFrame.from_dict(rows, orient='index')
    return df, model
