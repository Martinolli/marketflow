"""Offline, attestation-gated selection of a redesigned-evidence improvement path."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    method_evidence_improvement_candidate_redesigned_evidence_operator_review_service as review_service,
)


ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE = (
    "METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_USING_REDESIGNED_EVIDENCE_V1 = (
    "method_evidence_improvement_path_selection_using_redesigned_evidence_v1"
)
METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE = (
    "METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE"
)
METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY = (
    "METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY"
)
OPERATOR_DECISION = "SELECT_METHOD_EVIDENCE_IMPROVEMENT_PATH_USING_REDESIGNED_EVIDENCE"
OPERATOR_ATTESTATION_VERSION = (
    "method_evidence_improvement_path_selection_using_redesigned_evidence_attestation_v1"
)
REQUIRED_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ATTESTATION_PHRASE = (
    "SELECT METHOD EVIDENCE IMPROVEMENT PATH USING REDESIGNED EVIDENCE "
    "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY"
)
SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION = (
    "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION"
)
SELECTED_OPTION_RATIONALE = (
    "LABEL_OBJECTIVE_AND_SIGNAL_DEFINITION_SHOULD_BE_RECHECKED_BEFORE_MORE_EXECUTION_"
    "BECAUSE_OOS_EDGE_IS_SMALL_AND_LOCAL_MODEL_MATCHES_MAJORITY"
)
SELECTION_DECISION_BASIS = (
    "SOURCE_CANDIDATE_RECOMMENDED_OPTION_ACCEPTED_FOR_FUTURE_CANDIDATE_ONLY"
)
NEXT_ARTIFACT_KIND = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE"
)

EXPECTED_CANDIDATE_REVIEW_DIGEST = (
    "f98a468f3db63b53d76b0a5ff272c82cc4b826c0e97717f4326b0186bd39be81"
)
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_READINESS_REVIEW_DIGEST = review_service.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_REASSESSMENT_DIGEST = review_service.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = review_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = review_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_MATRIX_DIGEST = review_service.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = review_service.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = review_service.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = review_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = review_service.EXPECTED_RECORDS_DIGEST
EXPECTED_TARGET_UNIVERSE = list(review_service.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review_service.EXPECTED_RECORD_COUNTS)

SOURCE_REVIEW_ARTIFACT_KIND = (
    review_service.ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE
)
SOURCE_REVIEW_STATUS = (
    review_service.METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY
)
SOURCE_CANDIDATE_ARTIFACT_KIND = review_service.SOURCE_CANDIDATE_ARTIFACT_KIND
SOURCE_CANDIDATE_STATUS = review_service.SOURCE_CANDIDATE_STATUS
SOURCE_READINESS_DECISION = review_service.SOURCE_READINESS_DECISION
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

PATH_OPTION_IDS = list(review_service.IMPROVEMENT_OPTION_IDS)
PLANNED_NEXT_CANDIDATE_REVIEW_AREAS = [
    "current_label_family_objective_alignment",
    "tradeable_signal_vs_majority_structure",
    "cross_sectional_edge_materiality",
    "local_model_majority_equivalence",
    "horizon_and_threshold_noise_review",
    "class_balance_and_target_distribution_review",
    "per_ticker_label_behavior_review",
    "meta_limitation_label_behavior_review",
    "acceptance_threshold_prerequisite_review",
    "stop_or_continue_acceptance_path_review",
]
NEXT_CHAIN = [
    "Label Objective / Target Definition Review Candidate Using Redesigned Evidence v1.",
    "Label Objective / Target Definition Review Candidate Operator Review v1.",
    "Label Objective / Target Definition Review Approval v1, if selected.",
    "Optional label objective redesign or threshold/horizon refinement candidate, if review supports it.",
    "Optional improved evidence planning and execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "label_objective_target_definition_review_candidate_using_redesigned_evidence",
    "label_objective_target_definition_review_candidate_operator_review",
    "label_objective_target_definition_review_approval_if_selected",
    "label_objective_or_threshold_or_horizon_refinement_candidate_if_supported",
    "improved_evidence_planning_candidate_if_supported",
    "improved_evidence_execution_approval_if_required",
    "improved_evidence_execution_if_approved",
    "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "selection_does_not_create_next_candidate",
    "selection_does_not_approve_improvement",
    "selection_does_not_execute_improvement",
    "selection_does_not_generate_new_evidence",
    "selection_does_not_rerun_predictive_evidence",
    "selection_does_not_retrain_models",
    "selection_does_not_recompute_metrics",
    "selection_does_not_accept_predictive_usefulness",
    "selection_does_not_create_acceptance_candidate",
    "selection_does_not_accept_profitability",
    "selection_does_not_authorize_runtime",
    "selection_does_not_authorize_strategy",
    "selection_does_not_authorize_paper_trading",
    "selection_does_not_authorize_broker_execution",
    "selection_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_DIGESTS = {
    "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "method_evidence_improvement_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
    "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": EXPECTED_READINESS_REVIEW_DIGEST,
    "predictive_usefulness_reassessment_using_redesigned_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
    "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
    "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
    "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
    "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
    "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_source_readiness_not_ready",
    "operator_confirms_selection_only",
    "operator_confirms_no_next_candidate_created",
    "operator_confirms_no_improvement_approval",
    "operator_confirms_no_improvement_execution",
    "operator_confirms_no_evidence_generation",
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

CHECK_IDS = [
    "candidate_review_digest_bound", "candidate_digest_bound", "readiness_review_digest_bound",
    "reassessment_digest_bound", "results_review_digest_bound", "execution_digest_bound",
    "matrix_digest_bound", "feature_values_digest_bound", "label_values_digest_bound",
    "research_registry_digest_bound", "records_digest_bound", "target_universe_12_preserved",
    "target_universe_matches_review_universe", "records_digest_preserved", "meta_913_preserved",
    "operator_decision_matches", "operator_attestation_phrase_matches", "selected_option_is_option_a",
    "selected_option_matches_recommendation", "selection_scope_only", "path_selection_created_true",
    "method_evidence_improvement_path_selected_true",
    "ready_for_label_objective_target_definition_review_candidate_true", "next_artifact_kind_bound",
    "next_artifact_created_false", "method_evidence_improvement_approved_false",
    "method_evidence_improvement_authorized_false", "method_evidence_improvement_executed_false",
    "improved_evidence_planning_candidate_created_false", "predictive_usefulness_not_accepted",
    "acceptance_ready_false", "acceptance_candidate_created_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "path_options_preserved", "only_option_a_selected",
    "selection_basis_preserved", "next_candidate_scope_defined",
    "planned_next_candidate_review_areas_defined", "per_ticker_entries_12",
    "per_ticker_selection_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_selection_false",
    "model_training_in_selection_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(ValueError):
    """Raised when a selection violates its attestation or selection-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(f"{field} must be false")


