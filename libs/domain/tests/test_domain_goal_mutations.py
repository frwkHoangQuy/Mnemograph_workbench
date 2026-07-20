from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone
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
    GoalTransitionRecord,
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
LOCAL_TIME = datetime(2026, 7, 20, 15, 0, tzinfo=timezone(timedelta(hours=7)))


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


def _assert_transition(
    transition: GoalTransitionRecord,
    *,
    goal: Goal,
    event_id: TransitionEventId,
    previous_state: GoalState | None,
    next_state: GoalState,
    actor: ActorRef,
    occurred_at: datetime,
) -> None:
    assert transition.event_id == event_id
    assert transition.goal_id == goal.goal_id
    assert transition.version == goal.version
    assert transition.previous_state is previous_state
    assert transition.next_state is next_state
    assert transition.actor == actor
    assert transition.occurred_at == occurred_at.astimezone(UTC)


def _assert_rejected_atomically(
    operation: Callable[[], object],
    exception_type: type[Exception],
    goal: Goal,
    proposal: object | None = None,
) -> None:
    original_goal = goal
    original_proposal = proposal

    with pytest.raises(exception_type):
        operation()

    assert goal is original_goal
    assert goal == original_goal
    if proposal is not None:
        assert proposal is original_proposal
        assert proposal == original_proposal


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


def test_direct_approval_path_records_every_successful_mutation_value() -> None:
    goal_id = GoalId(uuid4())
    plan_id = GoalPlanId(uuid4())
    subgoal = create_subgoal(SubgoalId(uuid4()), goal_id, "Subquestion", "Resolve it")
    entries = (PlanSubgoalEntry(subgoal.subgoal_id, ()),)

    create_actor = _actor(ActorKind.USER)
    create_event_id = TransitionEventId(uuid4())
    created = create_goal(
        CreateGoalCommand(goal_id, "Research question", create_actor, create_event_id, LOCAL_TIME)
    )
    assert created.goal.goal_id == goal_id
    assert created.goal.state is GoalState.DRAFT
    assert created.goal.version == 0
    assert created.goal.current_proposal_plan_id is None
    assert created.goal.current_proposal_plan_version is None
    assert created.goal.approved_goal_plan_id is None
    assert created.goal.approved_goal_plan_version is None
    _assert_transition(
        created.transition,
        goal=created.goal,
        event_id=create_event_id,
        previous_state=None,
        next_state=GoalState.DRAFT,
        actor=create_actor,
        occurred_at=LOCAL_TIME,
    )

    scoping_actor = _actor(ActorKind.SYSTEM)
    scoping_event_id = TransitionEventId(uuid4())
    scoped = begin_scoping(
        created.goal,
        BeginScopingCommand(
            goal_id, scoping_actor, created.goal.version, scoping_event_id, LOCAL_TIME
        ),
    )
    assert scoped.goal.goal_id == goal_id
    assert scoped.goal.state is GoalState.SCOPING
    assert scoped.goal.version == 1
    assert scoped.goal.current_proposal_plan_id is None
    assert scoped.goal.current_proposal_plan_version is None
    assert scoped.goal.approved_goal_plan_id is None
    assert scoped.goal.approved_goal_plan_version is None
    _assert_transition(
        scoped.transition,
        goal=scoped.goal,
        event_id=scoping_event_id,
        previous_state=GoalState.DRAFT,
        next_state=GoalState.SCOPING,
        actor=scoping_actor,
        occurred_at=LOCAL_TIME,
    )

    proposal_actor = _actor(ActorKind.SYSTEM)
    proposal_event_id = TransitionEventId(uuid4())
    proposed = propose_goal_decomposition(
        scoped.goal,
        ProposeGoalDecompositionCommand(
            goal_id,
            proposal_actor,
            scoped.goal.version,
            plan_id,
            (subgoal,),
            entries,
            proposal_event_id,
            LOCAL_TIME,
        ),
    )
    assert proposed.goal.goal_id == goal_id
    assert proposed.goal.state is GoalState.AWAITING_PLAN_APPROVAL
    assert proposed.goal.version == 2
    assert proposed.goal.current_proposal_plan_id == plan_id
    assert proposed.goal.current_proposal_plan_version == 0
    assert proposed.goal.approved_goal_plan_id is None
    assert proposed.goal.approved_goal_plan_version is None
    assert proposed.proposal.plan_id == plan_id
    assert proposed.proposal.goal_id == goal_id
    assert proposed.proposal.version == 0
    assert proposed.proposal.entries == entries
    _assert_transition(
        proposed.transition,
        goal=proposed.goal,
        event_id=proposal_event_id,
        previous_state=GoalState.SCOPING,
        next_state=GoalState.AWAITING_PLAN_APPROVAL,
        actor=proposal_actor,
        occurred_at=LOCAL_TIME,
    )

    approval_actor = _actor(ActorKind.USER)
    approval_event_id = TransitionEventId(uuid4())
    approved = approve_goal_plan(
        proposed.goal,
        proposed.proposal,
        ApproveGoalPlanCommand(
            goal_id, approval_actor, proposed.goal.version, approval_event_id, LOCAL_TIME
        ),
    )
    assert approved.goal.goal_id == goal_id
    assert approved.goal.state is GoalState.DELIBERATING
    assert approved.goal.version == 3
    assert approved.goal.current_proposal_plan_id is None
    assert approved.goal.current_proposal_plan_version is None
    assert approved.goal.approved_goal_plan_id == plan_id
    assert approved.goal.approved_goal_plan_version == 0
    assert approved.approved_plan.plan_id == proposed.proposal.plan_id
    assert approved.approved_plan.goal_id == proposed.proposal.goal_id
    assert approved.approved_plan.version == proposed.proposal.version
    assert approved.approved_plan.entries == proposed.proposal.entries == entries
    _assert_transition(
        approved.transition,
        goal=approved.goal,
        event_id=approval_event_id,
        previous_state=GoalState.AWAITING_PLAN_APPROVAL,
        next_state=GoalState.DELIBERATING,
        actor=approval_actor,
        occurred_at=LOCAL_TIME,
    )


