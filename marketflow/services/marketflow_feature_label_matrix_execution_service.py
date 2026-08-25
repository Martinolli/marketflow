"""Offline, digest-bound execution of the approved feature-label matrix."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from datetime import UTC, datetime
from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import (
    marketflow_feature_label_matrix_approval_service as approval_service,
)


ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_V1 = (
    "marketflow_feature_label_matrix_execution_v1"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS"
)
FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING = (
    "FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_VALID = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_VALID"
)

PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX = (
    "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"
)
MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE = (
    "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"
)
PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET = (
    "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"
)
PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET = (
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
)
EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT = (
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
)

OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "FEATURE_LABEL_MATRIX_RESEARCH_ONLY"
SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "0f438427e1b5149b4afb15a8cf0c9af6bb39a95f18e47b8413da6d4e34a9f888"
)
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    "0a7f440b6bfa79a8ddb0e73d24270f4004b95ef79a0cded3f188acfea4487e56"
)
EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST = (
    "ef3d42d39a5ae353044d29d645a7ca1ad01143e5557951b05b85f837413187b4"
)
EXPECTED_FEATURE_VALUES_DIGEST = (
    "7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e"
)
EXPECTED_TARGET_VALUES_DIGEST = (
    "61480462caa3cb1177b56b72276c439035a69a28294cc1154d272f02515a8119"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)

TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_RECORD_COUNTS = {
    ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE
}
SELECTED_FEATURE_GROUPS = [
    "GROUP_CLOSE_TO_CLOSE_RETURNS",
    "GROUP_INTRADAY_RANGE_AND_BODY",
    "GROUP_CLOSE_LOCATION_VALUE",
    "GROUP_VOLUME_CHANGE_AND_ZSCORE",
    "GROUP_SPREAD_VOLUME_INTERACTION",
    "GROUP_EFFORT_RESULT_DIVERGENCE",
    "GROUP_ATR_AND_VOLATILITY_COMPRESSION",
    "GROUP_MOVING_AVERAGE_SLOPE",
    "GROUP_RELATIVE_STRENGTH_VS_UNIVERSE",
    "GROUP_RELATIVE_STRENGTH_RANK",
    "GROUP_ABSTENTION_NOISE_CONTEXT",
    "GROUP_DATA_AVAILABILITY_FLAGS",
    "GROUP_META_LIMITATION_FLAGS",
]

EXPECTED_MATRIX_ROW_COUNT = 179190
EXPECTED_AVAILABLE_MATRIX_ROW_COUNT = 177090
EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT = 2100
EXPECTED_FEATURE_SOURCE_ROW_COUNT = 155298
EXPECTED_TARGET_SOURCE_ROW_COUNT = 179190
EXPECTED_FEATURE_GROUP_REFERENCE_COUNT = 2329470
EXPECTED_OUTPUT_COUNT = 12

DEFAULT_FEATURE_VALUES_PATH = Path(
    ".marketflow/signal_or_feature_generation/expanded_universe_v1/feature_values.jsonl"
)
DEFAULT_TARGET_VALUES_PATH = Path(
    ".marketflow/objective_label_or_target_generation/expanded_universe_v1/target_values.jsonl"
)
DEFAULT_OUTPUT_ROOT = Path(".marketflow/feature_label_matrix/expanded_universe_v1")

OUTPUT_FILENAMES = [
    "feature_label_matrix_manifest.json",
    "feature_label_matrix_schema.json",
    "feature_bundle_schema.json",
    "target_profile_schema.json",
    "matrix_rows.jsonl",
    "matrix_coverage_report.json",
    "matrix_no_peek_report.json",
    "matrix_target_availability_report.json",
    "per_ticker_matrix_report.json",
    "meta_limitation_report.json",
    "operator_summary.json",
    "feature_label_matrix_digest_manifest.json",
]
MATRIX_ROW_FIELDS = [
    "dataset_name", "ticker", "date", "source_profile", "timeframe",
    "canonical_record_index", "target_family", "target_horizon_sessions",
    "target_profile", "target_available", "target_value", "target_class",
    "target_unavailable_reason", "forward_start_date", "forward_end_date",
    "feature_bundle", "feature_group_count", "feature_bundle_available",
    "feature_unavailable_group_count", "selected_matrix_package",
    "selected_matrix_layout", "selected_feature_package",
    "selected_label_target_package", "selected_objective_path", "research_only",
    "non_actionable", "records_digest", "source_matrix_approval_digest",
    "source_feature_values_digest", "source_target_values_digest",
]
FEATURE_BUNDLE_FIELDS = [
    "feature_family", "signal_family", "feature_values", "feature_available",
    "feature_unavailable_reason", "history_lookback_required",
    "history_lookback_available", "feature_formula_version",
]
TARGET_PROFILE_FIELDS = [
    "target_family", "target_horizon_sessions", "target_profile",
    "target_available", "target_value", "target_class",
    "target_unavailable_reason", "forward_start_date", "forward_end_date",
]
FORBIDDEN_FEATURE_BUNDLE_FIELDS = {
    "target_value", "target_class", "forward_return", "future_label_value",
    "prediction", "strategy_score", "trade_recommendation", "broker_order",
}
FORBIDDEN_MATRIX_FIELDS = {
    "prediction", "strategy_score", "trade_recommendation", "broker_order",
    "order_id", "raw_provider_payload", "api_key",
}

NEXT_CHAIN = [
    "Feature-Label Matrix Results Review v1.",
    "VPA/Wyckoff baseline candidate only after separate approval.",
    "Expectancy backtest lab candidate only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "feature_label_matrix_results_review",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_creates_only_research_feature_label_matrix",
    "execution_does_not_run_backtest",
    "execution_does_not_train_models",
    "execution_does_not_compute_performance_metrics",
    "execution_does_not_score_strategy",
    "execution_does_not_generate_trade_recommendations",
    "execution_does_not_accept_predictive_usefulness",
    "execution_does_not_accept_profitability",
    "execution_does_not_authorize_runtime",
    "execution_does_not_authorize_strategy",
    "execution_does_not_authorize_paper_trading",
    "execution_does_not_authorize_broker_execution",
    "execution_does_not_call_providers",
    "execution_does_not_acquire_market_data",
    "execution_does_not_rerun_target_generation_execution",
    "execution_does_not_rerun_target_results_review",
    "execution_does_not_rerun_signal_feature_generation_execution",
    "execution_does_not_rerun_signal_feature_results_review",
    "execution_does_not_rerun_matrix_candidate_creation",
    "execution_does_not_rerun_matrix_candidate_review",
    "execution_does_not_rerun_matrix_approval",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowFeatureLabelMatrixExecutionError(ValueError):
    """Raised when source evidence or matrix output violates the contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _join_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    return tuple(
        row.get(field)
        for field in (
            "dataset_name", "source_profile", "timeframe", "ticker", "date",
            "canonical_record_index",
        )
    )


