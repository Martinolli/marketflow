"""Offline, attestation-gated operator method-or-closure selection."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_not_ready_closure_method_tree_improved_evidence_service as closure_service


ARTIFACT_KIND_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE = (
    "OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE_V1 = (
    "operator_method_or_closure_selection_using_improved_evidence_v1"
)
OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_IMPROVED_EVIDENCE = (
    "OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_IMPROVED_EVIDENCE"
)
OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY = "OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY"
SELECTED_OPTION = "OPTION_A_STOP_ACCEPTANCE_PATH_CURRENT_DATASET"
SELECTED_DECISION = "SELECT_STOP_ACCEPTANCE_PATH_CURRENT_DATASET"
SELECTION_RATIONALE = (
    "CURRENT_IMPROVED_EVIDENCE_NOT_READY_SMALL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_OPTIONAL_MODEL_COVERAGE_INCOMPLETE"
)
NEXT_ARTIFACT_KIND = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE"
)
OPERATOR_ATTESTATION_VERSION = (
    "operator_method_or_closure_selection_using_improved_evidence_attestation_v1"
)
REQUIRED_OPERATOR_METHOD_OR_CLOSURE_SELECTION_ATTESTATION_PHRASE = (
    "SELECT OPTION_A STOP ACCEPTANCE PATH CURRENT DATASET USING IMPROVED EVIDENCE "
    "MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY"
)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_CLOSURE_DIGEST = "ca179fdfe2fcc3c1572339d7e35f8f201177d59d3b7fa5dc245b58620987cbda"
EXPECTED_READINESS_DIGEST = closure_service.EXPECTED_READINESS_DIGEST
EXPECTED_REASSESSMENT_DIGEST = closure_service.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = closure_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = closure_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_OUTPUT_BINDING_DIGEST = closure_service.EXPECTED_OUTPUT_BINDING_DIGEST
EXPECTED_MATRIX_DIGEST = closure_service.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = closure_service.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = closure_service.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = closure_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = closure_service.EXPECTED_RECORDS_DIGEST
SOURCE_EVIDENCE = deepcopy(closure_service.SOURCE_EVIDENCE)

TARGET_UNIVERSE = list(closure_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(closure_service.EXPECTED_RECORD_COUNTS)

SELECTION_OPTIONS_REVIEW = {
    option: {
        "source_status": value["option_status"],
        "selection_status": (
            "SELECTED_BY_OPERATOR"
            if option == SELECTED_OPTION
            else "NOT_ALLOWED_CURRENTLY"
            if option == "OPTION_H_ACCEPTANCE_CANDIDATE"
            else "NOT_SELECTED"
        ),
    }
    for option, value in closure_service.METHOD_PLANNING_TREE.items()
}

NEXT_CHAIN = [
    "Predictive Usefulness Acceptance Path Archive Record Using Improved Evidence v1.",
    "Optional future method/evidence work only after a separate operator decision.",
    "Future evidence candidate only after separate selection, review, and approval.",
    "Reassessment only after new evidence is created.",
    "Acceptance-readiness rerun only after new reassessment.",
    "Acceptance candidate only if future readiness passes.",
    "Profitability review only after separate predictive-usefulness acceptance chain.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence",
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
    "selection_does_not_create_archive_record",
    "selection_does_not_create_future_method_candidate",
    "selection_does_not_create_future_evidence_candidate",
    "selection_does_not_accept_predictive_usefulness",
    "selection_does_not_create_acceptance_candidate",
    "selection_does_not_create_acceptance_ceremony",
    "selection_does_not_accept_profitability",
    "selection_does_not_authorize_runtime",
    "selection_does_not_authorize_strategy",
    "selection_does_not_authorize_paper_trading",
    "selection_does_not_authorize_broker_execution",
    "selection_does_not_generate_trade_recommendations",
    "selection_does_not_regenerate_labels",
    "selection_does_not_create_new_targets",
    "selection_does_not_authorize_target_definition_change",
    "selection_does_not_generate_features",
    "selection_does_not_create_canonical_feature_label_matrix",
    "selection_does_not_rerun_predictive_evidence",
    "selection_does_not_rerun_reassessment",
    "selection_does_not_rerun_readiness_review",
    "selection_does_not_recompute_metrics",
    "selection_does_not_train_models",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_prior_predictive_evidence_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "do_not_mutate_current_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_selection_scope_only",
    "operator_confirms_acceptance_path_closed_current_dataset",
    "operator_confirms_ready_for_archive_record",
    "operator_confirms_no_method_improvement_candidate_created",
    "operator_confirms_no_future_evidence_candidate_created",
    "operator_confirms_no_reassessment_created",
    "operator_confirms_no_acceptance_candidate_created",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_strategy_authorization",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_label_regeneration",
    "operator_confirms_no_new_targets",
    "operator_confirms_no_feature_generation",
    "operator_confirms_no_feature_label_matrix",
    "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]


class OperatorMethodOrClosureSelectionImprovedEvidenceError(ValueError):
    """Raised when selection violates its attestation or selection-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(f"{field} must be false")


