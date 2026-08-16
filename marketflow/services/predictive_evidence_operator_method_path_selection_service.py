"""Offline operator selection of a future predictive-evidence method path."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import predictive_evidence_method_diagnostic_review_service as diagnostic


ARTIFACT_KIND_PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION = (
    "PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION"
)
SCHEMA_VERSION_PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION_V1 = (
    "predictive_evidence_operator_method_path_selection_v1"
)
PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTED = (
    "PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTED"
)
METHOD_PATH_SELECTION_ONLY_NOT_EXECUTION = "METHOD_PATH_SELECTION_ONLY_NOT_EXECUTION"
OPERATOR_DECISION_SELECT_LABEL_OBJECTIVE_REDESIGN_CANDIDATE = (
    "SELECT_METHOD_PATH_LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "predictive_evidence_operator_method_path_selection_attestation_v1"
)
REQUIRED_OPERATOR_METHOD_PATH_SELECTION_ATTESTATION_PHRASE = (
    "SELECT METHOD PATH LABEL OBJECTIVE REDESIGN CANDIDATE MSFT NVDA AMZN GOOGL "
    "META TSLA JPM XOM JNJ WMT CAT LMT METHOD_PATH_SELECTION_ONLY"
)
SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE = (
    "OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
)
SELECTED_NEXT_ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
)
SELECTED_FOR_FUTURE_CANDIDATE_ONLY = "SELECTED_FOR_FUTURE_CANDIDATE_ONLY"

EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST = (
    "416d0ce614f7bb034b473029e8a98b1d9b94adcde4204b986b898fcbb99c2b51"
)
EXPECTED_PLANNING_TREE_REVIEW_DIGEST = diagnostic.EXPECTED_PLANNING_TREE_REVIEW_DIGEST
EXPECTED_LATEST_READINESS_DIGEST = diagnostic.EXPECTED_LATEST_READINESS_DIGEST
EXPECTED_LATEST_REASSESSMENT_DIGEST = diagnostic.EXPECTED_LATEST_REASSESSMENT_DIGEST
EXPECTED_REFINED_RESULTS_REVIEW_DIGEST = diagnostic.EXPECTED_REFINED_RESULTS_REVIEW_DIGEST
EXPECTED_ORIGINAL_READINESS_DIGEST = diagnostic.EXPECTED_ORIGINAL_READINESS_DIGEST
EXPECTED_ORIGINAL_REASSESSMENT_DIGEST = diagnostic.EXPECTED_ORIGINAL_REASSESSMENT_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    diagnostic.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_RECORDS_DIGEST = diagnostic.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(diagnostic.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(diagnostic.EXPECTED_RECORD_COUNTS)
REGISTRY_APPROVED_DATASET_METADATA = deepcopy(
    diagnostic.REGISTRY_APPROVED_DATASET_METADATA
)
NOT_ACCEPTED = diagnostic.NOT_ACCEPTED
NOT_AUTHORIZED = diagnostic.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = diagnostic.RESEARCH_ONLY_NON_ACTIONABLE
ORIGINAL_READINESS_DECISION = diagnostic.ORIGINAL_READINESS_DECISION
REFINED_READINESS_DECISION = diagnostic.REFINED_READINESS_DECISION

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPTION_IDS = list(diagnostic.OPTION_IDS)
OPTION_STATES = {
    "OPTION_A_PAUSE_AND_ARCHIVE_RESEARCH_CHAIN": "NOT_SELECTED",
    "OPTION_B_METHOD_DIAGNOSTIC_REVIEW": "COMPLETED",
    "OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE": SELECTED_FOR_FUTURE_CANDIDATE_ONLY,
    "OPTION_D_FEATURE_METHOD_REDESIGN_CANDIDATE": "NOT_SELECTED",
    "OPTION_E_DATA_SCOPE_EXPANSION_CANDIDATE": "NOT_SELECTED",
    "OPTION_F_NEW_MODELING_APPROACH_CANDIDATE": "NOT_SELECTED",
    "OPTION_G_ACCEPTANCE_CANDIDATE": "NOT_ALLOWED_CURRENTLY",
}

SELECTION_REASON = (
    "LABEL_OBJECTIVE_AND_PREDICTION_TARGET_MUST_BE_DIAGNOSED_BEFORE_MORE_MODEL_OR_EXECUTION_WORK"
)
SELECTION_BASIS = (
    "TWO_CONSECUTIVE_READINESS_GATES_NOT_READY_AFTER_ORIGINAL_AND_REFINED_EVIDENCE"
)

NEXT_CHAIN = [
    "Label Objective Redesign Candidate v1.",
    "Label Objective Redesign Candidate Operator Review Package v1.",
    "Label Objective Redesign Approval Ceremony v1, if selected.",
    "Label Objective Redesign Execution Candidate v1.",
    "Future evidence execution chain only after separate approval.",
    "Predictive usefulness reassessment/readiness chain only after new evidence review.",
    "Predictive usefulness acceptance candidate only if readiness passes.",
    "Profitability chain only if separately required.",
    "Runtime migration chain only if separately authorized.",
]

RISK_CONTROLS = [
    "selection_does_not_create_redesign_candidate",
    "selection_does_not_authorize_execution",
    "selection_does_not_accept_predictive_usefulness",
    "selection_does_not_accept_profitability",
    "selection_does_not_authorize_runtime",
    "selection_does_not_authorize_strategy",
    "selection_does_not_authorize_paper_trading",
    "selection_does_not_authorize_broker_execution",
    "selection_does_not_generate_trade_recommendations",
    "acceptance_candidate_not_allowed_currently",
    "preserve_frozen_dataset",
    "preserve_meta_record_limitation",
    "research_outputs_non_actionable",
    "operator_review_required_for_next_candidate",
]

REQUIRED_DIGEST_FIELDS = {
    "predictive_evidence_method_diagnostic_review_package_digest": EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
    "predictive_evidence_planning_tree_review_package_digest": EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
    "latest_readiness_rerun_using_refined_evidence_digest": EXPECTED_LATEST_READINESS_DIGEST,
    "latest_reassessment_rerun_using_refined_evidence_digest": EXPECTED_LATEST_REASSESSMENT_DIGEST,
    "refined_results_review_digest": EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
    "original_acceptance_readiness_review_digest": EXPECTED_ORIGINAL_READINESS_DIGEST,
    "original_reassessment_review_digest": EXPECTED_ORIGINAL_REASSESSMENT_DIGEST,
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

BOOLEAN_CONFIRMATION_FIELDS = [
    "operator_confirms_original_readiness_not_ready",
    "operator_confirms_refined_readiness_not_ready",
    "operator_confirms_predictive_usefulness_not_accepted",
    "operator_confirms_profitability_not_accepted",
    "operator_confirms_runtime_not_authorized",
    "operator_confirms_acceptance_option_not_allowed",
    "operator_confirms_selection_scope_only",
    "operator_confirms_no_label_objective_redesign_candidate_created",
    "operator_confirms_no_execution_authorized",
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
    "method_diagnostic_digest_bound",
    "planning_tree_digest_bound",
    "latest_readiness_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_required_digests",
    "operator_confirms_original_and_refined_not_ready",
    "operator_confirms_predictive_usefulness_not_accepted",
    "operator_confirms_profitability_not_accepted",
    "operator_confirms_runtime_not_authorized",
    "selected_method_path_is_label_objective_redesign",
    "selection_scope_only",
    "label_objective_redesign_candidate_not_created",
    "execution_not_authorized",
    "acceptance_option_not_allowed",
    "method_options_defined",
    "option_states_correct",
    "next_chain_defined",
    "risk_controls_defined",
    "no_provider_requests",
    "no_market_data_acquisition",
    "no_dataset_regeneration",
    "no_predictive_rerun",
    "no_metric_recomputation",
    "no_strategy_scoring",
    "no_trade_recommendations",
    "no_runtime_activation",
    "no_tracked_marketflow_files",
]


class PredictiveEvidenceOperatorMethodPathSelectionError(ValueError):
    """Raised when an operator path selection violates its selection-only scope."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
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


