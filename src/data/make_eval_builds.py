"""Write data_eval/eval_builds.csv from DANTE's experiments/RQ1/<project>.csv.

    python -m src.data.make_eval_builds

One row per evaluation build: stored build name, LRTS keys, commit, timestamp,
LRTS num_fail_class, whether the diff has code changes, stored total_failures_in_build (DANTE-CCH, 10% budget
solution JSON) and the stored RQ1 DANTE-CCH APFDc. Fails if any build is not
in dataset.csv.
"""
import json
import os
import sys

import pandas as pd

from src.dante.tokenize import clean_and_tokenize_source
from src.data.loader import LRTSLoader, parse_stored_build_name
from src.tools.diff_reader import split_diff
from src.settings import load_config, repo_path



def main():
    cfg = load_config()
    p = cfg["paths"]
    rq1 = pd.read_csv(os.path.join(p["dante_root"], "experiments", "RQ1", f"{cfg['project']}.csv"))
    loader = LRTSLoader(p["lrts_root"], cfg["project"])
    rows, missing = [], []
    for name in rq1["build"].unique():
        _, pr, bid, stage = parse_stored_build_name(name)
        try:
            r = loader.row(pr, bid, stage)
        except KeyError:
            missing.append(name)
            continue
        sol = os.path.join(p["dante_solutions"], "Budget_10_Percent", name, "DANTE-CCH.json")
        stored_total = json.load(open(sol))["total_failures_in_build"] if os.path.exists(sol) else None
        apfdc = rq1[(rq1.build == name) & (rq1.method == "DANTE-CCH")]["apfdc"]
        diff_files = split_diff(open(loader.diff_path(r), encoding="utf-8", errors="ignore").read())
        has_code = any(clean_and_tokenize_source(v["changed_lines"], os.path.splitext(f)[1])[0]
                       for f, v in diff_files.items())
        rows.append({
            "build_name": name, "key": r["key"], "pr_name": pr, "build_id": bid, "stage_id": stage,
            "build_head_sha": r["build_head_sha"], "build_timestamp": r["build_timestamp"],
            "chrono_index": int(r.name), "lrts_num_fail_class": int(r["num_fail_class"]),
            "stored_total_failures": stored_total,
            "has_code_diff": has_code, "n_code_files": len(diff_files),
            "rq1_dante_cch_apfdc": float(apfdc.iloc[0]) if len(apfdc) else None,
        })
    out = pd.DataFrame(rows).sort_values("chrono_index")
    # Phase-1 subset: builds whose diff changes at least one file DANTE does not
    # ignore (EXTENSIONS_TO_IGNORE_IN_DIFF) and yields tokens. In the other builds
    # relevance (TF-IDF or LLM) has no input, so all relevance variants coincide.
    out["phase1_subset"] = out["has_code_diff"].astype(int)
    dest = repo_path(p["eval_builds"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dest, index=False)
    print(f"eval builds in RQ1 csv: {rq1['build'].nunique()}  found in dataset.csv: {len(out)}  "
          f"missing: {len(missing)}  phase1 subset: {int(out.phase1_subset.sum())}  -> {dest}")
    if missing:
        print("missing:", missing)
        sys.exit(1)


if __name__ == "__main__":
    main()
