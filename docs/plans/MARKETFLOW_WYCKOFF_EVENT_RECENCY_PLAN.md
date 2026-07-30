# MarketFlow Wyckoff Event Recency Plan

## Baseline

- Branch: `feature/swing-wyckoff-event-recency`
- Starting commit: `c14515edde64c47ca7934b17b6c3a7e8ddb62ce6`
- Baseline tag at HEAD: `v0.1.0-alpha.4-true-range-volatility`
- Python: `env\Scripts\python.exe` (`Python 3.12.10`)
- Working tree before plan creation: clean
- `pip check`: passing

## Defect To Reproduce

`marketflow/marketflow_strategy.py` currently resolves the strategy event context by taking the last non-null `wyckoff_confirmed_event` in the supplied frame. A confirmed event that occurred many bars before the decision row can therefore remain visible to `_event_score` and receive normal event credit with no event age, no temporal status, no configured recency policy, and no stale-event diagnostic.

## Scope

Allowed changes are limited to:

- Wyckoff confirmed-event occurrence provenance.
- Decision-row event resolution.
- Event age in bars.
- Explicit `max_event_age_bars` handling.
- Later-event supersession.
- Temporal event statuses and diagnostics.
- Event-score eligibility based on temporal status.
- Bounded propagation through Strategy Ranking, backtest candidate construction, walk-forward candidate construction, Studio views, reports, and focused tests/docs.

Out of scope:

- Wyckoff detection thresholds, classification, phase logic, or event names.
- The score value returned by `_event_score` for an accepted current event.
- Strategy component weights or non-event score components.
- Source identity, entry, stop, target, RR, min-RR gate, trend, Monte Carlo, PnF, Eigen, walk-forward slicing, outcome horizons, recommendations, providers, broker, execution, dependency changes, commits, or tags.

## Event Resolution Contract

- Provenance: `WYCKOFF_CONFIRMED_EVENT`.
- Status values:
  - `EVENT_CURRENT`
  - `EVENT_STALE`
  - `EVENT_NOT_AVAILABLE`
  - `EVENT_RECENCY_POLICY_NOT_CONFIGURED`
  - `EVENT_SUPERSEDED`
  - `EVENT_SOURCE_UNSAFE`
  - `EVENT_INVALID`
- Resolution uses only rows at or before the decision row.
- `event_age_bars = decision_row_position - occurrence_row_position`.
- The latest explicit confirmed event at or before the decision row is authoritative.
- A later confirmed event supersedes older events, including older bullish events.
- Future rows must not affect historical event resolution.
- Forward-filled labels are not new occurrences when the explicit occurrence marker identifies display copies.
- Sparse confirmed-event cells are explicit occurrences unless consecutive identical markerless labels create ambiguous explicitness.
- Consecutive identical markerless confirmed labels fail closed as source-unsafe.
- Missing or blank events produce `EVENT_NOT_AVAILABLE`.

## Recency Policy

- Add `max_event_age_bars: Optional[int]` to strategy configuration.
- `None` means no persistence window has been approved.
- Age `0` is current without a policy.
- Age `> 0` with `None` produces `EVENT_RECENCY_POLICY_NOT_CONFIGURED` and no positive event score.
- Configured integer policy:
  - `age <= max_event_age_bars` => `EVENT_CURRENT`
  - `age > max_event_age_bars` => `EVENT_STALE`
- Negative integers, bools, floats, and malformed values are invalid.
- No per-timeframe or guessed defaults will be introduced.

## Scoring Contract

- `_event_score` semantics are preserved for accepted current events.
- Stale, missing, unsafe, invalid, superseded, and unconfigured old events contribute `0`.
- A candidate does not require a current event to remain actionable or ranked if other evidence supports it.

## Propagation

- Strategy Ranking will emit event status, age, provenance, scoring eligibility, occurrence row, occurrence timestamp, and configured policy diagnostics.
- Backtest candidate snapshots and artifacts will carry the same diagnostics without changing entry, stop, target, RR, or outcome behavior.
- Walk-forward candidate construction will resolve the decision-row event from the training/in-sample prefix and add diagnostics without changing slicing or outcome horizons.
- Studio/reporting surfaces will show the diagnostics when present.

## Verification Plan

1. Reproduce the stale-event defect with synthetic data before production changes.
2. Add focused tests for current/no-policy/stale/invalid/missing/superseded/forward-fill/no-future-leakage behavior.
3. Add propagation tests for Strategy Ranking, backtest candidates, walk-forward candidates, and report columns.
4. Add source-assurance tests for unchanged protected strategy semantics and no arbitrary recency default.
5. Run:
   - `env\Scripts\python.exe -m pip check`
   - focused integrity tests
   - `env\Scripts\python.exe -m pytest --collect-only -q`
   - `env\Scripts\python.exe -m pytest -q`
   - `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`
   - `git diff --check`
   - before/after Git status comparison around the full suite

## Stop Conditions

Stop as `BLOCKED` if any required baseline condition is invalid, a dependency/network/manual check is required, forward-filled labels must be treated as new occurrences, stale/unconfigured old events retain positive score, an arbitrary default recency policy is introduced, future rows affect historical resolution, older bullish events are reused after later events, score weights or phase/detection logic changes, source identity/target/RR/True Range regress, tests mutate tracked files, full tests/compile fail, or critical/high review findings remain unresolved.
