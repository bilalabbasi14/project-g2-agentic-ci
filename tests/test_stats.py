import numpy as np
import pandas as pd
import pytest
import yaml

from src.eval.stats import (StatsError, holm, load_comparisons, main, paired_test, rank_biserial, run,
                            seed_average)
from src.pipeline import PER_BUILD_COLUMNS


def _rows(method, values, seed=1, budget=0.1, split="test", metric="dtc"):
    """per_build.csv rows (format of src/pipeline.py) for one method: {build: value}."""
    out = []
    for build, v in values.items():
        r = {c: None for c in PER_BUILD_COLUMNS}
        r.update({"run_id": f"E9_{split}_seed{seed}", "experiment": "E9", "split": split, "seed": seed,
                  "build": build, "budget": budget, "method": method, "dtc": v, "sapfdc": v / 2,
                  "sds": 0.5, "apfdc_full": 0.5})
        if metric != "dtc":
            r[metric] = v
        out.append(r)
    return out


def _write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=PER_BUILD_COLUMNS).to_csv(path, index=False)
    return str(path)


def _comparisons(tmp_path, families, friedman_sets=None, metrics=("dtc",), budgets=(0.1,)):
    cfg = {**families, "friedman_sets": friedman_sets or {}, "metrics": list(metrics), "budgets": list(budgets)}
    p = tmp_path / "comparisons.yaml"
    p.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return str(p)


# ------------------------------------------------------------ building blocks ----

def test_holm_issue_example():
    # sorted 0.01*3 = 0.03; 0.03*2 = 0.06; 0.04*1 = 0.04 -> made monotone 0.06
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_holm_caps_at_one_and_keeps_nan():
    assert holm([0.5, 0.6]) == pytest.approx([1.0, 1.0])
    out = holm([0.01, float("nan"), 0.04])
    assert out[0] == pytest.approx(0.02) and np.isnan(out[1]) and out[2] == pytest.approx(0.04)


def test_rank_biserial_extremes_and_symmetry():
    assert rank_biserial([0.1, 0.2, 0.3]) == 1.0
    assert rank_biserial([-0.1, -0.2, -0.3]) == -1.0
    assert rank_biserial([0.1, -0.1, 0.3, -0.3]) == 0.0
    assert rank_biserial([0.0, 0.0]) == 0.0


def test_all_zero_differences_give_p_one_and_effect_zero():
    r = paired_test([0.0, 0.0, 0.0])
    assert r["p_raw"] == 1.0 and r["effect_r"] == 0.0 and r["ties"] == 3 and r["n"] == 3


def test_seed_averaging():
    df = pd.DataFrame(_rows("M", {"b1": 0.2}, seed=1) + _rows("M", {"b1": 0.4}, seed=2))
    avg = seed_average(df, ["dtc"])
    assert avg.loc[(avg["method"] == "M") & (avg["build"] == "b1"), "value"].item() == pytest.approx(0.3)


def test_same_seed_in_two_runs_counts_once():
    # a deterministic method stored by two runs with the same seed must not outweigh another seed
    df = pd.DataFrame(_rows("M", {"b1": 0.2}, seed=1) * 2 + _rows("M", {"b1": 0.5}, seed=2))
    assert seed_average(df, ["dtc"])["value"].item() == pytest.approx(0.35)


def test_comparisons_file_as_specified():
    c = load_comparisons()
    assert c["families"]["RQ1"] == {"target": "LLM-relevance", "against": ["DANTE-CCH", "DANTE-CCH-shipped"]}
    assert c["families"]["RQ3"]["against"] == ["DANTE-CCH", "Tuned-weight (LLM)"]
    assert list(c["families"]) == ["RQ1", "RQ3", "E3", "E1", "E5"]
    assert len(c["friedman_sets"]["ALL"]) == 11
    assert c["metrics"] == ["dtc", "sapfdc"] and c["budgets"] == [0.05, 0.1, 0.2]


# ---------------------------------------------------------------- end to end ----

def _hand_made(tmp_path):
    # T vs O at budget 10%, dtc:
    #   build  T                       O     diff
    #   b1     0.5                     0.3   +0.2   win
    #   b2     0.5                     0.5    0     tie
    #   b3     0.8 (seeds: 0.7, 0.9)   0.4   +0.4   win
    #   b4     0.2                     0.4   -0.2   loss
    #   b5     0.6                     0.1   +0.5   win
    #   b6     0.9                     -     (not shared, left out)
    # non-zero |diff| ranks: 0.2, 0.2 -> 1.5 each; 0.4 -> 3; 0.5 -> 4
    # R+ = 1.5 + 3 + 4 = 8.5, R- = 1.5 -> W = 1.5, r = 7 / 10 = 0.7
    t1 = {"b1": 0.5, "b2": 0.5, "b3": 0.7, "b4": 0.2, "b5": 0.6, "b6": 0.9}
    t2 = {"b1": 0.5, "b2": 0.5, "b3": 0.9, "b4": 0.2, "b5": 0.6, "b6": 0.9}
    o = {"b1": 0.3, "b2": 0.5, "b3": 0.4, "b4": 0.4, "b5": 0.1}
    c = {"b1": 0.1, "b2": 0.2, "b3": 0.3, "b4": 0.1, "b5": 0.2}
    p1 = _write(tmp_path / "E9_test_seed1" / "per_build.csv",
                _rows("T", t1) + _rows("O", o) + _rows("C", c) + _rows("T", {"b1": 0.0}, split="dev"))
    p2 = _write(tmp_path / "E9_test_seed2" / "per_build.csv", _rows("T", t2, seed=2))
    comps = _comparisons(tmp_path, {"FAM": {"target": "T", "against": ["O", "C"]}},
                         {"S": ["T", "O", "C"]})
    return [p1, p2], comps


