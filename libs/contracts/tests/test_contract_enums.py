from mnemograph_contracts.enums import (
    ActorKind,
    DeliberationSessionState,
    EvidenceRelationship,
    GoalState,
    InterventionKind,
    SubgoalAcceptanceStatus,
    ValidationErrorCode,
)


def _values(enum_cls: type) -> list[str]:
    return [member.value for member in enum_cls]  # type: ignore[attr-defined]


def test_actor_kind_values_exact() -> None:
    assert _values(ActorKind) == ["USER", "SCIENTIST", "SA", "SYSTEM"]
    assert "MODERATOR" not in _values(ActorKind)


def test_goal_state_values_exact() -> None:
    assert _values(GoalState) == [
        "DRAFT",
        "SCOPING",
        "AWAITING_PLAN_APPROVAL",
        "DELIBERATING",
        "AWAITING_USER",
        "PAUSED",
        "CROSS_GOAL_REVIEW",
        "FINAL_CANDIDATE",
        "STOPPED",
    ]
    assert "ACCEPTED" not in _values(GoalState)
    assert "PUBLISHING" not in _values(GoalState)
    assert "COMPLETED" not in _values(GoalState)


def test_intervention_kind_values_exact() -> None:
    assert _values(InterventionKind) == [
        "GUIDE",
        "REVISE_SCOPE",
        "PAUSE",
        "STOP",
        "REOPEN",
        "CONTINUE",
        "CORRECT_CONTEXT",
    ]
    assert "ACCEPT_SUBGOAL" not in _values(InterventionKind)


def test_subgoal_acceptance_status_values_exact() -> None:
    assert _values(SubgoalAcceptanceStatus) == ["NOT_ACCEPTED", "USER_ACCEPTED"]


def test_deliberation_session_state_values_exact() -> None:
    assert _values(DeliberationSessionState) == [
        "SESSION_ACTIVE",
        "SESSION_PAUSED",
        "SESSION_STOPPED",
    ]


def test_evidence_relationship_values_exact() -> None:
    assert _values(EvidenceRelationship) == ["SUPPORTS", "CONTRADICTS"]


def test_validation_error_code_values_exact() -> None:
    assert _values(ValidationErrorCode) == [
        "REQUIRED",
        "INVALID_TYPE",
        "INVALID_UUID",
        "INVALID_ENUM",
        "OUT_OF_RANGE",
        "UNKNOWN_FIELD",
        "NAIVE_DATETIME",
        "INVALID_VALUE",
    ]
