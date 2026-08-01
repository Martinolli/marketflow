# MarketFlow Frozen Calendar Bar Engine Plan

## Status

Plan status: IMPLEMENTED FOR OFFLINE SYNTHETIC USE.

Date: 2026-08-01.

Branch: `feature/swing-frozen-calendar-bar-engine-v2-1`.

Base commit: `4cc9b2caf784c87dc5476ecefd147bd4f8a55c34`.

## Scope

This implementation resumes the previously blocked frozen-calendar and RTH bar
engine after accepted Contract v2.1 established source 15-minute timestamp
semantics.

The implementation is limited to:

- offline frozen-calendar preview generation;
- requested MIC and resolved calendar identity recording;
- exact start-stamped 15-minute source-window validation;
- deterministic RTH session validation;
- extended-hours exclusion receipts;
- early-close exclusion;
- `SWING` half-session aggregation;
- `POSITION_SWING` full-session aggregation;
- ex-dividend analytical segment tagging;
- current-segment prefix helpers;
- deterministic receipts and source-assurance tests.

## Contract Dependency

Accepted Contract v2.1 supplies the required timestamp boundary:

```text
provider_endpoint_family = STOCKS_CUSTOM_BARS_V2
provider_timestamp_field = t
provider_timestamp_unit = UNIX_EPOCH_MILLISECONDS
provider_timestamp_semantic = START_OF_AGGREGATE_WINDOW
source_interval_duration = PT15M
interval_boundary = LEFT_CLOSED_RIGHT_OPEN
timestamp_utc compatibility semantic = WINDOW_START
derived_bar_timestamp_semantic = WINDOW_END
```

Contract v1, v2, and v2.1 semantic content and digests remain unchanged.

## Implementation

Created isolated package:

```text
marketflow/historical_data/__init__.py
marketflow/historical_data/frozen_calendar.py
marketflow/historical_data/rth_bar_engine.py
marketflow/historical_data/analytical_segments.py
marketflow/historical_data/__main__.py
```

Created focused tests:

```text
tests/test_historical_data_engine.py
```

## Non-Goals

This task does not implement provider acquisition, provider requests,
normalization jobs, generated canonical datasets, operator calendar freeze,
registry approval, runtime profile migration, annotation, Strategy candidate
generation, Monte Carlo, outcomes, broker integration, or performance analysis.

## Verification Plan

Required final checks:

```text
env\Scripts\python.exe -m pip check
env\Scripts\python.exe -m pytest tests\test_historical_data_engine.py tests\test_acquisition_contract_v2_1.py tests\test_acquisition_contract_v2.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py -q
env\Scripts\python.exe -m pytest --collect-only -q
env\Scripts\python.exe -m pytest -q
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
git diff --check
```

## Verification Result

- Focused historical-data suite: 13 passed.
- Focused historical-data plus v1/v2/v2.1 regression and source assurance:
  99 passed.
- Full collection: 696 tests collected.
- Full default suite: 696 passed.
- `pip check`: passed.
- Compileall with warnings as errors: passed.
- `git diff --check`: passed.
- Packaging metadata: exact `exchange_calendars==4.13.2` declaration added to
  `requirements.txt`.
