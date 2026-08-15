"""Offline candidate for future additional predictive evidence using refined evidence."""

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
    feature_label_refinement_results_review_service as results_review,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_V1 = (
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_READY_FOR_OPERATOR_REVIEW = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_VALID"
)

EXPECTED_RESULTS_REVIEW_DIGEST = (
    "00604008d3c647f45896cd8b6707de519ed6eda4e32566b3c99910441ec6cc79"
)
EXPECTED_REFINEMENT_EXECUTION_DIGEST = results_review.EXPECTED_EXECUTION_DIGEST
EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST = (
    results_review.EXPECTED_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_DIGEST = (
    results_review.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_DIGEST = (
    results_review.EXPECTED_EXECUTION_CANDIDATE_DIGEST
)
EXPECTED_REFINEMENT_PLAN_APPROVAL_DIGEST = results_review.EXPECTED_PLAN_APPROVAL_DIGEST
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST = (
    "167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8"
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST = (
    "61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    results_review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    results_review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = results_review.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(results_review.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(results_review.EXPECTED_RECORD_COUNTS)
REGISTRY_APPROVED_DATASET_METADATA = {
    "dataset_name": "expanded_universe_canonical_dataset_v1",
    "dataset_scope": "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY",
    "registry_entry_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
    "source_profile": "RTH_FULL_SESSION_1D",
    "date_range_start": "2022-01-01",
    "date_range_end": "2025-12-31",
    "timeframe": "1d",
    "target_universe_count": 12,
    "total_canonical_record_count": 11946,
    "records_digest": EXPECTED_RECORDS_DIGEST,
    "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
    "registry_label": "RESEARCH_ONLY_NON_ACTIONABLE",
}

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
SOURCE_REVIEWED_NOT_REEXECUTED = "SOURCE_REVIEWED_NOT_REEXECUTED"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
NOT_AUTHORIZED_FOR_EXECUTION = "NOT_AUTHORIZED_FOR_EXECUTION"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_OBJECTIVE = (
    "PREPARE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REVIEWED_REFINED_FEATURE_LABEL_EVIDENCE"
)
CANDIDATE_SCOPE = (
    "REFINED_EVIDENCE_EXECUTION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
)
CANDIDATE_MODE = PLANNED_NOT_EXECUTED
CANDIDATE_AUTHORITY_STATUS = NOT_AUTHORIZED
SOURCE_REFINEMENT_OUTPUT_ROOT = (
    ".marketflow/feature_label_refinement/expanded_universe_v1/"
)

PLANNED_REFINED_EVIDENCE_INPUT_IDS = [
    "refined_label_generation_report",
    "refined_feature_generation_report",
    "refined_protocol_execution_report",
    "refined_model_comparison_report",
    "refined_walk_forward_report",
    "refined_out_of_sample_report",
    "refined_metric_report",
    "refined_leakage_control_report",
    "per_ticker_refinement_execution_summary",
    "feature_label_refinement_execution_digest_manifest",
]
PLANNED_EXECUTION_ACTIVITY_IDS = [
    "bind_reviewed_refined_label_evidence",
    "bind_reviewed_refined_feature_evidence",
    "bind_reviewed_refined_protocol_evidence",
    "bind_reviewed_model_comparison_evidence",
    "prepare_refined_additional_predictive_execution_manifest",
    "prepare_refined_walk_forward_reassessment",
    "prepare_refined_out_of_sample_reassessment",
    "prepare_refined_baseline_and_model_comparison_reassessment",
    "prepare_refined_calibration_and_stability_review",
    "prepare_refined_leakage_and_quality_review",
    "prepare_refined_operator_summary",
]
PLANNED_OUTPUT_IDS = [
    "refined_additional_predictive_evidence_execution_manifest",
    "refined_evidence_input_manifest",
    "refined_label_feature_binding_manifest",
    "refined_walk_forward_reassessment_report",
    "refined_out_of_sample_reassessment_report",
    "refined_baseline_model_comparison_report",
    "refined_calibration_stability_report",
    "refined_leakage_quality_report",
    "refined_execution_digest_manifest",
    "refined_operator_review_summary_template",
]
FUTURE_REFINED_EVIDENCE_EXECUTION_CHAIN = [
    "Additional Predictive Evidence Execution Candidate for Refined Evidence Operator Review Package.",
    "Additional Predictive Evidence Execution Approval Ceremony for Refined Evidence, if selected.",
    "Additional Predictive Evidence Execution for Refined Evidence.",
    "Additional Predictive Evidence Results Review for Refined Evidence.",
    "Predictive Usefulness Reassessment Review rerun using refined evidence.",
    "Predictive Usefulness Acceptance Readiness Review rerun.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
FUTURE_GATES = [
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_operator_review",
    "additional_predictive_evidence_execution_approval_for_refined_evidence_if_selected",
    "additional_predictive_evidence_execution_for_refined_evidence",
    "additional_predictive_evidence_results_review_for_refined_evidence",
    "predictive_usefulness_reassessment_review_rerun_using_refined_evidence",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_authorize_refined_evidence_execution",
    "no_execution_without_separate_operator_approval",
    "no_predictive_usefulness_acceptance_from_candidate",
    "no_acceptance_when_readiness_not_met",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_refinement_outputs_without_new_approval",
    "preserve_meta_reduced_record_count",
    "all_outputs_labeled_research_only",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
]

REQUIRED_CHECK_IDS = [
    "refinement_results_review_digest_bound",
    "refinement_execution_digest_bound",
    "refinement_execution_approval_digest_bound",
    "refinement_execution_candidate_review_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_results_review_universe",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "feature_label_refinement_results_review_ready_true",
    "refinement_results_support_future_additional_predictive_evidence_planning_true",
    "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence_true",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence_created_true",
    "candidate_scope_refined_evidence_candidate_only",
    "candidate_authority_status_not_authorized",
    "refined_label_family_count_7",
    "refined_label_available_values_82698",
    "refined_label_unavailable_values_924",
    "refined_feature_group_count_9",
    "refined_feature_fields_19",
    "refined_protocol_group_count_6",
    "model_comparison_group_count_5",
    "refined_walk_forward_fold_count_4",
    "refined_oos_rows_2988",
    "refined_oos_accuracy_range_bound",
    "refined_leakage_status_pass",
    "failed_leakage_controls_zero",
    "source_refinement_inputs_defined",
    "planned_execution_activities_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "per_ticker_candidate_entries_12",
    "per_ticker_candidate_digests_present",
    "future_refined_evidence_execution_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "live_provider_transport_enabled_false",
    "market_data_acquisition_performed_false",
    "dataset_generation_performed_false",
    "canonical_dataset_regenerated_false",
    "feature_label_refinement_execution_rerun_performed_false",
    "refined_label_generation_rerun_performed_false",
    "refined_feature_generation_rerun_performed_false",
    "refined_walk_forward_validation_rerun_performed_false",
    "refined_out_of_sample_evaluation_rerun_performed_false",
    "refined_metrics_recomputation_performed_false",
    "model_comparison_rerun_performed_false",
    "additional_predictive_evidence_execution_for_refined_evidence_approved_false",
    "additional_predictive_evidence_execution_for_refined_evidence_authorized_false",
    "additional_predictive_evidence_execution_for_refined_evidence_executed_false",
    "additional_predictive_evidence_results_for_refined_evidence_created_false",
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
    "no_additional_predictive_evidence_execution_approval_for_refined_evidence_created",
    "no_additional_predictive_evidence_execution_for_refined_evidence_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


class AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
    ValueError
):
    """Raised when the refined-evidence candidate violates its authority boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            f"{field} mismatch"
        )


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


def _planned_inputs() -> list[dict[str, Any]]:
    return [
        {
            "input_id": input_id,
            "source_status": SOURCE_REVIEWED_NOT_REEXECUTED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for input_id in PLANNED_REFINED_EVIDENCE_INPUT_IDS
    ]


def _planned_activities() -> list[dict[str, Any]]:
    return [
        {
            "activity_id": activity_id,
            "execution_status": PLANNED_NOT_EXECUTED,
            "authority_status": NOT_AUTHORIZED_FOR_EXECUTION,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for activity_id in PLANNED_EXECUTION_ACTIVITY_IDS
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one ticker candidate entry."""
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest",
        None,
    )
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
            "feature_label_refinement_results_status": "REVIEWED_RESEARCH_ONLY",
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "additional_predictive_evidence_execution_for_refined_evidence_authorized": False,
            "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        if ticker == "META":
            entry["refinement_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_REFINED_EVIDENCE_CHAIN"
            )
        digest_key = (
            "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
        )
        entry[digest_key] = (
            per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
                entry
            )
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_V1,
        "candidate_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_generation_performed": False,
        "canonical_dataset_regenerated": False,
        "feature_label_refinement_execution_rerun_performed": False,
        "refined_label_generation_rerun_performed": False,
        "refined_feature_generation_rerun_performed": False,
        "refined_walk_forward_validation_rerun_performed": False,
        "refined_out_of_sample_evaluation_rerun_performed": False,
        "refined_metrics_recomputation_performed": False,
        "model_comparison_rerun_performed": False,
        "additional_predictive_evidence_execution_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "feature_label_refinement_executed": True,
        "feature_label_refinement_results_created": True,
        "feature_label_refinement_results_review_created": True,
        "feature_label_refinement_results_review_ready": True,
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning": True,
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created": False,
        "additional_predictive_evidence_execution_for_refined_evidence_approved": False,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": False,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
        "additional_predictive_evidence_results_for_refined_evidence_created": False,
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
        "feature_label_refinement_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "feature_label_refinement_execution_digest": EXPECTED_REFINEMENT_EXECUTION_DIGEST,
        "feature_label_refinement_execution_approval_digest": EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
        "feature_label_refinement_execution_candidate_review_package_digest": EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        "feature_label_refinement_execution_candidate_digest": EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_DIGEST,
        "feature_label_refinement_plan_approval_digest": EXPECTED_REFINEMENT_PLAN_APPROVAL_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "registry_approved_dataset_metadata": deepcopy(
            REGISTRY_APPROVED_DATASET_METADATA
        ),
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "source_refinement_output_root": SOURCE_REFINEMENT_OUTPUT_ROOT,
        "source_refinement_output_count": 12,
        "source_refinement_output_status": "REVIEWED_AND_VERIFIED",
        "source_refinement_results_review_ready": True,
        "refined_label_family_count": 7,
        "refined_label_coverage_entries": 84,
        "refined_label_available_values": 82698,
        "refined_label_unavailable_values": 924,
        "refined_label_generation_digest": "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8",
        "refined_feature_group_count": 9,
        "refined_feature_category_count": 11,
        "refined_feature_field_count": 19,
        "refined_feature_rows": 11946,
        "refined_feature_null_or_unavailable_values": 1128,
        "refined_feature_generation_digest": "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00",
        "refined_protocol_group_count": 6,
        "chronological_splits": True,
        "one_session_embargo": True,
        "no_shuffle": True,
        "no_lookahead": True,
        "refined_walk_forward_fold_count": 4,
        "refined_walk_forward_evaluation_rows": 3024,
        "refined_oos_evaluation_rows": 2988,
        "refined_oos_accuracy_range": "0.119813 to 0.480924",
        "model_comparison_group_count": 5,
        "deterministic_comparisons_evaluated": 7,
        "unavailable_model_family_requests": 3,
        "unavailable_model_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "refined_leakage_status": PASS,
        "failed_leakage_controls": 0,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_objective": CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_scope": CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_mode": CANDIDATE_MODE,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status": CANDIDATE_AUTHORITY_STATUS,
        "planned_refined_evidence_inputs": _planned_inputs(),
        "planned_execution_activities": _planned_activities(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "future_refined_evidence_execution_chain": list(
            FUTURE_REFINED_EVIDENCE_EXECUTION_CHAIN
        ),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "additional_predictive_evidence_execution_approval_for_refined_evidence_artifact_created": False,
        "additional_predictive_evidence_execution_for_refined_evidence_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "refinement_results_review_digest_bound": (EXPECTED_RESULTS_REVIEW_DIGEST, candidate.get("feature_label_refinement_results_review_package_digest")),
        "refinement_execution_digest_bound": (EXPECTED_REFINEMENT_EXECUTION_DIGEST, candidate.get("feature_label_refinement_execution_digest")),
        "refinement_execution_approval_digest_bound": (EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST, candidate.get("feature_label_refinement_execution_approval_digest")),
        "refinement_execution_candidate_review_digest_bound": (EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_DIGEST, candidate.get("feature_label_refinement_execution_candidate_review_package_digest")),
        "research_registry_approval_digest_bound": (EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, candidate.get("research_registry_approval_digest")),
        "canonical_dataset_freeze_digest_bound": (EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, candidate.get("canonical_dataset_freeze_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, candidate.get("records_digest")),
        "target_universe_count_12": (12, candidate.get("target_universe_count")),
        "target_universe_matches_results_review_universe": (TARGET_UNIVERSE, candidate.get("target_universe")),
        "total_canonical_record_count_11946": (11946, candidate.get("total_canonical_record_count")),
        "meta_record_count_913_preserved": (913, candidate.get("meta_record_count")),
        "non_meta_record_counts_1003_preserved": (True, all(candidate.get("per_ticker_record_counts", {}).get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META")),
        "feature_label_refinement_results_review_ready_true": (True, candidate.get("feature_label_refinement_results_review_ready")),
        "refinement_results_support_future_additional_predictive_evidence_planning_true": (True, candidate.get("feature_label_refinement_results_support_future_additional_predictive_evidence_planning")),
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence_true": (True, candidate.get("ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence")),
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created_true": (True, candidate.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_created")),
        "candidate_scope_refined_evidence_candidate_only": (CANDIDATE_SCOPE, candidate.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_scope")),
        "candidate_authority_status_not_authorized": (NOT_AUTHORIZED, candidate.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status")),
        "refined_label_family_count_7": (7, candidate.get("refined_label_family_count")),
        "refined_label_available_values_82698": (82698, candidate.get("refined_label_available_values")),
        "refined_label_unavailable_values_924": (924, candidate.get("refined_label_unavailable_values")),
        "refined_feature_group_count_9": (9, candidate.get("refined_feature_group_count")),
        "refined_feature_fields_19": (19, candidate.get("refined_feature_field_count")),
        "refined_protocol_group_count_6": (6, candidate.get("refined_protocol_group_count")),
        "model_comparison_group_count_5": (5, candidate.get("model_comparison_group_count")),
        "refined_walk_forward_fold_count_4": (4, candidate.get("refined_walk_forward_fold_count")),
        "refined_oos_rows_2988": (2988, candidate.get("refined_oos_evaluation_rows")),
        "refined_oos_accuracy_range_bound": ("0.119813 to 0.480924", candidate.get("refined_oos_accuracy_range")),
        "refined_leakage_status_pass": (PASS, candidate.get("refined_leakage_status")),
        "failed_leakage_controls_zero": (0, candidate.get("failed_leakage_controls")),
        "source_refinement_inputs_defined": (_planned_inputs(), candidate.get("planned_refined_evidence_inputs")),
        "planned_execution_activities_defined": (_planned_activities(), candidate.get("planned_execution_activities")),
        "planned_outputs_not_generated": (True, bool(candidate.get("planned_outputs")) and all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in candidate.get("planned_outputs", []))),
        "planned_outputs_research_only": (True, bool(candidate.get("planned_outputs")) and all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in candidate.get("planned_outputs", []))),
        "per_ticker_candidate_entries_12": (12, len(candidate.get("per_ticker_candidate_entries", []))),
        "per_ticker_candidate_digests_present": (True, bool(candidate.get("per_ticker_candidate_entries")) and all(isinstance(item.get("per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"), str) and len(item["per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"]) == 64 for item in candidate.get("per_ticker_candidate_entries", []))),
        "future_refined_evidence_execution_chain_defined": (FUTURE_REFINED_EVIDENCE_EXECUTION_CHAIN, candidate.get("future_refined_evidence_execution_chain")),
        "future_gates_defined": (FUTURE_GATES, candidate.get("future_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
    }
    false_fields = {
        "provider_requests_made_false": "provider_requests_made",
        "live_provider_transport_enabled_false": "live_provider_transport_enabled",
        "market_data_acquisition_performed_false": "market_data_acquisition_performed",
        "dataset_generation_performed_false": "dataset_generation_performed",
        "canonical_dataset_regenerated_false": "canonical_dataset_regenerated",
        "feature_label_refinement_execution_rerun_performed_false": "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed_false": "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed_false": "refined_feature_generation_rerun_performed",
        "refined_walk_forward_validation_rerun_performed_false": "refined_walk_forward_validation_rerun_performed",
        "refined_out_of_sample_evaluation_rerun_performed_false": "refined_out_of_sample_evaluation_rerun_performed",
        "refined_metrics_recomputation_performed_false": "refined_metrics_recomputation_performed",
        "model_comparison_rerun_performed_false": "model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_for_refined_evidence_approved_false": "additional_predictive_evidence_execution_for_refined_evidence_approved",
        "additional_predictive_evidence_execution_for_refined_evidence_authorized_false": "additional_predictive_evidence_execution_for_refined_evidence_authorized",
        "additional_predictive_evidence_execution_for_refined_evidence_executed_false": "additional_predictive_evidence_execution_for_refined_evidence_executed",
        "additional_predictive_evidence_results_for_refined_evidence_created_false": "additional_predictive_evidence_results_for_refined_evidence_created",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready_false": "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended_false": "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created_false": "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready_false": "profitability_acceptance_ready",
        "profitability_acceptance_recommended_false": "profitability_acceptance_recommended",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "no_additional_predictive_evidence_execution_approval_for_refined_evidence_created": "additional_predictive_evidence_execution_approval_for_refined_evidence_artifact_created",
        "no_additional_predictive_evidence_execution_for_refined_evidence_created": "additional_predictive_evidence_execution_for_refined_evidence_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update(
        {check_id: (False, candidate.get(field)) for check_id, field in false_fields.items()}
    )
    values.update(
        {
            "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
            "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
            "runtime_use_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
            "strategy_use_not_authorized": (NOT_AUTHORIZED, candidate.get("strategy_use")),
            "paper_trading_not_authorized": (NOT_AUTHORIZED, candidate.get("paper_trading")),
            "broker_execution_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        }
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_review": not failed,
        "ready_for_additional_predictive_evidence_execution_approval_for_refined_evidence": False,
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate."""
    payload = deepcopy(candidate)
    payload.pop(
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest",
        None,
    )
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1() -> dict[str, Any]:
    """Build a planning-only candidate without replaying source evidence."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    ] = additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
        candidate
    )
    validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
        candidate
    )
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _validate_per_ticker_entries(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_candidate_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            "per_ticker_candidate_entries missing"
        )
    _expect(entries, _per_ticker_entries(), "per_ticker_candidate_entries")
    digest_key = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )
    for entry in entries:
        digest = entry.get(digest_key)
        if not isinstance(digest, str) or len(digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
                "per-ticker candidate digest missing"
            )
        _expect(
            digest,
            per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
                entry
            ),
            "per-ticker candidate digest",
        )


def validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is a complete non-authorizing candidate."""
    if not isinstance(candidate, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    exact_fields = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_V1,
        "candidate_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "feature_label_refinement_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "feature_label_refinement_execution_digest": EXPECTED_REFINEMENT_EXECUTION_DIGEST,
        "feature_label_refinement_execution_approval_digest": EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
        "feature_label_refinement_execution_candidate_review_package_digest": EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        "feature_label_refinement_execution_candidate_digest": EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_DIGEST,
        "feature_label_refinement_plan_approval_digest": EXPECTED_REFINEMENT_PLAN_APPROVAL_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "registry_approved_dataset_metadata": REGISTRY_APPROVED_DATASET_METADATA,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "source_refinement_output_root": SOURCE_REFINEMENT_OUTPUT_ROOT,
        "source_refinement_output_count": 12,
        "source_refinement_output_status": "REVIEWED_AND_VERIFIED",
        "refined_label_family_count": 7,
        "refined_label_coverage_entries": 84,
        "refined_label_available_values": 82698,
        "refined_label_unavailable_values": 924,
        "refined_label_generation_digest": "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8",
        "refined_feature_group_count": 9,
        "refined_feature_category_count": 11,
        "refined_feature_field_count": 19,
        "refined_feature_rows": 11946,
        "refined_feature_null_or_unavailable_values": 1128,
        "refined_feature_generation_digest": "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00",
        "refined_protocol_group_count": 6,
        "refined_walk_forward_fold_count": 4,
        "refined_walk_forward_evaluation_rows": 3024,
        "refined_oos_evaluation_rows": 2988,
        "refined_oos_accuracy_range": "0.119813 to 0.480924",
        "model_comparison_group_count": 5,
        "deterministic_comparisons_evaluated": 7,
        "unavailable_model_family_requests": 3,
        "unavailable_model_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "refined_leakage_status": PASS,
        "failed_leakage_controls": 0,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_objective": CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_scope": CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_mode": CANDIDATE_MODE,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status": CANDIDATE_AUTHORITY_STATUS,
        "planned_refined_evidence_inputs": _planned_inputs(),
        "planned_execution_activities": _planned_activities(),
        "planned_outputs": _planned_outputs(),
        "future_refined_evidence_execution_chain": FUTURE_REFINED_EVIDENCE_EXECUTION_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected in exact_fields.items():
        if field in {
            "planned_refined_evidence_inputs",
            "planned_execution_activities",
            "planned_outputs",
            "future_refined_evidence_execution_chain",
            "future_gates",
            "risk_controls",
        } and not candidate.get(field):
            raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
                f"{field} missing"
            )
        _expect(candidate.get(field), expected, field)
    true_fields = [
        "created_offline",
        "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized",
        "feature_label_refinement_executed",
        "feature_label_refinement_results_created",
        "feature_label_refinement_results_review_created",
        "feature_label_refinement_results_review_ready",
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning",
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_ready_for_operator_review",
        "source_refinement_results_review_ready",
        "chronological_splits",
        "one_session_embargo",
        "no_shuffle",
        "no_lookahead",
        "research_only",
        "operator_review_required",
    ]
    false_fields = [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_validation_rerun_performed",
        "refined_out_of_sample_evaluation_rerun_performed",
        "refined_metrics_recomputation_performed",
        "model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created",
        "additional_predictive_evidence_execution_for_refined_evidence_approved",
        "additional_predictive_evidence_execution_for_refined_evidence_authorized",
        "additional_predictive_evidence_execution_for_refined_evidence_executed",
        "additional_predictive_evidence_results_for_refined_evidence_created",
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
        "additional_predictive_evidence_execution_approval_for_refined_evidence_artifact_created",
        "additional_predictive_evidence_execution_for_refined_evidence_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ]
    for field in true_fields:
        _expect(candidate.get(field), True, field)
    for field in false_fields:
        _expect(candidate.get(field), False, field)
    _validate_per_ticker_entries(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            "candidate_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist],
        REQUIRED_CHECK_IDS,
        "candidate checklist IDs",
    )
    expected_checklist = _checklist(candidate)
    if any(item["status"] != PASS for item in expected_checklist):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            "candidate checklist contains a failed check"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get(
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            "candidate digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
            candidate
        ),
        "candidate digest",
    )
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": digest,
        "ready_for_operator_review": True,
        "blocker_count": 0,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": False,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_for_refined_evidence_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized Markdown summary of the planning-only candidate."""
    validation = validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
        candidate
    )
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Candidate for Refined Evidence",
        "",
        "## Title",
        "- Additional Predictive Evidence Execution Candidate for Refined Evidence v1.",
        "",
        "## Additional Predictive Evidence Execution Candidate for Refined Evidence",
        f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
        f"- Candidate digest: `{validation['additional_predictive_evidence_execution_candidate_for_refined_evidence_digest']}`.",
        "",
        "## Source Feature/Label Refinement Results Review",
        f"- Results-review digest: `{candidate['feature_label_refinement_results_review_package_digest']}`.",
        f"- Refinement-execution digest: `{candidate['feature_label_refinement_execution_digest']}`.",
        "",
        "## Registry-Approved Dataset Metadata",
    ]
    lines.extend(
        f"- {key}: `{value}`"
        for key, value in candidate["registry_approved_dataset_metadata"].items()
    )
    lines.extend(
        [
            "",
            "## Target Universe",
            f"- `{' '.join(candidate['target_universe'])}`.",
            "",
            "## Refined Evidence Source Profile",
            f"- Root/count/status: `{candidate['source_refinement_output_root']}` / `{candidate['source_refinement_output_count']}` / `{candidate['source_refinement_output_status']}`.",
            "",
            "## Refined Evidence Facts",
            f"- Labels/features/protocol/model groups: `{candidate['refined_label_family_count']}` / `{candidate['refined_feature_group_count']}` / `{candidate['refined_protocol_group_count']}` / `{candidate['model_comparison_group_count']}`.",
            f"- Walk-forward/OOS rows: `{candidate['refined_walk_forward_evaluation_rows']}` / `{candidate['refined_oos_evaluation_rows']}`.",
            "",
            "## Planned Refined Evidence Inputs",
        ]
    )
    lines.extend(
        f"- `{item['input_id']}`: `{item['source_status']}`."
        for item in candidate["planned_refined_evidence_inputs"]
    )
    lines.extend(["", "## Planned Execution Activities"])
    lines.extend(
        f"- `{item['activity_id']}`: `{item['execution_status']}`."
        for item in candidate["planned_execution_activities"]
    )
    lines.extend(["", "## Planned Outputs"])
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`."
        for item in candidate["planned_outputs"]
    )
    lines.extend(["", "## Per-Ticker Candidate Entries"])
    lines.extend(
        f"- `{item['ticker']}`: `{item['historical_record_count']}` records; `{item['additional_predictive_evidence_execution_candidate_for_refined_evidence_status']}`."
        for item in candidate["per_ticker_candidate_entries"]
    )
    for heading, key in (
        ("Future Refined-Evidence Execution Chain", "future_refined_evidence_execution_chain"),
        ("Future Gates", "future_gates"),
        ("Risk Controls", "risk_controls"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in candidate[key])
    lines.extend(
        [
            "",
            "## Execution Boundary",
            "- Candidate only; additional predictive evidence execution is neither approved, authorized, nor performed.",
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness remains `{candidate['predictive_usefulness']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability remains `{candidate['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{candidate['runtime_use']}` / `{candidate['strategy_use']}` / `{candidate['paper_trading']}` / `{candidate['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- No provider request, acquisition, dataset regeneration, refinement rerun, metrics recomputation, model-comparison rerun, strategy scoring, recommendation, acceptance, or runtime activation occurs.",
            "- Reviewed refined evidence remains research-only and non-actionable; META's exact 913-record limitation remains preserved.",
            "",
        ]
    )
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical candidate JSON once; existing output fails closed."""
    candidate = (
        build_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1()
    )
    validation = validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
        candidate
    )
    output_name = filename or (
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
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
        raise AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError(
            "candidate output already exists"
        ) from exc
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
