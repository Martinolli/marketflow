# MARKETFLOW_MONTE_CARLO_CALIBRATION_MILESTONE_STATUS

## 1. Purpose

This document records the current MarketFlow milestone/status after completing the Studio-visible Monte Carlo forecast-vs-actual calibration workflow.

This is a documentation-only checkpoint. It records the current repository and application status as a clean reference before future feature work. The workflow described here is for research/calibration only. It is not financial advice, not a trade signal system, and not parameter optimization.

## 2. Current Commit

```text
b786e39 - Add Studio Monte Carlo calibration summary section
```

## 3. Milestone Summary

Current end-to-end workflow:

```text
Strategy Ranking
→ Backtest Candidate Snapshot
→ Backtest Outcome Evaluation
→ Backtest Calibration Summary
→ Monte Carlo Forecast Calibration Summary
→ Generated Artifacts
```

This gives MarketFlow a complete UI-visible loop for joining probabilistic Monte Carlo forecasts to deterministic backtest outcome rows, then reviewing the joined calibration summary and saved markdown artifact through Generated Artifacts.

## 4. Implemented Workflow Components

### 4.1 Strategy Ranking and Candidate Snapshot

- Strategy Ranking selects candidates from canonical source CSVs.
- Selected candidates can be saved as `backtest_candidates_csv`.
- Candidate snapshots preserve entry, stop loss, take profit, source CSV, signal row, timestamp, and Wyckoff context when available.

### 4.2 Backtest Outcome Evaluation

- Candidate snapshots are evaluated deterministically against OHLC data.
- Results are saved as `backtest_results_csv`.
- Outcomes include:
  - `TP_FIRST`
  - `SL_FIRST`
  - `NEITHER`
  - `AMBIGUOUS`
  - `INVALID`
- Future-bar diagnostics are included:
  - `future_bars_available`
  - `evaluation_window_start_index`
  - `evaluation_window_end_index`
  - `signal_is_latest_row`
  - `neither_reason`

### 4.3 Backtest Calibration Summary

- Saved backtest result CSVs can be summarized.
- Markdown summaries can be generated.
- Files containing `_backtest_calibration_summary` are classified as `backtest_calibration_summary_md`.

### 4.4 Monte Carlo Join Metadata

- Newly generated `*_mc_summary.json` files include `join_metadata`.
- Metadata includes ticker, timeframe, source CSV, candidate snapshot file, signal row, signal timestamp, entry, stop loss, take profit, and join keys.
- Join keys include:
  - preferred key: ticker + timeframe + candidate snapshot file
  - secondary key: ticker + timeframe + source CSV + signal row index

### 4.5 Monte Carlo Forecast Calibration Service

- Enriched MC summaries can be joined to backtest result rows.
- Join methods include:
  - preferred
  - secondary
  - fallback levels
- Ambiguous or many-to-many joins are rejected.
- Eligibility blocks scoring for:
  - no future bars
  - partial future windows
  - horizon mismatch
  - invalid outcomes
  - ambiguous outcomes
- First calibration metrics are computed only for scoreable rows.

### 4.6 Monte Carlo Calibration Markdown Writer

- Monte Carlo calibration summaries can be saved as markdown.
- Files containing `_monte_carlo_calibration_summary` are classified as `monte_carlo_calibration_summary_md`.
- Markdown is previewable/downloadable through Generated Artifacts.

### 4.7 Studio Integration

- Strategy Ranking page now includes:
  - Backtest Candidate Snapshot
  - Backtest Outcome Evaluation
  - Backtest Calibration Summary
  - Monte Carlo Forecast Calibration Summary
- The Monte Carlo Forecast Calibration Summary section lists MC summary JSON artifacts and backtest result CSV artifacts, summarizes them, displays calibration/join tables, and can save markdown.

## 5. Current Artifact Types

| Artifact pattern                        | Kind                                 | Previewable                                 |
| --------------------------------------- | ------------------------------------ | ------------------------------------------- |
| `*_backtest_candidates*.csv`            | `backtest_candidates_csv`            | no                                          |
| `*_backtest_results*.csv`               | `backtest_results_csv`               | no                                          |
| `*_backtest_calibration_summary*.md`    | `backtest_calibration_summary_md`    | yes                                         |
| `*_mc_summary.json`                     | `mc_summary_json`                    | yes/no depending existing artifact behavior |
| `*_monte_carlo_calibration_summary*.md` | `monte_carlo_calibration_summary_md` | yes                                         |
| `*_candidate_decision_summary*.md`      | `candidate_decision_summary_md`      | yes                                         |
| `*_eigen_review_summary*.md`            | `eigen_review_summary_md`            | yes                                         |

