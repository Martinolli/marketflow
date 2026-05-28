# MARKETFLOW_BACKTEST_CALIBRATION_SUMMARY_PLAN

## 1. Purpose

This plan defines how MarketFlow should summarize deterministic backtest outcome result CSVs to support future parameter calibration.

This checkpoint is planning only. It does not change code, tests, Studio UI, Strategy Ranking, Monte Carlo, Backtest Outcome Evaluation, or artifact formats.

This is research/calibration only. It is not financial advice, not an optimization engine, and not a trade signal generator.

Implementation status: `marketflow/services/backtest_calibration_service.py` now provides service-only global and grouped summary metrics for saved `*_backtest_results*.csv` artifacts. Studio UI and markdown artifact writing remain future work.

Markdown artifact writer status: implemented service-level markdown generation and saving for Backtest Calibration Summary results. Studio UI remains future work.

## 2. Current Baseline

The current implemented pipeline is:

```text
Strategy Ranking
-> canonical `*_wyckoff_annotated.csv`
-> enriched Backtest Candidate Snapshot
-> Backtest Outcome Evaluation
-> `*_backtest_results.csv`
```

Current status:

- `backtest_results_csv` artifact classification exists
- full pytest is currently healthy
- signal-location enrichment reduced `INVALID` rows caused only by missing location

## 3. Problem Statement

Calibration is needed because one parameter set is not best for all tickers.

Key reasons:

- price scale differs by ticker
- volatility differs by ticker
- timeframes represent different real-world horizons
- 20 bars means different things on 1d, 4h, 1h, and 1w
- Monte Carlo model choice may differ by volatility regime
- backtest results should guide defaults over time

For example, AAPL trading above 250 and AI trading around 9 should not be assumed to share one universal horizon, model, or volatility interpretation.

## 4. Source Artifacts

Input artifacts:

```text
*_backtest_results*.csv
```

Artifact kind:

```text
backtest_results_csv
```

Expected result columns include:

- ticker
- timeframe
- source_csv
- signal_timestamp
- signal_row_index
- entry
- stop_loss
- take_profit
- risk_reward
- strategy_score
- wyckoff_phase
- wyckoff_event
- trend
- outcome
- bars_to_hit
- realized_R
- same_bar_hit
- tie_break_policy
- horizon_bars
- planned_rr
- mark_to_market_close
- outcome_error
- backtest_success

## 5. Core Summary Metrics

First-pass metrics:

```text
count
valid_count
invalid_count
invalid_rate
tp_first_count
sl_first_count
neither_count
ambiguous_count
tp_first_rate
sl_first_rate
neither_rate
ambiguous_rate
mean_realized_R
median_realized_R
win_loss_ratio
mean_bars_to_hit
median_bars_to_hit
mean_planned_rr
```

Clarifications:

- `INVALID` rows should be counted separately
- `NEITHER` is valid, not failure
- `AMBIGUOUS` is valid but should be reviewed
- `backtest_success=True` means outcome was evaluable, not profitable

## 6. Grouping Dimensions

Grouping dimensions:

```text
ticker
timeframe
horizon_bars
tie_break_policy
wyckoff_phase
wyckoff_event
trend
source_csv
report_date
```

Recommended first grouping:

```text
ticker + timeframe + horizon_bars + tie_break_policy
```

Secondary grouping:

```text
wyckoff_phase + wyckoff_event + trend
```

## 7. Timeframe-Aware Horizon Interpretation

Starting interpretation:

```text
1w horizon 12 ~= medium weekly thesis
1d horizon 20 ~= one trading month
4h horizon 40 ~= tactical multi-day swing
1h horizon 80 ~= short tactical/intraday swing
```

Horizon bars are not calendar days. Each timeframe needs its own default, and comparing horizons should be done within timeframe first.

## 8. Ticker-Aware Interpretation

Absolute price does not define risk. Calibration should compare outcomes in R, ATR, and percentage terms.

AAPL and AI need different volatility assumptions. Calibration should compare outcomes by ticker/timeframe rather than price level alone.

