# MarketFlow Frozen Calendar And RTH Bars

## Status

Architecture status: IMPLEMENTED FOR OFFLINE SYNTHETIC USE.

The package is isolated under:

```text
marketflow/historical_data/
```

It imports no provider, candidate builder, Monte Carlo, outcome evaluator,
Streamlit, or LLM modules. It reads no credentials or environment
configuration and writes no runtime registry state.

## Calendar Boundary

Calendar generation requires:

```text
exchange_calendars == 4.13.2
```

Version mismatch fails closed with:

```text
CALENDAR_IMPLEMENTATION_VERSION_MISMATCH
```

No weekday fallback, alternate calendar package fallback, or provider schedule
download exists.

## Calendar Request

The immutable request records:

- schema version;
- Contract v2.1 digest;
- requested primary-listing MIC;
- requested package calendar token;
- fixed range `2022-01-01` through `2025-12-31`;
- source timezone `America/New_York`;
- canonical timezone `UTC`;
- `exchange_calendars` version;
- tzdata version;
- official evidence identity and digest;
- calendar-generation code version.

The engine receives no ticker. Requested MIC and resolved calendar identity
remain distinct.

## Calendar Artifact

The immutable frozen-calendar preview records:

- requested MIC;
- requested calendar token;
- resolved calendar;
- alias relationship;
- normal full sessions;
- early-close sessions;
- explicitly represented closed dates;
- UTC open and close timestamps;
- semantic digest.

Normal sessions require local `09:30` through `16:00 America/New_York`.
Early-close sessions are excluded from derived canonical bars.

## Source Bars

Source bars are immutable analytical rows:

```text
window_start_utc
window_end_utc
open
high
low
close
volume
```

`timestamp_utc` compatibility metadata means `WINDOW_START`.

Validation rejects naive timestamps, non-UTC windows, non-15-minute duration,
nonaligned source starts, binary floats, NaN, Infinity, high below low,
negative volume, duplicate starts, unsorted starts, snapping, and tolerance.

## RTH Slots

Expected ordinary source starts:

- `09:30` through `12:30`, 13 morning windows;
- `12:45` through `15:45`, 13 afternoon windows;
- 26 full-session windows.

A source bar beginning at `16:00 America/New_York` is outside RTH. Extended
hours are counted in sanitized receipts and never replace missing RTH slots.

## Derived Bars

`SWING` derives `RTH_HALF_SESSION_195M` bars:

- morning: `[09:30,09:45)` through `[12:30,12:45)`, timestamp `12:45` local;
- afternoon: `[12:45,13:00)` through `[15:45,16:00)`, timestamp `16:00` local.

`POSITION_SWING` derives `RTH_FULL_SESSION_1D` bars:

- full RTH source windows, timestamp `16:00` local.

Aggregation is first open, maximum high, minimum low, final close, and exact
Decimal volume sum. No provider-native 4h or daily fallback exists.

## Runtime Boundary

The current runtime status remains:

```text
LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION
```

No `marketflow normal <ticker>` behavior is changed.
