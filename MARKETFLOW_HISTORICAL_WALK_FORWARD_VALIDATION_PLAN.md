# MARKETFLOW_HISTORICAL_WALK_FORWARD_VALIDATION_PLAN

## 1. Purpose

This plan defines how MarketFlow should validate historical strategy candidates using walk-forward logic.

This checkpoint is planning only. It does not implement historical walk-forward validation, change services, change Studio UI, change tests, change artifact formats, add dependencies, tune profile values, or change timeframe defaults.

The plan is intended to solve the latest-row `future_bars_available = 0` limitation by selecting historical decision rows that can later be evaluated against mature future bars. It is research and calibration only. It is not financial advice, not a trade signal system, not automatic optimization, and not a source of buy/sell recommendations.

The core validation constraint is no future data leakage: data after a historical decision row may be used only after candidate generation to evaluate what happened next.

Service status: service-only Historical Walk-Forward Validation service implemented in `marketflow/services/walk_forward_validation_service.py`. First implementation builds historical cases and evaluates deterministic backtest outcomes. Studio UI, markdown artifacts, and Monte Carlo forecast integration remain future work.

Markdown artifact writer status: implemented service-level markdown generation and saving for Historical Walk-Forward Validation summaries. Studio UI and Monte Carlo forecast integration remain future work.

Milestone status: `MARKETFLOW_WALK_FORWARD_VALIDATION_MILESTONE_STATUS.md` records the current service-level Historical Walk-Forward Validation workflow and markdown artifact writer checkpoint.

## 2. Current Checkpoint

```text
ef7fcd2 - Document profile validation summary
```

Relevant previous checkpoints:

```text
b506c05 - Add Studio parameter profile selector
f77cf59 - Document parameter profile milestone status
```

## 3. Problem Statement

The current Strategy Ranking workflow selects latest/current candidates. Latest-row candidates often have no future bars after the selected signal row.

Backtest Outcome Evaluation correctly produces `NEITHER` with `no_future_bars_available` when no future rows exist. Monte Carlo Forecast Calibration joins correctly, but marks rows as `not_yet_mature`. As a result, `scoreable_count` remains zero until future bars exist.

This validates the workflow, the artifact join path, and maturity handling, but it does not yet validate strategy performance.

```text
Latest-row validation confirms the pipeline works.
Historical walk-forward validation is needed to test whether the strategy has evidence.
```

## 4. Walk-Forward Concept

```text
For each historical decision point T:

1. Use only data available up to T.
2. Generate candidate/strategy context at T.
3. Record entry, stop loss, take profit, profile, and signal metadata.
4. Evaluate what happened after T over the selected horizon.
5. Compare forecast probabilities against actual outcome.
6. Repeat across many historical rows.
```

"Back" means selecting historical decision rows. "Forward" means checking future outcome after each selected row.

The signal generation path must not use future bars. Future bars are used only for outcome evaluation after candidate generation is complete.

## 5. No-Leakage Rule

```text
At decision row T, MarketFlow must not use any row after T to generate candidate features, Wyckoff labels, Eigen/PCA context, Monte Carlo calibration inputs, or strategy ranking inputs.
```

Future data can only be used after candidate generation to determine the actual outcome. Any future leakage invalidates the validation result. This is the most important guardrail for historical walk-forward validation.

## 6. Relationship With Current Workflow

Walk-forward validation should extend existing components instead of replacing them.

| Current component               | Walk-forward use                                                       |
| ------------------------------- | ---------------------------------------------------------------------- |
| Parameter Profile Selector      | provides profile context for horizon/window/path settings              |
| Data Sufficiency                | checks whether enough rows exist before each historical decision point |
| Strategy Ranking                | eventually generates candidate rows at historical decision points      |
| Backtest Candidate Snapshot     | stores historical candidate snapshots                                  |
| Backtest Outcome Evaluation     | evaluates future TP/SL/NEITHER after each historical signal            |
| Monte Carlo                     | produces forecast probabilities at each historical signal              |
| Monte Carlo Calibration Summary | compares forecast probabilities with actual historical outcomes        |

Current services should be reused where possible. The first implementation should be service-only before any Studio UI is added.

## 7. Candidate Selection Approaches

### 7.1 Snapshot Replay Approach

Use previously saved candidate snapshots, if available.

Pros:

- simple
- low risk
- reuses current artifacts

