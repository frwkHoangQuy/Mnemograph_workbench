# ADR-DOMAIN-001: Pure Domain and Published Contract Boundaries

Status: Accepted

Date: 2026-07-17

Deciders: project owner, Lead SA

Related issue: Delivery D1 planning record

Related baseline sections:

- Project Charter §§8, 13
- System Design §§4, 5, 7.3, 8.4, 10, 11.1, 15

Delivery scope: Delivery D1 — Domain & Contracts

## Context and problem

Delivery D1 must establish the pure domain and published contract boundaries for the workbench without introducing implementation code. The accepted baselines describe durable state ownership, state-machine discipline, structured outputs, and dependency boundaries, but the repository skeleton still contains generic placeholder import packages for `domain` and `contracts`.

This ADR records the approved boundary decisions for D1.

This ADR does not modify, override, or reorder either accepted baseline.

## Constraints

- Delivery D1 is a planning boundary, not an implementation authorization.
- Domain logic must remain dependency-free from frameworks, databases, queues, storage clients, and model-provider SDKs.
- Published contracts may validate transport shapes, but they must not absorb inward application/domain ports.
- The repository has no production consumer yet, so D1 may rename import modules without compatibility aliases.

## Decision drivers

- Keep domain logic pure and deterministic.
- Keep published contracts stable and transport-focused.
- Prevent framework and serialization concerns from leaking into the domain layer.
- Preserve a clean dependency arrow toward inward ports only.
- Make the first implementation batch small, testable, and reversible.

## Facts and evidence

- Project Charter §8 requires durable, replayable deliberation and human-controlled normative change.
- Project Charter §13 frames the capability roadmap that D1 supports.
- System Design §§4 and 5 define bounded modules and state-machine discipline.
- System Design §7.3 requires structured outputs to be parsed and validated before they become draft domain state.
- System Design §8.4 specifies append-only audit behavior and replay via snapshots/versioning rather than full event sourcing.
- System Design §10 describes the current MVP technology baseline with Python backend and explicit contracts.
- System Design §11.1 prohibits domain imports of web frameworks, database clients, or model SDKs.
- System Design §15 defines Delivery D1 as Domain & Contracts.
- The human approval for ADR-DOMAIN-001 was recorded on 2026-07-17 by the project owner and Lead SA.

## Assumptions

- Domain and contracts packages are still skeletons and do not yet expose real behavior.
- D1 will introduce only pure model and contract surfaces, not persistence or runtime orchestration.
- Tests may import both packages to verify semantic and wire-value compatibility once D1 begins.
- Future API and worker adapters can depend on both domain and contracts, but not the reverse.

## Options considered

1. Retain generic import modules.
2. Use a shared mnemograph namespace package across distributions.
3. Put Pydantic models directly in domain.
4. Make contracts import domain entities.
5. Put provider/application ports in contracts.
6. Implement the complete D5 publication lifecycle during D1.

## Trade-off comparison

| Option | Benefit | Risk |
|---|---|---|
| Retain generic import modules | No immediate rename work | Collision-prone, unclear, and hard to enforce boundary ownership |
| Shared namespace package across distributions | Common top-level naming | Adds indirection without solving ownership separation |
| Pydantic directly in domain | Easy validation reuse | Leaks framework/serialization concerns into pure domain logic |
| Contracts import domain entities | Fewer duplicate shapes | Couples transport compatibility to internal implementation details |
| Put ports in contracts | Centralizes interfaces | Moves inward application concerns into a published DTO package |
| Implement D5 publication in D1 | Appears to reduce future work | Violates the D1 boundary and collapses later delivery phases |

## Decision

### D1-A — Python package identities

- Distribution names remain:
  - `mnemograph-domain`
  - `mnemograph-contracts`
- Import modules will become:
  - `mnemograph_domain`
  - `mnemograph_contracts`
- The current generic `domain` and `contracts` imports are D0 placeholders, not violations of an earlier namespaced-import mandate.
- D1.1 will rename the import modules before domain behavior is added.
- No compatibility aliases will be created because no production consumer exists yet.

### D1-B — Representation boundary

- `mnemograph_domain` uses Python standard-library types only.
- Domain implementation may use frozen dataclasses, enums, `NewType`, `UUID`, timezone-aware `datetime`, and `typing.Protocol`.
- Domain must not import Pydantic, FastAPI, database clients, queue/storage clients, or model-provider SDKs.
- `mnemograph_contracts` uses Pydantic v2 for strict transport validation and JSON Schema generation.
- `pydantic==2.13.4` is explicitly approved as a direct dependency of `libs/contracts`.
- This approval is limited to `libs/contracts` and does not authorize any other dependency change.

### D1-C — Dependency direction

