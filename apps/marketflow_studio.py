"""Minimal local Streamlit interface for MarketFlow."""

from __future__ import annotations

import os
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("MARKETFLOW_CONSOLE_LOG_LEVEL", "WARNING")

import streamlit as st
import streamlit.components.v1 as components

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from marketflow.charts.pnf_chart import build_pnf_chart_from_sidecar
from marketflow.charts.eigen_chart import build_price_volume_eigen_chart
from marketflow.charts.wyckoff_chart import build_basic_wyckoff_candlestick_chart
from marketflow.services.analysis_service import run_single_ticker
from marketflow.services.analyst_chat_service import (
    build_response_filename,
    get_analyst_chat_config_status,
    run_analyst_chat,
)
from marketflow.services.analyst_packet_service import (
    build_analyst_packet,
    load_pnf_sidecars,
    load_default_analyst_profile,
    packet_to_pretty_json,
)
from marketflow.services.analyst_prompt_service import (
    PROMPT_STYLES,
    build_prompt_filename,
    build_wyckoff_analyst_prompt,
)
from marketflow.services.artifact_service import (
    generate_legacy_feature_plots_for_csv,
    list_report_artifacts,
    read_text_artifact,
)
from marketflow.services.backtest_calibration_artifact_service import (
    summarize_folder_to_backtest_calibration_markdown,
)
from marketflow.services.backtest_calibration_service import summarize_backtest_results_folder
from marketflow.services.backtest_candidate_artifact_service import write_backtest_candidate_csv
from marketflow.services.backtest_candidate_service import build_candidate_snapshot_from_strategy_candidate
from marketflow.services.backtest_result_service import (
    evaluate_candidate_snapshot_csv_to_results_csv,
    read_candidate_snapshot_csv,
)
from marketflow.services.batch_service import (
    normalize_batch_tickers,
    run_batch_analysis,
)
from marketflow.services.data_sufficiency_artifact_service import (
    summarize_folder_to_data_sufficiency_markdown,
)
from marketflow.services.data_sufficiency_service import (
    summarize_report_folder_data_sufficiency,
)
from marketflow.services.eigen_service import (
    compare_price_volume_eigen_windows,
    review_eigen_wyckoff_proximity,
    run_price_volume_eigen_for_csv,
)
from marketflow.services.monte_carlo_service import (
    list_monte_carlo_outputs,
    load_latest_close,
    run_monte_carlo_for_csv,
)
from marketflow.services.monte_carlo_calibration_artifact_service import (
    summarize_folder_to_monte_carlo_calibration_markdown,
)
from marketflow.services.monte_carlo_calibration_service import (
    summarize_monte_carlo_calibration_folder,
)
from marketflow.services.pnf_service import (
    classify_pnf_sidecar_source,
    generate_pnf_for_csv,
    generate_pnf_for_csvs,
    pnf_sidecar_source_warning,
)
from marketflow.services.report_index import (
    find_latest_ticker_report,
    infer_timeframe_from_csv_name,
    list_annotated_csv_files,
    list_available_tickers,
    list_report_date_folders,
    list_report_files,
    load_csv_for_chart,
    load_csv_preview,
    load_report_json,
    load_summary_text,
)
from marketflow.services.strategy_service import (
    get_report_root,
    normalize_tickers,
    rank_latest_candidates,
)


DEFAULT_TIMEFRAMES = ["1d", "4h", "1h"]
TIMEFRAME_OPTIONS = ["1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"]
CSV_PREVIEW_ROW_OPTIONS = [100, 250, 500, 1000]
CHART_ROW_OPTIONS = [200, 500, 1000, 2000]
PNF_ROW_OPTIONS = ["All", 200, 500, 1000, 2000]
LEGACY_PLOT_ROW_OPTIONS = ["All", 200, 500, 1000, 2000]
STRATEGY_TIMEFRAMES = ["1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"]
WYCKOFF_PHASE_OPTIONS = ["A", "B", "C", "D", "E", "UNKNOWN"]
MONTE_CARLO_MODELS = ["bootstrap", "gbm", "garch"]


def _load_latest_result(ticker: str) -> dict[str, Any]:
    """Load the newest generated report bundle for a ticker."""
    report_dir = find_latest_ticker_report(ticker)
    report_json = load_report_json(report_dir, ticker) if report_dir else None
    summary_text = load_summary_text(report_dir, ticker) if report_dir else None

    return {
        "ticker": ticker,
        "narrative": summary_text or "",
        "output_dir": report_dir,
        "success": bool(report_dir),
        "error": None if report_dir else f"No report found for {ticker}. Run an analysis first.",
        "error_type": None,
        "traceback": None,
        "report_json": report_json,
        "summary_text": summary_text,
        "report_files": list_report_files(report_dir) if report_dir else [],
    }


def _nested_get(data: dict[str, Any] | None, keys: list[str]) -> Any:
    """Read a nested value from a dictionary, returning None if any key is missing."""
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def _display_value(label: str, value: Any) -> None:
    """Display a scalar value if it is available."""
    if value is not None and value != "":
        st.metric(label, value)


def _format_probability(value: Any) -> str | None:
    """Format a probability-like value for display."""
    if value is None:
        return None
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return None


def _format_number(value: Any, decimals: int = 4) -> str | None:
    """Format a numeric value for compact metric display."""
    if value is None:
        return None
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def _stringify_display_value(value: Any) -> str:
    """Convert one display-table value to an Arrow-safe string."""
    if value is None:
        return ""
    if isinstance(value, float):
        return _format_number(value, decimals=6) or ""
    if isinstance(value, (str, int, bool)):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list):
        if all(not isinstance(item, (dict, list, tuple, set)) for item in value):
            return "; ".join(_stringify_display_value(item) for item in value)
        return json.dumps(value, default=str, separators=(",", ": "))
    if isinstance(value, dict):
        return json.dumps(value, default=str, separators=(",", ": "))
    return str(value)


def _safe_dataframe_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """
    Convert dataframe display rows to Arrow-safe strings.

    Intended only for UI display tables where mixed numeric/string/object columns
    can cause Streamlit/PyArrow serialization errors.
    """
    safe_rows: list[dict[str, str]] = []
    for row in rows:
        if isinstance(row, dict):
            safe_rows.append({str(key): _stringify_display_value(value) for key, value in row.items()})
        else:
            safe_rows.append({"value": _stringify_display_value(row)})
    return safe_rows


def _format_ui_number(value: Any, decimals: int = 2) -> str | None:
    """Format UI numbers without long floating point tails."""
    if value is None or value == "":
        return None
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def _is_formatted_number(value: str | None) -> bool:
    """Return True when a formatted string contains a plain number."""
    if value is None:
        return False
    return value.replace(".", "", 1).replace("-", "", 1).isdigit()


def _format_ui_price(value: Any, decimals: int = 2) -> str | None:
    """Format a price-like value for display."""
    formatted = _format_ui_number(value, decimals=decimals)
    return f"${formatted}" if _is_formatted_number(formatted) else formatted


def _format_ui_percent(value: Any, decimals: int = 2) -> str | None:
    """Format a percent-like value for display."""
    formatted = _format_ui_number(value, decimals=decimals)
    return f"{formatted}%" if _is_formatted_number(formatted) else formatted


def _display_optional_metric(label: str, value: Any) -> None:
    """Display a metric when available, otherwise show a muted missing value."""
    if value is None or value == "":
        st.caption(f"{label}: not available")
    else:
        st.metric(label, value)


def _render_error_details(result: dict[str, Any]) -> None:
    """Render a compact error message with debug details hidden by default."""
    if not result.get("error"):
        return

    error_type = result.get("error_type")
    if error_type:
        st.error(f"{error_type}: {result['error']}")
    else:
        st.error(result["error"])

    with st.expander("Error details"):
        if error_type:
            st.write(f"Type: `{error_type}`")
        if result.get("traceback"):
            st.code(result["traceback"], language="python")
        else:
            st.write("No traceback is available.")


def _report_dir_from_result(
    result: dict[str, Any] | None,
    empty_message: str,
) -> str | None:
    """Return the loaded report directory or render a friendly empty/error state."""
    if not result or not result.get("output_dir"):
        st.info(empty_message)
        return None

    report_dir = result["output_dir"]
    report_path = Path(report_dir)
    if not report_path.exists() or not report_path.is_dir():
        st.warning(f"Report directory does not exist: {report_dir}")
        return None

    return report_dir


def _render_loaded_report_caption(result: dict[str, Any] | None) -> None:
    """Show the currently loaded ticker and report directory when available."""
    if not result:
        st.caption("No report loaded. Use Run Analysis or Load Latest Report.")
        return

    ticker = result.get("ticker") or "unknown ticker"
    if result.get("output_dir"):
        st.caption(f"Loaded: `{ticker}` | `{result['output_dir']}`")
    elif result.get("error"):
        st.caption(f"No loaded report for {ticker}.")


def _annotated_csv_files_for_report(report_dir: str) -> list[str]:
    """Return annotated CSV files for a loaded report directory."""
    return list_annotated_csv_files(report_dir)


def _wyckoff_annotated_csv_files(csv_files: list[str]) -> list[str]:
    """Return only CSV files ending with `_wyckoff_annotated.csv`."""
    return [
        path
        for path in csv_files
        if Path(path).name.lower().endswith("_wyckoff_annotated.csv")
    ]


def _select_annotated_csv(
    csv_files: list[str],
    label: str,
    key: str,
) -> str:
    """Render a CSV selector using filenames as labels."""
    return st.selectbox(
        label,
        options=csv_files,
        format_func=lambda path: Path(path).name,
        key=key,
    )


def _default_csv_for_timeframe(
    csv_files: list[str],
    timeframe: str | None,
    *,
    annotated_only: bool = False,
) -> str | None:
    """Return the first CSV matching a timeframe for initial selector defaults."""
    if not timeframe:
        return None

    source_files = _wyckoff_annotated_csv_files(csv_files) if annotated_only else csv_files
    for csv_path in source_files:
        if infer_timeframe_from_csv_name(csv_path) == timeframe:
            return csv_path
    return None


def _select_csv_with_default(
    csv_files: list[str],
    label: str,
    key: str,
    *,
    default_csv: str | None = None,
) -> str:
    """Render a CSV selector that preserves its own selection across reruns."""
    selected_csv = st.session_state.get(key)
    if selected_csv not in csv_files:
        st.session_state[key] = default_csv if default_csv in csv_files else csv_files[0]

    return st.selectbox(
        label,
        options=csv_files,
        format_func=lambda path: Path(path).name,
        key=key,
    )


def _render_csv_file_context(csv_path: str) -> str | None:
    """Display selected CSV metadata shared by preview and chart tabs."""
    timeframe = infer_timeframe_from_csv_name(csv_path)
    st.write(f"Filename: `{Path(csv_path).name}`")
    if timeframe:
        st.write(f"Timeframe: `{timeframe}`")
    else:
        st.caption("Timeframe could not be inferred from the filename.")
    return timeframe


def _pnf_sidecar_label(sidecar: dict[str, Any]) -> str:
    """Return a compact label for a P&F sidecar selector."""
    parts = [str(sidecar.get("filename") or Path(str(sidecar.get("path") or "")).name or "P&F sidecar")]
    details = []
    source_type = sidecar.get("source_type") or classify_pnf_sidecar_source(sidecar)
    for key in ("inferred_timeframe", "timeframe"):
        value = sidecar.get(key)
        if value is not None and value != "":
            details.append(f"{key}: {value}")
    details.append(f"source: {source_type}")
    for key in ("direction", "objective"):
        value = sidecar.get(key)
        if value is not None and value != "":
            details.append(f"{key}: {value}")
    if details:
        parts.append(" | ".join(details))
    return " - ".join(parts)


def _pnf_metadata_row(sidecar: dict[str, Any]) -> dict[str, Any]:
    """Return compact metadata for the selected P&F sidecar."""
    source_type = sidecar.get("source_type") or classify_pnf_sidecar_source(sidecar)
    return {
        "filename": sidecar.get("filename"),
        "source_csv": sidecar.get("source_csv"),
        "source_type": source_type,
        "source_warning": sidecar.get("source_warning") or pnf_sidecar_source_warning(source_type),
        "timeframe": sidecar.get("inferred_timeframe") or sidecar.get("timeframe"),
        "direction": sidecar.get("direction"),
        "box_mode": sidecar.get("box_mode"),
        "box_value": sidecar.get("box_value"),
        "box_size": sidecar.get("box_size"),
        "reversal": sidecar.get("reversal"),
        "last_price": sidecar.get("last_price"),
        "breakout_level": sidecar.get("breakout_level"),
        "objective": sidecar.get("objective"),
        "objective_direction": sidecar.get("objective_direction"),
        "objective_quality": sidecar.get("objective_quality"),
        "objective_supports_trade": sidecar.get("objective_supports_trade"),
        "objective_distance_pct": sidecar.get("objective_distance_pct"),
        "objective_r_multiple": sidecar.get("objective_r_multiple"),
        "objective_notes": "; ".join(sidecar.get("objective_notes") or []),
    }


