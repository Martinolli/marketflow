"""Offline, non-authorizing predictive-usefulness reassessment review package."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    predictive_usefulness_reassessment_candidate_operator_review_service as candidate_review_service,
)


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_V1 = (
    "predictive_usefulness_reassessment_review_v1"
)
PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE_READY"
)

EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "469b87cb9c526d7a57e6e397fdfec86b436c6a428f0faeb65406477f24d0a7f4"
)
EXPECTED_CANDIDATE_DIGEST = candidate_review_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST = (
    candidate_review_service.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_EXECUTION_DIGEST = candidate_review_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_EXECUTION_APPROVAL_DIGEST = (
    candidate_review_service.EXPECTED_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    candidate_review_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    candidate_review_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = candidate_review_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(candidate_review_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_review_service.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = candidate_review_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_review_service.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_review_service.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = candidate_review_service.PLANNED_NOT_GENERATED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEW_DOMAIN_RESULTS = {
    "label_coverage_review": "PASS_WITH_EXPECTED_UNAVAILABLE_FUTURE_LABELS",
    "feature_coverage_review": "PASS_WITH_EXPECTED_ROLLING_NULLS",
    "walk_forward_stability_review": "MIXED_REQUIRES_READINESS_REVIEW",
    "out_of_sample_performance_review": "MIXED_REQUIRES_READINESS_REVIEW",
    "baseline_comparison_review": "MIXED_OR_INSUFFICIENT_FOR_ACCEPTANCE",
    "calibration_review": "REVIEWED_REQUIRES_READINESS_INTERPRETATION",
    "stability_analysis_review": "MIXED_REQUIRES_READINESS_REVIEW",
    "false_positive_false_negative_review": (
        "REVIEWED_REQUIRES_READINESS_INTERPRETATION"
    ),
    "leakage_control_review": "PASS",
    "data_quality_review": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
    "meta_reduced_record_count_review": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
    "operator_acceptance_boundary_review": "ACCEPTANCE_NOT_GRANTED",
}

FUTURE_ACCEPTANCE_CHAIN = [
    "Predictive usefulness acceptance readiness review.",
    "Predictive usefulness acceptance candidate, only if readiness review supports it.",
    "Predictive usefulness acceptance ceremony, only if operator explicitly approves.",
    "Profitability review chain, if separately required.",
    "Runtime migration candidate, only if usefulness/profitability gates are separately satisfied.",
    "Runtime migration review and approval, if ever separately authorized.",
]

FUTURE_GATES = [
    "predictive_usefulness_acceptance_readiness_review",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_predictive_usefulness_acceptance_from_reassessment_review",
    "no_predictive_usefulness_acceptance_without_readiness_review",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_predictive_evidence",
    "majority_accuracy_not_acceptance_evidence_by_itself",
    "buy_hold_reference_not_trade_recommendation",
    "mixed_signal_requires_operator_readiness_review",
    "all_outputs_labeled_research_only",
]

PLANNED_OUTPUT_NAMES = [
    "predictive_usefulness_acceptance_readiness_review_plan",
    "predictive_usefulness_acceptance_candidate_template",
    "acceptance_decision_matrix_template",
    "profitability_review_chain_template",
    "runtime_migration_chain_template",
    "operator_review_summary_template",
]


class PredictiveUsefulnessReassessmentReviewError(ValueError):
    """Raised when a reassessment review violates its review-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessReassessmentReviewError(f"{field} mismatch")


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


def _source_candidate_review(candidate_review_package: dict | None) -> dict[str, Any]:
    source = (
        candidate_review_service.build_predictive_usefulness_reassessment_candidate_review_package_v1()
        if candidate_review_package is None
        else deepcopy(candidate_review_package)
    )
    candidate_review_service.validate_predictive_usefulness_reassessment_candidate_review_package_v1(
        source
    )
    _expect(
        source.get(
            "predictive_usefulness_reassessment_candidate_review_package_digest"
        ),
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source candidate review package digest",
    )
    return source


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_predictive_usefulness_reassessment_review_digest", None)
    return payload