def build_predictive_evidence_operator_method_path_selection_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_method_diagnostic_review_digest: str,
    operator_confirms_planning_tree_review_digest: str,
    operator_confirms_latest_readiness_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_original_readiness_not_ready: bool,
    operator_confirms_refined_readiness_not_ready: bool,
    operator_confirms_predictive_usefulness_not_accepted: bool,
    operator_confirms_profitability_not_accepted: bool,
    operator_confirms_runtime_not_authorized: bool,
    operator_confirms_acceptance_option_not_allowed: bool,
    operator_confirms_selected_method_path: str,
    operator_confirms_selection_scope_only: bool,
    operator_confirms_no_label_objective_redesign_candidate_created: bool,
    operator_confirms_no_execution_authorized: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_SELECT_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
) -> dict:
    """Build the non-secret operator attestation for method-path selection."""
    return {
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_V1,
        "operator_reference": operator_reference,
        "operator_confirms_method_diagnostic_review_digest": operator_confirms_method_diagnostic_review_digest,
        "operator_confirms_planning_tree_review_digest": operator_confirms_planning_tree_review_digest,
        "operator_confirms_latest_readiness_digest": operator_confirms_latest_readiness_digest,
        "operator_confirms_research_registry_approval_digest": operator_confirms_research_registry_approval_digest,
        "operator_confirms_records_digest": operator_confirms_records_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_original_readiness_not_ready": operator_confirms_original_readiness_not_ready,
        "operator_confirms_refined_readiness_not_ready": operator_confirms_refined_readiness_not_ready,
        "operator_confirms_predictive_usefulness_not_accepted": operator_confirms_predictive_usefulness_not_accepted,
        "operator_confirms_profitability_not_accepted": operator_confirms_profitability_not_accepted,
        "operator_confirms_runtime_not_authorized": operator_confirms_runtime_not_authorized,
        "operator_confirms_acceptance_option_not_allowed": operator_confirms_acceptance_option_not_allowed,
        "operator_confirms_selected_method_path": operator_confirms_selected_method_path,
        "operator_confirms_selection_scope_only": operator_confirms_selection_scope_only,
        "operator_confirms_no_label_objective_redesign_candidate_created": operator_confirms_no_label_objective_redesign_candidate_created,
        "operator_confirms_no_execution_authorized": operator_confirms_no_execution_authorized,
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


def _validate_timestamp(timestamp: Any) -> None:
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "operator_attestation_timestamp_utc must be a non-empty UTC timestamp"
        )
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "operator_attestation_timestamp_utc must be ISO-8601"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "operator_attestation_timestamp_utc must be UTC"
        )


