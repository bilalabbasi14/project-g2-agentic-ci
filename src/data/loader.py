"""LRTS loader: per-build tables in chronological order.

Layout (checked on the extracted dataset; there is no "artifact/" folder):
    <lrts_root>/dataset.csv
    <lrts_root>/processed_test_result/<project>/<pr_name>_build<id>/stage_<stage>/test_class.csv.zip
        (the Kaggle copy has the extracted stage_<stage>/test_class.csv instead; both are read)
    <lrts_root>/shadata/<project>/diff/<pr_name>_build<id>.diff
test_class.csv columns: testclass, duration, outcome (1 = fail), last_outcome.
LRTS has no per-test flaky label in these files.
"""
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd

from src.dante.tokenize import clean_and_tokenize_source, find_test_source_path
from src.data.splitter import history_window, previous_builds
from src.tools.diff_reader import split_diff
from src.tools.history_retrieval import open_test_class_csv, resolve_test_class_file

STORED_NAME = re.compile(r"(?P<project>[\w-]+?)_build_(?P<pr>.+)_(?P<bid>\d+)_(?P<stage>[^_]+)_"
                         r"(?P<strategy>tfidf|bm25)_(?P<tok>specific|generic)_boosted_(?P<boost>True|False)")


def parse_stored_build_name(name):
    """'karaf_build_PR-1840_4_single_tfidf_specific_boosted_False' -> ('karaf', 'PR-1840', 4, 'single')."""
    m = STORED_NAME.fullmatch(name)
    if not m:
        raise ValueError(f"unrecognised build name: {name}")
    return m["project"], m["pr"], int(m["bid"]), m["stage"]


def build_key(pr_name, build_id):
    return f"{str(pr_name).replace('/', '_')}_build{build_id}"


@dataclass
class TestCase:
    __test__ = False          # not a pytest test class
    name: str
    duration: float
    outcome: int
    source_path: Optional[str] = None
    tokens: Optional[List[str]] = None

    @property
    def source_found(self):
        return self.tokens is not None


@dataclass
class BuildData:
    key: str
    pr_name: str
    build_id: int
    stage_id: str
    sha: str
    timestamp: float
    test_cases: Dict[str, TestCase]
    diff_text: str
    diff_files: Dict[str, dict]
    diff_tokens: Dict[str, List[str]]
    sources_available: bool = True
    source_texts: Dict[str, str] = field(default_factory=dict)

    def candidates(self):
        """DANTE candidates: source file found and duration > 0 (calculate_all_scores)."""
        return [t for t in self.test_cases.values() if t.source_found and t.duration > 0]

    def total_duration_all(self):
        """Budget base used by run_selection.main: sum over all test cases in the build."""
        return sum(t.duration for t in self.test_cases.values())


@dataclass
class HistoryData:
    frames: List[pd.DataFrame]                 # history builds, oldest first, with 'build_index'
    keys: List[str]
    previous_outcomes: List[Dict[str, int]]    # most recent first, for last_outcome_n


class LRTSLoader:
    def __init__(self, lrts_root, project, source_repo=None):
        self.root = lrts_root
        self.project = project
        self.repo = source_repo
        self.meta = self._load_metadata()
        self._cache = {}

    def _load_metadata(self):
        df = pd.read_csv(os.path.join(self.root, "dataset.csv"), low_memory=False)
        df = df[df['project'].str.lower() == self.project.lower()].copy()
        df['timestamp_for_sort'] = pd.to_numeric(df['build_timestamp'], errors='coerce').fillna(0)
        df = df.sort_values(by='timestamp_for_sort', ascending=True).reset_index(drop=True)
        df['key'] = [build_key(p, b) for p, b in zip(df['pr_name'], df['build_id'])]
        return df

    def row(self, pr_name, build_id, stage_id="single"):
        m = self.meta[(self.meta['pr_name'] == pr_name) & (self.meta['build_id'] == int(build_id))
                      & (self.meta['stage_id'] == stage_id)]
        if m.empty:
            raise KeyError(f"{pr_name} build {build_id} stage {stage_id} not in dataset.csv")
        return m.iloc[0]

    def test_class_path(self, row):
        return os.path.join(self.root, "processed_test_result", self.project,
                            build_key(row['pr_name'], row['build_id']), f"stage_{row['stage_id']}",
                            "test_class.csv.zip")

    def diff_path(self, row):
        return os.path.join(self.root, "shadata", self.project, "diff",
                            build_key(row['pr_name'], row['build_id']) + ".diff")

    def test_class_df(self, row):
        """Raw test_class.csv with 'build_index' = chronological position
        (_load_single_test_class_zip in run_selection.py). None if missing."""
        key = row.name
        if key not in self._cache:
            # the .zip, or the extracted test_class.csv that Kaggle serves instead
            path = resolve_test_class_file(self.test_class_path(row))
            df = None
            if path:
                with open_test_class_csv(path) as fh:
                    df = pd.read_csv(fh)
                df['build_index'] = row.name
            self._cache[key] = df
        return self._cache[key]

    def history(self, row, num_builds=100, lookback=10):
        hist = history_window(self.meta, row['timestamp_for_sort'], num_builds)
        frames = [self.test_class_df(r) for _, r in hist.iterrows()]
        prev = previous_builds(self.meta, row['timestamp_for_sort'], lookback)
        prev_out = []
        for _, r in prev.iterrows():
            df = self.test_class_df(r)
            prev_out.append({} if df is None else dict(zip(df['testclass'], df['outcome'])))
        return HistoryData(frames=[f for f in frames if f is not None], keys=list(hist['key']),
                           previous_outcomes=prev_out)

    def build(self, row, keep_sources=False):
        """Assemble the target build: test cases (with source lookup + tokens), diff and diff tokens."""
        df = self.test_class_df(row)
        if df is None:
            raise FileNotFoundError(self.test_class_path(row))
        with open(self.diff_path(row), "r", encoding="utf-8", errors="ignore") as f:
            diff_text = f.read()
        diff_files = split_diff(diff_text)
        diff_tokens = {p: clean_and_tokenize_source(v["changed_lines"], os.path.splitext(p)[1])[0]
                       for p, v in diff_files.items()}

        cases = {}
        for _, r in df.iterrows():
            fqn = r['testclass']
            if pd.isna(fqn):
                continue
            cases[fqn] = TestCase(name=fqn, duration=float(r['duration']), outcome=int(r['outcome']))

        sources_ok = False
        texts = {}
        if self.repo is not None and self.repo.ensure_commit(row['build_head_sha']):
            sources_ok = True
            tree = self.repo.tree(row['build_head_sha'])
            paths = list(tree)
            for t in cases.values():
                t.source_path = find_test_source_path(paths, t.name)
            blobs = self.repo.read_blobs([tree[t.source_path] for t in cases.values() if t.source_path])
            for t in cases.values():
                if t.source_path:
                    code = blobs.get(tree[t.source_path])
                    if code:
                        t.tokens = clean_and_tokenize_source(code, os.path.splitext(t.source_path)[1])[0]
                        if keep_sources:
                            texts[t.name] = code
        return BuildData(key=row['key'], pr_name=row['pr_name'], build_id=int(row['build_id']),
                         stage_id=row['stage_id'], sha=row['build_head_sha'],
                         timestamp=float(row['timestamp_for_sort']), test_cases=cases,
                         diff_text=diff_text, diff_files=diff_files, diff_tokens=diff_tokens,
                         sources_available=sources_ok, source_texts=texts)
