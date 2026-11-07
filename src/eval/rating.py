"""Explanation rating sheets and agreement (Gap 2, RQ2; docs/PROJECT_CONTEXT.md §8).

Three steps, run one after another:

    python -m src.eval.rating sample --run-dir results/E3_test_seed1 --n 100 --seed 42
        Draws the sample from <run-dir>/explanations.csv (format in src/pipeline.py;
        only rows with ok == True and method == "Full system"), stratified by budget,
        and writes rating_items.csv, rating_items.md (what raters read) and the blank
        sheets ratings_ali.csv and ratings_bilal.csv.
    python -m src.eval.rating agreement
        Checks both filled sheets, computes raw agreement and Cohen's kappa, and writes
        agreement.md, disagreements.csv and ratings_final.csv (agreed ratings filled in,
        final_rating empty for disagreements).
    python -m src.eval.rating final
        Reads ratings_final.csv after the discussion and writes rating_summary.csv/.md:
        shares sound / partly / unsound overall and per budget, kappa, and whether the
        RQ2 condition (share sound >= 0.80) holds.

All files go to results/gap2/ unless --out / --dir says otherwise.
"""
import argparse
import csv
import json
import logging
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from src.settings import repo_path

log = logging.getLogger(__name__)

RATINGS = ("sound", "partly", "unsound")
RATERS = ("ali", "bilal")
METHOD = "Full system"
RQ2_SOUND_SHARE = 0.80            # §8: RQ2 needs >= 80% of the sampled justifications rated sound
DEFAULT_DIR = "results/gap2"
DEFAULT_BUDGETS = (0.05, 0.10, 0.20)

ITEM_COLUMNS = ["item_id", "build", "budget", "test", "justification", "cited_facts", "evidence"]
SHEET_COLUMNS = ["item_id", "rating", "note"]
DISAGREEMENT_COLUMNS = ["item_id", "rating_ali", "rating_bilal"]
FINAL_COLUMNS = ["item_id", "rating_ali", "rating_bilal", "final_rating"]
SUMMARY_COLUMNS = ["scope", "budget", "n", "share_sound", "share_partly", "share_unsound", "kappa",
                   "rq2_sound_condition_holds"]

# copied from docs/PROJECT_CONTEXT.md §8 ("Explanation rating")
RATING_RULE = (
    "rate every one independently as *sound*, *partly sound* or *unsound*, using this rule: **sound** = "
    "every factual statement is supported by the evidence the explainer was given, *and* the stated reason "
    "for skipping follows from that evidence.")
INSTRUCTION = "Rate on your own. Do not look at the other rater's sheet. Do not use any AI tool to rate."

EVIDENCE_LABELS = {
    "test": "Test", "rank_by_value": "Rank by value", "n_candidates": "Candidate tests",
    "n_selected": "Selected tests", "history_score": "History score", "relevance_used": "Relevance used",
    "relevance_reason": "Semantic analyzer's reason", "changed_files": "Changed files",
    "duration_s": "Test duration (s)", "budget_s": "Budget (s)",
    "remaining_budget_at_turn_s": "Budget left when the test was reached (s)",
    "skip_cause": "Why it was skipped", "fits_if_budget_s": "Budget it would have needed (s)",
    "history": "History",
}
HISTORY_LABELS = {
    "history_builds": "builds in the history window", "runs": "runs", "failures": "failures",
    "failure_rate": "failure rate", "last_failure_distance": "builds since the last failure",
    "recent_outcomes": "recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run)",
}


class RatingError(ValueError):
    """Invalid input for a rating step; the message lists the exact problems."""


# ------------------------------------------------------------------ maths ----

def cohen_kappa(a, b, categories=RATINGS):
    """Unweighted Cohen's kappa of two equally long rating lists:
    (p_o - p_e) / (1 - p_e), with p_e from each rater's marginal shares.
    When both raters use a single, identical category (p_e = 1) kappa is 1.0."""
    if len(a) != len(b) or not a:
        raise ValueError("kappa needs two non-empty rating lists of the same length")
    n = len(a)
    p_o = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    p_e = sum((ca[c] / n) * (cb[c] / n) for c in categories)
    if p_e >= 1.0:
        return 1.0 if p_o == 1.0 else 0.0
    return (p_o - p_e) / (1.0 - p_e)


