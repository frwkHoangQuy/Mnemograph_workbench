# ADR-GOV-001: Phase Namespace Reconciliation

Status: Accepted

Date: 2026-07-17

Deciders: project owner, SA

Related issue: Human-approved ADR-GOV-001 reconciliation record

Related baseline sections:

- Project Charter §13
- System Design introduction
- System Design §15

## Context and problem

The Project Charter and the System Design use phase terminology for different purposes. The Project Charter §13 describes high-level product capability stages, while the System Design introduction states that the baseline is intended to be implemented through its phases and §15 decomposes delivery work into repository phases. Without a reconciliation, unqualified wording such as "Phase 1" can be ambiguous in issues, branches, implementation plans, commits, and pull requests.

This ADR records the human-approved namespace reconciliation. It does not modify, override, or reorder either accepted baseline.

## Constraints

- The accepted Project Charter and accepted System Design remain immutable normative baselines.
- This ADR may record terminology and scope reconciliation, but it has no authority to rewrite baseline meaning.
- Repository work must stay reviewable and use the approved delivery vocabulary.

## Decision drivers

- Preserve the distinction between capability roadmap language and implementation decomposition.
- Remove ambiguity from planning and governance artifacts.
- Keep baseline references intact while making repository delivery language explicit.

## Facts and evidence

- Project Charter §13 defines the capability roadmap.
- System Design introduction states the baseline is approved for implementation through phases.
- System Design §15 defines the repository delivery decomposition.
- Human approval for ADR-GOV-001 was recorded on 2026-07-17 by the project owner/SA.

## Assumptions

- Future repository work should refer to the delivery decomposition in System Design §15.
- Future references to the Charter should keep the Charter capability labels intact.
- No additional phase namespaces are required by this reconciliation.

## Options considered

1. Keep a single unqualified "Phase N" vocabulary.
2. Rename the baselines to share one unified phase namespace.
3. Separate the namespaces and require qualified references for Charter and delivery work.

## Trade-off comparison

| Option | Benefit | Risk |
|---|---|---|
| Single unqualified phase vocabulary | Simple wording | High ambiguity across baseline and repository usage |
| Unified baseline namespace | Fewer labels | Would require modifying accepted baseline meaning |
| Qualified C# and D# namespaces | Clear separation of scopes | Requires discipline in repository guidance |

## Decision

1. Project Charter §13 phases are high-level product capability stages.
   They use the qualified namespace:
   - Charter C0 — Governance & Contracts
   - Charter C1 — Evidence Vertical Slice
   - Charter C2 — Triadic Conversation
   - Charter C3 — Governance & Publication

2. System Design §15 phases are repository delivery phases.
   They use the qualified namespace:
   - Delivery D0 — Repository & Copilot Governance
   - Delivery D1 — Domain & Contracts
   - Delivery D2 — Evidence Vertical Slice
   - Delivery D3 — Scientist Vertical Slice
   - Delivery D4 — SA & Triadic Orchestration
   - Delivery D5 — Governance & Publication
   - Delivery D6 — Evaluation & Hardening

3. Repository issues, branches, implementation plans, commits and PRs must use the Delivery D# namespace from System Design §15.

4. New project documents must not use an unqualified expression such as "Phase 1".
   They must identify either a Charter Capability Stage C# or Repository Delivery Phase D#.

5. The next repository delivery target is Delivery D1 — Domain & Contracts.
   This statement does not authorize implementation without a separately approved issue and plan.

6. This ADR does not modify, override or reorder either accepted baseline.
   It disambiguates two phase namespaces whose scopes differ.

### Required mapping table

| Charter capability stage | Repository delivery mapping |
|---|---|
| Charter C0 — Governance & Contracts | Delivery D0 — Repository & Copilot Governance plus Delivery D1 — Domain & Contracts |
| Charter C1 — Evidence Vertical Slice | Delivery D2 — Evidence Vertical Slice plus Delivery D3 — Scientist Vertical Slice |
| Charter C2 — Triadic Conversation | Delivery D4 — SA & Triadic Orchestration |
| Charter C3 — Governance & Publication | Delivery D5 — Governance & Publication |
| No separately named Charter stage | Delivery D6 — Evaluation & Hardening |

## Rationale

The approved baselines already describe different concerns. The Charter expresses the product capability roadmap, and the System Design expresses the implementation and delivery decomposition. Qualifying the namespaces preserves both meanings and prevents future planning artifacts from collapsing distinct scopes into one ambiguous label.

## Positive consequences

- Future planning artifacts can refer to delivery work unambiguously.
- Charter references remain aligned with the product capability roadmap.
- Implementation discussions can distinguish roadmap intent from delivery sequencing.

## Negative consequences and risks

- Existing unqualified wording must be updated when encountered.
- Editors and reviewers must pay attention to the namespace prefix.
- Any future failure to use the qualified forms can reintroduce ambiguity.

## Dependency impact

No dependency changes are introduced by this ADR.

## Security impact

No direct security change is introduced. The main security-adjacent benefit is reduced governance ambiguity in review and planning artifacts.

## Data and migration impact

No data or migration impact.

## Operational impact

Repository guidance, issue templates, and future planning must use the D# delivery namespace. The existing D0 operational placeholders remain in place until a separately approved D1 batch changes them.

## Validation strategy

- Confirm the ADR text contains the explicit non-override statement.
- Confirm all repository-facing guidance uses C# and D# terminology where required.
- Confirm no baseline document is modified.
- Confirm the issue template only exposes delivery terminology for repository planning.

## Rollback or recovery

If the reconciliation needs to be revised, a superseding ADR must be recorded with explicit human approval. The accepted baselines remain unchanged.

## Rejected alternatives

- Retain ambiguous unqualified phase wording.
- Rewrite the accepted baselines to share one namespace.
- Treat repository delivery work as if it were the same thing as the Charter capability roadmap.

## Open questions

None.

## Traceability to implementation and tests

- ADR-GOV-001 establishes the terminology used by issue templates, plans, branches, commits, and PRs.
- Validation should confirm the repository guidance files reference the qualified namespaces and do not alter the accepted baselines.

## Human approval record

Approved by the project owner/SA on 2026-07-17.

## Supersession record

None.
