"""Offline, digest-bound review of generated redesigned-label outputs."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import redesigned_label_generation_execution_service as execution


ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE = (
    "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_V1 = (
    "redesigned_label_generation_results_review_v1"
)
REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE_READY = (
    "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE_READY"
)
REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_VALID = (
    "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_VALID"
)

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
DEFAULT_BRANCH = "feature/redesigned-label-generation-results-review-v1"
DEFAULT_BASE_COMMIT = "9292863565612e2fc62fc52ad35926a360d718fd"
EXPECTED_EXECUTION_DIGEST = (
    "0c1151794d913ead1653e5641e70f731932da2e9059dd534a14eec0ca5307506"
)
EXPECTED_LABEL_VALUES_DIGEST = (
    "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
)
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_HORIZON_ROW_COUNTS = {"1": 11946, "5": 83622, "10": 23892, "20": 23892}
GLOBAL_FIVE_SESSION_THRESHOLD = "0.026556108631"
BENCHMARK_RELATIVE_THRESHOLD = "0.02058653801"
OUTPUT_LABEL = execution.OUTPUT_LABEL
EVIDENCE_SCOPE = execution.EVIDENCE_SCOPE
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SOURCE_EVIDENCE = {
    "redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
    "redesigned_label_generation_approval_digest": execution.EXPECTED_REDESIGNED_LABEL_GENERATION_APPROVAL_DIGEST,
    "redesigned_label_generation_candidate_review_package_digest": execution.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
    "redesigned_label_generation_candidate_digest": execution.EXPECTED_CANDIDATE_DIGEST,
    "label_objective_redesign_results_review_package_digest": execution.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST,
    "label_objective_redesign_execution_digest": execution.EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_DIGEST,
    "operator_method_path_selection_digest": execution.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
    "research_registry_approval_digest": execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "records_digest": execution.EXPECTED_RECORDS_DIGEST,
    "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
}

LIMITATIONS = [
    "labels_are_research_only",
    "features_not_generated",
    "metrics_not_recomputed",
    "models_not_trained",
    "predictive_evidence_not_executed",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "trade_recommendations_not_generated",
    "meta_reduced_record_count_preserved",
    "forward_tail_labels_unavailable_by_design",
    "operator_review_required_before_feature_or_predictive_evidence_planning_candidate",
    "operator_approval_required_before_any_predictive_execution",
]
NEXT_CHAIN = [
    "Feature / Predictive Evidence Planning Candidate Using Redesigned Labels v1.",
    "Feature / Predictive Evidence Planning Candidate Operator Review Package v1.",
    "Feature / Predictive Evidence Planning Approval v1, if selected.",
    "Feature / Predictive Evidence Execution Candidate v1, if selected.",
    "Additional Predictive Evidence Execution and Results Review, if separately approved.",
    "Predictive Usefulness Reassessment and Readiness Review, only after new evidence.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels",
    "feature_or_predictive_evidence_planning_candidate_operator_review",
    "feature_or_predictive_evidence_planning_approval_if_selected",
    "feature_or_predictive_evidence_execution_candidate_if_selected",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_generate_features",
    "review_does_not_authorize_predictive_evidence_execution",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "preserve_meta_record_limitation",
    "forward_tail_unavailable_labels_remain_null",
    "no_predictive_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]
REQUIRED_CHECK_IDS = [
    "execution_digest_bound",
    "approval_digest_bound",
    "candidate_review_digest_bound",
    "candidate_digest_bound",
    "results_review_digest_bound",
    "operator_method_path_selection_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "label_values_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "source_execution_status_research_only",
    "generated_output_count_11",
    "output_digests_bound",
    "output_digest_mismatch_count_zero",
    "outputs_research_only_non_actionable",
    "label_values_verified",
    "label_family_coverage_verified",
    "threshold_report_verified",
    "horizon_report_verified",
    "availability_report_verified",
    "per_ticker_summary_verified",
    "meta_limitation_report_verified",
    "label_family_count_10",
    "threshold_strategy_count_7",
    "horizon_strategy_count_5",
    "label_value_row_count_143352",
    "available_label_value_count_142200",
    "unavailable_label_value_count_1152",
    "label_family_coverage_entries_144",
    "global_threshold_bound",
    "benchmark_relative_threshold_bound",
    "class_balance_descriptive_only",
    "threshold_optimization_false",
    "forward_tail_unavailable_labels_null",
    "meta_label_summary_preserved",
    "results_review_created_true",
    "results_review_ready_true",
    "ready_for_feature_or_predictive_evidence_planning_candidate_true",
    "feature_or_predictive_evidence_planning_candidate_created_false",
    "feature_generation_false",
    "metrics_recomputed_false",
    "model_training_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "redesigned_label_generation_rerun_false",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "limitations_recorded",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class RedesignedLabelGenerationResultsReviewError(ValueError):
    """Raised when generated label outputs cannot support a valid review."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RedesignedLabelGenerationResultsReviewError(
            f"{path.name} is not readable JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise RedesignedLabelGenerationResultsReviewError(
            f"{path.name} must contain a JSON object"
        )
    return payload


