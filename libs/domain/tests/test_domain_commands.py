from dataclasses import FrozenInstanceError, fields
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from mnemograph_domain import (
    ActorId,
    ActorKind,
    ActorRef,
    AggregateVersion,
    ApproveGoalPlanCommand,
    BeginScopingCommand,
    CreateGoalCommand,
    GoalId,
    GoalPlanId,
    ProposeGoalDecompositionCommand,
    ReviseGoalPlanCommand,
    TransitionEventId,
)


def test_all_five_goal_commands_are_frozen_and_have_exact_roles() -> None:
    goal_id = GoalId(uuid4())
    actor = ActorRef(ActorKind.USER, ActorId(uuid4()))
    event_id = TransitionEventId(uuid4())
    occurred_at = datetime(2026, 7, 20, tzinfo=UTC)
    commands = (
        CreateGoalCommand(goal_id, "Question", actor, event_id, occurred_at),
        BeginScopingCommand(goal_id, actor, AggregateVersion(0), event_id, occurred_at),
        ProposeGoalDecompositionCommand(
            goal_id,
            actor,
            AggregateVersion(0),
            GoalPlanId(uuid4()),
            (),
            (),
            event_id,
            occurred_at,
        ),
        ReviseGoalPlanCommand(goal_id, actor, AggregateVersion(0), event_id, occurred_at),
        ApproveGoalPlanCommand(goal_id, actor, AggregateVersion(0), event_id, occurred_at),
    )

    assert len(commands) == 5
    assert "expected_version" not in {field.name for field in fields(CreateGoalCommand)}
    for command in commands:
        with pytest.raises(FrozenInstanceError):
            command.goal_id = GoalId(uuid4())  # type: ignore[misc]