def _validate_attestation(attestation: dict[str, Any]) -> None:
    if not isinstance(attestation, dict):
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "operator_attestation must be a JSON object"
        )
    _expect(
        attestation.get("operator_decision"),
        OPERATOR_DECISION_SELECT_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "operator decision",
    )
    _expect(
        attestation.get("operator_attestation_phrase"),
        REQUIRED_OPERATOR_METHOD_PATH_SELECTION_ATTESTATION_PHRASE,
        "operator attestation phrase",
    )
    _expect(
        attestation.get("operator_attestation_version"),
        OPERATOR_ATTESTATION_VERSION_V1,
        "operator attestation version",
    )
    reference = attestation.get("operator_reference")
    if not isinstance(reference, str) or not reference.strip() or len(reference) > 128:
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "operator_reference must be a non-secret reference of 1 to 128 characters"
        )
    _validate_timestamp(attestation.get("operator_attestation_timestamp_utc"))
    expected_confirmations = {
        "operator_confirms_method_diagnostic_review_digest": EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "operator_confirms_planning_tree_review_digest": EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "operator_confirms_latest_readiness_digest": EXPECTED_LATEST_READINESS_DIGEST,
        "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_selected_method_path": SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
    }
    for field, expected in expected_confirmations.items():
        _expect(attestation.get(field), expected, field)
    for field in BOOLEAN_CONFIRMATION_FIELDS:
        _expect(attestation.get(field), True, field)


def _method_options() -> list[dict[str, Any]]:
    return [
        {
            "option_id": option_id,
            "status": OPTION_STATES[option_id],
            "execution_authorized": False,
            "candidate_created": False,
            "authority": "METHOD_PATH_SELECTION_ONLY_NOT_EXECUTION",
        }
        for option_id in OPTION_IDS
    ]


