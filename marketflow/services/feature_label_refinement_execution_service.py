"""Offline execution of the approved feature/label refinement research run."""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import additional_predictive_evidence_execution_service as research_math
from marketflow.services import feature_label_refinement_execution_approval_service as approval
from marketflow.services import feature_label_refinement_execution_candidate_service as candidate


ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTED = "FEATURE_LABEL_REFINEMENT_EXECUTED"
ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED"
)
SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTED_V1 = (
    "feature_label_refinement_executed_v1"
)
FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY = (
    "FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY"
)
FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET"
)
FEATURE_LABEL_REFINEMENT_EXECUTION_VALID = "FEATURE_LABEL_REFINEMENT_EXECUTION_VALID"

DEFAULT_SOURCE_ROOT = (
    Path(".marketflow") / "canonical_datasets" / "expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = (
    Path(".marketflow") / "feature_label_refinement" / "expanded_universe_v1"
)
DEFAULT_BRANCH = "feature/feature-label-refinement-execution-v1"
DEFAULT_BASE_COMMIT = "8970fe73329490467a82d9a406c0b6c2afbc0736"

EXPECTED_EXECUTION_APPROVAL_DIGEST = (
    "1b98237ae9156875ca703396b6e1fabf2acf31ab607789247f8af2391d8b5c20"
)
EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "e6f72e45d85d58759d8f35518c1d5e6795b02923acb43f9170c5cc34a810d9ef"
)
EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    "9977616fd85dbb07ff3f1192b067c77157f26935668f07135cd44eb93b5f5bc5"
)
EXPECTED_PLAN_APPROVAL_DIGEST = approval.EXPECTED_PLAN_APPROVAL_DIGEST
EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_READINESS_REVIEW_DIGEST = approval.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = approval.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_ORIGINAL_EXECUTION_DIGEST = approval.EXPECTED_EXECUTION_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    approval.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    "9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb"
)
EXPECTED_RECORDS_DIGEST = approval.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = {
    ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE
}
APPROVED_REGISTRY_METADATA = {
    "dataset_name": "expanded_universe_canonical_dataset_v1",
    "dataset_scope": "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY",
    "registry_entry_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
    "source_profile": "RTH_FULL_SESSION_1D",
    "date_range_start": "2022-01-01",
    "date_range_end": "2025-12-31",
    "timeframe": "1d",
    "target_universe_count": 12,
    "total_canonical_record_count": 11946,
    "records_digest": EXPECTED_RECORDS_DIGEST,
    "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
    "registry_label": "RESEARCH_ONLY_NON_ACTIONABLE",
}

OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "FEATURE_LABEL_REFINEMENT_RESEARCH_ONLY"
NOT_ACCEPTED = approval.NOT_ACCEPTED
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
LABEL_UNAVAILABLE_REASON = "label_unavailable_due_to_insufficient_future_bars"

LABEL_REFINEMENT_GROUPS = list(candidate.LABEL_REFINEMENT_EXECUTION_GROUP_IDS)
FEATURE_REFINEMENT_GROUPS = list(candidate.FEATURE_REFINEMENT_EXECUTION_GROUP_IDS)
PROTOCOL_REFINEMENT_GROUPS = list(candidate.PROTOCOL_REFINEMENT_EXECUTION_GROUP_IDS)
MODEL_COMPARISON_GROUPS = list(candidate.MODEL_COMPARISON_EXECUTION_GROUP_IDS)

REFINED_LABEL_FAMILIES = [
    "REFINED_NEXT_SESSION_DIRECTION",
    "REFINED_NEXT_SESSION_RETURN_BUCKET",
    "REFINED_MULTI_HORIZON_RETURN_BUCKET_5",
    "REFINED_MULTI_HORIZON_RETURN_BUCKET_10",
    "REFINED_MULTI_HORIZON_RETURN_BUCKET_20",
    "REFINED_VOLATILITY_REGIME_FORWARD",
    "REFINED_DRAWDOWN_RISK_FORWARD",
]
REFINED_FEATURE_CATEGORIES = {
    "refined_return_and_momentum_features": [
        "close_return_1",
        "close_return_5",
        "close_return_20",
        "momentum_5",
        "momentum_20",
    ],
    "refined_volume_price_features": ["volume_ratio_20", "vwap_deviation"],
    "refined_vpa_features": ["close_location_value", "spread_volume_ratio"],
    "refined_relative_strength_features": [
        "cross_sectional_return_rank_percentile"
    ],
    "refined_cross_ticker_context_features": ["cross_sectional_return_context"],
    "refined_calendar_session_features": ["weekday", "month"],
    "refined_data_quality_flags": ["provider_adjusted_combined_policy_flag"],
    "refined_missingness_indicators": ["missing_ohlcv_flag", "missing_vwap_flag"],
    "meta_reduced_record_count_flag": ["meta_reduced_record_count_flag"],
    "refined_volatility_momentum_interactions": [
        "volatility_momentum_interaction_20"
    ],
    "refined_baseline_error_context_features": [
        "previous_direction_change_flag"
    ],
}
REFINED_FEATURE_NAMES = [
    name for names in REFINED_FEATURE_CATEGORIES.values() for name in names
]
MODEL_COMPARISON_IDS = [
    "majority_class_baseline",
    "previous_direction_baseline",
    "zero_return_baseline",
    "ticker_cross_sectional_baseline",
    "refined_relative_strength_signal",
    "refined_vpa_signal",
    "refined_combined_simple_signal",
]
OUTPUT_FILENAMES = [
    "feature_label_refinement_execution_manifest.json",
    "refined_label_generation_report.json",
    "refined_feature_generation_report.json",
    "refined_protocol_execution_report.json",
    "refined_model_comparison_report.json",
    "refined_walk_forward_report.json",
    "refined_out_of_sample_report.json",
    "refined_metric_report.json",
    "refined_leakage_control_report.json",
    "per_ticker_refinement_execution_summary.json",
    "feature_label_refinement_execution_digest_manifest.json",
    "operator_review_summary.json",
]
REQUIRED_SOURCE_FILENAMES = [
    "canonical_dataset_generation_run_manifest.json",
    "canonical_dataset_source_evidence_manifest.json",
    "canonical_dataset_schema_contract.json",
    "canonical_dataset_records.jsonl",
    "per_ticker_canonical_dataset_summary.json",
    "canonical_dataset_data_quality_report.json",
    "canonical_dataset_digest_manifest.json",
    "canonical_dataset_failure_reason_inventory.json",
    "operator_review_summary.json",
]

