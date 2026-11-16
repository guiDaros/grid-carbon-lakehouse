# ADR-0012: Structured logs to Log Analytics with a hard daily cap

- **Status:** Accepted — verify free allowance in the portal before deploy
- **Date:** 2026-11-16

## Context
Container Apps Jobs need somewhere to send stdout/stderr. Without centralised logs, a failed cloud run is very hard to debug. Log Analytics is billed by ingested GB, the classic source of surprise Azure bills.

## Decision
- Application emits **structured JSON logs** (structlog) with `run_id` on every line.
- Container Apps environment sends logs to **Log Analytics** with a **daily ingestion cap** (start at 0.1 GB/day) and minimal retention, all set in Terraform.
- Our own `ops.pipeline_runs` table and webhook alerts remain the primary signals; Log Analytics is for debugging.

## Alternatives considered
| Option | Pros | Cons |
|---|---|---|
| No log destination | US$0 guaranteed | Blind when a job fails in prod; can't write a real postmortem |
| Log Analytics without cap | Full visibility | Unbounded cost risk (e.g. a log loop) |
| Ship logs to the lake ourselves | Cheap, queryable | Custom plumbing; lose platform logs (container start failures, OOM) |

## Consequences
**Positive:** debuggable prod at near-zero cost; cost risk bounded by design.
**Negative:** when the cap is hit, logs are dropped for the rest of the day; we must keep log volume disciplined (no payload dumps at INFO).
