"""Offline operator review for the redesigned-label planning candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import feature_predictive_evidence_planning_candidate_redesigned_labels_service as candidate_service


ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1 = (
    "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_v1"
)
FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY"
)
FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID"
)

DEFAULT_BRANCH = (
    "feature/feature-predictive-evidence-planning-candidate-review-redesigned-labels-v1"
)
DEFAULT_BASE_COMMIT = "75c74660bd1054af1e13604f62bce3bc2b2b7144"
EXPECTED_CANDIDATE_DIGEST = (
    "6de09ba499a262d6c7a1e5a0a69fee875c855bed86b78f28db4e099109a78251"
)
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


class FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
    ValueError
):
    """Raised when the operator-review package violates its closed contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
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


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(
        source
    )
    _expect(
        source.get(
            "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"
        ),
        EXPECTED_CANDIDATE_DIGEST,
        "source candidate digest",
    )
    _expect(source.get("candidate_summary", {}).get("total_checks"), 48, "source checklist total")
    _expect(source.get("candidate_summary", {}).get("passed_checks"), 48, "source checklist passed")
    _expect(source.get("candidate_summary", {}).get("failed_checks"), 0, "source checklist failed")
    _expect(source.get("candidate_summary", {}).get("blocker_count"), 0, "source blocker count")
    return source


def _per_ticker_review_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_feature_predictive_evidence_planning_candidate_review_digest",
        None,
    )
    return payload


