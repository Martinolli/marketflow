"""Offline operator approval for future redesigned-label feature generation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    feature_generation_candidate_redesigned_labels_operator_review_service as review_service,
)


ARTIFACT_KIND_FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS = (
    "FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_V1 = (
    "feature_generation_approval_using_redesigned_labels_v1"
)
FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS = (
    "FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS"
)
FEATURE_GENERATION_APPROVAL_ONLY = "FEATURE_GENERATION_APPROVAL_ONLY"
OPERATOR_DECISION_APPROVE_FEATURE_GENERATION_USING_REDESIGNED_LABELS = (
    "APPROVE_FEATURE_GENERATION_USING_REDESIGNED_LABELS"
)
OPERATOR_ATTESTATION_VERSION_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_V1 = (
    "feature_generation_approval_using_redesigned_labels_operator_attestation_v1"
)
REQUIRED_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE = (
    "APPROVE FEATURE GENERATION USING REDESIGNED LABELS "
    "MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "FEATURE_GENERATION_APPROVAL_ONLY"
)

DEFAULT_BRANCH = "feature/feature-generation-approval-redesigned-labels-v1"
DEFAULT_BASE_COMMIT = "0bf268f2a9c8ee9ac3a16dd59ce9cb33c60ee73b"
EXPECTED_CANDIDATE_REVIEW_DIGEST = (
    "d16cbdf42e44cbd95a5fa59fbb3dca5c00b6a888e8583f440369fa9a828d3a15"
)
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_PLANNING_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_PLANNING_APPROVAL_DIGEST
)
EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST = (
    review_service.candidate_service.EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_PLANNING_CANDIDATE_DIGEST = (
    review_service.candidate_service.EXPECTED_PLANNING_CANDIDATE_DIGEST
)
EXPECTED_RESULTS_REVIEW_DIGEST = review_service.candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = review_service.candidate_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST = review_service.candidate_service.EXPECTED_APPROVAL_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = review_service.candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = review_service.candidate_service.EXPECTED_RECORDS_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = review_service.candidate_service.EXPECTED_LABEL_VALUES_DIGEST

TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER
APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY = (
    "APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY"
)
NOT_REGENERATED = "NOT_REGENERATED"
NOT_EXECUTED = "NOT_EXECUTED"

FEATURE_GENERATION_OBJECTIVE = (
    "GENERATE_RESEARCH_ONLY_FEATURES_USING_REDESIGNED_LABELS_AND_FROZEN_CANONICAL_DATASET"
)
FEATURE_GENERATION_MODE = "AUTHORIZED_NOT_GENERATED"
FEATURE_GENERATION_AUTHORITY_STATUS = "AUTHORIZED_FOR_FUTURE_FEATURE_GENERATION_ONLY"

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_feature_generation_approval_scope_only",
    "operator_confirms_feature_generation_authorized",
    "operator_confirms_ready_for_feature_generation_execution_using_redesigned_labels",
    "operator_confirms_no_feature_generation_performed",
    "operator_confirms_no_feature_values_created",
    "operator_confirms_no_predictive_evidence_execution_candidate",
    "operator_confirms_no_predictive_evidence_execution",
    "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_strategy_authorization",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

NEXT_CHAIN = [
    "Feature Generation Execution Using Redesigned Labels v1.",
    "Feature Generation Results Review Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Candidate Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Approval and Execution, if separately approved.",
    "Additional Predictive Evidence Results Review.",
    "Predictive Usefulness Reassessment and Acceptance Readiness Review.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "feature_generation_execution_using_redesigned_labels",
    "feature_generation_results_review_using_redesigned_labels",
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution_if_approved",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "approval_does_not_generate_features_now",
    "approval_does_not_execute_predictive_evidence",
    "approval_does_not_train_models",
    "approval_does_not_recompute_metrics",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "preserve_meta_record_limitation",
    "no_predictive_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]


class FeatureGenerationApprovalRedesignedLabelsError(ValueError):
    """Raised when approval evidence or authority boundaries are invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureGenerationApprovalRedesignedLabelsError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise FeatureGenerationApprovalRedesignedLabelsError(
            f"{field} must be true"
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


def build_feature_generation_approval_using_redesigned_labels_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_feature_generation_candidate_review_digest: str,
    operator_confirms_feature_generation_candidate_digest: str,
    operator_confirms_feature_predictive_evidence_planning_approval_digest: str,
    operator_confirms_redesigned_label_results_review_digest: str,
    operator_confirms_redesigned_label_execution_digest: str,
    operator_confirms_redesigned_label_approval_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_label_values_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_feature_generation_approval_scope_only: bool,
    operator_confirms_feature_generation_authorized: bool,
    operator_confirms_ready_for_feature_generation_execution_using_redesigned_labels: bool,
    operator_confirms_no_feature_generation_performed: bool,
    operator_confirms_no_feature_values_created: bool,
    operator_confirms_no_predictive_evidence_execution_candidate: bool,
    operator_confirms_no_predictive_evidence_execution: bool,
    operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_FEATURE_GENERATION_USING_REDESIGNED_LABELS,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for exact validation."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_V1
        )
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_feature_generation_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_feature_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_feature_predictive_evidence_planning_approval_digest": EXPECTED_PLANNING_APPROVAL_DIGEST,
        "operator_confirms_redesigned_label_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "operator_confirms_redesigned_label_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "operator_confirms_redesigned_label_approval_digest": EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
        "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        "operator_confirms_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "operator_attestation missing"
        )
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_FEATURE_GENERATION_USING_REDESIGNED_LABELS,
        "operator_attestation_phrase": REQUIRED_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        **_expected_digest_confirmations(),
    }
    for field, expected_value in expected.items():
        _expect(attestation.get(field), expected_value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise FeatureGenerationApprovalRedesignedLabelsError(
                f"{field} required"
            )


def _source_review(source: dict[str, Any] | None) -> dict[str, Any]:
    package = (
        review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    try:
        review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(
            package
        )
    except review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError as exc:
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "source feature generation candidate review is invalid"
        ) from exc
    _expect(
        package.get(
            "feature_generation_candidate_using_redesigned_labels_review_package_digest"
        ),
        EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "source candidate review digest",
    )
    _expect(
        package.get("review_status"),
        review_service.FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY,
        "source candidate review status",
    )
    _expect(package.get("review_summary", {}).get("total_checks"), 55, "source review checklist total")
    _expect(package.get("review_summary", {}).get("passed_checks"), 55, "source review checklist passed")
    _expect(package.get("review_summary", {}).get("failed_checks"), 0, "source review checklist failed")
    _expect(package.get("review_summary", {}).get("blocker_count"), 0, "source review blocker count")
    return package


def _approved_source_inputs(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_input_id": row["source_input_id"],
            "approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY,
            "generation_status": NOT_REGENERATED,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_source_inputs"]
    ]


def _approved_feature_families(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "feature_family_id": row["feature_family_id"],
            "approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY,
            "feature_generation_authorized": True,
            "feature_generation_performed": False,
            "feature_values_created": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_feature_families"]
    ]


def _approved_feature_groups(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "feature_family_id": family["feature_family_id"],
            "feature_group_id": group["feature_group_id"],
            "approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY,
            "feature_generation_authorized": True,
            "feature_generation_performed": False,
            "feature_values_created": False,
            "leakage_sensitive": group["leakage_sensitive"],
            "research_only": True,
            "non_actionable": True,
        }
        for family in source["reviewed_planned_feature_families"]
        for group in family["planned_feature_groups"]
    ]


