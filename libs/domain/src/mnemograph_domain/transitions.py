from dataclasses import dataclass
from datetime import datetime

from mnemograph_domain.actors import ActorRef
from mnemograph_domain.datetimes import ensure_aware_utc
from mnemograph_domain.enums import GoalState
from mnemograph_domain.errors import InvalidStructuralInputError
from mnemograph_domain.goal_plans import ApprovedGoalPlan, GoalDecompositionProposal
from mnemograph_domain.goals import Goal
from mnemograph_domain.identifiers import GoalId, TransitionEventId
from mnemograph_domain.versioning import AggregateVersion


@dataclass(frozen=True)
class GoalTransitionRecord:
    event_id: TransitionEventId
    goal_id: GoalId
    version: AggregateVersion
    previous_state: GoalState | None
    next_state: GoalState
    actor: ActorRef
    occurred_at: datetime

    def __post_init__(self) -> None:
        if self.version < 0:
            raise InvalidStructuralInputError("GoalTransitionRecord.version must be non-negative")
        object.__setattr__(self, "occurred_at", ensure_aware_utc(self.occurred_at))


def _validate_transition(goal: Goal, transition: GoalTransitionRecord) -> None:
    if transition.goal_id != goal.goal_id:
        raise InvalidStructuralInputError("transition goal_id does not match Goal")
    if transition.version != goal.version:
        raise InvalidStructuralInputError("transition version does not match Goal")
    if transition.next_state is not goal.state:
        raise InvalidStructuralInputError("transition next_state does not match Goal")


@dataclass(frozen=True)
class GoalTransitionResult:
    goal: Goal
    transition: GoalTransitionRecord

    def __post_init__(self) -> None:
        _validate_transition(self.goal, self.transition)
        if self.goal.state in {GoalState.AWAITING_PLAN_APPROVAL, GoalState.DELIBERATING}:
            raise InvalidStructuralInputError("Goal state requires a plan payload")


@dataclass(frozen=True)
class GoalProposalResult:
    goal: Goal
    transition: GoalTransitionRecord
    proposal: GoalDecompositionProposal

    def __post_init__(self) -> None:
        _validate_transition(self.goal, self.transition)
        valid = (
            self.goal.state is GoalState.AWAITING_PLAN_APPROVAL
            and self.proposal.goal_id == self.goal.goal_id
            and self.proposal.plan_id == self.goal.current_proposal_plan_id
            and self.proposal.version == self.goal.current_proposal_plan_version
        )
        if not valid:
            raise InvalidStructuralInputError("proposal does not match resulting Goal")


@dataclass(frozen=True)
class GoalApprovalResult:
    goal: Goal
    transition: GoalTransitionRecord
    approved_plan: ApprovedGoalPlan

    def __post_init__(self) -> None:
        _validate_transition(self.goal, self.transition)
        valid = (
            self.goal.state is GoalState.DELIBERATING
            and self.approved_plan.goal_id == self.goal.goal_id
            and self.approved_plan.plan_id == self.goal.approved_goal_plan_id
            and self.approved_plan.version == self.goal.approved_goal_plan_version
        )
        if not valid:
            raise InvalidStructuralInputError("approved plan does not match resulting Goal")
