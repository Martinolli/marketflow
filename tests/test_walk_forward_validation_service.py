from __future__ import annotations

import pandas as pd

from marketflow.marketflow_strategy import (
    RR_GATE_PASSED,
    TARGET_PROVENANCE_WYCKOFF_TR_HIGH,
    TARGET_NOT_AVAILABLE,
    TARGET_RESOLVED,
)
from marketflow.services.walk_forward_validation_service import (
    build_and_evaluate_walk_forward_cases_from_csv,
    build_walk_forward_cases_from_csv,
    detect_walk_forward_timestamp_column,
    evaluate_walk_forward_cases,
    infer_walk_forward_ticker_from_csv_name,
    infer_walk_forward_timeframe_from_csv_name,
    summarize_walk_forward_validation,
)


def _rows(count: int, *, include_timestamp: bool = True, include_event: bool = True) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(count):
        close = 100.0 + index * 0.1
        row: dict[str, object] = {
            "open": close - 0.2,
            "high": close + 2.0,
            "low": close - 1.0,
            "close": close,
            "tr_high": close + 2.0,
            "wyckoff_phase": "C" if index % 2 == 0 else "D",
            "trend": "up",
            "strategy_score": 70.0 + (index % 10),
        }
        if include_timestamp:
            row["timestamp"] = f"2026-01-{(index % 28) + 1:02d} 10:{index % 60:02d}:00"
        if include_event:
            row["wyckoff_event"] = "SPRING_WEAK" if index % 2 == 0 else "UT_WEAK"
        rows.append(row)
    return rows


def _csv(tmp_path, count: int, name: str = "AAPL_1d_wyckoff_annotated.csv", **kwargs):
    path = tmp_path / name
    pd.DataFrame(_rows(count, **kwargs)).to_csv(path, index=False)
    return path


def test_infer_ticker_and_timeframe_from_filename():
    path = "AAPL_1d_wyckoff_annotated.csv"

    assert infer_walk_forward_ticker_from_csv_name(path) == "AAPL"
    assert infer_walk_forward_timeframe_from_csv_name(path) == "1d"
    assert infer_walk_forward_timeframe_from_csv_name("IONQ_30m_wyckoff_annotated.csv") == "30m"


def test_source_identity_mismatch_fails_before_building_cases(tmp_path):
    path = _csv(tmp_path, 130, name="BBB_4h_wyckoff_annotated.csv")

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        ticker="AAA",
        timeframe="4h",
    )

    assert result["success"] is False
    assert result["source_status"] == "DATASET_IDENTITY_MISMATCH"
    assert result["source_reason"] == "DATASET_IDENTITY_MISMATCH"
    assert result["ticker"] == "BBB"
    assert result["timeframe"] == "4h"
    assert result["cases"] == []


def test_source_identity_unknown_fails_when_caller_supplies_label(tmp_path):
    path = _csv(tmp_path, 130, name="AAA_source.csv")

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        ticker="AAA",
        timeframe="4h",
    )

    assert result["success"] is False
    assert result["source_status"] == "DATASET_IDENTITY_UNKNOWN"
    assert result["source_reason"] == "DATASET_IDENTITY_UNKNOWN"
    assert result["ticker"] == "AAA"
    assert result["timeframe"] is None
    assert result["cases"] == []


def test_source_identity_unknown_fails_without_caller_labels(tmp_path):
    path = _csv(tmp_path, 130, name="source.csv")

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test")

    assert result["success"] is False
    assert result["source_status"] == "DATASET_IDENTITY_UNKNOWN"
    assert result["source_reason"] == "DATASET_IDENTITY_UNKNOWN"
    assert result["ticker"] == "SOURCE"
    assert result["timeframe"] is None
    assert result["cases"] == []


def test_detect_timestamp_column():
    columns = ["open", "high", "low", "close", "timestamp"]

    assert detect_walk_forward_timestamp_column(columns) == "timestamp"


def test_build_cases_requires_enough_lookback(tmp_path):
    path = _csv(tmp_path, 120, name="IONQ_30m_wyckoff_annotated.csv")

    result = build_walk_forward_cases_from_csv(path, profile_name="intraday_tactical")

    assert result["success"] is False
    assert result["case_count"] == 0
    assert result["warnings"] or result["errors"]


