"""Offline terminal summary for the archived improved-evidence usefulness chain."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_acceptance_path_archive_record_improved_evidence_service as archive_service


ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE_V1 = (
    "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY"
)
CURRENT_IMPROVED_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED = (
    "CURRENT_IMPROVED_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED"
)
FINAL_REASON = (
    "CURRENT_IMPROVED_EVIDENCE_ARCHIVED_NOT_READY_SMALL_EDGE_LOCAL_MODEL_MATCHES_"
    "MAJORITY_OPTIONAL_MODEL_COVERAGE_INCOMPLETE"
)
FINAL_ARCHIVE_SUMMARY_ONLY = "FINAL_ARCHIVE_SUMMARY_ONLY"
FINAL_OUTCOME_REASON = "SMALL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_OPTIONAL_MODEL_COVERAGE_INCOMPLETE"

EXPECTED_ARCHIVE_DIGEST = "e38963a93be3518b531f60c55924b985d42761b60c07300450944b3e876dce99"
EXPECTED_SELECTION_DIGEST = archive_service.EXPECTED_SELECTION_DIGEST
EXPECTED_CLOSURE_DIGEST = archive_service.EXPECTED_CLOSURE_DIGEST
EXPECTED_READINESS_DIGEST = archive_service.EXPECTED_READINESS_DIGEST
EXPECTED_REASSESSMENT_DIGEST = archive_service.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = archive_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = archive_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_OUTPUT_BINDING_DIGEST = archive_service.EXPECTED_OUTPUT_BINDING_DIGEST
EXPECTED_MATRIX_DIGEST = archive_service.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = archive_service.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = archive_service.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = archive_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = archive_service.EXPECTED_RECORDS_DIGEST
SOURCE_EVIDENCE = deepcopy(archive_service.SOURCE_EVIDENCE)
TARGET_UNIVERSE = list(archive_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(archive_service.EXPECTED_RECORD_COUNTS)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

FINAL_PHASE_SUMMARY = [
    "Original predictive-evidence execution/review.",
    "Feature/label refinement planning, review, approval, execution, and review.",
    "Additional predictive evidence using refined evidence.",
    "Readiness review remained not ready.",
    "Method diagnostic and label objective redesign path.",
    "Redesigned label generation and results review.",
    "Feature generation using redesigned labels and review.",
    "Additional predictive evidence using redesigned labels and review.",
    "Readiness review remained not ready.",
    "Method/evidence improvement path using redesigned evidence.",
    "Label objective target-definition review and redesign execution.",
    "Improved evidence planning and review.",
    "Additional predictive evidence using improved evidence and review.",
    "Reassessment and acceptance-readiness review.",
    "Not-ready closure and method-planning tree.",
    "Operator selected Option A.",
    "Acceptance path archived as not ready.",
]
FUTURE_REOPEN_CONDITIONS = {
    "future_reopen_requires_new_operator_method_selection": True,
    "future_reopen_requires_new_method_or_objective_concept": True,
    "future_reopen_requires_separate_candidate_review_approval_execution_chain": True,
    "future_reopen_must_not_inherit_acceptance_authority": True,
    "future_runtime_requires_separate_authorization": True,
}
POSSIBLE_FUTURE_METHODS_IF_REOPENED = [
    "EXPECTANCY_FIRST_RESEARCH",
    "PAYOFF_ASYMMETRY_LABELS",
    "RISK_ADJUSTED_RETURN_OBJECTIVES",
    "BROADER_DATASET_OR_UNIVERSE_RESEARCH",
    "NEW_FEATURE_REVIEW",
    "MODEL_FAMILY_EXPANSION_AFTER_OBJECTIVE_REVIEW",
]
NEXT_CHAIN = [
    "No immediate next task required for the archived current path.",
    "Future research requires a new operator method-selection artifact if reopened.",
    "Any future evidence chain requires separate candidate, review, approval, execution, results review, reassessment, and readiness gates.",
    "Predictive usefulness acceptance candidate only if a future readiness review passes.",
    "Profitability review only after a separate predictive-usefulness acceptance chain.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "current_path_terminal_no_immediate_next_gate",
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
    "final_summary_does_not_create_future_method_candidate",
    "final_summary_does_not_create_future_evidence_candidate",
    "final_summary_does_not_accept_predictive_usefulness",
    "final_summary_does_not_create_acceptance_candidate",
    "final_summary_does_not_create_acceptance_ceremony",
    "final_summary_does_not_accept_profitability",
    "final_summary_does_not_authorize_runtime",
    "final_summary_does_not_authorize_strategy",
    "final_summary_does_not_authorize_paper_trading",
    "final_summary_does_not_authorize_broker_execution",
    "final_summary_does_not_generate_trade_recommendations",
    "final_summary_does_not_regenerate_labels",
    "final_summary_does_not_create_new_targets",
    "final_summary_does_not_authorize_target_definition_change",
    "final_summary_does_not_generate_features",
    "final_summary_does_not_create_canonical_feature_label_matrix",
    "final_summary_does_not_rerun_predictive_evidence",
    "final_summary_does_not_rerun_reassessment",
    "final_summary_does_not_rerun_readiness_review",
    "final_summary_does_not_recompute_metrics",
    "final_summary_does_not_train_models",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_prior_predictive_evidence_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "do_not_mutate_current_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(ValueError):
    """Raised when the final summary violates its terminal, non-actionable state."""


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_final_archive_summary_digest", None)
    return payload


def per_ticker_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker final-summary entry."""
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
            "final_chain_status": "ARCHIVED_NOT_READY",
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_archive_digest": EXPECTED_ARCHIVE_DIGEST,
            "source_selection_digest": EXPECTED_SELECTION_DIGEST,
            "source_readiness_digest": EXPECTED_READINESS_DIGEST,
            "final_summary_note": (
                "PRESERVE_META_LIMITATION_IN_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_final_archive_summary_digest"] = (
            per_ticker_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_summary() -> dict[str, Any]:
    final_outcome = {
        "final_chain_status": "ARCHIVED_NOT_READY",
        "final_predictive_usefulness_decision": "NOT_ACCEPTED",
        "final_acceptance_readiness_decision": "NOT_READY",
        "final_runtime_decision": NOT_AUTHORIZED,
        "final_profitability_decision": "NOT_ACCEPTED",
        "final_reason": FINAL_OUTCOME_REASON,
        "final_operator_selected_option": archive_service.selection.SELECTED_OPTION,
        "future_reopen_status": "REQUIRES_NEW_OPERATOR_METHOD_SELECTION",
        "recommended_future_research_direction_if_reopened": (
            "EXPECTANCY_FIRST_OR_NEW_OBJECTIVE_RESEARCH_OUTSIDE_ACCEPTANCE_CHAIN"
        ),
    }
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE_V1,
        "summary_status": MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY,
        "final_decision": CURRENT_IMPROVED_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED,
        "final_reason": FINAL_REASON,
        "summary_scope": FINAL_ARCHIVE_SUMMARY_ONLY,
        "created_offline": True,
        "research_only": True,
        "final_summary_record": True,
        "source_archive_artifact_kind": archive_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE,
        "source_archive_status": archive_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "source_archive_decision": archive_service.ARCHIVE_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH_NOT_READY,
        "source_archive_digest": EXPECTED_ARCHIVE_DIGEST,
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest": EXPECTED_ARCHIVE_DIGEST,
        "source_selection_digest": EXPECTED_SELECTION_DIGEST,
        "operator_method_or_closure_selection_using_improved_evidence_digest": EXPECTED_SELECTION_DIGEST,
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
        "marketflow_predictive_usefulness_final_archive_summary_created": True,
        "current_improved_evidence_predictive_usefulness_chain_finalized": True,
        "current_improved_evidence_predictive_usefulness_chain_archived_not_ready": True,
        "future_research_requires_new_method_concept": True,
        "new_method_selection_created": False,
        "new_method_candidate_created": False,
        "new_evidence_candidate_created": False,
        "new_evidence_execution_created": False,
        "new_reassessment_created": False,
        "new_readiness_review_created": False,
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
        "metric_recomputation_performed_in_final_summary": False,
        "model_training_performed_in_final_summary": False,
        "provider_requests_made_in_final_summary": False,
        "live_provider_transport_enabled_in_final_summary": False,
        "market_data_acquisition_performed_in_final_summary": False,
        "dataset_generation_performed_in_final_summary": False,
        "canonical_dataset_regenerated_in_final_summary": False,
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
        **{key: value for key, value in final_outcome.items() if key != "final_reason"},
        "final_outcome_reason": FINAL_OUTCOME_REASON,
        "final_outcome_classification": final_outcome,
        "final_phase_summary": list(FINAL_PHASE_SUMMARY),
        "future_reopen_conditions": deepcopy(FUTURE_REOPEN_CONDITIONS),
        "possible_future_methods_only_if_reopened": list(POSSIBLE_FUTURE_METHODS_IF_REOPENED),
        "per_ticker_final_summary_entries": _per_ticker_entries(),
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
        and isinstance(entry.get("per_ticker_final_archive_summary_digest"), str)
        and entry["per_ticker_final_archive_summary_digest"]
        == per_ticker_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(summary: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    entries = summary.get("per_ticker_final_summary_entries", [])
    unavailable = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    return [
        ("source_archive_digest_bound", EXPECTED_ARCHIVE_DIGEST, summary.get("source_archive_digest")),
        ("source_selection_digest_bound", EXPECTED_SELECTION_DIGEST, summary.get("source_selection_digest")),
        ("source_closure_digest_bound", EXPECTED_CLOSURE_DIGEST, summary.get("source_closure_digest")),
        ("source_readiness_digest_bound", EXPECTED_READINESS_DIGEST, summary.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", EXPECTED_REASSESSMENT_DIGEST, summary.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, summary.get("source_results_review_digest")),
        ("source_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, summary.get("source_execution_digest")),
        ("source_output_binding_digest_bound", EXPECTED_OUTPUT_BINDING_DIGEST, summary.get("source_output_binding_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, summary.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, summary.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, summary.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, summary.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, summary.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, summary.get("target_universe")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, summary.get("records_digest")),
        ("meta_913_preserved", 913, summary.get("meta_record_count")),
        ("final_summary_created_true", True, summary.get("marketflow_predictive_usefulness_final_archive_summary_created")),
        ("current_chain_finalized_true", True, summary.get("current_improved_evidence_predictive_usefulness_chain_finalized")),
        ("current_chain_archived_not_ready_true", True, summary.get("current_improved_evidence_predictive_usefulness_chain_archived_not_ready")),
        ("future_research_requires_new_method_concept_true", True, summary.get("future_research_requires_new_method_concept")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, summary.get("predictive_usefulness")),
        ("acceptance_ready_false", False, summary.get("predictive_usefulness_acceptance_ready")),
        ("acceptance_recommended_false", False, summary.get("predictive_usefulness_acceptance_recommended")),
        ("acceptance_candidate_created_false", False, summary.get("predictive_usefulness_acceptance_candidate_created")),
        ("acceptance_ceremony_allowed_false", False, summary.get("predictive_usefulness_acceptance_ceremony_allowed")),
        ("profitability_not_accepted", NOT_ACCEPTED, summary.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, summary.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, summary.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, summary.get("broker_execution")),
        ("trade_recommendations_false", False, summary.get("trade_recommendations_generated")),
        ("label_regeneration_authorized_false", False, summary.get("label_regeneration_authorized")),
        ("label_regeneration_performed_false", False, summary.get("label_regeneration_performed")),
        ("new_targets_created_false", False, summary.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, summary.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, summary.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, summary.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, summary.get("feature_label_matrix_created")),
        ("metric_recomputation_in_final_summary_false", False, summary.get("metric_recomputation_performed_in_final_summary")),
        ("model_training_in_final_summary_false", False, summary.get("model_training_performed_in_final_summary")),
        ("predictive_evidence_rerun_false", False, summary.get("additional_predictive_evidence_execution_rerun_performed")),
        ("reassessment_rerun_false", False, summary.get("predictive_usefulness_reassessment_rerun_performed")),
        ("readiness_rerun_false", False, summary.get("predictive_usefulness_acceptance_readiness_rerun_performed")),
        ("matrix_rows_preserved", 143352, summary.get("matrix_row_count")),
        ("small_cross_sectional_edge_preserved", "0.00309917", summary.get("cross_sectional_delta_vs_majority")),
        ("local_model_equivalence_preserved", summary.get("majority_accuracy"), summary.get("local_model_accuracy")),
        ("optional_models_unavailable_preserved", [unavailable, unavailable], [summary.get("optional_tree_model_status"), summary.get("optional_ensemble_model_status")]),
        ("leakage_controls_passed", [True, 0, 8], [summary.get("leakage_control_passed"), summary.get("leakage_failed_control_count"), summary.get("leakage_control_count")]),
        ("meta_limitation_preserved", True, summary.get("meta_reduced_record_count_preserved")),
        ("final_phase_summary_present", FINAL_PHASE_SUMMARY, summary.get("final_phase_summary")),
        ("future_reopen_conditions_present", FUTURE_REOPEN_CONDITIONS, summary.get("future_reopen_conditions")),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, summary.get("provider_requests_made_in_final_summary")),
        ("market_data_acquisition_false", False, summary.get("market_data_acquisition_performed_in_final_summary")),
        ("dataset_regeneration_false", False, summary.get("canonical_dataset_regenerated_in_final_summary")),
        ("raw_provider_payloads_not_committed", False, summary.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, summary.get("api_keys_stored_or_printed")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, summary.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, summary.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, summary.get("runtime_migration_approval_created")),
        ("next_chain_terminal_current_path", NEXT_CHAIN, summary.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, summary.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, summary.get("risk_controls")),
        ("no_tracked_marketflow_files", True, summary.get("no_tracked_marketflow_files")),
    ]


def _checklist(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(summary)]


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
        "final_summary_created": True,
        "current_improved_evidence_predictive_usefulness_chain_finalized": True,
        "current_improved_evidence_predictive_usefulness_chain_archived_not_ready": True,
        "final_predictive_usefulness_decision": "NOT_ACCEPTED",
        "final_runtime_decision": NOT_AUTHORIZED,
        "future_research_requires_new_method_concept": True,
        "future_reopen_requires_new_operator_method_selection": True,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(summary: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(summary))
    payload.pop("final_summary_checklist", None)
    payload.pop("final_summary_summary", None)
    payload.pop("marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest", None)
    return payload


def marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest_v1(
    summary: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the final archive summary."""
    return semantic_digest(_digest_payload(summary))


def build_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1() -> dict:
    """Build the terminal summary without providers, execution, or mutation."""
    summary = _base_summary()
    checklist = _checklist(summary)
    summary["final_summary_checklist"] = checklist
    summary["final_summary_summary"] = _summary(checklist)
    summary["marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"] = (
        marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest_v1(summary)
    )
    validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(summary)
    return summary


def validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
    summary: dict,
) -> dict:
    """Validate exact source bindings, terminal state, and closed authorities."""
    if not isinstance(summary, dict):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(
            "summary must be an object"
        )
    expected = _base_summary()
    for field, value in expected.items():
        if summary.get(field) != value:
            raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(
                f"{field} mismatch"
            )
    checklist = summary.get("final_summary_checklist")
    expected_checklist = _checklist(summary)
    if checklist != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(
            "final summary checklist mismatch"
        )
    if summary.get("final_summary_summary") != _summary(expected_checklist):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(
            "final summary totals mismatch"
        )
    digest = summary.get(
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(
            "final summary digest missing"
        )
    expected_digest = marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest_v1(
        summary
    )
    if digest != expected_digest:
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(
            "final summary digest mismatch"
        )
    return {
        "status": "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE_VALID",
        "artifact_kind": summary["artifact_kind"],
        "summary_status": summary["summary_status"],
        "final_decision": summary["final_decision"],
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest": digest,
        **{
            key: summary["final_summary_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_markdown_v1(
    summary: dict,
) -> str:
    """Render a sanitized Markdown view of the validated final summary."""
    validation = validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
        summary
    )
    sections = [
        ("Title", ["MarketFlow Predictive Usefulness Final Archive Summary Using Improved Evidence"]),
        (
            "MarketFlow Predictive Usefulness Final Archive Summary Using Improved Evidence",
            [
                f"Artifact/status/scope: `{summary['artifact_kind']}` / `{summary['summary_status']}` / `{summary['summary_scope']}`.",
                f"Digest: `{validation['marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest']}`.",
            ],
        ),
        (
            "Source Archive Record",
            [
                f"Artifact/status: `{summary['source_archive_artifact_kind']}` / `{summary['source_archive_status']}`.",
                f"Decision/digest: `{summary['source_archive_decision']}` / `{summary['source_archive_digest']}`.",
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Selection/closure/readiness: `{summary['source_selection_digest']}` / `{summary['source_closure_digest']}` / `{summary['source_readiness_digest']}`.",
                f"Matrix/features/labels: `{summary['feature_label_matrix_digest']}` / `{summary['feature_values_digest']}` / `{summary['redesigned_label_values_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"Dataset/records: `{summary['dataset_name']}` / `{summary['total_canonical_record_count']}`.",
                "Universe: " + ", ".join(f"`{ticker}`" for ticker in summary["target_universe"]) + ".",
                "META remains `913`; each non-META ticker remains `1003`.",
            ],
        ),
        (
            "Final Decision",
            [
                f"Decision: `{summary['final_decision']}`.",
                f"Reason: `{summary['final_reason']}`.",
            ],
        ),
        (
            "Final Evidence Summary",
            [
                f"Matrix/evaluable/unavailable/OOS: `{summary['matrix_row_count']} / {summary['evaluable_matrix_row_count']} / {summary['unavailable_target_count']} / {summary['oos_row_count']}`.",
                f"Majority/local/cross-sectional accuracy: `{summary['majority_accuracy']} / {summary['local_model_accuracy']} / {summary['cross_sectional_accuracy']}`.",
            ],
        ),
        (
            "Final Outcome Classification",
            [f"`{key}`: `{value}`." for key, value in summary["final_outcome_classification"].items()],
        ),
        ("Completed Phase Summary", summary["final_phase_summary"]),
        (
            "Per-Ticker Final Summary",
            [
                f"`{row['ticker']}`: `{row['final_chain_status']}`, records `{row['historical_record_count']}`, digest `{row['per_ticker_final_archive_summary_digest']}`."
                for row in summary["per_ticker_final_summary_entries"]
            ],
        ),
        (
            "Future Reopen Conditions",
            [f"`{key}`: `{value}`." for key, value in summary["future_reopen_conditions"].items()]
            + ["Possible methods: " + ", ".join(f"`{method}`" for method in summary["possible_future_methods_only_if_reopened"]) + "."],
        ),
        ("Next Chain", summary["next_chain"]),
        ("Next Gates", summary["next_gates"]),
        ("Risk Controls", summary["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate or ceremony exists."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{summary['final_summary_summary']['total_checks']} / {summary['final_summary_summary']['passed_checks']} / {summary['final_summary_summary']['failed_checks']} / {summary['final_summary_summary']['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            ["No new method/evidence candidate, provider, acquisition, regeneration, evidence/reassessment/readiness rerun, recomputation, training, acceptance, runtime, broker, or trading action occurred."],
        ),
    ]
    lines = ["# MarketFlow Predictive Usefulness Final Archive Summary Using Improved Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical summary JSON without overwriting an existing record."""
    summary = build_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1()
    validation = validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
        summary
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1.json"
    if path.exists():
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError(
            "final summary output already exists"
        )
    payload = canonical_json_bytes(summary)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": summary["artifact_kind"],
        "summary_status": summary["summary_status"],
        "final_decision": summary["final_decision"],
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest": validation[
            "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
