"""Phase 2 pipeline: runs any set of methods (MethodSpecs) on one build.

docs/PROJECT_CONTEXT.md §5 (formulas, methods, per-build flow, robustness) and
§9 (output files). Expensive work is shared: DANTE scores and the shortlist are
computed once per build, each relevance source at most once per build (and only
if a requested method needs it), and each orchestrator decision once per
relevance source per build, reused for every budget and every method with that
source.

Output files under <results_dir>/<run_id>/ (appended; created with a header):
    per_build.csv, llm_relevance.csv, orchestrator_decisions.csv,
    explanations.csv, runs/<build>.json (git-ignored), run_meta.json.
The column lists below are fixed; later issues read these files.
"""
import csv
import json
import logging
import os
import socket
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

from src.agent.fallback_router import FallbackRouter
from src.agent.orchestrator import ORCH_PROMPT_VERSION, make_input
from src.agent.semantic_analyzer import SemanticAnalyzer, make_request, prompt_version_from_config
from src.agent.shortlister import shortlist
from src.contracts import (DANTE_W, BuildState, CandidateTest, ChangedFile, DiffSummary, FinalRanking,
                           MethodSpec, validate)
from src.dante import rank, scores
from src.dante.scoring import score_table
from src.eval.metrics import all_metrics
from src.eval.stored import solution_metrics
from src.obs.trace import NullTrace
from src.settings import REPO_ROOT, repo_path
from src.tools.history_retrieval import HistoryRetrieval
from src.tools.registry import ToolRegistry

log = logging.getLogger(__name__)

METHODS_FILE = "experiments/methods.yaml"
STORED_METHOD = "DANTE-CCH (stored)"
# Columns of the DANTE score table that hold the target build's ground truth. They are
# used only for metrics (`failing`) and are removed from anything handed to a component
# (PROJECT_CONTEXT §6.3 rule 2).
OUTCOME_COLUMNS = ("actual_outcome",)
LLM_SOURCES = ("llm_shortlist", "llm_all_individual", "llm_single_call")
# weight modes that rank with an existing src.dante method instead of a weight
RANK_METHOD = {"random": "Random", "history_only": "History-only", "relevance_only": "TF-IDF-only"}
RANK_SOURCE = {"random": "random", "history_only": "history_only", "relevance_only": "tfidf_only"}

PER_BUILD_COLUMNS = [
    "run_id", "experiment", "split", "seed", "build", "budget", "method", "relevance_source", "weight_mode",
    "w", "ranking_source", "candidates", "failing", "selected", "found", "dtc", "sapfdc", "sds", "apfdc_full",
    "selected_duration_s", "total_duration_s", "time_saved_s", "llm_calls", "llm_cached_calls",
    "llm_latency_s", "prompt_tokens", "completion_tokens", "tool_calls", "decision_latency_s",
    "explainer_calls", "explainer_latency_s", "explainer_ok"]
LLM_RELEVANCE_COLUMNS = ["build", "relevance_source", "test", "relevance", "confidence", "reason",
                         "prompt_version", "fell_back"]
DECISION_COLUMNS = ["build", "relevance_source", "w", "confidence", "source", "steps", "llm_calls",
                    "tool_calls", "reason", "fallback_reason"]
EXPLANATION_COLUMNS = ["build", "budget", "method", "test", "rank_by_value", "ok", "error", "justification",
                       "cited_facts", "evidence", "latency_s", "prompt_tokens", "completion_tokens"]


# ------------------------------------------------------------------ setup ----

def load_method_specs(path=None, names=None) -> List[MethodSpec]:
    """All methods of the catalogue, or only `names` in the given order."""
    with open(repo_path(path or METHODS_FILE), "r", encoding="utf-8") as f:
        specs = [MethodSpec.from_dict(d) for d in yaml.safe_load(f)]
    if names is None:
        return specs
    by_name = {s.name: s for s in specs}
    unknown = [n for n in names if n not in by_name]
    if unknown:
        raise ValueError(f"unknown method(s) {unknown}; valid names: {', '.join(by_name)}")
    return [by_name[n] for n in names]


