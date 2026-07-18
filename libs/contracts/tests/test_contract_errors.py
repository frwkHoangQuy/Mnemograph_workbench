from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.enums import ActorKind, ValidationErrorCode
from mnemograph_contracts.errors import (
    ValidationErrorEnvelope,
    ValidationIssue,
    _map_pydantic_error_type,
    _validation_error_to_envelope,
)
from mnemograph_contracts.events import GoalTransitionRecord
from pydantic import ValidationError

MAPPING_TABLE: dict[str, ValidationErrorCode] = {
    "missing": ValidationErrorCode.REQUIRED,
    "union_tag_not_found": ValidationErrorCode.REQUIRED,
    "extra_forbidden": ValidationErrorCode.UNKNOWN_FIELD,
    "uuid_parsing": ValidationErrorCode.INVALID_UUID,
    "uuid_type": ValidationErrorCode.INVALID_TYPE,
    "is_instance_of": ValidationErrorCode.INVALID_TYPE,
    "string_type": ValidationErrorCode.INVALID_TYPE,
    "int_type": ValidationErrorCode.INVALID_TYPE,
    "tuple_type": ValidationErrorCode.INVALID_TYPE,
    "model_type": ValidationErrorCode.INVALID_TYPE,
    "enum": ValidationErrorCode.INVALID_ENUM,
    "literal_error": ValidationErrorCode.INVALID_ENUM,
    "union_tag_invalid": ValidationErrorCode.INVALID_ENUM,
    "greater_than_equal": ValidationErrorCode.OUT_OF_RANGE,
    "greater_than": ValidationErrorCode.OUT_OF_RANGE,
    "less_than_equal": ValidationErrorCode.OUT_OF_RANGE,
    "less_than": ValidationErrorCode.OUT_OF_RANGE,
    "string_too_short": ValidationErrorCode.OUT_OF_RANGE,
    "too_short": ValidationErrorCode.OUT_OF_RANGE,
    "datetime_type": ValidationErrorCode.INVALID_TYPE,
    "datetime_parsing": ValidationErrorCode.INVALID_TYPE,
    "datetime_from_date_parsing": ValidationErrorCode.INVALID_TYPE,
    "datetime_object_invalid": ValidationErrorCode.INVALID_TYPE,
    "naive_datetime": ValidationErrorCode.NAIVE_DATETIME,
}


def _actor() -> ActorRef:
    return ActorRef(kind=ActorKind.USER, actor_id=UUID("00000000-0000-0000-0000-000000000001"))


@pytest.mark.parametrize("error_type, expected", list(MAPPING_TABLE.items()))
def test_mapping_stable_codes(error_type: str, expected: ValidationErrorCode) -> None:
    assert _map_pydantic_error_type(error_type) is expected


def test_mapping_fallback_to_invalid_value() -> None:
    assert _map_pydantic_error_type("frozen_instance") is ValidationErrorCode.INVALID_VALUE
    assert _map_pydantic_error_type("json_invalid") is ValidationErrorCode.INVALID_VALUE
    assert _map_pydantic_error_type("no_such_type") is ValidationErrorCode.INVALID_VALUE


def test_validation_error_envelope_conversion() -> None:
    with pytest.raises(ValidationError) as exc:
        GoalTransitionRecord.model_validate_json(
            '{"event_id":"00000000-0000-0000-0000-000000000100","goal_id":"00000000-0000-0000-0000-000000000101","version":0,"previous_state":null,"next_state":"DRAFT","actor":{"kind":"USER","actor_id":"not-a-uuid"},"occurred_at":"2026-01-01T00:00:00+00:00"}'
        )
    envelope = _validation_error_to_envelope(exc.value)
    assert envelope.code == "VALIDATION_ERROR"
    assert len(envelope.issues) >= 1
    assert all(isinstance(issue.path, tuple) for issue in envelope.issues)
    dump = envelope.model_dump(mode="json")
    assert "msg" not in str(dump)
    assert "ctx" not in str(dump)
    assert "url" not in str(dump)


def test_error_model_shapes() -> None:
    issue = ValidationIssue(path=(), code=ValidationErrorCode.INVALID_VALUE)
    assert issue.path == ()
    envelope = ValidationErrorEnvelope(code="VALIDATION_ERROR", issues=(issue,))
    assert len(envelope.issues) == 1


def test_error_negative_cases() -> None:
    with pytest.raises(ValidationError):
        ValidationErrorEnvelope(code="VALIDATION_ERROR", issues=())
    with pytest.raises(ValidationError):
        ValidationIssue.model_validate_json('{"path":[],"code":"UNKNOWN"}')


def test_error_json_array_materializes_to_tuple_and_is_frozen() -> None:
    env = ValidationErrorEnvelope.model_validate_json(
        '{"code":"VALIDATION_ERROR","issues":[{"path":["x",1],"code":"INVALID_TYPE"}]}'
    )
    assert isinstance(env.issues, tuple)
    assert isinstance(env.issues[0].path, tuple)

    issue = ValidationIssue(path=("x", 1), code=ValidationErrorCode.INVALID_TYPE)
    with pytest.raises(ValidationError):
        issue.code = ValidationErrorCode.INVALID_VALUE
    with pytest.raises(ValidationError):
        env.code = "VALIDATION_ERROR"


def test_error_schemas_match_plan_requirements() -> None:
    env_schema = ValidationErrorEnvelope.model_json_schema()
    issue_schema = ValidationIssue.model_json_schema()

    assert env_schema["additionalProperties"] is False
    assert env_schema["properties"]["issues"]["minItems"] == 1

    assert issue_schema["additionalProperties"] is False
    path_schema = issue_schema["properties"]["path"]
    assert path_schema["type"] == "array"
    item_any_of = path_schema["items"]["anyOf"]
    assert any(item.get("type") == "string" for item in item_any_of)
    assert any(item.get("type") == "integer" for item in item_any_of)
