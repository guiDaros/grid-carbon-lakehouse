# ADR-0010: Operational metadata in Delta tables, not a cloud PostgreSQL

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
We need to store pipeline runs (audit), watermarks, and data-quality results. The original plan used Azure Database for PostgreSQL Flexible Server (B1MS, free for 12 months for new customers).

## Decision
Store operational metadata as **Delta tables under `ops/`** (`pipeline_runs`, `watermarks`, `dq_results`) in the same lake, written with delta-rs, in every environment. Locally, PostgreSQL exists **only** as Airflow's metadata database.

## Alternatives considered
| Option | Pros | Cons |
|---|---|---|
| Azure PostgreSQL Flexible Server | Real transactional DB; row-level updates; familiar SQL tooling | An extra always-on resource, credentials, firewall/networking setup; free only for 12 months and then billed; a second system to back up and monitor |
| Azure Table Storage | Very cheap key-value | Another API and data model; poor for analytics on run history |
| SQLite file on blob | Simple | Not safe for concurrent writers over object storage |

## Consequences
**Positive:** one less service, secret and network rule; zero cost; run history is queryable with the same DuckDB/dbt tooling (dashboards of pipeline health for free); same code path local and prod.
**Negative:** Delta is not built for high-frequency single-row updates — acceptable at hourly cadence (a handful of commits per hour), but requires periodic `OPTIMIZE`/`VACUUM` of `ops` tables. Concurrent commits rely on delta-rs' Azure support for atomic conditional writes — **to verify in the week-1 spike** (two concurrent writers test).

## Revisit when
Run frequency or concurrency grows (e.g. many parallel jobs per minute) or we need transactional locking across jobs.
