# MarketFlow Frozen Calendar Bar Engine Status

## Status

PASS.

The frozen-calendar and RTH bar-engine implementation may be accepted for
offline synthetic use.

## Initial Evidence

- Date: 2026-08-01.
- Branch: `feature/swing-frozen-calendar-bar-engine-v2-1`.
- Base commit: `4cc9b2caf784c87dc5476ecefd147bd4f8a55c34`.
- Initial working tree: intentionally dirty with four restored docs only.
- Python: `3.12.10` using `env\Scripts\python.exe`.
- `exchange_calendars`: `4.13.2`.
- tzdata: `2025.2` in the local environment.
- `pip check`: pass.
- Dependency declaration: `exchange_calendars==4.13.2` added to
  `requirements.txt`, which is consumed by `setup.py`.

## Contract Digest Non-Regression

- Contract v1 digest:
  `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`.
- Contract v2 digest:
  `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`.
- Contract v2.1 digest:
  `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`.

No Contract v1, v2, or v2.1 semantic content was changed.

## Calendar Result

Implemented immutable frozen-calendar request and artifact models.

Default dry preview:

- requested primary-listing MIC: `XNYS`;
- requested calendar token: `XNYS`;
- resolved calendar: `XNYS`;
- source timezone: `America/New_York`;
- canonical timezone: `UTC`;
- status: `CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE`;
- normal full sessions: 994;
- early-close sessions: 9.

Requested MIC and resolved calendar remain distinct fields. Alias behavior is
recorded when requested token and resolved calendar differ.

No calendar was operator-frozen.

## Timezone And DST

Focused tests verify:

- winter `09:30 America/New_York` maps to `14:30 UTC`;
- summer `09:30 America/New_York` maps to `13:30 UTC`;
- source-window duration remains exactly 15 minutes.

Calendar and source-bar timestamps are timezone-aware UTC.

## Source Timestamp Contract

Source 15-minute bars are start-stamped per Contract v2.1:

```text
START_OF_AGGREGATE_WINDOW
LEFT_CLOSED_RIGHT_OPEN
[window_start_utc, window_end_utc)
timestamp_utc = WINDOW_START
```

No source bar is treated as close-stamped.

## Source-Bar Validation

Implemented strict immutable `SourceBar` validation for:

- UTC-aware start/end;
- rejection of non-UTC aware source datetimes;
- exact 15-minute duration;
- exact UTC and local 15-minute alignment;
- exact Decimal OHLCV;
- finite values only;
- high greater than or equal to low;
- nonnegative volume;
- duplicate/unsorted source-start rejection;
- no binary-float numeric coercion.

## Session And RTH Slot Result

Implemented session outcomes:

- `SESSION_COMPLETE`;
- `EARLY_CLOSE_SESSION_EXCLUDED`;
- `FULL_MARKET_CLOSED`;
- `SESSION_SOURCE_MISSING`;
- `SESSION_SOURCE_INCOMPLETE`;
- `SESSION_SOURCE_DUPLICATE_SLOT`;
- `SESSION_SOURCE_EXTRA_SLOT`;
- `SESSION_SOURCE_INVALID`;
- `CALENDAR_DATA_CONFLICT`.

Normal full sessions require exactly 26 start-stamped source windows. Missing
ordinary slots block dataset completion rather than silently disappearing.

## Aggregation

`SWING`:

- `RTH_HALF_SESSION_195M`;
- morning source starts `09:30` through `12:30`, 13 bars;
- afternoon source starts `12:45` through `15:45`, 13 bars;
- derived timestamps `12:45` and `16:00` local converted to UTC.

`POSITION_SWING`:

- `RTH_FULL_SESSION_1D`;
- exactly 26 source bars;
- derived timestamp `16:00` local converted to UTC.

Aggregation uses first open, max high, min low, final close, and exact Decimal
volume sum. No provider-native 4h or daily fallback exists.

## Early-Close And Extended-Hours Behavior

Early-close sessions are excluded entirely and produce no canonical bars.

Extended-hours source bars are excluded from derived analytical data, counted
in sanitized receipts, and never used as RTH replacements.

## Ex-Dividend Segmentation

Implemented offline segment tagging from explicit dividend evidence only.

Normal-session ex-dividend events reset the current segment at that session.
Early-close or closed-date events reset at the next eligible full-session
canonical bar. Multiple same-date event IDs are retained.

## Component Readiness And Prefix Safety

New segments are tagged:

```text
ANALYTICAL_SEGMENT_WARMUP
```

The current-segment prefix helper returns only current-segment bars through
decision row `T` and excludes prior-segment and future rows.

## Dry CLI

Implemented:

```text
env\Scripts\python.exe -m marketflow.historical_data
```

The CLI validates Contracts v2 and v2.1, verifies the calendar package pin,
generates a sanitized non-ticker calendar preview receipt, and writes no data.

## Tests

Focused historical-data tests:

```text
env\Scripts\python.exe -m pytest tests\test_historical_data_engine.py -q
```

Result: 13 passed.

Focused historical-data plus v1/v2/v2.1 regression and source-assurance suite:

```text
env\Scripts\python.exe -m pytest tests\test_historical_data_engine.py tests\test_acquisition_contract_v2_1.py tests\test_acquisition_contract_v2.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py -q
```

Result: 99 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 696 collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 696 passed.

The test count increases from the accepted Contract v2.1 baseline of 683 to
696 because this task adds 13 focused historical-data engine tests.

Compileall:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

Diff check:

```text
git diff --check
```

Result: pass.

Post-test Git status:

```text
?? docs/architecture/MARKETFLOW_FROZEN_CALENDAR_AND_RTH_BARS.md
?? docs/plans/MARKETFLOW_FROZEN_CALENDAR_BAR_ENGINE_PLAN.md
?? docs/research/MARKETFLOW_ANALYTICAL_SEGMENT_POLICY.md
?? docs/status/MARKETFLOW_FROZEN_CALENDAR_BAR_ENGINE_STATUS.md
?? marketflow/historical_data/
?? tests/test_historical_data_engine.py
```

## No-Network Evidence

The package imports no provider, no candidate builder, no Monte Carlo, no
outcome evaluator, no Streamlit, and no LLM modules. It reads no credentials or
environment configuration and opens no socket.

## Reviewer Findings

Reviewer A:

```text
No high finding after focused tests. Contract v2.1 start-stamp boundary,
package pin, MIC/calendar resolution, DST, session slots, aggregation, and
Decimal behavior are covered.
```

Reviewer B:

```text
No high finding after focused tests. Ex-dividend segmentation, prefix safety,
runtime isolation, dry CLI/no-network behavior, source assurance, docs, and
prior integrity are covered.
```

## Blockers

None for offline synthetic-use acceptance.

## Remaining Limitations

- No provider data was used.
- No calendar was operator-frozen.
- No provider executor exists.
- No canonical dataset exists.
- Normal runtime migration remains pending.
- Research protocol remains blocked.
- Predictive usefulness and profitability remain unaccepted.

## Prohibited Actions

No commit or tag was created.

No provider call, calendar-network access, data download, annotation, candidate
generation, Monte Carlo, outcome evaluation, performance analysis, broker
integration, execution capability, source modification, report rewrite,
registry-authority operation, or runtime profile migration was added or
exercised.
