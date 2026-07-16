# Local Compose Stack

This stack is a replaceable local-development adapter only. It does not select a production database deployment, close the queue implementation decision, select a production object-storage provider, authorize application SDKs or clients, or establish production credentials or topology.

## Prerequisites

- Docker Engine or Docker Desktop with Compose v2

## Defaults

The stack uses non-production defaults when no `.env` file is present:

- PostgreSQL database: `mnemograph`
- PostgreSQL user: `mnemograph`
- PostgreSQL password: `changeme_local_only`
- PostgreSQL host port: `5432`
- Valkey host port: `6379`
- MinIO root user: `mnemograph`
- MinIO root password: `changeme_local_only`
- MinIO API port: `9000`
- MinIO console port: `9001`

## Local endpoints

- PostgreSQL: `127.0.0.1:5432`
- Valkey: `127.0.0.1:6379`
- MinIO API: `127.0.0.1:9000`
- MinIO console: `127.0.0.1:9001`

## Validation

From the repository root:

```bash
docker compose -f infra/compose/docker-compose.yml config
```

## Startup

From the repository root:

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

## Status and logs

From the repository root:

```bash
docker compose -f infra/compose/docker-compose.yml ps
docker compose -f infra/compose/docker-compose.yml logs -f
```

## Shutdown

From the repository root:

```bash
docker compose -f infra/compose/docker-compose.yml down
```

## Remove data volumes

This is destructive and permanently deletes local Compose data volumes:

```bash
docker compose -f infra/compose/docker-compose.yml down -v
```

## PostgreSQL extension bootstrap

`infra/compose/init/001-init-extensions.sql` initializes the local PostgreSQL container with the `vector` extension only. It is bootstrap for local infrastructure, not an application migration.

## Out of scope

- Application containers are out of scope.
- SDK integrations are out of scope.
- Production deployment decisions are out of scope.
