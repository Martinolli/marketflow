# MARKETFLOW_PARAMETER_PROFILE_PLAN

## 1. Purpose

This plan defines future MarketFlow parameter profiles for different analysis purposes and timeframes.

This checkpoint is planning only. It does not implement code changes, does not change existing defaults, does not add automatic optimization, and does not alter any Studio behavior yet.

The future profile work should remain research/calibration only. It is not financial advice, not a trade signal system, and not a buy/sell recommendation engine.

## 2. Current Baseline

Current implemented workflow:

```text
Strategy Ranking
→ Data Horizon / Parameter Sufficiency
→ Backtest Candidate Snapshot
→ Backtest Outcome Evaluation
→ Backtest Calibration Summary
→ Monte Carlo
→ Monte Carlo Forecast Calibration Summary
→ Generated Artifacts
```

Studio now warns when Backtest Outcome horizon and Monte Carlo horizon differ. Horizon mismatch does not block execution, but forecast-vs-actual calibration treats joined rows with mismatched horizons as not scoreable.

## 3. Problem Statement

MarketFlow now has several parameters that must be adjusted carefully by timeframe and purpose:

- Different timeframes require different horizons/windows.
- Daily and weekly data have fewer rows but less noise.
- 30m/15m data have more rows but more noise.
- 5m/1m are high noise and should be review-only for now.
- Eigen/PCA windows need enough rows.
- Monte Carlo and Backtest horizons should match for scoreable calibration.
- Data Sufficiency depends on available rows and selected parameters.
- One global default profile is not ideal.

## 4. Parameters Requiring Profile Control

| Parameter                | Current usage                              | Why profile control matters                                |
| ------------------------ | ------------------------------------------ | ---------------------------------------------------------- |
| Timeframe period         | data download / report generation          | controls available historical rows                         |
| Eigen/PCA window         | Eigen analyzer and sufficiency diagnostics | too large a window weakens small datasets                  |
| Monte Carlo horizon      | MC forecast horizon                        | must align with Backtest horizon for scoreable calibration |
| Backtest Outcome horizon | deterministic actual outcome window        | must align with MC horizon                                 |
| Monte Carlo paths        | simulation stability / runtime             | more paths improve stability but cost time                 |
| Block length             | bootstrap path structure                   | may vary by timeframe/noise                                |
| Minimum rows required    | Data Sufficiency heuristic                 | depends on window/horizon                                  |
| Low-timeframe posture    | 15m/30m/5m/1m                              | noise/provider caution                                     |

## 5. Current Default Timeframe Periods

Current baseline from `marketflow_data_parameters.py`:

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

This plan records the current baseline. This task does not change these values.

## 6. Proposed Profile Types

### 6.1 Fast Test Profile

Purpose:

- quick app testing
- lower runtime
- sanity checks

Suggested characteristics:

- fewer paths
- shorter horizons
- current or shorter periods
- not for serious calibration conclusions

Example:

```text
Eigen window: 40
Backtest horizon: 20
Monte Carlo horizon: 20
Monte Carlo paths: 10000
Block length: 8
```

### 6.2 Daily / Swing Profile

Purpose:

- 1d / 4h analysis
- swing context
- cleaner signal than intraday

Example:

```text
Preferred timeframes: 1d, 4h
Eigen window: 60–80
Backtest horizon: 10–20
Monte Carlo horizon: 10–20
Monte Carlo paths: 30000
Block length: 8–12
```

### 6.3 Intraday Tactical Profile

Purpose:

- 1h / 30m / 15m tactical candidates

Example:

```text
Preferred timeframes: 1h, 30m, 15m
Eigen window: 60–100
Backtest horizon: 50–60
Monte Carlo horizon: 50–60
Monte Carlo paths: 30000–40000
Block length: 8–16
```

### 6.4 Conservative Research Profile

Purpose:

- slower but more robust research/calibration
- broader row requirements
- stronger noise caution

Example:

```text
Eigen window: 80–120
Backtest horizon: matched to timeframe
Monte Carlo horizon: matched to backtest
Monte Carlo paths: 40000–50000
Block length: 12–20
```

### 6.5 Review-Only Low-Timeframe Profile

Purpose:

- 5m / 1m exploratory visual review only

Example:

```text
Preferred timeframes: 5m, 1m
Status: review-only
Use for diagnostics, not first-pass calibration
```

## 7. Timeframe-Specific Guidance

