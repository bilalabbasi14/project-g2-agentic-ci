import zipfile

import pytest

from src.agent.shortlister import shortlist
from src.tools import TOOL_SPECS, BudgetTracker, DiffReader, HistoryRetrieval, split_diff

DIFF = """diff --git a/pom.xml b/pom.xml
index 1111111..2222222 100644
--- a/pom.xml
+++ b/pom.xml
@@ -1 +1 @@
-<v>1</v>
+<v>2</v>
diff --git a/core/src/main/java/a/Foo.java b/core/src/main/java/a/Foo.java
index 3333333..4444444 100644
--- a/core/src/main/java/a/Foo.java
+++ b/core/src/main/java/a/Foo.java
@@ -1,3 +1,3 @@
 class Foo {
-  int x = 1;
+  int x = 2;
+  int y = 3;
 }
"""


def _zip(path, rows):
    with zipfile.ZipFile(path, "w") as z:
        body = "testclass,duration,outcome,last_outcome\n" + "".join(f"{t},{d},{o},0\n" for t, d, o in rows)
        z.writestr("test_class.csv", body)
    return path


def test_shortlist_union_and_order():
    hist = {"A": 0.9, "B": 0.5, "C": 0.0, "D": 0.1}
    tfidf = {"A": 0.1, "B": 0.0, "C": 0.8, "D": 0.7}
    # top-2 history: A, B ; top-2 tfidf: C, D
    assert shortlist(hist, tfidf, 2) == ["A", "C", "B", "D"]
    assert shortlist(hist, tfidf, 0) == []


def test_shortlist_ignores_zero_scores():
    assert shortlist({"A": 0.0, "B": 0.0}, {"A": 0.0, "B": 0.3}, 5) == ["B"]


def test_split_diff_filters_extensions_and_counts():
    files = split_diff(DIFF)
    assert list(files) == ["core/src/main/java/a/Foo.java"]
    f = files["core/src/main/java/a/Foo.java"]
    assert (f["added"], f["removed"]) == (2, 1)
    assert f["changed_lines"] == "  int x = 1;\n  int x = 2;\n  int y = 3;"


def test_diff_reader(tmp_path):
    p = tmp_path / "x.diff"
    p.write_text(DIFF)
    r = DiffReader(p)
    assert r.list_files() == ["core/src/main/java/a/Foo.java"]
    assert r("core/src/main/java/a/Foo.java")["found"] is True
    assert r("pom.xml") == {"file": "pom.xml", "found": False}


def test_history_retrieval(tmp_path):
    paths = [
        _zip(tmp_path / "b1.zip", [("T1", 1.0, 1), ("T2", 2.0, 0)]),
        _zip(tmp_path / "b2.zip", [("T1", 1.0, 0)]),
        _zip(tmp_path / "b3.zip", [("T1", 1.0, 1), ("T2", 2.0, 0)]),
        _zip(tmp_path / "b4.zip", [("T1", 1.0, 0), ("T2", 2.0, 0)]),
    ]
    h = HistoryRetrieval(paths, recent=3)
    t1 = h("T1")
    assert t1["runs"] == 4 and t1["failures"] == 2 and t1["failure_rate"] == 0.5
    assert t1["last_failure_distance"] == 2
    assert t1["recent_outcomes"] == [0, 1, 0]
    t2 = h("T2")
    assert t2["runs"] == 3 and t2["failures"] == 0 and t2["last_failure_distance"] is None
    assert t2["recent_outcomes"] == [None, 0, 0]
    assert h("missing")["runs"] == 0


def test_budget_tracker_skips_and_continues():
    b = BudgetTracker(10)
    sel = b.fill(["a", "b", "c", "d"], {"a": 4, "b": 7, "c": 6, "d": 1})
    # a(4) fits, b(7) would exceed, c(6) fits exactly at 10, d(1) does not fit
    assert sel == ["a", "c"]
    assert b.remaining == 0
    with pytest.raises(ValueError):
        BudgetTracker(-1)


def test_tool_specs_named():
    assert [t["name"] for t in TOOL_SPECS] == ["history_retrieval", "diff_reader", "budget_tracker"]
