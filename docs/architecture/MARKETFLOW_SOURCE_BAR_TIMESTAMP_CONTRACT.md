# MarketFlow Source Bar Timestamp Contract

## Status

Contract architecture status: READY FOR IMPLEMENTATION.

This document describes the narrow Contract v2.1 correction for the source
15-minute aggregate timestamp semantic. It does not implement acquisition,
calendar generation, bar construction, normalization, registry approval, or
runtime migration.

## Endpoint Binding

The timestamp policy applies only to:

```text
STOCKS_CUSTOM_BARS_V2
```

It is not generalized to grouped daily summaries, previous-day endpoints,
WebSocket aggregates, or another provider endpoint. Any other endpoint requires
a new endpoint-specific timestamp contract.

## Provider Timestamp

The provider result field is:

```text
t
```

Contracted meaning:

```text
UNIX_EPOCH_MILLISECONDS
START_OF_AGGREGATE_WINDOW
```

The decoded UTC instant is the canonical `window_start_utc`.

## Source Interval

The source interval is:

```text
PT15M
LEFT_CLOSED_RIGHT_OPEN
```

Canonical interval:

```text
[window_start_utc, window_end_utc)
```

where:

```text
window_end_utc = window_start_utc + PT15M
```

No tolerance, rounding, nearest-slot snapping, caller-selected timestamp
semantic, naive timestamp, or local-machine timezone dependency is permitted.

## Normalized Source Bar Identity

Future normalized source bars are identified by:

```text
window_start_utc
window_end_utc
open
high
low
close
volume
```

Compatibility metadata may retain `timestamp_utc`, but its meaning is fixed as
`WINDOW_START` and must not conflict with `window_start_utc`.

## RTH Source Slot Examples

Ordinary RTH source starts:

- morning: `09:30` through `12:30`, 13 bars;
- afternoon: `12:45` through `15:45`, 13 bars;
- full day: 26 bars.

Examples:

- `09:30` local start maps to `[09:30, 09:45)`;
- `12:30` local start is the final morning slot;
- `12:45` local start is the first afternoon slot;
- `15:45` local start maps to `[15:45, 16:00)`;
- no source bar beginning at `16:00` belongs to the RTH session.

## Derived Bar Timestamp Contract

Derived MarketFlow bars remain close-stamped:

- `SWING` morning: `12:45 America/New_York` converted to UTC;
- `SWING` afternoon: `16:00 America/New_York` converted to UTC;
- `POSITION_SWING`: `16:00 America/New_York` converted to UTC.

Provider-native 4h and daily substitutions remain prohibited.

## Runtime Boundary

Current runtime migration remains:

```text
LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION
```

Contract v2.1 does not change `marketflow normal <ticker>` behavior.
