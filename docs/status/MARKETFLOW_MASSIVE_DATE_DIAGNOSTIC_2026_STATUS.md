# MarketFlow Massive Date Diagnostic 2026 Status

## Status

`MASSIVE_DATE_DIAGNOSTIC_2026_SCHEMA_ACCEPTED_NONCANONICAL`

## Scope

- Adds a noncanonical date-differential diagnostic for Massive.com Custom Bars.
- Compares the provider's January 2026 first-page response shape against the
  prior January 2025 HTTP-200 schema rejection context.
- Does not modify the existing January 2025 smoke specification or digest.
- Does not modify canonical Contract-v2 acquisition range policy.
- Does not create a `MonthChunkRequest` for 2026.
- Does not invoke the monthly executor.
- Does not enable acquisition, registry writes, Strategy, or runtime migration.
- Does not inspect or retain API-key values, provider account state, billing
  state, provider portal state, credentials, or the provider account.

## Fixed Diagnostic Specification

- Schema: `marketflow.massive_provider_date_diagnostic.v1`
- Classification: `NONCANONICAL_PROVIDER_DATE_DIAGNOSTIC`
- Provider: `MASSIVE.COM`
- Endpoint: `STOCKS_CUSTOM_BARS_V2`
- Ticker: `AAPL`
- Month: `2026-01`
- Effective start: `2026-01-01`
- Effective end: `2026-01-31`
- Multiplier: `15`
- Timespan: `minute`
- Adjusted: `true`
- Sort: `asc`
- Limit: `50000`
- Maximum provider pages: `1`
- Canonical eligibility: false
- Registry eligibility: false
- Acquisition-generation eligibility: false
- Strategy enabled: false

Diagnostic digest:

```text
588e61a824799f24feedfeaa9b4629ed2f623b5ff0490624089562ca0eb63376
```

Required confirmation phrase:

```text
RUN MARKETFLOW MASSIVE DATE DIAGNOSTIC 588e61a82479
```

## Entitlement Context

- Operator-confirmed provider business identity: Massive.com.
- Legacy Polygon adapter/package names remain only where they accurately
  describe installed code.
- Operator-attested subscription: `STOCKS_STARTER`.
- Operator-attested current published historical entitlement: `FIVE_YEARS`.
- Operator-attested current published data recency: `FIFTEEN_MINUTE_DELAYED`.
- Relevant aggregate access: `INTRADAY_AND_DAILY_AVAILABLE`.
- `provider_entitlement_status`: `OPERATOR_ATTESTED_CONFIRMED`.
- January 2025 and January 2026 are treated as within the operator-attested
  provider historical entitlement for this diagnostic only.

## Date Differential Boundary

- January 2025 smoke context: provider authentication previously reached HTTP
  200 with a complete response body, but strict schema validation rejected the
  body.
- January 2026 diagnostic context: tests only whether the fixed first-page
  provider response shape differs by date.
- January 2026 remains outside the canonical Contract-v2 fixed range ending
  `2025-12-31`.
- A successful January 2026 diagnostic does not make January 2026 canonical,
  registry-eligible, acquisition-generation eligible, or Strategy-eligible.

## Implemented Commands

- `python -m marketflow.historical_data --massive-date-diagnostic-2026-plan`
  prints the fixed plan without network access, credential prompt, or writes.
- `python -m marketflow.historical_data --massive-date-diagnostic-2026-self-check`
  runs valid and rejected schema cases with `httpx.MockTransport` and a
  fictional key only.
- `python -m marketflow.historical_data --massive-date-diagnostic-2026-run`
  requires an interactive TTY, prints the sanitized plan, requires the exact
  digest-bound confirmation phrase, prompts through `getpass` only after
  authorization, and performs exactly one provider request if manually invoked.

## Sanitized Receipt Boundary

The live receipt may include only bounded structural diagnostics:

- diagnostic status;
- HTTP status;
- response body completeness;
- parser status;
- top-level field-name set;
- aggregate row field-name sets;
- missing and unexpected field names;
- fixed JSON type categories;
- failing row index;
- query/result counts;
- results-present and continuation-present booleans;
- bounded provider response status;
- diagnostic digest.

The receipt excludes API keys, authorization headers, raw URL, raw `next_url`,
cursor material, `request_id` values, response bodies, OHLCV/VWAP/transaction
values, raw exception text, and absolute paths.

## Sanitized Live Observation

The operator manually ran the fixed January-2026 diagnostic after offline
implementation. The sanitized observation was:

- Classification: `NONCANONICAL_PROVIDER_DATE_DIAGNOSTIC`
- Ticker: `AAPL`
- Effective start: `2026-01-01`
- Effective end: `2026-01-31`
- HTTP status: `200`
- Response body complete: true
- Provider response status: `OK`
- Parser status: `RESPONSE_SCHEMA_ACCEPTED`
- Diagnostic status: `DATE_DIAGNOSTIC_SCHEMA_ACCEPTED`
- Query count: `15331`
- Results count: `1279`
- Results present: true
- Continuation present: false
- Transport invocation count: `1`
- Retry attempted: false
- Pagination followed: false
- Monthly executor invoked: false
- Normalized artifact created: false
- Strategy enabled: false
- Canonical eligibility: false
- Registry eligibility: false
- Diagnostic digest:
  `588e61a824799f24feedfeaa9b4629ed2f623b5ff0490624089562ca0eb63376`

Observed top-level field names:

- `adjusted`
- `count`
- `queryCount`
- `results`
- `resultsCount`
- `status`
- `ticker`

No raw provider body, API key, Authorization header, request ID value, raw URL,
raw `next_url`, cursor, OHLCV/VWAP/transaction-count values, account data, or
provider portal data is included in this repository.

This live diagnostic was noncanonical. The response was schema accepted, but
that acceptance does not authorize acquisition, does not prove Strategy or
profitability, and did not create monthly normalization or runtime migration.

## Offline Evidence

- Focused diagnostic tests: `23 passed`.
- No additional provider call was made during acceptance.
- No real API key was inspected during implementation or acceptance.
- No commit, tag, or push was performed in this implementation pass.

## Pending

- Manual live execution remains pending explicit operator action in an
  interactive terminal for any future date-differential experiment.
- Next experiment: January 2025 through the same diagnostic code path.
- The remaining acquisition blockers are unchanged: fixed start date, fixed end
  date, 4h bar-construction policy, session policy, adjustment/corporate-action
  provenance, and pagination/completeness acceptance.
