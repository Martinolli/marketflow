"""Service helpers for running single-trade Monte Carlo simulations."""

from __future__ import annotations

import json
import math
import traceback
import importlib
import sys
import types
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.report_index import infer_timeframe_from_csv_name


SUPPORTED_MODELS = {"bootstrap", "gbm", "garch"}
OPTIONAL_SIMULATOR_IMPORTS = {"arch", "lightgbm"}
MONTE_CARLO_OUTPUT_PATTERNS = ("*_mc_summary.json", "*_mc_paths.html", "*_mc_hits.html")


def _json_safe_value(value: Any) -> Any:
    """Return a JSON-safe value for persisted Monte Carlo metadata."""
    if value is None:
        return None
    if value is pd.NA:
        return None
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_safe_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe_value(item) for item in value]
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, TypeError, ValueError):
            pass
    if value is pd.NA:
        return None
    try:
        if bool(pd.isna(value)):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _first_present(*values: Any) -> Any:
    """Return the first non-empty value."""
    for value in values:
        safe = _json_safe_value(value)
        if safe is None:
            continue
        if isinstance(safe, str) and not safe.strip():
            continue
        return safe
    return None


def _source_csv_name(value: Any) -> str | None:
    """Return a basename for a source CSV value."""
    value = _first_present(value)
    if value is None:
        return None
    return Path(str(value)).name


def _infer_ticker_from_csv_name(csv_path: str | Path | None) -> str | None:
    """Infer ticker from a canonical MarketFlow CSV filename when possible."""
    if not csv_path:
        return None
    stem = Path(str(csv_path)).name
    if "_" not in stem:
        return None
    ticker = stem.split("_", 1)[0].strip()
    return ticker or None


def _join_key(*parts: Any) -> str | None:
    """Build a compact join key when every part is present."""
    values = [_first_present(part) for part in parts]
    if any(value is None for value in values):
        return None
    return "|".join(str(value) for value in values)


