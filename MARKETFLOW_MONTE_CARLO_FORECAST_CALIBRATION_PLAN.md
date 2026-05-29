# MARKETFLOW_MONTE_CARLO_FORECAST_CALIBRATION_PLAN

## 1. Purpose

This plan defines how MarketFlow should compare Monte Carlo forecast probabilities against deterministic backtest outcomes.

This checkpoint began as planning only. It is for research/calibration only, is not financial advice, is not a trade signal generator, and is not parameter optimization.

Monte Carlo summary metadata enrichment status: implemented. Newly generated `*_mc_summary.json` files now include `join_metadata` for future forecast-vs-actual calibration joins.

Service status: service-only Monte Carlo forecast-vs-actual calibration join implemented in `marketflow/services/monte_carlo_calibration_service.py`. Studio UI remains future work.

Markdown artifact writer status: implemented service-level markdown generation and saving for Monte Carlo forecast-vs-actual calibration summaries. Studio UI remains future work.

## 2. Current Baseline

Current workflow:

```text
Strategy Ranking
→ Backtest Candidate Snapshot
→ Backtest Outcome Evaluation
→ Backtest Calibration Summary
```

Current artifacts include:

- `backtest_candidates_csv`
- `backtest_results_csv`
- `backtest_calibration_summary_md`
- Monte Carlo summary JSON artifacts, if available, such as `*_mc_summary.json`

Future-bar diagnostics are now available in backtest results and should be used to filter or flag forecast-vs-actual calibration comparisons:

- `future_bars_available`
- `evaluation_window_start_index`
- `evaluation_window_end_index`
- `signal_is_latest_row`
- `neither_reason`

## 3. Problem Statement

Monte Carlo produces probabilistic forecasts.

Backtest Outcome Evaluation produces deterministic actual outcomes.

To know whether forecasts are useful, MarketFlow needs to compare forecast probabilities with realized outcomes over many samples.

One or two rows are not enough.

Latest-row/no-future-bar cases should not be treated as completed calibration evidence.

## 4. Forecast Inputs

Expected Monte Carlo forecast fields to extract from MC artifacts or packet context:

```text
model
horizon_bars
tp_first_probability
sl_first_probability
neither_probability
expected_R
mean_R
median_R
probability_of_profit
simulation_count
seed
entry
stop_loss
take_profit
ticker
timeframe
source_csv
created_at
```

Use flexible field matching because existing MC artifacts may use slightly different names.

## 5. Actual Outcome Inputs

Actual fields from `backtest_results_csv`:

```text
ticker
timeframe
source_csv
candidate_snapshot_file
signal_timestamp
signal_row_index
entry
stop_loss
take_profit
outcome
realized_R
bars_to_hit
tie_break_policy
horizon_bars
future_bars_available
signal_is_latest_row
neither_reason
backtest_success
outcome_error
```

## 6. Join Key Strategy

Preferred exact join:

```text
ticker + timeframe + candidate_snapshot_file
```

Secondary join:

```text
ticker + timeframe + source_csv + signal_row_index
```

Fallback join:

```text
ticker + timeframe + entry + stop_loss + take_profit + created time proximity
```

Rules:

- exact joins preferred
- ambiguous matches must be rejected
- no many-to-many silent joins
- every joined row must include a `join_method`
- every failed join should be reported

## 7. Future-Bar Eligibility

Eligible for forecast-vs-actual scoring only when:

```text
backtest_success = true
future_bars_available > 0
neither_reason != no_future_bars_available
```

Preferred stricter eligibility:

```text
future_bars_available >= horizon_bars
```

Rows with:

```text
signal_is_latest_row = true
neither_reason = no_future_bars_available
```

should be classified as:

```text
not_yet_mature
```

not forecast failure.

## 8. Outcome Encoding

Actual outcome categories:

```text
TP_FIRST
SL_FIRST
NEITHER
AMBIGUOUS
INVALID
```

For calibration:

