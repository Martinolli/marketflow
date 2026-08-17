"""Planning-only feature and predictive-evidence candidate for redesigned labels."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import redesigned_label_generation_results_review_service as review


ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_V1 = (
    "feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1"
)
FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW"
)
FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_VALID = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_VALID"
)

DEFAULT_BRANCH = (
    "feature/feature-predictive-evidence-planning-candidate-redesigned-labels-v1"
)
DEFAULT_BASE_COMMIT = "bf7d6c5df08adfa4be9ab5dbdf1b613a43c3adad"
EXPECTED_RESULTS_REVIEW_DIGEST = (
    "f596d19db635735137c5d7073675a52b51444fa90d6a3acf09cc2aa0bc4ddd42"
)
EXPECTED_EXECUTION_DIGEST = review.EXPECTED_EXECUTION_DIGEST
EXPECTED_APPROVAL_DIGEST = review.SOURCE_EVIDENCE[
    "redesigned_label_generation_approval_digest"
]
EXPECTED_CANDIDATE_REVIEW_DIGEST = review.SOURCE_EVIDENCE[
    "redesigned_label_generation_candidate_review_package_digest"
]
EXPECTED_CANDIDATE_DIGEST = review.SOURCE_EVIDENCE[
    "redesigned_label_generation_candidate_digest"
]
EXPECTED_LABEL_OBJECTIVE_RESULTS_REVIEW_DIGEST = review.SOURCE_EVIDENCE[
    "label_objective_redesign_results_review_package_digest"
]
EXPECTED_LABEL_OBJECTIVE_EXECUTION_DIGEST = review.SOURCE_EVIDENCE[
    "label_objective_redesign_execution_digest"
]
EXPECTED_METHOD_SELECTION_DIGEST = review.SOURCE_EVIDENCE[
    "operator_method_path_selection_digest"
]
EXPECTED_RESEARCH_REGISTRY_DIGEST = review.SOURCE_EVIDENCE[
    "research_registry_approval_digest"
]
EXPECTED_RECORDS_DIGEST = review.SOURCE_EVIDENCE["records_digest"]
EXPECTED_LABEL_VALUES_DIGEST = review.EXPECTED_LABEL_VALUES_DIGEST
TARGET_UNIVERSE = list(review.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = review.NOT_ACCEPTED
NOT_AUTHORIZED = review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PLANNED_NOT_EVALUATED = "PLANNED_NOT_EVALUATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
SOURCE_REVIEWED_NOT_REGENERATED = "SOURCE_REVIEWED_NOT_REGENERATED"

PLAN_OBJECTIVE = "PLAN_FEATURE_AND_PREDICTIVE_EVIDENCE_CHAIN_USING_REDESIGNED_LABELS"
PLAN_SCOPE = "CANDIDATE_ONLY_NOT_FEATURE_GENERATION_NOT_PREDICTIVE_EXECUTION"
PLAN_MODE = PLANNED_NOT_EXECUTED
PLAN_AUTHORITY_STATUS = NOT_AUTHORIZED

SOURCE_INPUT_IDS = [
    "expanded_universe_canonical_dataset_v1",
    "redesigned_label_generation_results_review_package",
    "redesigned_label_values",
    "redesigned_label_family_coverage_report",
    "redesigned_threshold_generation_report",
    "redesigned_horizon_generation_report",
    "redesigned_label_availability_report",
    "per_ticker_redesigned_label_summary",
    "meta_limitation_preservation_report",
]
PLANNED_FEATURE_FAMILY_IDS = [
    "FEATURE_FAMILY_OHLCV_RETURNS_AND_RANGES",
    "FEATURE_FAMILY_VOLUME_PRICE_ANALYSIS",
    "FEATURE_FAMILY_VOLATILITY_AND_REALIZED_RANGE",
    "FEATURE_FAMILY_MOMENTUM_AND_TREND",
    "FEATURE_FAMILY_RELATIVE_STRENGTH_AND_CROSS_SECTIONAL_CONTEXT",
    "FEATURE_FAMILY_CALENDAR_AND_SESSION_CONTEXT",
    "FEATURE_FAMILY_LABEL_ALIGNED_HORIZON_CONTEXT",
    "FEATURE_FAMILY_QUALITY_MISSINGNESS_AND_META_LIMITATION_FLAGS",
    "FEATURE_FAMILY_REGIME_AND_INTERACTION_TERMS",
    "FEATURE_FAMILY_BASELINE_ERROR_CONTEXT",
]
PLANNED_PREDICTIVE_COMPONENT_IDS = [
    "chronological_split_using_redesigned_labels",
    "walk_forward_evaluation_using_redesigned_labels",
    "oos_evaluation_using_redesigned_labels",
    "baseline_comparison_using_redesigned_labels",
    "calibration_and_stability_review_using_redesigned_labels",
    "leakage_review_using_redesigned_labels",
    "feature_label_alignment_review",
    "per_ticker_vs_cross_sectional_review",
    "class_balance_and_availability_review",
    "operator_results_review",
]
PLANNED_MODEL_BASELINE_FAMILY_IDS = [
    "BASELINE_MAJORITY_CLASS",
    "BASELINE_PREVIOUS_DIRECTION",
    "BASELINE_BUY_HOLD_REFERENCE_ONLY",
    "BASELINE_TICKER_CROSS_SECTIONAL",
    "MODEL_FAMILY_REGULARIZED_LINEAR",
    "MODEL_FAMILY_TREE_BASELINE_OPTIONAL",
    "MODEL_FAMILY_ENSEMBLE_OPTIONAL",
    "MODEL_FAMILY_PER_TICKER_COMPARISON",
    "MODEL_FAMILY_GLOBAL_CROSS_SECTIONAL_COMPARISON",
]
PLANNED_OUTPUT_IDS = [
    "feature_predictive_evidence_planning_manifest",
    "redesigned_label_input_binding_manifest",
    "planned_feature_family_matrix",
    "planned_feature_schema_contract",
    "planned_feature_label_alignment_report_template",
    "planned_walk_forward_protocol_template",
    "planned_oos_protocol_template",
    "planned_baseline_model_comparison_template",
    "planned_leakage_quality_control_template",
    "planned_operator_review_summary_template",
]
FUTURE_CHAIN = [
    "Feature / Predictive Evidence Planning Candidate Operator Review Package v1.",
    "Feature / Predictive Evidence Planning Approval v1, if selected.",
    "Feature Generation Candidate Using Redesigned Labels v1, if selected.",
    "Feature Generation Approval and Execution, if separately approved.",
    "Additional Predictive Evidence Execution Candidate Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Approval and Execution, if separately approved.",
    "Additional Predictive Evidence Results Review.",
    "Predictive Usefulness Reassessment and Acceptance Readiness Review.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
FUTURE_GATES = [
    "feature_predictive_evidence_planning_candidate_operator_review",
    "feature_predictive_evidence_planning_approval_if_selected",
    "feature_generation_candidate_using_redesigned_labels_if_selected",
    "feature_generation_approval_if_required",
    "feature_generation_execution_if_approved",
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution_if_approved",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_generate_features",
    "candidate_does_not_execute_predictive_evidence",
    "candidate_does_not_train_models",
    "candidate_does_not_recompute_metrics",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "preserve_meta_record_limitation",
    "no_predictive_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]


class FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(ValueError):
    """Raised when the planning candidate violates its frozen contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
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