def load_tuned_weights(path) -> Dict[str, Any]:
    """experiments/tuned_weights.yaml as a dict ({} if the file does not exist yet)."""
    p = repo_path(path)
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@dataclass
class RunContext:
    run_id: str
    experiment: str
    split: str
    seed: int
    results_dir: Path
    trace: Any = field(default_factory=NullTrace)       # TraceLogger or NullTrace
    explainer_enabled: bool = False                     # seed in cfg["eval"]["explainer_seeds"]
    file_suffix: str = ""                               # ".shard0" etc.: one set of files per process

    @classmethod
    def create(cls, cfg, run_id, experiment, split, seed, results_dir, trace=None, file_suffix=""):
        return cls(run_id=run_id, experiment=experiment, split=split, seed=seed,
                   results_dir=Path(results_dir), trace=trace or NullTrace(),
                   explainer_enabled=seed in cfg["eval"]["explainer_seeds"], file_suffix=file_suffix)

    def file(self, stem, ext="csv"):
        """<run_dir>/<stem><file_suffix>.<ext>, e.g. per_build.shard0.csv."""
        return self.run_dir / f"{stem}{self.file_suffix}.{ext}"

    @property
    def run_dir(self):
        return self.results_dir / self.run_id


@dataclass
class Components:
    relevance_provider: Any = None              # LLM provider for the semantic analyzer
    orchestrator: Any = None                    # OrchestratorLike
    explainer: Any = None                       # ExplainerLike
    single_call: Any = None                     # SingleCallScorerLike
    tuned_weights: Dict[str, Any] = field(default_factory=dict)
    stored_loader: Optional[Callable] = None    # (cfg, build_name, budget, strategy) -> stored solution dict


def without_outcomes(df):
    """Copy of a score table without the target build's outcome columns."""
    return df.drop(columns=[c for c in OUTCOME_COLUMNS if c in df.columns])


# ------------------------------------------------------------ cost helpers ----

def _calls_since(provider, n0):
    calls = getattr(provider, "calls", None)
    return list(calls[n0:]) if calls is not None else []


def _n_calls(provider):
    calls = getattr(provider, "calls", None)
    return len(calls) if calls is not None else 0


def _cost(calls, n_calls=None):
    """Totals over LLMCallRecords; latency is the original one, cached or not."""
    return {"llm_calls": len(calls) if n_calls is None else n_calls,
            "llm_cached_calls": sum(1 for c in calls if getattr(c, "cached", False)),
            "llm_latency_s": sum(c.latency_s for c in calls),
            "prompt_tokens": sum(c.prompt_tokens or 0 for c in calls),
            "completion_tokens": sum(c.completion_tokens or 0 for c in calls),
            "tool_calls": 0, "tool_latency_s": 0.0}


def _add(a, b):
    return {k: a[k] + b[k] for k in a}


ZERO_COST = _cost([], 0)


# ------------------------------------------------------------ output files ----

def _append_csv(path, columns, rows):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="raise")
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c) for c in columns})


def diff_text_for_llm(build):
    """Changed hunks of the files DANTE keeps (code files), in path order."""
    return "\n".join(build.diff_files[p]["hunk_text"] for p in sorted(build.diff_files))


def stored_build_name(cfg, eval_row):
    """Name of the build's folder in DANTE's stored solutions."""
    name = getattr(eval_row, "build_name", None)
    if isinstance(name, str) and name:
        return name
    return (f"{cfg['project']}_build_{eval_row.pr_name}_{int(eval_row.build_id)}_{eval_row.stage_id}"
            "_tfidf_specific_boosted_False")


# ---------------------------------------------------------- relevance step ----

@dataclass
class RelevanceResult:
    source: str
    relevance: Dict[str, float]
    reasons: Dict[str, str]
    rows: List[dict]                  # llm_relevance.csv rows
    fallbacks: list
    fell_back: bool
    cost: Dict[str, float]


def _router_relevance(cfg, build, tests, df_tfidf, comps, ctx, source):
    provider = comps.relevance_provider
    if provider is None:
        raise ValueError(f"relevance source {source!r} needs a relevance_provider")
    llm = cfg["llm"]
    diff = diff_text_for_llm(build)
    version = prompt_version_from_config(cfg)
    reqs = [make_request(build.key, t, diff, build.source_texts.get(t, ""), llm["max_diff_chars"],
                         llm["max_test_chars"], prompt_version=version) for t in tests]
    dante_order = df_tfidf.sort_values(by="dante_cch_score", ascending=False).index.tolist()
    log_path = repo_path(cfg["paths"]["logs_dir"]) / "fallbacks.jsonl"
    router = FallbackRouter.from_config(SemanticAnalyzer(provider, trace=ctx.trace, run_id=ctx.run_id), cfg,
                                        log_path, trace=ctx.trace, run_id=ctx.run_id)
    n0 = _n_calls(provider)
    res = router.run(build.key, reqs, dante_order)
    rows = [{"build": build.key, "relevance_source": source, "test": r.test, "relevance": r.relevance,
             "confidence": r.confidence, "reason": r.reason, "prompt_version": version,
             "fell_back": res.fell_back} for r in res.responses]
    return RelevanceResult(source, dict(res.relevance), {r.test: r.reason for r in res.responses}, rows,
                           list(res.fallbacks), res.fell_back, _cost(_calls_since(provider, n0)))


