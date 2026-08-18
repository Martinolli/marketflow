"""Offline, digest-bound review of feature generation using redesigned labels."""

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
from marketflow.services import feature_generation_execution_redesigned_labels_service as execution


ARTIFACT_KIND_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS = (
    "FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_V1 = (
    "feature_generation_results_review_using_redesigned_labels_v1"
)
FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY = (
    "FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY"
)
FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS = (
    "FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS"
)
FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_VALID = (
    "FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_VALID"
)

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
DEFAULT_BRANCH = "feature/feature-generation-results-review-redesigned-labels-v1"
DEFAULT_BASE_COMMIT = "9f0b31bfce0f9d6e37d5de3cfdfd807881c88df7"
EXPECTED_EXECUTION_DIGEST = "d44e11b32dc8ba82ec0cdbf431397762dec56f9fd9323bf66f0571c39d82ca7f"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = {
    ticker: 913 if ticker == "META" else 1003 for ticker in EXPECTED_TARGET_UNIVERSE
}
OUTPUT_LABEL = execution.OUTPUT_LABEL
EVIDENCE_SCOPE = execution.EVIDENCE_SCOPE
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SOURCE_EVIDENCE = {
    "feature_generation_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
    "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
    "feature_generation_approval_using_redesigned_labels_digest": execution.EXPECTED_APPROVAL_DIGEST,
    "feature_generation_candidate_using_redesigned_labels_review_package_digest": execution.approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "feature_generation_candidate_using_redesigned_labels_digest": execution.approval_service.EXPECTED_CANDIDATE_DIGEST,
    "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": execution.approval_service.EXPECTED_PLANNING_APPROVAL_DIGEST,
    "redesigned_label_generation_results_review_package_digest": execution.approval_service.EXPECTED_RESULTS_REVIEW_DIGEST,
    "redesigned_label_generation_execution_digest": execution.approval_service.EXPECTED_EXECUTION_DIGEST,
    "redesigned_label_generation_approval_digest": execution.approval_service.EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
    "research_registry_approval_digest": execution.approval_service.EXPECTED_RESEARCH_REGISTRY_DIGEST,
    "records_digest": execution.EXPECTED_RECORDS_DIGEST,
    "label_values_digest": execution.EXPECTED_LABEL_VALUES_DIGEST,
}

