# MarketFlow Corporate-Action Authority v1 Plan

## Purpose
- Create an offline, digest-bound planning chain for future split-event and dividend-event authority.
- Use the approved post-identity-freeze registry inventory as source evidence.
- Keep this phase planning-only and non-actionable.

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
1. Combined corporate-action readiness review after split and dividend freeze.
2. Corporate-action authority approval ceremony, if required.
3. Acquisition generation candidate only after identity and corporate-action authority.
4. Canonical dataset candidate only after acquisition generation freeze.
5. Research registry approval only after canonical dataset freeze.

## Non-Goals
- No Massive.com / Polygon provider request.
- No provider refresh, provider transport enablement, or live validation rerun.
- No corporate-action authority approval.
- No split event authority candidate, approval, or freeze.
- No dividend event authority candidate, approval, or freeze.
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
- Corporate-action authority remains not created.
- Split event authority remains not created.
- Dividend event authority remains not created.
- Acquisition and dataset chains remain future work.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains future and separate.

## Next Tasks
1. Corporate-action authority plan candidate operator review package.
2. Corporate-action authority plan approval ceremony, if required.
3. Split event authority candidate.
4. Dividend event authority candidate.
5. Acquisition generation chain only after corporate-action authority.
