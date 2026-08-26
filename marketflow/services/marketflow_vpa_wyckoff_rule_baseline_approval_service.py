"""Offline attestation-bound approval for future VPA/Wyckoff execution."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_V1 = (
    "marketflow_vpa_wyckoff_rule_baseline_approval_v1"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED"
)
VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY = "VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY"
SELECTED_VPA_WYCKOFF_PACKAGE = "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"
SUPPORTING_VPA_WYCKOFF_PACKAGE = "PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT"
SELECTED_MATRIX_PACKAGE = "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"
SELECTED_MATRIX_LAYOUT = "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"
SELECTED_FEATURE_PACKAGE = "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"
SELECTED_LABEL_TARGET_PACKAGE = "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
SELECTED_OBJECTIVE_PATH = "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
OPERATOR_DECISION_APPROVE_VPA_WYCKOFF_RULE_BASELINE = (
    "APPROVE_VPA_WYCKOFF_RULE_BASELINE"
)
OPERATOR_ATTESTATION_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_V1 = (
    "marketflow_vpa_wyckoff_rule_baseline_approval_operator_attestation_v1"
)
REQUIRED_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE VPA WYCKOFF RULE BASELINE "
    "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE "
    "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX "
    "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE "
    "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET "
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET "
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY"
)

EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    "8447ca124e62ef8ea346aa2ee23d0a0c209791bf960659adf7cd75dc363dfbd9"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST = (
    review_service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST = review_service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = review_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = review_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = review_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = review_service.EXPECTED_SOURCE_RECORDS_DIGEST
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

SELECTED_RULE_FAMILY_IDS = [
    "VPA_RULE_VOLUME_CONFIRMATION",
    "VPA_RULE_SPREAD_VOLUME_EFFORT_RESULT",
    "VPA_RULE_CLOSE_LOCATION_PRESSURE",
    "VPA_RULE_BREAKOUT_EFFORT_CONFIRMATION",
    "VPA_RULE_PULLBACK_QUALITY",
    "VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION",
    "VPA_RULE_VOLATILITY_COMPRESSION_EXPANSION",
    "VPA_RULE_NOISE_ABSTENTION_FILTER",
]
SUPPORTING_RULE_FAMILY_IDS = [
    "VPA_RULE_CLIMAX_OR_EXHAUSTION_CONTEXT",
    "VPA_RULE_ABSORPTION_OR_NO_SUPPLY_DEMAND",
]
SELECTED_STATE_FAMILY_IDS = [
    "WYCKOFF_STATE_ACCUMULATION_CANDIDATE",
    "WYCKOFF_STATE_MARKUP_OR_UPTREND_CANDIDATE",
    "WYCKOFF_STATE_DISTRIBUTION_CANDIDATE",
    "WYCKOFF_STATE_MARKDOWN_OR_DOWNTREND_CANDIDATE",
    "WYCKOFF_STATE_TRADING_RANGE_OR_BALANCE",
    "WYCKOFF_STATE_NO_CLEAR_STRUCTURE",
]
SUPPORTING_STATE_FAMILY_IDS = [
    "WYCKOFF_STATE_POSSIBLE_SPRING_OR_SHAKEOUT",
    "WYCKOFF_STATE_POSSIBLE_UPTHRUST_OR_EXHAUSTION",
]

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_vpa_wyckoff_rule_baseline_authorized_for_future_execution_only",
    "operator_confirms_vpa_wyckoff_rule_baseline_not_executed",
    "operator_confirms_no_rule_values_created",
    "operator_confirms_no_state_values_created",
    "operator_confirms_no_baseline_outputs_created",
    "operator_confirms_no_backtest_execution",
    "operator_confirms_no_model_training",
    "operator_confirms_no_metric_computation",
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
    "VPA/Wyckoff Rule Baseline Execution v1, if approved.",
    "VPA/Wyckoff Rule Baseline Results Review v1.",
    "Expectancy Backtest Lab Candidate only after separate approval.",
    "Results review and readiness gates before predictive-usefulness acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "vpa_wyckoff_rule_baseline_execution_if_approved",
    "vpa_wyckoff_rule_baseline_results_review",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_execute_vpa_wyckoff_rules",
    "approval_does_not_create_rule_values",
    "approval_does_not_create_state_values",
    "approval_does_not_create_baseline_outputs",
    "approval_does_not_create_expectancy_backtest_lab_candidate",
    "approval_does_not_run_backtest",
    "approval_does_not_train_models",
    "approval_does_not_compute_metrics",
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
    "approval_does_not_rerun_feature_label_matrix_execution",
    "approval_does_not_rerun_feature_label_matrix_results_review",
    "approval_does_not_rerun_vpa_wyckoff_candidate_creation",
    "approval_does_not_rerun_vpa_wyckoff_candidate_review",
    "do_not_mutate_frozen_dataset",
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
    "source_matrix_results_review_digest_bound",
    "source_matrix_execution_digest_bound",
    "source_matrix_rows_digest_bound",
    "source_feature_values_digest_bound",
    "source_target_values_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "approval_scope_only",
    "selected_vpa_wyckoff_package_transparent_baseline",
    "selected_matrix_package_preserved",
    "selected_matrix_layout_preserved",
    "selected_feature_package_preserved",
    "selected_target_package_preserved",
    "selected_objective_path_preserved",
    "vpa_wyckoff_baseline_authorized_for_future_execution_true",
    "vpa_wyckoff_rule_baseline_selected_true",
    "vpa_wyckoff_rule_baseline_approved_true",
    "vpa_wyckoff_rule_baseline_authorized_true",
    "vpa_wyckoff_rule_baseline_executed_false",
    "rule_values_created_false",
    "state_values_created_false",
    "baseline_outputs_created_false",
    "approval_created_true",
    "ready_for_vpa_wyckoff_execution_true",
    "approved_package_present",
    "supporting_package_available_not_selected",
    "selected_rule_families_8",
    "selected_state_families_6",
    "supporting_rule_families_available_not_selected",
    "supporting_state_families_available_not_selected",
    "feature_group_mappings_approved",
    "design_questions_unanswered_12",
    "future_outputs_authorized_not_generated_10",
    "planned_rule_value_rows_179190",
    "planned_rule_state_rows_179190",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "expectancy_backtest_lab_candidate_created_false",
    "backtest_execution_authorized_false",
    "backtest_execution_performed_false",
    "model_training_authorized_false",
    "model_training_performed_false",
    "metric_computation_authorized_false",
    "metric_computation_performed_false",
    "strategy_scoring_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "feature_label_matrix_execution_rerun_false",
    "feature_label_matrix_results_review_rerun_false",
    "vpa_wyckoff_candidate_creation_rerun_false",
    "vpa_wyckoff_candidate_review_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowVpaWyckoffRuleBaselineApprovalError(ValueError):
    """Raised when evidence violates the approval-only contract."""


def build_marketflow_vpa_wyckoff_rule_baseline_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_matrix_results_review_digest: str,
    operator_confirms_matrix_rows_digest: str,
    operator_confirms_feature_values_digest: str,
    operator_confirms_target_values_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_vpa_wyckoff_package: str,
    operator_confirms_selected_matrix_package: str,
    operator_confirms_selected_matrix_layout: str,
    operator_confirms_selected_feature_package: str,
    operator_confirms_selected_label_target_package: str,
    operator_confirms_selected_objective_path: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_vpa_wyckoff_rule_baseline_authorized_for_future_execution_only: bool,
    operator_confirms_vpa_wyckoff_rule_baseline_not_executed: bool,
    operator_confirms_no_rule_values_created: bool,
    operator_confirms_no_state_values_created: bool,
    operator_confirms_no_baseline_outputs_created: bool,
    operator_confirms_no_backtest_execution: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_metric_computation: bool,
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
    selected_vpa_wyckoff_package: str = SELECTED_VPA_WYCKOFF_PACKAGE,
    selected_matrix_package: str = SELECTED_MATRIX_PACKAGE,
    selected_matrix_layout: str = SELECTED_MATRIX_LAYOUT,
    selected_feature_package: str = SELECTED_FEATURE_PACKAGE,
    selected_label_target_package: str = SELECTED_LABEL_TARGET_PACKAGE,
    selected_objective_path: str = SELECTED_OBJECTIVE_PATH,
    operator_decision: str = OPERATOR_DECISION_APPROVE_VPA_WYCKOFF_RULE_BASELINE,
) -> dict:
    """Build the complete non-secret operator attestation object."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_V1
        )
    }


