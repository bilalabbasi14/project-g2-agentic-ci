"""End-to-end run for one build (or the phase-1 subset): Phase 1 command line,
now a thin wrapper around src/pipeline.py.

    python run_end_to_end.py --build PR-1840_build4 --budget 10
    python run_end_to_end.py --subset --budget 5 10 20 [--skip-existing]
    python run_end_to_end.py --build PR-1287_build1 --budget 10 --provider mock

Runs the Phase 1 methods (Random, History-only, TF-IDF-only, DANTE-CCH-shipped,
DANTE-CCH, LLM-relevance, DANTE-CCH (stored)) through src.pipeline.run_build and
converts the result to the Phase 1 JSON format (plus Random (stored)), so
src/eval/summarize.py keeps working. The LLM is called once per build; its
relevance is reused for every budget.

Writes results/runs/<build>.json and logs/<build>.log; the pipeline's own
result files go to logs/e2e/ (git-ignored).
"""
import argparse
import json
import logging
import sys
import time

import pandas as pd

from src.agent.llm_provider import MockProvider, make_provider
from src.dante.compare_stored import load_stored
from src.data.loader import LRTSLoader
from src.data.sources import SourceRepo
from src.eval.stored import solution_metrics
from src.pipeline import Components, RunContext, load_method_specs, run_build as pipeline_run_build
from src.settings import load_config, repo_path

LLM_METHOD = "LLM-relevance"
PHASE1_METHODS = ["Random", "History-only", "TF-IDF-only", "DANTE-CCH-shipped", "DANTE-CCH", LLM_METHOD,
                  "DANTE-CCH (stored)"]
E2E_RUN_ID = "phase1_e2e"
log = logging.getLogger("e2e")


def _stored(cfg, build_name, budget, strategy):
    # looked up at call time so tests can replace load_stored
    return load_stored(cfg, build_name, budget, strategy)


class _Phase1Row:
    """Evaluation row as the pipeline expects it; every Phase 1 build is a Phase 1 build."""

    def __init__(self, e):
        self.pr_name, self.build_id, self.stage_id = e.pr_name, e.build_id, e.stage_id
        self.build_name = e.build_name
        self.key = getattr(e, "key", None)
        self.in_phase1 = True


def run_build(cfg, loader, e, budgets, provider):
    """Run all Phase 1 methods for one evaluation build. Returns the Phase 1 result dict."""
    t0 = time.perf_counter()
    specs = load_method_specs(names=PHASE1_METHODS)
    ctx = RunContext.create(cfg, E2E_RUN_ID, "phase1", "phase1", cfg["llm_p2"]["seed"],
                            repo_path(cfg["paths"]["logs_dir"]) / "e2e")
    comps = Components(relevance_provider=provider, stored_loader=_stored)
    n0 = len(provider.calls)
    res = pipeline_run_build(cfg, loader, _Phase1Row(e), specs, budgets, comps, ctx)
    calls = provider.calls[n0:]
    llm = res["relevance"]["llm_shortlist"]

    per_budget = []
    for b in budgets:
        rows = {m["method"]: m for m in res["methods"] if m["budget"] == b}
        methods = {name: rows[name]["metrics"] for name in PHASE1_METHODS if name in rows}
        methods["Random (stored)"] = solution_metrics(_stored(cfg, e.build_name, b, "Random"))
        lr = rows[LLM_METHOD]
        per_budget.append({"budget": b, "methods": methods, "llm_source": lr["ranking_source"],
                           "llm_selected": lr["selected"],
                           "remaining_budget": res["total_duration_s"] * b - lr["metrics"]["selected_duration"]})

    ok_calls = [c for c in calls if c.ok]
    return {
        "build": res["build"], "build_name": e.build_name, "commit": res["commit"],
        "candidates": res["candidates"], "total_failures": res["failing"],
        "changed_code_files": res["changed_code_files"],
        "shortlist": res["shortlist"], "llm_relevance": llm["relevance"],
        "llm_reasons": llm["reasons"],
        "llm_source": "dante_fallback" if llm["fell_back"] else "llm",
        "fallbacks": llm["fallbacks"],
        "llm": {"model": provider.model, "calls": len(calls), "failed_calls": len(calls) - len(ok_calls),
                "mean_latency_s": sum(c.latency_s for c in calls) / len(calls) if calls else None,
                "prompt_tokens": sum(c.prompt_tokens or 0 for c in calls),
                "completion_tokens": sum(c.completion_tokens or 0 for c in calls)},
        "budgets": per_budget,
        "wall_time_s": round(time.perf_counter() - t0, 1),
    }