def _base_selection(attestation: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION_V1,
        "selection_status": PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTED,
        "selection_scope": METHOD_PATH_SELECTION_ONLY_NOT_EXECUTION,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "operator_method_path_selection_created": True,
        "operator_method_path_selection_ready": True,
        "method_path_selected": True,
        "selected_method_path": SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "selected_next_artifact_kind": SELECTED_NEXT_ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "selected_path_status": SELECTED_FOR_FUTURE_CANDIDATE_ONLY,
        "ready_for_label_objective_redesign_candidate": True,
        "label_objective_redesign_candidate_created": False,
        "feature_method_redesign_candidate_created": False,
        "data_scope_expansion_candidate_created": False,
        "new_modeling_approach_candidate_created": False,
        "execution_authorized": False,
        "provider_requests_made_in_selection": False,
        "live_provider_transport_enabled_in_selection": False,
        "market_data_acquisition_performed_in_selection": False,
        "dataset_regeneration_performed_in_selection": False,
        "predictive_evidence_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "model_training_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
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
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        **REQUIRED_DIGEST_FIELDS,
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
        "registry_approved_dataset_metadata": deepcopy(
            REGISTRY_APPROVED_DATASET_METADATA
        ),
        "original_readiness_decision": ORIGINAL_READINESS_DECISION,
        "refined_readiness_decision": REFINED_READINESS_DECISION,
        "method_options": _method_options(),
        "selection_reason": SELECTION_REASON,
        "selection_basis": SELECTION_BASIS,
        "evidence_comparison": {
            "original_oos_majority_accuracy": "0.539491",
            "original_oos_previous_direction_accuracy": "0.495984",
            "original_oos_ticker_cross_sectional_accuracy": "0.502677",
            "original_oos_brier_score": "0.24875351",
            "refined_oos_accuracy_range": "0.119813 to 0.480924",
            "refined_signal_consistency": "WEAK_OR_MIXED",
            "refined_baseline_outperformance": "INSUFFICIENT_OR_MIXED",
            "refined_model_comparison": (
                "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE"
            ),
        },
        "next_chain": list(NEXT_CHAIN),
        "risk_controls": list(RISK_CONTROLS),
        "operator_attestation": deepcopy(attestation),
    }


def _derived_checks(selection: dict[str, Any]) -> dict[str, Any]:
    attestation = selection.get("operator_attestation", {})
    options = selection.get("method_options", [])
    option_map = {
        item.get("option_id"): item
        for item in options
        if isinstance(item, dict)
    } if isinstance(options, list) else {}
    digest_confirmations = {
        "operator_confirms_method_diagnostic_review_digest": EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "operator_confirms_planning_tree_review_digest": EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "operator_confirms_latest_readiness_digest": EXPECTED_LATEST_READINESS_DIGEST,
        "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
    }
    return {
        "method_diagnostic_digest_bound": selection.get(
            "predictive_evidence_method_diagnostic_review_package_digest"
        )
        == EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "planning_tree_digest_bound": selection.get(
            "predictive_evidence_planning_tree_review_package_digest"
        )
        == EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "latest_readiness_digest_bound": selection.get(
            "latest_readiness_rerun_using_refined_evidence_digest"
        )
        == EXPECTED_LATEST_READINESS_DIGEST,
        "research_registry_digest_bound": selection.get(
            "research_registry_approval_digest"
        )
        == EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest_bound": selection.get("records_digest")
        == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": selection.get("target_universe_count") == 12
        and selection.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": selection.get("records_digest")
        == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": selection.get("meta_record_count") == 913
        and selection.get("per_ticker_record_counts", {}).get("META") == 913,
        "operator_decision_matches": attestation.get("operator_decision")
        == OPERATOR_DECISION_SELECT_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "operator_attestation_phrase_matches": attestation.get(
            "operator_attestation_phrase"
        )
        == REQUIRED_OPERATOR_METHOD_PATH_SELECTION_ATTESTATION_PHRASE,
        "operator_confirms_all_required_digests": all(
            attestation.get(field) == expected
            for field, expected in digest_confirmations.items()
        ),
        "operator_confirms_original_and_refined_not_ready": attestation.get(
            "operator_confirms_original_readiness_not_ready"
        )
        is True
        and attestation.get("operator_confirms_refined_readiness_not_ready") is True,
        "operator_confirms_predictive_usefulness_not_accepted": attestation.get(
            "operator_confirms_predictive_usefulness_not_accepted"
        )
        is True,
        "operator_confirms_profitability_not_accepted": attestation.get(
            "operator_confirms_profitability_not_accepted"
        )
        is True,
        "operator_confirms_runtime_not_authorized": attestation.get(
            "operator_confirms_runtime_not_authorized"
        )
        is True,
        "selected_method_path_is_label_objective_redesign": selection.get(
            "selected_method_path"
        )
        == SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "selection_scope_only": selection.get("selection_scope")
        == METHOD_PATH_SELECTION_ONLY_NOT_EXECUTION
        and attestation.get("operator_confirms_selection_scope_only") is True,
        "label_objective_redesign_candidate_not_created": selection.get(
            "label_objective_redesign_candidate_created"
        )
        is False
        and attestation.get(
            "operator_confirms_no_label_objective_redesign_candidate_created"
        )
        is True,
        "execution_not_authorized": selection.get("execution_authorized") is False
        and attestation.get("operator_confirms_no_execution_authorized") is True,
        "acceptance_option_not_allowed": option_map.get(
            "OPTION_G_ACCEPTANCE_CANDIDATE", {}
        ).get("status")
        == "NOT_ALLOWED_CURRENTLY"
        and attestation.get("operator_confirms_acceptance_option_not_allowed") is True,
        "method_options_defined": list(option_map) == OPTION_IDS,
        "option_states_correct": all(
            option_map.get(option_id, {}).get("status") == expected
            for option_id, expected in OPTION_STATES.items()
        ),
        "next_chain_defined": selection.get("next_chain") == NEXT_CHAIN,
        "risk_controls_defined": selection.get("risk_controls") == RISK_CONTROLS,
        "no_provider_requests": selection.get("provider_requests_made_in_selection")
        is False,
        "no_market_data_acquisition": selection.get(
            "market_data_acquisition_performed_in_selection"
        )
        is False,
        "no_dataset_regeneration": selection.get(
            "dataset_regeneration_performed_in_selection"
        )
        is False,
        "no_predictive_rerun": selection.get("predictive_evidence_rerun_performed")
        is False,
        "no_metric_recomputation": selection.get("metrics_recomputation_performed")
        is False,
        "no_strategy_scoring": selection.get("new_strategy_scoring_performed")
        is False,
        "no_trade_recommendations": selection.get("trade_recommendations_generated")
        is False,
        "no_runtime_activation": selection.get("runtime_migration_approved") is False
        and selection.get("runtime_migration_active") is False,
        "no_tracked_marketflow_files": selection.get("no_tracked_marketflow_files")
        is True
        and selection.get("tracked_marketflow_files") == [],
    }


