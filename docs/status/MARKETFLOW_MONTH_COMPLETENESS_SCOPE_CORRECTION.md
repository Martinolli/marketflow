# MarketFlow Month Completeness Scope Correction

UTC status date: `2026-08-02T09:40:05Z`.

Status: `MONTH_COMPLETENESS_SCOPE_CORRECTION_ACCEPTED_OFFLINE`

Branch: `fix/swing-month-completeness-separation`

Base commit:

```text
75083194f97bce15d3d4f87d8dc3a1a7f8722255
```

## Diagnostic Context

The accepted Massive.com January-2025 diagnostic established that provider
request dates are source-local `America/New_York` calendar dates while returned
aggregate timestamps are canonical UTC instants.

The full smoke context accepted one raw provider page and one accepted page, but
the monthly executor then blocked the run with:

```text
fixed finding: RANGE_COVERAGE_INCOMPLETE
pagination status: PAGINATION_CHAIN_INVALID
normalized artifacts: none
```

That was a false completeness failure. A valid provider response is not required
to contain a bar for every empty 15-minute clock interval, weekend, closed
period, or no-trade interval.

## Reproduced Defect

Before production changes, a synthetic one-page January-2025 response was run
offline with:

- no continuation;
- valid HTTP-200 body shape;
- valid counts;
- ordered 15-minute start-stamped source rows;
- all rows inside the approved `America/New_York` request range;
- first returned row after January 1 local midnight;
- final returned row before February 1 local midnight;
- legitimate empty intervals between rows.

The pre-fix result reproduced the blocker:

```json
{
  "accepted_page_count": 1,
  "completeness_status": "INCOMPLETE",
  "fixed_findings": ["RANGE_COVERAGE_INCOMPLETE"],
  "pagination_status": "PAGINATION_CHAIN_INVALID",
  "raw_page_count": 1,
  "row_count": 0,
  "status": "MONTH_ACQUISITION_PAGINATION_INVALID"
}
```

Root cause: the monthly executor treated first and last returned source-window
local dates as exact calendar-boundary occupancy requirements. That confused
provider retrieval completeness with later market-session slot coverage.

## Corrected Semantics

Monthly acquisition now separates three concepts.

Provider page-chain completeness:

- accepted pages must be contiguous for the requested month;
- continuation chain defects remain invalid;
- repeated continuations remain invalid;
- duplicate/conflicting timestamps across pages remain invalid;
- a missing required subsequent page is `PAGINATION_INCOMPLETE`;
- a valid exhausted chain is `PAGINATION_EXHAUSTED`.

Request-range containment:

- source rows must be UTC-aware and strictly ordered;
- source windows must be inside the approved provider-local
  `America/New_York` request range;
- source intervals remain exactly 15 minutes;
- first and last returned timestamps are retained as evidence only.

Market-session slot coverage:

- monthly acquisition records `MARKET_SESSION_COVERAGE_NOT_EVALUATED`;
- RTH slot completeness remains a later frozen-calendar/bar-engine stage;
- no calendar engine or RTH bar engine is invoked here.

## Manifest Scope

A month-completeness manifest is now permitted when retrieval is complete:

```text
scope = PROVIDER_RETRIEVAL_COMPLETE
pagination_status = PAGINATION_EXHAUSTED
request_range_containment_status = REQUEST_RANGE_CONTAINED
market_session_coverage_status = MARKET_SESSION_COVERAGE_NOT_EVALUATED
canonical_dataset_complete = false
rth_dataset_complete = false
```

The manifest does not claim:

- `MARKET_SESSION_COVERAGE_COMPLETE`;
- `CANONICAL_DATASET_COMPLETE`;
- `RTH_DATASET_COMPLETE`.

Referenced raw-page and attempt manifests are validated from disk before the
completeness manifest is written. Normalized artifacts remain children of the
completeness manifest, so normalization cannot occur without retrieval
completeness evidence.

## Normalization

After a valid retrieval-completeness manifest, monthly acquisition writes:

- `MONTH_NORMALIZED_15M_OHLCV`;
- `MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS`.

Normalization preserves exact source order and every valid source row, including
extended-hours rows. It performs no RTH filtering, no synthetic filling, and no
missing-interval repair.

These normalized monthly artifacts remain noncanonical source evidence. They do
not become profile datasets and do not enable Strategy, registry, broker, or
execution behavior.

## Smoke Mapping

A valid one-page, no-continuation response now maps to:

```text
request_status = MONTH_ACQUISITION_COMPLETED
pagination_status = PAGINATION_EXHAUSTED
completeness_status = COMPLETE
smoke_status = SMOKE_COMPLETED_NONCANONICAL
```

The smoke receipt continues to report:

```text
canonical_eligibility = false
registry_eligibility = false
strategy_enabled = false
calendar_bar_derivation_enabled = false
```

## Non-Regressions

Preserved mappings:

- first-page authentication failure: `PAGINATION_NOT_STARTED`;
- first-page schema rejection: `PAGINATION_NOT_STARTED`;
- first-page timestamp-range failure: `PAGINATION_NOT_STARTED`;
- accepted-page continuation defect: `PAGINATION_CHAIN_INVALID`;
- missing required subsequent page: `PAGINATION_INCOMPLETE`;
- out-of-range source window: `TIMESTAMP_RANGE_INVALID` /
  `SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE`.

Strict schema/count/`otc` behavior is unchanged. Pagination loops, repeated
continuations, repeated pages, and duplicate timestamps across pages remain
blocked.

## Non-Actions

No provider request was made during this correction. No API key value,
credential, provider account, provider portal, billing data, raw live provider
body, or runtime smoke evidence was inspected or committed.

No dependency was installed, removed, upgraded, downgraded, or renamed.

No canonical data, registry authority, Strategy, Monte Carlo, outcome,
performance, broker, execution, historical report rewrite, runtime migration,
calendar derivation, or RTH filtering was introduced.
