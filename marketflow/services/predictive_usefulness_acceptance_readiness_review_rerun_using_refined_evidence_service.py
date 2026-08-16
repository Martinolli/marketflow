"""Offline refined-evidence acceptance-readiness rerun (not acceptance)."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    predictive_usefulness_reassessment_review_rerun_using_refined_evidence_service as reassessment,
)


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_V1 = (
    "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_COMPLETED = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_COMPLETED"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE"
)
READINESS_REASON_REFINED_EVIDENCE_WEAK_OR_MIXED_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE = (
    "REFINED_EVIDENCE_WEAK_OR_MIXED_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE"
)

EXPECTED_REASSESSMENT_RERUN_DIGEST = (
    "7520cd1c2f8d727ad7e94c0313c78e8bbb39bae410feeda539dd242ede28fcc0"
)
EXPECTED_REFINED_RESULTS_REVIEW_DIGEST = reassessment.EXPECTED_REFINED_RESULTS_REVIEW_DIGEST
EXPECTED_REFINED_EXECUTION_DIGEST = reassessment.EXPECTED_REFINED_EXECUTION_DIGEST
EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST = (
    reassessment.EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    reassessment.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = reassessment.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
EXPECTED_RECORDS_DIGEST = reassessment.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(reassessment.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(reassessment.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = reassessment.NOT_ACCEPTED
NOT_AUTHORIZED = reassessment.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = reassessment.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = reassessment.PLANNED_NOT_GENERATED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_MET = "FAIL_OR_NOT_MET"

READINESS_CRITERIA = [
    "leakage_controls_pass_required",
    "no_failed_controls_required",
    "minimum_refined_evidence_review_completion_required",
    "refined_oos_performance_minimum_required",
    "refined_signal_consistency_required",
    "refined_baseline_outperformance_required",
    "model_comparison_support_required",
    "calibration_stability_support_required",
    "operator_acceptance_boundary_required",
    "profitability_separation_required",
    "runtime_separation_required",
]

READINESS_FINDING_RESULTS = {
    "leakage_controls_pass_required": PASS,
    "no_failed_controls_required": PASS,
    "minimum_refined_evidence_review_completion_required": PASS,
    "refined_oos_performance_minimum_required": NOT_MET,
    "refined_signal_consistency_required": NOT_MET,
    "refined_baseline_outperformance_required": NOT_MET,
    "model_comparison_support_required": NOT_MET,
    "calibration_stability_support_required": NOT_MET,
    "operator_acceptance_boundary_required": PASS,
    "profitability_separation_required": PASS,
    "runtime_separation_required": PASS,
}

FUTURE_IMPROVEMENT_CHAIN = [
    "Refined Evidence Improvement Candidate, if desired.",
    "Additional refined feature/label/model evidence planning, if desired.",
    "Additional refined predictive evidence execution candidate, if new evidence is proposed.",
    "Additional refined predictive evidence execution approval and execution, if separately approved.",
    "Refined evidence results review.",
    "Predictive usefulness reassessment review rerun.",
    "Predictive usefulness acceptance readiness review rerun.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "refined_evidence_improvement_candidate_if_desired",
    "additional_refined_predictive_evidence_execution_candidate_if_new_evidence_proposed",
    "additional_refined_predictive_evidence_results_review_if_executed",
    "predictive_usefulness_reassessment_review_rerun_using_refined_evidence",
    "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_acceptance_when_readiness_not_met",
    "no_predictive_usefulness_acceptance_without_positive_readiness_decision",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_refined_evidence_without_new_approval",
    "weak_or_mixed_refined_signal_requires_improvement_or_additional_review",
    "low_or_mixed_oos_accuracy_not_acceptance_evidence",
    "model_comparison_not_acceptance_evidence_by_itself",
    "calibration_stability_not_acceptance_evidence_by_itself",
    "all_outputs_labeled_research_only",
]

PLANNED_OUTPUT_NAMES = [
    "refined_evidence_improvement_candidate_template",
    "additional_refined_evidence_planning_template",
    "future_readiness_rerun_template",
    "acceptance_candidate_template_if_ready_later",
    "operator_review_summary_template",
]

REGISTRY_APPROVED_DATASET_METADATA = deepcopy(
    reassessment.REGISTRY_APPROVED_DATASET_METADATA
)


class PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
    ValueError
):
    """Raised when the readiness rerun violates its non-accepting contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
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


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest",
        None,
    )
    return payload


