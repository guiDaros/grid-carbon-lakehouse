# Data sources — discovery notes

> Living document. Findings from manual API checks; refine during spec 001 (T13) and spec 002.
> Status legend: ✅ verified manually · ❓ to verify

## EIA Open Data API v2 (US — EIA-930 Hourly Electric Grid Monitor)

| Item | Notes |
|---|---|
| Auth | API key as `api_key` query parameter ✅ |
| Endpoint | `https://api.eia.gov/v2/electricity/rto/region-data/data/` ✅ (demand/forecast/net generation/interchange by balancing authority) |
| Other endpoints | `.../rto/fuel-type-data/data/` (generation by fuel type) ❓, `.../rto/interchange-data/data/` (BA-to-BA) ❓ |
| Time format | `period` like `2026-11-20T08` (`YYYY-MM-DD"T"HH24`), with `frequency=hourly` ✅ — confirm it is UTC (vs `local-hourly`) ❓ |
| Values | Returned as **strings** (e.g. `"23260"`) with `value-units` → must cast and validate ✅ |
| Revisions | Values are revised after publication → reprocessing window (ADR-0005) |

### Findings that shape the design
1. **Max 5,000 rows per JSON response.** The API returns a `warnings` entry ("incomplete return") and a `response.total` count when the limit is hit. ✅
   → Ingestion must **paginate with `offset`/`length`** until `total` is reached, and/or split the time window into chunks. Treat the "incomplete return" warning as an error if pagination is not complete. (Spec 002.)
2. **Several series types share the same endpoint**, identified by `type`: `D` (demand), `DF` (day-ahead demand forecast), `NG` (net generation), `TI` (total interchange). ✅
   → Always request/filter explicitly by `type` (`facets[type][]=...`).
   → **Forecasts (`DF`) have future timestamps** (e.g. `2026-11-20T08` returned on 2026-11-19). Freshness checks and watermarks **must be computed per type**, never from the max timestamp across all types — otherwise forecasts make stale actuals look fresh.
3. Rate limits ❓ · historical coverage ❓ · license/attribution: cite "U.S. Energy Information Administration (EIA)" ❓

## ENTSO-E Transparency Platform (Europe)

| Item | Notes |
|---|---|
| Auth | `securityToken` query parameter ✅ |
| Base URL | `https://web-api.tp.entsoe.eu/api` ✅ |
| Verified request | Actual total load: `documentType=A65&processType=A16&outBiddingZone_Domain=10YNL----------L&periodStart=YYYYMMDDHHMM&periodEnd=YYYYMMDDHHMM` ✅ |
| Other documents | Generation per type (`A75`), day-ahead prices (`A44`), physical flows (`A11`) ❓ |
| Format | **XML**, IEC 62325 schemas, e.g. `GL_MarketDocument` in namespace `urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0` ✅ |
| Time | `periodStart`/`periodEnd` in UTC, format `YYYYMMDDHHMM` ✅ |

### Findings that shape the design
1. **Namespaced XML.** The parser must handle namespaces explicitly (namespace differs per document type — generation/load vs. market/price documents). ✅
2. **Each `TimeSeries` carries its own `Period` with a `resolution`** (e.g. `PT15M`, `PT60M`) and `Point`s indexed by `position`. Timestamps must be computed as `period_start + (position - 1) × resolution`. ❓ verify on real payloads (spec 003)
3. Points may be omitted when values repeat (curve type `A03`) ❓ → must forward-fill if so.
4. Rate limits ❓ · error responses (`Acknowledgement_MarketDocument`) ❓ · license/attribution ❓

## Open-Meteo (weather)

| Item | Notes |
|---|---|
| Auth | None ❓ |
| Endpoints | Forecast and historical archive APIs ❓ |
| Rate limits / license | ❓ (non-commercial use terms) |