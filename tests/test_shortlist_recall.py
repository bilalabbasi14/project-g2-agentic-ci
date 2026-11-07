"""Shortlist recall (P2-12): recall_at_k, the summary and the output files; no data needed."""
import csv
from types import SimpleNamespace

from src.eval.shortlist_recall import CSV_COLUMNS, build_rows, recall_at_k, render_markdown, run, summarise
from src.settings import load_config
from tests.test_end_to_end import FakeLoader, _fixture


def test_failing_third_by_tfidf_recall_at_2_is_0_and_at_3_is_1():
    # F has no failure history (history 0), so it can only enter through TF-IDF, where it ranks 3rd.
    # top-2 history = {x, y}, top-2 TF-IDF = {x, y}            -> F not shortlisted: recall@2 = 0
    # top-3 history = {x, y, z}, top-3 TF-IDF = {x, y, F}      -> F shortlisted:     recall@3 = 1
    history = {"x": 0.5, "y": 0.4, "z": 0.3, "F": 0.0}
    tfidf = {"x": 0.9, "y": 0.8, "F": 0.7, "z": 0.1}
    assert recall_at_k(history, tfidf, {"F"}, 2) == (0, 0.0, 2)
    assert recall_at_k(history, tfidf, {"F"}, 3) == (1, 1.0, 4)


def test_failing_test_with_zero_scores_is_never_shortlisted():
    # the shortlister ignores zero scores, so G is not taken even when k exceeds the number of tests
    history = {"a": 0.3, "b": 0.2, "G": 0.0}
    tfidf = {"a": 0.0, "b": 0.6, "G": 0.0}
    for k in (1, 2, 3, 10, 50):
        n_in, recall, size = recall_at_k(history, tfidf, {"G"}, k)
        assert (n_in, recall) == (0, 0.0)
        assert size <= 2


def test_no_failing_test_gives_undefined_recall():
    assert recall_at_k({"a": 0.5}, {"a": 0.5}, set(), 10) == (0, None, 1)


def test_summary_and_markdown_mark_the_used_k():
    rows = [{"build": "B1", "k": 5, "n_failing": 2, "n_in_shortlist": 0, "recall": 0.0, "shortlist_size": 8},
            {"build": "B2", "k": 5, "n_failing": 1, "n_in_shortlist": 1, "recall": 1.0, "shortlist_size": 6},
            {"build": "B1", "k": 10, "n_failing": 2, "n_in_shortlist": 1, "recall": 0.5, "shortlist_size": 14},
            {"build": "B2", "k": 10, "n_failing": 1, "n_in_shortlist": 1, "recall": 1.0, "shortlist_size": 12},
            {"build": "B3", "k": 10, "n_failing": 0, "n_in_shortlist": 0, "recall": None, "shortlist_size": 11}]
    s = {x["k"]: x for x in summarise(rows, used_k=10)}
    assert s[5] == {"k": 5, "used": False, "n_builds": 2, "mean_recall": 0.5, "median_recall": 0.5,
                    "share_recall_0": 0.5, "share_recall_1": 0.5, "mean_shortlist_size": 7.0}
    assert s[10]["used"] and s[10]["n_builds"] == 2              # B3 has no failing test: left out
    assert (s[10]["mean_recall"], s[10]["share_recall_0"], s[10]["share_recall_1"]) == (0.75, 0.0, 0.5)
    md = render_markdown(list(s.values()), "test", 10, "python -m src.eval.shortlist_recall --split test", 2)
    assert "**k = 10 is the configuration actually used**" in md
    assert "| **10** | **used** |" in md and "| 5 | describes the limit only |" in md


def test_run_on_fixture_writes_the_files_with_exact_columns(tmp_path):
    cfg = load_config()
    build, hist = _fixture()
    rows = [SimpleNamespace(pr_name="PR-1", build_id=1, stage_id="single")]
    csv_path, md_path, summary = run(cfg, "test", [5, 20], loader=FakeLoader(build, hist), rows=rows,
                                     out_dir=tmp_path)
    assert (csv_path.name, md_path.name) == ("shortlist_recall_test.csv", "shortlist_recall_test.md")
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == CSV_COLUMNS
        out = list(reader)
    assert sorted(int(r["k"]) for r in out) == [5, 10, 20]           # the used k (10) is always reported
    assert all(r["build"] == "PR-1_build1" and r["n_failing"] == "2" for r in out)
    assert [s["k"] for s in summary if s["used"]] == [cfg["shortlist"]["k"]]
    assert "configuration actually used" in md_path.read_text(encoding="utf-8")


def test_outcomes_are_only_ground_truth():
    # flipping the outcomes changes which tests count as failing, never the shortlist itself
    from src.dante import scores
    cfg = load_config()
    build, hist = _fixture()
    df = scores(build, hist, cfg, "DANTE-CCH")
    flipped = df.assign(actual_outcome=1 - df["actual_outcome"])
    a = build_rows("B", df, [1, 2, 10])
    b = build_rows("B", flipped, [1, 2, 10])
    assert [r["shortlist_size"] for r in a] == [r["shortlist_size"] for r in b]
    assert [r["n_failing"] for r in a] != [r["n_failing"] for r in b]
