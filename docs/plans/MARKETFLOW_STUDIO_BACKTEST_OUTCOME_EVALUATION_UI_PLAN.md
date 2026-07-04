# MARKETFLOW_STUDIO_BACKTEST_OUTCOME_EVALUATION_UI_PLAN

## 1. Purpose

This plan defines a Studio UI control for evaluating saved Backtest Candidate Snapshot CSV artifacts against referenced OHLC source CSV data to produce deterministic Backtest Outcome Result CSV artifacts.

This is research and calibration only. It is not a trade signal, not financial advice, not broker execution, not Monte Carlo, not optimization, and not the full Backtest Lab.

## 2. Current Service Baseline

Implemented baseline:

- Studio can save selected Strategy Ranking candidates as `*_backtest_candidates*.csv`.
- `*_backtest_candidates*.csv` files are classified as `backtest_candidates_csv`.
- `marketflow/services/backtest_result_artifact_service.py` writes `*_backtest_results.csv`.
- `*_backtest_results*.csv` files are classified as `backtest_results_csv`.
- `marketflow/services/backtest_result_service.py` evaluates saved candidate snapshot CSVs into result CSVs.
- Studio now includes a `Backtest Outcome Evaluation` section for running the outcome evaluation service.

Implementation status: Studio now includes a `Backtest Outcome Evaluation` section on the Strategy Ranking page. It evaluates saved `backtest_candidates_csv` artifacts through `evaluate_candidate_snapshot_csv_to_results_csv(...)` and writes `backtest_results_csv` artifacts.

## 3. Proposed Studio Location

Recommended location: Strategy Ranking page, near the existing Backtest Candidate Snapshot section.

Alternative location: Generated Artifacts page, near a selected candidate snapshot CSV.

Recommended first implementation: add the control to Strategy Ranking after Backtest Candidate Snapshot. This keeps the workflow linear: candidate selection -> save candidate snapshot -> evaluate outcome later.

## 4. UI Section Name

Use:

```text
Backtest Outcome Evaluation
```

Description:

```text
Evaluate saved Backtest Candidate Snapshot CSV artifacts against their referenced OHLC source CSVs. This is a deterministic research/calibration step and does not create a trade signal.
```

## 5. Inputs

1. Candidate snapshot CSV selector

- Filter artifacts where `kind == backtest_candidates_csv`.
- Show filename and path.
- Default to latest saved candidate snapshot if available.

2. Horizon bars

- Integer.
- Default `20`.
- Minimum `1`.
- Reasonable max `500`.

3. Tie-break policy

- Selectbox values:
  - `conservative`
  - `optimistic`
  - `open_proximity`
  - `unknown`
- Default `conservative`.

4. Write invalid rows

- Checkbox.
- Default true.
- Help text: `When enabled, invalid/incomplete candidate snapshots are preserved as INVALID rows for audit.`

5. Output folder

- Default current report folder.
- No freeform path in first implementation unless an existing Studio pattern supports it.

## 6. Pre-run Preview

Before running, show:

- selected candidate snapshot file
- number of candidate rows if quick read succeeds
- warning if file cannot be read
- guardrail text
- expected output kind: `backtest_results_csv`

## 7. Run Button

Button label:

```text
Evaluate Backtest Outcomes
```

On click:

- call `evaluate_candidate_snapshot_csv_to_results_csv(...)`
- use selected candidate snapshot CSV path
- use selected horizon bars
- use selected tie-break policy
- use write invalid rows setting
- output to current report folder
- store result in session state:
  - `latest_backtest_outcome_evaluation`
  - `latest_backtest_results_csv`

## 8. Post-run Summary

After run, display:

- success/failure
- result filename
- result path
- count
- evaluated_count
- success_count
- invalid_count
- skipped_count
- errors
- warnings

If result CSV exists:

- show note: `Saved file appears in Generated Artifacts as backtest_results_csv.`
- optionally provide a download button using the existing artifact/download pattern if simple

## 9. Guardrails

Required UI wording:

- deterministic outcome evaluation only
- uses frozen candidate levels
- does not recompute Strategy Ranking
- does not run Monte Carlo
- does not optimize parameters
- does not make trade recommendations
- same-bar ambiguity follows selected tie-break policy
- invalid rows can be preserved for audit

## 10. Error Handling

Expected behavior:

- no candidate CSV found: show info message
- candidate CSV unreadable: show error
- no result rows produced: show warning
- missing `source_csv`: invalid result row if write invalid rows enabled
- missing signal location: invalid result row if write invalid rows enabled
- missing OHLC source file: invalid result row
- service exception: show error and do not crash page

## 11. Generated Artifacts Integration

After successful write:

- result CSV should be visible as `backtest_results_csv`
- no new artifact classification is needed
- no CSV preview changes in first implementation

## 12. Session State

Use keys:

```text
latest_backtest_outcome_evaluation
latest_backtest_results_csv
```

Selector key examples:

```text
backtest_outcome_candidate_csv
backtest_outcome_horizon_bars
backtest_outcome_tie_break_policy
backtest_outcome_write_invalid_rows
```

Avoid reusing Charts or Strategy Ranking keys.

## 13. Non-Goals

- no Backtest Lab page
- no calibration metrics
- no Monte Carlo forecast-vs-actual join
- no strategy optimization
- no broker integration
- no automatic candidate creation
- no CSV preview change
- no short setup support yet

## 14. Verification Plan For Future Implementation

Manual flow:

1. Run/load ticker report.
2. Select Strategy Ranking candidate.
3. Save Backtest Candidate Snapshot.
4. Confirm candidate CSV appears as `backtest_candidates_csv`.
5. Select candidate CSV in Backtest Outcome Evaluation section.
6. Set horizon bars.
7. Select tie-break policy.
8. Click `Evaluate Backtest Outcomes`.
9. Confirm `*_backtest_results.csv` is written.
10. Confirm Generated Artifacts classifies it as `backtest_results_csv`.
11. Confirm counts and errors/warnings display.
12. Confirm no Monte Carlo/Analyst Packet/P&F/Eigen logic changed.

## 15. Testing Plan For Future Implementation

Add or update tests only if UI helper functions are introduced.

Quality checks for future implementation:

```powershell
python -m py_compile apps\marketflow_studio.py marketflow\services\backtest_result_service.py
python -m pytest tests\test_backtest_result_service.py tests\test_backtest_result_artifact_service.py tests\test_backtest_candidate_artifact_service.py tests\test_backtest_candidate_service.py tests\test_backtest_service.py tests\test_backtesting_outcome_engine.py -q
python -m pytest -q
git diff --check
```

## 16. Recommended Next Implementation Task

Next recommended task:
Implement the Studio Backtest Outcome Evaluation section on the Strategy Ranking page using `evaluate_candidate_snapshot_csv_to_results_csv(...)`.

Status: Studio backtest outcome evaluation UI implemented on the Strategy Ranking page.
