"""Offline predictive usefulness assessment candidate from reviewed experiment results."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import predictive_experiment_execution_results_review_service as results_review


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE = (
    "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_V1 = (
    "predictive_usefulness_assessment_candidate_v1"
)
PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW = (
    "PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW"
)
PREDICTIVE_USEFULNESS_ASSESSMENT_REQUIRES_ADDITIONAL_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ASSESSMENT_REQUIRES_ADDITIONAL_EVIDENCE"
)

EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "281e2f0ce4f6050b4788188202003605af95af104b887374484bb1f46ce2b804"
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    results_review.EXPECTED_SOURCE_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    results_review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID = (
    results_review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    results_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    results_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST = (
    results_review.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    results_review.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = results_review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    results_review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

NOT_AUTHORIZED = results_review.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = results_review.RESEARCH_ONLY_NON_ACTIONABLE
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = (
    results_review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
AVAILABLE_RESEARCH_ONLY = "AVAILABLE_RESEARCH_ONLY"
NOT_ACCEPTANCE_EVIDENCE = "NOT_ACCEPTANCE_EVIDENCE"
UNAVAILABLE_IN_SOURCE_REPORTS = "UNAVAILABLE_IN_SOURCE_REPORTS"
EVIDENCE_AVAILABLE_FOR_OPERATOR_ASSESSMENT = "EVIDENCE_AVAILABLE_FOR_OPERATOR_ASSESSMENT"

ASSESSMENT_LIMITATIONS = [
    "single_ticker_scope",
    "single_asset_class_scope_if_applicable",
    "research_only_outputs",
    "simplified_chronological_split",
    "no_runtime_strategy_validation",
    "no transaction_cost_model",
    "no slippage_model",
    "no live_or_paper_trading_validation",
    "no profitability_acceptance",
    "no predictive_usefulness_acceptance",
    "failure_warning_counts_unavailable_in_source_reports",
    "operator_acceptance_ceremony_required",
]

NEXT_GATES = [
    "predictive_usefulness_assessment_operator_review",
    "predictive_usefulness_acceptance_candidate_if_operator_deems_sufficient",
    "profitability_review_candidate",
    "transaction_cost_and_slippage_model_if_profitability_is_reviewed",
    "multi_ticker_or_out_of-domain_generalization_if_required",
    "runtime_migration_approval_ceremony_if_ever_authorized",
]

REQUIRED_CHECK_IDS = [
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
    "provider_requests_made_false",
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
    "assessment_limitations_defined",
    "next_gates_defined",
]


class PredictiveUsefulnessAssessmentCandidateError(ValueError):
    """Raised when the predictive usefulness assessment candidate is invalid."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} passed" if status == PASS else f"{check_id} failed",
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessAssessmentCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessAssessmentCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessAssessmentCandidateError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _source_results_review_package(
    results_review_package: dict[str, Any] | None,
) -> dict[str, Any]:
    if results_review_package is not None:
        return deepcopy(results_review_package)
    package = results_review.build_predictive_experiment_execution_results_review_package_v1()
    results_review.validate_predictive_experiment_execution_results_review_package_v1(package)
    return package


def _failure_warning_status(value: Any) -> str:
    return UNAVAILABLE_IN_SOURCE_REPORTS if value == "unavailable" else str(value)


def _assessment_status(source: dict[str, Any]) -> str:
    ready = (
        source.get("predictive_experiment_execution_results_review_package_digest")
        == EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        and source.get("review_status")
        == results_review.PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY
        and source.get("actual_output_count") == results_review.EXPECTED_OUTPUT_COUNT
        and source.get("all_outputs_research_only_non_actionable") is True
        and source.get("metrics_labeled_research_only_not_performance_acceptance") is True
        and source.get("labels_generated") is True
        and source.get("feature_matrices_generated") is True
        and source.get("walk_forward_result_generated") is True
        and source.get("out_of_sample_result_generated") is True
        and source.get("baseline_result_count") == 8
        and source.get("metric_result_count") == 8
        and source.get("failure_count") == "unavailable"
        and source.get("warning_count") == "unavailable"
    )
    return (
        PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW
        if ready
        else PREDICTIVE_USEFULNESS_ASSESSMENT_REQUIRES_ADDITIONAL_EVIDENCE
    )


