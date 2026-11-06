"""Test-source cache, so runs need no git clone (P2-09).

    python -m src.data.source_cache --eval data_eval/eval_builds_p2.csv data_eval/eval_builds.csv \
        [--out <dir>] [--force] [--check 3]

For every build key in the given CSVs (deduplicated) it loads the build through
the git clone (`LRTSLoader.build(row, keep_sources=True)`) and writes
`<out>/<build_key>.json.gz` (gzip, UTF-8 JSON):

    {"build_key": ..., "sha": ..., "sources_available": bool,
     "sources": {"<test class>": {"path": "<repo path>", "text": "<source code>"}, ...}}

with one entry for every test case whose source path was found. Existing files
are skipped unless --force is given (resumable). LRTSLoader(source_cache_dir=...)
reads these files instead of git and produces the same BuildData. Because
Kaggle unpacks compressed files on upload, a plain `<build_key>.json` and a
folder `<build_key>.json/` or `<build_key>.json.gz/` holding the entry are read
too (see cache_file; the folder form is what Kaggle produced).

--check K loads the first K builds once through git and once through the
cache and prints whether the BuildData are identical.
"""
import argparse
import gzip
import json
import os
import sys
from pathlib import Path

import pandas as pd

from src.settings import load_config, repo_path


def cache_dir_from_config(cfg):
    """cfg["paths_p2"]["source_cache"] as a Path, or None when missing or empty (= no cache)."""
    value = (cfg.get("paths_p2") or {}).get("source_cache")
    if not value or not str(value).strip():
        return None
    return repo_path(str(value).strip())


def cache_file(cache_dir, build_key):
    """The cache file of a build, or None. Accepted forms, in this order:
    - a file `<key>.json.gz` (as written) or `<key>.json` (unpacked);
    - a folder `<key>.json/` or `<key>.json.gz/` holding the entry. This is how
      Kaggle unpacks an uploaded `.json.gz`: on 6 Nov 2026 every
      `<key>.json.gz` became a folder `<key>.json/` holding one file named after
      the gzip header (`<key>.json.gz.tmp`). Inside the folder, `<key>.json` is
      taken if present, otherwise its only file, whatever its name.
    read_cache recognises gzip by content, so the inner file may be either."""
    if cache_dir is None:
        return None
    base = Path(cache_dir)
    names = (f"{build_key}.json.gz", f"{build_key}.json")
    for name in names:
        p = base / name
        if p.is_file():
            return p
    for name in names:
        folder = base / name
        if folder.is_dir():
            inside = folder / f"{build_key}.json"
            if inside.is_file():
                return inside
            files = sorted(p for p in folder.iterdir() if p.is_file())
            if len(files) == 1:
                return files[0]
    return None


GZIP_MAGIC = b"\x1f\x8b"


def read_cache(path):
    """Read a cache file; gzip is recognised by its content, not its name."""
    path = Path(path)
    with open(path, "rb") as f:
        gzipped = f.read(2) == GZIP_MAGIC
    if gzipped:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cache_entry(build):
    """The cache content of a BuildData loaded with keep_sources=True."""
    return {"build_key": build.key, "sha": build.sha, "sources_available": bool(build.sources_available),
            "sources": {t.name: {"path": t.source_path, "text": build.source_texts.get(t.name, "")}
                        for t in build.test_cases.values() if t.source_path}}


