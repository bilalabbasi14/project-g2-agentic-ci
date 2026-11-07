"""Run one experiment (E1-E6, DEV) for one seed, optionally one shard of the builds.

    python -m experiments.run_experiment --exp E3 --seed 1 [--split test] [--methods ...]
        [--run-id E3_test_seed1] [--shard 0/2] [--base-url http://localhost:11435]
        [--provider ollama|mock] [--skip-existing] [--build-limit N] [--host kaggle-t4x2]
        [--relevance-prompt v1|v2]

Reads the config (G2_CONFIG), experiments/configs/<exp>.yaml, the evaluation set
(cfg["eval"]["eval_set"]; for split phase1, data_eval/eval_builds.csv), the
method catalogue and the tuned weights, builds one provider per component and
runs src.pipeline.run_build for each build of the shard, printing
`[n/N] build seconds fallbacks`. A shard writes to the same run folder but to
its own files (per_build.shard<i>.csv, ..., run_meta.shard<i>.json);
experiments/merge_shards.py combines them.
"""
import argparse
import copy
import json
import logging
import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import yaml

from src.agent.llm_provider import MockProvider, make_provider
from src.obs.trace import TraceLogger
from src.pipeline import Components, RunContext, load_method_specs, load_tuned_weights, run_builds
from src.settings import load_config, repo_path

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
SPLITS = ("dev", "test", "phase1")
log = logging.getLogger(__name__)


def shard(rows, i, n):
    """The rows whose position % n == i (positions in the given order)."""
    if not 0 <= i < n:
        raise ValueError(f"shard index {i} not in 0..{n - 1}")
    return [r for pos, r in enumerate(rows) if pos % n == i]


def parse_shard(text):
    """'0/2' -> (0, 2)."""
    try:
        i, n = (int(x) for x in text.split("/"))
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"--shard must look like 0/2, got {text!r}") from e
    if n < 1 or not 0 <= i < n:
        raise argparse.ArgumentTypeError(f"--shard {text}: index must be in 0..n-1")
    return i, n


def default_run_id(exp, split, seed):
    return f"{exp}_{split}_seed{seed}"


