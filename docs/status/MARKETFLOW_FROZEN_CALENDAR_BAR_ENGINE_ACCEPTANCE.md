# MarketFlow Frozen Calendar Bar Engine Acceptance

## Decision

FROZEN CALENDAR AND RTH BAR ENGINE: PASS FOR OFFLINE DETERMINISTIC MECHANICS.

PROVIDER EXECUTOR: NOT IMPLEMENTED.

OPERATOR CALENDAR FREEZE: NOT PERFORMED.

CANONICAL DATASETS: NOT AVAILABLE.

DATA ACQUISITION: DISABLED.

UTC acceptance date: `2026-08-01T16:33:34Z`.

Branch: `feature/swing-frozen-calendar-bar-engine-v2-1`.

Base commit: `4cc9b2caf784c87dc5476ecefd147bd4f8a55c34`.

No tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- isolated `marketflow.historical_data` package;
- pinned offline exchange-calendar preview generation;
- immutable frozen-calendar request and artifact models;
- requested MIC and resolved-calendar separation;
- start-stamped Contract v2.1 source-window validation;
- deterministic RTH session validation;
- extended-hours exclusion receipts;
- early-close exclusion;
- deterministic `SWING` half-session bars;
- deterministic `POSITION_SWING` full-session daily bars;
- offline ex-dividend analytical segment tagging;
- current-segment prefix helper;
- dry offline CLI;
- focused deterministic tests and source assurance.

Excluded scope:

- provider calls or provider executor;
- provider account, billing, portal, API-key, credential, or browser review;
- downloaded/provider market data;
- generated canonical market datasets;
- operator calendar freeze ceremony;
- registry authority or quarantine governance;
- annotation;
- Strategy candidate generation;
- Monte Carlo;
- outcome evaluation;
- performance analysis;
- broker integration;
- execution capability;
- normal ticker-only runtime migration.

## Dependency And Packaging Declaration

Runtime dependency:

```text
exchange_calendars==4.13.2
```

The installed runtime package version was verified as `4.13.2`.

Packaging review found the dependency was installed but not declared in the
authoritative `requirements.txt` consumed by `setup.py`. Disposition: fixed by
adding the exact pin `exchange_calendars==4.13.2` to `requirements.txt`.

No dependency was installed, upgraded, downgraded, renamed, or removed.

## Contract Digest Non-Regression

Contract v1 digest:

```text
29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
```

Contract v2 digest:

```text
59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
```

Contract v2.1 digest:

```text
538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
```

No Contract v1, v2, or v2.1 semantic file was modified.

## Calendar Model

The calendar implementation creates deterministic immutable preview artifacts
with:

- schema version;
- Contract v2.1 digest;
- requested primary-listing MIC;
- requested package calendar token;
- resolved package calendar;
- alias relationship;
- `exchange_calendars` version;
- tzdata version;
- fixed contract range;
- source timezone;
- canonical timezone;
- official exchange-evidence identity and digest;
- normal sessions;
- early-close sessions;
- explicitly represented closed dates;
- semantic digest.

Default dry CLI preview:

- requested primary-listing MIC: `XNYS`;
- requested calendar token: `XNYS`;
- resolved calendar: `XNYS`;
- calendar status: `CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE`;
- normal full sessions: 994;
- early-close sessions: 9;
- calendar digest:
  `31f35f9cf46ec509a712b20feb4c695542e8b8b67e51fe7621c7379de5aac70f`.

Package generation alone is not treated as operator-frozen authority.

## Requested MIC And Resolved Calendar

Requested primary-listing MIC is retained separately from requested calendar
token and resolved package calendar. Alias relationships such as
`XNAS_USES_XNYS_SCHEDULE` are recorded without rewriting the requested listing
venue.

## Timezone And DST

Source timezone is `America/New_York`.

Canonical timezone is `UTC`.

Focused tests verify:

- winter `09:30 America/New_York` maps to `14:30 UTC`;
- summer `09:30 America/New_York` maps to `13:30 UTC`;
- source intervals remain exactly 15 minutes.

Calendar and source-bar timestamps are timezone-aware UTC.

## Source Timestamp And Interval

Contract v2.1 semantics are enforced:

```text
provider timestamp field = t
provider timestamp unit = UNIX_EPOCH_MILLISECONDS
provider timestamp semantic = START_OF_AGGREGATE_WINDOW
source interval = [window_start_utc, window_end_utc)
window_end_utc = window_start_utc + PT15M
timestamp_utc compatibility semantic = WINDOW_START
```

No source bar is treated as close-stamped.

## Source-Bar Validation

The immutable `SourceBar` validates:

- `window_start_utc` and `window_end_utc` are UTC-aware;
- end equals start plus exactly 15 minutes;
- UTC and local starts align to exact 15-minute slots;
- OHLCV values are exact `Decimal`;
- binary floats are rejected for source values;
- NaN and Infinity are rejected;
- high is greater than or equal to low;
- volume is nonnegative;
- duplicate or non-monotonic starts fail closed;
- no snapping or tolerance is available.

Audit finding:

```text
HIGH - source-bar datetimes with non-UTC timezone offsets were normalized to
UTC instead of rejected.
```

Disposition: fixed. Non-UTC aware source datetimes now fail closed and focused
coverage was added.

## Session Classifications

Fixed classifications:

- `NORMAL_FULL_SESSION`;
- `EARLY_CLOSE_SESSION`;
- `FULL_MARKET_CLOSED`;
- `CALENDAR_SOURCE_UNRESOLVED`;
- `CALENDAR_CONFLICT`.

A normal full session must map to `09:30-16:00 America/New_York`.

Early-close sessions are excluded entirely. Closed dates create no expected
analytical bar. Missing source bars do not infer a closure or early close.

## RTH Slot Contract

Ordinary full sessions require exact start-stamped source windows:

- full day: `09:30` through `15:45`, count 26;
- morning: `09:30` through `12:30`, count 13;
- afternoon: `12:45` through `15:45`, count 13.

Confirmed boundaries:

- `[09:30,09:45)` first RTH interval;
- `[12:30,12:45)` final morning interval;
- `[12:45,13:00)` first afternoon interval;
- `[15:45,16:00)` final RTH interval;
- source start at `16:00` is outside RTH;
- no overlap or gap between morning and afternoon groups.

Missing, duplicate, extra, or unordered RTH slots fail closed. Extended-hours
slots never replace missing RTH slots.

## SWING Aggregation

`SWING` derives deterministic `RTH_HALF_SESSION_195M` bars:

- morning: 13 exact source bars, derived timestamp `12:45` local converted to
  UTC;
- afternoon: 13 exact source bars, derived timestamp `16:00` local converted
  to UTC.

Aggregation:

- open: first source open;
- high: exact maximum;
- low: exact minimum;
- close: last source close;
- volume: exact Decimal sum.

No partial bar, shortened bar, or provider-native 4h fallback exists.

## POSITION_SWING Aggregation

`POSITION_SWING` derives deterministic `RTH_FULL_SESSION_1D` bars:

- exactly 26 source bars;
- full-session OHLCV;
- exact Decimal volume sum;
- derived timestamp `16:00` local converted to UTC.

No provider-native daily fallback exists.

## Derived Result And Receipts

Derived result and public receipt models report:

- Contract v2.1 digest;
- frozen-calendar digest;
- profile;
- accepted full-session count;
- early-close exclusions;
- extended-hours exclusions;
- invalid/incomplete session counts;
- produced bar count;
- fixed findings;
- semantic dataset digest.

Public receipts do not expose OHLCV values or absolute paths. A normal
incomplete session returns blocked derivation status rather than a false
complete dataset claim.

## Ex-Dividend Segmentation

The segment engine receives explicit dividend evidence only. No
corporate-action provider is called.

Rules:

- normal ex-dividend sessions start a new segment before the first canonical
  bar of that session;
- both SWING bars and the POSITION_SWING bar for that session belong to the new
  segment;
- early-close or closed ex-dividend dates defer the boundary to the next
  eligible full-session canonical bar;
- multiple same-date events produce one boundary retaining all event IDs.

Segment start reasons are fixed:

```text
DATASET_START
EX_DIVIDEND_CONTINUITY_RESET
```

## Component Readiness And Prefix Safety

New segment status:

```text
ANALYTICAL_SEGMENT_WARMUP
```

There is no guessed global wait, manual unlock, fabricated readiness, or
candidate actionability.

The prefix helper returns only current-segment bars at or before decision row
`T`. Focused tests cover prior-segment exclusion, future-row exclusion,
future-bar invariance, and future-dividend-event invariance.

