"""Offline planning candidate for redesigning predictive label objectives."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    predictive_evidence_operator_method_path_selection_service as selection,
)


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_V1 = (
    "label_objective_redesign_candidate_v1"
)
LABEL_OBJECTIVE_REDESIGN_READY_FOR_OPERATOR_REVIEW = (
    "LABEL_OBJECTIVE_REDESIGN_READY_FOR_OPERATOR_REVIEW"
)
LABEL_OBJECTIVE_REDESIGN_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
LABEL_OBJECTIVE_REDESIGN_MODE = "PLANNED_NOT_EXECUTED"
LABEL_OBJECTIVE_REDESIGN_AUTHORITY_STATUS = "NOT_AUTHORIZED"
LABEL_OBJECTIVE_REDESIGN_OBJECTIVE = (
    "PLAN_LABEL_OBJECTIVE_AND_PREDICTION_TARGET_REDESIGN_AFTER_TWO_NOT_READY_"
    "READINESS_GATES"
)
SELECTED_METHOD_PATH = (
    selection.SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE
)

EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST = (
    "2f771999ff5e31dbd959ea1a33b08852cda46913ff1b5dfc6fe17bc0853ee14a"
)
EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST = (
    selection.EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST
)
EXPECTED_PLANNING_TREE_REVIEW_DIGEST = selection.EXPECTED_PLANNING_TREE_REVIEW_DIGEST
EXPECTED_LATEST_READINESS_DIGEST = selection.EXPECTED_LATEST_READINESS_DIGEST
EXPECTED_LATEST_REASSESSMENT_DIGEST = selection.EXPECTED_LATEST_REASSESSMENT_DIGEST
EXPECTED_REFINED_RESULTS_REVIEW_DIGEST = selection.EXPECTED_REFINED_RESULTS_REVIEW_DIGEST
EXPECTED_ORIGINAL_READINESS_DIGEST = selection.EXPECTED_ORIGINAL_READINESS_DIGEST
EXPECTED_ORIGINAL_REASSESSMENT_DIGEST = selection.EXPECTED_ORIGINAL_REASSESSMENT_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    selection.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_RECORDS_DIGEST = selection.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(selection.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(selection.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = selection.NOT_ACCEPTED
NOT_AUTHORIZED = selection.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = selection.RESEARCH_ONLY_NON_ACTIONABLE
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_DIGEST_FIELDS = {
    "operator_method_path_selection_digest": EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
    "predictive_evidence_method_diagnostic_review_package_digest": EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
    "predictive_evidence_planning_tree_review_package_digest": EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
    "latest_readiness_rerun_using_refined_evidence_digest": EXPECTED_LATEST_READINESS_DIGEST,
    "latest_reassessment_rerun_using_refined_evidence_digest": EXPECTED_LATEST_REASSESSMENT_DIGEST,
    "refined_results_review_digest": EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
    "original_acceptance_readiness_review_digest": EXPECTED_ORIGINAL_READINESS_DIGEST,
    "original_reassessment_review_digest": EXPECTED_ORIGINAL_REASSESSMENT_DIGEST,
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

DIAGNOSTIC_HYPOTHESES = [
    "label_objective_may_not_match_tradeable_signal",
    "prediction_horizon_may_not_match_available_features",
    "thresholds_may_create_noisy_or_imbalanced_classes",
    "absolute_return_labels_may_ignore_market_regime",
    "directional_labels_may_be_too_weak_for_daily_timeframe",
    "flat_or_no_trade_zone_may_be_missing",
    "risk_adjusted_target_may_be_more_relevant_than_raw_return",
    "benchmark_relative_target_may_be_required",
    "per_ticker_calibrated_labels_may_be_needed",
    "global_thresholds_may_not_fit_all_tickers",
    "class_balance_may_be unstable_across_windows",
    "label_availability_boundaries_may_affect_late_window_evaluation",
    "META_limitation_must_remain_preserved",
]

REDESIGN_DIMENSIONS = [
    "tradeability_alignment_dimension",
    "prediction_horizon_dimension",
    "return_threshold_dimension",
    "flat_return_tolerance_dimension",
    "class_balance_dimension",
    "absolute_vs_relative_return_dimension",
    "risk_adjusted_return_dimension",
    "drawdown_avoidance_dimension",
    "volatility_regime_conditioning_dimension",
    "benchmark_relative_performance_dimension",
    "per_ticker_calibration_dimension",
    "global_vs_ticker_specific_threshold_dimension",
    "late_window_label_availability_dimension",
    "meta_record_limitation_dimension",
]

LABEL_FAMILY_CANDIDATES = [
    "LABEL_FAMILY_CANDIDATE_DIRECTION_WITH_FLAT_ZONE",
    "LABEL_FAMILY_CANDIDATE_RETURN_BUCKET_REDESIGNED_THRESHOLDS",
    "LABEL_FAMILY_CANDIDATE_MULTI_HORIZON_5_10_20",
    "LABEL_FAMILY_CANDIDATE_BENCHMARK_RELATIVE_RETURN",
    "LABEL_FAMILY_CANDIDATE_VOLATILITY_ADJUSTED_RETURN",
    "LABEL_FAMILY_CANDIDATE_DRAWDOWN_AVOIDANCE",
    "LABEL_FAMILY_CANDIDATE_RISK_REWARD_ASYMMETRIC_TARGET",
    "LABEL_FAMILY_CANDIDATE_REGIME_CONDITIONED_DIRECTION",
    "LABEL_FAMILY_CANDIDATE_PER_TICKER_CALIBRATED_TARGET",
    "LABEL_FAMILY_CANDIDATE_NO_TRADE_ZONE_CLASS",
]

EVALUATION_QUESTIONS = [
    "does_label_match_tradeable_decision",
    "does_horizon_match_feature_information_content",
    "does_flat_zone_reduce_noise",
    "does_relative_return_reduce_market_beta_noise",
    "does_per_ticker_calibration_reduce_threshold_mismatch",
    "does_risk_adjusted_target_improve_stability",
    "does_drawdown_target_capture_useful_risk_signal",
    "does_regime_conditioning_reduce_instability",
    "does_label_balance_remain_stable_across_walk_forward_windows",
    "does_meta_record_limitation_change_label_availability_assessment",
]

FUTURE_CHAIN = [
    "Label Objective Redesign Candidate Operator Review Package v1.",
    "Label Objective Redesign Approval Ceremony v1, if selected.",
    "Label Objective Redesign Execution Candidate v1.",
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
    "label_objective_redesign_candidate_operator_review",
    "label_objective_redesign_approval_if_selected",
    "label_objective_redesign_execution_candidate",
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
    "candidate_does_not_authorize_label_generation",
    "candidate_does_not_authorize_execution",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "preserve_meta_record_limitation",
    "no_more_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

PLANNED_OUTPUTS = [
    "label_objective_redesign_manifest",
    "label_family_candidate_matrix",
    "threshold_design_matrix",
    "horizon_design_matrix",
    "per_ticker_label_objective_plan",
    "label_availability_boundary_plan",
    "operator_review_summary_template",
]

CHECK_IDS = [
    "operator_method_path_selection_digest_bound",
    "method_diagnostic_digest_bound",
    "planning_tree_digest_bound",
    "latest_readiness_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "selected_method_path_label_objective_redesign",
    "label_objective_redesign_candidate_created_true",
    "label_objective_redesign_ready_for_operator_review_true",
    "label_objective_redesign_not_approved",
    "label_objective_redesign_not_authorized",
    "label_objective_redesign_not_executed",
    "redesigned_label_generation_not_authorized",
    "redesigned_label_generation_not_performed",
    "hypotheses_defined",
    "redesign_dimensions_defined",
    "label_family_candidates_defined",
    "evaluation_questions_defined",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "future_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "no_provider_requests",
    "no_market_data_acquisition",
    "no_dataset_regeneration",
    "no_label_generation",
    "no_feature_generation",
    "no_metric_recomputation",
    "no_model_training",
    "no_strategy_scoring",
    "no_runtime_activation",
    "no_tracked_marketflow_files",
]


class LabelObjectiveRedesignCandidateError(ValueError):
    """Raised when the planning candidate violates its closed authority scope."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignCandidateError(f"{field} mismatch")


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


