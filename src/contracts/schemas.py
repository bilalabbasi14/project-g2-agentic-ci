"""JSON Schemas for the structures in models.py, plus a validate() helper."""
import jsonschema

from .models import (
    FALLBACK_REASONS, RANKING_SOURCES, RELEVANCE_SOURCES, TRACE_COMPONENTS, TRACE_EVENTS, WEIGHT_MODES,
)

_unit = {"type": "number", "minimum": 0, "maximum": 1}

FALLBACK_RECORD = {
    "type": "object",
    "required": ["build_id", "reason"],
    "properties": {
        "build_id": {"type": "string"},
        "reason": {"enum": list(FALLBACK_REASONS)},
        "detail": {"type": "string"},
        "test": {"type": ["string", "null"]},
    },
    "additionalProperties": False,
}

CANDIDATE_TEST = {
    "type": "object",
    "required": ["name", "duration"],
    "properties": {
        "name": {"type": "string"},
        "duration": {"type": "number", "minimum": 0},
        "history_score": {"type": "number"},
        "tfidf_score": {"type": "number"},
        "llm_relevance": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
        "final_score": {"type": ["number", "null"]},
    },
    "additionalProperties": False,
}

BUILD_STATE = {
    "type": "object",
    "required": ["build_id", "project", "budget_fraction", "budget_seconds", "diff_summary"],
    "properties": {
        "build_id": {"type": "string"},
        "project": {"type": "string"},
        "budget_fraction": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
        "budget_seconds": {"type": "number", "minimum": 0},
        "diff_summary": {
            "type": "object",
            "required": ["files"],
            "properties": {"files": {"type": "array", "items": {
                "type": "object",
                "required": ["path", "added_lines", "removed_lines"],
                "properties": {
                    "path": {"type": "string"},
                    "added_lines": {"type": "integer", "minimum": 0},
                    "removed_lines": {"type": "integer", "minimum": 0},
                },
                "additionalProperties": False,
            }}},
        },
        "candidates": {"type": "array", "items": CANDIDATE_TEST},
        "selected_tests": {"type": "array", "items": {"type": "string"}},
        "remaining_budget": {"type": "number"},
        "fallbacks": {"type": "array", "items": FALLBACK_RECORD},
    },
    "additionalProperties": False,
}

RELEVANCE_REQUEST = {
    "type": "object",
    "required": ["build_id", "test", "diff_chunk", "test_source"],
    "properties": {
        "build_id": {"type": "string"},
        "test": {"type": "string"},
        "diff_chunk": {"type": "string"},
        "test_source": {"type": "string"},
        "prompt_version": {"type": "string"},
    },
    "additionalProperties": False,
}

# What the model must return. Extra keys are rejected so drift is visible.
RELEVANCE_RESPONSE = {
    "type": "object",
    "required": ["test", "relevance", "reason"],
    "properties": {
        "test": {"type": "string", "minLength": 1},
        "relevance": _unit,
        "reason": {"type": "string", "minLength": 1},
        "confidence": _unit,
    },
    "additionalProperties": False,
}

FINAL_RANKING = {
    "type": "object",
    "required": ["build_id", "method", "source", "budget_fraction", "ordered_tests",
                 "selected_tests", "total_duration"],
    "properties": {
        "build_id": {"type": "string"},
        "method": {"type": "string"},
        "source": {"enum": list(RANKING_SOURCES)},
        "budget_fraction": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
        "ordered_tests": {"type": "array", "items": {"type": "string"}},
        "selected_tests": {"type": "array", "items": {"type": "string"}},
        "total_duration": {"type": "number", "minimum": 0},
        "scores": {"type": "object", "additionalProperties": {"type": "number"}},
    },
    "additionalProperties": False,
}

LLM_CALL_RECORD = {
    "type": "object",
    "required": ["model", "latency_s", "ok"],
    "properties": {
        "model": {"type": "string"},
        "latency_s": {"type": "number", "minimum": 0},
        "prompt_tokens": {"type": ["integer", "null"]},
        "completion_tokens": {"type": ["integer", "null"]},
        "ok": {"type": "boolean"},
        "error": {"type": ["string", "null"]},
        "cached": {"type": "boolean"},
        "component": {"enum": list(TRACE_COMPONENTS) + [None]},
    },
    "additionalProperties": False,
}

# ---------------------------------------------------------------- Phase 2 ----

METHOD_SPEC = {
    "type": "object",
    "required": ["name", "relevance_source", "weight_mode"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "relevance_source": {"enum": list(RELEVANCE_SOURCES)},
        "weight_mode": {"enum": list(WEIGHT_MODES)},
        "w": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
        "tuned_key": {"enum": ["tfidf", "llm", None]},
        "explainer": {"type": "boolean"},
    },
    "additionalProperties": False,
}

TOOL_CALL_RECORD = {
    "type": "object",
    "required": ["tool", "args", "output", "latency_s", "ok"],
    "properties": {
        "tool": {"type": "string"},
        "args": {"type": "object"},
        "output": {"type": "object"},
        "latency_s": {"type": "number", "minimum": 0},
        "ok": {"type": "boolean"},
        "error": {"type": ["string", "null"]},
    },
    "additionalProperties": False,
}