def _pnf_source_review_rows(sidecars: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return compact P&F sidecar source hygiene rows."""
    rows = []
    for sidecar in sidecars:
        source_type = sidecar.get("source_type") or classify_pnf_sidecar_source(sidecar)
        rows.append(
            {
                "filename": sidecar.get("filename"),
                "source_csv": sidecar.get("source_csv"),
                "timeframe": sidecar.get("inferred_timeframe") or sidecar.get("timeframe"),
                "source_type": source_type,
                "objective": sidecar.get("objective"),
                "last_price": sidecar.get("last_price"),
                "generated_by": sidecar.get("generated_by"),
                "source_warning": sidecar.get("source_warning") or pnf_sidecar_source_warning(source_type),
            }
        )
    return rows


def _pnf_generation_result_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return compact rows for P&F generation results."""
    rows: list[dict[str, Any]] = []
    for result in results:
        rows.append(
            {
                "success": result.get("success"),
                "csv": Path(str(result.get("csv_path") or "")).name,
                "timeframe": result.get("inferred_timeframe"),
                "box_mode": result.get("box_mode"),
                "box_value": result.get("box_value"),
                "box_size": result.get("box_size"),
                "reversal": result.get("reversal"),
                "nrows": result.get("nrows"),
                "last_price": result.get("last_price"),
                "columns_count": result.get("columns_count"),
                "objective": result.get("objective"),
                "sidecar_path": result.get("sidecar_path"),
                "error": result.get("error"),
            }
        )
    return rows


def _legacy_generation_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Return compact rows for generated legacy plot paths."""
    return [
        {
            "kind": Path(path).suffix.lower().lstrip("."),
            "name": Path(path).name,
            "path": path,
        }
        for path in result.get("generated_paths") or []
    ]


def _eigen_preview_rows(dataframe: Any) -> list[dict[str, Any]]:
    """Return compact preview rows for Price-Volume Eigen output."""
    if dataframe is None or getattr(dataframe, "empty", True):
        return []

    preview_columns = [
        "timestamp",
        "date",
        "datetime",
        "close",
        "volume",
        "pv_result_z",
        "pv_effort_z",
        "pv_eigen_coupling",
        "pv_eigen_residual",
        "pv_eigen_harmony",
        "pv_effort_result_divergence",
        "pv_divergence_strength",
    ]
    available = [column for column in preview_columns if column in dataframe.columns]
    return dataframe[available].tail(25).to_dict(orient="records") if available else []


def _render_eigen_chart_for_csv(csv_path: str, chart_rows: int, title: str | None = None) -> None:
    """Load and render a Price-Volume Eigen chart preview."""
    dataframe = load_csv_preview(csv_path, nrows=int(chart_rows))
    if dataframe is None:
        st.warning("Could not load the Eigen CSV for chart preview.")
        return
    fig = build_price_volume_eigen_chart(
        dataframe,
        title=title or Path(csv_path).stem,
        max_rows=int(chart_rows),
    )
    st.plotly_chart(fig, use_container_width=True)


def _parse_window_list(text: str, default: tuple[int, ...] = (20, 40, 60)) -> list[int]:
    """Parse a compact window list from comma/space/semicolon text."""
    parsed: set[int] = set()
    for token in re.split(r"[,;\s]+", str(text or "")):
        if not token:
            continue
        try:
            window = int(token)
        except ValueError:
            continue
        if window >= 5:
            parsed.add(window)
    if parsed:
        return sorted(parsed)
    return sorted({int(value) for value in default if int(value) >= 5})


def _markdown_cell(value: Any) -> str:
    """Return one markdown table cell with pipes normalized."""
    text = _summary_value(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _markdown_table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    """Build a compact markdown table from dict rows."""
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join("---" for _ in headers) + " |"
    data_lines = [
        "| " + " | ".join(_markdown_cell(row.get(header)) for header in headers) + " |"
        for row in rows
    ]
    if not data_lines:
        data_lines = ["| " + " | ".join("not available" for _ in headers) + " |"]
    return "\n".join([header_line, separator_line, *data_lines])


def _markdown_notes(notes: Any) -> str:
    """Build markdown bullet lines for a note list."""
    if not isinstance(notes, list) or not notes:
        return "- not available"
    lines = [f"- {_summary_value(note)}" for note in notes if note]
    return "\n".join(lines) if lines else "- not available"


def _eigen_review_summary_filename(source_csv: str) -> str:
    """Return a timestamped markdown filename for an Eigen review summary."""
    stem = Path(str(source_csv or "")).stem
    match = re.match(r"(?P<ticker>[A-Za-z0-9.-]+)_(?P<timeframe>1mo|1w|1d|4h|2h|1h|30m|15m|5m|1m)", stem)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if match:
        ticker = _safe_filename_part(match.group("ticker"), "marketflow")
        timeframe = _safe_filename_part(match.group("timeframe"), "selected")
        return f"{ticker}_{timeframe}_eigen_review_summary_{timestamp}.md"
    return f"eigen_review_summary_{timestamp}.md"


def _build_eigen_review_summary_markdown(
    *,
    source_csv: str,
    window_comparison: dict[str, Any] | None = None,
    proximity_review: dict[str, Any] | None = None,
) -> str:
    """
    Build a markdown artifact summarizing Eigen diagnostics.

    This is a reporting artifact only.
    It does not create signals or modify analytical logic.
    """
    comparison = window_comparison if isinstance(window_comparison, dict) else {}
    proximity = proximity_review if isinstance(proximity_review, dict) else {}
    comparison_interpretation = (
        comparison.get("interpretation") if isinstance(comparison.get("interpretation"), dict) else {}
    )
    proximity_summary = proximity.get("summary") if isinstance(proximity.get("summary"), dict) else {}
    result_mode = comparison.get("result_mode") or proximity.get("result_mode")
    effort_mode = comparison.get("effort_mode") or proximity.get("effort_mode")

    comparison_headers = [
        "window",
        "valid_rows",
        "divergence_count",
        "divergence_rate",
        "latest_residual",
        "latest_coupling",
        "latest_harmony",
        "latest_divergence",
        "max_residual",
        "mean_residual",
        "mean_coupling",
        "last_divergence_timestamp",
    ]
    proximity_headers = [
        "timestamp",
        "close",
        "residual",
        "coupling",
        "harmony",
        "divergence",
        "reason",
        "wyckoff_event",
        "confirmed_event",
        "proximity_status",
        "note",
    ]
    proximity_rows = []
    for row in proximity.get("review") or []:
        if not isinstance(row, dict):
            continue
        proximity_rows.append(
            {
                "timestamp": row.get("timestamp"),
                "close": row.get("close"),
                "residual": row.get("pv_eigen_residual"),
                "coupling": row.get("pv_eigen_coupling"),
                "harmony": row.get("pv_eigen_harmony"),
                "divergence": row.get("pv_effort_result_divergence"),
                "reason": row.get("attention_reason"),
                "wyckoff_event": row.get("wyckoff_event"),
                "confirmed_event": row.get("wyckoff_confirmed_event"),
                "proximity_status": row.get("proximity_status"),
                "note": row.get("note"),
            }
        )

    windows = comparison.get("windows") or [
        row.get("window")
        for row in comparison.get("comparison") or []
        if isinstance(row, dict) and row.get("window") is not None
    ]

    return f"""# MarketFlow Eigen Review Summary

## Metadata
- Created: {datetime.now().astimezone().isoformat(timespec="seconds")}
- Source CSV: {_summary_value(source_csv)}
- Result mode: {_summary_value(result_mode)}
- Effort mode: {_summary_value(effort_mode)}

## Window Comparison
- Windows: {_summary_notes(windows)}
- Broad observation: {_summary_value(comparison_interpretation.get("broad_observation"))}
- Notes:
{_markdown_notes(comparison_interpretation.get("notes"))}

### Window Comparison Table
{_markdown_table(comparison_headers, comparison.get("comparison") or [])}

## Eigen-Wyckoff Proximity Review
- Window: {_summary_value(proximity.get("window"))}
- Residual threshold: {_summary_value(proximity.get("residual_threshold"))}
- Proximity bars: {_summary_value(proximity.get("proximity_bars"))}
- Attention rows: {_summary_value(proximity.get("attention_count"))}
- Matched events: {_summary_value(proximity.get("matched_event_count"))}
- Eigen-only rows: {_summary_value(proximity.get("unmatched_attention_count"))}
- Broad observation: {_summary_value(proximity_summary.get("broad_observation"))}
- Notes:
{_markdown_notes(proximity_summary.get("notes"))}

### Proximity Review Table
{_markdown_table(proximity_headers, proximity_rows)}

## Interpretation Guardrails
- This artifact summarizes diagnostic Eigen outputs only.
- Eigen attention rows are not trading signals.
- Eigen-only rows are areas for visual review, not inferred Wyckoff events.
- This artifact does not change Strategy Ranking, Monte Carlo, P&F, or Analyst Packet decisions.
"""


def _classify_report_file(file_path: str) -> str:
    """Classify a generated report file for compact display."""
    name = Path(file_path).name.lower()
    if name.endswith("_summary_report.txt"):
        return "summary"
    if name.endswith("_llm_analysis.json") or name.endswith("_report.json"):
        return "report_json"
    if name.endswith("_wyckoff_annotated.csv"):
        return "annotated_csv"
    if name.endswith("_mc_summary.json"):
        return "monte_carlo_json"
    if name.endswith("_mc_paths.html") or name.endswith("_mc_hits.html"):
        return "monte_carlo_html"
    if name.endswith(".csv"):
        return "csv"
    if name.endswith(".html"):
        return "html"
    return "other"


def _report_file_rows(files: list[str]) -> list[dict[str, Any]]:
    """Build compact generated-file rows for Reports tab display."""
    return [
        {
            "Type": _classify_report_file(file_path),
            "Filename": Path(file_path).name,
            "Timeframe": infer_timeframe_from_csv_name(file_path) or "",
            "Full Path": file_path,
        }
        for file_path in files
    ]


def _artifact_display_rows(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return display rows for generated report artifacts."""
    return [
        {
            "kind": artifact.get("kind"),
            "timeframe": artifact.get("timeframe") or "",
            "source_csv": artifact.get("source_csv") or "",
            "box_size": artifact.get("box_size") or "",
            "reversal": artifact.get("reversal") or "",
            "name": artifact.get("name"),
            "modified": artifact.get("modified"),
            "size": artifact.get("size"),
            "path": artifact.get("path"),
        }
        for artifact in artifacts
    ]


def _artifact_label(artifact: dict[str, Any]) -> str:
    """Return a compact label for artifact selectors."""
    parts = [str(artifact.get("kind") or "artifact")]
    timeframe = artifact.get("timeframe")
    if timeframe:
        parts.append(str(timeframe))
    parts.append(str(artifact.get("name") or artifact.get("path") or "unnamed"))
    return " | ".join(parts)


def _artifact_mime_type(path: str) -> str:
    """Return a reasonable download MIME type for an artifact path."""
    suffix = Path(path).suffix.lower()
    if suffix == ".html":
        return "text/html"
    if suffix == ".json":
        return "application/json"
    if suffix == ".txt":
        return "text/plain"
    if suffix == ".md":
        return "text/markdown"
    if suffix == ".csv":
        return "text/csv"
    return "application/octet-stream"


def _render_artifact_preview(artifact: dict[str, Any], key_prefix: str, report_dir: str) -> None:
    """Render preview and download controls for one selected artifact."""
    artifact_path = str(artifact.get("path") or "")
    if not artifact_path:
        st.info("No artifact selected for preview.")
        return

    preview_result = read_text_artifact(artifact_path, report_dir=report_dir)
    if preview_result.get("success"):
        text = preview_result.get("text") or ""
        suffix = Path(artifact_path).suffix.lower()
        if suffix == ".html":
            components.html(text, height=700, scrolling=True)
        elif suffix == ".md":
            st.markdown(text)
            show_raw = st.checkbox(
                "Show raw markdown",
                value=False,
                key=f"{key_prefix}_show_raw_markdown",
            )
            if show_raw:
                st.divider()
                st.code(text, language="markdown")
        elif suffix == ".json":
            try:
                st.json(json.loads(text))
            except json.JSONDecodeError:
                st.code(text, language="json")
        else:
            st.code(text, language="text")
    elif preview_result.get("too_large"):
        st.info(preview_result.get("error") or "Artifact is too large to preview.")
    else:
        st.info(preview_result.get("error") or "This artifact is not previewable.")

    if st.button("Prepare download", key=f"{key_prefix}_prepare_download"):
        st.session_state[f"{key_prefix}_download_path"] = artifact_path

    if st.session_state.get(f"{key_prefix}_download_path") == artifact_path:
        try:
            data = Path(artifact_path).read_bytes()
            st.download_button(
                "Download selected artifact",
                data=data,
                file_name=Path(artifact_path).name,
                mime=_artifact_mime_type(artifact_path),
                key=f"{key_prefix}_download",
            )
        except Exception as exc:
            st.warning(f"Could not prepare download: {type(exc).__name__}: {exc}")
    else:
        st.caption("Download bytes are prepared only after you click Prepare download.")


def _render_generated_artifacts(report_dir: str, key_prefix: str = "report_artifacts") -> list[dict[str, Any]]:
    """Render a unified artifact browser for saved report outputs."""
    st.markdown("#### Generated Artifacts")
    artifacts = list_report_artifacts(report_dir)
    if not artifacts:
        st.info("No generated artifacts found in this report directory.")
        return []

    kind_options = sorted({str(artifact.get("kind")) for artifact in artifacts if artifact.get("kind")})
    selected_kinds = st.multiselect(
        "Artifact kinds",
        options=kind_options,
        default=kind_options,
        key=f"{key_prefix}_kind_filter",
    )

    timeframe_options = sorted(
        {str(artifact.get("timeframe")) for artifact in artifacts if artifact.get("timeframe")},
        key=lambda value: TIMEFRAME_OPTIONS.index(value) if value in TIMEFRAME_OPTIONS else len(TIMEFRAME_OPTIONS),
    )
    selected_timeframe = st.selectbox(
        "Artifact timeframe",
        options=["All", *timeframe_options],
        key=f"{key_prefix}_timeframe_filter",
    )

    filtered_artifacts = [
        artifact
        for artifact in artifacts
        if artifact.get("kind") in selected_kinds
        and (selected_timeframe == "All" or artifact.get("timeframe") == selected_timeframe)
    ]

    st.dataframe(_safe_dataframe_rows(_artifact_display_rows(filtered_artifacts)), use_container_width=True, hide_index=True)

    if filtered_artifacts:
        selected_artifact = st.selectbox(
            "Select artifact",
            options=filtered_artifacts,
            format_func=_artifact_label,
            key=f"{key_prefix}_preview_selector",
        )
        selected_path = str(selected_artifact.get("path") or "")
        st.dataframe(
            _safe_dataframe_rows(_artifact_display_rows([selected_artifact])),
            use_container_width=True,
            hide_index=True,
        )
        preview_col, clear_col = st.columns(2)
        with preview_col:
            if st.button("Preview selected artifact", key=f"{key_prefix}_preview_button"):
                st.session_state[f"{key_prefix}_preview_path"] = selected_path
                st.session_state[f"{key_prefix}_download_path"] = None
        with clear_col:
            if st.button("Clear preview", key=f"{key_prefix}_clear_preview_button"):
                st.session_state[f"{key_prefix}_preview_path"] = None
                st.session_state[f"{key_prefix}_download_path"] = None

        if st.session_state.get(f"{key_prefix}_preview_path") == selected_path:
            _render_artifact_preview(selected_artifact, key_prefix, report_dir)
        else:
            st.caption("Preview is lazy to keep Studio responsive. Click Preview selected artifact to render it.")
    else:
        st.info("No artifacts match the current filters.")

    return filtered_artifacts


def _render_summary_report(summary_text: str) -> None:
    """Render summary report text with navigable timeframe sections."""
    marker = re.compile(r"--- TIMEFRAME ANALYSIS:\s*([^-]+?)\s*---")
    matches = list(marker.finditer(summary_text))
    if not matches:
        st.text(summary_text)
        return

    intro = summary_text[: matches[0].start()].strip()
    if intro:
        st.text(intro)

    for index, match in enumerate(matches):
        timeframe = match.group(1).strip()
        section_start = match.end()
        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(summary_text)
        section_text = summary_text[section_start:section_end].strip()
        with st.expander(f"Timeframe Analysis: {timeframe}", expanded=False):
            st.text(section_text)


def _render_overview(result: dict[str, Any] | None) -> None:
    """Render the Overview tab."""
    if not result:
        st.info("Run an analysis or load the latest report to view an overview.")
        st.caption("Reports are loaded from the configured `.marketflow/reports` directory.")
        return

    report_json = result.get("report_json") or {}
    signal = report_json.get("signal") if isinstance(report_json, dict) else {}
    risk = report_json.get("risk_assessment") if isinstance(report_json, dict) else {}

    st.subheader(result.get("ticker") or "Ticker")
    if result.get("output_dir"):
        st.caption(f"Output directory: `{result['output_dir']}`")

    if result.get("error"):
        _render_error_details(result)
        if not report_json:
            return

    col1, col2, col3 = st.columns(3)
    with col1:
        _display_value("Current Price", _format_ui_price(report_json.get("current_price")))
        _display_value("Stop Loss", _format_ui_price(_nested_get(risk, ["stop_loss"])))
    with col2:
        _display_value("Signal Type", _nested_get(signal, ["type"]))
        _display_value("Take Profit", _format_ui_price(_nested_get(risk, ["take_profit"])))
    with col3:
        _display_value("Signal Strength", _nested_get(signal, ["strength"]))
        _display_value("Risk/Reward", _format_ui_number(_nested_get(risk, ["risk_reward_ratio"])))

    summary_text = result.get("summary_text") or result.get("narrative")
    if summary_text:
        st.markdown("#### Summary Preview")
        st.text_area(
            "Summary Preview",
            value=summary_text[:4000],
            height=260,
            label_visibility="collapsed",
        )


def _render_reports(result: dict[str, Any] | None) -> None:
    """Render the Reports tab."""
    report_dir = _report_dir_from_result(
        result,
        "No report directory loaded. Run an analysis or load the latest report first.",
    )
    if not report_dir:
        return

    st.write(f"Report directory: `{report_dir}`")

    summary_text = result.get("summary_text")
    if summary_text:
        st.markdown("#### Summary Report")
        _render_summary_report(summary_text)
    else:
        st.info("No summary report text is available for this report.")

    files = list_report_files(report_dir) or result.get("report_files") or []
    with st.expander("Generated files", expanded=False):
        if files:
            st.dataframe(_safe_dataframe_rows(_report_file_rows(files)), use_container_width=True, hide_index=True)
        else:
            st.info("No generated files found in this directory.")

    _render_generated_artifacts(report_dir, key_prefix="reports_artifacts")

    date_folders = list_report_date_folders()
    with st.expander("Report date / batch folders", expanded=False):
        if date_folders:
            st.dataframe(
                _safe_dataframe_rows([{"Folder": Path(folder).name, "Full Path": folder} for folder in date_folders]),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No report date or batch folders found.")

    report_parent = str(Path(report_dir).parent)
    tickers = list_available_tickers(report_parent)
    with st.expander("Available ticker folders", expanded=False):
        if tickers:
            st.dataframe(_safe_dataframe_rows([{"Ticker": ticker} for ticker in tickers]), use_container_width=True, hide_index=True)
        else:
            st.info("No ticker folders found beside this report.")


def _render_csv_preview(result: dict[str, Any] | None) -> None:
    """Render the CSV Preview tab."""
    report_dir = _report_dir_from_result(
        result,
        "Load a report or run an analysis before previewing CSV files.",
    )
    if not report_dir:
        return

    csv_files = _annotated_csv_files_for_report(report_dir)
    if not csv_files:
        st.info("No annotated CSV files found in this report directory.")
        st.caption("Run Analysis with timeframes that generate Wyckoff annotated exports.")
        return

    selected_csv = _select_annotated_csv(csv_files, "CSV file", "csv_preview_file")
    preview_rows = st.selectbox(
        "Preview rows",
        options=CSV_PREVIEW_ROW_OPTIONS,
        index=2,
        key="csv_preview_rows",
    )

    _render_csv_file_context(selected_csv)

    dataframe = load_csv_preview(selected_csv, nrows=preview_rows)
    if dataframe is None:
        st.error("Could not load this CSV file for preview.")
        return

    st.write(f"Rows in preview: `{len(dataframe)}`")
    st.write(f"Column count: `{len(dataframe.columns)}`")
    st.write("Columns:")
    st.write(", ".join(f"`{column}`" for column in dataframe.columns))

    st.dataframe(dataframe, use_container_width=True)


def _render_charts(result: dict[str, Any] | None) -> None:
    """Render the Charts tab."""
    report_dir = _report_dir_from_result(result, "Run an analysis or load a report first.")
    if not report_dir:
        return

    csv_files = _annotated_csv_files_for_report(report_dir)
    chart_selected_csv: str | None = None
    chart_timeframe: str | None = None
    if csv_files:
        selected_csv = _select_csv_with_default(
            csv_files,
            "Chart CSV file",
            "charts_main_timeframe",
        )
        chart_selected_csv = selected_csv
        chart_rows = st.selectbox(
            "Chart rows",
            options=CHART_ROW_OPTIONS,
            index=1,
            key="chart_rows",
        )

        chart_timeframe = _render_csv_file_context(selected_csv)

        dataframe = load_csv_for_chart(selected_csv, nrows=chart_rows)
        if dataframe is None:
            st.error("Could not load this CSV file for charting.")
        else:
            try:
                title_parts = [Path(selected_csv).stem]
                if chart_timeframe:
                    title_parts.append(chart_timeframe)
                fig = build_basic_wyckoff_candlestick_chart(
                    dataframe,
                    title=" - ".join(title_parts),
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as exc:
                st.error("Could not build chart.")
                with st.expander("Chart error details"):
                    st.write(f"Type: `{type(exc).__name__}`")
                    st.code(str(exc))
    else:
        st.info("No annotated CSV files found for charting.")
        st.caption("Charts use annotated OHLC CSV files generated by MarketFlow reports.")

    st.markdown("#### P&F Sidecar Chart")
    pnf_sidecars = load_pnf_sidecars(report_dir)
    if not pnf_sidecars:
        st.info("No P&F sidecar files found for this report.")

    st.markdown("##### Generate P&F Sidecars")
    if not csv_files:
        st.caption("Annotated CSV files are required before P&F sidecars can be generated.")
    else:
        pnf_default_csv = _default_csv_for_timeframe(csv_files, chart_timeframe, annotated_only=True)
        pnf_csv = _select_csv_with_default(
            csv_files,
            "P&F source CSV",
            "pnf_selected_csv",
            default_csv=pnf_default_csv,
        )
        row_choice = st.selectbox(
            "P&F row limit",
            options=PNF_ROW_OPTIONS,
            index=0,
            key="pnf_generation_rows",
        )
        reversal = st.number_input(
            "P&F reversal",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            key="pnf_generation_reversal",
        )
        box_mode = st.selectbox(
            "P&F box sizing",
            options=["auto", "fixed", "percent", "atr"],
            index=0,
            key="pnf_generation_box_mode",
        )
        box_size = None
        pnf_scale = None
        pnf_scale_value = None
        if box_mode == "fixed":
            box_size = st.number_input(
                "Fixed box size",
                min_value=0.000001,
                value=1.0,
                step=0.1,
                format="%.6f",
                key="pnf_generation_fixed_box_size",
            )
        elif box_mode in {"percent", "atr"}:
            pnf_scale = box_mode
            pnf_scale_value = st.number_input(
                "P&F scale value",
                min_value=0.000001,
                value=0.005 if box_mode == "percent" else 1.0,
                step=0.001,
                format="%.6f",
                key=f"pnf_generation_{box_mode}_scale_value",
            )

        nrows = None if row_choice == "All" else int(row_choice)
        pnf_bulk_csv_files = _wyckoff_annotated_csv_files(csv_files)
        if pnf_bulk_csv_files:
            st.caption(
                f"Bulk P&F generation will process {len(pnf_bulk_csv_files)} "
                "Wyckoff annotated CSV file(s)."
            )
        else:
            st.caption("No *_wyckoff_annotated.csv files are available for bulk P&F generation.")
        st.caption(f"P&F selected source: `{Path(pnf_csv).name}`")
        generate_col1, generate_col2 = st.columns(2)
        generation_results: list[dict[str, Any]] = []
        with generate_col1:
            if st.button("Generate P&F for selected CSV"):
                generation_results = [
                    generate_pnf_for_csv(
                        pnf_csv,
                        box_size=box_size,
                        reversal=int(reversal),
                        nrows=nrows,
                        pnf_scale=pnf_scale,
                        pnf_scale_value=pnf_scale_value,
                    )
                ]
        with generate_col2:
            if st.button(
                "Generate P&F for all Wyckoff annotated CSVs",
                disabled=not bool(pnf_bulk_csv_files),
            ):
                generation_results = generate_pnf_for_csvs(
                    pnf_bulk_csv_files,
                    box_size=box_size,
                    reversal=int(reversal),
                    nrows=nrows,
                    pnf_scale=pnf_scale,
                    pnf_scale_value=pnf_scale_value,
                )

        if generation_results:
            successes = [result for result in generation_results if result.get("success")]
            failures = [result for result in generation_results if not result.get("success")]
            if successes:
                st.success(f"Generated P&F outputs for {len(successes)} CSV file(s).")
            if failures:
                st.warning(f"P&F generation failed for {len(failures)} CSV file(s).")
            st.dataframe(
                _safe_dataframe_rows(_pnf_generation_result_rows(generation_results)),
                use_container_width=True,
                hide_index=True,
            )
            pnf_sidecars = load_pnf_sidecars(report_dir)

    st.markdown("##### Generate Legacy Feature Plots")
    if not csv_files:
        st.caption("Annotated CSV files are required before legacy feature plots can be generated.")
    else:
        legacy_default_csv = _default_csv_for_timeframe(csv_files, chart_timeframe) or chart_selected_csv
        legacy_csv = _select_csv_with_default(
            csv_files,
            "Legacy plot source CSV",
            "legacy_plot_selected_csv",
            default_csv=legacy_default_csv,
        )
        legacy_row_choice = st.selectbox(
            "Legacy plot row limit",
            options=LEGACY_PLOT_ROW_OPTIONS,
            index=0,
            key="legacy_plot_generation_rows",
        )
        legacy_col1, legacy_col2, legacy_col3, legacy_col4, legacy_col5 = st.columns(5)
        with legacy_col1:
            include_legacy_pnf = st.checkbox("P&F", value=True, key="legacy_include_pnf")
        with legacy_col2:
            include_price_volume = st.checkbox("Price-volume", value=True, key="legacy_include_price_volume")
        with legacy_col3:
            include_volume_profile = st.checkbox("Volume profile", value=True, key="legacy_include_volume_profile")
        with legacy_col4:
            include_volume_distribution = st.checkbox(
                "Volume distribution",
                value=True,
                key="legacy_include_volume_distribution",
            )
        with legacy_col5:
            include_spread = st.checkbox("Spread/features", value=True, key="legacy_include_spread")

        legacy_nrows = None if legacy_row_choice == "All" else int(legacy_row_choice)
        st.caption(f"Legacy plot selected source: `{Path(legacy_csv).name}`")
        if st.button("Generate legacy plots for selected CSV"):
            legacy_result = generate_legacy_feature_plots_for_csv(
                legacy_csv,
                nrows=legacy_nrows,
                include_pnf=include_legacy_pnf,
                include_price_volume=include_price_volume,
                include_volume_profile=include_volume_profile,
                include_volume_distribution=include_volume_distribution,
                include_spread=include_spread,
            )
            if legacy_result.get("success"):
                generated_count = len(legacy_result.get("generated_paths") or [])
                st.success(f"Generated {generated_count} legacy plot artifact(s).")
            else:
                st.warning(legacy_result.get("error") or "Legacy plot generation failed.")
                if legacy_result.get("traceback"):
                    with st.expander("Legacy plot error details"):
                        st.code(legacy_result["traceback"], language="python")

            generated_rows = _legacy_generation_rows(legacy_result)
            if generated_rows:
                st.dataframe(_safe_dataframe_rows(generated_rows), use_container_width=True, hide_index=True)
            pnf_sidecars = load_pnf_sidecars(report_dir)

    st.markdown("##### Price-Volume Eigen Analyzer")
    if not csv_files:
        st.caption("Annotated CSV files are required before Price-Volume Eigen features can be generated.")
    else:
        eigen_default_csv = _default_csv_for_timeframe(csv_files, chart_timeframe) or chart_selected_csv
        eigen_csv = _select_csv_with_default(
            csv_files,
            "Eigen analyzer source CSV",
            "eigen_source_csv",
            default_csv=eigen_default_csv,
        )
        eigen_col1, eigen_col2, eigen_col3, eigen_col4 = st.columns(4)
        with eigen_col1:
            eigen_window = st.number_input(
                "Eigen window",
                min_value=5,
                max_value=250,
                value=40,
                step=5,
                key="eigen_generation_window",
            )
        with eigen_col2:
            eigen_result_mode = st.selectbox(
                "Result mode",
                options=["spread_atr", "close_return"],
                index=0,
                key="eigen_generation_result_mode",
            )
        with eigen_col3:
            eigen_effort_mode = st.selectbox(
                "Effort mode",
                options=["volume_ratio", "volrel20", "volume_ma"],
                index=0,
                key="eigen_generation_effort_mode",
            )
        with eigen_col4:
            eigen_chart_rows = st.number_input(
                "Eigen chart rows",
                min_value=50,
                max_value=5000,
                value=500,
                step=50,
                key="eigen_chart_rows",
            )

        st.caption(f"Eigen Analyzer selected source: `{Path(eigen_csv).name}`")
        if st.button("Run Price-Volume Eigen Analyzer"):
            eigen_result = run_price_volume_eigen_for_csv(
                eigen_csv,
                window=int(eigen_window),
                result_mode=eigen_result_mode,
                effort_mode=eigen_effort_mode,
            )
            if eigen_result.get("success"):
                st.success("Price-Volume Eigen features generated.")
                st.caption(f"Source: `{Path(eigen_csv).name}`")
                st.caption(f"Output: `{eigen_result.get('output_path')}`")
                latest = eigen_result.get("latest") if isinstance(eigen_result.get("latest"), dict) else {}
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                with metric_col1:
                    _display_optional_metric("Rows", eigen_result.get("rows"))
                    _display_optional_metric("Divergences", eigen_result.get("divergence_count"))
                with metric_col2:
                    _display_optional_metric("Latest Coupling", _format_number(latest.get("pv_eigen_coupling"), decimals=4))
                    _display_optional_metric("Latest Residual", _format_number(latest.get("pv_eigen_residual"), decimals=4))
                with metric_col3:
                    _display_optional_metric("Latest Harmony", latest.get("pv_eigen_harmony"))
                    _display_optional_metric("Latest Divergence", latest.get("pv_effort_result_divergence"))
                with metric_col4:
                    _display_optional_metric("Latest Status", latest.get("pv_eigen_status"))
                    _display_optional_metric("Window", eigen_result.get("window"))

                eigen_output_path = str(eigen_result.get("output_path") or "")
                _render_eigen_chart_for_csv(
                    eigen_output_path,
                    int(eigen_chart_rows),
                    title=f"{Path(eigen_output_path).stem} Eigen Preview",
                )

                preview = load_csv_preview(eigen_output_path, nrows=200)
                preview_rows = _eigen_preview_rows(preview)
                if preview_rows:
                    st.dataframe(_safe_dataframe_rows(preview_rows), use_container_width=True, hide_index=True)
            else:
                st.warning(eigen_result.get("error") or "Price-Volume Eigen Analyzer failed.")
                if eigen_result.get("traceback"):
                    with st.expander("Eigen analyzer error details"):
                        st.code(eigen_result["traceback"], language="python")

        eigen_artifacts = [
            artifact
            for artifact in list_report_artifacts(report_dir)
            if artifact.get("kind") == "price_volume_eigen_csv"
        ]
        if eigen_artifacts:
            eigen_artifact_default = None
            if chart_timeframe:
                for artifact in eigen_artifacts:
                    artifact_path = str(artifact.get("path") or artifact.get("name") or "")
                    if infer_timeframe_from_csv_name(artifact_path) == chart_timeframe:
                        eigen_artifact_default = artifact
                        break
            if st.session_state.get("eigen_preview_csv") not in eigen_artifacts:
                st.session_state.eigen_preview_csv = eigen_artifact_default or eigen_artifacts[0]
            selected_eigen_artifact = st.selectbox(
                "Existing Price-Volume Eigen CSV",
                options=eigen_artifacts,
                format_func=lambda artifact: artifact.get("name") or Path(str(artifact.get("path") or "")).name,
                key="eigen_preview_csv",
            )
            st.caption(
                "Eigen Preview selected file: "
                f"`{selected_eigen_artifact.get('name') or Path(str(selected_eigen_artifact.get('path') or '')).name}`"
            )
            if st.button("Preview Eigen Chart"):
                _render_eigen_chart_for_csv(
                    str(selected_eigen_artifact.get("path") or ""),
                    int(eigen_chart_rows),
                    title=f"{selected_eigen_artifact.get('name') or 'Price-Volume Eigen'} Preview",
                )

        st.markdown("###### Eigen Window Comparison")
        comparison_windows_text = st.text_input(
            "Comparison windows",
            value="20,40,60",
            key="eigen_comparison_windows",
        )
        comparison_windows = _parse_window_list(comparison_windows_text)
        st.caption(f"Parsed windows: `{', '.join(str(window) for window in comparison_windows)}`")
        if st.button("Compare Eigen Windows"):
            comparison_result = compare_price_volume_eigen_windows(
                eigen_csv,
                windows=comparison_windows,
                result_mode=eigen_result_mode,
                effort_mode=eigen_effort_mode,
            )
            if comparison_result.get("success"):
                st.session_state.latest_eigen_window_comparison = comparison_result
                st.session_state.latest_eigen_source_csv = str(eigen_csv)
                st.dataframe(
                    _safe_dataframe_rows(comparison_result.get("comparison") or []),
                    use_container_width=True,
                    hide_index=True,
                )
                interpretation = comparison_result.get("interpretation") if isinstance(comparison_result.get("interpretation"), dict) else {}
                observation = interpretation.get("broad_observation")
                if observation:
                    st.info(str(observation))
                for note in interpretation.get("notes") or []:
                    st.caption(str(note))
            else:
                st.warning(comparison_result.get("error") or "Eigen window comparison failed.")
                if comparison_result.get("traceback"):
                    with st.expander("Eigen comparison error details"):
                        st.code(comparison_result["traceback"], language="python")

        st.markdown("###### Eigen-Wyckoff Proximity Review")
        st.caption(
            "This diagnostic compares Eigen attention rows with nearby Wyckoff labels. "
            "It does not create trading signals."
        )
        proximity_col1, proximity_col2, proximity_col3, proximity_col4 = st.columns(4)
        with proximity_col1:
            proximity_window = st.number_input(
                "Proximity window",
                min_value=5,
                max_value=250,
                value=20,
                step=5,
                key="eigen_wyckoff_window",
            )
        with proximity_col2:
            proximity_residual_threshold = st.number_input(
                "Residual threshold",
                min_value=0.0,
                max_value=25.0,
                value=2.0,
                step=0.25,
                key="eigen_wyckoff_residual_threshold",
            )
        with proximity_col3:
            proximity_bars = st.number_input(
                "Proximity bars",
                min_value=0,
                max_value=50,
                value=3,
                step=1,
                key="eigen_wyckoff_proximity_bars",
            )
        with proximity_col4:
            proximity_max_rows = st.number_input(
                "Review rows",
                min_value=1,
                max_value=500,
                value=50,
                step=10,
                key="eigen_wyckoff_max_rows",
            )

        if st.button("Review Eigen-Wyckoff Proximity"):
            proximity_result = review_eigen_wyckoff_proximity(
                eigen_csv,
                window=int(proximity_window),
                result_mode=eigen_result_mode,
                effort_mode=eigen_effort_mode,
                residual_threshold=float(proximity_residual_threshold),
                proximity_bars=int(proximity_bars),
                max_rows=int(proximity_max_rows),
            )
            if proximity_result.get("success"):
                st.session_state.latest_eigen_wyckoff_proximity = proximity_result
                st.session_state.latest_eigen_source_csv = str(eigen_csv)
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    _display_optional_metric("Attention rows", proximity_result.get("attention_count"))
                with metric_col2:
                    _display_optional_metric("Matched events", proximity_result.get("matched_event_count"))
                with metric_col3:
                    _display_optional_metric(
                        "Eigen-only rows",
                        proximity_result.get("unmatched_attention_count"),
                    )

                summary = proximity_result.get("summary") if isinstance(proximity_result.get("summary"), dict) else {}
                observation = summary.get("broad_observation")
                if observation:
                    st.info(str(observation))

                review_rows = proximity_result.get("review") or []
                if review_rows:
                    st.dataframe(_safe_dataframe_rows(review_rows), use_container_width=True, hide_index=True)
                else:
                    st.info("No Eigen attention rows found with the current threshold/window.")

                for note in summary.get("notes") or []:
                    st.caption(str(note))
            else:
                st.warning(proximity_result.get("error") or "Eigen-Wyckoff proximity review failed.")
                if proximity_result.get("traceback"):
                    with st.expander("Eigen-Wyckoff proximity error details"):
                        st.code(proximity_result["traceback"], language="python")

        st.markdown("###### Eigen Review Summary Artifact")
        latest_source_csv = st.session_state.get("latest_eigen_source_csv")
        latest_window_comparison = st.session_state.get("latest_eigen_window_comparison")
        latest_proximity_review = st.session_state.get("latest_eigen_wyckoff_proximity")
        has_window_comparison = isinstance(latest_window_comparison, dict) and latest_window_comparison.get("success")
        has_proximity_review = isinstance(latest_proximity_review, dict) and latest_proximity_review.get("success")
        summary_status_rows = [
            {
                "item": "Source CSV",
                "status": "available" if latest_source_csv else "missing",
                "detail": Path(str(latest_source_csv)).name if latest_source_csv else "",
            },
            {
                "item": "Window comparison",
                "status": "available" if has_window_comparison else "missing",
                "detail": ", ".join(str(window) for window in (latest_window_comparison or {}).get("windows", []))
                if has_window_comparison
                else "",
            },
            {
                "item": "Proximity review",
                "status": "available" if has_proximity_review else "missing",
                "detail": f"{(latest_proximity_review or {}).get('attention_count')} attention rows"
                if has_proximity_review
                else "",
            },
        ]
        st.dataframe(_safe_dataframe_rows(summary_status_rows), use_container_width=True, hide_index=True)
        if not has_window_comparison and not has_proximity_review:
            st.info("Run Eigen Window Comparison and/or Eigen-Wyckoff Proximity Review first.")
        else:
            summary_source_csv = str(latest_source_csv or eigen_csv)
            eigen_summary_markdown = _build_eigen_review_summary_markdown(
                source_csv=summary_source_csv,
                window_comparison=latest_window_comparison if has_window_comparison else None,
                proximity_review=latest_proximity_review if has_proximity_review else None,
            )
            eigen_summary_filename = _eigen_review_summary_filename(summary_source_csv)
            st.download_button(
                "Download Eigen Review Summary",
                data=eigen_summary_markdown,
                file_name=eigen_summary_filename,
                mime="text/markdown",
                key="download_eigen_review_summary",
            )
            if st.button("Save Eigen Review Summary to report folder"):
                if not report_dir:
                    st.warning("No report directory is available. Use Download instead.")
                else:
                    try:
                        save_path = Path(report_dir) / eigen_summary_filename
                        if save_path.exists():
                            stem = save_path.stem
                            suffix = save_path.suffix
                            counter = 2
                            while save_path.exists():
                                save_path = Path(report_dir) / f"{stem}_{counter}{suffix}"
                                counter += 1
                        save_path.write_text(eigen_summary_markdown, encoding="utf-8")
                        st.success(f"Saved Eigen review summary to `{save_path}`")
                        st.caption("Refresh Generated Artifacts to see this Eigen review summary.")
                    except Exception as exc:
                        st.error(f"Could not save Eigen review summary: {exc}")

    if pnf_sidecars:
        st.caption(
            "The reconstructed P&F chart is built from sidecar JSON and may not include every visual "
            "feature from the saved HTML plot. Use Generated Artifacts to preview the original saved P&F HTML."
        )
        st.markdown("##### P&F Sidecar Source Review")
        source_filter = st.selectbox(
            "P&F sidecar source filter",
            options=["all", "wyckoff_annotated", "raw_csv", "unknown"],
            key="pnf_sidecar_source_filter",
        )
        displayed_pnf_sidecars = [
            sidecar
            for sidecar in pnf_sidecars
            if source_filter == "all"
            or (sidecar.get("source_type") or classify_pnf_sidecar_source(sidecar)) == source_filter
        ]
        st.dataframe(
            _safe_dataframe_rows(_pnf_source_review_rows(displayed_pnf_sidecars)),
            use_container_width=True,
            hide_index=True,
        )
        if not displayed_pnf_sidecars:
            st.info("No P&F sidecars match the selected source filter.")
        else:
            selected_sidecar = st.selectbox(
                "P&F sidecar",
                options=displayed_pnf_sidecars,
                format_func=_pnf_sidecar_label,
                key="pnf_sidecar_chart_file",
            )
            st.dataframe(
                _safe_dataframe_rows([_pnf_metadata_row(selected_sidecar)]),
                use_container_width=True,
                hide_index=True,
            )
            try:
                fig = build_pnf_chart_from_sidecar(selected_sidecar)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as exc:
                st.info("Could not render this P&F sidecar as a chart.")
                with st.expander("P&F chart details"):
                    st.write(f"Type: `{type(exc).__name__}`")
                    st.code(str(exc))

    with st.expander("Generated Artifacts", expanded=False):
        _render_generated_artifacts(report_dir, key_prefix="charts_artifacts")


def _default_strategy_ticker_text(result: dict[str, Any] | None) -> str:
    """Return the currently loaded ticker as the strategy ticker default."""
    if result and result.get("ticker"):
        return str(result["ticker"])
    return "AAPL"


def _render_strategy_error(strategy_result: dict[str, Any]) -> None:
    """Render strategy ranking errors with traceback hidden by default."""
    error_type = strategy_result.get("error_type")
    error_message = strategy_result.get("error") or "Strategy ranking failed."
    if error_type:
        st.error(f"{error_type}: {error_message}")
    else:
        st.error(error_message)

    if strategy_result.get("traceback"):
        with st.expander("Strategy error details"):
            st.code(strategy_result["traceback"], language="python")


def _strategy_diagnostics_dataframe(diagnostics: dict[str, Any]) -> Any:
    """Return a compact ticker-check table for strategy diagnostics."""
    ticker_checks = diagnostics.get("ticker_checks") or {}
    rows = []
    for ticker, check in ticker_checks.items():
        rows.append(
            {
                "ticker": ticker,
                "ticker_folder_found": check.get("ticker_folder_found", False),
                "matching_csv_count": len(check.get("matching_timeframe_csvs") or []),
                "csv_count": len(check.get("csv_candidates") or []),
                "ticker_folder": check.get("ticker_folder"),
            }
        )
    return rows


def _render_strategy_diagnostics(strategy_result: dict[str, Any]) -> None:
    """Render strategy diagnostics in a collapsed expander."""
    diagnostics = strategy_result.get("diagnostics") or {}
    if not diagnostics:
        return

    with st.expander("Strategy diagnostics"):
        st.write(f"Report root: `{diagnostics.get('report_root')}`")
        st.write(f"Report root exists: `{diagnostics.get('report_root_exists')}`")
        batch_run_folders = diagnostics.get("batch_run_folders") or []
        ignored_batch_like = diagnostics.get("ignored_batch_like_folders") or []
        st.write(f"Valid batch run folders: `{len(batch_run_folders)}`")
        latest_batch = diagnostics.get("latest_batch_folder")
        if latest_batch:
            st.write(f"Latest valid batch folder: `{latest_batch}`")
        else:
            st.write("Latest valid batch folder: none found")
        st.write(
            f"Latest valid batch folder exists: `{diagnostics.get('latest_batch_folder_exists')}`"
        )
        if ignored_batch_like:
            st.write(f"Ignored batch-like folders: `{len(ignored_batch_like)}`")
            st.caption("Folders such as `batch_csv_*` are ignored as real batch runs.")
            for folder in ignored_batch_like[:10]:
                st.write(f"- `{folder}`")
        st.write(f"Requested tickers: `{', '.join(diagnostics.get('requested_tickers') or [])}`")
        st.write(f"Selected timeframe: `{diagnostics.get('requested_timeframe')}`")

        filters = diagnostics.get("filters") or {}
        st.write("Filters")
        st.json(filters)

        notes = diagnostics.get("notes") or []
        if notes:
            st.write("Notes")
            for note in notes:
                st.write(f"- {note}")

        ticker_rows = _strategy_diagnostics_dataframe(diagnostics)
        if ticker_rows:
            st.write("Ticker checks")
            st.dataframe(_safe_dataframe_rows(ticker_rows), use_container_width=True)

        st.write("Raw diagnostics")
        st.json(diagnostics)


def _current_strategy_candidate_for_backtest() -> dict[str, Any] | None:
    """Return the currently selected Strategy Ranking candidate for snapshot saving."""
    candidate = st.session_state.get("selected_strategy_candidate")
    if isinstance(candidate, dict):
        return candidate
    candidate = st.session_state.get("latest_strategy_candidate")
    if isinstance(candidate, dict):
        return candidate
    return None


def _report_dir_for_backtest_snapshot(result: dict[str, Any] | None) -> str | None:
    """Return the loaded report directory for backtest candidate artifact saving."""
    if not result or not result.get("output_dir"):
        return None
    report_dir = str(result.get("output_dir"))
    report_path = Path(report_dir)
    if report_path.exists() and report_path.is_dir():
        return report_dir
    return None


def _backtest_candidate_csv_artifacts(report_dir: str | None) -> list[dict[str, Any]]:
    """Return backtest candidate snapshot CSV artifacts for the selected report."""
    if not report_dir:
        return []
    artifacts = [
        artifact
        for artifact in list_report_artifacts(report_dir)
        if artifact.get("kind") == "backtest_candidates_csv"
    ]
    return sorted(
        artifacts,
        key=lambda artifact: (
            str(artifact.get("modified") or ""),
            str(artifact.get("name") or artifact.get("path") or ""),
        ),
        reverse=True,
    )


def _backtest_result_csv_artifacts(report_dir: str | None) -> list[dict[str, Any]]:
    """Return backtest result CSV artifacts for the selected report."""
    if not report_dir:
        return []
    artifacts = [
        artifact
        for artifact in list_report_artifacts(report_dir)
        if artifact.get("kind") == "backtest_results_csv"
    ]
    return sorted(
        artifacts,
        key=lambda artifact: (
            str(artifact.get("modified") or ""),
            str(artifact.get("name") or artifact.get("path") or ""),
        ),
        reverse=True,
    )


def _monte_carlo_summary_json_artifacts(report_dir: str | None) -> list[dict[str, Any]]:
    """Return Monte Carlo summary JSON artifacts for the selected report."""
    if not report_dir:
        return []
    artifacts = [
        artifact
        for artifact in list_report_artifacts(report_dir)
        if artifact.get("kind") == "mc_summary_json"
        or str(artifact.get("name") or "").lower().endswith("_mc_summary.json")
    ]
    return sorted(
        artifacts,
        key=lambda artifact: (
            str(artifact.get("modified") or ""),
            str(artifact.get("name") or artifact.get("path") or ""),
        ),
        reverse=True,
    )


def _default_backtest_candidate_csv_index(artifacts: list[dict[str, Any]]) -> int:
    """Return the default selected candidate snapshot artifact index."""
    if not artifacts:
        return 0
    latest = st.session_state.get("latest_backtest_candidate_csv")
    latest_path = str(latest.get("path") or "") if isinstance(latest, dict) else ""
    if latest_path:
        for index, artifact in enumerate(artifacts):
            if str(artifact.get("path") or "") == latest_path:
                return index
    return 0


def _backtest_candidate_preview_rows(rows: list[dict[str, Any]], max_rows: int = 5) -> list[dict[str, Any]]:
    """Return compact candidate snapshot rows for preview."""
    fields = [
        "ticker",
        "timeframe",
        "source_csv",
        "signal_timestamp",
        "signal_row_index",
        "entry",
        "stop_loss",
        "take_profit",
        "validation_status",
        "snapshot_success",
    ]
    return [{field: row.get(field) for field in fields} for row in rows[:max_rows] if isinstance(row, dict)]


def _backtest_outcome_summary_rows(evaluation_result: dict[str, Any]) -> list[dict[str, Any]]:
    """Return compact rows summarizing a backtest outcome evaluation result."""
    evaluation = evaluation_result.get("evaluation") if isinstance(evaluation_result.get("evaluation"), dict) else {}
    write_result = evaluation_result.get("write_result") if isinstance(evaluation_result.get("write_result"), dict) else {}
    return [
        {"item": "Success", "value": evaluation_result.get("success")},
        {"item": "Filename", "value": evaluation_result.get("filename") or write_result.get("filename")},
        {"item": "Path", "value": evaluation_result.get("path") or write_result.get("path")},
        {"item": "Candidate count", "value": evaluation.get("count")},
        {"item": "Evaluated count", "value": evaluation.get("evaluated_count")},
        {"item": "Success count", "value": evaluation.get("success_count")},
        {"item": "Invalid count", "value": evaluation.get("invalid_count")},
        {"item": "Skipped count", "value": evaluation.get("skipped_count")},
    ]


def _backtest_result_preview_rows(rows: list[dict[str, Any]], max_rows: int = 10) -> list[dict[str, Any]]:
    """Return compact backtest result rows for preview."""
    fields = [
        "ticker",
        "timeframe",
        "outcome",
        "realized_R",
        "bars_to_hit",
        "tie_break_policy",
        "horizon_bars",
        "backtest_success",
        "outcome_error",
    ]
    return [{field: row.get(field) for field in fields} for row in rows[:max_rows] if isinstance(row, dict)]


def _backtest_calibration_filename_context(result: dict[str, Any] | None) -> tuple[str | None, str | None]:
    """Return best-effort ticker/timeframe filename context for calibration summary artifacts."""
    candidate = _current_strategy_candidate_for_backtest()
    ticker = candidate.get("ticker") if isinstance(candidate, dict) else None
    timeframe = None
    if isinstance(candidate, dict):
        timeframe = candidate.get("tf") or candidate.get("timeframe")
    if not ticker and isinstance(result, dict):
        ticker = result.get("ticker")
    return ticker, timeframe


def _backtest_calibration_status_rows(
    summary_result: dict[str, Any],
    artifact_result: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return compact display rows for a calibration summary result."""
    artifact_result = artifact_result if isinstance(artifact_result, dict) else {}
    return [
        {"item": "Summary success", "value": summary_result.get("success")},
        {"item": "File count", "value": summary_result.get("file_count")},
        {"item": "Read count", "value": summary_result.get("read_count")},
        {"item": "Row count", "value": summary_result.get("count")},
        {"item": "Source result files", "value": len(summary_result.get("source_result_files") or [])},
        {"item": "Saved markdown", "value": artifact_result.get("success")},
        {"item": "Markdown filename", "value": artifact_result.get("filename")},
        {"item": "Markdown path", "value": artifact_result.get("path")},
    ]


def _render_backtest_calibration_summary_tables(summary_result: dict[str, Any]) -> None:
    """Render calibration summary tables from a service result."""
    st.write("Global Summary")
    summary_rows = summary_result.get("summary_rows") or []
    if summary_rows:
        st.dataframe(_safe_dataframe_rows(summary_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No global summary rows are available.")

    grouped_rows = summary_result.get("grouped_summary_rows") or []
    if grouped_rows:
        with st.expander(f"Grouped Summary ({len(grouped_rows)} rows)", expanded=len(grouped_rows) <= 10):
            st.dataframe(_safe_dataframe_rows(grouped_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No grouped summary rows are available.")

    invalid_reason_rows = summary_result.get("invalid_reason_rows") or []
    st.write("Invalid Row Review")
    if invalid_reason_rows:
        st.dataframe(_safe_dataframe_rows(invalid_reason_rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No invalid rows were summarized.")


def _monte_carlo_calibration_status_rows(
    summary_result: dict[str, Any],
    artifact_result: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return compact display rows for a Monte Carlo calibration summary result."""
    artifact_result = artifact_result if isinstance(artifact_result, dict) else {}
    summary = summary_result.get("summary") if isinstance(summary_result.get("summary"), dict) else {}
    return [
        {"item": "Summary success", "value": summary_result.get("success")},
        {"item": "Forecast files", "value": summary_result.get("forecast_file_count")},
        {"item": "Actual files", "value": summary_result.get("actual_file_count")},
        {"item": "Forecast rows", "value": len(summary_result.get("forecast_rows") or [])},
        {"item": "Actual rows", "value": len(summary_result.get("actual_rows") or [])},
        {"item": "Joined rows", "value": summary.get("joined_count", len(summary_result.get("join_rows") or []))},
        {"item": "Scoreable rows", "value": summary.get("scoreable_count")},
        {"item": "Not-yet-mature rows", "value": summary.get("not_yet_mature_count")},
        {"item": "Horizon mismatch rows", "value": summary.get("horizon_mismatch_count")},
        {"item": "Unmatched forecasts", "value": len(summary_result.get("unmatched_forecasts") or [])},
        {"item": "Unmatched outcomes", "value": len(summary_result.get("unmatched_outcomes") or [])},
        {"item": "Saved markdown", "value": artifact_result.get("success")},
        {"item": "Markdown filename", "value": artifact_result.get("filename")},
        {"item": "Markdown path", "value": artifact_result.get("path")},
    ]


def _render_monte_carlo_calibration_summary_tables(summary_result: dict[str, Any]) -> None:
    """Render Monte Carlo forecast calibration summary tables from a service result."""
    st.write("Calibration Summary")
    summary_rows = summary_result.get("summary_rows") or []
    if summary_rows:
        st.dataframe(_safe_dataframe_rows(summary_rows), use_container_width=True, hide_index=True)
    else:
        summary = summary_result.get("summary") if isinstance(summary_result.get("summary"), dict) else {}
        if summary:
            st.dataframe(_safe_dataframe_rows([summary]), use_container_width=True, hide_index=True)
        else:
            st.info("No calibration summary rows are available.")

    grouped_rows = summary_result.get("grouped_summary_rows") or []
    with st.expander(f"Grouped Summary ({len(grouped_rows)} rows)", expanded=False):
        if grouped_rows:
            st.dataframe(_safe_dataframe_rows(grouped_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No grouped summary rows are available.")

    join_rows = summary_result.get("join_rows") or []
    with st.expander(f"Join Rows ({len(join_rows)} rows)", expanded=bool(join_rows) and len(join_rows) <= 10):
        if join_rows:
            st.dataframe(_safe_dataframe_rows(join_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No joined forecast-vs-actual rows are available.")

    unmatched_forecasts = summary_result.get("unmatched_forecasts") or []
    if unmatched_forecasts:
        with st.expander(f"Unmatched Forecasts ({len(unmatched_forecasts)} rows)", expanded=True):
            st.dataframe(_safe_dataframe_rows(unmatched_forecasts), use_container_width=True, hide_index=True)

    unmatched_outcomes = summary_result.get("unmatched_outcomes") or []
    if unmatched_outcomes:
        with st.expander(f"Unmatched Outcomes ({len(unmatched_outcomes)} rows)", expanded=True):
            st.dataframe(_safe_dataframe_rows(unmatched_outcomes), use_container_width=True, hide_index=True)


def _render_monte_carlo_forecast_calibration_summary_section(result: dict[str, Any] | None) -> None:
    """Render Monte Carlo forecast-vs-actual calibration summary controls."""
    st.markdown("#### Monte Carlo Forecast Calibration Summary")
    st.caption(
        "Join enriched Monte Carlo forecast summaries with deterministic Backtest Outcome Result CSVs "
        "to review forecast-vs-actual calibration. This is research/calibration only and does not "
        "create trade signals."
    )
    st.info(
        "Reads saved `*_mc_summary.json` and `backtest_results_csv` artifacts. Does not rerun Monte Carlo, "
        "does not rerun backtests, and does not optimize parameters. Rows with no future bars are not "
        "forecast failures. Horizon mismatches are not scoreable. Small samples should not be overinterpreted."
    )

    report_dir = _report_dir_for_backtest_snapshot(result)
    if not report_dir:
        st.warning("No report folder is available for Monte Carlo Forecast Calibration Summary.")
        return

    forecast_artifacts = _monte_carlo_summary_json_artifacts(report_dir)
    if not forecast_artifacts:
        st.info("No Monte Carlo summary JSON artifacts were found. Run Monte Carlo for a selected candidate first.")
        return

    actual_artifacts = _backtest_result_csv_artifacts(report_dir)
    if not actual_artifacts:
        st.info("No backtest result CSV artifacts were found. Run Backtest Outcome Evaluation first.")
        return

    forecast_rows = [
        {
            "name": artifact.get("name"),
            "kind": artifact.get("kind"),
            "timeframe": artifact.get("timeframe"),
            "modified": artifact.get("modified"),
            "path": artifact.get("path"),
        }
        for artifact in forecast_artifacts
    ]
    actual_rows = [
        {
            "name": artifact.get("name"),
            "kind": artifact.get("kind"),
            "timeframe": artifact.get("timeframe"),
            "modified": artifact.get("modified"),
            "path": artifact.get("path"),
        }
        for artifact in actual_artifacts
    ]

    st.write(f"Available Monte Carlo summary JSON artifacts: `{len(forecast_rows)}`")
    st.dataframe(_safe_dataframe_rows(forecast_rows), use_container_width=True, hide_index=True)
    st.write(f"Available backtest result CSV artifacts: `{len(actual_rows)}`")
    st.dataframe(_safe_dataframe_rows(actual_rows), use_container_width=True, hide_index=True)
    st.caption("Expected output: `monte_carlo_calibration_summary_md`")

    save_markdown = st.checkbox(
        "Save markdown Monte Carlo calibration summary",
        value=True,
        key="monte_carlo_calibration_save_markdown",
    )

    if st.button("Summarize Monte Carlo Forecast Calibration"):
        try:
            summary_result = summarize_monte_carlo_calibration_folder(report_dir)
        except Exception as exc:
            summary_result = {
                "success": False,
                "report_dir": report_dir,
                "forecast_file_count": len(forecast_artifacts),
                "actual_file_count": len(actual_artifacts),
                "forecast_rows": [],
                "actual_rows": [],
                "join_rows": [],
                "unmatched_forecasts": [],
                "unmatched_outcomes": [],
                "summary": {},
                "summary_rows": [],
                "grouped_summary_rows": [],
                "warnings": [],
                "errors": [f"{type(exc).__name__}: {exc}"],
            }

        st.session_state["latest_monte_carlo_calibration_summary"] = summary_result
        st.session_state["latest_monte_carlo_calibration_summary_artifact"] = None
        artifact_result = None
        if save_markdown and summary_result.get("success"):
            ticker, timeframe = _backtest_calibration_filename_context(result)
            try:
                artifact_result = summarize_folder_to_monte_carlo_calibration_markdown(
                    report_dir,
                    ticker=ticker,
                    timeframe=timeframe,
                )
            except Exception as exc:
                artifact_result = {
                    "success": False,
                    "path": None,
                    "filename": None,
                    "errors": [f"{type(exc).__name__}: {exc}"],
                    "warnings": [],
                }
            st.session_state["latest_monte_carlo_calibration_summary_artifact"] = artifact_result

        if artifact_result is not None and artifact_result.get("success"):
            st.success(f"Saved Monte Carlo Forecast Calibration Summary: `{artifact_result.get('path')}`")
            st.caption("Saved file appears in Generated Artifacts as monte_carlo_calibration_summary_md.")
            st.caption(
                "Refresh or revisit Generated Artifacts to preview the monte_carlo_calibration_summary_md file."
            )
        elif artifact_result is not None and not artifact_result.get("success"):
            st.error("Could not save Monte Carlo Forecast Calibration Summary markdown.")

    latest_summary = st.session_state.get("latest_monte_carlo_calibration_summary")
    latest_artifact = st.session_state.get("latest_monte_carlo_calibration_summary_artifact")

    if isinstance(latest_summary, dict):
        if latest_summary.get("success"):
            st.success("Monte Carlo Forecast Calibration Summary is available.")
        else:
            st.warning("Monte Carlo Forecast Calibration Summary did not complete successfully.")

        st.dataframe(
            _safe_dataframe_rows(_monte_carlo_calibration_status_rows(latest_summary, latest_artifact)),
            use_container_width=True,
            hide_index=True,
        )

        warnings = latest_summary.get("warnings") or []
        errors = latest_summary.get("errors") or []
        if warnings:
            st.info("Warnings: " + "; ".join(str(warning) for warning in warnings))
        if errors:
            st.warning("Errors: " + "; ".join(str(error) for error in errors))

        if isinstance(latest_artifact, dict):
            artifact_errors = latest_artifact.get("errors") or []
            artifact_warnings = latest_artifact.get("warnings") or []
            if latest_artifact.get("path"):
                st.caption(f"Last saved Monte Carlo calibration artifact: `{latest_artifact.get('path')}`")
            if artifact_warnings:
                st.info("Artifact warnings: " + "; ".join(str(warning) for warning in artifact_warnings))
            if artifact_errors:
                st.warning("Artifact errors: " + "; ".join(str(error) for error in artifact_errors))

        _render_monte_carlo_calibration_summary_tables(latest_summary)


DATA_SUFFICIENCY_ROW_COLUMNS = [
    "ticker",
    "timeframe",
    "source_csv_name",
    "rows_available",
    "first_timestamp",
    "last_timestamp",
    "configured_period",
    "eigen_window",
    "monte_carlo_horizon",
    "backtest_horizon",
    "minimum_rows_required",
    "data_sufficiency_status",
    "eigen_sufficiency_status",
    "monte_carlo_sufficiency_status",
    "backtest_sufficiency_status",
    "calibration_sufficiency_status",
    "noise_warning",
    "provider_limit_warning",
]


def _data_sufficiency_status_rows(
    sufficiency_result: dict[str, Any],
    artifact_result: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return compact display rows for a Data Horizon / Parameter Sufficiency result."""
    artifact_result = artifact_result if isinstance(artifact_result, dict) else {}
    summary = sufficiency_result.get("summary") if isinstance(sufficiency_result.get("summary"), dict) else {}
    return [
        {"item": "Summary success", "value": sufficiency_result.get("success")},
        {"item": "CSV files", "value": sufficiency_result.get("csv_file_count")},
        {"item": "Sufficient", "value": summary.get("sufficient_count")},
        {"item": "Limited", "value": summary.get("limited_count")},
        {"item": "Insufficient", "value": summary.get("insufficient_count")},
        {"item": "Provider limited", "value": summary.get("provider_limited_count")},
        {"item": "Not yet mature", "value": summary.get("not_yet_mature_count")},
        {"item": "Unknown", "value": summary.get("unknown_count")},
        {"item": "Noise warnings", "value": summary.get("noise_warning_count")},
        {"item": "Provider-limit warnings", "value": summary.get("provider_limit_warning_count")},
        {"item": "Minimum rows required max", "value": summary.get("minimum_rows_required_max")},
        {"item": "Rows available min", "value": summary.get("rows_available_min")},
        {"item": "Rows available max", "value": summary.get("rows_available_max")},
        {"item": "Saved markdown", "value": artifact_result.get("success")},
        {"item": "Markdown filename", "value": artifact_result.get("filename")},
        {"item": "Markdown path", "value": artifact_result.get("path")},
    ]


def _render_data_sufficiency_summary_tables(sufficiency_result: dict[str, Any]) -> None:
    """Render Data Horizon / Parameter Sufficiency tables from a service result."""
    summary = sufficiency_result.get("summary") if isinstance(sufficiency_result.get("summary"), dict) else {}
    st.write("Summary")
    if summary:
        st.dataframe(_safe_dataframe_rows([summary]), use_container_width=True, hide_index=True)
    else:
        st.info("No data sufficiency summary is available.")

    rows = sufficiency_result.get("rows") or []
    compact_rows = [
        {column: row.get(column) for column in DATA_SUFFICIENCY_ROW_COLUMNS}
        for row in rows
        if isinstance(row, dict)
    ]
    with st.expander(f"CSV Sufficiency Rows ({len(compact_rows)} rows)", expanded=bool(compact_rows)):
        if compact_rows:
            st.dataframe(_safe_dataframe_rows(compact_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No CSV sufficiency rows are available.")

    warning_rows = [
        {
            "ticker": row.get("ticker"),
            "timeframe": row.get("timeframe"),
            "source_csv_name": row.get("source_csv_name"),
            "rows_available": row.get("rows_available"),
            "noise_warning": row.get("noise_warning"),
            "provider_limit_warning": row.get("provider_limit_warning"),
            "notes": row.get("notes"),
        }
        for row in rows
        if isinstance(row, dict) and (row.get("noise_warning") or row.get("provider_limit_warning"))
    ]
    if warning_rows:
        with st.expander(f"Warning Review ({len(warning_rows)} rows)", expanded=True):
            st.dataframe(_safe_dataframe_rows(warning_rows), use_container_width=True, hide_index=True)


def _session_int_default(key: str, fallback: int) -> int:
    value = st.session_state.get(key, fallback)
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return fallback
    return parsed if parsed > 0 else fallback


def _render_data_sufficiency_section(result: dict[str, Any] | None) -> None:
    """Render Data Horizon / Parameter Sufficiency diagnostics controls."""
    st.markdown("#### Data Horizon / Parameter Sufficiency")
    st.caption(
        "Assess whether the current report folder has enough source data for Eigen/PCA windows, "
        "Monte Carlo horizons, Backtest Outcome horizons, and calibration review. This is diagnostics "
        "only and does not optimize parameters."
    )
    st.info(
        "Reads saved source CSV artifacts, prefers canonical `*_wyckoff_annotated.csv`, and ignores "
        "derivative CSVs such as `*_pv_eigen.csv`, `*_backtest_candidates*.csv`, and "
        "`*_backtest_results*.csv`. Does not rerun analysis, Monte Carlo, or backtests. No automatic "
        "parameter optimization. Sufficient rows do not imply predictive validity. Low-timeframe noise "
        "remains visible."
    )

    report_dir = _report_dir_for_backtest_snapshot(result)
    if not report_dir:
        st.warning("No report folder is available for Data Sufficiency diagnostics.")
        return

    control_col1, control_col2, control_col3 = st.columns(3)
    with control_col1:
        eigen_window = st.number_input(
            "Eigen/PCA window",
            min_value=1,
            max_value=1000,
            value=80,
            step=1,
            key="data_sufficiency_eigen_window",
        )
    with control_col2:
        monte_carlo_horizon = st.number_input(
            "Monte Carlo horizon bars",
            min_value=1,
            max_value=1000,
            value=_session_int_default("monte_carlo_horizon_bars", 60),
            step=1,
            key="data_sufficiency_monte_carlo_horizon",
        )
    with control_col3:
        backtest_horizon = st.number_input(
            "Backtest horizon bars",
            min_value=1,
            max_value=1000,
            value=_session_int_default("backtest_outcome_horizon_bars", 60),
            step=1,
            key="data_sufficiency_backtest_horizon",
        )

    save_markdown = st.checkbox(
        "Save markdown data sufficiency summary",
        value=True,
        key="data_sufficiency_save_markdown",
    )

    if st.button("Summarize Data Sufficiency"):
        parameter_context = {
            "eigen_window": int(eigen_window),
            "monte_carlo_horizon": int(monte_carlo_horizon),
            "backtest_horizon": int(backtest_horizon),
        }
        try:
            sufficiency_result = summarize_report_folder_data_sufficiency(
                report_dir,
                parameter_context=parameter_context,
            )
        except Exception as exc:
            sufficiency_result = {
                "success": False,
                "report_dir": report_dir,
                "csv_file_count": 0,
                "rows": [],
                "summary": {},
                "warnings": [],
                "errors": [f"{type(exc).__name__}: {exc}"],
            }

        st.session_state["latest_data_sufficiency_summary"] = sufficiency_result
        st.session_state["latest_data_sufficiency_summary_artifact"] = None
        artifact_result = None
        if save_markdown and sufficiency_result.get("success"):
            ticker, timeframe = _backtest_calibration_filename_context(result)
            try:
                artifact_result = summarize_folder_to_data_sufficiency_markdown(
                    report_dir,
                    parameter_context=parameter_context,
                    ticker=ticker,
                    timeframe=timeframe,
                )
            except Exception as exc:
                artifact_result = {
                    "success": False,
                    "path": None,
                    "filename": None,
                    "errors": [f"{type(exc).__name__}: {exc}"],
                    "warnings": [],
                }
            st.session_state["latest_data_sufficiency_summary_artifact"] = artifact_result

        if artifact_result is not None and artifact_result.get("success"):
            st.success(f"Saved Data Sufficiency Summary: `{artifact_result.get('path')}`")
            st.caption("Saved file appears in Generated Artifacts as data_sufficiency_summary_md.")
            st.caption("Refresh or revisit Generated Artifacts to preview the data_sufficiency_summary_md file.")
        elif artifact_result is not None and not artifact_result.get("success"):
            st.error("Could not save Data Sufficiency Summary markdown.")

    latest_summary = st.session_state.get("latest_data_sufficiency_summary")
    latest_artifact = st.session_state.get("latest_data_sufficiency_summary_artifact")

    if isinstance(latest_summary, dict):
        if latest_summary.get("success"):
            st.success("Data Horizon / Parameter Sufficiency Summary is available.")
        else:
            st.warning("Data Horizon / Parameter Sufficiency Summary did not complete successfully.")

        st.dataframe(
            _safe_dataframe_rows(_data_sufficiency_status_rows(latest_summary, latest_artifact)),
            use_container_width=True,
            hide_index=True,
        )

        warnings = latest_summary.get("warnings") or []
        errors = latest_summary.get("errors") or []
        if warnings:
            st.info("Warnings: " + "; ".join(str(warning) for warning in warnings))
        if errors:
            st.warning("Errors: " + "; ".join(str(error) for error in errors))

        if isinstance(latest_artifact, dict):
            artifact_errors = latest_artifact.get("errors") or []
            artifact_warnings = latest_artifact.get("warnings") or []
            if latest_artifact.get("path"):
                st.caption(f"Last saved Data Sufficiency artifact: `{latest_artifact.get('path')}`")
            if artifact_warnings:
                st.info("Artifact warnings: " + "; ".join(str(warning) for warning in artifact_warnings))
            if artifact_errors:
                st.warning("Artifact errors: " + "; ".join(str(error) for error in artifact_errors))

        _render_data_sufficiency_summary_tables(latest_summary)


def _render_backtest_candidate_snapshot_section(result: dict[str, Any] | None) -> None:
    """Render save controls for the selected Strategy Ranking candidate snapshot."""
    st.markdown("#### Backtest Candidate Snapshot")
    st.caption(
        "Save the selected Strategy Ranking candidate as a frozen candidate snapshot for later "
        "backtest calibration. This does not run a backtest or create a trade signal."
    )

    selected_candidate = _current_strategy_candidate_for_backtest()
    if not selected_candidate:
        st.info("Select/send a Strategy Ranking candidate first.")
        return

    report_dir = _report_dir_for_backtest_snapshot(result)
    snapshot_result = build_candidate_snapshot_from_strategy_candidate(selected_candidate, report_dir=report_dir)
    snapshot = snapshot_result.get("snapshot") if isinstance(snapshot_result.get("snapshot"), dict) else {}
    validation = snapshot_result.get("validation") if isinstance(snapshot_result.get("validation"), dict) else {}
    validation_status = validation.get("status") or "unknown"

    st.write(f"Validation status: `{validation_status}`")
    errors = validation.get("errors") or []
    warnings = validation.get("warnings") or []
    if errors:
        st.warning("Validation errors: " + "; ".join(str(error) for error in errors))
    if warnings:
        st.info("Validation warnings: " + "; ".join(str(warning) for warning in warnings))
    if validation_status == "missing_signal_location":
        st.warning(
            "This candidate can be saved for audit, but deterministic outcome evaluation will require "
            "signal_row_index or signal_timestamp."
        )

    preview_fields = [
        "ticker",
        "timeframe",
        "source_csv",
        "signal_timestamp",
        "signal_row_index",
        "entry",
        "stop_loss",
        "take_profit",
        "risk_reward",
        "strategy_score",
        "wyckoff_phase",
        "wyckoff_event",
    ]
    preview_row = {field: snapshot.get(field) for field in preview_fields}
    preview_row["validation_status"] = validation_status
    st.dataframe(_safe_dataframe_rows([preview_row]), use_container_width=True, hide_index=True)

    if not report_dir:
        st.warning("No report folder is available to save the candidate snapshot.")
        return

    if st.button("Save Backtest Candidate Snapshot"):
        save_result = write_backtest_candidate_csv(
            snapshot_result,
            report_dir,
            ticker=snapshot.get("ticker"),
            timeframe=snapshot.get("timeframe"),
        )
        st.session_state["latest_backtest_candidate_snapshot"] = snapshot_result
        st.session_state["latest_backtest_candidate_csv"] = save_result
        if save_result.get("success"):
            st.success(f"Saved backtest candidate snapshot: `{save_result.get('path')}`")
            st.caption("Saved file will appear in Generated Artifacts as backtest_candidates_csv.")
        else:
            st.error("Could not save backtest candidate snapshot.")
            for error in save_result.get("errors") or []:
                st.write(f"- {error}")


def _render_backtest_outcome_evaluation_section(result: dict[str, Any] | None) -> None:
    """Render deterministic backtest outcome evaluation controls."""
    st.markdown("#### Backtest Outcome Evaluation")
    st.caption(
        "Evaluate saved Backtest Candidate Snapshot CSV artifacts against their referenced OHLC source CSVs. "
        "This is a deterministic research/calibration step and does not create a trade signal."
    )
    st.info(
        "Uses frozen candidate levels. Does not recompute Strategy Ranking, run Monte Carlo, or optimize "
        "parameters. Same-bar ambiguity follows the selected tie-break policy."
    )

    report_dir = _report_dir_for_backtest_snapshot(result)
    if not report_dir:
        st.warning("No report folder is available for backtest outcome evaluation.")
        return

    artifacts = _backtest_candidate_csv_artifacts(report_dir)
    if not artifacts:
        st.info("No backtest candidate snapshot CSV artifacts were found. Save a Backtest Candidate Snapshot first.")
        return

    artifact_options = [str(artifact.get("path") or "") for artifact in artifacts]
    artifact_by_path = {str(artifact.get("path") or ""): artifact for artifact in artifacts}
    default_path = artifact_options[_default_backtest_candidate_csv_index(artifacts)]
    if st.session_state.get("backtest_outcome_candidate_csv") not in artifact_options:
        st.session_state["backtest_outcome_candidate_csv"] = default_path

    selected_path = st.selectbox(
        "Backtest Candidate Snapshot CSV",
        options=artifact_options,
        format_func=lambda path: (
            f"{artifact_by_path[path].get('name') or Path(path).name}"
            f" | {artifact_by_path[path].get('modified', '')}"
        ),
        key="backtest_outcome_candidate_csv",
    )
    st.caption(f"Selected candidate snapshot: `{selected_path}`")
    st.caption("Expected output artifact kind: `backtest_results_csv`")

    read_result = read_candidate_snapshot_csv(selected_path)
    if read_result.get("success"):
        rows = read_result.get("rows") or []
        st.write(f"Candidate rows: `{read_result.get('count', len(rows))}`")
        preview_rows = _backtest_candidate_preview_rows(rows)
        if preview_rows:
            st.dataframe(_safe_dataframe_rows(preview_rows), use_container_width=True, hide_index=True)
    else:
        st.error("Could not read the selected candidate snapshot CSV.")
        for error in read_result.get("errors") or []:
            st.write(f"- {error}")

    control_col1, control_col2, control_col3 = st.columns(3)
    with control_col1:
        horizon_bars = st.number_input(
            "Horizon bars",
            min_value=1,
            max_value=500,
            value=20,
            step=1,
            key="backtest_outcome_horizon_bars",
        )
    with control_col2:
        tie_break_policy = st.selectbox(
            "Tie-break policy",
            options=["conservative", "optimistic", "open_proximity", "unknown"],
            index=0,
            key="backtest_outcome_tie_break_policy",
        )
    with control_col3:
        write_invalid_rows = st.checkbox(
            "Write invalid rows",
            value=True,
            key="backtest_outcome_write_invalid_rows",
            help="When enabled, invalid/incomplete candidate snapshots are preserved as INVALID rows for audit.",
        )

    evaluation_result = None
    if st.button("Evaluate Backtest Outcomes"):
        try:
            evaluation_result = evaluate_candidate_snapshot_csv_to_results_csv(
                selected_path,
                output_dir=report_dir,
                horizon_bars=int(horizon_bars),
                tie_break_policy=tie_break_policy,
                write_invalid_rows=write_invalid_rows,
            )
        except Exception as exc:
            evaluation_result = {
                "success": False,
                "path": None,
                "filename": None,
                "evaluation": {},
                "write_result": None,
                "errors": [f"{type(exc).__name__}: {exc}"],
                "warnings": [],
            }
        st.session_state["latest_backtest_outcome_evaluation"] = evaluation_result
        st.session_state["latest_backtest_results_csv"] = {
            "path": evaluation_result.get("path"),
            "filename": evaluation_result.get("filename"),
        }

    if evaluation_result is None:
        latest_evaluation = st.session_state.get("latest_backtest_outcome_evaluation")
        if (
            isinstance(latest_evaluation, dict)
            and str(latest_evaluation.get("candidates_csv_path") or "") == selected_path
        ):
            evaluation_result = latest_evaluation

    if isinstance(evaluation_result, dict):
        if evaluation_result.get("success"):
            st.success(f"Saved backtest outcome results: `{evaluation_result.get('path')}`")
            st.caption("Saved file appears in Generated Artifacts as backtest_results_csv.")
            st.caption("Refresh or revisit Generated Artifacts to see the new backtest_results_csv file.")
        elif evaluation_result:
            st.error("Backtest outcome evaluation did not produce a result CSV.")

        st.dataframe(
            _safe_dataframe_rows(_backtest_outcome_summary_rows(evaluation_result)),
            use_container_width=True,
            hide_index=True,
        )
        errors = evaluation_result.get("errors") or []
        warnings = evaluation_result.get("warnings") or []
        if errors:
            st.warning("Errors: " + "; ".join(str(error) for error in errors))
        if warnings:
            st.info("Warnings: " + "; ".join(str(warning) for warning in warnings))

        evaluation = evaluation_result.get("evaluation") if isinstance(evaluation_result.get("evaluation"), dict) else {}
        result_rows = evaluation.get("result_rows") or []
        preview_rows = _backtest_result_preview_rows(result_rows)
        if preview_rows:
            with st.expander("Backtest result row preview"):
                st.dataframe(_safe_dataframe_rows(preview_rows), use_container_width=True, hide_index=True)


def _render_backtest_calibration_summary_section(result: dict[str, Any] | None) -> None:
    """Render service-only Backtest Calibration Summary controls."""
    st.markdown("#### Backtest Calibration Summary")
    st.caption(
        "Summarize saved Backtest Outcome Result CSV artifacts for ticker/timeframe calibration review. "
        "This is a research/calibration summary and does not optimize parameters or create trade signals."
    )
    st.info(
        "Calibration only. Reads saved result CSVs, does not rerun backtests, does not run Monte Carlo, "
        "and does not optimize parameters. Small samples should not be overinterpreted."
    )

    report_dir = _report_dir_for_backtest_snapshot(result)
    if not report_dir:
        st.warning("No report folder is available for Backtest Calibration Summary.")
        return

    artifacts = _backtest_result_csv_artifacts(report_dir)
    if not artifacts:
        st.info("No backtest result CSV artifacts were found. Run Backtest Outcome Evaluation first.")
        return

    artifact_rows = [
        {
            "name": artifact.get("name"),
            "kind": artifact.get("kind"),
            "timeframe": artifact.get("timeframe"),
            "modified": artifact.get("modified"),
            "path": artifact.get("path"),
        }
        for artifact in artifacts
    ]
    st.write(f"Available backtest result CSV artifacts: `{len(artifact_rows)}`")
    st.dataframe(_safe_dataframe_rows(artifact_rows), use_container_width=True, hide_index=True)
    st.caption("Expected output: `backtest_calibration_summary_md`")

    save_markdown = st.checkbox(
        "Save markdown calibration summary",
        value=True,
        key="backtest_calibration_save_markdown",
    )

    if st.button("Summarize Backtest Calibration"):
        try:
            summary_result = summarize_backtest_results_folder(report_dir)
        except Exception as exc:
            summary_result = {
                "success": False,
                "report_dir": report_dir,
                "source_result_files": [],
                "file_count": len(artifacts),
                "read_count": 0,
                "count": 0,
                "summary": {},
                "summary_rows": [],
                "grouped_summary_rows": [],
                "invalid_reason_rows": [],
                "warnings": [],
                "errors": [f"{type(exc).__name__}: {exc}"],
            }

        st.session_state["latest_backtest_calibration_summary"] = summary_result
        st.session_state["latest_backtest_calibration_summary_artifact"] = None
        artifact_result = None
        if save_markdown and summary_result.get("success"):
            ticker, timeframe = _backtest_calibration_filename_context(result)
            try:
                artifact_result = summarize_folder_to_backtest_calibration_markdown(
                    report_dir,
                    ticker=ticker,
                    timeframe=timeframe,
                )
            except Exception as exc:
                artifact_result = {
                    "success": False,
                    "path": None,
                    "filename": None,
                    "errors": [f"{type(exc).__name__}: {exc}"],
                    "warnings": [],
                }
            st.session_state["latest_backtest_calibration_summary_artifact"] = artifact_result

        if artifact_result is not None and artifact_result.get("success"):
            st.success(f"Saved Backtest Calibration Summary: `{artifact_result.get('path')}`")
            st.caption("Saved file appears in Generated Artifacts as backtest_calibration_summary_md.")
            st.caption("Refresh or revisit Generated Artifacts to preview the backtest_calibration_summary_md file.")
        elif artifact_result is not None and not artifact_result.get("success"):
            st.error("Could not save Backtest Calibration Summary markdown.")

    latest_summary = st.session_state.get("latest_backtest_calibration_summary")
    latest_artifact = st.session_state.get("latest_backtest_calibration_summary_artifact")

    if isinstance(latest_summary, dict):
        if latest_summary.get("success"):
            st.success("Backtest Calibration Summary is available.")
        else:
            st.warning("Backtest Calibration Summary did not complete successfully.")

        st.dataframe(
            _safe_dataframe_rows(_backtest_calibration_status_rows(latest_summary, latest_artifact)),
            use_container_width=True,
            hide_index=True,
        )

        warnings = latest_summary.get("warnings") or []
        errors = latest_summary.get("errors") or []
        if warnings:
            st.info("Warnings: " + "; ".join(str(warning) for warning in warnings))
        if errors:
            st.warning("Errors: " + "; ".join(str(error) for error in errors))

        if isinstance(latest_artifact, dict):
            artifact_errors = latest_artifact.get("errors") or []
            artifact_warnings = latest_artifact.get("warnings") or []
            if latest_artifact.get("path"):
                st.caption(f"Last saved markdown artifact: `{latest_artifact.get('path')}`")
            if artifact_warnings:
                st.info("Artifact warnings: " + "; ".join(str(warning) for warning in artifact_warnings))
            if artifact_errors:
                st.warning("Artifact errors: " + "; ".join(str(error) for error in artifact_errors))

        _render_backtest_calibration_summary_tables(latest_summary)


def _render_strategy_results(strategy_result: dict[str, Any] | None, result: dict[str, Any] | None = None) -> None:
    """Render strategy ranking output."""
    if not strategy_result:
        st.info("Choose tickers and click Rank Candidates to scan existing reports.")
        return

    st.caption(f"Using report root: `{strategy_result.get('report_root')}`")
    st.caption("Strategy source: latest batch folder when available")
    st.caption(f"Selected timeframe: `{strategy_result.get('timeframe')}`")

    if not strategy_result.get("success"):
        _render_strategy_error(strategy_result)
        _render_strategy_diagnostics(strategy_result)
        return

    dataframe = strategy_result.get("dataframe")
    if dataframe is None or dataframe.empty:
        st.info(
            "No candidates passed the filters. Try a lower min RR, a different timeframe, "
            "or confirm reports exist for those tickers."
        )
        _render_strategy_diagnostics(strategy_result)
        return

    st.write(f"Result count: `{len(dataframe)}`")
    st.dataframe(dataframe, use_container_width=True)
    _render_strategy_diagnostics(strategy_result)

    results = strategy_result.get("results") or []
    labels = [
        f"{candidate.get('ticker', 'UNKNOWN')} | {candidate.get('tf', '')} | "
        f"score {candidate.get('score', 'NA')}"
        for candidate in results
    ]
    selected_index = st.selectbox(
        "Select candidate",
        options=list(range(len(results))),
        format_func=lambda index: labels[index],
    )
    selected_candidate = results[selected_index]
    st.session_state.latest_strategy_candidate = selected_candidate
    st.session_state.selected_strategy_candidate = selected_candidate
    if selected_candidate.get("mc_matched_by") == "fallback_latest":
        st.warning(
            "This candidate used a fallback Monte Carlo summary that may not match "
            "the selected timeframe."
        )
    st.json(selected_candidate)
    _render_data_sufficiency_section(result)
    _render_backtest_candidate_snapshot_section(result)
    _render_backtest_outcome_evaluation_section(result)
    _render_backtest_calibration_summary_section(result)
    _render_monte_carlo_forecast_calibration_summary_section(result)

    if st.button("Use selected candidate in Monte Carlo"):
        trade_plan = _trade_plan_from_strategy_candidate(selected_candidate)
        st.session_state.monte_carlo_prefill = trade_plan
        st.session_state.latest_strategy_candidate = selected_candidate
        st.session_state.selected_strategy_candidate = selected_candidate
        st.session_state.monte_carlo_result = None
        st.session_state.latest_monte_carlo_result = None
        st.success("Selected candidate sent to Monte Carlo tab.")


def _render_strategy_ranking(result: dict[str, Any] | None) -> None:
    """Render the Strategy Ranking tab."""
    st.write(
        "Rank long candidates from generated MarketFlow reports using the existing "
        "`marketflow_strategy` logic."
    )
    st.caption(f"Configured report root: `{get_report_root()}`")
    st.caption("This scan uses the latest batch/report namespace when available.")

    if st.session_state.get("strategy_tickers_prefill"):
        st.session_state.strategy_tickers = st.session_state.pop("strategy_tickers_prefill")

    if "strategy_tickers" not in st.session_state:
        st.session_state.strategy_tickers = _default_strategy_ticker_text(result)

    ticker_text = st.text_area(
        "Tickers",
        key="strategy_tickers",
        help="Enter tickers separated by spaces, commas, or new lines.",
    )
    strategy_tf = st.selectbox(
        "Timeframe",
        options=STRATEGY_TIMEFRAMES,
        index=1,
    )
    min_rr = st.number_input(
        "Minimum Risk/Reward",
        min_value=0.1,
        value=1.5,
        step=0.1,
    )
    max_sl_atr = st.number_input(
        "Max Stop ATR",
        min_value=0.1,
        value=2.0,
        step=0.1,
    )
    prefer_phases = st.multiselect(
        "Preferred Wyckoff Phases",
        options=WYCKOFF_PHASE_OPTIONS,
        default=["C", "D", "E"],
    )
    use_mc = st.checkbox(
        "Use Monte Carlo POP if available",
        value=False,
        help="Optional. If no MC files exist, strategy logic should use neutral defaults.",
    )
    st.caption(
        "Monte Carlo is optional. For safer workflow, rank candidates first, then run Monte Carlo "
        "on selected candidates. The MC checkbox uses available MC summaries when present."
    )
    st.caption(
        "When enabled, Strategy Ranking prefers Monte Carlo summaries matching the selected "
        "timeframe. If none are found, it may fall back to the latest MC summary and marks "
        "that in the results."
    )

    if st.button("Rank Candidates"):
        tickers = normalize_tickers(ticker_text)
        if not tickers:
            st.session_state.strategy_result = {
                "success": False,
                "error": "Enter at least one ticker.",
                "error_type": "ValidationError",
                "traceback": None,
                "results": [],
                "dataframe": None,
                "report_root": get_report_root(),
                "timeframe": strategy_tf,
            }
        else:
            with st.spinner("Ranking strategy candidates..."):
                st.session_state.strategy_result = rank_latest_candidates(
                    tickers=tickers,
                    timeframe=strategy_tf,
                    min_rr=float(min_rr),
                    max_sl_atr=float(max_sl_atr),
                    prefer_phases=tuple(prefer_phases),
                    use_mc=use_mc,
                )

    _render_strategy_results(st.session_state.get("strategy_result"), result)


def _render_batch_result(batch_result: dict[str, Any] | None) -> None:
    """Render batch analysis status and per-ticker results."""
    if not batch_result:
        st.info("Enter tickers and click Run Batch Analysis to analyze multiple symbols.")
        return

    if batch_result.get("success"):
        st.success("Batch analysis completed.")
    else:
        error_type = batch_result.get("error_type")
        error = batch_result.get("error") or "Batch analysis failed."
        st.error(f"{error_type}: {error}" if error_type else error)

    if batch_result.get("traceback"):
        with st.expander("Batch error details"):
            st.code(batch_result["traceback"], language="python")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _display_optional_metric("Run ID", batch_result.get("run_id"))
    with col2:
        _display_optional_metric("Namespace", batch_result.get("namespace") or "Disabled")
    with col3:
        succeeded = sum(1 for item in batch_result.get("results", []) if item.get("success"))
        _display_optional_metric("Succeeded", succeeded)
    with col4:
        failed = sum(1 for item in batch_result.get("results", []) if not item.get("success"))
        _display_optional_metric("Failed", failed)

    if batch_result.get("batch_output_dir"):
        st.caption(f"Batch output directory: `{batch_result['batch_output_dir']}`")
    if batch_result.get("summary_csv"):
        st.caption(f"Summary CSV: `{batch_result['summary_csv']}`")

    notes = batch_result.get("notes") or []
    if notes:
        with st.expander("Batch notes"):
            for note in notes:
                st.write(f"- {note}")

    results = batch_result.get("results") or []
    if results:
        st.dataframe(
            _safe_dataframe_rows([
                {
                    "ticker": item.get("ticker"),
                    "success": item.get("success"),
                    "output_dir": item.get("output_dir"),
                    "narrative_available": item.get("narrative_available"),
                    "error_type": item.get("error_type"),
                    "error": item.get("error"),
                }
                for item in results
            ]),
            use_container_width=True,
            hide_index=True,
        )

        successful_tickers = [item["ticker"] for item in results if item.get("success")]
        if successful_tickers:
            st.info("You can now use Strategy Ranking on these tickers.")
            if st.button("Use batch tickers in Strategy Ranking"):
                st.session_state.strategy_tickers_prefill = " ".join(successful_tickers)
                st.success("Batch tickers sent to Strategy Ranking.")


def _render_batch_analysis() -> None:
    """Render the Batch Analysis tab."""
    st.write("Run MarketFlow analysis for multiple tickers using the existing batch workflow.")

    ticker_text = st.text_area(
        "Batch tickers",
        value="AAPL MSFT NVDA",
        help="Enter tickers separated by spaces, commas, or new lines.",
        key="batch_tickers",
    )
    batch_timeframes = st.multiselect(
        "Batch timeframes",
        options=TIMEFRAME_OPTIONS,
        default=DEFAULT_TIMEFRAMES,
        key="batch_timeframes",
    )
    enable_tvm = st.checkbox(
        "Enable TVM batch memory",
        value=True,
        help="Creates a shared batch namespace and .tvm_store for the run.",
    )

    if st.button("Run Batch Analysis", type="primary"):
        tickers = normalize_batch_tickers(ticker_text)
        if not tickers:
            st.session_state.batch_result = {
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
        else:
            with st.spinner("Running batch analysis..."):
                st.session_state.batch_result = run_batch_analysis(
                    tickers=tickers,
                    timeframes=batch_timeframes,
                    enable_tvm=enable_tvm,
                )

    _render_batch_result(st.session_state.get("batch_result"))


def _default_trade_levels(latest_close: float | None) -> tuple[float, float, float]:
    """Return sensible entry, stop, and take-profit defaults."""
    if latest_close is None or latest_close <= 0:
        return 0.0, 0.0, 0.0
    return latest_close, latest_close * 0.98, latest_close * 1.05


def _safe_float(value: Any) -> float | None:
    """Convert a value to float when possible."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _trade_plan_from_strategy_candidate(candidate: dict[str, Any] | None) -> dict[str, Any] | None:
    """
    Return normalized trade plan from a Strategy Ranking candidate:
    ticker, csv, tf, entry, stop_loss, take_profit, source.
    """
    if not isinstance(candidate, dict):
        return None

    return {
        "ticker": candidate.get("ticker"),
        "csv": candidate.get("csv"),
        "tf": candidate.get("tf"),
        "entry": _safe_float(candidate.get("entry") if candidate.get("entry") is not None else candidate.get("close")),
        "stop_loss": _safe_float(
            candidate.get("stop_loss") if candidate.get("stop_loss") is not None else candidate.get("sl")
        ),
        "take_profit": _safe_float(
            candidate.get("take_profit") if candidate.get("take_profit") is not None else candidate.get("tp")
        ),
        "source": "strategy_ranking",
        "source_candidate": candidate,
    }


def _prefill_token(prefill: dict[str, Any] | None) -> tuple[Any, ...] | None:
    """Return a stable token for candidate Monte Carlo prefill state."""
    if not prefill:
        return None
    return (
        prefill.get("ticker"),
        prefill.get("csv"),
        prefill.get("tf"),
        prefill.get("entry"),
        prefill.get("stop_loss"),
        prefill.get("take_profit"),
        prefill.get("source"),
    )


def _path_matches(left: str, right: str) -> bool:
    """Return True when two paths point to the same file."""
    try:
        return Path(left).resolve() == Path(right).resolve()
    except Exception:
        return str(left) == str(right)


def _paths_match_optional(left: Any, right: Any) -> bool:
    """Return True when optional paths match after local resolution."""
    if not left and not right:
        return True
    if not left or not right:
        return False
    return _path_matches(str(left), str(right))


def _numbers_match(left: Any, right: Any, tolerance: float = 1e-6) -> bool:
    """Return True when optional numeric values match within tolerance."""
    left_value = _safe_float(left)
    right_value = _safe_float(right)
    if left_value is None and right_value is None:
        return True
    if left_value is None or right_value is None:
        return False
    return abs(left_value - right_value) <= tolerance


def _mc_trade_plan_from_result(mc_result: dict[str, Any] | None) -> dict[str, Any] | None:
    """Return normalized Monte Carlo trade-plan metadata from a result wrapper."""
    if not isinstance(mc_result, dict):
        return None
    trade_plan = mc_result.get("trade_plan")
    if isinstance(trade_plan, dict):
        return trade_plan

    raw = mc_result.get("result") if isinstance(mc_result.get("result"), dict) else {}
    params = raw.get("params") if isinstance(raw.get("params"), dict) else {}
    return {
        "ticker": mc_result.get("ticker"),
        "csv": mc_result.get("csv_path") or mc_result.get("csv"),
        "tf": mc_result.get("timeframe") or mc_result.get("tf"),
        "entry": _safe_float(params.get("entry") or mc_result.get("entry")),
        "stop_loss": _safe_float(params.get("sl") or mc_result.get("stop_loss")),
        "take_profit": _safe_float(params.get("tp") or mc_result.get("take_profit")),
        "source": mc_result.get("source") or "manual",
    }


def _monte_carlo_alignment(
    candidate: dict[str, Any] | None,
    mc_result: dict[str, Any] | None,
) -> dict[str, Any]:
    """Compare a Strategy Ranking candidate with a Monte Carlo result trade plan."""
    candidate_plan = _trade_plan_from_strategy_candidate(candidate)
    mc_plan = _mc_trade_plan_from_result(mc_result)

    if not candidate_plan:
        return {
            "candidate_csv": None,
            "candidate_tf": None,
            "candidate_entry": None,
            "candidate_stop_loss": None,
            "candidate_take_profit": None,
            "mc_csv": (mc_plan or {}).get("csv"),
            "mc_tf": (mc_plan or {}).get("tf"),
            "mc_entry": (mc_plan or {}).get("entry"),
            "mc_stop_loss": (mc_plan or {}).get("stop_loss"),
            "mc_take_profit": (mc_plan or {}).get("take_profit"),
            "matches": bool(mc_plan),
            "differences": [] if mc_plan else ["missing_monte_carlo_result"],
        }
    if not mc_plan:
        return {
            "candidate_csv": candidate_plan.get("csv"),
            "candidate_tf": candidate_plan.get("tf"),
            "candidate_entry": candidate_plan.get("entry"),
            "candidate_stop_loss": candidate_plan.get("stop_loss"),
            "candidate_take_profit": candidate_plan.get("take_profit"),
            "mc_csv": None,
            "mc_tf": None,
            "mc_entry": None,
            "mc_stop_loss": None,
            "mc_take_profit": None,
            "matches": False,
            "differences": ["missing_monte_carlo_result"],
        }

    differences: list[str] = []
    if not _paths_match_optional(candidate_plan.get("csv"), mc_plan.get("csv")):
        differences.append("csv")
    if (candidate_plan.get("tf") or None) != (mc_plan.get("tf") or None):
        differences.append("timeframe")
    if not _numbers_match(candidate_plan.get("entry"), mc_plan.get("entry")):
        differences.append("entry")
    if not _numbers_match(candidate_plan.get("stop_loss"), mc_plan.get("stop_loss")):
        differences.append("stop_loss")
    if not _numbers_match(candidate_plan.get("take_profit"), mc_plan.get("take_profit")):
        differences.append("take_profit")

    return {
        "candidate_csv": candidate_plan.get("csv"),
        "candidate_tf": candidate_plan.get("tf"),
        "candidate_entry": candidate_plan.get("entry"),
        "candidate_stop_loss": candidate_plan.get("stop_loss"),
        "candidate_take_profit": candidate_plan.get("take_profit"),
        "mc_csv": mc_plan.get("csv"),
        "mc_tf": mc_plan.get("tf"),
        "mc_entry": mc_plan.get("entry"),
        "mc_stop_loss": mc_plan.get("stop_loss"),
        "mc_take_profit": mc_plan.get("take_profit"),
        "matches": not differences,
        "differences": differences,
    }


def _format_alignment_path(path: Any) -> str | None:
    """Return a compact filename for alignment display."""
    if not path:
        return None
    return Path(str(path)).name


def _candidate_snapshot_context_for_monte_carlo(
    *,
    selected_csv: str,
    timeframe: str | None,
    entry: Any,
    stop_loss: Any,
    take_profit: Any,
) -> tuple[dict[str, Any] | None, str | None]:
    """Return latest candidate snapshot metadata only when it matches current MC inputs."""
    snapshot_result = st.session_state.get("latest_backtest_candidate_snapshot")
    if not isinstance(snapshot_result, dict):
        return None, None
    snapshot = snapshot_result.get("snapshot")
    if not isinstance(snapshot, dict):
        return None, None
    if not snapshot.get("source_csv") or not _paths_match_optional(snapshot.get("source_csv"), selected_csv):
        return None, None
    if (snapshot.get("timeframe") or None) != (timeframe or None):
        return None, None
    if not (
        _numbers_match(snapshot.get("entry"), entry)
        and _numbers_match(snapshot.get("stop_loss"), stop_loss)
        and _numbers_match(snapshot.get("take_profit"), take_profit)
    ):
        return None, None

    save_result = st.session_state.get("latest_backtest_candidate_csv")
    candidate_snapshot_file = None
    if isinstance(save_result, dict):
        candidate_snapshot_file = save_result.get("filename")
        if not candidate_snapshot_file and save_result.get("path"):
            candidate_snapshot_file = Path(str(save_result.get("path"))).name
    return snapshot, candidate_snapshot_file


def _safe_filename_part(value: Any, fallback: str) -> str:
    """Return a compact filename-safe token."""
    text = str(value or fallback).strip() or fallback
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    return text.strip("._") or fallback


def _alignment_display_rows(alignment: dict[str, Any]) -> list[dict[str, Any]]:
    """Return compact candidate/MC alignment rows for UI tables."""
    return [
        {
            "field": "timeframe",
            "candidate": alignment.get("candidate_tf"),
            "monte_carlo": alignment.get("mc_tf"),
        },
        {
            "field": "csv",
            "candidate": _format_alignment_path(alignment.get("candidate_csv")),
            "monte_carlo": _format_alignment_path(alignment.get("mc_csv")),
        },
        {
            "field": "entry",
            "candidate": alignment.get("candidate_entry"),
            "monte_carlo": alignment.get("mc_entry"),
        },
        {
            "field": "stop_loss",
            "candidate": alignment.get("candidate_stop_loss"),
            "monte_carlo": alignment.get("mc_stop_loss"),
        },
        {
            "field": "take_profit",
            "candidate": alignment.get("candidate_take_profit"),
            "monte_carlo": alignment.get("mc_take_profit"),
        },
        {
            "field": "matches",
            "candidate": "yes" if alignment.get("matches") else "no",
            "monte_carlo": "; ".join(alignment.get("differences") or []),
        },
    ]


def _candidate_decision_card_data(packet: dict[str, Any] | None) -> dict[str, Any]:
    """
    Build a compact display summary from an Analyst Packet.

    This function should only read packet fields and normalize them for UI.
    It must not change analytical logic.
    """
    if not isinstance(packet, dict):
        return {}

    packet_summary = packet.get("packet_summary") if isinstance(packet.get("packet_summary"), dict) else {}
    strategy_candidate = packet.get("strategy_candidate") if isinstance(packet.get("strategy_candidate"), dict) else {}
    monte_carlo = packet.get("monte_carlo") if isinstance(packet.get("monte_carlo"), dict) else {}
    pnf = packet.get("pnf") if isinstance(packet.get("pnf"), dict) else {}
    eigen = packet.get("eigen") if isinstance(packet.get("eigen"), dict) else {}
    eigen_latest = eigen.get("latest") if isinstance(eigen.get("latest"), dict) else {}
    eigen_summary = eigen.get("summary") if isinstance(eigen.get("summary"), dict) else {}
    pnf_selection = pnf.get("selection") if isinstance(pnf.get("selection"), dict) else {}
    selected_sidecar = pnf.get("selected_sidecar") if isinstance(pnf.get("selected_sidecar"), dict) else {}
    pnf_interpretation = pnf.get("objective_interpretation") if isinstance(pnf.get("objective_interpretation"), dict) else {}
    alignment = monte_carlo.get("alignment") if isinstance(monte_carlo.get("alignment"), dict) else None

    strategy_available = bool(strategy_candidate)
    mc_status = "missing"
    if monte_carlo:
        if monte_carlo.get("manual_scenario"):
            mc_status = "manual scenario"
        elif monte_carlo.get("matches_strategy_candidate") is False:
            mc_status = "manual scenario"
        elif isinstance(alignment, dict) and alignment.get("matches") is False:
            mc_status = "manual scenario"
        elif monte_carlo.get("matches_strategy_candidate") is True or (
            isinstance(alignment, dict) and alignment.get("matches")
        ):
            mc_status = "aligned"
        else:
            mc_status = "included"

    pnf_status = "missing"
    pnf_match_score = _safe_float(pnf_selection.get("match_score"))
    if selected_sidecar:
        pnf_status = "available but weak match" if pnf_match_score is not None and pnf_match_score < 50 else "matched"
    elif pnf.get("available"):
        pnf_status = "available but weak match"

    ready_for_analyst = bool(packet_summary.get("ready_for_analyst"))
    packet_status = "ready" if ready_for_analyst else "review needed"

    return {
        "ticker": packet_summary.get("ticker") or packet.get("ticker"),
        "selected_timeframe": packet_summary.get("selected_timeframe") or strategy_candidate.get("tf"),
        "current_price": packet_summary.get("current_price"),
        "trade_entry": packet_summary.get("trade_entry"),
        "trade_stop_loss": packet_summary.get("trade_stop_loss"),
        "trade_take_profit": packet_summary.get("trade_take_profit"),
        "strategy_score": packet_summary.get("strategy_score") or strategy_candidate.get("score"),
        "pop_gate": packet_summary.get("pop_gate"),
        "pnf_gate": packet_summary.get("pnf_gate"),
        "risk_rank": packet_summary.get("risk_rank"),
        "ready_for_analyst": ready_for_analyst,
        "phase": strategy_candidate.get("phase"),
        "event": strategy_candidate.get("event"),
        "trend": strategy_candidate.get("trend"),
        "score": strategy_candidate.get("score"),
        "rr": strategy_candidate.get("rr"),
        "pop_tp_first": monte_carlo.get("pop_tp_first"),
        "p_sl_first": monte_carlo.get("p_sl_first"),
        "p_neither": monte_carlo.get("p_neither"),
        "R_mean": monte_carlo.get("R_mean") if "R_mean" in monte_carlo else monte_carlo.get("r_mean"),
        "model": monte_carlo.get("model"),
        "paths": monte_carlo.get("paths"),
        "horizon_bars": monte_carlo.get("horizon_bars"),
        "matches_strategy_candidate": monte_carlo.get("matches_strategy_candidate"),
        "alignment": alignment,
        "manual_scenario": bool(monte_carlo.get("manual_scenario")),
        "pnf_selected_sidecar": selected_sidecar.get("filename") or pnf_selection.get("selected_filename"),
        "pnf_match_score": pnf_selection.get("match_score"),
        "pnf_matched_by": pnf_selection.get("matched_by"),
        "pnf_objective": selected_sidecar.get("objective"),
        "pnf_objective_r_multiple": selected_sidecar.get("objective_r_multiple"),
        "pnf_objective_direction": (
            pnf_interpretation.get("objective_direction")
            or packet_summary.get("pnf_objective_direction")
            or selected_sidecar.get("objective_direction")
        ),
        "pnf_objective_quality": (
            pnf_interpretation.get("objective_quality")
            or packet_summary.get("pnf_objective_quality")
            or selected_sidecar.get("objective_quality")
        ),
        "pnf_objective_supports_trade": (
            pnf_interpretation.get("objective_supports_trade")
            if "objective_supports_trade" in pnf_interpretation
            else packet_summary.get("pnf_objective_supports_trade")
        ),
        "pnf_objective_distance_pct": pnf_interpretation.get("objective_distance_pct") or selected_sidecar.get("objective_distance_pct"),
        "pnf_objective_notes": pnf_interpretation.get("notes") or selected_sidecar.get("objective_notes") or [],
        "eigen_available": packet_summary.get("eigen_available") if "eigen_available" in packet_summary else bool(eigen.get("available")),
        "eigen_matched_by": packet_summary.get("eigen_matched_by") or eigen.get("matched_by"),
        "eigen_latest_residual": packet_summary.get("eigen_latest_residual") if "eigen_latest_residual" in packet_summary else eigen_latest.get("pv_eigen_residual"),
        "eigen_latest_coupling": packet_summary.get("eigen_latest_coupling") if "eigen_latest_coupling" in packet_summary else eigen_latest.get("pv_eigen_coupling"),
        "eigen_latest_divergence": packet_summary.get("eigen_latest_divergence") if "eigen_latest_divergence" in packet_summary else eigen_latest.get("pv_effort_result_divergence"),
        "eigen_divergence_count": packet_summary.get("eigen_divergence_count") if "eigen_divergence_count" in packet_summary else eigen_summary.get("divergence_count"),
        "eigen_recent_divergence_count": packet_summary.get("eigen_recent_divergence_count") if "eigen_recent_divergence_count" in packet_summary else eigen_summary.get("recent_divergence_count"),
        "eigen_observation": eigen_summary.get("observation"),
        "strategy_status": "available" if strategy_available else "missing",
        "monte_carlo_status": mc_status,
        "pnf_status": pnf_status,
        "packet_status": packet_status,
    }


def _summary_value(value: Any) -> str:
    """Format a decision summary value for markdown."""
    if value is None or value == "":
        return "not available"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def _summary_percent(value: Any) -> str:
    """Format a decision summary probability for markdown."""
    if value is None or value == "":
        return "not available"
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return str(value)


def _summary_notes(value: Any) -> str:
    """Format note lists for markdown."""
    if isinstance(value, list):
        notes = [str(item) for item in value if item]
        return "; ".join(notes) if notes else "not available"
    return _summary_value(value)


def _candidate_decision_summary_filename(card: dict[str, Any]) -> str:
    """Return a timestamped markdown filename for the candidate decision summary."""
    ticker = _safe_filename_part(card.get("ticker"), "marketflow")
    timeframe = _safe_filename_part(card.get("selected_timeframe"), "selected")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{ticker}_{timeframe}_candidate_decision_summary_{timestamp}.md"


def _analyst_review_notes_filename(packet: dict[str, Any] | None = None) -> str:
    """Return a timestamped markdown filename for manual analyst review notes."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if isinstance(packet, dict):
        packet_summary = packet.get("packet_summary") if isinstance(packet.get("packet_summary"), dict) else {}
        strategy_candidate = (
            packet.get("strategy_candidate") if isinstance(packet.get("strategy_candidate"), dict) else {}
        )
        ticker = packet_summary.get("ticker") or packet.get("ticker")
        timeframe = (
            packet_summary.get("selected_timeframe")
            or strategy_candidate.get("tf")
            or _nested_get(packet, ["pnf", "selection", "candidate_timeframe"])
            or _nested_get(packet, ["pnf", "selected_sidecar", "inferred_timeframe"])
            or _nested_get(packet, ["pnf", "selected_sidecar", "timeframe"])
        )
        if ticker and timeframe:
            safe_ticker = _safe_filename_part(ticker, "marketflow")
            safe_timeframe = _safe_filename_part(timeframe, "selected")
            return f"{safe_ticker}_{safe_timeframe}_analyst_review_notes_{timestamp}.md"
    return f"marketflow_analyst_review_notes_{timestamp}.md"


def _pnf_objective_review_markdown(card: dict[str, Any]) -> str:
    """Return an optional P&F objective review line for decision summaries."""
    if card.get("pnf_objective_quality") == "supportive_extended":
        return (
            "- Objective review: Supportive but extended. Treat as a longer-range P&F objective, "
            "not necessarily the immediate trade target.\n"
        )
    return ""


def _build_candidate_decision_summary_markdown(
    card: dict[str, Any],
    packet: dict[str, Any],
) -> str:
    """
    Build a concise markdown decision snapshot from the Candidate Decision Card data.

    This is a reporting artifact only. It must not create new scoring logic.
    """
    source_files = packet.get("source_files") if isinstance(packet.get("source_files"), dict) else {}
    alignment = card.get("alignment") if isinstance(card.get("alignment"), dict) else {}
    alignment_text = "matches" if alignment.get("matches") else "not matched"
    differences = alignment.get("differences") or []
    if differences:
        alignment_text = f"{alignment_text} ({', '.join(str(item) for item in differences)})"
    objective_review = _pnf_objective_review_markdown(card)

    return f"""# MarketFlow Candidate Decision Summary

## Metadata
- Created: {datetime.now().astimezone().isoformat(timespec="seconds")}
- Ticker: {_summary_value(card.get("ticker"))}
- Timeframe: {_summary_value(card.get("selected_timeframe"))}
- Source report folder: {_summary_value(source_files.get("report_dir"))}

## Trade Plan
- Entry: {_summary_value(card.get("trade_entry"))}
- Stop Loss: {_summary_value(card.get("trade_stop_loss"))}
- Take Profit: {_summary_value(card.get("trade_take_profit"))}
- Risk/Reward: {_summary_value(card.get("rr"))}

## Strategy Context
- Score: {_summary_value(card.get("strategy_score") or card.get("score"))}
- Wyckoff Phase: {_summary_value(card.get("phase"))}
- Wyckoff Event: {_summary_value(card.get("event"))}
- Trend: {_summary_value(card.get("trend"))}

## Monte Carlo Context
- Status: {_summary_value(card.get("monte_carlo_status"))}
- Model: {_summary_value(card.get("model"))}
- Paths: {_summary_value(card.get("paths"))}
- Horizon: {_summary_value(card.get("horizon_bars"))}
- TP First: {_summary_percent(card.get("pop_tp_first"))}
- SL First: {_summary_percent(card.get("p_sl_first"))}
- Neither: {_summary_percent(card.get("p_neither"))}
- R Mean: {_summary_value(card.get("R_mean"))}
- Alignment: {alignment_text}

## P&F Context
- Status: {_summary_value(card.get("pnf_status"))}
- Selected sidecar: {_summary_value(card.get("pnf_selected_sidecar"))}
- Matched by: {_summary_value(card.get("pnf_matched_by"))}
- Match score: {_summary_value(card.get("pnf_match_score"))}
- P&F gate: {_summary_value(card.get("pnf_gate"))}
- Objective: {_summary_value(card.get("pnf_objective"))}
- Objective direction: {_summary_value(card.get("pnf_objective_direction"))}
- Objective supports trade: {_summary_value(card.get("pnf_objective_supports_trade"))}
- Objective quality: {_summary_value(card.get("pnf_objective_quality"))}
- Objective R: {_summary_value(card.get("pnf_objective_r_multiple"))}
- Objective notes: {_summary_notes(card.get("pnf_objective_notes"))}
{objective_review}

## Eigen Diagnostic Context
- Available: {_summary_value(card.get("eigen_available"))}
- Matched by: {_summary_value(card.get("eigen_matched_by"))}
- Latest residual: {_summary_value(card.get("eigen_latest_residual"))}
- Latest coupling: {_summary_value(card.get("eigen_latest_coupling"))}
- Latest divergence: {_summary_value(card.get("eigen_latest_divergence"))}
- Divergence count: {_summary_value(card.get("eigen_divergence_count"))}
- Recent divergence count: {_summary_value(card.get("eigen_recent_divergence_count"))}
- Observation: {_summary_value(card.get("eigen_observation"))}
- Guardrail: Diagnostic only; does not change gates or scores.

## Analyst Packet Readiness
- POP gate: {_summary_value(card.get("pop_gate"))}
- P&F gate: {_summary_value(card.get("pnf_gate"))}
- Risk rank: {_summary_value(card.get("risk_rank"))}
- Data ready for analyst review: {_summary_value(card.get("ready_for_analyst"))}

## Workflow Notes
- This summary is a snapshot of existing Strategy, Monte Carlo, P&F, and Analyst Packet data.
- It is not financial advice.
- It does not change the underlying analysis.
"""


def _review_posture_label(review_posture: str) -> str:
    """Return safe display text for manual review posture."""
    posture = str(review_posture or "watch").strip()
    if posture == "approved":
        return "approved by reviewer"
    return posture.replace("_", " ")


def _manual_review_text(value: str, fallback: str) -> str:
    """Return reviewer-entered markdown text or a neutral placeholder."""
    text = str(value or "").strip()
    return text if text else fallback


def _build_analyst_review_notes_markdown(
    *,
    packet: dict[str, Any] | None = None,
    review_posture: str = "watch",
    conviction: str = "medium",
    reviewer_notes: str = "",
    follow_up_actions: str = "",
    source_context: dict[str, Any] | None = None,
) -> str:
    """
    Build a human analyst review notes markdown artifact.

    This is a manual review artifact only.
    It does not create signals or modify analytical logic.
    """
    context = source_context if isinstance(source_context, dict) else {}
    card = _candidate_decision_card_data(packet)
    source_files = packet.get("source_files") if isinstance(packet, dict) and isinstance(packet.get("source_files"), dict) else {}
    report_dir = context.get("report_dir") or source_files.get("report_dir")
    packet_summary = packet.get("packet_summary") if isinstance(packet, dict) and isinstance(packet.get("packet_summary"), dict) else {}

    return f"""# MarketFlow Analyst Review Notes

## Metadata
- Created: {datetime.now().astimezone().isoformat(timespec="seconds")}
- Ticker: {_summary_value(card.get("ticker") or (packet.get("ticker") if isinstance(packet, dict) else None))}
- Timeframe: {_summary_value(card.get("selected_timeframe"))}
- Source report folder: {_summary_value(report_dir)}
- Packet version: {_summary_value(packet.get("packet_version") if isinstance(packet, dict) else None)}
- Review posture: {_review_posture_label(review_posture)}
- Conviction: {_summary_value(conviction)}

## Trade Plan Context
- Entry: {_summary_value(card.get("trade_entry"))}
- Stop Loss: {_summary_value(card.get("trade_stop_loss"))}
- Take Profit: {_summary_value(card.get("trade_take_profit"))}
- Risk/Reward: {_summary_value(card.get("rr"))}
- Strategy score: {_summary_value(card.get("strategy_score") or card.get("score"))}
- Wyckoff phase: {_summary_value(card.get("phase"))}
- Wyckoff event: {_summary_value(card.get("event"))}

## Evidence Snapshot
- Candidate Decision Summary available: {_summary_value(context.get("candidate_decision_summary_available"))}
- POP gate: {_summary_value(card.get("pop_gate") or packet_summary.get("pop_gate"))}
- P&F gate: {_summary_value(card.get("pnf_gate") or packet_summary.get("pnf_gate"))}
- P&F objective quality: {_summary_value(card.get("pnf_objective_quality") or packet_summary.get("pnf_objective_quality"))}
- P&F objective direction: {_summary_value(card.get("pnf_objective_direction") or packet_summary.get("pnf_objective_direction"))}
- P&F supports trade: {_summary_value(card.get("pnf_objective_supports_trade") if card.get("pnf_objective_supports_trade") is not None else packet_summary.get("pnf_objective_supports_trade"))}
- Risk rank: {_summary_value(card.get("risk_rank") or packet_summary.get("risk_rank"))}
- Data ready for analyst review: {_summary_value(card.get("ready_for_analyst") if card else packet_summary.get("ready_for_analyst"))}
- Monte Carlo TP first: {_summary_percent(card.get("pop_tp_first"))}
- Monte Carlo SL first: {_summary_percent(card.get("p_sl_first"))}
- Eigen review summary available: {_summary_value(context.get("eigen_review_summary_available"))}
- Eigen latest residual: {_summary_value(card.get("eigen_latest_residual"))}
- Eigen latest coupling: {_summary_value(card.get("eigen_latest_coupling"))}
- Eigen latest divergence: {_summary_value(card.get("eigen_latest_divergence"))}
- Eigen recent divergence count: {_summary_value(card.get("eigen_recent_divergence_count"))}
- Analyst prompt available: {_summary_value(context.get("analyst_prompt_available"))}
- Analyst response available: {_summary_value(context.get("analyst_response_available"))}

## Human Review Notes
{_manual_review_text(reviewer_notes, "_No manual review notes entered._")}

## Follow-up Actions
{_manual_review_text(follow_up_actions, "_No follow-up actions entered._")}

## Review Guardrails
- This artifact records a human review note.
- It does not create a trade signal.
- It does not change Strategy Ranking, Monte Carlo, P&F, Eigen, or Analyst Packet results.
- Any trading decision remains outside the software and requires independent risk management.
"""


def _latest_artifact_by_kind(artifacts: list[dict[str, Any]], kind: str) -> dict[str, Any] | None:
    """Return the newest artifact matching a kind when discovery data is available."""
    matches = [artifact for artifact in artifacts if artifact.get("kind") == kind]
    if not matches:
        return None
    return sorted(matches, key=lambda artifact: str(artifact.get("modified") or ""), reverse=True)[0]


def _build_analyst_review_source_context(
    report_dir: str | None,
    *,
    analyst_prompt_available: bool = False,
    analyst_response_available: bool = False,
) -> dict[str, Any]:
    """Build compact source availability metadata for Analyst Review Notes."""
    artifacts = list_report_artifacts(report_dir) if report_dir else []
    candidate_summary = _latest_artifact_by_kind(artifacts, "candidate_decision_summary_md")
    eigen_summary = _latest_artifact_by_kind(artifacts, "eigen_review_summary_md")
    analyst_prompt = _latest_artifact_by_kind(artifacts, "analyst_prompt_md")
    analyst_response = _latest_artifact_by_kind(artifacts, "analyst_response_md")

    return {
        "candidate_decision_summary_available": bool(candidate_summary),
        "candidate_decision_summary_filename": candidate_summary.get("name") if candidate_summary else None,
        "eigen_review_summary_available": bool(eigen_summary),
        "eigen_review_summary_filename": eigen_summary.get("name") if eigen_summary else None,
        "analyst_prompt_available": bool(analyst_prompt or analyst_prompt_available),
        "analyst_prompt_filename": analyst_prompt.get("name") if analyst_prompt else None,
        "analyst_response_available": bool(analyst_response or analyst_response_available),
        "analyst_response_filename": analyst_response.get("name") if analyst_response else None,
        "report_dir": report_dir,
    }


def _review_source_rows(source_context: dict[str, Any]) -> list[dict[str, Any]]:
    """Return compact rows for review source status indicators."""
    definitions = [
        (
            "Candidate Decision Summary",
            "candidate_decision_summary_available",
            "candidate_decision_summary_filename",
        ),
        ("Eigen Review Summary", "eigen_review_summary_available", "eigen_review_summary_filename"),
        ("Analyst Prompt", "analyst_prompt_available", "analyst_prompt_filename"),
        ("Analyst Response", "analyst_response_available", "analyst_response_filename"),
    ]
    rows = []
    for label, available_key, filename_key in definitions:
        available = bool(source_context.get(available_key))
        rows.append(
            {
                "source": label,
                "status": "available" if available else "missing",
                "filename": source_context.get(filename_key) or ("session" if available else ""),
            }
        )
    return rows


def _render_analyst_review_notes_section(
    *,
    packet: dict[str, Any],
    report_dir: str | None,
    prompt_markdown: str | None = None,
    response_markdown: str | None = None,
) -> None:
    """Render manual Analyst Review Notes controls."""
    st.divider()
    st.subheader("Analyst Review Notes")

    source_context = _build_analyst_review_source_context(
        report_dir,
        analyst_prompt_available=bool(
            prompt_markdown
            or st.session_state.get("latest_analyst_prompt")
            or st.session_state.get("wyckoff_analyst_prompt")
            or st.session_state.get("wyckoff_analyst_prompt_text")
        ),
        analyst_response_available=bool(
            response_markdown
            or st.session_state.get("analyst_chat_response_markdown")
        ),
    )

    st.dataframe(_safe_dataframe_rows(_review_source_rows(source_context)), use_container_width=True, hide_index=True)

    posture = st.selectbox(
        "Review posture",
        options=["watch", "no_trade", "paper_trade", "small_position", "approved", "rejected"],
        index=0,
        key="analyst_review_notes_posture",
    )
    conviction = st.selectbox(
        "Conviction",
        options=["low", "medium", "high"],
        index=1,
        key="analyst_review_notes_conviction",
    )
    reviewer_notes = st.text_area(
        "Reviewer notes",
        height=180,
        key="analyst_review_notes_text",
    )
    follow_up_actions = st.text_area(
        "Follow-up actions",
        height=140,
        key="analyst_review_notes_follow_up_actions",
    )

    notes_markdown = _build_analyst_review_notes_markdown(
        packet=packet,
        review_posture=posture,
        conviction=conviction,
        reviewer_notes=reviewer_notes,
        follow_up_actions=follow_up_actions,
        source_context=source_context,
    )
    notes_filename = _analyst_review_notes_filename(packet)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download Analyst Review Notes",
            data=notes_markdown,
            file_name=notes_filename,
            mime="text/markdown",
            key="download_analyst_review_notes",
        )
    with col2:
        if st.button("Save Analyst Review Notes to report folder"):
            if not report_dir:
                st.warning("No report folder is available. Use Download instead.")
            else:
                try:
                    save_path = Path(report_dir) / notes_filename
                    if save_path.exists():
                        stem = save_path.stem
                        suffix = save_path.suffix
                        counter = 2
                        while save_path.exists():
                            save_path = Path(report_dir) / f"{stem}_{counter}{suffix}"
                            counter += 1
                    save_path.write_text(notes_markdown, encoding="utf-8")
                    st.success(f"Saved analyst review notes to `{save_path}`")
                    st.caption("Refresh Generated Artifacts to see this analyst review notes markdown file.")
                except Exception as exc:
                    st.error(f"Could not save analyst review notes: {exc}")


def _checklist_label(ok: bool, text: str) -> str:
    """Return a compact visible checklist line."""
    return f"{'✓' if ok else '•'} {text}"


def _decision_inputs_rows(card: dict[str, Any], mc_excluded: bool) -> list[dict[str, Any]]:
    """Return Candidate Decision Card source/status rows."""
    alignment = card.get("alignment") if isinstance(card.get("alignment"), dict) else {}
    pnf_note = card.get("pnf_selected_sidecar") or "No matched sidecar"
    if card.get("pnf_objective_quality") or card.get("pnf_objective_direction"):
        pnf_note = (
            f"{pnf_note}; direction={card.get('pnf_objective_direction') or 'unknown'}; "
            f"quality={card.get('pnf_objective_quality') or 'unknown'}"
        )
    mc_note = "Monte Carlo result is not included"
    if card.get("monte_carlo_status") == "aligned":
        mc_note = "Matches selected Strategy Ranking candidate"
    elif card.get("monte_carlo_status") == "manual scenario":
        mc_note = "Included as explicit manual scenario"
    elif mc_excluded:
        mc_note = "Mismatched result excluded"
    elif alignment.get("differences"):
        mc_note = "; ".join(alignment.get("differences") or [])

    return [
        {
            "component": "Strategy Ranking",
            "status": card.get("strategy_status"),
            "source": card.get("selected_timeframe"),
            "note": card.get("event") or "No candidate selected",
        },
        {
            "component": "Monte Carlo",
            "status": "mismatch excluded" if mc_excluded else card.get("monte_carlo_status"),
            "source": card.get("model"),
            "note": mc_note,
        },
        {
            "component": "P&F",
            "status": card.get("pnf_status"),
            "source": card.get("pnf_matched_by"),
            "note": pnf_note,
        },
        {
            "component": "Analyst Packet",
            "status": card.get("packet_status"),
            "source": "packet_summary",
            "note": f"data_ready_for_analyst_review={card.get('ready_for_analyst')}",
        },
    ]


def _render_candidate_decision_card(packet: dict[str, Any], mc_excluded: bool = False) -> None:
    """Render a compact candidate coherence summary for the Analyst Packet page."""
    card = _candidate_decision_card_data(packet)
    if not card:
        return

    st.subheader("Candidate Decision Card")
    cols = st.columns(4)
    with cols[0]:
        _display_optional_metric("Ticker", card.get("ticker"))
        _display_optional_metric("Timeframe", card.get("selected_timeframe"))
        _display_optional_metric("Entry", _format_number(card.get("trade_entry")))
    with cols[1]:
        _display_optional_metric("Stop Loss", _format_number(card.get("trade_stop_loss")))
        _display_optional_metric("Take Profit", _format_number(card.get("trade_take_profit")))
        _display_optional_metric("Strategy Score", _format_number(card.get("strategy_score")))
    with cols[2]:
        phase_event = " / ".join(str(item) for item in (card.get("phase"), card.get("event")) if item)
        _display_optional_metric("Wyckoff Phase/Event", phase_event or None)
        _display_optional_metric("MC TP First", _format_probability(card.get("pop_tp_first")))
        _display_optional_metric("MC SL First", _format_probability(card.get("p_sl_first")))
    with cols[3]:
        _display_optional_metric("POP Gate", card.get("pop_gate"))
        _display_optional_metric("P&F Gate", card.get("pnf_gate"))
        _display_optional_metric("P&F Quality", card.get("pnf_objective_quality"))
        _display_optional_metric("Risk Rank", card.get("risk_rank"))
        _display_optional_metric("Data Ready for Analyst Review", card.get("ready_for_analyst"))

    st.markdown("#### Alignment Checklist")
    checklist = [
        _checklist_label(card.get("strategy_status") == "available", "Strategy candidate selected"),
        _checklist_label(card.get("monte_carlo_status") == "aligned", "Monte Carlo matches selected candidate"),
        _checklist_label(card.get("pnf_status") == "matched", "P&F sidecar matched selected candidate/timeframe"),
        _checklist_label(card.get("packet_status") == "ready", "Analyst Packet ready"),
    ]
    for item in checklist:
        st.write(item)

    if card.get("monte_carlo_status") == "missing":
        st.warning("Monte Carlo result is not included in this packet.")
    if mc_excluded:
        st.warning("Mismatched Monte Carlo result was excluded from this packet.")
    if card.get("manual_scenario") or card.get("monte_carlo_status") == "manual scenario":
        st.warning("Monte Carlo is included as an explicit manual scenario.")
    if card.get("pnf_status") == "missing":
        st.warning("No matched P&F sidecar is included.")
    if card.get("pnf_objective_supports_trade") is False:
        st.warning("P&F objective contradicts the selected long setup.")
    if card.get("pnf_objective_quality") == "supportive_extended":
        st.warning("P&F objective supports the selected long setup, but it is extended/far from current price.")
    if _safe_float(card.get("pnf_objective_r_multiple")) is not None and _safe_float(card.get("pnf_objective_r_multiple")) < 0:
        st.warning("P&F objective R is negative.")
    objective_distance_pct = _safe_float(card.get("pnf_objective_distance_pct"))
    objective_r_multiple = _safe_float(card.get("pnf_objective_r_multiple"))
    if card.get("pnf_objective_quality") != "supportive_extended" and objective_distance_pct is not None and abs(objective_distance_pct) > 0.75:
        st.warning("P&F objective is unusually far from last price.")
    if objective_r_multiple is not None and abs(objective_r_multiple) > 10:
        st.warning("P&F objective R is unusually large.")

    st.markdown("#### Eigen Diagnostic Context")
    eigen_cols = st.columns(4)
    with eigen_cols[0]:
        _display_optional_metric("Available", card.get("eigen_available"))
        _display_optional_metric("Matched by", card.get("eigen_matched_by"))
    with eigen_cols[1]:
        _display_optional_metric("Latest residual", _format_number(card.get("eigen_latest_residual"), decimals=4))
        _display_optional_metric("Latest coupling", _format_number(card.get("eigen_latest_coupling"), decimals=4))
    with eigen_cols[2]:
        _display_optional_metric("Latest divergence", card.get("eigen_latest_divergence"))
        _display_optional_metric("Divergence count", card.get("eigen_divergence_count"))
    with eigen_cols[3]:
        _display_optional_metric("Recent divergence count", card.get("eigen_recent_divergence_count"))
    _display_optional_metric("Observation", card.get("eigen_observation"))
    st.caption("Eigen context is diagnostic only and does not change gates or scores.")

    st.markdown("#### P&F Objective Interpretation")
    st.dataframe(
        _safe_dataframe_rows([
            {
                "objective_direction": card.get("pnf_objective_direction"),
                "objective_quality": card.get("pnf_objective_quality"),
                "supports_trade": card.get("pnf_objective_supports_trade"),
                "objective_r_multiple": card.get("pnf_objective_r_multiple"),
                "objective_distance_pct": card.get("pnf_objective_distance_pct"),
                "objective_review": (
                    "Supportive but extended. Treat as a longer-range P&F objective, not necessarily the immediate trade target."
                    if card.get("pnf_objective_quality") == "supportive_extended"
                    else ""
                ),
                "objective_notes": "; ".join(card.get("pnf_objective_notes") or []),
            }
        ]),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Decision Inputs")
    st.dataframe(
        _safe_dataframe_rows(_decision_inputs_rows(card, mc_excluded)),
        use_container_width=True,
        hide_index=True,
    )


def _sync_monte_carlo_prefill(prefill: dict[str, Any] | None) -> None:
    """Apply candidate prefill values to Monte Carlo widgets deterministically."""
    token = _prefill_token(prefill)
    if token is None:
        return
    should_apply = (
        token != st.session_state.get("monte_carlo_prefill_token")
        or st.session_state.get("monte_carlo_level_source") != "strategy_ranking"
    )
    if not should_apply:
        return

    entry = _safe_float(prefill.get("entry"))
    stop_loss = _safe_float(prefill.get("stop_loss"))
    take_profit = _safe_float(prefill.get("take_profit"))
    if entry is not None:
        st.session_state.monte_carlo_entry_value = entry
    if stop_loss is not None:
        st.session_state.monte_carlo_stop_loss_value = stop_loss
    if take_profit is not None:
        st.session_state.monte_carlo_take_profit_value = take_profit

    st.session_state.pop("monte_carlo_csv_file", None)
    st.session_state.pop("monte_carlo_manual_csv", None)
    st.session_state.monte_carlo_level_source = "strategy_ranking"
    st.session_state.monte_carlo_prefill_token = token
    st.session_state.monte_carlo_result = None
    st.session_state.latest_monte_carlo_result = None


def _candidate_csv_path(prefill: dict[str, Any] | None) -> str | None:
    """Return an existing candidate CSV path, or None if unavailable."""
    if not prefill or not prefill.get("csv"):
        return None
    path = Path(str(prefill["csv"]))
    return str(path) if path.exists() and path.is_file() else None


def _render_monte_carlo_error(monte_carlo_result: dict[str, Any]) -> None:
    """Render Monte Carlo service errors with traceback hidden by default."""
    error_type = monte_carlo_result.get("error_type")
    error_message = monte_carlo_result.get("error") or "Monte Carlo simulation failed."
    if error_type:
        st.error(f"{error_type}: {error_message}")
    else:
        st.error(error_message)

    if monte_carlo_result.get("traceback"):
        with st.expander("Monte Carlo error details"):
            st.code(monte_carlo_result["traceback"], language="python")


def _format_file_size(size_bytes: int | None) -> str:
    """Return a compact display string for a byte count."""
    if size_bytes is None:
        return "Unknown"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def _read_text_file(path: str, max_bytes: int = 8_000_000) -> tuple[str | None, str | None]:
    """
    Return (text, error). Used for preview/download of local generated files.
    """
    try:
        file_path = Path(path)
        if not file_path.exists() or not file_path.is_file():
            return None, "File is no longer available."
        if file_path.stat().st_size > max_bytes:
            return None, f"File is larger than {_format_file_size(max_bytes)}."
        return file_path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        return None, "File could not be read as UTF-8 text."
    except Exception as exc:
        return None, f"Could not read file: {exc}"


def _output_files_by_kind(output_files: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    """Return output files matching a Monte Carlo output kind."""
    return [
        item
        for item in output_files
        if isinstance(item, dict) and item.get("kind") == kind and item.get("path")
    ]


def _render_monte_carlo_download(
    item: dict[str, Any],
    label: str,
    mime: str,
    key_prefix: str,
) -> None:
    """Render a download button for a generated Monte Carlo text file."""
    path = str(item.get("path") or "")
    text, error = _read_text_file(path, max_bytes=32_000_000)
    if error:
        st.warning(f"{label}: {error}")
        return
    st.download_button(
        label,
        data=text or "",
        file_name=item.get("name") or Path(path).name,
        mime=mime,
        key=f"{key_prefix}_{Path(path).name}",
    )


def _render_monte_carlo_output_files(monte_carlo_result: dict[str, Any]) -> None:
    """Render Monte Carlo output files saved by the simulator."""
    st.subheader("Generated Monte Carlo files")
    st.caption("HTML plots can be previewed below or downloaded and opened in your browser.")

    csv_path = monte_carlo_result.get("csv_path") or ""
    if st.button("Refresh Monte Carlo output files"):
        monte_carlo_result["output_files"] = list_monte_carlo_outputs(csv_path)

    output_files = monte_carlo_result.get("output_files") or []
    if not output_files:
        st.info("No Monte Carlo output files were found beside the selected CSV.")
        return

    rows = [
        {
            "kind": item.get("kind"),
            "name": item.get("name"),
            "modified": item.get("modified"),
            "size": _format_file_size(item.get("size_bytes")),
            "path": item.get("path"),
        }
        for item in output_files
    ]
    st.dataframe(_safe_dataframe_rows(rows), use_container_width=True, hide_index=True)

    html_files = [
        item
        for item in output_files
        if item.get("kind") in {"paths_html", "hits_html"}
        and str(item.get("path") or "").lower().endswith(".html")
    ]
    if html_files:
        selected_html = st.selectbox(
            "Preview Monte Carlo HTML plot",
            options=html_files,
            format_func=lambda item: item.get("name") or Path(str(item.get("path"))).name,
        )
        if st.button("Preview selected plot"):
            path = str(selected_html.get("path") or "")
            html_text, error = _read_text_file(path)
            if error:
                st.warning(f"{error} Download the file or open it externally instead.")
            else:
                components.html(html_text or "", height=700, scrolling=True)

    paths_html = _output_files_by_kind(output_files, "paths_html")
    hits_html = _output_files_by_kind(output_files, "hits_html")
    summaries = _output_files_by_kind(output_files, "summary_json")

    download_cols = st.columns(3)
    with download_cols[0]:
        if paths_html:
            _render_monte_carlo_download(
                paths_html[0],
                "Download paths plot HTML",
                "text/html",
                "download_mc_paths",
            )
    with download_cols[1]:
        if hits_html:
            _render_monte_carlo_download(
                hits_html[0],
                "Download hits plot HTML",
                "text/html",
                "download_mc_hits",
            )
    with download_cols[2]:
        if summaries:
            _render_monte_carlo_download(
                summaries[0],
                "Download summary JSON",
                "application/json",
                "download_mc_summary",
            )


def _render_monte_carlo_results(monte_carlo_result: dict[str, Any] | None) -> None:
    """Render Monte Carlo output metrics and raw result data."""
    if not monte_carlo_result:
        st.info("Select a CSV and click Run Monte Carlo to simulate a single trade.")
        return

    if not monte_carlo_result.get("success"):
        _render_monte_carlo_error(monte_carlo_result)
        return

    result = monte_carlo_result.get("result") or {}
    params = result.get("params") or {}
    metrics = result.get("metrics_from_entry") or result.get("metrics_from_now") or {}

    st.success("Monte Carlo simulation completed.")
    st.caption(f"CSV: `{Path(monte_carlo_result.get('csv_path') or '').name}`")
    if monte_carlo_result.get("source") == "strategy_ranking":
        st.caption("Source: Strategy Ranking candidate")
    alignment = monte_carlo_result.get("alignment")
    if isinstance(alignment, dict):
        st.markdown("#### Monte Carlo Alignment")
        st.dataframe(_safe_dataframe_rows(_alignment_display_rows(alignment)), use_container_width=True, hide_index=True)
        if alignment.get("matches"):
            st.caption("Monte Carlo result matches the selected Strategy Ranking candidate.")
        else:
            st.warning(
                "Monte Carlo inputs differ from the selected Strategy Ranking candidate. "
                "This is allowed for manual scenario testing, but Analyst Packet will treat it as a modified MC scenario."
            )

    join_metadata = monte_carlo_result.get("join_metadata")
    if not isinstance(join_metadata, dict):
        join_metadata = result.get("join_metadata") if isinstance(result.get("join_metadata"), dict) else {}
    summary_enrichment = monte_carlo_result.get("summary_enrichment")
    st.markdown("#### Monte Carlo Join Metadata")
    if isinstance(summary_enrichment, dict):
        if summary_enrichment.get("success"):
            st.caption(f"Summary JSON enriched: `{summary_enrichment.get('filename')}`")
        elif summary_enrichment.get("warnings"):
            st.info("Summary JSON enrichment: " + "; ".join(str(item) for item in summary_enrichment.get("warnings") or []))
        elif summary_enrichment.get("errors"):
            st.warning("Summary JSON enrichment failed: " + "; ".join(str(item) for item in summary_enrichment.get("errors") or []))
    if join_metadata:
        fields = (
            "ticker",
            "timeframe",
            "source_csv",
            "candidate_snapshot_file",
            "signal_row_index",
            "signal_timestamp",
            "join_key_preferred",
            "join_key_secondary",
        )
        st.dataframe(
            _safe_dataframe_rows([{"field": field, "value": join_metadata.get(field)} for field in fields]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("No Monte Carlo join metadata is available for this run.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _display_optional_metric("Model", params.get("model"))
        _display_optional_metric("Entry", _format_number(params.get("entry")))
    with col2:
        _display_optional_metric("Stop Loss", _format_number(params.get("sl")))
        _display_optional_metric("Take Profit", _format_number(params.get("tp")))
    with col3:
        _display_optional_metric("Spot S0", _format_number(_nested_get(result, ["spot", "S0_now"])))
        _display_optional_metric(
            "Calibration Model",
            _nested_get(result, ["calibration", "model_used"]),
        )
    with col4:
        _display_optional_metric("TP First", _format_probability(metrics.get("pop_tp_first")))
        _display_optional_metric("SL First", _format_probability(metrics.get("p_sl_first")))

    col5, col6 = st.columns(2)
    with col5:
        _display_optional_metric("Median Bars to TP", metrics.get("t_hit_tp_median"))
    with col6:
        _display_optional_metric("Median Bars to SL", metrics.get("t_hit_sl_median"))

    _render_monte_carlo_output_files(monte_carlo_result)
    with st.expander("Raw Monte Carlo result"):
        st.json(result)


def _render_monte_carlo(result: dict[str, Any] | None) -> None:
    """Render the Monte Carlo tab."""
    prefill = st.session_state.get("monte_carlo_prefill")
    candidate_csv = _candidate_csv_path(prefill)
    _sync_monte_carlo_prefill(prefill)

    if prefill:
        ticker = prefill.get("ticker") or "candidate"
        timeframe_label = prefill.get("tf") or "unknown timeframe"
        st.info(f"Using candidate from Strategy Ranking: {ticker} {timeframe_label}")
        if st.button("Clear candidate prefill"):
            for key in [
                "monte_carlo_prefill",
                "monte_carlo_prefill_token",
                "monte_carlo_entry_value",
                "monte_carlo_stop_loss_value",
                "monte_carlo_take_profit_value",
                "monte_carlo_level_source",
                "monte_carlo_manual_csv",
            ]:
                st.session_state.pop(key, None)
            st.session_state.monte_carlo_result = None
            st.session_state.latest_monte_carlo_result = None
            st.rerun()

        if prefill.get("csv") and not candidate_csv:
            st.warning("The selected candidate CSV no longer exists. Please select a CSV manually.")

    report_dir = None
    if result and result.get("output_dir"):
        report_dir = _report_dir_from_result(result, "Run an analysis or load a report first.")
        if not report_dir and not candidate_csv:
            return
    elif not candidate_csv:
        st.info("Run an analysis, load a report, or send a strategy candidate first.")
        return

    csv_files = _annotated_csv_files_for_report(report_dir) if report_dir else []
    csv_options = list(csv_files)
    if candidate_csv and not any(_path_matches(candidate_csv, path) for path in csv_options):
        csv_options.insert(0, candidate_csv)

    if prefill and candidate_csv and not any(_path_matches(candidate_csv, path) for path in csv_files):
        st.caption("Using CSV from selected strategy candidate.")

    if not csv_files:
        if not candidate_csv:
            st.info("No annotated CSV files found for Monte Carlo simulation.")
            st.caption("Run Analysis first, then return here to select a generated OHLC CSV.")
            return

    selected_index = 0
    if candidate_csv:
        for index, csv_path in enumerate(csv_options):
            if _path_matches(candidate_csv, csv_path):
                selected_index = index
                break

    selected_csv = st.selectbox(
        "Monte Carlo CSV file",
        options=csv_options,
        index=selected_index,
        format_func=lambda path: Path(path).name,
        key="monte_carlo_csv_file",
    )
    timeframe = prefill.get("tf") if candidate_csv and _path_matches(candidate_csv, selected_csv) else None
    timeframe = timeframe or infer_timeframe_from_csv_name(selected_csv)
    _render_csv_file_context(selected_csv)
    if prefill and prefill.get("tf") and timeframe == prefill.get("tf"):
        st.caption(f"Timeframe from selected strategy candidate: `{timeframe}`")

    latest_close = load_latest_close(selected_csv)
    if latest_close is not None:
        st.caption(f"Latest close loaded from CSV: `{latest_close:.4f}`")
    else:
        st.warning("Could not load the latest close from this CSV. Enter trade levels manually.")

    default_entry, default_stop, default_take = _default_trade_levels(latest_close)
    if "monte_carlo_entry_value" not in st.session_state:
        st.session_state.monte_carlo_entry_value = float(default_entry)
    if "monte_carlo_stop_loss_value" not in st.session_state:
        st.session_state.monte_carlo_stop_loss_value = float(default_stop)
    if "monte_carlo_take_profit_value" not in st.session_state:
        st.session_state.monte_carlo_take_profit_value = float(default_take)

    if not candidate_csv and st.session_state.get("monte_carlo_manual_csv") != selected_csv:
        st.session_state.monte_carlo_entry_value = float(default_entry)
        st.session_state.monte_carlo_stop_loss_value = float(default_stop)
        st.session_state.monte_carlo_take_profit_value = float(default_take)
        st.session_state.monte_carlo_manual_csv = selected_csv
        st.session_state.monte_carlo_level_source = "manual"

    col1, col2, col3 = st.columns(3)
    with col1:
        entry = st.number_input(
            "Entry",
            min_value=0.0,
            step=0.01,
            format="%.4f",
            key="monte_carlo_entry_value",
        )
    with col2:
        stop_loss = st.number_input(
            "Stop Loss",
            min_value=0.0,
            step=0.01,
            format="%.4f",
            key="monte_carlo_stop_loss_value",
        )
    with col3:
        take_profit = st.number_input(
            "Take Profit",
            min_value=0.0,
            step=0.01,
            format="%.4f",
            key="monte_carlo_take_profit_value",
        )

    prefill_matches_selected_csv = bool(prefill and candidate_csv and _path_matches(candidate_csv, selected_csv))
    if prefill_matches_selected_csv:
        st.markdown("#### Strategy Candidate Prefill")
        st.dataframe(
            _safe_dataframe_rows([
                {
                    "ticker": prefill.get("ticker"),
                    "timeframe": prefill.get("tf"),
                    "CSV": Path(str(prefill.get("csv") or "")).name,
                    "entry": prefill.get("entry"),
                    "stop_loss": prefill.get("stop_loss"),
                    "take_profit": prefill.get("take_profit"),
                    "source": prefill.get("source"),
                }
            ]),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("#### Current Monte Carlo Inputs")
        st.dataframe(
            _safe_dataframe_rows([
                {
                    "entry": entry,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                }
            ]),
            use_container_width=True,
            hide_index=True,
        )
        if not (
            _numbers_match(prefill.get("entry"), entry)
            and _numbers_match(prefill.get("stop_loss"), stop_loss)
            and _numbers_match(prefill.get("take_profit"), take_profit)
        ):
            st.warning(
                "Monte Carlo inputs differ from the selected Strategy Ranking candidate. "
                "This is allowed for manual scenario testing, but Analyst Packet will treat it as a modified MC scenario."
            )

    col4, col5, col6, col7 = st.columns(4)
    with col4:
        model = st.selectbox("Model", options=MONTE_CARLO_MODELS, index=0)
        st.caption("Bootstrap is the recommended default. GARCH requires optional package `arch`.")
    with col5:
        paths = st.number_input("Paths", min_value=1000, max_value=50000, value=10000, step=1000)
    with col6:
        horizon = st.number_input("Horizon", min_value=1, max_value=250, value=20, step=1)
    with col7:
        block_len = st.number_input("Block Length", min_value=1, max_value=100, value=8, step=1)

    seed = st.number_input("Seed", value=42, step=1)
    save_plots = st.checkbox("Save plots", value=True)
    st.caption("Saved plots are written as HTML files beside the selected CSV and listed below after a run.")

    if st.button("Run Monte Carlo"):
        validation_errors = []
        if not Path(selected_csv).exists():
            validation_errors.append("Selected CSV file does not exist.")
        if entry <= 0:
            validation_errors.append("Entry must be greater than zero.")
        if stop_loss >= entry:
            validation_errors.append("Stop loss must be below entry.")
        if take_profit <= entry:
            validation_errors.append("Take profit must be above entry.")
        if paths <= 0:
            validation_errors.append("Paths must be positive.")
        if horizon <= 0:
            validation_errors.append("Horizon must be positive.")

        if validation_errors:
            for message in validation_errors:
                st.warning(message)
        else:
            source_candidate = st.session_state.get("selected_strategy_candidate")
            if not isinstance(source_candidate, dict):
                source_candidate = (prefill or {}).get("source_candidate") if isinstance(prefill, dict) else None
            inputs_match_prefill = (
                prefill_matches_selected_csv
                and _numbers_match((prefill or {}).get("entry"), entry)
                and _numbers_match((prefill or {}).get("stop_loss"), stop_loss)
                and _numbers_match((prefill or {}).get("take_profit"), take_profit)
            )
            trade_plan = {
                "ticker": (prefill or {}).get("ticker") or (result or {}).get("ticker"),
                "csv": selected_csv,
                "tf": timeframe,
                "entry": float(entry),
                "stop_loss": float(stop_loss),
                "take_profit": float(take_profit),
                "source": "strategy_ranking" if inputs_match_prefill else "manual",
            }
            candidate_snapshot, candidate_snapshot_file = _candidate_snapshot_context_for_monte_carlo(
                selected_csv=selected_csv,
                timeframe=timeframe,
                entry=entry,
                stop_loss=stop_loss,
                take_profit=take_profit,
            )
            with st.spinner("Running Monte Carlo simulation..."):
                mc_result = run_monte_carlo_for_csv(
                    csv_path=selected_csv,
                    entry=float(entry),
                    stop_loss=float(stop_loss),
                    take_profit=float(take_profit),
                    timeframe=timeframe,
                    model=model,
                    paths=int(paths),
                    horizon=int(horizon),
                    block_len=int(block_len),
                    seed=int(seed),
                    save_plots=save_plots,
                    trade_plan=trade_plan,
                    candidate_snapshot=candidate_snapshot,
                    candidate_snapshot_file=candidate_snapshot_file,
                    source_report_dir=report_dir,
                )
                mc_result["trade_plan"] = trade_plan
                mc_result["source_candidate"] = source_candidate if isinstance(source_candidate, dict) else None
                mc_result["alignment"] = _monte_carlo_alignment(source_candidate, mc_result)
                mc_result["matches_strategy_candidate"] = bool(mc_result["alignment"].get("matches"))
                mc_result["source"] = trade_plan["source"]
                st.session_state.monte_carlo_result = mc_result
                st.session_state.latest_monte_carlo_result = st.session_state.monte_carlo_result

    _render_monte_carlo_results(st.session_state.get("monte_carlo_result"))


def _strategy_candidate_for_packet() -> dict[str, Any] | None:
    """Return the best available strategy candidate context for analyst packets."""
    candidate = st.session_state.get("selected_strategy_candidate")
    if isinstance(candidate, dict):
        return candidate

    candidate = st.session_state.get("latest_strategy_candidate")
    if isinstance(candidate, dict):
        return candidate

    prefill = st.session_state.get("monte_carlo_prefill")
    if isinstance(prefill, dict):
        return {
            "ticker": prefill.get("ticker"),
            "csv": prefill.get("csv"),
            "tf": prefill.get("tf"),
            "close": prefill.get("entry"),
            "sl": prefill.get("stop_loss"),
            "tp": prefill.get("take_profit"),
        }
    return None


def _render_analyst_packet(result: dict[str, Any] | None) -> None:
    """Render the Analyst Packet Builder tab."""
    st.write(
        "This builds structured context for the future Wyckoff Volume Analyst. "
        "It does not call an LLM yet."
    )

    report_json = result.get("report_json") if result else None
    summary_text = result.get("summary_text") or result.get("narrative") if result else None
    report_dir = result.get("output_dir") if result else None
    strategy_candidate = _strategy_candidate_for_packet()
    ticker = (
        strategy_candidate.get("ticker")
        if isinstance(strategy_candidate, dict) and strategy_candidate.get("ticker")
        else result.get("ticker") if result else None
    )
    monte_carlo_result = (
        st.session_state.get("latest_monte_carlo_result")
        or st.session_state.get("monte_carlo_result")
    )
    monte_carlo_result_for_packet = monte_carlo_result
    monte_carlo_alignment = None
    allow_mismatched_mc = False

    if not ticker and strategy_candidate:
        ticker = strategy_candidate.get("ticker")

    if not ticker and not report_json:
        st.info("Load a report, run analysis, or select a strategy candidate first.")
        return

    st.caption(f"Ticker context: `{ticker or 'UNKNOWN'}`")
    if report_dir:
        st.caption(f"Report directory: `{report_dir}`")
    if strategy_candidate:
        st.caption("Strategy candidate context is available.")
    if monte_carlo_result and monte_carlo_result.get("success"):
        st.caption("Latest Monte Carlo result is available.")
        if isinstance(strategy_candidate, dict):
            monte_carlo_alignment = _monte_carlo_alignment(strategy_candidate, monte_carlo_result)
            if monte_carlo_alignment.get("matches"):
                st.caption("Latest Monte Carlo result matches the selected Strategy Ranking candidate.")
            else:
                st.warning(
                    "Latest Monte Carlo result does not match the selected Strategy Ranking candidate. "
                    "Re-run Monte Carlo from the selected candidate or continue without MC."
                )
                allow_mismatched_mc = st.checkbox(
                    "Allow mismatched Monte Carlo result as manual scenario",
                    value=False,
                    key="allow_mismatched_monte_carlo_packet",
                )
                if not allow_mismatched_mc:
                    monte_carlo_result_for_packet = None
                else:
                    monte_carlo_result_for_packet = {
                        **monte_carlo_result,
                        "alignment": monte_carlo_alignment,
                        "matches_strategy_candidate": False,
                        "manual_scenario": True,
                    }
        elif isinstance(monte_carlo_result, dict):
            monte_carlo_alignment = monte_carlo_result.get("alignment")

    if st.button("Build Analyst Packet", type="primary"):
        packet = build_analyst_packet(
            ticker=ticker or "",
            report_json=report_json,
            summary_text=summary_text,
            report_dir=report_dir,
            strategy_candidate=strategy_candidate,
            monte_carlo_result=monte_carlo_result_for_packet,
            profile=load_default_analyst_profile(),
        )
        st.session_state.analyst_packet = packet
        st.session_state.latest_analyst_packet = packet
        st.session_state.analyst_packet_json = packet_to_pretty_json(packet)

    packet = st.session_state.get("analyst_packet")
    pretty_json = st.session_state.get("analyst_packet_json")
    if not packet:
        st.info("Click Build Analyst Packet to generate structured analyst context.")
        return

    packet_summary = packet.get("packet_summary") or {}
    strategy_context = packet.get("strategy_candidate") or {}
    packet_monte_carlo = packet.get("monte_carlo")
    monte_carlo_context = packet_monte_carlo or {}
    pnf_context = packet.get("pnf") or {}
    mc_excluded_for_card = False
    if isinstance(strategy_candidate, dict) and isinstance(monte_carlo_result, dict) and monte_carlo_result.get("success"):
        current_alignment = _monte_carlo_alignment(strategy_candidate, monte_carlo_result)
        mc_excluded_for_card = bool(
            not current_alignment.get("matches") and not isinstance(packet_monte_carlo, dict)
        )

    _render_candidate_decision_card(packet, mc_excluded=mc_excluded_for_card)
    decision_card = _candidate_decision_card_data(packet)
    if decision_card:
        summary_markdown = _build_candidate_decision_summary_markdown(decision_card, packet)
        summary_filename = _candidate_decision_summary_filename(decision_card)
        st.download_button(
            "Download Decision Summary",
            data=summary_markdown,
            file_name=summary_filename,
            mime="text/markdown",
        )
        if st.button("Save Decision Summary to report folder"):
            if not report_dir:
                st.warning("No report directory is available. Use Download instead.")
            else:
                try:
                    save_path = Path(report_dir) / summary_filename
                    if save_path.exists():
                        stem = save_path.stem
                        suffix = save_path.suffix
                        counter = 2
                        while save_path.exists():
                            save_path = Path(report_dir) / f"{stem}_{counter}{suffix}"
                            counter += 1
                    save_path.write_text(summary_markdown, encoding="utf-8")
                    st.success(f"Saved decision summary to `{save_path}`")
                    st.caption("Refresh Generated Artifacts to see this decision summary.")
                except Exception as exc:
                    st.error(f"Could not save decision summary: {exc}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _display_optional_metric("Ticker", packet_summary.get("ticker") or packet.get("ticker"))
        _display_optional_metric(
            "Current Price",
            _format_number(packet_summary.get("current_price")),
        )
    with col2:
        _display_optional_metric("Strategy Score", _format_number(strategy_context.get("score")))
        _display_optional_metric("Strategy TF", strategy_context.get("tf"))
    with col3:
        _display_optional_metric("Trade Entry", _format_number(packet_summary.get("trade_entry")))
        _display_optional_metric("Trade Stop", _format_number(packet_summary.get("trade_stop_loss")))
    with col4:
        _display_optional_metric("Trade Take Profit", _format_number(packet_summary.get("trade_take_profit")))
        _display_optional_metric("POP Gate", packet_summary.get("pop_gate"))
        _display_optional_metric("Risk Rank", packet_summary.get("risk_rank"))

    col5, col6 = st.columns(2)
    with col5:
        _display_optional_metric("MC TP First", _format_probability(monte_carlo_context.get("pop_tp_first")))
    with col6:
        _display_optional_metric("MC SL First", _format_probability(monte_carlo_context.get("p_sl_first")))

    st.markdown("#### Monte Carlo Alignment")
    packet_alignment = monte_carlo_context.get("alignment") if isinstance(monte_carlo_context, dict) else None
    if isinstance(packet_alignment, dict):
        st.dataframe(
            _safe_dataframe_rows(_alignment_display_rows(packet_alignment)),
            use_container_width=True,
            hide_index=True,
        )
        if packet_alignment.get("matches"):
            st.caption("Monte Carlo alignment: matches yes.")
        else:
            st.warning(
                "Monte Carlo alignment: matches no. "
                f"Differences: {', '.join(packet_alignment.get('differences') or []) or 'unknown'}."
            )
    else:
        st.info("No matching Monte Carlo result was included in this packet.")

    if packet_summary.get("pnf_available"):
        pnf_col1, pnf_col2, pnf_col3, pnf_col4 = st.columns(4)
        with pnf_col1:
            _display_optional_metric("P&F Available", packet_summary.get("pnf_available"))
        with pnf_col2:
            _display_optional_metric("P&F Gate", packet_summary.get("pnf_gate"))
        with pnf_col3:
            _display_optional_metric(
                "Best P&F Objective",
                _format_number(packet_summary.get("best_pnf_objective")),
            )
        with pnf_col4:
            _display_optional_metric(
                "Best P&F R",
                _format_number(packet_summary.get("best_pnf_objective_r")),
            )

        selection = pnf_context.get("selection") if isinstance(pnf_context, dict) else {}
        selected_sidecar = (pnf_context.get("selected_sidecar") if isinstance(pnf_context, dict) else {}) or {}
        objective_interpretation = (
            pnf_context.get("objective_interpretation")
            if isinstance(pnf_context.get("objective_interpretation"), dict)
            else {}
        )
        if isinstance(selection, dict) and selection.get("selected_filename"):
            st.markdown("#### P&F Traceability")
            st.dataframe(
                _safe_dataframe_rows([
                    {
                        "selected_sidecar": selection.get("selected_filename"),
                        "match_score": selection.get("match_score"),
                        "matched_by": selection.get("matched_by"),
                        "match_reasons": "; ".join(selection.get("match_reasons") or []),
                        "candidate_timeframe": selection.get("candidate_timeframe"),
                        "candidate_csv": Path(str(selection.get("candidate_csv") or "")).name,
                        "source_type": selected_sidecar.get("source_type"),
                        "source_warning": selected_sidecar.get("source_warning"),
                        "sidecar_timeframe": selected_sidecar.get("inferred_timeframe") or selected_sidecar.get("timeframe"),
                        "box_size": selected_sidecar.get("box_size"),
                        "reversal": selected_sidecar.get("reversal"),
                        "objective": selected_sidecar.get("objective"),
                        "objective_direction": objective_interpretation.get("objective_direction") or selected_sidecar.get("objective_direction"),
                        "objective_quality": objective_interpretation.get("objective_quality") or selected_sidecar.get("objective_quality"),
                        "objective_supports_trade": (
                            objective_interpretation.get("objective_supports_trade")
                            if "objective_supports_trade" in objective_interpretation
                            else selected_sidecar.get("objective_supports_trade")
                        ),
                        "objective_distance_pct": objective_interpretation.get("objective_distance_pct") or selected_sidecar.get("objective_distance_pct"),
                        "objective_r_multiple": selected_sidecar.get("objective_r_multiple"),
                        "objective_notes": "; ".join(objective_interpretation.get("notes") or selected_sidecar.get("objective_notes") or []),
                    }
                ]),
                use_container_width=True,
                hide_index=True,
            )
            if len(pnf_context.get("sidecars") or []) > 1 and (selection.get("match_score") or 0) < 50:
                st.warning("Multiple P&F sidecars found. Verify selected sidecar before relying on P&F gate.")

        sidecars = pnf_context.get("sidecars") or []
        if sidecars:
            st.caption("P&F sidecars can also be visualized in the Charts tab.")
            with st.expander("P&F sidecars"):
                st.dataframe(
                    _safe_dataframe_rows([
                        {
                            "filename": item.get("filename"),
                            "source_csv": item.get("source_csv"),
                            "source_type": item.get("source_type"),
                            "source_warning": item.get("source_warning"),
                            "timeframe": item.get("inferred_timeframe") or item.get("timeframe"),
                            "direction": item.get("direction"),
                            "match_score": item.get("match_score"),
                            "matched_by": item.get("matched_by"),
                            "breakout_level": item.get("breakout_level"),
                            "objective": item.get("objective"),
                            "objective_direction": item.get("objective_direction"),
                            "objective_quality": item.get("objective_quality"),
                            "objective_supports_trade": item.get("objective_supports_trade"),
                            "objective_distance_pct": item.get("objective_distance_pct"),
                            "objective_r_multiple": item.get("objective_r_multiple"),
                            "objective_notes": "; ".join(item.get("objective_notes") or []),
                            "distance_to_objective_pct": item.get("distance_to_objective_pct"),
                        }
                        for item in sidecars
                        if isinstance(item, dict)
                    ]),
                    use_container_width=True,
                    hide_index=True,
                )
    else:
        st.warning("No P&F sidecars found; P&F gate remains pending.")
        st.caption("Generate P&F sidecars from the Charts tab if you want the P&F gate to be evaluated.")

    st.caption(f"Data ready for analyst review: `{packet_summary.get('ready_for_analyst')}`")

    missing_data = packet.get("missing_data") or []
    warnings = packet.get("warnings") or []
    if not packet_summary.get("pnf_available"):
        warnings = [
            item
            for item in warnings
            if item != "No P&F sidecars found; P&F gate remains pending."
        ]
    if missing_data:
        st.warning("Packet has missing data. Review the list below before using it downstream.")
        with st.expander("Missing data"):
            for item in missing_data:
                st.write(f"- {item}")
    if warnings:
        with st.expander("Warnings"):
            for item in warnings:
                st.write(f"- {item}")

    st.subheader("Analyst Packet JSON")
    st.caption("This is the generated packet, not a source report file.")
    st.json(packet)

    st.subheader("Pretty Analyst Packet JSON")
    st.text_area("Pretty JSON", value=pretty_json or packet_to_pretty_json(packet), height=360)

    if st.button("Save Analyst Packet to report folder"):
        if not report_dir:
            st.warning("No report directory is available. Use Download instead.")
        else:
            try:
                packet_ticker = packet.get("ticker") or packet_summary.get("ticker") or "marketflow"
                save_path = Path(report_dir) / f"{packet_ticker}_analyst_packet.json"
                save_path.write_text(pretty_json or packet_to_pretty_json(packet), encoding="utf-8")
                st.success(f"Saved analyst packet to `{save_path}`")
            except Exception as exc:
                st.error(f"Could not save analyst packet: {exc}")

    st.download_button(
        "Download analyst_packet.json",
        data=pretty_json or packet_to_pretty_json(packet),
        file_name=f"{packet.get('ticker') or 'marketflow'}_analyst_packet.json",
        mime="application/json",
    )


def _render_wyckoff_analyst_prompt(result: dict[str, Any] | None) -> None:
    """Render the Wyckoff Analyst prompt preview tab."""
    st.write("This tab only builds a prompt preview. It does not call an AI model yet.")

    packet = st.session_state.get("latest_analyst_packet") or st.session_state.get("analyst_packet")
    if not isinstance(packet, dict):
        st.info("Build an Analyst Packet first.")
        return

    report_dir = (
        _nested_get(packet, ["source_files", "report_dir"])
        or (result.get("output_dir") if result else None)
    )
    packet_summary = packet.get("packet_summary") or {}
    strategy_context = packet.get("strategy_candidate") or {}

    style = st.selectbox(
        "Prompt style",
        options=list(PROMPT_STYLES),
        index=0,
        key="wyckoff_prompt_style",
    )
    include_raw_json = st.checkbox(
        "Include raw Analyst Packet JSON",
        value=False,
        key="wyckoff_prompt_include_raw_json",
    )

    if st.button("Build Analyst Prompt", type="primary"):
        prompt = build_wyckoff_analyst_prompt(packet, style=style, include_raw_json=include_raw_json)
        st.session_state.wyckoff_analyst_prompt = prompt
        st.session_state.latest_analyst_prompt = prompt
        st.session_state.wyckoff_analyst_prompt_text = prompt
        st.session_state.wyckoff_analyst_prompt_style = style
        st.session_state.wyckoff_analyst_prompt_include_raw_json = include_raw_json
        st.session_state.wyckoff_analyst_prompt_filename = build_prompt_filename(
            packet,
            style=style,
            include_timestamp=False,
        )

    prompt = st.session_state.get("wyckoff_analyst_prompt")
    built_style = st.session_state.get("wyckoff_analyst_prompt_style") or style
    built_include_raw_json = st.session_state.get("wyckoff_analyst_prompt_include_raw_json")
    filename = st.session_state.get("wyckoff_analyst_prompt_filename") or build_prompt_filename(
        packet,
        style=built_style,
        include_timestamp=False,
    )
    if not prompt:
        st.info("Click Build Analyst Prompt to generate the markdown preview.")
        _render_analyst_review_notes_section(
            packet=packet,
            report_dir=report_dir,
            prompt_markdown=None,
            response_markdown=st.session_state.get("analyst_chat_response_markdown"),
        )
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _display_optional_metric("Ticker", packet_summary.get("ticker") or packet.get("ticker"))
        _display_optional_metric("Timeframe", packet_summary.get("selected_timeframe") or strategy_context.get("tf"))
    with col2:
        _display_optional_metric("POP Gate", packet_summary.get("pop_gate"))
        _display_optional_metric("P&F Gate", packet_summary.get("pnf_gate"))
    with col3:
        _display_optional_metric("Risk Rank", packet_summary.get("risk_rank"))
        _display_optional_metric("Data Ready for Analyst Review", packet_summary.get("ready_for_analyst"))
    with col4:
        _display_optional_metric("Prompt Style", built_style)
        _display_optional_metric("Raw JSON", built_include_raw_json)

    st.subheader("Generated Prompt")
    if not st.session_state.get("wyckoff_analyst_prompt_text"):
        st.session_state.wyckoff_analyst_prompt_text = prompt
    edited_prompt = st.text_area("Prompt markdown", height=520, key="wyckoff_analyst_prompt_text")

    with st.expander("Markdown preview", expanded=False):
        st.markdown(edited_prompt)

    st.download_button(
        "Download analyst prompt",
        data=edited_prompt,
        file_name=filename,
        mime="text/markdown",
    )

    if st.button("Save prompt to report folder"):
        if not report_dir:
            st.warning("No report folder is available. Use Download instead.")
        else:
            try:
                save_filename = build_prompt_filename(packet, style=built_style, include_timestamp=True)
                save_path = Path(report_dir) / save_filename
                if save_path.exists():
                    stem = save_path.stem
                    suffix = save_path.suffix
                    counter = 2
                    while save_path.exists():
                        save_path = Path(report_dir) / f"{stem}_{counter}{suffix}"
                        counter += 1
                save_path.write_text(edited_prompt, encoding="utf-8")
                st.success(f"Saved analyst prompt to `{save_path}`")
                st.caption("Different prompt styles save as separate markdown files. Refresh Generated Artifacts to see this file.")
            except Exception as exc:
                st.error(f"Could not save analyst prompt: {exc}")

    st.divider()
    st.subheader("Analyst Chat - Experimental")
    st.warning("This section does not run automatically. Review the prompt first, then click Run Analyst.")

    config_status = get_analyst_chat_config_status()
    config_col1, config_col2, config_col3 = st.columns(3)
    with config_col1:
        _display_optional_metric("Configured", config_status.get("configured"))
    with config_col2:
        _display_optional_metric("Provider", config_status.get("provider"))
    with config_col3:
        _display_optional_metric("Model", config_status.get("model"))

    missing_config = config_status.get("missing") or []
    if missing_config:
        st.info("Analyst Chat is not fully configured. Dry-run mode is available.")
        st.caption(f"Missing: {', '.join(str(item) for item in missing_config)}")
    for note in config_status.get("notes") or []:
        st.caption(str(note))

    provider_value = st.text_input(
        "Analyst provider",
        value=str(config_status.get("provider") or ""),
        key="analyst_chat_provider",
    )
    model_value = st.text_input(
        "Analyst model",
        value=str(config_status.get("model") or ""),
        key="analyst_chat_model",
    )
    dry_run = st.checkbox(
        "Dry run only",
        value=True,
        key="analyst_chat_dry_run",
    )

    run_disabled = not isinstance(packet, dict) or not bool((edited_prompt or "").strip())
    if run_disabled:
        st.info("Build and review an Analyst Prompt before running Analyst Chat.")

    if st.button("Run Analyst", type="primary", disabled=run_disabled):
        chat_result = run_analyst_chat(
            edited_prompt,
            provider=provider_value or None,
            model=model_value or None,
            dry_run=bool(dry_run),
            source_metadata={
                "ticker": packet_summary.get("ticker") or packet.get("ticker"),
                "timeframe": (
                    packet_summary.get("selected_timeframe")
                    or strategy_context.get("tf")
                    or _nested_get(packet, ["pnf", "selection", "candidate_timeframe"])
                    or _nested_get(packet, ["pnf", "selected_sidecar", "inferred_timeframe"])
                    or _nested_get(packet, ["pnf", "selected_sidecar", "timeframe"])
                ),
                "prompt_style": built_style,
                "source_prompt_filename": filename,
                "packet_version": packet.get("packet_version"),
            },
        )
        st.session_state.analyst_chat_result = chat_result
        st.session_state.analyst_chat_response_markdown = chat_result.get("response_markdown")
        st.session_state.analyst_chat_response_filename = (
            build_response_filename(packet, style=built_style, include_timestamp=True)
            if chat_result.get("response_markdown")
            else None
        )

    if st.button(
        "Clear analyst response",
        disabled=not st.session_state.get("analyst_chat_result")
        and not st.session_state.get("analyst_chat_response_markdown"),
    ):
        st.session_state.analyst_chat_result = None
        st.session_state.analyst_chat_response_markdown = None
        st.session_state.analyst_chat_response_filename = None

    chat_result = st.session_state.get("analyst_chat_result")
    response_markdown = st.session_state.get("analyst_chat_response_markdown")
    if isinstance(chat_result, dict):
        if chat_result.get("error"):
            st.warning(chat_result.get("error"))
        for note in chat_result.get("notes") or []:
            st.caption(str(note))
        status_col1, status_col2, status_col3, status_col4 = st.columns(4)
        with status_col1:
            _display_optional_metric("Execution Mode", chat_result.get("execution_mode"))
        with status_col2:
            _display_optional_metric("Dry Run", chat_result.get("dry_run"))
        with status_col3:
            _display_optional_metric("Prompt Characters", chat_result.get("prompt_chars"))
        with status_col4:
            _display_optional_metric(
                "Response Characters",
                len(str(response_markdown or "")) if response_markdown else 0,
            )
        with st.expander("Analyst Chat result details", expanded=False):
            st.json(
                {
                    "success": chat_result.get("success"),
                    "dry_run": chat_result.get("dry_run"),
                    "provider": chat_result.get("provider"),
                    "model": chat_result.get("model"),
                    "created_at": chat_result.get("created_at"),
                    "prompt_preview_chars": chat_result.get("prompt_preview_chars"),
                    "execution_mode": chat_result.get("execution_mode"),
                }
            )

    if response_markdown:
        response_filename = st.session_state.get("analyst_chat_response_filename")
        if not response_filename:
            response_filename = build_response_filename(packet, style=built_style, include_timestamp=True)
            st.session_state.analyst_chat_response_filename = response_filename
        st.markdown("#### Analyst Response Markdown")
        st.markdown(response_markdown)
        st.caption(f"Response filename preview: `{response_filename}`")
        st.download_button(
            "Download analyst response",
            data=response_markdown,
            file_name=response_filename,
            mime="text/markdown",
        )

        if st.button("Save analyst response to report folder"):
            if not report_dir:
                st.warning("No report folder is available. Use Download instead.")
            else:
                try:
                    save_filename = response_filename
                    save_path = Path(report_dir) / save_filename
                    if save_path.exists():
                        stem = save_path.stem
                        suffix = save_path.suffix
                        counter = 2
                        while save_path.exists():
                            save_path = Path(report_dir) / f"{stem}_{counter}{suffix}"
                            counter += 1
                    save_path.write_text(response_markdown, encoding="utf-8")
                    st.success(f"Saved analyst response to `{save_path}`")
                    st.caption("Refresh Generated Artifacts to see this analyst response markdown file.")
                except Exception as exc:
                    st.error(f"Could not save analyst response: {exc}")

    _render_analyst_review_notes_section(
        packet=packet,
        report_dir=report_dir,
        prompt_markdown=edited_prompt,
        response_markdown=response_markdown,
    )


def _render_raw_json(result: dict[str, Any] | None) -> None:
    """Render the Raw JSON tab."""
    report_json = result.get("report_json") if result else None
    if report_json:
        st.json(report_json)
    else:
        st.info("No JSON report is loaded.")


def main() -> None:
    """Run the MarketFlow Studio Streamlit app."""
    st.set_page_config(page_title="MarketFlow Studio", layout="wide")
    st.title("MarketFlow Studio")

    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "strategy_result" not in st.session_state:
        st.session_state.strategy_result = None
    if "batch_result" not in st.session_state:
        st.session_state.batch_result = None
    if "monte_carlo_result" not in st.session_state:
        st.session_state.monte_carlo_result = None
    if "latest_monte_carlo_result" not in st.session_state:
        st.session_state.latest_monte_carlo_result = None
    if "selected_strategy_candidate" not in st.session_state:
        st.session_state.selected_strategy_candidate = None
    if "latest_strategy_candidate" not in st.session_state:
        st.session_state.latest_strategy_candidate = None
    if "analyst_packet" not in st.session_state:
        st.session_state.analyst_packet = None
    if "latest_analyst_packet" not in st.session_state:
        st.session_state.latest_analyst_packet = None
    if "analyst_packet_json" not in st.session_state:
        st.session_state.analyst_packet_json = None
    if "wyckoff_analyst_prompt" not in st.session_state:
        st.session_state.wyckoff_analyst_prompt = None
    if "latest_analyst_prompt" not in st.session_state:
        st.session_state.latest_analyst_prompt = None
    if "wyckoff_analyst_prompt_filename" not in st.session_state:
        st.session_state.wyckoff_analyst_prompt_filename = None
    if "wyckoff_analyst_prompt_style" not in st.session_state:
        st.session_state.wyckoff_analyst_prompt_style = None
    if "wyckoff_analyst_prompt_include_raw_json" not in st.session_state:
        st.session_state.wyckoff_analyst_prompt_include_raw_json = None
    if "analyst_chat_result" not in st.session_state:
        st.session_state.analyst_chat_result = None
    if "analyst_chat_response_markdown" not in st.session_state:
        st.session_state.analyst_chat_response_markdown = None
    if "analyst_chat_response_filename" not in st.session_state:
        st.session_state.analyst_chat_response_filename = None
    if "latest_backtest_candidate_snapshot" not in st.session_state:
        st.session_state.latest_backtest_candidate_snapshot = None
    if "latest_backtest_candidate_csv" not in st.session_state:
        st.session_state.latest_backtest_candidate_csv = None
    if "latest_backtest_outcome_evaluation" not in st.session_state:
        st.session_state.latest_backtest_outcome_evaluation = None
    if "latest_backtest_results_csv" not in st.session_state:
        st.session_state.latest_backtest_results_csv = None
    if "latest_backtest_calibration_summary" not in st.session_state:
        st.session_state.latest_backtest_calibration_summary = None
    if "latest_backtest_calibration_summary_artifact" not in st.session_state:
        st.session_state.latest_backtest_calibration_summary_artifact = None

    with st.sidebar:
        st.header("Analysis")
        ticker = st.text_input("Ticker", value="AAPL").strip()
        timeframes = st.multiselect(
            "Timeframes",
            options=TIMEFRAME_OPTIONS,
            default=DEFAULT_TIMEFRAMES,
        )

        if st.button("Run Analysis", type="primary"):
            with st.spinner(f"Running analysis for {ticker}..."):
                st.session_state.analysis_result = run_single_ticker(ticker, timeframes)

        if st.button("Load Latest Report"):
            st.session_state.analysis_result = _load_latest_result(ticker)

        _render_loaded_report_caption(st.session_state.analysis_result)
        page = st.radio(
            "Workspace",
            [
                "Overview",
                "Reports",
                "CSV Preview",
                "Charts",
                "Strategy Ranking",
                "Batch Analysis",
                "Monte Carlo",
                "Analyst Packet",
                "Wyckoff Analyst",
                "Raw JSON",
            ],
            key="studio_workspace_page",
        )

    result = st.session_state.analysis_result
    st.subheader(page)
    if page == "Overview":
        _render_overview(result)
    elif page == "Reports":
        _render_reports(result)
    elif page == "CSV Preview":
        _render_csv_preview(result)
    elif page == "Charts":
        _render_charts(result)
    elif page == "Strategy Ranking":
        _render_strategy_ranking(result)
    elif page == "Batch Analysis":
        _render_batch_analysis()
    elif page == "Monte Carlo":
        _render_monte_carlo(result)
    elif page == "Analyst Packet":
        _render_analyst_packet(result)
    elif page == "Wyckoff Analyst":
        _render_wyckoff_analyst_prompt(result)
    elif page == "Raw JSON":
        _render_raw_json(result)


if __name__ == "__main__":
    main()
