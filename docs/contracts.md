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
