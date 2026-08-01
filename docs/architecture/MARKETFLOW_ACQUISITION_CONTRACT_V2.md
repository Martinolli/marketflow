# MarketFlow Acquisition Contract v2 Architecture

## Purpose

MarketFlow Historical Data Acquisition Contract v2 is a strict, source-controlled
declaration of the approved acquisition design. It is not an acquisition engine.

The implementation lives in:

- `config/fixed_date_acquisition_contract_v2.toml`;
- `marketflow/research/acquisition_contract_v2.py`;
- `tests/test_acquisition_contract_v2.py`.

The historical v1 contract remains unchanged and continues to represent the
previous blocked proposal.

## Provider Identity

The provider business identity is Massive.com.

The legacy provider brand is Polygon.io, and explicit Polygon adapter/package
names are preserved only where they describe the installed local code:

- business provider: `MASSIVE.COM`;
- former brand: `POLYGON.IO`;
- legacy adapter family: `polygon-api-client`;
- legacy adapter version: `1.14.6`;
- SDK migration status: `NOT_PERFORMED`.

No API-key values, provider account, billing information, provider portal, or
credentials are inspected by this contract.

## Contract State

Contract v2 status is:

`ACQUISITION_CONTRACT_V2_READY_FOR_IMPLEMENTATION`

Human acquisition design decisions are complete. Operational acquisition remains
disabled:

- `acquisition_enabled = false`;
- `provider_execution_enabled = false`;
- `calendar_generation_enabled = false`;
- `normalization_enabled = false`;
- `registry_authority_enabled = false`.

## Fixed Range

The common fixed historical range is:

- start date: `2022-01-01`;
- end date: `2025-12-31`;
- inclusive range: true;
- common for all profiles: true.

Rolling windows, relative periods, current-date dependency, ticker-specific
extensions, profile-specific dates, and row-gate auto-extension are prohibited.

## Source Bars

The only approved source acquisition bars are Massive.com 15-minute adjusted
aggregate bars:

- provider source interval: `15m`;
- timespan: `minute`;
- multiplier: `15`;
- adjusted: true;
- sort: `asc`;
- limit: `50000`;
- source timezone: `America/New_York`;
- canonical storage timezone: `UTC`.

Extended-hours source bars are excluded from derived datasets. Provider-native
4h and 1d bars are not canonical.

## Profile Bars

`SWING` uses locally constructed RTH half-session bars:

- profile contract version: `SWING_RTH_HALF_SESSION_V1`;
- canonical bar type: `RTH_HALF_SESSION_195M`;
- source interval: `15m`;
- source bars per canonical bar: `13`;
- minimum valid rows: `390`;
- morning segment: `09:30` to `12:45`;
- afternoon segment: `12:45` to `16:00`;
- timestamp semantic: `BAR_CLOSE_TIMESTAMP`;
- early-close sessions: excluded.

`POSITION_SWING` uses locally constructed RTH full-session daily bars:

- profile contract version: `POSITION_SWING_RTH_FULL_SESSION_V1`;
- canonical bar type: `RTH_FULL_SESSION_1D`;
- source interval: `15m`;
- source bars per canonical bar: `26`;
- minimum valid rows: `560`;
- full session segment: `09:30` to `16:00`;
- timestamp semantic: `SESSION_CLOSE_TIMESTAMP`;
- early-close sessions: excluded.

Higher-timeframe context is explicitly `NOT_IMPLEMENTED`.

## Calendar Architecture

The calendar design is a future frozen, exchange-aware calendar artifact:

- calendar package: `exchange_calendars`;
- package pin: `4.13.2`;
- calendar: `XNYS`;
- requested listing MIC retained separately from the resolved calendar;
- timezone-aware UTC schedule evidence required;
- full regular sessions: included;
- early-close sessions: excluded;
- ad-hoc closures: included;
- closure inference from missing provider bars: prohibited;
- dynamic unfrozen calendar use: prohibited.

The local contract receipt reports package install status using package metadata
only. It does not import `exchange_calendars` and does not generate a calendar.

## Identity And Corporate Actions

Instrument identity is point-in-time and fail-closed:

- identity source: `MASSIVE_POINT_IN_TIME_TICKER_OVERVIEW`;
- required evidence includes requested ticker, FIGI identifiers, CIK, active
  status, name, market, locale, primary exchange, query date, and raw identity
  response digest;
- automatic stitching is prohibited;
- ambiguous identity status is `IDENTITY_AMBIGUOUS_FAIL_CLOSED`.

Corporate action policy requires:

- split-adjusted provider bars;
- `adjusted=true` request and `MUST_MATCH_TRUE` response;
- independent split event audit;
- dividend event audit;
- no local second split adjustment;
- no dividend price adjustment;
- ex-dividend analytical continuity reset.

Cross-boundary true range and Wyckoff structure use are prohibited.

## Completeness And Equivalence

The acquisition design uses fixed calendar-month chunks over the 48-month
baseline range. Pagination exhaustion, raw provider page preservation, attempt
preservation, and all expected source slots after calendar join are required.

Semantic equivalence is strict:

- numeric equality: `STRICT_CANONICAL_DECIMAL_VALUE_EQUALITY`;
- provider JSON numbers must be parsed without binary float;
- tolerance is not allowed;
- NaN and infinity are rejected;
- negative zero canonicalizes to zero.

Core strategy columns are separated from audit columns. Supplemental audit fields
are prohibited from strategy input.

## Governance

Generation, registry, quarantine, and authority policies are declared only.
Future implementation must preserve:

- one coherent generation lifecycle;
- digest-bound human freeze;
- two-phase freeze;
- explicit recovery;
- no provisional Strategy use;
- no automatic freeze;
- no automatic canonical approval;
- profile/identity-segment/generation approval granularity;
- maximum one active approval per registry key;
- no newest-generation promotion;
- no manual file edit as approval;
- make-before-break supersession;
- quarantine until explicit human approval;
- immediate fail-closed per-key quarantine;
- reinstatement through a new approval record only;
- one bounded 10-second mutex wait;
- immutable event file per authority event;
- append-only authority journal;
- digest-chained head record;
- journal then head then pointer ordering;
- explicit recovery sentinels;
- deterministic authority audit ordering.

No provider execution, calendar generation, normalization, generation
transaction, registry authority transaction, mutex operation, authority journal
write, data download, annotation, candidate generation, Monte Carlo, outcome
evaluation, performance analysis, broker integration, or execution behavior is
implemented by v2.
