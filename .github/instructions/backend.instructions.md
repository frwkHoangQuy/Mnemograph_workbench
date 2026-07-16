---
description: "Python API and worker boundaries, strict typing, and Phase 0 placeholder behavior"
applyTo: "apps/api/**,apps/worker/**"
---

- Use Python 3.13 with strict typing.
- API and worker must not own domain decisions.
- External systems must eventually be accessed through explicit ports and adapters.
- No database, queue, storage or model client is authorized in Phase 0.
- API currently exposes GET /health only.
- Worker currently emits one deterministic readiness line only.
- Tests require no external services.
- Maintain Ruff, Mypy and pytest compliance.
- Use exact dependency pins only.
