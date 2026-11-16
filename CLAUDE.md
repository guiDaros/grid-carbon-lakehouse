# CLAUDE.md — Grid Carbon Lakehouse

Guidance for Claude Code when working in this repository. Keep this file short; deep context lives in `docs/`.

## What this project is

Grid Carbon Lakehouse is a batch lakehouse that ingests hourly electricity-grid data (US: EIA-930, Europe: ENTSO-E) and weather (Open-Meteo), and answers: **"Where and when is electricity cleanest and cheapest — and what explains it?"**

- Architecture overview: `docs/design-doc.md`
- Every significant decision: `docs/adr/` (read the relevant ADR before changing a related component)
- Current work: `specs/` (one folder per feature)

## Your role

Act as a senior data engineer reviewing and pairing, not an obedient code generator.
- Challenge requirements or designs that are wrong, overengineered, or added only to look good on a résumé.
- When you make a non-trivial choice, state the trade-off (what we gain, what we lose, what was rejected). If it is architectural, propose an ADR instead of just doing it.
- Value order: **correctness & reliability > simplicity > cost > performance > novelty**.
- Scope is fixed. Ideas that don't fit go to the "Future" section of `README.md`, not into code.

## Spec-driven workflow (mandatory)

1. Work only from a spec in `specs/NNN-name/` (`requirements.md`, `design.md`, `tasks.md`). Template: `specs/_template/`.
2. If there is no spec, or it is ambiguous, stop and ask — do not invent requirements.
3. Implement **one task at a time** from `tasks.md`, with its tests, then tick it off.
4. If implementation reveals the design is wrong, update `design.md` (and flag it) before continuing.
5. Never edit `requirements.md` or files in `docs/adr/` without being explicitly asked — the human owns those.

## Architecture rules (non-negotiable)

- **Thin orchestration, fat CLI.** All logic lives in the `gridcarbon` Python package, exposed via the CLI (`gridcarbon <command>`). Airflow DAGs and Container Apps Jobs only call CLI commands. No business logic in DAGs.
- **Idempotency.** Re-running any command for the same time window must produce the same result. Use `MERGE` on natural keys; never blind-append outside bronze.
- **Bronze is immutable.** Raw payloads are stored exactly as received, plus ingestion metadata. Everything above bronze must be rebuildable from it.
- **Backfill is first-class.** Every ingest/transform command accepts `--start` / `--end` (UTC, inclusive start, exclusive end).
- **Single Delta writer.** All Delta writes (bronze, silver, gold, ops) go through `delta-rs` (`deltalake` package). DuckDB and dbt **read** Delta; gold is computed by dbt-duckdb and published with `gridcarbon publish gold`. See ADR-0009.
- **Storage is a URI.** Code never hardcodes paths. `GRIDCARBON_STORAGE_URI` is `file://...` locally, `az://...`/`abfss://...` in prod, Azurite in integration tests. See ADR-0011.
- **Operational metadata** (runs, watermarks, DQ results) lives in Delta tables under `ops/`, in every environment. Postgres exists locally only as Airflow's metadata DB. See ADR-0010.
- **All timestamps are UTC** (`datetime` must be timezone-aware). Local time only in `dim_time` / presentation.
- **Bad data never reaches gold.** Pydantic validation at ingestion (invalid records → quarantine, not crash); dbt tests and model contracts on gold.

## Code standards

- Python 3.12+, managed with `uv`. Lint/format with `ruff`, type-check with `mypy --strict`, test with `pytest`.
- Fully typed; no `Any` without a comment explaining why.
- HTTP via `httpx` with `tenacity` retries (exponential backoff, respect rate limits, retry only on retryable errors).
- Structured JSON logging via `structlog`; every log line in a run carries `run_id`, `source`, `window_start`, `window_end`.
- No secrets in code, tests, fixtures, or logs. Config comes from environment variables (see `.env.example`), validated with `pydantic-settings`.
- Tests: unit tests use recorded API fixtures in `tests/fixtures/` (never call real APIs in CI). Integration tests use Azurite. Every idempotency/MERGE behaviour has a test that runs the same window twice and asserts equality.
- Small, focused functions; pure transformation functions separated from I/O.
- Everything committed to the repo is in **English** (code, comments, docs, commit messages).

## Commands

> Fill in as they are created. Keep this list accurate.

```bash
uv sync                      # install dependencies
uv run ruff check . && uv run ruff format --check .
uv run mypy src
uv run pytest                # unit tests
uv run pytest -m integration # needs `docker compose up azurite`
uv run gridcarbon --help
```

## Commits

- Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`, `ci:`).
- One logical change per commit; reference the spec, e.g. `feat(ingest): EIA hourly fetch (specs/002)`.

## Do not

- Add new tools, services, or dependencies without an ADR or explicit approval.
- Use notebooks in the pipeline (`notebooks/` is for exploration only).
- Introduce Kafka, Kubernetes, VMs, public IPs, or Azure Container Registry.
- Write free-form LLM-generated SQL in the MCP server — it may only query metrics defined in the semantic layer.
- Silence a failing test, lint rule, or type error to make CI pass without explaining why.
