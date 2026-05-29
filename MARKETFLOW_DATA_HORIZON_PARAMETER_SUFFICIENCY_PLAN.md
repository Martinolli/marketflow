# MARKETFLOW_DATA_HORIZON_PARAMETER_SUFFICIENCY_PLAN

## 1. Purpose

This plan defines how MarketFlow should assess whether available data is sufficient for the selected timeframe, Eigen/PCA window, Monte Carlo horizon, and Backtest Outcome horizon.

This is a planning-only checkpoint. It makes no code changes, changes no defaults, and adds no UI. The work described here is research/calibration only. It is not financial advice, not parameter optimization, and not a trade signal system.

Service status: service-only Data Horizon / Parameter Sufficiency Diagnostics implemented in `marketflow/services/data_sufficiency_service.py`. Studio UI remains future work.

Markdown artifact writer status: implemented service-level markdown generation and saving for Data Horizon / Parameter Sufficiency Diagnostics summaries.

Studio integration status: implemented as a Strategy Ranking page section that summarizes report-folder source CSV sufficiency and can write `data_sufficiency_summary_md` markdown artifacts.

Milestone status: `MARKETFLOW_DATA_SUFFICIENCY_MILESTONE_STATUS.md` records the current Studio-visible Data Horizon / Parameter Sufficiency workflow checkpoint.

Horizon alignment warning status: implemented in Studio as a non-blocking guardrail.

## 2. Current Baseline

Current implemented workflow:

```text
Strategy Ranking
→ Backtest Candidate Snapshot
→ Backtest Outcome Evaluation
→ Backtest Calibration Summary
→ Monte Carlo Forecast Calibration Summary
```

Current diagnostics already available:

- `future_bars_available`
- `evaluation_window_start_index`
- `evaluation_window_end_index`
- `signal_is_latest_row`
- `neither_reason`
- MC/backtest horizon mismatch detection in forecast calibration service

Current default timeframe periods from `marketflow/marketflow_data_parameters.py`:

```python
"timeframes": [
    {"interval": "1mo", "period": "5y"},
    {"interval": "1w", "period": "2y"},
    {"interval": "1d", "period": "365d"},
    {"interval": "4h", "period": "100d"},
    {"interval": "2h", "period": "60d"},
    {"interval": "1h", "period": "150d"},
    {"interval": "30m", "period": "20d"},
    {"interval": "15m", "period": "20d"},
    {"interval": "5m", "period": "20d"},
    {"interval": "1m", "period": "20d"}
]
```

## 3. Problem Statement

Data sufficiency matters because short periods may not provide enough rows for Eigen windows or stable Monte Carlo calibration. Latest-row candidates have no future bars, so a valid candidate can be unscoreable until future outcome bars exist. Historical forecast-vs-actual calibration needs both past candidate rows and future outcome windows.

Twenty calendar days of 15m/30m data may be enough for UI testing, but it is limited for robust calibration. Very low timeframes may add noise and provider-limit complications. One parameter set is not suitable for every timeframe.

## 4. Current Timeframe Configuration

| Timeframe | Current period | Notes                     |
| --------- | -------------- | ------------------------- |
| 1mo       | 5y             | long-term structure       |
| 1w        | 2y             | macro context             |
| 1d        | 365d           | daily tactical/strategic  |
| 4h        | 100d           | swing context             |
| 2h        | 60d            | tactical context          |
| 1h        | 150d           | tactical/intraday bridge  |
| 30m       | 20d            | intraday tactical         |
| 15m       | 20d            | intraday tactical/noisier |
| 5m        | 20d            | high noise / review       |
| 1m        | 20d            | very high noise / review  |

This checkpoint records the current configuration only. It does not recommend changing defaults yet.

## 5. Key Sufficiency Concepts

```text
rows_available
minimum_rows_required
analysis_window
forecast_horizon
backtest_horizon
future_bars_available
mature_outcome_window
provider_limit_risk
noise_risk
```

Sufficiency should be assessed at the artifact/data level, not only from configuration. A configured period may imply enough history, but the actual downloaded CSV may still be short, sparse, provider-limited, or missing enough future bars after a candidate signal row.

## 6. First Diagnostic Outputs

Future diagnostic fields:

```text
ticker
timeframe
source_csv
rows_available
first_timestamp
last_timestamp
configured_period
eigen_window
monte_carlo_horizon
backtest_horizon
minimum_rows_required
future_bars_available
bars_remaining_to_maturity
data_sufficiency_status
eigen_sufficiency_status
monte_carlo_sufficiency_status
backtest_sufficiency_status
calibration_sufficiency_status
provider_limit_warning
noise_warning
notes
```

## 7. Sufficiency Status Labels

```text
sufficient
limited
insufficient
provider_limited
not_yet_mature
unknown
```

Suggested meanings:

- `sufficient`: enough rows for selected analysis and calibration context
- `limited`: enough to run but weak for inference
- `insufficient`: not enough rows for selected parameters
- `provider_limited`: likely constrained by data provider history availability
- `not_yet_mature`: valid current candidate but no/insufficient future bars yet
- `unknown`: missing metadata or unreadable source

## 8. Minimum Row Logic

Recommended starting formula:

```text
minimum_rows_required =
max(
    eigen_window * 3,
    monte_carlo_horizon * 3,
    backtest_horizon * 3,
    100
)
```

For historical calibration / walk-forward later:

```text
minimum_rows_required =
lookback_window + forecast_horizon + safety_buffer
```

