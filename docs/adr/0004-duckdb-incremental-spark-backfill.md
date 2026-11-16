# ADR-0004: DuckDB for incremental transforms; Spark only for historical backfill

- **Status:** Proposed — numbers to be filled by the week-7 benchmark
- **Date:** 2026-11-16

## Context
Hourly increments are small (MBs). The historical backfill (several years × regions × sources) is larger, but still likely in the single-digit to tens of GB range.

## Decision
- **DuckDB** (via dbt-duckdb and the CLI) for all hourly/incremental work, local and prod.
- **PySpark + Delta** only for the one-off historical backfill, run locally, and benchmarked against DuckDB on the same workload.

## Alternatives considered
| Option | Why not |
|---|---|
| Spark for everything | JVM startup and memory make hourly jobs slower and more expensive; overkill for MB-scale increments. |
| DuckDB for everything (no Spark) | Probably sufficient even for the backfill — the benchmark may prove that. Spark is kept to produce evidence, not by default. |

## Consequences
**Positive:** cheap, fast hourly jobs in small containers; a data-backed comparison (time, memory, cost) instead of opinion.
**Negative:** two engines to maintain for one workload; Spark code exists mainly for the benchmark. **This is the first item to cut if the schedule slips.**

## Benchmark (to fill in)
| Engine | Data volume | Wall time | Peak memory | Notes |
|---|---|---|---|---|
| DuckDB | | | | |
| Spark (local) | | | | |
