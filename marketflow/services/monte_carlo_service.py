"""Service helpers for running single-trade Monte Carlo simulations."""

from __future__ import annotations

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

        return {
            "success": True,
            "error": None,
            "error_type": None,
            "traceback": None,
            "csv_path": str(path),
            "timeframe": selected_timeframe,
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
