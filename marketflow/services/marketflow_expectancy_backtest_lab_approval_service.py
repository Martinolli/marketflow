"""Offline attestation-bound approval for future expectancy-lab execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_expectancy_backtest_lab_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_V1 = (
    "marketflow_expectancy_backtest_lab_approval_v1"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED"
)
EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY = "EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY"

SELECTED_BACKTEST_LAB_PACKAGE = (
    "PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB"
)
SELECTED_VPA_WYCKOFF_PACKAGE = "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"
SELECTED_MATRIX_PACKAGE = "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"
SELECTED_MATRIX_LAYOUT = "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"
SELECTED_FEATURE_PACKAGE = "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"
SELECTED_LABEL_TARGET_PACKAGE = "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
SELECTED_OBJECTIVE_PATH = "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
OPERATOR_DECISION_APPROVE_EXPECTANCY_BACKTEST_LAB = (
    "APPROVE_EXPECTANCY_BACKTEST_LAB"
)
OPERATOR_ATTESTATION_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_V1 = (
    "marketflow_expectancy_backtest_lab_approval_operator_attestation_v1"
)
REQUIRED_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE EXPECTANCY BACKTEST LAB "
    "PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB "
    "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE "
    "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX "
    "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE "
    "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET "
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET "
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY"
)

EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    "20266beddbc11d488cdfb81e24748391949a1270c11e28c0b173752a0ee61b3b"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = (
    review_service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = (
    review_service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = review_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = review_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = review_service.EXPECTED_SOURCE_RECORDS_DIGEST
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

APPROVED_BASELINE_IDS = [
    "BASELINE_ALWAYS_ABSTAIN",
    "BASELINE_ALWAYS_AVAILABLE_TARGET",
    "BASELINE_SIMPLE_BUY_AND_HOLD_REFERENCE",
    "BASELINE_PREVIOUS_DIRECTION_REFERENCE",
    "BASELINE_VPA_WYCKOFF_RULE_TAG_REFERENCE",
    "BASELINE_TARGET_PROFILE_PRIOR_RATE_REFERENCE",
]
BLOCKED_BASELINE_ID = "BASELINE_RANDOMIZED_NULL_REFERENCE_BLOCKED"
APPROVED_METRIC_FAMILY_IDS = [
    metric_id
    for metric_id in review_service.candidate_service.METRIC_FAMILY_IDS
    if metric_id != "METRIC_CONFIDENCE_INTERVAL_OR_BOOTSTRAP_BLOCKED"
]
BLOCKED_METRIC_FAMILY_ID = "METRIC_CONFIDENCE_INTERVAL_OR_BOOTSTRAP_BLOCKED"

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_expectancy_backtest_lab_authorized_for_future_execution_only",
    "operator_confirms_backtest_execution_not_performed",
    "operator_confirms_no_backtest_rows_created",
    "operator_confirms_no_backtest_results_created",
    "operator_confirms_no_metric_values_computed",
    "operator_confirms_no_metric_reports_created",
    "operator_confirms_no_model_training",
    "operator_confirms_no_strategy_scoring",
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

NEXT_CHAIN = [
    "Expectancy Backtest Lab Execution v1, if approved.",
    "Expectancy Backtest Lab Results Review v1.",
    "Predictive-usefulness reassessment using expectancy lab evidence.",
    "Acceptance-readiness review only after reassessment.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_backtest_lab_execution_if_approved",
    "expectancy_backtest_lab_results_review",
    "predictive_usefulness_reassessment_using_expectancy_lab_evidence",
    "predictive_usefulness_acceptance_readiness_if_reassessment_supports_it",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_execute_backtest_lab",
    "approval_does_not_create_backtest_rows",
    "approval_does_not_create_backtest_results",
    "approval_does_not_compute_metric_values",
    "approval_does_not_create_metric_reports",
    "approval_does_not_train_models",
    "approval_does_not_score_strategy",
    "approval_does_not_generate_trade_recommendations",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_call_providers",
    "approval_does_not_acquire_market_data",
    "approval_does_not_rerun_vpa_wyckoff_execution",
    "approval_does_not_rerun_vpa_wyckoff_results_review",
    "approval_does_not_rerun_feature_label_matrix_execution",
    "approval_does_not_rerun_feature_label_matrix_results_review",
    "approval_does_not_rerun_signal_feature_generation",
    "approval_does_not_rerun_target_generation",
    "approval_does_not_rerun_expectancy_backtest_lab_candidate_creation",
    "approval_does_not_rerun_expectancy_backtest_lab_candidate_review",
    "do_not_mutate_frozen_dataset",
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
    "source_candidate_review_digest_bound",
    "source_candidate_digest_bound",
    "source_vpa_wyckoff_results_review_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound",
    "source_matrix_rows_digest_bound",
    "source_target_values_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "approval_scope_only",
    "selected_backtest_lab_package_matches",
    "selected_vpa_wyckoff_package_preserved",
    "selected_matrix_package_preserved",
    "selected_matrix_layout_preserved",
    "selected_feature_package_preserved",
    "selected_target_package_preserved",
    "selected_objective_path_preserved",
    "backtest_lab_authorized_for_future_execution_true",
    "backtest_execution_authorized_for_future_lab_execution_true",
    "metric_computation_authorized_for_future_lab_execution_true",
    "expectancy_backtest_lab_selected_true",
    "expectancy_backtest_lab_approved_true",
    "expectancy_backtest_lab_authorized_true",
    "approval_created_true",
    "ready_for_execution_true",
    "backtest_lab_executed_false",
    "backtest_rows_created_false",
    "backtest_results_created_false",
    "metric_values_computed_false",
    "metric_reports_created_false",
    "model_training_authorized_false",
    "model_training_performed_false",
    "strategy_scoring_false",
    "approved_package_present",
    "supporting_packages_available_not_selected",
    "objectives_approved_10",
    "baselines_approved_6",
    "blocked_baseline_not_approved",
    "chronological_plan_approved",
    "metric_families_approved_13",
    "blocked_metric_not_approved",
    "no_peek_controls_approved_11",
    "future_outputs_authorized_not_generated_14",
    "planned_backtest_lab_row_count_179190",
    "planned_evaluable_target_row_count_177090",
    "planned_unavailable_target_row_count_2100",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "paper_trading_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "vpa_wyckoff_execution_rerun_false",
    "vpa_wyckoff_results_review_rerun_false",
    "matrix_execution_rerun_false",
    "matrix_results_review_rerun_false",
    "signal_feature_generation_rerun_false",
    "target_generation_rerun_false",
    "candidate_creation_rerun_false",
    "candidate_review_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowExpectancyBacktestLabApprovalError(ValueError):
    """Raised when evidence violates the approval-only contract."""


def build_marketflow_expectancy_backtest_lab_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_vpa_wyckoff_results_review_digest: str,
    operator_confirms_vpa_wyckoff_rule_values_digest: str,
    operator_confirms_matrix_rows_digest: str,
    operator_confirms_target_values_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_backtest_lab_package: str,
    operator_confirms_selected_vpa_wyckoff_package: str,
    operator_confirms_selected_matrix_package: str,
    operator_confirms_selected_matrix_layout: str,
    operator_confirms_selected_feature_package: str,
    operator_confirms_selected_label_target_package: str,
    operator_confirms_selected_objective_path: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_expectancy_backtest_lab_authorized_for_future_execution_only: bool,
    operator_confirms_backtest_execution_not_performed: bool,
    operator_confirms_no_backtest_rows_created: bool,
    operator_confirms_no_backtest_results_created: bool,
    operator_confirms_no_metric_values_computed: bool,
    operator_confirms_no_metric_reports_created: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_backtest_lab_package: str = SELECTED_BACKTEST_LAB_PACKAGE,
    selected_vpa_wyckoff_package: str = SELECTED_VPA_WYCKOFF_PACKAGE,
    selected_matrix_package: str = SELECTED_MATRIX_PACKAGE,
    selected_matrix_layout: str = SELECTED_MATRIX_LAYOUT,
    selected_feature_package: str = SELECTED_FEATURE_PACKAGE,
    selected_label_target_package: str = SELECTED_LABEL_TARGET_PACKAGE,
    selected_objective_path: str = SELECTED_OBJECTIVE_PATH,
    operator_decision: str = OPERATOR_DECISION_APPROVE_EXPECTANCY_BACKTEST_LAB,
) -> dict[str, Any]:
    return {
        "operator_decision": operator_decision,
        "selected_backtest_lab_package": selected_backtest_lab_package,
        "selected_vpa_wyckoff_package": selected_vpa_wyckoff_package,
        "selected_matrix_package": selected_matrix_package,
        "selected_matrix_layout": selected_matrix_layout,
        "selected_feature_package": selected_feature_package,
        "selected_label_target_package": selected_label_target_package,
        "selected_objective_path": selected_objective_path,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_V1,
        "operator_reference": operator_reference,
        "operator_confirms_candidate_review_digest": operator_confirms_candidate_review_digest,
        "operator_confirms_candidate_digest": operator_confirms_candidate_digest,
        "operator_confirms_vpa_wyckoff_results_review_digest": operator_confirms_vpa_wyckoff_results_review_digest,
        "operator_confirms_vpa_wyckoff_rule_values_digest": operator_confirms_vpa_wyckoff_rule_values_digest,
        "operator_confirms_matrix_rows_digest": operator_confirms_matrix_rows_digest,
        "operator_confirms_target_values_digest": operator_confirms_target_values_digest,
        "operator_confirms_records_digest": operator_confirms_records_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_meta_record_count": operator_confirms_meta_record_count,
        "operator_confirms_non_meta_record_count": operator_confirms_non_meta_record_count,
        "operator_confirms_selected_backtest_lab_package": operator_confirms_selected_backtest_lab_package,
        "operator_confirms_selected_vpa_wyckoff_package": operator_confirms_selected_vpa_wyckoff_package,
        "operator_confirms_selected_matrix_package": operator_confirms_selected_matrix_package,
        "operator_confirms_selected_matrix_layout": operator_confirms_selected_matrix_layout,
        "operator_confirms_selected_feature_package": operator_confirms_selected_feature_package,
        "operator_confirms_selected_label_target_package": operator_confirms_selected_label_target_package,
        "operator_confirms_selected_objective_path": operator_confirms_selected_objective_path,
        "operator_confirms_approval_scope_only": operator_confirms_approval_scope_only,
        "operator_confirms_expectancy_backtest_lab_authorized_for_future_execution_only": operator_confirms_expectancy_backtest_lab_authorized_for_future_execution_only,
        "operator_confirms_backtest_execution_not_performed": operator_confirms_backtest_execution_not_performed,
        "operator_confirms_no_backtest_rows_created": operator_confirms_no_backtest_rows_created,
        "operator_confirms_no_backtest_results_created": operator_confirms_no_backtest_results_created,
        "operator_confirms_no_metric_values_computed": operator_confirms_no_metric_values_computed,
        "operator_confirms_no_metric_reports_created": operator_confirms_no_metric_reports_created,
        "operator_confirms_no_model_training": operator_confirms_no_model_training,
        "operator_confirms_no_strategy_scoring": operator_confirms_no_strategy_scoring,
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


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def _validate_operator_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "operator attestation must be an object"
        )
    exact = {
        "operator_decision": OPERATOR_DECISION_APPROVE_EXPECTANCY_BACKTEST_LAB,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_V1,
        "operator_confirms_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "operator_confirms_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "operator_confirms_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "operator_confirms_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "operator_confirms_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "operator_confirms_selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "operator_confirms_selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "operator_confirms_selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "operator_confirms_selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "operator_confirms_selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "operator_confirms_selected_objective_path": SELECTED_OBJECTIVE_PATH,
    }
    for field, expected in exact.items():
        _expect(attestation.get(field), expected, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect(attestation.get(field), True, field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise MarketFlowExpectancyBacktestLabApprovalError(f"{field} is required")


def _approved_package() -> dict[str, Any]:
    return {
        "package_id": SELECTED_BACKTEST_LAB_PACKAGE,
        "approval_status": "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY",
        "uses": [
            "reviewed feature-label matrix rows",
            "reviewed expectancy target profiles",
            "reviewed VPA/Wyckoff rule/state tags",
            "fixed cost/slippage assumptions from target-generation chain",
            "chronological no-peek windows",
            "horizon-aware embargo controls",
            "abstention/no-trade preservation",
        ],
        "planned_scope": "RESEARCH_ONLY_BACKTEST_LAB_EXECUTION_IF_SEPARATELY_INVOKED",
        "planned_backtest_lab_row_count": 179190,
        "planned_evaluable_target_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_metric_family_count": 13,
        "planned_blocked_metric_family_count": 1,
        "planned_baseline_count": 6,
        "planned_blocked_baseline_count": 1,
        "backtest_execution_performed": False,
        "backtest_rows_created": False,
        "backtest_results_created": False,
        "metric_values_computed": False,
        "research_only": True,
        "non_actionable": True,
    }


def _supporting_packages() -> list[dict[str, Any]]:
    return [
        {
            "package_id": package_id,
            "approval_status": "AVAILABLE_NOT_SELECTED",
            "execution_performed": False,
        }
        for package_id in (
            review_service.candidate_service.PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB,
            review_service.candidate_service.PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB,
            review_service.candidate_service.PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB,
        )
    ]


def _approved_objectives(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["reviewed_backtest_objectives"])
    for row in rows:
        row.update(
            {
                "approval_status": "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY",
                "backtest_execution_authorized_for_future_lab_execution": True,
                "metric_computation_authorized_for_future_lab_execution": True,
                "execution_performed": False,
                "metric_values_computed": False,
            }
        )
    return rows


def _approved_and_blocked_baselines(
    source: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows = deepcopy(source["reviewed_baselines"])
    approved: list[dict[str, Any]] = []
    blocked: dict[str, Any] | None = None
    for row in source_rows:
        if row["baseline_id"] == BLOCKED_BASELINE_ID:
            row["approval_status"] = (
                "NOT_APPROVED_BLOCKED_REQUIRES_SEPARATE_OPERATOR_APPROVAL"
            )
            blocked = row
        else:
            row.update(
                {
                    "approval_status": "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY",
                    "execution_performed": False,
                    "metric_values_computed": False,
                    "model_training_authorized": False,
                }
            )
            approved.append(row)
    if blocked is None:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "blocked randomized baseline is required"
        )
    return approved, blocked


def _approved_chronological_plan(source: Mapping[str, Any]) -> dict[str, Any]:
    row = deepcopy(source["reviewed_chronological_plan"])
    row["approval_status"] = (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY"
    )
    return row


def _approved_and_blocked_metrics(
    source: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows = deepcopy(source["reviewed_metric_families"])
    approved: list[dict[str, Any]] = []
    blocked: dict[str, Any] | None = None
    for row in source_rows:
        if row["metric_family_id"] == BLOCKED_METRIC_FAMILY_ID:
            row["approval_status"] = (
                "NOT_APPROVED_BLOCKED_REQUIRES_SEPARATE_OPERATOR_APPROVAL"
            )
            blocked = row
        else:
            row.update(
                {
                    "approval_status": "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY",
                    "metric_computation_authorized_for_future_lab_execution": True,
                    "metric_values_computed": False,
                    "backtest_execution_performed": False,
                    "model_training_authorized": False,
                }
            )
            approved.append(row)
    if blocked is None:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "blocked bootstrap metric is required"
        )
    return approved, blocked


def _approved_controls(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["reviewed_no_peek_and_leakage_controls"])
    for row in rows:
        row["approval_status"] = (
            "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_CONTROL"
        )
    return rows


def _approved_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["reviewed_future_outputs"])
    for row in rows:
        row["approval_status"] = "AUTHORIZED_NOT_GENERATED"
    return rows


def per_ticker_expectancy_backtest_lab_approval_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_backtest_lab_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approval_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_entry in source[
        "per_ticker_expectancy_backtest_lab_candidate_review_entries"
    ]:
        ticker = source_entry["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "expectancy_backtest_lab_candidate_review_status": review_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
            "expectancy_backtest_lab_approval_status": "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY",
            "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
            "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
            "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
            "selected_feature_package": SELECTED_FEATURE_PACKAGE,
            "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
            "planned_matrix_row_count": source_entry["planned_matrix_row_count"],
            "planned_evaluable_target_row_count": source_entry["planned_evaluable_target_row_count"],
            "planned_unavailable_target_row_count": source_entry["planned_unavailable_target_row_count"],
            "planned_rule_value_row_count": source_entry["planned_rule_value_row_count"],
            "planned_state_value_row_count": source_entry["planned_state_value_row_count"],
            "expectancy_backtest_lab_selected": True,
            "expectancy_backtest_lab_approved": True,
            "expectancy_backtest_lab_authorized": True,
            "expectancy_backtest_lab_executed": False,
            "expectancy_backtest_rows_created": False,
            "expectancy_backtest_results_created": False,
            "backtest_execution_authorized_for_future_lab_execution": True,
            "backtest_execution_performed": False,
            "metric_computation_authorized_for_future_lab_execution": True,
            "metric_computation_performed": False,
            "model_training_authorized": False,
            "strategy_scoring_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
            "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
            "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
            "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "approval_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_APPROVAL"
                if ticker == "META"
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_expectancy_backtest_lab_approval_digest"] = (
            per_ticker_expectancy_backtest_lab_approval_digest_v1(entry)
        )
        rows.append(entry)
    return rows


def _base_approval(
    source: Mapping[str, Any], operator_attestation: Mapping[str, Any]
) -> dict[str, Any]:
    approved_baselines, blocked_baseline = _approved_and_blocked_baselines(source)
    approved_metrics, blocked_metric = _approved_and_blocked_metrics(source)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_V1,
        "approval_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
        "approval_scope": EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "created_offline": True,
        "research_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_expectancy_backtest_lab_candidate_review_artifact_kind": review_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "source_expectancy_backtest_lab_candidate_review_status": review_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "source_expectancy_backtest_lab_candidate_review_scope": review_service.EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "source_expectancy_backtest_lab_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_expectancy_backtest_lab_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_rule_baseline_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": deepcopy(source["source_evidence"]),
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "matrix_row_count": source["matrix_row_count"],
        "available_matrix_row_count": source["available_matrix_row_count"],
        "unavailable_target_matrix_row_count": source["unavailable_target_matrix_row_count"],
        "rule_value_row_count": source["rule_value_row_count"],
        "state_value_row_count": source["state_value_row_count"],
        "selected_rule_family_count": source["selected_rule_family_count"],
        "selected_state_family_count": source["selected_state_family_count"],
        "rule_family_reference_count": source["rule_family_reference_count"],
        "state_family_reference_count": source["state_family_reference_count"],
        "target_profile_count": source["target_profile_count"],
        "feature_group_count_per_matrix_row": source["feature_group_count_per_matrix_row"],
        "target_unavailable_row_count": source["target_unavailable_row_count"],
        "candidate_philosophy": source["candidate_philosophy"],
        "candidate_primary_question": source["candidate_primary_question"],
        "candidate_secondary_question": source["candidate_secondary_question"],
        "candidate_boundary": source["candidate_boundary"],
        "approved_backtest_lab_package": _approved_package(),
        "supporting_backtest_lab_packages": _supporting_packages(),
        "approved_backtest_objectives": _approved_objectives(source),
        "approved_baselines": approved_baselines,
        "blocked_baseline": blocked_baseline,
        "approved_chronological_plan": _approved_chronological_plan(source),
        "approved_metric_families": approved_metrics,
        "blocked_metric_family": blocked_metric,
        "approved_no_peek_and_leakage_controls": _approved_controls(source),
        "approved_future_outputs": _approved_outputs(source),
        "planned_backtest_lab_row_count": 179190,
        "planned_evaluable_target_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_metric_family_count": 13,
        "planned_blocked_metric_family_count": 1,
        "planned_baseline_count": 6,
        "planned_blocked_baseline_count": 1,
        "planned_backtest_execution_scope": "RESEARCH_ONLY_NOT_PRODUCTION_NOT_RUNTIME",
        "per_ticker_expectancy_backtest_lab_approval_entries": _per_ticker_approval_entries(source),
        "expectancy_backtest_lab_candidate_created": True,
        "expectancy_backtest_lab_candidate_review_created": True,
        "expectancy_backtest_lab_candidate_review_ready": True,
        "expectancy_backtest_lab_selected": True,
        "expectancy_backtest_lab_approved": True,
        "expectancy_backtest_lab_authorized": True,
        "expectancy_backtest_lab_approval_created": True,
        "ready_for_expectancy_backtest_lab_execution": True,
        "expectancy_backtest_lab_authorized_for_future_execution": True,
        "backtest_execution_authorized_for_future_lab_execution": True,
        "metric_computation_authorized_for_future_lab_execution": True,
        "expectancy_backtest_lab_executed": False,
        "expectancy_backtest_rows_created": False,
        "expectancy_backtest_results_created": False,
        "metric_values_computed": False,
        "metric_reports_created": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
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
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False,
        "target_generation_rerun_performed": False,
        "expectancy_backtest_lab_candidate_creation_rerun_performed": False,
        "expectancy_backtest_lab_candidate_review_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": bool(actual),
        "severity": "INFO" if actual else BLOCKER,
        "message": "approval condition satisfied" if actual else "approval condition failed",
    }


def _check_values(approval: Mapping[str, Any]) -> dict[str, bool]:
    attestation = approval.get("operator_attestation", {})
    package = approval.get("approved_backtest_lab_package", {})
    supporting = approval.get("supporting_backtest_lab_packages", [])
    objectives = approval.get("approved_backtest_objectives", [])
    baselines = approval.get("approved_baselines", [])
    blocked_baseline = approval.get("blocked_baseline", {})
    metrics = approval.get("approved_metric_families", [])
    blocked_metric = approval.get("blocked_metric_family", {})
    controls = approval.get("approved_no_peek_and_leakage_controls", [])
    outputs = approval.get("approved_future_outputs", [])
    entries = approval.get("per_ticker_expectancy_backtest_lab_approval_entries", [])
    return {
        "source_candidate_review_digest_bound": approval.get("source_expectancy_backtest_lab_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": approval.get("source_expectancy_backtest_lab_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest_bound": approval.get("source_vpa_wyckoff_rule_baseline_results_review_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": approval.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": approval.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": approval.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": approval.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": approval.get("target_universe") == TARGET_UNIVERSE and approval.get("target_universe_count") == 12,
        "records_digest_preserved": approval.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": approval.get("meta_record_count") == 913,
        "operator_decision_matches": attestation.get("operator_decision") == OPERATOR_DECISION_APPROVE_EXPECTANCY_BACKTEST_LAB,
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase") == REQUIRED_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_ATTESTATION_PHRASE,
        "approval_scope_only": approval.get("approval_scope") == EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY and attestation.get("operator_confirms_approval_scope_only") is True,
        "selected_backtest_lab_package_matches": approval.get("selected_backtest_lab_package") == SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package_preserved": approval.get("selected_vpa_wyckoff_package") == SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package_preserved": approval.get("selected_matrix_package") == SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout_preserved": approval.get("selected_matrix_layout") == SELECTED_MATRIX_LAYOUT,
        "selected_feature_package_preserved": approval.get("selected_feature_package") == SELECTED_FEATURE_PACKAGE,
        "selected_target_package_preserved": approval.get("selected_label_target_package") == SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path_preserved": approval.get("selected_objective_path") == SELECTED_OBJECTIVE_PATH,
        "backtest_lab_authorized_for_future_execution_true": approval.get("expectancy_backtest_lab_authorized_for_future_execution") is True,
        "backtest_execution_authorized_for_future_lab_execution_true": approval.get("backtest_execution_authorized_for_future_lab_execution") is True,
        "metric_computation_authorized_for_future_lab_execution_true": approval.get("metric_computation_authorized_for_future_lab_execution") is True,
        "expectancy_backtest_lab_selected_true": approval.get("expectancy_backtest_lab_selected") is True,
        "expectancy_backtest_lab_approved_true": approval.get("expectancy_backtest_lab_approved") is True,
        "expectancy_backtest_lab_authorized_true": approval.get("expectancy_backtest_lab_authorized") is True,
        "approval_created_true": approval.get("expectancy_backtest_lab_approval_created") is True,
        "ready_for_execution_true": approval.get("ready_for_expectancy_backtest_lab_execution") is True,
        "backtest_lab_executed_false": approval.get("expectancy_backtest_lab_executed") is False,
        "backtest_rows_created_false": approval.get("expectancy_backtest_rows_created") is False,
        "backtest_results_created_false": approval.get("expectancy_backtest_results_created") is False,
        "metric_values_computed_false": approval.get("metric_values_computed") is False,
        "metric_reports_created_false": approval.get("metric_reports_created") is False,
        "model_training_authorized_false": approval.get("model_training_authorized") is False,
        "model_training_performed_false": approval.get("model_training_performed") is False,
        "strategy_scoring_false": approval.get("strategy_scoring_performed") is False,
        "approved_package_present": package == _approved_package(),
        "supporting_packages_available_not_selected": supporting == _supporting_packages(),
        "objectives_approved_10": len(objectives) == 10 and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY" and row.get("execution_performed") is False for row in objectives),
        "baselines_approved_6": [row.get("baseline_id") for row in baselines] == APPROVED_BASELINE_IDS and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY" for row in baselines),
        "blocked_baseline_not_approved": blocked_baseline.get("baseline_id") == BLOCKED_BASELINE_ID and blocked_baseline.get("approval_status") == "NOT_APPROVED_BLOCKED_REQUIRES_SEPARATE_OPERATOR_APPROVAL" and blocked_baseline.get("allowed_for_future_execution") is False,
        "chronological_plan_approved": approval.get("approved_chronological_plan", {}).get("approval_status") == "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY" and approval.get("approved_chronological_plan", {}).get("split_execution_status") == "PLANNED_NOT_EXECUTED",
        "metric_families_approved_13": [row.get("metric_family_id") for row in metrics] == APPROVED_METRIC_FAMILY_IDS and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY" for row in metrics),
        "blocked_metric_not_approved": blocked_metric.get("metric_family_id") == BLOCKED_METRIC_FAMILY_ID and blocked_metric.get("approval_status") == "NOT_APPROVED_BLOCKED_REQUIRES_SEPARATE_OPERATOR_APPROVAL" and blocked_metric.get("allowed_for_future_execution") is False,
        "no_peek_controls_approved_11": len(controls) == 11 and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_CONTROL" for row in controls),
        "future_outputs_authorized_not_generated_14": len(outputs) == 14 and all(row.get("approval_status") == "AUTHORIZED_NOT_GENERATED" and row.get("output_status") == "PLANNED_NOT_GENERATED" for row in outputs),
        "planned_backtest_lab_row_count_179190": approval.get("planned_backtest_lab_row_count") == 179190,
        "planned_evaluable_target_row_count_177090": approval.get("planned_evaluable_target_row_count") == 177090,
        "planned_unavailable_target_row_count_2100": approval.get("planned_unavailable_target_row_count") == 2100,
        "per_ticker_entries_12": len(entries) == 12 and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_expectancy_backtest_lab_approval_digest") == per_ticker_expectancy_backtest_lab_approval_digest_v1(row) for row in entries),
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": approval.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": approval.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": approval.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": approval.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": approval.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": approval.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": approval.get("provider_requests_made_in_approval") is False,
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed_in_approval") is False,
        "dataset_regeneration_false": approval.get("canonical_dataset_regenerated_in_approval") is False,
        "vpa_wyckoff_execution_rerun_false": approval.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": approval.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": approval.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": approval.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": approval.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": approval.get("target_generation_rerun_performed") is False,
        "candidate_creation_rerun_false": approval.get("expectancy_backtest_lab_candidate_creation_rerun_performed") is False,
        "candidate_review_rerun_false": approval.get("expectancy_backtest_lab_candidate_review_rerun_performed") is False,
        "raw_provider_payloads_not_committed": approval.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": approval.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": approval.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": approval.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": approval.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files") is True,
    }


def _approval_checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(approval)
    return [_check(check_id, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "expectancy_backtest_lab_selected": True,
        "expectancy_backtest_lab_approved": True,
        "expectancy_backtest_lab_authorized": True,
        "ready_for_expectancy_backtest_lab_execution": True,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "expectancy_backtest_lab_authorized_for_future_execution": True,
        "expectancy_backtest_lab_executed": False,
        "expectancy_backtest_rows_created": False,
        "expectancy_backtest_results_created": False,
        "metric_values_computed": False,
        "metric_reports_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_expectancy_backtest_lab_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(approval))
    payload.pop("marketflow_expectancy_backtest_lab_approval_digest", None)
    return semantic_digest(payload)


def build_marketflow_expectancy_backtest_lab_approval_v1(
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    """Approve future research-only lab execution without executing it."""

    source = (
        review_service.build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1()
        if source_review is None
        else deepcopy(source_review)
    )
    try:
        review_service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
            source
        )
    except review_service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError as exc:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "source candidate review is invalid"
        ) from exc
    if (
        source[
            "marketflow_expectancy_backtest_lab_candidate_operator_review_digest"
        ]
        != EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
    ):
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "source candidate review digest does not match approved evidence"
        )
    _validate_operator_attestation(operator_attestation)
    approval = _base_approval(source, operator_attestation)
    checklist = _approval_checklist(approval)
    approval["approval_checklist"] = checklist
    approval["approval_summary"] = _summary(checklist)
    if approval["approval_summary"]["blocker_count"]:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "expectancy backtest-lab approval contains blockers"
        )
    approval["marketflow_expectancy_backtest_lab_approval_digest"] = (
        marketflow_expectancy_backtest_lab_approval_digest_v1(approval)
    )
    validate_marketflow_expectancy_backtest_lab_approval_v1(approval)
    return approval


def validate_marketflow_expectancy_backtest_lab_approval_v1(
    approval: dict,
) -> dict[str, Any]:
    """Validate the attestation, evidence, approval, and closed boundaries."""

    if not isinstance(approval, dict):
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approval must be a JSON object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_V1,
        "approval_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
        "approval_scope": EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "source_expectancy_backtest_lab_candidate_review_artifact_kind": review_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "source_expectancy_backtest_lab_candidate_review_status": review_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "source_expectancy_backtest_lab_candidate_review_scope": review_service.EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "source_expectancy_backtest_lab_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_expectancy_backtest_lab_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_rule_baseline_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "planned_backtest_lab_row_count": 179190,
        "planned_evaluable_target_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_metric_family_count": 13,
        "planned_blocked_metric_family_count": 1,
        "planned_baseline_count": 6,
        "planned_blocked_baseline_count": 1,
        "planned_backtest_execution_scope": "RESEARCH_ONLY_NOT_PRODUCTION_NOT_RUNTIME",
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(approval.get(field), expected, field)
    for field in (
        "created_offline",
        "research_only",
        "operator_attestation_required",
        "meta_reduced_record_count_preserved",
        "expectancy_backtest_lab_candidate_created",
        "expectancy_backtest_lab_candidate_review_created",
        "expectancy_backtest_lab_candidate_review_ready",
        "expectancy_backtest_lab_selected",
        "expectancy_backtest_lab_approved",
        "expectancy_backtest_lab_authorized",
        "expectancy_backtest_lab_approval_created",
        "ready_for_expectancy_backtest_lab_execution",
        "expectancy_backtest_lab_authorized_for_future_execution",
        "backtest_execution_authorized_for_future_lab_execution",
        "metric_computation_authorized_for_future_lab_execution",
        "no_tracked_marketflow_files",
    ):
        _expect(approval.get(field), True, field)
    for field in (
        "expectancy_backtest_lab_executed",
        "expectancy_backtest_rows_created",
        "expectancy_backtest_results_created",
        "metric_values_computed",
        "metric_reports_created",
        "backtest_execution_performed",
        "model_training_authorized",
        "model_training_performed",
        "metric_computation_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval",
        "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_performed",
        "target_generation_rerun_performed",
        "expectancy_backtest_lab_candidate_creation_rerun_performed",
        "expectancy_backtest_lab_candidate_review_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ):
        _expect(approval.get(field), False, field)
    _expect(approval.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(approval.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approval.get(field), NOT_AUTHORIZED, field)
    _validate_operator_attestation(approval.get("operator_attestation", {}))
    expected_source_evidence = {
        "marketflow_expectancy_backtest_lab_candidate_v1_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        **deepcopy(review_service.candidate_service.SOURCE_EVIDENCE),
    }
    _expect(approval.get("source_evidence"), expected_source_evidence, "source_evidence")
    _expect(approval.get("approved_backtest_lab_package"), _approved_package(), "approved_backtest_lab_package")
    _expect(approval.get("supporting_backtest_lab_packages"), _supporting_packages(), "supporting_backtest_lab_packages")

    objectives = approval.get("approved_backtest_objectives", [])
    if [row.get("objective_id") for row in objectives] != review_service.candidate_service.BACKTEST_OBJECTIVE_IDS:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approved objectives mismatch"
        )
    baselines = approval.get("approved_baselines", [])
    if [row.get("baseline_id") for row in baselines] != APPROVED_BASELINE_IDS:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approved baselines mismatch"
        )
    blocked_baseline = approval.get("blocked_baseline", {})
    _expect(blocked_baseline.get("baseline_id"), BLOCKED_BASELINE_ID, "blocked_baseline")
    _expect(blocked_baseline.get("allowed_for_future_execution"), False, "blocked_baseline.allowed")
    plan = approval.get("approved_chronological_plan")
    if not isinstance(plan, dict):
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approved chronological plan missing"
        )
    _expect(plan.get("split_policy"), "CHRONOLOGICAL_NO_SHUFFLE", "split_policy")
    _expect(plan.get("split_execution_status"), "PLANNED_NOT_EXECUTED", "split_execution_status")
    _expect(plan.get("approval_status"), "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY", "chronological approval_status")
    metrics = approval.get("approved_metric_families", [])
    if [row.get("metric_family_id") for row in metrics] != APPROVED_METRIC_FAMILY_IDS:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approved metric families mismatch"
        )
    blocked_metric = approval.get("blocked_metric_family", {})
    _expect(blocked_metric.get("metric_family_id"), BLOCKED_METRIC_FAMILY_ID, "blocked_metric")
    _expect(blocked_metric.get("allowed_for_future_execution"), False, "blocked_metric.allowed")
    controls = approval.get("approved_no_peek_and_leakage_controls", [])
    if [row.get("control_id") for row in controls] != review_service.candidate_service.NO_PEEK_CONTROL_IDS:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approved no-peek controls mismatch"
        )
    outputs = approval.get("approved_future_outputs", [])
    if [row.get("output_id") for row in outputs] != review_service.candidate_service.FUTURE_OUTPUT_IDS:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approved future outputs mismatch"
        )
    entries = approval.get("per_ticker_expectancy_backtest_lab_approval_entries")
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "per-ticker approval entries mismatch"
        )
    for row in entries:
        _expect(
            row.get("per_ticker_expectancy_backtest_lab_approval_digest"),
            per_ticker_expectancy_backtest_lab_approval_digest_v1(row),
            f"{row.get('ticker')} approval digest",
        )
    checklist = _approval_checklist(approval)
    _expect(approval.get("approval_checklist"), checklist, "approval_checklist")
    if any(row["status"] != PASS for row in checklist):
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approval checklist contains failures"
        )
    _expect(approval.get("approval_summary"), _summary(checklist), "approval_summary")
    digest = approval.get("marketflow_expectancy_backtest_lab_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyBacktestLabApprovalError("approval digest missing")
    _expect(
        digest,
        marketflow_expectancy_backtest_lab_approval_digest_v1(approval),
        "approval digest",
    )
    return {
        "status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_expectancy_backtest_lab_approval_digest": digest,
        "total_checks": approval["approval_summary"]["total_checks"],
        "passed_checks": approval["approval_summary"]["passed_checks"],
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_marketflow_expectancy_backtest_lab_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a validated approval as operator-readable Markdown."""

    validation = validate_marketflow_expectancy_backtest_lab_approval_v1(approval)
    attestation = approval["operator_attestation"]
    sections = [
        (
            "Expectancy Backtest Lab Approval v1",
            [
                f"Artifact/status/scope: {approval['artifact_kind']} / {approval['approval_status']} / {approval['approval_scope']}.",
                f"Approval digest: {validation['marketflow_expectancy_backtest_lab_approval_digest']}.",
            ],
        ),
        (
            "Operator Attestation",
            [
                f"Reference: {attestation['operator_reference']}.",
                f"Timestamp: {attestation['operator_attestation_timestamp_utc']}.",
                "The exact non-secret approval phrase and all required confirmations were validated.",
            ],
        ),
        (
            "Source Candidate Review",
            [
                f"Review {EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST} remains immutable source evidence."
            ],
        ),
        (
            "Bound Evidence",
            [
                "Candidate review, candidate, VPA/Wyckoff, matrix, feature, target, records, and the complete upstream chain remain digest-bound."
            ],
        ),
        (
            "Dataset and Universe",
            [
                "The ordered twelve-ticker universe and 11,946 records are preserved; META remains exactly 913."
            ],
        ),
        (
            "Approval Scope",
            [
                "Approval authorizes only future separately invoked research-lab execution; it does not execute the lab."
            ],
        ),
        (
            "Selected Backtest Lab Package",
            [SELECTED_BACKTEST_LAB_PACKAGE],
        ),
        (
            "Selected Source Packages",
            [
                SELECTED_VPA_WYCKOFF_PACKAGE,
                SELECTED_MATRIX_PACKAGE,
                SELECTED_MATRIX_LAYOUT,
                SELECTED_FEATURE_PACKAGE,
                SELECTED_LABEL_TARGET_PACKAGE,
                SELECTED_OBJECTIVE_PATH,
            ],
        ),
        (
            "Approved Objectives",
            review_service.candidate_service.BACKTEST_OBJECTIVE_IDS,
        ),
        ("Approved Baselines", APPROVED_BASELINE_IDS),
        ("Blocked Baselines", [BLOCKED_BASELINE_ID]),
        (
            "Approved Chronological Plan",
            [
                "2022-2023 calibration, 2024 validation, and 2025 holdout are approved for future chronological execution with the required embargo; no split was executed."
            ],
        ),
        ("Approved Metric Families", APPROVED_METRIC_FAMILY_IDS),
        ("Blocked Metrics", [BLOCKED_METRIC_FAMILY_ID]),
        (
            "Approved No-Peek Controls",
            review_service.candidate_service.NO_PEEK_CONTROL_IDS,
        ),
        (
            "Approved Future Outputs",
            review_service.candidate_service.FUTURE_OUTPUT_IDS,
        ),
        (
            "Planned Counts",
            [
                "179,190 planned rows; 177,090 evaluable and 2,100 unavailable targets; thirteen approved metrics plus one blocked; six approved baselines plus one blocked."
            ],
        ),
        (
            "Per-Ticker Approval Summary",
            [
                "Twelve digest-bound approvals preserve 15,045 planned rows per non-META ticker and 13,695 for META."
            ],
        ),
        ("Next Chain", NEXT_CHAIN),
        ("Next Gates", NEXT_GATES),
        ("Risk Controls", RISK_CONTROLS),
        (
            "Predictive Usefulness Boundary",
            ["Predictive usefulness remains not accepted."],
        ),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        (
            "Runtime Boundary",
            [
                "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
            ],
        ),
        (
            "Checklist Summary",
            [
                f"{approval['approval_summary']['passed_checks']}/{approval['approval_summary']['total_checks']} checks pass with zero blockers."
            ],
        ),
        (
            "Guardrails",
            [
                "This artifact does not execute a backtest, create rows/results or reports, compute metric values, train models, score strategies, recommend trades, accept predictive usefulness/profitability, or authorize runtime/trading."
            ],
        ),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_expectancy_backtest_lab_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    """Write approval JSON and Markdown only to an explicit directory."""

    approval = build_marketflow_expectancy_backtest_lab_approval_v1(
        source_review=source_review,
        operator_attestation=operator_attestation,
    )
    validation = validate_marketflow_expectancy_backtest_lab_approval_v1(approval)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_expectancy_backtest_lab_approval_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowExpectancyBacktestLabApprovalError(
            "approval output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(approval))
    markdown_path.write_text(
        build_marketflow_expectancy_backtest_lab_approval_markdown_v1(approval),
        encoding="utf-8",
        newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path.resolve()),
        "markdown_path": str(markdown_path.resolve()),
    }