- `TP_FIRST` maps to TP event
- `SL_FIRST` maps to SL event
- `NEITHER` maps to Neither event only if the future-bar window is sufficient
- `AMBIGUOUS` should be reviewed or excluded from strict scoring
- `INVALID` is excluded from scoring but counted

## 9. First Calibration Metrics

First metrics:

```text
sample_count
eligible_count
not_yet_mature_count
invalid_count
ambiguous_count
tp_actual_rate
sl_actual_rate
neither_actual_rate
mean_forecast_tp_probability
mean_forecast_sl_probability
mean_forecast_neither_probability
mean_realized_R
mean_forecast_expected_R
forecast_vs_actual_tp_error
forecast_vs_actual_sl_error
forecast_vs_actual_neither_error
brier_score_tp
brier_score_sl
brier_score_neither
```

Compare probabilities to binary outcomes.

Keep counts beside every rate.

Do not overinterpret small samples.

## 10. Grouping Dimensions

Recommended grouping:

```text
ticker
timeframe
model
horizon_bars
tie_break_policy
wyckoff_phase
wyckoff_event
trend
```

First grouping:

```text
ticker + timeframe + model + horizon_bars
```

## 11. Service Design

Future service:

```text
marketflow/services/monte_carlo_calibration_service.py
```

Potential functions:

```python
def read_monte_carlo_forecast_artifact(path: str | Path) -> dict[str, Any]:
    ...

def build_forecast_actual_join_rows(
    forecast_rows: list[dict[str, Any]],
    outcome_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    ...

def summarize_forecast_calibration_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ...

def summarize_monte_carlo_calibration_folder(report_dir: str | Path) -> dict[str, Any]:
    ...
```

Return shape idea:

```python
{
    "success": bool,
    "join_rows": [...],
    "summary_rows": [...],
    "grouped_summary_rows": [...],
    "unmatched_forecasts": [...],
    "unmatched_outcomes": [...],
    "warnings": [...],
    "errors": [...],
}
```

## 12. Artifact Design

Future markdown artifact:

```text
*_monte_carlo_calibration_summary_YYYYMMDD_HHMMSS.md
```

Potential artifact kind:

```text
monte_carlo_calibration_summary_md
```

Include:

- metadata
- source forecast files
- source outcome files
- join summary
- eligibility summary
- forecast-vs-actual metrics
- unmatched row review
- guardrails

## 13. Studio Location

Recommended future location:

```text
Strategy Ranking page, after Backtest Calibration Summary
```

Alternative future location:

```text
Generated Artifacts page
```

First UI should:

- list MC summary artifacts
- list backtest result artifacts
- show join preview
- show eligible/not-yet-mature counts
- save markdown summary

## 14. Guardrails

- calibration only
- not financial advice
- no trade signal
- no automatic parameter optimization
- forecasts need many samples
- not-yet-mature rows should not be judged as forecast failures
- model comparison requires same ticker/timeframe/horizon conditions
- Monte Carlo model assumptions must remain visible

## 15. Small Sample Policy

- fewer than 10 eligible rows: small sample
- fewer than 30 eligible rows: caution
- fewer than 100 eligible rows: directional only
- always show counts beside rates

## 16. Non-Goals

- no implementation in this checkpoint
- no Studio UI
- no markdown writer
- no model changes
- no optimization
- no new simulation engine
- no short setup support
- no external dependencies

## 17. Future Tests

Planned tests:

1. exact join by candidate snapshot file
2. join by source CSV and signal row
3. ambiguous join rejected
4. no-future-bars row marked not_yet_mature
5. full-horizon NEITHER eligible
6. TP_FIRST actual encoded correctly
7. SL_FIRST actual encoded correctly
8. Brier score computed for TP event
9. grouped summary by ticker/timeframe/model/horizon
10. unmatched forecasts reported
11. unmatched outcomes reported
12. no mutation of input rows

## 18. Recommended Next Implementation Task

```text
Next recommended task:
Implement service-only Monte Carlo forecast-vs-actual calibration join planning helpers after enough forecast/outcome artifact examples are available.
```

Final status:

```text
Status: Monte Carlo forecast-vs-actual calibration planning checkpoint only.
```
