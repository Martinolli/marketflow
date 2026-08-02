# MarketFlow Massive Provider Local Date Range Correction

## Status

`MASSIVE_PROVIDER_LOCAL_DATE_RANGE_CORRECTED_OFFLINE`

## Diagnostic Context

A same-code-path Massive.com Custom Bars A/B diagnostic reported:

- January 2026: HTTP `200`, `RESPONSE_SCHEMA_ACCEPTED`, results count `1279`.
- January 2025: HTTP `200`, `RESPONSE_SCHEMA_REJECTED`, results count `1277`.

Both responses had the same accepted top-level field set:

- `adjusted`
- `count`
- `queryCount`
- `results`
- `resultsCount`
- `status`
- `ticker`

The January-2025 diagnostic had no missing top-level fields, no unexpected
top-level fields, and no type mismatches. The rejected condition was therefore
not a response-schema field mismatch.

## Reproduced Defect

The defect was reproduced offline before production source was changed.

The parser treated provider Custom Bars date-path parameters as UTC calendar
dates by comparing `window_start_utc.date()` with `effective_start` and
`effective_end`.

For a fixed request:

```text
effective_start = 2025-01-01
effective_end   = 2025-01-31
```

the current parser rejected valid source windows on the final requested
provider-local date when their canonical UTC timestamps crossed into
`2025-02-01`, including:

```text
2025-02-01T00:00:00Z = 2025-01-31 19:00 America/New_York
2025-02-01T00:45:00Z = 2025-01-31 19:45 America/New_York
```

January 31, 2025 was a Friday, so final-date after-hours windows could spill
into the next UTC date. January 31, 2026 was a Saturday, so the equivalent
month-end spill did not appear in the accepted January-2026 diagnostic.

## Corrected Contract

Massive.com Custom Bars request date-path parameters are interpreted as
provider/source-local calendar dates in:

```text
America/New_York
```

For a request:

```text
effective_start
effective_end
```

the parser now constructs:

```text
local_start         = effective_start at 00:00 America/New_York
local_end_exclusive = day after effective_end at 00:00 America/New_York
```

and converts both instants to UTC.

A source bar is accepted only when:

```text
utc_start <= window_start_utc < utc_end_exclusive
window_end_utc <= utc_end_exclusive
```

The parser uses timezone-aware datetimes and `zoneinfo` rules through the
accepted Contract v2.1 source-timezone policy. It does not use local-machine
timezone, a manually fixed UTC offset, timestamp tolerance, or timestamp
snapping.

Canonical source-bar timestamps remain UTC instants. The fixed request dates
remain unchanged.

## Boundary Results

January 2025:

- `2025-01-01 00:00 America/New_York` is accepted.
- `2025-01-31 19:00 America/New_York` is accepted as
  `2025-02-01T00:00:00Z`.
- `2025-01-31 19:45 America/New_York` is accepted as
  `2025-02-01T00:45:00Z`.
- `2025-01-31 23:45 America/New_York` is accepted as
  `2025-02-01T04:45:00Z`, with window end exactly at the upper bound.
- `2025-02-01 00:00 America/New_York` is rejected.

Summer DST:

- `2025-07-31 23:45 America/New_York` is accepted as
  `2025-08-01T03:45:00Z`.
- `2025-08-01 00:00 America/New_York` is rejected.

The January-2026 synthetic diagnostic response remains accepted under the same
logic.

## Failure Category

Provider source windows outside the approved provider-local date interval are
classified as:

```text
TIMESTAMP_RANGE_INVALID
```

The sanitized fixed finding is:

```text
SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE
```

This condition is no longer reported as `SCHEMA_FAILURE`. Schema field
allowlists, `count` compatibility, aggregate-row allowlists, `otc` validation,
Decimal parsing, duplicate timestamp rejection, strict ascending timestamp
order, OHLCV geometry, and response-body privacy remain unchanged.

## Monthly Executor Boundary

The monthly executor still requests the fixed Contract-v2 range
`2022-01-01` through `2025-12-31` in fixed calendar-month chunks.

Range coverage now evaluates first and last source windows by provider-local
date. Monthly normalization retains extended-hours source bars as source
evidence. No RTH filtering, Strategy path, calendar derivation, registry
eligibility, acquisition enablement, or runtime migration was added.

## Offline Evidence

No provider request occurred during this correction. No actual API key,
credential, provider account, portal, billing data, browser data, trade data,
raw provider body, or runtime diagnostic file was inspected or committed.

Focused correction and non-regression group:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_date_diagnostic.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py
```

Result during implementation: `89 passed`.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: `870 tests collected`.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: `870 passed`.

`pip check`: pass, `No broken requirements found.`

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass with Git LF-to-CRLF working-copy normalization
warnings only.

Test count explanation: accepted starting collection was `860` tests at the
January-2025 diagnostic implementation. Final collection is `870` because this
correction adds 10 deterministic tests covering the reproduced January-2025
UTC-spill defect, provider-local month-end acceptance, local next-date
rejection, summer DST, lower and upper interval bounds, naive timestamp
rejection, timestamp-range category propagation, monthly extended-hours
normalization retention, date-diagnostic 2025 acceptance, smoke propagation,
and source-assurance boundaries.
