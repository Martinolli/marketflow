# MARKETFLOW_BACKTEST_CALIBRATION_MILESTONE_STATUS

## 1. Purpose

This document records the current milestone/status after completing the Studio-visible backtest calibration workflow.

This is a documentation-only checkpoint. It records the current repository and app status as a clean reference before future features are added.

This workflow is research/calibration only. It is not financial advice and is not a trade signal system.

## 2. Current Commit

```text
6d5dfd4 - Add Studio backtest calibration summary section
```

## 3. Milestone Summary

The current end-to-end workflow is:

```text
Strategy Ranking
→ Backtest Candidate Snapshot
→ Backtest Outcome Evaluation
→ Backtest Calibration Summary
→ Generated Artifacts
```

This gives the project a complete UI-visible loop for deterministic backtest research/calibration.

## 4. Implemented Workflow Components

### 4.1 Strategy Ranking Source Hygiene

Strategy Ranking now prefers canonical `*_wyckoff_annotated.csv` source files.

Generated derivative CSVs are avoided by default. Ignored derivatives include:

- `*_pv_eigen.csv`
- `*_backtest_candidates*.csv`
- `*_backtest_results*.csv`

### 4.2 Candidate Snapshot Layer

Selected Strategy Ranking candidates can be saved as `*_backtest_candidates*.csv`.

These files are classified as `backtest_candidates_csv`.

Snapshots are enriched with signal row/timestamp evidence when the source CSV supports it. Latest-row fallback is used because Strategy Ranking is latest-row derived. Enrichment warnings remain visible.

### 4.3 Backtest Outcome Evaluation

Saved candidate snapshots can be evaluated against referenced OHLC CSVs.

Deterministic outcome results are written as `*_backtest_results*.csv`.

These files are classified as `backtest_results_csv`.

Outcomes include:

- `TP_FIRST`
- `SL_FIRST`
- `NEITHER`
- `AMBIGUOUS`
- `INVALID`

This remains long-only and research/calibration only.

### 4.4 Calibration Summary Service

Saved `backtest_results_csv` artifacts can be summarized.

The service computes global summary metrics, grouped summary metrics, and invalid reason summaries.

### 4.5 Calibration Markdown Artifact Writer

Calibration summaries can be saved as markdown.

Filenames contain `_backtest_calibration_summary`.

Files are classified as `backtest_calibration_summary_md`.

Markdown is previewable/downloadable through Generated Artifacts.

### 4.6 Studio Integration

The Strategy Ranking page includes:

- Backtest Candidate Snapshot
- Backtest Outcome Evaluation
- Backtest Calibration Summary

Calibration Summary lists result CSVs, summarizes them, and optionally saves markdown.

## 5. Current Artifact Types

| Artifact pattern                     | Kind                              | Previewable |
| ------------------------------------ | --------------------------------- | ----------- |
| `*_backtest_candidates*.csv`         | `backtest_candidates_csv`         | no          |
| `*_backtest_results*.csv`            | `backtest_results_csv`            | no          |
| `*_backtest_calibration_summary*.md` | `backtest_calibration_summary_md` | yes         |
| `*_candidate_decision_summary*.md`   | `candidate_decision_summary_md`   | yes         |
| `*_eigen_review_summary*.md`         | `eigen_review_summary_md`         | yes         |

## 6. Current Test Baseline

```text
Focused tests: 103 passed, 3 warnings
Full pytest: 198 passed, 2 skipped, 26 warnings
git diff --check: passed with CRLF normalization warnings only
```

Warnings/skips are known and non-blocking at this checkpoint.

The pass count increased because new calibration tests were added.

Full pytest is healthy.

## 7. Manual Verification Snapshot

```text
Report folder:
.marketflow\reports\2026-05-27\AAPL

Backtest result artifacts found:
2

Generated calibration summary:
AAPL_1d_backtest_calibration_summary_20260528_104518.md

Artifact kind:
backtest_calibration_summary_md

Previewable:
true

Downloadable:
true
```

Global Summary rendered.

Grouped Summary rendered.

Invalid Row Review rendered.

No Monte Carlo, Strategy Ranking, P&F, Eigen, or backtest math was changed in the Studio calibration UI step.

## 8. Current Guardrails

- research/calibration only
- not financial advice
- no broker integration
- no automatic optimization
- no buy/sell signals
- deterministic outcomes depend on saved historical data
- small samples should not be overinterpreted
- same-bar ambiguity depends on tie-break policy
- calibration summaries do not rerun backtests
- calibration summaries do not run Monte Carlo

## 9. Known Limitations

Post-milestone improvement: future-bar availability diagnostics were added after this milestone to make `NEITHER` outcomes easier to interpret.

Future planning status: Monte Carlo forecast-vs-actual calibration is planned in `MARKETFLOW_MONTE_CARLO_FORECAST_CALIBRATION_PLAN.md`.

- Backtest Outcome Evaluation is long-only
- Calibration Summary currently summarizes all `backtest_results_csv` files in current report folder
- no multi-select yet
- no Backtest Lab UI yet
- no Monte Carlo forecast-vs-actual join yet
- no parameter profile manager yet
- no automated optimization yet
- CSV result artifacts are downloadable but not previewed as tables in Generated Artifacts
- latest-row fallback should be revisited if Strategy Ranking stops being latest-row derived

## 10. Recommended Next Options

```text
A. Run broader app validation across AAAU/AAPL/AI/LOAR.
B. Add multi-select support for choosing which backtest_results_csv files to summarize.
C. Plan Monte Carlo forecast-vs-actual calibration join.
D. Add a Parameter Profile planning checkpoint.
E. Pause feature work and do a repository/documentation cleanup pass.
```

Recommended next step:

```text
A — run broader app validation across AAAU/AAPL/AI/LOAR, then decide between multi-select support and Monte Carlo forecast-vs-actual calibration.
```

## 11. Resume Checklist

```text
1. Pull latest main.
2. Confirm git status is clean.
3. Start Studio.
4. Load one known report folder.
5. Run Strategy Ranking.
6. Save Backtest Candidate Snapshot.
7. Run Backtest Outcome Evaluation.
8. Run Backtest Calibration Summary.
9. Confirm Generated Artifacts shows backtest_calibration_summary_md.
10. Review Global Summary, Grouped Summary, and Invalid Row Review.
```

## 12. Final Status

```text
Status: MarketFlow backtest calibration milestone documented.
```
