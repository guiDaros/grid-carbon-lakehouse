# ADR-0013: Passwordless identity — GitHub OIDC + managed identities

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
CI/CD must deploy to Azure and jobs must read/write storage, without long-lived secrets. The subscription is Azure for Students, activated through the GitHub Student Developer Pack with a personal Microsoft account (own tenant, so we have admin rights).

## Decision
- **CI → Azure:** a **user-assigned managed identity** with a **federated identity credential** trusting GitHub Actions OIDC tokens for this repository (scoped to `main` and the `prod` environment). Least-privilege role assignments on the resource group.
- **Jobs → Storage:** the Container Apps Job uses a managed identity with `Storage Blob Data Contributor` on the lake container only.
- **API keys** (EIA, ENTSO-E) stored as Container Apps secrets (Key Vault considered, see below).
- Terraform remote state in a separate storage account, accessed with Entra ID auth (no account keys).

## Alternatives considered
| Option | Why not |
|---|---|
| Service principal + client secret in GitHub Secrets | Long-lived secret to rotate and leak; exactly what interviewers flag. |
| App registration + federated credential | Equivalent security, but creates a tenant-level object; the managed identity lives in the subscription and is fully managed by Terraform. |
| Key Vault for API keys | Better practice at scale; adds a resource and access policies. Container Apps secrets are sufficient for 2 keys — revisit if secrets grow. |

## Consequences
**Positive:** no long-lived credentials anywhere; everything declared in Terraform; strong security signal.
**Negative:** bootstrap chicken-and-egg — the identity and state storage must be created once manually (documented `bootstrap/` script) before CI can run Terraform.
