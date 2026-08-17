"""Offline candidate for future redesigned-label generation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import label_objective_redesign_results_review_service as review


ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE = (
    "REDESIGNED_LABEL_GENERATION_CANDIDATE"
)
SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_CANDIDATE_V1 = (
    "redesigned_label_generation_candidate_v1"
)
REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REDESIGNED_LABEL_GENERATION_CANDIDATE_VALID = (
    "REDESIGNED_LABEL_GENERATION_CANDIDATE_VALID"
)

DEFAULT_BRANCH = "feature/redesigned-label-generation-candidate-v1"
DEFAULT_BASE_COMMIT = "bc7ac4cb24ad326dec5afbe9c37898fce552d5b3"
EXPECTED_RESULTS_REVIEW_DIGEST = (
    "bda6012c74cffb8841a6b9568c0985e2b6d1c337c7b7fcf892da4b724fcb15f9"
)
EXPECTED_EXECUTION_DIGEST = review.EXPECTED_EXECUTION_DIGEST
EXPECTED_EXECUTION_APPROVAL_DIGEST = review.execution.EXPECTED_EXECUTION_APPROVAL_DIGEST
EXPECTED_EXECUTION_CANDIDATE_REVIEW_DIGEST = (
    review.execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_EXECUTION_CANDIDATE_DIGEST = review.execution.EXPECTED_EXECUTION_CANDIDATE_DIGEST
EXPECTED_REDESIGN_APPROVAL_DIGEST = review.execution.EXPECTED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_DIGEST
EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST = review.execution.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = review.execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
EXPECTED_RECORDS_DIGEST = review.execution.EXPECTED_RECORDS_DIGEST
TARGET_UNIVERSE = list(review.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = review.NOT_ACCEPTED
NOT_AUTHORIZED = review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_OBJECTIVE = (
    "PREPARE_REDESIGNED_LABEL_GENERATION_CANDIDATE_FROM_REVIEWED_LABEL_OBJECTIVE_REDESIGN_OUTPUTS"
)
CANDIDATE_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION"
CANDIDATE_MODE = "PLANNED_NOT_GENERATED"
CANDIDATE_AUTHORITY_STATUS = "NOT_AUTHORIZED"
SOURCE_OUTPUT_ROOT = ".marketflow/label_objective_redesign/expanded_universe_v1/"

SOURCE_DESIGN_INPUT_IDS = [
    "label_objective_redesign_execution_manifest",
    "label_family_candidate_matrix",
    "threshold_design_matrix",
    "horizon_design_matrix",
    "per_ticker_label_objective_plan",
    "label_availability_boundary_plan",
    "meta_limitation_preservation_plan",
    "operator_review_summary_template",
]
PLANNED_LABEL_FAMILY_IDS = [
    "REDESIGNED_LABEL_DIRECTION_WITH_FLAT_ZONE",
    "REDESIGNED_LABEL_RETURN_BUCKET_REDESIGNED_THRESHOLDS",
    "REDESIGNED_LABEL_MULTI_HORIZON_5_10_20",
    "REDESIGNED_LABEL_BENCHMARK_RELATIVE_RETURN",
    "REDESIGNED_LABEL_VOLATILITY_ADJUSTED_RETURN",
    "REDESIGNED_LABEL_DRAWDOWN_AVOIDANCE",
    "REDESIGNED_LABEL_RISK_REWARD_ASYMMETRIC_TARGET",
    "REDESIGNED_LABEL_REGIME_CONDITIONED_DIRECTION",
    "REDESIGNED_LABEL_PER_TICKER_CALIBRATED_TARGET",
    "REDESIGNED_LABEL_NO_TRADE_ZONE_CLASS",
]
PLANNED_THRESHOLD_STRATEGY_IDS = [
    "global_threshold_candidate",
    "per_ticker_threshold_candidate",
    "training_window_only_threshold_candidate",
    "volatility_adjusted_threshold_candidate",
    "benchmark_relative_threshold_candidate",
    "flat_zone_threshold_candidate",
    "class_balance_review_candidate",
]
PLANNED_HORIZON_STRATEGY_IDS = [
    "one_session_horizon_candidate",
    "five_session_horizon_candidate",
    "ten_session_horizon_candidate",
    "twenty_session_horizon_candidate",
    "multi_horizon_comparison_candidate",
]
PLANNED_AVAILABILITY_RULE_IDS = [
    "training_window_threshold_fit_only",
    "forward_tail_unavailable_labels_marked_null",
    "no_peek_label_generation",
    "late_window_label_availability_boundary",
    "meta_record_count_limitation_preserved",
    "no_synthetic_rows",
    "no_backfill",
    "no_calendar_inference",
]
PLANNED_OUTPUT_IDS = [
    "redesigned_label_generation_manifest",
    "redesigned_label_family_selection_matrix",
    "redesigned_threshold_generation_plan",
    "redesigned_horizon_generation_plan",
    "redesigned_per_ticker_label_generation_plan",
    "redesigned_label_availability_boundary_plan",
    "redesigned_meta_limitation_handling_plan",
    "redesigned_label_generation_operator_summary_template",
]
FUTURE_CHAIN = [
    "Redesigned Label Generation Candidate Operator Review Package v1.",
    "Redesigned Label Generation Approval v1, if selected.",
    "Redesigned Label Generation Execution v1.",
    "Redesigned Label Generation Results Review v1.",
    "Feature / Predictive Evidence Planning Candidate using redesigned labels, if results support it.",
    "Additional Predictive Evidence Execution Candidate using redesigned labels, if separately selected.",
    "Additional Predictive Evidence Execution and Results Review, if separately approved.",
    "Predictive Usefulness Reassessment and Readiness Review, only after new evidence.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
FUTURE_GATES = [
    "redesigned_label_generation_candidate_operator_review",
    "redesigned_label_generation_approval_if_selected",
    "redesigned_label_generation_execution",
    "redesigned_label_generation_results_review",
    "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels",
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
    "candidate_does_not_generate_actual_labels",
    "candidate_does_not_authorize_feature_generation",
    "candidate_does_not_authorize_predictive_evidence_execution",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "preserve_meta_record_limitation",
    "no_label_generation_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]
CHECK_IDS = [
    "label_objective_redesign_results_review_digest_bound",
    "label_objective_redesign_execution_digest_bound",
    "label_objective_redesign_execution_approval_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "results_review_ready_true",
    "ready_for_redesigned_label_generation_candidate_true",
    "redesigned_label_generation_candidate_created_true",
    "redesigned_label_generation_candidate_ready_for_operator_review_true",
    "redesigned_label_generation_candidate_review_created_false",
    "redesigned_label_generation_approved_false",
    "redesigned_label_generation_authorized_false",
    "redesigned_label_generation_performed_false",
    "actual_redesigned_labels_generated_false",
    "source_design_inputs_defined",
    "planned_label_families_10",
    "planned_threshold_strategies_7",
    "planned_horizon_strategies_5",
    "planned_availability_rules_defined",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "future_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "feature_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "no_actual_label_generation",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "no_tracked_marketflow_files",
]


class RedesignedLabelGenerationCandidateError(ValueError):
    """Raised when the candidate violates its planning-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise RedesignedLabelGenerationCandidateError(f"{field} mismatch")


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


