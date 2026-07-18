import json
from typing import Any
from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.commands import (
    AcceptSubgoalCommand,
    ContinueDeliberationCommand,
    CorrectContextCommand,
    GuideDeliberationCommand,
    InterventionCommand,
    PauseDeliberationCommand,
    ReopenCheckpointCommand,
    ReopenSubgoalCommand,
    ReviseScopeCommand,
    StopDeliberationCommand,
)
from mnemograph_contracts.enums import ActorKind
from pydantic import TypeAdapter, ValidationError


def _actor() -> ActorRef:
    return ActorRef(kind=ActorKind.USER, actor_id=UUID("00000000-0000-0000-0000-000000000001"))


def _base(action: str) -> dict[str, Any]:
    return {
        "session_id": "00000000-0000-0000-0000-000000000010",
        "actor": {"kind": "USER", "actor_id": "00000000-0000-0000-0000-000000000001"},
        "expected_version": 0,
        "action": action,
    }


def test_intervention_command_alias_validates_all_branches() -> None:
    adapter: TypeAdapter[InterventionCommand] = TypeAdapter(InterventionCommand)
    payloads = [
        _base("CONTINUE"),
        {**_base("GUIDE"), "guidance": "g"},
        {**_base("CORRECT_CONTEXT"), "correction": "c"},
        {**_base("REVISE_SCOPE"), "revision": "r"},
        _base("PAUSE"),
        _base("STOP"),
        {
            **_base("REOPEN"),
            "target_kind": "CHECKPOINT",
            "checkpoint_id": "00000000-0000-0000-0000-000000000020",
        },
        {
            "subgoal_id": "00000000-0000-0000-0000-000000000030",
            "actor": {"kind": "USER", "actor_id": "00000000-0000-0000-0000-000000000001"},
            "expected_version": 0,
            "action": "REOPEN",
            "target_kind": "SUBGOAL",
        },
    ]
    for payload in payloads:
        adapter.validate_json(json.dumps(payload))

    native_payload = {
        "session_id": UUID("00000000-0000-0000-0000-000000000010"),
        "actor": _actor(),
        "expected_version": 0,
        "action": "CONTINUE",
    }
    adapter.validate_python(native_payload)


def test_accept_subgoal_command_validates_outside_alias() -> None:
    cmd = AcceptSubgoalCommand(
        subgoal_id=UUID("00000000-0000-0000-0000-000000000030"),
        actor=_actor(),
        expected_version=0,
    )
    assert cmd.expected_version == 0


def test_accept_subgoal_not_in_intervention_alias() -> None:
    adapter: TypeAdapter[InterventionCommand] = TypeAdapter(InterventionCommand)
    with pytest.raises(ValidationError) as exc:
        adapter.validate_json(
            json.dumps(
                {
                    "subgoal_id": "00000000-0000-0000-0000-000000000030",
                    "actor": {
                        "kind": "USER",
                        "actor_id": "00000000-0000-0000-0000-000000000001",
                    },
                    "expected_version": 0,
                    "action": "ACCEPT_SUBGOAL",
                }
            )
        )
    assert exc.value.errors()[0]["type"] == "union_tag_invalid"


