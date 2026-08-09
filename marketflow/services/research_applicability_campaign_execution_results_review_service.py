"""Offline results review for the research applicability campaign execution."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import research_applicability_campaign_execution_service as execution


ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_V1 = (
    "research_applicability_campaign_execution_results_review_v1"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c"
)
EXPECTED_SOURCE_EXECUTION_REQUEST_ID = execution.candidate.CAMPAIGN_EXECUTION_REQUEST_ID
EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST = execution.EXPECTED_APPROVAL_DIGEST
EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST = execution.approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    execution.approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CAMPAIGN_PLAN_DIGEST = execution.candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
EXPECTED_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST = (
    execution.candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST = (
    execution.candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = (
    execution.candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    execution.candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
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
    "campaign_plan_digest_bound",
    "campaign_plan_review_digest_bound",
    "dataset_availability_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "output_root_present",
    "expected_output_count_12",
    "actual_output_count_12",
    "all_outputs_labeled_research_only",
    "dataset_load_summary_matches",
    "schema_validation_pass",
    "bar_count_consistency_pass",
    "date_range_coverage_pass",
    "ohlc_consistency_pass",
    "volume_consistency_pass",
    "indicator_calculation_pass_research_only",
    "module_compatibility_listed",
    "failure_count_zero",
    "warning_count_zero",
    "no_trade_recommendations",
    "no_runtime_authorization_in_outputs",
    "no_predictive_acceptance_in_outputs",
    "no_profitability_acceptance_in_outputs",
    "provider_requests_made_in_review_false",
    "campaign_reexecution_performed_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
]

REMAINING_REQUIRED_TASKS = [
    "Predictive usefulness review candidate.",
    "Profitability review candidate.",
    "Runtime migration approval ceremony, if ever authorized.",
]


class ResearchApplicabilityCampaignExecutionResultsReviewError(ValueError):
    """Raised when the campaign execution results review violates guardrails."""


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
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(f"{field_name} must be false")


def _resolve_output_root(output_root: str | Path | None) -> Path:
    return DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)


def _load_json_file(path: Path) -> tuple[dict[str, Any] | None, str | None, int | None]:
    if not path.exists() or not path.is_file():
        return None, None, None
    payload = path.read_bytes()
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(
            "campaign output must be a JSON object"
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
        if any("recommendation" in str(key).lower() for key, _ in _walk_items(output)):
            return True
        if any(str(value).upper() in {"BUY", "SELL", "HOLD"} for value in _walk_values(output)):
            return True
    return False


def _has_runtime_authorization(outputs: dict[str, dict[str, Any]]) -> bool:
    for output in outputs.values():
        for key, value in _walk_items(output):
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
                return True
            if key in {
                "runtime_migration_approved",
                "runtime_migration_active",
                "strategy_runtime_migration",
                "automatic_stitching",
            } and value is True:
                return True
    return False


def _has_acceptance(outputs: dict[str, dict[str, Any]], field_name: str) -> bool:
    for output in outputs.values():
        for key, value in _walk_items(output):
            if key == field_name and value == "accepted":
                return True
            if value == field_name.upper() + "_ACCEPTED":
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
                "path": path.as_posix(),
                "exists": exists,
                "file_sha256": digest,
                "file_byte_size": byte_size,
                "output_label": data.get("output_label") if data else None,
                "report_name": data.get("report_name") if data else None,
            }
        )
    return entries, outputs


def _manifest_digest_summary(outputs: dict[str, dict[str, Any]], entries: list[dict[str, Any]]) -> dict[str, Any]:
    run_manifest = outputs.get("research_campaign_run_manifest") or {}
    declared = run_manifest.get("output_digests") if isinstance(run_manifest, dict) else None
    actual = {entry["name"]: entry["file_sha256"] for entry in entries if entry["file_sha256"]}
    verified = {}
    mismatches = {}
    if isinstance(declared, dict):
        for name, digest in declared.items():
            if name == "research_campaign_run_manifest":
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
        "run_manifest_file_digest_bound": actual.get("research_campaign_run_manifest"),
    }


def _dataset_load_summary(outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    report = outputs.get("dataset_load_report") or {}
    datasets = {
        dataset.get("dataset_profile"): dataset
        for dataset in report.get("datasets", [])
        if isinstance(dataset, dict)
    }
    return {
        "swing_row_count": datasets.get("SWING", {}).get("row_count"),
        "position_swing_row_count": datasets.get("POSITION_SWING", {}).get("row_count"),
        "datasets_digest_verified_count": report.get("datasets_digest_verified_count"),
        "summary_text": (
            "SWING 1988 rows, POSITION_SWING 994 rows, 2/2 dataset digests verified"
        ),
    }


def _result_facts(outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    dataset_summary = _dataset_load_summary(outputs)
    indicator_report = outputs.get("indicator_calculation_report") or {}
    return {
        "dataset_load_summary": dataset_summary,
        "schema_validation_status": (outputs.get("schema_validation_report") or {}).get(
            "schema_validation_status"
        ),
        "bar_count_consistency_status": (outputs.get("bar_count_consistency_report") or {}).get(
            "bar_count_consistency_status"
        ),
        "date_range_coverage_status": (outputs.get("date_range_coverage_report") or {}).get(
            "date_range_coverage_status"
        ),
        "ohlc_consistency_status": (outputs.get("ohlc_consistency_report") or {}).get(
            "ohlc_consistency_status"
        ),
        "volume_consistency_status": (outputs.get("volume_consistency_report") or {}).get(
            "volume_consistency_status"
        ),
        "indicator_calculation_status": indicator_report.get("indicator_calculation_status"),
        "indicator_acceptance_label": indicator_report.get("indicator_acceptance_label"),
        "module_compatibility_status": (outputs.get("module_compatibility_matrix") or {}).get(
            "module_compatibility_status"
        ),
        "failure_count": (outputs.get("failure_reason_inventory") or {}).get("failure_count"),
        "warning_count": (outputs.get("failure_reason_inventory") or {}).get("warning_count"),
    }


def _base_package_context(output_root: Path) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "campaign_reexecution_performed": False,
        "campaign_execution_authorized": True,
        "campaign_execution_performed": True,
        "campaign_results_generated": True,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_review_required": True,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED,
        "source_execution_status": execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_execution_request_id": EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
        "source_execution_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "source_execution_candidate_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_digest": (
            EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_plan_digest": EXPECTED_CAMPAIGN_PLAN_DIGEST,
        "campaign_plan_review_package_digest": EXPECTED_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST,
        "dataset_file_availability_verification_review_package_digest": (
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "output_root": output_root.as_posix(),
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
    }


def _summary(checklist: list[dict[str, Any]], *, review_status: str) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    ready = review_status == RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY and failed == 0
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": ready,
        "ready_for_predictive_usefulness_review": ready,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    actual_output_count = package.get("actual_output_count")
    output_files_missing = package.get("missing_output_count")
    return [
        _check("execution_artifact_kind_matches", execution.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED, package.get("source_execution_artifact_kind")),
        _check("execution_status_research_only", execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY, package.get("source_execution_status")),
        _check("execution_digest_matches", EXPECTED_SOURCE_EXECUTION_DIGEST, package.get("source_execution_digest")),
        _check("execution_request_id_matches", EXPECTED_SOURCE_EXECUTION_REQUEST_ID, package.get("source_execution_request_id")),
        _check("execution_approval_digest_bound", EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST, package.get("source_execution_approval_digest")),
        _check("execution_candidate_digest_bound", EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST, package.get("source_execution_candidate_digest")),
        _check("execution_candidate_review_digest_bound", EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("source_execution_candidate_review_package_digest")),
        _check("campaign_plan_digest_bound", EXPECTED_CAMPAIGN_PLAN_DIGEST, package.get("campaign_plan_digest")),
        _check("campaign_plan_review_digest_bound", EXPECTED_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST, package.get("campaign_plan_review_package_digest")),
        _check("dataset_availability_review_digest_bound", EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST, package.get("dataset_file_availability_verification_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, package.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, package.get("position_swing_registry_approval_digest")),
        _check("output_root_present", True, package.get("output_root_present")),
        _check("expected_output_count_12", EXPECTED_OUTPUT_COUNT, package.get("expected_output_count")),
        _check("actual_output_count_12", EXPECTED_OUTPUT_COUNT, actual_output_count),
        _check("all_outputs_labeled_research_only", True, package.get("all_outputs_research_only_non_actionable")),
        _check("dataset_load_summary_matches", True, package.get("dataset_load_summary_matches")),
        _check("schema_validation_pass", "PASS", package.get("schema_validation_status")),
        _check("bar_count_consistency_pass", "PASS", package.get("bar_count_consistency_status")),
        _check("date_range_coverage_pass", "PASS", package.get("date_range_coverage_status")),
        _check("ohlc_consistency_pass", "PASS", package.get("ohlc_consistency_status")),
        _check("volume_consistency_pass", "PASS", package.get("volume_consistency_status")),
        _check("indicator_calculation_pass_research_only", {"status": "PASS", "label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE}, {"status": package.get("indicator_calculation_status"), "label": package.get("indicator_acceptance_label")}),
        _check("module_compatibility_listed", "RESEARCH_ONLY_COMPATIBILITY_LISTED", package.get("module_compatibility_status")),
        _check("failure_count_zero", 0, package.get("failure_count")),
        _check("warning_count_zero", 0, package.get("warning_count")),
        _check("no_trade_recommendations", False, package.get("trade_recommendations_present")),
        _check("no_runtime_authorization_in_outputs", False, package.get("runtime_authorization_present_in_outputs")),
        _check("no_predictive_acceptance_in_outputs", False, package.get("predictive_acceptance_present_in_outputs")),
        _check("no_profitability_acceptance_in_outputs", False, package.get("profitability_acceptance_present_in_outputs")),
        _check("provider_requests_made_in_review_false", False, package.get("provider_requests_made_in_review")),
        _check("campaign_reexecution_performed_false", False, package.get("campaign_reexecution_performed")),
        _check("runtime_migration_approved_false", False, package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        _check("automatic_stitching_false", False, package.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, package.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, package.get("profitability"), severity=INFO),
    ]


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("research_applicability_campaign_execution_results_review_package_digest", None)
    return payload


def research_applicability_campaign_execution_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the results review package."""
    return semantic_digest(_digest_payload(review_package))


