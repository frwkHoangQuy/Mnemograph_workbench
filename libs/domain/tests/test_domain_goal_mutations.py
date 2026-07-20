from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from mnemograph_domain import (
    ActorId,
    ActorKind,
    ActorNotPermittedError,
    ActorRef,
    AggregateVersion,
    ApproveGoalPlanCommand,
    BeginScopingCommand,
    CreateGoalCommand,
    Goal,
    GoalId,
    GoalPlanId,
    GoalState,
    GoalVersionConflictError,
    IllegalGoalTransitionError,
    InvalidStructuralInputError,
    PlanSubgoalEntry,
    ProposeGoalDecompositionCommand,
    ReviseGoalPlanCommand,
    Subgoal,
    SubgoalId,
    TransitionEventId,
    approve_goal_plan,
    begin_scoping,
    create_goal,
    create_subgoal,
    propose_goal_decomposition,
    revise_goal_plan,
)

NOW = datetime(2026, 7, 20, 8, tzinfo=UTC)


def _actor(kind: ActorKind) -> ActorRef:
    return ActorRef(kind, ActorId(uuid4()))


def _created_goal() -> Goal:
    return create_goal(
        CreateGoalCommand(
            goal_id=GoalId(uuid4()),
            statement="Research question",
            actor=_actor(ActorKind.USER),
            event_id=TransitionEventId(uuid4()),
            occurred_at=NOW,
        )
    ).goal


def _scoping_goal() -> Goal:
    goal = _created_goal()
    return begin_scoping(
        goal,
        BeginScopingCommand(
            goal_id=goal.goal_id,
            actor=_actor(ActorKind.SYSTEM),
            expected_version=goal.version,
            event_id=TransitionEventId(uuid4()),
            occurred_at=NOW,
        ),
    ).goal


def _proposal_result(goal: Goal | None = None):  # type: ignore[no-untyped-def]
    scoped = goal or _scoping_goal()
    subgoal = create_subgoal(SubgoalId(uuid4()), scoped.goal_id, "Subquestion", "Resolved")
    entry = PlanSubgoalEntry(subgoal.subgoal_id, ())
    return propose_goal_decomposition(
        scoped,
        ProposeGoalDecompositionCommand(
            goal_id=scoped.goal_id,
            actor=_actor(ActorKind.SYSTEM),
            expected_version=scoped.version,
            plan_id=GoalPlanId(uuid4()),
            subgoals=(subgoal,),
            entries=(entry,),
            event_id=TransitionEventId(uuid4()),
            occurred_at=NOW,
        ),
    )


def test_legal_flow_reaches_but_does_not_exceed_deliberating() -> None:
    created = _created_goal()
    assert (created.state, created.version) == (GoalState.DRAFT, 0)
    scoped = _scoping_goal()
    assert (scoped.state, scoped.version) == (GoalState.SCOPING, 1)
    proposed = _proposal_result(scoped)
    assert (proposed.goal.state, proposed.goal.version, proposed.proposal.version) == (
        GoalState.AWAITING_PLAN_APPROVAL,
        2,
        0,
    )
    approved = approve_goal_plan(
        proposed.goal,
        proposed.proposal,
        ApproveGoalPlanCommand(
            goal_id=proposed.goal.goal_id,
            actor=_actor(ActorKind.USER),
            expected_version=proposed.goal.version,
            event_id=TransitionEventId(uuid4()),
            occurred_at=NOW,
        ),
    )
    assert approved.goal.state is GoalState.DELIBERATING
    assert approved.goal.version == 3
    assert approved.approved_plan.plan_id == proposed.proposal.plan_id
    assert approved.approved_plan.version == proposed.proposal.version == 0
    assert approved.goal.current_proposal_plan_id is None
    assert approved.goal.approved_goal_plan_version == 0


