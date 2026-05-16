"""Service wrapper for MarketFlow strategy ranking."""

from __future__ import annotations

import re
import traceback
from dataclasses import asdict
from typing import Any

import pandas as pd

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_strategy import StrategyConfig, rank_long_candidates


STRATEGY_COLUMNS = [
    "ticker",
    "tf",
    "close",
    "sl",
    "tp",
    "rr",
    "pop",
    "phase",
    "event",
    "trend",
    "score",
    "csv",
]


def get_report_root() -> str:
    """Return the configured MarketFlow report root directory."""
    return create_app_config().REPORT_DIR


def normalize_tickers(tickers: str | list[str] | None) -> list[str]:
    """
    Normalize ticker input from text or list into uppercase ticker symbols.

    Accepts comma-separated or whitespace-separated strings.
    """
    if not tickers:
        return []

    if isinstance(tickers, str):
        raw_tickers = re.split(r"[\s,]+", tickers)
    else:
        raw_tickers = tickers

    normalized: list[str] = []
    seen: set[str] = set()
    for ticker in raw_tickers:
        clean_ticker = str(ticker).strip().upper()
        if clean_ticker and clean_ticker not in seen:
            normalized.append(clean_ticker)
            seen.add(clean_ticker)

    return normalized


def _results_dataframe(results: list[dict[str, Any]]) -> pd.DataFrame:
    """Return strategy results as a stable-column DataFrame."""
    dataframe = pd.DataFrame(results)
    if dataframe.empty:
        return pd.DataFrame(columns=STRATEGY_COLUMNS)

    ordered_columns = [column for column in STRATEGY_COLUMNS if column in dataframe.columns]
    extra_columns = [column for column in dataframe.columns if column not in ordered_columns]
    return dataframe[[*ordered_columns, *extra_columns]]


def rank_latest_candidates(
    tickers: list[str],
    timeframe: str,
    min_rr: float = 1.5,
    max_sl_atr: float = 2.0,
    prefer_phases: tuple[str, ...] = ("C", "D", "E"),
    use_mc: bool = False,
) -> dict[str, Any]:
    """
    Rank long candidates using the latest batch/report folder.

    Return a UI-friendly dictionary with success/error metadata, raw results,
    DataFrame output, config, and report root.
    """
    report_root = get_report_root()
    cfg = StrategyConfig(
        min_rr=min_rr,
        max_sl_atr=max_sl_atr,
        prefer_phases=prefer_phases,
        use_mc=use_mc,
    )
    config = asdict(cfg)

    try:
        clean_tickers = normalize_tickers(tickers)
        if not clean_tickers:
            raise ValueError("At least one ticker is required.")

        clean_timeframe = (timeframe or "").strip()
        if not clean_timeframe:
            raise ValueError("Timeframe is required.")

        results = rank_long_candidates(
            report_root=report_root,
            date_glob="*",
            tickers=clean_tickers,
            tf=clean_timeframe,
            cfg=cfg,
            use_batch_namespace="latest",
        )
        dataframe = _results_dataframe(results)

        return {
            "success": True,
            "error": None,
            "error_type": None,
            "traceback": None,
            "results": results,
            "dataframe": dataframe,
            "config": config,
            "report_root": report_root,
            "tickers": clean_tickers,
            "timeframe": clean_timeframe,
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "traceback": traceback.format_exc(),
            "results": [],
            "dataframe": pd.DataFrame(columns=STRATEGY_COLUMNS),
            "config": config,
            "report_root": report_root,
            "tickers": normalize_tickers(tickers),
            "timeframe": timeframe,
        }

