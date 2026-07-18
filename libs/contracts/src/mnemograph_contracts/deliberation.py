from typing import Annotated, Literal
from uuid import UUID

from pydantic import Discriminator, Field, Tag, TypeAdapter

from mnemograph_contracts._base import ContractModel, _extract_string_tag
from mnemograph_contracts.actors import ActorRef
from mnemograph_contracts.enums import DeliberationSessionState


class DeliberationSessionRecord(ContractModel):
    session_id: UUID
    subgoal_id: UUID
    version: int = Field(ge=0)
    parent_session_id: UUID | None = None
    branched_from_checkpoint_id: UUID | None = None
    state: DeliberationSessionState


class DeliberationTurnRecord(ContractModel):
    turn_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    author: ActorRef
    content: str = Field(min_length=1)


class UserCheckpointRecord(ContractModel):
    checkpoint_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)


class ContinueInterventionRecord(ContractModel):
    intervention_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["CONTINUE"]


class GuideInterventionRecord(ContractModel):
    intervention_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["GUIDE"]
    guidance: str = Field(min_length=1)


class CorrectContextInterventionRecord(ContractModel):
    intervention_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["CORRECT_CONTEXT"]
    correction: str = Field(min_length=1)


class ReviseScopeInterventionRecord(ContractModel):
    intervention_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["REVISE_SCOPE"]
    revision: str = Field(min_length=1)


class PauseInterventionRecord(ContractModel):
    intervention_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["PAUSE"]


class StopInterventionRecord(ContractModel):
    intervention_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["STOP"]


class ReopenCheckpointInterventionRecord(ContractModel):
    intervention_id: UUID
    session_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["REOPEN"]
    target_kind: Literal["CHECKPOINT"]
    checkpoint_id: UUID


class ReopenSubgoalInterventionRecord(ContractModel):
    intervention_id: UUID
    subgoal_id: UUID
    sequence: int = Field(ge=0)
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["REOPEN"]
    target_kind: Literal["SUBGOAL"]


def _intervention_record_tag(value: object) -> str | None:
    action = _extract_string_tag(value, "action")
    if action is None:
        return None

    if action != "REOPEN":
        return action

    target_kind = _extract_string_tag(value, "target_kind")
    if target_kind is None:
        return None

    return f"REOPEN_{target_kind}"


type InterventionRecord = Annotated[
    (
        Annotated[ContinueInterventionRecord, Tag("CONTINUE")]
        | Annotated[GuideInterventionRecord, Tag("GUIDE")]
        | Annotated[CorrectContextInterventionRecord, Tag("CORRECT_CONTEXT")]
        | Annotated[ReviseScopeInterventionRecord, Tag("REVISE_SCOPE")]
        | Annotated[PauseInterventionRecord, Tag("PAUSE")]
        | Annotated[StopInterventionRecord, Tag("STOP")]
        | Annotated[ReopenCheckpointInterventionRecord, Tag("REOPEN_CHECKPOINT")]
        | Annotated[ReopenSubgoalInterventionRecord, Tag("REOPEN_SUBGOAL")]
    ),
    Discriminator(_intervention_record_tag),
]

_INTERVENTION_RECORD_ADAPTER: TypeAdapter[InterventionRecord] = TypeAdapter(InterventionRecord)
