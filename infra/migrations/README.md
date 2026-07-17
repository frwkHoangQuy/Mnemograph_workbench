# Migrations

No migration framework is selected in Phase 0. Alembic versus another migration approach remains an open ADR decision.

`001-init-extensions.sql` is infrastructure bootstrap only. It is not an application migration.

Application schema migrations must not be added before the migration decision is made.

This directory intentionally contains no executable migration.
