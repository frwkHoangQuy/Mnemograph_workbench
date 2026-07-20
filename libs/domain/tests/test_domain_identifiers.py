from uuid import uuid4

from mnemograph_domain import (
    ActorId,
    DeliberationSessionId,
    DeliberationTurnId,
    GoalId,
    GoalPlanId,
    InterventionId,
    SubgoalId,
    UserCheckpointId,
)


def test_identifier_aliases_wrap_uuid_values() -> None:
    value = uuid4()

    assert ActorId(value) == value
    assert GoalId(value) == value
    assert GoalPlanId(value) == value
    assert SubgoalId(value) == value
    assert DeliberationSessionId(value) == value
    assert DeliberationTurnId(value) == value
    assert UserCheckpointId(value) == value
    assert InterventionId(value) == value


def test_identifier_aliases_keep_stable_public_names() -> None:
    assert ActorId.__name__ == "ActorId"
    assert GoalId.__name__ == "GoalId"
    assert GoalPlanId.__name__ == "GoalPlanId"
    assert SubgoalId.__name__ == "SubgoalId"
    assert DeliberationSessionId.__name__ == "DeliberationSessionId"
    assert DeliberationTurnId.__name__ == "DeliberationTurnId"
    assert UserCheckpointId.__name__ == "UserCheckpointId"
    assert InterventionId.__name__ == "InterventionId"
