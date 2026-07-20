from dataclasses import dataclass

from mnemograph_domain.enums import SubgoalAcceptanceStatus
from mnemograph_domain.errors import InvalidStructuralInputError
from mnemograph_domain.identifiers import GoalId, SubgoalId
from mnemograph_domain.versioning import AggregateVersion, make_aggregate_version


@dataclass(frozen=True)
class Subgoal:
    subgoal_id: SubgoalId
    goal_id: GoalId
    version: AggregateVersion
    statement: str
    definition_of_done: str
    acceptance_status: SubgoalAcceptanceStatus

    def __post_init__(self) -> None:
        if self.version < 0:
            raise InvalidStructuralInputError("Subgoal.version must be non-negative")
        if not self.statement.strip():
            raise InvalidStructuralInputError("Subgoal.statement must contain non-whitespace")
        if not self.definition_of_done.strip():
            raise InvalidStructuralInputError(
                "Subgoal.definition_of_done must contain non-whitespace"
            )


def create_subgoal(
    subgoal_id: SubgoalId,
    goal_id: GoalId,
    statement: str,
    definition_of_done: str,
) -> Subgoal:
    return Subgoal(
        subgoal_id=subgoal_id,
        goal_id=goal_id,
        version=make_aggregate_version(0),
        statement=statement,
        definition_of_done=definition_of_done,
        acceptance_status=SubgoalAcceptanceStatus.NOT_ACCEPTED,
    )