ORCHESTRATOR_INPUT = {
    "type": "object",
    "required": ["build_id", "features", "shortlist", "changed_files", "budget_fractions",
                 "relevance_source"],
    "properties": {
        "build_id": {"type": "string"},
        "features": {"type": "object", "additionalProperties": {"type": "number"}},
        "shortlist": {"type": "array", "items": {
            "type": "object",
            "required": ["test", "history_score", "tfidf_relevance", "llm_relevance", "duration"],
            "properties": {
                "test": {"type": "string"},
                "history_score": {"type": "number"},
                "tfidf_relevance": {"type": "number"},
                "llm_relevance": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
                "duration": {"type": "number", "minimum": 0},
            },
            "additionalProperties": False,
        }},
        "changed_files": {"type": "array", "items": {"type": "string"}},
        "budget_fractions": {"type": "array", "items": {"type": "number", "exclusiveMinimum": 0, "maximum": 1}},
        "relevance_source": {"enum": list(RELEVANCE_SOURCES)},
    },
    "additionalProperties": False,
}

ORCHESTRATOR_DECISION = {
    "type": "object",
    "required": ["build_id", "w", "confidence", "source", "reason", "steps", "tool_calls", "llm_calls"],
    "properties": {
        "build_id": {"type": "string"},
        "w": {"type": "number", "minimum": 0, "maximum": 1},
        "confidence": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
        "source": {"enum": ["agent", "fallback"]},
        "reason": {"type": "string"},
        "steps": {"type": "integer", "minimum": 0},
        "tool_calls": {"type": "array", "items": TOOL_CALL_RECORD},
        "llm_calls": {"type": "integer", "minimum": 0},
        "fallback": {"anyOf": [{"type": "null"}, FALLBACK_RECORD]},
        "prompt_version": {"type": "string"},
    },
    "additionalProperties": False,
}

EXPLANATION_RECORD = {
    "type": "object",
    "required": ["build_id", "budget_fraction", "test", "rank_by_value", "evidence", "justification",
                 "cited_facts", "ok", "error", "latency_s", "prompt_tokens", "completion_tokens"],
    "properties": {
        "build_id": {"type": "string"},
        "budget_fraction": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
        "test": {"type": "string"},
        "rank_by_value": {"type": "integer", "minimum": 1},
        "evidence": {"type": "object"},
        "justification": {"type": ["string", "null"]},
        "cited_facts": {"type": "array", "items": {"type": "string"}},
        "ok": {"type": "boolean"},
        "error": {"type": ["string", "null"]},
        "latency_s": {"type": "number", "minimum": 0},
        "prompt_tokens": {"type": ["integer", "null"]},
        "completion_tokens": {"type": ["integer", "null"]},
        "prompt_version": {"type": "string"},
    },
    "additionalProperties": False,
}

TRACE_EVENT = {
    "type": "object",
    "required": ["run_id", "build_id", "component", "event", "step", "payload"],
    "properties": {
        "run_id": {"type": "string"},
        "build_id": {"type": "string"},
        "component": {"enum": list(TRACE_COMPONENTS)},
        "event": {"enum": list(TRACE_EVENTS)},
        "step": {"type": "integer", "minimum": 1},
        "payload": {"type": "object"},
        "latency_s": {"type": ["number", "null"], "minimum": 0},
        "ts": {"type": "string"},
    },
    "additionalProperties": False,
}

# --- LLM output schemas: what a model answer must look like before it is used ---

_reason = {"type": "string", "minLength": 1, "maxLength": 300}

ORCHESTRATOR_STEP = {
    "oneOf": [
        {
            "type": "object",
            "required": ["action", "tool", "args", "reason"],
            "properties": {
                "action": {"const": "call_tool"},
                "tool": {"enum": ["history_retrieval", "diff_reader"]},
                "args": {"type": "object"},
                "reason": _reason,
            },
            "additionalProperties": False,
        },
        {
            "type": "object",
            "required": ["action", "w", "confidence", "reason"],
            "properties": {
                "action": {"const": "final"},
                "w": _unit,
                "confidence": _unit,
                "reason": _reason,
            },
            "additionalProperties": False,
        },
    ],
}

EXPLANATION_RESPONSE = {
    "type": "object",
    "required": ["test", "justification", "cited_facts"],
    "properties": {
        "test": {"type": "string", "minLength": 1},
        "justification": {"type": "string", "minLength": 1, "maxLength": 400},
        "cited_facts": {"type": "array", "minItems": 1, "maxItems": 6,
                        "items": {"type": "string", "minLength": 1, "maxLength": 200}},
    },
    "additionalProperties": False,
}

SINGLE_CALL_RESPONSE = {
    "type": "object",
    "required": ["scores"],
    "properties": {
        "scores": {"type": "array", "items": {
            "type": "object",
            "required": ["test", "relevance"],
            "properties": {"test": {"type": "string", "minLength": 1}, "relevance": _unit},
            "additionalProperties": False,
        }},
    },
    "additionalProperties": False,
}

SCHEMAS = {
    "build_state": BUILD_STATE,
    "relevance_request": RELEVANCE_REQUEST,
    "relevance_response": RELEVANCE_RESPONSE,
    "final_ranking": FINAL_RANKING,
    "fallback_record": FALLBACK_RECORD,
    "llm_call_record": LLM_CALL_RECORD,
    "method_spec": METHOD_SPEC,
    "tool_call_record": TOOL_CALL_RECORD,
    "orchestrator_input": ORCHESTRATOR_INPUT,
    "orchestrator_decision": ORCHESTRATOR_DECISION,
    "explanation_record": EXPLANATION_RECORD,
    "trace_event": TRACE_EVENT,
    "orchestrator_step": ORCHESTRATOR_STEP,
    "explanation_response": EXPLANATION_RESPONSE,
    "single_call_response": SINGLE_CALL_RESPONSE,
}


def validate(instance, schema_name):
    """Raise jsonschema.ValidationError if instance does not match the named schema."""
    jsonschema.validate(instance, SCHEMAS[schema_name])
