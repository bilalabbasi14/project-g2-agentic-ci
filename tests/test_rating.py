import csv
import json
from collections import Counter

import pandas as pd
import pytest

from src.eval.rating import (INSTRUCTION, RatingError, cmd_agreement, cmd_final, cmd_sample, cohen_kappa,
                             draw_sample, load_explanations, main, read_sheet, stratum_sizes)
from src.pipeline import EXPLANATION_COLUMNS

BUDGETS = (0.05, 0.10, 0.20)


def _evidence(test):
    return {"test": test, "rank_by_value": 7, "n_candidates": 80, "n_selected": 9,
            "history": {"test": test, "history_builds": 100, "runs": 100, "failures": 2, "failure_rate": 0.02,
                        "last_failure_distance": 5, "recent_outcomes": [0, None, 1]},
            "history_score": 0.41, "relevance_used": 0.6, "relevance_reason": "uses the changed class",
            "changed_files": ["core/a/Cache.java"], "duration_s": 120.0, "budget_s": 300.0,
            "remaining_budget_at_turn_s": 40.5, "skip_cause": "did_not_fit", "fits_if_budget_s": 380.0}


def _write_explanations(run_dir, per_budget, extra_noise=True):
    """A fake explanations.csv in the format of src/pipeline.py (EXPLANATION_COLUMNS)."""
    rows = []
    for b, count in zip(BUDGETS, per_budget):
        for i in range(count):
            test = f"org.x.T{i:03d}Test"
            rows.append({"build": f"PR-{i % 7}_build{i}", "budget": b, "method": "Full system", "test": test,
                         "rank_by_value": 7, "ok": True, "error": "", "justification": f"Skipped {test} at {b}.",
                         "cited_facts": json.dumps(["failures: 2 of 100 runs"]),
                         "evidence": json.dumps(_evidence(test)), "latency_s": 1.0, "prompt_tokens": 10,
                         "completion_tokens": 5})
    if extra_noise:   # failed explanations and other methods must never be sampled
        rows.append({**rows[0], "ok": False, "justification": "", "test": "org.x.FailedTest"})
        rows.append({**rows[0], "method": "Full system (no shortlist)", "test": "org.x.OtherMethodTest"})
    run_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=EXPLANATION_COLUMNS).to_csv(run_dir / "explanations.csv", index=False)


def _read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _fill(path, ratings):
    rows = _read(path)
    for r, v in zip(rows, ratings):
        r["rating"] = v
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item_id", "rating", "note"])
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------ kappa ----

def test_kappa_identical_ratings_is_one():
    a = ["sound", "partly", "unsound", "sound"]
    assert cohen_kappa(a, list(a)) == 1.0
    assert cohen_kappa(["sound"] * 5, ["sound"] * 5) == 1.0     # p_e = 1 (single category)


def test_kappa_textbook_two_category_example():
    # Wikipedia "Cohen's kappa" example, 50 items, rows = rater A, columns = rater B:
    #            B yes  B no
    #   A yes      20     5
    #   A no       10    15
    # p_o = (20 + 15) / 50 = 0.70; p_e = 0.5 * 0.6 + 0.5 * 0.4 = 0.50; kappa = 0.20 / 0.50 = 0.40
    a = ["sound"] * 25 + ["unsound"] * 25
    b = ["sound"] * 20 + ["unsound"] * 5 + ["sound"] * 10 + ["unsound"] * 15
    assert cohen_kappa(a, b) == pytest.approx(0.4)


def test_kappa_three_category_worked_example():
    # Confusion matrix, 50 items, rows = Ali, columns = Bilal (sound, partly, unsound):
    #   sound    20  5  0   (row total 25)
    #   partly    3 10  2   (15)
    #   unsound   2  3  5   (10)
    #   column totals 25, 18, 7
    # p_o = (20 + 10 + 5) / 50 = 0.70
    # p_e = (25*25 + 15*18 + 10*7) / 50^2 = 965 / 2500 = 0.386
    # kappa = (0.70 - 0.386) / (1 - 0.386) = 0.314 / 0.614 = 0.511401
    cells = {("sound", "sound"): 20, ("sound", "partly"): 5, ("partly", "sound"): 3, ("partly", "partly"): 10,
             ("partly", "unsound"): 2, ("unsound", "sound"): 2, ("unsound", "partly"): 3,
             ("unsound", "unsound"): 5}
    a = [x for (x, _), k in cells.items() for _ in range(k)]
    b = [y for (_, y), k in cells.items() for _ in range(k)]
    assert cohen_kappa(a, b) == pytest.approx(0.314 / 0.614)


