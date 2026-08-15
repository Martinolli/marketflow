"""Offline results review for executed feature/label refinement evidence."""

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
from marketflow.services import feature_label_refinement_execution_service as execution


ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE = (
    "FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_V1 = (
    "feature_label_refinement_results_review_v1"
)
FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE_READY = (
    "FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE_READY"
)
FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_VALID = (
    "FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_VALID"
)

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
DEFAULT_BRANCH = "feature/feature-label-refinement-results-review-v1"
DEFAULT_BASE_COMMIT = "a362ee412b9f4090965dd2db4b014e88c9b673f0"
EXPECTED_EXECUTION_DIGEST = (
    "377d6d232dcdf4b94f9f2d66414ff994edca2d3d9d95f4fb97d9dbfaf2359b36"
)
EXPECTED_EXECUTION_APPROVAL_DIGEST = execution.EXPECTED_EXECUTION_APPROVAL_DIGEST
EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_EXECUTION_CANDIDATE_DIGEST = execution.EXPECTED_EXECUTION_CANDIDATE_DIGEST
EXPECTED_PLAN_APPROVAL_DIGEST = execution.EXPECTED_PLAN_APPROVAL_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    execution.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = execution.EXPECTED_RECORDS_DIGEST
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_OUTPUT_DIGESTS = {
    "feature_label_refinement_execution_manifest.json": "09fe54dd7064260b5af29733134c0cc5ef1dd8f00e71c39bada0cd751266dab4",
    "refined_label_generation_report.json": "910d4b0baabc7f6ae10098cfd0bc9d45ec3f5cc52ff874e7135734a848a12e9c",
    "refined_feature_generation_report.json": "fae82056c0cd1cf72103917606f3bb271860ffed6d7158f2895885aee1f3f602",
    "refined_protocol_execution_report.json": "fe577a317a8fc736d759041a177e56edf451e54ada1aa2012e2c667aa557c8e1",
    "refined_model_comparison_report.json": "51e2031f77cdbf8a4d71a30d6d8eb152503e4d0973e9e24b6de56a0c9806f0d9",
    "refined_walk_forward_report.json": "686a000b9c9356b6fc3a76eca176f797ba597ca3abc101c7a49469f1c5f68bd0",
    "refined_out_of_sample_report.json": "9bdbfdafd1782a4717cbdae04ee40e54083281ac546a0d0af46e0c442857674e",
    "refined_metric_report.json": "8b6a61014fbaa8d5140db2f02a336344846924d8e9afb236a5f99ca0e6c058d2",
    "refined_leakage_control_report.json": "5259544f7cc1ee74630f64058eaf32d4ff84e02bde437b1bd5a638e515de1d55",
    "per_ticker_refinement_execution_summary.json": "2113bd8ede57a494b4c2eda62f0c1170dc378c9824f86f9842eda6eb582bc85f",
    "feature_label_refinement_execution_digest_manifest.json": "c325ce7d2e70a6e042c9f03e5c14887d721e00612f0e6c78e1a9d425b1732c17",
    "operator_review_summary.json": "21be540379639c871fbfb2cfd36fdfd501e22eba9054d775a6d2b93c8ba562f1",
}

RESEARCH_ONLY_NON_ACTIONABLE = execution.OUTPUT_LABEL
FEATURE_LABEL_REFINEMENT_RESEARCH_ONLY = execution.EVIDENCE_SCOPE
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

