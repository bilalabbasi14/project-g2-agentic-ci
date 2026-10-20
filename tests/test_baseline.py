"""Hand-worked checks for the DANTE baseline port."""
import math

import pandas as pd
import pytest

from src.dante.history import (build_statistical_model, history_score, last_outcomes,
                               total_failures, wilson_interval)
from src.dante.relevance import max_relevance, min_max, relevance_per_file
from src.dante.selection import greedy_select, random_select
from src.dante.tokenize import clean_and_tokenize_source, find_test_source_path
from src.data.splitter import history_window, previous_builds


def test_wilson_interval_hand_computed():
    # p=0.5, n=20, z=1.96: denom=1.19208, centre=0.5+0.09604=0.59604,
    # spread=1.96*sqrt((0.25+0.048020)/20)=1.96*0.122070=0.239257
    lo, hi = wilson_interval(10, 20)
    assert lo == pytest.approx((0.59604 - 0.239257) / 1.19208, abs=1e-4)   # 0.29930
    assert hi == pytest.approx((0.59604 + 0.239257) / 1.19208, abs=1e-4)   # 0.70070
    assert wilson_interval(0, 0) == (0.0, 0.0)


def test_min_max():
    assert list(min_max([1.0, 3.0, 2.0])) == [0.0, 1.0, 0.5]
    assert list(min_max([0.2, 0.2])) == [0.5, 0.5]


def _frames(outcomes_per_build):
    return [pd.DataFrame({'testclass': list(b), 'outcome': list(b.values()), 'build_index': i})
            for i, b in enumerate(outcomes_per_build)]


def test_thfr_and_threshold():
    frames = _frames([{'A': 1, 'B': 0}, {'A': 0, 'B': 0}, {'A': 1, 'B': 1}, {'A': 0, 'B': 0}])
    m = build_statistical_model(frames, [1, 2], min_events=20)
    assert m['thfr'] == {'A': 0.5, 'B': 0.25}
    # fewer than 20 sticky events -> probability 0 for every window
    assert all(v['prob'] == 0.0 for v in m['p_fail_sticky_model'].values())
    assert total_failures(frames) == {'A': 2, 'B': 1}


def test_sticky_probability_window1():
    # one test, outcomes 1,1,0,1,1 ; shift(1) = nan,1,1,0,1 ; sticky rows: 2nd,3rd,5th
    # outcomes at sticky rows: 1,0,1 -> P = 2/3 (min_events=1)
    frames = _frames([{'A': o} for o in [1, 1, 0, 1, 1]])
    m = build_statistical_model(frames, [1], min_events=1)
    assert m['p_fail_sticky_model']['1']['prob'] == pytest.approx(2 / 3)
    assert m['p_fail_sticky_model']['1']['events'] == 3


def test_history_score_hand_computed():
    model = {'thfr': {'A': 0.1}, 'p_fail_sticky_model': {'1': {'prob': 0.6}, '2': {'prob': 0.4},
                                                         '3': {'prob': 0.3}}}
    # failed 1 and 3 builds ago: 0.1 + 0.6/1 + 0.3/3 = 0.8
    assert history_score('A', model, {1: 1, 2: 0, 3: 1}) == pytest.approx(0.8)
    assert history_score('Z', model, {}) == 0


def test_last_outcomes():
    prev = [{'A': 1}, {'A': 0, 'B': 1}]          # most recent first
    lo = last_outcomes(prev, [1, 2, 3])
    assert lo['A'] == {1: 1, 2: 0, 3: 0}
    assert lo['B'] == {1: 0, 2: 1, 3: 0}


