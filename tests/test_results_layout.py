"""Test results stored as test_class.csv.zip (LRTS) or as the extracted test_class.csv
(the Kaggle copy) must be read identically by the loader and the history tool."""
import zipfile

import pandas as pd

from src.data.loader import LRTSLoader
from src.tools.history_retrieval import (
    HistoryRetrieval, open_test_class_csv, read_test_class_zip, resolve_test_class_file,
)

BUILDS = [("PR-1", 1, 100.0), ("PR-1", 2, 200.0), ("PR-2", 1, 300.0)]
CSV = {
    ("PR-1", 1): "testclass,duration,outcome,last_outcome\na.T1,1.5,1,0\na.T2,0.25,0,0\n",
    ("PR-1", 2): "testclass,duration,outcome,last_outcome\na.T1,1.0,0,1\na.T2,0.5,1,0\nb.T3,2.0,0,0\n",
    ("PR-2", 1): "testclass,duration,outcome,last_outcome\na.T1,1.25,1,0\n,0.1,0,0\n",
}


def _root(tmp_path, name, extracted):
    root = tmp_path / name
    root.mkdir()
    rows = ["project,pr_name,build_id,stage_id,build_timestamp,build_head_sha"] + \
           [f"karaf,{pr},{b},single,{ts},{'0' * 40}" for pr, b, ts in BUILDS]
    (root / "dataset.csv").write_text("\n".join(rows) + "\n")
    for pr, b, _ in BUILDS:
        d = root / "processed_test_result" / "karaf" / f"{pr}_build{b}" / "stage_single"
        d.mkdir(parents=True)
        if extracted:
            (d / "test_class.csv").write_text(CSV[(pr, b)], newline="")
        else:
            with zipfile.ZipFile(d / "test_class.csv.zip", "w") as z:
                z.writestr("test_class.csv", CSV[(pr, b)])
    return root


def test_resolve_prefers_zip_then_extracted(tmp_path):
    z = _root(tmp_path, "z", extracted=False) / "processed_test_result/karaf/PR-1_build1/stage_single"
    e = _root(tmp_path, "e", extracted=True) / "processed_test_result/karaf/PR-1_build1/stage_single"
    assert resolve_test_class_file(str(z / "test_class.csv.zip")) == str(z / "test_class.csv.zip")
    assert resolve_test_class_file(str(e / "test_class.csv.zip")) == str(e / "test_class.csv")
    assert resolve_test_class_file(str(tmp_path / "nope" / "test_class.csv.zip")) is None
    with open_test_class_csv(str(e / "test_class.csv")) as a, open_test_class_csv(str(z / "test_class.csv.zip")) as b:
        assert a.read() == b.read()


def test_loader_reads_both_layouts_identically(tmp_path):
    lz = LRTSLoader(str(_root(tmp_path, "z", extracted=False)), "karaf")
    le = LRTSLoader(str(_root(tmp_path, "e", extracted=True)), "karaf")
    for (_, rz), (_, re_) in zip(lz.meta.iterrows(), le.meta.iterrows()):
        pd.testing.assert_frame_equal(lz.test_class_df(rz), le.test_class_df(re_))
    last_z, last_e = lz.meta.iloc[-1], le.meta.iloc[-1]
    hz, he = lz.history(last_z, 100, 10), le.history(last_e, 100, 10)
    assert len(hz.frames) == len(he.frames) == 2
    for a, b in zip(hz.frames, he.frames):
        pd.testing.assert_frame_equal(a, b)
    assert hz.previous_outcomes == he.previous_outcomes


def test_loader_missing_results_is_none(tmp_path):
    root = _root(tmp_path, "e", extracted=True)
    (root / "processed_test_result/karaf/PR-2_build1/stage_single/test_class.csv").unlink()
    loader = LRTSLoader(str(root), "karaf")
    assert loader.test_class_df(loader.meta.iloc[-1]) is None


def test_history_tool_reads_both_layouts_identically(tmp_path):
    def paths(root):
        return [str(root / f"processed_test_result/karaf/{pr}_build{b}/stage_single/test_class.csv.zip")
                for pr, b, _ in BUILDS]
    z, e = _root(tmp_path, "z", extracted=False), _root(tmp_path, "e", extracted=True)
    for test in ("a.T1", "a.T2", "b.T3", "missing"):
        assert HistoryRetrieval(paths(z), recent=3)(test) == HistoryRetrieval(paths(e), recent=3)(test)
    direct = str(e / "processed_test_result/karaf/PR-1_build2/stage_single/test_class.csv")
    assert read_test_class_zip(direct) == {"a.T1": (0, 1.0), "a.T2": (1, 0.5), "b.T3": (0, 2.0)}
