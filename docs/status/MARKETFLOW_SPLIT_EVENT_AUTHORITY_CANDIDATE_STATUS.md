# MarketFlow Split Event Authority Candidate Status

## Branch And Commit
- Branch: `feature/split-event-authority-candidate-v1`
- Base commit: `2c6ff2ccf1dd441b56e4fd1292903beacc7039c8`
- Implementation commit: the commit containing this document.

## Candidate Artifact
- Artifact kind: `SPLIT_EVENT_AUTHORITY_CANDIDATE`
- Candidate status: `SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW`
- Schema version: `split_event_authority_candidate_v1`
- Candidate digest: `7faaaaf19f0630f200c7decaafc2555ea23dab3bcfdffd17713487f33d5d8e0b`
- Created offline: `True`
- Provider requests made: `False`
- Live validation rerun performed: `False`
- Live provider transport enabled: `False`

## Source Corporate-Action Plan Approval
- Source approval artifact: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED`
- Source approval status: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED`
- Source approval scope: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY`
- Corporate-action authority plan approval digest: `bd02155f618bee231e4472049963343d57b7585920653b31aa5518e96ded0d2f`
- Corporate-action plan candidate review package digest: `6d0acf97fb36e5302d62c4077ef0dd902a36dc9bf88c7f0234fef07c516bf9c1`
- Corporate-action plan candidate digest: `3ab988e647eebf01ea489dd3e9da2a1edf7b9c8a50b26a54995d39cc3115753a`

## Bound Source Digests
- Registry inventory approval digest: `c380dd016035289d11b79723daafc6bdec694928233ff464ec386239ea820c82`
- Registry inventory review package digest: `d35861b3bb19d361241df0e6ba080306e647116cf5b12815ce1ddf2fb48cf51c`
- Registry inventory candidate digest: `459f20151cf531b32de91defb7d0a676b20ad68a13b4f391840a0e1db921ea34`
- Identity authority freeze digest: `55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30`
- Identity authority candidate review package digest: `31f010bb328dd71f578ea5c99cc1cb54332a6840d9693b373b73ac688ee118eb`
- Identity authority candidate digest: `0cb27ba65d1dfc57c73f716fdae9bc6baf803770ec11a8ea5868728f58711d3c`
- Live ticker validation results review package digest: `ebaa8b85894ec0eb6b29571c4f473d21b346d86e092a4e68158a401cb9ff7033`
- Live ticker validation execution digest: `96cdb4e97ea6255ddd04bd578a893a28c7a689b5e6d8247f9a26c341226d1ace`
- Ticker universe selection approval digest: `e0b56da411ada20f40fbefdcf74c1cce75ca86d13931471f518ef970db23188c`

## Target Universe
- Target universe count: `12`
- Target universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`

## Split Event Authority Candidate Objective
- `split_event_authority_candidate_objective`: `CREATE_SPLIT_EVENT_AUTHORITY_CANDIDATE_FOR_IDENTITY_APPROVED_EXPANDED_UNIVERSE`
- `split_event_authority_candidate_scope`: `CANDIDATE_ONLY_NOT_AUTHORITY`
- `split_event_authority_creation_status`: `NOT_CREATED`
- `split_event_authority_freeze_status`: `NOT_FROZEN`

