"""Candidate shortlister: which tests are worth an LLM relevance call.

Union of the top-K tests by history score and the top-K by TF-IDF score.
Scores are passed in (computed by the baseline); tests with a score of 0 in a
list are not taken from that list, so ties at zero do not fill the shortlist.
"""


def _top_k(scores, k):
    ranked = sorted(((s, name) for name, s in scores.items() if s > 0), key=lambda x: (-x[0], x[1]))
    return [name for _, name in ranked[:k]]


def shortlist(history_scores, tfidf_scores, k):
    """Return shortlisted test names ordered by best rank in either list, then by name."""
    if k <= 0:
        return []
    rank = {}
    for lst in (_top_k(history_scores, k), _top_k(tfidf_scores, k)):
        for i, name in enumerate(lst):
            rank[name] = min(rank.get(name, i), i)
    return sorted(rank, key=lambda n: (rank[n], n))
