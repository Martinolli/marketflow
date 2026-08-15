"""Offline operator review of the predictive-usefulness reassessment candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_reassessment_candidate_service as candidate_service


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_V1 = (
    "predictive_usefulness_reassessment_candidate_review_v1"
)
PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY"
)

EXPECTED_CANDIDATE_DIGEST = (
    "d1fb7dca18ff8b5565a3807be45b936d869e7fe9394af41c0b0ef125aeda4efe"
)
EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST = candidate_service.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
EXPECTED_EXECUTION_DIGEST = candidate_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_EXECUTION_APPROVAL_DIGEST = candidate_service.EXPECTED_EXECUTION_APPROVAL_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = candidate_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = candidate_service.PLANNED_NOT_GENERATED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"


class PredictiveUsefulnessReassessmentCandidateReviewError(ValueError):
    """Raised when a reassessment-candidate review violates its review-only boundary."""


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
        raise PredictiveUsefulnessReassessmentCandidateReviewError(f"{field} mismatch")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_predictive_usefulness_reassessment_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_predictive_usefulness_reassessment_candidate_v1(source)
    _expect(
        source.get("predictive_usefulness_reassessment_candidate_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "source candidate digest",
    )
    return source


def _per_ticker_review_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_predictive_usefulness_reassessment_candidate_review_digest", None)
    return payload


def per_ticker_predictive_usefulness_reassessment_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker candidate review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _per_ticker_review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_reassessment_candidate_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "predictive_evidence_results_status": source_entry[
                "predictive_evidence_results_status"
            ],
            "predictive_usefulness_reassessment_candidate_status": (
                "READY_FOR_OPERATOR_REVIEW"
            ),
            "predictive_usefulness_reassessment_candidate_review_status": (
                READY_FOR_OPERATOR_ASSESSMENT
            ),
            "predictive_usefulness": source_entry["predictive_usefulness"],
            "predictive_usefulness_acceptance_candidate_created": source_entry[
                "predictive_usefulness_acceptance_candidate_created"
            ],
            "profitability": source_entry["profitability"],
            "runtime_use": source_entry["runtime_use"],
            "strategy_use": source_entry["strategy_use"],
            "paper_trading": source_entry["paper_trading"],
            "broker_execution": source_entry["broker_execution"],
            "source_predictive_usefulness_reassessment_candidate_digest": (
                source["predictive_usefulness_reassessment_candidate_digest"]
            ),
            "per_ticker_predictive_usefulness_reassessment_candidate_digest": source_entry[
                "per_ticker_predictive_usefulness_reassessment_candidate_digest"
            ],
        }
        entry["per_ticker_predictive_usefulness_reassessment_candidate_review_digest"] = (
            per_ticker_predictive_usefulness_reassessment_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    source_summary = source["candidate_summary"]
    return {
        "artifact_kind": (
            ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE
        ),
        "schema_version": (
            SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_V1
        ),
        "review_status": (
            PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY
        ),
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
        "ready_for_predictive_usefulness_reassessment_candidate": True,
        "predictive_usefulness_reassessment_candidate_created": True,
        "predictive_usefulness_reassessment_candidate_review_created": True,
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
        "reviewed_predictive_usefulness_reassessment_candidate_kind": source[
            "artifact_kind"
        ],
        "reviewed_predictive_usefulness_reassessment_candidate_status": source[
            "candidate_status"
        ],
        "reviewed_predictive_usefulness_reassessment_candidate_digest": source[
            "predictive_usefulness_reassessment_candidate_digest"
        ],
        "reviewed_predictive_usefulness_reassessment_candidate_checklist_total": (
            source_summary["total_checks"]
        ),
        "reviewed_predictive_usefulness_reassessment_candidate_checklist_passed": (
            source_summary["passed_checks"]
        ),
        "reviewed_predictive_usefulness_reassessment_candidate_checklist_failed": (
            source_summary["failed_checks"]
        ),
        "reviewed_predictive_usefulness_reassessment_candidate_blocker_count": (
            source_summary["blocker_count"]
        ),
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
        "research_registry_approval_digest": source["research_registry_approval_digest"],
        "canonical_dataset_freeze_digest": source["canonical_dataset_freeze_digest"],
        "records_digest": source["records_digest"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "reviewed_registry_approved_dataset_metadata": deepcopy(
            source["registry_approved_dataset_metadata"]
        ),
        "evidence_summary_status": source["evidence_summary_status"],
        "evidence_supports_future_reassessment_review": source[
            "evidence_supports_future_reassessment_review"
        ],
        "evidence_supports_direct_acceptance": source[
            "evidence_supports_direct_acceptance"
        ],
        "operator_review_required_before_acceptance": source[
            "operator_review_required_before_acceptance"
        ],
        "acceptance_recommendation": source["acceptance_recommendation"],
        "reviewed_evidence_summary": deepcopy(source["reviewed_evidence_summary"]),
        "reviewed_performance_interpretation": deepcopy(
            source["performance_interpretation"]
        ),
        "per_ticker_reassessment_candidate_review_entries": (
            _per_ticker_review_entries(source)
        ),
        "reviewed_reassessment_domains": deepcopy(source["reassessment_domains"]),
        "reviewed_future_reassessment_chain": deepcopy(
            source["future_reassessment_chain"]
        ),
        "reviewed_future_gates": deepcopy(source["future_gates"]),
        "reviewed_risk_controls": deepcopy(source["risk_controls"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "planned_output_count": len(source["planned_outputs"]),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("candidate_kind_matches", candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE, "reviewed_predictive_usefulness_reassessment_candidate_kind"),
    ("candidate_status_ready_for_review", candidate_service.PREDICTIVE_USEFULNESS_REASSESSMENT_READY_FOR_OPERATOR_REVIEW, "reviewed_predictive_usefulness_reassessment_candidate_status"),
    ("candidate_digest_matches_expected", EXPECTED_CANDIDATE_DIGEST, "reviewed_predictive_usefulness_reassessment_candidate_digest"),
    ("candidate_checklist_zero_blockers", 0, "reviewed_predictive_usefulness_reassessment_candidate_blocker_count"),
    ("results_review_digest_bound", EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST, "additional_predictive_evidence_results_review_package_digest"),
    ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_digest"),
    ("execution_approval_digest_bound", EXPECTED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_candidate_universe", TARGET_UNIVERSE, "target_universe"),
    ("additional_predictive_evidence_executed_true", True, "additional_predictive_evidence_executed"),
    ("additional_predictive_evidence_results_review_ready_true", True, "additional_predictive_evidence_results_review_ready"),
    ("ready_for_predictive_usefulness_reassessment_candidate_true", True, "ready_for_predictive_usefulness_reassessment_candidate"),
    ("predictive_usefulness_reassessment_candidate_created_true", True, "predictive_usefulness_reassessment_candidate_created"),
    ("predictive_usefulness_reassessment_candidate_review_created_true", True, "predictive_usefulness_reassessment_candidate_review_created"),
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
    ("per_ticker_reassessment_entries_12", 12, "per_ticker_review_entry_count"),
    ("per_ticker_reassessment_candidate_digests_present", True, "per_ticker_candidate_digests_present"),
    ("per_ticker_reassessment_review_digests_present", True, "per_ticker_review_digests_present"),
    ("reassessment_domains_reviewed", candidate_service.REASSESSMENT_DOMAIN_IDS, "reassessment_domain_ids"),
    ("future_reassessment_chain_reviewed", candidate_service.FUTURE_REASSESSMENT_CHAIN, "reviewed_future_reassessment_chain"),
    ("future_gates_defined", candidate_service.FUTURE_GATES, "reviewed_future_gates"),
    ("risk_controls_defined", candidate_service.RISK_CONTROLS, "reviewed_risk_controls"),
    ("planned_outputs_7", 7, "planned_output_count"),
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
    evidence = review_package.get("reviewed_evidence_summary", {})
    performance = review_package.get("reviewed_performance_interpretation", {})
    entries = review_package.get("per_ticker_reassessment_candidate_review_entries", [])
    domains = review_package.get("reviewed_reassessment_domains", [])
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
        "per_ticker_review_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_candidate_digests_present": isinstance(entries, list)
        and all(
            isinstance(item, dict)
            and isinstance(
                item.get("per_ticker_predictive_usefulness_reassessment_candidate_digest"),
                str,
            )
            and len(item["per_ticker_predictive_usefulness_reassessment_candidate_digest"])
            == 64
            for item in entries
        ),
        "per_ticker_review_digests_present": isinstance(entries, list)
        and all(
            isinstance(item, dict)
            and isinstance(
                item.get(
                    "per_ticker_predictive_usefulness_reassessment_candidate_review_digest"
                ),
                str,
            )
            and len(
                item[
                    "per_ticker_predictive_usefulness_reassessment_candidate_review_digest"
                ]
            )
            == 64
            for item in entries
        ),
        "reassessment_domain_ids": [
            item.get("domain_id") for item in domains if isinstance(item, dict)
        ],
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(review_package)
    values.update(_derived_check_fields(review_package))
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
        "ready_for_operator_assessment": blockers == 0,
        "ready_for_predictive_usefulness_reassessment_review": False,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_usefulness_reassessment_candidate_review_package_digest", None)
    return payload


def predictive_usefulness_reassessment_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the semantic digest for the candidate operator-review package."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_usefulness_reassessment_candidate_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    """Build an offline review package for the exact reassessment candidate."""
    source = _source_candidate(candidate)
    review_package = _base_review(source)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package[
        "predictive_usefulness_reassessment_candidate_review_package_digest"
    ] = predictive_usefulness_reassessment_candidate_review_package_digest_v1(review_package)
    validate_predictive_usefulness_reassessment_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
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
                raise PredictiveUsefulnessReassessmentCandidateReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveUsefulnessReassessmentCandidateReviewError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveUsefulnessReassessmentCandidateReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveUsefulnessReassessmentCandidateReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_usefulness_reassessment_candidate_review_package_v1(
    review_package: dict,
) -> dict:
    """Validate the review package while keeping all later gates closed."""
    if not isinstance(review_package, dict):
        raise PredictiveUsefulnessReassessmentCandidateReviewError(
            "candidate review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    expected_source = candidate_service.build_predictive_usefulness_reassessment_candidate_v1()
    expected_base = _base_review(expected_source)
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessReassessmentCandidateReviewError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    failed = [item for item in expected_checklist if item.get("status") != PASS]
    if failed:
        raise PredictiveUsefulnessReassessmentCandidateReviewError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "predictive_usefulness_reassessment_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReassessmentCandidateReviewError(
            "predictive usefulness reassessment candidate review package digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_reassessment_candidate_review_package_digest_v1(
            review_package
        ),
        "predictive_usefulness_reassessment_candidate_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_usefulness_reassessment_candidate_review_package_digest": digest,
        "reviewed_predictive_usefulness_reassessment_candidate_digest": review_package[
            "reviewed_predictive_usefulness_reassessment_candidate_digest"
        ],
        "per_ticker_review_entry_count": len(
            review_package["per_ticker_reassessment_candidate_review_entries"]
        ),
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_operator_assessment": True,
        "ready_for_predictive_usefulness_reassessment_review": False,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_usefulness_reassessment_candidate_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized Markdown summary of the operator-review package."""
    validation = validate_predictive_usefulness_reassessment_candidate_review_package_v1(
        review_package
    )
    evidence = review_package["reviewed_evidence_summary"]
    performance = review_package["reviewed_performance_interpretation"]
    summary = review_package["review_summary"]
    registry = review_package["reviewed_registry_approved_dataset_metadata"]
    lines = [
        "# MarketFlow Predictive Usefulness Reassessment Candidate Operator Review Status",
        "",
        "## Title",
        "- Predictive Usefulness Reassessment Candidate Operator Review Package v1.",
        "",
        "## Predictive Usefulness Reassessment Candidate Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`",
        f"- Review digest: `{validation['predictive_usefulness_reassessment_candidate_review_package_digest']}`",
        "",
        "## Reviewed Candidate",
        f"- Candidate artifact/status: `{review_package['reviewed_predictive_usefulness_reassessment_candidate_kind']}` / `{review_package['reviewed_predictive_usefulness_reassessment_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_predictive_usefulness_reassessment_candidate_digest']}`",
        f"- Candidate checks/blockers: `{review_package['reviewed_predictive_usefulness_reassessment_candidate_checklist_passed']}` / `{review_package['reviewed_predictive_usefulness_reassessment_candidate_blocker_count']}`",
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
        "## Evidence Summary Review",
        f"- Label available/unavailable: `{evidence['label_available_values']}` / `{evidence['label_unavailable_values']}`",
        f"- Feature rows/fields: `{evidence['feature_rows']}` / `{evidence['feature_fields']}`",
        f"- Walk-forward folds/OOS rows: `{evidence['walk_forward_fold_count']}` / `{evidence['oos_evaluation_rows']}`",
        f"- Leakage status/failed controls: `{evidence['leakage_status']}` / `{evidence['failed_leakage_controls']}`",
        "",
        "## Performance Interpretation Review",
        f"- Walk-forward range/stability: `{performance['walk_forward_accuracy_range']}` / `{performance['walk_forward_accuracy_stability_status']}`",
        f"- Performance signal: `{performance['performance_signal_status']}`",
        f"- Baseline status: `{performance['baseline_outperformance_status']}`",
        "",
        "## Per-Ticker Reassessment Candidate Review Entries",
        f"- Entry count: `{len(review_package['per_ticker_reassessment_candidate_review_entries'])}`; all source candidate and review digests are bound.",
        "",
        "## Reassessment Domains",
    ]
    lines.extend(
        f"- `{item['domain_id']}`" for item in review_package["reviewed_reassessment_domains"]
    )
    lines.extend(["", "## Future Reassessment Chain"])
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(
            review_package["reviewed_future_reassessment_chain"], start=1
        )
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness: `{review_package['predictive_usefulness']}`; direct acceptance supported: `{review_package['evidence_supports_direct_acceptance']}`.",
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
            "- Review built offline from the exact candidate; no provider, acquisition, regeneration, rerun, recomputation, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- The reassessment review itself remains future work; planned outputs remain not generated and research-only.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_reassessment_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write canonical review JSON once without overwriting an existing artifact."""
    review_package = build_predictive_usefulness_reassessment_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_predictive_usefulness_reassessment_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "predictive_usefulness_reassessment_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessReassessmentCandidateReviewError(
            "predictive usefulness reassessment candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessReassessmentCandidateReviewError(
            "predictive usefulness reassessment candidate review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
