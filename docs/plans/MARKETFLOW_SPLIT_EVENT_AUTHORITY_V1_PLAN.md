# MarketFlow Split Event Authority v1 Plan

## Purpose
- Create an offline, digest-bound split event authority candidate for the 12 identity-frozen expanded-universe tickers.
- Bind the candidate to the approved corporate-action authority plan, registry inventory approval, and identity freeze evidence chain.
- Keep this phase candidate-only and non-authorizing.

## Source Corporate-Action Plan Approval
- Source artifact: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED`
- Source approval digest: `bd02155f618bee231e4472049963343d57b7585920653b31aa5518e96ded0d2f`
- Source approval scope: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY`
- Source plan review package digest: `6d0acf97fb36e5302d62c4077ef0dd902a36dc9bf88c7f0234fef07c516bf9c1`
- Source plan candidate digest: `3ab988e647eebf01ea489dd3e9da2a1edf7b9c8a50b26a54995d39cc3115753a`
- Registry inventory approval digest: `c380dd016035289d11b79723daafc6bdec694928233ff464ec386239ea820c82`
- Identity freeze digest: `55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30`

## Target Universe
- Target universe count: `12`
- Target universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`

## Split Evidence Requirements
- Planned evidence requirements only:
  - `split_event_history`
  - `split_ratio`
  - `split_execution_date`
  - `split_ex_date`
  - `split_provider_event_id_if_available`
  - `split_adjustment_implication`
  - `split_adjusted_price_impact_policy`
  - `split_reverse_split_flag_if_available`
  - `split_source_endpoint`
  - `provider_response_digest`
  - `sanitized_split_event_digest`
  - `split_event_absence_policy_if_no_splits_returned`
- This candidate does not fetch, infer, approve, or freeze split evidence.
- Unavailable future fields must be marked unavailable during future evidence or candidate creation.
- No field may be fabricated.

## Split Provider Evidence Request Policy
- `future_split_provider_request_policy_status`: `PLANNED_REQUIRES_SEPARATE_APPROVAL`
- `allowed_future_request_type`: `READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY`
- `api_key_handling`: `DO_NOT_STORE_KEYS_OR_PRINT_KEYS`
- `raw_payload_policy`: `DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS`
- `sanitized_status_doc_required`: `True`
- `rate_limit_policy`: `RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED`
- `provider_result_authority`: `SPLIT_EVENT_EVIDENCE_ONLY_NOT_SPLIT_AUTHORITY`

## Future Split Event Authority Chain
1. Split event authority candidate operator review package.
2. Split provider evidence request approval ceremony, if live provider access is required.
3. Split provider evidence execution.
4. Split event evidence/results review package.
5. Split event authority candidate update or discrepancy triage, if required.
6. Split event authority freeze ceremony.

## No-Split / Split Absence Policy
- Future no-split findings must come from reviewed provider evidence or an explicit no-split policy artifact.
- This candidate does not infer zero split events.
- Absence of split evidence in this candidate is `NOT_FETCHED`, not evidence of no splits.

## Adjusted-Price Implications
- Future split authority work must document split adjustment implications before acquisition or dataset generation.
- Adjusted and unadjusted price consequences must be reviewed before any downstream canonical dataset chain.
- This candidate does not alter default dataset source behavior.

## Future Corporate-Action Readiness Chain
1. Dividend event authority candidate.
2. Dividend event authority review/freeze chain.
3. Combined split/dividend corporate-action readiness review.
4. Corporate-action authority approval ceremony, if required.
5. Acquisition generation candidate only after identity and corporate-action authority.
6. Canonical dataset candidate only after acquisition generation freeze.
7. Research registry approval only after canonical dataset freeze.

## Non-Goals
- No Massive.com / Polygon provider request.
- No provider refresh, provider transport enablement, or live validation rerun.
- No split provider evidence execution in the approval ceremony.
- No split provider evidence execution unless the explicit live gate and API key are present.
- No split event authority approval or freeze.
- No dividend event authority candidate, approval, or freeze.
- No corporate-action authority approval.
- No acquisition generation authority.
- No canonical dataset generation.
- No research registry approval.
- No additional predictive evidence execution.
- No predictive experiment, walk-forward, label, feature-matrix, or strategy-scoring rerun.
- No predictive-usefulness acceptance or profitability acceptance.
- No runtime migration, runtime use, strategy use, paper trading, broker execution, automatic stitching, or trade recommendation.

## Guardrails
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

## Implementation Status
- Split event authority candidate implemented: `SPLIT_EVENT_AUTHORITY_CANDIDATE`.
- Candidate status: `SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW`.
- Candidate digest: `7faaaaf19f0630f200c7decaafc2555ea23dab3bcfdffd17713487f33d5d8e0b`.
- Split event authority candidate operator review package implemented: `SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE`.
- Review package status: `SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY`.
- Review package digest: `5f59edb21ab0e800aa714cfca41f3fe2b155f012ea7cc6c4c4c382146303c95a`.
- Review package checklist: `103 total / 103 passed / 0 failed / 0 blockers`.
- Review package planned output count: `8`; all planned outputs remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.
- Split provider evidence request approval ceremony implemented: `SPLIT_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED`.
- Split provider evidence request approval status: `SPLIT_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED`.
- Split provider evidence request approval digest: `7c7e93149fe118985fc218852d79e86b31c9ee5bbd75ebacd1890a3862d573db`.
- Split provider evidence request is authorized for future read-only evidence execution only.
- Split provider evidence execution service implemented for gated read-only execution: `SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED`.
- Split provider evidence execution attempted locally and blocked: `SPLIT_EVENT_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING`.
- Split provider evidence execution digest: `NOT_CREATED`.
- Split event authority remains not created.
- Split event evidence/results review remains future work until a successful gated execution creates sanitized evidence results.
- Split event authority freeze remains future work.
- Dividend event authority chain remains separate.
- Corporate-action authority remains not created.
- Acquisition and dataset chains remain future work.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains future and separate.

## Next Tasks
1. Correct the live gate/API-key environment, then rerun split provider evidence execution.
2. Split event evidence/results review package if execution succeeds.
3. Split event authority freeze ceremony after evidence review.
