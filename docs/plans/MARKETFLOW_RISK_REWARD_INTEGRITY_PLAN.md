# MarketFlow Risk/Reward Integrity Plan

## Observed Circularity

Current Strategy Ranking derives a long stop, manufactures the target from the configured minimum risk/reward value, recalculates risk/reward from that manufactured target, and then tests the recalculated value against the same minimum.

For `entry = 100`, `stop = 95`, and `minimum_rr = 2`, the current construction is:

```text
target = 100 + 2 * (100 - 95) = 110
rr = (110 - 100) / (100 - 95) = 2
```

Changing only `minimum_rr` to `3` changes the target to `115` and mechanically produces `rr = 3`. The gate therefore cannot independently test market opportunity because the threshold creates the target being tested.

## Affected Production Paths

- `marketflow/marketflow_strategy.py`
  - `StrategyConfig.min_rr`: eligibility threshold, currently also used to manufacture target.
  - `_atr`: current high-low volatility source for stop distance; retained unchanged.
  - `_derive_sl_tp_long`: current entry, stop, target, and RR construction; target/RR logic in scope, stop semantics retained.
  - `_rr`: RR calculation; must validate independent entry/stop/target values.
  - `rank_long_candidates`: reads source CSV, calculates levels, applies RR gate, emits candidate rows.
- `marketflow/services/strategy_service.py`
  - `STRATEGY_COLUMNS`, `inspect_strategy_inputs`, `rank_latest_candidates`: public Strategy service schema and diagnostics.
- `apps/marketflow_studio.py`
  - Strategy Ranking table and selected-candidate trade-plan prefill display target/RR.
- `marketflow/services/backtest_candidate_service.py`
  - Normalizes Strategy candidate target/RR into frozen snapshots and validates long levels.
- `marketflow/services/backtest_result_service.py`, `marketflow/services/backtest_service.py`, `marketflow/backtesting/outcome_engine.py`
  - Reopen source CSVs and evaluate outcomes using already supplied entry/stop/target/RR; outcome semantics are out of scope.
- `marketflow/services/walk_forward_validation_service.py`
  - Generates historical candidates at decision rows; currently manufactures take profit from `risk_reward * (entry - stop_loss)`.
- Reporting/artifact services persist target/RR fields from candidate rows but do not define the Strategy target.

## Entry And Stop Semantics Retained

Entry remains the current decision close for Strategy Ranking and walk-forward candidates. Stop remains the existing long stop behavior:

- Strategy Ranking: `max(tr_low, close - max_sl_atr * ATR)`.
- Walk-forward: current row low when below entry, otherwise current `risk_fraction` fallback.

High-low volatility, ATR windowing, and stop fallback behavior are not changed in this task.

## Independent Target-Source Inventory

Existing target-adjacent sources reviewed:

- Strategy CSV `tr_high`: trading-range high emitted by the existing Wyckoff confirmation adapter.
- Strategy CSV `tr_low`: already used as structural stop input; not a long target.
- Support/resistance analyzer output: exists in report JSON paths, but Strategy Ranking reads CSV sources and does not currently pass support/resistance lists into the ranking function.
- Point-and-Figure sidecars: exist, but are optional and not part of the current Strategy Ranking target contract.
- Monte Carlo results: optional probability diagnostics, not a deterministic structural target.
- User-entered Studio values: manual workflow input, not accepted as a Strategy Ranking target source.

## Accepted Target-Source Contract

Use the smallest existing deterministic structural source already in the Strategy CSV workflow:

```text
the decision-row Wyckoff trading-range high (`tr_high`) strictly above entry
```

Initial accepted provenance:

```text
WYCKOFF_TR_HIGH
```

Implementation details:

- For current Strategy Ranking, resolve from the decision prefix ending at the latest row.
- For walk-forward, resolve from the prefix ending at decision row `T`.
- Use the existing Wyckoff confirmation adapter trading-range detection on that prefix when possible.
- Fall back to a row-provided `tr_high` only when it is the decision row's already-materialized finite structural value.
- Never use `minimum_rr`, stop distance, score, recommendation, Monte Carlo, P&F, future bars, or fixed percentages to select the target.