@lru_cache(maxsize=1)
def _canonical_source_review() -> dict:
    return review_service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1()


def _source_review(source_review: dict | None) -> dict:
    source = deepcopy(_canonical_source_review()) if source_review is None else deepcopy(source_review)
    try:
        validation = review_service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
            source
        )
    except review_service.MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError as exc:
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError(
            "source VPA/Wyckoff candidate review invalid"
        ) from exc
    if (
        validation["marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"]
        != EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
    ):
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError(
            "source VPA/Wyckoff candidate review digest mismatch"
        )
    return source


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_VPA_WYCKOFF_RULE_BASELINE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_V1,
        "operator_confirms_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "operator_confirms_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "operator_confirms_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "operator_confirms_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "operator_confirms_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "operator_confirms_selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "operator_confirms_selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "operator_confirms_selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "operator_confirms_selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "operator_confirms_selected_objective_path": SELECTED_OBJECTIVE_PATH,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowVpaWyckoffRuleBaselineApprovalError(f"{field} mismatch")
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowVpaWyckoffRuleBaselineApprovalError(f"{field} must be true")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowVpaWyckoffRuleBaselineApprovalError(f"{field} required")


def _approved_rule_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = {
        row["rule_family_id"]: row
        for row in source["reviewed_vpa_wyckoff_rule_families"]
    }
    return [
        {
            **deepcopy(source_rows[rule_id]),
            "approval_status": "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY",
            "rule_execution_authorized_for_future_execution": True,
            "rule_execution_performed": False,
            "rule_values_created": False,
            "baseline_outputs_created": False,
            "backtest_authorized": False,
            "metric_computation_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for rule_id in SELECTED_RULE_FAMILY_IDS
    ]


def _supporting_rule_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = {
        row["rule_family_id"]: row
        for row in source["reviewed_vpa_wyckoff_rule_families"]
    }
    return [
        {
            **deepcopy(source_rows[rule_id]),
            "approval_status": "AVAILABLE_NOT_SELECTED",
            "rule_execution_authorized": False,
            "rule_execution_performed": False,
            "rule_values_created": False,
            "baseline_outputs_created": False,
            "research_only": True,
            "non_actionable": True,
        }
        for rule_id in SUPPORTING_RULE_FAMILY_IDS
    ]


def _approved_state_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = {
        row["state_family_id"]: row
        for row in source["reviewed_wyckoff_state_families"]
    }
    return [
        {
            **deepcopy(source_rows[state_id]),
            "approval_status": "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY",
            "state_execution_authorized_for_future_execution": True,
            "state_values_created": False,
            "baseline_outputs_created": False,
            "research_only": True,
            "non_actionable": True,
        }
        for state_id in SELECTED_STATE_FAMILY_IDS
    ]


def _supporting_state_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = {
        row["state_family_id"]: row
        for row in source["reviewed_wyckoff_state_families"]
    }
    return [
        {
            **deepcopy(source_rows[state_id]),
            "approval_status": "AVAILABLE_NOT_SELECTED",
            "state_execution_authorized_for_future_execution": False,
            "state_values_created": False,
            "baseline_outputs_created": False,
            "research_only": True,
            "non_actionable": True,
        }
        for state_id in SUPPORTING_STATE_FAMILY_IDS
    ]


def _approved_feature_group_mappings(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["reviewed_feature_group_mapping"])
    for row in rows:
        row["approval_status"] = (
            "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_CONTROL"
        )
        row["mapping_status"] = "PLANNED_NOT_EXECUTED"
        row["target_values_used"] = False
        row["future_data_used"] = False
    return rows


def _approved_design_questions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["reviewed_rule_design_questions"])
    for row in rows:
        row["question_status"] = "NOT_ANSWERED"
        row["approval_status"] = "APPROVED_FOR_FUTURE_RULE_DESIGN_REVIEW_ONLY"
    return rows


