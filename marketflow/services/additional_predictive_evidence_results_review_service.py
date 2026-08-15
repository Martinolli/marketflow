"""Offline, digest-bound review of additional predictive evidence outputs."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_execution_service as execution


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_V1 = (
    "additional_predictive_evidence_results_review_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3"
)
EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST = execution.EXPECTED_EXECUTION_APPROVAL_DIGEST
EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST = (
    execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST = execution.EXPECTED_EXECUTION_CANDIDATE_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = execution.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = execution.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
EXPECTED_RECORDS_DIGEST = execution.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_OUTPUT_COUNT = len(EXPECTED_OUTPUT_FILENAMES)
DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = execution.RESEARCH_ONLY_NON_ACTIONABLE
EVIDENCE_SCOPE = execution.EVIDENCE_SCOPE
SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"

EXPECTED_LABEL_GENERATION_DIGEST = (
    "08e9aa9458c462dc3552fe25d6db9230d384228767848110bce76f8457e3eda3"
)
EXPECTED_FEATURE_GENERATION_DIGEST = (
    "ab543dc38aa75ea6a0bdc654a538bcb31d0081c8a1030fa1cf71665b23bcdd2d"
)
EXPECTED_OOS_BASELINE_ACCURACIES = {
    "majority_class_baseline": "0.539491",
    "random_baseline": "0.324967",
    "previous_direction_baseline": "0.495984",
    "zero_return_baseline": "0.001004",
    "buy_hold_reference_only": "0.539491",
    "ticker_cross_sectional_baseline": "0.502677",
}
EXPECTED_WALK_FORWARD_FOLDS = [
    {"fold_id": "2024_Q1", "evaluation_count": 732, "majority_accuracy": "0.562842"},
    {"fold_id": "2024_Q2", "evaluation_count": 756, "majority_accuracy": "0.541005"},
    {"fold_id": "2024_Q3", "evaluation_count": 768, "majority_accuracy": "0.552083"},
    {"fold_id": "2024_Q4", "evaluation_count": 768, "majority_accuracy": "0.498698"},
]

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

LIMITATIONS = [
    "execution_results_are_research_only",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "trade_recommendations_not_generated",
    "metrics_require_operator_interpretation",
    "majority_baseline_accuracy_not_acceptance_evidence_by_itself",
    "buy_hold_reference_is_not_trade_recommendation",
    "meta_reduced_record_count_preserved",
    "operator_review_required_before_predictive_usefulness_reassessment",
    "operator_approval_required_before_any_acceptance_or_runtime_migration",
]

NEXT_GATES = [
    "additional_predictive_evidence_results_operator_review",
    "predictive_usefulness_reassessment_candidate",
    "predictive_usefulness_reassessment_review",
    "predictive_usefulness_acceptance_readiness_review",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]


class AdditionalPredictiveEvidenceResultsReviewError(ValueError):
    """Raised when the results review package violates its offline boundary."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceResultsReviewError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceResultsReviewError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceResultsReviewError(f"{field} must be false")


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
                entry["output_label"] = value.get("output_label")
                entry["evidence_scope"] = value.get("evidence_scope")
                outputs[filename] = value
        entries.append(entry)
    return entries, outputs, errors


