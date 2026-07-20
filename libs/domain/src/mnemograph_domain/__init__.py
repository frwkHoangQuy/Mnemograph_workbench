"""Pure-domain primitives and Goal scoping behavior for Delivery D1.4."""

from mnemograph_domain.actors import ActorRef
from mnemograph_domain.commands import (
    ApproveGoalPlanCommand,
    BeginScopingCommand,
    CreateGoalCommand,
    ProposeGoalDecompositionCommand,
    ReviseGoalPlanCommand,
)
from mnemograph_domain.datetimes import ensure_aware_utc
from mnemograph_domain.enums import (
    ActorKind,
    DeliberationSessionState,
    GoalState,
    InterventionKind,
    SubgoalAcceptanceStatus,
)
from mnemograph_domain.errors import (
    ActorNotPermittedError,
    GoalVersionConflictError,
    IllegalGoalTransitionError,
    InvalidStructuralInputError,
)
from mnemograph_domain.goal_mutations import (
    approve_goal_plan,
    begin_scoping,
    create_goal,
    propose_goal_decomposition,
    revise_goal_plan,
)
from mnemograph_domain.goal_plans import (
    ApprovedGoalPlan,
    GoalDecompositionProposal,
    PlanSubgoalEntry,
)
from mnemograph_domain.goals import Goal
from mnemograph_domain.identifiers import (
    ActorId,
    DeliberationSessionId,
    DeliberationTurnId,
    GoalId,
    GoalPlanId,
    InterventionId,
    SubgoalId,
    TransitionEventId,
    UserCheckpointId,
)
from mnemograph_domain.subgoals import Subgoal, create_subgoal
from mnemograph_domain.transitions import (
    GoalApprovalResult,
    GoalProposalResult,
    GoalTransitionRecord,
    GoalTransitionResult,
)
from mnemograph_domain.versioning import AggregateVersion, make_aggregate_version

__all__ = [
    "ActorId",
    "GoalId",
    "GoalPlanId",
    "SubgoalId",
    "DeliberationSessionId",
    "DeliberationTurnId",
    "UserCheckpointId",
    "InterventionId",
    "ActorKind",
    "GoalState",
    "SubgoalAcceptanceStatus",
    "DeliberationSessionState",
    "InterventionKind",
    "AggregateVersion",
    "make_aggregate_version",
    "ActorRef",
    "TransitionEventId",
    "GoalVersionConflictError",
    "IllegalGoalTransitionError",
    "ActorNotPermittedError",
    "InvalidStructuralInputError",
    "Subgoal",
    "PlanSubgoalEntry",
    "GoalDecompositionProposal",
    "ApprovedGoalPlan",
    "Goal",
    "CreateGoalCommand",
    "BeginScopingCommand",
    "ProposeGoalDecompositionCommand",
    "ReviseGoalPlanCommand",
    "ApproveGoalPlanCommand",
    "GoalTransitionRecord",
    "GoalTransitionResult",
    "GoalProposalResult",
    "GoalApprovalResult",
    "create_goal",
    "create_subgoal",
    "begin_scoping",
    "propose_goal_decomposition",
    "revise_goal_plan",
    "approve_goal_plan",
    "ensure_aware_utc",
]
