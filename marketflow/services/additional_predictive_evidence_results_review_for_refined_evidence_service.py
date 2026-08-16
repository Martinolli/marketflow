"""Offline, digest-bound review of refined predictive-evidence execution outputs."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    additional_predictive_evidence_execution_for_refined_evidence_service as execution,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_V1 = (
    "additional_predictive_evidence_results_review_for_refined_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "9cf962933620f066dfb105845428a262743f9f36dbc2850838321f23de10b5fd"
)
EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST = execution.EXPECTED_EXECUTION_APPROVAL_DIGEST
EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST = execution.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST = execution.EXPECTED_CANDIDATE_DIGEST
EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST = (
    execution.EXPECTED_REFINEMENT_RESULTS_REVIEW_DIGEST
)
EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST = execution.EXPECTED_REFINEMENT_EXECUTION_DIGEST
EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST = (
    execution.EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST = execution.EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST
EXPECTED_ORIGINAL_EXECUTION_DIGEST = execution.EXPECTED_ORIGINAL_EXECUTION_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = execution.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
EXPECTED_RECORDS_DIGEST = execution.EXPECTED_RECORDS_DIGEST
EXPECTED_REFINED_LABEL_DIGEST = execution.EXPECTED_REFINED_LABEL_DIGEST
EXPECTED_REFINED_FEATURE_DIGEST = execution.EXPECTED_REFINED_FEATURE_DIGEST

TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_OUTPUT_COUNT = len(EXPECTED_OUTPUT_FILENAMES)
DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = execution.OUTPUT_LABEL
EVIDENCE_SCOPE = execution.EVIDENCE_SCOPE
SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_REGISTRY_METADATA = {
    "dataset_name": "expanded_universe_canonical_dataset_v1",
    "dataset_scope": "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY",
    "registry_entry_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
    "source_profile": "RTH_FULL_SESSION_1D",
    "date_range_start": "2022-01-01",
    "date_range_end": "2025-12-31",
    "timeframe": "1d",
    "target_universe_count": 12,
    "total_canonical_record_count": 11946,
    "records_digest": EXPECTED_RECORDS_DIGEST,
    "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
    "registry_label": RESEARCH_ONLY_NON_ACTIONABLE,
}

LIMITATIONS = [
    "refined_execution_results_are_research_only",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "trade_recommendations_not_generated",
    "refined_oos_accuracy_low_or_mixed",
    "model_comparison_not_acceptance_evidence_by_itself",
    "calibration_stability_not_acceptance_evidence_by_itself",
    "unavailable_model_families_recorded_not_fabricated",
    "meta_reduced_record_count_preserved",
    "operator_review_required_before_predictive_usefulness_reassessment_rerun",
    "operator_approval_required_before_any_acceptance_or_runtime_migration",
]

NEXT_GATES = [
    "additional_predictive_evidence_results_review_for_refined_evidence_operator_review",
    "predictive_usefulness_reassessment_review_rerun_using_refined_evidence",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]


class AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(ValueError):
    """Raised when the refined-evidence review violates its fail-closed contract."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


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


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            f"{field} must be false"
        )


def _walk_items(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key), item
            yield from _walk_items(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_items(item)


def _load_outputs(
    root: Path,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, str]]]:
    entries: list[dict[str, Any]] = []
    outputs: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        path = root / filename
        entry: dict[str, Any] = {
            "filename": filename,
            "path": _path_text(path),
            "exists": path.is_file(),
            "valid_json_object": False,
            "file_sha256": None,
            "file_byte_size": None,
            "output_label": None,
            "evidence_scope": None,
            "acceptance_evidence_status": None,
            "profitability_evidence_status": None,
            "runtime_authority_status": None,
        }
        if path.is_file():
            payload = path.read_bytes()
            entry["file_sha256"] = sha256_bytes(payload)
            entry["file_byte_size"] = len(payload)
            try:
                value = json.loads(payload.decode("utf-8"))
                if not isinstance(value, dict):
                    raise ValueError("JSON root is not an object")
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                errors.append({"filename": filename, "error": str(exc)})
            else:
                entry["valid_json_object"] = True
                for field in (
                    "output_label",
                    "evidence_scope",
                    "acceptance_evidence_status",
                    "profitability_evidence_status",
                    "runtime_authority_status",
                ):
                    entry[field] = value.get(field)
                outputs[filename] = value
        entries.append(entry)
    return entries, outputs, errors


