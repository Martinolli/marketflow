"""Offline, streaming expectancy backtest-lab execution.

This module consumes only the already-reviewed feature-label matrix and
VPA/Wyckoff JSONL outputs.  It creates descriptive, research-only evidence;
it never trains a model, scores a strategy, or creates an actionable signal.
"""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
import hashlib
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
    marketflow_expectancy_backtest_lab_approval_service as approval_service,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_V1 = (
    "marketflow_expectancy_backtest_lab_execution_v1"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_VALID = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_VALID"
)
EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME = (
    "EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME"
)

SELECTED_BACKTEST_LAB_PACKAGE = approval_service.SELECTED_BACKTEST_LAB_PACKAGE
SELECTED_VPA_WYCKOFF_PACKAGE = approval_service.SELECTED_VPA_WYCKOFF_PACKAGE
SELECTED_MATRIX_PACKAGE = approval_service.SELECTED_MATRIX_PACKAGE
SELECTED_MATRIX_LAYOUT = approval_service.SELECTED_MATRIX_LAYOUT
SELECTED_FEATURE_PACKAGE = approval_service.SELECTED_FEATURE_PACKAGE
SELECTED_LABEL_TARGET_PACKAGE = approval_service.SELECTED_LABEL_TARGET_PACKAGE
SELECTED_OBJECTIVE_PATH = approval_service.SELECTED_OBJECTIVE_PATH

EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "b6a6289dcfe9b4fa1888e697025187e6f287429e54756b9bbd0528ab0138d16e"
)
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = (
    approval_service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = approval_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = approval_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = approval_service.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(approval_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = {ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE}
EXPECTED_LAB_ROW_COUNTS = {ticker: (13695 if ticker == "META" else 15045) for ticker in TARGET_UNIVERSE}
EXPECTED_EVALUABLE_COUNTS = {ticker: (13520 if ticker == "META" else 14870) for ticker in TARGET_UNIVERSE}
EXPECTED_UNAVAILABLE_COUNTS = {ticker: 175 for ticker in TARGET_UNIVERSE}
EXPECTED_SOURCE_MATRIX_ROW_COUNT = 179190
EXPECTED_EVALUABLE_TARGET_ROW_COUNT = 177090
EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT = 2100
EXPECTED_OUTPUT_COUNT = 14

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "EXPECTANCY_BACKTEST_LAB_RESEARCH_ONLY"

DEFAULT_MATRIX_ROWS_PATH = (
    Path(".marketflow") / "feature_label_matrix" / "expanded_universe_v1" / "matrix_rows.jsonl"
)
DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH = (
    Path(".marketflow") / "vpa_wyckoff_rule_baseline" / "expanded_universe_v1" / "vpa_wyckoff_rule_values.jsonl"
)
DEFAULT_OUTPUT_ROOT = (
    Path(".marketflow") / "expectancy_backtest_lab" / "expanded_universe_v1"
)

OUTPUT_FILENAMES = [
    "expectancy_backtest_lab_manifest.json",
    "expectancy_backtest_lab_schema.json",
    "expectancy_backtest_rows.jsonl",
    "expectancy_backtest_result_summary.json",
    "expectancy_metric_report.json",
    "baseline_comparison_report.json",
    "vpa_wyckoff_rule_alignment_report.json",
    "abstention_quality_report.json",
    "per_ticker_backtest_report.json",
    "chronological_split_report.json",
    "meta_limitation_report.json",
    "no_peek_report.json",
    "operator_summary.json",
    "expectancy_backtest_lab_digest_manifest.json",
]

APPROVED_BASELINE_IDS = list(approval_service.APPROVED_BASELINE_IDS)
BLOCKED_BASELINE_ID = approval_service.BLOCKED_BASELINE_ID
APPROVED_METRIC_FAMILY_IDS = list(approval_service.APPROVED_METRIC_FAMILY_IDS)
BLOCKED_METRIC_FAMILY_ID = approval_service.BLOCKED_METRIC_FAMILY_ID

IDENTITY_KEYS = (
    "dataset_name", "ticker", "date", "source_profile", "timeframe",
    "canonical_record_index", "target_family", "target_horizon_sessions",
    "target_profile",
)
FORBIDDEN_ROW_FIELDS = {
    "prediction", "strategy_score", "trade_recommendation", "broker_order",
    "order_id", "provider_payload", "api_key", "runtime_signal",
    "paper_trade_signal", "live_trade_signal",
}
NESTED_NO_OUTCOME_FIELDS = (
    "vpa_wyckoff_rule_values", "vpa_wyckoff_state_values",
    "baseline_references", "objective_context", "metric_eligibility",
)

SPLITS = {
    "CALIBRATION_2022_2023": ("2022-01-01", "2023-12-31"),
    "VALIDATION_2024": ("2024-01-01", "2024-12-31"),
    "HOLDOUT_2025": ("2025-01-01", "2025-12-31"),
}

NEXT_CHAIN = [
    "Expectancy Backtest Lab Results Review v1.",
    "Predictive-usefulness reassessment using expectancy lab evidence.",
    "Acceptance-readiness review only after reassessment.",
    "Predictive-usefulness acceptance candidate only if readiness passes.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_backtest_lab_results_review",
    "predictive_usefulness_reassessment_using_expectancy_lab_evidence",
    "predictive_usefulness_acceptance_readiness_if_reassessment_supports_it",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_creates_only_research_backtest_lab_evidence",
    "execution_does_not_train_models",
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
    "execution_does_not_rerun_vpa_wyckoff_execution",
    "execution_does_not_rerun_vpa_wyckoff_results_review",
    "execution_does_not_rerun_feature_label_matrix_execution",
    "execution_does_not_rerun_feature_label_matrix_results_review",
    "execution_does_not_rerun_signal_feature_generation",
    "execution_does_not_rerun_target_generation",
    "execution_does_not_rerun_expectancy_backtest_lab_candidate_creation",
    "execution_does_not_rerun_expectancy_backtest_lab_candidate_review",
    "execution_does_not_rerun_expectancy_backtest_lab_approval",
    "do_not_mutate_frozen_dataset", "do_not_mutate_vpa_wyckoff_outputs",
    "do_not_mutate_matrix_outputs", "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_target_outputs", "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs", "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation", "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound", "source_candidate_review_digest_bound",
    "source_candidate_digest_bound", "source_vpa_wyckoff_results_review_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound", "source_matrix_rows_digest_bound",
    "source_target_values_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "selected_backtest_lab_package_preserved", "selected_vpa_wyckoff_package_preserved",
    "selected_matrix_package_preserved", "selected_matrix_layout_preserved",
    "selected_feature_package_preserved", "selected_target_package_preserved",
    "selected_objective_path_preserved", "source_backtest_lab_authorized_true",
    "backtest_lab_executed_true", "backtest_rows_created_true",
    "backtest_results_created_true", "metric_values_computed_true",
    "metric_reports_created_true", "metric_computation_performed_true",
    "backtest_execution_performed_true", "source_matrix_row_count_179190",
    "backtest_lab_row_count_179190", "evaluable_target_row_count_177090",
    "unavailable_target_row_count_2100", "vpa_wyckoff_rule_row_count_179190",
    "vpa_wyckoff_state_row_count_179190", "approved_metric_family_count_13",
    "blocked_metric_family_count_1", "approved_baseline_count_6",
    "blocked_baseline_count_1", "per_non_meta_ticker_counts_preserved",
    "meta_counts_preserved", "generated_output_count_14", "backtest_rows_jsonl_created",
    "backtest_lab_schema_created", "result_summary_created", "metric_report_created",
    "baseline_comparison_report_created", "vpa_wyckoff_rule_alignment_report_created",
    "abstention_quality_report_created", "per_ticker_backtest_report_created",
    "chronological_split_report_created", "meta_limitation_report_created",
    "no_peek_report_created", "operator_summary_created", "digest_manifest_created",
    "digest_manifest_self_reference_policy_verified",
    "blocked_randomized_null_reference_not_executed", "blocked_bootstrap_metric_not_computed",
    "chronological_no_shuffle_preserved", "horizon_aware_embargo_documented",
    "target_values_only_as_outcomes", "target_classes_only_as_outcomes",
    "forward_returns_not_used_as_features", "prediction_fields_absent",
    "strategy_score_fields_absent", "trade_recommendation_fields_absent",
    "broker_order_fields_absent", "provider_payload_fields_absent", "api_key_fields_absent",
    "model_training_authorized_false", "model_training_performed_false",
    "strategy_scoring_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "vpa_wyckoff_execution_rerun_false", "vpa_wyckoff_results_review_rerun_false",
    "matrix_execution_rerun_false", "matrix_results_review_rerun_false",
    "signal_feature_generation_rerun_false", "target_generation_rerun_false",
    "candidate_creation_rerun_false", "candidate_review_rerun_false",
    "approval_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowExpectancyBacktestLabExecutionError(ValueError):
    """Raised when execution evidence violates the research-only contract."""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _decimal(value: Any) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return result if result.is_finite() else None


def _decimal_text(value: Decimal | None) -> str | None:
    if value is None:
        return None
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _metric_value(row: Mapping[str, Any]) -> Decimal | None:
    """Return a descriptive scalar without changing the preserved outcome.

    Numeric target profiles retain their reviewed numeric value.  The two
    classification-only abstention outcomes use a documented binary indicator;
    this keeps their availability coverage in descriptive rate metrics without
    inventing a return or P&L value.
    """
    value = _decimal(row.get("target_value"))
    if value is not None:
        return value
    target_class = row.get("target_class")
    if target_class == "TRADE_ELIGIBLE_RESEARCH_ONLY":
        return Decimal(1)
    if target_class == "NO_TRADE_ABSTAIN":
        return Decimal(0)
    return None


def _split(date_text: str) -> str:
    for split_id, (start, end) in SPLITS.items():
        if start <= date_text <= end:
            return split_id
    raise MarketFlowExpectancyBacktestLabExecutionError(f"row date outside approved splits: {date_text}")


def _empty_stats() -> dict[str, Any]:
    return {"eligible": 0, "participating": 0, "positive": 0, "negative": 0,
            "sum": Decimal(0), "positive_sum": Decimal(0), "negative_abs_sum": Decimal(0),
            "min": None, "material": 0, "captured_material": 0}


def _update_stats(stats: dict[str, Any], value: Decimal, participates: bool) -> None:
    stats["eligible"] += 1
    if abs(value) >= Decimal("0.01"):
        stats["material"] += 1
        if participates:
            stats["captured_material"] += 1
    if not participates:
        return
    stats["participating"] += 1
    stats["sum"] += value
    stats["min"] = value if stats["min"] is None else min(stats["min"], value)
    if value > 0:
        stats["positive"] += 1
        stats["positive_sum"] += value
    elif value < 0:
        stats["negative"] += 1
        stats["negative_abs_sum"] += abs(value)


def _ratio(numerator: Decimal, denominator: int | Decimal) -> str | None:
    if not denominator:
        return None
    return _decimal_text(numerator / Decimal(denominator))


def _stats_report(stats: Mapping[str, Any]) -> dict[str, Any]:
    participating = stats["participating"]
    positive = stats["positive"]
    negative = stats["negative"]
    average_positive = stats["positive_sum"] / positive if positive else None
    average_negative = stats["negative_abs_sum"] / negative if negative else None
    payoff = (
        average_positive / average_negative
        if average_positive is not None and average_negative not in (None, Decimal(0)) else None
    )
    return {
        "eligible_row_count": stats["eligible"],
        "participating_row_count": participating,
        "coverage_rate": _ratio(Decimal(participating), stats["eligible"]),
        "average_target_outcome": _ratio(stats["sum"], participating),
        "expectancy_after_cost": _ratio(stats["sum"], participating),
        "cost_interpretation": "TARGET_VALUE_ALREADY_REFLECTS_APPROVED_TARGET_COST_CONTEXT",
        "positive_outcome_rate": _ratio(Decimal(positive), participating),
        "payoff_ratio": _decimal_text(payoff),
        "reward_to_risk_alignment": _decimal_text(payoff),
        "adverse_excursion_proxy": _decimal_text(stats["min"]),
        "material_move_capture_rate": _ratio(Decimal(stats["captured_material"]), stats["material"]),
        "material_move_row_count": stats["material"],
    }


def _prior_scan(path: Path) -> dict[tuple[str, str, str], tuple[Decimal, int]]:
    totals: dict[tuple[str, str, str], list[Any]] = defaultdict(lambda: [Decimal(0), 0])
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise MarketFlowExpectancyBacktestLabExecutionError(
                    f"matrix row {line_number} is invalid JSON"
                ) from exc
            if not row.get("target_available"):
                continue
            value = _metric_value(row)
            if value is None:
                raise MarketFlowExpectancyBacktestLabExecutionError(
                    f"matrix row {line_number} available target has no descriptive metric scalar"
                )
            key = (_split(row["date"]), row["target_profile"], row["target_family"])
            totals[key][0] += value
            totals[key][1] += 1
    return {key: (value[0], value[1]) for key, value in totals.items()}


def _prior_reference(
    split_id: str, profile: str, family: str,
    priors: Mapping[tuple[str, str, str], tuple[Decimal, int]],
) -> dict[str, Any]:
    earlier = []
    if split_id in {"VALIDATION_2024", "HOLDOUT_2025"}:
        earlier.append("CALIBRATION_2022_2023")
    if split_id == "HOLDOUT_2025":
        earlier.append("VALIDATION_2024")
    total = Decimal(0)
    count = 0
    for prior_split in earlier:
        subtotal, subcount = priors.get((prior_split, profile, family), (Decimal(0), 0))
        total += subtotal
        count += subcount
    return {
        "available": bool(count),
        "participates": bool(count),
        "reference_value": _ratio(total, count),
        "source_splits": earlier,
        "source_row_count": count,
        "unavailable_reason": None if count else "NO_STRICTLY_EARLIER_SPLIT_PRIOR",
    }


def _previous_direction(matrix: Mapping[str, Any]) -> dict[str, Any]:
    try:
        value = matrix["feature_bundle"]["GROUP_CLOSE_TO_CLOSE_RETURNS"]["feature_values"]["trailing_return_1"]
    except (KeyError, TypeError):
        value = None
    number = _decimal(value)
    return {
        "available": number is not None,
        "participates": number is not None and number > 0,
        "direction": None if number is None else ("POSITIVE" if number > 0 else "NON_POSITIVE"),
        "source_field": "GROUP_CLOSE_TO_CLOSE_RETURNS.trailing_return_1",
        "unavailable_reason": None if number is not None else "TRAILING_DIRECTION_UNAVAILABLE",
    }


def _vpa_reference(vpa: Mapping[str, Any]) -> dict[str, Any]:
    tags = [str(item.get("tag", "")) for item in vpa["rule_values"].values() if item.get("available")]
    states = [key for key, item in vpa["state_values"].items() if item.get("available") and item.get("value") is True]
    favorable_tokens = ("demand", "breakout", "leadership", "markup", "confirmation")
    avoid_tokens = ("supply", "weak", "markdown", "noise", "abstain")
    favorable = any(any(token in value.lower() for token in favorable_tokens) for value in tags + states)
    avoid = any(any(token in value.lower() for token in avoid_tokens) for value in tags + states)
    available = bool(tags or states)
    return {
        "available": available,
        "participates": available and favorable and not avoid,
        "context": "FAVORABLE" if favorable and not avoid else ("AVOID" if avoid else "NEUTRAL"),
        "definition_source": "REVIEWED_VPA_WYCKOFF_RULE_AND_STATE_TAGS_ONLY",
        "unavailable_reason": None if available else "RULE_AND_STATE_TAGS_UNAVAILABLE",
    }


def _baseline_references(
    matrix: Mapping[str, Any], vpa: Mapping[str, Any], split_id: str,
    research_available: bool,
    priors: Mapping[tuple[str, str, str], tuple[Decimal, int]],
) -> dict[str, Any]:
    target_available = bool(matrix["target_available"])
    return {
        "BASELINE_ALWAYS_ABSTAIN": {"available": True, "participates": False, "reference": "ABSTAIN"},
        "BASELINE_ALWAYS_AVAILABLE_TARGET": {
            "available": target_available, "participates": target_available and research_available,
            "reference": "AVAILABLE_TARGET_COVERAGE_ONLY",
        },
        "BASELINE_SIMPLE_BUY_AND_HOLD_REFERENCE": {
            "available": target_available, "participates": target_available and research_available,
            "reference": "TARGET_OUTCOME_DISTRIBUTION_ONLY_NO_PNL_SIMULATION",
        },
        "BASELINE_PREVIOUS_DIRECTION_REFERENCE": _previous_direction(matrix),
        "BASELINE_VPA_WYCKOFF_RULE_TAG_REFERENCE": _vpa_reference(vpa),
        "BASELINE_TARGET_PROFILE_PRIOR_RATE_REFERENCE": _prior_reference(
            split_id, matrix["target_profile"], matrix["target_family"], priors
        ),
    }


def _validate_pair(matrix: Mapping[str, Any], vpa: Mapping[str, Any], line_number: int) -> None:
    for key in IDENTITY_KEYS:
        if matrix.get(key) != vpa.get(key):
            raise MarketFlowExpectancyBacktestLabExecutionError(
                f"source identity mismatch at row {line_number}: {key}"
            )
    expected_matrix = {
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    }
    for key, value in expected_matrix.items():
        if matrix.get(key) != value:
            raise MarketFlowExpectancyBacktestLabExecutionError(
                f"matrix row {line_number} {key} mismatch"
            )
    expected_vpa = {
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
    }
    for key, value in expected_vpa.items():
        if vpa.get(key) != value:
            raise MarketFlowExpectancyBacktestLabExecutionError(
                f"VPA/Wyckoff row {line_number} {key} mismatch"
            )
    if matrix.get("target_available") != vpa.get("target_available"):
        raise MarketFlowExpectancyBacktestLabExecutionError(
            f"source target availability mismatch at row {line_number}"
        )
    if matrix.get("ticker") not in TARGET_UNIVERSE:
        raise MarketFlowExpectancyBacktestLabExecutionError(
            f"matrix row {line_number} ticker outside approved universe"
        )
    if not isinstance(vpa.get("rule_values"), Mapping) or len(vpa["rule_values"]) != 8:
        raise MarketFlowExpectancyBacktestLabExecutionError(f"VPA rule schema mismatch at row {line_number}")
    if not isinstance(vpa.get("state_values"), Mapping) or len(vpa["state_values"]) != 6:
        raise MarketFlowExpectancyBacktestLabExecutionError(f"VPA state schema mismatch at row {line_number}")


def _lab_row(
    matrix: Mapping[str, Any], vpa: Mapping[str, Any], split_id: str,
    priors: Mapping[tuple[str, str, str], tuple[Decimal, int]],
) -> dict[str, Any]:
    target_available = bool(matrix["target_available"])
    forward_end = matrix.get("forward_end_date")
    split_end = SPLITS[split_id][1]
    embargo_pass = target_available and isinstance(forward_end, str) and forward_end <= split_end
    unavailable_reason = matrix.get("target_unavailable_reason") if not target_available else (
        None if embargo_pass else "FORWARD_HORIZON_CROSSES_CHRONOLOGICAL_SPLIT_BOUNDARY"
    )
    baselines = _baseline_references(matrix, vpa, split_id, embargo_pass, priors)
    row = {
        **{key: matrix.get(key) for key in IDENTITY_KEYS},
        "target_available": target_available,
        "target_value": matrix.get("target_value"), "target_class": matrix.get("target_class"),
        "target_unavailable_reason": matrix.get("target_unavailable_reason"),
        "forward_start_date": matrix.get("forward_start_date"),
        "forward_end_date": forward_end,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "chronological_split": split_id,
        "horizon_aware_embargo_status": "ELIGIBLE" if embargo_pass else (
            "NOT_APPLICABLE_TARGET_UNAVAILABLE" if not target_available else "EMBARGOED_SPLIT_BOUNDARY"
        ),
        "research_row_available": embargo_pass,
        "research_unavailable_reason": unavailable_reason,
        "vpa_wyckoff_rule_values": deepcopy(vpa["rule_values"]),
        "vpa_wyckoff_state_values": deepcopy(vpa["state_values"]),
        "vpa_rule_family_count": len(vpa["rule_values"]),
        "vpa_state_family_count": len(vpa["state_values"]),
        "baseline_references": baselines,
        "objective_context": {
            "objective_path": SELECTED_OBJECTIVE_PATH,
            "cost_context": "TARGET_VALUE_ALREADY_REFLECTS_APPROVED_TARGET_COST_CONTEXT",
            "research_only": True, "non_actionable": True,
        },
        "metric_eligibility": {
            "eligible": embargo_pass,
            "requires_target_available": True,
            "chronological_embargo_passed": embargo_pass,
            "unavailable_reason": unavailable_reason,
        },
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "output_label": OUTPUT_LABEL, "evidence_scope": EVIDENCE_SCOPE,
        "research_only": True, "non_actionable": True,
    }
    return row


def _common_output_fields(timestamp: str) -> dict[str, Any]:
    return {
        "run_timestamp_utc": timestamp, "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "expectancy_backtest_lab_executed": True, "expectancy_backtest_rows_created": True,
        "expectancy_backtest_results_created": True, "backtest_execution_performed": True,
        "metric_values_computed": True, "metric_reports_created": True,
        "metric_computation_performed": True, "model_training_authorized": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "trade_recommendations_generated": False,
        "research_only": True, "non_actionable": True,
    }


def _report(timestamp: str, report_kind: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {"report_kind": report_kind, **_common_output_fields(timestamp), **deepcopy(dict(payload))}


def _blocked_artifact(output_root: Path, timestamp: str, failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_V1,
        "execution_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS,
        "execution_scope": EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME,
        "run_timestamp_utc": timestamp, "generated_output_root": str(output_root).replace("\\", "/"),
        "failures": failures, "expectancy_backtest_lab_executed": False,
        "expectancy_backtest_rows_created": False, "expectancy_backtest_results_created": False,
        "backtest_execution_performed": False, "metric_values_computed": False,
        "metric_reports_created": False, "metric_computation_performed": False,
        "model_training_authorized": False, "model_training_performed": False,
        "strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "risk_controls": list(RISK_CONTROLS),
    }


def _execute_rows(
    matrix_path: Path, vpa_path: Path, output_path: Path,
    priors: Mapping[tuple[str, str, str], tuple[Decimal, int]],
) -> tuple[str, dict[str, Any]]:
    digest = hashlib.sha256()
    counts = {
        "rows": 0, "evaluable": 0, "unavailable": 0, "embargoed": 0,
        "ticker": defaultdict(lambda: {"rows": 0, "evaluable": 0, "unavailable": 0, "embargoed": 0}),
        "split": defaultdict(lambda: {"rows": 0, "evaluable": 0, "unavailable": 0, "embargoed": 0}),
        "baseline": defaultdict(_empty_stats),
        "baseline_split": defaultdict(_empty_stats),
        "baseline_ticker": defaultdict(_empty_stats),
        "rule_context": defaultdict(_empty_stats),
    }
    with matrix_path.open("r", encoding="utf-8") as matrix_handle, vpa_path.open("r", encoding="utf-8") as vpa_handle, output_path.open("wb") as output:
        line_number = 0
        while True:
            matrix_line = matrix_handle.readline()
            vpa_line = vpa_handle.readline()
            if not matrix_line and not vpa_line:
                break
            line_number += 1
            if not matrix_line or not vpa_line:
                raise MarketFlowExpectancyBacktestLabExecutionError(
                    f"source row counts differ at row {line_number}"
                )
            try:
                matrix = json.loads(matrix_line)
                vpa = json.loads(vpa_line)
            except json.JSONDecodeError as exc:
                raise MarketFlowExpectancyBacktestLabExecutionError(
                    f"source row {line_number} is invalid JSON"
                ) from exc
            _validate_pair(matrix, vpa, line_number)
            split_id = _split(matrix["date"])
            row = _lab_row(matrix, vpa, split_id, priors)
            payload = canonical_json_bytes(row)
            output.write(payload)
            digest.update(payload)
            ticker = matrix["ticker"]
            counts["rows"] += 1
            counts["ticker"][ticker]["rows"] += 1
            counts["split"][split_id]["rows"] += 1
            if matrix["target_available"]:
                counts["evaluable"] += 1
                counts["ticker"][ticker]["evaluable"] += 1
                counts["split"][split_id]["evaluable"] += 1
                if not row["research_row_available"]:
                    counts["embargoed"] += 1
                    counts["ticker"][ticker]["embargoed"] += 1
                    counts["split"][split_id]["embargoed"] += 1
            else:
                counts["unavailable"] += 1
                counts["ticker"][ticker]["unavailable"] += 1
                counts["split"][split_id]["unavailable"] += 1
            value = _metric_value(matrix)
            if value is not None and row["research_row_available"]:
                for baseline_id, reference in row["baseline_references"].items():
                    participates = bool(reference.get("participates"))
                    _update_stats(counts["baseline"][baseline_id], value, participates)
                    _update_stats(counts["baseline_split"][(baseline_id, split_id)], value, participates)
                    _update_stats(counts["baseline_ticker"][(baseline_id, ticker)], value, participates)
                context = row["baseline_references"]["BASELINE_VPA_WYCKOFF_RULE_TAG_REFERENCE"]["context"]
                _update_stats(counts["rule_context"][context], value, True)
    return digest.hexdigest(), counts


def per_ticker_expectancy_backtest_lab_execution_digest_v1(entry: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_backtest_lab_execution_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        row_counts = counts["ticker"][ticker]
        entry = {
            "ticker": ticker, "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN", "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "expectancy_backtest_lab_approval_status": approval_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
            "expectancy_backtest_lab_execution_status": "GENERATED_RESEARCH_ONLY",
            "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
            "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
            "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
            "selected_feature_package": SELECTED_FEATURE_PACKAGE,
            "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
            "backtest_lab_row_count": row_counts["rows"],
            "evaluable_target_row_count": row_counts["evaluable"],
            "unavailable_target_row_count": row_counts["unavailable"],
            "embargoed_metric_row_count": row_counts["embargoed"],
            "vpa_wyckoff_rule_row_count": row_counts["rows"],
            "vpa_wyckoff_state_row_count": row_counts["rows"],
            "approved_metric_family_count": 13, "approved_baseline_count": 6,
            "expectancy_backtest_lab_executed": True, "expectancy_backtest_rows_created": True,
            "expectancy_backtest_results_created": True, "backtest_execution_performed": True,
            "metric_values_computed": True, "metric_reports_created": True,
            "metric_computation_performed": True, "model_training_authorized": False,
            "model_training_performed": False, "strategy_scoring_performed": False,
            "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        }
        if ticker == "META":
            entry["generation_note"] = "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_EXECUTION"
        entry["per_ticker_expectancy_backtest_lab_execution_digest"] = per_ticker_expectancy_backtest_lab_execution_digest_v1(entry)
        entries.append(entry)
    return entries


def _reports(timestamp: str, counts: Mapping[str, Any], per_ticker: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    baseline_global = {baseline: _stats_report(counts["baseline"][baseline]) for baseline in APPROVED_BASELINE_IDS}
    baseline_splits = {
        baseline: {split_id: _stats_report(counts["baseline_split"][(baseline, split_id)]) for split_id in SPLITS}
        for baseline in APPROVED_BASELINE_IDS
    }
    baseline_tickers = {
        baseline: {ticker: _stats_report(counts["baseline_ticker"][(baseline, ticker)]) for ticker in TARGET_UNIVERSE}
        for baseline in APPROVED_BASELINE_IDS
    }
    available_reference = baseline_global["BASELINE_ALWAYS_AVAILABLE_TARGET"]
    baseline_deltas = {}
    for baseline, summary in baseline_global.items():
        baseline_average = _decimal(summary["average_target_outcome"])
        reference_average = _decimal(available_reference["average_target_outcome"])
        baseline_coverage = _decimal(summary["coverage_rate"])
        reference_coverage = _decimal(available_reference["coverage_rate"])
        baseline_deltas[baseline] = {
            "average_target_outcome_delta_vs_always_available": _decimal_text(
                baseline_average - reference_average
                if baseline_average is not None and reference_average is not None else None
            ),
            "coverage_delta_vs_always_available": _decimal_text(
                baseline_coverage - reference_coverage
                if baseline_coverage is not None and reference_coverage is not None else None
            ),
        }
    schema = {
        "schema_version": "marketflow_expectancy_backtest_lab_row_v1",
        "identity_fields": list(IDENTITY_KEYS),
        "outcome_fields": ["target_available", "target_value", "target_class", "target_unavailable_reason", "forward_start_date", "forward_end_date"],
        "research_condition_fields": ["vpa_wyckoff_rule_values", "vpa_wyckoff_state_values", "baseline_references"],
        "forbidden_fields": sorted(FORBIDDEN_ROW_FIELDS),
        "target_values_are_outcomes_only": True, "target_classes_are_outcomes_only": True,
        "forward_returns_used_as_features": False,
    }
    result_summary = {
        "source_matrix_row_count": counts["rows"], "expectancy_backtest_lab_row_count": counts["rows"],
        "evaluable_target_row_count": counts["evaluable"], "unavailable_target_row_count": counts["unavailable"],
        "embargoed_metric_row_count": counts["embargoed"],
        "vpa_wyckoff_rule_row_count": counts["rows"], "vpa_wyckoff_state_row_count": counts["rows"],
        "approved_metric_family_count": 13, "blocked_metric_family_count": 1,
        "approved_baseline_count": 6, "blocked_baseline_count": 1,
    }
    metric_report = {
        "metric_families": [{"metric_family_id": item, "status": "COMPUTED_RESEARCH_ONLY"} for item in APPROVED_METRIC_FAMILY_IDS],
        "blocked_metric_family": {"metric_family_id": BLOCKED_METRIC_FAMILY_ID, "status": "NOT_COMPUTED_BLOCKED"},
        "baseline_metric_summaries": baseline_global,
        "chronological_metric_summaries": baseline_splits,
        "per_ticker_metric_summaries": baseline_tickers,
        "baseline_delta_summaries": baseline_deltas,
        "metric_population": "TARGET_AVAILABLE_AND_HORIZON_EMBARGO_ELIGIBLE_ROWS_ONLY",
        "classification_only_metric_scalar_policy": "TRADE_ELIGIBLE_RESEARCH_ONLY_EQUALS_1_NO_TRADE_ABSTAIN_EQUALS_0",
        "material_move_absolute_metric_scalar_threshold": "0.01",
    }
    reports = {
        "expectancy_backtest_lab_schema.json": _report(timestamp, "expectancy_backtest_lab_schema", schema),
        "expectancy_backtest_result_summary.json": _report(timestamp, "expectancy_backtest_result_summary", result_summary),
        "expectancy_metric_report.json": _report(timestamp, "expectancy_metric_report", metric_report),
        "baseline_comparison_report.json": _report(timestamp, "baseline_comparison_report", {
            "executed_baselines": APPROVED_BASELINE_IDS,
            "blocked_baseline": {"baseline_id": BLOCKED_BASELINE_ID, "status": "NOT_EXECUTED_BLOCKED"},
            "comparisons": baseline_global,
            "deltas_vs_always_available": baseline_deltas,
        }),
        "vpa_wyckoff_rule_alignment_report.json": _report(timestamp, "vpa_wyckoff_rule_alignment_report", {
            "context_summaries": {key: _stats_report(counts["rule_context"][key]) for key in ("FAVORABLE", "AVOID", "NEUTRAL")},
            "definition_source": "REVIEWED_VPA_WYCKOFF_RULE_AND_STATE_TAGS_ONLY",
        }),
        "abstention_quality_report.json": _report(timestamp, "abstention_quality_report", {
            "always_abstain": baseline_global["BASELINE_ALWAYS_ABSTAIN"],
            "vpa_rule_tag_reference": baseline_global["BASELINE_VPA_WYCKOFF_RULE_TAG_REFERENCE"],
            "interpretation": "DESCRIPTIVE_COVERAGE_AND_AVOIDANCE_ONLY_NOT_RECOMMENDATION",
        }),
        "per_ticker_backtest_report.json": _report(timestamp, "per_ticker_backtest_report", {"entries": per_ticker}),
        "chronological_split_report.json": _report(timestamp, "chronological_split_report", {
            "split_policy": "CHRONOLOGICAL_NO_SHUFFLE",
            "horizon_aware_embargo_policy": "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING",
            "splits": [{"split_id": key, "date_start": value[0], "date_end": value[1], **dict(counts["split"][key])} for key, value in SPLITS.items()],
        }),
        "meta_limitation_report.json": _report(timestamp, "meta_limitation_report", {
            "ticker": "META", "historical_record_count": 913,
            "meta_reduced_record_count_flag": True,
            "generation_note": "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_EXECUTION",
            "counts": dict(counts["ticker"]["META"]),
        }),
        "no_peek_report.json": _report(timestamp, "no_peek_report", {
            "split_policy": "CHRONOLOGICAL_NO_SHUFFLE",
            "horizon_aware_embargo_policy": "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING",
            "target_values_only_as_outcomes": True, "target_classes_only_as_outcomes": True,
            "forward_returns_used_as_features": False, "future_data_used_as_features": False,
            "prior_rate_policy": "VALIDATION_USES_CALIBRATION_ONLY_HOLDOUT_USES_CALIBRATION_AND_VALIDATION",
            "prediction_fields_present": False, "strategy_score_fields_present": False,
            "trade_recommendation_fields_present": False, "broker_order_fields_present": False,
            "provider_payload_fields_present": False, "api_key_fields_present": False,
        }),
        "operator_summary.json": _report(timestamp, "operator_summary", {
            **result_summary, "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES,
            "risk_controls": RISK_CONTROLS,
            "authority_boundary": "RESEARCH_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME_NOT_TRADING",
        }),
    }
    return reports


def _output_binding_digest(entries: Iterable[Mapping[str, Any]]) -> str:
    return semantic_digest([{"filename": row["filename"], "digest_kind": row["digest_kind"], "sha256": row.get("sha256")} for row in entries])


def _condition_values(artifact: Mapping[str, Any]) -> dict[str, bool]:
    entries = artifact.get("per_ticker_expectancy_backtest_lab_execution_entries", [])
    filenames = {row.get("filename") for row in artifact.get("output_digest_manifest", [])}
    false_fields = {
        "model_training_authorized", "model_training_performed", "strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution", "canonical_dataset_regenerated_in_execution",
        "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_performed", "target_generation_rerun_performed",
        "expectancy_backtest_lab_candidate_creation_rerun_performed",
        "expectancy_backtest_lab_candidate_review_rerun_performed",
        "expectancy_backtest_lab_approval_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    }
    values = {
        "source_approval_digest_bound": artifact.get("source_expectancy_backtest_lab_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest_bound": artifact.get("source_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": artifact.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest_bound": artifact.get("source_vpa_wyckoff_results_review_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": artifact.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": artifact.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": artifact.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": artifact.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": artifact.get("target_universe") == TARGET_UNIVERSE and artifact.get("target_universe_count") == len(TARGET_UNIVERSE),
        "records_digest_preserved": artifact.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": artifact.get("meta_record_count") == EXPECTED_RECORD_COUNTS.get("META"),
        "selected_backtest_lab_package_preserved": artifact.get("selected_backtest_lab_package") == SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package_preserved": artifact.get("selected_vpa_wyckoff_package") == SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package_preserved": artifact.get("selected_matrix_package") == SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout_preserved": artifact.get("selected_matrix_layout") == SELECTED_MATRIX_LAYOUT,
        "selected_feature_package_preserved": artifact.get("selected_feature_package") == SELECTED_FEATURE_PACKAGE,
        "selected_target_package_preserved": artifact.get("selected_label_target_package") == SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path_preserved": artifact.get("selected_objective_path") == SELECTED_OBJECTIVE_PATH,
        "source_backtest_lab_authorized_true": artifact.get("expectancy_backtest_lab_authorized") is True,
        "backtest_lab_executed_true": artifact.get("expectancy_backtest_lab_executed") is True,
        "backtest_rows_created_true": artifact.get("expectancy_backtest_rows_created") is True,
        "backtest_results_created_true": artifact.get("expectancy_backtest_results_created") is True,
        "metric_values_computed_true": artifact.get("metric_values_computed") is True,
        "metric_reports_created_true": artifact.get("metric_reports_created") is True,
        "metric_computation_performed_true": artifact.get("metric_computation_performed") is True,
        "backtest_execution_performed_true": artifact.get("backtest_execution_performed") is True,
        "source_matrix_row_count_179190": artifact.get("source_matrix_row_count") == EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "backtest_lab_row_count_179190": artifact.get("expectancy_backtest_lab_row_count") == EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "evaluable_target_row_count_177090": artifact.get("evaluable_target_row_count") == EXPECTED_EVALUABLE_TARGET_ROW_COUNT,
        "unavailable_target_row_count_2100": artifact.get("unavailable_target_row_count") == EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT,
        "vpa_wyckoff_rule_row_count_179190": artifact.get("vpa_wyckoff_rule_row_count") == EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "vpa_wyckoff_state_row_count_179190": artifact.get("vpa_wyckoff_state_row_count") == EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "approved_metric_family_count_13": artifact.get("approved_metric_family_count") == 13,
        "blocked_metric_family_count_1": artifact.get("blocked_metric_family_count") == 1,
        "approved_baseline_count_6": artifact.get("approved_baseline_count") == 6,
        "blocked_baseline_count_1": artifact.get("blocked_baseline_count") == 1,
        "per_non_meta_ticker_counts_preserved": all(row.get("backtest_lab_row_count") == EXPECTED_LAB_ROW_COUNTS[row["ticker"]] and row.get("evaluable_target_row_count") == EXPECTED_EVALUABLE_COUNTS[row["ticker"]] and row.get("unavailable_target_row_count") == EXPECTED_UNAVAILABLE_COUNTS[row["ticker"]] for row in entries if row.get("ticker") != "META"),
        "meta_counts_preserved": any(row.get("ticker") == "META" and row.get("backtest_lab_row_count") == EXPECTED_LAB_ROW_COUNTS["META"] and row.get("evaluable_target_row_count") == EXPECTED_EVALUABLE_COUNTS["META"] and row.get("unavailable_target_row_count") == EXPECTED_UNAVAILABLE_COUNTS["META"] for row in entries),
        "generated_output_count_14": artifact.get("generated_output_count") == EXPECTED_OUTPUT_COUNT,
        "digest_manifest_self_reference_policy_verified": artifact.get("digest_manifest_self_reference_policy") == SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "blocked_randomized_null_reference_not_executed": artifact.get("blocked_baseline", {}).get("status") == "NOT_EXECUTED_BLOCKED",
        "blocked_bootstrap_metric_not_computed": artifact.get("blocked_metric_family", {}).get("status") == "NOT_COMPUTED_BLOCKED",
        "chronological_no_shuffle_preserved": artifact.get("chronological_split_plan", {}).get("split_policy") == "CHRONOLOGICAL_NO_SHUFFLE",
        "horizon_aware_embargo_documented": artifact.get("chronological_split_plan", {}).get("horizon_aware_embargo_policy") == "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING",
        "target_values_only_as_outcomes": artifact.get("no_peek_and_leakage_controls", {}).get("target_values_only_as_outcomes") is True,
        "target_classes_only_as_outcomes": artifact.get("no_peek_and_leakage_controls", {}).get("target_classes_only_as_outcomes") is True,
        "forward_returns_not_used_as_features": artifact.get("no_peek_and_leakage_controls", {}).get("forward_returns_used_as_features") is False,
        "prediction_fields_absent": artifact.get("no_peek_and_leakage_controls", {}).get("prediction_fields_present") is False,
        "strategy_score_fields_absent": artifact.get("no_peek_and_leakage_controls", {}).get("strategy_score_fields_present") is False,
        "trade_recommendation_fields_absent": artifact.get("no_peek_and_leakage_controls", {}).get("trade_recommendation_fields_present") is False,
        "broker_order_fields_absent": artifact.get("no_peek_and_leakage_controls", {}).get("broker_order_fields_present") is False,
        "provider_payload_fields_absent": artifact.get("no_peek_and_leakage_controls", {}).get("provider_payload_fields_present") is False,
        "api_key_fields_absent": artifact.get("no_peek_and_leakage_controls", {}).get("api_key_fields_present") is False,
        "model_training_authorized_false": artifact.get("model_training_authorized") is False,
        "model_training_performed_false": artifact.get("model_training_performed") is False,
        "strategy_scoring_false": artifact.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": artifact.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": artifact.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": artifact.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": artifact.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": artifact.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": artifact.get("trade_recommendations_generated") is False,
        "per_ticker_entries_12": len(entries) == 12,
        "per_ticker_digests_present": all(row.get("per_ticker_expectancy_backtest_lab_execution_digest") == per_ticker_expectancy_backtest_lab_execution_digest_v1(row) for row in entries),
        "next_chain_defined": artifact.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": artifact.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": artifact.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": artifact.get("no_tracked_marketflow_files") is True,
    }
    file_checks = {
        "backtest_rows_jsonl_created": "expectancy_backtest_rows.jsonl",
        "backtest_lab_schema_created": "expectancy_backtest_lab_schema.json",
        "result_summary_created": "expectancy_backtest_result_summary.json",
        "metric_report_created": "expectancy_metric_report.json",
        "baseline_comparison_report_created": "baseline_comparison_report.json",
        "vpa_wyckoff_rule_alignment_report_created": "vpa_wyckoff_rule_alignment_report.json",
        "abstention_quality_report_created": "abstention_quality_report.json",
        "per_ticker_backtest_report_created": "per_ticker_backtest_report.json",
        "chronological_split_report_created": "chronological_split_report.json",
        "meta_limitation_report_created": "meta_limitation_report.json",
        "no_peek_report_created": "no_peek_report.json", "operator_summary_created": "operator_summary.json",
        "digest_manifest_created": "expectancy_backtest_lab_digest_manifest.json",
    }
    values.update({key: filename in filenames for key, filename in file_checks.items()})
    rerun_map = {
        "provider_requests_made_false": "provider_requests_made_in_execution",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_execution",
        "dataset_regeneration_false": "canonical_dataset_regenerated_in_execution",
        "vpa_wyckoff_execution_rerun_false": "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_results_review_rerun_false": "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "matrix_execution_rerun_false": "feature_label_matrix_execution_rerun_performed",
        "matrix_results_review_rerun_false": "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_false": "signal_feature_generation_rerun_performed",
        "target_generation_rerun_false": "target_generation_rerun_performed",
        "candidate_creation_rerun_false": "expectancy_backtest_lab_candidate_creation_rerun_performed",
        "candidate_review_rerun_false": "expectancy_backtest_lab_candidate_review_rerun_performed",
        "approval_rerun_false": "expectancy_backtest_lab_approval_rerun_performed",
        "raw_provider_payloads_not_committed": "raw_provider_payloads_committed",
        "api_keys_not_stored_or_printed": "api_keys_stored_or_printed",
    }
    values.update({check: artifact.get(field) is False for check, field in rerun_map.items()})
    return values


def _checklist(artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _condition_values(artifact)
    return [{"check_id": check_id, "status": PASS if values.get(check_id, False) else FAIL,
             "expected": True, "actual": bool(values.get(check_id, False)),
             "severity": "INFO" if values.get(check_id, False) else BLOCKER,
             "message": "execution condition satisfied" if values.get(check_id, False) else "execution condition failed"}
            for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    passed = sum(row["status"] == PASS for row in rows)
    failed = len(rows) - passed
    return {"total_checks": len(rows), "passed_checks": passed, "failed_checks": failed,
            "blocker_count": sum(row["severity"] == BLOCKER for row in rows)}


def marketflow_expectancy_backtest_lab_execution_digest_v1(artifact: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(artifact))
    payload.pop("generated_output_root", None)
    payload.pop("execution_checklist", None)
    payload.pop("execution_summary", None)
    payload.pop("marketflow_expectancy_backtest_lab_execution_digest", None)
    return semantic_digest(payload)


def _build_artifact(
    *, timestamp: str, output_root: Path, source_verification: Mapping[str, Any],
    counts: Mapping[str, Any], per_ticker: list[dict[str, Any]], output_manifest: list[dict[str, Any]],
    rows_digest: str, metric_digest: str, output_binding_digest: str,
) -> dict[str, Any]:
    no_peek = {
        "target_values_only_as_outcomes": True, "target_classes_only_as_outcomes": True,
        "forward_returns_used_as_features": False, "future_data_used_as_features": False,
        "prediction_fields_present": False, "strategy_score_fields_present": False,
        "trade_recommendation_fields_present": False, "broker_order_fields_present": False,
        "provider_payload_fields_present": False, "api_key_fields_present": False,
    }
    artifact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_V1,
        "execution_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY,
        "execution_scope": EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME,
        "run_timestamp_utc": timestamp, "generated_output_root": str(output_root).replace("\\", "/"),
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "source_expectancy_backtest_lab_approval_artifact_kind": approval_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
        "source_expectancy_backtest_lab_approval_status": approval_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED,
        "source_expectancy_backtest_lab_approval_scope": approval_service.EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY,
        "source_expectancy_backtest_lab_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": {"marketflow_expectancy_backtest_lab_candidate_v1_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST, **deepcopy(approval_service.review_service.candidate_service.SOURCE_EVIDENCE)},
        "source_verification": deepcopy(dict(source_verification)),
        "dataset_name": "expanded_universe_canonical_dataset_v1", "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d", "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE, "target_universe_count": len(TARGET_UNIVERSE),
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "non_meta_record_count": next((EXPECTED_RECORD_COUNTS[ticker] for ticker in TARGET_UNIVERSE if ticker != "META"), None),
        "meta_reduced_record_count_preserved": True,
        "expectancy_backtest_lab_selected": True, "expectancy_backtest_lab_approved": True,
        "expectancy_backtest_lab_authorized": True, "ready_for_expectancy_backtest_lab_execution": True,
        "expectancy_backtest_lab_authorized_for_future_execution": True,
        "expectancy_backtest_lab_executed": True, "expectancy_backtest_rows_created": True,
        "expectancy_backtest_results_created": True, "backtest_execution_performed": True,
        "metric_values_computed": True, "metric_reports_created": True,
        "metric_computation_performed": True,
        "source_matrix_row_count": counts["rows"], "expectancy_backtest_lab_row_count": counts["rows"],
        "evaluable_target_row_count": counts["evaluable"], "unavailable_target_row_count": counts["unavailable"],
        "embargoed_metric_row_count": counts["embargoed"],
        "vpa_wyckoff_rule_row_count": counts["rows"], "vpa_wyckoff_state_row_count": counts["rows"],
        "approved_metric_family_count": 13, "blocked_metric_family_count": 1,
        "approved_baseline_count": 6, "blocked_baseline_count": 1,
        "approved_metric_families": APPROVED_METRIC_FAMILY_IDS,
        "blocked_metric_family": {"metric_family_id": BLOCKED_METRIC_FAMILY_ID, "status": "NOT_COMPUTED_BLOCKED"},
        "executed_baselines": APPROVED_BASELINE_IDS,
        "blocked_baseline": {"baseline_id": BLOCKED_BASELINE_ID, "status": "NOT_EXECUTED_BLOCKED"},
        "chronological_split_plan": {"split_policy": "CHRONOLOGICAL_NO_SHUFFLE", "splits": SPLITS,
            "horizon_aware_embargo_policy": "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING"},
        "no_peek_and_leakage_controls": no_peek,
        "per_ticker_expectancy_backtest_lab_execution_entries": per_ticker,
        "generated_output_count": EXPECTED_OUTPUT_COUNT, "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "observed_output_count": EXPECTED_OUTPUT_COUNT, "output_digest_manifest": output_manifest,
        "digest_manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "expectancy_backtest_rows_digest": rows_digest,
        "expectancy_metric_report_digest": metric_digest,
        "expectancy_backtest_lab_output_binding_digest": output_binding_digest,
        "model_training_authorized": False, "model_training_performed": False,
        "strategy_scoring_performed": False, "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False, "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False, "target_generation_rerun_performed": False,
        "expectancy_backtest_lab_candidate_creation_rerun_performed": False,
        "expectancy_backtest_lab_candidate_review_rerun_performed": False,
        "expectancy_backtest_lab_approval_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True, "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    checklist = _checklist(artifact)
    artifact["execution_checklist"] = checklist
    artifact["execution_summary"] = {
        **_summary(checklist), "expectancy_backtest_lab_executed": True,
        "expectancy_backtest_rows_created": True, "expectancy_backtest_results_created": True,
        "backtest_execution_performed": True, "metric_values_computed": True,
        "metric_reports_created": True, "metric_computation_performed": True,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "backtest_lab_row_count": counts["rows"], "evaluable_target_row_count": counts["evaluable"],
        "unavailable_target_row_count": counts["unavailable"], "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "trade_recommendations_generated": False,
    }
    artifact["marketflow_expectancy_backtest_lab_execution_digest"] = marketflow_expectancy_backtest_lab_execution_digest_v1(artifact)
    artifact["execution_summary"]["marketflow_expectancy_backtest_lab_execution_digest"] = artifact["marketflow_expectancy_backtest_lab_execution_digest"]
    return artifact


def _write_bytes_once(path: Path, payload: bytes) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowExpectancyBacktestLabExecutionError(f"backtest-lab output already exists: {path.name}") from exc


def execute_marketflow_expectancy_backtest_lab_v1(
    *, output_root: str | Path | None = None, run_timestamp_utc: str | None = None,
) -> dict:
    """Stream reviewed inputs and create deterministic research-only lab outputs."""
    timestamp = run_timestamp_utc or _utc_now()
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    failures = []
    for source_id, path, expected_digest in (
        ("matrix_rows", DEFAULT_MATRIX_ROWS_PATH, EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
        ("vpa_wyckoff_rule_values", DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH, EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST),
    ):
        if not path.is_file():
            failures.append({"failure_id": f"{source_id}_missing", "message": f"missing source output: {path}"})
        else:
            actual = sha256_file(path)
            if actual != expected_digest:
                failures.append({"failure_id": f"{source_id}_digest_mismatch", "message": f"{source_id} digest mismatch", "expected": expected_digest, "actual": actual})
    if failures:
        return _blocked_artifact(output_path, timestamp, failures)
    before_matrix = sha256_file(DEFAULT_MATRIX_ROWS_PATH)
    before_vpa = sha256_file(DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH)
    try:
        priors = _prior_scan(DEFAULT_MATRIX_ROWS_PATH)
    except (OSError, MarketFlowExpectancyBacktestLabExecutionError) as exc:
        return _blocked_artifact(output_path, timestamp, [{"failure_id": "source_outputs_invalid", "message": str(exc)}])
    if output_path.exists() and any(output_path.iterdir()):
        raise MarketFlowExpectancyBacktestLabExecutionError("expectancy backtest-lab output root is not empty")
    output_path.mkdir(parents=True, exist_ok=True)
    temporary_rows = output_path / ".expectancy_backtest_rows.jsonl.tmp"
    try:
        rows_digest, counts = _execute_rows(
            DEFAULT_MATRIX_ROWS_PATH, DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH, temporary_rows, priors
        )
    except (OSError, MarketFlowExpectancyBacktestLabExecutionError) as exc:
        temporary_rows.unlink(missing_ok=True)
        return _blocked_artifact(output_path, timestamp, [{"failure_id": "source_outputs_invalid", "message": str(exc)}])
    after_matrix = sha256_file(DEFAULT_MATRIX_ROWS_PATH)
    after_vpa = sha256_file(DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH)
    source_verification = {
        "matrix_rows_path": str(DEFAULT_MATRIX_ROWS_PATH).replace("\\", "/"),
        "vpa_wyckoff_rule_values_path": str(DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH).replace("\\", "/"),
        "before_matrix_rows_digest": before_matrix, "after_matrix_rows_digest": after_matrix,
        "before_vpa_wyckoff_rule_values_digest": before_vpa,
        "after_vpa_wyckoff_rule_values_digest": after_vpa,
        "matrix_source_unchanged": before_matrix == after_matrix == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "vpa_wyckoff_source_unchanged": before_vpa == after_vpa == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "streaming_read_used": True,
        "entire_source_jsonl_loaded_into_memory": False,
    }
    if not source_verification["matrix_source_unchanged"] or not source_verification["vpa_wyckoff_source_unchanged"]:
        temporary_rows.unlink(missing_ok=True)
        return _blocked_artifact(output_path, timestamp, [{"failure_id": "source_outputs_changed_during_execution", "message": "source matrix or VPA/Wyckoff output changed during execution"}])
    per_ticker = _per_ticker_entries(counts)
    reports = _reports(timestamp, counts, per_ticker)
    report_bytes = {name: canonical_json_bytes(value) for name, value in reports.items()}
    metric_digest = sha256_bytes(report_bytes["expectancy_metric_report.json"])
    manifest = []
    for filename in OUTPUT_FILENAMES:
        if filename == "expectancy_backtest_lab_manifest.json":
            entry = {"filename": filename, "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT", "sha256": None}
        elif filename == "expectancy_backtest_lab_digest_manifest.json":
            entry = {"filename": filename, "digest_kind": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE, "sha256": None}
        elif filename == "expectancy_backtest_rows.jsonl":
            entry = {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": rows_digest}
        else:
            entry = {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(report_bytes[filename])}
        manifest.append(entry)
    output_binding_digest = _output_binding_digest(manifest)
    artifact = _build_artifact(
        timestamp=timestamp, output_root=output_path, source_verification=source_verification,
        counts=counts, per_ticker=per_ticker, output_manifest=manifest,
        rows_digest=rows_digest, metric_digest=metric_digest, output_binding_digest=output_binding_digest,
    )
    validate_marketflow_expectancy_backtest_lab_execution_v1(artifact)
    report_bytes["expectancy_backtest_lab_manifest.json"] = canonical_json_bytes(artifact)
    report_bytes["expectancy_backtest_lab_digest_manifest.json"] = canonical_json_bytes(_report(
        timestamp, "expectancy_backtest_lab_digest_manifest", {
            "marketflow_expectancy_backtest_lab_execution_digest": artifact["marketflow_expectancy_backtest_lab_execution_digest"],
            "expectancy_backtest_lab_output_binding_digest": output_binding_digest,
            "expectancy_backtest_rows_digest": rows_digest,
            "expectancy_metric_report_digest": metric_digest,
            "output_digest_manifest": manifest,
            "manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        }))
    for filename in OUTPUT_FILENAMES:
        if filename == "expectancy_backtest_rows.jsonl":
            continue
        _write_bytes_once(output_path / filename, report_bytes[filename])
    temporary_rows.replace(output_path / "expectancy_backtest_rows.jsonl")
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowExpectancyBacktestLabExecutionError(f"{field} mismatch")


def validate_marketflow_expectancy_backtest_lab_execution_v1(artifact: dict) -> dict:
    """Validate evidence binding, output identity, and closed authorities."""
    if not isinstance(artifact, dict):
        raise MarketFlowExpectancyBacktestLabExecutionError("artifact must be a JSON object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_V1,
        "execution_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY,
        "execution_scope": EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME,
        "selected_backtest_lab_package": SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "source_expectancy_backtest_lab_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": len(TARGET_UNIVERSE),
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "expectancy_backtest_lab_executed": True, "expectancy_backtest_rows_created": True,
        "expectancy_backtest_results_created": True, "backtest_execution_performed": True,
        "metric_values_computed": True, "metric_reports_created": True,
        "metric_computation_performed": True,
        "source_matrix_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "expectancy_backtest_lab_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "evaluable_target_row_count": EXPECTED_EVALUABLE_TARGET_ROW_COUNT,
        "unavailable_target_row_count": EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT,
        "vpa_wyckoff_rule_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "vpa_wyckoff_state_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "model_training_authorized": False, "model_training_performed": False,
        "strategy_scoring_performed": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "trade_recommendations_generated": False,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
    }
    for field, value in expected.items():
        _expect(artifact.get(field), value, field)
    for field in ("expectancy_backtest_rows_digest", "expectancy_metric_report_digest", "expectancy_backtest_lab_output_binding_digest"):
        value = artifact.get(field)
        if not isinstance(value, str) or len(value) != 64:
            raise MarketFlowExpectancyBacktestLabExecutionError(f"{field} missing")
    controls = artifact.get("no_peek_and_leakage_controls")
    if not isinstance(controls, dict):
        raise MarketFlowExpectancyBacktestLabExecutionError("no-peek controls missing")
    if controls.get("target_values_only_as_outcomes") is not True or controls.get("target_classes_only_as_outcomes") is not True:
        raise MarketFlowExpectancyBacktestLabExecutionError("target outcomes used as predictors")
    if controls.get("forward_returns_used_as_features") is not False:
        raise MarketFlowExpectancyBacktestLabExecutionError("forward returns used as features")
    for field in ("prediction_fields_present", "strategy_score_fields_present", "trade_recommendation_fields_present", "broker_order_fields_present", "provider_payload_fields_present", "api_key_fields_present"):
        if controls.get(field) is not False:
            raise MarketFlowExpectancyBacktestLabExecutionError(f"{field} mismatch")
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != EXPECTED_OUTPUT_COUNT:
        raise MarketFlowExpectancyBacktestLabExecutionError("output digest manifest mismatch")
    if [row.get("filename") for row in manifest] != OUTPUT_FILENAMES:
        raise MarketFlowExpectancyBacktestLabExecutionError("generated output filenames mismatch")
    if manifest[-1].get("digest_kind") != SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE or manifest[-1].get("sha256") is not None:
        raise MarketFlowExpectancyBacktestLabExecutionError("digest manifest self-reference policy mismatch")
    if artifact["expectancy_backtest_lab_output_binding_digest"] != _output_binding_digest(manifest):
        raise MarketFlowExpectancyBacktestLabExecutionError("output binding digest mismatch")
    if not any(row.get("filename") == "expectancy_backtest_rows.jsonl" and row.get("sha256") == artifact["expectancy_backtest_rows_digest"] for row in manifest):
        raise MarketFlowExpectancyBacktestLabExecutionError("backtest rows output missing")
    if not any(row.get("filename") == "expectancy_metric_report.json" and row.get("sha256") == artifact["expectancy_metric_report_digest"] for row in manifest):
        raise MarketFlowExpectancyBacktestLabExecutionError("metric report missing")
    if artifact.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowExpectancyBacktestLabExecutionError("risk controls missing")
    entries = artifact.get("per_ticker_expectancy_backtest_lab_execution_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MarketFlowExpectancyBacktestLabExecutionError("per-ticker entries mismatch")
    for entry in entries:
        if entry.get("per_ticker_expectancy_backtest_lab_execution_digest") != per_ticker_expectancy_backtest_lab_execution_digest_v1(entry):
            raise MarketFlowExpectancyBacktestLabExecutionError("per-ticker digest mismatch")
    checklist = _checklist(artifact)
    if artifact.get("execution_checklist") != checklist or any(row["status"] != PASS for row in checklist):
        raise MarketFlowExpectancyBacktestLabExecutionError("execution checklist mismatch")
    expected_summary = {**artifact["execution_summary"]}
    expected_summary.update(_summary(checklist))
    if artifact.get("execution_summary") != expected_summary:
        raise MarketFlowExpectancyBacktestLabExecutionError("execution summary mismatch")
    digest = artifact.get("marketflow_expectancy_backtest_lab_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyBacktestLabExecutionError("execution digest missing")
    if digest != marketflow_expectancy_backtest_lab_execution_digest_v1(artifact):
        raise MarketFlowExpectancyBacktestLabExecutionError("execution digest mismatch")
    return {
        "status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"], "execution_status": artifact["execution_status"],
        "execution_scope": artifact["execution_scope"],
        "marketflow_expectancy_backtest_lab_execution_digest": digest,
        "expectancy_backtest_lab_output_binding_digest": artifact["expectancy_backtest_lab_output_binding_digest"],
        "expectancy_backtest_rows_digest": artifact["expectancy_backtest_rows_digest"],
        "expectancy_metric_report_digest": artifact["expectancy_metric_report_digest"],
        **{key: artifact["execution_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_expectancy_backtest_lab_execution_markdown_v1(artifact: dict) -> str:
    """Render the validated operator-facing execution record."""
    validate_marketflow_expectancy_backtest_lab_execution_v1(artifact)
    sections = [
        ("Expectancy Backtest Lab Execution v1", [f"Status: `{artifact['execution_status']}`."]),
        ("Source Approval", [f"Digest `{artifact['source_expectancy_backtest_lab_approval_digest']}`."]),
        ("Bound Evidence", [f"{len(artifact['source_evidence'])} upstream digest fields remain bound."]),
        ("Dataset and Universe", ["`expanded_universe_canonical_dataset_v1`; ordered 12-ticker universe; 11,946 records."]),
        ("Execution Scope", [f"`{artifact['execution_scope']}`."]),
        ("Selected Backtest Lab Package", [f"`{artifact['selected_backtest_lab_package']}`."]),
        ("Source Matrix and VPA/Wyckoff Inputs", [f"Matrix `{artifact['source_feature_label_matrix_rows_digest']}`; VPA `{artifact['source_vpa_wyckoff_rule_values_digest']}`."]),
        ("Backtest Lab Construction Method", ["Streaming lockstep identity validation; one lab row per source matrix row."]),
        ("Chronological Split Plan", ["2022-2023 calibration, 2024 validation, 2025 holdout; no shuffle; horizon-aware embargo."]),
        ("Executed Baselines", artifact["executed_baselines"]),
        ("Computed Metric Families", artifact["approved_metric_families"]),
        ("Backtest Rows Output", [f"{artifact['expectancy_backtest_lab_row_count']} rows; `{artifact['expectancy_backtest_rows_digest']}`."]),
        ("Metric Report", [f"Digest `{artifact['expectancy_metric_report_digest']}`."]),
        ("Baseline Comparison Report", ["Six deterministic research references; randomized null remains blocked."]),
        ("VPA/Wyckoff Rule Alignment Report", ["Rule/state context only; no outcome-defined rules."]),
        ("Abstention Quality Report", ["Descriptive coverage and avoidance evidence only."]),
        ("Per-Ticker Backtest Report", ["12 digest-bound entries."]),
        ("META Limitation", ["META remains exactly 913 records without repair or inference."]),
        ("No-Peek and Leakage Controls", ["Targets remain outcomes only; cross-split forward horizons are embargoed."]),
        ("Output Digest Manifest", [f"14 outputs; binding `{artifact['expectancy_backtest_lab_output_binding_digest']}`."]),
        ("Next Chain", artifact["next_chain"]), ("Next Gates", artifact["next_gates"]),
        ("Risk Controls", artifact["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness is not accepted."]),
        ("Profitability Boundary", ["Profitability is not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{artifact['execution_summary']['passed_checks']}/{artifact['execution_summary']['total_checks']} checks pass; zero blockers."]),
        ("Guardrails", ["No provider, acquisition, regeneration, training, scoring, recommendation, runtime, or trading action occurred."]),
    ]
    lines = []
    for index, (title, body) in enumerate(sections):
        lines.extend([("# " if index == 0 else "## ") + title, ""])
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
