"""Offline operator review package for the predictive evidence scope expansion plan."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import predictive_evidence_scope_expansion_plan_candidate_service as plan_service


ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE = (
    "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_V1 = (
    "predictive_evidence_scope_expansion_plan_candidate_review_v1"
)
PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
)
PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_STATUS_BINDING = (
    "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_STATUS_BINDING"
)
PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_OBJECT_BINDING = (
    "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST = (
    "daddabc04829ac2379c4439220d018d8b3b3403c35edb469e95e7b24ea6bd13f"
)
EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_TOTAL = 57
EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_PASSED = 57
EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_BLOCKER_COUNT = 0

EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    plan_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST = (
    plan_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST = (
    plan_service.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    plan_service.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
)
EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    plan_service.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ASSESSMENT_CANDIDATE_DIGEST = plan_service.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    plan_service.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    plan_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    plan_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    plan_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    plan_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

ACCEPTANCE_READINESS_STATE_NOT_READY = plan_service.ACCEPTANCE_READINESS_STATE_NOT_READY
ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED = (
    plan_service.ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED
)
SCOPE_EXPANSION_OBJECTIVE = plan_service.SCOPE_EXPANSION_OBJECTIVE
PLANNED_NOT_AUTHORIZED = plan_service.PLANNED_NOT_AUTHORIZED
NOT_SELECTED = plan_service.NOT_SELECTED
NOT_CREATED = plan_service.NOT_CREATED
NOT_AUTHORIZED = plan_service.NOT_AUTHORIZED
NOT_BOUND = plan_service.NOT_BOUND
CRITERIA_DEFINED_SELECTION_NOT_PERFORMED = plan_service.CRITERIA_DEFINED_SELECTION_NOT_PERFORMED
PLANNED_NOT_GENERATED = plan_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = plan_service.RESEARCH_ONLY_NON_ACTIONABLE
SCOPE_GAPS_ADDRESSED = list(plan_service.SCOPE_GAPS_ADDRESSED)
EXPANSION_DIMENSIONS = deepcopy(plan_service.EXPANSION_DIMENSIONS)
TICKER_SELECTION_CRITERIA = list(plan_service.TICKER_SELECTION_CRITERIA)
FUTURE_TICKER_AUTHORITY_CHAIN = list(plan_service.FUTURE_TICKER_AUTHORITY_CHAIN)
PLANNED_OUTPUT_IDS = list(plan_service.PLANNED_OUTPUT_IDS)
FUTURE_GATES = list(plan_service.FUTURE_GATES)
RISK_CONTROLS = list(plan_service.RISK_CONTROLS)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_CHECK_IDS = [
    "scope_expansion_candidate_kind_matches",
    "scope_expansion_candidate_status_ready_for_review",
    "scope_expansion_candidate_digest_matches",
    "scope_expansion_candidate_checklist_zero_blockers",
    "additional_predictive_evidence_plan_review_digest_bound",
    "additional_predictive_evidence_plan_candidate_digest_bound",
    "acceptance_readiness_review_digest_bound",
    "acceptance_readiness_candidate_digest_bound",
    "predictive_experiment_results_review_digest_bound",
    "predictive_experiment_execution_digest_bound",
    "predictive_experiment_execution_approval_digest_bound",
    "predictive_experiment_plan_digest_bound",
    "predictive_experiment_plan_review_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "scope_expansion_objective_matches",
    "scope_expansion_mode_planned_not_authorized",
    "single_ticker_scope_gap_addressed",
    "generalization_gap_addressed",
    "dimension_count_10",
    "ticker_selection_policy_criteria_defined_selection_not_performed",
    "candidate_ticker_list_not_bound",
    "approved_expanded_ticker_universe_empty",
    "future_ticker_authority_chain_15_steps",
    "planned_outputs_10",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "future_gates_14",
    "risk_controls_14",
    "provider_requests_made_in_review_false",
    "live_ticker_validation_performed_false",
    "final_ticker_selection_performed_false",
    "ticker_universe_selection_candidate_created_false",
    "scope_expansion_authorized_false",
    "expanded_ticker_universe_approved_false",
    "new_ticker_authority_created_false",
    "new_ticker_acquisition_authorized_false",
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
    "no_scope_expansion_approval_artifact_created",
    "no_ticker_universe_selection_candidate_created",
    "no_expanded_ticker_universe_approval_created",
    "no_new_ticker_authority_created",
    "no_acquisition_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(ValueError):
    """Raised when the scope expansion plan review package is invalid."""


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
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            f"{field_name} must be false"
        )


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


def _ticker_selection_policy() -> dict[str, Any]:
    return {
        "ticker_selection_policy_status": CRITERIA_DEFINED_SELECTION_NOT_PERFORMED,
        "candidate_ticker_list_status": NOT_BOUND,
        "approved_expanded_ticker_universe": [],
        "selection_criteria": list(TICKER_SELECTION_CRITERIA),
        "minimum_additional_ticker_count": "planned",
        "target_additional_ticker_count_range": "5_to_12",
        "final_ticker_selection_performed": False,
        "live_ticker_validation_performed": False,
        "operator_approval_required_before_selection": True,
    }


def _future_ticker_authority_chain() -> list[dict[str, Any]]:
    return [
        {
            "step_number": index,
            "authority_step": step,
            "execution_required": False,
            "performed_in_this_task": False,
            "operator_approval_required_before_execution": True,
        }
        for index, step in enumerate(FUTURE_TICKER_AUTHORITY_CHAIN, start=1)
    ]


def _recorded_scope_expansion_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": (
            plan_service.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE
        ),
        "candidate_status": (
            plan_service.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST
        ),
        "plan_summary": {
            "total_checks": EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_TOTAL,
            "passed_checks": EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_PASSED,
            "failed_checks": EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_FAILED,
            "blocker_count": EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_BLOCKER_COUNT,
            "ready_for_operator_review": True,
            "ready_for_ticker_universe_selection_candidate": False,
            "ready_for_scope_expansion_execution": False,
            "ready_for_additional_evidence_execution_candidate": False,
            "ready_for_predictive_usefulness_acceptance_candidate": False,
        },
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
        ),
        "predictive_experiment_results_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_execution_digest": EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST,
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
        "scope_expansion_objective": SCOPE_EXPANSION_OBJECTIVE,
        "scope_expansion_mode": PLANNED_NOT_AUTHORIZED,
        "new_ticker_selection_status": NOT_SELECTED,
        "new_ticker_authority_status": NOT_CREATED,
        "new_data_acquisition_status": NOT_AUTHORIZED,
        "scope_gaps_addressed": list(SCOPE_GAPS_ADDRESSED),
        "expansion_dimensions": deepcopy(EXPANSION_DIMENSIONS),
        "expansion_dimension_count": len(EXPANSION_DIMENSIONS),
        "ticker_selection_policy_status": CRITERIA_DEFINED_SELECTION_NOT_PERFORMED,
        "candidate_ticker_list_status": NOT_BOUND,
        "approved_expanded_ticker_universe": [],
        "ticker_selection_policy": _ticker_selection_policy(),
        "minimum_additional_ticker_count": "planned",
        "target_additional_ticker_count_range": "5_to_12",
        "future_ticker_authority_chain": _future_ticker_authority_chain(),
        "future_ticker_authority_chain_step_count": len(FUTURE_TICKER_AUTHORITY_CHAIN),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
        "future_gates": list(FUTURE_GATES),
        "future_gate_count": len(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "risk_control_count": len(RISK_CONTROLS),
    }


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            _recorded_scope_expansion_candidate(),
            PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_STATUS_BINDING,
        )
    plan_service.validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)
    return deepcopy(candidate), PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_OBJECT_BINDING


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["plan_summary"]
    return {
        "artifact_kind": (
            ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE
        ),
        "schema_version": (
            SCHEMA_VERSION_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_V1
        ),
        "review_status": (
            PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
        ),
        "scope_expansion_candidate_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_ticker_validation_performed": False,
        "final_ticker_selection_performed": False,
        "ticker_universe_selection_candidate_created": False,
        "scope_expansion_authorized": False,
        "expanded_ticker_universe_approved": False,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
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
        "ready_for_ticker_universe_selection_candidate": False,
        "ready_for_scope_expansion_execution": False,
        "ready_for_additional_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "scope_expansion_approval_artifact_created": False,
        "ticker_universe_selection_candidate_artifact_created": False,
        "expanded_ticker_universe_approval_artifact_created": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "reviewed_scope_expansion_candidate_kind": candidate["artifact_kind"],
        "reviewed_scope_expansion_candidate_status": candidate["candidate_status"],
        "reviewed_scope_expansion_candidate_digest": candidate[
            "predictive_evidence_scope_expansion_plan_candidate_digest"
        ],
        "reviewed_scope_expansion_candidate_checklist_total": summary["total_checks"],
        "reviewed_scope_expansion_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_scope_expansion_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_scope_expansion_candidate_blocker_count": summary["blocker_count"],
        "additional_predictive_evidence_plan_candidate_review_package_digest": candidate[
            "additional_predictive_evidence_plan_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_plan_candidate_digest": candidate[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            candidate["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"]
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": candidate[
            "predictive_usefulness_acceptance_readiness_candidate_digest"
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
        "predictive_experiment_plan_digest": candidate["predictive_experiment_plan_digest"],
        "predictive_experiment_plan_review_package_digest": candidate[
            "predictive_experiment_plan_review_package_digest"
        ],
        "swing_registry_approval_digest": candidate["swing_registry_approval_digest"],
        "position_swing_registry_approval_digest": candidate[
            "position_swing_registry_approval_digest"
        ],
        "scope_expansion_objective": candidate["scope_expansion_objective"],
        "scope_expansion_mode": candidate["scope_expansion_mode"],
        "new_ticker_selection_status": candidate["new_ticker_selection_status"],
        "new_ticker_authority_status": candidate["new_ticker_authority_status"],
        "new_data_acquisition_status": candidate["new_data_acquisition_status"],
        "scope_gaps_addressed": list(candidate["scope_gaps_addressed"]),
        "expansion_dimensions": deepcopy(candidate["expansion_dimensions"]),
        "dimension_count": len(candidate["expansion_dimensions"]),
        "ticker_selection_policy_status": candidate["ticker_selection_policy_status"],
        "candidate_ticker_list_status": candidate["candidate_ticker_list_status"],
        "approved_expanded_ticker_universe": list(candidate["approved_expanded_ticker_universe"]),
        "ticker_selection_policy": deepcopy(candidate["ticker_selection_policy"]),
        "minimum_additional_ticker_count": candidate["minimum_additional_ticker_count"],
        "target_additional_ticker_count_range": candidate["target_additional_ticker_count_range"],
        "future_ticker_authority_chain": deepcopy(candidate["future_ticker_authority_chain"]),
        "future_ticker_authority_chain_step_count": candidate[
            "future_ticker_authority_chain_step_count"
        ],
        "planned_outputs": deepcopy(candidate["planned_outputs"]),
        "planned_output_count": len(candidate["planned_outputs"]),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "future_gates": list(candidate["future_gates"]),
        "future_gate_count": len(candidate["future_gates"]),
        "risk_controls": list(candidate["risk_controls"]),
        "risk_control_count": len(candidate["risk_controls"]),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    planned_outputs = review_package.get("planned_outputs", [])
    gaps = set(review_package.get("scope_gaps_addressed", []))
    return [
        _check("scope_expansion_candidate_kind_matches", plan_service.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE, review_package.get("reviewed_scope_expansion_candidate_kind")),
        _check("scope_expansion_candidate_status_ready_for_review", plan_service.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_scope_expansion_candidate_status")),
        _check("scope_expansion_candidate_digest_matches", EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST, review_package.get("reviewed_scope_expansion_candidate_digest")),
        _check("scope_expansion_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_scope_expansion_candidate_blocker_count")),
        _check("additional_predictive_evidence_plan_review_digest_bound", EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("additional_predictive_evidence_plan_candidate_review_package_digest")),
        _check("additional_predictive_evidence_plan_candidate_digest_bound", EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST, review_package.get("additional_predictive_evidence_plan_candidate_digest")),
        _check("acceptance_readiness_review_digest_bound", EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_usefulness_acceptance_readiness_candidate_review_package_digest")),
        _check("acceptance_readiness_candidate_digest_bound", EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST, review_package.get("predictive_usefulness_acceptance_readiness_candidate_digest")),
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_experiment_results_review_package_digest")),
        _check("predictive_experiment_execution_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST, review_package.get("predictive_experiment_execution_digest")),
        _check("predictive_experiment_execution_approval_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST, review_package.get("predictive_experiment_execution_approval_digest")),
        _check("predictive_experiment_plan_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST, review_package.get("predictive_experiment_plan_digest")),
        _check("predictive_experiment_plan_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_experiment_plan_review_package_digest")),
        _check("swing_registry_approval_digest_bound", EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("swing_registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, review_package.get("position_swing_registry_approval_digest")),
        _check("scope_expansion_objective_matches", SCOPE_EXPANSION_OBJECTIVE, review_package.get("scope_expansion_objective")),
        _check("scope_expansion_mode_planned_not_authorized", PLANNED_NOT_AUTHORIZED, review_package.get("scope_expansion_mode")),
        _check("single_ticker_scope_gap_addressed", True, "single_ticker_scope" in gaps),
        _check("generalization_gap_addressed", True, "no_multi_ticker_or_out_of_domain_generalization" in gaps),
        _check("dimension_count_10", 10, review_package.get("dimension_count")),
        _check("ticker_selection_policy_criteria_defined_selection_not_performed", CRITERIA_DEFINED_SELECTION_NOT_PERFORMED, review_package.get("ticker_selection_policy_status")),
        _check("candidate_ticker_list_not_bound", NOT_BOUND, review_package.get("candidate_ticker_list_status")),
        _check("approved_expanded_ticker_universe_empty", [], review_package.get("approved_expanded_ticker_universe")),
        _check("future_ticker_authority_chain_15_steps", 15, review_package.get("future_ticker_authority_chain_step_count")),
        _check("planned_outputs_10", 10, review_package.get("planned_output_count")),
        _check("planned_outputs_not_generated", True, all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in planned_outputs)),
        _check("planned_outputs_research_only", True, all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned_outputs)),
        _check("future_gates_14", 14, review_package.get("future_gate_count")),
        _check("risk_controls_14", 14, review_package.get("risk_control_count")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("live_ticker_validation_performed_false", False, review_package.get("live_ticker_validation_performed")),
        _check("final_ticker_selection_performed_false", False, review_package.get("final_ticker_selection_performed")),
        _check("ticker_universe_selection_candidate_created_false", False, review_package.get("ticker_universe_selection_candidate_created")),
        _check("scope_expansion_authorized_false", False, review_package.get("scope_expansion_authorized")),
        _check("expanded_ticker_universe_approved_false", False, review_package.get("expanded_ticker_universe_approved")),
        _check("new_ticker_authority_created_false", False, review_package.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, review_package.get("new_ticker_acquisition_authorized")),
        _check("additional_predictive_evidence_execution_authorized_false", False, review_package.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, review_package.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, review_package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, review_package.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, review_package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, review_package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, review_package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, review_package.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, review_package.get("predictive_usefulness_acceptance_candidate_created")),
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
        _check("no_scope_expansion_approval_artifact_created", False, review_package.get("scope_expansion_approval_artifact_created")),
        _check("no_ticker_universe_selection_candidate_created", False, review_package.get("ticker_universe_selection_candidate_artifact_created")),
        _check("no_expanded_ticker_universe_approval_created", False, review_package.get("expanded_ticker_universe_approval_artifact_created")),
        _check("no_new_ticker_authority_created", False, review_package.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_artifact_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
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
        "ready_for_ticker_universe_selection_candidate": False,
        "ready_for_scope_expansion_execution": False,
        "ready_for_additional_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_evidence_scope_expansion_plan_candidate_review_package_digest", None)
    return payload


def predictive_evidence_scope_expansion_plan_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the scope expansion review package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for the scope expansion plan."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] = (
        predictive_evidence_scope_expansion_plan_candidate_review_package_digest_v1(
            review_package
        )
    )
    validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_APPROVED",
            "EXPANDED_TICKER_UNIVERSE_APPROVED",
            "TICKER_UNIVERSE_SELECTION_CANDIDATE",
            "NEW_TICKER_AUTHORITY_APPROVED",
            "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
            "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
            "TRADE_RECOMMENDATIONS",
        }:
            raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made_in_review",
            "live_ticker_validation_performed",
            "final_ticker_selection_performed",
            "ticker_universe_selection_candidate_created",
            "scope_expansion_authorized",
            "expanded_ticker_universe_approved",
            "new_ticker_authority_created",
            "new_ticker_acquisition_authorized",
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
            "ready_for_ticker_universe_selection_candidate",
            "ready_for_scope_expansion_execution",
            "ready_for_additional_evidence_execution_candidate",
            "ready_for_predictive_usefulness_acceptance_candidate",
            "scope_expansion_approval_artifact_created",
            "ticker_universe_selection_candidate_artifact_created",
            "expanded_ticker_universe_approval_artifact_created",
            "new_ticker_authority_artifact_created",
            "acquisition_authorization_artifact_created",
            "predictive_usefulness_acceptance_artifact_created",
            "profitability_acceptance_artifact_created",
            "runtime_migration_approval_artifact_created",
        } and value is True:
            raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if key == "approved_expanded_ticker_universe" and value:
            raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
                f"{current_path} must be empty"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the review package without authorizing scope expansion."""
    if not isinstance(review_package, dict):
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("scope_expansion_candidate_binding_mode") not in {
        PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_STATUS_BINDING,
        PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_OBJECT_BINDING,
    }:
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            "scope_expansion_candidate_binding_mode mismatch"
        )
    for field in ("operator_decision_required", "created_offline", "research_only"):
        _expect_true(review_package.get(field), field)
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in (
        "provider_requests_made_in_review",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "ticker_universe_selection_candidate_created",
        "scope_expansion_authorized",
        "expanded_ticker_universe_approved",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
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
        "ready_for_ticker_universe_selection_candidate",
        "ready_for_scope_expansion_execution",
        "ready_for_additional_evidence_execution_candidate",
        "ready_for_predictive_usefulness_acceptance_candidate",
        "scope_expansion_approval_artifact_created",
        "ticker_universe_selection_candidate_artifact_created",
        "expanded_ticker_universe_approval_artifact_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_scope_expansion_candidate_kind": (
            plan_service.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE
        ),
        "reviewed_scope_expansion_candidate_status": (
            plan_service.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_scope_expansion_candidate_digest": (
            EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST
        ),
        "reviewed_scope_expansion_candidate_checklist_total": (
            EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_TOTAL
        ),
        "reviewed_scope_expansion_candidate_checklist_passed": (
            EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_PASSED
        ),
        "reviewed_scope_expansion_candidate_checklist_failed": (
            EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_CHECKLIST_FAILED
        ),
        "reviewed_scope_expansion_candidate_blocker_count": (
            EXPECTED_REVIEWED_SCOPE_EXPANSION_CANDIDATE_BLOCKER_COUNT
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
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
        "scope_expansion_objective": SCOPE_EXPANSION_OBJECTIVE,
        "scope_expansion_mode": PLANNED_NOT_AUTHORIZED,
        "new_ticker_selection_status": NOT_SELECTED,
        "new_ticker_authority_status": NOT_CREATED,
        "new_data_acquisition_status": NOT_AUTHORIZED,
        "scope_gaps_addressed": SCOPE_GAPS_ADDRESSED,
        "ticker_selection_policy_status": CRITERIA_DEFINED_SELECTION_NOT_PERFORMED,
        "candidate_ticker_list_status": NOT_BOUND,
        "approved_expanded_ticker_universe": [],
        "ticker_selection_policy": _ticker_selection_policy(),
        "minimum_additional_ticker_count": "planned",
        "target_additional_ticker_count_range": "5_to_12",
    }.items():
        _expect(review_package.get(field), expected, field)
    for field, expected in {
        "expansion_dimensions": EXPANSION_DIMENSIONS,
        "future_ticker_authority_chain": _future_ticker_authority_chain(),
        "planned_outputs": _planned_outputs(),
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
    }.items():
        value = review_package.get(field)
        if not isinstance(value, list) or not value:
            raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
                f"{field} missing"
            )
        _expect(value, expected, field)
    for field, expected in {
        "dimension_count": 10,
        "future_ticker_authority_chain_step_count": 15,
        "planned_output_count": 10,
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "future_gate_count": 14,
        "risk_control_count": 14,
    }.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
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
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            "predictive_evidence_scope_expansion_plan_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        predictive_evidence_scope_expansion_plan_candidate_review_package_digest_v1(
            review_package
        ),
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": digest,
        "reviewed_scope_expansion_candidate_digest": review_package[
            "reviewed_scope_expansion_candidate_digest"
        ],
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            review_package["additional_predictive_evidence_plan_candidate_review_package_digest"]
        ),
        "additional_predictive_evidence_plan_candidate_digest": review_package[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "scope_expansion_objective": review_package["scope_expansion_objective"],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
        "ready_for_ticker_universe_selection_candidate": False,
        "ready_for_scope_expansion_execution": False,
        "ready_for_additional_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_predictive_evidence_scope_expansion_plan_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized predictive evidence scope expansion plan review summary."""
    validation = validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Predictive Evidence Scope Expansion Plan Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Predictive Evidence Scope Expansion Plan Candidate Operator Review Package v1.",
        "",
        "## Reviewed Predictive Evidence Scope Expansion Plan",
        f"- Candidate kind: `{review_package['reviewed_scope_expansion_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_scope_expansion_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_scope_expansion_candidate_digest']}`",
        f"- Review package digest: `{validation['predictive_evidence_scope_expansion_plan_candidate_review_package_digest']}`",
        "",
        "## Source Evidence",
        f"- Additional predictive evidence plan review package digest: `{review_package['additional_predictive_evidence_plan_candidate_review_package_digest']}`",
        f"- Additional predictive evidence plan candidate digest: `{review_package['additional_predictive_evidence_plan_candidate_digest']}`",
        f"- Acceptance readiness review package digest: `{review_package['predictive_usefulness_acceptance_readiness_candidate_review_package_digest']}`",
        f"- Acceptance readiness candidate digest: `{review_package['predictive_usefulness_acceptance_readiness_candidate_digest']}`",
        "",
        "## Scope Expansion Objective",
        f"- scope_expansion_objective: `{review_package['scope_expansion_objective']}`",
        f"- scope_expansion_mode: `{review_package['scope_expansion_mode']}`",
        f"- new_ticker_selection_status: `{review_package['new_ticker_selection_status']}`",
        f"- new_ticker_authority_status: `{review_package['new_ticker_authority_status']}`",
        f"- new_data_acquisition_status: `{review_package['new_data_acquisition_status']}`",
        "",
        "## Expansion Dimensions",
    ]
    lines.extend(
        f"- `{dimension['dimension_id']}`: {dimension['dimension_name']}"
        for dimension in review_package["expansion_dimensions"]
    )
    lines.extend(
        [
            "",
            "## Ticker Selection Policy",
            f"- ticker_selection_policy_status: `{review_package['ticker_selection_policy_status']}`",
            f"- candidate_ticker_list_status: `{review_package['candidate_ticker_list_status']}`",
            f"- approved_expanded_ticker_universe: `{review_package['approved_expanded_ticker_universe']}`",
            f"- target_additional_ticker_count_range: `{review_package['target_additional_ticker_count_range']}`",
            "",
            "## Required Authority Chain for Future Tickers",
        ]
    )
    lines.extend(
        f"- `{step['step_number']}`: `{step['authority_step']}`"
        for step in review_package["future_ticker_authority_chain"]
    )
    lines.extend(["", "## Planned Outputs"])
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`, `{item['actionability_label']}`"
        for item in review_package["planned_outputs"]
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
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
            f"- live_ticker_validation_performed: `{review_package['live_ticker_validation_performed']}`",
            f"- final_ticker_selection_performed: `{review_package['final_ticker_selection_performed']}`",
            f"- ticker_universe_selection_candidate_created: `{review_package['ticker_universe_selection_candidate_created']}`",
            f"- scope_expansion_authorized: `{review_package['scope_expansion_authorized']}`",
            f"- expanded_ticker_universe_approved: `{review_package['expanded_ticker_universe_approved']}`",
            f"- new_ticker_authority_created: `{review_package['new_ticker_authority_created']}`",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            f"- additional_predictive_evidence_execution_authorized: `{review_package['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{review_package['additional_predictive_evidence_executed']}`",
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
            f"- ready_for_operator_assessment: `{summary['ready_for_operator_assessment']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No ticker selection, live ticker validation, ticker authority, or acquisition occurred.",
            "- No scope expansion approval or ticker universe selection candidate was created.",
            "- No additional predictive evidence execution was authorized or performed.",
            "- No predictive experiment, walk-forward, label, or feature-matrix rerun occurred.",
            "- No strategy scoring or trade recommendations were generated.",
            "- No predictive-usefulness or profitability acceptance occurred.",
            "- No runtime migration, paper trading, or broker execution was authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the scope expansion plan review package without overwriting output."""
    review_package = build_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "predictive_evidence_scope_expansion_plan_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            "predictive evidence scope expansion plan review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError(
            "predictive evidence scope expansion plan review output already exists"
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
