# MarketFlow Feature/Label Refinement v1 Plan

## Purpose

Define an offline, digest-bound, research-only candidate plan for future feature, label, protocol, and model-comparison refinements responding to mixed stability and insufficient baseline outperformance. This document plans future work; it does not approve or execute it.

## Source Improvement Candidate Review

- Source artifact/status: `PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE` / `PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_READY`.
- Review digest: `88bb2540222082241fcdc2c14007828d711d8adbbcf9b2518d5131d34b794ce9`.
- Reviewed candidate digest: `3f993453ad80705a3bc002891d1def677d15f2a92044109efa3e4cfe9349d43d`.
- Candidate artifact/status: `FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE` / `FEATURE_LABEL_REFINEMENT_PLAN_READY_FOR_OPERATOR_REVIEW`.
- Candidate digest: `96266cb3869885c4c33025422b7730f4c3e1399967ef541dc0b0eb808480daf8`.

## Readiness Failure Basis

- Decision/reason: `PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY` / `MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE`.
- Stability and baseline-outperformance consistency: `FAIL_OR_NOT_MET / FAIL_OR_NOT_MET`.
- Walk-forward range: `0.498698 to 0.562842`; OOS majority/previous/cross-sectional: `0.539491 / 0.495984 / 0.502677`; Brier: `0.24875351`.
- Leakage remains `PASS` with `0` failed controls. This does not override the readiness failure.

## Planned Label Refinement Groups

- `return_bucket_threshold_refinement`
- `multi_horizon_label_refinement`
- `volatility_regime_window_refinement`
- `drawdown_risk_threshold_refinement`
- `flat_return_tolerance_review`
- `class_imbalance_review`
- `label_availability_boundary_review`

## Planned Feature Refinement Groups

- `vpa_feature_refinement`
- `relative_strength_feature_refinement`
- `cross_ticker_context_feature_refinement`
- `calendar_session_feature_refinement`
- `data_quality_flag_enrichment`
- `missingness_indicator_enrichment`
- `meta_reduced_record_count_feature_handling`
- `volatility_momentum_interaction_features`
- `baseline_error_context_features`

## Planned Protocol Refinement Groups

- `walk_forward_window_policy_refinement`
- `embargo_gap_policy_refinement`
- `stability_threshold_definition`
- `baseline_outperformance_threshold_definition`
- `calibration_acceptance_threshold_definition`
- `oos_generalization_threshold_definition`

## Planned Model Comparison Groups

- `regularized_linear_baseline_comparison`
- `tree_based_baseline_comparison_if_available`
- `simple_ensemble_baseline_comparison_if_available`
- `per_ticker_vs_cross_sectional_model_review`
- `global_vs_sector_like_grouping_review_if_available`

## Refinement Priority

- Priority 1: define baseline-outperformance and walk-forward policies, refine return-bucket thresholds, and refine relative-strength features.
- Priority 2: refine VPA features and volatility-regime windows, define calibration acceptance, and enrich data-quality flags.
- Priority 3: plan model comparisons, alternative horizons, and drawdown-risk threshold refinement.
- Priority does not authorize any refinement or comparison.

## Future Refinement Chain

1. Feature/Label Refinement Plan Candidate Operator Review Package.
2. Feature/Label Refinement Plan Approval Ceremony, if selected.
3. Feature/Label Refinement Execution Candidate.
4. Additional Predictive Evidence Execution Candidate for refined evidence.
5. Additional Predictive Evidence Execution Approval Ceremony, if required.
6. Additional Predictive Evidence Execution.
7. Additional Predictive Evidence Results Review.
8. Predictive Usefulness Reassessment Review rerun.
9. Predictive Usefulness Acceptance Readiness Review rerun.
10. Predictive Usefulness Acceptance Candidate, only if readiness passes.
11. Profitability review chain, if separately required.
12. Runtime migration chain, if ever separately authorized.

## Future Gates

- `feature_label_refinement_plan_candidate_operator_review`
- `feature_label_refinement_plan_approval_if_selected`
- `feature_label_refinement_execution_candidate`
- `additional_predictive_evidence_execution_candidate_for_refined_evidence`
- `additional_predictive_evidence_execution_approval_if_required`
- `additional_predictive_evidence_execution`
- `additional_predictive_evidence_results_review`
- `predictive_usefulness_reassessment_review_rerun`
- `predictive_usefulness_acceptance_readiness_review_rerun`
- `predictive_usefulness_acceptance_candidate_if_ready`
- `profitability_review_chain_if_required`
- `runtime_migration_chain_if_ever_authorized`

## Risk Controls

- Require operator approval before refinement execution and the appropriate execution approval before labels, features, comparisons, or evidence reruns.
- Do not derive predictive-usefulness acceptance from this plan, accept when readiness is unmet, or infer profitability.
- Do not mutate the frozen canonical dataset or repair META's exact `913`-record limitation.
- Do not switch runtime sources, stitch automatically, paper trade, call brokers, score strategies, or generate trade recommendations.
- Label all planned outputs research-only and non-actionable.

## Non-Goals

- Provider requests, market-data acquisition, dataset or canonical regeneration.
- Label, feature, validation, OOS, metrics, improvement, refinement, or model-comparison execution.
- Additional predictive-evidence execution candidacy, approval, execution, or results.
- Predictive-usefulness or profitability acceptance.
- Runtime migration, strategy use, paper trading, broker execution, or recommendations.

## Guardrails

- Bind only the exact reviewed source and inherited evidence digests.
- Preserve the exact 12-ticker order and frozen record counts.
- Keep every refinement group `PLANNED_NOT_EXECUTED`, `NOT_AUTHORIZED`, `NOT_EXECUTED`, research-only, and non-actionable.
- Keep planned outputs `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.
- Fail closed on changed source evidence, missing plan sections or digests, and any downstream authority signal.

## Current Progress

- Feature/Label Refinement Plan Candidate v1 is completed.
- Feature/Label Refinement Plan Candidate Operator Review Package v1 is implemented.
- Feature/Label Refinement Plan Approval Ceremony v1 is implemented.
- Feature/Label Refinement Execution Candidate v1 is implemented as an offline, digest-bound candidate only.
- Feature/Label Refinement Execution Candidate Operator Review Package v1 is implemented as a review-only layer.
- Separate execution approval remains future work if selected; refinement execution and results review remain future work.
- Approval authorizes only execution-candidate planning; refinement execution remains not authorized and not performed.
- Additional Predictive Evidence Execution Candidate remains future work.
- Predictive usefulness acceptance remains closed, profitability remains `not accepted`, and runtime activation remains separate future work.

## Next Tasks

1. Feature/Label Refinement Execution Approval Ceremony v1, if selected.
2. Feature/Label Refinement Execution v1, only after separate approval.
3. Feature/Label Refinement Results Review Package v1, only after execution.