# --------------------------------------------------------------- sampling ----

def test_stratum_sizes():
    assert stratum_sizes(100, BUDGETS) == {0.05: 34, 0.10: 33, 0.20: 33}


def test_sample_reproducible_and_respects_budget_counts(tmp_path):
    _write_explanations(tmp_path / "run", (60, 50, 45))
    cmd_sample(tmp_path / "run", 100, 42, tmp_path / "a")
    cmd_sample(tmp_path / "run", 100, 42, tmp_path / "b")
    a, b = _read(tmp_path / "a" / "rating_items.csv"), _read(tmp_path / "b" / "rating_items.csv")
    assert a == b
    assert [r["item_id"] for r in a] == [f"R{i:03d}" for i in range(1, 101)]
    assert Counter(float(r["budget"]) for r in a) == {0.05: 34, 0.10: 33, 0.20: 33}
    assert len({(r["build"], r["budget"], r["test"]) for r in a}) == 100
    assert not {"org.x.FailedTest", "org.x.OtherMethodTest"} & {r["test"] for r in a}
    assert list(a[0]) == ["item_id", "build", "budget", "test", "justification", "cited_facts", "evidence"]
    # another seed gives another sample
    cmd_sample(tmp_path / "run", 100, 7, tmp_path / "c")
    assert _read(tmp_path / "c" / "rating_items.csv") != a


def test_sample_item_order_is_random_not_by_budget(tmp_path):
    _write_explanations(tmp_path / "run", (60, 50, 45))
    items, _ = draw_sample(load_explanations(tmp_path / "run"), 100, 42)
    assert items["budget"].tolist() != sorted(items["budget"].tolist())


def test_small_stratum_taken_whole_and_filled_from_others(tmp_path):
    _write_explanations(tmp_path / "run", (60, 50, 20))
    notes = cmd_sample(tmp_path / "run", 100, 42, tmp_path / "out")
    got = Counter(float(r["budget"]) for r in _read(tmp_path / "out" / "rating_items.csv"))
    assert got[0.20] == 20 and sum(got.values()) == 100
    assert got[0.05] >= 34 and got[0.10] >= 33
    assert any("budget 0.2: only 20" in n for n in notes) and any(n.startswith("filled") for n in notes)
    assert "Sampling notes" in (tmp_path / "out" / "rating_items.md").read_text(encoding="utf-8")


def test_too_few_explanations_is_an_error(tmp_path):
    _write_explanations(tmp_path / "run", (5, 5, 5))
    with pytest.raises(RatingError, match="only 15 usable"):
        cmd_sample(tmp_path / "run", 100, 42, tmp_path / "out")


def test_sheets_and_markdown(tmp_path):
    _write_explanations(tmp_path / "run", (40, 40, 40))
    cmd_sample(tmp_path / "run", 30, 42, tmp_path / "out")
    for rater in ("ali", "bilal"):
        sheet = _read(tmp_path / "out" / f"ratings_{rater}.csv")
        assert [r["item_id"] for r in sheet] == [f"R{i:03d}" for i in range(1, 31)]
        assert all(r["rating"] == "" for r in sheet)
    md = (tmp_path / "out" / "rating_items.md").read_text(encoding="utf-8")
    assert INSTRUCTION in md and "**sound** = every factual statement is supported" in md
    assert md.count("\n## R") == 30
    assert "- Budget left when the test was reached (s): 40.5" in md      # readable, not raw JSON
    assert "  - failures: 2" in md and "0, -, 1" in md and '"remaining_budget_at_turn_s"' not in md
    assert "- failures: 2 of 100 runs" in md                              # cited facts listed


