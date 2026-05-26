# MARKETFLOW_BACKTEST_CANDIDATE_ARTIFACT_CONTRACT

## 1. Purpose

This contract defines how validated candidate snapshots will be saved as CSV artifacts for later deterministic backtesting and Monte Carlo calibration.

The artifact is for research and calibration only. It is not a trade signal engine, not financial advice, not Studio UI, and not backtest result generation. The first implementation should only persist frozen candidate snapshot rows and their validation state.

## 2. Current Baseline

The current backtest foundation includes:

- deterministic outcome evaluation in `marketflow/backtesting/outcome_engine.py`
- JSON-safe evaluation wrappers in `marketflow/services/backtest_service.py`
- candidate snapshot normalization and validation in `marketflow/services/backtest_candidate_service.py`
- `CandidateSnapshot` and `OutcomeResult` dataclasses in `marketflow/backtesting/schemas.py`

There is no candidate snapshot artifact writing yet, no artifact classification for backtest candidate CSVs, and no Studio integration.

## 3. Artifact Name

Planned filename pattern:

```text
{ticker}_{timeframe}_backtest_candidates_{YYYYMMDD_HHMMSS}.csv
```

Examples:

```text
LOAR_1d_backtest_candidates_20260526_151500.csv
IONQ_1w_backtest_candidates_20260526_151500.csv
```

Fallback:

```text
marketflow_backtest_candidates_{YYYYMMDD_HHMMSS}.csv
```

Rules:

- use safe filename parts only
- include a timestamp to avoid overwrite
- use a collision suffix fallback if a path already exists
- save in the selected report folder when available

## 4. Artifact Kind

Future artifact kind:

```text
backtest_candidates_csv
```

This should later be added to `marketflow/services/artifact_service.py`. Classification is not implemented in this planning checkpoint.

## 5. Required Columns

Required columns for `*_backtest_candidates.csv`, in order:

```text
created_at
ticker
timeframe
source_csv
source_report_dir
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
validation_status
validation_errors
validation_warnings
snapshot_success
```

## 6. Optional Future Columns

Optional future enrichment columns are not required for the first implementation:

```text
pnf_gate
pnf_objective_quality
pnf_objective_direction
pnf_supports_trade
mc_model
mc_paths
mc_horizon_bars
mc_pop_tp_first
mc_p_sl_first
mc_p_neither
eigen_available
eigen_latest_residual
eigen_latest_coupling
eigen_recent_divergence_count
analyst_packet_version
manual_scenario
```

Optional fields are grouping and context fields only. They must not affect deterministic outcome evaluation.

## 7. Data Types

Expected serialized types:

| Column | Type | Notes |
| ------ | ---- | ----- |
| `created_at` | string | ISO-like local timestamp or UTC timestamp; preserve as text in CSV. |
| `ticker` | string | Safe display ticker if available. |
| `timeframe` | string | Examples: `1d`, `1w`, `4h`. |
| `source_csv` | string | Original selected CSV path or filename. |
| `source_report_dir` | string | Report directory path if known. |
| `signal_timestamp` | string | Original candidate timestamp where possible. |
| `signal_timestamp_source` | string | Source field such as `timestamp`, `datetime`, or `date`. |
| `signal_row_index` | integer | Row index where the candidate was available. |
| `entry` | float | Frozen candidate entry/reference price. |
| `stop_loss` | float | Frozen candidate stop-loss level. |
| `take_profit` | float | Frozen candidate take-profit level. |
| `risk_reward` | float | Preserved or computed during normalization, not during CSV writing. |
| `strategy_score` | float | Strategy Ranking score if available. |
| `wyckoff_phase` | string | Wyckoff phase label if available. |
| `wyckoff_event` | string | Wyckoff event label if available. |
| `trend` | string | Trend label if available. |
| `candidate_source` | string | Usually `strategy_ranking` for Phase 2. |
| `report_date` | string | Report date if available. |
| `direction` | string | `long` for the current supported phase. |
| `source_strategy_rank` | integer | Source rank if known. |
| `validation_status` | string | One of the defined validation status values. |
| `validation_errors` | string | Semicolon-separated validation errors. |
| `validation_warnings` | string | Semicolon-separated validation warnings. |
| `snapshot_success` | boolean | True only when `validation_status == valid`. |

