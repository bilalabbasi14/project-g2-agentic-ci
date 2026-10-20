"""End-to-end run for one build (or the phase-1 subset).

    python run_end_to_end.py --build PR-1840_build4 --budget 10
    python run_end_to_end.py --subset --budget 5 10 20 [--skip-existing]
    python run_end_to_end.py --build PR-1287_build1 --budget 10 --provider mock

Steps per build: load build and history -> DANTE scores and ranking ->
shortlist top-K by history and by TF-IDF -> LLM relevance for the shortlist
(through the fallback router) -> LLM relevance replaces TF-IDF relevance in
the DANTE combination (shortlisted tests get the LLM value, the others 0) ->
greedy selection within each budget -> metrics against the true failures ->
comparison with stored DANTE-CCH and Random. The LLM is called once per build;
its relevance is reused for every budget.

Writes results/runs/<build>.json and logs/<build>.log.
"""
import argparse
import json
import logging
import sys
import time

import pandas as pd

from src.agent.fallback_router import FallbackRouter
from src.agent.llm_provider import MockProvider, make_provider
from src.agent.semantic_analyzer import SemanticAnalyzer, make_request
from src.agent.shortlister import shortlist
from src.contracts import BuildState, CandidateTest, ChangedFile, DiffSummary, FinalRanking, validate
from src.dante import rank, scores
from src.dante.compare_stored import load_stored
from src.data.loader import LRTSLoader
from src.data.sources import SourceRepo
from src.eval.compare_baselines import OUR_METHODS
from src.eval.metrics import all_metrics
from src.eval.stored import solution_metrics
from src.settings import load_config, repo_path

LLM_METHOD = "LLM-relevance"
log = logging.getLogger("e2e")


def diff_text_for_llm(build):
    """Changed hunks of the files DANTE keeps (code files), in path order."""
    return "\n".join(build.diff_files[p]["hunk_text"] for p in sorted(build.diff_files))


def llm_relevance(build, df, cfg, provider, log_path=None):
    """Shortlist, call the LLM through the fallback router; returns (RouterResult, shortlist)."""
    k = cfg["shortlist"]["k"]
    short = shortlist(df["history_score"].to_dict(), df["tfidf_relevance"].to_dict(), k)
    llm = cfg["llm"]
    diff = diff_text_for_llm(build)
    reqs = [make_request(build.key, t, diff, build.source_texts.get(t, ""),
                         llm["max_diff_chars"], llm["max_test_chars"]) for t in short]
    dante_order = df.sort_values(by="dante_cch_score", ascending=False).index.tolist()
    router = FallbackRouter.from_config(SemanticAnalyzer(provider), cfg, log_path)
    return router.run(build.key, reqs, dante_order), short


def run_build(cfg, loader, e, budgets, provider):
    """Run all methods for one evaluation build. Returns the result dict."""
    t0 = time.perf_counter()
    row = loader.row(e.pr_name, e.build_id, e.stage_id)
    h = cfg["history"]
    build = loader.build(row, keep_sources=True)
    hist = loader.history(row, h["num_builds"], max(h["lookback_windows"]))
    df_dante = scores(build, hist, cfg, "DANTE-CCH")
    df_shipped = scores(build, hist, cfg, "DANTE-CCH-shipped")
    n_calls_before = len(provider.calls)
    res, short = llm_relevance(build, df_dante, cfg, provider,
                               repo_path(cfg["paths"]["logs_dir"]) / "fallbacks.jsonl")
    calls = provider.calls[n_calls_before:]
    override = {t: res.relevance.get(t, 0.0) for t in df_dante.index}
    df_llm = scores(build, hist, cfg, "DANTE-CCH", relevance_override=override)
    failing = set(df_dante.index[df_dante["actual_outcome"] == 1])
    durations = df_dante["duration"].to_dict()

    per_budget = []
    for b in budgets:
        methods = {}
        for m in OUR_METHODS:
            df = df_shipped if m == "DANTE-CCH-shipped" else df_dante
            sel, order, _ = rank(build, hist, b, cfg, m, df=df)
            methods[m] = all_metrics(sel, durations, failing, full_order=order)
        if res.fell_back:
            sel, order, _ = rank(build, hist, b, cfg, "DANTE-CCH", df=df_dante)
            source = "dante_fallback"
        else:
            sel, order, _ = rank(build, hist, b, cfg, "DANTE-CCH", df=df_llm)
            source = "llm"
        methods[LLM_METHOD] = all_metrics(sel, durations, failing, full_order=order)
        ranking = FinalRanking(build_id=build.key, method=LLM_METHOD, source=source, budget_fraction=b,
                               ordered_tests=order, selected_tests=sel,
                               total_duration=sum(durations[t] for t in sel),
                               scores={t: float(df_llm.loc[t, "dante_cch_score"]) for t in order})
        validate(ranking.to_dict(), "final_ranking")
        for strat in ("DANTE-CCH", "Random"):
            methods[f"{strat} (stored)"] = solution_metrics(load_stored(cfg, e.build_name, b, strat))
        budget_s = build.total_duration_all() * b
        state = BuildState(
            build_id=build.key, project=cfg["project"], budget_fraction=b, budget_seconds=budget_s,
            diff_summary=DiffSummary([ChangedFile(p, v["added"], v["removed"]) for p, v in build.diff_files.items()]),
            candidates=[CandidateTest(name=t, duration=float(r.duration), history_score=float(r.history_score),
                                      tfidf_score=float(r.tfidf_relevance),
                                      llm_relevance=res.relevance.get(t),
                                      final_score=float(df_llm.loc[t, "dante_cch_score"]))
                        for t, r in df_dante.iterrows()],
            selected_tests=sel, remaining_budget=budget_s - ranking.total_duration, fallbacks=res.fallbacks)
        validate(state.to_dict(), "build_state")
        per_budget.append({"budget": b, "methods": methods, "llm_source": source,
                           "llm_selected": sel, "remaining_budget": state.remaining_budget})

    ok_calls = [c for c in calls if c.ok]
    return {
        "build": build.key, "build_name": e.build_name, "commit": build.sha,
        "candidates": len(df_dante), "total_failures": len(failing),
        "changed_code_files": len(build.diff_files),
        "shortlist": short, "llm_relevance": res.relevance,
        "llm_reasons": {r.test: r.reason for r in res.responses},
        "llm_source": "dante_fallback" if res.fell_back else "llm",
        "fallbacks": [f.to_dict() for f in res.fallbacks],
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
