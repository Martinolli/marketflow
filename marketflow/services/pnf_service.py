"""UI-safe helpers for generating Point & Figure sidecar outputs."""

from __future__ import annotations

import json
import time
import traceback as traceback_module
import importlib.util
from pathlib import Path
from typing import Any

import pandas as pd


def _plot_point_and_figure_callable() -> Any:
    """Load the existing script helper without requiring scripts/ to be a package."""
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "plot_annotated_features.py"
    spec = importlib.util.spec_from_file_location("marketflow_plot_annotated_features", script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load P&F plotting script: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.plot_point_and_figure


def _newest_file(output_dir: Path, pattern: str, since: float | None = None) -> Path | None:
    """Return the newest matching file, preferring files modified after ``since``."""
    files = [path for path in output_dir.glob(pattern) if path.is_file()]
    if not files:
        return None
    if since is not None:
        recent = [path for path in files if path.stat().st_mtime >= since]
        if recent:
            files = recent
    return max(files, key=lambda path: path.stat().st_mtime)


def _load_sidecar(path: Path | None) -> dict[str, Any]:
    """Load a generated P&F sidecar when available."""
    if not path or not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _result(
    *,
    success: bool,
    csv_path: str,
    output_dir: str | None = None,
    html_path: str | None = None,
    sidecar_path: str | None = None,
    box_size: float | None = None,
    reversal: int = 3,
    last_price: float | None = None,
    columns_count: int | None = None,
    objective: float | None = None,
    error: str | None = None,
    traceback: str | None = None,
) -> dict[str, Any]:
    """Build a stable P&F generation result."""
    return {
        "success": success,
        "csv_path": csv_path,
        "output_dir": output_dir,
        "html_path": html_path,
        "sidecar_path": sidecar_path,
        "box_size": box_size,
        "reversal": reversal,
        "last_price": last_price,
        "columns_count": columns_count,
        "objective": objective,
        "error": error,
        "traceback": traceback,
    }


def generate_pnf_for_csv(
    csv_path: str,
    box_size: float | None = None,
    reversal: int = 3,
    nrows: int | None = None,
    pnf_scale: str | None = None,
    pnf_scale_value: float | None = None,
) -> dict[str, Any]:
    """
    Generate a P&F HTML plot and P&F sidecar JSON for one annotated CSV.

    Return a structured result suitable for Streamlit display.
    """
    path = Path(str(csv_path))
    if not path.exists() or not path.is_file():
        return _result(success=False, csv_path=str(csv_path), reversal=reversal, error="CSV file does not exist.")

    output_dir = path.parent
    try:
        dataframe = pd.read_csv(path)
        required_columns = {"high", "low", "close"}
        missing_columns = sorted(required_columns.difference(dataframe.columns))
        if missing_columns:
            return _result(
                success=False,
                csv_path=str(path),
                output_dir=str(output_dir),
                reversal=reversal,
                error=f"CSV is missing required P&F columns: {', '.join(missing_columns)}.",
            )
        if nrows is not None and nrows > 0:
            dataframe = dataframe.tail(int(nrows))
        if dataframe.empty:
            return _result(
                success=False,
                csv_path=str(path),
                output_dir=str(output_dir),
                reversal=reversal,
                error="CSV has no rows available for P&F generation.",
            )

        started_at = time.time() - 1.0
        plot_point_and_figure = _plot_point_and_figure_callable()

        sidecar = plot_point_and_figure(
            dataframe,
            output_dir=str(output_dir),
            csv_file_name=path.name,
            show=False,
            box_size=box_size,
            reversal=reversal,
            wyckoff_overlay=False,
            pnf_scale=pnf_scale,
            pnf_scale_value=pnf_scale_value,
        )

        html_path = Path(str(sidecar.get("path"))) if isinstance(sidecar, dict) and sidecar.get("path") else None
        if not html_path or not html_path.exists():
            html_path = _newest_file(output_dir, "*_point_and_figure_plot.html", since=started_at)
        sidecar_path = _newest_file(output_dir, "*_pnf_meta.json", since=started_at)
        sidecar_data = _load_sidecar(sidecar_path)
        count = sidecar_data.get("count") if isinstance(sidecar_data.get("count"), dict) else {}
        columns = sidecar_data.get("columns") if isinstance(sidecar_data.get("columns"), list) else []

        return _result(
            success=True,
            csv_path=str(path),
            output_dir=str(output_dir),
            html_path=str(html_path) if html_path else None,
            sidecar_path=str(sidecar_path) if sidecar_path else None,
            box_size=float(sidecar_data.get("box")) if sidecar_data.get("box") is not None else box_size,
            reversal=int(sidecar_data.get("reversal") or reversal),
            last_price=float(sidecar_data.get("last_price")) if sidecar_data.get("last_price") is not None else None,
            columns_count=len(columns) if columns else None,
            objective=float(count.get("objective")) if count.get("objective") is not None else None,
            error=None,
        )
    except Exception as exc:
        return _result(
            success=False,
            csv_path=str(path),
            output_dir=str(output_dir),
            reversal=reversal,
            error=f"{type(exc).__name__}: {exc}",
            traceback=traceback_module.format_exc(),
        )


def generate_pnf_for_csvs(
    csv_paths: list[str],
    box_size: float | None = None,
    reversal: int = 3,
    nrows: int | None = None,
    pnf_scale: str | None = None,
    pnf_scale_value: float | None = None,
) -> list[dict[str, Any]]:
    """
    Generate P&F outputs for multiple CSVs.
    Continue after individual failures.
    """
    results: list[dict[str, Any]] = []
    for index, csv_path in enumerate(csv_paths):
        if index:
            time.sleep(1.05)
        results.append(
            generate_pnf_for_csv(
                csv_path,
                box_size=box_size,
                reversal=reversal,
                nrows=nrows,
                pnf_scale=pnf_scale,
                pnf_scale_value=pnf_scale_value,
            )
        )
    return results