## Dry CLI

Command:

```text
env\Scripts\python.exe -m marketflow.historical_data
```

The CLI validates Contracts v2 and v2.1, verifies the package pin, emits a
sanitized non-ticker readiness receipt, opens no socket, calls no provider,
accepts no ticker, writes no generated calendar or market dataset, runs no
annotation/candidate/MC/outcome path, changes no registry state, and performs
no runtime migration.

## Runtime Non-Migration

The current runtime remains:

```text
LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION
```

`marketflow normal <ticker>` was not changed. The new engine is not silently
consumed by current runtime source resolution.

## Tests

Focused historical-data suite:

```text
env\Scripts\python.exe -m pytest tests\test_historical_data_engine.py -q
```

Result: 13 passed.

Focused historical-data, Contract v1/v2/v2.1 regression, source-assurance, and
prior-integrity suite:

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

The test count increases from the accepted v2.1 baseline of 683 to 696 because
this task adds 13 focused historical-data tests.

## Pip, Compile, And Diff Checks

`pip check`: pass.

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass before staging.

`git diff --cached --check`: pass before commit.

## Warnings

No test or compile warning summary was emitted. No broad warning suppression
was introduced.

## No-Network Evidence

Source-level checks confirm:

- no provider import;
- no credential/environment read;
- no candidate, Monte Carlo, or outcome import;
- no Streamlit or LLM import;
- exact `exchange_calendars` version requirement;
- no calendar fallback;
- start-stamped source bars;
- no timestamp snapping or tolerance;
- no provider-native 4h or daily path;
- early-close exclusion;
- no missing-slot repair;
- no synthetic bars;
- no runtime migration.

The default pytest socket guard remained active in the full suite.

## Git Status Evidence

Pre-test Git status:

```text
?? docs/architecture/MARKETFLOW_FROZEN_CALENDAR_AND_RTH_BARS.md
?? docs/plans/MARKETFLOW_FROZEN_CALENDAR_BAR_ENGINE_PLAN.md
?? docs/research/MARKETFLOW_ANALYTICAL_SEGMENT_POLICY.md
?? docs/status/MARKETFLOW_FROZEN_CALENDAR_BAR_ENGINE_STATUS.md
?? marketflow/historical_data/
?? tests/test_historical_data_engine.py
```

Post-test Git status before staging:

```text
 M requirements.txt
?? docs/architecture/MARKETFLOW_FROZEN_CALENDAR_AND_RTH_BARS.md
?? docs/plans/MARKETFLOW_FROZEN_CALENDAR_BAR_ENGINE_PLAN.md
?? docs/research/MARKETFLOW_ANALYTICAL_SEGMENT_POLICY.md
?? docs/status/MARKETFLOW_FROZEN_CALENDAR_BAR_ENGINE_ACCEPTANCE.md
?? docs/status/MARKETFLOW_FROZEN_CALENDAR_BAR_ENGINE_STATUS.md
?? marketflow/historical_data/
?? tests/test_historical_data_engine.py
```

No tracked file was modified by tests other than the intentional dependency
declaration update made before final validation.

## Reviewer Findings

Reviewer A:

```text
HIGH - exchange_calendars was installed but not declared in authoritative
packaging metadata. Fixed by adding exchange_calendars==4.13.2 to
requirements.txt.
```

```text
HIGH - non-UTC aware source datetimes were normalized instead of rejected.
Fixed with fail-closed UTC validation and focused regression coverage.
```

Disposition: fixed. No high finding remains.

Reviewer B:

```text
No high finding after corrections. Segmentation, prefix safety, runtime
isolation, dry CLI/no-network, source assurance, tests/docs, and previous
integrity preservation are covered.
```

Disposition: accepted.

## Remaining Limitations

- Frozen-calendar/bar-engine implementation is accepted only for offline
  deterministic mechanics.
- No provider data was used.
- No actual calendar was operator-frozen.
- No acquisition executor exists.
- No canonical dataset exists.
- Normal runtime migration remains pending.
- Research protocol remains blocked.
- Predictive usefulness and profitability remain unaccepted.

## Next Implementation Phase

Future work may integrate accepted v2.1 canonical datasets and artifact
approval. That phase requires separate acceptance, generated canonical data,
registry approval, and runtime migration review.
