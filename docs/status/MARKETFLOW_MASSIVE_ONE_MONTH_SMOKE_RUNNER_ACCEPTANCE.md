# MarketFlow Massive One-Month Smoke Runner Acceptance

## Decision

PASS.

Accepted classification:

```text
MASSIVE_ONE_MONTH_SMOKE_RUNNER_OFFLINE_ACCEPTED_NOT_EXECUTED
```

UTC acceptance date: `2026-08-01T23:10:09Z`.

Branch: `feature/swing-massive-one-month-smoke-runner`.

Base commit: `f10b4f4dda98b6494276e3fba9396a7a7fba84ea`.

Baseline tag at base commit:

```text
v0.1.0-alpha.19-massive-rest-transport-offline
```

No Git tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- immutable controlled Massive.com one-month smoke specification;
- offline smoke plan command;
- interactive-only live smoke boundary;
- digest-bound authorization ceremony;
- hidden `getpass` credential boundary after authorization;
- isolated ignored runtime root for future live smoke artifacts;
- noncanonical smoke artifact and receipt contract;
- bounded monthly-executor integration for smoke provenance and truthful
  provider-execution evidence;
- focused smoke tests, source-assurance strengthening, and documentation.

Excluded scope:

- live Massive.com smoke execution;
- actual API-key inspection or use;
- provider account, portal, billing, browser, trade, or credential-store
  access;
- external network, DNS, socket, or data download;
- calendar freeze;
- derived SWING/POSITION bars;
- annotations, Strategy, Wyckoff, Monte Carlo, outcome, performance, broker,
  execution, report rewrite, registry authority, or normal runtime migration.

## Smoke Specification

Schema:

```text
marketflow.massive_provider_smoke.v1
```

Fixed target:

- classification: `NONCANONICAL_PROVIDER_SMOKE`;
- provider: `MASSIVE.COM`;
- endpoint: `STOCKS_CUSTOM_BARS_V2`;
- ticker: `AAPL`;
- month: `2025-01`;
- effective start: `2025-01-01`;
- effective end: `2025-01-31`;
- multiplier: `15`;
- timespan: `minute`;
- adjusted: `true`;
- sort: `asc`;
- limit: `50000`;
- Strategy enabled: false;
- calendar/bar derivation enabled: false;
- registry eligibility: false;
- canonical eligibility: false.

There is no caller override for ticker, month, dates, limit, provider, host, or
semantic policy. There is no current-date behavior and no automatic range
expansion.

## Smoke Digest

Smoke specification digest:

```text
2116c4dfa3e8ea759e5bca09cf0f4ccc329134f0cac1329ad871fb7746cdcfe4
```

The digest is deterministic canonical JSON and excludes API key, current time,
run ID, runtime path, provider response, OHLCV values, and console formatting.

## Plan Command

Command:

```text
env\Scripts\python.exe -m marketflow.historical_data --massive-smoke-plan
```

Result: pass.

Confirmed: no provider call, no credential prompt, no socket, no persistent
write, sanitized fixed plan, smoke digest visible, execution disabled, and no
semantic override accepted.

Required confirmation phrase:

```text
RUN MARKETFLOW MASSIVE SMOKE 2116c4dfa3e8
```

## Authorization Ceremony

The live command requires the exact digest-bound confirmation phrase before
the API-key prompt. Wrong phrase and wrong prefix reject. The confirmation text
is not persisted, cannot authorize another smoke specification, and the default
process-local live path rejects reuse of a successful authorization.

## Credential Boundary

The live credential path is only hidden `getpass` after authorization. No CLI
key, environment key, config key, ordinary visible input, URL key, provider
account query, or separate key-validation call exists.

Empty, whitespace, CR/LF, control-character, and header-injection keys are
rejected by `ProviderApiKey`. Raw keys are absent from public `repr`, `str`,
receipts, artifacts, logs, exceptions, and test assertion output. Tests use
fictional credentials only.

The monthly executor parses HTTP 200 bodies and screens credential-like
continuation URLs before raw-page persistence.

## Interactive-Only Behavior

Command:

```text
env\Scripts\python.exe -m marketflow.historical_data --massive-smoke-run
```

Result in this noninteractive acceptance shell: rejected with
`SMOKE_AUTHORIZATION_REJECTED` and finding `LIVE_SMOKE_REQUIRES_INTERACTIVE_TTY`.

The production live path rejects redirected standard input, piped confirmation,
piped API key, non-TTY execution, unattended operation, and ordinary CI
execution before credential prompt or transport construction.

## Live Network Boundary

The smoke runner is the only new boundary that can invoke
`MassiveRestTransport` with the real backend, and only after interactive
authorization and hidden credential entry.

