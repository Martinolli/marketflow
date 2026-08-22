"""Offline, digest-bound review of improved-evidence planning outputs."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes, sha256_file
from marketflow.services import improved_evidence_planning_execution_redesigned_evidence_service as execution


ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE = (
    "IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1 = (
    "improved_evidence_planning_results_review_using_redesigned_evidence_v1"
)
IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY = (
    "IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY"
)
IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS = (
    "IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS"
)
IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID = (
    "IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID"
)

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
DEFAULT_BRANCH = "feature/improved-evidence-planning-results-review-redesigned-evidence-v1"
DEFAULT_BASE_COMMIT = "108127be7d53b7435992c44550506729604cd0e1"
EXPECTED_EXECUTION_DIGEST = "1f2f04133a6b1d80dd30b5e8b4af08f1ae78aca8a164aa7a760a693192a894a4"
EXPECTED_OUTPUT_BINDING_DIGEST = "23edda5191badabced31ff152a60f2428ffa08730ebaa0ba8b2facfd2d87269c"
EXPECTED_APPROVAL_DIGEST = execution.EXPECTED_APPROVAL_DIGEST
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
SELECTED_DIRECTION = execution.SELECTED_DIRECTION
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

LIMITATIONS = [
    "review_is_research_only",
    "review_does_not_regenerate_labels",
    "review_does_not_create_new_targets",
    "review_does_not_authorize_target_definition_change",
    "review_does_not_generate_features",
    "review_does_not_create_feature_label_matrix",
    "review_does_not_create_additional_predictive_evidence_execution_candidate",
    "review_does_not_execute_predictive_evidence",
    "review_does_not_recompute_metrics",
    "review_does_not_train_models",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_approve_profitability",
    "review_does_not_authorize_runtime",
    "selected_direction_requires_operator_selection_before_any_future_evidence_candidate",
    "future_evidence_execution_requires_separate_candidate_review_and_approval",
    "meta_reduced_record_count_preserved",
]

NEXT_CHAIN = [
    "Optional Additional Predictive Evidence Execution Candidate Using Improved Evidence v1, if selected.",
    "Optional Additional Predictive Evidence Execution Candidate Operator Review v1.",
    "Optional Additional Predictive Evidence Execution Approval v1, if selected.",
    "Optional Additional Predictive Evidence Execution v1, if approved.",
    "Optional Additional Predictive Evidence Results Review v1.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_if_selected",
    "additional_predictive_evidence_execution_candidate_operator_review",
    "additional_predictive_evidence_execution_approval_if_selected",
    "additional_predictive_evidence_execution_if_approved",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "review_does_not_regenerate_labels", "review_does_not_create_new_targets",
    "review_does_not_authorize_target_definition_change", "review_does_not_generate_features",
    "review_does_not_create_feature_label_matrix",
    "review_does_not_create_additional_predictive_evidence_execution_candidate",
    "review_does_not_execute_predictive_evidence", "review_does_not_rerun_predictive_evidence",
    "review_does_not_retrain_models", "review_does_not_recompute_metrics",
    "review_does_not_accept_predictive_usefulness", "review_does_not_create_acceptance_candidate",
    "review_does_not_accept_profitability", "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy", "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution", "review_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset", "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs", "do_not_mutate_predictive_evidence_outputs",
    "do_not_mutate_label_objective_review_outputs", "do_not_mutate_label_objective_redesign_outputs",
    "do_not_mutate_improved_evidence_planning_outputs", "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "execution_digest_bound", "output_binding_digest_bound", "approval_digest_bound",
    "candidate_review_digest_bound", "candidate_digest_bound", "redesign_results_review_digest_bound",
    "redesign_execution_digest_bound", "redesign_output_binding_digest_bound",
    "target_definition_results_review_digest_bound", "target_definition_execution_digest_bound",
    "path_selection_digest_bound", "readiness_review_digest_bound", "reassessment_digest_bound",
    "predictive_results_review_digest_bound", "predictive_execution_digest_bound", "matrix_digest_bound",
    "feature_values_digest_bound", "label_values_digest_bound", "research_registry_digest_bound",
    "records_digest_bound", "target_universe_12_preserved", "records_digest_preserved",
    "meta_913_preserved", "source_execution_status_research_only", "selected_redesign_direction_preserved",
    "generated_output_count_14", "output_digests_bound", "output_digest_mismatch_count_zero",
    "outputs_research_only_non_actionable", "planning_execution_manifest_verified",
    "proposed_label_schema_report_verified", "no_trade_abstain_coverage_report_verified",
    "material_move_threshold_report_verified", "horizon_specific_validation_report_verified",
    "ticker_regime_split_validation_report_verified", "feature_label_alignment_report_verified",
    "chronological_split_embargo_report_verified", "baseline_model_comparison_plan_verified",
    "calibration_brier_plan_verified", "leakage_no_peek_control_plan_verified",
    "per_ticker_meta_reporting_plan_verified", "operator_summary_verified", "results_review_created_true",
    "results_review_ready_true", "ready_for_optional_additional_predictive_evidence_candidate_true",
    "label_regeneration_authorized_false", "label_regeneration_performed_false", "new_targets_created_false",
    "target_definition_change_authorized_false", "target_definition_change_performed_false",
    "feature_generation_authorized_false", "feature_generation_performed_false",
    "feature_label_matrix_created_false", "additional_predictive_evidence_execution_candidate_created_false",
    "additional_predictive_evidence_executed_false", "predictive_usefulness_not_accepted",
    "acceptance_ready_false", "acceptance_candidate_created_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "planning_scope_preserved", "selected_direction_reviewed",
    "future_evidence_candidate_readiness_recorded", "meta_limitation_preserved", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false", "market_data_acquisition_false",
    "dataset_regeneration_false", "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "improved_evidence_planning_execution_rerun_false",
    "metric_recomputation_in_review_false", "model_training_in_review_false",
    "raw_provider_payloads_not_committed", "api_keys_not_stored_or_printed",
    "no_predictive_usefulness_acceptance_artifact_created", "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created", "limitations_recorded", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError(ValueError):
    """Raised when saved planning outputs cannot support a valid review."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError(
            f"{path.name} is not readable JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError(
            f"{path.name} must contain a JSON object"
        )
    return payload


