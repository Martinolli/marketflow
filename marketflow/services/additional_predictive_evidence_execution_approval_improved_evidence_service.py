"""Offline approval for future predictive-evidence execution using improved evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_improved_evidence_operator_review_service as review_service,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_V1 = (
    "additional_predictive_evidence_execution_approval_using_improved_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE = (
    "APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE"
)
OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_V1 = (
    "additional_predictive_evidence_execution_approval_using_improved_evidence_operator_attestation_v1"
)
REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_ATTESTATION_PHRASE = (
    "APPROVE ADDITIONAL PREDICTIVE EVIDENCE EXECUTION USING IMPROVED EVIDENCE "
    "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS "
    "MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_VALID"
)

DEFAULT_BRANCH = "feature/additional-predictive-evidence-execution-approval-improved-evidence-v1"
DEFAULT_BASE_COMMIT = "63caa1b8208ecbab046bbbe8372d33b8334beec0"
EXPECTED_CANDIDATE_REVIEW_DIGEST = "1db2b5a32e4cbd475330b3558706e8f7319bdf8d29a53c9e8c26bc32cc2b2442"
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
BOUND_DIGESTS = deepcopy(review_service.candidate_service.BOUND_DIGESTS)
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review_service.EXPECTED_RECORD_COUNTS)
SELECTED_DIRECTION = review_service.SELECTED_DIRECTION
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

EXECUTION_OBJECTIVE = (
    "AUTHORIZE_FUTURE_RESEARCH_ONLY_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE"
)
EXECUTION_MODE = AUTHORIZED_NOT_EXECUTED
EXECUTION_AUTHORITY_STATUS = "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_EVIDENCE_EXECUTION"

NEXT_CHAIN = [
    "Optional Additional Predictive Evidence Execution Using Improved Evidence v1, if approved.",
    "Optional Additional Predictive Evidence Results Review Using Improved Evidence v1.",
    "Predictive usefulness reassessment rerun using improved evidence, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun using improved evidence, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "additional_predictive_evidence_execution_using_improved_evidence_if_approved",
    "additional_predictive_evidence_results_review_using_improved_evidence",
    "predictive_usefulness_reassessment_rerun_using_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_using_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_execute_predictive_evidence_now",
    "approval_does_not_generate_labels",
    "approval_does_not_create_new_targets",
    "approval_does_not_authorize_target_definition_change",
    "approval_does_not_generate_features_now",
    "approval_does_not_create_feature_label_matrix_now",
    "approval_does_not_recompute_metrics_now",
    "approval_does_not_train_models_now",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_create_acceptance_candidate",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "do_not_mutate_label_objective_review_outputs",
    "do_not_mutate_label_objective_redesign_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

DIGEST_CONFIRMATIONS = {
    "operator_confirms_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "operator_confirms_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
    "operator_confirms_planning_results_review_digest": BOUND_DIGESTS[
        "improved_evidence_planning_results_review_using_redesigned_evidence_digest"
    ],
    "operator_confirms_planning_execution_digest": BOUND_DIGESTS[
        "improved_evidence_planning_execution_using_redesigned_evidence_digest"
    ],
    "operator_confirms_records_digest": BOUND_DIGESTS["records_digest"],
}
VALUE_CONFIRMATIONS = {
    "operator_confirms_target_universe": TARGET_UNIVERSE,
    "operator_confirms_target_count": 12,
    "operator_confirms_meta_record_count": 913,
    "operator_confirms_non_meta_record_count": 1003,
    "operator_confirms_selected_redesign_direction": SELECTED_DIRECTION,
}
BOOLEAN_CONFIRMATIONS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_execution_authorized",
    "operator_confirms_ready_for_execution",
    "operator_confirms_no_execution_performed",
    "operator_confirms_no_results_created",
    "operator_confirms_no_label_regeneration",
    "operator_confirms_no_new_targets",
    "operator_confirms_no_target_definition_change_authorization",
    "operator_confirms_no_feature_generation",
    "operator_confirms_no_feature_label_matrix_creation",
    "operator_confirms_no_metric_recomputation_in_approval",
    "operator_confirms_no_model_training_in_approval",
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


class AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(ValueError):
    """Raised when approval violates the attested research-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
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


