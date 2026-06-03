# MARKETFLOW_PARAMETER_PROFILE_MILESTONE_STATUS

## 1. Purpose

This document records the current MarketFlow milestone/status after completing the Studio-visible Parameter Profile workflow.

This is a documentation-only checkpoint. It records the current repository and application status as a clean reference before future features. Parameter profiles are standardization helpers for research/calibration workflows. They are not optimization, not financial advice, and not a trade signal system.

Validation status: `MARKETFLOW_PROFILE_VALIDATION_SUMMARY_20260602.md` records the first validation run across AAPL, IONQ, AAAU, and LOAR using the Studio Parameter Profile Selector.

Related plan: `MARKETFLOW_HISTORICAL_WALK_FORWARD_VALIDATION_PLAN.md` defines the proposed historical walk-forward validation approach after the first profile validation run.

## 2. Current Commit

```text
b506c05 - Add Studio parameter profile selector
```

## 3. Milestone Summary

Completed workflow:

```text
Parameter Profile plan
→ Parameter Profile service
→ Studio Parameter Profile Selector
→ session controls for Data Sufficiency, Backtest Outcome, and Monte Carlo
```

This gives MarketFlow a controlled way to standardize key windows and horizons before running Data Sufficiency, Backtest Outcome Evaluation, Monte Carlo, and forecast-vs-actual calibration.

## 4. Implemented Workflow Components

### 4.1 Parameter Profile Plan

- Planning document exists at `MARKETFLOW_PARAMETER_PROFILE_PLAN.md`.
- It defines the purpose, guardrails, future profile structure, future service design, and future UI direction.

### 4.2 Parameter Profile Service

- Implemented in `marketflow/services/parameter_profile_service.py`.
- Provides built-in profiles.
- Provides validation.
- Provides timeframe posture checks.
- Provides parameter context for Data Sufficiency.
- Provides session update payloads for future/current Studio UI.
- Does not import Streamlit.
- Does not optimize parameters automatically.

### 4.3 Built-in Profiles

```text
fast_test
daily_swing
intraday_tactical
conservative_research
low_timeframe_review
```

- `fast_test`: quick runtime/app validation.
- `daily_swing`: 1d/4h swing-oriented analysis.
- `intraday_tactical`: 1h/30m/15m tactical analysis.
- `conservative_research`: slower broader research/calibration review.
- `low_timeframe_review`: 5m/1m exploratory visual review only.

### 4.4 Profile Validation

- Required fields are checked.
- Numeric fields must be positive.
- Unsupported timeframe posture values are rejected.
- Built-in calibration profiles must keep:

```text
monte_carlo_horizon == backtest_horizon
```

- Horizon mismatch inside a profile is treated as a validation error.

### 4.5 Timeframe Posture

Posture labels:

```text
preferred
allowed
caution
review_only
avoid
```

- `preferred`: profile is designed for this timeframe.
- `allowed`: usable with context.
- `caution`: usable but requires careful review.
- `review_only`: diagnostic/visual review only.
- `avoid`: not recommended for this profile.

### 4.6 Studio Integration

- Implemented in `apps/marketflow_studio.py`.
- Added `Parameter Profile Selector` on the Strategy Ranking page.
- Location: after selected candidate JSON and before Data Horizon / Parameter Sufficiency.
- The selector can apply profile values to current session controls.
- It shows profile summary/status rows.
- It shows selected candidate timeframe posture.
- Users can still manually override controls after applying a profile.

## 5. Studio Workflow Position

Current Strategy Ranking flow:

```text
Strategy Ranking candidate selection
→ Parameter Profile Selector
→ Data Horizon / Parameter Sufficiency
→ Backtest Candidate Snapshot
→ Backtest Outcome Evaluation
→ Backtest Calibration Summary
→ Monte Carlo Forecast Calibration Summary
```

The Parameter Profile Selector is placed early because profile values should be applied before sufficiency checks, horizon alignment should be established before backtest/Monte Carlo interpretation, and profile application helps reduce manual mismatch risk.

## 6. Session Keys Updated by Profiles

```text
data_sufficiency_eigen_window
data_sufficiency_backtest_horizon
data_sufficiency_monte_carlo_horizon
backtest_outcome_horizon_bars
monte_carlo_horizon_bars
monte_carlo_paths
monte_carlo_block_len
```

These are session-level values only. Global defaults are not changed, and users can override them manually.

## 7. Implemented Profile Values

| Profile                   | Eigen window | Backtest horizon | MC horizon | MC paths | Block length | Main posture      |
| ------------------------- | -----------: | ---------------: | ---------: | -------: | -----------: | ----------------- |
| Fast Test                 |           40 |               20 |         20 |    10000 |            8 | quick validation  |
| Daily / Swing             |           80 |               20 |         20 |    30000 |           10 | 1d/4h             |
| Intraday Tactical         |           80 |               60 |         60 |    30000 |           12 | 1h/30m/15m        |
| Conservative Research     |          120 |               60 |         60 |    50000 |           16 | broader research  |
| Review-Only Low-Timeframe |           40 |               20 |         20 |    10000 |            8 | 5m/1m review only |

