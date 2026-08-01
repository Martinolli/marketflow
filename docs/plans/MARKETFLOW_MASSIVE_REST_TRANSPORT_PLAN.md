# MarketFlow Massive REST Transport Plan

## Authority Boundary

This plan authorizes an offline-tested Massive REST transport boundary. It does
not authorize a live provider request, provider account review, API-key
inspection, one-ticker smoke test, canonical dataset generation, registry
authority action, or normal runtime migration.

The transport is production-capable code, but acceptance in this task is through
injected mock HTTP transport only.

## Fixed Provider Boundary

- Provider business identity: `MASSIVE.COM`
- REST host: `api.massive.com`
- Scheme: `https`
- Route:
  `/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}`
- Accepted source request values: multiplier `15`, timespan `minute`, adjusted
  `true`, sort `asc`, limit `50000`.

No arbitrary host, scheme, base URL, endpoint, legacy Polygon fallback, or
provider fallback is accepted.

## Implementation Plan

1. Add `marketflow/historical_data/massive_transport.py` with a narrow
   credential wrapper, deterministic request model, continuation validator, and
   `MassiveRestTransport.send(...)` method compatible with the monthly executor
   transport protocol.
2. Use `httpx` because it is source-declared in `requirements.txt`; do not add,
   install, remove, or change dependencies.
3. Inject the HTTP backend/client so tests use `httpx.MockTransport` and no
   default pytest test opens a real socket.
4. Construct exactly one GET request per transport call, with bearer-header
   authentication, `Accept: application/json`, `Accept-Encoding: identity`, a
   bounded non-private User-Agent, no cookies, no API-key query parameter, no
   redirects, TLS verification enabled, and `trust_env=false`.
5. Validate provider continuation URLs as evidence only, then reconstruct a safe
   Massive request for the same endpoint, ticker, range, multiplier, timespan,
   adjusted flag, sort, limit, and sanitized cursor identity.
6. Capture exact application response bytes subject to a 64 MiB limit, retain
   only selected non-secret headers, reject unsupported content encodings and
   non-JSON success content types, and map HTTP/exceptions to fixed categories.
7. Add `--massive-transport-self-check` to the historical-data dry CLI using a
   fictional key and injected mock backend only.
8. Add focused tests for dependency declaration, credential redaction, request
   construction, continuation validation, HTTP security settings, raw bytes,
   status/exception mapping, monthly executor integration, CLI self-check, and
   source assurance.

## Non-Goals

- No retry or sleep in the transport.
- No pagination-chain traversal in the transport.
- No aggregate parsing, normalization, or artifact writing in the transport.
- No environment credential read.
- No provider SDK import or legacy `polygon-api-client` invocation.
- No current runtime integration or default provider mode.
