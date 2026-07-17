# Mnemograph Triadic Research Workbench

Phase 0 is a repository and governance foundation. This is not Mnemograph_Core business logic. Only operational placeholders currently exist. Scientist and SA product roles are future runtime roles and differ from development custom agents. Production readiness is not claimed.

## Current Phase 0 behavior

- web: static placeholder page
- API: GET /health only
- worker: one deterministic readiness log line
- Compose: replaceable PostgreSQL/pgvector, Valkey and MinIO local adapters

No deliberation, evidence retrieval, model gateway, persistence, queue consumption or publication feature exists yet.

## Repository layout

| Path | Current purpose |
|---|---|
| [apps/web](apps/web) | Next.js placeholder web application for the Phase 0 static page |
| [apps/api](apps/api) | FastAPI placeholder API exposing GET /health |
| [apps/worker](apps/worker) | Deterministic readiness-line worker placeholder |
| [libs/contracts](libs/contracts) | Shared Python contract package skeleton |
| [libs/domain](libs/domain) | Shared Python domain package skeleton |
| [libs/prompts](libs/prompts) | Shared prompt source package skeleton |
| [libs/model_gateway](libs/model_gateway) | Shared model-gateway package skeleton |
| [libs/evaluation](libs/evaluation) | Shared evaluation package skeleton |
| [infra/compose](infra/compose) | Replaceable local Compose adapter stack |
| [docs](docs) | Baseline, ADR and runbook documentation and indexes |
| [tests](tests) | Test-purpose indexes for future contract, integration, E2E and golden coverage |
| [.github](.github) | Repository instructions, prompts, issue templates, PR template and CI workflow |

## Prerequisites

- Node.js 24.18.0
- pnpm 11.13.1
- Python 3.13.14
- uv 0.11.28
- Docker Engine or Docker Desktop with Compose v2, optional unless local backing adapters are needed

Corepack is used for pnpm.

## Initial setup

From the repository root:

```bash
corepack enable
pnpm install --frozen-lockfile
uv sync --all-packages --locked
```

No `.env` file is required for Phase 0. All active defaults are local-development values. `.env.example` files document optional configuration only. Real secrets must never be committed.

## Deterministic local validation

Next.js telemetry must be disabled during deterministic validation.

```bash
NEXT_TELEMETRY_DISABLED=1 pnpm run validate
```

```powershell
$env:NEXT_TELEMETRY_DISABLED = "1"
pnpm run validate
```

```bash
docker compose -f infra/compose/docker-compose.yml config
```

Compose validation requires Docker and does not start containers.

## Running the Phase 0 placeholders

### Web

```bash
pnpm --filter @mnemograph/web dev
```

Default URL: `http://localhost:3000`

### API

```bash
uv run uvicorn api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 8000
```

Health endpoint: `http://127.0.0.1:8000/health`

### Worker

```bash
uv run python -m worker.main
```

This prints one readiness line and exits; it does not consume a queue.

### Local adapters

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

See [infra/compose/README.md](infra/compose/README.md) for status, logs, shutdown and destructive volume-removal warnings.

## Quality gates

| Gate | Command |
|---|---|
| formatting | `pnpm run format:check` |
| lint | `pnpm run lint` |
| type checking | `pnpm run typecheck` |
| tests | `pnpm run test` |
| builds | `pnpm run build` |
| full gate | `pnpm run validate` |
| Compose syntax | `docker compose -f infra/compose/docker-compose.yml config` |

The full root commands coordinate Node and Python validation.

## Governance and Copilot workflow

Baseline documents and accepted ADRs take precedence. Work proceeds as one approved small batch at a time. Copilot plans before implementation. Copilot never commits, pushes, merges, amends or opens a PR autonomously. A human reviews and creates the commit. The pushed repository, branch and SHA are reviewed independently before the next batch. Dependency changes require explicit approval.

References:

- [AGENTS.md](AGENTS.md)
- [.github/copilot-instructions.md](.github/copilot-instructions.md)
- [docs/baseline/README.md](docs/baseline/README.md)
- [docs/adr/README.md](docs/adr/README.md)
- [docs/runbooks/copilot-workflow.md](docs/runbooks/copilot-workflow.md)
- [.github/ISSUE_TEMPLATE/implementation-task.yml](.github/ISSUE_TEMPLATE/implementation-task.yml)
- [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)

## CI

See [.github/workflows/ci.yml](.github/workflows/ci.yml).

CI contains web, Python and Compose-validation jobs. Workflow permissions are read-only. Web CI disables Next.js telemetry. Hosted-runner verification is still required on a pull request. Do not add a status badge before the workflow has run successfully on the intended default branch.

## Development boundaries

- domain does not depend on web frameworks, database clients or model SDKs
- web consumes published API contracts
- model_gateway contains no domain decisions
- prompts are versioned and tested as source
- Compose services are replaceable local adapters
- no provider or production platform is selected by Phase 0

## Current limitations

- no authentication implementation
- no migration framework
- no queue framework/client
- no object-storage SDK
- no model-provider integration
- no Scientist/SA runtime prompts
- no retrieval/OCR/embedding/reranking implementation
- no E2E or golden dataset content
- no production deployment configuration

See the [baseline index](docs/baseline/README.md) and System Design §17 for the open decisions instead of assuming new ones here.

## GitHub repository settings note

These are external manual settings, not repository files:

- creating and selecting the intended `main` default branch
- branch protection
- required CI status checks

Do not assume these settings are already configured.