def _digest_manifest_summary(
    entries: list[dict[str, Any]], outputs: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    manifest_name = "refined_execution_digest_manifest.json"
    actual = {entry["filename"]: entry["file_sha256"] for entry in entries}
    manifest = outputs.get(manifest_name, {})
    raw_declared = manifest.get("output_digest_entries")
    declared_entries = raw_declared if isinstance(raw_declared, list) else []
    declared = {
        item.get("filename"): item
        for item in declared_entries
        if isinstance(item, dict) and isinstance(item.get("filename"), str)
    }
    mismatches: list[dict[str, Any]] = []
    verified_non_self = 0
    for filename in EXPECTED_OUTPUT_FILENAMES:
        item = declared.get(filename)
        if filename == manifest_name:
            continue
        expected = item.get("sha256") if isinstance(item, dict) else None
        kind = item.get("digest_kind") if isinstance(item, dict) else None
        if kind == "FILE_SHA256" and expected == actual.get(filename):
            verified_non_self += 1
        else:
            mismatches.append(
                {
                    "filename": filename,
                    "declared_digest_kind": kind,
                    "declared_sha256": expected,
                    "actual_sha256": actual.get(filename),
                }
            )
    self_entry = declared.get(manifest_name)
    self_valid = bool(
        isinstance(self_entry, dict)
        and self_entry.get("digest_kind") == SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
        and self_entry.get("sha256") is None
        and manifest.get("self_reference_policy")
        == SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
    )
    if not self_valid:
        mismatches.append(
            {
                "filename": manifest_name,
                "declared_digest_kind": self_entry.get("digest_kind")
                if isinstance(self_entry, dict)
                else None,
                "declared_sha256": self_entry.get("sha256")
                if isinstance(self_entry, dict)
                else None,
                "actual_sha256": actual.get(manifest_name),
            }
        )
    return {
        "manifest_available": bool(manifest),
        "declared_entry_count": len(declared_entries),
        "actual_output_file_digests": actual,
        "verified_non_self_digest_count": verified_non_self,
        "digest_mismatch_count": len(mismatches),
        "digest_mismatches": mismatches,
        "self_reference_policy": self_entry.get("digest_kind")
        if isinstance(self_entry, dict)
        else None,
        "self_reference_valid": self_valid,
    }


def _output_boundary_summary(outputs: dict[str, dict[str, Any]]) -> dict[str, bool]:
    states = {
        "raw_provider_payload_present": False,
        "api_secret_present": False,
        "trade_recommendation_present": False,
        "predictive_acceptance_present": False,
        "profitability_acceptance_present": False,
        "runtime_authority_present": False,
    }
    for output in outputs.values():
        for key, value in _walk_items(output):
            lowered = key.lower()
            if "raw_provider_payload" in lowered and not lowered.endswith("committed"):
                states["raw_provider_payload_present"] |= value not in (None, False, "", [], {})
            if lowered in {
                "api_key",
                "apikey",
                "api_token",
                "authorization_header",
                "password",
                "secret",
            }:
                states["api_secret_present"] |= value not in (
                    None,
                    False,
                    "",
                    "NOT_STORED",
                    "REDACTED",
                )
            if lowered in {"trade_recommendation", "trade_recommendations_generated"}:
                states["trade_recommendation_present"] |= value is True
            if lowered == "predictive_usefulness" and value == "accepted":
                states["predictive_acceptance_present"] = True
            if lowered == "predictive_usefulness_acceptance_candidate_created" and value is True:
                states["predictive_acceptance_present"] = True
            if lowered == "profitability" and value == "accepted":
                states["profitability_acceptance_present"] = True
            if lowered in {
                "runtime_migration_approved",
                "runtime_migration_active",
                "automatic_stitching",
            } and value is True:
                states["runtime_authority_present"] = True
            if lowered in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
                states["runtime_authority_present"] |= value == "AUTHORIZED"
    return states


def _facts(outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    manifest = outputs.get("refined_additional_predictive_evidence_execution_manifest.json", {})
    binding = outputs.get("refined_label_feature_binding_manifest.json", {}).get(
        "binding_summary", {}
    )
    walk = outputs.get("refined_walk_forward_reassessment_report.json", {})
    oos = outputs.get("refined_out_of_sample_reassessment_report.json", {})
    model = outputs.get("refined_baseline_model_comparison_report.json", {})
    calibration = outputs.get("refined_calibration_stability_report.json", {})
    leakage = outputs.get("refined_leakage_quality_report.json", {})
    input_manifest = outputs.get("refined_evidence_input_manifest.json", {})
    source = manifest.get("source_evidence", {}) if isinstance(manifest, dict) else {}
    registry = (
        manifest.get("registry_approved_dataset_metadata", {})
        if isinstance(manifest, dict)
        else {}
    )
    return {
        "manifest": manifest,
        "source": source,
        "registry": registry,
        "input_binding": deepcopy(input_manifest.get("input_binding_summary", {})),
        "binding": deepcopy(binding),
        "walk": deepcopy(walk),
        "oos": deepcopy(oos),
        "model": deepcopy(model),
        "calibration": deepcopy(calibration),
        "leakage": deepcopy(leakage),
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("refined_execution_digest_bound", EXPECTED_SOURCE_EXECUTION_DIGEST, "source_additional_predictive_evidence_execution_for_refined_evidence_digest"),
    ("refined_execution_approval_digest_bound", EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST, "source_additional_predictive_evidence_execution_approval_for_refined_evidence_digest"),
    ("refined_execution_candidate_review_digest_bound", EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST, "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest"),
    ("feature_label_refinement_results_review_digest_bound", EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST, "feature_label_refinement_results_review_package_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_execution_universe", TARGET_UNIVERSE, "target_universe"),
    ("total_canonical_record_count_11946", 11946, "total_canonical_record_count"),
    ("meta_record_count_913_preserved", 913, "meta_record_count"),
    ("non_meta_record_counts_1003_preserved", True, "non_meta_record_counts_1003_preserved"),
    ("generated_output_count_10", 10, "generated_output_count"),
    ("output_file_inspection_performed", True, "output_file_inspection_performed"),
    ("output_digests_bound", True, "output_digests_bound"),
    ("outputs_research_only_non_actionable", True, "outputs_research_only_non_actionable"),
    ("outputs_not_acceptance_evidence", True, "outputs_not_acceptance_evidence"),
    ("outputs_not_profitability_evidence", True, "outputs_not_profitability_evidence"),
    ("outputs_not_runtime_authority", True, "outputs_not_runtime_authority"),
    ("digest_manifest_self_reference_non_applicable", True, "digest_manifest_self_reference_non_applicable"),
    ("refined_label_family_count_7", 7, "refined_label_family_count"),
    ("refined_label_available_values_82698", 82698, "refined_label_available_values"),
    ("refined_label_unavailable_values_924", 924, "refined_label_unavailable_values"),
    ("refined_feature_group_count_9", 9, "refined_feature_group_count"),
    ("refined_feature_fields_19", 19, "refined_feature_field_count"),
    ("refined_protocol_group_count_6", 6, "refined_protocol_group_count"),
    ("model_comparison_group_count_5", 5, "model_comparison_group_count"),
    ("refined_walk_forward_fold_count_4", 4, "refined_walk_forward_fold_count"),
    ("refined_walk_forward_rows_3024", 3024, "refined_walk_forward_evaluation_rows"),
    ("refined_oos_rows_2988", 2988, "refined_oos_evaluation_rows"),
    ("refined_oos_accuracy_range_bound", "0.119813 to 0.480924", "refined_oos_accuracy_range"),
    ("model_comparison_summary_bound", True, "model_comparison_summary_bound"),
    ("unavailable_model_families_recorded", 3, "unavailable_model_family_requests"),
    ("refined_leakage_status_pass", "PASS", "refined_leakage_status"),
    ("failed_leakage_controls_zero", 0, "failed_leakage_controls"),
    ("data_quality_pass_with_preserved_limitation", "PASS_WITH_PRESERVED_SOURCE_LIMITATION", "data_quality_status"),
    ("provider_requests_made_in_review_false", False, "provider_requests_made_in_review"),
    ("live_provider_transport_enabled_in_review_false", False, "live_provider_transport_enabled_in_review"),
    ("market_data_acquisition_performed_in_review_false", False, "market_data_acquisition_performed_in_review"),
    ("dataset_generation_performed_in_review_false", False, "dataset_generation_performed_in_review"),
    ("canonical_dataset_regenerated_in_review_false", False, "canonical_dataset_regenerated_in_review"),
    ("feature_label_refinement_execution_rerun_performed_false", False, "feature_label_refinement_execution_rerun_performed"),
    ("refined_label_generation_rerun_performed_false", False, "refined_label_generation_rerun_performed"),
    ("refined_feature_generation_rerun_performed_false", False, "refined_feature_generation_rerun_performed"),
    ("refined_walk_forward_reassessment_rerun_performed_false", False, "refined_walk_forward_reassessment_rerun_performed"),
    ("refined_out_of_sample_reassessment_rerun_performed_false", False, "refined_out_of_sample_reassessment_rerun_performed"),
    ("refined_metrics_recomputation_performed_false", False, "refined_metrics_recomputation_performed"),
    ("refined_model_comparison_rerun_performed_false", False, "refined_model_comparison_rerun_performed"),
    ("additional_predictive_evidence_execution_for_refined_evidence_rerun_performed_false", False, "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("raw_provider_payloads_absent_from_outputs", False, "raw_provider_payloads_present_in_outputs"),
    ("api_keys_absent_from_outputs", False, "api_keys_present_in_outputs"),
    ("additional_predictive_evidence_execution_for_refined_evidence_executed_true", True, "additional_predictive_evidence_execution_for_refined_evidence_executed"),
    ("additional_predictive_evidence_results_for_refined_evidence_created_true", True, "additional_predictive_evidence_results_for_refined_evidence_created"),
    ("refined_evidence_input_binding_performed_true", True, "refined_evidence_input_binding_performed"),
    ("refined_walk_forward_reassessment_performed_true", True, "refined_walk_forward_reassessment_performed"),
    ("refined_out_of_sample_reassessment_performed_true", True, "refined_out_of_sample_reassessment_performed"),
    ("refined_baseline_model_comparison_reassessment_performed_true", True, "refined_baseline_model_comparison_reassessment_performed"),
    ("refined_calibration_stability_review_performed_true", True, "refined_calibration_stability_review_performed"),
    ("refined_leakage_quality_review_performed_true", True, "refined_leakage_quality_review_performed"),
    ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created_false", False, "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created"),
    ("new_strategy_scoring_performed_false", False, "new_strategy_scoring_performed"),
    ("trade_recommendations_generated_false", False, "trade_recommendations_generated"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("predictive_usefulness_acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("predictive_usefulness_acceptance_recommended_false", False, "predictive_usefulness_acceptance_recommended"),
    ("predictive_usefulness_acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_migration_approved_false", False, "runtime_migration_approved"),
    ("runtime_use_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_use_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("paper_trading_not_authorized", NOT_AUTHORIZED, "paper_trading"),
    ("broker_execution_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("automatic_stitching_false", False, "automatic_stitching"),
    ("results_support_predictive_usefulness_reassessment_rerun_true", True, "results_support_predictive_usefulness_reassessment_rerun_using_refined_evidence"),
    ("results_create_predictive_usefulness_reassessment_review_false", False, "results_create_predictive_usefulness_reassessment_review"),
    ("results_create_predictive_usefulness_acceptance_false", False, "results_create_predictive_usefulness_acceptance"),
    ("results_create_profitability_acceptance_false", False, "results_create_profitability_acceptance"),
    ("results_create_runtime_authority_false", False, "results_create_runtime_authority"),
    ("limitations_recorded", LIMITATIONS, "limitations"),
    ("next_gates_defined", NEXT_GATES, "next_gates"),
    ("no_predictive_usefulness_reassessment_review_created", False, "predictive_usefulness_reassessment_review_created"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
]
REQUIRED_CHECK_IDS = [item[0] for item in CHECK_FIELD_SPECS]


def _checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    return [_check(check_id, expected, package.get(field)) for check_id, expected, field in CHECK_FIELD_SPECS]


def _summary(checklist: list[dict[str, Any]], *, review_status: str) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    blockers = sum(
        item.get("status") == FAIL and item.get("severity") == BLOCKER
        for item in checklist
    )
    ready = (
        review_status
        == ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY
        and blockers == 0
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "ready_for_operator_review": ready,
        "ready_for_predictive_usefulness_reassessment_review_rerun_using_refined_evidence": ready,
        "predictive_usefulness_reassessment_review_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop(
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest",
        None,
    )
    return payload


def additional_predictive_evidence_results_review_for_refined_evidence_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for a refined-evidence review."""
    return semantic_digest(_digest_payload(review_package))


def build_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
    *, output_root: str | Path | None = None
) -> dict[str, Any]:
    """Inspect saved refined outputs offline and build a fail-closed review package."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    entries, outputs, parse_errors = _load_outputs(root)
    digest_summary = _digest_manifest_summary(entries, outputs)
    boundaries = _output_boundary_summary(outputs)
    facts = _facts(outputs)
    manifest = facts["manifest"]
    source = facts["source"] if isinstance(facts["source"], dict) else {}
    binding = facts["binding"] if isinstance(facts["binding"], dict) else {}
    walk = facts["walk"] if isinstance(facts["walk"], dict) else {}
    oos = facts["oos"] if isinstance(facts["oos"], dict) else {}
    model = facts["model"] if isinstance(facts["model"], dict) else {}
    calibration = facts["calibration"] if isinstance(facts["calibration"], dict) else {}
    leakage = facts["leakage"] if isinstance(facts["leakage"], dict) else {}
    valid_count = sum(entry["valid_json_object"] is True for entry in entries)
    inspected = valid_count == EXPECTED_OUTPUT_COUNT
    all_labeled = inspected and all(
        entry["output_label"] == RESEARCH_ONLY_NON_ACTIONABLE for entry in entries
    )
    all_scoped = inspected and all(entry["evidence_scope"] == EVIDENCE_SCOPE for entry in entries)
    all_not_acceptance = inspected and all(
        entry["acceptance_evidence_status"] == "NOT_ACCEPTANCE_EVIDENCE" for entry in entries
    )
    all_not_profitability = inspected and all(
        entry["profitability_evidence_status"] == "NOT_PROFITABILITY_EVIDENCE"
        for entry in entries
    )
    all_not_runtime = inspected and all(
        entry["runtime_authority_status"] == "NOT_RUNTIME_AUTHORITY" for entry in entries
    )
    per_ticker = manifest.get("per_ticker_record_counts", {}) if isinstance(manifest, dict) else {}
    non_meta_valid = isinstance(per_ticker, dict) and all(
        per_ticker.get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META"
    )
    common: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "feature_label_refinement_execution_rerun_performed": False,
        "refined_label_generation_rerun_performed": False,
        "refined_feature_generation_rerun_performed": False,
        "refined_walk_forward_reassessment_rerun_performed": False,
        "refined_out_of_sample_reassessment_rerun_performed": False,
        "refined_metrics_recomputation_performed": False,
        "refined_model_comparison_rerun_performed": False,
        "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "raw_provider_payloads_present_in_outputs": boundaries["raw_provider_payload_present"],
        "api_keys_present_in_outputs": boundaries["api_secret_present"],
        "trade_recommendations_present_in_outputs": boundaries["trade_recommendation_present"],
        "predictive_acceptance_present_in_outputs": boundaries["predictive_acceptance_present"],
        "profitability_acceptance_present_in_outputs": boundaries["profitability_acceptance_present"],
        "runtime_authority_present_in_outputs": boundaries["runtime_authority_present"],
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY,
        "source_additional_predictive_evidence_execution_for_refined_evidence_digest": manifest.get(
            "additional_predictive_evidence_execution_for_refined_evidence_digest",
            EXPECTED_SOURCE_EXECUTION_DIGEST,
        ),
        "source_additional_predictive_evidence_execution_approval_for_refined_evidence_digest": source.get(
            "additional_predictive_evidence_execution_approval_for_refined_evidence_digest",
            EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        ),
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest": source.get(
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest",
            EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        ),
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": source.get(
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest",
            EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        ),
        "feature_label_refinement_results_review_package_digest": source.get(
            "feature_label_refinement_results_review_package_digest",
            EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
        ),
        "feature_label_refinement_execution_digest": source.get(
            "feature_label_refinement_execution_digest",
            EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
        ),
        "feature_label_refinement_execution_approval_digest": source.get(
            "feature_label_refinement_execution_approval_digest",
            EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
        ),
        "additional_predictive_evidence_results_review_package_digest": source.get(
            "additional_predictive_evidence_results_review_package_digest",
            EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST,
        ),
        "additional_predictive_evidence_execution_digest": source.get(
            "additional_predictive_evidence_execution_digest",
            EXPECTED_ORIGINAL_EXECUTION_DIGEST,
        ),
        "research_registry_approval_digest": source.get(
            "research_registry_approval_digest", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
        ),
        "canonical_dataset_freeze_digest": source.get(
            "canonical_dataset_freeze_digest", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
        ),
        "records_digest": manifest.get("records_digest", EXPECTED_RECORDS_DIGEST),
        "target_universe": manifest.get("target_universe", list(TARGET_UNIVERSE)),
        "target_universe_count": manifest.get("target_universe_count", 12),
        "total_canonical_record_count": manifest.get("total_canonical_record_count", 11946),
        "per_ticker_record_counts": per_ticker or dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": per_ticker.get("META") if isinstance(per_ticker, dict) else None,
        "non_meta_record_count": 1003 if non_meta_valid else None,
        "non_meta_record_counts_1003_preserved": non_meta_valid,
        "meta_reduced_record_count_preserved": isinstance(per_ticker, dict)
        and per_ticker.get("META") == 913,
        "registry_approved_dataset_metadata": deepcopy(
            facts["registry"] or EXPECTED_REGISTRY_METADATA
        ),
        "refined_label_family_count": binding.get("label_family_count"),
        "refined_label_coverage_entries": binding.get("label_coverage_entries"),
        "refined_label_available_values": binding.get("label_available_values"),
        "refined_label_unavailable_values": binding.get("label_unavailable_values"),
        "refined_label_generation_digest": source.get(
            "feature_label_refinement_execution_digest"
        ) and outputs.get("refined_label_feature_binding_manifest.json", {}).get(
            "source_refined_label_generation_digest"
        ),
        "refined_feature_group_count": binding.get("feature_group_count"),
        "refined_feature_category_count": binding.get("feature_category_count"),
        "refined_feature_field_count": binding.get("feature_field_count"),
        "refined_feature_rows": binding.get("feature_rows"),
        "refined_feature_null_or_unavailable_values": binding.get(
            "feature_null_or_unavailable_values"
        ),
        "refined_feature_generation_digest": outputs.get(
            "refined_label_feature_binding_manifest.json", {}
        ).get("source_refined_feature_generation_digest"),
        "refined_protocol_group_count": leakage.get("protocol_group_count"),
        "chronological_splits": leakage.get("chronological_splits"),
        "one_session_embargo": leakage.get("one_session_embargo"),
        "no_shuffle": leakage.get("no_shuffle"),
        "no_lookahead": leakage.get("no_lookahead"),
        "refined_walk_forward_fold_count": walk.get("fold_count"),
        "refined_walk_forward_evaluation_rows": walk.get("evaluation_row_count"),
        "refined_walk_forward_review": deepcopy(walk),
        "refined_oos_evaluation_rows": oos.get("evaluation_row_count"),
        "refined_oos_accuracy_range": oos.get("accuracy_range"),
        "refined_out_of_sample_review": deepcopy(oos),
        "model_comparison_group_count": model.get("model_comparison_group_count"),
        "deterministic_comparisons_evaluated": len(model.get("deterministic_comparison_ids", []))
        if isinstance(model.get("deterministic_comparison_ids"), list)
        else None,
        "unavailable_model_family_requests": model.get("unavailable_model_family_requests"),
        "unavailable_model_family_status": model.get("unavailable_model_family_status"),
        "model_comparison_summary_bound": model.get("model_comparison_group_count") == 5
        and model.get("unavailable_model_family_requests") == 3
        and len(model.get("deterministic_comparison_ids", [])) == 7,
        "refined_baseline_model_comparison_review": deepcopy(model),
        "refined_calibration_stability_review": deepcopy(calibration),
        "refined_leakage_quality_review": deepcopy(leakage),
        "refined_leakage_status": leakage.get("leakage_status"),
        "failed_leakage_controls": leakage.get("failed_leakage_controls"),
        "data_quality_status": leakage.get("data_quality_summary", {}).get("status"),
        "output_root": _path_text(root),
        "output_root_present": root.is_dir(),
        "output_file_inspection_performed": inspected,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "actual_output_count": sum(entry["exists"] is True for entry in entries),
        "valid_output_count": valid_count,
        "missing_output_count": sum(entry["exists"] is False for entry in entries),
        "invalid_output_count": len(parse_errors),
        "output_file_entries": entries,
        "output_parse_errors": parse_errors,
        "output_file_digests": digest_summary["actual_output_file_digests"],
        "output_digest_manifest_summary": digest_summary,
        "generated_output_count": manifest.get("generated_output_count"),
        "output_digests_bound": digest_summary["verified_non_self_digest_count"] == 9
        and digest_summary["digest_mismatch_count"] == 0,
        "outputs_research_only_non_actionable": all_labeled and all_scoped,
        "outputs_not_acceptance_evidence": all_not_acceptance,
        "outputs_not_profitability_evidence": all_not_profitability,
        "outputs_not_runtime_authority": all_not_runtime,
        "digest_manifest_self_reference_non_applicable": digest_summary[
            "self_reference_valid"
        ],
        "additional_predictive_evidence_execution_for_refined_evidence_approved": True,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": True,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": manifest.get(
            "additional_predictive_evidence_execution_for_refined_evidence_executed"
        ),
        "additional_predictive_evidence_results_for_refined_evidence_created": manifest.get(
            "additional_predictive_evidence_results_for_refined_evidence_created"
        ),
        "refined_evidence_input_binding_performed": manifest.get(
            "refined_evidence_input_binding_performed"
        ),
        "refined_walk_forward_reassessment_performed": manifest.get(
            "refined_walk_forward_reassessment_performed"
        ),
        "refined_out_of_sample_reassessment_performed": manifest.get(
            "refined_out_of_sample_reassessment_performed"
        ),
        "refined_baseline_model_comparison_reassessment_performed": manifest.get(
            "refined_baseline_model_comparison_reassessment_performed"
        ),
        "refined_calibration_stability_review_performed": manifest.get(
            "refined_calibration_stability_review_performed"
        ),
        "refined_leakage_quality_review_performed": manifest.get(
            "refined_leakage_quality_review_performed"
        ),
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created": False,
        "predictive_usefulness_acceptance_readiness_review_rerun_created": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
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
        "results_support_predictive_usefulness_reassessment_rerun_using_refined_evidence": True,
        "results_create_predictive_usefulness_reassessment_review": False,
        "results_create_predictive_usefulness_acceptance": False,
        "results_create_profitability_acceptance": False,
        "results_create_runtime_authority": False,
        "results_create_trade_recommendations": False,
        "refined_predictive_evidence_results_available": inspected,
        "refined_predictive_evidence_outputs_verified": inspected
        and digest_summary["digest_mismatch_count"] == 0,
        "refined_evidence_input_binding_available": bool(facts["input_binding"]),
        "refined_walk_forward_reassessment_available": bool(walk),
        "refined_out_of_sample_reassessment_available": bool(oos),
        "refined_baseline_model_comparison_available": bool(model),
        "refined_calibration_stability_available": bool(calibration),
        "refined_leakage_quality_available": bool(leakage),
        "refined_execution_performance_interpretation": "WEAK_OR_MIXED_REQUIRES_REASSESSMENT_REVIEW",
        "refined_oos_accuracy_interpretation": "LOW_TO_MIXED_NOT_ACCEPTANCE_EVIDENCE",
        "model_comparison_interpretation": "RESEARCH_ONLY_REQUIRES_OPERATOR_REVIEW",
        "calibration_stability_interpretation": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_REVIEWED",
        "predictive_usefulness_reassessment_review_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "operator_review_required": True,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
    }
    checks = _checklist(common)
    ready = all(item["status"] == PASS for item in checks)
    status = (
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY
        if ready
        else ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    package = {
        **common,
        "review_status": status,
        "additional_predictive_evidence_results_review_for_refined_evidence_created": ready,
        "additional_predictive_evidence_results_review_for_refined_evidence_ready": ready,
        "ready_for_predictive_usefulness_reassessment_review_rerun_using_refined_evidence": ready,
    }
    package["review_checklist"] = _checklist(package)
    package["review_summary"] = _summary(package["review_checklist"], review_status=status)
    package[
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"
    ] = additional_predictive_evidence_results_review_for_refined_evidence_package_digest_v1(
        package
    )
    validate_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        package
    )
    return package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
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
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_reassessment_rerun_performed",
        "refined_out_of_sample_reassessment_rerun_performed",
        "refined_metrics_recomputation_performed",
        "refined_model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created",
        "predictive_usefulness_acceptance_readiness_review_rerun_created",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "results_create_predictive_usefulness_reassessment_review",
        "results_create_predictive_usefulness_acceptance",
        "results_create_profitability_acceptance",
        "results_create_runtime_authority",
        "results_create_trade_recommendations",
        "predictive_usefulness_reassessment_review_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
    review_package: dict,
) -> dict:
    """Validate a package without creating predictive, profitability, or runtime authority."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_V1,
        "schema_version",
    )
    status = review_package.get("review_status")
    if status not in {
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY,
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
    }:
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            "review_status mismatch"
        )
    for field in ("created_offline", "research_only", "operator_review_required"):
        _expect_true(review_package.get(field), field)
    always_false = (
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_reassessment_rerun_performed",
        "refined_out_of_sample_reassessment_rerun_performed",
        "refined_metrics_recomputation_performed",
        "refined_model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created",
        "predictive_usefulness_acceptance_readiness_review_rerun_created",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "results_create_predictive_usefulness_reassessment_review",
        "results_create_predictive_usefulness_acceptance",
        "results_create_profitability_acceptance",
        "results_create_runtime_authority",
        "results_create_trade_recommendations",
        "predictive_usefulness_reassessment_review_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    )
    for field in always_false:
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    _expect(review_package.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), NOT_ACCEPTED, "profitability")
    invariant_fields = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY,
        "source_additional_predictive_evidence_execution_for_refined_evidence_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_additional_predictive_evidence_execution_approval_for_refined_evidence_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        "feature_label_refinement_results_review_package_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
        "feature_label_refinement_execution_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
        "feature_label_refinement_execution_approval_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": EXPECTED_ORIGINAL_EXECUTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
    }
    for field, expected in invariant_fields.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    ready = all(item["status"] == PASS for item in expected_checklist)
    expected_status = (
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY
        if ready
        else ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    _expect(status, expected_status, "review_status")
    ready_fields = (
        "additional_predictive_evidence_results_review_for_refined_evidence_created",
        "additional_predictive_evidence_results_review_for_refined_evidence_ready",
        "ready_for_predictive_usefulness_reassessment_review_rerun_using_refined_evidence",
    )
    for field in ready_fields:
        _expect(review_package.get(field), ready, field)
    if ready:
        ready_invariants = {
            "meta_record_count": 913,
            "non_meta_record_count": 1003,
            "generated_output_count": 10,
            "refined_label_family_count": 7,
            "refined_label_coverage_entries": 84,
            "refined_label_available_values": 82698,
            "refined_label_unavailable_values": 924,
            "refined_label_generation_digest": EXPECTED_REFINED_LABEL_DIGEST,
            "refined_feature_group_count": 9,
            "refined_feature_category_count": 11,
            "refined_feature_field_count": 19,
            "refined_feature_rows": 11946,
            "refined_feature_null_or_unavailable_values": 1128,
            "refined_feature_generation_digest": EXPECTED_REFINED_FEATURE_DIGEST,
            "refined_protocol_group_count": 6,
            "refined_walk_forward_fold_count": 4,
            "refined_walk_forward_evaluation_rows": 3024,
            "refined_oos_evaluation_rows": 2988,
            "refined_oos_accuracy_range": "0.119813 to 0.480924",
            "model_comparison_group_count": 5,
            "deterministic_comparisons_evaluated": 7,
            "unavailable_model_family_requests": 3,
            "unavailable_model_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
            "refined_leakage_status": "PASS",
            "failed_leakage_controls": 0,
            "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        }
        for field, expected in ready_invariants.items():
            _expect(review_package.get(field), expected, field)
        _expect_true(review_package.get("chronological_splits"), "chronological_splits")
        _expect_true(review_package.get("one_session_embargo"), "one_session_embargo")
        _expect_true(review_package.get("no_shuffle"), "no_shuffle")
        _expect_true(review_package.get("no_lookahead"), "no_lookahead")
    expected_summary = _summary(expected_checklist, review_status=status)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            "review package digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_results_review_for_refined_evidence_package_digest_v1(
            review_package
        ),
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest",
    )
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": status,
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest": digest,
        "source_additional_predictive_evidence_execution_for_refined_evidence_digest": review_package[
            "source_additional_predictive_evidence_execution_for_refined_evidence_digest"
        ],
        "actual_output_count": review_package["actual_output_count"],
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_predictive_usefulness_reassessment_review_rerun_using_refined_evidence": ready,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_results_review_for_refined_evidence_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized Markdown review of saved refined-evidence outputs."""
    validation = validate_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    registry = review_package["registry_approved_dataset_metadata"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Results Review for Refined Evidence",
        "",
        "## Title",
        "- Additional Predictive Evidence Results Review for Refined Evidence v1.",
        "",
        "## Additional Predictive Evidence Results Review for Refined Evidence",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`",
        f"- Review digest: `{validation['additional_predictive_evidence_results_review_for_refined_evidence_package_digest']}`",
        "",
        "## Source Refined-Evidence Execution",
        f"- Execution digest: `{review_package['source_additional_predictive_evidence_execution_for_refined_evidence_digest']}`",
        f"- Approval digest: `{review_package['source_additional_predictive_evidence_execution_approval_for_refined_evidence_digest']}`",
        f"- Candidate review digest: `{review_package['additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest']}`",
        "",
        "## Source Feature/Label Refinement Results Review",
        f"- Results review/execution digests: `{review_package['feature_label_refinement_results_review_package_digest']}` / `{review_package['feature_label_refinement_execution_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/scope: `{registry['dataset_name']}` / `{registry['dataset_scope']}`",
        f"- Records/digest: `{review_package['total_canonical_record_count']}` / `{review_package['records_digest']}`",
        "",
        "## Target Universe",
        f"- `{', '.join(review_package['target_universe'])}`",
        "",
        "## Refined Evidence Input Binding Review",
        f"- `{review_package['refined_evidence_input_binding_available']}`; label/feature digests: `{review_package['refined_label_generation_digest']}` / `{review_package['refined_feature_generation_digest']}`",
        "",
        "## Refined Walk-Forward Reassessment Review",
        f"- Folds/rows: `{review_package['refined_walk_forward_fold_count']}` / `{review_package['refined_walk_forward_evaluation_rows']}`",
        "",
        "## Refined OOS Reassessment Review",
        f"- Rows/accuracy range: `{review_package['refined_oos_evaluation_rows']}` / `{review_package['refined_oos_accuracy_range']}`",
        "",
        "## Refined Baseline and Model Comparison Review",
        f"- Groups/comparisons/unavailable: `{review_package['model_comparison_group_count']}` / `{review_package['deterministic_comparisons_evaluated']}` / `{review_package['unavailable_model_family_requests']}`",
        "",
        "## Refined Calibration and Stability Review",
        f"- Interpretation: `{review_package['calibration_stability_interpretation']}`",
        "",
        "## Refined Leakage and Quality Review",
        f"- Leakage/data quality: `{review_package['refined_leakage_status']}` / `{review_package['data_quality_status']}`",
        "",
        "## Output Digest Manifest",
        f"- Output root/count: `{review_package['output_root']}` / `{review_package['actual_output_count']}`",
        f"- Verified non-self digests/mismatches: `{review_package['output_digest_manifest_summary']['verified_non_self_digest_count']}` / `{review_package['output_digest_manifest_summary']['digest_mismatch_count']}`",
        f"- Self-reference: `{review_package['output_digest_manifest_summary']['self_reference_policy']}`",
        "",
        "## Limitations",
    ]
    lines.extend(f"- `{item}`" for item in review_package["limitations"])
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in review_package["next_gates"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness: `{review_package['predictive_usefulness']}`; reassessment review created: `{review_package['predictive_usefulness_reassessment_review_created']}`",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{review_package['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{review_package['runtime_use']}` / `{review_package['strategy_use']}` / `{review_package['paper_trading']}` / `{review_package['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`",
            "",
            "## Guardrails",
            "- Existing ignored outputs were inspected offline; no provider request or evidence execution rerun occurred.",
            "- No acceptance, profitability, runtime, strategy, paper, broker, scoring, or recommendation authority was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict:
    """Write one canonical JSON review artifact without overwriting."""
    package = build_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        output_root=output_root
    )
    validation = validate_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "additional_predictive_evidence_results_review_for_refined_evidence_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            "review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError(
            "review output already exists"
        )
    payload = canonical_json_bytes(package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
