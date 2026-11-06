# State and contracts

All structures live in `src/contracts/models.py` (dataclasses) and are validated
against JSON Schemas in `src/contracts/schemas.py` via `validate(obj, name)`.
Illustrative instances (synthetic values, not real data) are in `docs/examples/`.

## BuildState (`build_state`)

Per-build working state carried through the pipeline.

| field | type | meaning |
|---|---|---|
| `build_id` | str | LRTS build key `<pr_name>_build<build_id>`, e.g. `PR-1840_build4` |
| `project` | str | LRTS project name |
| `budget_fraction` | float (0,1] | budget as a fraction of total suite duration |
| `budget_seconds` | float | absolute budget for this build |
| `diff_summary.files[]` | `{path, added_lines, removed_lines}` | changed files kept after extension filtering |
| `candidates[]` | CandidateTest | tests eligible for selection |
| `selected_tests[]` | str | selected test classes, in run order |
| `remaining_budget` | float | `budget_seconds - sum(selected durations)` |
| `fallbacks[]` | FallbackRecord | fallbacks raised while processing this build |

CandidateTest: `name`, `duration`, `history_score`, `tfidf_score`,
`llm_relevance` (null until scored), `final_score` (null until combined).

## Relevance call

Request (`relevance_request`): `build_id`, `test`, `diff_chunk` (anonymised:
commit hashes, `index` lines, author/e-mail/date lines and timestamps removed;
truncated to `llm.max_diff_chars`), `test_source` (truncated to
`llm.max_test_chars`), `prompt_version`.

Response (`relevance_response`), the JSON object the model must return:

```json
{"test": "<fqn>", "relevance": 0.0-1.0, "reason": "<one sentence>", "confidence": 0.0-1.0}
```

`confidence` is optional. No other keys are allowed.

A response is rejected (and a fallback recorded) when:

| reason | condition |
|---|---|
| `timeout` | provider did not answer within `llm.timeout_s` |
| `provider_error` | connection or HTTP error |
| `invalid_json` | output is not parseable JSON |
| `schema_violation` | JSON does not match the schema, or `test` names a different test |
| `low_confidence` | `confidence` present and below `fallback.min_confidence` |

## FallbackRecord (`fallback_record`)

`build_id`, `reason` (one of the five above), `detail`, `test` (null = whole build).
With `fallback.scope: build`, any rejected call makes the whole build use the
supplied DANTE ranking; all records are kept in `BuildState.fallbacks` and
appended to `logs/fallbacks.jsonl`.

## LLMCallRecord (`llm_call_record`)

`model`, `latency_s`, `prompt_tokens`, `completion_tokens` (from Ollama's
`prompt_eval_count` / `eval_count`; null when not reported), `ok`, `error`.

## FinalRanking (`final_ranking`)

`build_id`, `method`, `source` (`llm`, `dante_fallback`, `dante`, `random`,
`history_only`, `tfidf_only`), `budget_fraction`, `ordered_tests` (full ranking),
`selected_tests` (greedy prefix that fits the budget; tests that do not fit are
skipped and scanning continues), `total_duration`, `scores`.

## Phase 2 structures

Added in P2-03. Constants in `src/contracts/models.py`: `RELEVANCE_SOURCES`,
`WEIGHT_MODES`, `TRACE_COMPONENTS`, `TRACE_EVENTS` and `DANTE_W = 2/3` (the
history weight that gives exactly DANTE's ranking, see
`tests/test_weight_equivalence.py`). The component interfaces are `typing.Protocol`
classes in `src/contracts/interfaces.py`; deterministic fakes for tests are in
`tests/fakes.py`.

`LLMCallRecord` gains two optional fields: `cached` (the answer came from the LLM
cache; latency and tokens are the original call's) and `component` (one of
`TRACE_COMPONENTS`, or null). Records created without them still validate.

### MethodSpec (`method_spec`)

One evaluated method: `name`, `relevance_source` (`none`, `tfidf`,
`llm_shortlist`, `llm_all_individual`, `llm_single_call`), `weight_mode`
(`random`, `history_only`, `relevance_only`, `fixed`, `tuned`, `agent`), `w`
(required in [0, 1] for `fixed`), `tuned_key` (`tfidf` or `llm`, required for
`tuned`) and `explainer`. `agent` mode needs a relevance source other than `none`.
Example: `docs/examples/method_spec.json`.