def test_revision_clears_linkage_and_allows_fresh_plan_identity() -> None:
    proposed = _proposal_result()
    revised = revise_goal_plan(
        proposed.goal,
        ReviseGoalPlanCommand(
            goal_id=proposed.goal.goal_id,
            actor=_actor(ActorKind.USER),
            expected_version=proposed.goal.version,
            event_id=TransitionEventId(uuid4()),
            occurred_at=NOW,
        ),
    )
    assert revised.goal.state is GoalState.SCOPING
    assert revised.goal.version == proposed.goal.version + 1
    assert revised.goal.current_proposal_plan_id is None
    replacement = _proposal_result(revised.goal)
    assert replacement.proposal.plan_id != proposed.proposal.plan_id
    assert replacement.proposal.version == 0


@pytest.mark.parametrize("kind", [ActorKind.SYSTEM, ActorKind.SCIENTIST, ActorKind.SA])
def test_create_goal_rejects_every_non_user_actor(kind: ActorKind) -> None:
    with pytest.raises(ActorNotPermittedError):
        create_goal(
            CreateGoalCommand(
                GoalId(uuid4()),
                "Question",
                _actor(kind),
                TransitionEventId(uuid4()),
                NOW,
            )
        )


def test_validation_order_actor_then_identity_then_version_then_state() -> None:
    goal = _created_goal()
    base = BeginScopingCommand(
        goal_id=GoalId(uuid4()),
        actor=_actor(ActorKind.USER),
        expected_version=AggregateVersion(99),
        event_id=TransitionEventId(uuid4()),
        occurred_at=NOW,
    )
    with pytest.raises(ActorNotPermittedError):
        begin_scoping(goal, base)
    with pytest.raises(InvalidStructuralInputError):
        begin_scoping(goal, replace(base, actor=_actor(ActorKind.SYSTEM)))
    with pytest.raises(GoalVersionConflictError):
        begin_scoping(
            goal,
            replace(base, actor=_actor(ActorKind.SYSTEM), goal_id=goal.goal_id),
        )
    scoped = _scoping_goal()
    with pytest.raises(IllegalGoalTransitionError):
        begin_scoping(
            scoped,
            replace(
                base,
                actor=_actor(ActorKind.SYSTEM),
                goal_id=scoped.goal_id,
                expected_version=scoped.version,
            ),
        )


def test_every_existing_goal_mutation_rejects_every_non_permitted_actor() -> None:
    draft = _created_goal()
    for kind in (ActorKind.USER, ActorKind.SCIENTIST, ActorKind.SA):
        with pytest.raises(ActorNotPermittedError):
            begin_scoping(
                draft,
                BeginScopingCommand(
                    draft.goal_id,
                    _actor(kind),
                    draft.version,
                    TransitionEventId(uuid4()),
                    NOW,
                ),
            )

    scoped = _scoping_goal()
    for kind in (ActorKind.USER, ActorKind.SCIENTIST, ActorKind.SA):
        with pytest.raises(ActorNotPermittedError):
            propose_goal_decomposition(
                scoped,
                ProposeGoalDecompositionCommand(
                    scoped.goal_id,
                    _actor(kind),
                    scoped.version,
                    GoalPlanId(uuid4()),
                    (),
                    (),
                    TransitionEventId(uuid4()),
                    NOW,
                ),
            )

    proposed = _proposal_result()
    for kind in (ActorKind.SYSTEM, ActorKind.SCIENTIST, ActorKind.SA):
        with pytest.raises(ActorNotPermittedError):
            revise_goal_plan(
                proposed.goal,
                ReviseGoalPlanCommand(
                    proposed.goal.goal_id,
                    _actor(kind),
                    proposed.goal.version,
                    TransitionEventId(uuid4()),
                    NOW,
                ),
            )
        with pytest.raises(ActorNotPermittedError):
            approve_goal_plan(
                proposed.goal,
                proposed.proposal,
                ApproveGoalPlanCommand(
                    proposed.goal.goal_id,
                    _actor(kind),
                    proposed.goal.version,
                    TransitionEventId(uuid4()),
                    NOW,
                ),
            )