def test_revision_and_reproposal_path_preserves_every_successful_mutation_value() -> None:
    goal_id = GoalId(uuid4())
    created = create_goal(
        CreateGoalCommand(
            goal_id,
            "Research question",
            _actor(ActorKind.USER),
            TransitionEventId(uuid4()),
            LOCAL_TIME,
        )
    )
    scoped = begin_scoping(
        created.goal,
        BeginScopingCommand(
            goal_id,
            _actor(ActorKind.SYSTEM),
            created.goal.version,
            TransitionEventId(uuid4()),
            LOCAL_TIME,
        ),
    )
    first_subgoal = create_subgoal(SubgoalId(uuid4()), goal_id, "First", "Done")
    first = propose_goal_decomposition(
        scoped.goal,
        ProposeGoalDecompositionCommand(
            goal_id,
            _actor(ActorKind.SYSTEM),
            scoped.goal.version,
            GoalPlanId(uuid4()),
            (first_subgoal,),
            (PlanSubgoalEntry(first_subgoal.subgoal_id, ()),),
            TransitionEventId(uuid4()),
            LOCAL_TIME,
        ),
    )

    revise_actor = _actor(ActorKind.USER)
    revise_event_id = TransitionEventId(uuid4())
    revised = revise_goal_plan(
        first.goal,
        ReviseGoalPlanCommand(
            goal_id, revise_actor, first.goal.version, revise_event_id, LOCAL_TIME
        ),
    )
    assert revised.goal.goal_id == goal_id
    assert revised.goal.state is GoalState.SCOPING
    assert revised.goal.version == 3
    assert revised.goal.current_proposal_plan_id is None
    assert revised.goal.current_proposal_plan_version is None
    assert revised.goal.approved_goal_plan_id is None
    assert revised.goal.approved_goal_plan_version is None
    _assert_transition(
        revised.transition,
        goal=revised.goal,
        event_id=revise_event_id,
        previous_state=GoalState.AWAITING_PLAN_APPROVAL,
        next_state=GoalState.SCOPING,
        actor=revise_actor,
        occurred_at=LOCAL_TIME,
    )

    second_subgoal = create_subgoal(SubgoalId(uuid4()), goal_id, "Second", "Done")
    second_entries = (PlanSubgoalEntry(second_subgoal.subgoal_id, ()),)
    reproposal_actor = _actor(ActorKind.SYSTEM)
    reproposal_event_id = TransitionEventId(uuid4())
    reproposed = propose_goal_decomposition(
        revised.goal,
        ProposeGoalDecompositionCommand(
            goal_id,
            reproposal_actor,
            revised.goal.version,
            GoalPlanId(uuid4()),
            (second_subgoal,),
            second_entries,
            reproposal_event_id,
            LOCAL_TIME,
        ),
    )
    assert reproposed.goal.goal_id == goal_id
    assert reproposed.goal.state is GoalState.AWAITING_PLAN_APPROVAL
    assert reproposed.goal.version == 4
    assert reproposed.goal.current_proposal_plan_id == reproposed.proposal.plan_id
    assert reproposed.goal.current_proposal_plan_version == reproposed.proposal.version == 0
    assert reproposed.goal.approved_goal_plan_id is None
    assert reproposed.goal.approved_goal_plan_version is None
    assert reproposed.proposal.goal_id == goal_id
    assert reproposed.proposal.entries == second_entries
    assert reproposed.proposal.plan_id != first.proposal.plan_id
    _assert_transition(
        reproposed.transition,
        goal=reproposed.goal,
        event_id=reproposal_event_id,
        previous_state=GoalState.SCOPING,
        next_state=GoalState.AWAITING_PLAN_APPROVAL,
        actor=reproposal_actor,
        occurred_at=LOCAL_TIME,
    )


