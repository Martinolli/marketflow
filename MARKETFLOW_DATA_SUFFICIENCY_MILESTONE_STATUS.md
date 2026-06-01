# MARKETFLOW_DATA_SUFFICIENCY_MILESTONE_STATUS

## 1. Purpose

This document records the current MarketFlow milestone/status after completing the Studio-visible Data Horizon / Parameter Sufficiency workflow.

This is a documentation-only checkpoint. It records the current repository and application status as a clean reference before future features. The workflow is diagnostics only and research/calibration only. It is not financial advice, not a trade signal system, and not parameter optimization.

## 2. Current Commit

```text
77787df - Add Studio data sufficiency section
```

## 3. Milestone Summary

Completed workflow:

```text
Data Sufficiency service
→ Data Sufficiency markdown writer
→ Studio Data Horizon / Parameter Sufficiency section
→ data_sufficiency_summary_md
→ Generated Artifacts preview
```

This gives MarketFlow a UI-visible diagnostic loop for checking whether report-folder source CSV data is sufficient for selected Eigen/PCA windows, Monte Carlo horizons, Backtest Outcome horizons, and calibration interpretation.

## 4. Implemented Workflow Components

### 4.1 Data Sufficiency Service

- Implemented in `marketflow/services/data_sufficiency_service.py`.
- Reads CSV artifacts.
- Counts rows.
- Detects timestamp columns.
- Infers ticker/timeframe from filenames.
- Applies configured-period fallback map.
- Calculates minimum row requirements.
- Classifies sufficiency.
- Surfaces low-timeframe/noise/provider warnings.
- Summarizes report folders.
- Prefers canonical `*_wyckoff_annotated.csv`.
- Ignores derivative CSVs such as:
  - `*_pv_eigen.csv`
  - `*_backtest_candidates*.csv`
  - `*_backtest_results*.csv`

### 4.2 Status Labels

Implemented labels:

```text
sufficient
limited
insufficient
provider_limited
not_yet_mature
unknown
```

- `sufficient`: enough rows for selected diagnostic context
- `limited`: enough to run but weak for inference
- `insufficient`: not enough rows for selected parameters
- `provider_limited`: likely constrained by provider/history availability
- `not_yet_mature`: valid current context but no/insufficient future bars
- `unknown`: missing/unreadable metadata or unavailable context

### 4.3 Minimum Row Logic

First heuristic:

```text
minimum_rows_required =
max(
    eigen_window * 3,
    monte_carlo_horizon * 3,
    backtest_horizon * 3,
    100
)
```

This is a heuristic only, not a mathematical law. Thresholds can be tuned later. Intraday data may require stronger caution due to noise.

### 4.4 Data Sufficiency Markdown Writer

- Implemented in `marketflow/services/data_sufficiency_artifact_service.py`.
- Builds preview-friendly markdown.
- Writes collision-safe files such as `IONQ_15m_data_sufficiency_summary_20260529_120000.md`.
- Provides `summarize_folder_to_data_sufficiency_markdown(...)`.
- Exports:
  - `DATA_SUFFICIENCY_SUMMARY_KIND`
  - filename builder
  - markdown builder
  - writer
  - folder convenience writer

### 4.5 Artifact Classification

Files containing `_data_sufficiency_summary` are classified as `data_sufficiency_summary_md`.

These files are previewable/downloadable through Generated Artifacts.

### 4.6 Studio Integration

- Implemented in `apps/marketflow_studio.py`.
- Added `Data Horizon / Parameter Sufficiency` section on the Strategy Ranking page.
- Location: after selected candidate JSON and before Backtest Candidate Snapshot.
- It uses:
  - `summarize_report_folder_data_sufficiency(...)`
  - `summarize_folder_to_data_sufficiency_markdown(...)`
- It displays:
  - compact status rows
  - Summary table
  - CSV Sufficiency Rows
  - Warning Review
  - service warnings/errors
- It can save `data_sufficiency_summary_md`.

## 5. Studio Workflow Position

Current Strategy Ranking flow:

```text
Strategy Ranking candidate selection
→ Data Horizon / Parameter Sufficiency
→ Backtest Candidate Snapshot
→ Backtest Outcome Evaluation
→ Backtest Calibration Summary
→ Monte Carlo Forecast Calibration Summary
```

Data Sufficiency is placed early because row-count and parameter risks should be visible before interpreting calibration outputs. Low-timeframe noise warnings should be visible before candidate/backtest interpretation, and the section helps prevent overconfidence in weak samples.

## 6. Current Controls

```text
Eigen/PCA window: default 80
Monte Carlo horizon bars: session value or 60
Backtest horizon bars: session value or 60
Save markdown data sufficiency summary: default checked
```

These controls do not change global defaults, do not optimize parameters, and only provide diagnostic context for the current report folder.

## 7. Current Artifact Types Added

