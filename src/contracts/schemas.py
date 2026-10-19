"""JSON Schemas for the structures in models.py, plus a validate() helper."""
import jsonschema

from .models import FALLBACK_REASONS, RANKING_SOURCES

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
}


def validate(instance, schema_name):
    """Raise jsonschema.ValidationError if instance does not match the named schema."""
    jsonschema.validate(instance, SCHEMAS[schema_name])