def build_additional_predictive_evidence_execution_approval_using_improved_evidence_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_planning_results_review_digest: str,
    operator_confirms_planning_execution_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_redesign_direction: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_execution_authorized: bool,
    operator_confirms_ready_for_execution: bool,
    operator_confirms_no_execution_performed: bool,
    operator_confirms_no_results_created: bool,
    operator_confirms_no_label_regeneration: bool,
    operator_confirms_no_new_targets: bool,
    operator_confirms_no_target_definition_change_authorization: bool,
    operator_confirms_no_feature_generation: bool,
    operator_confirms_no_feature_label_matrix_creation: bool,
    operator_confirms_no_metric_recomputation_in_approval: bool,
    operator_confirms_no_model_training_in_approval: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_redesign_direction: str = SELECTED_DIRECTION,
    operator_decision: str = OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE,
) -> dict[str, Any]:
    attestation = {
        "operator_decision": operator_decision,
        "selected_redesign_direction": selected_redesign_direction,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_V1,
        "operator_reference": operator_reference,
        "operator_confirms_candidate_review_digest": operator_confirms_candidate_review_digest,
        "operator_confirms_candidate_digest": operator_confirms_candidate_digest,
        "operator_confirms_planning_results_review_digest": operator_confirms_planning_results_review_digest,
        "operator_confirms_planning_execution_digest": operator_confirms_planning_execution_digest,
        "operator_confirms_records_digest": operator_confirms_records_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_meta_record_count": operator_confirms_meta_record_count,
        "operator_confirms_non_meta_record_count": operator_confirms_non_meta_record_count,
        "operator_confirms_selected_redesign_direction": operator_confirms_selected_redesign_direction,
        "operator_confirms_approval_scope_only": operator_confirms_approval_scope_only,
        "operator_confirms_execution_authorized": operator_confirms_execution_authorized,
        "operator_confirms_ready_for_execution": operator_confirms_ready_for_execution,
        "operator_confirms_no_execution_performed": operator_confirms_no_execution_performed,
        "operator_confirms_no_results_created": operator_confirms_no_results_created,
        "operator_confirms_no_label_regeneration": operator_confirms_no_label_regeneration,
        "operator_confirms_no_new_targets": operator_confirms_no_new_targets,
        "operator_confirms_no_target_definition_change_authorization": operator_confirms_no_target_definition_change_authorization,
        "operator_confirms_no_feature_generation": operator_confirms_no_feature_generation,
        "operator_confirms_no_feature_label_matrix_creation": operator_confirms_no_feature_label_matrix_creation,
        "operator_confirms_no_metric_recomputation_in_approval": operator_confirms_no_metric_recomputation_in_approval,
        "operator_confirms_no_model_training_in_approval": operator_confirms_no_model_training_in_approval,
        "operator_confirms_no_predictive_usefulness_acceptance": operator_confirms_no_predictive_usefulness_acceptance,
        "operator_confirms_no_profitability_acceptance": operator_confirms_no_profitability_acceptance,
        "operator_confirms_no_runtime_migration_approval": operator_confirms_no_runtime_migration_approval,
        "operator_confirms_no_strategy_authorization": operator_confirms_no_strategy_authorization,
        "operator_confirms_no_paper_trading": operator_confirms_no_paper_trading,
        "operator_confirms_no_broker_execution": operator_confirms_no_broker_execution,
        "operator_confirms_no_trade_recommendations": operator_confirms_no_trade_recommendations,
        "operator_confirms_no_api_key_storage_or_printing": operator_confirms_no_api_key_storage_or_printing,
        "operator_confirms_no_raw_payload_commit": operator_confirms_no_raw_payload_commit,
    }
    return _validated_attestation(attestation)


