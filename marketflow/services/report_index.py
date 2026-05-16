"""Helpers for locating and loading generated MarketFlow reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_utils import sanitize_filename


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