def build_method_evidence_improvement_path_selection_using_redesigned_evidence_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_readiness_review_digest: str,
    operator_confirms_reassessment_digest: str,
    operator_confirms_results_review_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_source_readiness_not_ready: bool,
    operator_confirms_selected_option: str,
    operator_confirms_next_artifact_kind: str,
    operator_confirms_selection_only: bool,
    operator_confirms_no_next_candidate_created: bool,
    operator_confirms_no_improvement_approval: bool,
    operator_confirms_no_improvement_execution: bool,
    operator_confirms_no_evidence_generation: bool,
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
    selected_option: str = SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build a non-secret operator attestation; the selection builder validates it."""
    return {
        "operator_decision": operator_decision,
        "selected_option": selected_option,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_reference": operator_reference,
        "operator_confirms_candidate_review_digest": operator_confirms_candidate_review_digest,
        "operator_confirms_candidate_digest": operator_confirms_candidate_digest,
        "operator_confirms_readiness_review_digest": operator_confirms_readiness_review_digest,
        "operator_confirms_reassessment_digest": operator_confirms_reassessment_digest,
        "operator_confirms_results_review_digest": operator_confirms_results_review_digest,
        "operator_confirms_records_digest": operator_confirms_records_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_meta_record_count": operator_confirms_meta_record_count,
        "operator_confirms_non_meta_record_count": operator_confirms_non_meta_record_count,
        "operator_confirms_source_readiness_not_ready": operator_confirms_source_readiness_not_ready,
        "operator_confirms_selected_option": operator_confirms_selected_option,
        "operator_confirms_next_artifact_kind": operator_confirms_next_artifact_kind,
        "operator_confirms_selection_only": operator_confirms_selection_only,
        "operator_confirms_no_next_candidate_created": operator_confirms_no_next_candidate_created,
        "operator_confirms_no_improvement_approval": operator_confirms_no_improvement_approval,
        "operator_confirms_no_improvement_execution": operator_confirms_no_improvement_execution,
        "operator_confirms_no_evidence_generation": operator_confirms_no_evidence_generation,
        "operator_confirms_no_metric_recomputation": operator_confirms_no_metric_recomputation,
        "operator_confirms_no_model_training": operator_confirms_no_model_training,
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


def _validate_attestation(attestation: Any) -> None:
    if not isinstance(attestation, dict):
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError("operator attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_option": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
        "operator_attestation_phrase": REQUIRED_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_readiness_review_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        "operator_confirms_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "operator_confirms_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        "operator_confirms_target_universe": EXPECTED_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_option": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
        "operator_confirms_next_artifact_kind": NEXT_ARTIFACT_KIND,
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, f"operator attestation {field}")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(
                f"operator attestation {field} missing"
            )
    for field in ATTESTATION_BOOLEAN_FIELDS:
        _expect_true(attestation.get(field), f"operator attestation {field}")


def _source_review(candidate_review_package: dict | None) -> dict[str, Any]:
    source = (
        review_service.build_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1()
        if candidate_review_package is None
        else deepcopy(candidate_review_package)
    )
    review_service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
        source
    )
    _expect(
        source.get("method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"),
        EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "source candidate review digest",
    )
    return source


def _path_options() -> list[dict[str, Any]]:
    rows = []
    for option_id in PATH_OPTION_IDS:
        selected = option_id == SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION
        row = {"option_id": option_id, "selected": selected}
        if selected:
            row.update({
                "selection_status": "SELECTED_FOR_NEXT_CANDIDATE_ONLY",
                "next_artifact_kind": NEXT_ARTIFACT_KIND,
                "approval_created": False,
                "execution_created": False,
                "research_only": True,
                "non_actionable": True,
            })
        rows.append(row)
    return rows


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_method_evidence_improvement_path_selection_digest", None)
    return payload


def per_ticker_method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for a per-ticker selection entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for reviewed in source["per_ticker_review_entries"]:
        ticker = reviewed["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": reviewed["registry_approval_status"],
            "canonical_dataset_status": reviewed["canonical_dataset_status"],
            "historical_record_count": reviewed["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "method_evidence_improvement_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "method_evidence_improvement_path_selection_status": "SELECTED_OPTION_A_FOR_NEXT_CANDIDATE_ONLY",
            "selected_option": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
            "next_artifact_created": False,
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
        if ticker == "META":
            entry["selection_note"] = (
                "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW"
            )
        entry["per_ticker_method_evidence_improvement_path_selection_digest"] = (
            per_ticker_method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_selection(source: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_USING_REDESIGNED_EVIDENCE_V1,
        "selection_status": METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE,
        "selection_scope": METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_candidate_review_artifact_kind": SOURCE_REVIEW_ARTIFACT_KIND,
        "source_candidate_review_status": SOURCE_REVIEW_STATUS,
        "source_candidate_artifact_kind": SOURCE_CANDIDATE_ARTIFACT_KIND,
        "source_candidate_status": SOURCE_CANDIDATE_STATUS,
        **REQUIRED_DIGESTS,
        "selected_method_evidence_improvement_option": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
        "selected_method_evidence_improvement_option_rationale": SELECTED_OPTION_RATIONALE,
        "selection_decision_basis": SELECTION_DECISION_BASIS,
        "next_artifact_kind": NEXT_ARTIFACT_KIND,
        "next_artifact_created": False,
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_created": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_created": True,
        "method_evidence_improvement_path_selected": True,
        "method_evidence_improvement_path_selection_created": True,
        "ready_for_label_objective_target_definition_review_candidate_using_redesigned_evidence": True,
        "method_evidence_improvement_approved": False,
        "method_evidence_improvement_authorized": False,
        "method_evidence_improvement_executed": False,
        "label_objective_target_definition_review_candidate_created": False,
        "improved_evidence_planning_candidate_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
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
        "provider_requests_made_in_selection": False,
        "live_provider_transport_enabled_in_selection": False,
        "market_data_acquisition_performed_in_selection": False,
        "dataset_generation_performed_in_selection": False,
        "canonical_dataset_regenerated_in_selection": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "metric_recomputation_performed_in_selection": False,
        "model_training_performed_in_selection": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "source_readiness_decision": source["source_readiness_decision"],
        "selection_basis": {
            "readiness_decision_not_ready": True,
            "oos_cross_sectional_delta_vs_majority": "0.00309917",
            "oos_local_model_delta_vs_majority": "0",
            "predictive_signal_readiness": "NOT_READY",
            "baseline_outperformance_readiness": "NOT_READY",
            "local_model_readiness": "NOT_READY",
            "stability_readiness": "NOT_READY",
            "calibration_readiness": "REQUIRES_OPERATOR_REVIEW",
            "optional_model_coverage_sufficiency": "FAIL_OR_NOT_MET",
            "source_candidate_recommended_option": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
            "selected_option_matches_recommendation": True,
        },
        "path_options": _path_options(),
        "next_candidate_scope": {
            "label_objective_target_definition_review_candidate_objective": (
                "REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION_AFTER_NOT_READY_REDESIGNED_EVIDENCE_DECISION"
            ),
            "label_objective_target_definition_review_candidate_scope": (
                "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
            ),
            "label_objective_target_definition_review_candidate_status": "PLANNED_NOT_CREATED",
            "label_objective_target_definition_review_candidate_authority_status": NOT_AUTHORIZED,
        },
        "planned_next_candidate_review_areas": [
            {"review_area": area, "status": PLANNED_NOT_EXECUTED, "mode": RESEARCH_ONLY_NON_ACTIONABLE}
            for area in PLANNED_NEXT_CANDIDATE_REVIEW_AREAS
        ],
        "per_ticker_selection_entries": _per_ticker_entries(source),
        "next_chain": deepcopy(NEXT_CHAIN),
        "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


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


def _checklist(selection: Mapping[str, Any]) -> list[dict[str, Any]]:
    options = selection.get("path_options", [])
    areas = selection.get("planned_next_candidate_review_areas", [])
    entries = selection.get("per_ticker_selection_entries", [])
    attestation = selection.get("operator_attestation", {})
    actuals = {
        "candidate_review_digest_bound": selection.get("method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"),
        "candidate_digest_bound": selection.get("method_evidence_improvement_candidate_using_redesigned_evidence_digest"),
        "readiness_review_digest_bound": selection.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": selection.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "results_review_digest_bound": selection.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": selection.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": selection.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": selection.get("feature_values_digest"),
        "label_values_digest_bound": selection.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": selection.get("research_registry_approval_digest"),
        "records_digest_bound": selection.get("records_digest"),
        "target_universe_12_preserved": selection.get("target_universe_count"),
        "target_universe_matches_review_universe": selection.get("target_universe"),
        "records_digest_preserved": selection.get("records_digest"),
        "meta_913_preserved": selection.get("meta_record_count"),
        "operator_decision_matches": attestation.get("operator_decision"),
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase"),
        "selected_option_is_option_a": selection.get("selected_method_evidence_improvement_option"),
        "selected_option_matches_recommendation": selection.get("selection_basis", {}).get("selected_option_matches_recommendation"),
        "selection_scope_only": selection.get("selection_scope"),
        "path_selection_created_true": selection.get("method_evidence_improvement_path_selection_created"),
        "method_evidence_improvement_path_selected_true": selection.get("method_evidence_improvement_path_selected"),
        "ready_for_label_objective_target_definition_review_candidate_true": selection.get("ready_for_label_objective_target_definition_review_candidate_using_redesigned_evidence"),
        "next_artifact_kind_bound": selection.get("next_artifact_kind"),
        "next_artifact_created_false": selection.get("next_artifact_created"),
        "method_evidence_improvement_approved_false": selection.get("method_evidence_improvement_approved"),
        "method_evidence_improvement_authorized_false": selection.get("method_evidence_improvement_authorized"),
        "method_evidence_improvement_executed_false": selection.get("method_evidence_improvement_executed"),
        "improved_evidence_planning_candidate_created_false": selection.get("improved_evidence_planning_candidate_created"),
        "predictive_usefulness_not_accepted": selection.get("predictive_usefulness"),
        "acceptance_ready_false": selection.get("predictive_usefulness_acceptance_ready"),
        "acceptance_candidate_created_false": selection.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": selection.get("profitability"),
        "runtime_not_authorized": selection.get("runtime_use"),
        "strategy_not_authorized": selection.get("strategy_use"),
        "broker_not_authorized": selection.get("broker_execution"),
        "trade_recommendations_false": selection.get("trade_recommendations_generated"),
        "path_options_preserved": [row.get("option_id") for row in options],
        "only_option_a_selected": [row.get("option_id") for row in options if row.get("selected") is True],
        "selection_basis_preserved": selection.get("selection_decision_basis"),
        "next_candidate_scope_defined": bool(selection.get("next_candidate_scope")),
        "planned_next_candidate_review_areas_defined": [row.get("review_area") for row in areas],
        "per_ticker_entries_12": len(entries),
        "per_ticker_selection_digests_present": all(isinstance(row.get("per_ticker_method_evidence_improvement_path_selection_digest"), str) and len(row["per_ticker_method_evidence_improvement_path_selection_digest"]) == 64 for row in entries),
        "provider_requests_made_false": selection.get("provider_requests_made_in_selection"),
        "market_data_acquisition_false": selection.get("market_data_acquisition_performed_in_selection"),
        "dataset_regeneration_false": selection.get("canonical_dataset_regenerated_in_selection"),
        "redesigned_label_regeneration_false": selection.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": selection.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": selection.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_selection_false": selection.get("metric_recomputation_performed_in_selection"),
        "model_training_in_selection_false": selection.get("model_training_performed_in_selection"),
        "no_predictive_usefulness_acceptance_artifact_created": selection.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": selection.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": selection.get("runtime_migration_approval_created"),
        "next_chain_defined": selection.get("next_chain"),
        "next_gates_defined": selection.get("next_gates"),
        "risk_controls_defined": selection.get("risk_controls"),
        "no_tracked_marketflow_files": selection.get("no_tracked_marketflow_files"),
    }
    expected = {
        "candidate_review_digest_bound": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "candidate_digest_bound": EXPECTED_CANDIDATE_DIGEST,
        "readiness_review_digest_bound": EXPECTED_READINESS_REVIEW_DIGEST,
        "reassessment_digest_bound": EXPECTED_REASSESSMENT_DIGEST,
        "results_review_digest_bound": EXPECTED_RESULTS_REVIEW_DIGEST,
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST,
        "matrix_digest_bound": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest_bound": EXPECTED_FEATURE_VALUES_DIGEST,
        "label_values_digest_bound": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest_bound": EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": 12,
        "target_universe_matches_review_universe": EXPECTED_TARGET_UNIVERSE,
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": 913,
        "operator_decision_matches": OPERATOR_DECISION,
        "operator_attestation_phrase_matches": REQUIRED_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ATTESTATION_PHRASE,
        "selected_option_is_option_a": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
        "selected_option_matches_recommendation": True,
        "selection_scope_only": METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY,
        "path_selection_created_true": True,
        "method_evidence_improvement_path_selected_true": True,
        "ready_for_label_objective_target_definition_review_candidate_true": True,
        "next_artifact_kind_bound": NEXT_ARTIFACT_KIND,
        "next_artifact_created_false": False,
        "method_evidence_improvement_approved_false": False,
        "method_evidence_improvement_authorized_false": False,
        "method_evidence_improvement_executed_false": False,
        "improved_evidence_planning_candidate_created_false": False,
        "predictive_usefulness_not_accepted": NOT_ACCEPTED,
        "acceptance_ready_false": False,
        "acceptance_candidate_created_false": False,
        "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED,
        "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED,
        "trade_recommendations_false": False,
        "path_options_preserved": PATH_OPTION_IDS,
        "only_option_a_selected": [SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION],
        "selection_basis_preserved": SELECTION_DECISION_BASIS,
        "next_candidate_scope_defined": True,
        "planned_next_candidate_review_areas_defined": PLANNED_NEXT_CANDIDATE_REVIEW_AREAS,
        "per_ticker_entries_12": 12,
        "per_ticker_selection_digests_present": True,
        "provider_requests_made_false": False,
        "market_data_acquisition_false": False,
        "dataset_regeneration_false": False,
        "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False,
        "predictive_evidence_rerun_false": False,
        "metric_recomputation_in_selection_false": False,
        "model_training_in_selection_false": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False,
        "no_runtime_migration_approval_created": False,
        "next_chain_defined": NEXT_CHAIN,
        "next_gates_defined": NEXT_GATES,
        "risk_controls_defined": RISK_CONTROLS,
        "no_tracked_marketflow_files": True,
    }
    return [_check(check_id, expected[check_id], actuals[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    passed = sum(row.get("status") == PASS for row in rows)
    failed = len(rows) - passed
    blockers = sum(row.get("status") == FAIL and row.get("severity") == BLOCKER for row in rows)
    return {
        "total_checks": len(rows),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "method_evidence_improvement_path_selected": True,
        "selected_option": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
        "next_artifact_kind": NEXT_ARTIFACT_KIND,
        "next_artifact_created": False,
        "method_evidence_improvement_approved": False,
        "method_evidence_improvement_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(selection: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(selection))
    payload.pop("method_evidence_improvement_path_selection_using_redesigned_evidence_digest", None)
    return payload


def method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(
    selection: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for the complete attested selection."""
    return semantic_digest(_digest_payload(selection))


