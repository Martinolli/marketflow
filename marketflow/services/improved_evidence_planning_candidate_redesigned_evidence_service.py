"""Offline planning candidate for improved evidence using redesigned evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    label_objective_redesign_results_review_redesigned_evidence_service as source_review,
)


ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE = (
    "IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1 = (
    "improved_evidence_planning_candidate_using_redesigned_evidence_v1"
)
IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW = (
    "IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
)
IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID = (
    "IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID"
)

DEFAULT_BRANCH = "feature/improved-evidence-planning-candidate-redesigned-evidence-v1"
DEFAULT_BASE_COMMIT = "228b9f1251be099b6b2e96e540f3092010da3d08"
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = (
    "6bbf7af2ae72e33dbc0a86da2b8ba8faa05edeea982baea89c6b511b3cd7d1f4"
)
EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "1ec655cff3efcb14bb7f72e6fe0debaf067850c686b539c6e9359d881186eb00"
)
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = (
    "a86063a3de2517af101ca23bc985939c7ede69c7848372b148d7d44fb6f42778"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "4ffb335cd01041c6db16974b2f9733b6235d96bfe941cd6c3739d99c45a894c7"
)

BOUND_DIGESTS = {
    "label_objective_redesign_results_review_using_redesigned_evidence_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
    "label_objective_redesign_execution_using_redesigned_evidence_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
    "label_objective_redesign_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
    "label_objective_redesign_approval_using_redesigned_evidence_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
    "label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest": "66ef0356d4bb73fe405db5e56cfa8ab10d499fc842d2906e3aeaf56c85df2494",
    "label_objective_redesign_candidate_using_redesigned_evidence_digest": "3ee05e4b4316d9dd874a3916fed7cf8ee8aa3f73ba7596d0f9473a9714145e45",
    "label_objective_target_definition_results_review_using_redesigned_evidence_digest": "682907f87575b8fde514c6db17b141420bfd55781b0b77c297ba358a378aff46",
    "label_objective_target_definition_review_execution_using_redesigned_evidence_digest": "7b5c299191abfd6aa8ef33ebed804757a2d57a6fb966ed1d51c78d1b233abe30",
    "label_objective_target_definition_review_output_binding_digest": "7efd91b24e1af35f93e37dc9bbb5e90fe03f1080f6296abe57afdbd326d0fbee",
    "label_objective_target_definition_review_approval_using_redesigned_evidence_digest": "01f667deeea9a478dca8e1f326b672ffbcedbf9c0a0b3da93d3fac1714c622db",
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest": "ebf9f1dddddc37167c457c64f28baab021b50249987e888e1ea0a31c78102d45",
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": "735d531f39c3eac771694b9044ed67f62c9aecbdc9ca0d5cd3e3368c45caf892",
    "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": "d56519f9eb9dbb3249a365893db080d65fee8fcccbea2a8f0839300f8d006c22",
    "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": "6c6e5019a5ce312b12e4b792ce989524ba5bf16f82b5f6e532ec742f99eba4da",
    "predictive_usefulness_reassessment_using_redesigned_evidence_digest": "32cd6e52de25584df7b54866034fbb378fad8dfe1e3f1656994dbd554d1b4985",
    "additional_predictive_evidence_results_review_using_redesigned_labels_digest": "90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed",
    "additional_predictive_evidence_execution_using_redesigned_labels_digest": "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b",
    "feature_label_matrix_digest": "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad",
    "feature_values_digest": "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1",
    "redesigned_label_values_digest": "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f",
    "research_registry_approval_digest": "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958",
    "records_digest": "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044",
}

TARGET_UNIVERSE = list(source_review.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(source_review.EXPECTED_RECORD_COUNTS)
SELECTED_DIRECTION = "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

CANDIDATE_OBJECTIVE = (
    "PREPARE_OPTIONAL_IMPROVED_EVIDENCE_PLAN_FOR_NO_TRADE_ABSTAIN_LABEL_OBJECTIVE_REDESIGN"
)
CANDIDATE_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
CANDIDATE_MODE = PLANNED_NOT_EXECUTED
CANDIDATE_AUTHORITY_STATUS = NOT_AUTHORIZED

IMPROVED_EVIDENCE_THEME_IDS = [
    "IMPROVED_EVIDENCE_THEME_NO_TRADE_ABSTAIN_LABEL_DESIGN",
    "IMPROVED_EVIDENCE_THEME_MATERIAL_MOVE_TARGET_DESIGN",
    "IMPROVED_EVIDENCE_THEME_CLASS_BALANCE_AND_COVERAGE_POLICY",
    "IMPROVED_EVIDENCE_THEME_HORIZON_SPECIFIC_SIGNAL_VALIDATION",
    "IMPROVED_EVIDENCE_THEME_TICKER_OR_REGIME_SPLIT_VALIDATION",
    "IMPROVED_EVIDENCE_THEME_RISK_ADJUSTED_TARGET_VALIDATION",
    "IMPROVED_EVIDENCE_THEME_FEATURE_LABEL_ALIGNMENT_REVIEW",
    "IMPROVED_EVIDENCE_THEME_BASELINE_OUTPERFORMANCE_THRESHOLD_POLICY",
    "IMPROVED_EVIDENCE_THEME_CALIBRATION_AND_CONFIDENCE_REVIEW",
    "IMPROVED_EVIDENCE_THEME_META_LIMITATION_HANDLING",
    "IMPROVED_EVIDENCE_THEME_ACCEPTANCE_READINESS_PREREQUISITES",
]

PLANNED_EVIDENCE_COMPONENT_IDS = [
    "COMPONENT_REDESIGNED_LABEL_SCHEMA_CANDIDATE",
    "COMPONENT_NO_TRADE_ABSTAIN_COVERAGE_ANALYSIS",
    "COMPONENT_MATERIAL_MOVE_THRESHOLD_ANALYSIS",
    "COMPONENT_HORIZON_SPECIFIC_EVALUATION_PLAN",
    "COMPONENT_TICKER_REGIME_EVALUATION_PLAN",
    "COMPONENT_FEATURE_LABEL_ALIGNMENT_PLAN",
    "COMPONENT_CHRONOLOGICAL_SPLIT_AND_EMBARGO_POLICY",
    "COMPONENT_BASELINE_AND_LOCAL_MODEL_COMPARISON_PLAN",
    "COMPONENT_CROSS_SECTIONAL_MODEL_COMPARISON_PLAN",
    "COMPONENT_CALIBRATION_AND_BRIER_REVIEW_PLAN",
    "COMPONENT_LEAKAGE_AND_NO_PEEK_CONTROL_PLAN",
    "COMPONENT_PER_TICKER_AND_META_LIMITATION_REPORTING_PLAN",
    "COMPONENT_OPERATOR_RESULTS_REVIEW_TEMPLATE",
]

PLANNED_DATA_PRODUCT_IDS = [
    "improved_evidence_planning_candidate_manifest",
    "proposed_label_schema_template",
    "no_trade_abstain_coverage_template",
    "material_move_threshold_template",
    "horizon_specific_validation_template",
    "ticker_regime_split_validation_template",
    "feature_label_alignment_template",
    "chronological_split_embargo_template",
    "baseline_model_comparison_template",
    "calibration_brier_template",
    "leakage_no_peek_control_template",
    "per_ticker_meta_reporting_template",
    "operator_review_summary_template",
]

PLANNED_FUTURE_OUTPUT_IDS = [
    "future_improved_evidence_execution_manifest",
    "future_redesigned_label_schema_report",
    "future_feature_label_matrix_report",
    "future_walk_forward_results",
    "future_oos_results",
    "future_baseline_model_comparison",
    "future_metric_family_results",
    "future_calibration_stability_report",
    "future_leakage_quality_control_report",
    "future_per_ticker_meta_review",
    "future_operator_review_summary",
    "future_digest_manifest",
]

NEXT_CHAIN = [
    "Optional Improved Evidence Planning Candidate Operator Review Using Redesigned Evidence v1.",
    "Optional Improved Evidence Planning Approval Using Redesigned Evidence v1, if selected.",
    "Optional Improved Evidence Planning Execution Using Redesigned Evidence v1, if approved.",
    "Optional Improved Evidence Planning Results Review Using Redesigned Evidence v1.",
    "Optional Additional Predictive Evidence Execution Candidate Using Improved Evidence v1, if supported.",
    "Optional Additional Predictive Evidence Execution Approval and Execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "improved_evidence_planning_candidate_operator_review_using_redesigned_evidence",
    "improved_evidence_planning_approval_using_redesigned_evidence_if_selected",
    "improved_evidence_planning_execution_using_redesigned_evidence_if_approved",
    "improved_evidence_planning_results_review_using_redesigned_evidence",
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_if_supported",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution_if_approved",
    "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "candidate_does_not_approve_planning",
    "candidate_does_not_execute_planning",
    "candidate_does_not_generate_labels",
    "candidate_does_not_create_new_targets",
    "candidate_does_not_authorize_target_definition_change",
    "candidate_does_not_generate_features",
    "candidate_does_not_create_feature_label_matrix",
    "candidate_does_not_create_predictive_evidence_execution_candidate",
    "candidate_does_not_execute_predictive_evidence",
    "candidate_does_not_rerun_predictive_evidence",
    "candidate_does_not_retrain_models",
    "candidate_does_not_recompute_metrics",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_create_acceptance_candidate",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "do_not_mutate_label_objective_review_outputs",
    "do_not_mutate_label_objective_redesign_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

CANDIDATE_BASIS = {
    "source_results_review_ready": True,
    "results_review_classification": "COMPLETED_RESEARCH_ONLY",
    "label_objective_redesign_classification": "COMPLETED_RESEARCH_ONLY",
    "selected_direction_analysis_status": "REVIEWED_RESEARCH_ONLY",
    "selected_direction": SELECTED_DIRECTION,
    "no_trade_abstain_objective_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "flat_class_majority_structure_review": "PRESENT_REQUIRES_OPERATOR_REVIEW",
    "material_move_target_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "horizon_specific_target_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "ticker_or_regime_split_target_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "risk_adjusted_target_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "label_family_impact_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "meta_limitation_review": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
    "acceptance_threshold_prerequisite_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "redesign_decision_review": "NO_LABEL_REGENERATION_OR_NEW_TARGETS_AUTHORIZED",
    "improved_evidence_planning_candidate_readiness": "OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION",
}


class ImprovedEvidencePlanningCandidateRedesignedEvidenceError(ValueError):
    """Raised when a planning candidate violates its closed authority boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
            f"{field} mismatch"
        )


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _improved_evidence_themes() -> list[dict[str, Any]]:
    return [
        {
            "theme_id": theme_id,
            "theme_status": PLANNED_NOT_EXECUTED,
            "approval_required_before_execution": True,
            "execution_authorized": False,
            "execution_performed": False,
            "label_regeneration_authorized": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for theme_id in IMPROVED_EVIDENCE_THEME_IDS
    ]


def _planned_evidence_components() -> list[dict[str, Any]]:
    return [
        {
            "component_id": component_id,
            "component_status": PLANNED_NOT_EXECUTED,
            "execution_authorized": False,
            "label_generation_authorized": False,
            "feature_generation_authorized": False,
            "metric_computation_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for component_id in PLANNED_EVIDENCE_COMPONENT_IDS
    ]


def _planned_products(
    product_ids: list[str], *, id_field: str
) -> list[dict[str, Any]]:
    return [
        {
            id_field: product_id,
            "output_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for product_id in product_ids
    ]


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_improved_evidence_planning_candidate_digest", None)
    return payload


def per_ticker_improved_evidence_planning_candidate_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for one ticker plan entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "label_objective_redesign_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "improved_evidence_planning_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "improved_evidence_planning_approved": False,
            "improved_evidence_planning_executed": False,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "additional_predictive_evidence_execution_candidate_created": False,
            "additional_predictive_evidence_executed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "planning_note": (
                "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_CANDIDATE"
                if is_meta
                else "STANDARD_FROZEN_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_improved_evidence_planning_candidate_digest"] = (
            per_ticker_improved_evidence_planning_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


CHECK_FIELD_SPECS = [
    ("redesign_results_review_digest_bound", EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST, "label_objective_redesign_results_review_using_redesigned_evidence_digest"),
    ("redesign_execution_digest_bound", EXPECTED_SOURCE_EXECUTION_DIGEST, "label_objective_redesign_execution_using_redesigned_evidence_digest"),
    ("redesign_output_binding_digest_bound", EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST, "label_objective_redesign_output_binding_digest"),
    ("redesign_approval_digest_bound", EXPECTED_SOURCE_APPROVAL_DIGEST, "label_objective_redesign_approval_using_redesigned_evidence_digest"),
    ("redesign_candidate_review_digest_bound", BOUND_DIGESTS["label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"], "label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"),
    ("redesign_candidate_digest_bound", BOUND_DIGESTS["label_objective_redesign_candidate_using_redesigned_evidence_digest"], "label_objective_redesign_candidate_using_redesigned_evidence_digest"),
    ("target_definition_results_review_digest_bound", BOUND_DIGESTS["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], "label_objective_target_definition_results_review_using_redesigned_evidence_digest"),
    ("target_definition_execution_digest_bound", BOUND_DIGESTS["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"),
    ("path_selection_digest_bound", BOUND_DIGESTS["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], "method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
    ("readiness_review_digest_bound", BOUND_DIGESTS["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
    ("reassessment_digest_bound", BOUND_DIGESTS["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], "predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
    ("predictive_results_review_digest_bound", BOUND_DIGESTS["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], "additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
    ("predictive_execution_digest_bound", BOUND_DIGESTS["additional_predictive_evidence_execution_using_redesigned_labels_digest"], "additional_predictive_evidence_execution_using_redesigned_labels_digest"),
    ("matrix_digest_bound", BOUND_DIGESTS["feature_label_matrix_digest"], "feature_label_matrix_digest"),
    ("feature_values_digest_bound", BOUND_DIGESTS["feature_values_digest"], "feature_values_digest"),
    ("label_values_digest_bound", BOUND_DIGESTS["redesigned_label_values_digest"], "redesigned_label_values_digest"),
    ("research_registry_digest_bound", BOUND_DIGESTS["research_registry_approval_digest"], "research_registry_approval_digest"),
    ("records_digest_bound", BOUND_DIGESTS["records_digest"], "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", BOUND_DIGESTS["records_digest"], "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("source_results_review_ready_true", True, "source_results_review_ready"),
    ("ready_for_improved_evidence_planning_candidate_true", True, "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence"),
    ("planning_candidate_created_true", True, "improved_evidence_planning_candidate_created"),
    ("planning_candidate_ready_true", True, "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review"),
    ("planning_approved_false", False, "improved_evidence_planning_approved"),
    ("planning_executed_false", False, "improved_evidence_planning_executed"),
    ("selected_redesign_direction_preserved", SELECTED_DIRECTION, "selected_direction"),
    ("label_regeneration_authorized_false", False, "label_regeneration_authorized"),
    ("label_regeneration_performed_false", False, "label_regeneration_performed"),
    ("new_targets_created_false", False, "new_targets_created"),
    ("target_definition_change_authorized_false", False, "target_definition_change_authorized"),
    ("target_definition_change_performed_false", False, "target_definition_change_performed"),
    ("features_generated_false", False, "features_generated"),
    ("feature_label_matrix_created_false", False, "feature_label_matrix_created"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
    ("additional_predictive_evidence_executed_false", False, "additional_predictive_evidence_executed"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("candidate_basis_preserved", CANDIDATE_BASIS, "candidate_basis"),
    ("candidate_objective_defined", CANDIDATE_OBJECTIVE, "improved_evidence_planning_candidate_objective"),
    ("improved_evidence_themes_defined", IMPROVED_EVIDENCE_THEME_IDS, "improved_evidence_theme_ids"),
    ("planned_evidence_components_defined", PLANNED_EVIDENCE_COMPONENT_IDS, "planned_evidence_component_ids"),
    ("planned_data_products_not_generated", True, "planned_data_products_not_generated"),
    ("future_outputs_not_generated", True, "planned_future_outputs_not_generated"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_digests_present", True, "per_ticker_digests_valid"),
    ("provider_requests_made_false", False, "provider_requests_made_in_candidate"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed_in_candidate"),
    ("dataset_regeneration_false", False, "canonical_dataset_regenerated_in_candidate"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("feature_regeneration_false", False, "feature_regeneration_performed"),
    ("predictive_evidence_rerun_false", False, "predictive_evidence_execution_rerun_performed"),
    ("label_objective_target_definition_review_execution_rerun_false", False, "label_objective_target_definition_review_execution_rerun_performed"),
    ("label_objective_redesign_execution_rerun_false", False, "label_objective_redesign_execution_rerun_performed"),
    ("metric_recomputation_in_candidate_false", False, "metric_recomputation_performed_in_candidate"),
    ("model_training_in_candidate_false", False, "model_training_performed_in_candidate"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("next_chain_defined", NEXT_CHAIN, "next_chain"),
    ("next_gates_defined", NEXT_GATES, "next_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [spec[0] for spec in CHECK_FIELD_SPECS]


def _derived_fields(candidate: Mapping[str, Any]) -> dict[str, Any]:
    themes = candidate.get("improved_evidence_themes", [])
    components = candidate.get("planned_evidence_components", [])
    products = candidate.get("planned_data_products", [])
    outputs = candidate.get("planned_future_outputs", [])
    entries = candidate.get("per_ticker_planning_entries", [])
    return {
        **candidate,
        "improved_evidence_theme_ids": (
            [row.get("theme_id") for row in themes]
            if isinstance(themes, list)
            else []
        ),
        "planned_evidence_component_ids": (
            [row.get("component_id") for row in components]
            if isinstance(components, list)
            else []
        ),
        "planned_data_products_not_generated": (
            isinstance(products, list)
            and len(products) == len(PLANNED_DATA_PRODUCT_IDS)
            and all(
                row.get("output_status") == PLANNED_NOT_GENERATED
                and row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE
                and row.get("generated") is False
                for row in products
            )
        ),
        "planned_future_outputs_not_generated": (
            isinstance(outputs, list)
            and len(outputs) == len(PLANNED_FUTURE_OUTPUT_IDS)
            and all(
                row.get("output_status") == PLANNED_NOT_GENERATED
                and row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE
                and row.get("generated") is False
                for row in outputs
            )
        ),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_digests_valid": (
            isinstance(entries, list)
            and len(entries) == 12
            and all(
                isinstance(
                    row.get("per_ticker_improved_evidence_planning_candidate_digest"),
                    str,
                )
                and len(row["per_ticker_improved_evidence_planning_candidate_digest"])
                == 64
                and row["per_ticker_improved_evidence_planning_candidate_digest"]
                == per_ticker_improved_evidence_planning_candidate_digest_v1(row)
                for row in entries
            )
        ),
    }


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_fields(candidate)
    return [
        _check(check_id, expected, fields.get(field))
        for check_id, expected, field in CHECK_FIELD_SPECS
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "improved_evidence_planning_candidate_ready": not failed,
        "ready_for_operator_review": not failed,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "improved_evidence_planning_approved": False,
        "improved_evidence_planning_executed": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1,
        "candidate_status": IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_results_review_artifact_kind": source_review.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "source_results_review_status": source_review.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        **BOUND_DIGESTS,
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "label_objective_redesign_results_review_created": True,
        "label_objective_redesign_results_review_ready": True,
        "source_results_review_ready": True,
        "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence": True,
        "improved_evidence_planning_candidate_created": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_created": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_created": False,
        "improved_evidence_planning_approved": False,
        "improved_evidence_planning_authorized": False,
        "improved_evidence_planning_executed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "features_generated": False,
        "feature_label_matrix_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_migration_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_candidate": False,
        "live_provider_transport_enabled_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "metric_recomputation_performed_in_candidate": False,
        "model_training_performed_in_candidate": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe_count": 12,
        "target_universe": list(TARGET_UNIVERSE),
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "candidate_basis": deepcopy(CANDIDATE_BASIS),
        "selected_direction": SELECTED_DIRECTION,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT",
        "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540,
        "oos_evaluated_rows": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "improved_evidence_planning_candidate_objective": CANDIDATE_OBJECTIVE,
        "improved_evidence_planning_candidate_scope": CANDIDATE_SCOPE,
        "improved_evidence_planning_candidate_mode": CANDIDATE_MODE,
        "improved_evidence_planning_candidate_authority_status": CANDIDATE_AUTHORITY_STATUS,
        "improved_evidence_themes": _improved_evidence_themes(),
        "planned_evidence_components": _planned_evidence_components(),
        "planned_data_products": _planned_products(
            PLANNED_DATA_PRODUCT_IDS, id_field="data_product_id"
        ),
        "planned_future_outputs": _planned_products(
            PLANNED_FUTURE_OUTPUT_IDS, id_field="future_output_id"
        ),
        "per_ticker_planning_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _digest_payload(candidate: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(candidate))
    payload.pop(
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest",
        None,
    )
    return payload


def improved_evidence_planning_candidate_using_redesigned_evidence_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the complete candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_improved_evidence_planning_candidate_using_redesigned_evidence_v1() -> dict:
    """Build the planning-only candidate from committed, frozen facts."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate[
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest"
    ] = improved_evidence_planning_candidate_using_redesigned_evidence_digest_v1(
        candidate
    )
    validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(
        candidate
    )
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    forbidden_artifacts = {
        "IMPROVED_EVIDENCE_PLANNING_CANDIDATE_REVIEW_PACKAGE",
        "IMPROVED_EVIDENCE_PLANNING_APPROVED",
        "IMPROVED_EVIDENCE_PLANNING_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "improved_evidence_planning_approved",
        "improved_evidence_planning_authorized",
        "improved_evidence_planning_executed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "features_generated",
        "feature_label_matrix_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_candidate",
        "model_training_performed_in_candidate",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
                    f"{current} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
                    f"{current} must remain not accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(
    candidate: dict,
) -> dict:
    """Fail closed unless the artifact is exactly the candidate-only contract."""
    if not isinstance(candidate, dict):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
            "candidate must be a JSON object"
        )
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "candidate_status",
    )
    _reject_forbidden_values(candidate)

    expected = {
        **BOUND_DIGESTS,
        "source_results_review_artifact_kind": source_review.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "source_results_review_status": source_review.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe_count": 12,
        "target_universe": TARGET_UNIVERSE,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "candidate_basis": CANDIDATE_BASIS,
        "selected_direction": SELECTED_DIRECTION,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT",
        "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540,
        "oos_evaluated_rows": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "improved_evidence_planning_candidate_objective": CANDIDATE_OBJECTIVE,
        "improved_evidence_planning_candidate_scope": CANDIDATE_SCOPE,
        "improved_evidence_planning_candidate_mode": CANDIDATE_MODE,
        "improved_evidence_planning_candidate_authority_status": CANDIDATE_AUTHORITY_STATUS,
        "improved_evidence_themes": _improved_evidence_themes(),
        "planned_evidence_components": _planned_evidence_components(),
        "planned_data_products": _planned_products(
            PLANNED_DATA_PRODUCT_IDS, id_field="data_product_id"
        ),
        "planned_future_outputs": _planned_products(
            PLANNED_FUTURE_OUTPUT_IDS, id_field="future_output_id"
        ),
        "per_ticker_planning_entries": _per_ticker_entries(),
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(candidate.get(field), expected_value, field)

    true_fields = [
        "created_offline",
        "research_only",
        "operator_review_required",
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
        "label_objective_redesign_results_review_created",
        "label_objective_redesign_results_review_ready",
        "source_results_review_ready",
        "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence",
        "improved_evidence_planning_candidate_created",
        "improved_evidence_planning_candidate_using_redesigned_evidence_created",
        "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    ]
    false_fields = [
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_created",
        "improved_evidence_planning_approved",
        "improved_evidence_planning_authorized",
        "improved_evidence_planning_executed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "features_generated",
        "feature_label_matrix_created",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "profitability_acceptance_created",
        "runtime_migration_approved",
        "runtime_migration_active",
        "runtime_migration_approval_created",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_candidate",
        "live_provider_transport_enabled_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate",
        "canonical_dataset_regenerated_in_candidate",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed",
        "metric_recomputation_performed_in_candidate",
        "model_training_performed_in_candidate",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ]
    for field in true_fields:
        _expect(candidate.get(field), True, field)
    for field in false_fields:
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)

    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
            "candidate_checklist mismatch"
        )
    _expect(
        [row.get("check_id") for row in checklist],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check ids",
    )
    _expect(checklist, _checklist(candidate), "candidate_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
            "candidate_checklist must pass"
        )
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get(
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
            "missing candidate digest"
        )
    _expect(
        digest,
        improved_evidence_planning_candidate_using_redesigned_evidence_digest_v1(
            candidate
        ),
        "candidate digest",
    )
    return {
        "status": IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest": digest,
        "per_ticker_planning_entry_count": len(
            candidate["per_ticker_planning_entries"]
        ),
        "blocker_count": candidate["candidate_summary"]["blocker_count"],
        "ready_for_operator_review": True,
        "improved_evidence_planning_approved": False,
        "improved_evidence_planning_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_improved_evidence_planning_candidate_using_redesigned_evidence_markdown_v1(
    candidate: dict,
) -> str:
    """Render the candidate without implying approval or execution authority."""
    validation = (
        validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(
            candidate
        )
    )
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Improved Evidence Planning Candidate Status",
        "",
        "## Title",
        "- Optional Improved Evidence Planning Candidate Using Redesigned Evidence v1.",
        "",
        "## Optional Improved Evidence Planning Candidate Using Redesigned Evidence",
        f"- Artifact/status/digest: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}` / `{validation['improved_evidence_planning_candidate_using_redesigned_evidence_digest']}`.",
        "",
        "## Source Redesign Results Review",
        f"- `{candidate['source_results_review_artifact_kind']}` / `{candidate['source_results_review_status']}` / `{candidate['source_results_review_digest']}`.",
        "",
        "## Bound Evidence",
        f"- Redesign execution/output binding/approval: `{candidate['label_objective_redesign_execution_using_redesigned_evidence_digest']}` / `{candidate['label_objective_redesign_output_binding_digest']}` / `{candidate['label_objective_redesign_approval_using_redesigned_evidence_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- `{candidate['dataset_name']}` has `{candidate['total_canonical_record_count']}` frozen rows for 12 ordered tickers; META remains `{candidate['meta_record_count']}`.",
        "",
        "## Candidate Basis",
        f"- Selected direction: `{candidate['selected_direction']}`; the source review is research-only and operator selection remains required.",
        "",
        "## Candidate Objective",
        f"- `{candidate['improved_evidence_planning_candidate_objective']}` / `{candidate['improved_evidence_planning_candidate_scope']}` / `{candidate['improved_evidence_planning_candidate_mode']}`.",
        "",
        "## Improved Evidence Themes",
    ]
    lines.extend(
        f"- `{row['theme_id']}`: `{row['theme_status']}`."
        for row in candidate["improved_evidence_themes"]
    )
    lines.extend(["", "## Planned Evidence Components"])
    lines.extend(
        f"- `{row['component_id']}`: `{row['component_status']}`."
        for row in candidate["planned_evidence_components"]
    )
    lines.extend(["", "## Planned Data Products"])
    lines.extend(
        f"- `{row['data_product_id']}`: `{row['output_status']}`."
        for row in candidate["planned_data_products"]
    )
    lines.extend(["", "## Planned Future Outputs"])
    lines.extend(
        f"- `{row['future_output_id']}`: `{row['output_status']}`."
        for row in candidate["planned_future_outputs"]
    )
    lines.extend(
        [
            "",
            "## Per-Ticker Planning Entries",
            "- Twelve digest-bound entries preserve registry order; META remains 913 records and every other ticker remains 1003.",
            "",
            "## Next Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}" for index, item in enumerate(candidate["next_chain"], 1)
    )
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in candidate["next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            "- Predictive usefulness remains `not accepted`; no acceptance-readiness or acceptance candidate is created.",
            "",
            "## Profitability Boundary",
            "- Profitability remains `not accepted`.",
            "",
            "## Runtime Boundary",
            "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- This artifact is a research-only planning candidate. It approves and executes nothing, regenerates no labels or features, creates no targets or feature-label matrix, recomputes no metrics, trains no model, and produces no trading action.",
            "",
        ]
    )
    return "\n".join(lines)


def write_improved_evidence_planning_candidate_using_redesigned_evidence_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write one canonical candidate JSON file without overwriting."""
    candidate = build_improved_evidence_planning_candidate_using_redesigned_evidence_v1()
    output_name = (
        filename
        or "improved_evidence_planning_candidate_using_redesigned_evidence_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
            "candidate filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceError(
            "candidate output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "candidate_status": candidate["candidate_status"],
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest": candidate[
            "improved_evidence_planning_candidate_using_redesigned_evidence_digest"
        ],
    }