def _single_call_relevance(build, df_tfidf, comps, ctx):
    scorer = comps.single_call
    if scorer is None:
        raise ValueError("relevance source 'llm_single_call' needs a single_call scorer")
    order = df_tfidf.sort_values(by="dante_cch_score", ascending=False).index.tolist()
    provider = getattr(scorer, "provider", None)
    n0 = _n_calls(provider)
    rel, fallbacks, n_calls = scorer.score(build.key, diff_text_for_llm(build), order, ctx.run_id)
    fell_back = not rel
    version = getattr(scorer, "prompt_version", "")
    rows = [{"build": build.key, "relevance_source": "llm_single_call", "test": t, "relevance": v,
             "confidence": None, "reason": None, "prompt_version": version, "fell_back": fell_back}
            for t, v in rel.items()]
    return RelevanceResult("llm_single_call", dict(rel), {}, rows, list(fallbacks), fell_back,
                           _cost(_calls_since(provider, n0), n_calls))


def compute_relevance(cfg, build, df_tfidf, short, comps, ctx, source):
    """One relevance source for one build."""
    if source == "none":
        return RelevanceResult(source, {t: 0.0 for t in df_tfidf.index}, {}, [], [], False, dict(ZERO_COST))
    if source == "tfidf":
        return RelevanceResult(source, df_tfidf["tfidf_relevance"].astype(float).to_dict(), {}, [], [], False,
                               dict(ZERO_COST))
    if source == "llm_shortlist":
        return _router_relevance(cfg, build, short, df_tfidf, comps, ctx, source)
    if source == "llm_all_individual":
        return _router_relevance(cfg, build, list(df_tfidf.index), df_tfidf, comps, ctx, source)
    if source == "llm_single_call":
        return _single_call_relevance(build, df_tfidf, comps, ctx)
    raise ValueError(f"unknown relevance source: {source}")


# ------------------------------------------------------------- the build ----

def _needs_relevance(spec):
    return spec.name != STORED_METHOD and spec.weight_mode not in RANK_METHOD


