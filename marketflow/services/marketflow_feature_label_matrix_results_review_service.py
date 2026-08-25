"""Offline review of existing feature-label matrix execution outputs."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_file,
)
from marketflow.services import (
    marketflow_feature_label_matrix_execution_service as execution,
)


ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE"
)
ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_V1 = (
    "marketflow_feature_label_matrix_results_review_v1"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING = (
    "FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_VALID = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_VALID"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_VALID = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_VALID"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "badaff7e1b34023d0ea2f2daa5b08e9cabaef0538b1da5c3c3b57f2b72d872f1"
)
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = (
    "697c74dd19f5c1ec60b372e39afc335fd9ea416ccf2a6b0c0600160a44b2ef8f"
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = (
    "edc8de9290c94561de344e1a86c39f2ecbe9ed2cc1ca6d54dd081c278c92c0c7"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = execution.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_MATRIX_ROW_COUNT = execution.EXPECTED_MATRIX_ROW_COUNT
EXPECTED_AVAILABLE_MATRIX_ROW_COUNT = execution.EXPECTED_AVAILABLE_MATRIX_ROW_COUNT
EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT = (
    execution.EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT
)
EXPECTED_FEATURE_GROUP_REFERENCE_COUNT = (
    execution.EXPECTED_FEATURE_GROUP_REFERENCE_COUNT
)
EXPECTED_FEATURE_SOURCE_ROW_COUNT = execution.EXPECTED_FEATURE_SOURCE_ROW_COUNT
EXPECTED_TARGET_SOURCE_ROW_COUNT = execution.EXPECTED_TARGET_SOURCE_ROW_COUNT
EXPECTED_PER_TICKER_UNAVAILABLE_TARGET_COUNT = 175
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NEXT_CHAIN = [
    "VPA/Wyckoff Rule Baseline Candidate v1.",
    "VPA/Wyckoff Rule Baseline Candidate Operator Review v1.",
    "VPA/Wyckoff Rule Baseline Approval v1.",
    "VPA/Wyckoff Rule Baseline Execution v1.",
    "VPA/Wyckoff Rule Baseline Results Review v1.",
    "Expectancy Backtest Lab Candidate only after separate approval.",
    "Results review and readiness gates before any predictive-usefulness acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "vpa_wyckoff_rule_baseline_candidate",
    "vpa_wyckoff_rule_baseline_candidate_operator_review",
    "vpa_wyckoff_rule_baseline_approval",
    "vpa_wyckoff_rule_baseline_execution",
    "vpa_wyckoff_rule_baseline_results_review",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_run_backtest",
    "review_does_not_train_models",
    "review_does_not_compute_performance_metrics",
    "review_does_not_score_strategy",
    "review_does_not_generate_trade_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_create_vpa_wyckoff_candidate",
    "review_does_not_create_expectancy_backtest_candidate",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_rerun_feature_label_matrix_execution",
    "review_does_not_rerun_target_generation_execution",
    "review_does_not_rerun_target_results_review",
    "review_does_not_rerun_signal_feature_generation_execution",
    "review_does_not_rerun_signal_feature_results_review",
    "review_does_not_rerun_matrix_candidate_creation",
    "review_does_not_rerun_matrix_candidate_review",
    "review_does_not_rerun_matrix_approval",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_matrix_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound", "source_output_binding_digest_bound",
    "source_matrix_rows_digest_bound", "source_approval_digest_bound",
    "source_candidate_review_digest_bound", "source_matrix_candidate_digest_bound",
    "source_signal_feature_results_review_digest_bound",
    "source_signal_feature_execution_digest_bound",
    "source_signal_feature_output_binding_digest_bound",
    "source_feature_values_digest_bound", "source_target_results_review_digest_bound",
    "source_target_generation_execution_digest_bound",
    "source_target_output_binding_digest_bound", "source_target_values_digest_bound",
    "source_signal_feature_approval_digest_bound",
    "source_signal_feature_candidate_review_digest_bound",
    "source_signal_feature_candidate_digest_bound", "source_target_approval_digest_bound",
    "source_design_results_review_digest_bound", "source_design_execution_digest_bound",
    "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_strategy_charter_approval_digest_bound", "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound", "source_archive_digest_bound",
    "source_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_prior_execution_digest_bound",
    "prior_matrix_digest_bound", "prior_feature_values_digest_bound",
    "prior_label_values_digest_bound", "research_registry_digest_bound",
    "records_digest_bound", "target_universe_12_preserved", "records_digest_preserved",
    "meta_913_preserved", "selected_matrix_package_preserved",
    "selected_matrix_layout_preserved", "selected_feature_package_preserved",
    "selected_target_package_preserved", "selected_objective_path_preserved",
    "expected_output_count_12", "observed_output_count_12",
    "output_digest_mismatch_count_zero", "matrix_rows_digest_matches",
    "matrix_rows_jsonl_schema_verified", "matrix_rows_count_verified",
    "matrix_row_count_179190", "available_matrix_row_count_177090",
    "unavailable_target_matrix_row_count_2100",
    "feature_group_count_per_matrix_row_13",
    "feature_group_reference_count_2329470", "non_meta_ticker_matrix_counts_verified",
    "meta_matrix_counts_verified", "target_values_not_inside_feature_bundle",
    "target_classes_not_inside_feature_bundle", "forward_returns_not_inside_feature_bundle",
    "future_data_not_inside_feature_bundle", "prediction_fields_absent",
    "strategy_score_fields_absent", "trade_recommendation_fields_absent",
    "broker_order_fields_absent", "provider_payload_fields_absent", "api_key_fields_absent",
    "digest_manifest_self_reference_policy_verified", "matrix_schema_verified",
    "feature_bundle_schema_verified", "target_profile_schema_verified",
    "matrix_coverage_report_verified", "matrix_no_peek_report_verified",
    "matrix_target_availability_report_verified", "per_ticker_matrix_report_verified",
    "meta_limitation_report_verified", "operator_summary_verified",
    "results_review_created_true", "results_review_ready_true",
    "ready_for_vpa_wyckoff_rule_baseline_candidate_true",
    "vpa_wyckoff_rule_baseline_candidate_created_false",
    "expectancy_backtest_lab_candidate_created_false",
    "backtest_execution_authorized_false", "backtest_execution_performed_false",
    "model_training_authorized_false", "model_training_performed_false",
    "metric_computation_authorized_false", "metric_computation_performed_false",
    "strategy_scoring_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "feature_label_matrix_execution_rerun_false", "target_generation_execution_rerun_false",
    "target_results_review_rerun_false", "signal_feature_generation_execution_rerun_false",
    "signal_feature_results_review_rerun_false", "matrix_candidate_creation_rerun_false",
    "matrix_candidate_review_rerun_false", "matrix_approval_rerun_false",
    "raw_provider_payloads_not_committed", "api_keys_not_stored_or_printed",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]

BUNDLE_FORBIDDEN_KEYS = {
    "target_value", "target_class", "forward_return", "future_label_value",
    "prediction", "prediction_value", "strategy_score", "trade_recommendation",
    "broker_order", "broker_order_id", "order_id", "raw_provider_payload",
    "provider_payload", "api_key", "api_keys",
}
ROW_FORBIDDEN_KEYS = {
    "prediction", "prediction_value", "strategy_score", "trade_recommendation",
    "broker_order", "broker_order_id", "order_id", "raw_provider_payload",
    "provider_payload", "api_key", "api_keys",
}


class MarketFlowFeatureLabelMatrixResultsReviewError(ValueError):
    """Raised when generated matrix evidence violates the review contract."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MarketFlowFeatureLabelMatrixResultsReviewError(
            f"invalid JSON output: {path.name}"
        ) from exc
    if not isinstance(value, dict):
        raise MarketFlowFeatureLabelMatrixResultsReviewError(
            f"JSON output must be an object: {path.name}"
        )
    return value


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


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


