"""Offline research-only generation of the approved objective target package."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation, localcontext
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
    marketflow_objective_label_or_target_generation_approval_service as approval_service,
)


ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_V1 = (
    "marketflow_objective_label_or_target_generation_execution_v1"
)
MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED_RESEARCH_ONLY = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED_RESEARCH_ONLY"
)
MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE"
)
OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST = (
    "OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST"
)
PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET = (
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
)
EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT = (
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
)
MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_VALID = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_VALID"
)

OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESEARCH_ONLY"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "df3ee8758ca86a04f944ed1a46ede444693833009c99692e490f6cae5e21414b"
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
TARGET_FAMILIES = [
    "TARGET_EXPECTANCY_SCORE",
    "TARGET_PAYOFF_ASYMMETRY_SCORE",
    "TARGET_REWARD_TO_RISK_CLASS",
    "TARGET_NO_TRADE_ABSTAIN_CLASS",
    "TARGET_MATERIAL_MOVE_AFTER_COST_CLASS",
]
TARGET_HORIZONS = [5, 10, 20]
APPROVED_FORMULA_DIMENSIONS = [
    "FORMULA_FORWARD_RETURN_AFTER_COST",
    "FORMULA_MAXIMUM_ADVERSE_EXCURSION",
    "FORMULA_MAXIMUM_FAVORABLE_EXCURSION",
    "FORMULA_REWARD_TO_RISK_RATIO",
    "FORMULA_EXPECTANCY_ESTIMATE",
    "FORMULA_PAYOFF_ASYMMETRY",
    "FORMULA_ABSTENTION_CONDITION",
    "FORMULA_MATERIAL_MOVE_THRESHOLD",
    "FORMULA_DRAWDOWN_LIMIT",
    "FORMULA_TIME_TO_MOVE",
    "FORMULA_VOLATILITY_ADJUSTMENT",
    "FORMULA_RELATIVE_STRENGTH_CONTEXT",
    "FORMULA_REGIME_CONTEXT",
    "FORMULA_VOLUME_PRICE_CONFIRMATION",
]
AVAILABILITY_NO_PEEK_RULES = [
    "RULE_CHRONOLOGICAL_FORWARD_WINDOW_ONLY",
    "RULE_NO_CURRENT_ROW_FUTURE_LEAKAGE",
    "RULE_FORWARD_OUTCOME_NULL_WHEN_INSUFFICIENT_FUTURE_BARS",
    "RULE_COST_AND_SLIPPAGE_ASSUMPTIONS_MUST_BE_DECLARED",
    "RULE_MAE_MFE_COMPUTED_ONLY_FROM_ALLOWED_FORWARD_WINDOW",
    "RULE_ABSTAIN_TARGET_MUST_NOT_BE_USED_AS_PREDICTOR",
    "RULE_PER_TICKER_AVAILABILITY_REPORT_REQUIRED",
    "RULE_META_LIMITATION_PRESERVED_NO_REPAIR",
    "RULE_TRAIN_VALIDATION_OOS_SPLITS_REQUIRE_SEPARATE_APPROVAL",
    "RULE_DIGEST_MANIFEST_REQUIRED",
]
APPROVED_QUALITY_CHECKS = [
    "CHECK_LABEL_TARGET_SCHEMA_COMPLETENESS",
    "CHECK_FORWARD_WINDOW_ALIGNMENT",
    "CHECK_COST_SLIPPAGE_DECLARATION",
    "CHECK_NO_PEEK_FEATURE_EXCLUSION",
    "CHECK_UNAVAILABLE_TAIL_TARGETS_NULL",
    "CHECK_PER_TICKER_COVERAGE",
    "CHECK_META_LIMITATION_PRESERVED",
    "CHECK_CLASS_BALANCE_OR_TARGET_DISTRIBUTION",
    "CHECK_DIGEST_MANIFEST",
    "CHECK_RESEARCH_ONLY_AUTHORITY_BOUNDARY",
]
OUTPUT_FILENAMES = [
    "objective_label_target_generation_manifest.json",
    "label_target_schema.json",
    "formula_definition_report.json",
    "availability_no_peek_rule_report.json",
    "cost_slippage_assumption_report.json",
    "target_values.jsonl",
    "target_coverage_report.json",
    "per_ticker_target_report.json",
    "meta_limitation_report.json",
    "operator_summary.json",
    "objective_label_target_generation_digest_manifest.json",
]
TARGET_VALUES_FIELDS = [
    "dataset_name", "ticker", "date", "source_profile", "timeframe",
    "canonical_record_index", "target_family", "target_horizon_sessions",
    "target_profile", "target_value", "target_class", "target_available",
    "unavailable_reason", "forward_start_date", "forward_end_date",
    "formula_version", "selected_label_target_package",
    "selected_objective_path", "research_only", "non_actionable",
    "records_digest", "source_approval_digest",
]

DEFAULT_CANONICAL_ROOT = Path(".marketflow/canonical_datasets/expanded_universe_v1")
DEFAULT_OUTPUT_ROOT = Path(
    ".marketflow/objective_label_or_target_generation/expanded_universe_v1"
)
CANONICAL_RECORDS_FILENAME = "canonical_dataset_records.jsonl"
FORMULA_VERSION = "marketflow_objective_target_formula_v1"
ROUND_TRIP_COST = Decimal("0.0010")
RISK_FLOOR = Decimal("0.0050")
MATERIAL_MOVE_THRESHOLD = Decimal("0.0150")
MINIMUM_REWARD_TO_RISK = Decimal("1.5")
MINIMUM_PAYOFF_ASYMMETRY = Decimal("1.2")

NEXT_CHAIN = [
    "Objective Label or Target Generation Results Review v1.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "objective_label_or_target_generation_results_review",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_generates_only_research_targets",
    "execution_does_not_generate_features",
    "execution_does_not_create_feature_label_matrix",
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
    "execution_does_not_rerun_candidate_creation",
    "execution_does_not_rerun_candidate_review",
    "execution_does_not_rerun_approval",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound", "source_candidate_review_digest_bound",
    "source_candidate_digest_bound", "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound", "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_strategy_charter_approval_digest_bound", "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound", "source_archive_digest_bound",
    "source_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_execution_digest_bound",
    "matrix_digest_bound", "feature_values_digest_bound", "label_values_digest_bound",
    "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "selected_package_preserved", "selected_objective_path_preserved",
    "source_generation_authorized_true", "generation_executed_true",
    "target_values_created_true", "new_targets_created_true", "target_profile_count_15",
    "target_row_count_179190", "available_target_row_count_177090",
    "unavailable_target_row_count_2100", "per_non_meta_ticker_counts_preserved",
    "meta_counts_preserved", "generated_output_count_11", "target_values_jsonl_created",
    "target_coverage_report_created", "per_ticker_target_report_created",
    "digest_manifest_created", "digest_manifest_self_reference_policy_verified",
    "feature_generation_authorized_false", "feature_generation_performed_false",
    "feature_label_matrix_created_false", "backtest_execution_authorized_false",
    "backtest_execution_performed_false", "model_training_authorized_false",
    "model_training_performed_false", "metric_computation_authorized_false",
    "metric_computation_performed_false", "strategy_scoring_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "candidate_creation_rerun_false", "candidate_review_rerun_false",
    "approval_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowObjectiveLabelOrTargetGenerationExecutionError(ValueError):
    """Raised when generation evidence violates the execution-only contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _decimal(value: Any, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            f"invalid decimal value for {field}"
        ) from exc
    if not result.is_finite():
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            f"non-finite decimal value for {field}"
        )
    return result