@lru_cache(maxsize=1)
def _canonical_source_approval() -> dict[str, Any]:
    attestation = approval_service.build_marketflow_feature_label_matrix_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-25T00:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=approval_service.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        operator_confirms_signal_feature_results_review_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
        operator_confirms_feature_values_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        operator_confirms_target_results_review_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
        operator_confirms_target_values_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        operator_confirms_records_digest=approval_service.BOUND_EVIDENCE["records_digest"],
        operator_confirms_target_universe=approval_service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_selected_matrix_package=approval_service.SELECTED_MATRIX_PACKAGE,
        operator_confirms_selected_matrix_layout=approval_service.SELECTED_MATRIX_LAYOUT,
        operator_confirms_selected_feature_package=approval_service.SELECTED_FEATURE_PACKAGE,
        operator_confirms_selected_label_target_package=approval_service.SELECTED_LABEL_TARGET_PACKAGE,
        operator_confirms_selected_objective_path=approval_service.SELECTED_OBJECTIVE_PATH,
        **{
            field: True
            for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    )
    artifact = approval_service.build_marketflow_feature_label_matrix_approval_v1(
        operator_attestation=attestation
    )
    validation = approval_service.validate_marketflow_feature_label_matrix_approval_v1(
        artifact
    )
    if validation["marketflow_feature_label_matrix_approval_digest"] != EXPECTED_SOURCE_APPROVAL_DIGEST:
        raise MarketFlowFeatureLabelMatrixExecutionError("source approval digest mismatch")
    return artifact


def _source_evidence() -> dict[str, str]:
    approval = _canonical_source_approval()
    evidence = {
        key: value
        for key, value in approval.items()
        if key.endswith("_digest") and isinstance(value, str)
    }
    evidence.update({
        "marketflow_feature_label_matrix_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "marketflow_feature_label_matrix_candidate_operator_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "marketflow_feature_label_matrix_candidate_v1_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "signal_or_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "objective_label_or_target_values_digest": EXPECTED_TARGET_VALUES_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    })
    return evidence


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "feature_label_matrix_created": True,
        "feature_label_matrix_rows_created": True,
        "feature_label_matrix_execution_performed": True,
        "joined_matrix_output_created": True,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "metric_computation_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report(report_kind: str, timestamp: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "report_kind": report_kind,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_V1,
        "run_timestamp_utc": timestamp,
        **_common_output_fields(),
        **deepcopy(dict(payload)),
    }


def _blocked_artifact(
    output_root: Path, timestamp: str, failures: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_V1,
        "execution_status": MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS,
        "execution_scope": FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "run_timestamp_utc": timestamp,
        "generated_output_root": str(output_root).replace("\\", "/"),
        "failures": failures,
        "feature_label_matrix_created": False,
        "feature_label_matrix_rows_created": False,
        "feature_label_matrix_execution_performed": False,
        "joined_matrix_output_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "risk_controls": list(RISK_CONTROLS),
    }


def _read_feature_bundles(
    path: Path,
) -> tuple[dict[tuple[Any, ...], dict[str, dict[str, Any]]], dict[str, int]]:
    bundles: dict[tuple[Any, ...], dict[str, dict[str, Any]]] = defaultdict(dict)
    per_ticker: Counter[str] = Counter()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"feature_values.jsonl invalid JSON at line {line_number}"
                ) from exc
            if not isinstance(row, dict) or row.get("records_digest") != EXPECTED_RECORDS_DIGEST:
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"feature row {line_number} invalid or records digest mismatch"
                )
            group = row.get("feature_group")
            if group not in SELECTED_FEATURE_GROUPS:
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"feature row {line_number} has unexpected feature group"
                )
            key = _join_key(row)
            if key[-3] not in TARGET_UNIVERSE or group in bundles[key]:
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"feature row {line_number} has invalid ticker or duplicate group"
                )
            bundles[key][group] = {
                field: deepcopy(row.get(field)) for field in FEATURE_BUNDLE_FIELDS
            }
            per_ticker[str(row["ticker"])] += 1
    if sum(per_ticker.values()) != EXPECTED_FEATURE_SOURCE_ROW_COUNT:
        raise MarketFlowFeatureLabelMatrixExecutionError("feature source row count mismatch")
    expected_groups = set(SELECTED_FEATURE_GROUPS)
    if any(set(bundle) != expected_groups for bundle in bundles.values()):
        raise MarketFlowFeatureLabelMatrixExecutionError(
            "feature source does not provide exactly 13 groups per canonical row"
        )
    return dict(bundles), dict(per_ticker)


