# MarketFlow Acquisition Contract v2 Acceptance

## Decision

CONTRACT V2 DECLARATIVE TOOLING: PASS.

PROVIDER EXECUTOR: NOT IMPLEMENTED.

CALENDAR / BAR ENGINE: NOT IMPLEMENTED.

DATA ACQUISITION: DISABLED.

CANONICAL DATA: NOT AVAILABLE.

UTC acceptance date: `2026-08-01T13:38:03Z`.

Branch: `feature/swing-acquisition-contract-v2`.

Base commit: `42907ba5bc0a8e5c866a323bfef14efe7244e01e`.

Baseline tag: `v0.1.0-alpha.13-fixed-date-acquisition-contract`.

No tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- strict source-controlled Contract v2 TOML;
- immutable declarative v2 contract model;
- strict single-config loader;
- deterministic canonical JSON and SHA-256 digest;
- sanitized dry CLI receipt;
- focused offline tests;
- documentation of the accepted acquisition design.

Excluded scope:

- provider executor;
- provider account, billing, portal, API-key, credential, or browser review;
- dependency installation or upgrade;
- calendar package installation;
- calendar generation;
- bar-builder engine;
- data acquisition;
- normalization;
- annotation;
- Strategy candidate generation;
- Monte Carlo;
- outcome evaluation;
- performance analysis;
- broker integration;
- execution capability;
- registry authority transaction;
- mutex or authority journal operation.

## v1 Non-Regression

The historical v1 contract remains available and unchanged as accepted blocked
evidence.

Accepted v1 digest:

`29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`

Confirmed:

- v1 schema remains available;
- v1 loader behavior remains unchanged;
- v1 acquisition remains disabled;
- v1 dry CLI reports `ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS`;
- v1 cannot load v2;
- v2 cannot load v1;
- no v1 source, config, or test file was edited for v2.

## v2 Schema And Digest

Contract schema version:

`marketflow.acquisition_contract.v2`

Decision set version:

`marketflow.acquisition_decisions.v2`

Contract status:

`ACQUISITION_CONTRACT_V2_READY_FOR_IMPLEMENTATION`

Human decisions status:

`COMPLETE`

Final v2 digest:

`59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`

The digest differs from the earlier reported
`59a5c18ece652583673e216dd6e2c837ba827fe3305188979c396d57d7468515`
because final acceptance corrections made retry classes, profile contract
identifiers, timestamp semantics, runtime migration status, and governance
declarations explicit in the semantic contract.

All implementation and execution gates remain false:

- `acquisition_enabled`;
- `provider_execution_enabled`;
- `calendar_generation_enabled`;
- `normalization_enabled`;
- `registry_authority_enabled`.

## Provider And Entitlement

Provider business identity: `MASSIVE.COM`.

Former brand: `POLYGON.IO`.

Legacy adapter/package: `polygon-api-client` version `1.14.6`.

Provider entitlement is operator-attested, not API-verified:

- subscription: `STOCKS_STARTER`;
- evidence: `OPERATOR_ATTESTED`;
- status: `OPERATOR_ATTESTED_CONFIRMED`;
- historical access: `FIVE_YEARS`;
- data recency: `FIFTEEN_MINUTE_DELAYED`;
- aggregate access: `INTRADAY_AND_DAILY_AVAILABLE`.

No provider account, billing, portal, API-key, credential, account data, trade
data, or browser data was inspected.

## Fixed Range

Fixed common range:

- start date: `2022-01-01`;
- end date: `2025-12-31`;
- inclusive range: true;
- common for all profiles: true.

The contract prohibits rolling windows, relative periods, current-date
dependency, ticker-specific ranges, profile-specific ranges, automatic
extension, and CLI/environment overrides.

## Technical Constants

Registry mutex wait:

- `registry_mutex_wait_seconds = 10`;
- one monotonic bounded wait;
- no indefinite wait;
- no busy loop;
- no repeated automatic retry;
- no CLI or environment override.

Provider retry:

- maximum attempts: 3;
- retry backoff seconds: `[2, 5]`;
- jitter: false.

Retryable classes:

