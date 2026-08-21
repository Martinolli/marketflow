"""Offline operator review of the redesigned-evidence label-objective candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import label_objective_redesign_candidate_redesigned_evidence_service as candidate_service


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1 = (
    "label_objective_redesign_candidate_using_redesigned_evidence_review_v1"
)
LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY"
)
LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID"
)

EXPECTED_CANDIDATE_DIGEST = "3ee05e4b4316d9dd874a3916fed7cf8ee8aa3f73ba7596d0f9473a9714145e45"
SOURCE_CANDIDATE_ARTIFACT_KIND = candidate_service.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE
SOURCE_CANDIDATE_STATUS = candidate_service.LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW
SOURCE_EVIDENCE = deepcopy(candidate_service.SOURCE_EVIDENCE)
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
CANDIDATE_BASIS = deepcopy(candidate_service.CANDIDATE_BASIS)
REDESIGN_THEME_IDS = list(candidate_service.REDESIGN_THEME_IDS)
REDESIGN_OPTION_IDS = list(candidate_service.REDESIGN_OPTION_IDS)
LABEL_FAMILIES = list(candidate_service.LABEL_FAMILIES)
REDESIGN_QUESTIONS = list(candidate_service.REDESIGN_QUESTIONS)
PLANNED_OUTPUT_NAMES = list(candidate_service.PLANNED_OUTPUT_NAMES)
NEXT_CHAIN = list(candidate_service.NEXT_CHAIN)
NEXT_GATES = list(candidate_service.NEXT_GATES)
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)
RECOMMENDED_REDESIGN_DIRECTION = candidate_service.RECOMMENDED_REDESIGN_DIRECTION
RECOMMENDATION_RATIONALE = candidate_service.RECOMMENDATION_RATIONALE
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED

CHECK_IDS = [
    "candidate_kind_matches", "candidate_status_ready_for_review", "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers", "label_objective_redesign_candidate_digest_bound",
    "results_review_digest_bound", "execution_digest_bound", "output_binding_digest_bound",
    "approval_digest_bound", "candidate_review_digest_bound", "path_selection_digest_bound",
    "readiness_review_digest_bound", "reassessment_digest_bound", "predictive_results_review_digest_bound",
    "predictive_execution_digest_bound", "matrix_digest_bound", "feature_values_digest_bound",
    "label_values_digest_bound", "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "results_review_ready_true", "ready_for_optional_redesign_or_refinement_candidate_true",
    "redesign_candidate_created_true", "redesign_candidate_review_created_true",
    "redesign_candidate_ready_true", "label_objective_redesign_approved_false",
    "label_objective_redesign_authorized_false", "label_objective_redesign_executed_false",
    "recommended_redesign_direction_not_selected_for_approval", "label_regeneration_authorized_false",
    "label_regeneration_performed_false", "new_targets_created_false",
    "target_definition_change_authorized_false", "target_definition_change_performed_false",
    "threshold_horizon_refinement_candidate_created_false", "improved_evidence_planning_candidate_created_false",
    "predictive_usefulness_not_accepted", "acceptance_ready_false", "acceptance_candidate_created_false",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "candidate_basis_reviewed",
    "candidate_objective_reviewed", "redesign_themes_reviewed", "redesign_options_reviewed",
    "recommended_redesign_direction_reviewed", "label_family_impact_review_reviewed",
    "redesign_questions_reviewed", "planned_outputs_not_generated", "planned_outputs_research_only",
    "per_ticker_entries_12", "per_ticker_candidate_digests_present", "per_ticker_review_digests_present",
    "provider_requests_made_false", "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false", "predictive_evidence_rerun_false",
    "label_objective_review_execution_rerun_false", "metric_recomputation_in_review_false",
    "model_training_in_review_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_reviewed", "next_gates_reviewed", "risk_controls_reviewed", "no_tracked_marketflow_files",
]

TRUE_FIELDS = [
    "created_offline", "research_only", "operator_review_required",
    "label_objective_target_definition_results_review_created",
    "label_objective_target_definition_results_review_ready",
    "ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence",
    "label_objective_redesign_candidate_created",
    "label_objective_redesign_candidate_using_redesigned_evidence_created",
    "label_objective_redesign_candidate_using_redesigned_evidence_ready_for_operator_review",
    "label_objective_redesign_candidate_using_redesigned_evidence_review_created",
    "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
]
FALSE_FIELDS = [
    "label_objective_redesign_approved", "label_objective_redesign_authorized",
    "label_objective_redesign_executed", "recommended_redesign_direction_selected_for_approval",
    "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
    "target_definition_change_authorized", "target_definition_change_performed",
    "threshold_horizon_refinement_candidate_created", "improved_evidence_planning_candidate_created",
    "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
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
    "metric_recomputation_performed_in_review", "model_training_performed_in_review",
    "raw_provider_payloads_committed", "api_keys_stored_or_printed",
]


class LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError(ValueError):
    """Raised when the operator-review package crosses its review-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError(f"{field} must be false")


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_label_objective_redesign_candidate_using_redesigned_evidence_v1()
        if candidate is None else deepcopy(candidate)
    )
    candidate_service.validate_label_objective_redesign_candidate_using_redesigned_evidence_v1(source)
    _expect(source.get("artifact_kind"), SOURCE_CANDIDATE_ARTIFACT_KIND, "source candidate kind")
    _expect(source.get("candidate_status"), SOURCE_CANDIDATE_STATUS, "source candidate status")
    _expect(source.get("label_objective_redesign_candidate_using_redesigned_evidence_digest"), EXPECTED_CANDIDATE_DIGEST, "source candidate digest")
    summary = source.get("summary", {})
    _expect(summary.get("total_checks"), 69, "source candidate checklist total")
    _expect(summary.get("passed_checks"), 69, "source candidate checklist passed")
    _expect(summary.get("failed_checks"), 0, "source candidate checklist failed")
    _expect(summary.get("blocker_count"), 0, "source candidate blockers")
    return source