def _source_design_inputs() -> list[dict[str, Any]]:
    return [
        {
            "source_input_id": input_id,
            "source_input_status": "SOURCE_REVIEWED_NOT_REGENERATED",
            "output_label": "RESEARCH_ONLY_NON_ACTIONABLE",
            "research_only": True,
            "non_actionable": True,
        }
        for input_id in SOURCE_DESIGN_INPUT_IDS
    ]


def _planned_label_families() -> list[dict[str, Any]]:
    return [
        {
            "planned_label_family_id": family_id,
            "planned_label_status": "PLANNED_NOT_GENERATED",
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "actual_label_values_created": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in PLANNED_LABEL_FAMILY_IDS
    ]


def _planned_threshold_strategies() -> list[dict[str, Any]]:
    return [
        {
            "threshold_strategy_id": strategy_id,
            "strategy_status": "PLANNED_NOT_COMPUTED",
            "threshold_computation_authorized": False,
            "threshold_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for strategy_id in PLANNED_THRESHOLD_STRATEGY_IDS
    ]


def _planned_horizon_strategies() -> list[dict[str, Any]]:
    return [
        {
            "horizon_strategy_id": strategy_id,
            "strategy_status": "PLANNED_NOT_COMPUTED",
            "horizon_selection_authorized": False,
            "horizon_selection_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for strategy_id in PLANNED_HORIZON_STRATEGY_IDS
    ]


def _planned_availability_rules() -> list[dict[str, Any]]:
    return [
        {
            "availability_rule_id": rule_id,
            "rule_status": "PLANNED_FOR_OPERATOR_REVIEW",
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for rule_id in PLANNED_AVAILABILITY_RULE_IDS
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "planned_output_id": output_id,
            "planned_output_status": "PLANNED_NOT_GENERATED",
            "output_label": "RESEARCH_ONLY_NON_ACTIONABLE",
            "research_only": True,
            "non_actionable": True,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def per_ticker_redesigned_label_generation_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one ticker candidate entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_redesigned_label_generation_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "source_label_objective_plan_status": "REVIEWED_DESIGN_ARTIFACT",
            "redesigned_label_generation_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "redesigned_label_generation_authorized": False,
            "redesigned_label_generation_performed": False,
            "actual_redesigned_labels_generated": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_label_objective_redesign_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        }
        if is_meta:
            entry["label_availability_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_NO_BACKFILL_OR_SYNTHETIC_LABELS"
            )
        entry["per_ticker_redesigned_label_generation_candidate_digest"] = (
            per_ticker_redesigned_label_generation_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_CANDIDATE_V1,
        "candidate_status": REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_regeneration_performed": False,
        "canonical_dataset_regenerated": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "label_objective_redesign_execution_approved": True,
        "label_objective_redesign_authorized": True,
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "label_objective_redesign_results_review_created": True,
        "label_objective_redesign_results_review_ready": True,
        "ready_for_redesigned_label_generation_candidate": True,
        "redesigned_label_generation_candidate_created": True,
        "redesigned_label_generation_candidate_ready_for_operator_review": True,
        "redesigned_label_generation_candidate_review_created": False,
        "redesigned_label_generation_approved": False,
        "redesigned_label_generation_authorized": False,
        "redesigned_label_generation_performed": False,
        "actual_redesigned_labels_generated": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "label_generation_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
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
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        "label_objective_redesign_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "label_objective_redesign_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "label_objective_redesign_execution_approval_digest": EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "label_objective_redesign_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        "label_objective_redesign_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "label_objective_redesign_approval_digest": EXPECTED_REDESIGN_APPROVAL_DIGEST,
        "operator_method_path_selection_digest": EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "redesigned_label_generation_candidate_objective": CANDIDATE_OBJECTIVE,
        "redesigned_label_generation_candidate_scope": CANDIDATE_SCOPE,
        "redesigned_label_generation_candidate_mode": CANDIDATE_MODE,
        "redesigned_label_generation_candidate_authority_status": CANDIDATE_AUTHORITY_STATUS,
        "source_label_objective_redesign_output_root": SOURCE_OUTPUT_ROOT,
        "source_label_objective_redesign_output_count": 8,
        "source_label_objective_redesign_output_status": "REVIEWED_AND_VERIFIED",
        "label_family_candidate_count": 10,
        "threshold_design_strategy_count": 7,
        "horizon_design_candidate_count": 5,
        "per_ticker_plan_count": 12,
        "planning_output_interpretation": "DESIGN_ARTIFACTS_READY_FOR_OPERATOR_REVIEW",
        "label_generation_interpretation": "NOT_GENERATED_NOT_AUTHORIZED",
        "predictive_usefulness_interpretation": "NOT_ACCEPTANCE_EVIDENCE",
        "source_design_inputs": _source_design_inputs(),
        "planned_redesigned_label_families": _planned_label_families(),
        "planned_threshold_strategies": _planned_threshold_strategies(),
        "planned_horizon_strategies": _planned_horizon_strategies(),
        "planned_label_availability_rules": _planned_availability_rules(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "planned_outputs": _planned_outputs(),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _derived_checks(candidate: dict[str, Any]) -> dict[str, bool]:
    entries = candidate.get("per_ticker_candidate_entries", [])
    inputs = candidate.get("source_design_inputs", [])
    families = candidate.get("planned_redesigned_label_families", [])
    thresholds = candidate.get("planned_threshold_strategies", [])
    horizons = candidate.get("planned_horizon_strategies", [])
    rules = candidate.get("planned_label_availability_rules", [])
    outputs = candidate.get("planned_outputs", [])
    counts = candidate.get("per_ticker_record_counts", {})
    return {
        "label_objective_redesign_results_review_digest_bound": candidate.get("label_objective_redesign_results_review_package_digest") == EXPECTED_RESULTS_REVIEW_DIGEST,
        "label_objective_redesign_execution_digest_bound": candidate.get("label_objective_redesign_execution_digest") == EXPECTED_EXECUTION_DIGEST,
        "label_objective_redesign_execution_approval_digest_bound": candidate.get("label_objective_redesign_execution_approval_digest") == EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "records_digest_bound": candidate.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": candidate.get("target_universe_count") == 12 and candidate.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": candidate.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": candidate.get("meta_record_count") == 913 and counts.get("META") == 913 and candidate.get("meta_reduced_record_count_preserved") is True,
        "results_review_ready_true": candidate.get("label_objective_redesign_results_review_ready") is True,
        "ready_for_redesigned_label_generation_candidate_true": candidate.get("ready_for_redesigned_label_generation_candidate") is True,
        "redesigned_label_generation_candidate_created_true": candidate.get("redesigned_label_generation_candidate_created") is True,
        "redesigned_label_generation_candidate_ready_for_operator_review_true": candidate.get("redesigned_label_generation_candidate_ready_for_operator_review") is True,
        "redesigned_label_generation_candidate_review_created_false": candidate.get("redesigned_label_generation_candidate_review_created") is False,
        "redesigned_label_generation_approved_false": candidate.get("redesigned_label_generation_approved") is False,
        "redesigned_label_generation_authorized_false": candidate.get("redesigned_label_generation_authorized") is False,
        "redesigned_label_generation_performed_false": candidate.get("redesigned_label_generation_performed") is False,
        "actual_redesigned_labels_generated_false": candidate.get("actual_redesigned_labels_generated") is False,
        "source_design_inputs_defined": [item.get("source_input_id") for item in inputs if isinstance(item, dict)] == SOURCE_DESIGN_INPUT_IDS,
        "planned_label_families_10": [item.get("planned_label_family_id") for item in families if isinstance(item, dict)] == PLANNED_LABEL_FAMILY_IDS,
        "planned_threshold_strategies_7": [item.get("threshold_strategy_id") for item in thresholds if isinstance(item, dict)] == PLANNED_THRESHOLD_STRATEGY_IDS,
        "planned_horizon_strategies_5": [item.get("horizon_strategy_id") for item in horizons if isinstance(item, dict)] == PLANNED_HORIZON_STRATEGY_IDS,
        "planned_availability_rules_defined": [item.get("availability_rule_id") for item in rules if isinstance(item, dict)] == PLANNED_AVAILABILITY_RULE_IDS,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12 and [item.get("ticker") for item in entries if isinstance(item, dict)] == TARGET_UNIVERSE,
        "per_ticker_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_redesigned_label_generation_candidate_digest"), str) and len(item["per_ticker_redesigned_label_generation_candidate_digest"]) == 64 and item["per_ticker_redesigned_label_generation_candidate_digest"] == per_ticker_redesigned_label_generation_candidate_digest_v1(item) for item in entries if isinstance(item, dict)),
        "future_chain_defined": candidate.get("future_chain") == FUTURE_CHAIN,
        "future_gates_defined": candidate.get("future_gates") == FUTURE_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "planned_outputs_not_generated": isinstance(outputs, list) and len(outputs) == 8 and all(item.get("planned_output_status") == "PLANNED_NOT_GENERATED" for item in outputs if isinstance(item, dict)),
        "planned_outputs_research_only": isinstance(outputs, list) and len(outputs) == 8 and all(item.get("output_label") == "RESEARCH_ONLY_NON_ACTIONABLE" and item.get("research_only") is True and item.get("non_actionable") is True for item in outputs if isinstance(item, dict)),
        "feature_generation_false": candidate.get("feature_generation_performed") is False and candidate.get("redesigned_feature_generation_performed") is False,
        "metric_recomputation_false": candidate.get("metric_recomputation_performed") is False,
        "model_training_false": candidate.get("model_training_performed") is False,
        "additional_predictive_evidence_execution_candidate_created_false": candidate.get("additional_predictive_evidence_execution_candidate_created") is False,
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": candidate.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": candidate.get("runtime_migration_approved") is False and candidate.get("runtime_migration_active") is False and candidate.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": candidate.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": candidate.get("paper_trading") == NOT_AUTHORIZED and candidate.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": candidate.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": candidate.get("provider_requests_made") is False,
        "market_data_acquisition_false": candidate.get("market_data_acquisition_performed") is False,
        "dataset_regeneration_false": candidate.get("dataset_regeneration_performed") is False and candidate.get("canonical_dataset_regenerated") is False,
        "no_actual_label_generation": candidate.get("label_generation_performed") is False and candidate.get("redesigned_label_generation_performed") is False and candidate.get("actual_redesigned_labels_generated") is False,
        "no_predictive_usefulness_acceptance_artifact_created": candidate.get("predictive_usefulness_acceptance_artifact_created") is False,
        "no_profitability_acceptance_created": candidate.get("profitability_acceptance_created") is False,
        "no_runtime_migration_approval_created": candidate.get("runtime_migration_approval_created") is False,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True and candidate.get("tracked_marketflow_files") == [],
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(candidate)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "redesigned_label_generation_candidate_ready": not failed,
        "ready_for_operator_review": not failed,
        "ready_for_redesigned_label_generation_approval": False,
        "ready_for_redesigned_label_generation_execution": False,
        "actual_redesigned_labels_generated": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def redesigned_label_generation_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic digest for the complete candidate."""
    payload = deepcopy(candidate)
    payload.pop("redesigned_label_generation_candidate_digest", None)
    return semantic_digest(payload)


def build_redesigned_label_generation_candidate_v1() -> dict[str, Any]:
    """Build the candidate without approving or generating any labels."""
    candidate = _base_candidate()
    candidate["review_checklist"] = _checklist(candidate)
    candidate["review_summary"] = _summary(candidate["review_checklist"])
    candidate["redesigned_label_generation_candidate_digest"] = (
        redesigned_label_generation_candidate_digest_v1(candidate)
    )
    validate_redesigned_label_generation_candidate_v1(candidate)
    return candidate


def _reject_forbidden_authority(value: Any, *, path: str = "candidate") -> None:
    forbidden_artifacts = {
        "REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE",
        "REDESIGNED_LABEL_GENERATION_APPROVED",
        "REDESIGNED_LABEL_GENERATION_EXECUTED",
        "LABEL_GENERATION_EXECUTED",
        "FEATURE_GENERATION_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true_fields = {
        "redesigned_label_generation_candidate_review_created",
        "redesigned_label_generation_approved",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "label_generation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
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
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "canonical_dataset_regenerated",
        "label_objective_redesign_execution_rerun_performed",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
        "label_generation_authorized",
        "actual_label_values_created",
        "threshold_computation_authorized",
        "threshold_computation_performed",
        "horizon_selection_authorized",
        "horizon_selection_performed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise RedesignedLabelGenerationCandidateError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true_fields and item is True:
                raise RedesignedLabelGenerationCandidateError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise RedesignedLabelGenerationCandidateError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise RedesignedLabelGenerationCandidateError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_redesigned_label_generation_candidate_v1(candidate: dict) -> dict[str, Any]:
    """Validate exact bindings and keep label-generation authority closed."""
    if not isinstance(candidate, dict):
        raise RedesignedLabelGenerationCandidateError(
            "redesigned label generation candidate must be a JSON object"
        )
    _reject_forbidden_authority(candidate)
    for field, expected in _base_candidate().items():
        _expect(candidate.get(field), expected, field)
    checklist = candidate.get("review_checklist")
    if not isinstance(checklist, list):
        raise RedesignedLabelGenerationCandidateError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise RedesignedLabelGenerationCandidateError(
            "review_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("review_summary"), expected_summary, "review_summary")
    digest = candidate.get("redesigned_label_generation_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise RedesignedLabelGenerationCandidateError(
            "redesigned label generation candidate digest missing"
        )
    _expect(
        digest,
        redesigned_label_generation_candidate_digest_v1(candidate),
        "redesigned_label_generation_candidate_digest",
    )
    return {
        "status": REDESIGNED_LABEL_GENERATION_CANDIDATE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "redesigned_label_generation_candidate_digest": digest,
        "ready_for_operator_review": True,
        "ready_for_redesigned_label_generation_approval": False,
        "ready_for_redesigned_label_generation_execution": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_redesigned_label_generation_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render the validated planning-only candidate as Markdown."""
    validate_redesigned_label_generation_candidate_v1(candidate)
    summary = candidate["review_summary"]
    lines = [
        "# MarketFlow Redesigned Label Generation Candidate", "",
        "## Title", "- Redesigned Label Generation Candidate v1.", "",
        "## Redesigned Label Generation Candidate", f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.", f"- Candidate digest: `{candidate['redesigned_label_generation_candidate_digest']}`.", "",
        "## Bound Evidence", f"- Results-review/execution/approval: `{candidate['label_objective_redesign_results_review_package_digest']}` / `{candidate['label_objective_redesign_execution_digest']}` / `{candidate['label_objective_redesign_execution_approval_digest']}`.", "",
        "## Dataset and Universe", f"- `{candidate['dataset_name']}` contains `{candidate['total_canonical_record_count']}` records for `{', '.join(candidate['target_universe'])}`; META remains `{candidate['meta_record_count']}`.", "",
        "## Source Design Artifacts",
    ]
    lines.extend(f"- `{item['source_input_id']}`: `{item['source_input_status']}`." for item in candidate["source_design_inputs"])
    for heading, key, id_key in [
        ("Planned Redesigned Label Families", "planned_redesigned_label_families", "planned_label_family_id"),
        ("Planned Threshold Strategies", "planned_threshold_strategies", "threshold_strategy_id"),
        ("Planned Horizon Strategies", "planned_horizon_strategies", "horizon_strategy_id"),
        ("Planned Availability Rules", "planned_label_availability_rules", "availability_rule_id"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_key]}`." for item in candidate[key])
    lines.extend(["", "## Per-Ticker Candidate Entries"])
    lines.extend(f"- `{item['ticker']}`: `{item['historical_record_count']}` records; labels not authorized or generated." for item in candidate["per_ticker_candidate_entries"])
    for heading, key in [("Future Chain", "future_chain"), ("Future Gates", "future_gates"), ("Risk Controls", "risk_controls")]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in candidate[key])
    lines.extend([
        "", "## Checklist Summary", f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "", "## Guardrails", "- Candidate only: no label or feature generation, predictive evidence, acceptance, profitability approval, runtime, trading, or recommendations.", "- The next task is a separate Redesigned Label Generation Candidate Operator Review Package v1.", "",
    ])
    return "\n".join(lines)


def write_redesigned_label_generation_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical candidate JSON without overwriting."""
    candidate = build_redesigned_label_generation_candidate_v1()
    validation = validate_redesigned_label_generation_candidate_v1(candidate)
    output_name = filename or "redesigned_label_generation_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise RedesignedLabelGenerationCandidateError(
            "candidate filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise RedesignedLabelGenerationCandidateError(
            "candidate output already exists"
        ) from exc
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
