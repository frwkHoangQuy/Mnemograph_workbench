from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.enums import ActorKind
from pydantic import ValidationError


@pytest.mark.parametrize(
    "kind", [ActorKind.USER, ActorKind.SCIENTIST, ActorKind.SA, ActorKind.SYSTEM]
)
def test_actor_ref_valid(kind: ActorKind) -> None:
    actor = ActorRef(kind=kind, actor_id=UUID("00000000-0000-0000-0000-000000000001"))
    assert actor.kind is kind


def test_actor_ref_valid_json_uuid() -> None:
    actor = ActorRef.model_validate_json(
        '{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001"}'
    )
    assert actor.actor_id == UUID("00000000-0000-0000-0000-000000000001")


def test_actor_ref_invalid_uuid() -> None:
    with pytest.raises(ValidationError):
        ActorRef.model_validate_json('{"kind":"USER","actor_id":"not-a-uuid"}')


def test_actor_ref_strict_uuid_in_python_mode() -> None:
    with pytest.raises(ValidationError):
        ActorRef.model_validate(
            {
                "kind": ActorKind.USER,
                "actor_id": "00000000-0000-0000-0000-000000000001",
            }
        )


def test_actor_ref_unknown_field_forbidden() -> None:
    with pytest.raises(ValidationError):
        ActorRef.model_validate_json(
            '{"kind":"USER","actor_id":"00000000-0000-0000-0000-000000000001","x":1}'
        )


def test_actor_ref_frozen_assignment() -> None:
    actor = ActorRef(kind=ActorKind.USER, actor_id=UUID("00000000-0000-0000-0000-000000000001"))
    with pytest.raises(ValidationError):
        actor.kind = ActorKind.SYSTEM