def per_ticker_feature_predictive_evidence_planning_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one ticker review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _per_ticker_review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_candidate_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "redesigned_label_generation_results_status": source_entry[
                "redesigned_label_generation_results_status"
            ],
            "feature_predictive_evidence_planning_candidate_status": source_entry[
                "feature_predictive_evidence_planning_candidate_status"
            ],
            "feature_predictive_evidence_planning_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "predictive_evidence_execution_authorized": False,
            "predictive_evidence_execution_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_feature_predictive_evidence_planning_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
            "per_ticker_feature_predictive_evidence_planning_candidate_digest": source_entry[
                "per_ticker_feature_predictive_evidence_planning_candidate_digest"
            ],
            "planning_note": source_entry["planning_note"],
        }
        entry[
            "per_ticker_feature_predictive_evidence_planning_candidate_review_digest"
        ] = per_ticker_feature_predictive_evidence_planning_candidate_review_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1,
        "review_status": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY,
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
        "redesigned_label_regeneration_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "reviewed_feature_predictive_evidence_planning_candidate_kind": source[
            "artifact_kind"
        ],
        "reviewed_feature_predictive_evidence_planning_candidate_status": source[
            "candidate_status"
        ],
        "reviewed_feature_predictive_evidence_planning_candidate_digest": source[
            "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"
        ],
        "reviewed_feature_predictive_evidence_planning_candidate_checklist_total": summary[
            "total_checks"
        ],
        "reviewed_feature_predictive_evidence_planning_candidate_checklist_passed": summary[
            "passed_checks"
        ],
        "reviewed_feature_predictive_evidence_planning_candidate_checklist_failed": summary[
            "failed_checks"
        ],
        "reviewed_feature_predictive_evidence_planning_candidate_blocker_count": summary[
            "blocker_count"
        ],
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": source[
            "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"
        ],
        "redesigned_label_generation_results_review_package_digest": source[
            "redesigned_label_generation_results_review_package_digest"
        ],
        "redesigned_label_generation_execution_digest": source[
            "redesigned_label_generation_execution_digest"
        ],
        "redesigned_label_generation_approval_digest": source[
            "redesigned_label_generation_approval_digest"
        ],
        "redesigned_label_generation_candidate_review_package_digest": source[
            "redesigned_label_generation_candidate_review_package_digest"
        ],
        "redesigned_label_generation_candidate_digest": source[
            "redesigned_label_generation_candidate_digest"
        ],
        "research_registry_approval_digest": source[
            "research_registry_approval_digest"
        ],
        "records_digest": source["records_digest"],
        "label_values_digest": source["label_values_digest"],
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "redesigned_label_generation_performed": True,
        "actual_redesigned_labels_generated": True,
        "redesigned_label_generation_results_created": True,
        "redesigned_label_generation_results_review_created": True,
        "redesigned_label_generation_results_review_ready": True,
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels": True,
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created": True,
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review": True,
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_review_created": True,
        "feature_predictive_evidence_planning_approved": False,
        "feature_generation_candidate_created": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
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
        "no_tracked_marketflow_files": True,
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "redesigned_label_output_root": source["redesigned_label_output_root"],
        "redesigned_label_output_count": source["redesigned_label_output_count"],
        "redesigned_label_output_status": source["redesigned_label_output_status"],
        "label_family_count": source["label_family_count"],
        "threshold_strategy_count": source["threshold_strategy_count"],
        "horizon_strategy_count": source["horizon_strategy_count"],
        "label_value_row_count": source["label_value_row_count"],
        "label_family_coverage_entries": source["label_family_coverage_entries"],
        "available_label_value_count": source["available_label_value_count"],
        "unavailable_label_value_count": source["unavailable_label_value_count"],
        "label_generation_interpretation": source["label_generation_interpretation"],
        "feature_generation_interpretation": source["feature_generation_interpretation"],
        "predictive_usefulness_interpretation": source[
            "predictive_usefulness_interpretation"
        ],
        "feature_predictive_evidence_planning_candidate_objective": source[
            "feature_predictive_evidence_planning_candidate_objective"
        ],
        "feature_predictive_evidence_planning_candidate_scope": source[
            "feature_predictive_evidence_planning_candidate_scope"
        ],
        "feature_predictive_evidence_planning_candidate_mode": source[
            "feature_predictive_evidence_planning_candidate_mode"
        ],
        "feature_predictive_evidence_planning_candidate_authority_status": source[
            "feature_predictive_evidence_planning_candidate_authority_status"
        ],
        "reviewed_source_inputs": deepcopy(source["source_inputs"]),
        "reviewed_planned_feature_families": deepcopy(
            source["planned_feature_families"]
        ),
        "reviewed_planned_predictive_evidence_components": deepcopy(
            source["planned_predictive_evidence_components"]
        ),
        "reviewed_planned_model_baseline_families": deepcopy(
            source["planned_model_baseline_families"]
        ),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "per_ticker_candidate_review_entries": _per_ticker_review_entries(source),
        "reviewed_future_chain": deepcopy(source["future_chain"]),
        "reviewed_future_gates": deepcopy(source["future_gates"]),
        "reviewed_risk_controls": deepcopy(source["risk_controls"]),
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("candidate_kind_matches", candidate_service.ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS, "reviewed_feature_predictive_evidence_planning_candidate_kind"),
    ("candidate_status_ready_for_review", candidate_service.FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW, "reviewed_feature_predictive_evidence_planning_candidate_status"),
    ("candidate_digest_matches_expected", EXPECTED_CANDIDATE_DIGEST, "reviewed_feature_predictive_evidence_planning_candidate_digest"),
    ("candidate_checklist_zero_blockers", 0, "reviewed_feature_predictive_evidence_planning_candidate_blocker_count"),
    ("feature_predictive_evidence_planning_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"),
    ("redesigned_label_results_review_digest_bound", candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST, "redesigned_label_generation_results_review_package_digest"),
    ("redesigned_label_execution_digest_bound", candidate_service.EXPECTED_EXECUTION_DIGEST, "redesigned_label_generation_execution_digest"),
    ("redesigned_label_approval_digest_bound", candidate_service.EXPECTED_APPROVAL_DIGEST, "redesigned_label_generation_approval_digest"),
    ("label_values_digest_bound", candidate_service.EXPECTED_LABEL_VALUES_DIGEST, "label_values_digest"),
    ("research_registry_digest_bound", candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST, "research_registry_approval_digest"),
    ("records_digest_bound", candidate_service.EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_12_preserved", 12, "target_universe_count"),
    ("target_universe_matches_candidate_universe", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", candidate_service.EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("redesigned_label_results_review_ready_true", True, "redesigned_label_generation_results_review_ready"),
    ("ready_for_feature_or_predictive_evidence_planning_candidate_true", True, "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels"),
    ("feature_predictive_evidence_planning_candidate_created_true", True, "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created"),
    ("feature_predictive_evidence_planning_candidate_review_created_true", True, "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_review_created"),
    ("feature_predictive_evidence_planning_candidate_ready_true", True, "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review"),
    ("feature_generation_candidate_created_false", False, "feature_generation_candidate_created"),
    ("feature_generation_false", False, "feature_generation_performed"),
    ("metric_recomputation_false", False, "metric_recomputation_performed"),
    ("model_training_false", False, "model_training_performed"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
    ("source_inputs_reviewed", candidate_service.SOURCE_INPUT_IDS, "reviewed_source_input_ids"),
    ("planned_feature_families_reviewed", candidate_service.PLANNED_FEATURE_FAMILY_IDS, "reviewed_feature_family_ids"),
    ("planned_predictive_components_reviewed", candidate_service.PLANNED_PREDICTIVE_COMPONENT_IDS, "reviewed_predictive_component_ids"),
    ("planned_model_baseline_families_reviewed", candidate_service.PLANNED_MODEL_BASELINE_FAMILY_IDS, "reviewed_model_baseline_family_ids"),
    ("planned_outputs_not_generated", True, "reviewed_planned_outputs_not_generated"),
    ("planned_outputs_research_only", True, "reviewed_planned_outputs_research_only"),
    ("redesigned_label_value_row_count_143352", 143352, "label_value_row_count"),
    ("available_label_count_142200", 142200, "available_label_value_count"),
    ("unavailable_label_count_1152", 1152, "unavailable_label_value_count"),
    ("label_family_count_10", 10, "label_family_count"),
    ("threshold_strategy_count_7", 7, "threshold_strategy_count"),
    ("horizon_strategy_count_5", 5, "horizon_strategy_count"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_candidate_digests_present", True, "per_ticker_candidate_digests_valid"),
    ("per_ticker_review_digests_present", True, "per_ticker_review_digests_valid"),
    ("future_chain_reviewed", candidate_service.FUTURE_CHAIN, "reviewed_future_chain"),
    ("future_gates_reviewed", candidate_service.FUTURE_GATES, "reviewed_future_gates"),
    ("risk_controls_reviewed", candidate_service.RISK_CONTROLS, "reviewed_risk_controls"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("provider_requests_made_false", False, "provider_requests_made"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed"),
    ("dataset_regeneration_false", False, "dataset_regeneration_performed"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [spec[0] for spec in CHECK_FIELD_SPECS]


def _derived_check_fields(review_package: dict[str, Any]) -> dict[str, Any]:
    source_inputs = review_package.get("reviewed_source_inputs", [])
    feature_families = review_package.get("reviewed_planned_feature_families", [])
    predictive_components = review_package.get(
        "reviewed_planned_predictive_evidence_components", []
    )
    model_families = review_package.get(
        "reviewed_planned_model_baseline_families", []
    )
    planned_outputs = review_package.get("reviewed_planned_outputs", [])
    entries = review_package.get("per_ticker_candidate_review_entries", [])
    return {
        **review_package,
        "reviewed_source_input_ids": [row.get("source_input_id") for row in source_inputs] if isinstance(source_inputs, list) else [],
        "reviewed_feature_family_ids": [row.get("feature_family_id") for row in feature_families] if isinstance(feature_families, list) else [],
        "reviewed_predictive_component_ids": [row.get("component_id") for row in predictive_components] if isinstance(predictive_components, list) else [],
        "reviewed_model_baseline_family_ids": [row.get("model_or_baseline_family_id") for row in model_families] if isinstance(model_families, list) else [],
        "reviewed_planned_outputs_not_generated": isinstance(planned_outputs, list) and len(planned_outputs) == len(candidate_service.PLANNED_OUTPUT_IDS) and all(row.get("output_status") == candidate_service.PLANNED_NOT_GENERATED and row.get("generated") is False for row in planned_outputs),
        "reviewed_planned_outputs_research_only": isinstance(planned_outputs, list) and len(planned_outputs) == len(candidate_service.PLANNED_OUTPUT_IDS) and all(row.get("output_label") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE and row.get("research_only") is True and row.get("non_actionable") is True for row in planned_outputs),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_candidate_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(isinstance(row.get("per_ticker_feature_predictive_evidence_planning_candidate_digest"), str) and len(row["per_ticker_feature_predictive_evidence_planning_candidate_digest"]) == 64 for row in entries),
        "per_ticker_review_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(isinstance(row.get("per_ticker_feature_predictive_evidence_planning_candidate_review_digest"), str) and len(row["per_ticker_feature_predictive_evidence_planning_candidate_review_digest"]) == 64 and row["per_ticker_feature_predictive_evidence_planning_candidate_review_digest"] == per_ticker_feature_predictive_evidence_planning_candidate_review_digest_v1(row) for row in entries),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    values = _derived_check_fields(review_package)
    return [_check(check_id, expected, values.get(field)) for check_id, expected, field in CHECK_FIELD_SPECS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_feature_predictive_evidence_planning_approval": False,
        "feature_generation_candidate_created": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop(
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest",
        None,
    )
    return payload


def feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_digest_payload(review_package))


def build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Build an offline review package over a validated planning candidate."""
    source = _source_candidate(candidate)
    review_package = _base_review(source)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package[
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"
    ] = feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest_v1(
        review_package
    )
    validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED",
        "FEATURE_GENERATION_CANDIDATE",
        "FEATURE_GENERATION_APPROVED",
        "FEATURE_GENERATION_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
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
    forbidden_true = {
        "feature_predictive_evidence_planning_approved",
        "feature_generation_candidate_created",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Fail closed unless this is exactly the non-approving operator review."""
    if not isinstance(review_package, dict):
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
            "review package must be a JSON object"
        )
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY, "review_status")
    _reject_forbidden_values(review_package)
    expected = {
        "reviewed_feature_predictive_evidence_planning_candidate_kind": candidate_service.ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS,
        "reviewed_feature_predictive_evidence_planning_candidate_status": candidate_service.FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW,
        "reviewed_feature_predictive_evidence_planning_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "reviewed_feature_predictive_evidence_planning_candidate_checklist_total": 48,
        "reviewed_feature_predictive_evidence_planning_candidate_checklist_passed": 48,
        "reviewed_feature_predictive_evidence_planning_candidate_checklist_failed": 0,
        "reviewed_feature_predictive_evidence_planning_candidate_blocker_count": 0,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "redesigned_label_generation_results_review_package_digest": candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": candidate_service.EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": candidate_service.EXPECTED_APPROVAL_DIGEST,
        "redesigned_label_generation_candidate_review_package_digest": candidate_service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "redesigned_label_generation_candidate_digest": candidate_service.EXPECTED_CANDIDATE_DIGEST,
        "research_registry_approval_digest": candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": candidate_service.EXPECTED_RECORDS_DIGEST,
        "label_values_digest": candidate_service.EXPECTED_LABEL_VALUES_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": candidate_service.EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "redesigned_label_output_count": 11,
        "redesigned_label_output_status": "REVIEWED_AND_VERIFIED",
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "label_value_row_count": 143352,
        "label_family_coverage_entries": 144,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "feature_predictive_evidence_planning_candidate_objective": candidate_service.PLAN_OBJECTIVE,
        "feature_predictive_evidence_planning_candidate_scope": candidate_service.PLAN_SCOPE,
        "feature_predictive_evidence_planning_candidate_mode": candidate_service.PLAN_MODE,
        "feature_predictive_evidence_planning_candidate_authority_status": candidate_service.PLAN_AUTHORITY_STATUS,
        "reviewed_source_inputs": candidate_service._source_inputs(),
        "reviewed_planned_feature_families": candidate_service._feature_families(),
        "reviewed_planned_predictive_evidence_components": candidate_service._predictive_components(),
        "reviewed_planned_model_baseline_families": candidate_service._model_baseline_families(),
        "reviewed_planned_outputs": candidate_service._planned_outputs(),
        "per_ticker_candidate_review_entries": _per_ticker_review_entries(candidate_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1()),
        "reviewed_future_chain": candidate_service.FUTURE_CHAIN,
        "reviewed_future_gates": candidate_service.FUTURE_GATES,
        "reviewed_risk_controls": candidate_service.RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
    true_fields = [
        "created_offline",
        "research_only",
        "operator_review_required",
        "redesigned_label_generation_approved",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_label_generation_results_created",
        "redesigned_label_generation_results_review_created",
        "redesigned_label_generation_results_review_ready",
        "ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels",
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created",
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review",
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_review_created",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    ]
    false_fields = [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "canonical_dataset_regenerated",
        "redesigned_label_regeneration_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "feature_predictive_evidence_planning_approved",
        "feature_generation_candidate_created",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
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
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ]
    for field in true_fields:
        _expect(review_package.get(field), True, field)
    for field in false_fields:
        _expect(review_package.get(field), False, field)
    _expect(review_package.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
            "review_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review_checklist check ids")
    if any(row.get("status") != PASS for row in checklist):
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
            "review_checklist must pass"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get(
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
            "missing review digest"
        )
    _expect(digest, feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest_v1(review_package), "review digest")
    return {
        "status": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": digest,
        "reviewed_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "per_ticker_review_entry_count": len(review_package["per_ticker_candidate_review_entries"]),
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": True,
        "ready_for_feature_predictive_evidence_planning_approval": False,
        "feature_generation_candidate_created": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render the operator review without implying approval."""
    validation = validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Feature Predictive Evidence Planning Candidate Operator Review", "",
        "## Title", "- Feature / Predictive Evidence Planning Candidate Operator Review Package Using Redesigned Labels v1.", "",
        "## Feature / Predictive Evidence Planning Candidate Review Using Redesigned Labels", f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest']}`.", "",
        "## Reviewed Candidate", f"- Candidate artifact/status/digest: `{review_package['reviewed_feature_predictive_evidence_planning_candidate_kind']}` / `{review_package['reviewed_feature_predictive_evidence_planning_candidate_status']}` / `{review_package['reviewed_feature_predictive_evidence_planning_candidate_digest']}`; source checklist 48/48 with zero blockers.", "",
        "## Bound Evidence", f"- Results review/execution/label-values digests: `{review_package['redesigned_label_generation_results_review_package_digest']}` / `{review_package['redesigned_label_generation_execution_digest']}` / `{review_package['label_values_digest']}`.", "",
        "## Dataset and Universe", f"- `{review_package['dataset_name']}` contains `{review_package['total_canonical_record_count']}` frozen records for 12 ordered tickers; META remains `{review_package['meta_record_count']}`.", "",
        "## Source Redesigned Label Profile", f"- Reviewed outputs/families/thresholds/horizons/label rows: `{review_package['redesigned_label_output_count']}` / `{review_package['label_family_count']}` / `{review_package['threshold_strategy_count']}` / `{review_package['horizon_strategy_count']}` / `{review_package['label_value_row_count']}`.", "",
        "## Reviewed Source Inputs",
    ]
    lines.extend(f"- `{row['source_input_id']}`: `{row['source_input_status']}`." for row in review_package["reviewed_source_inputs"])
    lines.extend(["", "## Reviewed Planned Feature Families"])
    lines.extend(f"- `{row['feature_family_id']}`: `{row['feature_generation_status']}`." for row in review_package["reviewed_planned_feature_families"])
    lines.extend(["", "## Reviewed Planned Predictive Evidence Components"])
    lines.extend(f"- `{row['component_id']}`: `{row['component_status']}`." for row in review_package["reviewed_planned_predictive_evidence_components"])
    lines.extend(["", "## Reviewed Planned Model and Baseline Families"])
    lines.extend(f"- `{row['model_or_baseline_family_id']}`: `{row['model_or_baseline_status']}`." for row in review_package["reviewed_planned_model_baseline_families"])
    lines.extend(["", "## Reviewed Planned Outputs"])
    lines.extend(f"- `{row['planned_output_id']}`: `{row['output_status']}`." for row in review_package["reviewed_planned_outputs"])
    lines.extend(["", "## Per-Ticker Review Entries", "- Twelve entries preserve the exact registry order and both candidate/review digests; META remains 913 records. Feature and predictive-execution flags are false for every ticker.", "", "## Future Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(review_package["reviewed_future_chain"], 1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_risk_controls"])
    lines.extend([
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- This review validates the committed planning candidate only. It creates no planning approval, feature candidate, predictive-execution candidate, feature, metric, model, predictive evidence, acceptance, profitability, runtime, recommendation, or trading authority.", "- A separately governed planning approval remains future work if the operator selects it.", "",
    ])
    return "\n".join(lines)


def write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting an existing file."""
    review_package = build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(candidate)
    output_name = filename or "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
            "review filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(review_package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError(
            "review output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": review_package["review_status"],
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": review_package["feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"],
    }