def _inspect_matrix_rows(path: Path) -> dict[str, Any]:
    row_count = available_count = unavailable_count = group_references = 0
    schema_valid = research_only_valid = package_binding_valid = True
    target_nullability_valid = True
    bundle_forbidden: set[str] = set()
    row_forbidden: set[str] = set()
    future_bundle_fields: set[str] = set()
    ticker_total: Counter[str] = Counter()
    ticker_available: Counter[str] = Counter()
    ticker_unavailable: Counter[str] = Counter()
    group_counts: Counter[int] = Counter()
    expected_groups = set(execution.SELECTED_FEATURE_GROUPS)
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    schema_valid = False
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError(f"matrix row {line_number} is not an object")
                row_count += 1
                schema_valid = schema_valid and set(row) == set(execution.MATRIX_ROW_FIELDS)
                ticker = row.get("ticker")
                if ticker not in TARGET_UNIVERSE:
                    schema_valid = False
                    continue
                bundle = row.get("feature_bundle")
                if not isinstance(bundle, dict) or set(bundle) != expected_groups:
                    schema_valid = False
                    continue
                group_count = len(bundle)
                group_counts[group_count] += 1
                group_references += group_count
                if row.get("feature_group_count") != group_count:
                    schema_valid = False
                bundle_keys = _nested_keys(bundle)
                bundle_forbidden.update(BUNDLE_FORBIDDEN_KEYS & bundle_keys)
                future_bundle_fields.update(
                    key for key in bundle_keys
                    if key.startswith("future_") or key.startswith("forward_")
                )
                for group in execution.SELECTED_FEATURE_GROUPS:
                    entry = bundle.get(group)
                    if not isinstance(entry, dict) or set(entry) != set(execution.FEATURE_BUNDLE_FIELDS):
                        schema_valid = False
                row_forbidden.update(ROW_FORBIDDEN_KEYS & set(row))
                research_only_valid = (
                    research_only_valid
                    and row.get("research_only") is True
                    and row.get("non_actionable") is True
                )
                package_binding_valid = (
                    package_binding_valid
                    and row.get("dataset_name") == "expanded_universe_canonical_dataset_v1"
                    and row.get("source_profile") == "RTH_FULL_SESSION_1D"
                    and row.get("timeframe") == "1d"
                    and row.get("records_digest") == execution.EXPECTED_RECORDS_DIGEST
                    and row.get("source_matrix_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST
                    and row.get("selected_matrix_package") == execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX
                    and row.get("selected_matrix_layout") == execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE
                    and row.get("selected_feature_package") == execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET
                    and row.get("selected_label_target_package") == execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET
                    and row.get("selected_objective_path") == execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT
                )
                ticker_total[ticker] += 1
                if row.get("target_available") is True:
                    available_count += 1
                    ticker_available[ticker] += 1
                    if row.get("target_value") is None and row.get("target_class") is None:
                        target_nullability_valid = False
                elif row.get("target_available") is False:
                    unavailable_count += 1
                    ticker_unavailable[ticker] += 1
                    if row.get("target_value") is not None or row.get("target_class") is not None:
                        target_nullability_valid = False
                else:
                    schema_valid = False
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise MarketFlowFeatureLabelMatrixResultsReviewError(
            "matrix_rows.jsonl could not be inspected"
        ) from exc
    non_meta_verified = all(
        ticker_total[ticker] == EXPECTED_RECORD_COUNTS[ticker] * 15
        and ticker_available[ticker] == (
            EXPECTED_RECORD_COUNTS[ticker] * 15
            - EXPECTED_PER_TICKER_UNAVAILABLE_TARGET_COUNT
        )
        and ticker_unavailable[ticker]
        == EXPECTED_PER_TICKER_UNAVAILABLE_TARGET_COUNT
        for ticker in TARGET_UNIVERSE if ticker != "META"
    )
    meta_verified = (
        ticker_total["META"] == EXPECTED_RECORD_COUNTS.get("META", 0) * 15
        and ticker_available["META"] == (
            EXPECTED_RECORD_COUNTS.get("META", 0) * 15
            - EXPECTED_PER_TICKER_UNAVAILABLE_TARGET_COUNT
        )
        and ticker_unavailable["META"]
        == EXPECTED_PER_TICKER_UNAVAILABLE_TARGET_COUNT
    )
    return {
        "matrix_row_count": row_count,
        "available_matrix_row_count": available_count,
        "unavailable_target_matrix_row_count": unavailable_count,
        "feature_group_reference_count": group_references,
        "feature_group_counts": dict(group_counts),
        "matrix_rows_jsonl_schema_verified": schema_valid,
        "research_only_non_actionable_verified": research_only_valid,
        "package_binding_verified": package_binding_valid,
        "target_unavailable_nullability_verified": target_nullability_valid,
        "target_values_inside_feature_bundle": "target_value" in bundle_forbidden,
        "target_classes_inside_feature_bundle": "target_class" in bundle_forbidden,
        "forward_returns_inside_feature_bundle": "forward_return" in bundle_forbidden,
        "future_data_inside_feature_bundle": bool(future_bundle_fields),
        "prediction_fields_present": bool({"prediction", "prediction_value"} & (bundle_forbidden | row_forbidden)),
        "strategy_score_fields_present": "strategy_score" in bundle_forbidden | row_forbidden,
        "trade_recommendation_fields_present": "trade_recommendation" in bundle_forbidden | row_forbidden,
        "broker_order_fields_present": bool({"broker_order", "broker_order_id", "order_id"} & (bundle_forbidden | row_forbidden)),
        "provider_payload_fields_present": bool({"raw_provider_payload", "provider_payload"} & (bundle_forbidden | row_forbidden)),
        "api_key_fields_present": bool({"api_key", "api_keys"} & (bundle_forbidden | row_forbidden)),
        "per_ticker_matrix_row_counts": {ticker: ticker_total[ticker] for ticker in TARGET_UNIVERSE},
        "per_ticker_available_matrix_row_counts": {ticker: ticker_available[ticker] for ticker in TARGET_UNIVERSE},
        "per_ticker_unavailable_target_matrix_row_counts": {ticker: ticker_unavailable[ticker] for ticker in TARGET_UNIVERSE},
        "non_meta_ticker_matrix_counts_verified": non_meta_verified,
        "meta_matrix_counts_verified": meta_verified,
    }


def _verify_reports(payloads: Mapping[str, dict[str, Any]]) -> dict[str, bool]:
    schema = payloads["feature_label_matrix_schema.json"]
    bundle = payloads["feature_bundle_schema.json"]
    target = payloads["target_profile_schema.json"]
    coverage = payloads["matrix_coverage_report.json"]
    no_peek = payloads["matrix_no_peek_report.json"]
    availability = payloads["matrix_target_availability_report.json"]
    per_ticker = payloads["per_ticker_matrix_report.json"]
    meta = payloads["meta_limitation_report.json"]
    operator = payloads["operator_summary.json"]
    common_reports = [
        payloads[name] for name in EXPECTED_OUTPUT_FILENAMES
        if name not in (EXPECTED_OUTPUT_FILENAMES[0], "matrix_rows.jsonl")
    ]
    common_valid = all(
        report.get("output_label") == execution.OUTPUT_LABEL
        and report.get("evidence_scope") == execution.EVIDENCE_SCOPE
        and report.get("research_only", True) is True
        and report.get("backtest_execution_authorized") is False
        and report.get("runtime_use") == NOT_AUTHORIZED
        for report in common_reports
    )
    ticker_rows = per_ticker.get("per_ticker_entries", [])
    return {
        "common_output_boundary_verified": common_valid,
        "matrix_schema_verified": (
            schema.get("matrix_row_fields") == execution.MATRIX_ROW_FIELDS
            and schema.get("one_matrix_row_per_target_row") is True
            and schema.get("target_outcomes_are_not_features") is True
        ),
        "feature_bundle_schema_verified": (
            bundle.get("feature_groups") == execution.SELECTED_FEATURE_GROUPS
            and bundle.get("feature_group_count") == 13
            and bundle.get("feature_bundle_entry_fields") == execution.FEATURE_BUNDLE_FIELDS
        ),
        "target_profile_schema_verified": (
            target.get("target_profile_count") == 15
            and target.get("unavailable_targets_retained_with_null_outcomes") is True
            and target.get("target_outcomes_are_outcome_fields_only") is True
        ),
        "matrix_coverage_report_verified": (
            coverage.get("matrix_row_count") == EXPECTED_MATRIX_ROW_COUNT
            and coverage.get("available_matrix_row_count") == EXPECTED_AVAILABLE_MATRIX_ROW_COUNT
            and coverage.get("unavailable_target_matrix_row_count") == EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT
            and coverage.get("feature_group_reference_count") == EXPECTED_FEATURE_GROUP_REFERENCE_COUNT
            and coverage.get("canonical_records_dropped") == 0
            and coverage.get("target_rows_dropped") == 0
        ),
        "matrix_no_peek_report_verified": all(
            no_peek.get(field) is True for field in (
                "target_values_not_inside_feature_bundle",
                "target_classes_not_inside_feature_bundle",
                "forward_returns_not_inside_feature_bundle",
                "future_data_not_inside_feature_bundle",
                "prediction_fields_absent", "strategy_score_fields_absent",
                "trade_recommendation_fields_absent",
            )
        ),
        "matrix_target_availability_report_verified": (
            availability.get("available_matrix_row_count") == EXPECTED_AVAILABLE_MATRIX_ROW_COUNT
            and availability.get("unavailable_target_matrix_row_count") == EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT
            and availability.get("unavailable_target_rows_retained") is True
            and availability.get("unavailable_target_values_are_null") is True
            and availability.get("unavailable_target_classes_are_null") is True
        ),
        "per_ticker_matrix_report_verified": (
            len(ticker_rows) == len(TARGET_UNIVERSE)
            and [row.get("ticker") for row in ticker_rows] == TARGET_UNIVERSE
        ),
        "meta_limitation_report_verified": (
            meta.get("ticker") == "META"
            and meta.get("historical_record_count") == EXPECTED_RECORD_COUNTS.get("META")
            and meta.get("matrix_row_count") == EXPECTED_RECORD_COUNTS.get("META", 0) * 15
            and meta.get("meta_reduced_record_count_flag") is True
            and meta.get("repaired_inferred_smoothed_or_fabricated") is False
        ),
        "operator_summary_verified": (
            operator.get("execution_status") == execution.MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY
            and operator.get("matrix_row_count") == EXPECTED_MATRIX_ROW_COUNT
            and operator.get("generated_output_count") == 12
        ),
    }


def _verify_outputs(output_root: Path) -> tuple[
    dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any],
    dict[str, bool], list[dict[str, Any]],
]:
    if not output_root.is_dir():
        return {}, [], {}, {}, [_failure(
            "missing_output_root", "feature-label matrix output root is missing",
            output_root=_path_text(output_root),
        )]
    actual_names = sorted(path.name for path in output_root.iterdir() if path.is_file())
    missing = [name for name in EXPECTED_OUTPUT_FILENAMES if name not in actual_names]
    if missing or len(actual_names) != 12:
        return {}, [], {}, {}, [_failure(
            "output_file_inventory_mismatch",
            "expected matrix output inventory is incomplete or contains extras",
            expected=EXPECTED_OUTPUT_FILENAMES, actual=actual_names, missing=missing,
        )]
    try:
        payloads = {
            filename: _load_json(output_root / filename)
            for filename in EXPECTED_OUTPUT_FILENAMES if filename != "matrix_rows.jsonl"
        }
        source = payloads["feature_label_matrix_manifest.json"]
        execution.validate_marketflow_feature_label_matrix_execution_v1(source)
        matrix_path = output_root / "matrix_rows.jsonl"
        matrix_before_sha = sha256_file(matrix_path)
        matrix_stats = _inspect_matrix_rows(matrix_path)
    except (
        MarketFlowFeatureLabelMatrixResultsReviewError,
        execution.MarketFlowFeatureLabelMatrixExecutionError,
    ) as exc:
        return {}, [], {}, {}, [_failure(
            "invalid_source_output", "feature-label matrix outputs are invalid", error=str(exc)
        )]
    digest_report = payloads["feature_label_matrix_digest_manifest.json"]
    recorded = digest_report.get("output_digest_manifest")
    if not isinstance(recorded, list) or recorded != source.get("output_digest_manifest"):
        return {}, [], {}, {}, [_failure(
            "digest_manifest_mismatch", "digest manifest does not match execution artifact"
        )]
    recorded_by_name = {
        row.get("filename"): row for row in recorded if isinstance(row, dict)
    }
    bindings: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        entry = recorded_by_name.get(filename, {})
        local_sha = (
            matrix_before_sha
            if filename == "matrix_rows.jsonl"
            else sha256_file(output_root / filename)
        )
        kind = entry.get("digest_kind")
        recorded_sha = entry.get("sha256")
        if filename == EXPECTED_OUTPUT_FILENAMES[0]:
            verified = kind == "SELF_REFERENTIAL_EXECUTION_ARTIFACT" and recorded_sha is None
        elif filename == EXPECTED_OUTPUT_FILENAMES[-1]:
            verified = kind == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE and recorded_sha is None
        else:
            verified = kind == "FILE_SHA256" and recorded_sha == local_sha
        bindings.append({
            "filename": filename,
            "local_sha256": local_sha,
            "recorded_digest_kind": kind,
            "recorded_sha256": recorded_sha,
            "verification_status": PASS if verified else FAIL,
        })
    failures: list[dict[str, Any]] = []
    local = {row["filename"]: row["local_sha256"] for row in bindings}
    if any(row["verification_status"] != PASS for row in bindings):
        failures.append(_failure(
            "output_digest_verification_failed", "one or more matrix output digests do not match"
        ))
    if local.get("matrix_rows.jsonl") != EXPECTED_SOURCE_MATRIX_ROWS_DIGEST:
        failures.append(_failure("matrix_rows_digest_mismatch", "matrix rows digest changed"))
    if source.get("marketflow_feature_label_matrix_execution_digest") != EXPECTED_SOURCE_EXECUTION_DIGEST:
        failures.append(_failure("source_execution_digest_mismatch", "source execution digest changed"))
    if source.get("feature_label_matrix_output_binding_digest") != EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST:
        failures.append(_failure("source_output_binding_digest_mismatch", "source binding digest changed"))
    if digest_report.get("manifest_self_reference_policy") != execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE:
        failures.append(_failure(
            "manifest_self_reference_policy_mismatch", "digest manifest policy changed"
        ))
    reports = _verify_reports(payloads)
    if not all(reports.values()):
        failures.append(_failure(
            "report_content_verification_failed", "one or more matrix reports failed verification",
            report_reviews=reports,
        ))
    matrix_valid = all((
        matrix_stats.get("matrix_rows_jsonl_schema_verified"),
        matrix_stats.get("research_only_non_actionable_verified"),
        matrix_stats.get("package_binding_verified"),
        matrix_stats.get("target_unavailable_nullability_verified"),
        matrix_stats.get("matrix_row_count") == EXPECTED_MATRIX_ROW_COUNT,
        matrix_stats.get("available_matrix_row_count") == EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        matrix_stats.get("unavailable_target_matrix_row_count") == EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        matrix_stats.get("feature_group_reference_count") == EXPECTED_FEATURE_GROUP_REFERENCE_COUNT,
        matrix_stats.get("feature_group_counts") == {13: EXPECTED_MATRIX_ROW_COUNT},
        matrix_stats.get("non_meta_ticker_matrix_counts_verified"),
        matrix_stats.get("meta_matrix_counts_verified"),
        not matrix_stats.get("target_values_inside_feature_bundle"),
        not matrix_stats.get("target_classes_inside_feature_bundle"),
        not matrix_stats.get("forward_returns_inside_feature_bundle"),
        not matrix_stats.get("future_data_inside_feature_bundle"),
        not matrix_stats.get("prediction_fields_present"),
        not matrix_stats.get("strategy_score_fields_present"),
        not matrix_stats.get("trade_recommendation_fields_present"),
        not matrix_stats.get("broker_order_fields_present"),
        not matrix_stats.get("provider_payload_fields_present"),
        not matrix_stats.get("api_key_fields_present"),
    ))
    if not matrix_valid:
        failures.append(_failure(
            "matrix_content_verification_failed",
            "matrix rows schema, counts, or boundaries failed verification",
            matrix_stats=matrix_stats,
        ))
    after_matrix_sha = sha256_file(output_root / "matrix_rows.jsonl")
    matrix_stats["matrix_rows_digest_before_streaming"] = local.get("matrix_rows.jsonl")
    matrix_stats["matrix_rows_digest_after_streaming"] = after_matrix_sha
    matrix_stats["matrix_output_unchanged_during_review"] = (
        after_matrix_sha == local.get("matrix_rows.jsonl") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
    )
    if not matrix_stats["matrix_output_unchanged_during_review"]:
        failures.append(_failure(
            "matrix_output_changed_during_review", "matrix rows changed during streaming review"
        ))
    return payloads, bindings, matrix_stats, reports, failures


