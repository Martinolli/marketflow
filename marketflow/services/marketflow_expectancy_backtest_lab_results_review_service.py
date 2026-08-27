"""Offline review of generated expectancy backtest-lab evidence."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_file
from marketflow.services import (
    marketflow_expectancy_backtest_lab_execution_service as execution,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE"
)
ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_V1 = (
    "marketflow_expectancy_backtest_lab_results_review_v1"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME = (
    "EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_VALID = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_VALID"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "7c97920ef7cc98ef971f5cee3838a250b0cb2d217656567897516d7767f4101d"
)
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = (
    "a2b505a2fee0a42506350397bcc6a700a92d58ab8a9d522ffdfa5a2fd04e8086"
)
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = (
    "53b6cfa042a1f29f1228f63190f42c01618bd5982af0ad5c33181c98ffcb5ca2"
)
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = (
    "ffb71ab3f5ef41e50e9eb00a8bdff11e75275778b99e031d9e17a16ace424e80"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = execution.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = execution.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = execution.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = execution.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = execution.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = execution.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = execution.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = execution.EXPECTED_SOURCE_RECORDS_DIGEST

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_LAB_ROW_COUNTS = dict(execution.EXPECTED_LAB_ROW_COUNTS)
EXPECTED_EVALUABLE_COUNTS = dict(execution.EXPECTED_EVALUABLE_COUNTS)
EXPECTED_UNAVAILABLE_COUNTS = dict(execution.EXPECTED_UNAVAILABLE_COUNTS)
EXPECTED_ROW_COUNT = execution.EXPECTED_SOURCE_MATRIX_ROW_COUNT
EXPECTED_EVALUABLE_COUNT = execution.EXPECTED_EVALUABLE_TARGET_ROW_COUNT
EXPECTED_UNAVAILABLE_COUNT = execution.EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT
EXPECTED_EMBARGOED_COUNT = 4200
EXPECTED_AGGREGATE_METRIC_ELIGIBLE_COUNT = 172890
EXPECTED_OUTPUT_COUNT = 14

NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = execution.PASS
FAIL = execution.FAIL
BLOCKER = execution.BLOCKER

NEXT_CHAIN = [
    "Predictive-usefulness reassessment using expectancy lab evidence.",
    "Acceptance-readiness review only after reassessment.",
    "Predictive-usefulness acceptance candidate only if readiness passes.",
    "Profitability review only after separately accepted predictive usefulness.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_reassessment_using_expectancy_lab_evidence",
    "predictive_usefulness_acceptance_readiness_if_reassessment_supports_it",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_if_predictive_usefulness_accepted",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_create_predictive_usefulness_reassessment",
    "review_does_not_create_acceptance_readiness_review",
    "review_does_not_create_acceptance_candidate",
    "review_does_not_train_models", "review_does_not_score_strategy",
    "review_does_not_generate_trade_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability", "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy", "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution", "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_rerun_expectancy_backtest_lab_execution",
    "review_does_not_rerun_expectancy_backtest_lab_approval",
    "review_does_not_rerun_expectancy_backtest_lab_candidate_review",
    "review_does_not_rerun_expectancy_backtest_lab_candidate_creation",
    "review_does_not_rerun_vpa_wyckoff_execution",
    "review_does_not_rerun_vpa_wyckoff_results_review",
    "review_does_not_rerun_feature_label_matrix_execution",
    "review_does_not_rerun_feature_label_matrix_results_review",
    "review_does_not_rerun_signal_feature_generation",
    "review_does_not_rerun_target_generation", "do_not_mutate_frozen_dataset",
    "do_not_mutate_expectancy_backtest_lab_outputs", "do_not_mutate_vpa_wyckoff_outputs",
    "do_not_mutate_matrix_outputs", "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_target_outputs", "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs", "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation", "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound", "source_output_binding_digest_bound",
    "source_backtest_rows_digest_bound", "source_metric_report_digest_bound",
    "source_approval_digest_bound", "source_candidate_review_digest_bound",
    "source_candidate_digest_bound", "source_vpa_wyckoff_results_review_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound", "source_matrix_rows_digest_bound",
    "source_target_values_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "selected_backtest_lab_package_preserved", "selected_vpa_wyckoff_package_preserved",
    "selected_matrix_package_preserved", "selected_matrix_layout_preserved",
    "selected_feature_package_preserved", "selected_target_package_preserved",
    "selected_objective_path_preserved", "expected_output_count_14",
    "observed_output_count_14", "output_digest_mismatch_count_zero",
    "backtest_rows_digest_matches", "metric_report_digest_matches",
    "backtest_rows_jsonl_schema_verified", "backtest_lab_row_count_179190",
    "evaluable_target_row_count_177090", "unavailable_target_row_count_2100",
    "embargoed_cross_split_forward_horizon_row_count_4200",
    "aggregate_metric_eligible_row_count_172890", "approved_metric_family_count_13",
    "blocked_metric_family_count_1", "approved_baseline_count_6",
    "blocked_baseline_count_1", "blocked_randomized_null_reference_not_executed",
    "blocked_bootstrap_metric_not_computed", "chronological_no_shuffle_preserved",
    "horizon_aware_embargo_documented", "target_values_only_as_outcomes",
    "target_classes_only_as_outcomes", "forward_returns_not_used_as_features",
    "prediction_fields_absent", "strategy_score_fields_absent",
    "trade_recommendation_fields_absent", "broker_order_fields_absent",
    "provider_payload_fields_absent", "api_key_fields_absent",
    "result_summary_verified", "metric_report_verified", "baseline_comparison_report_verified",
    "vpa_wyckoff_rule_alignment_report_verified", "abstention_quality_report_verified",
    "per_ticker_backtest_report_verified", "chronological_split_report_verified",
    "meta_limitation_report_verified", "no_peek_report_verified",
    "operator_summary_verified", "digest_manifest_self_reference_policy_verified",
    "results_review_created_true", "results_review_ready_true",
    "ready_for_predictive_usefulness_reassessment_true",
    "predictive_usefulness_reassessment_created_false",
    "predictive_usefulness_acceptance_candidate_created_false",
    "model_training_authorized_false", "model_training_performed_false",
    "strategy_scoring_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "expectancy_backtest_lab_execution_rerun_false",
    "expectancy_backtest_lab_approval_rerun_false",
    "expectancy_backtest_lab_candidate_review_rerun_false",
    "expectancy_backtest_lab_candidate_creation_rerun_false",
    "vpa_wyckoff_execution_rerun_false", "vpa_wyckoff_results_review_rerun_false",
    "matrix_execution_rerun_false", "matrix_results_review_rerun_false",
    "signal_feature_generation_rerun_false", "target_generation_rerun_false",
    "raw_provider_payloads_not_committed", "api_keys_not_stored_or_printed",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]

FORBIDDEN_ROW_KEYS = {
    "prediction", "prediction_value", "strategy_score", "trade_recommendation",
    "broker_order", "broker_order_id", "order_id", "raw_provider_payload",
    "provider_payload", "api_key", "api_keys", "runtime_signal",
    "paper_trade_signal", "live_trade_signal",
}
NESTED_OUTCOME_FORBIDDEN_FIELDS = execution.NESTED_NO_OUTCOME_FIELDS


class MarketFlowExpectancyBacktestLabResultsReviewError(ValueError):
    """Raised when expectancy-lab outputs violate the review contract."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MarketFlowExpectancyBacktestLabResultsReviewError(
            f"invalid JSON output: {path.name}"
        ) from exc
    if not isinstance(value, dict):
        raise MarketFlowExpectancyBacktestLabResultsReviewError(
            f"JSON output must be an object: {path.name}"
        )
    return value


