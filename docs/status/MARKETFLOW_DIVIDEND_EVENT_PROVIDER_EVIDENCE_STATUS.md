# MarketFlow Dividend-Event Provider Evidence Status

Status: ADAPTER IMPLEMENTED, LIVE SMOKE NOT PERFORMED

UTC status date: `2026-08-06`

## Scope

- repository: `marketflow`
- branch: `feature/dividend-event-live-provider-adapter-v1`
- base commit: `eb4c61e`
- ticker: `AAPL`
- fixed range: `2022-01-01` through `2025-12-31`
- provider: `Massive.com`
- endpoint: `GET /stocks/v1/dividends`
- provider endpoint value: `/stocks/v1/dividends`

This document records implementation status for the dividend-event provider
adapter and provider-bound candidate support. It is not a live provider smoke
receipt.

## Execution Modes

The candidate supports:

- response injection with fake or supplied provider response data
- live provider request behind `MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT=1`

Default tests use fake transport only. Manual live smoke remains a separate
task.

## Authority Boundary

The implementation binds the frozen identity, calendar, schedule, split-event
audit, and acquisition-contract digests from the fixed AAPL authority chain.

It does not create `DIVIDEND_EVENT_AUDIT_FROZEN` and does not set
`dividend_event_audit_frozen` to `true`.

It also does not create or approve:

- canonical eligibility
- registry eligibility
- acquisition generation freeze
- runtime migration
- strategy enablement
- broker or execution behavior
- predictive usefulness
- profitability

## Sanitization

API keys are accepted only through an explicit function argument or:

- `MASSIVE_API_KEY`
- `POLYGON_API_KEY`

The adapter stores sanitized request metadata only. It does not store API key
values in candidate artifacts, raw response evidence, timeline evidence,
receipts, tests, or documentation.

## Next Required Task

`DIVIDEND_EVENT_OPERATOR_REVIEW_PACKAGE`

Before that review package, a separate controlled live smoke can be run to bind
actual provider evidence for AAPL 2022-01-01 through 2025-12-31.