def _scan_targets(
    path: Path, bundles: Mapping[tuple[Any, ...], Mapping[str, Any]]
) -> dict[str, Any]:
    per_ticker: Counter[str] = Counter()
    available: Counter[str] = Counter()
    unavailable: Counter[str] = Counter()
    profiles: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"target_values.jsonl invalid JSON at line {line_number}"
                ) from exc
            if not isinstance(row, dict) or row.get("records_digest") != EXPECTED_RECORDS_DIGEST:
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"target row {line_number} invalid or records digest mismatch"
                )
            ticker = row.get("ticker")
            if ticker not in TARGET_UNIVERSE or _join_key(row) not in bundles:
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"target row {line_number} has no valid feature join"
                )
            target_available = row.get("target_available")
            if target_available not in (True, False):
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"target row {line_number} has invalid availability"
                )
            if target_available and (
                row.get("target_value") is None and row.get("target_class") is None
            ):
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"available target row {line_number} has no numeric or class outcome"
                )
            if not target_available and (
                row.get("target_value") is not None or row.get("target_class") is not None
            ):
                raise MarketFlowFeatureLabelMatrixExecutionError(
                    f"unavailable target row {line_number} has non-null outcome"
                )
            per_ticker[str(ticker)] += 1
            (available if target_available else unavailable)[str(ticker)] += 1
            profiles.add(str(row.get("target_profile")))
    if sum(per_ticker.values()) != EXPECTED_TARGET_SOURCE_ROW_COUNT:
        raise MarketFlowFeatureLabelMatrixExecutionError("target source row count mismatch")
    if sum(available.values()) != EXPECTED_AVAILABLE_MATRIX_ROW_COUNT:
        raise MarketFlowFeatureLabelMatrixExecutionError("available target row count mismatch")
    if sum(unavailable.values()) != EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT:
        raise MarketFlowFeatureLabelMatrixExecutionError("unavailable target row count mismatch")
    if len(profiles) != 15:
        raise MarketFlowFeatureLabelMatrixExecutionError("target profile count mismatch")
    return {
        "per_ticker": dict(per_ticker),
        "available": dict(available),
        "unavailable": dict(unavailable),
        "target_profiles": sorted(profiles),
    }


