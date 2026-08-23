"""Offline final archive record for the current improved-evidence acceptance path."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import operator_method_or_closure_selection_improved_evidence_service as selection


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE_V1 = (
    "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_CURRENT_IMPROVED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_CURRENT_IMPROVED_EVIDENCE"
)
ARCHIVE_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH_NOT_READY = (
    "ARCHIVE_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH_NOT_READY"
)
ARCHIVE_REASON = (
    "OPERATOR_SELECTED_STOP_CURRENT_DATASET_AFTER_NOT_READY_READINESS_SMALL_EDGE_"
    "LOCAL_MODEL_MATCHES_MAJORITY_AND_OPTIONAL_MODEL_COVERAGE_INCOMPLETE"
)
ARCHIVE_RECORD_ONLY = "ARCHIVE_RECORD_ONLY"
ARCHIVE_CLASSIFICATION = "FINAL_DISPOSITION_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH"
ACCEPTANCE_PATH_STATUS = "ARCHIVED_NOT_READY_FOR_CURRENT_IMPROVED_EVIDENCE"
FUTURE_REOPEN_STATUS = "REQUIRES_NEW_OPERATOR_METHOD_SELECTION"

EXPECTED_SELECTION_DIGEST = "fccd75c360f68fcb7181bcbbc3afb98ba57b1f667cd0b930a2e45d0041b2a048"
EXPECTED_CLOSURE_DIGEST = selection.EXPECTED_CLOSURE_DIGEST
EXPECTED_READINESS_DIGEST = selection.EXPECTED_READINESS_DIGEST
EXPECTED_REASSESSMENT_DIGEST = selection.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = selection.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = selection.EXPECTED_EXECUTION_DIGEST
EXPECTED_OUTPUT_BINDING_DIGEST = selection.EXPECTED_OUTPUT_BINDING_DIGEST
EXPECTED_MATRIX_DIGEST = selection.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = selection.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = selection.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = selection.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = selection.EXPECTED_RECORDS_DIGEST
SOURCE_EVIDENCE = deepcopy(selection.SOURCE_EVIDENCE)
TARGET_UNIVERSE = list(selection.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(selection.EXPECTED_RECORD_COUNTS)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ARCHIVED_OPTIONS = {
    option: {
        "source_status": values["source_status"],
        "selection_status": values["selection_status"],
        "archive_status": (
            "ARCHIVED_SELECTED_PATH"
            if option == selection.SELECTED_OPTION
            else "GOVERNANCE_OPTION_SUPERSEDED_BY_OPTION_A_ARCHIVE_RECORD"
            if option == "OPTION_G_STOP_PROJECT_OR_ARCHIVE_CURRENT_PREDICTIVE_ACCEPTANCE_CHAIN"
            else "PROHIBITED_CURRENT_EVIDENCE_NOT_READY"
            if option == "OPTION_H_ACCEPTANCE_CANDIDATE"
            else "AVAILABLE_ONLY_IF_REOPENED_BY_OPERATOR"
        ),
    }
    for option, values in selection.SELECTION_OPTIONS_REVIEW.items()
}

NEXT_CHAIN = [
    "Current predictive-usefulness acceptance path is archived for this improved-evidence set.",
    "No further action is required for the current acceptance path.",
    "Future research requires a new operator method selection artifact if reopened.",
    "Any future evidence candidate requires separate review, approval, execution, results review, reassessment, and readiness gates.",
    "Acceptance candidate only if a future readiness review passes.",
    "Profitability review only after separate predictive-usefulness acceptance chain.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "current_acceptance_path_archived_no_immediate_next_gate",
    "future_operator_method_selection_if_reopened",
    "future_method_or_evidence_improvement_candidate_if_selected",
    "future_evidence_candidate_review_approval_execution_if_selected",
    "future_reassessment_after_new_evidence",
    "future_acceptance_readiness_after_new_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "archive_does_not_create_future_method_candidate",
    "archive_does_not_create_future_evidence_candidate",
    "archive_does_not_accept_predictive_usefulness",
    "archive_does_not_create_acceptance_candidate",
    "archive_does_not_create_acceptance_ceremony",
    "archive_does_not_accept_profitability",
    "archive_does_not_authorize_runtime",
    "archive_does_not_authorize_strategy",
    "archive_does_not_authorize_paper_trading",
    "archive_does_not_authorize_broker_execution",
    "archive_does_not_generate_trade_recommendations",
    "archive_does_not_regenerate_labels",
    "archive_does_not_create_new_targets",
    "archive_does_not_authorize_target_definition_change",
    "archive_does_not_generate_features",
    "archive_does_not_create_canonical_feature_label_matrix",
    "archive_does_not_rerun_predictive_evidence",
    "archive_does_not_rerun_reassessment",
    "archive_does_not_rerun_readiness_review",
    "archive_does_not_recompute_metrics",
    "archive_does_not_train_models",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_prior_predictive_evidence_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "do_not_mutate_current_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(ValueError):
    """Raised when the terminal archive record violates its closed boundary."""


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_archive_record_digest", None)
    return payload


def per_ticker_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker archive entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "source_readiness_decision": selection.closure_service.readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
            "source_selection_decision": selection.SELECTED_DECISION,
            "archive_status": "ARCHIVED_NOT_READY_CURRENT_IMPROVED_EVIDENCE",
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_selection_digest": EXPECTED_SELECTION_DIGEST,
            "source_closure_digest": EXPECTED_CLOSURE_DIGEST,
            "source_readiness_digest": EXPECTED_READINESS_DIGEST,
            "archive_note": (
                "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_archive_record_digest"] = (
            per_ticker_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_archive() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE_V1,
        "archive_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "archive_decision": ARCHIVE_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH_NOT_READY,
        "archive_reason": ARCHIVE_REASON,
        "archive_scope": ARCHIVE_RECORD_ONLY,
        "created_offline": True,
        "research_only": True,
        "final_disposition_record": True,
        "source_operator_selection_artifact_kind": selection.ARTIFACT_KIND_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE,
        "source_operator_selection_status": selection.OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_IMPROVED_EVIDENCE,
        "source_operator_selection_scope": selection.OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY,
        "source_operator_selection_digest": EXPECTED_SELECTION_DIGEST,
        "operator_method_or_closure_selection_using_improved_evidence_digest": EXPECTED_SELECTION_DIGEST,
        "source_selected_option": selection.SELECTED_OPTION,
        "source_selected_decision": selection.SELECTED_DECISION,
        "source_closure_artifact_kind": selection.closure_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE,
        "source_closure_status": selection.closure_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "source_closure_decision": selection.closure_service.CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
        "source_closure_digest": EXPECTED_CLOSURE_DIGEST,
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest": EXPECTED_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_READINESS_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": EXPECTED_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        **deepcopy(SOURCE_EVIDENCE),
        "predictive_usefulness_acceptance_path_archive_record_created": True,
        "predictive_usefulness_acceptance_path_archived_for_current_improved_evidence": True,
        "current_improved_evidence_acceptance_path_final_disposition_recorded": True,
        "future_reopen_requires_new_operator_method_selection": True,
        "method_improvement_candidate_created": False,
        "future_evidence_candidate_created": False,
        "future_evidence_execution_created": False,
        "future_reassessment_created": False,
        "future_readiness_review_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_ceremony_allowed": False,
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
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_archive": False,
        "model_training_performed_in_archive": False,
        "provider_requests_made_in_archive": False,
        "live_provider_transport_enabled_in_archive": False,
        "market_data_acquisition_performed_in_archive": False,
        "dataset_generation_performed_in_archive": False,
        "canonical_dataset_regenerated_in_archive": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "additional_predictive_evidence_execution_rerun_performed": False,
        "predictive_usefulness_reassessment_rerun_performed": False,
        "predictive_usefulness_acceptance_readiness_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "selected_option": selection.SELECTED_OPTION,
        "selection_decision": selection.SELECTED_DECISION,
        "readiness_decision": selection.closure_service.readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "readiness_reason": selection.closure_service.readiness.READINESS_REASON,
        "closure_status": selection.closure_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "closure_decision": selection.closure_service.CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
        "recommended_current_decision": selection.SELECTED_OPTION,
        "matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_count": 1152,
        "oos_row_count": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "majority_brier": "0.04867526",
        "local_model_brier": "0.04867526",
        "cross_sectional_brier": "0.04831065",
        "optional_tree_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "optional_ensemble_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "leakage_control_passed": True,
        "leakage_failed_control_count": 0,
        "leakage_control_count": 8,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT",
        "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540,
        "archive_classification": ARCHIVE_CLASSIFICATION,
        "acceptance_path_status": ACCEPTANCE_PATH_STATUS,
        "future_reopen_status": FUTURE_REOPEN_STATUS,
        "predictive_usefulness_interpretation": "NOT_ACCEPTED",
        "profitability_interpretation": "NOT_ACCEPTED",
        "runtime_interpretation": NOT_AUTHORIZED,
        "archived_options": deepcopy(ARCHIVED_OPTIONS),
        "per_ticker_archive_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
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


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(entry, dict)
        and isinstance(entry.get("per_ticker_archive_record_digest"), str)
        and entry["per_ticker_archive_record_digest"]
        == per_ticker_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(archive: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    options = archive.get("archived_options", {})
    entries = archive.get("per_ticker_archive_entries", [])
    unavailable = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    return [
        ("source_selection_digest_bound", EXPECTED_SELECTION_DIGEST, archive.get("source_operator_selection_digest")),
        ("source_closure_digest_bound", EXPECTED_CLOSURE_DIGEST, archive.get("source_closure_digest")),
        ("source_readiness_digest_bound", EXPECTED_READINESS_DIGEST, archive.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", EXPECTED_REASSESSMENT_DIGEST, archive.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, archive.get("source_results_review_digest")),
        ("source_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, archive.get("source_execution_digest")),
        ("source_output_binding_digest_bound", EXPECTED_OUTPUT_BINDING_DIGEST, archive.get("source_output_binding_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, archive.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, archive.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, archive.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, archive.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, archive.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, archive.get("target_universe")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, archive.get("records_digest")),
        ("meta_913_preserved", 913, archive.get("meta_record_count")),
        ("selection_option_a_bound", selection.SELECTED_OPTION, archive.get("source_selected_option")),
        ("selection_decision_bound", selection.SELECTED_DECISION, archive.get("source_selected_decision")),
        ("archive_status_correct", PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_CURRENT_IMPROVED_EVIDENCE, archive.get("archive_status")),
        ("archive_decision_correct", ARCHIVE_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH_NOT_READY, archive.get("archive_decision")),
        ("archive_reason_correct", ARCHIVE_REASON, archive.get("archive_reason")),
        ("archive_record_created_true", True, archive.get("predictive_usefulness_acceptance_path_archive_record_created")),
        ("acceptance_path_archived_true", True, archive.get("predictive_usefulness_acceptance_path_archived_for_current_improved_evidence")),
        ("final_disposition_recorded_true", True, archive.get("current_improved_evidence_acceptance_path_final_disposition_recorded")),
        ("future_reopen_requires_new_operator_selection_true", True, archive.get("future_reopen_requires_new_operator_method_selection")),
        ("method_improvement_candidate_created_false", False, archive.get("method_improvement_candidate_created")),
        ("future_evidence_candidate_created_false", False, archive.get("future_evidence_candidate_created")),
        ("future_evidence_execution_created_false", False, archive.get("future_evidence_execution_created")),
        ("future_reassessment_created_false", False, archive.get("future_reassessment_created")),
        ("future_readiness_review_created_false", False, archive.get("future_readiness_review_created")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, archive.get("predictive_usefulness")),
        ("acceptance_ready_false", False, archive.get("predictive_usefulness_acceptance_ready")),
        ("acceptance_recommended_false", False, archive.get("predictive_usefulness_acceptance_recommended")),
        ("acceptance_candidate_created_false", False, archive.get("predictive_usefulness_acceptance_candidate_created")),
        ("acceptance_ceremony_allowed_false", False, archive.get("predictive_usefulness_acceptance_ceremony_allowed")),
        ("profitability_not_accepted", NOT_ACCEPTED, archive.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, archive.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, archive.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, archive.get("broker_execution")),
        ("trade_recommendations_false", False, archive.get("trade_recommendations_generated")),
        ("label_regeneration_authorized_false", False, archive.get("label_regeneration_authorized")),
        ("label_regeneration_performed_false", False, archive.get("label_regeneration_performed")),
        ("new_targets_created_false", False, archive.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, archive.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, archive.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, archive.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, archive.get("feature_label_matrix_created")),
        ("metric_recomputation_in_archive_false", False, archive.get("metric_recomputation_performed_in_archive")),
        ("model_training_in_archive_false", False, archive.get("model_training_performed_in_archive")),
        ("predictive_evidence_rerun_false", False, archive.get("additional_predictive_evidence_execution_rerun_performed")),
        ("reassessment_rerun_false", False, archive.get("predictive_usefulness_reassessment_rerun_performed")),
        ("readiness_rerun_false", False, archive.get("predictive_usefulness_acceptance_readiness_rerun_performed")),
        ("matrix_rows_preserved", 143352, archive.get("matrix_row_count")),
        ("small_cross_sectional_edge_preserved", "0.00309917", archive.get("cross_sectional_delta_vs_majority")),
        ("local_model_equivalence_preserved", archive.get("majority_accuracy"), archive.get("local_model_accuracy")),
        ("optional_models_unavailable_preserved", [unavailable, unavailable], [archive.get("optional_tree_model_status"), archive.get("optional_ensemble_model_status")]),
        ("leakage_controls_passed", [True, 0, 8], [archive.get("leakage_control_passed"), archive.get("leakage_failed_control_count"), archive.get("leakage_control_count")]),
        ("meta_limitation_preserved", True, archive.get("meta_reduced_record_count_preserved")),
        ("archived_options_present", list(ARCHIVED_OPTIONS), list(options) if isinstance(options, dict) else []),
        ("option_a_archived_selected_path", "ARCHIVED_SELECTED_PATH", options.get(selection.SELECTED_OPTION, {}).get("archive_status") if isinstance(options, dict) else None),
        ("option_h_acceptance_candidate_prohibited", "PROHIBITED_CURRENT_EVIDENCE_NOT_READY", options.get("OPTION_H_ACCEPTANCE_CANDIDATE", {}).get("archive_status") if isinstance(options, dict) else None),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, archive.get("provider_requests_made_in_archive")),
        ("market_data_acquisition_false", False, archive.get("market_data_acquisition_performed_in_archive")),
        ("dataset_regeneration_false", False, archive.get("canonical_dataset_regenerated_in_archive")),
        ("raw_provider_payloads_not_committed", False, archive.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, archive.get("api_keys_stored_or_printed")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, archive.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, archive.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, archive.get("runtime_migration_approval_created")),
        ("next_chain_defined", NEXT_CHAIN, archive.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, archive.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, archive.get("risk_controls")),
        ("no_tracked_marketflow_files", True, archive.get("no_tracked_marketflow_files")),
    ]


def _checklist(archive: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(archive)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = sum(row.get("status") != PASS for row in rows)
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - failed,
        "failed_checks": failed,
        "blocker_count": sum(
            row.get("status") != PASS and row.get("severity") == BLOCKER for row in rows
        ),
        "archive_record_created": True,
        "acceptance_path_archived_for_current_improved_evidence": True,
        "archive_decision": ARCHIVE_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH_NOT_READY,
        "source_selected_option": selection.SELECTED_OPTION,
        "future_reopen_requires_new_operator_method_selection": True,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(archive: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(archive))
    payload.pop("archive_checklist", None)
    payload.pop("archive_summary", None)
    payload.pop("predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest", None)
    return payload


def predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest_v1(
    archive: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the archive record."""
    return semantic_digest(_digest_payload(archive))


