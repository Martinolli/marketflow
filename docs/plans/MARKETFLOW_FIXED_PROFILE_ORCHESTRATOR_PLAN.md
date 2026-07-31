# MarketFlow Fixed Profile Orchestrator Plan

## Scope

Implement the normal operator workflow as a ticker-only, local-data-only
orchestrator. The same ticker is evaluated independently through two
source-defined profiles:

- `SWING`: candidate timeframe `4h`, minimum valid OHLCV rows `390`, intended
  use `SEVERAL_TRADING_DAYS`.
- `POSITION_SWING`: candidate timeframe `1d`, minimum valid OHLCV rows `560`,
  intended use `SEVERAL_DAYS_TO_WEEKS`.

The orchestrator must not acquire market data, choose periods, optimize
parameters, run Monte Carlo, run outcome evaluation, blend profile scores, or
promote legacy latest/first selection.

## Current Timeframe-List Problem

`marketflow/marketflow_data_parameters.py` currently exposes a broad
acquisition list:

| Interval | Period |
| --- | --- |
| `1mo` | `5y` |
| `1w` | `2y` |
| `1d` | `365d` |
| `4h` | `100d` |
| `2h` | `60d` |
| `1h` | `150d` |
| `30m` | `20d` |
| `15m` | `20d` |
| `5m` | `20d` |
| `1m` | `20d` |

`MarketFlowDataParameters.get_primary_timeframe()` returns the first list
item. Therefore list ordering currently changes primary-timeframe behavior for
callers that consume that method. That ordering must not define normal
`SWING` or `POSITION_SWING` semantics.

Current known callers and surfaces:

- `scripts/manual_checks/point_in_time_analyzer_real_data_check.py` calls
  `get_primary_timeframe()` for manual checks.
- `scripts/manual_checks/multi_timeframe_analyzer_real_data_check.py` calls
  `get_timeframes()` for manual checks.
- `marketflow/services/analysis_service.py` maps UI timeframe selections to
  period values and calls `run_analysis`; this is a Studio/service analysis
  path, not the normal fixed-profile contract.
- `marketflow/__main__.py analyze` exposes `--timeframes`; this remains an
  advanced/acquisition-oriented interface.
- `scripts/marketflow_batch_analysis.py` has no period flag, but canonical
  lineage mode accepts explicit lineage timeframes and profile. It remains an
  advanced workflow driver, not the normal ticker-only interface.
- `marketflow/marketflow_strategy.py` exposes timeframe and StrategyConfig
  controls. It remains advanced/research mode.
- `apps/marketflow_studio.py` exposes report artifact filters, CSV selection,
  Strategy Ranking timeframe/config controls, PnF, plot, and Eigen controls.
  It remains optional and non-authoritative.

Downloader/provider code consumes period/timeframe values through the analysis
facade and data-provider paths. This task does not change acquisition periods
or provider behavior.

## Risks

- Accidental primary-timeframe risk: normal semantics could drift if they call
  `get_primary_timeframe()` and the acquisition list is reordered.
- Duplicate-generation risk: changing periods or acquisition timeframes can
  create multiple local sources for one ticker/timeframe. Normal mode must
  fail closed on duplicate exact identities instead of selecting newest,
  longest, canonical-looking, first glob match, or modification time.
- Score-blending risk: presenting two profile outputs as one recommendation
  would create an unreviewed strategy semantic.
- Monte Carlo horizon risk: automatic MC would require unapproved horizons.

## Fixed Profile Schema

Profiles are immutable source constants with:

- profile version;
- profile ID;
- candidate timeframe;
- minimum valid OHLCV rows;
- intended-use classification;
- higher-timeframe context status;
- automatic Monte Carlo status;
- automatic outcome-evaluation status.

Profile digests are deterministic and exclude ticker, local paths, dates, run
IDs, artifact IDs, report formatting, and credentials.

## Normal Ticker-Only Contract

Normal mode accepts exactly one ticker. It rejects empty values, surrounding
whitespace, path separators, control characters, unsupported punctuation,
comma-separated lists, timeframe suffixes, filenames, source paths, account
data, and order-like input.

The same normalized ticker is evaluated separately under both profiles.

## Local Data Resolution

For each profile, normal mode resolves exactly one local canonical annotated
CSV source under the repository-controlled `.marketflow/reports` root for
`ticker + candidate_timeframe`.

Statuses:

- zero exact sources: `DATASET_NOT_FOUND`;
- one exact source: continue to read-only quality validation;
- multiple exact sources: `DATASET_IDENTITY_AMBIGUOUS`;
- unsafe or invalid source/root: `DATASET_INVALID`.

Raw CSVs and generated derivative CSVs are not normal-mode sources. No
provider download, automatic duplicate remediation, source outside the approved
local root, newest selection, longest-file selection, suffix preference,
modification-time selection, or fallback is allowed.

## Minimum-Row Gates

Dataset validation checks root confinement, regular CSV file status, required
OHLCV columns, parseable timestamps, chronological order, duplicate
timestamps, finite OHLCV, `high >= low`, and numeric nonnegative volume.
Invalid OHLCV rows are excluded from the valid-row count. If valid rows are
below the profile floor, the profile status is `INSUFFICIENT_HISTORY`.

## Independent Profile Runs

When a profile is ready, normal mode creates one separate Artifact Lineage v1
run for that profile, writes an `ANNOTATED_DATASET` artifact, calls the
canonical candidate builder, and writes a `CANDIDATE_CORE` artifact only when a
valid rank/action-eligible core exists.

`SWING` and `POSITION_SWING` must not share candidate core, candidate score,
event context, target, stop, RR, evidence state, Monte Carlo summary, plot, or
run ID.

## Boundaries

Automatic Monte Carlo remains disabled. The profile receipt reports
`MONTE_CARLO_NOT_AUTHORIZED` because SWING and POSITION_SWING MC horizons have
not been approved through the research protocol.

Outcome evaluation remains disabled and reports
`OUTCOME_EVALUATION_NOT_AUTHORIZED`.

Candidate-only plots are deferred in this task. No MC-overlay plot is created
without an MC artifact.

The canonical candidate builder remains single-timeframe. Profile results are
parallel, not hierarchical.

## Interface Classification

- Normal canonical mode: ticker only, fixed SWING and POSITION_SWING profiles,
  local source only, no semantic overrides.
- Advanced/research mode: explicit scripts and configuration may expose
  timeframe, StrategyConfig, evidence toggles, PnF, MC, and exact lineage
  handoffs.
- Legacy mode: timestamp/latest conveniences and historical reports; explicit
  opt-in only and no canonical-lineage claim where unsupported.

## Tests

Focused tests will use synthetic temporary datasets and temporary lineage
roots. They will cover profile immutability and digest behavior, strict ticker
input, source resolution, row gates, independent per-profile execution,
lineage receipts, no score blending, no automatic MC/outcome, CLI rejection of
semantic flags, and no list-order primary-timeframe dependency.

## Stop Conditions

Stop and fail closed if implementation would require provider acquisition,
dependency changes, data-file modification, historical report migration,
duplicate resolution, period changes, candidate formula changes, Monte Carlo
horizon definition, outcome evaluation, broker/execution behavior, or
profitability analysis.
