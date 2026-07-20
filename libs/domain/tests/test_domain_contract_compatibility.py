from dataclasses import is_dataclass
from uuid import uuid4

from mnemograph_contracts.actors import ActorRef as ContractActorRef
from mnemograph_contracts.deliberation import DeliberationSessionRecord
from mnemograph_contracts.enums import ActorKind as ContractActorKind
from mnemograph_contracts.enums import DeliberationSessionState as ContractDeliberationSessionState
from mnemograph_contracts.enums import GoalState as ContractGoalState
from mnemograph_contracts.enums import InterventionKind as ContractInterventionKind
from mnemograph_contracts.enums import SubgoalAcceptanceStatus as ContractSubgoalAcceptanceStatus
from mnemograph_contracts.goals import GoalResponse
from mnemograph_domain import (
    ActorId,
    ActorKind,
    ActorRef,
    AggregateVersion,
    DeliberationSessionId,
    DeliberationSessionState,
    GoalId,
    GoalState,
    InterventionKind,
    SubgoalAcceptanceStatus,
    make_aggregate_version,
)


def _enum_pairs(enum_type: type[object]) -> set[tuple[str, str]]:
    return {(member.name, member.value) for member in enum_type}  # type: ignore[attr-defined]


def test_domain_and_contract_enum_surfaces_match_by_name_and_value() -> None:
    assert _enum_pairs(ActorKind) == _enum_pairs(ContractActorKind)
    assert _enum_pairs(GoalState) == _enum_pairs(ContractGoalState)
    assert _enum_pairs(SubgoalAcceptanceStatus) == _enum_pairs(ContractSubgoalAcceptanceStatus)
    assert _enum_pairs(DeliberationSessionState) == _enum_pairs(ContractDeliberationSessionState)
    assert _enum_pairs(InterventionKind) == _enum_pairs(ContractInterventionKind)


def test_actor_ref_field_semantics_are_contract_compatible() -> None:
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


def test_domain_uuid_identifier_values_can_supply_contract_uuid_boundaries() -> None:
    goal_id = GoalId(uuid4())
    session_id = DeliberationSessionId(uuid4())

    goal_response = GoalResponse.model_validate(
        {
            "goal_id": goal_id,
            "statement": "Goal statement",
            "state": ContractGoalState.DRAFT,
            "version": 0,
        },
        strict=True,
    )
    session_record = DeliberationSessionRecord.model_validate(
        {
            "session_id": session_id,
            "subgoal_id": uuid4(),
            "version": 0,
            "state": ContractDeliberationSessionState.SESSION_ACTIVE,
        },
        strict=True,
    )

    assert goal_response.goal_id == goal_id
    assert session_record.session_id == session_id


def test_non_negative_aggregate_versions_are_accepted_by_contract_version_fields() -> None:
    zero_version = make_aggregate_version(0)
    next_version = make_aggregate_version(9)

    first = GoalResponse.model_validate(
        {
            "goal_id": uuid4(),
            "statement": "Version zero",
            "state": ContractGoalState.DRAFT,
            "version": zero_version,
        },
        strict=True,
    )
    second = DeliberationSessionRecord.model_validate(
        {
            "session_id": uuid4(),
            "subgoal_id": uuid4(),
            "version": next_version,
            "state": ContractDeliberationSessionState.SESSION_ACTIVE,
        },
        strict=True,
    )

    assert first.version == AggregateVersion(0)
    assert second.version == AggregateVersion(9)


def test_domain_and_contract_actor_representations_are_independent_types() -> None:
    assert ActorRef.__module__.startswith("mnemograph_domain")
    assert ContractActorRef.__module__.startswith("mnemograph_contracts")
    assert is_dataclass(ActorRef)
    assert not is_dataclass(ContractActorRef)
