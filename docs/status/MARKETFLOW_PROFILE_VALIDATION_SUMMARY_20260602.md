# MARKETFLOW_PROFILE_VALIDATION_SUMMARY_20260602

## 1. Purpose

This document records the first broader validation run after implementing the Studio Parameter Profile Selector.

This is a documentation-only validation summary. It records observed workflow behavior across selected tickers and timeframes, and it is intended to support future profile tuning and strategy validation.

This document is not a parameter tuning document yet. It is not financial advice, not a trade recommendation, and not automatic optimization.

## 2. Current Checkpoint

```text
f77cf59 - Document parameter profile milestone status
```

Relevant previous implementation checkpoint:

```text
b506c05 - Add Studio parameter profile selector
```

## 3. Validation Scope

Validation covered:

```text
AAPL 1d / Daily-Swing
IONQ 30m / Intraday Tactical
AAAU 30m / Intraday Tactical
LOAR 4h / Daily-Swing
```

Validation objective:

- confirm profile application
- confirm Data Sufficiency behavior
- confirm horizon alignment
- confirm artifacts save/preview
- confirm MC/backtest join behavior
- identify dataset constraints
- identify candidate-quality cautions

## 4. Summary of Validation Results

| Ticker | Timeframe | Profile           | Data Sufficiency | Horizon Aligned | Joined | Scoreable | Main Reason Not Scoreable | Workflow Status | Candidate Quality             |
| ------ | --------- | ----------------- | ---------------- | --------------- | ------ | --------- | ------------------------- | --------------- | ----------------------------- |
| AAPL   | 1d        | Daily/Swing       | sufficient       | yes             | yes    | no        | no future bars            | passed          | cautious/monitor              |
| IONQ   | 30m       | Intraday Tactical | sufficient       | yes             | yes    | no        | no future bars            | passed          | cautious/weak long            |
| AAAU   | 30m       | Intraday Tactical | sufficient       | yes             | yes    | no        | no future bars            | passed          | cautious/weak tactical spring |
| LOAR   | 4h        | Daily/Swing       | limited          | yes             | yes    | no        | no future bars            | passed          | cautious/weak                 |

## 5. AAPL 1d / Daily-Swing

```text
Ticker: AAPL
Timeframe: 1d
Profile: Daily/Swing
Rows available: 252
Minimum rows required: 240
Data sufficiency: sufficient
Backtest horizon: 20
Monte Carlo horizon: 20
Horizon aligned: yes
Joined count: 1
Scoreable count: 0
Not-yet-mature count: 1
Horizon mismatch count: 0
Future bars available: 0
Actual outcome: NEITHER
Wyckoff phase/event: D / UT_WEAK
Workflow status: passed
```

Candidate note:

- workflow is valid
- data is sufficient but with small margin
- candidate remains not scoreable because latest row has no future bars
- UT_WEAK context requires caution

## 6. IONQ 30m / Intraday Tactical

```text
Ticker: IONQ
Timeframe: 30m
Profile: Intraday Tactical
Rows available: 432
Minimum rows required: 240
Data sufficiency: sufficient
Noise warning: noise_caution
Backtest horizon: 60
Monte Carlo horizon: 60
Horizon aligned: yes
Joined count: 1
Scoreable count: 0
Not-yet-mature count: 1
Horizon mismatch count: 0
Future bars available: 0
Actual outcome: NEITHER
MC TP first: approximately 46.47%
MC SL first: approximately 52.23%
MC R mean: approximately -0.0558
Wyckoff phase/event: A / UT_WEAK
Workflow status: passed
```

Candidate note:

- workflow is valid
- Intraday Tactical profile fits row-count boundary
- 30m noise warning is expected
- MC distribution slightly favors SL first
- UT_WEAK long setup requires caution

## 7. AAAU 30m / Intraday Tactical

```text
Ticker: AAAU
Timeframe: 30m
Profile: Intraday Tactical
Rows available: 309
Minimum rows required: 240
Data sufficiency: sufficient
Noise warning: expected for 30m
Backtest horizon: 60
Monte Carlo horizon: 60
Horizon aligned: yes
Joined count: 1
Scoreable count: 0
Not-yet-mature count: 1
Horizon mismatch count: 0
Future bars available: 0
Actual outcome: NEITHER
Eligibility status: not_yet_mature
Scoreable reason: no_future_bars_available
MC TP first: approximately 44.54%
MC SL first: approximately 44.28%
MC R mean: approximately -0.2298
Wyckoff phase/event: C / SPRING_WEAK
Workflow status: passed
```

Candidate note:

- workflow is valid
- TP and SL probabilities are nearly balanced
- R mean is negative
- SPRING_WEAK may support tactical review but not strong confirmation
- treat as cautious/weak tactical setup

## 8. LOAR 4h / Daily-Swing