def build_operator_method_or_closure_selection_using_improved_evidence_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_closure_digest: str,
    operator_confirms_source_readiness_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selection_scope_only: bool,
    operator_confirms_selected_option: str,
    operator_confirms_acceptance_path_closed_current_dataset: bool,
    operator_confirms_ready_for_archive_record: bool,
    operator_confirms_no_method_improvement_candidate_created: bool,
    operator_confirms_no_future_evidence_candidate_created: bool,
    operator_confirms_no_reassessment_created: bool,
    operator_confirms_no_acceptance_candidate_created: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_label_regeneration: bool,
    operator_confirms_no_new_targets: bool,
    operator_confirms_no_feature_generation: bool,
    operator_confirms_no_feature_label_matrix: bool,
    operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_option: str = SELECTED_OPTION,
    operator_decision: str = SELECTED_DECISION,
) -> dict:
    """Build a non-secret operator attestation; selection validates it fail-closed."""
    return {
        "operator_decision": operator_decision,
        "selected_option": selected_option,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_reference": operator_reference,
        "operator_confirms_source_closure_digest": operator_confirms_source_closure_digest,
        "operator_confirms_source_readiness_digest": operator_confirms_source_readiness_digest,
        "operator_confirms_records_digest": operator_confirms_records_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_meta_record_count": operator_confirms_meta_record_count,
        "operator_confirms_non_meta_record_count": operator_confirms_non_meta_record_count,
        "operator_confirms_selected_option": operator_confirms_selected_option,
        **{
            field: value
            for field, value in locals().items()
            if field in ATTESTATION_BOOLEAN_FIELDS
        },
    }


def _validate_attestation(attestation: Any) -> None:
    if not isinstance(attestation, dict):
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError("operator attestation missing")
    expected = {
        "operator_decision": SELECTED_DECISION,
        "selected_option": SELECTED_OPTION,
        "operator_attestation_phrase": REQUIRED_OPERATOR_METHOD_OR_CLOSURE_SELECTION_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_closure_digest": EXPECTED_CLOSURE_DIGEST,
        "operator_confirms_source_readiness_digest": EXPECTED_READINESS_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_option": SELECTED_OPTION,
    }
    required_keys = set(expected) | set(ATTESTATION_BOOLEAN_FIELDS) | {
        "operator_attestation_timestamp_utc",
        "operator_reference",
    }
    if set(attestation) != required_keys:
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
            "operator attestation fields mismatch"
        )
    for field, value in expected.items():
        _expect(attestation.get(field), value, f"operator attestation {field}")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
                f"operator attestation {field} missing"
            )
    for field in ATTESTATION_BOOLEAN_FIELDS:
        _expect_true(attestation.get(field), f"operator attestation {field}")


def _selection_options_review() -> dict[str, dict[str, str]]:
    return deepcopy(SELECTION_OPTIONS_REVIEW)


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_operator_method_or_closure_selection_digest", None)
    return payload