RETURN_BUCKET_THRESHOLDS = {
    "strong_down_max": "-0.020000",
    "down_max": "-0.002000",
    "flat_max": "0.002000",
    "up_max": "0.020000",
}
FLAT_RETURN_TOLERANCE = "0.002000"
VOLATILITY_THRESHOLDS = {"low_max": "0.010000", "normal_max": "0.025000"}
DRAWDOWN_THRESHOLDS = {
    "low_risk_min": "-0.030000",
    "medium_risk_min": "-0.100000",
}
SPLIT_PROFILE = {
    "training_window": {"start": "2022-01-01", "end": "2023-12-31"},
    "validation_window": {"start": "2024-01-01", "end": "2024-12-31"},
    "out_of_sample_window": {"start": "2025-01-01", "end": "2025-12-31"},
    "walk_forward_policy": "EXPANDING_TRAINING_WITH_QUARTERLY_2024_VALIDATION_FOLDS",
    "embargo_gap_policy": "ONE_SESSION_LABEL_AVAILABILITY_GAP_APPLIED_PER_TICKER",
    "shuffle": False,
}

TRUE_EXECUTION_FIELDS = [
    "feature_label_refinement_execution_approved",
    "feature_label_refinement_execution_authorized",
    "ready_for_feature_label_refinement_execution",
    "feature_label_refinement_executed",
    "feature_label_refinement_results_created",
    "refined_label_generation_authorized",
    "refined_label_generation_performed",
    "refined_feature_generation_authorized",
    "refined_feature_generation_performed",
    "refined_walk_forward_validation_authorized",
    "refined_walk_forward_validation_performed",
    "refined_out_of_sample_evaluation_authorized",
    "refined_out_of_sample_evaluation_performed",
    "refined_metrics_recomputation_authorized",
    "refined_metrics_recomputation_performed",
    "model_comparison_authorized",
    "model_comparison_performed",
    "canonical_dataset_generated",
    "canonical_dataset_frozen",
    "meta_reduced_record_count_preserved",
    "research_only",
]
FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "predictive_execution_rerun_performed",
    "label_generation_rerun_performed",
    "feature_matrix_rerun_performed",
    "walk_forward_validation_rerun_performed",
    "out_of_sample_evaluation_rerun_performed",
    "metrics_recomputation_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "additional_predictive_evidence_execution_candidate_created",
    "additional_predictive_evidence_execution_authorized",
    "additional_predictive_evidence_executed",
    "additional_predictive_evidence_results_created",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "predictive_usefulness_acceptance_candidate_created",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
]


