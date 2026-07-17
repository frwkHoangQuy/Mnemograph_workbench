---
description: "Next.js App Router, strict TypeScript, and placeholder web behavior"
applyTo: "apps/web/**"
---

- Use Next.js App Router and strict TypeScript.
- Prefer server components by default.
- Add "use client" only when demonstrated interaction requires it.
- Web code must not access the database, queue, storage or model provider directly.
- Consume published API contracts only.
- Accessibility and semantic HTML are required.
- No remote fonts or network access in deterministic tests or builds.
- Use exact dependency pins only.
- Run focused web format, lint, typecheck and test before root validation.
- Current Phase 0 behavior remains a static placeholder.
