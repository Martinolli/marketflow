# MarketFlow Bar And Session Policy

## Status

Policy status: PROPOSED WITH BLOCKERS.

No bar-construction or session policy is approved by this document.

## Current Inventory Finding

Current legacy acquisition paths support interval strings that map directly to
provider aggregate parameters:

- `4h` maps to `multiplier=4`, `timespan=hour`;
- `1d` maps to `multiplier=1`, `timespan=day`;
- other legacy intervals remain present but are outside the accepted fixed
  research profiles.

The current code does not prove whether historical 4h files were produced from:

- provider-native 4h clocks;
- local aggregation from 1h;
- local aggregation from minute bars;
- another path.

Current 4h provenance is therefore:

```text
UNKNOWN_PROVENANCE
```

No session inference is made from existing timestamps alone.

## Four-Hour Construction Modes

Allowed proposed modes:

- `PROVIDER_NATIVE_CLOCK_4H`;
- `DETERMINISTIC_LOCAL_AGGREGATION`;
- `BAR_CONSTRUCTION_NOT_CONFIRMED`.

Current `SWING` state:

```text
BAR_CONSTRUCTION_NOT_CONFIRMED
```

### Provider-Native Clock 4h

If later approved, the contract must explicitly document:

- provider hour snapping;
- source timezone;
- multiplier-window behavior;
- extended-hours inclusion;
- full/partial bar policy;
- risk that provider windows do not align with 09:30-16:00 regular hours.

This mode is not approved by this task.

### Deterministic Local Aggregation

If later approved, a separate contract must define:

- base timeframe;
- session open and close;
- bar anchors;
- short final session bar treatment;
- early-close treatment;
- DST handling;
- extended-hours handling;
- missing base bars;
- OHLCV aggregation formulas.

Local aggregation is represented but not implemented in this task.

## Daily Bars

Current `POSITION_SWING` daily-bar state:

```text
PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW
```

The daily contract still must record:

- source aggregation timezone;
- session inclusion;
- split-adjusted status;
- dividend-adjustment limitation;
- missing-bar behavior;
- provider response metadata;
- fixed start and end dates.

The existence of `1d` data does not approve daily session semantics.

## Session Modes

Allowed session policy states:

- `REGULAR_TRADING_HOURS_ONLY`;
- `EXTENDED_HOURS_INCLUDED`;
- `PROVIDER_DEFAULT_SESSION`;
- `SESSION_POLICY_NOT_CONFIRMED`.

Current state:

```text
SESSION_POLICY_NOT_CONFIRMED
```

Requirements:

- no hidden default;
- no inference from timestamps alone;
- no silent mixing of pre-market, regular, and post-market bars;
- session policy is part of the contract digest;
- one profile cannot differ from another without an explicit profile-contract
  revision.

No exchange holiday calendar is invented in this task.

## Full And Partial Bars

Future canonical historical datasets contain completed bars only.

Policy:

- partial final bars are rejected;
- the acquisition end date must not include an unfinished current bar;
- provider omission of no-trade intervals is retained as absence;
- no zero-volume synthetic bars;
- no OHLC forward fill;
- no future fill;
- no manually invented bars.

No actual cutoff date is selected here.

## Timezone And DST

Provider epoch timestamps must be converted to UTC first. Source-local time may
then be derived for diagnostics.

Canonical normalized datasets must not store naive timestamps as authoritative.
Ambiguous or nonexistent local times fail unless source epoch timestamps resolve
them deterministically.
