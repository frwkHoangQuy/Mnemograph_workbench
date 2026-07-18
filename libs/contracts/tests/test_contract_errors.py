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


def _actor() -> ActorRef:
    return ActorRef(kind=ActorKind.USER, actor_id=UUID("00000000-0000-0000-0000-000000000001"))


def test_mapping_stable_codes() -> None:
    assert _map_pydantic_error_type("missing") is ValidationErrorCode.REQUIRED
    assert _map_pydantic_error_type("uuid_parsing") is ValidationErrorCode.INVALID_UUID
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
    with pytest.raises(ValidationError):
        env.code = "VALIDATION_ERROR"
