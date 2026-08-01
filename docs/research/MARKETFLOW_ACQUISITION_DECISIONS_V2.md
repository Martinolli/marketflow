# MarketFlow Acquisition Decisions v2

## Decision Status

Decision set: `marketflow.acquisition_decisions.v2`

Status: `COMPLETE`

Implementation authorization: declarative contract only.

Acquisition authorization: disabled.

## Provider Entitlement

The operator confirmed the provider information for this design:

- current brand: `MASSIVE.COM`;
- former brand: `POLYGON.IO`;
- subscription: `STOCKS_STARTER`;
- entitlement evidence: `OPERATOR_ATTESTED`;
- entitlement status: `OPERATOR_ATTESTED_CONFIRMED`;
- current published historical entitlement: `FIVE_YEARS`;
- current published data recency: `FIFTEEN_MINUTE_DELAYED`;
- aggregate access: `INTRADAY_AND_DAILY_AVAILABLE`.

This task did not inspect API-key values, provider account state, billing
information, the provider portal, or credentials.

## Fixed Range

Approved range:

- `start_date = 2022-01-01`;
- `end_date = 2025-12-31`.

The range is common to all profiles and is not derived from the current date.
Relative periods and rolling windows are prohibited.

## Bar Construction

All future acquisition uses 15-minute source bars.

`SWING` derives canonical 4h research bars from two regular-session segments:

- profile contract version: `SWING_RTH_HALF_SESSION_V1`;
- canonical bar type: `RTH_HALF_SESSION_195M`;
- `09:30` to `12:45`;
- `12:45` to `16:00`.

Each segment requires 13 source bars. Timestamps use bar-close semantics.
Early-close sessions are excluded in full.

`POSITION_SWING` derives canonical daily research bars from the full regular
session:

- profile contract version: `POSITION_SWING_RTH_FULL_SESSION_V1`;
- canonical bar type: `RTH_FULL_SESSION_1D`;
- `09:30` to `16:00`.

The full session requires 26 source bars. Timestamps use session-close
semantics. Early-close sessions are excluded in full.

Provider-native 4h and 1d bars are not canonical for this design.

## Session Policy

The approved session policy is regular trading hours only:

`REGULAR_TRADING_HOURS_ONLY`

Extended hours are excluded from derived datasets. Closure inference from
missing provider bars is prohibited.

## Calendar Policy

The approved calendar architecture is a frozen exchange-aware artifact using:

- `exchange_calendars`;
- version pin `4.13.2`;
- calendar `XNYS`;
- timezone `America/New_York`.

Future implementation must persist the calendar artifact and bind downstream
acceptance to its digest. This task does not install or import the calendar
package and does not generate the artifact.

## Corporate Actions

Split-adjusted provider bars are required. The request must use `adjusted=true`,
and the provider response metadata must match true.

Independent split event audit and dividend event audit are required. Local second
split adjustment and dividend price adjustment are prohibited.

Ex-dividend boundaries reset analytical continuity. Cross-boundary true range and
cross-boundary Wyckoff structure are prohibited.

## Completeness

Acquisition chunks are fixed calendar months across the baseline range.

Acceptance requires:

- mandatory pagination exhaustion;
- no partial-month success;
- one raw page record for each provider page;
- preservation of every attempt;
- explicit handling of multiple valid attempts;
- all expected source slots present after calendar join.

Retry policy permits only `TRANSPORT_TIMEOUT`, `CONNECTION_RESET`, `HTTP_408`,
`HTTP_429`, `HTTP_500`, `HTTP_502`, `HTTP_503`, and `HTTP_504`. Retry-After is
accepted only for HTTP 429 or 503 as strict integer seconds from 0 through 60,
and the effective wait is the maximum of the configured backoff and Retry-After.

## Semantic Equality

Numeric equivalence is:

`STRICT_CANONICAL_DECIMAL_VALUE_EQUALITY`

Provider JSON numbers must not be parsed through binary floats. Tolerance-based
equality is not allowed. NaN and infinity are rejected.

## Remaining Implementation Blockers

The human design decisions are complete, but the following implementation work is
not authorized in this task:

- provider executor;
- frozen calendar artifact generator;
- 15m-to-profile aggregation implementation;
- normalization implementation;
- generation transaction implementation;
- registry authority implementation;
- mutex and authority-journal implementation;
- canonical dataset approval.

Research protocol execution remains blocked until the future implementation is
completed, validated, and separately approved.