def _diagnostic_hypotheses() -> list[dict[str, Any]]:
    return [
        {
            "hypothesis_id": hypothesis_id,
            "hypothesis_status": "DIAGNOSTIC_HYPOTHESIS_NOT_TESTED",
            "evidence_basis": "TWO_NOT_READY_READINESS_GATES_AND_WEAK_OR_MIXED_METHOD_SIGNALS",
            "potential_effect": "MAY_LIMIT_STABLE_OUT_OF_SAMPLE_PREDICTIVE_EVIDENCE",
            "requires_future_design_review": True,
            "execution_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for hypothesis_id in DIAGNOSTIC_HYPOTHESES
    ]


def _redesign_dimensions() -> list[dict[str, Any]]:
    return [
        {
            "dimension_id": dimension_id,
            "dimension_status": "PLANNED_FOR_OPERATOR_REVIEW",
            "design_status": "NOT_DESIGNED",
            "authorization_status": NOT_AUTHORIZED,
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for dimension_id in REDESIGN_DIMENSIONS
    ]


def _label_family_candidates() -> list[dict[str, Any]]:
    return [
        {
            "label_family_candidate_id": candidate_id,
            "candidate_status": "PLANNED_NOT_GENERATED",
            "design_status": "CANDIDATE_ONLY",
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for candidate_id in LABEL_FAMILY_CANDIDATES
    ]


def _evaluation_questions() -> list[dict[str, Any]]:
    return [
        {
            "question_id": question_id,
            "question_status": "PLANNED_FOR_FUTURE_REVIEW",
            "answer_status": "NOT_ANSWERED",
            "requires_execution": False,
            "research_only": True,
        }
        for question_id in EVALUATION_QUESTIONS
    ]


def _per_ticker_digest(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_label_objective_redesign_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "selected_method_path": SELECTED_METHOD_PATH,
            "label_objective_redesign_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
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
            "source_operator_method_path_selection_digest": EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        }
        if is_meta:
            entry["redesign_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_LABEL_AVAILABILITY_LIMITATION"
            )
        entry["per_ticker_label_objective_redesign_candidate_digest"] = (
            _per_ticker_digest(entry)
        )
        entries.append(entry)
    return entries


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "output_status": "PLANNED_NOT_GENERATED",
            "authority": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUTS
    ]


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_V1,
        "candidate_status": LABEL_OBJECTIVE_REDESIGN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "operator_method_path_selection_created": True,
        "method_path_selected": True,
        "selected_method_path": SELECTED_METHOD_PATH,
        "label_objective_redesign_candidate_created": True,
        "label_objective_redesign_ready_for_operator_review": True,
        "label_objective_redesign_approved": False,
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
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "label_objective_redesign_objective": LABEL_OBJECTIVE_REDESIGN_OBJECTIVE,
        "label_objective_redesign_scope": LABEL_OBJECTIVE_REDESIGN_SCOPE,
        "label_objective_redesign_mode": LABEL_OBJECTIVE_REDESIGN_MODE,
        "label_objective_redesign_authority_status": LABEL_OBJECTIVE_REDESIGN_AUTHORITY_STATUS,
        "problem_basis": {
            "two_readiness_gates_not_ready": True,
            "original_readiness_decision": selection.ORIGINAL_READINESS_DECISION,
            "refined_readiness_decision": selection.REFINED_READINESS_DECISION,
            "method_diagnostic_conclusion": "METHOD_REVIEW_REQUIRED_BEFORE_MORE_EXECUTION",
            "overall_method_signal_status": "WEAK_OR_MIXED",
            "baseline_outperformance_status": "INSUFFICIENT_OR_MIXED",
            "oos_generalization_status": "LOW_TO_MIXED",
        },
        "evidence_comparison": {
            "original_oos_majority_accuracy": "0.539491",
            "original_oos_previous_direction_accuracy": "0.495984",
            "original_oos_ticker_cross_sectional_accuracy": "0.502677",
            "original_oos_brier_score": "0.24875351",
            "refined_oos_accuracy_range": "0.119813 to 0.480924",
            "refined_signal_consistency": "WEAK_OR_MIXED",
            "refined_baseline_outperformance": "INSUFFICIENT_OR_MIXED",
            "refined_model_comparison": "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE",
        },
        "diagnostic_hypotheses": _diagnostic_hypotheses(),
        "redesign_dimensions": _redesign_dimensions(),
        "label_family_candidates": _label_family_candidates(),
        "evaluation_questions": _evaluation_questions(),
        "per_ticker_entries": _per_ticker_entries(),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
    }


def _derived_checks(candidate: dict[str, Any]) -> dict[str, bool]:
    entries = candidate.get("per_ticker_entries", [])
    outputs = candidate.get("planned_outputs", [])
    counts = candidate.get("per_ticker_record_counts", {})
    return {
        "operator_method_path_selection_digest_bound": candidate.get("operator_method_path_selection_digest") == EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "method_diagnostic_digest_bound": candidate.get("predictive_evidence_method_diagnostic_review_package_digest") == EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "planning_tree_digest_bound": candidate.get("predictive_evidence_planning_tree_review_package_digest") == EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "latest_readiness_digest_bound": candidate.get("latest_readiness_rerun_using_refined_evidence_digest") == EXPECTED_LATEST_READINESS_DIGEST,
        "research_registry_digest_bound": candidate.get("research_registry_approval_digest") == EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest_bound": candidate.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": candidate.get("target_universe_count") == 12 and candidate.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": candidate.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": candidate.get("meta_record_count") == 913 and counts.get("META") == 913 and candidate.get("meta_reduced_record_count_preserved") is True,
        "selected_method_path_label_objective_redesign": candidate.get("selected_method_path") == SELECTED_METHOD_PATH,
        "label_objective_redesign_candidate_created_true": candidate.get("label_objective_redesign_candidate_created") is True,
        "label_objective_redesign_ready_for_operator_review_true": candidate.get("label_objective_redesign_ready_for_operator_review") is True,
        "label_objective_redesign_not_approved": candidate.get("label_objective_redesign_approved") is False,
        "label_objective_redesign_not_authorized": candidate.get("label_objective_redesign_authorized") is False,
        "label_objective_redesign_not_executed": candidate.get("label_objective_redesign_executed") is False,
        "redesigned_label_generation_not_authorized": candidate.get("redesigned_label_generation_authorized") is False,
        "redesigned_label_generation_not_performed": candidate.get("redesigned_label_generation_performed") is False,
        "hypotheses_defined": [item.get("hypothesis_id") for item in candidate.get("diagnostic_hypotheses", []) if isinstance(item, dict)] == DIAGNOSTIC_HYPOTHESES,
        "redesign_dimensions_defined": [item.get("dimension_id") for item in candidate.get("redesign_dimensions", []) if isinstance(item, dict)] == REDESIGN_DIMENSIONS,
        "label_family_candidates_defined": [item.get("label_family_candidate_id") for item in candidate.get("label_family_candidates", []) if isinstance(item, dict)] == LABEL_FAMILY_CANDIDATES,
        "evaluation_questions_defined": [item.get("question_id") for item in candidate.get("evaluation_questions", []) if isinstance(item, dict)] == EVALUATION_QUESTIONS,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12 and [item.get("ticker") for item in entries if isinstance(item, dict)] == TARGET_UNIVERSE,
        "per_ticker_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_label_objective_redesign_candidate_digest"), str) and len(item["per_ticker_label_objective_redesign_candidate_digest"]) == 64 and item["per_ticker_label_objective_redesign_candidate_digest"] == _per_ticker_digest(item) for item in entries if isinstance(item, dict)),
        "future_chain_defined": candidate.get("future_chain") == FUTURE_CHAIN,
        "future_gates_defined": candidate.get("future_gates") == FUTURE_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "planned_outputs_not_generated": isinstance(outputs, list) and len(outputs) == len(PLANNED_OUTPUTS) and all(item.get("output_status") == "PLANNED_NOT_GENERATED" for item in outputs if isinstance(item, dict)),
        "planned_outputs_research_only": isinstance(outputs, list) and len(outputs) == len(PLANNED_OUTPUTS) and all(item.get("authority") == RESEARCH_ONLY_NON_ACTIONABLE for item in outputs if isinstance(item, dict)),
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": candidate.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": candidate.get("runtime_migration_approved") is False and candidate.get("runtime_migration_active") is False and candidate.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": candidate.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": candidate.get("broker_execution") == NOT_AUTHORIZED and candidate.get("paper_trading") == NOT_AUTHORIZED,
        "trade_recommendations_false": candidate.get("trade_recommendations_generated") is False,
        "no_provider_requests": candidate.get("provider_requests_made") is False,
        "no_market_data_acquisition": candidate.get("market_data_acquisition_performed") is False,
        "no_dataset_regeneration": candidate.get("dataset_regeneration_performed") is False,
        "no_label_generation": candidate.get("label_generation_performed") is False and candidate.get("redesigned_label_generation_performed") is False,
        "no_feature_generation": candidate.get("feature_generation_performed") is False and candidate.get("redesigned_feature_generation_performed") is False,
        "no_metric_recomputation": candidate.get("metric_recomputation_performed") is False,
        "no_model_training": candidate.get("model_training_performed") is False,
        "no_strategy_scoring": candidate.get("new_strategy_scoring_performed") is False,
        "no_runtime_activation": candidate.get("runtime_migration_active") is False,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True and candidate.get("tracked_marketflow_files") == [],
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(candidate)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    blockers = sum(item.get("status") == FAIL and item.get("severity") == BLOCKER for item in checklist)
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "label_objective_redesign_candidate_ready": blockers == 0,
        "ready_for_operator_review": blockers == 0,
        "ready_for_label_objective_redesign_approval": False,
        "ready_for_label_objective_redesign_execution": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("label_objective_redesign_candidate_digest", None)
    return payload


