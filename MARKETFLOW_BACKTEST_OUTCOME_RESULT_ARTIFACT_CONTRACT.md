# MARKETFLOW_BACKTEST_OUTCOME_RESULT_ARTIFACT_CONTRACT

## 1. Purpose

This contract defines how deterministic backtest outcome results will be saved as CSV artifacts after evaluating candidate snapshots against OHLC data.

The artifact is for research and calibration only. It is not a trade signal engine, not financial advice, not Monte Carlo execution, not Strategy Ranking scoring, and not Studio UI. The first implementation should persist deterministic outcome rows only.

## 2. Current Baseline

Current implemented backtest pieces:

- candidate snapshots can be saved as `*_backtest_candidates*.csv`
- `*_backtest_candidates*.csv` files are classified as `backtest_candidates_csv`
- Studio can save the selected Strategy Ranking candidate as a candidate snapshot CSV
- the outcome engine can evaluate one candidate against OHLC data
- the backtest service wrapper returns JSON-safe outcome dictionaries

There is no outcome result artifact writer yet, no `backtest_results_csv` classification, no calibration summary, and no Backtest Lab UI.

## 3. Artifact Name

Planned filename pattern:

```text
{ticker}_{timeframe}_backtest_results_{YYYYMMDD_HHMMSS}.csv
```

Examples:

```text
LOAR_1d_backtest_results_20260526_160000.csv
IONQ_1w_backtest_results_20260526_160000.csv
```

Fallback:

```text
marketflow_backtest_results_{YYYYMMDD_HHMMSS}.csv
```

Rules:

- use safe filename parts only
- include a timestamp to avoid overwrite
- use a collision suffix fallback if needed
- save in the selected report folder or a future Backtest Lab output folder

## 4. Artifact Kind

Future artifact kind:

```text
backtest_results_csv
```

This should later be added to `marketflow/services/artifact_service.py`. Classification is not implemented in this planning checkpoint.

## 5. Input Sources

Possible future input sources:

1. One selected Strategy Ranking candidate snapshot
2. One `*_backtest_candidates*.csv`
3. A list of candidate snapshot results in memory
4. Future Backtest Lab candidate collection

Recommended first implementation input:

```text
Input: one or more saved candidate snapshot rows plus matching OHLC CSV data.
```

## 6. Required Columns

Required columns for `*_backtest_results.csv`, in order:

```text
created_at
ticker
timeframe
source_csv
source_report_dir
candidate_snapshot_file
signal_timestamp
signal_timestamp_source
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
direction
source_strategy_rank
candidate_validation_status
candidate_snapshot_success
outcome
bars_to_hit
realized_R
same_bar_hit
tie_break_policy
horizon_bars
hit_timestamp
hit_row_index
planned_rr
mark_to_market_close
outcome_error
backtest_success
```

## 7. Optional Future Columns

Optional future enrichment columns are not required for the first implementation:

```text
forecast_tp_first
forecast_sl_first
forecast_neither
forecast_R_mean
forecast_R_p50
forecast_R_p05
forecast_R_p95
mc_model
mc_paths
mc_horizon_bars
mc_block_len
mc_seed
pnf_gate
pnf_objective_quality
pnf_objective_direction
pnf_supports_trade
eigen_available
eigen_latest_residual
eigen_latest_coupling
eigen_recent_divergence_count
analyst_packet_version
manual_scenario
```

These are forecast, context, and grouping fields only. They must not affect deterministic outcome evaluation.

## 8. Data Types

Expected serialized types:

| Column | Type | Notes |
| ------ | ---- | ----- |
| `created_at` | string | Timestamp when the result row was written. |
| `ticker` | string | Candidate ticker if available. |
| `timeframe` | string | Candidate timeframe if available. |
| `source_csv` | string | OHLC/annotated CSV used for evaluation. |
| `source_report_dir` | string | Report folder or output folder if known. |
| `candidate_snapshot_file` | string | Source `*_backtest_candidates*.csv` filename when applicable. |
| `signal_timestamp` | string | Candidate signal timestamp, preserved as text. |
| `signal_timestamp_source` | string | Source timestamp field name. |
| `signal_row_index` | integer | Candidate decision row index. |
| `entry` | float | Frozen candidate entry/reference price. |
| `stop_loss` | float | Frozen candidate stop-loss level. |
| `take_profit` | float | Frozen candidate take-profit level. |
| `risk_reward` | float | Candidate risk/reward value if available. |
| `strategy_score` | float | Strategy Ranking score if available. |
| `wyckoff_phase` | string | Wyckoff phase label if available. |
| `wyckoff_event` | string | Wyckoff event label if available. |
| `trend` | string | Trend label if available. |
| `candidate_source` | string | Source of the candidate snapshot. |
| `report_date` | string | Report date if available. |
| `direction` | string | `long` for the current supported phase. |
| `source_strategy_rank` | integer | Strategy rank if known. |
| `candidate_validation_status` | string | Validation status from the candidate snapshot. |
| `candidate_snapshot_success` | boolean | True when the source snapshot was valid. |
| `outcome` | string enum | One of the supported outcome labels. |
| `bars_to_hit` | integer | Future bar count until TP/SL hit, if any. |
| `realized_R` | float | Outcome expressed in initial-risk units. |
| `same_bar_hit` | boolean | True when TP and SL were both touched in one OHLC bar. |
| `tie_break_policy` | string | Tie-break policy used for same-bar ambiguity. |
| `horizon_bars` | integer | Evaluation horizon setting. |
| `hit_timestamp` | string | Timestamp of first hit row, if any. |
| `hit_row_index` | integer | Row index of first hit row, if any. |
| `planned_rr` | float | Planned R used by the outcome engine. |
| `mark_to_market_close` | float | Horizon close used for `NEITHER`, if available. |
| `outcome_error` | string | Error text for invalid evaluation, if any. |
| `backtest_success` | boolean | True when `outcome != INVALID`. |

