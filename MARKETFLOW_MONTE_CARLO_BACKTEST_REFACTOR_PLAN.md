# MARKETFLOW_MONTE_CARLO_BACKTEST_REFACTOR_PLAN

## 1. Purpose

This planning checkpoint defines a future Monte Carlo / backtest refactor for MarketFlow. The refactor will compare Monte Carlo forecast assumptions against historical actual outcomes after Strategy Ranking candidates appear.

The goal is calibration and research: measure how forecast probabilities such as TP-first, SL-first, neither, and expected R compare with what happened in later OHLC bars. This is not financial advice, not a buy/sell signal engine, and not an automated trading system.

This plan incorporates ideas from the local note `markdown_files/monte_carlo_backtest_refactor.md`, including single-run versus backtest modes, model calibration, saved statistical exports, backtest CLI concepts, and known risks such as sequential performance, naming clarity, and silent model fallback behavior. The original note remains unchanged.

Monte Carlo forecast-vs-actual calibration plan created at `MARKETFLOW_MONTE_CARLO_FORECAST_CALIBRATION_PLAN.md`.

Monte Carlo summary metadata enrichment status: implemented for future forecast-vs-actual calibration.

Monte Carlo forecast-vs-actual calibration service status: service-only join and summary metrics implemented.

## 2. Current Workflow Baseline

Current Studio evidence flow:

Strategy Ranking candidate -> selected CSV/timeframe -> entry/SL/TP -> Monte Carlo simulation -> Analyst Packet -> Candidate Decision Summary -> Analyst Review Notes

Current Monte Carlo output includes probabilities and diagnostics such as:

- TP-first probability
- SL-first probability
- neither probability
- median bars to TP/SL
- R statistics
- model/calibration parameters
- generated HTML/JSON files

Monte Carlo can be run from a selected candidate and its result can be included in Analyst Packet evidence when aligned with the selected Strategy Ranking setup. It remains optional and does not replace analyst judgment.

## 3. Problem to Solve

Monte Carlo estimates possible future paths, but MarketFlow does not yet systematically compare forecast outputs against realized historical outcomes after a candidate appeared.

The missing comparison is:

- forecast TP-first probability versus actual TP-first occurrence
- forecast SL-first probability versus actual SL-first occurrence
- forecast neither probability versus actual neither occurrence
- expected R versus realized R

Without this loop, it is hard to tell whether Monte Carlo outputs are calibrated, overconfident, underconfident, or only useful for certain timeframes, Wyckoff events, models, or risk/reward profiles.

## 4. Core Backtest Question

When Strategy Ranking produces a candidate at bar T, and Monte Carlo estimates TP/SL probabilities from that point, what actually happened over the next H bars?

The backtest should answer this by replaying historical candidate snapshots without using future data before the signal bar.

## 5. Key Concepts

- candidate snapshot: A frozen record of the setup at the decision point.
- signal bar / decision bar: The row at which the candidate is considered available.
- entry price: The planned entry or reference price used by the candidate.
- stop loss: The planned invalidation level.
- take profit: The planned target level.
- horizon bars: The maximum number of future bars used to evaluate the outcome.
- TP-first outcome: The take-profit level is reached before the stop-loss level.
- SL-first outcome: The stop-loss level is reached before the take-profit level.
- neither outcome: Neither level is reached within the horizon.
- bars to hit: Number of future bars until the first TP/SL hit.
- realized R: Outcome expressed in units of initial risk.
- forecast probability: Monte Carlo estimated probability for an outcome.
- calibration bucket: A probability band used to compare predicted frequency versus realized frequency.

## 6. Candidate Snapshot Model

Proposed candidate snapshot fields:

```text
ticker
timeframe
source_csv
signal_timestamp
signal_row_index
entry
stop_loss
take_profit
risk_reward
strategy_score
wyckoff_phase
wyckoff_event
trend
candidate_source
report_date
```

Optional enrichment fields:

```text
pnf_gate
pnf_objective_quality
mc_model
mc_paths
mc_horizon_bars
eigen_available
eigen_recent_divergence_count
```

The optional fields are for later grouped analysis only. They should not change the initial outcome engine or introduce new scoring logic.

## 7. Outcome Engine Algorithm

Plain English algorithm:

For each candidate snapshot, locate the signal row in the annotated CSV. Starting after the signal bar, scan forward up to the configured horizon. If a future bar touches take profit before stop loss, record TP_FIRST. If it touches stop loss before take profit, record SL_FIRST. If both levels are touched in the same OHLC bar, apply a documented tie-break policy. If neither level is touched by the horizon, record NEITHER and calculate mark-to-market R from the horizon close when available.

Pseudocode:

```text
for snapshot in candidate_snapshots:
    rows = load_csv(snapshot.source_csv)
    signal_row = locate_signal_row(rows, snapshot.signal_timestamp, snapshot.signal_row_index)
    future_rows = rows after signal_row up to horizon_bars

    outcome = NEITHER
    bars_to_hit = null
    same_bar_hit = false

    for offset, bar in enumerate(future_rows, start=1):
        hit_tp = bar.high >= snapshot.take_profit
        hit_sl = bar.low <= snapshot.stop_loss

        if hit_tp and hit_sl:
            same_bar_hit = true
            outcome = apply_tie_break_policy(bar, snapshot)
            bars_to_hit = offset
            break
        else if hit_tp:
            outcome = TP_FIRST
            bars_to_hit = offset
            break
        else if hit_sl:
            outcome = SL_FIRST
            bars_to_hit = offset
            break

    if outcome == NEITHER:
        realized_R = mark_to_market_R(last_available_close, entry, stop_loss)
    else if outcome == TP_FIRST:
        realized_R = planned_R
    else if outcome == SL_FIRST:
        realized_R = -1
```

## 8. Same-Bar Tie-Break Policy

Same-bar TP and SL hits are ambiguous because OHLC data does not reveal intrabar sequence.

Possible policies:

- conservative: SL first
- optimistic: TP first
- open-proximity: whichever level is closer to open
- unknown: mark as ambiguous

Recommended default:

```text
conservative
```

Every same-bar event should also store:

```text
same_bar_hit = true
```

This preserves ambiguity for later review and sensitivity analysis.

## 9. Monte Carlo Forecast Capture

Fields to save from the Monte Carlo result:

```text
pop_tp_first
p_sl_first
p_neither
R_mean
R_p50
R_p05
R_p95
t_hit_tp_median
t_hit_sl_median
model
paths
block_len
seed
mu_bar
sigma_bar
```

The existing local note also mentions several models and calibration parameters. Initial implementation should focus on fields already emitted reliably by current services, then extend only after the output contract is stable.

## 10. Backtest Result Record

Proposed output record:

```text
ticker
timeframe
signal_timestamp
entry
stop_loss
take_profit
planned_rr
strategy_score
wyckoff_phase
wyckoff_event
forecast_tp_first
forecast_sl_first
forecast_neither
forecast_R_mean
actual_outcome
bars_to_hit
realized_R
same_bar_hit
tie_break_policy
horizon_bars
mc_model
source_csv
```

## 11. Calibration Analysis

Summary metrics:

- number of candidates
- TP-first rate
- SL-first rate
- neither rate
- mean realized R
- median realized R
- win rate
- expectancy
- average bars to TP
- average bars to SL
- Brier-style calibration for TP-first probability
- bucket analysis:
  - 0-20%
  - 20-40%
  - 40-60%
  - 60-80%
  - 80-100%

Calibration should compare forecast probability buckets to actual realized frequencies. For example, candidates forecast in the 60-80% TP-first bucket should be reviewed for their actual TP-first rate.

## 12. Grouped Analysis

Planned grouped summaries:

```text
ticker
timeframe
wyckoff_phase
wyckoff_event
strategy_score_bucket
risk_reward_bucket
mc_model
pnf_gate
pnf_objective_quality
eigen_recent_divergence_state
```

P&F and Eigen groupings are optional later enrichments. They should be added as grouping variables only, not as new initial backtest logic or scoring changes.

## 13. Proposed Artifacts

Planned saved artifacts:

```text
*_backtest_candidates.csv
*_backtest_results.csv
*_backtest_calibration_summary.json
*_backtest_calibration_summary.md
*_backtest_bucket_report.csv
*_backtest_equity_curve.csv
```

Planned artifact classifications to add later:

```text
backtest_candidates_csv
backtest_results_csv
backtest_calibration_json
backtest_calibration_summary_md
backtest_bucket_report_csv
backtest_equity_curve_csv
```

These should integrate with Generated Artifacts only after the first services produce stable output files.

## 14. Proposed Services

Future files:

```text
marketflow/services/backtest_service.py
marketflow/backtesting/__init__.py
marketflow/backtesting/outcome_engine.py
marketflow/backtesting/calibration.py
marketflow/backtesting/schemas.py
```

Do not create these files until implementation begins. The first implementation should keep service boundaries narrow and testable.

## 15. Proposed Studio UI

Future Studio workspace:

```text
Backtest Lab
```

Planned sections:

1. Candidate source
   - current report
   - selected ticker folder
   - date range
   - timeframe
2. Candidate generation/replay
3. Outcome engine settings
   - horizon bars
   - tie-break policy
4. Run backtest
5. Results table
6. Calibration summary
7. Bucket analysis
8. Save artifacts