```text
Ticker: LOAR
Timeframe: 4h
Profile: Daily/Swing
Rows available: 195
Minimum rows required: 240
Data sufficiency: limited
Backtest horizon: 20
Monte Carlo horizon: 20
Horizon aligned: yes
Joined count: 1
Scoreable count: 0
Not-yet-mature count: 1
Horizon mismatch count: 0
Future bars available: 0
Actual outcome: NEITHER
MC TP first: approximately 28.82%
MC SL first: approximately 46.60%
MC R mean: approximately -0.1179
Wyckoff phase/event: D / SPRING_WEAK
Trend: flat
Workflow status: passed
```

Candidate note:

- workflow is valid
- data sufficiency is limited because 4h has only 195 rows against 240 required
- MC distribution favors SL first
- flat trend and SPRING_WEAK context require caution
- useful case showing dataset-size constraint for 4h analysis

## 9. Key Findings

1. Studio Parameter Profile Selector is operationally valid.
2. Profiles apply expected session values.
3. Data Sufficiency correctly identifies sufficient and limited datasets.
4. Horizon alignment behavior works.
5. MC/backtest joins work.
6. All tested latest-row candidates are not scoreable because future bars are unavailable.
7. Horizon mismatch was not observed after profile application.
8. Intraday Tactical profile fits 30m/15m row-count requirements better.
9. Daily/Swing profile is usable but 1d/4h may be row-constrained.
10. 30m/15m require noise caution.
11. Candidate quality remains separate from workflow validity.

## 10. Dataset Constraint Finding

```text
1w / 1d / 4h provide cleaner structure but fewer rows.
30m / 15m provide more rows but higher noise.
```

Observed examples:

- AAPL 1d: 252 rows vs 240 required -> sufficient but small margin
- LOAR 4h: 195 rows vs 240 required -> limited
- IONQ 30m: 432 rows vs 240 required -> sufficient
- AAAU 30m: 309 rows vs 240 required -> sufficient

Daily/Swing with Eigen window 80 may be constrained on 1d/4h depending on available history. Intraday Tactical provides better row volume for Eigen/PCA but must keep noise warnings visible.

## 11. Candidate Quality Observations

- UT_WEAK long candidates require caution.
- SPRING_WEAK candidates may be tactically interesting but weak.
- MC probability balance should be reviewed alongside Wyckoff context.
- Negative R mean or negative median R should reduce confidence.
- Strategy Ranking score alone is not sufficient for candidate quality.
- Workflow validity does not imply candidate validity.

## 12. Current Guardrails Confirmed

- profiles do not optimize parameters
- profiles do not create buy/sell signals
- profile values can be manually overridden
- Data Sufficiency remains active after profile application
- horizon mismatch warning remains available
- latest-row no-future-bars rows are not forecast failures
- sufficient data does not imply predictive validity
- low-timeframe noise remains visible
- no future leakage

## 13. Recommended Profile Tuning Questions

Do not implement tuning yet. Record questions only:

1. Should Daily/Swing Eigen window remain 80, or should 4h use 60?
2. Should 4h use a longer data period if provider supports it?
3. Should 1w have a separate Macro Context profile?
4. Should 30m and 15m remain under the same Intraday Tactical profile?
5. Should candidate-quality labels include MC distribution caution?
6. Should UT_WEAK long candidates be downgraded automatically or only flagged?
7. Should profile metadata be saved into generated artifacts?

## 14. Recommended Next Technical Direction

```text
Historical walk-forward candidate validation plan
```

Current latest-row candidates are not scoreable immediately. Walk-forward validation can test historical candidate rows with known future bars. It is the correct path to evaluate whether the strategy has evidence, and it should be planned before implementation.

Next planning status: `docs/plans/MARKETFLOW_HISTORICAL_WALK_FORWARD_VALIDATION_PLAN.md` defines the next proposed path for validating historical candidates with mature future bars.

Implementation status: service-only historical walk-forward case builder and deterministic evaluator implemented.

Implementation status: Historical Walk-Forward Validation markdown artifact writer implemented.

Related milestone status: `docs/status/MARKETFLOW_WALK_FORWARD_VALIDATION_MILESTONE_STATUS.md` records the completed service-level walk-forward validation workflow and markdown artifact writer.

Alternative next tasks:

- tune profile values after more validation
- add profile metadata to generated artifacts
- add custom profiles later
- add multi-timeframe Wyckoff/Wave Alignment later

## 15. Resume Checklist

```text
1. Continue validating additional tickers if desired.
2. Wait for future bars to mature current latest-row candidates.
3. Re-run Monte Carlo Forecast Calibration Summary later.
4. Compare scoreable rows once available.
5. Plan historical walk-forward validation.
6. Only tune profiles after enough validation evidence.
```

## 16. Final Status

```text
Status: MarketFlow profile validation summary documented.
```
