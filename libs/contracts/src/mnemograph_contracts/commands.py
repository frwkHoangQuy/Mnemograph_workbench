from typing import Annotated, Literal
from uuid import UUID

from pydantic import Discriminator, Field, Tag, TypeAdapter

from mnemograph_contracts._base import ContractModel, _extract_string_tag
from mnemograph_contracts.actors import ActorRef


class ContinueDeliberationCommand(ContractModel):
    session_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["CONTINUE"]


class GuideDeliberationCommand(ContractModel):
    session_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["GUIDE"]
    guidance: str = Field(min_length=1)


class CorrectContextCommand(ContractModel):
    session_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["CORRECT_CONTEXT"]
    correction: str = Field(min_length=1)


class ReviseScopeCommand(ContractModel):
    session_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["REVISE_SCOPE"]
    revision: str = Field(min_length=1)


class PauseDeliberationCommand(ContractModel):
    session_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["PAUSE"]


class StopDeliberationCommand(ContractModel):
    session_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["STOP"]


class ReopenCheckpointCommand(ContractModel):
    session_id: UUID
    checkpoint_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["REOPEN"]
    target_kind: Literal["CHECKPOINT"]


class ReopenSubgoalCommand(ContractModel):
    subgoal_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)
    action: Literal["REOPEN"]
    target_kind: Literal["SUBGOAL"]


class AcceptSubgoalCommand(ContractModel):
    subgoal_id: UUID
    actor: ActorRef
    expected_version: int = Field(ge=0)


def _intervention_command_tag(value: object) -> str | None:
    action = _extract_string_tag(value, "action")
    if action is None:
        return None

    if action != "REOPEN":
        return action

    target_kind = _extract_string_tag(value, "target_kind")
    if target_kind is None:
        return None

    return f"REOPEN_{target_kind}"


type InterventionCommand = Annotated[
    (
        Annotated[ContinueDeliberationCommand, Tag("CONTINUE")]
        | Annotated[GuideDeliberationCommand, Tag("GUIDE")]
        | Annotated[CorrectContextCommand, Tag("CORRECT_CONTEXT")]
        | Annotated[ReviseScopeCommand, Tag("REVISE_SCOPE")]
        | Annotated[PauseDeliberationCommand, Tag("PAUSE")]
        | Annotated[StopDeliberationCommand, Tag("STOP")]
        | Annotated[ReopenCheckpointCommand, Tag("REOPEN_CHECKPOINT")]
        | Annotated[ReopenSubgoalCommand, Tag("REOPEN_SUBGOAL")]
    ),
    Discriminator(_intervention_command_tag),
]

_INTERVENTION_COMMAND_ADAPTER: TypeAdapter[InterventionCommand] = TypeAdapter(InterventionCommand)
