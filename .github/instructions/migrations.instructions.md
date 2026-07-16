---
description: "Infrastructure migration boundaries and ADR-gated database evolution"
applyTo: "infra/migrations/**"
---

- No migration framework is selected in Phase 0.
- Do not add executable migrations before an ADR.
- Compose init SQL is infrastructure bootstrap, not an application migration.
- Never create destructive or irreversible migration commands autonomously.
- Every future migration needs forward, rollback and data-risk analysis.
- Never place secrets or production credentials in migration files.