def _assessment_scope(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "research_only": True,
        "ticker_universe": ["AAPL"],
        "date_range": {"start": "2022-01-01", "end": "2025-12-31"},
        "dataset_profiles": ["SWING", "POSITION_SWING"],
        "output_root": source.get("output_root"),
        "single_ticker_scope": True,
        "strategy_runtime_scope": "NOT_IN_SCOPE",
    }


def _reviewed_result_facts(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "output_count": source.get("actual_output_count"),
        "all_outputs_research_only_non_actionable": source.get(
            "all_outputs_research_only_non_actionable"
        ),
        "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        "labels_generated": source.get("labels_generated"),
        "feature_matrices_generated": source.get("feature_matrices_generated"),
        "walk_forward_result_generated": source.get("walk_forward_result_generated"),
        "out_of_sample_result_generated": source.get("out_of_sample_result_generated"),
        "baseline_result_count": source.get("baseline_result_count"),
        "metric_result_count": source.get("metric_result_count"),
        "walk_forward_summary_status": source.get("walk_forward_summary_status"),
        "out_of_sample_summary_status": source.get("out_of_sample_summary_status"),
        "failure_count_status": _failure_warning_status(source.get("failure_count")),
        "warning_count_status": _failure_warning_status(source.get("warning_count")),
        "leakage_control_status": source.get("leakage_control_status"),
        "dataset_summary": deepcopy(source.get("dataset_summary")),
    }


def _classification() -> dict[str, Any]:
    return {
        "data_quality_evidence_status": PASS,
        "dataset_digest_evidence_status": PASS,
        "label_generation_evidence_status": PASS,
        "feature_matrix_evidence_status": PASS,
        "walk_forward_evidence_status": AVAILABLE_RESEARCH_ONLY,
        "out_of_sample_evidence_status": AVAILABLE_RESEARCH_ONLY,
        "baseline_comparison_evidence_status": AVAILABLE_RESEARCH_ONLY,
        "signal_metric_evidence_status": AVAILABLE_RESEARCH_ONLY,
        "metrics_acceptance_status": NOT_ACCEPTANCE_EVIDENCE,
        "failure_warning_count_status": UNAVAILABLE_IN_SOURCE_REPORTS,
        "predictive_usefulness_assessment_state": EVIDENCE_AVAILABLE_FOR_OPERATOR_ASSESSMENT,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_requires_operator_ceremony": True,
        "profitability_acceptance_ready": False,
        "runtime_migration_recommended": False,
    }