## 8. Horizon Alignment Rule

```text
For forecast-vs-actual calibration:
Monte Carlo horizon should equal Backtest Outcome horizon.
```

All built-in profiles follow this rule. Studio already warns if horizons diverge, and profile application should normally produce aligned horizons.

## 9. Relationship With Data Sufficiency

Profiles populate Data Sufficiency controls. Data Sufficiency still assesses whether the selected profile fits the available rows, profile selection does not bypass Data Sufficiency warnings, and sufficient data does not imply predictive validity.

## 10. Current Test Baseline

```text
Parameter Profile tests: 18 passed, 3 warnings
Data Sufficiency focused tests: 29 passed, 3 warnings
Monte Carlo focused tests: 38 passed, 3 warnings
Backtest focused tests: 101 passed, 3 warnings
Full pytest: 292 passed, 2 skipped, 26 warnings
git diff --check: passed with LF-to-CRLF warnings only
```

Warnings/skips are known and non-blocking at this checkpoint. Full pytest is healthy. No service math was changed during Studio UI wiring, and no timeframe defaults were changed.

## 11. Manual Verification Snapshot

```text
Studio:
http://localhost:8506

Selector location:
Strategy Ranking page after selected candidate JSON and before Data Horizon / Parameter Sufficiency

Intraday Tactical applied:
Data Sufficiency = 80 / 60 / 60
Monte Carlo paths = 30000
Monte Carlo horizon = 60
Monte Carlo block length = 12

Daily / Swing applied:
Horizons = 20 / 20
Paths = 30000
Block length = 10

Horizon alignment:
aligned caption shown after profile application
```

No Streamlit warnings were emitted during the smoke check. Users can still manually override values. No Monte Carlo, Backtest, Strategy Ranking, P&F, or Eigen logic was changed.

## 12. Current Guardrails

- profile selection is not optimization
- profile selection does not generate buy/sell signals
- profile selection does not guarantee predictive performance
- user can still override parameters
- horizon mismatch warning remains active
- Data Sufficiency must still evaluate whether profile values fit available rows
- no future leakage
- low-timeframe noise caution remains visible
- global defaults are not changed

## 13. Known Limitations

- Selector currently appears only on Strategy Ranking page.
- Selector is not duplicated on Monte Carlo tab.
- No persisted user profile preferences yet.
- No custom user-defined profiles yet.
- No profile editing UI yet.
- No automatic profile recommendation by ticker/timeframe.
- No automatic optimization.
- Existing saved artifacts may have been generated with older/manual parameters.
- Profile values are first-pass defaults and may need tuning after validation runs.

## 14. Recommended Next Options

```text
A. Run broader validation across AAPL / IONQ / AAAU / LOAR with profiles.
B. Document/tune profile values after validation evidence.
C. Add Parameter Profile milestone/status document.  [this document]
D. Add optional Parameter Profile selector to Monte Carlo tab.
E. Add custom user-defined profile support.
F. Add artifact/report field showing which profile was applied.
G. Plan Multi-Timeframe Wyckoff/Wave Alignment as a future feature.
H. Pause feature work and perform repository/documentation cleanup.
```

Recommended next step:

```text
A — run broader validation across known tickers/timeframes using Daily/Swing and Intraday Tactical profiles before tuning profile values or adding more UI.
```

## 15. Resume Checklist

```text
1. Pull latest main.
2. Confirm git status is clean.
3. Start Studio.
4. Load known report folder.
5. Run Strategy Ranking.
6. Select candidate.
7. Apply Parameter Profile.
8. Confirm Data Sufficiency controls update.
9. Confirm Backtest Outcome horizon updates.
10. Confirm Monte Carlo horizon/paths/block length update.
11. Confirm horizon alignment caption is shown.
12. Run Data Sufficiency.
13. Continue to Backtest Candidate Snapshot.
14. Run Backtest Outcome Evaluation.
15. Run Monte Carlo.
16. Run Monte Carlo Forecast Calibration Summary.
17. Review Generated Artifacts.
```

## 16. Future Advancement Parking Lot

Future planning topics, not part of the current implemented milestone:

```text
- Parameter profile tuning based on validation results
- Custom user-defined profiles
- Persisted profile preferences
- Profile metadata in generated artifacts
- Profile selector in Monte Carlo tab
- Historical walk-forward candidate generation
- Multi-Timeframe Wyckoff/Wave Alignment
- Macro/micro phase alignment
- FFT/wavelet-inspired signal features
- Markov-chain or regime-transition ideas
- Macro + micro forecast function
```

## 17. Final Status

```text
Status: MarketFlow Parameter Profile milestone documented.
```
