# ADR-0007: Only two environments — local and prod

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
Solo project with a hard cloud budget. A staging environment would duplicate cloud resources and Terraform state.

## Decision
Two environments: **local** (Docker Compose; Azurite for storage integration tests) and **prod** (Azure). CI runs unit tests, integration tests against Azurite, `dbt build` on sample data, and `terraform plan`.

## Alternatives considered
| Option | Why not |
|---|---|
| dev/staging/prod in Azure | Doubles or triples cloud cost and ops work for a single developer with no users depending on prod. |

## Consequences
**Positive:** cost and simplicity; CI + Azurite covers most of what staging would catch.
**Negative:** Azure-specific issues (IAM, networking, quotas) are first seen in prod. Mitigation: `terraform plan` in CI, small incremental deploys, a runbook, and willingness to write a postmortem when it happens.
