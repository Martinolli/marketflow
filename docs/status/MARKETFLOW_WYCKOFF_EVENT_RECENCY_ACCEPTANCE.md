# MarketFlow Wyckoff Event Recency Acceptance

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-30T15:49:32Z`
- Branch: `feature/swing-wyckoff-event-recency`
- Base commit: `c14515edde64c47ca7934b17b6c3a7e8ddb62ce6`
- Baseline tag: `v0.1.0-alpha.4-true-range-volatility`
- Commit intent: local commit only
- Tag: not created
- Push: not performed
- Remote configuration: not changed

## Scope And Exclusions

Accepted scope:

- explicit confirmed-event occurrence provenance;
- decision-row event resolution;
- event age in bars;
- explicit `max_event_age_bars` validation and propagation;
- current, stale, unavailable, unconfigured, unsafe, invalid, and supersession diagnostics;
- event-score eligibility based on temporal status;
- additive Strategy, service, backtest, walk-forward, Studio, artifact, test, and documentation updates.

Excluded scope:

- no Wyckoff event detection, classification, phase classification, or event-name change;
- no event-score value or event-weight change for accepted current events;
- no phase, PnF, POP/Monte Carlo, trend, score-normalization, entry, stop, target, RR, minimum-RR, True Range, Eigen/PCA, outcome, horizon, recommendation, provider, broker, or execution change;
- no guessed timeframe-specific or event-type-specific recency windows;
- no structural price-action invalidation.

MarketFlow remains research and decision-support software, not execution software.

## Reproduced Stale-Event Defect

Before production changes, a synthetic frame reproduced the accepted defect:

- explicit `SPRING_WEAK` occurred at row 2;
- decision row was row 29;
- no later explicit confirmed event occurred;
- old Strategy context still reported `SPRING_WEAK`;
- old `_event_score` returned `1.0`;
- no occurrence row, age, or recency classification existed.

Final behavior:

- row 2 remains the occurrence row;
- row 29 does not become a new occurrence;
- `event_age_bars = 27`;
- with `max_event_age_bars=None`, status is `EVENT_RECENCY_POLICY_NOT_CONFIGURED`;
- positive event score is `0`.

This release does not decide whether 27 bars should be stale under a future calibrated policy.

## Occurrence Provenance

Authoritative confirmed-event occurrence source:

- sparse `wyckoff_confirmed_event` cells emitted by the confirmation adapter;
- optional `wyckoff_confirmed_event_occurrence` marker, where `True` means explicit confirmed occurrence and `False` means display/copy context;
- fixed provenance: `WYCKOFF_CONFIRMED_EVENT`.

Occurrence diagnostics include event code, occurrence row position, decision row position, age in bars, configured policy, scoring eligibility, occurrence timestamp when safely available, and supersession count.

No future row can supply occurrence provenance for a historical decision row. No event diagnostic intentionally exposes an absolute file path.

## Sparse And Forward-Filled Findings

Column classification:

- `wyckoff_confirmed_event`: sparse confirmed-event occurrence marker when no occurrence marker column is present.
- `wyckoff_confirmed_event_occurrence`: explicit boolean occurrence marker.
- `wyckoff_event`: raw unconfirmed event label and walk-forward filter/display fallback only.
- `wyckoff_confidence`, `wyckoff_reasons`, and confirmed-event payload rows: metadata.

Findings:

- sparse confirmed-event cells create explicit occurrences when they are not ambiguous consecutive identical labels;
- missing or blank labels do not create occurrences;
- marker-backed forward-filled display copies do not refresh age;
- raw event fallback cannot claim confirmed-event provenance.

## Repeated Explicit Events

Accepted behavior:

- one explicit `SPRING_WEAK` followed by marker-backed forward-filled copies remains one occurrence and age keeps increasing;
- a later `SPRING_WEAK` after blank/no-event rows is a new occurrence and supersedes the old one;
- consecutive markerless sparse `SOS`/`SOS` rows fail closed because explicitness cannot be distinguished from forward-filled display copies;
- consecutive marker-backed `True`/`True` rows are also distinct explicit occurrences;
- malformed occurrence markers fail closed as `EVENT_SOURCE_UNSAFE`.

## Event Status Model

Fixed statuses:

- `EVENT_CURRENT`
- `EVENT_STALE`
- `EVENT_NOT_AVAILABLE`
- `EVENT_RECENCY_POLICY_NOT_CONFIGURED`
- `EVENT_SUPERSEDED`
- `EVENT_SOURCE_UNSAFE`
- `EVENT_INVALID`

`EVENT_SUPERSEDED` is represented in latest-event resolution through supersession metadata: older events are counted as superseded and are not selected or scored after a later explicit event. Public outputs carry sanitized scalar diagnostics rather than private resolver objects.

## Event Age

Formula:

```text
event_age_bars = decision_row_position - occurrence_row_position
```

Acceptance findings:

- age `0` means the event occurred on the decision row;
- negative age is unsafe;
- duplicate or non-monotonic timestamp chronology fails closed where timestamps are present;
- age uses chronological row positions, not elapsed clock time;
- appending future rows cannot change age at an earlier decision row.

## Recency Policy

Accepted type:

```text
max_event_age_bars: Optional[int]
```

Validation:

- `None`, `0`, and positive integers are accepted;
- negative integers, booleans, floats, NaN/Infinity, and strings are rejected;
- no StrategyConfig, service, Studio, CLI, backtest, walk-forward, environment-variable, timeframe-map, or event-type default is introduced.

## No-Policy Behavior

- Age `0` with `None`: `EVENT_CURRENT`; scoring permitted.
- Age `> 0` with `None`: `EVENT_RECENCY_POLICY_NOT_CONFIGURED`; scoring not permitted.
- No occurrence: `EVENT_NOT_AVAILABLE`; event score remains `0`.

Old unconfigured events are not silently classified current, stale, unavailable, or invalid.

## Configured Threshold

Boundary:

```text
age <= max_event_age_bars -> EVENT_CURRENT
age > max_event_age_bars  -> EVENT_STALE
```

Tests cover max age `0`, age `0`, age `1`, exact positive boundary, and one bar beyond boundary. Changing `max_event_age_bars` changes only event temporal status, scoring eligibility, event contribution, and composite score as the direct consequence of the existing event weight.

## Supersession

The latest explicit confirmed event at or before the decision row is authoritative.

Accepted examples:

- older `SPRING_WEAK`, later non-scoring `UT_WEAK`: latest non-scoring event is authoritative and contributes `0`;
- older non-scoring event, later `SOS`: later scoring event is authoritative and receives the unchanged current-event score;
- older `SOS`, later repeated explicit `SOS`: latest explicit occurrence is authoritative;
- future scoring or non-scoring events cannot supersede at historical row T.

Older scoring events are not recovered merely because a later event has score zero.

## Invalidation Finding

No strict source-defined event invalidation or confirmation-revocation field exists in the detector/adapter contract.

Documented limitation:

```text
STRUCTURAL_EVENT_INVALIDATION_NOT_IMPLEMENTED
```

The implementation does not infer invalidation from phase change, support break, target hit, stop hit, price distance, elapsed time beyond recency, or later raw unconfirmed text.

## Scoring Interaction

The existing `_event_score` function and accepted scoring set are unchanged. The event score still returns positive value for the existing scoring labels when the event is temporally accepted.

Temporal gate:

- `EVENT_CURRENT`: event contribution uses unchanged `_event_score`.
- stale, unconfigured old, unavailable, unsafe, invalid, and superseded older events: contribution `0`.

The event weight remains `1.0`; phase, PnF, POP/Monte Carlo, trend weights, and normalization remain unchanged.

## Strategy Path

Strategy Ranking flow:

1. strict ticker/timeframe source identity;
2. annotated source frame;
3. decision row;
4. confirmed-event occurrence resolution;
5. event age;
6. recency policy;
7. supersession;
8. temporal event score;
9. composite score;
10. additive diagnostics.

The path uses rows through the decision row and does not use a last-non-null shortcut that bypasses temporal classification.

## Backtest Enrichment

Backtest candidate construction preserves existing diagnostics when present. If missing, it can enrich diagnostics from source CSV plus exact signal row.

Acceptance findings:

- enrichment is bounded to rows `<= signal_row_index`;
- post-signal confirmed events, including repeated identical labels, are ignored;
- raw unconfirmed events are not upgraded to confirmed provenance;
- existing diagnostics are not overwritten;
- missing or unreadable evidence fails closed with explicit unavailable/unsafe event diagnostics;
- no candidate score or outcome is recomputed from future data during artifact reading.

## Walk-Forward

Walk-forward candidate construction:

- accepts `max_event_age_bars` explicitly;
- keeps `None` as `None`;
- adds no wrapper default;
- resolves confirmed-event diagnostics from prefix rows through T;
- does not treat raw `wyckoff_event` fallback as confirmed evidence;
- leaves future outcome evaluation separate;
- preserves existing slicing and horizon behavior.

## Studio And Reporting

Additive diagnostics are surfaced where supported:

- `event_status`;
- `event_provenance`;
- `event_age_bars`;
- `event_max_age_bars`;
- `event_scoring_eligible`;
- occurrence row/timestamp when safely available;
- decision row and resolution source where relevant.

Compact displays that omit fields do not label stale events as current. Missing age is not displayed as zero, and `None` max age is not documented as approved unlimited persistence.

## Non-Regression Findings

Strict source identity remains accepted:

- wrong-ticker fallback remains absent;
- missing/ambiguous source behavior remains fail-closed;
- validated ticker/timeframe labels remain truthful.

Target/RR remains accepted:

- target remains point-in-time `tr_high`;
- `minimum_rr` remains eligibility-only;
- entry/stop/target/RR formulas remain unchanged.

True Range remains accepted:

- gap-aware True Range calculation remains unchanged;
- volatility aggregation and stop formula remain unchanged.

## Verification Results

Final command evidence:

```text
pip check: No broken requirements found.
focused event-recency, propagation, leakage, source-identity, target/RR, True Range, and source-assurance tests: 182 passed, 3 warnings
pytest --collect-only -q: 460 tests collected
pytest -q: 460 passed, 3 warnings
compileall -W error: passed
git diff --check: passed
```

Warnings are the accepted third-party Polygon/websockets deprecation warnings only.

## Test Count

The accepted prior baseline collected `435` tests. The final acceptance pass collects `460` tests. The count increased by `25` because deterministic coverage was added for event recency, event propagation, repeated explicit events, marker-backed forward-filled copies, stricter threshold validation, future scoring/non-scoring leakage, backtest enrichment leakage/failure paths, raw-event provenance separation, and source-assurance protection.

## No-Network Evidence

Default pytest no-network controls remain active. No manual provider checks were run. No provider call, broker integration, execution path, dependency installation, dependency upgrade, dependency downgrade, or dependency removal was performed.

## Reviewer Findings And Dispositions

Prior event-recency reviewers:

- High: walk-forward could show blank event label with `EVENT_CURRENT`. Disposition: fixed by displaying resolved confirmed event where resolution finds one.
- High: normal walk-forward case building could not receive/pass `max_event_age_bars`. Disposition: fixed by adding explicit propagation.
- High: raw event fallback could claim confirmed-event provenance. Disposition: fixed by resolving temporal diagnostics only from confirmed-event columns.
- Medium: backtest construction only preserved diagnostics and did not resolve missing diagnostics from source context. Disposition: fixed with bounded signal-row enrichment.

Final acceptance reviewers:

- High: markerless repeated confirmed-event labels could refresh event age. Disposition: fixed by failing closed with `EVENT_SOURCE_UNSAFE` when consecutive identical markerless confirmed labels are encountered.
- High: backtest enrichment was signal-row bounded but not source-identity gated. Disposition: fixed by requiring `source_status == EXACT_MATCH` before enrichment can attach confirmed-event diagnostics.
- High: status/acceptance documentation was not truthful after the stricter ambiguity finding. Disposition: fixed in plan, status, and acceptance documents.

No critical or high reviewer finding remains unresolved.

## Remaining Limitations

- event-age calibration is not accepted;
- event predictive validity is not accepted;
- the complete swing strategy is not accepted;
- structural event invalidation is not implemented;
- existing compact displays may omit some diagnostics while preserving truthful source data in richer artifacts.

## Deferred Issues

- timeframe-specific event-age calibration;
- event-age calibration by event type;
- structural price-action event invalidation;
- phase/event interaction calibration;
- missing evidence treated as neutral evidence in other components;
- broader live ranking versus historical walk-forward alignment;
- predictive applicability for days/weeks;
- volatility-window and stop-multiplier calibration;
- structural target-quality calibration.

## Final Acceptance Statement

Event temporal integrity is accepted. Event-age calibration is not accepted. Event predictive validity is not accepted. The complete swing strategy is not accepted.
