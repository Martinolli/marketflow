# MarketFlow Corporate-Action Authority v1 Plan

## Purpose
- Maintain an offline, digest-bound corporate-action chain across completed split/dividend event freezes and the combined readiness review.
- Use the approved post-identity-freeze registry inventory as source evidence.
- Keep the combined readiness phase review-only and non-authorizing.

## Source Identity Registry Inventory Approval
- Source artifact: `POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED`
- Source approval digest: `c380dd016035289d11b79723daafc6bdec694928233ff464ec386239ea820c82`
- Source review package digest: `d35861b3bb19d361241df0e6ba080306e647116cf5b12815ce1ddf2fb48cf51c`
- Source registry inventory candidate digest: `459f20151cf531b32de91defb7d0a676b20ad68a13b4f391840a0e1db921ea34`
- Source identity freeze digest: `55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30`
- Approval scope: `IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY`

## Target Universe
- Target universe count: `12`
- Target universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`

## Split Event Authority Planning Method
- Create a split event authority candidate as a future artifact.
- Bind each future candidate to the identity freeze and registry inventory approval digests.
- Require operator review before any split event authority is created or frozen.
- Require a separate provider evidence request approval before any live provider execution, if live evidence is needed.
- Treat unavailable future split fields as unavailable in the future candidate.
- Do not infer zero split events from this plan.

## Dividend Event Authority Planning Method
- Create a dividend event authority candidate as a future artifact.
- Bind each future candidate to the identity freeze and registry inventory approval digests.
- Require operator review before any dividend event authority is created or frozen.
- Require a separate provider evidence request approval before any live provider execution, if live evidence is needed.
- Treat unavailable future dividend fields as unavailable in the future candidate.
- Do not infer zero dividend events from this plan.

## Dividend Policy And Adjusted/Unadjusted Data Implication
- Future dividend authority work must identify cash dividend amount, currency, ex-date, record date if available, pay date if available, and provider event ID if available.
- Future dividend policy reconciliation must explicitly document adjusted and unadjusted data implications before acquisition or dataset generation.
- This plan does not fetch, reconcile, approve, or freeze dividend evidence.

## Future Corporate-Action Readiness Chain
1. Combined corporate-action readiness review after split and dividend freeze: completed.
2. Corporate-action authority approval ceremony, if required.
3. Acquisition generation candidate only after identity and corporate-action authority.
4. Canonical dataset candidate only after acquisition generation freeze.
5. Research registry approval only after canonical dataset freeze.

## Non-Goals
- No Massive.com / Polygon provider request.
- No provider refresh, provider transport enablement, or live validation rerun.
- No corporate-action authority freeze; approval is limited to `CORPORATE_ACTION_AUTHORITY_ONLY`.
- No alteration or rerun of the completed split event authority freeze.
- No alteration or rerun of the completed dividend event authority freeze.
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
- `no_dividend_event_authority_without_operator_review`
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
- `operator_approval_required_before_any_provider_corporate_action_evidence_request`

## Implementation Status
- Corporate-action authority plan candidate implemented: `CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE`.
- Candidate status: `CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW`.
- Candidate digest: `3ab988e647eebf01ea489dd3e9da2a1edf7b9c8a50b26a54995d39cc3115753a`.
- Operator review package implemented: `CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE`.
- Operator review package status: `CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY`.
- Operator review package digest: `6d0acf97fb36e5302d62c4077ef0dd902a36dc9bf88c7f0234fef07c516bf9c1`.
- Corporate-action authority plan approval implemented: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED`.
- Corporate-action authority plan approval status: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED`.
- Corporate-action authority plan approval scope: `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY`.
- Corporate-action authority plan approval digest: `bd02155f618bee231e4472049963343d57b7585920653b31aa5518e96ded0d2f`.
- Corporate-action authority plan approval sets `ready_for_split_event_authority_candidate` to `True`.
- Corporate-action authority plan approval sets `ready_for_dividend_event_authority_candidate` to `True`.
- Split event authority freeze completed with scope `SPLIT_EVENT_AUTHORITY_ONLY` and digest `37a06dceac17761319f9d5eb716d64dced765997b8d1e9d8a79166162bfdb303`.
- Dividend event authority freeze completed with scope `DIVIDEND_EVENT_AUTHORITY_ONLY` and digest `98b7e740b750701eb1e63e6e0ad88ffd4d665c44ece2e0e85e0a15e4a2a4d6ae`.
- Combined split/dividend corporate-action readiness review implemented as `COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE` / `COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY`.
- Combined readiness review digest: `ee425cb1ee8b9e513d3ed4bc5ddc05ca7498a3003bc5820c5a2b5014f799d621`.
- The review checklist passes `56 / 56` checks with `0` blockers and supports a future corporate-action approval ceremony.
- Combined split/dividend readiness review is completed and remains the approval source evidence.
- Corporate-action authority approval ceremony implemented as `CORPORATE_ACTION_AUTHORITY_APPROVED` with scope `CORPORATE_ACTION_AUTHORITY_ONLY`.
- Corporate-action authority is created and approved but not frozen.
- Acquisition generation chain remains future and separate work.
- Dataset generation chain remains future and separate work.
- Acquisition and dataset chains remain future work.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains future and separate.

## Next Tasks
1. Acquisition Generation Chain Candidate v1.
2. Acquisition generation operator review and approval only through separate gates.
3. Canonical dataset and registry chains only after their separate gates.
4. Predictive usefulness and profitability remain not accepted; runtime activation remains future and separate.
