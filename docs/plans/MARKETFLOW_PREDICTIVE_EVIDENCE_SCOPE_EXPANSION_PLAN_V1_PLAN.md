# MarketFlow Predictive Evidence Scope Expansion Plan v1

## Purpose
- Define how future predictive evidence may be expanded beyond the current single-ticker AAPL evidence.
- Address `single_ticker_scope`, `no_multi_ticker_or_out_of_domain_generalization`, and `single_asset_class_scope_if_applicable`.
- Preserve the current conclusion that predictive usefulness acceptance is not ready.
- This plan does not select tickers, approve a ticker universe, create ticker authority, acquire data, or execute additional evidence.

## Source Evidence And Current Limitation
- Additional predictive evidence plan candidate review package digest: `24b19efc1fdb4cbf64c02f15011becd1872301efe596a4d8bb7989f8be299b8a`
- Additional predictive evidence plan candidate digest: `af23d2de4b77470f5d60622704312eee28fb857ebd9dfe81c1b288932cd6430f`
- Predictive usefulness acceptance readiness candidate review package digest: `17c43213689f45e7af9641354cae0e145bb71091d092b4abc856004ab9d7ba57`
- Predictive usefulness acceptance readiness candidate digest: `c6562d04616327bd1b293f36f9f80aa0c0713a02508e4f558803d0c528fd768e`
- Predictive experiment results review package digest: `281e2f0ce4f6050b4788188202003605af95af104b887374484bb1f46ce2b804`
- Current limitation: the available predictive evidence is research-only and still limited by single-ticker scope.
- acceptance_readiness_state: `NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE`
- predictive_evidence_sufficient_for_acceptance: `False`
- ready_for_acceptance_candidate: `False`

## Current Review Package
- Predictive evidence scope expansion plan candidate completed: `True`
- Predictive evidence scope expansion plan candidate digest: `daddabc04829ac2379c4439220d018d8b3b3403c35edb469e95e7b24ea6bd13f`
- Predictive evidence scope expansion plan candidate operator review package implemented: `True`
- Predictive evidence scope expansion plan candidate review package digest: `c94fd093f1e221e9dca127e44a3a788880602c570e9051b6e19666f1db142156`
- Ticker universe selection candidate remains future work.
- Scope expansion approval remains future work.
- New ticker authority remains future work.
- Predictive usefulness remains not accepted.
- Profitability remains not accepted.
- Runtime activation remains future and separate.

## Scope Expansion Objective
- scope_expansion_objective: `EXPAND_PREDICTIVE_EVIDENCE_BEYOND_SINGLE_TICKER_AAPL`
- scope_expansion_mode: `PLANNED_NOT_AUTHORIZED`
- new_ticker_selection_status: `NOT_SELECTED`
- new_ticker_authority_status: `NOT_CREATED`
- new_data_acquisition_status: `NOT_AUTHORIZED`
- approved_expanded_ticker_universe: `[]`

## Expansion Dimensions
- `ticker_count_expansion`: plan evidence beyond the current single AAPL ticker scope.
- `sector_or_industry_diversity`: plan cross-sector evidence before generalization is reassessed.
- `liquidity_regime_diversity`: plan evidence across liquidity profiles.
- `volatility_regime_diversity`: plan evidence across volatility regimes.
- `market_cap_or_size_diversity`: plan future size-profile coverage.
- `price_level_diversity`: plan price-level variation checks.
- `volume_profile_diversity`: plan volume-profile coverage.
- `time_period_or_regime_extension`: plan future time-regime coverage if separately authorized.
- `dataset_profile_replication`: plan replication across SWING and POSITION_SWING research profiles.
- `out_of_domain_generalization`: plan out-of-domain evidence before any usefulness acceptance candidate.

## Ticker Selection Policy
- ticker_selection_policy_status: `CRITERIA_DEFINED_SELECTION_NOT_PERFORMED`
- candidate_ticker_list_status: `NOT_BOUND`
- minimum_additional_ticker_count: `planned`
- target_additional_ticker_count_range: `5_to_12`
- Final ticker selection is not performed in this plan.
- Any future ticker candidate must satisfy the planned criteria before authority-chain work begins.

