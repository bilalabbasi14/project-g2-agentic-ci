"""check_data on a tiny fake data tree (2 builds instead of 726); no real data needed."""
from src.data.check_data import check, main, status_word

BUILDS = [("PR-1", 1), ("PR-2", 3)]


def _tree(tmp_path):
    lrts, dante = tmp_path / "lrts", tmp_path / "dante"
    sol = dante / "rq2_karaf"
    lines = ["project,pr_name,build_id,stage_id"] + [f"karaf,{pr},{b},single" for pr, b in BUILDS] + \
            ["activemq,PR-9,1,single"]
    lrts.mkdir()
    (lrts / "dataset.csv").write_text("\n".join(lines) + "\n")
    for pr, b in BUILDS:
        z = lrts / "processed_test_result" / "karaf" / f"{pr}_build{b}" / "stage_single"
        z.mkdir(parents=True)
        (z / "test_class.csv.zip").write_bytes(b"zip")
        d = lrts / "shadata" / "karaf" / "diff"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{pr}_build{b}.diff").write_text("diff")
    rq1 = dante / "experiments" / "RQ1"
    rq1.mkdir(parents=True)
    names = [f"karaf_build_{pr}_{b}_single_tfidf_specific_boosted_False" for pr, b in BUILDS]
    # two methods per build: the check counts distinct builds, not rows
    (rq1 / "karaf.csv").write_text("build,method,apfdc\n" + "".join(
        f"{n},{m},0.5\n" for n in names for m in ("DANTE-CCH", "Random")))
    for budget in ("Budget_05_Percent", "Budget_10_Percent", "Budget_20_Percent"):
        for n in names:
            f = sol / budget / n
            f.mkdir(parents=True)
            (f / "DANTE-CCH.json").write_text("{}")
            (f / "Random.json").write_text("{}")
    return lrts, dante, sol


def _run(tmp_path, tree):
    lrts, dante, sol = tree
    return check(str(lrts), str(dante), str(sol), expected_builds=2, expected_eval_builds=2)


def test_complete_tree_passes(tmp_path):
    res = _run(tmp_path, _tree(tmp_path))
    assert len(res) == 7
    assert all(passed for _, passed, _ in res), res


def test_missing_diff_fails_and_names_build(tmp_path):
    tree = _tree(tmp_path)
    (tree[0] / "shadata" / "karaf" / "diff" / "PR-2_build3.diff").unlink()
    res = {name: (passed, detail) for name, passed, detail in _run(tmp_path, tree)}
    passed, detail = res[".diff per build"]
    assert not passed
    assert "PR-2_build3" in detail and "1 of 2 found" in detail
    assert status_word(passed, detail) == "MISSING"
    assert res["test results per build"][0]


def test_wrong_counts_and_missing_json(tmp_path):
    tree = _tree(tmp_path)
    lrts, dante, sol = tree
    (sol / "Budget_10_Percent" / "karaf_build_PR-1_1_single_tfidf_specific_boosted_False" / "Random.json").unlink()
    res = {name: (passed, detail) for name, passed, detail in
           check(str(lrts), str(dante), str(sol), expected_builds=3, expected_eval_builds=2)}
    assert not res["dataset.csv"][0] and status_word(*res["dataset.csv"]) == "WRONG"
    assert not res["solutions Budget_10_Percent"][0]
    assert "karaf_build_PR-1_1" in res["solutions Budget_10_Percent"][1]
    assert res["solutions Budget_05_Percent"][0]


def test_missing_dataset(tmp_path):
    res = check(str(tmp_path / "nope"), str(tmp_path / "nope"), str(tmp_path / "nope"))
    assert not any(passed for _, passed, _ in res)
    assert all(status_word(p, d) == "MISSING" for _, p, d in res)


def test_main_exit_code(tmp_path, capsys):
    lrts, dante, sol = _tree(tmp_path)
    # default expected counts (726, 50) do not match the tiny tree, so main reports failure
    assert main(["--lrts", str(lrts), "--dante", str(dante), "--solutions", str(sol)]) == 1
    out = capsys.readouterr().out
    assert "WRONG" in out and "some checks failed" in out


def test_extracted_layout_passes(tmp_path):
    """Kaggle serves the test results extracted: stage_single/test_class.csv instead of the .zip."""
    lrts, dante, sol = _tree(tmp_path)
    for z in (lrts / "processed_test_result").rglob("test_class.csv.zip"):
        z.unlink()
        (z.parent / "test_class.csv").write_text("testclass,duration,outcome,last_outcome\n")
    res = {name: (passed, detail) for name, passed, detail in
           check(str(lrts), str(dante), str(sol), expected_builds=2, expected_eval_builds=2)}
    assert all(p for p, _ in res.values()), res
    assert res["test results per build"][1] == "2 of 2 found (0 test_class.csv.zip, 2 extracted test_class.csv)"


def test_rq1_without_build_column_is_wrong_not_a_crash(tmp_path):
    lrts, dante, sol = _tree(tmp_path)
    (dante / "experiments" / "RQ1" / "karaf.csv").write_text("name,method,apfdc\nx,DANTE-CCH,0.5\n")
    res = {name: (passed, detail) for name, passed, detail in
           check(str(lrts), str(dante), str(sol), expected_builds=2, expected_eval_builds=2)}
    passed, detail = res["RQ1/karaf.csv"]
    assert not passed and "no 'build' column" in detail
    assert status_word(passed, detail) == "WRONG"
    (dante / "experiments" / "RQ1" / "karaf.csv").write_text("")
    passed, detail = {n: (p, d) for n, p, d in check(str(lrts), str(dante), str(sol), 2, 2)}["RQ1/karaf.csv"]
    assert not passed and status_word(passed, detail) == "WRONG"
