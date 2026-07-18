from uuid import UUID

from pydantic import Field

from mnemograph_contracts._base import ContractModel
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.enums import EvidenceRelationship


class ClaimRecord(ContractModel):
    claim_id: UUID
    author: ActorRef
    text: str = Field(min_length=1)


class EvidenceLinkRecord(ContractModel):
    evidence_link_id: UUID
    claim_id: UUID
    evidence_passage_id: UUID
    relationship: EvidenceRelationship


class ArchitectureIssueRecord(ContractModel):
    architecture_issue_id: UUID
    claim_id: UUID
    author: ActorRef
    summary: str = Field(min_length=1)
