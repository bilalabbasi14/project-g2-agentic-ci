import json

import jsonschema
import pytest

from src.contracts import (
    BuildState, FallbackRecord, FinalRanking, RelevanceResponse, validate,
)
from src.settings import REPO_ROOT, load_config

EXAMPLES = REPO_ROOT / "docs" / "examples"


@pytest.mark.parametrize("name", [
    "build_state", "relevance_request", "relevance_response", "final_ranking", "fallback_record",
])
def test_examples_validate(name):
    validate(json.loads((EXAMPLES / f"{name}.json").read_text()), name)


def test_build_state_round_trip():
    d = json.loads((EXAMPLES / "build_state.json").read_text())
    state = BuildState.from_dict(d)
    assert state.to_dict() == d
    assert state.diff_summary.total_added == 4


def test_final_ranking_round_trip():
    d = json.loads((EXAMPLES / "final_ranking.json").read_text())
    assert FinalRanking.from_dict(d).to_dict() == d


def test_response_rejects_out_of_range_and_extra_keys():
    with pytest.raises(jsonschema.ValidationError):
        validate({"test": "a.B", "relevance": 1.5, "reason": "x"}, "relevance_response")
    with pytest.raises(jsonschema.ValidationError):
        validate({"test": "a.B", "relevance": 0.5, "reason": "x", "extra": 1}, "relevance_response")


def test_response_confidence_optional():
    r = RelevanceResponse.from_dict({"test": "a.B", "relevance": 0.5, "reason": "x"})
    assert r.confidence is None
    validate(r.to_dict(), "relevance_response")


def test_fallback_reason_checked():
    with pytest.raises(ValueError):
        FallbackRecord(build_id="b", reason="something_else")


def test_config_has_required_keys():
    cfg = load_config()
    assert cfg["project"] == "karaf"
    assert cfg["budgets"] == [0.05, 0.10, 0.20]
    for key in ("model", "base_url", "timeout_s"):
        assert key in cfg["llm"]
    assert cfg["shortlist"]["k"] > 0
