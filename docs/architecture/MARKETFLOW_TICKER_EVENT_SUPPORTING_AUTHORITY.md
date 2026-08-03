# MarketFlow Ticker Event Supporting Authority

MarketFlow Ticker Events Supporting Audit v1 is a source-authority supplement
for the accepted AAPL point-in-time identity evidence. It is not an identity
registry and does not replace the fixed Ticker Overview snapshots.

## Authority Model

Ticker Events evidence can support a continuity candidate only when the
experimental endpoint returns a structurally valid event array and no inclusive
contract-range ticker-change event is reported.

The supporting status is:

`IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE`

This status does not mean identity segment frozen, canonical approved, registry
eligible, acquisition-generation eligible, or Strategy authorized.

## Range Classification

Events are canonicalized by date, event type, and reported ticker. Each event is
classified as:

- `BEFORE_CONTRACT_RANGE`
- `WITHIN_CONTRACT_RANGE`
- `AFTER_CONTRACT_RANGE`

Any ticker-change event inside the inclusive `2022-01-01` through `2025-12-31`
range requires segment review. The system performs no automatic stitching and
does not infer prior or next ticker intervals beyond the endpoint evidence.

## Artifact Lineage

Ticker Events artifacts use a separate manifest schema:

`marketflow.ticker_event_audit_artifact_manifest.v1`

The chain is:

`TICKER_EVENTS_RAW_RESPONSE -> TICKER_EVENT_TIMELINE -> TICKER_EVENT_AUDIT_CANDIDATE -> TICKER_EVENT_AUDIT_RECEIPT`

The accepted identity continuity artifact is referenced by exact source run,
artifact ID, and semantic digest. It is not copied into the ticker-events run.

## Experimental Boundary

The endpoint stability is always recorded as `EXPERIMENTAL`. Endpoint
unavailability, malformed schema, missing `events`, or rejected status is not
treated as evidence that no ticker changes occurred.
