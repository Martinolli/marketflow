"""Offline predictive-usefulness acceptance-readiness review using improved evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_reassessment_rerun_using_improved_evidence_service as reassessment


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_V1 = (
    "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE"
)
READINESS_REASON = (
    "SMALL_CROSS_SECTIONAL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_AND_OPTIONAL_MODEL_COVERAGE_INCOMPLETE"
)
READINESS_DECISION_REASON = READINESS_REASON

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
SELECTED_DIRECTION = reassessment.SELECTED_DIRECTION

EXPECTED_REASSESSMENT_DIGEST = "1ccd45069f10284923c0ac2e93f02d0a5d787c78a1f9d7feb216855fd44356e5"
EXPECTED_RESULTS_REVIEW_DIGEST = reassessment.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = reassessment.EXPECTED_EXECUTION_DIGEST
EXPECTED_OUTPUT_BINDING_DIGEST = reassessment.EXPECTED_OUTPUT_BINDING_DIGEST
EXPECTED_APPROVAL_DIGEST = reassessment.EXPECTED_APPROVAL_DIGEST
EXPECTED_CANDIDATE_REVIEW_DIGEST = reassessment.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_CANDIDATE_DIGEST = reassessment.EXPECTED_CANDIDATE_DIGEST
EXPECTED_MATRIX_DIGEST = reassessment.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = reassessment.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = reassessment.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = reassessment.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = reassessment.EXPECTED_RECORDS_DIGEST
SOURCE_EVIDENCE = deepcopy(reassessment.SOURCE_EVIDENCE)

TARGET_UNIVERSE = list(reassessment.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(reassessment.EXPECTED_RECORD_COUNTS)

CRITERIA_POLICY = {
    "CRITERION_SOURCE_EVIDENCE_INTEGRITY": ("PASS", "All bound source digests match the reviewed evidence chain."),
    "CRITERION_REASSESSMENT_COMPLETED": ("PASS", "The source reassessment is completed and ready."),
    "CRITERION_LEAKAGE_CONTROLS": ("PASS", "Eight leakage controls passed with zero failures."),
    "CRITERION_OOS_PERFORMANCE_MATERIALITY": ("FAIL_OR_NOT_MET", "OOS evidence is not material enough for acceptance readiness."),
    "CRITERION_BASELINE_OUTPERFORMANCE_MATERIALITY": ("FAIL_OR_NOT_MET", "Baseline outperformance is not material enough for acceptance readiness."),
    "CRITERION_LOCAL_MODEL_OUTPERFORMANCE": ("FAIL_OR_NOT_MET", "The local model matches rather than outperforms the majority baseline."),
    "CRITERION_CROSS_SECTIONAL_EDGE_MATERIALITY": ("FAIL_OR_NOT_MET", "The 0.00309917 cross-sectional edge is too small for acceptance readiness."),
    "CRITERION_WALK_FORWARD_STABILITY": ("REQUIRES_OPERATOR_REVIEW", "Walk-forward stability requires operator review."),
    "CRITERION_CALIBRATION_AND_BRIER_SUPPORT": ("REQUIRES_OPERATOR_REVIEW", "The small Brier edge requires operator review."),
    "CRITERION_OPTIONAL_MODEL_COVERAGE": ("FAIL_OR_NOT_MET", "Optional tree and ensemble model families are unavailable."),
    "CRITERION_META_LIMITATION_AWARENESS": ("PASS_WITH_OPERATOR_AWARENESS", "META remains limited to 913 records."),
    "CRITERION_RESEARCH_ONLY_BOUNDARY": ("PASS", "The review remains research-only and non-actionable."),
    "CRITERION_PROFITABILITY_BOUNDARY": ("PASS", "Profitability remains not accepted."),
    "CRITERION_RUNTIME_BOUNDARY": ("PASS", "Runtime and trading authority remain closed."),
    "CRITERION_OPERATOR_BOUNDARY": ("PASS", "Operator review remains required."),
}

NEXT_CHAIN = [
    "Method or evidence improvement planning, if operator selects another improvement path.",
    "Additional evidence candidate, only after separate operator selection.",
    "Reassessment rerun, only if new evidence is created.",
    "Acceptance-readiness rerun, only after new reassessment.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "operator_method_or_evidence_improvement_selection_if_required",
    "method_or_evidence_improvement_candidate_if_selected",
    "improvement_operator_review",
    "improvement_approval_if_selected",
    "additional_evidence_execution_if_separately_approved",
    "predictive_usefulness_reassessment_rerun_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_new_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "readiness_review_does_not_accept_predictive_usefulness",
    "readiness_review_does_not_create_acceptance_candidate",
    "readiness_review_does_not_create_acceptance_ceremony",
    "readiness_review_does_not_accept_profitability",
    "readiness_review_does_not_authorize_runtime",
    "readiness_review_does_not_authorize_strategy",
    "readiness_review_does_not_authorize_paper_trading",
    "readiness_review_does_not_authorize_broker_execution",
    "readiness_review_does_not_generate_trade_recommendations",
    "readiness_review_does_not_regenerate_labels",
    "readiness_review_does_not_create_new_targets",
    "readiness_review_does_not_authorize_target_definition_change",
    "readiness_review_does_not_generate_features",
    "readiness_review_does_not_create_canonical_feature_label_matrix",
    "readiness_review_does_not_rerun_predictive_evidence",
    "readiness_review_does_not_rerun_reassessment",
    "readiness_review_does_not_recompute_metrics",
    "readiness_review_does_not_train_models",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_prior_predictive_evidence_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "do_not_mutate_current_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(ValueError):
    """Raised when the conservative readiness-review package is invalid."""


def _criteria() -> dict[str, dict[str, Any]]:
    return {
        criterion: {
            "criterion_id": criterion,
            "criterion_status": status,
            "evidence_summary": summary,
            "acceptance_evidence": False,
            "research_only": True,
            "non_actionable": True,
        }
        for criterion, (status, summary) in CRITERIA_POLICY.items()
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_predictive_usefulness_acceptance_readiness_digest", None)
    return payload


def per_ticker_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker readiness entry."""
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
            "predictive_usefulness_reassessment_status": "REASSESSED_RESEARCH_ONLY",
            "predictive_usefulness_acceptance_readiness_status": "NOT_READY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "label_regeneration_authorized": False,
            "new_targets_created": False,
            "feature_generation_authorized": False,
            "feature_label_matrix_created": False,
            "metric_recomputation_performed_in_readiness_review": False,
            "model_training_performed_in_readiness_review": False,
            "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
            "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
            "readiness_note": (
                "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_predictive_usefulness_acceptance_readiness_digest"] = (
            per_ticker_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_V1,
        "review_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "readiness_reason": READINESS_REASON,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_reassessment_artifact_kind": reassessment.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE,
        "source_reassessment_status": reassessment.PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE_READY,
        "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        **deepcopy(SOURCE_EVIDENCE),
        "predictive_usefulness_reassessment_using_improved_evidence_created": True,
        "predictive_usefulness_reassessment_using_improved_evidence_ready": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_improved_evidence": True,
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_created": True,
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_ready": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_ceremony_allowed": False,
        "additional_evidence_or_method_improvement_required": True,
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
        "metric_recomputation_performed_in_readiness_review": False,
        "model_training_performed_in_readiness_review": False,
        "provider_requests_made_in_readiness_review": False,
        "live_provider_transport_enabled_in_readiness_review": False,
        "market_data_acquisition_performed_in_readiness_review": False,
        "dataset_generation_performed_in_readiness_review": False,
        "canonical_dataset_regenerated_in_readiness_review": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "additional_predictive_evidence_execution_rerun_performed": False,
        "predictive_usefulness_reassessment_rerun_performed": False,
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
        "selected_redesign_direction": SELECTED_DIRECTION,
        "source_reassessment_ready": True,
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
        "readiness_classification": "COMPLETED_RESEARCH_ONLY",
        "predictive_signal_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "local_model_readiness": "NOT_READY",
        "cross_sectional_edge_readiness": "NOT_READY",
        "oos_performance_readiness": "NOT_READY",
        "walk_forward_readiness": "REQUIRES_OPERATOR_REVIEW",
        "calibration_brier_readiness": "REQUIRES_OPERATOR_REVIEW",
        "leakage_readiness": "PASS",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "acceptance_candidate_allowed": False,
        "acceptance_ceremony_allowed": False,
        "profitability_interpretation": "NOT_ACCEPTED",
        "runtime_interpretation": NOT_AUTHORIZED,
        "readiness_criteria": _criteria(),
        "per_ticker_readiness_entries": _per_ticker_entries(),
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
        isinstance(entry.get("per_ticker_predictive_usefulness_acceptance_readiness_digest"), str)
        and entry["per_ticker_predictive_usefulness_acceptance_readiness_digest"]
        == per_ticker_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(package: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    entries = package.get("per_ticker_readiness_entries", [])
    unavailable = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    return [
        ("source_reassessment_digest_bound", EXPECTED_REASSESSMENT_DIGEST, package.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, package.get("source_results_review_digest")),
        ("source_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, package.get("source_execution_digest")),
        ("source_output_binding_digest_bound", EXPECTED_OUTPUT_BINDING_DIGEST, package.get("source_output_binding_digest")),
        ("source_approval_digest_bound", EXPECTED_APPROVAL_DIGEST, package.get("source_approval_digest")),
        ("source_candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_DIGEST, package.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest")),
        ("source_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, package.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest")),
        ("planning_results_review_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_results_review_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_results_review_using_redesigned_evidence_digest")),
        ("planning_execution_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_execution_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_execution_using_redesigned_evidence_digest")),
        ("planning_output_binding_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_output_binding_digest"], package.get("improved_evidence_planning_output_binding_digest")),
        ("planning_approval_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_approval_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_approval_using_redesigned_evidence_digest")),
        ("redesign_results_review_digest_bound", SOURCE_EVIDENCE["label_objective_redesign_results_review_using_redesigned_evidence_digest"], package.get("label_objective_redesign_results_review_using_redesigned_evidence_digest")),
        ("redesign_execution_digest_bound", SOURCE_EVIDENCE["label_objective_redesign_execution_using_redesigned_evidence_digest"], package.get("label_objective_redesign_execution_using_redesigned_evidence_digest")),
        ("target_definition_results_review_digest_bound", SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], package.get("label_objective_target_definition_results_review_using_redesigned_evidence_digest")),
        ("target_definition_execution_digest_bound", SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], package.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest")),
        ("path_selection_digest_bound", SOURCE_EVIDENCE["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], package.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest")),
        ("prior_readiness_review_digest_bound", SOURCE_EVIDENCE["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], package.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest")),
        ("prior_reassessment_digest_bound", SOURCE_EVIDENCE["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], package.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest")),
        ("prior_predictive_results_review_digest_bound", SOURCE_EVIDENCE["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest")),
        ("prior_predictive_execution_digest_bound", SOURCE_EVIDENCE["additional_predictive_evidence_execution_using_redesigned_labels_digest"], package.get("additional_predictive_evidence_execution_using_redesigned_labels_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, package.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, package.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, package.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, package.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, package.get("target_universe")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("meta_913_preserved", 913, package.get("meta_record_count")),
        ("source_reassessment_ready_true", True, package.get("source_reassessment_ready")),
        ("readiness_review_created_true", True, package.get("predictive_usefulness_acceptance_readiness_using_improved_evidence_created")),
        ("readiness_review_completed_true", PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED, package.get("review_status")),
        ("readiness_ready_false", False, package.get("predictive_usefulness_acceptance_readiness_using_improved_evidence_ready")),
        ("readiness_decision_not_ready", PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE, package.get("readiness_decision")),
        ("acceptance_candidate_created_false", False, package.get("predictive_usefulness_acceptance_candidate_created")),
        ("acceptance_ceremony_allowed_false", False, package.get("predictive_usefulness_acceptance_ceremony_allowed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, package.get("predictive_usefulness")),
        ("acceptance_ready_false", False, package.get("predictive_usefulness_acceptance_ready")),
        ("acceptance_recommended_false", False, package.get("predictive_usefulness_acceptance_recommended")),
        ("profitability_not_accepted", NOT_ACCEPTED, package.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        ("trade_recommendations_false", False, package.get("trade_recommendations_generated")),
        ("label_regeneration_authorized_false", False, package.get("label_regeneration_authorized")),
        ("label_regeneration_performed_false", False, package.get("label_regeneration_performed")),
        ("new_targets_created_false", False, package.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, package.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, package.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, package.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, package.get("feature_label_matrix_created")),
        ("metric_recomputation_in_readiness_review_false", False, package.get("metric_recomputation_performed_in_readiness_review")),
        ("model_training_in_readiness_review_false", False, package.get("model_training_performed_in_readiness_review")),
        ("matrix_rows_preserved", 143352, package.get("matrix_row_count")),
        ("evaluable_rows_preserved", 142200, package.get("evaluable_matrix_row_count")),
        ("unavailable_targets_preserved", 1152, package.get("unavailable_target_count")),
        ("oos_rows_preserved", 34848, package.get("oos_row_count")),
        ("small_cross_sectional_edge_preserved", "0.00309917", package.get("cross_sectional_delta_vs_majority")),
        ("local_model_equivalence_preserved", package.get("majority_accuracy"), package.get("local_model_accuracy")),
        ("brier_values_preserved", ["0.04867526", "0.04867526", "0.04831065"], [package.get("majority_brier"), package.get("local_model_brier"), package.get("cross_sectional_brier")]),
        ("optional_models_unavailable_preserved", [unavailable, unavailable], [package.get("optional_tree_model_status"), package.get("optional_ensemble_model_status")]),
        ("leakage_controls_passed", [True, 0, 8], [package.get("leakage_control_passed"), package.get("leakage_failed_control_count"), package.get("leakage_control_count")]),
        ("meta_limitation_preserved", True, package.get("meta_reduced_record_count_preserved")),
        ("readiness_criteria_present", list(CRITERIA_POLICY), list(package.get("readiness_criteria", {}))),
        ("readiness_classification_conservative", "COMPLETED_RESEARCH_ONLY", package.get("readiness_classification")),
        ("acceptance_candidate_not_allowed", False, package.get("acceptance_candidate_allowed")),
        ("additional_evidence_required_true", True, package.get("additional_evidence_or_method_improvement_required")),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, package.get("provider_requests_made_in_readiness_review")),
        ("market_data_acquisition_false", False, package.get("market_data_acquisition_performed_in_readiness_review")),
        ("dataset_regeneration_false", False, package.get("canonical_dataset_regenerated_in_readiness_review")),
        ("redesigned_label_regeneration_false", False, package.get("redesigned_label_regeneration_performed")),
        ("feature_regeneration_false", False, package.get("feature_regeneration_performed")),
        ("predictive_evidence_rerun_false", False, package.get("additional_predictive_evidence_execution_rerun_performed")),
        ("reassessment_rerun_false", False, package.get("predictive_usefulness_reassessment_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
        ("next_chain_defined", NEXT_CHAIN, package.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, package.get("risk_controls")),
        ("no_tracked_marketflow_files", True, package.get("no_tracked_marketflow_files")),
    ]


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(check_id, expected, actual) for check_id, expected, actual in _check_definitions(package)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "readiness_review_completed": not failed,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "additional_evidence_or_method_improvement_required": True,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_readiness_review": False,
        "model_training_performed_in_readiness_review": False,
    }


def _digest_payload(package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(package))
    payload.pop("predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest", None)
    return payload


def predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest_v1(
    readiness_review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the readiness review."""
    return semantic_digest(_digest_payload(readiness_review))


def build_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1() -> dict:
    """Build the conservative offline readiness review from committed evidence."""
    package = _base_package()
    checklist = _checklist(package)
    package["readiness_checklist"] = checklist
    package["readiness_summary"] = _summary(checklist)
    package["predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"] = (
        predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest_v1(package)
    )
    validate_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(f"{field} must be false")


def validate_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(
    readiness_review: dict,
) -> dict:
    """Validate evidence bindings, not-ready findings, and closed authority gates."""
    if not isinstance(readiness_review, dict):
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
            "readiness review must be an object"
        )

    expected_fields = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_V1,
        "review_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "readiness_reason": READINESS_REASON,
        "source_reassessment_artifact_kind": reassessment.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE,
        "source_reassessment_status": reassessment.PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE_READY,
        "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
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
        "readiness_classification": "COMPLETED_RESEARCH_ONLY",
        "predictive_signal_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "local_model_readiness": "NOT_READY",
        "cross_sectional_edge_readiness": "NOT_READY",
        "oos_performance_readiness": "NOT_READY",
        "walk_forward_readiness": "REQUIRES_OPERATOR_REVIEW",
        "calibration_brier_readiness": "REQUIRES_OPERATOR_REVIEW",
        "leakage_readiness": "PASS",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "profitability_interpretation": "NOT_ACCEPTED",
        "runtime_interpretation": NOT_AUTHORIZED,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    expected_fields.update(SOURCE_EVIDENCE)
    for field, value in expected_fields.items():
        _expect(readiness_review.get(field), value, field)

    true_fields = (
        "created_offline",
        "research_only",
        "operator_review_required",
        "predictive_usefulness_reassessment_using_improved_evidence_created",
        "predictive_usefulness_reassessment_using_improved_evidence_ready",
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_improved_evidence",
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_created",
        "additional_evidence_or_method_improvement_required",
        "source_reassessment_ready",
        "leakage_control_passed",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(readiness_review.get(field), field)

    false_fields = (
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_ready",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_ceremony_allowed",
        "acceptance_candidate_allowed",
        "acceptance_ceremony_allowed",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "profitability_acceptance_created",
        "runtime_migration_approved",
        "runtime_migration_active",
        "runtime_migration_approval_created",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "metric_recomputation_performed_in_readiness_review",
        "model_training_performed_in_readiness_review",
        "provider_requests_made_in_readiness_review",
        "live_provider_transport_enabled_in_readiness_review",
        "market_data_acquisition_performed_in_readiness_review",
        "dataset_generation_performed_in_readiness_review",
        "canonical_dataset_regenerated_in_readiness_review",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
        "additional_predictive_evidence_execution_rerun_performed",
        "predictive_usefulness_reassessment_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    )
    for field in false_fields:
        _expect_false(readiness_review.get(field), field)

    criteria = readiness_review.get("readiness_criteria")
    if not isinstance(criteria, dict) or list(criteria) != list(CRITERIA_POLICY):
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
            "readiness criteria mismatch"
        )
    for criterion, (status, _) in CRITERIA_POLICY.items():
        value = criteria.get(criterion)
        if not isinstance(value, dict) or not value.get("evidence_summary"):
            raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
                f"{criterion} evidence missing"
            )
        _expect(value.get("criterion_id"), criterion, f"{criterion} criterion_id")
        _expect(value.get("criterion_status"), status, f"{criterion} criterion_status")
        _expect_false(value.get("acceptance_evidence"), f"{criterion} acceptance_evidence")
        _expect_true(value.get("research_only"), f"{criterion} research_only")
        _expect_true(value.get("non_actionable"), f"{criterion} non_actionable")

    entries = readiness_review.get("per_ticker_readiness_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
            "per-ticker readiness entries mismatch"
        )
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("predictive_usefulness_acceptance_readiness_status"), "NOT_READY", f"{ticker} readiness")
        _expect(entry.get("selected_redesign_direction"), SELECTED_DIRECTION, f"{ticker} direction")
        _expect(entry.get("source_reassessment_digest"), EXPECTED_REASSESSMENT_DIGEST, f"{ticker} reassessment")
        _expect(entry.get("source_results_review_digest"), EXPECTED_RESULTS_REVIEW_DIGEST, f"{ticker} results review")
        _expect(entry.get("predictive_usefulness"), NOT_ACCEPTED, f"{ticker} usefulness")
        _expect(entry.get("profitability"), NOT_ACCEPTED, f"{ticker} profitability")
        for field in (
            "predictive_usefulness_acceptance_ready",
            "predictive_usefulness_acceptance_candidate_created",
            "label_regeneration_authorized",
            "new_targets_created",
            "feature_generation_authorized",
            "feature_label_matrix_created",
            "metric_recomputation_performed_in_readiness_review",
            "model_training_performed_in_readiness_review",
        ):
            _expect_false(entry.get(field), f"{ticker} {field}")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        if ticker == "META":
            _expect(
                entry.get("readiness_note"),
                "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE",
                "META readiness_note",
            )
        digest = entry.get("per_ticker_predictive_usefulness_acceptance_readiness_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
                f"{ticker} per-ticker digest missing"
            )
        _expect(
            digest,
            per_ticker_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest_v1(entry),
            f"{ticker} per-ticker digest",
        )

    checklist = readiness_review.get("readiness_checklist")
    expected_check_ids = [definition[0] for definition in _check_definitions(readiness_review)]
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != expected_check_ids:
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
            "readiness checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
            "readiness checklist failed"
        )
    _expect(readiness_review.get("readiness_summary"), _summary(checklist), "readiness summary")

    digest = readiness_review.get(
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
            "readiness digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest_v1(
            readiness_review
        ),
        "readiness digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_VALID",
        "artifact_kind": readiness_review["artifact_kind"],
        "review_status": readiness_review["review_status"],
        "readiness_decision": readiness_review["readiness_decision"],
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": digest,
        **{
            key: readiness_review["readiness_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_markdown_v1(
    readiness_review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated readiness review."""
    validation = validate_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(
        readiness_review
    )
    sections = [
        ("Title", ["Predictive Usefulness Acceptance Readiness Review Using Improved Evidence"]),
        (
            "Predictive Usefulness Acceptance Readiness Review Using Improved Evidence",
            [
                f"Artifact/status: `{readiness_review['artifact_kind']}` / `{readiness_review['review_status']}`.",
                f"Digest: `{validation['predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest']}`.",
            ],
        ),
        (
            "Source Reassessment",
            [
                f"Artifact/status: `{readiness_review['source_reassessment_artifact_kind']}` / `{readiness_review['source_reassessment_status']}`.",
                f"Digest: `{readiness_review['source_reassessment_digest']}`.",
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Results review/execution/output binding: `{readiness_review['source_results_review_digest']}` / `{readiness_review['source_execution_digest']}` / `{readiness_review['source_output_binding_digest']}`.",
                f"Matrix/features/labels: `{readiness_review['feature_label_matrix_digest']}` / `{readiness_review['feature_values_digest']}` / `{readiness_review['redesigned_label_values_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"Dataset/records: `{readiness_review['dataset_name']}` / `{readiness_review['total_canonical_record_count']}`.",
                "Universe: " + ", ".join(f"`{ticker}`" for ticker in readiness_review["target_universe"]) + ".",
                "META remains `913`; each non-META ticker remains `1003`.",
            ],
        ),
        (
            "Evidence Summary",
            [
                f"Matrix/evaluable/unavailable/OOS: `{readiness_review['matrix_row_count']} / {readiness_review['evaluable_matrix_row_count']} / {readiness_review['unavailable_target_count']} / {readiness_review['oos_row_count']}`.",
                f"Majority/local/cross-sectional accuracy: `{readiness_review['majority_accuracy']} / {readiness_review['local_model_accuracy']} / {readiness_review['cross_sectional_accuracy']}`.",
            ],
        ),
        (
            "Readiness Decision",
            [
                f"Decision: `{readiness_review['readiness_decision']}`.",
                f"Reason: `{readiness_review['readiness_reason']}`.",
            ],
        ),
        (
            "Readiness Criteria",
            [
                f"`{name}`: `{value['criterion_status']}` — {value['evidence_summary']}"
                for name, value in readiness_review["readiness_criteria"].items()
            ],
        ),
        ("Predictive Signal Readiness", [f"`{readiness_review['predictive_signal_readiness']}`."]),
        ("Baseline Outperformance Readiness", [f"`{readiness_review['baseline_outperformance_readiness']}`."]),
        ("Local Model Readiness", [f"`{readiness_review['local_model_readiness']}`."]),
        ("Cross-Sectional Edge Readiness", [f"`{readiness_review['cross_sectional_edge_readiness']}`."]),
        ("OOS Readiness", [f"`{readiness_review['oos_performance_readiness']}`."]),
        ("Walk-Forward Readiness", [f"`{readiness_review['walk_forward_readiness']}`."]),
        (
            "Calibration / Brier Readiness",
            [
                f"`{readiness_review['calibration_brier_readiness']}`.",
                f"Majority/local/cross-sectional Brier: `{readiness_review['majority_brier']} / {readiness_review['local_model_brier']} / {readiness_review['cross_sectional_brier']}`.",
            ],
        ),
        (
            "Optional Model Coverage",
            [f"Tree/ensemble: `{readiness_review['optional_tree_model_status']}` / `{readiness_review['optional_ensemble_model_status']}`."],
        ),
        ("Leakage Readiness", [f"`{readiness_review['leakage_readiness']}`; eight controls and zero failures."]),
        ("META Readiness", [f"`{readiness_review['meta_readiness']}`; META remains at 913 records."]),
        (
            "Acceptance Boundary",
            ["Acceptance readiness is false. No acceptance candidate or ceremony is allowed or created."],
        ),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        (
            "Per-Ticker Readiness",
            [
                f"`{row['ticker']}`: readiness `{row['predictive_usefulness_acceptance_readiness_status']}`, records `{row['historical_record_count']}`, digest `{row['per_ticker_predictive_usefulness_acceptance_readiness_digest']}`."
                for row in readiness_review["per_ticker_readiness_entries"]
            ],
        ),
        ("Next Chain", readiness_review["next_chain"]),
        ("Next Gates", readiness_review["next_gates"]),
        ("Risk Controls", readiness_review["risk_controls"]),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{readiness_review['readiness_summary']['total_checks']} / {readiness_review['readiness_summary']['passed_checks']} / {readiness_review['readiness_summary']['failed_checks']} / {readiness_review['readiness_summary']['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            ["No provider, acquisition, regeneration, reassessment rerun, predictive rerun, metric recomputation, model training, acceptance, runtime, broker, or trading action occurred."],
        ),
    ]
    lines = ["# Predictive Usefulness Acceptance Readiness Review Using Improved Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical readiness-review JSON without overwriting an existing package."""
    package = build_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1()
    validation = validate_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(
        package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1.json"
    if path.exists():
        raise PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError(
            "readiness-review output already exists"
        )
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "readiness_decision": package["readiness_decision"],
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": validation[
            "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