def mock_provider():
    """Deterministic stand-in: relevance 0.5 for every test, echoing the test name."""
    def answer(prompt):
        test = prompt.split("Test class `", 1)[1].split("`", 1)[0]
        return json.dumps({"test": test, "relevance": 0.5, "reason": "mock", "confidence": 1.0})
    return MockProvider([answer])


def print_summary(result):
    rows = []
    for pb in result["budgets"]:
        for m, v in pb["methods"].items():
            rows.append({"budget": f"{int(round(pb['budget'] * 100))}%", "method": m, "dtc": v["dtc"],
                         "sapfdc": v["sapfdc"], "sds": v["sds"], "found": v["found"], "selected": v["selected"]})
    t = pd.DataFrame(rows)
    print(f"\n{result['build']}: candidates={result['candidates']} failures={result['total_failures']} "
          f"code files={result['changed_code_files']} shortlist={len(result['shortlist'])} "
          f"llm={result['llm_source']} calls={result['llm']['calls']} "
          f"mean latency={result['llm']['mean_latency_s'] or 0:.1f}s fallbacks={len(result['fallbacks'])}")
    print(t.to_string(index=False, float_format=lambda x: f"{x:.3f}"))


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", help="build key, e.g. PR-1840_build4")
    g.add_argument("--subset", action="store_true", help="all phase-1 subset builds")
    ap.add_argument("--budget", type=float, nargs="+", default=[10], help="percent, e.g. 5 10 20")
    ap.add_argument("--provider", choices=["ollama", "mock"], default="ollama")
    ap.add_argument("--skip-existing", action="store_true", help="skip builds that already have a result JSON")
    args = ap.parse_args()

    cfg = load_config()
    p = cfg["paths"]
    logs = repo_path(p["logs_dir"])
    runs = repo_path(p["results_dir"]) / "runs"
    logs.mkdir(parents=True, exist_ok=True)
    runs.mkdir(parents=True, exist_ok=True)
    loader = LRTSLoader(p["lrts_root"], cfg["project"], SourceRepo(p["repo_clone"], p["repo_url"]))
    ev = pd.read_csv(repo_path(p["eval_builds"]))
    targets = ev[ev["phase1_subset"] == 1] if args.subset else ev[ev["key"] == args.build]
    if targets.empty:
        sys.exit(f"build {args.build} is not an evaluation build (see {p['eval_builds']})")
    budgets = [b / 100 for b in args.budget]
    provider = mock_provider() if args.provider == "mock" else make_provider(cfg)

    suffix = "" if args.provider == "ollama" else f"_{args.provider}"
    for e in targets.itertuples():
        out = runs / f"{e.key}{suffix}.json"
        if args.skip_existing and out.exists():
            print(f"skip {e.key} (exists)")
            continue
        handler = logging.FileHandler(logs / f"{e.key}.log", mode="w", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        root.addHandler(handler)
        try:
            result = run_build(cfg, loader, e, budgets, provider)
            result["provider"] = args.provider
            out.write_text(json.dumps(result, indent=2))
            print_summary(result)
            print(f"-> {out}\n-> {logs / (e.key + '.log')}")
        finally:
            root.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    main()
