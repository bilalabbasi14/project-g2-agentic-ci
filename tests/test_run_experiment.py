"""Experiment runner and shard merge (P2-16) with a fake loader and mock providers (no data, no model)."""
import copy
import csv
import json

import pandas as pd
import pytest

from experiments import merge_shards
from experiments.run_experiment import default_run_id, main, parse_shard, shard
from src.settings import load_config
from tests.test_end_to_end import _fixture

KEYS = ["PR-1_build1", "PR-2_build1", "PR-3_build1", "PR-4_build1", "PR-5_build1"]


class KeyedLoader:
    """Returns the synthetic build under the requested key; `row` is the key itself."""

    def __init__(self):
        self.built = []

    def row(self, pr_name, build_id, stage_id):
        return f"{pr_name}_build{build_id}"

    def build(self, row, keep_sources=False):
        build, _ = _fixture()
        build = copy.deepcopy(build)
        build.key = row
        self.built.append(row)
        return build

    def history(self, row, *a):
        return _fixture()[1]


def _cfg(tmp_path):
    cfg = load_config()
    eval_csv = tmp_path / "eval.csv"
    pd.DataFrame({"key": KEYS, "pr_name": [k.split("_")[0] for k in KEYS], "build_id": 1, "stage_id": "single",
                  "in_phase1": False, "split": ["dev"] * 4 + ["test"]}).to_csv(eval_csv, index=False)
    cfg["eval"]["eval_set"] = str(eval_csv)
    cfg["paths"]["results_dir"] = str(tmp_path / "results")
    cfg["paths"]["logs_dir"] = str(tmp_path / "logs")
    cfg["trace"]["dir"] = str(tmp_path / "traces")
    cfg["tuning"]["tuned_weights_file"] = str(tmp_path / "none.yaml")
    return cfg


def _run(tmp_path, *extra, loader=None, lines=None):
    argv = ["--exp", "DEV", "--seed", "1", "--provider", "mock", "--methods", "DANTE-CCH", "LLM-relevance",
            "Agent-weighted", *extra]
    out = lines if lines is not None else []
    return main(argv, cfg=_cfg(tmp_path), loader=loader or KeyedLoader(), echo=out.append)


def _rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_shard_positions():
    assert shard(list(range(10)), 0, 2) == [0, 2, 4, 6, 8]
    both = shard(list(range(10)), 0, 2) + shard(list(range(10)), 1, 2)
    assert sorted(both) == list(range(10)) and len(both) == 10
    assert parse_shard("1/2") == (1, 2)
    with pytest.raises(ValueError):
        shard([1], 2, 2)


def test_default_run_id():
    assert default_run_id("E3", "test", 1) == "E3_test_seed1"


def test_two_shards_then_merge(tmp_path):
    lines = []
    m0 = _run(tmp_path, "--shard", "0/2", lines=lines)
    m1 = _run(tmp_path, "--shard", "1/2", lines=lines)
    assert m0["n_builds"] == 2 and m1["n_builds"] == 2 and m0["run_id"] == "DEV_dev_seed1"
    assert [ln.split()[0] for ln in lines if ln.startswith("[")] == ["[1/2]", "[2/2]", "[1/2]", "[2/2]"]
    run_dir = tmp_path / "results" / "DEV_dev_seed1"
    assert (run_dir / "per_build.shard0.csv").exists() and (run_dir / "per_build.shard1.csv").exists()
    out = merge_shards.merge_run(run_dir)
    assert out["run_meta"] == 4
    rows = _rows(run_dir / "per_build.csv")
    triples = [(r["build"], r["method"], r["budget"]) for r in rows]
    assert len(triples) == len(set(triples)) == 4 * 3 * 3        # 4 dev builds x 3 methods x 3 budgets
    assert sorted({r["build"] for r in rows}) == KEYS[:4]
    assert triples == sorted(triples, key=lambda t: (t[0], t[1], float(t[2])))
    assert not list(run_dir.glob("*.shard*"))
    meta = json.loads((run_dir / "run_meta.json").read_text(encoding="utf-8"))
    assert meta["n_builds"] == 4 and sorted(map(tuple, meta["shards"])) == [(0, 2), (1, 2)]
    assert len(_rows(run_dir / "orchestrator_decisions.csv")) == 4
    assert len(list((run_dir / "runs").glob("*.json"))) == 4


def test_skip_existing(tmp_path):
    _run(tmp_path, "--build-limit", "2")
    loader, lines = KeyedLoader(), []
    meta = _run(tmp_path, "--skip-existing", loader=loader, lines=lines)
    assert loader.built == KEYS[2:4] and meta["n_builds"] == 2
    assert meta["skipped_existing"] == KEYS[:2]
    assert any(ln.startswith(f"skip {KEYS[0]}") for ln in lines)