def stratum_sizes(n, budgets):
    """n split as evenly as possible over the budgets, the first ones getting the
    remainder (100 over three budgets -> 34, 33, 33)."""
    base, extra = divmod(n, len(budgets))
    return {b: base + (1 if i < extra else 0) for i, b in enumerate(budgets)}


# --------------------------------------------------------------- sampling ----

def _is_true(v):
    return str(v).strip().lower() in ("true", "1")


def _bkey(b):
    return round(float(b), 4)


def load_explanations(run_dir):
    """Rows of <run_dir>/explanations.csv usable for rating (ok and method "Full system"),
    in a fixed order so the sample does not depend on the order shards were merged."""
    path = Path(run_dir) / "explanations.csv"
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df = df[df["ok"].map(_is_true) & (df["method"] == METHOD)].copy()
    df["budget"] = df["budget"].map(_bkey)
    return df.sort_values(["budget", "build", "test"], kind="mergesort").reset_index(drop=True)


def draw_sample(df, n, seed, budgets=DEFAULT_BUDGETS):
    """Stratified sample of n rows by budget, item ids R001.. in random order.

    Returns (items DataFrame, notes). A stratum with fewer rows than its share
    gives all of them; the shortfall is filled from the other strata at random."""
    budgets = [_bkey(b) for b in budgets]
    if len(df) < n:
        raise RatingError(f"only {len(df)} usable explanations, {n} requested")
    rng = np.random.default_rng(seed)
    want = stratum_sizes(n, budgets)
    picked, leftover, notes = [], [], []
    for b in budgets:
        idx = df.index[df["budget"] == b].to_numpy()
        k = min(want[b], len(idx))
        if k < want[b]:
            notes.append(f"budget {b:g}: only {len(idx)} explanations, {want[b]} wanted; all taken")
        chosen = rng.choice(idx, size=k, replace=False) if k else np.array([], dtype=int)
        picked.extend(chosen.tolist())
        leftover.extend(sorted(set(idx.tolist()) - set(chosen.tolist())))
    short = n - len(picked)
    if short:
        fill = rng.choice(np.array(sorted(leftover)), size=short, replace=False).tolist()
        picked.extend(fill)
        got = Counter(df.loc[fill, "budget"])
        notes.append("filled " + ", ".join(f"{got[b]} from budget {b:g}" for b in budgets if got[b]))
    items = df.loc[picked].reset_index(drop=True)
    items = items.loc[rng.permutation(len(items))].reset_index(drop=True)
    items.insert(0, "item_id", [f"R{i:03d}" for i in range(1, len(items) + 1)])
    return items[ITEM_COLUMNS], notes


def _value(v):
    if v is None:
        return "none"
    if isinstance(v, list):
        return ", ".join("-" if x is None else str(x) for x in v) if v else "(none)"
    return str(v)


def evidence_lines(evidence):
    """The evidence JSON as a readable Markdown list (not raw JSON)."""
    lines = []
    for key, v in evidence.items():
        label = EVIDENCE_LABELS.get(key, key)
        if key == "history" and isinstance(v, dict):
            lines.append(f"- {label}:")
            lines.extend(f"  - {HISTORY_LABELS.get(k, k)}: {_value(x)}" for k, x in v.items() if k != "test")
        elif key == "changed_files" and isinstance(v, list):
            lines.append(f"- {label}:" + ("" if v else " (none)"))
            lines.extend(f"  - `{p}`" for p in v)
        else:
            lines.append(f"- {label}: {_value(v)}")
    return lines


