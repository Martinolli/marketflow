"""Offline execution candidate for the approved label-objective redesign."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import label_objective_redesign_approval_service as approval


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_V1 = (
    "label_objective_redesign_execution_candidate_v1"
)
LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
EXECUTION_CANDIDATE_OBJECTIVE = (
    "PREPARE_LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_FOR_APPROVED_REDESIGN_PLAN"
)
EXECUTION_CANDIDATE_SCOPE = (
    "EXECUTION_CANDIDATE_ONLY_NOT_AUTHORIZATION_NOT_EXECUTION"
)
EXECUTION_CANDIDATE_MODE = "PLANNED_NOT_EXECUTED"
EXECUTION_CANDIDATE_AUTHORITY_STATUS = "NOT_AUTHORIZED"

EXPECTED_APPROVAL_DIGEST = (
    "71cd46568009929a37afb2936d32ca6d9fb097c6c51a1cccf84af1bfc8eb0185"
)
EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANDIDATE_DIGEST = approval.EXPECTED_CANDIDATE_DIGEST
candidate_service = approval.candidate_service
TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
NOT_ACCEPTED = approval.NOT_ACCEPTED
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
PASS = approval.PASS
FAIL = approval.FAIL
BLOCKER = approval.BLOCKER

REQUIRED_DIGEST_FIELDS = {
    "label_objective_redesign_approval_digest": EXPECTED_APPROVAL_DIGEST,
    **approval.REQUIRED_DIGEST_FIELDS,
}

PLANNED_EXECUTION_ACTIVITIES = [
    "load_frozen_canonical_dataset_for_label_redesign",
    "verify_canonical_records_digest",
    "bind_approved_label_objective_hypotheses",
    "bind_approved_redesign_dimensions",
    "bind_approved_label_family_candidates",
    "bind_approved_evaluation_questions",
    "prepare_label_objective_redesign_manifest",
    "prepare_label_family_candidate_matrix",
    "prepare_threshold_design_matrix",
    "prepare_horizon_design_matrix",
    "prepare_per_ticker_label_objective_plan",
    "prepare_label_availability_boundary_plan",
    "prepare_meta_limitation_preservation_plan",
    "prepare_operator_review_summary",
]

PLANNED_WORKSTREAMS = [
    "tradeability_alignment_workstream",
    "prediction_horizon_workstream",
    "threshold_and_flat_zone_workstream",
    "absolute_vs_relative_return_workstream",
    "risk_adjusted_target_workstream",
    "drawdown_avoidance_workstream",
    "volatility_regime_conditioning_workstream",
    "benchmark_relative_target_workstream",
    "per_ticker_calibration_workstream",
    "meta_label_availability_workstream",
]

PLANNED_EXECUTION_OUTPUTS = [
    "label_objective_redesign_execution_manifest",
    "label_family_candidate_matrix",
    "threshold_design_matrix",
    "horizon_design_matrix",
    "per_ticker_label_objective_plan",
    "label_availability_boundary_plan",
    "meta_limitation_preservation_plan",
    "operator_review_summary_template",
]

FUTURE_CHAIN = [
    "Label Objective Redesign Execution Candidate Operator Review Package v1.",
    "Label Objective Redesign Execution Approval v1, if selected.",
    "Label Objective Redesign Execution v1.",
    "Label Objective Redesign Results Review v1.",
    "Additional Predictive Evidence Execution Candidate using redesigned labels, if results support it.",
    "Additional Predictive Evidence Execution and Results Review, if separately approved.",
    "Predictive Usefulness Reassessment and Readiness Review, only after new evidence.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "label_objective_redesign_execution_candidate_operator_review",
    "label_objective_redesign_execution_approval_if_selected",
    "label_objective_redesign_execution",
    "label_objective_redesign_results_review",
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "execution_candidate_does_not_authorize_label_generation",
    "execution_candidate_does_not_authorize_execution",
    "execution_candidate_does_not_accept_predictive_usefulness",
    "execution_candidate_does_not_accept_profitability",
    "execution_candidate_does_not_authorize_runtime",
    "execution_candidate_does_not_authorize_strategy",
    "execution_candidate_does_not_authorize_paper_trading",
    "execution_candidate_does_not_authorize_broker_execution",
    "execution_candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "preserve_meta_record_limitation",
    "no_more_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

CHECK_IDS = [
    "approval_digest_bound",
    "candidate_review_digest_bound",
    "candidate_digest_bound",
    "operator_method_path_selection_digest_bound",
    "method_diagnostic_digest_bound",
    "planning_tree_digest_bound",
    "latest_readiness_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "target_universe_matches_approval_universe",
    "records_digest_preserved",
    "meta_913_preserved",
    "label_objective_redesign_approved_true",
    "ready_for_label_objective_redesign_execution_candidate_true",
    "label_objective_redesign_execution_candidate_created_true",
    "label_objective_redesign_execution_candidate_ready_for_operator_review_true",
    "label_objective_redesign_execution_candidate_review_created_false",
    "label_objective_redesign_authorized_false",
    "label_objective_redesign_executed_false",
    "redesigned_label_generation_authorized_false",
    "redesigned_label_generation_performed_false",
    "planned_execution_activities_defined",
    "planned_workstreams_defined",
    "planned_label_family_outputs_10",
    "planned_execution_outputs_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "future_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "label_generation_false",
    "feature_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "strategy_scoring_false",
    "runtime_activation_false",
    "no_label_objective_redesign_execution_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "no_tracked_marketflow_files",
]


class LabelObjectiveRedesignExecutionCandidateError(ValueError):
    """Raised when the execution candidate violates its planning-only scope."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignExecutionCandidateError(f"{field} mismatch")


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