def build_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1() -> dict:
    """Build the terminal archive record without providers, execution, or mutation."""
    archive = _base_archive()
    checklist = _checklist(archive)
    archive["archive_checklist"] = checklist
    archive["archive_summary"] = _summary(checklist)
    archive["predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"] = (
        predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest_v1(archive)
    )
    validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(archive)
    return archive


def validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
    archive: dict,
) -> dict:
    """Validate the exact terminal archive state and all closed authorities."""
    if not isinstance(archive, dict):
        raise PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(
            "archive must be an object"
        )
    expected = _base_archive()
    for field, value in expected.items():
        if archive.get(field) != value:
            raise PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(
                f"{field} mismatch"
            )

    checklist = archive.get("archive_checklist")
    expected_checklist = _checklist(archive)
    if checklist != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(
            "archive checklist mismatch"
        )
    if archive.get("archive_summary") != _summary(expected_checklist):
        raise PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(
            "archive summary mismatch"
        )
    digest = archive.get(
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(
            "archive digest missing"
        )
    expected_digest = predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest_v1(
        archive
    )
    if digest != expected_digest:
        raise PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(
            "archive digest mismatch"
        )
    return {
        "status": "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE_VALID",
        "artifact_kind": archive["artifact_kind"],
        "archive_status": archive["archive_status"],
        "archive_decision": archive["archive_decision"],
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest": digest,
        **{
            key: archive["archive_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_markdown_v1(
    archive: dict,
) -> str:
    """Render a sanitized Markdown view of the validated archive record."""
    validation = validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
        archive
    )
    sections = [
        ("Title", ["Predictive Usefulness Acceptance Path Archive Record Using Improved Evidence"]),
        (
            "Predictive Usefulness Acceptance Path Archive Record Using Improved Evidence",
            [
                f"Artifact/status/scope: `{archive['artifact_kind']}` / `{archive['archive_status']}` / `{archive['archive_scope']}`.",
                f"Digest: `{validation['predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest']}`.",
            ],
        ),
        (
            "Source Operator Selection",
            [
                f"Artifact/status: `{archive['source_operator_selection_artifact_kind']}` / `{archive['source_operator_selection_status']}`.",
                f"Option/decision/digest: `{archive['source_selected_option']}` / `{archive['source_selected_decision']}` / `{archive['source_operator_selection_digest']}`.",
            ],
        ),
        (
            "Source Closure",
            [
                f"Artifact/status: `{archive['source_closure_artifact_kind']}` / `{archive['source_closure_status']}`.",
                f"Decision/digest: `{archive['source_closure_decision']}` / `{archive['source_closure_digest']}`.",
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Readiness/reassessment/results review: `{archive['source_readiness_digest']}` / `{archive['source_reassessment_digest']}` / `{archive['source_results_review_digest']}`.",
                f"Matrix/features/labels: `{archive['feature_label_matrix_digest']}` / `{archive['feature_values_digest']}` / `{archive['redesigned_label_values_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"Dataset/records: `{archive['dataset_name']}` / `{archive['total_canonical_record_count']}`.",
                "Universe: " + ", ".join(f"`{ticker}`" for ticker in archive["target_universe"]) + ".",
                "META remains `913`; each non-META ticker remains `1003`.",
            ],
        ),
        (
            "Archive Decision",
            [
                f"Decision/classification: `{archive['archive_decision']}` / `{archive['archive_classification']}`.",
                f"Reason: `{archive['archive_reason']}`.",
            ],
        ),
        (
            "Archive Basis",
            [
                f"Selected option/readiness: `{archive['selected_option']}` / `{archive['readiness_decision']}`.",
                f"Closure: `{archive['closure_status']}`.",
            ],
        ),
        (
            "Evidence Summary",
            [
                f"Matrix/evaluable/unavailable/OOS: `{archive['matrix_row_count']} / {archive['evaluable_matrix_row_count']} / {archive['unavailable_target_count']} / {archive['oos_row_count']}`.",
                f"Majority/local/cross-sectional accuracy: `{archive['majority_accuracy']} / {archive['local_model_accuracy']} / {archive['cross_sectional_accuracy']}`.",
            ],
        ),
        (
            "Archived Options",
            [
                f"`{name}`: source `{value['source_status']}`, selection `{value['selection_status']}`, archive `{value['archive_status']}`."
                for name, value in archive["archived_options"].items()
            ],
        ),
        (
            "Per-Ticker Archive",
            [
                f"`{row['ticker']}`: `{row['archive_status']}`, records `{row['historical_record_count']}`, digest `{row['per_ticker_archive_record_digest']}`."
                for row in archive["per_ticker_archive_entries"]
            ],
        ),
        (
            "Future Reopen Conditions",
            [
                "No further action is required for the current path.",
                f"Future reopen status: `{archive['future_reopen_status']}`.",
            ],
        ),
        ("Next Chain", archive["next_chain"]),
        ("Next Gates", archive["next_gates"]),
        ("Risk Controls", archive["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate or ceremony exists."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{archive['archive_summary']['total_checks']} / {archive['archive_summary']['passed_checks']} / {archive['archive_summary']['failed_checks']} / {archive['archive_summary']['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            ["No future candidate, provider, acquisition, regeneration, evidence/reassessment/readiness rerun, recomputation, training, acceptance, runtime, broker, or trading action occurred."],
        ),
    ]
    lines = ["# Predictive Usefulness Acceptance Path Archive Record Using Improved Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical archive JSON without overwriting an existing record."""
    archive = build_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1()
    validation = validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
        archive
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1.json"
    if path.exists():
        raise PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError(
            "archive output already exists"
        )
    payload = canonical_json_bytes(archive)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": archive["artifact_kind"],
        "archive_status": archive["archive_status"],
        "archive_decision": archive["archive_decision"],
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest": validation[
            "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