| Timeframe | Suggested posture     | Profile note                                       |
| --------- | --------------------- | -------------------------------------------------- |
| 1mo       | macro only            | low sample count                                   |
| 1w        | macro context         | useful for trend/context, not tactical calibration |
| 1d        | strategic/swing       | good candidate for swing profile                   |
| 4h        | swing/tactical bridge | useful with daily context                          |
| 2h        | tactical              | watch row count                                    |
| 1h        | tactical bridge       | useful for intraday profile                        |
| 30m       | micro/tactical        | useful but noise caution                           |
| 15m       | micro/tactical        | stronger noise caution                             |
| 5m        | review-only           | high noise                                         |
| 1m        | review-only           | very high noise                                    |

## 8. Horizon Alignment Rule

First rule:

```text
For forecast-vs-actual calibration:
Monte Carlo horizon should equal Backtest Outcome horizon.
```

If horizons differ, rows may join but become not scoreable. Studio now warns about this. Future profiles should set both horizons together.

## 9. Data Sufficiency Rule

Current heuristic:

```text
minimum_rows_required =
max(
    eigen_window * 3,
    monte_carlo_horizon * 3,
    backtest_horizon * 3,
    100
)
```

Profiles should respect this heuristic. If selected parameters exceed available data, Data Sufficiency should flag limited/insufficient. Low timeframes may require stronger caution.

## 10. Future Profile Data Structure

Plan a future module or config, but do not implement it in this checkpoint.

Possible future file:

```text
marketflow/config/parameter_profiles.py
```

or:

```text
marketflow/services/parameter_profile_service.py
```

Possible profile dictionary shape:

```python
PARAMETER_PROFILES = {
    "fast_test": {
        "label": "Fast Test",
        "description": "Quick app/runtime validation only.",
        "eigen_window": 40,
        "backtest_horizon": 20,
        "monte_carlo_horizon": 20,
        "monte_carlo_paths": 10000,
        "monte_carlo_block_len": 8,
        "timeframe_posture": {
            "5m": "review_only",
            "1m": "review_only",
        },
    },
    "intraday_tactical": {
        "label": "Intraday Tactical",
        "description": "1h/30m/15m tactical analysis.",
        "eigen_window": 80,
        "backtest_horizon": 60,
        "monte_carlo_horizon": 60,
        "monte_carlo_paths": 30000,
        "monte_carlo_block_len": 12,
    },
}
```

## 11. Future Service Design

Plan a future service:

```text
marketflow/services/parameter_profile_service.py
```

Potential functions:

```python
def list_parameter_profiles() -> list[dict[str, Any]]:
    ...

def get_parameter_profile(profile_name: str) -> dict[str, Any]:
    ...

def apply_parameter_profile_to_session(profile_name: str) -> dict[str, Any]:
    ...

def build_parameter_context_from_profile(profile_name: str) -> dict[str, Any]:
    ...

def validate_parameter_profile(profile: dict[str, Any]) -> dict[str, Any]:
    ...
```

Future implementation should not optimize parameters automatically. Profile selection should only populate/standardize inputs.

## 12. Future Studio Integration

Recommended future section/control:

```text
Parameter Profile Selector
```

Possible locations:

- Strategy Ranking page near Data Horizon / Parameter Sufficiency
- Monte Carlo tab before MC controls
- Backtest Outcome Evaluation section
- Data Sufficiency section

Recommended first UI:

- one selectbox: `Parameter profile`
- button: `Apply profile to current session`
- visible table showing:
  - Eigen window
  - Backtest horizon
  - Monte Carlo horizon
  - MC paths
  - Block length
  - low-timeframe posture

## 13. Guardrails

- profile selection is not optimization
- profile selection does not generate buy/sell signals
- profile selection does not guarantee predictive performance
- user can still override parameters
- horizon mismatch should remain visible
- Data Sufficiency must still evaluate whether the profile fits available rows
- no future leakage
- low-timeframe noise caution must remain visible

## 14. Non-Goals

- no implementation in this checkpoint
- no Python code changes
- no default changes
- no Studio UI changes
- no automatic optimization
- no machine learning parameter tuning
- no macro/micro forecast function
- no historical walk-forward generation

## 15. Future Tests

Planned tests for implementation:

1. List profiles returns expected built-in profiles.
2. Unknown profile returns safe error.
3. Profile validation catches missing horizon.
4. MC horizon and Backtest horizon match inside calibration profiles.
5. Review-only timeframes are labeled.
6. Parameter context generated correctly from profile.
7. Session application sets expected keys.
8. User overrides remain possible.
9. Data Sufficiency can consume profile-derived context.
10. No mutation of profile templates.

## 16. Recommended Next Implementation Task

```text
Next recommended task:
Implement service-only `marketflow/services/parameter_profile_service.py` with built-in profiles and tests, before adding Studio UI.
```

## 17. Final Status

```text
Status: MarketFlow Parameter Profile planning checkpoint only.
```
