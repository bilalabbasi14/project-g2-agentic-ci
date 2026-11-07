"""Failure analysis of the final system on one run (P2-14).

    python -m src.eval.failure_analysis --run-dir results/E3_test_seed1 --runs-json <folder of run JSONs>
        --traces <trace folder> --ratings results/gap2/ratings_final.csv
        [--causes results/analysis/failure_causes.yaml] [--out results/analysis] [--cases docs/cases]
        [--sample-dir logs_sample]

Every `Full system` build-budget pair of the run (5/10/20%) gets zero or more of
the categories below; each is decided by one pure function of this module:

    F1 Fallback, F2 Missed - outside shortlist, F3 Missed - low LLM relevance,
    F4 Missed - did not fit the budget, F5 Agent weight harmful,
    F6 Unsound explanation, F7 Possible memorisation, S Success.

A category that belongs to the whole build (F1, and F7 found in a relevance or
orchestrator reason) is given to all three budgets of that build.

Outputs:
- <out>/failure_categories.csv (build, budget, category, detail);
- <out>/failure_summary.md: count and share of build-budget pairs per category. The
  "likely cause and how it could be addressed" column is read from the --causes YAML
  file, which Bilal writes by hand; this module never generates that text;
- four cases in <cases>/ (success_1/2, failure_1/2) with the facts of the pair and
  its trajectory; the traces of those builds are exported to <sample-dir>/<run_id>/
  with src.obs.export_sample.

The failing tests of each build are read from the LRTS data (config paths) only as
ground truth for this analysis, never as input to a model. The run JSONs and the
full traces are not committed (downloaded from Kaggle, P2-21).
"""
import argparse
import csv
import json
import logging
import math
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set

import pandas as pd
import yaml

from src.agent.explainer import build_prompt as explainer_prompt
from src.settings import load_config, repo_path

log = logging.getLogger(__name__)

METHOD = "Full system"
DANTE = "DANTE-CCH"
AGENT = "Agent-weighted"
LOW_RELEVANCE = 0.2          # F3: "LLM relevance < 0.2" (P2-14)
TOP_BY_VALUE = 10            # F4: "in the top 10 by value" (P2-14)
CASE_BUDGET = 0.10           # success cases are chosen at the 10% budget (P2-14)
EPS = 1e-12                  # float tolerance when comparing %DTC values

CSV_COLUMNS = ["build", "budget", "category", "detail"]
CATEGORIES = {
    "F1": "Fallback: the relevance router used the DANTE ranking, or the orchestrator fell back",
    "F2": "Missed - outside shortlist: a failing candidate was not selected and not on the shortlist",
    "F3": "Missed - low LLM relevance: a failing candidate was not selected, was on the shortlist "
          f"and got LLM relevance < {LOW_RELEVANCE}",
    "F4": f"Missed - did not fit the budget: a failing candidate in the top {TOP_BY_VALUE} by value "
          "was not selected",
    "F5": f"Agent weight harmful: {AGENT} %DTC lower than {DANTE} %DTC",
    "F6": "Unsound explanation: an explanation of the pair was rated unsound",
    "F7": "Possible memorisation: an LLM reason or justification names an identifier absent from its prompt",
    "S": f"Success: a failing test caught that {DANTE} missed at the same budget",
}
FAILURE_CATEGORIES = [c for c in CATEGORIES if c.startswith("F")]
NOT_WRITTEN = "*(to be written by Bilal)*"

JIRA_KEY = re.compile(r"KARAF-\d+")
CAMEL_CASE = re.compile(r"\b[A-Z][a-z]+(?:[A-Z][a-z0-9]+)+\b")


# ------------------------------------------------------------ categories ----