def test_unknown_method_is_a_clear_error(tmp_path):
    with pytest.raises(SystemExit) as e:
        main(["--exp", "DEV", "--seed", "1", "--provider", "mock", "--methods", "DANTE-CCH", "Nope"],
             cfg=_cfg(tmp_path), loader=KeyedLoader(), echo=lambda *_: None)
    assert "Nope" in str(e.value) and "valid names" in str(e.value)


def test_missing_component_names_its_issue(tmp_path, monkeypatch):
    # simulate a component that is not merged: importing its module fails
    # (independent of which issues are actually merged)
    import sys
    monkeypatch.setitem(sys.modules, "src.agent.single_call", None)
    with pytest.raises(SystemExit) as e:
        main(["--exp", "DEV", "--seed", "1", "--provider", "mock", "--methods", "Single-call LLM"],
             cfg=_cfg(tmp_path), loader=KeyedLoader(), echo=lambda *_: None)
    assert "P2-17" in str(e.value) and "not merged yet" in str(e.value)


def test_mock_single_call_takes_the_success_path(tmp_path):
    pytest.importorskip("src.agent.single_call")
    main(["--exp", "DEV", "--seed", "1", "--provider", "mock", "--methods", "Single-call LLM",
          "--build-limit", "1"], cfg=_cfg(tmp_path), loader=KeyedLoader(), echo=lambda *_: None)
    rows = _rows(tmp_path / "results" / "DEV_dev_seed1" / "per_build.csv")
    assert rows and {r["ranking_source"] for r in rows} == {"llm"}            # no fallback
    assert {r["llm_calls"] for r in rows} == {"1"}


@pytest.mark.parametrize("cache", [True, False])
def test_runner_single_call_provider_uses_single_call_num_ctx(tmp_path, cache):
    """With Ollama, the single call must get single_call.num_ctx (16384), not llm_p2.num_ctx (8192)."""
    pytest.importorskip("src.agent.single_call")
    from experiments.run_experiment import make_components
    from src.pipeline import load_method_specs
    cfg = _cfg(tmp_path)
    cfg["llm_p2"]["cache"] = cache
    cfg["llm_p2"]["cache_dir"] = str(tmp_path / "llm_cache")
    comps = make_components(cfg, load_method_specs(names=["Single-call LLM"]), "ollama",
                            "http://127.0.0.1:11435", 2, trace=None)
    p = comps.single_call.provider
    inner = getattr(p, "inner", p)
    assert cfg["single_call"]["num_ctx"] == 16384 != cfg["llm_p2"]["num_ctx"]
    assert inner.num_ctx == 16384 and inner.request_options(0)["num_ctx"] == 16384
    assert inner.base_url == "http://127.0.0.1:11435"
    if cache:
        assert p.options_for(0)["num_ctx"] == 16384


def test_experiment_configs_load():
    from experiments.run_experiment import load_experiment
    from src.pipeline import load_method_specs
    for exp in ("E1", "E2", "E2_stored", "E3", "E5", "E5_noshortlist"):
        c = load_experiment(exp)
        assert c["split"] in ("test", "phase1") and load_method_specs(names=c["methods"])
    assert load_experiment("E5_noshortlist")["build_limit"] == 20
    assert load_experiment("DEV")["split"] == "dev"
    with pytest.raises(SystemExit):
        load_experiment("E9")


def test_notebook_is_clean_and_never_prints_the_token():
    from pathlib import Path
    nb = json.loads((Path(__file__).resolve().parent.parent / "experiments" / "kaggle_runner.ipynb")
                    .read_text(encoding="utf-8"))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert all(c["outputs"] == [] and c["execution_count"] is None for c in code)
    for c in code:
        for line in c["source"]:
            if "_token" in line or "_url" in line:
                assert "print(" not in line or "replace(_token" in line
    params = "".join(code[0]["source"])
    for name in ("REPO_REF", "EXP", "SPLIT", "SEEDS", "METHODS", "EXTRA_ARGS"):
        assert name + " =" in params


