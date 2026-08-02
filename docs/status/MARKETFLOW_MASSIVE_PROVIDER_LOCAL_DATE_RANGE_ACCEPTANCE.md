# MarketFlow Massive Provider-Local Date-Range Acceptance

UTC acceptance date: `2026-08-02T09:04:41Z`.

Commit scope: final offline acceptance and local commit for the Massive.com
provider-local date-range correction on branch
`fix/swing-massive-provider-local-date-range`.

Parent commit:

```text
c8d81c586da0f06116cc02e333d64a2ea4f7bf26
```

## Accepted Status

`MASSIVE_PROVIDER_LOCAL_DATE_RANGE_CORRECTION_ACCEPTED_OFFLINE`

The January-2025 rejection was confirmed as a parser boundary defect, not a
provider schema defect. The previous parser compared provider UTC dates to the
effective local month and rejected after-hours January 31, 2025 source windows
whose canonical UTC timestamps fell on February 1, 2025.

The corrected contract validates Contract v2.1 source windows against
`America/New_York` provider-local bounds converted to UTC:

```text
local_start = effective_start 00:00 America/New_York
local_end_exclusive = day after effective_end 00:00 America/New_York
accepted interval = utc_start <= window_start_utc < utc_end_exclusive
accepted interval end = window_end_utc <= utc_end_exclusive
```

The canonical row timezone remains UTC. The source-local timezone is
`America/New_York`.

## Root Defect Evidence

Before the production correction, the focused reproduction test failed with a
`ProviderResponseError` because the previous UTC-date check treated
`2025-02-01T00:45:00Z` as outside the January-2025 request even though it is
`2025-01-31 19:45 America/New_York`.

The defect was therefore:

```text
old boundary = window_start_utc.date() <= effective_end
correct boundary = provider-local source window inside effective local date range
```

January 31, 2025 was a Friday, so after-hours source rows could legitimately
spill into the next UTC date. January 31, 2026 was a Saturday, so the same
month-end UTC spill was not present in the accepted January-2026 diagnostic
evidence.

## Boundary Acceptance

The offline correction accepts these January-2025 source windows:

- `2025-01-01 00:00 America/New_York`.
- `2025-01-31 19:00 America/New_York` as `2025-02-01T00:00:00Z`.
- `2025-01-31 19:45 America/New_York` as `2025-02-01T00:45:00Z`.
- `2025-01-31 23:45 America/New_York` as `2025-02-01T04:45:00Z`, ending exactly at the upper bound.

The offline correction rejects:

- `2025-02-01 00:00 America/New_York`.
- Any source window whose 15-minute interval end exceeds the exclusive local upper bound.
- Naive timestamps.
- Duplicate or nonascending timestamps.

Summer DST coverage uses `ZoneInfo`, not a fixed offset:

- `2025-07-31 23:45 America/New_York` is accepted as `2025-08-01T03:45:00Z`.
- `2025-08-01 00:00 America/New_York` is rejected.

## Failure Classification

Out-of-range source windows are classified separately from schema failures:

```text
failure_category = TIMESTAMP_RANGE_INVALID
failure_stage = TIMESTAMP_RANGE
finding = SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE
```

This failure is not reported as `SCHEMA_FAILURE`,
`RESPONSE_SCHEMA_INVALID`, pagination failure, authentication failure, or
transport failure. Schema validations for top-level fields, row fields, count
coherence, `otc` type, numeric finite values, OHLCV geometry, negative volume,
and credential-like continuation URLs remain schema-path failures.

## Monthly Acquisition Boundary

Monthly acquisition now uses provider-local coverage for the first and last
accepted source windows while retaining canonical UTC chronology in raw and
normalized rows.

The executor does not apply RTH filtering. Accepted premarket, regular-session,
and after-hours source rows remain present for later bar-construction policy
work. No sorting repair, synthetic values, provider-account inspection, or
Contract date change is introduced.

## Diagnostic and Smoke Boundary

The January-2026 diagnostic remains accepted. A synthetic January-2025 response
with provider-local after-hours UTC spill is accepted through the same parser
path. Timestamp-range failures propagate with the bounded timestamp-range
category into the date diagnostic, monthly acquisition, and one-month smoke
paths.

No raw or normalized artifacts are written for invalid timestamp-range input.

## Contract and Digest Evidence

The fixed Contract range remains:

```text
2022-01-01 through 2025-12-31
```

Reproduced contract digests:

```text
v1   29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
v2   59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
v2.1 538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
```

Existing Massive.com diagnostic and smoke specification digests remain:

```text
2025 date diagnostic b90f5e8d681be1ca753f2fccd78ed778341aefb6d6c4fb89b1d657376a5e8e98
2026 date diagnostic 588e61a824799f24feedfeaa9b4629ed2f623b5ff0490624089562ca0eb63376
2025 smoke runner   2116c4dfa3e8ea759e5bca09cf0f4ccc329134f0cac1329ad871fb7746cdcfe4
```

## Independent Review

Two bounded read-only reviewers inspected the dirty correction before final
acceptance:

- Reviewer A: no findings. Confirmed provider-local bounds, interval-end logic,
  DST coverage, timestamp strictness, and monthly extended-hours retention.
- Reviewer B: no findings. Confirmed timestamp-range classification remains
  separate from schema/auth/pagination failures and that schema/count/OTC
  validations remain on the schema path.

Reviewer residual risks were limited to non-execution by the read-only
reviewers and the absence of explicit March/November DST transition-day tests.
The implementation delegates timezone rules to `zoneinfo`.

## Offline Validation Commands

The following checks are required for final acceptance and were run locally:

```text
env\Scripts\python.exe -m pip check
env\Scripts\python.exe -m pytest -q tests/test_massive_date_diagnostic.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py
env\Scripts\python.exe -m pytest --collect-only -q
env\Scripts\python.exe -m pytest -q
env\Scripts\python.exe -W error -m compileall marketflow tests
git diff --check
git diff --cached --check
```

Focused and full pytest were also rerun after staging the accepted source.

## Non-Actions

No provider API call was made by this acceptance task. No API key value,
provider account, billing information, provider portal, or credential was
inspected. No acquisition was enabled.

No Polygon SDK install, upgrade, replacement, or package change was performed.
The provider business identity is represented as Massive.com while legacy
Polygon adapter/package naming remains where it accurately describes installed
code.

No Strategy, Monte Carlo, outcome labeling, profitability, broker, execution,
registry rewrite, report rewrite, runtime ingestion migration, bar-construction
policy approval, session-policy approval, corporate-action provenance approval,
or pagination-completeness acceptance was introduced.

The remaining blockers are unchanged:

- fixed start date;
- fixed end date;
- 4h bar-construction policy;
- session policy;
- adjustment/corporate-action provenance;
- pagination and completeness acceptance.
