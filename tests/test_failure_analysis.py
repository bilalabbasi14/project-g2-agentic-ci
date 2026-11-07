"""Failure analysis (P2-14): one positive and one negative example per category, the
memorisation regex, and a small end-to-end run on fake files (no data, no model)."""
import csv
import json

import pandas as pd

from src.eval import failure_analysis as fa
from src.settings import load_config

FAIL = {"p.FailA", "p.FailB"}


# ------------------------------------------------------------ categories ----

def test_f1_fallback():
    agent = {"source": "agent", "fallback": None, "w": 0.7}
    assert fa.f1_fallback(False, agent) is None
    assert "relevance fell back" in fa.f1_fallback(True, agent)
    detail = fa.f1_fallback(False, {"source": "fallback", "fallback": {"reason": "low_confidence"}, "w": 0.6666667})
    assert "orchestrator fell back (low_confidence)" in detail


def test_f2_outside_shortlist():
    assert fa.f2_outside_shortlist(FAIL, selected=["p.FailA"], shortlist=["p.Other"]) == ["p.FailB"]
    assert fa.f2_outside_shortlist(FAIL, selected=["p.FailA"], shortlist=["p.FailB"]) == []      # on the shortlist
    assert fa.f2_outside_shortlist(FAIL, selected=sorted(FAIL), shortlist=[]) == []              # all caught


def test_f3_low_llm_relevance():
    short = ["p.FailA", "p.FailB"]
    assert fa.f3_low_llm_relevance(FAIL, [], short, {"p.FailA": 0.1, "p.FailB": 0.2}) == ["p.FailA"]
    assert fa.f3_low_llm_relevance(FAIL, [], short, {"p.FailA": 0.5, "p.FailB": 0.9}) == []
    assert fa.f3_low_llm_relevance(FAIL, ["p.FailA"], short, {"p.FailA": 0.0, "p.FailB": 0.9}) == []  # selected
    assert fa.f3_low_llm_relevance(FAIL, [], [], {"p.FailA": 0.0}) == []                         # not shortlisted


def test_f4_did_not_fit():
    ordered = [f"p.T{i}" for i in range(9)] + ["p.FailA"] + ["p.FailB"]   # FailA is 10th, FailB 11th
    assert fa.f4_did_not_fit(FAIL, selected=ordered[:3], ordered=ordered) == ["p.FailA"]
    assert fa.f4_did_not_fit(FAIL, selected=ordered[:10], ordered=ordered) == []    # FailA selected, FailB not top 10


def test_f5_agent_weight_harmful():
    assert fa.f5_agent_weight_harmful(0.5, 1.0)
    assert not fa.f5_agent_weight_harmful(1.0, 1.0)
    assert not fa.f5_agent_weight_harmful(1.0, 0.5)


def test_f6_unsound_explanations():
    rated = [{"build": "B1", "budget": 0.1, "test": "p.X", "final_rating": "unsound"},
             {"build": "B1", "budget": 0.1, "test": "p.Y", "final_rating": "sound"},
             {"build": "B1", "budget": 0.2, "test": "p.Z", "final_rating": "unsound"}]
    assert fa.f6_unsound_explanations(rated, "B1", 0.10) == ["p.X"]
    assert fa.f6_unsound_explanations(rated, "B2", 0.10) == []
    assert fa.f6_unsound_explanations(rated[1:2], "B1", 0.1) == []


def test_memorisation_regex_flags_identifiers_absent_from_the_prompt():
    text = "Likely affected, see KARAF-1234 and BundleContextImpl."
    assert fa.unsupported_identifiers(text, "diff of ShellCommand only") == ["BundleContextImpl", "KARAF-1234"]
    assert fa.unsupported_identifiers(text, "KARAF-1234 changed BundleContextImpl") == []
    assert fa.unsupported_identifiers("no identifiers here", "") == []


def test_s_caught_extra():
    assert fa.s_caught_extra(FAIL, selected_full=["p.FailA", "p.X"], selected_dante=["p.X"]) == ["p.FailA"]
    assert fa.s_caught_extra(FAIL, selected_full=["p.FailA"], selected_dante=["p.FailA"]) == []


# ------------------------------------------------------------ end to end ----

BUDGETS = (0.05, 0.1, 0.2)
FILLER = [f"p.T{i}" for i in range(10)]
# value orders; every missed failing test is ranked below 10th, so F4 never applies
ORDER = {"B1": ["p.FailA", "p.Hist", "p.Rel"] + FILLER + ["p.FailB"],
         "B2": ["p.Hist", "p.Rel"] + FILLER + ["p.FailA", "p.FailB"]}


def _method(name, budget, selected, ordered):
    return {"method": name, "budget": budget, "ranking_source": "llm", "w": 0.7, "metrics": {},
            "selected": selected, "ordered": ordered, "cost": {}}