def test_rerun_with_skip_existing_leaves_one_set_of_rows(tmp_path):
    """Running the same build twice into one run_id with --skip-existing must not append duplicates."""
    first = _run(tmp_path, "--build-limit", "1", "--skip-existing")
    loader = KeyedLoader()
    second = _run(tmp_path, "--build-limit", "1", "--skip-existing", loader=loader)
    assert first["n_builds"] == 1 and second["n_builds"] == 0 and loader.built == []
    rows = _rows(tmp_path / "results" / "DEV_dev_seed1" / "per_build.csv")
    triples = [(r["build"], r["method"], r["budget"]) for r in rows]
    assert len(triples) == len(set(triples)) == 3 * 3          # one build x 3 methods x 3 budgets
    assert {r["build"] for r in rows} == {KEYS[0]}


CLI_MODULES = ["experiments.run_experiment", "experiments.merge_shards", "src.data.source_cache",
               "src.data.make_eval_set_p2", "src.data.check_data", "src.data.extract_inputs",
               "src.obs.export_sample", "src.dante.compare_stored", "src.eval.compare_baselines",
               "src.agent.llm_smoke"]


def test_runner_help_renders():
    from experiments.run_experiment import build_parser
    text = build_parser().format_help()
    assert "--shard" in text and "position % n == i" in text


@pytest.mark.parametrize("module", CLI_MODULES)
def test_every_cli_help_exits_zero(module):
    """argparse help strings are %-formatted; an unescaped % breaks --help (and parsing on 3.14)."""
    import subprocess
    import sys
    from pathlib import Path
    r = subprocess.run([sys.executable, "-m", module, "--help"], capture_output=True, text=True, timeout=120,
                       cwd=Path(__file__).resolve().parent.parent)
    assert r.returncode == 0, r.stderr[-500:]
    assert "usage:" in r.stdout


def test_notebook_clone_cell_fails_loudly_and_hides_the_token():
    from pathlib import Path
    nb = json.loads((Path(__file__).resolve().parent.parent / "experiments" / "kaggle_runner.ipynb")
                    .read_text(encoding="utf-8"))
    clone = next("".join(c["source"]) for c in nb["cells"]
                 if c["cell_type"] == "code" and "GITHUB_TOKEN" in "".join(c["source"]))
    assert 'get_secret("GITHUB_TOKEN")' in clone                   # token only from the Kaggle Secret
    assert "capture_output=True" in clone                           # git output never shown raw
    assert 'replace(_token, "***")' in clone                        # errors masked
    assert "check=False" not in clone                               # no silent failure
    assert 'fetch", "--quiet", _url, REPO_REF' in clone             # fresh fetch even if the repo exists
    assert '"checkout", "--quiet", "--force", "FETCH_HEAD"' in clone
    assert "finally:" in clone and "set-url" in clone and "PUBLIC_URL" in clone   # remote reset in all cases
    assert "del _token, _url" in clone
    assert "ghp_" not in clone and "github_pat_" not in clone


def test_rerun_removes_the_stale_trace(tmp_path):
    cfg = _cfg(tmp_path)
    stale = tmp_path / "traces" / "DEV_dev_seed1" / f"{KEYS[0]}.jsonl"
    stale.parent.mkdir(parents=True)
    stale.write_text('{"stale": true}\n', encoding="utf-8")
    lines = []
    main(["--exp", "DEV", "--seed", "1", "--provider", "mock", "--methods", "LLM-relevance",
          "--build-limit", "1", "--skip-existing"], cfg=cfg, loader=KeyedLoader(), echo=lines.append)
    events = [json.loads(x) for x in stale.read_text(encoding="utf-8").splitlines()]
    assert events and all("stale" not in e for e in events)
    assert events[0]["step"] == 1                                   # one clean trajectory from step 1
    assert any(ln.startswith("removed stale trace") for ln in lines)


def test_merge_drops_failed_builds_that_later_succeeded(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    cols = merge_shards.PER_BUILD_COLUMNS
    row = {c: "" for c in cols}
    pd.DataFrame([{**row, "build": "B1", "method": "DANTE-CCH", "budget": "0.1"}], columns=cols).to_csv(
        run_dir / "per_build.shard0.csv", index=False)
    meta = {"run_id": "r", "started": "2026-11-06T10:00:00+00:00", "finished": "2026-11-06T10:05:00+00:00",
            "git_commit": "abc", "n_builds": 2, "shard": [0, 1], "skipped_existing": [],
            "failed_builds": [{"build": "B1", "error": "timeout in an earlier attempt"},
                              {"build": "B2", "error": "RuntimeError: still broken"}]}
    (run_dir / "run_meta.shard0.json").write_text(json.dumps(meta), encoding="utf-8")
    merge_shards.merge_run(run_dir)
    merged = json.loads((run_dir / "run_meta.json").read_text(encoding="utf-8"))
    assert [f["build"] for f in merged["failed_builds"]] == ["B2"]   # B1 now has rows, so it is not failed
