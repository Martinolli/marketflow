"""Offline operator review for the redesigned-label feature candidate."""

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
    feature_generation_candidate_redesigned_labels_service as candidate_service,
)


ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE = (
    "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1 = (
    "feature_generation_candidate_using_redesigned_labels_review_v1"
)
FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY = (
    "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY"
)
FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_VALID = (
    "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_VALID"
)

DEFAULT_BRANCH = "feature/feature-generation-candidate-review-redesigned-labels-v1"
DEFAULT_BASE_COMMIT = "1c770d4640fba8bcb649fdafb00b7043a1a7ae8e"
EXPECTED_CANDIDATE_DIGEST = (
    "21b3bc905f3d553f4ec74bd70f758bbbc9be02ae906af1732c3b4fb5aaf12d1e"
)

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER


class FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(ValueError):
    """Raised when the review package violates its closed contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
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
        candidate_service.build_feature_generation_candidate_using_redesigned_labels_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    try:
        candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1(
            source
        )
    except candidate_service.FeatureGenerationCandidateRedesignedLabelsError as exc:
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
            "source feature generation candidate is invalid"
        ) from exc
    _expect(
        source.get("feature_generation_candidate_using_redesigned_labels_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "source candidate digest",
    )
    _expect(
        source.get("candidate_status"),
        candidate_service.FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW,
        "source candidate status",
    )
    _expect(source.get("candidate_summary", {}).get("total_checks"), 47, "source checklist total")
    _expect(source.get("candidate_summary", {}).get("passed_checks"), 47, "source checklist passed")
    _expect(source.get("candidate_summary", {}).get("failed_checks"), 0, "source checklist failed")
    _expect(source.get("candidate_summary", {}).get("blocker_count"), 0, "source blocker count")
    return source


def _per_ticker_review_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_feature_generation_candidate_review_digest", None)
    return payload


def per_ticker_feature_generation_candidate_review_digest_v1(
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
            "feature_predictive_evidence_planning_approval_status": source_entry[
                "feature_predictive_evidence_planning_approval_status"
            ],
            "feature_generation_candidate_status": source_entry[
                "feature_generation_candidate_status"
            ],
            "feature_generation_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_values_created": False,
            "predictive_evidence_execution_authorized": False,
            "predictive_evidence_execution_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_feature_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
            "per_ticker_feature_generation_candidate_digest": source_entry[
                "per_ticker_feature_generation_candidate_digest"
            ],
        }
        if source_entry["ticker"] == "META":
            entry["planning_note"] = source_entry["planning_note"]
        entry["per_ticker_feature_generation_candidate_review_digest"] = (
            per_ticker_feature_generation_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1,
        "review_status": FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY,
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
        "reviewed_feature_generation_candidate_kind": source["artifact_kind"],
        "reviewed_feature_generation_candidate_status": source["candidate_status"],
        "reviewed_feature_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "reviewed_feature_generation_candidate_checklist_total": summary["total_checks"],
        "reviewed_feature_generation_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_feature_generation_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_feature_generation_candidate_blocker_count": summary["blocker_count"],
        "feature_generation_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": source[
            "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"
        ],
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": source[
            "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"
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
        "research_registry_approval_digest": source[
            "research_registry_approval_digest"
        ],
        "records_digest": source["records_digest"],
        "label_values_digest": source["label_values_digest"],
        "feature_predictive_evidence_planning_approved": True,
        "feature_predictive_evidence_planning_approval_created": True,
        "ready_for_feature_generation_candidate_using_redesigned_labels": True,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": False,
        "feature_generation_candidate_created": True,
        "feature_generation_candidate_using_redesigned_labels_created": True,
        "feature_generation_candidate_using_redesigned_labels_ready_for_operator_review": True,
        "feature_generation_candidate_using_redesigned_labels_review_created": True,
        "feature_generation_approved": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "feature_values_created": False,
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
        "redesigned_label_output_count": source["redesigned_label_output_count"],
        "redesigned_label_output_status": source[
            "redesigned_label_output_status"
        ],
        "label_family_count": source["label_family_count"],
        "threshold_strategy_count": source["threshold_strategy_count"],
        "horizon_strategy_count": source["horizon_strategy_count"],
        "label_value_row_count": source["label_value_row_count"],
        "label_family_coverage_entries": source["label_family_coverage_entries"],
        "available_label_value_count": source["available_label_value_count"],
        "unavailable_label_value_count": source["unavailable_label_value_count"],
        "feature_generation_candidate_objective": source[
            "feature_generation_candidate_objective"
        ],
        "feature_generation_candidate_scope": source[
            "feature_generation_candidate_scope"
        ],
        "feature_generation_candidate_mode": source[
            "feature_generation_candidate_mode"
        ],
        "feature_generation_candidate_authority_status": source[
            "feature_generation_candidate_authority_status"
        ],
        "reviewed_source_inputs": deepcopy(source["source_inputs"]),
        "reviewed_planned_feature_families": deepcopy(
            source["planned_feature_families"]
        ),
        "reviewed_feature_schema_contract": deepcopy(
            source["planned_feature_schema_contract"]
        ),
        "reviewed_feature_label_alignment_controls": deepcopy(
            source["planned_feature_label_alignment_controls"]
        ),
        "reviewed_quality_checks": deepcopy(source["planned_feature_quality_checks"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "per_ticker_candidate_review_entries": _per_ticker_review_entries(source),
        "future_chain": deepcopy(source["future_chain"]),
        "future_gates": deepcopy(source["future_gates"]),
        "risk_controls": deepcopy(source["risk_controls"]),
    }


CHECK_FIELD_SPECS = [
    ("candidate_kind_matches", candidate_service.ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS, "reviewed_feature_generation_candidate_kind"),
    ("candidate_status_ready_for_review", candidate_service.FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW, "reviewed_feature_generation_candidate_status"),
    ("candidate_digest_matches_expected", EXPECTED_CANDIDATE_DIGEST, "reviewed_feature_generation_candidate_digest"),
    ("candidate_checklist_zero_blockers", 0, "reviewed_feature_generation_candidate_blocker_count"),
    ("feature_generation_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "feature_generation_candidate_using_redesigned_labels_digest"),
    ("feature_predictive_evidence_planning_approval_digest_bound", candidate_service.EXPECTED_PLANNING_APPROVAL_DIGEST, "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"),
    ("planning_candidate_review_digest_bound", candidate_service.EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST, "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"),
    ("redesigned_label_results_review_digest_bound", candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST, "redesigned_label_generation_results_review_package_digest"),
    ("label_values_digest_bound", candidate_service.EXPECTED_LABEL_VALUES_DIGEST, "label_values_digest"),
    ("research_registry_digest_bound", candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST, "research_registry_approval_digest"),
    ("records_digest_bound", candidate_service.EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("target_universe_matches_candidate_universe", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", candidate_service.EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("feature_predictive_evidence_planning_approved_true", True, "feature_predictive_evidence_planning_approved"),
    ("ready_for_feature_generation_candidate_true", True, "ready_for_feature_generation_candidate_using_redesigned_labels"),
    ("ready_for_additional_predictive_evidence_execution_candidate_false", False, "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"),
    ("feature_generation_candidate_created_true", True, "feature_generation_candidate_created"),
    ("feature_generation_candidate_review_created_true", True, "feature_generation_candidate_using_redesigned_labels_review_created"),
    ("feature_generation_candidate_ready_for_operator_review_true", True, "feature_generation_candidate_using_redesigned_labels_ready_for_operator_review"),
    ("feature_generation_authorized_false", False, "feature_generation_authorized"),
    ("feature_generation_performed_false", False, "feature_generation_performed"),
    ("feature_values_created_false", False, "feature_values_created"),
    ("planned_feature_families_10_reviewed", candidate_service.PLANNED_FEATURE_FAMILY_IDS, "reviewed_feature_family_ids"),
    ("planned_feature_groups_reviewed", candidate_service.PLANNED_FEATURE_GROUP_IDS, "reviewed_feature_group_ids"),
    ("planned_feature_schema_contract_reviewed", candidate_service.FEATURE_SCHEMA_FIELDS, "reviewed_schema_fields"),
    ("planned_alignment_controls_reviewed", candidate_service.ALIGNMENT_CONTROL_IDS, "reviewed_alignment_control_ids"),
    ("planned_quality_checks_reviewed", candidate_service.PLANNED_QUALITY_CHECK_IDS, "reviewed_quality_check_ids"),
    ("planned_outputs_not_generated", True, "planned_outputs_not_generated"),
    ("planned_outputs_research_only", True, "planned_outputs_research_only"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_candidate_digests_present", True, "per_ticker_candidate_digests_valid"),
    ("per_ticker_review_digests_present", True, "per_ticker_review_digests_valid"),
    ("metric_recomputation_false", False, "metric_recomputation_performed"),
    ("model_training_false", False, "model_training_performed"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
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
    ("feature_generation_false", False, "feature_generation_performed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("future_chain_reviewed", candidate_service.FUTURE_CHAIN, "future_chain"),
    ("future_gates_reviewed", candidate_service.FUTURE_GATES, "future_gates"),
    ("risk_controls_reviewed", candidate_service.RISK_CONTROLS, "risk_controls"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [spec[0] for spec in CHECK_FIELD_SPECS]


def _derived_check_fields(review: dict[str, Any]) -> dict[str, Any]:
    families = review.get("reviewed_planned_feature_families", [])
    groups = [
        group
        for family in families
        for group in family.get("planned_feature_groups", [])
    ] if isinstance(families, list) else []
    schema = review.get("reviewed_feature_schema_contract", {})
    controls = review.get("reviewed_feature_label_alignment_controls", [])
    quality = review.get("reviewed_quality_checks", [])
    outputs = review.get("reviewed_planned_outputs", [])
    entries = review.get("per_ticker_candidate_review_entries", [])
    return {
        **review,
        "reviewed_feature_family_ids": [row.get("feature_family_id") for row in families] if isinstance(families, list) else [],
        "reviewed_feature_group_ids": [row.get("feature_group_id") for row in groups],
        "reviewed_schema_fields": schema.get("planned_schema_fields", []) if isinstance(schema, dict) else [],
        "reviewed_alignment_control_ids": [row.get("control_id") for row in controls] if isinstance(controls, list) else [],
        "reviewed_quality_check_ids": [row.get("planned_check_id") for row in quality] if isinstance(quality, list) else [],
        "planned_outputs_not_generated": isinstance(outputs, list) and len(outputs) == len(candidate_service.PLANNED_OUTPUT_IDS) and all(row.get("output_status") == candidate_service.PLANNED_NOT_GENERATED and row.get("generated") is False for row in outputs),
        "planned_outputs_research_only": isinstance(outputs, list) and len(outputs) == len(candidate_service.PLANNED_OUTPUT_IDS) and all(row.get("output_label") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE and row.get("research_only") is True and row.get("non_actionable") is True for row in outputs),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_candidate_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(isinstance(row.get("per_ticker_feature_generation_candidate_digest"), str) and len(row["per_ticker_feature_generation_candidate_digest"]) == 64 for row in entries),
        "per_ticker_review_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(isinstance(row.get("per_ticker_feature_generation_candidate_review_digest"), str) and len(row["per_ticker_feature_generation_candidate_review_digest"]) == 64 and row["per_ticker_feature_generation_candidate_review_digest"] == per_ticker_feature_generation_candidate_review_digest_v1(row) for row in entries),
    }


def _checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_check_fields(review)
    return [
        _check(check_id, expected, fields.get(field))
        for check_id, expected, field in CHECK_FIELD_SPECS
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_feature_generation_approval": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review)
    payload.pop(
        "feature_generation_candidate_using_redesigned_labels_review_package_digest",
        None,
    )
    return payload


def feature_generation_candidate_using_redesigned_labels_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_digest_payload(review_package))


def build_feature_generation_candidate_using_redesigned_labels_review_package_v1(
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Review one valid candidate without executing or authorizing features."""
    source = _source_candidate(candidate)
    review = _base_review(source)
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review[
        "feature_generation_candidate_using_redesigned_labels_review_package_digest"
    ] = feature_generation_candidate_using_redesigned_labels_review_package_digest_v1(
        review
    )
    validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(
        review
    )
    return review


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
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
        "feature_generation_approved",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "feature_values_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            if key in forbidden_true and item is True:
                raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
                    f"{path}.{key} must remain false"
                )
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        if value in forbidden_artifacts:
            raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
                f"{path} contains forbidden downstream artifact"
            )
        if value == "accepted":
            raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
                f"{path} must not accept predictive usefulness or profitability"
            )
        if value == "AUTHORIZED":
            raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
                f"{path} must not grant runtime or trading authority"
            )


def validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Fail closed unless the object is exactly the review-only package."""
    if not isinstance(review_package, dict):
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
            "review_package must be a JSON object"
        )
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY, "review_status")
    _reject_forbidden_values(review_package)
    source = _source_candidate(None)
    expected = _base_review(source)
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
            "review_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review_checklist check ids")
    _expect(checklist, _checklist(review_package), "review_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
            "review_checklist must pass"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get(
        "feature_generation_candidate_using_redesigned_labels_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
            "missing review digest"
        )
    _expect(digest, feature_generation_candidate_using_redesigned_labels_review_package_digest_v1(review_package), "review digest")
    return {
        "status": FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "feature_generation_candidate_using_redesigned_labels_review_package_digest": digest,
        "reviewed_feature_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "per_ticker_review_entry_count": len(
            review_package["per_ticker_candidate_review_entries"]
        ),
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": True,
        "ready_for_feature_generation_approval": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_feature_generation_candidate_using_redesigned_labels_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render the review package without implying approval or execution."""
    validation = validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Feature Generation Candidate Operator Review Status",
        "",
        "## Title",
        "- Feature Generation Candidate Operator Review Package Using Redesigned Labels v1.",
        "",
        "## Feature Generation Candidate Review Using Redesigned Labels",
        f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['feature_generation_candidate_using_redesigned_labels_review_package_digest']}`.",
        "",
        "## Reviewed Candidate",
        f"- Kind/status/digest: `{review_package['reviewed_feature_generation_candidate_kind']}` / `{review_package['reviewed_feature_generation_candidate_status']}` / `{review_package['reviewed_feature_generation_candidate_digest']}`.",
        f"- Candidate checklist total/passed/failed/blockers: `{review_package['reviewed_feature_generation_candidate_checklist_total']}` / `{review_package['reviewed_feature_generation_candidate_checklist_passed']}` / `{review_package['reviewed_feature_generation_candidate_checklist_failed']}` / `{review_package['reviewed_feature_generation_candidate_blocker_count']}`.",
        "",
        "## Bound Evidence",
        f"- Planning approval/review/candidate: `{review_package['feature_predictive_evidence_planning_approval_using_redesigned_labels_digest']}` / `{review_package['feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest']}` / `{review_package['feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- `{review_package['dataset_name']}` contains `{review_package['total_canonical_record_count']}` frozen records for the ordered 12-ticker universe; META remains `{review_package['meta_record_count']}`.",
        "",
        "## Source Redesigned Label Profile",
        f"- Reviewed outputs/families/thresholds/horizons/rows: `{review_package['redesigned_label_output_count']}` / `{review_package['label_family_count']}` / `{review_package['threshold_strategy_count']}` / `{review_package['horizon_strategy_count']}` / `{review_package['label_value_row_count']}`.",
        "",
        "## Reviewed Source Inputs",
    ]
    lines.extend(f"- `{row['source_input_id']}`: `{row['source_input_status']}`." for row in review_package["reviewed_source_inputs"])
    lines.extend(["", "## Reviewed Planned Feature Families"])
    lines.extend(f"- `{row['feature_family_id']}`: `{row['feature_generation_candidate_status']}`." for row in review_package["reviewed_planned_feature_families"])
    lines.extend(["", "## Reviewed Planned Feature Groups"])
    for family in review_package["reviewed_planned_feature_families"]:
        lines.extend(f"- `{group['feature_group_id']}`: `{group['group_status']}`." for group in family["planned_feature_groups"])
    lines.extend(["", "## Reviewed Feature Schema Contract", f"- `{review_package['reviewed_feature_schema_contract']['feature_schema_contract_status']}` with all 16 fields preserved and no feature values created."])
    lines.extend(["", "## Reviewed Feature / Label Alignment Controls"])
    lines.extend(f"- `{row['control_id']}`: `{row['execution_status']}`." for row in review_package["reviewed_feature_label_alignment_controls"])
    lines.extend(["", "## Reviewed Quality Checks"])
    lines.extend(f"- `{row['planned_check_id']}`: `{row['planned_check_status']}`." for row in review_package["reviewed_quality_checks"])
    lines.extend(["", "## Per-Ticker Review Entries", "- Twelve deterministic review entries preserve source candidate digests and exact record counts; META remains 913.", "", "## Future Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(review_package["future_chain"], 1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend([
        "",
        "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "",
        "## Guardrails",
        "- This review package assesses only the candidate. It does not approve, authorize, or perform feature generation and creates no feature values, predictive evidence, model training, acceptance, profitability, runtime, strategy, paper-trading, broker, or recommendation authority.",
        "- A separate feature-generation approval remains future work if selected.",
        "",
    ])
    return "\n".join(lines)


def write_feature_generation_candidate_using_redesigned_labels_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting existing evidence."""
    review = build_feature_generation_candidate_using_redesigned_labels_review_package_v1(
        candidate
    )
    output_name = filename or "feature_generation_candidate_using_redesigned_labels_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
            "review filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(review)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise FeatureGenerationCandidateRedesignedLabelsOperatorReviewError(
            "review output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": review["review_status"],
        "feature_generation_candidate_using_redesigned_labels_review_package_digest": review[
            "feature_generation_candidate_using_redesigned_labels_review_package_digest"
        ],
    }
