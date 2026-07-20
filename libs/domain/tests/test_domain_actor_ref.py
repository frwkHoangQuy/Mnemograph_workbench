from dataclasses import FrozenInstanceError, fields, is_dataclass
from uuid import uuid4

import pytest
from mnemograph_domain import ActorId, ActorKind, ActorRef


def test_actor_ref_has_exact_field_surface_and_annotations() -> None:
    field_names = [field.name for field in fields(ActorRef)]

    assert field_names == ["kind", "actor_id"]
    assert ActorRef.__annotations__ == {
        "kind": ActorKind,
        "actor_id": ActorId,
    }


def test_actor_ref_construction_works_for_every_approved_actor_kind() -> None:
    actor_id = ActorId(uuid4())

    for kind in ActorKind:
        actor = ActorRef(kind=kind, actor_id=actor_id)
        assert actor.kind is kind
        assert actor.actor_id == actor_id


def test_actor_ref_is_frozen() -> None:
    actor = ActorRef(kind=ActorKind.SYSTEM, actor_id=ActorId(uuid4()))

    with pytest.raises(FrozenInstanceError):
        actor.kind = ActorKind.SA  # type: ignore[misc]


def test_actor_ref_uses_standard_dataclass_value_equality() -> None:
    actor_id = ActorId(uuid4())

    first = ActorRef(kind=ActorKind.USER, actor_id=actor_id)
    second = ActorRef(kind=ActorKind.USER, actor_id=actor_id)
    different = ActorRef(kind=ActorKind.SYSTEM, actor_id=actor_id)

    assert first == second
    assert first != different


def test_actor_ref_does_not_define_slots() -> None:
    assert is_dataclass(ActorRef)
    assert not hasattr(ActorRef, "__slots__")
