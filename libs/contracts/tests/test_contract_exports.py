import mnemograph_contracts as contracts
import pytest
from mnemograph_contracts import (
    AcceptSubgoalCommand,
    ActorKind,
    ActorRef,
    ArchitectureIssueRecord,
    ClaimRecord,
    ContinueDeliberationCommand,
    ContinueInterventionRecord,
    CorrectContextCommand,
    CorrectContextInterventionRecord,
    DeliberationSessionRecord,
    DeliberationSessionState,
    DeliberationSessionTransitionRecord,
    DeliberationTurnRecord,
    EvidenceLinkRecord,
    EvidenceRelationship,
    GoalCreateRequest,
    GoalResponse,
    GoalState,
    GoalTransitionRecord,
    GuideDeliberationCommand,
    GuideInterventionRecord,
    InterventionCommand,
    InterventionKind,
    InterventionRecord,
    PauseDeliberationCommand,
    PauseInterventionRecord,
    ReopenCheckpointCommand,
    ReopenCheckpointInterventionRecord,
    ReopenSubgoalCommand,
    ReopenSubgoalInterventionRecord,
    ReviseScopeCommand,
    ReviseScopeInterventionRecord,
    StopDeliberationCommand,
    StopInterventionRecord,
    SubgoalAcceptanceStatus,
    SubgoalCreateRequest,
    SubgoalResponse,
    SubgoalTransitionRecord,
    UserCheckpointRecord,
    ValidationErrorCode,
    ValidationErrorEnvelope,
    ValidationIssue,
)


def test_public_exports_available() -> None:
    assert ActorKind.USER.value == "USER"
    assert GoalState.DRAFT.value == "DRAFT"
    assert InterventionKind.REOPEN.value == "REOPEN"
    assert SubgoalAcceptanceStatus.NOT_ACCEPTED.value == "NOT_ACCEPTED"
    assert DeliberationSessionState.SESSION_ACTIVE.value == "SESSION_ACTIVE"
    assert EvidenceRelationship.SUPPORTS.value == "SUPPORTS"
    assert ValidationErrorCode.INVALID_VALUE.value == "INVALID_VALUE"

    assert GoalCreateRequest is not None
    assert GoalResponse is not None
    assert SubgoalCreateRequest is not None
    assert SubgoalResponse is not None
    assert ActorRef is not None
    assert DeliberationSessionRecord is not None
    assert DeliberationTurnRecord is not None
    assert UserCheckpointRecord is not None
    assert ContinueInterventionRecord is not None
    assert GuideInterventionRecord is not None
    assert CorrectContextInterventionRecord is not None
    assert ReviseScopeInterventionRecord is not None
    assert PauseInterventionRecord is not None
    assert StopInterventionRecord is not None
    assert ReopenCheckpointInterventionRecord is not None
    assert ReopenSubgoalInterventionRecord is not None
    assert InterventionRecord is not None
    assert ClaimRecord is not None
    assert EvidenceLinkRecord is not None
    assert ArchitectureIssueRecord is not None
    assert ContinueDeliberationCommand is not None
    assert GuideDeliberationCommand is not None
    assert CorrectContextCommand is not None
    assert ReviseScopeCommand is not None
    assert PauseDeliberationCommand is not None
    assert StopDeliberationCommand is not None
    assert ReopenCheckpointCommand is not None
    assert ReopenSubgoalCommand is not None
    assert AcceptSubgoalCommand is not None
    assert InterventionCommand is not None
    assert GoalTransitionRecord is not None
    assert SubgoalTransitionRecord is not None
    assert DeliberationSessionTransitionRecord is not None
    assert ValidationIssue is not None
    assert ValidationErrorEnvelope is not None


def test_private_symbols_not_exported() -> None:
    with pytest.raises(AttributeError):
        contracts.__getattribute__("_intervention_command_tag")
    with pytest.raises(AttributeError):
        contracts.__getattribute__("_intervention_record_tag")
    with pytest.raises(AttributeError):
        contracts.__getattribute__("_map_pydantic_error_type")
    with pytest.raises(AttributeError):
        contracts.__getattribute__("_validation_error_to_envelope")
    with pytest.raises(AttributeError):
        contracts.__getattribute__("ContractModel")
