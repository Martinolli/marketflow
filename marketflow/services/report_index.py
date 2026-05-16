"""Helpers for locating and loading generated MarketFlow reports."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_utils import sanitize_filename


TIMEFRAME_TOKENS = ("1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m")


def _report_root() -> Path:
    """Return the configured MarketFlow report root directory."""
    return Path(create_app_config().REPORT_DIR)


def _safe_ticker(ticker: str) -> str:
    """Return the filesystem-safe ticker used by existing report generation."""
    return sanitize_filename((ticker or "").strip())


def find_latest_ticker_report(ticker: str) -> str | None:
    """Find the newest generated report directory for a ticker, if one exists."""
    safe_ticker = _safe_ticker(ticker)
    if not safe_ticker:
        return None

    root = _report_root()
    if not root.exists():
        return None

    candidates: dict[Path, float] = {}

    for date_dir in root.iterdir():
        ticker_dir = date_dir / safe_ticker
        if ticker_dir.is_dir():
            candidates[ticker_dir] = ticker_dir.stat().st_mtime

    report_filename = f"{safe_ticker}_report.json"
    for report_file in root.rglob(report_filename):
        if report_file.is_file():
            candidates[report_file.parent] = report_file.stat().st_mtime

    if not candidates:
        return None

    return str(max(candidates, key=candidates.get))


def list_report_date_folders() -> list[str]:
    """
    Return available date or batch folders under the configured report root.
    Should return folder paths or names sorted newest first.
    """
    root = _report_root()
    if not root.exists() or not root.is_dir():
        return []

    folders = [path for path in root.iterdir() if path.is_dir()]
    folders.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return [str(path) for path in folders]


def list_available_tickers(report_parent: str | None = None) -> list[str]:
    """
    Return available ticker folders.

    If report_parent is provided, list tickers under that folder.
    If report_parent is None, search under the configured report root.
    """
    if report_parent:
        parent = Path(report_parent)
        if not parent.exists() or not parent.is_dir():
            return []
        return sorted(path.name for path in parent.iterdir() if path.is_dir())

    root = _report_root()
    if not root.exists() or not root.is_dir():
        return []

    tickers: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_dir():
            continue
        if any(path.glob("*_report.json")) or any(path.glob("*_summary_report.txt")):
            tickers.add(path.name)

    return sorted(tickers)


def load_report_json(report_dir: str, ticker: str) -> dict[str, Any] | None:
    """Load the generated JSON report for a ticker from a report directory."""
    if not report_dir:
        return None

    report_path = Path(report_dir) / f"{_safe_ticker(ticker)}_report.json"
    if not report_path.exists():
        return None

    try:
        with open(report_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def load_summary_text(report_dir: str, ticker: str) -> str | None:
    """Load the generated text summary report for a ticker from a report directory."""
    if not report_dir:
        return None

    report_path = Path(report_dir) / f"{_safe_ticker(ticker)}_summary_report.txt"
    if not report_path.exists():
        return None

    try:
        text = report_path.read_text(encoding="utf-8").strip()
        return text or None
    except Exception:
        return None


def list_report_files(report_dir: str) -> list[str]:
    """List files generated in a report directory."""
    if not report_dir:
        return []

    path = Path(report_dir)
    if not path.exists() or not path.is_dir():
        return []

    return sorted(str(item) for item in path.iterdir() if item.is_file())


def list_annotated_csv_files(report_dir: str) -> list[str]:
    """
    Return CSV files in the ticker report directory that look like annotated data.

    Prefer files matching *_wyckoff_annotated.csv, then include other CSV files.
    """
    if not report_dir:
        return []

    path = Path(report_dir)
    if not path.exists() or not path.is_dir():
        return []

    annotated = sorted(item for item in path.glob("*_wyckoff_annotated.csv") if item.is_file())
    annotated_set = {item.resolve() for item in annotated}
    other_csv = sorted(
        item
        for item in path.glob("*.csv")
        if item.is_file() and item.resolve() not in annotated_set
    )
    return [str(item) for item in [*annotated, *other_csv]]


def infer_timeframe_from_csv_name(csv_path: str) -> str | None:
    """
    Infer timeframe from a CSV filename.

    Examples:
    AAPL_1d_wyckoff_annotated.csv -> 1d
    AAPL_4h_wyckoff_annotated.csv -> 4h
    AAPL_15m_wyckoff_annotated.csv -> 15m
    """
    if not csv_path:
        return None

    stem = Path(csv_path).stem
    parts = re.split(r"[_\-.]", stem)
    for part in reversed(parts):
        if part in TIMEFRAME_TOKENS:
            return part
    return None


def load_csv_preview(csv_path: str, nrows: int = 500) -> pd.DataFrame | None:
    """
    Load a CSV file safely for preview.

    Prefer reading the tail of the file if possible.
    If tail reading is inconvenient, read normally and return the last nrows.
    Must not crash the UI.
    Return None on failure.
    """
    if not csv_path:
        return None

    path = Path(csv_path)
    if not path.exists() or not path.is_file():
        return None

    try:
        nrows = max(int(nrows), 1)
        chunks = pd.read_csv(path, chunksize=nrows)
        last_chunk = None
        for chunk in chunks:
            last_chunk = chunk
        if last_chunk is None:
            return pd.DataFrame()
        return last_chunk.tail(nrows)
    except Exception:
        return None
