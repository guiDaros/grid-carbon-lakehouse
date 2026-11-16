# ADR-0001: Delta Lake (via delta-rs) as the table format

- **Status:** Proposed — confirm in week-1 spike
- **Date:** 2026-11-16

## Context
We need an open table format on object storage that supports upserts (`MERGE`) for revised source data, schema evolution, and time travel, readable by DuckDB (transformations), Spark (historical backfill) and, potentially, Databricks/Fabric. The project runs on Azure (ADLS Gen2), is written in Python, and must avoid a JVM in the hourly jobs to keep containers small and cheap.

## Decision
Use **Delta Lake**, written with **delta-rs** (`deltalake` Python package). No catalog service; tables are addressed by storage path.

## Alternatives considered
| Option | Why not (in this context) |
|---|---|
| **Apache Iceberg** (PyIceberg) | Strong, vendor-neutral format and arguably the market's direction. But it pushes us toward running/choosing a catalog (REST/SQL) — an extra component — and Azure's native analytics stack (Databricks, Fabric/OneLake) is Delta-first. More moving parts for a solo, cost-capped project. |
| **Plain Parquet + Hive-style partitions** | Simplest, but no ACID commits, no `MERGE`, no time travel. Revised data would require rewriting partitions by hand — exactly the reliability problem this project is about. |
| **DuckLake** | Very simple and elegant, but young and much less common in job descriptions; low signalling and ecosystem risk. |

## Consequences
**Positive**
- `MERGE`, ACID commits, time travel, schema evolution without a JVM.
- Read natively by DuckDB (`delta` extension), Spark, Polars, Databricks, Fabric.
- No catalog service to run or pay for.

**Negative**
- Delta is less vendor-neutral than Iceberg; some employers are Iceberg-first. Mitigation: this ADR documents the reasoning; the dbt models are format-agnostic.
- delta-rs lags Spark-Delta on some advanced protocol features; we must avoid enabling table features that DuckDB/delta-rs cannot read.
- No catalog → table discovery is by convention (path layout documented in the design doc).

## Revisit when
- We need multi-engine writes with a catalog, or a target employer stack is Iceberg-only.
