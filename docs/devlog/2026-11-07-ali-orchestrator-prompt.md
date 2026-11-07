# Orchestrator prompt: o1 copied its example, o2 decides per build

Date: 2026-11-07
Author: Muhammad Ali

## Observed failure or limitation

Issue #6 fixes a rule for the orchestrator prompt: run `Agent-weighted` on the **dev split** (seed 1), and improve the prompt if the orchestrator falls back on more than 20% of builds or gives the same w for every build.

With prompt **o1**, the dev run `DEV_orch_o1` (Kaggle, commit a11b865, 10 builds) gave **w = 0.5 with confidence 0.8 on every build**. It made no tool calls, took one step each time and never fell back. These are exactly the values of the example final answer in the o1 prompt (`{"action": "final", "w": 0.5, "confidence": 0.8, ...}`): the model copied the example instead of deciding per build. The rule is triggered (`rule_triggered = True` in `results/dev/orchestrator_prompt_iterations.csv`). With a constant w, Agent-weighted is not a per-build decision at all; it is a fixed weight of 0.5.

## Change

Prompt **o2** (`src/agent/orchestrator.py`, `PROMPT_TEMPLATE_O2`; `ORCH_PROMPT_VERSION = "o2"`):
- **Placeholders only.** The answer shapes contain no numbers the model could copy: `"w": <your weight for this build, from 0 to 1>`. Neither the o1 example values nor DANTE's 0.67 appear in the instructions; the only numbers are the 0–1 range and the formula's exponent 1.2. A test checks this.
- **Guidance.** The prompt explains which build features should lower w (a strong, specific relevance signal and a focused change) and which should raise it (flat or weak relevance, informative history). It says builds differ and should usually get different w, and it asks for a reason naming the deciding features.
- **Selection.** `orchestrator.prompt_version` in `config.yaml` and `config_kaggle.yaml` now selects the template (o1 stays available for the record), and `run_meta.json` records the version that actually ran.

**One o2 attempt ran o1 by mistake.** The first o2 run on Kaggle used o1, because `config_kaggle.yaml` still said `prompt_version: o1`. `run_meta.json` recorded o1, and the decisions repeated o1's w = 0.5 / confidence 0.8 on all 10 builds. That repeat is not committed, but it shows that o1's behaviour reproduces in a second session. The config was fixed, and a new test checks that `config_kaggle.yaml` differs from `config.yaml` only in paths. A later rerun into the same run folder was skipped by `--skip-existing`, and that zip was discarded too: its merged `run_meta.json` claimed o2 while its rows were o1 data, and only its `git_commit_warning` showed the mix. The committed o2 run was made from a cleared folder.

## Measured effect

Dev split, 10 builds, seed 1; both runs on Kaggle. The numbers come from `results/dev/orchestrator_prompt_iterations.csv`, written by `python -m src.agent.orchestrator_eval --runs results/DEV_orch_o1 results/DEV_orch_o2`:

| prompt | run | fallback rate | distinct w | w min / mean / max | mean confidence | tool calls per build | SAPFDc@10%: Agent-weighted | LLM-relevance | DANTE-CCH | rule triggered |
|---|---|---|---|---|---|---|---|---|---|---|
| o1 | DEV_orch_o1 (a11b865) | 0.0 | 1 | 0.5 / 0.50 / 0.5 | 0.80 | 0.0 | 0.6770 | 0.6725 | 0.5530 | yes |
| o2 | DEV_orch_o2 (6d620f2) | 0.0 | 5 | 0.2 / 0.47 / 0.8 | 0.76 | 0.0 | 0.6656 | 0.6725 | 0.5530 | no |

- **The rule is satisfied.** o2 gives varied w (0.2, 0.3, 0.5, 0.7, 0.8) and never falls back, so the iteration stops at o2, as the rule in issue #6 says. o2 is the prompt for the runs.
- **Ranking on dev.** o2's per-build weights rank slightly worse on dev than o1's constant 0.5: Agent-weighted SAPFDc@10% is 0.6656 against 0.6770. LLM-relevance (fixed w = 2/3) is 0.6725. The rule does not choose by SAPFDc, and was not changed after seeing these numbers.
- **Remaining weaknesses, for the failure analysis (P2-14) and the paper:**
  - Several o2 reasons point the wrong way. For example, "Low relevance signal and weak history indicate a need to trust relevance more" comes with w = 0.3, while the prompt says weak relevance should raise w.
  - o2 still never calls a tool.
  - The feature list in the prompt still describes `n_rel_ge_05` as "relevance >= 0.5" (shared with o1), so one copyable number remains in the build data shown to the model.
- **Test split.** No test-split run was made for this choice.