Cons:

- limited sample size
- only available when snapshots were saved

### 7.2 Historical Row Scan Approach

Scan a source CSV and generate candidate snapshots at multiple historical rows.

Pros:

- creates many mature samples
- better for validation

Cons:

- must ensure no future leakage
- strategy ranking may need row-limited mode

### 7.3 Event-Filtered Historical Scan

Generate candidate snapshots only when certain Wyckoff/event conditions occur, such as:

- SPRING_WEAK
- SPRING_CONFIRMED
- UT_WEAK
- SOS
- LPS
- trend/context filters

Pros:

- focused validation
- useful for testing candidate-quality rules

Cons:

- risk of overfitting if filters are tuned too aggressively

Recommended starting point: use a simple historical row scan or event-filtered scan, but only after a clear service plan exists.

## 8. Historical Decision Row Requirements

Each historical decision row should record:

```text
ticker
timeframe
source_csv
signal_row_index
signal_timestamp
profile_name
entry
stop_loss
take_profit
risk_reward
strategy_score
wyckoff_phase
wyckoff_event
trend
candidate_direction
lookback_rows_available
future_bars_available
```

The row must have enough prior data for the selected profile. The row must have enough future data to be scoreable unless it is intentionally marked not mature. The signal row must not be the latest row for historical validation.

## 9. Maturity and Scoreability

A row is scoreable when:

- forecast exists
- actual outcome exists
- MC horizon equals Backtest Outcome horizon
- future bars available are at least horizon
- outcome is not invalid or ambiguous
- join is unambiguous

A row is not scoreable when:

- no future bars
- partial future window
- horizon mismatch
- invalid candidate
- ambiguous actual outcome
- missing forecast
- missing actual result
- many-to-many join

The current calibration service already handles many of these concepts. Walk-forward validation should produce more scoreable rows by choosing historical rows with future bars available.

## 10. Relationship With Parameter Profiles

Profiles define Eigen window, Backtest horizon, MC horizon, MC paths, and block length. Walk-forward validation should record which profile was used for each historical case.

All built-in profiles align MC and Backtest horizons. Profile metadata should eventually be saved into generated artifacts.

Recommended profile usage:

- Daily/Swing for 1d/4h validation
- Intraday Tactical for 1h/30m/15m validation
- Low-Timeframe Review should remain review-only for 5m/1m

## 11. Relationship With Data Sufficiency

Data Sufficiency must be applied at historical decision row T. Sufficiency should count only rows up to T. Rows after T must not be counted for feature sufficiency. Future bars after T are only for outcome maturity.

Example:

```text
At row T:
lookback_rows_available = T + 1
future_bars_available = total_rows - T - 1
```

A historical row may be:

- sufficient for features
- mature for outcome
- both
- neither

## 12. Relationship With Monte Carlo

Monte Carlo should use only historical data up to decision row T. Bootstrap/GARCH/GBM calibration must not include future returns after T.

MC forecast horizon should match Backtest Outcome horizon. MC forecast artifacts should include historical decision metadata.

Future metadata should include:

```text
walk_forward_run_id
walk_forward_case_id
profile_name
decision_row_index
decision_timestamp
lookback_start_index
lookback_end_index
future_window_start_index
future_window_end_index
```

## 13. Relationship With Backtest Outcome Evaluation

Backtest Outcome Evaluation already evaluates TP/SL/NEITHER after a signal row. Walk-forward validation should use historical signal rows where future bars exist.

This will convert many current `not_yet_mature` situations into scoreable outcomes. Actual outcome should still record:

- TP_FIRST
- SL_FIRST
- NEITHER
- AMBIGUOUS
- INVALID

## 14. Proposed Future Service Design

Plan a future service:

```text
marketflow/services/walk_forward_validation_service.py
```

Potential functions:

```python
def build_walk_forward_cases_from_csv(
    csv_path: str | Path,
    *,
    profile_name: str,
    timeframe: str | None = None,
    min_signal_row: int | None = None,
    max_signal_row: int | None = None,
    step: int = 1,
    event_filters: list[str] | None = None,
    max_cases: int | None = None,
) -> dict[str, Any]:
    ...

def evaluate_walk_forward_cases(
    cases: list[dict[str, Any]],
    *,
    profile_name: str,
) -> dict[str, Any]:
    ...

def summarize_walk_forward_validation(
    evaluated_cases: list[dict[str, Any]],
) -> dict[str, Any]:
    ...

def write_walk_forward_validation_results_csv(
    evaluated_cases: list[dict[str, Any]],
    output_dir: str | Path,
) -> dict[str, Any]:
    ...
```