def per_ticker_operator_method_or_closure_selection_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker selection entry."""
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
            "source_readiness_decision": closure_service.readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
            "source_closure_status": closure_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
            "selected_option": SELECTED_OPTION,
            "selection_status": "ACCEPTANCE_PATH_STOP_SELECTED_FOR_CURRENT_DATASET",
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_closure_digest": EXPECTED_CLOSURE_DIGEST,
            "source_readiness_digest": EXPECTED_READINESS_DIGEST,
            "selection_note": (
                "PRESERVE_META_LIMITATION_IN_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_operator_method_or_closure_selection_digest"] = (
            per_ticker_operator_method_or_closure_selection_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_selection(attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE_V1,
        "selection_status": OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_IMPROVED_EVIDENCE,
        "selection_scope": OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY,
        "selected_option": SELECTED_OPTION,
        "selection_decision": SELECTED_DECISION,
        "selection_rationale": SELECTION_RATIONALE,
        "created_offline": True,
        "research_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_closure_artifact_kind": closure_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE,
        "source_closure_status": closure_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "source_closure_decision": closure_service.CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
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
        "operator_method_or_closure_selection_created": True,
        "operator_method_or_closure_selection_ready": True,
        "selected_method_or_closure_option": SELECTED_OPTION,
        "selected_operator_decision": SELECTED_DECISION,
        "ready_for_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence": True,
        "method_or_evidence_improvement_candidate_created": False,
        "method_or_evidence_improvement_selected": False,
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
        "metric_recomputation_performed_in_selection": False,
        "model_training_performed_in_selection": False,
        "provider_requests_made_in_selection": False,
        "live_provider_transport_enabled_in_selection": False,
        "market_data_acquisition_performed_in_selection": False,
        "dataset_generation_performed_in_selection": False,
        "canonical_dataset_regenerated_in_selection": False,
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
        "readiness_decision": closure_service.readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "readiness_reason": closure_service.readiness.READINESS_REASON,
        "closure_status": closure_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "closure_decision": closure_service.CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
        "recommended_current_decision": closure_service.RECOMMENDED_CURRENT_DECISION,
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
        "selection_options_review": _selection_options_review(),
        "next_artifact_if_selected_path": NEXT_ARTIFACT_KIND,
        "archive_record_created": False,
        "method_improvement_candidate_created": False,
        "per_ticker_selection_entries": _per_ticker_entries(),
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
        isinstance(entry.get("per_ticker_operator_method_or_closure_selection_digest"), str)
        and entry["per_ticker_operator_method_or_closure_selection_digest"]
        == per_ticker_operator_method_or_closure_selection_using_improved_evidence_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(selection: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    attestation = selection.get("operator_attestation", {})
    options = selection.get("selection_options_review", {})
    entries = selection.get("per_ticker_selection_entries", [])
    unavailable = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    return [
        ("source_closure_digest_bound", EXPECTED_CLOSURE_DIGEST, selection.get("source_closure_digest")),
        ("source_readiness_digest_bound", EXPECTED_READINESS_DIGEST, selection.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", EXPECTED_REASSESSMENT_DIGEST, selection.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, selection.get("source_results_review_digest")),
        ("source_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, selection.get("source_execution_digest")),
        ("source_output_binding_digest_bound", EXPECTED_OUTPUT_BINDING_DIGEST, selection.get("source_output_binding_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, selection.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, selection.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, selection.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, selection.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, selection.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, selection.get("target_universe")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, selection.get("records_digest")),
        ("meta_913_preserved", 913, selection.get("meta_record_count")),
        ("operator_decision_matches", SELECTED_DECISION, attestation.get("operator_decision") if isinstance(attestation, dict) else None),
        ("operator_attestation_phrase_matches", REQUIRED_OPERATOR_METHOD_OR_CLOSURE_SELECTION_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase") if isinstance(attestation, dict) else None),
        ("selection_scope_only", OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY, selection.get("selection_scope")),
        ("selected_option_a_stop_current_dataset", SELECTED_OPTION, selection.get("selected_option")),
        ("selected_option_matches_source_recommendation", closure_service.RECOMMENDED_CURRENT_DECISION, selection.get("selected_option")),
        ("acceptance_candidate_option_not_allowed", "NOT_ALLOWED_CURRENTLY", options.get("OPTION_H_ACCEPTANCE_CANDIDATE", {}).get("selection_status") if isinstance(options, dict) else None),
        ("selection_created_true", True, selection.get("operator_method_or_closure_selection_created")),
        ("selection_ready_true", True, selection.get("operator_method_or_closure_selection_ready")),
        ("ready_for_archive_record_true", True, selection.get("ready_for_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence")),
        ("archive_record_created_false", False, selection.get("archive_record_created")),
        ("method_improvement_candidate_created_false", False, selection.get("method_improvement_candidate_created")),
        ("future_evidence_candidate_created_false", False, selection.get("future_evidence_candidate_created")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, selection.get("predictive_usefulness")),
        ("acceptance_ready_false", False, selection.get("predictive_usefulness_acceptance_ready")),
        ("acceptance_recommended_false", False, selection.get("predictive_usefulness_acceptance_recommended")),
        ("acceptance_candidate_created_false", False, selection.get("predictive_usefulness_acceptance_candidate_created")),
        ("profitability_not_accepted", NOT_ACCEPTED, selection.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, selection.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, selection.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, selection.get("broker_execution")),
        ("trade_recommendations_false", False, selection.get("trade_recommendations_generated")),
        ("label_regeneration_authorized_false", False, selection.get("label_regeneration_authorized")),
        ("label_regeneration_performed_false", False, selection.get("label_regeneration_performed")),
        ("new_targets_created_false", False, selection.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, selection.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, selection.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, selection.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, selection.get("feature_label_matrix_created")),
        ("metric_recomputation_in_selection_false", False, selection.get("metric_recomputation_performed_in_selection")),
        ("model_training_in_selection_false", False, selection.get("model_training_performed_in_selection")),
        ("predictive_evidence_rerun_false", False, selection.get("additional_predictive_evidence_execution_rerun_performed")),
        ("reassessment_rerun_false", False, selection.get("predictive_usefulness_reassessment_rerun_performed")),
        ("readiness_rerun_false", False, selection.get("predictive_usefulness_acceptance_readiness_rerun_performed")),
        ("matrix_rows_preserved", 143352, selection.get("matrix_row_count")),
        ("small_cross_sectional_edge_preserved", "0.00309917", selection.get("cross_sectional_delta_vs_majority")),
        ("local_model_equivalence_preserved", selection.get("majority_accuracy"), selection.get("local_model_accuracy")),
        ("optional_models_unavailable_preserved", [unavailable, unavailable], [selection.get("optional_tree_model_status"), selection.get("optional_ensemble_model_status")]),
        ("leakage_controls_passed", [True, 0, 8], [selection.get("leakage_control_passed"), selection.get("leakage_failed_control_count"), selection.get("leakage_control_count")]),
        ("meta_limitation_preserved", True, selection.get("meta_reduced_record_count_preserved")),
        ("selection_options_present", list(SELECTION_OPTIONS_REVIEW), list(options) if isinstance(options, dict) else []),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, selection.get("provider_requests_made_in_selection")),
        ("market_data_acquisition_false", False, selection.get("market_data_acquisition_performed_in_selection")),
        ("dataset_regeneration_false", False, selection.get("canonical_dataset_regenerated_in_selection")),
        ("raw_provider_payloads_not_committed", False, selection.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, selection.get("api_keys_stored_or_printed")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, selection.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, selection.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, selection.get("runtime_migration_approval_created")),
        ("next_chain_defined", NEXT_CHAIN, selection.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, selection.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, selection.get("risk_controls")),
        ("no_tracked_marketflow_files", True, selection.get("no_tracked_marketflow_files")),
    ]


def _checklist(selection: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(check_id, expected, actual) for check_id, expected, actual in _check_definitions(selection)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "operator_selection_created": not failed,
        "selected_option": SELECTED_OPTION,
        "selected_decision": SELECTED_DECISION,
        "ready_for_archive_record": not failed,
        "archive_record_created": False,
        "method_improvement_candidate_created": False,
        "future_evidence_candidate_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(selection: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(selection))
    payload.pop("operator_method_or_closure_selection_using_improved_evidence_digest", None)
    return payload


def operator_method_or_closure_selection_using_improved_evidence_digest_v1(
    selection: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the selection artifact."""
    return semantic_digest(_digest_payload(selection))


