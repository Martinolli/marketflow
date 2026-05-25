"""Service wrapper for the Price-Volume Eigen Analyzer."""

from __future__ import annotations

import math
import traceback as traceback_module
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.analyzers.price_volume_eigen_analyzer import (
    EIGEN_FEATURE_COLUMNS,
    PriceVolumeEigenAnalyzer,
)


def _json_safe_value(value: Any) -> Any:
    """Convert pandas/numpy scalar values to JSON-safe Python values."""
    if value is None:
        return None
    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    if pd.isna(value):
        return None
    return value


def _latest_row(dataframe: pd.DataFrame) -> dict[str, Any]:
    if dataframe.empty:
        return {}

    latest = dataframe.iloc[-1]
    keys = [
        "timestamp",
        "date",
        "datetime",
        "close",
        "volume",
        "pv_result_z",
        "pv_effort_z",
        "pv_eigen_coupling",
        "pv_eigen_residual",
        "pv_eigen_harmony",
        "pv_effort_result_divergence",
        "pv_divergence_strength",
        "pv_eigen_status",
    ]
    return {
        key: _json_safe_value(latest.get(key))
        for key in keys
        if key in dataframe.columns
    }


def _sanitize_windows(windows: list[int] | tuple[int, ...] | None) -> list[int]:
    """Return sorted unique Eigen windows with a safe fallback."""
    parsed: set[int] = set()
    for value in windows or (20, 40, 60):
        try:
            window = int(value)
        except (TypeError, ValueError):
            continue
        if window >= 5:
            parsed.add(window)
    return sorted(parsed) or [20, 40, 60]


def _numeric_stat(series: pd.Series, stat: str) -> float | None:
    """Return a JSON-safe numeric statistic from a series."""
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return None
    if stat == "max":
        return _json_safe_value(float(values.max()))
    if stat == "mean":
        return _json_safe_value(float(values.mean()))
    return None


def _timestamp_for_index(dataframe: pd.DataFrame, index: int | None) -> str | None:
    """Return timestamp/date/datetime text for a row index when available."""
    if index is None or index < 0 or index >= len(dataframe):
        return None
    for column in ("timestamp", "date", "datetime"):
        if column in dataframe.columns:
            value = dataframe.iloc[index].get(column)
            if value is not None and not pd.isna(value):
                return str(value)
    return None


def _truthy_divergence(series: pd.Series) -> pd.Series:
    """Normalize divergence values from bools or CSV-like text."""
    if series.dtype == bool:
        return series.fillna(False)
    normalized = series.fillna(False).astype(str).str.strip().str.lower()
    return normalized.isin({"true", "1", "yes", "y"})


def _comparison_row(enriched: pd.DataFrame, window: int) -> dict[str, Any]:
    """Build one window comparison row from analyzer output."""
    valid = enriched[enriched.get("pv_eigen_status") == "ok"] if "pv_eigen_status" in enriched.columns else pd.DataFrame()
    latest = enriched.iloc[-1] if not enriched.empty else pd.Series(dtype=object)
    divergence = (
        _truthy_divergence(enriched["pv_effort_result_divergence"])
        if "pv_effort_result_divergence" in enriched.columns
        else pd.Series(False, index=enriched.index)
    )
    divergence_count = int(divergence.sum())
    divergence_indexes = [int(index) for index in range(len(enriched)) if bool(divergence.iloc[index])]
    last_divergence_index = divergence_indexes[-1] if divergence_indexes else None
    rows = int(len(enriched))

    return {
        "window": int(window),
        "valid_rows": int(len(valid)),
        "divergence_count": divergence_count,
        "divergence_rate": (divergence_count / rows) if rows else 0.0,
        "latest_status": _json_safe_value(latest.get("pv_eigen_status")),
        "latest_residual": _json_safe_value(latest.get("pv_eigen_residual")),
        "latest_coupling": _json_safe_value(latest.get("pv_eigen_coupling")),
        "latest_harmony": _json_safe_value(latest.get("pv_eigen_harmony")),
        "latest_divergence": _json_safe_value(latest.get("pv_effort_result_divergence")),
        "max_residual": _numeric_stat(enriched.get("pv_eigen_residual", pd.Series(dtype=float)), "max"),
        "mean_residual": _numeric_stat(enriched.get("pv_eigen_residual", pd.Series(dtype=float)), "mean"),
        "mean_coupling": _numeric_stat(enriched.get("pv_eigen_coupling", pd.Series(dtype=float)), "mean"),
        "last_divergence_index": last_divergence_index,
        "last_divergence_timestamp": _timestamp_for_index(enriched, last_divergence_index),
    }


def _window_comparison_interpretation(rows: int, comparison: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a descriptive, non-trading interpretation of window diagnostics."""
    recent_span = min(max(int(rows * 0.1), 1), 20) if rows else 0
    latest_windows = [
        item["window"]
        for item in comparison
        if item.get("latest_divergence") is True
    ]
    recent_windows = [
        item["window"]
        for item in comparison
        if item.get("last_divergence_index") is not None
        and rows
        and int(item["last_divergence_index"]) >= rows - recent_span
    ]
    selected_windows = [int(item["window"]) for item in comparison]
    shortest = min(selected_windows) if selected_windows else None

    if not recent_windows:
        observation = "No recent eigen divergence detected across selected windows."
    elif len(recent_windows) == 1 and recent_windows[0] == shortest:
        observation = "Eigen divergence appears mainly on the shortest window; this may indicate a local/tactical anomaly."
    elif len(recent_windows) >= len(selected_windows):
        observation = "Eigen divergence appears across most selected windows; this may indicate a persistent/background effort-result anomaly."
    elif len(recent_windows) >= 2:
        observation = "Eigen divergence appears across short and medium windows; this may indicate a broader effort-result anomaly."
    else:
        observation = "Eigen divergence appears on a limited subset of selected windows; review the window-specific diagnostics."

    return {
        "latest_divergence_windows": latest_windows,
        "recent_divergence_windows": recent_windows,
        "broad_observation": observation,
        "notes": [
            f"Recent means the last {recent_span} row(s), using the smaller of 10% of rows or 20 rows.",
            "Shorter windows react faster; longer windows emphasize broader background behavior.",
            "This comparison is diagnostic only and does not create trading signals.",
        ],
    }


def run_price_volume_eigen_for_csv(
    csv_path: str | Path,
    *,
    window: int = 40,
    result_mode: str = "spread_atr",
    effort_mode: str = "volume_ratio",
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """
    Run the standalone Price-Volume Eigen Analyzer for one CSV.

    This function only generates an enriched CSV artifact. It does not change
    Strategy Ranking, Monte Carlo, P&F, or Analyst Packet decisions.
    """
    try:
        source_path = Path(csv_path)
        if not source_path.exists() or not source_path.is_file():
            return {
                "success": False,
                "csv_path": str(csv_path),
                "error": "CSV file does not exist.",
                "error_type": "FileNotFoundError",
                "traceback": None,
            }

        dataframe = pd.read_csv(source_path)
        analyzer = PriceVolumeEigenAnalyzer(
            window=window,
            result_mode=result_mode,
            effort_mode=effort_mode,
        )
        enriched = analyzer.transform(dataframe)

        destination = Path(output_path) if output_path is not None else source_path.with_name(f"{source_path.stem}_pv_eigen.csv")
        destination.parent.mkdir(parents=True, exist_ok=True)
        enriched.to_csv(destination, index=False)

        divergence_count = int(enriched["pv_effort_result_divergence"].fillna(False).astype(bool).sum())
        columns_added = [column for column in EIGEN_FEATURE_COLUMNS if column in enriched.columns]

        return {
            "success": True,
            "csv_path": str(source_path),
            "output_path": str(destination),
            "rows": int(len(enriched)),
            "window": int(analyzer.window),
            "result_mode": analyzer.result_mode,
            "effort_mode": analyzer.effort_mode,
            "divergence_count": divergence_count,
            "latest": _latest_row(enriched),
            "columns_added": columns_added,
        }
    except Exception as exc:
        return {
            "success": False,
            "csv_path": str(csv_path),
            "error": str(exc),
            "error_type": type(exc).__name__,
            "traceback": traceback_module.format_exc(),
        }


def compare_price_volume_eigen_windows(
    csv_path: str | Path,
    *,
    windows: list[int] | tuple[int, ...] = (20, 40, 60),
    result_mode: str = "spread_atr",
    effort_mode: str = "volume_ratio",
) -> dict[str, Any]:
    """
    Compare Price-Volume Eigen diagnostics across rolling windows.

    This function does not save artifacts and does not create trading signals.
    """
    try:
        source_path = Path(csv_path)
        if not source_path.exists() or not source_path.is_file():
            return {
                "success": False,
                "csv_path": str(csv_path),
                "error": "CSV file does not exist.",
                "error_type": "FileNotFoundError",
                "traceback": None,
            }

        dataframe = pd.read_csv(source_path)
        safe_windows = _sanitize_windows(windows)
        comparison: list[dict[str, Any]] = []
        for window in safe_windows:
            analyzer = PriceVolumeEigenAnalyzer(
                window=window,
                result_mode=result_mode,
                effort_mode=effort_mode,
            )
            enriched = analyzer.transform(dataframe)
            comparison.append(_comparison_row(enriched, analyzer.window))

        rows = int(len(dataframe))
        return {
            "success": True,
            "csv_path": str(source_path),
            "rows": rows,
            "result_mode": result_mode,
            "effort_mode": effort_mode,
            "windows": safe_windows,
            "comparison": comparison,
            "interpretation": _window_comparison_interpretation(rows, comparison),
        }
    except Exception as exc:
        return {
            "success": False,
            "csv_path": str(csv_path),
            "error": str(exc),
            "error_type": type(exc).__name__,
            "traceback": traceback_module.format_exc(),
        }
