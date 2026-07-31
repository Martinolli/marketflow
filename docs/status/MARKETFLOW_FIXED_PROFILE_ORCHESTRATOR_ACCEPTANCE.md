# MarketFlow Fixed Profile Orchestrator Acceptance

Status: PASS

Date: 2026-07-31

Branch: `feature/swing-fixed-profile-orchestrator`

Base reviewed: `24d781f6f83ee8572013957fafa3fa84815345a0`

## Accepted Boundary

This acceptance covers the local, offline, ticker-only normal workflow:

- one ticker input only;
- `SWING` fixed to `4h` with `390` minimum valid OHLCV rows;
- `POSITION_SWING` fixed to `1d` with `560` minimum valid OHLCV rows;
- repository-local canonical annotated CSV sources only;
- independent profile lineage receipts;
- no blended score or combined recommendation.

This acceptance does not approve provider readiness, network acquisition,
broker connectivity, execution behavior, Monte Carlo horizons, outcome
evaluation, predictive usefulness, profitability, manual market checks,
protocol freeze, tag creation, push, or remote changes.

## Implementation Accepted

The accepted source boundary is:

- `marketflow/marketflow_data_parameters.py`: immutable fixed-profile contract
  definitions and deterministic profile digests.
- `marketflow/fixed_profile_orchestrator.py`: ticker validation, canonical
  local source resolution, OHLCV quality gates, independent profile lineage
  runs, candidate receipts, and fail-closed statuses.
- `marketflow/__main__.py`: `python -m marketflow normal <ticker>` CLI entry.
- `marketflow/__init__.py`: lazy package exports so normal blocked paths do not
  import provider/facade paths through package initialization.
- `tests/test_fixed_profile_orchestrator.py`: deterministic offline coverage
  for profile contract, source identity, row gates, CLI behavior, import
  isolation, lineage receipts, and partial failure handling.
- `docs/plans/MARKETFLOW_FIXED_PROFILE_ORCHESTRATOR_PLAN.md`: implementation
  plan and boundaries.
- `docs/architecture/MARKETFLOW_FIXED_ANALYSIS_PROFILES.md`: normal-mode
  architecture contract.
- `docs/status/MARKETFLOW_FIXED_PROFILE_ORCHESTRATOR_STATUS.md`: current status
  and evidence.

## Reviewer Findings Disposition

Independent review finding: normal mode could inherit environment/configured
report roots or eager imports from package/CLI startup.

Disposition: fixed. Normal source resolution now uses the repository-controlled
`.marketflow/reports` root by default, and blocked normal CLI paths are covered
by tests proving they do not import Strategy, facade, provider, Streamlit,
Monte Carlo, outcome, or LLM modules.

Independent review finding: raw CSV files could be accepted as normal canonical
sources.

Disposition: fixed. Normal source resolution accepts canonical annotated CSV
sources only. Raw ticker/timeframe CSVs and generated derivative artifacts are
rejected as unavailable rather than silently selected.

Independent review finding: profile analysis failure after lineage run creation
could lose the partial receipt.

Disposition: fixed. `PROFILE_ANALYSIS_FAILED` preserves the run ID and any
committed artifacts in the profile receipt.

Independent review finding: candidate-incomplete receipts lacked enough
operator diagnostics.

Disposition: fixed. Receipts now include candidate reason, score status,
profile calibration, active evidence profile, and missing/disabled/invalid
component lists when available.

Independent review finding: the normal CLI exposed an unused `--json` flag.

Disposition: fixed. The normal command emits JSON by contract and rejects
`--json` as an unrecognized semantic flag.

## Offline Evidence

- `env\Scripts\python.exe -m pip check`: passed, `No broken requirements
  found.`
- Pre-full-suite `git status --short`: only intended source, test, and
  documentation files were modified or untracked.
- `.marketflow/reports` status before full suite: clean.
- Focused orchestrator suite:
  `env\Scripts\python.exe -m pytest tests\test_fixed_profile_orchestrator.py -q`
  returned `31 passed`.
- Related fixed-profile/orchestration/lineage/CLI/evidence/source-assurance and
  prior-integrity suite returned `232 passed`.
- Collection gate:
  `env\Scripts\python.exe -m pytest --collect-only -q` collected `600 tests`.
- Full default suite: `env\Scripts\python.exe -m pytest -q` returned
  `600 passed`.
- Compile gate:
  `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`
  passed.
- Whitespace gate: `git diff --check` passed with Git LF-to-CRLF notices for
  touched tracked files only.
- Post-full-suite `git status --short`: only intended source, test, and
  documentation files were modified or untracked.
- `.marketflow/reports` status after full suite: clean.

## Artifact And Secret Boundary

No market data, historical `.marketflow/reports` artifacts, generated package
metadata, build outputs, credentials, provider settings, account data, broker
state, network evidence, Monte Carlo results, outcome results, or performance
claims are included in this acceptance boundary.

The normal workflow remains research and decision-support software. It does not
create execution capability.

## Release Action

Authorized local action: create one local commit with message
`feat: add ticker-only fixed-profile orchestrator`.

Explicitly not authorized: tag, push, remote change, network/provider check,
IBKR/broker check, Monte Carlo check, outcome/performance check, or manual
market-data check.