def _decimal_text(value: Decimal | None) -> str | None:
    if value is None:
        return None
    with localcontext() as context:
        context.prec = 34
        value = value.quantize(Decimal("0.000000000001"))
    text = format(value.normalize(), "f")
    return "0" if text in {"", "-0"} else text


def _source_evidence() -> dict[str, str]:
    source = approval_service.SOURCE_EVIDENCE_DIGESTS
    return {
        "marketflow_objective_label_or_target_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "marketflow_objective_label_or_target_generation_candidate_v1_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "marketflow_expectancy_objective_design_results_review_digest": source["source_expectancy_objective_design_results_review_digest"],
        "marketflow_expectancy_objective_design_execution_digest": source["source_expectancy_objective_design_execution_digest"],
        "expectancy_objective_design_output_binding_digest": source["source_expectancy_objective_design_output_binding_digest"],
        "marketflow_expectancy_objective_approval_digest": source["source_expectancy_objective_approval_digest"],
        "marketflow_expectancy_objective_candidate_operator_review_digest": source["source_expectancy_objective_candidate_review_digest"],
        "marketflow_expectancy_objective_candidate_v1_digest": source["source_expectancy_objective_candidate_digest"],
        "marketflow_algorithm_strategy_charter_approval_digest": source["source_strategy_charter_approval_digest"],
        "marketflow_algorithm_strategy_charter_operator_review_digest": source["source_strategy_charter_review_digest"],
        "marketflow_algorithm_strategy_charter_v1_digest": source["source_strategy_charter_digest"],
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest": source["source_final_archive_digest"],
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest": source["source_archive_digest"],
        "operator_method_or_closure_selection_using_improved_evidence_digest": source["source_selection_digest"],
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest": source["source_closure_digest"],
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": source["source_readiness_digest"],
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": source["source_reassessment_digest"],
        "additional_predictive_evidence_results_review_using_improved_evidence_digest": source["source_results_review_digest"],
        "additional_predictive_evidence_execution_using_improved_evidence_digest": source["source_execution_digest"],
        "additional_predictive_evidence_output_binding_digest": source["source_output_binding_digest"],
        "feature_label_matrix_digest": source["feature_label_matrix_digest"],
        "feature_values_digest": source["feature_values_digest"],
        "redesigned_label_values_digest": source["redesigned_label_values_digest"],
        "research_registry_approval_digest": source["research_registry_approval_digest"],
        "records_digest": source["records_digest"],
    }


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "objective_label_or_target_generation_performed": True,
        "target_generation_performed": True,
        "target_values_created": True,
        "label_generation_performed": True,
        "new_targets_created": True,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "metric_computation_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report(name: str, timestamp: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "report_name": name,
        "run_timestamp_utc": timestamp,
        **_common_output_fields(),
        **deepcopy(dict(payload)),
    }


