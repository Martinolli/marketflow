"""Offline predictive evidence scope expansion plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    additional_predictive_evidence_plan_candidate_operator_review_service as additional_review,
)


ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE = (
    "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_V1 = (
    "predictive_evidence_scope_expansion_plan_candidate_v1"
)
PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW = (
    "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "24b19efc1fdb4cbf64c02f15011becd1872301efe596a4d8bb7989f8be299b8a"
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST = (
    additional_review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST = (
    additional_review.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    additional_review.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
)
EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    additional_review.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ASSESSMENT_CANDIDATE_DIGEST = (
    additional_review.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    additional_review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    additional_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    additional_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST = (
    additional_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST = (
    additional_review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = additional_review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    additional_review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

ACCEPTANCE_READINESS_STATE_NOT_READY = additional_review.ACCEPTANCE_READINESS_STATE_NOT_READY
ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED = (
    additional_review.ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED
)
PLANNED_NOT_AUTHORIZED = "PLANNED_NOT_AUTHORIZED"
NOT_SELECTED = "NOT_SELECTED"
NOT_CREATED = "NOT_CREATED"
NOT_AUTHORIZED = additional_review.NOT_AUTHORIZED
NOT_BOUND = "NOT_BOUND"
CRITERIA_DEFINED_SELECTION_NOT_PERFORMED = "CRITERIA_DEFINED_SELECTION_NOT_PERFORMED"
PLANNED_NOT_GENERATED = additional_review.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = additional_review.RESEARCH_ONLY_NON_ACTIONABLE
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SCOPE_EXPANSION_OBJECTIVE = "EXPAND_PREDICTIVE_EVIDENCE_BEYOND_SINGLE_TICKER_AAPL"
SCOPE_GAPS_ADDRESSED = [
    "single_ticker_scope",
    "no_multi_ticker_or_out_of_domain_generalization",
    "single_asset_class_scope_if_applicable",
]

EXPANSION_DIMENSIONS = [
    {
        "dimension_id": "ticker_count_expansion",
        "dimension_name": "Ticker count expansion",
        "purpose": "Plan future evidence beyond the current single AAPL ticker scope.",
        "addresses_gap": ["single_ticker_scope"],
        "selection_criteria": [
            "operator-approved ticker universe candidate",
            "complete per-ticker authority chain before acquisition",
        ],
        "planned_evidence_output": "ticker_selection_criteria_report",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "sector_or_industry_diversity",
        "dimension_name": "Sector or industry diversity",
        "purpose": "Plan future cross-sector checks before generalization is reassessed.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["documented sector or industry labels", "operator scope review"],
        "planned_evidence_output": "expansion_dimension_matrix",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "liquidity_regime_diversity",
        "dimension_name": "Liquidity regime diversity",
        "purpose": "Plan evidence across liquidity profiles without selecting tickers now.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["predefined liquidity bands", "file availability verification"],
        "planned_evidence_output": "dataset_replication_requirements_report",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "volatility_regime_diversity",
        "dimension_name": "Volatility regime diversity",
        "purpose": "Plan checks across volatility regimes before future usefulness review.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["predefined volatility bands", "research-only interpretation"],
        "planned_evidence_output": "generalization_evidence_requirements_report",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "market_cap_or_size_diversity",
        "dimension_name": "Market cap or size diversity",
        "purpose": "Plan future size-profile coverage for out-of-domain evidence.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["predefined size buckets", "approved identity segment"],
        "planned_evidence_output": "expansion_dimension_matrix",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "price_level_diversity",
        "dimension_name": "Price level diversity",
        "purpose": "Plan price-level variation checks for future evidence replication.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["predefined price-level buckets", "frozen canonical datasets"],
        "planned_evidence_output": "dataset_replication_requirements_report",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "volume_profile_diversity",
        "dimension_name": "Volume profile diversity",
        "purpose": "Plan volume-profile coverage without authorizing acquisition.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["predefined volume buckets", "research registry approval"],
        "planned_evidence_output": "expansion_dimension_matrix",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "time_period_or_regime_extension",
        "dimension_name": "Time period or regime extension",
        "purpose": "Plan future time-regime coverage if operator authorizes new evidence.",
        "addresses_gap": ["single_ticker_scope", "no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["documented date scope", "provider authority if new data is required"],
        "planned_evidence_output": "generalization_evidence_requirements_report",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "dataset_profile_replication",
        "dimension_name": "Dataset profile replication",
        "purpose": "Plan replication across SWING and POSITION_SWING research profiles.",
        "addresses_gap": ["single_asset_class_scope_if_applicable"],
        "selection_criteria": ["SWING freeze", "POSITION_SWING freeze", "file availability verification"],
        "planned_evidence_output": "dataset_replication_requirements_report",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
    {
        "dimension_id": "out_of_domain_generalization",
        "dimension_name": "Out-of-domain generalization",
        "purpose": "Plan explicit out-of-domain evidence before any usefulness acceptance candidate.",
        "addresses_gap": ["no_multi_ticker_or_out_of_domain_generalization"],
        "selection_criteria": ["operator-defined out-of-domain scope", "separate acceptance readiness reassessment"],
        "planned_evidence_output": "generalization_evidence_requirements_report",
        "execution_required": False,
        "operator_approval_required_before_execution": True,
    },
]

TICKER_SELECTION_CRITERIA = [
    "must_be_common_stock_or_explicitly_approved_security_type",
    "must_have_valid_identity_segment",
    "must_have_calendar_mapping",
    "must_have_split_event_audit",
    "must_have_dividend_event_audit_or_explicit_no_dividend_policy",
    "must_have_acquisition_generation_authority",
    "must_have_canonical_dataset_freeze_for_SWING",
    "must_have_canonical_dataset_freeze_for_POSITION_SWING",
    "must_have_research_registry_approval",
    "must_have_file_availability_verification",
    "must_remain_research_only",
    "must_not_authorize_runtime_or_trading",
]

FUTURE_TICKER_AUTHORITY_CHAIN = [
    "identity_segment_candidate_review_freeze",
    "exchange_calendar_candidate_review_freeze_or_valid_reuse",
    "split_event_audit_candidate_provider_evidence_review_freeze",
    "dividend_event_audit_candidate_provider_evidence_review_freeze",
    "acquisition_generation_candidate_live_generation_triage_freeze",
    "canonical_dataset_candidate_review_freeze_for_SWING",
    "registry_approval_for_SWING_research_dataset",
    "canonical_dataset_candidate_review_freeze_for_POSITION_SWING",
    "registry_approval_for_POSITION_SWING_research_dataset",
    "read_only_registry_discovery",
    "dataset_file_availability_verification",
    "research_applicability_campaign_plan_execution_review",
    "predictive_experiment_plan_execution_review",
    "predictive_usefulness_assessment",
    "acceptance_readiness_reassessment",
]

PLANNED_OUTPUT_IDS = [
    "scope_expansion_plan_manifest",
    "ticker_selection_criteria_report",
    "expansion_dimension_matrix",
    "future_ticker_authority_chain_template",
    "scope_expansion_risk_register",
    "dataset_replication_requirements_report",
    "multi_ticker_research_campaign_plan_template",
    "generalization_evidence_requirements_report",
    "operator_decision_gate_plan",
    "non_runtime_boundary_confirmation_plan",
]

FUTURE_GATES = [
    "scope_expansion_plan_operator_review",
    "ticker_universe_selection_candidate",
    "ticker_universe_selection_operator_review",
    "ticker_universe_selection_approval_ceremony",
    "identity_authority_chain_per_selected_ticker",
    "corporate_action_audit_chain_per_selected_ticker",
    "acquisition_generation_chain_per_selected_ticker",
    "canonical_dataset_chain_per_selected_ticker",
    "research_registry_approval_per_selected_ticker",
    "dataset_file_availability_verification_per_selected_ticker",
    "multi_ticker_research_campaign_execution_candidate",
    "multi_ticker_predictive_experiment_execution_candidate",
    "multi_ticker_predictive_usefulness_assessment",
    "acceptance_readiness_reassessment_after_expansion",
]

RISK_CONTROLS = [
    "no_provider_refresh_without_authority",
    "no_ticker_selection_without_operator_review",
    "no_new_ticker_inclusion_without_identity_authority",
    "no_acquisition_without_corporate_action_audits",
    "no_registry_approval_without_frozen_dataset",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "no_predictive_usefulness_acceptance_in_scope_planning",
    "no_profitability_acceptance_in_scope_planning",
    "all_outputs_labeled_research_only",
    "operator_approval_required_before_any_new_ticker_chain_begins",
]

REQUIRED_CHECK_IDS = [
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
    "readiness_state_not_ready",
    "predictive_evidence_sufficient_for_acceptance_false",
    "ready_for_acceptance_candidate_false",
    "scope_expansion_objective_defined",
    "single_ticker_scope_gap_addressed",
    "generalization_gap_addressed",
    "expansion_dimensions_defined",
    "ticker_selection_policy_defined",
    "final_ticker_selection_not_performed",
    "approved_expanded_ticker_universe_empty",
    "future_ticker_authority_chain_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "live_ticker_validation_performed_false",
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
]


class PredictiveEvidenceScopeExpansionPlanCandidateError(ValueError):
    """Raised when the predictive evidence scope expansion plan candidate is invalid."""


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
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(f"{field_name} must be false")


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


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_V1,
        "candidate_status": PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_ticker_validation_performed": False,
        "final_ticker_selection_performed": False,
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
        "operator_review_required": True,
        "scope_expansion_execution_requires_operator_approval": True,
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


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    planned_outputs = candidate.get("planned_outputs", [])
    gaps = set(candidate.get("scope_gaps_addressed", []))
    return [
        _check("additional_predictive_evidence_plan_review_digest_bound", EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("additional_predictive_evidence_plan_candidate_review_package_digest")),
        _check("additional_predictive_evidence_plan_candidate_digest_bound", EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST, candidate.get("additional_predictive_evidence_plan_candidate_digest")),
        _check("acceptance_readiness_review_digest_bound", EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_usefulness_acceptance_readiness_candidate_review_package_digest")),
        _check("acceptance_readiness_candidate_digest_bound", EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST, candidate.get("predictive_usefulness_acceptance_readiness_candidate_digest")),
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
        _check("scope_expansion_objective_defined", SCOPE_EXPANSION_OBJECTIVE, candidate.get("scope_expansion_objective")),
        _check("single_ticker_scope_gap_addressed", True, "single_ticker_scope" in gaps),
        _check("generalization_gap_addressed", True, "no_multi_ticker_or_out_of_domain_generalization" in gaps),
        _check("expansion_dimensions_defined", EXPANSION_DIMENSIONS, candidate.get("expansion_dimensions")),
        _check("ticker_selection_policy_defined", _ticker_selection_policy(), candidate.get("ticker_selection_policy")),
        _check("final_ticker_selection_not_performed", False, candidate.get("final_ticker_selection_performed")),
        _check("approved_expanded_ticker_universe_empty", [], candidate.get("approved_expanded_ticker_universe")),
        _check("future_ticker_authority_chain_defined", _future_ticker_authority_chain(), candidate.get("future_ticker_authority_chain")),
        _check("planned_outputs_not_generated", True, all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in planned_outputs)),
        _check("planned_outputs_research_only", True, all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned_outputs)),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("live_ticker_validation_performed_false", False, candidate.get("live_ticker_validation_performed")),
        _check("scope_expansion_authorized_false", False, candidate.get("scope_expansion_authorized")),
        _check("expanded_ticker_universe_approved_false", False, candidate.get("expanded_ticker_universe_approved")),
        _check("new_ticker_authority_created_false", False, candidate.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, candidate.get("new_ticker_acquisition_authorized")),
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
        "ready_for_ticker_universe_selection_candidate": False,
        "ready_for_scope_expansion_execution": False,
        "ready_for_additional_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("predictive_evidence_scope_expansion_plan_candidate_digest", None)
    return payload


def predictive_evidence_scope_expansion_plan_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the scope expansion plan."""
    return semantic_digest(_digest_payload(candidate))


