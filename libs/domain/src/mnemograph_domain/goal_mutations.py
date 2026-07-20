from mnemograph_domain.commands import (
    ApproveGoalPlanCommand,
    BeginScopingCommand,
    CreateGoalCommand,
    ProposeGoalDecompositionCommand,
    ReviseGoalPlanCommand,
)
from mnemograph_domain.enums import ActorKind, GoalState
from mnemograph_domain.errors import (
    ActorNotPermittedError,
    GoalVersionConflictError,
    IllegalGoalTransitionError,
    InvalidStructuralInputError,
)
from mnemograph_domain.goal_plans import ApprovedGoalPlan, GoalDecompositionProposal
from mnemograph_domain.goals import Goal
from mnemograph_domain.transitions import (
    GoalApprovalResult,
    GoalProposalResult,
    GoalTransitionRecord,
    GoalTransitionResult,
)
from mnemograph_domain.versioning import make_aggregate_version


def _require_actor(actual: ActorKind, required: ActorKind) -> None:
    if actual is not required:
        raise ActorNotPermittedError(f"{required.value} actor required")


def _require_goal_identity(goal: Goal, command_goal_id: object) -> None:
    if command_goal_id != goal.goal_id:
        raise InvalidStructuralInputError("command goal_id does not match Goal")


def _require_version(goal: Goal, expected_version: int) -> None:
    if expected_version != goal.version:
        raise GoalVersionConflictError("expected_version does not match Goal.version")


def _require_state(goal: Goal, required: GoalState) -> None:
    if goal.state is not required:
        raise IllegalGoalTransitionError(
            f"operation requires {required.value}, got {goal.state.value}"
        )


def _transition(
    goal: Goal,
    previous_state: GoalState | None,
    command: CreateGoalCommand
    | BeginScopingCommand
    | ProposeGoalDecompositionCommand
    | ReviseGoalPlanCommand
    | ApproveGoalPlanCommand,
) -> GoalTransitionRecord:
    return GoalTransitionRecord(
        event_id=command.event_id,
        goal_id=goal.goal_id,
        version=goal.version,
        previous_state=previous_state,
        next_state=goal.state,
        actor=command.actor,
        occurred_at=command.occurred_at,
    )


def create_goal(command: CreateGoalCommand) -> GoalTransitionResult:
    _require_actor(command.actor.kind, ActorKind.USER)
    goal = Goal(
        goal_id=command.goal_id,
        statement=command.statement,
        state=GoalState.DRAFT,
        version=make_aggregate_version(0),
        current_proposal_plan_id=None,
        current_proposal_plan_version=None,
        approved_goal_plan_id=None,
        approved_goal_plan_version=None,
    )
    return GoalTransitionResult(goal=goal, transition=_transition(goal, None, command))


def begin_scoping(goal: Goal, command: BeginScopingCommand) -> GoalTransitionResult:
    _require_actor(command.actor.kind, ActorKind.SYSTEM)
    _require_goal_identity(goal, command.goal_id)
    _require_version(goal, command.expected_version)
    _require_state(goal, GoalState.DRAFT)
    next_goal = Goal(
        goal_id=goal.goal_id,
        statement=goal.statement,
        state=GoalState.SCOPING,
        version=make_aggregate_version(goal.version + 1),
        current_proposal_plan_id=None,
        current_proposal_plan_version=None,
        approved_goal_plan_id=None,
        approved_goal_plan_version=None,
    )
    return GoalTransitionResult(
        goal=next_goal,
        transition=_transition(next_goal, goal.state, command),
    )


def propose_goal_decomposition(
    goal: Goal,
    command: ProposeGoalDecompositionCommand,
) -> GoalProposalResult:
    _require_actor(command.actor.kind, ActorKind.SYSTEM)
    _require_goal_identity(goal, command.goal_id)
    _require_version(goal, command.expected_version)
    _require_state(goal, GoalState.SCOPING)

    subgoal_ids = [subgoal.subgoal_id for subgoal in command.subgoals]
    entry_ids = [entry.subgoal_id for entry in command.entries]
    if len(subgoal_ids) != len(set(subgoal_ids)) or len(entry_ids) != len(set(entry_ids)):
        raise InvalidStructuralInputError("duplicate Subgoal in proposal input")
    if any(subgoal.goal_id != goal.goal_id for subgoal in command.subgoals):
        raise InvalidStructuralInputError("Subgoal goal_id does not match Goal")
    if set(subgoal_ids) != set(entry_ids):
        raise InvalidStructuralInputError("supplied Subgoals and plan entries must match exactly")

    plan_version = make_aggregate_version(0)
    proposal = GoalDecompositionProposal(
        plan_id=command.plan_id,
        goal_id=goal.goal_id,
        version=plan_version,
        entries=command.entries,
    )
    next_goal = Goal(
        goal_id=goal.goal_id,
        statement=goal.statement,
        state=GoalState.AWAITING_PLAN_APPROVAL,
        version=make_aggregate_version(goal.version + 1),
        current_proposal_plan_id=proposal.plan_id,
        current_proposal_plan_version=proposal.version,
        approved_goal_plan_id=None,
        approved_goal_plan_version=None,
    )
    return GoalProposalResult(
        goal=next_goal,
        transition=_transition(next_goal, goal.state, command),
        proposal=proposal,
    )


def revise_goal_plan(goal: Goal, command: ReviseGoalPlanCommand) -> GoalTransitionResult:
    _require_actor(command.actor.kind, ActorKind.USER)
    _require_goal_identity(goal, command.goal_id)
    _require_version(goal, command.expected_version)
    _require_state(goal, GoalState.AWAITING_PLAN_APPROVAL)
    next_goal = Goal(
        goal_id=goal.goal_id,
        statement=goal.statement,
        state=GoalState.SCOPING,
        version=make_aggregate_version(goal.version + 1),
        current_proposal_plan_id=None,
        current_proposal_plan_version=None,
        approved_goal_plan_id=None,
        approved_goal_plan_version=None,
    )
    return GoalTransitionResult(
        goal=next_goal,
        transition=_transition(next_goal, goal.state, command),
    )


def approve_goal_plan(
    goal: Goal,
    proposal: GoalDecompositionProposal,
    command: ApproveGoalPlanCommand,
) -> GoalApprovalResult:
    _require_actor(command.actor.kind, ActorKind.USER)
    _require_goal_identity(goal, command.goal_id)
    if proposal.goal_id != goal.goal_id:
        raise InvalidStructuralInputError("proposal goal_id does not match Goal")
    _require_version(goal, command.expected_version)
    _require_state(goal, GoalState.AWAITING_PLAN_APPROVAL)
    if (
        proposal.plan_id != goal.current_proposal_plan_id
        or proposal.version != goal.current_proposal_plan_version
    ):
        raise InvalidStructuralInputError("proposal is not the Goal's current proposal")

    approved_plan = ApprovedGoalPlan(
        plan_id=proposal.plan_id,
        goal_id=proposal.goal_id,
        version=proposal.version,
        entries=proposal.entries,
    )
    next_goal = Goal(
        goal_id=goal.goal_id,
        statement=goal.statement,
        state=GoalState.DELIBERATING,
        version=make_aggregate_version(goal.version + 1),
        current_proposal_plan_id=None,
        current_proposal_plan_version=None,
        approved_goal_plan_id=approved_plan.plan_id,
        approved_goal_plan_version=approved_plan.version,
    )
    return GoalApprovalResult(
        goal=next_goal,
        transition=_transition(next_goal, goal.state, command),
        approved_plan=approved_plan,
    )
