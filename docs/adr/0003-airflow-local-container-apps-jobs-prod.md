# ADR-0003: Airflow for local/dev, Azure Container Apps Jobs for production scheduling

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
We want a widely used orchestrator (Airflow) for dependency management, backfills and visibility, but running Airflow 24/7 in the cloud (scheduler, webserver/API server, metadata DB) costs well beyond the ≤ US$5/month budget.

## Decision
- **Local/dev/demo:** Apache Airflow 3.x via Docker Compose, with Astronomer Cosmos to render dbt models as tasks.
- **Production:** Azure Container Apps **Jobs** on a cron schedule, running the same container image and the same CLI commands.
- Enabled by the "thin orchestration, fat CLI" rule: DAGs and jobs only call `gridcarbon ...` commands.

## Alternatives considered
| Option | Why not |
|---|---|
| Airflow in the cloud (VM, Container Apps, or managed) | Always-on compute + database: tens of US$/month. Breaks the budget. |
| Container Apps Jobs only (no Airflow) | Cheapest, but loses the most-requested orchestrator and a good local developer experience (DAG view, backfill UI). |
| Dagster / Prefect | Good tools, but Airflow has broader market demand and I already have production experience with it. |

## Consequences
**Positive:** prod cost ≈ US$0; one codebase for both environments; Airflow skills still demonstrated.
**Negative:** two scheduling definitions to keep in sync (DAGs and Terraform cron). Prod lacks Airflow's UI → compensated by the `ops.pipeline_runs` audit table and alerts. Inter-job dependencies in prod are expressed as a single sequential job command (`gridcarbon run hourly`) rather than a DAG.

## Revisit when
Workflows need complex cross-job dependencies in prod, or budget allows a managed orchestrator.
