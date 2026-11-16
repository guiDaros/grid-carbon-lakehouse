# ADR-0005: Handling late-arriving and revised source data

- **Status:** Accepted (details refined in specs 002/003)
- **Date:** 2026-11-16

## Context
EIA-930 and ENTSO-E revise previously published values; ENTSO-E also publishes late. Naive appends create duplicates; naive overwrites lose history.

## Decision
1. **Bronze:** append every fetched payload unchanged, with `ingested_at`, `source`, `request_window`, `payload_hash`. Never mutate.
2. **Every run re-fetches a reprocessing window** (default: last 72 h, configurable per source) in addition to new hours.
3. **Silver:** `MERGE` on the natural key (e.g. `region_id, source_type, period_start_utc`). Update only when the value hash changed; record `first_seen_at`, `last_updated_at`, `revision_count`.
4. **Gold** is recomputed for affected windows only.
5. Revisions older than the reprocessing window are captured by scheduled backfills (`gridcarbon backfill --start --end`).

## Alternatives considered
| Option | Why not |
|---|---|
| Overwrite partitions per day | Simple but rewrites more data than needed and loses revision metadata. |
| Full SCD2 on every fact | Complete history, but multiplies storage and complexity for little analytical value. History remains available through bronze and Delta time travel. SCD2 is reserved for `dim_region`. |
| Ignore revisions | Silent incorrectness — unacceptable given "correctness first". |

## Consequences
**Positive:** idempotent, auditable, no duplicates; revision rate becomes a measurable data-quality metric.
**Negative:** each run re-reads ~72 h (more API calls; must respect rate limits). Revisions outside the window are only applied on backfill.
