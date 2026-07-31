# MarketFlow Fixed Profile Orchestrator Status

Status: LOCAL ACCEPTANCE PASSED, COMMIT AUTHORIZED

## Boundary

This task implements the normal ticker-only fixed-profile workflow and permits
one local commit of the verified implementation. It does not approve predictive
usefulness, profitability, provider readiness, broker readiness, execution
capability, Monte Carlo horizons, outcome campaigns, research protocol freeze,
tag creation, push, or remote changes.

## Intended Normal Contract

Normal input is one ticker only. MarketFlow evaluates:

- `SWING` on `4h` with `390` minimum valid OHLCV rows.
- `POSITION_SWING` on `1d` with `560` minimum valid OHLCV rows.

Results remain separate. No blended score or combined recommendation is
created.

## Current Implementation Notes

- Existing timeframe and period settings remain acquisition/advanced settings.
- `get_primary_timeframe()` remains legacy-compatible for existing callers,
  but normal mode must not use it.
- Fixed profile definitions are immutable source constants in
  `marketflow/marketflow_data_parameters.py`.
- Normal ticker-only orchestration is implemented in
  `marketflow/fixed_profile_orchestrator.py`.
- The normal CLI is `env\Scripts\python.exe -m marketflow normal <ticker>`.
- Normal mode uses the repository-controlled `.marketflow/reports` source root,
  not environment/configured `REPORT_DIR`.
- Normal source resolution accepts canonical annotated CSV sources only. Raw
  CSVs and generated derivative CSVs are not normal-mode sources.
- Structurally blocked normal CLI runs do not import Strategy, facade,
  provider, Streamlit, Monte Carlo, outcome, or LLM modules.
- Studio remains optional and non-authoritative.
- Existing advanced Strategy, Monte Carlo, plot, and batch commands remain
  available with explicit options.

## Expected Blockers

Local data may block a profile independently:

- `DATASET_NOT_FOUND`;
- `DATASET_IDENTITY_AMBIGUOUS`;
- `DATASET_INVALID`;
- `INSUFFICIENT_HISTORY`;
- `CANDIDATE_NOT_AVAILABLE`;
- `CANDIDATE_INCOMPLETE`;
- `PROFILE_ANALYSIS_FAILED`.

Automatic Monte Carlo and outcome evaluation remain blocked by authorization
status:

- `MONTE_CARLO_NOT_AUTHORIZED`;
- `OUTCOME_EVALUATION_NOT_AUTHORIZED`.

Because automatic Monte Carlo is not authorized, the accepted Strategy
rank-eligibility contract may leave otherwise data-ready profiles as
`CANDIDATE_INCOMPLETE`. Normal mode does not fabricate POP evidence, define an
MC horizon, or force a `CANDIDATE_CORE` artifact. It writes a candidate artifact
only if the existing canonical candidate builder reports a valid
rank/action-eligible candidate under accepted semantics.

## Verification Plan

Required checks use `env\Scripts\python.exe` and remain offline:

- `env\Scripts\python.exe -m pip check`;
- focused fixed-profile orchestrator tests;
- related lineage/source/data-parameter tests;
- `env\Scripts\python.exe -m pytest --collect-only -q`;
- full `env\Scripts\python.exe -m pytest -q`;
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`;
- `git diff --check`;
- final `git status --short`.

No tag, push, remote change, provider check, broker check, manual market-data
check, Monte Carlo run, or outcome/performance run is authorized in this task.

## Verification Evidence

Current local checks:

- `env\Scripts\python.exe -m pip check`: passed.
- Focused fixed-profile orchestrator tests: `31 passed`.
- Related fixed-profile/orchestration/lineage/CLI/evidence/source-assurance and
  prior-integrity tests: `232 passed`.
- `env\Scripts\python.exe -m pytest --collect-only -q`: `600 tests collected`.
- `env\Scripts\python.exe -m pytest -q`: `600 passed`.
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: passed.
- `git diff --check`: passed with Git LF-to-CRLF notices for touched tracked
  files only.

Test count explanation: accepted Artifact Lineage v1 baseline collected `569`
tests. This task currently adds `31` focused deterministic tests for fixed profile
contract values and digests, profile immutability, normal ticker validation,
exact local source resolution, row gates, independent lineage runs, MC/outcome
authorization blocking, CLI semantic-flag rejection, import isolation,
canonical-source-only resolution, candidate-incomplete diagnostics, partial
failure receipts, and top-level status semantics.
