import zipfile

import pandas as pd

from src.contracts import validate
from src.tools import TOOL_SPECS
from src.tools.diff_reader import DiffReader, split_diff
from src.tools.history_retrieval import HistoryRetrieval
from src.tools.registry import ToolRegistry

CSV = [
    "testclass,duration,outcome,last_outcome\n"
    "p.ATest,1.5,1,0\np.BTest,2.0,0,0\n,3.0,1,0\n",
    "testclass,duration,outcome,last_outcome\n"
    "p.ATest,1.0,0,1\np.CTest,,1,0\n",
]


def _zips(tmp_path):
    paths = []
    for i, text in enumerate(CSV):
        p = tmp_path / f"b{i}" / "test_class.csv.zip"
        p.parent.mkdir()
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("test_class.csv", text)
        paths.append(p)
    return paths


def _frames(tmp_path):
    import io
    return [pd.read_csv(io.StringIO(t)).assign(build_index=i) for i, t in enumerate(CSV)]


def test_from_frames_equals_zip_files(tmp_path):
    from_zip = HistoryRetrieval(_zips(tmp_path), recent=10)
    from_mem = HistoryRetrieval.from_frames(_frames(tmp_path), recent=10)
    for test in ("p.ATest", "p.BTest", "p.CTest", "p.Missing"):
        assert from_mem(test) == from_zip(test)
    assert from_mem("p.ATest")["failures"] == 1 and from_mem("p.ATest")["last_failure_distance"] == 2


DIFF = ("diff --git a/src/A.java b/src/A.java\n--- a/src/A.java\n+++ b/src/A.java\n@@ -1 +1 @@\n-old\n+new\n"
        "diff --git a/pom.xml b/pom.xml\n+<x/>\n")


def test_diff_reader_from_files_matches_file(tmp_path):
    path = tmp_path / "b.diff"
    path.write_text(DIFF, encoding="utf-8")
    from_file = DiffReader(path)
    from_mem = DiffReader.from_files(split_diff(DIFF))
    assert from_mem.list_files() == from_file.list_files() == ["src/A.java"]
    assert from_mem("src/A.java") == from_file("src/A.java")
    assert from_mem("nope.java") == {"file": "nope.java", "found": False}


def _registry(tmp_path, **kw):
    return ToolRegistry.for_build(_frames(tmp_path), split_diff(DIFF), **kw)


def test_specs_only_offer_allowed_tools(tmp_path):
    assert [s["name"] for s in _registry(tmp_path).specs()] == ["history_retrieval", "diff_reader"]
    assert [s["name"] for s in _registry(tmp_path, allowed=("diff_reader",)).specs()] == ["diff_reader"]
    assert "budget_tracker" in [s["name"] for s in TOOL_SPECS]   # exists, but never offered


def test_valid_calls(tmp_path):
    reg = _registry(tmp_path)
    h = reg.call("history_retrieval", {"test": "p.ATest"})
    assert h.ok and h.error is None and h.output["runs"] == 2 and h.latency_s >= 0
    d = reg.call("diff_reader", {"file": "src/A.java"})
    assert d.ok and d.output["found"] and d.output["added"] == 1
    for rec in (h, d):
        validate(rec.to_dict(), "tool_call_record")


def test_bad_calls_never_raise(tmp_path):
    reg = _registry(tmp_path, allowed=("history_retrieval",))
    cases = [("budget_tracker", {"test": "x", "duration": 1.0}),   # exists but not offered
             ("diff_reader", {"file": "src/A.java"}),               # not allowed here
             ("no_such_tool", {}),
             ("history_retrieval", {}),                              # missing argument
             ("history_retrieval", {"test": 5}),                     # wrong type
             ("history_retrieval", "p.ATest")]                       # args not an object
    for name, args in cases:
        rec = reg.call(name, args)
        assert rec.ok is False and rec.error and rec.output == {}
        validate(rec.to_dict(), "tool_call_record")


def test_exception_inside_tool_is_caught(tmp_path):
    reg = _registry(tmp_path)

    def boom(_):
        raise RuntimeError("disk on fire")

    reg.tools["history_retrieval"] = boom
    rec = reg.call("history_retrieval", {"test": "p.ATest"})
    assert rec.ok is False and "disk on fire" in rec.error