def label_objective_redesign_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic digest for the planning candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_label_objective_redesign_candidate_v1() -> dict:
    """Build the offline, non-authorizing label-objective redesign candidate."""
    candidate = _base_candidate()
    candidate["review_checklist"] = _checklist(candidate)
    candidate["review_summary"] = _summary(candidate["review_checklist"])
    candidate["label_objective_redesign_candidate_digest"] = (
        label_objective_redesign_candidate_digest_v1(candidate)
    )
    validate_label_objective_redesign_candidate_v1(candidate)
    return candidate


def _reject_forbidden_authority(value: Any, *, path: str = "candidate") -> None:
    forbidden_true_fields = {
        "label_objective_redesign_approved",
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
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveRedesignCandidateError(f"{current} must remain false")
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise LabelObjectiveRedesignCandidateError(f"{current} must not be AUTHORIZED")
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveRedesignCandidateError(f"{current} must not be accepted")
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_label_objective_redesign_candidate_v1(candidate: dict) -> dict:
    """Validate exact evidence bindings and keep every downstream gate closed."""
    if not isinstance(candidate, dict):
        raise LabelObjectiveRedesignCandidateError("candidate must be a JSON object")
    _reject_forbidden_authority(candidate)
    expected_base = _base_candidate()
    for field, expected in expected_base.items():
        _expect(candidate.get(field), expected, field)
    checklist = candidate.get("review_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveRedesignCandidateError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise LabelObjectiveRedesignCandidateError("review_checklist contains a failed check")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("review_summary"), expected_summary, "review_summary")
    digest = candidate.get("label_objective_redesign_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignCandidateError("label objective redesign candidate digest missing")
    _expect(digest, label_objective_redesign_candidate_digest_v1(candidate), "label_objective_redesign_candidate_digest")
    return {
        "status": "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "label_objective_redesign_candidate_digest": digest,
        "ready_for_operator_review": True,
        "ready_for_label_objective_redesign_approval": False,
        "ready_for_label_objective_redesign_execution": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_label_objective_redesign_candidate_markdown_v1(candidate: dict) -> str:
    """Render the validated planning candidate as a non-actionable summary."""
    validate_label_objective_redesign_candidate_v1(candidate)
    summary = candidate["review_summary"]
    lines = [
        "# MarketFlow Label Objective Redesign Candidate",
        "",
        "## Title",
        "- Label Objective Redesign Candidate v1.",
        "",
        "## Label Objective Redesign Candidate",
        f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
        f"- Scope/mode: `{candidate['label_objective_redesign_scope']}` / `{candidate['label_objective_redesign_mode']}`.",
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
        "## Problem Basis",
    ])
    lines.extend(f"- {key}: `{value}`." for key, value in candidate["problem_basis"].items())
    for heading, key, id_key in [
        ("Diagnostic Hypotheses", "diagnostic_hypotheses", "hypothesis_id"),
        ("Redesign Dimensions", "redesign_dimensions", "dimension_id"),
        ("Planned Label Family Candidates", "label_family_candidates", "label_family_candidate_id"),
        ("Planned Evaluation Questions", "evaluation_questions", "question_id"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_key]}`." for item in candidate[key])
    lines.extend(["", "## Per-Ticker Entries"])
    lines.extend(f"- `{item['ticker']}`: `{item['historical_record_count']}` records; redesign not authorized." for item in candidate["per_ticker_entries"])
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
        "- Planning only; no approval, label or feature generation, predictive execution, acceptance, profitability, runtime, trading, or recommendations.",
    ])
    return "\n".join(lines)


def write_label_objective_redesign_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write one canonical candidate JSON without overwriting an existing file."""
    candidate = build_label_objective_redesign_candidate_v1()
    validation = validate_label_objective_redesign_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "label_objective_redesign_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LabelObjectiveRedesignCandidateError("candidate filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise LabelObjectiveRedesignCandidateError("candidate output already exists")
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
