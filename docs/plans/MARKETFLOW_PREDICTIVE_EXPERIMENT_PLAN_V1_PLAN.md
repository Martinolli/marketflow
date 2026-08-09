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
- Predictive experiment execution candidate digest: `36d724706fe3ea43592eb4589ffae3370f15dd4393d3226fbf9c9155f02561da`
- Predictive experiment execution candidate operator review package digest: `3541d8dc086c28dc3fac75e46e8982230889f958655ad14dc74dd647c8ed7e99`
- Predictive experiment execution approval digest: `d1578a7858da3686d7322f4405e8c5f8075fdb32efa4f77bdae6af2242f4f4be`
- Dataset registry approvals remain research dataset authorities only.

## Operator Review Package
- Artifact kind: `PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE`
- Status: `PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY`
- Checklist summary: `46` passed, `0` failed, `0` blockers.
- The package is ready for operator assessment and for a future predictive experiment execution candidate.
- The package does not authorize predictive experiment execution.

## Execution Candidate
- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE`
- Status: `PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW`
- Execution request ID: `AAPL_PREDICTIVE_EXPERIMENT_EXECUTION_2022_2025_V1`
- Checklist summary: `51` passed, `0` failed, `0` blockers.
- The execution candidate defines a future offline research experiment request only.
- Predictive experiment execution remains future work and is not authorized.

## Execution Candidate Operator Review Package
- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE`
- Status: `PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY`
- Checklist summary: `52` passed, `0` failed, `0` blockers.
- The execution candidate operator review package is implemented.
- The review package does not authorize predictive experiment execution.

## Execution Approval Ceremony
- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED`
- Status: `PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED`
- Checklist summary: `73` passed, `0` failed, `0` blockers.
- The execution approval ceremony is implemented.
- `predictive_experiment_execution_authorized` is `True` for a future research-only, non-actionable execution.
- Predictive experiment execution approval is completed.
- The approval digest remains the source evidence for execution.
- Predictive usefulness remains `not accepted`.
- Profitability remains `not accepted`.
- Runtime use, Strategy use, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- Runtime migration remains not recommended, not approved, and inactive.

## Predictive Experiment Execution
- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTED`
- Status: `PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY`
- Execution digest: `f165b6a066e81e8d5f6c4de2a5603e0dc74aa29ea90dc19cc887b3474bfd32b0`
- Execution implemented on branch `feature/predictive-experiment-execution-v1`.
- Generated outputs are ignored artifacts under `.marketflow/predictive_experiments/AAPL/2022_2025`.
- `predictive_experiment_executed`, `walk_forward_validation_performed`, `out_of_sample_evaluation_performed`, `label_generation_performed`, and `feature_matrix_generation_performed` are `True` only for this research-only execution artifact.
- Strategy scoring and trade recommendation generation remain `False`.
- Provider requests made remain `False`.
- Predictive usefulness remains `not accepted`.
- Profitability remains `not accepted`.
- Runtime activation remains future work and is not approved.

## Predictive Experiment Execution Results Review
- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE`
- Status: `PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY`
- Review package digest: `281e2f0ce4f6050b4788188202003605af95af104b887374484bb1f46ce2b804`
- Execution results review implemented on branch `feature/predictive-experiment-execution-results-review-v1`.
- The review inspected the ignored generated outputs under `.marketflow/predictive_experiments/AAPL/2022_2025` without rerunning the predictive experiment.
- Predictive usefulness assessment remains future work.
- Profitability remains `not accepted`.
- Runtime activation remains future work and is not approved.

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
- Experiment execution required the implemented approval ceremony artifact before the research-only run.
- Outputs from future execution must be labeled `RESEARCH_ONLY_NON_ACTIONABLE`.
- Predictive usefulness and profitability review remain separate future tasks after experiment results exist.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains explicitly unauthorized.
- Runtime activation remains future work and is not approved by this candidate.

## Next Tasks
1. Predictive usefulness assessment candidate.
2. Profitability review after predictive usefulness assessment.
3. Separate runtime migration approval ceremony, if ever authorized.