The first implementation should be service-only. Do not add Studio UI first. Do not perform parameter optimization inside the service.

## 15. Proposed Future Artifact Types

Plan future artifacts:

```text
*_walk_forward_cases*.csv
*_walk_forward_results*.csv
*_walk_forward_validation_summary*.md
```

Potential artifact kinds:

```text
walk_forward_cases_csv
walk_forward_results_csv
walk_forward_validation_summary_md
```

Recommended columns:

- ticker
- timeframe
- profile_name
- signal_row_index
- signal_timestamp
- entry
- stop_loss
- take_profit
- actual_outcome
- future_bars_available
- mc_tp_probability
- mc_sl_probability
- mc_neither_probability
- scoreable
- scoreable_reason
- realized_R
- forecast_R_mean
- wyckoff_phase
- wyckoff_event
- trend
- notes

## 16. Validation Metrics

Plan metrics:

```text
sample_count
scoreable_count
tp_actual_rate
sl_actual_rate
neither_actual_rate
mean_forecast_tp_probability
mean_forecast_sl_probability
mean_forecast_neither_probability
Brier scores
mean_realized_R
median_realized_R
mean_forecast_R
forecast_vs_actual_error
win_rate
loss_rate
neither_rate
average_bars_to_outcome
```

Group by:

- ticker
- timeframe
- profile
- Wyckoff phase
- Wyckoff event
- trend
- candidate direction

## 17. Dataset Constraints

Current findings:

- 1w/1d/4h have cleaner structure but fewer rows
- 30m/15m have more rows but higher noise
- Daily/Swing with Eigen window 80 may be constrained on 1d/4h depending on history
- Intraday Tactical gives better row volume but requires noise caution
- low timeframes should not be overinterpreted

## 18. First Implementation Strategy

Recommend a conservative first implementation:

```text
Phase 1: service-only case builder
Phase 2: service-only outcome evaluation using existing backtest logic
Phase 3: summary CSV/markdown artifact writer
Phase 4: Studio UI only after service and tests are stable
```

Initial scope:

- one ticker/timeframe CSV
- one selected profile
- simple row stepping
- no MC first if too complex
- or MC optional after backtest cases are stable

Suggested initial version:

- build historical cases
- evaluate deterministic backtest outcomes
- produce scoreable rows
- add Monte Carlo forecast integration later

## 19. Guardrails

- no future leakage
- no automatic optimization
- no buy/sell recommendations
- no broker integration
- no profile tuning inside walk-forward service
- no use of future bars for feature generation
- small samples must be flagged
- low-timeframe noise must remain visible
- historical validation does not guarantee future performance
- candidate quality remains separate from workflow validity

## 20. Non-Goals

- no implementation in this checkpoint
- no code changes
- no Studio UI changes
- no default/profile tuning
- no machine learning optimization
- no automatic strategy search
- no macro/micro forecast function yet
- no multi-timeframe alignment implementation yet

## 21. Future Tests

1. Case builder never selects rows without enough lookback.
2. Case builder can require enough future bars.
3. Case builder can include non-mature rows when requested.
4. Future bars are not used in feature window.
5. Horizon alignment is preserved from profile.
6. Event filters select only matching rows.
7. Unknown profile returns safe error.
8. Empty CSV returns safe error.
9. Missing timestamp handled safely.
10. Walk-forward results are JSON/CSV safe.
11. Scoreable count increases when historical rows have enough future bars.
12. No mutation of input data/context.
13. Deterministic output with fixed seed/step settings.
14. Summary groups correctly by ticker/timeframe/profile/event.
15. No future leakage regression test.

## 22. Recommended Next Implementation Task

```text
Next recommended task:
Implement service-only `marketflow/services/walk_forward_validation_service.py` to build historical candidate cases from a source CSV using profile-aware lookback/future-bar rules.
```

Start without Studio UI. Start with deterministic backtest outcome evaluation. Add Monte Carlo forecast integration only after the case builder is stable.

## 23. Final Status

```text
Status: Historical walk-forward candidate validation planning checkpoint only.
```
