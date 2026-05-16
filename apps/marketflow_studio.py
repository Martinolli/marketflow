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
from marketflow.services.strategy_service import (
    get_report_root,
    normalize_tickers,
    rank_latest_candidates,
)


DEFAULT_TIMEFRAMES = ["1d", "4h", "1h"]
TIMEFRAME_OPTIONS = ["1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"]
CSV_PREVIEW_ROW_OPTIONS = [100, 250, 500, 1000]
CHART_ROW_OPTIONS = [200, 500, 1000, 2000]
STRATEGY_TIMEFRAMES = ["1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"]
WYCKOFF_PHASE_OPTIONS = ["A", "B", "C", "D", "E", "UNKNOWN"]


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
    report_dir = _report_dir_from_result(
        result,
        "No report directory loaded. Run an analysis or load the latest report first.",
    )
    if not report_dir:
        return

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
    if not csv_files:
        st.info("No annotated CSV files found for charting.")
        st.caption("Charts use annotated OHLC CSV files generated by MarketFlow reports.")
        return

    selected_csv = _select_annotated_csv(csv_files, "Chart CSV file", "chart_csv_file")
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
        return

    dataframe = strategy_result.get("dataframe")
    if dataframe is None or dataframe.empty:
        st.info(
            "No candidates passed the filters. Try a lower min RR, a different timeframe, "
            "or confirm reports exist for those tickers."
        )
        return

    st.write(f"Result count: `{len(dataframe)}`")
    st.dataframe(dataframe, use_container_width=True)

    results = strategy_result.get("results") or []
    labels = [
        f"{candidate.get('ticker', 'UNKNOWN')} | {candidate.get('tf', '')} | "
        f"score {candidate.get('score', 'NA')}"
        for candidate in results
    ]
    selected_label = st.selectbox("Select candidate", options=labels)
    selected_index = labels.index(selected_label)
    st.json(results[selected_index])


def _render_strategy_ranking(result: dict[str, Any] | None) -> None:
    """Render the Strategy Ranking tab."""
    st.write(
        "Rank long candidates from generated MarketFlow reports using the existing "
        "`marketflow_strategy` logic."
    )
    st.caption(f"Configured report root: `{get_report_root()}`")
    st.caption("This scan uses the latest batch/report namespace when available.")

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

    result = st.session_state.analysis_result
    overview_tab, reports_tab, csv_tab, charts_tab, strategy_tab, raw_json_tab = st.tabs(
        ["Overview", "Reports", "CSV Preview", "Charts", "Strategy Ranking", "Raw JSON"]
    )

    with overview_tab:
        _render_overview(result)

    with reports_tab:
        _render_reports(result)

    with csv_tab:
        _render_csv_preview(result)

    with charts_tab:
        _render_charts(result)

    with strategy_tab:
        _render_strategy_ranking(result)

    with raw_json_tab:
        _render_raw_json(result)


if __name__ == "__main__":
    main()
