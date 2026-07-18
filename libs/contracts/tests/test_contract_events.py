from datetime import datetime
from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.enums import (
    ActorKind,
    DeliberationSessionState,
    GoalState,
    SubgoalAcceptanceStatus,
)
from mnemograph_contracts.events import (
    DeliberationSessionTransitionRecord,
    GoalTransitionRecord,
    SubgoalTransitionRecord,
)
from pydantic import ValidationError


def _actor() -> ActorRef:
    return ActorRef(kind=ActorKind.USER, actor_id=UUID("00000000-0000-0000-0000-000000000001"))


def test_transition_records_validate_and_normalize_utc() -> None:
    goal = GoalTransitionRecord(
        event_id=UUID("00000000-0000-0000-0000-000000000100"),
        goal_id=UUID("00000000-0000-0000-0000-000000000101"),
        version=0,
        previous_state=None,
        next_state=GoalState.DRAFT,
        actor=_actor(),
        occurred_at=datetime.fromisoformat("2026-01-01T10:00:00+07:00"),
    )
    assert goal.occurred_at.isoformat().endswith("+00:00")

    parsed = SubgoalTransitionRecord.model_validate_json(
        '{"event_id":"00000000-0000-0000-0000-000000000110","subgoal_id":"00000000-0000-0000-0000-000000000111","version":0,"previous_status":null,"next_status":"NOT_ACCEPTED","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"2026-01-01T10:00:00+07:00"}'
    )
    assert parsed.occurred_at.isoformat().endswith("+00:00")


def test_transition_previous_required_but_nullable() -> None:
    with pytest.raises(ValidationError):
        GoalTransitionRecord.model_validate_json(
            '{"event_id":"00000000-0000-0000-0000-000000000100","goal_id":"00000000-0000-0000-0000-000000000101","version":0,"next_state":"DRAFT","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"2026-01-01T00:00:00+00:00"}'
        )

    explicit_null = DeliberationSessionTransitionRecord.model_validate_json(
        '{"event_id":"00000000-0000-0000-0000-000000000120","session_id":"00000000-0000-0000-0000-000000000121","version":0,"previous_status":null,"next_status":"SESSION_ACTIVE","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"2026-01-01T00:00:00+00:00"}'
    )
    assert explicit_null.previous_status is None


def test_transition_negative_cases() -> None:
    with pytest.raises(ValidationError):
        DeliberationSessionTransitionRecord.model_validate_json(
            '{"event_id":"00000000-0000-0000-0000-000000000120","session_id":"00000000-0000-0000-0000-000000000121","version":0,"previous_status":null,"next_status":"UNKNOWN","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"2026-01-01T00:00:00+00:00"}'
        )
    with pytest.raises(ValidationError):
        GoalTransitionRecord.model_validate_json(
            '{"event_id":"00000000-0000-0000-0000-000000000100","goal_id":"00000000-0000-0000-0000-000000000101","version":0,"previous_state":null,"next_state":"DRAFT","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"bad"}'
        )
    with pytest.raises(ValidationError):
        GoalTransitionRecord.model_validate_json(
            '{"event_id":"00000000-0000-0000-0000-000000000100","goal_id":"00000000-0000-0000-0000-000000000101","version":0,"previous_state":null,"next_state":"DRAFT","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"2026-01-01T00:00:00"}'
        )
    with pytest.raises(ValidationError):
        GoalTransitionRecord(
            event_id=UUID("00000000-0000-0000-0000-000000000100"),
            goal_id=UUID("00000000-0000-0000-0000-000000000101"),
            version=0,
            previous_state=None,
            next_state=GoalState.DRAFT,
            actor=_actor(),
            occurred_at=datetime(2026, 1, 1, 0, 0, 0),
        )
    with pytest.raises(ValidationError):
        GoalTransitionRecord.model_validate_json(
            '{"event_id":"00000000-0000-0000-0000-000000000100","goal_id":"00000000-0000-0000-0000-000000000101","version":-1,"previous_state":null,"next_state":"DRAFT","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"2026-01-01T00:00:00+00:00"}'
        )
    with pytest.raises(ValidationError):
        GoalTransitionRecord.model_validate_json(
            '{"event_id":"00000000-0000-0000-0000-000000000100","goal_id":"00000000-0000-0000-0000-000000000101","version":0,"previous_state":null,"next_state":"DRAFT","actor":{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"},"occurred_at":"2026-01-01T00:00:00+00:00","extra":1}'
        )


def test_transition_schema_required_nullable_and_additional_properties() -> None:
    schemas = [
        GoalTransitionRecord.model_json_schema(),
        SubgoalTransitionRecord.model_json_schema(),
        DeliberationSessionTransitionRecord.model_json_schema(),
    ]
    nullable_fields = ["previous_state", "previous_status", "previous_status"]

    for schema, field_name in zip(schemas, nullable_fields, strict=True):
        assert schema["additionalProperties"] is False
        assert field_name in schema["required"]
        any_of = schema["properties"][field_name]["anyOf"]
        assert any(item.get("type") == "null" for item in any_of)


def test_all_transition_models_are_frozen() -> None:
    models = [
        GoalTransitionRecord(
            event_id=UUID("00000000-0000-0000-0000-000000000100"),
            goal_id=UUID("00000000-0000-0000-0000-000000000101"),
            version=0,
            previous_state=None,
            next_state=GoalState.DRAFT,
            actor=_actor(),
            occurred_at=datetime.fromisoformat("2026-01-01T00:00:00+00:00"),
        ),
        SubgoalTransitionRecord(
            event_id=UUID("00000000-0000-0000-0000-000000000110"),
            subgoal_id=UUID("00000000-0000-0000-0000-000000000111"),
            version=0,
            previous_status=SubgoalAcceptanceStatus.NOT_ACCEPTED,
            next_status=SubgoalAcceptanceStatus.USER_ACCEPTED,
            actor=_actor(),
            occurred_at=datetime.fromisoformat("2026-01-01T00:00:00+00:00"),
        ),
        DeliberationSessionTransitionRecord(
            event_id=UUID("00000000-0000-0000-0000-000000000120"),
            session_id=UUID("00000000-0000-0000-0000-000000000121"),
            version=0,
            previous_status=None,
            next_status=DeliberationSessionState.SESSION_ACTIVE,
            actor=_actor(),
            occurred_at=datetime.fromisoformat("2026-01-01T00:00:00+00:00"),
        ),
    ]

    for model in models:
        field_name = "version"
        with pytest.raises(ValidationError):
            setattr(model, field_name, 1)