- `TRANSPORT_TIMEOUT`;
- `CONNECTION_RESET`;
- `HTTP_408`;
- `HTTP_429`;
- `HTTP_500`;
- `HTTP_502`;
- `HTTP_503`;
- `HTTP_504`.

Nonretryable classes include authentication, authorization, invalid request,
unsupported ticker, schema failure, semantic mismatch, adjustment mismatch,
invalid timestamps/OHLCV, and provider-response variance.

Retry-After:

- only HTTP 429 or 503;
- strict integer seconds;
- range 0 through 60;
- effective wait is max(configured backoff, Retry-After);
- malformed, negative, or greater than 60 blocks retry.

## Calendar Pin

Calendar package declaration:

- package: `exchange_calendars`;
- pinned version: `4.13.2`.

Local readiness metadata:

- installed: false;
- installed version: `NOT_INSTALLED`;
- pin matches installed: false.

The calendar pin is declarative only. The dependency was not installed by this
task. Package absence cannot activate a fallback. Package version is not treated
as the frozen calendar artifact itself. Future frozen calendar acceptance must
retain package, tzdata, calendar implementation, official exchange evidence,
and schedule digest.

## Profile Contracts

Base source bars:

- source interval: `15m`;
- multiplier: 15;
- timespan: `minute`;
- adjusted: true;
- sort: `asc`;
- limit: 50000;
- source timezone: `America/New_York`;
- canonical timezone: `UTC`;
- extended hours in derived data: excluded.

`SWING`:

- profile contract version: `SWING_RTH_HALF_SESSION_V1`;
- canonical bar type: `RTH_HALF_SESSION_195M`;
- minimum valid rows: 390;
- source bars per half-session bar: 13;
- segment 1: `09:30` to `12:45`;
- segment 2: `12:45` to `16:00`;
- timestamp semantic: `BAR_CLOSE_TIMESTAMP`;
- early-close session: excluded;
- higher-timeframe context: `NOT_IMPLEMENTED`.

`POSITION_SWING`:

- profile contract version: `POSITION_SWING_RTH_FULL_SESSION_V1`;
- canonical bar type: `RTH_FULL_SESSION_1D`;
- minimum valid rows: 560;
- source bars per canonical bar: 26;
- segment: `09:30` to `16:00`;
- timestamp semantic: `SESSION_CLOSE_TIMESTAMP`;
- early-close session: excluded;
- higher-timeframe context: `NOT_IMPLEMENTED`.

No provider-native 4h or provider-native 1d source is canonical under v2.

Current runtime migration remains explicitly:

`LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION`

The current normal CLI is not silently migrated.

## Identity And Calendar Policy

Calendar policy:

- exchange-aware frozen calendar artifact;
- requested listing MIC retained separately from resolved calendar;
- missing bars cannot infer closure;
- dynamic unfrozen calendar use is prohibited;
- early closes are excluded;
- timezone-aware UTC schedule evidence is required.

Instrument identity:

- Massive point-in-time Ticker Overview;
- start and end identity snapshots required;
- primary exchange MIC retained;
- Composite FIGI and Share Class FIGI where available;
- ticker-event audit is supporting evidence, not sole authority;
- identity changes create immutable segments;
- no automatic stitching.

## Corporate Actions

Split policy:

- provider split-adjusted bars;
- explicit `adjusted=true`;
- response must match true;
- independent split-event audit;
- no second local split adjustment.

Dividend policy:

- no dividend price adjustment;
- dividend-event audit required;
- ex-dividend continuity reset;
- no cross-boundary True Range;
- no cross-boundary Wyckoff structure;
- component-based post-boundary readiness;
- no arbitrary global warm-up;
- no manual unlock.

## Chunking, Raw Evidence, And Retries

Chunking:

- 48 fixed calendar-month chunks before identity clipping;
- clipped first and last segment months permitted;
- pagination exhausted whenever continuation exists;
- no partial-month success;
- no duplicate page or repeated continuation;
- no first-page-only acceptance.

Raw evidence:

- one immutable raw artifact per provider page;
- exact provider bytes required;
- one explicit month-completeness manifest;
- reformatted JSON is not raw;
- credential-bearing continuation retention is prohibited.

Attempts:

- every attempt immutable;
- failed attempts retained;
- one explicitly accepted attempt per logical page;
- no latest-response preference.

