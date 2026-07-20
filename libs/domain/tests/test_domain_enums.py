from mnemograph_contracts.enums import (
    ActorKind as ContractActorKind,
)
from mnemograph_contracts.enums import (
    DeliberationSessionState as ContractDeliberationSessionState,
)
from mnemograph_contracts.enums import (
    GoalState as ContractGoalState,
)
from mnemograph_contracts.enums import (
    InterventionKind as ContractInterventionKind,
)
from mnemograph_contracts.enums import (
    SubgoalAcceptanceStatus as ContractSubgoalAcceptanceStatus,
)
from mnemograph_domain import (
    ActorKind,
    DeliberationSessionState,
    GoalState,
    InterventionKind,
    SubgoalAcceptanceStatus,
)


def _enum_values(enum_type: type[object]) -> list[str]:
    return [member.value for member in enum_type]  # type: ignore[attr-defined]


def test_actor_kind_values_are_contract_compatible() -> None:
    assert _enum_values(ActorKind) == _enum_values(ContractActorKind)
    assert "MODERATOR" not in _enum_values(ActorKind)


def test_goal_state_values_are_contract_compatible() -> None:
    assert _enum_values(GoalState) == _enum_values(ContractGoalState)


def test_subgoal_acceptance_values_are_contract_compatible() -> None:
    assert _enum_values(SubgoalAcceptanceStatus) == _enum_values(ContractSubgoalAcceptanceStatus)


def test_deliberation_session_state_values_are_contract_compatible() -> None:
    assert _enum_values(DeliberationSessionState) == _enum_values(ContractDeliberationSessionState)


def test_intervention_kind_values_are_contract_compatible() -> None:
    assert _enum_values(InterventionKind) == _enum_values(ContractInterventionKind)
