"""Shortlist recall (P2-12): how many failing tests the LLM can see at all.

The LLM only scores shortlisted tests: the union of the top k tests by history
score and the top k by TF-IDF relevance (src.agent.shortlister; tests with a
score of 0 are not taken from a list). A failing test that is not on the
shortlist gets LLM relevance 0, so the LLM cannot help find it. For every build
of a split this module computes, from the DANTE-CCH scores only (no LLM, CPU):

    recall@k = |failing ∩ shortlist_k| / |failing|

    python -m src.eval.shortlist_recall --split test [--k 5 10 15 20]

writes results/analysis/shortlist_recall_<split>.csv and .md.

The target build's outcomes (`actual_outcome`) are used only as the ground
truth for the recall, never as input to the shortlist. The shortlist size the
pipeline uses stays cfg["shortlist"]["k"] (10, fixed in Phase 1); the other k
values only describe the limit of the shortlist and are not used to change k.
"""
import argparse
import csv
import logging
import statistics
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd

from src.agent.shortlister import shortlist
from src.settings import load_config, repo_path

log = logging.getLogger(__name__)

DEFAULT_KS = (5, 10, 15, 20)
CSV_COLUMNS = ["build", "k", "n_failing", "n_in_shortlist", "recall", "shortlist_size"]
SPLITS = ("dev", "test")


def recall_at_k(history_scores: Dict[str, float], tfidf_scores: Dict[str, float], failing: Iterable[str],
                k: int) -> Tuple[int, Optional[float], int]:
    """(failing tests on the shortlist, recall@k, shortlist size) for one build.

    The shortlist is built exactly as in the pipeline (src.agent.shortlister).
    recall is None when the build has no failing test (it is then undefined)."""
    short = set(shortlist(history_scores, tfidf_scores, k))
    failing = set(failing)
    n_in = len(failing & short)
    recall = n_in / len(failing) if failing else None
    return n_in, recall, len(short)


def build_rows(build_key: str, df: pd.DataFrame, ks: Iterable[int]) -> List[dict]:
    """CSV rows (one per k) for one build from its DANTE-CCH score table.
    `actual_outcome` gives the failing candidates, the ground truth only."""
    history = df["history_score"].astype(float).to_dict()
    tfidf = df["tfidf_relevance"].astype(float).to_dict()
    failing = set(df.index[df["actual_outcome"] == 1])
    rows = []
    for k in ks:
        n_in, recall, size = recall_at_k(history, tfidf, failing, k)
        rows.append({"build": build_key, "k": int(k), "n_failing": len(failing), "n_in_shortlist": n_in,
                     "recall": recall, "shortlist_size": size})
    return rows


def summarise(rows: List[dict], used_k: int) -> List[dict]:
    """One summary per k over the builds with a defined recall: mean and median
    recall, share of builds with recall 0 and with recall 1, mean shortlist size."""
    out = []
    for k in sorted({r["k"] for r in rows}):
        ok = [r for r in rows if r["k"] == k and r["recall"] is not None]
        rec = [r["recall"] for r in ok]
        out.append({
            "k": k, "used": k == used_k, "n_builds": len(ok),
            "mean_recall": statistics.fmean(rec) if rec else None,
            "median_recall": statistics.median(rec) if rec else None,
            "share_recall_0": sum(1 for x in rec if x == 0) / len(rec) if rec else None,
            "share_recall_1": sum(1 for x in rec if x == 1) / len(rec) if rec else None,
            "mean_shortlist_size": statistics.fmean(r["shortlist_size"] for r in ok) if ok else None,
        })
    return out


def _fmt(x, digits=3):
    return "–" if x is None else f"{x:.{digits}f}"