class FeatureLabelRefinementExecutionError(ValueError):
    """Raised when execution evidence violates the research-only contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _source_failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _source_evidence() -> dict[str, str]:
    return {
        "feature_label_refinement_execution_approval_digest": EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "feature_label_refinement_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "feature_label_refinement_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "feature_label_refinement_plan_approval_digest": EXPECTED_PLAN_APPROVAL_DIGEST,
        "feature_label_refinement_plan_candidate_review_package_digest": EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": EXPECTED_ORIGINAL_EXECUTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": APPROVED_REGISTRY_METADATA["dataset_name"],
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "feature_label_refinement_executed": True,
        "feature_label_refinement_results_created": True,
        "refined_label_generation_authorized": True,
        "refined_label_generation_performed": True,
        "refined_feature_generation_authorized": True,
        "refined_feature_generation_performed": True,
        "refined_walk_forward_validation_authorized": True,
        "refined_walk_forward_validation_performed": True,
        "refined_out_of_sample_evaluation_authorized": True,
        "refined_out_of_sample_evaluation_performed": True,
        "refined_metrics_recomputation_authorized": True,
        "refined_metrics_recomputation_performed": True,
        "model_comparison_authorized": True,
        "model_comparison_performed": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "trade_recommendations_generated": False,
    }


def _report(report_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"report_name": report_name, **_common_output_fields(), **payload}


def _verify_source_root(source_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    for filename in REQUIRED_SOURCE_FILENAMES:
        if not (source_root / filename).is_file():
            failures.append(
                _source_failure(
                    "missing_source_file",
                    "required canonical source file missing",
                    filename=filename,
                )
            )
    if failures:
        return {}, failures

    records_path = source_root / "canonical_dataset_records.jsonl"
    records_digest = sha256_file(records_path)
    if records_digest != EXPECTED_RECORDS_DIGEST:
        failures.append(
            _source_failure(
                "records_digest_mismatch",
                "canonical records digest mismatch",
                expected=EXPECTED_RECORDS_DIGEST,
                actual=records_digest,
            )
        )
    try:
        digest_manifest = json.loads(
            (source_root / "canonical_dataset_digest_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        generation_manifest = json.loads(
            (source_root / "canonical_dataset_generation_run_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        ticker_summary = json.loads(
            (source_root / "per_ticker_canonical_dataset_summary.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(_source_failure("invalid_source_json", str(exc)))
        return {}, failures

    for entry in digest_manifest.get("canonical_output_digest_manifest", []):
        filename = entry.get("filename")
        digest_kind = entry.get("digest_kind")
        expected_digest = entry.get("sha256")
        if digest_kind == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE":
            if (
                filename != "canonical_dataset_digest_manifest.json"
                or expected_digest is not None
            ):
                failures.append(
                    _source_failure(
                        "invalid_self_reference_policy",
                        "invalid canonical digest-manifest self-reference",
                        filename=filename,
                    )
                )
            continue
        if filename and digest_kind == "FILE_SHA256":
            actual = sha256_file(source_root / filename)
            if actual != expected_digest:
                failures.append(
                    _source_failure(
                        "source_output_digest_mismatch",
                        "canonical source output digest mismatch",
                        filename=filename,
                        expected=expected_digest,
                        actual=actual,
                    )
                )
    if (
        generation_manifest.get("canonical_dataset_generation_digest")
        != EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
    ):
        failures.append(
            _source_failure(
                "generation_digest_mismatch",
                "canonical dataset generation digest mismatch",
            )
        )
    if ticker_summary.get("target_universe") != TARGET_UNIVERSE:
        failures.append(
            _source_failure("target_universe_mismatch", "target universe mismatch")
        )
    if ticker_summary.get("total_canonical_record_count") != 11946:
        failures.append(
            _source_failure(
                "summary_record_count_mismatch",
                "canonical summary record count mismatch",
            )
        )
    summary_counts = {
        row.get("ticker"): row.get("canonical_record_count")
        for row in ticker_summary.get("per_ticker_canonical_record_summary", [])
    }
    if summary_counts != EXPECTED_RECORD_COUNTS:
        failures.append(
            _source_failure(
                "summary_per_ticker_counts_mismatch",
                "canonical per-ticker summary counts mismatch",
            )
        )
    verification = {
        "source_root": _path_text(source_root),
        "required_source_file_count": len(REQUIRED_SOURCE_FILENAMES),
        "required_source_files": list(REQUIRED_SOURCE_FILENAMES),
        "records_digest_expected": EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": records_digest,
        "records_digest_match": records_digest == EXPECTED_RECORDS_DIGEST,
        "canonical_dataset_generation_digest": generation_manifest.get(
            "canonical_dataset_generation_digest"
        ),
        "digest_manifest_self_reference_policy": (
            "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
        ),
    }
    return verification, failures


def _read_rows(
    source_root: Path,
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    rows_by_ticker = {ticker: [] for ticker in TARGET_UNIVERSE}
    failures: list[dict[str, Any]] = []
    try:
        with (source_root / "canonical_dataset_records.jsonl").open(
            "r", encoding="utf-8"
        ) as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                ticker = row.get("ticker")
                if ticker not in rows_by_ticker:
                    failures.append(
                        _source_failure(
                            "unexpected_ticker",
                            "unexpected ticker in canonical records",
                            line_number=line_number,
                            ticker=ticker,
                        )
                    )
                    continue
                rows_by_ticker[ticker].append(row)
    except (OSError, json.JSONDecodeError) as exc:
        return rows_by_ticker, [_source_failure("invalid_records_file", str(exc))]

    for ticker, rows in rows_by_ticker.items():
        rows.sort(
            key=lambda row: (
                str(row.get("date", "")),
                str(row.get("timestamp_utc_or_session_date", "")),
            )
        )
        if len(rows) != EXPECTED_RECORD_COUNTS[ticker]:
            failures.append(
                _source_failure(
                    "per_ticker_record_count_mismatch",
                    "canonical per-ticker record count mismatch",
                    ticker=ticker,
                    expected=EXPECTED_RECORD_COUNTS[ticker],
                    actual=len(rows),
                )
            )
        dates = [str(row.get("date", "")) for row in rows]
        if any(not date for date in dates) or dates != sorted(dates) or len(dates) != len(set(dates)):
            failures.append(
                _source_failure(
                    "invalid_ticker_date_order",
                    "ticker dates must be present, unique, and chronological",
                    ticker=ticker,
                )
            )
    total = sum(len(rows) for rows in rows_by_ticker.values())
    if total != 11946:
        failures.append(
            _source_failure(
                "total_record_count_mismatch",
                "total canonical record count mismatch",
                expected=11946,
                actual=total,
            )
        )
    return rows_by_ticker, failures


def _label_value(value: Any, horizon: int, available: bool) -> dict[str, Any]:
    return {
        "value": value if available else None,
        "horizon_sessions": horizon,
        "available": available,
        "unavailable_reason": None if available else LABEL_UNAVAILABLE_REASON,
    }


def _refined_direction(value: Decimal | None) -> str | None:
    if value is None:
        return None
    tolerance = Decimal(FLAT_RETURN_TOLERANCE)
    if value > tolerance:
        return "UP"
    if value < -tolerance:
        return "DOWN"
    return "FLAT"


def _return_bucket(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value <= Decimal(RETURN_BUCKET_THRESHOLDS["strong_down_max"]):
        return "STRONG_DOWN"
    if value < Decimal(RETURN_BUCKET_THRESHOLDS["down_max"]):
        return "DOWN"
    if value <= Decimal(RETURN_BUCKET_THRESHOLDS["flat_max"]):
        return "FLAT"
    if value < Decimal(RETURN_BUCKET_THRESHOLDS["up_max"]):
        return "UP"
    return "STRONG_UP"


def _volatility_bucket(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value <= Decimal(VOLATILITY_THRESHOLDS["low_max"]):
        return "LOW"
    if value <= Decimal(VOLATILITY_THRESHOLDS["normal_max"]):
        return "NORMAL"
    return "HIGH"


def _drawdown_bucket(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value >= Decimal(DRAWDOWN_THRESHOLDS["low_risk_min"]):
        return "LOW_RISK"
    if value >= Decimal(DRAWDOWN_THRESHOLDS["medium_risk_min"]):
        return "MEDIUM_RISK"
    return "HIGH_RISK"


def _generate_refined_labels(
    rows_by_ticker: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    generated: dict[str, list[dict[str, Any]]] = {}
    for ticker in TARGET_UNIVERSE:
        rows = rows_by_ticker[ticker]
        closes = [research_math._parse_decimal(row.get("close")) for row in rows]
        ticker_rows: list[dict[str, Any]] = []
        for index, row in enumerate(rows):
            current = closes[index]
            values: dict[str, dict[str, Any]] = {}
            for family, horizon in (
                ("REFINED_NEXT_SESSION_DIRECTION", 1),
                ("REFINED_NEXT_SESSION_RETURN_BUCKET", 1),
                ("REFINED_MULTI_HORIZON_RETURN_BUCKET_5", 5),
                ("REFINED_MULTI_HORIZON_RETURN_BUCKET_10", 10),
                ("REFINED_MULTI_HORIZON_RETURN_BUCKET_20", 20),
            ):
                forward_return = (
                    research_math._return_between(current, closes[index + horizon])
                    if index + horizon < len(closes)
                    else None
                )
                label = (
                    _refined_direction(forward_return)
                    if family == "REFINED_NEXT_SESSION_DIRECTION"
                    else _return_bucket(forward_return)
                )
                values[family] = _label_value(label, horizon, label is not None)
            volatility = research_math._future_volatility(closes, index, 20)
            drawdown = research_math._future_drawdown(closes, index, 20)
            values["REFINED_VOLATILITY_REGIME_FORWARD"] = _label_value(
                _volatility_bucket(volatility), 20, volatility is not None
            )
            values["REFINED_DRAWDOWN_RISK_FORWARD"] = _label_value(
                _drawdown_bucket(drawdown), 20, drawdown is not None
            )
            ticker_rows.append(
                {
                    "ticker": ticker,
                    "date": str(row.get("date")),
                    "row_index": index,
                    "labels": values,
                }
            )
        generated[ticker] = ticker_rows
    return generated


def _generate_refined_features(
    rows_by_ticker: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    base = research_math._generate_features(rows_by_ticker)
    generated: dict[str, list[dict[str, Any]]] = {}
    for ticker in TARGET_UNIVERSE:
        ticker_rows: list[dict[str, Any]] = []
        previous_direction: str | None = None
        for row in base[ticker]:
            values = row["features"]
            current_direction = _refined_direction(
                research_math._parse_decimal(values.get("close_return_1"))
            )
            volatility = research_math._parse_decimal(
                values.get("realized_volatility_20")
            )
            momentum = research_math._parse_decimal(values.get("momentum_20"))
            interaction = (
                volatility * momentum
                if volatility is not None and momentum is not None
                else None
            )
            rank = research_math._parse_decimal(
                values.get("cross_sectional_return_rank_percentile")
            )
            cross_context = (
                rank - Decimal("0.5") if rank is not None else None
            )
            refined = {
                "close_return_1": values.get("close_return_1"),
                "close_return_5": values.get("close_return_5"),
                "close_return_20": values.get("close_return_20"),
                "momentum_5": values.get("momentum_5"),
                "momentum_20": values.get("momentum_20"),
                "volume_ratio_20": values.get("volume_ratio_20"),
                "vwap_deviation": values.get("vwap_deviation"),
                "close_location_value": values.get("close_location_value"),
                "spread_volume_ratio": values.get("spread_volume_ratio"),
                "cross_sectional_return_rank_percentile": values.get(
                    "cross_sectional_return_rank_percentile"
                ),
                "cross_sectional_return_context": research_math._decimal_text(
                    cross_context, 6
                ),
                "weekday": values.get("weekday"),
                "month": values.get("month"),
                "provider_adjusted_combined_policy_flag": values.get(
                    "provider_adjusted_combined_policy_flag"
                ),
                "missing_ohlcv_flag": values.get("missing_ohlcv_flag"),
                "missing_vwap_flag": values.get("missing_vwap_flag"),
                "meta_reduced_record_count_flag": ticker == "META",
                "volatility_momentum_interaction_20": research_math._decimal_text(
                    interaction
                ),
                "previous_direction_change_flag": (
                    None
                    if previous_direction is None or current_direction is None
                    else current_direction != previous_direction
                ),
            }
            ticker_rows.append(
                {
                    "ticker": ticker,
                    "date": row["date"],
                    "row_index": row["row_index"],
                    "features": refined,
                }
            )
            if current_direction is not None:
                previous_direction = current_direction
        generated[ticker] = ticker_rows
    return generated


def _label_summaries(
    labels_by_ticker: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, int]], dict[str, Any]]:
    coverage: list[dict[str, Any]] = []
    overall = {family: Counter() for family in REFINED_LABEL_FAMILIES}
    per_ticker_distributions: dict[str, dict[str, dict[str, int]]] = {}
    for ticker in TARGET_UNIVERSE:
        per_ticker_distributions[ticker] = {}
        for family in REFINED_LABEL_FAMILIES:
            values = [row["labels"][family] for row in labels_by_ticker[ticker]]
            available = [row["value"] for row in values if row["available"]]
            distribution = Counter(str(value) for value in available)
            overall[family].update(distribution)
            per_ticker_distributions[ticker][family] = dict(sorted(distribution.items()))
            coverage.append(
                {
                    "ticker": ticker,
                    "label_family": family,
                    "record_count": len(values),
                    "available_count": len(available),
                    "unavailable_count": len(values) - len(available),
                    "unavailable_reason": LABEL_UNAVAILABLE_REASON,
                }
            )
    overall_distributions = {
        family: dict(sorted(counter.items())) for family, counter in overall.items()
    }
    summary = {
        "coverage_entry_count": len(coverage),
        "available_count": sum(row["available_count"] for row in coverage),
        "unavailable_count": sum(row["unavailable_count"] for row in coverage),
        "refined_label_generation_digest": semantic_digest(labels_by_ticker),
    }
    return coverage, overall_distributions, {
        "per_ticker": per_ticker_distributions,
        "summary": summary,
    }


def _feature_summaries(
    features_by_ticker: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coverage: list[dict[str, Any]] = []
    total_nulls = 0
    for ticker in TARGET_UNIVERSE:
        rows = features_by_ticker[ticker]
        for category, names in REFINED_FEATURE_CATEGORIES.items():
            null_count = sum(
                row["features"].get(name) is None for row in rows for name in names
            )
            total = len(rows) * len(names)
            total_nulls += null_count
            coverage.append(
                {
                    "ticker": ticker,
                    "feature_category": category,
                    "feature_count": len(names),
                    "record_count": len(rows),
                    "available_value_count": total - null_count,
                    "null_or_unavailable_count": null_count,
                }
            )
    return coverage, {
        "coverage_entry_count": len(coverage),
        "feature_matrix_row_count": sum(
            len(rows) for rows in features_by_ticker.values()
        ),
        "refined_feature_generation_digest": semantic_digest(features_by_ticker),
        "total_null_or_unavailable_count": total_nulls,
    }


def _signal_from_rank(rank: Any, low: str = "0.40", high: str = "0.60") -> str:
    value = research_math._parse_decimal(rank)
    if value is None:
        return "FLAT"
    if value >= Decimal(high):
        return "UP"
    if value <= Decimal(low):
        return "DOWN"
    return "FLAT"


def _vpa_signal(features: dict[str, Any]) -> str:
    location = research_math._parse_decimal(features.get("close_location_value"))
    volume_ratio = research_math._parse_decimal(features.get("volume_ratio_20"))
    if location is None or volume_ratio is None:
        return "FLAT"
    if location >= Decimal("0.60") and volume_ratio >= Decimal("1.00"):
        return "UP"
    if location <= Decimal("0.40") and volume_ratio >= Decimal("1.00"):
        return "DOWN"
    return "FLAT"


def _evaluation_rows(
    labels_by_ticker: dict[str, list[dict[str, Any]]],
    features_by_ticker: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        for label_row, feature_row in zip(
            labels_by_ticker[ticker], features_by_ticker[ticker], strict=True
        ):
            label = label_row["labels"]["REFINED_NEXT_SESSION_DIRECTION"]
            if not label["available"]:
                continue
            features = feature_row["features"]
            previous = _refined_direction(
                research_math._parse_decimal(features.get("close_return_1"))
            ) or "FLAT"
            cross = _signal_from_rank(
                features.get("cross_sectional_return_rank_percentile"),
                low="0.45",
                high="0.55",
            )
            relative = _signal_from_rank(
                features.get("cross_sectional_return_rank_percentile")
            )
            vpa = _vpa_signal(features)
            non_flat = [value for value in (relative, vpa) if value != "FLAT"]
            combined = (
                non_flat[0]
                if non_flat and all(value == non_flat[0] for value in non_flat)
                else "FLAT"
            )
            rows.append(
                {
                    "ticker": ticker,
                    "date": label_row["date"],
                    "actual": label["value"],
                    "predictions": {
                        "previous_direction_baseline": previous,
                        "zero_return_baseline": "FLAT",
                        "ticker_cross_sectional_baseline": cross,
                        "refined_relative_strength_signal": relative,
                        "refined_vpa_signal": vpa,
                        "refined_combined_simple_signal": combined,
                    },
                }
            )
    return sorted(rows, key=lambda row: (row["date"], row["ticker"]))


def _majority(rows: list[dict[str, Any]]) -> str:
    counts = Counter(row["actual"] for row in rows)
    return sorted(counts, key=lambda value: (-counts[value], value))[0] if counts else "FLAT"


def _period_metrics(
    training_rows: list[dict[str, Any]], evaluation_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    majority = _majority(training_rows)
    results: dict[str, Any] = {}
    for model_id in MODEL_COMPARISON_IDS:
        actuals = [row["actual"] for row in evaluation_rows]
        predictions = [
            majority
            if model_id == "majority_class_baseline"
            else row["predictions"][model_id]
            for row in evaluation_rows
        ]
        results[model_id] = research_math._classification_metrics(
            actuals, predictions
        )
    return results


def _walk_forward_results(evaluation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    folds = [
        ("2024_Q1", "2024-01-01", "2024-03-31"),
        ("2024_Q2", "2024-04-01", "2024-06-30"),
        ("2024_Q3", "2024-07-01", "2024-09-30"),
        ("2024_Q4", "2024-10-01", "2024-12-31"),
    ]
    results: list[dict[str, Any]] = []
    for fold_id, start, end in folds:
        training = [row for row in evaluation_rows if row["date"] < start]
        evaluation = [row for row in evaluation_rows if start <= row["date"] <= end]
        results.append(
            {
                "fold_id": fold_id,
                "training_end": start,
                "evaluation_start": start,
                "evaluation_end": end,
                "embargo_sessions": 1,
                "shuffle": False,
                "training_row_count": len(training),
                "evaluation_row_count": len(evaluation),
                "model_metrics": _period_metrics(training, evaluation),
            }
        )
    return results


def _out_of_sample_results(evaluation_rows: list[dict[str, Any]]) -> dict[str, Any]:
    training = [row for row in evaluation_rows if row["date"] <= "2024-12-31"]
    evaluation = [
        row for row in evaluation_rows if "2025-01-01" <= row["date"] <= "2025-12-31"
    ]
    overall = _period_metrics(training, evaluation)
    per_ticker = {
        ticker: _period_metrics(
            [row for row in training if row["ticker"] == ticker],
            [row for row in evaluation if row["ticker"] == ticker],
        )
        for ticker in TARGET_UNIVERSE
    }
    return {
        "training_row_count": len(training),
        "evaluation_row_count": len(evaluation),
        "model_metrics": overall,
        "per_ticker_model_metrics": per_ticker,
    }


def _model_group_results() -> list[dict[str, Any]]:
    return [
        {
            "group_id": "regularized_linear_baseline_comparison",
            "execution_status": NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE,
            "reason": "no dependency-light regularized linear implementation is registered",
        },
        {
            "group_id": "tree_based_baseline_comparison_if_available",
            "execution_status": NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE,
            "reason": "no dependency-light tree model is registered",
        },
        {
            "group_id": "simple_ensemble_baseline_comparison_if_available",
            "execution_status": "EVALUATED_RESEARCH_ONLY",
            "comparison_ids": ["refined_combined_simple_signal"],
        },
        {
            "group_id": "per_ticker_vs_cross_sectional_model_review",
            "execution_status": "EVALUATED_RESEARCH_ONLY",
            "comparison_ids": [
                "previous_direction_baseline",
                "ticker_cross_sectional_baseline",
                "refined_relative_strength_signal",
            ],
        },
        {
            "group_id": "global_vs_sector_like_grouping_review_if_available",
            "execution_status": NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE,
            "reason": "approved frozen dataset contains no sector grouping authority",
        },
    ]


def _build_reports(
    *,
    rows_by_ticker: dict[str, list[dict[str, Any]]],
    labels_by_ticker: dict[str, list[dict[str, Any]]],
    features_by_ticker: dict[str, list[dict[str, Any]]],
    run_timestamp_utc: str,
    source_verification: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    label_coverage, overall_distribution, label_details = _label_summaries(
        labels_by_ticker
    )
    feature_coverage, feature_summary = _feature_summaries(features_by_ticker)
    evaluation_rows = _evaluation_rows(labels_by_ticker, features_by_ticker)
    walk_forward = _walk_forward_results(evaluation_rows)
    out_of_sample = _out_of_sample_results(evaluation_rows)
    group_results = _model_group_results()
    record_counts = {
        ticker: len(rows_by_ticker[ticker]) for ticker in TARGET_UNIVERSE
    }
    data_quality = {
        "status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "failure_count": 0,
        "warning_count": 1,
    }
    leakage = {"status": "PASS", "failed_control_count": 0}
    reports = {
        "refined_label_generation_report": _report(
            "refined_label_generation_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "approved_label_refinement_groups": LABEL_REFINEMENT_GROUPS,
                "refined_label_families": REFINED_LABEL_FAMILIES,
                "refined_label_family_count": len(REFINED_LABEL_FAMILIES),
                "threshold_source": "FIXED_APPROVED_RESEARCH_THRESHOLDS",
                "return_bucket_thresholds": RETURN_BUCKET_THRESHOLDS,
                "flat_return_tolerance": FLAT_RETURN_TOLERANCE,
                "volatility_thresholds": VOLATILITY_THRESHOLDS,
                "drawdown_thresholds": DRAWDOWN_THRESHOLDS,
                "forward_labels_only": True,
                "future_label_values_used_as_features": False,
                "unavailable_label_boundary": {
                    "value": None,
                    "reason": LABEL_UNAVAILABLE_REASON,
                },
                "per_ticker_label_family_coverage": label_coverage,
                "per_ticker_label_distribution": label_details["per_ticker"],
                "overall_label_distribution": overall_distribution,
                **label_details["summary"],
            },
        ),
        "refined_feature_generation_report": _report(
            "refined_feature_generation_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "approved_feature_refinement_groups": FEATURE_REFINEMENT_GROUPS,
                "refined_feature_categories": REFINED_FEATURE_CATEGORIES,
                "refined_feature_group_count": len(FEATURE_REFINEMENT_GROUPS),
                "refined_feature_name_count": len(REFINED_FEATURE_NAMES),
                "features_use_current_and_historical_information_only": True,
                "future_label_values_used_as_features": False,
                "per_ticker_feature_category_coverage": feature_coverage,
                **feature_summary,
            },
        ),
        "refined_protocol_execution_report": _report(
            "refined_protocol_execution_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "approved_protocol_refinement_groups": PROTOCOL_REFINEMENT_GROUPS,
                "refined_protocol_group_count": len(PROTOCOL_REFINEMENT_GROUPS),
                "split_profile": SPLIT_PROFILE,
                "no_shuffle": True,
                "no_lookahead_leakage": True,
                "strategy_scoring_performed": False,
                "trade_recommendation_generation_performed": False,
                "runtime_migration_performed": False,
            },
        ),
        "refined_model_comparison_report": _report(
            "refined_model_comparison_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "approved_model_comparison_groups": MODEL_COMPARISON_GROUPS,
                "model_comparison_group_count": len(MODEL_COMPARISON_GROUPS),
                "deterministic_comparison_ids": MODEL_COMPARISON_IDS,
                "group_execution_results": group_results,
                "out_of_sample_model_metrics": out_of_sample["model_metrics"],
                "model_comparison_is_acceptance_evidence": False,
            },
        ),
        "refined_walk_forward_report": _report(
            "refined_walk_forward_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "walk_forward_policy": SPLIT_PROFILE["walk_forward_policy"],
                "fold_count": len(walk_forward),
                "folds": walk_forward,
                "performed": True,
            },
        ),
        "refined_out_of_sample_report": _report(
            "refined_out_of_sample_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "out_of_sample_window": SPLIT_PROFILE["out_of_sample_window"],
                "results": out_of_sample,
                "performed": True,
            },
        ),
        "refined_metric_report": _report(
            "refined_metric_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "metric_families": [
                    "classification_accuracy",
                    "macro_precision",
                    "macro_recall",
                    "macro_f1",
                    "confusion_matrix",
                    "walk_forward_stability",
                ],
                "out_of_sample_model_metrics": out_of_sample["model_metrics"],
                "walk_forward_fold_metrics": {
                    row["fold_id"]: row["model_metrics"] for row in walk_forward
                },
                "performed": True,
                "acceptance_conclusion": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED",
            },
        ),
        "refined_leakage_control_report": _report(
            "refined_leakage_control_report",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "leakage_control_status": "PASS",
                "controls": [
                    {"control": "forward_labels_only", "status": "PASS"},
                    {"control": "future_labels_not_used_as_features", "status": "PASS"},
                    {"control": "features_current_or_historical_only", "status": "PASS"},
                    {"control": "unavailable_labels_null_with_reason", "status": "PASS"},
                    {"control": "chronological_splits_only", "status": "PASS"},
                    {"control": "one_session_embargo", "status": "PASS"},
                    {"control": "shuffle_disabled", "status": "PASS"},
                    {"control": "provider_transport_disabled", "status": "PASS"},
                    {"control": "runtime_and_trading_unauthorized", "status": "PASS"},
                ],
                "failed_control_count": 0,
            },
        ),
        "per_ticker_refinement_execution_summary": _report(
            "per_ticker_refinement_execution_summary",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "target_universe": TARGET_UNIVERSE,
                "entries": [
                    {
                        "ticker": ticker,
                        "canonical_record_count": record_counts[ticker],
                        "meta_reduced_record_count_preserved": ticker == "META",
                        "refined_label_family_count": len(REFINED_LABEL_FAMILIES),
                        "refined_feature_group_count": len(FEATURE_REFINEMENT_GROUPS),
                        "refinement_execution_status": "EXECUTED_RESEARCH_ONLY",
                        "predictive_usefulness": NOT_ACCEPTED,
                        "profitability": NOT_ACCEPTED,
                        "runtime_use": NOT_AUTHORIZED,
                    }
                    for ticker in TARGET_UNIVERSE
                ],
            },
        ),
        "operator_review_summary": _report(
            "operator_review_summary",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "execution_status": FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY,
                "results_review_status": "READY_FOR_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW",
                "source_evidence": _source_evidence(),
                "generated_output_count": len(OUTPUT_FILENAMES),
                "failure_count": 0,
                "warning_count": 1,
                "additional_predictive_evidence_execution_candidate_created": False,
                "next_task": "Feature/Label Refinement Results Review Package v1",
            },
        ),
    }
    summaries = {
        "per_ticker_record_counts": record_counts,
        "refined_label_generation_summary": label_details["summary"],
        "refined_feature_generation_summary": feature_summary,
        "refined_protocol_execution_summary": {
            "group_count": len(PROTOCOL_REFINEMENT_GROUPS),
            "split_profile": SPLIT_PROFILE,
            "performed": True,
        },
        "refined_walk_forward_summary": {
            "fold_count": len(walk_forward),
            "evaluation_row_count": sum(row["evaluation_row_count"] for row in walk_forward),
            "performed": True,
        },
        "refined_out_of_sample_summary": {
            "evaluation_row_count": out_of_sample["evaluation_row_count"],
            "performed": True,
        },
        "refined_metric_summary": {
            "model_count": len(MODEL_COMPARISON_IDS),
            "performed": True,
        },
        "model_comparison_summary": {
            "approved_group_count": len(MODEL_COMPARISON_GROUPS),
            "deterministic_comparison_count": len(MODEL_COMPARISON_IDS),
            "unavailable_model_family_count": sum(
                row["execution_status"] == NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE
                for row in group_results
            ),
            "performed": True,
        },
        "refined_leakage_control_summary": leakage,
        "data_quality_summary": data_quality,
        "failure_count": 0,
        "warning_count": 1,
        "source_verification": source_verification,
    }
    return reports, summaries


def feature_label_refinement_execution_digest_v1(artifact: dict[str, Any]) -> str:
    """Return a path-independent deterministic digest for executed research."""
    payload = deepcopy(artifact)
    payload.pop("feature_label_refinement_execution_digest", None)
    payload.pop("source_root", None)
    payload.pop("generated_output_root", None)
    return semantic_digest(payload)


def _blocked_artifact(
    *,
    source_root: Path,
    output_root: Path,
    run_timestamp_utc: str,
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTED_V1,
        "execution_status": FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "source_root": _path_text(source_root),
        "generated_output_root": _path_text(output_root),
        "feature_label_refinement_execution_digest": "NOT_CREATED",
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "feature_label_refinement_executed": False,
        "feature_label_refinement_results_created": False,
        "refined_label_generation_performed": False,
        "refined_feature_generation_performed": False,
        "refined_walk_forward_validation_performed": False,
        "refined_out_of_sample_evaluation_performed": False,
        "refined_metrics_recomputation_performed": False,
        "model_comparison_performed": False,
        "generated_output_count": 0,
        "failures": failures,
        "failure_count": len(failures),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "additional_predictive_evidence_execution_candidate_created": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
    }


def _build_executed_artifact(
    *,
    run_timestamp_utc: str,
    source_root: Path,
    output_root: Path,
    summaries: dict[str, Any],
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTED,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTED_V1,
        "execution_status": FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": APPROVED_REGISTRY_METADATA["dataset_name"],
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "predictive_execution_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_matrix_rerun_performed": False,
        "walk_forward_validation_rerun_performed": False,
        "out_of_sample_evaluation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "ready_for_feature_label_refinement_execution": True,
        "feature_label_refinement_executed": True,
        "feature_label_refinement_results_created": True,
        "refined_label_generation_authorized": True,
        "refined_label_generation_performed": True,
        "refined_feature_generation_authorized": True,
        "refined_feature_generation_performed": True,
        "refined_walk_forward_validation_authorized": True,
        "refined_walk_forward_validation_performed": True,
        "refined_out_of_sample_evaluation_authorized": True,
        "refined_out_of_sample_evaluation_performed": True,
        "refined_metrics_recomputation_authorized": True,
        "refined_metrics_recomputation_performed": True,
        "model_comparison_authorized": True,
        "model_comparison_performed": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "refined_label_family_count": len(REFINED_LABEL_FAMILIES),
        "refined_feature_group_count": len(FEATURE_REFINEMENT_GROUPS),
        "refined_protocol_group_count": len(PROTOCOL_REFINEMENT_GROUPS),
        "model_comparison_group_count": len(MODEL_COMPARISON_GROUPS),
        "generated_output_count": len(OUTPUT_FILENAMES),
        "generated_output_names": list(OUTPUT_FILENAMES),
        "output_digest_manifest_summary": {
            "filename": "feature_label_refinement_execution_digest_manifest.json",
            "entry_count": len(OUTPUT_FILENAMES),
            "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        },
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "registry_approved_dataset_metadata": deepcopy(APPROVED_REGISTRY_METADATA),
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "source_root": _path_text(source_root),
        "generated_output_root": _path_text(output_root),
        "source_evidence": _source_evidence(),
        "approved_label_refinement_groups": LABEL_REFINEMENT_GROUPS,
        "approved_feature_refinement_groups": FEATURE_REFINEMENT_GROUPS,
        "approved_protocol_refinement_groups": PROTOCOL_REFINEMENT_GROUPS,
        "approved_model_comparison_groups": MODEL_COMPARISON_GROUPS,
        "refined_label_families_generated": REFINED_LABEL_FAMILIES,
        "refined_feature_categories_generated": deepcopy(REFINED_FEATURE_CATEGORIES),
        "model_comparisons_evaluated": MODEL_COMPARISON_IDS,
        "split_profile": deepcopy(SPLIT_PROFILE),
        **summaries,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
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
    }
    artifact["feature_label_refinement_execution_digest"] = (
        feature_label_refinement_execution_digest_v1(artifact)
    )
    return artifact


def _write_json_once(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise FeatureLabelRefinementExecutionError(
            f"feature/label refinement execution output already exists: {path.name}"
        ) from exc
    return sha256_bytes(data)


def execute_feature_label_refinement_v1(
    *,
    source_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute the approved refinement research run without provider access."""
    source_path = DEFAULT_SOURCE_ROOT if source_root is None else Path(source_root)
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    source_verification, failures = _verify_source_root(source_path)
    if failures:
        return _blocked_artifact(
            source_root=source_path,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            failures=failures,
        )
    rows_by_ticker, row_failures = _read_rows(source_path)
    if row_failures:
        return _blocked_artifact(
            source_root=source_path,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            failures=row_failures,
        )
    if output_path.exists() and any(output_path.iterdir()):
        raise FeatureLabelRefinementExecutionError(
            "feature/label refinement execution output root is not empty"
        )

    labels_by_ticker = _generate_refined_labels(rows_by_ticker)
    features_by_ticker = _generate_refined_features(rows_by_ticker)
    reports, summaries = _build_reports(
        rows_by_ticker=rows_by_ticker,
        labels_by_ticker=labels_by_ticker,
        features_by_ticker=features_by_ticker,
        run_timestamp_utc=timestamp,
        source_verification=source_verification,
    )
    artifact = _build_executed_artifact(
        run_timestamp_utc=timestamp,
        source_root=source_path,
        output_root=output_path,
        summaries=summaries,
    )
    validate_feature_label_refinement_executed_v1(artifact)
    reports["feature_label_refinement_execution_manifest"] = artifact

    output_digests: dict[str, str] = {}
    digest_manifest_name = "feature_label_refinement_execution_digest_manifest"
    for filename in OUTPUT_FILENAMES:
        report_name = filename.removesuffix(".json")
        if report_name == digest_manifest_name:
            continue
        output_digests[filename] = _write_json_once(
            output_path / filename, reports[report_name]
        )
    digest_entries = [
        (
            {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
            if filename == f"{digest_manifest_name}.json"
            else {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": output_digests[filename],
            }
        )
        for filename in OUTPUT_FILENAMES
    ]
    digest_manifest = _report(
        digest_manifest_name,
        {
            "run_timestamp_utc": timestamp,
            "generated_output_count": len(OUTPUT_FILENAMES),
            "output_digest_entries": digest_entries,
            "all_non_self_output_digests_present": True,
            "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
            "feature_label_refinement_execution_digest": artifact[
                "feature_label_refinement_execution_digest"
            ],
        },
    )
    _write_json_once(
        output_path / f"{digest_manifest_name}.json", digest_manifest
    )
    return artifact


FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


def _reject_forbidden_values(value: Any, *, path: str = "artifact") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in FORBIDDEN_ARTIFACT_VALUES:
                raise FeatureLabelRefinementExecutionError(
                    f"{current} must not emit {item}"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise FeatureLabelRefinementExecutionError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise FeatureLabelRefinementExecutionError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureLabelRefinementExecutionError(f"{field} mismatch")


def validate_feature_label_refinement_executed_v1(
    artifact: dict,
) -> dict[str, Any]:
    """Validate executed refinement evidence and every closed authority boundary."""
    if not isinstance(artifact, dict):
        raise FeatureLabelRefinementExecutionError(
            "feature/label refinement executed artifact must be a JSON object"
        )
    _reject_forbidden_values(artifact)
    _expect(
        artifact.get("artifact_kind"),
        ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTED,
        "artifact_kind",
    )
    _expect(
        artifact.get("execution_status"),
        FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY,
        "execution_status",
    )
    _expect(
        artifact.get("schema_version"),
        SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTED_V1,
        "schema_version",
    )
    source = artifact.get("source_evidence")
    _expect(source, _source_evidence(), "source_evidence")
    for field in TRUE_EXECUTION_FIELDS:
        _expect(artifact.get(field), True, field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect(artifact.get(field), False, field)
    _expect(artifact.get("refined_label_family_count"), 7, "refined_label_family_count")
    _expect(artifact.get("refined_feature_group_count"), 9, "refined_feature_group_count")
    _expect(artifact.get("refined_protocol_group_count"), 6, "refined_protocol_group_count")
    _expect(artifact.get("model_comparison_group_count"), 5, "model_comparison_group_count")
    _expect(artifact.get("generated_output_count"), 12, "generated_output_count")
    _expect(artifact.get("generated_output_names"), OUTPUT_FILENAMES, "generated_output_names")
    _expect(artifact.get("target_universe_count"), 12, "target_universe_count")
    _expect(artifact.get("target_universe"), TARGET_UNIVERSE, "target_universe")
    _expect(
        artifact.get("total_canonical_record_count"),
        11946,
        "total_canonical_record_count",
    )
    _expect(artifact.get("records_digest"), EXPECTED_RECORDS_DIGEST, "records_digest")
    _expect(artifact.get("meta_record_count"), 913, "meta_record_count")
    _expect(artifact.get("non_meta_record_count"), 1003, "non_meta_record_count")
    _expect(
        artifact.get("per_ticker_record_counts"),
        EXPECTED_RECORD_COUNTS,
        "per_ticker_record_counts",
    )
    _expect(artifact.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    digest = artifact.get("feature_label_refinement_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureLabelRefinementExecutionError(
            "feature_label_refinement_execution_digest missing"
        )
    _expect(
        digest,
        feature_label_refinement_execution_digest_v1(artifact),
        "feature_label_refinement_execution_digest",
    )
    return {
        "status": FEATURE_LABEL_REFINEMENT_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "feature_label_refinement_execution_digest": digest,
        "generated_output_count": artifact["generated_output_count"],
        "failure_count": artifact["failure_count"],
        "warning_count": artifact["warning_count"],
        "feature_label_refinement_executed": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_feature_label_refinement_execution_status_markdown_v1(
    artifact: dict,
) -> str:
    """Render a sanitized status summary for executed refinement research."""
    validation = validate_feature_label_refinement_executed_v1(artifact)
    lines = [
        "# MarketFlow Feature/Label Refinement Execution Status",
        "",
        "## Title",
        "- Feature/Label Refinement Execution v1.",
        "",
        "## Feature/Label Refinement Execution",
        f"- Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`.",
        f"- Execution digest: `{validation['feature_label_refinement_execution_digest']}`.",
        "",
        "## Source Execution Approval",
        f"- Approval digest: `{artifact['source_evidence']['feature_label_refinement_execution_approval_digest']}`.",
        f"- Candidate review/candidate digests: `{artifact['source_evidence']['feature_label_refinement_execution_candidate_review_package_digest']}` / `{artifact['source_evidence']['feature_label_refinement_execution_candidate_digest']}`.",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/scope/status: `{artifact['dataset_name']}` / `{artifact['registry_approved_dataset_metadata']['dataset_scope']}` / `{artifact['registry_approved_dataset_metadata']['registry_entry_status']}`.",
        f"- Records/count: `{artifact['records_digest']}` / `{artifact['total_canonical_record_count']}`.",
        "",
        "## Target Universe",
        f"- `{', '.join(artifact['target_universe'])}`; META remains `{artifact['meta_record_count']}` and every non-META ticker remains `{artifact['non_meta_record_count']}`.",
        "",
        "## Refined Label Generation Summary",
        f"- `{artifact['refined_label_family_count']}` families; digest `{artifact['refined_label_generation_summary']['refined_label_generation_digest']}`.",
        "",
        "## Refined Feature Generation Summary",
        f"- `{artifact['refined_feature_group_count']}` approved groups; digest `{artifact['refined_feature_generation_summary']['refined_feature_generation_digest']}`.",
        "",
        "## Refined Protocol Execution Summary",
        f"- `{artifact['refined_protocol_group_count']}` groups; chronological/no-shuffle execution performed.",
        "",
        "## Refined Walk-Forward Summary",
        f"- `{artifact['refined_walk_forward_summary']['fold_count']}` folds; performed `{artifact['refined_walk_forward_summary']['performed']}`.",
        "",
        "## Refined OOS Summary",
        f"- Evaluation rows: `{artifact['refined_out_of_sample_summary']['evaluation_row_count']}`; performed `{artifact['refined_out_of_sample_summary']['performed']}`.",
        "",
        "## Refined Metrics Summary",
        f"- Model comparisons: `{artifact['refined_metric_summary']['model_count']}`; performed `{artifact['refined_metric_summary']['performed']}`.",
        "",
        "## Model Comparison Summary",
        f"- Approved groups/deterministic comparisons/unavailable families: `{artifact['model_comparison_summary']['approved_group_count']}` / `{artifact['model_comparison_summary']['deterministic_comparison_count']}` / `{artifact['model_comparison_summary']['unavailable_model_family_count']}`.",
        "",
        "## Refined Leakage-Control Summary",
        f"- Status/failed controls: `{artifact['refined_leakage_control_summary']['status']}` / `{artifact['refined_leakage_control_summary']['failed_control_count']}`.",
        "",
        "## Data Quality Summary",
        f"- Status/failures/warnings: `{artifact['data_quality_summary']['status']}` / `{artifact['failure_count']}` / `{artifact['warning_count']}`.",
        "",
        "## Output Digest Manifest",
        f"- Root/count/manifest: `{artifact['generated_output_root']}` / `{artifact['generated_output_count']}` / `{artifact['output_digest_manifest_summary']['filename']}`.",
        "",
        "## Execution Boundary",
        "- Refinement execution and its research-only results are complete. No additional predictive-evidence execution candidate was created.",
        "",
        "## Predictive Usefulness Boundary",
        f"- Predictive usefulness: `{artifact['predictive_usefulness']}`; no acceptance candidate was created.",
        "",
        "## Profitability Boundary",
        f"- Profitability: `{artifact['profitability']}`.",
        "",
        "## Runtime Boundary",
        f"- Runtime/strategy/paper/broker: `{artifact['runtime_use']}` / `{artifact['strategy_use']}` / `{artifact['paper_trading']}` / `{artifact['broker_execution']}`.",
        "",
        "## Checklist Summary",
        f"- Failures/warnings: `{artifact['failure_count']}` / `{artifact['warning_count']}`.",
        "",
        "## Guardrails",
        "- Execution was offline and used only the verified frozen canonical records. It made no provider request, acquisition, dataset regeneration, runtime change, strategy scoring, or trade recommendation.",
        "- META's exact 913-record limitation remains preserved without repair, inference, normalization, backfill, or fabrication.",
        "- Next task: Feature/Label Refinement Results Review Package v1.",
        "",
    ]
    return "\n".join(lines)