def _approved_future_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["reviewed_planned_future_outputs"])
    for row in rows:
        row["approval_status"] = "AUTHORIZED_NOT_GENERATED"
        row["output_status"] = "PLANNED_NOT_GENERATED"
        row["research_only"] = True
        row["non_actionable"] = True
    return rows


def per_ticker_vpa_wyckoff_rule_baseline_approval_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest of one ticker approval entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_vpa_wyckoff_rule_baseline_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = {
        row["ticker"]: row
        for row in source["per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries"]
    }
    rows: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        source_row = source_rows[ticker]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_row["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "vpa_wyckoff_candidate_review_status": review_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
            "vpa_wyckoff_rule_baseline_approval_status": "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY",
            "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
            "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
            "selected_feature_package": SELECTED_FEATURE_PACKAGE,
            "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
            "planned_matrix_row_count": source_row["planned_matrix_row_count"],
            "planned_rule_family_count": 8,
            "planned_wyckoff_state_family_count": 6,
            "vpa_wyckoff_rule_baseline_selected": True,
            "vpa_wyckoff_rule_baseline_approved": True,
            "vpa_wyckoff_rule_baseline_authorized": True,
            "vpa_wyckoff_rule_baseline_executed": False,
            "vpa_wyckoff_rule_values_created": False,
            "vpa_wyckoff_state_values_created": False,
            "vpa_wyckoff_baseline_outputs_created": False,
            "expectancy_backtest_lab_candidate_created": False,
            "backtest_execution_authorized": False,
            "model_training_authorized": False,
            "metric_computation_authorized": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
            "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
            "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "approval_note": (
                "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_APPROVAL"
                if ticker == "META"
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_vpa_wyckoff_rule_baseline_approval_digest"] = (
            per_ticker_vpa_wyckoff_rule_baseline_approval_digest_v1(entry)
        )
        rows.append(entry)
    return rows


