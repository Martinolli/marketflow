# MarketFlow Predictive Usefulness Assessment v1 Plan

## Objective
- Produce an offline, digest-bound predictive usefulness assessment candidate from the reviewed predictive experiment execution results.
- Keep the artifact limited to operator assessment readiness.
- Do not accept predictive usefulness, profitability, runtime migration, strategy use, paper trading, or broker execution.

## Inputs
- Results review package digest: `281e2f0ce4f6050b4788188202003605af95af104b887374484bb1f46ce2b804`
- Execution digest: `f165b6a066e81e8d5f6c4de2a5603e0dc74aa29ea90dc19cc887b3474bfd32b0`
- Execution approval digest: `d1578a7858da3686d7322f4405e8c5f8075fdb32efa4f77bdae6af2242f4f4be`
- Execution request ID: `AAPL_PREDICTIVE_EXPERIMENT_EXECUTION_2022_2025_V1`
- Plan digest: `2d338822163dd25f262a32940153ff9842bb7e3213372ad09ce705bbfddede71`
- Plan review digest: `e71197fb6838e2caa99d1cffa3c6bd8847d3170d6f842ea921e5345dac349180`
- Predictive usefulness review candidate digest: `e5724cc5eb106b2aa24c68e80bb24835b293fe50009a4eb01b21154553bc79b6`
- Predictive usefulness review candidate review digest: `f124ee8e7e6b72f9d8f5f2a495bb0afa09ef02e4d8a6a03e795a04de4276efe2`
- Swing registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- Position swing registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`

## Assessment Steps
1. Load or receive the reviewed predictive experiment results package offline.
2. Bind the assessment candidate to the expected results-review, execution, approval, plan, review, and registry digests.
3. Extract reviewed facts for output count, research-only labels, label generation, feature matrices, walk-forward/OOS availability, baseline counts, metric counts, and failure/warning count availability.
4. Classify evidence as available for operator assessment while marking metrics as not acceptance evidence.
5. Preserve explicit limitations and next gates.
6. Validate that predictive usefulness, profitability, runtime migration, strategy use, paper trading, and broker execution remain not accepted or not authorized.

## Candidate Result
- Artifact kind: `PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE`
- Schema version: `predictive_usefulness_assessment_candidate_v1`
- Candidate status: `PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW`
- Candidate digest: `b98c8fc1a6d64ddb1d3da313659b4e2105702e7d33550840cc00cb0008105598`

## Required Boundaries
- created_offline: `True`
- provider_requests_made: `False`
- experiment_reexecution_performed: `False`
- walk_forward_rerun_performed: `False`
- label_regeneration_performed: `False`
- feature_matrix_regeneration_performed: `False`
- new_strategy_scoring_performed: `False`
- trade_recommendations_generated: `False`
- predictive_usefulness_acceptance_ready: `False`
- predictive_usefulness_acceptance_recommended: `False`
- profitability_acceptance_ready: `False`
- profitability_acceptance_recommended: `False`
- runtime_migration_recommended: `False`
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`
- automatic_stitching: `False`

## Acceptance Boundary
- This plan is not predictive usefulness acceptance.
- This plan is not profitability acceptance.
- This plan is not runtime migration approval.
- This plan is not strategy runtime activation.
- Any later acceptance or migration step requires a separate operator ceremony.