# -------------------------------------------------------------- agreement ----

def _sampled(tmp_path, n=6):
    _write_explanations(tmp_path / "run", (10, 10, 10))
    cmd_sample(tmp_path / "run", n, 42, tmp_path / "out")
    return tmp_path / "out"


def test_invalid_rating_reported_with_its_row(tmp_path):
    d = _sampled(tmp_path)
    _fill(d / "ratings_ali.csv", ["sound", "partly", "Sound ", "good", "unsound", ""])
    with pytest.raises(RatingError) as e:
        read_sheet(d / "ratings_ali.csv")
    msg = str(e.value)
    assert "ratings_ali.csv line 5, item R004: rating = 'good'" in msg      # header is line 1
    assert "line 7, item R006: rating = ''" in msg
    assert "R003" not in msg                                              # case and spaces are accepted
    _fill(d / "ratings_bilal.csv", ["sound"] * 6)
    assert main(["agreement", "--dir", str(d)]) == 1


def test_agreement_and_final_flow(tmp_path):
    d = _sampled(tmp_path)
    ali = ["sound", "sound", "partly", "unsound", "sound", "sound"]
    bilal = ["sound", "partly", "partly", "unsound", "sound", "unsound"]
    _fill(d / "ratings_ali.csv", ali)
    _fill(d / "ratings_bilal.csv", bilal)
    stats = cmd_agreement(d)
    assert stats["n"] == 6 and stats["raw_agreement"] == pytest.approx(4 / 6)
    assert stats["kappa"] == pytest.approx(cohen_kappa(ali, bilal))
    assert stats["share_sound_ali"] == pytest.approx(4 / 6) and stats["share_sound_bilal"] == pytest.approx(2 / 6)
    assert _read(d / "disagreements.csv") == [
        {"item_id": "R002", "rating_ali": "sound", "rating_bilal": "partly"},
        {"item_id": "R006", "rating_ali": "sound", "rating_bilal": "unsound"}]
    final = _read(d / "ratings_final.csv")
    assert [r["final_rating"] for r in final] == ["sound", "", "partly", "unsound", "sound", ""]
    assert "Cohen's kappa" in (d / "agreement.md").read_text(encoding="utf-8")

    with pytest.raises(RatingError, match="final_rating"):     # disagreements not resolved yet
        cmd_final(d)
    final[1]["final_rating"], final[5]["final_rating"] = "sound", "unsound"
    with open(d / "ratings_final.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(final[0]))
        w.writeheader()
        w.writerows(final)
    rows = cmd_final(d)
    overall = rows[0]
    assert overall["n"] == 6 and overall["share_sound"] == pytest.approx(round(3 / 6, 4))
    assert overall["rq2_sound_condition_holds"] is False
    assert overall["kappa"] == pytest.approx(round(stats["kappa"], 4))
    assert sum(r["n"] for r in rows[1:]) == 6
    summary = _read(d / "rating_summary.csv")
    assert summary[0]["scope"] == "overall" and summary[0]["rq2_sound_condition_holds"] == "False"
    assert "does not hold" in (d / "rating_summary.md").read_text(encoding="utf-8")


def test_rq2_condition_holds_at_eighty_percent(tmp_path):
    d = _sampled(tmp_path, n=10)
    ratings = ["sound"] * 8 + ["partly", "unsound"]
    _fill(d / "ratings_ali.csv", ratings)
    _fill(d / "ratings_bilal.csv", ratings)
    cmd_agreement(d)
    rows = cmd_final(d)
    assert rows[0]["share_sound"] == 0.8 and rows[0]["rq2_sound_condition_holds"] is True
    assert rows[0]["kappa"] == 1.0


def test_cli_sample(tmp_path):
    _write_explanations(tmp_path / "run", (10, 10, 10))
    assert main(["sample", "--run-dir", str(tmp_path / "run"), "--n", "9", "--seed", "42",
                 "--out", str(tmp_path / "out")]) == 0
    assert len(_read(tmp_path / "out" / "rating_items.csv")) == 9