Markdown calibration summaries are previewable. JSON MC summaries are primarily inspection/download data if the current artifact browser behavior does not preview them directly.

## 6. Current Test Baseline

```text
MC-focused tests: 38 passed, 3 warnings
Backtest-focused tests: 101 passed, 3 warnings
Full pytest: 245 passed, 2 skipped, 26 warnings
git diff --check: passed with LF-to-CRLF warnings only
```

The warnings/skips are known and non-blocking at this checkpoint. Full pytest is healthy. No service math was changed during Studio UI wiring.

## 7. Manual Verification Snapshot

```text
Report folder:
.marketflow\reports\2026-05-29\IONQ

Monte Carlo summary JSON artifacts found:
1

Backtest result CSV artifacts found:
1

Calibration result:
joined_count = 1
scoreable_count = 0
not_yet_mature_count = 1
horizon_mismatch_count = 1

Generated artifact:
*_monte_carlo_calibration_summary*.md

Artifact kind:
monte_carlo_calibration_summary_md

Previewable:
true
```

Calibration Summary rendered. Grouped Summary rendered. Join Rows rendered. The markdown preview contained Calibration Summary, Grouped Summary, Join Rows, and Guardrails. No Monte Carlo math, Backtest math, Strategy Ranking, P&F, or Eigen logic was changed in this UI step.

## 8. Current Guardrails

- Research/calibration only.
- Not financial advice.
- No broker integration.
- No buy/sell signals.
- No automatic parameter optimization.
- No-future-bar rows are not forecast failures.
- Horizon mismatches are not scoreable.
- Partial future windows are not scoreable in the first strict implementation.
- Small samples should not be overinterpreted.
- Comparisons should be made under similar ticker/timeframe/horizon conditions.

## 9. Known Limitations

- First Studio UI pass summarizes all matching MC/backtest artifacts in the current report folder.
- No multi-select/filtering yet.
- Most latest-row candidates remain not yet mature until future bars exist.
- Horizon mismatch can occur if Backtest Outcome Evaluation horizon and Monte Carlo horizon are configured differently.
- No probability bucket reporting yet.
- No historical walk-forward candidate generation yet.
- No Data Horizon / Sufficiency Diagnostics yet.
- No Multi-Timeframe Wyckoff/Wave Alignment service yet.
- No macro/micro forecast function yet.
- No parameter profile manager yet.
- No automated optimization.

## 10. Recommended Next Options

```text
A. Run broader app validation across additional tickers/timeframes.
B. Add Data Horizon / Parameter Sufficiency Diagnostics planning checkpoint.
C. Add multi-select/filtering for Monte Carlo calibration artifacts.
D. Plan Multi-Timeframe Wyckoff/Wave Alignment as a future feature.
E. Plan historical walk-forward candidate generation.
F. Pause feature work and do a repository/documentation cleanup pass.
```

Recommended next step:
B — create a Data Horizon / Parameter Sufficiency Diagnostics planning checkpoint, because timeframe periods, Eigen windows, MC horizons, and backtest horizons now directly affect calibration reliability.

## 11. Resume Checklist

```text
1. Pull latest main.
2. Confirm git status is clean.
3. Start Studio.
4. Load a known report folder.
5. Run Strategy Ranking.
6. Save Backtest Candidate Snapshot.
7. Run Backtest Outcome Evaluation.
8. Run Backtest Calibration Summary.
9. Run Monte Carlo from selected candidate.
10. Run Monte Carlo Forecast Calibration Summary.
11. Confirm Generated Artifacts shows monte_carlo_calibration_summary_md.
12. Review Calibration Summary, Grouped Summary, Join Rows, and Guardrails.
```

## 12. Future Advancement Parking Lot

Future planning topics, not part of the current implemented milestone:

```text
- Multi-Timeframe Wyckoff/Wave Alignment
- Macro/micro phase alignment
- FFT/wavelet-inspired signal features
- Markov-chain or regime-transition ideas
- Macro + micro forecast function
```

## 13. Final Status

```text
Status: MarketFlow Monte Carlo forecast calibration milestone documented.
```
