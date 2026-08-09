"""Offline results review for predictive experiment execution outputs."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import predictive_experiment_execution_service as execution


ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_V1 = (
    "predictive_experiment_execution_results_review_v1"
)
PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY"
)
PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "f165b6a066e81e8d5f6c4de2a5603e0dc74aa29ea90dc19cc887b3474bfd32b0"
)
EXPECTED_SOURCE_EXECUTION_REQUEST_ID = execution.candidate.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST = execution.EXPECTED_APPROVAL_DIGEST
EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST = execution.approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    execution.approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    execution.candidate.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    execution.candidate.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST = (
    execution.EXPECTED_SOURCE_DIGESTS["predictive_usefulness_review_candidate_digest"]
)
EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    execution.EXPECTED_SOURCE_DIGESTS[
        "predictive_usefulness_review_candidate_review_package_digest"
    ]
)
EXPECTED_CAMPAIGN_RESULTS_REVIEW_PACKAGE_DIGEST = (
    execution.EXPECTED_SOURCE_DIGESTS["campaign_results_review_package_digest"]
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = (
    execution.EXPECTED_SOURCE_DIGESTS["swing_registry_approval_digest"]
)
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    execution.EXPECTED_SOURCE_DIGESTS["position_swing_registry_approval_digest"]
)

EXPECTED_OUTPUT_COUNT = len(execution.OUTPUT_NAMES)
EXPECTED_OUTPUT_NAMES = list(execution.OUTPUT_NAMES)
DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = execution.RESEARCH_ONLY_NON_ACTIONABLE
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = execution.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "execution_artifact_kind_matches",
    "execution_status_research_only",
    "execution_digest_matches",
    "execution_request_id_matches",
    "execution_approval_digest_bound",
    "execution_candidate_digest_bound",
    "execution_candidate_review_digest_bound",
    "predictive_experiment_plan_digest_bound",
    "predictive_experiment_plan_review_digest_bound",
    "campaign_results_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "output_root_present",
    "expected_output_count_13",
    "actual_output_count_13",
    "all_outputs_labeled_research_only",
    "metrics_labeled_research_only_not_performance_acceptance",
    "labels_generated_true",
    "feature_matrices_generated_true",
    "walk_forward_result_generated_true",
    "out_of_sample_result_generated_true",
    "no_trade_recommendations",
    "no_runtime_authorization_in_outputs",
    "no_strategy_authorization_in_outputs",
    "no_broker_authorization_in_outputs",
    "no_predictive_acceptance_in_outputs",
    "no_profitability_acceptance_in_outputs",
    "provider_requests_made_in_review_false",
    "experiment_reexecution_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "runtime_migration_recommended_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
]

REMAINING_REQUIRED_TASKS = [
    "Predictive usefulness assessment candidate.",
    "Profitability review after predictive usefulness assessment.",
    "Separate runtime migration approval ceremony, if ever authorized.",
]


class PredictiveExperimentExecutionResultsReviewError(ValueError):
    """Raised when predictive execution results review violates guardrails."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
    message: str | None = None,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": message or (f"{check_id} passed" if status == PASS else f"{check_id} failed"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PredictiveExperimentExecutionResultsReviewError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveExperimentExecutionResultsReviewError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveExperimentExecutionResultsReviewError(f"{field_name} must be false")


def _resolve_output_root(output_root: str | Path | None) -> Path:
    return DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json_file(path: Path) -> tuple[dict[str, Any] | None, str | None, int | None]:
    if not path.exists() or not path.is_file():
        return None, None, None
    payload = path.read_bytes()
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise PredictiveExperimentExecutionResultsReviewError(
            "predictive experiment output must be a JSON object"
        )
    return data, sha256_bytes(payload), len(payload)


