# ADR-DOMAIN-002: Delivery D1.2 Schema Scope and Moderator Semantics

## ADR ID

ADR-DOMAIN-002

## Title

Delivery D1.2 Schema Scope and Moderator Semantics

## Status

Proposed

## Date

2026-07-18

## Deciders

Pending explicit human approval

## Related issue

[GitHub Issue #14](https://github.com/frwkHoangQuy/Mnemograph_workbench/issues/14)

## Related baseline sections

- [Project Charter](../baseline/Mnemograph_Triadic_Research_Workbench_Project_Charter_v1.0.md) Sections 2, 4, 8, 10, 11, and 13.
- [System Design](../baseline/Mnemograph_Triadic_Research_Workbench_System_Design_v0.1.md) Sections 2, 4, 5, 7.3, 10, 11.1, and 15.
- [ADR-GOV-001: Phase Namespace Reconciliation](ADR-GOV-001-phase-namespace-reconciliation.md).
- [ADR-DOMAIN-001: Pure Domain and Published Contract Boundaries](ADR-DOMAIN-001-pure-domain-and-published-contract-boundaries.md), especially D1-D and D1-E.
- [North Star System Vision](../vision/north-star-system-vision-v1.0.md) Sections 6, 8 through 10, 18, and 21.
- [North Star Architecture Impact Assessment](../architecture/north-star-impact-assessment-v0.1.md) Sections 5, 8, 9, 16 through 18, 22, and 23.

## Delivery scope

Delivery D1.2 clarification only.

> **Proposed and non-normative:** This draft has no authority until explicitly accepted by an authorized human. It does not authorize Delivery D1.2 implementation, and Delivery D1.2 remains frozen. The accepted baselines and accepted ADRs remain authoritative. This draft does not modify or supersede ADR-DOMAIN-001.

## Context and problem

The exact first MVP includes Scientist, SA, and Moderator roles in one standalone room. ADR-DOMAIN-001 defines the Delivery D1 domain actor values as `USER`, `SCIENTIST`, `SA`, and `SYSTEM`. The candidate North Star Vision and Architecture Impact Assessment identify a vocabulary clarification: Moderator is visible in the first-MVP user experience, but the current four `ActorKind` values do not name a separate Moderator actor.

This draft asks how a future, separately approved Delivery D1.2 schema foundation could express that exact first-MVP distinction without expanding the domain actor vocabulary, creating a generic role platform, or treating a user-facing role label as human authority.

The question is deliberately narrow. It does not decide runtime orchestration, a Room aggregate, role management, provider selection, tool permissions, memory, federation, persistence, publication, or any other future North Star capability.

## Constraints

- This ADR is Proposed and non-normative until explicitly accepted by an authorized human.
- GitHub Issue #14 authorizes ADR drafting only; it does not accept this proposed decision or authorize Delivery D1.2 implementation.
- Delivery D1.2 remains frozen.
- The Project Charter, System Design, ADR-GOV-001, and ADR-DOMAIN-001 remain authoritative.
- This draft must not modify, supersede, or reinterpret ADR-DOMAIN-001.
- Delivery D1 remains bounded at `FINAL_CANDIDATE`; acceptance, publication, and completion remain Delivery D5 concerns.
- The domain remains Python-standard-library-only, and published contracts retain the Pydantic boundary already established by ADR-DOMAIN-001.
- No dependency, lockfile, source-code, migration, workflow, or implementation change is authorized by this documentation batch.

## Decision drivers

- Reconcile the visible first-MVP Moderator role with the existing four domain `ActorKind` values.
- Preserve explicit user authority for approval, acceptance, stopping, reopening, and normative changes.
- Keep Scientist and SA attributable as content authors.
- Avoid premature generic role abstractions or a fifth domain actor kind.
- Preserve `Role != Model` and keep role semantics separate from model, provider, and tool selection.
- Keep Delivery D1.2 a strict schema foundation for already approved Delivery D1 concepts only.
- Avoid hard-coding future North Star options into early contracts.

## Facts and evidence

- ADR-DOMAIN-001 D1-D defines `ActorKind` and `ActorRef` for exactly `USER`, `SCIENTIST`, `SA`, and `SYSTEM` identities at the domain level.
- ADR-DOMAIN-001 D1-E gives Goal, Subgoal, and DeliberationSession separate state ownership and stops Delivery D1 at `FINAL_CANDIDATE`.
- The System Design separates Deliberation, Scientific Reasoning, Architecture Review, Decision and Normative Governance, Publication, Model Gateway, and Audit responsibilities.
- The North Star Vision preserves Scientist, SA, and Moderator roles in the exact first MVP, treats future role diversity as candidate-only, and states that a role is not a model.
- The Architecture Impact Assessment identifies Moderator representation as a clarification required before any future D1.2 resumption and warns against generic role management, a Room aggregate, governed memory, federation, or Delivery D5 behavior in D1.2.
- GitHub Issue #14 is supplied as Lead-SA-verified approval for ADR drafting only.

### Scientific evidence boundary

Scientific sourcing is not applicable to this decision. This ADR makes no scientific claim, does not invent citations, and does not treat model output as scientific evidence.

## Assumptions

- A future, separately approved Delivery D1.2 batch can remain limited to contract-schema clarification for already approved Delivery D1 concepts.
- The first-MVP Moderator role can be visible to users without becoming a separate domain actor kind or a human authority.
- Persisted mutation issuance and visible role identity can remain distinct without deciding runtime orchestration behavior.
- Any later need for dynamic roles, a role registry, broader tool policies, or a different actor vocabulary would require separate human review and an appropriate governance artifact.

## Options considered

### Option A: Add `MODERATOR` to `ActorKind`

Add a fifth domain actor kind for Moderator.

### Option B: Treat Moderator as a user-facing orchestration role or policy whose persisted orchestration mutations use `ActorKind.SYSTEM`

Keep the four existing `ActorKind` values. Treat Moderator as visible first-MVP orchestration semantics rather than a separate Delivery D1 domain actor kind.

### Option C: Introduce a generic role registry during Delivery D1.2

Create a generalized role registry to represent current and future role identities, capabilities, and policies.

### Option D: Defer Moderator semantics and proceed with ambiguous contracts

Leave the relation between visible Moderator behavior and persisted actor attribution unspecified while proceeding with future D1.2 work.

## Trade-off comparison

| Option | Benefit | Risk | Delivery D1.2 compatibility |
|---|---|---|---|
| A. Add `MODERATOR` to `ActorKind` | Makes the user-facing label visible in domain vocabulary | Expands an accepted actor boundary without evidence that a separate domain actor is needed | Poor; risks premature domain generalization |
| B. Moderator as visible orchestration policy with `SYSTEM` persisted mutations | Preserves the current actor values while keeping first-MVP moderation visible | Requires disciplined distinction among role identity, mutation issuer, and content author | Strong; confines the clarification to existing concepts |
| C. Generic role registry | Appears extensible for future role diversity | Creates an unapproved horizontal platform and prematurely models candidate futures | Poor; outside strict schema-foundation scope |
| D. Defer semantics and proceed ambiguously | Avoids drafting a clarification | Leaves attribution and schema meaning unclear before any future D1.2 work | Poor; does not resolve the identified ambiguity |

## Proposed decision

This draft proposes Option B for explicit human review. It is not an accepted decision and does not authorize implementation.

### Moderator semantics

- Moderator is a visible first-MVP orchestration role or policy.
- Moderator is not a human authority.
- Moderator is not a separate Delivery D1 domain actor kind.
- The only Delivery D1 domain `ActorKind` values remain `USER`, `SCIENTIST`, `SA`, and `SYSTEM`.
- D1.2 does not add `MODERATOR` to `ActorKind`.
- Persisted orchestration mutations are issued as `ActorKind.SYSTEM`.
- Scientist and SA remain attributable content authors for their respective content.
- USER retains approval, acceptance, stopping, reopening, and normative authority.
- D1.2 does not create a generic role registry.

### Distinct concepts

| Concept | Proposed first-MVP meaning | Must remain distinct from |
|---|---|---|
| Role identity | A visible user-facing purpose, such as Scientist, SA, or Moderator | Persisted mutation issuer, content author, model/provider, tool permission, and human authority |
| Persisted mutation issuer | The domain identity recorded for an orchestration mutation; Moderator orchestration uses `ActorKind.SYSTEM` | A claim that SYSTEM is a human principal or content author |
| Content author | The attributable author of content; Scientist and SA remain attributable for their content | The orchestration policy that scheduled or presented the content |
| Model/provider | A capability behind a role through the Model Gateway | Role identity, authority, and content ownership |
| Tool permissions | A separately bounded future policy concern | Actor kind, role label, model/provider choice, and human authority |
| Human authority | USER control over approval, acceptance, stopping, reopening, and normative decisions | A role label, system mutation, model behavior, or tool capability |

Role remains separate from model and provider selection. This draft selects neither a model nor a provider, and it does not authorize a tool-permission implementation.

### D1.2 scope guardrails

The proposed D1.2 boundary is a strict Pydantic contract-schema foundation for already approved Delivery D1 concepts only. It may rely on the Pydantic dependency already approved by ADR-DOMAIN-001 for `libs/contracts`; this draft does not add, remove, or modify dependencies or lockfiles.

The following are explicitly outside proposed D1.2 scope:

- Room aggregate or room topology;
- dynamic roles or a role registry;
- governed memory or memory promotion;
- room federation or cross-room exchange;
- external integrations or consequential actions;
- provider, model, tool, storage, queue, framework, cloud, or authentication selection;
- persistence and migrations;
- runtime orchestration;
- acceptance and publication behavior;
- Delivery D5 behavior; and
- source code or implementation authorization.

Delivery D1 remains bounded at `FINAL_CANDIDATE`. Acceptance, `FinalAcceptedProposal`, publication, and completion remain Delivery D5 concerns.

## Rationale

Option B preserves the accepted four-value domain actor boundary while making the first-MVP Moderator semantics explicit to future contract review. It avoids treating a visible orchestration policy as a new principal, human authority, content author, provider choice, or generic role-management foundation.

This narrow distinction supports the exact first MVP without projecting candidate North Star role diversity into Delivery D1. It also preserves the established state ownership and delivery boundary: orchestration can be attributable in persisted state through `SYSTEM`, while the user experience can identify moderation without changing the domain actor taxonomy.

## Positive consequences

- The first-MVP Scientist-SA-Moderator configuration can remain visible without adding a fifth domain actor kind.
- The existing `ActorKind` values remain stable: `USER`, `SCIENTIST`, `SA`, and `SYSTEM`.
- USER authority remains explicit and cannot be inferred from a Moderator label or system mutation.
- Scientist and SA retain attributable authorship of their content.
- Role, mutation issuer, content author, model/provider, tool permissions, and human authority stay separate.
- D1.2 can remain focused on a narrow contract-schema foundation if a later human-approved scope resumes it.
- Candidate future role diversity, rooms, memory, federation, and external action remain outside Delivery D1.

## Negative consequences and risks

- A visible Moderator label and `SYSTEM` mutation issuer may be confused unless future schema and user-facing terminology preserve the distinction.
- The proposal deliberately does not solve future dynamic roles, temporary specialists, or organizational role policy.
- A future role-policy capability may need a separate bounded context or ADR after a running MVP provides evidence.
- Treating `SYSTEM` as a mutation issuer must not be misread as granting SYSTEM human authority, content ownership, or consequential-action authority.
- Any attempt to implement more than the strict D1.2 foundation would exceed this proposed scope and require separate human approval.

## Dependency impact

No dependency impact is authorized. ADR-DOMAIN-001 already approves `pydantic==2.13.4` as a direct dependency of `libs/contracts`; this draft neither changes that approval nor authorizes any dependency or lockfile change.

## Security impact

This draft introduces no security implementation. Its proposed conceptual boundary supports least-authority reasoning by keeping Moderator separate from human authority, tool permissions, external action, provider choice, and authentication. Any security, consent, access, or tool-policy design remains outside Delivery D1.2.

## Data and migration impact

No data model, persistence design, migration, retention mechanism, or audit-storage implementation is authorized. Persisted mutation issuer is a proposed contract semantic only; it does not select a database, storage technology, or migration path.

## Operational impact

No runtime orchestration, service behavior, worker behavior, API route, provider integration, queue, or deployment change is authorized. Delivery D1.2 remains frozen pending explicit human approval, a bounded implementation issue, and an approved plan.

## Validation strategy

For this proposed ADR draft:

- Verify its status is Proposed everywhere it is indexed or described.
- Verify the proposed actor set remains exactly `USER`, `SCIENTIST`, `SA`, and `SYSTEM`.
- Verify this draft explicitly excludes adding `MODERATOR` to `ActorKind` and creating a generic role registry.
- Verify the D1.2 exclusions preserve the `FINAL_CANDIDATE` and Delivery D5 boundaries.
- Verify no baseline, accepted ADR, source, dependency, workflow, lockfile, or implementation artifact changes.

If an authorized human later accepts this proposal and separately authorizes implementation, future contract tests should verify the stated actor values, attribution distinctions, user-only authority guards, and the absence of acceptance or publication behavior in Delivery D1. No implementation or test change is authorized by this draft.

## Rollback or recovery

While Proposed, this ADR has no implementation effect and may be rejected or revised by an authorized human. If a later accepted decision requires a different boundary, it must be recorded through the applicable human-governed ADR or System Design process. This draft does not alter ADR-DOMAIN-001.

## Rejected alternatives

This draft proposes against Options A, C, and D for human review:

- Option A would expand `ActorKind` before a separate domain actor need is established.
- Option C would introduce a generic role registry before there is approved scope or evidence for one.
- Option D would preserve ambiguity in an area identified as needing clarification before any future D1.2 resumption.

These alternatives are not formally rejected unless and until an authorized human resolves this Proposed ADR.

## Open questions

- If a later D1.2 implementation is separately approved, which minimum contract field or mapping documentation, if any, is necessary to distinguish visible Moderator semantics from `ActorKind.SYSTEM` mutation attribution?
- Does a later first-MVP user-facing specification need to name Moderator as an orchestration policy explicitly, without converting that label into a domain actor kind?
- What future evidence would justify a bounded role-policy capability rather than the fixed first-MVP configuration?
- Which future governance artifact would be required before tool permissions, external action, dynamic roles, or broader authority semantics are considered?

## Traceability to implementation and tests

This proposed ADR creates no implementation work. If an authorized human later accepts it and separately authorizes a bounded D1.2 batch, traceability should include:

- contract-schema evidence that the only domain `ActorKind` values are `USER`, `SCIENTIST`, `SA`, and `SYSTEM`;
- tests or review evidence that persisted orchestration mutations use `SYSTEM` without assigning human authority to that identity;
- attributable Scientist and SA content authorship distinct from orchestration mutation issuance;
- user-only guards for approval, acceptance, stopping, reopening, and normative decisions; and
- confirmation that Delivery D1 remains at `FINAL_CANDIDATE` without acceptance, publication, or completion behavior.

## Human approval record

- Status: Pending
- Reviewer: Pending
- Approval date: Pending
- This proposed ADR has not been accepted.
- Issue #14 authorizes drafting only.
- Delivery D1.2 remains frozen.

## Supersession record

None. This proposed ADR does not supersede ADR-DOMAIN-001, any other ADR, or an accepted baseline.
