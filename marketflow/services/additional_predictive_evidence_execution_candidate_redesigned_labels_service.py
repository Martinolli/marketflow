"""Offline candidate for future predictive evidence using redesigned labels."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import feature_generation_results_review_redesigned_labels_service as review_service


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_V1 = (
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_VALID"
)

DEFAULT_BRANCH = "feature/additional-predictive-evidence-execution-candidate-redesigned-labels-v1"
DEFAULT_BASE_COMMIT = "099872ee85ea97e617faedecddd0bef16a8ce4c8"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
SOURCE_REVIEWED_NOT_REGENERATED = "SOURCE_REVIEWED_NOT_REGENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PLANNED_NOT_EVALUATED = "PLANNED_NOT_EVALUATED"
PLANNED_NOT_COMPUTED = "PLANNED_NOT_COMPUTED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_RESULTS_REVIEW_DIGEST = "e46bbd76b895a9513d338b415cef364baf778fe5ade67128a069631ae2bbbda3"
EXPECTED_EXECUTION_DIGEST = review_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = review_service.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_APPROVAL_DIGEST = review_service.SOURCE_EVIDENCE["feature_generation_approval_using_redesigned_labels_digest"]
EXPECTED_CANDIDATE_REVIEW_DIGEST = review_service.SOURCE_EVIDENCE["feature_generation_candidate_using_redesigned_labels_review_package_digest"]
EXPECTED_CANDIDATE_DIGEST = review_service.SOURCE_EVIDENCE["feature_generation_candidate_using_redesigned_labels_digest"]
EXPECTED_PLANNING_APPROVAL_DIGEST = review_service.SOURCE_EVIDENCE["feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"]
EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST = review_service.SOURCE_EVIDENCE["redesigned_label_generation_results_review_package_digest"]
EXPECTED_REDESIGNED_LABEL_EXECUTION_DIGEST = review_service.SOURCE_EVIDENCE["redesigned_label_generation_execution_digest"]
EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST = review_service.SOURCE_EVIDENCE["redesigned_label_generation_approval_digest"]
EXPECTED_RESEARCH_REGISTRY_DIGEST = review_service.SOURCE_EVIDENCE["research_registry_approval_digest"]
EXPECTED_RECORDS_DIGEST = review_service.SOURCE_EVIDENCE["records_digest"]
EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST = review_service.SOURCE_EVIDENCE["label_values_digest"]
TARGET_UNIVERSE = list(review_service.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review_service.EXPECTED_RECORD_COUNTS)

EXECUTION_CANDIDATE_OBJECTIVE = (
    "PREPARE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS_AND_FEATURES"
)
EXECUTION_CANDIDATE_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
EXECUTION_CANDIDATE_MODE = PLANNED_NOT_EXECUTED
EXECUTION_CANDIDATE_AUTHORITY_STATUS = NOT_AUTHORIZED

SOURCE_INPUT_IDS = [
    "expanded_universe_canonical_dataset_v1",
    "redesigned_label_generation_results_review_package",
    "redesigned_label_values",
    "feature_generation_results_review_package_using_redesigned_labels",
    "feature_values",
    "feature_family_coverage_report",
    "feature_group_generation_report",
    "feature_schema_contract_report",
    "feature_label_alignment_report",
    "feature_quality_report",
    "per_ticker_feature_summary",
    "meta_limitation_feature_handling_report",
]

PLANNED_EXECUTION_ACTIVITY_IDS = [
    "bind_feature_values_and_redesigned_labels",
    "build_feature_label_matrix_candidate",
    "verify_feature_label_alignment",
    "define_chronological_train_validation_oos_splits",
    "define_walk_forward_evaluation_protocol",
    "define_oos_holdout_protocol",
    "define_baseline_comparison_protocol",
    "define_model_family_comparison_protocol",
    "define_metric_family_computation_plan",
    "define_calibration_and_stability_review_plan",
    "define_leakage_and_quality_review_plan",
    "define_per_ticker_and_cross_sectional_review_plan",
    "prepare_operator_review_summary",
]

PLANNED_SPLITS = {
    "training_window": "2022-01-01 through 2023-12-31",
    "validation_window": "2024-01-01 through 2024-12-31",
    "oos_window": "2025-01-01 through 2025-12-31",
    "shuffle_allowed": False,
    "chronological_order_required": True,
    "embargo_policy": "PLANNED_FOR_OPERATOR_REVIEW",
}

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

PLANNED_METRIC_FAMILY_IDS = [
    "accuracy",
    "macro_precision",
    "macro_recall",
    "macro_f1",
    "confusion_matrix",
    "brier_score",
    "calibration_summary",
    "class_balance",
    "walk_forward_stability",
    "baseline_outperformance_delta",
]

PLANNED_OUTPUT_IDS = [
    "additional_predictive_evidence_execution_candidate_manifest",
    "source_feature_label_binding_manifest",
    "planned_feature_label_matrix_profile",
    "planned_chronological_split_profile",
    "planned_walk_forward_protocol",
    "planned_oos_holdout_protocol",
    "planned_baseline_model_comparison_plan",
    "planned_metric_family_plan",
    "planned_calibration_stability_plan",
    "planned_leakage_quality_control_plan",
    "planned_per_ticker_cross_sectional_review_plan",
    "planned_operator_review_summary_template",
]

FUTURE_CHAIN = [
    "Additional Predictive Evidence Execution Candidate Operator Review Package Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Approval Using Redesigned Labels v1, if selected.",
    "Additional Predictive Evidence Execution Using Redesigned Labels v1.",
    "Additional Predictive Evidence Results Review Using Redesigned Labels v1.",
    "Predictive Usefulness Reassessment Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "additional_predictive_evidence_execution_candidate_operator_review_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_using_redesigned_labels_if_selected",
    "additional_predictive_evidence_execution_using_redesigned_labels",
    "additional_predictive_evidence_results_review_using_redesigned_labels",
    "predictive_usefulness_reassessment_using_redesigned_evidence",
    "predictive_usefulness_acceptance_readiness_using_redesigned_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
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
    "do_not_mutate_feature_outputs",
    "preserve_meta_record_limitation",
    "no_predictive_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "feature_generation_results_review_digest_bound",
    "feature_generation_execution_digest_bound",
    "feature_values_digest_bound",
    "feature_generation_approval_digest_bound",
    "redesigned_label_results_review_digest_bound",
    "redesigned_label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "label_values_digest_preserved",
    "feature_values_digest_preserved",
    "meta_913_preserved",
    "feature_generation_results_review_ready_true",
    "ready_for_predictive_evidence_candidate_true",
    "additional_predictive_evidence_execution_candidate_created_true",
    "additional_predictive_evidence_execution_candidate_ready_true",
    "additional_predictive_evidence_execution_candidate_review_created_false",
    "predictive_evidence_execution_authorized_false",
    "predictive_evidence_executed_false",
    "feature_label_matrix_planned_not_generated",
    "planned_execution_activities_defined",
    "planned_splits_defined",
    "planned_model_baseline_families_9",
    "planned_metric_families_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "metric_recomputation_false",
    "model_training_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "redesigned_label_regeneration_false",
    "feature_regeneration_false",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "future_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]

FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
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


class AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(ValueError):
    """Raised when the candidate violates its planning-only contract."""


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
            "source_input": source_input,
            "source_status": SOURCE_REVIEWED_NOT_REGENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for source_input in SOURCE_INPUT_IDS
    ]


def _planned_activities() -> list[dict[str, Any]]:
    return [
        {
            "activity_id": activity_id,
            "activity_status": PLANNED_NOT_EXECUTED,
            "execution_authorized": False,
            "execution_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for activity_id in PLANNED_EXECUTION_ACTIVITY_IDS
    ]


def _planned_matrix() -> dict[str, Any]:
    return {
        "matrix_status": PLANNED_NOT_GENERATED,
        "feature_values_digest_bound": True,
        "redesigned_label_values_digest_bound": True,
        "records_digest_bound": True,
        "feature_row_count": 203082,
        "label_row_count": 143352,
        "target_universe_count": 12,
        "feature_label_join_strategy": "TICKER_DATE_HORIZON_AND_LABEL_FAMILY_ALIGNMENT_PLANNED",
        "join_execution_performed": False,
        "matrix_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _planned_model_baseline_families() -> list[dict[str, Any]]:
    return [
        {
            "model_or_baseline_family": family,
            "model_or_baseline_status": PLANNED_NOT_EVALUATED,
            "training_authorized": False,
            "training_performed": False,
            "metric_computation_authorized": False,
            "metric_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family in PLANNED_MODEL_BASELINE_FAMILY_IDS
    ]


def _planned_metric_families() -> list[dict[str, Any]]:
    return [
        {
            "metric_family": metric,
            "metric_status": PLANNED_NOT_COMPUTED,
            "metric_computation_authorized": False,
            "metric_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for metric in PLANNED_METRIC_FAMILY_IDS
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "output_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one ticker candidate entry."""
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_additional_predictive_evidence_execution_candidate_digest", None
    )
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "redesigned_label_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "feature_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "additional_predictive_evidence_execution_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "feature_values_created": True,
            "predictive_evidence_execution_authorized": False,
            "predictive_evidence_execution_performed": False,
            "metric_recomputation_performed": False,
            "model_training_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_feature_generation_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
            "source_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
            "source_redesigned_label_values_digest": EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST,
        }
        if ticker == "META":
            entry["planning_note"] = "PRESERVE_META_LIMITATION_IN_PREDICTIVE_EVIDENCE_CANDIDATE"
        entry["per_ticker_additional_predictive_evidence_execution_candidate_digest"] = (
            per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_V1,
        "candidate_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_generation_performed": False,
        "canonical_dataset_regenerated": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_generation_approved": True,
        "feature_generation_authorized": True,
        "redesigned_feature_generation_authorized": True,
        "feature_generation_performed": True,
        "redesigned_feature_generation_performed": True,
        "feature_values_created": True,
        "feature_generation_results_created": True,
        "feature_generation_results_review_created": True,
        "feature_generation_results_review_ready": True,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_created": True,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created": False,
        "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_evidence_results_created": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
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
        "feature_generation_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "feature_generation_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": EXPECTED_PLANNING_APPROVAL_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_REDESIGNED_LABEL_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST,
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
        "label_value_row_count": 143352,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "feature_output_count": 12,
        "feature_output_status": "REVIEWED_AND_VERIFIED",
        "feature_family_count": 10,
        "feature_group_count": 17,
        "feature_schema_field_count": 16,
        "feature_value_row_count": 203082,
        "available_feature_value_count": 190848,
        "unavailable_feature_value_count": 12234,
        "additional_predictive_evidence_execution_candidate_objective": EXECUTION_CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_scope": EXECUTION_CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_candidate_mode": EXECUTION_CANDIDATE_MODE,
        "additional_predictive_evidence_execution_candidate_authority_status": EXECUTION_CANDIDATE_AUTHORITY_STATUS,
        "source_inputs": _source_inputs(),
        "planned_feature_label_matrix": _planned_matrix(),
        "planned_execution_activities": _planned_activities(),
        "planned_splits": deepcopy(PLANNED_SPLITS),
        "planned_model_baseline_families": _planned_model_baseline_families(),
        "planned_metric_families": _planned_metric_families(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_candidate_entries", [])
    outputs = candidate.get("planned_outputs", [])
    values: dict[str, tuple[Any, Any]] = {
        "feature_generation_results_review_digest_bound": (EXPECTED_RESULTS_REVIEW_DIGEST, candidate.get("feature_generation_results_review_using_redesigned_labels_digest")),
        "feature_generation_execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, candidate.get("feature_generation_execution_using_redesigned_labels_digest")),
        "feature_values_digest_bound": (EXPECTED_FEATURE_VALUES_DIGEST, candidate.get("feature_values_digest")),
        "feature_generation_approval_digest_bound": (EXPECTED_APPROVAL_DIGEST, candidate.get("feature_generation_approval_using_redesigned_labels_digest")),
        "redesigned_label_results_review_digest_bound": (EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST, candidate.get("redesigned_label_generation_results_review_package_digest")),
        "redesigned_label_values_digest_bound": (EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST, candidate.get("redesigned_label_values_digest")),
        "research_registry_digest_bound": (EXPECTED_RESEARCH_REGISTRY_DIGEST, candidate.get("research_registry_approval_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, candidate.get("records_digest")),
        "target_universe_12_preserved": (TARGET_UNIVERSE, candidate.get("target_universe")),
        "records_digest_preserved": (EXPECTED_RECORDS_DIGEST, candidate.get("records_digest")),
        "label_values_digest_preserved": (EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST, candidate.get("redesigned_label_values_digest")),
        "feature_values_digest_preserved": (EXPECTED_FEATURE_VALUES_DIGEST, candidate.get("feature_values_digest")),
        "meta_913_preserved": (913, candidate.get("meta_record_count")),
        "feature_generation_results_review_ready_true": (True, candidate.get("feature_generation_results_review_ready")),
        "ready_for_predictive_evidence_candidate_true": (True, candidate.get("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels")),
        "additional_predictive_evidence_execution_candidate_created_true": (True, candidate.get("additional_predictive_evidence_execution_candidate_created")),
        "additional_predictive_evidence_execution_candidate_ready_true": (True, candidate.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_ready_for_operator_review")),
        "additional_predictive_evidence_execution_candidate_review_created_false": (False, candidate.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created")),
        "predictive_evidence_execution_authorized_false": (False, candidate.get("additional_predictive_evidence_execution_authorized")),
        "predictive_evidence_executed_false": (False, candidate.get("additional_predictive_evidence_executed")),
        "feature_label_matrix_planned_not_generated": (PLANNED_NOT_GENERATED, candidate.get("planned_feature_label_matrix", {}).get("matrix_status")),
        "planned_execution_activities_defined": (_planned_activities(), candidate.get("planned_execution_activities")),
        "planned_splits_defined": (PLANNED_SPLITS, candidate.get("planned_splits")),
        "planned_model_baseline_families_9": (9, len(candidate.get("planned_model_baseline_families", []))),
        "planned_metric_families_defined": (_planned_metric_families(), candidate.get("planned_metric_families")),
        "planned_outputs_not_generated": (True, bool(outputs) and all(row.get("output_status") == PLANNED_NOT_GENERATED for row in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(row.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
        "per_ticker_entries_12": (12, len(entries)),
        "per_ticker_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_additional_predictive_evidence_execution_candidate_digest"), str) and len(row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]) == 64 for row in entries)),
        "metric_recomputation_false": (False, candidate.get("metric_recomputation_performed")),
        "model_training_false": (False, candidate.get("model_training_performed")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, candidate.get("strategy_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        "trade_recommendations_false": (False, candidate.get("trade_recommendations_generated")),
        "provider_requests_made_false": (False, candidate.get("provider_requests_made")),
        "market_data_acquisition_false": (False, candidate.get("market_data_acquisition_performed")),
        "dataset_regeneration_false": (False, candidate.get("canonical_dataset_regenerated")),
        "redesigned_label_regeneration_false": (False, candidate.get("redesigned_label_regeneration_performed")),
        "feature_regeneration_false": (False, candidate.get("feature_regeneration_performed")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, candidate.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, candidate.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, candidate.get("runtime_migration_approval_created")),
        "future_chain_defined": (FUTURE_CHAIN, candidate.get("future_chain")),
        "future_gates_defined": (FUTURE_GATES, candidate.get("future_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (True, candidate.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "additional_predictive_evidence_execution_candidate_ready": not failed,
        "ready_for_operator_review": not failed,
        "predictive_evidence_execution_authorized": False,
        "predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate."""
    payload = deepcopy(candidate)
    payload.pop(
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest",
        None,
    )
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1() -> dict[str, Any]:
    """Build a candidate without authorizing or performing predictive work."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate[
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"
    ] = additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(
        candidate
    )
    validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(
        candidate
    )
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            f"{field} mismatch"
        )


def validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is the exact non-authorizing candidate."""
    if not isinstance(candidate, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    expected_base = _base_candidate()
    for field, expected in expected_base.items():
        _expect(candidate.get(field), expected, field)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            "candidate_checklist missing"
        )
    expected_checklist = _checklist(candidate)
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "candidate checklist check IDs")
    if any(row["status"] != PASS for row in expected_checklist):
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            "candidate checklist contains a failed check"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), summary, "candidate_summary")
    entries = candidate.get("per_ticker_candidate_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            "per-ticker candidate entries missing"
        )
    for entry in entries:
        digest = entry.get(
            "per_ticker_additional_predictive_evidence_execution_candidate_digest"
        )
        if not isinstance(digest, str) or len(digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
                "per-ticker candidate digest missing"
            )
        _expect(
            digest,
            per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(entry),
            "per-ticker candidate digest",
        )
    digest = candidate.get(
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            "candidate digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": digest,
        "ready_for_operator_review": True,
        "blocker_count": 0,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized Markdown summary of the candidate."""
    validation = validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Candidate Using Redesigned Labels Status", "",
        "## Title", "- Additional Predictive Evidence Execution Candidate Using Redesigned Labels v1.", "",
        "## Additional Predictive Evidence Execution Candidate Using Redesigned Labels", f"- Artifact/status/digest: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}` / `{validation['additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest']}`.", "",
        "## Bound Evidence", f"- Feature review/execution/values: `{candidate['feature_generation_results_review_using_redesigned_labels_digest']}` / `{candidate['feature_generation_execution_using_redesigned_labels_digest']}` / `{candidate['feature_values_digest']}`.", "",
        "## Dataset and Universe", f"- `{candidate['dataset_name']}` contains `{candidate['total_canonical_record_count']}` records for `{' '.join(candidate['target_universe'])}`; META remains `{candidate['meta_record_count']}`.", "",
        "## Source Redesigned Label Profile", f"- Rows/available/unavailable/families/thresholds/horizons: `{candidate['label_value_row_count']}` / `{candidate['available_label_value_count']}` / `{candidate['unavailable_label_value_count']}` / `{candidate['label_family_count']}` / `{candidate['threshold_strategy_count']}` / `{candidate['horizon_strategy_count']}`.", "",
        "## Source Feature Profile", f"- Outputs/families/groups/schema/rows: `{candidate['feature_output_count']}` / `{candidate['feature_family_count']}` / `{candidate['feature_group_count']}` / `{candidate['feature_schema_field_count']}` / `{candidate['feature_value_row_count']}`.", "",
        "## Candidate Objective", f"- `{candidate['additional_predictive_evidence_execution_candidate_objective']}`; scope/mode/authority: `{candidate['additional_predictive_evidence_execution_candidate_scope']}` / `{candidate['additional_predictive_evidence_execution_candidate_mode']}` / `{candidate['additional_predictive_evidence_execution_candidate_authority_status']}`.", "",
        "## Source Inputs",
    ]
    lines.extend(f"- `{row['source_input']}`: `{row['source_status']}` / `{row['actionability_label']}`" for row in candidate["source_inputs"])
    lines.extend(["", "## Planned Feature / Label Matrix", f"- Status/join: `{candidate['planned_feature_label_matrix']['matrix_status']}` / `{candidate['planned_feature_label_matrix']['feature_label_join_strategy']}`; no matrix was generated.", "", "## Planned Execution Activities"])
    lines.extend(f"- `{row['activity_id']}`: `{row['activity_status']}`" for row in candidate["planned_execution_activities"])
    lines.extend(["", "## Planned Splits"])
    lines.extend(f"- {key}: `{value}`" for key, value in candidate["planned_splits"].items())
    lines.extend(["", "## Planned Model and Baseline Families"])
    lines.extend(f"- `{row['model_or_baseline_family']}`: `{row['model_or_baseline_status']}`" for row in candidate["planned_model_baseline_families"])
    lines.extend(["", "## Planned Metric Families"])
    lines.extend(f"- `{row['metric_family']}`: `{row['metric_status']}`" for row in candidate["planned_metric_families"])
    lines.extend(["", "## Planned Outputs"])
    lines.extend(f"- `{row['output_id']}`: `{row['output_status']}`" for row in candidate["planned_outputs"])
    lines.extend(["", "## Per-Ticker Candidate Entries"])
    lines.extend(f"- `{row['ticker']}`: `{row['historical_record_count']}` records; `{row['additional_predictive_evidence_execution_candidate_status']}`" for row in candidate["per_ticker_candidate_entries"])
    lines.extend(["", "## Future Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(candidate["future_chain"], 1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend([
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- Candidate only: no predictive execution, matrix generation, metric recomputation, model training, scoring, acceptance, profitability, runtime, recommendation, broker, or trading authority or action.", "- Source dataset, redesigned-label outputs, and feature outputs remain reviewed and unmodified; operator review and separate approval are required before execution.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write one canonical candidate package without overwriting an artifact."""
    candidate = build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1()
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1.json"
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError(
            "candidate output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": candidate["additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"],
    }