def build_operator_method_or_closure_selection_using_improved_evidence_v1(
    *, operator_attestation: dict
) -> dict:
    """Build the selection after validating the exact non-secret attestation."""
    _validate_attestation(operator_attestation)
    selection = _base_selection(operator_attestation)
    checklist = _checklist(selection)
    selection["selection_checklist"] = checklist
    selection["selection_summary"] = _summary(checklist)
    selection["operator_method_or_closure_selection_using_improved_evidence_digest"] = (
        operator_method_or_closure_selection_using_improved_evidence_digest_v1(selection)
    )
    validate_operator_method_or_closure_selection_using_improved_evidence_v1(selection)
    return selection


def validate_operator_method_or_closure_selection_using_improved_evidence_v1(
    selection: dict,
) -> dict:
    """Validate attestation, evidence bindings, selected option, and closed gates."""
    if not isinstance(selection, dict):
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
            "selection must be an object"
        )
    _validate_attestation(selection.get("operator_attestation"))

    expected_fields = {
        "artifact_kind": ARTIFACT_KIND_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE_V1,
        "selection_status": OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_IMPROVED_EVIDENCE,
        "selection_scope": OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY,
        "selected_option": SELECTED_OPTION,
        "selection_decision": SELECTED_DECISION,
        "selection_rationale": SELECTION_RATIONALE,
        "source_closure_artifact_kind": closure_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE,
        "source_closure_status": closure_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "source_closure_decision": closure_service.CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
        "source_closure_digest": EXPECTED_CLOSURE_DIGEST,
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest": EXPECTED_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_READINESS_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": EXPECTED_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "selected_method_or_closure_option": SELECTED_OPTION,
        "selected_operator_decision": SELECTED_DECISION,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "readiness_decision": closure_service.readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "readiness_reason": closure_service.readiness.READINESS_REASON,
        "closure_status": closure_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "closure_decision": closure_service.CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
        "recommended_current_decision": closure_service.RECOMMENDED_CURRENT_DECISION,
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
        "selection_options_review": SELECTION_OPTIONS_REVIEW,
        "next_artifact_if_selected_path": NEXT_ARTIFACT_KIND,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    expected_fields.update(SOURCE_EVIDENCE)
    for field, value in expected_fields.items():
        _expect(selection.get(field), value, field)

    true_fields = (
        "created_offline",
        "research_only",
        "operator_attestation_required",
        "operator_method_or_closure_selection_created",
        "operator_method_or_closure_selection_ready",
        "ready_for_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence",
        "leakage_control_passed",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(selection.get(field), field)

    false_fields = (
        "method_or_evidence_improvement_candidate_created",
        "method_or_evidence_improvement_selected",
        "future_evidence_candidate_created",
        "future_evidence_execution_created",
        "future_reassessment_created",
        "future_readiness_review_created",
        "archive_record_created",
        "method_improvement_candidate_created",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_ceremony_allowed",
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
        "metric_recomputation_performed_in_selection",
        "model_training_performed_in_selection",
        "provider_requests_made_in_selection",
        "live_provider_transport_enabled_in_selection",
        "market_data_acquisition_performed_in_selection",
        "dataset_generation_performed_in_selection",
        "canonical_dataset_regenerated_in_selection",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
        "additional_predictive_evidence_execution_rerun_performed",
        "predictive_usefulness_reassessment_rerun_performed",
        "predictive_usefulness_acceptance_readiness_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    )
    for field in false_fields:
        _expect_false(selection.get(field), field)

    options = selection.get("selection_options_review")
    if not isinstance(options, dict) or list(options) != list(SELECTION_OPTIONS_REVIEW):
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
            "selection options mismatch"
        )
    for option, expected in SELECTION_OPTIONS_REVIEW.items():
        _expect(options.get(option), expected, f"{option} selection option")
    _expect(
        options[SELECTED_OPTION]["selection_status"],
        "SELECTED_BY_OPERATOR",
        "selected Option A",
    )
    _expect(
        options["OPTION_H_ACCEPTANCE_CANDIDATE"]["selection_status"],
        "NOT_ALLOWED_CURRENTLY",
        "acceptance candidate option",
    )

    entries = selection.get("per_ticker_selection_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
            "per-ticker selection entries mismatch"
        )
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("selected_option"), SELECTED_OPTION, f"{ticker} selected option")
        _expect(entry.get("source_closure_digest"), EXPECTED_CLOSURE_DIGEST, f"{ticker} closure digest")
        _expect(entry.get("source_readiness_digest"), EXPECTED_READINESS_DIGEST, f"{ticker} readiness digest")
        _expect(entry.get("predictive_usefulness"), NOT_ACCEPTED, f"{ticker} usefulness")
        _expect(entry.get("profitability"), NOT_ACCEPTED, f"{ticker} profitability")
        _expect_false(entry.get("predictive_usefulness_acceptance_ready"), f"{ticker} acceptance ready")
        _expect_false(entry.get("predictive_usefulness_acceptance_candidate_created"), f"{ticker} candidate")
        _expect_false(entry.get("trade_recommendations_generated"), f"{ticker} recommendations")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        if ticker == "META":
            _expect(
                entry.get("selection_note"),
                "PRESERVE_META_LIMITATION_IN_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE",
                "META selection_note",
            )
        digest = entry.get("per_ticker_operator_method_or_closure_selection_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
                f"{ticker} per-ticker digest missing"
            )
        _expect(
            digest,
            per_ticker_operator_method_or_closure_selection_using_improved_evidence_digest_v1(entry),
            f"{ticker} per-ticker digest",
        )

    checklist = selection.get("selection_checklist")
    expected_check_ids = [definition[0] for definition in _check_definitions(selection)]
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != expected_check_ids:
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
            "selection checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
            "selection checklist failed"
        )
    _expect(selection.get("selection_summary"), _summary(checklist), "selection summary")

    digest = selection.get("operator_method_or_closure_selection_using_improved_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError("selection digest missing")
    _expect(
        digest,
        operator_method_or_closure_selection_using_improved_evidence_digest_v1(selection),
        "selection digest",
    )
    return {
        "status": "OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE_VALID",
        "artifact_kind": selection["artifact_kind"],
        "selection_status": selection["selection_status"],
        "selected_option": selection["selected_option"],
        "operator_method_or_closure_selection_using_improved_evidence_digest": digest,
        **{
            key: selection["selection_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_operator_method_or_closure_selection_using_improved_evidence_markdown_v1(
    selection: dict,
) -> str:
    """Render a sanitized Markdown view of the validated selection artifact."""
    validation = validate_operator_method_or_closure_selection_using_improved_evidence_v1(
        selection
    )
    attestation = selection["operator_attestation"]
    sections = [
        ("Title", ["Operator Method or Closure Selection Using Improved Evidence"]),
        (
            "Operator Method or Closure Selection Using Improved Evidence",
            [
                f"Artifact/status/scope: `{selection['artifact_kind']}` / `{selection['selection_status']}` / `{selection['selection_scope']}`.",
                f"Digest: `{validation['operator_method_or_closure_selection_using_improved_evidence_digest']}`.",
            ],
        ),
        (
            "Operator Attestation",
            [
                f"Reference/timestamp/version: `{attestation['operator_reference']}` / `{attestation['operator_attestation_timestamp_utc']}` / `{attestation['operator_attestation_version']}`.",
                f"Decision/option: `{attestation['operator_decision']}` / `{attestation['selected_option']}`.",
                "The attestation is non-secret and confirms every selection-only boundary.",
            ],
        ),
        (
            "Source Closure",
            [
                f"Artifact/status: `{selection['source_closure_artifact_kind']}` / `{selection['source_closure_status']}`.",
                f"Decision/digest: `{selection['source_closure_decision']}` / `{selection['source_closure_digest']}`.",
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Readiness/reassessment/results review: `{selection['source_readiness_digest']}` / `{selection['source_reassessment_digest']}` / `{selection['source_results_review_digest']}`.",
                f"Matrix/features/labels: `{selection['feature_label_matrix_digest']}` / `{selection['feature_values_digest']}` / `{selection['redesigned_label_values_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"Dataset/records: `{selection['dataset_name']}` / `{selection['total_canonical_record_count']}`.",
                "Universe: " + ", ".join(f"`{ticker}`" for ticker in selection["target_universe"]) + ".",
                "META remains `913`; each non-META ticker remains `1003`.",
            ],
        ),
        (
            "Selection Decision",
            [
                f"Selected option/decision: `{selection['selected_option']}` / `{selection['selection_decision']}`.",
                f"Rationale: `{selection['selection_rationale']}`.",
            ],
        ),
        (
            "Selection Basis",
            [
                f"Readiness/closure: `{selection['readiness_decision']}` / `{selection['closure_status']}`.",
                f"Source recommendation: `{selection['recommended_current_decision']}`.",
            ],
        ),
        (
            "Evidence Summary",
            [
                f"Matrix/evaluable/unavailable/OOS: `{selection['matrix_row_count']} / {selection['evaluable_matrix_row_count']} / {selection['unavailable_target_count']} / {selection['oos_row_count']}`.",
                f"Majority/local/cross-sectional accuracy: `{selection['majority_accuracy']} / {selection['local_model_accuracy']} / {selection['cross_sectional_accuracy']}`.",
            ],
        ),
        (
            "Selection Options Review",
            [
                f"`{name}`: source `{value['source_status']}`, selection `{value['selection_status']}`."
                for name, value in selection["selection_options_review"].items()
            ],
        ),
        ("Selected Option", [f"`{selection['selected_option']}` is selected for the current dataset and evidence set only."]),
        (
            "Next Artifact",
            [
                f"Planned kind: `{selection['next_artifact_if_selected_path']}`.",
                "The archive record is not created by this selection.",
            ],
        ),
        (
            "Per-Ticker Selection",
            [
                f"`{row['ticker']}`: `{row['selection_status']}`, records `{row['historical_record_count']}`, digest `{row['per_ticker_operator_method_or_closure_selection_digest']}`."
                for row in selection["per_ticker_selection_entries"]
            ],
        ),
        ("Next Chain", selection["next_chain"]),
        ("Next Gates", selection["next_gates"]),
        ("Risk Controls", selection["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate or ceremony is created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{selection['selection_summary']['total_checks']} / {selection['selection_summary']['passed_checks']} / {selection['selection_summary']['failed_checks']} / {selection['selection_summary']['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            ["No archive record, future candidate, provider, acquisition, regeneration, evidence/reassessment/readiness rerun, metric recomputation, model training, acceptance, runtime, broker, or trading action occurred."],
        ),
    ]
    lines = ["# Operator Method or Closure Selection Using Improved Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_operator_method_or_closure_selection_using_improved_evidence_v1(
    output_dir: str | Path,
    *,
    operator_attestation: dict,
) -> dict:
    """Write canonical selection JSON without overwriting an existing artifact."""
    selection = build_operator_method_or_closure_selection_using_improved_evidence_v1(
        operator_attestation=operator_attestation
    )
    validation = validate_operator_method_or_closure_selection_using_improved_evidence_v1(
        selection
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "operator_method_or_closure_selection_using_improved_evidence_v1.json"
    if path.exists():
        raise OperatorMethodOrClosureSelectionImprovedEvidenceError(
            "selection output already exists"
        )
    payload = canonical_json_bytes(selection)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": selection["artifact_kind"],
        "selection_status": selection["selection_status"],
        "selected_option": selection["selected_option"],
        "operator_method_or_closure_selection_using_improved_evidence_digest": validation[
            "operator_method_or_closure_selection_using_improved_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
