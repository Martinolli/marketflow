"""Minimal local Streamlit interface for MarketFlow."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from marketflow.charts.wyckoff_chart import build_basic_wyckoff_candlestick_chart
from marketflow.services.analysis_service import run_single_ticker
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


DEFAULT_TIMEFRAMES = ["1d", "4h", "1h"]
TIMEFRAME_OPTIONS = ["1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"]


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
        "error": None if report_dir else f"No report found for {ticker}.",
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


def _render_overview(result: dict[str, Any] | None) -> None:
    """Render the Overview tab."""
    if not result:
        st.info("Run an analysis or load the latest report to view an overview.")
        return

    report_json = result.get("report_json") or {}
    signal = report_json.get("signal") if isinstance(report_json, dict) else {}
    risk = report_json.get("risk_assessment") if isinstance(report_json, dict) else {}

    st.subheader(result.get("ticker") or "Ticker")
    if result.get("output_dir"):
        st.caption(f"Output directory: {result['output_dir']}")

    if result.get("error"):
        st.error(result["error"])
        with st.expander("Error details"):
            if result.get("error_type"):
                st.write(f"Type: `{result['error_type']}`")
            if result.get("traceback"):
                st.code(result["traceback"], language="python")
            else:
                st.write("No additional debug details are available.")

    col1, col2, col3 = st.columns(3)
    with col1:
        _display_value("Current Price", report_json.get("current_price"))
        _display_value("Stop Loss", _nested_get(risk, ["stop_loss"]))
    with col2:
        _display_value("Signal Type", _nested_get(signal, ["type"]))
        _display_value("Take Profit", _nested_get(risk, ["take_profit"]))
    with col3:
        _display_value("Signal Strength", _nested_get(signal, ["strength"]))
        _display_value("Risk/Reward", _nested_get(risk, ["risk_reward_ratio"]))

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
    if not result or not result.get("output_dir"):
        st.info("No report directory loaded.")
        return

    report_dir = result["output_dir"]
    st.write(f"Report directory: `{report_dir}`")

    files = list_report_files(report_dir) or result.get("report_files") or []
    if files:
        st.markdown("#### Generated Files")
        for file_path in files:
            st.write(f"- `{file_path}`")
    else:
        st.info("No generated files found in this directory.")

    date_folders = list_report_date_folders()
    if date_folders:
        st.markdown("#### Report Date / Batch Folders")
        for folder in date_folders:
            st.write(f"- `{folder}`")

    report_parent = str(Path(report_dir).parent)
    tickers = list_available_tickers(report_parent)
    if tickers:
        st.markdown("#### Available Ticker Folders")
        st.write(", ".join(f"`{ticker}`" for ticker in tickers))

    summary_text = result.get("summary_text")
    if summary_text:
        st.markdown("#### Summary")
        st.text(summary_text)


def _render_csv_preview(result: dict[str, Any] | None) -> None:
    """Render the CSV Preview tab."""
    if not result or not result.get("output_dir"):
        st.info("Load a report or run an analysis before previewing CSV files.")
        return

    report_dir = result["output_dir"]
    report_path = Path(report_dir)
    if not report_path.exists() or not report_path.is_dir():
        st.warning(f"Report directory does not exist: {report_dir}")
        return

    csv_files = list_annotated_csv_files(report_dir)
    if not csv_files:
        st.info("No annotated CSV files found in this report directory.")
        return

    selected_csv = st.selectbox(
        "CSV file",
        options=csv_files,
        format_func=lambda path: Path(path).name,
        key="csv_preview_file",
    )
    preview_rows = st.selectbox(
        "Preview rows",
        options=[100, 250, 500, 1000],
        index=2,
        key="csv_preview_rows",
    )

    timeframe = infer_timeframe_from_csv_name(selected_csv)
    st.write(f"Filename: `{Path(selected_csv).name}`")
    if timeframe:
        st.write(f"Timeframe: `{timeframe}`")
    else:
        st.write("Timeframe: unknown")

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
    if not result or not result.get("output_dir"):
        st.info("Run an analysis or load a report first.")
        return

    report_dir = result["output_dir"]
    report_path = Path(report_dir)
    if not report_path.exists() or not report_path.is_dir():
        st.warning(f"Report directory does not exist: {report_dir}")
        return

    csv_files = list_annotated_csv_files(report_dir)
    if not csv_files:
        st.info("No annotated CSV files found for charting.")
        return

    selected_csv = st.selectbox(
        "Chart CSV file",
        options=csv_files,
        format_func=lambda path: Path(path).name,
        key="chart_csv_file",
    )
    chart_rows = st.selectbox(
        "Chart rows",
        options=[200, 500, 1000, 2000],
        index=1,
        key="chart_rows",
    )

    timeframe = infer_timeframe_from_csv_name(selected_csv)
    st.write(f"Filename: `{Path(selected_csv).name}`")
    if timeframe:
        st.write(f"Timeframe: `{timeframe}`")
    else:
        st.write("Timeframe: unknown")

    dataframe = load_csv_for_chart(selected_csv, nrows=chart_rows)
    if dataframe is None:
        st.error("Could not load this CSV file for charting.")
        return

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

    result = st.session_state.analysis_result
    overview_tab, reports_tab, csv_tab, charts_tab, raw_json_tab = st.tabs(
        ["Overview", "Reports", "CSV Preview", "Charts", "Raw JSON"]
    )

    with overview_tab:
        _render_overview(result)

    with reports_tab:
        _render_reports(result)

    with csv_tab:
        _render_csv_preview(result)

    with charts_tab:
        _render_charts(result)

    with raw_json_tab:
        _render_raw_json(result)


if __name__ == "__main__":
    main()