Outcome values:

```text
TP_FIRST
SL_FIRST
NEITHER
AMBIGUOUS
INVALID
```

## 9. Backtest Success Semantics

```text
backtest_success = true when outcome is not INVALID
backtest_success = false when outcome is INVALID
```

Clarifications:

- `NEITHER` is a valid outcome, not a failure
- `AMBIGUOUS` is valid evaluation but requires policy review
- invalid candidate snapshots should either be skipped or written as `INVALID`, depending on writer mode

## 10. Row-Level Contract

One CSV row equals one candidate snapshot evaluated against one OHLC data source.

Rules:

- do not mutate entry, stop loss, or take profit
- do not recompute Strategy Ranking fields
- do not run Monte Carlo
- do not join forecasts in the first implementation
- outcome evaluation starts after the signal row
- preserve tie-break policy
- preserve candidate validation status
- preserve source evidence

## 11. Candidate Snapshot Handling

Candidate row handling:

- valid snapshots can be evaluated
- missing signal location should produce `INVALID` outcome or be skipped based on mode
- missing source CSV should produce `INVALID` outcome or be skipped based on mode
- invalid levels should produce `INVALID`
- unsupported direction remains unsupported in the current long-only phase

Recommended first implementation mode:

```text
write_invalid_rows = true
```

This means invalid candidate snapshots are written with outcome `INVALID` and `backtest_success = false`.

## 12. Tie-Break Policy

Supported policies from the existing outcome engine:

```text
conservative
optimistic
open_proximity
unknown
```

Recommended default:

```text
conservative
```

Same-bar TP/SL ambiguity is unavoidable with OHLC data, so the selected policy must be saved in every result row.

## 13. Horizon Policy

```text
horizon_bars
```

Rules:

- required setting for evaluation
- stored in every result row
- future window starts after signal row
- no future rows before signal row may be used to create snapshot fields

## 14. Proposed Writer Service

Future file:

```text
marketflow/services/backtest_result_artifact_service.py
```

Planned functions:

```python
build_backtest_results_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> str

backtest_result_row(
    *,
    snapshot_row: dict[str, Any],
    outcome_result: dict[str, Any],
    candidate_snapshot_file: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]

write_backtest_results_csv(
    result_rows: list[dict[str, Any]],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
) -> dict[str, Any]
```

Return shape:

```python
{
    "success": bool,
    "path": str | None,
    "filename": str | None,
    "count": int,
    "success_count": int,
    "invalid_count": int,
    "errors": [...],
    "warnings": [...],
}
```

Do not implement this service as part of this contract checkpoint.

## 15. Proposed Evaluation Service

Future service or extension:

```text
marketflow/services/backtest_result_service.py
```

Possible functions:

```python
evaluate_candidate_snapshot_row(
    snapshot_row: dict[str, Any],
    *,
    horizon_bars: int = 20,
    tie_break_policy: str = "conservative",
) -> dict[str, Any]

evaluate_candidate_snapshot_csv(
    candidates_csv_path: str | Path,
    *,
    horizon_bars: int = 20,
    tie_break_policy: str = "conservative",
) -> dict[str, Any]
```

This should be implemented after the artifact contract is stable.

## 16. Artifact Browser Integration

Future `artifact_service.py` classification:

```text
*_backtest_results*.csv
```

should be classified as:

```text
backtest_results_csv
```

Preview and download:

- CSV preview can use existing CSV/artifact preview behavior if present
- download-only is acceptable initially

Do not implement artifact browser integration in this checkpoint.

## 17. Studio Integration Later

Future Studio flow:

1. User saves Backtest Candidate Snapshot.
2. User selects candidate snapshot CSV.
3. User chooses horizon bars and tie-break policy.
4. User clicks `Evaluate Backtest Outcomes`.
5. Studio writes `*_backtest_results.csv`.
6. Generated Artifacts shows `backtest_results_csv`.

No Studio UI should be added in this contract task.

## 18. Guardrails

- no Monte Carlo forecast join in the first result artifact
- no Strategy Ranking recomputation
- no future data used before signal row
- no automatic trade signal
- no broker integration
- no calibration scoring yet
- no optimization or parameter fitting
- all ambiguity must be explicit

## 19. Testing Plan For Future Implementation

Future tests should cover:

- filename generation with ticker/timeframe
- fallback filename
- row conversion for `TP_FIRST`
- row conversion for `SL_FIRST`
- row conversion for `NEITHER`
- row conversion for `AMBIGUOUS`
- row conversion for `INVALID`
- same-bar conservative policy preserved
- `horizon_bars` preserved
- write one result
- write multiple results
- invalid rows preserved
- collision suffix fallback
- artifact classification later

## 20. Non-Goals

- no Studio UI
- no calibration metrics
- no Monte Carlo forecast join
- no batch replay over many reports
- no repository cleanup
- no short setup support yet

## 21. Recommended Next Implementation Task

Next recommended task:
Implement `marketflow/services/backtest_result_artifact_service.py` for filename generation, result row conversion, and CSV writing, with tests. No Studio UI yet.

Status: outcome result artifact contract planning checkpoint only.
