"""DANTE relevance signal (TF-IDF).

Mirrors TfidfRelevance (relevance_strategies.py) and the relevance block of
process_single_build (pipeline_orchestrator.py): the corpus is the token list
of every test class with non-empty tokens; for each changed file the diff
tokens are scored by cosine similarity, min-max normalised over the corpus
(0.5 for all if max == min), and stored per changed file. The per-test value
used for scoring is the max over changed files (calculate_all_scores).
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def min_max(scores):
    scores = np.asarray(scores, dtype=float)
    if scores.size == 0:
        return scores
    rng = scores.max() - scores.min()
    if rng > 1e-9:
        return (scores - scores.min()) / rng
    return np.full_like(scores, 0.5)


def relevance_per_file(test_tokens, diff_tokens_by_file):
    """test_tokens: {test: [tokens]}; diff_tokens_by_file: {path: [tokens]}.
    Returns {test: {path: normalised score}} for tests with non-empty tokens."""
    corpus_tests = [t for t, toks in test_tokens.items() if toks]
    if not corpus_tests:
        return {}
    vec = TfidfVectorizer()
    matrix = vec.fit_transform([" ".join(test_tokens[t]) for t in corpus_tests])
    out = {t: {} for t in corpus_tests}
    for path, toks in diff_tokens_by_file.items():
        if not toks:
            continue
        scores = cosine_similarity(vec.transform([" ".join(toks)]), matrix).flatten()
        for t, s in zip(corpus_tests, min_max(scores)):
            out[t][path] = float(s)
    return out


def max_relevance(per_file):
    return max(per_file.values()) if per_file else 0.0
