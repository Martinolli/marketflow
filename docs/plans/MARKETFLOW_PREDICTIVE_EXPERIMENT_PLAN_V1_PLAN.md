# MarketFlow Predictive Experiment Plan v1 Plan

## Purpose
- Define a research-only predictive experiment design for future operator review.
- Bind the plan to the predictive usefulness review candidate and operator review package.
- Preserve the boundary between planning and execution.

## Source Evidence
- Predictive usefulness review candidate digest: `e5724cc5eb106b2aa24c68e80bb24835b293fe50009a4eb01b21154553bc79b6`
- Predictive usefulness review candidate review package digest: `f124ee8e7e6b72f9d8f5f2a495bb0afa09ef02e4d8a6a03e795a04de4276efe2`
- Campaign results review digest: `c0421913adbd4a0a02bb1d062a0ef1efd4081c4e1656a46073f4e45fdfd4408b`
- Campaign execution digest: `f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c`
- Predictive experiment plan candidate digest: `2d338822163dd25f262a32940153ff9842bb7e3213372ad09ce705bbfddede71`
- Predictive experiment plan candidate operator review package digest: `e71197fb6838e2caa99d1cffa3c6bd8847d3170d6f842ea921e5345dac349180`
- Dataset registry approvals remain research dataset authorities only.

## Operator Review Package
- Artifact kind: `PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE`
- Status: `PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY`
- Checklist summary: `46` passed, `0` failed, `0` blockers.
- The package is ready for operator assessment and for a future predictive experiment execution candidate.
- The package does not authorize predictive experiment execution.

## Research-Only Predictive Experiment Design
- Ticker universe is limited to `AAPL`.
- Dataset profiles are limited to `SWING / RTH_HALF_SESSION_195M` and `POSITION_SWING / RTH_FULL_SESSION_1D`.
- Date range is `2022-01-01` through `2025-12-31`.
- Runtime and strategy use remain `NOT_AUTHORIZED`.
- The plan defines future labels, features, splits, baselines, metrics, and reviews, but executes none of them.

## Label Definitions
- `SWING_NEXT_BAR_DIRECTION`
- `SWING_NEXT_BAR_RETURN_BUCKET`
- `POSITION_SWING_NEXT_SESSION_DIRECTION`
- `POSITION_SWING_NEXT_SESSION_RETURN_BUCKET`
- Label calculation requires future operator approval and leakage-control review.

## Walk-Forward Plan
- Method: `chronological_walk_forward`
- Training, validation, and test windows remain planned.
- Shuffle is disabled.
- Time order is preserved.
- Walk-forward validation is not performed by this candidate.

## OOS Plan
- Final holdout period remains planned.
- Future leakage is prohibited.
- Out-of-sample evaluation is not performed by this candidate.

## Baselines And Metrics
- Baselines: majority class, zero return, naive persistence, seeded random.
- Metrics: directional accuracy, balanced accuracy, precision/recall, ROC AUC if applicable, information coefficient if applicable, calibration, confusion matrix, and lift over baseline.
- Metrics are research-only signal-quality measures and not profitability acceptance.

## Leakage Controls
- Labels must be forward-only.
- Features must not include future information.
- Splits must be time-based.
- Random shuffle is disabled.
- Embargo or gap rules are required if the final window design needs them.
- Dataset digests must be locked and reverified before execution.

## Non-Goals
- Do not fetch provider data.
- Do not regenerate datasets.
- Do not rerun the campaign.
- Do not execute predictive experiments.
- Do not run walk-forward validation.
- Do not run strategy scoring.
- Do not generate trade recommendations.
- Do not accept predictive usefulness or profitability.
- Do not approve runtime migration, paper trading, or broker execution.

## Guardrails
- Default tests remain deterministic and offline.
- Experiment execution requires a separate operator review package and approval ceremony.
- Outputs from future execution must be labeled `RESEARCH_ONLY_NON_ACTIONABLE`.
- Predictive usefulness and profitability review remain separate future tasks after experiment results exist.
- Runtime activation remains explicitly unauthorized.

## Next Tasks
1. Predictive experiment execution candidate.
2. Predictive experiment execution approval ceremony.
3. Predictive experiment execution.
4. Predictive usefulness review after experiment results.
