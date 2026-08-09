"""Offline additional predictive evidence plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    predictive_usefulness_acceptance_readiness_candidate_operator_review_service as readiness_review,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_V1 = (
    "additional_predictive_evidence_plan_candidate_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST = (
    "17c43213689f45e7af9641354cae0e145bb71091d092b4abc856004ab9d7ba57"
)
EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    readiness_review.EXPECTED_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
)
EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    readiness_review.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ASSESSMENT_CANDIDATE_DIGEST = readiness_review.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    readiness_review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    readiness_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    readiness_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    readiness_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    readiness_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = readiness_review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    readiness_review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

ACCEPTANCE_READINESS_STATE_NOT_READY = readiness_review.ACCEPTANCE_READINESS_STATE_NOT_READY
ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED = (
    readiness_review.ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED
)
NOT_AUTHORIZED = readiness_review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

GAPS_ADDRESSED = list(readiness_review.NOT_READY_REASONS)

PLAN_PHASES = [
    {
        "phase_id": "phase_01_evidence_reporting_completeness_enhancement",
        "phase_name": "Evidence reporting completeness enhancement",
        "purpose": "Define missing evidence-reporting fields before any future execution.",
        "addresses_gap": ["metrics_marked_not_acceptance_evidence"],
        "planned_inputs": [
            "predictive_usefulness_acceptance_readiness_candidate_review_package",
            "predictive_experiment_results_review_package",
        ],
        "planned_outputs": ["additional_evidence_plan_manifest"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_02_failure_warning_count_instrumentation",
        "phase_name": "Failure/warning count instrumentation",
        "purpose": "Plan explicit failure and warning count reporting for future evidence.",
        "addresses_gap": ["failure_warning_counts_unavailable"],
        "planned_inputs": ["existing predictive experiment result summaries"],
        "planned_outputs": ["failure_warning_instrumentation_plan"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_03_stronger_walk_forward_protocol_design",
        "phase_name": "Stronger walk-forward protocol design",
        "purpose": "Define a stronger future walk-forward protocol before reruns are considered.",
        "addresses_gap": ["simplified_chronological_split"],
        "planned_inputs": ["current simplified chronological research split notes"],
        "planned_outputs": ["stronger_walk_forward_protocol_plan"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_04_expanded_out_of_sample_validation_design",
        "phase_name": "Expanded out-of-sample validation design",
        "purpose": "Plan expanded OOS validation windows and interpretation boundaries.",
        "addresses_gap": ["simplified_chronological_split"],
        "planned_inputs": ["current chronological OOS research split notes"],
        "planned_outputs": ["expanded_oos_validation_plan"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_05_multi_ticker_replication_or_single_ticker_justification",
        "phase_name": "Multi-ticker replication or operator-accepted single-ticker justification",
        "purpose": "Plan broader ticker evidence or document an explicit operator scope decision.",
        "addresses_gap": [
            "single_ticker_scope",
            "single_asset_class_scope_if_applicable",
            "no_multi_ticker_or_out_of_domain_generalization",
        ],
        "planned_inputs": ["registry-approved research profiles", "operator scope decision"],
        "planned_outputs": [
            "multi_ticker_replication_or_single_ticker_justification_plan"
        ],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_06_signal_stability_analysis_across_time_slices",
        "phase_name": "Signal stability analysis across time slices",
        "purpose": "Plan time-slice stability checks before reassessing predictive usefulness.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "planned_inputs": ["future operator-approved evidence outputs"],
        "planned_outputs": ["signal_stability_analysis_plan"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_07_baseline_comparison_predefined_thresholds",
        "phase_name": "Baseline comparison interpretation with predefined thresholds",
        "purpose": "Plan threshold definitions and baseline interpretation before review.",
        "addresses_gap": ["metrics_marked_not_acceptance_evidence"],
        "planned_inputs": ["existing baseline and metric count summary"],
        "planned_outputs": ["baseline_interpretation_threshold_plan"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_08_transaction_cost_slippage_modeling_if_profitability_reviewed",
        "phase_name": "Transaction cost and slippage modeling, if profitability is later reviewed",
        "purpose": "Plan cost and slippage evidence only for a separate future profitability review.",
        "addresses_gap": [
            "no_transaction_cost_model",
            "no_slippage_model",
            "no_profitability_acceptance",
        ],
        "planned_inputs": ["future profitability review scope if authorized"],
        "planned_outputs": ["cost_slippage_modeling_plan_if_profitability_reviewed"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_09_non_runtime_acceptance_boundary_confirmation",
        "phase_name": "Explicit non-runtime acceptance boundary confirmation",
        "purpose": "Plan written boundaries separating research evidence from runtime use.",
        "addresses_gap": [
            "no_runtime_strategy_validation",
            "no_live_or_paper_trading_validation",
        ],
        "planned_inputs": ["current NOT_AUTHORIZED runtime boundary"],
        "planned_outputs": ["non_runtime_boundary_confirmation_plan"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
    {
        "phase_id": "phase_10_operator_decision_gate_before_acceptance_candidate",
        "phase_name": "Operator decision gate before any acceptance candidate",
        "purpose": "Plan the explicit operator decision required before any acceptance candidate.",
        "addresses_gap": ["operator_acceptance_ceremony_required"],
        "planned_inputs": ["future additional evidence review package"],
        "planned_outputs": ["operator_decision_gate_plan"],
        "execution_required": False,
        "operator_approval_required_before_execution": True,
        "runtime_authorization_required": False,
    },
]

PLANNED_OUTPUT_IDS = [
    "additional_evidence_plan_manifest",
    "failure_warning_instrumentation_plan",
    "stronger_walk_forward_protocol_plan",
    "expanded_oos_validation_plan",
    "multi_ticker_replication_or_single_ticker_justification_plan",
    "signal_stability_analysis_plan",
    "baseline_interpretation_threshold_plan",
    "cost_slippage_modeling_plan_if_profitability_reviewed",
    "non_runtime_boundary_confirmation_plan",
    "operator_decision_gate_plan",
]

FUTURE_EXECUTION_GATES = [
    "additional_predictive_evidence_plan_operator_review",
    "additional_predictive_evidence_execution_candidate",
    "additional_predictive_evidence_execution_approval",
    "dataset_scope_expansion_authority_if_new_tickers_are_added",
    "provider_access_authority_if_new_data_is_required",
    "failure_warning_reporting_review",
    "walk_forward_protocol_review",
    "oos_validation_protocol_review",
    "signal_stability_review",
    "baseline_threshold_review",
    "cost_slippage_model_review_if_profitability_is_reviewed",
    "predictive_usefulness_acceptance_readiness_reassessment",
]

RISK_CONTROLS = [
    "no_provider_refresh_without_authority",
    "no_new_ticker_inclusion_without_authority",
    "no_broker_execution",
    "no_paper_trading",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_trade_recommendations",
    "no_predictive_usefulness_acceptance_in_evidence_planning",
    "no_profitability_acceptance_in_evidence_planning",
    "all_outputs_labeled_research_only",
    "operator_approval_required_before_execution",
]

REQUIRED_CHECK_IDS = [
    "acceptance_readiness_review_digest_bound",
    "acceptance_readiness_candidate_digest_bound",
    "assessment_review_digest_bound",
    "assessment_candidate_digest_bound",
    "predictive_experiment_results_review_digest_bound",
    "predictive_experiment_execution_digest_bound",
    "predictive_experiment_execution_approval_digest_bound",
    "predictive_experiment_plan_digest_bound",
    "predictive_experiment_plan_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "readiness_state_not_ready",
    "predictive_evidence_sufficient_for_acceptance_false",
    "ready_for_acceptance_candidate_false",
    "gap_single_ticker_scope_addressed",
    "gap_simplified_split_addressed",
    "gap_failure_warning_counts_addressed",
    "gap_metrics_not_acceptance_evidence_addressed",
    "gap_no_runtime_validation_addressed",
    "gap_no_cost_slippage_model_addressed",
    "gap_no_live_paper_validation_addressed",
    "gap_no_generalization_addressed",
    "plan_phases_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "future_execution_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
    "predictive_experiment_rerun_performed_false",
    "walk_forward_rerun_performed_false",
    "label_regeneration_performed_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
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
]


class AdditionalPredictiveEvidencePlanCandidateError(ValueError):
    """Raised when the additional predictive evidence plan candidate is invalid."""


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
        raise AdditionalPredictiveEvidencePlanCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidencePlanCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidencePlanCandidateError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_V1,
        "candidate_status": ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_experiment_rerun_authorized": False,
        "predictive_experiment_rerun_performed": False,
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
        "execution_requires_operator_approval": True,
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
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
        "ready_for_acceptance_candidate": False,
        "gaps_addressed": list(GAPS_ADDRESSED),
        "plan_phases": deepcopy(PLAN_PHASES),
        "planned_outputs": _planned_outputs(),
        "future_execution_gates": list(FUTURE_EXECUTION_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    gaps = set(candidate.get("gaps_addressed", []))
    planned_outputs = candidate.get("planned_outputs", [])
    return [
        _check("acceptance_readiness_review_digest_bound", EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_usefulness_acceptance_readiness_candidate_review_package_digest")),
        _check("acceptance_readiness_candidate_digest_bound", EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST, candidate.get("predictive_usefulness_acceptance_readiness_candidate_digest")),
        _check("assessment_review_digest_bound", EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_usefulness_assessment_candidate_review_package_digest")),
        _check("assessment_candidate_digest_bound", EXPECTED_ASSESSMENT_CANDIDATE_DIGEST, candidate.get("predictive_usefulness_assessment_candidate_digest")),
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_experiment_results_review_package_digest")),
        _check("predictive_experiment_execution_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST, candidate.get("predictive_experiment_execution_digest")),
        _check("predictive_experiment_execution_approval_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST, candidate.get("predictive_experiment_execution_approval_digest")),
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, candidate.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_experiment_plan_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, candidate.get("position_swing_registry_approval_digest")),
        _check("readiness_state_not_ready", ACCEPTANCE_READINESS_STATE_NOT_READY, candidate.get("acceptance_readiness_state")),
        _check("predictive_evidence_sufficient_for_acceptance_false", False, candidate.get("predictive_evidence_sufficient_for_acceptance")),
        _check("ready_for_acceptance_candidate_false", False, candidate.get("ready_for_acceptance_candidate")),
        _check("gap_single_ticker_scope_addressed", True, "single_ticker_scope" in gaps),
        _check("gap_simplified_split_addressed", True, "simplified_chronological_split" in gaps),
        _check("gap_failure_warning_counts_addressed", True, "failure_warning_counts_unavailable" in gaps),
        _check("gap_metrics_not_acceptance_evidence_addressed", True, "metrics_marked_not_acceptance_evidence" in gaps),
        _check("gap_no_runtime_validation_addressed", True, "no_runtime_strategy_validation" in gaps),
        _check("gap_no_cost_slippage_model_addressed", True, {"no_transaction_cost_model", "no_slippage_model"}.issubset(gaps)),
        _check("gap_no_live_paper_validation_addressed", True, "no_live_or_paper_trading_validation" in gaps),
        _check("gap_no_generalization_addressed", True, "no_multi_ticker_or_out_of_domain_generalization" in gaps),
        _check("plan_phases_defined", PLAN_PHASES, candidate.get("plan_phases")),
        _check("planned_outputs_not_generated", True, all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in planned_outputs)),
        _check("planned_outputs_research_only", True, all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned_outputs)),
        _check("future_execution_gates_defined", FUTURE_EXECUTION_GATES, candidate.get("future_execution_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("additional_predictive_evidence_execution_authorized_false", False, candidate.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, candidate.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, candidate.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, candidate.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, candidate.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, candidate.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, candidate.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
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
        "ready_for_additional_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("additional_predictive_evidence_plan_candidate_digest", None)
    return payload


def additional_predictive_evidence_plan_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the plan candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_additional_predictive_evidence_plan_candidate_v1() -> dict[str, Any]:
    """Build an offline planning artifact for future additional evidence only."""
    candidate = _base_candidate()
    candidate["plan_checklist"] = _checklist(candidate)
    candidate["plan_summary"] = _summary(candidate["plan_checklist"])
    candidate["additional_predictive_evidence_plan_candidate_digest"] = (
        additional_predictive_evidence_plan_candidate_digest_v1(candidate)
    )
    validate_additional_predictive_evidence_plan_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
            "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
            "TRADE_RECOMMENDATIONS",
        }:
            raise AdditionalPredictiveEvidencePlanCandidateError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made",
            "additional_predictive_evidence_execution_authorized",
            "additional_predictive_evidence_executed",
            "predictive_experiment_rerun_authorized",
            "predictive_experiment_rerun_performed",
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
            raise AdditionalPredictiveEvidencePlanCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise AdditionalPredictiveEvidencePlanCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise AdditionalPredictiveEvidencePlanCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_additional_predictive_evidence_plan_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate the additional evidence plan without authorizing execution."""
    if not isinstance(candidate, dict):
        raise AdditionalPredictiveEvidencePlanCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW,
        "candidate_status",
    )
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "execution_requires_operator_approval",
        "predictive_evidence_available_for_review",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
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
    ):
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
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
        _expect(candidate.get(field), expected, field)
    for field, expected in {
        "gaps_addressed": GAPS_ADDRESSED,
        "plan_phases": PLAN_PHASES,
        "planned_outputs": _planned_outputs(),
        "future_execution_gates": FUTURE_EXECUTION_GATES,
        "risk_controls": RISK_CONTROLS,
    }.items():
        value = candidate.get(field)
        if not isinstance(value, list) or not value:
            raise AdditionalPredictiveEvidencePlanCandidateError(f"{field} missing")
        _expect(value, expected, field)
    checklist = candidate.get("plan_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidencePlanCandidateError("plan_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "plan_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise AdditionalPredictiveEvidencePlanCandidateError(
            f"plan checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "plan_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("plan_summary"), expected_summary, "plan_summary")
    digest = candidate.get("additional_predictive_evidence_plan_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidencePlanCandidateError(
            "additional_predictive_evidence_plan_candidate_digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_plan_candidate_digest_v1(candidate),
        "additional_predictive_evidence_plan_candidate_digest",
    )
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_plan_candidate_digest": digest,
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": candidate[
            "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
        ],
        "predictive_usefulness_acceptance_readiness_candidate_digest": candidate[
            "predictive_usefulness_acceptance_readiness_candidate_digest"
        ],
        "ready_for_operator_review": candidate["plan_summary"]["ready_for_operator_review"],
        "ready_for_additional_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_additional_predictive_evidence_plan_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized additional predictive evidence plan candidate summary."""
    validation = validate_additional_predictive_evidence_plan_candidate_v1(candidate)
    summary = candidate["plan_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Plan Candidate Status",
        "",
        "## Title",
        "- Additional Predictive Evidence Plan Candidate v1.",
        "",
        "## Purpose",
        "- Plan additional research evidence required before any future predictive usefulness acceptance candidate may be considered.",
        "- This artifact does not execute experiments or authorize execution.",
        "",
        "## Source Readiness Evidence",
        f"- Acceptance readiness review package digest: `{candidate['predictive_usefulness_acceptance_readiness_candidate_review_package_digest']}`",
        f"- Acceptance readiness candidate digest: `{candidate['predictive_usefulness_acceptance_readiness_candidate_digest']}`",
        f"- Assessment review package digest: `{candidate['predictive_usefulness_assessment_candidate_review_package_digest']}`",
        f"- Assessment candidate digest: `{candidate['predictive_usefulness_assessment_candidate_digest']}`",
        f"- Candidate digest: `{validation['additional_predictive_evidence_plan_candidate_digest']}`",
        "",
        "## Gaps Addressed",
    ]
    lines.extend(f"- `{item}`" for item in candidate["gaps_addressed"])
    lines.extend(["", "## Plan Phases"])
    lines.extend(
        f"- `{phase['phase_id']}`: {phase['phase_name']}"
        for phase in candidate["plan_phases"]
    )
    lines.extend(["", "## Planned Outputs"])
    lines.extend(f"- `{item['output_id']}`: `{item['generation_status']}`" for item in candidate["planned_outputs"])
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_execution_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
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
            f"- additional_predictive_evidence_execution_authorized: `{candidate['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{candidate['additional_predictive_evidence_executed']}`",
            f"- predictive_experiment_rerun_authorized: `{candidate['predictive_experiment_rerun_authorized']}`",
            f"- predictive_experiment_rerun_performed: `{candidate['predictive_experiment_rerun_performed']}`",
            f"- walk_forward_rerun_performed: `{candidate['walk_forward_rerun_performed']}`",
            f"- new_strategy_scoring_performed: `{candidate['new_strategy_scoring_performed']}`",
            f"- trade_recommendations_generated: `{candidate['trade_recommendations_generated']}`",
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
            "- No additional predictive evidence execution was authorized or performed.",
            "- No predictive experiment, walk-forward, label, or feature-matrix rerun occurred.",
            "- No strategy scoring or trade recommendations were generated.",
            "- No predictive-usefulness or profitability acceptance occurred.",
            "- No runtime migration, paper trading, or broker execution was authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def write_additional_predictive_evidence_plan_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the additional predictive evidence plan candidate without overwriting output."""
    candidate = build_additional_predictive_evidence_plan_candidate_v1()
    validation = validate_additional_predictive_evidence_plan_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "additional_predictive_evidence_plan_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidencePlanCandidateError(
            "additional predictive evidence plan filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise AdditionalPredictiveEvidencePlanCandidateError(
            "additional predictive evidence plan output already exists"
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
