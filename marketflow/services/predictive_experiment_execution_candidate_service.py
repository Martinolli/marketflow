"""Offline predictive experiment execution candidate for future operator review."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    predictive_experiment_plan_candidate_operator_review_service as plan_review_service,
)


ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_V1 = (
    "predictive_experiment_execution_candidate_v1"
)
PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    plan_review_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    "e71197fb6838e2caa99d1cffa3c6bd8847d3170d6f842ea921e5345dac349180"
)
EXPECTED_SWING_DATASET_ROWS_DIGEST = (
    "e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc"
)
EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST = (
    "163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3"
)
PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID = (
    "AAPL_PREDICTIVE_EXPERIMENT_EXECUTION_2022_2025_V1"
)

NOT_AUTHORIZED = plan_review_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_GENERATED = plan_review_service.plan_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = plan_review_service.plan_service.RESEARCH_ONLY_NON_ACTIONABLE
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = (
    plan_review_service.plan_service.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
)

LABEL_DEFINITIONS = list(plan_review_service.plan_service.LABEL_DEFINITIONS)
FEATURE_FAMILIES = list(plan_review_service.plan_service.FEATURE_FAMILIES)
BASELINE_COMPARISONS = list(plan_review_service.plan_service.BASELINE_COMPARISONS)
SIGNAL_QUALITY_METRICS = list(plan_review_service.plan_service.SIGNAL_QUALITY_METRICS)
LEAKAGE_CONTROLS = list(plan_review_service.plan_service.LEAKAGE_CONTROLS)

PLANNED_OUTPUT_NAMES = [
    "predictive_experiment_run_manifest",
    "label_definition_report",
    "label_generation_report",
    "feature_family_report",
    "feature_matrix_manifest",
    "walk_forward_configuration_report",
    "out_of_sample_split_report",
    "baseline_comparison_report",
    "signal_quality_metrics_report",
    "stability_analysis_report",
    "false_positive_false_negative_report",
    "leakage_control_report",
    "operator_review_summary",
]
EXECUTION_GATES = [
    "predictive_experiment_execution_candidate_operator_review",
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
RISK_CONTROLS = list(plan_review_service.plan_service.RISK_CONTROLS)
NON_GOALS = [
    "Execute predictive experiments.",
    "Run walk-forward validation.",
    "Run out-of-sample evaluation.",
    "Calculate labels.",
    "Calculate feature matrices.",
    "Run strategy scoring.",
    "Generate trade recommendations.",
    "Accept predictive usefulness or profitability.",
    "Authorize runtime migration, paper trading, or broker execution.",
]

REQUIRED_CHECK_IDS = [
    "predictive_experiment_plan_digest_bound",
    "predictive_experiment_plan_review_digest_bound",
    "predictive_usefulness_review_candidate_digest_bound",
    "predictive_usefulness_review_candidate_review_digest_bound",
    "campaign_results_review_digest_bound",
    "campaign_execution_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "execution_request_id_defined",
    "experiment_scope_research_only",
    "ticker_universe_aapl_only",
    "profiles_swing_and_position_swing",
    "date_range_matches",
    "execution_mode_offline_research_experiment",
    "runtime_mode_not_runtime",
    "strategy_mode_not_strategy_input",
    "broker_mode_disabled",
    "paper_trading_mode_disabled",
    "labels_defined",
    "feature_families_defined",
    "walk_forward_plan_preserved",
    "out_of_sample_plan_preserved",
    "baselines_defined",
    "metrics_defined_research_only",
    "leakage_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "execution_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "predictive_experiment_execution_authorized_false",
    "predictive_experiment_executed_false",
    "walk_forward_validation_performed_false",
    "out_of_sample_evaluation_performed_false",
    "label_generation_performed_false",
    "feature_matrix_generation_performed_false",
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


class PredictiveExperimentExecutionCandidateError(ValueError):
    """Raised when a predictive experiment execution candidate is invalid."""


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
        raise PredictiveExperimentExecutionCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveExperimentExecutionCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveExperimentExecutionCandidateError(f"{field_name} must be false")


def _planned_inputs() -> list[dict[str, str]]:
    return [
        {
            "profile": "SWING",
            "timeframe": "RTH_HALF_SESSION_195M",
            "registry_key": plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_KEY,
            "dataset_rows_digest": EXPECTED_SWING_DATASET_ROWS_DIGEST,
            "path": (
                ".marketflow/canonical_candidates/AAPL/SWING/"
                "AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv"
            ),
        },
        {
            "profile": "POSITION_SWING",
            "timeframe": "RTH_FULL_SESSION_1D",
            "registry_key": plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_KEY,
            "dataset_rows_digest": EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST,
            "path": (
                ".marketflow/canonical_candidates/AAPL/POSITION_SWING/"
                "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv"
            ),
        },
    ]


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "name": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _base_candidate() -> dict[str, Any]:
    reviewed_package = (
        plan_review_service.build_predictive_experiment_plan_candidate_review_package_v1()
    )
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_V1,
        "candidate_status": PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "predictive_experiment_execution_authorized": False,
        "predictive_experiment_executed": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_performed": False,
        "label_generation_performed": False,
        "feature_matrix_generation_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": (
            plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
        ),
        "predictive_usefulness_acceptance_ready": False,
        "profitability": plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
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
        "predictive_experiment_plan_digest": reviewed_package["reviewed_plan_digest"],
        "predictive_experiment_plan_review_package_digest": reviewed_package[
            "predictive_experiment_plan_candidate_review_package_digest"
        ],
        "predictive_usefulness_review_candidate_digest": reviewed_package[
            "predictive_usefulness_review_candidate_digest"
        ],
        "predictive_usefulness_review_candidate_review_package_digest": reviewed_package[
            "predictive_usefulness_review_candidate_review_package_digest"
        ],
        "campaign_execution_results_review_package_digest": reviewed_package[
            "campaign_execution_results_review_package_digest"
        ],
        "campaign_execution_digest": reviewed_package["campaign_execution_digest"],
        "execution_request_id": reviewed_package["execution_request_id"],
        "swing_registry_approval_digest": reviewed_package["swing_registry_approval_digest"],
        "swing_registry_key": plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_KEY,
        "swing_dataset_rows_digest": EXPECTED_SWING_DATASET_ROWS_DIGEST,
        "position_swing_registry_approval_digest": reviewed_package[
            "position_swing_registry_approval_digest"
        ],
        "position_swing_registry_key": (
            plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_KEY
        ),
        "position_swing_dataset_rows_digest": EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST,
        "predictive_experiment_execution_request_id": (
            PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID
        ),
        "experiment_name": "AAPL_SWING_POSITION_SWING_PREDICTIVE_EXPERIMENT_EXECUTION_V1",
        "experiment_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "dataset_profiles": deepcopy(reviewed_package["dataset_profiles"]),
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "registry_scope": "RESEARCH_DATASET",
        "execution_mode": "OFFLINE_RESEARCH_EXPERIMENT",
        "runtime_mode": "NOT_RUNTIME",
        "strategy_mode": "NOT_STRATEGY_INPUT",
        "broker_mode": "DISABLED",
        "paper_trading_mode": "DISABLED",
        "planned_input_files": _planned_inputs(),
        "planned_output_root": ".marketflow/predictive_experiments/AAPL/2022_2025/",
        "label_definitions": deepcopy(reviewed_package["label_definitions"]),
        "feature_family_plan": deepcopy(reviewed_package["feature_family_plan"]),
        "walk_forward_plan": deepcopy(reviewed_package["walk_forward_plan"]),
        "out_of_sample_plan": deepcopy(reviewed_package["out_of_sample_plan"]),
        "baseline_comparisons": list(reviewed_package["baseline_comparisons"]),
        "signal_quality_metrics": [
            {"metric": metric, "acceptance_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE}
            for metric in SIGNAL_QUALITY_METRICS
        ],
        "stability_checks": list(reviewed_package["stability_checks"]),
        "false_positive_false_negative_analysis": deepcopy(
            reviewed_package["false_positive_false_negative_analysis"]
        ),
        "leakage_controls": list(reviewed_package["leakage_controls"]),
        "planned_outputs": _planned_outputs(),
        "execution_gates": list(EXECUTION_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "non_goals": list(NON_GOALS),
        "remaining_tasks": [
            "Predictive experiment execution candidate operator review package.",
            "Predictive experiment execution approval ceremony.",
            "Predictive experiment execution.",
            "Predictive usefulness review after experiment results.",
        ],
    }


def _profiles(candidate: dict[str, Any]) -> list[str]:
    profiles = candidate.get("dataset_profiles")
    if not isinstance(profiles, list):
        return []
    return [item.get("profile") for item in profiles if isinstance(item, dict)]


def _metric_acceptance_labels(candidate: dict[str, Any]) -> list[str]:
    metrics = candidate.get("signal_quality_metrics")
    if not isinstance(metrics, list):
        return []
    return [
        item.get("acceptance_label")
        for item in metrics
        if isinstance(item, dict) and "acceptance_label" in item
    ]


def _planned_outputs_not_generated(candidate: dict[str, Any]) -> bool:
    outputs = candidate.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(item, dict) and item.get("generation_status") == PLANNED_NOT_GENERATED
        for item in outputs
    )


def _planned_outputs_research_only(candidate: dict[str, Any]) -> bool:
    outputs = candidate.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        isinstance(item, dict) and item.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = candidate.get("signal_quality_metrics", [])
    return [
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, candidate.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_experiment_plan_review_package_digest")),
        _check("predictive_usefulness_review_candidate_digest_bound", plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST, candidate.get("predictive_usefulness_review_candidate_digest")),
        _check("predictive_usefulness_review_candidate_review_digest_bound", plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_usefulness_review_candidate_review_package_digest")),
        _check("campaign_results_review_digest_bound", plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("campaign_execution_results_review_package_digest")),
        _check("campaign_execution_digest_bound", plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST, candidate.get("campaign_execution_digest")),
        _check("swing_registry_approval_digest_bound", plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("position_swing_registry_approval_digest")),
        _check("execution_request_id_defined", PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID, candidate.get("predictive_experiment_execution_request_id")),
        _check("experiment_scope_research_only", "RESEARCH_ONLY", candidate.get("experiment_scope")),
        _check("ticker_universe_aapl_only", ["AAPL"], candidate.get("ticker_universe")),
        _check("profiles_swing_and_position_swing", ["SWING", "POSITION_SWING"], _profiles(candidate)),
        _check("date_range_matches", {"start": "2022-01-01", "end": "2025-12-31"}, {"start": candidate.get("date_range_start"), "end": candidate.get("date_range_end")}),
        _check("execution_mode_offline_research_experiment", "OFFLINE_RESEARCH_EXPERIMENT", candidate.get("execution_mode")),
        _check("runtime_mode_not_runtime", "NOT_RUNTIME", candidate.get("runtime_mode")),
        _check("strategy_mode_not_strategy_input", "NOT_STRATEGY_INPUT", candidate.get("strategy_mode")),
        _check("broker_mode_disabled", "DISABLED", candidate.get("broker_mode")),
        _check("paper_trading_mode_disabled", "DISABLED", candidate.get("paper_trading_mode")),
        _check("labels_defined", LABEL_DEFINITIONS, [item.get("label") for item in candidate.get("label_definitions", []) if isinstance(item, dict)]),
        _check("feature_families_defined", FEATURE_FAMILIES, [item.get("feature_family") for item in candidate.get("feature_family_plan", []) if isinstance(item, dict)]),
        _check("walk_forward_plan_preserved", "chronological_walk_forward", (candidate.get("walk_forward_plan") or {}).get("method")),
        _check("out_of_sample_plan_preserved", True, (candidate.get("out_of_sample_plan") or {}).get("no_future_leakage")),
        _check("baselines_defined", BASELINE_COMPARISONS, candidate.get("baseline_comparisons")),
        _check("metrics_defined_research_only", [RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE] * len(metrics), _metric_acceptance_labels(candidate)),
        _check("leakage_controls_defined", LEAKAGE_CONTROLS, candidate.get("leakage_controls")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(candidate)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(candidate)),
        _check("execution_gates_defined", EXECUTION_GATES, candidate.get("execution_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("predictive_experiment_execution_authorized_false", False, candidate.get("predictive_experiment_execution_authorized")),
        _check("predictive_experiment_executed_false", False, candidate.get("predictive_experiment_executed")),
        _check("walk_forward_validation_performed_false", False, candidate.get("walk_forward_validation_performed")),
        _check("out_of_sample_evaluation_performed_false", False, candidate.get("out_of_sample_evaluation_performed")),
        _check("label_generation_performed_false", False, candidate.get("label_generation_performed")),
        _check("feature_matrix_generation_performed_false", False, candidate.get("feature_matrix_generation_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        _check("profitability_acceptance_ready_false", False, candidate.get("profitability_acceptance_ready")),
        _check("runtime_migration_recommended_false", False, candidate.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
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
        "experiment_execution_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("predictive_experiment_execution_candidate_digest", None)
    return payload


def predictive_experiment_execution_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the execution candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_predictive_experiment_execution_candidate_v1() -> dict[str, Any]:
    """Build an offline candidate request for future predictive experiment execution."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["predictive_experiment_execution_candidate_digest"] = (
        predictive_experiment_execution_candidate_digest_v1(candidate)
    )
    validate_predictive_experiment_execution_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
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
            raise PredictiveExperimentExecutionCandidateError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made",
            "predictive_experiment_execution_authorized",
            "predictive_experiment_executed",
            "walk_forward_validation_performed",
            "out_of_sample_evaluation_performed",
            "label_generation_performed",
            "feature_matrix_generation_performed",
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
            raise PredictiveExperimentExecutionCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise PredictiveExperimentExecutionCandidateError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveExperimentExecutionCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_experiment_execution_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate an execution candidate without authorizing or running an experiment."""
    if not isinstance(candidate, dict):
        raise PredictiveExperimentExecutionCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW,
        "candidate_status",
    )
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "experiment_execution_requires_operator_approval",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "predictive_experiment_execution_authorized",
        "predictive_experiment_executed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "label_generation_performed",
        "feature_matrix_generation_performed",
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
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
        "predictive_experiment_plan_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
        "predictive_experiment_plan_review_package_digest": EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_review_candidate_digest": plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST,
        "predictive_usefulness_review_candidate_review_package_digest": plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "campaign_execution_results_review_package_digest": plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "campaign_execution_digest": plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "execution_request_id": plan_review_service.plan_service.EXPECTED_EXECUTION_REQUEST_ID,
        "swing_registry_approval_digest": plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "swing_registry_key": plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_KEY,
        "swing_dataset_rows_digest": EXPECTED_SWING_DATASET_ROWS_DIGEST,
        "position_swing_registry_approval_digest": plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_key": plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_KEY,
        "position_swing_dataset_rows_digest": EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST,
        "predictive_experiment_execution_request_id": PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID,
        "experiment_scope": "RESEARCH_ONLY",
        "ticker_universe": ["AAPL"],
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "registry_scope": "RESEARCH_DATASET",
        "execution_mode": "OFFLINE_RESEARCH_EXPERIMENT",
        "runtime_mode": "NOT_RUNTIME",
        "strategy_mode": "NOT_STRATEGY_INPUT",
        "broker_mode": "DISABLED",
        "paper_trading_mode": "DISABLED",
        "planned_output_root": ".marketflow/predictive_experiments/AAPL/2022_2025/",
    }.items():
        _expect(candidate.get(field), expected, field)
    _expect(_profiles(candidate), ["SWING", "POSITION_SWING"], "dataset_profiles")
    _expect(candidate.get("planned_input_files"), _planned_inputs(), "planned_input_files")
    _expect(
        [item.get("label") for item in candidate.get("label_definitions", []) if isinstance(item, dict)],
        LABEL_DEFINITIONS,
        "label_definitions",
    )
    _expect(
        [
            item.get("feature_family")
            for item in candidate.get("feature_family_plan", [])
            if isinstance(item, dict)
        ],
        FEATURE_FAMILIES,
        "feature_family_plan",
    )
    if not isinstance(candidate.get("walk_forward_plan"), dict) or not candidate["walk_forward_plan"]:
        raise PredictiveExperimentExecutionCandidateError("walk_forward_plan missing")
    if not isinstance(candidate.get("out_of_sample_plan"), dict) or not candidate["out_of_sample_plan"]:
        raise PredictiveExperimentExecutionCandidateError("out_of_sample_plan missing")
    _expect(
        candidate["walk_forward_plan"].get("method"),
        "chronological_walk_forward",
        "walk_forward_plan",
    )
    _expect_true(candidate["walk_forward_plan"].get("no_shuffle"), "walk_forward_plan.no_shuffle")
    _expect_true(
        candidate["walk_forward_plan"].get("time_order_preserved"),
        "walk_forward_plan.time_order_preserved",
    )
    _expect_true(
        candidate["out_of_sample_plan"].get("no_future_leakage"),
        "out_of_sample_plan.no_future_leakage",
    )
    _expect(candidate.get("baseline_comparisons"), BASELINE_COMPARISONS, "baseline_comparisons")
    _expect(
        [item.get("metric") for item in candidate.get("signal_quality_metrics", []) if isinstance(item, dict)],
        SIGNAL_QUALITY_METRICS,
        "signal_quality_metrics",
    )
    _expect(
        _metric_acceptance_labels(candidate),
        [RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE] * len(SIGNAL_QUALITY_METRICS),
        "signal_quality_metrics acceptance labels",
    )
    _expect(candidate.get("leakage_controls"), LEAKAGE_CONTROLS, "leakage_controls")
    _expect_true(_planned_outputs_not_generated(candidate), "planned_outputs_not_generated")
    _expect_true(_planned_outputs_research_only(candidate), "planned_outputs_research_only")
    _expect(candidate.get("execution_gates"), EXECUTION_GATES, "execution_gates")
    _expect(candidate.get("risk_controls"), RISK_CONTROLS, "risk_controls")
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise PredictiveExperimentExecutionCandidateError("candidate_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveExperimentExecutionCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), expected_summary, "candidate_summary")
    digest = candidate.get("predictive_experiment_execution_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveExperimentExecutionCandidateError(
            "predictive_experiment_execution_candidate_digest missing"
        )
    _expect(
        digest,
        predictive_experiment_execution_candidate_digest_v1(candidate),
        "predictive_experiment_execution_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "predictive_experiment_execution_candidate_digest": digest,
        "predictive_experiment_execution_request_id": candidate[
            "predictive_experiment_execution_request_id"
        ],
        "predictive_experiment_plan_digest": candidate["predictive_experiment_plan_digest"],
        "predictive_experiment_plan_review_package_digest": candidate[
            "predictive_experiment_plan_review_package_digest"
        ],
        "campaign_execution_results_review_package_digest": candidate[
            "campaign_execution_results_review_package_digest"
        ],
        "ready_for_operator_review": candidate["candidate_summary"][
            "ready_for_operator_review"
        ],
        "experiment_execution_authorized": False,
        "experiment_execution_performed": False,
        "predictive_usefulness": (
            plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
        ),
        "profitability": plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_experiment_execution_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized predictive experiment execution candidate summary."""
    validation = validate_predictive_experiment_execution_candidate_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Predictive Experiment Execution Candidate Status",
        "",
        "## Title",
        "- Predictive Experiment Execution Candidate v1.",
        "",
        "## Purpose",
        "- Define a future offline research experiment request without executing it.",
        "",
        "## Execution Candidate Scope",
        f"- Request ID: `{candidate['predictive_experiment_execution_request_id']}`",
        f"- Candidate digest: `{validation['predictive_experiment_execution_candidate_digest']}`",
        f"- Ticker universe: `{', '.join(candidate['ticker_universe'])}`",
        f"- Date range: `{candidate['date_range_start']} through {candidate['date_range_end']}`",
        f"- Execution mode: `{candidate['execution_mode']}`",
        f"- Runtime mode: `{candidate['runtime_mode']}`",
        f"- Strategy mode: `{candidate['strategy_mode']}`",
        "",
        "## Source Evidence",
        f"- Predictive experiment plan digest: `{candidate['predictive_experiment_plan_digest']}`",
        f"- Predictive experiment plan review digest: `{candidate['predictive_experiment_plan_review_package_digest']}`",
        f"- Predictive usefulness candidate digest: `{candidate['predictive_usefulness_review_candidate_digest']}`",
        f"- Predictive usefulness candidate review digest: `{candidate['predictive_usefulness_review_candidate_review_package_digest']}`",
        f"- Campaign results review digest: `{candidate['campaign_execution_results_review_package_digest']}`",
        f"- Campaign execution digest: `{candidate['campaign_execution_digest']}`",
        "",
        "## Planned Inputs",
    ]
    lines.extend(
        f"- `{item['profile']}` `{item['path']}` digest `{item['dataset_rows_digest']}`"
        for item in candidate["planned_input_files"]
    )
    lines.extend(["", "## Labels and Features"])
    lines.extend(f"- Label: `{item['label']}`" for item in candidate["label_definitions"])
    lines.extend(
        f"- Feature family: `{item['feature_family']}`"
        for item in candidate["feature_family_plan"]
    )
    lines.extend(
        [
            "",
            "## Walk-Forward / OOS Design",
            f"- Walk-forward type: `{candidate['walk_forward_plan']['method']}`",
            f"- No shuffle: `{candidate['walk_forward_plan']['no_shuffle']}`",
            f"- Final holdout: `{candidate['out_of_sample_plan']['final_holdout_period']}`",
            "",
            "## Planned Outputs",
        ]
    )
    lines.extend(f"- `{item['name']}` `{item['generation_status']}`" for item in candidate["planned_outputs"])
    lines.extend(["", "## Execution Gates"])
    lines.extend(f"- `{item}`" for item in candidate["execution_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Boundary Conditions",
            f"- provider_requests_made: `{candidate['provider_requests_made']}`",
            f"- predictive_experiment_execution_authorized: `{candidate['predictive_experiment_execution_authorized']}`",
            f"- predictive_experiment_executed: `{candidate['predictive_experiment_executed']}`",
            f"- walk_forward_validation_performed: `{candidate['walk_forward_validation_performed']}`",
            f"- label_generation_performed: `{candidate['label_generation_performed']}`",
            f"- feature_matrix_generation_performed: `{candidate['feature_matrix_generation_performed']}`",
            f"- new_strategy_scoring_performed: `{candidate['new_strategy_scoring_performed']}`",
            f"- trade_recommendations_generated: `{candidate['trade_recommendations_generated']}`",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- profitability: `{candidate['profitability']}`",
            f"- runtime_use: `{candidate['runtime_use']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Non-Goals",
        ]
    )
    lines.extend(f"- {item}" for item in candidate["non_goals"])
    lines.append("")
    return "\n".join(lines)


def write_predictive_experiment_execution_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the predictive experiment execution candidate JSON without overwriting output."""
    candidate = build_predictive_experiment_execution_candidate_v1()
    validation = validate_predictive_experiment_execution_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_experiment_execution_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveExperimentExecutionCandidateError(
            "predictive experiment execution candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveExperimentExecutionCandidateError(
            "predictive experiment execution candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