def build_monte_carlo_join_metadata(
    *,
    csv_path: str | Path | None = None,
    timeframe: str | None = None,
    trade_plan: dict[str, Any] | None = None,
    candidate_snapshot: dict[str, Any] | None = None,
    candidate_snapshot_file: str | None = None,
    source_report_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Build JSON-safe metadata for future MC forecast-vs-actual joins."""
    trade = dict(trade_plan) if isinstance(trade_plan, dict) else {}
    snapshot = dict(candidate_snapshot) if isinstance(candidate_snapshot, dict) else {}
    source_csv_value = _first_present(snapshot.get("source_csv"), snapshot.get("csv"), trade.get("source_csv"), trade.get("csv"), csv_path)
    source_csv_path = _first_present(snapshot.get("source_csv"), snapshot.get("csv"), trade.get("source_csv"), trade.get("csv"), csv_path)
    selected_timeframe = _first_present(
        snapshot.get("timeframe"),
        snapshot.get("tf"),
        trade.get("timeframe"),
        trade.get("tf"),
        timeframe,
        infer_timeframe_from_csv_name(str(csv_path or "")),
    )
    ticker = _first_present(
        snapshot.get("ticker"),
        trade.get("ticker"),
        _infer_ticker_from_csv_name(source_csv_value),
        _infer_ticker_from_csv_name(csv_path),
    )

    metadata = {
        "ticker": ticker,
        "timeframe": selected_timeframe,
        "source_csv": _source_csv_name(source_csv_value),
        "source_csv_path": source_csv_path,
        "source_report_dir": _first_present(snapshot.get("source_report_dir"), source_report_dir),
        "candidate_snapshot_file": _first_present(candidate_snapshot_file),
        "signal_row_index": _first_present(snapshot.get("signal_row_index"), trade.get("signal_row_index")),
        "signal_timestamp": _first_present(snapshot.get("signal_timestamp"), trade.get("signal_timestamp")),
        "entry": _first_present(snapshot.get("entry"), trade.get("entry")),
        "stop_loss": _first_present(snapshot.get("stop_loss"), snapshot.get("sl"), trade.get("stop_loss"), trade.get("sl")),
        "take_profit": _first_present(
            snapshot.get("take_profit"),
            snapshot.get("tp"),
            trade.get("take_profit"),
            trade.get("tp"),
        ),
        "risk_reward": _first_present(snapshot.get("risk_reward"), snapshot.get("rr"), trade.get("risk_reward"), trade.get("rr")),
        "strategy_score": _first_present(snapshot.get("strategy_score"), snapshot.get("score"), trade.get("strategy_score"), trade.get("score")),
        "wyckoff_phase": _first_present(snapshot.get("wyckoff_phase"), snapshot.get("phase"), trade.get("wyckoff_phase"), trade.get("phase")),
        "wyckoff_event": _first_present(snapshot.get("wyckoff_event"), snapshot.get("event"), trade.get("wyckoff_event"), trade.get("event")),
        "trend": _first_present(snapshot.get("trend"), trade.get("trend")),
        "candidate_source": _first_present(snapshot.get("candidate_source"), trade.get("candidate_source"), trade.get("source")),
        "source_strategy_rank": _first_present(snapshot.get("source_strategy_rank"), trade.get("source_strategy_rank")),
        "candidate_validation_status": _first_present(snapshot.get("validation_status"), trade.get("validation_status")),
        "candidate_snapshot_success": _first_present(snapshot.get("snapshot_success"), trade.get("snapshot_success")),
        "metadata_version": "mc_join_metadata_v1",
    }
    metadata["join_key_preferred"] = _join_key(
        metadata["ticker"],
        metadata["timeframe"],
        metadata["candidate_snapshot_file"],
    )
    metadata["join_key_secondary"] = _join_key(
        metadata["ticker"],
        metadata["timeframe"],
        metadata["source_csv"],
        metadata["signal_row_index"],
    )
    return {key: _json_safe_value(value) for key, value in metadata.items()}


def _install_optional_dependency_stub(module_name: str) -> None:
    """Install a minimal stub for optional simulator imports not used by simple models."""
    if module_name in sys.modules:
        return

    module = types.ModuleType(module_name)

    def _missing_dependency(*args: Any, **kwargs: Any) -> None:
        raise ImportError(
            f"Optional dependency '{module_name}' is required for this Monte Carlo model."
        )

    if module_name == "arch":
        module.arch_model = _missing_dependency
    elif module_name == "lightgbm":
        module.LGBMRegressor = _missing_dependency

    sys.modules[module_name] = module


def _load_simulator_class(model: str) -> Any:
    """Load the existing simulator class while tolerating unused optional imports."""
    if model == "garch":
        module = importlib.import_module("marketflow.marketflow_monte_carlo_trade")
        return module.MonteCarloTradeSimulator

    for _ in range(len(OPTIONAL_SIMULATOR_IMPORTS) + 1):
        try:
            module = importlib.import_module("marketflow.marketflow_monte_carlo_trade")
            return module.MonteCarloTradeSimulator
        except ModuleNotFoundError as exc:
            if exc.name not in OPTIONAL_SIMULATOR_IMPORTS:
                raise
            _install_optional_dependency_stub(exc.name)

    module = importlib.import_module("marketflow.marketflow_monte_carlo_trade")
    return module.MonteCarloTradeSimulator


def load_latest_close(csv_path: str) -> float | None:
    """
    Load the latest close price from a CSV.

    Return None if the file is missing, malformed, or does not contain a usable
    close column.
    """
    if not csv_path:
        return None

    path = Path(csv_path)
    if not path.exists() or not path.is_file():
        return None

    try:
        last_chunk = None
        for chunk in pd.read_csv(path, usecols=["close"], chunksize=1000):
            last_chunk = chunk
        if last_chunk is None or "close" not in last_chunk.columns:
            return None

        closes = pd.to_numeric(last_chunk["close"], errors="coerce").dropna()
        if closes.empty:
            return None
        return float(closes.iloc[-1])
    except Exception:
        return None


def _classify_output_file(path: Path) -> str:
    """Classify a Monte Carlo output file by filename suffix."""
    name = path.name
    if name.endswith("_mc_summary.json"):
        return "summary_json"
    if name.endswith("_mc_paths.html"):
        return "paths_html"
    if name.endswith("_mc_hits.html"):
        return "hits_html"
    return "unknown"


def list_monte_carlo_outputs(csv_path: str) -> list[dict[str, Any]]:
    """
    List Monte Carlo output files saved beside the selected CSV.

    Return dictionaries sorted newest first. Each dictionary includes path,
    name, kind, modified timestamp, and size in bytes. Missing paths or
    filesystem errors return an empty list.
    """
    if not csv_path:
        return []

    try:
        path = Path(csv_path)
        parent = path.parent
        if not parent.exists() or not parent.is_dir():
            return []

        output_paths: set[Path] = set()
        for pattern in MONTE_CARLO_OUTPUT_PATTERNS:
            output_paths.update(
                file_path for file_path in parent.glob(pattern) if file_path.is_file()
            )

        output_files = []
        for output_path in output_paths:
            stat = output_path.stat()
            output_files.append(
                {
                    "path": str(output_path),
                    "name": output_path.name,
                    "kind": _classify_output_file(output_path),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
                    "size_bytes": int(stat.st_size),
                    "_mtime": stat.st_mtime,
                }
            )

        output_files.sort(key=lambda item: item["_mtime"], reverse=True)
        for item in output_files:
            item.pop("_mtime", None)
        return output_files
    except Exception:
        return []


def enrich_latest_monte_carlo_summary_json(
    csv_path: str | Path,
    join_metadata: dict[str, Any],
) -> dict[str, Any]:
    """Add join metadata to the newest Monte Carlo summary JSON beside a CSV."""
    result = {
        "success": False,
        "path": None,
        "filename": None,
        "errors": [],
        "warnings": [],
    }
    summaries = [
        item
        for item in list_monte_carlo_outputs(str(csv_path))
        if item.get("kind") == "summary_json" and item.get("path")
    ]
    if not summaries:
        result["warnings"].append("No Monte Carlo summary JSON found to enrich.")
        return result

    summary_path = Path(str(summaries[0]["path"]))
    try:
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            result["errors"].append("Monte Carlo summary JSON is not an object.")
            return result
        safe_metadata = _json_safe_value(join_metadata)
        payload["join_metadata"] = safe_metadata
        for key in (
            "ticker",
            "timeframe",
            "source_csv",
            "source_csv_path",
            "source_report_dir",
            "candidate_snapshot_file",
        ):
            if safe_metadata.get(key) is not None:
                payload[key] = safe_metadata.get(key)
        summary_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        result["success"] = True
        result["path"] = str(summary_path)
        result["filename"] = summary_path.name
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def run_monte_carlo_for_csv(
    csv_path: str,
    entry: float | None,
    stop_loss: float,
    take_profit: float,
    timeframe: str | None = None,
    model: str = "bootstrap",
    paths: int = 10000,
    horizon: int = 20,
    block_len: int = 8,
    seed: int = 42,
    nrows: int | None = 4000,
    save_plots: bool = True,
    trade_plan: dict[str, Any] | None = None,
    candidate_snapshot: dict[str, Any] | None = None,
    candidate_snapshot_file: str | None = None,
    source_report_dir: str | Path | None = None,
) -> dict[str, Any]:
    """
    Run a single Monte Carlo trade simulation for one CSV.

    Return a UI-friendly dictionary containing success state, structured error
    details, the selected CSV path, inferred timeframe, and the simulator result.
    """
    path = Path(csv_path) if csv_path else None
    normalized_model = (model or "").strip().lower()

    try:
        if path is None or not path.exists() or not path.is_file():
            raise FileNotFoundError(f"CSV file does not exist: {csv_path}")
        if normalized_model not in SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported Monte Carlo model '{model}'. "
                f"Choose one of: {', '.join(sorted(SUPPORTED_MODELS))}."
            )

        entry_value = None if entry is None else float(entry)
        stop_value = float(stop_loss)
        take_value = float(take_profit)
        if entry_value is not None and entry_value <= 0:
            raise ValueError("Entry must be greater than zero.")
        if stop_value <= 0 or take_value <= 0:
            raise ValueError("Stop loss and take profit must be greater than zero.")
        if entry_value is not None and stop_value >= entry_value:
            raise ValueError("Stop loss must be below entry.")
        if entry_value is not None and take_value <= entry_value:
            raise ValueError("Take profit must be above entry.")
        if int(paths) <= 0:
            raise ValueError("Paths must be positive.")
        if int(horizon) <= 0:
            raise ValueError("Horizon must be positive.")

        selected_timeframe = timeframe or infer_timeframe_from_csv_name(str(path))
        MonteCarloTradeSimulator = _load_simulator_class(normalized_model)
        simulator = MonteCarloTradeSimulator(model_type=normalized_model)
        result = simulator.simulate_trade_for_csv(
            csv_path=str(path),
            tp=take_value,
            sl=stop_value,
            entry=entry_value,
            tf=selected_timeframe,
            horizon_bars=int(horizon),
            model=normalized_model,
            n_paths=int(paths),
            block_len=int(block_len),
            seed=int(seed),
            nrows=nrows,
            save_plots=save_plots,
            save_json=True,
        )
        join_metadata = build_monte_carlo_join_metadata(
            csv_path=path,
            timeframe=selected_timeframe,
            trade_plan=trade_plan,
            candidate_snapshot=candidate_snapshot,
            candidate_snapshot_file=candidate_snapshot_file,
            source_report_dir=source_report_dir,
        )
        if isinstance(result, dict):
            result["join_metadata"] = join_metadata
            for key in ("ticker", "timeframe", "source_csv", "source_csv_path", "candidate_snapshot_file"):
                if join_metadata.get(key) is not None:
                    result[key] = join_metadata.get(key)
        enrichment_result = enrich_latest_monte_carlo_summary_json(path, join_metadata)

        return {
            "success": True,
            "error": None,
            "error_type": None,
            "traceback": None,
            "csv_path": str(path),
            "timeframe": selected_timeframe,
            "ticker": join_metadata.get("ticker"),
            "source_csv": join_metadata.get("source_csv"),
            "source_csv_path": join_metadata.get("source_csv_path"),
            "candidate_snapshot_file": join_metadata.get("candidate_snapshot_file"),
            "join_metadata": join_metadata,
            "summary_enrichment": enrichment_result,
            "result": result,
            "output_files": list_monte_carlo_outputs(str(path)),
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "traceback": traceback.format_exc(),
            "csv_path": str(path) if path else csv_path,
            "timeframe": timeframe or infer_timeframe_from_csv_name(csv_path or ""),
            "result": None,
            "output_files": [],
        }