def per_ticker_label_objective_redesign_candidate_using_redesigned_evidence_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_label_objective_redesign_candidate_review_digest", None)
    return semantic_digest(payload)


def label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest_v1(
    review_package: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review_package))
    payload.pop("label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_candidate_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry["meta_reduced_record_count_flag"],
            "label_objective_target_definition_results_review_status": source_entry["label_objective_target_definition_results_review_status"],
            "label_objective_redesign_candidate_status": source_entry["label_objective_redesign_candidate_status"],
            "label_objective_redesign_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "label_objective_redesign_approved": False, "label_objective_redesign_executed": False,
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "new_targets_created": False, "target_definition_change_authorized": False,
            "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False, "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "source_label_objective_redesign_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
            "per_ticker_label_objective_redesign_candidate_digest": source_entry["per_ticker_label_objective_redesign_candidate_digest"],
        }
        if source_entry["ticker"] == "META":
            entry["candidate_note"] = source_entry["candidate_note"]
        entry["per_ticker_label_objective_redesign_candidate_review_digest"] = (
            per_ticker_label_objective_redesign_candidate_using_redesigned_evidence_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package(source: Mapping[str, Any]) -> dict[str, Any]:
    evidence = source["source_evidence"]
    package: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1,
        "review_status": LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "source_candidate_artifact_kind": source["artifact_kind"],
        "source_candidate_status": source["candidate_status"],
        "source_candidate_digest": source["label_objective_redesign_candidate_using_redesigned_evidence_digest"],
        "source_candidate_checklist_total": source["summary"]["total_checks"],
        "source_candidate_checklist_passed": source["summary"]["passed_checks"],
        "source_candidate_checklist_failed": source["summary"]["failed_checks"],
        "source_candidate_blocker_count": source["summary"]["blocker_count"],
        "label_objective_redesign_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **deepcopy(evidence),
        "dataset_name": source["dataset_name"], "source_profile": source["source_profile"],
        "timeframe": source["timeframe"], "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"], "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"], "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "reviewed_candidate_basis": deepcopy(source["candidate_basis"]),
        "reviewed_label_objective_redesign_candidate_objective": source["label_objective_redesign_candidate_objective"],
        "reviewed_label_objective_redesign_candidate_scope": source["label_objective_redesign_candidate_scope"],
        "reviewed_label_objective_redesign_candidate_mode": source["label_objective_redesign_candidate_mode"],
        "reviewed_label_objective_redesign_candidate_authority_status": source["label_objective_redesign_candidate_authority_status"],
        "reviewed_redesign_themes": deepcopy(source["redesign_themes"]),
        "reviewed_redesign_options": deepcopy(source["redesign_options"]),
        "recommended_redesign_direction": source["recommended_redesign_direction"],
        "recommended_redesign_direction_rationale": source["recommended_redesign_direction_rationale"],
        "reviewed_label_family_impact_review": deepcopy(source["current_label_family_impact_review"]),
        "reviewed_redesign_questions": deepcopy(source["planned_redesign_questions"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "per_ticker_review_entries": _per_ticker_entries(source),
        "next_chain": deepcopy(source["next_chain"]), "next_gates": deepcopy(source["next_gates"]),
        "risk_controls": deepcopy(source["risk_controls"]),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
    }
    for field in TRUE_FIELDS:
        package[field] = True
    for field in FALSE_FIELDS:
        package[field] = False
    return package


def _check(check_id: str, passed: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": "PASS" if passed else "FAIL",
        "expected": True, "actual": passed, "severity": "BLOCKER",
        "message": f"{check_id} {'passed' if passed else 'failed'}",
    }


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    themes = package.get("reviewed_redesign_themes", [])
    options = package.get("reviewed_redesign_options", [])
    families = package.get("reviewed_label_family_impact_review", [])
    questions = package.get("reviewed_redesign_questions", [])
    outputs = package.get("reviewed_planned_outputs", [])
    entries = package.get("per_ticker_review_entries", [])
    facts = {
        "candidate_kind_matches": package.get("source_candidate_artifact_kind") == SOURCE_CANDIDATE_ARTIFACT_KIND,
        "candidate_status_ready_for_review": package.get("source_candidate_status") == SOURCE_CANDIDATE_STATUS,
        "candidate_digest_matches_expected": package.get("source_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "candidate_checklist_zero_blockers": package.get("source_candidate_blocker_count") == 0,
        "label_objective_redesign_candidate_digest_bound": package.get("label_objective_redesign_candidate_using_redesigned_evidence_digest") == EXPECTED_CANDIDATE_DIGEST,
        "results_review_digest_bound": package.get("label_objective_target_definition_results_review_using_redesigned_evidence_digest") == SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"],
        "execution_digest_bound": package.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest") == SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"],
        "output_binding_digest_bound": package.get("label_objective_target_definition_review_output_binding_digest") == SOURCE_EVIDENCE["label_objective_target_definition_review_output_binding_digest"],
        "approval_digest_bound": package.get("label_objective_target_definition_review_approval_using_redesigned_evidence_digest") == SOURCE_EVIDENCE["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"],
        "candidate_review_digest_bound": package.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest") == SOURCE_EVIDENCE["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"],
        "path_selection_digest_bound": package.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest") == SOURCE_EVIDENCE["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"],
        "readiness_review_digest_bound": package.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest") == SOURCE_EVIDENCE["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"],
        "reassessment_digest_bound": package.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest") == SOURCE_EVIDENCE["predictive_usefulness_reassessment_using_redesigned_evidence_digest"],
        "predictive_results_review_digest_bound": package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest") == SOURCE_EVIDENCE["additional_predictive_evidence_results_review_using_redesigned_labels_digest"],
        "predictive_execution_digest_bound": package.get("additional_predictive_evidence_execution_using_redesigned_labels_digest") == SOURCE_EVIDENCE["additional_predictive_evidence_execution_using_redesigned_labels_digest"],
        "matrix_digest_bound": package.get("feature_label_matrix_digest") == SOURCE_EVIDENCE["feature_label_matrix_digest"],
        "feature_values_digest_bound": package.get("feature_values_digest") == SOURCE_EVIDENCE["feature_values_digest"],
        "label_values_digest_bound": package.get("redesigned_label_values_digest") == SOURCE_EVIDENCE["redesigned_label_values_digest"],
        "research_registry_digest_bound": package.get("research_registry_approval_digest") == SOURCE_EVIDENCE["research_registry_approval_digest"],
        "records_digest_bound": package.get("records_digest") == SOURCE_EVIDENCE["records_digest"],
        "target_universe_12_preserved": package.get("target_universe") == TARGET_UNIVERSE and package.get("target_universe_count") == 12,
        "records_digest_preserved": package.get("records_digest") == SOURCE_EVIDENCE["records_digest"],
        "meta_913_preserved": package.get("meta_record_count") == 913 and package.get("meta_reduced_record_count_preserved") is True,
        "results_review_ready_true": package.get("label_objective_target_definition_results_review_ready") is True,
        "ready_for_optional_redesign_or_refinement_candidate_true": package.get("ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence") is True,
        "redesign_candidate_created_true": package.get("label_objective_redesign_candidate_using_redesigned_evidence_created") is True,
        "redesign_candidate_review_created_true": package.get("label_objective_redesign_candidate_using_redesigned_evidence_review_created") is True,
        "redesign_candidate_ready_true": package.get("label_objective_redesign_candidate_using_redesigned_evidence_ready_for_operator_review") is True,
        "label_objective_redesign_approved_false": package.get("label_objective_redesign_approved") is False,
        "label_objective_redesign_authorized_false": package.get("label_objective_redesign_authorized") is False,
        "label_objective_redesign_executed_false": package.get("label_objective_redesign_executed") is False,
        "recommended_redesign_direction_not_selected_for_approval": package.get("recommended_redesign_direction_selected_for_approval") is False,
        "label_regeneration_authorized_false": package.get("label_regeneration_authorized") is False,
        "label_regeneration_performed_false": package.get("label_regeneration_performed") is False,
        "new_targets_created_false": package.get("new_targets_created") is False,
        "target_definition_change_authorized_false": package.get("target_definition_change_authorized") is False,
        "target_definition_change_performed_false": package.get("target_definition_change_performed") is False,
        "threshold_horizon_refinement_candidate_created_false": package.get("threshold_horizon_refinement_candidate_created") is False,
        "improved_evidence_planning_candidate_created_false": package.get("improved_evidence_planning_candidate_created") is False,
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness") == NOT_ACCEPTED,
        "acceptance_ready_false": package.get("predictive_usefulness_acceptance_ready") is False,
        "acceptance_candidate_created_false": package.get("predictive_usefulness_acceptance_candidate_created") is False,
        "profitability_not_accepted": package.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": package.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": package.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": package.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": package.get("trade_recommendations_generated") is False,
        "candidate_basis_reviewed": package.get("reviewed_candidate_basis") == CANDIDATE_BASIS,
        "candidate_objective_reviewed": package.get("reviewed_label_objective_redesign_candidate_objective") == "PREPARE_OPTIONAL_LABEL_OBJECTIVE_REDESIGN_PATH_AFTER_RESULTS_REVIEW_FOUND_MAJORITY_STRUCTURE_AND_WEAK_EDGE",
        "redesign_themes_reviewed": [row.get("theme") for row in themes] == REDESIGN_THEME_IDS,
        "redesign_options_reviewed": [row.get("option") for row in options] == REDESIGN_OPTION_IDS,
        "recommended_redesign_direction_reviewed": package.get("recommended_redesign_direction") == RECOMMENDED_REDESIGN_DIRECTION,
        "label_family_impact_review_reviewed": [row.get("label_family") for row in families] == LABEL_FAMILIES,
        "redesign_questions_reviewed": [row.get("question") for row in questions] == REDESIGN_QUESTIONS,
        "planned_outputs_not_generated": len(outputs) == 11 and all(row.get("output_status") == "PLANNED_NOT_GENERATED" for row in outputs),
        "planned_outputs_research_only": len(outputs) == 11 and all(row.get("output_scope") == "RESEARCH_ONLY_NON_ACTIONABLE" for row in outputs),
        "per_ticker_entries_12": len(entries) == 12,
        "per_ticker_candidate_digests_present": all(row.get("per_ticker_label_objective_redesign_candidate_digest") for row in entries),
        "per_ticker_review_digests_present": all(row.get("per_ticker_label_objective_redesign_candidate_review_digest") for row in entries),
        "provider_requests_made_false": package.get("provider_requests_made_in_review") is False,
        "market_data_acquisition_false": package.get("market_data_acquisition_performed_in_review") is False,
        "dataset_regeneration_false": package.get("canonical_dataset_regenerated_in_review") is False,
        "redesigned_label_regeneration_false": package.get("redesigned_label_regeneration_performed") is False,
        "feature_regeneration_false": package.get("feature_regeneration_performed") is False,
        "predictive_evidence_rerun_false": package.get("predictive_evidence_execution_rerun_performed") is False,
        "label_objective_review_execution_rerun_false": package.get("label_objective_target_definition_review_execution_rerun_performed") is False,
        "metric_recomputation_in_review_false": package.get("metric_recomputation_performed_in_review") is False,
        "model_training_in_review_false": package.get("model_training_performed_in_review") is False,
        "raw_provider_payloads_not_committed": package.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": package.get("api_keys_stored_or_printed") is False,
        "no_predictive_usefulness_acceptance_artifact_created": package.get("predictive_usefulness_acceptance_artifact_created") is False,
        "no_profitability_acceptance_created": package.get("profitability_acceptance_created") is False,
        "no_runtime_migration_approval_created": package.get("runtime_migration_approval_created") is False,
        "next_chain_reviewed": package.get("next_chain") == NEXT_CHAIN,
        "next_gates_reviewed": package.get("next_gates") == NEXT_GATES,
        "risk_controls_reviewed": package.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files") is True,
    }
    return [_check(check_id, facts[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == "PASS" for row in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed,
        "failed_checks": len(checklist) - passed,
        "blocker_count": sum(row["status"] == "FAIL" for row in checklist),
        "ready_for_operator_assessment": True, "ready_for_label_objective_redesign_approval": False,
        "recommended_redesign_direction": RECOMMENDED_REDESIGN_DIRECTION,
        "recommended_redesign_direction_selected_for_approval": False,
        "label_objective_redesign_approved": False, "label_objective_redesign_executed": False,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def build_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    source = _source_candidate(candidate)
    package = _base_package(source)
    package["review_checklist"] = _checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    package["label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"] = (
        label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest_v1(package)
    )
    validate_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(package)
    return package


def _validate_reviewed_structures(package: Mapping[str, Any]) -> None:
    themes = package.get("reviewed_redesign_themes")
    if not isinstance(themes, list) or [row.get("theme") for row in themes] != REDESIGN_THEME_IDS:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("reviewed redesign themes mismatch")
    for row in themes:
        _expect(row.get("theme_status"), "PLANNED_NOT_EXECUTED", "theme status")
        _expect_true(row.get("approval_required_before_execution"), "theme approval required")
        for field in ("execution_authorized", "execution_performed", "label_regeneration_authorized", "target_definition_change_authorized"):
            _expect_false(row.get(field), f"theme {field}")
        _expect_true(row.get("research_only"), "theme research only")
        _expect_true(row.get("non_actionable"), "theme non actionable")
    options = package.get("reviewed_redesign_options")
    if not isinstance(options, list) or [row.get("option") for row in options] != REDESIGN_OPTION_IDS:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("reviewed redesign options mismatch")
    for row in options:
        _expect(row.get("option_status"), "AVAILABLE_FOR_OPERATOR_REVIEW", "option status")
        for field in ("selected", "approved", "executed", "creates_new_labels", "creates_new_targets", "label_regeneration_authorized", "target_definition_change_authorized"):
            _expect_false(row.get(field), f"option {field}")
        _expect_true(row.get("research_only"), "option research only")
        _expect_true(row.get("non_actionable"), "option non actionable")
    families = package.get("reviewed_label_family_impact_review")
    if not isinstance(families, list) or [row.get("label_family") for row in families] != LABEL_FAMILIES:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("reviewed label family impact mismatch")
    for row in families:
        _expect(row.get("impact_review_status"), "PLANNED_NOT_EXECUTED", "family review status")
        _expect(row.get("possible_redesign_impact"), "TO_BE_REVIEWED", "family impact")
        _expect_false(row.get("label_regeneration_authorized"), "family label regeneration")
        _expect_false(row.get("target_definition_change_authorized"), "family target change")
        _expect_true(row.get("research_only"), "family research only")
        _expect_true(row.get("non_actionable"), "family non actionable")
    questions = package.get("reviewed_redesign_questions")
    if not isinstance(questions, list) or [row.get("question") for row in questions] != REDESIGN_QUESTIONS:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("reviewed redesign questions mismatch")
    for row in questions:
        _expect(row.get("question_status"), "NOT_ANSWERED", "question status")
        _expect_true(row.get("requires_separate_review_or_execution"), "question separate review")
        _expect_true(row.get("research_only"), "question research only")
        _expect_true(row.get("non_actionable"), "question non actionable")
    outputs = package.get("reviewed_planned_outputs")
    if not isinstance(outputs, list) or [row.get("output_name") for row in outputs] != PLANNED_OUTPUT_NAMES:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("reviewed planned outputs mismatch")
    for row in outputs:
        _expect(row.get("output_status"), "PLANNED_NOT_GENERATED", "planned output status")
        _expect(row.get("output_scope"), "RESEARCH_ONLY_NON_ACTIONABLE", "planned output scope")


def validate_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(
    review_package: dict,
) -> dict:
    if not isinstance(review_package, dict):
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("review_package must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1,
        "review_status": LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "source_candidate_artifact_kind": SOURCE_CANDIDATE_ARTIFACT_KIND,
        "source_candidate_status": SOURCE_CANDIDATE_STATUS, "source_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "source_candidate_checklist_total": 69, "source_candidate_checklist_passed": 69,
        "source_candidate_checklist_failed": 0, "source_candidate_blocker_count": 0,
        "label_objective_redesign_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **SOURCE_EVIDENCE,
        "dataset_name": "expanded_universe_canonical_dataset_v1", "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d", "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "meta_record_count": 913, "non_meta_record_count": 1003,
        "records_digest": SOURCE_EVIDENCE["records_digest"], "reviewed_candidate_basis": CANDIDATE_BASIS,
        "reviewed_label_objective_redesign_candidate_objective": "PREPARE_OPTIONAL_LABEL_OBJECTIVE_REDESIGN_PATH_AFTER_RESULTS_REVIEW_FOUND_MAJORITY_STRUCTURE_AND_WEAK_EDGE",
        "reviewed_label_objective_redesign_candidate_scope": "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION",
        "reviewed_label_objective_redesign_candidate_mode": "PLANNED_NOT_EXECUTED",
        "reviewed_label_objective_redesign_candidate_authority_status": NOT_AUTHORIZED,
        "recommended_redesign_direction": RECOMMENDED_REDESIGN_DIRECTION,
        "recommended_redesign_direction_rationale": RECOMMENDATION_RATIONALE,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    for field in TRUE_FIELDS:
        _expect_true(review_package.get(field), field)
    for field in FALSE_FIELDS:
        _expect_false(review_package.get(field), field)
    _validate_reviewed_structures(review_package)
    entries = review_package.get("per_ticker_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("per-ticker review entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("registry_approval_status"), "APPROVED_FOR_RESEARCH_REGISTRY_ONLY", f"{ticker} registry status")
        _expect(entry.get("canonical_dataset_status"), "FROZEN", f"{ticker} dataset status")
        _expect(entry.get("label_objective_target_definition_results_review_status"), "REVIEWED_RESEARCH_ONLY", f"{ticker} results review status")
        _expect(entry.get("label_objective_redesign_candidate_status"), "PLANNED_READY_FOR_OPERATOR_REVIEW", f"{ticker} candidate status")
        _expect(entry.get("label_objective_redesign_candidate_review_status"), "READY_FOR_OPERATOR_ASSESSMENT", f"{ticker} review status")
        _expect(entry.get("source_label_objective_redesign_candidate_digest"), EXPECTED_CANDIDATE_DIGEST, f"{ticker} candidate digest")
        for field in ("label_objective_redesign_approved", "label_objective_redesign_executed", "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created", "target_definition_change_authorized", "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created"):
            _expect_false(entry.get(field), f"{ticker} {field}")
        _expect(entry.get("predictive_usefulness"), NOT_ACCEPTED, f"{ticker} usefulness")
        _expect(entry.get("profitability"), NOT_ACCEPTED, f"{ticker} profitability")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        candidate_digest = entry.get("per_ticker_label_objective_redesign_candidate_digest")
        if not isinstance(candidate_digest, str) or len(candidate_digest) != 64:
            raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError(f"{ticker} candidate digest missing")
        review_digest = entry.get("per_ticker_label_objective_redesign_candidate_review_digest")
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError(f"{ticker} review digest missing")
        _expect(review_digest, per_ticker_label_objective_redesign_candidate_using_redesigned_evidence_review_digest_v1(entry), f"{ticker} review digest")
        if ticker == "META":
            _expect(entry.get("candidate_note"), "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_REDESIGN_CANDIDATE", "META note")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != CHECK_IDS:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("review checklist mismatch")
    _expect(checklist, _checklist(review_package), "review checklist")
    if any(row.get("status") != "PASS" for row in checklist):
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("review checklist failed")
    _expect(review_package.get("review_summary"), _summary(checklist), "review summary")
    digest = review_package.get("label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("review digest missing")
    _expect(digest, label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest_v1(review_package), "review digest")
    return {
        "validation_status": LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID,
        "review_digest": digest, **{key: review_package["review_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_label_objective_redesign_candidate_using_redesigned_evidence_review_markdown_v1(
    review_package: dict,
) -> str:
    validate_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(review_package)
    sections = [
        ("Title", "Optional Label Objective Redesign Candidate Review Using Redesigned Evidence v1."),
        ("Optional Label Objective Redesign Candidate Review Using Redesigned Evidence", review_package["review_status"]),
        ("Reviewed Candidate", f"{review_package['source_candidate_digest']}; 69/69 checks and zero blockers."),
        ("Source Results Review", review_package["label_objective_target_definition_results_review_using_redesigned_evidence_digest"]),
        ("Bound Evidence", "All candidate, review-chain, predictive, matrix, feature, label, registry, and records digests are bound."),
        ("Dataset and Universe", f"{review_package['dataset_name']}; {', '.join(review_package['target_universe'])}; META=913."),
        ("Reviewed Candidate Basis", str(review_package["reviewed_candidate_basis"])),
        ("Reviewed Candidate Objective", review_package["reviewed_label_objective_redesign_candidate_objective"]),
        ("Reviewed Redesign Themes", "\n".join(f"- {row['theme']}" for row in review_package["reviewed_redesign_themes"])),
        ("Reviewed Redesign Options", "\n".join(f"- {row['option']} (selected: false)" for row in review_package["reviewed_redesign_options"])),
        ("Reviewed Label Family Impact Review", "\n".join(f"- {row['label_family']}" for row in review_package["reviewed_label_family_impact_review"])),
        ("Reviewed Redesign Questions", "\n".join(f"- {row['question']}" for row in review_package["reviewed_redesign_questions"])),
        ("Reviewed Planned Outputs", "\n".join(f"- {row['output_name']}: {row['output_status']}" for row in review_package["reviewed_planned_outputs"])),
        ("Per-Ticker Review Entries", "\n".join(f"- {row['ticker']}: {row['historical_record_count']} records" for row in review_package["per_ticker_review_entries"])),
        ("Next Chain", "\n".join(f"{index}. {item}" for index, item in enumerate(review_package["next_chain"], 1))),
        ("Next Gates", "\n".join(f"- {item}" for item in review_package["next_gates"])),
        ("Risk Controls", "\n".join(f"- {item}" for item in review_package["risk_controls"])),
        ("Predictive Usefulness Boundary", "Predictive usefulness remains not accepted."),
        ("Profitability Boundary", "Profitability remains not accepted."),
        ("Runtime Boundary", "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."),
        ("Checklist Summary", f"{review_package['review_summary']['passed_checks']}/{review_package['review_summary']['total_checks']} passed; zero blockers."),
        ("Guardrails", "Review only: no selection, approval, execution, regeneration, target creation, provider, runtime, or trading action."),
    ]
    lines = ["# Optional Label Objective Redesign Candidate Review Using Redesigned Evidence", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", body, ""])
    return "\n".join(lines)


def write_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict:
    package = build_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(candidate)
    validation = validate_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "label_objective_redesign_candidate_using_redesigned_evidence_review_v1.json"
    payload = canonical_json_bytes(package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError("review output already exists") from exc
    return {
        "path": str(path).replace("\\", "/"), "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"], "review_digest": validation["review_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
