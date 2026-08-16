"""Offline predictive-usefulness reassessment rerun over reviewed refined evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    additional_predictive_evidence_results_review_for_refined_evidence_service as source_review,
)


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_V1 = (
    "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_v1"
)
PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE_READY"
)

EXPECTED_REFINED_RESULTS_REVIEW_DIGEST = (
    "539d06be9b20edee5ff883030e4fd1091fdaefb468fa595001178bf7ec0740da"
)
EXPECTED_REFINED_EXECUTION_DIGEST = source_review.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST = (
    source_review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST = (
    source_review.EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST
)
EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST = (
    source_review.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST
)
EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST = source_review.EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST
EXPECTED_ORIGINAL_EXECUTION_DIGEST = source_review.EXPECTED_ORIGINAL_EXECUTION_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    source_review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = source_review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
EXPECTED_RECORDS_DIGEST = source_review.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(source_review.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(source_review.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = source_review.NOT_ACCEPTED
NOT_AUTHORIZED = source_review.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = source_review.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
NOT_ACCEPTANCE = "NOT_ACCEPTANCE"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEW_DOMAIN_RESULTS = {
    "refined_label_coverage_review": "REVIEWED_RESEARCH_ONLY",
    "refined_feature_coverage_review": "REVIEWED_RESEARCH_ONLY",
    "refined_protocol_review": "PASS_RESEARCH_ONLY",
    "refined_walk_forward_reassessment_review": (
        "WEAK_OR_MIXED_REQUIRES_READINESS_REVIEW"
    ),
    "refined_oos_reassessment_review": "LOW_TO_MIXED_REQUIRES_READINESS_REVIEW",
    "refined_baseline_model_comparison_review": "INSUFFICIENT_OR_MIXED",
    "refined_calibration_stability_review": (
        "NOT_ACCEPTANCE_EVIDENCE_UNTIL_READINESS_REVIEW"
    ),
    "refined_leakage_quality_review": "PASS",
    "data_quality_review": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
    "meta_reduced_record_count_review": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
    "operator_acceptance_boundary_review": "ACCEPTANCE_NOT_GRANTED",
}

FUTURE_CHAIN = [
    "Predictive Usefulness Acceptance Readiness Review Rerun Using Refined Evidence.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Predictive Usefulness Acceptance Ceremony, only if separately approved.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_predictive_usefulness_acceptance_from_reassessment_rerun",
    "no_predictive_usefulness_acceptance_without_readiness_review",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_refined_evidence_without_new_approval",
    "preserve_meta_reduced_record_count",
    "all_outputs_labeled_research_only",
    "low_or_mixed_oos_accuracy_not_acceptance_evidence",
    "model_comparison_not_acceptance_evidence_by_itself",
    "calibration_stability_not_acceptance_evidence_by_itself",
]

PLANNED_OUTPUT_NAMES = [
    "predictive_usefulness_acceptance_readiness_review_rerun_plan",
    "predictive_usefulness_acceptance_candidate_template_if_ready",
    "profitability_review_chain_template_if_required",
    "runtime_migration_chain_template_if_ever_authorized",
    "operator_review_summary_template",
]

REGISTRY_APPROVED_DATASET_METADATA = deepcopy(source_review.EXPECTED_REGISTRY_METADATA)


class PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(ValueError):
    """Raised when the reassessment rerun violates its review-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
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
        "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest",
        None,
    )
    return payload


