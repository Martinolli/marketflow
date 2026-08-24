"""Offline candidate for a future feature-label matrix construction contract."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_objective_label_or_target_generation_results_review_service as target_review,
)
from marketflow.services import (
    marketflow_signal_or_feature_generation_results_review_service as feature_review,
)


ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1 = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1 = (
    "marketflow_feature_label_matrix_candidate_v1"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION = (
    "FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION"
)
PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX = (
    "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_VALID = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_VALID"
)

EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST = (
    "8de3cfa3d4543a05956c4d9e55940525417336ffcbe523c674b43924fd22ddb7"
)
EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST = (
    "bcccbdc57616e7ff0c350535628a4a2b2cb752e11b4c98b0b9905fed9f9e4e60"
)
EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST = (
    "5e0ef154d13782bc58c284b2d664f35e7f0724bb890efc2235e840df62dbf4e8"
)
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = (
    "7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e"
)
EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST = (
    "41afa9e7159f2788f8dce3c44343c2058414fb51efb95b5d6714246ab866e47c"
)
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = (
    "61480462caa3cb1177b56b72276c439035a69a28294cc1154d272f02515a8119"
)

TARGET_UNIVERSE = list(feature_review.TARGET_UNIVERSE)
NOT_ACCEPTED = feature_review.NOT_ACCEPTED
NOT_AUTHORIZED = feature_review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SOURCE_EVIDENCE = {
    "marketflow_signal_or_feature_generation_results_review_digest": EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
    **feature_review.SOURCE_EVIDENCE,
}

CANDIDATE_PHILOSOPHY = (
    "Prepare a future feature-label matrix by defining how reviewed history-only "
    "feature rows may be aligned to reviewed expectancy target rows without leaking "
    "target values, future data, strategy scores, recommendations, or runtime "
    "authority into predictors."
)
CANDIDATE_PRIMARY_QUESTION = (
    "What matrix layout should connect 13 history-only feature groups to 15 "
    "expectancy target profiles while preserving target availability, no-peek "
    "controls, and per-ticker/META limitations?"
)
CANDIDATE_SECONDARY_QUESTION = (
    "Should the first matrix use one row per target profile with a wide feature "
    "bundle, or a long audit layout for feature-target traceability?"
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no matrix rows, joined outputs, metrics, models, backtests, "
    "scores, recommendations, or runtime artifacts are created."
)

MATRIX_LAYOUTS = [
    {
        "layout_id": "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE",
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "planned_matrix_row_count": 179190,
        "planned_available_matrix_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_feature_group_count_per_matrix_row": 13,
        "rationale": "One matrix row per target profile, with history-only features bundled by ticker/date/canonical index. This mirrors target availability and avoids row explosion.",
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
    },
    {
        "layout_id": "MATRIX_LAYOUT_LONG_FEATURE_TARGET_AUDIT",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "planned_long_audit_pair_count": 2329470,
        "calculation": "179190 target rows x 13 feature groups",
        "rationale": "Useful for auditing each feature group against each target profile, but too large for the first primary matrix.",
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
    },
    {
        "layout_id": "MATRIX_LAYOUT_CANONICAL_RECORD_FEATURE_BUNDLE",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "planned_canonical_feature_bundle_count": 11946,
        "rationale": "Useful as an intermediate feature bundle keyed by canonical record before target expansion.",
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
    },
]

ALIGNMENT_KEY_IDS = [
    "MATRIX_KEY_DATASET_NAME",
    "MATRIX_KEY_SOURCE_PROFILE",
    "MATRIX_KEY_TIMEFRAME",
    "MATRIX_KEY_TICKER",
    "MATRIX_KEY_DATE",
    "MATRIX_KEY_CANONICAL_RECORD_INDEX",
    "MATRIX_KEY_TARGET_FAMILY",
    "MATRIX_KEY_TARGET_HORIZON_SESSIONS",
    "MATRIX_KEY_TARGET_PROFILE",
]
FEATURE_SIDE_JOIN_RULE_IDS = [
    "RULE_JOIN_FEATURES_BY_TICKER_DATE_CANONICAL_INDEX",
    "RULE_USE_ONLY_REVIEWED_FEATURE_VALUES_DIGEST",
    "RULE_FEATURE_GROUPS_BUNDLED_HISTORY_ONLY",
    "RULE_FEATURE_UNAVAILABLE_VALUES_RETAINED_AS_NULL",
    "RULE_NO_TARGET_VALUES_IN_FEATURE_BUNDLE",
    "RULE_NO_TARGET_CLASSES_IN_FEATURE_BUNDLE",
    "RULE_NO_FORWARD_RETURNS_IN_FEATURE_BUNDLE",
    "RULE_NO_FUTURE_DATA_IN_FEATURE_BUNDLE",
]
TARGET_SIDE_JOIN_RULE_IDS = [
    "RULE_JOIN_TARGETS_BY_TICKER_DATE_CANONICAL_INDEX",
    "RULE_EXPAND_ONE_ROW_PER_TARGET_PROFILE",
    "RULE_RETAIN_TARGET_UNAVAILABLE_ROWS_WITH_NULL_TARGETS",
    "RULE_EXCLUDE_UNAVAILABLE_TARGETS_FROM_FUTURE_MODEL_TRAINING",
    "RULE_TARGET_PROFILE_AND_HORIZON_AS_METADATA",
    "RULE_TARGET_VALUE_IS_OUTCOME_NOT_PREDICTOR",
    "RULE_TARGET_CLASS_IS_OUTCOME_NOT_PREDICTOR",
]
QUALITY_CHECK_IDS = [
    "CHECK_FEATURE_VALUES_DIGEST_MATCHES_SOURCE",
    "CHECK_TARGET_VALUES_DIGEST_MATCHES_SOURCE",
    "CHECK_RECORDS_DIGEST_MATCHES_SOURCE",
    "CHECK_MATRIX_ROW_COUNT_EXPECTED",
    "CHECK_TARGET_AVAILABILITY_COUNTS_PRESERVED",
    "CHECK_FEATURE_AVAILABILITY_COUNTS_PRESERVED",
    "CHECK_NO_TARGET_LEAKAGE_IN_FEATURE_COLUMNS",
    "CHECK_NO_FORWARD_RETURN_FEATURES",
    "CHECK_NO_FUTURE_DATA_FEATURES",
    "CHECK_PER_TICKER_MATRIX_COUNTS",
    "CHECK_META_LIMITATION_PRESERVED",
    "CHECK_RESEARCH_ONLY_AUTHORITY_BOUNDARY",
    "CHECK_DIGEST_MANIFEST_REQUIRED",
]
FUTURE_OUTPUT_IDS = [
    "future_feature_label_matrix_manifest",
    "future_feature_label_matrix_schema",
    "future_feature_bundle_schema",
    "future_target_profile_schema",
    "future_matrix_rows_jsonl",
    "future_matrix_coverage_report",
    "future_matrix_no_peek_report",
    "future_matrix_target_availability_report",
    "future_per_ticker_matrix_report",
    "future_meta_limitation_report",
    "future_operator_summary",
    "future_digest_manifest",
]

NEXT_CHAIN = [
    "Feature-Label Matrix Candidate Operator Review v1.",
    "Feature-Label Matrix Approval v1, if selected.",
    "Feature-Label Matrix Execution v1, if approved.",
    "Feature-Label Matrix Results Review v1.",
    "VPA/Wyckoff baseline candidate only after separate approval.",
    "Expectancy backtest lab candidate only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "feature_label_matrix_candidate_operator_review",
    "feature_label_matrix_approval_if_selected",
    "feature_label_matrix_execution_if_approved",
    "feature_label_matrix_results_review",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_create_feature_label_matrix",
    "candidate_does_not_join_features_and_targets",
    "candidate_does_not_create_matrix_rows",
    "candidate_does_not_run_backtest",
    "candidate_does_not_train_models",
    "candidate_does_not_compute_metrics",
    "candidate_does_not_score_strategy",
    "candidate_does_not_generate_trade_recommendations",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_call_providers",
    "candidate_does_not_acquire_market_data",
    "candidate_does_not_rerun_target_generation_execution",
    "candidate_does_not_rerun_target_results_review",
    "candidate_does_not_rerun_signal_feature_generation_execution",
    "candidate_does_not_rerun_signal_feature_results_review",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_signal_feature_results_review_digest_bound",
    "source_signal_feature_execution_digest_bound",
    "source_signal_feature_output_binding_digest_bound",
    "source_feature_values_digest_bound", "source_signal_feature_approval_digest_bound",
    "source_signal_feature_candidate_review_digest_bound",
    "source_signal_feature_candidate_digest_bound",
    "source_target_results_review_digest_bound",
    "source_target_generation_execution_digest_bound",
    "source_target_output_binding_digest_bound", "source_target_values_digest_bound",
    "source_target_approval_digest_bound", "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound", "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_strategy_charter_approval_digest_bound", "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound", "source_archive_digest_bound",
    "source_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_prior_execution_digest_bound",
    "prior_matrix_digest_bound", "prior_feature_values_digest_bound",
    "prior_label_values_digest_bound", "research_registry_digest_bound",
    "records_digest_bound", "target_universe_12_preserved",
    "records_digest_preserved", "meta_913_preserved",
    "target_results_review_ready_true", "signal_feature_results_review_ready_true",
    "ready_for_matrix_candidate_true", "candidate_created_true", "candidate_ready_true",
    "candidate_scope_only", "selected_feature_package_preserved",
    "selected_target_package_preserved", "selected_objective_path_preserved",
    "feature_values_digest_bound", "target_values_digest_bound",
    "feature_row_count_155298_preserved", "target_row_count_179190_preserved",
    "planned_matrix_row_count_179190", "planned_available_matrix_row_count_177090",
    "planned_unavailable_target_row_count_2100", "recommended_matrix_package_defined",
    "matrix_layouts_defined", "alignment_keys_defined", "feature_side_join_rules_defined",
    "target_side_join_rules_defined", "quality_checks_defined", "future_outputs_not_generated",
    "per_ticker_entries_12", "per_ticker_digests_present", "selection_created_false",
    "approval_created_false", "execution_created_false", "feature_label_matrix_selected_false",
    "feature_label_matrix_approved_false", "feature_label_matrix_created_false",
    "feature_label_matrix_rows_created_false", "backtest_execution_authorized_false",
    "backtest_execution_performed_false", "model_training_authorized_false",
    "model_training_performed_false", "metric_computation_authorized_false",
    "metric_computation_performed_false", "strategy_scoring_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "target_generation_execution_rerun_false", "target_results_review_rerun_false",
    "signal_feature_generation_execution_rerun_false",
    "signal_feature_results_review_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowFeatureLabelMatrixCandidateError(ValueError):
    """Raised when a matrix candidate violates the candidate-only contract."""


def _planned_entries(ids: list[str], *, kind: str) -> list[dict[str, Any]]:
    status_field = "quality_check_status" if kind == "quality_check" else (
        "key_status" if kind == "alignment_key" else "rule_status"
    )
    return [
        {
            f"{kind}_id": item,
            status_field: "PLANNED_NOT_EXECUTED",
            **(
                {"requires_future_matrix_approval": True}
                if kind != "quality_check"
                else {}
            ),
        }
        for item in ids
    ]


def _per_ticker_entries() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": 913 if is_meta else 1003,
            "meta_reduced_record_count_flag": is_meta,
            "signal_or_feature_results_review_status": feature_review.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
            "target_results_review_status": target_review.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
            "feature_label_matrix_candidate_status": "READY_FOR_OPERATOR_REVIEW",
            "selected_feature_package": feature_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": feature_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": feature_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "recommended_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "planned_matrix_row_count": 13695 if is_meta else 15045,
            "planned_available_matrix_row_count": 13520 if is_meta else 14870,
            "planned_unavailable_target_row_count": 175,
            "planned_feature_row_count": 11869 if is_meta else 13039,
            "feature_label_matrix_selected": False,
            "feature_label_matrix_approved": False,
            "feature_label_matrix_created": False,
            "feature_label_matrix_rows_created": False,
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
            "source_signal_feature_results_review_digest": EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
            "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
            "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "candidate_note": (
                "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_CANDIDATE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_feature_label_matrix_candidate_digest"] = semantic_digest(entry)
        rows.append(entry)
    return rows


def _base_candidate() -> dict[str, Any]:
    alignment_keys = _planned_entries(ALIGNMENT_KEY_IDS, kind="alignment_key")
    feature_rules = _planned_entries(
        FEATURE_SIDE_JOIN_RULE_IDS, kind="feature_side_join_rule"
    )
    target_rules = _planned_entries(
        TARGET_SIDE_JOIN_RULE_IDS, kind="target_side_join_rule"
    )
    quality_checks = _planned_entries(QUALITY_CHECK_IDS, kind="quality_check")
    future_outputs = [
        {
            "output_id": item,
            "output_status": "PLANNED_NOT_GENERATED",
            "research_only": True,
            "non_actionable": True,
        }
        for item in FUTURE_OUTPUT_IDS
    ]
    recommended_package = {
        "package_id": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "selected_feature_package": feature_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": feature_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": feature_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "recommended_layout": "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE",
        "planned_matrix_row_count": 179190,
        "planned_available_matrix_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_feature_group_count": 13,
        "planned_target_profile_count": 15,
        "rationale": "This package aligns the reviewed signal/feature values to the reviewed expectancy target profiles while preserving no-peek, target availability, and research-only boundaries.",
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
    }
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION,
        "selected_feature_package": feature_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": feature_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": feature_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_signal_or_feature_generation_results_review_artifact_kind": feature_review.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE,
        "source_signal_or_feature_generation_results_review_status": feature_review.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "source_signal_or_feature_generation_results_review_scope": feature_review.SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "source_signal_or_feature_generation_results_review_digest": EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
        "source_signal_or_feature_generation_execution_digest": EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST,
        "source_signal_or_feature_generation_output_binding_digest": EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST,
        "source_signal_or_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_objective_label_or_target_generation_results_review_artifact_kind": target_review.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE,
        "source_objective_label_or_target_generation_results_review_status": target_review.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "source_objective_label_or_target_generation_results_review_digest": EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
        "source_objective_label_or_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": feature_review.execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "target_results_review_ready": True,
        "signal_or_feature_generation_results_review_ready": True,
        "ready_for_feature_label_matrix_candidate": True,
        "feature_label_matrix_candidate_created": True,
        "feature_label_matrix_candidate_ready_for_operator_review": True,
        "ready_for_feature_label_matrix_candidate_operator_review": True,
        "feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "feature_row_count": 155298,
        "available_feature_row_count": 155142,
        "unavailable_feature_row_count": 156,
        "target_row_count": 179190,
        "available_target_row_count": 177090,
        "unavailable_target_row_count": 2100,
        "selected_feature_group_count": 13,
        "target_profile_count": 15,
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_primary_question": CANDIDATE_PRIMARY_QUESTION,
        "candidate_secondary_question": CANDIDATE_SECONDARY_QUESTION,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "matrix_layouts": deepcopy(MATRIX_LAYOUTS),
        "recommended_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "recommended_matrix_package_definition": recommended_package,
        "matrix_alignment_keys": alignment_keys,
        "feature_side_join_rules": feature_rules,
        "target_side_join_rules": target_rules,
        "matrix_quality_checks": quality_checks,
        "planned_future_outputs": future_outputs,
        "planned_matrix_row_count": 179190,
        "planned_available_matrix_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_feature_group_count": 13,
        "planned_target_profile_count": 15,
        "planned_canonical_record_count": 11946,
        "per_ticker_feature_label_matrix_candidate_entries": _per_ticker_entries(),
        "feature_label_matrix_selected": False,
        "feature_label_matrix_approved": False,
        "feature_label_matrix_authorized": False,
        "feature_label_matrix_created": False,
        "feature_label_matrix_rows_created": False,
        "feature_label_matrix_execution_performed": False,
        "selection_created": False,
        "approval_created": False,
        "creation_created": False,
        "execution_created": False,
        "generation_created": False,
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
        "provider_requests_made_in_candidate": False,
        "live_provider_transport_enabled_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "signal_or_feature_generation_execution_rerun_performed": False,
        "signal_or_feature_generation_results_review_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": actual,
        "severity": BLOCKER,
        "message": "candidate condition satisfied" if actual else "candidate condition failed",
    }


def _check_values(candidate: Mapping[str, Any]) -> dict[str, bool]:
    evidence = candidate.get("source_evidence", {})
    entries = candidate.get("per_ticker_feature_label_matrix_candidate_entries", [])
    evidence_checks = {
        "source_signal_feature_results_review_digest_bound": "marketflow_signal_or_feature_generation_results_review_digest",
        "source_signal_feature_execution_digest_bound": "marketflow_signal_or_feature_generation_execution_digest",
        "source_signal_feature_output_binding_digest_bound": "signal_or_feature_generation_output_binding_digest",
        "source_feature_values_digest_bound": "signal_or_feature_values_digest",
        "source_signal_feature_approval_digest_bound": "marketflow_signal_or_feature_generation_approval_digest",
        "source_signal_feature_candidate_review_digest_bound": "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
        "source_signal_feature_candidate_digest_bound": "marketflow_signal_or_feature_generation_candidate_v1_digest",
        "source_target_results_review_digest_bound": "marketflow_objective_label_or_target_generation_results_review_digest",
        "source_target_generation_execution_digest_bound": "marketflow_objective_label_or_target_generation_execution_digest",
        "source_target_output_binding_digest_bound": "objective_label_or_target_generation_output_binding_digest",
        "source_target_values_digest_bound": "objective_label_or_target_values_digest",
        "source_target_approval_digest_bound": "marketflow_objective_label_or_target_generation_approval_digest",
        "source_design_results_review_digest_bound": "marketflow_expectancy_objective_design_results_review_digest",
        "source_design_execution_digest_bound": "marketflow_expectancy_objective_design_execution_digest",
        "source_design_output_binding_digest_bound": "expectancy_objective_design_output_binding_digest",
        "source_expectancy_objective_approval_digest_bound": "marketflow_expectancy_objective_approval_digest",
        "source_strategy_charter_approval_digest_bound": "marketflow_algorithm_strategy_charter_approval_digest",
        "source_strategy_charter_digest_bound": "marketflow_algorithm_strategy_charter_v1_digest",
        "source_final_archive_digest_bound": "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest",
        "source_archive_digest_bound": "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest",
        "source_selection_digest_bound": "operator_method_or_closure_selection_using_improved_evidence_digest",
        "source_closure_digest_bound": "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest",
        "source_readiness_digest_bound": "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest",
        "source_reassessment_digest_bound": "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest",
        "source_results_review_digest_bound": "additional_predictive_evidence_results_review_using_improved_evidence_digest",
        "source_prior_execution_digest_bound": "additional_predictive_evidence_execution_using_improved_evidence_digest",
        "prior_matrix_digest_bound": "feature_label_matrix_digest",
        "prior_feature_values_digest_bound": "feature_values_digest",
        "prior_label_values_digest_bound": "redesigned_label_values_digest",
        "research_registry_digest_bound": "research_registry_approval_digest",
        "records_digest_bound": "records_digest",
    }
    values = {
        check_id: evidence.get(key) == SOURCE_EVIDENCE[key]
        for check_id, key in evidence_checks.items()
    }
    values.update({
        "target_universe_12_preserved": candidate.get("target_universe") == TARGET_UNIVERSE and candidate.get("target_universe_count") == 12,
        "records_digest_preserved": candidate.get("records_digest") == feature_review.execution.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": candidate.get("meta_record_count") == 913,
        "target_results_review_ready_true": candidate.get("target_results_review_ready") is True,
        "signal_feature_results_review_ready_true": candidate.get("signal_or_feature_generation_results_review_ready") is True,
        "ready_for_matrix_candidate_true": candidate.get("ready_for_feature_label_matrix_candidate") is True,
        "candidate_created_true": candidate.get("feature_label_matrix_candidate_created") is True,
        "candidate_ready_true": candidate.get("feature_label_matrix_candidate_ready_for_operator_review") is True and candidate.get("ready_for_feature_label_matrix_candidate_operator_review") is True,
        "candidate_scope_only": candidate.get("candidate_scope") == FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION,
        "selected_feature_package_preserved": candidate.get("selected_feature_package") == feature_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_target_package_preserved": candidate.get("selected_label_target_package") == feature_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": candidate.get("selected_objective_path") == feature_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "feature_values_digest_bound": candidate.get("feature_values_digest") == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "target_values_digest_bound": candidate.get("target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "feature_row_count_155298_preserved": candidate.get("feature_row_count") == 155298,
        "target_row_count_179190_preserved": candidate.get("target_row_count") == 179190,
        "planned_matrix_row_count_179190": candidate.get("planned_matrix_row_count") == 179190,
        "planned_available_matrix_row_count_177090": candidate.get("planned_available_matrix_row_count") == 177090,
        "planned_unavailable_target_row_count_2100": candidate.get("planned_unavailable_target_row_count") == 2100,
        "recommended_matrix_package_defined": candidate.get("recommended_matrix_package") == PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX and candidate.get("recommended_matrix_package_definition", {}).get("status") == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "matrix_layouts_defined": candidate.get("matrix_layouts") == MATRIX_LAYOUTS,
        "alignment_keys_defined": [row.get("alignment_key_id") for row in candidate.get("matrix_alignment_keys", [])] == ALIGNMENT_KEY_IDS,
        "feature_side_join_rules_defined": [row.get("feature_side_join_rule_id") for row in candidate.get("feature_side_join_rules", [])] == FEATURE_SIDE_JOIN_RULE_IDS,
        "target_side_join_rules_defined": [row.get("target_side_join_rule_id") for row in candidate.get("target_side_join_rules", [])] == TARGET_SIDE_JOIN_RULE_IDS,
        "quality_checks_defined": [row.get("quality_check_id") for row in candidate.get("matrix_quality_checks", [])] == QUALITY_CHECK_IDS,
        "future_outputs_not_generated": [row.get("output_id") for row in candidate.get("planned_future_outputs", [])] == FUTURE_OUTPUT_IDS and all(row.get("output_status") == "PLANNED_NOT_GENERATED" for row in candidate.get("planned_future_outputs", [])),
        "per_ticker_entries_12": len(entries) == 12 and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(isinstance(row.get("per_ticker_feature_label_matrix_candidate_digest"), str) and len(row["per_ticker_feature_label_matrix_candidate_digest"]) == 64 for row in entries),
        "selection_created_false": candidate.get("selection_created") is False,
        "approval_created_false": candidate.get("approval_created") is False,
        "execution_created_false": candidate.get("execution_created") is False,
        "feature_label_matrix_selected_false": candidate.get("feature_label_matrix_selected") is False,
        "feature_label_matrix_approved_false": candidate.get("feature_label_matrix_approved") is False,
        "feature_label_matrix_created_false": candidate.get("feature_label_matrix_created") is False,
        "feature_label_matrix_rows_created_false": candidate.get("feature_label_matrix_rows_created") is False,
        "backtest_execution_authorized_false": candidate.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": candidate.get("backtest_execution_performed") is False,
        "model_training_authorized_false": candidate.get("model_training_authorized") is False,
        "model_training_performed_false": candidate.get("model_training_performed") is False,
        "metric_computation_authorized_false": candidate.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": candidate.get("metric_computation_performed") is False,
        "strategy_scoring_false": candidate.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": candidate.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": candidate.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": candidate.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": candidate.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": candidate.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": candidate.get("provider_requests_made_in_candidate") is False,
        "market_data_acquisition_false": candidate.get("market_data_acquisition_performed_in_candidate") is False,
        "dataset_regeneration_false": candidate.get("canonical_dataset_regenerated_in_candidate") is False,
        "target_generation_execution_rerun_false": candidate.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": candidate.get("target_generation_results_review_rerun_performed") is False,
        "signal_feature_generation_execution_rerun_false": candidate.get("signal_or_feature_generation_execution_rerun_performed") is False,
        "signal_feature_results_review_rerun_false": candidate.get("signal_or_feature_generation_results_review_rerun_performed") is False,
        "raw_provider_payloads_not_committed": candidate.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": candidate.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": candidate.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": candidate.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True,
    })
    return values


def _candidate_checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(candidate)
    return [_check(check_id, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(row["status"] == FAIL for row in checklist),
        "feature_label_matrix_candidate_created": True,
        "feature_label_matrix_candidate_ready_for_operator_review": True,
        "recommended_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "planned_matrix_row_count": 179190,
        "planned_available_matrix_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
        "feature_label_matrix_created": False,
        "feature_label_matrix_rows_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_feature_label_matrix_candidate_v1_digest(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    payload.pop("marketflow_feature_label_matrix_candidate_v1_digest", None)
    return semantic_digest(payload)


def build_marketflow_feature_label_matrix_candidate_v1() -> dict:
    """Build candidate-only matrix planning metadata without joining source rows."""
    candidate = _base_candidate()
    checklist = _candidate_checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    if candidate["candidate_summary"]["blocker_count"]:
        raise MarketFlowFeatureLabelMatrixCandidateError(
            "feature-label matrix candidate checklist contains blockers"
        )
    candidate["marketflow_feature_label_matrix_candidate_v1_digest"] = (
        marketflow_feature_label_matrix_candidate_v1_digest(candidate)
    )
    validate_marketflow_feature_label_matrix_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowFeatureLabelMatrixCandidateError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_feature_label_matrix_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate candidate-only matrix planning evidence and closed boundaries."""
    if not isinstance(candidate, dict):
        raise MarketFlowFeatureLabelMatrixCandidateError(
            "feature-label matrix candidate must be a JSON object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION,
        "selected_feature_package": feature_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": feature_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": feature_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_signal_or_feature_generation_results_review_artifact_kind": feature_review.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE,
        "source_signal_or_feature_generation_results_review_status": feature_review.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "source_signal_or_feature_generation_results_review_scope": feature_review.SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "source_signal_or_feature_generation_results_review_digest": EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
        "source_signal_or_feature_generation_execution_digest": EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST,
        "source_signal_or_feature_generation_output_binding_digest": EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST,
        "source_signal_or_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_objective_label_or_target_generation_results_review_artifact_kind": target_review.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE,
        "source_objective_label_or_target_generation_results_review_status": target_review.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "source_objective_label_or_target_generation_results_review_digest": EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
        "source_objective_label_or_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_evidence": SOURCE_EVIDENCE,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": feature_review.execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "feature_row_count": 155298,
        "available_feature_row_count": 155142,
        "unavailable_feature_row_count": 156,
        "target_row_count": 179190,
        "available_target_row_count": 177090,
        "unavailable_target_row_count": 2100,
        "selected_feature_group_count": 13,
        "target_profile_count": 15,
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_primary_question": CANDIDATE_PRIMARY_QUESTION,
        "candidate_secondary_question": CANDIDATE_SECONDARY_QUESTION,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "matrix_layouts": MATRIX_LAYOUTS,
        "recommended_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "planned_matrix_row_count": 179190,
        "planned_available_matrix_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_feature_group_count": 13,
        "planned_target_profile_count": 15,
        "planned_canonical_record_count": 11946,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(candidate.get(field), expected, field)
    for field in (
        "created_offline", "research_only", "operator_review_required",
        "meta_reduced_record_count_preserved", "target_results_review_ready",
        "signal_or_feature_generation_results_review_ready",
        "ready_for_feature_label_matrix_candidate", "feature_label_matrix_candidate_created",
        "feature_label_matrix_candidate_ready_for_operator_review",
        "ready_for_feature_label_matrix_candidate_operator_review",
    ):
        _expect(candidate.get(field), True, field)
    for field in (
        "feature_label_matrix_selected", "feature_label_matrix_approved",
        "feature_label_matrix_authorized", "feature_label_matrix_created",
        "feature_label_matrix_rows_created", "feature_label_matrix_execution_performed",
        "selection_created", "approval_created", "creation_created", "execution_created",
        "generation_created", "backtest_execution_authorized", "backtest_execution_performed",
        "model_training_authorized", "model_training_performed",
        "metric_computation_authorized", "metric_computation_performed",
        "strategy_scoring_performed", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved",
        "runtime_migration_active", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_candidate",
        "live_provider_transport_enabled_in_candidate",
        "market_data_acquisition_performed_in_candidate", "dataset_generation_performed_in_candidate",
        "canonical_dataset_regenerated_in_candidate", "target_generation_execution_rerun_performed",
        "target_generation_results_review_rerun_performed",
        "signal_or_feature_generation_execution_rerun_performed",
        "signal_or_feature_generation_results_review_rerun_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    ):
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    package = candidate.get("recommended_matrix_package_definition")
    if not isinstance(package, dict) or package.get("package_id") != PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX:
        raise MarketFlowFeatureLabelMatrixCandidateError(
            "recommended matrix package missing"
        )
    expected_planned = {
        "matrix_alignment_keys": ("alignment_key_id", ALIGNMENT_KEY_IDS),
        "feature_side_join_rules": ("feature_side_join_rule_id", FEATURE_SIDE_JOIN_RULE_IDS),
        "target_side_join_rules": ("target_side_join_rule_id", TARGET_SIDE_JOIN_RULE_IDS),
        "matrix_quality_checks": ("quality_check_id", QUALITY_CHECK_IDS),
        "planned_future_outputs": ("output_id", FUTURE_OUTPUT_IDS),
    }
    for field, (id_field, expected_ids) in expected_planned.items():
        rows = candidate.get(field)
        if not isinstance(rows, list) or [row.get(id_field) for row in rows] != expected_ids:
            raise MarketFlowFeatureLabelMatrixCandidateError(f"{field} mismatch")
    if any(row.get("output_status") != "PLANNED_NOT_GENERATED" for row in candidate["planned_future_outputs"]):
        raise MarketFlowFeatureLabelMatrixCandidateError("future output was generated")
    entries = candidate.get("per_ticker_feature_label_matrix_candidate_entries")
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowFeatureLabelMatrixCandidateError("per-ticker candidate entries mismatch")
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop("per_ticker_feature_label_matrix_candidate_digest", None)
        _expect(digest, semantic_digest(payload), f"{row.get('ticker')} candidate digest")
    expected_checklist = _candidate_checklist(candidate)
    _expect(candidate.get("candidate_checklist"), expected_checklist, "candidate_checklist")
    if any(row["status"] != PASS for row in expected_checklist):
        raise MarketFlowFeatureLabelMatrixCandidateError("candidate checklist contains failures")
    _expect(candidate.get("candidate_summary"), _summary(expected_checklist), "candidate_summary")
    digest = candidate.get("marketflow_feature_label_matrix_candidate_v1_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowFeatureLabelMatrixCandidateError("candidate digest missing")
    _expect(digest, marketflow_feature_label_matrix_candidate_v1_digest(candidate), "candidate digest")
    return {
        "status": MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_feature_label_matrix_candidate_v1_digest": digest,
        "recommended_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "total_checks": candidate["candidate_summary"]["total_checks"],
        "passed_checks": candidate["candidate_summary"]["passed_checks"],
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_marketflow_feature_label_matrix_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the candidate-only matrix plan as Markdown."""
    validation = validate_marketflow_feature_label_matrix_candidate_v1(candidate)
    sections = [
        ("Feature-Label Matrix Candidate v1", [
            f"Artifact/status/scope: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}` / `{candidate['candidate_scope']}`.",
            f"Candidate digest: `{validation['marketflow_feature_label_matrix_candidate_v1_digest']}`.",
        ]),
        ("Source Signal or Feature Results Review", [
            f"Ready source review `{EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST}` is bound without rerunning it."
        ]),
        ("Source Target Results Review", [
            f"Ready target review `{EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST}` and target values `{EXPECTED_SOURCE_TARGET_VALUES_DIGEST}` are bound."
        ]),
        ("Bound Evidence", [
            f"Feature values `{EXPECTED_SOURCE_FEATURE_VALUES_DIGEST}` and the complete upstream digest chain are preserved."
        ]),
        ("Dataset and Universe", [
            "`expanded_universe_canonical_dataset_v1`, 11,946 records, ordered twelve-ticker universe; META remains exactly 913 records."
        ]),
        ("Candidate Basis", [
            "155,298 feature rows across 13 groups and 179,190 target rows across 15 profiles define planning counts only."
        ]),
        ("Candidate Philosophy", [
            candidate["candidate_philosophy"], candidate["candidate_primary_question"],
            candidate["candidate_secondary_question"], candidate["candidate_boundary"],
        ]),
        ("Recommended Matrix Package", [
            f"`{PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX}` is recommended for operator review but not selected, approved, or executed."
        ]),
        ("Proposed Matrix Layouts", [
            f"`{row['layout_id']}`: {row['status']}" for row in candidate["matrix_layouts"]
        ]),
        ("Matrix Alignment Keys", [
            ", ".join(f"`{item}`" for item in ALIGNMENT_KEY_IDS)
        ]),
        ("Feature-Side Join Rules", [
            ", ".join(f"`{item}`" for item in FEATURE_SIDE_JOIN_RULE_IDS)
        ]),
        ("Target-Side Join Rules", [
            ", ".join(f"`{item}`" for item in TARGET_SIDE_JOIN_RULE_IDS)
        ]),
        ("Planned Matrix Counts", [
            "179,190 planned rows: 177,090 target-available and 2,100 target-unavailable; 13 feature groups, 15 target profiles, and 11,946 canonical records."
        ]),
        ("Matrix Quality Checks", [
            ", ".join(f"`{item}`" for item in QUALITY_CHECK_IDS)
        ]),
        ("Planned Future Outputs", [
            "Twelve outputs remain `PLANNED_NOT_GENERATED`; no matrix or joined artifact exists."
        ]),
        ("Per-Ticker Candidate Summary", [
            "Each non-META ticker plans 15,045 matrix rows and 13,039 feature rows; META plans 13,695 and 11,869 while preserving its 913-record limitation."
        ]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", [
            "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
        ]),
        ("Checklist Summary", [
            f"{candidate['candidate_summary']['passed_checks']}/{candidate['candidate_summary']['total_checks']} checks pass with zero blockers."
        ]),
        ("Guardrails", [
            "This candidate performs no source rerun, feature-target join, matrix creation, backtest, model training, metric computation, scoring, recommendation, acceptance, runtime, or trading action."
        ]),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_feature_label_matrix_candidate_v1(
    output_dir: str | Path,
) -> dict:
    """Write validated candidate JSON and Markdown to an explicit directory."""
    candidate = build_marketflow_feature_label_matrix_candidate_v1()
    validation = validate_marketflow_feature_label_matrix_candidate_v1(candidate)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_feature_label_matrix_candidate_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowFeatureLabelMatrixCandidateError(
            "feature-label matrix candidate output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(candidate))
    markdown_path.write_text(
        build_marketflow_feature_label_matrix_candidate_markdown_v1(candidate),
        encoding="utf-8",
        newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path).replace("\\", "/"),
        "markdown_path": str(markdown_path).replace("\\", "/"),
    }