def render_markdown(summary: List[dict], split: str, used_k: int, command: str, n_builds: int,
                    notes: Iterable[str] = ()) -> str:
    """Readable summary; the k actually used by the pipeline is marked."""
    lines = [
        f"# Shortlist recall — {split} split", "",
        f"Command: `{command}`", "",
        f"Builds: {n_builds} (split `{split}` of the evaluation set). For each build, the failing candidates come "
        "from the build's own outcomes, used only as ground truth here.", "",
        "recall@k = failing candidates on the shortlist / failing candidates. The shortlist is the union of the "
        "top k candidates by history score and the top k by TF-IDF relevance (DANTE-CCH scores; candidates with "
        "a score of 0 are not taken from a list). A failing test outside the shortlist gets LLM relevance 0.", "",
        f"**k = {used_k} is the configuration actually used** (`shortlist.k` in config.yaml, fixed in Phase 1). "
        "The other k values only describe the limit of the shortlist; they are not used to change k.", "",
        "| k | configuration | builds | mean recall | median recall | share recall = 0 | share recall = 1 "
        "| mean shortlist size |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for s in summary:
        k = f"**{s['k']}**" if s["used"] else str(s["k"])
        used = "**used**" if s["used"] else "describes the limit only"
        lines.append(f"| {k} | {used} | {s['n_builds']} | {_fmt(s['mean_recall'])} | {_fmt(s['median_recall'])} "
                     f"| {_fmt(s['share_recall_0'])} | {_fmt(s['share_recall_1'])} "
                     f"| {_fmt(s['mean_shortlist_size'], 1)} |")
    notes = list(notes)
    if notes:
        lines += ["", "Notes:"] + [f"- {n}" for n in notes]
    return "\n".join(lines) + "\n"


def write_outputs(rows: List[dict], markdown: str, out_dir: Path, split: str) -> Tuple[Path, Path]:
    """Write shortlist_recall_<split>.csv and .md into out_dir."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"shortlist_recall_{split}.csv"
    md_path = out_dir / f"shortlist_recall_{split}.md"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "recall": "" if r["recall"] is None else r["recall"]})
    md_path.write_text(markdown, encoding="utf-8")
    return csv_path, md_path


def split_rows(cfg, split: str) -> list:
    """Evaluation builds of the split (cfg["eval"]["eval_set"]), in eval-set order."""
    df = pd.read_csv(repo_path(cfg["eval"]["eval_set"]))
    return list(df[df["split"] == split].itertuples(index=False))


def make_loader(cfg):
    """Loader with the source cache (P2-09). The git clone is used only if it
    already exists: this analysis never starts a clone."""
    from src.data.loader import LRTSLoader
    from src.data.source_cache import cache_dir_from_config
    from src.data.sources import SourceRepo
    p = cfg["paths"]
    clone = p.get("repo_clone")
    repo = SourceRepo(clone, p.get("repo_url")) if clone and Path(clone).is_dir() else None
    return LRTSLoader(p["lrts_root"], cfg["project"], repo, source_cache_dir=cache_dir_from_config(cfg))


def run(cfg, split: str, ks: Iterable[int], loader=None, rows=None, out_dir=None, command: str = ""):
    """Compute the recall for every build of the split and write the CSV and the
    Markdown summary. Returns (csv_path, md_path, summary)."""
    from src.dante import scores
    used_k = int(cfg["shortlist"]["k"])
    ks = sorted({int(k) for k in ks} | {used_k})
    loader = loader or make_loader(cfg)
    rows = split_rows(cfg, split) if rows is None else rows
    h = cfg["history"]
    out, notes, n_builds = [], [], 0
    for e in rows:
        row = loader.row(e.pr_name, e.build_id, e.stage_id)
        build = loader.build(row)
        if not build.sources_available:
            log.warning("%s: no test sources (no cache file and no clone); TF-IDF relevance is 0", build.key)
            notes.append(f"{build.key}: loaded without test sources, so its TF-IDF relevance is 0.")
        hist = loader.history(row, h["num_builds"], max(h["lookback_windows"]))
        df = scores(build, hist, cfg, "DANTE-CCH")
        if df is None or df.empty:
            log.warning("%s: no DANTE scores (no candidates); skipped", build.key)
            notes.append(f"{build.key}: no DANTE scores (no candidates); skipped.")
            continue
        out += build_rows(build.key, df, ks)
        n_builds += 1
    summary = summarise(out, used_k)
    md = render_markdown(summary, split, used_k, command, n_builds, notes)
    out_dir = Path(out_dir) if out_dir else repo_path(cfg["paths"]["results_dir"]) / "analysis"
    csv_path, md_path = write_outputs(out, md, out_dir, split)
    return csv_path, md_path, summary


def main(argv=None):
    ap = argparse.ArgumentParser(description="Shortlist recall per build (DANTE scores only, no LLM).")
    ap.add_argument("--split", choices=SPLITS, default="test")
    ap.add_argument("--k", type=int, nargs="+", default=list(DEFAULT_KS), help="shortlist sizes to report")
    ap.add_argument("--out", help="output folder (default: <results_dir>/analysis)")
    args = ap.parse_args(argv)
    command = "python -m src.eval.shortlist_recall " + " ".join(argv if argv is not None else sys.argv[1:])
    csv_path, md_path, summary = run(load_config(), args.split, args.k, out_dir=args.out, command=command.strip())
    for s in summary:
        print(f"k={s['k']}{' (used)' if s['used'] else ''}: builds={s['n_builds']} "
              f"mean recall={_fmt(s['mean_recall'])} share recall=0: {_fmt(s['share_recall_0'])}")
    print(f"-> {csv_path}\n-> {md_path}")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    sys.exit(main())