Recommended future ticker classes:

- large liquid equity
- speculative/high-volatility equity
- ETF/commodity proxy
- low-history ticker
- unknown/review needed

## 9. Monte Carlo Model Calibration Future

This plan does not join Monte Carlo forecasts yet.

Future comparison should evaluate:

- Monte Carlo model
- horizon
- TP-first forecast
- SL-first forecast
- neither forecast
- actual deterministic outcome
- calibration error

Future model categories:

- bootstrap
- GARCH
- GBM
- other

## 10. Recommended First Service Design

Plan future service file:

```text
marketflow/services/backtest_calibration_service.py
```

Potential functions:

```python
def read_backtest_results_csv(path: str | Path) -> dict[str, Any]:
    ...

def summarize_backtest_results_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ...

def summarize_backtest_results_csv(path: str | Path) -> dict[str, Any]:
    ...

def summarize_backtest_results_folder(report_dir: str | Path) -> dict[str, Any]:
    ...
```

Return shape idea:

```python
{
    "success": bool,
    "count": int,
    "summary_rows": [...],
    "grouped_summary_rows": [...],
    "errors": [...],
    "warnings": [...],
}
```

## 11. Future Artifact Design

Plan a future markdown artifact:

```text
*_backtest_calibration_summary_YYYYMMDD_HHMMSS.md
```

Potential artifact kind:

```text
backtest_calibration_summary_md
```

Include:

- metadata
- source result files
- global summary
- grouped summary
- invalid row review
- notes and guardrails

Do not implement in this task.

## 12. Future Studio Location

Recommended location:

```text
Strategy Ranking page, after Backtest Outcome Evaluation
```

Alternative future location:

```text
Generated Artifacts page
```

Recommended first UI:

- select result CSVs from current report folder
- summarize selected result files
- show grouped table
- save markdown summary artifact

## 13. Guardrails

- calibration only
- does not optimize automatically
- does not produce buy/sell signals
- deterministic backtest outcomes are historical/contextual
- small sample sizes are not reliable
- invalid rows must remain visible
- tie-break policy affects ambiguous same-bar outcomes
- do not compare 1h and 1d horizons directly without normalization

## 14. Handling Small Samples

Small-sample policy:

- if sample size < 10, show small-sample warning
- if sample size < 30, show caution
- grouped metrics with very small samples should not be overinterpreted
- report counts beside every rate

## 15. Invalid Row Review

Summarize invalid rows by reason:

- missing source_csv
- missing signal location
- missing levels
- invalid levels
- unsupported direction
- source CSV unreadable
- other

Goal:
Track whether pipeline quality is improving.

## 16. Acceptance Criteria For Future Implementation

Future implementation should satisfy:

- reads one or more `*_backtest_results*.csv`
- computes global summary
- computes grouped summary
- separates invalid rows
- preserves `NEITHER` and `AMBIGUOUS` correctly
- produces JSON-safe dictionaries
- has focused unit tests
- does not change existing backtest evaluation behavior

## 17. Future Tests

Planned tests:

1. one valid TP_FIRST row summary
2. one valid SL_FIRST row summary
3. NEITHER counted as valid
4. AMBIGUOUS counted as valid
5. INVALID counted separately
6. grouped summary by ticker/timeframe/horizon
7. missing optional columns handled safely
8. empty input returns warning
9. folder summary discovers only `backtest_results_csv`
10. small sample warning generated
11. invalid reasons summarized
12. no mutation of input rows

## 18. Non-Goals

- no implementation in this checkpoint
- no Studio UI
- no artifact writer
- no Monte Carlo join
- no parameter optimization
- no machine learning
- no trade recommendation
- no short setup support
- no external dependencies

## 19. Recommended Next Implementation Task

Next recommended task:
Implement `marketflow/services/backtest_calibration_service.py` with service-only summary metrics for saved `*_backtest_results*.csv` files.

Status: Backtest Calibration Summary service implemented at the service-only summary layer.