def _checklist(selection: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(selection)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    blockers = sum(
        item.get("status") == FAIL and item.get("severity") == BLOCKER
        for item in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "operator_method_path_selection_ready": blockers == 0,
        "selected_method_path": SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "ready_for_label_objective_redesign_candidate": True,
        "label_objective_redesign_candidate_created": False,
        "acceptance_candidate_allowed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(selection: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(selection)
    payload.pop("predictive_evidence_operator_method_path_selection_digest", None)
    return payload


def predictive_evidence_operator_method_path_selection_digest_v1(
    selection: dict[str, Any],
) -> str:
    """Return the deterministic digest for the attested selection."""
    return semantic_digest(_digest_payload(selection))


def build_predictive_evidence_operator_method_path_selection_v1(
    *,
    operator_attestation: dict,
) -> dict:
    """Build the selected future planning path after strict attestation checks."""
    _validate_attestation(operator_attestation)
    selection = _base_selection(operator_attestation)
    selection["review_checklist"] = _checklist(selection)
    selection["review_summary"] = _summary(selection["review_checklist"])
    selection["predictive_evidence_operator_method_path_selection_digest"] = (
        predictive_evidence_operator_method_path_selection_digest_v1(selection)
    )
    validate_predictive_evidence_operator_method_path_selection_v1(selection)
    return selection


def _reject_forbidden_authority(value: Any, *, path: str = "selection") -> None:
    forbidden_true_fields = {
        "label_objective_redesign_candidate_created",
        "feature_method_redesign_candidate_created",
        "data_scope_expansion_candidate_created",
        "new_modeling_approach_candidate_created",
        "execution_authorized",
        "provider_requests_made_in_selection",
        "live_provider_transport_enabled_in_selection",
        "market_data_acquisition_performed_in_selection",
        "dataset_regeneration_performed_in_selection",
        "predictive_evidence_rerun_performed",
        "metrics_recomputation_performed",
        "model_training_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
        "candidate_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise PredictiveEvidenceOperatorMethodPathSelectionError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise PredictiveEvidenceOperatorMethodPathSelectionError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveEvidenceOperatorMethodPathSelectionError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_predictive_evidence_operator_method_path_selection_v1(
    selection: dict,
) -> dict:
    """Validate the strict attestation, selected path, and closed authorities."""
    if not isinstance(selection, dict):
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "method path selection must be a JSON object"
        )
    _reject_forbidden_authority(selection)
    attestation = selection.get("operator_attestation")
    _validate_attestation(attestation)
    expected_base = _base_selection(attestation)
    for field, expected in expected_base.items():
        _expect(selection.get(field), expected, field)
    checklist = selection.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(selection)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "review_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(selection.get("review_summary"), expected_summary, "review_summary")
    digest = selection.get(
        "predictive_evidence_operator_method_path_selection_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "predictive evidence operator method path selection digest missing"
        )
    _expect(
        digest,
        predictive_evidence_operator_method_path_selection_digest_v1(selection),
        "predictive_evidence_operator_method_path_selection_digest",
    )
    return {
        "status": "PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION_VALID",
        "artifact_kind": selection["artifact_kind"],
        "selection_status": selection["selection_status"],
        "selection_scope": selection["selection_scope"],
        "predictive_evidence_operator_method_path_selection_digest": digest,
        "selected_method_path": selection["selected_method_path"],
        "ready_for_label_objective_redesign_candidate": True,
        "label_objective_redesign_candidate_created": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_predictive_evidence_operator_method_path_selection_markdown_v1(
    selection: dict,
) -> str:
    """Render a sanitized Markdown summary of the attested method selection."""
    validation = validate_predictive_evidence_operator_method_path_selection_v1(
        selection
    )
    attestation = selection["operator_attestation"]
    evidence = selection["evidence_comparison"]
    summary = selection["review_summary"]
    lines = [
        "# MarketFlow Predictive Evidence Operator Method Path Selection",
        "",
        "## Title",
        "- Operator Method Path Selection v1.",
        "",
        "## Operator Method Path Selection",
        f"- Artifact/status/scope: `{selection['artifact_kind']}` / `{selection['selection_status']}` / `{selection['selection_scope']}`.",
        f"- Digest: `{validation['predictive_evidence_operator_method_path_selection_digest']}`.",
        "",
        "## Operator Attestation",
        f"- Reference/timestamp/version: `{attestation['operator_reference']}` / `{attestation['operator_attestation_timestamp_utc']}` / `{attestation['operator_attestation_version']}`.",
        f"- Decision: `{attestation['operator_decision']}`.",
        "",
        "## Bound Evidence",
    ]
    lines.extend(
        f"- `{field}`: `{digest}`"
        for field, digest in REQUIRED_DIGEST_FIELDS.items()
    )
    lines.extend(
        [
            "",
            "## Dataset and Universe",
            f"- Dataset/profile/timeframe: `{selection['dataset_name']}` / `{selection['source_profile']}` / `{selection['timeframe']}`.",
            f"- Universe: `{', '.join(selection['target_universe'])}`.",
            "- Records: `11946`; META remains `913`, every other ticker remains `1003`.",
            "",
            "## Evidence Comparison",
            f"- Original OOS majority/previous/cross-sectional: `{evidence['original_oos_majority_accuracy']}` / `{evidence['original_oos_previous_direction_accuracy']}` / `{evidence['original_oos_ticker_cross_sectional_accuracy']}`.",
            f"- Refined OOS/signal/baseline: `{evidence['refined_oos_accuracy_range']}` / `{evidence['refined_signal_consistency']}` / `{evidence['refined_baseline_outperformance']}`.",
            "",
            "## Method Options",
        ]
    )
    lines.extend(
        f"- `{item['option_id']}`: `{item['status']}`"
        for item in selection["method_options"]
    )
    lines.extend(
        [
            "",
            "## Selected Method Path",
            f"- Path/next artifact/status: `{selection['selected_method_path']}` / `{selection['selected_next_artifact_kind']}` / `{selection['selected_path_status']}`.",
            "- The next artifact is not created by this selection.",
            "",
            "## Selection Rationale",
            f"- Reason/basis: `{selection['selection_reason']}` / `{selection['selection_basis']}`.",
            "",
            "## Next Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(selection["next_chain"], start=1)
    )
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in selection["risk_controls"])
    lines.extend(
        [
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- This attested selection opens only a future candidate-planning gate. It creates no redesign candidate and authorizes no execution, acceptance, profitability, runtime, strategy, paper, broker, or recommendation action.",
            "- No provider request, acquisition, dataset regeneration, evidence rerun, metric recomputation, model training, scoring, recommendation, raw payload commit, or API-key storage occurred.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_evidence_operator_method_path_selection_v1(
    output_dir: str | Path,
    *,
    operator_attestation: dict,
    filename: str | None = None,
) -> dict:
    """Write one canonical attested selection JSON without overwriting."""
    selection = build_predictive_evidence_operator_method_path_selection_v1(
        operator_attestation=operator_attestation
    )
    validation = validate_predictive_evidence_operator_method_path_selection_v1(
        selection
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_evidence_operator_method_path_selection_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "method path selection filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveEvidenceOperatorMethodPathSelectionError(
            "method path selection output already exists"
        )
    payload = canonical_json_bytes(selection)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
