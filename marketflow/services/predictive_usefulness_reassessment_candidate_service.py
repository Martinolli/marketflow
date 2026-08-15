"""Offline predictive-usefulness reassessment candidate from reviewed evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_results_review_service as results_review


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_V1 = (
    "predictive_usefulness_reassessment_candidate_v1"
)
PREDICTIVE_USEFULNESS_REASSESSMENT_READY_FOR_OPERATOR_REVIEW = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8"
)
EXPECTED_EXECUTION_DIGEST = results_review.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_EXECUTION_APPROVAL_DIGEST = results_review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    results_review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    results_review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    results_review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    results_review.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
)
EXPECTED_RECORDS_DIGEST = results_review.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(results_review.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(results_review.EXPECTED_RECORD_COUNTS)
REGISTRY_APPROVED_DATASET_METADATA = deepcopy(
    results_review.execution.APPROVED_REGISTRY_METADATA
)
NOT_ACCEPTED = results_review.NOT_ACCEPTED
NOT_AUTHORIZED = results_review.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = results_review.RESEARCH_ONLY_NON_ACTIONABLE

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
CANDIDATE_READY_FOR_OPERATOR_REVIEW = "CANDIDATE_READY_FOR_OPERATOR_REVIEW"
NOT_ACCEPTANCE = "NOT_ACCEPTANCE"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"

REASSESSMENT_DOMAIN_IDS = [
    "label_coverage_review",
    "feature_coverage_review",
    "walk_forward_stability_review",
    "out_of_sample_performance_review",
    "baseline_comparison_review",
    "calibration_review",
    "stability_analysis_review",
    "false_positive_false_negative_review",
    "leakage_control_review",
    "data_quality_review",
    "meta_reduced_record_count_review",
    "operator_acceptance_boundary_review",
]

FUTURE_REASSESSMENT_CHAIN = [
    "Predictive usefulness reassessment candidate operator review package.",
    "Predictive usefulness reassessment review package.",
    "Predictive usefulness acceptance readiness review.",
    "Predictive usefulness acceptance ceremony, only if evidence is sufficient.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "predictive_usefulness_reassessment_candidate_operator_review",
    "predictive_usefulness_reassessment_review",
    "predictive_usefulness_acceptance_readiness_review",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_predictive_usefulness_acceptance_from_candidate",
    "no_predictive_usefulness_acceptance_without_readiness_review",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_predictive_evidence",
    "all_outputs_labeled_research_only",
]

PLANNED_OUTPUT_IDS = [
    "predictive_usefulness_reassessment_candidate_manifest",
    "evidence_interpretation_matrix",
    "per_ticker_reassessment_candidate_summary",
    "baseline_comparison_interpretation_template",
    "walk_forward_stability_interpretation_template",
    "oos_performance_interpretation_template",
    "operator_review_summary_template",
]


class PredictiveUsefulnessReassessmentCandidateError(ValueError):
    """Raised when a reassessment candidate violates its candidate-only boundary."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessReassessmentCandidateError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessReassessmentCandidateError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessReassessmentCandidateError(f"{field} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_predictive_usefulness_reassessment_candidate_digest", None)
    return payload