def run_build(cfg, loader, eval_row, specs, budgets, comps, ctx) -> dict:
    """Run every spec for one evaluation build and append its rows to the result files."""
    t0 = time.perf_counter()
    h, d = cfg["history"], cfg["dante"]
    row = loader.row(eval_row.pr_name, eval_row.build_id, eval_row.stage_id)
    build = loader.build(row, keep_sources=True)
    hist = loader.history(row, h["num_builds"], max(h["lookback_windows"]))
    bid = build.key
    ctx.trace.event(bid, "pipeline", "state", {"stage": "loaded", "n_candidates": len(build.candidates()),
                                                "n_history_builds": len(hist.frames)})

    # 1. DANTE scores once (DANTE weights; same order as w = 2/3)
    df_tfidf = scores(build, hist, cfg, "DANTE-CCH")
    if df_tfidf is None or df_tfidf.empty:
        raise ValueError(f"{bid}: no DANTE scores (no history model or no candidates)")
    ctx.trace.event(bid, "pipeline", "state", {"stage": "dante_scored", "n_candidates": len(df_tfidf)})
    failing = set(df_tfidf.index[df_tfidf["actual_outcome"] == 1])    # ground truth: metrics only
    durations = df_tfidf["duration"].to_dict()
    total_all = build.total_duration_all()

    # 2. shortlist once
    short = shortlist(df_tfidf["history_score"].to_dict(), df_tfidf["tfidf_relevance"].to_dict(),
                      cfg["shortlist"]["k"])
    ctx.trace.event(bid, "pipeline", "state", {"stage": "shortlisted", "shortlist": short})

    # 3. relevance sources, each at most once
    rel = {}
    for spec in specs:
        if _needs_relevance(spec) and spec.relevance_source not in rel:
            rel[spec.relevance_source] = compute_relevance(cfg, build, df_tfidf, short, comps, ctx,
                                                           spec.relevance_source)

    # 4. orchestrator decisions, once per relevance source
    decisions, decision_cost = {}, {}
    for spec in specs:
        src = spec.relevance_source
        if spec.weight_mode != "agent" or src in decisions or not _needs_relevance(spec):
            continue
        if rel[src].fell_back:
            decisions[src] = None        # ranking uses DANTE anyway; no decision needed
            decision_cost[src] = dict(ZERO_COST)
            continue
        if comps.orchestrator is None:
            raise ValueError(f"method {spec.name!r} needs an orchestrator")
        o_provider = getattr(comps.orchestrator, "provider", None)
        n0 = _n_calls(o_provider)
        llm_rel = rel[src].relevance if src in LLM_SOURCES else {}
        inp = make_input(build, hist, without_outcomes(df_tfidf), short, llm_rel, src, budgets)
        dec = comps.orchestrator.decide(inp, ToolRegistry.for_build(hist.frames, build.diff_files), ctx.run_id)
        validate(dec.to_dict(), "orchestrator_decision")
        decisions[src] = dec
        c = _cost(_calls_since(o_provider, n0), dec.llm_calls)
        c["tool_calls"] = len(dec.tool_calls)
        c["tool_latency_s"] = sum(t.latency_s for t in dec.tool_calls)
        decision_cost[src] = c

    # 5./6. per spec: weight, scores, selection per budget
    weighted = {}

    def weighted_df(src, w):
        key = (src, w)
        if key not in weighted:
            override = None
            if src != "tfidf":
                values = rel[src].relevance
                override = {t: float(values.get(t, 0.0)) for t in df_tfidf.index}
            weighted[key], _ = score_table(build, hist, h["lookback_windows"], h["min_sticky_events"],
                                           w_history=w, w_relevance=1 - w, power=d["relevance_power"],
                                           relevance_override=override)
        return weighted[key]

    history_tool = HistoryRetrieval.from_frames(hist.frames)
    rows, explanation_rows, methods = [], [], []
    for spec in specs:
        if spec.name == STORED_METHOD:
            if bool(getattr(eval_row, "in_phase1", False)) and comps.stored_loader is not None:
                for b in budgets:
                    m = solution_metrics(comps.stored_loader(cfg, stored_build_name(cfg, eval_row), b, "DANTE-CCH"))
                    methods.append({"method": spec.name, "budget": b, "ranking_source": "stored", "w": None,
                                    "metrics": m, "selected": None, "cost": dict(ZERO_COST)})
                    rows.append(_row(ctx, bid, b, spec, None, "stored", len(df_tfidf), len(failing), m,
                                     total_all, ZERO_COST, None))
            continue

        src = spec.relevance_source
        r = rel.get(src)
        cost = dict(r.cost) if r else dict(ZERO_COST)
        reasons = r.reasons if r else {}
        fallbacks = list(r.fallbacks) if r else []
        decision = None
        if spec.weight_mode in RANK_METHOD:
            rank_method, ranking_source, w, df_spec = RANK_METHOD[spec.weight_mode], \
                RANK_SOURCE[spec.weight_mode], None, df_tfidf
        elif r.fell_back:
            rank_method, ranking_source, w, df_spec = "DANTE-CCH", "dante_fallback", DANTE_W, df_tfidf
            if spec.weight_mode == "agent":
                cost = _add(cost, decision_cost[src])
        else:
            if spec.weight_mode == "fixed":
                w = float(spec.w)
            elif spec.weight_mode == "tuned":
                if spec.tuned_key not in comps.tuned_weights:
                    raise KeyError(f"no tuned weight for {spec.tuned_key!r} (experiments/tuned_weights.yaml)")
                w = float(comps.tuned_weights[spec.tuned_key]["w"])
            else:
                decision = decisions[src]
                w = float(decision.w)
                cost = _add(cost, decision_cost[src])
                if decision.fallback is not None:
                    fallbacks.append(decision.fallback)
            rank_method, df_spec = "DANTE-CCH", weighted_df(src, w)
            ranking_source = "llm" if src in LLM_SOURCES else "dante"

        for b in budgets:
            sel, order, _ = rank(build, hist, b, cfg, rank_method, df=df_spec)
            m = all_metrics(sel, durations, failing, full_order=order)
            score_col = "dante_cch_score" if rank_method in ("DANTE-CCH", "Random") else \
                {"History-only": "history_score", "TF-IDF-only": "tfidf_relevance"}[rank_method]
            ranking = FinalRanking(build_id=bid, method=spec.name, source=ranking_source, budget_fraction=b,
                                   ordered_tests=order, selected_tests=sel, total_duration=m["selected_duration"],
                                   scores={t: float(df_spec.at[t, score_col]) for t in order})
            validate(ranking.to_dict(), "final_ranking")
            budget_s = total_all * b
            if spec.name.startswith("Full system"):
                llm_values = r.relevance if (r and src in LLM_SOURCES and not r.fell_back) else {}
                state = BuildState(
                    build_id=bid, project=cfg["project"], budget_fraction=b, budget_seconds=budget_s,
                    diff_summary=DiffSummary([ChangedFile(p, v["added"], v["removed"])
                                              for p, v in build.diff_files.items()]),
                    candidates=[CandidateTest(name=t, duration=float(x.duration),
                                              history_score=float(x.history_score),
                                              tfidf_score=float(x.tfidf_relevance),
                                              llm_relevance=llm_values.get(t),
                                              final_score=float(df_spec.at[t, "dante_cch_score"]))
                                for t, x in df_tfidf.iterrows()],
                    selected_tests=sel, remaining_budget=budget_s - m["selected_duration"], fallbacks=fallbacks)
                validate(state.to_dict(), "build_state")
            ctx.trace.event(bid, "pipeline", "state", {"stage": "selected", "method": spec.name, "budget": b,
                                                        "selected": sel})
            expl = []
            if spec.explainer and ctx.explainer_enabled and comps.explainer is not None:
                expl = comps.explainer.explain(bid, b, without_outcomes(df_spec), sel, order, durations, budget_s,
                                               build.diff_files,
                                               reasons, history_tool, ctx.run_id)
                for e in expl:
                    validate(e.to_dict(), "explanation_record")
                    explanation_rows.append({
                        "build": bid, "budget": b, "method": spec.name, "test": e.test,
                        "rank_by_value": e.rank_by_value, "ok": e.ok, "error": e.error,
                        "justification": e.justification, "cited_facts": json.dumps(e.cited_facts),
                        "evidence": json.dumps(e.evidence, ensure_ascii=False), "latency_s": e.latency_s,
                        "prompt_tokens": e.prompt_tokens, "completion_tokens": e.completion_tokens})
            expl_cost = {"explainer_calls": len(expl), "explainer_latency_s": sum(e.latency_s for e in expl),
                         "explainer_ok": sum(1 for e in expl if e.ok)}
            methods.append({"method": spec.name, "budget": b, "ranking_source": ranking_source, "w": w,
                            "metrics": m, "selected": sel, "ordered": order, "cost": {**cost, **expl_cost}})
            rows.append(_row(ctx, bid, b, spec, w, ranking_source, len(df_tfidf), len(failing), m, total_all,
                             cost, expl_cost))

    result = {
        "run_id": ctx.run_id, "experiment": ctx.experiment, "split": ctx.split, "seed": ctx.seed,
        "build": bid, "commit": build.sha, "candidates": len(df_tfidf), "failing": len(failing),
        "changed_code_files": len(build.diff_files), "shortlist": short, "total_duration_s": total_all,
        "relevance": {s: {"relevance": r.relevance if s in LLM_SOURCES else {}, "reasons": r.reasons,
                          "fell_back": r.fell_back, "fallbacks": [f.to_dict() for f in r.fallbacks],
                          "cost": r.cost} for s, r in rel.items()},
        "decisions": {s: (dec.to_dict() if dec else None) for s, dec in decisions.items()},
        "methods": methods, "explanations": explanation_rows,
        "wall_time_s": round(time.perf_counter() - t0, 3),
    }
    _write_build_outputs(ctx, bid, result, rows, rel, decisions, explanation_rows)
    return result


