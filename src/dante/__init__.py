"""DANTE baseline: history + TF-IDF relevance, CCH ranking, greedy budget selection.

    scores(build, history, cfg, method)                -> DataFrame; history_score and
                                                          tfidf_relevance are separate columns
    rank(build, history, budget_fraction, cfg, method) -> (selected, ordered, scores_df)

Methods
  DANTE-CCH          base = 1.0*history + 0.5*tfidf**1.2, value = base*max(fails,0.1)/duration
  DANTE-CCH-shipped  same with relevance weight 0. In the shipped run_selection.py,
                     relevance is read under key "bm25" (experiment_config.RELEVANCE_STRATEGY_KEY)
                     while pipeline_orchestrator.py stores it under "tfidf", so relevance is 0.
  History-only       rank by the history score alone
  TF-IDF-only        rank by max TF-IDF relevance alone
  Random             pandas sample(frac=1, random_state=42)
All methods use the same greedy budget fill (skip what does not fit, keep scanning).
"""
from src.dante.scoring import score_table
from src.dante.selection import greedy_select, random_select

METHODS = ("DANTE-CCH", "DANTE-CCH-shipped", "History-only", "TF-IDF-only", "Random")

RANK_COLUMN = {
    "DANTE-CCH": "dante_cch_score",
    "DANTE-CCH-shipped": "dante_cch_score",
    "History-only": "history_score",
    "TF-IDF-only": "tfidf_relevance",
}


def scores(build, history, cfg, method="DANTE-CCH", relevance_override=None, w_relevance=None):
    d, h = cfg["dante"], cfg["history"]
    if w_relevance is None:
        w_relevance = 0.0 if method == "DANTE-CCH-shipped" else d["weight_relevance"]
    df, _ = score_table(build, history, h["lookback_windows"], h["min_sticky_events"],
                        d["weight_history"], w_relevance, d["relevance_power"], relevance_override)
    return df


def budget_seconds(build, fraction):
    """Budget = fraction of the summed duration of all test cases in the build (run_selection.main)."""
    return build.total_duration_all() * fraction


def rank(build, history, budget_fraction, cfg, method="DANTE-CCH", relevance_override=None, df=None):
    if df is None:
        df = scores(build, history, cfg, method, relevance_override)
    if df is None or df.empty:
        return [], [], df
    budget = budget_seconds(build, budget_fraction)
    if method == "Random":
        sel, order = random_select(df, budget, cfg["dante"]["random_seed"])
    else:
        sel, order = greedy_select(df, RANK_COLUMN.get(method, "dante_cch_score"), budget)
    return sel, order, df
