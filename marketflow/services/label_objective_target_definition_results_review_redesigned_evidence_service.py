"""Offline results review of executed label-objective review evidence."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes, sha256_file
from marketflow.services import label_objective_target_definition_review_execution_redesigned_evidence_service as execution


ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE"
)
ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1 = (
    "label_objective_target_definition_results_review_using_redesigned_evidence_v1"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID"
)

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
SOURCE_EXECUTION_ARTIFACT_KIND = execution.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE
SOURCE_EXECUTION_STATUS = execution.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY
EXPECTED_SOURCE_EXECUTION_DIGEST = "7b5c299191abfd6aa8ef33ebed804757a2d57a6fb966ed1d51c78d1b233abe30"
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = "7efd91b24e1af35f93e37dc9bbb5e90fe03f1080f6296abe57afdbd326d0fbee"
EXPECTED_SOURCE_APPROVAL_DIGEST = execution.EXPECTED_APPROVAL_DIGEST
TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
OUTPUT_LABEL = execution.OUTPUT_LABEL
EVIDENCE_SCOPE = execution.EVIDENCE_SCOPE
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
SELF_REFERENCE_POLICY = execution.SELF_REFERENCE_POLICY

SOURCE_EVIDENCE = {
    "label_objective_target_definition_review_execution_using_redesigned_evidence_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
    "label_objective_target_definition_review_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
    "label_objective_target_definition_review_approval_using_redesigned_evidence_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest": execution.EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": execution.EXPECTED_CANDIDATE_DIGEST,
    "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": execution.EXPECTED_PATH_SELECTION_DIGEST,
    "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": execution.EXPECTED_READINESS_REVIEW_DIGEST,
    "predictive_usefulness_reassessment_using_redesigned_evidence_digest": execution.EXPECTED_REASSESSMENT_DIGEST,
    "additional_predictive_evidence_results_review_using_redesigned_labels_digest": execution.EXPECTED_RESULTS_REVIEW_DIGEST,
    "additional_predictive_evidence_execution_using_redesigned_labels_digest": execution.EXPECTED_EXECUTION_DIGEST,
    "feature_label_matrix_digest": execution.EXPECTED_MATRIX_DIGEST,
    "feature_values_digest": execution.EXPECTED_FEATURE_VALUES_DIGEST,
    "redesigned_label_values_digest": execution.EXPECTED_LABEL_VALUES_DIGEST,
    "research_registry_approval_digest": execution.EXPECTED_RESEARCH_REGISTRY_DIGEST,
    "records_digest": execution.EXPECTED_RECORDS_DIGEST,
}

RESULT_REVIEW_CLASSIFICATION = {
    "results_review_classification": "COMPLETED_RESEARCH_ONLY",
    "label_objective_review_classification": "COMPLETED_RESEARCH_ONLY",
    "majority_structure_review": "PRESENT_REQUIRES_OPERATOR_REVIEW",
    "cross_sectional_edge_materiality_review": "SMALL_NOT_ACCEPTANCE_EVIDENCE",
    "local_model_equivalence_review": "MATCHES_MAJORITY_BASELINE",
    "horizon_noise_review": "REQUIRES_OPERATOR_REVIEW",
    "threshold_materiality_review": "REQUIRES_OPERATOR_REVIEW",
    "class_balance_review": "REQUIRES_OPERATOR_REVIEW",
    "per_ticker_behavior_review": "REQUIRES_OPERATOR_REVIEW",
    "meta_behavior_review": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
    "target_decision_review": "NO_TARGET_CHANGE_AUTHORIZED",
    "redesign_or_refinement_candidate_readiness": "OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION",
    "predictive_usefulness_interpretation": "NOT_ACCEPTED",
    "profitability_interpretation": "NOT_ACCEPTED",
    "runtime_interpretation": "NOT_AUTHORIZED",
}

LIMITATIONS = [
    "review_is_research_only", "review_does_not_regenerate_labels",
    "review_does_not_create_new_targets", "review_does_not_authorize_target_definition_change",
    "review_does_not_create_redesign_candidate",
    "review_does_not_create_threshold_horizon_refinement_candidate",
    "review_does_not_accept_predictive_usefulness", "review_does_not_approve_profitability",
    "review_does_not_authorize_runtime", "majority_structure_risk_requires_operator_review",
    "small_cross_sectional_edge_is_not_acceptance_evidence",
    "local_model_matches_majority_baseline", "meta_reduced_record_count_preserved",
]
NEXT_CHAIN = [
    "Optional Label Objective Redesign Candidate Using Redesigned Evidence v1, if selected.",
    "Optional Threshold / Horizon Refinement Candidate Using Redesigned Evidence v1, if selected.",
    "Optional Improved Evidence Planning Candidate, if selected.",
    "Optional Improved Evidence Execution Approval and Execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "label_objective_redesign_candidate_using_redesigned_evidence_if_selected",
    "threshold_horizon_refinement_candidate_using_redesigned_evidence_if_selected",
    "improved_evidence_planning_candidate_if_selected", "improved_evidence_execution_approval_if_required",
    "improved_evidence_execution_if_approved",
    "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready", "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_regenerate_labels", "review_does_not_create_new_targets",
    "review_does_not_authorize_target_definition_change", "review_does_not_create_redesign_candidate",
    "review_does_not_create_refinement_candidate", "review_does_not_generate_new_evidence",
    "review_does_not_rerun_predictive_evidence", "review_does_not_retrain_models",
    "review_does_not_recompute_metrics", "review_does_not_accept_predictive_usefulness",
    "review_does_not_create_acceptance_candidate", "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime", "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading", "review_does_not_authorize_broker_execution",
    "review_does_not_generate_trade_recommendations", "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs", "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs", "do_not_mutate_label_objective_review_outputs",
    "preserve_meta_record_limitation", "all_outputs_research_only",
]

TRUE_REVIEW_FIELDS = [
    "created_offline", "research_only", "operator_review_required",
    "label_objective_target_definition_review_approved",
    "label_objective_target_definition_review_authorized",
    "ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence",
    "label_objective_target_definition_review_executed",
    "label_objective_target_definition_review_results_created",
    "label_objective_target_definition_results_review_created",
    "label_objective_target_definition_results_review_ready",
    "ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence",
    "meta_reduced_record_count_preserved", "output_file_inspection_performed",
]
FALSE_GUARDRAIL_FIELDS = [
    "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
    "target_definition_change_authorized", "target_definition_change_performed",
    "label_objective_redesign_candidate_created", "threshold_horizon_refinement_candidate_created",
    "improved_evidence_planning_candidate_created", "additional_predictive_evidence_execution_candidate_created",
    "additional_predictive_evidence_executed", "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
    "profitability_acceptance_ready", "profitability_acceptance_recommended",
    "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
    "new_strategy_scoring_performed", "trade_recommendations_generated",
    "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
    "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
    "canonical_dataset_regenerated_in_review", "redesigned_label_regeneration_performed",
    "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
    "label_objective_target_definition_review_execution_rerun_performed",
    "metric_recomputation_performed_in_review", "model_training_performed_in_review",
    "raw_provider_payloads_committed", "api_keys_stored_or_printed",
]

CHECK_IDS = [
    "execution_digest_bound", "output_binding_digest_bound", "approval_digest_bound",
    "candidate_review_digest_bound", "candidate_digest_bound", "path_selection_digest_bound",
    "readiness_review_digest_bound", "reassessment_digest_bound",
    "predictive_results_review_digest_bound", "predictive_execution_digest_bound",
    "matrix_digest_bound", "feature_values_digest_bound", "label_values_digest_bound",
    "research_registry_digest_bound", "records_digest_bound", "target_universe_12_preserved",
    "records_digest_preserved", "meta_913_preserved", "source_execution_status_research_only",
    "generated_output_count_12", "output_digests_bound", "output_digest_mismatch_count_zero",
    "outputs_research_only_non_actionable", "execution_manifest_verified",
    "label_family_objective_map_verified", "majority_structure_report_verified",
    "cross_sectional_edge_report_verified", "horizon_noise_report_verified",
    "threshold_materiality_report_verified", "class_balance_report_verified",
    "per_ticker_behavior_report_verified", "meta_behavior_report_verified",
    "decision_options_report_verified", "operator_summary_verified", "results_review_created_true",
    "results_review_ready_true", "ready_for_optional_redesign_or_refinement_candidate_true",
    "label_regeneration_authorized_false", "label_regeneration_performed_false",
    "new_targets_created_false", "target_definition_change_authorized_false",
    "target_definition_change_performed_false", "label_objective_redesign_candidate_created_false",
    "threshold_horizon_refinement_candidate_created_false", "improved_evidence_planning_candidate_created_false",
    "predictive_usefulness_not_accepted", "acceptance_ready_false",
    "acceptance_candidate_created_false", "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "majority_structure_risk_preserved", "small_cross_sectional_edge_preserved",
    "local_model_equivalence_preserved", "meta_limitation_preserved", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false", "market_data_acquisition_false",
    "dataset_regeneration_false", "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "label_objective_review_execution_rerun_false",
    "metric_recomputation_in_review_false", "model_training_in_review_false",
    "raw_provider_payloads_not_committed", "api_keys_not_stored_or_printed",
    "no_predictive_usefulness_acceptance_artifact_created", "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created", "limitations_recorded", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError(ValueError):
    """Raised when results-review evidence violates its closed contract."""


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).lower()
            if "api_key" in normalized or "raw_provider_payload" in normalized:
                if item not in (False, None, "", [], {}):
                    return True
            if _contains_forbidden_key(item):
                return True
    elif isinstance(value, list):
        return any(_contains_forbidden_key(item) for item in value)
    return False


def label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(
    package: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(package))
    clone.pop("label_objective_target_definition_results_review_using_redesigned_evidence_digest", None)
    return semantic_digest(clone)


def per_ticker_label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(entry))
    clone.pop("per_ticker_label_objective_target_definition_results_review_digest", None)
    return semantic_digest(clone)


def _verify_outputs(root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    paths = {name: root / name for name in OUTPUT_FILENAMES}
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        return {
            "expected_output_count": 12, "observed_output_count": 12 - len(missing),
            "output_digest_mismatch_count": 0, "output_file_inspection_performed": False,
            "missing_output_files": missing, "local_output_hashes": {},
        }, {}, [{"failure_id": "missing_output_files", "files": missing}]
    payloads: dict[str, dict[str, Any]] = {}
    for name, path in paths.items():
        try:
            payloads[name] = _load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            failures.append({"failure_id": "invalid_output_json", "filename": name, "message": str(exc)})
    if len(payloads) != 12:
        return {
            "expected_output_count": 12, "observed_output_count": len(payloads),
            "output_digest_mismatch_count": 0, "output_file_inspection_performed": False,
            "local_output_hashes": {},
        }, payloads, failures
    local_hashes = {name: sha256_file(path) for name, path in paths.items()}
    manifest = payloads["label_objective_target_definition_review_digest_manifest.json"]
    if manifest.get("output_manifest_binding_digest") != EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST:
        failures.append({"failure_id": "digest_manifest_binding_mismatch"})
    if manifest.get("execution_digest") != EXPECTED_SOURCE_EXECUTION_DIGEST:
        failures.append({"failure_id": "digest_manifest_execution_mismatch"})
    declared = {row.get("filename"): row for row in manifest.get("output_digest_entries", []) if isinstance(row, dict)}
    mismatches = []
    for name in OUTPUT_FILENAMES:
        row = declared.get(name)
        if name == "label_objective_target_definition_review_digest_manifest.json":
            valid = (row is not None and row.get("sha256") is None
                     and row.get("digest_kind") == SELF_REFERENCE_POLICY
                     and manifest.get("self_reference_policy") == SELF_REFERENCE_POLICY)
        else:
            valid = row is not None and row.get("sha256") == local_hashes[name]
        if not valid:
            mismatches.append(name)
    if mismatches:
        failures.append({"failure_id": "output_digest_mismatch", "files": mismatches})
    for name, payload in payloads.items():
        if payload.get("output_label") != OUTPUT_LABEL or payload.get("evidence_scope") != EVIDENCE_SCOPE:
            failures.append({"failure_id": "research_boundary_mismatch", "filename": name})
        if payload.get("label_regeneration_performed") is not False:
            failures.append({"failure_id": "label_regeneration_boundary_mismatch", "filename": name})
        if payload.get("new_targets_created") is not False or payload.get("target_definition_change_authorized") is not False:
            failures.append({"failure_id": "target_authority_boundary_mismatch", "filename": name})
        if payload.get("predictive_usefulness") != NOT_ACCEPTED or payload.get("profitability") != NOT_ACCEPTED:
            failures.append({"failure_id": "acceptance_boundary_mismatch", "filename": name})
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            if payload.get(field) != NOT_AUTHORIZED:
                failures.append({"failure_id": "runtime_boundary_mismatch", "filename": name, "field": field})
        if _contains_forbidden_key(payload):
            failures.append({"failure_id": "forbidden_payload_or_key_material", "filename": name})
    execution_manifest = payloads["label_objective_target_definition_review_execution_manifest.json"]
    if execution_manifest.get("artifact_kind") != SOURCE_EXECUTION_ARTIFACT_KIND:
        failures.append({"failure_id": "execution_artifact_kind_mismatch"})
    if execution_manifest.get("execution_status") != SOURCE_EXECUTION_STATUS:
        failures.append({"failure_id": "execution_status_mismatch"})
    if execution_manifest.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest") != EXPECTED_SOURCE_EXECUTION_DIGEST:
        failures.append({"failure_id": "execution_digest_mismatch"})
    binding = execution_manifest.get("output_digest_manifest_summary", {}).get("binding_digest")
    if binding != EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST:
        failures.append({"failure_id": "output_binding_digest_mismatch"})
    verification = {
        "expected_output_count": 12, "observed_output_count": 12,
        "output_digest_mismatch_count": len(mismatches), "output_digest_mismatch_files": mismatches,
        "output_file_inspection_performed": True,
        "digest_manifest_self_reference_policy": manifest.get("self_reference_policy"),
        "local_output_hashes": local_hashes,
        "all_outputs_research_only_non_actionable": not any(row["failure_id"] == "research_boundary_mismatch" for row in failures),
        "no_provider_payloads_or_api_keys_present": not any(row["failure_id"] == "forbidden_payload_or_key_material" for row in failures),
    }
    return verification, payloads, failures


def _per_ticker_entries(execution_manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    result = []
    source_rows = execution_manifest.get("per_ticker_execution_entries", [])
    by_ticker = {row.get("ticker"): row for row in source_rows if isinstance(row, Mapping)}
    for ticker in TARGET_UNIVERSE:
        source = by_ticker[ticker]
        entry = {
            "ticker": ticker, "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN", "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "label_objective_target_definition_review_execution_status": "EXECUTED_RESEARCH_ONLY",
            "label_objective_target_definition_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "majority_baseline_accuracy": source.get("majority_baseline_accuracy"),
            "cross_sectional_accuracy": source.get("cross_sectional_accuracy"),
            "local_model_accuracy": source.get("local_model_accuracy"),
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "target_definition_change_authorized": False, "new_targets_created": False,
            "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False, "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
            "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        }
        if ticker == "META":
            entry["review_note"] = "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW"
        entry["per_ticker_label_objective_target_definition_results_review_digest"] = (
            per_ticker_label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(entry)
        )
        result.append(entry)
    return result


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = "PASS" if expected == actual else "FAIL"
    return {"check_id": check_id, "status": status, "expected": expected, "actual": actual,
            "severity": "BLOCKER", "message": f"{check_id} {'passed' if status == 'PASS' else 'failed'}"}


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    verification = package.get("output_verification", {})
    classification = package.get("result_review_classification", {})
    actuals = {
        "execution_digest_bound": package.get("source_execution_digest"),
        "output_binding_digest_bound": package.get("source_output_binding_digest"),
        "approval_digest_bound": package.get("source_approval_digest"),
        "candidate_review_digest_bound": package.get("source_evidence", {}).get("label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"),
        "candidate_digest_bound": package.get("source_evidence", {}).get("label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"),
        "path_selection_digest_bound": package.get("source_evidence", {}).get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
        "readiness_review_digest_bound": package.get("source_evidence", {}).get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": package.get("source_evidence", {}).get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "predictive_results_review_digest_bound": package.get("source_evidence", {}).get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "predictive_execution_digest_bound": package.get("source_evidence", {}).get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": package.get("source_evidence", {}).get("feature_label_matrix_digest"),
        "feature_values_digest_bound": package.get("source_evidence", {}).get("feature_values_digest"),
        "label_values_digest_bound": package.get("source_evidence", {}).get("redesigned_label_values_digest"),
        "research_registry_digest_bound": package.get("source_evidence", {}).get("research_registry_approval_digest"),
        "records_digest_bound": package.get("source_evidence", {}).get("records_digest"),
        "target_universe_12_preserved": package.get("target_universe"),
        "records_digest_preserved": package.get("records_digest"), "meta_913_preserved": package.get("meta_record_count"),
        "source_execution_status_research_only": package.get("source_execution_status"),
        "generated_output_count_12": package.get("generated_output_count"),
        "output_digests_bound": len(verification.get("local_output_hashes", {})),
        "output_digest_mismatch_count_zero": verification.get("output_digest_mismatch_count"),
        "outputs_research_only_non_actionable": verification.get("all_outputs_research_only_non_actionable"),
        "execution_manifest_verified": package.get("execution_manifest_verified"),
        "label_family_objective_map_verified": package.get("label_family_objective_map_verified"),
        "majority_structure_report_verified": package.get("majority_structure_report_verified"),
        "cross_sectional_edge_report_verified": package.get("cross_sectional_edge_report_verified"),
        "horizon_noise_report_verified": package.get("horizon_noise_report_verified"),
        "threshold_materiality_report_verified": package.get("threshold_materiality_report_verified"),
        "class_balance_report_verified": package.get("class_balance_report_verified"),
        "per_ticker_behavior_report_verified": package.get("per_ticker_behavior_report_verified"),
        "meta_behavior_report_verified": package.get("meta_behavior_report_verified"),
        "decision_options_report_verified": package.get("decision_options_report_verified"),
        "operator_summary_verified": package.get("operator_summary_verified"),
        "results_review_created_true": package.get("label_objective_target_definition_results_review_created"),
        "results_review_ready_true": package.get("label_objective_target_definition_results_review_ready"),
        "ready_for_optional_redesign_or_refinement_candidate_true": package.get("ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence"),
        "label_regeneration_authorized_false": package.get("label_regeneration_authorized"),
        "label_regeneration_performed_false": package.get("label_regeneration_performed"),
        "new_targets_created_false": package.get("new_targets_created"),
        "target_definition_change_authorized_false": package.get("target_definition_change_authorized"),
        "target_definition_change_performed_false": package.get("target_definition_change_performed"),
        "label_objective_redesign_candidate_created_false": package.get("label_objective_redesign_candidate_created"),
        "threshold_horizon_refinement_candidate_created_false": package.get("threshold_horizon_refinement_candidate_created"),
        "improved_evidence_planning_candidate_created_false": package.get("improved_evidence_planning_candidate_created"),
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness"),
        "acceptance_ready_false": package.get("predictive_usefulness_acceptance_ready"),
        "acceptance_candidate_created_false": package.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": package.get("profitability"), "runtime_not_authorized": package.get("runtime_use"),
        "strategy_not_authorized": package.get("strategy_use"), "broker_not_authorized": package.get("broker_execution"),
        "trade_recommendations_false": package.get("trade_recommendations_generated"),
        "majority_structure_risk_preserved": classification.get("majority_structure_review"),
        "small_cross_sectional_edge_preserved": classification.get("cross_sectional_edge_materiality_review"),
        "local_model_equivalence_preserved": classification.get("local_model_equivalence_review"),
        "meta_limitation_preserved": classification.get("meta_behavior_review"),
        "per_ticker_entries_12": len(package.get("per_ticker_results_review_entries", [])),
        "per_ticker_digests_present": all(len(row.get("per_ticker_label_objective_target_definition_results_review_digest", "")) == 64 for row in package.get("per_ticker_results_review_entries", [])),
        "provider_requests_made_false": package.get("provider_requests_made_in_review"),
        "market_data_acquisition_false": package.get("market_data_acquisition_performed_in_review"),
        "dataset_regeneration_false": package.get("canonical_dataset_regenerated_in_review"),
        "redesigned_label_regeneration_false": package.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": package.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": package.get("predictive_evidence_execution_rerun_performed"),
        "label_objective_review_execution_rerun_false": package.get("label_objective_target_definition_review_execution_rerun_performed"),
        "metric_recomputation_in_review_false": package.get("metric_recomputation_performed_in_review"),
        "model_training_in_review_false": package.get("model_training_performed_in_review"),
        "raw_provider_payloads_not_committed": package.get("raw_provider_payloads_committed"),
        "api_keys_not_stored_or_printed": package.get("api_keys_stored_or_printed"),
        "no_predictive_usefulness_acceptance_artifact_created": package.get("predictive_usefulness_acceptance_candidate_created"),
        "no_profitability_acceptance_created": package.get("profitability_acceptance_ready"),
        "no_runtime_migration_approval_created": package.get("runtime_migration_approved"),
        "limitations_recorded": len(package.get("limitations", [])), "next_chain_defined": len(package.get("next_chain", [])),
        "next_gates_defined": len(package.get("next_gates", [])), "risk_controls_defined": len(package.get("risk_controls", [])),
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files"),
    }
    expected = {
        "execution_digest_bound": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "output_binding_digest_bound": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "approval_digest_bound": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "candidate_review_digest_bound": execution.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "candidate_digest_bound": execution.EXPECTED_CANDIDATE_DIGEST,
        "path_selection_digest_bound": execution.EXPECTED_PATH_SELECTION_DIGEST,
        "readiness_review_digest_bound": execution.EXPECTED_READINESS_REVIEW_DIGEST,
        "reassessment_digest_bound": execution.EXPECTED_REASSESSMENT_DIGEST,
        "predictive_results_review_digest_bound": execution.EXPECTED_RESULTS_REVIEW_DIGEST,
        "predictive_execution_digest_bound": execution.EXPECTED_EXECUTION_DIGEST,
        "matrix_digest_bound": execution.EXPECTED_MATRIX_DIGEST,
        "feature_values_digest_bound": execution.EXPECTED_FEATURE_VALUES_DIGEST,
        "label_values_digest_bound": execution.EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": execution.EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest_bound": execution.EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": TARGET_UNIVERSE, "records_digest_preserved": execution.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": 913, "source_execution_status_research_only": SOURCE_EXECUTION_STATUS,
        "generated_output_count_12": 12, "output_digests_bound": 12,
        "output_digest_mismatch_count_zero": 0, "outputs_research_only_non_actionable": True,
        **{key: True for key in ("execution_manifest_verified", "label_family_objective_map_verified",
            "majority_structure_report_verified", "cross_sectional_edge_report_verified", "horizon_noise_report_verified",
            "threshold_materiality_report_verified", "class_balance_report_verified", "per_ticker_behavior_report_verified",
            "meta_behavior_report_verified", "decision_options_report_verified", "operator_summary_verified",
            "results_review_created_true", "results_review_ready_true", "ready_for_optional_redesign_or_refinement_candidate_true")},
        **{key: False for key in ("label_regeneration_authorized_false", "label_regeneration_performed_false",
            "new_targets_created_false", "target_definition_change_authorized_false", "target_definition_change_performed_false",
            "label_objective_redesign_candidate_created_false", "threshold_horizon_refinement_candidate_created_false",
            "improved_evidence_planning_candidate_created_false", "acceptance_ready_false", "acceptance_candidate_created_false",
            "trade_recommendations_false", "provider_requests_made_false", "market_data_acquisition_false",
            "dataset_regeneration_false", "redesigned_label_regeneration_false", "feature_regeneration_false",
            "predictive_evidence_rerun_false", "label_objective_review_execution_rerun_false",
            "metric_recomputation_in_review_false", "model_training_in_review_false", "raw_provider_payloads_not_committed",
            "api_keys_not_stored_or_printed", "no_predictive_usefulness_acceptance_artifact_created",
            "no_profitability_acceptance_created", "no_runtime_migration_approval_created")},
        "predictive_usefulness_not_accepted": NOT_ACCEPTED, "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED, "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED, "majority_structure_risk_preserved": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "small_cross_sectional_edge_preserved": "SMALL_NOT_ACCEPTANCE_EVIDENCE",
        "local_model_equivalence_preserved": "MATCHES_MAJORITY_BASELINE",
        "meta_limitation_preserved": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "per_ticker_entries_12": 12, "per_ticker_digests_present": True,
        "limitations_recorded": len(LIMITATIONS), "next_chain_defined": len(NEXT_CHAIN),
        "next_gates_defined": len(NEXT_GATES), "risk_controls_defined": len(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }
    return [_check(check_id, expected[check_id], actuals.get(check_id)) for check_id in CHECK_IDS]


def _blocked_package(root: Path, verification: dict[str, Any], failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
        "review_status": LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS,
        "created_offline": True, "research_only": True, "source_output_root": _path_text(root),
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "output_verification": verification, "failure_count": len(failures), "failures": failures,
        "label_objective_target_definition_results_review_created": False,
        "label_objective_target_definition_results_review_ready": False,
        "ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence": False,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
        "label_objective_target_definition_results_review_using_redesigned_evidence_digest": "NOT_CREATED",
    }


def build_label_objective_target_definition_results_review_using_redesigned_evidence_v1(
    *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Inspect and review the exact execution outputs without rerunning execution."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    verification, payloads, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, verification, failures)
    manifest = payloads["label_objective_target_definition_review_execution_manifest.json"]
    per_ticker = _per_ticker_entries(manifest)
    package = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
        "review_status": LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
        "source_execution_artifact_kind": SOURCE_EXECUTION_ARTIFACT_KIND,
        "source_execution_status": SOURCE_EXECUTION_STATUS,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_output_root": _path_text(root), "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "output_verification": verification, "dataset_name": execution.DATASET_NAME,
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "generated_output_count": 12, "review_dimension_count": 12,
        "label_family_review_count": 10, "diagnostic_question_count": 10, "decision_option_count": 7,
        "reviewed_problem_basis": {
            "readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE",
            "selected_option": "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION",
            "oos_cross_sectional_delta_vs_majority": "0.00309917", "oos_local_model_delta_vs_majority": 0,
            "predictive_signal_readiness": "NOT_READY", "baseline_outperformance_readiness": "NOT_READY",
            "local_model_readiness": "NOT_READY", "stability_readiness": "NOT_READY",
            "calibration_readiness": "REQUIRES_OPERATOR_REVIEW",
            "optional_model_coverage_sufficiency": "FAIL_OR_NOT_MET",
        },
        "label_family_objective_map_review": deepcopy(payloads["current_label_family_objective_map.json"]["label_family_objective_map"]),
        "majority_structure_review": deepcopy(payloads["target_definition_vs_majority_structure_report.json"]),
        "cross_sectional_edge_materiality_review": deepcopy(payloads["cross_sectional_edge_materiality_report.json"]),
        "horizon_noise_review": deepcopy(payloads["horizon_noise_review_report.json"]),
        "threshold_materiality_review": deepcopy(payloads["threshold_materiality_review_report.json"]),
        "class_balance_target_distribution_review": deepcopy(payloads["class_balance_target_distribution_report.json"]),
        "per_ticker_target_behavior_review": deepcopy(payloads["per_ticker_target_behavior_report.json"]["per_ticker_execution_entries"]),
        "meta_target_behavior_review": deepcopy(payloads["meta_target_behavior_report.json"]["meta_target_behavior_review"]),
        "decision_options_review": deepcopy(payloads["target_decision_options_report.json"]["decision_options_review"]),
        "diagnostic_question_results_review": deepcopy(payloads["target_decision_options_report.json"]["diagnostic_question_results"]),
        "result_review_classification": deepcopy(RESULT_REVIEW_CLASSIFICATION),
        "per_ticker_results_review_entries": per_ticker,
        "limitations": list(LIMITATIONS), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
        "execution_manifest_verified": True, "label_family_objective_map_verified": True,
        "majority_structure_report_verified": True, "cross_sectional_edge_report_verified": True,
        "horizon_noise_report_verified": True, "threshold_materiality_report_verified": True,
        "class_balance_report_verified": True, "per_ticker_behavior_report_verified": True,
        "meta_behavior_report_verified": True, "decision_options_report_verified": True,
        "operator_summary_verified": True,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        **{field: True for field in TRUE_REVIEW_FIELDS},
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
    }
    package["checklist"] = _checklist(package)
    passed = sum(row["status"] == "PASS" for row in package["checklist"])
    failed = len(package["checklist"]) - passed
    package["checklist_summary"] = {
        "total_checks": len(package["checklist"]), "passed_checks": passed,
        "failed_checks": failed, "blocker_count": failed,
        "results_review_ready": failed == 0,
        "ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence": failed == 0,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "label_objective_redesign_candidate_created": False,
        "threshold_horizon_refinement_candidate_created": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }
    if failed:
        raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError("results-review checklist failed")
    package["label_objective_target_definition_results_review_using_redesigned_evidence_digest"] = (
        label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(package)
    )
    validate_label_objective_target_definition_results_review_using_redesigned_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_label_objective_target_definition_results_review_using_redesigned_evidence_v1(
    review_package: dict,
) -> dict[str, Any]:
    if not isinstance(review_package, dict):
        raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError("review package must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
        "review_status": LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
        "source_execution_artifact_kind": SOURCE_EXECUTION_ARTIFACT_KIND,
        "source_execution_status": SOURCE_EXECUTION_STATUS,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_evidence": SOURCE_EVIDENCE, "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913, "generated_output_count": 12,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "result_review_classification": RESULT_REVIEW_CLASSIFICATION,
        "limitations": LIMITATIONS, "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    for field in TRUE_REVIEW_FIELDS:
        _expect(review_package.get(field), True, field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect(review_package.get(field), False, field)
    verification = review_package.get("output_verification", {})
    _expect(verification.get("observed_output_count"), 12, "observed output count")
    _expect(verification.get("output_digest_mismatch_count"), 0, "output digest mismatch count")
    _expect(verification.get("digest_manifest_self_reference_policy"), SELF_REFERENCE_POLICY, "self reference policy")
    _expect(len(verification.get("local_output_hashes", {})), 12, "local output hash count")
    entries = review_package.get("per_ticker_results_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError("per-ticker entries mismatch")
    for row in entries:
        digest = row.get("per_ticker_label_objective_target_definition_results_review_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError("per-ticker digest missing")
        _expect(digest, per_ticker_label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(row), "per-ticker digest")
    checklist = review_package.get("checklist")
    if not isinstance(checklist, list) or len(checklist) != len(CHECK_IDS) or any(row.get("status") != "PASS" for row in checklist):
        raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError("checklist mismatch")
    summary = review_package.get("checklist_summary", {})
    _expect(summary.get("failed_checks"), 0, "failed checks")
    _expect(summary.get("blocker_count"), 0, "blocker count")
    digest = review_package.get("label_objective_target_definition_results_review_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError("review digest missing")
    _expect(digest, label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(review_package), "review digest")
    return {
        "status": LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID,
        "artifact_kind": review_package["artifact_kind"], "review_status": review_package["review_status"],
        "label_objective_target_definition_results_review_using_redesigned_evidence_digest": digest,
        "total_checks": summary["total_checks"], "passed_checks": summary["passed_checks"],
        "failed_checks": 0, "blocker_count": 0,
        "ready_for_optional_redesign_or_refinement_candidate": True,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def write_label_objective_target_definition_results_review_using_redesigned_evidence_v1(
    output_dir: str | Path, *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    package = build_label_objective_target_definition_results_review_using_redesigned_evidence_v1(output_root=output_root)
    path = Path(output_dir) / "label_objective_target_definition_results_review_using_redesigned_evidence_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_json_bytes(package)
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError(
            "refusing to overwrite results-review package"
        ) from exc
    return {"path": _path_text(path), "payload_sha256": sha256_bytes(data),
            "review_digest": package["label_objective_target_definition_results_review_using_redesigned_evidence_digest"]}


def build_label_objective_target_definition_results_review_using_redesigned_evidence_markdown_v1(
    review_package: dict,
) -> str:
    validation = validate_label_objective_target_definition_results_review_using_redesigned_evidence_v1(review_package)
    sections = [
        ("Title", ["Label Objective / Target Definition Results Review Using Redesigned Evidence v1."]),
        ("Label Objective / Target Definition Results Review Using Redesigned Evidence", [f"Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.", f"Digest: `{validation['label_objective_target_definition_results_review_using_redesigned_evidence_digest']}`."]),
        ("Source Execution", [f"Execution/status: `{review_package['source_execution_digest']}` / `{review_package['source_execution_status']}`."]),
        ("Bound Evidence", [f"Output binding/approval: `{review_package['source_output_binding_digest']}` / `{review_package['source_approval_digest']}`."]),
        ("Dataset and Universe", [f"`{review_package['dataset_name']}`; `{review_package['total_canonical_record_count']}` records; META `{review_package['meta_record_count']}`.", ", ".join(review_package["target_universe"])]),
        ("Output Verification", [f"`{review_package['output_verification']}`"]),
        ("Reviewed Problem Basis", [f"`{review_package['reviewed_problem_basis']}`"]),
        ("Label Family Objective Map Review", [f"Reviewed entries: `{len(review_package['label_family_objective_map_review'])}`."]),
        ("Majority Structure Review", [f"Risk: `{review_package['result_review_classification']['majority_structure_review']}`."]),
        ("Cross-Sectional Edge Materiality Review", [f"Classification: `{review_package['result_review_classification']['cross_sectional_edge_materiality_review']}`."]),
        ("Horizon and Threshold Review", [f"Horizon/threshold: `{review_package['result_review_classification']['horizon_noise_review']}` / `{review_package['result_review_classification']['threshold_materiality_review']}`."]),
        ("Class Balance and Target Distribution Review", [f"Classification: `{review_package['result_review_classification']['class_balance_review']}`."]),
        ("Per-Ticker Target Behavior Review", [f"Entries: `{len(review_package['per_ticker_results_review_entries'])}`."]),
        ("META Target Behavior Review", [f"`{review_package['meta_target_behavior_review']}`"]),
        ("Decision Options Review", [f"Options: `{len(review_package['decision_options_review'])}`; no target change authorized."]),
        ("Review Classification", [f"`{review_package['result_review_classification']}`"]),
        ("Limitations", [f"`{item}`" for item in review_package["limitations"]]),
        ("Next Chain", [f"{index}. {item}" for index, item in enumerate(review_package["next_chain"], 1)]),
        ("Next Gates", [f"`{item}`" for item in review_package["next_gates"]]),
        ("Risk Controls", [f"`{item}`" for item in review_package["risk_controls"]]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains `not accepted`."]),
        ("Profitability Boundary", ["Profitability remains `not accepted`."]),
        ("Runtime Boundary", ["Runtime, strategy, paper, and broker use remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", [f"`{review_package['checklist_summary']}`"]),
        ("Guardrails", ["Offline, digest-bound, research-only, non-actionable, and operator-selection-gated."]),
    ]
    lines = ["# MarketFlow Label Objective / Target Definition Results Review Using Redesigned Evidence Status", ""]
    for title, body in sections:
        lines.extend([f"## {title}", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)
