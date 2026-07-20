from dataclasses import dataclass

from mnemograph_domain.errors import InvalidStructuralInputError
from mnemograph_domain.identifiers import GoalId, GoalPlanId, SubgoalId
from mnemograph_domain.versioning import AggregateVersion


@dataclass(frozen=True)
class PlanSubgoalEntry:
    subgoal_id: SubgoalId
    depends_on: tuple[SubgoalId, ...]

    def __post_init__(self) -> None:
        if self.subgoal_id in self.depends_on:
            raise InvalidStructuralInputError("a plan entry cannot depend on itself")
        if len(self.depends_on) != len(set(self.depends_on)):
            raise InvalidStructuralInputError("duplicate dependency edge")


@dataclass(frozen=True)
class GoalDecompositionProposal:
    plan_id: GoalPlanId
    goal_id: GoalId
    version: AggregateVersion
    entries: tuple[PlanSubgoalEntry, ...]

    def __post_init__(self) -> None:
        if self.version < 0:
            raise InvalidStructuralInputError(
                "GoalDecompositionProposal.version must be non-negative"
            )
        _validate_plan_entries(self.entries)


@dataclass(frozen=True)
class ApprovedGoalPlan:
    plan_id: GoalPlanId
    goal_id: GoalId
    version: AggregateVersion
    entries: tuple[PlanSubgoalEntry, ...]

    def __post_init__(self) -> None:
        if self.version < 0:
            raise InvalidStructuralInputError("ApprovedGoalPlan.version must be non-negative")
        _validate_plan_entries(self.entries)


def _validate_plan_entries(entries: tuple[PlanSubgoalEntry, ...]) -> None:
    entry_ids = [entry.subgoal_id for entry in entries]
    if len(entry_ids) != len(set(entry_ids)):
        raise InvalidStructuralInputError("duplicate subgoal_id in plan entries")

    known_ids = set(entry_ids)
    for entry in entries:
        if any(dependency not in known_ids for dependency in entry.depends_on):
            raise InvalidStructuralInputError("dangling dependency edge")

    remaining_dependencies = {entry.subgoal_id: set(entry.depends_on) for entry in entries}
    resolved: set[SubgoalId] = set()
    while len(resolved) < len(remaining_dependencies):
        ready = {
            subgoal_id
            for subgoal_id, dependencies in remaining_dependencies.items()
            if subgoal_id not in resolved and dependencies <= resolved
        }
        if not ready:
            raise InvalidStructuralInputError("plan dependency graph contains a cycle")
        resolved.update(ready)
