"""Offline, digest-bound review of label-objective redesign planning outputs."""

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
from marketflow.services import label_objective_redesign_execution_service as execution


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE = (
    "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_V1 = (
    "label_objective_redesign_results_review_v1"
)
LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY = (
    "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY"
)
LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_VALID = (
    "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_VALID"
)

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
DEFAULT_BRANCH = "feature/label-objective-redesign-results-review-v1"
DEFAULT_BASE_COMMIT = "11cacf31ecafc190a4662c8193e904a851083bf0"
EXPECTED_EXECUTION_DIGEST = (
    "d43bb214850f8068b445d1620ae8f4f948162eda309f04acf6fdd7b73abd63a4"
)
EXPECTED_OUTPUT_DIGESTS = {
    "label_objective_redesign_execution_manifest.json": "f99cd1de2ba09641246c7b0c7dd25009e1d51a9cf108937de04720634ce6cb48",
    "label_family_candidate_matrix.json": "551dd9a1ffbe1145313ed39b3b9b5f8d4e0d0e131f9e0d8fd882b37a9295d6bc",
    "threshold_design_matrix.json": "20c21b30f2a850a1292ad6f18bc456d0ac8a9dbb3ed7d3441a36ef571500fbf1",
    "horizon_design_matrix.json": "d4e27075f502fa5d6eefcbfbb13d006a320000a08914a424377af66e4ab95b76",
    "per_ticker_label_objective_plan.json": "b8dbb1ef35afbc77fa38840378ce56ece46123d21ab345b342fbcc2acc88544b",
    "label_availability_boundary_plan.json": "1cb26b84a51ce6ec2b92010d187373f494e21b43b274348ca6dea7c21aa5121b",
    "meta_limitation_preservation_plan.json": "3c1dda906a95a7c57efb981d4e685e80e89bb937c135bb3964247c6a558cbb36",
    "operator_review_summary_template.json": "957687b2b5d1714a4efa44d18bb6af69558156dbfcbb52ebcb1a16465208c033",
}
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

