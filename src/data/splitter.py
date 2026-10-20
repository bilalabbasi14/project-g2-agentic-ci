"""Chronological history split.

Same rule as main() in DANTE's run_selection.py: the history of a target
build is the NUM_BUILDS_FOR_PROB_MODEL most recent builds of the project
whose timestamp is strictly earlier than the target's, taken from all builds
in dataset.csv (not only the evaluation builds).
"""


def history_window(metadata, target_timestamp, num_builds):
    """metadata: chronologically sorted DataFrame with 'timestamp_for_sort'."""
    return metadata[metadata['timestamp_for_sort'] < target_timestamp].tail(num_builds)


def previous_builds(metadata, target_timestamp, n):
    """The n builds immediately before the target, most recent first."""
    return history_window(metadata, target_timestamp, n).iloc[::-1]