def _row(ctx, bid, b, spec, w, ranking_source, n_cand, n_fail, m, total_all, cost, expl_cost):
    expl_cost = expl_cost or {"explainer_calls": 0, "explainer_latency_s": 0.0, "explainer_ok": 0}
    sel_dur = m.get("selected_duration") or 0.0
    return {"run_id": ctx.run_id, "experiment": ctx.experiment, "split": ctx.split, "seed": ctx.seed,
            "build": bid, "budget": b, "method": spec.name, "relevance_source": spec.relevance_source,
            "weight_mode": spec.weight_mode, "w": w, "ranking_source": ranking_source, "candidates": n_cand,
            "failing": n_fail, "selected": m.get("selected"), "found": m.get("found"), "dtc": m.get("dtc"),
            "sapfdc": m.get("sapfdc"), "sds": m.get("sds"), "apfdc_full": m.get("apfdc_full"),
            "selected_duration_s": sel_dur, "total_duration_s": total_all, "time_saved_s": total_all - sel_dur,
            "llm_calls": cost["llm_calls"], "llm_cached_calls": cost["llm_cached_calls"],
            "llm_latency_s": cost["llm_latency_s"], "prompt_tokens": cost["prompt_tokens"],
            "completion_tokens": cost["completion_tokens"], "tool_calls": cost["tool_calls"],
            "decision_latency_s": cost["llm_latency_s"] + cost["tool_latency_s"], **expl_cost}


