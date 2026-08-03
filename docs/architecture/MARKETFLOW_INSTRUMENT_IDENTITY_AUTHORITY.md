# MarketFlow Instrument Identity Authority

## Purpose

Instrument Identity Evidence v1 establishes bounded source-authority candidate
evidence for whether the fixed `AAPL` ticker refers to the same listed security
and share class at the Acquisition Contract v2 boundary dates:

- `2022-01-01`
- `2025-12-31`

The provider business identity is represented as `MASSIVE.COM`. Legacy
Polygon-specific adapter or package names are preserved only where they
accurately describe already installed code.

## Specification

The immutable specification uses:

- schema version: `marketflow.instrument_identity_specification.v1`
- classification: `PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL`
- endpoint family: `TICKER_OVERVIEW_V3`
- ticker: `AAPL`
- expected market: `stocks`
- expected locale: `us`
- expected currency: `usd`

Canonical eligibility, registry eligibility, generation-freeze eligibility, and
Strategy enablement are all fixed false.

No caller can override ticker, dates, provider, endpoint, host, market, locale,
currency, credential source, or artifact root through the public CLI.

## Request Boundary

The Ticker Overview request is fixed to:

`GET https://api.massive.com/v3/reference/tickers/AAPL`

Each run prepares exactly one request for `2022-01-01` and one request for
`2025-12-31`, each with a single `date` query parameter.

The request uses bearer-header authentication, `Accept: application/json`,
`Accept-Encoding: identity`, TLS verification, redirects disabled,
`trust_env=False`, no cookies, and no internal retry.

The Custom Bars endpoint, Ticker Events endpoint, All Tickers endpoint, splits,
dividends, calendar freeze, Strategy, Monte Carlo, outcomes, broker, execution,
and registry authority are not invoked by this package.

## Projection

Live response bytes are first retained as `TICKER_OVERVIEW_RAW_RESPONSE`
artifacts with byte SHA-256, byte size, raw-byte media type, safe relative
paths, and saved-disk validation. The bounded identity projection is parsed
only from those validated bytes.

Only the bounded identity projection becomes public source-authority evidence:

- as-of date;
- ticker;
- active status;
- market, locale, and currency;
- primary exchange;
- Composite FIGI;
- Share Class FIGI;
- security type;
- explicit CIK, list-date, and delist-date presence statuses;
- provider status;
- identity projection digest.

Provider descriptive, contact, branding, capitalization, employee, and share
count data may be structurally recognized by the parser but is not projected
into authority evidence or public receipts.

Actual OHLCV values are not part of Ticker Overview identity evidence and remain
sanitized from receipts.

## Continuity

Continuity is supported only when both snapshots are complete, all critical
identity fields match exactly, neither snapshot creates an inactive or delisted
conflict for the requested boundary, and optional present-on-both supporting
fields do not conflict.

Critical identity changes produce:

`IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW`

The package never stitches identity changes automatically, never chooses the
newest snapshot as authoritative, and never infers continuity solely from the
ticker text.

Because Ticker Events audit is not implemented in this phase, a matching
start/end comparison can produce only an identity-continuity candidate, not a
canonical or frozen identity approval.
