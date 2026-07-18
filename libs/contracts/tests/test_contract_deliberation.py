import json
from typing import Any
from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.deliberation import (
    ContinueInterventionRecord,
    CorrectContextInterventionRecord,
    DeliberationSessionRecord,
    DeliberationTurnRecord,
    GuideInterventionRecord,
    InterventionRecord,
    PauseInterventionRecord,
    ReopenCheckpointInterventionRecord,
    ReopenSubgoalInterventionRecord,
    ReviseScopeInterventionRecord,
    StopInterventionRecord,
    UserCheckpointRecord,
)
from mnemograph_contracts.enums import ActorKind, DeliberationSessionState
from pydantic import TypeAdapter, ValidationError


def _actor() -> ActorRef:
    return ActorRef(kind=ActorKind.SYSTEM, actor_id=UUID("00000000-0000-0000-0000-000000000001"))


def test_deliberation_records_valid() -> None:
    session = DeliberationSessionRecord(
        session_id=UUID("00000000-0000-0000-0000-000000000010"),
        subgoal_id=UUID("00000000-0000-0000-0000-000000000011"),
        version=0,
        state=DeliberationSessionState.SESSION_ACTIVE,
    )
    assert session.parent_session_id is None

    turn = DeliberationTurnRecord(
        turn_id=UUID("00000000-0000-0000-0000-000000000012"),
        session_id=session.session_id,
        sequence=0,
        author=_actor(),
        content="hello",
    )
    assert turn.content == "hello"

    checkpoint = UserCheckpointRecord(
        checkpoint_id=UUID("00000000-0000-0000-0000-000000000013"),
        session_id=session.session_id,
        sequence=0,
    )
    assert checkpoint.sequence == 0


def test_intervention_record_union_validates_all_eight() -> None:
    adapter: TypeAdapter[InterventionRecord] = TypeAdapter(InterventionRecord)
    common = {
        "intervention_id": "00000000-0000-0000-0000-000000000020",
        "sequence": 0,
        "actor": {"kind": "SYSTEM", "actor_id": "00000000-0000-0000-0000-000000000001"},
        "expected_version": 0,
    }
    payloads: list[dict[str, Any]] = [
        {**common, "session_id": "00000000-0000-0000-0000-000000000010", "action": "CONTINUE"},
        {
            **common,
            "session_id": "00000000-0000-0000-0000-000000000010",
            "action": "GUIDE",
            "guidance": "g",
        },
        {
            **common,
            "session_id": "00000000-0000-0000-0000-000000000010",
            "action": "CORRECT_CONTEXT",
            "correction": "c",
        },
        {
            **common,
            "session_id": "00000000-0000-0000-0000-000000000010",
            "action": "REVISE_SCOPE",
            "revision": "r",
        },
        {**common, "session_id": "00000000-0000-0000-0000-000000000010", "action": "PAUSE"},
        {**common, "session_id": "00000000-0000-0000-0000-000000000010", "action": "STOP"},
        {
            **common,
            "session_id": "00000000-0000-0000-0000-000000000010",
            "action": "REOPEN",
            "target_kind": "CHECKPOINT",
            "checkpoint_id": "00000000-0000-0000-0000-000000000021",
        },
        {
            **common,
            "subgoal_id": "00000000-0000-0000-0000-000000000011",
            "action": "REOPEN",
            "target_kind": "SUBGOAL",
        },
    ]
    for payload in payloads:
        adapter.validate_json(json.dumps(payload))

    native_payload = {
        "intervention_id": UUID("00000000-0000-0000-0000-000000000020"),
        "session_id": UUID("00000000-0000-0000-0000-000000000010"),
        "sequence": 0,
        "actor": _actor(),
        "expected_version": 0,
        "action": "CONTINUE",
    }
    adapter.validate_python(native_payload)


def test_deliberation_discriminator_missing_or_invalid() -> None:
    adapter: TypeAdapter[InterventionRecord] = TypeAdapter(InterventionRecord)
    with pytest.raises(ValidationError) as exc_missing:
        adapter.validate_json(
            json.dumps(
                {
                    "intervention_id": "00000000-0000-0000-0000-000000000020",
                    "session_id": "00000000-0000-0000-0000-000000000010",
                    "sequence": 0,
                    "actor": {
                        "kind": "SYSTEM",
                        "actor_id": "00000000-0000-0000-0000-000000000001",
                    },
                    "expected_version": 0,
                }
            )
        )
    assert exc_missing.value.errors()[0]["type"] == "union_tag_not_found"

    with pytest.raises(ValidationError) as exc_invalid:
        adapter.validate_json(
            json.dumps(
                {
                    "intervention_id": "00000000-0000-0000-0000-000000000020",
                    "session_id": "00000000-0000-0000-0000-000000000010",
                    "sequence": 0,
                    "actor": {
                        "kind": "SYSTEM",
                        "actor_id": "00000000-0000-0000-0000-000000000001",
                    },
                    "expected_version": 0,
                    "action": "UNKNOWN",
                }
            )
        )
    assert exc_invalid.value.errors()[0]["type"] == "union_tag_invalid"