def f1_fallback(relevance_fell_back: bool, decision: Optional[dict]) -> Optional[str]:
    """F1: the build fell back to DANTE (relevance router) or the orchestrator fell back.

    `decision` is the orchestrator record of the run JSON (source "agent" when the
    agent's own answer was used). Returns a short detail, or None."""
    parts = []
    if relevance_fell_back:
        parts.append("relevance fell back to the DANTE ranking")
    if decision is not None and (decision.get("fallback") or decision.get("source") != "agent"):
        fb = decision.get("fallback")
        reason = fb.get("reason") if isinstance(fb, dict) else fb
        parts.append(f"orchestrator fell back ({reason or decision.get('source')}), w = {decision.get('w')}")
    return "; ".join(parts) or None


def missed(failing: Iterable[str], selected: Iterable[str]) -> Set[str]:
    """Failing candidates that the selection did not include."""
    return set(failing) - set(selected)


def f2_outside_shortlist(failing: Iterable[str], selected: Iterable[str], shortlist: Iterable[str]) -> List[str]:
    """F2: failing candidates that were not selected and not on the shortlist
    (so the LLM never scored them)."""
    short = set(shortlist)
    return sorted(t for t in missed(failing, selected) if t not in short)


def f3_low_llm_relevance(failing: Iterable[str], selected: Iterable[str], shortlist: Iterable[str],
                         llm_relevance: Dict[str, float], threshold: float = LOW_RELEVANCE) -> List[str]:
    """F3: failing candidates that were not selected, were on the shortlist and got
    LLM relevance < threshold (a shortlisted test without a value counts as 0)."""
    short = set(shortlist)
    return sorted(t for t in missed(failing, selected)
                  if t in short and float(llm_relevance.get(t, 0.0)) < threshold)


def f4_did_not_fit(failing: Iterable[str], selected: Iterable[str], ordered: Sequence[str],
                   top_n: int = TOP_BY_VALUE) -> List[str]:
    """F4: failing candidates in the top `top_n` of the value ordering that were not
    selected: the greedy selection skipped them because they did not fit the
    remaining budget."""
    fail, sel = set(failing), set(selected)
    return [t for t in ordered[:top_n] if t in fail and t not in sel]


def f5_agent_weight_harmful(dtc_agent: float, dtc_dante: float) -> bool:
    """F5: the agent's per-build weight gave a lower %DTC than DANTE's fixed weight."""
    return dtc_agent < dtc_dante - EPS


def f6_unsound_explanations(rated: Iterable[dict], build: str, budget: float) -> List[str]:
    """F6: tests of this build and budget whose explanation was rated unsound.

    `rated` holds dicts with build, budget, test and final_rating (the rating items
    joined with ratings_final.csv)."""
    return sorted(r["test"] for r in rated
                  if r["build"] == build and math.isclose(float(r["budget"]), float(budget))
                  and str(r["final_rating"]).strip().lower() == "unsound")


def unsupported_identifiers(text: str, prompt: str) -> List[str]:
    """F7: identifiers in an LLM text (a JIRA key KARAF-<n>, or a CamelCase name)
    that do not occur anywhere in the prompt the model was given."""
    found = set(JIRA_KEY.findall(text or "")) | set(CAMEL_CASE.findall(text or ""))
    return sorted(i for i in found if i not in (prompt or ""))


def s_caught_extra(failing: Iterable[str], selected_full: Iterable[str], selected_dante: Iterable[str]) -> List[str]:
    """S: failing tests that the full system selected and DANTE-CCH did not."""
    return sorted(set(failing) & set(selected_full) - set(selected_dante))


# ---------------------------------------------------------------- inputs ----

def _bkey(budget) -> float:
    return round(float(budget), 4)


def load_run_json(runs_json: Path, build: str) -> dict:
    with open(Path(runs_json) / f"{build}.json", encoding="utf-8") as f:
        return json.load(f)


def method_entry(run: dict, method: str, budget: float) -> dict:
    """The run JSON's record of one method at one budget."""
    for m in run["methods"]:
        if m["method"] == method and math.isclose(float(m["budget"]), float(budget)):
            return m
    raise KeyError(f"{run['build']}: no {method} at budget {budget}")


