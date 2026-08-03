# MarketFlow Instrument Identity Evidence Status

Status: LIVE EVIDENCE ACCEPTED AS NONCANONICAL CANDIDATE

## Scope Result

MarketFlow Instrument Identity Evidence v1 adds offline tooling for two fixed
Massive.com Ticker Overview snapshots for `AAPL`:

- start snapshot date: `2022-01-01`
- end snapshot date: `2025-12-31`

The evidence classification remains:

`PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL`

## Offline Result

The implementation provides:

- immutable identity specification and deterministic specification digest;
- fixed request construction for `GET /v3/reference/tickers/AAPL` with one
  point-in-time `date` query parameter;
- strict Ticker Overview response parsing with unknown-field fail-closed
  behavior;
- bounded raw response and identity projection artifacts under the ignored
  source-authority runtime root;
- deterministic start/end continuity comparison;
- sanitized public receipt generation;
- offline plan and mock-only self-check commands;
- a controlled live-run boundary that is implemented but not executed here.

## Current Evidence State

The original offline tooling acceptance remains historically true:

No live identity request occurred in that task.

No actual Massive.com key was requested, inspected, read from the environment,
or printed in that task.

The corrected controlled live run has been accepted offline as noncanonical
candidate evidence in
`docs/status/MARKETFLOW_INSTRUMENT_IDENTITY_LIVE_EVIDENCE_ACCEPTANCE.md`.

The accepted runtime chain contains the source-authorized six manifests:

- `TICKER_OVERVIEW_RAW_RESPONSE`: 2
- `TICKER_OVERVIEW_SNAPSHOT`: 2
- `IDENTITY_CONTINUITY_CANDIDATE`: 1
- `INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT`: 1

The corrected acceptance did not execute another provider request, request or
inspect credentials, expose raw provider bodies, or modify production source.

## Repository-Root Correction

A later controlled local live attempt accepted the digest-bound confirmation
phrase and prompted for the API key too early, then failed before any provider
request with:

`INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED`

The defect was a fragile `pyproject.toml` repository marker. This checkout has
valid fixed evidence but no `pyproject.toml`, so the previous root helper could
not resolve the source checkout. The corrected helper derives the root from the
identity source module path and validates `AGENTS.md`, `requirements.txt`, the
identity module file, and `config/fixed_date_acquisition_contract_v2_1.toml`.

The live command now performs nonsecret repository/runtime preflight after
operator confirmation and before `getpass`, secret-wrapper construction,
transport construction, runtime-directory creation, or provider request.
Expected local failures return a sanitized receipt without traceback, absolute
path, exception text, URL, request ID, API key, or Authorization header.

No provider request was completed by the failed attempt, and no identity
artifact or snapshot was accepted from it.

Ticker Events audit remains:

`TICKER_EVENT_AUDIT_NOT_IMPLEMENTED`

Identity continuity is therefore a candidate result only. It is not a frozen
identity segment and does not create canonical registry authority.

## Pending Authority

The following remain outside this phase:

- Ticker Events continuity audit;
- split and dividend evidence;
- calendar and RTH authority freeze;
- canonical registry approval;
- production source authorization for Strategy;
- Monte Carlo, outcomes, broker, execution, and performance paths.

## Live Evidence Acceptance

The required post-correction live evidence run has been completed and accepted
offline as a sanitized noncanonical candidate. It still cannot freeze identity
authority without the remaining evidence.

The previous repository-root correction status said:

Final live identity tooling acceptance remains `BLOCKED`

That block is superseded by the corrected live-evidence acceptance document.
