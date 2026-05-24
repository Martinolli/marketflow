"""Minimal local Streamlit interface for MarketFlow."""

from __future__ import annotations

import os
import json
import re
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("MARKETFLOW_CONSOLE_LOG_LEVEL", "WARNING")

import streamlit as st
import streamlit.components.v1 as components

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from marketflow.charts.pnf_chart import build_pnf_chart_from_sidecar
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
from marketflow.services.batch_service import (
    normalize_batch_tickers,
    run_batch_analysis,
)
from marketflow.services.monte_carlo_service import (
    list_monte_carlo_outputs,
    load_latest_close,
    run_monte_carlo_for_csv,
)
from marketflow.services.pnf_service import (
    generate_pnf_for_csv,
    generate_pnf_for_csvs,
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
    for key in ("inferred_timeframe", "timeframe", "direction", "objective"):
        value = sidecar.get(key)
        if value is not None and value != "":
            details.append(f"{key}: {value}")
    if details:
        parts.append(" | ".join(details))
    return " - ".join(parts)


def _pnf_metadata_row(sidecar: dict[str, Any]) -> dict[str, Any]:
    """Return compact metadata for the selected P&F sidecar."""
    return {
        "filename": sidecar.get("filename"),
        "source_csv": sidecar.get("source_csv"),
        "timeframe": sidecar.get("inferred_timeframe") or sidecar.get("timeframe"),
        "direction": sidecar.get("direction"),
        "box_mode": sidecar.get("box_mode"),
        "box_value": sidecar.get("box_value"),
        "box_size": sidecar.get("box_size"),
        "reversal": sidecar.get("reversal"),
        "last_price": sidecar.get("last_price"),
        "breakout_level": sidecar.get("breakout_level"),
        "objective": sidecar.get("objective"),
        "objective_r_multiple": sidecar.get("objective_r_multiple"),
    }


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
    if csv_files:
        selected_csv = _select_annotated_csv(csv_files, "Chart CSV file", "chart_csv_file")
        chart_selected_csv = selected_csv
        chart_rows = st.selectbox(
            "Chart rows",
            options=CHART_ROW_OPTIONS,
            index=1,
            key="chart_rows",
        )

        timeframe = _render_csv_file_context(selected_csv)

        dataframe = load_csv_for_chart(selected_csv, nrows=chart_rows)
        if dataframe is None:
            st.error("Could not load this CSV file for charting.")
        else:
            try:
                title_parts = [Path(selected_csv).stem]
                if timeframe:
                    title_parts.append(timeframe)
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
        pnf_csv = st.selectbox(
            "P&F source CSV",
            options=csv_files,
            format_func=lambda path: Path(path).name,
            key="pnf_generation_csv",
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
            if st.button("Generate P&F for all annotated CSVs"):
                generation_results = generate_pnf_for_csvs(
                    csv_files,
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
        default_legacy_index = 0
        if chart_selected_csv in csv_files:
            default_legacy_index = csv_files.index(chart_selected_csv)
        legacy_csv = st.selectbox(
            "Legacy plot source CSV",
            options=csv_files,
            index=default_legacy_index,
            format_func=lambda path: Path(path).name,
            key="legacy_plot_generation_csv",
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

    if pnf_sidecars:
        st.caption(
            "The reconstructed P&F chart is built from sidecar JSON and may not include every visual "
            "feature from the saved HTML plot. Use Generated Artifacts to preview the original saved P&F HTML."
        )
        selected_sidecar = st.selectbox(
            "P&F sidecar",
            options=pnf_sidecars,
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


def _render_strategy_results(strategy_result: dict[str, Any] | None) -> None:
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

    if st.button("Use selected candidate in Monte Carlo"):
        st.session_state.monte_carlo_prefill = {
            "ticker": selected_candidate.get("ticker"),
            "csv": selected_candidate.get("csv"),
            "tf": selected_candidate.get("tf"),
            "entry": selected_candidate.get("close"),
            "stop_loss": selected_candidate.get("sl"),
            "take_profit": selected_candidate.get("tp"),
            "source": "strategy_ranking",
        }
        st.session_state.latest_strategy_candidate = selected_candidate
        st.session_state.selected_strategy_candidate = selected_candidate
        st.session_state.monte_carlo_result = None
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

    _render_strategy_results(st.session_state.get("strategy_result"))


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


def _sync_monte_carlo_prefill(prefill: dict[str, Any] | None) -> None:
    """Apply candidate prefill values to Monte Carlo widgets once per candidate."""
    token = _prefill_token(prefill)
    if token is None or token == st.session_state.get("monte_carlo_prefill_token"):
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
    st.session_state.monte_carlo_prefill_token = token


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
            ]:
                st.session_state.pop(key, None)
            st.session_state.monte_carlo_result = None
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
                )
                st.session_state.monte_carlo_result = mc_result
                if prefill and candidate_csv and _path_matches(candidate_csv, selected_csv):
                    st.session_state.monte_carlo_result["source"] = prefill.get("source")
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

    if st.button("Build Analyst Packet", type="primary"):
        packet = build_analyst_packet(
            ticker=ticker or "",
            report_json=report_json,
            summary_text=summary_text,
            report_dir=report_dir,
            strategy_candidate=strategy_candidate,
            monte_carlo_result=monte_carlo_result,
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
    monte_carlo_context = packet.get("monte_carlo") or {}
    pnf_context = packet.get("pnf") or {}

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
        _display_optional_metric("POP Gate", packet_summary.get("pop_gate"))
        _display_optional_metric("Risk Rank", packet_summary.get("risk_rank"))

    col5, col6 = st.columns(2)
    with col5:
        _display_optional_metric("MC TP First", _format_probability(monte_carlo_context.get("pop_tp_first")))
    with col6:
        _display_optional_metric("MC SL First", _format_probability(monte_carlo_context.get("p_sl_first")))

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
                        "sidecar_timeframe": selected_sidecar.get("inferred_timeframe") or selected_sidecar.get("timeframe"),
                        "box_size": selected_sidecar.get("box_size"),
                        "reversal": selected_sidecar.get("reversal"),
                        "objective": selected_sidecar.get("objective"),
                        "objective_r_multiple": selected_sidecar.get("objective_r_multiple"),
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
                            "timeframe": item.get("inferred_timeframe") or item.get("timeframe"),
                            "direction": item.get("direction"),
                            "match_score": item.get("match_score"),
                            "matched_by": item.get("matched_by"),
                            "breakout_level": item.get("breakout_level"),
                            "objective": item.get("objective"),
                            "objective_r_multiple": item.get("objective_r_multiple"),
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

    st.caption(f"Ready for analyst: `{packet_summary.get('ready_for_analyst')}`")

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
        _display_optional_metric("Ready", packet_summary.get("ready_for_analyst"))
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
    if "analyst_packet" not in st.session_state:
        st.session_state.analyst_packet = None
    if "latest_analyst_packet" not in st.session_state:
        st.session_state.latest_analyst_packet = None
    if "analyst_packet_json" not in st.session_state:
        st.session_state.analyst_packet_json = None
    if "wyckoff_analyst_prompt" not in st.session_state:
        st.session_state.wyckoff_analyst_prompt = None
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
