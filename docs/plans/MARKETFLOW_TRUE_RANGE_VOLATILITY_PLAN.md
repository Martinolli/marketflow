# MarketFlow True Range Volatility Plan

## Purpose

Correct the Strategy Ranking volatility input so ATR-style stop distance uses True Range rather than same-bar high-low range only.

The change is limited to the per-bar range input used by the existing strategy volatility aggregation. It does not accept or change the broader swing strategy.

## Starting Baseline

- Branch: `feature/swing-true-range-volatility`
- Baseline commit: `105e288ab324741ec3a78ff2f70b7b3ef950dd91`
- Baseline tag at HEAD: `v0.1.0-alpha.3-risk-reward-integrity`
- Python interpreter: `env\Scripts\python.exe`
- Dependency blocker resolved externally: `streamlit==1.45.1`
- Working tree requirement: clean before implementation

## Defect To Reproduce First

The current Strategy Ranking volatility helper computes range as:

```text
high - low
```

This ignores overnight/session gaps visible through the previous close. A gap-up bar whose high-low spread is small can therefore understate risk, tighten the ATR stop, and alter eligibility through a false risk/reward improvement.

Focused tests must be added and run before production edits to demonstrate that gap-up and gap-down volatility is understated.

## True Range Contract

For each OHLC row, compute:

```text
max(
  high - low,
  abs(high - previous_close),
  abs(low - previous_close)
)
```

The first valid bar uses `high - low` because no previous close exists.

Validation must fail closed when:

- required OHLC columns are missing;
- high, low, or close is non-numeric or non-finite;
- `high < low`;
- a previous close needed by a later row is non-finite;
- volatility aggregation produces no finite positive value.

Data order must not be silently changed or repaired.

## Aggregation Boundary

Preserve the existing aggregation method:

- simple rolling mean;
- existing `atr_len`;
- existing warmup fallback to the available tail average when the rolling value is not yet available.

Do not change smoothing, lookback length, `min_periods`, or stop multiplier.

## Status And Provenance

Expose bounded volatility diagnostics where existing candidate metadata surfaces can carry them:

- `VOLATILITY_RESOLVED`
- `VOLATILITY_NOT_AVAILABLE`
- `VOLATILITY_INVALID`
- `VOLATILITY_SOURCE_UNSAFE`

Expected resolved provenance:

- `TRUE_RANGE_SIMPLE_ROLLING`

These diagnostics are informational and fail-closed. They must not manufacture zero volatility or convert missing/invalid volatility into an actionable candidate.

## Explicit Non-Goals

No change to:

- stop formula or `max_sl_atr` multiplier;
- entry semantics;
- `tr_high` target semantics or target provenance;
- minimum-RR threshold behavior;
- risk/reward formula;
- scoring weights, score normalization, phase score, event score, P&F neutral score, POP behavior, or trend placeholder;
- Wyckoff event classification, recency, trading-range detection, or confidence scoring;
- Monte Carlo, Point-and-Figure, Eigen/PCA, source identity, walk-forward slicing, outcome horizons, provider, broker, or execution behavior.

MarketFlow remains research and decision-support software, not execution software.

## Implementation Plan

1. Add focused tests that reproduce the current high-low-only gap defect.
2. Add a canonical True Range resolver in `marketflow/marketflow_strategy.py`.
3. Feed the existing ATR aggregation from the True Range series.
4. Return fixed volatility status/provenance from long trade-level resolution.
5. Propagate the new diagnostics through Strategy Ranking and existing strategy/backtest/Studio metadata surfaces where practical.
6. Update source-assurance tests so the intentionally changed volatility helper is covered by a new true-range contract and the unrelated formulas remain protected.
7. Run bounded read-only independent reviews and resolve any critical or high findings.

## Required Verification

Use only:

```text
env\Scripts\python.exe
```

Required final checks:

- `python -m pip check`
- focused True Range, propagation, leakage, source-identity, target/RR, and source-assurance tests
- `python -m pytest --collect-only -q`
- `python -m pytest -q`
- `python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`
- `git diff --check`
- Git status immediately before and after the full default suite

No dependency install, network/provider check, commit, tag, or push is part of this task.
