"""Offline execution of approved predictive research using reviewed refined evidence."""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import (
    additional_predictive_evidence_execution_approval_for_refined_evidence_service as approval,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE"
)
ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_V1 = (
    "additional_predictive_evidence_executed_for_refined_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_REFINED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_REFINED_EVIDENCE"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_VALID"
)

DEFAULT_SOURCE_ROOT = (
    Path(".marketflow") / "feature_label_refinement" / "expanded_universe_v1"
)
DEFAULT_CANONICAL_SOURCE_ROOT = (
    Path(".marketflow") / "canonical_datasets" / "expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = (
    Path(".marketflow")
    / "additional_predictive_evidence_refined"
    / "expanded_universe_v1"
)
DEFAULT_BRANCH = "feature/additional-predictive-evidence-execution-refined-evidence-v1"
DEFAULT_BASE_COMMIT = "96a4b83720fad948fa9664f33f66fcf18d1b85a8"

EXPECTED_EXECUTION_APPROVAL_DIGEST = (
    "5ad7b3b8df3156ab6b35b9490dcd4ae05bda3d1a7786212481b78d549103a8dd"
)
EXPECTED_CANDIDATE_REVIEW_DIGEST = approval.EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST
EXPECTED_CANDIDATE_DIGEST = approval.EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST
EXPECTED_REFINEMENT_RESULTS_REVIEW_DIGEST = approval.EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST
EXPECTED_REFINEMENT_EXECUTION_DIGEST = approval.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST
EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST = approval.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST
EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST = approval.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST
EXPECTED_ORIGINAL_EXECUTION_DIGEST = approval.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = approval.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
EXPECTED_RECORDS_DIGEST = approval.EXPECTED_RECORDS_DIGEST
EXPECTED_REFINED_LABEL_DIGEST = "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8"
EXPECTED_REFINED_FEATURE_DIGEST = "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00"

TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(approval.EXPECTED_RECORD_COUNTS)
REGISTRY_APPROVED_DATASET_METADATA = deepcopy(approval.REGISTRY_APPROVED_DATASET_METADATA)
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "ADDITIONAL_PREDICTIVE_EVIDENCE_REFINED_EVIDENCE_RESEARCH_ONLY"
NOT_ACCEPTED = approval.NOT_ACCEPTED
NOT_AUTHORIZED = approval.NOT_AUTHORIZED

REQUIRED_SOURCE_FILENAMES = [
    "feature_label_refinement_execution_manifest.json",
    "refined_label_generation_report.json",
    "refined_feature_generation_report.json",
    "refined_protocol_execution_report.json",
    "refined_model_comparison_report.json",
    "refined_walk_forward_report.json",
    "refined_out_of_sample_report.json",
    "refined_metric_report.json",
    "refined_leakage_control_report.json",
    "per_ticker_refinement_execution_summary.json",
    "feature_label_refinement_execution_digest_manifest.json",
    "operator_review_summary.json",
]
OUTPUT_FILENAMES = [
    "refined_additional_predictive_evidence_execution_manifest.json",
    "refined_evidence_input_manifest.json",
    "refined_label_feature_binding_manifest.json",
    "refined_walk_forward_reassessment_report.json",
    "refined_out_of_sample_reassessment_report.json",
    "refined_baseline_model_comparison_report.json",
    "refined_calibration_stability_report.json",
    "refined_leakage_quality_report.json",
    "refined_execution_digest_manifest.json",
    "refined_operator_review_summary.json",
]

TRUE_EXECUTION_FIELDS = [
    "feature_label_refinement_execution_approved",
    "feature_label_refinement_execution_authorized",
    "feature_label_refinement_executed",
    "feature_label_refinement_results_created",
    "feature_label_refinement_results_review_created",
    "feature_label_refinement_results_review_ready",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_created",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created",
    "additional_predictive_evidence_execution_for_refined_evidence_approved",
    "additional_predictive_evidence_execution_for_refined_evidence_authorized",
    "ready_for_additional_predictive_evidence_execution_for_refined_evidence",
    "additional_predictive_evidence_execution_for_refined_evidence_executed",
    "additional_predictive_evidence_results_for_refined_evidence_created",
    "refined_evidence_input_binding_performed",
    "refined_walk_forward_reassessment_performed",
    "refined_out_of_sample_reassessment_performed",
    "refined_baseline_model_comparison_reassessment_performed",
    "refined_calibration_stability_review_performed",
    "refined_leakage_quality_review_performed",
    "canonical_dataset_generated",
    "canonical_dataset_frozen",
    "meta_reduced_record_count_preserved",
    "research_only",
]
FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "feature_label_refinement_execution_rerun_performed",
    "refined_label_generation_rerun_performed",
    "refined_feature_generation_rerun_performed",
    "refined_walk_forward_validation_rerun_performed",
    "refined_out_of_sample_evaluation_rerun_performed",
    "refined_metrics_recomputation_performed",
    "model_comparison_rerun_performed",
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
]


class AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(ValueError):
    """Raised when refined-evidence execution violates its guarded contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _source_evidence() -> dict[str, str]:
    return {
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest": EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_label_refinement_results_review_package_digest": EXPECTED_REFINEMENT_RESULTS_REVIEW_DIGEST,
        "feature_label_refinement_execution_digest": EXPECTED_REFINEMENT_EXECUTION_DIGEST,
        "feature_label_refinement_execution_approval_digest": EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": EXPECTED_ORIGINAL_EXECUTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _common_output_fields() -> dict[str, Any]:
    values = {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": REGISTRY_APPROVED_DATASET_METADATA["dataset_name"],
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "additional_predictive_evidence_execution_for_refined_evidence_approved": True,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": True,
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence": True,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": True,
        "additional_predictive_evidence_results_for_refined_evidence_created": True,
        "refined_evidence_input_binding_performed": True,
        "refined_walk_forward_reassessment_performed": True,
        "refined_out_of_sample_reassessment_performed": True,
        "refined_baseline_model_comparison_reassessment_performed": True,
        "refined_calibration_stability_review_performed": True,
        "refined_leakage_quality_review_performed": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "trade_recommendations_generated": False,
        "acceptance_evidence_status": "NOT_ACCEPTANCE_EVIDENCE",
        "profitability_evidence_status": "NOT_PROFITABILITY_EVIDENCE",
        "runtime_authority_status": "NOT_RUNTIME_AUTHORITY",
    }
    return values


def _report(report_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"report_name": report_name, **_common_output_fields(), **payload}


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _verify_refined_sources(
    source_root: Path, canonical_source_root: Path
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    for filename in REQUIRED_SOURCE_FILENAMES:
        if not (source_root / filename).is_file():
            failures.append(
                _failure(
                    "missing_refined_source_file",
                    "required refined-evidence source file missing",
                    filename=filename,
                )
            )
    records_path = canonical_source_root / "canonical_dataset_records.jsonl"
    if not records_path.is_file():
        failures.append(
            _failure(
                "missing_canonical_records",
                "canonical records file required for verification is missing",
            )
        )
    if failures:
        return {}, {}, failures

    try:
        reports = {
            filename.removesuffix(".json"): _load_json(source_root / filename)
            for filename in REQUIRED_SOURCE_FILENAMES
        }
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {}, {}, [_failure("invalid_refined_source_json", str(exc))]

    digest_manifest = reports["feature_label_refinement_execution_digest_manifest"]
    entries = digest_manifest.get("output_digest_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        failures.append(
            _failure("invalid_refined_digest_manifest", "digest manifest must contain 12 entries")
        )
        entries = []
    seen: set[str] = set()
    for entry in entries:
        filename = entry.get("filename")
        digest_kind = entry.get("digest_kind")
        expected = entry.get("sha256")
        if not isinstance(filename, str):
            failures.append(_failure("invalid_digest_entry", "digest filename missing"))
            continue
        seen.add(filename)
        if digest_kind == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE":
            if filename != "feature_label_refinement_execution_digest_manifest.json" or expected is not None:
                failures.append(
                    _failure("invalid_self_reference_policy", "refined digest self-reference is invalid")
                )
            continue
        if digest_kind != "FILE_SHA256" or not isinstance(expected, str):
            failures.append(_failure("invalid_digest_entry", "refined digest entry is invalid", filename=filename))
            continue
        path = source_root / filename
        if not path.is_file() or sha256_file(path) != expected:
            failures.append(
                _failure("refined_source_digest_mismatch", "refined source output digest mismatch", filename=filename)
            )
    if seen != set(REQUIRED_SOURCE_FILENAMES):
        failures.append(_failure("refined_digest_inventory_mismatch", "refined digest inventory mismatch"))

    records_digest = sha256_file(records_path)
    if records_digest != EXPECTED_RECORDS_DIGEST:
        failures.append(_failure("records_digest_mismatch", "canonical records digest mismatch", actual=records_digest))
    counts: Counter[str] = Counter()
    total = 0
    try:
        with records_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                counts[str(row.get("ticker"))] += 1
                total += 1
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(_failure("invalid_canonical_records", str(exc)))
    if total != 11946:
        failures.append(_failure("canonical_record_count_mismatch", "canonical record count mismatch", actual=total))
    if dict(counts) != EXPECTED_RECORD_COUNTS:
        failures.append(_failure("canonical_ticker_counts_mismatch", "canonical per-ticker counts mismatch"))

    label = reports["refined_label_generation_report"]
    feature = reports["refined_feature_generation_report"]
    protocol = reports["refined_protocol_execution_report"]
    model = reports["refined_model_comparison_report"]
    walk = reports["refined_walk_forward_report"]
    oos = reports["refined_out_of_sample_report"]
    leakage = reports["refined_leakage_control_report"]
    ticker_summary = reports["per_ticker_refinement_execution_summary"]
    manifest = reports["feature_label_refinement_execution_manifest"]
    expected_values = [
        (label.get("refined_label_family_count"), 7, "refined_label_family_count"),
        (label.get("coverage_entry_count"), 84, "refined_label_coverage_entries"),
        (label.get("available_count"), 82698, "refined_label_available_values"),
        (label.get("unavailable_count"), 924, "refined_label_unavailable_values"),
        (label.get("refined_label_generation_digest"), EXPECTED_REFINED_LABEL_DIGEST, "refined_label_generation_digest"),
        (feature.get("refined_feature_group_count"), 9, "refined_feature_group_count"),
        (feature.get("refined_feature_name_count"), 19, "refined_feature_field_count"),
        (feature.get("feature_matrix_row_count"), 11946, "refined_feature_rows"),
        (feature.get("total_null_or_unavailable_count"), 1128, "refined_feature_null_count"),
        (feature.get("refined_feature_generation_digest"), EXPECTED_REFINED_FEATURE_DIGEST, "refined_feature_generation_digest"),
        (protocol.get("refined_protocol_group_count"), 6, "refined_protocol_group_count"),
        (protocol.get("no_shuffle"), True, "no_shuffle"),
        (protocol.get("no_lookahead_leakage"), True, "no_lookahead"),
        (walk.get("fold_count"), 4, "walk_forward_fold_count"),
        (sum(int(fold.get("evaluation_row_count", 0)) for fold in walk.get("folds", [])), 3024, "walk_forward_evaluation_rows"),
        (model.get("model_comparison_group_count"), 5, "model_comparison_group_count"),
        (len(model.get("deterministic_comparison_ids", [])), 7, "deterministic_comparisons_evaluated"),
        (leakage.get("leakage_control_status"), "PASS", "refined_leakage_status"),
        (leakage.get("failed_control_count"), 0, "failed_leakage_controls"),
        (ticker_summary.get("target_universe"), TARGET_UNIVERSE, "target_universe"),
        (manifest.get("feature_label_refinement_execution_digest"), EXPECTED_REFINEMENT_EXECUTION_DIGEST, "refinement_execution_digest"),
    ]
    oos_metrics = model.get("out_of_sample_model_metrics", {})
    accuracies = sorted(str(value.get("accuracy")) for value in oos_metrics.values())
    expected_values.extend(
        [
            (all(value.get("evaluated_count") == 2988 for value in oos_metrics.values()), True, "oos_evaluation_rows"),
            ((accuracies[0], accuracies[-1]) if accuracies else None, ("0.119813", "0.480924"), "oos_accuracy_range"),
            (sum(1 for item in model.get("group_execution_results", []) if item.get("execution_status") == "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"), 3, "unavailable_model_family_requests"),
            (manifest.get("data_quality_summary", {}).get("status"), "PASS_WITH_PRESERVED_SOURCE_LIMITATION", "data_quality_status"),
        ]
    )
    for actual, expected, field in expected_values:
        if actual != expected:
            failures.append(_failure("refined_source_fact_mismatch", f"{field} mismatch", expected=expected, actual=actual))

    verification = {
        "source_root": _path_text(source_root),
        "canonical_source_root": _path_text(canonical_source_root),
        "source_refinement_output_count": 12,
        "required_source_files": list(REQUIRED_SOURCE_FILENAMES),
        "all_non_self_digest_manifest_entries_match": not any(item["failure_id"] in {"refined_source_digest_mismatch", "invalid_digest_entry", "refined_digest_inventory_mismatch"} for item in failures),
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "records_digest_expected": EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": records_digest,
        "records_digest_match": records_digest == EXPECTED_RECORDS_DIGEST,
        "total_canonical_record_count": total,
        "per_ticker_record_counts": dict(counts),
    }
    return verification, reports, failures


def _fold_summary(walk_report: dict[str, Any]) -> list[dict[str, Any]]:
    summaries = []
    for fold in walk_report.get("folds", []):
        accuracies = [str(metrics.get("accuracy")) for metrics in fold.get("model_metrics", {}).values()]
        summaries.append(
            {
                "fold_id": fold.get("fold_id"),
                "training_row_count": fold.get("training_row_count"),
                "evaluation_row_count": fold.get("evaluation_row_count"),
                "embargo_sessions": fold.get("embargo_sessions"),
                "shuffle": fold.get("shuffle"),
                "accuracy_range": f"{min(accuracies)} to {max(accuracies)}" if accuracies else "NOT_AVAILABLE",
            }
        )
    return summaries


def _build_summaries(reports: dict[str, dict[str, Any]], verification: dict[str, Any]) -> dict[str, Any]:
    label = reports["refined_label_generation_report"]
    feature = reports["refined_feature_generation_report"]
    protocol = reports["refined_protocol_execution_report"]
    walk = reports["refined_walk_forward_report"]
    oos = reports["refined_out_of_sample_report"]
    model = reports["refined_model_comparison_report"]
    metrics = reports["refined_metric_report"]
    leakage = reports["refined_leakage_control_report"]
    source_manifest = reports["feature_label_refinement_execution_manifest"]
    return {
        "refined_evidence_input_binding_summary": {
            "binding_status": "BOUND_REVIEWED_REFINED_EVIDENCE",
            "source_output_count": 12,
            "all_non_self_digests_verified": verification["all_non_self_digest_manifest_entries_match"],
            "records_digest_verified": verification["records_digest_match"],
            "refined_label_generation_digest": label["refined_label_generation_digest"],
            "refined_feature_generation_digest": feature["refined_feature_generation_digest"],
        },
        "refined_label_feature_binding_summary": {
            "binding_status": "BOUND_NOT_REGENERATED",
            "label_family_count": label["refined_label_family_count"],
            "label_coverage_entries": label["coverage_entry_count"],
            "label_available_values": label["available_count"],
            "label_unavailable_values": label["unavailable_count"],
            "feature_group_count": feature["refined_feature_group_count"],
            "feature_category_count": 11,
            "feature_field_count": feature["refined_feature_name_count"],
            "feature_rows": feature["feature_matrix_row_count"],
            "feature_null_or_unavailable_values": feature["total_null_or_unavailable_count"],
            "features_current_or_historical_only": feature["features_use_current_and_historical_information_only"],
            "future_labels_used_as_features": feature["future_label_values_used_as_features"],
        },
        "refined_walk_forward_reassessment_summary": {
            "reassessment_status": "ASSESSED_FROM_REVIEWED_SOURCE_NOT_RERUN",
            "fold_count": walk["fold_count"],
            "evaluation_row_count": sum(fold["evaluation_row_count"] for fold in walk["folds"]),
            "walk_forward_policy": walk["walk_forward_policy"],
            "fold_summaries": _fold_summary(walk),
        },
        "refined_out_of_sample_reassessment_summary": {
            "reassessment_status": "ASSESSED_FROM_REVIEWED_SOURCE_NOT_RERUN",
            "out_of_sample_window": deepcopy(oos["out_of_sample_window"]),
            "evaluation_row_count": 2988,
            "model_metrics": deepcopy(model["out_of_sample_model_metrics"]),
            "accuracy_range": "0.119813 to 0.480924",
        },
        "refined_baseline_model_comparison_summary": {
            "reassessment_status": "ASSESSED_FROM_REVIEWED_SOURCE_NOT_RERUN",
            "model_comparison_group_count": model["model_comparison_group_count"],
            "deterministic_comparison_ids": deepcopy(model["deterministic_comparison_ids"]),
            "group_execution_results": deepcopy(model["group_execution_results"]),
            "unavailable_model_family_requests": 3,
            "unavailable_model_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
            "model_comparison_is_acceptance_evidence": model["model_comparison_is_acceptance_evidence"],
        },
        "refined_calibration_stability_summary": {
            "review_status": "REVIEWED_FROM_EXISTING_REFINED_METRICS",
            "metric_families": deepcopy(metrics["metric_families"]),
            "walk_forward_fold_metrics": deepcopy(metrics["walk_forward_fold_metrics"]),
            "out_of_sample_model_metrics": deepcopy(metrics["out_of_sample_model_metrics"]),
            "acceptance_conclusion": metrics["acceptance_conclusion"],
        },
        "refined_leakage_quality_summary": {
            "review_status": "REVIEWED_FROM_EXISTING_REFINED_EVIDENCE",
            "leakage_status": leakage["leakage_control_status"],
            "failed_leakage_controls": leakage["failed_control_count"],
            "controls": deepcopy(leakage["controls"]),
            "protocol_group_count": protocol["refined_protocol_group_count"],
            "chronological_splits": True,
            "one_session_embargo": True,
            "no_shuffle": protocol["no_shuffle"],
            "no_lookahead": protocol["no_lookahead_leakage"],
        },
        "data_quality_summary": deepcopy(source_manifest["data_quality_summary"]),
    }


def _execution_digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("additional_predictive_evidence_execution_for_refined_evidence_digest", None)
    # The output location is operational metadata, not research evidence identity.
    payload.pop("generated_output_root", None)
    return payload


def additional_predictive_evidence_execution_for_refined_evidence_digest_v1(
    artifact: dict[str, Any],
) -> str:
    return semantic_digest(_execution_digest_payload(artifact))


def _blocked_artifact(
    *,
    source_root: Path,
    canonical_source_root: Path,
    output_root: Path,
    run_timestamp_utc: str,
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_REFINED_EVIDENCE,
        "created_offline": True,
        "run_timestamp_utc": run_timestamp_utc,
        "source_root": _path_text(source_root),
        "canonical_source_root": _path_text(canonical_source_root),
        "output_root": _path_text(output_root),
        "source_evidence": _source_evidence(),
        "additional_predictive_evidence_execution_for_refined_evidence_digest": "NOT_CREATED",
        "additional_predictive_evidence_execution_for_refined_evidence_approved": True,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": True,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
        "additional_predictive_evidence_results_for_refined_evidence_created": False,
        "generated_output_count": 0,
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "feature_label_refinement_execution_rerun_performed": False,
        "refined_label_generation_rerun_performed": False,
        "refined_feature_generation_rerun_performed": False,
        "refined_walk_forward_validation_rerun_performed": False,
        "refined_out_of_sample_evaluation_rerun_performed": False,
        "refined_metrics_recomputation_performed": False,
        "model_comparison_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "failure_count": len(failures),
        "failures": deepcopy(failures),
    }


def _build_artifact(
    *,
    run_timestamp_utc: str,
    source_root: Path,
    canonical_source_root: Path,
    output_root: Path,
    verification: dict[str, Any],
    summaries: dict[str, Any],
) -> dict[str, Any]:
    artifact = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY,
        "created_offline": True,
        "run_timestamp_utc": run_timestamp_utc,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "source_root": _path_text(source_root),
        "canonical_source_root": _path_text(canonical_source_root),
        "generated_output_root": _path_text(output_root),
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "acceptance_evidence_status": "NOT_ACCEPTANCE_EVIDENCE",
        "profitability_evidence_status": "NOT_PROFITABILITY_EVIDENCE",
        "runtime_authority_status": "NOT_RUNTIME_AUTHORITY",
        "source_verification": deepcopy(verification),
        "source_evidence": _source_evidence(),
        "registry_approved_dataset_metadata": deepcopy(REGISTRY_APPROVED_DATASET_METADATA),
        "dataset_name": REGISTRY_APPROVED_DATASET_METADATA["dataset_name"],
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "refined_label_family_count": 7,
        "refined_feature_group_count": 9,
        "refined_feature_field_count": 19,
        "refined_protocol_group_count": 6,
        "model_comparison_group_count": 5,
        "refined_leakage_status": "PASS",
        "failed_leakage_controls": 0,
        "generated_output_count": 10,
        "generated_output_names": list(OUTPUT_FILENAMES),
        "output_digest_manifest_summary": {
            "filename": "refined_execution_digest_manifest.json",
            "entry_count": 10,
            "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        },
        "failure_count": 0,
        "warning_count": 1,
        "warnings": ["META_PRESERVED_REDUCED_RECORD_COUNT_913"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        **{field: True for field in TRUE_EXECUTION_FIELDS},
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        **deepcopy(summaries),
    }
    artifact["additional_predictive_evidence_execution_for_refined_evidence_digest"] = (
        additional_predictive_evidence_execution_for_refined_evidence_digest_v1(artifact)
    )
    return artifact


def _build_reports(
    *, artifact: dict[str, Any], reports: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    timestamp = artifact["run_timestamp_utc"]
    source = artifact["source_evidence"]
    summaries = {
        key: deepcopy(artifact[key])
        for key in (
            "refined_evidence_input_binding_summary",
            "refined_label_feature_binding_summary",
            "refined_walk_forward_reassessment_summary",
            "refined_out_of_sample_reassessment_summary",
            "refined_baseline_model_comparison_summary",
            "refined_calibration_stability_summary",
            "refined_leakage_quality_summary",
            "data_quality_summary",
        )
    }
    return {
        "refined_additional_predictive_evidence_execution_manifest": deepcopy(artifact),
        "refined_evidence_input_manifest": _report(
            "refined_evidence_input_manifest",
            {
                "run_timestamp_utc": timestamp,
                "source_evidence": deepcopy(source),
                "source_verification": deepcopy(artifact["source_verification"]),
                "input_binding_summary": summaries["refined_evidence_input_binding_summary"],
                "source_file_digest_entries": deepcopy(reports["feature_label_refinement_execution_digest_manifest"]["output_digest_entries"]),
            },
        ),
        "refined_label_feature_binding_manifest": _report(
            "refined_label_feature_binding_manifest",
            {
                "run_timestamp_utc": timestamp,
                "binding_summary": summaries["refined_label_feature_binding_summary"],
                "source_refined_label_generation_digest": EXPECTED_REFINED_LABEL_DIGEST,
                "source_refined_feature_generation_digest": EXPECTED_REFINED_FEATURE_DIGEST,
            },
        ),
        "refined_walk_forward_reassessment_report": _report(
            "refined_walk_forward_reassessment_report",
            {"run_timestamp_utc": timestamp, **summaries["refined_walk_forward_reassessment_summary"]},
        ),
        "refined_out_of_sample_reassessment_report": _report(
            "refined_out_of_sample_reassessment_report",
            {"run_timestamp_utc": timestamp, **summaries["refined_out_of_sample_reassessment_summary"]},
        ),
        "refined_baseline_model_comparison_report": _report(
            "refined_baseline_model_comparison_report",
            {"run_timestamp_utc": timestamp, **summaries["refined_baseline_model_comparison_summary"]},
        ),
        "refined_calibration_stability_report": _report(
            "refined_calibration_stability_report",
            {"run_timestamp_utc": timestamp, **summaries["refined_calibration_stability_summary"]},
        ),
        "refined_leakage_quality_report": _report(
            "refined_leakage_quality_report",
            {
                "run_timestamp_utc": timestamp,
                **summaries["refined_leakage_quality_summary"],
                "data_quality_summary": summaries["data_quality_summary"],
            },
        ),
        "refined_operator_review_summary": _report(
            "refined_operator_review_summary",
            {
                "run_timestamp_utc": timestamp,
                "execution_status": artifact["execution_status"],
                "execution_digest": artifact["additional_predictive_evidence_execution_for_refined_evidence_digest"],
                "generated_output_count": 10,
                "failure_count": 0,
                "warning_count": 1,
                "data_quality_summary": summaries["data_quality_summary"],
                "next_task": "Additional Predictive Evidence Results Review for Refined Evidence v1",
            },
        ),
    }


def _write_outputs_once(
    output_root: Path, reports: dict[str, dict[str, Any]], execution_digest: str
) -> None:
    targets = [output_root / filename for filename in OUTPUT_FILENAMES]
    existing = [path.name for path in targets if path.exists()]
    if existing:
        raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(
            f"refined-evidence execution outputs already exist: {', '.join(existing)}"
        )
    payloads: dict[str, bytes] = {}
    digest_manifest_name = "refined_execution_digest_manifest"
    for filename in OUTPUT_FILENAMES:
        report_name = filename.removesuffix(".json")
        if report_name == digest_manifest_name:
            continue
        payloads[filename] = canonical_json_bytes(reports[report_name])
    digest_entries = [
        (
            {"filename": filename, "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "sha256": None}
            if filename == "refined_execution_digest_manifest.json"
            else {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(payloads[filename])}
        )
        for filename in OUTPUT_FILENAMES
    ]
    digest_manifest = _report(
        digest_manifest_name,
        {
            "run_timestamp_utc": reports["refined_additional_predictive_evidence_execution_manifest"]["run_timestamp_utc"],
            "generated_output_count": 10,
            "output_digest_entries": digest_entries,
            "all_non_self_output_digests_present": True,
            "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
            "additional_predictive_evidence_execution_for_refined_evidence_digest": execution_digest,
        },
    )
    payloads["refined_execution_digest_manifest.json"] = canonical_json_bytes(digest_manifest)
    output_root.mkdir(parents=True, exist_ok=True)
    for filename in OUTPUT_FILENAMES:
        path = output_root / filename
        try:
            with path.open("xb") as handle:
                handle.write(payloads[filename])
        except FileExistsError as exc:
            raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(
                f"refusing to overwrite refined-evidence output: {filename}"
            ) from exc


def execute_additional_predictive_evidence_for_refined_evidence_v1(
    *,
    source_root: str | Path | None = None,
    canonical_source_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Bind and reassess reviewed refined evidence without rerunning its source work."""
    source_path = DEFAULT_SOURCE_ROOT if source_root is None else Path(source_root)
    canonical_path = DEFAULT_CANONICAL_SOURCE_ROOT if canonical_source_root is None else Path(canonical_source_root)
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    verification, source_reports, failures = _verify_refined_sources(source_path, canonical_path)
    if failures:
        return _blocked_artifact(
            source_root=source_path,
            canonical_source_root=canonical_path,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            failures=failures,
        )
    if output_path.exists() and any(output_path.iterdir()):
        raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(
            "refined-evidence execution output root is not empty"
        )
    summaries = _build_summaries(source_reports, verification)
    artifact = _build_artifact(
        run_timestamp_utc=timestamp,
        source_root=source_path,
        canonical_source_root=canonical_path,
        output_root=output_path,
        verification=verification,
        summaries=summaries,
    )
    validate_additional_predictive_evidence_executed_for_refined_evidence_v1(artifact)
    reports = _build_reports(artifact=artifact, reports=source_reports)
    _write_outputs_once(
        output_path,
        reports,
        artifact["additional_predictive_evidence_execution_for_refined_evidence_digest"],
    )
    return artifact


