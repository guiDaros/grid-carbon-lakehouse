# 001 — Project skeleton & storage spike: Design

## Overview
A `uv`-managed src-layout package with a Typer CLI and shared `config`, `logging`, `windows` and `storage` modules, plus CI and an integration-test suite that answers the spike questions against Azurite. The spike is not throwaway: it exercises the production `storage` module, and the tests remain as regression tests. All code follows full standards (mypy --strict, tests).

## Components & files
| Path | Responsibility |
|---|---|
| `.python-version` | `3.12` |
| `pyproject.toml` | Metadata, deps, ruff/mypy/pytest config (`addopts = -m "not integration"`, marker registered), `gridcarbon` script |
| `src/gridcarbon/__init__.py` | `__version__` |
| `src/gridcarbon/cli.py` | Typer app: `--version`, `check-credentials` |
| `src/gridcarbon/config.py` | `Settings` (pydantic-settings); storage location normalisation (FR-5) |
| `src/gridcarbon/logging.py` | structlog JSON; `run_id` binding; redaction processor for `api_key`/`securityToken`/`token`/`key` params; `httpx`/`httpcore` loggers at WARNING |
| `src/gridcarbon/windows.py` | `TimeWindow` (UTC, half-open) + parser (FR-6) |
| `src/gridcarbon/storage.py` | `StorageLocation` → `table_uri(layer, source, dataset)`, delta-rs `storage_options`, DuckDB setup statements; `create_table()` helper pinning protocol/features (SQ-6) |
| `src/gridcarbon/sources/credentials.py` | One minimal request per source; returns status; never includes the URL in errors |
| `tests/unit/` | config, windows, storage, logging redaction, CLI (HTTP mocked with `respx`) |
| `tests/integration/conftest.py` | Azurite fixture: unique container per session, cleanup |
| `tests/integration/test_storage_spike.py` | SQ-1 … SQ-6 |
| `tests/integration/dbt_spike/` | Minimal dbt-duckdb project for SQ-4 |
| `docker-compose.yml` | `azurite` service only |
| `.pre-commit-config.yaml` | ruff, ruff-format, mypy, gitleaks, whitespace hooks |
| `.gitleaks.toml` | Allowlist for the public Azurite dev account key |
| `.github/workflows/ci.yml` | Jobs: lint+types, unit, integration (Azurite service), gitleaks |
| `Makefile` | `setup`, `lint`, `test`, `test-integration`, `up`, `down` |
| `docs/spikes/001-findings.md` | Spike results |

## Storage access (FR-5, ADR-0011 amendment)
- Local dev: path → `file:///abs/path`.
- Azurite and ADLS: `az://<container>/<prefix>` (Blob API). Azurite does not emulate the ADLS Gen2 `dfs` endpoint, so using `abfss://` would leave the prod code path untested.
- Azurite connection: account name/key + `http://127.0.0.1:10000` endpoint, with emulator/allow-http options in delta-rs `storage_options`; DuckDB via an Azure secret with the connection string.
- Prod (week 6): managed identity; same `az://` URIs.

## Key choices
| Choice | Pros | Cons | Decision |
|---|---|---|---|
| CLI: Typer vs Click vs argparse | Typer: type hints, less boilerplate, built on Click | One more dependency | Typer (approved) |
| HTTP mocking: respx | Explicit, fast, native to httpx | Hand-written responses | respx in 001; recorded + scrubbed fixtures in 002 |
| Spike as tests on production module vs `spikes/` scripts | Repeatable, CI-guarded, no half-finished code | More upfront rigour | Tests on production module |
| `az://` everywhere vs `abfss://` in prod | Same code path in tests and prod | Doesn't use ADLS-specific dfs features (not needed) | `az://` |
| Missing log context fields: omit vs null | Omit keeps logs compact, no ambiguity | Queries must handle missing keys | Omit |

## Spike test design
- SQ-1/SQ-5: write → append → MERGE (Arrow table, natural key); rerun MERGE; compare sorted tables and assert no new data change in the second commit's metrics.
- SQ-2: DuckDB with `delta` + `azure` extensions; compare `delta_scan` result with delta-rs read.
- SQ-3a: two processes append concurrently; assert both rows present, log versions contiguous.
- SQ-3b: two processes update the same key from the same read version; assert exactly one succeeds and the other raises a commit-conflict error.
- SQ-4: dbt `dbtRunner` builds a model from `delta_scan`; result → Arrow → delta-rs MERGE; assert schema (tz-aware UTC microsecond timestamps, decimals) and values.
- SQ-6: assert table protocol (min reader/writer versions, features) matches what the helper pins and that DuckDB reads it.

## Risks
- DuckDB's Azure/delta extensions with a custom endpoint (SQ-2) — most likely failure; fallback defined.
- Azurite vs ADLS concurrency semantics (SQ-3) — re-check in week 6.

## Related ADRs
0001, 0009, 0010, 0011 (amended: `az://` only), 0013.