## Planned Selection Criteria
- `must_be_common_stock_or_explicitly_approved_security_type`
- `must_have_valid_identity_segment`
- `must_have_calendar_mapping`
- `must_have_split_event_audit`
- `must_have_dividend_event_audit_or_explicit_no_dividend_policy`
- `must_have_acquisition_generation_authority`
- `must_have_canonical_dataset_freeze_for_SWING`
- `must_have_canonical_dataset_freeze_for_POSITION_SWING`
- `must_have_research_registry_approval`
- `must_have_file_availability_verification`
- `must_remain_research_only`
- `must_not_authorize_runtime_or_trading`

## Required Authority Chain For Future Selected Tickers
1. Identity segment candidate/review/freeze.
2. Exchange calendar candidate/review/freeze or reuse approved calendar if valid.
3. Split event audit candidate/provider evidence/review/freeze.
4. Dividend event audit candidate/provider evidence/review/freeze.
5. Acquisition generation candidate/live generation/triage/freeze.
6. Canonical dataset candidate/review/freeze for SWING.
7. Registry approval for SWING research dataset.
8. Canonical dataset candidate/review/freeze for POSITION_SWING.
9. Registry approval for POSITION_SWING research dataset.
10. Read-only registry discovery.
11. Dataset file availability verification.
12. Research applicability campaign plan/execution/review.
13. Predictive experiment plan/execution/review.
14. Predictive usefulness assessment.
15. Acceptance readiness reassessment.

## Planned Outputs
- `scope_expansion_plan_manifest`
- `ticker_selection_criteria_report`
- `expansion_dimension_matrix`
- `future_ticker_authority_chain_template`
- `scope_expansion_risk_register`
- `dataset_replication_requirements_report`
- `multi_ticker_research_campaign_plan_template`
- `generalization_evidence_requirements_report`
- `operator_decision_gate_plan`
- `non_runtime_boundary_confirmation_plan`

All planned outputs are `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Future Gates
- `scope_expansion_plan_operator_review`
- `ticker_universe_selection_candidate`
- `ticker_universe_selection_operator_review`
- `ticker_universe_selection_approval_ceremony`
- `identity_authority_chain_per_selected_ticker`
- `corporate_action_audit_chain_per_selected_ticker`
- `acquisition_generation_chain_per_selected_ticker`
- `canonical_dataset_chain_per_selected_ticker`
- `research_registry_approval_per_selected_ticker`
- `dataset_file_availability_verification_per_selected_ticker`
- `multi_ticker_research_campaign_execution_candidate`
- `multi_ticker_predictive_experiment_execution_candidate`
- `multi_ticker_predictive_usefulness_assessment`
- `acceptance_readiness_reassessment_after_expansion`

## Non-Goals
- Do not execute scope expansion.
- Do not create `PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_APPROVED`.
- Do not create `EXPANDED_TICKER_UNIVERSE_APPROVED`.
- Do not create `NEW_TICKER_AUTHORITY_APPROVED`.
- Do not select final tickers.
- Do not validate live tickers.
- Do not acquire data for new tickers.
- Do not create `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED`.
- Do not create `PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE`.
- Do not accept predictive usefulness.
- Do not accept profitability.
- Do not recommend, approve, activate, or default runtime migration.
- Do not generate trade recommendations.

## Guardrails
- No Massive.com / Polygon provider request.
- No provider data fetch.
- No ticker selection.
- No live ticker validation.
- No new ticker authority.
- No acquisition.
- No dataset regeneration.
- No predictive experiment, walk-forward, label, or feature-matrix rerun.
- No strategy scoring.
- No runtime, strategy, paper-trading, or broker authorization.
- Operator approval is required before any future ticker chain begins.

## Next Tasks
1. Operator assessment of the predictive evidence scope expansion plan candidate review package.
2. Ticker universe selection candidate only after explicit operator direction.
3. Ticker universe selection operator review.
4. Per-ticker authority chain, if approved.
5. Additional predictive evidence execution only after new evidence exists.
