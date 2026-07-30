# MarketFlow True Range Volatility Acceptance

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-30T14:58:03Z`
- Branch: `feature/swing-true-range-volatility`
- Base commit: `105e288ab324741ec3a78ff2f70b7b3ef950dd91`
- Baseline tag: `v0.1.0-alpha.3-risk-reward-integrity`
- Commit intent: local commit only
- Tag: not created
- Push: not performed
- Remote configuration: not changed

## Scope

Accepted scope:

- Strategy Ranking volatility input corrected from high-low only to True Range.
- Existing simple rolling aggregation, `atr_len`, warmup tail average, stop formula, and `max_sl_atr` multiplier preserved.
- Fixed volatility statuses and resolved provenance added.
- Truthful volatility diagnostics propagated through Strategy Ranking, strategy service output, Studio trade-plan/snapshot previews, and backtest snapshot dict/CSV surfaces.
- Focused deterministic tests and source-assurance coverage added.

Exclusions:

- no volatility-window calibration;
- no smoothing calibration;
- no stop-multiplier calibration;
- no entry semantic change;
- no structural target semantic change;
- no target provenance change;
- no RR formula change;
- no minimum-RR target dependency;
- no score component, score weight, score normalization, or trend change;
- no Wyckoff phase/event classification or recency change;
- no Monte Carlo, Point-and-Figure, Eigen/PCA, provider, broker, execution, outcome, or holding-horizon change.

MarketFlow remains research and decision-support software, not execution software.

## High-Low Limitation

The accepted baseline Strategy Ranking volatility helper used same-bar high-low as the complete per-bar range input:

```text
high - low
```

That understated volatility when a bar opened or traded after a gap from the immediately preceding close.

## True Range Formula

The corrected per-bar input is:

```text
range_1 = high - low
range_2 = abs(high - previous_close)
range_3 = abs(low - previous_close)

true_range = max(range_1, range_2, range_3)
```

The first valid chronological bar has no previous close, so its True Range is high-low.

## Input Validation

Volatility fails closed when:

- required OHLC columns are missing;
- OHLC columns are duplicated;
- high, low, or close is malformed, NaN, or infinite;
- `high < low`;
- a previous close needed by a later row is unavailable;
- timestamped data is non-monotonic, duplicated, or unparseable;
- the resolved volatility value is missing, zero, negative, or non-finite.

Invalid volatility does not become zero, high-low fallback, forward-filled data, stale candidate data, or an actionable candidate.

## Aggregation And Warmup

The retained aggregation is:

- source of window: `StrategyConfig.atr_len`;
- default window: `14`;
- aggregation: simple rolling mean;
- rolling behavior: `true_range.rolling(window).mean().iloc[-1]`;
- warmup behavior: when the rolling value is unavailable, use `true_range.iloc[-window:].mean()`;
- missing-value behavior: invalid source values fail closed before aggregation.

No Wilder ATR, EMA, EWM, RMA, smoothing coefficient, third-party ATR implementation, min-periods redesign, window redesign, or warmup redesign was introduced.

Resolved provenance is:

```text
TRUE_RANGE_SIMPLE_ROLLING
```

Fixed statuses are:

- `VOLATILITY_RESOLVED`
- `VOLATILITY_NOT_AVAILABLE`
- `VOLATILITY_INVALID`
- `VOLATILITY_SOURCE_UNSAFE`

## Point-In-Time Findings

At decision row T, True Range uses only:

- `high_T`;
- `low_T`;
- `close_(T-1)`.

Aggregated volatility is computed from rows `<= T`. Future rows with extreme gaps or ranges do not alter the volatility, stop, or RR resolved for a prior decision row.

Timestamped data is not silently reordered. Non-monotonic or duplicate timestamped rows fail closed as source-unsafe.

## Gap Findings

Synthetic gap checks confirm:

- gap up with previous close `100`, high `105`, low `104` produces True Range `5`;
- gap down from previous close `104.5`, high `96`, low `95` produces True Range `9.5`;
- no-gap bar where high-low is dominant preserves high-low behavior.

The direct acceptance examples are represented by the same formula:

- previous close `100`, high `103`, low `102` -> True Range `3`;
- previous close `100`, high `98`, low `97` -> True Range `3`;
- previous close `100`, high `102`, low `99` -> True Range `3`.

## Stop Interaction

The stop formula remains:

```text
stop = max(tr_low or -1e12, close - cfg.max_sl_atr * volatility)
```

The multiplier remains `cfg.max_sl_atr`, default `2.0`. This task changes only the volatility value supplied to that existing formula.

No-gap data retains the same volatility and stop behavior as the old high-low input. Gap-aware data widens the volatility input when the previous-close gap dominates. No compensating multiplier, threshold, entry, direction, or rounding change was made.

## Target And RR Non-Regression

The target remains the point-in-time structural `tr_high` with provenance:

```text
WYCKOFF_TR_HIGH
```

The target does not depend on volatility, stop distance, or `minimum_rr`.

RR remains:

```text
(target - entry) / (entry - stop)
```

`minimum_rr` remains an eligibility gate only. Corrected True Range can change the stop and therefore raw RR, but it does not construct or alter the target.

## Scoring Interaction

Volatility and stop distance do not directly enter the analytical score. They affect actionability through stop/RR eligibility before ranked output.

Unchanged score elements:

- phase score;
- event score;
- P&F neutral score;
- POP handling;
- trend placeholder;
- score weights;
- normalization.

## Live, Backtest, And Walk-Forward Findings

Current Strategy Ranking computes the corrected True Range volatility directly and emits status/provenance.

Backtest candidate creation does not recompute volatility. It preserves the Strategy Ranking candidate's volatility diagnostics in snapshot dict and CSV surfaces, and outcome evaluation remains driven only by supplied entry, stop, and target.

Walk-forward candidate construction has no ATR-like volatility input in this accepted scope. It retains its previously accepted row-low/risk-fraction stop behavior and decision-row prefix target handling. Changing that stop model would be a separate strategy-semantic change and is deferred.

Future outcome evaluation remains unchanged and future-only.

## Studio And Reporting Findings

Strategy service output, Studio trade-plan/snapshot previews, and backtest candidate artifacts carry additive volatility diagnostics when present.

The compact CLI table remains a visibility limitation: it omits the diagnostic fields, but saved JSON contains the full candidate dictionary. The compact table makes no false Wilder ATR claim and does not make invalid volatility actionable.

No execution, broker, provider, or automated-trading language was added.

## Source-Identity Non-Regression

Strict source identity remains accepted:

- wrong-ticker same-timeframe fallback remains absent;
- missing sources are not scored;
- ambiguous sources fail closed;
- validated ticker/timeframe labels remain truthful;
- Studio source paths remain confined;
- backtest and walk-forward source mismatch remains fail-closed.

## Focused Tests

Focused deterministic coverage includes:

- direct first-row high-low behavior;
- gap-up True Range;
- gap-down True Range;
- no-gap high-low equivalence;
- existing rolling window behavior;
- existing warmup tail average behavior;
- prefix invariance with future extreme gaps/ranges;
- trade-level decision-row prefix safety;
- `high < low`;
- missing high;
- missing low;
- missing previous close;
- malformed numeric input;
- NaN/Infinity;
- duplicate OHLC columns;
- unsafe timestamp chronology;
- zero valid range;
- unavailable and invalid statuses;
- stop widened only through corrected gap-aware volatility;
- target unchanged;
- RR target independence;
- Strategy Ranking and backtest snapshot diagnostic propagation;
- Studio/source-assurance diagnostics;
- source-identity non-regression;
- risk/reward non-regression;
- no-network guard.

## Verification Results

Final command evidence:

```text
pip check: No broken requirements found.
focused True Range, propagation, leakage, source-identity, target/RR, source-assurance, and no-network tests: 154 passed, 3 warnings
pytest --collect-only -q: 435 tests collected
pytest -q: 435 passed, 3 warnings
compileall -W error full baseline: passed
git diff --check: passed
```

Git status immediately before the full default suite:

```text
 M apps/marketflow_studio.py
 M marketflow/marketflow_strategy.py
 M marketflow/services/backtest_candidate_artifact_service.py
 M marketflow/services/backtest_candidate_service.py
 M marketflow/services/strategy_service.py
 M tests/test_source_assurance.py