def trace_dir_for(traces: Path, run_id: str) -> Path:
    """Accepts either the run's own trace folder or its parent (<traces>/<run_id>/)."""
    traces = Path(traces)
    return traces / run_id if (traces / run_id).is_dir() else traces


def read_trace(trace_dir: Path, build: str) -> List[dict]:
    path = Path(trace_dir) / f"{build}.jsonl"
    if not path.exists():
        log.warning("no trace for %s (%s); F7 is not checked for its relevance and orchestrator reasons",
                    build, path)
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prompts_by_component(events: Iterable[dict]) -> Dict[str, Dict[Optional[str], str]]:
    """{component: {test or None: all prompts of its llm_call events, joined}}."""
    out: Dict[str, Dict[Optional[str], List[str]]] = {}
    for ev in events:
        if ev.get("event") != "llm_call":
            continue
        p = ev.get("payload") or {}
        out.setdefault(ev.get("component"), {}).setdefault(p.get("test"), []).append(p.get("prompt") or "")
    return {c: {t: "\n".join(ps) for t, ps in d.items()} for c, d in out.items()}


def read_ratings(ratings: Path) -> List[dict]:
    """ratings_final.csv joined with rating_items.csv (same folder) on item_id."""
    ratings = Path(ratings)
    items = {r["item_id"]: r for r in csv.DictReader(open(ratings.parent / "rating_items.csv", encoding="utf-8",
                                                           newline=""))}
    out = []
    for r in csv.DictReader(open(ratings, encoding="utf-8", newline="")):
        it = items[r["item_id"]]
        out.append({"item_id": r["item_id"], "build": it["build"], "budget": float(it["budget"]),
                    "test": it["test"], "final_rating": r["final_rating"]})
    return out


def failing_candidates(cfg: dict, builds: Iterable[str], candidates: Dict[str, Sequence[str]]) -> Dict[str, Set[str]]:
    """Failing candidates per build from the LRTS test results (ground truth only)."""
    from src.data.loader import LRTSLoader
    ev = pd.read_csv(repo_path(cfg["eval"]["eval_set"])).set_index("key")
    loader = LRTSLoader(cfg["paths"]["lrts_root"], cfg["project"])
    out = {}
    for b in builds:
        r = ev.loc[b]
        df = loader.test_class_df(loader.row(r["pr_name"], r["build_id"], r["stage_id"]))
        if df is None:
            raise FileNotFoundError(f"no LRTS test results for {b}")
        out[b] = set(df.loc[df["outcome"] == 1, "testclass"].dropna()) & set(candidates[b])
    return out


# -------------------------------------------------------------- analysis ----

