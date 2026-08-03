# MarketFlow Instrument Identity Evidence Plan

## Scope

Implement offline tooling for `marketflow.instrument_identity_specification.v1`
using two fixed Massive.com Ticker Overview snapshots for `AAPL`:

- start snapshot date: `2022-01-01`
- end snapshot date: `2025-12-31`

This phase creates noncanonical source-authority candidate evidence only. It
does not perform a live provider request, inspect credentials, call Ticker
Events, run splits/dividends, freeze calendar authority, update registry
authority, or enable Strategy/performance/runtime migration.

## Fixed Boundaries

- Provider business identity: `MASSIVE.COM`.
- Endpoint family: `TICKER_OVERVIEW_V3`.
- Endpoint: `GET https://api.massive.com/v3/reference/tickers/AAPL`.
- Query: exactly one `date=YYYY-MM-DD` parameter.
- Authentication: bearer header only.
- HTTP client: `httpx` with redirects disabled, `trust_env=False`, TLS
  verification enabled, no cookies, and no retry inside the identity
  transport.
- Runtime artifacts: `.marketflow/source_authority/identity/runs/`.
- CLI overrides: none for ticker, dates, provider, host, endpoint, root, key,
  market, locale, or currency.

## Implementation Steps

1. Add `marketflow/source_authority` with immutable specification, request,
   parser, raw-response artifact, projection artifact, continuity, receipt,
   and CLI code.
2. Use mock-only tests for transport, parsing, artifact persistence, CLI plan,
   self-check, and controlled live-run boundaries.
3. Preserve existing historical-data transport, monthly acquisition, calendar,
   RTH, Contract v1/v2/v2.1, Strategy, Monte Carlo, outcome, registry, and
   runtime behavior.
4. Document authority boundaries, credential handling, and current noncanonical
   status.

## Acceptance

Tooling passes only when deterministic offline tests prove:

- fixed AAPL/two-date specification and deterministic digest;
- exact Ticker Overview request construction with no API key in URL;
- strict top-level and result-field parsing;
- immutable raw response and sanitized snapshot artifacts with saved-disk
  validation before identity projection;
- start/end continuity comparison with no automatic stitching;
- Ticker Events audit remains `TICKER_EVENT_AUDIT_NOT_IMPLEMENTED`;
- plan command writes nothing;
- self-check uses `httpx.MockTransport` and temporary output only;
- live command requires TTY confirmation before `getpass`;
- public receipts exclude secrets, URLs, request IDs, raw bodies, contact
  fields, market cap, employee/share counts, absolute paths, and performance
  values.