```json
{"name": "Agent-weighted", "relevance_source": "llm_shortlist", "weight_mode": "agent",
 "w": null, "tuned_key": null, "explainer": false}
```

### ToolCallRecord (`tool_call_record`)

One tool call: `tool`, `args`, `output`, `latency_s`, `ok`, `error`. A failed
call has `ok: false` and an error string; the registry never raises.

```json
{"tool": "history_retrieval", "args": {"test": "org.example.cache.LruCacheTest"},
 "output": {"runs": 98, "failures": 0}, "latency_s": 0.002, "ok": true, "error": null}
```

### OrchestratorInput (`orchestrator_input`)

What the orchestrator sees for one build: `build_id`, `features` (numbers only),
`shortlist` (items with `test`, `history_score`, `tfidf_relevance`,
`llm_relevance` (null for non-LLM sources) and `duration`), `changed_files`,
`budget_fractions`, `relevance_source`. Never contains target-build outcomes.

```json
{"build_id": "PR-0000_build1", "features": {"n_code_files": 1.0, "hist_max": 0.2},
 "shortlist": [{"test": "org.example.cache.LruCacheTest", "history_score": 0.2,
                "tfidf_relevance": 0.9, "llm_relevance": 0.8, "duration": 30.0}],
 "changed_files": ["core/src/main/java/org/example/cache/LruCache.java"],
 "budget_fractions": [0.05, 0.1, 0.2], "relevance_source": "llm_shortlist"}
```

### OrchestratorDecision (`orchestrator_decision`)

The w chosen for one build: `w`, `confidence`, `source` (`agent`, or
`fallback` with `w = 2/3` and a `fallback` FallbackRecord), `reason`, `steps`
(LLM calls made), `tool_calls` (ToolCallRecords), `llm_calls`,
`prompt_version`. Example: `docs/examples/orchestrator_decision.json`.

```json
{"build_id": "PR-0000_build1", "w": 0.6666667, "confidence": null, "source": "fallback",
 "reason": "invalid answer after retry", "steps": 2, "tool_calls": [], "llm_calls": 2,
 "fallback": {"build_id": "PR-0000_build1", "reason": "invalid_json", "detail": "", "test": null},
 "prompt_version": "o1"}
```

### ExplanationRecord (`explanation_record`)

One justification for a skipped test: `build_id`, `budget_fraction`, `test`,
`rank_by_value` (1 = first in the ranking), `evidence` (exactly what the LLM was
given), `justification` and `cited_facts` (null and empty when `ok` is false),
`ok`, `error`, `latency_s`, `prompt_tokens`, `completion_tokens`,
`prompt_version`. Example: `docs/examples/explanation_record.json`.

### TraceEvent (`trace_event`)

One step of an agent trajectory: `run_id`, `build_id`, `component` (one of
`TRACE_COMPONENTS`), `event` (`llm_call`, `tool_call`, `decision`, `fallback`,
`state`, `explanation`), `step` (starts at 1 per build), `payload`, `latency_s`,
`ts` (ISO-8601 UTC). Example: `docs/examples/trace_event.json`.

### LLM output schemas

Every model answer is validated before use; all have `additionalProperties: false`.

`orchestrator_step` is one of two shapes:

```json
{"action": "call_tool", "tool": "history_retrieval", "args": {"test": "org.example.cache.LruCacheTest"},
 "reason": "Check whether this relevant test failed recently."}
```

```json
{"action": "final", "w": 0.45, "confidence": 0.7, "reason": "Relevant tests have no failure history."}
```

`tool` is `history_retrieval` or `diff_reader`; `w` and `confidence` are in [0, 1];
`reason` has 1-300 characters.

`explanation_response`: `test`, `justification` (1-400 characters) and
`cited_facts` (1-6 strings of 1-200 characters).

```json
{"test": "org.example.web.ServletTest",
 "justification": "It never failed in 98 runs and its 100 s run did not fit the 90 s left.",
 "cited_facts": ["failures: 0 of 98 runs", "duration_s: 100.0"]}
```

`single_call_response`: `scores`, a list of `{"test", "relevance"}` items with
relevance in [0, 1] and no other keys.

```json
{"scores": [{"test": "org.example.cache.LruCacheTest", "relevance": 0.9},
            {"test": "org.example.web.ServletTest", "relevance": 0.0}]}
```