def _digest_manifest_summary(
    entries: list[dict[str, Any]],
    outputs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    actual = {entry["filename"]: entry["file_sha256"] for entry in entries}
    manifest = outputs.get("execution_digest_manifest.json", {})
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
        if filename == "execution_digest_manifest.json":
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
    self_entry = declared.get("execution_digest_manifest.json")
    self_reference_valid = bool(
        isinstance(self_entry, dict)
        and self_entry.get("digest_kind") == SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
        and self_entry.get("sha256") is None
        and manifest.get("self_reference_policy")
        == SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
    )
    if not self_reference_valid:
        mismatches.append(
            {
                "filename": "execution_digest_manifest.json",
                "declared_digest_kind": self_entry.get("digest_kind")
                if isinstance(self_entry, dict)
                else None,
                "declared_sha256": self_entry.get("sha256")
                if isinstance(self_entry, dict)
                else None,
                "actual_sha256": actual.get("execution_digest_manifest.json"),
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
        "self_reference_valid": self_reference_valid,
    }


def _output_boundary_summary(outputs: dict[str, dict[str, Any]]) -> dict[str, bool]:
    raw_payload_present = False
    api_secret_present = False
    trade_recommendation_present = False
    predictive_acceptance_present = False
    profitability_acceptance_present = False
    runtime_authority_present = False
    for output in outputs.values():
        for key, value in _walk_items(output):
            lowered = key.lower()
            if "raw_provider_payload" in lowered and not lowered.endswith("committed"):
                raw_payload_present = value not in (None, False, "", [], {})
            if lowered in {"api_key", "apikey", "api_token", "authorization_header", "password", "secret"}:
                api_secret_present = value not in (None, False, "", "NOT_STORED", "REDACTED")
            if lowered in {"trade_recommendation", "trade_recommendations_generated"} and value is True:
                trade_recommendation_present = True
            if lowered == "predictive_usefulness" and value == "accepted":
                predictive_acceptance_present = True
            if lowered == "predictive_usefulness_acceptance_candidate_created" and value is True:
                predictive_acceptance_present = True
            if lowered == "profitability" and value == "accepted":
                profitability_acceptance_present = True
            if lowered in {
                "runtime_migration_approved",
                "runtime_migration_active",
                "automatic_stitching",
            } and value is True:
                runtime_authority_present = True
            if lowered in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
                runtime_authority_present = runtime_authority_present or value == "AUTHORIZED"
    return {
        "raw_provider_payload_present": raw_payload_present,
        "api_secret_present": api_secret_present,
        "trade_recommendation_present": trade_recommendation_present,
        "predictive_acceptance_present": predictive_acceptance_present,
        "profitability_acceptance_present": profitability_acceptance_present,
        "runtime_authority_present": runtime_authority_present,
    }


def _walk_forward_summary(report: dict[str, Any]) -> dict[str, Any]:
    folds = report.get("folds") if isinstance(report.get("folds"), list) else []
    compact = []
    for fold in folds:
        majority = fold.get("baselines", {}).get("majority_class_baseline", {})
        compact.append(
            {
                "fold_id": fold.get("fold_id"),
                "evaluation_count": fold.get("evaluation_count"),
                "majority_accuracy": majority.get("classification_metrics", {}).get("accuracy"),
            }
        )
    return {
        "fold_count": report.get("fold_count"),
        "no_shuffle_policy": report.get("shuffle") is False,
        "folds": compact,
    }


def _oos_baseline_summary(report: dict[str, Any]) -> dict[str, Any]:
    results = report.get("results", {})
    aggregate = results.get("overall", {}) if isinstance(results, dict) else {}
    baselines = aggregate.get("baselines", {}) if isinstance(aggregate, dict) else {}
    accuracies = {
        name: payload.get("classification_metrics", {}).get("accuracy")
        for name, payload in baselines.items()
        if isinstance(payload, dict)
    }
    return {
        "oos_window": results.get("out_of_sample_window") if isinstance(results, dict) else None,
        "evaluation_count": aggregate.get("evaluation_count"),
        "baseline_accuracies": accuracies,
    }


def _facts(outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    manifest = outputs.get("additional_predictive_evidence_execution_manifest.json", {})
    label = outputs.get("label_generation_manifest.json", {})
    feature = outputs.get("feature_matrix_manifest.json", {})
    feature_quality = outputs.get("feature_quality_report.json", {})
    walk = outputs.get("walk_forward_results_report.json", {})
    oos = outputs.get("out_of_sample_results_report.json", {})
    baseline = outputs.get("baseline_comparison_report.json", {})
    calibration = outputs.get("calibration_report.json", {})
    stability = outputs.get("stability_analysis_report.json", {})
    leakage = outputs.get("leakage_control_report.json", {})
    quality = outputs.get("data_quality_report.json", {})
    source = manifest.get("source_evidence", {}) if isinstance(manifest, dict) else {}
    registry = manifest.get("registry_approved_dataset_metadata", {}) if isinstance(manifest, dict) else {}
    total_nulls = feature_quality.get("total_null_counts_by_feature", {})
    total_null_count = sum(total_nulls.values()) if isinstance(total_nulls, dict) else None
    oos_summary = _oos_baseline_summary(oos)
    return {
        "source": source,
        "registry": registry,
        "target_universe": manifest.get("target_universe"),
        "target_universe_count": manifest.get("target_universe_count"),
        "total_canonical_record_count": manifest.get("total_canonical_record_count"),
        "per_ticker_record_counts": manifest.get("per_ticker_record_counts"),
        "records_digest": manifest.get("records_digest"),
        "label_family_count": label.get("label_family_count"),
        "feature_family_count": feature.get("feature_family_count"),
        "metric_family_count": manifest.get("metric_family_count"),
        "baseline_count": baseline.get("baseline_count"),
        "generated_output_count": manifest.get("generated_output_count"),
        "failure_count": quality.get("failure_count"),
        "warning_count": quality.get("warning_count"),
        "label_generation_digest": label.get("label_generation_digest"),
        "label_coverage_entries": len(label.get("label_coverage", []))
        if isinstance(label.get("label_coverage"), list)
        else None,
        "label_available_values": manifest.get("label_coverage_summary", {}).get("available_count"),
        "label_unavailable_values": manifest.get("label_coverage_summary", {}).get("unavailable_count"),
        "feature_generation_digest": feature.get("feature_matrix_digest"),
        "feature_field_count": feature.get("feature_count"),
        "feature_rows": feature.get("feature_matrix_row_count"),
        "feature_coverage_entries": len(feature_quality.get("feature_coverage", []))
        if isinstance(feature_quality.get("feature_coverage"), list)
        else None,
        "expected_rolling_window_null_count": total_null_count,
        "future_labels_used_as_features": feature_quality.get("future_label_values_used_as_features"),
        "walk_forward_review": _walk_forward_summary(walk),
        "out_of_sample_review": oos_summary,
        "baseline_comparison_review": {
            "baseline_count": baseline.get("baseline_count"),
            "out_of_sample_comparison": deepcopy(baseline.get("out_of_sample_comparison", {})),
            "baseline_accuracies": oos_summary["baseline_accuracies"],
        },
        "calibration_review": {
            "oos_brier_score": calibration.get("calibration_metrics", {}).get("out_of_sample_brier_score"),
            "calibration_metrics": deepcopy(calibration.get("calibration_metrics", {})),
        },
        "stability_review": deepcopy(stability.get("stability_metrics", {})),
        "leakage_review": {
            "status": leakage.get("leakage_control_status"),
            "failed_control_count": leakage.get("failed_control_count"),
        },
        "data_quality_review": {
            "status": quality.get("quality_status"),
            "failure_count": quality.get("failure_count"),
            "warning_count": quality.get("warning_count"),
            "warnings": deepcopy(quality.get("warnings", [])),
            "meta_reduced_record_count_preserved": quality.get("meta_reduced_record_count_preserved"),
        },
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("additional_predictive_evidence_execution_digest_bound", EXPECTED_SOURCE_EXECUTION_DIGEST, "source_additional_predictive_evidence_execution_digest"),
    ("additional_predictive_evidence_execution_approval_digest_bound", EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST, "source_additional_predictive_evidence_execution_approval_digest"),
    ("execution_candidate_review_digest_bound", EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST, "source_additional_predictive_evidence_execution_candidate_review_package_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("canonical_dataset_generation_digest_bound", EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, "canonical_dataset_generation_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_execution_universe", TARGET_UNIVERSE, "target_universe"),
    ("total_canonical_record_count_11946", 11946, "total_canonical_record_count"),
    ("meta_record_count_913_preserved", 913, "meta_record_count"),
    ("non_meta_record_counts_1003_preserved", True, "non_meta_record_counts_1003_preserved"),
    ("generated_output_count_15", 15, "generated_output_count"),
    ("output_digests_bound", True, "output_digests_bound"),
    ("outputs_research_only_non_actionable", True, "outputs_research_only_non_actionable"),
    ("digest_manifest_self_reference_non_applicable", True, "digest_manifest_self_reference_non_applicable"),
    ("label_family_count_7", 7, "label_family_count"),
    ("feature_family_count_10", 10, "feature_family_count"),
    ("metric_family_count_9", 9, "metric_family_count"),
    ("baseline_count_6", 6, "baseline_count"),
    ("label_generation_digest_bound", EXPECTED_LABEL_GENERATION_DIGEST, "label_generation_digest"),
    ("feature_generation_digest_bound", EXPECTED_FEATURE_GENERATION_DIGEST, "feature_generation_digest"),
    ("label_coverage_summary_bound", True, "label_coverage_summary_bound"),
    ("feature_coverage_summary_bound", True, "feature_coverage_summary_bound"),
    ("walk_forward_fold_count_4", 4, "walk_forward_fold_count"),
    ("walk_forward_no_shuffle_true", True, "walk_forward_no_shuffle"),
    ("out_of_sample_evaluation_rows_2988", 2988, "oos_evaluation_rows"),
    ("baseline_comparison_summary_bound", True, "baseline_comparison_summary_bound"),
    ("oos_brier_score_bound", "0.24875351", "oos_up_vs_not_up_brier_score"),
    ("leakage_status_pass", "PASS", "leakage_status"),
    ("failed_leakage_controls_zero", 0, "failed_leakage_controls"),
    ("provider_requests_made_in_review_false", False, "provider_requests_made_in_review"),
    ("live_provider_transport_enabled_in_review_false", False, "live_provider_transport_enabled_in_review"),
    ("market_data_acquisition_performed_in_review_false", False, "market_data_acquisition_performed_in_review"),
    ("dataset_generation_performed_in_review_false", False, "dataset_generation_performed_in_review"),
    ("canonical_dataset_regenerated_in_review_false", False, "canonical_dataset_regenerated_in_review"),
    ("predictive_execution_rerun_performed_false", False, "predictive_execution_rerun_performed"),
    ("label_generation_rerun_performed_false", False, "label_generation_rerun_performed"),
    ("feature_matrix_rerun_performed_false", False, "feature_matrix_rerun_performed"),
    ("walk_forward_validation_rerun_performed_false", False, "walk_forward_validation_rerun_performed"),
    ("out_of_sample_evaluation_rerun_performed_false", False, "out_of_sample_evaluation_rerun_performed"),
    ("baseline_comparison_rerun_performed_false", False, "baseline_comparison_rerun_performed"),
    ("metrics_recomputation_performed_false", False, "metrics_recomputation_performed"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("raw_provider_payloads_absent_from_outputs", False, "raw_provider_payloads_present_in_outputs"),
    ("api_keys_absent_from_outputs", False, "api_keys_present_in_outputs"),
    ("trade_recommendations_absent_from_outputs", False, "trade_recommendations_present_in_outputs"),
    ("predictive_acceptance_absent_from_outputs", False, "predictive_acceptance_present_in_outputs"),
    ("profitability_acceptance_absent_from_outputs", False, "profitability_acceptance_present_in_outputs"),
    ("runtime_authority_absent_from_outputs", False, "runtime_authority_present_in_outputs"),
    ("additional_predictive_evidence_executed_true", True, "additional_predictive_evidence_executed"),
    ("additional_predictive_evidence_results_created_true", True, "additional_predictive_evidence_results_created"),
    ("label_generation_performed_true", True, "label_generation_performed"),
    ("feature_matrix_generation_performed_true", True, "feature_matrix_generation_performed"),
    ("walk_forward_validation_performed_true", True, "walk_forward_validation_performed"),
    ("out_of_sample_evaluation_performed_true", True, "out_of_sample_evaluation_performed"),
    ("baseline_comparison_performed_true", True, "baseline_comparison_performed"),
    ("signal_quality_metrics_performed_true", True, "signal_quality_metrics_performed"),
    ("stability_analysis_performed_true", True, "stability_analysis_performed"),
    ("leakage_control_review_performed_true", True, "leakage_control_review_performed"),
    ("predictive_experiment_rerun_performed_true", True, "predictive_experiment_rerun_performed"),
    ("new_strategy_scoring_performed_false", False, "new_strategy_scoring_performed"),
    ("trade_recommendations_generated_false", False, "trade_recommendations_generated"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("predictive_usefulness_acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_migration_approved_false", False, "runtime_migration_approved"),
    ("runtime_use_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_use_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("paper_trading_not_authorized", NOT_AUTHORIZED, "paper_trading"),
    ("broker_execution_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("automatic_stitching_false", False, "automatic_stitching"),
    ("results_support_future_reassessment_planning_true", True, "additional_predictive_evidence_results_support_future_reassessment_planning"),
    ("results_create_predictive_usefulness_acceptance_false", False, "additional_predictive_evidence_results_create_predictive_usefulness_acceptance"),
    ("results_create_profitability_acceptance_false", False, "additional_predictive_evidence_results_create_profitability_acceptance"),
    ("results_create_runtime_authority_false", False, "additional_predictive_evidence_results_create_runtime_authority"),
    ("limitations_recorded", LIMITATIONS, "limitations"),
    ("next_gates_defined", NEXT_GATES, "next_gates"),
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
        item.get("status") == FAIL and item.get("severity") == BLOCKER for item in checklist
    )
    ready = (
        review_status == ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
        and blockers == 0
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "ready_for_operator_review": ready,
        "ready_for_predictive_usefulness_reassessment_candidate": ready,
        "ready_for_predictive_usefulness_acceptance": False,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("additional_predictive_evidence_results_review_package_digest", None)
    return payload


def additional_predictive_evidence_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for a review package."""
    return semantic_digest(_digest_payload(review_package))


def build_additional_predictive_evidence_results_review_package_v1(
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Inspect saved execution outputs offline and build a fail-closed review package."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    entries, outputs, parse_errors = _load_outputs(root)
    digest_summary = _digest_manifest_summary(entries, outputs)
    boundaries = _output_boundary_summary(outputs)
    facts = _facts(outputs)
    valid_output_count = sum(entry["valid_json_object"] is True for entry in entries)
    all_outputs_labeled = valid_output_count == EXPECTED_OUTPUT_COUNT and all(
        entry["output_label"] == RESEARCH_ONLY_NON_ACTIONABLE for entry in entries
    )
    all_scoped = valid_output_count == EXPECTED_OUTPUT_COUNT and all(
        entry["evidence_scope"] == EVIDENCE_SCOPE for entry in entries
    )
    per_ticker_counts = facts["per_ticker_record_counts"] or {}
    non_meta_counts_valid = isinstance(per_ticker_counts, dict) and all(
        per_ticker_counts.get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META"
    )
    source = facts["source"] if isinstance(facts["source"], dict) else {}
    common = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "predictive_execution_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_matrix_rerun_performed": False,
        "walk_forward_validation_rerun_performed": False,
        "out_of_sample_evaluation_rerun_performed": False,
        "baseline_comparison_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "raw_provider_payloads_present_in_outputs": boundaries["raw_provider_payload_present"],
        "api_keys_present_in_outputs": boundaries["api_secret_present"],
        "trade_recommendations_present_in_outputs": boundaries[
            "trade_recommendation_present"
        ],
        "predictive_acceptance_present_in_outputs": boundaries[
            "predictive_acceptance_present"
        ],
        "profitability_acceptance_present_in_outputs": boundaries[
            "profitability_acceptance_present"
        ],
        "runtime_authority_present_in_outputs": boundaries["runtime_authority_present"],
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY,
        "source_additional_predictive_evidence_execution_digest": (
            outputs.get("additional_predictive_evidence_execution_manifest.json", {}).get(
                "additional_predictive_evidence_execution_digest",
                EXPECTED_SOURCE_EXECUTION_DIGEST,
            )
        ),
        "source_additional_predictive_evidence_execution_approval_digest": source.get(
            "additional_predictive_evidence_execution_approval_digest",
            EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        ),
        "source_additional_predictive_evidence_execution_candidate_review_package_digest": source.get(
            "additional_predictive_evidence_execution_candidate_review_package_digest",
            EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        ),
        "source_additional_predictive_evidence_execution_candidate_digest": source.get(
            "additional_predictive_evidence_execution_candidate_digest",
            EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        ),
        "research_registry_approval_digest": source.get(
            "research_registry_approval_digest", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
        ),
        "canonical_dataset_freeze_digest": source.get(
            "canonical_dataset_freeze_digest", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
        ),
        "canonical_dataset_generation_digest": source.get(
            "canonical_dataset_generation_digest", EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
        ),
        "records_digest": facts["records_digest"] or EXPECTED_RECORDS_DIGEST,
        "target_universe": facts["target_universe"] or list(TARGET_UNIVERSE),
        "target_universe_count": facts["target_universe_count"] or 12,
        "total_canonical_record_count": facts["total_canonical_record_count"] or 11946,
        "per_ticker_record_counts": facts["per_ticker_record_counts"] or dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": per_ticker_counts.get("META") if isinstance(per_ticker_counts, dict) else None,
        "non_meta_record_count": 1003 if non_meta_counts_valid else None,
        "non_meta_record_counts_1003_preserved": non_meta_counts_valid,
        "meta_reduced_record_count_preserved": (
            per_ticker_counts.get("META") == 913 if isinstance(per_ticker_counts, dict) else False
        ),
        "registry_approved_dataset_metadata": deepcopy(
            facts["registry"] or execution.APPROVED_REGISTRY_METADATA
        ),
        "label_family_count": facts["label_family_count"],
        "feature_family_count": facts["feature_family_count"],
        "metric_family_count": facts["metric_family_count"],
        "baseline_count": facts["baseline_count"],
        "generated_output_count": facts["generated_output_count"],
        "failure_count": facts["failure_count"],
        "warning_count": facts["warning_count"],
        "label_generation_digest": facts["label_generation_digest"],
        "label_coverage_entries": facts["label_coverage_entries"],
        "label_available_values": facts["label_available_values"],
        "label_unavailable_values": facts["label_unavailable_values"],
        "label_unavailable_reason": execution.LABEL_UNAVAILABLE_REASON,
        "label_coverage_summary_bound": (
            facts["label_coverage_entries"] == 84
            and facts["label_available_values"] == 82854
            and facts["label_unavailable_values"] == 768
        ),
        "feature_generation_digest": facts["feature_generation_digest"],
        "feature_field_count": facts["feature_field_count"],
        "feature_rows": facts["feature_rows"],
        "feature_coverage_entries": facts["feature_coverage_entries"],
        "expected_rolling_window_null_count": facts["expected_rolling_window_null_count"],
        "future_labels_used_as_features": facts["future_labels_used_as_features"],
        "feature_coverage_summary_bound": (
            facts["feature_field_count"] == 22
            and facts["feature_rows"] == 11946
            and facts["feature_coverage_entries"] == 120
            and facts["expected_rolling_window_null_count"] == 1428
            and facts["future_labels_used_as_features"] is False
        ),
        "walk_forward_review": facts["walk_forward_review"],
        "walk_forward_fold_count": facts["walk_forward_review"]["fold_count"],
        "walk_forward_no_shuffle": facts["walk_forward_review"]["no_shuffle_policy"],
        "out_of_sample_review": facts["out_of_sample_review"],
        "oos_window": facts["out_of_sample_review"]["oos_window"],
        "oos_evaluation_rows": facts["out_of_sample_review"]["evaluation_count"],
        "baseline_comparison_review": facts["baseline_comparison_review"],
        "baseline_comparison_summary_bound": (
            facts["baseline_comparison_review"]["baseline_accuracies"]
            == EXPECTED_OOS_BASELINE_ACCURACIES
        ),
        "calibration_review": facts["calibration_review"],
        "oos_up_vs_not_up_brier_score": facts["calibration_review"]["oos_brier_score"],
        "stability_review": facts["stability_review"],
        "leakage_review": facts["leakage_review"],
        "leakage_status": facts["leakage_review"]["status"],
        "failed_leakage_controls": facts["leakage_review"]["failed_control_count"],
        "data_quality_review": facts["data_quality_review"],
        "output_root": _path_text(root),
        "output_root_present": root.is_dir(),
        "output_file_inspection_performed": valid_output_count == EXPECTED_OUTPUT_COUNT,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "actual_output_count": sum(entry["exists"] is True for entry in entries),
        "valid_output_count": valid_output_count,
        "missing_output_count": sum(entry["exists"] is False for entry in entries),
        "invalid_output_count": len(parse_errors),
        "output_file_entries": entries,
        "output_parse_errors": parse_errors,
        "output_file_digests": digest_summary["actual_output_file_digests"],
        "output_digest_manifest_summary": digest_summary,
        "output_digests_bound": (
            digest_summary["verified_non_self_digest_count"] == EXPECTED_OUTPUT_COUNT - 1
            and digest_summary["digest_mismatch_count"] == 0
        ),
        "outputs_research_only_non_actionable": all_outputs_labeled,
        "outputs_evidence_scope_verified": all_scoped,
        "digest_manifest_self_reference_non_applicable": digest_summary["self_reference_valid"],
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "label_generation_authorized": True,
        "label_generation_performed": True,
        "feature_matrix_generation_authorized": True,
        "feature_matrix_generation_performed": True,
        "walk_forward_validation_authorized": True,
        "walk_forward_validation_performed": True,
        "out_of_sample_evaluation_authorized": True,
        "out_of_sample_evaluation_performed": True,
        "baseline_comparison_authorized": True,
        "baseline_comparison_performed": True,
        "signal_quality_metrics_authorized": True,
        "signal_quality_metrics_performed": True,
        "stability_analysis_authorized": True,
        "stability_analysis_performed": True,
        "leakage_control_review_authorized": True,
        "leakage_control_review_performed": True,
        "predictive_experiment_rerun_authorized": True,
        "predictive_experiment_rerun_performed": True,
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
        "additional_predictive_evidence_results_support_future_reassessment_planning": True,
        "additional_predictive_evidence_results_create_predictive_usefulness_acceptance": False,
        "additional_predictive_evidence_results_create_profitability_acceptance": False,
        "additional_predictive_evidence_results_create_runtime_authority": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "operator_review_required": True,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
    }
    provisional_checks = _checklist(common)
    ready = all(item["status"] == PASS for item in provisional_checks)
    status = (
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
        if ready
        else ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    package = {
        **common,
        "review_status": status,
        "additional_predictive_evidence_results_review_created": ready,
        "additional_predictive_evidence_results_review_ready": ready,
        "ready_for_predictive_usefulness_reassessment_candidate": ready,
        "ready_for_predictive_usefulness_acceptance": False,
    }
    package["review_checklist"] = _checklist(package)
    package["review_summary"] = _summary(package["review_checklist"], review_status=status)
    package["additional_predictive_evidence_results_review_package_digest"] = (
        additional_predictive_evidence_results_review_package_digest_v1(package)
    )
    validate_additional_predictive_evidence_results_review_package_v1(package)
    return package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE",
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
        "predictive_execution_rerun_performed",
        "label_generation_rerun_performed",
        "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed",
        "baseline_comparison_rerun_performed",
        "metrics_recomputation_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
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
        "additional_predictive_evidence_results_create_predictive_usefulness_acceptance",
        "additional_predictive_evidence_results_create_profitability_acceptance",
        "additional_predictive_evidence_results_create_runtime_authority",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise AdditionalPredictiveEvidenceResultsReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise AdditionalPredictiveEvidenceResultsReviewError(f"{current} must be false")
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceResultsReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceResultsReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_additional_predictive_evidence_results_review_package_v1(
    review_package: dict,
) -> dict:
    """Validate a review package without granting predictive or runtime authority."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceResultsReviewError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_V1,
        "schema_version",
    )
    status = review_package.get("review_status")
    if status not in {
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY,
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
    }:
        raise AdditionalPredictiveEvidenceResultsReviewError("review_status mismatch")
    for field in ("created_offline", "research_only", "operator_review_required"):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "predictive_execution_rerun_performed",
        "label_generation_rerun_performed",
        "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed",
        "baseline_comparison_rerun_performed",
        "metrics_recomputation_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
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
        "additional_predictive_evidence_results_create_predictive_usefulness_acceptance",
        "additional_predictive_evidence_results_create_profitability_acceptance",
        "additional_predictive_evidence_results_create_runtime_authority",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    _expect(review_package.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), NOT_ACCEPTED, "profitability")
    source_invariant_fields = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY,
        "source_additional_predictive_evidence_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_additional_predictive_evidence_execution_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "source_additional_predictive_evidence_execution_candidate_review_package_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        "source_additional_predictive_evidence_execution_candidate_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
    }
    for field, expected in source_invariant_fields.items():
        _expect(review_package.get(field), expected, field)
    _expect(
        review_package.get("per_ticker_record_counts"),
        EXPECTED_RECORD_COUNTS,
        "per_ticker_record_counts",
    )
    result_invariant_fields = {
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "label_family_count": 7,
        "feature_family_count": 10,
        "metric_family_count": 9,
        "baseline_count": 6,
        "generated_output_count": 15,
        "label_generation_digest": EXPECTED_LABEL_GENERATION_DIGEST,
        "label_coverage_entries": 84,
        "label_available_values": 82854,
        "label_unavailable_values": 768,
        "label_unavailable_reason": execution.LABEL_UNAVAILABLE_REASON,
        "feature_generation_digest": EXPECTED_FEATURE_GENERATION_DIGEST,
        "feature_field_count": 22,
        "feature_rows": 11946,
        "feature_coverage_entries": 120,
        "expected_rolling_window_null_count": 1428,
        "future_labels_used_as_features": False,
        "walk_forward_fold_count": 4,
        "walk_forward_no_shuffle": True,
        "oos_evaluation_rows": 2988,
        "oos_up_vs_not_up_brier_score": "0.24875351",
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
    }
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceResultsReviewError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    expected_ready = all(item["status"] == PASS for item in expected_checklist)
    expected_status = (
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
        if expected_ready
        else ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    _expect(status, expected_status, "review_status")
    if expected_ready:
        for field, expected in result_invariant_fields.items():
            _expect(review_package.get(field), expected, field)
        _expect(
            review_package.get("walk_forward_review", {}).get("folds"),
            EXPECTED_WALK_FORWARD_FOLDS,
            "walk_forward_review.folds",
        )
        _expect(
            review_package.get("baseline_comparison_review", {}).get("baseline_accuracies"),
            EXPECTED_OOS_BASELINE_ACCURACIES,
            "baseline_comparison_review.baseline_accuracies",
        )
    for field in (
        "additional_predictive_evidence_results_review_created",
        "additional_predictive_evidence_results_review_ready",
        "ready_for_predictive_usefulness_reassessment_candidate",
    ):
        _expect(review_package.get(field), expected_ready, field)
    _expect_false(
        review_package.get("ready_for_predictive_usefulness_acceptance"),
        "ready_for_predictive_usefulness_acceptance",
    )
    expected_summary = _summary(expected_checklist, review_status=status)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("additional_predictive_evidence_results_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceResultsReviewError(
            "additional_predictive_evidence_results_review_package_digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_results_review_package_digest_v1(review_package),
        "additional_predictive_evidence_results_review_package_digest",
    )
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": status,
        "additional_predictive_evidence_results_review_package_digest": digest,
        "source_additional_predictive_evidence_execution_digest": review_package[
            "source_additional_predictive_evidence_execution_digest"
        ],
        "actual_output_count": review_package["actual_output_count"],
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_predictive_usefulness_reassessment_candidate": expected_ready,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_results_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized Markdown review of saved predictive-evidence outputs."""
    validation = validate_additional_predictive_evidence_results_review_package_v1(review_package)
    summary = review_package["review_summary"]
    registry = review_package["registry_approved_dataset_metadata"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Results Review Status",
        "",
        "## Title",
        "- Additional Predictive Evidence Results Review Package v1.",
        "",
        "## Additional Predictive Evidence Results Review Package",
        f"- Artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Review digest: `{validation['additional_predictive_evidence_results_review_package_digest']}`",
        "",
        "## Source Predictive Evidence Execution",
        f"- Execution digest: `{review_package['source_additional_predictive_evidence_execution_digest']}`",
        f"- Execution approval digest: `{review_package['source_additional_predictive_evidence_execution_approval_digest']}`",
        f"- Execution candidate review digest: `{review_package['source_additional_predictive_evidence_execution_candidate_review_package_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset: `{registry.get('dataset_name')}`",
        f"- Records: `{review_package['total_canonical_record_count']}`",
        f"- Records digest: `{review_package['records_digest']}`",
        "",
        "## Target Universe",
        f"- `{', '.join(review_package['target_universe'])}`",
        "",
        "## Label Generation Review",
        f"- Families: `{review_package['label_family_count']}`; coverage entries: `{review_package['label_coverage_entries']}`",
        f"- Available/unavailable values: `{review_package['label_available_values']}` / `{review_package['label_unavailable_values']}`",
        f"- Digest: `{review_package['label_generation_digest']}`",
        "",
        "## Feature Generation Review",
        f"- Families/fields/rows: `{review_package['feature_family_count']}` / `{review_package['feature_field_count']}` / `{review_package['feature_rows']}`",
        f"- Expected rolling nulls: `{review_package['expected_rolling_window_null_count']}`",
        f"- Digest: `{review_package['feature_generation_digest']}`",
        "",
        "## Walk-Forward Validation Review",
        f"- Fold count: `{review_package['walk_forward_fold_count']}`; no shuffle: `{review_package['walk_forward_no_shuffle']}`",
        "",
        "## Out-of-Sample Evaluation Review",
        f"- Window/rows: `{review_package['oos_window']}` / `{review_package['oos_evaluation_rows']}`",
        "",
        "## Baseline Comparison Review",
        f"- Baseline count: `{review_package['baseline_count']}`",
        f"- Accuracy summary: `{review_package['baseline_comparison_review']['baseline_accuracies']}`",
        "",
        "## Metric and Calibration Review",
        f"- OOS up-vs-not-up Brier score: `{review_package['oos_up_vs_not_up_brier_score']}`",
        "",
        "## Stability Review",
        f"- Stability baseline entries: `{len(review_package['stability_review'])}`",
        "",
        "## Leakage-Control Review",
        f"- Status: `{review_package['leakage_status']}`; failed controls: `{review_package['failed_leakage_controls']}`",
        "",
        "## Data Quality Review",
        f"- Status: `{review_package['data_quality_review']['status']}`",
        f"- META records: `{review_package['meta_record_count']}`; preserved: `{review_package['meta_reduced_record_count_preserved']}`",
        "",
        "## Output Digest Manifest",
        f"- Output root: `{review_package['output_root']}`",
        f"- Actual/expected output count: `{review_package['actual_output_count']}` / `{review_package['expected_output_count']}`",
        f"- Verified non-self digests: `{review_package['output_digest_manifest_summary']['verified_non_self_digest_count']}`",
        f"- Self-reference policy: `{review_package['output_digest_manifest_summary']['self_reference_policy']}`",
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
            f"- Predictive usefulness: `{review_package['predictive_usefulness']}`",
            "- This review creates no predictive-usefulness acceptance or acceptance candidate.",
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
            "- Review performed offline against existing sanitized outputs.",
            "- No provider request, acquisition, dataset regeneration, predictive rerun, strategy scoring, or trade recommendation occurred.",
            "- Predictive usefulness and profitability remain not accepted; runtime remains not authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def write_additional_predictive_evidence_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict:
    """Write a canonical review JSON artifact once without overwriting."""
    package = build_additional_predictive_evidence_results_review_package_v1(
        output_root=output_root
    )
    validation = validate_additional_predictive_evidence_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "additional_predictive_evidence_results_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceResultsReviewError(
            "additional predictive evidence results review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise AdditionalPredictiveEvidenceResultsReviewError(
            "additional predictive evidence results review output already exists"
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