def _walk_values(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_values(item)
    else:
        yield value


def _walk_items(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key), item
            yield from _walk_items(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_items(item)


def _has_trade_recommendation(outputs: dict[str, dict[str, Any]]) -> bool:
    for output in outputs.values():
        for key, value in _walk_items(output):
            if "recommendation" in key.lower():
                return True
            if str(value).upper() in {"BUY", "SELL", "HOLD"}:
                return True
    return False


def _has_authorized_field(outputs: dict[str, dict[str, Any]], field_name: str) -> bool:
    for output in outputs.values():
        for key, value in _walk_items(output):
            if key == field_name and value == "AUTHORIZED":
                return True
    return False


def _has_runtime_authorization(outputs: dict[str, dict[str, Any]]) -> bool:
    runtime_fields = {
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    }
    for output in outputs.values():
        for key, value in _walk_items(output):
            if key in runtime_fields and value is True:
                return True
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
                if value == "AUTHORIZED":
                    return True
    return False


def _has_acceptance(outputs: dict[str, dict[str, Any]], field_name: str) -> bool:
    for output in outputs.values():
        for key, value in _walk_items(output):
            if key == field_name and value == "accepted":
                return True
            if isinstance(value, str) and value == f"{field_name.upper()}_ACCEPTED":
                return True
    return False


def _output_file_entries(output_root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    outputs: dict[str, dict[str, Any]] = {}
    for name in EXPECTED_OUTPUT_NAMES:
        path = output_root / f"{name}.json"
        data, digest, byte_size = _load_json_file(path)
        exists = data is not None
        if data is not None:
            outputs[name] = data
        entries.append(
            {
                "name": name,
                "path": _path_text(path),
                "exists": exists,
                "file_sha256": digest,
                "file_byte_size": byte_size,
                "output_label": data.get("output_label") if data else None,
                "metrics_label": data.get("metrics_label") if data else None,
                "report_name": data.get("report_name") if data else None,
            }
        )
    return entries, outputs


def _manifest_digest_summary(
    outputs: dict[str, dict[str, Any]],
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    run_manifest = outputs.get("predictive_experiment_run_manifest") or {}
    declared = run_manifest.get("output_digests") if isinstance(run_manifest, dict) else None
    actual = {entry["name"]: entry["file_sha256"] for entry in entries if entry["file_sha256"]}
    verified: dict[str, bool] = {}
    mismatches: dict[str, dict[str, str | None]] = {}
    if isinstance(declared, dict):
        for name, digest in declared.items():
            if name == "predictive_experiment_run_manifest":
                continue
            verified[name] = actual.get(name) == digest
            if actual.get(name) != digest:
                mismatches[name] = {"declared": digest, "actual": actual.get(name)}
    return {
        "manifest_available": isinstance(declared, dict),
        "manifest_declared_output_digests": declared if isinstance(declared, dict) else {},
        "actual_output_digests": actual,
        "manifest_digest_verified_count": sum(1 for value in verified.values() if value is True),
        "manifest_digest_mismatch_count": len(mismatches),
        "manifest_digest_mismatches": mismatches,
        "run_manifest_file_digest_bound": actual.get("predictive_experiment_run_manifest"),
    }


def _baseline_result_count(outputs: dict[str, dict[str, Any]]) -> int | str:
    results = (outputs.get("baseline_comparison_report") or {}).get("results")
    if not isinstance(results, dict):
        return "unavailable"
    return sum(len(value) for value in results.values() if isinstance(value, dict))


def _metric_result_count(outputs: dict[str, dict[str, Any]]) -> int | str:
    results = (outputs.get("signal_quality_metrics_report") or {}).get("results")
    if not isinstance(results, dict):
        return "unavailable"
    return sum(len(value) for value in results.values() if isinstance(value, dict))


def _labels_generated(outputs: dict[str, dict[str, Any]]) -> bool:
    report = outputs.get("label_generation_report") or {}
    return report.get("label_generation_performed") is True


def _feature_matrices_generated(outputs: dict[str, dict[str, Any]]) -> bool:
    report = outputs.get("feature_matrix_manifest") or {}
    return report.get("feature_matrix_generation_performed") is True


def _walk_forward_generated(outputs: dict[str, dict[str, Any]]) -> bool:
    report = outputs.get("walk_forward_configuration_report") or {}
    return report.get("walk_forward_validation_performed") is True


def _oos_generated(outputs: dict[str, dict[str, Any]]) -> bool:
    report = outputs.get("out_of_sample_split_report") or {}
    return report.get("out_of_sample_evaluation_performed") is True


def _all_metrics_labeled(outputs: dict[str, dict[str, Any]]) -> bool:
    metric_outputs = [
        outputs.get("walk_forward_configuration_report"),
        outputs.get("baseline_comparison_report"),
        outputs.get("signal_quality_metrics_report"),
        outputs.get("stability_analysis_report"),
        outputs.get("false_positive_false_negative_report"),
        outputs.get("operator_review_summary"),
        outputs.get("predictive_experiment_run_manifest"),
    ]
    return all(
        isinstance(output, dict)
        and output.get("metrics_label") == RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
        for output in metric_outputs
    )


def _dataset_summary(outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    label_report = outputs.get("label_generation_report") or {}
    datasets = label_report.get("datasets") if isinstance(label_report, dict) else None
    by_profile = {
        item.get("dataset_profile"): item
        for item in datasets or []
        if isinstance(item, dict) and item.get("dataset_profile")
    }
    return {
        "dataset_count": len(by_profile) if by_profile else "unavailable",
        "swing_row_count": by_profile.get("SWING", {}).get("row_count"),
        "position_swing_row_count": by_profile.get("POSITION_SWING", {}).get("row_count"),
        "label_available_count": sum(
            item.get("available_label_count", 0)
            for item in by_profile.values()
            if isinstance(item.get("available_label_count"), int)
        )
        if by_profile
        else "unavailable",
    }


def _result_facts(outputs: dict[str, dict[str, Any]], *, missing_count: int) -> dict[str, Any]:
    if missing_count:
        return {
            "dataset_count": "unavailable",
            "labels_generated": False,
            "feature_matrices_generated": False,
            "walk_forward_result_generated": False,
            "out_of_sample_result_generated": False,
            "baseline_result_count": "unavailable",
            "metric_result_count": "unavailable",
            "walk_forward_summary_status": "unavailable",
            "out_of_sample_summary_status": "unavailable",
            "failure_count": "unavailable",
            "warning_count": "unavailable",
            "dataset_summary": {
                "dataset_count": "unavailable",
                "swing_row_count": None,
                "position_swing_row_count": None,
                "label_available_count": "unavailable",
            },
            "leakage_control_status": "unavailable",
        }
    return {
        "dataset_count": _dataset_summary(outputs)["dataset_count"],
        "labels_generated": _labels_generated(outputs),
        "feature_matrices_generated": _feature_matrices_generated(outputs),
        "walk_forward_result_generated": _walk_forward_generated(outputs),
        "out_of_sample_result_generated": _oos_generated(outputs),
        "baseline_result_count": _baseline_result_count(outputs),
        "metric_result_count": _metric_result_count(outputs),
        "walk_forward_summary_status": (
            "SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT"
            if _walk_forward_generated(outputs)
            else "unavailable"
        ),
        "out_of_sample_summary_status": "CHRONOLOGICAL_OOS_RESEARCH_SPLIT"
        if _oos_generated(outputs)
        else "unavailable",
        "failure_count": "unavailable",
        "warning_count": "unavailable",
        "dataset_summary": _dataset_summary(outputs),
        "leakage_control_status": (outputs.get("leakage_control_report") or {}).get(
            "leakage_control_status",
            "unavailable",
        ),
    }


def _base_package_context(output_root: Path) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "experiment_reexecution_performed": False,
        "predictive_experiment_execution_authorized": True,
        "predictive_experiment_executed": True,
        "walk_forward_validation_performed": True,
        "out_of_sample_evaluation_performed": True,
        "label_generation_performed": True,
        "feature_matrix_generation_performed": True,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "operator_review_required": True,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED,
        "source_execution_status": execution.PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_execution_request_id": EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
        "source_execution_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "source_execution_candidate_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_digest": (
            EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_plan_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
        "predictive_experiment_plan_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_review_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_review_candidate_review_package_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_results_review_package_digest": EXPECTED_CAMPAIGN_RESULTS_REVIEW_PACKAGE_DIGEST,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "output_root": _path_text(output_root),
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
    }


def _summary(checklist: list[dict[str, Any]], *, review_status: str) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    ready = (
        review_status == PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY
        and failed == 0
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": ready,
        "ready_for_predictive_usefulness_assessment": ready,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("execution_artifact_kind_matches", execution.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED, package.get("source_execution_artifact_kind")),
        _check("execution_status_research_only", execution.PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY, package.get("source_execution_status")),
        _check("execution_digest_matches", EXPECTED_SOURCE_EXECUTION_DIGEST, package.get("source_execution_digest")),
        _check("execution_request_id_matches", EXPECTED_SOURCE_EXECUTION_REQUEST_ID, package.get("source_execution_request_id")),
        _check("execution_approval_digest_bound", EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST, package.get("source_execution_approval_digest")),
        _check("execution_candidate_digest_bound", EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST, package.get("source_execution_candidate_digest")),
        _check("execution_candidate_review_digest_bound", EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("source_execution_candidate_review_package_digest")),
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, package.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, package.get("predictive_experiment_plan_review_package_digest")),
        _check("campaign_results_review_digest_bound", EXPECTED_CAMPAIGN_RESULTS_REVIEW_PACKAGE_DIGEST, package.get("campaign_results_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, package.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, package.get("position_swing_registry_approval_digest")),
        _check("output_root_present", True, package.get("output_root_present")),
        _check("expected_output_count_13", EXPECTED_OUTPUT_COUNT, package.get("expected_output_count")),
        _check("actual_output_count_13", EXPECTED_OUTPUT_COUNT, package.get("actual_output_count")),
        _check("all_outputs_labeled_research_only", True, package.get("all_outputs_research_only_non_actionable")),
        _check("metrics_labeled_research_only_not_performance_acceptance", True, package.get("metrics_labeled_research_only_not_performance_acceptance")),
        _check("labels_generated_true", True, package.get("labels_generated")),
        _check("feature_matrices_generated_true", True, package.get("feature_matrices_generated")),
        _check("walk_forward_result_generated_true", True, package.get("walk_forward_result_generated")),
        _check("out_of_sample_result_generated_true", True, package.get("out_of_sample_result_generated")),
        _check("no_trade_recommendations", False, package.get("trade_recommendations_present")),
        _check("no_runtime_authorization_in_outputs", False, package.get("runtime_authorization_present_in_outputs")),
        _check("no_strategy_authorization_in_outputs", False, package.get("strategy_authorization_present_in_outputs")),
        _check("no_broker_authorization_in_outputs", False, package.get("broker_authorization_present_in_outputs")),
        _check("no_predictive_acceptance_in_outputs", False, package.get("predictive_acceptance_present_in_outputs")),
        _check("no_profitability_acceptance_in_outputs", False, package.get("profitability_acceptance_present_in_outputs")),
        _check("provider_requests_made_in_review_false", False, package.get("provider_requests_made_in_review")),
        _check("experiment_reexecution_performed_false", False, package.get("experiment_reexecution_performed")),
        _check("new_strategy_scoring_performed_false", False, package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, package.get("trade_recommendations_generated")),
        _check("runtime_migration_recommended_false", False, package.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        _check("automatic_stitching_false", False, package.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, package.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, package.get("profitability_acceptance_ready")),
    ]


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_experiment_execution_results_review_package_digest", None)
    return payload


def predictive_experiment_execution_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the results review package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_experiment_execution_results_review_package_v1(
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for already-generated predictive outputs."""
    root = _resolve_output_root(output_root)
    entries, outputs = _output_file_entries(root)
    missing_count = sum(1 for entry in entries if entry["exists"] is not True)
    actual_output_count = sum(1 for entry in entries if entry["exists"] is True)
    all_labeled = (
        actual_output_count == EXPECTED_OUTPUT_COUNT
        and all(entry["output_label"] == RESEARCH_ONLY_NON_ACTIONABLE for entry in entries)
    )
    digest_summary = _manifest_digest_summary(outputs, entries)
    facts = _result_facts(outputs, missing_count=missing_count)
    package = {
        **_base_package_context(root),
        "review_status": (
            PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY
            if missing_count == 0
            else PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS
        ),
        "output_file_inspection_performed": missing_count == 0,
        "output_root_present": root.exists() and root.is_dir(),
        "actual_output_count": actual_output_count,
        "missing_output_count": missing_count,
        "expected_outputs": list(EXPECTED_OUTPUT_NAMES),
        "output_files": entries,
        "all_outputs_research_only_non_actionable": all_labeled,
        "metrics_labeled_research_only_not_performance_acceptance": (
            missing_count == 0 and _all_metrics_labeled(outputs)
        ),
        "output_digest_manifest": digest_summary["actual_output_digests"],
        "manifest_declared_output_digests": digest_summary["manifest_declared_output_digests"],
        "manifest_digest_verified_count": digest_summary["manifest_digest_verified_count"],
        "manifest_digest_mismatch_count": digest_summary["manifest_digest_mismatch_count"],
        "manifest_digest_mismatches": digest_summary["manifest_digest_mismatches"],
        "run_manifest_file_digest_bound": digest_summary["run_manifest_file_digest_bound"],
        "dataset_count": facts["dataset_count"],
        "dataset_summary": facts["dataset_summary"],
        "labels_generated": facts["labels_generated"],
        "feature_matrices_generated": facts["feature_matrices_generated"],
        "walk_forward_result_generated": facts["walk_forward_result_generated"],
        "out_of_sample_result_generated": facts["out_of_sample_result_generated"],
        "baseline_result_count": facts["baseline_result_count"],
        "metric_result_count": facts["metric_result_count"],
        "walk_forward_summary_status": facts["walk_forward_summary_status"],
        "out_of_sample_summary_status": facts["out_of_sample_summary_status"],
        "leakage_control_status": facts["leakage_control_status"],
        "failure_count": facts["failure_count"],
        "warning_count": facts["warning_count"],
        "trade_recommendations_present": _has_trade_recommendation(outputs),
        "runtime_authorization_present_in_outputs": _has_runtime_authorization(outputs),
        "strategy_authorization_present_in_outputs": _has_authorized_field(outputs, "strategy_use"),
        "broker_authorization_present_in_outputs": _has_authorized_field(outputs, "broker_execution"),
        "predictive_acceptance_present_in_outputs": _has_acceptance(outputs, "predictive_usefulness"),
        "profitability_acceptance_present_in_outputs": _has_acceptance(outputs, "profitability"),
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist, review_status=package["review_status"])
    package["predictive_experiment_execution_results_review_package_digest"] = (
        predictive_experiment_execution_results_review_package_digest_v1(package)
    )
    validate_predictive_experiment_execution_results_review_package_v1(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
            "TRADE_RECOMMENDATIONS",
        }:
            raise PredictiveExperimentExecutionResultsReviewError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made_in_review",
            "experiment_reexecution_performed",
            "new_strategy_scoring_performed",
            "trade_recommendations_generated",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "predictive_usefulness_acceptance_ready",
            "profitability_acceptance_ready",
        } and value is True:
            raise PredictiveExperimentExecutionResultsReviewError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise PredictiveExperimentExecutionResultsReviewError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveExperimentExecutionResultsReviewError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_experiment_execution_results_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a predictive execution results review without accepting runtime use."""
    if not isinstance(review_package, dict):
        raise PredictiveExperimentExecutionResultsReviewError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_V1,
        "schema_version",
    )
    status = review_package.get("review_status")
    if status not in {
        PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY,
        PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS,
    }:
        raise PredictiveExperimentExecutionResultsReviewError("review_status mismatch")
    for field in (
        "created_offline",
        "predictive_experiment_execution_authorized",
        "predictive_experiment_executed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "label_generation_performed",
        "feature_matrix_generation_performed",
        "research_only",
        "operator_review_required",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "experiment_reexecution_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "profitability_acceptance_ready",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED,
        "source_execution_status": execution.PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_execution_request_id": EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
        "source_execution_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "source_execution_candidate_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "predictive_experiment_plan_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
        "predictive_experiment_plan_review_package_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_review_candidate_digest": EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST,
        "predictive_usefulness_review_candidate_review_package_digest": EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "campaign_results_review_package_digest": EXPECTED_CAMPAIGN_RESULTS_REVIEW_PACKAGE_DIGEST,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
    }.items():
        _expect(review_package.get(field), expected, field)
    if status == PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY:
        _expect(review_package.get("missing_output_count"), 0, "missing_output_count")
        _expect(review_package.get("actual_output_count"), EXPECTED_OUTPUT_COUNT, "actual_output_count")
        _expect_true(
            review_package.get("all_outputs_research_only_non_actionable"),
            "all_outputs_research_only_non_actionable",
        )
        _expect_true(
            review_package.get("metrics_labeled_research_only_not_performance_acceptance"),
            "metrics_labeled_research_only_not_performance_acceptance",
        )
        for field in (
            "labels_generated",
            "feature_matrices_generated",
            "walk_forward_result_generated",
            "out_of_sample_result_generated",
        ):
            _expect_true(review_package.get(field), field)
        for field in (
            "trade_recommendations_present",
            "runtime_authorization_present_in_outputs",
            "strategy_authorization_present_in_outputs",
            "broker_authorization_present_in_outputs",
            "predictive_acceptance_present_in_outputs",
            "profitability_acceptance_present_in_outputs",
        ):
            _expect_false(review_package.get(field), field)
    elif review_package.get("actual_output_count") == EXPECTED_OUTPUT_COUNT:
        raise PredictiveExperimentExecutionResultsReviewError(
            "review status blocked while outputs are complete"
        )
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveExperimentExecutionResultsReviewError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    if status == PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY:
        failed = [item for item in expected_checklist if item["status"] != PASS]
        if failed:
            raise PredictiveExperimentExecutionResultsReviewError(
                f"review checklist contains failed check: {failed[0]['check_id']}"
            )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist, review_status=status)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("predictive_experiment_execution_results_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveExperimentExecutionResultsReviewError(
            "predictive_experiment_execution_results_review_package_digest missing"
        )
    _expect(
        digest,
        predictive_experiment_execution_results_review_package_digest_v1(review_package),
        "predictive_experiment_execution_results_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_experiment_execution_results_review_package_digest": digest,
        "source_execution_digest": review_package["source_execution_digest"],
        "source_execution_request_id": review_package["source_execution_request_id"],
        "actual_output_count": review_package["actual_output_count"],
        "failure_count": review_package["failure_count"],
        "warning_count": review_package["warning_count"],
        "ready_for_predictive_usefulness_assessment": review_package["review_summary"][
            "ready_for_predictive_usefulness_assessment"
        ],
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_predictive_experiment_execution_results_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized predictive experiment execution results review summary."""
    validation = validate_predictive_experiment_execution_results_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Predictive Experiment Execution Results Review Status",
        "",
        "## Title",
        "- Predictive Experiment Execution Results Operator Review Package v1.",
        "",
        "## Reviewed Predictive Experiment Execution",
        f"- Artifact kind: `{review_package['source_execution_artifact_kind']}`",
        f"- Execution status: `{review_package['source_execution_status']}`",
        f"- Execution digest: `{review_package['source_execution_digest']}`",
        f"- Approval digest: `{review_package['source_execution_approval_digest']}`",
        f"- Execution request ID: `{review_package['source_execution_request_id']}`",
        f"- Results review package digest: `{validation['predictive_experiment_execution_results_review_package_digest']}`",
        "",
        "## Output Summary",
        f"- Output root: `{review_package['output_root']}`",
        f"- Expected output count: `{review_package['expected_output_count']}`",
        f"- Actual output count: `{review_package['actual_output_count']}`",
        f"- All outputs research-only non-actionable: `{review_package['all_outputs_research_only_non_actionable']}`",
        "",
        "## Label and Feature Matrix Summary",
        f"- Dataset count: `{review_package['dataset_count']}`",
        f"- Labels generated: `{review_package['labels_generated']}`",
        f"- Feature matrices generated: `{review_package['feature_matrices_generated']}`",
        "",
        "## Walk-Forward / OOS Summary",
        f"- Walk-forward result generated: `{review_package['walk_forward_result_generated']}`",
        f"- Walk-forward summary status: `{review_package['walk_forward_summary_status']}`",
        f"- Out-of-sample result generated: `{review_package['out_of_sample_result_generated']}`",
        f"- Out-of-sample summary status: `{review_package['out_of_sample_summary_status']}`",
        "",
        "## Baseline and Metrics Summary",
        f"- Baseline result count: `{review_package['baseline_result_count']}`",
        f"- Metric result count: `{review_package['metric_result_count']}`",
        f"- Metrics label: `{RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE}`",
        "",
        "## Leakage Controls Summary",
        f"- Leakage control status: `{review_package['leakage_control_status']}`",
        "",
        "## Failure/Warning Inventory",
        f"- Failure count: `{review_package['failure_count']}`",
        f"- Warning count: `{review_package['warning_count']}`",
        "",
        "## Predictive/Profitability Boundary",
        f"- ready_for_predictive_usefulness_assessment: `{summary['ready_for_predictive_usefulness_assessment']}`",
        f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
        f"- predictive_usefulness_acceptance_ready: `{review_package['predictive_usefulness_acceptance_ready']}`",
        f"- profitability: `{review_package['profitability']}`",
        f"- profitability_acceptance_ready: `{review_package['profitability_acceptance_ready']}`",
        "",
        "## Runtime Boundary",
        f"- provider_requests_made_in_review: `{review_package['provider_requests_made_in_review']}`",
        f"- experiment_reexecution_performed: `{review_package['experiment_reexecution_performed']}`",
        f"- new_strategy_scoring_performed: `{review_package['new_strategy_scoring_performed']}`",
        f"- trade_recommendations_generated: `{review_package['trade_recommendations_generated']}`",
        f"- runtime_migration_recommended: `{review_package['runtime_migration_recommended']}`",
        f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
        f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
        f"- strategy_runtime_migration: `{review_package['strategy_runtime_migration']}`",
        f"- runtime_use: `{review_package['runtime_use']}`",
        f"- strategy_use: `{review_package['strategy_use']}`",
        f"- paper_trading: `{review_package['paper_trading']}`",
        f"- broker_execution: `{review_package['broker_execution']}`",
        "",
        "## Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        "",
        "## Remaining Required Tasks",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(review_package["remaining_required_tasks"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No predictive experiment reexecution was performed.",
            "- No Strategy runtime behavior was modified.",
            "- No runtime activation occurred.",
            "- No predictive-usefulness or profitability acceptance occurred.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_experiment_execution_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the results review package JSON artifact without overwriting output."""
    package = build_predictive_experiment_execution_results_review_package_v1(
        output_root=output_root
    )
    validation = validate_predictive_experiment_execution_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename or "predictive_experiment_execution_results_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveExperimentExecutionResultsReviewError(
            "predictive experiment execution results review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveExperimentExecutionResultsReviewError(
            "predictive experiment execution results review output already exists"
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