def build_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build the selection-only artifact from the validated committed review package."""
    _validate_attestation(operator_attestation)
    source = _source_review(candidate_review_package)
    selection = _base_selection(source, operator_attestation)
    selection["selection_checklist"] = _checklist(selection)
    selection["selection_summary"] = _summary(selection["selection_checklist"])
    selection["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"] = (
        method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(selection)
    )
    validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(selection)
    return selection


def _reject_forbidden_authority(value: Any, *, path: str = "selection") -> None:
    forbidden_true_fields = {
        "next_artifact_created", "method_evidence_improvement_approved",
        "method_evidence_improvement_authorized", "method_evidence_improvement_executed",
        "label_objective_target_definition_review_candidate_created",
        "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_executed", "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "profitability_acceptance_created",
        "runtime_migration_approved", "runtime_migration_active", "runtime_migration_approval_created",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_selection", "live_provider_transport_enabled_in_selection",
        "market_data_acquisition_performed_in_selection", "dataset_generation_performed_in_selection",
        "canonical_dataset_regenerated_in_selection", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_selection", "model_training_performed_in_selection",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
    selection: dict,
) -> dict:
    """Validate all bindings, digests, checklist rows, and closed authorities."""
    if not isinstance(selection, dict):
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError("selection must be an object")
    _reject_forbidden_authority(selection)
    _validate_attestation(selection.get("operator_attestation"))
    source = _source_review(None)
    expected_base = _base_selection(source, selection["operator_attestation"])
    for field, value in expected_base.items():
        _expect(selection.get(field), value, field)
    entries = selection.get("per_ticker_selection_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError("per-ticker entries mismatch")
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        _expect(row.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(row.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        digest = row.get("per_ticker_method_evidence_improvement_path_selection_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(f"{ticker} selection digest missing")
        _expect(
            digest,
            per_ticker_method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(row),
            f"{ticker} selection digest",
        )
    checklist = selection.get("selection_checklist")
    if not isinstance(checklist, list):
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError("selection checklist missing")
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "selection checklist IDs")
    expected_checklist = _checklist(selection)
    _expect(checklist, expected_checklist, "selection checklist")
    if any(row["status"] != PASS for row in checklist):
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError("selection checklist failed")
    _expect(selection.get("selection_summary"), _summary(checklist), "selection summary")
    digest = selection.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError("selection digest missing")
    _expect(
        digest,
        method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(selection),
        "selection digest",
    )
    return {
        "status": "METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_USING_REDESIGNED_EVIDENCE_VALID",
        "artifact_kind": selection["artifact_kind"],
        "selection_status": selection["selection_status"],
        "selection_scope": selection["selection_scope"],
        "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": digest,
        "selected_option": SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
        "next_artifact_kind": NEXT_ARTIFACT_KIND,
        "next_artifact_created": False,
        **{key: selection["selection_summary"][key] for key in (
            "total_checks", "passed_checks", "failed_checks", "blocker_count"
        )},
    }


def build_method_evidence_improvement_path_selection_using_redesigned_evidence_markdown_v1(
    selection: dict,
) -> str:
    """Render a sanitized Markdown view of the validated selection."""
    validation = validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(selection)
    attestation = selection["operator_attestation"]
    summary = selection["selection_summary"]
    sections = [
        ("Title", ["Method / Evidence Improvement Path Selection Using Redesigned Evidence"]),
        ("Method / Evidence Improvement Path Selection Using Redesigned Evidence", [
            f"Artifact/status/scope: `{selection['artifact_kind']}` / `{selection['selection_status']}` / `{selection['selection_scope']}`.",
            f"Digest: `{validation['method_evidence_improvement_path_selection_using_redesigned_evidence_digest']}`.",
        ]),
        ("Operator Attestation", [
            f"Reference/timestamp/version: `{attestation['operator_reference']}` / `{attestation['operator_attestation_timestamp_utc']}` / `{attestation['operator_attestation_version']}`.",
            f"Decision: `{attestation['operator_decision']}`.",
        ]),
        ("Source Candidate Review", [
            f"Artifact/status: `{selection['source_candidate_review_artifact_kind']}` / `{selection['source_candidate_review_status']}`.",
            f"Digest: `{selection['method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest']}`.",
        ]),
        ("Bound Evidence", [f"`{field}`: `{digest}`." for field, digest in REQUIRED_DIGESTS.items()]),
        ("Dataset and Universe", [
            f"Dataset/profile/timeframe: `{selection['dataset_name']}` / `{selection['source_profile']}` / `{selection['timeframe']}`.",
            "Universe: " + ", ".join(f"`{ticker}`" for ticker in selection["target_universe"]) + ".",
            "META remains `913`; every other ticker remains `1003`.",
        ]),
        ("Path Options", [f"`{row['option_id']}`: selected `{row['selected']}`." for row in selection["path_options"]]),
        ("Selected Option", [
            f"Selected: `{selection['selected_method_evidence_improvement_option']}`.",
            f"Next artifact: `{selection['next_artifact_kind']}`; created: `{selection['next_artifact_created']}`.",
        ]),
        ("Selection Basis", [f"`{key}`: `{value}`." for key, value in selection["selection_basis"].items()]),
        ("Next Candidate Scope", [f"`{key}`: `{value}`." for key, value in selection["next_candidate_scope"].items()]),
        ("Planned Next-Candidate Review Areas", [f"`{row['review_area']}`: `{row['status']}` / `{row['mode']}`." for row in selection["planned_next_candidate_review_areas"]]),
        ("Per-Ticker Selection Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, status `{row['method_evidence_improvement_path_selection_status']}`, digest `{row['per_ticker_method_evidence_improvement_path_selection_digest']}`." for row in selection["per_ticker_selection_entries"]]),
        ("Next Chain", selection["next_chain"]),
        ("Next Gates", selection["next_gates"]),
        ("Risk Controls", selection["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate was created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`."]),
        ("Guardrails", ["This artifact selects Option A for a future candidate only. It creates no candidate, approval, execution, evidence, acceptance, profitability, runtime, strategy, broker, or trading authority."]),
    ]
    lines = ["# Method / Evidence Improvement Path Selection Using Redesigned Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical selection JSON without overwriting an existing artifact."""
    selection = build_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
        selection
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "method_evidence_improvement_path_selection_using_redesigned_evidence_v1.json"
    if path.exists():
        raise MethodEvidenceImprovementPathSelectionRedesignedEvidenceError(
            "selection output already exists"
        )
    payload = canonical_json_bytes(selection)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
