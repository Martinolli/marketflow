"""Offline operator review package for the predictive experiment plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_experiment_plan_candidate_service as plan_service


ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE = (
    "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_V1 = (
    "predictive_experiment_plan_candidate_review_v1"
)
PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
)
PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_STATUS_BINDING = (
    "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_STATUS_BINDING"
)
PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_OBJECT_BINDING = (
    "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_DIGEST = (
    "2d338822163dd25f262a32940153ff9842bb7e3213372ad09ce705bbfddede71"
)

NOT_AUTHORIZED = plan_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REMAINING_TASKS = [
    "Predictive experiment execution candidate.",
    "Predictive experiment execution approval ceremony.",
    "Predictive experiment execution.",
    "Predictive usefulness review after experiment results.",
]

REQUIRED_CHECK_IDS = [
    "predictive_experiment_plan_kind_matches",
    "predictive_experiment_plan_status_ready_for_review",
    "predictive_experiment_plan_digest_matches",
    "predictive_experiment_plan_checklist_zero_blockers",
    "predictive_usefulness_review_candidate_digest_bound",
    "predictive_usefulness_review_candidate_review_digest_bound",
    "campaign_results_review_digest_bound",
    "campaign_execution_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "experiment_scope_research_only",
    "ticker_universe_aapl_only",
    "profiles_swing_and_position_swing",
    "date_range_matches",
    "label_definitions_defined",
    "feature_family_plan_defined",
    "walk_forward_plan_defined",
    "out_of_sample_plan_defined",
    "baseline_comparisons_defined",
    "signal_quality_metrics_defined",
    "stability_checks_defined",
    "false_positive_false_negative_analysis_defined",
    "leakage_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "execution_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_in_review_false",
    "predictive_experiment_execution_authorized_false",
    "predictive_experiment_executed_false",
    "walk_forward_validation_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
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


class PredictiveExperimentPlanCandidateReviewPackageError(ValueError):
    """Raised when the predictive experiment plan review package is invalid."""


def _check(check_id: str, expected: Any, actual: Any, *, severity: str = BLOCKER) -> dict[str, Any]:
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
        raise PredictiveExperimentPlanCandidateReviewPackageError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveExperimentPlanCandidateReviewPackageError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveExperimentPlanCandidateReviewPackageError(f"{field_name} must be false")


def _plan_for_binding(plan: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if plan is None:
        return (
            plan_service.build_predictive_experiment_plan_candidate_v1(),
            PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_STATUS_BINDING,
        )
    plan_service.validate_predictive_experiment_plan_candidate_v1(plan)
    return plan, PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_OBJECT_BINDING


def _profiles(review_package: dict[str, Any]) -> list[str]:
    profiles = review_package.get("dataset_profiles")
    if not isinstance(profiles, list):
        return []
    return [item.get("profile") for item in profiles if isinstance(item, dict)]


def _planned_outputs_not_generated(review_package: dict[str, Any]) -> bool:
    outputs = review_package.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(item, dict)
        and item.get("generation_status") == plan_service.PLANNED_NOT_GENERATED
        for item in outputs
    )


def _planned_outputs_research_only(review_package: dict[str, Any]) -> bool:
    outputs = review_package.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(item, dict)
        and item.get("output_label") == plan_service.RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def _base_review_package(plan: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = plan["plan_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_V1,
        "review_status": PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "plan_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "predictive_experiment_execution_authorized": False,
        "predictive_experiment_executed": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "profitability": plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
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
        "reviewed_plan_kind": plan["artifact_kind"],
        "reviewed_plan_status": plan["plan_status"],
        "reviewed_plan_digest": plan["predictive_experiment_plan_candidate_digest"],
        "reviewed_plan_checklist_total": summary["total_checks"],
        "reviewed_plan_checklist_passed": summary["passed_checks"],
        "reviewed_plan_checklist_failed": summary["failed_checks"],
        "reviewed_plan_blocker_count": summary["blocker_count"],
        "predictive_usefulness_review_candidate_digest": plan[
            "predictive_usefulness_review_candidate_digest"
        ],
        "predictive_usefulness_review_candidate_review_package_digest": plan[
            "predictive_usefulness_review_candidate_review_package_digest"
        ],
        "campaign_execution_results_review_package_digest": plan[
            "campaign_execution_results_review_package_digest"
        ],
        "campaign_execution_digest": plan["campaign_execution_digest"],
        "execution_request_id": plan["execution_request_id"],
        "swing_registry_approval_digest": plan["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": plan[
            "position_swing_registry_approval_digest"
        ],
        "experiment_scope": "RESEARCH_ONLY",
        "ticker_universe": list(plan["ticker_universe"]),
        "dataset_profiles": deepcopy(plan["dataset_profiles"]),
        "date_range_start": plan["date_range"]["start"],
        "date_range_end": plan["date_range"]["end"],
        "label_definitions": deepcopy(plan["label_definitions"]),
        "feature_family_plan": deepcopy(plan["feature_family_plan"]),
        "walk_forward_plan": deepcopy(plan["walk_forward_plan"]),
        "out_of_sample_plan": deepcopy(plan["out_of_sample_plan"]),
        "baseline_comparisons": list(plan["baseline_comparisons"]),
        "signal_quality_metrics": deepcopy(plan["signal_quality_metrics"]),
        "stability_checks": list(plan["stability_checks"]),
        "false_positive_false_negative_analysis": deepcopy(
            plan["false_positive_false_negative_analysis"]
        ),
        "leakage_controls": list(plan["leakage_controls"]),
        "planned_outputs": deepcopy(plan["planned_outputs"]),
        "execution_gates": list(plan["execution_gates"]),
        "risk_controls": list(plan["risk_controls"]),
        "remaining_tasks": list(REMAINING_TASKS),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("predictive_experiment_plan_kind_matches", plan_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE, review_package.get("reviewed_plan_kind")),
        _check("predictive_experiment_plan_status_ready_for_review", plan_service.PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_plan_status")),
        _check("predictive_experiment_plan_digest_matches", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_DIGEST, review_package.get("reviewed_plan_digest")),
        _check("predictive_experiment_plan_checklist_zero_blockers", 0, review_package.get("reviewed_plan_blocker_count")),
        _check("predictive_usefulness_review_candidate_digest_bound", plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST, review_package.get("predictive_usefulness_review_candidate_digest")),
        _check("predictive_usefulness_review_candidate_review_digest_bound", plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_usefulness_review_candidate_review_package_digest")),
        _check("campaign_results_review_digest_bound", plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("campaign_execution_results_review_package_digest")),
        _check("campaign_execution_digest_bound", plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST, review_package.get("campaign_execution_digest")),
        _check("swing_registry_approval_digest_bound", plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("position_swing_registry_approval_digest")),
        _check("experiment_scope_research_only", "RESEARCH_ONLY", review_package.get("experiment_scope")),
        _check("ticker_universe_aapl_only", ["AAPL"], review_package.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["SWING", "POSITION_SWING"], _profiles(review_package)),
        _check("date_range_matches", {"start": "2022-01-01", "end": "2025-12-31"}, {"start": review_package.get("date_range_start"), "end": review_package.get("date_range_end")}),
        _check("label_definitions_defined", plan_service.LABEL_DEFINITIONS, [item.get("label") for item in review_package.get("label_definitions", []) if isinstance(item, dict)]),
        _check("feature_family_plan_defined", plan_service.FEATURE_FAMILIES, [item.get("feature_family") for item in review_package.get("feature_family_plan", []) if isinstance(item, dict)]),
        _check("walk_forward_plan_defined", True, isinstance(review_package.get("walk_forward_plan"), dict) and bool(review_package.get("walk_forward_plan"))),
        _check("out_of_sample_plan_defined", True, isinstance(review_package.get("out_of_sample_plan"), dict) and bool(review_package.get("out_of_sample_plan"))),
        _check("baseline_comparisons_defined", plan_service.BASELINE_COMPARISONS, review_package.get("baseline_comparisons")),
        _check("signal_quality_metrics_defined", plan_service.SIGNAL_QUALITY_METRICS, [item.get("metric") for item in review_package.get("signal_quality_metrics", []) if isinstance(item, dict)]),
        _check("stability_checks_defined", plan_service.STABILITY_CHECKS, review_package.get("stability_checks")),
        _check("false_positive_false_negative_analysis_defined", True, isinstance(review_package.get("false_positive_false_negative_analysis"), dict) and bool(review_package.get("false_positive_false_negative_analysis"))),
        _check("leakage_controls_defined", plan_service.LEAKAGE_CONTROLS, review_package.get("leakage_controls")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(review_package)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(review_package)),
        _check("execution_gates_defined", plan_service.EXECUTION_GATES, review_package.get("execution_gates")),
        _check("risk_controls_defined", plan_service.RISK_CONTROLS, review_package.get("risk_controls")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("predictive_experiment_execution_authorized_false", False, review_package.get("predictive_experiment_execution_authorized")),
        _check("predictive_experiment_executed_false", False, review_package.get("predictive_experiment_executed")),
        _check("walk_forward_validation_performed_false", False, review_package.get("walk_forward_validation_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, review_package.get("profitability_acceptance_ready")),
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
        "ready_for_predictive_experiment_execution_candidate": ready,
        "predictive_experiment_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_experiment_plan_candidate_review_package_digest", None)
    return payload


def predictive_experiment_plan_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the plan review package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_experiment_plan_candidate_review_package_v1(
    plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for a predictive experiment plan."""
    bound_plan, binding_mode = _plan_for_binding(plan)
    review_package = _base_review_package(bound_plan, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["predictive_experiment_plan_candidate_review_package_digest"] = (
        predictive_experiment_plan_candidate_review_package_digest_v1(review_package)
    )
    validate_predictive_experiment_plan_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "PREDICTIVE_EXPERIMENT_EXECUTED",
            "WALK_FORWARD_VALIDATION_EXECUTED",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise PredictiveExperimentPlanCandidateReviewPackageError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made_in_review",
            "predictive_experiment_execution_authorized",
            "predictive_experiment_executed",
            "walk_forward_validation_performed",
            "out_of_sample_evaluation_performed",
            "new_strategy_scoring_performed",
            "trade_recommendations_generated",
            "predictive_usefulness_acceptance_ready",
            "profitability_acceptance_ready",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise PredictiveExperimentPlanCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise PredictiveExperimentPlanCandidateReviewPackageError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveExperimentPlanCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_experiment_plan_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a plan review package without authorizing experiment execution."""
    if not isinstance(review_package, dict):
        raise PredictiveExperimentPlanCandidateReviewPackageError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("plan_binding_mode") not in {
        PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_STATUS_BINDING,
        PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_OBJECT_BINDING,
    }:
        raise PredictiveExperimentPlanCandidateReviewPackageError("plan_binding_mode mismatch")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_true(review_package.get("created_offline"), "created_offline")
    for field in (
        "provider_requests_made_in_review",
        "predictive_experiment_execution_authorized",
        "predictive_experiment_executed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
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
    for field, expected in {
        "predictive_usefulness": plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_plan_kind": plan_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE,
        "reviewed_plan_status": plan_service.PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW,
        "reviewed_plan_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_DIGEST,
        "reviewed_plan_checklist_total": len(plan_service.REQUIRED_CHECK_IDS),
        "reviewed_plan_checklist_passed": len(plan_service.REQUIRED_CHECK_IDS),
        "reviewed_plan_checklist_failed": 0,
        "reviewed_plan_blocker_count": 0,
        "predictive_usefulness_review_candidate_digest": plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST,
        "predictive_usefulness_review_candidate_review_package_digest": plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "campaign_execution_results_review_package_digest": plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "campaign_execution_digest": plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "execution_request_id": plan_service.EXPECTED_EXECUTION_REQUEST_ID,
        "swing_registry_approval_digest": plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "experiment_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
    }.items():
        _expect(review_package.get(field), expected, field)
    _expect(_profiles(review_package), ["SWING", "POSITION_SWING"], "dataset_profiles")
    if [item.get("label") for item in review_package.get("label_definitions", []) if isinstance(item, dict)] != plan_service.LABEL_DEFINITIONS:
        raise PredictiveExperimentPlanCandidateReviewPackageError("label_definitions mismatch")
    if [item.get("feature_family") for item in review_package.get("feature_family_plan", []) if isinstance(item, dict)] != plan_service.FEATURE_FAMILIES:
        raise PredictiveExperimentPlanCandidateReviewPackageError("feature_family_plan mismatch")
    if not isinstance(review_package.get("walk_forward_plan"), dict) or not review_package["walk_forward_plan"]:
        raise PredictiveExperimentPlanCandidateReviewPackageError("walk_forward_plan missing")
    if not isinstance(review_package.get("out_of_sample_plan"), dict) or not review_package["out_of_sample_plan"]:
        raise PredictiveExperimentPlanCandidateReviewPackageError("out_of_sample_plan missing")
    _expect(review_package.get("baseline_comparisons"), plan_service.BASELINE_COMPARISONS, "baseline_comparisons")
    _expect([item.get("metric") for item in review_package.get("signal_quality_metrics", []) if isinstance(item, dict)], plan_service.SIGNAL_QUALITY_METRICS, "signal_quality_metrics")
    _expect(review_package.get("stability_checks"), plan_service.STABILITY_CHECKS, "stability_checks")
    if not isinstance(review_package.get("false_positive_false_negative_analysis"), dict) or not review_package["false_positive_false_negative_analysis"]:
        raise PredictiveExperimentPlanCandidateReviewPackageError("false_positive_false_negative_analysis missing")
    _expect(review_package.get("leakage_controls"), plan_service.LEAKAGE_CONTROLS, "leakage_controls")
    _expect_true(_planned_outputs_not_generated(review_package), "planned_outputs_not_generated")
    _expect_true(_planned_outputs_research_only(review_package), "planned_outputs_research_only")
    _expect(review_package.get("execution_gates"), plan_service.EXECUTION_GATES, "execution_gates")
    _expect(review_package.get("risk_controls"), plan_service.RISK_CONTROLS, "risk_controls")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveExperimentPlanCandidateReviewPackageError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveExperimentPlanCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("predictive_experiment_plan_candidate_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveExperimentPlanCandidateReviewPackageError(
            "predictive_experiment_plan_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        predictive_experiment_plan_candidate_review_package_digest_v1(review_package),
        "predictive_experiment_plan_candidate_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_experiment_plan_candidate_review_package_digest": digest,
        "reviewed_plan_digest": review_package["reviewed_plan_digest"],
        "predictive_usefulness_review_candidate_digest": review_package[
            "predictive_usefulness_review_candidate_digest"
        ],
        "predictive_usefulness_review_candidate_review_package_digest": review_package[
            "predictive_usefulness_review_candidate_review_package_digest"
        ],
        "campaign_execution_results_review_package_digest": review_package[
            "campaign_execution_results_review_package_digest"
        ],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
        "ready_for_predictive_experiment_execution_candidate": review_package["review_summary"][
            "ready_for_predictive_experiment_execution_candidate"
        ],
        "predictive_experiment_execution_authorized": False,
        "predictive_usefulness": plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_experiment_plan_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized predictive experiment plan review package summary."""
    validation = validate_predictive_experiment_plan_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Predictive Experiment Plan Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Predictive Experiment Plan Candidate Operator Review Package v1.",
        "",
        "## Reviewed Predictive Experiment Plan",
        f"- Plan digest: `{review_package['reviewed_plan_digest']}`",
        f"- Review package digest: `{validation['predictive_experiment_plan_candidate_review_package_digest']}`",
        "",
        "## Source Evidence",
        f"- Predictive usefulness candidate digest: `{review_package['predictive_usefulness_review_candidate_digest']}`",
        f"- Predictive usefulness candidate review digest: `{review_package['predictive_usefulness_review_candidate_review_package_digest']}`",
        f"- Campaign results review digest: `{review_package['campaign_execution_results_review_package_digest']}`",
        "",
        "## Experiment Scope",
        f"- Ticker universe: `{', '.join(review_package['ticker_universe'])}`",
        f"- Date range: `{review_package['date_range_start']} through {review_package['date_range_end']}`",
        "",
        "## Labels and Features",
    ]
    lines.extend(f"- Label: `{item['label']}`" for item in review_package["label_definitions"])
    lines.extend(f"- Feature family: `{item['feature_family']}`" for item in review_package["feature_family_plan"])
    lines.extend(
        [
            "",
            "## Walk-Forward / OOS Design",
            f"- Walk-forward type: `{review_package['walk_forward_plan']['method']}`",
            f"- No shuffle: `{review_package['walk_forward_plan']['no_shuffle']}`",
            f"- Final holdout: `{review_package['out_of_sample_plan']['final_holdout_period']}`",
            "",
            "## Baselines and Metrics",
        ]
    )
    lines.extend(f"- Baseline: `{item}`" for item in review_package["baseline_comparisons"])
    lines.extend(f"- Metric: `{item['metric']}`" for item in review_package["signal_quality_metrics"])
    lines.extend(["", "## Leakage Controls"])
    lines.extend(f"- `{item}`" for item in review_package["leakage_controls"])
    lines.extend(["", "## Execution Gates"])
    lines.extend(f"- `{item}`" for item in review_package["execution_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Boundary Conditions",
            f"- predictive_experiment_execution_authorized: `{review_package['predictive_experiment_execution_authorized']}`",
            f"- predictive_experiment_executed: `{review_package['predictive_experiment_executed']}`",
            f"- walk_forward_validation_performed: `{review_package['walk_forward_validation_performed']}`",
            f"- trade_recommendations_generated: `{review_package['trade_recommendations_generated']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            f"- runtime_use: `{review_package['runtime_use']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Remaining Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(review_package["remaining_tasks"], start=1))
    lines.append("")
    return "\n".join(lines)


def write_predictive_experiment_plan_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    plan: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the predictive experiment plan review package without overwriting output."""
    review_package = build_predictive_experiment_plan_candidate_review_package_v1(plan=plan)
    validation = validate_predictive_experiment_plan_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_experiment_plan_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveExperimentPlanCandidateReviewPackageError(
            "predictive experiment plan review package filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveExperimentPlanCandidateReviewPackageError(
            "predictive experiment plan review package output already exists"
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
