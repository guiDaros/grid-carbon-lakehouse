# ADR-0002: Hourly micro-batch, no streaming

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
Sources publish data hourly (EIA-930) or in 15/60-minute resolutions with publication delays (ENTSO-E). The freshness SLA is ~3 hours. Data is also revised after publication.

## Decision
Ingest with **hourly scheduled batch jobs** that pull a sliding window (latest hours + a reprocessing window for revisions). No Kafka, Event Hubs, or stream processors.

## Alternatives considered
| Option | Why not |
|---|---|
| Kafka / Event Hubs + stream processing | Sources are pull-based REST APIs that update hourly; streaming adds always-on infrastructure (cost) and operational burden with zero gain in freshness. Revisions are easier to handle in batch windows. |
| Daily batch | Cheaper still, but misses the "near real-time grid" use case (carbon-aware scheduling needs today's hours). |

## Consequences
**Positive:** near-zero cost (fits serverless job free grants), simple retries and backfills, deterministic windows.
**Negative:** minimum latency ≈ source latency + 1 h. We don't demonstrate streaming skills — deliberately; knowing when *not* to stream is the point.

## Revisit when
A source offers push/streaming data and a use case needs sub-hour latency.
