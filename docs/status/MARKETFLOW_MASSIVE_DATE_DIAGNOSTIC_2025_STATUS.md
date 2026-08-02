# MarketFlow Massive Date Diagnostic 2025 Status

## Status

`MASSIVE_DATE_DIAGNOSTIC_2025_IMPLEMENTED_OFFLINE_NOT_EXECUTED`

## Purpose

- Adds the January-2025 side of the Massive.com Custom Bars date-response A/B
  diagnostic.
- Uses the same accepted diagnostic code path as the January-2026 diagnostic.
- The only specification differences are the fixed month/date fields and the
  resulting deterministic digest.
- This diagnostic remains noncanonical even though January 2025 lies inside
  the Contract-v2 calendar range.

## Fixed Diagnostic Specification

- Schema: `marketflow.massive_provider_date_diagnostic.v1`
- Classification: `NONCANONICAL_PROVIDER_DATE_DIAGNOSTIC`
- Provider: `MASSIVE.COM`
- Endpoint: `STOCKS_CUSTOM_BARS_V2`
- Ticker: `AAPL`
- Month: `2025-01`
- Effective start: `2025-01-01`
- Effective end: `2025-01-31`
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
b90f5e8d681be1ca753f2fccd78ed778341aefb6d6c4fb89b1d657376a5e8e98
```

Required confirmation phrase:

```text
RUN MARKETFLOW MASSIVE DATE DIAGNOSTIC b90f5e8d681b
```

## A/B Relationship

Accepted January-2026 diagnostic digest remains:

```text
588e61a824799f24feedfeaa9b4629ed2f623b5ff0490624089562ca0eb63376
```

The 2025 and 2026 diagnostic specifications are identical except for:

- `month_key`;
- `effective_start`;
- `effective_end`.

The accepted January-2026 live observation was HTTP `200`,
`RESPONSE_SCHEMA_ACCEPTED`, `results_count=1279`, one request, no retry, no
pagination, no normalization, and no canonical or registry eligibility. The
2025 diagnostic is intended as the same-code-path comparison target.

## Canonical And Monthly Boundary

- Contract-v2 range remains `2022-01-01` through `2025-12-31`.
- January 2025 being inside that range does not make this diagnostic canonical.
- No Contract file was modified.
- No `MonthChunkRequest` is created by the diagnostic.
- The monthly acquisition executor is not invoked.
- No completeness manifest is written.
- No normalized OHLCV or supplemental aggregate artifact is produced.
- No canonical registry evidence is created.
- No runtime migration is performed.
- The existing January-2025 smoke digest remains:
  `2116c4dfa3e8ea759e5bca09cf0f4ccc329134f0cac1329ad871fb7746cdcfe4`.

## Implemented Commands

- `python -m marketflow.historical_data --massive-date-diagnostic-2025-plan`
  prints the fixed plan without network access, credential prompt, or writes.
- `python -m marketflow.historical_data --massive-date-diagnostic-2025-self-check`
  runs valid and rejected schema cases through the shared diagnostic path with
  `httpx.MockTransport` and a fictional key only.
- `python -m marketflow.historical_data --massive-date-diagnostic-2025-run`
  requires an interactive TTY, prints the sanitized plan, requires the exact
  digest-bound confirmation phrase, prompts through `getpass` only after
  authorization, and performs exactly one provider request if manually invoked.

No ticker, date, month, provider, host, endpoint, limit, API key, timeout, or
semantic override is accepted.

## Sanitized Receipt Boundary

Receipts may contain only bounded structural/provider metadata:

- diagnostic schema/version;
- classification;
- diagnostic digest;
- ticker and effective dates;
- HTTP status;
- response body completeness;
- parser status;
- bounded provider response status identifier;
- top-level and row field-name sets;
- missing and unexpected field names;
- fixed JSON type categories;
- failing row index;
- query and result counts;
- results-present and continuation-present booleans;
- transport invocation count;
- retry, pagination, monthly executor, normalization, and runtime flags.

Receipts exclude API key, Authorization header, raw URL, raw `next_url`, cursor,
request ID value, raw response body, OHLCV/VWAP/transaction-count values, raw
exception text, absolute paths, account data, and provider-account data.

## Offline Evidence

- Focused diagnostic tests: `28 passed`.
- The 2026 diagnostic digest reproduced unchanged.
- The January-2025 smoke digest reproduced unchanged.
- The 2025 plan command is offline and credential-free.
- The 2025 self-check uses mock HTTP only and writes no persistent artifacts.
- The 2025 live command rejects noninteractive execution before credential
  prompt or request construction.
- No provider call was made during implementation.
- No actual API key was requested or inspected.
- No dependency was installed, updated, downgraded, renamed, or removed.
- No commit, tag, or push was performed in this implementation pass.

## Pending

- Next step: one manual January-2025 live diagnostic using the same accepted
  key and the same noncanonical one-request boundary.
- The remaining acquisition blockers are unchanged: fixed start date, fixed end
  date, 4h bar-construction policy, session policy, adjustment/corporate-action
  provenance, and pagination/completeness acceptance.
