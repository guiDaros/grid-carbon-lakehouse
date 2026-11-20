# 001 — Project skeleton & storage spike: Requirements

> Owned by the human. Revision 2 — incorporates the first Claude Code review.

## Problem
Before building any pipeline we need (a) a repository skeleton that enforces quality and security from the first commit, and (b) evidence that the storage stack — delta-rs, DuckDB, dbt-duckdb and Azurite — works the way ADR-0001, 0009, 0010 and 0011 assume. Each assumption must end with a yes/no answer and, if "no", a fallback.

## Scope
**In scope**
- Python package `gridcarbon` (src layout), `uv`, Python version pinned in `.python-version` (3.12).
- CLI with **Typer** (approved new dependency).
- Tooling: ruff, mypy (strict), pytest, pre-commit with secret scanning (gitleaks).
- Settings (`pydantic-settings`), structured JSON logging (`structlog`) with secret redaction.
- UTC window parsing utility for `--start` / `--end`.
- Storage module resolving a location to delta-rs and DuckDB configuration.
- `docker-compose.yml` with **Azurite only** (Airflow/Postgres come in a later spec).
- GitHub Actions CI: lint, types, unit tests, integration tests against an Azurite service container.
- Storage spike implemented as **permanent integration tests** using the production `storage` module (no throwaway `spikes/` code).
- `gridcarbon check-credentials` for EIA and ENTSO-E.
- `docs/sources.md` discovery (T13).

**Out of scope**
- Real ingestion, data models, Airflow, Terraform, Azure resources, recorded API fixtures (spec 002).

## Functional requirements
- FR-1: `uv sync` installs everything; `uv run gridcarbon --help` and `--version` work.
- FR-2: `gridcarbon check-credentials` makes one minimal authenticated request per source and prints OK/FAIL per source; exits non-zero if any configured source fails; never prints secrets.
- FR-3: Settings load from environment / `.env`. A missing or invalid required setting fails fast with a message naming the variable.
- FR-4: Every log line is JSON and includes `run_id`. `source`, `window_start`, `window_end` are included when known and **omitted** (not null) otherwise.
- FR-5: `GRIDCARBON_STORAGE_URI` accepts either a **local path** (relative or absolute, resolved to an absolute `file:///` URI) or an **`az://<container>/<prefix>`** URI. `abfss://` is not supported (see ADR-0011 amendment). The same `az://` code path is used with Azurite and ADLS.
- FR-6: A window parser for `--start` / `--end` accepts ISO-8601 with explicit UTC offset or `Z`, rejects naive datetimes and `start >= end`, and represents a half-open interval `[start, end)`.
- FR-7: The storage layout (paths for bronze/silver/gold/ops) is defined in `docs/design-doc.md` and implemented by a single helper; no other module builds table paths.

## Spike questions (each ends with a passing test or a documented "no" + fallback)
| # | Question | Fallback if "no" |
|---|---|---|
| SQ-1 | delta-rs can create, append and `MERGE` a table on local `file://` and on Azurite via `az://` | None — blocks the architecture; stop and escalate |
| SQ-2 | DuckDB `delta_scan` reads a delta-rs table on Azurite | Read with delta-rs → Arrow → register in DuckDB; requires ADR-0009 amendment |
| SQ-3a | Two concurrent **appends** to the same table on Azurite both succeed | Retry-on-conflict in the writer |
| SQ-3b | Two concurrent **updates of the same row** (watermark) → exactly one commit wins, the other raises a commit conflict (no silent lost update) | Retry-with-reread in the ops writer; if conflicts are not detected at all → revisit ADR-0010 |
| SQ-4 | DuckDB → Arrow → delta-rs `MERGE` round trip preserves types: `TIMESTAMP` UTC tz and microsecond precision, `DECIMAL` precision/scale, strings | Explicit schema casts in the publish step |
| SQ-5 | Re-running the same `MERGE` with the same input leaves the table contents identical | None — idempotency is mandatory |
| SQ-6 | Tables created by our single table-creation helper keep reader/writer protocol versions/features readable by DuckDB | Pin protocol/features in the helper |

**Timebox:** 3 working days for SQ-1…SQ-6. If a question fails, switch to its fallback, record it, and move on — no open-ended investigation.

## Non-functional requirements
- NFR-1: CI < 10 min; never calls real external APIs.
- NFR-2: **No secrets in the repo, logs or fixtures.** API keys travel in query strings (`api_key`, `securityToken`), so: the `httpx` logger is set to WARNING, our own logging redacts these parameters, and a test asserts a fake key never appears in captured logs or exception messages.
- NFR-3: Secret scanning (gitleaks) in pre-commit and CI, with an allowlist for the public Azurite development key.
- NFR-4: Dependencies pinned via `uv.lock`; Python pinned in `.python-version`.
- NFR-5: Plain `uv run pytest` runs unit tests only (`addopts = -m "not integration"`, marker registered); integration tests run with `uv run pytest -m integration`.

## Acceptance criteria
- [ ] AC-1: On a clean clone, `uv sync && uv run pytest` passes without Docker.
- [ ] AC-2: With `docker compose up -d azurite`, `uv run pytest -m integration` passes and covers SQ-1…SQ-6 (or documents the fallback taken).
- [ ] AC-3: CI is green on `main`: ruff, mypy --strict, unit, integration (Azurite service container), gitleaks.
- [ ] AC-4: `gridcarbon check-credentials` returns OK for EIA and ENTSO-E with real keys in `.env` (manual).
- [ ] AC-5: Tests prove: settings fail fast per variable (FR-3); window parser rejects naive/inverted windows (FR-6); local relative path → absolute `file:///` (FR-5); secrets never appear in logs (NFR-2).
- [ ] AC-6: `docs/spikes/001-findings.md` records each SQ result, versions used, and fallbacks taken.
- [ ] AC-7: **Human** updates ADR-0001/0009/0010/0011 status based on the findings.
- [ ] AC-8: `docs/sources.md` resolves the ❓ items for EIA (UTC under `frequency=hourly`, inclusive/exclusive `start`/`end`, rate limits) and ENTSO-E (rate limits, error document).

## Open questions
- SQ-3 behaviour on real ADLS may differ from Azurite → re-check once in week 6 (smoke test).
