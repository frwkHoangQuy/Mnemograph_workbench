from uuid import UUID

from pydantic import Field

from mnemograph_contracts._base import ContractModel
from mnemograph_contracts.enums import ActorKind


class ActorRef(ContractModel):
    kind: ActorKind
    actor_id: UUID = Field()
