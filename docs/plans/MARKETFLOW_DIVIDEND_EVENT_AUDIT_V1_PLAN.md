# MarketFlow Dividend-Event Audit v1 Plan

Status: OFFLINE SCAFFOLD / PROVIDER EVIDENCE REQUIRED

## Purpose

Dividend-Event Audit Candidate v1 creates an offline scaffold artifact for the
fixed AAPL 2022-01-01 through 2025-12-31 authority chain.

It creates only:

`DIVIDEND_EVENT_AUDIT_CANDIDATE`

with candidate status:

`DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE`

It does not call Massive.com, Polygon, a dividends endpoint, or any provider
adapter. It does not create `DIVIDEND_EVENT_AUDIT_FROZEN` and does not set
`dividend_event_audit_frozen` to `true`.

## Authority Chain Position

The dividend-event scaffold starts after identity, exchange-calendar, and
split-event audit authority have been frozen. It binds to:

- identity frozen digest:
  `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- exchange calendar frozen digest:
  `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- schedule digest:
  `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- split-event audit frozen digest:
  `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- split-event audit status:
  `SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT`
- acquisition contract digest:
  `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`

The deterministic dividend-event audit candidate digest is:

`9f50358696a79496bc14f7c526553072f3026b5df28c1d94e65da4c88791a4c0`

The scaffold checklist is `19 total`, `19 passed`, `0 failed`, `0 blockers`.

## Fixed Segment

- ticker: `AAPL`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- primary MIC: `XNAS`
- security type: `CS`
- segment range: `2022-01-01` through `2025-12-31`

## Fixed Acquisition Contract

- contract: `CORE ACQUISITION CONTRACT v2.1`
- source: `Massive.com Custom Bars`
- bar interval: `15-minute`
- adjusted: `true`
- ascending: `true`
- source timestamps are aggregate window starts: `true`
- source timezone: `America/New_York`
- canonical storage timezone: `UTC`

This scaffold binds the acquisition contract digest only. It does not generate
acquisition data and does not approve acquisition generation.

## Provider Evidence Status

- provider evidence required: `true`
- provider evidence status: `NOT_BOUND`
- provider request performed in this task: `false`
- provider endpoint: `null`
- provider query identifier: `null`
- raw response artifact id: `null`
- raw response digest: `null`
- event timeline artifact id: `null`
- event timeline digest: `null`
- audit receipt artifact id: `null`

No raw provider payloads, API keys, request bodies, response payloads, timeline
artifacts, or receipts are stored by this scaffold.

## Dividend Event Outline

The scaffold deliberately leaves future provider-derived values unpopulated:

- dividend event count total: `null`
- dividend event count pre-range: `null`
- dividend event count in-range: `null`
- dividend event count post-range: `null`
- dividend event count unknown: `null`
- dividend events: `[]`
- audit status: `null`

Future normalized dividend event records are expected to define:

- `ex_dividend_date`
- `declaration_date`
- `record_date`
- `payable_date`
- `cash_amount`
- `currency`
- `frequency`
- `dividend_type`
- `ticker`
- `composite_figi_if_available`
- `raw_event_index`
- `raw_event_digest`
- `event_position`

Valid event positions are `PRE_RANGE`, `IN_RANGE`, `POST_RANGE`, and `UNKNOWN`.

## Authority Boundary

- identity_segment_frozen: `true`
- calendar_operator_frozen: `true`
- split_event_audit_frozen: `true`
- dividend_event_audit_frozen: `false`
- canonical_eligibility: `false`
- registry_eligibility: `false`
- acquisition_generation_freeze: `false`
- strategy_runtime_migration: `false`
- automatic_stitching: `false`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Next Required Task

`DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION`

## Remaining Roadmap

- Dividend-event provider evidence collection.
- Dividend-event audit candidate with bound provider evidence.
- Dividend-event operator review package.
- Dividend-event operator freeze ceremony.
- Full 2022-2025 acquisition generation.
- Acquisition-generation freeze.
- SWING canonical dataset and registry approval.
- POSITION_SWING canonical dataset and registry approval.
- Normal runtime migration.
- Applicability/research campaign.
- Predictive and profitability evaluation.

## Non-Goals

This task does not create canonical eligibility, registry eligibility,
acquisition-generation freeze, Strategy/runtime migration, broker behavior,
execution behavior, predictive acceptance, or profitability acceptance.

This task does not inspect, require, print, store, or validate any API key.