Multiple valid responses:

- semantic equivalence required;
- equivalent retries choose lowest valid attempt ordinal;
- differing projections produce `PROVIDER_RESPONSE_VARIANCE`;
- no automatic acceptance.

## Decimal And Semantic Projection

Semantic retry projection:

`OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1`

Numeric equality:

`STRICT_CANONICAL_DECIMAL_VALUE_EQUALITY`

Confirmed:

- no Python float equivalence;
- no epsilon;
- no display rounding;
- negative zero canonicalized;
- NaN and Infinity rejected;
- timestamps and counts exact integers.

Required row fields:

- timestamp;
- OHLCV.

Optional presence-sensitive fields:

- VWAP;
- transaction count.

Missing supplemental values are never fabricated, zero-filled, or
forward-filled.

## Normalization And Consolidation

Contract v2 declares paired monthly artifacts:

- monthly normalized OHLCV;
- monthly normalized aggregate audit fields.

The paired artifacts require identical row count and timestamp ordering.
Monthly normalization happens first. Explicit ordered identity-segment
consolidation happens later. Segment OHLCV and audit artifacts remain separate.
Dynamic Strategy scanning of monthly files is prohibited. One coherent
acquisition generation per identity segment is required. Mixed adjustment or
evidence generations are prohibited.

## Generation Governance

Declared generation statuses:

- `OPEN`;
- `INCOMPLETE`;
- `BLOCKED`;
- `READY_FOR_FREEZE`;
- `PREPARED`;
- `FROZEN`.

The contract requires explicit digest-bound operator freeze, two-phase freeze,
explicit recovery, and no provisional Strategy use. Automatic freeze and
automatic canonical approval are prohibited.

## Registry Governance

Canonical registry governance is declared for profile and identity segment
generations. It requires explicit digest-bound approval, two-phase approval,
maximum one active approval per key, make-before-break supersession, and
explicit recoveries. Newest generation promotion and manual file edit as
approval are prohibited.

## Quarantine, Authority, And Audit Governance

Quarantine:

- immediate fail-closed per-key quarantine;
- persistent pre-gate pending/active latches;
- immutable evidence;
- abort unfinished runs;
- validation epochs;
- per-key named mutex;
- reviewed clearance/suspension;
- reinstatement through a new approval record only;
- no old-run revival.

Authority storage:

- immutable event file per event;
- immutable head snapshot per generation;
- atomic `current-head.ref`;
- journal to head to pointer ordering;
- explicit head/pointer recovery;
- external two-phase recovery records;
- recovery sentinels;
- no startup auto-repair.

Authority audit:

- requested-key validation for normal use;
- explicit full audit command required;
- one key mutex at a time;
- non-atomic multi-key observations;
- start/end key-set reconciliation;
- immutable audit evidence;
- no authority-changing effect.

These policies are declared but not implemented in this task.

## Loader And Path Boundary

The v2 loader accepts only the approved direct repo config:

`config/fixed_date_acquisition_contract_v2.toml`

It rejects external absolute paths, traversal, nested config paths, arbitrary
URLs, environment-expanded paths, device/ADS-style references, symlink escape
where testable, unknown fields, missing fields, credential-like fields,
ticker-specific fields, altered dates, altered timeframes, weakened row floors,
altered technical constants, altered session/adjustment/stitching/freeze/
registry/authority policy, and `acquisition_enabled=true`.

Boolean fields require real booleans; strings or integers do not coerce into
booleans.

## Canonical Serialization And Dry CLI

Serialization uses deterministic UTF-8 canonical JSON with recursively sorted
keys, stable separators, exact integers and dates, no binary floats, and no
digest hardcoding in production source. Insertion order is irrelevant, and one
semantic field change changes the digest.

Dry CLI:

```powershell
env\Scripts\python.exe -m marketflow.research.acquisition_contract_v2
```

The CLI loads and validates v2, calculates the digest, reports calendar package
installation status as metadata, prints a sanitized receipt, exits zero for a
valid non-executable contract, and accepts no ticker/date/API-key/semantic
override.

Exit zero means:

`CONTRACT V2 STRUCTURALLY VALID AND READY FOR IMPLEMENTATION`