def _source_inputs() -> list[dict[str, Any]]:
    return [
        {
            "source_input_id": source_input_id,
            "source_input_status": SOURCE_REVIEWED_NOT_REGENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "research_only": True,
            "non_actionable": True,
        }
        for source_input_id in SOURCE_INPUT_IDS
    ]


def _feature_families() -> list[dict[str, Any]]:
    return [
        {
            "feature_family_id": family_id,
            "feature_generation_status": PLANNED_NOT_GENERATED,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in PLANNED_FEATURE_FAMILY_IDS
    ]


def _predictive_components() -> list[dict[str, Any]]:
    return [
        {
            "component_id": component_id,
            "component_status": PLANNED_NOT_EXECUTED,
            "execution_authorized": False,
            "execution_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for component_id in PLANNED_PREDICTIVE_COMPONENT_IDS
    ]


def _model_baseline_families() -> list[dict[str, Any]]:
    return [
        {
            "model_or_baseline_family_id": family_id,
            "model_or_baseline_status": PLANNED_NOT_EVALUATED,
            "training_authorized": False,
            "training_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in PLANNED_MODEL_BASELINE_FAMILY_IDS
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "planned_output_id": output_id,
            "output_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_feature_predictive_evidence_planning_candidate_digest", None
    )
    return payload


def per_ticker_feature_predictive_evidence_planning_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one ticker planning entry."""
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
            "redesigned_label_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "feature_predictive_evidence_planning_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "predictive_evidence_execution_authorized": False,
            "predictive_evidence_execution_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_redesigned_label_generation_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
            "planning_note": (
                "PRESERVE_META_LIMITATION_IN_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING"
                if is_meta
                else "STANDARD_FROZEN_RECORD_COUNT_PRESERVED"
            ),
        }
        entry[
            "per_ticker_feature_predictive_evidence_planning_candidate_digest"
        ] = per_ticker_feature_predictive_evidence_planning_candidate_digest_v1(entry)
        entries.append(entry)
    return entries


CHECK_FIELD_SPECS = [
    ("redesigned_label_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, "redesigned_label_generation_results_review_package_digest"),
    ("redesigned_label_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "redesigned_label_generation_execution_digest"),
    ("redesigned_label_approval_digest_bound", EXPECTED_APPROVAL_DIGEST, "redesigned_label_generation_approval_digest"),
    ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, "label_values_digest"),
    ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, "research_registry_approval_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("redesigned_label_results_review_ready_true", True, "redesigned_label_generation_results_review_ready"),
    ("ready_for_feature_or_predictive_evidence_planning_candidate_true", True, "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels"),
    ("feature_predictive_evidence_planning_candidate_created_true", True, "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created"),
    ("feature_predictive_evidence_planning_candidate_ready_true", True, "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review"),
    ("redesigned_label_value_row_count_143352", 143352, "label_value_row_count"),
    ("available_label_count_142200", 142200, "available_label_value_count"),
    ("unavailable_label_count_1152", 1152, "unavailable_label_value_count"),
    ("label_family_count_10", 10, "label_family_count"),
    ("threshold_strategy_count_7", 7, "threshold_strategy_count"),
    ("horizon_strategy_count_5", 5, "horizon_strategy_count"),
    ("source_inputs_defined", SOURCE_INPUT_IDS, "source_input_ids"),
    ("planned_feature_families_defined", PLANNED_FEATURE_FAMILY_IDS, "planned_feature_family_ids"),
    ("planned_predictive_components_defined", PLANNED_PREDICTIVE_COMPONENT_IDS, "planned_predictive_component_ids"),
    ("planned_model_baseline_families_defined", PLANNED_MODEL_BASELINE_FAMILY_IDS, "planned_model_baseline_family_ids"),
    ("planned_outputs_not_generated", True, "planned_outputs_not_generated"),
    ("planned_outputs_research_only", True, "planned_outputs_research_only"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_digests_present", True, "per_ticker_digests_valid"),
    ("future_chain_defined", FUTURE_CHAIN, "future_chain"),
    ("future_gates_defined", FUTURE_GATES, "future_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("feature_generation_false", False, "feature_generation_performed"),
    ("metric_recomputation_false", False, "metric_recomputation_performed"),
    ("model_training_false", False, "model_training_performed"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("provider_requests_made_false", False, "provider_requests_made"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed"),
    ("dataset_regeneration_false", False, "dataset_regeneration_performed"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [spec[0] for spec in CHECK_FIELD_SPECS]


def _derived_check_fields(candidate: dict[str, Any]) -> dict[str, Any]:
    source_inputs = candidate.get("source_inputs", [])
    feature_families = candidate.get("planned_feature_families", [])
    predictive_components = candidate.get("planned_predictive_evidence_components", [])
    model_families = candidate.get("planned_model_baseline_families", [])
    planned_outputs = candidate.get("planned_outputs", [])
    entries = candidate.get("per_ticker_candidate_entries", [])
    return {
        **candidate,
        "source_input_ids": [row.get("source_input_id") for row in source_inputs] if isinstance(source_inputs, list) else [],
        "planned_feature_family_ids": [row.get("feature_family_id") for row in feature_families] if isinstance(feature_families, list) else [],
        "planned_predictive_component_ids": [row.get("component_id") for row in predictive_components] if isinstance(predictive_components, list) else [],
        "planned_model_baseline_family_ids": [row.get("model_or_baseline_family_id") for row in model_families] if isinstance(model_families, list) else [],
        "planned_outputs_not_generated": isinstance(planned_outputs, list) and len(planned_outputs) == len(PLANNED_OUTPUT_IDS) and all(row.get("output_status") == PLANNED_NOT_GENERATED and row.get("generated") is False for row in planned_outputs),
        "planned_outputs_research_only": isinstance(planned_outputs, list) and len(planned_outputs) == len(PLANNED_OUTPUT_IDS) and all(row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE and row.get("research_only") is True and row.get("non_actionable") is True for row in planned_outputs),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(isinstance(row.get("per_ticker_feature_predictive_evidence_planning_candidate_digest"), str) and len(row["per_ticker_feature_predictive_evidence_planning_candidate_digest"]) == 64 and row["per_ticker_feature_predictive_evidence_planning_candidate_digest"] == per_ticker_feature_predictive_evidence_planning_candidate_digest_v1(row) for row in entries),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_check_fields(candidate)
    return [_check(check_id, expected, fields.get(field)) for check_id, expected, field in CHECK_FIELD_SPECS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "feature_predictive_evidence_planning_candidate_ready": not failed,
        "ready_for_operator_review": not failed,
        "feature_generation_candidate_created": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_V1,
        "candidate_status": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_regeneration_performed": False,
        "canonical_dataset_regenerated": False,
        "redesigned_label_regeneration_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "redesigned_label_generation_candidate_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "redesigned_label_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "label_objective_redesign_results_review_package_digest": EXPECTED_LABEL_OBJECTIVE_RESULTS_REVIEW_DIGEST,
        "label_objective_redesign_execution_digest": EXPECTED_LABEL_OBJECTIVE_EXECUTION_DIGEST,
        "operator_method_path_selection_digest": EXPECTED_METHOD_SELECTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "redesigned_label_generation_performed": True,
        "actual_redesigned_labels_generated": True,
        "redesigned_label_generation_results_created": True,
        "redesigned_label_generation_results_review_created": True,
        "redesigned_label_generation_results_review_ready": True,
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels": True,
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created": True,
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review": True,
        "feature_generation_candidate_created": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "no_tracked_marketflow_files": True,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "redesigned_label_output_root": ".marketflow/redesigned_label_generation/expanded_universe_v1/",
        "redesigned_label_output_count": 11,
        "redesigned_label_output_status": "REVIEWED_AND_VERIFIED",
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "label_value_row_count": 143352,
        "label_family_coverage_entries": 144,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "label_generation_interpretation": "GENERATED_RESEARCH_ONLY",
        "feature_generation_interpretation": "NOT_GENERATED_NOT_AUTHORIZED",
        "predictive_usefulness_interpretation": "NOT_ACCEPTANCE_EVIDENCE",
        "feature_predictive_evidence_planning_candidate_objective": PLAN_OBJECTIVE,
        "feature_predictive_evidence_planning_candidate_scope": PLAN_SCOPE,
        "feature_predictive_evidence_planning_candidate_mode": PLAN_MODE,
        "feature_predictive_evidence_planning_candidate_authority_status": PLAN_AUTHORITY_STATUS,
        "source_inputs": _source_inputs(),
        "planned_feature_families": _feature_families(),
        "planned_predictive_evidence_components": _predictive_components(),
        "planned_model_baseline_families": _model_baseline_families(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop(
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest",
        None,
    )
    return payload


def feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the planning candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1() -> dict[str, Any]:
    """Build the planning candidate without reading outputs or invoking providers."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate[
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"
    ] = feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest_v1(
        candidate
    )
    validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(
        candidate
    )
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    forbidden_artifacts = {
        "FEATURE_GENERATION_CANDIDATE",
        "FEATURE_GENERATION_APPROVED",
        "FEATURE_GENERATION_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "feature_generation_candidate_created",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is exactly the planning-only candidate."""
    if not isinstance(candidate, dict):
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
            "candidate must be a JSON object"
        )
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_V1, "schema_version")
    _expect(candidate.get("candidate_status"), FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    _reject_forbidden_values(candidate)
    expected = {
        "redesigned_label_generation_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "redesigned_label_generation_candidate_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "redesigned_label_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "label_objective_redesign_results_review_package_digest": EXPECTED_LABEL_OBJECTIVE_RESULTS_REVIEW_DIGEST,
        "label_objective_redesign_execution_digest": EXPECTED_LABEL_OBJECTIVE_EXECUTION_DIGEST,
        "operator_method_path_selection_digest": EXPECTED_METHOD_SELECTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "redesigned_label_output_count": 11,
        "redesigned_label_output_status": "REVIEWED_AND_VERIFIED",
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "label_value_row_count": 143352,
        "label_family_coverage_entries": 144,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "feature_predictive_evidence_planning_candidate_objective": PLAN_OBJECTIVE,
        "feature_predictive_evidence_planning_candidate_scope": PLAN_SCOPE,
        "feature_predictive_evidence_planning_candidate_mode": PLAN_MODE,
        "feature_predictive_evidence_planning_candidate_authority_status": PLAN_AUTHORITY_STATUS,
        "source_inputs": _source_inputs(),
        "planned_feature_families": _feature_families(),
        "planned_predictive_evidence_components": _predictive_components(),
        "planned_model_baseline_families": _model_baseline_families(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "future_chain": FUTURE_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(candidate.get(field), expected_value, field)
    true_fields = [
        "created_offline",
        "research_only",
        "operator_review_required",
        "redesigned_label_generation_approved",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_label_generation_results_created",
        "redesigned_label_generation_results_review_created",
        "redesigned_label_generation_results_review_ready",
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels",
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created",
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    ]
    false_fields = [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "canonical_dataset_regenerated",
        "redesigned_label_regeneration_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "feature_generation_candidate_created",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
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
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
            "candidate_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "candidate_checklist check ids")
    if any(row.get("status") != PASS for row in checklist):
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
            "candidate_checklist must pass"
        )
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get(
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
            "missing candidate digest"
        )
    _expect(digest, feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest_v1(candidate), "candidate digest")
    return {
        "status": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": digest,
        "per_ticker_candidate_entry_count": len(candidate["per_ticker_candidate_entries"]),
        "blocker_count": candidate["candidate_summary"]["blocker_count"],
        "ready_for_operator_review": True,
        "feature_generation_candidate_created": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render the planning candidate without implying execution authority."""
    validation = validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Feature Predictive Evidence Planning Candidate Status", "",
        "## Title", "- Feature / Predictive Evidence Planning Candidate Using Redesigned Labels v1.", "",
        "## Feature / Predictive Evidence Planning Candidate Using Redesigned Labels", f"- Artifact/status/digest: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}` / `{validation['feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest']}`.", "",
        "## Bound Evidence", f"- Results review/execution/approval: `{candidate['redesigned_label_generation_results_review_package_digest']}` / `{candidate['redesigned_label_generation_execution_digest']}` / `{candidate['redesigned_label_generation_approval_digest']}`.", "",
        "## Dataset and Universe", f"- `{candidate['dataset_name']}` contains `{candidate['total_canonical_record_count']}` frozen records for 12 ordered tickers; META remains `{candidate['meta_record_count']}`.", "",
        "## Source Redesigned Label Profile", f"- Reviewed outputs/families/thresholds/horizons/label rows: `{candidate['redesigned_label_output_count']}` / `{candidate['label_family_count']}` / `{candidate['threshold_strategy_count']}` / `{candidate['horizon_strategy_count']}` / `{candidate['label_value_row_count']}`.", "",
        "## Source Inputs",
    ]
    lines.extend(f"- `{row['source_input_id']}`: `{row['source_input_status']}`." for row in candidate["source_inputs"])
    lines.extend(["", "## Planned Feature Families"])
    lines.extend(f"- `{row['feature_family_id']}`: `{row['feature_generation_status']}`." for row in candidate["planned_feature_families"])
    lines.extend(["", "## Planned Predictive Evidence Components"])
    lines.extend(f"- `{row['component_id']}`: `{row['component_status']}`." for row in candidate["planned_predictive_evidence_components"])
    lines.extend(["", "## Planned Model and Baseline Families"])
    lines.extend(f"- `{row['model_or_baseline_family_id']}`: `{row['model_or_baseline_status']}`." for row in candidate["planned_model_baseline_families"])
    lines.extend(["", "## Planned Outputs"])
    lines.extend(f"- `{row['planned_output_id']}`: `{row['output_status']}`." for row in candidate["planned_outputs"])
    lines.extend(["", "## Per-Ticker Candidate Entries", f"- Twelve deterministic entries preserve the exact registry order; META remains 913 records and every other ticker remains 1003. All feature and predictive-execution flags are false.", "", "## Future Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(candidate["future_chain"], 1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend([
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- This candidate uses committed reviewed facts only. It reads no provider, market-data, canonical-dataset, or redesigned-label output and generates no feature, metric, model, predictive evidence, recommendation, acceptance, profitability, runtime, or trading artifact.", "- Operator review is required before any separately governed approval or execution candidate.", "",
    ])
    return "\n".join(lines)


def write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical candidate without overwriting an existing file."""
    candidate = build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1()
    output_name = filename or "feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
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
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError(
            "candidate output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "candidate_status": candidate["candidate_status"],
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": candidate["feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"],
    }
