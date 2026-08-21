"""Attestation-gated approval of future research-only label-objective redesign."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import label_objective_redesign_candidate_redesigned_evidence_operator_review_service as review_service


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_USING_REDESIGNED_EVIDENCE_V1 = (
    "label_objective_redesign_approval_using_redesigned_evidence_v1"
)
LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE"
)
LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY = "LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY"
SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION = (
    "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS"
)
OPERATOR_DECISION = "APPROVE_LABEL_OBJECTIVE_REDESIGN_USING_REDESIGNED_EVIDENCE"
OPERATOR_ATTESTATION_VERSION = (
    "label_objective_redesign_approval_using_redesigned_evidence_attestation_v1"
)
REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE LABEL OBJECTIVE REDESIGN USING REDESIGNED EVIDENCE "
    "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS MSFT NVDA AMZN GOOGL "
    "META TSLA JPM XOM JNJ WMT CAT LMT LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY"
)

EXPECTED_CANDIDATE_REVIEW_DIGEST = "66ef0356d4bb73fe405db5e56cfa8ab10d499fc842d2906e3aeaf56c85df2494"
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
SOURCE_REVIEW_ARTIFACT_KIND = review_service.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE
SOURCE_REVIEW_STATUS = review_service.LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY
SOURCE_CANDIDATE_ARTIFACT_KIND = review_service.SOURCE_CANDIDATE_ARTIFACT_KIND
SOURCE_CANDIDATE_STATUS = review_service.SOURCE_CANDIDATE_STATUS
SOURCE_EVIDENCE = deepcopy(review_service.SOURCE_EVIDENCE)
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review_service.EXPECTED_RECORD_COUNTS)
CANDIDATE_BASIS = deepcopy(review_service.CANDIDATE_BASIS)
REDESIGN_THEME_IDS = list(review_service.REDESIGN_THEME_IDS)
REDESIGN_OPTION_IDS = list(review_service.REDESIGN_OPTION_IDS)
LABEL_FAMILIES = list(review_service.LABEL_FAMILIES)
REDESIGN_QUESTIONS = list(review_service.REDESIGN_QUESTIONS)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED

APPROVED_FUTURE_OUTPUT_NAMES = [
    "label_objective_redesign_execution_manifest",
    "flat_class_and_majority_structure_redesign_report",
    "no_trade_abstain_objective_report", "material_move_target_definition_report",
    "horizon_specific_target_design_report", "ticker_or_regime_split_target_report",
    "risk_adjusted_target_definition_report", "label_family_impact_review_report",
    "meta_target_limitation_review_report", "acceptance_threshold_prerequisite_report",
    "operator_review_summary", "digest_manifest",
]
NEXT_CHAIN = [
    "Optional Label Objective Redesign Execution Using Redesigned Evidence v1.",
    "Optional Label Objective Redesign Results Review Using Redesigned Evidence v1.",
    "Optional improved evidence planning candidate, if redesign results support it.",
    "Optional improved evidence execution approval and execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "label_objective_redesign_execution_using_redesigned_evidence_if_approved",
    "label_objective_redesign_results_review_using_redesigned_evidence",
    "improved_evidence_planning_candidate_if_supported", "improved_evidence_execution_approval_if_required",
    "improved_evidence_execution_if_approved", "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready", "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_execute_redesign_now", "approval_does_not_regenerate_labels",
    "approval_does_not_create_new_targets", "approval_does_not_authorize_operational_target_definition_change",
    "approval_does_not_create_threshold_horizon_refinement_candidate",
    "approval_does_not_generate_new_evidence_now", "approval_does_not_rerun_predictive_evidence",
    "approval_does_not_retrain_models", "approval_does_not_recompute_metrics",
    "approval_does_not_accept_predictive_usefulness", "approval_does_not_create_acceptance_candidate",
    "approval_does_not_accept_profitability", "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy", "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution", "approval_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset", "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs", "do_not_mutate_predictive_evidence_outputs",
    "do_not_mutate_label_objective_review_outputs", "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_approval_scope_only", "operator_confirms_redesign_authorized",
    "operator_confirms_ready_for_redesign_execution", "operator_confirms_no_redesign_execution",
    "operator_confirms_no_label_regeneration", "operator_confirms_no_new_targets",
    "operator_confirms_no_target_definition_change_authorization",
    "operator_confirms_no_threshold_horizon_refinement_candidate",
    "operator_confirms_no_predictive_evidence_rerun", "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training", "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance", "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_strategy_authorization", "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution", "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing", "operator_confirms_no_raw_payload_commit",
]
CHECK_IDS = [
    "candidate_review_digest_bound", "candidate_digest_bound", "results_review_digest_bound",
    "execution_digest_bound", "output_binding_digest_bound", "approval_digest_bound",
    "candidate_review_target_definition_digest_bound", "path_selection_digest_bound",
    "readiness_review_digest_bound", "reassessment_digest_bound", "predictive_results_review_digest_bound",
    "predictive_execution_digest_bound", "matrix_digest_bound", "feature_values_digest_bound",
    "label_values_digest_bound", "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "target_universe_matches_review_universe",
    "records_digest_preserved", "meta_913_preserved", "operator_decision_matches",
    "operator_attestation_phrase_matches", "recommended_redesign_direction_confirmed",
    "selected_redesign_direction_matches_recommendation", "approval_scope_only",
    "label_objective_redesign_approved_true", "label_objective_redesign_approval_created_true",
    "label_objective_redesign_authorized_true", "ready_for_redesign_execution_true",
    "redesign_executed_false", "label_regeneration_authorized_false",
    "label_regeneration_performed_false", "new_targets_created_false",
    "target_definition_change_authorized_false", "target_definition_change_performed_false",
    "threshold_horizon_refinement_candidate_created_false", "improved_evidence_planning_candidate_created_false",
    "predictive_usefulness_not_accepted", "acceptance_ready_false", "acceptance_candidate_created_false",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "approved_candidate_basis_preserved",
    "approved_redesign_objective_defined", "approved_redesign_direction_selected",
    "only_recommended_option_selected", "approved_redesign_themes_11",
    "approved_label_family_impact_review_10", "approved_redesign_questions_10",
    "approved_future_outputs", "per_ticker_approval_entries_12", "per_ticker_approval_digests_present",
    "provider_requests_made_false", "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false", "predictive_evidence_rerun_false",
    "label_objective_review_execution_rerun_false", "metric_recomputation_in_approval_false",
    "model_training_in_approval_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "no_label_objective_redesign_execution_created",
    "no_threshold_horizon_refinement_candidate_created", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class LabelObjectiveRedesignApprovalRedesignedEvidenceError(ValueError):
    """Raised when approval violates the exact attestation or approval-only scope."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError(f"{field} mismatch")


