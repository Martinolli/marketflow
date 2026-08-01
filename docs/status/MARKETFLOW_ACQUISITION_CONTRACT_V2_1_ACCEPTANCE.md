# MarketFlow Acquisition Contract v2.1 Acceptance

## Decision

CONTRACT V2.1 DECLARATIVE TOOLING: PASS.

PROVIDER EXECUTOR: NOT IMPLEMENTED.

FROZEN CALENDAR ENGINE: NOT IMPLEMENTED.

RTH BAR ENGINE: NOT IMPLEMENTED.

DATA ACQUISITION: DISABLED.

CANONICAL DATA: NOT AVAILABLE.

UTC acceptance date: `2026-08-01T15:02:15Z`.

Branch: `feature/swing-acquisition-contract-v2-1`.

Base commit: `23b690f35d5e6bc8f4d439a6ded4c956f7f37005`.

No tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- strict source-controlled Contract v2.1 TOML;
- immutable declarative v2.1 contract model;
- strict single-config loader;
- endpoint-specific source timestamp policy;
- deterministic canonical JSON and SHA-256 digest;
- sanitized dry CLI receipt;
- focused offline tests;
- documentation of the timestamp-semantics correction.

Excluded scope:

- provider executor;
- provider account, billing, portal, API-key, credential, or browser review;
- dependency installation or upgrade;
- calendar generation;
- frozen-calendar engine;
- RTH bar engine;
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
- runtime profile migration.

## v1 Non-Regression

Contract v1 remains unchanged historical evidence.

Accepted v1 digest:

```text
29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
```

Confirmed:

- v1 schema remains available;
- v1 loader behavior remains unchanged;
- v1 acquisition remains disabled;
- v1 digest remains exact;
- v1 cannot load v2.1 through the v2.1 loader boundary;
- v1 files were not edited for v2.1.

## v2 Non-Regression

Contract v2 remains unchanged historical evidence.

Accepted v2 digest:

```text
59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
```

Confirmed:

- v2 schema remains available;
- v2 loader behavior remains unchanged;
- v2 acquisition remains disabled;
- v2 digest remains exact;
- v2 cannot load v2.1;
- v2.1 cannot load v2;
- v2 files were not edited for v2.1.

## v2.1 Schema And Digest

Contract schema version:

```text
marketflow.acquisition_contract.v2.1
```

Decision set version:

```text
marketflow.acquisition_decisions.v2.1
```

Contract status:

```text
ACQUISITION_CONTRACT_V2_1_READY_FOR_IMPLEMENTATION
```

Base contract schema:

```text
marketflow.acquisition_contract.v2
```

Base contract digest:

```text
59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
```

Final v2.1 digest:

```text
538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
```

All execution gates remain false:

- `acquisition_enabled`;
- `provider_execution_enabled`;
- `calendar_generation_enabled`;
- `normalization_enabled`;
- `registry_authority_enabled`.

## Endpoint Binding

The timestamp policy is bound only to:

```text
STOCKS_CUSTOM_BARS_V2
```

It does not apply to grouped daily summaries, previous-day endpoints,
WebSocket aggregates, another provider endpoint, or another provider family.
Another endpoint requires a new endpoint-specific timestamp contract.

## Source Timestamp Semantic

Contract v2.1 fixes the missing source timestamp semantic from Contract v2.

Exact policy:

```text
provider_timestamp_field = t
provider_timestamp_unit = UNIX_EPOCH_MILLISECONDS
provider_timestamp_semantic = START_OF_AGGREGATE_WINDOW
source_interval_minutes = 15
source_interval_duration = PT15M
interval_boundary = LEFT_CLOSED_RIGHT_OPEN
canonical_start_field = window_start_utc
canonical_end_field = window_end_utc
canonical_storage_timezone = UTC
session_mapping_timezone = America/New_York
derived_bar_timestamp_semantic = WINDOW_END
exact_slot_alignment_required = true
timestamp_snapping_enabled = false
timestamp_tolerance_enabled = false
```

Compatibility field `timestamp_utc`, where retained, means `WINDOW_START`.

## Normalized Source Interval

The future normalized source-bar representation is:

```text
window_start_utc
window_end_utc
open
high
low
close
volume
```

The source interval is:

```text
[window_start_utc, window_end_utc)
```

with `window_end_utc` exactly 15 minutes after `window_start_utc`.

The helper converts provider epoch milliseconds with integer arithmetic. No
binary-float timestamp arithmetic, naive timestamp, local-machine timezone,
rounding, snapping, tolerance, or caller-selected timestamp semantic is used.

## Slot Boundaries

Ordinary-session source starts:

- morning: `09:30` through `12:30`, count 13;
- afternoon: `12:45` through `15:45`, count 13;
- daily: count 26.

Confirmed:

- `[09:30,09:45)` is the first RTH source interval;
- `[12:30,12:45)` is the final morning interval;
- `[12:45,13:00)` is the first afternoon interval;
- `[15:45,16:00)` is the final RTH interval;
- a source interval beginning at `16:00` is outside RTH;
- no source interval is assigned to both derived bars;
- there is no gap between morning and afternoon windows.

## Timezone And DST

Focused tests verify:

- winter `09:30 America/New_York` converts to `14:30 UTC`;
- summer `09:30 America/New_York` converts to `13:30 UTC`;
- the source interval remains exactly 15 minutes.

DST changes UTC offset, not local session anchors. No naive local datetime is
stored as authoritative.

## Derived Timestamps