It does not mean acquisition ready.

The CLI reads no environment credential, opens no socket, calls no provider,
creates no calendar, dataset, registry state, sentinel, candidate, Monte Carlo,
or outcome, and does not freeze or authorize acquisition.

## Verification Evidence

Focused v2 tests:

`18 passed`

Focused v2, v1-regression, and source-assurance suite:

`73 passed`

Final checks after independent reviews:

- `env\Scripts\python.exe -m pip check`: passed,
  `No broken requirements found.`;
- `env\Scripts\python.exe -m pytest tests\test_acquisition_contract_v2.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py -q`:
  73 passed;
- `env\Scripts\python.exe -m pytest --collect-only -q`: 670 tests collected;
- `env\Scripts\python.exe -m pytest -q`: 670 passed;
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`:
  passed;
- `git diff --check`: passed.

Test count explanation:

- accepted starting baseline: 652 tests;
- final collection: 670 tests;
- increase: 18 focused Contract v2 tests.

The added tests cover v2 loading, fixed provider/date/profile/session/calendar/
identity/corporate-action/retry/chunking/Decimal/normalization/governance
policy, strict path loading, v1/v2 separation, dry CLI behavior, source
assurance, and prior-integrity non-regression.

Pre-test Git status:

```text
?? config/fixed_date_acquisition_contract_v2.toml
?? docs/architecture/MARKETFLOW_ACQUISITION_CONTRACT_V2.md
?? docs/plans/MARKETFLOW_ACQUISITION_CONTRACT_V2_PLAN.md
?? docs/research/MARKETFLOW_ACQUISITION_DECISIONS_V2.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_ACCEPTANCE.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_STATUS.md
?? marketflow/research/acquisition_contract_v2.py
?? tests/test_acquisition_contract_v2.py
```

Post-test Git status:

```text
?? config/fixed_date_acquisition_contract_v2.toml
?? docs/architecture/MARKETFLOW_ACQUISITION_CONTRACT_V2.md
?? docs/plans/MARKETFLOW_ACQUISITION_CONTRACT_V2_PLAN.md
?? docs/research/MARKETFLOW_ACQUISITION_DECISIONS_V2.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_ACCEPTANCE.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_STATUS.md
?? marketflow/research/acquisition_contract_v2.py
?? tests/test_acquisition_contract_v2.py
```

No tracked file was modified by tests.

## Warning Result

The isolated v2 path imports no provider client and does not import
`exchange_calendars` at module import. No broad warning suppression was
introduced. Provider/websocket warnings may be absent because those modules are
not imported by the isolated v2 path.

## No-Network And No-Execution Evidence

No provider call, network call, calendar generation, data download, dataset
write, annotation, candidate generation, Monte Carlo, outcome evaluation,
performance analysis, broker integration, execution path, registry-authority
operation, sentinel creation, report rewrite, dependency installation, or venv
modification was performed by this acceptance work.

## Reviewer Findings

Reviewer A: no findings. The reviewer independently checked provider identity,
fixed dates, profiles, sessions, calendar, identity, corporate actions,
chunking/retry/raw evidence, Decimal semantics, normalization, technical
constants, and v1/v2 separation, and recomputed the v2 digest.

Reviewer B: one Medium documentation finding. The initial acceptance document
did not yet record final pip, collect-only, full-suite, compileall, diff, and
pre/post Git status evidence and still marked reviews pending. Disposition:
fixed in this document after the final rerun. Reviewer B found no source,
config, or test issue.

No critical or high reviewer finding remains.

## Remaining Limitations

- Acquisition executor does not exist.
- Frozen calendar does not exist.
- Bar-builder engine does not exist.
- Calendar dependency is not installed by this phase.
- Acquisition remains disabled.
- Canonical datasets do not exist.
- Current fixed-profile runtime migration remains pending.
- Research protocol remains blocked.
- Predictive usefulness and profitability remain unaccepted.

## Next Implementation Phase

The next phase is a separate implementation proposal for the frozen calendar
artifact and 15-minute-to-profile bar builder. That phase must remain offline by
default, preserve this contract digest boundary, and require separate
acceptance before any acquisition executor or canonical data approval is
introduced.