def _approved_schema_contract(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "feature_schema_contract_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY,
        "approved_schema_fields": deepcopy(
            source["reviewed_feature_schema_contract"]["planned_schema_fields"]
        ),
        "feature_values_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _approved_alignment_controls(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "control_id": row["control_id"],
            "approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY,
            "execution_status": NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_feature_label_alignment_controls"]
    ]


def _approved_quality_checks(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "quality_check_id": row["planned_check_id"],
            "approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY,
            "planned_check_status": NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_quality_checks"]
    ]


def per_ticker_feature_generation_approval_digest_v1(entry: dict[str, Any]) -> str:
    """Return the semantic digest for one ticker's feature approval."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_feature_generation_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approvals(source: dict[str, Any]) -> list[dict[str, Any]]:
    approvals: list[dict[str, Any]] = []
    for row in source["per_ticker_candidate_review_entries"]:
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row["meta_reduced_record_count_flag"],
            "redesigned_label_generation_results_status": row[
                "redesigned_label_generation_results_status"
            ],
            "feature_generation_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "feature_generation_approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY,
            "feature_generation_authorized": True,
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
            "source_feature_generation_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
            "source_feature_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        }
        if row["ticker"] == "META":
            entry["planning_note"] = (
                "PRESERVE_META_LIMITATION_IN_FEATURE_GENERATION_APPROVAL"
            )
        entry["per_ticker_feature_generation_approval_digest"] = (
            per_ticker_feature_generation_approval_digest_v1(entry)
        )
        approvals.append(entry)
    return approvals


def _base_approval(
    source: dict[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_V1,
        "approval_status": FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS,
        "approval_scope": FEATURE_GENERATION_APPROVAL_ONLY,
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
        "operator_attestation": deepcopy(dict(attestation)),
        "feature_generation_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": EXPECTED_PLANNING_APPROVAL_DIGEST,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": EXPECTED_PLANNING_CANDIDATE_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_predictive_evidence_planning_approved": True,
        "feature_predictive_evidence_planning_approval_created": True,
        "ready_for_feature_generation_candidate_using_redesigned_labels": True,
        "feature_generation_candidate_created": True,
        "feature_generation_candidate_using_redesigned_labels_created": True,
        "feature_generation_candidate_using_redesigned_labels_ready_for_operator_review": True,
        "feature_generation_candidate_using_redesigned_labels_review_created": True,
        "feature_generation_approved": True,
        "feature_generation_approval_created": True,
        "feature_generation_authorized": True,
        "redesigned_feature_generation_authorized": True,
        "ready_for_feature_generation_execution_using_redesigned_labels": True,
        "feature_generation_performed": False,
        "redesigned_feature_generation_performed": False,
        "feature_values_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": False,
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
        "feature_generation_execution_created": False,
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
        "feature_generation_objective": FEATURE_GENERATION_OBJECTIVE,
        "feature_generation_scope": FEATURE_GENERATION_APPROVAL_ONLY,
        "feature_generation_mode": FEATURE_GENERATION_MODE,
        "feature_generation_authority_status": FEATURE_GENERATION_AUTHORITY_STATUS,
        "approved_source_inputs": _approved_source_inputs(source),
        "approved_feature_families": _approved_feature_families(source),
        "approved_feature_groups": _approved_feature_groups(source),
        "approved_feature_schema_contract": _approved_schema_contract(source),
        "approved_feature_label_alignment_controls": _approved_alignment_controls(source),
        "approved_feature_quality_checks": _approved_quality_checks(source),
        "per_ticker_approval_entries": _per_ticker_approvals(source),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


CHECK_FIELD_SPECS = [
    ("feature_generation_candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_DIGEST, "feature_generation_candidate_using_redesigned_labels_review_package_digest"),
    ("feature_generation_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "feature_generation_candidate_using_redesigned_labels_digest"),
    ("feature_predictive_evidence_planning_approval_digest_bound", EXPECTED_PLANNING_APPROVAL_DIGEST, "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"),
    ("redesigned_label_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, "redesigned_label_generation_results_review_package_digest"),
    ("redesigned_label_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "redesigned_label_generation_execution_digest"),
    ("redesigned_label_approval_digest_bound", EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST, "redesigned_label_generation_approval_digest"),
    ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, "label_values_digest"),
    ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, "research_registry_approval_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("target_universe_matches_review_universe", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("operator_decision_matches", OPERATOR_DECISION_APPROVE_FEATURE_GENERATION_USING_REDESIGNED_LABELS, "operator_decision"),
    ("operator_attestation_phrase_matches", REQUIRED_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE, "operator_attestation_phrase"),
    ("operator_confirms_all_required_digests", True, "operator_confirms_all_required_digests"),
    ("approval_scope_feature_generation_only", FEATURE_GENERATION_APPROVAL_ONLY, "approval_scope"),
    ("feature_generation_approved_true", True, "feature_generation_approved"),
    ("feature_generation_approval_created_true", True, "feature_generation_approval_created"),
    ("feature_generation_authorized_true", True, "feature_generation_authorized"),
    ("redesigned_feature_generation_authorized_true", True, "redesigned_feature_generation_authorized"),
    ("ready_for_feature_generation_execution_using_redesigned_labels_true", True, "ready_for_feature_generation_execution_using_redesigned_labels"),
    ("feature_generation_performed_false", False, "feature_generation_performed"),
    ("redesigned_feature_generation_performed_false", False, "redesigned_feature_generation_performed"),
    ("feature_values_created_false", False, "feature_values_created"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
    ("additional_predictive_evidence_execution_authorized_false", False, "additional_predictive_evidence_execution_authorized"),
    ("additional_predictive_evidence_executed_false", False, "additional_predictive_evidence_executed"),
    ("metric_recomputation_false", False, "metric_recomputation_performed"),
    ("model_training_false", False, "model_training_performed"),
    ("approved_source_inputs_10", review_service.candidate_service.SOURCE_INPUT_IDS, "approved_source_input_ids"),
    ("approved_feature_families_10", review_service.candidate_service.PLANNED_FEATURE_FAMILY_IDS, "approved_feature_family_ids"),
    ("approved_feature_groups_17", review_service.candidate_service.PLANNED_FEATURE_GROUP_IDS, "approved_feature_group_ids"),
    ("approved_schema_contract_16", review_service.candidate_service.FEATURE_SCHEMA_FIELDS, "approved_schema_fields"),
    ("approved_alignment_controls_10", review_service.candidate_service.ALIGNMENT_CONTROL_IDS, "approved_alignment_control_ids"),
    ("approved_quality_checks_10", review_service.candidate_service.PLANNED_QUALITY_CHECK_IDS, "approved_quality_check_ids"),
    ("per_ticker_approval_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_approval_digests_present", True, "per_ticker_approval_digests_valid"),
    ("next_chain_defined", NEXT_CHAIN, "next_chain"),
    ("next_gates_defined", NEXT_GATES, "next_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("paper_trading_not_authorized", NOT_AUTHORIZED, "paper_trading"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("provider_requests_made_false", False, "provider_requests_made"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed"),
    ("dataset_regeneration_false", False, "dataset_regeneration_performed"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("feature_generation_false", False, "feature_generation_performed"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("no_feature_generation_execution_created", False, "feature_generation_execution_created"),
    ("no_additional_predictive_evidence_execution_candidate_created", False, "additional_predictive_evidence_execution_candidate_created"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [spec[0] for spec in CHECK_FIELD_SPECS]


def _derived_check_fields(approval: dict[str, Any]) -> dict[str, Any]:
    attestation = approval.get("operator_attestation", {})
    inputs = approval.get("approved_source_inputs", [])
    families = approval.get("approved_feature_families", [])
    groups = approval.get("approved_feature_groups", [])
    schema = approval.get("approved_feature_schema_contract", {})
    controls = approval.get("approved_feature_label_alignment_controls", [])
    quality = approval.get("approved_feature_quality_checks", [])
    entries = approval.get("per_ticker_approval_entries", [])
    return {
        **approval,
        "operator_decision": attestation.get("operator_decision") if isinstance(attestation, dict) else None,
        "operator_attestation_phrase": attestation.get("operator_attestation_phrase") if isinstance(attestation, dict) else None,
        "operator_confirms_all_required_digests": isinstance(attestation, dict) and all(attestation.get(field) == expected for field, expected in _expected_digest_confirmations().items()),
        "approved_source_input_ids": [row.get("source_input_id") for row in inputs] if isinstance(inputs, list) else [],
        "approved_feature_family_ids": [row.get("feature_family_id") for row in families] if isinstance(families, list) else [],
        "approved_feature_group_ids": [row.get("feature_group_id") for row in groups] if isinstance(groups, list) else [],
        "approved_schema_fields": schema.get("approved_schema_fields", []) if isinstance(schema, dict) else [],
        "approved_alignment_control_ids": [row.get("control_id") for row in controls] if isinstance(controls, list) else [],
        "approved_quality_check_ids": [row.get("quality_check_id") for row in quality] if isinstance(quality, list) else [],
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_approval_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(isinstance(row.get("per_ticker_feature_generation_approval_digest"), str) and len(row["per_ticker_feature_generation_approval_digest"]) == 64 and row["per_ticker_feature_generation_approval_digest"] == per_ticker_feature_generation_approval_digest_v1(row) for row in entries),
    }


def _checklist(approval: dict[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_check_fields(approval)
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
        "feature_generation_approved_by_operator": not failed,
        "approval_scope": FEATURE_GENERATION_APPROVAL_ONLY,
        "feature_generation_authorized": not failed,
        "ready_for_feature_generation_execution_using_redesigned_labels": not failed,
        "feature_generation_performed": False,
        "feature_values_created": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(approval: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approval)
    payload.pop("feature_generation_approval_using_redesigned_labels_digest", None)
    return payload


def feature_generation_approval_using_redesigned_labels_digest_v1(
    approval: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval."""
    return semantic_digest(_digest_payload(approval))