def _validated_attestation(attestation: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, Mapping):
        raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
            "operator_attestation must be an object"
        )
    required_keys = {
        "operator_decision", "selected_redesign_direction", "operator_attestation_phrase",
        "operator_attestation_timestamp_utc", "operator_attestation_version", "operator_reference",
        *DIGEST_CONFIRMATIONS, *VALUE_CONFIRMATIONS, *BOOLEAN_CONFIRMATIONS,
    }
    _expect(set(attestation), required_keys, "operator_attestation fields")
    _expect(
        attestation.get("operator_decision"),
        OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE,
        "operator_decision",
    )
    _expect(attestation.get("selected_redesign_direction"), SELECTED_DIRECTION,
            "selected_redesign_direction")
    _expect(
        attestation.get("operator_attestation_phrase"),
        REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_ATTESTATION_PHRASE,
        "operator_attestation_phrase",
    )
    _expect(
        attestation.get("operator_attestation_version"),
        OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_V1,
        "operator_attestation_version",
    )
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
                f"{field} must be non-empty"
            )
    for field, expected in {**DIGEST_CONFIRMATIONS, **VALUE_CONFIRMATIONS}.items():
        _expect(attestation.get(field), expected, field)
    for field in BOOLEAN_CONFIRMATIONS:
        _expect(attestation.get(field), True, field)
    return deepcopy(dict(attestation))


def _source_review(candidate_review_package: dict | None) -> dict[str, Any]:
    source = (
        review_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1()
        if candidate_review_package is None else deepcopy(candidate_review_package)
    )
    review_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(
        source
    )
    _expect(
        source.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest"),
        EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "source candidate review digest",
    )
    _expect(source.get("source_candidate_digest"), EXPECTED_CANDIDATE_DIGEST,
            "source candidate digest")
    summary = source.get("review_summary", {})
    _expect(summary.get("total_checks"), 84, "source review checklist total")
    _expect(summary.get("passed_checks"), 84, "source review checklist passed")
    _expect(summary.get("failed_checks"), 0, "source review checklist failed")
    _expect(summary.get("blocker_count"), 0, "source review blockers")
    return source


def _approved_source_inputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_input_id": row["source_input_id"],
            "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_EVIDENCE_EXECUTION_ONLY",
            "execution_performed": False,
            "source_regenerated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_source_inputs"]
    ]


def _approved_execution_activities(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "activity_id": row["activity_id"],
            "activity_status": AUTHORIZED_NOT_EXECUTED,
            "execution_authorized": True,
            "execution_performed": False,
            "label_generation_authorized": False,
            "feature_generation_authorized": False,
            "feature_label_matrix_creation_authorized": False,
            "metric_computation_performed": False,
            "model_training_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_execution_activities"]
    ]


def _approved_boundaries() -> dict[str, Any]:
    return {
        "improved_label_schema_generation_status": "AUTHORIZED_NOT_GENERATED_FOR_EXECUTION_PLANNING_ONLY",
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_status": NOT_AUTHORIZED,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_status": NOT_AUTHORIZED,
        "feature_label_matrix_created": False,
    }


def _approved_model_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "model_family_id": row["model_family_id"],
            "model_family_status": "AUTHORIZED_NOT_EVALUATED",
            "training_performed": False,
            "metric_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_model_and_baseline_families"]
    ]


def _approved_metric_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "metric_family_id": row["metric_family_id"],
            "metric_status": "AUTHORIZED_NOT_COMPUTED",
            "metric_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_metric_families"]
    ]


def _approved_future_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "future_output_id": row["future_output_id"],
            "output_status": AUTHORIZED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_future_outputs"]
    ]