The UI should make calibration/research language explicit and avoid buy/sell labels.

## 16. Implementation Phases

### Phase 1 - Outcome Engine Only

Status: implemented as standalone outcome engine with synthetic tests.

Phase 1.1 status: service wrapper implemented for JSON-safe single-candidate and simple batch evaluation. No Studio UI or artifacts yet.

- Given one CSV and one candidate snapshot, compute actual outcome.
- Unit tests with synthetic OHLC data.

### Phase 2 - Candidate Snapshot Collection

Phase 2 design checkpoint created at `MARKETFLOW_CANDIDATE_SNAPSHOT_COLLECTION_DESIGN.md`.

Phase 2.1 status: candidate snapshot normalization and validation service implemented. Snapshot CSV artifacts and Studio integration remain future work.

Phase 2.2 artifact contract checkpoint created at `MARKETFLOW_BACKTEST_CANDIDATE_ARTIFACT_CONTRACT.md`.

Phase 2.2 implementation status: candidate snapshot CSV writer implemented. Generated Artifacts classification and the selected-candidate Studio save control are implemented. Backtest execution remains future work.

Studio save control status: selected Strategy Ranking candidates can be saved as `*_backtest_candidates*.csv` artifacts. Backtest execution remains future work.

Backtest Outcome Result CSV artifact contract created at `MARKETFLOW_BACKTEST_OUTCOME_RESULT_ARTIFACT_CONTRACT.md`.

Backtest Outcome Result CSV writer status: implemented service-level filename generation, row conversion, and CSV writing. Generated Artifacts classification is implemented. Studio integration remains future work.

Backtest outcome evaluation service status: implemented service-only candidate snapshot CSV evaluation to `*_backtest_results.csv`.

Studio Backtest Outcome Evaluation UI plan created at `MARKETFLOW_STUDIO_BACKTEST_OUTCOME_EVALUATION_UI_PLAN.md`.

Studio Backtest Outcome Evaluation status: implemented as a Strategy Ranking page section for saved candidate snapshot CSVs.

Candidate signal-location enrichment plan created at `MARKETFLOW_CANDIDATE_SIGNAL_LOCATION_ENRICHMENT_PLAN.md`.

Candidate signal-location enrichment status: implemented in the candidate snapshot service.

- Extract candidates from Strategy Ranking output or annotated CSV/report context.
- Save candidate snapshot CSV.

### Phase 3 - MC Forecast Join

- Join Monte Carlo result fields with candidate snapshots.
- Preserve alignment metadata.

### Phase 4 - Calibration Summary

Backtest Calibration Summary plan created at `MARKETFLOW_BACKTEST_CALIBRATION_SUMMARY_PLAN.md`.

Backtest Calibration Summary service status: implemented service-only result CSV summaries.

Backtest Calibration Summary artifact writer status: implemented markdown summary writer for saved result CSV summaries.

- Compute actual versus forecast metrics.
- Save summary JSON/Markdown.

### Phase 5 - Studio Backtest Lab

- Add UI controls and artifact browser integration.

### Phase 6 - Optional Evidence Enrichment

- Add P&F and Eigen context as grouping variables only.

## 17. Testing Strategy

Tests to add during implementation:

- synthetic TP-first case
- synthetic SL-first case
- synthetic neither case
- same-bar conservative tie-break
- missing columns
- short horizon
- invalid candidate levels
- known CSV fixture
- calibration bucket calculation
- artifact classification

Tests should focus first on deterministic outcome behavior before touching Studio UI.

## 18. Non-Goals

- No broker integration.
- No live trading.
- No automated trade execution.
- No financial advice.
- No modification to Strategy Ranking scoring during the initial phases.
- No use of future data before signal bar.
- No optimization loop in initial implementation.
- No parameter fitting to maximize past returns in the first version.

## 19. Risks and Guardrails

Key risks:

- look-ahead bias
- survivorship bias
- small sample sizes
- same-bar ambiguity
- OHLC intrabar uncertainty
- overfitting
- regime changes
- ticker selection bias
- path-dependency and slippage not represented

Guardrails:

- Keep signal-bar data boundaries explicit.
- Store tie-break policy and same-bar ambiguity.
- Treat calibration as descriptive research, not strategy optimization.
- Avoid changing Strategy Ranking or Monte Carlo math during early phases.
- Prefer transparent artifact outputs over opaque UI-only state.
- Surface model fallback warnings clearly if later refactoring touches model execution behavior.

## 20. Recommended First Implementation Task

Recommended first task:

```text
Phase 1 - implement standalone outcome engine with synthetic tests
```

Do not implement it yet.

Status: planning checkpoint only.
Next recommended task: implement Phase 1 outcome engine with tests.