def per_ticker_predictive_usefulness_reassessment_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one ticker's reassessment candidate entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "predictive_evidence_results_status": "REVIEWED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_candidate_status": (
                CANDIDATE_READY_FOR_OPERATOR_REVIEW
            ),
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_predictive_usefulness_reassessment_candidate_digest"] = (
            per_ticker_predictive_usefulness_reassessment_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _reassessment_domains() -> list[dict[str, str]]:
    return [
        {
            "domain_id": domain_id,
            "candidate_status": CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "acceptance_status": NOT_ACCEPTANCE,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for domain_id in REASSESSMENT_DOMAIN_IDS
    ]


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_V1,
        "candidate_status": PREDICTIVE_USEFULNESS_REASSESSMENT_READY_FOR_OPERATOR_REVIEW,
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
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "additional_predictive_evidence_results_review_created": True,
        "additional_predictive_evidence_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_candidate": True,
        "predictive_usefulness_reassessment_candidate_created": True,
        "predictive_usefulness_reassessment_ready_for_operator_review": True,
        "predictive_usefulness_reassessment_review_created": False,
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
        "additional_predictive_evidence_results_review_package_digest": (
            EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "additional_predictive_evidence_execution_approval_digest": (
            EXPECTED_EXECUTION_APPROVAL_DIGEST
        ),
        "additional_predictive_evidence_execution_candidate_review_package_digest": (
            EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "registry_approved_dataset_metadata": deepcopy(REGISTRY_APPROVED_DATASET_METADATA),
        "evidence_summary_status": "READY_FOR_OPERATOR_REVIEW",
        "evidence_supports_future_reassessment_review": True,
        "evidence_supports_direct_acceptance": False,
        "operator_review_required_before_acceptance": True,
        "acceptance_recommendation": "NOT_RECOMMENDED_AT_CANDIDATE_STAGE",
        "reviewed_evidence_summary": {
            "label_coverage_entries": 84,
            "label_available_values": 82854,
            "label_unavailable_values": 768,
            "feature_rows": 11946,
            "feature_fields": 22,
            "walk_forward_fold_count": 4,
            "oos_evaluation_rows": 2988,
            "leakage_status": "PASS",
            "failed_leakage_controls": 0,
        },
        "performance_interpretation": {
            "walk_forward_accuracy_range": "0.498698 to 0.562842",
            "walk_forward_accuracy_min": "0.498698",
            "walk_forward_accuracy_max": "0.562842",
            "walk_forward_accuracy_stability_status": "MIXED_REQUIRES_OPERATOR_REVIEW",
            "oos_majority_accuracy": "0.539491",
            "oos_previous_direction_accuracy": "0.495984",
            "oos_ticker_cross_sectional_accuracy": "0.502677",
            "oos_brier_score": "0.24875351",
            "performance_signal_status": "REVIEW_REQUIRED_NOT_ACCEPTANCE_EVIDENCE",
            "baseline_outperformance_status": "MIXED_OR_INSUFFICIENT_FOR_ACCEPTANCE",
        },
        "per_ticker_reassessment_candidate_entries": _per_ticker_entries(),
        "reassessment_domains": _reassessment_domains(),
        "future_reassessment_chain": list(FUTURE_REASSESSMENT_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("results_review_digest_bound", EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST, "additional_predictive_evidence_results_review_package_digest"),
    ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_digest"),
    ("execution_approval_digest_bound", EXPECTED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_results_review_universe", TARGET_UNIVERSE, "target_universe"),
    ("additional_predictive_evidence_executed_true", True, "additional_predictive_evidence_executed"),
    ("additional_predictive_evidence_results_review_ready_true", True, "additional_predictive_evidence_results_review_ready"),
    ("ready_for_predictive_usefulness_reassessment_candidate_true", True, "ready_for_predictive_usefulness_reassessment_candidate"),
    ("predictive_usefulness_reassessment_candidate_created_true", True, "predictive_usefulness_reassessment_candidate_created"),
    ("predictive_usefulness_reassessment_scope_candidate_only", False, "predictive_usefulness_reassessment_review_created"),
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
    ("performance_signal_status_review_required", "REVIEW_REQUIRED_NOT_ACCEPTANCE_EVIDENCE", "check_performance_signal_status"),
    ("evidence_supports_direct_acceptance_false", False, "evidence_supports_direct_acceptance"),
    ("acceptance_recommendation_not_recommended_at_candidate_stage", "NOT_RECOMMENDED_AT_CANDIDATE_STAGE", "acceptance_recommendation"),
    ("per_ticker_reassessment_entries_12", 12, "per_ticker_reassessment_entry_count"),
    ("per_ticker_reassessment_digests_present", True, "per_ticker_reassessment_digests_present"),
    ("reassessment_domains_defined", REASSESSMENT_DOMAIN_IDS, "reassessment_domain_ids"),
    ("future_reassessment_chain_defined", FUTURE_REASSESSMENT_CHAIN, "future_reassessment_chain"),
    ("future_gates_defined", FUTURE_GATES, "future_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("planned_outputs_not_generated", True, "planned_outputs_not_generated"),
    ("planned_outputs_research_only", True, "planned_outputs_research_only"),
    ("provider_requests_made_false", False, "provider_requests_made"),
    ("live_provider_transport_enabled_false", False, "live_provider_transport_enabled"),
    ("market_data_acquisition_performed_false", False, "market_data_acquisition_performed"),
    ("dataset_generation_performed_false", False, "dataset_generation_performed"),
    ("canonical_dataset_regenerated_false", False, "canonical_dataset_regenerated"),
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


def _derived_check_fields(candidate: dict[str, Any]) -> dict[str, Any]:
    evidence = candidate.get("reviewed_evidence_summary", {})
    performance = candidate.get("performance_interpretation", {})
    entries = candidate.get("per_ticker_reassessment_candidate_entries", [])
    domains = candidate.get("reassessment_domains", [])
    planned = candidate.get("planned_outputs", [])
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
        "check_walk_forward_accuracy_range": performance.get("walk_forward_accuracy_range"),
        "check_performance_signal_status": performance.get("performance_signal_status"),
        "oos_performance_summary_bound": {
            "oos_majority_accuracy": performance.get("oos_majority_accuracy"),
            "oos_previous_direction_accuracy": performance.get("oos_previous_direction_accuracy"),
            "oos_ticker_cross_sectional_accuracy": performance.get(
                "oos_ticker_cross_sectional_accuracy"
            ),
            "oos_brier_score": performance.get("oos_brier_score"),
        }
        == {
            "oos_majority_accuracy": "0.539491",
            "oos_previous_direction_accuracy": "0.495984",
            "oos_ticker_cross_sectional_accuracy": "0.502677",
            "oos_brier_score": "0.24875351",
        },
        "per_ticker_reassessment_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_reassessment_digests_present": isinstance(entries, list)
        and all(
            isinstance(entry, dict)
            and isinstance(
                entry.get("per_ticker_predictive_usefulness_reassessment_candidate_digest"),
                str,
            )
            and len(entry["per_ticker_predictive_usefulness_reassessment_candidate_digest"])
            == 64
            for entry in entries
        ),
        "reassessment_domain_ids": [
            item.get("domain_id") for item in domains if isinstance(item, dict)
        ],
        "planned_outputs_not_generated": isinstance(planned, list)
        and all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in planned),
        "planned_outputs_research_only": isinstance(planned, list)
        and all(item.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(candidate)
    values.update(_derived_check_fields(candidate))
    return [_check(check_id, expected, values.get(field)) for check_id, expected, field in CHECK_FIELD_SPECS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    blockers = sum(
        item.get("status") == FAIL and item.get("severity") == BLOCKER for item in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "ready_for_operator_review": blockers == 0,
        "ready_for_predictive_usefulness_reassessment_review": False,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("predictive_usefulness_reassessment_candidate_digest", None)
    return payload


def predictive_usefulness_reassessment_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the reassessment candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_predictive_usefulness_reassessment_candidate_v1() -> dict:
    """Build the offline candidate without inspecting providers or regenerating evidence."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["predictive_usefulness_reassessment_candidate_digest"] = (
        predictive_usefulness_reassessment_candidate_digest_v1(candidate)
    )
    validate_predictive_usefulness_reassessment_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
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
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "predictive_execution_rerun_performed",
        "label_generation_rerun_performed",
        "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed",
        "metrics_recomputation_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_usefulness_reassessment_review_created",
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
        "evidence_supports_direct_acceptance",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise PredictiveUsefulnessReassessmentCandidateError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveUsefulnessReassessmentCandidateError(f"{current} must be false")
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveUsefulnessReassessmentCandidateError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveUsefulnessReassessmentCandidateError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_usefulness_reassessment_candidate_v1(candidate: dict) -> dict:
    """Validate the candidate without creating usefulness acceptance or runtime authority."""
    if not isinstance(candidate, dict):
        raise PredictiveUsefulnessReassessmentCandidateError(
            "reassessment candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    expected_base = _base_candidate()
    for field, expected in expected_base.items():
        if field in {
            "per_ticker_reassessment_candidate_entries",
            "reassessment_domains",
            "future_reassessment_chain",
            "future_gates",
            "risk_controls",
            "planned_outputs",
        }:
            continue
        _expect(candidate.get(field), expected, field)
    _expect(
        candidate.get("per_ticker_reassessment_candidate_entries"),
        expected_base["per_ticker_reassessment_candidate_entries"],
        "per_ticker_reassessment_candidate_entries",
    )
    _expect(candidate.get("reassessment_domains"), _reassessment_domains(), "reassessment_domains")
    _expect(
        candidate.get("future_reassessment_chain"),
        FUTURE_REASSESSMENT_CHAIN,
        "future_reassessment_chain",
    )
    _expect(candidate.get("future_gates"), FUTURE_GATES, "future_gates")
    _expect(candidate.get("risk_controls"), RISK_CONTROLS, "risk_controls")
    _expect(candidate.get("planned_outputs"), _planned_outputs(), "planned_outputs")
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessReassessmentCandidateError("candidate_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    _expect(checklist, expected_checklist, "candidate_checklist")
    failed = [item for item in expected_checklist if item.get("status") != PASS]
    if failed:
        raise PredictiveUsefulnessReassessmentCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), expected_summary, "candidate_summary")
    digest = candidate.get("predictive_usefulness_reassessment_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReassessmentCandidateError(
            "predictive_usefulness_reassessment_candidate_digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_reassessment_candidate_digest_v1(candidate),
        "predictive_usefulness_reassessment_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "predictive_usefulness_reassessment_candidate_digest": digest,
        "source_results_review_package_digest": candidate[
            "additional_predictive_evidence_results_review_package_digest"
        ],
        "per_ticker_entry_count": len(candidate["per_ticker_reassessment_candidate_entries"]),
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_operator_review": True,
        "ready_for_predictive_usefulness_reassessment_review": False,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_usefulness_reassessment_candidate_markdown_v1(candidate: dict) -> str:
    """Render a sanitized Markdown summary of the candidate-only artifact."""
    validation = validate_predictive_usefulness_reassessment_candidate_v1(candidate)
    evidence = candidate["reviewed_evidence_summary"]
    performance = candidate["performance_interpretation"]
    summary = candidate["candidate_summary"]
    registry = candidate["registry_approved_dataset_metadata"]
    lines = [
        "# MarketFlow Predictive Usefulness Reassessment Candidate Status",
        "",
        "## Title",
        "- Predictive Usefulness Reassessment Candidate v1.",
        "",
        "## Predictive Usefulness Reassessment Candidate",
        f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`",
        f"- Candidate digest: `{validation['predictive_usefulness_reassessment_candidate_digest']}`",
        "",
        "## Source Additional Predictive Evidence Results Review",
        f"- Results-review digest: `{candidate['additional_predictive_evidence_results_review_package_digest']}`",
        f"- Execution digest: `{candidate['additional_predictive_evidence_execution_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/scope: `{registry['dataset_name']}` / `{registry['dataset_scope']}`",
        f"- Record count/digest: `{registry['total_canonical_record_count']}` / `{registry['records_digest']}`",
        "",
        "## Target Universe",
        f"- `{', '.join(candidate['target_universe'])}`",
        "",
        "## Evidence Summary",
        f"- Label coverage available/unavailable: `{evidence['label_available_values']}` / `{evidence['label_unavailable_values']}`",
        f"- Feature rows/fields: `{evidence['feature_rows']}` / `{evidence['feature_fields']}`",
        f"- Walk-forward folds/OOS rows: `{evidence['walk_forward_fold_count']}` / `{evidence['oos_evaluation_rows']}`",
        f"- Leakage status/failed controls: `{evidence['leakage_status']}` / `{evidence['failed_leakage_controls']}`",
        "",
        "## Performance Interpretation",
        f"- Walk-forward accuracy range: `{performance['walk_forward_accuracy_range']}`",
        f"- Stability: `{performance['walk_forward_accuracy_stability_status']}`",
        f"- Signal status: `{performance['performance_signal_status']}`",
        f"- Baseline status: `{performance['baseline_outperformance_status']}`",
        "",
        "## Per-Ticker Reassessment Candidate Entries",
        f"- Entry count: `{len(candidate['per_ticker_reassessment_candidate_entries'])}`; META retains `913` records and every other ticker `1003`.",
        "",
        "## Reassessment Domains",
    ]
    lines.extend(f"- `{item['domain_id']}`" for item in candidate["reassessment_domains"])
    lines.extend(["", "## Future Reassessment Chain"])
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(candidate["future_reassessment_chain"], start=1)
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness: `{candidate['predictive_usefulness']}`.",
            f"- Direct acceptance supported: `{candidate['evidence_supports_direct_acceptance']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{candidate['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{candidate['runtime_use']}` / `{candidate['strategy_use']}` / `{candidate['paper_trading']}` / `{candidate['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- Candidate built offline from committed review facts; no provider, acquisition, regeneration, rerun, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- All planned outputs remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_reassessment_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write canonical candidate JSON once without overwriting an existing artifact."""
    candidate = build_predictive_usefulness_reassessment_candidate_v1()
    validation = validate_predictive_usefulness_reassessment_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_usefulness_reassessment_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessReassessmentCandidateError(
            "predictive usefulness reassessment candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessReassessmentCandidateError(
            "predictive usefulness reassessment candidate output already exists"
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
