---
description: "Deterministic tests, import boundaries, and repository validation"
applyTo: "tests/**,**/tests/**,**/*.test.ts,**/*.test.tsx,**/test_*.py"
---

- Tests must be deterministic and isolated.
- Phase 0 tests use no external services.
- Test actual installed or src packages, not wrapper modules.
- Import Vitest functions explicitly.
- Python tests must pass with warnings treated as errors.
- Do not weaken or delete assertions to make a gate pass.
- Add regression coverage for every corrected defect.
- Later domain tests must prioritize invariants and state transitions.
- Full root validation remains mandatory after focused tests.
