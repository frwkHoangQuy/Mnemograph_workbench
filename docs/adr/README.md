# ADRs

This directory holds architecture decision record guidance for this repository.

An ADR captures a human-reviewed architecture decision, its context, trade-offs, consequences, validation and traceability. It is a normative record only after explicit human approval.

The seven already accepted ADRs remain authoritative only in System Design §16. Phase 0 does not transcribe them into individual ADR files.

Future ADR files start as Proposed and require explicit human approval before they can become Accepted. An ADR proposal issue is not the accepted ADR document.

Status lifecycle: Proposed, Accepted, Rejected, Superseded.

Future file naming convention: ADR-<CATEGORY>-<NUMBER>-<short-title>.md.

Relationship to the delivery flow:

- ADRs establish or record architecture decisions.
- Implementation issues describe bounded work to satisfy approved decisions.
- Approved plans break the work into reviewable batches.
- Code and tests provide execution evidence against the approved plan.

Reference files:

- [ADR template](template.md)
- [System Design](../baseline/Mnemograph_Triadic_Research_Workbench_System_Design_v0.1.md)
- [ADR proposal issue template](../../.github/ISSUE_TEMPLATE/adr-proposal.md)