LIMITATIONS = [
    "results_are_planning_artifacts_only",
    "actual_redesigned_labels_not_generated",
    "redesigned_label_generation_not_authorized",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "trade_recommendations_not_generated",
    "meta_reduced_record_count_preserved",
    "operator_review_required_before_redesigned_label_generation_candidate",
    "operator_approval_required_before_any_label_generation",
]
NEXT_CHAIN = [
    "Redesigned Label Generation Candidate v1.",
    "Redesigned Label Generation Candidate Operator Review Package v1.",
    "Redesigned Label Generation Approval v1, if selected.",
    "Redesigned Label Generation Execution v1.",
    "Redesigned Label Generation Results Review v1.",
    "Additional Predictive Evidence Execution Candidate using redesigned labels, if results support it.",
    "Additional Predictive Evidence Execution and Results Review, if separately approved.",
    "Predictive Usefulness Reassessment and Readiness Review, only after new evidence.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "redesigned_label_generation_candidate",
    "redesigned_label_generation_candidate_operator_review",
    "redesigned_label_generation_approval_if_selected",
    "redesigned_label_generation_execution",
    "redesigned_label_generation_results_review",
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_generate_labels",
    "review_does_not_authorize_label_generation",
    "review_does_not_authorize_execution",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "preserve_meta_record_limitation",
    "no_more_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]
REQUIRED_CHECK_IDS = [
    "execution_digest_bound",
    "execution_approval_digest_bound",
    "execution_candidate_review_digest_bound",
    "execution_candidate_digest_bound",
    "redesign_approval_digest_bound",
    "candidate_review_digest_bound",
    "operator_method_path_selection_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "source_execution_status_research_only",
    "generated_output_count_8",
    "output_digests_bound",
    "output_digest_mismatch_count_zero",
    "outputs_research_only_non_actionable",
    "label_family_candidate_matrix_verified",
    "threshold_design_matrix_verified",
    "horizon_design_matrix_verified",
    "per_ticker_plan_verified",
    "label_availability_boundary_plan_verified",
    "meta_limitation_preservation_plan_verified",
    "candidate_label_family_count_10",
    "threshold_design_strategy_count_7",
    "horizon_design_candidate_count_5",
    "per_ticker_plan_count_12",
    "results_review_created_true",
    "results_review_ready_true",
    "ready_for_redesigned_label_generation_candidate_true",
    "redesigned_label_generation_candidate_created_false",
    "actual_labels_generated_false",
    "redesigned_label_generation_authorized_false",
    "redesigned_label_generation_performed_false",
    "features_generated_false",
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
    "label_objective_redesign_execution_rerun_false",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "limitations_recorded",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class LabelObjectiveRedesignResultsReviewError(ValueError):
    """Raised when redesign outputs cannot support a valid review package."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LabelObjectiveRedesignResultsReviewError(
            f"{path.name} is not readable JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise LabelObjectiveRedesignResultsReviewError(
            f"{path.name} must contain a JSON object"
        )
    return payload


def _source_evidence() -> dict[str, str]:
    return {
        "label_objective_redesign_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "label_objective_redesign_execution_approval_digest": execution.EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "label_objective_redesign_execution_candidate_review_package_digest": execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "label_objective_redesign_execution_candidate_digest": execution.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "label_objective_redesign_approval_digest": execution.EXPECTED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_DIGEST,
        "label_objective_redesign_candidate_review_package_digest": execution.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_method_path_selection_digest": execution.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "research_registry_approval_digest": execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
    }


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
        "label_generation_authorized",
        "label_generation_performed",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "additional_predictive_evidence_execution_candidate_created",
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


def _blocked_package(output_root: Path, reasons: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_V1,
        "review_status": LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_root": _path_text(output_root),
        "output_file_inspection_performed": False,
        "label_objective_redesign_results_review_created": False,
        "label_objective_redesign_results_review_ready": False,
        "ready_for_redesigned_label_generation_candidate": False,
        "redesigned_label_generation_candidate_created": False,
        "redesigned_label_generation_authorized": False,
        "redesigned_label_generation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "label_objective_redesign_results_review_package_digest": "NOT_CREATED",
        "blocker_reasons": reasons,
        "blocker_count": len(reasons),
    }


def _verify_outputs(
    output_root: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        if not (output_root / filename).is_file():
            failures.append({"failure_id": "missing_output_file", "filename": filename})
    if failures:
        return {}, [], failures
    try:
        payloads = {
            filename: _load_json(output_root / filename)
            for filename in EXPECTED_OUTPUT_FILENAMES
        }
    except LabelObjectiveRedesignResultsReviewError as exc:
        return {}, [], [{"failure_id": "invalid_output_json", "message": str(exc)}]

    source = payloads[EXPECTED_OUTPUT_FILENAMES[0]]
    entries = {
        row.get("filename"): row
        for row in source.get("output_digest_manifest", [])
        if isinstance(row, dict)
    }
    bindings: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        actual = sha256_file(output_root / filename)
        expected = EXPECTED_OUTPUT_DIGESTS[filename]
        entry = entries.get(filename)
        status = PASS
        if actual != expected:
            status = FAIL
            failures.append({
                "failure_id": "local_output_digest_mismatch",
                "filename": filename,
                "expected": expected,
                "actual": actual,
            })
        if filename == EXPECTED_OUTPUT_FILENAMES[0]:
            valid_entry = entry == {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
        else:
            valid_entry = entry == {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": actual,
            }
        if not valid_entry:
            status = FAIL
            failures.append({"failure_id": "digest_manifest_entry_mismatch", "filename": filename})
        payload = payloads[filename]
        if payload.get("output_label") != execution.OUTPUT_LABEL:
            status = FAIL
            failures.append({"failure_id": "output_label_mismatch", "filename": filename})
        if payload.get("evidence_scope") != execution.EVIDENCE_SCOPE:
            status = FAIL
            failures.append({"failure_id": "evidence_scope_mismatch", "filename": filename})
        forbidden = _forbidden_output_field(payload)
        if forbidden:
            status = FAIL
            failures.append({"failure_id": "forbidden_output_authority", "filename": filename, "field": forbidden})
        if _contains_sensitive_value(payload):
            status = FAIL
            failures.append({"failure_id": "sensitive_output_value", "filename": filename})
        bindings.append({
            "filename": filename,
            "local_sha256": actual,
            "recorded_digest_kind": entry.get("digest_kind") if entry else None,
            "recorded_sha256": entry.get("sha256") if entry else None,
            "verification_status": status,
        })
    return payloads, bindings, failures


def _base_package(
    output_root: Path,
    payloads: dict[str, dict[str, Any]],
    bindings: list[dict[str, Any]],
) -> dict[str, Any]:
    source = payloads["label_objective_redesign_execution_manifest.json"]
    family = payloads["label_family_candidate_matrix.json"]
    threshold = payloads["threshold_design_matrix.json"]
    horizon = payloads["horizon_design_matrix.json"]
    per_ticker = payloads["per_ticker_label_objective_plan.json"]
    availability = payloads["label_availability_boundary_plan.json"]
    meta = payloads["meta_limitation_preservation_plan.json"]
    operator = payloads["operator_review_summary_template.json"]
    output_digests = {row["filename"]: row["local_sha256"] for row in bindings}
    source_evidence = _source_evidence()
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_V1,
        "review_status": LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY,
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
        "predictive_evidence_rerun_performed": False,
        "refined_evidence_rerun_performed": False,
        "label_generation_performed": False,
        "redesigned_label_generation_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "source_execution_artifact_kind": source["artifact_kind"],
        "source_execution_status": source["execution_status"],
        "source_label_objective_redesign_execution_digest": source["label_objective_redesign_execution_digest"],
        "source_label_objective_redesign_execution_approval_digest": source_evidence["label_objective_redesign_execution_approval_digest"],
        "source_label_objective_redesign_execution_candidate_review_package_digest": source_evidence["label_objective_redesign_execution_candidate_review_package_digest"],
        "source_label_objective_redesign_execution_candidate_digest": source_evidence["label_objective_redesign_execution_candidate_digest"],
        "source_label_objective_redesign_approval_digest": source_evidence["label_objective_redesign_approval_digest"],
        "source_label_objective_redesign_candidate_review_package_digest": source_evidence["label_objective_redesign_candidate_review_package_digest"],
        "source_operator_method_path_selection_digest": source_evidence["operator_method_path_selection_digest"],
        "source_research_registry_approval_digest": source_evidence["research_registry_approval_digest"],
        "source_evidence": source_evidence,
        "label_objective_redesign_execution_approved": True,
        "label_objective_redesign_authorized": True,
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "label_objective_redesign_results_review_created": True,
        "label_objective_redesign_results_review_ready": True,
        "ready_for_redesigned_label_generation_candidate": True,
        "redesigned_label_generation_candidate_created": False,
        "redesigned_label_generation_authorized": False,
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
        "generated_planning_outputs": [Path(name).stem for name in EXPECTED_OUTPUT_FILENAMES],
        "candidate_label_family_count": family["candidate_label_family_count"],
        "threshold_design_strategy_count": threshold["threshold_design_strategy_count"],
        "horizon_design_candidate_count": horizon["horizon_design_candidate_count"],
        "per_ticker_plan_count": per_ticker["per_ticker_plan_count"],
        "output_root": _path_text(output_root),
        "output_file_inspection_performed": True,
        "output_digest_bindings": bindings,
        "output_digests": output_digests,
        "non_self_output_digest_match_count": sum(
            row["verification_status"] == PASS and row["recorded_digest_kind"] == "FILE_SHA256"
            for row in bindings
        ),
        "output_digest_mismatch_count": sum(row["verification_status"] != PASS for row in bindings),
        "output_digest_verification_status": PASS,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "outputs_research_only_non_actionable": True,
        "outputs_evidence_scope": execution.EVIDENCE_SCOPE,
        "label_family_candidate_matrix_review": {
            "available": True,
            "candidate_count": family["candidate_label_family_count"],
            "generation_status": "NOT_GENERATED",
            "authorization_status": "NOT_AUTHORIZED_FOR_LABEL_GENERATION",
            "verified": all(row["generation_status"] == execution.NOT_GENERATED and row["authorization_status"] == execution.NOT_AUTHORIZED_FOR_LABEL_GENERATION for row in family["label_family_candidates"]),
        },
        "threshold_design_matrix_review": {
            "available": True,
            "strategy_count": threshold["threshold_design_strategy_count"],
            "final_thresholds_computed": any(row["final_threshold_computed"] for row in threshold["threshold_design_strategies"]),
            "verified": all(row["status"] == execution.DESIGN_ONLY_NOT_EXECUTED and not row["final_threshold_computed"] for row in threshold["threshold_design_strategies"]),
        },
        "horizon_design_matrix_review": {
            "available": True,
            "candidate_count": horizon["horizon_design_candidate_count"],
            "final_horizon_selected": any(row["final_horizon_selected"] for row in horizon["horizon_design_candidates"]),
            "verified": all(row["status"] == execution.DESIGN_ONLY_NOT_EXECUTED and not row["final_horizon_selected"] for row in horizon["horizon_design_candidates"]),
        },
        "per_ticker_label_objective_plan_review": {
            "available": True,
            "plan_count": per_ticker["per_ticker_plan_count"],
            "target_universe": list(per_ticker["target_universe"]),
            "verified": all(row["execution_status"] == execution.NOT_EXECUTED and not row["label_generation_performed"] for row in per_ticker["per_ticker_label_objective_plans"]),
        },
        "label_availability_boundary_plan_review": {
            "available": True,
            "rule_count": len(availability["availability_rules"]),
            "verified": availability["plan_status"] == execution.DESIGN_ONLY_NOT_EXECUTED and not availability["label_generation_authorized"] and not availability["label_generation_performed"],
        },
        "meta_limitation_preservation_plan_review": {
            "available": True,
            "ticker": meta["ticker"],
            "record_count": meta["historical_record_count"],
            "no_backfill": meta["no_backfill"],
            "no_repair": meta["no_repair"],
            "no_synthetic_rows": meta["no_synthetic_rows"],
            "verified": meta["ticker"] == "META" and meta["historical_record_count"] == 913 and meta["no_backfill"] and meta["no_repair"] and meta["no_synthetic_rows"],
        },
        "operator_review_summary_template_review": {
            "available": True,
            "operator_decision": operator["operator_decision"],
            "verified": operator["review_status"] == "AWAITING_SEPARATE_RESULTS_REVIEW" and operator["operator_decision"] is None and not operator["results_review_created"],
        },
        "label_objective_redesign_planning_outputs_available": True,
        "label_objective_redesign_outputs_verified": True,
        "label_family_candidate_matrix_available": True,
        "threshold_design_matrix_available": True,
        "horizon_design_matrix_available": True,
        "per_ticker_label_objective_plan_available": True,
        "label_availability_boundary_plan_available": True,
        "meta_limitation_preservation_plan_available": True,
        "results_support_future_redesigned_label_generation_candidate": True,
        "results_create_redesigned_label_generation_candidate": False,
        "results_create_actual_labels": False,
        "results_create_features": False,
        "results_create_predictive_evidence": False,
        "results_create_predictive_usefulness_acceptance": False,
        "results_create_profitability_acceptance": False,
        "results_create_runtime_authority": False,
        "planning_output_interpretation": "DESIGN_ARTIFACTS_READY_FOR_OPERATOR_REVIEW",
        "label_generation_interpretation": "NOT_GENERATED_NOT_AUTHORIZED",
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
    source = _source_evidence()
    values: dict[str, tuple[Any, Any]] = {
        "execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, package.get("source_label_objective_redesign_execution_digest")),
        "execution_approval_digest_bound": (source["label_objective_redesign_execution_approval_digest"], package.get("source_label_objective_redesign_execution_approval_digest")),
        "execution_candidate_review_digest_bound": (source["label_objective_redesign_execution_candidate_review_package_digest"], package.get("source_label_objective_redesign_execution_candidate_review_package_digest")),
        "execution_candidate_digest_bound": (source["label_objective_redesign_execution_candidate_digest"], package.get("source_label_objective_redesign_execution_candidate_digest")),
        "redesign_approval_digest_bound": (source["label_objective_redesign_approval_digest"], package.get("source_label_objective_redesign_approval_digest")),
        "candidate_review_digest_bound": (source["label_objective_redesign_candidate_review_package_digest"], package.get("source_label_objective_redesign_candidate_review_package_digest")),
        "operator_method_path_selection_digest_bound": (source["operator_method_path_selection_digest"], package.get("source_operator_method_path_selection_digest")),
        "research_registry_digest_bound": (source["research_registry_approval_digest"], package.get("source_research_registry_approval_digest")),
        "records_digest_bound": (source["records_digest"], package.get("records_digest")),
        "target_universe_12_preserved": (EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        "records_digest_preserved": (execution.EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        "meta_913_preserved": (913, package.get("meta_record_count")),
        "source_execution_status_research_only": (execution.LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY, package.get("source_execution_status")),
        "generated_output_count_8": (8, package.get("generated_output_count")),
        "output_digests_bound": (EXPECTED_OUTPUT_DIGESTS, package.get("output_digests")),
        "output_digest_mismatch_count_zero": (0, package.get("output_digest_mismatch_count")),
        "outputs_research_only_non_actionable": (True, package.get("outputs_research_only_non_actionable")),
        "label_family_candidate_matrix_verified": (True, package.get("label_family_candidate_matrix_review", {}).get("verified")),
        "threshold_design_matrix_verified": (True, package.get("threshold_design_matrix_review", {}).get("verified")),
        "horizon_design_matrix_verified": (True, package.get("horizon_design_matrix_review", {}).get("verified")),
        "per_ticker_plan_verified": (True, package.get("per_ticker_label_objective_plan_review", {}).get("verified")),
        "label_availability_boundary_plan_verified": (True, package.get("label_availability_boundary_plan_review", {}).get("verified")),
        "meta_limitation_preservation_plan_verified": (True, package.get("meta_limitation_preservation_plan_review", {}).get("verified")),
        "candidate_label_family_count_10": (10, package.get("candidate_label_family_count")),
        "threshold_design_strategy_count_7": (7, package.get("threshold_design_strategy_count")),
        "horizon_design_candidate_count_5": (5, package.get("horizon_design_candidate_count")),
        "per_ticker_plan_count_12": (12, package.get("per_ticker_plan_count")),
        "results_review_created_true": (True, package.get("label_objective_redesign_results_review_created")),
        "results_review_ready_true": (True, package.get("label_objective_redesign_results_review_ready")),
        "ready_for_redesigned_label_generation_candidate_true": (True, package.get("ready_for_redesigned_label_generation_candidate")),
        "redesigned_label_generation_candidate_created_false": (False, package.get("redesigned_label_generation_candidate_created")),
        "actual_labels_generated_false": (False, package.get("label_generation_performed")),
        "redesigned_label_generation_authorized_false": (False, package.get("redesigned_label_generation_authorized")),
        "redesigned_label_generation_performed_false": (False, package.get("redesigned_label_generation_performed")),
        "features_generated_false": (False, package.get("feature_generation_performed")),
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
        "label_objective_redesign_execution_rerun_false": (False, package.get("label_objective_redesign_execution_rerun_performed")),
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
        "ready_for_redesigned_label_generation_candidate": not failed,
        "redesigned_label_generation_candidate_created": False,
        "actual_labels_generated": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("label_objective_redesign_results_review_package_digest", None)
    if "output_root" in payload:
        payload["output_root"] = DEFAULT_OUTPUT_ROOT.as_posix()
    return payload


def label_objective_redesign_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return a deterministic, output-location-independent semantic digest."""
    return semantic_digest(_digest_payload(review_package))


def build_label_objective_redesign_results_review_package_v1(
    *, output_root: str | Path | None = None
) -> dict[str, Any]:
    """Inspect existing ignored planning outputs without rerunning execution."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    try:
        execution.validate_label_objective_redesign_executed_v1(
            payloads["label_objective_redesign_execution_manifest.json"]
        )
    except execution.LabelObjectiveRedesignExecutionError as exc:
        return _blocked_package(root, [{"failure_id": "invalid_source_execution_artifact", "message": str(exc)}])
    package = _base_package(root, payloads, bindings)
    package["review_checklist"] = _review_checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    if package["review_summary"]["blocker_count"]:
        return _blocked_package(root, [
            {"failure_id": "review_check_failed", "check_id": row["check_id"]}
            for row in package["review_checklist"]
            if row["status"] != PASS
        ])
    package["label_objective_redesign_results_review_package_digest"] = (
        label_objective_redesign_results_review_package_digest_v1(package)
    )
    validate_label_objective_redesign_results_review_package_v1(package)
    return package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "REDESIGNED_LABEL_GENERATION_CANDIDATE",
        "LABEL_GENERATION_EXECUTED",
        "REDESIGNED_LABEL_GENERATION_EXECUTED",
        "FEATURE_GENERATION_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
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
                raise LabelObjectiveRedesignResultsReviewError(f"{current} must not emit {item}")
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise LabelObjectiveRedesignResultsReviewError(f"{current} must not be AUTHORIZED")
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveRedesignResultsReviewError(f"{current} must not be accepted")
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignResultsReviewError(f"{field} mismatch")


def validate_label_objective_redesign_results_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Validate a ready or blocked package without touching source outputs."""
    if not isinstance(review_package, dict):
        raise LabelObjectiveRedesignResultsReviewError("review package must be a JSON object")
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_V1, "schema_version")
    if review_package.get("review_status") == LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        _expect(review_package.get("label_objective_redesign_results_review_ready"), False, "blocked review ready")
        _expect(review_package.get("ready_for_redesigned_label_generation_candidate"), False, "blocked candidate readiness")
        _expect(review_package.get("redesigned_label_generation_candidate_created"), False, "blocked candidate created")
        _expect(review_package.get("label_objective_redesign_results_review_package_digest"), "NOT_CREATED", "blocked review digest")
        return {"status": "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_BLOCKED_VALID", "review_status": review_package["review_status"], "blocker_count": review_package.get("blocker_count", 0)}

    _expect(review_package.get("review_status"), LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY, "review_status")
    _reject_forbidden_values(review_package)
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED,
        "source_execution_status": execution.LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY,
        "source_label_objective_redesign_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_label_objective_redesign_execution_approval_digest": execution.EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "source_label_objective_redesign_execution_candidate_review_package_digest": execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_research_registry_approval_digest": execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "generated_output_count": 8,
        "generated_output_names": EXPECTED_OUTPUT_FILENAMES,
        "output_digests": EXPECTED_OUTPUT_DIGESTS,
        "candidate_label_family_count": 10,
        "threshold_design_strategy_count": 7,
        "horizon_design_candidate_count": 5,
        "per_ticker_plan_count": 12,
        "limitations": LIMITATIONS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
    true_fields = [
        "created_offline", "research_only", "operator_review_required",
        "label_objective_redesign_execution_approved", "label_objective_redesign_authorized",
        "label_objective_redesign_executed", "label_objective_redesign_results_created",
        "label_objective_redesign_results_review_created", "label_objective_redesign_results_review_ready",
        "ready_for_redesigned_label_generation_candidate", "output_file_inspection_performed",
        "outputs_research_only_non_actionable", "label_objective_redesign_planning_outputs_available",
        "label_objective_redesign_outputs_verified", "results_support_future_redesigned_label_generation_candidate",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ]
    false_fields = [
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "label_objective_redesign_execution_rerun_performed",
        "predictive_evidence_rerun_performed", "refined_evidence_rerun_performed",
        "label_generation_performed", "redesigned_label_generation_candidate_created",
        "redesigned_label_generation_authorized", "redesigned_label_generation_performed",
        "feature_generation_performed", "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed", "metric_recomputation_performed",
        "model_training_performed", "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed", "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "results_create_redesigned_label_generation_candidate", "results_create_actual_labels",
        "results_create_features", "results_create_predictive_evidence",
        "results_create_predictive_usefulness_acceptance", "results_create_profitability_acceptance",
        "results_create_runtime_authority", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
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
    _expect(review_package.get("non_self_output_digest_match_count"), 7, "non_self_output_digest_match_count")
    _expect(review_package.get("digest_manifest_self_reference_policy"), "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "digest_manifest_self_reference_policy")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveRedesignResultsReviewError("review_checklist mismatch")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review_checklist check ids")
    if any(row.get("status") != PASS for row in checklist):
        raise LabelObjectiveRedesignResultsReviewError("review_checklist must pass")
    expected_summary = _summary(checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("label_objective_redesign_results_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignResultsReviewError("missing review digest")
    _expect(digest, label_objective_redesign_results_review_package_digest_v1(review_package), "review digest")
    return {
        "status": LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "label_objective_redesign_results_review_package_digest": digest,
        "source_label_objective_redesign_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "generated_output_count": 8,
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_redesigned_label_generation_candidate": True,
        "redesigned_label_generation_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_label_objective_redesign_results_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized review without reproducing source output bodies."""
    validation = validate_label_objective_redesign_results_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Label Objective Redesign Results Review Status", "",
        "## Title", "- Label Objective Redesign Results Review v1.", "",
        "## Label Objective Redesign Results Review", f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['label_objective_redesign_results_review_package_digest']}`.", "",
        "## Source Execution", f"- Artifact/status/digest: `{review_package['source_execution_artifact_kind']}` / `{review_package['source_execution_status']}` / `{review_package['source_label_objective_redesign_execution_digest']}`.", "",
        "## Dataset and Universe", f"- `{review_package['dataset_name']}` contains `{review_package['total_canonical_record_count']}` frozen records for `{', '.join(review_package['target_universe'])}`; META remains `{review_package['meta_record_count']}`.", "",
        "## Generated Planning Outputs", f"- All `{review_package['generated_output_count']}` outputs were inspected offline and digest-bound; seven non-self hashes match and the manifest self-reference is explicitly non-applicable.", "",
        "## Label Family Candidate Matrix Review", "- Ten design-only candidate families are present; no label values were generated or authorized.", "",
        "## Threshold Design Matrix Review", "- Seven threshold strategies are present; no final threshold was computed.", "",
        "## Horizon Design Matrix Review", "- Five horizon candidates are present; no final horizon was selected.", "",
        "## Per-Ticker Label Objective Plan Review", "- Twelve ordered ticker plans are present; every plan remains not executed.", "",
        "## Label Availability Boundary Plan Review", "- Forward-horizon, training-window, no-peek, and unavailable-outcome boundaries remain design-only.", "",
        "## META Limitation Preservation Review", "- META remains limited to 913 records with no backfill, repair, or synthetic rows.", "",
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
        "", "## Predictive Usefulness Boundary", f"- Predictive usefulness remains `{review_package['predictive_usefulness']}`; this is not acceptance evidence.",
        "", "## Profitability Boundary", f"- Profitability remains `{review_package['profitability']}`.",
        "", "## Runtime Boundary", f"- Runtime/strategy/paper/broker remain `{review_package['runtime_use']}` / `{review_package['strategy_use']}` / `{review_package['paper_trading']}` / `{review_package['broker_execution']}`.",
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- The review inspected and hashed existing ignored planning outputs only. It made no provider request and performed no dataset, label, feature, metric, model, strategy, recommendation, acceptance, or runtime action.", "- Readiness supports only the next separately governed candidate step; it does not create or authorize that candidate or any label generation.", "",
    ])
    return "\n".join(lines)


def write_label_objective_redesign_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting existing evidence."""
    package = build_label_objective_redesign_results_review_package_v1(output_root=output_root)
    validate_label_objective_redesign_results_review_package_v1(package)
    output_name = filename or "label_objective_redesign_results_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LabelObjectiveRedesignResultsReviewError("results review filename must be a simple JSON filename")
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise LabelObjectiveRedesignResultsReviewError("results review output already exists") from exc
    return {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": package["review_status"],
        "label_objective_redesign_results_review_package_digest": package["label_objective_redesign_results_review_package_digest"],
    }