The future live target is exactly AAPL / January 2025 Custom Bars. It performs
no entitlement, account, billing, ticker-overview, corporate-action, key
validation, broader acquisition, or fallback-provider request.

This acceptance did not execute the live path.

## Runtime Root

Source-defined live root:

```text
.marketflow/provider_smoke/runs/
```

Confirmed: opaque run directory, no ticker/month in directory names, ignored by
Git through `.marketflow/`, no arbitrary external production root, no canonical
data root, no report-root reuse, no registry root, no overwrite, and safe
relative artifact references. Tests use temporary directories.

## Artifact Chain

Smoke artifacts retain:

```text
LIVE_PROVIDER_SMOKE_NONCANONICAL
```

Allowed live smoke artifacts:

- month request;
- attempt records;
- raw pages;
- completeness manifest;
- normalized 15m OHLCV;
- normalized supplemental aggregate-audit fields;
- monthly receipt;
- smoke receipt.

Not created: frozen calendar, derived SWING/POSITION bars, analytical segment
maps, annotations, candidates, Monte Carlo, outcomes, canonical registry
records, reports, or runtime migration artifacts.

## Receipt

The smoke receipt may contain status, smoke digest, smoke run ID, fixed
classification, provider, ticker, month, attempt count, accepted-page count,
raw-page count, pagination/completeness status, normalized row count, safe
artifact receipts, first/last source timestamp where approved, Contract v2.1
digest, and fixed findings.

It excludes API key, Authorization header, raw URL, raw `next_url`, raw provider
body, OHLCV/VWAP/count values, absolute paths, account/provider-account data,
raw exception strings, candidate values, and performance values.

Fixed statuses covered:

- `SMOKE_PLAN_VALID`;
- `SMOKE_AUTHORIZATION_REJECTED`;
- `SMOKE_CREDENTIAL_REJECTED`;
- `SMOKE_TRANSPORT_FAILED`;
- `SMOKE_MONTH_INCOMPLETE`;
- `SMOKE_COMPLETED_NONCANONICAL`;
- `SMOKE_INVALID`.

A successful smoke does not enable acquisition or create canonical data.

## Self-Check

Command:

```text
env\Scripts\python.exe -m marketflow.historical_data --massive-smoke-self-check
```

Result: pass.

Confirmed: mock HTTP only, fictional key only, injected prompt seams, temporary
output only, no socket, no persistent artifacts, sanitized receipt, no key
leakage, and no Strategy/calendar/bar/registry path. The self-check is distinct
from `--massive-smoke-run`.

## Contract Non-Regression

Reproduced digests:

```text
v1:    29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
v2:    59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
v2.1:  538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
smoke: 2116c4dfa3e8ea759e5bca09cf0f4ccc329134f0cac1329ad871fb7746cdcfe4
```

## No-Network Evidence

No automated test opens an external socket for this smoke path. Smoke tests use
`httpx.MockTransport`; source assurance rejects default-test
`MassiveRestTransport` construction without `MockTransport`. No default pytest
path invokes the live command or reads a real key. Existing socket-denial and
manual-check collection boundaries remain in source assurance.

## Normal Runtime

`marketflow normal <ticker>` remains unchanged and does not invoke the smoke
runner or Massive transport. Runtime migration status remains:

```text
LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION
```

## Verification

Python:

```text
Python 3.12.10
```

`pip check`: pass, `No broken requirements found.`

Focused smoke plus source-assurance regression:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_one_month_smoke.py tests/test_source_assurance.py
```

Result: 44 passed.

Expanded smoke-runner, Massive transport, monthly executor, historical
artifact, Contract, source-assurance, packaging, and prior-integrity group:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_one_month_smoke.py tests/test_massive_rest_transport.py tests/test_fake_transport_monthly_acquisition.py tests/test_historical_data_artifacts.py tests/test_historical_data_engine.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py
```

Result: 237 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 821 tests collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 821 passed.

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass with Git LF-to-CRLF working-copy normalization
warnings only.

Staged diff checks:

```text
git diff --cached --name-status
```

Result: 11 intended smoke-runner source, bounded executor/CLI/source-assurance,
test, documentation, and acceptance-evidence files staged.

```text
git diff --cached --stat
```

Result: 11 files changed, 1895 insertions, 29 deletions.

```text
git diff --cached --check
```

Result: pass.

Final staged-source rerun:

- expanded regression group: 237 passed;
- full default suite: 821 passed.

Test count explanation: accepted starting collection was 798 tests at
`v0.1.0-alpha.19-massive-rest-transport-offline`. Final collection is 821
because this task adds 22 focused smoke-runner tests and 1 source-assurance
test.

## Git Status Evidence