def items_markdown(items, notes):
    out = ["# Explanation rating sheet (Gap 2, RQ2)", "",
           f"**Rating rule** (docs/PROJECT_CONTEXT.md §8): {RATING_RULE}", "",
           f"**{INSTRUCTION}**", "",
           "Write one of `sound`, `partly`, `unsound` in the `rating` column of your own sheet "
           "(`ratings_ali.csv` or `ratings_bilal.csv`), and a short note when it helps.", ""]
    if notes:
        out += ["Sampling notes: " + "; ".join(notes), ""]
    for r in items.itertuples(index=False):
        evidence = json.loads(r.evidence) if r.evidence else {}
        facts = json.loads(r.cited_facts) if r.cited_facts else []
        out += [f"## {r.item_id}", "", f"Build `{r.build}`, budget {float(r.budget):.0%}, test `{r.test}`", "",
                "**Evidence given to the explainer**", ""]
        out += evidence_lines(evidence)
        out += ["", "**Justification**", "", f"> {r.justification}", "", "**Cited facts**", ""]
        out += [f"- {f}" for f in facts] or ["- (none)"]
        out.append("")
    return "\n".join(out)


def _write_csv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})


def cmd_sample(run_dir, n, seed, out_dir, budgets=DEFAULT_BUDGETS):
    """Write rating_items.csv/.md and the two blank sheets; returns the notes."""
    out = Path(out_dir)
    items, notes = draw_sample(load_explanations(run_dir), n, seed, budgets)
    for note in notes:
        log.warning(note)
    _write_csv(out / "rating_items.csv", ITEM_COLUMNS, items.to_dict("records"))
    (out / "rating_items.md").write_text(items_markdown(items, notes), encoding="utf-8")
    for rater in RATERS:
        _write_csv(out / f"ratings_{rater}.csv", SHEET_COLUMNS,
                   [{"item_id": i, "rating": "", "note": ""} for i in items["item_id"]])
    return notes


# -------------------------------------------------------------- agreement ----

def read_sheet(path, column="rating"):
    """{item_id: rating} from a filled sheet; raises RatingError listing every row
    (file, line, item_id, value) whose rating is not sound / partly / unsound."""
    rows, bad = {}, []
    with open(path, "r", encoding="utf-8", newline="") as f:
        for line, r in enumerate(csv.DictReader(f), start=2):      # line 1 is the header
            value = (r.get(column) or "").strip().lower()
            if value not in RATINGS:
                bad.append(f"{Path(path).name} line {line}, item {r.get('item_id')}: {column} = "
                           f"{r.get(column)!r}")
            rows[r["item_id"]] = value
    if bad:
        raise RatingError("invalid ratings (allowed: sound, partly, unsound):\n" + "\n".join(bad))
    return rows


def _paired(a, b):
    if set(a) != set(b):
        only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
        raise RatingError(f"the sheets rate different items: only Ali {only_a}, only Bilal {only_b}")
    ids = sorted(a)
    return ids, [a[i] for i in ids], [b[i] for i in ids]


def _share(values, category):
    return sum(1 for v in values if v == category) / len(values) if values else 0.0


