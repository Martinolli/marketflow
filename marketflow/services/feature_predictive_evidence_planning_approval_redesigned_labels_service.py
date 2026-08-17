"""Offline operator approval for feature/predictive planning using redesigned labels."""

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
    feature_predictive_evidence_planning_candidate_redesigned_labels_operator_review_service as review_service,
)


ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_V1 = (
    "feature_predictive_evidence_planning_approval_using_redesigned_labels_v1"
)
FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS"
)
FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY = (
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS = (
    "APPROVE_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS"
)
OPERATOR_ATTESTATION_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_V1 = (
    "feature_predictive_evidence_planning_approval_using_redesigned_labels_operator_attestation_v1"
)
REQUIRED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE = (
    "APPROVE FEATURE PREDICTIVE EVIDENCE PLANNING USING REDESIGNED LABELS "
    "MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY"
)

DEFAULT_BRANCH = (
    "feature/feature-predictive-evidence-planning-approval-redesigned-labels-v1"
)
DEFAULT_BASE_COMMIT = "30421e0cd201393e46113de1a8c8f331f7b37e70"
EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "82495e036e79777e6cb69935f98051e76c7b7296254cb82990e34217a82a67e8"
)
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = review_service.candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = review_service.candidate_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_APPROVAL_DIGEST = review_service.candidate_service.EXPECTED_APPROVAL_DIGEST
EXPECTED_REDESIGNED_LABEL_CANDIDATE_REVIEW_DIGEST = (
    review_service.candidate_service.EXPECTED_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_REDESIGNED_LABEL_CANDIDATE_DIGEST = (
    review_service.candidate_service.EXPECTED_CANDIDATE_DIGEST
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
)
EXPECTED_RECORDS_DIGEST = review_service.candidate_service.EXPECTED_RECORDS_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = review_service.candidate_service.EXPECTED_LABEL_VALUES_DIGEST

TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

APPROVED_FOR_FUTURE_PLANNING_ONLY = "APPROVED_FOR_FUTURE_PLANNING_ONLY"
APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY = (
    "APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY"
)
NOT_REGENERATED = "NOT_REGENERATED"

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_redesigned_label_profile",
    "operator_confirms_feature_predictive_evidence_planning_approval_scope_only",
    "operator_confirms_feature_predictive_evidence_planning_approved",
    "operator_confirms_ready_for_feature_generation_candidate_using_redesigned_labels",
    "operator_confirms_not_ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "operator_confirms_no_feature_generation_candidate_created",
    "operator_confirms_no_feature_generation_authorization",
    "operator_confirms_no_feature_generation",
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
    "Feature Generation Candidate Using Redesigned Labels v1.",
    "Feature Generation Candidate Operator Review Package v1.",
    "Feature Generation Approval v1, if selected.",
    "Feature Generation Execution v1.",
    "Feature Generation Results Review v1.",
    "Additional Predictive Evidence Execution Candidate Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Approval and Execution, if separately approved.",
    "Additional Predictive Evidence Results Review.",
    "Predictive Usefulness Reassessment and Acceptance Readiness Review.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "feature_generation_candidate_using_redesigned_labels",
    "feature_generation_candidate_operator_review",
    "feature_generation_approval_if_required",
    "feature_generation_execution_if_approved",
    "feature_generation_results_review",
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
    "approval_does_not_create_feature_generation_candidate",
    "approval_does_not_generate_features",
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

REQUIRED_CHECK_IDS = [
    "planning_candidate_review_digest_bound",
    "planning_candidate_digest_bound",
    "redesigned_label_results_review_digest_bound",
    "redesigned_label_execution_digest_bound",
    "redesigned_label_approval_digest_bound",
    "label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "target_universe_matches_review_universe",
    "records_digest_preserved",
    "meta_913_preserved",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_required_digests",
    "operator_confirms_redesigned_label_profile",
    "approval_scope_feature_predictive_evidence_planning_only",
    "feature_predictive_evidence_planning_approved_true",
    "feature_predictive_evidence_planning_approval_created_true",
    "ready_for_feature_generation_candidate_using_redesigned_labels_true",
    "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels_false",
    "feature_generation_candidate_created_false",
    "feature_generation_authorized_false",
    "feature_generation_performed_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "metric_recomputation_false",
    "model_training_false",
    "approved_source_inputs_9",
    "approved_feature_families_10",
    "approved_predictive_components_10",
    "approved_model_baseline_families_9",
    "per_ticker_approval_entries_12",
    "per_ticker_approval_digests_present",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "paper_trading_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "redesigned_label_regeneration_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "no_feature_generation_candidate_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "no_tracked_marketflow_files",
]


class FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(ValueError):
    """Raised when the planning approval violates its frozen contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            f"{field} must be true"
        )


def build_feature_predictive_evidence_planning_approval_using_redesigned_labels_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_feature_predictive_evidence_planning_candidate_review_digest: str,
    operator_confirms_feature_predictive_evidence_planning_candidate_digest: str,
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
    operator_confirms_redesigned_label_profile: bool,
    operator_confirms_feature_predictive_evidence_planning_approval_scope_only: bool,
    operator_confirms_feature_predictive_evidence_planning_approved: bool,
    operator_confirms_ready_for_feature_generation_candidate_using_redesigned_labels: bool,
    operator_confirms_not_ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels: bool,
    operator_confirms_no_feature_generation_candidate_created: bool,
    operator_confirms_no_feature_generation_authorization: bool,
    operator_confirms_no_feature_generation: bool,
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
    operator_decision: str = OPERATOR_DECISION_APPROVE_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS,
) -> dict[str, Any]:
    """Build a non-secret operator attestation; approval validates every field."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_V1
        )
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_feature_predictive_evidence_planning_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_feature_predictive_evidence_planning_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_redesigned_label_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "operator_confirms_redesigned_label_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "operator_confirms_redesigned_label_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        "operator_confirms_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "operator_attestation missing"
        )
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS,
        "operator_attestation_phrase": REQUIRED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
                f"{field} required"
            )