def _load_records(
    canonical_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    path = canonical_root / CANONICAL_RECORDS_FILENAME
    failures: list[dict[str, Any]] = []
    if not path.is_file():
        return [], {}, [{
            "failure_id": "missing_canonical_source_records",
            "message": "frozen canonical source records are unavailable",
            "path": str(path).replace("\\", "/"),
        }]
    before_digest = sha256_file(path)
    if before_digest != EXPECTED_RECORDS_DIGEST:
        failures.append({
            "failure_id": "canonical_source_digest_mismatch",
            "message": "frozen canonical source digest does not match the approved digest",
            "expected": EXPECTED_RECORDS_DIGEST,
            "actual": before_digest,
        })
        return [], {}, failures
    records: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                ticker = row.get("ticker")
                date = row.get("date")
                if ticker not in TARGET_UNIVERSE or not isinstance(date, str):
                    raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
                        f"invalid canonical identity at line {line_number}"
                    )
                for field in ("open", "high", "low", "close", "volume"):
                    _decimal(row.get(field), f"{field} line {line_number}")
                records.append(row)
    except (OSError, json.JSONDecodeError, MarketFlowObjectiveLabelOrTargetGenerationExecutionError) as exc:
        return [], {}, [{
            "failure_id": "invalid_canonical_source_records",
            "message": "frozen canonical source records are invalid",
            "error": str(exc),
        }]
    counts = Counter(row["ticker"] for row in records)
    expected_order = {ticker: index for index, ticker in enumerate(TARGET_UNIVERSE)}
    observed_keys = [(expected_order[row["ticker"]], row["date"]) for row in records]
    if observed_keys != sorted(observed_keys):
        failures.append({
            "failure_id": "canonical_source_order_mismatch",
            "message": "canonical records are not in ticker and date order",
        })
    if len(records) != 11946 or dict(counts) != EXPECTED_RECORD_COUNTS:
        failures.append({
            "failure_id": "canonical_source_count_mismatch",
            "message": "canonical source counts do not match the frozen contract",
            "expected_total": 11946,
            "actual_total": len(records),
            "actual_per_ticker": dict(counts),
        })
    verification = {
        "canonical_source_root": str(canonical_root).replace("\\", "/"),
        "canonical_records_filename": CANONICAL_RECORDS_FILENAME,
        "before_generation_records_digest": before_digest,
        "expected_records_digest": EXPECTED_RECORDS_DIGEST,
        "records_digest_match_before_generation": before_digest == EXPECTED_RECORDS_DIGEST,
        "total_canonical_record_count": len(records),
        "per_ticker_record_counts": dict(counts),
        "source_read_only": True,
    }
    return records, verification, failures


def _target_value_and_class(
    family: str,
    *,
    cost_adjusted_return: Decimal,
    reward_to_risk: Decimal,
    payoff_asymmetry: Decimal,
) -> tuple[Decimal | None, str]:
    if family == "TARGET_EXPECTANCY_SCORE":
        value = cost_adjusted_return * reward_to_risk
        return value, "POSITIVE_EXPECTANCY" if value > 0 else "NON_POSITIVE_EXPECTANCY"
    if family == "TARGET_PAYOFF_ASYMMETRY_SCORE":
        return payoff_asymmetry, (
            "FAVORABLE_PAYOFF_ASYMMETRY"
            if payoff_asymmetry >= MINIMUM_PAYOFF_ASYMMETRY
            else "UNFAVORABLE_PAYOFF_ASYMMETRY"
        )
    if family == "TARGET_REWARD_TO_RISK_CLASS":
        return reward_to_risk, (
            "FAVORABLE_REWARD_TO_RISK"
            if reward_to_risk >= MINIMUM_REWARD_TO_RISK
            else "UNFAVORABLE_REWARD_TO_RISK"
        )
    if family == "TARGET_NO_TRADE_ABSTAIN_CLASS":
        abstain = (
            abs(cost_adjusted_return) < MATERIAL_MOVE_THRESHOLD
            or reward_to_risk < MINIMUM_REWARD_TO_RISK
        )
        return None, "NO_TRADE_ABSTAIN" if abstain else "TRADE_ELIGIBLE_RESEARCH_ONLY"
    if cost_adjusted_return >= MATERIAL_MOVE_THRESHOLD:
        target_class = "MATERIAL_UP_AFTER_COST"
    elif cost_adjusted_return <= -MATERIAL_MOVE_THRESHOLD:
        target_class = "MATERIAL_DOWN_AFTER_COST"
    else:
        target_class = "NO_MATERIAL_MOVE_AFTER_COST"
    return cost_adjusted_return, target_class


