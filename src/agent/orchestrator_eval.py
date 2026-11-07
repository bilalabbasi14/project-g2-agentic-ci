"""Summarise orchestrator prompt iterations on the dev split (P2-06, item 4).

    python -m src.agent.orchestrator_eval --runs results/DEV_orch_o1 results/DEV_orch_o2 \
        [--out results/dev/orchestrator_prompt_iterations.csv]

One row per dev run of `Agent-weighted`: the orchestrator prompt version (from
run_meta.json), the fallback rate, the distribution of the chosen w, tool use,
and mean SAPFDc at 10% for Agent-weighted, LLM-relevance and DANTE-CCH on the same
builds. `rule_triggered` applies the rule fixed in issue #6: the prompt must be
improved if the orchestrator falls back on more than 20% of builds or gives the
same w for every build. Only dev-split runs are accepted (leakage rule 3).
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

MAX_FALLBACK_RATE = 0.20          # issue #6: more than this share of builds falling back -> improve the prompt
BUDGET = 0.10
SOURCE = "llm_shortlist"          # the relevance source of Agent-weighted
COLUMNS = ["prompt_version", "run_id", "git_commit", "builds", "fallback_rate", "distinct_w", "w_min", "w_mean",
           "w_max", "w_std", "mean_confidence", "mean_tool_calls", "sapfdc_mean_10_agent",
           "sapfdc_mean_10_llm_relevance", "sapfdc_mean_10_dante", "rule_triggered"]


def summarise_run(run_dir):
    run_dir = Path(run_dir)
    meta = json.loads((run_dir / "run_meta.json").read_text(encoding="utf-8"))
    if meta.get("split") != "dev":
        raise ValueError(f"{run_dir}: orchestrator prompt iterations use dev-split runs only, got {meta.get('split')!r}")
    if meta.get("git_commit_warning"):
        raise ValueError(f"{run_dir}: run mixes commits ({meta['git_commit_warning']}); rerun it from one commit")
    dec = pd.read_csv(run_dir / "orchestrator_decisions.csv")
    dec = dec[dec["relevance_source"] == SOURCE]
    if dec.empty:
        raise ValueError(f"{run_dir}: no orchestrator decisions for {SOURCE}")
    pb = pd.read_csv(run_dir / "per_build.csv")
    at = pb[(pb["budget"] - BUDGET).abs() < 1e-9]

    def sapfdc(method):
        rows = at[at["method"] == method]
        return float(rows["sapfdc"].mean()) if len(rows) else float("nan")

    fallback_rate = float((dec["source"] == "fallback").mean())
    distinct = int(dec["w"].round(6).nunique())
    return {
        "prompt_version": meta["prompt_versions"]["orchestrator"], "run_id": meta["run_id"],
        "git_commit": meta["git_commit"][:7], "builds": int(dec["build"].nunique()),
        "fallback_rate": fallback_rate, "distinct_w": distinct,
        "w_min": float(dec["w"].min()), "w_mean": float(dec["w"].mean()), "w_max": float(dec["w"].max()),
        "w_std": float(dec["w"].std(ddof=1)) if len(dec) > 1 else 0.0,
        "mean_confidence": float(dec["confidence"].mean()), "mean_tool_calls": float(dec["tool_calls"].mean()),
        "sapfdc_mean_10_agent": sapfdc("Agent-weighted"), "sapfdc_mean_10_llm_relevance": sapfdc("LLM-relevance"),
        "sapfdc_mean_10_dante": sapfdc("DANTE-CCH"),
        "rule_triggered": bool(fallback_rate > MAX_FALLBACK_RATE or distinct == 1),
    }


def summarise(run_dirs):
    return pd.DataFrame([summarise_run(d) for d in run_dirs], columns=COLUMNS)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Summarise orchestrator prompt iterations on the dev split.")
    ap.add_argument("--runs", nargs="+", required=True, help="dev run folders, oldest prompt first")
    ap.add_argument("--out", default="results/dev/orchestrator_prompt_iterations.csv")
    args = ap.parse_args(argv)
    df = summarise(args.runs)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, lineterminator="\n")
    print(df.to_string(index=False))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
