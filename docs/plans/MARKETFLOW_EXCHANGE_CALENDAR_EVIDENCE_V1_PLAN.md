# MarketFlow Exchange Calendar Evidence v1 Plan

Status: IMPLEMENTED AS CANDIDATE WITH OPERATOR REVIEW PACKAGE PLAN

## Purpose

Exchange Calendar Evidence Candidate v1 creates an offline, digest-bound
calendar evidence candidate for the frozen AAPL identity segment and fixed
`CORE ACQUISITION CONTRACT v2.1`.

It creates only:

`EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE`

with status:

`EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW`

It does not create `EXCHANGE_CALENDAR_FROZEN`, and it does not set
`calendar_operator_frozen` to `true`.

## Frozen Identity Segment Relationship

The candidate binds to the frozen AAPL identity segment:

- ticker: `AAPL`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- primary MIC: `XNAS`
- security type: `CS`
- segment range: `2022-01-01` through `2025-12-31`
- frozen identity segment digest:
  `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`

The acquisition contract digest remains:

`538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`

## Requested and Resolved Calendar

The candidate preserves the accepted calendar alias relationship:

- requested calendar: `XNAS`
- resolved calendar: `XNYS`
- alias: `XNAS_USES_XNYS_SCHEDULE`
- calendar timezone: `America/New_York`
- canonical storage timezone: `UTC`
- calendar source library: `exchange_calendars`
- calendar source library version: `4.13.2`
- calendar authority status: `NOT_OPERATOR_FROZEN`

The deterministic candidate digest is:

`867aa02ad9c9c737eda3d8398eda4e4aad3181cd4bc5505600ccf9647b0d60ee`

The deterministic schedule digest is:

`b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`

## Schedule Coverage

The candidate summarizes deterministic XNYS schedule evidence for
`2022-01-01` through `2025-12-31`:

- open sessions: `1003`
- full sessions: `994`
- half sessions: `9`
- special closes: `9`
- special opens: `0`
- first session: `2022-01-03`
- last session: `2025-12-31`

The full schedule row list is built by the service helper for validation and
digesting, but no generated runtime schedule artifact is committed by this
plan.

## Monthly 2025-01 Cross-Check

The candidate preserves the accepted live monthly source evidence cross-check:

- normalized source rows: `1277`
- extended-hours rows: `757`
- expected RTH rows: `520`
- validated RTH rows: `520`
- RTH reconciliation: `RTH_SOURCE_ROWS_RECONCILED`
- full ordinary sessions: `20`
- incomplete ordinary sessions: `0`
- `SWING` RTH half-session 195m bars: `40`
- `POSITION_SWING` RTH full-session 1d bars: `20`

## Authority Boundary

The candidate preserves these boundaries:

- `identity_segment_frozen`: `true`
- `calendar_operator_frozen`: `false`
- `canonical_eligibility`: `false`
- `registry_eligibility`: `false`
- `acquisition_generation_freeze`: `false`
- `strategy_runtime_migration`: `false`
- `automatic_stitching`: `false`
- predictive usefulness: not accepted
- profitability: not accepted

## Non-Goals

This phase does not make provider requests, call Massive.com, call Polygon,
call Ticker Overview, call Ticker Events, fetch split or dividend events,
generate acquisition bars, freeze calendar evidence, approve canonical or
registry eligibility, or modify Strategy/runtime/broker/execution logic.

No raw provider payloads are copied, rewritten, regenerated, or committed.

## Next Steps

## Operator Review Package

Exchange Calendar Evidence Operator Review Package v1 adds an offline,
digest-bound review artifact:

`EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE`

with status:

`EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY`

The review package verifies and summarizes the calendar candidate kind,
candidate status, calendar candidate digest, schedule digest, frozen identity
segment binding, calendar alias binding, schedule coverage, accepted 2025-01
monthly cross-check, authority flags, guardrails, and remaining tasks before
any future calendar freeze ceremony.

The accepted review package semantic digest is:

`5e7e528068cd161e06a7a3cf6b30c40909023f23eb6b64661abb063363a690cb`

The review package may mark the calendar evidence ready for operator
assessment when all software checks pass, but it does not approve a freeze. It
keeps `operator_decision` null, `calendar_operator_frozen` false, and
`software_freeze_authorized` false.

## Next Steps

The next step is a separate digest-bound exchange calendar operator freeze
ceremony. That later ceremony is required before any `EXCHANGE_CALENDAR_FROZEN`
artifact or `calendar_operator_frozen = true` state can exist.