def analyse(run_dir: Path, runs_json: Path, traces: Path, ratings: Path, failing: Dict[str, Set[str]],
            max_justification_chars: int) -> List[dict]:
    """Rows (build, budget, category, detail) for every Full system build-budget pair."""
    run_dir = Path(run_dir)
    pb = pd.read_csv(run_dir / "per_build.csv")
    dtc = {(r.build, r.method, _bkey(r.budget)): float(r.dtc) for r in pb.itertuples()}
    pairs = sorted({(r.build, _bkey(r.budget)) for r in pb[pb["method"] == METHOD].itertuples()})
    budgets = sorted({b for _, b in pairs})
    tdir = trace_dir_for(traces, run_dir.name)
    rated = read_ratings(ratings)
    expl = pd.read_csv(run_dir / "explanations.csv", dtype={"ok": str}) if (run_dir / "explanations.csv").exists() \
        else pd.DataFrame(columns=["build", "budget", "method", "test", "ok", "justification", "evidence"])
    expl = expl[(expl["method"] == METHOD) & (expl["ok"].astype(str).str.lower() == "true")]

    rows = []
    for build in sorted({b for b, _ in pairs}):
        run = load_run_json(runs_json, build)
        rel = run["relevance"].get("llm_shortlist") or {}
        decision = (run.get("decisions") or {}).get("llm_shortlist")
        fail = failing[build]
        if len(fail) != int(run["failing"]):
            raise ValueError(f"{build}: {len(fail)} failing candidates from LRTS, run JSON says {run['failing']}")
        prompts = prompts_by_component(read_trace(tdir, build))

        per_build_f7 = []
        rel_prompts = prompts.get("semantic_analyzer", {})
        for test, reason in sorted((rel.get("reasons") or {}).items()):
            if test in rel_prompts:
                ids = unsupported_identifiers(reason, rel_prompts[test])
                if ids:
                    per_build_f7.append(f"relevance reason for {test}: {', '.join(ids)}")
        orch_prompt = "\n".join(prompts.get("orchestrator", {}).values())
        if decision and decision.get("source") == "agent" and orch_prompt:
            ids = unsupported_identifiers(decision.get("reason") or "", orch_prompt)
            if ids:
                per_build_f7.append(f"orchestrator reason: {', '.join(ids)}")
        f1 = f1_fallback(bool(rel.get("fell_back")), decision)

        for budget in budgets:
            full = method_entry(run, METHOD, budget)
            dante = method_entry(run, DANTE, budget)
            found = {
                "F1": f1,
                "F2": f2_outside_shortlist(fail, full["selected"], run["shortlist"]),
                "F3": f3_low_llm_relevance(fail, full["selected"], run["shortlist"], rel.get("relevance") or {}),
                "F4": f4_did_not_fit(fail, full["selected"], full["ordered"]),
                "F5": f5_agent_weight_harmful(dtc[(build, AGENT, budget)], dtc[(build, DANTE, budget)]),
                "F6": f6_unsound_explanations(rated, build, budget),
                "S": s_caught_extra(fail, full["selected"], dante["selected"]),
            }
            f7 = list(per_build_f7)
            for e in expl[(expl["build"] == build) & (expl["budget"].map(_bkey) == budget)].itertuples():
                prompt = explainer_prompt(json.loads(e.evidence), max_justification_chars)
                ids = unsupported_identifiers(e.justification, prompt)
                if ids:
                    f7.append(f"justification for {e.test}: {', '.join(ids)}")
            found["F7"] = f7
            for cat in CATEGORIES:
                value = found[cat]
                if not value:
                    continue
                if cat == "F5":
                    detail = f"{AGENT} %DTC {dtc[(build, AGENT, budget)]:.3f} < {DANTE} {dtc[(build, DANTE, budget)]:.3f}"
                elif cat in ("F1",):
                    detail = value
                elif cat == "F7":
                    detail = " | ".join(value)
                else:
                    detail = "; ".join(value)
                rows.append({"build": build, "budget": budget, "category": cat, "detail": detail})
    return rows


def _budget_column(budget: float) -> str:
    return f"pairs_{round(float(budget) * 100)}pct"


def summarise(rows: List[dict], n_pairs: int, budgets: Sequence[float]) -> pd.DataFrame:
    """Count and share of build-budget pairs per category, overall and per budget
    (columns category, pairs, share, pairs_<b>pct)."""
    df = pd.DataFrame(rows, columns=CSV_COLUMNS)
    out = []
    for cat in CATEGORIES:
        sub = df[df["category"] == cat]
        rec = {"category": cat, "pairs": len(sub), "share": len(sub) / n_pairs if n_pairs else 0.0}
        for b in budgets:
            rec[_budget_column(b)] = int((sub["budget"].map(_bkey) == _bkey(b)).sum())
        out.append(rec)
    return pd.DataFrame(out)


def read_causes(path: Optional[Path]) -> Dict[str, str]:
    """{category: hand-written likely-cause text}; empty entries count as not written."""
    if not path or not Path(path).exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {str(k): " ".join(str(v).split()) for k, v in data.items() if v and str(v).strip()}


