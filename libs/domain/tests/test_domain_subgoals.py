from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest
from mnemograph_domain import (
    AggregateVersion,
    GoalId,
    InvalidStructuralInputError,
    Subgoal,
    SubgoalAcceptanceStatus,
    SubgoalId,
    create_subgoal,
)


def test_create_subgoal_is_plain_deterministic_structural_factory() -> None:
    subgoal_id = SubgoalId(uuid4())
    goal_id = GoalId(uuid4())

    subgoal = create_subgoal(subgoal_id, goal_id, "Question", "Answer it")

    assert subgoal == Subgoal(
        subgoal_id=subgoal_id,
        goal_id=goal_id,
        version=AggregateVersion(0),
        statement="Question",
        definition_of_done="Answer it",
        acceptance_status=SubgoalAcceptanceStatus.NOT_ACCEPTED,
    )
    with pytest.raises(FrozenInstanceError):
        subgoal.statement = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(("statement", "definition"), [(" ", "done"), ("question", "\t")])
def test_subgoal_rejects_whitespace_only_text(statement: str, definition: str) -> None:
    with pytest.raises(InvalidStructuralInputError):
        create_subgoal(SubgoalId(uuid4()), GoalId(uuid4()), statement, definition)


def test_direct_subgoal_construction_rejects_negative_version() -> None:
    with pytest.raises(InvalidStructuralInputError, match="non-negative"):
        Subgoal(
            subgoal_id=SubgoalId(uuid4()),
            goal_id=GoalId(uuid4()),
            version=AggregateVersion(-1),
            statement="Question",
            definition_of_done="Done",
            acceptance_status=SubgoalAcceptanceStatus.NOT_ACCEPTED,
        )
