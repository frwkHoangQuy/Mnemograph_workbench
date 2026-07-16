## Summary

- Outcome:
- Why the change is needed:

## Governance references

- Related implementation issue:
- Approved plan and batch:
- Related ADRs:
- Implementation phase:

## Scope

- Files/modules changed:
- Explicit exclusions:
- Confirmation that no unrelated changes are included:

## Acceptance criteria mapping

| Acceptance criterion | Evidence |
|---|---|

## Validation checklist

- [ ] focused tests passed
- [ ] pnpm install --frozen-lockfile
- [ ] uv sync --all-packages --locked
- [ ] pnpm run validate
- [ ] docker compose config when Compose changed
- [ ] migration validation when migrations changed
- [ ] git diff --check
- [ ] manual verification where applicable

## Governance and safety checklist

- [ ] baseline documents are unchanged
- [ ] accepted ADRs are not silently reinterpreted
- [ ] no direct dependency was added, removed or upgraded without approval
- [ ] lockfiles were package-manager generated
- [ ] pnpm allowBuilds was not broadened without approval
- [ ] no secrets or credentials are committed
- [ ] local Compose services remain replaceable adapters
- [ ] Scientist/SA product roles were not confused with development agents
- [ ] no out-of-phase feature or scope drift was introduced
- [ ] destructive or irreversible changes are identified
- [ ] Copilot did not autonomously commit, push, merge or open the PR

## Risk and recovery

- Risks:
- Rollback/recovery:
- Migration/data-loss considerations:

## Review record

- test-reviewer result:
- security-reviewer result:
- Remaining blockers:
- Explicit human approval: