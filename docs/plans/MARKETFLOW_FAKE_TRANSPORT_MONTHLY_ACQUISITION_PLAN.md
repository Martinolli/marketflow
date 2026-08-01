# MarketFlow Fake-Transport Monthly Acquisition Plan

## Authority Boundary

This plan authorizes an offline, deterministic fake-transport executor for one
calendar-month acquisition request. It does not authorize provider execution,
credential inspection, provider account inspection, SDK installation or SDK
migration, registry writes, strategy semantics, runtime ingestion, or live data
download.

Provider business identity is represented as Massive.com. Legacy Polygon
adapter/package naming is preserved only where it accurately describes existing
installed code or adapter-family references.

## Fixed Contract Inputs

- Base acquisition contract: `marketflow.acquisition_contract.v2`
- Timestamp contract: `marketflow.acquisition_contract.v2.1`
- v2 digest: `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`
- v2.1 digest: `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`
- Provider execution enabled: `false`
- Provider entitlement status: `OPERATOR_ATTESTED_CONFIRMED`
- Source bars: 15-minute Massive.com stock aggregates, adjusted, ascending, limit
  50000, provider timestamp `t` as start-of-window Unix epoch milliseconds.

## Implementation Plan

1. Add a strict fake transport that consumes scripted request/outcome pairs in
   order, rejects unexpected requests, retains unconsumed responses as failures,
   and exposes no real URL, DNS, socket, credential, SDK, or provider client path.
2. Add strict provider-response parsing that uses `Decimal` JSON parsing,
   rejects NaN/Infinity, rejects numeric strings and bool-as-int values, validates
   exact 15-minute timestamp windows, and produces a semantic retry projection.
3. Add a monthly acquisition executor that builds one fixed month request,
   constructs logical page identities, records all immutable attempts, applies
   retry and Retry-After policy, preserves exact raw response bytes, validates
   pagination, emits a completeness manifest, and normalizes only from that
   manifest.
4. Add paired normalized artifacts:
   `MONTH_NORMALIZED_15M_OHLCV` and
   `MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS`, with matching timestamps and row
   counts.
5. Add sanitized receipts with no raw OHLCV, raw body, raw URL, credentials,
   account data, absolute paths, or raw exception strings.
6. Add a dry CLI self-check, `--monthly-acquisition-self-check`, that uses only
   temporary fake data, performs no sleep, and leaves no persistent artifacts.
7. Add focused offline tests for retry, pagination, parsing, semantic equivalence,
   artifact lineage, sanitization, source-assurance boundaries, and CLI behavior.

## Retry and Blocking Policy

Retryable categories are exactly:

- `TRANSPORT_TIMEOUT`
- `CONNECTION_RESET`
- `HTTP_408`
- `HTTP_429`
- `HTTP_500`
- `HTTP_502`
- `HTTP_503`
- `HTTP_504`

Maximum attempts are three. Configured backoffs are two and five seconds. Jitter
is disabled. Retry-After is valid only for HTTP 429 and HTTP 503 as an integer
from 0 through 60 seconds. The effective delay is the maximum of configured
backoff and Retry-After. Malformed, negative, non-integer, or greater-than-60
values block with `RETRY_AFTER_POLICY_VIOLATION`. No delay is recorded after a
final attempt.

Non-retryable failures block the logical page and month. These include
authentication, authorization, invalid request, unsupported ticker, schema
failure, semantic mismatch, adjustment mismatch, invalid timestamp/OHLCV,
provider response variance, and pagination invalidity.

## Artifact Plan

Monthly acquisition uses a separate schema:
`marketflow.monthly_acquisition_artifact_manifest.v1`.

Artifact types:

- `MONTH_CHUNK_REQUEST_CONTRACT`
- `REQUEST_ATTEMPT_RECORD`
- `RAW_PROVIDER_PAGE`
- `MONTH_CHUNK_COMPLETENESS_MANIFEST`
- `MONTH_NORMALIZED_15M_OHLCV`
- `MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS`
- `MONTH_ACQUISITION_RECEIPT`

Every downstream artifact binds explicit parent manifest references and
artifact IDs. The executor validates lineage from the exact emitted manifest
references; it never discovers artifacts by glob or timestamp ordering.

## Acceptance Scope

The acceptance target is deterministic local tooling correctness, not provider
connectivity, profitability, predictive readiness, full historical coverage, or
normal runtime acquisition enablement.