def per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker readiness entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry: dict[str, Any] = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "refined_evidence_results_status": "REVIEWED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_rerun_status": (
                "REASSESSMENT_RERUN_COMPLETED_RESEARCH_ONLY"
            ),
            "predictive_usefulness_acceptance_readiness_rerun_status": (
                "NOT_READY_USING_REFINED_EVIDENCE"
            ),
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_reassessment_rerun_digest": EXPECTED_REASSESSMENT_RERUN_DIGEST,
        }
        if is_meta:
            entry["refinement_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_READINESS_RERUN"
            )
        entry[
            "per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"
        ] = per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _readiness_findings() -> list[dict[str, str]]:
    return [
        {"criterion_id": criterion, "result": READINESS_FINDING_RESULTS[criterion]}
        for criterion in READINESS_CRITERIA
    ]


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_name": name,
            "status": PLANNED_NOT_GENERATED,
            "label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _base_review() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_V1,
        "review_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_COMPLETED,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE,
        "readiness_reason": READINESS_REASON_REFINED_EVIDENCE_WEAK_OR_MIXED_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "feature_label_refinement_execution_rerun_performed": False,
        "refined_label_generation_rerun_performed": False,
        "refined_feature_generation_rerun_performed": False,
        "refined_walk_forward_reassessment_rerun_performed": False,
        "refined_out_of_sample_reassessment_rerun_performed": False,
        "refined_metrics_recomputation_performed": False,
        "refined_model_comparison_rerun_performed": False,
        "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created": True,
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_ready": True,
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created": True,
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_completed": True,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ceremony_ready": False,
        "ready_for_refined_evidence_improvement_or_additional_evidence_planning": True,
        "predictive_usefulness": NOT_ACCEPTED,
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
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest": EXPECTED_REASSESSMENT_RERUN_DIGEST,
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest": EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_for_refined_evidence_digest": EXPECTED_REFINED_EXECUTION_DIGEST,
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest": EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "registry_approved_dataset_metadata": deepcopy(
            REGISTRY_APPROVED_DATASET_METADATA
        ),
        "refined_label_family_count": 7,
        "refined_label_available_values": 82698,
        "refined_label_unavailable_values": 924,
        "refined_feature_group_count": 9,
        "refined_feature_category_count": 11,
        "refined_feature_field_count": 19,
        "refined_feature_rows": 11946,
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
        "refined_leakage_status": "PASS",
        "failed_leakage_controls": 0,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "refined_evidence_predictive_signal_consistency": "WEAK_OR_MIXED",
        "refined_baseline_outperformance_consistency": "INSUFFICIENT_OR_MIXED",
        "refined_oos_performance_assessment": (
            "LOW_TO_MIXED_NOT_ACCEPTANCE_EVIDENCE"
        ),
        "model_comparison_assessment": "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE",
        "calibration_stability_assessment": (
            "NOT_ACCEPTANCE_EVIDENCE_UNTIL_READINESS_REVIEW"
        ),
        "readiness_criteria": list(READINESS_CRITERIA),
        "readiness_findings": _readiness_findings(),
        "acceptance_candidate_allowed": False,
        "acceptance_ceremony_allowed": False,
        "additional_evidence_or_model_improvement_required": True,
        "per_ticker_readiness_entries": _per_ticker_entries(),
        "future_improvement_chain": list(FUTURE_IMPROVEMENT_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("reassessment_rerun_digest_bound", EXPECTED_REASSESSMENT_RERUN_DIGEST, "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest"),
    ("refined_results_review_digest_bound", EXPECTED_REFINED_RESULTS_REVIEW_DIGEST, "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"),
    ("refined_execution_digest_bound", EXPECTED_REFINED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_for_refined_evidence_digest"),
    ("refined_execution_approval_digest_bound", EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_for_refined_evidence_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_reassessment_rerun_universe", TARGET_UNIVERSE, "target_universe"),
    ("total_canonical_record_count_11946", 11946, "total_canonical_record_count"),
    ("meta_record_count_913_preserved", 913, "meta_record_count"),
    ("non_meta_record_counts_1003_preserved", True, "check_non_meta_record_counts"),
    ("reassessment_rerun_created_true", True, "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created"),
    ("reassessment_rerun_ready_true", True, "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_ready"),
    ("acceptance_readiness_rerun_created_true", True, "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created"),
    ("acceptance_readiness_rerun_completed_true", True, "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_completed"),
    ("refined_label_family_count_7", 7, "refined_label_family_count"),
    ("refined_feature_group_count_9", 9, "refined_feature_group_count"),
    ("refined_feature_fields_19", 19, "refined_feature_field_count"),
    ("refined_protocol_group_count_6", 6, "refined_protocol_group_count"),
    ("model_comparison_group_count_5", 5, "model_comparison_group_count"),
    ("refined_oos_rows_2988", 2988, "refined_oos_evaluation_rows"),
    ("refined_oos_accuracy_range_bound", "0.119813 to 0.480924", "refined_oos_accuracy_range"),
    ("refined_leakage_status_pass", "PASS", "refined_leakage_status"),
    ("failed_leakage_controls_zero", 0, "failed_leakage_controls"),
    ("data_quality_pass_with_preserved_limitation", "PASS_WITH_PRESERVED_SOURCE_LIMITATION", "data_quality_status"),
    ("leakage_controls_pass_required_pass", PASS, "finding_leakage_controls_pass_required"),
    ("no_failed_controls_required_pass", PASS, "finding_no_failed_controls_required"),
    ("minimum_refined_evidence_review_completion_required_pass", PASS, "finding_minimum_refined_evidence_review_completion_required"),
    ("refined_oos_performance_minimum_required_not_met", NOT_MET, "finding_refined_oos_performance_minimum_required"),
    ("refined_signal_consistency_required_not_met", NOT_MET, "finding_refined_signal_consistency_required"),
    ("refined_baseline_outperformance_required_not_met", NOT_MET, "finding_refined_baseline_outperformance_required"),
    ("model_comparison_support_required_not_met", NOT_MET, "finding_model_comparison_support_required"),
    ("calibration_stability_support_required_not_met", NOT_MET, "finding_calibration_stability_support_required"),
    ("readiness_decision_not_ready_using_refined_evidence", PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE, "readiness_decision"),
    ("readiness_reason_weak_or_mixed_and_insufficient_baseline_outperformance", READINESS_REASON_REFINED_EVIDENCE_WEAK_OR_MIXED_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE, "readiness_reason"),
    ("acceptance_candidate_allowed_false", False, "acceptance_candidate_allowed"),
    ("acceptance_ceremony_allowed_false", False, "acceptance_ceremony_allowed"),
    ("additional_evidence_or_model_improvement_required_true", True, "additional_evidence_or_model_improvement_required"),
    ("per_ticker_readiness_entries_12", 12, "check_per_ticker_entry_count"),
    ("per_ticker_readiness_digests_present", True, "check_per_ticker_digests"),
    ("future_improvement_chain_defined", FUTURE_IMPROVEMENT_CHAIN, "future_improvement_chain"),
    ("future_gates_defined", FUTURE_GATES, "future_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("planned_outputs_not_generated", True, "check_planned_outputs_not_generated"),
    ("planned_outputs_research_only", True, "check_planned_outputs_research_only"),
    ("provider_requests_made_in_review_false", False, "provider_requests_made_in_review"),
    ("live_provider_transport_enabled_in_review_false", False, "live_provider_transport_enabled_in_review"),
    ("market_data_acquisition_performed_in_review_false", False, "market_data_acquisition_performed_in_review"),
    ("dataset_generation_performed_in_review_false", False, "dataset_generation_performed_in_review"),
    ("canonical_dataset_regenerated_in_review_false", False, "canonical_dataset_regenerated_in_review"),
    ("feature_label_refinement_execution_rerun_performed_false", False, "feature_label_refinement_execution_rerun_performed"),
    ("refined_label_generation_rerun_performed_false", False, "refined_label_generation_rerun_performed"),
    ("refined_feature_generation_rerun_performed_false", False, "refined_feature_generation_rerun_performed"),
    ("refined_walk_forward_reassessment_rerun_performed_false", False, "refined_walk_forward_reassessment_rerun_performed"),
    ("refined_out_of_sample_reassessment_rerun_performed_false", False, "refined_out_of_sample_reassessment_rerun_performed"),
    ("refined_metrics_recomputation_performed_false", False, "refined_metrics_recomputation_performed"),
    ("refined_model_comparison_rerun_performed_false", False, "refined_model_comparison_rerun_performed"),
    ("additional_predictive_evidence_execution_for_refined_evidence_rerun_performed_false", False, "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("new_strategy_scoring_performed_false", False, "new_strategy_scoring_performed"),
    ("trade_recommendations_generated_false", False, "trade_recommendations_generated"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("predictive_usefulness_acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("predictive_usefulness_acceptance_recommended_false", False, "predictive_usefulness_acceptance_recommended"),
    ("predictive_usefulness_acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("profitability_acceptance_ready_false", False, "profitability_acceptance_ready"),
    ("profitability_acceptance_recommended_false", False, "profitability_acceptance_recommended"),
    ("runtime_migration_approved_false", False, "runtime_migration_approved"),
    ("runtime_use_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_use_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("paper_trading_not_authorized", NOT_AUTHORIZED, "paper_trading"),
    ("broker_execution_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("automatic_stitching_false", False, "automatic_stitching"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
]
REQUIRED_CHECK_IDS = [item[0] for item in CHECK_FIELD_SPECS]


def _derived_check_fields(review: dict[str, Any]) -> dict[str, Any]:
    findings = review.get("readiness_findings", [])
    entries = review.get("per_ticker_readiness_entries", [])
    planned = review.get("planned_outputs", [])
    counts = review.get("per_ticker_record_counts", {})
    values = {
        f"finding_{item.get('criterion_id')}": item.get("result")
        for item in findings
        if isinstance(item, dict)
    }
    values.update(
        {
            "check_non_meta_record_counts": isinstance(counts, dict)
            and all(
                counts.get(ticker) == 1003
                for ticker in TARGET_UNIVERSE
                if ticker != "META"
            ),
            "check_per_ticker_entry_count": len(entries)
            if isinstance(entries, list)
            else 0,
            "check_per_ticker_digests": isinstance(entries, list)
            and all(
                isinstance(item, dict)
                and isinstance(
                    item.get(
                        "per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"
                    ),
                    str,
                )
                and item[
                    "per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"
                ]
                == per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(
                    item
                )
                for item in entries
            ),
            "check_planned_outputs_not_generated": isinstance(planned, list)
            and len(planned) == len(PLANNED_OUTPUT_NAMES)
            and all(item.get("status") == PLANNED_NOT_GENERATED for item in planned),
            "check_planned_outputs_research_only": isinstance(planned, list)
            and len(planned) == len(PLANNED_OUTPUT_NAMES)
            and all(
                item.get("label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned
            ),
        }
    )
    return values


def _checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(review)
    values.update(_derived_check_fields(review))
    return [
        _check(check_id, expected, values.get(field))
        for check_id, expected, field in CHECK_FIELD_SPECS
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(row.get("status") == PASS for row in checklist)
    failed = total - passed
    blockers = sum(
        row.get("status") == FAIL and row.get("severity") == BLOCKER
        for row in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "acceptance_readiness_review_rerun_completed": True,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "ready_for_refined_evidence_improvement_or_additional_evidence_planning": blockers
        == 0,
    }


def _digest_payload(review: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review)
    payload.pop(
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest",
        None,
    )
    return payload


def predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(
    review: dict[str, Any],
) -> str:
    """Return the deterministic digest for the readiness rerun."""
    return semantic_digest(_digest_payload(review))


def build_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1() -> dict:
    """Build the exact not-ready decision from the reviewed refined evidence."""
    review = _base_review()
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review[
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"
    ] = predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(
        review
    )
    validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(
        review
    )
    return review


def _reject_forbidden_values(value: Any, *, path: str = "review") -> None:
    forbidden_artifacts = {
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_reassessment_rerun_performed",
        "refined_out_of_sample_reassessment_rerun_performed",
        "refined_metrics_recomputation_performed",
        "refined_model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ceremony_ready",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "acceptance_candidate_allowed",
        "acceptance_ceremony_allowed",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
                    f"{current} must not be accepted"
                )
            if key == "readiness_decision" and item != PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE:
                raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
                    f"{current} must remain not ready"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(
    review: dict,
) -> dict:
    """Validate exact refined-evidence binding and reject implied acceptance."""
    if not isinstance(review, dict):
        raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
            "acceptance readiness rerun must be a JSON object"
        )
    _reject_forbidden_values(review)
    expected_base = _base_review()
    for field, expected in expected_base.items():
        _expect(review.get(field), expected, field)
    checklist = review.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
            "review_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review)
    _expect(checklist, expected_checklist, "review_checklist")
    failed = [row for row in expected_checklist if row.get("status") != PASS]
    if failed:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review.get("review_summary"), expected_summary, "review_summary")
    digest = review.get(
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
            "acceptance readiness rerun digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(
            review
        ),
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_VALID",
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "readiness_decision": review["readiness_decision"],
        "readiness_reason": review["readiness_reason"],
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest": digest,
        "source_reassessment_rerun_digest": review[
            "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest"
        ],
        "per_ticker_readiness_entry_count": len(review["per_ticker_readiness_entries"]),
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "ready_for_refined_evidence_improvement_or_additional_evidence_planning": True,
    }


def build_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown summary of the refined not-ready decision."""
    validation = validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(
        review
    )
    metadata = review["registry_approved_dataset_metadata"]
    summary = review["review_summary"]
    lines = [
        "# MarketFlow Predictive Usefulness Acceptance Readiness Review Rerun Using Refined Evidence",
        "",
        "## Title",
        "- Predictive Usefulness Acceptance Readiness Review Rerun Using Refined Evidence v1.",
        "",
        "## Predictive Usefulness Acceptance Readiness Review Rerun Using Refined Evidence",
        f"- Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`",
        f"- Digest: `{validation['predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest']}`",
        "",
        "## Source Reassessment Rerun",
        f"- Reassessment digest: `{review['predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest']}`",
        f"- Refined-results digest: `{review['additional_predictive_evidence_results_review_for_refined_evidence_package_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/scope: `{metadata['dataset_name']}` / `{metadata['dataset_scope']}`",
        f"- Records/digest: `{metadata['total_canonical_record_count']}` / `{metadata['records_digest']}`",
        "",
        "## Target Universe",
        f"- `{', '.join(review['target_universe'])}`",
        "",
        "## Readiness Criteria",
    ]
    lines.extend(f"- `{criterion}`" for criterion in review["readiness_criteria"])
    lines.extend(["", "## Readiness Findings"])
    lines.extend(
        f"- `{finding['criterion_id']}`: `{finding['result']}`"
        for finding in review["readiness_findings"]
    )
    lines.extend(
        [
            "",
            "## Readiness Decision",
            f"- Decision/reason: `{review['readiness_decision']}` / `{review['readiness_reason']}`.",
            f"- Acceptance candidate/ceremony allowed: `{review['acceptance_candidate_allowed']}` / `{review['acceptance_ceremony_allowed']}`.",
            f"- Additional evidence or improvement required: `{review['additional_evidence_or_model_improvement_required']}`.",
            "",
            "## Per-Ticker Readiness Entries",
            f"- Entry count: `{len(review['per_ticker_readiness_entries'])}`; META remains 913 records and every other ticker remains 1003.",
            "",
            "## Future Improvement Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(review["future_improvement_chain"], start=1)
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review["risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness/readiness: `{review['predictive_usefulness']}` / `{review['predictive_usefulness_acceptance_ready']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{review['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{review['runtime_use']}` / `{review['strategy_use']}` / `{review['paper_trading']}` / `{review['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- The weak/mixed evidence is not ready for acceptance. No provider request, acquisition, regeneration, refined rerun, recomputation, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- Planned outputs remain not generated and research-only; future evidence improvement requires its own approval chain.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write one canonical readiness-rerun JSON file without overwriting."""
    review = build_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1()
    validation = validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or (
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
            "acceptance readiness rerun filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError(
            "acceptance readiness rerun output already exists"
        )
    payload = canonical_json_bytes(review)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
