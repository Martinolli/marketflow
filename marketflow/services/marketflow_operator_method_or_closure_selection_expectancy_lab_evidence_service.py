"""Offline, attestation-bound operator selection for expectancy-lab evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_service as closure_service,
)


ARTIFACT_KIND_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE"
)
SCHEMA_VERSION_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_V1 = (
    "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1"
)
MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_EXPECTANCY_LAB_EVIDENCE"
)
OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY_NOT_ARCHIVE_NOT_ACCEPTANCE_NOT_RUNTIME = (
    "OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY_NOT_ARCHIVE_NOT_ACCEPTANCE_NOT_RUNTIME"
)
SELECTED_OPERATOR_OPTION = "OPTION_A_ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY"
SELECTED_OPERATOR_DECISION = "SELECT_ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY"
OPERATOR_DECISION = "SELECT_OPERATOR_METHOD_OR_CLOSURE"
OPERATOR_ATTESTATION_VERSION = (
    "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_attestation_v1"
)
REQUIRED_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_ATTESTATION_PHRASE = (
    "SELECT OPTION_A ARCHIVE CURRENT EXPECTANCY LAB EVIDENCE PATH AS NOT READY "
    "MARKETFLOW EXPECTANCY LAB EVIDENCE MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY_NOT_ARCHIVE_NOT_ACCEPTANCE_NOT_RUNTIME"
)
MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_VALID = (
    "MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_VALID"
)

EXPECTED_SOURCE_CLOSURE_DIGEST = "4d0c1c490c794aef2401440d4ca54127aec198cabeee0b8557ca1b168c23bf0f"
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = closure_service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = closure_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = closure_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_EXECUTION_DIGEST = closure_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = closure_service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = closure_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = closure_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = closure_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = closure_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = closure_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = closure_service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = closure_service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = closure_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = closure_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = closure_service.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(closure_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(closure_service.EXPECTED_RECORD_COUNTS)
EXPECTED_LAB_ROW_COUNTS = dict(closure_service.EXPECTED_LAB_ROW_COUNTS)
EXPECTED_EVALUABLE_COUNTS = dict(closure_service.EXPECTED_EVALUABLE_COUNTS)
EXPECTED_UNAVAILABLE_COUNTS = dict(closure_service.EXPECTED_UNAVAILABLE_COUNTS)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_selection_scope_only",
    "operator_confirms_archive_record_not_created",
    "operator_confirms_method_improvement_candidate_not_created",
    "operator_confirms_new_evidence_candidate_not_created",
    "operator_confirms_acceptance_candidate_not_created",
    "operator_confirms_predictive_usefulness_not_accepted",
    "operator_confirms_profitability_not_accepted",
    "operator_confirms_runtime_not_authorized",
    "operator_confirms_no_strategy_authorization",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

NEXT_CHAIN = [
    "Predictive-Usefulness Acceptance Path Archive Record Using Expectancy Lab Evidence v1.",
    "Future reopening only by a new operator method selection artifact.",
    "Optional future method/evidence improvement candidate only if separately selected later.",
    "New evidence chain only if separately approved later.",
    "Reassessment/readiness rerun only after new evidence.",
    "Predictive-usefulness acceptance candidate only if a future readiness review passes.",
    "Profitability review only after predictive usefulness is separately accepted.",
    "Runtime migration only if ever separately authorized.",
]

NEXT_GATES = [
    "predictive_usefulness_acceptance_path_archive_record_using_expectancy_lab_evidence",
    "future_operator_method_selection_if_reopened",
    "optional_future_method_or_evidence_improvement_candidate",
    "new_evidence_chain_if_separately_approved",
    "future_predictive_usefulness_reassessment_rerun",
    "future_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_if_predictive_usefulness_accepted",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "selection_does_not_create_archive_record",
    "selection_does_not_create_method_improvement_candidate",
    "selection_does_not_create_new_evidence_candidate",
    "selection_does_not_create_acceptance_candidate",
    "selection_does_not_accept_predictive_usefulness",
    "selection_does_not_accept_profitability",
    "selection_does_not_authorize_runtime",
    "selection_does_not_authorize_strategy",
    "selection_does_not_authorize_paper_trading",
    "selection_does_not_authorize_broker_execution",
    "selection_does_not_generate_trade_recommendations",
    "selection_does_not_train_models",
    "selection_does_not_score_strategy",
    "selection_does_not_call_providers",
    "selection_does_not_acquire_market_data",
    "selection_does_not_recompute_metrics_from_raw_rows",
    "selection_does_not_rerun_closure",
    "selection_does_not_rerun_acceptance_readiness_review",
    "selection_does_not_rerun_predictive_usefulness_reassessment",
    "selection_does_not_rerun_expectancy_backtest_lab_execution",
    "selection_does_not_rerun_expectancy_backtest_lab_results_review",
    "selection_does_not_rerun_vpa_wyckoff_execution",
    "selection_does_not_rerun_vpa_wyckoff_results_review",
    "selection_does_not_rerun_feature_label_matrix_execution",
    "selection_does_not_rerun_feature_label_matrix_results_review",
    "selection_does_not_rerun_signal_feature_generation",
    "selection_does_not_rerun_target_generation",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_expectancy_backtest_lab_outputs",
    "do_not_mutate_vpa_wyckoff_outputs",
    "do_not_mutate_matrix_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_closure_digest_bound", "source_acceptance_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_results_review_digest_bound",
    "source_backtest_rows_digest_bound", "source_metric_report_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound", "source_matrix_rows_digest_bound",
    "source_target_values_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "operator_decision_matches", "operator_attestation_phrase_matches", "selection_scope_only",
    "selected_option_option_a", "selected_decision_archive_current_path",
    "source_recommended_option_a_bound", "operator_selection_created_true",
    "operator_selection_completed_true", "ready_for_archive_record_true",
    "archive_record_created_false", "method_improvement_candidate_created_false",
    "new_evidence_candidate_created_false", "acceptance_candidate_created_false",
    "predictive_usefulness_not_accepted", "predictive_usefulness_accepted_false",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "paper_trading_not_authorized",
    "broker_not_authorized", "trade_recommendations_false",
    "option_a_selected_for_archive_record_not_created",
    "options_b_to_f_available_not_selected", "option_g_blocked", "option_h_not_allowed",
    "source_backtest_lab_row_count_179190", "evaluable_target_row_count_177090",
    "unavailable_target_row_count_2100", "embargoed_cross_split_forward_horizon_row_count_4200",
    "aggregate_metric_eligible_row_count_172890", "per_ticker_entries_12",
    "per_ticker_digests_present", "model_training_authorized_false",
    "model_training_performed_false", "strategy_scoring_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "metric_recomputation_from_raw_rows_false", "closure_rerun_false",
    "acceptance_readiness_review_rerun_false", "predictive_usefulness_reassessment_rerun_false",
    "expectancy_backtest_lab_execution_rerun_false",
    "expectancy_backtest_lab_results_review_rerun_false", "vpa_wyckoff_execution_rerun_false",
    "vpa_wyckoff_results_review_rerun_false", "matrix_execution_rerun_false",
    "matrix_results_review_rerun_false", "signal_feature_generation_rerun_false",
    "target_generation_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(ValueError):
    """Raised when the operator selection violates its attestation or boundaries."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            f"{field} mismatch"
        )


