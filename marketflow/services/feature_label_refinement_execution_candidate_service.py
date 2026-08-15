"""Offline candidate for future feature/label refinement execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import feature_label_refinement_plan_approval_service as approval_service
from marketflow.services import feature_label_refinement_plan_candidate_service as plan_service


ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE"
)
SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_V1 = (
    "feature_label_refinement_execution_candidate_v1"
)
FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_PLAN_APPROVAL_DIGEST = (
    "0dc0dc8a6a70b6549f453995ad639092da0e2b615fa059013592ae51a9609f2f"
)
EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval_service.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PLAN_CANDIDATE_DIGEST = approval_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval_service.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST = (
    approval_service.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST
)
EXPECTED_READINESS_REVIEW_DIGEST = approval_service.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_REASSESSMENT_REVIEW_DIGEST = (
    approval_service.EXPECTED_REASSESSMENT_REVIEW_DIGEST
)
EXPECTED_RESULTS_REVIEW_DIGEST = approval_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = approval_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    approval_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    approval_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = approval_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(approval_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = {
    ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE
}
NOT_ACCEPTED = approval_service.NOT_ACCEPTED
NOT_AUTHORIZED = approval_service.NOT_AUTHORIZED
PASS = approval_service.PASS
FAIL = approval_service.FAIL
BLOCKER = approval_service.BLOCKER

PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
NOT_EXECUTED = "NOT_EXECUTED"
PLANNED_FOR_EXECUTION_CANDIDATE_ONLY = "PLANNED_FOR_EXECUTION_CANDIDATE_ONLY"
NOT_AUTHORIZED_FOR_EXECUTION = "NOT_AUTHORIZED_FOR_EXECUTION"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"

EXECUTION_CANDIDATE_OBJECTIVE = (
    "PREPARE_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_FOR_APPROVED_PLAN"
)
EXECUTION_CANDIDATE_SCOPE = "EXECUTION_CANDIDATE_ONLY_NOT_AUTHORIZATION_NOT_EXECUTION"
EXECUTION_MODE = PLANNED_NOT_EXECUTED
EXECUTION_AUTHORITY_STATUS = NOT_AUTHORIZED

LABEL_REFINEMENT_EXECUTION_GROUP_IDS = list(plan_service.LABEL_REFINEMENT_GROUP_IDS)
FEATURE_REFINEMENT_EXECUTION_GROUP_IDS = list(plan_service.FEATURE_REFINEMENT_GROUP_IDS)
PROTOCOL_REFINEMENT_EXECUTION_GROUP_IDS = list(plan_service.PROTOCOL_REFINEMENT_GROUP_IDS)
MODEL_COMPARISON_EXECUTION_GROUP_IDS = list(plan_service.MODEL_COMPARISON_GROUP_IDS)

PLANNED_EXECUTION_STEP_IDS = [
    "load_frozen_canonical_dataset",
    "verify_records_digest",
    "apply_label_refinement_plan",
    "apply_feature_refinement_plan",
    "apply_protocol_refinement_plan",
    "prepare_model_comparison_plan",
    "generate_refined_label_manifest",
    "generate_refined_feature_manifest",
    "prepare_refined_walk_forward_plan",
    "prepare_refined_oos_plan",
    "prepare_refined_metric_plan",
    "prepare_refined_leakage_control_plan",
    "prepare_operator_review_summary",
]

PLANNED_EXECUTION_OUTPUT_NAMES = [
    "feature_label_refinement_execution_manifest",
    "refined_label_generation_plan",
    "refined_feature_generation_plan",
    "refined_protocol_execution_plan",
    "refined_model_comparison_plan",
    "refined_walk_forward_plan",
    "refined_oos_plan",
    "refined_metric_plan",
    "refined_leakage_control_plan",
    "per_ticker_refinement_execution_candidate_summary",
    "execution_candidate_digest_manifest",
    "operator_review_summary_template",
]

FUTURE_EXECUTION_CHAIN = [
    "Feature/Label Refinement Execution Candidate Operator Review Package.",
    "Feature/Label Refinement Execution Approval Ceremony, if selected.",
    "Feature/Label Refinement Execution.",
    "Feature/Label Refinement Results Review Package.",
    "Additional Predictive Evidence Execution Candidate for refined evidence.",
    "Additional Predictive Evidence Execution Approval Ceremony, if required.",
    "Additional Predictive Evidence Execution.",
    "Additional Predictive Evidence Results Review.",
    "Predictive Usefulness Reassessment Review rerun.",
    "Predictive Usefulness Acceptance Readiness Review rerun.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "feature_label_refinement_execution_candidate_operator_review",
    "feature_label_refinement_execution_approval_if_selected",
    "feature_label_refinement_execution",
    "feature_label_refinement_results_review",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_review_rerun",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "execution_candidate_does_not_authorize_execution",
    "no_refinement_execution_without_separate_execution_approval",
    "no_label_generation_without_execution_approval",
    "no_feature_generation_without_execution_approval",
    "no_model_comparison_without_execution_approval",
    "no_predictive_usefulness_acceptance_from_execution_candidate",
    "no_acceptance_when_readiness_not_met",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_predictive_evidence_without_new_approval",
    "preserve_meta_reduced_record_count",
    "all_outputs_labeled_research_only",
]

REQUIRED_CHECK_IDS = [
    "plan_approval_digest_bound",
    "plan_candidate_review_digest_bound",
    "plan_candidate_digest_bound",
    "improvement_candidate_review_digest_bound",
    "readiness_review_digest_bound",
    "reassessment_review_digest_bound",
    "results_review_digest_bound",
    "execution_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_plan_approval_universe",
    "plan_approved_true",
    "ready_for_feature_label_refinement_execution_candidate_true",
    "feature_label_refinement_execution_candidate_created_true",
    "execution_candidate_scope_candidate_only",
    "execution_authority_status_not_authorized",
    "readiness_decision_not_ready",
    "readiness_reason_mixed_stability_and_insufficient_baseline_outperformance",
    "label_refinement_execution_groups_7",
    "feature_refinement_execution_groups_9",
    "protocol_refinement_execution_groups_6",
    "model_comparison_execution_groups_5",
    "planned_execution_steps_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "per_ticker_execution_candidate_entries_12",
    "per_ticker_execution_candidate_digests_present",
    "future_execution_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "live_provider_transport_enabled_false",
    "market_data_acquisition_performed_false",
    "dataset_generation_performed_false",
    "canonical_dataset_regenerated_false",
    "predictive_execution_rerun_performed_false",
    "label_generation_rerun_performed_false",
    "feature_matrix_rerun_performed_false",
    "walk_forward_validation_rerun_performed_false",
    "out_of_sample_evaluation_rerun_performed_false",
    "metrics_recomputation_performed_false",
    "improvement_execution_performed_false",
    "refinement_option_execution_performed_false",
    "label_refinement_execution_performed_false",
    "feature_refinement_execution_performed_false",
    "protocol_refinement_execution_performed_false",
    "model_comparison_performed_false",
    "feature_label_refinement_execution_approved_false",
    "feature_label_refinement_execution_authorized_false",
    "feature_label_refinement_executed_false",
    "feature_label_refinement_results_created_false",
    "refined_label_generation_authorized_false",
    "refined_label_generation_performed_false",
    "refined_feature_generation_authorized_false",
    "refined_feature_generation_performed_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
    "predictive_usefulness_acceptance_candidate_created_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "profitability_acceptance_recommended_false",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "no_feature_label_refinement_execution_approval_created",
    "no_feature_label_refinement_execution_artifact_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

FORBIDDEN_ARTIFACT_VALUES = {
    "FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED",
    "FEATURE_LABEL_REFINEMENT_EXECUTED",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "LABEL_GENERATION_EXECUTED",
    "FEATURE_MATRIX_GENERATION_EXECUTED",
    "WALK_FORWARD_VALIDATION_EXECUTED",
    "OUT_OF_SAMPLE_EVALUATION_EXECUTED",
    "MODEL_COMPARISON_EXECUTED",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


class FeatureLabelRefinementExecutionCandidateError(ValueError):
    """Raised when an execution candidate violates its candidate-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureLabelRefinementExecutionCandidateError(f"{field} mismatch")


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _readiness_failure_basis() -> dict[str, Any]:
    return {
        "readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
        "stability_consistency_required": "FAIL_OR_NOT_MET",
        "baseline_outperformance_consistency_required": "FAIL_OR_NOT_MET",
        "walk_forward_accuracy_range": "0.498698 to 0.562842",
        "oos_majority_accuracy": "0.539491",
        "oos_previous_direction_accuracy": "0.495984",
        "oos_ticker_cross_sectional_accuracy": "0.502677",
        "oos_brier_score": "0.24875351",
        "leakage_status": PASS,
        "failed_leakage_controls": 0,
    }


