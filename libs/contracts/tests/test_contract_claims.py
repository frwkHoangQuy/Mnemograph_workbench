from uuid import UUID

import pytest
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.claims import ArchitectureIssueRecord, ClaimRecord, EvidenceLinkRecord
from mnemograph_contracts.enums import ActorKind, EvidenceRelationship
from pydantic import ValidationError


def _actor() -> ActorRef:
    return ActorRef(kind=ActorKind.USER, actor_id=UUID("00000000-0000-0000-0000-000000000001"))


def test_claim_evidence_architecture_valid() -> None:
    claim = ClaimRecord(
        claim_id=UUID("00000000-0000-0000-0000-000000000100"),
        author=_actor(),
        text="The model selection is traceable.",
    )
    assert claim.text

    for relationship in (EvidenceRelationship.SUPPORTS, EvidenceRelationship.CONTRADICTS):
        link = EvidenceLinkRecord(
            evidence_link_id=UUID("00000000-0000-0000-0000-000000000200"),
            claim_id=claim.claim_id,
            evidence_passage_id=UUID("00000000-0000-0000-0000-000000000300"),
            relationship=relationship,
        )
        assert link.relationship is relationship

    issue = ArchitectureIssueRecord(
        architecture_issue_id=UUID("00000000-0000-0000-0000-000000000400"),
        claim_id=claim.claim_id,
        author=_actor(),
        summary="Needs explicit owner",
    )
    assert issue.summary


def test_claim_text_empty_fails() -> None:
    with pytest.raises(ValidationError):
        ClaimRecord(
            claim_id=UUID("00000000-0000-0000-0000-000000000100"),
            author=_actor(),
            text="",
        )


def test_architecture_issue_summary_empty_fails() -> None:
    with pytest.raises(ValidationError):
        ArchitectureIssueRecord(
            architecture_issue_id=UUID("00000000-0000-0000-0000-000000000400"),
            claim_id=UUID("00000000-0000-0000-0000-000000000100"),
            author=_actor(),
            summary="",
        )


def test_evidence_link_invalid_relationship_fails() -> None:
    with pytest.raises(ValidationError):
        EvidenceLinkRecord.model_validate_json(
            '{"evidence_link_id":"00000000-0000-0000-0000-000000000200","claim_id":"00000000-0000-0000-0000-000000000100","evidence_passage_id":"00000000-0000-0000-0000-000000000300","relationship":"NEUTRAL"}'
        )


def test_evidence_link_unknown_fields_fail() -> None:
    with pytest.raises(ValidationError):
        EvidenceLinkRecord.model_validate_json(
            '{"evidence_link_id":"00000000-0000-0000-0000-000000000200","claim_id":"00000000-0000-0000-0000-000000000100","evidence_passage_id":"00000000-0000-0000-0000-000000000300","relationship":"SUPPORTS","source_version":1}'
        )
    with pytest.raises(ValidationError):
        EvidenceLinkRecord.model_validate_json(
            '{"evidence_link_id":"00000000-0000-0000-0000-000000000200","claim_id":"00000000-0000-0000-0000-000000000100","evidence_passage_id":"00000000-0000-0000-0000-000000000300","relationship":"SUPPORTS","locator":"x"}'
        )
    with pytest.raises(ValidationError):
        EvidenceLinkRecord.model_validate_json(
            '{"evidence_link_id":"00000000-0000-0000-0000-000000000200","claim_id":"00000000-0000-0000-0000-000000000100","evidence_passage_id":"00000000-0000-0000-0000-000000000300","relationship":"SUPPORTS","excerpt_hash":"x"}'
        )


def test_claim_record_frozen_assignment_fails() -> None:
    claim = ClaimRecord(
        claim_id=UUID("00000000-0000-0000-0000-000000000100"),
        author=_actor(),
        text="The model selection is traceable.",
    )
    with pytest.raises(ValidationError):
        claim.text = "changed"


def test_evidence_link_and_architecture_issue_frozen_assignment_fails() -> None:
    link = EvidenceLinkRecord(
        evidence_link_id=UUID("00000000-0000-0000-0000-000000000200"),
        claim_id=UUID("00000000-0000-0000-0000-000000000100"),
        evidence_passage_id=UUID("00000000-0000-0000-0000-000000000300"),
        relationship=EvidenceRelationship.SUPPORTS,
    )
    with pytest.raises(ValidationError):
        link.relationship = EvidenceRelationship.CONTRADICTS

    issue = ArchitectureIssueRecord(
        architecture_issue_id=UUID("00000000-0000-0000-0000-000000000400"),
        claim_id=UUID("00000000-0000-0000-0000-000000000100"),
        author=_actor(),
        summary="Needs explicit owner",
    )
    with pytest.raises(ValidationError):
        issue.summary = "changed"
