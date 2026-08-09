"""Offline operator review package for the predictive usefulness assessment candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import predictive_usefulness_assessment_candidate_service as candidate_service


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE = (
    "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_V1 = (
    "predictive_usefulness_assessment_candidate_review_v1"
)
PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY"
)
PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_STATUS_BINDING = (
    "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_STATUS_BINDING"
)
PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_OBJECT_BINDING = (
    "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_DIGEST = (
    "b98c8fc1a6d64ddb1d3da313659b4e2105702e7d33550840cc00cb0008105598"
)
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = candidate_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    candidate_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = (
    candidate_service.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_ASSESSMENT_LIMITATIONS = list(candidate_service.ASSESSMENT_LIMITATIONS)
EXPECTED_NEXT_GATES = list(candidate_service.NEXT_GATES)

REQUIRED_CHECK_IDS = [
    "assessment_candidate_kind_matches",
    "assessment_candidate_status_ready_for_review",
    "assessment_candidate_digest_matches",
    "predictive_experiment_results_review_digest_bound",
    "predictive_experiment_execution_digest_bound",
    "predictive_experiment_execution_approval_digest_bound",
    "predictive_experiment_plan_digest_bound",
    "predictive_experiment_plan_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "output_count_13",
    "outputs_research_only_non_actionable",
    "metrics_label_research_only_not_performance_acceptance",
    "labels_generated_true",
    "feature_matrices_generated_true",
    "walk_forward_result_available",
    "out_of_sample_result_available",
    "baseline_results_available",
    "metric_results_available",
    "failure_warning_counts_unavailable_acknowledged",
    "data_quality_evidence_pass",
    "assessment_scope_research_only",
    "ticker_universe_aapl_only",
    "profiles_swing_and_position_swing",
    "assessment_limitations_defined",
    "next_gates_defined",
    "provider_requests_made_in_review_false",
    "experiment_reexecution_performed_false",
    "walk_forward_rerun_performed_false",
    "label_regeneration_performed_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
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
]


class PredictiveUsefulnessAssessmentCandidateReviewPackageError(ValueError):
    """Raised when the predictive usefulness assessment review package is invalid."""


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
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _recorded_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE,
        "assessment_status": (
            candidate_service.PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW
        ),
        "predictive_usefulness_assessment_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_DIGEST
        ),
        "source_results_review_package_digest": (
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
        "predictive_usefulness_review_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_review_candidate_review_package_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "assessment_scope": {
            "research_only": True,
            "ticker_universe": ["AAPL"],
            "date_range": {"start": "2022-01-01", "end": "2025-12-31"},
            "dataset_profiles": ["SWING", "POSITION_SWING"],
            "single_ticker_scope": True,
            "strategy_runtime_scope": "NOT_IN_SCOPE",
        },
        "reviewed_result_facts": {
            "output_count": 13,
            "all_outputs_research_only_non_actionable": True,
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "labels_generated": True,
            "feature_matrices_generated": True,
            "walk_forward_result_generated": True,
            "out_of_sample_result_generated": True,
            "baseline_result_count": 8,
            "metric_result_count": 8,
            "walk_forward_summary_status": "SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT",
            "out_of_sample_summary_status": "CHRONOLOGICAL_OOS_RESEARCH_SPLIT",
            "failure_count_status": candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
            "warning_count_status": candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
        },
        "predictive_evidence_classification": {
            "data_quality_evidence_status": PASS,
            "dataset_digest_evidence_status": PASS,
            "label_generation_evidence_status": PASS,
            "feature_matrix_evidence_status": PASS,
            "walk_forward_evidence_status": candidate_service.AVAILABLE_RESEARCH_ONLY,
            "out_of_sample_evidence_status": candidate_service.AVAILABLE_RESEARCH_ONLY,
            "baseline_comparison_evidence_status": candidate_service.AVAILABLE_RESEARCH_ONLY,
            "signal_metric_evidence_status": candidate_service.AVAILABLE_RESEARCH_ONLY,
            "metrics_acceptance_status": candidate_service.NOT_ACCEPTANCE_EVIDENCE,
            "failure_warning_count_status": candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
            "predictive_usefulness_assessment_state": (
                candidate_service.EVIDENCE_AVAILABLE_FOR_OPERATOR_ASSESSMENT
            ),
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_recommended": False,
            "predictive_usefulness_acceptance_requires_operator_ceremony": True,
            "profitability_acceptance_ready": False,
            "runtime_migration_recommended": False,
        },
        "assessment_limitations": list(EXPECTED_ASSESSMENT_LIMITATIONS),
        "additional_evidence_next_gates": list(EXPECTED_NEXT_GATES),
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
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
            _recorded_candidate(),
            PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_STATUS_BINDING,
        )
    candidate_service.validate_predictive_usefulness_assessment_candidate_v1(candidate)
    return (
        deepcopy(candidate),
        PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_OBJECT_BINDING,
    )


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    facts = candidate["reviewed_result_facts"]
    scope = candidate["assessment_scope"]
    classification = candidate["predictive_evidence_classification"]
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_V1,
        "review_status": PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY,
        "assessment_candidate_binding_mode": binding_mode,
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
        "reviewed_assessment_candidate_kind": candidate["artifact_kind"],
        "reviewed_assessment_candidate_status": candidate["assessment_status"],
        "reviewed_assessment_candidate_digest": candidate[
            "predictive_usefulness_assessment_candidate_digest"
        ],
        "predictive_experiment_results_review_package_digest": candidate[
            "source_results_review_package_digest"
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
        "predictive_usefulness_review_candidate_digest": candidate[
            "predictive_usefulness_review_candidate_digest"
        ],
        "predictive_usefulness_review_candidate_review_package_digest": candidate[
            "predictive_usefulness_review_candidate_review_package_digest"
        ],
        "swing_registry_approval_digest": candidate["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": candidate[
            "position_swing_registry_approval_digest"
        ],
        "assessment_scope": deepcopy(scope),
        "output_count": facts["output_count"],
        "all_outputs_research_only_non_actionable": facts[
            "all_outputs_research_only_non_actionable"
        ],
        "metrics_label": facts["metrics_label"],
        "labels_generated": facts["labels_generated"],
        "feature_matrices_generated": facts["feature_matrices_generated"],
        "walk_forward_result_generated": facts["walk_forward_result_generated"],
        "out_of_sample_result_generated": facts["out_of_sample_result_generated"],
        "baseline_result_count": facts["baseline_result_count"],
        "metric_result_count": facts["metric_result_count"],
        "walk_forward_summary_status": facts["walk_forward_summary_status"],
        "out_of_sample_summary_status": facts["out_of_sample_summary_status"],
        "failure_count_status": facts["failure_count_status"],
        "warning_count_status": facts["warning_count_status"],
        "assessment_classification": deepcopy(classification),
        "assessment_limitations": list(candidate["assessment_limitations"]),
        "additional_evidence_next_gates": list(candidate["additional_evidence_next_gates"]),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    classification = review_package.get("assessment_classification", {})
    scope = review_package.get("assessment_scope", {})
    return [
        _check("assessment_candidate_kind_matches", candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE, review_package.get("reviewed_assessment_candidate_kind")),
        _check("assessment_candidate_status_ready_for_review", candidate_service.PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_assessment_candidate_status")),
        _check("assessment_candidate_digest_matches", EXPECTED_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_DIGEST, review_package.get("reviewed_assessment_candidate_digest")),
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_experiment_results_review_package_digest")),
        _check("predictive_experiment_execution_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST, review_package.get("predictive_experiment_execution_digest")),
        _check("predictive_experiment_execution_approval_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST, review_package.get("predictive_experiment_execution_approval_digest")),
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, review_package.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_experiment_plan_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("position_swing_registry_approval_digest")),
        _check("output_count_13", 13, review_package.get("output_count")),
        _check("outputs_research_only_non_actionable", True, review_package.get("all_outputs_research_only_non_actionable")),
        _check("metrics_label_research_only_not_performance_acceptance", RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE, review_package.get("metrics_label")),
        _check("labels_generated_true", True, review_package.get("labels_generated")),
        _check("feature_matrices_generated_true", True, review_package.get("feature_matrices_generated")),
        _check("walk_forward_result_available", True, review_package.get("walk_forward_result_generated")),
        _check("out_of_sample_result_available", True, review_package.get("out_of_sample_result_generated")),
        _check("baseline_results_available", 8, review_package.get("baseline_result_count")),
        _check("metric_results_available", 8, review_package.get("metric_result_count")),
        _check("failure_warning_counts_unavailable_acknowledged", [candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS, candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS], [review_package.get("failure_count_status"), review_package.get("warning_count_status")]),
        _check("data_quality_evidence_pass", PASS, classification.get("data_quality_evidence_status")),
        _check("assessment_scope_research_only", True, scope.get("research_only")),
        _check("ticker_universe_aapl_only", ["AAPL"], scope.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["SWING", "POSITION_SWING"], scope.get("dataset_profiles")),
        _check("assessment_limitations_defined", EXPECTED_ASSESSMENT_LIMITATIONS, review_package.get("assessment_limitations")),
        _check("next_gates_defined", EXPECTED_NEXT_GATES, review_package.get("additional_evidence_next_gates")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("experiment_reexecution_performed_false", False, review_package.get("experiment_reexecution_performed")),
        _check("walk_forward_rerun_performed_false", False, review_package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, review_package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, review_package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, review_package.get("predictive_usefulness_acceptance_recommended")),
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
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_usefulness_assessment_candidate_review_package_digest", None)
    return payload


def predictive_usefulness_assessment_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_usefulness_assessment_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for the assessment candidate."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["predictive_usefulness_assessment_candidate_review_package_digest"] = (
        predictive_usefulness_assessment_candidate_review_package_digest_v1(review_package)
    )
    validate_predictive_usefulness_assessment_candidate_review_package_v1(review_package)
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
            "TRADE_RECOMMENDATIONS",
        }:
            raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
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
            "profitability_acceptance_ready",
            "profitability_acceptance_recommended",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_usefulness_assessment_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the operator review package without accepting predictive usefulness."""
    if not isinstance(review_package, dict):
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("assessment_candidate_binding_mode") not in {
        PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_STATUS_BINDING,
        PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_OBJECT_BINDING,
    }:
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            "assessment_candidate_binding_mode mismatch"
        )
    for field in ("operator_decision_required", "created_offline", "research_only"):
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
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
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
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_assessment_candidate_kind": (
            candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE
        ),
        "reviewed_assessment_candidate_status": (
            candidate_service.PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_assessment_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_DIGEST
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
        "predictive_usefulness_review_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_review_candidate_review_package_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "output_count": 13,
        "all_outputs_research_only_non_actionable": True,
        "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        "labels_generated": True,
        "feature_matrices_generated": True,
        "walk_forward_result_generated": True,
        "out_of_sample_result_generated": True,
        "baseline_result_count": 8,
        "metric_result_count": 8,
        "walk_forward_summary_status": "SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT",
        "out_of_sample_summary_status": "CHRONOLOGICAL_OOS_RESEARCH_SPLIT",
        "failure_count_status": candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
        "warning_count_status": candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
    }.items():
        _expect(review_package.get(field), expected, field)
    classification = review_package.get("assessment_classification")
    if not isinstance(classification, dict):
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            "assessment_classification missing"
        )
    _expect(classification.get("data_quality_evidence_status"), PASS, "data_quality_evidence_status")
    _expect(
        classification.get("metrics_acceptance_status"),
        candidate_service.NOT_ACCEPTANCE_EVIDENCE,
        "metrics_acceptance_status",
    )
    _expect_false(
        classification.get("predictive_usefulness_acceptance_ready"),
        "classification.predictive_usefulness_acceptance_ready",
    )
    _expect_false(
        classification.get("predictive_usefulness_acceptance_recommended"),
        "classification.predictive_usefulness_acceptance_recommended",
    )
    _expect_false(
        classification.get("profitability_acceptance_ready"),
        "classification.profitability_acceptance_ready",
    )
    _expect_false(
        classification.get("runtime_migration_recommended"),
        "classification.runtime_migration_recommended",
    )
    scope = review_package.get("assessment_scope")
    if not isinstance(scope, dict):
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError("assessment_scope missing")
    _expect_true(scope.get("research_only"), "assessment_scope.research_only")
    _expect(scope.get("ticker_universe"), ["AAPL"], "assessment_scope.ticker_universe")
    _expect(
        scope.get("dataset_profiles"),
        ["SWING", "POSITION_SWING"],
        "assessment_scope.dataset_profiles",
    )
    _expect(
        review_package.get("assessment_limitations"),
        EXPECTED_ASSESSMENT_LIMITATIONS,
        "assessment_limitations",
    )
    _expect(
        review_package.get("additional_evidence_next_gates"),
        EXPECTED_NEXT_GATES,
        "additional_evidence_next_gates",
    )
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
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
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "predictive_usefulness_assessment_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            "predictive_usefulness_assessment_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_assessment_candidate_review_package_digest_v1(review_package),
        "predictive_usefulness_assessment_candidate_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_usefulness_assessment_candidate_review_package_digest": digest,
        "reviewed_assessment_candidate_digest": review_package[
            "reviewed_assessment_candidate_digest"
        ],
        "predictive_experiment_results_review_package_digest": review_package[
            "predictive_experiment_results_review_package_digest"
        ],
        "predictive_experiment_execution_digest": review_package[
            "predictive_experiment_execution_digest"
        ],
        "predictive_experiment_execution_request_id": review_package[
            "predictive_experiment_execution_request_id"
        ],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_predictive_usefulness_assessment_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized predictive usefulness assessment candidate review summary."""
    validation = validate_predictive_usefulness_assessment_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    classification = review_package["assessment_classification"]
    lines = [
        "# MarketFlow Predictive Usefulness Assessment Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Predictive Usefulness Assessment Candidate Operator Review Package v1.",
        "",
        "## Reviewed Predictive Usefulness Assessment Candidate",
        f"- Candidate kind: `{review_package['reviewed_assessment_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_assessment_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_assessment_candidate_digest']}`",
        f"- Review package digest: `{validation['predictive_usefulness_assessment_candidate_review_package_digest']}`",
        "",
        "## Source Evidence",
        f"- Results review package digest: `{review_package['predictive_experiment_results_review_package_digest']}`",
        f"- Execution digest: `{review_package['predictive_experiment_execution_digest']}`",
        f"- Approval digest: `{review_package['predictive_experiment_execution_approval_digest']}`",
        f"- Execution request ID: `{review_package['predictive_experiment_execution_request_id']}`",
        "",
        "## Assessment Classification",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in classification.items())
    lines.extend(
        [
            "",
            "## Evidence Summary",
            f"- Output count: `{review_package['output_count']}`",
            f"- All outputs research-only non-actionable: `{review_package['all_outputs_research_only_non_actionable']}`",
            f"- Metrics label: `{review_package['metrics_label']}`",
            f"- Labels generated: `{review_package['labels_generated']}`",
            f"- Feature matrices generated: `{review_package['feature_matrices_generated']}`",
            f"- Walk-forward result generated: `{review_package['walk_forward_result_generated']}`",
            f"- Out-of-sample result generated: `{review_package['out_of_sample_result_generated']}`",
            f"- Baseline result count: `{review_package['baseline_result_count']}`",
            f"- Metric result count: `{review_package['metric_result_count']}`",
            "",
            "## Limitations",
        ]
    )
    lines.extend(f"- `{item}`" for item in review_package["assessment_limitations"])
    lines.extend(["", "## Additional Evidence / Next Gates"])
    lines.extend(f"- `{item}`" for item in review_package["additional_evidence_next_gates"])
    lines.extend(
        [
            "",
            "## Predictive/Profitability Boundary",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- predictive_usefulness_acceptance_ready: `{review_package['predictive_usefulness_acceptance_ready']}`",
            f"- predictive_usefulness_acceptance_recommended: `{review_package['predictive_usefulness_acceptance_recommended']}`",
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


def write_predictive_usefulness_assessment_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the assessment candidate review package without overwriting output."""
    review_package = build_predictive_usefulness_assessment_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_predictive_usefulness_assessment_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename or "predictive_usefulness_assessment_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            "predictive usefulness assessment candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessAssessmentCandidateReviewPackageError(
            "predictive usefulness assessment candidate review output already exists"
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