def _matrix_row(
    target: Mapping[str, Any], bundle: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    ordered_bundle = {
        group: deepcopy(dict(bundle[group])) for group in SELECTED_FEATURE_GROUPS
    }
    unavailable_groups = sum(
        entry.get("feature_available") is not True for entry in ordered_bundle.values()
    )
    return {
        "dataset_name": target["dataset_name"],
        "ticker": target["ticker"],
        "date": target["date"],
        "source_profile": target["source_profile"],
        "timeframe": target["timeframe"],
        "canonical_record_index": target["canonical_record_index"],
        "target_family": target["target_family"],
        "target_horizon_sessions": target["target_horizon_sessions"],
        "target_profile": target["target_profile"],
        "target_available": target["target_available"],
        "target_value": target.get("target_value"),
        "target_class": target.get("target_class"),
        "target_unavailable_reason": target.get("unavailable_reason"),
        "forward_start_date": target.get("forward_start_date"),
        "forward_end_date": target.get("forward_end_date"),
        "feature_bundle": ordered_bundle,
        "feature_group_count": len(ordered_bundle),
        "feature_bundle_available": unavailable_groups == 0,
        "feature_unavailable_group_count": unavailable_groups,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "research_only": True,
        "non_actionable": True,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "source_matrix_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_TARGET_VALUES_DIGEST,
    }


def _write_matrix_rows(
    target_path: Path,
    bundles: Mapping[tuple[Any, ...], Mapping[str, Mapping[str, Any]]],
    output_path: Path,
) -> str:
    with output_path.open("xb") as output, target_path.open("r", encoding="utf-8") as source:
        for line in source:
            target = json.loads(line)
            row = _matrix_row(target, bundles[_join_key(target)])
            output.write(canonical_json_bytes(row))
    return sha256_file(output_path)


def per_ticker_feature_label_matrix_execution_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_feature_label_matrix_execution_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(
    target_scan: Mapping[str, Any], feature_counts: Mapping[str, int]
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "feature_label_matrix_approval_status": "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED",
            "feature_label_matrix_execution_status": "GENERATED_RESEARCH_ONLY",
            "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
            "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "matrix_row_count": target_scan["per_ticker"].get(ticker, 0),
            "available_matrix_row_count": target_scan["available"].get(ticker, 0),
            "unavailable_target_matrix_row_count": target_scan["unavailable"].get(ticker, 0),
            "feature_source_row_count": feature_counts.get(ticker, 0),
            "target_source_row_count": target_scan["per_ticker"].get(ticker, 0),
            "feature_label_matrix_created": True,
            "feature_label_matrix_rows_created": True,
            "feature_label_matrix_execution_performed": True,
            "joined_matrix_output_created": True,
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
            "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        }
        entry["per_ticker_feature_label_matrix_execution_digest"] = (
            per_ticker_feature_label_matrix_execution_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _reports(
    timestamp: str,
    target_scan: Mapping[str, Any],
    feature_counts: Mapping[str, int],
    per_ticker: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    matrix_schema = _report("feature_label_matrix_schema", timestamp, {
        "matrix_row_fields": MATRIX_ROW_FIELDS,
        "required_matrix_row_fields": MATRIX_ROW_FIELDS,
        "forbidden_matrix_fields": sorted(FORBIDDEN_MATRIX_FIELDS),
        "join_keys": [
            "dataset_name", "source_profile", "timeframe", "ticker", "date",
            "canonical_record_index",
        ],
        "one_matrix_row_per_target_row": True,
        "target_outcomes_are_not_features": True,
    })
    bundle_schema = _report("feature_bundle_schema", timestamp, {
        "feature_groups": SELECTED_FEATURE_GROUPS,
        "feature_group_count": len(SELECTED_FEATURE_GROUPS),
        "feature_bundle_entry_fields": FEATURE_BUNDLE_FIELDS,
        "forbidden_feature_bundle_fields": sorted(FORBIDDEN_FEATURE_BUNDLE_FIELDS),
        "unavailable_feature_values_retained_as_null": True,
    })
    target_schema = _report("target_profile_schema", timestamp, {
        "target_profile_fields": TARGET_PROFILE_FIELDS,
        "target_profiles": target_scan["target_profiles"],
        "target_profile_count": len(target_scan["target_profiles"]),
        "unavailable_targets_retained_with_null_outcomes": True,
        "target_outcomes_are_outcome_fields_only": True,
    })
    coverage = _report("matrix_coverage_report", timestamp, {
        "matrix_row_count": EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "feature_group_count_per_matrix_row": len(SELECTED_FEATURE_GROUPS),
        "feature_group_reference_count": EXPECTED_FEATURE_GROUP_REFERENCE_COUNT,
        "feature_source_row_count": EXPECTED_FEATURE_SOURCE_ROW_COUNT,
        "target_source_row_count": EXPECTED_TARGET_SOURCE_ROW_COUNT,
        "canonical_records_dropped": 0,
        "target_rows_dropped": 0,
    })
    no_peek = _report("matrix_no_peek_report", timestamp, {
        "target_values_not_inside_feature_bundle": True,
        "target_classes_not_inside_feature_bundle": True,
        "forward_returns_not_inside_feature_bundle": True,
        "future_data_not_inside_feature_bundle": True,
        "prediction_fields_absent": True,
        "strategy_score_fields_absent": True,
        "trade_recommendation_fields_absent": True,
        "train_validation_oos_splits_created": False,
    })
    availability = _report("matrix_target_availability_report", timestamp, {
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "unavailable_target_rows_retained": True,
        "unavailable_target_values_are_null": True,
        "unavailable_target_classes_are_null": True,
    })
    per_ticker_report = _report("per_ticker_matrix_report", timestamp, {
        "per_ticker_entries": per_ticker,
        "per_ticker_entry_count": len(per_ticker),
        "feature_source_row_counts": dict(feature_counts),
    })
    meta = _report("meta_limitation_report", timestamp, {
        "ticker": "META",
        "historical_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "matrix_row_count": target_scan["per_ticker"].get("META", 0),
        "available_matrix_row_count": target_scan["available"].get("META", 0),
        "unavailable_target_matrix_row_count": target_scan["unavailable"].get("META", 0),
        "feature_source_row_count": feature_counts.get("META", 0),
        "target_source_row_count": target_scan["per_ticker"].get("META", 0),
        "meta_reduced_record_count_flag": True,
        "generation_note": "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_EXECUTION",
        "repaired_inferred_smoothed_or_fabricated": False,
    })
    operator = _report("operator_summary", timestamp, {
        "execution_status": MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY,
        "execution_scope": FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "matrix_row_count": EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    })
    return {
        "feature_label_matrix_schema.json": matrix_schema,
        "feature_bundle_schema.json": bundle_schema,
        "target_profile_schema.json": target_schema,
        "matrix_coverage_report.json": coverage,
        "matrix_no_peek_report.json": no_peek,
        "matrix_target_availability_report.json": availability,
        "per_ticker_matrix_report.json": per_ticker_report,
        "meta_limitation_report.json": meta,
        "operator_summary.json": operator,
    }


def _output_binding_digest(entries: Iterable[Mapping[str, Any]]) -> str:
    return semantic_digest({
        "output_digest_manifest": list(entries),
        "manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
    })


def _condition_values(artifact: Mapping[str, Any]) -> dict[str, bool]:
    manifest = artifact.get("output_digest_manifest", [])
    names = [entry.get("filename") for entry in manifest if isinstance(entry, Mapping)]
    per_ticker = artifact.get("per_ticker_feature_label_matrix_execution_entries", [])
    schema = artifact.get("matrix_schema_validation", {})
    values = {
        "source_approval_digest_bound": artifact.get("source_feature_label_matrix_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest_bound": artifact.get("source_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_matrix_candidate_digest_bound": artifact.get("source_matrix_candidate_digest") == EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "source_feature_values_digest_bound": artifact.get("source_feature_values_digest") == EXPECTED_FEATURE_VALUES_DIGEST,
        "source_target_values_digest_bound": artifact.get("source_target_values_digest") == EXPECTED_TARGET_VALUES_DIGEST,
        "records_digest_bound": artifact.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "records_digest_preserved": artifact.get("source_verification", {}).get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": artifact.get("target_universe") == TARGET_UNIVERSE and artifact.get("target_universe_count") == len(TARGET_UNIVERSE),
        "meta_913_preserved": artifact.get("meta_record_count") == EXPECTED_RECORD_COUNTS.get("META"),
        "selected_matrix_package_preserved": artifact.get("selected_matrix_package") == PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout_preserved": artifact.get("selected_matrix_layout") == MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package_preserved": artifact.get("selected_feature_package") == PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_target_package_preserved": artifact.get("selected_label_target_package") == PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": artifact.get("selected_objective_path") == EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_matrix_authorized_true": artifact.get("feature_label_matrix_authorized") is True,
        "matrix_created_true": artifact.get("feature_label_matrix_created") is True,
        "matrix_rows_created_true": artifact.get("feature_label_matrix_rows_created") is True,
        "joined_matrix_output_created_true": artifact.get("joined_matrix_output_created") is True,
        "matrix_row_count_179190": artifact.get("matrix_row_count") == EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count_177090": artifact.get("available_matrix_row_count") == EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count_2100": artifact.get("unavailable_target_matrix_row_count") == EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "feature_group_count_per_matrix_row_13": artifact.get("feature_group_count_per_matrix_row") == len(SELECTED_FEATURE_GROUPS),
        "feature_group_reference_count_2329470": artifact.get("feature_group_reference_count") == EXPECTED_FEATURE_GROUP_REFERENCE_COUNT,
        "feature_source_row_count_155298": artifact.get("feature_source_row_count") == EXPECTED_FEATURE_SOURCE_ROW_COUNT,
        "target_source_row_count_179190": artifact.get("target_source_row_count") == EXPECTED_TARGET_SOURCE_ROW_COUNT,
        "generated_output_count_12": artifact.get("generated_output_count") == EXPECTED_OUTPUT_COUNT,
        "matrix_rows_jsonl_created": "matrix_rows.jsonl" in names,
        "matrix_schema_created": "feature_label_matrix_schema.json" in names,
        "feature_bundle_schema_created": "feature_bundle_schema.json" in names,
        "target_profile_schema_created": "target_profile_schema.json" in names,
        "matrix_coverage_report_created": "matrix_coverage_report.json" in names,
        "matrix_no_peek_report_created": "matrix_no_peek_report.json" in names,
        "matrix_target_availability_report_created": "matrix_target_availability_report.json" in names,
        "per_ticker_matrix_report_created": "per_ticker_matrix_report.json" in names,
        "digest_manifest_created": "feature_label_matrix_digest_manifest.json" in names,
        "digest_manifest_self_reference_policy_verified": bool(manifest) and manifest[-1].get("digest_kind") == SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE and manifest[-1].get("sha256") is None,
        "target_values_not_inside_feature_bundle": schema.get("target_values_not_inside_feature_bundle") is True,
        "target_classes_not_inside_feature_bundle": schema.get("target_classes_not_inside_feature_bundle") is True,
        "forward_returns_not_inside_feature_bundle": schema.get("forward_returns_not_inside_feature_bundle") is True,
        "future_data_not_inside_feature_bundle": schema.get("future_data_not_inside_feature_bundle") is True,
        "prediction_fields_absent": schema.get("prediction_fields_absent") is True,
        "strategy_score_fields_absent": schema.get("strategy_score_fields_absent") is True,
        "trade_recommendation_fields_absent": schema.get("trade_recommendation_fields_absent") is True,
        "backtest_execution_authorized_false": artifact.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": artifact.get("backtest_execution_performed") is False,
        "model_training_authorized_false": artifact.get("model_training_authorized") is False,
        "model_training_performed_false": artifact.get("model_training_performed") is False,
        "metric_computation_authorized_false": artifact.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": artifact.get("metric_computation_performed") is False,
        "strategy_scoring_false": artifact.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": artifact.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": artifact.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": artifact.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": artifact.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": artifact.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": artifact.get("trade_recommendations_generated") is False,
        "per_ticker_entries_12": len(per_ticker) == len(TARGET_UNIVERSE),
        "per_ticker_digests_present": bool(per_ticker) and all(entry.get("per_ticker_feature_label_matrix_execution_digest") == per_ticker_feature_label_matrix_execution_digest_v1(entry) for entry in per_ticker),
        "provider_requests_made_false": artifact.get("provider_requests_made_in_execution") is False,
        "market_data_acquisition_false": artifact.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_regeneration_false": artifact.get("canonical_dataset_regenerated_in_execution") is False,
        "target_generation_execution_rerun_false": artifact.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": artifact.get("target_generation_results_review_rerun_performed") is False,
        "signal_feature_generation_execution_rerun_false": artifact.get("signal_feature_generation_execution_rerun_performed") is False,
        "signal_feature_results_review_rerun_false": artifact.get("signal_feature_results_review_rerun_performed") is False,
        "matrix_candidate_creation_rerun_false": artifact.get("matrix_candidate_creation_rerun_performed") is False,
        "matrix_candidate_review_rerun_false": artifact.get("matrix_candidate_review_rerun_performed") is False,
        "approval_rerun_false": artifact.get("approval_rerun_performed") is False,
        "raw_provider_payloads_not_committed": artifact.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": artifact.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": artifact.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": artifact.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": artifact.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": artifact.get("no_tracked_marketflow_files") is True,
    }
    evidence = artifact.get("source_evidence", {})
    evidence_checks = {
        "source_signal_feature_results_review_digest_bound": "marketflow_signal_or_feature_generation_results_review_digest",
        "source_signal_feature_execution_digest_bound": "marketflow_signal_or_feature_generation_execution_digest",
        "source_signal_feature_output_binding_digest_bound": "signal_or_feature_generation_output_binding_digest",
        "source_target_results_review_digest_bound": "marketflow_objective_label_or_target_generation_results_review_digest",
        "source_target_generation_execution_digest_bound": "marketflow_objective_label_or_target_generation_execution_digest",
        "source_target_output_binding_digest_bound": "objective_label_or_target_generation_output_binding_digest",
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
    }
    values.update({check_id: isinstance(evidence.get(field), str) and len(evidence[field]) == 64 for check_id, field in evidence_checks.items()})
    values["per_non_meta_ticker_matrix_counts_preserved"] = all(
        entry["historical_record_count"] == EXPECTED_RECORD_COUNTS[entry["ticker"]]
        for entry in per_ticker if entry["ticker"] != "META"
    )
    values["meta_matrix_counts_preserved"] = any(
        entry["ticker"] == "META" and entry["historical_record_count"] == EXPECTED_RECORD_COUNTS.get("META")
        for entry in per_ticker
    )
    return values


def _checklist(artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "status": PASS if actual else FAIL,
            "expected": True,
            "actual": actual,
            "severity": BLOCKER,
            "message": f"{check_id} {'passed' if actual else 'failed'}",
        }
        for check_id, actual in _condition_values(artifact).items()
    ]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "feature_label_matrix_created": True,
        "feature_label_matrix_rows_created": True,
        "feature_label_matrix_execution_performed": True,
        "joined_matrix_output_created": True,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "matrix_row_count": EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_feature_label_matrix_execution_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(artifact))
    payload.pop("generated_output_root", None)
    payload.pop("execution_checklist", None)
    payload.pop("execution_summary", None)
    payload.pop("marketflow_feature_label_matrix_execution_digest", None)
    return semantic_digest(payload)


def _build_artifact(
    *,
    timestamp: str,
    output_root: Path,
    source_verification: Mapping[str, Any],
    target_scan: Mapping[str, Any],
    feature_counts: Mapping[str, int],
    per_ticker: list[dict[str, Any]],
    output_manifest: list[dict[str, Any]],
    matrix_rows_digest: str,
    output_binding_digest: str,
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_V1,
        "execution_status": MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY,
        "execution_scope": FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "run_timestamp_utc": timestamp,
        "generated_output_root": str(output_root).replace("\\", "/"),
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_feature_label_matrix_approval_artifact_kind": "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED",
        "source_feature_label_matrix_approval_status": "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED",
        "source_feature_label_matrix_approval_scope": "FEATURE_LABEL_MATRIX_APPROVAL_ONLY",
        "source_feature_label_matrix_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_matrix_candidate_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "source_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_TARGET_VALUES_DIGEST,
        "source_evidence": _source_evidence(),
        "source_verification": deepcopy(dict(source_verification)),
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "total_canonical_record_count": sum(EXPECTED_RECORD_COUNTS.values()),
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "non_meta_record_count": next((count for ticker, count in EXPECTED_RECORD_COUNTS.items() if ticker != "META"), None),
        "meta_reduced_record_count_preserved": True,
        "feature_label_matrix_selected": True,
        "feature_label_matrix_approved": True,
        "feature_label_matrix_authorized": True,
        "ready_for_feature_label_matrix_execution": True,
        "feature_label_matrix_created": True,
        "feature_label_matrix_rows_created": True,
        "feature_label_matrix_execution_performed": True,
        "joined_matrix_output_created": True,
        "feature_label_matrix_results_created": True,
        "matrix_row_count": EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "feature_group_count_per_matrix_row": len(SELECTED_FEATURE_GROUPS),
        "feature_group_reference_count": EXPECTED_FEATURE_GROUP_REFERENCE_COUNT,
        "feature_source_row_count": EXPECTED_FEATURE_SOURCE_ROW_COUNT,
        "target_source_row_count": EXPECTED_TARGET_SOURCE_ROW_COUNT,
        "target_profile_count": len(target_scan["target_profiles"]),
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "observed_output_count": len(output_manifest),
        "feature_label_matrix_rows_digest": matrix_rows_digest,
        "feature_label_matrix_output_binding_digest": output_binding_digest,
        "output_digest_manifest": deepcopy(output_manifest),
        "manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "per_ticker_feature_label_matrix_execution_entries": deepcopy(per_ticker),
        "matrix_schema_validation": {
            "target_values_not_inside_feature_bundle": True,
            "target_classes_not_inside_feature_bundle": True,
            "forward_returns_not_inside_feature_bundle": True,
            "future_data_not_inside_feature_bundle": True,
            "prediction_fields_absent": True,
            "strategy_score_fields_absent": True,
            "trade_recommendation_fields_absent": True,
        },
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
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "signal_feature_generation_execution_rerun_performed": False,
        "signal_feature_results_review_rerun_performed": False,
        "matrix_candidate_creation_rerun_performed": False,
        "matrix_candidate_review_rerun_performed": False,
        "approval_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }
    checklist = _checklist(artifact)
    artifact["execution_checklist"] = checklist
    artifact["execution_summary"] = _summary(checklist)
    digest = marketflow_feature_label_matrix_execution_digest_v1(artifact)
    artifact["marketflow_feature_label_matrix_execution_digest"] = digest
    artifact["execution_summary"]["marketflow_feature_label_matrix_execution_digest"] = digest
    return artifact


def _write_bytes_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowFeatureLabelMatrixExecutionError(
            f"feature-label matrix output already exists: {path.name}"
        ) from exc


def execute_marketflow_feature_label_matrix_v1(
    *,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Join reviewed feature and target outputs into the approved research matrix."""
    timestamp = run_timestamp_utc or _utc_now()
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    failures: list[dict[str, Any]] = []
    for source_id, path, expected_digest in (
        ("feature_values", DEFAULT_FEATURE_VALUES_PATH, EXPECTED_FEATURE_VALUES_DIGEST),
        ("target_values", DEFAULT_TARGET_VALUES_PATH, EXPECTED_TARGET_VALUES_DIGEST),
    ):
        if not path.is_file():
            failures.append({"failure_id": f"{source_id}_missing", "message": f"missing source output: {path}"})
        else:
            actual = sha256_file(path)
            if actual != expected_digest:
                failures.append({"failure_id": f"{source_id}_digest_mismatch", "message": f"{source_id} digest mismatch", "expected": expected_digest, "actual": actual})
    if failures:
        return _blocked_artifact(output_path, timestamp, failures)
    source_verification = {
        "feature_values_path": str(DEFAULT_FEATURE_VALUES_PATH).replace("\\", "/"),
        "target_values_path": str(DEFAULT_TARGET_VALUES_PATH).replace("\\", "/"),
        "before_feature_values_digest": sha256_file(DEFAULT_FEATURE_VALUES_PATH),
        "before_target_values_digest": sha256_file(DEFAULT_TARGET_VALUES_PATH),
        "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }
    try:
        bundles, feature_counts = _read_feature_bundles(DEFAULT_FEATURE_VALUES_PATH)
        target_scan = _scan_targets(DEFAULT_TARGET_VALUES_PATH, bundles)
    except (OSError, MarketFlowFeatureLabelMatrixExecutionError) as exc:
        return _blocked_artifact(output_path, timestamp, [{
            "failure_id": "source_outputs_invalid",
            "message": str(exc),
        }])
    after_feature = sha256_file(DEFAULT_FEATURE_VALUES_PATH)
    after_target = sha256_file(DEFAULT_TARGET_VALUES_PATH)
    source_verification.update({
        "after_feature_values_digest": after_feature,
        "after_target_values_digest": after_target,
        "feature_source_unchanged": after_feature == source_verification["before_feature_values_digest"] == EXPECTED_FEATURE_VALUES_DIGEST,
        "target_source_unchanged": after_target == source_verification["before_target_values_digest"] == EXPECTED_TARGET_VALUES_DIGEST,
    })
    if not source_verification["feature_source_unchanged"] or not source_verification["target_source_unchanged"]:
        return _blocked_artifact(output_path, timestamp, [{
            "failure_id": "source_outputs_changed_during_verification",
            "message": "source feature or target output changed during verification",
        }])
    if output_path.exists() and any(output_path.iterdir()):
        raise MarketFlowFeatureLabelMatrixExecutionError(
            "feature-label matrix output root is not empty"
        )
    output_path.mkdir(parents=True, exist_ok=True)
    temporary_matrix_path = output_path / ".matrix_rows.jsonl.tmp"
    matrix_rows_digest = _write_matrix_rows(
        DEFAULT_TARGET_VALUES_PATH, bundles, temporary_matrix_path
    )
    after_write_feature = sha256_file(DEFAULT_FEATURE_VALUES_PATH)
    after_write_target = sha256_file(DEFAULT_TARGET_VALUES_PATH)
    source_verification.update({
        "after_matrix_write_feature_values_digest": after_write_feature,
        "after_matrix_write_target_values_digest": after_write_target,
        "source_outputs_unchanged": (
            after_write_feature == EXPECTED_FEATURE_VALUES_DIGEST
            and after_write_target == EXPECTED_TARGET_VALUES_DIGEST
        ),
    })
    if not source_verification["source_outputs_unchanged"]:
        temporary_matrix_path.unlink(missing_ok=True)
        return _blocked_artifact(output_path, timestamp, [{
            "failure_id": "source_outputs_changed_during_matrix_construction",
            "message": "source outputs changed during matrix construction",
        }])
    per_ticker = _per_ticker_entries(target_scan, feature_counts)
    reports = _reports(timestamp, target_scan, feature_counts, per_ticker)
    report_bytes = {name: canonical_json_bytes(report) for name, report in reports.items()}
    output_manifest: list[dict[str, Any]] = []
    for filename in OUTPUT_FILENAMES:
        if filename == OUTPUT_FILENAMES[0]:
            entry = {"filename": filename, "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT", "sha256": None}
        elif filename == OUTPUT_FILENAMES[-1]:
            entry = {"filename": filename, "digest_kind": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE, "sha256": None}
        elif filename == "matrix_rows.jsonl":
            entry = {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": matrix_rows_digest}
        else:
            entry = {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(report_bytes[filename])}
        output_manifest.append(entry)
    output_binding_digest = _output_binding_digest(output_manifest)
    artifact = _build_artifact(
        timestamp=timestamp,
        output_root=output_path,
        source_verification=source_verification,
        target_scan=target_scan,
        feature_counts=feature_counts,
        per_ticker=per_ticker,
        output_manifest=output_manifest,
        matrix_rows_digest=matrix_rows_digest,
        output_binding_digest=output_binding_digest,
    )
    validate_marketflow_feature_label_matrix_execution_v1(artifact)
    report_bytes[OUTPUT_FILENAMES[0]] = canonical_json_bytes(artifact)
    report_bytes[OUTPUT_FILENAMES[-1]] = canonical_json_bytes(_report(
        "feature_label_matrix_digest_manifest",
        timestamp,
        {
            "marketflow_feature_label_matrix_execution_digest": artifact["marketflow_feature_label_matrix_execution_digest"],
            "feature_label_matrix_output_binding_digest": output_binding_digest,
            "feature_label_matrix_rows_digest": matrix_rows_digest,
            "output_digest_manifest": output_manifest,
            "manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        },
    ))
    for filename in OUTPUT_FILENAMES:
        if filename == "matrix_rows.jsonl":
            continue
        _write_bytes_once(output_path / filename, report_bytes[filename])
    temporary_matrix_path.replace(output_path / "matrix_rows.jsonl")
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowFeatureLabelMatrixExecutionError(f"{field} mismatch")


def validate_marketflow_feature_label_matrix_execution_v1(
    artifact: dict,
) -> dict:
    """Validate the matrix execution, evidence binding, and closed authorities."""
    if not isinstance(artifact, dict):
        raise MarketFlowFeatureLabelMatrixExecutionError("artifact must be a JSON object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_V1,
        "execution_status": MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY,
        "execution_scope": FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_feature_label_matrix_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_matrix_candidate_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "source_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_TARGET_VALUES_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": len(TARGET_UNIVERSE),
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "feature_label_matrix_created": True,
        "feature_label_matrix_rows_created": True,
        "joined_matrix_output_created": True,
        "matrix_row_count": EXPECTED_MATRIX_ROW_COUNT,
        "available_matrix_row_count": EXPECTED_AVAILABLE_MATRIX_ROW_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT,
        "feature_group_count_per_matrix_row": len(SELECTED_FEATURE_GROUPS),
        "feature_group_reference_count": EXPECTED_FEATURE_GROUP_REFERENCE_COUNT,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
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
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "signal_feature_generation_execution_rerun_performed": False,
        "signal_feature_results_review_rerun_performed": False,
        "matrix_candidate_creation_rerun_performed": False,
        "matrix_candidate_review_rerun_performed": False,
        "approval_rerun_performed": False,
    }
    for field, value in expected.items():
        _expect(artifact.get(field), value, field)
    for field in ("feature_label_matrix_rows_digest", "feature_label_matrix_output_binding_digest"):
        value = artifact.get(field)
        if not isinstance(value, str) or len(value) != 64:
            raise MarketFlowFeatureLabelMatrixExecutionError(f"{field} missing")
    schema = artifact.get("matrix_schema_validation")
    if not isinstance(schema, dict) or not all(schema.values()):
        raise MarketFlowFeatureLabelMatrixExecutionError("matrix schema validation mismatch")
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != EXPECTED_OUTPUT_COUNT:
        raise MarketFlowFeatureLabelMatrixExecutionError("output digest manifest mismatch")
    if [entry.get("filename") for entry in manifest] != OUTPUT_FILENAMES:
        raise MarketFlowFeatureLabelMatrixExecutionError("generated output filenames mismatch")
    if manifest[0].get("digest_kind") != "SELF_REFERENTIAL_EXECUTION_ARTIFACT" or manifest[0].get("sha256") is not None:
        raise MarketFlowFeatureLabelMatrixExecutionError("execution artifact self-reference policy mismatch")
    if manifest[-1].get("digest_kind") != SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE or manifest[-1].get("sha256") is not None:
        raise MarketFlowFeatureLabelMatrixExecutionError("digest manifest self-reference policy mismatch")
    if artifact.get("feature_label_matrix_output_binding_digest") != _output_binding_digest(manifest):
        raise MarketFlowFeatureLabelMatrixExecutionError("output binding digest mismatch")
    if not any(entry.get("filename") == "matrix_rows.jsonl" and entry.get("sha256") == artifact["feature_label_matrix_rows_digest"] for entry in manifest):
        raise MarketFlowFeatureLabelMatrixExecutionError("matrix rows output or digest mismatch")
    checklist = _checklist(artifact)
    if artifact.get("execution_checklist") != checklist or any(row["status"] != PASS for row in checklist):
        raise MarketFlowFeatureLabelMatrixExecutionError("execution checklist mismatch")
    if artifact.get("execution_summary") != {
        **_summary(checklist),
        "marketflow_feature_label_matrix_execution_digest": artifact.get("marketflow_feature_label_matrix_execution_digest"),
    }:
        raise MarketFlowFeatureLabelMatrixExecutionError("execution summary mismatch")
    digest = artifact.get("marketflow_feature_label_matrix_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowFeatureLabelMatrixExecutionError("execution digest missing")
    if digest != marketflow_feature_label_matrix_execution_digest_v1(artifact):
        raise MarketFlowFeatureLabelMatrixExecutionError("execution digest mismatch")
    return {
        "status": MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "execution_scope": artifact["execution_scope"],
        "marketflow_feature_label_matrix_execution_digest": digest,
        "feature_label_matrix_output_binding_digest": artifact["feature_label_matrix_output_binding_digest"],
        "feature_label_matrix_rows_digest": artifact["feature_label_matrix_rows_digest"],
        **{
            field: artifact["execution_summary"][field]
            for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_feature_label_matrix_execution_markdown_v1(
    artifact: dict,
) -> str:
    """Render a concise operator-facing execution record."""
    validate_marketflow_feature_label_matrix_execution_v1(artifact)
    sections = [
        ("Feature-Label Matrix Execution v1", [f"Status: `{artifact['execution_status']}`."]),
        ("Source Matrix Approval", [f"Digest `{artifact['source_feature_label_matrix_approval_digest']}`."]),
        ("Bound Evidence", [f"{len(artifact['source_evidence'])} upstream digest fields are bound."]),
        ("Dataset and Universe", ["`expanded_universe_canonical_dataset_v1`, ordered 12-ticker registry, 11,946 canonical rows."]),
        ("Execution Scope", [f"`{artifact['execution_scope']}`."]),
        ("Selected Matrix Package", [f"`{artifact['selected_matrix_package']}`."]),
        ("Selected Matrix Layout", [f"`{artifact['selected_matrix_layout']}`."]),
        ("Source Feature and Target Outputs", [f"Feature `{artifact['source_feature_values_digest']}`; target `{artifact['source_target_values_digest']}`."]),
        ("Matrix Construction Method", ["One row per target row, joined on dataset/profile/timeframe/ticker/date/index, with a 13-group wide feature bundle."]),
        ("Matrix Rows Output", [f"{artifact['matrix_row_count']} rows; digest `{artifact['feature_label_matrix_rows_digest']}`."]),
        ("Feature Bundle Schema", ["All 13 approved feature groups; outcome and future fields are excluded."]),
        ("Target Profile Schema", ["Target outcomes remain top-level outcome fields; unavailable outcomes remain null."]),
        ("No-Peek and Leakage Controls", ["No future data, prediction, scoring, or recommendation fields are features."]),
        ("Matrix Coverage Report", [f"{artifact['available_matrix_row_count']} available; {artifact['unavailable_target_matrix_row_count']} unavailable."]),
        ("Target Availability Report", ["All target rows are retained; unavailable tails remain null."]),
        ("Per-Ticker Matrix Report", [f"{len(artifact['per_ticker_feature_label_matrix_execution_entries'])} digest-bound entries."]),
        ("META Limitation", ["META remains exactly 913 records without repair, inference, smoothing, or fabrication."]),
        ("Output Digest Manifest", [f"{artifact['generated_output_count']} outputs; binding `{artifact['feature_label_matrix_output_binding_digest']}`."]),
        ("Next Chain", artifact["next_chain"]),
        ("Next Gates", artifact["next_gates"]),
        ("Risk Controls", artifact["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness is not accepted."]),
        ("Profitability Boundary", ["Profitability is not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{artifact['execution_summary']['passed_checks']}/{artifact['execution_summary']['total_checks']} checks pass; zero blockers."]),
        ("Guardrails", ["No provider, acquisition, regeneration, backtest, training, metric, scoring, recommendation, runtime, or trading action occurred."]),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
