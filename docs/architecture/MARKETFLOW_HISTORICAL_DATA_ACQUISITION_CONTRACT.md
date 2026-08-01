# MarketFlow Historical Data Acquisition Contract

## Purpose

This document defines the proposed fixed-date historical acquisition contract
for future MarketFlow research datasets. It is a design and validation contract
only. It does not download data, contact a provider, annotate data, select
actual acquisition dates, run Strategy candidates, run Monte Carlo, run outcome
evaluation, inspect performance, or create execution capability.

## Contract Status

Current status:

```text
ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS
```

Provider entitlement is operator-attested confirmed. Acquisition remains
disabled until a human operator approves:

- exact fixed start and end dates;
- 4h bar construction and session convention;
- extended-hours inclusion or exclusion;
- final corporate-action and adjustment treatment.

The contract cannot be frozen by the offline dry CLI.

## Provider Contract

Provider identity:

```text
MASSIVE_POLYGON_STOCKS_CUSTOM_BARS
```

Business identity:

```text
MASSIVE.COM
```

Former brand and installed adapter/package naming:

```text
POLYGON.IO
polygon-api-client==1.14.6
```

Installed dependency names are not renamed. The provider contract records:

- endpoint family: `STOCKS_AGGREGATES_CUSTOM_BARS`;
- endpoint contract version: `v2_aggs_ticker_range`;
- asset class: `US_EQUITY`;
- exact ticker, unresolved in the source-controlled example;
- multiplier and timespan;
- fixed start and end dates, unresolved in the source-controlled example;
- `adjusted=true`;
- `sort=asc`;
- explicit base-aggregate limit;
- requested session policy;
- source aggregation timezone;
- canonical storage timezone;
- expected response schema;
- provider entitlement status.

The contract never stores API keys, account identity, arbitrary URLs, local
output paths, or mutable period strings.

## Provider Entitlement

Operator-attested provider information:

- provider current brand: `MASSIVE.COM`;
- former brand: `POLYGON.IO`;
- subscription: `STOCKS_STARTER`;
- entitlement evidence: `OPERATOR_ATTESTED`;
- published historical entitlement: `FIVE_YEARS`;
- published data recency: `FIFTEEN_MINUTE_DELAYED`;
- aggregate access: `INTRADAY_AND_DAILY_AVAILABLE`;
- provider entitlement status: `OPERATOR_ATTESTED_CONFIRMED`.

No API key, provider account, billing information, provider portal, or
credential value was inspected.

## Fixed-Date Semantics

Future executable contracts must use explicit ISO calendar dates:

```text
start_date
end_date
```

The start date must be strictly before the end date. Relative values such as
`today`, `now`, `100d`, `365d`, `2y`, or `5y` are rejected. No current-date,
environment, filesystem, or rolling-window default is allowed.

The fictional source-controlled example keeps both dates as:

```text
HUMAN_APPROVAL_REQUIRED
```

That state is valid only while acquisition remains disabled.

## Fixed Profiles

Accepted acquisition requirements remain bound to fixed analysis profiles:

| Profile | Timeframe | Minimum valid OHLCV rows | Multiplier | Timespan | Status |
| --- | --- | ---: | ---: | --- | --- |
| `SWING` | `4h` | 390 | 4 | `hour` | blocked |
| `POSITION_SWING` | `1d` | 560 | 1 | `day` | blocked |

Row gates cannot be weakened by the loader.

## Bar And Session Policy

4h construction is unresolved and scientific-critical. Supported contract
states include:

- `PROVIDER_NATIVE_CLOCK_4H`;
- `DETERMINISTIC_LOCAL_AGGREGATION`;
- `BAR_CONSTRUCTION_NOT_CONFIRMED`.

The current proposed state for `SWING` is:

```text
BAR_CONSTRUCTION_NOT_CONFIRMED
```

Daily bars are represented as:

```text
PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW
```

Session policy must be explicit and part of the digest. Supported states are:

- `REGULAR_TRADING_HOURS_ONLY`;
- `EXTENDED_HOURS_INCLUDED`;
- `PROVIDER_DEFAULT_SESSION`;
- `SESSION_POLICY_NOT_CONFIRMED`.

The current proposed state is `SESSION_POLICY_NOT_CONFIRMED`.

## Timezone And DST

The contract records:

- source aggregation timezone: `AMERICA_NEW_YORK`;
- original provider timestamps: preserve provider epoch timestamps;
- canonical storage timezone: `UTC`;
- source-local timezone metadata for diagnostics;
- DST conversion policy: epoch to UTC first, then source-local diagnostics.

Naive timestamps are prohibited for canonical normalized datasets. Ambiguous or
nonexistent local DST times must fail unless resolved deterministically from
provider epoch timestamps.

## Adjustment Policy

Required proposed adjustment state:

```text
split_adjusted_requested = true
provider_adjusted_response = MUST_MATCH_REQUEST
dividend_adjusted = false
corporate_action_metadata_status = NOT_CONFIRMED
adjustment_provenance_status = CONTRACT_PROPOSED
```

Adjustment mismatch invalidates acquisition. No dividend-adjustment claim is
made. Corporate-action processing is future work.

## Pagination And Completeness

The future acquisition contract requires:

- explicit base-aggregate limit;
- maximum supported limit;
- request chunk boundaries;
- iterator exhaustion;
- duplicate-boundary rejection;
- response-count validation where meaningful;
- no partial result acceptance;
- no silent truncation, repeated page, skipped page, or first-page-only
  assumption.

Fixed completeness statuses include:

- `REQUEST_COMPLETE`;
- `REQUEST_TRUNCATED`;
- `PAGINATION_INCOMPLETE`;
- `PAGE_DUPLICATE`;
- `RANGE_COVERAGE_INCOMPLETE`;
- `PROVIDER_RESPONSE_INVALID`.

Provider pagination is not implemented or run by this contract module.

## Response Validation

Future responses must validate:

- status;
- ticker;
- adjusted flag;
- timezone-aware UTC timestamps;
- ascending order;
- no duplicate timestamps;
- finite OHLCV;
- `high >= low`;
- nonnegative volume;
- completed bars only;
- no unknown response shape.

No partial CSV may be committed after validation failure.

## Raw And Normalized Artifacts

The design defines two immutable future artifacts:

1. `RAW_PROVIDER_RESPONSE`
2. `NORMALIZED_OHLCV_DATASET`

Raw response bytes should be preserved where practical and permitted. The
normalized dataset is deterministic OHLCV with UTC timestamps and contracted
optional provider fields only.

Future provenance records include raw digest, normalized digest, parent
relationship, request-contract digest, code commit, retrieval timestamp,
source timezone, adjustment metadata, completeness status, and no credential or
absolute path.

## Artifact Lineage Extension

Future lineage chain:

```text
ACQUISITION_REQUEST_CONTRACT
  -> RAW_PROVIDER_RESPONSE
  -> NORMALIZED_OHLCV_DATASET
  -> ANNOTATED_DATASET
```

This is a proposed extension to Artifact Lineage v1. Current accepted lineage
semantics are not rewritten by this task.

## Offline CLI

The dry CLI is:

```powershell
env\Scripts\python.exe -m marketflow.research.fixed_date_acquisition_contract
```

It validates the fictional source-controlled example, computes a deterministic
digest, and prints a sanitized readiness receipt. It does not accept ticker,
date, or API-key flags.