def _execution_candidate_profile() -> dict[str, Any]:
    return {
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "dataset_scope": "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY",
        "registry_entry_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "source_profile": "RTH_FULL_SESSION_1D",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "execution_profile_status": PLANNED_NOT_EXECUTED,
    }


def _planned_execution_steps() -> list[dict[str, Any]]:
    return [
        {
            "step_id": step_id,
            "execution_status": PLANNED_NOT_EXECUTED,
            "authorization_status": NOT_AUTHORIZED_FOR_EXECUTION,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for step_id in PLANNED_EXECUTION_STEP_IDS
    ]


def _planned_groups(group_ids: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "group_id": group_id,
            "execution_candidate_status": PLANNED_FOR_EXECUTION_CANDIDATE_ONLY,
            "authorization_status": NOT_AUTHORIZED,
            "execution_status": NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for group_id in group_ids
    ]


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_name": output_name,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_name in PLANNED_EXECUTION_OUTPUT_NAMES
    ]


def per_ticker_feature_label_refinement_execution_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker candidate entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_feature_label_refinement_execution_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "readiness_status": "NOT_READY",
            "feature_label_refinement_plan_status": (
                approval_service.APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
            ),
            "feature_label_refinement_execution_candidate_status": (
                PLANNED_READY_FOR_OPERATOR_REVIEW
            ),
            "feature_label_refinement_execution_authorized": False,
            "feature_label_refinement_executed": False,
            "refined_label_generation_authorized": False,
            "refined_label_generation_performed": False,
            "refined_feature_generation_authorized": False,
            "refined_feature_generation_performed": False,
            "model_comparison_authorized": False,
            "model_comparison_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_feature_label_refinement_plan_approval_digest": (
                EXPECTED_PLAN_APPROVAL_DIGEST
            ),
            "source_feature_label_refinement_plan_candidate_review_digest": (
                EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
            ),
        }
        if ticker == "META":
            entry["refinement_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_FEATURE_PLAN"
            )
        entry["per_ticker_feature_label_refinement_execution_candidate_digest"] = (
            per_ticker_feature_label_refinement_execution_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_V1,
        "candidate_status": FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_generation_performed": False,
        "canonical_dataset_regenerated": False,
        "predictive_execution_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_matrix_rerun_performed": False,
        "walk_forward_validation_rerun_performed": False,
        "out_of_sample_evaluation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "improvement_execution_performed": False,
        "refinement_option_execution_performed": False,
        "label_refinement_execution_performed": False,
        "feature_refinement_execution_performed": False,
        "protocol_refinement_execution_performed": False,
        "model_comparison_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_label_refinement_plan_candidate_created": True,
        "feature_label_refinement_plan_candidate_review_created": True,
        "feature_label_refinement_plan_approved": True,
        "feature_label_refinement_plan_approval_created": True,
        "ready_for_feature_label_refinement_execution_candidate": True,
        "feature_label_refinement_execution_candidate_created": True,
        "feature_label_refinement_execution_candidate_ready_for_operator_review": True,
        "feature_label_refinement_execution_candidate_review_created": False,
        "feature_label_refinement_execution_approved": False,
        "feature_label_refinement_execution_authorized": False,
        "feature_label_refinement_executed": False,
        "feature_label_refinement_results_created": False,
        "refined_label_generation_authorized": False,
        "refined_label_generation_performed": False,
        "refined_feature_generation_authorized": False,
        "refined_feature_generation_performed": False,
        "refined_walk_forward_validation_authorized": False,
        "refined_walk_forward_validation_performed": False,
        "refined_out_of_sample_evaluation_authorized": False,
        "refined_out_of_sample_evaluation_performed": False,
        "refined_metrics_recomputation_authorized": False,
        "refined_metrics_recomputation_performed": False,
        "model_comparison_authorized": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "operator_review_required": True,
        "feature_label_refinement_plan_approval_digest": EXPECTED_PLAN_APPROVAL_DIGEST,
        "feature_label_refinement_plan_candidate_review_package_digest": (
            EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "feature_label_refinement_plan_candidate_digest": EXPECTED_PLAN_CANDIDATE_DIGEST,
        "predictive_evidence_improvement_candidate_review_package_digest": (
            EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_improvement_candidate_digest": (
            EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_review_digest": (
            EXPECTED_READINESS_REVIEW_DIGEST
        ),
        "predictive_usefulness_reassessment_review_package_digest": (
            EXPECTED_REASSESSMENT_REVIEW_DIGEST
        ),
        "additional_predictive_evidence_results_review_package_digest": (
            EXPECTED_RESULTS_REVIEW_DIGEST
        ),
        "additional_predictive_evidence_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "feature_label_refinement_plan_objective": plan_service.PLAN_OBJECTIVE,
        "feature_label_refinement_plan_scope": approval_service.PLAN_APPROVAL_SCOPE,
        "feature_label_refinement_plan_mode": approval_service.APPROVED_NOT_EXECUTED,
        "feature_label_refinement_plan_authority_status": (
            approval_service.APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
        ),
        "feature_label_refinement_execution_candidate_objective": (
            EXECUTION_CANDIDATE_OBJECTIVE
        ),
        "feature_label_refinement_execution_candidate_scope": EXECUTION_CANDIDATE_SCOPE,
        "feature_label_refinement_execution_mode": EXECUTION_MODE,
        "feature_label_refinement_execution_authority_status": (
            EXECUTION_AUTHORITY_STATUS
        ),
        "readiness_failure_basis": _readiness_failure_basis(),
        "execution_candidate_profile": _execution_candidate_profile(),
        "planned_execution_steps": _planned_execution_steps(),
        "planned_label_refinement_execution_groups": _planned_groups(
            LABEL_REFINEMENT_EXECUTION_GROUP_IDS
        ),
        "planned_feature_refinement_execution_groups": _planned_groups(
            FEATURE_REFINEMENT_EXECUTION_GROUP_IDS
        ),
        "planned_protocol_refinement_execution_groups": _planned_groups(
            PROTOCOL_REFINEMENT_EXECUTION_GROUP_IDS
        ),
        "planned_model_comparison_execution_groups": _planned_groups(
            MODEL_COMPARISON_EXECUTION_GROUP_IDS
        ),
        "planned_execution_outputs": _planned_outputs(),
        "per_ticker_execution_candidate_entries": _per_ticker_entries(),
        "future_execution_chain": list(FUTURE_EXECUTION_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "feature_label_refinement_execution_approval_created": False,
        "feature_label_refinement_execution_artifact_created": False,
        "additional_predictive_evidence_execution_candidate_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    outputs = candidate.get("planned_execution_outputs", [])
    entries = candidate.get("per_ticker_execution_candidate_entries", [])
    basis = candidate.get("readiness_failure_basis", {})
    fields = {
        "plan_approval_digest_bound": (EXPECTED_PLAN_APPROVAL_DIGEST, candidate.get("feature_label_refinement_plan_approval_digest")),
        "plan_candidate_review_digest_bound": (EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("feature_label_refinement_plan_candidate_review_package_digest")),
        "plan_candidate_digest_bound": (EXPECTED_PLAN_CANDIDATE_DIGEST, candidate.get("feature_label_refinement_plan_candidate_digest")),
        "improvement_candidate_review_digest_bound": (EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_evidence_improvement_candidate_review_package_digest")),
        "readiness_review_digest_bound": (EXPECTED_READINESS_REVIEW_DIGEST, candidate.get("predictive_usefulness_acceptance_readiness_review_digest")),
        "reassessment_review_digest_bound": (EXPECTED_REASSESSMENT_REVIEW_DIGEST, candidate.get("predictive_usefulness_reassessment_review_package_digest")),
        "results_review_digest_bound": (EXPECTED_RESULTS_REVIEW_DIGEST, candidate.get("additional_predictive_evidence_results_review_package_digest")),
        "execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, candidate.get("additional_predictive_evidence_execution_digest")),
        "research_registry_approval_digest_bound": (EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, candidate.get("research_registry_approval_digest")),
        "canonical_dataset_freeze_digest_bound": (EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, candidate.get("canonical_dataset_freeze_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, candidate.get("records_digest")),
        "target_universe_count_12": (12, candidate.get("target_universe_count")),
        "target_universe_matches_plan_approval_universe": (TARGET_UNIVERSE, candidate.get("target_universe")),
        "plan_approved_true": (True, candidate.get("feature_label_refinement_plan_approved")),
        "ready_for_feature_label_refinement_execution_candidate_true": (True, candidate.get("ready_for_feature_label_refinement_execution_candidate")),
        "feature_label_refinement_execution_candidate_created_true": (True, candidate.get("feature_label_refinement_execution_candidate_created")),
        "execution_candidate_scope_candidate_only": (EXECUTION_CANDIDATE_SCOPE, candidate.get("feature_label_refinement_execution_candidate_scope")),
        "execution_authority_status_not_authorized": (NOT_AUTHORIZED, candidate.get("feature_label_refinement_execution_authority_status")),
        "readiness_decision_not_ready": ("PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY", basis.get("readiness_decision")),
        "readiness_reason_mixed_stability_and_insufficient_baseline_outperformance": ("MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE", basis.get("readiness_reason")),
        "label_refinement_execution_groups_7": (7, len(candidate.get("planned_label_refinement_execution_groups", []))),
        "feature_refinement_execution_groups_9": (9, len(candidate.get("planned_feature_refinement_execution_groups", []))),
        "protocol_refinement_execution_groups_6": (6, len(candidate.get("planned_protocol_refinement_execution_groups", []))),
        "model_comparison_execution_groups_5": (5, len(candidate.get("planned_model_comparison_execution_groups", []))),
        "planned_execution_steps_defined": (_planned_execution_steps(), candidate.get("planned_execution_steps")),
        "planned_outputs_not_generated": (True, bool(outputs) and all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)),
        "per_ticker_execution_candidate_entries_12": (12, len(entries)),
        "per_ticker_execution_candidate_digests_present": (True, bool(entries) and all(isinstance(item.get("per_ticker_feature_label_refinement_execution_candidate_digest"), str) and len(item["per_ticker_feature_label_refinement_execution_candidate_digest"]) == 64 for item in entries)),
        "future_execution_chain_defined": (FUTURE_EXECUTION_CHAIN, candidate.get("future_execution_chain")),
        "future_gates_defined": (FUTURE_GATES, candidate.get("future_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
    }
    false_checks = {
        "provider_requests_made_false": "provider_requests_made",
        "live_provider_transport_enabled_false": "live_provider_transport_enabled",
        "market_data_acquisition_performed_false": "market_data_acquisition_performed",
        "dataset_generation_performed_false": "dataset_generation_performed",
        "canonical_dataset_regenerated_false": "canonical_dataset_regenerated",
        "predictive_execution_rerun_performed_false": "predictive_execution_rerun_performed",
        "label_generation_rerun_performed_false": "label_generation_rerun_performed",
        "feature_matrix_rerun_performed_false": "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed_false": "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed_false": "out_of_sample_evaluation_rerun_performed",
        "metrics_recomputation_performed_false": "metrics_recomputation_performed",
        "improvement_execution_performed_false": "improvement_execution_performed",
        "refinement_option_execution_performed_false": "refinement_option_execution_performed",
        "label_refinement_execution_performed_false": "label_refinement_execution_performed",
        "feature_refinement_execution_performed_false": "feature_refinement_execution_performed",
        "protocol_refinement_execution_performed_false": "protocol_refinement_execution_performed",
        "model_comparison_performed_false": "model_comparison_performed",
        "feature_label_refinement_execution_approved_false": "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized_false": "feature_label_refinement_execution_authorized",
        "feature_label_refinement_executed_false": "feature_label_refinement_executed",
        "feature_label_refinement_results_created_false": "feature_label_refinement_results_created",
        "refined_label_generation_authorized_false": "refined_label_generation_authorized",
        "refined_label_generation_performed_false": "refined_label_generation_performed",
        "refined_feature_generation_authorized_false": "refined_feature_generation_authorized",
        "refined_feature_generation_performed_false": "refined_feature_generation_performed",
        "additional_predictive_evidence_execution_candidate_created_false": "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready_false": "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended_false": "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created_false": "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready_false": "profitability_acceptance_ready",
        "profitability_acceptance_recommended_false": "profitability_acceptance_recommended",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "no_feature_label_refinement_execution_approval_created": "feature_label_refinement_execution_approval_created",
        "no_feature_label_refinement_execution_artifact_created": "feature_label_refinement_execution_artifact_created",
        "no_additional_predictive_evidence_execution_candidate_created": "additional_predictive_evidence_execution_candidate_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    fields.update({check_id: (False, candidate.get(field)) for check_id, field in false_checks.items()})
    fields.update({
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, candidate.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, candidate.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
    })
    return [_check(check_id, *fields[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(
            item.get("status") == FAIL and item.get("severity") == BLOCKER
            for item in checklist
        ),
        "ready_for_operator_review": failed == 0,
        "ready_for_feature_label_refinement_execution_approval": False,
        "ready_for_feature_label_refinement_execution": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def feature_label_refinement_execution_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the complete candidate."""
    payload = deepcopy(candidate)
    payload.pop("feature_label_refinement_execution_candidate_digest", None)
    return semantic_digest(payload)


def build_feature_label_refinement_execution_candidate_v1() -> dict[str, Any]:
    """Build the candidate without authorizing or executing refinement work."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["feature_label_refinement_execution_candidate_digest"] = (
        feature_label_refinement_execution_candidate_digest_v1(candidate)
    )
    validate_feature_label_refinement_execution_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise FeatureLabelRefinementExecutionCandidateError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _validate_per_ticker_entries(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_execution_candidate_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise FeatureLabelRefinementExecutionCandidateError(
            "per-ticker execution candidate entries missing"
        )
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    _expect(entries, _per_ticker_entries(), "per-ticker entries")
    for entry in entries:
        digest = entry.get(
            "per_ticker_feature_label_refinement_execution_candidate_digest"
        )
        if not isinstance(digest, str) or len(digest) != 64:
            raise FeatureLabelRefinementExecutionCandidateError(
                "per-ticker execution candidate digest missing"
            )
        _expect(
            digest,
            per_ticker_feature_label_refinement_execution_candidate_digest_v1(entry),
            "per-ticker execution candidate digest",
        )


def validate_feature_label_refinement_execution_candidate_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is the exact non-authorizing candidate."""
    if not isinstance(candidate, dict):
        raise FeatureLabelRefinementExecutionCandidateError(
            "feature/label refinement execution candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    expected_base = _base_candidate()
    for field, expected in expected_base.items():
        _expect(candidate.get(field), expected, field)
    _validate_per_ticker_entries(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise FeatureLabelRefinementExecutionCandidateError("candidate_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise FeatureLabelRefinementExecutionCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), expected_summary, "candidate_summary")
    digest = candidate.get("feature_label_refinement_execution_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureLabelRefinementExecutionCandidateError(
            "feature label refinement execution candidate digest missing"
        )
    _expect(
        digest,
        feature_label_refinement_execution_candidate_digest_v1(candidate),
        "feature label refinement execution candidate digest",
    )
    return {
        "status": "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "feature_label_refinement_execution_candidate_digest": digest,
        "ready_for_operator_review": expected_summary["ready_for_operator_review"],
        "blocker_count": expected_summary["blocker_count"],
        "feature_label_refinement_execution_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_feature_label_refinement_execution_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized status document for the candidate."""
    validation = validate_feature_label_refinement_execution_candidate_v1(candidate)
    summary = candidate["candidate_summary"]
    basis = candidate["readiness_failure_basis"]
    profile = candidate["execution_candidate_profile"]
    lines = [
        "# MarketFlow Feature/Label Refinement Execution Candidate Status",
        "",
        "## Title",
        "- Feature/Label Refinement Execution Candidate v1.",
        "",
        "## Feature/Label Refinement Execution Candidate",
        f"- Artifact: `{candidate['artifact_kind']}`",
        f"- Status: `{candidate['candidate_status']}`",
        f"- Candidate digest: `{validation['feature_label_refinement_execution_candidate_digest']}`",
        "",
        "## Source Plan Approval",
        f"- Plan approval digest: `{candidate['feature_label_refinement_plan_approval_digest']}`",
        f"- Plan candidate review digest: `{candidate['feature_label_refinement_plan_candidate_review_package_digest']}`",
        f"- Plan candidate digest: `{candidate['feature_label_refinement_plan_candidate_digest']}`",
        "",
        "## Execution Candidate Objective",
        f"- Objective: `{candidate['feature_label_refinement_execution_candidate_objective']}`",
        f"- Scope: `{candidate['feature_label_refinement_execution_candidate_scope']}`",
        f"- Authority: `{candidate['feature_label_refinement_execution_authority_status']}`",
        "",
        "## Readiness Failure Basis",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in basis.items())
    lines.extend(["", "## Execution Candidate Profile"])
    lines.extend(f"- {key}: `{value}`" for key, value in profile.items())
    for heading, key, id_field in (
        ("Planned Execution Steps", "planned_execution_steps", "step_id"),
        ("Planned Label Refinement Execution Groups", "planned_label_refinement_execution_groups", "group_id"),
        ("Planned Feature Refinement Execution Groups", "planned_feature_refinement_execution_groups", "group_id"),
        ("Planned Protocol Refinement Execution Groups", "planned_protocol_refinement_execution_groups", "group_id"),
        ("Planned Model Comparison Execution Groups", "planned_model_comparison_execution_groups", "group_id"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_field]}`" for item in candidate[key])
    lines.extend(["", "## Per-Ticker Execution Candidate Entries"])
    lines.extend(
        f"- `{item['ticker']}`: `{item['historical_record_count']}` records; "
        f"`{item['feature_label_refinement_execution_candidate_status']}`"
        for item in candidate["per_ticker_execution_candidate_entries"]
    )
    for heading, values in (
        ("Future Execution Chain", candidate["future_execution_chain"]),
        ("Future Gates", candidate["future_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {value}" for value in values)
    lines.extend(
        [
            "",
            "## Execution Boundary",
            "- Candidate only; refinement execution remains not authorized and not performed.",
            "",
            "## Predictive Usefulness Boundary",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            "",
            "## Profitability Boundary",
            f"- profitability: `{candidate['profitability']}`",
            "",
            "## Runtime Boundary",
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
            "- No provider request, acquisition, dataset regeneration, predictive rerun, label/feature generation, metric recomputation, refinement execution, or model comparison occurs.",
            "- No predictive usefulness or profitability acceptance, runtime activation, strategy scoring, or trade recommendation occurs.",
            "- META remains exactly 913 records; all other tickers remain exactly 1003 records.",
            "",
        ]
    )
    return "\n".join(lines)


def write_feature_label_refinement_execution_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical candidate JSON once; existing output fails closed."""
    candidate = build_feature_label_refinement_execution_candidate_v1()
    validation = validate_feature_label_refinement_execution_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "feature_label_refinement_execution_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureLabelRefinementExecutionCandidateError(
            "candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise FeatureLabelRefinementExecutionCandidateError(
            "feature label refinement execution candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
