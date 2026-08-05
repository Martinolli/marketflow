# MarketFlow Split-Event Live Provider Evidence Status

Status: PASS, LIVE PROVIDER EVIDENCE OBSERVED

UTC status date: `2026-08-05`

## Scope

- repository: `marketflow`
- branch: `feature/split-event-live-evidence-smoke-aapl-v1`
- base commit: `0e88aa7`
- ticker: `AAPL`
- fixed range: `2022-01-01` through `2025-12-31`
- provider: `Massive.com`
- endpoint: `GET /stocks/v1/splits`
- provider endpoint value: `/stocks/v1/splits`
- provider request mode: `LIVE_PROVIDER_REQUEST`

This document records a controlled live split-event provider smoke for the
already fixed AAPL identity segment. It is sanitized status evidence only.

## Environment Handling

Before the live smoke, `.env` was confirmed ignored by Git:

`git check-ignore -v .env`

The process loaded only these relevant environment variables from `.env`, when
present:

- `MASSIVE_API_KEY`
- `POLYGON_API_KEY`

The live gate was enabled only for the current PowerShell process:

`MARKETFLOW_ENABLE_LIVE_SPLIT_AUDIT=1`

No API key value is included in this document.

## Live Smoke Result

- provider response status: `OK`
- provider response page count: `1`
- provider raw response row count: `0`
- split event count total: `0`
- split event count pre-range: `0`
- split event count in-range: `0`
- split event count post-range: `0`
- split event count unknown: `0`
- audit status: `SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT`
- split event audit frozen: `false`

Digest evidence:

- raw response digest:
  `e8db3f18ca3b441a4ae6436d22f48a5481fe5ab0554c092b7cba4010178974bf`
- timeline digest:
  `e73556f686e19eef149a95141718bb6c5ab2f53f4df9e5e3f9520f7c050c5076`
- receipt digest:
  `dd09dd19fe091816310ec4896ba1d63579f5e794d2efc4de7a897e9c5b117d91`
- candidate semantic digest:
  `92c0a4b4350be4731501fae3300f528bf5f42e5140f01e587ff9c87014c1f66b`

## Authority Boundary

This live smoke does not create `SPLIT_EVENT_AUDIT_FROZEN` and does not set
`split_event_audit_frozen` to `true`.

It also does not create or approve:

- canonical eligibility
- registry eligibility
- acquisition generation freeze
- runtime migration
- strategy enablement
- broker or execution behavior
- dividend evidence
- raw provider payload publication

The observed result is provider evidence for operator review only. It is not a
production source freeze and does not authorize automatic stitching.

## Sanitization

This document contains no raw provider payload, API key, account data, broker
data, tax data, personal data, or provider credential metadata.

The smoke used the existing live provider adapter and persisted no secret value
in candidate, timeline, receipt, metadata, or documentation.

## Next Required Task

`SPLIT_EVENT_OPERATOR_REVIEW_PACKAGE`

## Follow-On Review Package

The split-event operator review package has been implemented on branch
`feature/split-event-operator-review-package-v1` as an offline, digest-bound
review layer over this recorded live evidence.

The review package binds this live smoke through
`LIVE_PROVIDER_EVIDENCE_STATUS_BINDING` and records review package digest:

`f3c393c3981152b93e25de4aadfdac16f6c579208c703809f46f6291fb3930e6`

The live evidence remains source evidence for review. The split-event audit is
still not frozen, and `split_event_audit_frozen` remains `false`.
