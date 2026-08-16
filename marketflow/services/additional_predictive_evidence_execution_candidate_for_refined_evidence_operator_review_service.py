"""Offline operator review of the refined-evidence execution candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_for_refined_evidence_service as candidate_service,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_V1 = (
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_READY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_VALID"
)
CANDIDATE_BUILT_OFFLINE_BINDING = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_BUILT_OFFLINE_BINDING"
)
CANDIDATE_OBJECT_BINDING = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_OBJECT_BINDING"
)

EXPECTED_CANDIDATE_DIGEST = (
    "dce3a92d05eaba5c2b9307c08799c27bbadb69e804c27c157c7290eec705c340"
)
EXPECTED_CANDIDATE_CHECKLIST_TOTAL = 75
EXPECTED_CANDIDATE_CHECKLIST_PASSED = 75
EXPECTED_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_CANDIDATE_BLOCKER_COUNT = 0

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER

REQUIRED_CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "refined_evidence_candidate_digest_bound",
    "refinement_results_review_digest_bound",
    "refinement_execution_digest_bound",
    "refinement_execution_approval_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_candidate_universe",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "feature_label_refinement_results_review_ready_true",
    "refinement_results_support_future_additional_predictive_evidence_planning_true",
    "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence_true",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_created_true",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created_true",
    "candidate_scope_refined_evidence_candidate_only",
    "candidate_authority_status_not_authorized",
    "refined_label_family_count_7",
    "refined_label_available_values_82698",
    "refined_label_unavailable_values_924",
    "refined_feature_group_count_9",
    "refined_feature_fields_19",
    "refined_protocol_group_count_6",
    "model_comparison_group_count_5",
    "refined_walk_forward_fold_count_4",
    "refined_oos_rows_2988",
    "refined_oos_accuracy_range_bound",
    "refined_leakage_status_pass",
    "failed_leakage_controls_zero",
    "source_refinement_inputs_reviewed",
    "planned_execution_activities_reviewed",
    "planned_outputs_10_reviewed",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "per_ticker_candidate_entries_12",
    "per_ticker_candidate_digests_present",
    "per_ticker_review_digests_present",
    "future_refined_evidence_execution_chain_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
    "dataset_generation_performed_in_review_false",
    "canonical_dataset_regenerated_in_review_false",
    "feature_label_refinement_execution_rerun_performed_false",
    "refined_label_generation_rerun_performed_false",
    "refined_feature_generation_rerun_performed_false",
    "refined_walk_forward_validation_rerun_performed_false",
    "refined_out_of_sample_evaluation_rerun_performed_false",
    "refined_metrics_recomputation_performed_false",
    "model_comparison_rerun_performed_false",
    "additional_predictive_evidence_execution_performed_false",
    "additional_predictive_evidence_execution_approval_created_false",
    "additional_predictive_evidence_execution_for_refined_evidence_approved_false",
    "additional_predictive_evidence_execution_for_refined_evidence_authorized_false",
    "additional_predictive_evidence_execution_for_refined_evidence_executed_false",
    "additional_predictive_evidence_results_for_refined_evidence_created_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
    "predictive_usefulness_acceptance_candidate_created_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "profitability_acceptance_recommended_false",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "no_additional_predictive_evidence_execution_approval_for_refined_evidence_created",
    "no_additional_predictive_evidence_execution_for_refined_evidence_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

FORBIDDEN_ARTIFACT_VALUES = set(candidate_service.FORBIDDEN_ARTIFACT_VALUES)


class AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
    ValueError
):
    """Raised when the review package violates its review-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
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


def _candidate_for_binding(
    candidate: dict[str, Any] | None,
) -> tuple[dict[str, Any], str]:
    if candidate is None:
        bound = candidate_service.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1()
        binding_mode = CANDIDATE_BUILT_OFFLINE_BINDING
    else:
        candidate_service.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
            candidate
        )
        bound = deepcopy(candidate)
        binding_mode = CANDIDATE_OBJECT_BINDING
    _expect(
        bound.get(
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
        ),
        EXPECTED_CANDIDATE_DIGEST,
        "candidate digest",
    )
    return bound, binding_mode


