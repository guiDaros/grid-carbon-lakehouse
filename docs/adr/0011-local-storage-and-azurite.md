# ADR-0011: Local filesystem for development, Azurite for integration tests, ADLS Gen2 in prod

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
We want local-first development that mirrors cloud behaviour, without paying for cloud resources during development. The original plan used MinIO, but MinIO's community edition was put into maintenance mode (Dec 2025) and its repository was archived in Feb 2026; it also emulates S3, not Azure.

## Decision
- Storage location is a single setting: `GRIDCARBON_STORAGE_URI`.
- **Local dev:** `file://` on the local filesystem (fastest feedback loop).
- **Integration tests / CI:** **Azurite** (Microsoft's official Azure Storage emulator) in Docker, exercising the real Azure code path (auth config, `az://` URIs, delta-rs and DuckDB Azure clients).
- **Prod:** ADLS Gen2 with hierarchical namespace, accessed via managed identity.

## Alternatives considered
| Option | Why not |
|---|---|
| MinIO | Archived upstream; S3 API ≠ Azure, so it wouldn't test our real code path. |
| Real Azure storage for dev/CI | Costs money and needs credentials in CI for every run. |
| Azurite for everything locally | Slower and more friction for day-to-day work than plain files. |

## Consequences
**Positive:** zero-cost dev and CI; the Azure path is tested before deploy; vendor-maintained emulator.
**Negative:** Azurite does not emulate every ADLS Gen2 (hierarchical namespace) behaviour — e.g. some directory/ACL semantics. Small risk of "works on Azurite, fails on ADLS" — mitigated by a smoke test after each deploy. **Spike task:** confirm delta-rs and DuckDB both work against Azurite.

## Amendment 1 (2026-11-19): `az://` only, no `abfss://`
Azurite emulates the Blob endpoint only, not the ADLS Gen2 `dfs` endpoint. If prod used `abfss://` (dfs) while tests used `az://` (blob), the prod access path would never be integration-tested. Decision: **all environments use `az://<container>/<prefix>`** (Blob API) on the HNS-enabled ADLS Gen2 account. We give up nothing we need (we don't use POSIX ACLs or dfs-specific operations). Local development additionally accepts a plain filesystem path, normalised to an absolute `file:///` URI (`file://./relative` is not a valid URI).