def per_ticker_predictive_usefulness_reassessment_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker reassessment review."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_reassessment_candidate_review_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "predictive_evidence_results_status": "REVIEWED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_candidate_status": (
                "READY_FOR_OPERATOR_REVIEW"
            ),
            "predictive_usefulness_reassessment_review_status": (
                "REASSESSMENT_REVIEW_COMPLETED_RESEARCH_ONLY"
            ),
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_predictive_usefulness_reassessment_candidate_review_digest": (
                source[
                    "predictive_usefulness_reassessment_candidate_review_package_digest"
                ]
            ),
            "source_predictive_usefulness_reassessment_candidate_digest": source[
                "predictive_usefulness_reassessment_candidate_digest"
            ],
        }
        entry["per_ticker_predictive_usefulness_reassessment_review_digest"] = (
            per_ticker_predictive_usefulness_reassessment_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _review_domains() -> list[dict[str, str]]:
    return [
        {
            "domain_id": domain_id,
            "review_result": result,
            "label": RESEARCH_ONLY_NON_ACTIONABLE,
            "authority": "NOT_ACCEPTANCE",
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


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_V1,
        "review_status": PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "predictive_execution_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_matrix_rerun_performed": False,
        "walk_forward_validation_rerun_performed": False,
        "out_of_sample_evaluation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "additional_predictive_evidence_results_review_created": True,
        "additional_predictive_evidence_results_review_ready": True,
        "predictive_usefulness_reassessment_candidate_created": True,
        "predictive_usefulness_reassessment_candidate_review_created": True,
        "predictive_usefulness_reassessment_review_created": True,
        "predictive_usefulness_reassessment_review_ready": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review": True,
        "ready_for_predictive_usefulness_acceptance": False,
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
        "predictive_usefulness_reassessment_candidate_review_package_digest": source[
            "predictive_usefulness_reassessment_candidate_review_package_digest"
        ],
        "predictive_usefulness_reassessment_candidate_digest": source[
            "predictive_usefulness_reassessment_candidate_digest"
        ],
        "additional_predictive_evidence_results_review_package_digest": source[
            "additional_predictive_evidence_results_review_package_digest"
        ],
        "additional_predictive_evidence_execution_digest": source[
            "additional_predictive_evidence_execution_digest"
        ],
        "additional_predictive_evidence_execution_approval_digest": source[
            "additional_predictive_evidence_execution_approval_digest"
        ],
        "research_registry_approval_digest": source[
            "research_registry_approval_digest"
        ],
        "canonical_dataset_freeze_digest": source["canonical_dataset_freeze_digest"],
        "records_digest": source["records_digest"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "registry_approved_dataset_metadata": deepcopy(
            source["reviewed_registry_approved_dataset_metadata"]
        ),
        "evidence_summary": deepcopy(source["reviewed_evidence_summary"]),
        "performance_interpretation": deepcopy(
            source["reviewed_performance_interpretation"]
        ),
        "reassessment_review_status": "COMPLETED_RESEARCH_ONLY",
        "evidence_quality_for_acceptance_readiness": (
            "MIXED_REQUIRES_READINESS_REVIEW"
        ),
        "predictive_signal_consistency": "MIXED",
        "baseline_outperformance_consistency": "INSUFFICIENT_OR_MIXED",
        "leakage_control_assessment": "PASS",
        "data_quality_assessment": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "meta_limitation_assessment": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "reassessment_supports_future_acceptance_readiness_review": True,
        "reassessment_supports_direct_predictive_usefulness_acceptance": False,
        "reassessment_recommends_predictive_usefulness_acceptance": False,
        "acceptance_decision_required_later": True,
        "per_ticker_reassessment_review_entries": _per_ticker_entries(source),
        "review_domains": _review_domains(),
        "future_acceptance_chain": deepcopy(FUTURE_ACCEPTANCE_CHAIN),
        "future_gates": deepcopy(FUTURE_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST, "predictive_usefulness_reassessment_candidate_review_package_digest"),
    ("candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "predictive_usefulness_reassessment_candidate_digest"),
    ("results_review_digest_bound", EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST, "additional_predictive_evidence_results_review_package_digest"),
    ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_digest"),
    ("execution_approval_digest_bound", EXPECTED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_candidate_review_universe", TARGET_UNIVERSE, "target_universe"),
    ("additional_predictive_evidence_executed_true", True, "additional_predictive_evidence_executed"),
    ("additional_predictive_evidence_results_review_ready_true", True, "additional_predictive_evidence_results_review_ready"),
    ("predictive_usefulness_reassessment_candidate_created_true", True, "predictive_usefulness_reassessment_candidate_created"),
    ("predictive_usefulness_reassessment_candidate_review_created_true", True, "predictive_usefulness_reassessment_candidate_review_created"),
    ("predictive_usefulness_reassessment_review_created_true", True, "predictive_usefulness_reassessment_review_created"),
    ("predictive_usefulness_reassessment_review_ready_true", True, "predictive_usefulness_reassessment_review_ready"),
    ("label_coverage_entries_84", 84, "check_label_coverage_entries"),
    ("label_available_values_82854", 82854, "check_label_available_values"),
    ("label_unavailable_values_768", 768, "check_label_unavailable_values"),
    ("feature_rows_11946", 11946, "check_feature_rows"),
    ("feature_fields_22", 22, "check_feature_fields"),
    ("walk_forward_fold_count_4", 4, "check_walk_forward_fold_count"),
    ("oos_evaluation_rows_2988", 2988, "check_oos_evaluation_rows"),
    ("leakage_status_pass", "PASS", "check_leakage_status"),
    ("failed_leakage_controls_zero", 0, "check_failed_leakage_controls"),
    ("walk_forward_accuracy_range_bound", "0.498698 to 0.562842", "check_walk_forward_accuracy_range"),
    ("oos_performance_summary_bound", True, "oos_performance_summary_bound"),
    ("reassessment_review_completed_research_only", "COMPLETED_RESEARCH_ONLY", "reassessment_review_status"),
    ("evidence_quality_mixed_requires_readiness_review", "MIXED_REQUIRES_READINESS_REVIEW", "evidence_quality_for_acceptance_readiness"),
    ("predictive_signal_consistency_mixed", "MIXED", "predictive_signal_consistency"),
    ("baseline_outperformance_insufficient_or_mixed", "INSUFFICIENT_OR_MIXED", "baseline_outperformance_consistency"),
    ("reassessment_supports_future_acceptance_readiness_review_true", True, "reassessment_supports_future_acceptance_readiness_review"),
    ("reassessment_supports_direct_acceptance_false", False, "reassessment_supports_direct_predictive_usefulness_acceptance"),
    ("reassessment_recommends_acceptance_false", False, "reassessment_recommends_predictive_usefulness_acceptance"),
    ("per_ticker_reassessment_review_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_reassessment_review_digests_present", True, "per_ticker_digests_valid"),
    ("review_domains_defined", REVIEW_DOMAIN_RESULTS, "review_domain_results"),
    ("future_acceptance_chain_defined", FUTURE_ACCEPTANCE_CHAIN, "future_acceptance_chain"),
    ("future_gates_defined", FUTURE_GATES, "future_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("planned_outputs_not_generated", PLANNED_NOT_GENERATED, "planned_outputs_status"),
    ("planned_outputs_research_only", RESEARCH_ONLY_NON_ACTIONABLE, "planned_outputs_label"),
    ("provider_requests_made_in_review_false", False, "provider_requests_made_in_review"),
    ("live_provider_transport_enabled_in_review_false", False, "live_provider_transport_enabled_in_review"),
    ("market_data_acquisition_performed_in_review_false", False, "market_data_acquisition_performed_in_review"),
    ("dataset_generation_performed_in_review_false", False, "dataset_generation_performed_in_review"),
    ("canonical_dataset_regenerated_in_review_false", False, "canonical_dataset_regenerated_in_review"),
    ("predictive_execution_rerun_performed_false", False, "predictive_execution_rerun_performed"),
    ("label_generation_rerun_performed_false", False, "label_generation_rerun_performed"),
    ("feature_matrix_rerun_performed_false", False, "feature_matrix_rerun_performed"),
    ("walk_forward_validation_rerun_performed_false", False, "walk_forward_validation_rerun_performed"),
    ("out_of_sample_evaluation_rerun_performed_false", False, "out_of_sample_evaluation_rerun_performed"),
    ("metrics_recomputation_performed_false", False, "metrics_recomputation_performed"),
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
    evidence = review_package.get("evidence_summary", {})
    performance = review_package.get("performance_interpretation", {})
    entries = review_package.get("per_ticker_reassessment_review_entries", [])
    domains = review_package.get("review_domains", [])
    return {
        "check_label_coverage_entries": evidence.get("label_coverage_entries"),
        "check_label_available_values": evidence.get("label_available_values"),
        "check_label_unavailable_values": evidence.get("label_unavailable_values"),
        "check_feature_rows": evidence.get("feature_rows"),
        "check_feature_fields": evidence.get("feature_fields"),
        "check_walk_forward_fold_count": evidence.get("walk_forward_fold_count"),
        "check_oos_evaluation_rows": evidence.get("oos_evaluation_rows"),
        "check_leakage_status": evidence.get("leakage_status"),
        "check_failed_leakage_controls": evidence.get("failed_leakage_controls"),
        "check_walk_forward_accuracy_range": performance.get(
            "walk_forward_accuracy_range"
        ),
        "oos_performance_summary_bound": {
            key: performance.get(key)
            for key in (
                "oos_majority_accuracy",
                "oos_previous_direction_accuracy",
                "oos_ticker_cross_sectional_accuracy",
                "oos_brier_score",
            )
        }
        == {
            "oos_majority_accuracy": "0.539491",
            "oos_previous_direction_accuracy": "0.495984",
            "oos_ticker_cross_sectional_accuracy": "0.502677",
            "oos_brier_score": "0.24875351",
        },
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_digests_valid": isinstance(entries, list)
        and all(
            isinstance(item, dict)
            and isinstance(
                item.get("per_ticker_predictive_usefulness_reassessment_review_digest"),
                str,
            )
            and item["per_ticker_predictive_usefulness_reassessment_review_digest"]
            == per_ticker_predictive_usefulness_reassessment_review_digest_v1(item)
            for item in entries
        ),
        "review_domain_results": {
            item.get("domain_id"): item.get("review_result")
            for item in domains
            if isinstance(item, dict)
        },
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(review_package)
    values.update(_derived_check_fields(review_package))
    return [_check(check_id, expected, values.get(field)) for check_id, expected, field in CHECK_FIELD_SPECS]


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
        "ready_for_predictive_usefulness_acceptance_readiness_review": blockers == 0,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_usefulness_reassessment_review_package_digest", None)
    return payload


def predictive_usefulness_reassessment_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for a reassessment review."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_usefulness_reassessment_review_package_v1(
    *, candidate_review_package: dict | None = None
) -> dict:
    """Build the exact offline reassessment review without granting acceptance."""
    source = _source_candidate_review(candidate_review_package)
    review_package = _base_review(source)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["predictive_usefulness_reassessment_review_package_digest"] = (
        predictive_usefulness_reassessment_review_package_digest_v1(review_package)
    )
    validate_predictive_usefulness_reassessment_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
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
        "predictive_execution_rerun_performed",
        "label_generation_rerun_performed",
        "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed",
        "metrics_recomputation_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "ready_for_predictive_usefulness_acceptance",
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
                raise PredictiveUsefulnessReassessmentReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveUsefulnessReassessmentReviewError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveUsefulnessReassessmentReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveUsefulnessReassessmentReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_usefulness_reassessment_review_package_v1(
    review_package: dict,
) -> dict:
    """Fail closed unless the review exactly matches the approved offline contract."""
    if not isinstance(review_package, dict):
        raise PredictiveUsefulnessReassessmentReviewError(
            "reassessment review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    expected_source = (
        candidate_review_service.build_predictive_usefulness_reassessment_candidate_review_package_v1()
    )
    expected_base = _base_review(expected_source)
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessReassessmentReviewError("review_checklist missing")
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    failed = [row for row in expected_checklist if row.get("status") != PASS]
    if failed:
        raise PredictiveUsefulnessReassessmentReviewError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "predictive_usefulness_reassessment_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReassessmentReviewError(
            "predictive usefulness reassessment review package digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_reassessment_review_package_digest_v1(review_package),
        "predictive_usefulness_reassessment_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_usefulness_reassessment_review_package_digest": digest,
        "source_candidate_review_package_digest": review_package[
            "predictive_usefulness_reassessment_candidate_review_package_digest"
        ],
        "per_ticker_review_entry_count": len(
            review_package["per_ticker_reassessment_review_entries"]
        ),
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_predictive_usefulness_acceptance_readiness_review": True,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_usefulness_reassessment_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render the sanitized operator-facing reassessment review summary."""
    validation = validate_predictive_usefulness_reassessment_review_package_v1(
        review_package
    )
    evidence = review_package["evidence_summary"]
    performance = review_package["performance_interpretation"]
    registry = review_package["registry_approved_dataset_metadata"]
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Predictive Usefulness Reassessment Review Status",
        "",
        "## Title",
        "- Predictive Usefulness Reassessment Review Package v1.",
        "",
        "## Predictive Usefulness Reassessment Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`",
        f"- Review digest: `{validation['predictive_usefulness_reassessment_review_package_digest']}`",
        "",
        "## Source Candidate Review",
        f"- Candidate-review digest: `{review_package['predictive_usefulness_reassessment_candidate_review_package_digest']}`",
        f"- Candidate digest: `{review_package['predictive_usefulness_reassessment_candidate_digest']}`",
        "",
        "## Source Additional Predictive Evidence Results Review",
        f"- Results-review digest: `{review_package['additional_predictive_evidence_results_review_package_digest']}`",
        f"- Execution digest: `{review_package['additional_predictive_evidence_execution_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/scope: `{registry['dataset_name']}` / `{registry['dataset_scope']}`",
        f"- Records/digest: `{registry['total_canonical_record_count']}` / `{registry['records_digest']}`",
        "",
        "## Target Universe",
        f"- `{', '.join(review_package['target_universe'])}`",
        "",
        "## Evidence Summary",
        f"- Labels available/unavailable: `{evidence['label_available_values']}` / `{evidence['label_unavailable_values']}`",
        f"- Features rows/fields: `{evidence['feature_rows']}` / `{evidence['feature_fields']}`",
        f"- Walk-forward folds/OOS rows: `{evidence['walk_forward_fold_count']}` / `{evidence['oos_evaluation_rows']}`",
        f"- Leakage/failed controls: `{evidence['leakage_status']}` / `{evidence['failed_leakage_controls']}`",
        "",
        "## Performance Interpretation",
        f"- Walk-forward range/stability: `{performance['walk_forward_accuracy_range']}` / `{performance['walk_forward_accuracy_stability_status']}`",
        f"- Signal/baseline: `{performance['performance_signal_status']}` / `{performance['baseline_outperformance_status']}`",
        f"- Review classification: `{review_package['evidence_quality_for_acceptance_readiness']}`; direct acceptance supported: `{review_package['reassessment_supports_direct_predictive_usefulness_acceptance']}`.",
        "",
        "## Per-Ticker Reassessment Review Entries",
        f"- Entry count: `{len(review_package['per_ticker_reassessment_review_entries'])}`; META preserves 913 records and all other tickers preserve 1003.",
        "",
        "## Review Domains",
    ]
    lines.extend(
        f"- `{row['domain_id']}`: `{row['review_result']}`"
        for row in review_package["review_domains"]
    )
    lines.extend(["", "## Future Acceptance Chain"])
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(review_package["future_acceptance_chain"], start=1)
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness: `{review_package['predictive_usefulness']}`; acceptance readiness review is future work.",
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
            "- Built offline from exact reviewed evidence; no provider request, acquisition, regeneration, predictive rerun, recomputation, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- Planned outputs remain not generated and research-only; this review only opens the later acceptance-readiness review gate.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_reassessment_review_package_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write canonical review JSON once without overwriting an existing file."""
    review_package = build_predictive_usefulness_reassessment_review_package_v1(
        candidate_review_package=candidate_review_package
    )
    validation = validate_predictive_usefulness_reassessment_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_usefulness_reassessment_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessReassessmentReviewError(
            "predictive usefulness reassessment review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessReassessmentReviewError(
            "predictive usefulness reassessment review output already exists"
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
