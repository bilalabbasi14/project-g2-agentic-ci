"""history_retrieval tool: past outcomes of one test class from local LRTS files.

Takes the test_class.csv.zip paths of the history builds, oldest first (the
caller chooses which builds, e.g. the 100 builds before the target). Reads
only those files; outcome 1 = fail, anything else counts as not failed.
"""
import csv
import io
import zipfile


def read_test_class_zip(path):
    """Return {testclass: (outcome, duration)} from one LRTS test_class.csv.zip."""
    with zipfile.ZipFile(path) as z:
        name = next(n for n in z.namelist() if n.lower().endswith("test_class.csv"))
        with z.open(name) as fh:
            rows = csv.DictReader(io.TextIOWrapper(fh, "utf-8"))
            out = {}
            for r in rows:
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


class HistoryRetrieval:
    def __init__(self, history_zip_paths, recent=10):
        self.paths = list(history_zip_paths)
        self.recent = recent
        self._builds = None

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
