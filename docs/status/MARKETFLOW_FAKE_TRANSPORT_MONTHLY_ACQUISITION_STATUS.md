# MarketFlow Fake-Transport Monthly Acquisition Status

## Status

`FAKE_TRANSPORT_MONTHLY_ACQUISITION_IMPLEMENTED_OFFLINE`

## Accepted Boundaries

- Provider business identity: `Massive.com`
- Former brand: `POLYGON.IO`
- Legacy installed adapter family naming remains explicit where applicable:
  `polygon-api-client`
- Provider entitlement status:
  `OPERATOR_ATTESTED_CONFIRMED`
- Provider execution enabled: `false`
- Acquisition enabled: `false`
- Runtime migration performed: `false`
- SDK migration performed: `false`

## Implemented

- Strict deterministic fake transport.
- Fixed one-month request contract for fictional tickers only.
- Logical page request identities with predecessor and sanitized continuation
  binding.
- Immutable attempt records with retry and Retry-After decisions.
- Exact raw response byte artifacts for complete fake bodies.
- Strict Decimal provider-response parsing.
- Semantic retry projection and variance blocking.
- Pagination chain validation for repeated continuations and duplicate
  timestamps.
- Completeness manifest before normalization.
- Paired normalized OHLCV and aggregate-audit artifacts.
- Sanitized monthly acquisition receipt.
- Dry CLI self-check:
  `python -m marketflow.historical_data --monthly-acquisition-self-check`.

## Not Implemented

- Real Massive.com/Polygon provider execution.
- API-key, provider account, billing, portal, or credential inspection.
- SDK install, SDK upgrade, or SDK migration.
- Runtime historical ingestion migration.
- Registry writes.
- Strategy, backtest, Monte Carlo, walk-forward, or trading execution semantics.
- Real sleep, DNS, socket, URL request execution, or provider data download.

## Remaining Blocking Items for Real Acquisition

- Fixed start date.
- Fixed end date.
- 4h bar-construction policy.
- Session policy.
- Adjustment and corporate-action provenance.
- Pagination and completeness acceptance for live provider behavior.
