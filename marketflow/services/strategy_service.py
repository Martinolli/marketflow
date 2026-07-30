"""Service wrapper for MarketFlow strategy ranking."""

from __future__ import annotations

import re
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_strategy import StrategyConfig, rank_long_candidates, resolve_strategy_source_identity


STRATEGY_COLUMNS = [
    "ticker",
    "tf",
    "close",
    "sl",
    "tp",
    "rr",
    "target_status",
    "target_provenance",
    "target_structural_level_kind",
    "rr_status",
    "pop",
    "phase",
    "event",
    "trend",
    "score",
    "mc_summary_path",
    "mc_matched_by",
    "mc_requested_tf",
    "mc_matched_tf",
    "csv",
    "source_csv_name",
    "source_report_dir",
    "source_status",
]
BATCH_RUN_PATTERN = re.compile(r"^batch_(\d{8})_(\d{6})$")
BATCH_LIKE_PATTERN = re.compile(r"^batch_")


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


def _has_surrounding_whitespace(value: str) -> bool:
    return value != value.strip()


def _request_whitespace_errors(tickers: str | list[str] | None, timeframe: str | None) -> list[str]:
    errors: list[str] = []
    if isinstance(tickers, str) and _has_surrounding_whitespace(tickers):
        errors.append("Ticker request contains surrounding whitespace.")
    elif isinstance(tickers, list):
        for ticker in tickers:
            if _has_surrounding_whitespace(str(ticker)):
                errors.append("Ticker request contains surrounding whitespace.")
                break
    if timeframe is None or _has_surrounding_whitespace(str(timeframe)):
        errors.append("Timeframe request contains surrounding whitespace.")
    return errors


def _results_dataframe(results: list[dict[str, Any]]) -> pd.DataFrame:
    """Return strategy results as a stable-column DataFrame."""
    dataframe = pd.DataFrame(results)
    if dataframe.empty:
        return pd.DataFrame(columns=STRATEGY_COLUMNS)

    ordered_columns = [column for column in STRATEGY_COLUMNS if column in dataframe.columns]
    extra_columns = [column for column in dataframe.columns if column not in ordered_columns]
    return dataframe[[*ordered_columns, *extra_columns]]


def is_batch_run_folder(path: str | Path) -> bool:
    """
    Return True only for real batch run folders named batch_YYYYMMDD_HHMMSS.

    Excludes batch_csv_* and other summary folders.
    """
    path_obj = Path(path)
    return path_obj.is_dir() and bool(BATCH_RUN_PATTERN.fullmatch(path_obj.name))


def _batch_run_sort_key(path: Path) -> str:
    """Return a sortable timestamp token for a valid batch run folder."""
    match = BATCH_RUN_PATTERN.fullmatch(path.name)
    if not match:
        return ""
    return "".join(match.groups())


def list_batch_run_folders(report_root: str) -> list[str]:
    """
    Return valid batch run folders sorted newest first.

    Only include folders matching batch_YYYYMMDD_HHMMSS.
    """
    root = Path(report_root)
    if not root.exists() or not root.is_dir():
        return []

    folders = [path for path in root.iterdir() if is_batch_run_folder(path)]
    folders.sort(key=_batch_run_sort_key, reverse=True)
    return [str(path) for path in folders]


def _ignored_batch_like_folders(report_root: str) -> list[str]:
    """Return batch-like folders excluded from valid batch-run detection."""
    root = Path(report_root)
    if not root.exists() or not root.is_dir():
        return []

    ignored = [
        path
        for path in root.iterdir()
        if path.is_dir()
        and BATCH_LIKE_PATTERN.match(path.name)
        and not is_batch_run_folder(path)
    ]
    ignored.sort(key=lambda path: path.name, reverse=True)
    return [str(path) for path in ignored]


def find_latest_batch_folder(report_root: str) -> str | None:
    """
    Find latest valid batch run folder under report_root.

    Return path or None.
    """
    batch_folders = list_batch_run_folders(report_root)
    if not batch_folders:
        return None
    return batch_folders[0]


def _ticker_folder_candidates(report_root: str, ticker: str) -> list[Path]:
    """Return likely report folders for a ticker under the report root."""
    root = Path(report_root)
    if not root.exists() or not root.is_dir():
        return []

    candidates = [path for path in root.rglob(ticker) if path.is_dir()]
    candidates.sort(key=lambda path: path.stat().st_mtime)
    return candidates


def _relative_to_root(report_root: str, value: str | None) -> str | None:
    if not value:
        return None
    try:
        return Path(value).resolve(strict=True).relative_to(Path(report_root).resolve(strict=True)).as_posix()
    except (OSError, ValueError):
        return Path(value).name


