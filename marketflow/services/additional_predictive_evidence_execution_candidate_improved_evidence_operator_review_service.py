"""Offline operator review for the improved-evidence execution candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_execution_candidate_improved_evidence_service as candidate_service


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_V1 = (
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_READY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_VALID"
)

DEFAULT_BRANCH = "feature/additional-predictive-evidence-execution-candidate-review-improved-evidence-v1"
DEFAULT_BASE_COMMIT = "3471fb33418c0c0cc0a28ffeac46358944a0712b"
EXPECTED_CANDIDATE_DIGEST = "5705fd75afa0d614836f5b74d8a074054fd4f45b9395d5694f9f647a9322956f"
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
SELECTED_DIRECTION = candidate_service.SELECTED_DIRECTION
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


class AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(ValueError):
    """Raised when the review violates its non-authorizing contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
            f"{field} mismatch"
        )


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": expected, "actual": actual,
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1()
        if candidate is None else deepcopy(candidate)
    )
    candidate_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(source)
    _expect(source.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"),
            EXPECTED_CANDIDATE_DIGEST, "source candidate digest")
    summary = source.get("candidate_summary", {})
    _expect(summary.get("total_checks"), 78, "source checklist total")
    _expect(summary.get("passed_checks"), 78, "source checklist passed")
    _expect(summary.get("failed_checks"), 0, "source checklist failed")
    _expect(summary.get("blocker_count"), 0, "source blocker count")
    return source


def per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_additional_predictive_evidence_execution_candidate_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for source_entry in source["per_ticker_candidate_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry["meta_reduced_record_count_flag"],
            "improved_evidence_planning_results_review_status": source_entry[
                "improved_evidence_planning_results_review_status"
            ],
            "additional_predictive_evidence_execution_candidate_status": source_entry[
                "additional_predictive_evidence_execution_candidate_status"
            ],
            "additional_predictive_evidence_execution_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "selected_redesign_direction": source_entry["selected_redesign_direction"],
            "additional_predictive_evidence_execution_approved": False,
            "additional_predictive_evidence_execution_authorized": False,
            "additional_predictive_evidence_executed": False,
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "new_targets_created": False, "target_definition_change_authorized": False,
            "feature_generation_authorized": False, "feature_generation_performed": False,
            "feature_label_matrix_created": False, "metric_recomputation_performed_in_review": False,
            "model_training_performed_in_review": False, "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_additional_predictive_evidence_execution_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
            "per_ticker_additional_predictive_evidence_execution_candidate_digest": source_entry[
                "per_ticker_additional_predictive_evidence_execution_candidate_digest"
            ],
        }
        if "candidate_note" in source_entry:
            entry["candidate_note"] = source_entry["candidate_note"]
        entry["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"] = (
            per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _reviewed_candidate_objective(source: Mapping[str, Any]) -> dict[str, Any]:
    fields = [
        "additional_predictive_evidence_execution_candidate_objective",
        "additional_predictive_evidence_execution_candidate_scope",
        "additional_predictive_evidence_execution_candidate_mode",
        "additional_predictive_evidence_execution_candidate_authority_status",
    ]
    return {field: source[field] for field in fields}


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_V1,
        "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_READY,
        "branch": DEFAULT_BRANCH, "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_candidate_artifact_kind": source["artifact_kind"],
        "source_candidate_status": source["candidate_status"],
        "source_candidate_digest": source[
            "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"
        ],
        "source_candidate_checklist_total": summary["total_checks"],
        "source_candidate_checklist_passed": summary["passed_checks"],
        "source_candidate_checklist_failed": summary["failed_checks"],
        "source_candidate_blocker_count": summary["blocker_count"],
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": source[
            "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"
        ],
        **deepcopy(candidate_service.BOUND_DIGESTS),
        "improved_evidence_planning_results_review_created": True,
        "improved_evidence_planning_results_review_ready": True,
        "source_results_review_ready": True,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_created": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created": True,
        "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "feature_generation_authorized": False,
        "feature_generation_performed": False, "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_review": False, "model_training_performed_in_review": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False, "profitability_acceptance_created": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_migration_approval_created": False, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "automatic_stitching": False,
        "new_strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False, "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "redesigned_label_regeneration_performed": False, "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "improved_evidence_planning_execution_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "dataset_name": source["dataset_name"], "source_profile": source["source_profile"],
        "timeframe": source["timeframe"], "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"], "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "records_digest": source["records_digest"], "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source["meta_reduced_record_count_preserved"],
        "selected_redesign_direction": source["selected_redesign_direction"],
        "majority_structure_risk": source["majority_structure_risk"],
        "largest_aggregated_class": source["largest_aggregated_class"],
        "largest_aggregated_class_count": source["largest_aggregated_class_count"],
        "no_trade_count": source["no_trade_count"], "oos_evaluated_rows": source["oos_evaluated_rows"],
        "majority_accuracy": source["majority_accuracy"], "local_model_accuracy": source["local_model_accuracy"],
        "cross_sectional_accuracy": source["cross_sectional_accuracy"],
        "cross_sectional_delta_vs_majority": source["cross_sectional_delta_vs_majority"],
        "global_five_session_threshold": source["global_five_session_threshold"],
        "benchmark_relative_threshold": source["benchmark_relative_threshold"],
        "reviewed_candidate_basis": deepcopy(source["candidate_basis"]),
        "reviewed_candidate_objective": _reviewed_candidate_objective(source),
        "reviewed_planned_source_inputs": deepcopy(source["planned_source_inputs"]),
        "reviewed_planned_execution_activities": deepcopy(source["planned_execution_activities"]),
        "reviewed_label_feature_matrix_boundaries": deepcopy(source["label_feature_matrix_boundaries"]),
        "reviewed_planned_model_and_baseline_families": deepcopy(source["planned_model_and_baseline_families"]),
        "reviewed_planned_metric_families": deepcopy(source["planned_metric_families"]),
        "reviewed_planned_future_outputs": deepcopy(source["planned_future_outputs"]),
        "per_ticker_review_entries": _per_ticker_review_entries(source),
        "next_chain": deepcopy(source["next_chain"]), "next_gates": deepcopy(source["next_gates"]),
        "risk_controls": deepcopy(source["risk_controls"]), "no_tracked_marketflow_files": True,
    }