def summary_markdown(summary: pd.DataFrame, causes: Dict[str, str], run_id: str, n_builds: int,
                     budgets: Sequence[float], command: str) -> str:
    head = [f"# Failure analysis of `{METHOD}`, run `{run_id}`", "",
            f"Generated by `{command}`. Every number comes from `failure_categories.csv`; the last column is "
            "written by hand by Bilal in `failure_causes.yaml` (not generated).", "",
            f"Build-budget pairs analysed: {n_builds} builds × {len(budgets)} budgets = {n_builds * len(budgets)}. "
            "A pair can have several categories.", "",
            "| Category | Meaning | Pairs | Share | " + " | ".join(f"{b:.0%}" for b in budgets)
            + " | Likely cause and how it could be addressed |",
            "|---|---|---|---|" + "---|" * len(budgets) + "---|"]
    for rec in summary.to_dict("records"):
        per = " | ".join(str(rec[_budget_column(b)]) for b in budgets)
        head.append(f"| {rec['category']} | {CATEGORIES[rec['category']]} | {rec['pairs']} | {rec['share']:.3f} | "
                    f"{per} | {causes.get(rec['category'], NOT_WRITTEN)} |")
    return "\n".join(head) + "\n"


# ----------------------------------------------------------------- cases ----

def choose_cases(rows: List[dict], pb: pd.DataFrame, summary: pd.DataFrame) -> List[dict]:
    """success_1/2: the two 10% pairs with the largest %DTC gain of Full system over
    DANTE-CCH (ties by build key); failure_1/2: the first pair (by build key, then
    budget) of each of the two most frequent F-categories (ties by category id)."""
    at = pb[pb["budget"].map(_bkey) == _bkey(CASE_BUDGET)]
    full = at[at["method"] == METHOD].set_index("build")["dtc"]
    dante = at[at["method"] == DANTE].set_index("build")["dtc"]
    gain = (full - dante).rename("gain").reset_index().sort_values(["gain", "build"], ascending=[False, True])
    cases = [{"name": f"success_{i + 1}", "build": r.build, "budget": _bkey(CASE_BUDGET), "category": "S",
              "why": f"rank {i + 1} by %DTC gain of {METHOD} over {DANTE} at {CASE_BUDGET:.0%} "
                     f"(gain {r.gain:+.3f}; ties by build key)"}
             for i, r in enumerate(gain.head(2).itertuples())]
    freq = summary[summary["category"].isin(FAILURE_CATEGORIES) & (summary["pairs"] > 0)].copy()
    freq["order"] = freq["category"].map(FAILURE_CATEGORIES.index)
    freq = freq.sort_values(["pairs", "order"], ascending=[False, True]).head(2)
    for i, r in enumerate(freq.itertuples()):
        first = sorted((x["build"], x["budget"]) for x in rows if x["category"] == r.category)[0]
        cases.append({"name": f"failure_{i + 1}", "build": first[0], "budget": first[1], "category": r.category,
                      "why": f"first pair (by build key, then budget) of {r.category}, the "
                             f"{'most' if i == 0 else 'second most'} frequent failure category ({r.pairs} pairs)"})
    return cases


def _fmt(x, digits=3):
    return f"{x:.{digits}f}" if isinstance(x, float) else str(x)


