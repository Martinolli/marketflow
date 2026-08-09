"""Offline predictive experiment plan candidate for future research-only experiments."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import predictive_usefulness_review_candidate_operator_review_service as review_service


ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE = (
    "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_V1 = (
    "predictive_experiment_plan_candidate_v1"
)
PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW = (
    "PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST = (
    review_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "f124ee8e7e6b72f9d8f5f2a495bb0afa09ef02e4d8a6a03e795a04de4276efe2"
)
EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST = (
    review_service.candidate_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CAMPAIGN_EXECUTION_DIGEST = (
    review_service.candidate_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST
)
EXPECTED_EXECUTION_REQUEST_ID = review_service.candidate_service.EXPECTED_EXECUTION_REQUEST_ID
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_SWING_REGISTRY_KEY = (
    "AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1"
)
EXPECTED_POSITION_SWING_REGISTRY_KEY = (
    "AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1"
)

NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = "RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE"

LABEL_DEFINITIONS = [
    "SWING_NEXT_BAR_DIRECTION",
    "SWING_NEXT_BAR_RETURN_BUCKET",
    "POSITION_SWING_NEXT_SESSION_DIRECTION",
    "POSITION_SWING_NEXT_SESSION_RETURN_BUCKET",
]
FEATURE_FAMILIES = [
    "price_return_features",
    "range_volatility_features",
    "volume_context_features",
    "rolling_mean_features",
    "rolling_zscore_features",
    "bar_position_features",
]
BASELINE_COMPARISONS = [
    "majority_class_baseline",
    "zero_return_baseline",
    "naive_persistence_baseline",
    "random_baseline_seeded",
]
SIGNAL_QUALITY_METRICS = [
    "directional_accuracy",
    "balanced_accuracy",
    "precision_recall",
    "roc_auc_if_applicable",
    "information_coefficient_if_applicable",
    "calibration_summary",
    "confusion_matrix",
    "lift_over_baseline",
]
STABILITY_CHECKS = [
    "time_slice_stability",
    "profile_comparison_stability",
    "feature_missingness_stability",
    "metric_confidence_interval_plan",
]
LEAKAGE_CONTROLS = [
    "label_forward_only",
    "no_future_features",
    "split_by_time",
    "no_random_shuffle",
    "embargo_or_gap_if_required",
    "dataset_digest_lock",
]
PLANNED_OUTPUT_NAMES = [
    "predictive_experiment_run_manifest",
    "label_definition_report",
    "feature_family_report",
    "walk_forward_plan_report",
    "out_of_sample_plan_report",
    "baseline_comparison_report",
    "signal_quality_metrics_report",
    "stability_analysis_report",
    "false_positive_false_negative_report",
    "operator_review_summary",
]
EXECUTION_GATES = [
    "predictive_experiment_plan_operator_review",
    "predictive_experiment_execution_approval",
    "dataset_digest_reverification",
    "label_definition_operator_acceptance",
    "leakage_control_review",
    "walk_forward_configuration_review",
    "no_broker_execution_confirmation",
    "no_paper_trading_confirmation",
    "no_runtime_default_change_confirmation",
    "output_labeling_research_only_confirmation",
]
RISK_CONTROLS = [
    "no provider refresh",
    "no broker execution",
    "no paper trading",
    "no runtime source switch",
    "no automatic stitching",
    "no trade recommendations",
    "no predictive usefulness acceptance in experiment execution",
    "no profitability acceptance in experiment execution",
    "all outputs labeled research-only",
    "operator approval required before experiment execution",
]
NON_GOALS = [
    "Execute predictive experiments.",
    "Run walk-forward validation.",
    "Run strategy scoring.",
    "Generate trade recommendations.",
    "Accept predictive usefulness or profitability.",
    "Authorize runtime migration, paper trading, or broker execution.",
]

REQUIRED_CHECK_IDS = [
    "predictive_review_candidate_digest_bound",
    "predictive_review_candidate_review_digest_bound",
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
    "provider_requests_made_false",
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


class PredictiveExperimentPlanCandidateError(ValueError):
    """Raised when a predictive experiment plan candidate violates guardrails."""


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
        raise PredictiveExperimentPlanCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveExperimentPlanCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveExperimentPlanCandidateError(f"{field_name} must be false")


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "name": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _base_plan() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_V1,
        "plan_status": PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "predictive_experiment_execution_authorized": False,
        "predictive_experiment_executed": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_performed": False,
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
        "experiment_execution_requires_operator_approval": True,
        "predictive_usefulness_review_candidate_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_review_candidate_review_package_digest": (
            EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_execution_results_review_package_digest": (
            EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_execution_digest": EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "execution_request_id": EXPECTED_EXECUTION_REQUEST_ID,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "swing_registry_key": EXPECTED_SWING_REGISTRY_KEY,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "position_swing_registry_key": EXPECTED_POSITION_SWING_REGISTRY_KEY,
        "data_quality_readiness": True,
        "module_compatibility_readiness": True,
        "outputs_reviewed": 12,
        "failure_count": 0,
        "warning_count": 0,
        "experiment_name": "AAPL_SWING_POSITION_SWING_PREDICTIVE_EXPERIMENT_PLAN_V1",
        "experiment_scope": {
            "ticker": "AAPL",
            "registry_scope": "RESEARCH_DATASET",
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "research_only": True,
        },
        "dataset_profiles": [
            {
                "profile": "SWING",
                "timeframe": "RTH_HALF_SESSION_195M",
                "registry_key": EXPECTED_SWING_REGISTRY_KEY,
            },
            {
                "profile": "POSITION_SWING",
                "timeframe": "RTH_FULL_SESSION_1D",
                "registry_key": EXPECTED_POSITION_SWING_REGISTRY_KEY,
            },
        ],
        "ticker_universe": ["AAPL"],
        "date_range": {"start": "2022-01-01", "end": "2025-12-31"},
        "label_definitions": [
            {"label": label, "status": "PLANNED_ONLY", "calculated": False}
            for label in LABEL_DEFINITIONS
        ],
        "feature_family_plan": [
            {"feature_family": feature, "status": "PLANNED_ONLY", "calculated": False}
            for feature in FEATURE_FAMILIES
        ],
        "walk_forward_plan": {
            "method": "chronological_walk_forward",
            "training_window": "planned",
            "validation_window": "planned",
            "test_window": "planned",
            "no_shuffle": True,
            "time_order_preserved": True,
            "status": "PLANNED_ONLY",
        },
        "out_of_sample_plan": {
            "final_holdout_period": "planned",
            "no_future_leakage": True,
            "status": "PLANNED_ONLY",
        },
        "baseline_comparisons": list(BASELINE_COMPARISONS),
        "signal_quality_metrics": [
            {"metric": metric, "acceptance_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE}
            for metric in SIGNAL_QUALITY_METRICS
        ],
        "stability_checks": list(STABILITY_CHECKS),
        "false_positive_false_negative_analysis": {
            "status": "PLANNED_ONLY",
            "analysis_if_applicable": True,
            "requires_label_definition": True,
        },
        "leakage_controls": list(LEAKAGE_CONTROLS),
        "minimum_evidence_requirements": [
            "operator-approved label definitions",
            "dataset digest reverification",
            "time-ordered walk-forward configuration",
            "baseline comparison outputs",
            "signal quality metric outputs",
            "stability analysis outputs",
        ],
        "planned_outputs": _planned_outputs(),
        "execution_gates": list(EXECUTION_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "non_goals": list(NON_GOALS),
        "remaining_tasks": [
            "Predictive experiment plan candidate operator review package.",
            "Predictive experiment execution candidate.",
            "Predictive experiment execution approval ceremony.",
            "Predictive experiment execution.",
            "Predictive usefulness review after experiment results.",
        ],
    }


def _profiles(plan: dict[str, Any]) -> list[str]:
    profiles = plan.get("dataset_profiles")
    if not isinstance(profiles, list):
        return []
    return [item.get("profile") for item in profiles if isinstance(item, dict)]


def _planned_outputs_not_generated(plan: dict[str, Any]) -> bool:
    outputs = plan.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(item, dict) and item.get("generation_status") == PLANNED_NOT_GENERATED
        for item in outputs
    )


def _planned_outputs_research_only(plan: dict[str, Any]) -> bool:
    outputs = plan.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(item, dict) and item.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def _checklist(plan: dict[str, Any]) -> list[dict[str, Any]]:
    profiles = _profiles(plan)
    return [
        _check("predictive_review_candidate_digest_bound", EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST, plan.get("predictive_usefulness_review_candidate_digest")),
        _check("predictive_review_candidate_review_digest_bound", EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST, plan.get("predictive_usefulness_review_candidate_review_package_digest")),
        _check("campaign_results_review_digest_bound", EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, plan.get("campaign_execution_results_review_package_digest")),
        _check("campaign_execution_digest_bound", EXPECTED_CAMPAIGN_EXECUTION_DIGEST, plan.get("campaign_execution_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, plan.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, plan.get("position_swing_registry_approval_digest")),
        _check("experiment_scope_research_only", True, (plan.get("experiment_scope") or {}).get("research_only")),
        _check("ticker_universe_aapl_only", ["AAPL"], plan.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["SWING", "POSITION_SWING"], profiles),
        _check("date_range_matches", {"start": "2022-01-01", "end": "2025-12-31"}, plan.get("date_range")),
        _check("label_definitions_defined", LABEL_DEFINITIONS, [item.get("label") for item in plan.get("label_definitions", []) if isinstance(item, dict)]),
        _check("feature_family_plan_defined", FEATURE_FAMILIES, [item.get("feature_family") for item in plan.get("feature_family_plan", []) if isinstance(item, dict)]),
        _check("walk_forward_plan_defined", True, isinstance(plan.get("walk_forward_plan"), dict) and bool(plan.get("walk_forward_plan"))),
        _check("out_of_sample_plan_defined", True, isinstance(plan.get("out_of_sample_plan"), dict) and bool(plan.get("out_of_sample_plan"))),
        _check("baseline_comparisons_defined", BASELINE_COMPARISONS, plan.get("baseline_comparisons")),
        _check("signal_quality_metrics_defined", SIGNAL_QUALITY_METRICS, [item.get("metric") for item in plan.get("signal_quality_metrics", []) if isinstance(item, dict)]),
        _check("stability_checks_defined", STABILITY_CHECKS, plan.get("stability_checks")),
        _check("false_positive_false_negative_analysis_defined", True, isinstance(plan.get("false_positive_false_negative_analysis"), dict) and bool(plan.get("false_positive_false_negative_analysis"))),
        _check("leakage_controls_defined", LEAKAGE_CONTROLS, plan.get("leakage_controls")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(plan)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(plan)),
        _check("execution_gates_defined", EXECUTION_GATES, plan.get("execution_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, plan.get("risk_controls")),
        _check("provider_requests_made_false", False, plan.get("provider_requests_made")),
        _check("predictive_experiment_execution_authorized_false", False, plan.get("predictive_experiment_execution_authorized")),
        _check("predictive_experiment_executed_false", False, plan.get("predictive_experiment_executed")),
        _check("walk_forward_validation_performed_false", False, plan.get("walk_forward_validation_performed")),
        _check("new_strategy_scoring_performed_false", False, plan.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, plan.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, plan.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, plan.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, plan.get("profitability")),
        _check("profitability_acceptance_ready_false", False, plan.get("profitability_acceptance_ready")),
        _check("runtime_migration_recommended_false", False, plan.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, plan.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, plan.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, plan.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, plan.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, plan.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, plan.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, plan.get("broker_execution")),
        _check("automatic_stitching_false", False, plan.get("automatic_stitching")),
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
        "ready_for_operator_review": ready,
        "experiment_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(plan: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(plan)
    payload.pop("predictive_experiment_plan_candidate_digest", None)
    return payload


def predictive_experiment_plan_candidate_digest_v1(plan: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the predictive experiment plan."""
    return semantic_digest(_digest_payload(plan))