def _planned_activities() -> list[dict[str, Any]]:
    return [
        {
            "activity_id": activity_id,
            "activity_status": "PLANNED_NOT_EXECUTED",
            "authorization_status": NOT_AUTHORIZED,
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for activity_id in PLANNED_EXECUTION_ACTIVITIES
    ]


def _planned_workstreams() -> list[dict[str, Any]]:
    return [
        {
            "workstream_id": workstream_id,
            "workstream_status": "PLANNED_FOR_EXECUTION_CANDIDATE_ONLY",
            "authorization_status": NOT_AUTHORIZED,
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for workstream_id in PLANNED_WORKSTREAMS
    ]


def _planned_label_family_outputs() -> list[dict[str, Any]]:
    return [
        {
            "label_family_candidate_id": candidate_id,
            "planned_output_status": "PLANNED_NOT_GENERATED",
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for candidate_id in candidate_service.LABEL_FAMILY_CANDIDATES
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "output_status": "PLANNED_NOT_GENERATED",
            "authority": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_EXECUTION_OUTPUTS
    ]


def per_ticker_label_objective_redesign_execution_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one ticker planning entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_label_objective_redesign_execution_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": candidate_service.EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "selected_method_path": candidate_service.SELECTED_METHOD_PATH,
            "label_objective_redesign_approval_status": (
                approval.APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
            ),
            "label_objective_redesign_execution_candidate_status": (
                "PLANNED_READY_FOR_OPERATOR_REVIEW"
            ),
            "label_objective_redesign_authorized": False,
            "label_objective_redesign_executed": False,
            "redesigned_label_generation_authorized": False,
            "redesigned_label_generation_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_label_objective_redesign_approval_digest": EXPECTED_APPROVAL_DIGEST,
            "source_label_objective_redesign_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        }
        if is_meta:
            entry["redesign_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_LABEL_AVAILABILITY_LIMITATION"
            )
        entry["per_ticker_label_objective_redesign_execution_candidate_digest"] = (
            per_ticker_label_objective_redesign_execution_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_V1,
        "candidate_status": LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "label_objective_redesign_candidate_created": True,
        "label_objective_redesign_candidate_review_created": True,
        "label_objective_redesign_approved": True,
        "label_objective_redesign_approval_created": True,
        "ready_for_label_objective_redesign_execution_candidate": True,
        "label_objective_redesign_execution_candidate_created": True,
        "label_objective_redesign_execution_candidate_ready_for_operator_review": True,
        "label_objective_redesign_execution_candidate_review_created": False,
        "label_objective_redesign_authorized": False,
        "label_objective_redesign_executed": False,
        "label_objective_redesign_results_created": False,
        "redesigned_label_generation_authorized": False,
        "redesigned_label_generation_performed": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
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
        "provider_requests_made": False,
        "market_data_acquisition_performed": False,
        "dataset_regeneration_performed": False,
        "label_generation_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "label_objective_redesign_execution_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        **REQUIRED_DIGEST_FIELDS,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(candidate_service.EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "selected_method_path": candidate_service.SELECTED_METHOD_PATH,
        "label_objective_redesign_execution_candidate_objective": EXECUTION_CANDIDATE_OBJECTIVE,
        "label_objective_redesign_execution_candidate_scope": EXECUTION_CANDIDATE_SCOPE,
        "label_objective_redesign_execution_candidate_mode": EXECUTION_CANDIDATE_MODE,
        "label_objective_redesign_execution_candidate_authority_status": EXECUTION_CANDIDATE_AUTHORITY_STATUS,
        "problem_basis": {
            "two_readiness_gates_not_ready": True,
            "original_readiness_decision": candidate_service.selection.ORIGINAL_READINESS_DECISION,
            "refined_readiness_decision": candidate_service.selection.REFINED_READINESS_DECISION,
            "method_diagnostic_conclusion": "METHOD_REVIEW_REQUIRED_BEFORE_MORE_EXECUTION",
            "overall_method_signal_status": "WEAK_OR_MIXED",
            "baseline_outperformance_status": "INSUFFICIENT_OR_MIXED",
            "oos_generalization_status": "LOW_TO_MIXED",
        },
        "planned_execution_activities": _planned_activities(),
        "planned_workstreams": _planned_workstreams(),
        "planned_label_family_outputs": _planned_label_family_outputs(),
        "planned_execution_outputs": _planned_outputs(),
        "per_ticker_entries": _per_ticker_entries(),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _derived_checks(candidate: dict[str, Any]) -> dict[str, bool]:
    entries = candidate.get("per_ticker_entries", [])
    outputs = candidate.get("planned_execution_outputs", [])
    counts = candidate.get("per_ticker_record_counts", {})
    return {
        "approval_digest_bound": candidate.get("label_objective_redesign_approval_digest") == EXPECTED_APPROVAL_DIGEST,
        "candidate_review_digest_bound": candidate.get("label_objective_redesign_candidate_review_package_digest") == EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "candidate_digest_bound": candidate.get("label_objective_redesign_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "operator_method_path_selection_digest_bound": candidate.get("operator_method_path_selection_digest") == candidate_service.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "method_diagnostic_digest_bound": candidate.get("predictive_evidence_method_diagnostic_review_package_digest") == candidate_service.EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "planning_tree_digest_bound": candidate.get("predictive_evidence_planning_tree_review_package_digest") == candidate_service.EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "latest_readiness_digest_bound": candidate.get("latest_readiness_rerun_using_refined_evidence_digest") == candidate_service.EXPECTED_LATEST_READINESS_DIGEST,
        "research_registry_digest_bound": candidate.get("research_registry_approval_digest") == candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest_bound": candidate.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": candidate.get("target_universe_count") == 12 and candidate.get("target_universe") == TARGET_UNIVERSE,
        "target_universe_matches_approval_universe": candidate.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": candidate.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": candidate.get("meta_record_count") == 913 and counts.get("META") == 913 and candidate.get("meta_reduced_record_count_preserved") is True,
        "label_objective_redesign_approved_true": candidate.get("label_objective_redesign_approved") is True,
        "ready_for_label_objective_redesign_execution_candidate_true": candidate.get("ready_for_label_objective_redesign_execution_candidate") is True,
        "label_objective_redesign_execution_candidate_created_true": candidate.get("label_objective_redesign_execution_candidate_created") is True,
        "label_objective_redesign_execution_candidate_ready_for_operator_review_true": candidate.get("label_objective_redesign_execution_candidate_ready_for_operator_review") is True,
        "label_objective_redesign_execution_candidate_review_created_false": candidate.get("label_objective_redesign_execution_candidate_review_created") is False,
        "label_objective_redesign_authorized_false": candidate.get("label_objective_redesign_authorized") is False,
        "label_objective_redesign_executed_false": candidate.get("label_objective_redesign_executed") is False,
        "redesigned_label_generation_authorized_false": candidate.get("redesigned_label_generation_authorized") is False,
        "redesigned_label_generation_performed_false": candidate.get("redesigned_label_generation_performed") is False,
        "planned_execution_activities_defined": [item.get("activity_id") for item in candidate.get("planned_execution_activities", []) if isinstance(item, dict)] == PLANNED_EXECUTION_ACTIVITIES,
        "planned_workstreams_defined": [item.get("workstream_id") for item in candidate.get("planned_workstreams", []) if isinstance(item, dict)] == PLANNED_WORKSTREAMS,
        "planned_label_family_outputs_10": [item.get("label_family_candidate_id") for item in candidate.get("planned_label_family_outputs", []) if isinstance(item, dict)] == candidate_service.LABEL_FAMILY_CANDIDATES,
        "planned_execution_outputs_defined": [item.get("output_id") for item in outputs if isinstance(item, dict)] == PLANNED_EXECUTION_OUTPUTS,
        "planned_outputs_not_generated": isinstance(outputs, list) and len(outputs) == len(PLANNED_EXECUTION_OUTPUTS) and all(item.get("output_status") == "PLANNED_NOT_GENERATED" for item in outputs if isinstance(item, dict)),
        "planned_outputs_research_only": isinstance(outputs, list) and len(outputs) == len(PLANNED_EXECUTION_OUTPUTS) and all(item.get("authority") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for item in outputs if isinstance(item, dict)),
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12 and [item.get("ticker") for item in entries if isinstance(item, dict)] == TARGET_UNIVERSE,
        "per_ticker_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_label_objective_redesign_execution_candidate_digest"), str) and len(item["per_ticker_label_objective_redesign_execution_candidate_digest"]) == 64 and item["per_ticker_label_objective_redesign_execution_candidate_digest"] == per_ticker_label_objective_redesign_execution_candidate_digest_v1(item) for item in entries if isinstance(item, dict)),
        "future_chain_defined": candidate.get("future_chain") == FUTURE_CHAIN,
        "future_gates_defined": candidate.get("future_gates") == FUTURE_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": candidate.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": candidate.get("runtime_migration_approved") is False and candidate.get("runtime_migration_active") is False and candidate.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": candidate.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": candidate.get("paper_trading") == NOT_AUTHORIZED and candidate.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": candidate.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": candidate.get("provider_requests_made") is False,
        "market_data_acquisition_false": candidate.get("market_data_acquisition_performed") is False,
        "dataset_regeneration_false": candidate.get("dataset_regeneration_performed") is False,
        "label_generation_false": candidate.get("label_generation_performed") is False and candidate.get("redesigned_label_generation_performed") is False,
        "feature_generation_false": candidate.get("feature_generation_performed") is False and candidate.get("redesigned_feature_generation_performed") is False,
        "metric_recomputation_false": candidate.get("metric_recomputation_performed") is False,
        "model_training_false": candidate.get("model_training_performed") is False,
        "strategy_scoring_false": candidate.get("new_strategy_scoring_performed") is False,
        "runtime_activation_false": candidate.get("runtime_migration_active") is False,
        "no_label_objective_redesign_execution_created": candidate.get("label_objective_redesign_execution_created") is False,
        "no_additional_predictive_evidence_execution_candidate_created": candidate.get("additional_predictive_evidence_execution_candidate_created") is False,
        "no_predictive_usefulness_acceptance_artifact_created": candidate.get("predictive_usefulness_acceptance_artifact_created") is False,
        "no_profitability_acceptance_created": candidate.get("profitability_acceptance_created") is False,
        "no_runtime_migration_approval_created": candidate.get("runtime_migration_approval_created") is False,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True and candidate.get("tracked_marketflow_files") == [],
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(candidate)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    blockers = sum(
        item.get("status") == FAIL and item.get("severity") == BLOCKER
        for item in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "label_objective_redesign_execution_candidate_ready": blockers == 0,
        "ready_for_operator_review": blockers == 0,
        "ready_for_label_objective_redesign_execution_approval": False,
        "ready_for_label_objective_redesign_execution": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("label_objective_redesign_execution_candidate_digest", None)
    return payload


def label_objective_redesign_execution_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic execution-candidate digest."""
    return semantic_digest(_digest_payload(candidate))


def build_label_objective_redesign_execution_candidate_v1() -> dict:
    """Build the approved but non-authorizing execution candidate."""
    candidate = _base_candidate()
    candidate["review_checklist"] = _checklist(candidate)
    candidate["review_summary"] = _summary(candidate["review_checklist"])
    candidate["label_objective_redesign_execution_candidate_digest"] = (
        label_objective_redesign_execution_candidate_digest_v1(candidate)
    )
    validate_label_objective_redesign_execution_candidate_v1(candidate)
    return candidate


def _reject_forbidden_authority(value: Any, *, path: str = "candidate") -> None:
    forbidden_true_fields = {
        "label_objective_redesign_execution_candidate_review_created",
        "label_objective_redesign_authorized",
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "label_generation_authorized",
        "label_generation_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "label_objective_redesign_execution_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveRedesignExecutionCandidateError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise LabelObjectiveRedesignExecutionCandidateError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveRedesignExecutionCandidateError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_label_objective_redesign_execution_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate exact bindings and keep execution authority closed."""
    if not isinstance(candidate, dict):
        raise LabelObjectiveRedesignExecutionCandidateError(
            "execution candidate must be a JSON object"
        )
    _reject_forbidden_authority(candidate)
    expected_base = _base_candidate()
    for field, expected in expected_base.items():
        _expect(candidate.get(field), expected, field)
    checklist = candidate.get("review_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveRedesignExecutionCandidateError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise LabelObjectiveRedesignExecutionCandidateError(
            "review_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("review_summary"), expected_summary, "review_summary")
    digest = candidate.get("label_objective_redesign_execution_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignExecutionCandidateError(
            "label objective redesign execution candidate digest missing"
        )
    _expect(
        digest,
        label_objective_redesign_execution_candidate_digest_v1(candidate),
        "label_objective_redesign_execution_candidate_digest",
    )
    return {
        "status": "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "label_objective_redesign_execution_candidate_digest": digest,
        "ready_for_operator_review": True,
        "ready_for_label_objective_redesign_execution_approval": False,
        "ready_for_label_objective_redesign_execution": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_label_objective_redesign_execution_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated execution candidate as planning-only Markdown."""
    validate_label_objective_redesign_execution_candidate_v1(candidate)
    summary = candidate["review_summary"]
    lines = [
        "# MarketFlow Label Objective Redesign Execution Candidate",
        "",
        "## Title",
        "- Label Objective Redesign Execution Candidate v1.",
        "",
        "## Label Objective Redesign Execution Candidate",
        f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
        "",
        "## Bound Evidence",
    ]
    lines.extend(f"- {field}: `{candidate[field]}`." for field in REQUIRED_DIGEST_FIELDS)
    lines.extend([
        "",
        "## Dataset and Universe",
        f"- Dataset: `{candidate['dataset_name']}`; records: `{candidate['total_canonical_record_count']}`.",
        f"- Universe: `{', '.join(candidate['target_universe'])}`; META records: `{candidate['meta_record_count']}`.",
        "",
        "## Execution Candidate Objective",
        f"- Objective: `{candidate['label_objective_redesign_execution_candidate_objective']}`.",
        f"- Scope/mode: `{candidate['label_objective_redesign_execution_candidate_scope']}` / `{candidate['label_objective_redesign_execution_candidate_mode']}`.",
        "",
        "## Problem Basis",
    ])
    lines.extend(f"- {key}: `{value}`." for key, value in candidate["problem_basis"].items())
    for heading, key, id_key in [
        ("Planned Execution Activities", "planned_execution_activities", "activity_id"),
        ("Planned Workstreams", "planned_workstreams", "workstream_id"),
        ("Planned Label Family Outputs", "planned_label_family_outputs", "label_family_candidate_id"),
        ("Planned Execution Outputs", "planned_execution_outputs", "output_id"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_key]}`." for item in candidate[key])
    lines.extend(["", "## Per-Ticker Entries"])
    lines.extend(f"- `{item['ticker']}`: `{item['historical_record_count']}` records; execution unauthorized." for item in candidate["per_ticker_entries"])
    for heading, key in [
        ("Future Chain", "future_chain"),
        ("Future Gates", "future_gates"),
        ("Risk Controls", "risk_controls"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in candidate[key])
    lines.extend([
        "",
        "## Checklist Summary",
        f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "",
        "## Guardrails",
        "- Planning only; no redesign authorization or execution, label or feature generation, predictive acceptance, runtime, trading, or recommendations.",
    ])
    return "\n".join(lines)


def write_label_objective_redesign_execution_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write one canonical execution-candidate JSON without overwriting."""
    candidate = build_label_objective_redesign_execution_candidate_v1()
    validation = validate_label_objective_redesign_execution_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "label_objective_redesign_execution_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LabelObjectiveRedesignExecutionCandidateError(
            "execution candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise LabelObjectiveRedesignExecutionCandidateError(
            "execution candidate output already exists"
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
