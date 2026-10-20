"""Aggregate results/runs/<build>.json into results/initial_results.csv and print
the README table.

    python -m src.eval.summarize

Per method and budget: number of builds, mean and median %DTC, mean and median
SAPFDc, median SDS, and median APFDc of the full ranking (budget-independent;
for the stored methods it is the RQ1 apfdc column). LLM rows add mean latency,
total tokens and the number of fallbacks. Builds without failures would be
excluded from %DTC and SAPFDc (all evaluation builds have failures).
"""
import glob
import json
import os

import pandas as pd

from src.eval.stored import rq1_table
from src.settings import load_config, repo_path

ORDER = ["Random (stored)", "Random", "DANTE-CCH (stored)", "DANTE-CCH-shipped", "DANTE-CCH",
         "History-only", "TF-IDF-only", "LLM-relevance"]


def load_runs(runs_dir):
    return [json.load(open(f)) for f in sorted(glob.glob(os.path.join(runs_dir, "PR-*_build*.json")))
            if not f.endswith("_mock.json")]


def main():
    cfg = load_config()
    runs = load_runs(repo_path(cfg["paths"]["results_dir"]) / "runs")
    if not runs:
        raise SystemExit("no run JSONs found; run run_end_to_end.py first")
    rq1 = rq1_table(cfg["paths"]["dante_root"])
    rq1 = rq1[rq1.project == cfg["project"]].set_index(["build", "method"])["apfdc"]
    rows = []
    for r in runs:
        for pb in r["budgets"]:
            for m, v in pb["methods"].items():
                ap = v.get("apfdc_full")
                if m.endswith("(stored)"):
                    ap = float(rq1[(r["build_name"], m.replace(" (stored)", ""))])
                rows.append({"build": r["build"], "budget": pb["budget"], "method": m,
                             "dtc": v["dtc"], "sapfdc": v["sapfdc"], "sds": v["sds"], "apfdc": ap})
    df = pd.DataFrame(rows)
    g = df.groupby(["method", "budget"])
    out = pd.DataFrame({
        "builds": g["build"].nunique(),
        "dtc_mean": g["dtc"].mean(), "dtc_median": g["dtc"].median(),
        "sapfdc_mean": g["sapfdc"].mean(), "sapfdc_median": g["sapfdc"].median(),
        "sds_median": g["sds"].median(), "apfdc_median": g["apfdc"].median(),
    }).reset_index()
    out["method"] = pd.Categorical(out["method"], ORDER, ordered=True)
    out = out.sort_values(["budget", "method"])

    calls = sum(r["llm"]["calls"] for r in runs)
    lat = [r["llm"]["mean_latency_s"] * r["llm"]["calls"] for r in runs if r["llm"]["calls"]]
    llm = {"llm_calls": calls,
           "llm_mean_latency_s": sum(lat) / calls if calls else None,
           "llm_prompt_tokens": sum(r["llm"]["prompt_tokens"] for r in runs),
           "llm_completion_tokens": sum(r["llm"]["completion_tokens"] for r in runs),
           "llm_fallbacks": sum(len(r["fallbacks"]) for r in runs),
           "llm_builds_fallen_back": sum(r["llm_source"] == "dante_fallback" for r in runs)}
    for k, v in llm.items():
        out[k] = [v if m == "LLM-relevance" else None for m in out["method"]]
    dest = repo_path(cfg["paths"]["results_dir"]) / "initial_results.csv"
    out.to_csv(dest, index=False, float_format="%.6f")

    builds = sorted(r["build"] for r in runs)
    print(f"builds ({len(builds)}): {', '.join(builds)}\n")
    budgets = sorted(out["budget"].unique())
    head = "| Method | " + " | ".join(f"%DTC {int(round(b * 100))}%" for b in budgets) + " | " + \
           " | ".join(f"SAPFDc {int(round(b * 100))}%" for b in budgets) + " | APFDc |"
    print(head)
    print("|" + "---|" * (2 + 2 * len(budgets)))
    for m in ORDER:
        s = out[out["method"] == m].set_index("budget")
        if s.empty:
            continue
        cells = [f"{s.loc[b, 'dtc_mean']:.3f}" for b in budgets] + [f"{s.loc[b, 'sapfdc_mean']:.3f}" for b in budgets]
        print(f"| {m} | " + " | ".join(cells) + f" | {s['apfdc_median'].iloc[0]:.3f} |")
    print(f"\n%DTC and SAPFDc: mean over builds; APFDc: median over builds of the full ranking.")
    print(f"LLM: {llm['llm_calls']} calls, mean latency {llm['llm_mean_latency_s']:.1f} s, "
          f"{llm['llm_prompt_tokens']} prompt + {llm['llm_completion_tokens']} completion tokens, "
          f"{llm['llm_fallbacks']} fallbacks ({llm['llm_builds_fallen_back']} builds used the DANTE ranking)")
    print(f"-> {dest}")


if __name__ == "__main__":
    main()
