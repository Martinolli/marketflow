# MarketFlow Redesigned Label Generation v1 Plan

## Purpose

Define an offline, digest-bound candidate for possible future redesigned-label generation from reviewed label-objective redesign planning outputs. The candidate is research-only, non-actionable, and does not grant approval or execution authority.

## Source Label Objective Redesign Results Review

- Source artifact/status: `LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE` / `LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY`.
- Source digest: `bda6012c74cffb8841a6b9568c0985e2b6d1c337c7b7fcf892da4b724fcb15f9`.
- The source review verified eight saved design outputs with zero digest mismatches and concluded only that the designs support a future candidate.
- The review remains source evidence and is not rerun or replaced by this candidate.

## Source Design Artifacts

The execution manifest, label-family matrix, threshold matrix, horizon matrix, per-ticker plan, availability-boundary plan, META limitation plan, and operator-summary template remain reviewed, not regenerated, research-only, and non-actionable.

## Planned Redesigned Label Families

Ten planned candidates cover flat-zone direction, redesigned return buckets, 5/10/20-session targets, benchmark-relative return, volatility-adjusted return, drawdown avoidance, asymmetric risk/reward, regime-conditioned direction, per-ticker calibration, and a no-trade-zone class. No label family is selected, authorized, computed, or generated.

## Planned Threshold Strategies

Seven planned strategies cover global, per-ticker, training-window-only, volatility-adjusted, benchmark-relative, flat-zone, and class-balance approaches. All remain `PLANNED_NOT_COMPUTED`.

## Planned Horizon Strategies

Five planned candidates cover one, five, ten, and twenty sessions plus multi-horizon comparison. No horizon is selected or computed.

## Planned Availability Rules

Eight rules preserve training-window-only threshold fitting, null forward-tail labels, no-peek generation, late-window boundaries, META's reduced record count, no synthetic rows, no backfill, and no calendar inference. They remain operator-review plans and are not executed.

## Dataset And Per-Ticker Boundary

- Preserve the exact 12-ticker order and `11946` frozen records.
- Preserve records digest `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- META remains `913` records; every other ticker remains `1003`.
- Every ticker receives a deterministic planning-entry digest, without generated labels.

## Future Chain

1. Redesigned Label Generation Candidate Operator Review Package v1.
2. Redesigned Label Generation Approval v1, if selected.
3. Redesigned Label Generation Execution v1.
4. Redesigned Label Generation Results Review v1.
5. Feature or predictive-evidence planning using redesigned labels only if results support it.
6. Separately governed additional predictive evidence, reassessment/readiness, acceptance candidacy, profitability review, and runtime migration.

## Future Gates

The plan records separate operator-review, approval, execution, results-review, evidence-planning/execution, reassessment/readiness, acceptance-candidate, profitability, and runtime gates. Recording a gate does not open it.

## Risk Controls

The candidate cannot authorize or perform label or feature generation, predictive-evidence execution, predictive-usefulness acceptance, profitability acceptance, runtime or strategy use, paper trading, broker execution, or recommendations. It cannot mutate the frozen dataset, repair META, or advance without separate operator approval.

## Non-Goals And Guardrails

- No provider access, `.env` inspection, live transport, market-data acquisition, dataset regeneration, redesign execution rerun, label/feature generation, metric recomputation, model training, strategy scoring, recommendations, acceptance, profitability approval, runtime activation, or broker/IBKR change.
- Planned outputs remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.
- Predictive usefulness and profitability remain `not accepted`; runtime remains `NOT_AUTHORIZED`.
- Default tests remain deterministic, offline, credential-free, and isolated.

## Next Task

- `Redesigned Label Generation Candidate Operator Review Package v1` is future, separate work.
- The candidate does not create its review package and grants no label-generation authority.