def build_label_objective_redesign_approval_using_redesigned_evidence_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_results_review_digest: str,
    operator_confirms_execution_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_recommended_redesign_direction: str,
    operator_confirms_selected_redesign_direction: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_redesign_authorized: bool,
    operator_confirms_ready_for_redesign_execution: bool,
    operator_confirms_no_redesign_execution: bool,
    operator_confirms_no_label_regeneration: bool,
    operator_confirms_no_new_targets: bool,
    operator_confirms_no_target_definition_change_authorization: bool,
    operator_confirms_no_threshold_horizon_refinement_candidate: bool,
    operator_confirms_no_predictive_evidence_rerun: bool,
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
    selected_redesign_direction: str = SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    attestation = {key: value for key, value in locals().items()}
    attestation["operator_confirms_target_universe"] = list(operator_confirms_target_universe)
    attestation["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    return attestation


def _validate_attestation(attestation: Any) -> None:
    if not isinstance(attestation, dict):
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError("operator attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "operator_attestation_phrase": REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_results_review_digest": SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"],
        "operator_confirms_execution_digest": SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"],
        "operator_confirms_records_digest": SOURCE_EVIDENCE["records_digest"],
        "operator_confirms_target_universe": TARGET_UNIVERSE, "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913, "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_recommended_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "operator_confirms_selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, f"operator attestation {field}")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise LabelObjectiveRedesignApprovalRedesignedEvidenceError(f"operator attestation {field} missing")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        _expect(attestation.get(field), True, f"operator attestation {field}")


def _source_review(candidate_review_package: dict | None) -> dict[str, Any]:
    source = (
        review_service.build_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1()
        if candidate_review_package is None else deepcopy(candidate_review_package)
    )
    review_service.validate_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(source)
    _expect(source.get("label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"), EXPECTED_CANDIDATE_REVIEW_DIGEST, "source candidate review digest")
    return source


def _approved_options() -> list[dict[str, Any]]:
    rows = []
    for option in REDESIGN_OPTION_IDS:
        selected = option == SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION
        rows.append({
            "redesign_option": option, "selected_for_approval": selected,
            "approval_status": (
                "APPROVED_FOR_FUTURE_RESEARCH_ONLY_REDESIGN_EXECUTION"
                if selected else "NOT_SELECTED_FOR_APPROVAL"
            ),
            "execution_performed": False, "label_regeneration_authorized": False,
            "target_definition_change_authorized": False, "creates_new_labels": False,
            "creates_new_targets": False, "research_only": True, "non_actionable": True,
        })
    return rows


def _approved_themes() -> list[dict[str, Any]]:
    return [{
        "theme": theme, "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_REDESIGN_REVIEW_ONLY",
        "execution_performed": False, "label_regeneration_authorized": False,
        "target_definition_change_authorized": False, "research_only": True, "non_actionable": True,
    } for theme in REDESIGN_THEME_IDS]


def _approved_families() -> list[dict[str, Any]]:
    return [{
        "label_family": family, "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_IMPACT_REVIEW_ONLY",
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "target_definition_change_authorized": False, "target_definition_change_performed": False,
        "research_only": True, "non_actionable": True,
    } for family in LABEL_FAMILIES]


def _approved_questions() -> list[dict[str, Any]]:
    return [{
        "question": question, "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_REDESIGN_REVIEW_ONLY",
        "question_answered": False, "execution_performed": False,
        "research_only": True, "non_actionable": True,
    } for question in REDESIGN_QUESTIONS]


def _approved_outputs() -> list[dict[str, Any]]:
    return [{
        "output_name": name, "output_status": "AUTHORIZED_NOT_GENERATED",
        "output_scope": "RESEARCH_ONLY_NON_ACTIONABLE",
    } for name in APPROVED_FUTURE_OUTPUT_NAMES]


def per_ticker_label_objective_redesign_approval_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_label_objective_redesign_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_review_entries"]:
        ticker = row["ticker"]
        entry = {
            "ticker": ticker, "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN", "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "label_objective_target_definition_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "label_objective_redesign_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "label_objective_redesign_approval_status": "APPROVED_FOR_FUTURE_RESEARCH_REDESIGN_EXECUTION_ONLY",
            "selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
            "label_objective_redesign_authorized": True, "label_objective_redesign_executed": False,
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "new_targets_created": False, "target_definition_change_authorized": False,
            "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False, "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "source_label_objective_redesign_candidate_review_digest": row["per_ticker_label_objective_redesign_candidate_review_digest"],
            "source_label_objective_redesign_candidate_digest": row["per_ticker_label_objective_redesign_candidate_digest"],
        }
        if ticker == "META":
            entry["approval_note"] = "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_REDESIGN_APPROVAL"
        entry["per_ticker_label_objective_redesign_approval_digest"] = (
            per_ticker_label_objective_redesign_approval_using_redesigned_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_approval(source: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    approval = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_USING_REDESIGNED_EVIDENCE_V1,
        "approval_status": LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE,
        "approval_scope": LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_candidate_review_artifact_kind": SOURCE_REVIEW_ARTIFACT_KIND,
        "source_candidate_review_status": SOURCE_REVIEW_STATUS,
        "source_candidate_artifact_kind": SOURCE_CANDIDATE_ARTIFACT_KIND,
        "source_candidate_status": SOURCE_CANDIDATE_STATUS,
        "label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "label_objective_redesign_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **deepcopy(SOURCE_EVIDENCE),
        "source_candidate_review_target_universe": deepcopy(source["target_universe"]),
        "label_objective_target_definition_results_review_created": True,
        "label_objective_target_definition_results_review_ready": True,
        "ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence": True,
        "label_objective_redesign_candidate_created": True,
        "label_objective_redesign_candidate_using_redesigned_evidence_created": True,
        "label_objective_redesign_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "label_objective_redesign_candidate_using_redesigned_evidence_review_created": True,
        "label_objective_redesign_approved": True, "label_objective_redesign_approval_created": True,
        "label_objective_redesign_authorized": True,
        "ready_for_label_objective_redesign_execution_using_redesigned_evidence": True,
        "selected_label_objective_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "recommended_redesign_direction_selected_for_approval": True,
        "label_objective_redesign_executed": False, "label_objective_redesign_execution_created": False,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "threshold_horizon_refinement_candidate_created": False,
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
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "metric_recomputation_performed_in_approval": False,
        "model_training_performed_in_approval": False, "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": source["dataset_name"], "source_profile": source["source_profile"],
        "timeframe": source["timeframe"], "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"], "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"], "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source["meta_reduced_record_count_preserved"],
        "approved_candidate_basis": deepcopy(source["reviewed_candidate_basis"]),
        "label_objective_redesign_objective": "PREPARE_OPTIONAL_RESEARCH_ONLY_LABEL_OBJECTIVE_REDESIGN_AFTER_FLAT_CLASS_AND_MAJORITY_STRUCTURE_REVIEW",
        "label_objective_redesign_scope": LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY,
        "label_objective_redesign_mode": "AUTHORIZED_NOT_EXECUTED",
        "label_objective_redesign_authority_status": "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_REDESIGN_EXECUTION",
        "approved_redesign_options": _approved_options(), "approved_redesign_themes": _approved_themes(),
        "approved_label_family_impact_review": _approved_families(),
        "approved_redesign_questions": _approved_questions(),
        "approved_future_outputs": _approved_outputs(),
        "per_ticker_approval_entries": _per_ticker_entries(source),
        "next_chain": deepcopy(NEXT_CHAIN), "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }
    return approval


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = "PASS" if actual == expected else "FAIL"
    return {"check_id": check_id, "status": status, "expected": expected, "actual": actual,
            "severity": "BLOCKER", "message": f"{check_id} {'passed' if status == 'PASS' else 'failed'}"}


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    attestation = approval.get("operator_attestation", {})
    options = approval.get("approved_redesign_options", [])
    themes = approval.get("approved_redesign_themes", [])
    families = approval.get("approved_label_family_impact_review", [])
    questions = approval.get("approved_redesign_questions", [])
    outputs = approval.get("approved_future_outputs", [])
    entries = approval.get("per_ticker_approval_entries", [])
    actuals = {
        "candidate_review_digest_bound": approval.get("label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"),
        "candidate_digest_bound": approval.get("label_objective_redesign_candidate_using_redesigned_evidence_digest"),
        "results_review_digest_bound": approval.get("label_objective_target_definition_results_review_using_redesigned_evidence_digest"),
        "execution_digest_bound": approval.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest"),
        "output_binding_digest_bound": approval.get("label_objective_target_definition_review_output_binding_digest"),
        "approval_digest_bound": approval.get("label_objective_target_definition_review_approval_using_redesigned_evidence_digest"),
        "candidate_review_target_definition_digest_bound": approval.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"),
        "path_selection_digest_bound": approval.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
        "readiness_review_digest_bound": approval.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": approval.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "predictive_results_review_digest_bound": approval.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "predictive_execution_digest_bound": approval.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": approval.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": approval.get("feature_values_digest"),
        "label_values_digest_bound": approval.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": approval.get("research_registry_approval_digest"),
        "records_digest_bound": approval.get("records_digest"),
        "target_universe_12_preserved": approval.get("target_universe_count"),
        "target_universe_matches_review_universe": approval.get("target_universe") == approval.get("source_candidate_review_target_universe"),
        "records_digest_preserved": approval.get("records_digest"), "meta_913_preserved": approval.get("meta_record_count"),
        "operator_decision_matches": attestation.get("operator_decision"),
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase"),
        "recommended_redesign_direction_confirmed": attestation.get("operator_confirms_recommended_redesign_direction"),
        "selected_redesign_direction_matches_recommendation": approval.get("selected_label_objective_redesign_direction"),
        "approval_scope_only": approval.get("approval_scope"),
        "label_objective_redesign_approved_true": approval.get("label_objective_redesign_approved"),
        "label_objective_redesign_approval_created_true": approval.get("label_objective_redesign_approval_created"),
        "label_objective_redesign_authorized_true": approval.get("label_objective_redesign_authorized"),
        "ready_for_redesign_execution_true": approval.get("ready_for_label_objective_redesign_execution_using_redesigned_evidence"),
        "redesign_executed_false": approval.get("label_objective_redesign_executed"),
        "label_regeneration_authorized_false": approval.get("label_regeneration_authorized"),
        "label_regeneration_performed_false": approval.get("label_regeneration_performed"),
        "new_targets_created_false": approval.get("new_targets_created"),
        "target_definition_change_authorized_false": approval.get("target_definition_change_authorized"),
        "target_definition_change_performed_false": approval.get("target_definition_change_performed"),
        "threshold_horizon_refinement_candidate_created_false": approval.get("threshold_horizon_refinement_candidate_created"),
        "improved_evidence_planning_candidate_created_false": approval.get("improved_evidence_planning_candidate_created"),
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness"),
        "acceptance_ready_false": approval.get("predictive_usefulness_acceptance_ready"),
        "acceptance_candidate_created_false": approval.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": approval.get("profitability"), "runtime_not_authorized": approval.get("runtime_use"),
        "strategy_not_authorized": approval.get("strategy_use"), "broker_not_authorized": approval.get("broker_execution"),
        "trade_recommendations_false": approval.get("trade_recommendations_generated"),
        "approved_candidate_basis_preserved": approval.get("approved_candidate_basis"),
        "approved_redesign_objective_defined": [approval.get("label_objective_redesign_objective"), approval.get("label_objective_redesign_scope"), approval.get("label_objective_redesign_mode"), approval.get("label_objective_redesign_authority_status")],
        "approved_redesign_direction_selected": approval.get("selected_label_objective_redesign_direction"),
        "only_recommended_option_selected": [row.get("redesign_option") for row in options if row.get("selected_for_approval")],
        "approved_redesign_themes_11": [row.get("theme") for row in themes],
        "approved_label_family_impact_review_10": [row.get("label_family") for row in families],
        "approved_redesign_questions_10": [row.get("question") for row in questions],
        "approved_future_outputs": [row.get("output_name") for row in outputs],
        "per_ticker_approval_entries_12": len(entries),
        "per_ticker_approval_digests_present": all(row.get("per_ticker_label_objective_redesign_approval_digest") for row in entries),
        "provider_requests_made_false": approval.get("provider_requests_made_in_approval"),
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed_in_approval"),
        "dataset_regeneration_false": approval.get("canonical_dataset_regenerated_in_approval"),
        "redesigned_label_regeneration_false": approval.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": approval.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": approval.get("predictive_evidence_execution_rerun_performed"),
        "label_objective_review_execution_rerun_false": approval.get("label_objective_target_definition_review_execution_rerun_performed"),
        "metric_recomputation_in_approval_false": approval.get("metric_recomputation_performed_in_approval"),
        "model_training_in_approval_false": approval.get("model_training_performed_in_approval"),
        "raw_provider_payloads_not_committed": approval.get("raw_provider_payloads_committed"),
        "api_keys_not_stored_or_printed": approval.get("api_keys_stored_or_printed"),
        "no_label_objective_redesign_execution_created": approval.get("label_objective_redesign_execution_created"),
        "no_threshold_horizon_refinement_candidate_created": approval.get("threshold_horizon_refinement_candidate_created"),
        "no_predictive_usefulness_acceptance_artifact_created": approval.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": approval.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": approval.get("runtime_migration_approval_created"),
        "next_chain_defined": approval.get("next_chain"), "next_gates_defined": approval.get("next_gates"),
        "risk_controls_defined": approval.get("risk_controls"), "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files"),
    }
    expected = {
        "candidate_review_digest_bound": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "candidate_digest_bound": EXPECTED_CANDIDATE_DIGEST,
        "results_review_digest_bound": SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"],
        "execution_digest_bound": SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"],
        "output_binding_digest_bound": SOURCE_EVIDENCE["label_objective_target_definition_review_output_binding_digest"],
        "approval_digest_bound": SOURCE_EVIDENCE["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"],
        "candidate_review_target_definition_digest_bound": SOURCE_EVIDENCE["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"],
        "path_selection_digest_bound": SOURCE_EVIDENCE["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"],
        "readiness_review_digest_bound": SOURCE_EVIDENCE["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"],
        "reassessment_digest_bound": SOURCE_EVIDENCE["predictive_usefulness_reassessment_using_redesigned_evidence_digest"],
        "predictive_results_review_digest_bound": SOURCE_EVIDENCE["additional_predictive_evidence_results_review_using_redesigned_labels_digest"],
        "predictive_execution_digest_bound": SOURCE_EVIDENCE["additional_predictive_evidence_execution_using_redesigned_labels_digest"],
        "matrix_digest_bound": SOURCE_EVIDENCE["feature_label_matrix_digest"],
        "feature_values_digest_bound": SOURCE_EVIDENCE["feature_values_digest"],
        "label_values_digest_bound": SOURCE_EVIDENCE["redesigned_label_values_digest"],
        "research_registry_digest_bound": SOURCE_EVIDENCE["research_registry_approval_digest"],
        "records_digest_bound": SOURCE_EVIDENCE["records_digest"],
        "target_universe_12_preserved": 12, "target_universe_matches_review_universe": True,
        "records_digest_preserved": SOURCE_EVIDENCE["records_digest"], "meta_913_preserved": 913,
        "operator_decision_matches": OPERATOR_DECISION,
        "operator_attestation_phrase_matches": REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE,
        "recommended_redesign_direction_confirmed": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "selected_redesign_direction_matches_recommendation": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "approval_scope_only": LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY,
        "label_objective_redesign_approved_true": True, "label_objective_redesign_approval_created_true": True,
        "label_objective_redesign_authorized_true": True, "ready_for_redesign_execution_true": True,
        "redesign_executed_false": False, "label_regeneration_authorized_false": False,
        "label_regeneration_performed_false": False, "new_targets_created_false": False,
        "target_definition_change_authorized_false": False, "target_definition_change_performed_false": False,
        "threshold_horizon_refinement_candidate_created_false": False,
        "improved_evidence_planning_candidate_created_false": False,
        "predictive_usefulness_not_accepted": NOT_ACCEPTED, "acceptance_ready_false": False,
        "acceptance_candidate_created_false": False, "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED, "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED, "trade_recommendations_false": False,
        "approved_candidate_basis_preserved": CANDIDATE_BASIS,
        "approved_redesign_objective_defined": ["PREPARE_OPTIONAL_RESEARCH_ONLY_LABEL_OBJECTIVE_REDESIGN_AFTER_FLAT_CLASS_AND_MAJORITY_STRUCTURE_REVIEW", LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY, "AUTHORIZED_NOT_EXECUTED", "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_REDESIGN_EXECUTION"],
        "approved_redesign_direction_selected": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "only_recommended_option_selected": [SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION],
        "approved_redesign_themes_11": REDESIGN_THEME_IDS,
        "approved_label_family_impact_review_10": LABEL_FAMILIES,
        "approved_redesign_questions_10": REDESIGN_QUESTIONS,
        "approved_future_outputs": APPROVED_FUTURE_OUTPUT_NAMES,
        "per_ticker_approval_entries_12": 12, "per_ticker_approval_digests_present": True,
        "provider_requests_made_false": False, "market_data_acquisition_false": False,
        "dataset_regeneration_false": False, "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False, "predictive_evidence_rerun_false": False,
        "label_objective_review_execution_rerun_false": False,
        "metric_recomputation_in_approval_false": False, "model_training_in_approval_false": False,
        "raw_provider_payloads_not_committed": False, "api_keys_not_stored_or_printed": False,
        "no_label_objective_redesign_execution_created": False,
        "no_threshold_horizon_refinement_candidate_created": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False, "no_runtime_migration_approval_created": False,
        "next_chain_defined": NEXT_CHAIN, "next_gates_defined": NEXT_GATES,
        "risk_controls_defined": RISK_CONTROLS, "no_tracked_marketflow_files": True,
    }
    return [_check(check_id, expected[check_id], actuals[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == "PASS" for row in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed,
        "failed_checks": len(checklist) - passed,
        "blocker_count": sum(row["status"] == "FAIL" for row in checklist),
        "label_objective_redesign_approved_by_operator": True,
        "approval_scope": LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY,
        "selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "label_objective_redesign_authorized": True,
        "ready_for_label_objective_redesign_execution_using_redesigned_evidence": True,
        "label_objective_redesign_executed": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "trade_recommendations_generated": False,
    }


def label_objective_redesign_approval_using_redesigned_evidence_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(approval))
    payload.pop("label_objective_redesign_approval_using_redesigned_evidence_digest", None)
    return semantic_digest(payload)


def build_label_objective_redesign_approved_using_redesigned_evidence_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    _validate_attestation(operator_attestation)
    source = _source_review(candidate_review_package)
    approval = _base_approval(source, operator_attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval["label_objective_redesign_approval_using_redesigned_evidence_digest"] = (
        label_objective_redesign_approval_using_redesigned_evidence_digest_v1(approval)
    )
    validate_label_objective_redesign_approved_using_redesigned_evidence_v1(approval)
    return approval


def _reject_forbidden_authority(value: Any, path: str = "approval") -> None:
    forbidden_true = {
        "label_objective_redesign_executed", "label_objective_redesign_execution_created",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "threshold_horizon_refinement_candidate_created", "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended", "profitability_acceptance_created",
        "runtime_migration_approved", "runtime_migration_active", "runtime_migration_approval_created",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_approval", "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval", "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "metric_recomputation_performed_in_approval", "model_training_performed_in_approval",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "execution_performed",
        "creates_new_labels", "creates_new_targets", "question_answered",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true and item is True:
                raise LabelObjectiveRedesignApprovalRedesignedEvidenceError(f"{current} must remain false")
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise LabelObjectiveRedesignApprovalRedesignedEvidenceError(f"{current} must remain unauthorized")
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveRedesignApprovalRedesignedEvidenceError(f"{current} must remain unaccepted")
            _reject_forbidden_authority(item, current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, f"{path}[{index}]")


def validate_label_objective_redesign_approved_using_redesigned_evidence_v1(
    approval: dict,
) -> dict:
    if not isinstance(approval, dict):
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError("approval must be an object")
    _reject_forbidden_authority(approval)
    _validate_attestation(approval.get("operator_attestation"))
    source = _source_review(None)
    expected_base = _base_approval(source, approval["operator_attestation"])
    for field, value in expected_base.items():
        _expect(approval.get(field), value, field)
    entries = approval.get("per_ticker_approval_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError("per-ticker approval entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        _expect(row.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(row.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        digest = row.get("per_ticker_label_objective_redesign_approval_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise LabelObjectiveRedesignApprovalRedesignedEvidenceError(f"{ticker} approval digest missing")
        _expect(digest, per_ticker_label_objective_redesign_approval_using_redesigned_evidence_digest_v1(row), f"{ticker} approval digest")
    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != CHECK_IDS:
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError("approval checklist mismatch")
    _expect(checklist, _checklist(approval), "approval checklist")
    if any(row["status"] != "PASS" for row in checklist):
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError("approval checklist failed")
    _expect(approval.get("approval_summary"), _summary(checklist), "approval summary")
    digest = approval.get("label_objective_redesign_approval_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError("approval digest missing")
    _expect(digest, label_objective_redesign_approval_using_redesigned_evidence_digest_v1(approval), "approval digest")
    return {
        "validation_status": "LABEL_OBJECTIVE_REDESIGN_APPROVAL_USING_REDESIGNED_EVIDENCE_VALID",
        "approval_digest": digest,
        **{key: approval["approval_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_label_objective_redesign_approved_using_redesigned_evidence_markdown_v1(
    approval: dict,
) -> str:
    validate_label_objective_redesign_approved_using_redesigned_evidence_v1(approval)
    attestation = approval["operator_attestation"]
    sections = [
        ("Title", "Optional Label Objective Redesign Approval Using Redesigned Evidence v1."),
        ("Optional Label Objective Redesign Approval Using Redesigned Evidence", f"{approval['artifact_kind']} / {approval['approval_status']} / {approval['approval_scope']}"),
        ("Operator Attestation", f"{attestation['operator_reference']} / {attestation['operator_attestation_timestamp_utc']} / {attestation['operator_decision']}"),
        ("Source Candidate Review", f"{approval['source_candidate_review_artifact_kind']} / {approval['label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest']}"),
        ("Bound Evidence", "Candidate-review, candidate, review-chain, predictive, matrix, feature, label, registry, and records digests are bound."),
        ("Dataset and Universe", f"{approval['dataset_name']}; {', '.join(approval['target_universe'])}; META=913."),
        ("Approved Candidate Basis", str(approval["approved_candidate_basis"])),
        ("Approved Redesign Objective", approval["label_objective_redesign_objective"]),
        ("Selected Redesign Direction", approval["selected_label_objective_redesign_direction"]),
        ("Approved Redesign Themes", "\n".join(f"- {row['theme']}" for row in approval["approved_redesign_themes"])),
        ("Approved Label Family Impact Review", "\n".join(f"- {row['label_family']}" for row in approval["approved_label_family_impact_review"])),
        ("Approved Redesign Questions", "\n".join(f"- {row['question']}" for row in approval["approved_redesign_questions"])),
        ("Approved Future Outputs", "\n".join(f"- {row['output_name']}: {row['output_status']}" for row in approval["approved_future_outputs"])),
        ("Per-Ticker Approval Entries", "\n".join(f"- {row['ticker']}: {row['historical_record_count']} records" for row in approval["per_ticker_approval_entries"])),
        ("Next Chain", "\n".join(f"{index}. {item}" for index, item in enumerate(approval["next_chain"], 1))),
        ("Next Gates", "\n".join(f"- {item}" for item in approval["next_gates"])),
        ("Risk Controls", "\n".join(f"- {item}" for item in approval["risk_controls"])),
        ("Predictive Usefulness Boundary", "Predictive usefulness remains not accepted."),
        ("Profitability Boundary", "Profitability remains not accepted."),
        ("Runtime Boundary", "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."),
        ("Checklist Summary", f"{approval['approval_summary']['passed_checks']}/{approval['approval_summary']['total_checks']} passed; zero blockers."),
        ("Guardrails", "Approval only: no redesign execution, regeneration, new targets, operational target change, provider, runtime, or trading action."),
    ]
    lines = ["# Optional Label Objective Redesign Approval Using Redesigned Evidence", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", body, ""])
    return "\n".join(lines)


def write_label_objective_redesign_approved_using_redesigned_evidence_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    approval = build_label_objective_redesign_approved_using_redesigned_evidence_v1(
        candidate_review_package=candidate_review_package, operator_attestation=operator_attestation,
    )
    validation = validate_label_objective_redesign_approved_using_redesigned_evidence_v1(approval)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "label_objective_redesign_approval_using_redesigned_evidence_v1.json"
    payload = canonical_json_bytes(approval)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise LabelObjectiveRedesignApprovalRedesignedEvidenceError("approval output already exists") from exc
    return validation | {"path": str(path).replace("\\", "/"), "payload_sha256": sha256_bytes(payload)}
