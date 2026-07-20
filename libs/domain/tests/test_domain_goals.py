from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest
from mnemograph_domain import (
    AggregateVersion,
    Goal,
    GoalId,
    GoalPlanId,
    GoalState,
    InvalidStructuralInputError,
)


def _goal(state: GoalState) -> Goal:
    plan_id = GoalPlanId(uuid4())
    proposal = state is GoalState.AWAITING_PLAN_APPROVAL
    approved = state is GoalState.DELIBERATING
    return Goal(
        goal_id=GoalId(uuid4()),
        statement="Research question",
        state=state,
        version=AggregateVersion(0),
        current_proposal_plan_id=plan_id if proposal else None,
        current_proposal_plan_version=AggregateVersion(0) if proposal else None,
        approved_goal_plan_id=plan_id if approved else None,
        approved_goal_plan_version=AggregateVersion(0) if approved else None,
    )


@pytest.mark.parametrize(
    "state",
    [GoalState.DRAFT, GoalState.SCOPING, GoalState.AWAITING_PLAN_APPROVAL, GoalState.DELIBERATING],
)
def test_goal_accepts_exact_in_scope_state_linkage_rows(state: GoalState) -> None:
    goal = _goal(state)
    with pytest.raises(FrozenInstanceError):
        goal.state = GoalState.STOPPED  # type: ignore[misc]


@pytest.mark.parametrize(
    "state",
    [
        GoalState.AWAITING_USER,
        GoalState.PAUSED,
        GoalState.CROSS_GOAL_REVIEW,
        GoalState.FINAL_CANDIDATE,
        GoalState.STOPPED,
    ],
)
def test_goal_rejects_out_of_scope_states(state: GoalState) -> None:
    with pytest.raises(InvalidStructuralInputError):
        _goal(state)


def test_goal_rejects_partial_or_wrong_state_linkage() -> None:
    with pytest.raises(InvalidStructuralInputError):
        Goal(
            goal_id=GoalId(uuid4()),
            statement="Question",
            state=GoalState.AWAITING_PLAN_APPROVAL,
            version=AggregateVersion(0),
            current_proposal_plan_id=None,
            current_proposal_plan_version=None,
            approved_goal_plan_id=None,
            approved_goal_plan_version=None,
        )


@pytest.mark.parametrize(("statement", "version"), [(" ", 0), ("Question", -1)])
def test_goal_rejects_invalid_statement_or_version(statement: str, version: int) -> None:
    with pytest.raises(InvalidStructuralInputError):
        Goal(
            goal_id=GoalId(uuid4()),
            statement=statement,
            state=GoalState.DRAFT,
            version=AggregateVersion(version),
            current_proposal_plan_id=None,
            current_proposal_plan_version=None,
            approved_goal_plan_id=None,
            approved_goal_plan_version=None,
        )
