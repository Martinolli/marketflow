# MarketFlow Timestamp Semantics Decision

## Decision

Contract v2.1 fixes one missing Contract v2 field: source 15-minute aggregate
timestamps are start-stamped for the endpoint-specific custom-bars source.

Approved values:

```text
provider_endpoint_family = STOCKS_CUSTOM_BARS_V2
provider_timestamp_field = t
provider_timestamp_unit = UNIX_EPOCH_MILLISECONDS
provider_timestamp_semantic = START_OF_AGGREGATE_WINDOW
source_interval_duration = PT15M
interval_boundary = LEFT_CLOSED_RIGHT_OPEN
```

## Interpretation

Provider field `t` decodes to `window_start_utc`.

The canonical source interval is:

```text
[window_start_utc, window_end_utc)
```

with `window_end_utc` exactly 15 minutes after `window_start_utc`.

## RTH Consequence

The ordinary RTH source sequence begins at `09:30 America/New_York` and ends
with a source bar starting at `15:45 America/New_York`.

No bar starting at `16:00 America/New_York` belongs to the RTH session.

## Derived Bars

Derived bars remain close-stamped:

- `SWING` morning: `12:45 America/New_York`;
- `SWING` afternoon: `16:00 America/New_York`;
- `POSITION_SWING`: `16:00 America/New_York`.

The source bar timestamp semantic and derived bar timestamp semantic are
therefore intentionally different.

## Endpoint Specificity

This decision applies only to `STOCKS_CUSTOM_BARS_V2`. It does not approve
timestamp semantics for other provider endpoints or provider-native 4h/daily
aggregates.

## Remaining Boundary

Contract v2.1 is declarative and offline. The frozen-calendar and RTH bar
engine remains unimplemented until this contract is accepted.