def write_cache(path, entry):
    """Write atomically (temp file + rename) so an interrupted run leaves no half file.
    The gzip header stores the name `<key>.json` (not the temp name) and mtime 0,
    so a tool that unpacks the file gets `<key>.json` and the bytes are reproducible."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    inner = path.name[:-3] if path.name.endswith(".gz") else path.name
    with open(tmp, "wb") as raw, gzip.GzipFile(filename=inner, mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(json.dumps(entry, ensure_ascii=False).encode("utf-8"))
    os.replace(tmp, path)


def eval_keys(csv_paths):
    """Build keys from the evaluation CSVs, deduplicated, in first-seen order."""
    keys = []
    for p in csv_paths:
        keys += pd.read_csv(repo_path(p))["key"].tolist()
    return list(dict.fromkeys(keys))


def build_cache(loader, keys, out_dir, force=False, echo=print):
    """Write one cache file per key. Returns a summary dict."""
    out_dir = Path(out_dir)
    rows = loader.meta.set_index("key")
    summary = {"builds": len(keys), "written": 0, "skipped_existing": 0, "missing_in_dataset": 0,
               "without_sources": 0, "tests_with_source": 0}
    for i, key in enumerate(keys, 1):
        target = out_dir / f"{key}.json.gz"
        if target.exists() and not force:
            summary["skipped_existing"] += 1
            echo(f"{i}/{len(keys)} {key} skipped (exists)")
            continue
        if key not in rows.index:
            summary["missing_in_dataset"] += 1
            echo(f"{i}/{len(keys)} {key} not in dataset.csv")
            continue
        row = loader.meta[loader.meta["key"] == key].iloc[0]
        entry = cache_entry(loader.build(row, keep_sources=True))
        write_cache(target, entry)
        summary["written"] += 1
        summary["tests_with_source"] += len(entry["sources"])
        if not entry["sources_available"]:
            summary["without_sources"] += 1
        echo(f"{i}/{len(keys)} {key} {len(entry['sources'])}")
    return summary


def build_signature(build):
    """Everything the cache must reproduce, for comparing two BuildData."""
    return {"key": build.key, "sources_available": build.sources_available,
            "test_cases": {n: (t.duration, t.outcome, t.source_path, t.tokens) for n, t in build.test_cases.items()},
            "source_texts": dict(build.source_texts), "diff_tokens": build.diff_tokens}


def check(git_loader, cache_loader, keys):
    """[(key, identical)] comparing BuildData from git and from the cache."""
    out = []
    for key in keys:
        row = git_loader.meta[git_loader.meta["key"] == key].iloc[0]
        a = build_signature(git_loader.build(row, keep_sources=True))
        b = build_signature(cache_loader.build(row, keep_sources=True))
        out.append((key, a == b, len(a["test_cases"]), sum(1 for v in a["test_cases"].values() if v[3])))
    return out


def main(argv=None):
    from src.data.loader import LRTSLoader
    from src.data.sources import SourceRepo
    ap = argparse.ArgumentParser(description="Precompute test sources for the evaluation builds.")
    ap.add_argument("--eval", nargs="+", required=True, help="evaluation CSVs with a 'key' column")
    ap.add_argument("--out", help="cache folder (default: paths_p2.source_cache)")
    ap.add_argument("--force", action="store_true", help="rewrite existing files")
    ap.add_argument("--check", type=int, default=0, metavar="K",
                    help="afterwards, compare git and cache BuildData for the first K builds")
    args = ap.parse_args(argv)
    cfg = load_config()
    p = cfg["paths"]
    out = Path(args.out) if args.out else cache_dir_from_config(cfg)
    if out is None:
        raise SystemExit("no --out and no paths_p2.source_cache in the config")
    keys = eval_keys(args.eval)
    git_loader = LRTSLoader(p["lrts_root"], cfg["project"], SourceRepo(p["repo_clone"], p["repo_url"]))
    s = build_cache(git_loader, keys, out, args.force)
    print(f"summary: {len(keys)} builds; written {s['written']}, skipped (existing) {s['skipped_existing']}, "
          f"not in dataset.csv {s['missing_in_dataset']}, without sources {s['without_sources']}, "
          f"tests with source (written files) {s['tests_with_source']} -> {out}")
    if args.check:
        cache_loader = LRTSLoader(p["lrts_root"], cfg["project"], None, source_cache_dir=out)
        results = check(git_loader, cache_loader, keys[:args.check])
        for key, same, n, n_tok in results:
            print(f"check {key}: {'identical' if same else 'DIFFERENT'} ({n} test cases, {n_tok} with tokens)")
        if not all(r[1] for r in results):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
