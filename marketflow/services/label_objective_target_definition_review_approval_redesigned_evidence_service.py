"""Attestation-gated offline approval of future label-objective review execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import label_objective_target_definition_review_candidate_redesigned_evidence_operator_review_service as review_service


ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_USING_REDESIGNED_EVIDENCE_V1 = (
    "label_objective_target_definition_review_approval_using_redesigned_evidence_v1"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY"
)
OPERATOR_DECISION = "APPROVE_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_USING_REDESIGNED_EVIDENCE"
OPERATOR_ATTESTATION_VERSION = (
    "label_objective_target_definition_review_approval_using_redesigned_evidence_attestation_v1"
)
REQUIRED_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE LABEL OBJECTIVE TARGET DEFINITION REVIEW USING REDESIGNED EVIDENCE "
    "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY"
)

EXPECTED_CANDIDATE_REVIEW_DIGEST = (
    "ebf9f1dddddc37167c457c64f28baab021b50249987e888e1ea0a31c78102d45"
)
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_PATH_SELECTION_DIGEST = review_service.EXPECTED_PATH_SELECTION_DIGEST
EXPECTED_METHOD_EVIDENCE_CANDIDATE_REVIEW_DIGEST = review_service.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_METHOD_EVIDENCE_CANDIDATE_DIGEST = review_service.EXPECTED_METHOD_EVIDENCE_CANDIDATE_DIGEST
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
SELECTED_OPTION = review_service.SELECTED_OPTION
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

SOURCE_REVIEW_ARTIFACT_KIND = (
    review_service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE
)
SOURCE_REVIEW_STATUS = (
    review_service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY
)
SOURCE_CANDIDATE_ARTIFACT_KIND = review_service.SOURCE_CANDIDATE_ARTIFACT_KIND
SOURCE_CANDIDATE_STATUS = review_service.SOURCE_CANDIDATE_STATUS
REVIEW_DIMENSION_IDS = list(review_service.REVIEW_DIMENSION_IDS)
LABEL_FAMILY_IDS = list(review_service.LABEL_FAMILY_IDS)
DIAGNOSTIC_QUESTIONS = list(review_service.DIAGNOSTIC_QUESTIONS)
DECISION_OPTION_IDS = list(review_service.DECISION_OPTION_IDS)

APPROVED_FUTURE_OUTPUT_NAMES = [
    "label_objective_target_definition_review_execution_manifest",
    "current_label_family_objective_map",
    "target_definition_vs_majority_structure_report",
    "cross_sectional_edge_materiality_report",
    "horizon_noise_review_report",
    "threshold_materiality_review_report",
    "class_balance_target_distribution_report",
    "per_ticker_target_behavior_report",
    "meta_target_behavior_report",
    "target_decision_options_report",
    "operator_review_summary",
    "digest_manifest",
]
NEXT_CHAIN = [
    "Label Objective / Target Definition Review Execution Using Redesigned Evidence v1.",
    "Label Objective / Target Definition Results Review Using Redesigned Evidence v1.",
    "Optional label objective redesign or threshold/horizon refinement candidate, if review supports it.",
    "Optional improved evidence planning and execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "label_objective_target_definition_review_execution_using_redesigned_evidence",
    "label_objective_target_definition_results_review_using_redesigned_evidence",
    "label_objective_redesign_or_threshold_horizon_refinement_candidate_if_supported",
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
    "approval_does_not_execute_label_objective_review_now",
    "approval_does_not_regenerate_labels",
    "approval_does_not_create_new_targets",
    "approval_does_not_authorize_target_definition_change",
    "approval_does_not_generate_new_evidence",
    "approval_does_not_rerun_predictive_evidence",
    "approval_does_not_retrain_models",
    "approval_does_not_recompute_metrics",
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
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_DIGESTS = {
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
    "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": EXPECTED_PATH_SELECTION_DIGEST,
    "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_METHOD_EVIDENCE_CANDIDATE_REVIEW_DIGEST,
    "method_evidence_improvement_candidate_using_redesigned_evidence_digest": EXPECTED_METHOD_EVIDENCE_CANDIDATE_DIGEST,
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
    "operator_confirms_approval_scope_only", "operator_confirms_review_authorized",
    "operator_confirms_ready_for_review_execution", "operator_confirms_no_review_execution",
    "operator_confirms_no_label_regeneration", "operator_confirms_no_new_targets",
    "operator_confirms_no_target_definition_change_authorization",
    "operator_confirms_no_predictive_evidence_rerun", "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training", "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance", "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_strategy_authorization", "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution", "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing", "operator_confirms_no_raw_payload_commit",
]

CHECK_IDS = [
    "candidate_review_digest_bound", "candidate_digest_bound", "path_selection_digest_bound",
    "readiness_review_digest_bound", "reassessment_digest_bound", "results_review_digest_bound",
    "execution_digest_bound", "matrix_digest_bound", "feature_values_digest_bound",
    "label_values_digest_bound", "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "target_universe_matches_review_universe",
    "records_digest_preserved", "meta_913_preserved", "operator_decision_matches",
    "operator_attestation_phrase_matches", "selected_option_is_option_a", "approval_scope_only",
    "label_objective_target_definition_review_approved_true",
    "label_objective_target_definition_review_approval_created_true",
    "label_objective_target_definition_review_authorized_true", "ready_for_review_execution_true",
    "review_executed_false", "label_regeneration_authorized_false",
    "label_regeneration_performed_false", "target_definition_change_authorized_false",
    "new_targets_created_false", "predictive_usefulness_not_accepted", "acceptance_ready_false",
    "acceptance_candidate_created_false", "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "approved_problem_basis_preserved", "approved_review_objective_defined", "approved_dimensions_12",
    "approved_label_family_review_plan_10", "approved_diagnostic_questions_10",
    "approved_decision_options_7", "approved_future_outputs", "per_ticker_approval_entries_12",
    "per_ticker_approval_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_approval_false",
    "model_training_in_approval_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "no_label_objective_review_execution_created",
    "no_label_objective_redesign_candidate_created", "no_threshold_horizon_refinement_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created", "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(ValueError):
    """Raised when approval violates its attestation or approval-only scope."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(
            f"{field} mismatch"
        )