def test_build_cases_with_enough_rows_and_mature_future(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test")

    assert result["success"] is True
    assert result["case_count"] > 0
    assert all(case["future_bars_available"] >= 20 for case in result["cases"])
    assert all(case["signal_row_index"] <= 320 - result["horizon_bars"] - 1 for case in result["cases"])


def test_no_future_leakage_metadata(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=1)
    case = result["cases"][0]

    assert case["lookback_end_index"] == case["signal_row_index"]
    assert case["future_window_start_index"] == case["signal_row_index"] + 1
    assert case["future_window_end_index"] >= case["future_window_start_index"]
    assert case["lookback_rows_available"] == case["signal_row_index"] + 1


def test_event_filter_selects_only_matching_rows(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        event_filters=["SPRING_WEAK"],
        max_cases=5,
    )

    assert result["case_count"] == 5
    assert {case["wyckoff_event"] for case in result["cases"]} == {"SPRING_WEAK"}


def test_build_cases_uses_wyckoff_confirmed_event_for_filter(tmp_path):
    rows = _rows(320)
    for index, row in enumerate(rows):
        row["wyckoff_event"] = "SC"
        row["wyckoff_confirmed_event"] = "SPRING_WEAK" if index % 2 == 0 else "UT_WEAK"
    path = tmp_path / "IONQ_30m_wyckoff_annotated.csv"
    pd.DataFrame(rows).to_csv(path, index=False)

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        event_filters=["SPRING_WEAK"],
        step=1,
        max_cases=5,
        require_mature_future=True,
    )

    assert result["success"] is True
    assert result["case_count"] > 0
    assert result["event_column"] == "wyckoff_confirmed_event"
    assert all(case["wyckoff_event"] == "SPRING_WEAK" for case in result["cases"])
    assert all(case["wyckoff_event_source"] == "wyckoff_confirmed_event" for case in result["cases"])


def test_build_cases_falls_back_to_raw_wyckoff_event_when_confirmed_missing(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        event_filters=["SPRING_WEAK"],
        step=1,
        max_cases=5,
        require_mature_future=True,
    )

    assert result["success"] is True
    assert result["case_count"] > 0
    assert result["event_column"] == "wyckoff_event"
    assert all(case["wyckoff_event"] == "SPRING_WEAK" for case in result["cases"])
    assert all(case["wyckoff_event_source"] == "wyckoff_event" for case in result["cases"])


def test_missing_event_column_with_filter_returns_zero_cases(tmp_path):
    path = _csv(tmp_path, 320, include_event=False)

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        event_filters=["SPRING_WEAK"],
    )

    assert result["success"] is False
    assert result["case_count"] == 0
    assert result["warnings"]


def test_max_cases_respected(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=3)

    assert result["case_count"] == 3


def test_step_respected(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test", step=5, max_cases=4)
    indices = [case["signal_row_index"] for case in result["cases"]]

    assert indices == [119, 124, 129, 134]


def test_candidate_fields_valid(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=1)
    case = result["cases"][0]

    assert case["snapshot_success"] is True
    assert case["entry"] is not None
    assert case["stop_loss"] < case["entry"]
    assert case["take_profit"] > case["entry"]
    assert case["target_status"] == TARGET_RESOLVED
    assert case["target_provenance"] == TARGET_PROVENANCE_WYCKOFF_TR_HIGH
    assert case["target_structural_level_kind"] == "resistance"
    assert case["rr_status"] == RR_GATE_PASSED
    assert case["signal_row_index"] == 119
    assert case["source_csv"] == str(path)
    assert case["candidate_source"] == "walk_forward_validation"
    assert case["profile_name"] == "fast_test"
    assert case["wyckoff_event_source"] == "wyckoff_event"
    assert case["wyckoff_phase_source"] == "wyckoff_phase"
    assert case["trend_source"] == "trend"


def test_missing_structural_target_records_target_status_as_rr_status(tmp_path):
    rows = _rows(320)
    for row in rows:
        row.pop("tr_high", None)
    path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    pd.DataFrame(rows).to_csv(path, index=False)

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        max_cases=1,
        include_invalid_cases=True,
    )
    case = result["cases"][0]

    assert case["snapshot_success"] is False
    assert case["target_status"] == TARGET_NOT_AVAILABLE
    assert case["rr_status"] == TARGET_NOT_AVAILABLE