?? docs/plans/MARKETFLOW_TRUE_RANGE_VOLATILITY_PLAN.md
?? docs/status/MARKETFLOW_TRUE_RANGE_VOLATILITY_ACCEPTANCE.md
?? docs/status/MARKETFLOW_TRUE_RANGE_VOLATILITY_STATUS.md
?? tests/test_true_range_volatility.py
```

Git status immediately after the full default suite:

```text
 M apps/marketflow_studio.py
 M marketflow/marketflow_strategy.py
 M marketflow/services/backtest_candidate_artifact_service.py
 M marketflow/services/backtest_candidate_service.py
 M marketflow/services/strategy_service.py
 M tests/test_source_assurance.py
?? docs/plans/MARKETFLOW_TRUE_RANGE_VOLATILITY_PLAN.md
?? docs/status/MARKETFLOW_TRUE_RANGE_VOLATILITY_ACCEPTANCE.md
?? docs/status/MARKETFLOW_TRUE_RANGE_VOLATILITY_STATUS.md
?? tests/test_true_range_volatility.py
```

The before/after status comparison is unchanged, so the default suite did not modify tracked files.

## Test Count

The accepted risk/reward baseline collected `423` tests.

This task adds `12` deterministic tests, bringing the final collected count to `435`.

## Warning Result

Expected warning boundary: only the three accepted third-party Polygon/websockets deprecation warnings.

## No-Network Evidence

Default pytest no-network controls remain active. No manual provider checks were run. No provider call, broker integration, execution path, or dependency change was added or exercised.

## Reviewer Findings And Dispositions

Reviewer A:

- Medium: timestamped source rows could be non-monotonic or duplicated while True Range used physical previous-row order. Disposition: fixed with timestamp chronology validation and focused/source-assurance coverage.
- Medium: walk-forward candidate construction does not use Strategy Ranking volatility. Disposition: accepted as scope boundary and documented; walk-forward has no ATR-like volatility input in this release, and changing its stop model would violate the requested semantic freeze.

Reviewer B:

- Medium: status document evidence was stale after test additions. Disposition: corrected in status and acceptance evidence after final checks.

No critical or high reviewer finding remains unresolved.

## Remaining Limitations

- True Range input integrity is accepted; volatility calibration is not accepted.
- Stop calibration is not accepted.
- Walk-forward stop construction remains a separate pre-existing model.
- CLI display remains compact and omits volatility diagnostics.
- Predictive validity and profitability are not accepted.
- The complete swing strategy is not accepted.

## Deferred Issues

- volatility-window and smoothing calibration;
- stop-multiplier calibration;
- stale Wyckoff event reuse;
- missing evidence treated as neutral evidence;
- broader live ranking versus historical walk-forward alignment;
- predictive applicability for days/weeks;
- structural target-quality calibration.

## Final Acceptance Statement

True Range input integrity is accepted. Volatility calibration is not accepted. Stop calibration is not accepted. The complete swing strategy is not accepted.
