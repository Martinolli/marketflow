# MarketFlow Expanded Universe Per-Ticker Identity Authority v1 Plan

## Scope
- This plan is an offline, research-only plan for future per-ticker identity authority across the validated expanded universe.
- This plan is not an identity authority candidate, identity freeze, corporate-action authority, acquisition authorization, dataset generation authorization, registry approval, predictive acceptance, profitability acceptance, runtime approval, paper trading approval, broker execution approval, or trade recommendation.

## Source Evidence Required Before Plan Review
- Live ticker validation results review package digest: `ebaa8b85894ec0eb6b29571c4f473d21b346d86e092a4e68158a401cb9ff7033`
- Live ticker validation execution digest: `96cdb4e97ea6255ddd04bd578a893a28c7a689b5e6d8247f9a26c341226d1ace`
- Live ticker validation approval digest: `2bf668bb4aae3756652ee5eea790b76d1ba73bdd7723efc1c31227c5c3e897e4`
- Ticker universe selection approval digest: `e0b56da411ada20f40fbefdcf74c1cce75ca86d13931471f518ef970db23188c`
- Predictive evidence scope expansion plan candidate review package digest: `c94fd093f1e221e9dca127e44a3a788880602c570e9051b6e19666f1db142156`

## Universe
- Tickers: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`
- Required source validation status for each ticker: `VALIDATED_READ_ONLY`
- Required identity authority plan status for each ticker: `PLANNED_NOT_CREATED`
- Required identity candidate status for each ticker: `NOT_CREATED`
- Required identity review status for each ticker: `NOT_CREATED`
- Required identity freeze status for each ticker: `NOT_FROZEN`

## Identity Fields To Bind
- `ticker`
- `provider_canonical_ticker_if_available`
- `provider_name_if_available`
- `security_type_if_available`
- `market_if_available`
- `locale_if_available`
- `primary_exchange_if_available`
- `active_status_if_available`
- `currency_if_available`
- `cik_if_available`
- `composite_figi_if_available`
- `share_class_figi_if_available`
- `source_endpoint`
- `provider_response_digest`
- `sanitized_validation_digest`

## Field Groups
- `core_symbol_identity_fields`
- `provider_reference_identity_fields`
- `security_classification_fields`
- `exchange_and_market_fields`
- `provider_cross_reference_fields`
- `audit_digest_fields`
- `limitation_fields`

## Evidence Limitations
- `reference_details_only`
- `corporate_action_availability_not_evaluated_by_selected_endpoint`
- `historical_aggregate_availability_not_evaluated_by_selected_endpoint`
- `identity_freeze_not_created`

## Future Authority Chain
1. Per-ticker identity authority candidate.
2. Per-ticker identity candidate operator review package.
3. Identity evidence discrepancy triage, if required.
4. Per-ticker identity authority freeze ceremony.
5. Post-freeze identity registry/read-only discovery.
6. Corporate-action authority chain only after identity freeze.
7. Acquisition generation chain only after identity and corporate-action authority.
8. Canonical dataset chain only after acquisition freeze.
9. Research registry approval only after canonical dataset freeze.

## Future Gates
- `expanded_universe_identity_authority_plan_operator_review`
- `per_ticker_identity_authority_candidate`
- `per_ticker_identity_authority_candidate_operator_review`
- `per_ticker_identity_authority_freeze_approval`
- `identity_discrepancy_triage_if_needed`
- `post_identity_freeze_registry_inventory`
- `corporate_action_authority_chain_candidate`
- `acquisition_generation_chain_candidate`
- `canonical_dataset_chain_candidate`
- `research_registry_chain_candidate`

## Planned Outputs
- `expanded_universe_identity_authority_plan_manifest`
- `per_ticker_identity_evidence_requirement_matrix`
- `identity_field_mapping_template`
- `identity_discrepancy_triage_template`
- `per_ticker_identity_candidate_template`
- `per_ticker_identity_review_template`
- `identity_freeze_checklist_template`
- `post_identity_freeze_registry_inventory_template`
- `operator_review_summary_template`

## Risk Controls
- `no_provider_refresh_without_authority`
- `no_raw_provider_payload_commit`
- `no_api_key_storage_or_printing`
- `no_identity_freeze_without_operator_ceremony`
- `no_corporate_action_authority_without_identity_freeze`
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
- `operator_approval_required_before_identity_authority_creation`

## Non-Goals
- No provider call, provider refresh, provider transport enablement, or live validation rerun.
- No identity authority freeze.
- No split or dividend event authority.
- No acquisition generation authority.
- No canonical dataset generation.
- No research registry approval.
- No additional predictive evidence execution.
- No predictive experiment, walk-forward, label, feature-matrix, or strategy-scoring rerun.
- No predictive-usefulness acceptance or profitability acceptance.
- No runtime migration, runtime use, strategy use, paper trading, broker execution, automatic stitching, or trade recommendation.

## Operator Review Outcome Needed
- The next allowable step is operator assessment of the `EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE` artifact.
- A later per-ticker identity authority freeze remains a separate ceremony and requires separate operator approval.

## Implementation Status
- Identity authority plan candidate completed: `EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE`.
- Operator review package implemented: `EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE`.
- Plan candidate reviewed through the plan candidate operator review package.
- Identity authority candidate implemented: `EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE`.
- Identity authority candidate operator review package implemented: `EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE`.
- Identity authority candidate review package digest: `31f010bb328dd71f578ea5c99cc1cb54332a6840d9693b373b73ac688ee118eb`.
- Identity freeze remains future work.
- Corporate-action chain remains future work.
- Acquisition and dataset chains remain future work.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains future and separate.
