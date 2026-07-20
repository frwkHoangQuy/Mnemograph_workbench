from uuid import uuid4

from mnemograph_contracts.actors import ActorRef as ContractActorRef
from mnemograph_contracts.enums import ActorKind as ContractActorKind
from mnemograph_domain import ActorId, ActorKind, ActorRef


def test_actor_ref_maps_to_contract_actor_ref() -> None:
    actor_id = uuid4()
    domain_actor = ActorRef(kind=ActorKind.SCIENTIST, actor_id=ActorId(actor_id))

    contract_actor = ContractActorRef.model_validate(
        {
            "kind": ContractActorKind(domain_actor.kind.value),
            "actor_id": actor_id,
        },
        strict=True,
    )

    assert contract_actor.kind is ContractActorKind.SCIENTIST
    assert contract_actor.actor_id == actor_id


def test_actor_kind_serialization_matches_contract_values() -> None:
    for domain_kind in ActorKind:
        contract_kind = ContractActorKind(domain_kind.value)
        assert contract_kind.value == domain_kind.value