def per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for one ticker reassessment rerun."""
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
            "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_status": (
                "REASSESSMENT_RERUN_COMPLETED_RESEARCH_ONLY"
            ),
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_refined_evidence_results_review_digest": (
                EXPECTED_REFINED_RESULTS_REVIEW_DIGEST
            ),
        }
        if is_meta:
            entry["refinement_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_REASSESSMENT_RERUN"
            )
        entry[
            "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest"
        ] = per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _review_domains() -> list[dict[str, str]]:
    return [
        {
            "domain_id": domain_id,
            "review_result": result,
            "label": RESEARCH_ONLY_NON_ACTIONABLE,
            "authority": NOT_ACCEPTANCE,
        }
        for domain_id, result in REVIEW_DOMAIN_RESULTS.items()
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
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_V1,
        "review_status": PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE_READY,
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
        "additional_predictive_evidence_execution_for_refined_evidence_executed": True,
        "additional_predictive_evidence_results_for_refined_evidence_created": True,
        "additional_predictive_evidence_results_review_for_refined_evidence_created": True,
        "additional_predictive_evidence_results_review_for_refined_evidence_ready": True,
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created": True,
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_ready": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence": True,
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
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
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest": EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_for_refined_evidence_digest": EXPECTED_REFINED_EXECUTION_DIGEST,
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest": EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST,
        "feature_label_refinement_results_review_package_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
        "feature_label_refinement_execution_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": EXPECTED_ORIGINAL_EXECUTION_DIGEST,
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
        "generated_output_count": 10,
        "failure_count": 0,
        "warning_count": 1,
        "warnings": ["META_PRESERVED_REDUCED_RECORD_COUNT_913"],
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
        "reassessment_review_status": "COMPLETED_RESEARCH_ONLY",
        "refined_evidence_predictive_signal_consistency": "WEAK_OR_MIXED",
        "refined_baseline_outperformance_consistency": "INSUFFICIENT_OR_MIXED",
        "refined_oos_performance_assessment": (
            "LOW_TO_MIXED_NOT_ACCEPTANCE_EVIDENCE"
        ),
        "model_comparison_assessment": "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE",
        "calibration_stability_assessment": (
            "NOT_ACCEPTANCE_EVIDENCE_UNTIL_READINESS_REVIEW"
        ),
        "leakage_control_assessment": "PASS",
        "data_quality_assessment": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "meta_limitation_assessment": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "reassessment_supports_future_acceptance_readiness_review_rerun_using_refined_evidence": True,
        "reassessment_supports_direct_predictive_usefulness_acceptance": False,
        "reassessment_recommends_predictive_usefulness_acceptance": False,
        "acceptance_decision_required_later": True,
        "review_domains": _review_domains(),
        "per_ticker_reassessment_rerun_entries": _per_ticker_entries(),
        "future_chain": list(FUTURE_CHAIN),
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
    ("refined_results_review_digest_bound", EXPECTED_REFINED_RESULTS_REVIEW_DIGEST, "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"),
    ("refined_execution_digest_bound", EXPECTED_REFINED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_for_refined_evidence_digest"),
    ("refined_execution_approval_digest_bound", EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_for_refined_evidence_digest"),
    ("feature_label_refinement_results_review_digest_bound", EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST, "feature_label_refinement_results_review_package_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_refined_results_review_universe", TARGET_UNIVERSE, "target_universe"),
    ("total_canonical_record_count_11946", 11946, "total_canonical_record_count"),
    ("meta_record_count_913_preserved", 913, "meta_record_count"),
    ("non_meta_record_counts_1003_preserved", True, "check_non_meta_record_counts"),
    ("additional_predictive_evidence_results_review_for_refined_evidence_ready_true", True, "additional_predictive_evidence_results_review_for_refined_evidence_ready"),
    ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created_true", True, "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created"),
    ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_ready_true", True, "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_ready"),
    ("refined_label_family_count_7", 7, "refined_label_family_count"),
    ("refined_label_available_values_82698", 82698, "refined_label_available_values"),
    ("refined_label_unavailable_values_924", 924, "refined_label_unavailable_values"),
    ("refined_feature_group_count_9", 9, "refined_feature_group_count"),
    ("refined_feature_fields_19", 19, "refined_feature_field_count"),
    ("refined_protocol_group_count_6", 6, "refined_protocol_group_count"),
    ("model_comparison_group_count_5", 5, "model_comparison_group_count"),
    ("refined_walk_forward_fold_count_4", 4, "refined_walk_forward_fold_count"),
    ("refined_oos_rows_2988", 2988, "refined_oos_evaluation_rows"),
    ("refined_oos_accuracy_range_bound", "0.119813 to 0.480924", "refined_oos_accuracy_range"),
    ("refined_leakage_status_pass", "PASS", "refined_leakage_status"),
    ("failed_leakage_controls_zero", 0, "failed_leakage_controls"),
    ("data_quality_pass_with_preserved_limitation", "PASS_WITH_PRESERVED_SOURCE_LIMITATION", "data_quality_status"),
    ("reassessment_review_completed_research_only", "COMPLETED_RESEARCH_ONLY", "reassessment_review_status"),
    ("refined_evidence_predictive_signal_weak_or_mixed", "WEAK_OR_MIXED", "refined_evidence_predictive_signal_consistency"),
    ("refined_baseline_outperformance_insufficient_or_mixed", "INSUFFICIENT_OR_MIXED", "refined_baseline_outperformance_consistency"),
    ("refined_oos_performance_low_to_mixed_not_acceptance_evidence", "LOW_TO_MIXED_NOT_ACCEPTANCE_EVIDENCE", "refined_oos_performance_assessment"),
    ("reassessment_supports_future_readiness_review_rerun_true", True, "reassessment_supports_future_acceptance_readiness_review_rerun_using_refined_evidence"),
    ("reassessment_supports_direct_acceptance_false", False, "reassessment_supports_direct_predictive_usefulness_acceptance"),
    ("reassessment_recommends_acceptance_false", False, "reassessment_recommends_predictive_usefulness_acceptance"),
    ("review_domains_defined", REVIEW_DOMAIN_RESULTS, "check_review_domain_results"),
    ("per_ticker_reassessment_entries_12", 12, "check_per_ticker_entry_count"),
    ("per_ticker_reassessment_digests_present", True, "check_per_ticker_digests"),
    ("future_chain_defined", FUTURE_CHAIN, "future_chain"),
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
    ("predictive_usefulness_acceptance_readiness_review_rerun_created_false", False, "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created"),
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


def _derived_check_fields(review_package: dict[str, Any]) -> dict[str, Any]:
    entries = review_package.get("per_ticker_reassessment_rerun_entries", [])
    domains = review_package.get("review_domains", [])
    planned = review_package.get("planned_outputs", [])
    counts = review_package.get("per_ticker_record_counts", {})
    return {
        "check_non_meta_record_counts": isinstance(counts, dict)
        and all(counts.get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META"),
        "check_review_domain_results": {
            item.get("domain_id"): item.get("review_result")
            for item in domains
            if isinstance(item, dict)
        },
        "check_per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "check_per_ticker_digests": isinstance(entries, list)
        and all(
            isinstance(item, dict)
            and isinstance(
                item.get(
                    "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest"
                ),
                str,
            )
            and item[
                "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest"
            ]
            == per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest_v1(
                item
            )
            for item in entries
        ),
        "check_planned_outputs_not_generated": isinstance(planned, list)
        and len(planned) == len(PLANNED_OUTPUT_NAMES)
        and all(item.get("status") == PLANNED_NOT_GENERATED for item in planned),
        "check_planned_outputs_research_only": isinstance(planned, list)
        and len(planned) == len(PLANNED_OUTPUT_NAMES)
        and all(item.get("label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(review_package)
    values.update(_derived_check_fields(review_package))
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
        "ready_for_operator_review": blockers == 0,
        "ready_for_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence": blockers
        == 0,
        "predictive_usefulness_acceptance_readiness_review_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop(
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest",
        None,
    )
    return payload


def predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic digest for the reassessment rerun package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1() -> dict:
    """Build the exact offline reassessment rerun without granting acceptance."""
    review_package = _base_review()
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package[
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest"
    ] = predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest_v1(
        review_package
    )
    validate_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE",
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
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created",
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
        "reassessment_supports_direct_predictive_usefulness_acceptance",
        "reassessment_recommends_predictive_usefulness_acceptance",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
    review_package: dict,
) -> dict:
    """Fail closed unless the package exactly matches the offline review contract."""
    if not isinstance(review_package, dict):
        raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
            "reassessment rerun package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    expected_base = _base_review()
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
            "review_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    failed = [row for row in expected_checklist if row.get("status") != PASS]
    if failed:
        raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
            "reassessment rerun package digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest_v1(
            review_package
        ),
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest": digest,
        "source_refined_evidence_results_review_digest": review_package[
            "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"
        ],
        "per_ticker_reassessment_entry_count": len(
            review_package["per_ticker_reassessment_rerun_entries"]
        ),
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_markdown_v1(
    review_package: dict,
) -> str:
    """Render the sanitized operator-facing reassessment rerun summary."""
    validation = validate_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
        review_package
    )
    registry = review_package["registry_approved_dataset_metadata"]
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Predictive Usefulness Reassessment Review Rerun Using Refined Evidence",
        "",
        "## Title",
        "- Predictive Usefulness Reassessment Review Rerun Using Refined Evidence v1.",
        "",
        "## Predictive Usefulness Reassessment Review Rerun Using Refined Evidence",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`",
        f"- Review digest: `{validation['predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest']}`",
        "",
        "## Source Refined-Evidence Results Review",
        f"- Results-review digest: `{review_package['additional_predictive_evidence_results_review_for_refined_evidence_package_digest']}`",
        f"- Execution/approval digests: `{review_package['additional_predictive_evidence_execution_for_refined_evidence_digest']}` / `{review_package['additional_predictive_evidence_execution_approval_for_refined_evidence_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/scope: `{registry['dataset_name']}` / `{registry['dataset_scope']}`",
        f"- Records/digest: `{registry['total_canonical_record_count']}` / `{registry['records_digest']}`",
        "",
        "## Target Universe",
        f"- `{', '.join(review_package['target_universe'])}`",
        "",
        "## Refined Evidence Facts",
        f"- Labels available/unavailable: `{review_package['refined_label_available_values']}` / `{review_package['refined_label_unavailable_values']}`",
        f"- Features groups/fields/rows: `{review_package['refined_feature_group_count']}` / `{review_package['refined_feature_field_count']}` / `{review_package['refined_feature_rows']}`",
        f"- Walk-forward folds/OOS rows/range: `{review_package['refined_walk_forward_fold_count']}` / `{review_package['refined_oos_evaluation_rows']}` / `{review_package['refined_oos_accuracy_range']}`",
        "",
        "## Reassessment Classification",
        f"- Status/signal/baseline: `{review_package['reassessment_review_status']}` / `{review_package['refined_evidence_predictive_signal_consistency']}` / `{review_package['refined_baseline_outperformance_consistency']}`",
        f"- OOS assessment: `{review_package['refined_oos_performance_assessment']}`",
        "",
        "## Review Domains",
    ]
    lines.extend(
        f"- `{row['domain_id']}`: `{row['review_result']}`"
        for row in review_package["review_domains"]
    )
    lines.extend(
        [
            "",
            "## Per-Ticker Reassessment Entries",
            f"- Entry count: `{len(review_package['per_ticker_reassessment_rerun_entries'])}`; META preserves 913 records and all others preserve 1003.",
            "",
            "## Future Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(review_package["future_chain"], start=1)
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness: `{review_package['predictive_usefulness']}`; acceptance-readiness rerun is future work.",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{review_package['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{review_package['runtime_use']}` / `{review_package['strategy_use']}` / `{review_package['paper_trading']}` / `{review_package['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- Built offline from the exact refined-results review contract; no provider request, acquisition, regeneration, evidence rerun, recomputation, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- Planned outputs remain not generated and research-only; this package opens only the later acceptance-readiness review-rerun gate.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write one canonical JSON package without overwriting an existing file."""
    review_package = (
        build_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1()
    )
    validation = validate_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or (
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
            "reassessment rerun filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError(
            "reassessment rerun output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