def case_markdown(case: dict, run: dict, pb: pd.DataFrame, rows: List[dict], fail: Set[str],
                  events: List[dict], run_id: str, sample_rel: str) -> str:
    """Facts of one build-budget pair and its trajectory (no interpretation)."""
    b, budget = case["build"], case["budget"]
    full, dante = method_entry(run, METHOD, budget), method_entry(run, DANTE, budget)
    rel = run["relevance"].get("llm_shortlist") or {}
    decision = (run.get("decisions") or {}).get("llm_shortlist") or {}
    at = pb[(pb["build"] == b) & (pb["budget"].map(_bkey) == _bkey(budget))].set_index("method")
    title = "Success" if case["name"].startswith("success") else f"Failure ({case['category']})"
    lines = [f"# {title} case: `{b}` at the {budget:.0%} budget", "",
             f"- **Run:** `{run_id}` · **method:** `{METHOD}` compared with `{DANTE}`",
             f"- **Why this case:** {case['why']}",
             f"- **Categories of this pair:** "
             + (", ".join(f"{x['category']} ({x['detail']})" for x in rows
                          if x["build"] == b and _bkey(x["budget"]) == _bkey(budget)) or "none"),
             "", "## What happened", "",
             f"- Candidates: {run['candidates']}; failing candidates: {len(fail)}; shortlist size: {len(run['shortlist'])}.",
             f"- Orchestrator: w = {decision.get('w')}, confidence {decision.get('confidence')}, source "
             f"`{decision.get('source')}`, reason: \"{decision.get('reason')}\".",
             "", "| Metric | Full system | DANTE-CCH |", "|---|---|---|"]
    for col, label in (("dtc", "%DTC"), ("sapfdc", "SAPFDc"), ("apfdc_full", "APFDc (full order)"),
                       ("selected", "Selected tests"), ("found", "Failing tests found"),
                       ("selected_duration_s", "Selected duration (s)")):
        lines.append(f"| {label} | {_fmt(at.loc[METHOD, col])} | {_fmt(at.loc[DANTE, col])} |")
    lines += ["", "Failing candidates:", "",
              "| Test | Selected by Full system | Selected by DANTE-CCH | On shortlist | LLM relevance | "
              "Rank by value (Full system) |", "|---|---|---|---|---|---|"]
    order = {t: i + 1 for i, t in enumerate(full["ordered"])}
    for t in sorted(fail):
        r = (rel.get("relevance") or {}).get(t)
        lines.append(f"| `{t}` | {'yes' if t in full['selected'] else 'no'} | {'yes' if t in dante['selected'] else 'no'} "
                     f"| {'yes' if t in run['shortlist'] else 'no'} | {'-' if r is None else _fmt(float(r), 2)} "
                     f"| {order.get(t, '-')} |")
    reasons = {t: x for t, x in (rel.get("reasons") or {}).items() if t in fail}
    if reasons:
        lines += ["", "LLM relevance reasons for the failing candidates:", ""]
        lines += [f"- `{t}`: \"{x}\"" for t, x in sorted(reasons.items())]
    lines += ["", "## Trajectory", "",
              f"Full trace: [{sample_rel}/{b}.md](../../{sample_rel}/{b}.md) (raw events: `{sample_rel}/{b}.jsonl`), "
              "exported with `src.obs.export_sample`.", "",
              "| Step | Component | Event | Summary |", "|---|---|---|---|"]
    for ev in sorted(events, key=lambda e: e["step"]):
        lines.append(f"| {ev['step']} | {ev.get('component')} | {ev.get('event')} | {event_summary(ev)} |")
    return "\n".join(lines) + "\n"


def event_summary(ev: dict) -> str:
    """One short line per trace event for the case files' trajectory table."""
    p = ev.get("payload") or {}
    kind = (ev.get("component"), ev.get("event"))
    if ev.get("event") == "state":
        parts = [str(p.get("stage", ""))]
        if "method" in p:
            parts.append(f"{p['method']} at {float(p['budget']):.0%}")
        for key, label in (("selected", "selected"), ("shortlist", "shortlisted")):
            if key in p:
                parts.append(f"{len(p[key])} {label}")
        if "n_candidates" in p:
            parts.append(f"{p['n_candidates']} candidates")
        return ", ".join(x for x in parts if x)
    if kind == ("orchestrator", "decision"):
        return f"w = {p.get('w')}, confidence {p.get('confidence')}, source {p.get('source')}"
    if ev.get("event") == "llm_call":
        try:
            answer = json.loads(p.get("response") or "")
        except (TypeError, ValueError):
            answer = {}
        if not isinstance(answer, dict):
            answer = {}
        shown = {k: answer[k] for k in ("relevance", "w", "action") if k in answer}
        head = f"`{p['test']}`" if p.get("test") else f"step {p.get('step')}"
        return f"{head}, attempt {p.get('attempt')}, cached {p.get('cached')}" + (f", {shown}" if shown else "")
    if kind == ("explainer", "explanation"):
        return f"`{p.get('test')}` at {float(p.get('budget', 0)):.0%}, ok = {p.get('ok')}"
    return ", ".join(f"{k} = {v}" for k, v in list(p.items())[:3])


