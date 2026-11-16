# ADR-0006: AI access restricted to the semantic layer, measured by evals; no public chatbot

- **Status:** Accepted
- **Date:** 2026-11-16

## Context
We want an AI "analyst" over the data without hallucinated metrics, runaway costs, or abuse of a public endpoint.

## Decision
- An **MCP server** exposes typed tools (`list_metrics`, `query_metric`, `compare_regions`, `explain_metric`) that only execute **metrics defined in a versioned YAML semantic layer**.
- No free-form LLM-generated SQL against the warehouse.
- An **eval suite** (~50 questions with expected answers) reports accuracy, latency and cost per question in the README.
- Runs locally; demonstrated in the video. Not hosted publicly.

## Alternatives considered
| Option | Why not |
|---|---|
| Text-to-SQL chatbot | Flexible but unreliable (wrong joins, made-up columns) and hard to evaluate. |
| Public hosted chatbot | Ongoing LLM cost, abuse risk, auth burden — incompatible with the budget. |

## Consequences
**Positive:** answers are consistent with dashboard metrics; quality is quantified, not claimed.
**Negative:** questions outside the defined metrics can't be answered (by design); recruiters can't try it live — mitigated by the video and eval results.
