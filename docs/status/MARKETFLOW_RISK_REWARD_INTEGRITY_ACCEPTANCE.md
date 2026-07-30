# MarketFlow Risk/Reward Integrity Acceptance

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-30T14:19:23Z`
- Branch: `feature/swing-risk-reward-integrity`
- Base commit: `2ccaa223d4a193d655713285291d04267637f79a`
- Baseline tag: `v0.1.0-alpha.2-source-identity`
- Commit intent: local commit only
- Tag: not created
- Push: not performed
- Remote configuration: not changed

## Scope

Accepted scope:

- independent structural long-target resolution;
- target provenance and fixed target status values;
- risk/reward calculation from entry, stop, and independently resolved target;
- `minimum_rr` as an eligibility threshold only;
- point-in-time `tr_low` and `tr_high` adapter output needed for historical target safety;
- bounded propagation of target/RR status into Strategy, walk-forward, backtest snapshot, Studio, and report surfaces;
- focused deterministic tests and source-assurance coverage.

Exclusions:

- no entry-reference semantic change;
- no stop-calculation semantic change;
- no high-low volatility or ATR redesign;
- no score component, score weight, score normalization, or trend change;
- no Wyckoff phase/event classification redesign;
- no Monte Carlo, Point-and-Figure, Eigen/PCA, outcome, holding-horizon, provider, broker, or execution change.

## Exact Circular Defect

The baseline Strategy Ranking target was manufactured from the eligibility threshold:

```text
entry = 100
stop = 95
risk = 5

