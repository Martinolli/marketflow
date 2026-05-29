"""Service-only Monte Carlo forecast-vs-actual calibration joins."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.artifact_service import list_report_artifacts
from marketflow.services.backtest_calibration_service import read_backtest_results_csv


MC_FORECAST_SUMMARY_KIND = "mc_summary_json"
BACKTEST_RESULTS_KIND = "backtest_results_csv"

VALID_ACTUAL_OUTCOMES = {"TP_FIRST", "SL_FIRST", "NEITHER", "AMBIGUOUS"}
INVALID_OUTCOME = "INVALID"

ELIGIBLE = "eligible"
NOT_YET_MATURE = "not_yet_mature"
HORIZON_MISMATCH = "horizon_mismatch"
PARTIAL_FUTURE_WINDOW = "partial_future_window"
INVALID = "invalid"
AMBIGUOUS = "ambiguous"
UNMATCHED = "unmatched"
NOT_SCOREABLE = "not_scoreable"

DEFAULT_GROUP_COLUMNS = ("ticker", "timeframe", "model", "mc_horizon_bars")
SMALL_SAMPLE_THRESHOLD = 10
CAUTION_SAMPLE_THRESHOLD = 30

JOINED = "joined"
PREFERRED_JOIN = "preferred"
SECONDARY_JOIN = "secondary"
FALLBACK_LEVELS_JOIN = "fallback_levels"
NUMERIC_TOLERANCE = 1e-6


def _json_safe_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, TypeError, ValueError):
            pass
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    try:
        is_missing = pd.isna(value)
    except (TypeError, ValueError):
        is_missing = False
    try:
        if bool(is_missing):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _is_missing(value: Any) -> bool:
    value = _json_safe_value(value)
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _to_float(value: Any) -> float | None:
    value = _json_safe_value(value)
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def _to_int(value: Any) -> int | None:
    value = _json_safe_value(value)
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    if not parsed.is_integer():
        return None
    return int(parsed)


def _to_bool(value: Any) -> bool:
    value = _json_safe_value(value)
    if value is True:
        return True
    if value is False or value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return bool(value)
    return False


def _first_present(*values: Any) -> Any:
    for value in values:
        safe_value = _json_safe_value(value)
        if not _is_missing(safe_value):
            return safe_value
    return None


def _basename(value: Any) -> str | None:
    value = _json_safe_value(value)
    if _is_missing(value):
        return None
    return str(value).replace("\\", "/").rstrip("/").split("/")[-1] or None


def _join_key(*parts: Any) -> str | None:
    safe_parts = [_json_safe_value(part) for part in parts]
    if any(_is_missing(part) for part in safe_parts):
        return None
    return "|".join(str(part) for part in safe_parts)


def _append_reason(reason: str | None, note: str) -> str:
    if not reason:
        return note
    if note in {part.strip() for part in reason.split(";")}:
        return reason
    return f"{reason};{note}"


def normalize_actual_outcome(value: Any) -> str:
    """Normalize supported actual outcome labels, treating missing/unknown as INVALID."""

    if hasattr(value, "name") and not isinstance(value, (str, bytes, bytearray)):
        normalized = normalize_actual_outcome(getattr(value, "name"))
        if normalized != INVALID_OUTCOME:
            return normalized
    if hasattr(value, "value") and not isinstance(value, (str, bytes, bytearray)):
        normalized = normalize_actual_outcome(getattr(value, "value"))
        if normalized != INVALID_OUTCOME:
            return normalized

    value = _json_safe_value(value)
    if _is_missing(value):
        return INVALID_OUTCOME
    label = str(value).strip().upper()
    if label in VALID_ACTUAL_OUTCOMES or label == INVALID_OUTCOME:
        return label
    return INVALID_OUTCOME


def normalize_monte_carlo_forecast_row(
    data: dict[str, Any],
    *,
    path: str | Path | None = None,
) -> dict[str, Any]:
    source = dict(data) if isinstance(data, dict) else {}
    join_metadata = source.get("join_metadata") if isinstance(source.get("join_metadata"), dict) else {}
    params = source.get("params") if isinstance(source.get("params"), dict) else {}
    metrics = source.get("metrics_from_now") if isinstance(source.get("metrics_from_now"), dict) else {}
    calibration = source.get("calibration") if isinstance(source.get("calibration"), dict) else {}
    artifact_path = Path(path) if path is not None else None

    source_csv = _first_present(join_metadata.get("source_csv"), source.get("source_csv"), source.get("csv"))
    source_csv_path = _first_present(join_metadata.get("source_csv_path"), source.get("source_csv_path"))
    ticker = _first_present(join_metadata.get("ticker"), source.get("ticker"))
    timeframe = _first_present(join_metadata.get("timeframe"), source.get("timeframe"), source.get("tf"))

    return {
        "forecast_path": str(artifact_path) if artifact_path is not None else None,
        "forecast_file": artifact_path.name if artifact_path is not None else None,
        "ticker": ticker,
        "timeframe": timeframe,
        "source_csv": source_csv,
        "source_csv_path": source_csv_path,
        "source_report_dir": _first_present(join_metadata.get("source_report_dir"), source.get("source_report_dir")),
        "candidate_snapshot_file": _first_present(
            join_metadata.get("candidate_snapshot_file"),
            source.get("candidate_snapshot_file"),
        ),
        "signal_row_index": _to_int(join_metadata.get("signal_row_index")),
        "signal_timestamp": _json_safe_value(join_metadata.get("signal_timestamp")),
        "entry": _to_float(_first_present(join_metadata.get("entry"), params.get("entry"))),
        "stop_loss": _to_float(_first_present(join_metadata.get("stop_loss"), params.get("sl"))),
        "take_profit": _to_float(_first_present(join_metadata.get("take_profit"), params.get("tp"))),
        "risk_reward": _to_float(join_metadata.get("risk_reward")),
        "strategy_score": _to_float(join_metadata.get("strategy_score")),
        "wyckoff_phase": _json_safe_value(join_metadata.get("wyckoff_phase")),
        "wyckoff_event": _json_safe_value(join_metadata.get("wyckoff_event")),
        "trend": _json_safe_value(join_metadata.get("trend")),
        "join_key_preferred": _json_safe_value(join_metadata.get("join_key_preferred")),
        "join_key_secondary": _json_safe_value(join_metadata.get("join_key_secondary")),
        "metadata_version": _json_safe_value(join_metadata.get("metadata_version")),
        "model": _json_safe_value(params.get("model")),
        "model_used": _json_safe_value(calibration.get("model_used")),
        "mc_horizon_bars": _to_int(params.get("horizon_bars")),
        "paths": _to_int(params.get("paths")),
        "block_len": _to_int(params.get("block_len")),
        "seed": _to_int(params.get("seed")),
        "forecast_tp_probability": _to_float(metrics.get("pop_tp_first")),
        "forecast_sl_probability": _to_float(metrics.get("p_sl_first")),
        "forecast_neither_probability": _to_float(metrics.get("p_neither")),
        "forecast_R_mean": _to_float(metrics.get("R_mean")),
        "forecast_R_p50": _to_float(metrics.get("R_p50")),
        "forecast_R_p05": _to_float(metrics.get("R_p05")),
        "forecast_R_p95": _to_float(metrics.get("R_p95")),
        "forecast_t_hit_tp_median": _to_float(metrics.get("t_hit_tp_median")),
        "forecast_t_hit_sl_median": _to_float(metrics.get("t_hit_sl_median")),
    }


def read_monte_carlo_forecast_artifact(path: str | Path) -> dict[str, Any]:
    result = {
        "success": False,
        "path": str(path),
        "forecast_row": None,
        "errors": [],
        "warnings": [],
    }
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result

    if not isinstance(data, dict):
        result["errors"].append("Monte Carlo summary JSON must contain an object.")
        return result

    if not isinstance(data.get("join_metadata"), dict):
        result["warnings"].append("Monte Carlo summary JSON is missing join_metadata.")
    result["forecast_row"] = normalize_monte_carlo_forecast_row(data, path=path)
    result["success"] = True
    return result


def normalize_actual_outcome_row(row: dict[str, Any]) -> dict[str, Any]:
    source = dict(row) if isinstance(row, dict) else {}
    ticker = _json_safe_value(source.get("ticker"))
    timeframe = _json_safe_value(source.get("timeframe"))
    source_csv = _json_safe_value(source.get("source_csv"))
    candidate_snapshot_file = _json_safe_value(source.get("candidate_snapshot_file"))
    signal_row_index = _to_int(source.get("signal_row_index"))
    source_csv_basename = _basename(source_csv)

    return {
        "actual_ticker": ticker,
        "actual_timeframe": timeframe,
        "actual_source_csv": source_csv,
        "actual_candidate_snapshot_file": candidate_snapshot_file,
        "actual_signal_row_index": signal_row_index,
        "actual_signal_timestamp": _json_safe_value(source.get("signal_timestamp")),
        "actual_entry": _to_float(source.get("entry")),
        "actual_stop_loss": _to_float(source.get("stop_loss")),
        "actual_take_profit": _to_float(source.get("take_profit")),
        "actual_outcome": normalize_actual_outcome(source.get("outcome")),
        "actual_realized_R": _to_float(source.get("realized_R")),
        "actual_bars_to_hit": _to_int(source.get("bars_to_hit")),
        "actual_tie_break_policy": _json_safe_value(source.get("tie_break_policy")),
        "actual_horizon_bars": _to_int(source.get("horizon_bars")),
        "future_bars_available": _to_int(source.get("future_bars_available")),
        "evaluation_window_start_index": _to_int(source.get("evaluation_window_start_index")),
        "evaluation_window_end_index": _to_int(source.get("evaluation_window_end_index")),
        "signal_is_latest_row": _to_bool(source.get("signal_is_latest_row")),
        "neither_reason": _json_safe_value(source.get("neither_reason")),
        "backtest_success": _to_bool(source.get("backtest_success")),
        "outcome_error": _json_safe_value(source.get("outcome_error")),
        "actual_join_key_preferred": _join_key(ticker, timeframe, candidate_snapshot_file),
        "actual_join_key_secondary": _join_key(ticker, timeframe, source_csv_basename, signal_row_index),
    }


def read_actual_outcome_artifact(path: str | Path) -> dict[str, Any]:
    read_result = read_backtest_results_csv(path)
    result = {
        "success": bool(read_result.get("success")),
        "path": str(path),
        "actual_rows": [],
        "errors": list(read_result.get("errors") or []),
        "warnings": list(read_result.get("warnings") or []),
    }
    if not read_result.get("success"):
        return result
    result["actual_rows"] = [
        normalize_actual_outcome_row(row)
        for row in read_result.get("rows") or []
        if isinstance(row, dict)
    ]
    return result


def _index_actual_rows(
    actual_rows: list[dict[str, Any]],
    key_column: str,
) -> dict[str, list[tuple[int, dict[str, Any]]]]:
    index: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for position, row in enumerate(actual_rows):
        key = _json_safe_value(row.get(key_column))
        if _is_missing(key):
            continue
        index.setdefault(str(key), []).append((position, row))
    return index


def _unmatched_forecast_row(
    forecast_row: dict[str, Any],
    *,
    join_method: str | None,
    join_status: str,
    join_warning: str,
) -> dict[str, Any]:
    return {
        **dict(forecast_row),
        "join_method": join_method,
        "join_status": join_status,
        "join_warning": join_warning,
        "scoreable": False,
        "scoreable_reason": join_warning,
        "eligibility_status": join_status,
    }


def _match_exact(
    forecast_row: dict[str, Any],
    actual_index: dict[str, list[tuple[int, dict[str, Any]]]],
    forecast_key_column: str,
    used_actual_positions: set[int],
) -> tuple[int, dict[str, Any], str | None] | tuple[None, None, str | None]:
    forecast_key = _json_safe_value(forecast_row.get(forecast_key_column))
    if _is_missing(forecast_key):
        return None, None, None
    matches = actual_index.get(str(forecast_key), [])
    if not matches:
        return None, None, None
    available = [(position, row) for position, row in matches if position not in used_actual_positions]
    if len(matches) > 1 or len(available) != 1:
        return None, None, f"Ambiguous exact join for key `{forecast_key}`."
    return available[0][0], available[0][1], None


def _levels_match(forecast_row: dict[str, Any], actual_row: dict[str, Any]) -> bool:
    if _json_safe_value(forecast_row.get("ticker")) != _json_safe_value(actual_row.get("actual_ticker")):
        return False
    if _json_safe_value(forecast_row.get("timeframe")) != _json_safe_value(actual_row.get("actual_timeframe")):
        return False
    for forecast_column, actual_column in (
        ("entry", "actual_entry"),
        ("stop_loss", "actual_stop_loss"),
        ("take_profit", "actual_take_profit"),
    ):
        forecast_value = _to_float(forecast_row.get(forecast_column))
        actual_value = _to_float(actual_row.get(actual_column))
        if forecast_value is None or actual_value is None:
            return False
        if abs(forecast_value - actual_value) > NUMERIC_TOLERANCE:
            return False

    forecast_source = _basename(_first_present(forecast_row.get("source_csv"), forecast_row.get("source_csv_path")))
    actual_source = _basename(actual_row.get("actual_source_csv"))
    if forecast_source and actual_source and forecast_source != actual_source:
        return False
    return True


def _match_fallback(
    forecast_row: dict[str, Any],
    actual_rows: list[dict[str, Any]],
    used_actual_positions: set[int],
) -> tuple[int, dict[str, Any], str | None] | tuple[None, None, str | None]:
    matches = [
        (position, actual_row)
        for position, actual_row in enumerate(actual_rows)
        if position not in used_actual_positions and _levels_match(forecast_row, actual_row)
    ]
    if not matches:
        return None, None, None
    if len(matches) > 1:
        return None, None, "Ambiguous fallback level join."
    return matches[0][0], matches[0][1], None


def build_forecast_actual_join_rows(
    forecast_rows: list[dict[str, Any]],
    actual_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    forecasts = [dict(row) for row in forecast_rows or [] if isinstance(row, dict)]
    actuals = [dict(row) for row in actual_rows or [] if isinstance(row, dict)]
    warnings: list[str] = []
    errors: list[str] = []
    join_rows: list[dict[str, Any]] = []
    unmatched_forecasts: list[dict[str, Any]] = []
    used_actual_positions: set[int] = set()

    preferred_index = _index_actual_rows(actuals, "actual_join_key_preferred")
    secondary_index = _index_actual_rows(actuals, "actual_join_key_secondary")

    for forecast_row in forecasts:
        matched_position, matched_row, warning = _match_exact(
            forecast_row,
            preferred_index,
            "join_key_preferred",
            used_actual_positions,
        )
        join_method = PREFERRED_JOIN

        if warning:
            warnings.append(warning)
            unmatched_forecasts.append(
                _unmatched_forecast_row(
                    forecast_row,
                    join_method=join_method,
                    join_status=AMBIGUOUS,
                    join_warning=warning,
                )
            )
            continue

        if matched_row is None:
            matched_position, matched_row, warning = _match_exact(
                forecast_row,
                secondary_index,
                "join_key_secondary",
                used_actual_positions,
            )
            join_method = SECONDARY_JOIN
            if warning:
                warnings.append(warning)
                unmatched_forecasts.append(
                    _unmatched_forecast_row(
                        forecast_row,
                        join_method=join_method,
                        join_status=AMBIGUOUS,
                        join_warning=warning,
                    )
                )
                continue

        if matched_row is None:
            matched_position, matched_row, warning = _match_fallback(
                forecast_row,
                actuals,
                used_actual_positions,
            )
            join_method = FALLBACK_LEVELS_JOIN
            if warning:
                warnings.append(warning)
                unmatched_forecasts.append(
                    _unmatched_forecast_row(
                        forecast_row,
                        join_method=join_method,
                        join_status=AMBIGUOUS,
                        join_warning=warning,
                    )
                )
                continue

        if matched_row is None or matched_position is None:
            unmatched_forecasts.append(
                _unmatched_forecast_row(
                    forecast_row,
                    join_method=None,
                    join_status=UNMATCHED,
                    join_warning="No matching actual outcome row found.",
                )
            )
            continue

        used_actual_positions.add(matched_position)
        join_rows.append(
            build_joined_calibration_row(
                forecast_row,
                matched_row,
                join_method=join_method,
            )
        )

    unmatched_outcomes = [
        {**actual_row, "join_status": UNMATCHED, "join_warning": "No matching forecast row found."}
        for position, actual_row in enumerate(actuals)
        if position not in used_actual_positions
    ]

    return {
        "success": not errors,
        "join_rows": join_rows,
        "unmatched_forecasts": unmatched_forecasts,
        "unmatched_outcomes": unmatched_outcomes,
        "warnings": warnings,
        "errors": errors,
    }


def build_joined_calibration_row(
    forecast_row: dict[str, Any],
    actual_row: dict[str, Any],
    *,
    join_method: str,
    join_warning: str | None = None,
) -> dict[str, Any]:
    row = {
        "forecast_path": _json_safe_value(forecast_row.get("forecast_path")),
        "forecast_file": _json_safe_value(forecast_row.get("forecast_file")),
        "ticker": _json_safe_value(forecast_row.get("ticker")),
        "timeframe": _json_safe_value(forecast_row.get("timeframe")),
        "source_csv": _json_safe_value(forecast_row.get("source_csv")),
        "candidate_snapshot_file": _json_safe_value(forecast_row.get("candidate_snapshot_file")),
        "signal_row_index": _to_int(forecast_row.get("signal_row_index")),
        "signal_timestamp": _json_safe_value(forecast_row.get("signal_timestamp")),
        "model": _json_safe_value(forecast_row.get("model")),
        "model_used": _json_safe_value(forecast_row.get("model_used")),
        "mc_horizon_bars": _to_int(forecast_row.get("mc_horizon_bars")),
        "paths": _to_int(forecast_row.get("paths")),
        "forecast_tp_probability": _to_float(forecast_row.get("forecast_tp_probability")),
        "forecast_sl_probability": _to_float(forecast_row.get("forecast_sl_probability")),
        "forecast_neither_probability": _to_float(forecast_row.get("forecast_neither_probability")),
        "forecast_R_mean": _to_float(forecast_row.get("forecast_R_mean")),
        "actual_outcome": normalize_actual_outcome(actual_row.get("actual_outcome")),
        "actual_realized_R": _to_float(actual_row.get("actual_realized_R")),
        "actual_bars_to_hit": _to_int(actual_row.get("actual_bars_to_hit")),
        "actual_horizon_bars": _to_int(actual_row.get("actual_horizon_bars")),
        "future_bars_available": _to_int(actual_row.get("future_bars_available")),
        "signal_is_latest_row": _to_bool(actual_row.get("signal_is_latest_row")),
        "neither_reason": _json_safe_value(actual_row.get("neither_reason")),
        "backtest_success": _to_bool(actual_row.get("backtest_success")),
        "outcome_error": _json_safe_value(actual_row.get("outcome_error")),
        "tie_break_policy": _json_safe_value(actual_row.get("actual_tie_break_policy")),
        "join_method": join_method,
        "join_status": JOINED,
        "join_warning": join_warning,
        "horizon_match": None,
        "maturity_status": None,
        "scoreable": False,
        "scoreable_reason": None,
        "eligibility_status": NOT_SCOREABLE,
    }
    row.update(classify_forecast_actual_eligibility(row))
    row["actual_tp_event"] = 1 if row["actual_outcome"] == "TP_FIRST" else 0
    row["actual_sl_event"] = 1 if row["actual_outcome"] == "SL_FIRST" else 0
    row["actual_neither_event"] = 1 if row["actual_outcome"] == "NEITHER" and row["scoreable"] else 0
    return row


def classify_forecast_actual_eligibility(joined_row: dict[str, Any]) -> dict[str, Any]:
    row = dict(joined_row) if isinstance(joined_row, dict) else {}
    actual_outcome = normalize_actual_outcome(row.get("actual_outcome"))
    mc_horizon = _to_int(row.get("mc_horizon_bars"))
    actual_horizon = _to_int(row.get("actual_horizon_bars"))
    future_bars = _to_int(row.get("future_bars_available"))
    neither_reason = str(_json_safe_value(row.get("neither_reason")) or "").strip()
    backtest_success = _to_bool(row.get("backtest_success"))
    horizon_match = mc_horizon is not None and actual_horizon is not None and mc_horizon == actual_horizon
    reason: str | None = None

    if not backtest_success:
        reason = str(_json_safe_value(row.get("outcome_error")) or "").strip() or "backtest_not_successful"
        return {
            "horizon_match": horizon_match,
            "maturity_status": INVALID,
            "scoreable": False,
            "scoreable_reason": reason,
            "eligibility_status": INVALID,
        }

    if actual_outcome == INVALID_OUTCOME:
        return {
            "horizon_match": horizon_match,
            "maturity_status": INVALID,
            "scoreable": False,
            "scoreable_reason": "invalid_actual_outcome",
            "eligibility_status": INVALID,
        }

    if actual_outcome == "AMBIGUOUS":
        return {
            "horizon_match": horizon_match,
            "maturity_status": AMBIGUOUS,
            "scoreable": False,
            "scoreable_reason": "ambiguous_actual_outcome",
            "eligibility_status": AMBIGUOUS,
        }

    has_no_future_bars = future_bars == 0 or neither_reason == "no_future_bars_available"
    if has_no_future_bars:
        reason = "no_future_bars_available"
        if not horizon_match:
            reason = _append_reason(reason, HORIZON_MISMATCH)
        return {
            "horizon_match": horizon_match,
            "maturity_status": NOT_YET_MATURE,
            "scoreable": False,
            "scoreable_reason": reason,
            "eligibility_status": NOT_YET_MATURE,
        }

    if not horizon_match:
        return {
            "horizon_match": horizon_match,
            "maturity_status": HORIZON_MISMATCH,
            "scoreable": False,
            "scoreable_reason": HORIZON_MISMATCH,
            "eligibility_status": HORIZON_MISMATCH,
        }

    if future_bars is None:
        return {
            "horizon_match": horizon_match,
            "maturity_status": NOT_SCOREABLE,
            "scoreable": False,
            "scoreable_reason": "future_bars_available_missing",
            "eligibility_status": NOT_SCOREABLE,
        }

    if actual_horizon is not None and 0 < future_bars < actual_horizon:
        return {
            "horizon_match": horizon_match,
            "maturity_status": PARTIAL_FUTURE_WINDOW,
            "scoreable": False,
            "scoreable_reason": PARTIAL_FUTURE_WINDOW,
            "eligibility_status": PARTIAL_FUTURE_WINDOW,
        }

    return {
        "horizon_match": horizon_match,
        "maturity_status": ELIGIBLE,
        "scoreable": True,
        "scoreable_reason": None,
        "eligibility_status": ELIGIBLE,
    }


def _rate(count: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return count / denominator


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _numeric_values(rows: list[dict[str, Any]], column: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        value = _to_float(row.get(column))
        if value is not None:
            values.append(value)
    return values


def _small_sample_warning(count: int) -> str | None:
    if count < SMALL_SAMPLE_THRESHOLD:
        return "small_sample"
    if count < CAUTION_SAMPLE_THRESHOLD:
        return "caution_sample"
    if count < 100:
        return "directional_only"
    return None


def _brier_score(rows: list[dict[str, Any]], probability_column: str, event_column: str) -> float | None:
    errors: list[float] = []
    for row in rows:
        probability = _to_float(row.get(probability_column))
        event = _to_float(row.get(event_column))
        if probability is None or event is None:
            continue
        errors.append((probability - event) ** 2)
    return _mean(errors)


def _summary_for_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_rows = [dict(row) for row in rows or [] if isinstance(row, dict)]
    scoreable_rows = [row for row in source_rows if row.get("scoreable") is True]
    scoreable_count = len(scoreable_rows)
    joined_count = sum(1 for row in source_rows if row.get("join_status") == JOINED)
    unmatched_forecast_count = sum(1 for row in source_rows if row.get("join_status") == UNMATCHED)
    tp_actual_count = sum(1 for row in scoreable_rows if row.get("actual_outcome") == "TP_FIRST")
    sl_actual_count = sum(1 for row in scoreable_rows if row.get("actual_outcome") == "SL_FIRST")
    neither_actual_count = sum(1 for row in scoreable_rows if row.get("actual_outcome") == "NEITHER")

    tp_rate = _rate(tp_actual_count, scoreable_count)
    sl_rate = _rate(sl_actual_count, scoreable_count)
    neither_rate = _rate(neither_actual_count, scoreable_count)
    mean_tp_probability = _mean(_numeric_values(scoreable_rows, "forecast_tp_probability"))
    mean_sl_probability = _mean(_numeric_values(scoreable_rows, "forecast_sl_probability"))
    mean_neither_probability = _mean(_numeric_values(scoreable_rows, "forecast_neither_probability"))

    return {
        "sample_count": len(source_rows),
        "joined_count": joined_count,
        "scoreable_count": scoreable_count,
        "not_scoreable_count": len(source_rows) - scoreable_count,
        "eligible_count": sum(1 for row in source_rows if row.get("eligibility_status") == ELIGIBLE),
        "not_yet_mature_count": sum(1 for row in source_rows if row.get("eligibility_status") == NOT_YET_MATURE),
        "horizon_mismatch_count": sum(
            1
            for row in source_rows
            if row.get("eligibility_status") == HORIZON_MISMATCH or row.get("horizon_match") is False
        ),
        "partial_future_window_count": sum(
            1 for row in source_rows if row.get("eligibility_status") == PARTIAL_FUTURE_WINDOW
        ),
        "invalid_count": sum(1 for row in source_rows if row.get("eligibility_status") == INVALID),
        "ambiguous_count": sum(1 for row in source_rows if row.get("eligibility_status") == AMBIGUOUS),
        "unmatched_forecast_count": unmatched_forecast_count,
        "tp_actual_count": tp_actual_count,
        "sl_actual_count": sl_actual_count,
        "neither_actual_count": neither_actual_count,
        "tp_actual_rate": tp_rate,
        "sl_actual_rate": sl_rate,
        "neither_actual_rate": neither_rate,
        "mean_forecast_tp_probability": mean_tp_probability,
        "mean_forecast_sl_probability": mean_sl_probability,
        "mean_forecast_neither_probability": mean_neither_probability,
        "mean_realized_R": _mean(_numeric_values(scoreable_rows, "actual_realized_R")),
        "mean_forecast_R_mean": _mean(_numeric_values(scoreable_rows, "forecast_R_mean")),
        "forecast_vs_actual_tp_error": None if mean_tp_probability is None or tp_rate is None else mean_tp_probability - tp_rate,
        "forecast_vs_actual_sl_error": None if mean_sl_probability is None or sl_rate is None else mean_sl_probability - sl_rate,
        "forecast_vs_actual_neither_error": (
            None if mean_neither_probability is None or neither_rate is None else mean_neither_probability - neither_rate
        ),
        "brier_score_tp": _brier_score(scoreable_rows, "forecast_tp_probability", "actual_tp_event"),
        "brier_score_sl": _brier_score(scoreable_rows, "forecast_sl_probability", "actual_sl_event"),
        "brier_score_neither": _brier_score(scoreable_rows, "forecast_neither_probability", "actual_neither_event"),
        "small_sample_warning": _small_sample_warning(scoreable_count),
    }


def _available_group_columns(
    rows: list[dict[str, Any]],
    requested_columns: tuple[str, ...],
    warnings: list[str],
) -> list[str]:
    available_columns: list[str] = []
    for column in requested_columns:
        if any(column in row for row in rows):
            available_columns.append(column)
        else:
            warnings.append(f"Requested group column `{column}` is missing from all rows.")
    return available_columns


def _group_value(row: dict[str, Any], column: str) -> Any:
    value = _json_safe_value(row.get(column))
    if _is_missing(value):
        return "UNKNOWN"
    return value


def _group_key(values: tuple[Any, ...]) -> str:
    return "|".join(str(_json_safe_value(value)) for value in values)


def _grouped_summary_rows(rows: list[dict[str, Any]], group_columns: list[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for row in rows:
        key = tuple(_group_value(row, column) for column in group_columns)
        grouped.setdefault(key, []).append(row)

    summary_rows: list[dict[str, Any]] = []
    for key, group_rows in grouped.items():
        summary = _summary_for_rows(group_rows)
        group_values = dict(zip(group_columns, key))
        summary_rows.append({"group_key": _group_key(key), **group_values, **summary})
    return sorted(summary_rows, key=lambda row: str(row.get("group_key") or ""))


def summarize_forecast_calibration_rows(
    rows: list[dict[str, Any]],
    *,
    group_columns: tuple[str, ...] | list[str] | None = None,
) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    source_rows = [dict(row) for row in rows or [] if isinstance(row, dict)]
    requested_group_columns = tuple(group_columns) if group_columns is not None else DEFAULT_GROUP_COLUMNS

    if not source_rows:
        warnings.append("No Monte Carlo forecast calibration rows to summarize.")
        summary = _summary_for_rows([])
        return {
            "success": False,
            "count": 0,
            "summary": summary,
            "summary_rows": [summary],
            "grouped_summary_rows": [],
            "warnings": warnings,
            "errors": errors,
        }

    available_group_columns = _available_group_columns(source_rows, requested_group_columns, warnings)
    grouped_rows: list[dict[str, Any]] = []
    if available_group_columns:
        grouped_rows = _grouped_summary_rows(source_rows, available_group_columns)
    else:
        warnings.append("No requested group columns are available; grouped summary is empty.")

    summary = _summary_for_rows(source_rows)
    return {
        "success": True,
        "count": len(source_rows),
        "summary": summary,
        "summary_rows": [summary],
        "grouped_summary_rows": grouped_rows,
        "warnings": warnings,
        "errors": errors,
    }


def _is_mc_summary_artifact(artifact: dict[str, Any]) -> bool:
    kind = artifact.get("kind")
    name = str(artifact.get("name") or "").lower()
    return kind in {MC_FORECAST_SUMMARY_KIND, "mc_summary"} or name.endswith("_mc_summary.json")


def _is_backtest_results_artifact(artifact: dict[str, Any]) -> bool:
    name = str(artifact.get("name") or "").lower()
    return artifact.get("kind") == BACKTEST_RESULTS_KIND or ("_backtest_results" in name and name.endswith(".csv"))


def summarize_monte_carlo_calibration_folder(
    report_dir: str | Path,
    *,
    group_columns: tuple[str, ...] | list[str] | None = None,
) -> dict[str, Any]:
    report_path = Path(report_dir)
    warnings: list[str] = []
    errors: list[str] = []
    artifacts = list_report_artifacts(str(report_path))
    forecast_files = [artifact.get("path") for artifact in artifacts if _is_mc_summary_artifact(artifact) and artifact.get("path")]
    actual_files = [artifact.get("path") for artifact in artifacts if _is_backtest_results_artifact(artifact) and artifact.get("path")]

    forecast_rows: list[dict[str, Any]] = []
    actual_rows: list[dict[str, Any]] = []

    for forecast_file in forecast_files:
        read_result = read_monte_carlo_forecast_artifact(str(forecast_file))
        warnings.extend(f"{forecast_file}: {warning}" for warning in read_result.get("warnings") or [])
        if not read_result.get("success"):
            errors.extend(f"{forecast_file}: {error}" for error in read_result.get("errors") or [])
            continue
        forecast_row = read_result.get("forecast_row")
        if isinstance(forecast_row, dict):
            forecast_rows.append(forecast_row)

    for actual_file in actual_files:
        read_result = read_actual_outcome_artifact(str(actual_file))
        warnings.extend(f"{actual_file}: {warning}" for warning in read_result.get("warnings") or [])
        if not read_result.get("success"):
            errors.extend(f"{actual_file}: {error}" for error in read_result.get("errors") or [])
            continue
        actual_rows.extend(read_result.get("actual_rows") or [])

    join_result = build_forecast_actual_join_rows(forecast_rows, actual_rows)
    warnings.extend(join_result.get("warnings") or [])
    errors.extend(join_result.get("errors") or [])

    summary_input_rows = list(join_result.get("join_rows") or []) + list(join_result.get("unmatched_forecasts") or [])
    summary_result = summarize_forecast_calibration_rows(summary_input_rows, group_columns=group_columns)
    warnings.extend(summary_result.get("warnings") or [])
    errors.extend(summary_result.get("errors") or [])

    return {
        "success": bool(join_result.get("success")) and bool(summary_result.get("success")) and not errors,
        "report_dir": str(report_path),
        "forecast_file_count": len(forecast_files),
        "actual_file_count": len(actual_files),
        "forecast_rows": forecast_rows,
        "actual_rows": actual_rows,
        "join_rows": join_result.get("join_rows") or [],
        "unmatched_forecasts": join_result.get("unmatched_forecasts") or [],
        "unmatched_outcomes": join_result.get("unmatched_outcomes") or [],
        "summary": summary_result.get("summary") or {},
        "summary_rows": summary_result.get("summary_rows") or [],
        "grouped_summary_rows": summary_result.get("grouped_summary_rows") or [],
        "warnings": warnings,
        "errors": errors,
    }