def build_research_applicability_campaign_execution_results_review_package_v1(
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for already-generated campaign outputs."""
    root = _resolve_output_root(output_root)
    entries, outputs = _output_file_entries(root)
    missing_count = sum(1 for entry in entries if entry["exists"] is not True)
    actual_output_count = sum(1 for entry in entries if entry["exists"] is True)
    output_root_present = root.exists() and root.is_dir()
    all_labeled = (
        actual_output_count == EXPECTED_OUTPUT_COUNT
        and all(entry["output_label"] == RESEARCH_ONLY_NON_ACTIONABLE for entry in entries)
    )
    digest_summary = _manifest_digest_summary(outputs, entries)
    facts = _result_facts(outputs) if missing_count == 0 else {
        "dataset_load_summary": {
            "swing_row_count": None,
            "position_swing_row_count": None,
            "datasets_digest_verified_count": None,
            "summary_text": "output inspection blocked",
        },
        "schema_validation_status": None,
        "bar_count_consistency_status": None,
        "date_range_coverage_status": None,
        "ohlc_consistency_status": None,
        "volume_consistency_status": None,
        "indicator_calculation_status": None,
        "indicator_acceptance_label": None,
        "module_compatibility_status": None,
        "failure_count": None,
        "warning_count": None,
    }
    dataset_summary = facts["dataset_load_summary"]
    dataset_load_matches = {
        "swing_row_count": dataset_summary.get("swing_row_count"),
        "position_swing_row_count": dataset_summary.get("position_swing_row_count"),
        "datasets_digest_verified_count": dataset_summary.get("datasets_digest_verified_count"),
    } == {
        "swing_row_count": 1988,
        "position_swing_row_count": 994,
        "datasets_digest_verified_count": 2,
    }
    package = {
        **_base_package_context(root),
        "review_status": (
            RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY
            if missing_count == 0
            else RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS
        ),
        "output_file_inspection_performed": missing_count == 0,
        "output_root_present": output_root_present,
        "actual_output_count": actual_output_count,
        "missing_output_count": missing_count,
        "expected_outputs": list(EXPECTED_OUTPUT_NAMES),
        "output_files": entries,
        "all_outputs_research_only_non_actionable": all_labeled,
        "output_digest_manifest": digest_summary["actual_output_digests"],
        "manifest_declared_output_digests": digest_summary["manifest_declared_output_digests"],
        "manifest_digest_verified_count": digest_summary["manifest_digest_verified_count"],
        "manifest_digest_mismatch_count": digest_summary["manifest_digest_mismatch_count"],
        "manifest_digest_mismatches": digest_summary["manifest_digest_mismatches"],
        "run_manifest_file_digest_bound": digest_summary["run_manifest_file_digest_bound"],
        "dataset_load_summary": dataset_summary,
        "dataset_load_summary_matches": dataset_load_matches,
        "schema_validation_status": facts["schema_validation_status"],
        "bar_count_consistency_status": facts["bar_count_consistency_status"],
        "date_range_coverage_status": facts["date_range_coverage_status"],
        "ohlc_consistency_status": facts["ohlc_consistency_status"],
        "volume_consistency_status": facts["volume_consistency_status"],
        "indicator_calculation_status": facts["indicator_calculation_status"],
        "indicator_acceptance_label": facts["indicator_acceptance_label"],
        "module_compatibility_status": facts["module_compatibility_status"],
        "failure_count": facts["failure_count"],
        "warning_count": facts["warning_count"],
        "trade_recommendations_present": _has_trade_recommendation(outputs),
        "runtime_authorization_present_in_outputs": _has_runtime_authorization(outputs),
        "predictive_acceptance_present_in_outputs": _has_acceptance(outputs, "predictive_usefulness"),
        "profitability_acceptance_present_in_outputs": _has_acceptance(outputs, "profitability"),
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist, review_status=package["review_status"])
    package["research_applicability_campaign_execution_results_review_package_digest"] = (
        research_applicability_campaign_execution_results_review_package_digest_v1(package)
    )
    validate_research_applicability_campaign_execution_results_review_package_v1(package)
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
        }:
            raise ResearchApplicabilityCampaignExecutionResultsReviewError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made_in_review",
            "campaign_reexecution_performed",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise ResearchApplicabilityCampaignExecutionResultsReviewError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ResearchApplicabilityCampaignExecutionResultsReviewError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ResearchApplicabilityCampaignExecutionResultsReviewError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_research_applicability_campaign_execution_results_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate an execution results review package without accepting performance or runtime use."""
    if not isinstance(review_package, dict):
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_V1,
        "schema_version",
    )
    status = review_package.get("review_status")
    if status not in {
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY,
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS,
    }:
        raise ResearchApplicabilityCampaignExecutionResultsReviewError("review_status mismatch")
    for field in (
        "created_offline",
        "campaign_execution_authorized",
        "campaign_execution_performed",
        "campaign_results_generated",
        "operator_review_required",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "campaign_reexecution_performed",
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
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED,
        "source_execution_status": execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_execution_request_id": EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
        "source_execution_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "source_execution_candidate_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        "source_execution_candidate_review_package_digest": EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "campaign_plan_digest": EXPECTED_CAMPAIGN_PLAN_DIGEST,
        "campaign_plan_review_package_digest": EXPECTED_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST,
        "dataset_file_availability_verification_review_package_digest": EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
    }.items():
        _expect(review_package.get(field), expected, field)
    if status == RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY:
        _expect(review_package.get("missing_output_count"), 0, "missing_output_count")
        _expect(review_package.get("actual_output_count"), EXPECTED_OUTPUT_COUNT, "actual_output_count")
        _expect_true(
            review_package.get("all_outputs_research_only_non_actionable"),
            "all_outputs_research_only_non_actionable",
        )
        _expect_true(review_package.get("dataset_load_summary_matches"), "dataset_load_summary_matches")
        for field in (
            "schema_validation_status",
            "bar_count_consistency_status",
            "date_range_coverage_status",
            "ohlc_consistency_status",
            "volume_consistency_status",
            "indicator_calculation_status",
        ):
            _expect(review_package.get(field), "PASS", field)
        _expect(
            review_package.get("indicator_acceptance_label"),
            RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "indicator_acceptance_label",
        )
        _expect(
            review_package.get("module_compatibility_status"),
            "RESEARCH_ONLY_COMPATIBILITY_LISTED",
            "module_compatibility_status",
        )
        _expect(review_package.get("failure_count"), 0, "failure_count")
        _expect(review_package.get("warning_count"), 0, "warning_count")
        _expect_false(review_package.get("trade_recommendations_present"), "trade_recommendations_present")
        _expect_false(
            review_package.get("runtime_authorization_present_in_outputs"),
            "runtime_authorization_present_in_outputs",
        )
        _expect_false(
            review_package.get("predictive_acceptance_present_in_outputs"),
            "predictive_acceptance_present_in_outputs",
        )
        _expect_false(
            review_package.get("profitability_acceptance_present_in_outputs"),
            "profitability_acceptance_present_in_outputs",
        )
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ResearchApplicabilityCampaignExecutionResultsReviewError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    if status == RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY:
        failed = [item for item in expected_checklist if item["status"] != PASS]
        if failed:
            raise ResearchApplicabilityCampaignExecutionResultsReviewError(
                f"review checklist contains failed check: {failed[0]['check_id']}"
            )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist, review_status=status)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("research_applicability_campaign_execution_results_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(
            "research_applicability_campaign_execution_results_review_package_digest missing"
        )
    _expect(
        digest,
        research_applicability_campaign_execution_results_review_package_digest_v1(review_package),
        "research_applicability_campaign_execution_results_review_package_digest",
    )
    return {
        "status": "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "research_applicability_campaign_execution_results_review_package_digest": digest,
        "source_execution_digest": review_package["source_execution_digest"],
        "source_execution_request_id": review_package["source_execution_request_id"],
        "actual_output_count": review_package["actual_output_count"],
        "failure_count": review_package["failure_count"],
        "warning_count": review_package["warning_count"],
        "ready_for_predictive_usefulness_review": review_package["review_summary"][
            "ready_for_predictive_usefulness_review"
        ],
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_research_applicability_campaign_execution_results_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized results review package summary."""
    validation = validate_research_applicability_campaign_execution_results_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Research Applicability Campaign Execution Results Review Status",
        "",
        "## Title",
        "- Research Applicability Campaign Execution Results Operator Review Package v1.",
        "",
        "## Reviewed Research Campaign Execution",
        f"- Artifact kind: `{review_package['source_execution_artifact_kind']}`",
        f"- Execution status: `{review_package['source_execution_status']}`",
        f"- Execution digest: `{review_package['source_execution_digest']}`",
        f"- Execution request ID: `{review_package['source_execution_request_id']}`",
        f"- Results review package digest: `{validation['research_applicability_campaign_execution_results_review_package_digest']}`",
        "",
        "## Output Summary",
        f"- Output root: `{review_package['output_root']}`",
        f"- Expected output count: `{review_package['expected_output_count']}`",
        f"- Actual output count: `{review_package['actual_output_count']}`",
        f"- All outputs research-only non-actionable: `{review_package['all_outputs_research_only_non_actionable']}`",
        "",
        "## Data Quality Summary",
        f"- Dataset load summary: `{review_package['dataset_load_summary']['summary_text']}`",
        f"- Schema validation status: `{review_package['schema_validation_status']}`",
        f"- Bar count consistency status: `{review_package['bar_count_consistency_status']}`",
        f"- Date range coverage status: `{review_package['date_range_coverage_status']}`",
        f"- OHLC consistency status: `{review_package['ohlc_consistency_status']}`",
        f"- Volume consistency status: `{review_package['volume_consistency_status']}`",
        f"- Indicator calculation status: `{review_package['indicator_calculation_status']}`",
        "",
        "## Module Compatibility Summary",
        f"- Module compatibility status: `{review_package['module_compatibility_status']}`",
        "",
        "## Failure Warning Inventory",
        f"- Failure count: `{review_package['failure_count']}`",
        f"- Warning count: `{review_package['warning_count']}`",
        "",
        "## Runtime Boundary",
        f"- provider_requests_made_in_review: `{review_package['provider_requests_made_in_review']}`",
        f"- campaign_reexecution_performed: `{review_package['campaign_reexecution_performed']}`",
        f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
        f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
        f"- strategy_runtime_migration: `{review_package['strategy_runtime_migration']}`",
        f"- runtime_use: `{review_package['runtime_use']}`",
        f"- strategy_use: `{review_package['strategy_use']}`",
        f"- paper_trading: `{review_package['paper_trading']}`",
        f"- broker_execution: `{review_package['broker_execution']}`",
        "",
        "## Predictive Profitability Boundary",
        f"- ready_for_predictive_usefulness_review: `{summary['ready_for_predictive_usefulness_review']}`",
        f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
        f"- profitability: `{review_package['profitability']}`",
        "- Predictive usefulness is not accepted by this review.",
        "- Profitability is not accepted by this review.",
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
            "- No campaign reexecution was performed.",
            "- No Strategy runtime behavior was modified.",
            "- No runtime activation occurred.",
            "- No predictive-usefulness or profitability acceptance occurred.",
            "",
        ]
    )
    return "\n".join(lines)


def write_research_applicability_campaign_execution_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the results review package JSON artifact without overwriting output."""
    package = build_research_applicability_campaign_execution_results_review_package_v1(
        output_root=output_root
    )
    validation = validate_research_applicability_campaign_execution_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename or "research_applicability_campaign_execution_results_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(
            "research applicability campaign execution results review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ResearchApplicabilityCampaignExecutionResultsReviewError(
            "research applicability campaign execution results review output already exists"
        )
    payload = canonical_json_bytes(package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