def test_approval_rejects_current_proposal_version_mismatch_without_mutation() -> None:
    proposed = _proposal_result()
    mismatched_proposal = replace(proposed.proposal, version=AggregateVersion(1))
    command = ApproveGoalPlanCommand(
        proposed.goal.goal_id,
        _actor(ActorKind.USER),
        proposed.goal.version,
        TransitionEventId(uuid4()),
        LOCAL_TIME,
    )

    _assert_rejected_atomically(
        lambda: approve_goal_plan(proposed.goal, mismatched_proposal, command),
        InvalidStructuralInputError,
        proposed.goal,
        mismatched_proposal,
    )


def test_proposal_rejects_duplicate_entry_ids_with_unique_supplied_subgoals() -> None:
    scoped = _scoping_goal()
    first = create_subgoal(SubgoalId(uuid4()), scoped.goal_id, "First", "Done")
    second = create_subgoal(SubgoalId(uuid4()), scoped.goal_id, "Second", "Done")
    duplicate_entries = (
        PlanSubgoalEntry(first.subgoal_id, ()),
        PlanSubgoalEntry(first.subgoal_id, ()),
    )
    command = ProposeGoalDecompositionCommand(
        scoped.goal_id,
        _actor(ActorKind.SYSTEM),
        scoped.version,
        GoalPlanId(uuid4()),
        (first, second),
        duplicate_entries,
        TransitionEventId(uuid4()),
        LOCAL_TIME,
    )

    _assert_rejected_atomically(
        lambda: propose_goal_decomposition(scoped, command),
        InvalidStructuralInputError,
        scoped,
    )


def test_propose_validation_precedence_covers_actor_identity_version_state_and_payload() -> None:
    scoped = _scoping_goal()
    payload_subgoal = create_subgoal(SubgoalId(uuid4()), scoped.goal_id, "One", "Done")
    payload_command = ProposeGoalDecompositionCommand(
        GoalId(uuid4()),
        _actor(ActorKind.USER),
        AggregateVersion(99),
        GoalPlanId(uuid4()),
        (payload_subgoal,),
        (),
        TransitionEventId(uuid4()),
        LOCAL_TIME,
    )
    _assert_rejected_atomically(
        lambda: propose_goal_decomposition(scoped, payload_command),
        ActorNotPermittedError,
        scoped,
    )
    _assert_rejected_atomically(
        lambda: propose_goal_decomposition(
            scoped, replace(payload_command, actor=_actor(ActorKind.SYSTEM))
        ),
        InvalidStructuralInputError,
        scoped,
    )
    _assert_rejected_atomically(
        lambda: propose_goal_decomposition(
            scoped,
            replace(
                payload_command,
                actor=_actor(ActorKind.SYSTEM),
                goal_id=scoped.goal_id,
            ),
        ),
        GoalVersionConflictError,
        scoped,
    )
    draft = _created_goal()
    _assert_rejected_atomically(
        lambda: propose_goal_decomposition(
            draft,
            replace(
                payload_command,
                actor=_actor(ActorKind.SYSTEM),
                goal_id=draft.goal_id,
                expected_version=draft.version,
            ),
        ),
        IllegalGoalTransitionError,
        draft,
    )
    _assert_rejected_atomically(
        lambda: propose_goal_decomposition(
            scoped,
            replace(
                payload_command,
                actor=_actor(ActorKind.SYSTEM),
                goal_id=scoped.goal_id,
                expected_version=scoped.version,
            ),
        ),
        InvalidStructuralInputError,
        scoped,
    )


