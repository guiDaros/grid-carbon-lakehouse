# ADR-0008: Static dashboard with Evidence.dev on GitHub Pages

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
The dashboard must be public (recruiters click a link), cost nothing, and stay fast with no server to maintain.

## Decision
Build the dashboard with **Evidence.dev** (SQL + Markdown, "BI as code"), generated from gold exports and deployed as a static site to **GitHub Pages** by CI on a schedule.

## Alternatives considered
| Option | Why not |
|---|---|
| Power BI | Very common in jobs (and I've used it), but public sharing requires a paid/Pro setup or "publish to web" limitations; not version-controlled. |
| Streamlit / Superset hosted | Need a running server → cost and maintenance. |
| Grafana Cloud free | Better for ops metrics than analytical storytelling. |

## Consequences
**Positive:** US$0, versioned in Git, reviewed in PRs, fast.
**Negative:** data is as fresh as the last build (e.g. every few hours), not live; no ad-hoc exploration for viewers. Power BI familiarity is shown via résumé experience instead.
