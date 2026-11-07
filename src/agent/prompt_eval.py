"""Compare relevance prompt versions on the dev split and apply the fixed decision rule (P2-07).

    python -m src.agent.prompt_eval --runs results/DEV_prompt_v1 results/DEV_prompt_v2 \
        [--out results/dev/prompt_comparison.csv]

Reads each run folder's per_build.csv (method LLM-relevance) and llm_relevance.csv.
Decision rule, fixed before the runs: the prompt with the higher sapfdc_mean_10
wins; if the two are within TIE_MARGIN, the one with the lower share_rel_le_0_2
wins. Only dev-split runs may be compared (leakage rule 3).
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

METHOD = "LLM-relevance"
BUDGET = 0.10
TIE_MARGIN = 0.005
COLUMNS = ["prompt_version", "builds", "dtc_mean_10", "sapfdc_mean_10", "share_rel_le_0_2", "share_rel_ge_0_5",
           "fallback_builds", "mean_latency_s"]


def summarise_run(run_dir):
    """One comparison row for one run folder."""
    run_dir = Path(run_dir)
    pb = pd.read_csv(run_dir / "per_build.csv")
    if set(pb["split"].astype(str)) != {"dev"}:
        raise ValueError(f"{run_dir}: prompt comparison uses dev-split runs only, found {sorted(set(pb['split']))}")
    rows = pb[(pb["method"] == METHOD) & ((pb["budget"] - BUDGET).abs() < 1e-9)]
    if rows.empty:
        raise ValueError(f"{run_dir}: no {METHOD} rows at budget {BUDGET}")
    rel = pd.read_csv(run_dir / "llm_relevance.csv")
    rel = rel[rel["relevance_source"] == "llm_shortlist"]
    versions = sorted(set(rel["prompt_version"].astype(str)))
    if len(versions) != 1:
        raise ValueError(f"{run_dir}: expected one prompt version in llm_relevance.csv, found {versions}")
    calls = rows["llm_calls"].sum()
    return {
        "prompt_version": versions[0],
        "builds": int(rows["build"].nunique()),
        "dtc_mean_10": float(rows["dtc"].mean()),
        "sapfdc_mean_10": float(rows["sapfdc"].mean()),
        "share_rel_le_0_2": float((rel["relevance"] <= 0.2).mean()) if len(rel) else 0.0,
        "share_rel_ge_0_5": float((rel["relevance"] >= 0.5).mean()) if len(rel) else 0.0,
        "fallback_builds": int((rows["ranking_source"] == "dante_fallback").sum()),
        "mean_latency_s": float(rows["llm_latency_s"].sum() / calls) if calls else 0.0,
    }


def compare_prompts(run_dirs):
    """DataFrame with one row per prompt version (COLUMNS)."""
    return pd.DataFrame([summarise_run(d) for d in run_dirs], columns=COLUMNS)


def choose(df):
    """(winner, explanation) by the fixed rule: higher sapfdc_mean_10; within TIE_MARGIN, lower share_rel_le_0_2."""
    if len(df) != 2:
        raise ValueError("the decision rule compares exactly two prompts")
    a, b = df.iloc[0], df.iloc[1]
    diff = a["sapfdc_mean_10"] - b["sapfdc_mean_10"]
    if abs(diff) > TIE_MARGIN:
        win = a if diff > 0 else b
        return win["prompt_version"], (f"higher sapfdc_mean_10 ({win['sapfdc_mean_10']:.4f}; difference "
                                       f"{abs(diff):.4f} > {TIE_MARGIN})")
    win = a if a["share_rel_le_0_2"] <= b["share_rel_le_0_2"] else b
    return win["prompt_version"], (f"sapfdc_mean_10 within {TIE_MARGIN} (difference {abs(diff):.4f}); lower "
                                   f"share_rel_le_0_2 ({win['share_rel_le_0_2']:.4f})")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare relevance prompts on dev-split runs.")
    ap.add_argument("--runs", nargs=2, required=True, help="the two run folders (v1 and v2)")
    ap.add_argument("--out", default="results/dev/prompt_comparison.csv")
    args = ap.parse_args(argv)
    df = compare_prompts(args.runs)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, lineterminator="\n")
    winner, why = choose(df)
    print(df.to_string(index=False))
    print(f"winner: {winner} ({why}) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
