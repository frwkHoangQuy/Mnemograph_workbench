from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest
from mnemograph_domain import ActorId, ActorKind, ActorRef


def test_actor_ref_holds_kind_and_identifier() -> None:
    actor_id = ActorId(uuid4())

    actor = ActorRef(kind=ActorKind.USER, actor_id=actor_id)

    assert actor.kind is ActorKind.USER
    assert actor.actor_id == actor_id


def test_actor_ref_is_frozen() -> None:
    actor = ActorRef(kind=ActorKind.SYSTEM, actor_id=ActorId(uuid4()))

    with pytest.raises(FrozenInstanceError):
        actor.kind = ActorKind.SA  # type: ignore[misc]