def build_feature_generation_approved_using_redesigned_labels_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    """Approve future feature generation only after exact operator attestation."""
    _validate_attestation(operator_attestation)
    source = _source_review(candidate_review_package)
    approval = _base_approval(source, operator_attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval["feature_generation_approval_using_redesigned_labels_digest"] = (
        feature_generation_approval_using_redesigned_labels_digest_v1(approval)
    )
    validate_feature_generation_approved_using_redesigned_labels_v1(approval)
    return approval


def _reject_forbidden_values(value: Any, *, path: str = "approval") -> None:
    forbidden_artifacts = {
        "FEATURE_GENERATION_EXECUTED",
        "FEATURE_VALUES_CREATED",
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
        "feature_generation_performed",
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
        "feature_generation_execution_created",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            if key in forbidden_true and item is True:
                raise FeatureGenerationApprovalRedesignedLabelsError(
                    f"{path}.{key} must remain false"
                )
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        if value in forbidden_artifacts:
            raise FeatureGenerationApprovalRedesignedLabelsError(
                f"{path} contains forbidden downstream artifact"
            )
        if value == "accepted":
            raise FeatureGenerationApprovalRedesignedLabelsError(
                f"{path} must not accept predictive usefulness or profitability"
            )
        if value == "AUTHORIZED":
            raise FeatureGenerationApprovalRedesignedLabelsError(
                f"{path} must not grant runtime or trading authority"
            )


def validate_feature_generation_approved_using_redesigned_labels_v1(
    approval: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is exactly the attested approval-only scope."""
    if not isinstance(approval, dict):
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "approval must be a JSON object"
        )
    _expect(approval.get("artifact_kind"), ARTIFACT_KIND_FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS, "artifact_kind")
    _expect(approval.get("schema_version"), SCHEMA_VERSION_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_V1, "schema_version")
    _expect(approval.get("approval_status"), FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS, "approval_status")
    _expect(approval.get("approval_scope"), FEATURE_GENERATION_APPROVAL_ONLY, "approval_scope")
    _validate_attestation(approval.get("operator_attestation", {}))
    _reject_forbidden_values(approval)
    source = _source_review(None)
    expected = _base_approval(source, approval["operator_attestation"])
    for field, expected_value in expected.items():
        _expect(approval.get(field), expected_value, field)
    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list):
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "approval_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "approval_checklist check ids")
    _expect(checklist, _checklist(approval), "approval_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "approval_checklist must pass"
        )
    _expect(approval.get("approval_summary"), _summary(checklist), "approval_summary")
    digest = approval.get("feature_generation_approval_using_redesigned_labels_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "missing approval digest"
        )
    _expect(digest, feature_generation_approval_using_redesigned_labels_digest_v1(approval), "approval digest")
    return {
        "status": FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS,
        "artifact_kind": approval["artifact_kind"],
        "approval_scope": approval["approval_scope"],
        "feature_generation_approval_using_redesigned_labels_digest": digest,
        "per_ticker_approval_entry_count": len(approval["per_ticker_approval_entries"]),
        "blocker_count": approval["approval_summary"]["blocker_count"],
        "feature_generation_authorized": True,
        "ready_for_feature_generation_execution_using_redesigned_labels": True,
        "feature_generation_performed": False,
        "feature_values_created": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_feature_generation_approved_using_redesigned_labels_markdown_v1(
    approval: dict,
) -> str:
    """Render the approval without implying feature execution or downstream authority."""
    validation = validate_feature_generation_approved_using_redesigned_labels_v1(
        approval
    )
    attestation = approval["operator_attestation"]
    summary = approval["approval_summary"]
    lines = [
        "# MarketFlow Feature Generation Approval Using Redesigned Labels Status",
        "",
        "## Title",
        "- Feature Generation Approval Using Redesigned Labels v1.",
        "",
        "## Feature Generation Approval Using Redesigned Labels",
        f"- Artifact/status/scope/digest: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}` / `{validation['feature_generation_approval_using_redesigned_labels_digest']}`.",
        "",
        "## Operator Attestation",
        f"- Operator reference/timestamp: `{attestation['operator_reference']}` / `{attestation['operator_attestation_timestamp_utc']}`.",
        f"- Decision: `{attestation['operator_decision']}`.",
        f"- Exact phrase: `{attestation['operator_attestation_phrase']}`.",
        "",
        "## Bound Evidence",
        f"- Candidate review/candidate: `{approval['feature_generation_candidate_using_redesigned_labels_review_package_digest']}` / `{approval['feature_generation_candidate_using_redesigned_labels_digest']}`.",
        f"- Planning approval/results review/label values: `{approval['feature_predictive_evidence_planning_approval_using_redesigned_labels_digest']}` / `{approval['redesigned_label_generation_results_review_package_digest']}` / `{approval['label_values_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- `{approval['dataset_name']}` contains `{approval['total_canonical_record_count']}` frozen records for the ordered 12-ticker universe; META remains `{approval['meta_record_count']}`.",
        "",
        "## Approved Source Inputs",
    ]
    lines.extend(f"- `{row['source_input_id']}`: `{row['approval_status']}`." for row in approval["approved_source_inputs"])
    lines.extend(["", "## Approved Feature Families"])
    lines.extend(f"- `{row['feature_family_id']}`: `{row['approval_status']}`." for row in approval["approved_feature_families"])
    lines.extend(["", "## Approved Feature Groups"])
    lines.extend(f"- `{row['feature_group_id']}`: `{row['approval_status']}`." for row in approval["approved_feature_groups"])
    lines.extend(["", "## Approved Feature Schema Contract", f"- `{approval['approved_feature_schema_contract']['feature_schema_contract_status']}` with all 16 fields bound and no feature values created."])
    lines.extend(["", "## Approved Feature / Label Alignment Controls"])
    lines.extend(f"- `{row['control_id']}`: `{row['execution_status']}`." for row in approval["approved_feature_label_alignment_controls"])
    lines.extend(["", "## Approved Quality Checks"])
    lines.extend(f"- `{row['quality_check_id']}`: `{row['planned_check_status']}`." for row in approval["approved_feature_quality_checks"])
    lines.extend(["", "## Per-Ticker Approval Entries", "- Twelve deterministic approval entries authorize future feature generation only; META remains 913 records and no feature values exist.", "", "## Next Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(approval["next_chain"], 1))
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in approval["next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in approval["risk_controls"])
    lines.extend([
        "",
        "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "",
        "## Guardrails",
        "- This artifact authorizes only future research-only feature generation. It does not create feature values or execute predictive evidence, metrics, training, scoring, recommendations, acceptance, profitability, runtime, strategy, paper trading, or broker actions.",
        "- Feature-generation execution remains a separate future task.",
        "",
    ])
    return "\n".join(lines)


def write_feature_generation_approved_using_redesigned_labels_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical approval without overwriting existing evidence."""
    approval = build_feature_generation_approved_using_redesigned_labels_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    output_name = filename or "feature_generation_approval_using_redesigned_labels_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "approval filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(approval)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise FeatureGenerationApprovalRedesignedLabelsError(
            "approval output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "feature_generation_approval_using_redesigned_labels_digest": approval[
            "feature_generation_approval_using_redesigned_labels_digest"
        ],
    }