def test_every_existing_goal_mutation_rejects_stale_version() -> None:
    draft = _created_goal()
    with pytest.raises(GoalVersionConflictError):
        begin_scoping(
            draft,
            BeginScopingCommand(
                draft.goal_id,
                _actor(ActorKind.SYSTEM),
                AggregateVersion(99),
                TransitionEventId(uuid4()),
                NOW,
            ),
        )

    scoped = _scoping_goal()
    with pytest.raises(GoalVersionConflictError):
        propose_goal_decomposition(
            scoped,
            ProposeGoalDecompositionCommand(
                scoped.goal_id,
                _actor(ActorKind.SYSTEM),
                AggregateVersion(99),
                GoalPlanId(uuid4()),
                (),
                (),
                TransitionEventId(uuid4()),
                NOW,
            ),
        )

    proposed = _proposal_result()
    with pytest.raises(GoalVersionConflictError):
        revise_goal_plan(
            proposed.goal,
            ReviseGoalPlanCommand(
                proposed.goal.goal_id,
                _actor(ActorKind.USER),
                AggregateVersion(99),
                TransitionEventId(uuid4()),
                NOW,
            ),
        )
    with pytest.raises(GoalVersionConflictError):
        approve_goal_plan(
            proposed.goal,
            proposed.proposal,
            ApproveGoalPlanCommand(
                proposed.goal.goal_id,
                _actor(ActorKind.USER),
                AggregateVersion(99),
                TransitionEventId(uuid4()),
                NOW,
            ),
        )


def test_every_illegal_source_state_operation_pair_is_rejected() -> None:
    draft = _created_goal()
    scoped = _scoping_goal()
    proposed = _proposal_result()
    approved = approve_goal_plan(
        proposed.goal,
        proposed.proposal,
        ApproveGoalPlanCommand(
            proposed.goal.goal_id,
            _actor(ActorKind.USER),
            proposed.goal.version,
            TransitionEventId(uuid4()),
            NOW,
        ),
    )
    goals = (draft, scoped, proposed.goal, approved.goal)

    for goal in goals:
        if goal.state is not GoalState.DRAFT:
            with pytest.raises(IllegalGoalTransitionError):
                begin_scoping(
                    goal,
                    BeginScopingCommand(
                        goal.goal_id,
                        _actor(ActorKind.SYSTEM),
                        goal.version,
                        TransitionEventId(uuid4()),
                        NOW,
                    ),
                )
        if goal.state is not GoalState.SCOPING:
            with pytest.raises(IllegalGoalTransitionError):
                propose_goal_decomposition(
                    goal,
                    ProposeGoalDecompositionCommand(
                        goal.goal_id,
                        _actor(ActorKind.SYSTEM),
                        goal.version,
                        GoalPlanId(uuid4()),
                        (),
                        (),
                        TransitionEventId(uuid4()),
                        NOW,
                    ),
                )
        if goal.state is not GoalState.AWAITING_PLAN_APPROVAL:
            with pytest.raises(IllegalGoalTransitionError):
                revise_goal_plan(
                    goal,
                    ReviseGoalPlanCommand(
                        goal.goal_id,
                        _actor(ActorKind.USER),
                        goal.version,
                        TransitionEventId(uuid4()),
                        NOW,
                    ),
                )
            matching_proposal = replace(proposed.proposal, goal_id=goal.goal_id)
            with pytest.raises(IllegalGoalTransitionError):
                approve_goal_plan(
                    goal,
                    matching_proposal,
                    ApproveGoalPlanCommand(
                        goal.goal_id,
                        _actor(ActorKind.USER),
                        goal.version,
                        TransitionEventId(uuid4()),
                        NOW,
                    ),
                )


