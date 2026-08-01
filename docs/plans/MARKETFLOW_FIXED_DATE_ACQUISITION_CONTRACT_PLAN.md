# MarketFlow Fixed-Date Acquisition Contract Plan

## Status

Plan status: IMPLEMENTED FOR OFFLINE ACCEPTANCE.

Implementation status: COMPLETE.

Acquisition status: DISABLED.

This plan defines offline contract tooling only. It does not authorize provider
access, data download, annotation, Strategy candidate generation, Monte Carlo,
outcome evaluation, performance analysis, broker integration, or execution.

## Starting Boundary

- Branch: `feature/swing-fixed-date-acquisition-contract`.
- Base commit: `bf1187c27792a5903966bf3066f216ca923707cf`.
- Required interpreter: `env\Scripts\python.exe`.
- Accepted profile contracts remain:
  - `SWING`: candidate timeframe `4h`, minimum valid OHLCV rows `390`.
  - `POSITION_SWING`: candidate timeframe `1d`, minimum valid OHLCV rows `560`.
- Contract outcome must remain `ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS`
  until remaining required human approvals are supplied.

## Constraints

- No provider call.
- No network call.
- No credential or environment-value inspection.
- Provider entitlement is operator-attested confirmed for Massive.com
  `STOCKS_STARTER`, five years of history, fifteen-minute delayed data, and
  intraday/daily aggregates. This does not enable acquisition.
- No actual ticker, acquisition date, local path, or API endpoint URL in the
  source-controlled example.
- No dependency changes.
- No source data, historical report, or active virtual-environment mutation.
- No accepted Strategy, fixed-profile, lineage, remediation, or no-peek
  semantic change.

## Implementation Scope

Create an isolated offline contract module:

```text
marketflow/research/fixed_date_acquisition_contract.py
```

The module will provide:

- fixed enum/string contracts for provider identity, entitlement, profiles,
  bar construction, session policy, timezone policy, adjustment policy,
  pagination/completeness, artifact provenance, readiness status, and response
  validation;
- immutable dataclass contract models;
- strict dictionary/TOML loading with unknown-field rejection;
- explicit fixed `start_date` and `end_date` semantics with relative-period and
  current-date default rejection;
- profile validation for `SWING` and `POSITION_SWING`;
- deterministic canonical UTF-8 JSON serialization and SHA-256 digest;
- synthetic fake-response validation helpers only;
- sanitized readiness receipt generation;
- a no-network dry CLI that validates the fictional example and prints the
  sanitized receipt.

The module will not import provider clients, Strategy candidate builder,
outcome evaluator, Monte Carlo, Streamlit, LLM, sockets, or credentials.

## Documentation Scope

Create:

- `docs/status/MARKETFLOW_FIXED_DATE_ACQUISITION_CONTRACT_STATUS.md`;
- `docs/architecture/MARKETFLOW_HISTORICAL_DATA_ACQUISITION_CONTRACT.md`;
- `docs/research/MARKETFLOW_BAR_AND_SESSION_POLICY.md`;
- `config/fixed_date_acquisition_contract.example.toml`.

The status document will record the current acquisition inventory and why the
contract remains blocked.

## Test Scope

Add deterministic offline tests for:

- contract immutability, serialization, digest stability, and digest changes;
- strict loader unknown/missing-field rejection;
- fixed-date validation and relative-period rejection;
- exact profile mappings and row gates;
- unresolved 4h, daily, and session policies blocking execution;
- explicit adjustment policy and mismatch rejection;
- pagination/completeness fake sequences;
- fake response validation failures;
- provenance sanitization and raw/normalized digest relationship;
- dry CLI output and rejected operational flags;
- AST/source assurance proving no provider/network/candidate/outcome/Monte
  Carlo/credential path in the contract module;
- non-regression for accepted fixed-profile, Artifact Lineage v1, remediation,
  and source-identity boundaries.

## Review And Verification

Run two bounded read-only reviews after implementation:

- Reviewer A: provider inventory, date/session/bar construction, adjustment,
  timezone/DST, pagination/completeness, and response validation.
- Reviewer B: canonical serialization, provenance/lineage, entitlement
  blocker, dry CLI/no-network controls, tests/docs, and prior milestone
  preservation.

Required final checks:

```powershell
$python = (Resolve-Path ".\env\Scripts\python.exe").Path
& $python -m pip check
& $python -m pytest --collect-only -q
& $python -m pytest -q
& $python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
git diff --check
```

Final acceptance may create one local commit if every offline check passes. No
tag or push is authorized.