## Target Resolution Model

Create a narrow immutable target-resolution model with fixed status and provenance values.

Statuses:

- `TARGET_RESOLVED`
- `TARGET_NOT_AVAILABLE`
- `TARGET_INVALID`
- `TARGET_SOURCE_AMBIGUOUS`
- `TARGET_SOURCE_UNSAFE`

Provenance:

- `WYCKOFF_TR_HIGH`

Public candidate output may expose sanitized target status and provenance only.

## Target-Unavailable And Invalid Behavior

When no independent target exists:

- do not fabricate `tp`;
- do not fabricate `rr`;
- skip the candidate as non-actionable with `TARGET_NOT_AVAILABLE`.

When target is invalid, ambiguous, or unsafe:

- fail closed;
- do not rank it as actionable;
- expose only fixed sanitized status/reason.

Invalid long setup inputs include non-finite values, non-positive entry/stop/target, stop equal to or above entry, target equal to or below entry, zero or negative risk, and zero or negative reward.

## Risk/Reward Formula And Gate

For the existing long-only path:

```text
risk = entry - stop
reward = target - entry
rr = reward / risk
```

`minimum_rr` is used only after RR has been calculated from independently resolved values.

Eligibility:

- `rr >= minimum_rr`: `RR_GATE_PASSED`
- `rr < minimum_rr`: `RR_BELOW_MINIMUM`

Invalid `minimum_rr` values fail closed and are not silently replaced.

## Historical No-Leakage Requirements

At decision row `T`, target resolution may use rows at or before `T` only. Future rows may be used only by outcome evaluation after candidate construction.

Leakage regression:

- resolve a target at decision row `T`;
- append a future extreme high;
- resolve again for the same decision row;
- confirm the target at `T` does not change.

If a target source cannot be resolved without future rows, return `TARGET_SOURCE_UNSAFE` or stop blocked.

## Batch And Ranking Behavior

Focused tests will cover a deterministic batch with:

- valid structural target and RR above minimum;
- valid structural target and RR below minimum;
- no target;
- invalid target;
- ambiguous target source.

Only eligible candidates enter actionable ranking. Failed candidates remain distinguishable by fixed target/RR statuses and cannot affect another candidate's target, RR, score, or ordering.

## Tests

Focused tests will cover:

- reproduction of the circular pre-fix target behavior;
- target independence from minimum RR values `1`, `2`, and `3`;
- eligibility changes while target remains fixed;
- valid target above entry;
- target equal to or below entry;
- stop equal to or above entry;
- missing, invalid, ambiguous, and unsafe targets;
- invalid minimum RR;
- RR above/equal/below threshold;
- no rounding-induced false pass;
- deterministic decision-row trading-range high selection;
- future-bar leakage prevention;
- current Strategy path;
- backtest candidate path;
- walk-forward path;
- Studio/report semantics;
- source assurance, no tracked-file mutation, and no network.

## Source Assurance

Add AST/source-level checks proving:

- `minimum_rr` is not used to construct a target;
- no `entry + minimum_rr * risk` production target construction remains;
- target resolution does not depend on stop distance;
- RR calculation occurs only after target resolution;
- missing target is not filled with zero or a synthetic fallback;
- future rows are not used by historical target resolution;
- stop calculation source, volatility source, score weights, Wyckoff detection, Monte Carlo, P&F, Eigen/PCA, outcome logic, and source identity controls remain bounded.

## Exclusions

No changes to volatility, ATR, stop semantics, entry semantics, candidate score formulas, score weights, trend calculation, Wyckoff phase/event detection, event recency, Monte Carlo, Point-and-Figure, Eigen/PCA, walk-forward decision-row slicing, future outcome evaluation, horizons, recommendation thresholds, direction, broker behavior, provider calls, or execution.

## Stop Conditions

Stop blocked if no point-in-time-safe independent target can be resolved, target still depends on `minimum_rr` or stop distance, unavailable target is fabricated, invalid target becomes actionable, score weights change, source identity regresses, tests modify tracked files, a network call completes, required checks fail, or any critical/high review finding remains unresolved.