def _base_candidate(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_V1,
        "created_offline": True,
        "provider_requests_made": False,
        "experiment_reexecution_performed": False,
        "walk_forward_rerun_performed": False,
        "label_regeneration_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "operator_review_required": True,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_requires_operator_ceremony": True,
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
        "source_results_review_artifact_kind": (
            results_review.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE
        ),
        "source_results_review_status": source.get("review_status"),
        "source_results_review_package_digest": source.get(
            "predictive_experiment_execution_results_review_package_digest"
        ),
        "predictive_experiment_execution_digest": source.get("source_execution_digest"),
        "predictive_experiment_execution_request_id": source.get(
            "source_execution_request_id"
        ),
        "predictive_experiment_execution_approval_digest": source.get(
            "source_execution_approval_digest"
        ),
        "predictive_experiment_plan_digest": source.get("predictive_experiment_plan_digest"),
        "predictive_experiment_plan_review_package_digest": source.get(
            "predictive_experiment_plan_review_package_digest"
        ),
        "predictive_usefulness_review_candidate_digest": source.get(
            "predictive_usefulness_review_candidate_digest"
        ),
        "predictive_usefulness_review_candidate_review_package_digest": source.get(
            "predictive_usefulness_review_candidate_review_package_digest"
        ),
        "swing_registry_approval_digest": source.get("swing_registry_approval_digest"),
        "position_swing_registry_approval_digest": source.get(
            "position_swing_registry_approval_digest"
        ),
        "assessment_scope": _assessment_scope(source),
        "reviewed_result_facts": _reviewed_result_facts(source),
        "predictive_evidence_classification": _classification(),
        "assessment_limitations": list(ASSESSMENT_LIMITATIONS),
        "additional_evidence_next_gates": list(NEXT_GATES),
        "source_results_review_summary": deepcopy(source.get("review_summary")),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    facts = candidate.get("reviewed_result_facts", {})
    scope = candidate.get("assessment_scope", {})
    classification = candidate.get("predictive_evidence_classification", {})
    return [
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("source_results_review_package_digest")),
        _check("predictive_experiment_execution_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST, candidate.get("predictive_experiment_execution_digest")),
        _check("predictive_experiment_execution_approval_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST, candidate.get("predictive_experiment_execution_approval_digest")),
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, candidate.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_experiment_plan_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("position_swing_registry_approval_digest")),
        _check("output_count_13", results_review.EXPECTED_OUTPUT_COUNT, facts.get("output_count")),
        _check("outputs_research_only_non_actionable", True, facts.get("all_outputs_research_only_non_actionable")),
        _check("metrics_label_research_only_not_performance_acceptance", RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE, facts.get("metrics_label")),
        _check("labels_generated_true", True, facts.get("labels_generated")),
        _check("feature_matrices_generated_true", True, facts.get("feature_matrices_generated")),
        _check("walk_forward_result_available", True, facts.get("walk_forward_result_generated")),
        _check("out_of_sample_result_available", True, facts.get("out_of_sample_result_generated")),
        _check("baseline_results_available", 8, facts.get("baseline_result_count")),
        _check("metric_results_available", 8, facts.get("metric_result_count")),
        _check("failure_warning_counts_unavailable_acknowledged", [UNAVAILABLE_IN_SOURCE_REPORTS, UNAVAILABLE_IN_SOURCE_REPORTS], [facts.get("failure_count_status"), facts.get("warning_count_status")]),
        _check("data_quality_evidence_pass", PASS, classification.get("data_quality_evidence_status")),
        _check("assessment_scope_research_only", True, scope.get("research_only")),
        _check("ticker_universe_aapl_only", ["AAPL"], scope.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["SWING", "POSITION_SWING"], scope.get("dataset_profiles")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("experiment_reexecution_performed_false", False, candidate.get("experiment_reexecution_performed")),
        _check("walk_forward_rerun_performed_false", False, candidate.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, candidate.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, candidate.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, candidate.get("predictive_usefulness_acceptance_recommended")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        _check("profitability_acceptance_ready_false", False, candidate.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, candidate.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, candidate.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("assessment_limitations_defined", ASSESSMENT_LIMITATIONS, candidate.get("assessment_limitations")),
        _check("next_gates_defined", NEXT_GATES, candidate.get("additional_evidence_next_gates")),
    ]


def _summary(checklist: list[dict[str, Any]], *, assessment_status: str) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    ready = (
        assessment_status == PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW
        and failed == 0
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": ready,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("predictive_usefulness_assessment_candidate_digest", None)
    return payload


def predictive_usefulness_assessment_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the assessment candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_predictive_usefulness_assessment_candidate_v1(
    results_review_package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline assessment candidate from reviewed predictive experiment results."""
    source = _source_results_review_package(results_review_package)
    candidate = _base_candidate(source)
    candidate["assessment_status"] = _assessment_status(source)
    candidate["assessment_checklist"] = _checklist(candidate)
    candidate["assessment_summary"] = _summary(
        candidate["assessment_checklist"],
        assessment_status=candidate["assessment_status"],
    )
    candidate["predictive_usefulness_assessment_candidate_digest"] = (
        predictive_usefulness_assessment_candidate_digest_v1(candidate)
    )
    validate_predictive_usefulness_assessment_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
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
            raise PredictiveUsefulnessAssessmentCandidateError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made",
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
            raise PredictiveUsefulnessAssessmentCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PredictiveUsefulnessAssessmentCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveUsefulnessAssessmentCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_usefulness_assessment_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate an assessment candidate without granting acceptance or runtime use."""
    if not isinstance(candidate, dict):
        raise PredictiveUsefulnessAssessmentCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_V1,
        "schema_version",
    )
    status = candidate.get("assessment_status")
    if status not in {
        PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW,
        PREDICTIVE_USEFULNESS_ASSESSMENT_REQUIRES_ADDITIONAL_EVIDENCE,
    }:
        raise PredictiveUsefulnessAssessmentCandidateError("assessment_status mismatch")
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "predictive_usefulness_acceptance_requires_operator_ceremony",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
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
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    _expect(
        candidate.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(candidate.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "source_results_review_artifact_kind": (
            results_review.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE
        ),
        "source_results_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_execution_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
        ),
        "predictive_experiment_execution_request_id": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
        ),
        "predictive_experiment_execution_approval_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
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
    }.items():
        _expect(candidate.get(field), expected, field)
    facts = candidate.get("reviewed_result_facts")
    if not isinstance(facts, dict):
        raise PredictiveUsefulnessAssessmentCandidateError("reviewed_result_facts missing")
    for field, expected in {
        "output_count": results_review.EXPECTED_OUTPUT_COUNT,
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
        "failure_count_status": UNAVAILABLE_IN_SOURCE_REPORTS,
        "warning_count_status": UNAVAILABLE_IN_SOURCE_REPORTS,
    }.items():
        _expect(facts.get(field), expected, f"reviewed_result_facts.{field}")
    classification = candidate.get("predictive_evidence_classification")
    if classification != _classification():
        raise PredictiveUsefulnessAssessmentCandidateError(
            "predictive_evidence_classification mismatch"
        )
    scope = candidate.get("assessment_scope")
    if not isinstance(scope, dict):
        raise PredictiveUsefulnessAssessmentCandidateError("assessment_scope missing")
    _expect(scope.get("ticker_universe"), ["AAPL"], "assessment_scope.ticker_universe")
    _expect(
        scope.get("dataset_profiles"),
        ["SWING", "POSITION_SWING"],
        "assessment_scope.dataset_profiles",
    )
    _expect_true(scope.get("research_only"), "assessment_scope.research_only")
    _expect(candidate.get("assessment_limitations"), ASSESSMENT_LIMITATIONS, "assessment_limitations")
    _expect(candidate.get("additional_evidence_next_gates"), NEXT_GATES, "additional_evidence_next_gates")
    checklist = candidate.get("assessment_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessAssessmentCandidateError("assessment_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "assessment_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    if status == PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW:
        failed = [item for item in expected_checklist if item["status"] != PASS]
        if failed:
            raise PredictiveUsefulnessAssessmentCandidateError(
                f"assessment checklist contains failed check: {failed[0]['check_id']}"
            )
    _expect(checklist, expected_checklist, "assessment_checklist")
    expected_summary = _summary(expected_checklist, assessment_status=status)
    _expect(candidate.get("assessment_summary"), expected_summary, "assessment_summary")
    digest = candidate.get("predictive_usefulness_assessment_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAssessmentCandidateError(
            "predictive_usefulness_assessment_candidate_digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_assessment_candidate_digest_v1(candidate),
        "predictive_usefulness_assessment_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "assessment_status": candidate["assessment_status"],
        "predictive_usefulness_assessment_candidate_digest": digest,
        "source_results_review_package_digest": candidate["source_results_review_package_digest"],
        "predictive_experiment_execution_digest": candidate[
            "predictive_experiment_execution_digest"
        ],
        "predictive_experiment_execution_request_id": candidate[
            "predictive_experiment_execution_request_id"
        ],
        "ready_for_operator_review": candidate["assessment_summary"][
            "ready_for_operator_review"
        ],
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_predictive_usefulness_assessment_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized predictive usefulness assessment candidate summary."""
    validation = validate_predictive_usefulness_assessment_candidate_v1(candidate)
    summary = candidate["assessment_summary"]
    facts = candidate["reviewed_result_facts"]
    classification = candidate["predictive_evidence_classification"]
    lines = [
        "# MarketFlow Predictive Usefulness Assessment Candidate Status",
        "",
        "## Purpose",
        "- Summarize reviewed predictive experiment results for operator assessment.",
        "- This candidate does not accept predictive usefulness, profitability, or runtime use.",
        "",
        "## Source Predictive Experiment Results",
        f"- Results review package digest: `{candidate['source_results_review_package_digest']}`",
        f"- Execution digest: `{candidate['predictive_experiment_execution_digest']}`",
        f"- Approval digest: `{candidate['predictive_experiment_execution_approval_digest']}`",
        f"- Execution request ID: `{candidate['predictive_experiment_execution_request_id']}`",
        "",
        "## Assessment Classification",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in classification.items())
    lines.extend(
        [
            "",
            "## Evidence Summary",
            f"- Output count: `{facts['output_count']}`",
            f"- All outputs research-only non-actionable: `{facts['all_outputs_research_only_non_actionable']}`",
            f"- Metrics label: `{facts['metrics_label']}`",
            f"- Labels generated: `{facts['labels_generated']}`",
            f"- Feature matrices generated: `{facts['feature_matrices_generated']}`",
            f"- Walk-forward result generated: `{facts['walk_forward_result_generated']}`",
            f"- Out-of-sample result generated: `{facts['out_of_sample_result_generated']}`",
            f"- Baseline result count: `{facts['baseline_result_count']}`",
            f"- Metric result count: `{facts['metric_result_count']}`",
            f"- Failure count status: `{facts['failure_count_status']}`",
            f"- Warning count status: `{facts['warning_count_status']}`",
            "",
            "## Limitations",
        ]
    )
    lines.extend(f"- `{item}`" for item in candidate["assessment_limitations"])
    lines.extend(["", "## Additional Evidence / Next Gates"])
    lines.extend(f"- `{item}`" for item in candidate["additional_evidence_next_gates"])
    lines.extend(
        [
            "",
            "## Predictive/Profitability Boundary",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- predictive_usefulness_acceptance_ready: `{candidate['predictive_usefulness_acceptance_ready']}`",
            f"- predictive_usefulness_acceptance_recommended: `{candidate['predictive_usefulness_acceptance_recommended']}`",
            f"- profitability: `{candidate['profitability']}`",
            f"- profitability_acceptance_ready: `{candidate['profitability_acceptance_ready']}`",
            f"- profitability_acceptance_recommended: `{candidate['profitability_acceptance_recommended']}`",
            "",
            "## Runtime Boundary",
            f"- provider_requests_made: `{candidate['provider_requests_made']}`",
            f"- experiment_reexecution_performed: `{candidate['experiment_reexecution_performed']}`",
            f"- walk_forward_rerun_performed: `{candidate['walk_forward_rerun_performed']}`",
            f"- label_regeneration_performed: `{candidate['label_regeneration_performed']}`",
            f"- feature_matrix_regeneration_performed: `{candidate['feature_matrix_regeneration_performed']}`",
            f"- new_strategy_scoring_performed: `{candidate['new_strategy_scoring_performed']}`",
            f"- trade_recommendations_generated: `{candidate['trade_recommendations_generated']}`",
            f"- runtime_migration_recommended: `{candidate['runtime_migration_recommended']}`",
            f"- runtime_migration_approved: `{candidate['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{candidate['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{candidate['strategy_runtime_migration']}`",
            f"- runtime_use: `{candidate['runtime_use']}`",
            f"- strategy_use: `{candidate['strategy_use']}`",
            f"- paper_trading: `{candidate['paper_trading']}`",
            f"- broker_execution: `{candidate['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Candidate digest: `{validation['predictive_usefulness_assessment_candidate_digest']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No predictive experiment, walk-forward, label, or feature-matrix rerun occurred.",
            "- No strategy scoring or trade recommendations were generated.",
            "- No runtime migration, paper trading, or broker execution was authorized.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_assessment_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the assessment candidate JSON artifact without overwriting output."""
    candidate = build_predictive_usefulness_assessment_candidate_v1()
    validation = validate_predictive_usefulness_assessment_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_usefulness_assessment_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessAssessmentCandidateError(
            "predictive usefulness assessment candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessAssessmentCandidateError(
            "predictive usefulness assessment candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
