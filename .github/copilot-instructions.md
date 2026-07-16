# Copilot Instructions

## Project Summary

Mnemograph Triadic Research Workbench is a phased repository foundation for the workbench. Phase 0 currently contains only repository skeletons, static placeholder runtime behavior, and replaceable local-development infrastructure.

## Current Boundary

Phase 0 stays within the operational-placeholder exception:

- web static placeholder page
- API GET /health
- worker deterministic readiness line

Scientist and SA are future runtime product roles. Development custom agents are repository implementation assistants. Copilot must not impersonate a Scientist or SA participant.

## Repository Layout

- apps/web
- apps/api
- apps/worker
- libs/contracts
- libs/domain
- libs/prompts
- libs/model_gateway
- libs/evaluation
- infra/compose
- infra/migrations

## Current Technology

- Node.js 24.18.0
- pnpm 11.13.1
- Turborepo 2.10.5
- Next.js 16.2.10
- React 19.2.7
- Python 3.13.14
- uv 0.11.28
- FastAPI 0.139.2
- Pydantic 2.13.4
- pytest 9.1.1
- Vitest 4.1.10

## Primary Commands

- pnpm install --frozen-lockfile
- uv sync --all-packages --locked
- pnpm run validate
- docker compose -f infra/compose/docker-compose.yml config

## References

- [AGENTS.md](../AGENTS.md)
- [Project Charter](../docs/baseline/Mnemograph_Triadic_Research_Workbench_Project_Charter_v1.0.md)
- [System Design](../docs/baseline/Mnemograph_Triadic_Research_Workbench_System_Design_v0.1.md)

## Explicit Constraints

- The baseline is immutable.
- Exact dependency pins require approval.
- Local Compose services are replaceable adapters.
- Scientist/SA product roles differ from development agents.
- Copilot stops for human review and does not commit autonomously.
