# ADR-DOMAIN-003: Delivery D1 Public Contract Vocabulary Reconciliation

## ADR ID

ADR-DOMAIN-003

## Title

Delivery D1 Public Contract Vocabulary Reconciliation

## Status

Accepted

## Date

2026-07-18

## Deciders

Human project owner, Lead SA

## Related issue

[GitHub Issue #17](https://github.com/frwkHoangQuy/Mnemograph_workbench/issues/17)

## Related baseline sections

- [Project Charter](../baseline/Mnemograph_Triadic_Research_Workbench_Project_Charter_v1.0.md) §8.2 and §8.5.
- [System Design](../baseline/Mnemograph_Triadic_Research_Workbench_System_Design_v0.1.md) §5.2 and §5.4.
- [ADR-GOV-001: Phase Namespace Reconciliation](ADR-GOV-001-phase-namespace-reconciliation.md).
- [ADR-DOMAIN-001: Pure Domain and Published Contract Boundaries](ADR-DOMAIN-001-pure-domain-and-published-contract-boundaries.md), especially D1-D and D1-E.
- [ADR-DOMAIN-002: Delivery D1.2 Schema Scope and Moderator Semantics](ADR-DOMAIN-002-d1-2-schema-scope-and-moderator-semantics.md).
- GitHub Issue #16 (current Delivery D1.2 implementation issue, Approved for planning only).

## Delivery scope

Delivery D1.2 public contract wire-vocabulary reconciliation.

> **Accepted decision.** On 2026-07-18, after Lead-SA review, the human project owner explicitly accepted Dimension A option A2, Dimension B option B3, and Dimension C option C2. This ADR records that accepted decision. ADR acceptance does not authorize Delivery D1.2 implementation; Issue #16 remains the current D1.2 implementation issue and is Approved for planning only.

## Context and problem

Delivery D1.2 planning for Issue #16 identified that the Project Charter and the System Design — both accepted baselines — use materially different vocabulary for the same underlying Delivery D1 concepts:

1. **Goal lifecycle wire names through `FINAL_CANDIDATE` or `STOPPED`.** Charter §8.5 names `GoalSubmitted`, `JointScoping`, `DecompositionProposed`, `SubgoalDeliberation`, `UserCheckpoint`; System Design §5.2 names `Draft`, `Scoping`, `AwaitingPlanApproval`, `Deliberating`, `AwaitingUser` for what appears to be the same sequence of concepts. Both agree on `Paused`, `CrossGoalReview`, `FinalCandidate`, and `Stopped`.
2. **Intervention/checkpoint-action vocabulary.** Charter §8.2 names `CONTINUE`, `GUIDE`, `REVISE_SCOPE`, `ACCEPT_SUBGOAL`, `REOPEN`, `PAUSE`, `STOP`; System Design §5.4 names `GUIDE`, `CORRECT_CONTEXT`, `REVISE_SCOPE`, `PAUSE`, `STOP`, `REOPEN`. `CONTINUE` and `ACCEPT_SUBGOAL` appear only in the Charter; `CORRECT_CONTEXT` appears only in System Design.
3. **Classification of `ACCEPT_SUBGOAL`.** Neither baseline states whether Subgoal acceptance is a member of the general intervention/checkpoint-action enum or a structurally separate command. ADR-DOMAIN-001 D1-E requires that Subgoal acceptance be issued as a user command, but that requirement is satisfied equally whether the command is a member of the general intervention enum or a dedicated command family; it does not by itself favor either structure. System Design §5.2's Goal-workflow diagram separately treats "Accept subgoals" as a distinct transition trigger from the §5.4 intervention list, and `ACCEPT_SUBGOAL` is absent from §5.4's intervention list itself.

No accepted ADR previously reconciled either conflict. GitHub Issue #17 recorded the human project owner's decision to resolve all three dimensions, selecting option A2 for Dimension A, option B3 for Dimension B, and option C2 for Dimension C.

## Constraints

- GitHub Issue #17 records the explicit human decision context for this ADR.
- GitHub Issue #16 is the current Delivery D1.2 implementation issue and is Approved for planning only; this ADR does not change that status. ADR-DOMAIN-003's acceptance does not authorize Delivery D1.2 implementation. Issue #16 requires a revised full implementation plan and a separate, explicit human implementation approval before any Delivery D1.2 code change proceeds. This ADR does not imply that a different or additional implementation issue is required, unless the human authority changes or decomposes Issue #16's scope.
- This ADR must not modify, supersede, or reinterpret ADR-DOMAIN-001 or ADR-DOMAIN-002.
- Delivery D1 remains bounded at `FINAL_CANDIDATE` or `STOPPED`; `ACCEPTED`, `PUBLISHING`, and `COMPLETED` remain Delivery D5 concerns and must not become D1 wire values or D1 behavior.
- `ActorKind` remains exactly `USER`, `SCIENTIST`, `SA`, and `SYSTEM`; Moderator remains ADR-DOMAIN-002 Option B (a visible orchestration policy whose persisted mutations use `ActorKind.SYSTEM`, not a domain actor kind).
- This ADR does not define entity field lists, `ActorRef` shape, error-envelope fields, `EntityId`/datetime implementation mechanics, Pydantic validators, API behavior, persistence, or runtime orchestration.
- No dependency, lockfile, or source-code change is authorized by this ADR.
- No baseline document is modified by this ADR.

## Decision drivers

- Resolve the two identified Charter/System Design vocabulary conflicts without declaring either accepted baseline invalid or superseded.
- Preserve full traceability from any adopted wire token back to its Charter and/or System Design source term.
- Preserve the `FINAL_CANDIDATE`/`STOPPED` Delivery D1 boundary and the Delivery D5 exclusion of `ACCEPTED`/`PUBLISHING`/`COMPLETED`.
- Preserve `USER` normative authority without encoding actor-authorization logic in the contract (Pydantic) layer.
- Avoid re-litigating ADR-DOMAIN-001's primitive conventions or ADR-DOMAIN-002's Moderator/`ActorKind` decision.
- Keep the reconciliation to vocabulary/classification only — no entity fields, schemas, or implementation mechanics.
- Preserve Issue #16's existing planning-only approval status without implying a new implementation issue is required.

## Facts and evidence

- Project Charter §8.5 defines a Goal state-machine diagram using `GoalSubmitted`, `JointScoping`, `DecompositionProposed`, `SubgoalDeliberation`, `UserCheckpoint`, `Paused`, `CrossGoalReview`, `FinalCandidate`, `Completed`, `Stopped`.
- System Design §5.2 defines a Goal workflow diagram using `Draft`, `Scoping`, `AwaitingPlanApproval`, `Deliberating`, `AwaitingUser`, `Paused`, `CrossGoalReview`, `FinalCandidate`, `Accepted`, `Publishing`, `Completed`, `Stopped`.
- Project Charter §8.2 lists checkpoint actions `CONTINUE`, `GUIDE`, `REVISE_SCOPE`, `ACCEPT_SUBGOAL`, `REOPEN`, `PAUSE`, `STOP`.
- System Design §5.4 lists intervention semantics `GUIDE`, `CORRECT_CONTEXT`, `REVISE_SCOPE`, `PAUSE`, `STOP`, `REOPEN`.
- ADR-DOMAIN-001 D1-E states Goal progresses "through `FINAL_CANDIDATE` or `STOPPED`," that Subgoal "may be accepted or reopened only by a user command," and that Delivery D1 must not implement `ACCEPTED`, `PUBLISHING`, or `COMPLETED` behavior merely for enum compatibility.
- ADR-DOMAIN-002 establishes that `ActorKind` remains exactly `USER`, `SCIENTIST`, `SA`, `SYSTEM`, and that Moderator is a visible orchestration policy whose persisted mutations use `ActorKind.SYSTEM`.
- GitHub Issue #16 is the current Delivery D1.2 implementation issue and is Approved for planning only.
- During proposal review on 2026-07-18, Lead SA verified GitHub Issue #17's recorded human selection of exactly A2 (Dimension A), B3 (Dimension B), and C2 (Dimension C).

### Scientific evidence boundary

Scientific sourcing is not applicable to this decision. This ADR makes no scientific claim, does not invent citations, and does not treat model output as scientific evidence.

## Assumptions

- A future Delivery D1.2 implementation batch, delivered under Issue #16's revised and separately approved implementation plan, will consume this vocabulary without needing to revisit the classification questions resolved here.
- Any later need to change this vocabulary would require a superseding ADR with explicit human approval.

## Options considered

### Dimension A — canonical Goal-state wire vocabulary through `FINAL_CANDIDATE` or `STOPPED`

- **A1** — adopt Charter §8.5 vocabulary verbatim as wire tokens (`GOAL_SUBMITTED`, `JOINT_SCOPING`, `DECOMPOSITION_PROPOSED`, `SUBGOAL_DELIBERATION`, `USER_CHECKPOINT`, plus shared `PAUSED`/`CROSS_GOAL_REVIEW`/`FINAL_CANDIDATE`/`STOPPED`).
- **A2 (selected)** — adopt System Design §5.2 vocabulary verbatim as wire tokens (`DRAFT`, `SCOPING`, `AWAITING_PLAN_APPROVAL`, `DELIBERATING`, `AWAITING_USER`, plus shared `PAUSED`/`CROSS_GOAL_REVIEW`/`FINAL_CANDIDATE`/`STOPPED`).
- **A3** — new reconciled vocabulary layer with newly coined tokens for the five divergent states, explicitly mapped to both sources.
- **A-Defer** — leave the Goal-state wire vocabulary unresolved.

### Dimension B — canonical intervention/checkpoint-action wire vocabulary

- **B1** — adopt Charter §8.2 vocabulary verbatim (excluding `ACCEPT_SUBGOAL`, decided under Dimension C), dropping System Design's `CORRECT_CONTEXT`.
- **B2** — adopt System Design §5.4 vocabulary verbatim, dropping Charter's `CONTINUE`.
- **B3 (selected)** — adopt the union of both accepted vocabularies: `GUIDE`, `REVISE_SCOPE`, `PAUSE`, `STOP`, `REOPEN` (common to both), plus `CONTINUE` (Charter §8.2 only) and `CORRECT_CONTEXT` (System Design §5.4 only), treating the two document-specific terms as additive rather than competing.
- **B-Defer** — leave the intervention-action wire vocabulary unresolved.

### Dimension C — classification of `ACCEPT_SUBGOAL`

- **C1** — `ACCEPT_SUBGOAL` is a member of the general intervention/checkpoint-action enum, carried by the future general user-intervention mutating-command family.
- **C2 (selected)** — `ACCEPT_SUBGOAL` is a dedicated Subgoal command intent, absent from the general intervention/checkpoint-action enum, distinct from the general user-intervention command family.
- **C-Defer** — leave the classification unresolved.

Both C1 and C2 satisfy ADR-DOMAIN-001 D1-E's "user command" requirement; that requirement establishes `USER`-authorized, mutating-command semantics but does not independently favor a separate command family over general-enum membership, or vice versa. The selection of C2 is based on (a) `ACCEPT_SUBGOAL` being absent from System Design §5.4's general intervention list, (b) System Design §5.2's Goal-workflow diagram treating "Accept subgoals" as a distinct transition trigger separate from the §5.4 intervention list, and (c) the human authority's explicit selection of C2 recorded on GitHub Issue #17 — not on any independent reading of ADR-DOMAIN-001's "user command" phrase as favoring either structure.

## Trade-off comparison

| Dimension | Option | Benefit | Risk |
|---|---|---|---|
| A | A1 (Charter verbatim) | Favors product/working-agreement wording | Discards System Design's delivery-decomposition wording without a stated implementation reason |
| A | A2 (System Design verbatim) — **selected** | Favors the document that already enumerates Delivery D1 in §15; wording maps naturally onto delivery-phase code identifiers | Discards Charter's specific pre-`FinalCandidate` wording as the wire form (traceability preserved via mapping table) |
| A | A3 (new reconciled) | Avoids privileging either baseline | Introduces novel tokens absent from both accepted documents |
| A | A-Defer | No risk of incorrect selection | Indefinitely blocks any D1.2 Goal-state schema |
| B | B1 (Charter verbatim) | Simpler, fewer tokens | Drops System Design's `CORRECT_CONTEXT` entirely |
| B | B2 (System Design verbatim) | Simpler, fewer tokens | Drops Charter's `CONTINUE` entirely |
| B | B3 (union) — **selected** | Preserves both documents' distinct actions without asserting an unstated synonym | Slightly larger enum than either single-source option |
| B | B-Defer | No risk of incorrect selection | Indefinitely blocks any D1.2 intervention-action schema |
| C | C1 (intervention enum member) | Single enum for all checkpoint-facing actions | Not selected by the human authority on Issue #17; does not reflect `ACCEPT_SUBGOAL`'s absence from System Design §5.4's general intervention list |
| C | C2 (dedicated command intent) — **selected** | Matches System Design's distinct "Accept subgoals" transition trigger, keeps Subgoal acceptance out of the general intervention enum, and reflects the human authority's explicit selection on Issue #17 | Requires a second command family to be defined in a future D1.2 batch |
| C | C-Defer | No risk of incorrect selection | Indefinitely blocks any D1.2 Subgoal-acceptance modeling |

## Decision

This ADR **adopts** option **A2** for Dimension A, option **B3** for Dimension B, and option **C2** for Dimension C. The human project owner explicitly accepted these decisions on 2026-07-18 after Lead-SA review; they are normative decisions recorded by this Accepted ADR.

### Decision A (A2) — canonical D1 Goal-state wire vocabulary

The canonical Delivery D1 Goal-state wire vocabulary, through `FINAL_CANDIDATE` or `STOPPED` only, is System Design §5.2's vocabulary, expressed as the following exact wire tokens:

- `DRAFT`
- `SCOPING`
- `AWAITING_PLAN_APPROVAL`
- `DELIBERATING`
- `AWAITING_USER`
- `PAUSED`
- `CROSS_GOAL_REVIEW`
- `FINAL_CANDIDATE`
- `STOPPED`

This ADR selects System Design's vocabulary as the **canonical D1 wire vocabulary** while preserving full traceability to the Charter's equivalent terms via the mapping table below. The Charter's vocabulary is **not** described as invalid or superseded — it remains the accepted product/working-agreement description of the same lifecycle; this ADR fixes which terms are canonical at the D1 contract wire level.

`ACCEPTED`, `PUBLISHING`, and `COMPLETED` are explicitly **excluded** from this enum; they remain Delivery D5 concerns and must not appear as D1 wire values or D1 behavior.

### Decision B (B3) — canonical intervention/checkpoint-action wire vocabulary

The canonical Delivery D1 general intervention/checkpoint-action wire vocabulary is the union of both accepted baselines' terms, expressed as the following exact wire values:

- `GUIDE`
- `REVISE_SCOPE`
- `PAUSE`
- `STOP`
- `REOPEN`
- `CONTINUE`
- `CORRECT_CONTEXT`

`GUIDE`, `REVISE_SCOPE`, `PAUSE`, `STOP`, and `REOPEN` appear in both accepted baselines. `CONTINUE` comes from Charter §8.2. `CORRECT_CONTEXT` comes from System Design §5.4. `CONTINUE` and `CORRECT_CONTEXT` remain distinct wire values — neither is treated as a synonym or restatement of the other, or of `GUIDE`.

The presentation order above is **non-semantic**; it does not imply priority, sequence, or default selection. Unless a later, separately approved implementation plan explicitly fixes an ordering for a specific purpose (e.g., a stable JSON Schema enum order), no significance attaches to this list's order.

### Decision C (C2) — classification of `ACCEPT_SUBGOAL`

`ACCEPT_SUBGOAL` is a **dedicated Subgoal command intent**, distinct from the general intervention/checkpoint-action command family. It **must not** appear as a member of the Decision B enum above.

This decision defines **classification only**. It does not define:
- the command's field list or wire shape;
- any API behavior; or
- any Pydantic implementation mechanics.

Whichever future revised D1.2 implementation batch, delivered under a separately approved Issue #16 implementation plan, defines the Subgoal-acceptance command schema **must** include `expected_version` on that command, per ADR-DOMAIN-001 D1-D's requirement that every mutating command carries `expected_version`. `USER` normative authority over Subgoal acceptance (Charter §8, ADR-DOMAIN-002) must be preserved conceptually and structurally (e.g., an `actor: ActorRef` data field), but **must not** be encoded as a `USER`-only Pydantic validator or any other contract-layer authorization check — that enforcement remains `mnemograph_domain`'s and the future application layer's responsibility.

`REOPEN` remains part of the Decision B general intervention/checkpoint-action vocabulary; its eventual command-envelope packaging (which command family carries it) remains deferred to Issue #16's future revised implementation plan and is not decided by this Dimension C decision.

## Exact vocabulary and mapping tables

### Goal-state mapping (Decision A / A2)

| Charter §8.5 term | System Design §5.2 term (canonical D1 wire token) |
|---|---|
| `GoalSubmitted` | `DRAFT` |
| `JointScoping` | `SCOPING` |
| `DecompositionProposed` | `AWAITING_PLAN_APPROVAL` |
| `SubgoalDeliberation` | `DELIBERATING` |
| `UserCheckpoint` | `AWAITING_USER` |
| `Paused` | `PAUSED` |
| `CrossGoalReview` | `CROSS_GOAL_REVIEW` |
| `FinalCandidate` | `FINAL_CANDIDATE` |
| `Stopped` | `STOPPED` |

`Accepted`, `Publishing`, and `Completed` (System Design §5.2) and `Completed` (Charter §8.5) are **not** part of this table; they remain Delivery D5 and are referenced here only to state the exclusion boundary.

### Intervention/checkpoint-action vocabulary (Decision B / B3)

| Wire value | Source |
|---|---|
| `GUIDE` | Charter §8.2 and System Design §5.4 (identical in both) |
| `REVISE_SCOPE` | Charter §8.2 and System Design §5.4 (identical in both) |
| `PAUSE` | Charter §8.2 and System Design §5.4 (identical in both) |
| `STOP` | Charter §8.2 and System Design §5.4 (identical in both) |
| `REOPEN` | Charter §8.2 and System Design §5.4 (identical in both) |
| `CONTINUE` | Charter §8.2 only |
| `CORRECT_CONTEXT` | System Design §5.4 only |

`ACCEPT_SUBGOAL` (Charter §8.2) is **not** part of this table; see Decision C.

### `ACCEPT_SUBGOAL` classification (Decision C / C2)

| Term | Classification |
|---|---|
| `ACCEPT_SUBGOAL` | Dedicated Subgoal command intent; not a member of the intervention/checkpoint-action enum above; exact command schema deferred to Issue #16's future revised implementation plan |

## Rationale

Selecting System Design §5.2's vocabulary for Decision A keeps the D1 wire vocabulary aligned with the document that already frames Delivery D1 as a repository delivery phase (System Design §15, ADR-GOV-001), while the mapping table preserves full traceability to the Charter's equivalent product-facing terms, so neither baseline is treated as invalid. Selecting the union for Decision B (B3) avoids discarding either baseline's distinct action (`CONTINUE` or `CORRECT_CONTEXT`) and avoids asserting an unstated synonym between them. Selecting C2 for Dimension C reflects `ACCEPT_SUBGOAL`'s absence from System Design §5.4's general intervention list, System Design §5.2's own diagram treating Subgoal acceptance as a separate transition trigger from the general intervention list, and the human authority's explicit selection recorded on GitHub Issue #17. ADR-DOMAIN-001 D1-E's "user command" requirement is satisfied under either C1 or C2 and does not independently favor C2 over C1.

## Positive consequences

- The D1.2 Goal-state and intervention-action wire vocabularies are fully specified and traceable to both accepted baselines.
- Neither the Charter nor the System Design is treated as superseded; the mapping tables make the correspondence explicit and reviewable.
- `ACCEPT_SUBGOAL`'s classification is resolved without inventing command schema details.
- A future Delivery D1.2 implementation batch, delivered under Issue #16's revised and separately approved implementation plan, can proceed to schema-level work without needing to re-litigate these three questions.
- The `FINAL_CANDIDATE`/`STOPPED` boundary and the Delivery D5 exclusion of `ACCEPTED`/`PUBLISHING`/`COMPLETED` remain intact.

## Negative consequences and risks

- Contributors reading the Charter narrative need to consult this ADR's mapping table to find the corresponding D1 wire token, rather than finding it directly in the Charter.
- The Decision B union vocabulary is one token larger than either single-source option, though this is presented as a benefit (no dropped term) rather than pure cost.
- C2's dedicated-command-intent classification means Issue #16's future revised D1.2 implementation batch must define two command families (general intervention and Subgoal acceptance) instead of one.

## Dependency impact

No dependency impact. This ADR adds, removes, or changes no dependency, and does not reopen ADR-DOMAIN-001's approval of `pydantic==2.13.4` for `libs/contracts`.

## Security impact

No authentication or authorization subsystem is introduced or implemented by this ADR. `USER` normative authority is preserved for Subgoal acceptance and all other user-reserved actions; no wire token or classification decided here grants human authority to `SYSTEM`, `SCIENTIST`, `SA`, or a Moderator label. Any actor-attribution field a future D1.2 schema carries (e.g., `actor: ActorRef`) remains data only; this ADR does not authorize a contract-layer (Pydantic) validator to enforce `USER`-only authorization or any other role-authorization or legal-transition behavior — that responsibility remains with `mnemograph_domain` and the future application layer.

## Data and migration impact

No persistence design, migration, or data model is authorized by this ADR. The vocabulary decided here is a contract-wire naming convention only; it does not select a database, storage technology, or migration path.

## Operational impact

No runtime orchestration, API route, worker behavior, or Compose change is authorized by this ADR. Delivery D1.2 implementation remains unauthorized. GitHub Issue #16 remains Approved for planning only; this ADR resolves the vocabulary-level blocking questions previously identified for Issue #16's future revised implementation plan. This Accepted ADR does not itself authorize implementation and does not require a different or additional implementation issue.

## Validation strategy

For this Accepted ADR:

- Verify this ADR's status is Accepted everywhere it is indexed or described.
- Verify the Decision A enum contains exactly the nine listed tokens and excludes `ACCEPTED`, `PUBLISHING`, `COMPLETED`.
- Verify the Decision B enum contains exactly the seven listed tokens and excludes `ACCEPT_SUBGOAL`.
- Verify this ADR does not modify, supersede, or reinterpret ADR-DOMAIN-001 or ADR-DOMAIN-002, and does not alter the `ActorKind` value set or Moderator semantics.
- Verify no baseline, dependency, lockfile, or implementation artifact is changed by this ADR.
- Verify ADR acceptance has not changed Issue #16's Approved-for-planning-only status or authorized Delivery D1.2 implementation.

If Issue #16's revised implementation plan is later separately approved by explicit human authority, future contract tests should verify: the exact Decision A and Decision B wire-token sets (including absence of Delivery D5 values and absence of `MODERATOR`); that `ACCEPT_SUBGOAL` does not appear in the intervention/checkpoint-action enum; that any Subgoal-acceptance command requires `expected_version`; and that no contract-layer validator encodes `USER`-only or other actor-based authorization. No implementation or test change is authorized by this ADR itself.

## Rollback or recovery

If a later accepted decision requires a different vocabulary or classification, it must be recorded through a superseding ADR with explicit human approval. This ADR does not alter ADR-DOMAIN-001 or ADR-DOMAIN-002.

## Rejected alternatives

This Accepted ADR's decision does not select, for each dimension, the following options recorded in Issue #17. This Accepted ADR supersedes no artifact; an option "not selected" here is not thereby superseded, deprecated, or rejected as a matter of record — it is simply not the option chosen by the human authority's accepted decision on Issue #17.

- Dimension A: A1 (Charter verbatim) and A3 (new reconciled vocabulary) are not selected under this accepted decision; A-Defer is not selected under this accepted decision.
- Dimension B: B1 (Charter verbatim, dropping `CORRECT_CONTEXT`) and B2 (System Design verbatim, dropping `CONTINUE`) are not selected under this accepted decision; B-Defer is not selected under this accepted decision.
- Dimension C: C1 (intervention-enum member) is not selected under this accepted decision; C-Defer is not selected under this accepted decision.

## Open questions

- Should a later D1.2 implementation plan fix a specific presentation order for the Decision B enum, or leave it non-semantic as stated here?
- What exact command schema will Issue #16's future revised D1.2 implementation batch define for the `ACCEPT_SUBGOAL` dedicated command intent, and will it also cover Subgoal reopening?

## Traceability to implementation and tests

This Accepted ADR creates no implementation work by itself. If Issue #16's revised implementation plan is later separately approved by explicit human authority, traceability should include:

- contract-schema evidence that the Goal-state enum contains exactly the Decision A tokens;
- contract-schema evidence that the intervention/checkpoint-action enum contains exactly the Decision B tokens and excludes `ACCEPT_SUBGOAL`;
- a distinct Subgoal-acceptance command schema requiring `expected_version`, per Decision C;
- absence of any contract-layer actor-authorization validator; and
- confirmation that `ACCEPTED`, `PUBLISHING`, and `COMPLETED` do not appear in the D1 public contract surface.

## Human approval record

- Status: Accepted
- Accepted decisions: A2 / B3 / C2
- Decision authority: Human project owner
- Lead-SA review: Approved
- Acceptance date: 2026-07-18
- Delivery D1.2 remains implementation-unauthorized.
- Issue #16 remains Approved for planning only. It requires a revised full implementation plan and a separate, explicit human implementation approval before Delivery D1.2 implementation proceeds. No additional or different implementation issue is implied unless the human authority changes or decomposes Issue #16's scope.

## Supersession record

None. This ADR does not supersede ADR-DOMAIN-001, ADR-DOMAIN-002, ADR-GOV-001, any accepted baseline, or any option recorded in Issue #17. It does not modify or reinterpret ADR-DOMAIN-001 or ADR-DOMAIN-002; it only clarifies the contract-vocabulary mapping while preserving both ADRs' normative semantics.
