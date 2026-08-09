"""Offline operator review package for the predictive usefulness review candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_review_candidate_service as candidate_service


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE = (
    "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_V1 = (
    "predictive_usefulness_review_candidate_review_v1"
)
PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_READY"
)
PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_STATUS_BINDING = (
    "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_STATUS_BINDING"
)
PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_OBJECT_BINDING = (
    "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST = (
    "e5724cc5eb106b2aa24c68e80bb24835b293fe50009a4eb01b21154553bc79b6"
)

NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REMAINING_REQUIRED_TASKS = [
    "Predictive experiment plan candidate.",
    "Walk-forward experiment plan.",
    "Predictive usefulness review after experiments.",
]

REQUIRED_CHECK_IDS = [
    "predictive_candidate_kind_matches",
    "predictive_candidate_status_ready_for_review",
    "predictive_candidate_digest_matches",
    "predictive_candidate_checklist_zero_blockers",
    "campaign_results_review_digest_bound",
    "campaign_execution_digest_bound",
    "execution_request_id_bound",
    "outputs_reviewed_12",
    "outputs_research_only_non_actionable",
    "data_quality_checks_passed",
    "module_compatibility_listed",
    "failure_count_zero",
    "warning_count_zero",
    "data_quality_readiness_true",
    "module_compatibility_readiness_true",
    "predictive_experiment_results_available_false",
    "walk_forward_results_available_false",
    "out_of_sample_results_available_false",
    "label_definition_available_false",
    "predictive_metrics_available_false",
    "additional_evidence_required_defined",
    "ready_for_predictive_experiment_planning_true",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "runtime_migration_recommended_false",
    "provider_requests_made_in_review_false",
    "campaign_reexecution_performed_false",
    "new_strategy_scoring_performed_false",
    "walk_forward_validation_performed_false",
    "trade_recommendations_generated_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
]


class PredictiveUsefulnessReviewCandidateReviewPackageError(ValueError):
    """Raised when the predictive usefulness candidate review package is invalid."""


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
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(f"{field_name} must be false")


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            candidate_service.build_predictive_usefulness_review_candidate_v1(),
            PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_STATUS_BINDING,
        )
    candidate_service.validate_predictive_usefulness_review_candidate_v1(candidate)
    return candidate, PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_OBJECT_BINDING


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    candidate_summary = candidate["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_V1,
        "review_status": PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_READY,
        "candidate_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "campaign_reexecution_performed": False,
        "new_strategy_scoring_performed": False,
        "walk_forward_validation_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": candidate_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "profitability": candidate_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
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
        "reviewed_candidate_kind": candidate[
            "artifact_kind"
        ],
        "reviewed_candidate_status": candidate["candidate_status"],
        "reviewed_candidate_digest": candidate["predictive_usefulness_review_candidate_digest"],
        "reviewed_candidate_checklist_total": candidate_summary["total_checks"],
        "reviewed_candidate_checklist_passed": candidate_summary["passed_checks"],
        "reviewed_candidate_checklist_failed": candidate_summary["failed_checks"],
        "reviewed_candidate_blocker_count": candidate_summary["blocker_count"],
        "campaign_execution_results_review_package_digest": candidate[
            "campaign_execution_results_review_package_digest"
        ],
        "campaign_execution_digest": candidate["campaign_execution_digest"],
        "execution_request_id": candidate["execution_request_id"],
        "campaign_execution_approval_digest": candidate["campaign_execution_approval_digest"],
        "campaign_execution_candidate_review_digest": candidate[
            "campaign_execution_candidate_review_digest"
        ],
        "campaign_plan_review_digest": candidate["campaign_plan_review_digest"],
        "dataset_availability_review_digest": candidate["dataset_availability_review_digest"],
        "swing_registry_approval_digest": candidate["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": candidate[
            "position_swing_registry_approval_digest"
        ],
        "outputs_reviewed": candidate["outputs_reviewed"],
        "all_outputs_research_only_non_actionable": candidate[
            "all_outputs_research_only_non_actionable"
        ],
        "dataset_load_status": candidate["dataset_load_status"],
        "schema_validation_status": candidate["schema_validation_status"],
        "bar_count_consistency_status": candidate["bar_count_consistency_status"],
        "date_range_coverage_status": candidate["date_range_coverage_status"],
        "ohlc_consistency_status": candidate["ohlc_consistency_status"],
        "volume_consistency_status": candidate["volume_consistency_status"],
        "indicator_calculation_status": candidate["indicator_calculation_status"],
        "module_compatibility_status": candidate["module_compatibility_status"],
        "failure_count": candidate["failure_count"],
        "warning_count": candidate["warning_count"],
        "data_quality_readiness": candidate["data_quality_readiness"],
        "module_compatibility_readiness": candidate["module_compatibility_readiness"],
        "predictive_experiment_results_available": candidate[
            "predictive_experiment_results_available"
        ],
        "walk_forward_results_available": candidate["walk_forward_results_available"],
        "out_of_sample_results_available": candidate["out_of_sample_results_available"],
        "label_definition_available": candidate["label_definition_available"],
        "predictive_metrics_available": candidate["predictive_metrics_available"],
        "additional_evidence_required": list(candidate["additional_evidence_required"]),
        "ready_for_predictive_experiment_planning": candidate_summary[
            "ready_for_predictive_experiment_planning"
        ],
        "evidence_classification": deepcopy(candidate["predictive_evidence_classification"]),
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }


def _data_quality_checks_passed(review_package: dict[str, Any]) -> bool:
    return all(
        review_package.get(field) == PASS
        for field in (
            "dataset_load_status",
            "schema_validation_status",
            "bar_count_consistency_status",
            "date_range_coverage_status",
            "ohlc_consistency_status",
            "volume_consistency_status",
            "indicator_calculation_status",
        )
    )


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("predictive_candidate_kind_matches", candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE, review_package.get("reviewed_candidate_kind")),
        _check("predictive_candidate_status_ready_for_review", candidate_service.PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_candidate_status")),
        _check("predictive_candidate_digest_matches", EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST, review_package.get("reviewed_candidate_digest")),
        _check("predictive_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_candidate_blocker_count")),
        _check("campaign_results_review_digest_bound", candidate_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("campaign_execution_results_review_package_digest")),
        _check("campaign_execution_digest_bound", candidate_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST, review_package.get("campaign_execution_digest")),
        _check("execution_request_id_bound", candidate_service.EXPECTED_EXECUTION_REQUEST_ID, review_package.get("execution_request_id")),
        _check("outputs_reviewed_12", 12, review_package.get("outputs_reviewed")),
        _check("outputs_research_only_non_actionable", True, review_package.get("all_outputs_research_only_non_actionable")),
        _check("data_quality_checks_passed", True, _data_quality_checks_passed(review_package)),
        _check("module_compatibility_listed", "RESEARCH_ONLY_COMPATIBILITY_LISTED", review_package.get("module_compatibility_status")),
        _check("failure_count_zero", 0, review_package.get("failure_count")),
        _check("warning_count_zero", 0, review_package.get("warning_count")),
        _check("data_quality_readiness_true", True, review_package.get("data_quality_readiness")),
        _check("module_compatibility_readiness_true", True, review_package.get("module_compatibility_readiness")),
        _check("predictive_experiment_results_available_false", False, review_package.get("predictive_experiment_results_available")),
        _check("walk_forward_results_available_false", False, review_package.get("walk_forward_results_available")),
        _check("out_of_sample_results_available_false", False, review_package.get("out_of_sample_results_available")),
        _check("label_definition_available_false", False, review_package.get("label_definition_available")),
        _check("predictive_metrics_available_false", False, review_package.get("predictive_metrics_available")),
        _check("additional_evidence_required_defined", candidate_service.ADDITIONAL_EVIDENCE_REQUIRED, review_package.get("additional_evidence_required")),
        _check("ready_for_predictive_experiment_planning_true", True, review_package.get("ready_for_predictive_experiment_planning")),
        _check("predictive_usefulness_not_accepted", candidate_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", candidate_service.acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, review_package.get("profitability_acceptance_ready")),
        _check("runtime_migration_recommended_false", False, review_package.get("runtime_migration_recommended")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("campaign_reexecution_performed_false", False, review_package.get("campaign_reexecution_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("walk_forward_validation_performed_false", False, review_package.get("walk_forward_validation_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    ready = failed == 0
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_assessment": ready,
        "ready_for_predictive_experiment_planning": ready,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_usefulness_review_candidate_review_package_digest", None)
    return payload


def predictive_usefulness_review_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_usefulness_review_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for the predictive usefulness candidate."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["predictive_usefulness_review_candidate_review_package_digest"] = (
        predictive_usefulness_review_candidate_review_package_digest_v1(review_package)
    )
    validate_predictive_usefulness_review_candidate_review_package_v1(review_package)
    return review_package


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
            raise PredictiveUsefulnessReviewCandidateReviewPackageError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made_in_review",
            "campaign_reexecution_performed",
            "new_strategy_scoring_performed",
            "walk_forward_validation_performed",
            "trade_recommendations_generated",
            "predictive_usefulness_acceptance_ready",
            "profitability_acceptance_ready",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise PredictiveUsefulnessReviewCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise PredictiveUsefulnessReviewCandidateReviewPackageError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveUsefulnessReviewCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_usefulness_review_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the operator review package without accepting predictive usefulness."""
    if not isinstance(review_package, dict):
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("candidate_binding_mode") not in {
        PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_STATUS_BINDING,
        PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_OBJECT_BINDING,
    }:
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(
            "candidate_binding_mode mismatch"
        )
    for field in ("operator_decision_required", "created_offline"):
        _expect_true(review_package.get(field), field)
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in (
        "provider_requests_made_in_review",
        "campaign_reexecution_performed",
        "new_strategy_scoring_performed",
        "walk_forward_validation_performed",
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
    for field, expected in {
        "predictive_usefulness": candidate_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": candidate_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_candidate_kind": (
            candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE
        ),
        "reviewed_candidate_status": (
            candidate_service.PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_candidate_digest": EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST,
        "reviewed_candidate_checklist_total": len(candidate_service.REQUIRED_CHECK_IDS),
        "reviewed_candidate_checklist_passed": len(candidate_service.REQUIRED_CHECK_IDS),
        "reviewed_candidate_checklist_failed": 0,
        "reviewed_candidate_blocker_count": 0,
        "campaign_execution_results_review_package_digest": (
            candidate_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_execution_digest": candidate_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "execution_request_id": candidate_service.EXPECTED_EXECUTION_REQUEST_ID,
        "campaign_execution_approval_digest": (
            candidate_service.EXPECTED_CAMPAIGN_EXECUTION_APPROVAL_DIGEST
        ),
        "campaign_execution_candidate_review_digest": (
            candidate_service.EXPECTED_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_DIGEST
        ),
        "campaign_plan_review_digest": candidate_service.EXPECTED_CAMPAIGN_PLAN_REVIEW_DIGEST,
        "dataset_availability_review_digest": (
            candidate_service.EXPECTED_DATASET_AVAILABILITY_REVIEW_DIGEST
        ),
        "swing_registry_approval_digest": (
            candidate_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "position_swing_registry_approval_digest": (
            candidate_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "outputs_reviewed": 12,
        "module_compatibility_status": "RESEARCH_ONLY_COMPATIBILITY_LISTED",
        "failure_count": 0,
        "warning_count": 0,
    }.items():
        _expect(review_package.get(field), expected, field)
    for field in (
        "dataset_load_status",
        "schema_validation_status",
        "bar_count_consistency_status",
        "date_range_coverage_status",
        "ohlc_consistency_status",
        "volume_consistency_status",
        "indicator_calculation_status",
    ):
        _expect(review_package.get(field), PASS, field)
    for field in (
        "all_outputs_research_only_non_actionable",
        "data_quality_readiness",
        "module_compatibility_readiness",
        "ready_for_predictive_experiment_planning",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "predictive_experiment_results_available",
        "walk_forward_results_available",
        "out_of_sample_results_available",
        "label_definition_available",
        "predictive_metrics_available",
    ):
        _expect_false(review_package.get(field), field)
    if review_package.get("additional_evidence_required") != (
        candidate_service.ADDITIONAL_EVIDENCE_REQUIRED
    ):
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(
            "additional_evidence_required mismatch"
        )
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessReviewCandidateReviewPackageError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("predictive_usefulness_review_candidate_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(
            "predictive_usefulness_review_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_review_candidate_review_package_digest_v1(review_package),
        "predictive_usefulness_review_candidate_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_usefulness_review_candidate_review_package_digest": digest,
        "reviewed_candidate_digest": review_package["reviewed_candidate_digest"],
        "campaign_execution_results_review_package_digest": review_package[
            "campaign_execution_results_review_package_digest"
        ],
        "campaign_execution_digest": review_package["campaign_execution_digest"],
        "execution_request_id": review_package["execution_request_id"],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
        "ready_for_predictive_experiment_planning": review_package["review_summary"][
            "ready_for_predictive_experiment_planning"
        ],
        "predictive_usefulness": candidate_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": candidate_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_predictive_usefulness_review_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized predictive usefulness candidate review package summary."""
    validation = validate_predictive_usefulness_review_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    classification = review_package["evidence_classification"]
    lines = [
        "# MarketFlow Predictive Usefulness Review Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Predictive Usefulness Review Candidate Operator Review Package v1.",
        "",
        "## Reviewed Predictive Usefulness Candidate",
        f"- Candidate kind: `{review_package['reviewed_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_candidate_digest']}`",
        f"- Review package digest: `{validation['predictive_usefulness_review_candidate_review_package_digest']}`",
        "",
        "## Source Research Results",
        f"- Campaign results review digest: `{review_package['campaign_execution_results_review_package_digest']}`",
        f"- Campaign execution digest: `{review_package['campaign_execution_digest']}`",
        f"- Execution request ID: `{review_package['execution_request_id']}`",
        f"- Outputs reviewed: `{review_package['outputs_reviewed']}`",
        "",
        "## Evidence Classification",
        f"- data_quality_readiness: `{classification['data_quality_readiness']}`",
        f"- module_compatibility_readiness: `{classification['module_compatibility_readiness']}`",
        f"- predictive_experiment_results_available: `{classification['predictive_experiment_results_available']}`",
        f"- walk_forward_results_available: `{classification['walk_forward_results_available']}`",
        f"- out_of_sample_results_available: `{classification['out_of_sample_results_available']}`",
        f"- label_definition_available: `{classification['label_definition_available']}`",
        f"- predictive_metrics_available: `{classification['predictive_metrics_available']}`",
        "",
        "## Additional Evidence Required",
    ]
    lines.extend(f"- `{item}`" for item in review_package["additional_evidence_required"])
    lines.extend(
        [
            "",
            "## Boundary Conditions",
            f"- provider_requests_made_in_review: `{review_package['provider_requests_made_in_review']}`",
            f"- campaign_reexecution_performed: `{review_package['campaign_reexecution_performed']}`",
            f"- new_strategy_scoring_performed: `{review_package['new_strategy_scoring_performed']}`",
            f"- walk_forward_validation_performed: `{review_package['walk_forward_validation_performed']}`",
            f"- trade_recommendations_generated: `{review_package['trade_recommendations_generated']}`",
            f"- runtime_migration_recommended: `{review_package['runtime_migration_recommended']}`",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
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
    )
    lines.extend(
        f"{index}. {task}"
        for index, task in enumerate(review_package["remaining_required_tasks"], start=1)
    )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No predictive experiments or walk-forward validation were executed.",
            "- No strategy scoring or trade recommendations were generated.",
            "- No predictive-usefulness or profitability acceptance occurred.",
            "- No runtime migration, paper trading, or broker execution was authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_review_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the predictive usefulness candidate review package without overwriting."""
    review_package = build_predictive_usefulness_review_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_predictive_usefulness_review_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_usefulness_review_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(
            "predictive usefulness candidate review package filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessReviewCandidateReviewPackageError(
            "predictive usefulness candidate review package output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