def inspect_strategy_inputs(
    report_root: str,
    tickers: list[str],
    timeframe: str,
    min_rr: float,
    max_sl_atr: float,
    prefer_phases: tuple[str, ...],
    use_mc: bool,
) -> dict[str, Any]:
    """
    Inspect report folders and CSV availability before ranking.

    Return diagnostics dictionary for UI troubleshooting.
    """
    root = Path(report_root)
    batch_run_folders = list_batch_run_folders(report_root)
    ignored_batch_like_folders = _ignored_batch_like_folders(report_root)
    latest_batch_folder = find_latest_batch_folder(report_root)
    clean_tickers = normalize_tickers(tickers)
    clean_timeframe = str(timeframe or "")

    diagnostics: dict[str, Any] = {
        "report_root": report_root,
        "report_root_exists": root.exists() and root.is_dir(),
        "requested_tickers": clean_tickers,
        "requested_timeframe": clean_timeframe,
        "latest_batch_folder": latest_batch_folder,
        "latest_batch_folder_exists": bool(
            latest_batch_folder and Path(latest_batch_folder).exists()
        ),
        "batch_run_folders": batch_run_folders,
        "ignored_batch_like_folders": ignored_batch_like_folders,
        "ticker_checks": {},
        "filters": {
            "min_rr": float(min_rr),
            "max_sl_atr": float(max_sl_atr),
            "prefer_phases": list(prefer_phases),
            "use_mc": bool(use_mc),
        },
        "notes": [],
    }

    notes: list[str] = diagnostics["notes"]
    if not diagnostics["report_root_exists"]:
        notes.append("Report root does not exist yet. Run an analysis first.")
        return diagnostics

    if not latest_batch_folder:
        if ignored_batch_like_folders:
            notes.append(
                "Found batch-like summary folders, but no valid batch run folder "
                "matching batch_YYYYMMDD_HHMMSS."
            )
        notes.append(
            "No batch folder found. Strategy will still search recursively under the "
            "report root for exact ticker/timeframe source identities."
        )

    if use_mc:
        notes.append(
            "Timeframe-aware Monte Carlo matching is enabled for Strategy Ranking."
        )
        notes.append(
            "If no MC summary matches the selected timeframe, results may fall back "
            "to the latest available MC summary and mark `mc_matched_by` as `fallback_latest`."
        )

    total_matching_csvs = 0
    total_ticker_folders = 0

    for ticker in clean_tickers:
        folders = _ticker_folder_candidates(report_root, ticker)
        ticker_folder = folders[-1] if folders else None
        csv_candidates = sorted(ticker_folder.glob("*.csv")) if ticker_folder else []
        source_resolution = (
            resolve_strategy_source_identity(str(ticker_folder), ticker, clean_timeframe)
            if ticker_folder
            else None
        )

        total_ticker_folders += 1 if ticker_folder else 0
        total_matching_csvs += 1 if source_resolution and source_resolution.success else 0

        diagnostics["ticker_checks"][ticker] = {
            "ticker_folder_found": ticker_folder is not None,
            "ticker_folder": _relative_to_root(report_root, str(ticker_folder)) if ticker_folder else None,
            "csv_candidates": [_relative_to_root(report_root, str(path)) for path in csv_candidates],
            "source_status": source_resolution.status if source_resolution else None,
            "source_reason": source_resolution.reason if source_resolution else None,
            "source_csv_name": (
                source_resolution.source.name
                if source_resolution and source_resolution.source is not None
                else None
            ),
        }

        if not ticker_folder:
            notes.append(f"No ticker folder found for {ticker}.")
        elif not csv_candidates:
            notes.append(f"No CSV files found in the latest {ticker} report folder.")
        elif not (source_resolution and source_resolution.success):
            notes.append(
                f"No exact source identity matching timeframe `{clean_timeframe}` was found for {ticker}."
            )

    if clean_tickers and total_ticker_folders == 0:
        notes.append("No ticker folders were found for the requested tickers.")

    if clean_tickers and total_matching_csvs == 0:
        notes.append(
            f"No CSV files matching timeframe `{clean_timeframe}` were found for the "
            "requested tickers. Try another timeframe or run analysis first."
        )

    return diagnostics


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
    clean_tickers = normalize_tickers(tickers)
    request_errors = _request_whitespace_errors(tickers, timeframe)
    clean_timeframe = str(timeframe or "")
    diagnostics = inspect_strategy_inputs(
        report_root=report_root,
        tickers=clean_tickers,
        timeframe=clean_timeframe,
        min_rr=min_rr,
        max_sl_atr=max_sl_atr,
        prefer_phases=prefer_phases,
        use_mc=use_mc,
    )

    try:
        if request_errors:
            raise ValueError("; ".join(request_errors))

        if not clean_tickers:
            raise ValueError("At least one ticker is required.")

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
        if not results:
            diagnostics["notes"].append(
                "Strategy ran successfully but returned no candidates. Filters may be too "
                "strict, or the matching reports may not satisfy the strategy criteria."
            )

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
            "diagnostics": diagnostics,
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
            "diagnostics": diagnostics,
        }
