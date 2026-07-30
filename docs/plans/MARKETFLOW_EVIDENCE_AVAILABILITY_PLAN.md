# MarketFlow Evidence Availability Plan

## Mission

Correct Strategy Ranking evidence-availability semantics so missing, invalid,
unsafe, or disabled evidence cannot masquerade as valid neutral evidence.

MarketFlow remains research and decision-support software, not execution
software.

## Observed Neutral-Placeholder Risk

Current Strategy Ranking normalizes all configured weights and then supplies
neutral numeric placeholders for unavailable optional evidence:

- Point-and-Figure uses `_pnf_score_neutral()` and returns `0.5`.
- Monte Carlo POP uses `0.5` when `cfg.use_mc` is false or when no valid POP is
  found.

Because the configured `pnf` and `pop` weights stay in the composite score,
absence of evidence can look like valid neutral evidence.

## Score-Bearing Component Inventory

| Component | Weight | Range | Source | Current fallback | Valid neutral possible | Required/configurable |
| --- | ---: | --- | --- | --- | --- | --- |
| `phase` | `2.0` | `0.0..1.0` | `_phase_score(ctx["phase"])` | unknown phase scores `0.0` | no current neutral contract | required |
| `event` | `1.0` | `0.0..1.0` | accepted Wyckoff event resolver plus `_event_score` | unavailable/stale/unconfigured scores `0.0` | zero can be valid semantic evidence | required |
| `pnf` | `1.0` | `0.0..1.0` | currently not wired in Strategy Ranking | always `0.5` | yes, if a real source permits it | configurable |
| `pop` | `2.5` | `0.0..1.0` | latest Monte Carlo metrics `pop_tp_first` | missing/off becomes `0.5` | yes, if MC actually produced `0.5` | configurable |
| `trend` | `1.0` | `0.5..0.75` | close versus rolling mean | invalid rolling mean can become `flat`/`0.5` | yes, flat trend is semantic | required |

Configured weights must remain unchanged.

## Status Contract

Use fixed evidence statuses:

- `EVIDENCE_AVAILABLE`
- `EVIDENCE_DISABLED_BY_CONFIGURATION`
- `EVIDENCE_NOT_AVAILABLE`
- `EVIDENCE_INVALID`
- `EVIDENCE_SOURCE_UNSAFE`
- `EVIDENCE_NOT_APPLICABLE`

Rules:

- Available evidence requires finite in-range score and provenance.
- Disabled evidence has no score and is excluded from the active denominator.
- Expected-but-unavailable, invalid, or source-unsafe evidence has no score and
  cannot produce a complete actionable composite score.
- Not applicable is reserved for a deterministic source-defined contract, not
  missing data.

## Valid Neutral Versus Unavailable

A score of `0.5` remains valid only when the subsystem actually resolved, the
source is safe, the component contract permits `0.5`, and provenance identifies
the real source result. The numeric value itself cannot prove availability.

## Active Evidence Profile

The active profile is derived only from explicit `StrategyConfig` flags and the
fixed required components:

- `phase`, `event`, and `trend` are active by default.
- `pop` is active only when `use_mc=True`.
- `pnf` is active only when `use_pnf=True`.

Disabled components retain configured weights for diagnostics, receive active
weight `0`, and are excluded from numerator and denominator.

## Composite And Normalization Contract

Statuses:

- `SCORE_COMPLETE`: every active expected component is available and active
  weight total is positive.
- `SCORE_INCOMPLETE`: one or more active expected components is unavailable,
  invalid, or unsafe.
- `SCORE_INVALID`: active profile or score contract is invalid.
- `SCORE_PROFILE_UNSAFE`: configured profile cannot be safely scored.

For `SCORE_COMPLETE`:

```text
composite_score = sum(active_weight * score) / sum(active_weight)
```

No missing-score substitution is allowed. Unexpected missing evidence does not
renormalize into a complete score. If diagnostic partial scores are retained,
they must be explicitly labeled and must not overwrite `score` or
`composite_score`.

## Ranking Eligibility

Only `SCORE_COMPLETE` candidates enter complete-evidence ranking. Incomplete,
invalid, or unsafe candidates may retain diagnostics but cannot be ranked as
comparable complete candidates or presented as actionable score output.

Disabled-component profiles are explicit. Recommendation-threshold calibration
for alternate disabled profiles remains deferred and must not be claimed.

## Propagation

Additive diagnostics should propagate through:

- Strategy Ranking candidate dictionaries;
- Strategy service DataFrame columns;
- backtest candidate snapshots and CSV artifacts;
- backtest result CSV artifacts;
- walk-forward case dictionaries and artifacts;
- Studio tables/previews where supported.

No absolute private paths or object reprs should be exposed.

Legacy artifacts created before evidence statuses existed must not infer
availability from numeric values alone. Old POP/PnF `0.5` and `composite_score`
fields are either preserved under explicit modern diagnostics or marked
non-actionable as `SCORE_INCOMPLETE` with missing component evidence.

## Tests

Focused tests will reproduce the current placeholder behavior before
production changes, then prove:

- missing Monte Carlo and PnF evidence do not become `0.5`;
- disabled evidence is distinct from missing expected evidence;
- genuine neutral MC/PnF evidence remains valid;
- incomplete candidates do not enter complete-evidence ranking;
- legacy POP/PnF/composite numerics without statuses fail closed;
- configured weights and existing formulas remain unchanged;
- source identity, target/RR, True Range, and Wyckoff event recency remain
  accepted.

Source-assurance tests will protect against reintroducing neutral placeholders
for missing MC/PnF evidence and against changing protected formulas.

## Exclusions

Do not change Monte Carlo formulas or parameters, PnF semantics, trend formula,
Wyckoff phase/event scoring values, event weight, component weights, source
identity, entry, stop, target, RR, True Range, minimum-RR gates,
walk-forward slicing, future-outcome evaluation, providers, brokers, or
execution behavior.

Do not invent a minimum evidence-coverage threshold.

## Stop Conditions

Stop blocked if branch/base/cleanliness checks fail, dependencies change, a
network call completes, configured weights or protected formulas change,
missing evidence still becomes valid neutral evidence, disabled and missing
remain indistinguishable, valid `0.5` evidence is rejected, incomplete evidence
receives an actionable complete score, protected accepted integrity areas
regress, tests mutate tracked files, full tests fail, compileall fails, or a
critical/high reviewer finding remains unresolved.