def _contains_sensitive_value(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() in {
                "api_key",
                "apikey",
                "authorization_header",
                "provider_payload",
                "raw_provider_payload",
            }:
                return True
            if _contains_sensitive_value(item):
                return True
    elif isinstance(value, list):
        return any(_contains_sensitive_value(item) for item in value)
    return False


def _forbidden_output_field(value: Any) -> str | None:
    forbidden_true = {
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in forbidden_true and item is True:
                return str(key)
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                return str(key)
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                return str(key)
            nested = _forbidden_output_field(item)
            if nested:
                return f"{key}.{nested}"
    elif isinstance(value, list):
        for index, item in enumerate(value):
            nested = _forbidden_output_field(item)
            if nested:
                return f"[{index}].{nested}"
    return None


LABEL_VALUE_FIELDS = {
    "availability_reason",
    "benchmark_basis",
    "date",
    "forward_return",
    "horizon",
    "label_available",
    "label_family",
    "label_value",
    "meta_reduced_record_count_flag",
    "non_actionable",
    "record_index_for_ticker",
    "research_only",
    "threshold_strategy",
    "threshold_value_used",
    "ticker",
    "window_partition",
}


def _inspect_label_values(path: Path) -> dict[str, Any]:
    row_count = 0
    available_count = 0
    unavailable_count = 0
    horizon_counts: dict[str, int] = {}
    ticker_counts: dict[str, dict[str, int]] = {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise RedesignedLabelGenerationResultsReviewError(
                        f"redesigned_label_values.jsonl line {line_number} is invalid JSON"
                    ) from exc
                if not isinstance(row, dict) or set(row) != LABEL_VALUE_FIELDS:
                    raise RedesignedLabelGenerationResultsReviewError(
                        f"redesigned_label_values.jsonl line {line_number} fields mismatch"
                    )
                if row["research_only"] is not True or row["non_actionable"] is not True:
                    raise RedesignedLabelGenerationResultsReviewError(
                        f"redesigned_label_values.jsonl line {line_number} is actionable"
                    )
                ticker = row["ticker"]
                horizon = str(row["horizon"])
                if ticker not in EXPECTED_TARGET_UNIVERSE or horizon not in {"1", "5", "10", "20"}:
                    raise RedesignedLabelGenerationResultsReviewError(
                        f"redesigned_label_values.jsonl line {line_number} identity mismatch"
                    )
                is_available = row["label_available"] is True
                if not is_available and (
                    row["label_value"] is not None or row["forward_return"] is not None
                ):
                    raise RedesignedLabelGenerationResultsReviewError(
                        f"redesigned_label_values.jsonl line {line_number} unavailable value must be null"
                    )
                if is_available and row["label_value"] is None:
                    raise RedesignedLabelGenerationResultsReviewError(
                        f"redesigned_label_values.jsonl line {line_number} available label is null"
                    )
                row_count += 1
                available_count += int(is_available)
                unavailable_count += int(not is_available)
                horizon_counts[horizon] = horizon_counts.get(horizon, 0) + 1
                counts = ticker_counts.setdefault(
                    ticker, {"rows": 0, "available": 0, "unavailable": 0}
                )
                counts["rows"] += 1
                counts["available"] += int(is_available)
                counts["unavailable"] += int(not is_available)
    except OSError as exc:
        raise RedesignedLabelGenerationResultsReviewError(
            "redesigned_label_values.jsonl is not readable"
        ) from exc
    return {
        "row_count": row_count,
        "available_count": available_count,
        "unavailable_count": unavailable_count,
        "horizon_counts": horizon_counts,
        "ticker_counts": ticker_counts,
        "feature_values_present": False,
        "model_metrics_present": False,
        "raw_provider_payloads_present": False,
        "api_keys_present": False,
        "forward_tail_unavailable_labels_null": True,
    }


def _blocked_package(output_root: Path, reasons: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_V1,
        "review_status": REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_root": _path_text(output_root),
        "output_file_inspection_performed": False,
        "source_redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_redesigned_label_generation_approval_digest": execution.EXPECTED_REDESIGNED_LABEL_GENERATION_APPROVAL_DIGEST,
        "redesigned_label_generation_results_review_created": False,
        "redesigned_label_generation_results_review_ready": False,
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels": False,
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "redesigned_label_generation_results_review_package_digest": "NOT_CREATED",
        "blocker_reasons": reasons,
        "blocker_count": len(reasons),
    }


def _verify_outputs(
    output_root: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        if not (output_root / filename).is_file():
            failures.append({"failure_id": "missing_output_file", "filename": filename})
    if failures:
        return {}, [], {}, failures
    try:
        payloads = {
            filename: _load_json(output_root / filename)
            for filename in EXPECTED_OUTPUT_FILENAMES
            if filename.endswith(".json")
        }
        label_stats = _inspect_label_values(output_root / "redesigned_label_values.jsonl")
    except RedesignedLabelGenerationResultsReviewError as exc:
        return {}, [], {}, [{"failure_id": "invalid_output", "message": str(exc)}]

    digest_payload = payloads["redesigned_label_generation_digest_manifest.json"]
    source_payload = payloads["redesigned_label_generation_execution_manifest.json"]
    recorded_rows = digest_payload.get("output_digest_manifest")
    source_rows = source_payload.get("output_digest_manifest")
    if not isinstance(recorded_rows, list) or recorded_rows != source_rows:
        failures.append({"failure_id": "digest_manifest_list_mismatch"})
        recorded_rows = []
    recorded = {
        row.get("filename"): row for row in recorded_rows if isinstance(row, dict)
    }
    bindings: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        local_sha256 = sha256_file(output_root / filename)
        entry = recorded.get(filename)
        status = PASS
        if filename == "redesigned_label_generation_execution_manifest.json":
            expected_entry = {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
                "sha256": None,
            }
        elif filename == "redesigned_label_generation_digest_manifest.json":
            expected_entry = {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
        else:
            expected_entry = {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": local_sha256,
            }
        if entry != expected_entry:
            status = FAIL
            failures.append(
                {"failure_id": "digest_manifest_entry_mismatch", "filename": filename}
            )
        bindings.append(
            {
                "filename": filename,
                "local_sha256": local_sha256,
                "recorded_digest_kind": entry.get("digest_kind") if entry else None,
                "recorded_sha256": entry.get("sha256") if entry else None,
                "verification_status": status,
            }
        )

    for filename, payload in payloads.items():
        if payload.get("output_label") != OUTPUT_LABEL:
            failures.append({"failure_id": "output_label_mismatch", "filename": filename})
        if payload.get("evidence_scope") != EVIDENCE_SCOPE:
            failures.append({"failure_id": "evidence_scope_mismatch", "filename": filename})
        forbidden = _forbidden_output_field(payload)
        if forbidden:
            failures.append(
                {"failure_id": "forbidden_output_authority", "filename": filename, "field": forbidden}
            )
        if _contains_sensitive_value(payload):
            failures.append({"failure_id": "sensitive_output_value", "filename": filename})
    return payloads, bindings, label_stats, failures


def _per_ticker_verified(rows: Any, label_stats: dict[str, Any]) -> bool:
    if not isinstance(rows, list) or [row.get("ticker") for row in rows] != EXPECTED_TARGET_UNIVERSE:
        return False
    for row in rows:
        ticker = row["ticker"]
        expected_records = 913 if ticker == "META" else 1003
        expected_rows = 10956 if ticker == "META" else 12036
        expected_available = 10860 if ticker == "META" else 11940
        expected = {
            "historical_record_count": expected_records,
            "label_value_row_count": expected_rows,
            "available_label_value_count": expected_available,
            "unavailable_label_value_count": 96,
            "meta_reduced_record_count_flag": ticker == "META",
        }
        if any(row.get(key) != value for key, value in expected.items()):
            return False
        stream = label_stats.get("ticker_counts", {}).get(ticker, {})
        if stream != {
            "rows": expected_rows,
            "available": expected_available,
            "unavailable": 96,
        }:
            return False
    return True


def _base_package(
    output_root: Path,
    payloads: dict[str, dict[str, Any]],
    bindings: list[dict[str, Any]],
    label_stats: dict[str, Any],
) -> dict[str, Any]:
    source = payloads["redesigned_label_generation_execution_manifest.json"]
    family = payloads["redesigned_label_family_coverage_report.json"]
    threshold = payloads["redesigned_threshold_generation_report.json"]
    horizon = payloads["redesigned_horizon_generation_report.json"]
    availability = payloads["redesigned_label_availability_report.json"]
    per_ticker = payloads["per_ticker_redesigned_label_summary.json"]
    meta = payloads["meta_limitation_preservation_report.json"]
    operator = payloads["operator_review_summary.json"]
    output_digests = {row["filename"]: row["local_sha256"] for row in bindings}
    per_ticker_rows = per_ticker.get("per_ticker_label_summary")
    per_ticker_verified = _per_ticker_verified(per_ticker_rows, label_stats)
    label_values_verified = (
        label_stats.get("row_count") == 143352
        and label_stats.get("available_count") == 142200
        and label_stats.get("unavailable_count") == 1152
        and label_stats.get("horizon_counts") == EXPECTED_HORIZON_ROW_COUNTS
        and per_ticker_verified
        and output_digests.get("redesigned_label_values.jsonl") == EXPECTED_LABEL_VALUES_DIGEST
    )
    return {
        "artifact_kind": ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_V1,
        "review_status": REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "redesigned_label_generation_execution_rerun_performed": False,
        "redesigned_label_regeneration_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "source_execution_artifact_kind": source["artifact_kind"],
        "source_execution_status": source["execution_status"],
        "source_redesigned_label_generation_execution_digest": source["redesigned_label_generation_execution_digest"],
        "source_redesigned_label_generation_approval_digest": SOURCE_EVIDENCE["redesigned_label_generation_approval_digest"],
        "source_redesigned_label_generation_candidate_review_package_digest": SOURCE_EVIDENCE["redesigned_label_generation_candidate_review_package_digest"],
        "source_redesigned_label_generation_candidate_digest": SOURCE_EVIDENCE["redesigned_label_generation_candidate_digest"],
        "source_label_objective_redesign_results_review_package_digest": SOURCE_EVIDENCE["label_objective_redesign_results_review_package_digest"],
        "source_label_objective_redesign_execution_digest": SOURCE_EVIDENCE["label_objective_redesign_execution_digest"],
        "source_operator_method_path_selection_digest": SOURCE_EVIDENCE["operator_method_path_selection_digest"],
        "source_research_registry_approval_digest": SOURCE_EVIDENCE["research_registry_approval_digest"],
        "source_evidence": dict(SOURCE_EVIDENCE),
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "redesigned_label_generation_performed": True,
        "actual_redesigned_labels_generated": True,
        "redesigned_label_generation_results_created": True,
        "redesigned_label_generation_results_review_created": True,
        "redesigned_label_generation_results_review_ready": True,
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels": True,
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "dataset_name": source["dataset_name"],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "generated_output_count": source["generated_output_count"],
        "generated_output_names": list(source["generated_output_names"]),
        "label_family_count": family["label_family_count"],
        "threshold_strategy_count": threshold["threshold_strategy_count"],
        "horizon_strategy_count": horizon["horizon_strategy_count"],
        "label_value_row_count": availability["label_value_row_count"],
        "label_family_coverage_entries": family["label_family_coverage_entries"],
        "available_label_value_count": availability["available_label_value_count"],
        "unavailable_label_value_count": availability["unavailable_label_value_count"],
        "label_values_digest": output_digests["redesigned_label_values.jsonl"],
        "global_five_session_threshold": threshold["global_threshold_5_session"],
        "benchmark_relative_threshold": threshold["benchmark_relative_threshold_5_session"],
        "per_ticker_thresholds_recorded": bool(threshold["per_ticker_thresholds_5_session"]),
        "volatility_adjusted_thresholds_recorded": bool(threshold["volatility_adjusted_thresholds_5_session"]),
        "class_balance_output_descriptive_only": bool(threshold["class_balance_distribution"]),
        "threshold_optimization_performed": threshold["threshold_optimization_performed"],
        "one_session_label_rows": horizon["horizon_label_row_counts"]["1"],
        "five_session_label_rows": horizon["horizon_label_row_counts"]["5"],
        "ten_session_label_rows": horizon["horizon_label_row_counts"]["10"],
        "twenty_session_label_rows": horizon["horizon_label_row_counts"]["20"],
        "non_meta_label_rows_per_ticker": 12036,
        "non_meta_available_labels_per_ticker": 11940,
        "non_meta_unavailable_labels_per_ticker": 96,
        "meta_label_rows": meta["meta_label_value_row_count"],
        "meta_available_labels": meta["meta_available_label_value_count"],
        "meta_unavailable_labels": meta["meta_unavailable_label_value_count"],
        "meta_source_record_count": meta["historical_record_count"],
        "output_root": _path_text(output_root),
        "output_file_inspection_performed": True,
        "output_digest_bindings": bindings,
        "output_digests": output_digests,
        "recorded_file_digest_match_count": sum(
            row["recorded_digest_kind"] == "FILE_SHA256" and row["verification_status"] == PASS
            for row in bindings
        ),
        "local_output_digest_count": len(output_digests),
        "output_digest_mismatch_count": sum(row["verification_status"] != PASS for row in bindings),
        "output_digest_verification_status": PASS,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "execution_manifest_self_reference_policy": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
        "outputs_research_only_non_actionable": True,
        "outputs_evidence_scope": EVIDENCE_SCOPE,
        "label_values_review": {
            "available": True,
            "verified": label_values_verified,
            "row_count": label_stats["row_count"],
            "available_count": label_stats["available_count"],
            "unavailable_count": label_stats["unavailable_count"],
            "feature_values_present": False,
            "model_metrics_present": False,
            "raw_provider_payloads_present": False,
            "api_keys_present": False,
            "forward_tail_unavailable_labels_null": label_stats["forward_tail_unavailable_labels_null"],
        },
        "label_family_coverage_review": {
            "available": True,
            "verified": family["label_family_count"] == 10 and family["label_family_coverage_entries"] == 144 and len(family["coverage_entries"]) == 144,
            "family_count": family["label_family_count"],
            "coverage_entries": family["label_family_coverage_entries"],
        },
        "threshold_strategy_review": {
            "available": True,
            "verified": threshold["threshold_strategy_count"] == 7 and threshold["global_threshold_5_session"] == GLOBAL_FIVE_SESSION_THRESHOLD and threshold["benchmark_relative_threshold_5_session"] == BENCHMARK_RELATIVE_THRESHOLD and threshold["threshold_optimization_performed"] is False,
            "strategy_count": threshold["threshold_strategy_count"],
            "global_five_session_threshold": threshold["global_threshold_5_session"],
            "benchmark_relative_threshold": threshold["benchmark_relative_threshold_5_session"],
            "class_balance_descriptive_only": bool(threshold["class_balance_distribution"]),
            "threshold_optimization_performed": threshold["threshold_optimization_performed"],
        },
        "horizon_strategy_review": {
            "available": True,
            "verified": horizon["horizon_strategy_count"] == 5 and horizon["horizon_label_row_counts"] == EXPECTED_HORIZON_ROW_COUNTS and label_stats["horizon_counts"] == EXPECTED_HORIZON_ROW_COUNTS,
            "strategy_count": horizon["horizon_strategy_count"],
            "row_counts": dict(horizon["horizon_label_row_counts"]),
        },
        "label_availability_review": {
            "available": True,
            "verified": availability["label_value_row_count"] == label_stats["row_count"] == 143352 and availability["available_label_value_count"] == label_stats["available_count"] == 142200 and availability["unavailable_label_value_count"] == label_stats["unavailable_count"] == 1152 and availability["forward_tail_unavailable_value"] is None,
            "forward_tail_unavailable_value": availability["forward_tail_unavailable_value"],
            "forward_tail_availability_reason": availability["forward_tail_availability_reason"],
        },
        "per_ticker_redesigned_label_summary_review": {
            "available": True,
            "verified": per_ticker_verified,
            "ticker_count": len(per_ticker_rows),
            "target_universe": [row["ticker"] for row in per_ticker_rows],
        },
        "meta_limitation_preservation_review": {
            "available": True,
            "verified": meta["ticker"] == "META" and meta["historical_record_count"] == 913 and meta["meta_label_value_row_count"] == 10956 and meta["meta_available_label_value_count"] == 10860 and meta["meta_unavailable_label_value_count"] == 96 and meta["no_backfill"] and meta["no_repair"] and meta["no_synthetic_rows"],
            "historical_record_count": meta["historical_record_count"],
            "label_rows": meta["meta_label_value_row_count"],
            "available_labels": meta["meta_available_label_value_count"],
            "unavailable_labels": meta["meta_unavailable_label_value_count"],
        },
        "operator_review_summary_review": {
            "available": True,
            "verified": operator["review_status"] == "AWAITING_SEPARATE_RESULTS_REVIEW" and operator["results_review_created"] is False and operator["operator_decision"] is None,
        },
        "redesigned_label_outputs_available": True,
        "redesigned_label_outputs_verified": True,
        "redesigned_label_values_available": True,
        "redesigned_label_family_coverage_available": True,
        "redesigned_threshold_report_available": True,
        "redesigned_horizon_report_available": True,
        "redesigned_availability_report_available": True,
        "per_ticker_redesigned_label_summary_available": True,
        "meta_limitation_report_available": True,
        "results_support_future_feature_or_predictive_evidence_planning_candidate": True,
        "results_create_feature_or_predictive_evidence_planning_candidate": False,
        "results_create_features": False,
        "results_create_predictive_evidence": False,
        "results_create_predictive_usefulness_acceptance": False,
        "results_create_profitability_acceptance": False,
        "results_create_runtime_authority": False,
        "label_generation_interpretation": "GENERATED_RESEARCH_ONLY",
        "feature_generation_interpretation": "NOT_GENERATED_NOT_AUTHORIZED",
        "predictive_usefulness_interpretation": "NOT_ACCEPTANCE_EVIDENCE",
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
        "no_tracked_marketflow_files": source["no_tracked_marketflow_files"],
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "limitations": list(LIMITATIONS),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


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


def _review_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, package.get("source_redesigned_label_generation_execution_digest")),
        "approval_digest_bound": (SOURCE_EVIDENCE["redesigned_label_generation_approval_digest"], package.get("source_redesigned_label_generation_approval_digest")),
        "candidate_review_digest_bound": (SOURCE_EVIDENCE["redesigned_label_generation_candidate_review_package_digest"], package.get("source_redesigned_label_generation_candidate_review_package_digest")),
        "candidate_digest_bound": (SOURCE_EVIDENCE["redesigned_label_generation_candidate_digest"], package.get("source_redesigned_label_generation_candidate_digest")),
        "results_review_digest_bound": (SOURCE_EVIDENCE["label_objective_redesign_results_review_package_digest"], package.get("source_label_objective_redesign_results_review_package_digest")),
        "operator_method_path_selection_digest_bound": (SOURCE_EVIDENCE["operator_method_path_selection_digest"], package.get("source_operator_method_path_selection_digest")),
        "research_registry_digest_bound": (SOURCE_EVIDENCE["research_registry_approval_digest"], package.get("source_research_registry_approval_digest")),
        "records_digest_bound": (SOURCE_EVIDENCE["records_digest"], package.get("records_digest")),
        "label_values_digest_bound": (EXPECTED_LABEL_VALUES_DIGEST, package.get("label_values_digest")),
        "target_universe_12_preserved": (EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        "records_digest_preserved": (execution.EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        "meta_913_preserved": (913, package.get("meta_record_count")),
        "source_execution_status_research_only": (execution.REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY, package.get("source_execution_status")),
        "generated_output_count_11": (11, package.get("generated_output_count")),
        "output_digests_bound": (11, package.get("local_output_digest_count")),
        "output_digest_mismatch_count_zero": (0, package.get("output_digest_mismatch_count")),
        "outputs_research_only_non_actionable": (True, package.get("outputs_research_only_non_actionable")),
        "label_values_verified": (True, package.get("label_values_review", {}).get("verified")),
        "label_family_coverage_verified": (True, package.get("label_family_coverage_review", {}).get("verified")),
        "threshold_report_verified": (True, package.get("threshold_strategy_review", {}).get("verified")),
        "horizon_report_verified": (True, package.get("horizon_strategy_review", {}).get("verified")),
        "availability_report_verified": (True, package.get("label_availability_review", {}).get("verified")),
        "per_ticker_summary_verified": (True, package.get("per_ticker_redesigned_label_summary_review", {}).get("verified")),
        "meta_limitation_report_verified": (True, package.get("meta_limitation_preservation_review", {}).get("verified")),
        "label_family_count_10": (10, package.get("label_family_count")),
        "threshold_strategy_count_7": (7, package.get("threshold_strategy_count")),
        "horizon_strategy_count_5": (5, package.get("horizon_strategy_count")),
        "label_value_row_count_143352": (143352, package.get("label_value_row_count")),
        "available_label_value_count_142200": (142200, package.get("available_label_value_count")),
        "unavailable_label_value_count_1152": (1152, package.get("unavailable_label_value_count")),
        "label_family_coverage_entries_144": (144, package.get("label_family_coverage_entries")),
        "global_threshold_bound": (GLOBAL_FIVE_SESSION_THRESHOLD, package.get("global_five_session_threshold")),
        "benchmark_relative_threshold_bound": (BENCHMARK_RELATIVE_THRESHOLD, package.get("benchmark_relative_threshold")),
        "class_balance_descriptive_only": (True, package.get("class_balance_output_descriptive_only")),
        "threshold_optimization_false": (False, package.get("threshold_optimization_performed")),
        "forward_tail_unavailable_labels_null": (True, package.get("label_values_review", {}).get("forward_tail_unavailable_labels_null")),
        "meta_label_summary_preserved": (True, package.get("meta_limitation_preservation_review", {}).get("verified")),
        "results_review_created_true": (True, package.get("redesigned_label_generation_results_review_created")),
        "results_review_ready_true": (True, package.get("redesigned_label_generation_results_review_ready")),
        "ready_for_feature_or_predictive_evidence_planning_candidate_true": (True, package.get("ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels")),
        "feature_or_predictive_evidence_planning_candidate_created_false": (False, package.get("feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created")),
        "feature_generation_false": (False, package.get("feature_generation_performed")),
        "metrics_recomputed_false": (False, package.get("metric_recomputation_performed")),
        "model_training_false": (False, package.get("model_training_performed")),
        "additional_predictive_evidence_execution_candidate_created_false": (False, package.get("additional_predictive_evidence_execution_candidate_created")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, package.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, package.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, package.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, package.get("strategy_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, package.get("broker_execution")),
        "trade_recommendations_false": (False, package.get("trade_recommendations_generated")),
        "provider_requests_made_false": (False, package.get("provider_requests_made_in_review")),
        "market_data_acquisition_false": (False, package.get("market_data_acquisition_performed_in_review")),
        "dataset_regeneration_false": (False, package.get("canonical_dataset_regenerated_in_review")),
        "redesigned_label_generation_rerun_false": (False, package.get("redesigned_label_generation_execution_rerun_performed")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, package.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, package.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, package.get("runtime_migration_approval_created")),
        "limitations_recorded": (LIMITATIONS, package.get("limitations")),
        "next_chain_defined": (NEXT_CHAIN, package.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, package.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, package.get("risk_controls")),
        "no_tracked_marketflow_files": (True, package.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "results_review_ready": not failed,
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels": not failed,
        "feature_or_predictive_evidence_planning_candidate_created": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("redesigned_label_generation_results_review_package_digest", None)
    if "output_root" in payload:
        payload["output_root"] = DEFAULT_OUTPUT_ROOT.as_posix()
    return payload


def redesigned_label_generation_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return a deterministic, output-location-independent semantic digest."""
    return semantic_digest(_digest_payload(review_package))


def build_redesigned_label_generation_results_review_package_v1(
    *, output_root: str | Path | None = None
) -> dict[str, Any]:
    """Inspect existing ignored label outputs without rerunning generation."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, label_stats, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    try:
        execution.validate_redesigned_label_generation_executed_v1(
            payloads["redesigned_label_generation_execution_manifest.json"]
        )
    except execution.RedesignedLabelGenerationExecutionError as exc:
        return _blocked_package(
            root,
            [{"failure_id": "invalid_source_execution_artifact", "message": str(exc)}],
        )
    package = _base_package(root, payloads, bindings, label_stats)
    package["review_checklist"] = _review_checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    if package["review_summary"]["blocker_count"]:
        return _blocked_package(
            root,
            [
                {"failure_id": "review_check_failed", "check_id": row["check_id"]}
                for row in package["review_checklist"]
                if row["status"] != PASS
            ],
        )
    package["redesigned_label_generation_results_review_package_digest"] = (
        redesigned_label_generation_results_review_package_digest_v1(package)
    )
    validate_redesigned_label_generation_results_review_package_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise RedesignedLabelGenerationResultsReviewError(f"{field} mismatch")


def validate_redesigned_label_generation_results_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Validate a ready or blocked review without touching source outputs."""
    if not isinstance(review_package, dict):
        raise RedesignedLabelGenerationResultsReviewError(
            "review package must be a JSON object"
        )
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_V1,
        "schema_version",
    )
    if review_package.get("review_status") == REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        _expect(review_package.get("redesigned_label_generation_results_review_ready"), False, "blocked review ready")
        _expect(review_package.get("ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels"), False, "blocked planning readiness")
        _expect(review_package.get("feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created"), False, "blocked planning candidate created")
        _expect(review_package.get("redesigned_label_generation_results_review_package_digest"), "NOT_CREATED", "blocked review digest")
        return {
            "status": "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_BLOCKED_VALID",
            "review_status": review_package["review_status"],
            "blocker_count": review_package.get("blocker_count", 0),
        }

    _expect(review_package.get("review_status"), REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE_READY, "review_status")
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_EXECUTED,
        "source_execution_status": execution.REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY,
        "source_redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_redesigned_label_generation_approval_digest": SOURCE_EVIDENCE["redesigned_label_generation_approval_digest"],
        "source_redesigned_label_generation_candidate_review_package_digest": SOURCE_EVIDENCE["redesigned_label_generation_candidate_review_package_digest"],
        "source_redesigned_label_generation_candidate_digest": SOURCE_EVIDENCE["redesigned_label_generation_candidate_digest"],
        "source_label_objective_redesign_results_review_package_digest": SOURCE_EVIDENCE["label_objective_redesign_results_review_package_digest"],
        "source_label_objective_redesign_execution_digest": SOURCE_EVIDENCE["label_objective_redesign_execution_digest"],
        "source_operator_method_path_selection_digest": SOURCE_EVIDENCE["operator_method_path_selection_digest"],
        "source_research_registry_approval_digest": SOURCE_EVIDENCE["research_registry_approval_digest"],
        "source_evidence": SOURCE_EVIDENCE,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "generated_output_count": 11,
        "generated_output_names": EXPECTED_OUTPUT_FILENAMES,
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "label_value_row_count": 143352,
        "label_family_coverage_entries": 144,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "global_five_session_threshold": GLOBAL_FIVE_SESSION_THRESHOLD,
        "benchmark_relative_threshold": BENCHMARK_RELATIVE_THRESHOLD,
        "one_session_label_rows": 11946,
        "five_session_label_rows": 83622,
        "ten_session_label_rows": 23892,
        "twenty_session_label_rows": 23892,
        "meta_label_rows": 10956,
        "meta_available_labels": 10860,
        "meta_unavailable_labels": 96,
        "meta_source_record_count": 913,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "limitations": LIMITATIONS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
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
        "output_file_inspection_performed",
        "outputs_research_only_non_actionable",
        "redesigned_label_outputs_available",
        "redesigned_label_outputs_verified",
        "results_support_future_feature_or_predictive_evidence_planning_candidate",
        "meta_reduced_record_count_preserved",
        "class_balance_output_descriptive_only",
        "per_ticker_thresholds_recorded",
        "volatility_adjusted_thresholds_recorded",
        "no_tracked_marketflow_files",
    ]
    false_fields = [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "label_objective_redesign_execution_rerun_performed",
        "redesigned_label_generation_execution_rerun_performed",
        "redesigned_label_regeneration_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "threshold_optimization_performed",
        "results_create_feature_or_predictive_evidence_planning_candidate",
        "results_create_features",
        "results_create_predictive_evidence",
        "results_create_predictive_usefulness_acceptance",
        "results_create_profitability_acceptance",
        "results_create_runtime_authority",
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
        _expect(review_package.get(field), True, field)
    for field in false_fields:
        _expect(review_package.get(field), False, field)
    _expect(review_package.get("local_output_digest_count"), 11, "local_output_digest_count")
    _expect(review_package.get("recorded_file_digest_match_count"), 9, "recorded_file_digest_match_count")
    _expect(review_package.get("output_digest_mismatch_count"), 0, "output_digest_mismatch_count")
    output_digests = review_package.get("output_digests")
    if not isinstance(output_digests, dict) or list(output_digests) != EXPECTED_OUTPUT_FILENAMES:
        raise RedesignedLabelGenerationResultsReviewError("output_digests mismatch")
    if any(not isinstance(value, str) or len(value) != 64 for value in output_digests.values()):
        raise RedesignedLabelGenerationResultsReviewError("output_digests must contain SHA-256 values")
    _expect(output_digests["redesigned_label_values.jsonl"], EXPECTED_LABEL_VALUES_DIGEST, "label values output digest")
    for field in (
        "label_values_review",
        "label_family_coverage_review",
        "threshold_strategy_review",
        "horizon_strategy_review",
        "label_availability_review",
        "per_ticker_redesigned_label_summary_review",
        "meta_limitation_preservation_review",
        "operator_review_summary_review",
    ):
        _expect(review_package.get(field, {}).get("verified"), True, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise RedesignedLabelGenerationResultsReviewError("review_checklist mismatch")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review_checklist check ids")
    if any(row.get("status") != PASS for row in checklist):
        raise RedesignedLabelGenerationResultsReviewError("review_checklist must pass")
    expected_summary = _summary(checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("redesigned_label_generation_results_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise RedesignedLabelGenerationResultsReviewError("missing review digest")
    _expect(digest, redesigned_label_generation_results_review_package_digest_v1(review_package), "review digest")
    return {
        "status": REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "redesigned_label_generation_results_review_package_digest": digest,
        "source_redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "generated_output_count": 11,
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels": True,
        "feature_or_predictive_evidence_planning_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_redesigned_label_generation_results_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized review without reproducing generated label values."""
    validation = validate_redesigned_label_generation_results_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Redesigned Label Generation Results Review Status", "",
        "## Title", "- Redesigned Label Generation Results Review v1.", "",
        "## Redesigned Label Generation Results Review", f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['redesigned_label_generation_results_review_package_digest']}`.", "",
        "## Source Execution", f"- Artifact/status/digest: `{review_package['source_execution_artifact_kind']}` / `{review_package['source_execution_status']}` / `{review_package['source_redesigned_label_generation_execution_digest']}`.", "",
        "## Dataset and Universe", f"- `{review_package['dataset_name']}` contains `{review_package['total_canonical_record_count']}` frozen records for 12 ordered tickers; META remains `{review_package['meta_record_count']}`.", "",
        "## Generated Label Outputs", f"- All `{review_package['generated_output_count']}` ignored outputs were inspected offline; nine recorded hashes and all eleven local hashes are bound.", "",
        "## Label Family Coverage Review", f"- `{review_package['label_family_count']}` families produced `{review_package['label_family_coverage_entries']}` coverage entries.", "",
        "## Threshold Strategy Review", f"- Seven strategies are recorded; the five-session global and benchmark-relative thresholds are `{review_package['global_five_session_threshold']}` and `{review_package['benchmark_relative_threshold']}`. Class balance is descriptive only and optimization was not performed.", "",
        "## Horizon Strategy Review", f"- Horizon rows: 1=`{review_package['one_session_label_rows']}`, 5=`{review_package['five_session_label_rows']}`, 10=`{review_package['ten_session_label_rows']}`, 20=`{review_package['twenty_session_label_rows']}`.", "",
        "## Label Availability Review", f"- Rows/available/unavailable: `{review_package['label_value_row_count']}` / `{review_package['available_label_value_count']}` / `{review_package['unavailable_label_value_count']}`; unavailable forward-tail values remain null.", "",
        "## Per-Ticker Label Summary", "- Each non-META ticker has 12,036 rows (11,940 available, 96 unavailable); META has 10,956 (10,860 available, 96 unavailable).", "",
        "## META Limitation Preservation Review", "- META remains limited to 913 source records with no backfill, repair, or synthetic rows.", "",
        "## Output Digest Manifest", f"- Recorded/local/mismatched output digests: `{review_package['recorded_file_digest_match_count']}` / `{review_package['local_output_digest_count']}` / `{review_package['output_digest_mismatch_count']}`. The digest manifest self-reference is explicitly `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE`.", "",
        "## Limitations",
    ]
    lines.extend(f"- `{item}`" for item in review_package["limitations"])
    lines.extend(["", "## Next Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(review_package["next_chain"], 1))
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in review_package["next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend([
        "", "## Predictive Usefulness Boundary", f"- Predictive usefulness remains `{review_package['predictive_usefulness']}`; generated labels are not acceptance evidence.",
        "", "## Profitability Boundary", f"- Profitability remains `{review_package['profitability']}`.",
        "", "## Runtime Boundary", f"- Runtime/strategy/paper/broker remain `{review_package['runtime_use']}` / `{review_package['strategy_use']}` / `{review_package['paper_trading']}` / `{review_package['broker_execution']}`.",
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- The review read and hashed existing ignored outputs only. It made no provider request and performed no acquisition, dataset, label, feature, metric, model, predictive, recommendation, acceptance, profitability, runtime, or trading action.", "- Readiness supports only a future separately governed planning candidate; the review does not create or authorize that candidate.", "",
    ])
    return "\n".join(lines)


def write_redesigned_label_generation_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting evidence."""
    package = build_redesigned_label_generation_results_review_package_v1(
        output_root=output_root
    )
    validate_redesigned_label_generation_results_review_package_v1(package)
    output_name = filename or "redesigned_label_generation_results_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise RedesignedLabelGenerationResultsReviewError(
            "results review filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise RedesignedLabelGenerationResultsReviewError(
            "results review output already exists"
        ) from exc
    return {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": package["review_status"],
        "redesigned_label_generation_results_review_package_digest": package["redesigned_label_generation_results_review_package_digest"],
    }
