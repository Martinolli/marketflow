"""Offline operator review package for the predictive usefulness acceptance readiness candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    predictive_usefulness_acceptance_readiness_candidate_service as readiness_service,
)


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_V1 = (
    "predictive_usefulness_acceptance_readiness_candidate_review_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE_READY"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_STATUS_BINDING = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_STATUS_BINDING"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_OBJECT_BINDING = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    "c6562d04616327bd1b293f36f9f80aa0c0713a02508e4f558803d0c528fd768e"
)
EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_TOTAL = 47
EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_PASSED = 47
EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_READINESS_CANDIDATE_BLOCKER_COUNT = 0

EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    readiness_service.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ASSESSMENT_CANDIDATE_DIGEST = readiness_service.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    readiness_service.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    readiness_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    readiness_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID = (
    readiness_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    readiness_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    readiness_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = readiness_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    readiness_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

ACCEPTANCE_READINESS_STATE_NOT_READY = readiness_service.ACCEPTANCE_READINESS_STATE_NOT_READY
ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED = (
    readiness_service.ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED
)
NOT_READY_REASONS = list(readiness_service.NOT_READY_REASONS)
ADDITIONAL_EVIDENCE_REQUIRED = list(readiness_service.ADDITIONAL_EVIDENCE_REQUIRED)
NEXT_GATES = list(readiness_service.NEXT_GATES)
NOT_AUTHORIZED = readiness_service.NOT_AUTHORIZED
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = (
    readiness_service.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_CHECK_IDS = [
    "readiness_candidate_kind_matches",
    "readiness_candidate_status_not_ready",
    "readiness_candidate_digest_matches",
    "readiness_candidate_checklist_zero_blockers",
    "assessment_candidate_review_digest_bound",
    "assessment_candidate_digest_bound",
    "predictive_experiment_results_review_digest_bound",
    "predictive_experiment_execution_digest_bound",
    "predictive_experiment_execution_approval_digest_bound",
    "predictive_experiment_plan_digest_bound",
    "predictive_experiment_plan_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "acceptance_readiness_state_not_ready",
    "acceptance_readiness_reason_limited_evidence",
    "predictive_evidence_available_for_review_true",
    "predictive_evidence_sufficient_for_acceptance_false",
    "ready_for_acceptance_candidate_false",
    "reasons_acceptance_not_ready_defined",
    "additional_evidence_required_defined",
    "next_gates_defined",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
    "predictive_usefulness_acceptance_candidate_created_false",
    "predictive_usefulness_acceptance_ceremony_required_true",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "profitability_acceptance_recommended_false",
    "runtime_migration_recommended_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "provider_requests_made_in_review_false",
    "experiment_reexecution_performed_false",
    "walk_forward_rerun_performed_false",
    "label_regeneration_performed_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_predictive_usefulness_acceptance_candidate_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(ValueError):
    """Raised when the acceptance readiness candidate review package is invalid."""


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
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _recorded_readiness_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": (
            readiness_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE
        ),
        "candidate_status": (
            readiness_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
        ),
        "readiness_summary": {
            "total_checks": EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_TOTAL,
            "passed_checks": EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_PASSED,
            "failed_checks": EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_FAILED,
            "blocker_count": EXPECTED_REVIEWED_READINESS_CANDIDATE_BLOCKER_COUNT,
            "ready_for_operator_review": True,
            "ready_for_acceptance_candidate": False,
        },
        "predictive_usefulness_assessment_candidate_review_package_digest": (
            EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_assessment_candidate_digest": EXPECTED_ASSESSMENT_CANDIDATE_DIGEST,
        "predictive_experiment_results_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_execution_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
        ),
        "predictive_experiment_execution_approval_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
        ),
        "predictive_experiment_execution_request_id": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
        ),
        "predictive_experiment_plan_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
        "predictive_experiment_plan_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "acceptance_readiness_state": ACCEPTANCE_READINESS_STATE_NOT_READY,
        "acceptance_readiness_reason": ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED,
        "predictive_evidence_available_for_review": True,
        "predictive_evidence_sufficient_for_acceptance": False,
        "acceptance_not_ready_reasons": list(NOT_READY_REASONS),
        "additional_evidence_required": list(ADDITIONAL_EVIDENCE_REQUIRED),
        "next_gates": list(NEXT_GATES),
        "created_offline": True,
        "provider_requests_made": False,
        "experiment_reexecution_performed": False,
        "walk_forward_rerun_performed": False,
        "label_regeneration_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ceremony_required": True,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
    }


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            _recorded_readiness_candidate(),
            PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_STATUS_BINDING,
        )
    readiness_service.validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)
    return (
        deepcopy(candidate),
        PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_OBJECT_BINDING,
    )


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["readiness_summary"]
    return {
        "artifact_kind": (
            ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE
        ),
        "schema_version": (
            SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_V1
        ),
        "review_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE_READY,
        "readiness_candidate_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "experiment_reexecution_performed": False,
        "walk_forward_rerun_performed": False,
        "label_regeneration_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ceremony_required": True,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness_acceptance_candidate_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "reviewed_readiness_candidate_kind": candidate["artifact_kind"],
        "reviewed_readiness_candidate_status": candidate["candidate_status"],
        "reviewed_readiness_candidate_digest": candidate[
            "predictive_usefulness_acceptance_readiness_candidate_digest"
        ],
        "reviewed_readiness_candidate_checklist_total": summary["total_checks"],
        "reviewed_readiness_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_readiness_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_readiness_candidate_blocker_count": summary["blocker_count"],
        "predictive_usefulness_assessment_candidate_review_package_digest": candidate[
            "predictive_usefulness_assessment_candidate_review_package_digest"
        ],
        "predictive_usefulness_assessment_candidate_digest": candidate[
            "predictive_usefulness_assessment_candidate_digest"
        ],
        "predictive_experiment_results_review_package_digest": candidate[
            "predictive_experiment_results_review_package_digest"
        ],
        "predictive_experiment_execution_digest": candidate[
            "predictive_experiment_execution_digest"
        ],
        "predictive_experiment_execution_approval_digest": candidate[
            "predictive_experiment_execution_approval_digest"
        ],
        "predictive_experiment_execution_request_id": candidate[
            "predictive_experiment_execution_request_id"
        ],
        "predictive_experiment_plan_digest": candidate["predictive_experiment_plan_digest"],
        "predictive_experiment_plan_review_package_digest": candidate[
            "predictive_experiment_plan_review_package_digest"
        ],
        "swing_registry_approval_digest": candidate["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": candidate[
            "position_swing_registry_approval_digest"
        ],
        "acceptance_readiness_state": candidate["acceptance_readiness_state"],
        "acceptance_readiness_reason": candidate["acceptance_readiness_reason"],
        "predictive_evidence_available_for_review": candidate[
            "predictive_evidence_available_for_review"
        ],
        "predictive_evidence_sufficient_for_acceptance": candidate[
            "predictive_evidence_sufficient_for_acceptance"
        ],
        "ready_for_acceptance_candidate": False,
        "acceptance_not_ready_reasons": list(candidate["acceptance_not_ready_reasons"]),
        "additional_evidence_required": list(candidate["additional_evidence_required"]),
        "next_gates": list(candidate["next_gates"]),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("readiness_candidate_kind_matches", readiness_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE, review_package.get("reviewed_readiness_candidate_kind")),
        _check("readiness_candidate_status_not_ready", readiness_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE, review_package.get("reviewed_readiness_candidate_status")),
        _check("readiness_candidate_digest_matches", EXPECTED_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_DIGEST, review_package.get("reviewed_readiness_candidate_digest")),
        _check("readiness_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_readiness_candidate_blocker_count")),
        _check("assessment_candidate_review_digest_bound", EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_usefulness_assessment_candidate_review_package_digest")),
        _check("assessment_candidate_digest_bound", EXPECTED_ASSESSMENT_CANDIDATE_DIGEST, review_package.get("predictive_usefulness_assessment_candidate_digest")),
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_experiment_results_review_package_digest")),
        _check("predictive_experiment_execution_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST, review_package.get("predictive_experiment_execution_digest")),
        _check("predictive_experiment_execution_approval_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST, review_package.get("predictive_experiment_execution_approval_digest")),
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, review_package.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_experiment_plan_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("position_swing_registry_approval_digest")),
        _check("acceptance_readiness_state_not_ready", ACCEPTANCE_READINESS_STATE_NOT_READY, review_package.get("acceptance_readiness_state")),
        _check("acceptance_readiness_reason_limited_evidence", ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED, review_package.get("acceptance_readiness_reason")),
        _check("predictive_evidence_available_for_review_true", True, review_package.get("predictive_evidence_available_for_review")),
        _check("predictive_evidence_sufficient_for_acceptance_false", False, review_package.get("predictive_evidence_sufficient_for_acceptance")),
        _check("ready_for_acceptance_candidate_false", False, review_package.get("ready_for_acceptance_candidate")),
        _check("reasons_acceptance_not_ready_defined", NOT_READY_REASONS, review_package.get("acceptance_not_ready_reasons")),
        _check("additional_evidence_required_defined", ADDITIONAL_EVIDENCE_REQUIRED, review_package.get("additional_evidence_required")),
        _check("next_gates_defined", NEXT_GATES, review_package.get("next_gates")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, review_package.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, review_package.get("predictive_usefulness_acceptance_candidate_created")),
        _check("predictive_usefulness_acceptance_ceremony_required_true", True, review_package.get("predictive_usefulness_acceptance_ceremony_required")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, review_package.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, review_package.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, review_package.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("experiment_reexecution_performed_false", False, review_package.get("experiment_reexecution_performed")),
        _check("walk_forward_rerun_performed_false", False, review_package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, review_package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, review_package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_predictive_usefulness_acceptance_candidate_created", False, review_package.get("predictive_usefulness_acceptance_candidate_artifact_created")),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_artifact_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_artifact_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_assessment": failed == 0,
        "ready_for_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop(
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest",
        None,
    )
    return payload


def predictive_usefulness_acceptance_readiness_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for the acceptance readiness candidate."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package[
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    ] = predictive_usefulness_acceptance_readiness_candidate_review_package_digest_v1(
        review_package
    )
    validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
            "TRADE_RECOMMENDATIONS",
        }:
            raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made_in_review",
            "experiment_reexecution_performed",
            "walk_forward_rerun_performed",
            "label_regeneration_performed",
            "feature_matrix_regeneration_performed",
            "new_strategy_scoring_performed",
            "trade_recommendations_generated",
            "predictive_usefulness_acceptance_ready",
            "predictive_usefulness_acceptance_recommended",
            "predictive_usefulness_acceptance_candidate_created",
            "profitability_acceptance_ready",
            "profitability_acceptance_recommended",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "predictive_evidence_sufficient_for_acceptance",
            "ready_for_acceptance_candidate",
        } and value is True:
            raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the review package without accepting usefulness or runtime use."""
    if not isinstance(review_package, dict):
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("readiness_candidate_binding_mode") not in {
        PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_STATUS_BINDING,
        PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_OBJECT_BINDING,
    }:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            "readiness_candidate_binding_mode mismatch"
        )
    for field in (
        "operator_decision_required",
        "created_offline",
        "research_only",
        "predictive_usefulness_acceptance_ceremony_required",
        "predictive_evidence_available_for_review",
    ):
        _expect_true(review_package.get(field), field)
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in (
        "provider_requests_made_in_review",
        "experiment_reexecution_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_evidence_sufficient_for_acceptance",
        "ready_for_acceptance_candidate",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_acceptance_candidate_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_readiness_candidate_kind": (
            readiness_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE
        ),
        "reviewed_readiness_candidate_status": (
            readiness_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE
        ),
        "reviewed_readiness_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
        ),
        "reviewed_readiness_candidate_checklist_total": (
            EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_TOTAL
        ),
        "reviewed_readiness_candidate_checklist_passed": (
            EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_PASSED
        ),
        "reviewed_readiness_candidate_checklist_failed": (
            EXPECTED_REVIEWED_READINESS_CANDIDATE_CHECKLIST_FAILED
        ),
        "reviewed_readiness_candidate_blocker_count": (
            EXPECTED_REVIEWED_READINESS_CANDIDATE_BLOCKER_COUNT
        ),
        "predictive_usefulness_assessment_candidate_review_package_digest": (
            EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_assessment_candidate_digest": (
            EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
        ),
        "predictive_experiment_results_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_execution_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
        ),
        "predictive_experiment_execution_approval_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
        ),
        "predictive_experiment_execution_request_id": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
        ),
        "predictive_experiment_plan_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
        "predictive_experiment_plan_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "acceptance_readiness_state": ACCEPTANCE_READINESS_STATE_NOT_READY,
        "acceptance_readiness_reason": ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED,
    }.items():
        _expect(review_package.get(field), expected, field)
    _expect(
        review_package.get("acceptance_not_ready_reasons"),
        NOT_READY_REASONS,
        "acceptance_not_ready_reasons",
    )
    _expect(
        review_package.get("additional_evidence_required"),
        ADDITIONAL_EVIDENCE_REQUIRED,
        "additional_evidence_required",
    )
    _expect(review_package.get("next_gates"), NEXT_GATES, "next_gates")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            "predictive_usefulness_acceptance_readiness_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_acceptance_readiness_candidate_review_package_digest_v1(
            review_package
        ),
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest",
    )
    return {
        "status": (
            "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE_VALID"
        ),
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": digest,
        "reviewed_readiness_candidate_digest": review_package[
            "reviewed_readiness_candidate_digest"
        ],
        "predictive_usefulness_assessment_candidate_review_package_digest": review_package[
            "predictive_usefulness_assessment_candidate_review_package_digest"
        ],
        "predictive_usefulness_assessment_candidate_digest": review_package[
            "predictive_usefulness_assessment_candidate_digest"
        ],
        "predictive_experiment_results_review_package_digest": review_package[
            "predictive_experiment_results_review_package_digest"
        ],
        "acceptance_readiness_state": review_package["acceptance_readiness_state"],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
        "ready_for_acceptance_candidate": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_predictive_usefulness_acceptance_readiness_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized acceptance readiness candidate review summary."""
    validation = validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Predictive Usefulness Acceptance Readiness Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Predictive Usefulness Acceptance Readiness Candidate Operator Review Package v1.",
        "",
        "## Reviewed Acceptance Readiness Candidate",
        f"- Candidate kind: `{review_package['reviewed_readiness_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_readiness_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_readiness_candidate_digest']}`",
        f"- Review package digest: `{validation['predictive_usefulness_acceptance_readiness_candidate_review_package_digest']}`",
        "",
        "## Readiness Classification",
        f"- acceptance_readiness_state: `{review_package['acceptance_readiness_state']}`",
        f"- acceptance_readiness_reason: `{review_package['acceptance_readiness_reason']}`",
        f"- predictive_evidence_available_for_review: `{review_package['predictive_evidence_available_for_review']}`",
        f"- predictive_evidence_sufficient_for_acceptance: `{review_package['predictive_evidence_sufficient_for_acceptance']}`",
        f"- ready_for_acceptance_candidate: `{review_package['ready_for_acceptance_candidate']}`",
        "",
        "## Reasons Acceptance Is Not Ready",
    ]
    lines.extend(f"- `{item}`" for item in review_package["acceptance_not_ready_reasons"])
    lines.extend(["", "## Additional Evidence Required"])
    lines.extend(f"- `{item}`" for item in review_package["additional_evidence_required"])
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in review_package["next_gates"])
    lines.extend(
        [
            "",
            "## Predictive/Profitability Boundary",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- predictive_usefulness_acceptance_ready: `{review_package['predictive_usefulness_acceptance_ready']}`",
            f"- predictive_usefulness_acceptance_recommended: `{review_package['predictive_usefulness_acceptance_recommended']}`",
            f"- predictive_usefulness_acceptance_candidate_created: `{review_package['predictive_usefulness_acceptance_candidate_created']}`",
            f"- profitability: `{review_package['profitability']}`",
            f"- profitability_acceptance_ready: `{review_package['profitability_acceptance_ready']}`",
            f"- profitability_acceptance_recommended: `{review_package['profitability_acceptance_recommended']}`",
            "",
            "## Runtime Boundary",
            f"- provider_requests_made_in_review: `{review_package['provider_requests_made_in_review']}`",
            f"- experiment_reexecution_performed: `{review_package['experiment_reexecution_performed']}`",
            f"- walk_forward_rerun_performed: `{review_package['walk_forward_rerun_performed']}`",
            f"- label_regeneration_performed: `{review_package['label_regeneration_performed']}`",
            f"- feature_matrix_regeneration_performed: `{review_package['feature_matrix_regeneration_performed']}`",
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
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No predictive experiment, walk-forward, label, or feature-matrix rerun occurred.",
            "- No strategy scoring or trade recommendations were generated.",
            "- No predictive-usefulness or profitability acceptance occurred.",
            "- No runtime migration, paper trading, or broker execution was authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the acceptance readiness candidate review package without overwriting output."""
    review_package = (
        build_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            candidate=candidate
        )
    )
    validation = validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "predictive_usefulness_acceptance_readiness_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            "predictive usefulness acceptance readiness candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError(
            "predictive usefulness acceptance readiness candidate review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
