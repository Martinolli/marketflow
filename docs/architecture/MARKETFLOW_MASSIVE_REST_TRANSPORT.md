# MarketFlow Massive REST Transport

## Scope

The Massive REST transport is the HTTP boundary for future monthly acquisition
execution. It is production-capable code accepted in this phase only through
offline mock HTTP tests. No real provider request, one-ticker smoke test,
canonical dataset, calendar freeze, registry action, or runtime migration is
authorized here.

## Fixed Endpoint

- Provider business identity: `MASSIVE.COM`
- Scheme: `https`
- Host: `api.massive.com`
- Path template:
  `/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}`
- Accepted monthly source values: multiplier `15`, timespan `minute`, adjusted
  `true`, sort `asc`, limit `50000`.

The transport does not accept caller-provided base URLs, arbitrary hosts,
arbitrary endpoints, HTTP, legacy `api.polygon.io`, or provider fallback.

## Request Boundary

The public transport call receives the logical page-request identity already
used by the monthly executor. The transport instance binds the full immutable
month request and validates request digest, month key, page ordinal, and
continuation identity.

Initial requests are reconstructed from the accepted month request. Continuation
URLs are treated as raw provider evidence, validated strictly, and reconstructed
as safe Massive requests. The raw `next_url` is not part of public receipts,
manifests, or logs.

## HTTP Security

The transport uses `httpx`, which is source-declared in `requirements.txt`.
Source-defined constants are fixed:

- connect timeout: 10 seconds;
- read timeout: 30 seconds;
- write timeout: 10 seconds;
- pool timeout: 10 seconds;
- maximum body size: 67108864 bytes.

HTTP settings:

- TLS verification enabled;
- redirects disabled;
- `trust_env=false`;
- `Accept-Encoding: identity`;
- no cookies;
- no environment proxy or certificate inheritance;
- one bounded non-private User-Agent.

## Response Boundary

The transport returns one immutable outcome per call. It captures exact
application body bytes under `Accept-Encoding: identity`, subject to the 64 MiB
limit. It does not reserialize JSON, normalize whitespace, decode before raw
evidence storage, retry, sleep, traverse pagination, normalize bars, or accept
attempts.

Only selected response headers are retained: `Content-Type`, `Content-Length`,
`Content-Encoding`, `Retry-After`, and bounded request/correlation IDs.

## Monthly Executor Integration

The monthly executor remains responsible for retries, attempt records,
semantic equivalence, page acceptance, pagination, completeness, and
normalization. The transport supplies raw bytes and fixed failure categories
only.
