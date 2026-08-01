# MarketFlow Monthly Acquisition Artifacts

## Scope

This document describes the offline fake-transport monthly acquisition artifact
graph. It is not a provider-integration design and does not enable Massive.com
or legacy Polygon adapter execution.

## Artifact Schema

Monthly acquisition artifacts use:
`marketflow.monthly_acquisition_artifact_manifest.v1`.

The schema is intentionally separate from the historical processing manifest so
fake acquisition evidence can be audited without pretending that normal runtime
historical ingestion has been enabled.

## Artifact Types

- `MONTH_CHUNK_REQUEST_CONTRACT`: fixed month request, v2/v2.1 digests,
  fictional ticker, source bar policy, provider identity, and request semantic
  digest.
- `REQUEST_ATTEMPT_RECORD`: immutable sanitized attempt record, attempt ordinal,
  transport outcome category, retry decision, Retry-After decision, accepted
  attempt marker, and semantic projection digest when available.
- `RAW_PROVIDER_PAGE`: exact response bytes from the scripted fake transport.
- `MONTH_CHUNK_COMPLETENESS_MANIFEST`: accepted page chain, accepted attempt per
  page, raw page digests, pagination status, row count, and page count.
- `MONTH_NORMALIZED_15M_OHLCV`: normalized 15-minute OHLCV rows emitted only
  from the completeness manifest.
- `MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS`: paired audit fields with the same
  timestamps and row count as normalized OHLCV.
- `MONTH_ACQUISITION_RECEIPT`: sanitized execution receipt with no raw OHLCV,
  raw body, raw URL, credentials, absolute paths, provider account data, or raw
  exception strings.

## Lineage Rules

The request contract is the parent of attempts and raw pages. The completeness
manifest depends on accepted raw pages. Normalized OHLCV and normalized audit
artifacts depend on the completeness manifest. The receipt depends on the
request, attempt, completeness, and normalized artifacts emitted during the run.

Lineage validation uses exact manifest references produced during execution.
Artifacts are never selected by globbing, timestamp ordering, file size, row
count, or latest-file heuristics.

## Fake Transport Boundary

The fake transport consumes strict scripted request/outcome pairs and fails on
unexpected requests or unconsumed scripted responses. Outcomes are deterministic:
transport timeout, connection reset, fixed HTTP status, complete HTTP response
bytes, crash after complete body, and no response.

No provider client, Massive.com account, legacy Polygon account, SDK migration,
credential value, socket, DNS, URL request execution, external clock, random
selection, or live provider data is part of this artifact path.

## Parsing and Projection

Provider response parsing uses JSON `Decimal` parsing and rejects NaN, Infinity,
binary floats, numeric strings, and boolean-as-integer values. The parser accepts
only exact 15-minute source timestamps under the v2.1 start-of-window contract.

Semantic retry comparison uses
`OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1`. It includes ticker, adjusted flag,
status, counts, continuation presence, and row OHLCV/audit-presence values. It
excludes attempt timing, request IDs, retrieval metadata, raw formatting, key
order, credentials, raw URLs, and opaque raw cursor values.

## Normalization Rule

Normalization is monthly-first and completeness-manifest-first. Raw pages without
a valid completeness manifest are not normalizable. No regular-trading-hours
filtering, profile derivation, strategy evaluation, registry write, or runtime
migration is performed here.
