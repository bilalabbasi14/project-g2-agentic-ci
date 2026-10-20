"""Extract only the needed parts of the two archives (see data/README.md).

    python -m src.data.extract_inputs --downloads <folder with the zips>

Writes to paths.lrts_root, paths.dante_root and paths.dante_solutions from config.yaml.
Existing files are overwritten. Uses zipfile only (no unzip needed on Windows).
"""
import argparse
import os
import re
import zipfile

from src.settings import load_config

SOLUTION = re.compile(r"ML_TCSP/experiments/RQ2 and RQ3/{project}_\d{{8}}-\d{{6}}/(Budget_(?:05|10|20)_Percent)/"
                      r"({project}_build_[^/]+)/solution_classical_(DANTE-CCH|Random)_[^/]+\.json")


def _write(z, info, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with z.open(info) as r, open(dest, "wb") as w:
        w.write(r.read())


def extract_lrts(zip_path, dest_root, project):
    n = 0
    with zipfile.ZipFile(zip_path) as z:
        for i in z.infolist():
            f = i.filename
            if i.is_dir():
                continue
            if (f == "long_running_test_suites/dataset.csv"
                    or f.startswith(f"long_running_test_suites/processed_test_result/{project}/")
                    or f.startswith(f"long_running_test_suites/shadata/{project}/")):
                _write(z, i, os.path.join(dest_root, f.split("/", 1)[1]))
                n += 1
    return n


def extract_dante(zip_path, dante_root, solutions_root, project):
    n = 0
    sol = re.compile(SOLUTION.pattern.format(project=re.escape(project)))
    with zipfile.ZipFile(zip_path) as z:
        for i in z.infolist():
            f = i.filename
            if re.fullmatch(r"ML_TCSP/src/[^/]+\.(py|md)", f) or re.fullmatch(r"ML_TCSP/experiments/RQ1/[^/]+\.csv", f):
                _write(z, i, os.path.join(dante_root, f.split("/", 1)[1]))
                n += 1
                continue
            m = sol.fullmatch(f)
            if m:
                _write(z, i, os.path.join(solutions_root, m.group(1), m.group(2), f"{m.group(3)}.json"))
                n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--downloads", required=True)
    args = ap.parse_args()
    cfg = load_config()
    p = cfg["paths"]
    n1 = extract_lrts(os.path.join(args.downloads, "long_running_test_suites.zip"), p["lrts_root"], cfg["project"])
    n2 = extract_dante(os.path.join(args.downloads, "ML_TCSP.zip"), p["dante_root"], p["dante_solutions"], cfg["project"])
    print(f"LRTS files: {n1} -> {p['lrts_root']}\nDANTE files: {n2} -> {p['dante_root']}, {p['dante_solutions']}")


if __name__ == "__main__":
    main()