def load_experiment(exp):
    path = CONFIG_DIR / f"{exp}.yaml"
    if not path.exists():
        valid = sorted(p.stem for p in CONFIG_DIR.glob("*.yaml"))
        raise SystemExit(f"unknown experiment {exp!r}; valid: {', '.join(valid)}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def eval_rows(cfg, split, build_limit=None):
    """Evaluation builds of a split, in eval-set order, as rows for run_build."""
    if split == "phase1":
        df = pd.read_csv(repo_path(cfg["paths"]["eval_builds"]))
        df = df.assign(in_phase1=True)
    else:
        df = pd.read_csv(repo_path(cfg["eval"]["eval_set"]))
        df = df[df["split"] == split]
    rows = [SimpleNamespace(**r) for r in df.to_dict("records")]
    return rows[:build_limit] if build_limit else rows


def mock_relevance(prompt):
    test = prompt.split("Test class `", 1)[1].split("`", 1)[0]
    return json.dumps({"test": test, "relevance": 0.5, "reason": "mock", "confidence": 1.0})


MOCK_ORCHESTRATOR = json.dumps({"action": "final", "w": 0.6666667, "confidence": 0.9, "reason": "mock"})

_LISTED_TEST = re.compile(r"^\d+\. (\S+)$", re.MULTILINE)


def mock_single_call(prompt):
    """Mock single-call answer that rates every numbered test in the prompt with 0.5,
    so laptop runs exercise the scorer's success path (not only its fallback)."""
    return json.dumps({"scores": [{"test": t, "relevance": 0.5} for t in _LISTED_TEST.findall(prompt)]})


def _import_component(module, cls, issue, method):
    """Lazily import a component that another issue delivers; exit clearly if it is missing."""
    try:
        mod = __import__(module, fromlist=[cls])
        return getattr(mod, cls)
    except (ImportError, AttributeError):
        raise SystemExit(f"method {method!r} needs {module}.{cls} from {issue}, which is not merged yet")


def make_components(cfg, specs, provider_kind, base_url, seed, trace):
    """One provider per component; only the components the methods need."""
    def provider(component, mock_answers):
        if provider_kind == "mock":
            p = MockProvider(mock_answers)
            p.component = component
            return p
        return make_provider(cfg, component=component, base_url=base_url, seed=seed)

    sources = {s.relevance_source for s in specs}
    comps = Components(tuned_weights=load_tuned_weights(cfg["tuning"]["tuned_weights_file"]))
    if sources & {"llm_shortlist", "llm_all_individual"}:
        comps.relevance_provider = provider("semantic_analyzer", [mock_relevance])
    agent = [s for s in specs if s.weight_mode == "agent"]
    if agent:
        from src.agent.orchestrator import LLMOrchestrator
        comps.orchestrator = LLMOrchestrator(provider("orchestrator", [MOCK_ORCHESTRATOR]), cfg, trace=trace)
    explained = [s for s in specs if s.explainer]
    if explained:
        cls = _import_component("src.agent.explainer", "LLMExplainer", "P2-10 (issue #10)", explained[0].name)
        comps.explainer = cls(provider("explainer", ['{"justification": "mock", "cited_facts": []}']), cfg,
                              trace=trace)
    single = [s for s in specs if s.relevance_source == "llm_single_call"]
    if single:
        cls = _import_component("src.agent.single_call", "SingleCallScorer", "P2-17 (issue #17)", single[0].name)
        if provider_kind == "mock":
            sc_provider = provider("single_call", [mock_single_call])
        else:
            # built with single_call.num_ctx (16384), not llm_p2.num_ctx (8192): the prompt plus the
            # full answer for ~200 candidates is about 8,600-8,900 tokens (review of PR #52)
            from src.agent.single_call import make_single_call_provider
            sc_provider = make_single_call_provider(cfg, base_url=base_url, seed=seed)
        comps.single_call = cls(sc_provider, cfg, trace=trace)
    if any(s.weight_mode == "tuned" and s.tuned_key not in comps.tuned_weights for s in specs):
        missing = sorted({s.tuned_key for s in specs if s.weight_mode == "tuned"} - set(comps.tuned_weights))
        raise SystemExit(f"tuned weights {missing} missing from {cfg['tuning']['tuned_weights_file']} (P2-11)")
    return comps


def make_loader(cfg):
    from src.data.loader import LRTSLoader
    from src.data.source_cache import cache_dir_from_config
    from src.data.sources import SourceRepo
    p = cfg["paths"]
    repo = SourceRepo(p["repo_clone"], p.get("repo_url")) if p.get("repo_clone") else None
    return LRTSLoader(p["lrts_root"], cfg["project"], repo, source_cache_dir=cache_dir_from_config(cfg))


def build_parser():
    ap = argparse.ArgumentParser(description="Run one experiment for one seed.")
    ap.add_argument("--exp", required=True, help="experiments/configs/<exp>.yaml, e.g. E3")
    ap.add_argument("--split", choices=SPLITS, help="override the config's split")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--methods", nargs="+", help="override the config's method list")
    ap.add_argument("--run-id", help="default: <exp>_<split>_seed<seed>")
    ap.add_argument("--shard", type=parse_shard, help="i/n: only builds whose position %% n == i")
    ap.add_argument("--base-url", help="Ollama server for this process")
    ap.add_argument("--provider", choices=["ollama", "mock"], default="ollama")
    ap.add_argument("--skip-existing", action="store_true", help="skip builds with runs/<build>.json")
    ap.add_argument("--build-limit", type=int, help="first N builds of the split, in eval-set order")
    ap.add_argument("--host", help='recorded in run_meta, e.g. "kaggle-t4x2"')
    ap.add_argument("--relevance-prompt", choices=["v1", "v2"],
                    help="override llm_p2.relevance_prompt_version (dev comparison, P2-07)")
    return ap


def main(argv=None, cfg=None, loader=None, echo=print):
    """cfg and loader can be injected (tests); otherwise they come from the config."""
    args = build_parser().parse_args(argv)
    cfg = copy.deepcopy(cfg) if cfg is not None else load_config()
    if args.relevance_prompt:
        cfg.setdefault("llm_p2", {})["relevance_prompt_version"] = args.relevance_prompt
    exp = load_experiment(args.exp)
    split = args.split or exp.get("split")
    if split not in SPLITS:
        raise SystemExit(f"experiment {args.exp} has no split; use --split ({', '.join(SPLITS)})")
    names = args.methods or exp.get("methods") or []
    if not names:
        raise SystemExit(f"experiment {args.exp} lists no methods; give them with --methods")
    try:
        specs = load_method_specs(names=names)
    except ValueError as e:
        raise SystemExit(str(e))
    budgets = [float(b) for b in exp.get("budgets", [0.05, 0.10, 0.20])]
    run_id = args.run_id or default_run_id(args.exp, split, args.seed)
    limit = args.build_limit or exp.get("build_limit")
    rows = eval_rows(cfg, split, limit)
    suffix = ""
    if args.shard:
        i, n = args.shard
        rows = shard(rows, i, n)
        suffix = f".shard{i}"

    trace = TraceLogger.from_config(cfg, run_id)
    ctx = RunContext.create(cfg, run_id, args.exp, split, args.seed, repo_path(cfg["paths"]["results_dir"]),
                            trace=trace, file_suffix=suffix)
    skipped = []
    if args.skip_existing:
        keep = []
        for r in rows:
            (skipped if (ctx.run_dir / "runs" / f"{r.key}.json").exists() else keep).append(r)
        rows = keep
        for r in skipped:
            echo(f"skip {r.key} (runs/{r.key}.json exists)")
    for r in rows:
        # a build that runs (again) starts with an empty trace file, so each build
        # has one clean trajectory even after an interrupted earlier attempt
        stale = trace.path(r.key)
        if stale.exists():
            stale.unlink()
            echo(f"removed stale trace {stale.name}")
    comps = make_components(cfg, specs, args.provider, args.base_url, args.seed, trace)
    loader = loader or make_loader(cfg)

    def progress(i, n, key, seconds, fallbacks, error):
        echo(f"[{i}/{n}] {key} {seconds:.1f}s fallbacks={fallbacks}" + (f" FAILED {error}" if error else ""))

    meta = run_builds(cfg, loader, rows, specs, budgets, comps, ctx,
                      config_file=Path(os.environ.get("G2_CONFIG") or "config.yaml").name, host=args.host,
                      progress=progress, extra_meta={"shard": list(args.shard) if args.shard else None,
                                                     "provider": args.provider,
                                                     "skipped_existing": [r.key for r in skipped]})
    echo(f"done: {meta['n_builds']} builds, {len(meta['failed_builds'])} failed -> {ctx.run_dir}")
    return meta


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
    sys.exit(0)
