from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest
from mnemograph_domain import (
    AggregateVersion,
    ApprovedGoalPlan,
    GoalDecompositionProposal,
    GoalId,
    GoalPlanId,
    InvalidStructuralInputError,
    PlanSubgoalEntry,
    SubgoalId,
)


def _entry(subgoal_id: SubgoalId, *dependencies: SubgoalId) -> PlanSubgoalEntry:
    return PlanSubgoalEntry(subgoal_id=subgoal_id, depends_on=dependencies)


def _proposal(*entries: PlanSubgoalEntry) -> GoalDecompositionProposal:
    return GoalDecompositionProposal(
        plan_id=GoalPlanId(uuid4()),
        goal_id=GoalId(uuid4()),
        version=AggregateVersion(0),
        entries=entries,
    )


def test_zero_entry_proposal_and_approved_plan_are_valid_and_immutable() -> None:
    proposal = _proposal()
    approved = ApprovedGoalPlan(
        plan_id=proposal.plan_id,
        goal_id=proposal.goal_id,
        version=proposal.version,
        entries=proposal.entries,
    )

    assert proposal.entries == approved.entries == ()
    with pytest.raises(FrozenInstanceError):
        proposal.entries = ()  # type: ignore[misc]


def test_display_order_is_independent_of_dependency_order() -> None:
    first = SubgoalId(uuid4())
    second = SubgoalId(uuid4())
    proposal = _proposal(_entry(second, first), _entry(first))
    assert tuple(entry.subgoal_id for entry in proposal.entries) == (second, first)


def test_duplicate_subgoal_entries_are_rejected() -> None:
    subgoal_id = SubgoalId(uuid4())
    with pytest.raises(InvalidStructuralInputError, match="duplicate subgoal_id"):
        _proposal(_entry(subgoal_id), _entry(subgoal_id))


def test_duplicate_dependency_edge_is_rejected_before_normalization() -> None:
    subgoal_id = SubgoalId(uuid4())
    dependency = SubgoalId(uuid4())
    with pytest.raises(InvalidStructuralInputError, match="duplicate dependency"):
        _entry(subgoal_id, dependency, dependency)


def test_self_edge_is_rejected() -> None:
    subgoal_id = SubgoalId(uuid4())
    with pytest.raises(InvalidStructuralInputError, match="itself"):
        _entry(subgoal_id, subgoal_id)


def test_dangling_dependency_is_rejected() -> None:
    with pytest.raises(InvalidStructuralInputError, match="dangling"):
        _proposal(_entry(SubgoalId(uuid4()), SubgoalId(uuid4())))


def test_cycle_is_rejected_independently_of_tuple_position() -> None:
    first, second, third = (SubgoalId(uuid4()) for _ in range(3))
    with pytest.raises(InvalidStructuralInputError, match="cycle"):
        _proposal(_entry(first, third), _entry(second, first), _entry(third, second))


@pytest.mark.parametrize("plan_type", [GoalDecompositionProposal, ApprovedGoalPlan])
def test_plan_types_reject_negative_versions(plan_type: type[object]) -> None:
    with pytest.raises(InvalidStructuralInputError, match="non-negative"):
        plan_type(  # type: ignore[call-arg]
            plan_id=GoalPlanId(uuid4()),
            goal_id=GoalId(uuid4()),
            version=AggregateVersion(-1),
            entries=(),
        )
