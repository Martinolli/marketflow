# MarketFlow Noncanonical Provider Smoke Architecture

## Boundary

The Massive one-month smoke runner is an operator-controlled harness for a
future first real Massive.com request. The runner is production-capable, but
this implementation is accepted offline only.

The smoke output is always classified:

```text
NONCANONICAL_PROVIDER_SMOKE
```

It is not a canonical acquisition generation, canonical registry candidate,
calendar freeze, Strategy source, research dataset, performance test, or
investment recommendation.

## Fixed Target

- Provider: `MASSIVE.COM`
- Endpoint: `STOCKS_CUSTOM_BARS_V2`
- Ticker: `AAPL`
- Month: `2025-01`
- Effective start: `2025-01-01`
- Effective end: `2025-01-31`
- Source interval: 15-minute Custom Bars
- Adjusted: `true`
- Sort: `asc`
- Limit: `50000`

The specification is source-defined and immutable. CLI, environment, config,
host, ticker, month, date, limit, provider, and semantic overrides are not
accepted.

## Digest

The smoke specification is serialized as deterministic canonical JSON and
hashed with SHA-256.

Current smoke digest:

```text
2116c4dfa3e8ea759e5bca09cf0f4ccc329134f0cac1329ad871fb7746cdcfe4
```

The digest excludes API keys, current time, local paths, run IDs, provider
responses, market prices, and report formatting.

## Execution Model

Plan mode validates the specification and Contracts, prints a sanitized receipt,
requests no credential, writes no artifact, and opens no socket.

Live mode is interactive only. It prints the sanitized plan, prints the
classification and exclusions, requires a digest-bound confirmation phrase,
then requests the API key through hidden `getpass` input. Only after that
ceremony does it construct the accepted `ProviderApiKey` wrapper and
`MassiveRestTransport`. Monthly artifacts created through this live smoke path
mark provider execution as enabled while acquisition remains disabled.

The monthly executor remains responsible for retries, attempt evidence,
accepted-page selection, pagination, completeness, raw byte artifact writing,
and monthly normalization. The smoke runner does not duplicate those policies.

## Runtime Root

Source-defined live root:

```text
.marketflow/provider_smoke/runs/
```

Run directories use opaque IDs only and do not include ticker or month. Tests
inject pytest temporary roots. The smoke root is ignored through the existing
`.marketflow/` ignore rule.

## Artifact Chain

The live smoke may create monthly request, attempt, raw page, completeness,
normalized OHLCV, normalized aggregate-audit, monthly receipt, and smoke
receipt artifacts.

All smoke artifacts are marked:

```text
LIVE_PROVIDER_SMOKE_NONCANONICAL
```

They must not claim canonical, approved, registry eligible, frozen acquisition
generation, research dataset, or Strategy-source status.

HTTP 200 provider bodies are parsed and continuation URLs are checked before
raw page persistence. A credential-like or otherwise invalid continuation is
rejected without storing that response body as a raw page artifact.

## Excluded Runtime Paths

The smoke runner does not invoke frozen-calendar derivation, RTH bar derivation,
SWING/POSITION aggregation, analytical segmentation, annotation, Strategy,
Wyckoff, Monte Carlo, outcomes, optimization, broker, execution, registry
authority, report rewriting, or normal ticker-only runtime migration.