LIMITATIONS = [
    "refinement_results_are_research_only",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "trade_recommendations_not_generated",
    "refined_oos_accuracy_low_or_mixed",
    "model_comparison_not_acceptance_evidence_by_itself",
    "unavailable_model_families_recorded_not_fabricated",
    "meta_reduced_record_count_preserved",
    "operator_review_required_before_additional_predictive_evidence_candidate",
    "operator_approval_required_before_any_acceptance_or_runtime_migration",
]
NEXT_GATES = [
    "feature_label_refinement_results_operator_review",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence",
    "additional_predictive_evidence_execution_candidate_operator_review",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_review_rerun",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
REQUIRED_CHECK_IDS = [
    "feature_label_refinement_execution_digest_bound",
    "feature_label_refinement_execution_approval_digest_bound",
    "feature_label_refinement_execution_candidate_review_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_universe",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "generated_output_count_12",
    "output_digests_bound",
    "outputs_research_only_non_actionable",
    "digest_manifest_self_reference_non_applicable",
    "refined_label_family_count_7",
    "refined_feature_group_count_9",
    "refined_feature_fields_19",
    "refined_protocol_group_count_6",
    "model_comparison_group_count_5",
    "refined_label_generation_digest_bound",
    "refined_feature_generation_digest_bound",
    "refined_label_coverage_summary_bound",
    "refined_feature_coverage_summary_bound",
    "refined_walk_forward_fold_count_4",
    "refined_walk_forward_rows_3024",
    "refined_oos_rows_2988",
    "refined_oos_accuracy_range_bound",
    "model_comparison_summary_bound",
    "unavailable_model_families_recorded",
    "refined_leakage_status_pass",
    "failed_leakage_controls_zero",
    "data_quality_pass_with_preserved_limitation",
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
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "feature_label_refinement_executed_true",
    "feature_label_refinement_results_created_true",
    "refined_label_generation_performed_true",
    "refined_feature_generation_performed_true",
    "refined_walk_forward_validation_performed_true",
    "refined_out_of_sample_evaluation_performed_true",
    "refined_metrics_recomputation_performed_true",
    "model_comparison_performed_true",
    "additional_predictive_evidence_execution_candidate_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_candidate_created_false",
    "profitability_not_accepted",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "results_support_future_additional_predictive_evidence_planning_true",
    "results_create_additional_predictive_evidence_execution_candidate_false",
    "results_create_predictive_usefulness_acceptance_false",
    "results_create_profitability_acceptance_false",
    "results_create_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class FeatureLabelRefinementResultsReviewError(ValueError):
    """Raised when refinement results cannot support a valid review package."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FeatureLabelRefinementResultsReviewError(
            f"{path.name} is not readable JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise FeatureLabelRefinementResultsReviewError(
            f"{path.name} must contain a JSON object"
        )
    return payload


def _contains_sensitive_value(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered_key = str(key).lower()
            if lowered_key in {
                "api_key",
                "apikey",
                "access_token",
                "authorization",
                "provider_response_body",
                "raw_provider_payload",
                "raw_provider_payloads",
            }:
                return True
            if _contains_sensitive_value(item):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_sensitive_value(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(
            token in lowered
            for token in ("bearer ", "apikey=", "api_key=", "access_token=")
        )
    return False


def _forbidden_output_field(payload: Mapping[str, Any]) -> str | None:
    forbidden_true = {
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
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
    }
    for key, value in payload.items():
        if key in forbidden_true and value is True:
            return key
        if key in {
            "runtime_use",
            "strategy_use",
            "paper_trading",
            "broker_execution",
        } and value == "AUTHORIZED":
            return key
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            return key
        if isinstance(value, Mapping):
            nested = _forbidden_output_field(value)
            if nested:
                return f"{key}.{nested}"
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, Mapping):
                    nested = _forbidden_output_field(item)
                    if nested:
                        return f"{key}[{index}].{nested}"
    return None


def _blocked_package(output_root: Path, reasons: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_V1,
        "review_status": FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "created_offline": True,
        "output_root": _path_text(output_root),
        "output_file_inspection_performed": False,
        "feature_label_refinement_results_review_created": False,
        "feature_label_refinement_results_review_ready": False,
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning": False,
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "feature_label_refinement_results_review_package_digest": "NOT_CREATED",
        "blocker_reasons": reasons,
        "blocker_count": len(reasons),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
    }


def _verify_outputs(
    output_root: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    payloads: dict[str, dict[str, Any]] = {}
    bindings: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        path = output_root / filename
        if not path.is_file():
            failures.append(
                {"failure_id": "missing_output_file", "filename": filename}
            )
    if failures:
        return payloads, bindings, failures

    try:
        payloads = {
            filename: _load_json(output_root / filename)
            for filename in EXPECTED_OUTPUT_FILENAMES
        }
    except FeatureLabelRefinementResultsReviewError as exc:
        return {}, [], [{"failure_id": "invalid_output_json", "message": str(exc)}]

    manifest = payloads["feature_label_refinement_execution_digest_manifest.json"]
    manifest_entries = {
        row.get("filename"): row
        for row in manifest.get("output_digest_entries", [])
        if isinstance(row, dict)
    }
    for filename in EXPECTED_OUTPUT_FILENAMES:
        path = output_root / filename
        actual = sha256_file(path)
        expected_local = EXPECTED_OUTPUT_DIGESTS[filename]
        manifest_entry = manifest_entries.get(filename)
        verification_status = PASS
        if actual != expected_local:
            verification_status = FAIL
            failures.append(
                {
                    "failure_id": "local_output_digest_mismatch",
                    "filename": filename,
                    "expected": expected_local,
                    "actual": actual,
                }
            )
        if filename == "feature_label_refinement_execution_digest_manifest.json":
            valid_manifest_entry = manifest_entry == {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
        else:
            valid_manifest_entry = manifest_entry == {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": actual,
            }
        if not valid_manifest_entry:
            verification_status = FAIL
            failures.append(
                {
                    "failure_id": "digest_manifest_entry_mismatch",
                    "filename": filename,
                }
            )
        payload = payloads[filename]
        if payload.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE:
            verification_status = FAIL
            failures.append(
                {"failure_id": "output_label_mismatch", "filename": filename}
            )
        if payload.get("evidence_scope") != FEATURE_LABEL_REFINEMENT_RESEARCH_ONLY:
            verification_status = FAIL
            failures.append(
                {"failure_id": "evidence_scope_mismatch", "filename": filename}
            )
        forbidden = _forbidden_output_field(payload)
        if forbidden:
            verification_status = FAIL
            failures.append(
                {
                    "failure_id": "forbidden_output_authority",
                    "filename": filename,
                    "field": forbidden,
                }
            )
        if _contains_sensitive_value(payload):
            verification_status = FAIL
            failures.append(
                {"failure_id": "sensitive_output_value", "filename": filename}
            )
        bindings.append(
            {
                "filename": filename,
                "local_sha256": actual,
                "recorded_digest_kind": manifest_entry.get("digest_kind")
                if manifest_entry
                else None,
                "recorded_sha256": manifest_entry.get("sha256")
                if manifest_entry
                else None,
                "verification_status": verification_status,
            }
        )
    return payloads, bindings, failures


def _base_package(
    *, output_root: Path, payloads: dict[str, dict[str, Any]], bindings: list[dict[str, Any]]
) -> dict[str, Any]:
    source = payloads["feature_label_refinement_execution_manifest.json"]
    label = payloads["refined_label_generation_report.json"]
    feature = payloads["refined_feature_generation_report.json"]
    protocol = payloads["refined_protocol_execution_report.json"]
    walk = payloads["refined_walk_forward_report.json"]
    oos = payloads["refined_out_of_sample_report.json"]
    model = payloads["refined_model_comparison_report.json"]
    leakage = payloads["refined_leakage_control_report.json"]
    per_ticker = payloads["per_ticker_refinement_execution_summary.json"]
    accuracies = sorted(
        row["accuracy"] for row in oos["results"]["model_metrics"].values()
    )
    output_digests = {
        row["filename"]: row["local_sha256"] for row in bindings
    }
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_V1,
        "review_status": FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE_READY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
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
        "refined_metrics_recomputation_rerun_performed": False,
        "model_comparison_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "source_execution_artifact_kind": source["artifact_kind"],
        "source_execution_status": source["execution_status"],
        "source_feature_label_refinement_execution_digest": source[
            "feature_label_refinement_execution_digest"
        ],
        "source_feature_label_refinement_execution_approval_digest": source[
            "source_evidence"
        ]["feature_label_refinement_execution_approval_digest"],
        "source_feature_label_refinement_execution_candidate_review_package_digest": source[
            "source_evidence"
        ]["feature_label_refinement_execution_candidate_review_package_digest"],
        "source_feature_label_refinement_execution_candidate_digest": source[
            "source_evidence"
        ]["feature_label_refinement_execution_candidate_digest"],
        "source_feature_label_refinement_plan_approval_digest": source[
            "source_evidence"
        ]["feature_label_refinement_plan_approval_digest"],
        "source_research_registry_approval_digest": source["source_evidence"][
            "research_registry_approval_digest"
        ],
        "source_canonical_dataset_freeze_digest": source["source_evidence"][
            "canonical_dataset_freeze_digest"
        ],
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "feature_label_refinement_executed": True,
        "feature_label_refinement_results_created": True,
        "refined_label_generation_authorized": True,
        "refined_label_generation_performed": True,
        "refined_feature_generation_authorized": True,
        "refined_feature_generation_performed": True,
        "refined_walk_forward_validation_authorized": True,
        "refined_walk_forward_validation_performed": True,
        "refined_out_of_sample_evaluation_authorized": True,
        "refined_out_of_sample_evaluation_performed": True,
        "refined_metrics_recomputation_authorized": True,
        "refined_metrics_recomputation_performed": True,
        "model_comparison_authorized": True,
        "model_comparison_performed": True,
        "feature_label_refinement_results_review_created": True,
        "feature_label_refinement_results_review_ready": True,
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning": True,
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "dataset_name": source["dataset_name"],
        "registry_approved_dataset_metadata": deepcopy(
            source["registry_approved_dataset_metadata"]
        ),
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "refined_label_family_count": source["refined_label_family_count"],
        "refined_feature_group_count": source["refined_feature_group_count"],
        "refined_feature_category_count": len(source["refined_feature_categories_generated"]),
        "refined_feature_field_count": feature["refined_feature_name_count"],
        "refined_protocol_group_count": source["refined_protocol_group_count"],
        "model_comparison_group_count": source["model_comparison_group_count"],
        "generated_output_count": source["generated_output_count"],
        "generated_output_names": list(source["generated_output_names"]),
        "output_root": _path_text(output_root),
        "output_file_inspection_performed": True,
        "output_digest_bindings": bindings,
        "output_digests": output_digests,
        "output_digest_verification_status": PASS,
        "outputs_research_only_non_actionable": True,
        "outputs_evidence_scope": FEATURE_LABEL_REFINEMENT_RESEARCH_ONLY,
        "digest_manifest_self_reference_policy": (
            "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
        ),
        "per_ticker_results_review_entries": deepcopy(per_ticker["entries"]),
        "refined_label_generation_review": {
            "coverage_entries": label["coverage_entry_count"],
            "available_values": label["available_count"],
            "unavailable_values": label["unavailable_count"],
            "refined_label_generation_digest": label[
                "refined_label_generation_digest"
            ],
            "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
        },
        "refined_feature_generation_review": {
            "feature_rows": feature["feature_matrix_row_count"],
            "feature_fields": feature["refined_feature_name_count"],
            "null_or_unavailable_values": feature[
                "total_null_or_unavailable_count"
            ],
            "refined_feature_generation_digest": feature[
                "refined_feature_generation_digest"
            ],
            "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
        },
        "refined_protocol_review": {
            "chronological_splits": True,
            "one_session_embargo": True,
            "no_shuffle": protocol["no_shuffle"],
            "no_lookahead": protocol["no_lookahead_leakage"],
            "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
        },
        "refined_walk_forward_review": {
            "fold_count": walk["fold_count"],
            "evaluation_rows": source["refined_walk_forward_summary"][
                "evaluation_row_count"
            ],
            "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
        },
        "refined_out_of_sample_review": {
            "evaluation_rows": oos["results"]["evaluation_row_count"],
            "accuracy_min": accuracies[0],
            "accuracy_max": accuracies[-1],
            "accuracy_range": f"{accuracies[0]} to {accuracies[-1]}",
            "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
        },
        "refined_metric_review": {
            "metrics_recomputed": True,
            "model_count": source["refined_metric_summary"]["model_count"],
            "acceptance_conclusion": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED",
        },
        "model_comparison_review": {
            "group_count": model["model_comparison_group_count"],
            "deterministic_comparisons_evaluated": len(
                model["deterministic_comparison_ids"]
            ),
            "unavailable_model_family_requests": source[
                "model_comparison_summary"
            ]["unavailable_model_family_count"],
            "unavailable_model_family_status": (
                execution.NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE
            ),
            "interpretation": "RESEARCH_ONLY_REQUIRES_OPERATOR_REVIEW",
        },
        "refined_leakage_control_review": {
            "status": leakage["leakage_control_status"],
            "failed_controls": leakage["failed_control_count"],
        },
        "data_quality_review": {
            "status": source["data_quality_summary"]["status"],
            "failure_count": source["failure_count"],
            "warning_count": source["warning_count"],
            "warning": "META_REDUCED_RECORD_COUNT_PRESERVED_EXACTLY_913",
        },
        "feature_label_refinement_results_available": True,
        "feature_label_refinement_outputs_verified": True,
        "refined_label_generation_results_available": True,
        "refined_feature_generation_results_available": True,
        "refined_protocol_results_available": True,
        "refined_walk_forward_results_available": True,
        "refined_out_of_sample_results_available": True,
        "refined_metrics_results_available": True,
        "model_comparison_results_available": True,
        "refined_leakage_control_passed": True,
        "refinement_results_support_future_additional_predictive_evidence_planning": True,
        "refinement_results_create_additional_predictive_evidence_execution_candidate": False,
        "refinement_results_create_predictive_usefulness_acceptance": False,
        "refinement_results_create_profitability_acceptance": False,
        "refinement_results_create_runtime_authority": False,
        "refinement_results_create_trade_recommendations": False,
        "refinement_performance_interpretation": (
            "WEAK_OR_MIXED_REQUIRES_FUTURE_REVIEW"
        ),
        "refined_oos_accuracy_interpretation": (
            "LOW_TO_MIXED_NOT_ACCEPTANCE_EVIDENCE"
        ),
        "model_comparison_interpretation": (
            "RESEARCH_ONLY_REQUIRES_OPERATOR_REVIEW"
        ),
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
        "operator_review_required": True,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "additional_predictive_evidence_execution_candidate_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
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
    values = {
        "feature_label_refinement_execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, package.get("source_feature_label_refinement_execution_digest")),
        "feature_label_refinement_execution_approval_digest_bound": (EXPECTED_EXECUTION_APPROVAL_DIGEST, package.get("source_feature_label_refinement_execution_approval_digest")),
        "feature_label_refinement_execution_candidate_review_digest_bound": (EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("source_feature_label_refinement_execution_candidate_review_package_digest")),
        "research_registry_approval_digest_bound": (EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, package.get("source_research_registry_approval_digest")),
        "canonical_dataset_freeze_digest_bound": (EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, package.get("source_canonical_dataset_freeze_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        "target_universe_count_12": (12, package.get("target_universe_count")),
        "target_universe_matches_execution_universe": (EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        "total_canonical_record_count_11946": (11946, package.get("total_canonical_record_count")),
        "meta_record_count_913_preserved": (913, package.get("meta_record_count")),
        "non_meta_record_counts_1003_preserved": (True, all(package.get("per_ticker_record_counts", {}).get(ticker) == 1003 for ticker in EXPECTED_TARGET_UNIVERSE if ticker != "META")),
        "generated_output_count_12": (12, package.get("generated_output_count")),
        "output_digests_bound": (EXPECTED_OUTPUT_DIGESTS, package.get("output_digests")),
        "outputs_research_only_non_actionable": (True, package.get("outputs_research_only_non_actionable")),
        "digest_manifest_self_reference_non_applicable": ("SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", package.get("digest_manifest_self_reference_policy")),
        "refined_label_family_count_7": (7, package.get("refined_label_family_count")),
        "refined_feature_group_count_9": (9, package.get("refined_feature_group_count")),
        "refined_feature_fields_19": (19, package.get("refined_feature_field_count")),
        "refined_protocol_group_count_6": (6, package.get("refined_protocol_group_count")),
        "model_comparison_group_count_5": (5, package.get("model_comparison_group_count")),
        "refined_label_generation_digest_bound": ("04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8", package.get("refined_label_generation_review", {}).get("refined_label_generation_digest")),
        "refined_feature_generation_digest_bound": ("35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00", package.get("refined_feature_generation_review", {}).get("refined_feature_generation_digest")),
        "refined_label_coverage_summary_bound": ({"coverage_entries": 84, "available_values": 82698, "unavailable_values": 924}, {key: package.get("refined_label_generation_review", {}).get(key) for key in ("coverage_entries", "available_values", "unavailable_values")}),
        "refined_feature_coverage_summary_bound": ({"feature_rows": 11946, "feature_fields": 19, "null_or_unavailable_values": 1128}, {key: package.get("refined_feature_generation_review", {}).get(key) for key in ("feature_rows", "feature_fields", "null_or_unavailable_values")}),
        "refined_walk_forward_fold_count_4": (4, package.get("refined_walk_forward_review", {}).get("fold_count")),
        "refined_walk_forward_rows_3024": (3024, package.get("refined_walk_forward_review", {}).get("evaluation_rows")),
        "refined_oos_rows_2988": (2988, package.get("refined_out_of_sample_review", {}).get("evaluation_rows")),
        "refined_oos_accuracy_range_bound": ("0.119813 to 0.480924", package.get("refined_out_of_sample_review", {}).get("accuracy_range")),
        "model_comparison_summary_bound": ({"group_count": 5, "deterministic_comparisons_evaluated": 7, "unavailable_model_family_requests": 3}, {key: package.get("model_comparison_review", {}).get(key) for key in ("group_count", "deterministic_comparisons_evaluated", "unavailable_model_family_requests")}),
        "unavailable_model_families_recorded": (execution.NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE, package.get("model_comparison_review", {}).get("unavailable_model_family_status")),
        "refined_leakage_status_pass": (PASS, package.get("refined_leakage_control_review", {}).get("status")),
        "failed_leakage_controls_zero": (0, package.get("refined_leakage_control_review", {}).get("failed_controls")),
        "data_quality_pass_with_preserved_limitation": ("PASS_WITH_PRESERVED_SOURCE_LIMITATION", package.get("data_quality_review", {}).get("status")),
        "limitations_recorded": (LIMITATIONS, package.get("limitations")),
        "next_gates_defined": (NEXT_GATES, package.get("next_gates")),
    }
    false_checks = {
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
        "refined_metrics_recomputation_performed_false": "refined_metrics_recomputation_rerun_performed",
        "model_comparison_rerun_performed_false": "model_comparison_rerun_performed",
        "raw_provider_payloads_not_committed": "raw_provider_payloads_committed",
        "api_keys_not_stored_or_printed": "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_created_false": "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "predictive_usefulness_acceptance_candidate_created_false": "predictive_usefulness_acceptance_candidate_created",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "results_create_additional_predictive_evidence_execution_candidate_false": "refinement_results_create_additional_predictive_evidence_execution_candidate",
        "results_create_predictive_usefulness_acceptance_false": "refinement_results_create_predictive_usefulness_acceptance",
        "results_create_profitability_acceptance_false": "refinement_results_create_profitability_acceptance",
        "results_create_runtime_authority_false": "refinement_results_create_runtime_authority",
        "no_additional_predictive_evidence_execution_candidate_created": "additional_predictive_evidence_execution_candidate_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    true_checks = {
        "feature_label_refinement_executed_true": "feature_label_refinement_executed",
        "feature_label_refinement_results_created_true": "feature_label_refinement_results_created",
        "refined_label_generation_performed_true": "refined_label_generation_performed",
        "refined_feature_generation_performed_true": "refined_feature_generation_performed",
        "refined_walk_forward_validation_performed_true": "refined_walk_forward_validation_performed",
        "refined_out_of_sample_evaluation_performed_true": "refined_out_of_sample_evaluation_performed",
        "refined_metrics_recomputation_performed_true": "refined_metrics_recomputation_performed",
        "model_comparison_performed_true": "model_comparison_performed",
        "results_support_future_additional_predictive_evidence_planning_true": "refinement_results_support_future_additional_predictive_evidence_planning",
    }
    values.update(
        {check_id: (False, package.get(field)) for check_id, field in false_checks.items()}
    )
    values.update(
        {check_id: (True, package.get(field)) for check_id, field in true_checks.items()}
    )
    values.update(
        {
            "predictive_usefulness_not_accepted": (NOT_ACCEPTED, package.get("predictive_usefulness")),
            "profitability_not_accepted": (NOT_ACCEPTED, package.get("profitability")),
            "runtime_use_not_authorized": (NOT_AUTHORIZED, package.get("runtime_use")),
            "strategy_use_not_authorized": (NOT_AUTHORIZED, package.get("strategy_use")),
            "paper_trading_not_authorized": (NOT_AUTHORIZED, package.get("paper_trading")),
            "broker_execution_not_authorized": (NOT_AUTHORIZED, package.get("broker_execution")),
        }
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_review": not failed,
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence": not failed,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("feature_label_refinement_results_review_package_digest", None)
    if "output_root" in payload:
        payload["output_root"] = DEFAULT_OUTPUT_ROOT.as_posix()
    return payload


def feature_label_refinement_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return a deterministic output-location-independent review digest."""
    return semantic_digest(_digest_payload(review_package))


def build_feature_label_refinement_results_review_package_v1(
    *, output_root: str | Path | None = None
) -> dict[str, Any]:
    """Inspect and review existing refinement outputs without rerunning them."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    try:
        execution.validate_feature_label_refinement_executed_v1(
            payloads["feature_label_refinement_execution_manifest.json"]
        )
    except execution.FeatureLabelRefinementExecutionError as exc:
        return _blocked_package(
            root,
            [{"failure_id": "invalid_source_execution_artifact", "message": str(exc)}],
        )
    package = _base_package(output_root=root, payloads=payloads, bindings=bindings)
    package["review_checklist"] = _review_checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    if package["review_summary"]["blocker_count"]:
        return _blocked_package(
            root,
            [
                {
                    "failure_id": "review_check_failed",
                    "check_id": row["check_id"],
                }
                for row in package["review_checklist"]
                if row["status"] != PASS
            ],
        )
    package["feature_label_refinement_results_review_package_digest"] = (
        feature_label_refinement_results_review_package_digest_v1(package)
    )
    validate_feature_label_refinement_results_review_package_v1(package)
    return package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise FeatureLabelRefinementResultsReviewError(
                    f"{current} must not emit {item}"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise FeatureLabelRefinementResultsReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise FeatureLabelRefinementResultsReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureLabelRefinementResultsReviewError(f"{field} mismatch")


def validate_feature_label_refinement_results_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Validate ready or blocked review packages without touching source outputs."""
    if not isinstance(review_package, dict):
        raise FeatureLabelRefinementResultsReviewError(
            "feature/label refinement results review package must be a JSON object"
        )
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_V1,
        "schema_version",
    )
    if (
        review_package.get("review_status")
        == FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    ):
        _expect(
            review_package.get("feature_label_refinement_results_review_ready"),
            False,
            "blocked review ready",
        )
        _expect(
            review_package.get("additional_predictive_evidence_execution_candidate_created"),
            False,
            "blocked candidate created",
        )
        _expect(
            review_package.get("feature_label_refinement_results_review_package_digest"),
            "NOT_CREATED",
            "blocked review digest",
        )
        return {
            "status": "FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_VALID",
            "review_status": review_package["review_status"],
            "blocker_count": review_package.get("blocker_count", 0),
        }
    _expect(
        review_package.get("review_status"),
        FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE_READY,
        "review_status",
    )
    _reject_forbidden_values(review_package)
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTED,
        "source_execution_status": execution.FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY,
        "source_feature_label_refinement_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_feature_label_refinement_execution_approval_digest": EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "source_feature_label_refinement_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "source_canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "refined_label_family_count": 7,
        "refined_feature_group_count": 9,
        "refined_feature_category_count": 11,
        "refined_feature_field_count": 19,
        "refined_protocol_group_count": 6,
        "model_comparison_group_count": 5,
        "generated_output_count": 12,
        "generated_output_names": EXPECTED_OUTPUT_FILENAMES,
        "output_digests": EXPECTED_OUTPUT_DIGESTS,
        "outputs_research_only_non_actionable": True,
        "outputs_evidence_scope": FEATURE_LABEL_REFINEMENT_RESEARCH_ONLY,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
    true_fields = [
        "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized",
        "feature_label_refinement_executed",
        "feature_label_refinement_results_created",
        "refined_label_generation_authorized",
        "refined_label_generation_performed",
        "refined_feature_generation_authorized",
        "refined_feature_generation_performed",
        "refined_walk_forward_validation_authorized",
        "refined_walk_forward_validation_performed",
        "refined_out_of_sample_evaluation_authorized",
        "refined_out_of_sample_evaluation_performed",
        "refined_metrics_recomputation_authorized",
        "refined_metrics_recomputation_performed",
        "model_comparison_authorized",
        "model_comparison_performed",
        "feature_label_refinement_results_review_created",
        "feature_label_refinement_results_review_ready",
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning",
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence",
        "output_file_inspection_performed",
        "feature_label_refinement_outputs_verified",
        "refinement_results_support_future_additional_predictive_evidence_planning",
        "research_only",
        "operator_review_required",
    ]
    false_fields = [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_validation_rerun_performed",
        "refined_out_of_sample_evaluation_rerun_performed",
        "refined_metrics_recomputation_rerun_performed",
        "model_comparison_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
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
        "refinement_results_create_additional_predictive_evidence_execution_candidate",
        "refinement_results_create_predictive_usefulness_acceptance",
        "refinement_results_create_profitability_acceptance",
        "refinement_results_create_runtime_authority",
        "refinement_results_create_trade_recommendations",
    ]
    for field in true_fields:
        _expect(review_package.get(field), True, field)
    for field in false_fields:
        _expect(review_package.get(field), False, field)
    _expect(review_package.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    _expect(
        review_package.get("refined_label_generation_review"),
        {
            "coverage_entries": 84,
            "available_values": 82698,
            "unavailable_values": 924,
            "refined_label_generation_digest": "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8",
            "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
        },
        "refined_label_generation_review",
    )
    _expect(
        review_package.get("refined_feature_generation_review"),
        {
            "feature_rows": 11946,
            "feature_fields": 19,
            "null_or_unavailable_values": 1128,
            "refined_feature_generation_digest": "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00",
            "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
        },
        "refined_feature_generation_review",
    )
    _expect(review_package.get("refined_walk_forward_review", {}).get("fold_count"), 4, "walk-forward fold count")
    _expect(review_package.get("refined_walk_forward_review", {}).get("evaluation_rows"), 3024, "walk-forward rows")
    _expect(review_package.get("refined_out_of_sample_review", {}).get("evaluation_rows"), 2988, "OOS rows")
    _expect(review_package.get("refined_out_of_sample_review", {}).get("accuracy_range"), "0.119813 to 0.480924", "OOS accuracy range")
    _expect(review_package.get("refined_leakage_control_review"), {"status": PASS, "failed_controls": 0}, "leakage review")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise FeatureLabelRefinementResultsReviewError("review_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review checklist IDs")
    _expect(checklist, _review_checklist(review_package), "review checklist")
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get("feature_label_refinement_results_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureLabelRefinementResultsReviewError("review package digest missing")
    _expect(
        digest,
        feature_label_refinement_results_review_package_digest_v1(review_package),
        "review package digest",
    )
    return {
        "status": FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "feature_label_refinement_results_review_package_digest": digest,
        "source_feature_label_refinement_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "generated_output_count": 12,
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_review": True,
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_feature_label_refinement_results_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized review summary without reproducing source evidence."""
    validation = validate_feature_label_refinement_results_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Feature/Label Refinement Results Review Status",
        "",
        "## Title",
        "- Feature/Label Refinement Results Review Package v1.",
        "",
        "## Feature/Label Refinement Results Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
        f"- Review digest: `{validation['feature_label_refinement_results_review_package_digest']}`.",
        "",
        "## Source Feature/Label Refinement Execution",
        f"- Execution/status/digest: `{review_package['source_execution_artifact_kind']}` / `{review_package['source_execution_status']}` / `{review_package['source_feature_label_refinement_execution_digest']}`.",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/records: `{review_package['dataset_name']}` / `{review_package['total_canonical_record_count']}`.",
        "",
        "## Target Universe",
        f"- `{', '.join(review_package['target_universe'])}`; META remains `{review_package['meta_record_count']}` records.",
        "",
        "## Refined Label Generation Review",
        f"- Coverage/available/unavailable: `{review_package['refined_label_generation_review']['coverage_entries']}` / `{review_package['refined_label_generation_review']['available_values']}` / `{review_package['refined_label_generation_review']['unavailable_values']}`.",
        "",
        "## Refined Feature Generation Review",
        f"- Rows/fields/nulls: `{review_package['refined_feature_generation_review']['feature_rows']}` / `{review_package['refined_feature_generation_review']['feature_fields']}` / `{review_package['refined_feature_generation_review']['null_or_unavailable_values']}`.",
        "",
        "## Refined Protocol Review",
        "- Chronological splits, one-session embargo, no shuffle, and no lookahead are preserved.",
        "",
        "## Refined Walk-Forward Review",
        f"- Folds/evaluation rows: `{review_package['refined_walk_forward_review']['fold_count']}` / `{review_package['refined_walk_forward_review']['evaluation_rows']}`.",
        "",
        "## Refined OOS Review",
        f"- Rows/accuracy range: `{review_package['refined_out_of_sample_review']['evaluation_rows']}` / `{review_package['refined_out_of_sample_review']['accuracy_range']}`.",
        "",
        "## Refined Metrics Review",
        "- Metrics remain research-only and not acceptance evidence.",
        "",
        "## Model Comparison Review",
        f"- Groups/comparisons/unavailable families: `{review_package['model_comparison_review']['group_count']}` / `{review_package['model_comparison_review']['deterministic_comparisons_evaluated']}` / `{review_package['model_comparison_review']['unavailable_model_family_requests']}`.",
        "",
        "## Refined Leakage-Control Review",
        f"- Status/failed controls: `{review_package['refined_leakage_control_review']['status']}` / `{review_package['refined_leakage_control_review']['failed_controls']}`.",
        "",
        "## Data Quality Review",
        f"- Status/failures/warnings: `{review_package['data_quality_review']['status']}` / `{review_package['data_quality_review']['failure_count']}` / `{review_package['data_quality_review']['warning_count']}`.",
        "",
        "## Output Digest Manifest",
        f"- Root/count/status: `{review_package['output_root']}` / `{review_package['generated_output_count']}` / `{review_package['output_digest_verification_status']}`.",
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
            f"- Predictive usefulness remains `{review_package['predictive_usefulness']}`; no acceptance candidate exists.",
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
            "- Review inspected and hashed existing ignored outputs only. It made no provider request and performed no execution, regeneration, recomputation, model rerun, strategy scoring, recommendation, acceptance, or runtime activation.",
            "- Readiness for future planning does not create an additional predictive-evidence execution candidate.",
            "- Next task: Additional Predictive Evidence Execution Candidate for Refined Evidence v1.",
            "",
        ]
    )
    return "\n".join(lines)


def write_feature_label_refinement_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting existing evidence."""
    package = build_feature_label_refinement_results_review_package_v1(
        output_root=output_root
    )
    validate_feature_label_refinement_results_review_package_v1(package)
    output_name = filename or "feature_label_refinement_results_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureLabelRefinementResultsReviewError(
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
        raise FeatureLabelRefinementResultsReviewError(
            "results review output already exists"
        ) from exc
    return {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": package["review_status"],
        "feature_label_refinement_results_review_package_digest": package[
            "feature_label_refinement_results_review_package_digest"
        ],
    }