def build_label_objective_target_definition_review_approval_using_redesigned_evidence_attestation_v1(
    *, operator_reference: str, operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str, operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str, operator_confirms_path_selection_digest: str,
    operator_confirms_readiness_review_digest: str, operator_confirms_reassessment_digest: str,
    operator_confirms_results_review_digest: str, operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str], operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int, operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_option: str, operator_confirms_approval_scope_only: bool,
    operator_confirms_review_authorized: bool, operator_confirms_ready_for_review_execution: bool,
    operator_confirms_no_review_execution: bool, operator_confirms_no_label_regeneration: bool,
    operator_confirms_no_new_targets: bool,
    operator_confirms_no_target_definition_change_authorization: bool,
    operator_confirms_no_predictive_evidence_rerun: bool,
    operator_confirms_no_metric_recomputation: bool, operator_confirms_no_model_training: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool, operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool, operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build the non-secret operator attestation for the approval ceremony."""
    attestation = {key: value for key, value in locals().items()}
    attestation["operator_confirms_target_universe"] = list(operator_confirms_target_universe)
    attestation["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    return attestation


def _validate_attestation(attestation: Any) -> None:
    if not isinstance(attestation, dict):
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(
            "operator attestation missing"
        )
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "operator_attestation_phrase": REQUIRED_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_path_selection_digest": EXPECTED_PATH_SELECTION_DIGEST,
        "operator_confirms_readiness_review_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        "operator_confirms_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "operator_confirms_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        "operator_confirms_target_universe": EXPECTED_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_option": SELECTED_OPTION,
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, f"operator attestation {field}")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(
                f"operator attestation {field} missing"
            )
    _expect(attestation.get("operator_attestation_version"), OPERATOR_ATTESTATION_VERSION, "operator attestation version")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        _expect(attestation.get(field), True, f"operator attestation {field}")


def _source_review(candidate_review_package: dict | None) -> dict[str, Any]:
    source = (
        review_service.build_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1()
        if candidate_review_package is None else deepcopy(candidate_review_package)
    )
    review_service.validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(source)
    _expect(
        source.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"),
        EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "source candidate review digest",
    )
    return source


def _approved_dimensions() -> list[dict[str, Any]]:
    return [{
        "dimension_id": item, "approval_status": "APPROVED_FOR_FUTURE_REVIEW_EXECUTION_ONLY",
        "execution_performed": False, "label_regeneration_authorized": False,
        "target_definition_change_authorized": False, "research_only": True, "non_actionable": True,
    } for item in REVIEW_DIMENSION_IDS]


def _approved_label_families() -> list[dict[str, Any]]:
    return [{
        "label_family": item, "approval_status": "APPROVED_FOR_FUTURE_REVIEW_EXECUTION_ONLY",
        "review_execution_authorized": True, "review_execution_performed": False,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "target_definition_change_authorized": False, "target_definition_change_performed": False,
        "research_only": True, "non_actionable": True,
    } for item in LABEL_FAMILY_IDS]


def _approved_questions() -> list[dict[str, Any]]:
    return [{
        "question": item, "approval_status": "APPROVED_FOR_FUTURE_REVIEW_EXECUTION_ONLY",
        "question_answered": False, "execution_performed": False,
        "research_only": True, "non_actionable": True,
    } for item in DIAGNOSTIC_QUESTIONS]


def _approved_options() -> list[dict[str, Any]]:
    return [{
        "decision_option": item, "approval_status": "APPROVED_FOR_FUTURE_REVIEW_CONSIDERATION_ONLY",
        "selected": False, "approved_for_target_change": False, "executed": False,
        "creates_new_labels": False, "research_only": True, "non_actionable": True,
    } for item in DECISION_OPTION_IDS]


def _approved_outputs() -> list[dict[str, Any]]:
    return [{
        "output_name": item, "output_status": "AUTHORIZED_NOT_GENERATED",
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
    } for item in APPROVED_FUTURE_OUTPUT_NAMES]


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_label_objective_target_definition_review_approval_digest", None)
    return payload


def per_ticker_label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker approval entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_review_entries"]:
        ticker = row["ticker"]
        entry = {
            "ticker": ticker, "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "path_selection_status": "SELECTED_OPTION_A_FOR_NEXT_CANDIDATE_ONLY",
            "label_objective_target_definition_review_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "label_objective_target_definition_review_approval_status": "APPROVED_FOR_FUTURE_RESEARCH_REVIEW_EXECUTION_ONLY",
            "label_objective_target_definition_review_authorized": True,
            "label_objective_target_definition_review_executed": False,
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "target_definition_change_authorized": False, "new_targets_created": False,
            "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_label_objective_target_definition_review_candidate_review_digest": row["per_ticker_label_objective_target_definition_review_candidate_review_digest"],
            "source_label_objective_target_definition_review_candidate_digest": row["per_ticker_label_objective_target_definition_review_candidate_digest"],
        }
        if ticker == "META":
            entry["approval_note"] = "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL"
        entry["per_ticker_label_objective_target_definition_review_approval_digest"] = (
            per_ticker_label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_approval(source: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_USING_REDESIGNED_EVIDENCE_V1,
        "approval_status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE,
        "approval_scope": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_candidate_review_artifact_kind": SOURCE_REVIEW_ARTIFACT_KIND,
        "source_candidate_review_status": SOURCE_REVIEW_STATUS,
        "source_candidate_artifact_kind": SOURCE_CANDIDATE_ARTIFACT_KIND,
        "source_candidate_status": SOURCE_CANDIDATE_STATUS,
        **REQUIRED_DIGESTS,
        "method_evidence_improvement_path_selected": True,
        "method_evidence_improvement_path_selection_created": True,
        "selected_method_evidence_improvement_option": SELECTED_OPTION,
        "ready_for_label_objective_target_definition_review_candidate_using_redesigned_evidence": True,
        "label_objective_target_definition_review_candidate_created": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_created": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_created": True,
        "label_objective_target_definition_review_approved": True,
        "label_objective_target_definition_review_approval_created": True,
        "label_objective_target_definition_review_authorized": True,
        "ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence": True,
        "label_objective_target_definition_review_executed": False,
        "label_objective_target_definition_review_execution_created": False,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "label_objective_redesign_candidate_created": False,
        "threshold_horizon_refinement_candidate_created": False,
        "improved_evidence_planning_candidate_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False, "profitability_acceptance_created": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_migration_approval_created": False, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "automatic_stitching": False,
        "new_strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "provider_requests_made_in_approval": False, "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "redesigned_label_regeneration_performed": False, "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "metric_recomputation_performed_in_approval": False,
        "model_training_performed_in_approval": False, "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": source["dataset_name"], "source_profile": source["source_profile"],
        "timeframe": source["timeframe"], "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"], "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "meta_record_count": source["meta_record_count"], "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source["meta_reduced_record_count_preserved"],
        "approved_problem_basis": deepcopy(source["reviewed_problem_basis"]),
        "label_objective_target_definition_review_objective": "REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION_AFTER_NOT_READY_REDESIGNED_EVIDENCE_DECISION",
        "label_objective_target_definition_review_scope": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY,
        "label_objective_target_definition_review_mode": "AUTHORIZED_NOT_EXECUTED",
        "label_objective_target_definition_review_authority_status": "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_REVIEW_EXECUTION",
        "approved_dimensions": _approved_dimensions(),
        "approved_label_family_review_plan": _approved_label_families(),
        "approved_diagnostic_questions": _approved_questions(),
        "approved_decision_options": _approved_options(),
        "approved_future_outputs": _approved_outputs(),
        "per_ticker_approval_entries": _per_ticker_entries(source),
        "next_chain": deepcopy(NEXT_CHAIN), "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": expected, "actual": actual,
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    attestation = approval.get("operator_attestation", {})
    dimensions = approval.get("approved_dimensions", [])
    families = approval.get("approved_label_family_review_plan", [])
    questions = approval.get("approved_diagnostic_questions", [])
    options = approval.get("approved_decision_options", [])
    outputs = approval.get("approved_future_outputs", [])
    entries = approval.get("per_ticker_approval_entries", [])
    source = _source_review(None)
    actuals = {
        "candidate_review_digest_bound": approval.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"),
        "candidate_digest_bound": approval.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"),
        "path_selection_digest_bound": approval.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
        "readiness_review_digest_bound": approval.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": approval.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "results_review_digest_bound": approval.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": approval.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": approval.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": approval.get("feature_values_digest"),
        "label_values_digest_bound": approval.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": approval.get("research_registry_approval_digest"),
        "records_digest_bound": approval.get("records_digest"),
        "target_universe_12_preserved": approval.get("target_universe_count"),
        "target_universe_matches_review_universe": approval.get("target_universe"),
        "records_digest_preserved": approval.get("records_digest"), "meta_913_preserved": approval.get("meta_record_count"),
        "operator_decision_matches": attestation.get("operator_decision"),
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase"),
        "selected_option_is_option_a": approval.get("selected_method_evidence_improvement_option"),
        "approval_scope_only": approval.get("approval_scope"),
        "label_objective_target_definition_review_approved_true": approval.get("label_objective_target_definition_review_approved"),
        "label_objective_target_definition_review_approval_created_true": approval.get("label_objective_target_definition_review_approval_created"),
        "label_objective_target_definition_review_authorized_true": approval.get("label_objective_target_definition_review_authorized"),
        "ready_for_review_execution_true": approval.get("ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence"),
        "review_executed_false": approval.get("label_objective_target_definition_review_executed"),
        "label_regeneration_authorized_false": approval.get("label_regeneration_authorized"),
        "label_regeneration_performed_false": approval.get("label_regeneration_performed"),
        "target_definition_change_authorized_false": approval.get("target_definition_change_authorized"),
        "new_targets_created_false": approval.get("new_targets_created"),
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness"),
        "acceptance_ready_false": approval.get("predictive_usefulness_acceptance_ready"),
        "acceptance_candidate_created_false": approval.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": approval.get("profitability"), "runtime_not_authorized": approval.get("runtime_use"),
        "strategy_not_authorized": approval.get("strategy_use"), "broker_not_authorized": approval.get("broker_execution"),
        "trade_recommendations_false": approval.get("trade_recommendations_generated"),
        "approved_problem_basis_preserved": approval.get("approved_problem_basis"),
        "approved_review_objective_defined": [approval.get("label_objective_target_definition_review_objective"), approval.get("label_objective_target_definition_review_scope"), approval.get("label_objective_target_definition_review_mode"), approval.get("label_objective_target_definition_review_authority_status")],
        "approved_dimensions_12": [row.get("dimension_id") for row in dimensions],
        "approved_label_family_review_plan_10": [row.get("label_family") for row in families],
        "approved_diagnostic_questions_10": [row.get("question") for row in questions],
        "approved_decision_options_7": [row.get("decision_option") for row in options],
        "approved_future_outputs": [row.get("output_name") for row in outputs],
        "per_ticker_approval_entries_12": len(entries),
        "per_ticker_approval_digests_present": all(isinstance(row.get("per_ticker_label_objective_target_definition_review_approval_digest"), str) and len(row["per_ticker_label_objective_target_definition_review_approval_digest"]) == 64 for row in entries),
        "provider_requests_made_false": approval.get("provider_requests_made_in_approval"),
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed_in_approval"),
        "dataset_regeneration_false": approval.get("canonical_dataset_regenerated_in_approval"),
        "redesigned_label_regeneration_false": approval.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": approval.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": approval.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_approval_false": approval.get("metric_recomputation_performed_in_approval"),
        "model_training_in_approval_false": approval.get("model_training_performed_in_approval"),
        "raw_provider_payloads_not_committed": approval.get("raw_provider_payloads_committed"),
        "api_keys_not_stored_or_printed": approval.get("api_keys_stored_or_printed"),
        "no_label_objective_review_execution_created": approval.get("label_objective_target_definition_review_execution_created"),
        "no_label_objective_redesign_candidate_created": approval.get("label_objective_redesign_candidate_created"),
        "no_threshold_horizon_refinement_candidate_created": approval.get("threshold_horizon_refinement_candidate_created"),
        "no_predictive_usefulness_acceptance_artifact_created": approval.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": approval.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": approval.get("runtime_migration_approval_created"),
        "next_chain_defined": approval.get("next_chain"), "next_gates_defined": approval.get("next_gates"),
        "risk_controls_defined": approval.get("risk_controls"), "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files"),
    }
    expected = {
        "candidate_review_digest_bound": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "candidate_digest_bound": EXPECTED_CANDIDATE_DIGEST, "path_selection_digest_bound": EXPECTED_PATH_SELECTION_DIGEST,
        "readiness_review_digest_bound": EXPECTED_READINESS_REVIEW_DIGEST,
        "reassessment_digest_bound": EXPECTED_REASSESSMENT_DIGEST, "results_review_digest_bound": EXPECTED_RESULTS_REVIEW_DIGEST,
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST, "matrix_digest_bound": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest_bound": EXPECTED_FEATURE_VALUES_DIGEST, "label_values_digest_bound": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": EXPECTED_RESEARCH_REGISTRY_DIGEST, "records_digest_bound": EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": 12, "target_universe_matches_review_universe": EXPECTED_TARGET_UNIVERSE,
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST, "meta_913_preserved": 913,
        "operator_decision_matches": OPERATOR_DECISION,
        "operator_attestation_phrase_matches": REQUIRED_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ATTESTATION_PHRASE,
        "selected_option_is_option_a": SELECTED_OPTION, "approval_scope_only": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY,
        "label_objective_target_definition_review_approved_true": True,
        "label_objective_target_definition_review_approval_created_true": True,
        "label_objective_target_definition_review_authorized_true": True, "ready_for_review_execution_true": True,
        "review_executed_false": False, "label_regeneration_authorized_false": False,
        "label_regeneration_performed_false": False, "target_definition_change_authorized_false": False,
        "new_targets_created_false": False, "predictive_usefulness_not_accepted": NOT_ACCEPTED,
        "acceptance_ready_false": False, "acceptance_candidate_created_false": False,
        "profitability_not_accepted": NOT_ACCEPTED, "runtime_not_authorized": NOT_AUTHORIZED,
        "strategy_not_authorized": NOT_AUTHORIZED, "broker_not_authorized": NOT_AUTHORIZED,
        "trade_recommendations_false": False, "approved_problem_basis_preserved": source["reviewed_problem_basis"],
        "approved_review_objective_defined": ["REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION_AFTER_NOT_READY_REDESIGNED_EVIDENCE_DECISION", LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY, "AUTHORIZED_NOT_EXECUTED", "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_REVIEW_EXECUTION"],
        "approved_dimensions_12": REVIEW_DIMENSION_IDS, "approved_label_family_review_plan_10": LABEL_FAMILY_IDS,
        "approved_diagnostic_questions_10": DIAGNOSTIC_QUESTIONS, "approved_decision_options_7": DECISION_OPTION_IDS,
        "approved_future_outputs": APPROVED_FUTURE_OUTPUT_NAMES, "per_ticker_approval_entries_12": 12,
        "per_ticker_approval_digests_present": True, "provider_requests_made_false": False,
        "market_data_acquisition_false": False, "dataset_regeneration_false": False,
        "redesigned_label_regeneration_false": False, "feature_regeneration_false": False,
        "predictive_evidence_rerun_false": False, "metric_recomputation_in_approval_false": False,
        "model_training_in_approval_false": False, "raw_provider_payloads_not_committed": False,
        "api_keys_not_stored_or_printed": False, "no_label_objective_review_execution_created": False,
        "no_label_objective_redesign_candidate_created": False, "no_threshold_horizon_refinement_candidate_created": False,
        "no_predictive_usefulness_acceptance_artifact_created": False, "no_profitability_acceptance_created": False,
        "no_runtime_migration_approval_created": False, "next_chain_defined": NEXT_CHAIN,
        "next_gates_defined": NEXT_GATES, "risk_controls_defined": RISK_CONTROLS,
        "no_tracked_marketflow_files": True,
    }
    return [_check(check_id, expected[check_id], actuals[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist); passed = sum(row.get("status") == PASS for row in rows); failed = len(rows) - passed
    blockers = sum(row.get("status") == FAIL and row.get("severity") == BLOCKER for row in rows)
    return {
        "total_checks": len(rows), "passed_checks": passed, "failed_checks": failed, "blocker_count": blockers,
        "label_objective_target_definition_review_approved_by_operator": True,
        "approval_scope": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY,
        "label_objective_target_definition_review_authorized": True,
        "ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence": True,
        "label_objective_target_definition_review_executed": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "trade_recommendations_generated": False,
    }


def _digest_payload(approval: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(approval)); payload.pop("label_objective_target_definition_review_approval_using_redesigned_evidence_digest", None); return payload


def label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic approval digest."""
    return semantic_digest(_digest_payload(approval))


