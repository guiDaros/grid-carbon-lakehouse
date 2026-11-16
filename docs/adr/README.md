# Architecture Decision Records

Format: Context → Decision → Alternatives considered → Consequences (positive and negative) → Revisit when.
Status values: Proposed, Accepted, Superseded by ADR-XXXX.

| ADR | Title | Status |
|---|---|---|
| [0001](0001-delta-lake-table-format.md) | Delta Lake (via delta-rs) as the table format | Proposed (spike) |
| [0002](0002-batch-not-streaming.md) | Hourly micro-batch, no streaming | Accepted |
| [0003](0003-airflow-local-container-apps-jobs-prod.md) | Airflow locally, Container Apps Jobs in prod | Accepted |
| [0004](0004-duckdb-incremental-spark-backfill.md) | DuckDB for incremental, Spark only for backfill | Proposed (benchmark) |
| [0005](0005-late-and-revised-data.md) | Late-arriving and revised data | Accepted |
| [0006](0006-ai-layer-semantic-only.md) | AI restricted to semantic layer + evals | Accepted |
| [0007](0007-environments-local-and-prod.md) | Only local and prod environments | Accepted |
| [0008](0008-static-dashboard-evidence.md) | Static dashboard with Evidence.dev | Accepted |
| [0009](0009-single-delta-writer.md) | delta-rs as single Delta writer; publish gold step | Proposed (spike) |
| [0010](0010-ops-metadata-in-delta.md) | Ops metadata in Delta, not cloud Postgres | Accepted |
| [0011](0011-local-storage-and-azurite.md) | Local filesystem, Azurite for tests, ADLS in prod | Accepted |
| [0012](0012-logging-and-log-analytics-cap.md) | Log Analytics with a hard daily cap | Accepted |
| [0013](0013-identity-oidc-managed-identity.md) | GitHub OIDC + managed identities | Accepted |