def _write_fake_run(tmp_path):
    """Two builds. B1: Full system catches FailA (DANTE-CCH does not) and misses FailB,
    which is outside the shortlist (F2). B2: FailA is shortlisted, gets relevance 0.1
    and is missed (F3); one explanation is rated unsound (F6)."""
    run_dir = tmp_path / "results" / "E3_test_seed1"
    runs = tmp_path / "runs"
    traces = tmp_path / "traces" / "E3_test_seed1"
    gap2 = tmp_path / "gap2"
    for d in (run_dir, runs, traces, gap2):
        d.mkdir(parents=True)
    pb = []
    for b in BUDGETS:
        for build, full_dtc, dante_dtc, agent_dtc in (("B1", 0.5, 0.0, 0.5), ("B2", 0.0, 0.0, 0.0)):
            for method, dtc in (("Full system", full_dtc), ("DANTE-CCH", dante_dtc), ("Agent-weighted", agent_dtc)):
                pb.append({"build": build, "budget": b, "method": method, "dtc": dtc, "sapfdc": dtc,
                           "apfdc_full": 0.5, "selected": 2, "found": int(dtc * 2), "selected_duration_s": 1.0})
    pd.DataFrame(pb).to_csv(run_dir / "per_build.csv", index=False)
    for build, full_sel, dante_sel, short, rel in (
            ("B1", ["p.FailA", "p.Hist"], ["p.Hist", "p.Rel"], ["p.FailA", "p.Hist"], {"p.FailA": 0.9}),
            ("B2", ["p.Hist", "p.Rel"], ["p.Hist", "p.Rel"], ["p.FailA", "p.Hist"], {"p.FailA": 0.1})):
        run = {"build": build, "candidates": len(ORDER[build]), "failing": 2 if build == "B1" else 1,
               "shortlist": short,
               "relevance": {"llm_shortlist": {"relevance": rel, "reasons": {"p.FailA": "Touches ShellCommand"},
                                               "fell_back": False, "fallbacks": []}},
               "decisions": {"llm_shortlist": {"w": 0.7, "confidence": 0.9, "source": "agent",
                                               "reason": "History dominates", "fallback": None}},
               "methods": [m for b in BUDGETS for m in (_method("Full system", b, full_sel, ORDER[build]),
                                                        _method("DANTE-CCH", b, dante_sel, ORDER[build]))]}
        (runs / f"{build}.json").write_text(json.dumps(run), encoding="utf-8")
        events = [{"step": 1, "component": "pipeline", "event": "state",
                   "payload": {"stage": "loaded", "n_candidates": len(ORDER[build])}},
                  {"step": 2, "component": "semantic_analyzer", "event": "llm_call",
                   "payload": {"test": "p.FailA", "prompt": "diff changes ShellCommand", "attempt": 0,
                               "cached": False, "response": "{\"relevance\": 0.1}"}},
                  {"step": 3, "component": "orchestrator", "event": "llm_call",
                   "payload": {"step": 1, "prompt": "choose w", "attempt": 0, "cached": False,
                               "response": "{\"w\": 0.7}"}}]
        (traces / f"{build}.jsonl").write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
    evidence = {"test": "p.Rel", "skip_cause": "did_not_fit"}
    pd.DataFrame([{"build": "B2", "budget": 0.1, "method": "Full system", "test": "p.Rel", "ok": True,
                   "justification": "Skipped: it did not fit.", "evidence": json.dumps(evidence)}]
                 ).to_csv(run_dir / "explanations.csv", index=False)
    with open(gap2 / "rating_items.csv", "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows([["item_id", "build", "budget", "test"], ["R001", "B2", "0.1", "p.Rel"]])
    with open(gap2 / "ratings_final.csv", "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows([["item_id", "rating_ali", "rating_bilal", "final_rating"],
                                 ["R001", "unsound", "unsound", "unsound"]])
    causes = tmp_path / "failure_causes.yaml"
    causes.write_text("F2: |\n  Hand-written text for F2.\nF3: ''\n", encoding="utf-8")
    return run_dir, runs, traces, gap2 / "ratings_final.csv", causes


def test_end_to_end_on_a_fake_run(tmp_path):
    run_dir, runs, traces, ratings, causes = _write_fake_run(tmp_path)
    failing = {"B1": {"p.FailA", "p.FailB"}, "B2": {"p.FailA"}}
    out, cases = tmp_path / "analysis", tmp_path / "cases"
    rows, summary, chosen = fa.run(run_dir, runs, traces.parent, ratings, causes=causes, out=out, cases_dir=cases,
                                   sample_dir="logs_sample", cfg=load_config(), failing=failing, export=False)
    got = {(r["build"], r["budget"], r["category"]) for r in rows}
    for b in BUDGETS:
        assert ("B1", b, "S") in got and ("B1", b, "F2") in got and ("B2", b, "F3") in got
        assert ("B1", b, "F3") not in got and ("B2", b, "F2") not in got
    assert ("B2", 0.1, "F6") in got and ("B2", 0.05, "F6") not in got
    assert not [r for r in rows if r["category"] in ("F1", "F4", "F5", "F7")]

    with open(out / "failure_categories.csv", encoding="utf-8", newline="") as f:
        assert next(csv.reader(f)) == fa.CSV_COLUMNS
    counts = summary.set_index("category")["pairs"].to_dict()
    assert counts["F2"] == 3 and counts["F3"] == 3 and counts["F6"] == 1 and counts["S"] == 3
    md = (out / "failure_summary.md").read_text(encoding="utf-8")
    assert "Hand-written text for F2." in md                      # taken from the causes file
    assert md.count(fa.NOT_WRITTEN) == len(fa.CATEGORIES) - 1     # an empty entry is not written

    assert [c["name"] for c in chosen] == ["success_1", "success_2", "failure_1", "failure_2"]
    assert chosen[0]["build"] == "B1"                             # largest %DTC gain at 10%
    assert {chosen[2]["category"], chosen[3]["category"]} == {"F2", "F3"}
    for c in chosen:
        text = (cases / f"{c['name']}.md").read_text(encoding="utf-8")
        assert c["build"] in text and "## Trajectory" in text and "logs_sample/E3_test_seed1" in text


def test_causes_file_is_read_never_written(tmp_path):
    assert fa.read_causes(tmp_path / "missing.yaml") == {}
    p = tmp_path / "c.yaml"
    p.write_text("F1: |\n  Line one\n  line two.\nF2: null\n", encoding="utf-8")
    assert fa.read_causes(p) == {"F1": "Line one line two."}