def _approved_package() -> dict[str, Any]:
    return {
        "package_id": SELECTED_VPA_WYCKOFF_PACKAGE,
        "approval_status": "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY",
        "included_rule_families": list(SELECTED_RULE_FAMILY_IDS),
        "included_state_families": list(SELECTED_STATE_FAMILY_IDS),
        "selected_rule_family_count": 8,
        "selected_wyckoff_state_family_count": 6,
        "planned_rule_value_rows": 179190,
        "planned_rule_state_rows": 179190,
        "planned_source_matrix_row_count": 179190,
        "planned_rule_evaluation_scope": "RESEARCH_ONLY_RULE_TAGGING_NOT_BACKTEST",
        "rule_execution_performed": False,
        "rule_values_created": False,
        "state_values_created": False,
        "baseline_outputs_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _supporting_package() -> dict[str, Any]:
    return {
        "package_id": SUPPORTING_VPA_WYCKOFF_PACKAGE,
        "approval_status": "AVAILABLE_NOT_SELECTED",
        "included_rule_families": list(SUPPORTING_RULE_FAMILY_IDS),
        "included_state_families": list(SUPPORTING_STATE_FAMILY_IDS),
        "rule_execution_performed": False,
        "rule_values_created": False,
        "state_values_created": False,
        "baseline_outputs_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _base_approval(
    source: Mapping[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_V1,
        "approval_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED,
        "approval_scope": VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "created_offline": True,
        "research_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_vpa_wyckoff_rule_baseline_candidate_review_artifact_kind": source["artifact_kind"],
        "source_vpa_wyckoff_rule_baseline_candidate_review_status": source["review_status"],
        "source_vpa_wyckoff_rule_baseline_candidate_review_scope": source["review_scope"],
        "source_vpa_wyckoff_rule_baseline_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_baseline_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
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
        "feature_group_count_per_matrix_row": source["feature_group_count_per_matrix_row"],
        "feature_group_reference_count": source["feature_group_reference_count"],
        "feature_source_row_count": source["feature_source_row_count"],
        "target_source_row_count": source["target_source_row_count"],
        "vpa_wyckoff_rule_baseline_candidate_created": True,
        "vpa_wyckoff_rule_baseline_candidate_review_created": True,
        "vpa_wyckoff_rule_baseline_candidate_review_ready": True,
        "vpa_wyckoff_rule_baseline_selected": True,
        "vpa_wyckoff_rule_baseline_approved": True,
        "vpa_wyckoff_rule_baseline_authorized": True,
        "vpa_wyckoff_rule_baseline_approval_created": True,
        "ready_for_vpa_wyckoff_rule_baseline_execution": True,
        "vpa_wyckoff_rule_baseline_authorized_for_future_execution": True,
        "vpa_wyckoff_rule_baseline_executed": False,
        "vpa_wyckoff_rule_values_created": False,
        "vpa_wyckoff_state_values_created": False,
        "vpa_wyckoff_baseline_outputs_created": False,
        "expectancy_backtest_lab_candidate_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
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
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "vpa_wyckoff_candidate_creation_rerun_performed": False,
        "vpa_wyckoff_candidate_review_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "approved_vpa_wyckoff_package": _approved_package(),
        "supporting_vpa_wyckoff_package": _supporting_package(),
        "approved_vpa_wyckoff_rule_families": _approved_rule_families(source),
        "supporting_vpa_wyckoff_rule_families": _supporting_rule_families(source),
        "approved_wyckoff_state_families": _approved_state_families(source),
        "supporting_wyckoff_state_families": _supporting_state_families(source),
        "approved_feature_group_mappings": _approved_feature_group_mappings(source),
        "approved_rule_design_questions": _approved_design_questions(source),
        "approved_future_outputs": _approved_future_outputs(source),
        "planned_source_matrix_row_count": 179190,
        "planned_rule_family_count": 8,
        "planned_wyckoff_state_family_count": 6,
        "planned_rule_value_rows": 179190,
        "planned_rule_state_rows": 179190,
        "planned_rule_evaluation_scope": "RESEARCH_ONLY_RULE_TAGGING_NOT_BACKTEST",
        "per_ticker_vpa_wyckoff_rule_baseline_approval_entries": _per_ticker_entries(source),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return (
        isinstance(entries, list)
        and [row.get("ticker") for row in entries if isinstance(row, Mapping)]
        == TARGET_UNIVERSE
        and all(
            isinstance(row, Mapping)
            and row.get("per_ticker_vpa_wyckoff_rule_baseline_approval_digest")
            == per_ticker_vpa_wyckoff_rule_baseline_approval_digest_v1(row)
            for row in entries
        )
    )


def _conditions(approval: Mapping[str, Any]) -> dict[str, bool]:
    operator = approval.get("operator_attestation", {})
    entries = approval.get(
        "per_ticker_vpa_wyckoff_rule_baseline_approval_entries", []
    )
    approved_rules = approval.get("approved_vpa_wyckoff_rule_families", [])
    approved_states = approval.get("approved_wyckoff_state_families", [])
    supporting_rules = approval.get("supporting_vpa_wyckoff_rule_families", [])
    supporting_states = approval.get("supporting_wyckoff_state_families", [])
    conditions = {
        "source_candidate_review_digest_bound": approval.get("source_vpa_wyckoff_rule_baseline_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": approval.get("source_vpa_wyckoff_rule_baseline_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest_bound": approval.get("source_feature_label_matrix_results_review_digest") == EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest_bound": approval.get("source_feature_label_matrix_execution_digest") == EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_rows_digest_bound": approval.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest_bound": approval.get("source_feature_values_digest") == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest_bound": approval.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": approval.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": approval.get("target_universe") == TARGET_UNIVERSE and approval.get("target_universe_count") == 12,
        "records_digest_preserved": approval.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": approval.get("meta_record_count") == 913,
        "operator_decision_matches": operator.get("operator_decision") == OPERATOR_DECISION_APPROVE_VPA_WYCKOFF_RULE_BASELINE,
        "operator_attestation_phrase_matches": operator.get("operator_attestation_phrase") == REQUIRED_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ATTESTATION_PHRASE,
        "approval_scope_only": approval.get("approval_scope") == VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY,
        "selected_vpa_wyckoff_package_transparent_baseline": approval.get("selected_vpa_wyckoff_package") == SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package_preserved": approval.get("selected_matrix_package") == SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout_preserved": approval.get("selected_matrix_layout") == SELECTED_MATRIX_LAYOUT,
        "selected_feature_package_preserved": approval.get("selected_feature_package") == SELECTED_FEATURE_PACKAGE,
        "selected_target_package_preserved": approval.get("selected_label_target_package") == SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path_preserved": approval.get("selected_objective_path") == SELECTED_OBJECTIVE_PATH,
        "vpa_wyckoff_baseline_authorized_for_future_execution_true": approval.get("vpa_wyckoff_rule_baseline_authorized_for_future_execution") is True,
        "vpa_wyckoff_rule_baseline_selected_true": approval.get("vpa_wyckoff_rule_baseline_selected") is True,
        "vpa_wyckoff_rule_baseline_approved_true": approval.get("vpa_wyckoff_rule_baseline_approved") is True,
        "vpa_wyckoff_rule_baseline_authorized_true": approval.get("vpa_wyckoff_rule_baseline_authorized") is True,
        "vpa_wyckoff_rule_baseline_executed_false": approval.get("vpa_wyckoff_rule_baseline_executed") is False,
        "rule_values_created_false": approval.get("vpa_wyckoff_rule_values_created") is False,
        "state_values_created_false": approval.get("vpa_wyckoff_state_values_created") is False,
        "baseline_outputs_created_false": approval.get("vpa_wyckoff_baseline_outputs_created") is False,
        "approval_created_true": approval.get("vpa_wyckoff_rule_baseline_approval_created") is True,
        "ready_for_vpa_wyckoff_execution_true": approval.get("ready_for_vpa_wyckoff_rule_baseline_execution") is True,
        "approved_package_present": approval.get("approved_vpa_wyckoff_package", {}).get("approval_status") == "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY",
        "supporting_package_available_not_selected": approval.get("supporting_vpa_wyckoff_package", {}).get("approval_status") == "AVAILABLE_NOT_SELECTED",
        "selected_rule_families_8": len(approved_rules) == 8 and [row.get("rule_family_id") for row in approved_rules] == SELECTED_RULE_FAMILY_IDS,
        "selected_state_families_6": len(approved_states) == 6 and [row.get("state_family_id") for row in approved_states] == SELECTED_STATE_FAMILY_IDS,
        "supporting_rule_families_available_not_selected": len(supporting_rules) == 2 and [row.get("rule_family_id") for row in supporting_rules] == SUPPORTING_RULE_FAMILY_IDS and all(row.get("approval_status") == "AVAILABLE_NOT_SELECTED" for row in supporting_rules),
        "supporting_state_families_available_not_selected": len(supporting_states) == 2 and [row.get("state_family_id") for row in supporting_states] == SUPPORTING_STATE_FAMILY_IDS and all(row.get("approval_status") == "AVAILABLE_NOT_SELECTED" for row in supporting_states),
        "feature_group_mappings_approved": len(approval.get("approved_feature_group_mappings", [])) == 13 and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_CONTROL" and row.get("mapping_status") == "PLANNED_NOT_EXECUTED" for row in approval.get("approved_feature_group_mappings", [])),
        "design_questions_unanswered_12": len(approval.get("approved_rule_design_questions", [])) == 12 and all(row.get("question_status") == "NOT_ANSWERED" and row.get("approval_status") == "APPROVED_FOR_FUTURE_RULE_DESIGN_REVIEW_ONLY" for row in approval.get("approved_rule_design_questions", [])),
        "future_outputs_authorized_not_generated_10": len(approval.get("approved_future_outputs", [])) == 10 and all(row.get("approval_status") == "AUTHORIZED_NOT_GENERATED" and row.get("output_status") == "PLANNED_NOT_GENERATED" for row in approval.get("approved_future_outputs", [])),
        "planned_rule_value_rows_179190": approval.get("planned_rule_value_rows") == 179190,
        "planned_rule_state_rows_179190": approval.get("planned_rule_state_rows") == 179190,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "expectancy_backtest_lab_candidate_created_false": approval.get("expectancy_backtest_lab_candidate_created") is False,
        "backtest_execution_authorized_false": approval.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": approval.get("backtest_execution_performed") is False,
        "model_training_authorized_false": approval.get("model_training_authorized") is False,
        "model_training_performed_false": approval.get("model_training_performed") is False,
        "metric_computation_authorized_false": approval.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": approval.get("metric_computation_performed") is False,
        "strategy_scoring_false": approval.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": approval.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": approval.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": approval.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": approval.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": approval.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": approval.get("provider_requests_made_in_approval") is False,
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed_in_approval") is False,
        "dataset_regeneration_false": approval.get("canonical_dataset_regenerated_in_approval") is False,
        "feature_label_matrix_execution_rerun_false": approval.get("feature_label_matrix_execution_rerun_performed") is False,
        "feature_label_matrix_results_review_rerun_false": approval.get("feature_label_matrix_results_review_rerun_performed") is False,
        "vpa_wyckoff_candidate_creation_rerun_false": approval.get("vpa_wyckoff_candidate_creation_rerun_performed") is False,
        "vpa_wyckoff_candidate_review_rerun_false": approval.get("vpa_wyckoff_candidate_review_rerun_performed") is False,
        "raw_provider_payloads_not_committed": approval.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": approval.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": approval.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": approval.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": approval.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files") is True,
    }
    if list(conditions) != REQUIRED_CHECK_IDS:
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError(
            "internal checklist definition mismatch"
        )
    return conditions


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "status": PASS if actual else FAIL,
            "expected": True,
            "actual": actual,
            "severity": BLOCKER,
            "message": f"{check_id} {'passed' if actual else 'failed'}",
        }
        for check_id, actual in _conditions(approval).items()
    ]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "vpa_wyckoff_rule_baseline_selected": True,
        "vpa_wyckoff_rule_baseline_approved": True,
        "vpa_wyckoff_rule_baseline_authorized": True,
        "ready_for_vpa_wyckoff_rule_baseline_execution": True,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "vpa_wyckoff_rule_baseline_authorized_for_future_execution": True,
        "vpa_wyckoff_rule_baseline_executed": False,
        "vpa_wyckoff_rule_values_created": False,
        "vpa_wyckoff_state_values_created": False,
        "vpa_wyckoff_baseline_outputs_created": False,
        "expectancy_backtest_lab_candidate_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_vpa_wyckoff_rule_baseline_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    payload = deepcopy(dict(approval))
    payload.pop("approval_checklist", None)
    payload.pop("approval_summary", None)
    payload.pop("marketflow_vpa_wyckoff_rule_baseline_approval_digest", None)
    return semantic_digest(payload)


def build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict
) -> dict:
    """Build approval for future VPA/Wyckoff rule-baseline execution only."""
    source = _source_review(source_review)
    _validate_attestation(operator_attestation)
    approval = _base_approval(source, operator_attestation)
    checklist = _checklist(approval)
    approval["approval_checklist"] = checklist
    approval["approval_summary"] = _summary(checklist)
    approval["marketflow_vpa_wyckoff_rule_baseline_approval_digest"] = (
        marketflow_vpa_wyckoff_rule_baseline_approval_digest_v1(approval)
    )
    validate_marketflow_vpa_wyckoff_rule_baseline_approval_v1(approval)
    return approval


def validate_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
    approval: dict,
) -> dict:
    """Validate attestation, evidence, approved controls, and closed authorities."""
    if not isinstance(approval, dict):
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError(
            "approval must be a JSON object"
        )
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(_source_review(None), attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowVpaWyckoffRuleBaselineApprovalError(f"{field} mismatch")
    expected_checklist = _checklist(approval)
    if approval.get("approval_checklist") != expected_checklist or any(
        row["status"] != PASS for row in expected_checklist
    ):
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError(
            "approval checklist mismatch"
        )
    if approval.get("approval_summary") != _summary(expected_checklist):
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError("approval summary mismatch")
    digest = approval.get("marketflow_vpa_wyckoff_rule_baseline_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError("approval digest missing")
    if digest != marketflow_vpa_wyckoff_rule_baseline_approval_digest_v1(approval):
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError("approval digest mismatch")
    return {
        "status": "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_VALID",
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_vpa_wyckoff_rule_baseline_approval_digest": digest,
        **{
            field: approval["approval_summary"][field]
            for field in (
                "total_checks",
                "passed_checks",
                "failed_checks",
                "blocker_count",
            )
        },
    }


def build_marketflow_vpa_wyckoff_rule_baseline_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view of the validated approval artifact."""
    validation = validate_marketflow_vpa_wyckoff_rule_baseline_approval_v1(approval)
    operator = approval["operator_attestation"]
    sections = [
        ("Title", ["VPA/Wyckoff Rule Baseline Approval v1"]),
        (
            "VPA/Wyckoff Rule Baseline Approval v1",
            [
                f"Artifact/status/scope: `{approval['artifact_kind']}` / "
                f"`{approval['approval_status']}` / `{approval['approval_scope']}`.",
                "Approval digest: "
                f"`{validation['marketflow_vpa_wyckoff_rule_baseline_approval_digest']}`.",
            ],
        ),
        (
            "Operator Attestation",
            [
                f"Decision/reference/timestamp: `{operator['operator_decision']}` / "
                f"`{operator['operator_reference']}` / "
                f"`{operator['operator_attestation_timestamp_utc']}`.",
                f"Exact phrase: {operator['operator_attestation_phrase']}.",
            ],
        ),
        (
            "Source Candidate Review",
            [
                "Review/candidate digests: "
                f"`{approval['source_vpa_wyckoff_rule_baseline_candidate_review_digest']}` / "
                f"`{approval['source_vpa_wyckoff_rule_baseline_candidate_digest']}`."
            ],
        ),
        (
            "Bound Evidence",
            [
                "Matrix review/rows: "
                f"`{approval['source_feature_label_matrix_results_review_digest']}` / "
                f"`{approval['source_feature_label_matrix_rows_digest']}`.",
                "Feature/target values: "
                f"`{approval['source_feature_values_digest']}` / "
                f"`{approval['source_target_values_digest']}`.",
                f"Records: `{approval['records_digest']}`; complete upstream digest chain preserved.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"`{approval['dataset_name']}`, {approval['total_canonical_record_count']} "
                f"records; {', '.join(approval['target_universe'])}.",
                "META remains exactly 913 records; every other ticker remains 1,003.",
            ],
        ),
        (
            "Approval Scope",
            [
                "Future research-only VPA/Wyckoff rule-baseline execution; "
                "this artifact performs no rule or state evaluation."
            ],
        ),
        ("Selected VPA/Wyckoff Package", [approval["selected_vpa_wyckoff_package"]]),
        (
            "Selected Matrix and Feature Packages",
            [
                f"{approval['selected_matrix_package']} / {approval['selected_matrix_layout']}.",
                f"{approval['selected_feature_package']} / "
                f"{approval['selected_label_target_package']} / "
                f"{approval['selected_objective_path']}.",
            ],
        ),
        (
            "Approved Rule Families",
            [row["rule_family_id"] for row in approval["approved_vpa_wyckoff_rule_families"]],
        ),
        (
            "Approved Wyckoff State Families",
            [row["state_family_id"] for row in approval["approved_wyckoff_state_families"]],
        ),
        (
            "Supporting Package",
            [
                f"{approval['supporting_vpa_wyckoff_package']['package_id']}: "
                "available, not selected."
            ],
        ),
        (
            "Approved Feature Group Mapping",
            [
                f"{row['source_feature_group']} -> "
                f"{', '.join(row['planned_rule_or_state_families'])}."
                for row in approval["approved_feature_group_mappings"]
            ],
        ),
        (
            "Design Questions",
            [
                f"{row['question_id']}: {row['question_status']}."
                for row in approval["approved_rule_design_questions"]
            ],
        ),
        (
            "Approved Future Outputs",
            [
                f"{row['output_id']}: {row['approval_status']}."
                for row in approval["approved_future_outputs"]
            ],
        ),
        (
            "Planned Counts",
            [
                f"{approval['planned_rule_value_rows']} planned rule-value rows; "
                f"{approval['planned_rule_state_rows']} planned state rows; no rows generated."
            ],
        ),
        (
            "Per-Ticker Approval Summary",
            [
                f"{row['ticker']}: records {row['historical_record_count']}, planned rows "
                f"{row['planned_matrix_row_count']}, digest "
                f"`{row['per_ticker_vpa_wyckoff_rule_baseline_approval_digest']}`."
                for row in approval[
                    "per_ticker_vpa_wyckoff_rule_baseline_approval_entries"
                ]
            ],
        ),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", approval["next_gates"]),
        ("Risk Controls", approval["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        (
            "Runtime Boundary",
            [
                "Runtime, strategy, paper trading, and broker execution remain "
                "NOT_AUTHORIZED."
            ],
        ),
        (
            "Checklist Summary",
            [
                f"{approval['approval_summary']['passed_checks']}/"
                f"{approval['approval_summary']['total_checks']} checks pass with zero blockers."
            ],
        ),
        (
            "Guardrails",
            [
                "This approval creates no rule values, state values, baseline outputs, "
                "backtest, metric, model, recommendation, acceptance, runtime artifact, "
                "or trading authority."
            ],
        ),
    ]
    lines = ["# VPA/Wyckoff Rule Baseline Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", "", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write validated approval JSON and Markdown to an explicit directory."""
    approval = build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation
    )
    validation = validate_marketflow_vpa_wyckoff_rule_baseline_approval_v1(approval)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_vpa_wyckoff_rule_baseline_approval_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowVpaWyckoffRuleBaselineApprovalError(
            "VPA/Wyckoff rule-baseline approval output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(approval))
    markdown_path.write_text(
        build_marketflow_vpa_wyckoff_rule_baseline_approval_markdown_v1(approval),
        encoding="utf-8",
        newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path).replace("\\", "/"),
        "markdown_path": str(markdown_path).replace("\\", "/"),
    }
