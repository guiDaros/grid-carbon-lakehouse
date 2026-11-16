# ADR-0009: delta-rs is the single Delta writer; dbt-duckdb computes, a CLI step publishes gold

- **Status:** Proposed — confirm in week-1 spike
- **Date:** 2026-11-16

## Context
dbt-duckdb is our modelling tool. DuckDB's `delta` extension can now write to Delta tables, but write support is limited to inserts (no `MERGE`/upsert), while our silver and gold layers need upserts for revised data (ADR-0005). Having several libraries write to the same Delta tables increases the risk of protocol/feature incompatibilities.

## Decision
- **All Delta writes** (bronze, silver, gold, ops) go through **delta-rs**.
- **dbt-duckdb** reads silver via `delta_scan`, builds and tests gold models inside DuckDB (with model contracts).
- **`gridcarbon publish gold`** writes the tested gold relations to Delta with delta-rs (`MERGE` for incremental facts, overwrite for small dimensions).
- Publishing happens only after `dbt build` succeeds → failed tests block bad data from reaching gold.

## Alternatives considered
| Option | Pros | Cons |
|---|---|---|
| DuckDB native Delta `INSERT` from dbt | One step fewer | No `MERGE`; second writer library; newer, less battle-tested write path |
| Gold as plain Parquet (dbt `external` materialization) | Simplest | No ACID/time travel on gold; readers may see partial writes |
| Gold stays in a `.duckdb` file | Very simple | A database file on blob storage isn't a lakehouse table; poor multi-reader story |

## Consequences
**Positive:** one write path with `MERGE` everywhere; a natural "quality gate" between dbt and published gold; consistent table features.
**Negative:** an extra step and a little glue code (DuckDB → Arrow → delta-rs); gold briefly lives in DuckDB before publishing (memory bound by gold size — small for this project).

## Revisit when
DuckDB's Delta extension supports `MERGE` and is proven stable with delta-rs-written tables.
