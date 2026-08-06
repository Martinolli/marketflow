# MarketFlow Dividend-Event Audit v1 Plan

Status: LIVE PROVIDER ADAPTER IMPLEMENTED / PROVIDER-BOUND CANDIDATE SUPPORTED / OPERATOR REVIEW PACKAGE READY / NO FREEZE

## Purpose

Dividend-Event Audit Candidate v1 creates an offline scaffold artifact and now
supports a provider-bound candidate from either injected provider response data
or an explicitly gated live Massive.com provider request.

It creates only:

`DIVIDEND_EVENT_AUDIT_CANDIDATE`

and, after recorded live evidence is reviewed offline:

`DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE`

with either scaffold status:

`DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE`

or provider-bound candidate status:

`DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND`

or review-package status:

`DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY`

It does not create `DIVIDEND_EVENT_AUDIT_FROZEN` and does not set
`dividend_event_audit_frozen` to `true`.

## Authority Chain Position

The dividend-event candidate starts after identity, exchange-calendar, and
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

The deterministic scaffold digest remains:

`9f50358696a79496bc14f7c526553072f3026b5df28c1d94e65da4c88791a4c0`

Provider-bound candidates retain this value as
`previous_scaffold_candidate_digest` and do not mutate frozen authority
digests.

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

This candidate binds the acquisition contract digest only. It does not generate
acquisition data and does not approve acquisition generation.

## Provider Evidence Collection

Provider evidence binding supports two modes:

- response injection
- live provider request

The live adapter uses:

`GET /stocks/v1/dividends`

Provider metadata records:

- provider: `MASSIVE.COM`
- endpoint stability: `CURRENT_STOCKS_V1_DIVIDENDS`
- provider request mode: `LIVE_PROVIDER_REQUEST`
- ticker filter: `AAPL`
- ex-dividend date filters: `2022-01-01` through `2025-12-31`
- sort: `ex_dividend_date.asc`
- limit: `5000`

The endpoint is queried by ticker. The candidate retains the frozen Composite
FIGI binding in provider evidence and records this endpoint limitation
explicitly.

Live execution is blocked unless:

`MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT=1`

An API key is accepted from an explicit function argument or from existing
environment conventions:

- `MASSIVE_API_KEY`
- `POLYGON_API_KEY`

API keys are not stored in candidate artifacts, request metadata, raw response
objects, timeline objects, receipts, documentation, or tests.

The default pytest suite uses fake transport only. It does not depend on live
provider availability and does not perform network access.

## Provider-Bound Candidate

A provider-bound candidate records:

- `artifact_kind`: `DIVIDEND_EVENT_AUDIT_CANDIDATE`
- `schema_version`: `dividend_event_audit_candidate_v1`
- `candidate_status`: `DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND`
- `created_offline`: `false`
- `dividend_events_provider_evidence_bound`: `true`
- `dividend_event_audit_complete`: `true`
- `dividend_event_audit_frozen`: `false`
- `operator_review_required`: `true`
- `operator_freeze_required`: `true`

Injected response mode records:

- `provider_requests_made`: `false`
- `provider_response_injected`: `true`
- `provider_request_mode`: `PROVIDER_RESPONSE_INJECTION`

Live request mode records:

- `provider_requests_made`: `true`
- `provider_response_injected`: `false`
- `provider_request_mode`: `LIVE_PROVIDER_REQUEST`

Both modes produce deterministic raw response, event timeline, audit receipt,
and candidate digests.

## Event Timeline

Each normalized event contains only supported fields:

- `ex_dividend_date`
- `declaration_date`
- `record_date`
- `pay_date`
- `cash_amount`
- `split_adjusted_cash_amount`
- `historical_adjustment_factor`
- `currency`
- `frequency`
- `distribution_type`
- `dividend_type_if_available`
- `ticker`
- `composite_figi_if_available`
- `raw_event_index`
- `raw_event_digest`
- `event_position`

Missing provider fields remain `null`. The service does not fabricate missing
provider values from the fixed identity segment.

Event position is classified using `ex_dividend_date`:

- earlier than `2022-01-01`: `PRE_RANGE`
- `2022-01-01` through `2025-12-31`: `IN_RANGE`
- later than `2025-12-31`: `POST_RANGE`
- missing or unparseable: `UNKNOWN`

Counts are derived from normalized provider data and are never guessed.

## Audit Status

Provider-bound evidence produces:

- `DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND` when in-range
  count is zero and evidence is otherwise usable
- `DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND` when in-range count
  is greater than zero
- `DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE` when evidence contains
  unknown event dates

In-range dividends are not a failure. They are source evidence for the next
operator review and later acquisition-generation adjustment policy work.

## Operator Review Package

Dividend-Event Operator Review Package v1 binds to the recorded live AAPL
dividend evidence status without making a new provider request and without
copying raw provider payload data.

The review package records:

- `artifact_kind`: `DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE`
- `schema_version`: `dividend_event_audit_candidate_review_v1`
- `review_status`: `DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY`
- `created_offline`: `true`
- `provider_requests_made_in_review`: `false`
- `operator_decision_required`: `true`
- `operator_decision`: `null`
- `dividend_event_audit_frozen`: `false`
- `automatic_stitching`: `false`

Recorded live evidence bindings:

- candidate semantic digest:
  `19a6275675c14e4ab06c9785828c60bd6a27274507fcddc60dced2ce82662d50`
- raw response digest:
  `3b60a63bf0103c1f6b735efd6b086626605c7e717f45d0299965e8988dee396f`
- timeline digest:
  `e5d13b1e203b3106855571299f147d0221d92ebcbed019e4b50e6f8e908c0659`
- receipt digest:
  `e8bb85d0ceefbe5f1bad411e333142e7957cca09572d0f7be64612eba4bef9e5`
- review package digest:
  `5cfa4b8f86658b84df932afbf8278d431f18a1082014b3df3ad8c15af2d55742`
- checks: `39` total, `39` passed, `0` failed, `0` blockers

The review package records `16` in-range dividends. This is not a blocker.
It sets the implication:

`ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`

## Non-Goals

This task does not call Ticker Overview, Ticker Events, calendar, split events,
custom bars, registry, Strategy, runtime, or broker paths.

This task does not create canonical eligibility, registry eligibility,
acquisition-generation freeze, Strategy/runtime migration, broker behavior,
execution behavior, predictive acceptance, or profitability acceptance.

## Next Tasks

1. Digest-bound dividend-event operator freeze ceremony.
2. Full 2022-2025 acquisition generation.
3. Acquisition-generation freeze.
4. SWING canonical dataset and registry approval.
5. POSITION_SWING canonical dataset and registry approval.
6. Normal runtime migration.
7. Applicability/research campaign.
8. Predictive and profitability evaluation.
