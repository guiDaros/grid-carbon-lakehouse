# Grid Carbon Lakehouse — Design Doc (v0)

> Status: v0 — enough to start spec 001. Expanded as specs land.

## 1. Problem
Electricity is cleaner and cheaper at some hours and places than others. Grid data that shows this is public but scattered across operators, formats (JSON/XML), resolutions (15/60 min), time zones and revisions. This project builds a reliable, low-cost pipeline that answers: **where and when is electricity cleanest and cheapest — and what explains it?**

## 2. Requirements (summary)
- Hourly ingestion of EIA-930 (US), ENTSO-E (Europe) and Open-Meteo (weather).
- Freshness SLA: generation/load available in gold ≤ 3 h after the source publishes it.
- Idempotent runs and backfills for any time window; revised source data applied without duplicates.
- Data quality gates before gold; auditable run history.
- Cloud cost ≤ US$5/month.

## 3. Architecture
Batch lakehouse (bronze → silver → gold) on Delta Lake. Python CLI (`gridcarbon`) holds all logic; Airflow (local) and Azure Container Apps Jobs (prod) only call CLI commands. delta-rs is the only Delta writer; DuckDB/dbt read and transform. See `docs/adr/`.

## 4. Storage layout
Root = `GRIDCARBON_STORAGE_URI` (local path or `az://<container>/<prefix>`). Tables are discovered by path (no catalog, ADR-0001). Only `gridcarbon.storage.table_uri()` builds these paths.

```
<root>/
├── bronze/<source>/<dataset>/        # raw payloads + ingestion metadata, append-only
│     e.g. bronze/eia/region_data/, bronze/entsoe/actual_load/
├── silver/<source>/<dataset>/        # typed, UTC, deduplicated, MERGE on natural key
│     e.g. silver/eia/demand_hourly/, silver/entsoe/generation_by_type/
├── gold/<model>/                     # published dbt models
│     e.g. gold/fct_generation_hourly/, gold/dim_region/
├── quarantine/<source>/<dataset>/    # records that failed validation
└── ops/
      ├── pipeline_runs/
      ├── watermarks/                 # one row per (source, dataset, series_type)
      └── dq_results/
```

Naming: `snake_case`; `<source>` ∈ {`eia`, `entsoe`, `openmeteo`}. Partitioning decided per table in its spec (default: none until volume justifies it).

## 5. Time semantics
- All stored timestamps are UTC, timezone-aware.
- Windows are half-open `[start, end)`. Each source adapter converts to the source's own convention (e.g. inclusive/exclusive end) — documented in `docs/sources.md`.
- Watermarks and freshness are tracked **per series type** (EIA forecasts carry future timestamps).

## 6. Open items
- Spike results (spec 001) may amend storage access (ADR-0009/0011).
- Data model detail → spec 004 (dbt).
