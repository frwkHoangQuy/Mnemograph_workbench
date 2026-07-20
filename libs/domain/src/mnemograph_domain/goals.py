from dataclasses import dataclass

from mnemograph_domain.enums import GoalState
from mnemograph_domain.errors import InvalidStructuralInputError
from mnemograph_domain.identifiers import GoalId, GoalPlanId
from mnemograph_domain.versioning import AggregateVersion


@dataclass(frozen=True)
class Goal:
    goal_id: GoalId
    statement: str
    state: GoalState
    version: AggregateVersion
    current_proposal_plan_id: GoalPlanId | None
    current_proposal_plan_version: AggregateVersion | None
    approved_goal_plan_id: GoalPlanId | None
    approved_goal_plan_version: AggregateVersion | None

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise InvalidStructuralInputError("Goal.statement must contain non-whitespace")
        if self.version < 0:
            raise InvalidStructuralInputError("Goal.version must be non-negative")

        proposal_set = (
            self.current_proposal_plan_id is not None
            and self.current_proposal_plan_version is not None
        )
        proposal_empty = (
            self.current_proposal_plan_id is None and self.current_proposal_plan_version is None
        )
        approved_set = (
            self.approved_goal_plan_id is not None and self.approved_goal_plan_version is not None
        )
        approved_empty = (
            self.approved_goal_plan_id is None and self.approved_goal_plan_version is None
        )

        valid = (
            (
                self.state in {GoalState.DRAFT, GoalState.SCOPING}
                and proposal_empty
                and approved_empty
            )
            or (self.state is GoalState.AWAITING_PLAN_APPROVAL and proposal_set and approved_empty)
            or (self.state is GoalState.DELIBERATING and proposal_empty and approved_set)
        )
        if not valid:
            raise InvalidStructuralInputError("Goal state and plan linkage are inconsistent")