def build_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
    *, candidate_review_package: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build approval for future review execution after strict attestation checks."""
    _validate_attestation(operator_attestation)
    source = _source_review(candidate_review_package)
    approval = _base_approval(source, operator_attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"] = (
        label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(approval)
    )
    validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(approval)
    return approval


def _reject_forbidden_authority(value: Any, *, path: str = "approval") -> None:
    forbidden_true_fields = {
        "label_objective_target_definition_review_executed", "label_objective_target_definition_review_execution_created",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "label_objective_redesign_candidate_created", "threshold_horizon_refinement_candidate_created",
        "improved_evidence_planning_candidate_created", "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed", "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "profitability_acceptance_created",
        "runtime_migration_approved", "runtime_migration_active", "runtime_migration_approval_created",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_approval", "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval", "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_approval", "model_training_performed_in_approval",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "approved_for_target_change",
        "executed", "creates_new_labels", "question_answered", "execution_performed",
        "review_execution_performed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(f"{current} must remain false")
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(f"{current} must not be AUTHORIZED")
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(f"{current} must not be accepted")
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value): _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
    approval: dict,
) -> dict:
    """Validate the exact attestation, approval bindings, and closed downstream authority."""
    if not isinstance(approval, dict):
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError("approval must be an object")
    _reject_forbidden_authority(approval); _validate_attestation(approval.get("operator_attestation"))
    source = _source_review(None); expected_base = _base_approval(source, approval["operator_attestation"])
    for field, value in expected_base.items(): _expect(approval.get(field), value, field)
    entries = approval.get("per_ticker_approval_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError("per-ticker approval entries mismatch")
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]; _expect(row.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(row.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        digest = row.get("per_ticker_label_objective_target_definition_review_approval_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError(f"{ticker} approval digest missing")
        _expect(digest, per_ticker_label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(row), f"{ticker} approval digest")
    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError("approval checklist missing")
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "approval checklist IDs")
    expected_checklist = _checklist(approval); _expect(checklist, expected_checklist, "approval checklist")
    if any(row["status"] != PASS for row in checklist):
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError("approval checklist failed")
    _expect(approval.get("approval_summary"), _summary(checklist), "approval summary")
    digest = approval.get("label_objective_target_definition_review_approval_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError("approval digest missing")
    _expect(digest, label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(approval), "approval digest")
    return {"status": "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_USING_REDESIGNED_EVIDENCE_VALID",
            "artifact_kind": approval["artifact_kind"], "approval_status": approval["approval_status"],
            "approval_scope": approval["approval_scope"],
            "label_objective_target_definition_review_approval_using_redesigned_evidence_digest": digest,
            **{key: approval["approval_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def build_label_objective_target_definition_review_approved_using_redesigned_evidence_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view of the validated approval."""
    validation = validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(approval)
    attestation = approval["operator_attestation"]; summary = approval["approval_summary"]
    sections = [
        ("Title", ["Label Objective / Target Definition Review Approval Using Redesigned Evidence"]),
        ("Label Objective / Target Definition Review Approval Using Redesigned Evidence", [f"Artifact/status/scope: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}`.", f"Digest: `{validation['label_objective_target_definition_review_approval_using_redesigned_evidence_digest']}`."]),
        ("Operator Attestation", [f"Reference/timestamp/version: `{attestation['operator_reference']}` / `{attestation['operator_attestation_timestamp_utc']}` / `{attestation['operator_attestation_version']}`.", f"Decision: `{attestation['operator_decision']}`."]),
        ("Source Candidate Review", [f"Artifact/status: `{approval['source_candidate_review_artifact_kind']}` / `{approval['source_candidate_review_status']}`.", f"Digest: `{approval['label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest']}`."]),
        ("Bound Evidence", [f"`{field}`: `{digest}`." for field, digest in REQUIRED_DIGESTS.items()]),
        ("Dataset and Universe", [f"Dataset/profile/timeframe: `{approval['dataset_name']}` / `{approval['source_profile']}` / `{approval['timeframe']}`.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in approval["target_universe"]) + ".", "META remains `913`; every other ticker remains `1003`."]),
        ("Approved Problem Basis", [f"`{key}`: `{value}`." for key, value in approval["approved_problem_basis"].items()]),
        ("Approved Review Objective", [f"Objective: `{approval['label_objective_target_definition_review_objective']}`.", f"Scope/mode/authority: `{approval['label_objective_target_definition_review_scope']}` / `{approval['label_objective_target_definition_review_mode']}` / `{approval['label_objective_target_definition_review_authority_status']}`."]),
        ("Approved Dimensions", [f"`{row['dimension_id']}`: `{row['approval_status']}`." for row in approval["approved_dimensions"]]),
        ("Approved Label Family Review Plan", [f"`{row['label_family']}`: `{row['approval_status']}`." for row in approval["approved_label_family_review_plan"]]),
        ("Approved Diagnostic Questions", [f"`{row['question']}`: `{row['approval_status']}`." for row in approval["approved_diagnostic_questions"]]),
        ("Approved Decision Options", [f"`{row['decision_option']}`: `{row['approval_status']}`; selected `{row['selected']}`." for row in approval["approved_decision_options"]]),
        ("Approved Future Outputs", [f"`{row['output_name']}`: `{row['output_status']}` / `{row['output_label']}`." for row in approval["approved_future_outputs"]]),
        ("Per-Ticker Approval Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, status `{row['label_objective_target_definition_review_approval_status']}`, digest `{row['per_ticker_label_objective_target_definition_review_approval_digest']}`." for row in approval["per_ticker_approval_entries"]]),
        ("Next Chain", approval["next_chain"]), ("Next Gates", approval["next_gates"]),
        ("Risk Controls", approval["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate was created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`."]),
        ("Guardrails", ["This approval authorizes only future research review execution. It does not execute review, regenerate labels, create targets, authorize target changes, accept usefulness or profitability, or authorize runtime or trading."]),
    ]
    lines = ["# Label Objective / Target Definition Review Approval Using Redesigned Evidence", ""]
    for title, rows in sections: lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
    output_dir: str | Path, *, candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
        candidate_review_package=candidate_review_package, operator_attestation=operator_attestation)
    validation = validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(approval)
    directory = Path(output_dir); directory.mkdir(parents=True, exist_ok=True)
    path = directory / "label_objective_target_definition_review_approval_using_redesigned_evidence_v1.json"
    if path.exists():
        raise LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError("approval output already exists")
    payload = canonical_json_bytes(approval)
    with path.open("xb") as handle: handle.write(payload)
    return validation | {"path": str(path).replace("\\", "/"), "payload_byte_size": len(payload), "payload_sha256": sha256_bytes(payload)}
