# MarketFlow Acquisition Generation Candidate v1 Plan

Status: LIVE GENERATION COMPLETED / TARGETED TRIAGE COMPLETED / OPERATOR REVIEW PACKAGE COMPLETED / OPERATOR FREEZE CEREMONY IMPLEMENTED

## Purpose

Acquisition Generation Candidate v1 creates a candidate artifact for fixed AAPL
2022-01-01 through 2025-12-31 15-minute adjusted custom bars. It prepares
provider-backed acquisition evidence for later operator review.

It creates only:

`ACQUISITION_GENERATION_CANDIDATE`

with candidate status:

`ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW`

for completed injected or fake provider-response evidence, or:

`ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION`

when no provider responses are supplied.

It does not create `ACQUISITION_GENERATION_FROZEN` and does not approve
canonical eligibility, registry eligibility, acquisition-generation freeze, or
Strategy/runtime migration.

## Prerequisite Authority Chain

The candidate binds to the frozen authority chain:

- identity frozen digest:
  `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- exchange calendar frozen digest:
  `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- schedule digest:
  `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- split-event audit frozen digest:
  `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- dividend-event audit frozen digest:
  `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`

## Endpoint And Contract

Provider endpoint boundary:

`GET /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}`

Fixed query:

- ticker: `AAPL`
- multiplier: `15`
- timespan: `minute`
- adjusted: `true`
- sort: `asc`
- limit: `50000`
- source: `Massive.com Custom Bars`
- source timestamps: aggregate-window starts
- source timezone: `America/New_York`
- canonical storage timezone: `UTC`
- acquisition contract digest:
  `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`

Request metadata is sanitized and does not store API keys.

## Monthly Chunking

The candidate uses deterministic monthly chunking:

- chunking strategy: `MONTHLY`
- chunk count expected: `48`
- first chunk: `2022-01`
- last chunk: `2025-12`

Each chunk records request metadata, response status, row count, raw digest,
projection digest, and request semantic digest.

## Normalized Source Rows

Provider aggregate rows are normalized into deterministic source rows with:

- ticker
- UTC canonical timestamp
- provider source timestamp
- source timezone
- OHLCV
- optional VWAP, transactions, and OTC fields
- adjusted flag
- source interval minutes
- source row index
- source chunk id
- raw row digest

Missing optional provider fields remain `null`.

## RTH And Extended-Hours Reconciliation

Rows are classified against the frozen XNAS/XNYS schedule as:

- `RTH`
- `EXTENDED_HOURS`
- `OUT_OF_CALENDAR_RANGE`
- `UNKNOWN`

Extended-hours rows are preserved and counted. They are not discarded in this
candidate layer.

The deterministic fake fixture produced:

- normalized source rows: `1324`
- RTH rows: `520`
- extended-hours rows: `788`
- out-of-calendar-range rows: `16`
- unknown-session rows: `0`

## Accepted 2025-01 Cross-Check

The fixture validates the accepted 2025-01 source evidence exactly:

- normalized source rows: `1277`
- extended-hours rows: `757`
- expected RTH rows: `520`
- validated RTH rows: `520`
- RTH reconciliation: `RTH_SOURCE_ROWS_RECONCILED`
- full ordinary sessions: `20`
- incomplete ordinary sessions: `0`
- SWING RTH half-session bars: `40`
- POSITION_SWING RTH full-session bars: `20`
- requested calendar: `XNAS`
- resolved calendar: `XNYS`
- alias: `XNAS_USES_XNYS_SCHEDULE`

## Candidate Evidence Digests

Deterministic fake-transport candidate evidence:

- acquisition candidate digest:
  `bb5230258b61d8819492cb6be8932ddac30cfb741dbbec88f8b418da4db31c87`
- provider raw response digest:
  `0cd56d1a336ae65a70598a36371fdeb0993cf704ca2e60f498092cf16ec20a1f`
- normalized source rows digest:
  `74639a8316892e2c635130808f791580e8701ed9036876a456031ded0406ca32`
- monthly reconciliation digest:
  `7027d080ae996a1e24588327d052f3615cdf6582bf6d140cc57a01c23f48adb7`
