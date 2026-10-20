"""Evaluation metrics.

APFDc follows calculate_apfdc_metric in DANTE's run_prioritization.py:

    APFDc = 1 - sum_i (C_before_i + d_i / 2) / (m * C_total) + 1 / (2 n)

where the sum runs over the m failing tests of the scored set, C_before_i is
the summed duration of tests ordered before failing test i, d_i its duration,
C_total the summed duration of the scored set and n its size. APFDc = 1.0 when
m = 0 and 0.0 when C_total = 0 (as in the original).

%DTC   = failing classes in the selection / failing classes among candidates.
         Undefined (None) for builds with no failing candidate; such builds are
         excluded from %DTC and SAPFDc.
SAPFDc = %DTC x APFDc computed on the selected tests in selection order
         (m, C_total and n taken over the selection). The package readme names
         SAPFDc but ships no implementation; this is our definition. We do not use
         post_hoc_prioritizer.calculate_napfdc, whose fallback sets fault coverage to 1.
SDS    = distinct Java packages in the selection / selection size (None if empty).
         Also named but not implemented in the package.
"""


def apfdc(order, durations, failing):
    """order: test names; durations: {test: seconds}; failing: set of failing test names."""
    m = sum(1 for t in order if t in failing)
    n = len(order)
    if m == 0:
        return 1.0
    total = sum(durations[t] for t in order)
    if total == 0:
        return 0.0
    cum, s = 0.0, 0.0
    for t in order:
        d = durations[t]
        if t in failing:
            s += cum + d / 2.0
        cum += d
    return 1.0 - s / (m * total) + 1.0 / (2.0 * n)


def dtc(selected, failing):
    """Fraction of failing tests caught; None if there are no failing tests."""
    if not failing:
        return None
    return len(set(selected) & set(failing)) / len(failing)


def sapfdc(selected, durations, failing):
    d = dtc(selected, failing)
    if d is None:
        return None
    if d == 0:
        return 0.0
    return d * apfdc(selected, durations, set(failing))


def package_of(test):
    return test.split("$")[0].rsplit(".", 1)[0] if "." in test else ""


def sds(selected):
    if not selected:
        return None
    return len({package_of(t) for t in selected}) / len(selected)


def all_metrics(selected, durations, failing, full_order=None):
    """Metrics for one build/budget. full_order (optional) gives APFDc of the full ranking."""
    failing = set(failing)
    out = {"dtc": dtc(selected, failing), "sapfdc": sapfdc(selected, durations, failing),
           "sds": sds(selected), "selected": len(selected),
           "found": len(set(selected) & failing), "total_failures": len(failing),
           "selected_duration": sum(durations[t] for t in selected)}
    if full_order is not None:
        out["apfdc_full"] = apfdc(full_order, durations, failing)
    return out