This is a first heuristic, not a mathematical law. Thresholds should be adjustable later. Intraday data may require higher minimums due to noise.

## 9. Timeframe-Specific Guidance

| Timeframe | Suggested diagnostic posture                             |
| --------- | -------------------------------------------------------- |
| 1mo       | macro only, low sample count                             |
| 1w        | macro trend/context, limited sample count                |
| 1d        | suitable for strategic/swing calibration if enough years |
| 4h        | useful for swing/tactical calibration                    |
| 2h        | tactical, watch sample size                              |
| 1h        | useful tactical/intraday bridge                          |
| 30m       | useful micro/tactical, noise caution                     |
| 15m       | useful micro/tactical, stronger noise caution            |
| 5m        | high noise, avoid for first calibration engine           |
| 1m        | very high noise, avoid for first calibration engine      |

## 10. Recommended Future Default Profiles

### Conservative Research Profile

```text
1mo: 10y if available
1w: 5y if available
1d: 2y–5y
4h: 180d–365d
2h: 120d–180d
1h: 180d–365d
30m: 30d–60d
15m: 30d–60d
5m: disabled or review only
1m: disabled or review only
```

### Fast Test Profile

```text
Keep current defaults or smaller for fast app testing.
```

### Intraday Research Profile

```text
Prioritize 1h, 30m, 15m.
Disable or down-rank 5m/1m until data quality is proven.
```

No profile is implemented in this checkpoint.

## 11. Relationship With Monte Carlo Calibration

- Monte Carlo forecast horizon must match Backtest Outcome horizon to be scoreable.
- MC calibration should reject or flag horizon mismatch.
- No-future-bars rows are not forecast failures.
- Partial future windows are not scoreable in the strict first implementation.
- Data Sufficiency Diagnostics should make these issues visible before calibration.

## 12. Relationship With Eigen/PCA

Eigen/PCA windows require enough rows. For example, Eigen window 80 on a dataset with only 90 rows is weak.

Future diagnostics should label:

- enough rows
- limited rows
- insufficient rows

Eigen results should include row-count context.

## 13. Relationship With Multi-Timeframe Analysis

Future relevance:

- macro timeframes: 1w, 1d, 4h
- micro timeframes: 1h, 30m, 15m
- 5m/1m are parked as high-noise review-only candidates
- Data sufficiency should support future Multi-Timeframe Wyckoff/Wave Alignment

No multi-timeframe service is implemented in this checkpoint.

## 14. Future Service Design

Future service:

```text
marketflow/services/data_sufficiency_service.py
```

Potential functions:

```python
def assess_csv_data_sufficiency(
    csv_path: str | Path,
    *,
    timeframe: str | None = None,
    configured_period: str | None = None,
    eigen_window: int | None = None,
    monte_carlo_horizon: int | None = None,
    backtest_horizon: int | None = None,
) -> dict[str, Any]:
    ...

def summarize_report_folder_data_sufficiency(
    report_dir: str | Path,
    *,
    parameter_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def build_timeframe_sufficiency_profile(
    timeframe: str,
    rows_available: int,
    parameter_context: dict[str, Any],
) -> dict[str, Any]:
    ...
```

Return shape idea:

```python
{
    "success": bool,
    "rows": [...],
    "summary": {...},
    "warnings": [...],
    "errors": [...],
}
```

## 15. Future Artifact Design

Future markdown artifact:

```text
*_data_sufficiency_summary_YYYYMMDD_HHMMSS.md
```

Potential artifact kind:

```text
data_sufficiency_summary_md
```

Include:

- metadata
- timeframe configuration
- CSV row-count table
- parameter sufficiency table
- warnings
- recommended review notes
- guardrails

## 16. Future Studio Location

Recommended location:

```text
Generated Artifacts / Data Quality section
```

Alternative:

```text
Strategy Ranking page before Backtest Candidate Snapshot
```

Recommended first UI:

- show source CSVs in report folder
- show rows available by timeframe
- show selected Eigen/MC/Backtest horizons
- show sufficiency status before running calibration

## 17. Guardrails

- Diagnostics only.
- No automatic parameter optimization.
- No trade recommendations.
- Low timeframe noise must remain visible.
- Provider limits must remain visible.
- Sufficient rows do not imply predictive validity.
- Insufficient rows should block or warn before scoreable calibration.
- No future data leakage.

## 18. Non-Goals

- No implementation in this checkpoint.
- No changes to defaults.
- No Studio UI.
- No artifact writer.
- No data provider changes.
- No Monte Carlo model changes.
- No Eigen/PCA changes.
- No parameter optimizer.
- No macro/micro forecast function.

## 19. Future Tests

Planned tests:

1. CSV with enough rows returns sufficient
2. CSV with low rows returns limited
3. CSV below minimum returns insufficient
4. missing timestamp handled safely
5. Eigen window larger than available rows returns insufficient
6. MC horizon larger than reasonable available rows returns limited/insufficient
7. backtest horizon mismatch flagged in context
8. report folder summary groups by timeframe
9. provider-limited warning for very low timeframes
10. no mutation of input context

## 20. Recommended Next Implementation Task

```text
Next recommended task:
Implement service-only `marketflow/services/data_sufficiency_service.py` to assess CSV row counts, timeframe coverage, and parameter sufficiency before adding Studio UI.
```

```text
Status: Data Horizon / Parameter Sufficiency Diagnostics planning checkpoint only.
```
