# MarketFlow Evidence Availability Acceptance

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-30T17:00:31Z`
- Branch: `feature/swing-evidence-availability`
- Base commit: `48c434a31cb03a1abfa0f955b428b0dc161cbcf9`
- Baseline tag: `v0.1.0-alpha.5-wyckoff-event-recency`
- Local commit: pending final gate
- Tag: not created
- Push: not performed
- Remote configuration: not changed

## Scope

Accepted scope is limited to evidence-availability status modeling, disabled
versus unavailable evidence, component score validation, active profile
diagnostics, composite-score completeness, rank eligibility, additive
propagation, focused tests, and documentation.

Explicit exclusions remain unchanged: no Monte Carlo formula or parameter
change, no Point-and-Figure semantic change, no phase/event/trend formula
change, no source-identity change, no entry/stop/target/RR/True Range change,
no event-recency change, no walk-forward slicing or outcome-evaluation change,
and no provider, broker, or execution behavior.

## Defects Accepted

Original placeholder defects:

- Missing or unused PnF evidence could receive `_pnf_score_neutral()`, commonly
  `0.5`, while the PnF weight stayed in the normalized composite score.
- Missing Monte Carlo POP could flow through `pop if pop is not None else 0.5`
  while the POP weight stayed in the normalized composite score.

The correction removes the placeholder at the component boundary. Display logic
does not hide a fabricated number after scoring.

## Evidence Contract

Score-bearing components are `phase`, `event`, `pnf`, `pop`, and `trend`.

Fixed component statuses are:

- `EVIDENCE_AVAILABLE`
- `EVIDENCE_DISABLED_BY_CONFIGURATION`
- `EVIDENCE_NOT_AVAILABLE`
- `EVIDENCE_INVALID`
- `EVIDENCE_SOURCE_UNSAFE`
- `EVIDENCE_NOT_APPLICABLE`

`EVIDENCE_AVAILABLE` requires finite in-range score and provenance.
Unavailable, disabled, invalid, unsafe, and not-applicable evidence has no
score, is not scoring eligible, and cannot carry a numeric sentinel.

## Valid Neutral Evidence

Valid neutral `0.5` remains accepted only when produced by real subsystem
evidence:

- Monte Carlo POP `0.5` with `MONTE_CARLO_POP` provenance is available.
- PnF score `0.5` with `PNF_SCORE_COLUMN` provenance is available.

Numeric equality to `0.5` is never used to infer availability, absence,
disablement, or invalidity.

## Component Findings

Disabled components are marked `EVIDENCE_DISABLED_BY_CONFIGURATION`, retain
configured weights for diagnostics, have active weight `0`, and carry no score.

Expected active missing evidence is marked unavailable, invalid, or unsafe as
appropriate, produces no `score` or actionable `composite_score`, and does not
renormalize around the missing component.

The active evidence profile is deterministic: `phase,event,trend` are required;
`pop` is active only when `use_mc=True`; `pnf` is active only when
`use_pnf=True`. No environment value, exception, or candidate result changes
another candidate's active profile.

Disabled weighted profiles are marked
`SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED` and are not rank eligible.

## Composite And Ranking

`SCORE_COMPLETE` exists only when every active expected component is
`EVIDENCE_AVAILABLE` and active weight total is positive.

For complete evidence:

```text
composite_score = sum(active_weight * component_score) / sum(active weights) * 100
```

Configured weights and existing component formulas remain unchanged, and the
complete-profile score matches the historical genuine-evidence calculation.

Incomplete, invalid, unsafe, or uncalibrated profiles are visible as
diagnostics but cannot enter complete-evidence ranking or produce READY-style
actionability from score completeness.

## Legacy Artifacts

Legacy backtest, dict, CSV, and result artifacts created before evidence
statuses existed are high risk because numeric values alone do not prove
availability.

Disposition:

- legacy POP `0.5` without status does not become `EVIDENCE_AVAILABLE`;
- legacy PnF `0.5` without status does not become `EVIDENCE_AVAILABLE`;
- legacy `composite_score` without component states becomes non-actionable;
- missing status/provenance produces `SCORE_INCOMPLETE`;
- `rank_eligible` is false;
- explicit modern safe diagnostics are not overwritten;
- event enrichment remains bounded to the historical decision row;
- future rows cannot supply missing event evidence for a historical decision.

No old artifact may be silently upgraded to complete evidence.

## Propagation

Strategy Ranking emits score status, active profile, component statuses, scores,
configured weights, active weights, provenance, reasons, evidence coverage, and
rank eligibility.

Backtest candidate snapshots, candidate CSV artifacts, result CSV artifacts,
service JSON responses, and outcome-engine candidate normalization preserve
score diagnostics without changing outcome evaluation.

Walk-forward cases and artifacts preserve score diagnostics supplied by source
rows. Decision-row slicing and future outcome evaluation are unchanged.

Studio/reporting displays additive diagnostics, distinguishes disabled from
unavailable evidence, shows genuine neutral values only with available status,
and disables Monte Carlo handoff for incomplete or uncalibrated profiles.

## Non-Regression

Prior accepted integrity boundaries remain accepted:

- source identity;
- independent structural target and honest RR;
- True Range volatility;
- Wyckoff event recency and supersession;
- no-network default behavior;
- deterministic offline tests;
- clean tracked-file behavior.

No provider call, broker integration, execution capability, dependency change,
or unrelated strategy-semantic change was added or exercised.

## Verification

Final required checks:

```text
pip check: No broken requirements found.
focused evidence/scoring/legacy/propagation/source-identity/target/RR/True Range/event-recency/source-assurance tests: 259 passed, 3 warnings
pytest --collect-only -q: 505 tests collected
pytest -q: 505 passed, 3 warnings
compileall -W error: passed
git diff --check: passed
git diff --cached --check: passed
```

Warnings are limited to the accepted third-party `polygon` / `websockets`
deprecation warnings.

Pre-full-suite and post-full-suite `git status --short` matched. The default
suite did not modify tracked files.

No manual provider, broker, execution, dependency, or network check was run.

## Test Count

Accepted prior count: `460` tests.

Final collection: `505` tests.

Increase: `45` deterministic tests. The increase covers evidence availability,
valid neutral evidence, missing/disabled/invalid status separation, event
availability, zero/missing active weights, complete-score equality, batch
independence, legacy artifact fail-closed behavior, bounded historical
enrichment, propagation, Studio/service/report diagnostics, and source
assurance.

## Reviewer Findings

Reviewer A initial findings:

- High: active expected components with zero/missing/invalid weights could drop
  from completeness checks. Fixed.
- Medium: malformed POP could be classified missing. Fixed.
- Medium: backtest service/outcome responses dropped diagnostics. Fixed.

Reviewer B initial findings:

- High: stale/unconfigured/missing event evidence could become available score
  input. Fixed.
- High: disabled-profile scores were Studio-actionable. Fixed.
- Medium: missing event-availability tests. Fixed.

Final legacy-artifact audit finding:

- High-risk boundary: legacy numeric pre-status score fields needed explicit
  fail-closed status. Fixed with
  `LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE` and six focused tests.

Final independent review findings:

- High: walk-forward legacy rows could carry old composite values without score
  status. Fixed with walk-forward legacy fail-closed marking.
- High: generic backtest candidate serialization bypassed snapshot
  normalization. Fixed by routing dict/dataclass candidates through
  `normalize_candidate_snapshot`.
- High: Studio allowed unknown score status for Monte Carlo handoff. Fixed;
  only `SCORE_COMPLETE` is handoff eligible.
- High: partial legacy diagnostics could claim `SCORE_COMPLETE` without full
  component statuses. Fixed; complete preservation requires all component
  statuses available.
- High: snapshot dict-to-dataclass conversion dropped score diagnostics. Fixed
  with field-preserving conversion.
- High: Strategy ranker docstring still described old neutral-placeholder
  behavior. Fixed.
- High: status-only `SCORE_COMPLETE` legacy diagnostics could bypass
  fail-closed handling, while disabled-component complete diagnostics were
  initially too aggressively rewritten. Fixed; complete preservation now
  requires active profile, finite scores, provenance, active weights, scoring
  eligibility, and explicit uncalibrated/non-rank-eligible disabled components.
- High: pure status-only complete artifacts and non-complete artifacts with
  rank eligibility could remain actionable. Fixed; complete claims are
  validated even without numeric legacy scores, and non-complete statuses force
  non-rank-eligible, non-actionable scores.

Targeted re-reviews reported no remaining critical or high blocker.

## Deferred Issues

Deferred explicitly:

- recommendation-threshold calibration for alternate disabled-component
  profiles;
- minimum evidence-coverage calibration;
- broader live ranking versus historical walk-forward alignment;
- predictive applicability for days/weeks;
- volatility-window and stop-multiplier calibration;
- event-age calibration;
- structural event invalidation;
- structural target-quality calibration.

Evidence-availability integrity is accepted.

Disabled-profile score calibration is not accepted.

Minimum evidence coverage is not accepted.

Complete swing-strategy predictive validity is not accepted.
