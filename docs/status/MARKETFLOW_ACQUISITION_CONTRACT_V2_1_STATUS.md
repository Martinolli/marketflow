# MarketFlow Acquisition Contract v2.1 Status

## Status

PASS.

Contract v2.1 fixes the missing source timestamp semantic while keeping
Contract v1 and Contract v2 unchanged.

## Initial State

- Branch: `feature/swing-acquisition-contract-v2-1`.
- Starting commit: `23b690f35d5e6bc8f4d439a6ded4c956f7f37005`.
- Initial working tree: clean.
- Pre-test Git status:
  untracked v2.1 source/config/test/docs only.
- Python: `3.12.10` using `env\Scripts\python.exe`.
- `pip check`: pass.

## Files Added

- `config/fixed_date_acquisition_contract_v2_1.toml`;
- `marketflow/research/acquisition_contract_v2_1.py`;
- `tests/test_acquisition_contract_v2_1.py`;
- `docs/plans/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_PLAN.md`;
- `docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_STATUS.md`;
- `docs/architecture/MARKETFLOW_SOURCE_BAR_TIMESTAMP_CONTRACT.md`;
- `docs/research/MARKETFLOW_TIMESTAMP_SEMANTICS_DECISION.md`.

## v1 And v2 Non-Regression

- Contract v1 digest:
  `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`.
- Contract v2 digest:
  `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`.

Contract v1 and Contract v2 source/config semantic content remains unchanged.

## v2.1 Contract

- Schema: `marketflow.acquisition_contract.v2.1`.
- Decision set: `marketflow.acquisition_decisions.v2.1`.
- Status: `ACQUISITION_CONTRACT_V2_1_READY_FOR_IMPLEMENTATION`.
- Base schema: `marketflow.acquisition_contract.v2`.
- Base v2 digest:
  `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`.
- v2.1 digest:
  `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`.

All execution gates remain false:

- `acquisition_enabled`;
- `provider_execution_enabled`;
- `calendar_generation_enabled`;
- `normalization_enabled`;
- `registry_authority_enabled`.

## Timestamp Policy

- Provider endpoint family: `STOCKS_CUSTOM_BARS_V2`.
- Provider timestamp field: `t`.
- Provider timestamp unit: `UNIX_EPOCH_MILLISECONDS`.
- Source timestamp semantic: `START_OF_AGGREGATE_WINDOW`.
- Source interval: `PT15M`.
- Interval boundary: `LEFT_CLOSED_RIGHT_OPEN`.
- Canonical start field: `window_start_utc`.
- Canonical end field: `window_end_utc`.
- Compatibility `timestamp_utc` semantic: `WINDOW_START`.
- Derived timestamp semantic: `WINDOW_END`.

## Slot Boundary Result

The documented ordinary-session source starts are:

- morning: `09:30` through `12:30`, 13 bars;
- afternoon: `12:45` through `15:45`, 13 bars;
- full RTH day: 26 bars.

No source bar beginning at `16:00` is an RTH source slot.

## DST Result

Focused tests verify:

- winter `09:30 America/New_York` converts to `14:30 UTC`;
- summer `09:30 America/New_York` converts to `13:30 UTC`;
- the interval duration remains exactly 15 minutes.

## Loader And CLI

The strict loader accepts only:

```text
config/fixed_date_acquisition_contract_v2_1.toml
```

It rejects v1/v2 files, unknown versions, unsafe paths, unknown fields,
credential-like fields, ticker-specific content, semantic drift, and enabled
acquisition gates.

The dry CLI:

```text
env\Scripts\python.exe -m marketflow.research.acquisition_contract_v2_1
```

validates v2.1, verifies the base v2 digest, computes the v2.1 digest, and
prints a sanitized receipt. It accepts no ticker/date/semantic/acquisition
override.

## Tests

Focused v2.1 suite:

```text
env\Scripts\python.exe -m pytest tests\test_acquisition_contract_v2_1.py -q
```

Result: 13 passed.

Full-suite and compile results are recorded in the final task response.

Focused v2.1, v1/v2 regression, and source-assurance suite:

```text
env\Scripts\python.exe -m pytest tests\test_acquisition_contract_v2_1.py tests\test_acquisition_contract_v2.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py -q
```

Result: 86 passed.

Collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 683 collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 683 passed.

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
?? config/fixed_date_acquisition_contract_v2_1.toml
?? docs/architecture/MARKETFLOW_SOURCE_BAR_TIMESTAMP_CONTRACT.md
?? docs/plans/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_PLAN.md
?? docs/research/MARKETFLOW_TIMESTAMP_SEMANTICS_DECISION.md
?? docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_1_STATUS.md
?? marketflow/research/acquisition_contract_v2_1.py
?? tests/test_acquisition_contract_v2_1.py
```

The test count increases from the accepted 670 baseline to 683 because this
task adds 13 focused v2.1 tests.

## Reviewer Findings

Reviewer A:

```text
No high finding. Endpoint binding, source timestamp semantic, slot boundaries,
DST behavior, and v1/v2 non-regression are covered by focused tests.
```

Reviewer B:

```text
No high finding. Strict loader, digest/version separation, dry CLI/no-network
isolation, docs, and previous-integrity constants are covered by focused and
source-level tests.
```

## Remaining Limitations

- Frozen-calendar engine remains unimplemented.
- RTH bar engine remains unimplemented.
- No provider call or data generation occurred.
- No real canonical calendar has been frozen.
- No provider executor exists.
- No canonical dataset exists.
- Runtime migration remains pending.
- Predictive usefulness and profitability remain unaccepted.

## Prohibited Actions

No commit or tag was created.

No dependency change, provider call, calendar generation, data download,
annotation, candidate generation, Monte Carlo, outcome evaluation, performance
analysis, broker integration, execution capability, source modification,
report rewrite, registry-authority operation, or runtime profile migration
occurred.