def _source_review(source: dict[str, Any] | None) -> dict[str, Any]:
    package = (
        review_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    try:
        validation = review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(
            package
        )
    except review_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError as exc:
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "source planning candidate review is invalid"
        ) from exc
    _expect(
        package.get(
            "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"
        ),
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source planning candidate review digest",
    )
    _expect(
        package.get("review_status"),
        review_service.FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY,
        "source planning candidate review status",
    )
    _expect(package.get("review_summary", {}).get("blocker_count"), 0, "source blockers")
    _expect(
        validation.get(
            "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"
        ),
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "validated source planning candidate review digest",
    )
    return package


def _approved_source_inputs(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_input_id": row["source_input_id"],
            "approval_status": APPROVED_FOR_FUTURE_PLANNING_ONLY,
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
            "approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_feature_families"]
    ]


def _approved_predictive_components(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "component_id": row["component_id"],
            "approval_status": APPROVED_FOR_FUTURE_PLANNING_ONLY,
            "execution_authorized": False,
            "execution_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_predictive_evidence_components"]
    ]


def _approved_model_baseline_families(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "model_or_baseline_family_id": row["model_or_baseline_family_id"],
            "approval_status": APPROVED_FOR_FUTURE_PLANNING_ONLY,
            "training_authorized": False,
            "training_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_model_baseline_families"]
    ]


def per_ticker_feature_predictive_evidence_planning_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one ticker's planning approval."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_feature_predictive_evidence_planning_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approvals(source: dict[str, Any]) -> list[dict[str, Any]]:
    approvals: list[dict[str, Any]] = []
    for row in source["per_ticker_candidate_review_entries"]:
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row["meta_reduced_record_count_flag"],
            "redesigned_label_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "feature_predictive_evidence_planning_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "feature_predictive_evidence_planning_approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY,
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
            "source_feature_predictive_evidence_planning_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_feature_predictive_evidence_planning_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        }
        if row["ticker"] == "META":
            entry["planning_note"] = (
                "PRESERVE_META_LIMITATION_IN_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING"
            )
        entry["per_ticker_feature_predictive_evidence_planning_approval_digest"] = (
            per_ticker_feature_predictive_evidence_planning_approval_digest_v1(entry)
        )
        approvals.append(entry)
    return approvals


