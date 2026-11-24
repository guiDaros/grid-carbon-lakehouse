# 001 — Project skeleton & storage spike: Tasks

> One task at a time. Each task leaves CI green (once CI exists) and includes its tests.

- [x] T1: `uv init` src-layout package `gridcarbon`, `.python-version` (3.12), `pyproject.toml` with ruff/mypy(strict)/pytest config (`-m "not integration"`, marker registered), `__version__`, Typer CLI with `--version`. Unit test. — FR-1, NFR-4, NFR-5
- [x] T2: `.pre-commit-config.yaml` (ruff, ruff-format, mypy, gitleaks), `.gitleaks.toml` allowlist for the Azurite key, `Makefile`. — NFR-3
- [ ] T3: `.github/workflows/ci.yml`: lint+types, unit, gitleaks jobs. — AC-3 (partial)
- [ ] T4: `config.py` + `logging.py` (JSON, `run_id`, optional context fields omitted, redaction, httpx logger WARNING). Tests incl. secret-never-logged. — FR-3, FR-4, NFR-2
- [ ] T5: `windows.py` UTC half-open window + parser. Tests. — FR-6
- [ ] T6: `storage.py` (location normalisation, `table_uri` per layout in design doc, delta-rs options, DuckDB setup, `create_table` helper). Unit tests. — FR-5, FR-7
- [ ] T7: `docker-compose.yml` (Azurite only), integration fixtures, CI integration job with Azurite service container. — AC-2 (infra)
- [ ] T8: SQ-1 + SQ-5 + SQ-6 tests. — AC-2
- [ ] T9: SQ-2 test (or fallback documented). — AC-2
- [ ] T10: SQ-3a + SQ-3b tests. — AC-2
- [ ] T11: SQ-4 dbt-duckdb project + round-trip type test. — AC-2
- [ ] T12: `sources/credentials.py` + `check-credentials` (respx unit tests; manual run with real keys). — FR-2, AC-4
- [ ] T13: `docs/spikes/001-findings.md` (results, versions, fallbacks). Human then updates ADR statuses. — AC-6, AC-7
- [ ] T14: Resolve ❓ items in `docs/sources.md` (human-led, Claude assists). — AC-8

**Timebox for T8–T11:** 3 working days. On failure: take the fallback, record it, move on.

## Done when
- [ ] All acceptance criteria in `requirements.md` met
- [ ] ruff, mypy --strict, pytest (unit + integration), gitleaks green locally and in CI
- [ ] `CLAUDE.md` "Commands" section updated
