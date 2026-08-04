# MarketFlow Identity Segment Evidence Freeze v1 Plan

Status: IMPLEMENTED WITH OPERATOR REVIEW PACKAGE PLAN

## Purpose

MarketFlow Identity Segment Evidence Freeze v1 creates an offline,
reference-only `IDENTITY_SEGMENT_CANDIDATE` for operator review of the fixed
AAPL identity segment:

- ticker: `AAPL`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- primary MIC: `XNAS`
- security type: `CS`
- segment range: `2022-01-01` through `2025-12-31`

The candidate status is
`IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW`.

The candidate implementation is present in
`marketflow/services/identity_segment_freeze_service.py`. It creates only
`IDENTITY_SEGMENT_CANDIDATE`; it does not create `IDENTITY_SEGMENT_FROZEN`.
The accepted candidate semantic digest is:

`263902ddc149728d095a4f8bc941c92a82c2d4360e0a038d231e0eac6c70dc57`

## Evidence Bound

The candidate binds accepted evidence by reference only:

- `CORE ACQUISITION CONTRACT v2.1`
- contract digest:
  `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`
- identity run: `ident-509de6e2eb5e4a1db785e034bcfaf045`
- continuity artifact: `ident-art-8607986a2341423182614a41c6236ed9`
- start snapshot digest:
  `75a3fb5cccda09c05001129ec7161ad479457a714a5903828c67c5cfeb965928`
- end snapshot digest:
  `5e80a556b6172d8ca8985177f8c17e05183322fb5981ba92def57d4698aa4f50`
- Ticker Events audit run:
  `tkev-959a591271874fe49bc8cb34bb29be36`
- Ticker Events raw response artifact:
  `tkev-art-5d8ed7c1aa0e451ab1c7b297230dca33`
- Ticker Events raw response digest:
  `07082085e9e41c467e020774954c045e83613d9581976ca26e87b74e3bbf15dc`
- Ticker Events timeline artifact:
  `tkev-art-54a14c247fb2459a9c588dd4695b4358`
- Ticker Events timeline digest:
  `36ccff35908df36a7fadb124d6cb846e4ac0cace578830e7591f7edf92bde820`
- Ticker Events audit artifact:
  `tkev-art-df20d0c474464b74a28a6f4ed451fef6`
- Ticker Events receipt artifact:
  `tkev-art-2168e3f7caec46d59436ab0e4280d49d`

The accepted January 2025 monthly source evidence is also referenced,
including 1277 normalized rows, 757 extended-hours rows, 520 expected RTH
rows, 520 validated RTH rows, `RTH_SOURCE_ROWS_RECONCILED`, 20 full ordinary
sessions, zero incomplete ordinary sessions, 40 `SWING` half-session bars,
20 `POSITION_SWING` full-session bars, requested calendar `XNAS`, resolved
calendar `XNYS`, alias `XNAS_USES_XNYS_SCHEDULE`, and calendar authority
`NOT_OPERATOR_FROZEN`.

## Authority Boundary

The candidate preserves these boundaries:

- `identity_continuity_evidence`: `SUPPORTED_AS_CANDIDATE`
- `identity_segment_frozen`: `false`
- `calendar_operator_frozen`: `false`
- `canonical_eligibility`: `false`
- `registry_eligibility`: `false`
- `acquisition_generation_freeze`: `false`
- `strategy_runtime_migration`: `false`
- `automatic_stitching`: `false`
- predictive usefulness: not accepted
- profitability: not accepted

## Why Not Frozen Yet

This task prepares evidence for operator review only. It does not create
`IDENTITY_SEGMENT_FROZEN`, populate operator approval fields, record a freeze
timestamp, or identify a freeze operator. A later digest-bound operator
ceremony is required before any frozen identity segment can exist.

The Ticker Events evidence remains supporting evidence from an experimental
endpoint. The returned `2003-09-10` `ticker_change` event is before the fixed
contract range and the in-range event count is zero, but this does not
authorize automatic stitching.

## Operator Review Package

Identity Segment Candidate Operator Review Package v1 adds an offline,
digest-bound review artifact:

`IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE`

with status:

`IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY`

The review package verifies and summarizes the candidate kind, candidate
status, candidate semantic digest, segment fields, bound identity evidence,
bound Ticker Events evidence, authority flags, reference-only guardrails, and
remaining tasks before any future operator freeze ceremony.

The review package may mark the evidence ready for operator assessment when
all software checks pass, but it does not approve a freeze. It keeps
`operator_decision` null, `identity_segment_frozen` false, and
`software_freeze_authorized` false. The next freeze step remains a separate
digest-bound operator ceremony.

## Non-Goals

This phase does not make provider requests, call Ticker Overview, call Ticker
Events, refresh calendars, fetch splits or dividends, generate acquisition
data, freeze calendar evidence, approve canonical registry eligibility, modify
Strategy runtime behavior, or accept predictive usefulness or profitability.

No raw provider payloads are copied, rewritten, regenerated, or committed.
