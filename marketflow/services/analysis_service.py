"""Application service wrapper for running MarketFlow analysis."""

from __future__ import annotations

import traceback
from typing import Any

from marketflow.marketflow_analysis import run_analysis
from marketflow.services.report_index import (
    list_report_files,
    load_report_json,
    load_summary_text,
)


TIMEFRAME_PERIODS = {
    "1mo": "5y",
    "1w": "2y",
    "1d": "365d",
    "4h": "100d",
    "2h": "60d",
    "1h": "40d",
    "30m": "20d",
    "15m": "20d",
    "5m": "20d",
    "1m": "20d",
}


def normalize_timeframes(
    timeframes: list[str] | list[dict[str, Any]] | None,
) -> list[dict[str, str]] | None:
    """Normalize UI timeframe selections into MarketFlow timeframe dictionaries."""
    if not timeframes:
        return None

    normalized: list[dict[str, str]] = []
    unsupported: list[str] = []

    for timeframe in timeframes:
        if not timeframe:
            continue

        if isinstance(timeframe, dict):
            interval = timeframe.get("interval")
            period = timeframe.get("period")
            if interval and period:
                normalized.append(timeframe)
                continue
            raise ValueError(
                "Timeframe dictionaries must include both 'interval' and 'period'."
            )

        if isinstance(timeframe, str):
            interval = timeframe.strip()
            if not interval:
                continue

            period = TIMEFRAME_PERIODS.get(interval)
            if not period:
                unsupported.append(interval)
                continue

            normalized.append({"interval": interval, "period": period})
            continue

        raise ValueError(f"Unsupported timeframe value: {timeframe!r}")

    if unsupported:
        supported = ", ".join(TIMEFRAME_PERIODS)
        bad_values = ", ".join(unsupported)
        raise ValueError(f"Unsupported timeframe(s): {bad_values}. Supported: {supported}.")

    return normalized or None


def _error_result(ticker: str, error: str, error_type: str) -> dict[str, Any]:
    """Build a consistent error result for the Streamlit UI."""
    return {
        "ticker": ticker,
        "narrative": "",
        "output_dir": None,
        "success": False,
        "error": error,
        "error_type": error_type,
        "traceback": None,
    }


def run_single_ticker(
    ticker: str,
    timeframes: list[str] | list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run analysis for one ticker and return a UI-friendly result dictionary."""
    clean_ticker = (ticker or "").strip()

    if not clean_ticker:
        return _error_result(clean_ticker, "Ticker is required.", "ValidationError")

    try:
        normalized_timeframes = normalize_timeframes(timeframes)
        narrative, output_dir = run_analysis(
            clean_ticker,
            timeframes=normalized_timeframes,
        )
        return {
            "ticker": clean_ticker,
            "narrative": narrative,
            "output_dir": output_dir,
            "success": True,
            "error": None,
            "error_type": None,
            "traceback": None,
            "timeframes": normalized_timeframes,
            "report_json": load_report_json(output_dir, clean_ticker),
            "summary_text": load_summary_text(output_dir, clean_ticker),
            "report_files": list_report_files(output_dir),
        }
    except Exception as exc:
        return {
            "ticker": clean_ticker,
            "narrative": "",
            "output_dir": None,
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "traceback": traceback.format_exc(),
        }
