# MarketFlow Predictive Experiment Execution Status

## Branch And Commit
- Branch: `feature/predictive-experiment-execution-v1`
- Base commit: `cf0fdd4dca061c69f5dc8b12da5e0634a99cfca4`
- Implementation commit: the commit containing this document.

## Execution Artifact
- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTED`
- Execution status: `PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY`
- Execution digest: `f165b6a066e81e8d5f6c4de2a5603e0dc74aa29ea90dc19cc887b3474bfd32b0`
- Execution request ID: `AAPL_PREDICTIVE_EXPERIMENT_EXECUTION_2022_2025_V1`
- Execution timestamp UTC: `2026-08-09T00:00:00Z`

## Bound Source Evidence
- predictive_experiment_execution_approval_digest: `d1578a7858da3686d7322f4405e8c5f8075fdb32efa4f77bdae6af2242f4f4be`
- execution_candidate_digest: `36d724706fe3ea43592eb4589ffae3370f15dd4393d3226fbf9c9155f02561da`
- execution_candidate_review_package_digest: `3541d8dc086c28dc3fac75e46e8982230889f958655ad14dc74dd647c8ed7e99`
- predictive_experiment_plan_digest: `2d338822163dd25f262a32940153ff9842bb7e3213372ad09ce705bbfddede71`
- predictive_experiment_plan_review_package_digest: `e71197fb6838e2caa99d1cffa3c6bd8847d3170d6f842ea921e5345dac349180`
- predictive_usefulness_review_candidate_digest: `e5724cc5eb106b2aa24c68e80bb24835b293fe50009a4eb01b21154553bc79b6`
- predictive_usefulness_review_candidate_review_package_digest: `f124ee8e7e6b72f9d8f5f2a495bb0afa09ef02e4d8a6a03e795a04de4276efe2`
- campaign_results_review_package_digest: `c0421913adbd4a0a02bb1d062a0ef1efd4081c4e1656a46073f4e45fdfd4408b`
- campaign_execution_digest: `f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c`
- swing_registry_approval_digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- position_swing_registry_approval_digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`

## Outputs Generated Summary
- Output root path: `.marketflow/predictive_experiments/AAPL/2022_2025`
- Planned output count: `13`
- Generated output count: `13`
- Research output label: `RESEARCH_ONLY_NON_ACTIONABLE`
- Metrics label: `RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE`

## Output Digest Manifest
- `baseline_comparison_report`: `0ecf752e53ca01fa4964fd9bdacc202feba6f733d7e5b90348712a256a6755ad`
- `false_positive_false_negative_report`: `990299d5b21c990999ac6bcbc6e16453920caffde8b71b779137f1631b00b834`
- `feature_family_report`: `a3184620ca35fccf4d0716f6a102f6ab476a66c74baf131e2c4b36c7ab5d22bd`
- `feature_matrix_manifest`: `d47b0b0c764d99cb43543c686df718fa07cc06a921838f8375344614d0616a5f`
- `label_definition_report`: `cf14451acb87e967d7f34a4649b4dc94aef2158f4e3207d68c60fcda49c4301c`
- `label_generation_report`: `7bbe2e491ae47c648445660fbf576a2ca1efba94afbb8ebbbbbe888d988a486b`
- `leakage_control_report`: `9d55493e824e4cdfffb890ab96a49dd16844cc7d9c4508d08654ee2830245619`
- `operator_review_summary`: `61994c990395db927542f687f61bcf3c8e3a24b6b35897bc4784d6751d9b9731`
- `out_of_sample_split_report`: `065034daf0685d96d9c31d93ebe11ac06ac465a980163235fb54f810bf45eb83`
- `predictive_experiment_run_manifest`: `ec1b706514b4148e5950869f273c4ae8315ffb829ea19eb647bfc8304bcde4d8`
- `signal_quality_metrics_report`: `95be534ca66ff6f4ea74c515e1be0014aaebb3d080d9a83bb370638c8d6fd249`
- `stability_analysis_report`: `a5f1c6986b23fd22b72cfd0c6d57034d1c59a9fc2d9b3a1269f00c4ffb5db4c7`
- `walk_forward_configuration_report`: `35e4ef95dae8b319ae43328cc11583c47982783f6fb44d5569c54b28165d3f98`

## Dataset Verification Summary
- Dataset count: `2`
- Datasets loaded count: `2`
- Dataset digests verified count: `2`
- Manifest digests verified count: `2`

## Experiment Execution Boundary
- predictive_experiment_execution_authorized: `True`
- predictive_experiment_executed: `True`
- walk_forward_validation_performed: `True`
- out_of_sample_evaluation_performed: `True`
- label_generation_performed: `True`
- feature_matrix_generation_performed: `True`
- new_strategy_scoring_performed: `False`
- trade_recommendations_generated: `False`
- provider_requests_made: `False`

## Predictive And Profitability Boundary
- predictive_usefulness: `not accepted`
- predictive_usefulness_acceptance_ready: `False`
- profitability: `not accepted`
- profitability_acceptance_ready: `False`

## Runtime Boundary
- runtime_migration_recommended: `False`
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`
- automatic_stitching: `False`

## Review Boundary
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Results review remains a separate future task.
- Runtime migration and runtime activation remain future, separate authorization paths.

## Follow-On Results Review Status
- The execution artifact remains the source evidence for the follow-on results review.
- Follow-on results review implemented on branch `feature/predictive-experiment-execution-results-review-v1`.
- Follow-on results review artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE`.
- Follow-on results review status: `PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY`.
- Follow-on results review digest: `281e2f0ce4f6050b4788188202003605af95af104b887374484bb1f46ce2b804`.
- Follow-on results review did not rerun the predictive experiment or regenerate outputs.
- Predictive usefulness remains `not accepted`.
- Profitability remains `not accepted`.
- Runtime use, Strategy use, paper trading, and broker execution remain `NOT_AUTHORIZED`.

## Non-Goals
- No provider request was made.
- No strategy scoring was performed.
- No broker, IBKR, paper-trading, or execution pathway was enabled.
- No predictive usefulness or profitability acceptance was granted.
- No runtime migration was recommended, approved, activated, or made default.