def test_command_discriminator_missing_or_invalid() -> None:
    adapter: TypeAdapter[InterventionCommand] = TypeAdapter(InterventionCommand)
    with pytest.raises(ValidationError) as exc_missing:
        adapter.validate_json(
            json.dumps(
                {
                    "session_id": "00000000-0000-0000-0000-000000000010",
                    "actor": {
                        "kind": "USER",
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
                    "session_id": "00000000-0000-0000-0000-000000000010",
                    "actor": {
                        "kind": "USER",
                        "actor_id": "00000000-0000-0000-0000-000000000001",
                    },
                    "expected_version": 0,
                    "action": "UNKNOWN",
                }
            )
        )
    assert exc_invalid.value.errors()[0]["type"] == "union_tag_invalid"


def test_command_required_and_validation_failures() -> None:
    with pytest.raises(ValidationError) as exc_negative_version:
        ContinueDeliberationCommand(
            session_id=UUID(int=10), actor=_actor(), expected_version=-1, action="CONTINUE"
        )
    assert exc_negative_version.value.errors()[0]["type"] == "greater_than_equal"
    assert tuple(exc_negative_version.value.errors()[0]["loc"]) == ("expected_version",)

    adapter: TypeAdapter[InterventionCommand] = TypeAdapter(InterventionCommand)
    with pytest.raises(ValidationError) as exc_missing_expected_version:
        adapter.validate_json(
            json.dumps(
                {
                    "session_id": "00000000-0000-0000-0000-000000000010",
                    "actor": {
                        "kind": "USER",
                        "actor_id": "00000000-0000-0000-0000-000000000001",
                    },
                    "action": "CONTINUE",
                }
            )
        )
    assert exc_missing_expected_version.value.errors()[0]["type"] == "missing"
    assert tuple(exc_missing_expected_version.value.errors()[0]["loc"])[-1] == "expected_version"

    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("GUIDE"), "guidance": ""}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("CORRECT_CONTEXT"), "correction": ""}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("REVISE_SCOPE"), "revision": ""}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("REOPEN"), "target_kind": "INVALID"}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("REOPEN")}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("CONTINUE"), "action": 1}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("REOPEN"), "target_kind": 1}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("CONTINUE"), "command_id": "x"}))
    with pytest.raises(ValidationError):
        adapter.validate_json(json.dumps({**_base("CONTINUE"), "correlation_id": "x"}))


def test_command_json_schema_has_exact_union_shape() -> None:
    schema = TypeAdapter(InterventionCommand).json_schema()
    assert len(schema["oneOf"]) == 8


def test_command_literals_are_required_and_fixed() -> None:
    schema = TypeAdapter(InterventionCommand).json_schema()
    defs = schema.get("$defs", {})
    expected_actions = {
        "ContinueDeliberationCommand": "CONTINUE",
        "GuideDeliberationCommand": "GUIDE",
        "CorrectContextCommand": "CORRECT_CONTEXT",
        "ReviseScopeCommand": "REVISE_SCOPE",
        "PauseDeliberationCommand": "PAUSE",
        "StopDeliberationCommand": "STOP",
        "ReopenCheckpointCommand": "REOPEN",
        "ReopenSubgoalCommand": "REOPEN",
    }
    for model_name, literal in expected_actions.items():
        model_schema = defs[model_name]
        assert "action" in model_schema["required"]
        assert model_schema["properties"]["action"]["const"] == literal

    assert "target_kind" in defs["ReopenCheckpointCommand"]["required"]
    assert defs["ReopenCheckpointCommand"]["properties"]["target_kind"]["const"] == "CHECKPOINT"
    assert "target_kind" in defs["ReopenSubgoalCommand"]["required"]
    assert defs["ReopenSubgoalCommand"]["properties"]["target_kind"]["const"] == "SUBGOAL"


def test_all_command_models_are_frozen() -> None:
    models = [
        ContinueDeliberationCommand(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            actor=_actor(),
            expected_version=0,
            action="CONTINUE",
        ),
        GuideDeliberationCommand(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            actor=_actor(),
            expected_version=0,
            action="GUIDE",
            guidance="g",
        ),
        CorrectContextCommand(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            actor=_actor(),
            expected_version=0,
            action="CORRECT_CONTEXT",
            correction="c",
        ),
        ReviseScopeCommand(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            actor=_actor(),
            expected_version=0,
            action="REVISE_SCOPE",
            revision="r",
        ),
        PauseDeliberationCommand(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            actor=_actor(),
            expected_version=0,
            action="PAUSE",
        ),
        StopDeliberationCommand(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            actor=_actor(),
            expected_version=0,
            action="STOP",
        ),
        ReopenCheckpointCommand(
            session_id=UUID("00000000-0000-0000-0000-000000000010"),
            checkpoint_id=UUID("00000000-0000-0000-0000-000000000020"),
            actor=_actor(),
            expected_version=0,
            action="REOPEN",
            target_kind="CHECKPOINT",
        ),
        ReopenSubgoalCommand(
            subgoal_id=UUID("00000000-0000-0000-0000-000000000030"),
            actor=_actor(),
            expected_version=0,
            action="REOPEN",
            target_kind="SUBGOAL",
        ),
        AcceptSubgoalCommand(
            subgoal_id=UUID("00000000-0000-0000-0000-000000000030"),
            actor=_actor(),
            expected_version=0,
        ),
    ]

    for model in models:
        field_name = "expected_version"
        with pytest.raises(ValidationError):
            setattr(model, field_name, 1)