- acquisition generation receipt digest:
  `573e071ca9084e46555773e6ca74a0b1b9ac5909f6faed5c10067dc25b6fe80e`

That fixture evidence remains test evidence only. The recorded live generation
evidence below supersedes it for operator review.

Recorded full live 2022-2025 acquisition evidence:

- acquisition candidate digest:
  `5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb`
- chunk manifest digest:
  `8a4bf37f501fb7da5ea23e04d5ebe90da2cdfda1bf9e06e55e4c459be53fa374`
- provider raw response digest:
  `aea820006bb458b9e51a1cda23ae24be02f476aafb36bec6c65d3740812d06c7`
- normalized source rows digest:
  `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- monthly reconciliation digest:
  `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- acquisition receipt digest:
  `63b1934fbaf4b146fadcfbb5cb4649e18b1e91d8d304cf3afdee71220d005eed`

The full live generation completed `48` of `48` chunks with `0` failed chunks.
It produced `63804` raw rows, `63804` normalized rows, `25970` RTH rows,
`37834` extended-hours rows, and `0` out-of-calendar/unknown rows.

## Targeted Per-Session Triage

The targeted per-session diagnostic rerun completed the 9 previously
non-reconciled months and found all target sessions reconciled at session
level:

- acquisition operator review status: `READY_AFTER_TRIAGE`
- all monthly mismatches explained: `true`
- mismatch explanation: `EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION`
- per-session issue summary: `{"RECONCILED":188}`
- per-session severity summary: `{"INFO":188}`
- targeted diagnostic receipt digest:
  `82ec97bbc5eba73a275cc8221bb4a59235ed093a6e6dbe14058eac26980d26c8`

## Operator Review Package

Acquisition Generation Operator Review Package v1 is implemented as an
offline, digest-bound review layer:

- artifact kind: `ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE`
- review status: `ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY`
- provider requests made in review: `false`
- review package status:
  `docs/status/MARKETFLOW_ACQUISITION_GENERATION_OPERATOR_REVIEW_PACKAGE_STATUS.md`

The review package makes the candidate ready for human operator assessment,
but it does not authorize software freeze, canonical eligibility, registry
eligibility, or runtime migration.

## Operator Freeze Ceremony

Acquisition Generation Operator Freeze Ceremony v1 is implemented as a guarded
offline ceremony:

- artifact kind: `ACQUISITION_GENERATION_FROZEN`
- freeze status: `ACQUISITION_GENERATION_FROZEN`
- acquisition generation freeze: `true`
- provider requests made in freeze: `false`
- frozen status:
  `docs/status/MARKETFLOW_ACQUISITION_GENERATION_OPERATOR_FREEZE_STATUS.md`

Only the acquisition generation evidence is frozen. Canonical eligibility,
registry eligibility, Strategy/runtime migration, automatic stitching,
predictive usefulness, and profitability remain not approved.

The next implementation step is a SWING canonical dataset candidate, followed
by SWING/POSITION_SWING review and registry approval work.

## Dividend Implication

The candidate preserves the frozen dividend-event implication:

- in-range dividends found: `true`
- in-range dividend count: `16`
- implication:
  `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`

This implication is not canonical approval and not acquisition-generation
freeze approval.

## Non-Goals

This candidate does not:

- refresh identity, calendar, split, dividend, Ticker Overview, or Ticker
  Events evidence
- approve canonical eligibility
- approve registry eligibility
- migrate Strategy/runtime logic
- assert predictive usefulness
- assert profitability
- perform broker or trading functions
- commit generated raw bars or large CSV artifacts

## Next Tasks

1. Digest-bound acquisition generation operator freeze ceremony.
2. SWING canonical dataset candidate.
3. SWING canonical dataset operator review/freeze.
4. SWING registry approval.
5. POSITION_SWING canonical dataset candidate.
6. POSITION_SWING canonical dataset operator review/freeze.
7. POSITION_SWING registry approval.
8. Normal runtime migration.
9. Applicability/research campaign.
10. Predictive and profitability evaluation.
