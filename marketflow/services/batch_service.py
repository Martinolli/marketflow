"""Service helpers for running batch MarketFlow analysis from the UI."""

from __future__ import annotations

import os
import re
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

from marketflow.batch_utils import write_batch_summary_csv
from marketflow.marketflow_analysis import embed_fn, run_analysis
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_utils import sanitize_filename
from marketflow.services.analysis_service import normalize_timeframes
from marketflow.transient_vector_memory import TransientVectorMemory


def normalize_batch_tickers(tickers: str | list[str] | None) -> list[str]:
    """
    Normalize ticker input from comma, whitespace, or newline separated text.

    Return uppercase ticker symbols with duplicates removed while preserving
    order. Characters outside common ticker formats are stripped.
    """
    if not tickers:
        return []

    if isinstance(tickers, str):
        raw_values = re.split(r"[\s,]+", tickers)
    else:
        raw_values = [str(value) for value in tickers]

    normalized: list[str] = []
    seen: set[str] = set()
    for value in raw_values:
        ticker = re.sub(r"[^A-Z0-9:._-]", "", value.strip().upper())
        if ticker and ticker not in seen:
            normalized.append(ticker)
            seen.add(ticker)
    return normalized


def _ticker_result(
    ticker: str,
    success: bool,
    output_dir: str | None = None,
    narrative: str | None = None,
    error: str | None = None,
    error_type: str | None = None,
) -> dict[str, Any]:
    """Build a UI-friendly per-ticker batch result."""
    return {
        "ticker": ticker,
        "success": success,
        "output_dir": output_dir,
        "narrative_available": bool(narrative),
        "error": error,
        "error_type": error_type,
    }


def run_batch_analysis(
    tickers: list[str],
    timeframes: list[str] | list[dict[str, Any]] | None = None,
    enable_tvm: bool = True,
) -> dict[str, Any]:
    """
    Run MarketFlow analysis for multiple tickers.

    Each ticker is handled independently so one failure does not stop the
    batch. The returned dictionary is shaped for Streamlit rendering.
    """
    logger = get_logger("marketflow_batch_analysis")
    clean_tickers = normalize_batch_tickers(tickers)
    notes: list[str] = []

    if not clean_tickers:
        return {
            "success": False,
            "error": "Enter at least one ticker.",
            "error_type": "ValidationError",
            "traceback": None,
            "run_id": None,
            "namespace": None,
            "batch_output_dir": None,
            "summary_csv": None,
            "results": [],
            "notes": ["No valid ticker symbols were provided."],
        }

    try:
        normalized_timeframes = normalize_timeframes(timeframes)
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "traceback": traceback.format_exc(),
            "run_id": None,
            "namespace": None,
            "batch_output_dir": None,
            "summary_csv": None,
            "results": [],
            "notes": ["Timeframe normalization failed before batch analysis started."],
        }

    config = create_app_config()
    report_root = config.REPORT_DIR
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    namespace = f"batch:{run_id}" if enable_tvm else None
    batch_output_dir = (
        os.path.join(report_root, f"batch_{run_id}") if enable_tvm else None
    )
    tvm = None

    if enable_tvm:
        logger.info(f"Starting UI batch analysis. TVM Namespace: '{namespace}'")
        Path(batch_output_dir).mkdir(parents=True, exist_ok=True)
        tvm = TransientVectorMemory(embed_fn=embed_fn, dim=1536, ttl_seconds=48 * 3600)
    else:
        logger.info("Starting UI batch analysis with TVM disabled.")

    results: list[dict[str, Any]] = []
    successful_runs: list[dict[str, str]] = []

    for ticker in clean_tickers:
        logger.info(f"--- Processing ticker: {ticker} ---")
        try:
            narrative, output_dir = run_analysis(
                ticker,
                timeframes=normalized_timeframes,
                logger=logger,
            )
            successful_runs.append({"ticker": ticker, "output_dir": output_dir})
        except Exception as exc:
            logger.error(f"Failed to process ticker {ticker}: {exc}", exc_info=True)
            results.append(
                _ticker_result(
                    ticker=ticker,
                    success=False,
                    error=str(exc),
                    error_type=type(exc).__name__,
                )
            )
            continue

        results.append(
            _ticker_result(
                ticker=ticker,
                success=True,
                output_dir=output_dir,
                narrative=narrative,
            )
        )

        if enable_tvm and tvm and narrative and namespace:
            try:
                tvm.upsert_text(
                    namespace=namespace,
                    report_id=f"{sanitize_filename(ticker)}_{run_id}",
                    text=narrative,
                    meta={"source": "marketflow_analysis", "ticker": ticker},
                )
            except Exception as exc:
                logger.error(f"Failed to upsert {ticker} into batch TVM: {exc}", exc_info=True)
                notes.append(f"TVM upsert failed for {ticker}: {type(exc).__name__}: {exc}")
        elif enable_tvm:
            notes.append(f"No narrative generated for {ticker}; TVM upsert skipped.")

    if enable_tvm and tvm and namespace and batch_output_dir:
        try:
            tvm_dir = os.path.join(batch_output_dir, ".tvm_store")
            tvm.save_namespace(namespace, tvm_dir)
            ns_file = os.path.join(batch_output_dir, ".tvm_namespace")
            with open(ns_file, "w", encoding="utf-8") as file:
                file.write(namespace)
            notes.append(f"TVM namespace saved to {batch_output_dir}.")
        except Exception as exc:
            logger.error(f"Failed to save batch TVM store: {exc}", exc_info=True)
            notes.append(f"TVM save failed: {type(exc).__name__}: {exc}")

    summary_csv = None
    try:
        output_summary_csv_data = os.path.join(report_root, f"batch_csv_{run_id}")
        summary_csv = write_batch_summary_csv(
            successful_runs,
            output_summary_csv_data,
            logger,
        )
        if summary_csv:
            notes.append(f"Summary CSV created at {summary_csv}.")
        else:
            notes.append("Summary CSV was not created.")
    except Exception as exc:
        logger.error(f"Failed to write batch summary CSV: {exc}", exc_info=True)
        notes.append(f"Summary CSV creation failed: {type(exc).__name__}: {exc}")

    succeeded = sum(1 for item in results if item["success"])
    failed = len(results) - succeeded
    notes.extend(
        [
            f"Requested tickers: {len(clean_tickers)}.",
            f"Succeeded: {succeeded}.",
            f"Failed: {failed}.",
            f"TVM enabled: {enable_tvm}.",
        ]
    )

    return {
        "success": succeeded > 0,
        "error": None if succeeded > 0 else "All batch ticker analyses failed.",
        "error_type": None if succeeded > 0 else "BatchAnalysisError",
        "traceback": None,
        "run_id": run_id,
        "namespace": namespace,
        "batch_output_dir": batch_output_dir,
        "summary_csv": summary_csv,
        "results": results,
        "notes": notes,
        "timeframes": normalized_timeframes,
    }
