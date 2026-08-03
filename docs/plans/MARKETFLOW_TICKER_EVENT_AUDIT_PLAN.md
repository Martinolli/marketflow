# MarketFlow Ticker Events Supporting Audit v1 Plan

Status: IMPLEMENTATION PLAN

## Scope

MarketFlow Ticker Events Supporting Audit v1 adds offline tooling and a
controlled-live boundary for Massive.com's experimental Ticker Events endpoint.
The audit is supporting evidence for the already accepted AAPL point-in-time
identity snapshots. It does not replace those snapshots, create final identity
authority, or automatically stitch identities.

Fixed source identity evidence:

- identity run ID: `ident-509de6e2eb5e4a1db785e034bcfaf045`
- continuity artifact ID: `ident-art-8607986a2341423182614a41c6236ed9`
- continuity status: `IDENTITY_CONTINUITY_SUPPORTED`
- ticker context: `AAPL`
- contract boundary: `2022-01-01` through `2025-12-31`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- primary exchange: `XNAS`
- security type: `CS`

## Fixed Specification

The audit specification is immutable:

- schema: `marketflow.ticker_event_audit_specification.v1`
- classification: `PROVIDER_TICKER_EVENT_AUDIT_CANDIDATE_NONCANONICAL`
- provider: `MASSIVE.COM`
- endpoint family: `TICKER_EVENTS_EXPERIMENTAL_VX`
- endpoint stability: `EXPERIMENTAL`
- query identifier type: `COMPOSITE_FIGI`
- query identifier: `BBG000B9XRY4`
- event type: `ticker_change`

No caller, CLI, environment, identifier, ticker, date, event-type, host, path,
version, root, run-ID, transport, or credential override is public.

## Source Evidence Binding

Before any live audit request, local preflight validates the exact accepted
six-manifest instrument identity chain:

- `TICKER_OVERVIEW_RAW_RESPONSE`: 2
- `TICKER_OVERVIEW_SNAPSHOT`: 2
- `IDENTITY_CONTINUITY_CANDIDATE`: 1
- `INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT`: 1

Validation checks manifest schema, common run ID, artifact IDs, path
containment, regular-file payloads, byte size, SHA-256, semantic digests, and
lineage. Raw Ticker Overview provider bodies are not printed or copied.

## Request Boundary

The controlled live command is implemented but must not be executed during this
task. Its fixed request is one Massive.com Ticker Events request using the
Composite FIGI path identifier and `types=ticker_change`. It uses bearer-header
authentication only, `Accept: application/json`, `Accept-Encoding: identity`,
TLS verification, redirects disabled, `trust_env=False`, no cookies, no retry,
no pagination, and no endpoint-version substitution.

The endpoint is experimental. Endpoint unavailability or incomplete evidence is
not treated as proof of no ticker changes.

## Evidence Artifacts

Ticker Events artifacts use:

`marketflow.ticker_event_audit_artifact_manifest.v1`

The new runtime root is repository-derived:

`.marketflow/source_authority/ticker_events/runs/`

The audit chain is:

`TICKER_EVENTS_RAW_RESPONSE -> TICKER_EVENT_TIMELINE -> TICKER_EVENT_AUDIT_CANDIDATE -> TICKER_EVENT_AUDIT_RECEIPT`

The accepted identity continuity artifact remains an external source-authority
parent by exact ID and digest. It is not copied into the new run.

## Authority Boundary

When no in-range ticker-change event is reported, the combined candidate status
is:

`IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE`

That still does not freeze an identity segment, approve canonical registry
authority, authorize acquisition generation, or enable Strategy.

Calendar, splits, dividends, registry, and Strategy remain pending.