def test_begin_scoping_validation_precedence_covers_actor_identity_version_and_state() -> None:
    draft = _created_goal()
    command = BeginScopingCommand(
        GoalId(uuid4()),
        _actor(ActorKind.USER),
        AggregateVersion(99),
        TransitionEventId(uuid4()),
        LOCAL_TIME,
    )
    _assert_rejected_atomically(
        lambda: begin_scoping(draft, command), ActorNotPermittedError, draft
    )
    _assert_rejected_atomically(
        lambda: begin_scoping(draft, replace(command, actor=_actor(ActorKind.SYSTEM))),
        InvalidStructuralInputError,
        draft,
    )
    _assert_rejected_atomically(
        lambda: begin_scoping(
            draft,
            replace(command, actor=_actor(ActorKind.SYSTEM), goal_id=draft.goal_id),
        ),
        GoalVersionConflictError,
        draft,
    )
    scoped = _scoping_goal()
    _assert_rejected_atomically(
        lambda: begin_scoping(
            scoped,
            replace(
                command,
                actor=_actor(ActorKind.SYSTEM),
                goal_id=scoped.goal_id,
                expected_version=scoped.version,
            ),
        ),
        IllegalGoalTransitionError,
        scoped,
    )


def test_revise_validation_precedence_covers_actor_identity_version_and_state() -> None:
    proposed = _proposal_result()
    command = ReviseGoalPlanCommand(
        GoalId(uuid4()),
        _actor(ActorKind.SYSTEM),
        AggregateVersion(99),
        TransitionEventId(uuid4()),
        LOCAL_TIME,
    )
    _assert_rejected_atomically(
        lambda: revise_goal_plan(proposed.goal, command),
        ActorNotPermittedError,
        proposed.goal,
        proposed.proposal,
    )
    _assert_rejected_atomically(
        lambda: revise_goal_plan(proposed.goal, replace(command, actor=_actor(ActorKind.USER))),
        InvalidStructuralInputError,
        proposed.goal,
        proposed.proposal,
    )
    _assert_rejected_atomically(
        lambda: revise_goal_plan(
            proposed.goal,
            replace(command, actor=_actor(ActorKind.USER), goal_id=proposed.goal.goal_id),
        ),
        GoalVersionConflictError,
        proposed.goal,
        proposed.proposal,
    )
    scoped = _scoping_goal()
    _assert_rejected_atomically(
        lambda: revise_goal_plan(
            scoped,
            replace(
                command,
                actor=_actor(ActorKind.USER),
                goal_id=scoped.goal_id,
                expected_version=scoped.version,
            ),
        ),
        IllegalGoalTransitionError,
        scoped,
    )


def test_approval_validation_precedence_covers_actor_identities_version_state_and_linkage() -> None:
    proposed = _proposal_result()
    command = ApproveGoalPlanCommand(
        GoalId(uuid4()),
        _actor(ActorKind.SYSTEM),
        AggregateVersion(99),
        TransitionEventId(uuid4()),
        LOCAL_TIME,
    )
    wrong_proposal = replace(proposed.proposal, goal_id=GoalId(uuid4()))
    _assert_rejected_atomically(
        lambda: approve_goal_plan(proposed.goal, wrong_proposal, command),
        ActorNotPermittedError,
        proposed.goal,
        wrong_proposal,
    )
    _assert_rejected_atomically(
        lambda: approve_goal_plan(
            proposed.goal, proposed.proposal, replace(command, actor=_actor(ActorKind.USER))
        ),
        InvalidStructuralInputError,
        proposed.goal,
        proposed.proposal,
    )
    _assert_rejected_atomically(
        lambda: approve_goal_plan(
            proposed.goal,
            wrong_proposal,
            replace(command, actor=_actor(ActorKind.USER), goal_id=proposed.goal.goal_id),
        ),
        InvalidStructuralInputError,
        proposed.goal,
        wrong_proposal,
    )
    _assert_rejected_atomically(
        lambda: approve_goal_plan(
            proposed.goal,
            proposed.proposal,
            replace(
                command,
                actor=_actor(ActorKind.USER),
                goal_id=proposed.goal.goal_id,
            ),
        ),
        GoalVersionConflictError,
        proposed.goal,
        proposed.proposal,
    )
    scoped = _scoping_goal()
    scoped_proposal = replace(proposed.proposal, goal_id=scoped.goal_id)
    _assert_rejected_atomically(
        lambda: approve_goal_plan(
            scoped,
            scoped_proposal,
            replace(
                command,
                actor=_actor(ActorKind.USER),
                goal_id=scoped.goal_id,
                expected_version=scoped.version,
            ),
        ),
        IllegalGoalTransitionError,
        scoped,
        scoped_proposal,
    )
    linkage_mismatch = replace(proposed.proposal, plan_id=GoalPlanId(uuid4()))
    _assert_rejected_atomically(
        lambda: approve_goal_plan(
            proposed.goal,
            linkage_mismatch,
            replace(
                command,
                actor=_actor(ActorKind.USER),
                goal_id=proposed.goal.goal_id,
                expected_version=proposed.goal.version,
            ),
        ),
        InvalidStructuralInputError,
        proposed.goal,
        linkage_mismatch,
    )
