# grid-carbon-lakehouse

Production-grade Azure lakehouse that ingests hourly US (EIA-930) and European (ENTSO-E) grid data plus weather to answer: **where and when is electricity cleanest and cheapest — and what explains it?**

> 🚧 Work in progress. Design: [`docs/design-doc.md`](docs/design-doc.md) · Decisions: [`docs/adr/`](docs/adr/) · Current work: [`specs/`](specs/)

**Stack:** Python · SQL · Delta Lake (delta-rs) · DuckDB · dbt · Airflow · Azure (ADLS Gen2, Container Apps Jobs) · Terraform · GitHub Actions · MCP

## Future
Ideas deliberately left out of scope are listed here.