CHECK_FIELD_SPECS = [
    ("candidate_kind_matches", candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE, "source_candidate_artifact_kind"),
    ("candidate_status_ready_for_review", candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_READY_FOR_OPERATOR_REVIEW, "source_candidate_status"),
    ("candidate_digest_matches_expected", EXPECTED_CANDIDATE_DIGEST, "source_candidate_digest"),
    ("candidate_checklist_zero_blockers", 0, "source_candidate_blocker_count"),
    ("additional_predictive_evidence_execution_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"),
    ("planning_results_review_digest_bound", candidate_service.BOUND_DIGESTS["improved_evidence_planning_results_review_using_redesigned_evidence_digest"], "improved_evidence_planning_results_review_using_redesigned_evidence_digest"),
    ("planning_execution_digest_bound", candidate_service.BOUND_DIGESTS["improved_evidence_planning_execution_using_redesigned_evidence_digest"], "improved_evidence_planning_execution_using_redesigned_evidence_digest"),
    ("planning_output_binding_digest_bound", candidate_service.BOUND_DIGESTS["improved_evidence_planning_output_binding_digest"], "improved_evidence_planning_output_binding_digest"),
    ("planning_approval_digest_bound", candidate_service.BOUND_DIGESTS["improved_evidence_planning_approval_using_redesigned_evidence_digest"], "improved_evidence_planning_approval_using_redesigned_evidence_digest"),
    ("planning_candidate_review_digest_bound", candidate_service.BOUND_DIGESTS["improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"], "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"),
    ("planning_candidate_digest_bound", candidate_service.BOUND_DIGESTS["improved_evidence_planning_candidate_using_redesigned_evidence_digest"], "improved_evidence_planning_candidate_using_redesigned_evidence_digest"),
    ("redesign_results_review_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_results_review_using_redesigned_evidence_digest"], "label_objective_redesign_results_review_using_redesigned_evidence_digest"),
    ("redesign_execution_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_execution_using_redesigned_evidence_digest"], "label_objective_redesign_execution_using_redesigned_evidence_digest"),
    ("redesign_output_binding_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_output_binding_digest"], "label_objective_redesign_output_binding_digest"),
    ("target_definition_results_review_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], "label_objective_target_definition_results_review_using_redesigned_evidence_digest"),
    ("target_definition_execution_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"),
    ("path_selection_digest_bound", candidate_service.BOUND_DIGESTS["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], "method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
    ("readiness_review_digest_bound", candidate_service.BOUND_DIGESTS["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
    ("reassessment_digest_bound", candidate_service.BOUND_DIGESTS["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], "predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
    ("predictive_results_review_digest_bound", candidate_service.BOUND_DIGESTS["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], "additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
    ("predictive_execution_digest_bound", candidate_service.BOUND_DIGESTS["additional_predictive_evidence_execution_using_redesigned_labels_digest"], "additional_predictive_evidence_execution_using_redesigned_labels_digest"),
    ("matrix_digest_bound", candidate_service.BOUND_DIGESTS["feature_label_matrix_digest"], "feature_label_matrix_digest"),
    ("feature_values_digest_bound", candidate_service.BOUND_DIGESTS["feature_values_digest"], "feature_values_digest"),
    ("label_values_digest_bound", candidate_service.BOUND_DIGESTS["redesigned_label_values_digest"], "redesigned_label_values_digest"),
    ("research_registry_digest_bound", candidate_service.BOUND_DIGESTS["research_registry_approval_digest"], "research_registry_approval_digest"),
    ("records_digest_bound", candidate_service.BOUND_DIGESTS["records_digest"], "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", candidate_service.BOUND_DIGESTS["records_digest"], "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("source_results_review_ready_true", True, "source_results_review_ready"),
    ("ready_for_additional_predictive_evidence_candidate_true", True, "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence"),
    ("candidate_created_true", True, "additional_predictive_evidence_execution_candidate_created"),
    ("candidate_review_created_true", True, "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created"),
    ("candidate_ready_true", True, "additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review"),
    ("execution_approved_false", False, "additional_predictive_evidence_execution_approved"),
    ("execution_authorized_false", False, "additional_predictive_evidence_execution_authorized"),
    ("execution_performed_false", False, "additional_predictive_evidence_executed"),
    ("results_created_false", False, "additional_predictive_evidence_results_created"),
    ("selected_redesign_direction_preserved", SELECTED_DIRECTION, "selected_redesign_direction"),
    ("label_regeneration_authorized_false", False, "label_regeneration_authorized"),
    ("label_regeneration_performed_false", False, "label_regeneration_performed"),
    ("new_targets_created_false", False, "new_targets_created"),
    ("target_definition_change_authorized_false", False, "target_definition_change_authorized"),
    ("target_definition_change_performed_false", False, "target_definition_change_performed"),
    ("feature_generation_authorized_false", False, "feature_generation_authorized"),
    ("feature_generation_performed_false", False, "feature_generation_performed"),
    ("feature_label_matrix_created_false", False, "feature_label_matrix_created"),
    ("metric_recomputation_in_review_false", False, "metric_recomputation_performed_in_review"),
    ("model_training_in_review_false", False, "model_training_performed_in_review"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("candidate_basis_reviewed", candidate_service.CANDIDATE_BASIS, "reviewed_candidate_basis"),
    ("candidate_objective_reviewed", True, "candidate_objective_valid"),
    ("planned_source_inputs_reviewed", True, "source_inputs_valid"),
    ("planned_execution_activities_reviewed", True, "activities_valid"),
    ("label_feature_matrix_boundaries_reviewed", candidate_service._label_feature_matrix_boundaries(), "reviewed_label_feature_matrix_boundaries"),
    ("model_families_planned_not_evaluated", True, "models_valid"),
    ("metric_families_planned_not_computed", True, "metrics_valid"),
    ("future_outputs_not_generated", True, "outputs_valid"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_candidate_digests_present", True, "per_ticker_candidate_digests_valid"),
    ("per_ticker_review_digests_present", True, "per_ticker_review_digests_valid"),
    ("provider_requests_made_false", False, "provider_requests_made_in_review"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed_in_review"),
    ("dataset_regeneration_false", False, "canonical_dataset_regenerated_in_review"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("feature_regeneration_false", False, "feature_regeneration_performed"),
    ("predictive_evidence_rerun_false", False, "predictive_evidence_execution_rerun_performed"),
    ("improved_evidence_planning_execution_rerun_false", False, "improved_evidence_planning_execution_rerun_performed"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("next_chain_reviewed", candidate_service.NEXT_CHAIN, "next_chain"),
    ("next_gates_reviewed", candidate_service.NEXT_GATES, "next_gates"),
    ("risk_controls_reviewed", candidate_service.RISK_CONTROLS, "risk_controls"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [row[0] for row in CHECK_FIELD_SPECS]


def _derived_fields(review_package: Mapping[str, Any]) -> dict[str, Any]:
    objective = review_package.get("reviewed_candidate_objective")
    entries = review_package.get("per_ticker_review_entries", [])
    return {
        **review_package,
        "candidate_objective_valid": objective == {
            "additional_predictive_evidence_execution_candidate_objective": candidate_service.CANDIDATE_OBJECTIVE,
            "additional_predictive_evidence_execution_candidate_scope": candidate_service.CANDIDATE_SCOPE,
            "additional_predictive_evidence_execution_candidate_mode": candidate_service.CANDIDATE_MODE,
            "additional_predictive_evidence_execution_candidate_authority_status": candidate_service.CANDIDATE_AUTHORITY_STATUS,
        },
        "source_inputs_valid": review_package.get("reviewed_planned_source_inputs") == candidate_service._planned_source_inputs(),
        "activities_valid": review_package.get("reviewed_planned_execution_activities") == candidate_service._planned_execution_activities(),
        "models_valid": review_package.get("reviewed_planned_model_and_baseline_families") == candidate_service._planned_model_families(),
        "metrics_valid": review_package.get("reviewed_planned_metric_families") == candidate_service._planned_metric_families(),
        "outputs_valid": review_package.get("reviewed_planned_future_outputs") == candidate_service._planned_future_outputs(),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_candidate_digests_valid": (
            isinstance(entries, list) and len(entries) == 12 and all(
                isinstance(row.get("per_ticker_additional_predictive_evidence_execution_candidate_digest"), str)
                and len(row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]) == 64
                for row in entries
            )
        ),
        "per_ticker_review_digests_valid": (
            isinstance(entries, list) and len(entries) == 12 and all(
                isinstance(row.get("per_ticker_additional_predictive_evidence_execution_candidate_review_digest"), str)
                and len(row["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"]) == 64
                and row["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"]
                == per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(row)
                for row in entries
            )
        ),
    }


def _checklist(review_package: Mapping[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_fields(review_package)
    return [_check(check_id, expected, fields.get(field))
            for check_id, expected, field in CHECK_FIELD_SPECS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_additional_predictive_evidence_execution_approval": False,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "feature_generation_performed": False,
        "feature_label_matrix_created": False, "metric_recomputation_performed": False,
        "model_training_performed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest_v1(
    review_package: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review_package))
    payload.pop("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest", None)
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Build a review-only package around a validated candidate."""
    source = _source_candidate(candidate)
    review = _base_review(source)
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review["additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest"] = (
        additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest_v1(review)
    )
    validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(review)
    return review


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED", "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE", "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED", "RUNTIME_MIGRATION_APPROVED", "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION", "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "additional_predictive_evidence_execution_approved", "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "metric_recomputation_performed_in_review", "model_training_performed_in_review",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved", "runtime_migration_active",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_evidence_execution_rerun_performed",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
                    f"{current} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
                    f"{current} must remain not accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Fail closed unless the package is exactly the review-only contract."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
            "review package must be a JSON object"
        )
    _expect(review_package.get("artifact_kind"),
            ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE,
            "artifact_kind")
    _expect(review_package.get("schema_version"),
            SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_V1,
            "schema_version")
    _expect(review_package.get("review_status"),
            ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_READY,
            "review_status")
    _reject_forbidden_values(review_package)
    expected = {
        "source_candidate_artifact_kind": candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE,
        "source_candidate_status": candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "source_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "source_candidate_checklist_total": 78, "source_candidate_checklist_passed": 78,
        "source_candidate_checklist_failed": 0, "source_candidate_blocker_count": 0,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **candidate_service.BOUND_DIGESTS,
        "dataset_name": "expanded_universe_canonical_dataset_v1", "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d", "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "records_digest": candidate_service.BOUND_DIGESTS["records_digest"],
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "reviewed_candidate_basis": candidate_service.CANDIDATE_BASIS,
        "reviewed_candidate_objective": {
            "additional_predictive_evidence_execution_candidate_objective": candidate_service.CANDIDATE_OBJECTIVE,
            "additional_predictive_evidence_execution_candidate_scope": candidate_service.CANDIDATE_SCOPE,
            "additional_predictive_evidence_execution_candidate_mode": candidate_service.CANDIDATE_MODE,
            "additional_predictive_evidence_execution_candidate_authority_status": candidate_service.CANDIDATE_AUTHORITY_STATUS,
        },
        "reviewed_planned_source_inputs": candidate_service._planned_source_inputs(),
        "reviewed_planned_execution_activities": candidate_service._planned_execution_activities(),
        "reviewed_label_feature_matrix_boundaries": candidate_service._label_feature_matrix_boundaries(),
        "reviewed_planned_model_and_baseline_families": candidate_service._planned_model_families(),
        "reviewed_planned_metric_families": candidate_service._planned_metric_families(),
        "reviewed_planned_future_outputs": candidate_service._planned_future_outputs(),
        "next_chain": candidate_service.NEXT_CHAIN, "next_gates": candidate_service.NEXT_GATES,
        "risk_controls": candidate_service.RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
    true_fields = [
        "created_offline", "research_only", "operator_review_required",
        "improved_evidence_planning_results_review_created", "improved_evidence_planning_results_review_ready",
        "source_results_review_ready",
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_created",
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review",
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ]
    false_fields = [
        "additional_predictive_evidence_execution_approved", "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "metric_recomputation_performed_in_review", "model_training_performed_in_review",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "profitability_acceptance_created", "runtime_migration_approved", "runtime_migration_active",
        "runtime_migration_approval_created", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review", "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review", "canonical_dataset_regenerated_in_review",
        "redesigned_label_regeneration_performed", "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed",
        "improved_evidence_planning_execution_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ]
    for field in true_fields:
        _expect(review_package.get(field), True, field)
    for field in false_fields:
        _expect(review_package.get(field), False, field)
    _expect(review_package.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    entries = review_package.get("per_ticker_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
            "per-ticker entries mismatch"
        )
    _expect(entries, _per_ticker_review_entries(
        candidate_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1()
    ), "per-ticker entries")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
            "review_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS,
            "review_checklist check ids")
    _expect(checklist, _checklist(review_package), "review_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
            "review_checklist must pass"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get(
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
            "missing review digest"
        )
    _expect(digest,
            additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest_v1(review_package),
            "review digest")
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_VALID,
        "artifact_kind": review_package["artifact_kind"], "review_status": review_package["review_status"],
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest": digest,
        "source_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "per_ticker_review_entry_count": len(entries),
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": True,
        "ready_for_additional_predictive_evidence_execution_approval": False,
        "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a review-only Markdown package."""
    validation = validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Candidate Review Using Improved Evidence Status", "",
        "## Title", "- Optional Additional Predictive Evidence Execution Candidate Operator Review Using Improved Evidence v1.", "",
        "## Optional Additional Predictive Evidence Execution Candidate Review Using Improved Evidence",
        f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest']}`.", "",
        "## Reviewed Candidate",
        f"- `{review_package['source_candidate_artifact_kind']}` / `{review_package['source_candidate_status']}` / `{review_package['source_candidate_digest']}`; checklist 78/78/0/0.", "",
        "## Source Improved Evidence Planning Results Review",
        f"- `{review_package['improved_evidence_planning_results_review_using_redesigned_evidence_digest']}`.", "",
        "## Bound Evidence", f"- The complete candidate and source digest chain is bound; records `{review_package['records_digest']}`.", "",
        "## Dataset and Universe", "- The frozen 12-ticker dataset remains 11,946 rows; META remains 913.", "",
        "## Reviewed Candidate Basis", f"- `{review_package['reviewed_candidate_basis']}`", "",
        "## Reviewed Candidate Objective", f"- `{review_package['reviewed_candidate_objective']}`", "",
        "## Reviewed Planned Source Inputs",
    ]
    lines.extend(f"- `{row['source_input_id']}`: `{row['source_input_status']}`."
                 for row in review_package["reviewed_planned_source_inputs"])
    lines.extend(["", "## Reviewed Planned Execution Activities"])
    lines.extend(f"- `{row['activity_id']}`: `{row['activity_status']}`."
                 for row in review_package["reviewed_planned_execution_activities"])
    lines.extend(["", "## Reviewed Label / Feature / Matrix Boundaries",
                  f"- `{review_package['reviewed_label_feature_matrix_boundaries']}`", "",
                  "## Reviewed Planned Model and Baseline Families"])
    lines.extend(f"- `{row['model_family_id']}`: `{row['model_family_status']}`."
                 for row in review_package["reviewed_planned_model_and_baseline_families"])
    lines.extend(["", "## Reviewed Planned Metric Families"])
    lines.extend(f"- `{row['metric_family_id']}`: `{row['metric_status']}`."
                 for row in review_package["reviewed_planned_metric_families"])
    lines.extend(["", "## Reviewed Planned Future Outputs"])
    lines.extend(f"- `{row['future_output_id']}`: `{row['output_status']}`."
                 for row in review_package["reviewed_planned_future_outputs"])
    lines.extend(["", "## Per-Ticker Review Entries",
                  "- Twelve entries preserve both source candidate and review digests; META remains 913.",
                  "", "## Next Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(review_package["next_chain"], 1))
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in review_package["next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend([
        "", "## Predictive Usefulness Boundary", "- Predictive usefulness remains `not accepted`.",
        "", "## Profitability Boundary", "- Profitability remains `not accepted`.",
        "", "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
        "", "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails",
        "- This review approves and executes nothing, regenerates no labels or features, creates no targets or matrix rows, computes no metrics, trains no model, and produces no trading action.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(
    output_dir: str | Path, *, candidate: dict | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting."""
    review = build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(
        candidate=candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_v1.json"
    payload = canonical_json_bytes(review)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError(
            "review output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"), "filename": path.name,
        "payload_byte_size": len(payload), "payload_sha256": sha256_bytes(payload),
        "review_status": review["review_status"],
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest": review[
            "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest"
        ],
    }
