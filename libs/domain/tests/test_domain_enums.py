from enum import StrEnum

import mnemograph_domain
from mnemograph_domain import enums as domain_enums
from mnemograph_domain.enums import (
    ActorKind,
    DeliberationSessionState,
    GoalState,
    InterventionKind,
    SubgoalAcceptanceStatus,
)


def _enum_mapping(enum_type: type[StrEnum]) -> dict[str, str]:
    return {member.name: member.value for member in enum_type}


def test_domain_enum_inventory_contains_only_the_five_approved_surfaces() -> None:
    enum_names = {
        name
        for name, value in vars(domain_enums).items()
        if isinstance(value, type)
        and issubclass(value, StrEnum)
        and value.__module__ == domain_enums.__name__
    }

    assert enum_names == {
        "ActorKind",
        "GoalState",
        "SubgoalAcceptanceStatus",
        "DeliberationSessionState",
        "InterventionKind",
    }
    assert not hasattr(domain_enums, "EvidenceRelationship")
    assert not hasattr(mnemograph_domain, "EvidenceRelationship")


def test_actor_kind_exact_name_value_mapping() -> None:
    assert _enum_mapping(ActorKind) == {
        "USER": "USER",
        "SCIENTIST": "SCIENTIST",
        "SA": "SA",
        "SYSTEM": "SYSTEM",
    }
    assert "MODERATOR" not in _enum_mapping(ActorKind)


def test_goal_state_exact_name_value_mapping() -> None:
    values = _enum_mapping(GoalState)

    assert values == {
        "DRAFT": "DRAFT",
        "SCOPING": "SCOPING",
        "AWAITING_PLAN_APPROVAL": "AWAITING_PLAN_APPROVAL",
        "DELIBERATING": "DELIBERATING",
        "AWAITING_USER": "AWAITING_USER",
        "PAUSED": "PAUSED",
        "CROSS_GOAL_REVIEW": "CROSS_GOAL_REVIEW",
        "FINAL_CANDIDATE": "FINAL_CANDIDATE",
        "STOPPED": "STOPPED",
    }
    assert "ACCEPTED" not in values
    assert "PUBLISHING" not in values
    assert "COMPLETED" not in values


def test_subgoal_acceptance_status_exact_name_value_mapping() -> None:
    assert _enum_mapping(SubgoalAcceptanceStatus) == {
        "NOT_ACCEPTED": "NOT_ACCEPTED",
        "USER_ACCEPTED": "USER_ACCEPTED",
    }


def test_deliberation_session_state_exact_name_value_mapping() -> None:
    assert _enum_mapping(DeliberationSessionState) == {
        "SESSION_ACTIVE": "SESSION_ACTIVE",
        "SESSION_PAUSED": "SESSION_PAUSED",
        "SESSION_STOPPED": "SESSION_STOPPED",
    }


def test_intervention_kind_exact_name_value_mapping() -> None:
    values = _enum_mapping(InterventionKind)

    assert values == {
        "GUIDE": "GUIDE",
        "REVISE_SCOPE": "REVISE_SCOPE",
        "PAUSE": "PAUSE",
        "STOP": "STOP",
        "REOPEN": "REOPEN",
        "CONTINUE": "CONTINUE",
        "CORRECT_CONTEXT": "CORRECT_CONTEXT",
    }
    assert "CONTINUE" in values
    assert "CORRECT_CONTEXT" in values
