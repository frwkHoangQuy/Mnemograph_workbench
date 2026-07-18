import json
from typing import Any
from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.deliberation import (
    ContinueInterventionRecord,
    DeliberationSessionRecord,
    DeliberationTurnRecord,
    GuideInterventionRecord,
    InterventionRecord,
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
    schema = adapter.json_schema()
    assert len(schema["oneOf"]) == 8


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

    adapter: TypeAdapter[InterventionRecord] = TypeAdapter(InterventionRecord)
    with pytest.raises(ValidationError):
        adapter.validate_python({"action": "CONTINUE"})
    with pytest.raises(ValidationError):
        adapter.validate_python({"action": "REOPEN"})
    with pytest.raises(ValidationError):
        adapter.validate_python({"action": "REOPEN", "target_kind": "INVALID"})
    with pytest.raises(ValidationError):
        adapter.validate_python(
            {
                "intervention_id": "00000000-0000-0000-0000-000000000020",
                "session_id": "00000000-0000-0000-0000-000000000010",
                "sequence": -1,
                "actor": {"kind": "SYSTEM", "actor_id": "00000000-0000-0000-0000-000000000001"},
                "expected_version": 0,
                "action": "CONTINUE",
            }
        )
    with pytest.raises(ValidationError):
        adapter.validate_python(
            {
                "intervention_id": "00000000-0000-0000-0000-000000000020",
                "session_id": "00000000-0000-0000-0000-000000000010",
                "sequence": 0,
                "actor": {"kind": "SYSTEM", "actor_id": "00000000-0000-0000-0000-000000000001"},
                "expected_version": -1,
                "action": "CONTINUE",
            }
        )


def test_deliberation_models_are_frozen() -> None:
    record = ContinueInterventionRecord(
        intervention_id=UUID("00000000-0000-0000-0000-000000000020"),
        session_id=UUID("00000000-0000-0000-0000-000000000010"),
        sequence=0,
        actor=_actor(),
        expected_version=0,
        action="CONTINUE",
    )
    with pytest.raises(ValidationError):
        record.sequence = 1