def per_ticker_additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_additional_predictive_evidence_execution_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approval_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for source_entry in source["per_ticker_review_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry["meta_reduced_record_count_flag"],
            "improved_evidence_planning_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "additional_predictive_evidence_execution_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "additional_predictive_evidence_execution_approval_status": "APPROVED_FOR_FUTURE_RESEARCH_EXECUTION_ONLY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "additional_predictive_evidence_execution_authorized": True,
            "additional_predictive_evidence_executed": False,
            "additional_predictive_evidence_results_created": False,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_label_matrix_created": False,
            "metric_recomputation_performed_in_approval": False,
            "model_training_performed_in_approval": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
            "source_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        }
        if source_entry["ticker"] == "META":
            entry["approval_note"] = (
                "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE"
            )
        entry["per_ticker_additional_predictive_evidence_execution_approval_digest"] = (
            per_ticker_additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_approval(
    source: Mapping[str, Any], operator_attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_V1,
        "approval_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_candidate_review_artifact_kind": source["artifact_kind"],
        "source_candidate_review_status": source["review_status"],
        "source_candidate_artifact_kind": source["source_candidate_artifact_kind"],
        "source_candidate_status": source["source_candidate_status"],
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **deepcopy(BOUND_DIGESTS),
        "improved_evidence_planning_results_review_created": True,
        "improved_evidence_planning_results_review_ready": True,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_created": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created": True,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_approval_created": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence": True,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_approval": False,
        "model_training_performed_in_approval": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_migration_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "improved_evidence_planning_execution_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "records_digest": source["records_digest"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source["meta_reduced_record_count_preserved"],
        "selected_redesign_direction": source["selected_redesign_direction"],
        "majority_structure_risk": source["majority_structure_risk"],
        "largest_aggregated_class": source["largest_aggregated_class"],
        "largest_aggregated_class_count": source["largest_aggregated_class_count"],
        "no_trade_count": source["no_trade_count"],
        "oos_evaluated_rows": source["oos_evaluated_rows"],
        "majority_accuracy": source["majority_accuracy"],
        "local_model_accuracy": source["local_model_accuracy"],
        "cross_sectional_accuracy": source["cross_sectional_accuracy"],
        "cross_sectional_delta_vs_majority": source["cross_sectional_delta_vs_majority"],
        "global_five_session_threshold": source["global_five_session_threshold"],
        "benchmark_relative_threshold": source["benchmark_relative_threshold"],
        "approved_candidate_basis": deepcopy(source["reviewed_candidate_basis"]),
        "approved_objective": {
            "additional_predictive_evidence_execution_objective": EXECUTION_OBJECTIVE,
            "additional_predictive_evidence_execution_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
            "additional_predictive_evidence_execution_mode": EXECUTION_MODE,
            "additional_predictive_evidence_execution_authority_status": EXECUTION_AUTHORITY_STATUS,
        },
        "approved_source_inputs": _approved_source_inputs(source),
        "approved_execution_activities": _approved_execution_activities(source),
        "approved_label_feature_matrix_boundaries": _approved_boundaries(),
        "approved_model_and_baseline_families": _approved_model_families(source),
        "approved_metric_families": _approved_metric_families(source),
        "approved_future_outputs": _approved_future_outputs(source),
        "per_ticker_approval_entries": _per_ticker_approval_entries(source),
        "next_chain": deepcopy(NEXT_CHAIN),
        "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


def _derived_fields(approval: Mapping[str, Any]) -> dict[str, Any]:
    entries = approval.get("per_ticker_approval_entries", [])
    return {
        **approval,
        "target_universe_matches_review_universe": approval.get("target_universe") == TARGET_UNIVERSE,
        "approved_objective_valid": approval.get("approved_objective") == {
            "additional_predictive_evidence_execution_objective": EXECUTION_OBJECTIVE,
            "additional_predictive_evidence_execution_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
            "additional_predictive_evidence_execution_mode": EXECUTION_MODE,
            "additional_predictive_evidence_execution_authority_status": EXECUTION_AUTHORITY_STATUS,
        },
        "approved_source_input_count": len(approval.get("approved_source_inputs", [])),
        "approved_execution_activity_count": len(approval.get("approved_execution_activities", [])),
        "approved_model_family_count": len(approval.get("approved_model_and_baseline_families", [])),
        "approved_metric_family_count": len(approval.get("approved_metric_families", [])),
        "approved_future_output_count": len(approval.get("approved_future_outputs", [])),
        "per_ticker_approval_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_approval_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(
            isinstance(row.get("per_ticker_additional_predictive_evidence_execution_approval_digest"), str)
            and len(row["per_ticker_additional_predictive_evidence_execution_approval_digest"]) == 64
            and row["per_ticker_additional_predictive_evidence_execution_approval_digest"]
            == per_ticker_additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(row)
            for row in entries
        ),
    }


CHECK_FIELD_SPECS = [
    ("candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_DIGEST, "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest"),
    ("candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"),
    ("planning_results_review_digest_bound", BOUND_DIGESTS["improved_evidence_planning_results_review_using_redesigned_evidence_digest"], "improved_evidence_planning_results_review_using_redesigned_evidence_digest"),
    ("planning_execution_digest_bound", BOUND_DIGESTS["improved_evidence_planning_execution_using_redesigned_evidence_digest"], "improved_evidence_planning_execution_using_redesigned_evidence_digest"),
    ("planning_output_binding_digest_bound", BOUND_DIGESTS["improved_evidence_planning_output_binding_digest"], "improved_evidence_planning_output_binding_digest"),
    ("planning_approval_digest_bound", BOUND_DIGESTS["improved_evidence_planning_approval_using_redesigned_evidence_digest"], "improved_evidence_planning_approval_using_redesigned_evidence_digest"),
    ("planning_candidate_review_digest_bound", BOUND_DIGESTS["improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"], "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"),
    ("planning_candidate_digest_bound", BOUND_DIGESTS["improved_evidence_planning_candidate_using_redesigned_evidence_digest"], "improved_evidence_planning_candidate_using_redesigned_evidence_digest"),
    ("redesign_results_review_digest_bound", BOUND_DIGESTS["label_objective_redesign_results_review_using_redesigned_evidence_digest"], "label_objective_redesign_results_review_using_redesigned_evidence_digest"),
    ("redesign_execution_digest_bound", BOUND_DIGESTS["label_objective_redesign_execution_using_redesigned_evidence_digest"], "label_objective_redesign_execution_using_redesigned_evidence_digest"),
    ("target_definition_results_review_digest_bound", BOUND_DIGESTS["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], "label_objective_target_definition_results_review_using_redesigned_evidence_digest"),
    ("target_definition_execution_digest_bound", BOUND_DIGESTS["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"),
    ("path_selection_digest_bound", BOUND_DIGESTS["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], "method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
    ("readiness_review_digest_bound", BOUND_DIGESTS["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
    ("reassessment_digest_bound", BOUND_DIGESTS["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], "predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
    ("predictive_results_review_digest_bound", BOUND_DIGESTS["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], "additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
    ("predictive_execution_digest_bound", BOUND_DIGESTS["additional_predictive_evidence_execution_using_redesigned_labels_digest"], "additional_predictive_evidence_execution_using_redesigned_labels_digest"),
    ("matrix_digest_bound", BOUND_DIGESTS["feature_label_matrix_digest"], "feature_label_matrix_digest"),
    ("feature_values_digest_bound", BOUND_DIGESTS["feature_values_digest"], "feature_values_digest"),
    ("label_values_digest_bound", BOUND_DIGESTS["redesigned_label_values_digest"], "redesigned_label_values_digest"),
    ("research_registry_digest_bound", BOUND_DIGESTS["research_registry_approval_digest"], "research_registry_approval_digest"),
    ("records_digest_bound", BOUND_DIGESTS["records_digest"], "records_digest"),
    ("target_universe_12_preserved", 12, "target_universe_count"),
    ("target_universe_matches_review_universe", True, "target_universe_matches_review_universe"),
    ("records_digest_preserved", BOUND_DIGESTS["records_digest"], "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("operator_decision_matches", OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE, "operator_decision"),
    ("operator_attestation_phrase_matches", REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_ATTESTATION_PHRASE, "operator_attestation_phrase"),
    ("selected_redesign_direction_preserved", SELECTED_DIRECTION, "selected_redesign_direction"),
    ("approval_scope_only", ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY, "approval_scope"),
    ("additional_predictive_evidence_execution_approved_true", True, "additional_predictive_evidence_execution_approved"),
    ("additional_predictive_evidence_execution_approval_created_true", True, "additional_predictive_evidence_execution_approval_created"),
    ("additional_predictive_evidence_execution_authorized_true", True, "additional_predictive_evidence_execution_authorized"),
    ("ready_for_execution_true", True, "ready_for_additional_predictive_evidence_execution_using_improved_evidence"),
    ("execution_performed_false", False, "additional_predictive_evidence_executed"),
    ("results_created_false", False, "additional_predictive_evidence_results_created"),
    ("label_regeneration_authorized_false", False, "label_regeneration_authorized"),
    ("label_regeneration_performed_false", False, "label_regeneration_performed"),
    ("new_targets_created_false", False, "new_targets_created"),
    ("target_definition_change_authorized_false", False, "target_definition_change_authorized"),
    ("target_definition_change_performed_false", False, "target_definition_change_performed"),
    ("feature_generation_authorized_false", False, "feature_generation_authorized"),
    ("feature_generation_performed_false", False, "feature_generation_performed"),
    ("feature_label_matrix_created_false", False, "feature_label_matrix_created"),
    ("metric_recomputation_in_approval_false", False, "metric_recomputation_performed_in_approval"),
    ("model_training_in_approval_false", False, "model_training_performed_in_approval"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("approved_candidate_basis_preserved", review_service.candidate_service.CANDIDATE_BASIS, "approved_candidate_basis"),
    ("approved_objective_defined", True, "approved_objective_valid"),
    ("approved_source_inputs_15", 15, "approved_source_input_count"),
    ("approved_execution_activities_12", 12, "approved_execution_activity_count"),
    ("label_feature_matrix_boundaries_preserved", _approved_boundaries(), "approved_label_feature_matrix_boundaries"),
    ("approved_model_families_9", 9, "approved_model_family_count"),
    ("approved_metric_families_10", 10, "approved_metric_family_count"),
    ("approved_future_outputs_12", 12, "approved_future_output_count"),
    ("per_ticker_approval_entries_12", 12, "per_ticker_approval_entry_count"),
    ("per_ticker_approval_digests_present", True, "per_ticker_approval_digests_valid"),
    ("provider_requests_made_false", False, "provider_requests_made_in_approval"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed_in_approval"),
    ("dataset_regeneration_false", False, "canonical_dataset_regenerated_in_approval"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("feature_regeneration_false", False, "feature_regeneration_performed"),
    ("predictive_evidence_execution_rerun_false", False, "predictive_evidence_execution_rerun_performed"),
    ("improved_evidence_planning_execution_rerun_false", False, "improved_evidence_planning_execution_rerun_performed"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("next_chain_defined", NEXT_CHAIN, "next_chain"),
    ("next_gates_defined", NEXT_GATES, "next_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [row[0] for row in CHECK_FIELD_SPECS]


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_fields(approval)
    attestation = approval.get("operator_attestation", {})
    fields["operator_decision"] = attestation.get("operator_decision")
    fields["operator_attestation_phrase"] = attestation.get("operator_attestation_phrase")
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
        "additional_predictive_evidence_execution_approved_by_operator": not failed,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "additional_predictive_evidence_execution_authorized": not failed,
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence": not failed,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_approval": False,
        "model_training_performed_in_approval": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(approval))
    payload.pop("additional_predictive_evidence_execution_approval_using_improved_evidence_digest", None)
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    source = _source_review(candidate_review_package)
    attestation = _validated_attestation(operator_attestation)
    approval = _base_approval(source, attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval["additional_predictive_evidence_execution_approval_using_improved_evidence_digest"] = (
        additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(approval)
    )
    validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(approval)
    return approval


def _reject_forbidden_values(value: Any, *, path: str = "approval") -> None:
    forbidden_artifacts = {
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
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
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "metric_recomputation_performed_in_approval", "model_training_performed_in_approval",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "profitability_acceptance_created", "runtime_migration_approved", "runtime_migration_active",
        "runtime_migration_approval_created", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval", "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval", "canonical_dataset_regenerated_in_approval",
        "redesigned_label_regeneration_performed", "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed",
        "improved_evidence_planning_execution_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
                    f"{current} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
                    f"{current} must remain not accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
    approval: dict,
) -> dict[str, Any]:
    if not isinstance(approval, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
            "approval must be a JSON object"
        )
    _expect(
        approval.get("artifact_kind"),
        ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE,
        "artifact_kind",
    )
    _expect(
        approval.get("schema_version"),
        SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_V1,
        "schema_version",
    )
    _expect(
        approval.get("approval_status"),
        ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE,
        "approval_status",
    )
    _expect(approval.get("approval_scope"),
            ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY, "approval_scope")
    attestation = _validated_attestation(approval.get("operator_attestation", {}))
    _reject_forbidden_values(approval)
    source = _source_review(None)
    expected_base = _base_approval(source, attestation)
    for field, expected_value in expected_base.items():
        _expect(approval.get(field), expected_value, field)
    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
            "approval_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS,
            "approval_checklist check ids")
    _expect(checklist, _checklist(approval), "approval_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
            "approval_checklist must pass"
        )
    _expect(approval.get("approval_summary"), _summary(checklist), "approval_summary")
    digest = approval.get(
        "additional_predictive_evidence_execution_approval_using_improved_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
            "missing approval digest"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(approval),
        "approval digest",
    )
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_VALID,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "additional_predictive_evidence_execution_approval_using_improved_evidence_digest": digest,
        "per_ticker_approval_entry_count": len(approval["per_ticker_approval_entries"]),
        "blocker_count": approval["approval_summary"]["blocker_count"],
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence": True,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_additional_predictive_evidence_execution_approved_using_improved_evidence_markdown_v1(
    approval: dict,
) -> str:
    validation = validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
        approval
    )
    summary = approval["approval_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Approval Using Improved Evidence", "",
        "## Title", "- Optional Additional Predictive Evidence Execution Approval Using Improved Evidence v1.", "",
        "## Optional Additional Predictive Evidence Execution Approval Using Improved Evidence",
        f"- Artifact/status/scope: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}`.",
        f"- Approval digest: `{validation['additional_predictive_evidence_execution_approval_using_improved_evidence_digest']}`.", "",
        "## Operator Attestation",
        f"- Decision/reference/version: `{approval['operator_attestation']['operator_decision']}` / `{approval['operator_attestation']['operator_reference']}` / `{approval['operator_attestation']['operator_attestation_version']}`.", "",
        "## Source Candidate Review",
        f"- `{approval['source_candidate_review_artifact_kind']}` / `{approval['source_candidate_review_status']}` / `{approval['additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest']}`.", "",
        "## Bound Evidence", "- The candidate review, candidate, and complete source digest chain are bound.", "",
        "## Dataset and Universe", "- The frozen 12-ticker dataset remains 11,946 rows; META remains 913.", "",
        "## Approved Candidate Basis", f"- `{approval['approved_candidate_basis']}`", "",
        "## Approved Objective", f"- `{approval['approved_objective']}`", "",
        "## Approved Source Inputs",
    ]
    lines.extend(
        f"- `{row['source_input_id']}`: `{row['approval_status']}`."
        for row in approval["approved_source_inputs"]
    )
    lines.extend(["", "## Approved Execution Activities"])
    lines.extend(
        f"- `{row['activity_id']}`: `{row['activity_status']}`."
        for row in approval["approved_execution_activities"]
    )
    lines.extend([
        "", "## Approved Label / Feature / Matrix Boundaries",
        f"- `{approval['approved_label_feature_matrix_boundaries']}`", "",
        "## Approved Model and Baseline Families",
    ])
    lines.extend(
        f"- `{row['model_family_id']}`: `{row['model_family_status']}`."
        for row in approval["approved_model_and_baseline_families"]
    )
    lines.extend(["", "## Approved Metric Families"])
    lines.extend(
        f"- `{row['metric_family_id']}`: `{row['metric_status']}`."
        for row in approval["approved_metric_families"]
    )
    lines.extend(["", "## Approved Future Outputs"])
    lines.extend(
        f"- `{row['future_output_id']}`: `{row['output_status']}`."
        for row in approval["approved_future_outputs"]
    )
    lines.extend([
        "", "## Per-Ticker Approval Entries",
        "- Twelve entries authorize future research-only execution; META remains 913.",
        "", "## Next Chain",
    ])
    lines.extend(f"{index}. {item}" for index, item in enumerate(approval["next_chain"], 1))
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in approval["next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in approval["risk_controls"])
    lines.extend([
        "", "## Predictive Usefulness Boundary", "- Predictive usefulness remains `not accepted`.",
        "", "## Profitability Boundary", "- Profitability remains `not accepted`.",
        "", "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
        "", "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails",
        "- This approval authorizes only future research evidence execution. It performs no execution, regeneration, metric computation, model training, acceptance, runtime, or trading action.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    approval = build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "additional_predictive_evidence_execution_approval_using_improved_evidence_v1.json"
    payload = canonical_json_bytes(approval)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError(
            "approval output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "approval_status": approval["approval_status"],
        "additional_predictive_evidence_execution_approval_using_improved_evidence_digest": approval[
            "additional_predictive_evidence_execution_approval_using_improved_evidence_digest"
        ],
    }
