"""history_retrieval tool: past outcomes of one test class from local LRTS files.

Takes the test_class.csv.zip paths of the history builds, oldest first (the
caller chooses which builds, e.g. the 100 builds before the target). Reads
only those files; outcome 1 = fail, anything else counts as not failed.

A build's test results may be stored as the original `test_class.csv.zip` or,
in the copy Kaggle serves, already extracted as `test_class.csv` in the same
folder. resolve_test_class_file / open_test_class_csv accept both, so laptops
and Kaggle use the same code.
"""
import contextlib
import csv
import io
import os
import zipfile

CSV_NAME = "test_class.csv"


def resolve_test_class_file(zip_path):
    """Return the existing results file for a build: the .zip if present, else the
    extracted test_class.csv next to it, else None. Accepts str or path-like."""
    zip_path = os.fspath(zip_path)
    if os.path.isfile(zip_path):
        return zip_path
    extracted = os.path.join(os.path.dirname(zip_path), CSV_NAME)
    return extracted if os.path.isfile(extracted) else None


@contextlib.contextmanager
def open_test_class_csv(path):
    """Open test_class.csv as UTF-8 text, from inside a .zip or as a plain file."""
    path = os.fspath(path)
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.lower().endswith(CSV_NAME))
            with z.open(name) as fh:
                yield io.TextIOWrapper(fh, "utf-8")
    else:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            yield fh


def read_test_class_zip(path):
    """Return {testclass: (outcome, duration)} from one build's test results
    (test_class.csv.zip, or its extracted test_class.csv)."""
    resolved = resolve_test_class_file(path) or path
    with open_test_class_csv(resolved) as fh:
        out = {}
        for r in csv.DictReader(fh):
            if not r.get("testclass"):
                continue
            try:
                outcome = int(float(r.get("outcome") or 0))
            except ValueError:
                outcome = 0
            try:
                duration = float(r.get("duration") or 0)
            except ValueError:
                duration = 0.0
            out[r["testclass"]] = (outcome, duration)
        return out


def _frame_to_outcomes(frame):
    """{testclass: (outcome, duration)} from an in-memory test_class frame, with
    the same parsing as read_test_class_zip (empty names skipped, bad numbers -> 0)."""
    out = {}
    cols = frame.columns
    for r in frame.to_dict("records"):
        name = r.get("testclass")
        if name is None or name != name or name == "":   # None, NaN or empty
            continue
        o = r.get("outcome") if "outcome" in cols else 0
        try:
            outcome = int(float(o)) if o == o and o not in (None, "") else 0
        except (TypeError, ValueError):
            outcome = 0
        d = r.get("duration") if "duration" in cols else 0
        try:
            duration = float(d) if d == d and d not in (None, "") else 0.0
        except (TypeError, ValueError):
            duration = 0.0
        out[str(name)] = (outcome, duration)
    return out


class HistoryRetrieval:
    def __init__(self, history_zip_paths, recent=10):
        self.paths = list(history_zip_paths)
        self.recent = recent
        self._builds = None

    @classmethod
    def from_frames(cls, frames, recent=10):
        """Build the tool from frames already in memory (HistoryData.frames, oldest
        first; columns testclass, outcome, duration). Gives the same output as
        reading the equivalent test_class files, without any disk access."""
        tool = cls([], recent)
        tool._builds = [_frame_to_outcomes(f) for f in frames]
        return tool

    def _load(self):
        if self._builds is None:
            self._builds = [read_test_class_zip(p) for p in self.paths]
        return self._builds

    def __call__(self, test):
        builds = self._load()
        outcomes = [b[test][0] for b in builds if test in b]
        n = len(builds)
        last_fail = next((n - i for i in range(n - 1, -1, -1)
                          if test in builds[i] and builds[i][test][0] == 1), None)
        recent = [(b[test][0] if test in b else None) for b in builds[-self.recent:]] if self.recent else []
        return {
            "test": test,
            "history_builds": n,
            "runs": len(outcomes),
            "failures": sum(1 for o in outcomes if o == 1),
            "failure_rate": (sum(1 for o in outcomes if o == 1) / len(outcomes)) if outcomes else 0.0,
            "last_failure_distance": last_fail,   # 1 = failed in the most recent history build
            "recent_outcomes": recent,            # oldest first; None = test not run in that build
        }