def build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_closure_digest: str,
    operator_confirms_acceptance_readiness_digest: str,
    operator_confirms_reassessment_digest: str,
    operator_confirms_results_review_digest: str,
    operator_confirms_backtest_rows_digest: str,
    operator_confirms_metric_report_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_option: str,
    operator_confirms_selection_scope_only: bool,
    operator_confirms_archive_record_not_created: bool,
    operator_confirms_method_improvement_candidate_not_created: bool,
    operator_confirms_new_evidence_candidate_not_created: bool,
    operator_confirms_acceptance_candidate_not_created: bool,
    operator_confirms_predictive_usefulness_not_accepted: bool,
    operator_confirms_profitability_not_accepted: bool,
    operator_confirms_runtime_not_authorized: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_operator_option: str = SELECTED_OPERATOR_OPTION,
    selected_operator_decision: str = SELECTED_OPERATOR_DECISION,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build the exact non-secret operator attestation object."""
    return {
        "operator_decision": operator_decision,
        "selected_operator_option": selected_operator_option,
        "selected_operator_decision": selected_operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_reference": operator_reference,
        "operator_confirms_source_closure_digest": operator_confirms_source_closure_digest,
        "operator_confirms_acceptance_readiness_digest": operator_confirms_acceptance_readiness_digest,
        "operator_confirms_reassessment_digest": operator_confirms_reassessment_digest,
        "operator_confirms_results_review_digest": operator_confirms_results_review_digest,
        "operator_confirms_backtest_rows_digest": operator_confirms_backtest_rows_digest,
        "operator_confirms_metric_report_digest": operator_confirms_metric_report_digest,
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
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "operator attestation missing"
        )
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_operator_option": SELECTED_OPERATOR_OPTION,
        "selected_operator_decision": SELECTED_OPERATOR_DECISION,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "operator_confirms_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "operator_confirms_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "operator_confirms_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "operator_confirms_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "operator_confirms_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "operator_confirms_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_option": SELECTED_OPERATOR_OPTION,
    }
    required = set(expected) | set(ATTESTATION_BOOLEAN_FIELDS) | {
        "operator_attestation_timestamp_utc", "operator_reference"
    }
    if set(attestation) != required:
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "operator attestation fields mismatch"
        )
    for field, value in expected.items():
        _expect(attestation.get(field), value, f"operator attestation {field}")
    for field in ("operator_attestation_timestamp_utc", "operator_reference"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
                f"operator attestation {field} missing"
            )
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
                f"operator attestation {field} must be true"
            )


def _validate_source_closure(source_closure: Mapping[str, Any]) -> None:
    if not isinstance(source_closure, dict):
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "source_closure must be an object"
        )
    try:
        closure_service.validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(
            source_closure
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "source closure is invalid"
        ) from exc
    if source_closure.get(
        "marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"
    ) != EXPECTED_SOURCE_CLOSURE_DIGEST:
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "source closure digest mismatch"
        )


def _source_evidence(source_closure: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_closure is not None:
        _validate_source_closure(source_closure)
        return deepcopy(source_closure["source_evidence"])
    return closure_service._source_evidence(None)


def _selection_options() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for option_id, source in closure_service.METHOD_PLANNING_TREE.items():
        if option_id == SELECTED_OPERATOR_OPTION:
            status_after = "SELECTED_FOR_ARCHIVE_RECORD_NOT_CREATED"
        elif option_id.startswith(("OPTION_B_", "OPTION_C_", "OPTION_D_", "OPTION_E_", "OPTION_F_")):
            status_after = "AVAILABLE_FOR_FUTURE_OPERATOR_SELECTION_NOT_SELECTED"
        elif option_id.startswith("OPTION_G_"):
            status_after = "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE"
        else:
            status_after = "NOT_ALLOWED_CURRENTLY"
        rows[option_id] = {
            "option_id": option_id,
            "option_status_before_selection": source["option_status"],
            "option_status_after_selection": status_after,
            "status_after_selection": status_after,
            "selected_by_operator": option_id == SELECTED_OPERATOR_OPTION,
            "selected_for_archive_record": option_id == SELECTED_OPERATOR_OPTION,
            "archive_record_created": False,
            "creates_acceptance_candidate": False,
            "creates_runtime_authority": False,
            "research_only": True,
            "non_actionable": True,
        }
    return rows


def per_ticker_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker selection entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_operator_method_or_closure_selection_digest", None)
    return semantic_digest(payload)


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
            "source_closure_status": closure_service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
            "operator_selection_status": "SELECTED_ARCHIVE_CURRENT_PATH_NOT_READY",
            "selected_operator_option": SELECTED_OPERATOR_OPTION,
            "selected_operator_decision": SELECTED_OPERATOR_DECISION,
            "backtest_lab_row_count": EXPECTED_LAB_ROW_COUNTS[ticker],
            "evaluable_target_row_count": EXPECTED_EVALUABLE_COUNTS[ticker],
            "unavailable_target_row_count": EXPECTED_UNAVAILABLE_COUNTS[ticker],
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_accepted": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_recommended": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
            "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
            "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
            "selection_note": (
                "PRESERVE_META_LIMITATION_IN_OPERATOR_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_operator_method_or_closure_selection_digest"] = (
            per_ticker_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_selection(
    attestation: Mapping[str, Any], source_closure: Mapping[str, Any] | None
) -> dict[str, Any]:
    execution = closure_service.readiness.reassessment.execution
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_V1,
        "selection_status": MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_EXPECTANCY_LAB_EVIDENCE,
        "selection_scope": OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY_NOT_ARCHIVE_NOT_ACCEPTANCE_NOT_RUNTIME,
        "selected_operator_option": SELECTED_OPERATOR_OPTION,
        "selected_operator_decision": SELECTED_OPERATOR_DECISION,
        "created_offline": True, "research_only": True, "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_closure_artifact_kind": closure_service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_closure_status": closure_service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_closure_decision": closure_service.CLOSE_CURRENT_EXPECTANCY_LAB_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_OR_ARCHIVE_SELECTION,
        "source_closure_scope": closure_service.PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_expectancy_backtest_lab_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_expectancy_backtest_lab_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_expectancy_backtest_lab_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_closure),
        "selected_backtest_lab_package": execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "operator_method_or_closure_selection_created": True,
        "operator_method_or_closure_selection_completed": True,
        "ready_for_predictive_usefulness_acceptance_path_archive_record": True,
        "archive_record_created": False, "method_improvement_candidate_created": False,
        "new_evidence_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "profitability_acceptance_ready": False, "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False, "model_training_authorized": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "new_strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "provider_requests_made_in_selection": False,
        "live_provider_transport_enabled_in_selection": False,
        "market_data_acquisition_performed_in_selection": False,
        "dataset_generation_performed_in_selection": False,
        "canonical_dataset_regenerated_in_selection": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "closure_rerun_performed": False, "acceptance_readiness_review_rerun_performed": False,
        "predictive_usefulness_reassessment_rerun_performed": False,
        "expectancy_backtest_lab_execution_rerun_performed": False,
        "expectancy_backtest_lab_results_review_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False,
        "target_generation_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "source_closure_recommended_current_decision": closure_service.RECOMMENDED_CURRENT_DECISION,
        "source_readiness_decision": closure_service.readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_closure_classification": "COMPLETED_RESEARCH_ONLY",
        "source_acceptance_path_status": "CLOSED_NOT_READY",
        "metric_materiality_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "per_ticker_stability_readiness": "REQUIRES_OPERATOR_REVIEW",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "source_matrix_row_count": 179190, "expectancy_backtest_lab_row_count": 179190,
        "evaluable_target_row_count": 177090, "unavailable_target_row_count": 2100,
        "embargoed_cross_split_forward_horizon_row_count": 4200,
        "aggregate_metric_eligible_row_count": 172890,
        "selection_options": _selection_options(),
        "per_ticker_selection_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(row, dict)
        and row.get("per_ticker_operator_method_or_closure_selection_digest")
        == per_ticker_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest_v1(row)
        for row in entries
    )


def _check_values(selection: Mapping[str, Any]) -> dict[str, bool]:
    attestation = selection.get("operator_attestation")
    options = selection.get("selection_options")
    entries = selection.get("per_ticker_selection_entries")
    option = lambda key: options.get(key, {}) if isinstance(options, dict) else {}
    option_a = option(SELECTED_OPERATOR_OPTION)
    return {
        "source_closure_digest_bound": selection.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_acceptance_readiness_digest_bound": selection.get("source_acceptance_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": selection.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": selection.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": selection.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": selection.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": selection.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": selection.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": selection.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": selection.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": selection.get("target_universe") == TARGET_UNIVERSE and selection.get("target_universe_count") == 12,
        "records_digest_preserved": selection.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": selection.get("meta_record_count") == 913,
        "operator_decision_matches": isinstance(attestation, dict) and attestation.get("operator_decision") == OPERATOR_DECISION,
        "operator_attestation_phrase_matches": isinstance(attestation, dict) and attestation.get("operator_attestation_phrase") == REQUIRED_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_ATTESTATION_PHRASE,
        "selection_scope_only": selection.get("selection_scope") == OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY_NOT_ARCHIVE_NOT_ACCEPTANCE_NOT_RUNTIME,
        "selected_option_option_a": selection.get("selected_operator_option") == SELECTED_OPERATOR_OPTION,
        "selected_decision_archive_current_path": selection.get("selected_operator_decision") == SELECTED_OPERATOR_DECISION,
        "source_recommended_option_a_bound": selection.get("source_closure_recommended_current_decision") == SELECTED_OPERATOR_OPTION,
        "operator_selection_created_true": selection.get("operator_method_or_closure_selection_created") is True,
        "operator_selection_completed_true": selection.get("operator_method_or_closure_selection_completed") is True,
        "ready_for_archive_record_true": selection.get("ready_for_predictive_usefulness_acceptance_path_archive_record") is True,
        "archive_record_created_false": selection.get("archive_record_created") is False,
        "method_improvement_candidate_created_false": selection.get("method_improvement_candidate_created") is False,
        "new_evidence_candidate_created_false": selection.get("new_evidence_candidate_created") is False,
        "acceptance_candidate_created_false": selection.get("predictive_usefulness_acceptance_candidate_created") is False,
        "predictive_usefulness_not_accepted": selection.get("predictive_usefulness") == NOT_ACCEPTED,
        "predictive_usefulness_accepted_false": selection.get("predictive_usefulness_accepted") is False,
        "predictive_usefulness_acceptance_ready_false": selection.get("predictive_usefulness_acceptance_ready") is False,
        "predictive_usefulness_acceptance_recommended_false": selection.get("predictive_usefulness_acceptance_recommended") is False,
        "profitability_not_accepted": selection.get("profitability") == NOT_ACCEPTED and selection.get("profitability_accepted") is False,
        "runtime_not_authorized": selection.get("runtime_use") == NOT_AUTHORIZED and selection.get("runtime_migration_approved") is False,
        "strategy_not_authorized": selection.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": selection.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": selection.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": selection.get("trade_recommendations_generated") is False,
        "option_a_selected_for_archive_record_not_created": option_a.get("option_status_after_selection") == "SELECTED_FOR_ARCHIVE_RECORD_NOT_CREATED" and option_a.get("selected_for_archive_record") is True and option_a.get("archive_record_created") is False,
        "options_b_to_f_available_not_selected": isinstance(options, dict) and all(row.get("status_after_selection") == "AVAILABLE_FOR_FUTURE_OPERATOR_SELECTION_NOT_SELECTED" and row.get("selected_by_operator") is False for row in list(options.values())[1:6]),
        "option_g_blocked": option("OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED").get("status_after_selection") == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE",
        "option_h_not_allowed": option("OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE").get("status_after_selection") == "NOT_ALLOWED_CURRENTLY",
        "source_backtest_lab_row_count_179190": selection.get("expectancy_backtest_lab_row_count") == 179190,
        "evaluable_target_row_count_177090": selection.get("evaluable_target_row_count") == 177090,
        "unavailable_target_row_count_2100": selection.get("unavailable_target_row_count") == 2100,
        "embargoed_cross_split_forward_horizon_row_count_4200": selection.get("embargoed_cross_split_forward_horizon_row_count") == 4200,
        "aggregate_metric_eligible_row_count_172890": selection.get("aggregate_metric_eligible_row_count") == 172890,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "model_training_authorized_false": selection.get("model_training_authorized") is False,
        "model_training_performed_false": selection.get("model_training_performed") is False,
        "strategy_scoring_false": selection.get("strategy_scoring_performed") is False and selection.get("new_strategy_scoring_performed") is False,
        "provider_requests_made_false": selection.get("provider_requests_made_in_selection") is False,
        "market_data_acquisition_false": selection.get("market_data_acquisition_performed_in_selection") is False,
        "dataset_regeneration_false": selection.get("canonical_dataset_regenerated_in_selection") is False,
        "metric_recomputation_from_raw_rows_false": selection.get("metric_recomputation_from_raw_rows_performed") is False,
        "closure_rerun_false": selection.get("closure_rerun_performed") is False,
        "acceptance_readiness_review_rerun_false": selection.get("acceptance_readiness_review_rerun_performed") is False,
        "predictive_usefulness_reassessment_rerun_false": selection.get("predictive_usefulness_reassessment_rerun_performed") is False,
        "expectancy_backtest_lab_execution_rerun_false": selection.get("expectancy_backtest_lab_execution_rerun_performed") is False,
        "expectancy_backtest_lab_results_review_rerun_false": selection.get("expectancy_backtest_lab_results_review_rerun_performed") is False,
        "vpa_wyckoff_execution_rerun_false": selection.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": selection.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": selection.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": selection.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": selection.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": selection.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": selection.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": selection.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": selection.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": selection.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": selection.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": selection.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "selection evidence matches" if actual else "selection evidence mismatch",
    }


def _checklist(selection: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(selection)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "operator_method_or_closure_selection_created": True,
        "operator_method_or_closure_selection_completed": True,
        "selected_operator_option": SELECTED_OPERATOR_OPTION,
        "selected_operator_decision": SELECTED_OPERATOR_DECISION,
        "ready_for_predictive_usefulness_acceptance_path_archive_record": True,
        "archive_record_created": False, "method_improvement_candidate_created": False,
        "new_evidence_candidate_created": False, "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "next_recommended_task": "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE_V1",
    }


def marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest_v1(
    selection: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the selection artifact."""
    payload = deepcopy(dict(selection))
    payload.pop("selection_checklist", None)
    payload.pop("selection_summary", None)
    payload.pop("marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest", None)
    return semantic_digest(payload)


