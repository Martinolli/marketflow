# MarketFlow Acquisition Contract v2 Plan

## Status

Plan status: IMPLEMENTED AND LOCALLY VERIFIED.

Scope: declarative offline Contract v2 only.

Acquisition status: DISABLED.

No provider execution, calendar generation, bar aggregation, dataset
normalization, acquisition-generation transaction, registry approval
transaction, Windows mutex operation, authority journal write, data download,
annotation, Strategy candidate generation, Monte Carlo, outcome evaluation,
performance analysis, broker integration, or execution behavior is authorized.

## Starting Evidence

- Branch: `feature/swing-acquisition-contract-v2`.
- Starting commit: `42907ba5bc0a8e5c866a323bfef14efe7244e01e`.
- Baseline tag: `v0.1.0-alpha.13-fixed-date-acquisition-contract`.
- Working tree: clean before v2 work.
- Python: `3.12.10`.
- `pip check`: passed, `No broken requirements found.`
- Historical v1 dry digest:
  `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`.

## Implementation Scope

Create:

- `marketflow/research/acquisition_contract_v2.py`;
- `config/fixed_date_acquisition_contract_v2.toml`;
- `docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_STATUS.md`;
- `docs/architecture/MARKETFLOW_ACQUISITION_CONTRACT_V2.md`;
- `docs/research/MARKETFLOW_ACQUISITION_DECISIONS_V2.md`;
- focused deterministic Contract v2 tests.

The v2 module will define immutable submodels, fixed enum/string constants,
strict TOML loading, deterministic canonical JSON, SHA-256 digesting, sanitized
readiness receipts, and a no-network dry CLI.

## Decisions To Encode

Contract v2 encodes approved human semantic decisions for:

- fixed common date range `2022-01-01` through `2025-12-31`;
- Massive.com / legacy Polygon operator-attested entitlement;
- 15-minute split-adjusted source bars;
- RTH-only derived datasets with extended hours excluded;
- SWING half-session 195-minute canonical bars;
- POSITION_SWING full-session 1-day canonical bars;
- exchange-aware frozen calendar artifact architecture;
- point-in-time instrument identity evidence;
- split and dividend audit policy;
- monthly chunking, raw page retention, retry, and Decimal equivalence;
- normalized core/audit artifact separation;
- coherent generation, registry, quarantine, authority, and audit governance.

## Explicit Non-Implementation

Contract v2 readiness means:

- human semantic decisions: COMPLETE;
- declarative contract implementation: targeted by this task;
- provider executor: NOT IMPLEMENTED;
- calendar artifact generator: NOT IMPLEMENTED;
- normalization engine: NOT IMPLEMENTED;
- generation governance engine: NOT IMPLEMENTED;
- registry authority engine: NOT IMPLEMENTED;
- canonical data: NOT AVAILABLE;
- research protocol: BLOCKED;
- predictive usefulness/profitability: NOT ACCEPTED.

## Verification Result

Required checks used only `env\Scripts\python.exe`:

```powershell
$python = (Resolve-Path ".\env\Scripts\python.exe").Path
& $python -m pip check
& $python -m pytest --collect-only -q
& $python -m pytest -q
& $python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
git diff --check
```

Results:

- `pip check`: passed.
- `pytest --collect-only -q`: 670 tests collected.
- `pytest -q`: 670 passed.
- `compileall -W error`: passed.
- `git diff --check`: passed.
- Final v2 digest after acceptance corrections:
  `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`.

Focused tests cover v1/v2 separation, fixed decisions, loader/path
safety, serialization/digest determinism, dry CLI behavior, source assurance,
and prior-integrity non-regression.

No commit or tag will be created in this task.
