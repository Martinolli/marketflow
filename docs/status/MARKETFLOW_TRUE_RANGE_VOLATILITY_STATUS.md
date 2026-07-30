# MarketFlow True Range Volatility Status

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-30T14:58:03Z`
- Branch: `feature/swing-true-range-volatility`
- Base commit: `105e288ab324741ec3a78ff2f70b7b3ef950dd91`
- Baseline tag: `v0.1.0-alpha.3-risk-reward-integrity`
- Commit intent: no commit
- Tag: not created
- Push: not performed
- Dependency changes by Codex: none

## Scope

Accepted scope for this task:

- Strategy Ranking volatility input now uses True Range instead of same-bar high-low only.
- Existing simple rolling aggregation, `atr_len`, warmup tail average, stop formula, and `max_sl_atr` multiplier are preserved.
- Volatility failures are fixed statuses and fail closed.
- Bounded volatility diagnostics are propagated through Strategy Ranking, strategy service output, backtest snapshot dict/CSV surfaces, and Studio trade-plan/snapshot previews.
- Focused deterministic tests cover gap behavior, aggregation preservation, prefix behavior, invalid inputs, stop interaction, target/RR invariance, source assurance, and propagation.

Explicit exclusions:

- no target/RR semantic change;
- no score weight, score normalization, phase score, event score, P&F, POP, or trend change;
- no Wyckoff event classification, recency, or trading-range redesign;
- no Monte Carlo, Eigen/PCA, source identity, walk-forward slicing, outcome horizon, provider, broker, or execution change.

MarketFlow remains research and decision-support software, not execution software.

## Defect Reproduction

Pre-production focused tests were added and run against the baseline. The run failed as expected because `_atr` used high-low only, invalid `high < low` still produced an actionable candidate, and volatility diagnostics were absent.

## Corrected Contract

Per-bar True Range is:

```text
max(high - low, abs(high - previous_close), abs(low - previous_close))
```

The first valid bar uses high-low. Required OHLC columns are validated as unique, numeric, finite, and geometrically valid with `high >= low`. Missing, invalid, non-finite, duplicate, or unsafe OHLC inputs do not produce an actionable candidate.

Resolved volatility provenance:

```text
TRUE_RANGE_SIMPLE_ROLLING
```

Fixed volatility statuses:

- `VOLATILITY_RESOLVED`
- `VOLATILITY_NOT_AVAILABLE`
- `VOLATILITY_INVALID`
- `VOLATILITY_SOURCE_UNSAFE`

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

Expected warning boundary: only the three accepted third-party Polygon/websockets deprecation warnings.

The accepted baseline collected `423` tests. This task adds `12` deterministic tests, bringing the final collected count to `435`.

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

## Reviewer Findings

Reviewer A:

- Low: duplicate `close` columns failed closed but were reported as `VOLATILITY_INVALID` before the volatility resolver could classify them as source-unsafe. Disposition: fixed by resolving volatility before reading entry close and covered by duplicate-column regression.
- Low: prefix-invariance coverage tested `_atr` on a sliced frame but did not directly exercise `_resolve_long_trade_levels(..., decision_row_index=...)`. Disposition: fixed with direct trade-level decision-prefix coverage.
- Medium: timestamped source rows could be non-monotonic or duplicated while True Range used physical previous-row order. Disposition: fixed with timestamp chronology validation and focused/source-assurance coverage.
- Medium: walk-forward candidate construction does not use Strategy Ranking volatility. Disposition: accepted as scope boundary and documented in the final acceptance artifact; walk-forward has no ATR-like volatility input in this release, and changing its stop model would violate the requested semantic freeze.

Reviewer B:

- Medium: required status document was missing. Disposition: fixed by adding this acceptance document.
- Medium: status evidence became stale after test additions. Disposition: corrected to the final `154` focused-test and `435` full-suite evidence.
- Low: CLI table remains compact and omits volatility diagnostics. Disposition: accepted as visibility-only; saved JSON, strategy service output, Studio trade plan/snapshot surfaces, and backtest snapshot dict/CSV surfaces carry the diagnostics.
- Low: invalid-input tests did not cover non-finite OHLC, missing previous close, or duplicate OHLC source-unsafe cases. Disposition: fixed with additional focused tests.

No critical, high, or medium reviewer finding remains unresolved.

## Final Acceptance Statement

True Range volatility integrity is accepted for the scoped Strategy Ranking volatility input. The complete swing strategy is not yet accepted.
