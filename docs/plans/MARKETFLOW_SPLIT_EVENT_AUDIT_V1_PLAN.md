# MarketFlow Split-Event Audit v1 Plan

Status: OFFLINE SCAFFOLD / CONTRACT IMPLEMENTED

## Purpose

Split-Event Audit Evidence Candidate v1 creates an offline scaffold artifact
for the future provider-backed split-event audit chain.

It creates only:

`SPLIT_EVENT_AUDIT_CANDIDATE`

with status:

`SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE`

It does not claim that the split audit is complete, does not assert zero split
events, does not assert in-range split events, and does not create
`SPLIT_EVENT_AUDIT_FROZEN`.

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

## Fixed Segment

The candidate binds to:

- ticker: `AAPL`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- primary MIC: `XNAS`
- security type: `CS`
- segment range: `2022-01-01` through `2025-12-31`

## Provider Evidence

No provider evidence is collected in this task.

The candidate records:

- `provider_evidence_required`: `true`
- `provider_evidence_status`: `NOT_BOUND`
- `provider_request_performed_in_this_task`: `false`
- provider endpoint/query identifiers: `null`
- raw response/timeline/receipt artifact IDs and digests: `null`
- split event counts: `null`
- split events: empty
- audit status: `null`

The next required task is:

`SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION`

## Authority Boundary

The scaffold preserves these boundaries:

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

This phase does not make provider requests, call Massive.com, call Polygon,
call Ticker Details, call Ticker Events, call Splits, call Dividends, call
Corporate Actions, refresh source evidence, generate acquisition bars, freeze
split evidence, approve canonical or registry eligibility, or modify
Strategy/runtime/broker/execution logic.

No raw provider payloads are copied, rewritten, regenerated, or committed.

## Next Tasks

1. Split-event provider evidence collection.
2. Split-event audit candidate with bound provider evidence.
3. Split-event operator review package.
4. Split-event operator freeze ceremony.
5. Dividend-event audit chain.
