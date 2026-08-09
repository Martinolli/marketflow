# MarketFlow Predictive Experiment Plan Candidate Status

## Branch And Commit
- Branch: `feature/predictive-experiment-plan-candidate-v1`
- Base commit: `6c30aa5283d631cd121395df1f7031a3b8069be8`
- Implementation commit: the commit containing this document.

## Plan Artifact
- Artifact kind: `PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE`
- Plan status: `PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW`
- Schema version: `predictive_experiment_plan_candidate_v1`
- Plan digest: `2d338822163dd25f262a32940153ff9842bb7e3213372ad09ce705bbfddede71`

## Source Evidence
- Predictive usefulness review candidate digest: `e5724cc5eb106b2aa24c68e80bb24835b293fe50009a4eb01b21154553bc79b6`
- Predictive usefulness review candidate review package digest: `f124ee8e7e6b72f9d8f5f2a495bb0afa09ef02e4d8a6a03e795a04de4276efe2`
- Campaign execution results review package digest: `c0421913adbd4a0a02bb1d062a0ef1efd4081c4e1656a46073f4e45fdfd4408b`
- Campaign execution digest: `f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c`
- Execution request ID: `AAPL_RESEARCH_APPLICABILITY_EXECUTION_2022_2025_V1`
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- SWING registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- POSITION_SWING registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`

## Experiment Scope
- Ticker universe: `AAPL`
- Dataset profiles: `SWING / RTH_HALF_SESSION_195M`, `POSITION_SWING / RTH_FULL_SESSION_1D`
- Date range: `2022-01-01` through `2025-12-31`
- Registry scope: `RESEARCH_DATASET`
- Runtime use: `NOT_AUTHORIZED`
- Strategy use: `NOT_AUTHORIZED`
- Research-only: `True`

## Planned Labels
- `SWING_NEXT_BAR_DIRECTION`
- `SWING_NEXT_BAR_RETURN_BUCKET`
- `POSITION_SWING_NEXT_SESSION_DIRECTION`
- `POSITION_SWING_NEXT_SESSION_RETURN_BUCKET`
- Labels are planned only and were not calculated.

## Walk-Forward And OOS Plan
- Walk-forward method: `chronological_walk_forward`
- Training window: `planned`
- Validation window: `planned`
- Test window: `planned`
- No shuffle: `True`
- Time order preserved: `True`
- Final holdout period: `planned`
- No future leakage: `True`
- No walk-forward validation or OOS evaluation was executed.

## Baselines And Metrics
- Baselines: `majority_class_baseline`, `zero_return_baseline`, `naive_persistence_baseline`, `random_baseline_seeded`
- Metrics: `directional_accuracy`, `balanced_accuracy`, `precision_recall`, `roc_auc_if_applicable`, `information_coefficient_if_applicable`, `calibration_summary`, `confusion_matrix`, `lift_over_baseline`
- Metric outputs are planned as `RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE`.

## Leakage Controls
- `label_forward_only`
- `no_future_features`
- `split_by_time`
- `no_random_shuffle`
- `embargo_or_gap_if_required`
- `dataset_digest_lock`

## Execution Gates
- `predictive_experiment_plan_operator_review`
- `predictive_experiment_execution_approval`
- `dataset_digest_reverification`
- `label_definition_operator_acceptance`
- `leakage_control_review`
- `walk_forward_configuration_review`
- `no_broker_execution_confirmation`
- `no_paper_trading_confirmation`
- `no_runtime_default_change_confirmation`
- `output_labeling_research_only_confirmation`

## Risk Controls
- `no provider refresh`
- `no broker execution`
- `no paper trading`
- `no runtime source switch`
- `no automatic stitching`
- `no trade recommendations`
- `no predictive usefulness acceptance in experiment execution`
- `no profitability acceptance in experiment execution`
- `all outputs labeled research-only`
- `operator approval required before experiment execution`

## Boundary Conditions
- provider_requests_made: `False`
- predictive_experiment_execution_authorized: `False`
- predictive_experiment_executed: `False`
- walk_forward_validation_performed: `False`
- out_of_sample_evaluation_performed: `False`
- new_strategy_scoring_performed: `False`
- trade_recommendations_generated: `False`
- predictive_usefulness: `not accepted`
- predictive_usefulness_acceptance_ready: `False`
- profitability: `not accepted`
- profitability_acceptance_ready: `False`
- runtime_migration_recommended: `False`
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`
- automatic_stitching: `False`

## Checklist Summary
- Total checks: `42`
- Passed checks: `42`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator review: `True`
- Experiment execution authorized: `False`
- Runtime migration authorized: `False`
- Runtime activation authorized: `False`

## Next Task
- Predictive experiment plan candidate operator review package.