# ------------------------------------------------------------------- CLI ----

def run(run_dir, runs_json, traces, ratings, causes=None, out="results/analysis", cases_dir="docs/cases",
        sample_dir="logs_sample", cfg=None, failing=None, export=True):
    """Whole analysis; `failing` can be injected (tests), otherwise it comes from LRTS."""
    cfg = cfg or load_config()
    run_dir_arg = Path(run_dir).as_posix()
    run_dir, runs_json = Path(repo_path(run_dir)), Path(runs_json)
    pb = pd.read_csv(run_dir / "per_build.csv")
    builds = sorted(pb.loc[pb["method"] == METHOD, "build"].unique())
    budgets = sorted({_bkey(b) for b in pb["budget"]})
    if failing is None:
        candidates = {b: method_entry(load_run_json(runs_json, b), METHOD, budgets[0])["ordered"] for b in builds}
        failing = failing_candidates(cfg, builds, candidates)
    rows = analyse(run_dir, runs_json, traces, ratings, failing, int(cfg["explainer"]["max_justification_chars"]))

    out = Path(repo_path(out))
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=CSV_COLUMNS).to_csv(out / "failure_categories.csv", index=False)
    summary = summarise(rows, len(builds) * len(budgets), budgets)
    command = f"python -m src.eval.failure_analysis --run-dir {run_dir_arg} ..."
    (out / "failure_summary.md").write_text(
        summary_markdown(summary, read_causes(causes), run_dir.name, len(builds), budgets, command), encoding="utf-8")

    cases_dir = Path(repo_path(cases_dir))
    cases_dir.mkdir(parents=True, exist_ok=True)
    tdir = trace_dir_for(traces, run_dir.name)
    chosen = choose_cases(rows, pb, summary)
    dest = Path(repo_path(sample_dir)) / tdir.name
    # a trace already in the sample is the same file of the same run: keep it as it is
    new = sorted(b for b in {c["build"] for c in chosen} if not (dest / f"{b}.jsonl").exists())
    if export and new:
        from src.obs.export_sample import export as export_traces
        export_traces(tdir.parent, tdir.name, new, repo_path(sample_dir))
    sample_rel = f"{Path(sample_dir).as_posix()}/{tdir.name}"
    for c in chosen:
        text = case_markdown(c, load_run_json(runs_json, c["build"]), pb, rows, failing[c["build"]],
                             read_trace(tdir, c["build"]), run_dir.name, sample_rel)
        (cases_dir / f"{c['name']}.md").write_text(text, encoding="utf-8")
    return rows, summary, chosen


def main(argv=None):
    ap = argparse.ArgumentParser(description="Failure analysis of the Full system on one run (P2-14).")
    ap.add_argument("--run-dir", required=True, help="e.g. results/E3_test_seed1")
    ap.add_argument("--runs-json", required=True, help="folder with the run's <build>.json files (not committed)")
    ap.add_argument("--traces", required=True, help="the run's trace folder (<build>.jsonl), or its parent")
    ap.add_argument("--ratings", required=True, help="results/gap2/ratings_final.csv (rating_items.csv next to it)")
    ap.add_argument("--causes", default="results/analysis/failure_causes.yaml",
                    help="hand-written likely causes per category (read, never written)")
    ap.add_argument("--out", default="results/analysis")
    ap.add_argument("--cases", default="docs/cases")
    ap.add_argument("--sample-dir", default="logs_sample")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    rows, summary, chosen = run(args.run_dir, args.runs_json, args.traces, args.ratings,
                                repo_path(args.causes), args.out, args.cases, args.sample_dir)
    for r in summary.itertuples(index=False):
        log.info("%s: %d pairs (%.3f)", r.category, r.pairs, r.share)
    for c in chosen:
        log.info("%s: %s at %.2f (%s)", c["name"], c["build"], c["budget"], c["category"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
