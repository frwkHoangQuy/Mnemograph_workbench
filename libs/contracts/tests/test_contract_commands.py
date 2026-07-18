from typing import Any
from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.commands import (
    AcceptSubgoalCommand,
    ContinueDeliberationCommand,
    InterventionCommand,
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
        adapter.validate_json(__import__("json").dumps(payload))

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
    with pytest.raises(ValidationError):
        adapter.validate_python(
            {
                "subgoal_id": "00000000-0000-0000-0000-000000000030",
                "actor": {"kind": "USER", "actor_id": "00000000-0000-0000-0000-000000000001"},
                "expected_version": 0,
                "action": "ACCEPT_SUBGOAL",
            }
        )


def test_command_required_and_validation_failures() -> None:
    with pytest.raises(ValidationError):
        ContinueDeliberationCommand(
            session_id=UUID(int=10), actor=_actor(), expected_version=-1, action="CONTINUE"
        )

    adapter: TypeAdapter[InterventionCommand] = TypeAdapter(InterventionCommand)
    with pytest.raises(ValidationError):
        adapter.validate_python(
            {
                "session_id": "00000000-0000-0000-0000-000000000010",
                "actor": {"kind": "USER", "actor_id": "00000000-0000-0000-0000-000000000001"},
                "action": "CONTINUE",
            }
        )
    with pytest.raises(ValidationError):
        adapter.validate_python({**_base("GUIDE"), "guidance": ""})
    with pytest.raises(ValidationError):
        adapter.validate_python({**_base("REOPEN"), "target_kind": "INVALID"})
    with pytest.raises(ValidationError):
        adapter.validate_python({**_base("REOPEN")})
    with pytest.raises(ValidationError):
        adapter.validate_python({**_base("CONTINUE"), "action": 1})
    with pytest.raises(ValidationError):
        adapter.validate_python({**_base("REOPEN"), "target_kind": 1})
    with pytest.raises(ValidationError):
        adapter.validate_python({**_base("CONTINUE"), "command_id": "x"})
    with pytest.raises(ValidationError):
        adapter.validate_python({**_base("CONTINUE"), "correlation_id": "x"})


def test_command_json_schema_has_exact_union_shape() -> None:
    schema = TypeAdapter(InterventionCommand).json_schema()
    assert len(schema["oneOf"]) == 8
