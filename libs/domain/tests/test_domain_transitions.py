from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta, timezone
from uuid import uuid4

import pytest
from mnemograph_domain import (
    ActorId,
    ActorKind,
    ActorRef,
    AggregateVersion,
    ApprovedGoalPlan,
    Goal,
    GoalApprovalResult,
    GoalDecompositionProposal,
    GoalId,
    GoalPlanId,
    GoalProposalResult,
    GoalState,
    GoalTransitionRecord,
    GoalTransitionResult,
    InvalidStructuralInputError,
    TransitionEventId,
)


def _actor() -> ActorRef:
    return ActorRef(ActorKind.USER, ActorId(uuid4()))


def _goal(state: GoalState = GoalState.DRAFT) -> Goal:
    plan_id = GoalPlanId(uuid4())
    return Goal(
        goal_id=GoalId(uuid4()),
        statement="Question",
        state=state,
        version=AggregateVersion(2),
        current_proposal_plan_id=plan_id if state is GoalState.AWAITING_PLAN_APPROVAL else None,
        current_proposal_plan_version=(
            AggregateVersion(0) if state is GoalState.AWAITING_PLAN_APPROVAL else None
        ),
        approved_goal_plan_id=plan_id if state is GoalState.DELIBERATING else None,
        approved_goal_plan_version=(
            AggregateVersion(0) if state is GoalState.DELIBERATING else None
        ),
    )


def _transition(goal: Goal, occurred_at: datetime | None = None) -> GoalTransitionRecord:
    return GoalTransitionRecord(
        event_id=TransitionEventId(uuid4()),
        goal_id=goal.goal_id,
        version=goal.version,
        previous_state=None,
        next_state=goal.state,
        actor=_actor(),
        occurred_at=occurred_at or datetime(2026, 7, 20, tzinfo=UTC),
    )


def test_transition_record_normalizes_datetime_and_is_immutable() -> None:
    local_time = datetime(2026, 7, 20, 15, tzinfo=timezone(timedelta(hours=7)))
    transition = _transition(_goal(), local_time)
    assert transition.occurred_at == datetime(2026, 7, 20, 8, tzinfo=UTC)
    with pytest.raises(FrozenInstanceError):
        transition.version = AggregateVersion(4)  # type: ignore[misc]


def test_transition_record_rejects_naive_datetime_and_negative_version() -> None:
    goal = _goal()
    with pytest.raises(ValueError, match="timezone-aware"):
        _transition(goal, datetime(2026, 7, 20))
    with pytest.raises(InvalidStructuralInputError, match="non-negative"):
        replace(_transition(goal), version=AggregateVersion(-1))


@pytest.mark.parametrize("field", ["goal_id", "version", "next_state"])
def test_all_result_types_reject_transition_mismatch(field: str) -> None:
    transition_goal = _goal()
    proposal_goal = _goal(GoalState.AWAITING_PLAN_APPROVAL)
    proposal = GoalDecompositionProposal(
        plan_id=proposal_goal.current_proposal_plan_id,  # type: ignore[arg-type]
        goal_id=proposal_goal.goal_id,
        version=proposal_goal.current_proposal_plan_version,  # type: ignore[arg-type]
        entries=(),
    )
    approval_goal = _goal(GoalState.DELIBERATING)
    approved_plan = ApprovedGoalPlan(
        plan_id=approval_goal.approved_goal_plan_id,  # type: ignore[arg-type]
        goal_id=approval_goal.goal_id,
        version=approval_goal.approved_goal_plan_version,  # type: ignore[arg-type]
        entries=(),
    )

    transitions: tuple[GoalTransitionRecord, ...] = (
        _transition(transition_goal),
        _transition(proposal_goal),
        _transition(approval_goal),
    )
    if field == "goal_id":
        transitions = tuple(
            replace(transition, goal_id=GoalId(uuid4())) for transition in transitions
        )
    elif field == "version":
        transitions = tuple(
            replace(transition, version=AggregateVersion(99)) for transition in transitions
        )
    else:
        transitions = tuple(
            replace(
                transition,
                next_state=(
                    GoalState.DRAFT
                    if transition.next_state is not GoalState.DRAFT
                    else GoalState.SCOPING
                ),
            )
            for transition in transitions
        )
    with pytest.raises(InvalidStructuralInputError):
        GoalTransitionResult(transition_goal, transitions[0])
    with pytest.raises(InvalidStructuralInputError):
        GoalProposalResult(proposal_goal, transitions[1], proposal)
    with pytest.raises(InvalidStructuralInputError):
        GoalApprovalResult(approval_goal, transitions[2], approved_plan)


