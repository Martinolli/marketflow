"""UI-safe helpers for generating Point & Figure sidecar outputs."""

from __future__ import annotations

import json
import time
import traceback as traceback_module
import importlib.util
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.report_index import infer_timeframe_from_csv_name


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


def _pnf_box_metadata(box_size: float | None, pnf_scale: str | None, pnf_scale_value: float | None) -> tuple[str, float | None]:
    """Return the user-facing P&F box mode and value used by Studio."""
    if pnf_scale:
        return str(pnf_scale), float(pnf_scale_value) if pnf_scale_value is not None else None
    if box_size is not None:
        return "fixed", float(box_size)
    return "auto", None


def _write_sidecar_metadata(
    sidecar_path: Path | None,
    *,
    csv_path: Path,
    box_size: float | None,
    reversal: int,
    nrows: int | None,
    pnf_scale: str | None,
    pnf_scale_value: float | None,
) -> dict[str, Any]:
    """Ensure newly generated Studio sidecars carry source/timeframe traceability."""
    data = _load_sidecar(sidecar_path)
    if not data or sidecar_path is None:
        return data

    box_mode, box_value = _pnf_box_metadata(box_size, pnf_scale, pnf_scale_value)
    data.update(
        {
            "source_csv": csv_path.name,
            "source_csv_path": str(csv_path),
            "inferred_timeframe": infer_timeframe_from_csv_name(str(csv_path)),
            "generated_by": "marketflow_studio",
            "box_mode": box_mode,
            "box_value": box_value,
            "box_size": data.get("box_size") if data.get("box_size") is not None else data.get("box"),
            "reversal": int(data.get("reversal") or reversal),
            "nrows": nrows,
            "generated_at": data.get("generated_at") or datetime.now(timezone.utc).isoformat(),
        }
    )
    try:
        sidecar_path.write_text(json.dumps(data, indent=2, default=float), encoding="utf-8")
    except Exception:
        pass
    return data


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
    source_csv: str | None = None,
    source_csv_path: str | None = None,
    inferred_timeframe: str | None = None,
    generated_by: str | None = None,
    box_mode: str | None = None,
    box_value: float | None = None,
    nrows: int | None = None,
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
        "source_csv": source_csv,
        "source_csv_path": source_csv_path,
        "inferred_timeframe": inferred_timeframe,
        "generated_by": generated_by,
        "box_mode": box_mode,
        "box_value": box_value,
        "nrows": nrows,
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
            source_csv_path=str(path),
            generated_by="marketflow_studio",
            nrows=nrows,
        )

        html_path = Path(str(sidecar.get("path"))) if isinstance(sidecar, dict) and sidecar.get("path") else None
        if not html_path or not html_path.exists():
            html_path = _newest_file(output_dir, "*_point_and_figure_plot.html", since=started_at)
        sidecar_path = _newest_file(output_dir, "*_pnf_meta.json", since=started_at)
        sidecar_data = _write_sidecar_metadata(
            sidecar_path,
            csv_path=path,
            box_size=box_size,
            reversal=reversal,
            nrows=nrows,
            pnf_scale=pnf_scale,
            pnf_scale_value=pnf_scale_value,
        )
        count = sidecar_data.get("count") if isinstance(sidecar_data.get("count"), dict) else {}
        columns = sidecar_data.get("columns") if isinstance(sidecar_data.get("columns"), list) else []
        box_mode, box_value = _pnf_box_metadata(box_size, pnf_scale, pnf_scale_value)

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
            source_csv=sidecar_data.get("source_csv") or path.name,
            source_csv_path=sidecar_data.get("source_csv_path") or str(path),
            inferred_timeframe=sidecar_data.get("inferred_timeframe") or infer_timeframe_from_csv_name(str(path)),
            generated_by=sidecar_data.get("generated_by") or "marketflow_studio",
            box_mode=sidecar_data.get("box_mode") or box_mode,
            box_value=sidecar_data.get("box_value") if sidecar_data.get("box_value") is not None else box_value,
            nrows=sidecar_data.get("nrows") if sidecar_data.get("nrows") is not None else nrows,
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