def cmd_agreement(dir_):
    """Write agreement.md, disagreements.csv and ratings_final.csv; returns the stats."""
    d = Path(dir_)
    ids, ali, bilal = _paired(read_sheet(d / "ratings_ali.csv"), read_sheet(d / "ratings_bilal.csv"))
    kappa = cohen_kappa(ali, bilal)
    raw = sum(1 for x, y in zip(ali, bilal) if x == y) / len(ids)
    stats = {"n": len(ids), "raw_agreement": raw, "kappa": kappa,
             "share_sound_ali": _share(ali, "sound"), "share_sound_bilal": _share(bilal, "sound")}
    pairs = list(zip(ids, ali, bilal))
    _write_csv(d / "disagreements.csv", DISAGREEMENT_COLUMNS,
               [{"item_id": i, "rating_ali": x, "rating_bilal": y} for i, x, y in pairs if x != y])
    _write_csv(d / "ratings_final.csv", FINAL_COLUMNS,
               [{"item_id": i, "rating_ali": x, "rating_bilal": y, "final_rating": x if x == y else ""}
                for i, x, y in pairs])
    matrix = Counter(zip(ali, bilal))
    lines = ["# Explanation rating: agreement", "",
             f"- Items rated by both: {stats['n']}",
             f"- Raw agreement: {raw:.3f}",
             f"- Cohen's kappa (unweighted, 3 categories): {kappa:.3f}",
             f"- Share rated sound: Ali {stats['share_sound_ali']:.3f}, Bilal {stats['share_sound_bilal']:.3f}",
             f"- Disagreements to resolve by discussion: {sum(1 for _, x, y in pairs if x != y)} "
             "(`disagreements.csv`; write the agreed rating in `final_rating` of `ratings_final.csv`)", "",
             "Confusion matrix (rows Ali, columns Bilal):", "",
             "| Ali \\ Bilal | " + " | ".join(RATINGS) + " |",
             "|---|" + "---|" * len(RATINGS)]
    lines += [f"| {r} | " + " | ".join(str(matrix[(r, c)]) for c in RATINGS) + " |" for r in RATINGS]
    (d / "agreement.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return stats


# ------------------------------------------------------------------ final ----

def cmd_final(dir_):
    """Write rating_summary.csv/.md from ratings_final.csv; returns the summary rows."""
    d = Path(dir_)
    final = read_sheet(d / "ratings_final.csv", column="final_rating")
    ids, ali, bilal = _paired(read_sheet(d / "ratings_final.csv", "rating_ali"),
                              read_sheet(d / "ratings_final.csv", "rating_bilal"))
    kappa = cohen_kappa(ali, bilal)
    items = pd.read_csv(d / "rating_items.csv", dtype=str, keep_default_na=False)
    budget_of = {r.item_id: _bkey(r.budget) for r in items.itertuples(index=False)}
    missing = sorted(set(final) - set(budget_of))
    if missing:
        raise RatingError(f"items not in rating_items.csv: {missing}")

    def row(scope, budget, values):
        r = {"scope": scope, "budget": budget, "n": len(values), "kappa": round(kappa, 4),
             **{f"share_{c}": round(_share(values, c), 4) for c in RATINGS}}
        r["rq2_sound_condition_holds"] = (r["share_sound"] >= RQ2_SOUND_SHARE) if scope == "overall" else ""
        return r

    rows = [row("overall", "", list(final.values()))]
    for b in sorted(set(budget_of.values())):
        rows.append(row("budget", b, [v for i, v in final.items() if budget_of[i] == b]))
    _write_csv(d / "rating_summary.csv", SUMMARY_COLUMNS, rows)
    overall = rows[0]
    lines = ["# Explanation rating: summary (RQ2)", "",
             f"- Items: {overall['n']}",
             f"- Cohen's kappa before discussion: {kappa:.3f}",
             f"- RQ2 soundness condition (share sound >= {RQ2_SOUND_SHARE:.2f}): "
             f"**{'holds' if overall['rq2_sound_condition_holds'] else 'does not hold'}** "
             f"(share sound {overall['share_sound']:.3f})", "",
             "| Scope | n | sound | partly | unsound |", "|---|---|---|---|---|"]
    for r in rows:
        scope = "overall" if r["scope"] == "overall" else "budget {:.0%}".format(r["budget"])
        lines.append(f"| {scope} | {r['n']} | {r['share_sound']:.3f} | {r['share_partly']:.3f} | "
                     f"{r['share_unsound']:.3f} |")
    (d / "rating_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rows


# -------------------------------------------------------------------- CLI ----

def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m src.eval.rating", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample", help="draw the stratified sample and write the rating sheets")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--n", type=int, default=100)
    s.add_argument("--seed", type=int, default=42)
    s.add_argument("--out", default=DEFAULT_DIR)
    for name, text in (("agreement", "raw agreement, Cohen's kappa, disagreements"),
                       ("final", "summary after the disagreements were resolved")):
        sub.add_parser(name, help=text).add_argument("--dir", default=DEFAULT_DIR)
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        if args.cmd == "sample":
            cmd_sample(repo_path(args.run_dir), args.n, args.seed, repo_path(args.out))
        elif args.cmd == "agreement":
            stats = cmd_agreement(repo_path(args.dir))
            log.info("n=%d raw agreement=%.3f kappa=%.3f", stats["n"], stats["raw_agreement"], stats["kappa"])
        else:
            overall = cmd_final(repo_path(args.dir))[0]
            log.info("share sound=%.3f RQ2 condition holds: %s", overall["share_sound"],
                     overall["rq2_sound_condition_holds"])
    except RatingError as e:
        log.error("%s", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