def per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker review entry."""
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest",
        None,
    )
    return semantic_digest(payload)


def _per_ticker_review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    candidate_digest = candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    ]
    for source in candidate["per_ticker_candidate_entries"]:
        entry = deepcopy(source)
        entry[
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_status"
        ] = READY_FOR_OPERATOR_ASSESSMENT
        entry[
            "source_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
        ] = candidate_digest
        entry[
            "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest"
        ] = per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_review_package(
    candidate: dict[str, Any], binding_mode: str
) -> dict[str, Any]:
    summary = candidate["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_V1,
        "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_READY,
        "candidate_binding_mode": binding_mode,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "feature_label_refinement_execution_rerun_performed": False,
        "refined_label_generation_rerun_performed": False,
        "refined_feature_generation_rerun_performed": False,
        "refined_walk_forward_validation_rerun_performed": False,
        "refined_out_of_sample_evaluation_rerun_performed": False,
        "refined_metrics_recomputation_performed": False,
        "model_comparison_rerun_performed": False,
        "additional_predictive_evidence_execution_performed": False,
        "additional_predictive_evidence_execution_approval_created": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "feature_label_refinement_executed": True,
        "feature_label_refinement_results_created": True,
        "feature_label_refinement_results_review_created": True,
        "feature_label_refinement_results_review_ready": True,
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning": True,
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_for_refined_evidence_approved": False,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": False,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
        "additional_predictive_evidence_results_for_refined_evidence_created": False,
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
        "research_only": True,
        "operator_review_required": True,
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_kind": candidate["artifact_kind"],
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_status": candidate["candidate_status"],
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": candidate["additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"],
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_checklist_total": summary["total_checks"],
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_checklist_passed": summary["passed_checks"],
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_checklist_failed": summary["failed_checks"],
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_blocker_count": summary["blocker_count"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": candidate["additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"],
        "feature_label_refinement_results_review_package_digest": candidate["feature_label_refinement_results_review_package_digest"],
        "feature_label_refinement_execution_digest": candidate["feature_label_refinement_execution_digest"],
        "feature_label_refinement_execution_approval_digest": candidate["feature_label_refinement_execution_approval_digest"],
        "additional_predictive_evidence_results_review_package_digest": candidate["additional_predictive_evidence_results_review_package_digest"],
        "additional_predictive_evidence_execution_digest": candidate["additional_predictive_evidence_execution_digest"],
        "research_registry_approval_digest": candidate["research_registry_approval_digest"],
        "canonical_dataset_freeze_digest": candidate["canonical_dataset_freeze_digest"],
        "records_digest": candidate["records_digest"],
        "target_universe": list(candidate["target_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "registry_approved_dataset_metadata": deepcopy(candidate["registry_approved_dataset_metadata"]),
        "dataset_name": candidate["dataset_name"],
        "total_canonical_record_count": candidate["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(candidate["per_ticker_record_counts"]),
        "meta_record_count": candidate["meta_record_count"],
        "non_meta_record_count": candidate["non_meta_record_count"],
        "source_refinement_output_root": candidate["source_refinement_output_root"],
        "source_refinement_output_count": candidate["source_refinement_output_count"],
        "source_refinement_output_status": candidate["source_refinement_output_status"],
        "source_refinement_results_review_ready": candidate["source_refinement_results_review_ready"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_objective": candidate["additional_predictive_evidence_execution_candidate_for_refined_evidence_objective"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_scope": candidate["additional_predictive_evidence_execution_candidate_for_refined_evidence_scope"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_mode": candidate["additional_predictive_evidence_execution_candidate_for_refined_evidence_mode"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status": candidate["additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status"],
        "refined_label_family_count": candidate["refined_label_family_count"],
        "refined_label_coverage_entries": candidate["refined_label_coverage_entries"],
        "refined_label_available_values": candidate["refined_label_available_values"],
        "refined_label_unavailable_values": candidate["refined_label_unavailable_values"],
        "refined_label_generation_digest": candidate["refined_label_generation_digest"],
        "refined_feature_group_count": candidate["refined_feature_group_count"],
        "refined_feature_category_count": candidate["refined_feature_category_count"],
        "refined_feature_field_count": candidate["refined_feature_field_count"],
        "refined_feature_rows": candidate["refined_feature_rows"],
        "refined_feature_null_or_unavailable_values": candidate["refined_feature_null_or_unavailable_values"],
        "refined_feature_generation_digest": candidate["refined_feature_generation_digest"],
        "refined_protocol_group_count": candidate["refined_protocol_group_count"],
        "chronological_splits": candidate["chronological_splits"],
        "one_session_embargo": candidate["one_session_embargo"],
        "no_shuffle": candidate["no_shuffle"],
        "no_lookahead": candidate["no_lookahead"],
        "refined_walk_forward_fold_count": candidate["refined_walk_forward_fold_count"],
        "refined_walk_forward_evaluation_rows": candidate["refined_walk_forward_evaluation_rows"],
        "refined_oos_evaluation_rows": candidate["refined_oos_evaluation_rows"],
        "refined_oos_accuracy_range": candidate["refined_oos_accuracy_range"],
        "model_comparison_group_count": candidate["model_comparison_group_count"],
        "deterministic_comparisons_evaluated": candidate["deterministic_comparisons_evaluated"],
        "unavailable_model_family_requests": candidate["unavailable_model_family_requests"],
        "unavailable_model_family_status": candidate["unavailable_model_family_status"],
        "refined_leakage_status": candidate["refined_leakage_status"],
        "failed_leakage_controls": candidate["failed_leakage_controls"],
        "data_quality_status": candidate["data_quality_status"],
        "reviewed_planned_refined_evidence_inputs": deepcopy(candidate["planned_refined_evidence_inputs"]),
        "reviewed_planned_execution_activities": deepcopy(candidate["planned_execution_activities"]),
        "reviewed_planned_outputs": deepcopy(candidate["planned_outputs"]),
        "per_ticker_candidate_review_entries": _per_ticker_review_entries(candidate),
        "reviewed_future_refined_evidence_execution_chain": list(candidate["future_refined_evidence_execution_chain"]),
        "reviewed_future_gates": list(candidate["future_gates"]),
        "reviewed_risk_controls": list(candidate["risk_controls"]),
        "additional_predictive_evidence_execution_approval_for_refined_evidence_artifact_created": False,
        "additional_predictive_evidence_execution_for_refined_evidence_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    outputs = review_package.get("reviewed_planned_outputs", [])
    entries = review_package.get("per_ticker_candidate_review_entries", [])
    fields: dict[str, tuple[Any, Any]] = {
        "candidate_kind_matches": (candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_kind")),
        "candidate_status_ready_for_review": (candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_status")),
        "candidate_digest_matches_expected": (EXPECTED_CANDIDATE_DIGEST, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest")),
        "candidate_checklist_zero_blockers": (0, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_blocker_count")),
        "refined_evidence_candidate_digest_bound": (EXPECTED_CANDIDATE_DIGEST, review_package.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_digest")),
        "refinement_results_review_digest_bound": (candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST, review_package.get("feature_label_refinement_results_review_package_digest")),
        "refinement_execution_digest_bound": (candidate_service.EXPECTED_REFINEMENT_EXECUTION_DIGEST, review_package.get("feature_label_refinement_execution_digest")),
        "refinement_execution_approval_digest_bound": (candidate_service.EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST, review_package.get("feature_label_refinement_execution_approval_digest")),
        "research_registry_approval_digest_bound": (candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, review_package.get("research_registry_approval_digest")),
        "canonical_dataset_freeze_digest_bound": (candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, review_package.get("canonical_dataset_freeze_digest")),
        "records_digest_bound": (candidate_service.EXPECTED_RECORDS_DIGEST, review_package.get("records_digest")),
        "target_universe_count_12": (12, review_package.get("target_universe_count")),
        "target_universe_matches_candidate_universe": (TARGET_UNIVERSE, review_package.get("target_universe")),
        "total_canonical_record_count_11946": (11946, review_package.get("total_canonical_record_count")),
        "meta_record_count_913_preserved": (913, review_package.get("meta_record_count")),
        "non_meta_record_counts_1003_preserved": (True, all(review_package.get("per_ticker_record_counts", {}).get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META")),
        "feature_label_refinement_results_review_ready_true": (True, review_package.get("feature_label_refinement_results_review_ready")),
        "refinement_results_support_future_additional_predictive_evidence_planning_true": (True, review_package.get("feature_label_refinement_results_support_future_additional_predictive_evidence_planning")),
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence_true": (True, review_package.get("ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence")),
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created_true": (True, review_package.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_created")),
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created_true": (True, review_package.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created")),
        "candidate_scope_refined_evidence_candidate_only": (candidate_service.CANDIDATE_SCOPE, review_package.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_scope")),
        "candidate_authority_status_not_authorized": (NOT_AUTHORIZED, review_package.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status")),
        "refined_label_family_count_7": (7, review_package.get("refined_label_family_count")),
        "refined_label_available_values_82698": (82698, review_package.get("refined_label_available_values")),
        "refined_label_unavailable_values_924": (924, review_package.get("refined_label_unavailable_values")),
        "refined_feature_group_count_9": (9, review_package.get("refined_feature_group_count")),
        "refined_feature_fields_19": (19, review_package.get("refined_feature_field_count")),
        "refined_protocol_group_count_6": (6, review_package.get("refined_protocol_group_count")),
        "model_comparison_group_count_5": (5, review_package.get("model_comparison_group_count")),
        "refined_walk_forward_fold_count_4": (4, review_package.get("refined_walk_forward_fold_count")),
        "refined_oos_rows_2988": (2988, review_package.get("refined_oos_evaluation_rows")),
        "refined_oos_accuracy_range_bound": ("0.119813 to 0.480924", review_package.get("refined_oos_accuracy_range")),
        "refined_leakage_status_pass": (PASS, review_package.get("refined_leakage_status")),
        "failed_leakage_controls_zero": (0, review_package.get("failed_leakage_controls")),
        "source_refinement_inputs_reviewed": (candidate_service.PLANNED_REFINED_EVIDENCE_INPUT_IDS, [item.get("input_id") for item in review_package.get("reviewed_planned_refined_evidence_inputs", [])]),
        "planned_execution_activities_reviewed": (candidate_service.PLANNED_EXECUTION_ACTIVITY_IDS, [item.get("activity_id") for item in review_package.get("reviewed_planned_execution_activities", [])]),
        "planned_outputs_10_reviewed": (10, len(outputs)),
        "planned_outputs_not_generated": (True, bool(outputs) and all(item.get("generation_status") == candidate_service.PLANNED_NOT_GENERATED for item in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(item.get("actionability_label") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)),
        "per_ticker_candidate_entries_12": (12, len(entries)),
        "per_ticker_candidate_digests_present": (True, bool(entries) and all(isinstance(item.get("per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"), str) and len(item["per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"]) == 64 for item in entries)),
        "per_ticker_review_digests_present": (True, bool(entries) and all(isinstance(item.get("per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest"), str) and len(item["per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest"]) == 64 for item in entries)),
        "future_refined_evidence_execution_chain_reviewed": (candidate_service.FUTURE_REFINED_EVIDENCE_EXECUTION_CHAIN, review_package.get("reviewed_future_refined_evidence_execution_chain")),
        "future_gates_defined": (candidate_service.FUTURE_GATES, review_package.get("reviewed_future_gates")),
        "risk_controls_defined": (candidate_service.RISK_CONTROLS, review_package.get("reviewed_risk_controls")),
    }
    false_fields = {
        "provider_requests_made_in_review_false": "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review_false": "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review_false": "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review_false": "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review_false": "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed_false": "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed_false": "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed_false": "refined_feature_generation_rerun_performed",
        "refined_walk_forward_validation_rerun_performed_false": "refined_walk_forward_validation_rerun_performed",
        "refined_out_of_sample_evaluation_rerun_performed_false": "refined_out_of_sample_evaluation_rerun_performed",
        "refined_metrics_recomputation_performed_false": "refined_metrics_recomputation_performed",
        "model_comparison_rerun_performed_false": "model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_performed_false": "additional_predictive_evidence_execution_performed",
        "additional_predictive_evidence_execution_approval_created_false": "additional_predictive_evidence_execution_approval_created",
        "additional_predictive_evidence_execution_for_refined_evidence_approved_false": "additional_predictive_evidence_execution_for_refined_evidence_approved",
        "additional_predictive_evidence_execution_for_refined_evidence_authorized_false": "additional_predictive_evidence_execution_for_refined_evidence_authorized",
        "additional_predictive_evidence_execution_for_refined_evidence_executed_false": "additional_predictive_evidence_execution_for_refined_evidence_executed",
        "additional_predictive_evidence_results_for_refined_evidence_created_false": "additional_predictive_evidence_results_for_refined_evidence_created",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready_false": "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended_false": "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created_false": "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready_false": "profitability_acceptance_ready",
        "profitability_acceptance_recommended_false": "profitability_acceptance_recommended",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "no_additional_predictive_evidence_execution_approval_for_refined_evidence_created": "additional_predictive_evidence_execution_approval_for_refined_evidence_artifact_created",
        "no_additional_predictive_evidence_execution_for_refined_evidence_created": "additional_predictive_evidence_execution_for_refined_evidence_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    fields.update(
        {check_id: (False, review_package.get(field)) for check_id, field in false_fields.items()}
    )
    fields.update(
        {
            "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review_package.get("predictive_usefulness")),
            "profitability_not_accepted": (NOT_ACCEPTED, review_package.get("profitability")),
            "runtime_use_not_authorized": (NOT_AUTHORIZED, review_package.get("runtime_use")),
            "strategy_use_not_authorized": (NOT_AUTHORIZED, review_package.get("strategy_use")),
            "paper_trading_not_authorized": (NOT_AUTHORIZED, review_package.get("paper_trading")),
            "broker_execution_not_authorized": (NOT_AUTHORIZED, review_package.get("broker_execution")),
        }
    )
    return [_check(check_id, *fields[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_additional_predictive_evidence_execution_approval_for_refined_evidence": False,
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    payload = deepcopy(review_package)
    payload.pop(
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest",
        None,
    )
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Build the review package from the exact offline refined-evidence candidate."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    package = _base_review_package(bound_candidate, binding_mode)
    package["review_checklist"] = _checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    package[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest"
    ] = additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest_v1(
        package
    )
    validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        package
    )
    return package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expected_candidate() -> dict[str, Any]:
    candidate = candidate_service.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1()
    _expect(
        candidate[
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
        ],
        EXPECTED_CANDIDATE_DIGEST,
        "expected candidate digest",
    )
    return candidate


def _validate_per_ticker_entries(review_package: dict[str, Any]) -> None:
    entries = review_package.get("per_ticker_candidate_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "per-ticker candidate review entries missing"
        )
    _expect(
        entries,
        _per_ticker_review_entries(_expected_candidate()),
        "per-ticker candidate review entries",
    )
    candidate_digest_key = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )
    review_digest_key = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest"
    )
    for entry in entries:
        if not isinstance(entry.get(candidate_digest_key), str) or len(entry[candidate_digest_key]) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
                "per-ticker candidate digest missing"
            )
        review_digest = entry.get(review_digest_key)
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
                "per-ticker review digest missing"
            )
        _expect(
            review_digest,
            per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest_v1(
                entry
            ),
            "per-ticker review digest",
        )


def validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Fail closed unless the package is an exact non-authorizing review."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    binding_mode = review_package.get("candidate_binding_mode")
    if binding_mode not in {CANDIDATE_BUILT_OFFLINE_BINDING, CANDIDATE_OBJECT_BINDING}:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "candidate_binding_mode mismatch"
        )
    expected_base = _base_review_package(_expected_candidate(), binding_mode)
    for field, expected in expected_base.items():
        if field in {
            "reviewed_planned_refined_evidence_inputs",
            "reviewed_planned_execution_activities",
            "reviewed_planned_outputs",
            "reviewed_future_refined_evidence_execution_chain",
            "reviewed_future_gates",
            "reviewed_risk_controls",
        } and not review_package.get(field):
            raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
                f"{field} missing"
            )
        _expect(review_package.get(field), expected, field)
    _validate_per_ticker_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist],
        REQUIRED_CHECK_IDS,
        "review checklist IDs",
    )
    expected_checklist = _checklist(review_package)
    if any(item["status"] != PASS for item in expected_checklist):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "review checklist contains a failed check"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get(
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "review package digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest_v1(
            review_package
        ),
        "review package digest",
    )
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest": digest,
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        "ready_for_operator_assessment": True,
        "blocker_count": 0,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": False,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized Markdown summary of the operator-review package."""
    validation = validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Refined-Evidence Execution Candidate Operator Review",
        "",
        "## Title",
        "- Additional Predictive Evidence Execution Candidate for Refined Evidence Operator Review Package v1.",
        "",
        "## Additional Predictive Evidence Execution Candidate for Refined Evidence Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
        f"- Review digest: `{validation['additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest']}`.",
        "",
        "## Reviewed Candidate",
        f"- Candidate kind/status: `{review_package['reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_kind']}` / `{review_package['reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_status']}`.",
        f"- Candidate digest/checks/blockers: `{review_package['reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest']}` / `{review_package['reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_checklist_total']}` / `{review_package['reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_blocker_count']}`.",
        "",
        "## Source Feature/Label Refinement Results Review",
        f"- Results-review digest: `{review_package['feature_label_refinement_results_review_package_digest']}`.",
        f"- Refinement-execution digest: `{review_package['feature_label_refinement_execution_digest']}`.",
        "",
        "## Registry-Approved Dataset Metadata",
    ]
    lines.extend(
        f"- {key}: `{value}`"
        for key, value in review_package["registry_approved_dataset_metadata"].items()
    )
    lines.extend(
        [
            "",
            "## Target Universe",
            f"- `{' '.join(review_package['target_universe'])}`.",
            "",
            "## Refined Evidence Source Profile",
            f"- Root/count/status: `{review_package['source_refinement_output_root']}` / `{review_package['source_refinement_output_count']}` / `{review_package['source_refinement_output_status']}`.",
            "",
            "## Refined Evidence Facts",
            f"- Label/feature/protocol/model groups: `{review_package['refined_label_family_count']}` / `{review_package['refined_feature_group_count']}` / `{review_package['refined_protocol_group_count']}` / `{review_package['model_comparison_group_count']}`.",
            f"- Walk-forward/OOS rows: `{review_package['refined_walk_forward_evaluation_rows']}` / `{review_package['refined_oos_evaluation_rows']}`.",
            "",
            "## Reviewed Refined Evidence Inputs",
        ]
    )
    lines.extend(
        f"- `{item['input_id']}`: `{item['source_status']}`."
        for item in review_package["reviewed_planned_refined_evidence_inputs"]
    )
    lines.extend(["", "## Reviewed Execution Activities"])
    lines.extend(
        f"- `{item['activity_id']}`: `{item['execution_status']}`."
        for item in review_package["reviewed_planned_execution_activities"]
    )
    lines.extend(["", "## Reviewed Planned Outputs"])
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`."
        for item in review_package["reviewed_planned_outputs"]
    )
    lines.extend(["", "## Per-Ticker Candidate Review Entries"])
    lines.extend(
        f"- `{item['ticker']}`: `{item['historical_record_count']}` records; `{item['additional_predictive_evidence_execution_candidate_for_refined_evidence_review_status']}`."
        for item in review_package["per_ticker_candidate_review_entries"]
    )
    for heading, key in (
        ("Future Refined-Evidence Execution Chain", "reviewed_future_refined_evidence_execution_chain"),
        ("Future Gates", "reviewed_future_gates"),
        ("Risk Controls", "reviewed_risk_controls"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in review_package[key])
    lines.extend(
        [
            "",
            "## Execution Boundary",
            "- Review package only; additional predictive-evidence approval, authorization, execution, and results remain false.",
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness remains `{review_package['predictive_usefulness']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability remains `{review_package['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{review_package['runtime_use']}` / `{review_package['strategy_use']}` / `{review_package['paper_trading']}` / `{review_package['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- No provider request, acquisition, dataset regeneration, refinement rerun, metric recomputation, model rerun, execution approval, strategy scoring, recommendation, acceptance, or runtime activation occurs.",
            "- Reviewed evidence remains research-only and non-actionable; META's exact 913-record limitation remains preserved.",
            "",
        ]
    )
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON once; existing output fails closed."""
    package = build_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        candidate
    )
    validation = validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        package
    )
    output_name = filename or (
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "review filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError(
            "review output already exists"
        ) from exc
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
