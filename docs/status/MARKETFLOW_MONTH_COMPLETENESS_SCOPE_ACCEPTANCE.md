# MarketFlow Month Completeness Scope Acceptance

UTC acceptance date: `2026-08-02T09:56:53Z`.

Status: `MONTH_COMPLETENESS_SCOPE_CORRECTION_ACCEPTED_FOR_LOCAL_COMMIT`

Branch: `fix/swing-month-completeness-separation`

Parent commit:

```text
75083194f97bce15d3d4f87d8dc3a1a7f8722255
```

## Decision

PASS.

The monthly retrieval-completeness correction is accepted offline for local
commit. Production source was frozen during final acceptance. The successful
live Massive.com smoke was executed before this final acceptance pass against
the same uncommitted production behavior.

## Root Defect

The reproduced defect was a false month-completeness failure. The monthly
executor treated first and last returned source bars as required calendar-month
boundary occupancy. That incorrectly classified a valid exhausted provider page
chain as:

```text
RANGE_COVERAGE_INCOMPLETE
PAGINATION_CHAIN_INVALID
```

Provider retrieval completeness does not require bars for weekends, holidays,
overnight empty periods, every 15-minute clock interval, or intervals without
qualifying trades.

## Corrected Scope

The correction separates:

1. provider page-chain completeness;
2. provider-local request-range containment;
3. later frozen-calendar/RTH session-slot coverage.

Successful monthly `COMPLETE` now means:

```text
PROVIDER_RETRIEVAL_COMPLETE
```

It does not mean canonical profile data complete, RTH data complete, market
session coverage complete, Strategy-ready, registry-approved, or performance
validated.

## Page Chain

A valid one-page accepted response with no continuation reports:

```text
PAGINATION_EXHAUSTED
```

It no longer reports `PAGINATION_CHAIN_INVALID`.

Real pagination defects remain distinct:

- repeated continuation: invalid;
- duplicate/conflicting timestamp: invalid;
- missing required subsequent page: incomplete.

## Request-Range Containment

Returned source windows still must be inside the approved provider-local
`America/New_York` date interval and remain UTC-aware, strictly ordered, and
15-minute source intervals. Genuine out-of-range windows remain blocked through
the accepted timestamp-range category.

The executor no longer requires:

- first returned timestamp equals month start;
- last returned timestamp equals month end;
- continuous returned bars;
- one returned bar for every clock interval.

## Session Coverage

Monthly retrieval records:

```text
MARKET_SESSION_COVERAGE_NOT_EVALUATED
```

The accepted frozen-calendar/RTH bar-engine stage remains responsible for full
session coverage, exact RTH slots, early-close policy, missing RTH bars, and
extended-hours exclusion.

## Manifest

The month-completeness manifest is written only after page-chain exhaustion,
request-range containment, duplicate/conflict checks, and saved raw-page and
attempt-manifest validation.

Manifest scope:

```text
PROVIDER_RETRIEVAL_COMPLETE
```

The manifest does not claim:

- `MARKET_SESSION_COVERAGE_COMPLETE`;
- `CANONICAL_DATASET_COMPLETE`;
- `RTH_DATASET_COMPLETE`.

## Normalized Pair

Successful retrieval creates:

- `MONTH_NORMALIZED_15M_OHLCV`;
- `MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS`.

The normalized pair remains monthly source evidence. It preserves source order,
retains extended-hours rows, performs no RTH filtering, performs no
missing-interval repair, and introduces no synthetic source values.

## Non-Regressions

Preserved:

- first-page authentication failure remains `PAGINATION_NOT_STARTED`;
- first-page schema rejection remains `PAGINATION_NOT_STARTED`;
- first-page timestamp-range rejection remains `PAGINATION_NOT_STARTED`;
- actual pagination loops/conflicts remain invalid;
- missing subsequent page remains incomplete;
- Contract v1/v2/v2.1 digests remain unchanged;
- normal runtime remains unmigrated.

## Final Acceptance Checks

Required checks were run with:

```text
env\Scripts\python.exe
Python 3.12.10
```

Final evidence:

- `pip check`: pass;
- focused tests: pass;
- full collection: pass;
- full default pytest suite: pass;
- compileall with warnings as errors: pass;
- Git diff checks: pass.

## Non-Actions

No additional provider request was made during this final acceptance. No API key,
credential, provider account, provider portal, billing data, raw provider body,
raw request URL, raw continuation URL, request ID value, or runtime payload was
inspected or committed.

No tag was created. No push was performed. The remote was not altered.

No calendar derivation, Strategy, Monte Carlo, outcome, performance, broker,
execution, registry authority, report rewrite, or runtime migration occurred.
