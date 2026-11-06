"""Source cache (P2-09): the cache gives the same BuildData as the git clone (no real data, no git)."""
import gzip
import json
import zipfile

from src.data import source_cache as sc
from src.data.loader import LRTSLoader

SHA = "a" * 40
KEY = "PR-7_build3"
CSV = ("testclass,duration,outcome,last_outcome\n"
       "org.x.FooTest,2.0,1,0\norg.x.BarTest,1.0,0,0\norg.y.EmptyTest,1.0,0,0\norg.z.MissingTest,3.0,0,0\n")
DIFF = "diff --git a/src/org/x/Foo.java b/src/org/x/Foo.java\n--- a/src/org/x/Foo.java\n+++ b/src/org/x/Foo.java\n" \
       "@@ -1 +1 @@\n-int foo() { return 1; }\n+int foo() { return cacheLookup(2); }\n"


class FakeRepo:
    """ensure_commit / tree / read_blobs with fixed content; counts calls."""

    def __init__(self, available=True):
        self.available = available
        self.calls = 0
        self.files = {"src/test/org/x/FooTest.java": ("o1", "class FooTest { void testCacheLookup() { foo(); } }"),
                      "src/test/org/x/BarTest.java": ("o2", "class BarTest { void bar() {} }"),
                      "src/test/org/y/EmptyTest.java": ("o3", ""),
                      "src/main/org/x/Foo.java": ("o4", "class Foo {}")}

    def ensure_commit(self, sha):
        self.calls += 1
        return self.available

    def tree(self, sha):
        return {p: oid for p, (oid, _) in self.files.items()}

    def read_blobs(self, oids):
        texts = {oid: t for oid, t in self.files.values()}
        return {o: texts[o] for o in oids if texts[o] is not None}


def _lrts(tmp_path):
    root = tmp_path / "lrts"
    (root / "shadata" / "karaf" / "diff").mkdir(parents=True)
    (root / "dataset.csv").write_text("project,pr_name,build_id,stage_id,build_timestamp,build_head_sha\n"
                                      f"karaf,PR-7,3,single,100.0,{SHA}\n")
    d = root / "processed_test_result" / "karaf" / KEY / "stage_single"
    d.mkdir(parents=True)
    with zipfile.ZipFile(d / "test_class.csv.zip", "w") as z:
        z.writestr("test_class.csv", CSV)
    (root / "shadata" / "karaf" / "diff" / f"{KEY}.diff").write_text(DIFF)
    return str(root)


def _row(loader):
    return loader.meta.iloc[0]


def test_cache_equals_git(tmp_path):
    root, out = _lrts(tmp_path), tmp_path / "cache"
    git = LRTSLoader(root, "karaf", FakeRepo())
    summary = sc.build_cache(git, [KEY], out, echo=lambda *_: None)
    assert summary["written"] == 1 and summary["tests_with_source"] == 3   # MissingTest has no file
    with gzip.open(out / f"{KEY}.json.gz", "rt", encoding="utf-8") as f:
        entry = json.load(f)
    assert entry["build_key"] == KEY and entry["sha"] == SHA and entry["sources_available"] is True
    assert entry["sources"]["org.x.FooTest"]["path"] == "src/test/org/x/FooTest.java"

    repo = FakeRepo()
    cached = LRTSLoader(root, "karaf", repo, source_cache_dir=out)
    for keep in (True, False):
        a = sc.build_signature(LRTSLoader(root, "karaf", FakeRepo()).build(_row(git), keep_sources=keep))
        b = sc.build_signature(cached.build(_row(cached), keep_sources=keep))
        assert a == b
    assert repo.calls == 0                       # the cache was used, not the repo
    a = git.build(_row(git), keep_sources=True)
    assert a.test_cases["org.x.FooTest"].tokens and a.test_cases["org.y.EmptyTest"].tokens is None
    assert a.test_cases["org.y.EmptyTest"].source_path and a.test_cases["org.z.MissingTest"].source_path is None
    assert sc.check(git, cached, [KEY])[0][1] is True


def test_plain_json_is_read_too(tmp_path):
    root, out = _lrts(tmp_path), tmp_path / "cache"
    git = LRTSLoader(root, "karaf", FakeRepo())
    sc.build_cache(git, [KEY], out, echo=lambda *_: None)
    gz = out / f"{KEY}.json.gz"
    with gzip.open(gz, "rt", encoding="utf-8") as f:
        (out / f"{KEY}.json").write_text(f.read(), encoding="utf-8")   # as if Kaggle unpacked it
    gz.unlink()
    cached = LRTSLoader(root, "karaf", None, source_cache_dir=out)
    assert sc.build_signature(cached.build(_row(cached), True)) == sc.build_signature(git.build(_row(git), True))


def test_missing_cache_file_falls_back_to_repo(tmp_path):
    root = _lrts(tmp_path)
    repo = FakeRepo()
    loader = LRTSLoader(root, "karaf", repo, source_cache_dir=tmp_path / "empty")
    b = loader.build(_row(loader), keep_sources=True)
    assert repo.calls == 1 and b.sources_available and b.test_cases["org.x.FooTest"].tokens


def test_neither_cache_nor_repo_means_no_sources(tmp_path):
    root = _lrts(tmp_path)
    for loader in (LRTSLoader(root, "karaf"), LRTSLoader(root, "karaf", FakeRepo(available=False))):
        b = loader.build(_row(loader), keep_sources=True)
        assert b.sources_available is False and b.source_texts == {}
        assert all(t.tokens is None for t in b.test_cases.values())