def test_all_existing_goal_mutations_reject_goal_identity_mismatch() -> None:
    draft = _created_goal()
    with pytest.raises(InvalidStructuralInputError):
        begin_scoping(
            draft,
            BeginScopingCommand(
                GoalId(uuid4()),
                _actor(ActorKind.SYSTEM),
                draft.version,
                TransitionEventId(uuid4()),
                NOW,
            ),
        )
    scoped = _scoping_goal()
    with pytest.raises(InvalidStructuralInputError):
        propose_goal_decomposition(
            scoped,
            ProposeGoalDecompositionCommand(
                GoalId(uuid4()),
                _actor(ActorKind.SYSTEM),
                scoped.version,
                GoalPlanId(uuid4()),
                (),
                (),
                TransitionEventId(uuid4()),
                NOW,
            ),
        )
    proposed = _proposal_result()
    with pytest.raises(InvalidStructuralInputError):
        revise_goal_plan(
            proposed.goal,
            ReviseGoalPlanCommand(
                GoalId(uuid4()),
                _actor(ActorKind.USER),
                proposed.goal.version,
                TransitionEventId(uuid4()),
                NOW,
            ),
        )
    with pytest.raises(InvalidStructuralInputError):
        approve_goal_plan(
            proposed.goal,
            proposed.proposal,
            ApproveGoalPlanCommand(
                GoalId(uuid4()),
                _actor(ActorKind.USER),
                proposed.goal.version,
                TransitionEventId(uuid4()),
                NOW,
            ),
        )


def test_approval_rejects_proposal_goal_or_current_linkage_mismatch() -> None:
    proposed = _proposal_result()
    command = ApproveGoalPlanCommand(
        proposed.goal.goal_id,
        _actor(ActorKind.USER),
        proposed.goal.version,
        TransitionEventId(uuid4()),
        NOW,
    )
    with pytest.raises(InvalidStructuralInputError):
        approve_goal_plan(
            proposed.goal,
            replace(proposed.proposal, goal_id=GoalId(uuid4())),
            command,
        )
    with pytest.raises(InvalidStructuralInputError):
        approve_goal_plan(
            proposed.goal,
            replace(proposed.proposal, plan_id=GoalPlanId(uuid4())),
            command,
        )


@pytest.mark.parametrize("case", ["missing", "extra", "wrong_goal", "duplicate"])
def test_proposal_requires_exact_subgoal_entry_set(case: str) -> None:
    goal = _scoping_goal()
    first = create_subgoal(SubgoalId(uuid4()), goal.goal_id, "One", "Done")
    second = create_subgoal(SubgoalId(uuid4()), goal.goal_id, "Two", "Done")
    subgoals: tuple[Subgoal, ...] = (first,)
    entries = (PlanSubgoalEntry(first.subgoal_id, ()),)
    if case == "missing":
        entries = (PlanSubgoalEntry(second.subgoal_id, ()),)
    elif case == "extra":
        subgoals = (first, second)
    elif case == "wrong_goal":
        subgoals = (replace(first, goal_id=GoalId(uuid4())),)
    else:
        subgoals = (first, first)
    command = ProposeGoalDecompositionCommand(
        goal.goal_id,
        _actor(ActorKind.SYSTEM),
        goal.version,
        GoalPlanId(uuid4()),
        subgoals,
        entries,
        TransitionEventId(uuid4()),
        NOW,
    )
    with pytest.raises(InvalidStructuralInputError):
        propose_goal_decomposition(goal, command)


def test_rejection_never_mutates_original_values() -> None:
    goal = _created_goal()
    snapshot = goal
    with pytest.raises(GoalVersionConflictError):
        begin_scoping(
            goal,
            BeginScopingCommand(
                goal.goal_id,
                _actor(ActorKind.SYSTEM),
                AggregateVersion(99),
                TransitionEventId(uuid4()),
                NOW,
            ),
        )
    assert goal is snapshot
    assert goal.state is GoalState.DRAFT


def test_identical_caller_supplied_values_produce_identical_transitions() -> None:
    command = CreateGoalCommand(
        GoalId(uuid4()),
        "Question",
        _actor(ActorKind.USER),
        TransitionEventId(uuid4()),
        NOW,
    )
    assert create_goal(command).transition == create_goal(command).transition


def test_no_later_delivery_goal_states_exist() -> None:
    assert not hasattr(GoalState, "ACCEPTED")
    assert not hasattr(GoalState, "PUBLISHING")
    assert not hasattr(GoalState, "COMPLETED")