| Artifact pattern                 | Kind                          | Previewable |
| -------------------------------- | ----------------------------- | ----------- |
| `*_data_sufficiency_summary*.md` | `data_sufficiency_summary_md` | yes         |

This complements existing markdown artifact kinds:

- `backtest_calibration_summary_md`
- `monte_carlo_calibration_summary_md`
- `candidate_decision_summary_md`
- `eigen_review_summary_md`

## 8. Current Test Baseline

```text
Data sufficiency focused tests: 29 passed, 3 warnings
Monte Carlo calibration focused tests: 38 passed, 3 warnings
Backtest focused tests: 101 passed, 3 warnings
Full pytest: 274 passed, 2 skipped, 26 warnings
git diff --check: passed with LF-to-CRLF warnings only
```

Warnings/skips are known and non-blocking at this checkpoint. Full pytest is healthy. No service math was changed during Studio UI wiring, and no timeframe defaults were changed.

## 9. Manual Verification Snapshot

```text
Report folder:
.marketflow\reports\2026-05-29\IONQ

Result:
canonical Wyckoff CSVs assessed
derivative CSVs ignored
5 rows assessed
15m warning = strong_noise_caution
30m warning = noise_caution
saved artifact kind = data_sufficiency_summary_md
previewable = true
downloadable = true
```

Browser smoke confirmed the section appears in the intended location. Markdown save works. Generated Artifacts preview guidance is shown. No Monte Carlo, Backtest, Strategy Ranking, P&F, or Eigen logic was changed.

Post-milestone implementation status: Studio horizon alignment warnings implemented between Backtest Outcome Evaluation and Monte Carlo.

Parameter Profile plan created at `MARKETFLOW_PARAMETER_PROFILE_PLAN.md`.

## 10. Current Guardrails

- diagnostics only
- research/calibration only
- not financial advice
- no broker integration
- no buy/sell signals
- no automatic parameter optimization
- sufficient data does not imply predictive validity
- low-timeframe noise must remain visible
- provider limitations must remain visible
- no future data leakage
- derivative CSVs should not be treated as primary source data for sufficiency checks

## 11. Known Limitations

- First Studio UI pass summarizes all eligible canonical source CSVs in the report folder.
- No artifact multi-select/filtering yet.
- No per-timeframe parameter profile manager yet.
- No persisted parameter profiles yet.
- No automatic synchronization between Backtest horizon and Monte Carlo horizon.
- No blocking behavior yet; the section warns but does not prevent calibration runs.
- No direct integration yet with Monte Carlo Forecast Calibration Summary.
- No historical walk-forward candidate generation yet.
- No Multi-Timeframe Wyckoff/Wave Alignment service yet.
- No macro/micro forecast function yet.
- No parameter optimization.

## 12. Recommended Next Options

```text
A. Run broader app validation across additional tickers/timeframes.
B. Add parameter profile planning/implementation for timeframe-specific defaults.
C. Add artifact multi-select/filtering for Data Sufficiency and Monte Carlo Calibration.
D. Add horizon alignment warning between Backtest Outcome Evaluation and Monte Carlo.
E. Plan historical walk-forward candidate generation.
F. Plan Multi-Timeframe Wyckoff/Wave Alignment as a future feature.
G. Pause feature work and do repository/documentation cleanup.
```

Recommended next step:
D — add horizon alignment warning between Backtest Outcome Evaluation and Monte Carlo, because horizon mismatch already affects scoreability in forecast-vs-actual calibration.

Alternative next step:
B — parameter profile planning/implementation if the priority is to standardize timeframe-specific defaults before adding more UI warnings.

## 13. Resume Checklist

```text
1. Pull latest main.
2. Confirm git status is clean.
3. Start Studio.
4. Load a known report folder.
5. Run Strategy Ranking.
6. Review selected candidate JSON.
7. Run Data Horizon / Parameter Sufficiency.
8. Confirm source CSV rows and warnings.
9. Save data_sufficiency_summary_md if needed.
10. Continue to Backtest Candidate Snapshot.
11. Run Backtest Outcome Evaluation.
12. Run Backtest Calibration Summary.
13. Run Monte Carlo from selected candidate.
14. Run Monte Carlo Forecast Calibration Summary.
15. Review Generated Artifacts.
```

## 14. Future Advancement Parking Lot

Future planning topics, not part of the current implemented milestone:

```text
- Parameter profile manager
- Timeframe-specific default profiles
- Data sufficiency blocking/warning gates
- Horizon alignment guardrails
- Historical walk-forward candidate generation
- Multi-Timeframe Wyckoff/Wave Alignment
- Macro/micro phase alignment
- FFT/wavelet-inspired signal features
- Markov-chain or regime-transition ideas
- Macro + micro forecast function
```

## 15. Final Status

```text
Status: MarketFlow Data Horizon / Parameter Sufficiency milestone documented.
```