def test_greedy_selection_skips_and_continues():
    df = pd.DataFrame({'s': [5.0, 4.0, 3.0, 2.0], 'duration': [6.0, 5.0, 4.0, 1.0]},
                      index=['a', 'b', 'c', 'd'])
    sel, order = greedy_select(df, 's', budget_seconds=11.0)
    # a(6) -> 6, b(5) -> 11, c(4) skipped, d(1) skipped (would be 12)
    assert order == ['a', 'b', 'c', 'd'] and sel == ['a', 'b']
    sel, _ = greedy_select(df, 's', budget_seconds=10.0)
    # a(6), b skipped (11), c(4) -> 10, d skipped
    assert sel == ['a', 'c']


def test_random_select_reproducible():
    df = pd.DataFrame({'duration': [1.0] * 10}, index=list('abcdefghij'))
    assert random_select(df, 3, 42) == random_select(df, 3, 42)
    assert len(random_select(df, 3, 42)[0]) == 3


def test_relevance_prefers_matching_test():
    rel = relevance_per_file({'T1': ['cache', 'evict'], 'T2': ['servlet', 'http'], 'T3': []},
                             {'Cache.java': ['cache', 'evict', 'size']})
    assert set(rel) == {'T1', 'T2'}                  # empty-token tests are not in the corpus
    assert rel['T1']['Cache.java'] == 1.0 and rel['T2']['Cache.java'] == 0.0
    assert max_relevance(rel['T1']) == 1.0 and max_relevance({}) == 0.0


def test_tokenizer_java():
    toks, methods = clean_and_tokenize_source(
        "// c\npublic class FooCacheTest { @Test public void evictsOld() { String s = \"hello world\"; } }",
        ".java")
    assert {'foo', 'cache', 'test', 'evicts', 'old', 'hello', 'world'} <= set(toks)
    assert 'public' not in toks and 'evictsold' in methods


def test_find_test_source_path():
    paths = ['a/src/main/java/org/x/FooTest.java', 'b/src/test/java/org/x/FooTest.java',
             '.git/FooTest.java', 'c/Bar.java']
    # equal package depth (2); the /test/ directory bonus (+0.5) picks b
    assert find_test_source_path(paths, 'org.x.FooTest') == 'b/src/test/java/org/x/FooTest.java'
    assert find_test_source_path(paths, 'org.x.FooTest$Inner') is not None
    assert find_test_source_path(paths, 'org.y.Missing') is None
    assert find_test_source_path(['k/FooTest.java'], 'z.FooTest') == 'k/FooTest.java'


def test_history_uses_only_earlier_builds():
    meta = pd.DataFrame({'timestamp_for_sort': [10, 20, 30, 30, 40, 50], 'key': list('abcdef')})
    h = history_window(meta, 30, 100)
    assert list(h['key']) == ['a', 'b']               # strictly earlier; equal timestamps excluded
    assert (h['timestamp_for_sort'] < 30).all()
    assert list(history_window(meta, 50, 2)['key']) == ['d', 'e']
    assert list(previous_builds(meta, 50, 2)['key']) == ['e', 'd']



def test_sticky_mode_dante_vs_per_test():
    frames = _frames([{'A': 1, 'B': 0}, {'A': 0, 'B': 0}, {'A': 1, 'B': 0}])
    dante = build_statistical_model(frames, [2], min_events=1, sticky_mode="dante")
    per_test = build_statistical_model(frames, [2], min_events=1, sticky_mode="per_test")
    assert dante['p_fail_sticky_model']['2']['events'] == 2
    assert dante['p_fail_sticky_model']['2']['prob'] == pytest.approx(0.0)
    assert per_test['p_fail_sticky_model']['2']['events'] == 2
    assert per_test['p_fail_sticky_model']['2']['prob'] == pytest.approx(0.5)


def test_sticky_modes_agree_for_a_single_test():
    frames = _frames([{'A': o} for o in [1, 0, 1, 1, 0]])
    dante = build_statistical_model(frames, [1, 2, 3], min_events=1, sticky_mode="dante")
    per_test = build_statistical_model(frames, [1, 2, 3], min_events=1, sticky_mode="per_test")
    assert dante['p_fail_sticky_model'] == per_test['p_fail_sticky_model']