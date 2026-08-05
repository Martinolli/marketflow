# MarketFlow Split-Event Audit v1 Plan

Status: LIVE PROVIDER ADAPTER IMPLEMENTED / EXPLICIT-GATE MODE

## Purpose

Split-Event Audit Evidence Candidate v1 creates an offline scaffold artifact,
supports a provider-bound candidate from supplied provider response data, and
now supports a live Massive.com provider adapter behind an explicit execution
gate.

It creates only candidate artifacts:

`SPLIT_EVENT_AUDIT_CANDIDATE`

with either scaffold status:

`SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE`

or provider-bound candidate status:

`SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND`

It does not create `SPLIT_EVENT_AUDIT_FROZEN` and does not set
`split_event_audit_frozen` to `true`.

## Authority Chain Position

Split-event audit comes after identity and calendar authority have been
operator-frozen because future split evidence must be interpreted against a
fixed identity segment and a fixed exchange calendar schedule.

This scaffold binds to:

- identity frozen digest:
  `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- exchange calendar frozen digest:
  `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- schedule digest:
  `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- acquisition contract digest:
  `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`

The deterministic split-event audit candidate digest is:

`6874936bcbc10db46f5ad084b1ada6fa1658502994a1a935472507452d09d33d`

The scaffold checklist is `21 total`, `21 passed`, `0 failed`, `0 blockers`.
The provider-bound candidate retains the scaffold digest as
`previous_scaffold_candidate_digest` and does not mutate any frozen authority
digest.

## Fixed Segment

The candidate binds to:

- ticker: `AAPL`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- primary MIC: `XNAS`
- security type: `CS`
- segment range: `2022-01-01` through `2025-12-31`

## Provider Evidence Collection Status

Provider evidence binding supports two modes:

- response injection
- live provider request

The live adapter uses:

`GET /stocks/v1/splits`

Provider metadata records:

- provider: `MASSIVE.COM`
- endpoint stability: `CURRENT_STOCKS_V1_SPLITS`
- provider request mode: `LIVE_PROVIDER_REQUEST`
- ticker filter: `AAPL`
- execution date filters: `2022-01-01` through `2025-12-31`
- sort: `execution_date.asc`
- limit: `5000`

Live execution is blocked unless:

`MARKETFLOW_ENABLE_LIVE_SPLIT_AUDIT=1`

An API key is accepted from an explicit function argument or from existing
environment conventions:

- `MASSIVE_API_KEY`
- `POLYGON_API_KEY`

API keys are wrapped by the existing `ProviderApiKey` boundary and are not
stored in candidate artifacts, request metadata, raw response objects, timeline
objects, receipts, logs, or tests.

The default pytest suite uses fake transport only. It does not depend on live
provider availability and does not perform network access.

Injected provider response data produces a provider-bound candidate that
records:

- `provider_evidence_required`: `true`
- `provider_evidence_status`: `BOUND`
- `provider_request_performed_in_this_task`: `false`
- `provider_requests_made`: `false`
- `provider_response_injected`: `true`
- `split_events_provider_evidence_bound`: `true`
- `split_event_audit_complete`: `true`
- `split_event_audit_frozen`: `false`
- provider endpoint: `null`
- provider endpoint stability:
  `SPLIT_ENDPOINT_ADAPTER_REQUIRED_NOT_LIVE_VERIFIED`
- provider endpoint limitation:
  `NO_SAFE_EXISTING_SPLIT_EVENT_PROVIDER_ENDPOINT_ADAPTER_IN_REPOSITORY`
- provider query ticker: `AAPL`
- provider query Composite FIGI: `BBG000B9XRY4`
- provider query range: `2022-01-01` through `2025-12-31`
- deterministic raw response, timeline, receipt, and candidate digests

Live provider response data produces a provider-bound candidate that records:

- `provider_requests_made`: `true`
- `provider_response_injected`: `false`
- `provider_request_mode`: `LIVE_PROVIDER_REQUEST`
- `split_events_provider_evidence_bound`: `true`
- `split_event_audit_complete`: `true`
- `split_event_audit_frozen`: `false`
- deterministic raw response, timeline, receipt, and candidate digests
- sanitized provider request metadata
- provider raw response page count and row count

The provider evidence object includes:

- `provider_name`
- `provider_endpoint`
- `provider_endpoint_stability`
- `provider_query_identifier`
- `provider_query_ticker`
- `provider_query_composite_figi`
- `provider_query_start`
- `provider_query_end`
- `provider_request_timestamp_utc`
- `provider_request_mode`
- `provider_response_artifact_id`
- `provider_raw_response_digest`
- `provider_raw_response_row_count`
- `provider_response_status`

## Live Adapter Scope

The live adapter is intentionally small and bounded:

- It requests only Massive.com stock split evidence for the fixed AAPL segment.
- It does not call Ticker Overview, Ticker Events, calendar, dividends, custom
  bars, registry, Strategy, runtime, or broker paths.
- It supports fake transport for deterministic tests.
- It rejects credential-like query parameters and untrusted pagination URLs.
- It supports `next_url` pagination only for the expected Massive host, scheme,
  path, and query shape.
- It stores sanitized request metadata only.

Pagination support is bounded by a safe page limit. If the provider returns
more pages than the limit, collection fails closed.

## Event Timeline

The provider-bound candidate builds a deterministic split-event timeline from
the injected response rows.

Each event records:

- `execution_date`
- `declaration_date`
- `record_date`
- `payable_date`
- `split_from`
- `split_to`
- `split_ratio`
- `ticker`
- `composite_figi_if_available`
- `raw_event_index`
- `raw_event_digest`
- `event_position`

Missing provider fields remain `null`. The service does not fabricate missing
provider values from the fixed identity segment.

Event position is classified as:

- `PRE_RANGE`
- `IN_RANGE`
- `POST_RANGE`
- `UNKNOWN`

Counts are derived from provider response rows:

- `split_event_count_total`
- `split_event_count_pre_range`
- `split_event_count_in_range`
- `split_event_count_post_range`
- `split_event_count_unknown`

## Audit Status Meanings

Provider-bound candidates use these audit statuses:

- `SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT`: provider evidence is
  bound and the in-range split count is zero.
- `SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT`: provider evidence is bound
  and the in-range split count is greater than zero.
- `SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE`: provider evidence is bound
  but one or more split events cannot be positioned in the fixed range.

The next required task is:

`SPLIT_EVENT_OPERATOR_REVIEW_PACKAGE`

## Authority Boundary

The scaffold and provider-bound candidate preserve these boundaries:

- `identity_segment_frozen`: `true`
- `calendar_operator_frozen`: `true`
- `split_event_audit_frozen`: `false`
- `dividend_event_audit_frozen`: `false`
- `canonical_eligibility`: `false`
- `registry_eligibility`: `false`
- `acquisition_generation_freeze`: `false`
- `strategy_runtime_migration`: `false`
- `automatic_stitching`: `false`
- predictive usefulness: not accepted
- profitability: not accepted

## Non-Goals

This phase does not make live provider requests by default, call Ticker
Overview, call Ticker Events, call Dividends, call Custom Bars, refresh calendar
source evidence, generate acquisition bars, freeze split evidence, approve
canonical or registry eligibility, or modify Strategy/runtime/broker/execution
logic.

No raw provider payloads are copied, rewritten, regenerated, or committed by
default tests.

## Next Tasks

1. Split-event operator review package.
2. Split-event operator freeze ceremony.
3. Dividend-event audit candidate.
