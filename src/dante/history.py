"""DANTE history signal.

Mirrors build_statistical_model and the history part of calculate_all_scores
in DANTE's run_selection.py:

    THFR(t)     = mean outcome of t over the history builds
    P_n         = P(fail | sticky_n), pooled over all tests; 0 if fewer than
                  MIN_STICKY_EVENTS_FOR_CONFIDENCE sticky events
    history(t)  = THFR(t) + sum_n [last_outcome_n(t) == 1] * P_n / n

A Wilson 95% interval is computed per window (as DANTE does) and reported as
'confidence', but it is not used in the score.

Note: DANTE computes is_sticky as
    full_history.groupby('testclass')['outcome'].shift(1).rolling(window=n, min_periods=1).max()
The rolling window runs over consecutive rows of the whole frame, not per
test class. This is reproduced as written (sticky_mode="dante");
sticky_mode="per_test" gives the per-test reading for comparison.
"""
import math

import pandas as pd


def wilson_interval(successes, n, z=1.96):
    """Wilson score interval (as in build_statistical_model)."""
    if n == 0:
        return 0.0, 0.0
    p = successes / n
    denom = 1 + z ** 2 / n
    centre = p + z ** 2 / (2 * n)
    spread = z * math.sqrt((p * (1 - p) + z ** 2 / (4 * n)) / n)
    return (centre - spread) / denom, (centre + spread) / denom


def build_statistical_model(history_frames, windows, min_events=20, sticky_mode="dante"):
    """history_frames: test_class DataFrames of the history builds, each with a
    'build_index' column (chronological position). Returns {'thfr', 'p_fail_sticky_model'}."""
    frames = [f for f in history_frames if f is not None]
    if not frames:
        return None
    full = pd.concat(frames, ignore_index=True)
    full = full.sort_values(by='build_index').set_index('build_index')
    thfr = full.groupby('testclass')['outcome'].mean().to_dict()
    p_base = full['outcome'].mean()
    prob_map = {}
    for n in windows:
        shifted = full.groupby('testclass')['outcome'].shift(1)
        if sticky_mode == "dante":
            is_sticky = shifted.rolling(window=n, min_periods=1).max()
        else:
            tmp = pd.DataFrame({'t': full['testclass'].values, 's': shifted.values})
            is_sticky = pd.Series(tmp.groupby('t')['s'].transform(
                lambda s: s.rolling(window=n, min_periods=1).max()).values, index=full.index)
        sticky = pd.DataFrame({'outcome': full['outcome'], 'is_sticky': is_sticky == 1.0})
        ev = sticky[sticky['is_sticky']]
        count, fails = len(ev), ev['outcome'].sum()
        if count < min_events:
            prob_map[str(n)] = {'prob': 0.0, 'lift': 1.0, 'confidence': 0.0, 'events': count}
        else:
            p_hat = fails / count
            lo, hi = wilson_interval(fails, count)
            prob_map[str(n)] = {'prob': p_hat, 'lift': p_hat / p_base if p_base > 0 else 1.0,
                                'confidence': 1.0 - (hi - lo), 'events': count}
    return {'thfr': thfr, 'p_fail_sticky_model': prob_map}


def last_outcomes(previous_builds, windows):
    """previous_builds: list of {testclass: outcome} for the builds before the
    target, most recent first. Returns {testclass: {n: outcome n builds ago}}
    (0 when the test did not run), like augment_history.py."""
    tests = set().union(*previous_builds) if previous_builds else set()
    out = {}
    for t in tests:
        out[t] = {n: (previous_builds[n - 1].get(t, 0) if n - 1 < len(previous_builds) else 0) for n in windows}
    return out


def history_score(test, model, last_outcome):
    """THFR + sum over windows of P_n / n where the test failed exactly n builds ago."""
    score = model['thfr'].get(test, 0)
    for n_str, data in model['p_fail_sticky_model'].items():
        if last_outcome.get(int(n_str), 0) == 1:
            score += (1.0 / int(n_str)) * data['prob']
    return score


def total_failures(history_frames):
    """Sum of outcomes per test over the history builds (history_lookup in calculate_all_scores)."""
    frames = [f for f in history_frames if f is not None]
    if not frames:
        return {}
    full = pd.concat(frames, ignore_index=True)
    return full.groupby('testclass')['outcome'].sum().to_dict()
