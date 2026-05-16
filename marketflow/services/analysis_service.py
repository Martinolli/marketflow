"""Application service wrapper for running MarketFlow analysis."""

from __future__ import annotations

from typing import Any

from marketflow.marketflow_analysis import run_analysis
from marketflow.services.report_index import (
    list_report_files,
    load_report_json,
    load_summary_text,
)


def run_single_ticker(ticker: str, timeframes: list[str] | None = None) -> dict[str, Any]:
    """Run analysis for one ticker and return a UI-friendly result dictionary."""
    clean_ticker = (ticker or "").strip()
    clean_timeframes = [tf.strip() for tf in (timeframes or []) if tf and tf.strip()]

    if not clean_ticker:
        return {
            "ticker": clean_ticker,
            "narrative": "",
            "output_dir": None,
            "success": False,
            "error": "Ticker is required.",
        }

    try:
        narrative, output_dir = run_analysis(
            clean_ticker,
            timeframes=clean_timeframes or None,
        )
        return {
            "ticker": clean_ticker,
            "narrative": narrative,
            "output_dir": output_dir,
            "success": True,
            "error": None,
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
        }