- `domain` does not depend on `contracts`.
- `contracts` does not import domain implementation modules.
- Future API/worker adapters or mapper layers may depend on both domain and contracts.
- Application/domain ports must not be placed in published contracts.
- If D1 needs a port for deterministic participant/model fakes, it must be a stdlib `typing.Protocol` owned by the inward domain/application boundary.
- Tests may import both packages to verify semantic enum and wire-value compatibility.
- Domain has no dependency arrow to external systems; external adapters implement inward-facing ports.

### D1-D — Primitive conventions

- Entity-specific identifiers use `typing.NewType` over `uuid.UUID`.
- Contract representations expose UUID-compatible wire values.
- Timestamps are timezone-aware `datetime` values normalized to UTC.
- Naive `datetime` values are rejected.
- Aggregate versions are non-negative integers.
- Every mutating command carries `expected_version`.
- Successful state mutation increments the aggregate version exactly once.
- `ActorKind` and `ActorRef` represent `USER`, `SCIENTIST`, `SA`, and `SYSTEM` identities at the domain level.
- `ActorRef` is not authentication or authorization implementation.
- Authentication providers and persistence identifiers remain out of Delivery D1 scope.

### D1-E — State ownership and phase boundary

- `Goal` owns decomposition, approved-plan linkage, and overall progress through `FINAL_CANDIDATE` or `STOPPED`.
- `Subgoal` has an independently testable lifecycle and may be accepted or reopened only by a user command.
- `Goal` may enter `CROSS_GOAL_REVIEW` only after all required subgoals satisfy their acceptance guard.
- `DeliberationSession` owns immutable turns, checkpoints, interventions, pause/resume behavior, and branch history.
- `Claim`, `EvidenceLink`, and `ArchitectureIssue` remain distinct records/contracts aligned with their bounded-module ownership.
- Delivery D1 emits immutable transition records but does not implement persistence or audit-event storage.
- `FINAL_CANDIDATE` is the Delivery D1 handoff boundary.
- Acceptance, `FinalAcceptedProposal` behavior, publishing, and completion transitions belong to Delivery D5.
- Delivery D1 must not implement `ACCEPTED`, `PUBLISHING`, or `COMPLETED` behavior merely for enum compatibility.
- D1 structural validation may validate identifier shape and local linkage.
- Existence checks against stored referenced entities belong to a future application/repository boundary.

## Rationale

Generic top-level imports `domain` and `contracts` are collision-prone and unclear. Separate pure-domain and published-contract representations prevent Pydantic and framework concerns from leaking into domain logic. Contract/domain independence protects published schema compatibility. Ports belong at inward domain/application boundaries, not DTO packages. Aggregate ownership prevents a single oversized state machine from absorbing decision and publication behavior. These decisions refine implementation boundaries without modifying or overriding either accepted baseline.

## Positive consequences

- The domain layer stays pure and testable with standard-library types.
- Published contracts can validate transport shapes without entangling domain internals.
- Future adapters have a clear dependency path inward to domain/application ports.
- The D1 implementation plan can be split into narrow, reviewable batches.

## Negative consequences and risks

- D1.1 must rename import modules and update import tests atomically.
- Contract validation semantics become more explicit and may require additional adapter mapping.
- The current generic placeholder import modules must be retired before behavior is added.
- Contract and domain type duplication may need careful coordination to avoid drift.

## Dependency impact

- `libs/contracts` receives an approved direct dependency on `pydantic==2.13.4`.
- No other dependency change is approved by this ADR.
- Domain remains standard-library only.

## Security impact

This ADR does not introduce security behavior. It reduces boundary ambiguity by keeping domain state pure and preventing provider, persistence, and transport code from entering the domain package.

## Data and migration impact

No data or migration impact is authorized by this ADR.

## Operational impact

D1.1 must update wheel package paths and import tests atomically. D1 structural validation may only check local shape and linkage; existence checks remain future application/repository work. The ADR itself does not authorize implementation code.

## Validation strategy

- Dependency-boundary tests must reject prohibited imports.
- Contract tests must verify JSON Schema and wire-enum compatibility.
- State-machine tests must cover legal transitions, rejected transitions, actor guards, and stale `expected_version`.
- Import tests must verify the namespaced modules once D1.1 begins.
- No source code or package change is performed by this ADR task.

## Rollback or recovery

If the boundary decisions need revision, a superseding ADR must record the change with explicit human approval. Until then, the accepted baselines and this ADR remain in force.

## Rejected alternatives

- Retain generic import modules.
- Use a shared mnemograph namespace package across distributions.
- Put Pydantic models directly in domain.
- Make contracts import domain entities.
- Put provider/application ports in contracts.
- Implement the complete D5 publication lifecycle during D1.

## Open questions

None.

## Traceability to implementation and tests

- D1.1 package-path updates and import tests establish the namespaced module transition.
- Domain invariants map to deterministic state-machine tests with stale-version and actor-guard coverage.
- Contract validation maps to JSON Schema and wire-enum tests.
- Boundary enforcement maps to import-graph tests.

## Human approval record

Approved by the project owner and Lead SA on 2026-07-17.

## Supersession record

None.