def per_ticker_feature_label_matrix_results_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_feature_label_matrix_results_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_entries = source["per_ticker_feature_label_matrix_execution_entries"]
    rows: list[dict[str, Any]] = []
    for source_entry in source_entries:
        ticker = source_entry["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "feature_label_matrix_execution_status": execution.MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY,
            "feature_label_matrix_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
            "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "matrix_row_count": source_entry["matrix_row_count"],
            "available_matrix_row_count": source_entry["available_matrix_row_count"],
            "unavailable_target_matrix_row_count": source_entry["unavailable_target_matrix_row_count"],
            "feature_source_row_count": source_entry["feature_source_row_count"],
            "target_source_row_count": source_entry["target_source_row_count"],
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
            "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
            "source_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
            "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_RESULTS_REVIEW"
                if ticker == "META" else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_feature_label_matrix_results_review_digest"] = (
            per_ticker_feature_label_matrix_results_review_digest_v1(entry)
        )
        rows.append(entry)
    return rows


def _source_evidence(source: Mapping[str, Any]) -> dict[str, str]:
    evidence = deepcopy(source.get("source_evidence", {}))
    evidence.update({
        "marketflow_feature_label_matrix_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
    })
    return evidence


def _blocked_package(output_root: Path, failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "review_scope": FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "created_offline": True,
        "research_only": True,
        "source_output_root": _path_text(output_root),
        "feature_label_matrix_results_review_created": False,
        "feature_label_matrix_results_review_ready": False,
        "ready_for_vpa_wyckoff_rule_baseline_candidate": False,
        "vpa_wyckoff_rule_baseline_candidate_created": False,
        "expectancy_backtest_lab_candidate_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "expected_output_count": 12,
        "observed_output_count": 0,
        "marketflow_feature_label_matrix_results_review_digest": "NOT_CREATED",
        "risk_controls": list(RISK_CONTROLS),
        "failures": failures,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "review condition satisfied" if status == PASS else "review condition failed",
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    source = review.get("source_evidence", {})
    inspection = review.get("matrix_rows_inspection", {})
    reports = review.get("report_reviews", {})
    entries = review.get("per_ticker_feature_label_matrix_results_review_entries", [])
    digest_checks = {
        "source_execution_digest_bound": "marketflow_feature_label_matrix_execution_digest",
        "source_output_binding_digest_bound": "feature_label_matrix_output_binding_digest",
        "source_matrix_rows_digest_bound": "feature_label_matrix_rows_digest",
        "source_approval_digest_bound": "marketflow_feature_label_matrix_approval_digest",
        "source_candidate_review_digest_bound": "marketflow_feature_label_matrix_candidate_operator_review_digest",
        "source_matrix_candidate_digest_bound": "marketflow_feature_label_matrix_candidate_v1_digest",
        "source_signal_feature_results_review_digest_bound": "marketflow_signal_or_feature_generation_results_review_digest",
        "source_signal_feature_execution_digest_bound": "marketflow_signal_or_feature_generation_execution_digest",
        "source_signal_feature_output_binding_digest_bound": "signal_or_feature_generation_output_binding_digest",
        "source_feature_values_digest_bound": "signal_or_feature_values_digest",
        "source_target_results_review_digest_bound": "marketflow_objective_label_or_target_generation_results_review_digest",
        "source_target_generation_execution_digest_bound": "marketflow_objective_label_or_target_generation_execution_digest",
        "source_target_output_binding_digest_bound": "objective_label_or_target_generation_output_binding_digest",
        "source_target_values_digest_bound": "objective_label_or_target_values_digest",
        "source_signal_feature_approval_digest_bound": "marketflow_signal_or_feature_generation_approval_digest",
        "source_signal_feature_candidate_review_digest_bound": "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
        "source_signal_feature_candidate_digest_bound": "marketflow_signal_or_feature_generation_candidate_v1_digest",
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
        "prior_matrix_digest_bound": "prior_feature_label_matrix_digest",
        "prior_feature_values_digest_bound": "prior_feature_values_digest",
        "prior_label_values_digest_bound": "redesigned_label_values_digest",
        "research_registry_digest_bound": "research_registry_approval_digest",
        "records_digest_bound": "records_digest",
    }
    values = {
        check_id: isinstance(source.get(key), str) and len(source[key]) == 64
        for check_id, key in digest_checks.items()
    }
    values.update({
        "target_universe_12_preserved": review.get("target_universe") == TARGET_UNIVERSE and review.get("target_universe_count") == len(TARGET_UNIVERSE),
        "records_digest_preserved": review.get("records_digest") == execution.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": review.get("meta_record_count") == EXPECTED_RECORD_COUNTS.get("META"),
        "selected_matrix_package_preserved": review.get("selected_matrix_package") == execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout_preserved": review.get("selected_matrix_layout") == execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package_preserved": review.get("selected_feature_package") == execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_target_package_preserved": review.get("selected_label_target_package") == execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": review.get("selected_objective_path") == execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "expected_output_count_12": review.get("expected_output_count") == 12,
        "observed_output_count_12": review.get("observed_output_count") == 12,
        "output_digest_mismatch_count_zero": review.get("output_digest_mismatch_count") == 0,
        "matrix_rows_digest_matches": review.get("local_output_digests", {}).get("matrix_rows.jsonl") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "matrix_rows_jsonl_schema_verified": inspection.get("matrix_rows_jsonl_schema_verified") is True,
        "matrix_rows_count_verified": review.get("matrix_rows_count_verified") is True,
        "matrix_row_count_179190": review.get("matrix_row_count") == EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count_177090": review.get("available_matrix_row_count") == EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count_2100": review.get("unavailable_target_matrix_row_count") == EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "feature_group_count_per_matrix_row_13": review.get("feature_group_count_per_matrix_row") == 13,
        "feature_group_reference_count_2329470": review.get("feature_group_reference_count") == EXPECTED_FEATURE_GROUP_REFERENCE_COUNT,
        "non_meta_ticker_matrix_counts_verified": inspection.get("non_meta_ticker_matrix_counts_verified") is True,
        "meta_matrix_counts_verified": inspection.get("meta_matrix_counts_verified") is True,
        "target_values_not_inside_feature_bundle": review.get("target_values_inside_feature_bundle") is False,
        "target_classes_not_inside_feature_bundle": review.get("target_classes_inside_feature_bundle") is False,
        "forward_returns_not_inside_feature_bundle": review.get("forward_returns_inside_feature_bundle") is False,
        "future_data_not_inside_feature_bundle": review.get("future_data_inside_feature_bundle") is False,
        "prediction_fields_absent": review.get("prediction_fields_present") is False,
        "strategy_score_fields_absent": review.get("strategy_score_fields_present") is False,
        "trade_recommendation_fields_absent": review.get("trade_recommendation_fields_present") is False,
        "broker_order_fields_absent": review.get("broker_order_fields_present") is False,
        "provider_payload_fields_absent": review.get("provider_payload_fields_present") is False,
        "api_key_fields_absent": review.get("api_key_fields_present") is False,
        "digest_manifest_self_reference_policy_verified": review.get("digest_manifest_self_reference_policy") == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "matrix_schema_verified": reports.get("matrix_schema_verified") is True,
        "feature_bundle_schema_verified": reports.get("feature_bundle_schema_verified") is True,
        "target_profile_schema_verified": reports.get("target_profile_schema_verified") is True,
        "matrix_coverage_report_verified": reports.get("matrix_coverage_report_verified") is True,
        "matrix_no_peek_report_verified": reports.get("matrix_no_peek_report_verified") is True,
        "matrix_target_availability_report_verified": reports.get("matrix_target_availability_report_verified") is True,
        "per_ticker_matrix_report_verified": reports.get("per_ticker_matrix_report_verified") is True,
        "meta_limitation_report_verified": reports.get("meta_limitation_report_verified") is True,
        "operator_summary_verified": reports.get("operator_summary_verified") is True,
        "results_review_created_true": review.get("feature_label_matrix_results_review_created") is True,
        "results_review_ready_true": review.get("feature_label_matrix_results_review_ready") is True,
        "ready_for_vpa_wyckoff_rule_baseline_candidate_true": review.get("ready_for_vpa_wyckoff_rule_baseline_candidate") is True,
        "vpa_wyckoff_rule_baseline_candidate_created_false": review.get("vpa_wyckoff_rule_baseline_candidate_created") is False,
        "expectancy_backtest_lab_candidate_created_false": review.get("expectancy_backtest_lab_candidate_created") is False,
        "backtest_execution_authorized_false": review.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": review.get("backtest_execution_performed") is False,
        "model_training_authorized_false": review.get("model_training_authorized") is False,
        "model_training_performed_false": review.get("model_training_performed") is False,
        "metric_computation_authorized_false": review.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": review.get("metric_computation_performed") is False,
        "strategy_scoring_false": review.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": review.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review.get("trade_recommendations_generated") is False,
        "per_ticker_entries_12": len(entries) == len(TARGET_UNIVERSE) and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_feature_label_matrix_results_review_digest") == per_ticker_feature_label_matrix_results_review_digest_v1(row) for row in entries),
        "provider_requests_made_false": review.get("provider_requests_made_in_review") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_review") is False,
        "dataset_regeneration_false": review.get("canonical_dataset_regenerated_in_review") is False,
        "feature_label_matrix_execution_rerun_false": review.get("feature_label_matrix_execution_rerun_performed") is False,
        "target_generation_execution_rerun_false": review.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": review.get("target_generation_results_review_rerun_performed") is False,
        "signal_feature_generation_execution_rerun_false": review.get("signal_feature_generation_execution_rerun_performed") is False,
        "signal_feature_results_review_rerun_false": review.get("signal_feature_results_review_rerun_performed") is False,
        "matrix_candidate_creation_rerun_false": review.get("matrix_candidate_creation_rerun_performed") is False,
        "matrix_candidate_review_rerun_false": review.get("matrix_candidate_review_rerun_performed") is False,
        "matrix_approval_rerun_false": review.get("matrix_approval_rerun_performed") is False,
        "raw_provider_payloads_not_committed": review.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": review.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    })
    return values


def _review_checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, True, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist), "passed_checks": passed,
        "failed_checks": failed, "blocker_count": failed,
        "feature_label_matrix_results_review_created": True,
        "feature_label_matrix_results_review_ready": True,
        "ready_for_vpa_wyckoff_rule_baseline_candidate": True,
        "vpa_wyckoff_rule_baseline_candidate_created": False,
        "expectancy_backtest_lab_candidate_created": False,
        "matrix_row_count": EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "output_digest_mismatch_count": 0,
        "backtest_execution_performed": False, "model_training_performed": False,
        "metric_computation_performed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _base_review(
    output_root: Path,
    payloads: Mapping[str, dict[str, Any]],
    bindings: list[dict[str, Any]],
    matrix_stats: Mapping[str, Any],
    report_reviews: Mapping[str, bool],
) -> dict[str, Any]:
    source = payloads["feature_label_matrix_manifest.json"]
    local_digests = {row["filename"]: row["local_sha256"] for row in bindings}
    entries = _per_ticker_review_entries(source)
    review = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_output_root": _path_text(output_root),
        "source_feature_label_matrix_execution_artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED,
        "source_feature_label_matrix_execution_status": execution.MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY,
        "source_feature_label_matrix_execution_scope": execution.FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_label_matrix_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": source["source_candidate_review_digest"],
        "source_matrix_candidate_digest": source["source_matrix_candidate_digest"],
        "source_signal_feature_results_review_digest": source["source_evidence"]["marketflow_signal_or_feature_generation_results_review_digest"],
        "source_feature_values_digest": source["source_feature_values_digest"],
        "source_target_results_review_digest": source["source_evidence"]["marketflow_objective_label_or_target_generation_results_review_digest"],
        "source_target_values_digest": source["source_target_values_digest"],
        "source_evidence": _source_evidence(source),
        "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": len(TARGET_UNIVERSE),
        "total_canonical_record_count": sum(EXPECTED_RECORD_COUNTS.values()),
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "non_meta_record_count": next((count for ticker, count in EXPECTED_RECORD_COUNTS.items() if ticker != "META"), None),
        "meta_reduced_record_count_preserved": True,
        "feature_label_matrix_created": True, "feature_label_matrix_rows_created": True,
        "feature_label_matrix_execution_performed": True, "joined_matrix_output_created": True,
        "feature_label_matrix_results_created": True,
        "feature_label_matrix_results_review_created": True,
        "feature_label_matrix_results_review_ready": True,
        "ready_for_vpa_wyckoff_rule_baseline_candidate": True,
        "vpa_wyckoff_rule_baseline_candidate_created": False,
        "expectancy_backtest_lab_candidate_created": False,
        "matrix_row_count": matrix_stats["matrix_row_count"],
        "available_matrix_row_count": matrix_stats["available_matrix_row_count"],
        "unavailable_target_matrix_row_count": matrix_stats["unavailable_target_matrix_row_count"],
        "feature_group_count_per_matrix_row": 13,
        "feature_group_reference_count": matrix_stats["feature_group_reference_count"],
        "feature_source_row_count": EXPECTED_FEATURE_SOURCE_ROW_COUNT,
        "target_source_row_count": EXPECTED_TARGET_SOURCE_ROW_COUNT,
        "expected_output_count": 12, "observed_output_count": len(bindings),
        "output_file_inspection_performed": True,
        "output_digest_bindings": deepcopy(bindings), "local_output_digests": local_digests,
        "recorded_file_digest_match_count": sum(
            row["recorded_digest_kind"] == "FILE_SHA256" and row["verification_status"] == PASS
            for row in bindings
        ),
        "local_output_digest_count": len(local_digests),
        "output_digest_mismatch_count": sum(row["verification_status"] != PASS for row in bindings),
        "digest_manifest_self_reference_policy": execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "execution_artifact_special_policy": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
        "matrix_rows_inspection": deepcopy(dict(matrix_stats)),
        "matrix_rows_jsonl_schema_verified": matrix_stats["matrix_rows_jsonl_schema_verified"],
        "matrix_rows_count_verified": matrix_stats["matrix_row_count"] == EXPECTED_MATRIX_ROW_COUNT,
        "per_ticker_matrix_counts_verified": matrix_stats["non_meta_ticker_matrix_counts_verified"] and matrix_stats["meta_matrix_counts_verified"],
        "meta_limitation_verified": matrix_stats["meta_matrix_counts_verified"],
        "report_reviews": deepcopy(dict(report_reviews)),
        "matrix_rows_jsonl_review": "VERIFIED_RESEARCH_ONLY",
        "matrix_schema_review": "VERIFIED", "feature_bundle_schema_review": "VERIFIED",
        "target_profile_schema_review": "VERIFIED", "matrix_coverage_report_review": "VERIFIED",
        "matrix_no_peek_report_review": "VERIFIED",
        "matrix_target_availability_report_review": "VERIFIED",
        "per_ticker_matrix_report_review": "VERIFIED", "meta_limitation_report_review": "VERIFIED",
        "operator_summary_review": "VERIFIED", "digest_manifest_review": "VERIFIED_ZERO_MISMATCHES",
        "per_ticker_feature_label_matrix_results_review_entries": entries,
        **{
            field: matrix_stats[field] for field in (
                "target_values_inside_feature_bundle", "target_classes_inside_feature_bundle",
                "forward_returns_inside_feature_bundle", "future_data_inside_feature_bundle",
                "prediction_fields_present", "strategy_score_fields_present",
                "trade_recommendation_fields_present", "broker_order_fields_present",
                "provider_payload_fields_present", "api_key_fields_present",
            )
        },
        "backtest_execution_authorized": False, "backtest_execution_performed": False,
        "model_training_authorized": False, "model_training_performed": False,
        "metric_computation_authorized": False, "metric_computation_performed": False,
        "strategy_scoring_performed": False, "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False, "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False, "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "signal_feature_generation_execution_rerun_performed": False,
        "signal_feature_results_review_rerun_performed": False,
        "matrix_candidate_creation_rerun_performed": False,
        "matrix_candidate_review_rerun_performed": False,
        "matrix_approval_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }
    return review


def marketflow_feature_label_matrix_results_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop("marketflow_feature_label_matrix_results_review_digest", None)
    payload.pop("source_output_root", None)
    return semantic_digest(payload)


def build_marketflow_feature_label_matrix_results_review_v1(
    *, output_root: str | Path | None = None,
) -> dict:
    """Stream and bind existing matrix outputs without regenerating them."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, matrix_stats, report_reviews, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    review = _base_review(root, payloads, bindings, matrix_stats, report_reviews)
    checklist = _review_checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    if review["review_summary"]["blocker_count"]:
        return _blocked_package(root, [_failure(
            "review_checklist_blocked", "results-review checklist contains blockers",
            failed_check_ids=[row["check_id"] for row in checklist if row["status"] != PASS],
        )])
    review["marketflow_feature_label_matrix_results_review_digest"] = (
        marketflow_feature_label_matrix_results_review_digest_v1(review)
    )
    validate_marketflow_feature_label_matrix_results_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowFeatureLabelMatrixResultsReviewError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_feature_label_matrix_results_review_v1(review: dict) -> dict:
    """Validate a ready or fail-closed matrix results-review package."""
    if not isinstance(review, dict):
        raise MarketFlowFeatureLabelMatrixResultsReviewError("results review must be an object")
    if review.get("review_status") == MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        _expect(review.get("artifact_kind"), ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED, "artifact_kind")
        _expect(review.get("feature_label_matrix_results_review_created"), False, "results_review_created")
        _expect(review.get("feature_label_matrix_results_review_ready"), False, "results_review_ready")
        _expect(review.get("ready_for_vpa_wyckoff_rule_baseline_candidate"), False, "ready_for_vpa_wyckoff_rule_baseline_candidate")
        _expect(review.get("marketflow_feature_label_matrix_results_review_digest"), "NOT_CREATED", "blocked review digest")
        return {
            "status": MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_VALID,
            "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
            "failure_count": len(review.get("failures", [])),
        }
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_feature_label_matrix_execution_artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED,
        "source_feature_label_matrix_execution_status": execution.MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY,
        "source_feature_label_matrix_execution_scope": execution.FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_label_matrix_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": len(TARGET_UNIVERSE),
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "expected_output_count": 12, "observed_output_count": 12,
        "output_digest_mismatch_count": 0,
        "matrix_row_count": EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "feature_group_count_per_matrix_row": 13,
        "feature_group_reference_count": EXPECTED_FEATURE_GROUP_REFERENCE_COUNT,
        "digest_manifest_self_reference_policy": execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(review.get(field), expected, field)
    for field in (
        "created_offline", "research_only", "operator_review_required",
        "feature_label_matrix_created", "feature_label_matrix_rows_created",
        "feature_label_matrix_execution_performed", "joined_matrix_output_created",
        "feature_label_matrix_results_created", "feature_label_matrix_results_review_created",
        "feature_label_matrix_results_review_ready",
        "ready_for_vpa_wyckoff_rule_baseline_candidate", "output_file_inspection_performed",
        "matrix_rows_jsonl_schema_verified", "matrix_rows_count_verified",
        "per_ticker_matrix_counts_verified", "meta_limitation_verified",
    ):
        _expect(review.get(field), True, field)
    for field in (
        "vpa_wyckoff_rule_baseline_candidate_created", "expectancy_backtest_lab_candidate_created",
        "target_values_inside_feature_bundle", "target_classes_inside_feature_bundle",
        "forward_returns_inside_feature_bundle", "future_data_inside_feature_bundle",
        "prediction_fields_present", "strategy_score_fields_present",
        "trade_recommendation_fields_present", "broker_order_fields_present",
        "provider_payload_fields_present", "api_key_fields_present",
        "backtest_execution_authorized", "backtest_execution_performed",
        "model_training_authorized", "model_training_performed",
        "metric_computation_authorized", "metric_computation_performed",
        "strategy_scoring_performed", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "feature_label_matrix_execution_rerun_performed",
        "target_generation_execution_rerun_performed",
        "target_generation_results_review_rerun_performed",
        "signal_feature_generation_execution_rerun_performed",
        "signal_feature_results_review_rerun_performed",
        "matrix_candidate_creation_rerun_performed", "matrix_candidate_review_rerun_performed",
        "matrix_approval_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ):
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    local = review.get("local_output_digests")
    if not isinstance(local, dict) or list(local) != EXPECTED_OUTPUT_FILENAMES:
        raise MarketFlowFeatureLabelMatrixResultsReviewError("local_output_digests mismatch")
    if any(not isinstance(value, str) or len(value) != 64 for value in local.values()):
        raise MarketFlowFeatureLabelMatrixResultsReviewError("local output SHA-256 missing")
    _expect(local["matrix_rows.jsonl"], EXPECTED_SOURCE_MATRIX_ROWS_DIGEST, "matrix rows digest")
    review_fields = {
        "matrix_rows_jsonl_review": "VERIFIED_RESEARCH_ONLY",
        "matrix_schema_review": "VERIFIED", "feature_bundle_schema_review": "VERIFIED",
        "target_profile_schema_review": "VERIFIED", "matrix_coverage_report_review": "VERIFIED",
        "matrix_no_peek_report_review": "VERIFIED",
        "matrix_target_availability_report_review": "VERIFIED",
        "per_ticker_matrix_report_review": "VERIFIED", "meta_limitation_report_review": "VERIFIED",
        "operator_summary_review": "VERIFIED", "digest_manifest_review": "VERIFIED_ZERO_MISMATCHES",
    }
    for field, expected in review_fields.items():
        _expect(review.get(field), expected, field)
    entries = review.get("per_ticker_feature_label_matrix_results_review_entries")
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowFeatureLabelMatrixResultsReviewError("per-ticker review entries mismatch")
    for row in entries:
        _expect(
            row.get("per_ticker_feature_label_matrix_results_review_digest"),
            per_ticker_feature_label_matrix_results_review_digest_v1(row),
            f"{row.get('ticker')} review digest",
        )
    checklist = _review_checklist(review)
    _expect(review.get("review_checklist"), checklist, "review_checklist")
    if any(row["status"] != PASS for row in checklist):
        raise MarketFlowFeatureLabelMatrixResultsReviewError("review checklist contains failures")
    _expect(review.get("review_summary"), _summary(checklist), "review_summary")
    digest = review.get("marketflow_feature_label_matrix_results_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowFeatureLabelMatrixResultsReviewError("review digest missing")
    _expect(digest, marketflow_feature_label_matrix_results_review_digest_v1(review), "review digest")
    return {
        "status": MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_feature_label_matrix_results_review_digest": digest,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "total_checks": review["review_summary"]["total_checks"],
        "passed_checks": review["review_summary"]["passed_checks"],
        "failed_checks": 0, "blocker_count": 0,
    }


def build_marketflow_feature_label_matrix_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the digest-bound matrix results review as Markdown."""
    validation = validate_marketflow_feature_label_matrix_results_review_v1(review)
    sections = [
        ("Feature-Label Matrix Results Review v1", [
            f"Artifact/status/scope: `{review['artifact_kind']}` / `{review['review_status']}` / `{review['review_scope']}`.",
            f"Review digest: `{validation['marketflow_feature_label_matrix_results_review_digest']}`.",
        ]),
        ("Source Feature-Label Matrix Execution", [f"Execution `{EXPECTED_SOURCE_EXECUTION_DIGEST}` was inspected read-only and not rerun."]),
        ("Bound Evidence", [f"Output binding `{EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST}` and rows `{EXPECTED_SOURCE_MATRIX_ROWS_DIGEST}` are bound with the upstream chain."]),
        ("Dataset and Universe", ["`expanded_universe_canonical_dataset_v1`, 11,946 records, ordered twelve-ticker universe; META remains 913."]),
        ("Output Verification", ["All twelve local SHA-256 values, ten ordinary manifest hashes, and both special policies were verified with zero mismatches."]),
        ("Selected Matrix Package", [f"`{execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX}`."]),
        ("Selected Matrix Layout", [f"`{execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE}`."]),
        ("Matrix Rows Review", [f"Streaming validation confirmed {review['matrix_row_count']:,} schema-valid research-only rows."]),
        ("Feature Bundle Review", ["Every row contains exactly thirteen approved feature groups; unavailable features remain null."]),
        ("Target Profile Review", ["All fifteen outcome profiles remain top-level; unavailable outcomes remain null."]),
        ("No-Peek and Leakage Review", ["Target, future, prediction, score, recommendation, order, provider-payload, and credential fields are absent from features."]),
        ("Matrix Coverage Review", [f"{review['available_matrix_row_count']:,} available and {review['unavailable_target_matrix_row_count']:,} unavailable rows; no rows dropped."]),
        ("Target Availability Review", ["All unavailable target tails remain retained with null numeric and class outcomes."]),
        ("Per-Ticker Matrix Report Review", ["Non-META counts are 15,045 each; META is 13,695; all twelve entries are digest-bound."]),
        ("META Limitation Review", ["META's exact 913-record limitation remains preserved without repair, inference, smoothing, or fabrication."]),
        ("Output Digest Manifest", ["Ten file hashes, `SELF_REFERENTIAL_EXECUTION_ARTIFACT`, and `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` are verified."]),
        ("Next Chain", review["next_chain"]), ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['review_summary']['passed_checks']}/{review['review_summary']['total_checks']} checks pass with zero blockers."]),
        ("Guardrails", ["The review only makes a future VPA/Wyckoff candidate ready; it creates no candidate, backtest, model, metric, score, recommendation, acceptance, runtime, or trading authority."]),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_feature_label_matrix_results_review_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
) -> dict:
    """Write validated review JSON and Markdown to an explicit directory."""
    review = build_marketflow_feature_label_matrix_results_review_v1(output_root=output_root)
    validation = validate_marketflow_feature_label_matrix_results_review_v1(review)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_feature_label_matrix_results_review_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowFeatureLabelMatrixResultsReviewError("results-review output already exists")
    json_path.write_bytes(canonical_json_bytes(review))
    markdown_path.write_text(
        build_marketflow_feature_label_matrix_results_review_markdown_v1(review),
        encoding="utf-8", newline="\n",
    )
    return {**validation, "json_path": _path_text(json_path), "markdown_path": _path_text(markdown_path)}