For Phase 2.2, use semicolon-separated strings for `validation_errors` and `validation_warnings` because they are readable in plain CSV tools.

Example:

```text
Missing source_csv.; Missing signal_row_index or signal_timestamp.
```

## 8. Snapshot Success Semantics

```text
snapshot_success = true when validation_status == valid
snapshot_success = false otherwise
```

Invalid or incomplete snapshots may still be saved for audit. Later outcome evaluation should skip them or mark them invalid rather than attempting a deterministic outcome.

## 9. Validation Status Values

Current validation statuses:

```text
valid
missing_source_csv
missing_levels
missing_signal_location
invalid_levels
unsupported_direction
```

Meanings:

- `valid`: Snapshot has source CSV, levels, supported direction, and signal location.
- `missing_source_csv`: Snapshot does not identify the CSV data used for the candidate.
- `missing_levels`: Entry, stop loss, or take profit is missing or non-numeric.
- `missing_signal_location`: Neither signal row index nor signal timestamp is available.
- `invalid_levels`: Long setup levels are invalid; expected `stop_loss < entry < take_profit`.
- `unsupported_direction`: Direction is not supported by the current long-only phase.

## 10. Row-Level Contract

One CSV row equals one frozen candidate snapshot.

Rules:

- do not mutate entry, stop loss, or take profit during writing
- do not recompute levels during writing
- do not evaluate outcome during writing
- do not join Monte Carlo forecasts during initial artifact writing
- preserve validation status
- preserve source evidence

## 11. Multiple Candidate Behavior

Future writer behavior:

- accepts one snapshot or a list of snapshots
- normalizes and validates each row if needed
- writes all rows
- returns count, valid count, and invalid count
- does not fail the whole file because one snapshot is invalid
- file-level success means the file was written, not that all snapshots were valid

## 12. Proposed Writer Service

Recommended future file:

```text
marketflow/services/backtest_candidate_artifact_service.py
```

This should be a separate service instead of extending `marketflow/services/backtest_candidate_service.py`, because normalization and validation should remain independent from file output and artifact concerns.

Planned functions:

```python
build_backtest_candidates_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> str

candidate_snapshot_row(
    snapshot_result: dict[str, Any],
    *,
    created_at: str | None = None,
) -> dict[str, Any]

write_backtest_candidates_csv(
    snapshot_results: list[dict[str, Any]],
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
    "valid_count": int,
    "invalid_count": int,
    "errors": [...],
    "warnings": [...],
}
```

This is planned only. Do not implement it as part of this checkpoint.

## 13. Artifact Browser Integration

Future `artifact_service.py` classification:

```text
*_backtest_candidates*.csv
```

should be classified as:

```text
backtest_candidates_csv
```

Preview and download:

- CSV preview can use existing CSV/artifact preview behavior if present
- otherwise download-only is acceptable initially

Do not implement artifact browser integration in this checkpoint.

## 14. Studio Integration Later

Future Studio flow:

1. User selects Strategy Ranking candidate.
2. Studio builds candidate snapshot.
3. Studio shows validation status.
4. User clicks `Save Backtest Candidate Snapshot`.
5. CSV artifact appears in Generated Artifacts.

No Studio UI should be added in the artifact contract task.

## 15. Guardrails

- no outcome evaluation during snapshot writing
- no Monte Carlo forecast join
- no future rows used
- no automatic trade signal
- invalid snapshots saved only for audit
- signal location required for later valid outcome evaluation

## 16. Testing Plan For Future Implementation

Future tests should cover:

- filename generation with ticker/timeframe
- fallback filename
- row conversion from valid snapshot result
- row conversion from invalid snapshot result
- semicolon serialization of validation errors/warnings
- write one snapshot
- write multiple snapshots
- valid_count / invalid_count
- collision suffix fallback
- artifact classification later

## 17. Non-Goals

- no Studio UI
- no outcome evaluation
- no calibration metrics
- no Monte Carlo forecast join
- no batch replay over history
- no cleanup of deprecated repo files

## 18. Recommended Next Implementation Task

Next recommended task:
Implement `marketflow/services/backtest_candidate_artifact_service.py` for filename generation, row conversion, and CSV writing, with tests. No Studio UI yet.

Status: artifact contract planning checkpoint only.