def test_evaluate_cases_returns_result_rows(tmp_path):
    path = _csv(tmp_path, 320)
    build_result = build_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=2)

    result = evaluate_walk_forward_cases(build_result["cases"], profile_name="fast_test")

    assert result["evaluated_count"] == 2
    assert result["result_rows"]
    assert result["result_rows"][0]["outcome"] == "TP_FIRST"


def test_build_and_evaluate_convenience_returns_summary(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_and_evaluate_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=3)

    assert result["build_result"]["case_count"] == 3
    assert result["evaluation_result"]["evaluated_count"] == 3
    assert result["summary"]["scoreable_count"] == 3


def test_unknown_profile_returns_safe_error(tmp_path):
    path = _csv(tmp_path, 320)

    result = build_walk_forward_cases_from_csv(path, profile_name="unknown_profile")

    assert result["success"] is False
    assert result["errors"]


def test_empty_csv_returns_safe_error(tmp_path):
    path = tmp_path / "EMPTY_1d_wyckoff_annotated.csv"
    pd.DataFrame(columns=["timestamp", "open", "high", "low", "close"]).to_csv(path, index=False)

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test")

    assert result["success"] is False
    assert result["errors"]


def test_missing_timestamp_handled_safely(tmp_path):
    path = _csv(tmp_path, 320, include_timestamp=False)

    result = build_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=1)
    case = result["cases"][0]

    assert result["success"] is True
    assert result["timestamp_column"] is None
    assert case["signal_timestamp"] is None
    assert case["signal_row_index"] == 119


def test_repeated_calls_produce_fresh_cases(tmp_path):
    path = _csv(tmp_path, 320)

    first = build_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=2)
    first["cases"][0]["signal_row_index"] = -1
    second = build_walk_forward_cases_from_csv(path, profile_name="fast_test", max_cases=2)

    assert [case["signal_row_index"] for case in second["cases"]] == [119, 120]


def test_deterministic_with_fixed_inputs(tmp_path):
    path = _csv(tmp_path, 320)

    first = build_walk_forward_cases_from_csv(path, profile_name="fast_test", step=7, max_cases=4)
    second = build_walk_forward_cases_from_csv(path, profile_name="fast_test", step=7, max_cases=4)

    assert first["case_count"] == second["case_count"]
    assert [case["signal_row_index"] for case in first["cases"]] == [
        case["signal_row_index"] for case in second["cases"]
    ]


def test_summary_counts_outcomes_correctly():
    rows = [
        {"outcome": "TP_FIRST", "future_bars_available": 20, "horizon_bars": 20, "realized_R": 1.5},
        {"outcome": "SL_FIRST", "future_bars_available": 20, "horizon_bars": 20, "realized_R": -1.0},
        {"outcome": "NEITHER", "future_bars_available": 20, "horizon_bars": 20, "realized_R": 0.2},
        {"outcome": "INVALID", "future_bars_available": "", "horizon_bars": 20, "outcome_error": "bad"},
        {"outcome": "AMBIGUOUS", "future_bars_available": 20, "horizon_bars": 20},
        {"outcome": "NEITHER", "future_bars_available": 3, "horizon_bars": 20, "realized_R": 0.1},
    ]

    summary = summarize_walk_forward_validation(rows)

    assert summary["sample_count"] == 6
    assert summary["scoreable_count"] == 3
    assert summary["tp_first_count"] == 1
    assert summary["sl_first_count"] == 1
    assert summary["neither_count"] == 2
    assert summary["invalid_count"] == 1
    assert summary["ambiguous_count"] == 1
    assert summary["not_mature_count"] == 1
    assert summary["win_rate"] == 1 / 3
    assert summary["loss_rate"] == 1 / 3
    assert summary["neither_rate"] == 1 / 3