Derived MarketFlow bars remain close-stamped:

- `SWING` morning timestamp: `12:45 America/New_York` converted to UTC;
- `SWING` afternoon timestamp: `16:00 America/New_York` converted to UTC;
- `POSITION_SWING` timestamp: `16:00 America/New_York` converted to UTC.

Rejected by contract/tests:

- source bars treated as close-stamped;
- derived bars treated as start-stamped;
- provider-native 4h or daily substitution.

## Loader And Path Safety

The strict loader accepts only:

```text
config/fixed_date_acquisition_contract_v2_1.toml
```

It rejects:

- v1 or v2 configs;
- external absolute paths;
- traversal;
- nested config paths;
- ADS-style paths;
- symlink escape where testable;
- environment-expanded paths;
- URL-like paths;
- unknown or missing fields;
- credential-like fields;
- ticker-specific content;
- semantic overrides;
- duration overrides;
- snapping or tolerance enablement;
- `acquisition_enabled=true`;
- non-boolean acquisition gates.

## Dry CLI

Command:

```text
env\Scripts\python.exe -m marketflow.research.acquisition_contract_v2_1
```

The dry CLI validates v2.1, verifies the base v2 digest, calculates the v2.1
digest, prints a sanitized receipt, and keeps every acquisition/execution gate
false.

Exit zero means:

```text
CONTRACT V2.1 STRUCTURALLY VALID AND READY FOR BAR-ENGINE IMPLEMENTATION
```

It does not mean acquisition is authorized.

## No-Network And No-Execution Evidence

Source-level checks confirm the v2.1 module has no provider import, no
frozen-calendar engine import, no candidate/Monte Carlo/outcome import, no
Streamlit or LLM import, no environment read, no socket path, no timestamp
snapping or tolerance path, and no provider-native 4h/daily canonical path.

No provider call, calendar generation, data download, annotation, candidate
generation, Monte Carlo, outcome evaluation, performance analysis, broker
integration, execution capability, source modification, report rewrite,
registry-authority operation, or runtime profile migration occurred.

## Audit Finding And Correction

Reviewer finding:

```text
MEDIUM - source_window_from_epoch_ms used division by 1000, introducing
binary-float timestamp arithmetic despite the v2.1 integer epoch-millisecond
contract.
```

Disposition: fixed.

Correction:

- replaced float division with integer `divmod(epoch_milliseconds, 1000)`;
- added source-level regression coverage requiring integer conversion;
- v2.1 semantic digest remained unchanged because the TOML contract did not
  change.

## Tests

Focused v2.1 suite:

```text
env\Scripts\python.exe -m pytest tests\test_acquisition_contract_v2_1.py -q
```

Result: 13 passed.

Focused v2.1, v1/v2 regression, and source-assurance suite:

```text
env\Scripts\python.exe -m pytest tests\test_acquisition_contract_v2_1.py tests\test_acquisition_contract_v2.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py -q
```

Result: 86 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 683 collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 683 passed.

The test count increases from the accepted 670 baseline to 683 because v2.1
adds 13 focused tests.

## Pip, Compile, And Diff Checks

`pip check`: pass.

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass.

`git diff --cached --check`: pass before commit.

## Warning Review

No broad warning suppression was introduced. No project-owned warning was
hidden. The absence of warning output in the focused and full checks is from
the executed test/import paths, not global suppression.

## Git Status Evidence

Pre-test Git status:

```text
?? config/fixed_date_acquisition_contract_v2_1.toml
?? docs/architecture/MARKETFLOW_SOURCE_BAR_TIMESTAMP_CONTRACT.md
?? docs/plans/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_PLAN.md
?? docs/research/MARKETFLOW_TIMESTAMP_SEMANTICS_DECISION.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_STATUS.md
?? marketflow/research/acquisition_contract_v2_1.py
?? tests/test_acquisition_contract_v2_1.py
```

Post-test Git status before commit:

```text
?? config/fixed_date_acquisition_contract_v2_1.toml
?? docs/architecture/MARKETFLOW_SOURCE_BAR_TIMESTAMP_CONTRACT.md
?? docs/plans/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_PLAN.md
?? docs/research/MARKETFLOW_TIMESTAMP_SEMANTICS_DECISION.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_ACCEPTANCE.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_STATUS.md
?? marketflow/research/acquisition_contract_v2_1.py
?? tests/test_acquisition_contract_v2_1.py
```

No tracked file was modified by tests.

## Reviewer Findings

Reviewer A:

```text
Medium integer timestamp arithmetic finding fixed. Endpoint binding, source
timestamp semantics, interval/slot boundaries, DST, derived timestamps, and
v1/v2 non-regression have no remaining high finding.
```

Reviewer B:

```text
No high finding. Strict loader/path boundary, canonical digest, dry
CLI/no-network behavior, source assurance, tests/docs, and prior-integrity
preservation are covered.
```

## Remaining Limitations

- Calendar and bar engine are still not implemented.
- Acquisition remains disabled.
- No canonical datasets exist.
- No provider executor exists.
- No real canonical calendar has been frozen.
- Normal runtime migration remains pending.
- Research protocol remains blocked until later implementation evidence.
- Predictive usefulness and profitability remain unaccepted.

## Next Implementation Phase

The next phase may implement the offline frozen-calendar and deterministic RTH
bar engine against accepted Contract v2.1. That future phase must remain
offline unless separately authorized and must not infer timestamp semantics
outside this endpoint-specific contract.
