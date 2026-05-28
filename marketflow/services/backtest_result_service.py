"""Service orchestration for saved candidate snapshot backtest results."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.backtest_result_artifact_service import (
    backtest_result_row,
    write_backtest_results_csv,
)
from marketflow.services.backtest_service import evaluate_backtest_candidate_from_csv


def _is_truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        try:
            return bool(value) and not bool(pd.isna(value))
        except (TypeError, ValueError):
            return bool(value)
    return False


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def _candidate_row_is_evaluable(row: dict[str, Any]) -> tuple[bool, list[str]]:
    source = row if isinstance(row, dict) else {}
    reasons: list[str] = []

    if not _is_truthy(source.get("snapshot_success")):
        reasons.append("candidate snapshot is not valid")
    if _is_missing(source.get("source_csv")):
        reasons.append("missing source_csv")
    if _is_missing(source.get("signal_row_index")) and _is_missing(source.get("signal_timestamp")):
        reasons.append("missing signal location")
    if (
        _is_missing(source.get("entry"))
        or _is_missing(source.get("stop_loss"))
        or _is_missing(source.get("take_profit"))
    ):
        reasons.append("missing entry/stop/take profit")

    direction = source.get("direction")
    if not _is_missing(direction) and str(direction).strip().lower() != "long":
        reasons.append("unsupported direction")

    return not reasons, reasons


def _invalid_outcome_result(
    *,
    reason: str,
    horizon_bars: int,
    tie_break_policy: str,
) -> dict[str, Any]:
    return {
        "outcome": "INVALID",
        "bars_to_hit": None,
        "realized_R": None,
        "same_bar_hit": False,
        "tie_break_policy": tie_break_policy,
        "horizon_bars": horizon_bars,
        "future_bars_available": None,
        "evaluation_window_start_index": None,
        "evaluation_window_end_index": None,
        "signal_is_latest_row": None,
        "neither_reason": None,
        "hit_timestamp": None,
        "hit_row_index": None,
        "planned_rr": None,
        "mark_to_market_close": None,
        "error": reason,
    }


def _outcome_is_success(result_row: dict[str, Any]) -> bool:
    return result_row.get("backtest_success") is True or str(result_row.get("backtest_success")).lower() == "true"


def evaluate_candidate_snapshot_row(
    snapshot_row: dict[str, Any],
    *,
    horizon_bars: int = 20,
    tie_break_policy: str = "conservative",
    candidate_snapshot_file: str | None = None,
    write_invalid_rows: bool = True,
) -> dict[str, Any]:
    _ = write_invalid_rows
    snapshot = dict(snapshot_row) if isinstance(snapshot_row, dict) else {}
    errors: list[str] = []
    warnings: list[str] = []

    evaluable, reasons = _candidate_row_is_evaluable(snapshot)
    if not evaluable:
        errors.extend(reasons)
        outcome_result = _invalid_outcome_result(
            reason="; ".join(reasons),
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
        )
        result_row = backtest_result_row(
            snapshot_row=snapshot,
            outcome_result=outcome_result,
            candidate_snapshot_file=candidate_snapshot_file,
        )
        return {
            "success": False,
            "snapshot_row": snapshot,
            "outcome_result": outcome_result,
            "result_row": result_row,
            "errors": errors,
            "warnings": warnings,
        }

    service_result = evaluate_backtest_candidate_from_csv(
        snapshot.get("source_csv"),
        snapshot,
        horizon_bars=horizon_bars,
        tie_break_policy=tie_break_policy,
    )
    result_row = backtest_result_row(
        snapshot_row=snapshot,
        outcome_result=service_result,
        candidate_snapshot_file=candidate_snapshot_file,
    )
    if not _outcome_is_success(result_row):
        error = service_result.get("error") or result_row.get("outcome_error")
        if error:
            errors.append(str(error))

    return {
        "success": _outcome_is_success(result_row),
        "snapshot_row": snapshot,
        "outcome_result": service_result,
        "result_row": result_row,
        "errors": errors,
        "warnings": warnings,
    }


def evaluate_candidate_snapshot_rows(
    snapshot_rows: list[dict[str, Any]],
    *,
    horizon_bars: int = 20,
    tie_break_policy: str = "conservative",
    candidate_snapshot_file: str | None = None,
    write_invalid_rows: bool = True,
) -> dict[str, Any]:
    rows = list(snapshot_rows or [])
    results = [
        evaluate_candidate_snapshot_row(
            row,
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
            candidate_snapshot_file=candidate_snapshot_file,
            write_invalid_rows=write_invalid_rows,
        )
        for row in rows
    ]

    result_rows: list[dict[str, Any]] = []
    skipped_count = 0
    errors: list[str] = []
    warnings: list[str] = []
    for item in results:
        errors.extend(item.get("errors") or [])
        warnings.extend(item.get("warnings") or [])
        result_row = item.get("result_row")
        if result_row is not None and (write_invalid_rows or item.get("success")):
            result_rows.append(result_row)
        elif not item.get("success"):
            skipped_count += 1

    success_count = sum(1 for row in result_rows if _outcome_is_success(row))
    invalid_count = len(result_rows) - success_count
    return {
        "success": bool(result_rows),
        "count": len(rows),
        "evaluated_count": len(result_rows),
        "success_count": success_count,
        "invalid_count": invalid_count,
        "skipped_count": skipped_count,
        "results": results,
        "result_rows": result_rows,
        "errors": errors,
        "warnings": warnings,
    }


def read_candidate_snapshot_csv(candidates_csv_path: str | Path) -> dict[str, Any]:
    path = Path(candidates_csv_path)
    result = {
        "success": False,
        "path": str(path),
        "count": 0,
        "rows": [],
        "errors": [],
    }
    try:
        data = pd.read_csv(path)
        rows = data.where(pd.notna(data), None).to_dict(orient="records")
        result["success"] = True
        result["count"] = len(rows)
        result["rows"] = rows
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def evaluate_candidate_snapshot_csv(
    candidates_csv_path: str | Path,
    *,
    horizon_bars: int = 20,
    tie_break_policy: str = "conservative",
    write_invalid_rows: bool = True,
) -> dict[str, Any]:
    read_result = read_candidate_snapshot_csv(candidates_csv_path)
    if not read_result.get("success"):
        return {
            "success": False,
            "count": 0,
            "evaluated_count": 0,
            "success_count": 0,
            "invalid_count": 0,
            "skipped_count": 0,
            "results": [],
            "result_rows": [],
            "errors": list(read_result.get("errors") or []),
            "warnings": [],
            "read_result": read_result,
        }

    return {
        **evaluate_candidate_snapshot_rows(
            read_result.get("rows") or [],
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
            candidate_snapshot_file=Path(candidates_csv_path).name,
            write_invalid_rows=write_invalid_rows,
        ),
        "read_result": read_result,
    }


def evaluate_candidate_snapshot_csv_to_results_csv(
    candidates_csv_path: str | Path,
    output_dir: str | Path | None = None,
    *,
    horizon_bars: int = 20,
    tie_break_policy: str = "conservative",
    write_invalid_rows: bool = True,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    path = Path(candidates_csv_path)
    evaluation = evaluate_candidate_snapshot_csv(
        path,
        horizon_bars=horizon_bars,
        tie_break_policy=tie_break_policy,
        write_invalid_rows=write_invalid_rows,
    )

    errors = list(evaluation.get("errors") or [])
    warnings = list(evaluation.get("warnings") or [])
    result_rows = evaluation.get("result_rows") or []
    if not result_rows:
        return {
            "success": False,
            "candidates_csv_path": str(path),
            "evaluation": evaluation,
            "write_result": None,
            "path": None,
            "filename": None,
            "errors": errors or ["No backtest result rows were produced."],
            "warnings": warnings,
        }

    first_row = result_rows[0]
    inferred_ticker = ticker if ticker is not None else first_row.get("ticker") or None
    inferred_timeframe = timeframe if timeframe is not None else first_row.get("timeframe") or None
    target_dir = Path(output_dir) if output_dir is not None else path.parent
    write_result = write_backtest_results_csv(
        result_rows,
        target_dir,
        ticker=inferred_ticker,
        timeframe=inferred_timeframe,
        timestamp=timestamp,
    )
    errors.extend(write_result.get("errors") or [])
    warnings.extend(write_result.get("warnings") or [])

    return {
        "success": bool(result_rows) and bool(write_result.get("success")),
        "candidates_csv_path": str(path),
        "evaluation": evaluation,
        "write_result": write_result,
        "path": write_result.get("path"),
        "filename": write_result.get("filename"),
        "errors": errors,
        "warnings": warnings,
    }