def _write_build_outputs(ctx, bid, result, rows, rel, decisions, explanation_rows):
    """Called only after the whole build has finished, so a build that fails partway
    writes no rows. runs/<build>.json is written last, through a temporary file: it
    marks the build as complete (the runner's --skip-existing relies on it)."""
    d = ctx.run_dir
    _append_csv(ctx.file("per_build"), PER_BUILD_COLUMNS, rows)
    _append_csv(ctx.file("llm_relevance"), LLM_RELEVANCE_COLUMNS, [x for r in rel.values() for x in r.rows])
    _append_csv(ctx.file("orchestrator_decisions"), DECISION_COLUMNS, [
        {"build": bid, "relevance_source": s, "w": dec.w, "confidence": dec.confidence, "source": dec.source,
         "steps": dec.steps, "llm_calls": dec.llm_calls, "tool_calls": len(dec.tool_calls), "reason": dec.reason,
         "fallback_reason": dec.fallback.reason if dec.fallback else None}
        for s, dec in decisions.items() if dec is not None])
    _append_csv(ctx.file("explanations"), EXPLANATION_COLUMNS, explanation_rows)
    (d / "runs").mkdir(parents=True, exist_ok=True)
    tmp = d / "runs" / f"{bid}.json.tmp"
    tmp.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    os.replace(tmp, d / "runs" / f"{bid}.json")


# ---------------------------------------------------------------- the run ----

def git_commit():
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True,
                             timeout=10)
        sha = out.stdout.strip() if out.returncode == 0 else ""
        return sha or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def count_fallbacks(result):
    """Relevance and orchestrator fallbacks of one run_build result."""
    n = sum(len(r["fallbacks"]) for r in result["relevance"].values())
    return n + sum(1 for d in result["decisions"].values() if d and d.get("fallback"))


def run_builds(cfg, loader, eval_rows, specs, budgets, comps, ctx, config_file="config.yaml", host=None,
               progress=None, extra_meta=None):
    """Run every build; a build that raises is logged and recorded in failed_builds.
    progress(i, n, build, seconds, fallbacks, error) is called after each build.
    Writes run_meta<file_suffix>.json and returns it."""
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    eval_rows = list(eval_rows)
    failed = []
    n = 0
    for e in eval_rows:
        n += 1
        key = getattr(e, "key", None) or f"{e.pr_name}_build{e.build_id}"
        t0 = time.perf_counter()
        try:
            res = run_build(cfg, loader, e, specs, budgets, comps, ctx)
            if progress:
                progress(n, len(eval_rows), key, time.perf_counter() - t0, count_fallbacks(res), None)
        except Exception as ex:   # one bad build must not stop the run
            log.exception("build %s failed", key)
            failed.append({"build": key, "error": f"{type(ex).__name__}: {ex}"})
            if progress:
                progress(n, len(eval_rows), key, time.perf_counter() - t0, 0, failed[-1]["error"])
    model = getattr(comps.relevance_provider, "model", None) or cfg["llm"]["model"]
    meta = {
        "run_id": ctx.run_id, "experiment": ctx.experiment, "split": ctx.split, "seed": ctx.seed,
        "git_commit": git_commit(), "model": model,
        "prompt_versions": {"relevance": prompt_version_from_config(cfg), "orchestrator": ORCH_PROMPT_VERSION,
                            "explainer": getattr(comps.explainer, "prompt_version",
                                                 cfg["explainer"]["prompt_version"]),
                            "single_call": getattr(comps.single_call, "prompt_version",
                                                   cfg["single_call"].get("prompt_version"))},
        "methods": [s.name for s in specs], "budgets": list(budgets), "config_file": config_file,
        "started": started, "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_builds": n, "failed_builds": failed, "host": host or socket.gethostname(),
        **(extra_meta or {}),
    }
    ctx.run_dir.mkdir(parents=True, exist_ok=True)
    ctx.file("run_meta", "json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta
