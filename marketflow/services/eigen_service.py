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
