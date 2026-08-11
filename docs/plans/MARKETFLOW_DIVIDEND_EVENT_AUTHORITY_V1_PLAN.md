# MarketFlow Dividend Event Authority v1 Plan

## Purpose
- Create an offline, digest-bound dividend event authority candidate for the 12 identity-frozen expanded-universe tickers.
- Bind the candidate to the approved corporate-action authority plan, split event authority candidate review package, registry inventory approval, and identity freeze evidence chain.
- Keep this phase candidate-only and non-authorizing.

## Source Corporate-Action Plan Approval
- Source artifact: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED`
- Source approval digest: `bd02155f618bee231e4472049963343d57b7585920653b31aa5518e96ded0d2f`
- Source approval scope: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY`
- Source plan review package digest: `6d0acf97fb36e5302d62c4077ef0dd902a36dc9bf88c7f0234fef07c516bf9c1`
- Source plan candidate digest: `3ab988e647eebf01ea489dd3e9da2a1edf7b9c8a50b26a54995d39cc3115753a`
- Registry inventory approval digest: `c380dd016035289d11b79723daafc6bdec694928233ff464ec386239ea820c82`
- Identity freeze digest: `55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30`

## Source Split Candidate Review Status
- Source artifact: `SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE`
- Source review status: `SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY`
- Source review package digest: `5f59edb21ab0e800aa714cfca41f3fe2b155f012ea7cc6c4c4c382146303c95a`
- Source split candidate digest: `7faaaaf19f0630f200c7decaafc2555ea23dab3bcfdffd17713487f33d5d8e0b`
- Split event authority remains not created and not frozen.

## Target Universe
- Target universe count: `12`
- Target universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`

## Dividend Evidence Requirements
- Planned evidence requirements only:
  - `dividend_event_history`
  - `cash_dividend_amount`
  - `dividend_currency`
  - `dividend_ex_date`
  - `dividend_record_date_if_available`
  - `dividend_pay_date_if_available`
  - `dividend_declaration_date_if_available`
  - `dividend_provider_event_id_if_available`
  - `dividend_frequency_if_available`
  - `special_dividend_flag_if_available`
  - `dividend_adjustment_implication`
  - `dividend_adjusted_price_impact_policy`
  - `dividend_source_endpoint`
  - `provider_response_digest`
  - `sanitized_dividend_event_digest`
  - `dividend_event_absence_policy_if_no_dividends_returned`
- This candidate does not fetch, infer, approve, or freeze dividend evidence.
- Unavailable future fields must be marked unavailable during future evidence or candidate creation.
- No field may be fabricated.

## Dividend Provider Evidence Request Policy
- `future_dividend_provider_request_policy_status`: `PLANNED_REQUIRES_SEPARATE_APPROVAL`
- `allowed_future_request_type`: `READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY`
- `api_key_handling`: `DO_NOT_STORE_KEYS_OR_PRINT_KEYS`
- `raw_payload_policy`: `DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS`
- `sanitized_status_doc_required`: `True`
- `rate_limit_policy`: `RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED`
- `provider_result_authority`: `DIVIDEND_EVENT_EVIDENCE_ONLY_NOT_DIVIDEND_AUTHORITY`

## Dividend Policy Reconciliation
- Planned reconciliation requirements:
  - `adjusted_vs_unadjusted_price_policy`
  - `cash_dividend_treatment_policy`
  - `special_dividend_treatment_policy`
  - `dividend_reinvestment_not_assumed`
  - `total_return_not_assumed_unless_later_authorized`
  - `dividend_adjustment_impact_on_canonical_dataset`
  - `dividend_adjustment_impact_on_predictive_labels`
  - `dividend_absence_policy`
- This candidate does not authorize adjusted-price policy changes, total-return handling, label regeneration, feature regeneration, or dataset source changes.

## No-Dividend / Dividend Absence Policy
- Future no-dividend findings must come from reviewed provider evidence or an explicit no-dividend policy artifact.
- This candidate does not infer zero dividend events.
- Absence of dividend evidence in this candidate is `NOT_FETCHED`, not evidence of no dividends.

## Adjusted-Price And Total-Return Implications
- Future dividend authority work must document cash-dividend and special-dividend adjustment implications before acquisition or dataset generation.
- Adjusted/unadjusted price and total-return consequences must be reviewed before any downstream canonical dataset chain.
- Dividend reinvestment and total-return assumptions are not assumed unless later authorized.

## Future Dividend Event Authority Chain
1. Dividend event authority candidate operator review package.
2. Dividend provider evidence request approval ceremony, if live provider access is required.
3. Dividend provider evidence execution.
4. Dividend event evidence/results review package.
5. Dividend policy reconciliation review.
6. Dividend event authority candidate update or discrepancy triage, if required.
7. Dividend event authority freeze ceremony.

## Future Corporate-Action Readiness Chain
1. Split event authority evidence/review/freeze chain.
2. Combined split/dividend corporate-action readiness review.
3. Corporate-action authority approval ceremony, if required.
4. Acquisition generation candidate only after identity and corporate-action authority.
5. Canonical dataset candidate only after acquisition generation freeze.
6. Research registry approval only after canonical dataset freeze.

## Non-Goals
- No Massive.com / Polygon provider request.
- No provider refresh, provider transport enablement, or live validation rerun.
- No dividend provider evidence request approval.
- No dividend provider evidence execution.
- No dividend event authority approval or freeze.
- No split event authority approval or freeze.
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
- `no_dividend_event_authority_without_operator_review`
- `no_dividend_event_freeze_without_evidence_review_or_explicit_no_dividend_policy`
- `no_dividend_adjustment_policy_without_operator_review`
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
- `operator_approval_required_before_any_provider_dividend_evidence_request`

## Implementation Status
- Dividend event authority candidate implemented: `DIVIDEND_EVENT_AUTHORITY_CANDIDATE`.
- Candidate status: `DIVIDEND_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW`.
- Candidate digest: `44cabaebea32b4d618d13c4e1c77190c2549b9c15c8481460ab66211d1f44097`.
- Candidate checklist: `96 total / 96 passed / 0 failed / 0 blockers`.
- Dividend event authority remains not created.
- Dividend provider evidence request approval remains future work, if required.
- Dividend provider evidence execution remains future work.
- Dividend event evidence/results review remains future work.
- Dividend policy reconciliation review remains future work.
- Dividend event authority freeze remains future work.
- Split event authority remains not created.
- Corporate-action authority remains not created.
- Acquisition and dataset chains remain future work.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains future and separate.

## Next Tasks
1. Dividend event authority candidate operator review package.
2. Dividend provider evidence request approval, if required.
3. Dividend provider evidence execution.
4. Dividend event evidence review.
5. Dividend policy reconciliation review.
6. Dividend event authority freeze ceremony.