def test_hand_made_pairwise_row(tmp_path):
    paths, comps = _hand_made(tmp_path)
    pw, fr, sv = run(paths, tmp_path / "out", comps)
    row = pw[(pw["other"] == "O") & (pw["metric"] == "dtc")].iloc[0]
    assert (row["n"], row["wins"], row["ties"], row["losses"]) == (5, 3, 1, 1)
    assert row["mean_diff"] == pytest.approx(0.18) and row["median_diff"] == pytest.approx(0.2)
    assert row["W"] == pytest.approx(1.5) and row["effect_r"] == pytest.approx(0.7)
    assert 0 < row["p_raw"] <= 1 and row["family"] == "FAM" and row["budget"] == 0.1
    # Holm within the family {O, C}
    fam = pw[pw["metric"] == "dtc"]
    assert fam["p_holm"].tolist() == pytest.approx(holm(fam["p_raw"].tolist()))
    on_disk = pd.read_csv(tmp_path / "out" / "pairwise.csv")
    assert list(on_disk.columns) == ["family", "target", "other", "metric", "budget", "n", "mean_diff",
                                     "median_diff", "wins", "ties", "losses", "W", "p_raw", "p_holm",
                                     "significant", "effect_r"]
    assert (tmp_path / "out" / "summary.md").read_text(encoding="utf-8").startswith("# Statistics")


def test_dev_split_is_ignored(tmp_path):
    paths, comps = _hand_made(tmp_path)
    pw, _, _ = run(paths, tmp_path / "out", comps)
    # the dev row T/b1 = 0.0 would turn b1 into a loss if it were used
    assert pw[pw["other"] == "O"].iloc[0]["wins"] == 3


def test_friedman_uses_builds_shared_by_all_methods(tmp_path):
    paths, comps = _hand_made(tmp_path)
    _, fr, _ = run(paths, tmp_path / "out", comps)
    assert set(fr["method"]) == {"T", "O", "C"} and (fr["n_builds"] == 5).all()
    assert fr["statistic"].nunique() == 1 and 0 <= fr["p_value"].iloc[0] <= 1
    ranks = dict(zip(fr["method"], fr["mean_rank"]))
    assert ranks["T"] < ranks["C"]          # rank 1 = best; T beats C on every build


def test_seed_variability(tmp_path):
    paths, comps = _hand_made(tmp_path)
    _, _, sv = run(paths, tmp_path / "out", comps)
    row = sv[(sv["method"] == "T") & (sv["metric"] == "dtc")].iloc[0]
    # per-seed means over builds b1..b6: seed 1 = 3.4 / 6, seed 2 = 3.6 / 6
    s1, s2 = 3.4 / 6, 3.6 / 6
    assert row["seeds"] == "1;2"
    assert row["mean"] == pytest.approx((s1 + s2) / 2) and row["std"] == pytest.approx(np.std([s1, s2], ddof=1))
    assert set(sv["method"]) == {"T"}       # O and C have one seed
    assert list(pd.read_csv(tmp_path / "out" / "seed_variability.csv").columns) == \
        ["method", "budget", "metric", "seeds", "mean", "std"]


def test_missing_methods_fail_with_clear_message(tmp_path):
    paths, _ = _hand_made(tmp_path)
    comps = _comparisons(tmp_path, {"FAM": {"target": "T", "against": ["O", "Ghost"]}}, {"S": ["T", "Nope", "C"]})
    with pytest.raises(StatsError, match="methods missing from the test-split results: Ghost, Nope"):
        run(paths, tmp_path / "out", comps)


def test_cli_with_glob(tmp_path):
    paths, comps = _hand_made(tmp_path)
    pattern = str(tmp_path / "E*_test_seed*" / "per_build.csv")
    assert main(["--runs", pattern, "--out", str(tmp_path / "cli"), "--comparisons", comps]) == 0
    for name in ("friedman.csv", "pairwise.csv", "seed_variability.csv", "summary.md"):
        assert (tmp_path / "cli" / name).exists()
    assert main(["--runs", str(tmp_path / "none*" / "x.csv"), "--out", str(tmp_path / "cli")]) == 1