minimum_rr = 2 -> old target = 100 + 2 * 5 = 110 -> calculated RR = 2
minimum_rr = 3 -> old target = 100 + 3 * 5 = 115 -> calculated RR = 3
```

This made the target and calculated RR depend mechanically on the threshold being tested.

## Production Paths Changed

- `marketflow/marketflow_strategy.py`
- `marketflow/marketflow_wyckoff_confirmation_adapter.py`
- `marketflow/services/strategy_service.py`
- `marketflow/services/walk_forward_validation_service.py`
- `marketflow/services/walk_forward_validation_artifact_service.py`
- `marketflow/services/backtest_candidate_service.py`
- `marketflow/services/backtest_candidate_artifact_service.py`
- `apps/marketflow_studio.py`

## Independent Target Source

The accepted target source is the decision-row Wyckoff trading-range high:

```text
provenance = WYCKOFF_TR_HIGH
column = tr_high
row = decision row
kind = resistance
```

The resolver reads the decision-row `tr_high`, rejects missing/non-finite/non-positive values, rejects ambiguous duplicate `tr_high` sources, and requires `target > entry` for long candidates. It does not read `minimum_rr`, stop distance, score, Monte Carlo, P&F, Eigen/PCA, future outcome, provider data, or operator-entered targets.

## Point-In-Time Findings

The Wyckoff adapter now emits `tr_low` and `tr_high` columns per decision row from the prefix ending at that row. Early rows before the configured minimum touch-count worth of observations remain missing. Appending future extreme highs or lows does not alter previously emitted `tr_low` / `tr_high` values at decision row T.

The adapter's compact `confirmed_events` payload also records the row's point-in-time `tr_low` / `tr_high`, not the full-frame range. Phase and event scoring behavior still uses the existing full-frame `lo` / `hi` path and was not redesigned in this acceptance.

## Target Status Contract

Fixed target statuses:

- `TARGET_RESOLVED`
- `TARGET_NOT_AVAILABLE`
- `TARGET_INVALID`
- `TARGET_SOURCE_AMBIGUOUS`
- `TARGET_SOURCE_UNSAFE`

Missing target behavior:

- no synthetic target;
- no RR value;
- non-actionable;
- `TARGET_NOT_AVAILABLE`.

Invalid or unsafe target behavior:

- no actionable candidate;
- fixed sanitized status;
- no manufactured replacement target.

## Geometry And RR Contract

For long-only candidates:

```text
risk = entry - stop
reward = target - entry
rr = reward / risk
```

Accepted geometry:

- finite positive entry;
- finite positive stop;
- `stop < entry`;
- finite positive target;
- `target > entry`;
- positive risk and reward.

Rejected geometry:

- target equal to or below entry;
- stop equal to or above entry;
- NaN or Infinity;
- malformed numeric input;
- zero risk or reward.

The implementation does not use absolute-value repair, zero-distance repair, zero target fallback, or `minimum_rr`-derived replacement targets.

## Minimum-RR Gate

`minimum_rr` is validated as finite and strictly positive. It is read only after the independent target and raw RR exist.

```text
rr >= minimum_rr -> RR_GATE_PASSED
rr < minimum_rr  -> RR_BELOW_MINIMUM
```

A fixed entry, stop, and structural target retains identical entry, stop, target, provenance, and raw RR for `minimum_rr` values `1`, `2`, and `3`; only eligibility can change.

## Scoring Interaction

RR is an eligibility filter before actionable ranking output. The analytical score formula, weights, phase score, event score, P&F neutral score, POP handling, and trend placeholder were not redesigned. Low-RR or missing-target candidates are non-actionable and skipped from ranked output rather than having score weights adjusted.

## Live, Backtest, And Walk-Forward Findings

Live Strategy Ranking:

- uses validated source identity;
- uses latest decision-row `tr_high`;
- resolves target before RR threshold comparison;
- skips missing/invalid/ambiguous target candidates before scoring/ranking output;
- emits target status, provenance, structural level kind, and RR status.

Backtest snapshot path:

- preserves target/RR metadata in dict and CSV artifact surfaces;
- keeps `CandidateSnapshot` dataclass schema unchanged;
- evaluates outcomes only from supplied entry, stop, and target.

Walk-forward path:

- validates source identity before case construction;
- passes `data.iloc[: index + 1]` into candidate construction;
- uses decision-row `tr_high` for target;
- keeps existing walk-forward entry, stop, timing, future-window, holding-horizon, and outcome semantics;
- records `TARGET_NOT_AVAILABLE` distinctly from `RR_BELOW_MINIMUM`.

The broader live-ranking versus historical-candidate alignment issue remains deferred beyond the target contract.

## Studio And Reporting Findings

Strategy service output, Studio displays, walk-forward case artifacts, Markdown case tables, backtest candidate snapshots, and backtest candidate CSVs now expose target/RR status and provenance where those surfaces support candidate metadata. Missing targets remain blank/`None`, not zero. No execution language, broker integration, or trading automation was added.

CLI table output remains a compact legacy display and does not include all metadata columns; saved JSON and service/report surfaces carry the status/provenance fields.

## Source-Identity Non-Regression

Strict ticker/timeframe source identity remains accepted. Wrong-ticker same-timeframe fallback is absent, missing datasets are not scored, ambiguous datasets fail closed, validated labels remain truthful, walk-forward source mismatch fails closed, and Studio/backtest source path confinement remains covered by source-assurance tests.

## Test Count

The source-identity accepted baseline collected `403` tests. This risk/reward task adds `20` deterministic tests, bringing the final collected count to `423`.

Added coverage includes circularity evidence, target invariance, RR threshold behavior, malformed numeric inputs, target missing/invalid/ambiguous cases, no rounding false-pass, point-in-time adapter TR columns and event payloads, walk-forward target status propagation, backtest propagation, Studio/status source assurance, and updated fixture data required by the independent target contract.

## Verification Results

Final command evidence from the last required check sequence:

```text
pip check: No broken requirements found.
focused risk/reward, propagation, leakage, source-identity, network-guard, and source-assurance tests: 195 passed, 3 warnings
pytest --collect-only -q: 423 tests collected
pytest -q: 423 passed, 3 warnings
compileall -W error full baseline: passed
git diff --check: passed
```

Expected warning boundary: only the three accepted third-party Polygon/websockets deprecation warnings.

## No-Network Evidence

Default pytest no-network controls remain active. No manual provider checks were run. No dependency was installed, upgraded, downgraded, or removed. No broker integration or execution capability was added or exercised.

## Reviewer Findings And Dispositions

Reviewer A:

- Medium: malformed numeric OHLC/TR inputs could raise before fail-closed RR handling. Disposition: fixed by validating close, ATR, and `tr_low` at the level-resolution boundary with regression coverage.
- Medium: confirmed-event TR metadata still used full-frame values. Disposition: fixed; compact event payload now records row point-in-time TR values with regression and source-assurance coverage.
- Low: TR columns become finite after minimum row-count even if `_detect_tr` falls back to prefix extrema. Disposition: accepted as point-in-time safe; target-quality calibration remains deferred.

Reviewer B:

- Medium: confirmed-event TR metadata still used full-frame values. Disposition: fixed with the same adapter payload correction.
- Low: status evidence omitted the full compile baseline and test-count explanation. Disposition: final acceptance document records the full baseline and count change.
- Low: plan language overstated "nearest" resistance. Disposition: corrected to single decision-row `tr_high` contract.

No critical or high reviewer finding remains unresolved.

## Remaining Limitations

- The target source is a deterministic structural `tr_high`; this acceptance does not prove target predictive quality.
- `CandidateSnapshot` dataclass intentionally omits target/RR metadata while dict/CSV surfaces preserve it.
- CLI display remains compact and omits the new metadata columns.
- Existing Wyckoff event scoring/classification and event recency were not accepted as strategy-valid.

## Deferred Issues

- high-low volatility instead of true range;
- stale Wyckoff event reuse;
- missing evidence treated as neutral evidence;
- live ranking versus historical walk-forward alignment beyond the target contract;
- predictive applicability for days/weeks;
- target-quality calibration across market regimes.

## Final Acceptance Statement

Target/RR integrity is accepted. Target predictive quality is not accepted. The complete swing strategy is not yet accepted.
