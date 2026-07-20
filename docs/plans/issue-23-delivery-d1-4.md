# Delivery D1.4 Final Implementation Plan — Issue #23 — v1.5

Status: **DRAFT PLAN FOR LEAD-SA AND HUMAN REVIEW. NOT AN IMPLEMENTATION.**

Implementation authorization: **NOT APPROVED.**

This is a complete, standalone revision. Plan v1.5 supersedes Plan v1.4 in
full and does not require an earlier plan to be read alongside it. It
preserves every substantive R1, R2, R3, and R4 decision. In particular, it
retains the R3-01 boundary-test reconciliation, the R3-02 complete
direct-construction invariants for the three public result types, and the
R4 restoration of the public structural factory `create_subgoal` to the
package-root API.

**Current planning-artifact provenance.** The canonical active Plan v1.5
artifact is this tracked file:
`docs/plans/issue-23-delivery-d1-4.md`. Its planning-only branch is
`planning/23-d1-4-goal-plan`. The branch and tracked file exist only to
support plan review. This planning branch must never be merged into `main`,
and their existence grants no implementation authorization.

**Disclosure required by R1-11 (historical provenance; carried forward,
unchanged in substance).** Plan v1.0 was written to the historical ignored
file `tmp/delivery-d1.4-final-implementation-plan-v1.0.md` under a prior
planning turn whose own prompt (per the R1 review) prohibited creating or
writing repository files, including ignored files — that write was a
planning-process deviation, not an equivalence between "writing an ignored
file" and "no workspace mutation." Plan v1.1 was subsequently written to
the historical ignored file `tmp/delivery-d1-4-plan-v1.1.md` under an
explicit authorization permitting exactly that one write. Neither historical
ignored file is the current or canonical Plan v1.5 artifact. The reviewed
artifact was migrated to the tracked planning path by commit
`11a30b7b6ff22995e51dbc5de51a510acdbb2817`; the R4 correction was then
recorded by commit `7757c80ac3bc7561891cf8f82110cad78dd70b3e`.

---

## A. Summary and boundary

**Objective.** Plan the first Goal Management domain-behavior vertical
slice on top of the completed Delivery D1.3 pure-domain primitives. The
slice creates a Goal, moves it through scoping, attaches a decomposition
proposal, allows user-directed revision, and allows user approval — and
stops the instant the Goal first enters `DELIBERATING`.

**Exact start boundary.** No `Goal`, `Subgoal`, `GoalDecompositionProposal`,
or `ApprovedGoalPlan` type exists in `mnemograph_domain` today.

**Exact stop boundary (unchanged across R1 and R2).** The Goal's first
transition into `DELIBERATING`. No `DELIBERATING -> AWAITING_USER`, no
DeliberationSession, no Subgoal *acceptance or reopen* behavior, no
`CROSS_GOAL_REVIEW`, `FINAL_CANDIDATE`, `STOPPED`, or Delivery D5 concept is
in scope. Subgoal *creation* is in scope only as a **plain structural
factory** (R2-01, superseding R1's version of this boundary): it
establishes `Subgoal`'s independent identity and version at `0`/
`NOT_ACCEPTED` using caller-supplied identifiers, but it is not framed as a
"mutation" — it carries no command object, no actor-authority rule, no
`expected_version`, no event identifier, no timestamp, and it emits no
transition record. Subgoal's *acceptance/reopen mutation* behavior remains
entirely deferred, unchanged from R1.

**Disposition of the R1 review (carried forward).** Every R1-01 through
R1-11 requirement was treated as binding for v1.1 and remains satisfied by
v1.5 except where R2 explicitly narrows or reverses a v1.1 choice (noted
per DR ID in Section D). The R1-accepted parts of v1.0 — the checkpoint,
the `DELIBERATING` stop boundary, the accepted `GoalState` vocabulary,
USER-only revision/approval, `SYSTEM` as the recommended orchestration
issuer for the four Goal mutations, optimistic concurrency with
exactly-one Goal-version increment, immutable transition emission without
persistence, the standard-library-only domain boundary, the
no-contracts/no-dependency/no-infrastructure boundary, and one initial
implementation commit followed only by separate correction commits if
later authorized — remain preserved.

**Disposition of the R2 review.** Every R2-01 through R2-07 requirement is
treated as binding for this v1.5 revision. Section D marks, for every DR
ID, whether R2 left it Unchanged, further Superseded, Removed, or newly
introduced it, with an explicit R2 cross-reference. The R2 review's
"Accepted corrections" list is preserved unless a specific R2 item
required further change: verified checkpoint and clean-state evidence;
deterministic caller-supplied IDs and timestamps; independent Subgoal
identity/version foundation; Goal ID/version plan linkage; separated
display order and dependency DAG; named domain errors; explicit
domain/contract mapping; non-whitespace domain string policy;
semantic-only runtime validation policy; the exact `DELIBERATING` stop
boundary; and the dependency/contracts/infrastructure exclusions.

**Disposition of the R3 correction.** R3-01 and R3-02 are binding for this
v1.5 revision. R3-01 reconciles the inherited D1.3 boundary-test baseline:
`TransitionEventId` is no longer forbidden, the obsolete blanket ban on
domain `datetime` imports and datetime-related public helpers is replaced,
and a narrow allowlist asserts the sole authorized datetime surface
(`datetime` from the standard library and `ensure_aware_utc`). R3-02
completes the public result-value invariants without adding a type, module,
test path, exception, export, or changed path.

**Disposition of the R4 correction.** R4 restores `create_subgoal` as a
package-root export. This is a newly proposed public-API decision requiring
explicit human approval: `create_subgoal` is a public structural factory, and
root-exporting it keeps the domain API consistent. It changes no planned path,
module, test path, dependency, implementation behavior, or delivery scope.

**Why this remains one reviewable vertical slice.** The design still
involves three independently versioned things (`Goal`, `Subgoal`,
`GoalPlan`-family), but all three are still needed together to reach
`DELIBERATING` at all — a `Goal` cannot legally reach
`AWAITING_PLAN_APPROVAL` without a `GoalDecompositionProposal`, which
cannot legally exist without at least the option of referencing
independently created `Subgoal`s. Splitting this into separate commits
would leave intermediate, non-independently-testable states.

**Implementation authorization.** This document is a plan only. Its tracked
review branch and canonical artifact authorize no implementation activity.
A separate, explicit human implementation approval is required after Lead-SA
review, exactly as occurred for Delivery D1.3.

---

## B. Preflight evidence

**Plan v1.5 correction-session preflight (before this edit).**

| Check | Command | Result |
|---|---|---|
| Repository root | `git rev-parse --show-toplevel` | `D:/Dev/mnemograph-workbench` |
| Current branch | `git branch --show-current` | `planning/23-d1-4-goal-plan` |
| `origin/main` | `git rev-parse origin/main` | `eb43e1248b563c3e3117a971deacb140092e908f` |
| Local planning branch | `git rev-parse planning/23-d1-4-goal-plan` | `7757c80ac3bc7561891cf8f82110cad78dd70b3e` |
| Remote planning branch | `git rev-parse origin/planning/23-d1-4-goal-plan` | `7757c80ac3bc7561891cf8f82110cad78dd70b3e` |
| Working tree and index | `git status --porcelain=v1` | *(empty — clean)* |
| Canonical artifact | `git ls-files --error-unmatch docs/plans/issue-23-delivery-d1-4.md` | tracked file exists |
| R4 parent | `git rev-parse 7757c80ac3bc7561891cf8f82110cad78dd70b3e^` | `11a30b7b6ff22995e51dbc5de51a510acdbb2817` |
| R4 changed paths | `git diff-tree --no-commit-id --name-only -r 7757c80ac3bc7561891cf8f82110cad78dd70b3e` | only `docs/plans/issue-23-delivery-d1-4.md` |

The historical v1.0 and v1.1 ignored files named in the R1-11 disclosure
are retained solely as historical provenance. The current active artifact is
the tracked canonical path above, on the planning-only branch above. The
branch and file support plan review only; the branch must never be merged
into `main`, and neither grants implementation authorization.

---

## C. Source-of-truth traceability (corrected)

| Behavior area | Authoritative source | Classification | Disposition |
|---|---|---|---|
| Goal lifecycle vocabulary (`DRAFT`…`DELIBERATING`…) | ADR-DOMAIN-003 Decision A; existing `mnemograph_domain.enums.GoalState` | Fixed | Unchanged — R1/R2 both accept |
| Candidate 5-step lifecycle for this slice | Issue #23 Objective/"Goal lifecycle" | Fixed | Unchanged |
| `ActorKind` = `USER`/`SCIENTIST`/`SA`/`SYSTEM`; Moderator is policy, not a kind | ADR-DOMAIN-002 Option B; ADR-DOMAIN-001 D1-D | Fixed | Unchanged |
| Identifiers use `typing.NewType` over `uuid.UUID` | ADR-DOMAIN-001 D1-D | Fixed (rule) | Unchanged |
| `GoalId`, `GoalPlanId`, `SubgoalId` already exist | Delivery D1.3 | Fixed | Unchanged; all three used with corrected semantics |
| Timestamps timezone-aware, UTC-normalized; naive rejected | ADR-DOMAIN-001 D1-D | Fixed (rule) | Unchanged rule; caller-supplied injection mechanism (R1-03) unchanged by R2 |
| Aggregate versions non-negative; mutating commands carry `expected_version`; successful mutation increments exactly once | ADR-DOMAIN-001 D1-D | Fixed | Unchanged rule; creation's factory-exemption reasoning (R1-07) unchanged by R2 |
| `Goal` owns decomposition/approved-plan *linkage*; Subgoal has an **independently testable lifecycle** | ADR-DOMAIN-001 D1-E | Fixed | R1-01 corrected v1.0's unversioned-value-object error; R2-01 further narrows Subgoal *creation* to a plain structural factory with no lifecycle-mutation trappings |
| Existing `SubgoalResponse`/`AcceptSubgoalCommand` already carry Subgoal identity+version | `libs/contracts/src/mnemograph_contracts/subgoals.py`, `commands.py` (unchanged, existing) | Fixed (existing) | Unchanged since R1-01 |
| Charter's `approved_goal_plan_version` linkage convention | Cited by the R1 review as an accepted-Charter term | Fixed (per R1-02's citation) | R2-02 further clarifies: approval **preserves**, does not increment, this value |
| `GoalTransitionRecord` contract shape | `libs/contracts/src/mnemograph_contracts/events.py` (unchanged) | Fixed | Unchanged shape; explicit-mapping compatibility method (R1-09) unchanged by R2 |
| Pydantic `Field(min_length=1)` accepts whitespace-only strings | `libs/contracts/src/mnemograph_contracts/goals.py`, `subgoals.py` (unchanged) — Pydantic library behavior | Fixed (factual correction) | Unchanged since R1-08 |
| `mnemograph_domain` remains stdlib-only | ADR-DOMAIN-001 D1-B/D1-C | Fixed | Unchanged |
| D1.3 "no custom exception" test freezes the D1.3 primitive surface, not a permanent ban | R1-07's explicit reading of Delivery D1.3's test intent | Fixed (clarification) | Unchanged; the 4 named errors (DR-08) are extended by R2-04 to cover additional invariant categories, no new class added |
| Every mutation over an existing `Goal` must reject a command whose `goal_id` does not match the `Goal` it is applied to; `approve_goal_plan` must additionally reject a supplied `proposal.goal_id` mismatch | R2-03 | Binding correction | New — identity guards added to every mutation over an existing `Goal` |
| Approval preserves the proposal's `plan_id` **and** content `version` unchanged; only `Goal.version` increments | R2-02 | Binding correction | Reverses v1.1's "promotion increments the shared plan-version lineage" rule |
| Subgoal creation in D1.4 is a plain structural factory only — no command object, no actor guard, no `expected_version`, no event identifier, no timestamp, no transition emission | R2-01 | Binding correction | Removes v1.1's `CreateSubgoalCommand`, DR-20, and the `SYSTEM`/`create_subgoal` authority-matrix row |
| `PlanSubgoalEntry.depends_on` must be able to represent — and therefore reject — a duplicate dependency edge, which a `frozenset` field cannot represent by the time `__post_init__` runs | R2-05 | Binding correction (factual) | Changes the field type from `frozenset[SubgoalId]` to `tuple[SubgoalId, ...]`, with an explicit duplicate check |
| A single `GoalMutationResult` type permitted representing inconsistent optional-payload combinations that no mutation ever produces | R2-04 | Binding correction | Replaced by three distinct result types (`GoalTransitionResult`, `GoalProposalResult`, `GoalApprovalResult`) whose shape alone makes the invalid combinations unrepresentable |
| Inherited D1.3 boundary assertions still forbid `TransitionEventId` and blanket-forbid domain datetime imports/helpers | R3-01 | Binding correction | Remove `TransitionEventId` from `FORBIDDEN_EXPORTS`; replace/remove the obsolete blanket datetime prohibition while retaining the AST stdlib-only import boundary and adding a narrow authorized-datetime-surface assertion |
| The three public result types lack complete direct-construction consistency invariants | R3-02 | Binding correction | Retain the three result classes and existing transition checks; add state/payload and Goal-linkage checks to each class, all raising `InvalidStructuralInputError` |
| No dependency/lockfile/contracts-production/baseline/ADR/app/infra/workflow/Compose change | Issue #23 | Fixed | Unchanged |

