from uuid import UUID

from pydantic import Field

from mnemograph_contracts._base import ContractModel
from mnemograph_contracts.enums import SubgoalAcceptanceStatus


class SubgoalCreateRequest(ContractModel):
    goal_id: UUID
    statement: str = Field(min_length=1)
    definition_of_done: str = Field(min_length=1)


class SubgoalResponse(ContractModel):
    subgoal_id: UUID
    goal_id: UUID
    statement: str = Field(min_length=1)
    definition_of_done: str = Field(min_length=1)
    version: int = Field(ge=0)
    acceptance_status: SubgoalAcceptanceStatus