def build_predictive_evidence_scope_expansion_plan_candidate_v1() -> dict[str, Any]:
    """Build an offline planning artifact for future predictive evidence scope expansion."""
    candidate = _base_candidate()
    candidate["plan_checklist"] = _checklist(candidate)
    candidate["plan_summary"] = _summary(candidate["plan_checklist"])
    candidate["predictive_evidence_scope_expansion_plan_candidate_digest"] = (
        predictive_evidence_scope_expansion_plan_candidate_digest_v1(candidate)
    )
    validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_APPROVED",
            "EXPANDED_TICKER_UNIVERSE_APPROVED",
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
            raise PredictiveEvidenceScopeExpansionPlanCandidateError(
                f"{current_path} must not emit {value}"
            )
        if key in {
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
            "provider_requests_made",
            "live_ticker_validation_performed",
            "final_ticker_selection_performed",
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
            raise PredictiveEvidenceScopeExpansionPlanCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PredictiveEvidenceScopeExpansionPlanCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveEvidenceScopeExpansionPlanCandidateError(
                f"{current_path} must not be accepted"
            )
        if key == "approved_expanded_ticker_universe" and value:
            raise PredictiveEvidenceScopeExpansionPlanCandidateError(
                f"{current_path} must be empty"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_evidence_scope_expansion_plan_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate the scope expansion plan without authorizing scope expansion."""
    if not isinstance(candidate, dict):
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW,
        "candidate_status",
    )
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "scope_expansion_execution_requires_operator_approval",
        "predictive_evidence_available_for_review",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
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
        "scope_expansion_objective": SCOPE_EXPANSION_OBJECTIVE,
        "scope_expansion_mode": PLANNED_NOT_AUTHORIZED,
        "new_ticker_selection_status": NOT_SELECTED,
        "new_ticker_authority_status": NOT_CREATED,
        "new_data_acquisition_status": NOT_AUTHORIZED,
        "scope_gaps_addressed": SCOPE_GAPS_ADDRESSED,
        "ticker_selection_policy_status": CRITERIA_DEFINED_SELECTION_NOT_PERFORMED,
        "candidate_ticker_list_status": NOT_BOUND,
        "approved_expanded_ticker_universe": [],
        "minimum_additional_ticker_count": "planned",
        "target_additional_ticker_count_range": "5_to_12",
    }.items():
        _expect(candidate.get(field), expected, field)
    for field, expected in {
        "expansion_dimensions": EXPANSION_DIMENSIONS,
        "ticker_selection_policy": _ticker_selection_policy(),
        "future_ticker_authority_chain": _future_ticker_authority_chain(),
        "planned_outputs": _planned_outputs(),
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
    }.items():
        value = candidate.get(field)
        if not isinstance(value, list | dict) or not value:
            raise PredictiveEvidenceScopeExpansionPlanCandidateError(f"{field} missing")
        _expect(value, expected, field)
    for field, expected in {
        "expansion_dimension_count": len(EXPANSION_DIMENSIONS),
        "future_ticker_authority_chain_step_count": len(FUTURE_TICKER_AUTHORITY_CHAIN),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
        "future_gate_count": len(FUTURE_GATES),
        "risk_control_count": len(RISK_CONTROLS),
    }.items():
        _expect(candidate.get(field), expected, field)
    checklist = candidate.get("plan_checklist")
    if not isinstance(checklist, list):
        raise PredictiveEvidenceScopeExpansionPlanCandidateError("plan_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "plan_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(
            f"plan checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "plan_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("plan_summary"), expected_summary, "plan_summary")
    digest = candidate.get("predictive_evidence_scope_expansion_plan_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(
            "predictive_evidence_scope_expansion_plan_candidate_digest missing"
        )
    _expect(
        digest,
        predictive_evidence_scope_expansion_plan_candidate_digest_v1(candidate),
        "predictive_evidence_scope_expansion_plan_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "predictive_evidence_scope_expansion_plan_candidate_digest": digest,
        "additional_predictive_evidence_plan_candidate_review_package_digest": candidate[
            "additional_predictive_evidence_plan_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_plan_candidate_digest": candidate[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "scope_expansion_objective": SCOPE_EXPANSION_OBJECTIVE,
        "ready_for_operator_review": candidate["plan_summary"]["ready_for_operator_review"],
        "ready_for_ticker_universe_selection_candidate": False,
        "ready_for_scope_expansion_execution": False,
        "ready_for_additional_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_predictive_evidence_scope_expansion_plan_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized predictive evidence scope expansion plan summary."""
    validation = validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)
    summary = candidate["plan_summary"]
    lines = [
        "# MarketFlow Predictive Evidence Scope Expansion Plan Candidate Status",
        "",
        "## Title",
        "- Predictive Evidence Scope Expansion Plan Candidate v1.",
        "",
        "## Purpose",
        "- Plan future evidence scope expansion beyond the current single-ticker AAPL evidence.",
        "- This artifact does not select tickers, create ticker authority, acquire data, or authorize execution.",
        "",
        "## Source Evidence",
        f"- Additional predictive evidence plan review package digest: `{candidate['additional_predictive_evidence_plan_candidate_review_package_digest']}`",
        f"- Additional predictive evidence plan candidate digest: `{candidate['additional_predictive_evidence_plan_candidate_digest']}`",
        f"- Acceptance readiness review package digest: `{candidate['predictive_usefulness_acceptance_readiness_candidate_review_package_digest']}`",
        f"- Acceptance readiness candidate digest: `{candidate['predictive_usefulness_acceptance_readiness_candidate_digest']}`",
        f"- Candidate digest: `{validation['predictive_evidence_scope_expansion_plan_candidate_digest']}`",
        "",
        "## Scope Expansion Objective",
        f"- scope_expansion_objective: `{candidate['scope_expansion_objective']}`",
        f"- scope_expansion_mode: `{candidate['scope_expansion_mode']}`",
        f"- new_ticker_selection_status: `{candidate['new_ticker_selection_status']}`",
        f"- new_ticker_authority_status: `{candidate['new_ticker_authority_status']}`",
        f"- new_data_acquisition_status: `{candidate['new_data_acquisition_status']}`",
        "",
        "## Expansion Dimensions",
    ]
    lines.extend(
        f"- `{dimension['dimension_id']}`: {dimension['dimension_name']}"
        for dimension in candidate["expansion_dimensions"]
    )
    lines.extend(
        [
            "",
            "## Ticker Selection Policy",
            f"- ticker_selection_policy_status: `{candidate['ticker_selection_policy_status']}`",
            f"- candidate_ticker_list_status: `{candidate['candidate_ticker_list_status']}`",
            f"- approved_expanded_ticker_universe: `{candidate['approved_expanded_ticker_universe']}`",
        ]
    )
    lines.extend(
        f"- `{criterion}`" for criterion in candidate["ticker_selection_policy"]["selection_criteria"]
    )
    lines.extend(["", "## Required Authority Chain for Future Tickers"])
    lines.extend(
        f"- `{step['step_number']}`: `{step['authority_step']}`"
        for step in candidate["future_ticker_authority_chain"]
    )
    lines.extend(["", "## Planned Outputs"])
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`, `{item['actionability_label']}`"
        for item in candidate["planned_outputs"]
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
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
            f"- live_ticker_validation_performed: `{candidate['live_ticker_validation_performed']}`",
            f"- final_ticker_selection_performed: `{candidate['final_ticker_selection_performed']}`",
            f"- scope_expansion_authorized: `{candidate['scope_expansion_authorized']}`",
            f"- expanded_ticker_universe_approved: `{candidate['expanded_ticker_universe_approved']}`",
            f"- new_ticker_authority_created: `{candidate['new_ticker_authority_created']}`",
            f"- new_ticker_acquisition_authorized: `{candidate['new_ticker_acquisition_authorized']}`",
            f"- additional_predictive_evidence_execution_authorized: `{candidate['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{candidate['additional_predictive_evidence_executed']}`",
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
            "- No live ticker validation, final ticker selection, ticker authority, or acquisition occurred.",
            "- No additional predictive evidence execution was authorized or performed.",
            "- No predictive experiment, walk-forward, label, or feature-matrix rerun occurred.",
            "- No strategy scoring or trade recommendations were generated.",
            "- No predictive-usefulness or profitability acceptance occurred.",
            "- No runtime migration, paper trading, or broker execution was authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_evidence_scope_expansion_plan_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the predictive evidence scope expansion plan candidate without overwriting."""
    candidate = build_predictive_evidence_scope_expansion_plan_candidate_v1()
    validation = validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_evidence_scope_expansion_plan_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(
            "predictive evidence scope expansion plan filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveEvidenceScopeExpansionPlanCandidateError(
            "predictive evidence scope expansion plan output already exists"
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
