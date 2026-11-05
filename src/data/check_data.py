"""Check that a data folder has everything the code expects.

    python -m src.data.check_data [--lrts <lrts_root>] [--dante <dante_root>] [--solutions <dante_solutions>]

Defaults are paths.lrts_root, paths.dante_root and paths.dante_solutions from
config.yaml (or the file in G2_CONFIG). Prints one line per check with OK,
MISSING or WRONG and exits with code 0 only if every check passes.
"""
import argparse
import csv
import os
import sys

from src.data.loader import build_key
from src.settings import load_config

BUDGET_DIRS = ("Budget_05_Percent", "Budget_10_Percent", "Budget_20_Percent")
STRATEGIES = ("DANTE-CCH", "Random")
MAX_LISTED = 5


def _karaf_builds(dataset_csv, project):
    """(pr_name, build_id, stage_id) of every dataset.csv row of the project."""
    with open(dataset_csv, newline="", encoding="utf-8") as f:
        return [(r["pr_name"], r["build_id"], r["stage_id"]) for r in csv.DictReader(f)
                if (r.get("project") or "").lower() == project.lower()]


def _listed(keys):
    shown = ", ".join(keys[:MAX_LISTED])
    return shown + (f" (+{len(keys) - MAX_LISTED} more)" if len(keys) > MAX_LISTED else "")


def check(lrts_root, dante_root, solutions_root, expected_builds=726, expected_eval_builds=50,
          project="karaf"):
    """Return one (name, passed, detail) tuple per check.

    Checks: dataset.csv has `expected_builds` rows of the project; each of those
    builds has its test_class.csv.zip and its .diff; DANTE's RQ1 CSV for the
    project lists `expected_eval_builds` distinct builds; each stored-solution
    budget folder has that many build folders, each with DANTE-CCH.json and
    Random.json. A missing file gives a detail starting with "missing".
    """
    results = []
    dataset = os.path.join(lrts_root, "dataset.csv")
    builds = []
    if not os.path.isfile(dataset):
        results.append(("dataset.csv", False, f"missing: {dataset}"))
    else:
        builds = _karaf_builds(dataset, project)
        results.append(("dataset.csv", len(builds) == expected_builds,
                        f"{len(builds)} {project} rows (expected {expected_builds})"))

    keys = [build_key(pr, bid) for pr, bid, _ in builds]
    zips = [os.path.join(lrts_root, "processed_test_result", project, build_key(pr, bid), f"stage_{st}",
                         "test_class.csv.zip") for pr, bid, st in builds]
    diffs = [os.path.join(lrts_root, "shadata", project, "diff", f"{k}.diff") for k in keys]
    for name, paths in (("test_class.csv.zip per build", zips), (".diff per build", diffs)):
        if not builds:
            results.append((name, False, "missing: no builds to check (dataset.csv missing or empty)"))
            continue
        missing = [k for k, p in zip(keys, paths) if not os.path.isfile(p)]
        detail = f"{len(keys) - len(missing)} of {len(keys)} found"
        results.append((name, not missing, detail + (f"; missing: {_listed(missing)}" if missing else "")))

    rq1 = os.path.join(dante_root, "experiments", "RQ1", f"{project}.csv")
    if not os.path.isfile(rq1):
        results.append((f"RQ1/{project}.csv", False, f"missing: {rq1}"))
    else:
        with open(rq1, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        n = len({r["build"] for r in rows})
        results.append((f"RQ1/{project}.csv", n == expected_eval_builds,
                        f"{n} distinct builds in {len(rows)} rows (expected {expected_eval_builds} builds)"))

    for budget in BUDGET_DIRS:
        folder = os.path.join(solutions_root, budget)
        name = f"solutions {budget}"
        if not os.path.isdir(folder):
            results.append((name, False, f"missing: {folder}"))
            continue
        build_dirs = sorted(d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d)))
        incomplete = [d for d in build_dirs
                      if not all(os.path.isfile(os.path.join(folder, d, f"{s}.json")) for s in STRATEGIES)]
        detail = f"{len(build_dirs)} build folders (expected {expected_eval_builds})"
        if incomplete:
            detail += f"; missing DANTE-CCH.json or Random.json in: {_listed(incomplete)}"
        results.append((name, len(build_dirs) == expected_eval_builds and not incomplete, detail))
    return results


def status_word(passed, detail):
    if passed:
        return "OK"
    return "MISSING" if "missing" in detail else "WRONG"


def main(argv=None):
    cfg = load_config()
    p = cfg["paths"]
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lrts", default=p["lrts_root"])
    ap.add_argument("--dante", default=p["dante_root"])
    ap.add_argument("--solutions", default=p["dante_solutions"])
    args = ap.parse_args(argv)
    results = check(args.lrts, args.dante, args.solutions, project=cfg["project"])
    for name, passed, detail in results:
        print(f"{status_word(passed, detail):7s} {name}: {detail}")
    ok = all(passed for _, passed, _ in results)
    print("all checks passed" if ok else "some checks failed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