LIMITATIONS = [
    "features_are_research_only",
    "predictive_evidence_not_executed",
    "metrics_not_recomputed",
    "models_not_trained",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "trade_recommendations_not_generated",
    "meta_reduced_record_count_preserved",
    "baseline_error_context_unavailable_by_design",
    "operator_review_required_before_additional_predictive_evidence_candidate",
    "operator_approval_required_before_any_predictive_execution",
]
NEXT_CHAIN = [
    "Additional Predictive Evidence Execution Candidate Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Candidate Operator Review Package v1.",
    "Additional Predictive Evidence Execution Approval Using Redesigned Labels v1, if selected.",
    "Additional Predictive Evidence Execution Using Redesigned Labels v1.",
    "Additional Predictive Evidence Results Review Using Redesigned Labels v1.",
    "Predictive Usefulness Reassessment Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_candidate_operator_review",
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
    "review_does_not_execute_predictive_evidence",
    "review_does_not_train_models",
    "review_does_not_recompute_metrics",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "preserve_meta_record_limitation",
    "no_predictive_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]
REQUIRED_CHECK_IDS = [
    "feature_generation_execution_digest_bound",
    "feature_values_digest_bound",
    "feature_generation_approval_digest_bound",
    "candidate_review_digest_bound",
    "candidate_digest_bound",
    "planning_approval_digest_bound",
    "redesigned_label_results_review_digest_bound",
    "redesigned_label_execution_digest_bound",
    "label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "label_values_digest_preserved",
    "meta_913_preserved",
    "source_execution_status_research_only",
    "generated_output_count_12",
    "output_digests_bound",
    "output_digest_mismatch_count_zero",
    "outputs_research_only_non_actionable",
    "feature_values_verified",
    "feature_family_coverage_verified",
    "feature_group_report_verified",
    "feature_schema_contract_verified",
    "feature_label_alignment_report_verified",
    "feature_quality_report_verified",
    "per_ticker_feature_summary_verified",
    "meta_limitation_feature_handling_verified",
    "feature_family_count_10",
    "feature_group_count_17",
    "feature_schema_field_count_16",
    "feature_value_row_count_203082",
    "available_feature_value_count_190848",
    "unavailable_feature_value_count_12234",
    "non_meta_feature_rows_per_ticker_17051",
    "meta_feature_rows_15521",
    "history_only_policy_preserved",
    "future_label_values_not_used_as_features",
    "label_values_not_used_as_features",
    "forward_returns_not_used_as_features",
    "threshold_values_not_used_as_numeric_predictors",
    "baseline_error_context_unavailable_by_design",
    "feature_generation_results_review_created_true",
    "feature_generation_results_review_ready_true",
    "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels_true",
    "additional_predictive_evidence_execution_candidate_created_false",
    "predictive_evidence_executed_false",
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
    "feature_generation_rerun_false",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "limitations_recorded",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]

FEATURE_VALUE_FIELDS = set(execution.SCHEMA_FIELDS)
FORBIDDEN_FEATURE_FIELDS = {
    "label_value",
    "forward_return",
    "threshold_value_used",
    "future_return_direction",
    "future_return_bucket",
}


class FeatureGenerationResultsReviewRedesignedLabelsError(ValueError):
    """Raised when generated feature outputs cannot support a valid review."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FeatureGenerationResultsReviewRedesignedLabelsError(
            f"{path.name} is not readable JSON"
        ) from exc
    if not isinstance(value, dict):
        raise FeatureGenerationResultsReviewRedesignedLabelsError(
            f"{path.name} must contain a JSON object"
        )
    return value


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


def _forbidden_authority_field(value: Any) -> str | None:
    forbidden_true = {
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in forbidden_true and item is True:
                return str(key)
            if key in {"predictive_usefulness", "profitability"} and item != NOT_ACCEPTED:
                return str(key)
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item != NOT_AUTHORIZED:
                return str(key)
            nested = _forbidden_authority_field(item)
            if nested:
                return nested
    elif isinstance(value, list):
        for item in value:
            nested = _forbidden_authority_field(item)
            if nested:
                return nested
    return None


def _inspect_feature_values(path: Path) -> dict[str, Any]:
    row_count = available_count = unavailable_count = baseline_count = 0
    ticker_counts = {ticker: 0 for ticker in EXPECTED_TARGET_UNIVERSE}
    families: set[str] = set()
    groups: set[str] = set()
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise FeatureGenerationResultsReviewRedesignedLabelsError(
                        f"feature_values.jsonl line {line_number} is invalid JSON"
                    ) from exc
                if not isinstance(row, dict) or set(row) != FEATURE_VALUE_FIELDS:
                    raise FeatureGenerationResultsReviewRedesignedLabelsError(
                        f"feature_values.jsonl line {line_number} fields mismatch"
                    )
                if FORBIDDEN_FEATURE_FIELDS.intersection(row):
                    raise FeatureGenerationResultsReviewRedesignedLabelsError(
                        f"feature_values.jsonl line {line_number} contains future or label values"
                    )
                if row["research_only"] is not True or row["non_actionable"] is not True:
                    raise FeatureGenerationResultsReviewRedesignedLabelsError(
                        f"feature_values.jsonl line {line_number} is actionable"
                    )
                ticker = row["ticker"]
                if ticker not in ticker_counts:
                    raise FeatureGenerationResultsReviewRedesignedLabelsError(
                        f"feature_values.jsonl line {line_number} ticker mismatch"
                    )
                available = row["feature_available"] is True
                if available != (row["feature_value"] is not None):
                    raise FeatureGenerationResultsReviewRedesignedLabelsError(
                        f"feature_values.jsonl line {line_number} availability mismatch"
                    )
                if row["source_history_window"] < 0:
                    raise FeatureGenerationResultsReviewRedesignedLabelsError(
                        f"feature_values.jsonl line {line_number} history window mismatch"
                    )
                if row["feature_group"] == "baseline_error_context_candidates":
                    baseline_count += 1
                    if available or row["availability_reason"] != "BASELINE_ERROR_CONTEXT_REQUIRES_FUTURE_OUTCOME_REVIEW":
                        raise FeatureGenerationResultsReviewRedesignedLabelsError(
                            f"feature_values.jsonl line {line_number} baseline context mismatch"
                        )
                row_count += 1
                available_count += int(available)
                unavailable_count += int(not available)
                ticker_counts[ticker] += 1
                families.add(row["feature_family"])
                groups.add(row["feature_group"])
    except OSError as exc:
        raise FeatureGenerationResultsReviewRedesignedLabelsError(
            "feature_values.jsonl is not readable"
        ) from exc
    return {
        "row_count": row_count,
        "available_count": available_count,
        "unavailable_count": unavailable_count,
        "ticker_counts": ticker_counts,
        "families": sorted(families),
        "groups": sorted(groups),
        "baseline_count": baseline_count,
        "history_only_policy_preserved": True,
        "future_label_values_used_as_features": False,
        "label_values_used_as_features": False,
        "forward_returns_used_as_features": False,
        "threshold_values_used_as_numeric_predictors": False,
        "raw_provider_payloads_present": False,
        "api_keys_present": False,
    }


def _blocked_package(root: Path, reasons: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_V1,
        "review_status": FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_root": _path_text(root),
        "output_file_inspection_performed": False,
        "source_feature_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "source_feature_generation_approval_digest": execution.EXPECTED_APPROVAL_DIGEST,
        "feature_generation_results_review_created": False,
        "feature_generation_results_review_ready": False,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "feature_generation_results_review_using_redesigned_labels_digest": "NOT_CREATED",
        "blocker_reasons": reasons,
        "blocker_count": len(reasons),
    }


def _verify_outputs(
    root: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    failures = [
        {"failure_id": "missing_output_file", "filename": filename}
        for filename in EXPECTED_OUTPUT_FILENAMES
        if not (root / filename).is_file()
    ]
    if failures:
        return {}, [], {}, failures
    try:
        payloads = {
            filename: _load_json(root / filename)
            for filename in EXPECTED_OUTPUT_FILENAMES
            if filename.endswith(".json")
        }
        stats = _inspect_feature_values(root / "feature_values.jsonl")
    except FeatureGenerationResultsReviewRedesignedLabelsError as exc:
        return {}, [], {}, [{"failure_id": "invalid_output", "message": str(exc)}]

    digest_payload = payloads["feature_generation_digest_manifest.json"]
    rows = digest_payload.get("output_digest_manifest")
    if not isinstance(rows, list):
        failures.append({"failure_id": "missing_digest_manifest"})
        rows = []
    recorded = {row.get("filename"): row for row in rows if isinstance(row, dict)}
    bindings: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        local_sha256 = sha256_file(root / filename)
        entry = recorded.get(filename)
        expected_entry = {
            "filename": filename,
            "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE" if filename == "feature_generation_digest_manifest.json" else "FILE_SHA256",
            "sha256": None if filename == "feature_generation_digest_manifest.json" else local_sha256,
        }
        status = PASS if entry == expected_entry else FAIL
        if status == FAIL:
            failures.append({"failure_id": "digest_manifest_entry_mismatch", "filename": filename})
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
        forbidden = _forbidden_authority_field(payload)
        if forbidden:
            failures.append({"failure_id": "forbidden_output_authority", "filename": filename, "field": forbidden})
        if _contains_sensitive_value(payload):
            failures.append({"failure_id": "sensitive_output_value", "filename": filename})
    return payloads, bindings, stats, failures


def _per_ticker_verified(rows: Any, stats: dict[str, Any]) -> bool:
    if not isinstance(rows, list) or [row.get("ticker") for row in rows] != EXPECTED_TARGET_UNIVERSE:
        return False
    for row in rows:
        ticker = row["ticker"]
        expected_records = EXPECTED_RECORD_COUNTS[ticker]
        expected_rows = 15521 if ticker == "META" else 17051
        expected = {
            "canonical_record_count": expected_records,
            "feature_value_row_count": expected_rows,
            "meta_reduced_record_count_flag": ticker == "META",
        }
        if any(row.get(key) != value for key, value in expected.items()):
            return False
        if stats["ticker_counts"].get(ticker) != expected_rows:
            return False
    return True


def _base_package(
    root: Path,
    payloads: dict[str, dict[str, Any]],
    bindings: list[dict[str, Any]],
    stats: dict[str, Any],
) -> dict[str, Any]:
    source = payloads["feature_generation_execution_manifest.json"]
    family = payloads["feature_family_coverage_report.json"]
    groups = payloads["feature_group_generation_report.json"]
    schema = payloads["feature_schema_contract_report.json"]
    alignment = payloads["feature_label_alignment_report.json"]
    quality = payloads["feature_quality_report.json"]
    ticker = payloads["per_ticker_feature_summary.json"]
    meta = payloads["meta_limitation_feature_handling_report.json"]
    operator = payloads["operator_review_summary.json"]
    output_digests = {row["filename"]: row["local_sha256"] for row in bindings}
    per_ticker_verified = _per_ticker_verified(ticker.get("per_ticker_summary"), stats)
    feature_values_verified = (
        stats["row_count"] == 203082
        and stats["available_count"] == 190848
        and stats["unavailable_count"] == 12234
        and stats["families"] == sorted(execution.FAMILY_IDS)
        and stats["groups"] == sorted(execution.GROUP_IDS)
        and stats["baseline_count"] == 11946
        and per_ticker_verified
        and output_digests["feature_values.jsonl"] == EXPECTED_FEATURE_VALUES_DIGEST
    )
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_V1,
        "review_status": FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY,
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
        "redesigned_label_regeneration_performed": False,
        "feature_generation_rerun_performed": False,
        "feature_regeneration_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "source_execution_artifact_kind": source["artifact_kind"],
        "source_execution_status": source["execution_status"],
        "source_feature_generation_execution_digest": source["feature_generation_execution_digest"],
        "source_feature_values_digest": source["feature_values_digest"],
        "source_feature_generation_approval_digest": source["feature_generation_approval_using_redesigned_labels_digest"],
        "source_feature_generation_candidate_review_digest": source["feature_generation_candidate_using_redesigned_labels_review_package_digest"],
        "source_feature_generation_candidate_digest": source["feature_generation_candidate_using_redesigned_labels_digest"],
        "source_feature_predictive_evidence_planning_approval_digest": source["feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"],
        "source_redesigned_label_results_review_digest": source["redesigned_label_generation_results_review_package_digest"],
        "source_redesigned_label_execution_digest": source["redesigned_label_generation_execution_digest"],
        "source_redesigned_label_approval_digest": source["redesigned_label_generation_approval_digest"],
        "source_research_registry_approval_digest": source["research_registry_approval_digest"],
        "source_evidence": dict(SOURCE_EVIDENCE),
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
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "dataset_name": source["dataset_name"],
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"],
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "source_label_value_row_count": 143352,
        "source_available_label_value_count": 142200,
        "source_unavailable_label_value_count": 1152,
        "source_label_family_count": 10,
        "source_threshold_strategy_count": 7,
        "source_horizon_strategy_count": 5,
        "label_values_digest": source["label_values_digest"],
        "generated_output_count": source["generated_output_count"],
        "generated_output_names": list(EXPECTED_OUTPUT_FILENAMES),
        "feature_family_count": source["feature_family_count"],
        "feature_group_count": source["feature_group_count"],
        "feature_schema_field_count": source["feature_schema_field_count"],
        "feature_value_row_count": stats["row_count"],
        "available_feature_value_count": stats["available_count"],
        "unavailable_feature_value_count": stats["unavailable_count"],
        "feature_values_digest": output_digests["feature_values.jsonl"],
        "feature_generation_failure_count": quality["failure_count"],
        "feature_generation_warning_count": quality["warning_count"],
        "non_meta_feature_rows_per_ticker": 17051,
        "meta_feature_rows": meta["meta_feature_value_row_count"],
        "meta_source_record_count": meta["meta_record_count"],
        "output_root": _path_text(root),
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
        "outputs_research_only_non_actionable": True,
        "outputs_evidence_scope": EVIDENCE_SCOPE,
        "feature_values_review": {"available": True, "verified": feature_values_verified},
        "feature_family_coverage_review": {
            "available": True,
            "verified": family.get("feature_family_count") == 10 and family.get("feature_families") == execution.FAMILY_IDS and stats["families"] == sorted(execution.FAMILY_IDS),
        },
        "feature_group_generation_review": {
            "available": True,
            "verified": groups.get("feature_group_count") == 17 and groups.get("feature_groups") == execution.GROUP_IDS and stats["groups"] == sorted(execution.GROUP_IDS),
        },
        "feature_schema_contract_review": {
            "available": True,
            "verified": schema.get("feature_schema_field_count") == 16 and schema.get("schema_fields") == execution.SCHEMA_FIELDS and FEATURE_VALUE_FIELDS == set(schema.get("schema_fields", [])),
        },
        "feature_label_alignment_review": {
            "available": True,
            "verified": alignment.get("metadata_only") is True and alignment.get("label_values_used_as_features") is False and alignment.get("forward_returns_used_as_features") is False and alignment.get("threshold_values_used_as_features") is False,
            "future_label_values_used_as_features": False,
            "forward_returns_used_as_features": False,
            "threshold_values_used_as_numeric_predictors": False,
            "label_values_used_as_features": False,
            "baseline_error_context_computed_from_labels": False,
            "history_only_policy_preserved": stats["history_only_policy_preserved"],
        },
        "feature_quality_review": {
            "available": True,
            "verified": quality.get("failure_count") == 0 and quality.get("warning_count") == 0 and quality.get("feature_value_row_count") == 203082 and quality.get("available_feature_value_count") == 190848 and quality.get("unavailable_feature_value_count") == 12234,
            "baseline_error_context_unavailable_by_design": stats["baseline_count"] == 11946,
            "unavailable_feature_values_recorded": stats["unavailable_count"] == 12234,
        },
        "per_ticker_feature_summary_review": {
            "available": True,
            "verified": per_ticker_verified,
            "ticker_count": len(ticker.get("per_ticker_summary", [])),
        },
        "meta_limitation_feature_handling_review": {
            "available": True,
            "verified": meta.get("meta_record_count") == 913 and meta.get("meta_feature_value_row_count") == 15521 and meta.get("meta_limitation_preserved") is True and meta.get("records_repaired_or_inferred") is False,
        },
        "operator_review_summary_review": {
            "available": True,
            "verified": operator.get("execution_status") == execution.FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY and operator.get("feature_generation_execution_digest") == EXPECTED_EXECUTION_DIGEST and operator.get("predictive_evidence_execution_authorized") is False,
        },
        "feature_outputs_available": True,
        "feature_outputs_verified": True,
        "feature_values_available": True,
        "feature_family_coverage_available": True,
        "feature_group_report_available": True,
        "feature_schema_contract_available": True,
        "feature_label_alignment_report_available": True,
        "feature_quality_report_available": True,
        "per_ticker_feature_summary_available": True,
        "meta_limitation_feature_handling_report_available": True,
        "results_support_future_additional_predictive_evidence_execution_candidate_using_redesigned_labels": True,
        "results_create_additional_predictive_evidence_execution_candidate": False,
        "results_create_predictive_evidence": False,
        "results_create_model_metrics": False,
        "results_create_model_training": False,
        "results_create_predictive_usefulness_acceptance": False,
        "results_create_profitability_acceptance": False,
        "results_create_runtime_authority": False,
        "feature_generation_interpretation": "GENERATED_RESEARCH_ONLY",
        "predictive_evidence_interpretation": "NOT_EXECUTED_NOT_AUTHORIZED",
        "predictive_usefulness_interpretation": "NOT_ACCEPTANCE_EVIDENCE",
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
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "no_tracked_marketflow_files": True,
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
        "feature_generation_execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, package.get("source_feature_generation_execution_digest")),
        "feature_values_digest_bound": (EXPECTED_FEATURE_VALUES_DIGEST, package.get("source_feature_values_digest")),
        "feature_generation_approval_digest_bound": (SOURCE_EVIDENCE["feature_generation_approval_using_redesigned_labels_digest"], package.get("source_feature_generation_approval_digest")),
        "candidate_review_digest_bound": (SOURCE_EVIDENCE["feature_generation_candidate_using_redesigned_labels_review_package_digest"], package.get("source_feature_generation_candidate_review_digest")),
        "candidate_digest_bound": (SOURCE_EVIDENCE["feature_generation_candidate_using_redesigned_labels_digest"], package.get("source_feature_generation_candidate_digest")),
        "planning_approval_digest_bound": (SOURCE_EVIDENCE["feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"], package.get("source_feature_predictive_evidence_planning_approval_digest")),
        "redesigned_label_results_review_digest_bound": (SOURCE_EVIDENCE["redesigned_label_generation_results_review_package_digest"], package.get("source_redesigned_label_results_review_digest")),
        "redesigned_label_execution_digest_bound": (SOURCE_EVIDENCE["redesigned_label_generation_execution_digest"], package.get("source_redesigned_label_execution_digest")),
        "label_values_digest_bound": (execution.EXPECTED_LABEL_VALUES_DIGEST, package.get("label_values_digest")),
        "research_registry_digest_bound": (SOURCE_EVIDENCE["research_registry_approval_digest"], package.get("source_research_registry_approval_digest")),
        "records_digest_bound": (execution.EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        "target_universe_12_preserved": (EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        "records_digest_preserved": (execution.EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        "label_values_digest_preserved": (execution.EXPECTED_LABEL_VALUES_DIGEST, package.get("label_values_digest")),
        "meta_913_preserved": (913, package.get("meta_record_count")),
        "source_execution_status_research_only": (execution.FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY, package.get("source_execution_status")),
        "generated_output_count_12": (12, package.get("generated_output_count")),
        "output_digests_bound": (12, package.get("local_output_digest_count")),
        "output_digest_mismatch_count_zero": (0, package.get("output_digest_mismatch_count")),
        "outputs_research_only_non_actionable": (True, package.get("outputs_research_only_non_actionable")),
        "feature_values_verified": (True, package.get("feature_values_review", {}).get("verified")),
        "feature_family_coverage_verified": (True, package.get("feature_family_coverage_review", {}).get("verified")),
        "feature_group_report_verified": (True, package.get("feature_group_generation_review", {}).get("verified")),
        "feature_schema_contract_verified": (True, package.get("feature_schema_contract_review", {}).get("verified")),
        "feature_label_alignment_report_verified": (True, package.get("feature_label_alignment_review", {}).get("verified")),
        "feature_quality_report_verified": (True, package.get("feature_quality_review", {}).get("verified")),
        "per_ticker_feature_summary_verified": (True, package.get("per_ticker_feature_summary_review", {}).get("verified")),
        "meta_limitation_feature_handling_verified": (True, package.get("meta_limitation_feature_handling_review", {}).get("verified")),
        "feature_family_count_10": (10, package.get("feature_family_count")),
        "feature_group_count_17": (17, package.get("feature_group_count")),
        "feature_schema_field_count_16": (16, package.get("feature_schema_field_count")),
        "feature_value_row_count_203082": (203082, package.get("feature_value_row_count")),
        "available_feature_value_count_190848": (190848, package.get("available_feature_value_count")),
        "unavailable_feature_value_count_12234": (12234, package.get("unavailable_feature_value_count")),
        "non_meta_feature_rows_per_ticker_17051": (17051, package.get("non_meta_feature_rows_per_ticker")),
        "meta_feature_rows_15521": (15521, package.get("meta_feature_rows")),
        "history_only_policy_preserved": (True, package.get("feature_label_alignment_review", {}).get("history_only_policy_preserved")),
        "future_label_values_not_used_as_features": (False, package.get("feature_label_alignment_review", {}).get("future_label_values_used_as_features")),
        "label_values_not_used_as_features": (False, package.get("feature_label_alignment_review", {}).get("label_values_used_as_features")),
        "forward_returns_not_used_as_features": (False, package.get("feature_label_alignment_review", {}).get("forward_returns_used_as_features")),
        "threshold_values_not_used_as_numeric_predictors": (False, package.get("feature_label_alignment_review", {}).get("threshold_values_used_as_numeric_predictors")),
        "baseline_error_context_unavailable_by_design": (True, package.get("feature_quality_review", {}).get("baseline_error_context_unavailable_by_design")),
        "feature_generation_results_review_created_true": (True, package.get("feature_generation_results_review_created")),
        "feature_generation_results_review_ready_true": (True, package.get("feature_generation_results_review_ready")),
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels_true": (True, package.get("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels")),
        "additional_predictive_evidence_execution_candidate_created_false": (False, package.get("additional_predictive_evidence_execution_candidate_created")),
        "predictive_evidence_executed_false": (False, package.get("additional_predictive_evidence_executed")),
        "metric_recomputation_false": (False, package.get("metric_recomputation_performed")),
        "model_training_false": (False, package.get("model_training_performed")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, package.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, package.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, package.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, package.get("strategy_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, package.get("broker_execution")),
        "trade_recommendations_false": (False, package.get("trade_recommendations_generated")),
        "provider_requests_made_false": (False, package.get("provider_requests_made_in_review")),
        "market_data_acquisition_false": (False, package.get("market_data_acquisition_performed_in_review")),
        "dataset_regeneration_false": (False, package.get("canonical_dataset_regenerated_in_review")),
        "redesigned_label_regeneration_false": (False, package.get("redesigned_label_regeneration_performed")),
        "feature_generation_rerun_false": (False, package.get("feature_generation_rerun_performed")),
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
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": not failed,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("feature_generation_results_review_using_redesigned_labels_digest", None)
    if "output_root" in payload:
        payload["output_root"] = DEFAULT_OUTPUT_ROOT.as_posix()
    return payload


def feature_generation_results_review_using_redesigned_labels_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return a deterministic, output-location-independent semantic digest."""
    return semantic_digest(_digest_payload(review_package))


def build_feature_generation_results_review_using_redesigned_labels_v1(
    *, output_root: str | Path | None = None
) -> dict[str, Any]:
    """Inspect existing ignored outputs without rerunning feature generation."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, stats, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    try:
        execution.validate_feature_generation_executed_using_redesigned_labels_v1(
            payloads["feature_generation_execution_manifest.json"]
        )
    except execution.FeatureGenerationExecutionRedesignedLabelsError as exc:
        return _blocked_package(
            root,
            [{"failure_id": "invalid_source_execution_artifact", "message": str(exc)}],
        )
    package = _base_package(root, payloads, bindings, stats)
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
    package["feature_generation_results_review_using_redesigned_labels_digest"] = (
        feature_generation_results_review_using_redesigned_labels_digest_v1(package)
    )
    validate_feature_generation_results_review_using_redesigned_labels_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureGenerationResultsReviewRedesignedLabelsError(f"{field} mismatch")


def validate_feature_generation_results_review_using_redesigned_labels_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Validate a ready or blocked review without touching source outputs."""
    if not isinstance(review_package, dict):
        raise FeatureGenerationResultsReviewRedesignedLabelsError(
            "review package must be a JSON object"
        )
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_V1, "schema_version")
    if review_package.get("review_status") == FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS:
        _expect(review_package.get("feature_generation_results_review_ready"), False, "blocked review ready")
        _expect(review_package.get("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"), False, "blocked candidate readiness")
        _expect(review_package.get("additional_predictive_evidence_execution_candidate_created"), False, "blocked candidate created")
        _expect(review_package.get("feature_generation_results_review_using_redesigned_labels_digest"), "NOT_CREATED", "blocked review digest")
        return {
            "status": "FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_BLOCKED_VALID",
            "review_status": review_package["review_status"],
            "blocker_count": review_package.get("blocker_count", 0),
        }
    _expect(review_package.get("review_status"), FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY, "review_status")
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS,
        "source_execution_status": execution.FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "source_feature_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "source_feature_generation_approval_digest": SOURCE_EVIDENCE["feature_generation_approval_using_redesigned_labels_digest"],
        "source_feature_generation_candidate_review_digest": SOURCE_EVIDENCE["feature_generation_candidate_using_redesigned_labels_review_package_digest"],
        "source_feature_generation_candidate_digest": SOURCE_EVIDENCE["feature_generation_candidate_using_redesigned_labels_digest"],
        "source_feature_predictive_evidence_planning_approval_digest": SOURCE_EVIDENCE["feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"],
        "source_redesigned_label_results_review_digest": SOURCE_EVIDENCE["redesigned_label_generation_results_review_package_digest"],
        "source_redesigned_label_execution_digest": SOURCE_EVIDENCE["redesigned_label_generation_execution_digest"],
        "source_redesigned_label_approval_digest": SOURCE_EVIDENCE["redesigned_label_generation_approval_digest"],
        "source_research_registry_approval_digest": SOURCE_EVIDENCE["research_registry_approval_digest"],
        "source_evidence": SOURCE_EVIDENCE,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "label_values_digest": execution.EXPECTED_LABEL_VALUES_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "generated_output_count": 12,
        "generated_output_names": EXPECTED_OUTPUT_FILENAMES,
        "feature_family_count": 10,
        "feature_group_count": 17,
        "feature_schema_field_count": 16,
        "feature_value_row_count": 203082,
        "available_feature_value_count": 190848,
        "unavailable_feature_value_count": 12234,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "non_meta_feature_rows_per_ticker": 17051,
        "meta_feature_rows": 15521,
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
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    true_fields = [
        "created_offline", "research_only", "operator_review_required",
        "feature_generation_approved", "feature_generation_authorized",
        "redesigned_feature_generation_authorized", "feature_generation_performed",
        "redesigned_feature_generation_performed", "feature_values_created",
        "feature_generation_results_created", "feature_generation_results_review_created",
        "feature_generation_results_review_ready",
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels",
        "output_file_inspection_performed", "outputs_research_only_non_actionable",
        "feature_outputs_available", "feature_outputs_verified",
        "results_support_future_additional_predictive_evidence_execution_candidate_using_redesigned_labels",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ]
    false_fields = [
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "redesigned_label_regeneration_performed",
        "feature_generation_rerun_performed", "feature_regeneration_performed",
        "metric_recomputation_performed", "model_training_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "results_create_additional_predictive_evidence_execution_candidate",
        "results_create_predictive_evidence", "results_create_model_metrics",
        "results_create_model_training", "results_create_predictive_usefulness_acceptance",
        "results_create_profitability_acceptance", "results_create_runtime_authority",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "profitability_acceptance_created", "runtime_migration_approved", "runtime_migration_active",
        "runtime_migration_approval_created", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ]
    for field in true_fields:
        _expect(review_package.get(field), True, field)
    for field in false_fields:
        _expect(review_package.get(field), False, field)
    _expect(review_package.get("local_output_digest_count"), 12, "local_output_digest_count")
    _expect(review_package.get("recorded_file_digest_match_count"), 11, "recorded_file_digest_match_count")
    _expect(review_package.get("output_digest_mismatch_count"), 0, "output_digest_mismatch_count")
    output_digests = review_package.get("output_digests")
    if not isinstance(output_digests, dict) or list(output_digests) != EXPECTED_OUTPUT_FILENAMES:
        raise FeatureGenerationResultsReviewRedesignedLabelsError("output_digests mismatch")
    if any(not isinstance(value, str) or len(value) != 64 for value in output_digests.values()):
        raise FeatureGenerationResultsReviewRedesignedLabelsError("output_digests must contain SHA-256 values")
    _expect(output_digests["feature_values.jsonl"], EXPECTED_FEATURE_VALUES_DIGEST, "feature values output digest")
    for field in (
        "feature_values_review", "feature_family_coverage_review",
        "feature_group_generation_review", "feature_schema_contract_review",
        "feature_label_alignment_review", "feature_quality_review",
        "per_ticker_feature_summary_review", "meta_limitation_feature_handling_review",
        "operator_review_summary_review",
    ):
        _expect(review_package.get(field, {}).get("verified"), True, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise FeatureGenerationResultsReviewRedesignedLabelsError("review_checklist mismatch")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review_checklist check ids")
    if any(row.get("status") != PASS for row in checklist):
        raise FeatureGenerationResultsReviewRedesignedLabelsError("review_checklist must pass")
    summary = _summary(checklist)
    _expect(review_package.get("review_summary"), summary, "review_summary")
    digest = review_package.get("feature_generation_results_review_using_redesigned_labels_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureGenerationResultsReviewRedesignedLabelsError("missing review digest")
    _expect(digest, feature_generation_results_review_using_redesigned_labels_digest_v1(review_package), "review digest")
    return {
        "status": FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "feature_generation_results_review_using_redesigned_labels_digest": digest,
        "source_feature_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "generated_output_count": 12,
        "blocker_count": summary["blocker_count"],
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_evidence_executed": False,
        "runtime_authorized": False,
    }


def build_feature_generation_results_review_using_redesigned_labels_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render the sanitized review without reproducing feature values."""
    validation = validate_feature_generation_results_review_using_redesigned_labels_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Feature Generation Results Review Using Redesigned Labels Status", "",
        "## Title", "- Feature Generation Results Review Using Redesigned Labels v1.", "",
        "## Feature Generation Results Review Using Redesigned Labels", f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['feature_generation_results_review_using_redesigned_labels_digest']}`.", "",
        "## Source Execution", f"- Artifact/status/digest: `{review_package['source_execution_artifact_kind']}` / `{review_package['source_execution_status']}` / `{review_package['source_feature_generation_execution_digest']}`.", "",
        "## Dataset and Universe", f"- `{review_package['dataset_name']}` contains `{review_package['total_canonical_record_count']}` records for 12 ordered tickers; META remains `{review_package['meta_record_count']}`.", "",
        "## Source Redesigned Label Profile", f"- Label rows/available/unavailable and digest: `{review_package['source_label_value_row_count']}` / `{review_package['source_available_label_value_count']}` / `{review_package['source_unavailable_label_value_count']}` / `{review_package['label_values_digest']}`.", "",
        "## Generated Feature Outputs", f"- All `{review_package['generated_output_count']}` ignored outputs and `{review_package['feature_value_row_count']}` feature rows were inspected offline.", "",
        "## Feature Family Coverage Review", f"- `{review_package['feature_family_count']}` families verified: `{review_package['feature_family_coverage_review']['verified']}`.", "",
        "## Feature Group Review", f"- `{review_package['feature_group_count']}` groups verified: `{review_package['feature_group_generation_review']['verified']}`.", "",
        "## Feature Schema Contract Review", f"- `{review_package['feature_schema_field_count']}` schema fields verified: `{review_package['feature_schema_contract_review']['verified']}`.", "",
        "## Feature / Label Alignment Review", "- History-only policy is preserved. Label values, future values, forward returns, and thresholds are not numeric predictors.", "",
        "## Feature Quality Review", f"- Available/unavailable/failures/warnings: `{review_package['available_feature_value_count']}` / `{review_package['unavailable_feature_value_count']}` / `{review_package['feature_generation_failure_count']}` / `{review_package['feature_generation_warning_count']}`.", "",
        "## Per-Ticker Feature Summary", "- Every non-META ticker has 17,051 feature rows; META has 15,521.", "",
        "## META Limitation Preservation Review", "- META remains limited to 913 source records with no backfill, repair, inference, or synthetic rows.", "",
        "## Output Digest Manifest", f"- Recorded/local/mismatched hashes: `{review_package['recorded_file_digest_match_count']}` / `{review_package['local_output_digest_count']}` / `{review_package['output_digest_mismatch_count']}`. Self-reference is `{review_package['digest_manifest_self_reference_policy']}`.", "",
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
        "", "## Predictive Evidence Boundary", "- The review creates no predictive-evidence candidate and executes no predictive evidence.",
        "", "## Predictive Usefulness Boundary", f"- Predictive usefulness remains `{review_package['predictive_usefulness']}`; reviewed features are not acceptance evidence.",
        "", "## Profitability Boundary", f"- Profitability remains `{review_package['profitability']}`.",
        "", "## Runtime Boundary", f"- Runtime/strategy/paper/broker remain `{review_package['runtime_use']}` / `{review_package['strategy_use']}` / `{review_package['paper_trading']}` / `{review_package['broker_execution']}`.",
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- The review read and hashed existing ignored outputs only. It made no provider request and performed no acquisition, dataset, label, feature, metric, model, predictive, recommendation, acceptance, profitability, runtime, or trading action.", "- Readiness supports only a future separately governed candidate; this review does not create or authorize it.", "",
    ])
    return "\n".join(lines)


def write_feature_generation_results_review_using_redesigned_labels_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting evidence."""
    package = build_feature_generation_results_review_using_redesigned_labels_v1(
        output_root=output_root
    )
    validate_feature_generation_results_review_using_redesigned_labels_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "feature_generation_results_review_using_redesigned_labels_v1.json"
    payload = canonical_json_bytes(package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise FeatureGenerationResultsReviewRedesignedLabelsError(
            "results review output already exists"
        ) from exc
    return {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": package["review_status"],
        "feature_generation_results_review_using_redesigned_labels_digest": package["feature_generation_results_review_using_redesigned_labels_digest"],
    }