def _base_artifact(
    source: dict[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_V1,
        "approval_status": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS,
        "approval_scope": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY,
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
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "redesigned_label_generation_candidate_review_package_digest": EXPECTED_REDESIGNED_LABEL_CANDIDATE_REVIEW_DIGEST,
        "redesigned_label_generation_candidate_digest": EXPECTED_REDESIGNED_LABEL_CANDIDATE_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
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
        "feature_predictive_evidence_planning_approved": True,
        "feature_predictive_evidence_planning_approval_created": True,
        "ready_for_feature_generation_candidate_using_redesigned_labels": True,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": False,
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
        "redesigned_label_output_count": source["redesigned_label_output_count"],
        "redesigned_label_output_status": source["redesigned_label_output_status"],
        "label_family_count": source["label_family_count"],
        "threshold_strategy_count": source["threshold_strategy_count"],
        "horizon_strategy_count": source["horizon_strategy_count"],
        "label_value_row_count": source["label_value_row_count"],
        "label_family_coverage_entries": source["label_family_coverage_entries"],
        "available_label_value_count": source["available_label_value_count"],
        "unavailable_label_value_count": source["unavailable_label_value_count"],
        "feature_predictive_evidence_planning_objective": "APPROVE_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS",
        "feature_predictive_evidence_planning_scope": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY,
        "feature_predictive_evidence_planning_mode": "APPROVED_NOT_EXECUTED",
        "feature_predictive_evidence_planning_authority_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY,
        "approved_source_inputs": _approved_source_inputs(source),
        "approved_planned_feature_families": _approved_feature_families(source),
        "approved_planned_predictive_evidence_components": _approved_predictive_components(source),
        "approved_planned_model_baseline_families": _approved_model_baseline_families(source),
        "per_ticker_feature_predictive_evidence_planning_approvals": _per_ticker_approvals(source),
        "next_chain": deepcopy(NEXT_CHAIN),
        "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": "check passed" if status == PASS else "approval boundary mismatch",
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return (
        isinstance(entries, list)
        and len(entries) == 12
        and all(
            isinstance(row.get("per_ticker_feature_predictive_evidence_planning_approval_digest"), str)
            and len(row["per_ticker_feature_predictive_evidence_planning_approval_digest"]) == 64
            and row["per_ticker_feature_predictive_evidence_planning_approval_digest"]
            == per_ticker_feature_predictive_evidence_planning_approval_digest_v1(row)
            for row in entries
        )
    )


def _checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    operator = artifact["operator_attestation"]
    entries = artifact["per_ticker_feature_predictive_evidence_planning_approvals"]
    values: dict[str, tuple[Any, Any]] = {
        "planning_candidate_review_digest_bound": (EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest")),
        "planning_candidate_digest_bound": (EXPECTED_CANDIDATE_DIGEST, artifact.get("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest")),
        "redesigned_label_results_review_digest_bound": (EXPECTED_RESULTS_REVIEW_DIGEST, artifact.get("redesigned_label_generation_results_review_package_digest")),
        "redesigned_label_execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, artifact.get("redesigned_label_generation_execution_digest")),
        "redesigned_label_approval_digest_bound": (EXPECTED_APPROVAL_DIGEST, artifact.get("redesigned_label_generation_approval_digest")),
        "label_values_digest_bound": (EXPECTED_LABEL_VALUES_DIGEST, artifact.get("label_values_digest")),
        "research_registry_digest_bound": (EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, artifact.get("research_registry_approval_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, artifact.get("records_digest")),
        "target_universe_12_preserved": (12, artifact.get("target_universe_count")),
        "target_universe_matches_review_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "records_digest_preserved": (EXPECTED_RECORDS_DIGEST, artifact.get("records_digest")),
        "meta_913_preserved": (913, artifact.get("meta_record_count")),
        "operator_decision_matches": (OPERATOR_DECISION_APPROVE_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_USING_REDESIGNED_LABELS, operator.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        "operator_confirms_all_required_digests": (True, all(operator.get(field) == expected for field, expected in _expected_digest_confirmations().items())),
        "operator_confirms_redesigned_label_profile": (True, operator.get("operator_confirms_redesigned_label_profile")),
        "approval_scope_feature_predictive_evidence_planning_only": (FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY, artifact.get("approval_scope")),
        "feature_predictive_evidence_planning_approved_true": (True, artifact.get("feature_predictive_evidence_planning_approved")),
        "feature_predictive_evidence_planning_approval_created_true": (True, artifact.get("feature_predictive_evidence_planning_approval_created")),
        "ready_for_feature_generation_candidate_using_redesigned_labels_true": (True, artifact.get("ready_for_feature_generation_candidate_using_redesigned_labels")),
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels_false": (False, artifact.get("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels")),
        "feature_generation_candidate_created_false": (False, artifact.get("feature_generation_candidate_created")),
        "feature_generation_authorized_false": (False, artifact.get("feature_generation_authorized")),
        "feature_generation_performed_false": (False, artifact.get("feature_generation_performed")),
        "additional_predictive_evidence_execution_candidate_created_false": (False, artifact.get("additional_predictive_evidence_execution_candidate_created")),
        "additional_predictive_evidence_execution_authorized_false": (False, artifact.get("additional_predictive_evidence_execution_authorized")),
        "additional_predictive_evidence_executed_false": (False, artifact.get("additional_predictive_evidence_executed")),
        "metric_recomputation_false": (False, artifact.get("metric_recomputation_performed")),
        "model_training_false": (False, artifact.get("model_training_performed")),
        "approved_source_inputs_9": (9, len(artifact.get("approved_source_inputs", []))),
        "approved_feature_families_10": (10, len(artifact.get("approved_planned_feature_families", []))),
        "approved_predictive_components_10": (10, len(artifact.get("approved_planned_predictive_evidence_components", []))),
        "approved_model_baseline_families_9": (9, len(artifact.get("approved_planned_model_baseline_families", []))),
        "per_ticker_approval_entries_12": (12, len(entries)),
        "per_ticker_approval_digests_present": (True, _per_ticker_digests_valid(entries)),
        "next_chain_defined": (NEXT_CHAIN, artifact.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, artifact.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, artifact.get("risk_controls")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        "trade_recommendations_false": (False, artifact.get("trade_recommendations_generated")),
        "provider_requests_made_false": (False, artifact.get("provider_requests_made")),
        "market_data_acquisition_false": (False, artifact.get("market_data_acquisition_performed")),
        "dataset_regeneration_false": (False, artifact.get("dataset_regeneration_performed")),
        "redesigned_label_regeneration_false": (False, artifact.get("redesigned_label_regeneration_performed")),
        "raw_provider_payloads_not_committed": (False, artifact.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, artifact.get("api_keys_stored_or_printed")),
        "no_feature_generation_candidate_created": (False, artifact.get("feature_generation_candidate_created")),
        "no_additional_predictive_evidence_execution_candidate_created": (False, artifact.get("additional_predictive_evidence_execution_candidate_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, artifact.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, artifact.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, artifact.get("runtime_migration_approval_created")),
        "no_tracked_marketflow_files": (True, artifact.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    approved = not failed
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "feature_predictive_evidence_planning_approved_by_operator": approved,
        "approval_scope": FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_ONLY,
        "feature_predictive_evidence_planning_approved": approved,
        "ready_for_feature_generation_candidate_using_redesigned_labels": approved,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": False,
        "feature_generation_candidate_created": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def feature_predictive_evidence_planning_approval_using_redesigned_labels_digest_v1(
    approval: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    payload = deepcopy(approval)
    payload.pop(
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest",
        None,
    )
    return semantic_digest(payload)


def build_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    """Build the attestation-gated planning approval without provider access."""
    source = _source_review(candidate_review_package)
    _validate_attestation(operator_attestation)
    approval = _base_artifact(source, operator_attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval[
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"
    ] = feature_predictive_evidence_planning_approval_using_redesigned_labels_digest_v1(
        approval
    )
    validate_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
        approval
    )
    return approval


def _reject_forbidden_values(value: Any, *, path: str = "approval") -> None:
    forbidden_artifacts = {
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
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "canonical_dataset_regenerated",
        "redesigned_label_regeneration_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
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
        "feature_generation_authorized",
        "predictive_evidence_execution_authorized",
        "predictive_evidence_execution_performed",
        "execution_authorized",
        "execution_performed",
        "training_authorized",
        "training_performed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
                    f"{current} contains forbidden downstream artifact"
                )
            if key in forbidden_true and item is True:
                raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _validate_per_ticker(approval: dict[str, Any]) -> None:
    entries = approval.get("per_ticker_feature_predictive_evidence_planning_approvals")
    if not isinstance(entries, list) or len(entries) != 12:
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "per-ticker planning approvals mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": 913 if ticker == "META" else 1003,
            "meta_reduced_record_count_flag": ticker == "META",
            "redesigned_label_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "feature_predictive_evidence_planning_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "feature_predictive_evidence_planning_approval_status": APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY,
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
            "source_feature_predictive_evidence_planning_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_feature_predictive_evidence_planning_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"per_ticker.{ticker}.{field}")
        if ticker == "META":
            _expect(
                row.get("planning_note"),
                "PRESERVE_META_LIMITATION_IN_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING",
                "per_ticker.META.planning_note",
            )
        elif "planning_note" in row:
            raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
                f"per_ticker.{ticker}.planning_note must be absent"
            )
        digest = row.get(
            "per_ticker_feature_predictive_evidence_planning_approval_digest"
        )
        if not isinstance(digest, str) or len(digest) != 64:
            raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
                f"per_ticker.{ticker}.approval digest missing"
            )
        _expect(
            digest,
            per_ticker_feature_predictive_evidence_planning_approval_digest_v1(row),
            f"per_ticker.{ticker}.approval digest",
        )


def validate_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
    approval: dict,
) -> dict[str, Any]:
    """Validate exact planning approval while every execution gate stays closed."""
    if not isinstance(approval, dict):
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "planning approval must be a JSON object"
        )
    _reject_forbidden_values(approval)
    _validate_attestation(approval.get("operator_attestation", {}))
    source = _source_review(None)
    expected_base = _base_artifact(source, approval["operator_attestation"])
    for field, expected in expected_base.items():
        _expect(approval.get(field), expected, field)
    _validate_per_ticker(approval)
    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list):
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "approval_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "approval_checklist check IDs",
    )
    expected_checklist = _checklist(approval)
    _expect(checklist, expected_checklist, "approval_checklist")
    failed = [row for row in expected_checklist if row["status"] != PASS]
    if failed:
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(approval.get("approval_summary"), expected_summary, "approval_summary")
    digest = approval.get(
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "planning approval digest missing"
        )
    _expect(
        digest,
        feature_predictive_evidence_planning_approval_using_redesigned_labels_digest_v1(
            approval
        ),
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest",
    )
    return {
        "status": "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_LABELS_VALID",
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": digest,
        "source_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "per_ticker_approval_count": 12,
        "blocker_count": 0,
        "feature_predictive_evidence_planning_approved": True,
        "ready_for_feature_generation_candidate_using_redesigned_labels": True,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": False,
        "feature_generation_candidate_created": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_feature_predictive_evidence_planning_approved_using_redesigned_labels_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized operator-facing approval summary."""
    validation = validate_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
        approval
    )
    operator = approval["operator_attestation"]
    summary = approval["approval_summary"]
    lines = [
        "# MarketFlow Feature Predictive Evidence Planning Approval Using Redesigned Labels",
        "",
        "## Title",
        "- Feature / Predictive Evidence Planning Approval Using Redesigned Labels v1.",
        "",
        "## Feature / Predictive Evidence Planning Approval Using Redesigned Labels",
        f"- Artifact/status/scope: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}`.",
        f"- Approval digest: `{validation['feature_predictive_evidence_planning_approval_using_redesigned_labels_digest']}`.",
        "",
        "## Operator Attestation",
        f"- Reference/timestamp/version: `{operator['operator_reference']}` / `{operator['operator_attestation_timestamp_utc']}` / `{operator['operator_attestation_version']}`.",
        "- The exact non-secret phrase and every required digest and boundary confirmation passed.",
        "",
        "## Bound Evidence",
        f"- Candidate review/candidate: `{EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST}` / `{EXPECTED_CANDIDATE_DIGEST}`.",
        f"- Results review/execution/label values: `{EXPECTED_RESULTS_REVIEW_DIGEST}` / `{EXPECTED_EXECUTION_DIGEST}` / `{EXPECTED_LABEL_VALUES_DIGEST}`.",
        "",
        "## Dataset and Universe",
        f"- `{approval['dataset_name']}` contains `{approval['total_canonical_record_count']}` records across 12 ordered tickers; META remains `{approval['meta_record_count']}`.",
        "",
        "## Approved Redesigned Label Profile",
        f"- Outputs/families/thresholds/horizons/rows: `{approval['redesigned_label_output_count']}` / `{approval['label_family_count']}` / `{approval['threshold_strategy_count']}` / `{approval['horizon_strategy_count']}` / `{approval['label_value_row_count']}`.",
        "",
        "## Approved Source Inputs",
    ]
    lines.extend(
        f"- `{row['source_input_id']}`: `{row['approval_status']}`."
        for row in approval["approved_source_inputs"]
    )
    lines.extend(["", "## Approved Feature Families"])
    lines.extend(
        f"- `{row['feature_family_id']}`: `{row['approval_status']}`."
        for row in approval["approved_planned_feature_families"]
    )
    lines.extend(["", "## Approved Predictive Evidence Components"])
    lines.extend(
        f"- `{row['component_id']}`: `{row['approval_status']}`."
        for row in approval["approved_planned_predictive_evidence_components"]
    )
    lines.extend(["", "## Approved Model and Baseline Families"])
    lines.extend(
        f"- `{row['model_or_baseline_family_id']}`: `{row['approval_status']}`."
        for row in approval["approved_planned_model_baseline_families"]
    )
    lines.extend(
        [
            "",
            "## Per-Ticker Approval Entries",
            "- Twelve deterministic approvals preserve registry order and META's 913-record limitation; feature generation and predictive execution remain unauthorized.",
            "",
            "## Next Chain",
        ]
    )
    lines.extend(f"{index}. {item}" for index, item in enumerate(NEXT_CHAIN, 1))
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in NEXT_GATES)
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in RISK_CONTROLS)
    lines.extend(
        [
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- This approval authorizes future feature-generation candidate planning only. It creates no feature-generation candidate, feature, metric, model, predictive execution, acceptance, profitability, runtime, recommendation, or trading authority.",
            "- The predictive-evidence execution candidate remains not ready until separately planned feature generation is reviewed.",
            "",
        ]
    )
    return "\n".join(lines)


def write_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical approval JSON once without overwriting."""
    approval = build_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_feature_predictive_evidence_planning_approved_using_redesigned_labels_v1(
        approval
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "feature_predictive_evidence_planning_approved_using_redesigned_labels_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "planning approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise FeaturePredictiveEvidencePlanningApprovalRedesignedLabelsError(
            "planning approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
