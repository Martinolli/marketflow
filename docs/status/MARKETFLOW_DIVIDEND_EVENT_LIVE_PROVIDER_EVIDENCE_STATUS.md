# MarketFlow Dividend-Event Live Provider Evidence Status

Status: PASS, LIVE PROVIDER EVIDENCE OBSERVED

UTC status date: `2026-08-06`

## Scope

- repository: `marketflow`
- branch: `feature/dividend-event-live-evidence-smoke-aapl-v1`
- base commit: `198d375`
- ticker: `AAPL`
- fixed range: `2022-01-01` through `2025-12-31`
- provider: `Massive.com`
- endpoint: `GET /stocks/v1/dividends`
- provider endpoint value: `/stocks/v1/dividends`
- provider request mode: `LIVE_PROVIDER_REQUEST`

This document records a controlled live dividend-event provider smoke for the
already fixed AAPL identity segment. It is sanitized status evidence only.

## Environment Handling

Before the live smoke, `.env` was confirmed ignored by Git:

`git check-ignore -v .env`

The process loaded only these relevant environment variables from `.env`, when
present:

- `MASSIVE_API_KEY`
- `POLYGON_API_KEY`

The live gate was enabled only for the current PowerShell process:

`MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT=1`

No API key value is included in this document.

## Live Smoke Result

- provider response status: `OK`
- provider response page count: `1`
- provider raw response row count: `16`
- dividend event count total: `16`
- dividend event count pre-range: `0`
- dividend event count in-range: `16`
- dividend event count post-range: `0`
- dividend event count unknown: `0`
- audit status: `DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND`
- dividend event audit frozen: `false`

Digest evidence:

- raw response digest:
  `3b60a63bf0103c1f6b735efd6b086626605c7e717f45d0299965e8988dee396f`
- timeline digest:
  `e5d13b1e203b3106855571299f147d0221d92ebcbed019e4b50e6f8e908c0659`
- receipt digest:
  `e8bb85d0ceefbe5f1bad411e333142e7957cca09572d0f7be64612eba4bef9e5`
- candidate semantic digest:
  `19a6275675c14e4ab06c9785828c60bd6a27274507fcddc60dced2ce82662d50`

## Authority Boundary

This live smoke does not create `DIVIDEND_EVENT_AUDIT_FROZEN` and does not set
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
- raw provider payload publication

The observed in-range dividends are source evidence for operator review and
later acquisition-generation adjustment policy work. They are not a failure.

## Sanitization

This document contains no raw provider payload, API key, account data, broker
data, tax data, personal data, or provider credential metadata.

The smoke used the live provider adapter and persisted no secret value in the
candidate summary, timeline digest, receipt digest, metadata, or documentation.

## Next Required Task

`DIVIDEND_EVENT_OPERATOR_REVIEW_PACKAGE`

The next recommended task is a dividend-event operator review package over this
recorded live evidence. A later operator freeze ceremony is still required
before dividend-event audit authority is frozen.