def build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
    *, source_closure: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build the selection after exact attestation validation, without source reruns."""
    _validate_attestation(operator_attestation)
    selection = _base_selection(operator_attestation, source_closure)
    selection["selection_checklist"] = _checklist(selection)
    selection["selection_summary"] = _summary(selection["selection_checklist"])
    selection["marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"] = (
        marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest_v1(selection)
    )
    validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(selection)
    return selection


def validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
    selection: dict,
) -> dict:
    """Validate attestation, source bindings, selection, and closed authority gates."""
    if not isinstance(selection, dict):
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "selection must be an object"
        )
    _validate_attestation(selection.get("operator_attestation"))
    expected = _base_selection(selection["operator_attestation"], None)
    for field, value in expected.items():
        _expect(selection.get(field), value, field)
    entries = selection.get("per_ticker_selection_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "per-ticker selection entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    if not _per_ticker_digests_valid(entries):
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "per-ticker selection digest mismatch"
        )
    checklist = selection.get("selection_checklist")
    if not isinstance(checklist, list):
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "selection checklist missing"
        )
    _expect(checklist, _checklist(selection), "selection checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "selection checklist failed"
        )
    _expect(selection.get("selection_summary"), _summary(checklist), "selection summary")
    digest = selection.get(
        "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "selection digest missing"
        )
    _expect(
        digest,
        marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest_v1(selection),
        "selection digest",
    )
    return {
        "status": MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_VALID,
        "artifact_kind": selection["artifact_kind"],
        "selection_status": selection["selection_status"],
        "selected_operator_option": selection["selected_operator_option"],
        "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest": digest,
        **{
            key: selection["selection_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_markdown_v1(
    selection: dict,
) -> str:
    """Render a sanitized Markdown view of the validated selection."""
    validation = validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(selection)
    attestation = selection["operator_attestation"]
    sections = [
        ("Title", ["Operator Method or Closure Selection Using Expectancy Lab Evidence v1"]),
        ("Operator Method or Closure Selection Using Expectancy Lab Evidence v1", [f"Artifact/status: `{selection['artifact_kind']}` / `{selection['selection_status']}`.", f"Digest: `{validation['marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest']}`."]),
        ("Operator Attestation", [f"Reference/version: `{attestation['operator_reference']}` / `{attestation['operator_attestation_version']}`.", "The exact non-secret phrase and all closed-boundary confirmations were validated."]),
        ("Source Closure", [f"Status: `{selection['source_closure_status']}`.", f"Digest: `{selection['source_closure_digest']}`."]),
        ("Bound Evidence", [f"Readiness/reassessment: `{selection['source_acceptance_readiness_digest']}` / `{selection['source_reassessment_digest']}`.", f"Rows/metrics: `{selection['source_backtest_rows_digest']}` / `{selection['source_metric_report_digest']}`."]),
        ("Dataset and Universe", [f"`{selection['dataset_name']}` has `{selection['total_canonical_record_count']}` records across `{selection['target_universe_count']}` tickers.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in selection["target_universe"]) + "."]),
        ("Selection Scope", [f"`{selection['selection_scope']}`; archive creation and all acceptance/runtime authority remain outside scope."]),
        ("Selected Option", [f"`{selection['selected_operator_option']}` / `{selection['selected_operator_decision']}`.", "Option A is selected for a future archive record; the archive record is not created."]),
        ("Selection Basis", [f"Source path: `{selection['source_acceptance_path_status']}`; materiality/baseline/stability: `{selection['metric_materiality_readiness']} / {selection['baseline_outperformance_readiness']} / {selection['per_ticker_stability_readiness']}`."]),
        ("Unselected Options", [f"`{option_id}`: `{row['status_after_selection']}`." for option_id, row in selection["selection_options"].items() if option_id != SELECTED_OPERATOR_OPTION]),
        ("Per-Ticker Selection", [f"`{row['ticker']}`: `{row['operator_selection_status']}`, digest `{row['per_ticker_operator_method_or_closure_selection_digest']}`." for row in selection["per_ticker_selection_entries"]]),
        ("META Limitation", ["META remains exactly 913 historical records; its reduced-record limitation is preserved."]),
        ("Next Chain", selection["next_chain"]), ("Next Gates", selection["next_gates"]),
        ("Risk Controls", selection["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate is created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{selection['selection_summary']['total_checks']} / {selection['selection_summary']['passed_checks']} / {selection['selection_summary']['failed_checks']} / {selection['selection_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, source rerun, raw-row metric recomputation, model training, scoring, recommendation, acceptance, archive, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Operator Method or Closure Selection Using Expectancy Lab Evidence v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
    output_dir: str | Path,
    *,
    source_closure: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical selection JSON without overwriting an existing package."""
    selection = build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
        source_closure=source_closure, operator_attestation=operator_attestation
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1.json"
    if path.exists():
        raise MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError(
            "selection output already exists"
        )
    payload = canonical_json_bytes(selection)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": selection["artifact_kind"],
        "selection_status": selection["selection_status"],
        "selected_operator_option": selection["selected_operator_option"],
        "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest": selection["marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
