# MarketFlow Acquisition Contract v2 Status

## Current Status

Status: IMPLEMENTED LOCALLY AS DECLARATIVE OFFLINE CONTRACT.

Contract status:

`ACQUISITION_CONTRACT_V2_READY_FOR_IMPLEMENTATION`

Human decisions status:

`COMPLETE`

Acquisition status:

`DISABLED`

No commit or tag was created for this task.

## Starting Baseline

- Branch: `feature/swing-acquisition-contract-v2`.
- Starting commit: `42907ba5bc0a8e5c866a323bfef14efe7244e01e`.
- Baseline tag: `v0.1.0-alpha.13-fixed-date-acquisition-contract`.
- Initial working tree: clean.
- Python: `3.12.10`.
- Initial `pip check`: passed.
- Historical v1 digest:
  `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`.

## Local v2 Receipt

Observed from:

```powershell
env\Scripts\python.exe -m marketflow.research.acquisition_contract_v2
```

Contract digest:

`59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`

The digest changed from the earlier reported
`59a5c18ece652583673e216dd6e2c837ba827fe3305188979c396d57d7468515` after
final acceptance corrections made retry classes, profile contract identifiers,
timestamp semantics, runtime migration status, and governance declarations
explicit in the semantic contract.

Receipt evidence:

- acquisition enabled: false;
- provider execution enabled: false;
- calendar generation enabled: false;
- normalization enabled: false;
- registry authority enabled: false;
- provider business identity: `MASSIVE.COM`;
- former brand: `POLYGON.IO`;
- provider entitlement status: `OPERATOR_ATTESTED_CONFIRMED`;
- fixed start date: `2022-01-01`;
- fixed end date: `2025-12-31`;
- source interval: `15m`;
- source timezone: `America/New_York`;
- canonical storage timezone: `UTC`;
- runtime profile migration status:
  `LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION`;
- SWING profile contract version: `SWING_RTH_HALF_SESSION_V1`;
- SWING canonical bar type: `RTH_HALF_SESSION_195M`;
- SWING source bars per canonical bar: `13`;
- SWING timestamp semantic: `BAR_CLOSE_TIMESTAMP`;
- POSITION_SWING profile contract version:
  `POSITION_SWING_RTH_FULL_SESSION_V1`;
- POSITION_SWING canonical bar type: `RTH_FULL_SESSION_1D`;
- POSITION_SWING source bars per canonical bar: `26`.
- POSITION_SWING timestamp semantic: `SESSION_CLOSE_TIMESTAMP`.

Calendar package receipt:

- package: `exchange_calendars`;
- contract pin: `4.13.2`;
- locally installed: false;
- installed version: `NOT_INSTALLED`;
- pin matches installed: false.

This is not a failure of Contract v2 because the task did not authorize calendar
package installation, calendar import, or calendar artifact generation.

## Implemented Files

- `config/fixed_date_acquisition_contract_v2.toml`;
- `marketflow/research/acquisition_contract_v2.py`;
- `tests/test_acquisition_contract_v2.py`;
- `docs/plans/MARKETFLOW_ACQUISITION_CONTRACT_V2_PLAN.md`;
- `docs/architecture/MARKETFLOW_ACQUISITION_CONTRACT_V2.md`;
- `docs/research/MARKETFLOW_ACQUISITION_DECISIONS_V2.md`;
- `docs/status/MARKETFLOW_ACQUISITION_CONTRACT_V2_STATUS.md`.

## Scope Assurance

Implemented:

- immutable v2 contract models;
- strict source-controlled TOML loader;
- fixed provider entitlement declaration;
- fixed date range;
- fixed source/session/bar/corporate-action/calendar/completeness policies;
- deterministic canonical JSON and SHA-256 digest;
- sanitized offline readiness receipt;
- dry CLI with no operational arguments;
- focused offline tests.

Not implemented:

- provider execution;
- provider account or credential inspection;
- data downloads;
- calendar generation;
- bar aggregation;
- normalization;
- generation transactions;
- registry transactions;
- mutex operations;
- authority journal writes;
- annotation;
- candidate generation;
- Monte Carlo;
- outcome evaluation;
- performance acceptance;
- broker or execution behavior.

## Focused Test Evidence

Focused v2 test command:

```powershell
env\Scripts\python.exe -m pytest tests\test_acquisition_contract_v2.py -q
```

Result:

`18 passed`

Coverage includes:

- v2 loader and readiness receipt;
- Massive.com business identity with explicit legacy Polygon adapter naming;
- fixed date range and relative-date rejection;
- 15-minute source bar policy;
- SWING and POSITION_SWING profile bar policy;
- aggregation, calendar, identity, and corporate-action policy;
- retry and Retry-After policy;
- chunking, semantic equivalence, normalization, generation, registry,
  quarantine, authority storage, and authority audit policy;
- strict Decimal canonicalization;
- deterministic serialization and digest sensitivity;
- loader rejection of unsafe fields and operational enablement;
- direct repo `config/*.toml` loader boundary;
- v1 loader rejection and v1 digest regression;
- dry CLI no-operational-argument behavior;
- source assurance against provider/network/candidate/outcome imports.

## Final Acceptance Checks

Final local acceptance checks completed:

- `env\Scripts\python.exe -m pip check`: passed,
  `No broken requirements found.`;
- `env\Scripts\python.exe -m pytest --collect-only -q`: 670 tests collected;
- `env\Scripts\python.exe -m pytest -q`: 670 passed;
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`:
  passed;
- `git diff --check`: passed.

Git status before and after the full suite showed only the intended untracked v2
source/config/doc/test files.

## Independent Read-Only Reviews

Two bounded read-only subagent reviews were completed. Both reported no
findings.

Review focus:

- source/config policy correctness and scope safety;
- no acquisition enablement;
- no provider execution imports;
- no credential or environment inspection;
- strict TOML loading;
- v1 separation;
- Massive.com business identity with legacy Polygon adapter naming only where
  appropriate;
- docs and digest evidence consistency.