def _source_evidence() -> dict[str, str]:
    return {
        "improved_evidence_planning_execution_using_redesigned_evidence_digest": EXPECTED_EXECUTION_DIGEST,
        "improved_evidence_planning_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        **execution._source_evidence(),
    }


def _contains_sensitive_value(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() in {
                "api_key", "apikey", "authorization_header", "provider_payload", "raw_provider_payload"
            }:
                return True
            if _contains_sensitive_value(item):
                return True
    elif isinstance(value, list):
        return any(_contains_sensitive_value(item) for item in value)
    return False


def _forbidden_output_field(value: Any) -> str | None:
    forbidden_true = {
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready", "runtime_migration_approved", "runtime_migration_active",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
    }
    forbidden_authorized = {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in forbidden_true and item is True:
                return str(key)
            if key in forbidden_authorized and item != NOT_AUTHORIZED:
                return str(key)
            if key == "predictive_usefulness" and item == "accepted":
                return str(key)
            if key == "profitability" and item == "accepted":
                return str(key)
            nested = _forbidden_output_field(item)
            if nested:
                return nested
    elif isinstance(value, list):
        for item in value:
            nested = _forbidden_output_field(item)
            if nested:
                return nested
    return None


def _blocked_package(output_root: Path, reasons: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
        "review_status": IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "output_root": _path_text(output_root), "output_file_inspection_performed": False,
        "expected_output_count": 14, "observed_output_count": 0,
        "improved_evidence_planning_results_review_created": False,
        "improved_evidence_planning_results_review_ready": False,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "improved_evidence_planning_results_review_using_redesigned_evidence_digest": "NOT_CREATED",
        "blocker_reasons": reasons, "blocker_count": len(reasons),
    }


def _verify_outputs(
    output_root: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    paths = {filename: output_root / filename for filename in EXPECTED_OUTPUT_FILENAMES}
    for filename, path in paths.items():
        if not path.is_file():
            failures.append({"failure_id": "missing_output_file", "filename": filename})
    if failures:
        return {}, [], failures
    before_hashes = {filename: sha256_file(path) for filename, path in paths.items()}
    try:
        payloads = {filename: _load_json(path) for filename, path in paths.items()}
    except ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError as exc:
        return {}, [], [{"failure_id": "invalid_output_json", "message": str(exc)}]

    digest_manifest = payloads["improved_evidence_planning_digest_manifest.json"]
    rows = digest_manifest.get("output_digest_entries", [])
    if not isinstance(rows, list) or [row.get("filename") for row in rows if isinstance(row, dict)] != EXPECTED_OUTPUT_FILENAMES:
        failures.append({"failure_id": "digest_manifest_filename_mismatch"})
        entries: dict[str, dict[str, Any]] = {}
    else:
        entries = {row["filename"]: row for row in rows}

    bindings: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        actual = before_hashes[filename]
        entry = entries.get(filename)
        if filename == "improved_evidence_planning_digest_manifest.json":
            entry_valid = entry == {
                "filename": filename, "digest_kind": execution.SELF_REFERENCE_POLICY, "sha256": None,
            }
        else:
            entry_valid = entry == {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": actual}
        payload = payloads[filename]
        label_valid = payload.get("output_label") == execution.OUTPUT_LABEL
        scope_valid = payload.get("evidence_scope") == execution.EVIDENCE_SCOPE
        forbidden = _forbidden_output_field(payload)
        sensitive = _contains_sensitive_value(payload)
        status = PASS if entry_valid and label_valid and scope_valid and not forbidden and not sensitive else FAIL
        if not entry_valid:
            failures.append({"failure_id": "digest_manifest_entry_mismatch", "filename": filename})
        if not label_valid:
            failures.append({"failure_id": "output_label_mismatch", "filename": filename})
        if not scope_valid:
            failures.append({"failure_id": "evidence_scope_mismatch", "filename": filename})
        if forbidden:
            failures.append({"failure_id": "forbidden_output_authority", "filename": filename, "field": forbidden})
        if sensitive:
            failures.append({"failure_id": "sensitive_output_value", "filename": filename})
        bindings.append({
            "filename": filename, "local_sha256": actual,
            "recorded_digest_kind": entry.get("digest_kind") if entry else None,
            "recorded_sha256": entry.get("sha256") if entry else None,
            "verification_status": status,
        })

    source = payloads["improved_evidence_planning_execution_manifest.json"]
    if source.get("improved_evidence_planning_execution_using_redesigned_evidence_digest") != EXPECTED_EXECUTION_DIGEST:
        failures.append({"failure_id": "execution_digest_mismatch"})
    if source.get("output_digest_manifest_summary", {}).get("binding_digest") != EXPECTED_OUTPUT_BINDING_DIGEST:
        failures.append({"failure_id": "output_binding_digest_mismatch"})
    if digest_manifest.get("self_reference_policy") != execution.SELF_REFERENCE_POLICY:
        failures.append({"failure_id": "self_reference_policy_mismatch"})
    if digest_manifest.get("execution_digest") != EXPECTED_EXECUTION_DIGEST:
        failures.append({"failure_id": "digest_manifest_execution_digest_mismatch"})
    after_hashes = {filename: sha256_file(path) for filename, path in paths.items()}
    if before_hashes != after_hashes:
        failures.append({"failure_id": "source_output_mutated"})
    return payloads, bindings, failures


def per_ticker_improved_evidence_planning_results_review_digest_v1(entry: Mapping[str, Any]) -> str:
    clone = deepcopy(dict(entry))
    clone.pop("per_ticker_improved_evidence_planning_results_review_digest", None)
    return semantic_digest(clone)


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for source_row in source["per_ticker_execution_entries"]:
        ticker = source_row["ticker"]
        entry = {
            "ticker": ticker, "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN", "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "improved_evidence_planning_execution_status": "EXECUTED_RESEARCH_ONLY",
            "improved_evidence_planning_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "new_targets_created": False, "target_definition_change_authorized": False,
            "feature_generation_authorized": False, "feature_generation_performed": False,
            "feature_label_matrix_created": False,
            "additional_predictive_evidence_execution_candidate_created": False,
            "additional_predictive_evidence_executed": False,
            "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False, "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
            "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        }
        if ticker == "META":
            entry["review_note"] = "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW"
        entry["per_ticker_improved_evidence_planning_results_review_digest"] = (
            per_ticker_improved_evidence_planning_results_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _review(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "available": True, "verified": True,
        "plan_status": payload.get("plan_status"), "objective": payload.get("objective"),
        "execution_performed": payload.get("execution_performed"),
    }


def _base_package(
    output_root: Path, payloads: dict[str, dict[str, Any]], bindings: list[dict[str, Any]],
) -> dict[str, Any]:
    source = payloads["improved_evidence_planning_execution_manifest.json"]
    evidence = _source_evidence()
    local_hashes = {row["filename"]: row["local_sha256"] for row in bindings}
    per_ticker = _per_ticker_review_entries(source)
    classification = {
        "results_review_classification": "COMPLETED_RESEARCH_ONLY",
        "improved_evidence_planning_classification": "COMPLETED_RESEARCH_ONLY",
        "planning_execution_scope_review": "PLANNING_EXECUTION_ONLY_NOT_EVIDENCE_EXECUTION",
        "selected_redesign_direction_review": "REVIEWED_RESEARCH_ONLY",
        "label_schema_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "no_trade_abstain_coverage_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "material_move_threshold_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "horizon_specific_validation_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "ticker_regime_split_validation_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "feature_label_alignment_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "chronological_split_embargo_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "baseline_model_comparison_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "calibration_brier_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "leakage_no_peek_control_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "per_ticker_meta_reporting_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
        "additional_predictive_evidence_candidate_readiness": "OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION",
        "planning_decision_review": "NO_LABEL_GENERATION_FEATURE_GENERATION_MATRIX_CREATION_OR_PREDICTIVE_EXECUTION_AUTHORIZED",
        "predictive_usefulness_interpretation": "NOT_ACCEPTED",
        "profitability_interpretation": "NOT_ACCEPTED", "runtime_interpretation": "NOT_AUTHORIZED",
    }
    return {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
        "review_status": IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
        "branch": DEFAULT_BRANCH, "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_execution_artifact_kind": source["artifact_kind"],
        "source_execution_status": source["execution_status"],
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST, "source_evidence": evidence,
        "improved_evidence_planning_approved": True, "improved_evidence_planning_authorized": True,
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence": True,
        "improved_evidence_planning_executed": True, "improved_evidence_planning_results_created": True,
        "improved_evidence_planning_results_review_created": True,
        "improved_evidence_planning_results_review_ready": True,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": True,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "dataset_name": source["dataset_name"], "source_profile": source["source_profile"],
        "timeframe": source["timeframe"], "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"], "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"], "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source["meta_reduced_record_count_preserved"],
        "generated_output_count": source["generated_output_count"],
        "generated_output_names": list(source["generated_output_names"]),
        "improved_evidence_theme_count": source["improved_evidence_theme_count"],
        "planned_evidence_component_count": source["planned_evidence_component_count"],
        "planned_data_product_count": source["planned_data_product_count"],
        "planned_future_output_count": source["planned_future_output_count"],
        "planning_facts": deepcopy(source["planning_facts"]),
        "planning_execution_classification": deepcopy(source["planning_execution_classification"]),
        "output_root": _path_text(output_root), "expected_output_count": 14,
        "observed_output_count": len(bindings), "output_file_inspection_performed": True,
        "output_digest_bindings": bindings, "local_output_hashes": local_hashes,
        "output_digest_mismatch_count": sum(row["verification_status"] != PASS for row in bindings),
        "non_self_output_digest_match_count": sum(
            row["verification_status"] == PASS and row["recorded_digest_kind"] == "FILE_SHA256"
            for row in bindings
        ),
        "digest_manifest_self_reference_policy": execution.SELF_REFERENCE_POLICY,
        "outputs_research_only_non_actionable": True, "outputs_evidence_scope": execution.EVIDENCE_SCOPE,
        "planning_execution_manifest_review": {"available": True, "verified": True},
        "proposed_label_schema_plan_review": _review(payloads["proposed_label_schema_report.json"]),
        "no_trade_abstain_coverage_plan_review": _review(payloads["no_trade_abstain_coverage_report.json"]),
        "material_move_threshold_plan_review": _review(payloads["material_move_threshold_report.json"]),
        "horizon_specific_validation_plan_review": _review(payloads["horizon_specific_validation_report.json"]),
        "ticker_regime_split_validation_plan_review": _review(payloads["ticker_regime_split_validation_report.json"]),
        "feature_label_alignment_plan_review": _review(payloads["feature_label_alignment_report.json"]),
        "chronological_split_embargo_plan_review": _review(payloads["chronological_split_embargo_report.json"]),
        "baseline_model_comparison_plan_review": _review(payloads["baseline_model_comparison_plan.json"]),
        "calibration_brier_plan_review": _review(payloads["calibration_brier_plan.json"]),
        "leakage_no_peek_control_plan_review": _review(payloads["leakage_no_peek_control_plan.json"]),
        "per_ticker_meta_reporting_plan_review": _review(payloads["per_ticker_meta_reporting_plan.json"]),
        "operator_summary_review": {"available": True, "verified": True,
            "execution_status": payloads["operator_review_summary.json"].get("execution_status"),
            "next_task": payloads["operator_review_summary.json"].get("next_task")},
        "review_classification": classification, "per_ticker_results_review_entries": per_ticker,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "feature_generation_authorized": False,
        "feature_generation_performed": False, "feature_label_matrix_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False, "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False, "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False, "canonical_dataset_regenerated_in_review": False,
        "redesigned_label_regeneration_performed": False, "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "improved_evidence_planning_execution_rerun_performed": False,
        "metric_recomputation_performed_in_review": False, "model_training_performed_in_review": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False, "runtime_migration_approval_created": False,
        "limitations": list(LIMITATIONS), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": expected, "actual": actual,
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _review_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = package.get("source_evidence", {})
    values: dict[str, tuple[Any, Any]] = {
        "execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, package.get("source_execution_digest")),
        "output_binding_digest_bound": (EXPECTED_OUTPUT_BINDING_DIGEST, package.get("source_output_binding_digest")),
        "approval_digest_bound": (EXPECTED_APPROVAL_DIGEST, package.get("source_approval_digest")),
        "candidate_review_digest_bound": (execution.EXPECTED_CANDIDATE_REVIEW_DIGEST, evidence.get("improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest")),
        "candidate_digest_bound": (execution.EXPECTED_CANDIDATE_DIGEST, evidence.get("improved_evidence_planning_candidate_using_redesigned_evidence_digest")),
        "target_universe_12_preserved": (EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        "records_digest_preserved": (execution.EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        "meta_913_preserved": (913, package.get("meta_record_count")),
        "source_execution_status_research_only": (execution.IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY, package.get("source_execution_status")),
        "selected_redesign_direction_preserved": (SELECTED_DIRECTION, package.get("selected_redesign_direction")),
        "generated_output_count_14": (14, package.get("generated_output_count")),
        "output_digests_bound": (14, len(package.get("local_output_hashes", {}))),
        "output_digest_mismatch_count_zero": (0, package.get("output_digest_mismatch_count")),
        "outputs_research_only_non_actionable": (True, package.get("outputs_research_only_non_actionable")),
        "planning_execution_manifest_verified": (True, package.get("planning_execution_manifest_review", {}).get("verified")),
        "results_review_created_true": (True, package.get("improved_evidence_planning_results_review_created")),
        "results_review_ready_true": (True, package.get("improved_evidence_planning_results_review_ready")),
        "ready_for_optional_additional_predictive_evidence_candidate_true": (True, package.get("ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence")),
        "label_regeneration_authorized_false": (False, package.get("label_regeneration_authorized")),
        "label_regeneration_performed_false": (False, package.get("label_regeneration_performed")),
        "new_targets_created_false": (False, package.get("new_targets_created")),
        "target_definition_change_authorized_false": (False, package.get("target_definition_change_authorized")),
        "target_definition_change_performed_false": (False, package.get("target_definition_change_performed")),
        "feature_generation_authorized_false": (False, package.get("feature_generation_authorized")),
        "feature_generation_performed_false": (False, package.get("feature_generation_performed")),
        "feature_label_matrix_created_false": (False, package.get("feature_label_matrix_created")),
        "additional_predictive_evidence_execution_candidate_created_false": (False, package.get("additional_predictive_evidence_execution_candidate_created")),
        "additional_predictive_evidence_executed_false": (False, package.get("additional_predictive_evidence_executed")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, package.get("predictive_usefulness")),
        "acceptance_ready_false": (False, package.get("predictive_usefulness_acceptance_ready")),
        "acceptance_candidate_created_false": (False, package.get("predictive_usefulness_acceptance_candidate_created")),
        "profitability_not_accepted": (NOT_ACCEPTED, package.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, package.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, package.get("strategy_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, package.get("broker_execution")),
        "trade_recommendations_false": (False, package.get("trade_recommendations_generated")),
        "planning_scope_preserved": (execution.PLANNING_EXECUTION_SCOPE, package.get("review_classification", {}).get("planning_execution_scope_review")),
        "selected_direction_reviewed": ("REVIEWED_RESEARCH_ONLY", package.get("review_classification", {}).get("selected_redesign_direction_review")),
        "future_evidence_candidate_readiness_recorded": ("OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION", package.get("review_classification", {}).get("additional_predictive_evidence_candidate_readiness")),
        "meta_limitation_preserved": (True, package.get("meta_reduced_record_count_preserved")),
        "per_ticker_entries_12": (12, len(package.get("per_ticker_results_review_entries", []))),
        "per_ticker_digests_present": (True, all(len(row.get("per_ticker_improved_evidence_planning_results_review_digest", "")) == 64 for row in package.get("per_ticker_results_review_entries", []))),
        "provider_requests_made_false": (False, package.get("provider_requests_made_in_review")),
        "market_data_acquisition_false": (False, package.get("market_data_acquisition_performed_in_review")),
        "dataset_regeneration_false": (False, package.get("canonical_dataset_regenerated_in_review")),
        "redesigned_label_regeneration_false": (False, package.get("redesigned_label_regeneration_performed")),
        "feature_regeneration_false": (False, package.get("feature_regeneration_performed")),
        "predictive_evidence_rerun_false": (False, package.get("predictive_evidence_execution_rerun_performed")),
        "improved_evidence_planning_execution_rerun_false": (False, package.get("improved_evidence_planning_execution_rerun_performed")),
        "metric_recomputation_in_review_false": (False, package.get("metric_recomputation_performed_in_review")),
        "model_training_in_review_false": (False, package.get("model_training_performed_in_review")),
        "raw_provider_payloads_not_committed": (False, package.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, package.get("api_keys_stored_or_printed")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, package.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, package.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, package.get("runtime_migration_approval_created")),
        "limitations_recorded": (LIMITATIONS, package.get("limitations")),
        "next_chain_defined": (NEXT_CHAIN, package.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, package.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, package.get("risk_controls")),
        "no_tracked_marketflow_files": (True, package.get("no_tracked_marketflow_files")),
    }
    evidence_checks = {
        "redesign_results_review_digest_bound": "label_objective_redesign_results_review_using_redesigned_evidence_digest",
        "redesign_execution_digest_bound": "label_objective_redesign_execution_using_redesigned_evidence_digest",
        "redesign_output_binding_digest_bound": "label_objective_redesign_output_binding_digest",
        "target_definition_results_review_digest_bound": "label_objective_target_definition_results_review_using_redesigned_evidence_digest",
        "target_definition_execution_digest_bound": "label_objective_target_definition_review_execution_using_redesigned_evidence_digest",
        "path_selection_digest_bound": "method_evidence_improvement_path_selection_using_redesigned_evidence_digest",
        "readiness_review_digest_bound": "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest",
        "reassessment_digest_bound": "predictive_usefulness_reassessment_using_redesigned_evidence_digest",
        "predictive_results_review_digest_bound": "additional_predictive_evidence_results_review_using_redesigned_labels_digest",
        "predictive_execution_digest_bound": "additional_predictive_evidence_execution_using_redesigned_labels_digest",
        "matrix_digest_bound": "feature_label_matrix_digest", "feature_values_digest_bound": "feature_values_digest",
        "label_values_digest_bound": "redesigned_label_values_digest",
        "research_registry_digest_bound": "research_registry_approval_digest", "records_digest_bound": "records_digest",
    }
    expected_evidence = _source_evidence()
    for check_id, field in evidence_checks.items():
        values[check_id] = (expected_evidence[field], evidence.get(field))
    report_checks = {
        "proposed_label_schema_report_verified": "proposed_label_schema_plan_review",
        "no_trade_abstain_coverage_report_verified": "no_trade_abstain_coverage_plan_review",
        "material_move_threshold_report_verified": "material_move_threshold_plan_review",
        "horizon_specific_validation_report_verified": "horizon_specific_validation_plan_review",
        "ticker_regime_split_validation_report_verified": "ticker_regime_split_validation_plan_review",
        "feature_label_alignment_report_verified": "feature_label_alignment_plan_review",
        "chronological_split_embargo_report_verified": "chronological_split_embargo_plan_review",
        "baseline_model_comparison_plan_verified": "baseline_model_comparison_plan_review",
        "calibration_brier_plan_verified": "calibration_brier_plan_review",
        "leakage_no_peek_control_plan_verified": "leakage_no_peek_control_plan_review",
        "per_ticker_meta_reporting_plan_verified": "per_ticker_meta_reporting_plan_review",
        "operator_summary_verified": "operator_summary_review",
    }
    for check_id, field in report_checks.items():
        values[check_id] = (True, package.get(field, {}).get("verified"))
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed), "results_review_ready": not failed,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": not failed,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def improved_evidence_planning_results_review_using_redesigned_evidence_digest_v1(
    review_package: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review_package))
    payload.pop("improved_evidence_planning_results_review_using_redesigned_evidence_digest", None)
    if "output_root" in payload:
        payload["output_root"] = DEFAULT_OUTPUT_ROOT.as_posix()
    return semantic_digest(payload)


def build_improved_evidence_planning_results_review_using_redesigned_evidence_v1(
    *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Inspect and hash existing outputs without rerunning planning execution."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    try:
        execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
            payloads["improved_evidence_planning_execution_manifest.json"]
        )
    except execution.ImprovedEvidencePlanningExecutionRedesignedEvidenceError as exc:
        return _blocked_package(root, [{"failure_id": "invalid_source_execution_artifact", "message": str(exc)}])
    package = _base_package(root, payloads, bindings)
    package["review_checklist"] = _review_checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    if package["review_summary"]["blocker_count"]:
        return _blocked_package(root, [
            {"failure_id": "review_check_failed", "check_id": row["check_id"]}
            for row in package["review_checklist"] if row["status"] != PASS
        ])
    package["improved_evidence_planning_results_review_using_redesigned_evidence_digest"] = (
        improved_evidence_planning_results_review_using_redesigned_evidence_digest_v1(package)
    )
    validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError(f"{field} mismatch")


def validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Validate ready and blocked review packages without touching source outputs."""
    if not isinstance(review_package, dict):
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError("review package must be a JSON object")
    _expect(review_package.get("artifact_kind"),
            ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
            "artifact_kind")
    _expect(review_package.get("schema_version"),
            SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
            "schema_version")
    if review_package.get("review_status") == IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS:
        _expect(review_package.get("improved_evidence_planning_results_review_ready"), False, "blocked review ready")
        _expect(review_package.get("ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence"), False, "blocked candidate readiness")
        _expect(review_package.get("improved_evidence_planning_results_review_using_redesigned_evidence_digest"), "NOT_CREATED", "blocked digest")
        return {"status": "IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_BLOCKED_VALID",
                "review_status": review_package["review_status"], "blocker_count": review_package.get("blocker_count", 0)}
    _expect(review_package.get("review_status"),
            IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
            "review_status")
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE,
        "source_execution_status": execution.IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST, "source_evidence": _source_evidence(),
        "selected_redesign_direction": SELECTED_DIRECTION, "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12, "total_canonical_record_count": 11946,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST, "meta_record_count": 913,
        "non_meta_record_count": 1003, "generated_output_count": 14,
        "generated_output_names": EXPECTED_OUTPUT_FILENAMES, "expected_output_count": 14,
        "observed_output_count": 14, "digest_manifest_self_reference_policy": execution.SELF_REFERENCE_POLICY,
        "limitations": LIMITATIONS, "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
    true_fields = [
        "created_offline", "research_only", "operator_review_required", "improved_evidence_planning_approved",
        "improved_evidence_planning_authorized", "ready_for_improved_evidence_planning_execution_using_redesigned_evidence",
        "improved_evidence_planning_executed", "improved_evidence_planning_results_created",
        "improved_evidence_planning_results_review_created", "improved_evidence_planning_results_review_ready",
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence",
        "output_file_inspection_performed", "outputs_research_only_non_actionable",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ]
    false_fields = [
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed", "improved_evidence_planning_execution_rerun_performed",
        "metric_recomputation_performed_in_review", "model_training_performed_in_review",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ]
    for field in true_fields:
        _expect(review_package.get(field), True, field)
    for field in false_fields:
        _expect(review_package.get(field), False, field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    _expect(review_package.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), NOT_ACCEPTED, "profitability")
    _expect(review_package.get("output_digest_mismatch_count"), 0, "output_digest_mismatch_count")
    _expect(review_package.get("non_self_output_digest_match_count"), 13, "non_self digest match count")
    hashes = review_package.get("local_output_hashes")
    if not isinstance(hashes, dict) or len(hashes) != 14 or any(len(value) != 64 for value in hashes.values()):
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError("local output hashes mismatch")
    entries = review_package.get("per_ticker_results_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError("per-ticker entries mismatch")
    for entry in entries:
        digest = entry.get("per_ticker_improved_evidence_planning_results_review_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError("per-ticker digest missing")
        _expect(digest, per_ticker_improved_evidence_planning_results_review_digest_v1(entry), "per-ticker digest")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError("review checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review checklist ids")
    if any(row.get("status") != PASS for row in checklist):
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError("review checklist must pass")
    _expect(review_package.get("review_summary"), _summary(checklist), "review summary")
    digest = review_package.get("improved_evidence_planning_results_review_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError("missing review digest")
    _expect(digest, improved_evidence_planning_results_review_using_redesigned_evidence_digest_v1(review_package), "review digest")
    return {
        "status": IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID,
        "artifact_kind": review_package["artifact_kind"], "review_status": review_package["review_status"],
        "improved_evidence_planning_results_review_using_redesigned_evidence_digest": digest,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST, "generated_output_count": 14,
        "blocker_count": 0,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_improved_evidence_planning_results_review_using_redesigned_evidence_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized Markdown review without reproducing source output bodies."""
    validation = validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(review_package)
    summary = review_package["review_summary"]
    sections = [
        ("Title", ["Optional Improved Evidence Planning Results Review Using Redesigned Evidence v1."]),
        ("Optional Improved Evidence Planning Results Review Using Redesigned Evidence", [
            f"Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['improved_evidence_planning_results_review_using_redesigned_evidence_digest']}`."
        ]),
        ("Source Execution", [f"Execution digest/binding: `{review_package['source_execution_digest']}` / `{review_package['source_output_binding_digest']}`."]),
        ("Bound Evidence", [f"Approval/records: `{review_package['source_approval_digest']}` / `{review_package['records_digest']}`."]),
        ("Dataset and Universe", [f"`{review_package['dataset_name']}`; 11,946 records; META 913.", ", ".join(review_package["target_universe"])]),
        ("Output Verification", [f"Observed/expected/mismatches: `{review_package['observed_output_count']}` / `14` / `{review_package['output_digest_mismatch_count']}`.", f"Self-reference: `{review_package['digest_manifest_self_reference_policy']}`."]),
        ("Selected Redesign Direction", [f"`{SELECTED_DIRECTION}` remains research-only and requires operator selection."]),
        ("Planning Scope Review", [f"`{review_package['review_classification']['planning_execution_scope_review']}`."]),
        ("Proposed Label Schema Plan Review", [str(review_package["proposed_label_schema_plan_review"])]),
        ("No-Trade / Abstain Coverage Plan Review", [str(review_package["no_trade_abstain_coverage_plan_review"])]),
        ("Material-Move Threshold Plan Review", [str(review_package["material_move_threshold_plan_review"])]),
        ("Horizon-Specific Validation Plan Review", [str(review_package["horizon_specific_validation_plan_review"])]),
        ("Ticker / Regime Split Validation Plan Review", [str(review_package["ticker_regime_split_validation_plan_review"])]),
        ("Feature-Label Alignment Plan Review", [str(review_package["feature_label_alignment_plan_review"])]),
        ("Chronological Split and Embargo Plan Review", [str(review_package["chronological_split_embargo_plan_review"])]),
        ("Baseline and Model Comparison Plan Review", [str(review_package["baseline_model_comparison_plan_review"])]),
        ("Calibration / Brier Plan Review", [str(review_package["calibration_brier_plan_review"])]),
        ("Leakage and No-Peek Control Plan Review", [str(review_package["leakage_no_peek_control_plan_review"])]),
        ("Per-Ticker and META Reporting Plan Review", [str(review_package["per_ticker_meta_reporting_plan_review"])]),
        ("Review Classification", [str(review_package["review_classification"])]),
    ]
    lines = ["# MarketFlow Improved Evidence Planning Results Review Using Redesigned Evidence Status", ""]
    for title, body in sections:
        lines.extend([f"## {title}", *[f"- {item}" for item in body], ""])
    for title, values in (("Limitations", LIMITATIONS), ("Next Chain", NEXT_CHAIN),
                          ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS)):
        lines.append(f"## {title}")
        lines.extend(f"{index}. {item}" if title == "Next Chain" else f"- `{item}`"
                     for index, item in enumerate(values, 1))
        lines.append("")
    lines.extend([
        "## Predictive Usefulness Boundary", "- Predictive usefulness remains `not accepted`.", "",
        "## Profitability Boundary", "- Profitability remains `not accepted`.", "",
        "## Runtime Boundary", "- Runtime, strategy, paper, and broker use remain `NOT_AUTHORIZED`.", "",
        "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.", "",
        "## Guardrails", "- Existing ignored planning outputs were hashed and reviewed read-only; no execution, regeneration, candidate creation, acceptance, profitability, runtime, or trading action occurred.", "",
    ])
    return "\n".join(lines)


def write_improved_evidence_planning_results_review_using_redesigned_evidence_v1(
    output_dir: str | Path, *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Write one canonical ready review package without overwriting evidence."""
    package = build_improved_evidence_planning_results_review_using_redesigned_evidence_v1(
        output_root=output_root
    )
    validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "improved_evidence_planning_results_review_using_redesigned_evidence_v1.json"
    payload = canonical_json_bytes(package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError(
            "results review output already exists"
        ) from exc
    return {
        "path": _path_text(path), "filename": path.name, "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload), "review_status": package["review_status"],
        "improved_evidence_planning_results_review_using_redesigned_evidence_digest": package[
            "improved_evidence_planning_results_review_using_redesigned_evidence_digest"
        ],
    }