FORBIDDEN_ARTIFACT_VALUES = {
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


def _reject_forbidden(value: Any, path: str = "artifact") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}"
            if isinstance(item, str) and item in FORBIDDEN_ARTIFACT_VALUES:
                raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(
                    f"{child} must not emit {item}"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(f"{child} must not be AUTHORIZED")
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(f"{child} must not be accepted")
            _reject_forbidden(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden(item, f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(f"{field} mismatch")


def validate_additional_predictive_evidence_executed_for_refined_evidence_v1(
    artifact: dict,
) -> dict[str, Any]:
    """Validate execution evidence and every closed downstream authority boundary."""
    if not isinstance(artifact, dict):
        raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError("artifact must be a JSON object")
    _reject_forbidden(artifact)
    expected = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "acceptance_evidence_status": "NOT_ACCEPTANCE_EVIDENCE",
        "profitability_evidence_status": "NOT_PROFITABILITY_EVIDENCE",
        "runtime_authority_status": "NOT_RUNTIME_AUTHORITY",
        "source_evidence": _source_evidence(),
        "registry_approved_dataset_metadata": REGISTRY_APPROVED_DATASET_METADATA,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "refined_label_family_count": 7,
        "refined_feature_group_count": 9,
        "refined_feature_field_count": 19,
        "refined_protocol_group_count": 6,
        "model_comparison_group_count": 5,
        "refined_leakage_status": "PASS",
        "failed_leakage_controls": 0,
        "generated_output_count": 10,
        "generated_output_names": OUTPUT_FILENAMES,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected_value in expected.items():
        _expect(artifact.get(field), expected_value, field)
    for field in TRUE_EXECUTION_FIELDS:
        _expect(artifact.get(field), True, field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect(artifact.get(field), False, field)
    verification = artifact.get("source_verification", {})
    _expect(verification.get("source_refinement_output_count"), 12, "source_refinement_output_count")
    _expect(verification.get("all_non_self_digest_manifest_entries_match"), True, "source digest verification")
    _expect(verification.get("digest_manifest_self_reference_policy"), "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "source self-reference policy")
    _expect(verification.get("records_digest_match"), True, "records_digest_match")
    for field in (
        "refined_evidence_input_binding_summary",
        "refined_label_feature_binding_summary",
        "refined_walk_forward_reassessment_summary",
        "refined_out_of_sample_reassessment_summary",
        "refined_baseline_model_comparison_summary",
        "refined_calibration_stability_summary",
        "refined_leakage_quality_summary",
        "data_quality_summary",
    ):
        if not isinstance(artifact.get(field), dict) or not artifact[field]:
            raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError(f"{field} missing")
    _expect(artifact["refined_walk_forward_reassessment_summary"].get("fold_count"), 4, "walk-forward fold count")
    _expect(artifact["refined_walk_forward_reassessment_summary"].get("evaluation_row_count"), 3024, "walk-forward evaluation rows")
    _expect(artifact["refined_out_of_sample_reassessment_summary"].get("evaluation_row_count"), 2988, "OOS evaluation rows")
    _expect(artifact["refined_out_of_sample_reassessment_summary"].get("accuracy_range"), "0.119813 to 0.480924", "OOS accuracy range")
    _expect(artifact["refined_baseline_model_comparison_summary"].get("unavailable_model_family_requests"), 3, "unavailable model families")
    _expect(artifact["refined_leakage_quality_summary"].get("leakage_status"), "PASS", "leakage status")
    _expect(artifact["data_quality_summary"].get("status"), "PASS_WITH_PRESERVED_SOURCE_LIMITATION", "data quality status")
    _expect(artifact.get("failure_count"), 0, "failure_count")
    digest = artifact.get("additional_predictive_evidence_execution_for_refined_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError("execution digest missing")
    _expect(digest, additional_predictive_evidence_execution_for_refined_evidence_digest_v1(artifact), "execution digest")
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "additional_predictive_evidence_execution_for_refined_evidence_digest": digest,
        "generated_output_count": 10,
        "failure_count": 0,
        "warning_count": artifact["warning_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_execution_for_refined_evidence_status_markdown_v1(
    artifact: dict,
) -> str:
    validation = validate_additional_predictive_evidence_executed_for_refined_evidence_v1(artifact)
    source = artifact["source_evidence"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution for Refined Evidence Status",
        "",
        "## Title",
        "- Additional Predictive Evidence Execution for Refined Evidence v1.",
        "",
        "## Additional Predictive Evidence Execution for Refined Evidence",
        f"- Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`.",
        f"- Execution digest: `{validation['additional_predictive_evidence_execution_for_refined_evidence_digest']}`.",
        "",
        "## Source Execution Approval",
        f"- Approval digest: `{source['additional_predictive_evidence_execution_approval_for_refined_evidence_digest']}`.",
        f"- Candidate review/candidate digests: `{source['additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest']}` / `{source['additional_predictive_evidence_execution_candidate_for_refined_evidence_digest']}`.",
        "",
        "## Source Feature/Label Refinement Results Review",
        f"- Results-review/execution digests: `{source['feature_label_refinement_results_review_package_digest']}` / `{source['feature_label_refinement_execution_digest']}`.",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/records: `{artifact['dataset_name']}` / `{artifact['total_canonical_record_count']}`.",
        "",
        "## Target Universe",
        "- " + ", ".join(artifact["target_universe"]),
        "",
        "## Refined Evidence Input Binding",
        f"- `{artifact['refined_evidence_input_binding_summary']}`",
        "",
        "## Refined Label/Feature Binding Summary",
        f"- `{artifact['refined_label_feature_binding_summary']}`",
        "",
        "## Refined Walk-Forward Reassessment",
        f"- `{artifact['refined_walk_forward_reassessment_summary']}`",
        "",
        "## Refined OOS Reassessment",
        f"- Rows/range: `{artifact['refined_out_of_sample_reassessment_summary']['evaluation_row_count']}` / `{artifact['refined_out_of_sample_reassessment_summary']['accuracy_range']}`.",
        "",
        "## Refined Baseline and Model Comparison Reassessment",
        f"- `{artifact['refined_baseline_model_comparison_summary']}`",
        "",
        "## Refined Calibration and Stability Review",
        f"- Review status: `{artifact['refined_calibration_stability_summary']['review_status']}`.",
        "",
        "## Refined Leakage and Quality Review",
        f"- Leakage/data quality: `{artifact['refined_leakage_status']}` / `{artifact['data_quality_summary']['status']}`.",
        "",
        "## Output Digest Manifest",
        f"- `{artifact['output_digest_manifest_summary']}`",
        "",
        "## Execution Boundary",
        "- Source evidence was bound and reassessed; no source refinement, provider, acquisition, or dataset work was rerun.",
        "",
        "## Predictive Usefulness Boundary",
        "- Predictive usefulness remains `not accepted`.",
        "",
        "## Profitability Boundary",
        "- Profitability remains `not accepted`.",
        "",
        "## Runtime Boundary",
        "- Runtime, strategy, paper, and broker use remain `NOT_AUTHORIZED`.",
        "",
        "## Checklist Summary",
        f"- Failures/warnings: `{artifact['failure_count']}` / `{artifact['warning_count']}`.",
        "",
        "## Guardrails",
        "- Research-only, non-actionable, not acceptance evidence, not profitability evidence, and not runtime authority.",
        "",
    ]
    return "\n".join(lines)
