"""Offline predictive usefulness acceptance readiness candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    predictive_usefulness_assessment_candidate_operator_review_service as assessment_review,
)


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_V1 = (
    "predictive_usefulness_acceptance_readiness_candidate_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE"
)

ACCEPTANCE_READINESS_STATE_NOT_READY = "NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE"
ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED = (
    "CURRENT_EVIDENCE_IS_RESEARCH_ONLY_AND_LIMITED"
)

EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "b73bcd2f6004a457112688cfa8ff487b266a1b74ea3135d2be7f68c1fb3aadd5"
)
EXPECTED_ASSESSMENT_CANDIDATE_DIGEST = (
    assessment_review.EXPECTED_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    assessment_review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    assessment_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    assessment_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID = (
    assessment_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    assessment_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    assessment_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = assessment_review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    assessment_review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

NOT_AUTHORIZED = assessment_review.NOT_AUTHORIZED
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = (
    assessment_review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NOT_READY_REASONS = [
    "single_ticker_scope",
    "single_asset_class_scope_if_applicable",
    "simplified_chronological_split",
    "failure_warning_counts_unavailable",
    "metrics_marked_not_acceptance_evidence",
    "no_runtime_strategy_validation",
    "no_transaction_cost_model",
    "no_slippage_model",
    "no_live_or_paper_trading_validation",
    "no_profitability_acceptance",
    "no_multi_ticker_or_out_of_domain_generalization",
    "operator_acceptance_ceremony_required",
]

ADDITIONAL_EVIDENCE_REQUIRED = [
    "multi_ticker_research_replication_or_operator_accepted_single_ticker_scope",
    "expanded_out_of_sample_validation",
    "documented_failure_warning_counts",
    "stronger_walk_forward_protocol_or_operator_accepted_simplified_split",
    "signal_stability_across_time_slices",
    "baseline_comparison_interpretation",
    "metric_thresholds_defined_before_review",
    "transaction_cost_and_slippage_model_if_profitability_will_be_reviewed",
    "explicit_non_runtime_acceptance_boundary",
    "operator_decision_to_create_acceptance_candidate",
]

NEXT_GATES = [
    "predictive_usefulness_acceptance_readiness_operator_review",
    "additional_predictive_evidence_plan_candidate",
    "predictive_usefulness_acceptance_candidate_only_if_operator_approves",
    "predictive_usefulness_acceptance_ceremony_if_candidate_is_approved",
    "profitability_review_candidate_separate",
    "runtime_migration_approval_ceremony_separate_if_ever_authorized",
]

REQUIRED_CHECK_IDS = [
    "assessment_candidate_review_digest_bound",
    "assessment_candidate_digest_bound",
    "predictive_experiment_results_review_digest_bound",
    "predictive_experiment_execution_digest_bound",
    "predictive_experiment_execution_approval_digest_bound",
    "predictive_experiment_plan_digest_bound",
    "predictive_experiment_plan_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "output_count_13",
    "outputs_research_only_non_actionable",
    "metrics_label_not_acceptance_evidence",
    "labels_generated_true",
    "feature_matrices_generated_true",
    "walk_forward_result_available",
    "out_of_sample_result_available",
    "baseline_results_available",
    "metric_results_available",
    "failure_warning_counts_unavailable_acknowledged",
    "acceptance_readiness_state_not_ready",
    "predictive_evidence_available_for_review_true",
    "predictive_evidence_sufficient_for_acceptance_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
    "predictive_usefulness_acceptance_candidate_created_false",
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
    "provider_requests_made_false",
    "experiment_reexecution_performed_false",
    "walk_forward_rerun_performed_false",
    "label_regeneration_performed_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "additional_evidence_required_defined",
    "next_gates_defined",
]


class PredictiveUsefulnessAcceptanceReadinessCandidateError(ValueError):
    """Raised when the predictive usefulness acceptance readiness candidate is invalid."""


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
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_V1,
        "candidate_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE,
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
        "operator_review_required": True,
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
        "failure_count_status": assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
        "warning_count_status": assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
        "acceptance_readiness_state": ACCEPTANCE_READINESS_STATE_NOT_READY,
        "acceptance_readiness_reason": ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED,
        "predictive_evidence_available_for_review": True,
        "predictive_evidence_sufficient_for_acceptance": False,
        "acceptance_not_ready_reasons": list(NOT_READY_REASONS),
        "additional_evidence_required": list(ADDITIONAL_EVIDENCE_REQUIRED),
        "next_gates": list(NEXT_GATES),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("assessment_candidate_review_digest_bound", EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_usefulness_assessment_candidate_review_package_digest")),
        _check("assessment_candidate_digest_bound", EXPECTED_ASSESSMENT_CANDIDATE_DIGEST, candidate.get("predictive_usefulness_assessment_candidate_digest")),
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_experiment_results_review_package_digest")),
        _check("predictive_experiment_execution_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST, candidate.get("predictive_experiment_execution_digest")),
        _check("predictive_experiment_execution_approval_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST, candidate.get("predictive_experiment_execution_approval_digest")),
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, candidate.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_experiment_plan_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("position_swing_registry_approval_digest")),
        _check("output_count_13", 13, candidate.get("output_count")),
        _check("outputs_research_only_non_actionable", True, candidate.get("all_outputs_research_only_non_actionable")),
        _check("metrics_label_not_acceptance_evidence", RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE, candidate.get("metrics_label")),
        _check("labels_generated_true", True, candidate.get("labels_generated")),
        _check("feature_matrices_generated_true", True, candidate.get("feature_matrices_generated")),
        _check("walk_forward_result_available", True, candidate.get("walk_forward_result_generated")),
        _check("out_of_sample_result_available", True, candidate.get("out_of_sample_result_generated")),
        _check("baseline_results_available", 8, candidate.get("baseline_result_count")),
        _check("metric_results_available", 8, candidate.get("metric_result_count")),
        _check("failure_warning_counts_unavailable_acknowledged", [assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS, assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS], [candidate.get("failure_count_status"), candidate.get("warning_count_status")]),
        _check("acceptance_readiness_state_not_ready", ACCEPTANCE_READINESS_STATE_NOT_READY, candidate.get("acceptance_readiness_state")),
        _check("predictive_evidence_available_for_review_true", True, candidate.get("predictive_evidence_available_for_review")),
        _check("predictive_evidence_sufficient_for_acceptance_false", False, candidate.get("predictive_evidence_sufficient_for_acceptance")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, candidate.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, candidate.get("predictive_usefulness_acceptance_candidate_created")),
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
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("experiment_reexecution_performed_false", False, candidate.get("experiment_reexecution_performed")),
        _check("walk_forward_rerun_performed_false", False, candidate.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, candidate.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, candidate.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check("additional_evidence_required_defined", ADDITIONAL_EVIDENCE_REQUIRED, candidate.get("additional_evidence_required")),
        _check("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
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
        "ready_for_operator_review": failed == 0,
        "ready_for_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("predictive_usefulness_acceptance_readiness_candidate_digest", None)
    return payload


def predictive_usefulness_acceptance_readiness_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the readiness candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_predictive_usefulness_acceptance_readiness_candidate_v1() -> dict[str, Any]:
    """Build an offline readiness candidate that does not accept predictive usefulness."""
    candidate = _base_candidate()
    candidate["readiness_checklist"] = _checklist(candidate)
    candidate["readiness_summary"] = _summary(candidate["readiness_checklist"])
    candidate["predictive_usefulness_acceptance_readiness_candidate_digest"] = (
        predictive_usefulness_acceptance_readiness_candidate_digest_v1(candidate)
    )
    validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
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
            raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
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
            "predictive_usefulness_acceptance_candidate_created",
            "profitability_acceptance_ready",
            "profitability_acceptance_recommended",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
            "predictive_evidence_sufficient_for_acceptance",
        } and value is True:
            raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_usefulness_acceptance_readiness_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate a readiness candidate without granting acceptance or runtime use."""
    if not isinstance(candidate, dict):
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE,
        "candidate_status",
    )
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "predictive_usefulness_acceptance_ceremony_required",
        "predictive_evidence_available_for_review",
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
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_evidence_sufficient_for_acceptance",
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
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
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
        "failure_count_status": assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
        "warning_count_status": assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS,
        "acceptance_readiness_state": ACCEPTANCE_READINESS_STATE_NOT_READY,
        "acceptance_readiness_reason": ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED,
    }.items():
        _expect(candidate.get(field), expected, field)
    _expect(
        candidate.get("acceptance_not_ready_reasons"),
        NOT_READY_REASONS,
        "acceptance_not_ready_reasons",
    )
    _expect(
        candidate.get("additional_evidence_required"),
        ADDITIONAL_EVIDENCE_REQUIRED,
        "additional_evidence_required",
    )
    _expect(candidate.get("next_gates"), NEXT_GATES, "next_gates")
    checklist = candidate.get("readiness_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            "readiness_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "readiness_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            f"readiness checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "readiness_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("readiness_summary"), expected_summary, "readiness_summary")
    digest = candidate.get("predictive_usefulness_acceptance_readiness_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            "predictive_usefulness_acceptance_readiness_candidate_digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_acceptance_readiness_candidate_digest_v1(candidate),
        "predictive_usefulness_acceptance_readiness_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "predictive_usefulness_acceptance_readiness_candidate_digest": digest,
        "predictive_usefulness_assessment_candidate_review_package_digest": candidate[
            "predictive_usefulness_assessment_candidate_review_package_digest"
        ],
        "predictive_usefulness_assessment_candidate_digest": candidate[
            "predictive_usefulness_assessment_candidate_digest"
        ],
        "acceptance_readiness_state": candidate["acceptance_readiness_state"],
        "ready_for_operator_review": candidate["readiness_summary"]["ready_for_operator_review"],
        "ready_for_acceptance_candidate": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_predictive_usefulness_acceptance_readiness_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized predictive usefulness acceptance readiness summary."""
    validation = validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)
    summary = candidate["readiness_summary"]
    lines = [
        "# MarketFlow Predictive Usefulness Acceptance Readiness Candidate Status",
        "",
        "## Title",
        "- Predictive Usefulness Acceptance Readiness Candidate v1.",
        "",
        "## Purpose",
        "- Classify whether reviewed research evidence is ready for a future predictive usefulness acceptance candidate.",
        "- Current evidence is not sufficient for acceptance.",
        "",
        "## Source Assessment Evidence",
        f"- Assessment candidate review package digest: `{candidate['predictive_usefulness_assessment_candidate_review_package_digest']}`",
        f"- Assessment candidate digest: `{candidate['predictive_usefulness_assessment_candidate_digest']}`",
        f"- Predictive experiment results review digest: `{candidate['predictive_experiment_results_review_package_digest']}`",
        f"- Predictive experiment execution digest: `{candidate['predictive_experiment_execution_digest']}`",
        "",
        "## Readiness Classification",
        f"- acceptance_readiness_state: `{candidate['acceptance_readiness_state']}`",
        f"- acceptance_readiness_reason: `{candidate['acceptance_readiness_reason']}`",
        f"- predictive_evidence_available_for_review: `{candidate['predictive_evidence_available_for_review']}`",
        f"- predictive_evidence_sufficient_for_acceptance: `{candidate['predictive_evidence_sufficient_for_acceptance']}`",
        f"- Candidate digest: `{validation['predictive_usefulness_acceptance_readiness_candidate_digest']}`",
        "",
        "## Reasons Acceptance Is Not Ready",
    ]
    lines.extend(f"- `{item}`" for item in candidate["acceptance_not_ready_reasons"])
    lines.extend(["", "## Additional Evidence Required"])
    lines.extend(f"- `{item}`" for item in candidate["additional_evidence_required"])
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in candidate["next_gates"])
    lines.extend(
        [
            "",
            "## Predictive/Profitability Boundary",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- predictive_usefulness_acceptance_ready: `{candidate['predictive_usefulness_acceptance_ready']}`",
            f"- predictive_usefulness_acceptance_recommended: `{candidate['predictive_usefulness_acceptance_recommended']}`",
            f"- predictive_usefulness_acceptance_candidate_created: `{candidate['predictive_usefulness_acceptance_candidate_created']}`",
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


def write_predictive_usefulness_acceptance_readiness_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the readiness candidate JSON artifact without overwriting output."""
    candidate = build_predictive_usefulness_acceptance_readiness_candidate_v1()
    validation = validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_usefulness_acceptance_readiness_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            "predictive usefulness acceptance readiness filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessAcceptanceReadinessCandidateError(
            "predictive usefulness acceptance readiness output already exists"
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
