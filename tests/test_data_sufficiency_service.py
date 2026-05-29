from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta

from marketflow.services.data_sufficiency_service import (
    INSUFFICIENT,
    LIMITED,
    NOT_YET_MATURE,
    SUFFICIENT,
    assess_csv_data_sufficiency,
    calculate_minimum_rows_required,
    detect_timestamp_column,
    infer_ticker_from_csv_name,
    infer_timeframe_from_csv_name,
    summarize_report_folder_data_sufficiency,
)


def _write_csv(path, rows: int, *, include_timestamp: bool = True) -> None:
    start = datetime(2026, 1, 1, 9, 30)
    columns = ["open", "high", "low", "close"]
    if include_timestamp:
        columns = ["timestamp", *columns]
    lines = [",".join(columns)]
    for index in range(rows):
        values = [100 + index, 101 + index, 99 + index, 100.5 + index]
        if include_timestamp:
            values = [(start + timedelta(minutes=index)).isoformat(), *values]
        lines.append(",".join(str(value) for value in values))
    path.write_text("\n".join(lines), encoding="utf-8")


def test_infer_ticker_timeframe_from_filename():
    path = "AAPL_1d_wyckoff_annotated.csv"

    assert infer_ticker_from_csv_name(path) == "AAPL"
    assert infer_timeframe_from_csv_name(path) == "1d"


def test_timestamp_column_detection():
    column = detect_timestamp_column(["open", "high", "low", "close", "timestamp"])

    assert column == "timestamp"


def test_minimum_row_calculation():
    minimum = calculate_minimum_rows_required(
        eigen_window=80,
        monte_carlo_horizon=60,
        backtest_horizon=20,
    )

    assert minimum == 240


def test_sufficient_csv(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 300)

    result = assess_csv_data_sufficiency(
        path,
        eigen_window=80,
        monte_carlo_horizon=60,
        backtest_horizon=20,
    )

    assert result["success"] is True
    assert result["rows_available"] == 300
    assert result["minimum_rows_required"] == 240
    assert result["data_sufficiency_status"] == SUFFICIENT


def test_limited_csv(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 150)

    result = assess_csv_data_sufficiency(
        path,
        eigen_window=80,
        monte_carlo_horizon=60,
        backtest_horizon=20,
    )

    assert result["data_sufficiency_status"] == LIMITED


def test_insufficient_csv(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 40)

    result = assess_csv_data_sufficiency(
        path,
        eigen_window=80,
        monte_carlo_horizon=60,
        backtest_horizon=20,
    )

    assert result["data_sufficiency_status"] == INSUFFICIENT


def test_missing_timestamp_handled_safely(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 120, include_timestamp=False)

    result = assess_csv_data_sufficiency(path, backtest_horizon=20)

    assert result["success"] is True
    assert result["timestamp_column"] is None
    assert result["warnings"]
    assert "timestamp_column_missing" in result["notes"]


def test_eigen_window_larger_than_available_rows(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 50)

    result = assess_csv_data_sufficiency(path, eigen_window=80)

    assert result["eigen_sufficiency_status"] == INSUFFICIENT


def test_monte_carlo_horizon_limited(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 120)

    result = assess_csv_data_sufficiency(path, monte_carlo_horizon=60)

    assert result["monte_carlo_sufficiency_status"] == LIMITED


def test_no_future_bars_calibration_status(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 300)

    result = assess_csv_data_sufficiency(path, backtest_horizon=20, future_bars_available=0)

    assert result["calibration_sufficiency_status"] == NOT_YET_MATURE
    assert result["bars_remaining_to_maturity"] == 20


def test_partial_future_window(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 300)

    result = assess_csv_data_sufficiency(path, backtest_horizon=20, future_bars_available=5)

    assert result["calibration_sufficiency_status"] == NOT_YET_MATURE
    assert result["bars_remaining_to_maturity"] == 15


def test_low_timeframe_warning(tmp_path):
    path = tmp_path / "AAPL_5m_wyckoff_annotated.csv"
    _write_csv(path, 300)

    result = assess_csv_data_sufficiency(path)

    assert result["noise_warning"]


def test_report_folder_summary_prefers_canonical_csvs(tmp_path):
    canonical = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    eigen = tmp_path / "AAPL_1d_pv_eigen.csv"
    backtest = tmp_path / "AAPL_1d_backtest_results_20260529.csv"
    _write_csv(canonical, 300)
    _write_csv(eigen, 300)
    _write_csv(backtest, 300)

    result = summarize_report_folder_data_sufficiency(
        tmp_path,
        parameter_context={"eigen_window": 80, "monte_carlo_horizon": 60, "backtest_horizon": 20},
    )

    assert result["success"] is True
    assert result["csv_file_count"] == 1
    assert result["rows"][0]["source_csv_name"] == canonical.name


def test_report_folder_fallback_readable_csv(tmp_path):
    fallback = tmp_path / "AAPL_1d_raw.csv"
    _write_csv(fallback, 120)

    result = summarize_report_folder_data_sufficiency(tmp_path, parameter_context={"backtest_horizon": 20})

    assert result["success"] is True
    assert result["csv_file_count"] == 1
    assert result["rows"][0]["source_csv_name"] == fallback.name
    assert result["warnings"]


def test_by_timeframe_parameter_context(tmp_path):
    daily = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    intraday = tmp_path / "AAPL_30m_wyckoff_annotated.csv"
    _write_csv(daily, 300)
    _write_csv(intraday, 300)
    context = {
        "eigen_window": 20,
        "monte_carlo_horizon": 20,
        "backtest_horizon": 20,
        "by_timeframe": {
            "30m": {
                "eigen_window": 80,
                "monte_carlo_horizon": 60,
                "backtest_horizon": 60,
            }
        },
    }

    result = summarize_report_folder_data_sufficiency(tmp_path, parameter_context=context)
    by_name = {row["source_csv_name"]: row for row in result["rows"]}

    assert by_name[daily.name]["minimum_rows_required"] == 100
    assert by_name[intraday.name]["minimum_rows_required"] == 240


def test_no_mutation_of_parameter_context(tmp_path):
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    _write_csv(path, 300)
    context = {
        "eigen_window": 20,
        "by_timeframe": {"1d": {"monte_carlo_horizon": 60}},
    }
    original = deepcopy(context)

    summarize_report_folder_data_sufficiency(tmp_path, parameter_context=context)

    assert context == original