---

## D. Revised consolidated decision register

Every unresolved row is a single Lead-SA/human decision point. **Status**
marks whether the DR ID is **Unchanged**, **Superseded** (recommendation
reversed/materially altered), **Removed** (the underlying question no
longer applies), or **New**. Stable DR IDs are retained wherever the
underlying question is unchanged. No item is silently pre-selected; every
downstream section built on a recommendation re-flags the DR ID.

| ID | Status | Question | Accepted-source constraints | Bounded options | Trade-offs | Recommendation (non-binding) | Blocked elements |
|---|---|---|---|---|---|---|---|
| DR-01 | **Superseded** (R1-01; further narrowed R2-01) | Is Subgoal a value object inside Goal, or an independently identified and versioned entity? | ADR-DOMAIN-001 D1-E ("independently testable lifecycle"); existing `SubgoalResponse`/`AcceptSubgoalCommand` already carry identity+version; R1-01/R2-01 are explicit and binding. | (a) Independently versioned entity with its own `subgoal_id`, `goal_id`, `version`, `statement`, `definition_of_done`, `acceptance_status`, created via a **plain structural factory** at version `0`/`NOT_ACCEPTED` (R2-01: no command, no actor guard, no event, no transition). (b) v1.0's original unversioned value object (**rejected by R1-01**). (c) v1.1's `CreateSubgoalCommand`+`SYSTEM`-guarded factory (**rejected by R2-01** as an unsupported middle state between "merely structural" and "lifecycle behavior"). | (a) matches the accepted boundary, existing contract shapes, and R2's explicit narrowing; (b)/(c) are both explicitly rejected. | (a) | `Subgoal` shape (F), ownership model (E), transition matrix (G) |
| DR-02 | **Superseded** (R1-02) | Do `GoalDecompositionProposal`/`ApprovedGoalPlan` carry their own version? | R1-02 cites the Charter's `approved_goal_plan_version` linkage convention as binding context; R2-02 confirms a plan version field is still appropriate, only its *increment behavior* changes. | (a) Yes — a `GoalPlan`-family version, independent of Goal's version, but (per R2-02) **never incremented within this slice** since no operation mutates a plan's own content after creation. (b) No independent version (v1.0's original recommendation, rejected by R1-02). | (a) matches the cited linkage convention; (b) is explicitly rejected. | (a) | `GoalDecompositionProposal`/`ApprovedGoalPlan` shape (F), Goal linkage (E, F) |
| DR-03 | Unchanged | Who issues `DRAFT -> SCOPING`? | R1/R2 "Accepted"/"Accepted corrections" lists both name `SYSTEM` attribution as the recommended issuer for orchestration mutations. | (a) `SYSTEM`. (b) `USER`. | (a) matches both reviews' accepted direction. | (a) | `BeginScopingCommand`/`begin_scoping` (F), authority matrix (G) |
| DR-04 | Unchanged | Who issues `SCOPING -> AWAITING_PLAN_APPROVAL`? | Same accepted `SYSTEM`-attribution direction; Charter §8.1 "Orchestrator tạo…". | (a) `SYSTEM`. (b) `USER`. | (a) matches Charter wording and both reviews' accepted direction. | (a) | `ProposeGoalDecompositionCommand`/`propose_goal_decomposition` (F), authority matrix (G) |
| DR-05 | Unchanged (still open) | Does revision (`AWAITING_PLAN_APPROVAL -> SCOPING`) clear or retain the Goal's current-proposal linkage? | Not fixed. No persistence/audit in this slice. | (a) Clears `current_proposal_plan_id`/`current_proposal_plan_version` to `None`. (b) Retains them until superseded by the next proposal. | (a) simplest, matches "no audit trail in D1"; (b) preserves a reference nothing in this slice reads while in `SCOPING`. | (a) | `revise_goal_plan` field deltas (G) |
| DR-06 | **Superseded** (R1-02; reversed R2-02) | Does `ApprovedGoalPlan` reuse the same `GoalPlanId` as its source proposal, and what happens to its version? | R1-02's direction: "the same logical GoalPlan identity may be promoted from proposal to approved plan, with explicit version semantics." R2-02 is explicit and binding: approval must **not** increment plan version. | (a) Same `plan_id`; **same version, unchanged** — approval copies `plan_id` and `version` from the proposal verbatim (R2-02). (b) Same `plan_id`; version incremented by one on promotion (v1.1's rule — **rejected by R2-02**, since approval does not change plan content). (c) New `plan_id` minted at approval (not the R1/R2-recommended direction). | (a) matches R2-02's explicit "approval is a Goal lifecycle mutation, not a plan-content mutation" framing; (b) is explicitly rejected; (c) was never the recommended direction. | (a) | `ApprovedGoalPlan` shape (F), `approve_goal_plan` (G) |
| DR-07 | Unchanged (still open) | Does each `propose_goal_decomposition` call (including resubmission after revision) mint a fresh `plan_id`+version-`0`, or does one logical plan identity persist with an incrementing version across resubmissions? | R1-02 required this to be explicitly resolved. R2-02 confirms plan version never increments *within one proposal's lifetime*, which is orthogonal to whether a *resubmission* gets a fresh identity. | (a) Fresh `plan_id` and version `0` every proposal call — no cross-revision plan lineage; because plan version never increments (DR-06/R2-02), every `GoalDecompositionProposal` in this slice is created, and remains, at version `0` for its entire existence. (b) One stable `plan_id` persists across revision rounds. | (a) is simpler, no lineage bookkeeping, and is now the *only* option under which "version" is ever anything but a vestigial `0` in this slice; (b) preserves one identity across a plan's edit history but was never explicitly mandated for the proposal stage. | (a) | `propose_goal_decomposition` (G), `GoalPlan` version rules (H) |
| DR-08 | **Superseded** (R1-07; scope extended R2-04) | Plain `ValueError` or a narrow named error taxonomy? | R1-07: the D1.3 "no custom exception" test freezes the D1.3 primitive surface, not a permanent ban. R2-04 requires the taxonomy to also cover identity/result-shape/state-table violations, without adding a fifth class. | (a) Four narrow exception classes (`GoalVersionConflictError`, `IllegalGoalTransitionError`, `ActorNotPermittedError`, `InvalidStructuralInputError`), each subclassing `ValueError` directly, defined in `errors.py`. `InvalidStructuralInputError` now also covers: Goal/command identity mismatches (R2-03), Subgoal↔entries set-mismatches (R2-03), out-of-scope `GoalState` construction (R2-04), and negative versions on any of `Goal`/`Subgoal`/`GoalDecompositionProposal`/`ApprovedGoalPlan`/`GoalTransitionRecord` (R2-04). (b) A fifth, narrower exception class per new category (rejected — R2 does not request this, and it would grow the public surface beyond what any accepted source requires). | (a) reuses the same four classes for every new invariant R2 adds, keeping the taxonomy stable; (b) would multiply exception classes without new distinguishing value for this slice's callers. | (a) | Every mutation's/constructor's failure path (H, N), `test_domain_boundaries.py` scope (L) |
| DR-09 | **Superseded** (R2-04; completed R3-02) | Exact mutation-result shape and value invariants? | R2-04: a single result type permitted inconsistent optional-payload combinations; R3-02 completes direct-construction invariants without expanding the public surface. | (a) Three distinct frozen result types: `GoalTransitionResult(goal, transition)` for `create_goal`/`begin_scoping`/`revise_goal_plan`, rejecting a Goal state that requires proposal/approved-plan payload; `GoalProposalResult(goal, transition, proposal)` only for `AWAITING_PLAN_APPROVAL`, with proposal Goal/plan ID/version linkage checks; `GoalApprovalResult(goal, transition, approved_plan)` only for `DELIBERATING`, with approved-plan Goal/plan ID/version linkage checks. All retain the transition Goal ID/version/next-state checks and raise `InvalidStructuralInputError` on every violation. (b) v1.1's single `GoalMutationResult(goal, transition, proposal=None, approved_plan=None)` (**superseded by R2-04**). | (a) makes wrong payload presence structurally impossible and wrong payload/Goal linkage directly unconstructable; (b) required exhaustive conditional validation. | (a) | Every mutation's return type (F, G) |
| DR-10 | Unchanged | One command dataclass per mutation, or plain keyword arguments? | Issue #23 explicitly asks for "command or mutation-intent types"; contracts already uses this pattern. Applies only to the four *Goal* mutations — Subgoal creation is explicitly **not** command-driven (R2-01). | (a) One frozen dataclass per Goal mutation (carrying `event_id`/`occurred_at` per R1-03). (b) Plain parameters. | (a) symmetric with contracts, testable in isolation; (b) less boilerplate. | (a) | `commands.py` (F, L) |
| DR-11 | **Refined reasoning** (R1-07) | Does `create_goal` carry `expected_version`? | R1-07: creation must be explicitly framed as a **factory operation**, not a mutation command over an existing aggregate. R2-01 additionally confirms `create_subgoal` is not even a command at all, so this question now applies only to `create_goal`. | (a) `create_goal` is a factory, structurally outside the "every mutating command carries `expected_version`" rule because there is no pre-existing `Goal` instance to compare against; the rule applies only to the four Goal mutation commands over an *existing* `Goal`. (b) A sentinel `expected_version` on creation (rejected — no non-arbitrary sentinel exists). | (a) is the only option that does not require an artificial sentinel value. | (a) | `CreateGoalCommand` shape (F) |
| DR-12 | **Refined** (R2-03) | Validation-check ordering inside each mutation? | Not fixed by any source; R2-03 adds a new identity-guard requirement that must be placed somewhere in this order. | (a) actor-authority guard → **Goal-identity guard** (`command.goal_id == goal.goal_id`; for `approve_goal_plan`, also `proposal.goal_id == goal.goal_id`) → `expected_version` comparison → transition-legality (source-state) check → payload/structural invariants (including the Subgoal↔entries set-equality check and, for `approve_goal_plan`, the `proposal.plan_id`/`version` linkage-consistency check). (b) Any other ordering. | (a) never reveals version-conflict detail to an unauthorized or misdirected caller and defers the most expensive checks last; inserting the identity guard right after authority (rather than reordering the whole sequence) keeps the v1.1 ordering otherwise stable. | (a) | Every mutation's control flow (H) |
| DR-13 | Unchanged (R1-03) | Are `event_id`/`occurred_at`/every ID caller-supplied, or partly generated internally? | R1-03 is explicit and binding: no `uuid4()`, `datetime.now()`, or hidden clock/ID source inside domain mutations. R2-01 additionally removes the *only* place v1.1 had internal generation (`event_id` was already caller-supplied in v1.1; `create_subgoal` never had a clock/ID concern since it never emitted a transition). | (a) Fully caller-supplied: `GoalId`, `GoalPlanId`, every `SubgoalId`, `TransitionEventId`, and `occurred_at` are all required fields on the relevant Goal command, never generated inside a mutation function; `create_subgoal`'s parameters (`subgoal_id`, `goal_id`, `statement`, `definition_of_done`) are likewise all caller-supplied. (b) Any internal generation (rejected). | (a) is the only option R1-03/R2-01 permit. | (a) | Every command/factory shape (F), every mutation signature (G) |
| DR-14 | Unchanged (R1-01) | Does the independent `Subgoal` entity carry `acceptance_status`? | R1-01 explicitly lists `acceptance_status` among the minimum required fields. | (a) Include it, initialized to `NOT_ACCEPTED` by `create_subgoal`. (b) Omit it (contradicts R1-01). | (a) is required. | (a) | `Subgoal` shape (F) |
| DR-15 | Unchanged (R1-06) | Where does required/optional Subgoal membership live? | R1-06: compare `Subgoal.required`, plan-level `required_subgoal_ids`, and "all required, optionality deferred"; explicitly warns against approving a field "merely to avoid a possible future breaking change." | (a) No required/optional concept in D1.4 at all — every Subgoal referenced by an approved plan is implicitly required; deferred entirely to the batch implementing the `CROSS_GOAL_REVIEW` guard. (b) `PlanSubgoalEntry.required: bool`. (c) `GoalDecompositionProposal.required_subgoal_ids: frozenset[SubgoalId]`. | (a) avoids the anti-pattern R1-06 warns against; (b)/(c) both front-load an unconsumed distinction. | (a) | `PlanSubgoalEntry`/`GoalDecompositionProposal` shape (F, I) |
| DR-16 | Unchanged (R1-06) | Must dependency edges be tuple-position-constrained, or a proper acyclic graph independent of display order? | R1-06 explicitly rejects tuple-position-based ordering; requires acyclicity independent of display/tuple position. Unaffected by R2-05's separate field-type correction. | (a) Dependency edges are validated as a proper directed graph via cycle detection (Kahn's-algorithm-style topological-sort attempt) **independent of `entries` tuple position**; tuple position remains only the *display* order. (b) v1.0's "must appear earlier in the tuple" rule (rejected). | (a) correctly separates the two concepts R1-06 names. | (a) | `_validate_plan_entries` (F, I) |
| DR-16a | **Superseded** (R1-06; corrected R2-05) | Duplicate-edge, dangling-reference, self-edge behavior — and how is a duplicate edge *represented* in the first place? | R1-06 requires these to be defined. R2-05: v1.1's `frozenset[SubgoalId]` field silently deduplicates *before* `__post_init__` runs, so a duplicate edge can never be observed or rejected — the field type itself must change. | (a) `PlanSubgoalEntry.depends_on: tuple[SubgoalId, ...]` (not `frozenset`), so duplicate entries survive into `__post_init__`/`_validate_plan_entries` and can be explicitly rejected (`InvalidStructuralInputError`) rather than silently normalized away; dangling references (a `depends_on` entry not present among `entries`) and self-edges (`entry.subgoal_id in entry.depends_on`) are rejected the same way; order within `depends_on` remains non-semantic (R2-05: "keep dependency order non-semantic"). (b) Keep `frozenset` and treat duplicate edges as normalized-not-rejected (**rejected by R2-05**, since R1 already required duplicates to be rejectable). | (a) is the only option under which a duplicate edge is even representable, let alone rejectable, satisfying both R1-06 and R2-05; (b) was already shown by R2-05 to be factually incapable of the R1-required behavior. | (a) | `PlanSubgoalEntry`/`_validate_plan_entries` (F, I), tests (N) |
| DR-16b | Unchanged (R1-06) | May a valid plan contain zero Subgoal entries? | R1-06 explicitly raises this ("when the initial Goal does not require decomposition"). | (a) Yes — `entries: tuple[PlanSubgoalEntry, ...] = ()` is valid. (b) No — at least one entry is required. | (a) matches R1-06's framing of a legitimate "no decomposition needed" case. | (a) | `GoalDecompositionProposal`/`ApprovedGoalPlan` construction (F, I) |
| DR-17 | Unchanged (R1-02) | Does Goal store the full `ApprovedGoalPlan` object, or only its ID+version? | R1-02: "reconsider storing the entire approved object inside Goal... recommended default is an ID/version linkage." Unaffected by R2-02 (which changes the *value* of the version stored, not whether it is stored by reference). | (a) `Goal.approved_goal_plan_id: GoalPlanId | None` + `Goal.approved_goal_plan_version: AggregateVersion | None` (ID/version linkage only). (b) v1.0's full-object embedding (rejected). | (a) matches R1-02's recommended default and the existing ID-only `GoalResponse` boundary. | (a) | `Goal` shape (F), aggregate/ownership model (E) |
| DR-17a | Unchanged (derived from DR-17) | Does Goal need an analogous *current-proposal* ID/version linkage pair while in `SCOPING`/`AWAITING_PLAN_APPROVAL`? | Structurally necessary once Goal no longer embeds the proposal object. | (a) `Goal.current_proposal_plan_id: GoalPlanId | None` + `Goal.current_proposal_plan_version: AggregateVersion | None`, set by `propose_goal_decomposition`, read/cleared by `revise_goal_plan`/`approve_goal_plan`. | No real alternative once DR-17 is resolved. | (a) | `Goal` shape (F), transition matrix (G) |
| DR-17b | Unchanged (R1-05) | Does `approve_goal_plan` clear the current-proposal linkage once it produces the approved-plan linkage? | R1-05 explicitly asks this. Unaffected by R2-02 (the *value copied into* `approved_goal_plan_version` changes; whether `current_proposal_*` is cleared afterward does not). | (a) Yes — cleared to `None` once `approved_goal_plan_id`/`version` are set. (b) No — both linkage pairs remain populated simultaneously. | (a) avoids Goal simultaneously claiming a "pending" and an "approved" plan once approval has happened. | (a) | `approve_goal_plan` field deltas (G) |
| DR-18 | Unchanged (R1-10) | Is `libs/domain/README.md` updated? | R1-10: recommended because the existing text says domain logic arrives only in later batches, while D1.4 introduces it. | (a) Update it (default in Section L's frozen set). (b) Leave unchanged. | (a) keeps the README accurate. | (a) | Exact changed-file set (L) |
| DR-19 | Unchanged | One implementation commit? | Both R1's and R2's "Accepted" lists explicitly preserve this. | (a) One commit for the whole slice. (b) Multiple commits. | (a) matches the accepted direction and the D1.3 precedent. | (a) | Commit boundary (P) |
| DR-20 | **Removed** (R2-01) | Does `create_subgoal` require an actor-authority guard, and which actor? | R2-01 explicitly requires removing `CreateSubgoalCommand`, DR-20, and the `SYSTEM` creation-authority matrix row: Subgoal creation is "merely structural," not lifecycle behavior, so it has *no* actor-authority rule at all. | — (question no longer applies; `create_subgoal` has no actor parameter of any kind). | — | — (removed, not answered) | `create_subgoal` shape (F, G) — now has no actor guard by design, not by an unresolved choice |
| DR-21 | **Refined** (R2-01) | Are Subgoals created via a separate factory *before* `propose_goal_decomposition`, or minted inline within that same call? | R1-01 allows a proposal to "reference Subgoal IDs or immutable Subgoal definitions." R2-01 confirms the separate-factory direction but removes the command wrapper around it. | (a) Separate `create_subgoal(subgoal_id, goal_id, statement, definition_of_done) -> Subgoal` plain-function call per Subgoal (no command object, per R2-01), producing independently versioned `Subgoal` entities that are then referenced (by ID, cross-validated against the full objects) inside `ProposeGoalDecompositionCommand`. (b) `ProposeGoalDecompositionCommand` carries only `(statement, definition_of_done)` pairs and `propose_goal_decomposition` mints the `Subgoal` entities inline. | (a) treats Subgoal creation as its own first-class, independently testable operation while remaining a plain factory (not a mutation); (b) blurs Subgoal's independent creation into Goal's mutation function. | (a) | `subgoals.py`, `goal_mutations.py` (F, G), implementation sequence (M) |
| DR-22 | Unchanged (R1-02) | One unified `GoalPlan` type with a status field, or two distinct types sharing `plan_id`+version lineage? | R1-02 asked this to be "separately resolved." Unaffected by R2-02 (which changes what "sharing... version lineage" means — sharing the *same, unincremented* value — not whether the types remain distinct). | (a) Two distinct frozen dataclass types (`GoalDecompositionProposal`, `ApprovedGoalPlan`), sharing `plan_id` and — per R2-02 — the exact same, unincremented `version`. (b) One `GoalPlan` dataclass with a status field. | (a) preserves Issue #23's explicit separate naming and keeps "proposal immutability"/"approved-plan immutability" as literally distinct types. | (a) | `goal_plans.py` shape (F) |
| DR-23 | Unchanged (R1-08) | Do domain strings require length ≥ 1, or at least one non-whitespace character? | R1-08: Pydantic's `Field(min_length=1)` accepts whitespace-only strings; `.strip()`-based checking is stricter, not a mirror. | (a) At least one non-whitespace character after `.strip()` — documented as an intentional domain-side strengthening. (b) Length ≥ 1 only (contract-identical). | (a) rejects semantically meaningless input. | (a) — classified **newly proposed** | `Goal`/`Subgoal` `__post_init__` (J) |
| DR-24 | Unchanged (R1-08) | Do dataclass constructors perform generic `isinstance`-based runtime type-checking for every field? | R1-08 requires this policy stated explicitly. | (a) No generic `isinstance` checks; static typing/mypy is trusted for structural type correctness. Only the specific semantic invariants enumerated in this plan are checked at runtime — extended by R2-04 to also cover: out-of-scope `GoalState` construction, negative versions on every versioned type, and the new identity/set-equality/result-shape checks. (b) Full `isinstance` checking on every field. | (a) matches the D1.3 precedent and keeps the checked set to exactly what R1/R2 require. | (a) | `__post_init__` scope for every dataclass (J), test matrix (N) |
| DR-25 | Unchanged (R1-09) | Direct `model_validate(domain_object, strict=True)` pass-through, or explicit field-by-field mapping? | R1-09: domain and contract enum/`ActorRef` classes are independent types; strict-mode Pydantic validation of a foreign class is not guaranteed to succeed. | (a) Explicit mapping functions per type family. (b) v1.0's direct pass-through assumption (rejected). | (a) is verified against Pydantic's actual strict-mode behavior. | (a) | `test_domain_contract_compatibility.py` (K, N) |
| DR-26 | **New** (R2-03) | Exact scope and mechanics of the Goal/command identity guard? | R2-03 requires rejecting `command.goal_id != goal.goal_id` on every mutation over an existing `Goal`, and `proposal.goal_id != goal.goal_id` on approval specifically. | (a) Every one of the four Goal-mutation functions (`begin_scoping`, `propose_goal_decomposition`, `revise_goal_plan`, `approve_goal_plan`) compares `command.goal_id == goal.goal_id` as its first structural check (immediately after the actor guard, DR-12); `approve_goal_plan` additionally compares `proposal.goal_id == goal.goal_id`; any mismatch raises `InvalidStructuralInputError`. (b) Omit the check on the theory that a caller would never construct a mismatched command (rejected — R2-03 explicitly requires the rejection to exist and be tested). | (a) is the only option R2-03 permits; it also gives a single, uniform place (DR-12's ordering) for the check across all four mutations. | (a) | Every Goal mutation function (G, H), tests (N) |
| DR-27 | **New** (R2-03) | Exact set-relation required between `ProposeGoalDecompositionCommand.subgoals` and `.entries`? | R2-03's recommended rule: Subgoal IDs unique; every supplied Subgoal has `goal_id == goal.goal_id`; the set of supplied Subgoal IDs equals the set of entry Subgoal IDs exactly; no unreferenced supplied Subgoal and no entry without a supplied Subgoal. | (a) Exact set-equality: `{s.subgoal_id for s in command.subgoals} == {e.subgoal_id for e in command.entries}`, with no duplicates in either collection and every supplied `Subgoal.goal_id == goal.goal_id`; any violation raises `InvalidStructuralInputError`. (b) One-directional containment only (every entry must reference a supplied Subgoal, but "extra" unreferenced supplied Subgoals are tolerated) — a looser rule not requested by R2-03's recommended wording. | (a) matches R2-03's explicit recommended rule word-for-word and leaves no ambiguity about "unreferenced" Subgoals; (b) would silently tolerate caller mistakes R2-03's wording does not sanction. | (a) | `propose_goal_decomposition` (G, H), tests (N) |
| DR-28 | **New** (R4) | Is `create_subgoal` package-root exported? | R4 requires this policy to be explicit. `create_subgoal` is a public structural factory, while R2-01 preserves its non-command, non-lifecycle semantics. | (a) Root-export `create_subgoal`. (b) Leave it only at `mnemograph_domain.subgoals.create_subgoal`. | (a) keeps the public domain API consistent with the other planned public factories without changing behavior or scope; (b) leaves the public factory omitted from the package-root inventory. | (a) | `__init__.py` export set (F.10, L), boundary assertion (N) |

**Consolidated bundle:** Sections D (this table) and Q together form the
single decision bundle for one Lead-SA/human review pass; Section Q
additionally restates every row's classification (fixed / binding
correction / structurally derived / newly proposed) per R2-06. No newly
proposed public semantic in Sections E–N is treated as approved; every one
traces to a specific DR ID above and is blocked until that row is
resolved.

---

## E. Aggregate, entity, value-object, and ownership model (corrected)

Per R1-01/R1-02/R1-17, this slice now has **three** independently versioned
things instead of one:

| Name | Kind | Version? | Notes |
|---|---|---|---|
| `Goal` | Aggregate root | Yes, own `AggregateVersion` | Owns *linkage* (ID+version pairs) to a current proposal and an approved plan — never the embedded objects (DR-17) |
| `Subgoal` | Independently versioned entity (its own consistency unit) | Yes, own `AggregateVersion`, starting at `0` | Created via the plain `create_subgoal` structural factory (R2-01: no command, no actor guard, no `expected_version`, no event, no transition); acceptance/reopen mutation is deferred; **not owned by Goal's version** — referencing a Subgoal from a plan does not touch Goal's or the Subgoal's version |
| `GoalDecompositionProposal` / `ApprovedGoalPlan` | Two distinct, immutable snapshots sharing one logical plan identity (`plan_id`) and the *same, never-incremented* `version` (DR-06/R2-02, DR-22) | Yes, own `AggregateVersion`, fixed at creation and never mutated within this slice | Neither embeds full `Subgoal` objects — each holds only `PlanSubgoalEntry` records (`subgoal_id` + dependency metadata), keeping "plan-owned ordering/dependency metadata" (R1-01/R1-06) separate from "Subgoal-owned lifecycle state" |

**Entity vs. value-object boundary:** `Goal`, `Subgoal`,
`GoalDecompositionProposal`, `ApprovedGoalPlan`, `GoalTransitionRecord`, and
every command are frozen dataclasses. `PlanSubgoalEntry` is a frozen
value object (no independent identity of its own beyond the `subgoal_id`
it references). "Mutation" still means: a pure function takes the
current immutable value(s) plus a command and returns new immutable
value(s) — nothing is mutated in place, and (per R1-03) nothing is
generated internally that the caller did not supply.

**Goal's plan linkage (corrected per DR-17/DR-17a/DR-17b):**

```
Goal.current_proposal_plan_id:      GoalPlanId | None
Goal.current_proposal_plan_version: AggregateVersion | None
Goal.approved_goal_plan_id:         GoalPlanId | None
Goal.approved_goal_plan_version:    AggregateVersion | None
```

Goal never embeds the `GoalDecompositionProposal`/`ApprovedGoalPlan`
object. Mutation functions that need the actual proposal object (namely
`approve_goal_plan`) take it as an **explicit parameter**, supplied by the
caller (a future application/repository layer resolves and passes it in;
this remains entirely out of scope for domain persistence per
ADR-DOMAIN-001 D1-E).

**Subgoal ownership:** `Subgoal` is created independently via the plain
`create_subgoal` factory (R2-01: not a command-driven mutation — no actor,
no `expected_version`, no event, no transition), is never embedded by
value inside a proposal/plan, and is referenced only by `subgoal_id` from
`PlanSubgoalEntry`. This is the direct structural fix R1-01 requires,
further narrowed by R2-01: Subgoal's `version`/`acceptance_status`
lifecycle is not duplicated or shadowed anywhere in the plan/proposal
shapes, and its creation is not dressed up as lifecycle behavior it does
not yet have.

**Intentionally deferred (unchanged from v1.0):** DeliberationSession
attachment; Subgoal acceptance/reopen and its `SubgoalTransitionRecord`;
the "all required Subgoals accepted" `CROSS_GOAL_REVIEW` guard;
proposal-history/audit retention beyond the single current linkage;
persistence or a repository abstraction of any kind.

**Why no persistence abstraction is needed:** unchanged from v1.0 — every
function in this slice is a pure, in-memory transformation; nothing is
stored, queued, or externally resolved.

---

## F. Exact public and internal symbol inventory

All new modules live under `libs/domain/src/mnemograph_domain/`. Every
item is newly proposed unless marked otherwise; every item cites the DR
ID(s) it depends on.

### F.1 `identifiers.py` (existing — one addition, unchanged from v1.0)

| Symbol | Kind | Definition |
|---|---|---|
| `TransitionEventId` | `NewType` | `NewType("TransitionEventId", UUID)` |

### F.2 `datetimes.py` (new, unchanged from v1.0)

```python
def ensure_aware_utc(value: datetime) -> datetime: ...
```
Raises `ValueError` if `value.tzinfo is None or value.utcoffset() is None`.
Otherwise returns `value.astimezone(UTC)`.

### F.3 `errors.py` (new — DR-08)

```python
class GoalVersionConflictError(ValueError): ...
class IllegalGoalTransitionError(ValueError): ...
class ActorNotPermittedError(ValueError): ...
class InvalidStructuralInputError(ValueError): ...
```

No shared custom base class beyond `ValueError` itself (kept narrow, per
"narrow, standard-library-only mechanism").

### F.4 `subgoals.py` (new — DR-01, DR-14, DR-20, DR-21)

```python
@dataclass(frozen=True)
class Subgoal:
    subgoal_id: SubgoalId
    goal_id: GoalId
    version: AggregateVersion
    statement: str
    definition_of_done: str
    acceptance_status: SubgoalAcceptanceStatus

    def __post_init__(self) -> None: ...
        # raises InvalidStructuralInputError if statement/definition_of_done
        # have no non-whitespace character (DR-23); does not re-validate
        # acceptance_status against version (see Section J note)
```

```python
def create_subgoal(
    subgoal_id: SubgoalId,
    goal_id: GoalId,
    statement: str,
    definition_of_done: str,
) -> Subgoal: ...
```
A plain structural factory (R2-01): no command object, no `actor`
parameter, no actor-authority rule, no `expected_version`, no event
identifier, no timestamp, and it emits no transition record. Constructs
`Subgoal(subgoal_id=subgoal_id, goal_id=goal_id,
version=make_aggregate_version(0), statement=statement,
definition_of_done=definition_of_done,
acceptance_status=SubgoalAcceptanceStatus.NOT_ACCEPTED)`. `CreateSubgoalCommand`
is **removed** (R2-01) — it does not exist in Plan v1.5.

### F.5 `goal_plans.py` (new — DR-02, DR-06, DR-15, DR-16, DR-16a, DR-16b, DR-22)

```python
@dataclass(frozen=True)
class PlanSubgoalEntry:
    subgoal_id: SubgoalId
    depends_on: tuple[SubgoalId, ...]

    def __post_init__(self) -> None: ...
        # raises InvalidStructuralInputError on self-edge or on a duplicate
        # SubgoalId appearing more than once within depends_on (DR-16a,
        # corrected R2-05); depends_on is a tuple (not a frozenset) so that
        # a duplicate edge survives construction and can be rejected rather
        # than silently deduplicated; order within depends_on is non-semantic
```

No `required` field on `PlanSubgoalEntry` (DR-15, recommended option (a):
no required/optional concept in D1.4).

```python
@dataclass(frozen=True)
class GoalDecompositionProposal:
    plan_id: GoalPlanId
    goal_id: GoalId
    version: AggregateVersion
    entries: tuple[PlanSubgoalEntry, ...]

    def __post_init__(self) -> None: ...
        # delegates to _validate_plan_entries(self.entries) — DR-16/16a/16b
```

```python
@dataclass(frozen=True)
class ApprovedGoalPlan:
    plan_id: GoalPlanId
    goal_id: GoalId
    version: AggregateVersion
    entries: tuple[PlanSubgoalEntry, ...]

    def __post_init__(self) -> None: ...
        # same validation as GoalDecompositionProposal (defense-in-depth,
        # since this is always constructed from an already-validated proposal)
```

```python
def _validate_plan_entries(entries: tuple[PlanSubgoalEntry, ...]) -> None: ...
```
Internal (not exported). Raises `InvalidStructuralInputError` if: any
`subgoal_id` repeats across `entries` (DR-16a); any `depends_on` entry is
not a `subgoal_id` present among `entries` (dangling reference, DR-16a);
any `SubgoalId` repeats **within** a single entry's `depends_on` tuple
(duplicate edge, DR-16a/R2-05); the directed graph formed by
`entries`/`depends_on` contains a cycle, checked via a topological-sort
attempt (Kahn's algorithm: repeatedly remove entries with zero remaining
in-degree; if any entries remain after no more can be removed, a cycle
exists) that is **independent of `entries` tuple position** (DR-16). Does
**not** reject an empty `entries` tuple (DR-16b, recommended: zero-Subgoal
plans are valid).

### F.6 `goals.py` (new — DR-11, DR-17, DR-17a, DR-17b, DR-23)

```python
@dataclass(frozen=True)
class Goal:
    goal_id: GoalId
    statement: str
    state: GoalState
    version: AggregateVersion
    current_proposal_plan_id: GoalPlanId | None
    current_proposal_plan_version: AggregateVersion | None
    approved_goal_plan_id: GoalPlanId | None
    approved_goal_plan_version: AggregateVersion | None

    def __post_init__(self) -> None: ...
```
`__post_init__` raises `InvalidStructuralInputError` if: `statement` has no
non-whitespace character (DR-23); `version` is negative (defense-in-depth
re-check, since `AggregateVersion` itself cannot self-validate); or the
`state`/linkage combination is inconsistent per this exact table:

| `state` | `current_proposal_plan_id`/`version` | `approved_goal_plan_id`/`version` |
|---|---|---|
| `DRAFT` | must both be `None` | must both be `None` |
| `SCOPING` | must both be `None` | must both be `None` |
| `AWAITING_PLAN_APPROVAL` | must both be **set** | must both be `None` |
| `DELIBERATING` | must both be `None` (cleared per DR-17b) | must both be **set** |

### F.7 `commands.py` (new — DR-10, DR-11, DR-13)

```python
@dataclass(frozen=True)
class CreateGoalCommand:
    goal_id: GoalId
    statement: str
    actor: ActorRef
    event_id: TransitionEventId
    occurred_at: datetime

@dataclass(frozen=True)
class BeginScopingCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    event_id: TransitionEventId
    occurred_at: datetime

@dataclass(frozen=True)
class ProposeGoalDecompositionCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    plan_id: GoalPlanId
    subgoals: tuple[Subgoal, ...]
    entries: tuple[PlanSubgoalEntry, ...]
    event_id: TransitionEventId
    occurred_at: datetime

@dataclass(frozen=True)
class ReviseGoalPlanCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    event_id: TransitionEventId
    occurred_at: datetime

@dataclass(frozen=True)
class ApproveGoalPlanCommand:
    goal_id: GoalId
    actor: ActorRef
    expected_version: AggregateVersion
    event_id: TransitionEventId
    occurred_at: datetime
```

No command carries a `Literal["ACTION"]` discriminator (unchanged
reasoning from v1.0 — each is consumed by exactly one named function, no
discriminated union exists in this slice).

### F.8 `transitions.py` (new — DR-09)

```python
@dataclass(frozen=True)
class GoalTransitionRecord:
    event_id: TransitionEventId
    goal_id: GoalId
    version: AggregateVersion
    previous_state: GoalState | None
    next_state: GoalState
    actor: ActorRef
    occurred_at: datetime

    def __post_init__(self) -> None:
        if self.version < 0:
            raise InvalidStructuralInputError("GoalTransitionRecord.version must be non-negative")
        object.__setattr__(self, "occurred_at", ensure_aware_utc(self.occurred_at))
```
Normalizes (or raises on naive input) even when constructed directly,
satisfying R1-04's explicit requirement for this exact type; the added
non-negative `version` check satisfies R2-04.

**Result shapes (R2-04, superseding v1.1's single `GoalMutationResult`):**

```python
@dataclass(frozen=True)
class GoalTransitionResult:
    goal: Goal
    transition: GoalTransitionRecord

    def __post_init__(self) -> None: ...
        # raises InvalidStructuralInputError if transition.goal_id != goal.goal_id,
        # transition.version != goal.version, transition.next_state != goal.state,
        # or goal.state requires a current-proposal or approved-plan payload

@dataclass(frozen=True)
class GoalProposalResult:
    goal: Goal
    transition: GoalTransitionRecord
    proposal: GoalDecompositionProposal

    def __post_init__(self) -> None: ...
        # same transition cross-checks as GoalTransitionResult; also raises
        # InvalidStructuralInputError unless goal.state is
        # AWAITING_PLAN_APPROVAL, proposal.goal_id == goal.goal_id, and
        # proposal.plan_id/version match goal.current_proposal_plan_id/version

@dataclass(frozen=True)
class GoalApprovalResult:
    goal: Goal
    transition: GoalTransitionRecord
    approved_plan: ApprovedGoalPlan

    def __post_init__(self) -> None: ...
        # same transition cross-checks as GoalTransitionResult; also raises
        # InvalidStructuralInputError unless goal.state is DELIBERATING,
        # approved_plan.goal_id == goal.goal_id, and approved_plan.plan_id/
        # version match goal.approved_goal_plan_id/version
```
Each type's very *shape* makes an invalid payload combination
unrepresentable — there is no field to hold a `proposal` on
`GoalTransitionResult`, for example — while the minimal `__post_init__`
cross-check still catches internally inconsistent *values* (e.g., a
`transition.version` that does not match `goal.version`), which the type
system alone cannot prevent. In addition, `GoalTransitionResult` rejects a
resulting `Goal` in any state that requires a proposal or approved-plan
payload (`AWAITING_PLAN_APPROVAL` or `DELIBERATING`); `GoalProposalResult`
requires `AWAITING_PLAN_APPROVAL` and exact proposal-to-Goal ID/version
linkage; and `GoalApprovalResult` requires `DELIBERATING` and exact
approved-plan-to-Goal ID/version linkage. Every result invariant, including
the existing transition consistency checks, raises
`InvalidStructuralInputError`. `GoalMutationResult` is **removed** — it
does not exist in Plan v1.5.

### F.9 `goal_mutations.py` (new — the five Goal mutation functions)

```python
def create_goal(command: CreateGoalCommand) -> GoalTransitionResult: ...

def begin_scoping(goal: Goal, command: BeginScopingCommand) -> GoalTransitionResult: ...

def propose_goal_decomposition(
    goal: Goal,
    command: ProposeGoalDecompositionCommand,
) -> GoalProposalResult: ...

def revise_goal_plan(goal: Goal, command: ReviseGoalPlanCommand) -> GoalTransitionResult: ...

def approve_goal_plan(
    goal: Goal,
    proposal: GoalDecompositionProposal,
    command: ApproveGoalPlanCommand,
) -> GoalApprovalResult: ...
```

Every Goal-mutation function (all except `create_goal`) validates, in
order (DR-12/DR-26): actor-authority guard; `command.goal_id ==
goal.goal_id` (DR-26); `expected_version` comparison; transition-legality
check; payload/structural invariants. `propose_goal_decomposition`
additionally validates the Subgoal↔entries set-equality rule (DR-27):
every supplied `Subgoal.goal_id == goal.goal_id`, no duplicate IDs in
either `command.subgoals` or `command.entries`, and
`{s.subgoal_id for s in command.subgoals} == {e.subgoal_id for e in
command.entries}` exactly. `approve_goal_plan` takes the current
`GoalDecompositionProposal` as an explicit parameter (Goal itself only
carries its ID/version linkage, per DR-17), and additionally verifies
`proposal.goal_id == goal.goal_id` (DR-26) and `proposal.plan_id ==
goal.current_proposal_plan_id and proposal.version ==
goal.current_proposal_plan_version` (unchanged linkage check), raising
`InvalidStructuralInputError` on any mismatch. `approve_goal_plan` copies
`proposal.version` **unchanged** into `approved_goal_plan_version` and
into `ApprovedGoalPlan.version` (DR-06/R2-02) — it never computes
`proposal.version + 1`.

### F.10 `__init__.py` (existing — modified)

New exports added to the existing 16 Delivery D1.3 symbols (none removed):

```
TransitionEventId
GoalVersionConflictError
IllegalGoalTransitionError
ActorNotPermittedError
InvalidStructuralInputError
Subgoal
PlanSubgoalEntry
GoalDecompositionProposal
ApprovedGoalPlan
Goal
CreateGoalCommand
BeginScopingCommand
ProposeGoalDecompositionCommand
ReviseGoalPlanCommand
ApproveGoalPlanCommand
GoalTransitionRecord
GoalTransitionResult
GoalProposalResult
GoalApprovalResult
create_goal
create_subgoal
begin_scoping
propose_goal_decomposition
revise_goal_plan
approve_goal_plan
ensure_aware_utc
```

That is 26 new symbols added to the existing 16, for a package-root
`__all__` of exactly **42** symbols after this batch. `create_subgoal` is a
root export as well as a public module-level structural factory at
`mnemograph_domain.subgoals` (DR-28/R4). (`CreateSubgoalCommand` and
`GoalMutationResult` from v1.1 are removed; `GoalTransitionResult`,
`GoalProposalResult`, and `GoalApprovalResult` replace them.)
`_validate_plan_entries` is **not** exported.

---

## G. Complete function/command signatures, transition matrix, and authority matrix

### G.1 State-transition matrix with exact aggregate-field deltas

Atomicity is proven per R1-04's corrected framing: **in terms of
observable state and returned/emitted values**, not in terms of "no
temporary object is ever constructed." Specifically: on any rejected call,
(1) the `Goal`/plan value(s) passed in by the caller are returned
unchanged by reference (this function never returns a mutated view of
them — Python's immutability of frozen dataclasses guarantees the
caller's original objects are never altered), and (2) the function raises
one of the four named exceptions and returns nothing — no
`GoalTransitionResult`/`GoalProposalResult`/`GoalApprovalResult`, and
therefore no `GoalTransitionRecord`, is ever returned to the caller on a
rejected call.

`create_subgoal` is not part of this Goal transition matrix at all (R2-01):
it is a plain structural factory with no actor guard, no `expected_version`,
and no transition emission. Its only rejection condition is a
whitespace-only `statement`/`definition_of_done`, which raises
`InvalidStructuralInputError`.

| Operation | Source state | Result state | Actor | `expected_version` | Field deltas (before → after) | Transition emitted | Rejection → exception | Source/DR |
|---|---|---|---|---|---|---|---|---|
| `create_goal` | *(none)* | `DRAFT` | `USER` | N/A — factory (DR-11) | `version`: n/a → `0`; `current_proposal_*`/`approved_goal_plan_*`: n/a → all `None` | `previous_state=None, next_state=DRAFT, version=0` | non-`USER` actor → `ActorNotPermittedError`; empty/whitespace-only `statement` → `InvalidStructuralInputError` | Charter §8.1; DR-11, DR-23 |
| `begin_scoping` | `DRAFT` | `SCOPING` | `SYSTEM` (DR-03) | must equal `goal.version` (`0`) | `version`: `0` → `1`; linkage fields unchanged (`None`/`None`) | `previous_state=DRAFT, next_state=SCOPING, version=1` | wrong actor → `ActorNotPermittedError`; `command.goal_id != goal.goal_id` → `InvalidStructuralInputError` (DR-26); stale version → `GoalVersionConflictError`; `goal.state != DRAFT` → `IllegalGoalTransitionError` | System Design §5.2; DR-03, DR-12, DR-26 |
| `propose_goal_decomposition` | `SCOPING` | `AWAITING_PLAN_APPROVAL` | `SYSTEM` (DR-04) | must equal `goal.version` | `version`: `+1`; `current_proposal_plan_id`: `None` → `command.plan_id`; `current_proposal_plan_version`: `None` → `0` (fresh proposal, DR-07 option (a); plan version never increments — R2-02) | `previous_state=SCOPING, next_state=AWAITING_PLAN_APPROVAL` | wrong actor → `ActorNotPermittedError`; `command.goal_id != goal.goal_id` → `InvalidStructuralInputError` (DR-26); stale version → `GoalVersionConflictError`; `goal.state != SCOPING` → `IllegalGoalTransitionError`; Subgoal↔entries set-mismatch, any supplied `Subgoal.goal_id != goal.goal_id`, or `_validate_plan_entries` failure → `InvalidStructuralInputError` (DR-27) | Charter §8.1 step 4; DR-02, DR-04, DR-07, DR-12, DR-16, DR-16a, DR-16b, DR-21, DR-26, DR-27 |
| `revise_goal_plan` | `AWAITING_PLAN_APPROVAL` | `SCOPING` | `USER` (fixed) | must equal `goal.version` | `version`: `+1`; `current_proposal_plan_id`/`version`: set → `None` (DR-05, cleared) | `previous_state=AWAITING_PLAN_APPROVAL, next_state=SCOPING` | wrong actor → `ActorNotPermittedError`; `command.goal_id != goal.goal_id` → `InvalidStructuralInputError` (DR-26); stale version → `GoalVersionConflictError`; `goal.state != AWAITING_PLAN_APPROVAL` → `IllegalGoalTransitionError` | System Design §5.2 "User revises"; fixed; DR-05, DR-12, DR-26 |
| `approve_goal_plan` | `AWAITING_PLAN_APPROVAL` | `DELIBERATING` | `USER` (fixed) | must equal `goal.version` | `version`: `+1`; `current_proposal_plan_id`/`version`: set → `None` (DR-17b); `approved_goal_plan_id`: `None` → `proposal.plan_id`; `approved_goal_plan_version`: `None` → `proposal.version` **unchanged, not incremented** (DR-06/DR-22, R2-02) | `previous_state=AWAITING_PLAN_APPROVAL, next_state=DELIBERATING` | wrong actor → `ActorNotPermittedError`; `command.goal_id != goal.goal_id` or `proposal.goal_id != goal.goal_id` → `InvalidStructuralInputError` (DR-26); stale version → `GoalVersionConflictError`; `goal.state != AWAITING_PLAN_APPROVAL` → `IllegalGoalTransitionError`; `proposal.plan_id`/`version` mismatch against `goal.current_proposal_plan_id`/`version` → `InvalidStructuralInputError` | System Design §5.2 "User approves"; ADR-DOMAIN-001 D1-E stop boundary; DR-06, DR-12, DR-17b, DR-22, DR-26 |

No row exists for any transition beyond `DELIBERATING`, and none is
authorized.

### G.2 Authority matrix

| Concept | Meaning | Must not be confused with |
|---|---|---|
| Human normative authority | `USER`'s exclusive right to revise/approve the plan | Any other kind's ability to issue a mutation |
| Actor attribution | The `actor: ActorRef` on a command/transition | Authentication or "content authorship" |
| Authentication | Verifying a real human is behind a `USER` command | Out of scope entirely |
| Orchestration policy | `SYSTEM`-attributed mutations for `begin_scoping`/`propose_goal_decomposition` | Human authority — `SYSTEM` never approves/revises |
| Content authorship | Scientist/SA producing proposal *content* (out of this slice) | The mutation issuer that attaches records (`SYSTEM`) |
| Structural (non-lifecycle) creation | `create_subgoal`'s plain factory call, with no actor of any kind (R2-01) | A mutation, which by definition carries actor attribution |

| Mutation | `USER` | `SYSTEM` | `SCIENTIST` | `SA` | Why |
|---|---|---|---|---|---|
| `create_goal` | Allowed | Rejected | Rejected | Rejected | Charter frames goal submission as user-originated |
| `begin_scoping` | Rejected (DR-03) | Allowed (DR-03) | Rejected | Rejected | R1/R2-accepted orchestration attribution |
| `propose_goal_decomposition` | Rejected (DR-04) | Allowed (DR-04) | Rejected | Rejected | R1/R2-accepted orchestration attribution |
| `revise_goal_plan` | Allowed | Rejected | Rejected | Rejected | System Design §5.2 "User revises" |
| `approve_goal_plan` | Allowed | Rejected | Rejected | Rejected | System Design §5.2 "User approves" |

`create_subgoal` has **no row** in this table (R2-01): it takes no
`actor` parameter at all and is not gated by any `ActorKind`. `MODERATOR`
is not introduced as an `ActorKind` anywhere in this plan. `SCIENTIST`/`SA`
never issue a mutation in this slice.

---

## H. Version, creation, ID/time, and failure semantics

| Concept | Definition |
|---|---|
| Creation version | `AggregateVersion(0)` for both `create_goal` and `create_subgoal` |
| Creation vs. `expected_version` rule (R1-07 corrected reasoning) | `create_goal` is a **factory**, not a mutation command over an existing aggregate; ADR-DOMAIN-001 D1-D's "every mutating command carries `expected_version`" applies only to the four Goal-mutation commands operating on an *existing* `Goal`. `create_subgoal` is not even a command (R2-01), so this question does not apply to it at all. |
| `expected_version` comparison | Exact equality (`!=` rejected, not `<`/`>`) against `goal.version` |
| Identity guard (R2-03/DR-26) | Every Goal-mutation function rejects `command.goal_id != goal.goal_id`; `approve_goal_plan` additionally rejects `proposal.goal_id != goal.goal_id` — checked immediately after the actor-authority guard, before the `expected_version` comparison |
| Successful version increment | Exactly `+1` per successful Goal mutation (never `0`, never `+2`). A `GoalDecompositionProposal`'s or `ApprovedGoalPlan`'s own `version` is **never** incremented anywhere in this slice (R2-02): it is fixed at `0` when the proposal is created and copied unchanged into the approved plan. |
| Version-conflict rejection | `GoalVersionConflictError` (DR-08); no new `Goal`/transition/plan value is constructed |
| Illegal-transition rejection | `IllegalGoalTransitionError` (DR-08); same non-construction guarantee |
| Actor-authority rejection | `ActorNotPermittedError` (DR-08) |
| Structural/plan rejection | `InvalidStructuralInputError` (DR-08) — covers empty/whitespace statements, plan-graph violations, proposal-linkage mismatches, Goal/command identity mismatches (DR-26), Subgoal↔entries set-mismatches (DR-27), out-of-scope `GoalState` construction, and negative versions on any versioned type (R2-04) |
| Ordering of validation checks | actor-authority guard → Goal-identity guard (DR-26) → `expected_version` comparison → transition-legality check → payload/structural invariants (→ proposal-identity/linkage-consistency check, `approve_goal_plan` only) — DR-12 |
| Whether failures emit anything | No — a rejected call raises and returns nothing |
| Mutation result structure | `GoalTransitionResult`, `GoalProposalResult`, or `GoalApprovalResult`, one per mutation kind (DR-09, superseding v1.1's single `GoalMutationResult`) |
| Transition-event identifier | `TransitionEventId`, **caller-supplied** via `command.event_id` (DR-13) — never generated inside a mutation function |
| `occurred_at` | **Caller-supplied** `datetime` via `command.occurred_at` (DR-13); passed through `ensure_aware_utc` inside `GoalTransitionRecord.__post_init__` |
| Determinism (R1-03/R2-01) | No mutation function in this slice calls `uuid4()`, `datetime.now()`, or any other clock/ID source; every `GoalId`, `GoalPlanId`, `SubgoalId`, `TransitionEventId`, and `occurred_at` value enters the domain exclusively through a command field (or, for `create_subgoal`, a plain parameter) |

**Proof that each successful mutation increments Goal version exactly
once:** each Goal mutation function computes
`new_version = AggregateVersion(goal.version + 1)` in exactly one place,
used for both the returned `Goal.version` and the `GoalTransitionRecord.version`,
and that computation is reached only after every guard above has passed.

---

## I. GoalPlan/Subgoal order, dependency, required-membership, and structural invariants

| Invariant | Classification | Where enforced |
|---|---|---|
| Goal ID linkage (`GoalDecompositionProposal.goal_id`/`ApprovedGoalPlan.goal_id` equals the owning `Goal.goal_id`; `Subgoal.goal_id` equals the same) | Structurally derived; enforced by `goal_mutations.py` (DR-26/DR-27), not by the dataclasses' own `__post_init__` | `propose_goal_decomposition`, `approve_goal_plan` |
| Command/Goal identity guard | Newly proposed (DR-26, R2-03): every Goal-mutation command's `goal_id` must equal the `Goal` it is applied to; approval additionally requires `proposal.goal_id == goal.goal_id` | Every Goal-mutation function |
| Subgoal↔entries set-equality | Newly proposed (DR-27, R2-03): the set of `command.subgoals` IDs must equal the set of `command.entries` IDs exactly, with every supplied Subgoal's `goal_id` matching | `propose_goal_decomposition` |
| Plan identity/version lineage (`plan_id` reused across proposal→approval; **version copied unchanged**, never incremented) | Newly proposed (DR-06/R2-02, DR-22) | `approve_goal_plan` |
| Subgoal ID uniqueness within one proposal's `entries` | Newly proposed | `_validate_plan_entries` (DR-16a) |
| Display order vs. dependency graph (R1-06 separation) | Newly proposed (DR-16) | `entries` tuple position = display order; `depends_on` graph = dependency validity, checked independent of position |
| Duplicate dependency edge within one entry's `depends_on` | Newly proposed (DR-16a, corrected R2-05): representable and rejectable because `depends_on` is a `tuple`, not a `frozenset` | `PlanSubgoalEntry.__post_init__`/`_validate_plan_entries` |
| Required vs. optional Subgoal membership | Newly proposed (DR-15) — **not modeled in D1.4** (recommended option (a): all referenced Subgoals implicitly required; the distinction is deferred) | N/A in this slice |
| Dependency membership | Newly proposed — every `depends_on` entry must be a `subgoal_id` present among the same `entries` | `_validate_plan_entries` (DR-16a) |
| Self-dependencies | Newly proposed | `PlanSubgoalEntry.__post_init__` (DR-16a) |
| Cycles | Newly proposed (DR-16) — precluded via topological-sort-style graph validation, independent of tuple position | `_validate_plan_entries` |
| Zero-Subgoal plans | Newly proposed (DR-16b, recommended: valid) | `_validate_plan_entries` permits an empty `entries` tuple |
| Non-empty Goal statement | Newly proposed as "non-whitespace," not merely non-empty (DR-23) | `Goal.__post_init__` |
| Non-empty Subgoal statement/Definition of Done | Same correction (DR-23) | `Subgoal.__post_init__` |
| Out-of-scope `GoalState` construction rejected | Newly proposed (R2-04): a `Goal` may only be constructed in `DRAFT`, `SCOPING`, `AWAITING_PLAN_APPROVAL`, or `DELIBERATING`; any other `GoalState` member (`AWAITING_USER`, `PAUSED`, `CROSS_GOAL_REVIEW`, `FINAL_CANDIDATE`, `STOPPED`) is rejected outright | `Goal.__post_init__` |
| Negative version on any versioned type | Newly proposed (R2-04): re-checked in `__post_init__` for `Goal`, `Subgoal`, `GoalDecompositionProposal`, `ApprovedGoalPlan`, and `GoalTransitionRecord` | Each type's own `__post_init__` |
| Result-type internal consistency | Binding correction (R2-04/R3-02): transition Goal ID/version/next-state equality; transition-only result rejects payload-requiring states; proposal/approval result state and Goal-plan linkage equality | `GoalTransitionResult`/`GoalProposalResult`/`GoalApprovalResult.__post_init__`, all violations `InvalidStructuralInputError` |
| Proposal/approved-plan immutability | Structurally derived (frozen dataclasses) | `GoalDecompositionProposal`, `ApprovedGoalPlan` |
| Proposal-to-approved-plan relationship | Newly proposed (DR-06, R2-02): `ApprovedGoalPlan` is produced from the *current* proposal's `plan_id`/`entries`/`version`, with `version` copied **unchanged** | `approve_goal_plan` |
| Independent Subgoal version at creation | Newly proposed (DR-01): starts at `0`, `NOT_ACCEPTED`, via the plain `create_subgoal` factory (R2-01) | `create_subgoal` |
| Existence checks against externally stored entities | **Out of scope** — ADR-DOMAIN-001 D1-E reserves this for a future application/repository boundary; this slice can only check that a referenced `subgoal_id` is present among the `Subgoal` objects and `PlanSubgoalEntry` records supplied together in the *same* `ProposeGoalDecompositionCommand` call | Not implemented beyond that local cross-check |

---

## J. Construction and runtime-validation policy (DR-24, R1-04, R1-08)

**Non-bypassability strategy (R1-04):** every dataclass that carries a
value whose invariant this slice's mutation logic relies on performs that
check in its own `__post_init__`, **regardless of how the instance is
constructed** — directly, or via a factory/mutation function — because
`__post_init__` always runs on every construction path in Python. This is
the chosen mechanism (over "internal constructor + public factory," which
Python cannot enforce without a metaclass or module-private convention
that would still be bypassable by direct class access, and over any
generic validation framework, which is explicitly excluded).

**What is validated in `__post_init__`, exactly:**

| Type | Checked in `__post_init__` | Not checked (relies on static typing only) |
|---|---|---|
| `Goal` | `statement` non-whitespace (DR-23); `version` non-negative; `state` is one of the 4 in-scope `GoalState` members, rejecting the other 5 out-of-scope members outright (R2-04); `state`/linkage-field consistency (F.6 table) | — |
| `Subgoal` | `statement`/`definition_of_done` non-whitespace; `version` non-negative | That `acceptance_status` is consistent with `version` (see note below) |
| `PlanSubgoalEntry` | no self-edge; no duplicate `SubgoalId` within `depends_on` (R2-05) | Cross-entry checks (duplicate-across-entries/dangling/cycle) — those require the *whole* `entries` collection and are checked once by `_validate_plan_entries`, not per-entry |
| `GoalDecompositionProposal`/`ApprovedGoalPlan` | delegates to `_validate_plan_entries`; `version` non-negative (R2-04) | — |
| `GoalTransitionRecord` | naive-datetime rejection; UTC normalization (via `object.__setattr__`); `version` non-negative (R2-04) | — |
| `GoalTransitionResult`/`GoalProposalResult`/`GoalApprovalResult` | `transition.goal_id == goal.goal_id`; `transition.version == goal.version`; `transition.next_state == goal.state`; `GoalTransitionResult` rejects `AWAITING_PLAN_APPROVAL`/`DELIBERATING`; `GoalProposalResult` requires `AWAITING_PLAN_APPROVAL`, `proposal.goal_id == goal.goal_id`, and exact `current_proposal_plan_id`/`version` linkage; `GoalApprovalResult` requires `DELIBERATING`, `approved_plan.goal_id == goal.goal_id`, and exact `approved_goal_plan_id`/`version` linkage (R3-02) | — |
| Every command; `create_subgoal`'s plain parameters | none beyond dataclass/parameter typing | Field/parameter values are trusted as supplied |

**Explicit non-enforcement note:** `Subgoal.__post_init__` does **not**
assert that `acceptance_status == NOT_ACCEPTED` implies `version == 0`, or
vice versa. Reasoning: no mutation function in this slice ever reads or
relies on that relationship (acceptance mutation is deferred entirely), so
enforcing it now would encode acceptance-transition rules prematurely,
adjacent to the explicitly out-of-scope "acceptance-status mutation."
This is called out explicitly rather than silently omitted.

**`AggregateVersion` residual gap:** `AggregateVersion` remains a
`NewType` (Delivery D1.3, unchanged) and therefore cannot self-validate —
calling `AggregateVersion(-1)` directly still produces a value with no
runtime check. This gap is closed **one layer up**: every dataclass field
typed `AggregateVersion` (`Goal.version`, `Subgoal.version`,
`GoalDecompositionProposal.version`, `ApprovedGoalPlan.version`, and —
added per R2-04 — `GoalTransitionRecord.version`) re-validates
non-negativity in its owning dataclass's `__post_init__`, so a
`Goal`/`Subgoal`/plan/transition constructed with a negative version —
however that negative value was produced — is rejected at the point where
it would first become observable as domain state.

**Whitespace policy (DR-23):** domain strings require at least one
non-whitespace character (`.strip()` non-empty), which is **stricter**
than the existing contract's `Field(min_length=1)` (which accepts
whitespace-only strings). This is documented as an intentional domain-side
strengthening, not a semantic mirror.

**Generic type-checking policy (DR-24):** no `isinstance`-based runtime
type-checking is added for any field; static typing (`mypy --strict`) is
trusted for structural type correctness. Only the semantic invariants
listed above are runtime-checked.

---

## K. Domain/contract semantic-compatibility mappings (corrected, R1-09)

R1-09 establishes that domain and contract types are independent Python
classes, and that passing a domain object directly into
`ContractModel.model_validate(..., strict=True)` is **not** guaranteed to
succeed (in particular, a domain `ActorKind`/`GoalState`/etc. enum member
is not automatically accepted as valid input for the *contract's*
same-named-but-distinct enum class under `strict=True`). Compatibility is
therefore proven via **explicit mapping**, not direct pass-through:

| Domain type | Contract type | Mapping method |
|---|---|---|
| `mnemograph_domain.enums.*` member | `mnemograph_contracts.enums.*` member | Convert explicitly: `ContractEnum(domain_member.value)` — matched by **name/value**, never passed as the domain enum instance itself |
| `ActorRef` (domain) | `ActorRef` (contract) | Reconstruct explicitly: `ContractActorRef(kind=ContractActorKind(domain_actor.kind.value), actor_id=domain_actor.actor_id)` — the `actor_id` field is directly compatible because `ActorId` is a `NewType(UUID)`, which **is** a `uuid.UUID` instance at runtime |
| `GoalId`/`GoalPlanId`/`SubgoalId`/`TransitionEventId` (domain) | `UUID` (contract) | Directly compatible — every domain identifier `NewType` **is** a `uuid.UUID` at runtime; no conversion function needed |
| `AggregateVersion` (domain) | `int` (contract, `Field(ge=0)`) | Directly compatible — `AggregateVersion` **is** an `int` at runtime |
| `datetime` (domain, already UTC-aware via `ensure_aware_utc`) | `UtcDateTime` (contract, `Annotated[datetime, AfterValidator(ensure_aware_utc)]`) | Directly compatible as a raw `datetime.datetime` value — Pydantic accepts native `datetime` objects and re-validates/re-normalizes them through its own `AfterValidator` |
| `GoalTransitionRecord` (domain) | `GoalTransitionRecord` (contract) | Field-by-field explicit construction using the mappings above, then `model_validate(..., strict=True)` on the resulting **plain dict of already-contract-native values** — never on the domain dataclass instance itself |
| `Subgoal` (domain) | `SubgoalResponse` (contract) | Explicit construction: `subgoal_id`, `goal_id` (UUID-compatible directly), `statement`, `definition_of_done` (`str`-compatible directly), `version` (`int`-compatible directly), `acceptance_status` (enum, converted by value) — this now covers the `goal_id`/`version` fields R1-09 flags as omitted in v1.0's Subgoal shape |

No test in this batch asserts that a bare domain object can be passed
directly as the sole argument to a contract model's `model_validate`. Every
compatibility test constructs an explicit, already-contract-native
payload (a `dict` or contract-native keyword arguments) from the domain
object's fields, then validates that payload.

**Documented intentional shape difference (unchanged from v1.0):**
`mnemograph_contracts` does not yet publish a `GoalDecompositionProposal`,
`ApprovedGoalPlan`, or dependency-graph-aware Subgoal shape. This gap is
pre-existing, not created by this plan, and reconciling it is left to a
future, separately approved Delivery D1.x contracts batch. No contracts
production change is proposed here.

---

## L. Exact changed-file set and exact package-root export set (frozen, R1-10)

**One exact recommended set — 22 paths total.** No alternative counts are
offered at this level; alternatives (e.g., omitting the README) are
recorded only inside Section D's decision analysis (DR-18), not as a
second top-level file count.

| Path | Create/Modify | Contents |
|---|---|---|
| `libs/domain/src/mnemograph_domain/identifiers.py` | Modify | `+ TransitionEventId` |
| `libs/domain/src/mnemograph_domain/datetimes.py` | Create | `ensure_aware_utc` |
| `libs/domain/src/mnemograph_domain/errors.py` | Create | 4 exception classes |
| `libs/domain/src/mnemograph_domain/subgoals.py` | Create | `Subgoal`, `create_subgoal` (plain structural factory — no command, R2-01) |
| `libs/domain/src/mnemograph_domain/goal_plans.py` | Create | `PlanSubgoalEntry` (tuple-based `depends_on`, R2-05), `GoalDecompositionProposal`, `ApprovedGoalPlan`, `_validate_plan_entries` |
| `libs/domain/src/mnemograph_domain/goals.py` | Create | `Goal` |
| `libs/domain/src/mnemograph_domain/commands.py` | Create | 5 Goal command dataclasses (`CreateSubgoalCommand` never existed here — R2-01) |
| `libs/domain/src/mnemograph_domain/transitions.py` | Create | `GoalTransitionRecord`, `GoalTransitionResult`, `GoalProposalResult`, `GoalApprovalResult` (R2-04, replacing v1.1's single `GoalMutationResult`) |
| `libs/domain/src/mnemograph_domain/goal_mutations.py` | Create | `create_goal`, `begin_scoping`, `propose_goal_decomposition`, `revise_goal_plan`, `approve_goal_plan` |
| `libs/domain/src/mnemograph_domain/__init__.py` | Modify | 26 new exports (Section F.10, including `create_subgoal`) |
| `libs/domain/tests/test_domain_identifiers.py` | Modify | `+ TransitionEventId` in approved/deferred sets |
| `libs/domain/tests/test_domain_datetimes.py` | Create | `ensure_aware_utc` tests |
| `libs/domain/tests/test_domain_errors.py` | Create | Exception hierarchy/identity tests |
| `libs/domain/tests/test_domain_subgoals.py` | Create | `Subgoal`/`create_subgoal` tests (no actor-guard test — R2-01 removed the guard) |
| `libs/domain/tests/test_domain_goal_plans.py` | Create | Plan-entry/graph-validation tests, including duplicate-edge-within-`depends_on` (R2-05) |
| `libs/domain/tests/test_domain_goals.py` | Create | `Goal` construction/linkage-consistency tests, including out-of-scope-state rejection (R2-04) |
| `libs/domain/tests/test_domain_commands.py` | Create | Command construction/immutability tests |
| `libs/domain/tests/test_domain_transitions.py` | Create | `GoalTransitionRecord` and all three result-type construction/immutability/cross-validation tests |
| `libs/domain/tests/test_domain_goal_mutations.py` | Create | Full transition/version/authority/identity/atomicity matrix |
| `libs/domain/tests/test_domain_contract_compatibility.py` | Modify | New explicit-mapping compatibility assertions (K) |
| `libs/domain/tests/test_domain_boundaries.py` | Modify | Updated `APPROVED_EXPORTS` (42 symbols, including `create_subgoal`); remove `TransitionEventId` from `FORBIDDEN_EXPORTS`; replace/remove the obsolete blanket datetime ban with a narrow authorized-datetime-surface assertion; exception-surface assertion remains a named allowlist of exactly the 4 classes in `errors.py` |
| `libs/domain/README.md` | Modify | Documents the new Delivery D1.4 modules (DR-18, included by default per R1-10) |

**Expected unchanged (confirmed by Section O's guard commands):**
`libs/domain/pyproject.toml`; `uv.lock`; root `pyproject.toml`;
`libs/contracts/src/**`; `libs/domain/src/mnemograph_domain/enums.py`,
`versioning.py`, `actors.py`; `libs/domain/tests/test_domain_enums.py`,
`test_domain_versioning.py`, `test_domain_actor_ref.py`,
`test_import_domain.py`; all baselines, accepted ADRs, `apps/**`,
`infra/**`, `.github/workflows/**`, Compose files.

**Exact package-root export set:** the existing 16 Delivery D1.3 symbols
plus the 26 listed in Section F.10 — **42 symbols total**, no duplicates,
recalculated after removing `CreateSubgoalCommand`/`GoalMutationResult`
and adding `GoalTransitionResult`/`GoalProposalResult`/`GoalApprovalResult`
(R2-07), with `create_subgoal` retained as a root export (DR-28/R4).

---

## M. Dependency-ordered implementation sequence

| Step | Files | Symbols/tests | Prerequisite DR IDs | Validation after step |
|---|---|---|---|---|
| 1 | `identifiers.py`; `test_domain_identifiers.py` | `TransitionEventId` | none | `uv run pytest libs/domain/tests/test_domain_identifiers.py` |
| 2 | `datetimes.py`; `test_domain_datetimes.py` | `ensure_aware_utc` | none | `uv run pytest libs/domain/tests/test_domain_datetimes.py` |
| 3 | `errors.py`; `test_domain_errors.py` | 4 exception classes | DR-08 | `uv run pytest libs/domain/tests/test_domain_errors.py` |
| 4 | `subgoals.py`; `test_domain_subgoals.py` | `Subgoal`, `create_subgoal` (plain factory, R2-01) | DR-01, DR-14, DR-21, DR-23, DR-24 | `uv run pytest libs/domain/tests/test_domain_subgoals.py` |
| 5 | `goal_plans.py`; `test_domain_goal_plans.py` | `PlanSubgoalEntry` (tuple `depends_on`, R2-05), `GoalDecompositionProposal`, `ApprovedGoalPlan` | DR-02, DR-06, DR-15, DR-16, DR-16a, DR-16b, DR-22 | `uv run pytest libs/domain/tests/test_domain_goal_plans.py` |
| 6 | `goals.py`; `test_domain_goals.py` | `Goal` | DR-11, DR-17, DR-17a, DR-17b, DR-23, DR-24 | `uv run pytest libs/domain/tests/test_domain_goals.py` |
| 7 | `commands.py`; `test_domain_commands.py` | 5 Goal command dataclasses | DR-10, DR-11, DR-13 | `uv run pytest libs/domain/tests/test_domain_commands.py` |
| 8 | `transitions.py`; `test_domain_transitions.py` | `GoalTransitionRecord`, `GoalTransitionResult`, `GoalProposalResult`, `GoalApprovalResult`; complete direct-construction result invariants (R3-02) | DR-09 | `uv run pytest libs/domain/tests/test_domain_transitions.py` |
| 9 | `goal_mutations.py`; `test_domain_goal_mutations.py` | 5 mutation functions | DR-03, DR-04, DR-05, DR-06, DR-07, DR-12, DR-13, DR-17b, DR-26, DR-27 | `uv run pytest libs/domain/tests/test_domain_goal_mutations.py` |
| 10 | `__init__.py` | 26 new exports, including `create_subgoal` | all of the above, DR-28 | `uv run pytest libs/domain/tests` |
| 11 | `test_domain_contract_compatibility.py` | new mapping-based assertions | DR-25 | `uv run pytest libs/domain/tests/test_domain_contract_compatibility.py` |
| 12 | `test_domain_boundaries.py` | updated `APPROVED_EXPORTS`; remove `TransitionEventId` from `FORBIDDEN_EXPORTS`; replace blanket datetime ban with narrow authorized-datetime assertion; named exception allowlist | DR-08 | `uv run pytest libs/domain/tests/test_domain_boundaries.py` |
| 13 | `README.md` | documentation only | DR-18 | `pnpm run validate` |
| 14 | *(whole batch)* | — | all DR IDs resolved | full Section O command list |

Steps 1–3 are independent of the aggregate and can land first. Steps 4–9
are mutually dependent and must land together. Step 10 finalizes exports
once every symbol name is settled. Steps 11–13 are compatibility/boundary/
documentation passes over the completed implementation.

---

## N. Complete positive and negative test matrix

| Category | Test file | Scenario | Acceptance criterion |
|---|---|---|---|
| Construction/immutability | `test_domain_goals.py` | Valid `Goal` per each state row (F.6 table); field reassignment | Construction succeeds only for consistent state/linkage combinations; reassignment raises `FrozenInstanceError` |
| Negative construction | `test_domain_goals.py` | `Goal(state=AWAITING_PLAN_APPROVAL, current_proposal_plan_id=None, ...)`; `Goal(state=DELIBERATING, approved_goal_plan_id=None, ...)`; negative `version`; whitespace-only `statement` | Each raises `InvalidStructuralInputError` |
| Construction/immutability | `test_domain_subgoals.py` | Valid `Subgoal` via `create_subgoal`; field reassignment | Succeeds; reassignment raises `FrozenInstanceError` |
| Negative construction | `test_domain_subgoals.py` | Negative `version`; whitespace-only `statement`/`definition_of_done` | Raises `InvalidStructuralInputError` |
| No actor guard (R2-01) | `test_domain_subgoals.py` | `create_subgoal` called with no `actor` argument of any kind | Succeeds — confirms the plain-factory shape has no actor parameter to guard |
| Construction/immutability | `test_domain_goal_plans.py` | Valid `GoalDecompositionProposal`/`ApprovedGoalPlan`, including zero-entry case (DR-16b) | Succeeds |
| Negative construction | `test_domain_goal_plans.py` | Duplicate `subgoal_id` across entries; dangling `depends_on`; self-edge; a genuine cycle (e.g., A→B→C→A); a duplicate `SubgoalId` repeated within one entry's `depends_on` tuple (R2-05) | Each raises `InvalidStructuralInputError` |
| Display order vs. dependency | `test_domain_goal_plans.py` | `entries` listed in an order that does **not** match dependency order, but the graph is acyclic | Construction succeeds (proves DR-16's separation) |
| Construction/immutability | `test_domain_commands.py` | Each of the 5 Goal commands; field reassignment | Succeeds; reassignment raises `FrozenInstanceError` |
| Construction/immutability | `test_domain_transitions.py` | `GoalTransitionRecord`, `GoalTransitionResult`, `GoalProposalResult`, `GoalApprovalResult`; field reassignment | Succeeds; reassignment raises `FrozenInstanceError` |
| Result-type shape (R2-04) | `test_domain_transitions.py` | Attempt to construct `GoalTransitionResult` with a `proposal` or `approved_plan` field | Fails at the type level — no such field exists on that class |
| Result-type value consistency (R2-04/R3-02) | `test_domain_transitions.py` | Construct any of the three result types with a mismatched `transition.goal_id`/`version`/`next_state` relative to `goal` | Raises `InvalidStructuralInputError` |
| Result-type direct-construction invariants (R3-02) | `test_domain_transitions.py` | Construct `GoalTransitionResult` with a resulting `Goal` in `AWAITING_PLAN_APPROVAL` or `DELIBERATING`; construct `GoalProposalResult` with wrong Goal state, `proposal.goal_id`, `proposal.plan_id`, or proposal version; construct `GoalApprovalResult` with wrong Goal state, `approved_plan.goal_id`, `approved_plan.plan_id`, or approved-plan version | Every inconsistent category raises `InvalidStructuralInputError`; valid proposal/approval results still construct successfully |
| Negative version, direct construction (R2-04) | `test_domain_transitions.py`, `test_domain_goal_plans.py` | `GoalTransitionRecord(version=-1, ...)`; `GoalDecompositionProposal(version=-1, ...)`; `ApprovedGoalPlan(version=-1, ...)` | Each raises `InvalidStructuralInputError` |
| Naive/UTC datetime | `test_domain_transitions.py`, `test_domain_datetimes.py` | Naive `datetime`; non-UTC aware `datetime`; UTC aware `datetime` — passed directly to `GoalTransitionRecord(...)` | Naive raises `ValueError`; non-UTC is normalized; UTC round-trips unchanged — proven even via **direct** construction (R1-04) |
| Legal transitions | `test_domain_goal_mutations.py` | Each of the 5 rows in G.1, in sequence from creation to `DELIBERATING` | Field deltas match G.1 exactly at each step; `goal.version` progresses `0,1,2,3,4`; `approved_goal_plan_version` equals the proposal's own (unincremented) `version` (R2-02) |
| Illegal transitions | `test_domain_goal_mutations.py` | Every (source-state, operation) pair not in G.1 | Raises `IllegalGoalTransitionError` |
| Out-of-scope state construction (R2-04) | `test_domain_goals.py` | `Goal(state=GoalState.AWAITING_USER, ...)` and each of `PAUSED`/`CROSS_GOAL_REVIEW`/`FINAL_CANDIDATE`/`STOPPED` | Each raises `InvalidStructuralInputError` |
| Actor-authority guards | `test_domain_goal_mutations.py` | Each Goal mutation attempted by every non-permitted `ActorKind`; `create_goal` attempted by every non-`USER` actor (R2-04) | Raises `ActorNotPermittedError` |
| Identity guard (R2-03/DR-26) | `test_domain_goal_mutations.py` | Each Goal mutation called with `command.goal_id != goal.goal_id`; `approve_goal_plan` called with `proposal.goal_id != goal.goal_id` | Raises `InvalidStructuralInputError` |
| Subgoal↔entries set-equality (R2-03/DR-27) | `test_domain_goal_mutations.py` | `propose_goal_decomposition` with an entry referencing a `subgoal_id` not present in `command.subgoals`, or a supplied Subgoal not referenced by any entry, or a supplied Subgoal whose `goal_id` does not match | Raises `InvalidStructuralInputError` |
| Stale version | `test_domain_goal_mutations.py` | Each mutation with `expected_version != goal.version` | Raises `GoalVersionConflictError`; no result returned |
| No mutation on rejection | `test_domain_goal_mutations.py` | Every rejection case above | Assert the original `goal`/`proposal` objects are unchanged and no result was returned |
| `approve_goal_plan` linkage check | `test_domain_goal_mutations.py` | `proposal.plan_id`/`version` does not match `goal.current_proposal_plan_id`/`version` | Raises `InvalidStructuralInputError` |
| Plan-version preservation (R2-02) | `test_domain_goal_mutations.py` | `approve_goal_plan` on a proposal at version `0` | `ApprovedGoalPlan.version == 0`; `goal.approved_goal_plan_version == 0` — never `1` |
| Determinism | `test_domain_goal_mutations.py` | Two calls with identical caller-supplied `event_id`/`occurred_at`/IDs | Produce byte-identical `GoalTransitionRecord` values (proves no hidden randomness/clock — R1-03/R2-01) |
| Domain/contract compatibility | `test_domain_contract_compatibility.py` | Explicit mapping of `GoalTransitionRecord`, `ActorRef`, all enums, `Subgoal` (including `goal_id`/`version`) into contract-native payloads, then `model_validate(strict=True)` | Succeeds; round-trips equal; existing D1.3 assertions continue to pass unmodified |
| Dependency boundaries (R3-01) | `test_domain_boundaries.py` | AST-based import test over all new files; `TransitionEventId` absent from `FORBIDDEN_EXPORTS`; no blanket datetime prohibition; narrow authorized-datetime-surface assertion | All new files import only stdlib or `mnemograph_domain`; the only datetime import is stdlib `datetime`, and the only datetime-related package-root helper is `ensure_aware_utc` |
| Package-root exports | `test_domain_boundaries.py` | `mnemograph_domain.__all__` | Equals exactly the 42-symbol set, no duplicates, including `create_subgoal` |
| Named exception allowlist | `test_domain_boundaries.py` | Every exported object that is an exception class | Set equals exactly `{GoalVersionConflictError, IllegalGoalTransitionError, ActorNotPermittedError, InvalidStructuralInputError}` |
| D1/D5 exclusion | `test_domain_goal_mutations.py` | `GoalState.ACCEPTED`/`PUBLISHING`/`COMPLETED` do not exist; no function references any state beyond `DELIBERATING` | Confirms unchanged enum and no out-of-scope reference |

---

## O. Validation and scoped diff-proof commands

Working directory: repository root.

```
uv run pytest libs/domain/tests
uv run ruff format --check libs/domain
uv run ruff check libs/domain
uv run mypy .
pnpm run validate
git diff --check
git diff --name-only
git diff --name-only -- libs/domain/pyproject.toml
git diff --name-only -- uv.lock
git diff --name-only -- libs/contracts/src/mnemograph_contracts
```

Focused commands for the exact new/modified test files:

```
uv run pytest libs/domain/tests/test_domain_identifiers.py
uv run pytest libs/domain/tests/test_domain_datetimes.py
uv run pytest libs/domain/tests/test_domain_errors.py
uv run pytest libs/domain/tests/test_domain_subgoals.py
uv run pytest libs/domain/tests/test_domain_goal_plans.py
uv run pytest libs/domain/tests/test_domain_goals.py
uv run pytest libs/domain/tests/test_domain_commands.py
uv run pytest libs/domain/tests/test_domain_transitions.py
uv run pytest libs/domain/tests/test_domain_goal_mutations.py
uv run pytest libs/domain/tests/test_domain_contract_compatibility.py
uv run pytest libs/domain/tests/test_domain_boundaries.py
```

`test_domain_boundaries.py` is a required focused gate for R3-01: it must
prove the production-import boundary remains stdlib-only, `TransitionEventId`
is removed from `FORBIDDEN_EXPORTS`, the former blanket datetime prohibition
is absent, and the narrow authorized surface permits only standard-library
`datetime` imports plus the single public helper `ensure_aware_utc`.
`test_domain_transitions.py` is a required focused gate for R3-02: it must
exercise every direct-construction rejection listed in Section N and assert
`InvalidStructuralInputError` for each.

| Command | Expected exit code | Expected output |
|---|---|---|
| `uv run pytest libs/domain/tests` | `0` | all tests pass, including R3-01 boundary reconciliation and R3-02 result-invariant negatives |
| `uv run ruff format --check libs/domain` | `0` | already formatted |
| `uv run ruff check libs/domain` | `0` | `All checks passed!` |
| `uv run mypy .` | `0` | `Success: no issues found...` |
| `pnpm run validate` | `0` | all sub-gates pass |
| `git diff --check` | `0` | no output |
| `git diff --name-only` | `0` | exactly the 22 paths in Section L |
| `git diff --name-only -- libs/domain/pyproject.toml` | `0` | **no output** |
| `git diff --name-only -- uv.lock` | `0` | **no output** |
| `git diff --name-only -- libs/contracts/src/mnemograph_contracts` | `0` | **no output** |

---

## P. Risk, rollback, and commit boundary

- **Dependency impact:** none; stdlib-only boundary automatically re-verified.
- **Security/authority impact:** none introduced; `USER` retains exclusive
  authority over revision/approval; `SYSTEM`'s role (`begin_scoping`,
  `propose_goal_decomposition`) remains orchestration attribution, not
  authentication or human authority; `create_subgoal` carries no actor of
  any kind (R2-01), so it introduces no attribution surface at all.
- **Compatibility impact:** the domain surface grows from 16 to 42
  exported symbols, purely additively. The corrected compatibility tests
  (K) are more rigorous than v1.0's, reducing the risk of a false-positive
  "compatible" claim.
- **Data/migration/operational impact:** none — no persistence, no runtime
  surface.
- **Rollback procedure:** unchanged from v1.0 — do not merge the future
  branch, or revert its single merge commit.
- **Likely implementation failure modes:** (1) forgetting to update
  `test_domain_boundaries.py`'s exception-allowlist and export-set
  constants when the final symbol names are chosen; (2) accidentally
  re-deriving `occurred_at`/IDs internally instead of threading them
  through from the command (regresses R1-03); (3) validating the
  dependency graph using tuple position instead of a true graph
  traversal (regresses R1-06); (4) accidentally incrementing
  `ApprovedGoalPlan.version` on approval (regresses R2-02); (5) omitting
  the Goal/command or proposal/Goal identity guard on any of the four
  Goal mutations (regresses R2-03).
- **How the file boundary limits risk:** all 22 paths are confined to
  `libs/domain/**`; the three scoped `git diff --name-only` guard commands
  mechanically prove no contracts/dependency/lockfile path was touched.
- **Commit boundary:** one implementation commit remains appropriate
  (DR-19, R1-accepted), for the same interdependency reasoning as v1.0.
  Proposed message (not authorized to use yet):
  `feat(domain): establish D1.4 goal-plan-subgoal scoping and plan approval slice`

---

## Q. Consolidated human-decision bundle

Per R2-06, this table includes **every** DR ID's selected disposition —
not only rows still open — each explicitly classified as fixed by an
accepted source, a binding factual/review correction, structurally
derived, or newly proposed requiring human approval. Full
constraints/options/trade-offs for every row are in Section D; this is
the sufficient, single-pass index.

| DR ID | One-line question | Selected disposition | Classification |
|---|---|---|---|
| DR-01 | Subgoal ownership model | Independently identified/versioned entity; creation is a plain structural factory (no command/actor/event) | Binding correction (R1-01, narrowed R2-01) |
| DR-02 | Does the plan family carry its own version? | Yes, but never incremented in this slice | Binding correction (R1-02, refined R2-02) |
| DR-03 | `begin_scoping` actor | `SYSTEM` | Newly proposed, R1/R2-accepted direction |
| DR-04 | `propose_goal_decomposition` actor | `SYSTEM` | Newly proposed, R1/R2-accepted direction |
| DR-05 | Revision clears current-proposal linkage? | Yes | Newly proposed |
| DR-06 | Approved plan's `plan_id`/version relative to its proposal | Same `plan_id`; same, unincremented `version` | Binding correction (R2-02) |
| DR-07 | Fresh plan identity per proposal round? | Yes | Newly proposed |
| DR-08 | Error taxonomy | 4 narrow `ValueError` subclasses in `errors.py`, extended to cover R2-03/R2-04 categories | Binding correction (R1-07), scope extended (R2-04) |
| DR-09 | Mutation result shape | Three distinct result types (`GoalTransitionResult`, `GoalProposalResult`, `GoalApprovalResult`) | Binding correction (R2-04) |
| R3-01 | D1.3 boundary-test reconciliation | Permit `TransitionEventId`; replace the blanket datetime prohibition with the narrow authorized datetime surface | Binding correction (R3-01) |
| R3-02 | Result-type direct-construction invariants | Retain the three result types and add complete state/payload/Goal-linkage invariants | Binding correction (R3-02) |
| DR-10 | Command-dataclass pattern for Goal mutations | Yes, one per Goal mutation | Newly proposed |
| DR-11 | `create_goal` and `expected_version` | Exempt — factory, not a mutation over an existing aggregate | Structurally derived (R1-07 reasoning) |
| DR-12 | Validation-check ordering | actor → Goal-identity → `expected_version` → transition-legality → payload/structural (→ proposal-identity, approval only) | Newly proposed, refined R2-03 |
| DR-13 | Deterministic ID/time injection | Fully caller-supplied; no internal `uuid4()`/`datetime.now()` anywhere | Binding correction (R1-03) |
| DR-14 | Subgoal carries `acceptance_status`? | Yes, initialized `NOT_ACCEPTED` | Binding correction (R1-01) |
| DR-15 | Required/optional Subgoal membership | Not modeled in D1.4 | Newly proposed |
| DR-16 | Dependency graph validity vs. display order | Independent of tuple position; validated via topological-sort-style cycle detection | Binding correction (R1-06) |
| DR-16a | Duplicate/dangling/self-edge representation | `depends_on` is a `tuple`, not `frozenset`; all three rejected explicitly | Binding correction (R1-06, corrected R2-05) |
| DR-16b | Zero-Subgoal plans valid? | Yes | Newly proposed |
| DR-17 | Goal's approved-plan linkage | ID/version only, never the embedded object | Binding correction (R1-02) |
| DR-17a | Goal's current-proposal linkage | ID/version pair, mirroring DR-17 | Structurally derived |
| DR-17b | Approval clears current-proposal linkage? | Yes | Newly proposed |
| DR-18 | README update | Yes, included in Section L's frozen set | Newly proposed |
| DR-19 | One implementation commit? | Yes | Newly proposed, R1/R2-accepted direction |
| DR-20 | *(removed)* `create_subgoal` actor guard | N/A — no actor guard exists; question does not apply | Removed (R2-01) |
| DR-21 | Subgoal creation separate from proposal attachment? | Yes, via a plain factory function (no command wrapper) | Refined (R2-01) |
| DR-22 | Unified `GoalPlan` type vs. two distinct types | Two distinct types sharing `plan_id` and the same unincremented version | Newly proposed, refined R2-02 |
| DR-23 | Whitespace vs. length-only string validation | Non-whitespace required (stricter than contract) | Newly proposed |
| DR-24 | Generic `isinstance` runtime type-checking | No — semantic checks only, scope extended per R2-04 | Newly proposed |
| DR-25 | Domain/contract compatibility method | Explicit field-by-field mapping, never direct `model_validate` pass-through | Binding correction (R1-09) |
| DR-26 | Goal/command (and proposal/Goal) identity guard | Reject any `goal_id` mismatch; checked right after the actor guard | Binding correction (R2-03) |
| DR-27 | Subgoal↔entries set-relation for `propose_goal_decomposition` | Exact set equality, no duplicates, matching `goal_id` on every supplied Subgoal | Binding correction (R2-03) |
| DR-28 | Package-root export policy for `create_subgoal` | Root-export `create_subgoal` | Newly proposed, requiring explicit human approval (R4): it is a public structural factory and root export keeps the domain API consistent |

Every "newly proposed" row above is a recommendation, not a decision;
every "binding correction" row reflects an explicit R1/R2 review
requirement already made mandatory for this revision. Lead-SA/human review
may accept, reject, or substitute any newly-proposed row without
requiring a further planning round, provided the substitution remains
within this slice's stated boundary (Section A).

---

## R. Stop conditions and authorization gate

**Stop conditions.** Implementation must stop and report if: the
checkpoint drifts from `eb43e1248b563c3e3117a971deacb140092e908f`; the
tracked working tree or index is dirty at the start of implementation; any
Section D decision remains unresolved; any changed path falls outside
Section L's exact 22; any dependency/lockfile/contracts-production change
becomes necessary; any required validation command fails and cannot be
corrected within the exact boundary; or any request arrives to implement
behavior beyond first entry into `DELIBERATING`.

**Authorization gate.**

Plan v1.5 is submitted for Lead-SA and human review. No decision in
Section D or Q is self-approved by this planning process. The canonical
active artifact is the tracked file
`docs/plans/issue-23-delivery-d1-4.md` on the planning-only branch
`planning/23-d1-4-goal-plan`. The branch and tracked file exist only to
support plan review; this planning branch must never be merged into `main`;
and their existence grants no implementation authorization. The planning
history includes the tracked-artifact migration commit
`11a30b7b6ff22995e51dbc5de51a510acdbb2817` and R4 correction commit
`7757c80ac3bc7561891cf8f82110cad78dd70b3e`. Neither historical ignored
`tmp/` artifact identified in the R1-11 disclosure is current or canonical.

**Implementation authorization remains NOT APPROVED.**

*(End of plan.)*
