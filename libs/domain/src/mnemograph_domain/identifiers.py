from typing import NewType
from uuid import UUID

ActorId = NewType("ActorId", UUID)
GoalId = NewType("GoalId", UUID)
GoalPlanId = NewType("GoalPlanId", UUID)
SubgoalId = NewType("SubgoalId", UUID)
DeliberationSessionId = NewType("DeliberationSessionId", UUID)
DeliberationTurnId = NewType("DeliberationTurnId", UUID)
UserCheckpointId = NewType("UserCheckpointId", UUID)
InterventionId = NewType("InterventionId", UUID)