## Per-Ticker Split Event Candidate Summary
- Per-ticker split event candidate entries: `12`
- Each entry has identity authority status `FROZEN`.
- Each entry has registry inventory status `APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY`.
- Each entry has corporate-action plan status `APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY`.
- Each entry has split event candidate status `SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Each entry keeps split event authority `NOT_CREATED` and split event freeze `NOT_FROZEN`.
- Each entry keeps provider evidence request `NOT_AUTHORIZED`, provider evidence execution `NOT_EXECUTED`, and split history `NOT_FETCHED`.
- Each entry includes deterministic `per_ticker_split_event_candidate_digest`.

## Split Event Evidence Requirements
- These are planned evidence requirements only.
- This candidate does not fetch provider evidence.
- Unavailable future fields must be marked unavailable during future evidence or candidate creation.
- No field may be fabricated.
- Planned fields: `split_event_history`, `split_ratio`, `split_execution_date`, `split_ex_date`, `split_provider_event_id_if_available`, `split_adjustment_implication`, `split_adjusted_price_impact_policy`, `split_reverse_split_flag_if_available`, `split_source_endpoint`, `provider_response_digest`, `sanitized_split_event_digest`, `split_event_absence_policy_if_no_splits_returned`

## Future Split Provider Request Policy
- `future_split_provider_request_policy_status`: `PLANNED_REQUIRES_SEPARATE_APPROVAL`
- `allowed_future_request_type`: `READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY`
- `api_key_handling`: `DO_NOT_STORE_KEYS_OR_PRINT_KEYS`
- `raw_payload_policy`: `DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS`
- `sanitized_status_doc_required`: `True`
- `rate_limit_policy`: `RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED`
- `provider_result_authority`: `SPLIT_EVENT_EVIDENCE_ONLY_NOT_SPLIT_AUTHORITY`

## Future Split Authority Chain
1. Split event authority candidate operator review package.
2. Split provider evidence request approval ceremony, if live provider access is required.
3. Split provider evidence execution.
4. Split event evidence/results review package.
5. Split event authority candidate update or discrepancy triage, if required.
6. Split event authority freeze ceremony.

## Future Corporate-Action Readiness Chain
1. Dividend event authority candidate.
2. Dividend event authority review/freeze chain.
3. Combined split/dividend corporate-action readiness review.
4. Corporate-action authority approval ceremony, if required.
5. Acquisition generation candidate only after identity and corporate-action authority.
6. Canonical dataset candidate only after acquisition generation freeze.
7. Research registry approval only after canonical dataset freeze.

## Future Gates
- `split_event_authority_candidate_operator_review`
- `split_provider_evidence_request_approval_if_required`
- `split_provider_evidence_execution`
- `split_event_evidence_results_review`
- `split_event_discrepancy_triage_if_required`
- `split_event_authority_freeze`
- `dividend_event_authority_candidate`
- `dividend_event_authority_candidate_review`
- `combined_corporate_action_readiness_review`
- `corporate_action_authority_approval_if_required`
- `acquisition_generation_chain_candidate`
- `canonical_dataset_chain_candidate`
- `research_registry_chain_candidate`

## Risk Controls
- `no_provider_refresh_without_authority`
- `no_raw_provider_payload_commit`
- `no_api_key_storage_or_printing`
- `no_split_event_authority_without_operator_review`
- `no_split_event_freeze_without_evidence_review_or_explicit_no_split_policy`
- `no_corporate_action_authority_without_split_and_dividend_freeze_or_explicit_policy`
- `no_acquisition_authority_without_identity_and_corporate_action_authority`
- `no_dataset_generation_without_acquisition_freeze`
- `no_runtime_source_switch`
- `no_automatic_stitching`
- `no_broker_execution`
- `no_paper_trading`
- `no_trade_recommendations`
- `no_predictive_usefulness_acceptance`
- `no_profitability_acceptance`
- `all_outputs_labeled_research_only`
- `operator_approval_required_before_any_provider_split_evidence_request`

## Split Authority Boundary
- `split_event_authority_candidate_created`: `True`
- `split_event_authority_review_created`: `False`
- `split_event_authority_created`: `False`
- `split_event_authority_frozen`: `False`
- `split_provider_evidence_request_authorized`: `False`
- `split_provider_evidence_executed`: `False`
- `split_provider_evidence_results_created`: `False`

## Dividend Boundary
- `ready_for_dividend_event_authority_candidate`: `True`
- `dividend_event_authority_candidate_created`: `False`
- `dividend_event_authority_review_created`: `False`
- `dividend_event_authority_created`: `False`
- `dividend_event_authority_frozen`: `False`

## Corporate-Action Authority Boundary
- `corporate_action_authority_plan_approved`: `True`
- `corporate_action_authority_created`: `False`
- `corporate_action_authority_artifact_created`: `False`

## Acquisition Boundary
- `new_ticker_acquisition_authorized`: `False`
- `acquisition_generation_authorized`: `False`
- `acquisition_authorization_created`: `False`

## Dataset Generation Boundary
- `dataset_generation_authorized`: `False`
- `dataset_generation_authorization_created`: `False`
- `canonical_dataset_authorized`: `False`
- `registry_approval_created`: `False`

## Predictive/Profitability Boundary
- `additional_predictive_evidence_execution_authorized`: `False`
- `additional_predictive_evidence_executed`: `False`
- `predictive_experiment_rerun_authorized`: `False`
- `predictive_experiment_rerun_performed`: `False`
- `walk_forward_rerun_performed`: `False`
- `label_regeneration_performed`: `False`
- `feature_matrix_regeneration_performed`: `False`
- `new_strategy_scoring_performed`: `False`
- `trade_recommendations_generated`: `False`
- `predictive_usefulness`: `not accepted`
- `profitability`: `not accepted`

## Runtime Boundary
- `runtime_migration_recommended`: `False`
- `runtime_migration_approved`: `False`
- `runtime_migration_active`: `False`
- `strategy_runtime_migration`: `False`
- `runtime_use`: `NOT_AUTHORIZED`
- `strategy_use`: `NOT_AUTHORIZED`
- `paper_trading`: `NOT_AUTHORIZED`
- `broker_execution`: `NOT_AUTHORIZED`
- `automatic_stitching`: `False`

## Checklist Summary
- Total checks: `90`
- Passed checks: `90`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator review: `True`
- Ready for split event provider evidence request approval: `False`
- Ready for split event authority freeze: `False`
- Split event authority authorized: `False`
- Split event authority frozen: `False`
- Dividend event authority authorized: `False`
- Corporate-action authority authorized: `False`
- Acquisition authorized: `False`
- Dataset generation authorized: `False`
- Additional predictive evidence execution authorized: `False`
- Predictive usefulness accepted: `False`
- Profitability accepted: `False`
- Runtime migration authorized: `False`
- Software runtime activation authorized: `False`

## Follow-On Operator Review Package
- Follow-on artifact kind: `SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE`
- Follow-on review status: `SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY`
- Follow-on review package digest: `5f59edb21ab0e800aa714cfca41f3fe2b155f012ea7cc6c4c4c382146303c95a`
- The review package binds this candidate digest: `7faaaaf19f0630f200c7decaafc2555ea23dab3bcfdffd17713487f33d5d8e0b`
- Review package checklist: `103 total / 103 passed / 0 failed / 0 blockers`
- Review package status only sets `split_event_authority_review_created` to `True`.
- The candidate remains the source evidence; the review package does not create a split event authority, freeze, provider evidence request approval, provider evidence execution, dividend authority, corporate-action authority, acquisition authority, dataset authorization, predictive/profitability acceptance, or runtime activation.

## Next Task Recommendation
1. Split provider evidence request approval, if required.
2. Split provider evidence execution.
3. Split event evidence review.
4. Split event authority freeze ceremony.