@pytest.mark.parametrize("state", [GoalState.AWAITING_PLAN_APPROVAL, GoalState.DELIBERATING])
def test_transition_only_result_rejects_states_requiring_payload(state: GoalState) -> None:
    goal = _goal(state)
    with pytest.raises(InvalidStructuralInputError, match="payload"):
        GoalTransitionResult(goal, _transition(goal))


def test_valid_proposal_and_approval_results_construct_and_are_immutable() -> None:
    proposal_goal = _goal(GoalState.AWAITING_PLAN_APPROVAL)
    proposal = GoalDecompositionProposal(
        plan_id=proposal_goal.current_proposal_plan_id,  # type: ignore[arg-type]
        goal_id=proposal_goal.goal_id,
        version=proposal_goal.current_proposal_plan_version,  # type: ignore[arg-type]
        entries=(),
    )
    proposal_result = GoalProposalResult(proposal_goal, _transition(proposal_goal), proposal)

    approved_goal = _goal(GoalState.DELIBERATING)
    approved = ApprovedGoalPlan(
        plan_id=approved_goal.approved_goal_plan_id,  # type: ignore[arg-type]
        goal_id=approved_goal.goal_id,
        version=approved_goal.approved_goal_plan_version,  # type: ignore[arg-type]
        entries=(),
    )
    approval_result = GoalApprovalResult(approved_goal, _transition(approved_goal), approved)

    with pytest.raises(FrozenInstanceError):
        proposal_result.proposal = proposal  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        approval_result.approved_plan = approved  # type: ignore[misc]


@pytest.mark.parametrize("mismatch", ["state", "goal_id", "plan_id", "version"])
def test_proposal_result_rejects_every_direct_construction_mismatch(mismatch: str) -> None:
    goal = _goal(GoalState.AWAITING_PLAN_APPROVAL)
    proposal = GoalDecompositionProposal(
        plan_id=goal.current_proposal_plan_id,  # type: ignore[arg-type]
        goal_id=goal.goal_id,
        version=goal.current_proposal_plan_version,  # type: ignore[arg-type]
        entries=(),
    )
    if mismatch == "state":
        wrong_goal = _goal(GoalState.SCOPING)
        proposal = replace(proposal, goal_id=wrong_goal.goal_id)
        with pytest.raises(InvalidStructuralInputError):
            GoalProposalResult(wrong_goal, _transition(wrong_goal), proposal)
        return
    if mismatch == "goal_id":
        proposal = replace(proposal, goal_id=GoalId(uuid4()))
    elif mismatch == "plan_id":
        proposal = replace(proposal, plan_id=GoalPlanId(uuid4()))
    else:
        proposal = replace(proposal, version=AggregateVersion(9))
    with pytest.raises(InvalidStructuralInputError):
        GoalProposalResult(goal, _transition(goal), proposal)


@pytest.mark.parametrize("mismatch", ["state", "goal_id", "plan_id", "version"])
def test_approval_result_rejects_every_direct_construction_mismatch(mismatch: str) -> None:
    goal = _goal(GoalState.DELIBERATING)
    approved = ApprovedGoalPlan(
        plan_id=goal.approved_goal_plan_id,  # type: ignore[arg-type]
        goal_id=goal.goal_id,
        version=goal.approved_goal_plan_version,  # type: ignore[arg-type]
        entries=(),
    )
    if mismatch == "state":
        wrong_goal = _goal(GoalState.SCOPING)
        approved = replace(approved, goal_id=wrong_goal.goal_id)
        with pytest.raises(InvalidStructuralInputError):
            GoalApprovalResult(wrong_goal, _transition(wrong_goal), approved)
        return
    if mismatch == "goal_id":
        approved = replace(approved, goal_id=GoalId(uuid4()))
    elif mismatch == "plan_id":
        approved = replace(approved, plan_id=GoalPlanId(uuid4()))
    else:
        approved = replace(approved, version=AggregateVersion(9))
    with pytest.raises(InvalidStructuralInputError):
        GoalApprovalResult(goal, _transition(goal), approved)


def test_transition_result_shape_has_no_plan_payload_fields() -> None:
    with pytest.raises(TypeError):
        GoalTransitionResult(_goal(), _transition(_goal()), proposal=None)  # type: ignore[call-arg]
