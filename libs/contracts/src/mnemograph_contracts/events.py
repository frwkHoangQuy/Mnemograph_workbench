from uuid import UUID

from pydantic import Field

from mnemograph_contracts._base import ContractModel, UtcDateTime
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.enums import DeliberationSessionState, GoalState, SubgoalAcceptanceStatus


class GoalTransitionRecord(ContractModel):
    event_id: UUID
    goal_id: UUID
    version: int = Field(ge=0)
    previous_state: GoalState | None
    next_state: GoalState
    actor: ActorRef
    occurred_at: UtcDateTime


class SubgoalTransitionRecord(ContractModel):
    event_id: UUID
    subgoal_id: UUID
    version: int = Field(ge=0)
    previous_status: SubgoalAcceptanceStatus | None
    next_status: SubgoalAcceptanceStatus
    actor: ActorRef
    occurred_at: UtcDateTime


class DeliberationSessionTransitionRecord(ContractModel):
    event_id: UUID
    session_id: UUID
    version: int = Field(ge=0)
    previous_status: DeliberationSessionState | None
    next_status: DeliberationSessionState
    actor: ActorRef
    occurred_at: UtcDateTime
