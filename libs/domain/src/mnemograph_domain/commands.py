from dataclasses import dataclass
from datetime import datetime

from mnemograph_domain.actors import ActorRef
from mnemograph_domain.goal_plans import PlanSubgoalEntry
from mnemograph_domain.identifiers import GoalId, GoalPlanId, TransitionEventId
from mnemograph_domain.subgoals import Subgoal
from mnemograph_domain.versioning import AggregateVersion


@dataclass(frozen=True)
class CreateGoalCommand:
    goal_id: GoalId
    statement: str
    actor: ActorRef
    event_id: TransitionEventId
    occurred_at: datetime


@dataclass(frozen=True)
class BeginScopingCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    event_id: TransitionEventId
    occurred_at: datetime


@dataclass(frozen=True)
class ProposeGoalDecompositionCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    plan_id: GoalPlanId
    subgoals: tuple[Subgoal, ...]
    entries: tuple[PlanSubgoalEntry, ...]
    event_id: TransitionEventId
    occurred_at: datetime


@dataclass(frozen=True)
class ReviseGoalPlanCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    event_id: TransitionEventId
    occurred_at: datetime


@dataclass(frozen=True)
class ApproveGoalPlanCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    event_id: TransitionEventId
    occurred_at: datetime
