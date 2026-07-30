# MarketFlow Evidence Availability Status

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-30`
- Branch: `feature/swing-evidence-availability`
- Base commit: `48c434a31cb03a1abfa0f955b428b0dc161cbcf9`
- Baseline tag: `v0.1.0-alpha.5-wyckoff-event-recency`
- Commit: not created
- Tag: not created
- Push: not performed

## Exact Neutral-Placeholder Defect

The pre-fix Strategy Ranking path normalized all configured component weights
and supplied numeric neutral placeholders when optional score-bearing evidence
was absent:

- Point-and-Figure returned `0.5` through `_pnf_score_neutral()`.
- Monte Carlo POP used `0.5` when disabled or missing.

Those values entered the numerator while the `pnf` and `pop` weights remained in
the denominator, making absent evidence look like valid neutral evidence.

## Affected Components And Paths

Score-bearing components:

- `phase`, weight `2.0`, range `0.0..1.0`;
- `event`, weight `1.0`, range `0.0..1.0`;
- `pnf`, weight `1.0`, range `0.0..1.0`;
- `pop`, weight `2.5`, range `0.0..1.0`;
- `trend`, weight `1.0`, range `0.5..0.75`.

Changed paths:

- Strategy Ranking evidence model and composite scoring;
- Strategy service output columns;
- backtest candidate/result schemas and artifacts;
- backtest service and outcome-engine candidate normalization;
- walk-forward case/result propagation;
- Studio strategy and walk-forward displays;
- focused tests and source assurance.

## Component Status Contract

Fixed evidence statuses:

- `EVIDENCE_AVAILABLE`
- `EVIDENCE_DISABLED_BY_CONFIGURATION`
- `EVIDENCE_NOT_AVAILABLE`
- `EVIDENCE_INVALID`
- `EVIDENCE_SOURCE_UNSAFE`
- `EVIDENCE_NOT_APPLICABLE`

Unavailable, disabled, invalid, unsafe, and not-applicable states carry no
score. Valid evidence requires a finite in-range score and provenance.

## Valid Neutral Evidence

Valid `0.5` remains accepted only when the subsystem actually provides it:

- Monte Carlo POP `0.5` with `MONTE_CARLO_POP` provenance remains available.
- PnF score `0.5` with `PNF_SCORE_COLUMN` provenance remains available.

Missing, malformed, out-of-range, disabled, or unsafe evidence cannot become
available merely because `0.5` exists as a fallback number.

## Disabled And Missing Behavior

Explicit disabled behavior:

- disabled components have active weight `0`;
- configured weight remains visible;
- `score_profile_calibration = SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED`;
- `rank_eligible = False`.

Expected but missing behavior:

- active expected missing components produce `SCORE_INCOMPLETE`;
- no `score` / `composite_score` is emitted;
- no unexpected missing-component renormalization occurs.

Invalid behavior:

- malformed/out-of-range POP and PnF scores produce `EVIDENCE_INVALID`;
- active missing or invalid components are retained in diagnostics even if
  their configured weight is zero or malformed.

## Active Profile

The active profile is deterministic:

- required active components: `phase,event,trend`;
- `pop` active only when `use_mc=True`;
- `pnf` active only when `use_pnf=True`;
- no environment value or provider response changes the profile.

## Composite And Ranking

`SCORE_COMPLETE` exists only when all active expected components are available
and active weight total is positive.

`SCORE_INCOMPLETE` has no actionable complete composite score. Incomplete
candidates may retain diagnostics but do not become comparable complete-score
candidates.

Complete disabled-component profiles can compute diagnostic scores on their
active denominator, but are marked uncalibrated and not rank/action eligible.

## Live, Backtest, Walk-Forward, Studio

Live Strategy Ranking now emits component-level status, score, configured
weight, active weight, provenance, and reason fields.

Backtest candidate snapshots, candidate CSV artifacts, result CSV artifacts,
service JSON responses, and outcome-engine candidate normalization preserve
score diagnostics without changing outcome evaluation.

Legacy backtest candidate snapshots that contain only pre-status numeric score
fields are marked `SCORE_INCOMPLETE` with
`LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE`. Legacy POP/PnF `0.5` and old
`composite_score` values do not become `EVIDENCE_AVAILABLE`, do not produce an
actionable `composite_score`, and remain non-rank-eligible unless explicit
modern evidence diagnostics already exist.

Walk-forward cases preserve score diagnostics supplied by source rows; slicing
and future outcome evaluation are unchanged.

Studio shows score status/profile diagnostics in table data, labels incomplete
or uncalibrated candidates, and disables Monte Carlo handoff for incomplete or
uncalibrated score profiles.

## Non-Regression

Preserved:

- configured weights;
- phase score formula;
- event score formula for current accepted events;
- event weight;
- Monte Carlo formula/parameters;
- PnF calculation semantics;
- trend formula;
- source identity;
- entry, stop, target, RR, and minimum-RR gate;
- True Range volatility;
- Wyckoff event recency resolver;
- walk-forward slicing and future-outcome evaluation.

## Verification

Final required checks:

```text
pip check: No broken requirements found.
focused evidence/scoring/propagation/source-identity/target/RR/True Range/event-recency/source-assurance tests: 259 passed, 3 warnings
pytest --collect-only -q: 505 tests collected
pytest -q: 505 passed, 3 warnings
compileall -W error: passed
git diff --check: passed
```

The only warnings are the accepted third-party `polygon` / `websockets`
deprecation warnings.

Pre-full-suite and post-full-suite `git status --short` matched. The default
suite did not modify tracked files.

No manual provider, broker, execution, dependency, or network check was run.

## Test Count

Accepted baseline: `460` tests.

Final collection: `505` tests.

Increase: `45` deterministic tests covering evidence availability, valid
neutral evidence, missing/disabled/invalid status separation, event
availability interaction, zero/missing active weights, complete-score equality,
batch independence, legacy artifact fail-closed behavior, bounded historical
enrichment, propagation, Studio/service/report diagnostics, and source
assurance.

## Reviewer Findings

Reviewer A initial findings:

- High: zero/missing/invalid active component weights could drop expected
  evidence from completeness checks. Disposition: fixed; `_score_from_evidence`
  evaluates every `expected_by_profile` component.
- Medium: malformed POP was classified missing. Disposition: fixed; malformed
  POP reaches evidence validation and becomes `EVIDENCE_INVALID`.
- Medium: backtest service/outcome responses dropped diagnostics. Disposition:
  fixed in service fields and outcome-engine candidate normalization.

Reviewer B initial findings:

- High: stale/unconfigured/missing event evidence could become available score
  input. Disposition: fixed; non-current event statuses become
  `EVIDENCE_NOT_AVAILABLE` score input with event status as reason.
- High: disabled-profile scores were Studio-actionable. Disposition: fixed;
  disabled profiles are explicitly uncalibrated and `rank_eligible=False`;
  Studio handoff is disabled.
- Medium: missing event-availability tests. Disposition: fixed with stale,
  unconfigured-old, and missing-event tests.

Targeted re-reviews reported no remaining critical or high blocker.

Final legacy-artifact audit found one additional high-risk boundary in legacy
snapshot normalization: numeric pre-status score fields needed an explicit
non-actionable status. Disposition: fixed with a fail-closed legacy marker and
six focused tests covering legacy POP `0.5`, legacy PnF `0.5`, old
`composite_score`, preservation of explicit safe diagnostics, unavailable
bounded enrichment, and future-row non-enrichment.

Final independent reviews found additional high legacy/actionability blockers:
walk-forward legacy rows, generic backtest serialization, Studio unknown-status
handoff, partial legacy complete diagnostics, dataclass propagation, and a
stale Strategy docstring. Disposition: fixed with shared fail-closed
normalization, walk-forward legacy markers, Studio unknown-status disabling,
dataclass field-preserving conversion, source assurance, status-only complete
rejection, disabled-profile preservation, non-complete non-actionability, and
ten added tests.

## Deferred Issues

Deferred explicitly:

- calibration of recommendation thresholds for alternate disabled-component
  profiles;
- minimum evidence-coverage calibration;
- broader live ranking versus historical walk-forward alignment;
- predictive applicability for days/weeks;
- volatility-window and stop-multiplier calibration;
- event-age calibration;
- structural event invalidation;
- structural target-quality calibration.

No profitability, execution readiness, or complete strategy-validity claim is
made.