Pre-test status:

```text
## feature/swing-massive-one-month-smoke-runner
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
 M marketflow/historical_data/monthly_acquisition.py
?? docs/architecture/MARKETFLOW_NONCANONICAL_PROVIDER_SMOKE.md
?? docs/plans/MARKETFLOW_MASSIVE_ONE_MONTH_SMOKE_PLAN.md
?? docs/security/MARKETFLOW_LIVE_SMOKE_CREDENTIAL_POLICY.md
?? docs/status/MARKETFLOW_MASSIVE_ONE_MONTH_SMOKE_RUNNER_STATUS.md
?? marketflow/historical_data/massive_smoke.py
?? tests/test_massive_one_month_smoke.py
```

Post-test status before staging:

```text
## feature/swing-massive-one-month-smoke-runner
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
 M marketflow/historical_data/monthly_acquisition.py
 M tests/test_source_assurance.py
?? docs/architecture/MARKETFLOW_NONCANONICAL_PROVIDER_SMOKE.md
?? docs/plans/MARKETFLOW_MASSIVE_ONE_MONTH_SMOKE_PLAN.md
?? docs/security/MARKETFLOW_LIVE_SMOKE_CREDENTIAL_POLICY.md
?? docs/status/MARKETFLOW_MASSIVE_ONE_MONTH_SMOKE_RUNNER_STATUS.md
?? marketflow/historical_data/massive_smoke.py
?? tests/test_massive_one_month_smoke.py
```

`.marketflow/` appears only as ignored local state. No persistent smoke output
under `.marketflow/provider_smoke/runs/` was created by acceptance checks.

Pre-final-staged-source-rerun status:

```text
## feature/swing-massive-one-month-smoke-runner
A  docs/architecture/MARKETFLOW_NONCANONICAL_PROVIDER_SMOKE.md
A  docs/plans/MARKETFLOW_MASSIVE_ONE_MONTH_SMOKE_PLAN.md
A  docs/security/MARKETFLOW_LIVE_SMOKE_CREDENTIAL_POLICY.md
A  docs/status/MARKETFLOW_MASSIVE_ONE_MONTH_SMOKE_RUNNER_ACCEPTANCE.md
A  docs/status/MARKETFLOW_MASSIVE_ONE_MONTH_SMOKE_RUNNER_STATUS.md
M  marketflow/historical_data/__init__.py
M  marketflow/historical_data/__main__.py
A  marketflow/historical_data/massive_smoke.py
M  marketflow/historical_data/monthly_acquisition.py
A  tests/test_massive_one_month_smoke.py
M  tests/test_source_assurance.py
```

## Reviewer Findings

Reviewer A initial findings from implementation audit:

- Medium: live-provider artifacts reported provider execution disabled.
  Disposition: fixed with `provider_execution_enabled=True` for smoke live
  monthly execution while fake defaults remain false.
- Medium: credential-like `next_url` could be persisted before parser
  rejection. Disposition: fixed by parsing HTTP 200 bodies before raw-page
  persistence and adding regression coverage.

Reviewer A final findings:

- Medium: default no-network source assurance did not cover
  `MassiveRestTransport`. Disposition: fixed with a source-assurance test
  requiring `httpx.MockTransport` for default-test `MassiveRestTransport`
  construction.
- Low: default live CLI path did not use active authorization reuse protection.
  Disposition: fixed with process-local `_LIVE_AUTHORIZATION_STATE` and focused
  coverage proving reuse rejects before credential prompt or transport
  construction.

Reviewer B: no findings.

No critical or high reviewer finding remains.

## Warnings

Git reports LF-to-CRLF working-copy normalization warnings on modified text
files. No project-owned warning was suppressed to make tests pass.

## Remaining Limitations

- Live smoke has not been executed.
- No actual API key was inspected.
- No provider request occurred.
- No market data was downloaded.
- Future live target remains AAPL / January 2025.
- All smoke output remains noncanonical.
- Acquisition remains disabled.
- No Strategy or performance path exists.
- Normal runtime migration remains pending.

## Manual Smoke Procedure

Future live smoke requires a separately authorized operator action in an
interactive terminal:

```powershell
$python = (Resolve-Path ".\env\Scripts\python.exe").Path
& $python -m marketflow.historical_data --massive-smoke-plan
& $python -m marketflow.historical_data --massive-smoke-run
```

The operator must type exactly:

```text
RUN MARKETFLOW MASSIVE SMOKE 2116c4dfa3e8
```

Only after that phrase is accepted will the hidden Massive.com API-key prompt
appear. Any resulting artifacts remain noncanonical smoke evidence and do not
enable acquisition, canonical registry approval, Strategy use, or runtime
migration.
