"""Copy chosen build traces into logs_sample/ and render them as readable Markdown.

    python -m src.obs.export_sample --run-id E3_test_seed1 --builds PR-1840_build4 PR-2001_build2 [--n 10] [--out logs_sample]

For each build: <trace dir>/<run_id>/<build>.jsonl is copied to
<out>/<run_id>/<build>.jsonl and <out>/<run_id>/<build>.md is written with one
numbered section per event (time, component, event, latency, payload;
prompts and responses in fenced code blocks). With --n, the first n builds of
the run in alphabetical order are exported.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

from src.settings import load_config, repo_path

TEXT_KEYS = ("prompt", "response")


def render_markdown(events, build_id, run_id):
    """Markdown for one build's events, in step order."""
    lines = [f"# Trace of {build_id}", "", f"Run: `{run_id}` · events: {len(events)}", ""]
    for ev in sorted(events, key=lambda e: e["step"]):
        latency = "—" if ev.get("latency_s") is None else f"{ev['latency_s']:.3f} s"
        lines += [f"## {ev['step']}. {ev['component']} · {ev['event']}", "",
                  f"- time: {ev.get('ts') or '—'}", f"- latency: {latency}", ""]
        payload = dict(ev.get("payload") or {})
        texts = {k: payload.pop(k) for k in TEXT_KEYS if isinstance(payload.get(k), str)}
        if payload:
            lines += ["```json", json.dumps(payload, indent=2, ensure_ascii=False), "```", ""]
        for k, text in texts.items():
            lines += [f"**{k}**", "", "```text", text.replace("```", "'''"), "```", ""]
    return "\n".join(lines)


def export(trace_dir, run_id, builds, out_dir):
    """Copy and render the given builds; returns the written Markdown paths."""
    src_dir = Path(trace_dir) / run_id
    dest = Path(out_dir) / run_id
    dest.mkdir(parents=True, exist_ok=True)
    written = []
    for b in builds:
        src = src_dir / f"{b}.jsonl"
        if not src.exists():
            raise FileNotFoundError(f"no trace for build {b}: {src}")
        shutil.copyfile(src, dest / f"{b}.jsonl")
        events = [json.loads(line) for line in src.read_text(encoding="utf-8").splitlines() if line.strip()]
        md = dest / f"{b}.md"
        md.write_text(render_markdown(events, b, run_id), encoding="utf-8")
        written.append(md)
    return written


def main(argv=None):
    cfg = load_config()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--builds", nargs="+")
    ap.add_argument("--n", type=int, help="export the first n builds of the run (alphabetical)")
    ap.add_argument("--out", default="logs_sample")
    ap.add_argument("--trace-dir", default=cfg["trace"]["dir"])
    args = ap.parse_args(argv)
    trace_dir = repo_path(args.trace_dir)
    builds = list(args.builds or [])
    if not builds and args.n:
        builds = sorted(p.stem for p in (trace_dir / args.run_id).glob("*.jsonl"))[:args.n]
    if not builds:
        ap.error("give --builds and/or --n")
    for md in export(trace_dir, args.run_id, builds, repo_path(args.out)):
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