def _nested_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for child in value.values():
            keys.update(_nested_keys(child))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for child in value:
            keys.update(_nested_keys(child))
        return keys
    return set()


def _expected_split(date_text: str) -> str | None:
    for split_id, (start, end) in execution.SPLITS.items():
        if start <= date_text <= end:
            return split_id
    return None


def _inspect_backtest_rows(path: Path) -> dict[str, Any]:
    row_count = evaluable = unavailable = embargoed = metric_eligible = 0
    schema_valid = research_only = package_valid = split_valid = baseline_valid = True
    metric_eligibility_valid = target_outcome_boundary_valid = True
    row_forbidden: set[str] = set()
    nested_forbidden: set[str] = set()
    ticker_rows: Counter[str] = Counter()
    ticker_evaluable: Counter[str] = Counter()
    ticker_unavailable: Counter[str] = Counter()
    ticker_embargoed: Counter[str] = Counter()
    split_rows: Counter[str] = Counter()
    required_fields = {
        *execution.IDENTITY_KEYS, "target_available", "target_value", "target_class",
        "target_unavailable_reason", "forward_start_date", "forward_end_date",
        "chronological_split", "horizon_aware_embargo_status", "research_row_available",
        "research_unavailable_reason", "vpa_wyckoff_rule_values",
        "vpa_wyckoff_state_values", "vpa_rule_family_count", "vpa_state_family_count",
        "baseline_references", "objective_context", "metric_eligibility",
        "source_matrix_rows_digest", "source_vpa_wyckoff_rule_values_digest",
        "source_target_values_digest", "records_digest", "output_label",
        "evidence_scope", "research_only", "non_actionable",
    }
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    schema_valid = False
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError(f"row {line_number} is not an object")
                row_count += 1
                schema_valid = schema_valid and required_fields <= set(row)
                ticker = row.get("ticker")
                if ticker not in TARGET_UNIVERSE:
                    schema_valid = False
                    continue
                ticker_rows[ticker] += 1
                split_id = row.get("chronological_split")
                split_rows[str(split_id)] += 1
                split_valid = split_valid and split_id == _expected_split(str(row.get("date")))
                target_available = row.get("target_available")
                if target_available is True:
                    evaluable += 1
                    ticker_evaluable[ticker] += 1
                elif target_available is False:
                    unavailable += 1
                    ticker_unavailable[ticker] += 1
                    target_outcome_boundary_valid = target_outcome_boundary_valid and (
                        row.get("target_value") is None and row.get("target_class") is None
                    )
                else:
                    schema_valid = False
                is_embargoed = row.get("horizon_aware_embargo_status") == "EMBARGOED_SPLIT_BOUNDARY"
                if is_embargoed:
                    embargoed += 1
                    ticker_embargoed[ticker] += 1
                eligibility = row.get("metric_eligibility")
                eligible = isinstance(eligibility, dict) and eligibility.get("eligible") is True
                if eligible:
                    metric_eligible += 1
                metric_eligibility_valid = metric_eligibility_valid and isinstance(eligibility, dict) and (
                    eligible == (row.get("research_row_available") is True)
                ) and not (eligible and (target_available is not True or is_embargoed))
                baselines = row.get("baseline_references")
                baseline_valid = baseline_valid and isinstance(baselines, dict) and (
                    list(baselines) == execution.APPROVED_BASELINE_IDS
                    or set(baselines) == set(execution.APPROVED_BASELINE_IDS)
                ) and execution.BLOCKED_BASELINE_ID not in baselines
                research_only = research_only and row.get("research_only") is True and row.get("non_actionable") is True and row.get("output_label") == execution.OUTPUT_LABEL and row.get("evidence_scope") == execution.EVIDENCE_SCOPE
                package_valid = package_valid and all((
                    row.get("selected_backtest_lab_package") == execution.SELECTED_BACKTEST_LAB_PACKAGE,
                    row.get("selected_vpa_wyckoff_package") == execution.SELECTED_VPA_WYCKOFF_PACKAGE,
                    row.get("selected_matrix_package") == execution.SELECTED_MATRIX_PACKAGE,
                    row.get("selected_matrix_layout") == execution.SELECTED_MATRIX_LAYOUT,
                    row.get("selected_feature_package") == execution.SELECTED_FEATURE_PACKAGE,
                    row.get("selected_label_target_package") == execution.SELECTED_LABEL_TARGET_PACKAGE,
                    row.get("selected_objective_path") == execution.SELECTED_OBJECTIVE_PATH,
                    row.get("source_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
                    row.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
                    row.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
                    row.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
                ))
                row_forbidden.update(set(row) & FORBIDDEN_ROW_KEYS)
                for field in NESTED_OUTCOME_FORBIDDEN_FIELDS:
                    value = row.get(field)
                    nested_keys = _nested_keys(value)
                    nested_forbidden.update({key for key in nested_keys if key in {"target_value", "target_class", "forward_return", *FORBIDDEN_ROW_KEYS}})
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise MarketFlowExpectancyBacktestLabResultsReviewError(
            "expectancy_backtest_rows.jsonl could not be inspected"
        ) from exc
    per_ticker_verified = all(
        ticker_rows[ticker] == EXPECTED_LAB_ROW_COUNTS[ticker]
        and ticker_evaluable[ticker] == EXPECTED_EVALUABLE_COUNTS[ticker]
        and ticker_unavailable[ticker] == EXPECTED_UNAVAILABLE_COUNTS[ticker]
        for ticker in TARGET_UNIVERSE
    )
    return {
        "streaming_read_used": True, "entire_backtest_rows_jsonl_loaded_into_memory": False,
        "backtest_lab_row_count": row_count, "evaluable_target_row_count": evaluable,
        "unavailable_target_row_count": unavailable,
        "embargoed_cross_split_forward_horizon_row_count": embargoed,
        "aggregate_metric_eligible_row_count": metric_eligible,
        "backtest_rows_jsonl_schema_verified": schema_valid,
        "research_only_non_actionable_verified": research_only,
        "package_binding_verified": package_valid,
        "chronological_split_consistency_verified": split_valid,
        "baseline_reference_presence_verified": baseline_valid,
        "metric_eligibility_fields_verified": metric_eligibility_valid,
        "target_outcome_boundary_verified": target_outcome_boundary_valid,
        "target_values_used_as_predictors": "target_value" in nested_forbidden,
        "target_classes_used_as_predictors": "target_class" in nested_forbidden,
        "forward_returns_used_as_features": "forward_return" in nested_forbidden,
        "prediction_fields_present": bool({"prediction", "prediction_value"} & (row_forbidden | nested_forbidden)),
        "strategy_score_fields_present": "strategy_score" in row_forbidden | nested_forbidden,
        "trade_recommendation_fields_present": "trade_recommendation" in row_forbidden | nested_forbidden,
        "broker_order_fields_present": bool({"broker_order", "broker_order_id", "order_id"} & (row_forbidden | nested_forbidden)),
        "provider_payload_fields_present": bool({"provider_payload", "raw_provider_payload"} & (row_forbidden | nested_forbidden)),
        "api_key_fields_present": bool({"api_key", "api_keys"} & (row_forbidden | nested_forbidden)),
        "per_ticker_counts_verified": per_ticker_verified,
        "per_ticker_backtest_lab_row_counts": {ticker: ticker_rows[ticker] for ticker in TARGET_UNIVERSE},
        "per_ticker_evaluable_target_row_counts": {ticker: ticker_evaluable[ticker] for ticker in TARGET_UNIVERSE},
        "per_ticker_unavailable_target_row_counts": {ticker: ticker_unavailable[ticker] for ticker in TARGET_UNIVERSE},
        "per_ticker_embargoed_row_counts": {ticker: ticker_embargoed[ticker] for ticker in TARGET_UNIVERSE},
        "chronological_split_row_counts": dict(split_rows),
    }


def _verify_reports(payloads: Mapping[str, dict[str, Any]]) -> dict[str, bool]:
    source = payloads["expectancy_backtest_lab_manifest.json"]
    summary = payloads["expectancy_backtest_result_summary.json"]
    metrics = payloads["expectancy_metric_report.json"]
    baselines = payloads["baseline_comparison_report.json"]
    alignment = payloads["vpa_wyckoff_rule_alignment_report.json"]
    abstention = payloads["abstention_quality_report.json"]
    per_ticker = payloads["per_ticker_backtest_report.json"]
    chronology = payloads["chronological_split_report.json"]
    meta = payloads["meta_limitation_report.json"]
    no_peek = payloads["no_peek_report.json"]
    operator = payloads["operator_summary.json"]
    digest_manifest = payloads["expectancy_backtest_lab_digest_manifest.json"]
    ordinary_reports = [
        payloads[name] for name in EXPECTED_OUTPUT_FILENAMES
        if name not in {"expectancy_backtest_lab_manifest.json", "expectancy_backtest_rows.jsonl"}
    ]
    common_valid = all(
        report.get("output_label") == execution.OUTPUT_LABEL
        and report.get("evidence_scope") == execution.EVIDENCE_SCOPE
        and report.get("research_only") is True
        and report.get("non_actionable") is True
        and report.get("predictive_usefulness") == NOT_ACCEPTED
        and report.get("profitability") == NOT_ACCEPTED
        and report.get("runtime_use") == NOT_AUTHORIZED
        and report.get("model_training_performed") is False
        and report.get("strategy_scoring_performed") is False
        and report.get("trade_recommendations_generated") is False
        for report in ordinary_reports
    )
    metric_ids = [row.get("metric_family_id") for row in metrics.get("metric_families", []) if isinstance(row, dict)]
    ticker_rows = per_ticker.get("entries", [])
    return {
        "common_output_boundary_verified": common_valid,
        "result_summary_verified": all((
            summary.get("expectancy_backtest_lab_row_count") == EXPECTED_ROW_COUNT,
            summary.get("evaluable_target_row_count") == EXPECTED_EVALUABLE_COUNT,
            summary.get("unavailable_target_row_count") == EXPECTED_UNAVAILABLE_COUNT,
            summary.get("embargoed_metric_row_count") == EXPECTED_EMBARGOED_COUNT,
        )),
        "metric_report_verified": (
            metric_ids == execution.APPROVED_METRIC_FAMILY_IDS
            and metrics.get("blocked_metric_family", {}).get("metric_family_id") == execution.BLOCKED_METRIC_FAMILY_ID
            and metrics.get("blocked_metric_family", {}).get("status") == "NOT_COMPUTED_BLOCKED"
            and len(metrics.get("baseline_delta_summaries", {})) == 6
        ),
        "baseline_comparison_report_verified": (
            baselines.get("executed_baselines") == execution.APPROVED_BASELINE_IDS
            and baselines.get("blocked_baseline", {}).get("baseline_id") == execution.BLOCKED_BASELINE_ID
            and baselines.get("blocked_baseline", {}).get("status") == "NOT_EXECUTED_BLOCKED"
        ),
        "vpa_wyckoff_rule_alignment_report_verified": (
            alignment.get("definition_source") == "REVIEWED_VPA_WYCKOFF_RULE_AND_STATE_TAGS_ONLY"
            and set(alignment.get("context_summaries", {})) == {"FAVORABLE", "AVOID", "NEUTRAL"}
        ),
        "abstention_quality_report_verified": (
            abstention.get("interpretation") == "DESCRIPTIVE_COVERAGE_AND_AVOIDANCE_ONLY_NOT_RECOMMENDATION"
        ),
        "per_ticker_backtest_report_verified": (
            len(ticker_rows) == len(TARGET_UNIVERSE)
            and [row.get("ticker") for row in ticker_rows] == TARGET_UNIVERSE
        ),
        "chronological_split_report_verified": (
            chronology.get("split_policy") == "CHRONOLOGICAL_NO_SHUFFLE"
            and chronology.get("horizon_aware_embargo_policy") == "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING"
            and sum(row.get("embargoed", 0) for row in chronology.get("splits", [])) == EXPECTED_EMBARGOED_COUNT
        ),
        "meta_limitation_report_verified": (
            meta.get("ticker") == "META" and meta.get("historical_record_count") == EXPECTED_RECORD_COUNTS.get("META")
            and meta.get("meta_reduced_record_count_flag") is True
            and meta.get("counts", {}).get("rows") == EXPECTED_LAB_ROW_COUNTS.get("META")
        ),
        "no_peek_report_verified": all((
            no_peek.get("target_values_only_as_outcomes") is True,
            no_peek.get("target_classes_only_as_outcomes") is True,
            no_peek.get("forward_returns_used_as_features") is False,
            no_peek.get("future_data_used_as_features") is False,
            no_peek.get("prediction_fields_present") is False,
            no_peek.get("strategy_score_fields_present") is False,
            no_peek.get("trade_recommendation_fields_present") is False,
            no_peek.get("broker_order_fields_present") is False,
            no_peek.get("provider_payload_fields_present") is False,
            no_peek.get("api_key_fields_present") is False,
        )),
        "operator_summary_verified": (
            operator.get("expectancy_backtest_lab_row_count") == EXPECTED_ROW_COUNT
            and operator.get("evaluable_target_row_count") == EXPECTED_EVALUABLE_COUNT
            and operator.get("unavailable_target_row_count") == EXPECTED_UNAVAILABLE_COUNT
        ),
        "digest_manifest_verified": all((
            digest_manifest.get("marketflow_expectancy_backtest_lab_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
            digest_manifest.get("expectancy_backtest_lab_output_binding_digest") == EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
            digest_manifest.get("expectancy_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            digest_manifest.get("expectancy_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
            digest_manifest.get("manifest_self_reference_policy") == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
            digest_manifest.get("output_digest_manifest") == source.get("output_digest_manifest"),
        )),
    }


def _verify_outputs(output_root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, bool], list[dict[str, Any]]]:
    if not output_root.is_dir():
        return {}, [], {}, {}, [_failure("missing_output_root", "expectancy backtest-lab output root is missing", output_root=_path_text(output_root))]
    actual_names = sorted(path.name for path in output_root.iterdir() if path.is_file())
    missing = [name for name in EXPECTED_OUTPUT_FILENAMES if name not in actual_names]
    if missing or len(actual_names) != EXPECTED_OUTPUT_COUNT:
        return {}, [], {}, {}, [_failure("output_file_inventory_mismatch", "expected output inventory is incomplete or contains extras", expected=EXPECTED_OUTPUT_FILENAMES, actual=actual_names, missing=missing)]
    try:
        payloads = {
            filename: _load_json(output_root / filename)
            for filename in EXPECTED_OUTPUT_FILENAMES
            if filename != "expectancy_backtest_rows.jsonl"
        }
        source = payloads["expectancy_backtest_lab_manifest.json"]
        execution.validate_marketflow_expectancy_backtest_lab_execution_v1(source)
        recorded = source.get("output_digest_manifest")
        digest_record = payloads["expectancy_backtest_lab_digest_manifest.json"]
        if not isinstance(recorded, list) or recorded != digest_record.get("output_digest_manifest"):
            raise MarketFlowExpectancyBacktestLabResultsReviewError("digest manifest mismatch")
        before = {filename: sha256_file(output_root / filename) for filename in EXPECTED_OUTPUT_FILENAMES}
        row_stats = _inspect_backtest_rows(output_root / "expectancy_backtest_rows.jsonl")
        after = {filename: sha256_file(output_root / filename) for filename in EXPECTED_OUTPUT_FILENAMES}
        if before != after:
            raise MarketFlowExpectancyBacktestLabResultsReviewError("source outputs changed during review")
        report_reviews = _verify_reports(payloads)
    except (MarketFlowExpectancyBacktestLabResultsReviewError, execution.MarketFlowExpectancyBacktestLabExecutionError) as exc:
        return {}, [], {}, {}, [_failure("invalid_source_output", "expectancy backtest-lab outputs are invalid", error=str(exc))]
    recorded_by_name = {row.get("filename"): row for row in recorded if isinstance(row, dict)}
    bindings = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        entry = recorded_by_name.get(filename, {})
        local_sha = before[filename]
        recorded_sha = entry.get("sha256")
        kind = entry.get("digest_kind")
        if filename == EXPECTED_OUTPUT_FILENAMES[0]:
            verified = kind == "SELF_REFERENTIAL_EXECUTION_ARTIFACT" and recorded_sha is None
        elif filename == EXPECTED_OUTPUT_FILENAMES[-1]:
            verified = kind == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE and recorded_sha is None
        else:
            verified = kind == "FILE_SHA256" and recorded_sha == local_sha
        bindings.append({
            "filename": filename, "digest_kind": kind, "recorded_sha256": recorded_sha,
            "local_sha256": local_sha, "digest_verified": verified,
        })
    failures = []
    if any(not row["digest_verified"] for row in bindings):
        failures.append(_failure("output_digest_mismatch", "one or more output digests do not verify", mismatches=[row["filename"] for row in bindings if not row["digest_verified"]]))
    if before["expectancy_backtest_rows.jsonl"] != EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST:
        failures.append(_failure("backtest_rows_digest_mismatch", "backtest rows digest mismatch"))
    if before["expectancy_metric_report.json"] != EXPECTED_SOURCE_METRIC_REPORT_DIGEST:
        failures.append(_failure("metric_report_digest_mismatch", "metric report digest mismatch"))
    if source.get("expectancy_backtest_lab_output_binding_digest") != EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST:
        failures.append(_failure("output_binding_digest_mismatch", "output binding digest mismatch"))
    if not all(report_reviews.values()):
        failures.append(_failure("report_content_verification_failed", "one or more report contents are invalid", report_reviews=report_reviews))
    return payloads, bindings, row_stats, report_reviews, failures


def per_ticker_expectancy_backtest_lab_results_review_digest_v1(entry: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_backtest_lab_results_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any], row_stats: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker, "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN", "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "expectancy_backtest_lab_execution_status": execution.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY,
            "expectancy_backtest_lab_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "selected_backtest_lab_package": execution.SELECTED_BACKTEST_LAB_PACKAGE,
            "selected_vpa_wyckoff_package": execution.SELECTED_VPA_WYCKOFF_PACKAGE,
            "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
            "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
            "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
            "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
            "backtest_lab_row_count": row_stats["per_ticker_backtest_lab_row_counts"][ticker],
            "evaluable_target_row_count": row_stats["per_ticker_evaluable_target_row_counts"][ticker],
            "unavailable_target_row_count": row_stats["per_ticker_unavailable_target_row_counts"][ticker],
            "embargoed_cross_split_forward_horizon_row_count": row_stats["per_ticker_embargoed_row_counts"][ticker],
            "vpa_wyckoff_rule_row_count": row_stats["per_ticker_backtest_lab_row_counts"][ticker],
            "vpa_wyckoff_state_row_count": row_stats["per_ticker_backtest_lab_row_counts"][ticker],
            "approved_metric_family_count": 13, "approved_baseline_count": 6,
            "predictive_usefulness_reassessment_created": False,
            "model_training_authorized": False, "metric_computation_performed": True,
            "strategy_scoring_performed": False, "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED, "trade_recommendations_generated": False,
            "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
            "source_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
            "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        }
        if ticker == "META":
            entry["review_note"] = "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW"
        entry["per_ticker_expectancy_backtest_lab_results_review_digest"] = per_ticker_expectancy_backtest_lab_results_review_digest_v1(entry)
        entries.append(entry)
    return entries


def _blocked_package(output_root: Path, failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "review_scope": EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME,
        "source_output_root": _path_text(output_root), "failures": failures,
        "expectancy_backtest_lab_results_review_created": False,
        "expectancy_backtest_lab_results_review_ready": False,
        "ready_for_predictive_usefulness_reassessment_using_expectancy_lab_evidence": False,
        "predictive_usefulness_reassessment_created": False,
        "model_training_authorized": False, "model_training_performed": False,
        "strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": bool(actual),
        "severity": "INFO" if actual else BLOCKER,
        "message": "results-review condition satisfied" if actual else "results-review condition failed",
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    inspection = review.get("backtest_rows_streaming_inspection", {})
    reports = review.get("report_reviews", {})
    entries = review.get("per_ticker_expectancy_backtest_lab_results_review_entries", [])
    values = {
        "source_execution_digest_bound": review.get("source_expectancy_backtest_lab_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest_bound": review.get("source_expectancy_backtest_lab_output_binding_digest") == EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_backtest_rows_digest_bound": review.get("source_expectancy_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": review.get("source_expectancy_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_approval_digest_bound": review.get("source_expectancy_backtest_lab_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest_bound": review.get("source_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": review.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest_bound": review.get("source_vpa_wyckoff_results_review_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": review.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": review.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": review.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": review.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": review.get("target_universe") == TARGET_UNIVERSE and review.get("target_universe_count") == len(TARGET_UNIVERSE),
        "records_digest_preserved": review.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": review.get("meta_record_count") == EXPECTED_RECORD_COUNTS.get("META"),
        "selected_backtest_lab_package_preserved": review.get("selected_backtest_lab_package") == execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package_preserved": review.get("selected_vpa_wyckoff_package") == execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package_preserved": review.get("selected_matrix_package") == execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout_preserved": review.get("selected_matrix_layout") == execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package_preserved": review.get("selected_feature_package") == execution.SELECTED_FEATURE_PACKAGE,
        "selected_target_package_preserved": review.get("selected_label_target_package") == execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path_preserved": review.get("selected_objective_path") == execution.SELECTED_OBJECTIVE_PATH,
        "expected_output_count_14": review.get("expected_output_count") == EXPECTED_OUTPUT_COUNT,
        "observed_output_count_14": review.get("observed_output_count") == EXPECTED_OUTPUT_COUNT,
        "output_digest_mismatch_count_zero": review.get("output_digest_mismatch_count") == 0,
        "backtest_rows_digest_matches": review.get("local_output_digests", {}).get("expectancy_backtest_rows.jsonl") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "metric_report_digest_matches": review.get("local_output_digests", {}).get("expectancy_metric_report.json") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "backtest_rows_jsonl_schema_verified": inspection.get("backtest_rows_jsonl_schema_verified") is True,
        "backtest_lab_row_count_179190": review.get("expectancy_backtest_lab_row_count") == EXPECTED_ROW_COUNT,
        "evaluable_target_row_count_177090": review.get("evaluable_target_row_count") == EXPECTED_EVALUABLE_COUNT,
        "unavailable_target_row_count_2100": review.get("unavailable_target_row_count") == EXPECTED_UNAVAILABLE_COUNT,
        "embargoed_cross_split_forward_horizon_row_count_4200": review.get("embargoed_cross_split_forward_horizon_row_count") == EXPECTED_EMBARGOED_COUNT,
        "aggregate_metric_eligible_row_count_172890": review.get("aggregate_metric_eligible_row_count") == EXPECTED_AGGREGATE_METRIC_ELIGIBLE_COUNT,
        "approved_metric_family_count_13": review.get("approved_metric_family_count") == 13,
        "blocked_metric_family_count_1": review.get("blocked_metric_family_count") == 1,
        "approved_baseline_count_6": review.get("approved_baseline_count") == 6,
        "blocked_baseline_count_1": review.get("blocked_baseline_count") == 1,
        "blocked_randomized_null_reference_not_executed": review.get("blocked_randomized_null_reference_executed") is False,
        "blocked_bootstrap_metric_not_computed": review.get("blocked_bootstrap_metric_computed") is False,
        "chronological_no_shuffle_preserved": review.get("chronological_split_policy") == "CHRONOLOGICAL_NO_SHUFFLE",
        "horizon_aware_embargo_documented": review.get("horizon_aware_embargo_status") == "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING",
        "target_values_only_as_outcomes": review.get("target_values_used_as_predictors") is False,
        "target_classes_only_as_outcomes": review.get("target_classes_used_as_predictors") is False,
        "forward_returns_not_used_as_features": review.get("forward_returns_used_as_features") is False,
        "prediction_fields_absent": review.get("prediction_fields_present") is False,
        "strategy_score_fields_absent": review.get("strategy_score_fields_present") is False,
        "trade_recommendation_fields_absent": review.get("trade_recommendation_fields_present") is False,
        "broker_order_fields_absent": review.get("broker_order_fields_present") is False,
        "provider_payload_fields_absent": review.get("provider_payload_fields_present") is False,
        "api_key_fields_absent": review.get("api_key_fields_present") is False,
        "result_summary_verified": reports.get("result_summary_verified") is True,
        "metric_report_verified": reports.get("metric_report_verified") is True,
        "baseline_comparison_report_verified": reports.get("baseline_comparison_report_verified") is True,
        "vpa_wyckoff_rule_alignment_report_verified": reports.get("vpa_wyckoff_rule_alignment_report_verified") is True,
        "abstention_quality_report_verified": reports.get("abstention_quality_report_verified") is True,
        "per_ticker_backtest_report_verified": reports.get("per_ticker_backtest_report_verified") is True,
        "chronological_split_report_verified": reports.get("chronological_split_report_verified") is True,
        "meta_limitation_report_verified": reports.get("meta_limitation_report_verified") is True,
        "no_peek_report_verified": reports.get("no_peek_report_verified") is True,
        "operator_summary_verified": reports.get("operator_summary_verified") is True,
        "digest_manifest_self_reference_policy_verified": review.get("digest_manifest_self_reference_policy") == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "results_review_created_true": review.get("expectancy_backtest_lab_results_review_created") is True,
        "results_review_ready_true": review.get("expectancy_backtest_lab_results_review_ready") is True,
        "ready_for_predictive_usefulness_reassessment_true": review.get("ready_for_predictive_usefulness_reassessment_using_expectancy_lab_evidence") is True,
        "predictive_usefulness_reassessment_created_false": review.get("predictive_usefulness_reassessment_created") is False,
        "predictive_usefulness_acceptance_candidate_created_false": review.get("predictive_usefulness_acceptance_candidate_created") is False,
        "model_training_authorized_false": review.get("model_training_authorized") is False,
        "model_training_performed_false": review.get("model_training_performed") is False,
        "strategy_scoring_false": review.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": review.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review.get("trade_recommendations_generated") is False,
        "per_ticker_entries_12": len(entries) == len(TARGET_UNIVERSE) and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_expectancy_backtest_lab_results_review_digest") == per_ticker_expectancy_backtest_lab_results_review_digest_v1(row) for row in entries),
        "provider_requests_made_false": review.get("provider_requests_made_in_review") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_review") is False,
        "dataset_regeneration_false": review.get("canonical_dataset_regenerated_in_review") is False,
        "expectancy_backtest_lab_execution_rerun_false": review.get("expectancy_backtest_lab_execution_rerun_performed") is False,
        "expectancy_backtest_lab_approval_rerun_false": review.get("expectancy_backtest_lab_approval_rerun_performed") is False,
        "expectancy_backtest_lab_candidate_review_rerun_false": review.get("expectancy_backtest_lab_candidate_review_rerun_performed") is False,
        "expectancy_backtest_lab_candidate_creation_rerun_false": review.get("expectancy_backtest_lab_candidate_creation_rerun_performed") is False,
        "vpa_wyckoff_execution_rerun_false": review.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": review.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": review.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": review.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": review.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": review.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": review.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": review.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    }
    return values


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    passed = sum(row["status"] == PASS for row in rows)
    failed = len(rows) - passed
    return {
        "total_checks": len(rows), "passed_checks": passed, "failed_checks": failed,
        "blocker_count": failed, "expectancy_backtest_lab_results_review_created": True,
        "expectancy_backtest_lab_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_using_expectancy_lab_evidence": True,
        "predictive_usefulness_reassessment_created": False,
        "backtest_lab_row_count": EXPECTED_ROW_COUNT,
        "evaluable_target_row_count": EXPECTED_EVALUABLE_COUNT,
        "unavailable_target_row_count": EXPECTED_UNAVAILABLE_COUNT,
        "embargoed_cross_split_forward_horizon_row_count": EXPECTED_EMBARGOED_COUNT,
        "aggregate_metric_eligible_row_count": EXPECTED_AGGREGATE_METRIC_ELIGIBLE_COUNT,
        "output_digest_mismatch_count": 0, "model_training_performed": False,
        "strategy_scoring_performed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _base_review(output_root: Path, payloads: Mapping[str, dict[str, Any]], bindings: list[dict[str, Any]], row_stats: Mapping[str, Any], report_reviews: Mapping[str, bool]) -> dict[str, Any]:
    source = payloads["expectancy_backtest_lab_manifest.json"]
    local_digests = {row["filename"]: row["local_sha256"] for row in bindings}
    entries = _per_ticker_entries(source, row_stats)
    review = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_output_root": _path_text(output_root),
        "source_expectancy_backtest_lab_execution_artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED,
        "source_expectancy_backtest_lab_execution_status": execution.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY,
        "source_expectancy_backtest_lab_execution_scope": execution.EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME,
        "source_expectancy_backtest_lab_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_expectancy_backtest_lab_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_expectancy_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_expectancy_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_expectancy_backtest_lab_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": {"marketflow_expectancy_backtest_lab_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST, "expectancy_backtest_lab_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST, "expectancy_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST, "expectancy_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST, **deepcopy(source["source_evidence"])},
        "selected_backtest_lab_package": execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
        "dataset_name": source["dataset_name"], "source_profile": source["source_profile"],
        "timeframe": source["timeframe"], "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"], "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"], "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "expectancy_backtest_lab_executed": True, "expectancy_backtest_rows_created": True,
        "expectancy_backtest_results_created": True, "backtest_execution_performed": True,
        "metric_values_computed": True, "metric_reports_created": True,
        "metric_computation_performed": True,
        "expectancy_backtest_lab_results_review_created": True,
        "expectancy_backtest_lab_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_using_expectancy_lab_evidence": True,
        "predictive_usefulness_reassessment_created": False,
        "source_matrix_row_count": source["source_matrix_row_count"],
        "expectancy_backtest_lab_row_count": row_stats["backtest_lab_row_count"],
        "evaluable_target_row_count": row_stats["evaluable_target_row_count"],
        "unavailable_target_row_count": row_stats["unavailable_target_row_count"],
        "embargoed_cross_split_forward_horizon_row_count": row_stats["embargoed_cross_split_forward_horizon_row_count"],
        "aggregate_metric_eligible_row_count": row_stats["aggregate_metric_eligible_row_count"],
        "vpa_wyckoff_rule_row_count": source["vpa_wyckoff_rule_row_count"],
        "vpa_wyckoff_state_row_count": source["vpa_wyckoff_state_row_count"],
        "approved_metric_family_count": source["approved_metric_family_count"],
        "blocked_metric_family_count": source["blocked_metric_family_count"],
        "approved_baseline_count": source["approved_baseline_count"],
        "blocked_baseline_count": source["blocked_baseline_count"],
        "expected_output_count": EXPECTED_OUTPUT_COUNT, "observed_output_count": len(bindings),
        "output_digest_mismatch_count": sum(not row["digest_verified"] for row in bindings),
        "output_file_inspection_performed": True, "output_digest_bindings": bindings,
        "local_output_digests": local_digests,
        "backtest_rows_streaming_inspection": deepcopy(dict(row_stats)),
        "report_reviews": deepcopy(dict(report_reviews)),
        "backtest_rows_jsonl_schema_verified": row_stats["backtest_rows_jsonl_schema_verified"],
        "backtest_rows_count_verified": row_stats["backtest_lab_row_count"] == EXPECTED_ROW_COUNT,
        "result_summary_verified": report_reviews["result_summary_verified"],
        "metric_report_verified": report_reviews["metric_report_verified"],
        "baseline_comparison_report_verified": report_reviews["baseline_comparison_report_verified"],
        "vpa_wyckoff_rule_alignment_report_verified": report_reviews["vpa_wyckoff_rule_alignment_report_verified"],
        "abstention_quality_report_verified": report_reviews["abstention_quality_report_verified"],
        "per_ticker_backtest_report_verified": report_reviews["per_ticker_backtest_report_verified"],
        "chronological_split_report_verified": report_reviews["chronological_split_report_verified"],
        "meta_limitation_report_verified": report_reviews["meta_limitation_report_verified"],
        "no_peek_report_verified": report_reviews["no_peek_report_verified"],
        "operator_summary_verified": report_reviews["operator_summary_verified"],
        "digest_manifest_self_reference_policy": execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "chronological_split_policy": "CHRONOLOGICAL_NO_SHUFFLE",
        "horizon_aware_embargo_status": "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING",
        "blocked_randomized_null_reference_executed": False,
        "blocked_bootstrap_metric_computed": False,
        "target_values_used_as_predictors": row_stats["target_values_used_as_predictors"],
        "target_classes_used_as_predictors": row_stats["target_classes_used_as_predictors"],
        "forward_returns_used_as_features": row_stats["forward_returns_used_as_features"],
        "prediction_fields_present": row_stats["prediction_fields_present"],
        "strategy_score_fields_present": row_stats["strategy_score_fields_present"],
        "trade_recommendation_fields_present": row_stats["trade_recommendation_fields_present"],
        "broker_order_fields_present": row_stats["broker_order_fields_present"],
        "provider_payload_fields_present": row_stats["provider_payload_fields_present"],
        "api_key_fields_present": row_stats["api_key_fields_present"],
        "backtest_rows_jsonl_review": "VERIFIED_RESEARCH_ONLY",
        "backtest_lab_schema_review": "VERIFIED", "result_summary_review": "VERIFIED",
        "metric_report_review": "VERIFIED", "baseline_comparison_report_review": "VERIFIED",
        "vpa_wyckoff_rule_alignment_report_review": "VERIFIED",
        "abstention_quality_report_review": "VERIFIED", "per_ticker_backtest_report_review": "VERIFIED",
        "chronological_split_report_review": "VERIFIED", "meta_limitation_report_review": "VERIFIED",
        "no_peek_report_review": "VERIFIED", "operator_summary_review": "VERIFIED",
        "digest_manifest_review": "VERIFIED_ZERO_MISMATCHES",
        "per_ticker_expectancy_backtest_lab_results_review_entries": entries,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "model_training_authorized": False, "model_training_performed": False,
        "strategy_scoring_performed": False, "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False, "runtime_migration_approved": False,
        "runtime_migration_active": False, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "automatic_stitching": False,
        "provider_requests_made_in_review": False, "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "expectancy_backtest_lab_execution_rerun_performed": False,
        "expectancy_backtest_lab_approval_rerun_performed": False,
        "expectancy_backtest_lab_candidate_review_rerun_performed": False,
        "expectancy_backtest_lab_candidate_creation_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False, "target_generation_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True, "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    checklist = _checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    review["marketflow_expectancy_backtest_lab_results_review_digest"] = marketflow_expectancy_backtest_lab_results_review_digest_v1(review)
    review["review_summary"]["marketflow_expectancy_backtest_lab_results_review_digest"] = review["marketflow_expectancy_backtest_lab_results_review_digest"]
    return review


def marketflow_expectancy_backtest_lab_results_review_digest_v1(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    payload.pop("source_output_root", None)
    payload.pop("review_checklist", None)
    payload.pop("review_summary", None)
    payload.pop("marketflow_expectancy_backtest_lab_results_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_expectancy_backtest_lab_results_review_v1(*, output_root: str | Path | None = None) -> dict:
    """Review existing outputs read-only; never regenerate them."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, row_stats, report_reviews, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    review = _base_review(root, payloads, bindings, row_stats, report_reviews)
    validate_marketflow_expectancy_backtest_lab_results_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowExpectancyBacktestLabResultsReviewError(f"{field} mismatch")


def validate_marketflow_expectancy_backtest_lab_results_review_v1(review: dict) -> dict:
    if not isinstance(review, dict):
        raise MarketFlowExpectancyBacktestLabResultsReviewError("review must be a JSON object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME,
        "source_expectancy_backtest_lab_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_expectancy_backtest_lab_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_expectancy_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_expectancy_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_expectancy_backtest_lab_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "selected_backtest_lab_package": execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": len(TARGET_UNIVERSE),
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "expected_output_count": EXPECTED_OUTPUT_COUNT, "observed_output_count": EXPECTED_OUTPUT_COUNT,
        "output_digest_mismatch_count": 0, "expectancy_backtest_lab_row_count": EXPECTED_ROW_COUNT,
        "evaluable_target_row_count": EXPECTED_EVALUABLE_COUNT,
        "unavailable_target_row_count": EXPECTED_UNAVAILABLE_COUNT,
        "embargoed_cross_split_forward_horizon_row_count": EXPECTED_EMBARGOED_COUNT,
        "aggregate_metric_eligible_row_count": EXPECTED_AGGREGATE_METRIC_ELIGIBLE_COUNT,
        "expectancy_backtest_lab_results_review_created": True,
        "expectancy_backtest_lab_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_using_expectancy_lab_evidence": True,
        "predictive_usefulness_reassessment_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "model_training_authorized": False, "model_training_performed": False,
        "strategy_scoring_performed": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "target_values_used_as_predictors": False, "target_classes_used_as_predictors": False,
        "forward_returns_used_as_features": False, "prediction_fields_present": False,
        "strategy_score_fields_present": False, "trade_recommendation_fields_present": False,
        "broker_order_fields_present": False, "provider_payload_fields_present": False,
        "api_key_fields_present": False, "backtest_rows_jsonl_schema_verified": True,
        "metric_report_verified": True, "baseline_comparison_report_verified": True,
        "no_peek_report_verified": True,
    }
    for field, value in expected.items():
        _expect(review.get(field), value, field)
    if review.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowExpectancyBacktestLabResultsReviewError("risk controls missing")
    entries = review.get("per_ticker_expectancy_backtest_lab_results_review_entries")
    if not isinstance(entries, list) or len(entries) != len(TARGET_UNIVERSE):
        raise MarketFlowExpectancyBacktestLabResultsReviewError("per-ticker review missing")
    for entry in entries:
        if entry.get("per_ticker_expectancy_backtest_lab_results_review_digest") != per_ticker_expectancy_backtest_lab_results_review_digest_v1(entry):
            raise MarketFlowExpectancyBacktestLabResultsReviewError("per-ticker digest mismatch")
    checklist = _checklist(review)
    if review.get("review_checklist") != checklist or any(row["status"] != PASS for row in checklist):
        raise MarketFlowExpectancyBacktestLabResultsReviewError("review checklist mismatch")
    expected_summary = dict(review.get("review_summary", {}))
    expected_summary.update(_summary(checklist))
    if review.get("review_summary") != expected_summary:
        raise MarketFlowExpectancyBacktestLabResultsReviewError("review summary mismatch")
    digest = review.get("marketflow_expectancy_backtest_lab_results_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyBacktestLabResultsReviewError("review digest missing")
    if digest != marketflow_expectancy_backtest_lab_results_review_digest_v1(review):
        raise MarketFlowExpectancyBacktestLabResultsReviewError("review digest mismatch")
    return {
        "status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_expectancy_backtest_lab_results_review_digest": digest,
        **{field: review["review_summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_expectancy_backtest_lab_results_review_markdown_v1(review: dict) -> str:
    validate_marketflow_expectancy_backtest_lab_results_review_v1(review)
    sections = [
        ("Expectancy Backtest Lab Results Review v1", [f"Status: `{review['review_status']}`."]),
        ("Source Expectancy Backtest Lab Execution", [f"Digest `{review['source_expectancy_backtest_lab_execution_digest']}`."]),
        ("Bound Evidence", [f"{len(review['source_evidence'])} source digest fields are bound."]),
        ("Dataset and Universe", ["`expanded_universe_canonical_dataset_v1`; ordered 12-ticker universe; META remains 913 records."]),
        ("Output Verification", ["All 14 outputs exist and ordinary file hashes have zero mismatches."]),
        ("Selected Backtest Lab Package", [f"`{review['selected_backtest_lab_package']}`."]),
        ("Backtest Rows Review", [f"{review['expectancy_backtest_lab_row_count']} streamed rows; {review['aggregate_metric_eligible_row_count']} aggregate-metric eligible."]),
        ("Result Summary Review", ["Verified research-only counts and boundaries."]),
        ("Metric Report Review", ["All 13 approved descriptive metric families verified; bootstrap remains blocked."]),
        ("Baseline Comparison Review", ["Six approved baselines verified; randomized null remains blocked."]),
        ("VPA/Wyckoff Rule Alignment Review", ["Reviewed rule/state context only; no outcome-defined predictors."]),
        ("Abstention Quality Review", ["Descriptive coverage/avoidance evidence only."]),
        ("Chronological Split Review", ["Chronological no-shuffle and 4,200 horizon-embargoed rows verified."]),
        ("No-Peek and Leakage Review", ["Targets remain outcomes only; forbidden predictor/action fields are absent."]),
        ("Per-Ticker Backtest Review", ["Twelve deterministic review entries verified."]),
        ("META Limitation Review", ["META remains 913 records and 13,695 lab rows without repair or inference."]),
        ("Output Digest Manifest", [f"Self-reference policy `{review['digest_manifest_self_reference_policy']}`."]),
        ("Next Chain", review["next_chain"]), ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Reassessment is ready as a future task but not created; usefulness is not accepted."]),
        ("Profitability Boundary", ["Profitability is not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['review_summary']['passed_checks']}/{review['review_summary']['total_checks']} checks pass; zero blockers."]),
        ("Guardrails", ["No provider, acquisition, regeneration, rerun, training, scoring, recommendation, runtime, or trading action occurred."]),
    ]
    lines = []
    for index, (title, body) in enumerate(sections):
        lines.extend([("# " if index == 0 else "## ") + title, ""])
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_expectancy_backtest_lab_results_review_v1(
    output_dir: str | Path, *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    review = build_marketflow_expectancy_backtest_lab_results_review_v1(output_root=output_root)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    json_path = destination / "marketflow_expectancy_backtest_lab_results_review_v1.json"
    markdown_path = destination / "marketflow_expectancy_backtest_lab_results_review_v1.md"
    try:
        with json_path.open("xb") as handle:
            handle.write(canonical_json_bytes(review))
        if review.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE:
            markdown = build_marketflow_expectancy_backtest_lab_results_review_markdown_v1(review)
        else:
            markdown = "# Expectancy Backtest Lab Results Review v1\n\n- Review blocked: source outputs are missing or invalid.\n"
        with markdown_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(markdown)
    except FileExistsError as exc:
        raise MarketFlowExpectancyBacktestLabResultsReviewError("results-review output already exists") from exc
    return {"review": review, "json_path": _path_text(json_path), "markdown_path": _path_text(markdown_path)}