def test_unavailable_commit_is_cached_as_no_sources(tmp_path):
    root, out = _lrts(tmp_path), tmp_path / "cache"
    s = sc.build_cache(LRTSLoader(root, "karaf", FakeRepo(available=False)), [KEY], out, echo=lambda *_: None)
    assert s["without_sources"] == 1
    cached = LRTSLoader(root, "karaf", FakeRepo(), source_cache_dir=out)
    assert cached.build(_row(cached)).sources_available is False


def test_second_run_skips_existing_unless_forced(tmp_path):
    root, out = _lrts(tmp_path), tmp_path / "cache"
    git = LRTSLoader(root, "karaf", FakeRepo())
    assert sc.build_cache(git, [KEY], out, echo=lambda *_: None)["written"] == 1
    lines = []
    s = sc.build_cache(git, [KEY, "PR-9_build1"], out, echo=lines.append)
    assert s["written"] == 0 and s["skipped_existing"] == 1 and s["missing_in_dataset"] == 1
    assert lines[0] == f"1/2 {KEY} skipped (exists)"
    assert sc.build_cache(git, [KEY], out, force=True, echo=lambda *_: None)["written"] == 1


def test_eval_keys_dedup_and_config_dir(tmp_path):
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    a.write_text("key,x\nK1,1\nK2,2\n")
    b.write_text("key\nK2\nK3\n")
    assert sc.eval_keys([a, b]) == ["K1", "K2", "K3"]
    assert sc.cache_dir_from_config({}) is None
    assert sc.cache_dir_from_config({"paths_p2": {"source_cache": "  "}}) is None
    assert sc.cache_dir_from_config({"paths_p2": {"source_cache": str(tmp_path)}}) == tmp_path


def test_three_cache_forms_give_identical_builddata(tmp_path):
    """<key>.json.gz (as written), <key>.json (unpacked) and a folder <key>.json.gz/ holding the JSON."""
    root = _lrts(tmp_path)
    git = LRTSLoader(root, "karaf", FakeRepo())
    gz_dir = tmp_path / "gz"
    sc.build_cache(git, [KEY], gz_dir, echo=lambda *_: None)
    with gzip.open(gz_dir / f"{KEY}.json.gz", "rt", encoding="utf-8") as f:
        text = f.read()
    plain_dir = tmp_path / "plain"
    plain_dir.mkdir()
    (plain_dir / f"{KEY}.json").write_text(text, encoding="utf-8")
    folder_dir = tmp_path / "folder"
    (folder_dir / f"{KEY}.json.gz").mkdir(parents=True)
    (folder_dir / f"{KEY}.json.gz" / f"{KEY}.json").write_text(text, encoding="utf-8")
    odd_dir = tmp_path / "odd"                      # folder form with another file name inside
    (odd_dir / f"{KEY}.json.gz").mkdir(parents=True)
    (odd_dir / f"{KEY}.json.gz" / "data").write_text(text, encoding="utf-8")

    expected = sc.build_signature(git.build(_row(git), keep_sources=True))
    for d in (gz_dir, plain_dir, folder_dir, odd_dir):
        repo = FakeRepo()
        loader = LRTSLoader(root, "karaf", repo, source_cache_dir=d)
        assert sc.cache_file(d, KEY) is not None
        assert sc.build_signature(loader.build(_row(loader), keep_sources=True)) == expected, d.name
        assert repo.calls == 0, d.name                # read from the cache, not from git
    assert sc.cache_file(tmp_path / "missing", KEY) is None


def test_real_kaggle_layout_folder_named_json(tmp_path):
    """The layout Kaggle produced on 6 Nov 2026 from the uploaded zip:
    /kaggle/input/datasets/<user>/g2-source-cache/g2-source-cache/<key>.json/<key>.json.gz.tmp
    (each .json.gz unpacked into a folder named <key>.json holding one file named after the gzip header)."""
    root = _lrts(tmp_path)
    git = LRTSLoader(root, "karaf", FakeRepo())
    written = tmp_path / "written"
    sc.build_cache(git, [KEY], written, echo=lambda *_: None)
    gz_bytes = (written / f"{KEY}.json.gz").read_bytes()
    expected = sc.build_signature(git.build(_row(git), keep_sources=True))
    for label, content in (("unpacked", gzip.decompress(gz_bytes)), ("still-gzipped", gz_bytes)):
        mount = tmp_path / label / "g2-source-cache" / "g2-source-cache"
        (mount / f"{KEY}.json").mkdir(parents=True)
        (mount / f"{KEY}.json" / f"{KEY}.json.gz.tmp").write_bytes(content)
        repo = FakeRepo()
        loader = LRTSLoader(root, "karaf", repo, source_cache_dir=mount)
        b = loader.build(_row(loader), keep_sources=True)
        assert b.sources_available and sc.build_signature(b) == expected, label
        assert repo.calls == 0, label
    empty = tmp_path / "empty" / f"{KEY}.json"          # a folder with two files is ambiguous: not used
    empty.mkdir(parents=True)
    (empty / "a").write_text("{}")
    (empty / "b").write_text("{}")
    assert sc.cache_file(empty.parent, KEY) is None


def test_written_gzip_header_names_the_json(tmp_path):
    root = _lrts(tmp_path)
    sc.build_cache(LRTSLoader(root, "karaf", FakeRepo()), [KEY], tmp_path / "c", echo=lambda *_: None)
    data = (tmp_path / "c" / f"{KEY}.json.gz").read_bytes()
    assert data[:2] == b"\x1f\x8b" and data[3] & 0x08                     # FNAME flag set
    assert data[10:data.index(b"\x00", 10)] == f"{KEY}.json".encode()      # not the .tmp name
    assert data[4:8] == b"\x00\x00\x00\x00"                                # mtime 0: reproducible bytes