def test_deliberation_negative_and_missing_fields_fail() -> None:
    with pytest.raises(ValidationError):
        DeliberationSessionRecord.model_validate_json(
            '{"session_id":"00000000-0000-0000-0000-000000000010","subgoal_id":"00000000-0000-0000-0000-000000000011","version":0,"state":"SESSION_UNKNOWN"}'
        )
    with pytest.raises(ValidationError):
        DeliberationTurnRecord(
            turn_id=UUID("00000000-0000-0000-0000-000000000012"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            author=_actor(),
            content="",
        )
    with pytest.raises(ValidationError):
        GuideInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="GUIDE",
            guidance="",
        )
    with pytest.raises(ValidationError):
        CorrectContextInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="CORRECT_CONTEXT",
            correction="",
        )
    with pytest.raises(ValidationError):
        ReviseScopeInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="REVISE_SCOPE",
            revision="",
        )

    adapter: TypeAdapter[InterventionRecord] = TypeAdapter(InterventionRecord)
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({"action": "CONTINUE"}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({"action": "REOPEN"}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({"action": "REOPEN", "target_kind": "INVALID"}))

    with pytest.raises(ValidationError):
        adapter.validate_python(
            {
                "intervention_id": UUID("00000000-0000-0000-0000-000000000020"),
                "session_id": UUID("00000000-0000-0000-0000-000000000010"),
                "sequence": -1,
                "actor": _actor(),
                "expected_version": 0,
                "action": "CONTINUE",
            }
        )
    with pytest.raises(ValidationError):
        adapter.validate_python(
            {
                "intervention_id": UUID("00000000-0000-0000-0000-000000000020"),
                "session_id": UUID("00000000-0000-0000-0000-000000000010"),
                "sequence": 0,
                "actor": _actor(),
                "expected_version": -1,
                "action": "CONTINUE",
            }
        )


def test_intervention_record_schema_shape_and_literals() -> None:
    schema = TypeAdapter(InterventionRecord).json_schema()
    assert len(schema["oneOf"]) == 8

    defs = schema.get("$defs", {})
    expected_actions = {
        "ContinueInterventionRecord": "CONTINUE",
        "GuideInterventionRecord": "GUIDE",
        "CorrectContextInterventionRecord": "CORRECT_CONTEXT",
        "ReviseScopeInterventionRecord": "REVISE_SCOPE",
        "PauseInterventionRecord": "PAUSE",
        "StopInterventionRecord": "STOP",
        "ReopenCheckpointInterventionRecord": "REOPEN",
        "ReopenSubgoalInterventionRecord": "REOPEN",
    }
    for model_name, literal in expected_actions.items():
        model_schema = defs[model_name]
        assert "action" in model_schema["required"]
        assert model_schema["properties"]["action"]["const"] == literal

    assert "target_kind" in defs["ReopenCheckpointInterventionRecord"]["required"]
    assert (
        defs["ReopenCheckpointInterventionRecord"]["properties"]["target_kind"]["const"]
        == "CHECKPOINT"
    )
    assert "target_kind" in defs["ReopenSubgoalInterventionRecord"]["required"]
    assert (
        defs["ReopenSubgoalInterventionRecord"]["properties"]["target_kind"]["const"] == "SUBGOAL"
    )


def test_all_deliberation_models_are_frozen() -> None:
    models = [
        DeliberationSessionRecord(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            subgoal_id=UUID("00000000-0000-0000-0000-000000000011"),
            version=0,
            state=DeliberationSessionState.SESSION_ACTIVE,
        ),
        DeliberationTurnRecord(
            turn_id=UUID("00000000-0000-0000-0000-000000000012"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            author=_actor(),
            content="content",
        ),
        UserCheckpointRecord(
            checkpoint_id=UUID("00000000-0000-0000-0000-000000000013"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
        ),
        ContinueInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="CONTINUE",
        ),
        GuideInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="GUIDE",
            guidance="g",
        ),
        CorrectContextInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="CORRECT_CONTEXT",
            correction="c",
        ),
        ReviseScopeInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="REVISE_SCOPE",
            revision="r",
        ),
        PauseInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="PAUSE",
        ),
        StopInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="STOP",
        ),
        ReopenCheckpointInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="REOPEN",
            target_kind="CHECKPOINT",
            checkpoint_id=UUID("00000000-0000-0000-0000-000000000021"),
        ),
        ReopenSubgoalInterventionRecord(
            intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
            subgoal_id=UUID("00000000-0000-0000-0000-000000000011"),
            sequence=0,
            actor=_actor(),
            expected_version=0,
            action="REOPEN",
            target_kind="SUBGOAL",
        ),
    ]

    for model in models:
        field_name = next(iter(type(model).model_fields.keys()))
        with pytest.raises(ValidationError):
            setattr(model, field_name, getattr(model, field_name))