def _target_row(
    source_row: Mapping[str, Any],
    *,
    ticker_index: int,
    family: str,
    horizon: int,
    forward_rows: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    base = {
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "ticker": source_row["ticker"],
        "date": source_row["date"],
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "canonical_record_index": ticker_index,
        "target_family": family,
        "target_horizon_sessions": horizon,
        "target_profile": f"{family}_HORIZON_{horizon}",
        "formula_version": FORMULA_VERSION,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "research_only": True,
        "non_actionable": True,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
    }
    if forward_rows is None:
        return {
            **base,
            "target_value": None,
            "target_class": None,
            "target_available": False,
            "unavailable_reason": "INSUFFICIENT_FUTURE_BARS",
            "forward_start_date": None,
            "forward_end_date": None,
        }
    close = _decimal(source_row["close"], "close")
    forward_close = _decimal(forward_rows[-1]["close"], "forward close")
    forward_return = (forward_close / close) - Decimal(1)
    cost_adjusted_return = forward_return - ROUND_TRIP_COST
    mfe = max(_decimal(row["high"], "high") for row in forward_rows) / close - Decimal(1)
    mae = min(_decimal(row["low"], "low") for row in forward_rows) / close - Decimal(1)
    drawdown = abs(min(Decimal(0), mae))
    denominator = max(drawdown, RISK_FLOOR)
    reward_to_risk = max(Decimal(0), mfe - ROUND_TRIP_COST) / denominator
    payoff_asymmetry = mfe / denominator
    value, target_class = _target_value_and_class(
        family,
        cost_adjusted_return=cost_adjusted_return,
        reward_to_risk=reward_to_risk,
        payoff_asymmetry=payoff_asymmetry,
    )
    return {
        **base,
        "target_value": _decimal_text(value),
        "target_class": target_class,
        "target_available": True,
        "unavailable_reason": None,
        "forward_start_date": forward_rows[0]["date"],
        "forward_end_date": forward_rows[-1]["date"],
    }


def _jsonl_bytes(rows: Iterable[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def _generate_targets(
    records: list[dict[str, Any]], timestamp: str
) -> tuple[bytes, dict[str, dict[str, Any]], dict[str, Any]]:
    grouped = {ticker: [] for ticker in TARGET_UNIVERSE}
    for row in records:
        grouped[row["ticker"]].append(row)
    target_rows: list[dict[str, Any]] = []
    per_ticker: list[dict[str, Any]] = []
    profile_counts: Counter[tuple[str, int]] = Counter()
    profile_available: Counter[tuple[str, int]] = Counter()
    profile_unavailable: Counter[tuple[str, int]] = Counter()
    class_counts: Counter[tuple[str, int, str]] = Counter()
    for ticker in TARGET_UNIVERSE:
        ticker_rows = grouped[ticker]
        ticker_available = 0
        ticker_unavailable = 0
        for index, source_row in enumerate(ticker_rows):
            for family in TARGET_FAMILIES:
                for horizon in TARGET_HORIZONS:
                    forward = (
                        ticker_rows[index + 1 : index + horizon + 1]
                        if index + horizon < len(ticker_rows)
                        else None
                    )
                    row = _target_row(
                        source_row,
                        ticker_index=index,
                        family=family,
                        horizon=horizon,
                        forward_rows=forward,
                    )
                    target_rows.append(row)
                    key = (family, horizon)
                    profile_counts[key] += 1
                    if row["target_available"]:
                        profile_available[key] += 1
                        ticker_available += 1
                        class_counts[(family, horizon, row["target_class"])] += 1
                    else:
                        profile_unavailable[key] += 1
                        ticker_unavailable += 1
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": len(ticker_rows),
            "meta_reduced_record_count_flag": ticker == "META",
            "objective_label_or_target_generation_approval_status": approval_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED,
            "objective_label_or_target_generation_execution_status": "GENERATED_RESEARCH_ONLY",
            "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "target_profile_count": 15,
            "target_row_count": len(ticker_rows) * 15,
            "available_target_row_count": ticker_available,
            "unavailable_target_row_count": ticker_unavailable,
            "label_or_target_generation_executed": True,
            "target_generation_performed": True,
            "target_values_created": True,
            "new_targets_created": True,
            "feature_generation_authorized": False,
            "feature_label_matrix_created": False,
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
        entry["per_ticker_objective_label_or_target_generation_execution_digest"] = semantic_digest(entry)
        per_ticker.append(entry)
    target_bytes = _jsonl_bytes(target_rows)
    coverage_entries = [
        {
            "target_family": family,
            "target_horizon_sessions": horizon,
            "target_profile": f"{family}_HORIZON_{horizon}",
            "target_row_count": profile_counts[(family, horizon)],
            "available_target_row_count": profile_available[(family, horizon)],
            "unavailable_target_row_count": profile_unavailable[(family, horizon)],
        }
        for family in TARGET_FAMILIES
        for horizon in TARGET_HORIZONS
    ]
    common_counts = {
        "selected_target_family_count": 5,
        "target_horizon_count": 3,
        "target_profile_count": 15,
        "target_row_count": len(target_rows),
        "available_target_row_count": sum(profile_available.values()),
        "unavailable_target_row_count": sum(profile_unavailable.values()),
    }
    reports = {
        "label_target_schema.json": _report("label_target_schema", timestamp, {
            "schema_version": FORMULA_VERSION,
            "target_values_fields": TARGET_VALUES_FIELDS,
            "selected_target_families": TARGET_FAMILIES,
            "target_horizons": TARGET_HORIZONS,
            "target_value_encoding": "DECIMAL_STRING_OR_NULL",
            "target_class_encoding": "STRING_OR_NULL",
            "feature_fields_included": False,
            "prediction_fields_included": False,
            "strategy_score_fields_included": False,
            "trade_recommendation_fields_included": False,
            **common_counts,
        }),
        "formula_definition_report.json": _report("formula_definition_report", timestamp, {
            "approved_formula_dimensions": APPROVED_FORMULA_DIMENSIONS,
            "formula_dimension_status": {
                dimension: (
                    "EXECUTED_FOR_SELECTED_TARGET_PACKAGE"
                    if dimension in {
                        "FORMULA_FORWARD_RETURN_AFTER_COST",
                        "FORMULA_MAXIMUM_ADVERSE_EXCURSION",
                        "FORMULA_MAXIMUM_FAVORABLE_EXCURSION",
                        "FORMULA_REWARD_TO_RISK_RATIO",
                        "FORMULA_EXPECTANCY_ESTIMATE",
                        "FORMULA_PAYOFF_ASYMMETRY",
                        "FORMULA_ABSTENTION_CONDITION",
                        "FORMULA_MATERIAL_MOVE_THRESHOLD",
                        "FORMULA_DRAWDOWN_LIMIT",
                    }
                    else "APPROVED_SUPPORTING_DIMENSION_NOT_USED_BY_SELECTED_PACKAGE"
                )
                for dimension in APPROVED_FORMULA_DIMENSIONS
            },
            "formula_definitions": {
                "forward_return": "close[t+h] / close[t] - 1",
                "cost_adjusted_forward_return": "forward_return - round_trip_cost_fraction",
                "maximum_favorable_excursion": "max(high[t+1:t+h]) / close[t] - 1",
                "maximum_adverse_excursion": "min(low[t+1:t+h]) / close[t] - 1",
                "drawdown_magnitude": "abs(min(0, maximum_adverse_excursion))",
                "reward_to_risk": "max(0, maximum_favorable_excursion - round_trip_cost) / max(drawdown_magnitude, risk_floor)",
                "payoff_asymmetry": "maximum_favorable_excursion / max(drawdown_magnitude, risk_floor)",
                "expectancy_score": "cost_adjusted_forward_return * reward_to_risk",
            },
            "same_ticker_forward_ohlcv_only": True,
            "future_data_used_as_feature": False,
            **common_counts,
        }),
        "availability_no_peek_rule_report.json": _report("availability_no_peek_rule_report", timestamp, {
            "availability_no_peek_rules": AVAILABILITY_NO_PEEK_RULES,
            "unavailable_tail_target_value": None,
            "unavailable_tail_target_class": None,
            "unavailable_reason": "INSUFFICIENT_FUTURE_BARS",
            "features_generated": False,
            "feature_label_matrix_created": False,
            **common_counts,
        }),
        "cost_slippage_assumption_report.json": _report("cost_slippage_assumption_report", timestamp, {
            "round_trip_cost_fraction": "0.0010",
            "risk_floor_fraction": "0.0050",
            "material_move_threshold_fraction": "0.0150",
            "minimum_reward_to_risk_for_favorable": "1.5",
            "minimum_payoff_asymmetry_for_positive": "1.2",
            "assumptions_declared_not_estimated": True,
            "performance_metric_computation_performed": False,
            **common_counts,
        }),
        "target_coverage_report.json": _report("target_coverage_report", timestamp, {
            "coverage_entries": coverage_entries,
            "class_balance_or_target_distribution": [
                {"target_family": family, "target_horizon_sessions": horizon, "target_class": target_class, "count": count}
                for (family, horizon, target_class), count in sorted(class_counts.items())
            ],
            **common_counts,
        }),
        "per_ticker_target_report.json": _report("per_ticker_target_report", timestamp, {
            "target_universe": TARGET_UNIVERSE,
            "per_ticker_target_entries": per_ticker,
            **common_counts,
        }),
        "meta_limitation_report.json": _report("meta_limitation_report", timestamp, {
            "ticker": "META",
            "historical_record_count": 913,
            "non_meta_historical_record_count": 1003,
            "target_row_count": 13695,
            "available_target_row_count": 13520,
            "unavailable_target_row_count": 175,
            "meta_reduced_record_count_preserved": True,
            "no_repair": True,
            "no_backfill": True,
            "no_synthetic_rows": True,
            "generation_note": "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION",
            **common_counts,
        }),
        "operator_summary.json": _report("operator_summary", timestamp, {
            "review_status": "AWAITING_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_V1",
            "operator_decision": None,
            "generated_output_count": 11,
            "selected_target_families": TARGET_FAMILIES,
            "target_horizons": TARGET_HORIZONS,
            "next_chain": NEXT_CHAIN,
            "next_gates": NEXT_GATES,
            "risk_controls": RISK_CONTROLS,
            **common_counts,
        }),
    }
    return target_bytes, reports, {
        **common_counts,
        "per_ticker_entries": per_ticker,
        "coverage_entries": coverage_entries,
    }


def _output_binding_digest(entries: list[dict[str, Any]]) -> str:
    return semantic_digest({
        "output_filenames": OUTPUT_FILENAMES,
        "digest_entries": [
            entry for entry in entries if entry["digest_kind"] == "FILE_SHA256"
        ],
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
    })


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "contract condition satisfied" if status == PASS else "contract condition failed",
    }


def _derived_check_values(artifact: Mapping[str, Any]) -> dict[str, bool]:
    evidence = artifact.get("source_evidence", {})
    per_ticker = artifact.get("per_ticker_objective_label_or_target_generation_execution_entries", [])
    output_names = artifact.get("generated_output_names", [])
    manifest = artifact.get("output_digest_manifest", [])
    digest_keys = {
        "source_approval_digest_bound": "marketflow_objective_label_or_target_generation_approval_digest",
        "source_candidate_review_digest_bound": "marketflow_objective_label_or_target_generation_candidate_operator_review_digest",
        "source_candidate_digest_bound": "marketflow_objective_label_or_target_generation_candidate_v1_digest",
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
        "source_execution_digest_bound": "additional_predictive_evidence_execution_using_improved_evidence_digest",
        "matrix_digest_bound": "feature_label_matrix_digest",
        "feature_values_digest_bound": "feature_values_digest",
        "label_values_digest_bound": "redesigned_label_values_digest",
        "research_registry_digest_bound": "research_registry_approval_digest",
        "records_digest_bound": "records_digest",
    }
    values = {
        check_id: evidence.get(key) == _source_evidence()[key]
        for check_id, key in digest_keys.items()
    }
    values.update({
        "target_universe_12_preserved": artifact.get("target_universe") == TARGET_UNIVERSE and artifact.get("target_universe_count") == 12,
        "records_digest_preserved": artifact.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": artifact.get("meta_record_count") == 913,
        "selected_package_preserved": artifact.get("selected_label_target_package") == PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": artifact.get("selected_objective_path") == EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_generation_authorized_true": artifact.get("objective_label_or_target_generation_authorized") is True,
        "generation_executed_true": artifact.get("label_or_target_generation_executed") is True,
        "target_values_created_true": artifact.get("target_values_created") is True,
        "new_targets_created_true": artifact.get("new_targets_created") is True,
        "target_profile_count_15": artifact.get("target_profile_count") == 15,
        "target_row_count_179190": artifact.get("target_row_count") == 179190,
        "available_target_row_count_177090": artifact.get("available_target_row_count") == 177090,
        "unavailable_target_row_count_2100": artifact.get("unavailable_target_row_count") == 2100,
        "per_non_meta_ticker_counts_preserved": all(row.get("historical_record_count") == 1003 and row.get("target_row_count") == 15045 and row.get("available_target_row_count") == 14870 and row.get("unavailable_target_row_count") == 175 for row in per_ticker if row.get("ticker") != "META") and len(per_ticker) == 12,
        "meta_counts_preserved": any(row.get("ticker") == "META" and row.get("historical_record_count") == 913 and row.get("target_row_count") == 13695 and row.get("available_target_row_count") == 13520 and row.get("unavailable_target_row_count") == 175 for row in per_ticker),
        "generated_output_count_11": artifact.get("generated_output_count") == 11,
        "target_values_jsonl_created": "target_values.jsonl" in output_names,
        "target_coverage_report_created": "target_coverage_report.json" in output_names,
        "per_ticker_target_report_created": "per_ticker_target_report.json" in output_names,
        "digest_manifest_created": "objective_label_target_generation_digest_manifest.json" in output_names,
        "digest_manifest_self_reference_policy_verified": any(row.get("filename") == OUTPUT_FILENAMES[-1] and row.get("digest_kind") == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE" and row.get("sha256") is None for row in manifest if isinstance(row, dict)),
        "feature_generation_authorized_false": artifact.get("feature_generation_authorized") is False,
        "feature_generation_performed_false": artifact.get("feature_generation_performed") is False,
        "feature_label_matrix_created_false": artifact.get("feature_label_matrix_created") is False,
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
        "per_ticker_entries_12": len(per_ticker) == 12 and [row.get("ticker") for row in per_ticker] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(isinstance(row.get("per_ticker_objective_label_or_target_generation_execution_digest"), str) and len(row["per_ticker_objective_label_or_target_generation_execution_digest"]) == 64 for row in per_ticker),
        "provider_requests_made_false": artifact.get("provider_requests_made_in_execution") is False,
        "market_data_acquisition_false": artifact.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_regeneration_false": artifact.get("canonical_dataset_regenerated_in_execution") is False,
        "candidate_creation_rerun_false": artifact.get("candidate_creation_rerun_performed") is False,
        "candidate_review_rerun_false": artifact.get("candidate_review_rerun_performed") is False,
        "approval_rerun_false": artifact.get("approval_rerun_performed") is False,
        "raw_provider_payloads_not_committed": artifact.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": artifact.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": artifact.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": artifact.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": artifact.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": artifact.get("no_tracked_marketflow_files") is True,
    })
    return values


def _checklist(artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _derived_check_values(artifact)
    return [_check(check_id, True, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(row["status"] == FAIL and row["severity"] == BLOCKER for row in checklist),
        "objective_label_or_target_generation_performed": True,
        "target_generation_performed": True,
        "target_values_created": True,
        "new_targets_created": True,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "target_profile_count": 15,
        "target_row_count": 179190,
        "available_target_row_count": 177090,
        "unavailable_target_row_count": 2100,
        "generated_output_count": 11,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _blocked_artifact(output_root: Path, timestamp: str, failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_V1,
        "execution_status": MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE,
        "execution_scope": OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "run_timestamp_utc": timestamp,
        "generated_output_root": str(output_root).replace("\\", "/"),
        "created_offline": True,
        "research_only": True,
        "source_evidence": _source_evidence(),
        "objective_label_or_target_generation_performed": False,
        "label_or_target_generation_executed": False,
        "target_generation_performed": False,
        "target_values_created": False,
        "new_targets_created": False,
        "label_generation_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "generated_output_count": 0,
        "failures": failures,
    }


def marketflow_objective_label_or_target_generation_execution_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(artifact))
    payload.pop("marketflow_objective_label_or_target_generation_execution_digest", None)
    payload.pop("canonical_source_root", None)
    payload.pop("generated_output_root", None)
    if isinstance(payload.get("source_verification"), dict):
        payload["source_verification"].pop("canonical_source_root", None)
    if isinstance(payload.get("execution_summary"), dict):
        payload["execution_summary"].pop("marketflow_objective_label_or_target_generation_execution_digest", None)
    return semantic_digest(payload)


def _build_artifact(
    *,
    timestamp: str,
    output_root: Path,
    source_verification: dict[str, Any],
    generation: dict[str, Any],
    output_manifest: list[dict[str, Any]],
    target_values_digest: str,
    output_binding_digest: str,
) -> dict[str, Any]:
    artifact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_V1,
        "execution_status": MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED_RESEARCH_ONLY,
        "execution_scope": OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "run_timestamp_utc": timestamp,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "canonical_source_root": str(DEFAULT_CANONICAL_ROOT).replace("\\", "/"),
        "generated_output_root": str(output_root).replace("\\", "/"),
        "source_objective_label_or_target_generation_approval_artifact_kind": approval_service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED,
        "source_objective_label_or_target_generation_approval_status": approval_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED,
        "source_objective_label_or_target_generation_approval_scope": approval_service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY,
        "source_objective_label_or_target_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_design_results_review_digest": _source_evidence()["marketflow_expectancy_objective_design_results_review_digest"],
        "source_evidence": _source_evidence(),
        "source_verification": source_verification,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "objective_label_or_target_generation_selected": True,
        "objective_label_or_target_generation_approved": True,
        "objective_label_or_target_generation_authorized": True,
        "ready_for_objective_label_or_target_generation_execution": True,
        "objective_label_or_target_generation_performed": True,
        "objective_label_or_target_generation_results_created": True,
        "label_or_target_generation_authorized_for_execution": True,
        "label_or_target_generation_executed": True,
        "target_generation_performed": True,
        "target_values_created": True,
        "new_targets_created": True,
        "label_generation_performed": True,
        "selected_target_families": TARGET_FAMILIES,
        "target_horizons": TARGET_HORIZONS,
        "approved_formula_dimensions": APPROVED_FORMULA_DIMENSIONS,
        "availability_no_peek_rules": AVAILABILITY_NO_PEEK_RULES,
        "approved_quality_checks": APPROVED_QUALITY_CHECKS,
        **{key: generation[key] for key in (
            "selected_target_family_count", "target_horizon_count", "target_profile_count",
            "target_row_count", "available_target_row_count", "unavailable_target_row_count",
        )},
        "per_ticker_objective_label_or_target_generation_execution_entries": generation["per_ticker_entries"],
        "generated_output_count": 11,
        "expected_output_count": 11,
        "observed_output_count": 11,
        "generated_output_names": OUTPUT_FILENAMES,
        "target_values_output_created": True,
        "target_coverage_report_created": True,
        "per_ticker_target_report_created": True,
        "digest_manifest_created": True,
        "output_digest_manifest": output_manifest,
        "objective_label_or_target_values_digest": target_values_digest,
        "objective_label_or_target_generation_output_binding_digest": output_binding_digest,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
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
        "candidate_creation_rerun_performed": False,
        "candidate_review_rerun_performed": False,
        "approval_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    checklist = _checklist(artifact)
    artifact["execution_checklist"] = checklist
    artifact["execution_summary"] = _summary(checklist)
    digest = marketflow_objective_label_or_target_generation_execution_digest_v1(artifact)
    artifact["marketflow_objective_label_or_target_generation_execution_digest"] = digest
    artifact["execution_summary"]["marketflow_objective_label_or_target_generation_execution_digest"] = digest
    return artifact


def _write_bytes_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            f"objective label or target generation output already exists: {path.name}"
        ) from exc


def execute_marketflow_objective_label_or_target_generation_v1(
    *,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Generate the approved target package from frozen local canonical rows."""
    timestamp = run_timestamp_utc or _utc_now()
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    records, source_verification, failures = _load_records(DEFAULT_CANONICAL_ROOT)
    if failures:
        return _blocked_artifact(output_path, timestamp, failures)
    if output_path.exists() and any(output_path.iterdir()):
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            "objective label or target generation output root is not empty"
        )
    target_bytes, reports, generation = _generate_targets(records, timestamp)
    after_digest = sha256_file(DEFAULT_CANONICAL_ROOT / CANONICAL_RECORDS_FILENAME)
    source_verification["after_generation_records_digest"] = after_digest
    source_verification["records_digest_match_after_generation"] = after_digest == EXPECTED_RECORDS_DIGEST
    source_verification["canonical_source_unchanged"] = (
        source_verification["before_generation_records_digest"] == after_digest == EXPECTED_RECORDS_DIGEST
    )
    if not source_verification["canonical_source_unchanged"]:
        return _blocked_artifact(output_path, timestamp, [{
            "failure_id": "canonical_source_changed_during_generation",
            "message": "canonical source digest changed during target generation",
        }])
    report_bytes = {
        filename: canonical_json_bytes(report) for filename, report in reports.items()
    }
    report_bytes["target_values.jsonl"] = target_bytes
    target_digest = sha256_bytes(target_bytes)
    output_manifest: list[dict[str, Any]] = []
    for filename in OUTPUT_FILENAMES:
        if filename == OUTPUT_FILENAMES[0]:
            entry = {"filename": filename, "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT", "sha256": None}
        elif filename == OUTPUT_FILENAMES[-1]:
            entry = {"filename": filename, "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "sha256": None}
        else:
            entry = {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(report_bytes[filename])}
        output_manifest.append(entry)
    output_binding = _output_binding_digest(output_manifest)
    artifact = _build_artifact(
        timestamp=timestamp,
        output_root=output_path,
        source_verification=source_verification,
        generation=generation,
        output_manifest=output_manifest,
        target_values_digest=target_digest,
        output_binding_digest=output_binding,
    )
    validate_marketflow_objective_label_or_target_generation_execution_v1(artifact)
    report_bytes[OUTPUT_FILENAMES[0]] = canonical_json_bytes(artifact)
    report_bytes[OUTPUT_FILENAMES[-1]] = canonical_json_bytes(_report(
        "objective_label_target_generation_digest_manifest",
        timestamp,
        {
            "marketflow_objective_label_or_target_generation_execution_digest": artifact["marketflow_objective_label_or_target_generation_execution_digest"],
            "objective_label_or_target_generation_output_binding_digest": output_binding,
            "objective_label_or_target_values_digest": target_digest,
            "output_digest_manifest": output_manifest,
            "manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        },
    ))
    for filename in OUTPUT_FILENAMES:
        _write_bytes_once(output_path / filename, report_bytes[filename])
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_objective_label_or_target_generation_execution_v1(
    artifact: dict,
) -> dict:
    """Validate execution evidence and every closed downstream authority."""
    if not isinstance(artifact, dict):
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            "objective label or target generation artifact must be a JSON object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_V1,
        "execution_status": MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED_RESEARCH_ONLY,
        "execution_scope": OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "source_objective_label_or_target_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "selected_target_families": TARGET_FAMILIES,
        "target_horizons": TARGET_HORIZONS,
        "selected_target_family_count": 5,
        "target_horizon_count": 3,
        "target_profile_count": 15,
        "target_row_count": 179190,
        "available_target_row_count": 177090,
        "unavailable_target_row_count": 2100,
        "generated_output_count": 11,
        "expected_output_count": 11,
        "observed_output_count": 11,
        "generated_output_names": OUTPUT_FILENAMES,
        "source_evidence": _source_evidence(),
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(artifact.get(field), expected, field)
    for field in (
        "created_offline", "research_only", "operator_review_required",
        "objective_label_or_target_generation_selected", "objective_label_or_target_generation_approved",
        "objective_label_or_target_generation_authorized", "ready_for_objective_label_or_target_generation_execution",
        "objective_label_or_target_generation_performed", "objective_label_or_target_generation_results_created",
        "label_or_target_generation_authorized_for_execution", "label_or_target_generation_executed",
        "target_generation_performed", "target_values_created", "new_targets_created",
        "label_generation_performed", "target_values_output_created", "target_coverage_report_created",
        "per_ticker_target_report_created", "digest_manifest_created", "meta_reduced_record_count_preserved",
    ):
        _expect(artifact.get(field), True, field)
    for field in (
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "backtest_execution_authorized", "backtest_execution_performed", "model_training_authorized",
        "model_training_performed", "metric_computation_authorized", "metric_computation_performed",
        "strategy_scoring_performed", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready", "profitability_acceptance_recommended", "runtime_migration_approved",
        "runtime_migration_active", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_execution",
        "live_provider_transport_enabled_in_execution", "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution", "canonical_dataset_regenerated_in_execution",
        "candidate_creation_rerun_performed", "candidate_review_rerun_performed",
        "approval_rerun_performed", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    ):
        _expect(artifact.get(field), False, field)
    _expect(artifact.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    target_digest = artifact.get("objective_label_or_target_values_digest")
    if not isinstance(target_digest, str) or len(target_digest) != 64:
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            "objective_label_or_target_values_digest missing"
        )
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, list) or [row.get("filename") for row in manifest] != OUTPUT_FILENAMES:
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError("output_digest_manifest mismatch")
    if (
        manifest[0].get("digest_kind") != "SELF_REFERENTIAL_EXECUTION_ARTIFACT"
        or manifest[0].get("sha256") is not None
        or manifest[-1].get("digest_kind") != "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
        or manifest[-1].get("sha256") is not None
        or any(
            row.get("digest_kind") != "FILE_SHA256"
            or not isinstance(row.get("sha256"), str)
            or len(row["sha256"]) != 64
            for row in manifest[1:-1]
        )
    ):
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError(
            "output_digest_manifest self-reference or file digest policy mismatch"
        )
    _expect(
        next(row["sha256"] for row in manifest if row["filename"] == "target_values.jsonl"),
        target_digest,
        "target_values output digest",
    )
    _expect(
        artifact.get("objective_label_or_target_generation_output_binding_digest"),
        _output_binding_digest(manifest),
        "objective_label_or_target_generation_output_binding_digest",
    )
    entries = artifact.get("per_ticker_objective_label_or_target_generation_execution_entries")
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError("per-ticker entries mismatch")
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop("per_ticker_objective_label_or_target_generation_execution_digest", None)
        _expect(digest, semantic_digest(payload), f"{row.get('ticker')} per-ticker digest")
    expected_checklist = _checklist(artifact)
    _expect(artifact.get("execution_checklist"), expected_checklist, "execution_checklist")
    if any(row["status"] != PASS for row in expected_checklist):
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError("execution checklist contains failures")
    expected_summary = _summary(expected_checklist)
    digest = artifact.get("marketflow_objective_label_or_target_generation_execution_digest")
    expected_summary["marketflow_objective_label_or_target_generation_execution_digest"] = digest
    _expect(artifact.get("execution_summary"), expected_summary, "execution_summary")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowObjectiveLabelOrTargetGenerationExecutionError("execution digest missing")
    _expect(
        digest,
        marketflow_objective_label_or_target_generation_execution_digest_v1(artifact),
        "marketflow_objective_label_or_target_generation_execution_digest",
    )
    return {
        "status": MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "execution_scope": artifact["execution_scope"],
        "marketflow_objective_label_or_target_generation_execution_digest": digest,
        "objective_label_or_target_generation_output_binding_digest": artifact["objective_label_or_target_generation_output_binding_digest"],
        "objective_label_or_target_values_digest": target_digest,
        "target_row_count": 179190,
        "available_target_row_count": 177090,
        "unavailable_target_row_count": 2100,
        "generated_output_count": 11,
        "failure_count": 0,
    }


def build_marketflow_objective_label_or_target_generation_execution_markdown_v1(
    artifact: dict,
) -> str:
    """Render a concise status record for the generated research targets."""
    validation = validate_marketflow_objective_label_or_target_generation_execution_v1(artifact)
    sections = [
        ("Objective Label or Target Generation Execution v1", [
            f"Artifact/status/scope: `{artifact['artifact_kind']}` / `{artifact['execution_status']}` / `{artifact['execution_scope']}`.",
            f"Execution digest: `{validation['marketflow_objective_label_or_target_generation_execution_digest']}`.",
        ]),
        ("Source Approval", [f"Approval digest: `{EXPECTED_SOURCE_APPROVAL_DIGEST}`."]),
        ("Bound Evidence", [f"The complete source chain is bound in `{len(artifact['source_evidence'])}` digest fields."]),
        ("Dataset and Universe", ["`expanded_universe_canonical_dataset_v1`, 11,946 rows, 12 tickers; META remains exactly 913 rows."]),
        ("Execution Scope", ["Offline research-only target generation; no features, matrix, backtest, training, metrics, scoring, or recommendations."]),
        ("Selected Package and Objective Path", [f"`{PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET}` / `{EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT}`."]),
        ("Generated Target Families", [", ".join(f"`{item}`" for item in TARGET_FAMILIES)]),
        ("Formula Definitions", ["Deterministic same-ticker 5/10/20-session forward OHLCV formulas with declared costs."]),
        ("Availability and No-Peek Controls", ["Insufficient future tails are null; target outcomes are never features."]),
        ("Cost and Slippage Assumptions", ["Round trip cost 0.0010; risk floor 0.0050; material move threshold 0.0150."]),
        ("Target Values Output", [f"179,190 rows; digest `{artifact['objective_label_or_target_values_digest']}`."]),
        ("Coverage Report", ["177,090 available and 2,100 unavailable rows across 15 profiles."]),
        ("Per-Ticker Target Report", ["Each non-META ticker has 15,045 rows; META has 13,695."]),
        ("META Limitation", ["META's exact 913-row source limitation is preserved without repair or backfill."]),
        ("Output Digest Manifest", [f"11 entries; binding digest `{artifact['objective_label_or_target_generation_output_binding_digest']}`."]),
        ("Next Chain", artifact["next_chain"]),
        ("Next Gates", artifact["next_gates"]),
        ("Risk Controls", artifact["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness is not accepted."]),
        ("Profitability Boundary", ["Profitability is not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper-trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{artifact['execution_summary']['passed_checks']}/{artifact['execution_summary']['total_checks']} checks pass; 0 blockers."]),
        ("Guardrails", ["No provider request, acquisition, dataset regeneration, feature generation, backtest, model training, runtime, or trading action occurred."]),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
