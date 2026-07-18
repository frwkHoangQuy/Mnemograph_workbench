from uuid import UUID

from pydantic import Field

from mnemograph_contracts._base import ContractModel
from mnemograph_contracts.enums import GoalState


class GoalCreateRequest(ContractModel):
    statement: str = Field(min_length=1)


class GoalResponse(ContractModel):
    goal_id: UUID
    statement: str = Field(min_length=1)
    state: GoalState
    version: int = Field(ge=0)
    approved_goal_plan_id: UUID | None = None