def build_predictive_experiment_plan_candidate_v1() -> dict[str, Any]:
    """Build an offline plan candidate for future predictive experiments."""
    plan = _base_plan()
    plan["plan_checklist"] = _checklist(plan)
    plan["plan_summary"] = _summary(plan["plan_checklist"])
    plan["predictive_experiment_plan_candidate_digest"] = (
        predictive_experiment_plan_candidate_digest_v1(plan)
    )
    validate_predictive_experiment_plan_candidate_v1(plan)
    return plan


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "plan") -> None:
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
            raise PredictiveExperimentPlanCandidateError(f"{current_path} must not emit {value}")
        if key in {
            "provider_requests_made",
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
            raise PredictiveExperimentPlanCandidateError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise PredictiveExperimentPlanCandidateError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveExperimentPlanCandidateError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_experiment_plan_candidate_v1(plan: dict[str, Any]) -> dict[str, Any]:
    """Validate a predictive experiment plan without authorizing execution."""
    if not isinstance(plan, dict):
        raise PredictiveExperimentPlanCandidateError("plan must be a JSON object")
    _reject_forbidden_values(plan)
    _expect(plan.get("artifact_kind"), ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE, "artifact_kind")
    _expect(plan.get("schema_version"), SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_V1, "schema_version")
    _expect(plan.get("plan_status"), PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW, "plan_status")
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "experiment_execution_requires_operator_approval",
        "data_quality_readiness",
        "module_compatibility_readiness",
    ):
        _expect_true(plan.get(field), field)
    for field in (
        "provider_requests_made",
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
        _expect_false(plan.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(plan.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "predictive_usefulness_review_candidate_digest": EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST,
        "predictive_usefulness_review_candidate_review_package_digest": EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "campaign_execution_results_review_package_digest": EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "campaign_execution_digest": EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "execution_request_id": EXPECTED_EXECUTION_REQUEST_ID,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "swing_registry_key": EXPECTED_SWING_REGISTRY_KEY,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_key": EXPECTED_POSITION_SWING_REGISTRY_KEY,
        "outputs_reviewed": 12,
        "failure_count": 0,
        "warning_count": 0,
        "ticker_universe": ["AAPL"],
        "date_range": {"start": "2022-01-01", "end": "2025-12-31"},
    }.items():
        _expect(plan.get(field), expected, field)
    _expect(_profiles(plan), ["SWING", "POSITION_SWING"], "dataset_profiles")
    if [item.get("label") for item in plan.get("label_definitions", []) if isinstance(item, dict)] != LABEL_DEFINITIONS:
        raise PredictiveExperimentPlanCandidateError("label_definitions mismatch")
    if [item.get("feature_family") for item in plan.get("feature_family_plan", []) if isinstance(item, dict)] != FEATURE_FAMILIES:
        raise PredictiveExperimentPlanCandidateError("feature_family_plan mismatch")
    if not isinstance(plan.get("walk_forward_plan"), dict) or not plan["walk_forward_plan"]:
        raise PredictiveExperimentPlanCandidateError("walk_forward_plan missing")
    if not isinstance(plan.get("out_of_sample_plan"), dict) or not plan["out_of_sample_plan"]:
        raise PredictiveExperimentPlanCandidateError("out_of_sample_plan missing")
    _expect(plan.get("baseline_comparisons"), BASELINE_COMPARISONS, "baseline_comparisons")
    _expect(
        [item.get("metric") for item in plan.get("signal_quality_metrics", []) if isinstance(item, dict)],
        SIGNAL_QUALITY_METRICS,
        "signal_quality_metrics",
    )
    _expect(plan.get("stability_checks"), STABILITY_CHECKS, "stability_checks")
    if not isinstance(plan.get("false_positive_false_negative_analysis"), dict) or not plan["false_positive_false_negative_analysis"]:
        raise PredictiveExperimentPlanCandidateError("false_positive_false_negative_analysis missing")
    _expect(plan.get("leakage_controls"), LEAKAGE_CONTROLS, "leakage_controls")
    _expect(plan.get("execution_gates"), EXECUTION_GATES, "execution_gates")
    _expect(plan.get("risk_controls"), RISK_CONTROLS, "risk_controls")
    _expect_true(_planned_outputs_not_generated(plan), "planned_outputs_not_generated")
    _expect_true(_planned_outputs_research_only(plan), "planned_outputs_research_only")
    checklist = plan.get("plan_checklist")
    if not isinstance(checklist, list):
        raise PredictiveExperimentPlanCandidateError("plan_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "plan_checklist check IDs",
    )
    expected_checklist = _checklist(plan)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveExperimentPlanCandidateError(
            f"plan checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "plan_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(plan.get("plan_summary"), expected_summary, "plan_summary")
    digest = plan.get("predictive_experiment_plan_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveExperimentPlanCandidateError("predictive_experiment_plan_candidate_digest missing")
    _expect(
        digest,
        predictive_experiment_plan_candidate_digest_v1(plan),
        "predictive_experiment_plan_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_VALID",
        "artifact_kind": plan["artifact_kind"],
        "plan_status": plan["plan_status"],
        "predictive_experiment_plan_candidate_digest": digest,
        "predictive_usefulness_review_candidate_digest": plan[
            "predictive_usefulness_review_candidate_digest"
        ],
        "predictive_usefulness_review_candidate_review_package_digest": plan[
            "predictive_usefulness_review_candidate_review_package_digest"
        ],
        "campaign_execution_results_review_package_digest": plan[
            "campaign_execution_results_review_package_digest"
        ],
        "ready_for_operator_review": plan["plan_summary"]["ready_for_operator_review"],
        "experiment_execution_authorized": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_experiment_plan_candidate_markdown_v1(plan: dict[str, Any]) -> str:
    """Render a sanitized predictive experiment plan candidate summary."""
    validation = validate_predictive_experiment_plan_candidate_v1(plan)
    summary = plan["plan_summary"]
    lines = [
        "# MarketFlow Predictive Experiment Plan Candidate Status",
        "",
        "## Title",
        "- Predictive Experiment Plan Candidate v1.",
        "",
        "## Purpose",
        "- Define future research-only predictive experiments without executing them.",
        "",
        "## Source Evidence",
        f"- Predictive usefulness candidate digest: `{plan['predictive_usefulness_review_candidate_digest']}`",
        f"- Predictive usefulness candidate review digest: `{plan['predictive_usefulness_review_candidate_review_package_digest']}`",
        f"- Campaign results review digest: `{plan['campaign_execution_results_review_package_digest']}`",
        f"- Plan digest: `{validation['predictive_experiment_plan_candidate_digest']}`",
        "",
        "## Experiment Scope",
        f"- Ticker universe: `{', '.join(plan['ticker_universe'])}`",
        f"- Date range: `{plan['date_range']['start']} through {plan['date_range']['end']}`",
        f"- Runtime use: `{plan['runtime_use']}`",
        f"- Strategy use: `{plan['strategy_use']}`",
        "",
        "## Planned Labels",
    ]
    lines.extend(f"- `{item['label']}`" for item in plan["label_definitions"])
    lines.extend(["", "## Planned Feature Families"])
    lines.extend(f"- `{item['feature_family']}`" for item in plan["feature_family_plan"])
    lines.extend(
        [
            "",
            "## Walk-Forward Plan",
            f"- Method: `{plan['walk_forward_plan']['method']}`",
            f"- No shuffle: `{plan['walk_forward_plan']['no_shuffle']}`",
            f"- Time order preserved: `{plan['walk_forward_plan']['time_order_preserved']}`",
            "",
            "## Out-of-Sample Plan",
            f"- Final holdout period: `{plan['out_of_sample_plan']['final_holdout_period']}`",
            f"- No future leakage: `{plan['out_of_sample_plan']['no_future_leakage']}`",
            "",
            "## Baselines and Metrics",
        ]
    )
    lines.extend(f"- Baseline: `{item}`" for item in plan["baseline_comparisons"])
    lines.extend(f"- Metric: `{item['metric']}`" for item in plan["signal_quality_metrics"])
    lines.extend(["", "## Leakage Controls"])
    lines.extend(f"- `{item}`" for item in plan["leakage_controls"])
    lines.extend(["", "## Execution Gates"])
    lines.extend(f"- `{item}`" for item in plan["execution_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in plan["risk_controls"])
    lines.extend(
        [
            "",
            "## Boundary Conditions",
            f"- provider_requests_made: `{plan['provider_requests_made']}`",
            f"- predictive_experiment_execution_authorized: `{plan['predictive_experiment_execution_authorized']}`",
            f"- predictive_experiment_executed: `{plan['predictive_experiment_executed']}`",
            f"- walk_forward_validation_performed: `{plan['walk_forward_validation_performed']}`",
            f"- new_strategy_scoring_performed: `{plan['new_strategy_scoring_performed']}`",
            f"- trade_recommendations_generated: `{plan['trade_recommendations_generated']}`",
            f"- predictive_usefulness: `{plan['predictive_usefulness']}`",
            f"- profitability: `{plan['profitability']}`",
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
    lines.extend(f"{index}. {task}" for index, task in enumerate(plan["remaining_tasks"], start=1))
    lines.append("")
    return "\n".join(lines)


def write_predictive_experiment_plan_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the predictive experiment plan candidate JSON without overwriting output."""
    plan = build_predictive_experiment_plan_candidate_v1()
    validation = validate_predictive_experiment_plan_candidate_v1(plan)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_experiment_plan_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveExperimentPlanCandidateError(
            "predictive experiment plan candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveExperimentPlanCandidateError(
            "predictive experiment plan candidate output already exists"
        )
    payload = canonical_json_bytes(plan)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
