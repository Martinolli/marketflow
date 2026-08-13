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
- Split event authority is now frozen in the follow-on split chain.
- Split event authority freeze digest: `37a06dceac17761319f9d5eb716d64dced765997b8d1e9d8a79166162bfdb303`

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
- `dividend_provider_request_policy_status`: `APPROVED_AND_EXECUTED_READ_ONLY`
- `dividend_provider_request_approval_digest`: `f2b96963ceced82579a647fa1e51ddca1dad91b3de66a35aad8fc389cdbbb2ff`
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
1. Dividend event authority candidate operator review package: completed.
2. Dividend provider evidence request approval ceremony: completed.
3. Dividend provider evidence execution: completed read-only.
4. Dividend event evidence/results review package: implemented and ready for operator review.
5. Dividend policy reconciliation review: implemented and ready for operator assessment.
6. Dividend policy reconciliation approval ceremony: implemented for future freeze input only.
7. Dividend event authority candidate update or discrepancy triage, if required.
8. Dividend event authority freeze ceremony: completed with dividend-event-only scope.

## Future Corporate-Action Readiness Chain
1. Split event authority evidence/review/freeze chain.
2. Combined split/dividend corporate-action readiness review: next separate task.
3. Corporate-action authority approval ceremony, if required.
4. Acquisition generation candidate only after identity and corporate-action authority.
5. Canonical dataset candidate only after acquisition generation freeze.
6. Research registry approval only after canonical dataset freeze.

## Non-Goals
- No additional Massive.com / Polygon provider request.
- No provider refresh, provider transport enablement, or live validation rerun during this documentation update.
- No dividend provider evidence request approval outside the guarded offline approval ceremony.
- No dividend event authority beyond the separately attested, evidence-bound dividend-only freeze.
- No split event authority alteration after the split-only freeze.
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
- Dividend event authority candidate operator review package implemented: `DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE`.
- Review package status: `DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY`.
- Review package digest: `cf120d55beaa22f1fbd4f27d9a7a6539583e5cd67f3d0ffe5a186f318f27a104`.
- Review checklist: `110 total / 110 passed / 0 failed / 0 blockers`.
- Review planned outputs: `9`, all `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.
- Dividend provider evidence request approval ceremony implemented: `DIVIDEND_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED`.
- Dividend provider evidence request approval status: `DIVIDEND_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED`.
- Dividend provider evidence request approval digest: `f2b96963ceced82579a647fa1e51ddca1dad91b3de66a35aad8fc389cdbbb2ff`.
- Dividend provider evidence request is authorized for future read-only evidence execution only.
- Dividend provider evidence execution service implemented: `DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED` / `DIVIDEND_EVENT_PROVIDER_EVIDENCE_BLOCKED`.
- Dividend provider evidence execution branch created: `feature/dividend-provider-evidence-execution-live-run-v1`.
- Dividend provider evidence execution attempted from base commit `85d8eb9cc405553f67d7fb7a075be20465345624` and blocked as `DIVIDEND_EVENT_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING`.
- Dividend provider evidence execution digest: `NOT_CREATED`.
- Dividend provider execution endpoint selected: `Massive.com /stocks/v1/dividends` with mode `CURRENT_STOCKS_V1_DIVIDENDS`.
- Dividend provider evidence execution retry branch created: `feature/dividend-provider-evidence-execution-live-run-retry-v1`.
- Dividend provider evidence execution retried from base commit `bf61988ea38c63d3cc1c607c8e45c2b4acf36a87` and blocked as `DIVIDEND_EVENT_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING`.
- Dividend provider evidence request approval completed and remains source evidence only.
- Dividend provider evidence execution retry digest: `NOT_CREATED`.
- Dividend provider evidence execution completed on `feature/dividend-provider-evidence-execution-live-run-retry2-v1` as `DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED` / `DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY`.
- Successful dividend provider evidence execution digest: `4759a412411f7019090bd89ebc1d44040f5b2fe895074ccc9a08c21852b009d9`.
- Successful execution created `7` ignored sanitized outputs from `12` read-only provider requests: `12` successful responses and `0` failed responses.
- Dividend evidence results review implemented as `DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE` / `DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY`.
- Dividend evidence results review package digest: `ce32ad46c0a48be9a763ea1570aef0c9ba6b4ef3c96d1ea82f2884aaf7fd9007`.
- The results review supports future dividend authority planning but creates no dividend authority or freeze.
- Dividend policy reconciliation review implemented as `DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE` / `DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY`.
- Dividend policy reconciliation review digest: `fd671ad814765dabacb06bcd51627efe2052bf10d8d0cf40e37b862a75e02ff0`.
- Dividend policy reconciliation approval implemented as `DIVIDEND_POLICY_RECONCILIATION_APPROVED` with scope `DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY`.
- Dividend policy reconciliation approval digest: `96f146e4ce0257c8cf84c8b6d26e620ba485a8c3c575e4335c42be36e3870d62`.
- Adjusted-price, cash/special-dividend, and zero-row absence decisions are approved for future dividend-authority freeze input only; total return and reinvestment remain not assumed.
- Policy approval sets readiness for a separate dividend freeze ceremony but creates no dividend authority or freeze.
- Dividend event authority freeze ceremony implemented as `DIVIDEND_EVENT_AUTHORITY_FROZEN` with scope `DIVIDEND_EVENT_AUTHORITY_ONLY`.
- Dividend event authority freeze digest: `98b7e740b750701eb1e63e6e0ad88ffd4d665c44ece2e0e85e0a15e4a2a4d6ae`.
- Dividend event authority created/frozen: `True / True` only within the dividend-event authority scope.
- The freeze checklist passes `66 / 66` checks with `0` blockers.
- Split event authority remains frozen.
- Combined split/dividend corporate-action readiness remains future work.
- Corporate-action authority remains not created.
- Acquisition and dataset chains remain future work.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains future and separate.

## Next Tasks
1. Combined Split/Dividend Corporate-Action Readiness Review Package v1.
2. Corporate-action authority approval only if separately required.
3. Acquisition and dataset chains only after their separate authority gates.
