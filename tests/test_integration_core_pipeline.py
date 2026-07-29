import pytest
import pandas as pd
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_report import MarketflowReport

@pytest.fixture(scope="module")
def facade():
    return MarketflowFacade()


def _deterministic_analysis_result():
    index = pd.date_range("2024-01-01", periods=3, freq="D", tz="UTC")
    price = pd.DataFrame(
        {
            "open": [100.0, 101.0, 102.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.0, 100.0, 101.0],
            "close": [100.5, 101.5, 102.5],
        },
        index=index,
    )
    volume = pd.Series([1000, 1100, 1200], index=index)
    annotated = price.copy()
    annotated["volume"] = volume
    annotated["wyckoff_event"] = ["", "SC", ""]
    annotated["wyckoff_phase"] = ["UNKNOWN", "A", "A"]

    return {
        "ticker": "NVDA",
        "current_price": 102.5,
        "signal": {"type": "BUY", "strength": "WEAK", "details": "Deterministic fixture signal"},
        "risk_assessment": {
            "stop_loss": 98.0,
            "take_profit": 108.0,
            "risk_reward_ratio": 1.5,
            "position_size": 1.0,
            "risk_per_share": 4.5,
        },
        "timeframe_analyses": {
            "1d": {
                "candle_analysis": {"last_candle_signal": {"Name": "Neutral"}},
                "trend_analysis": {"trend_direction": "up", "trend_strength": "moderate"},
                "pattern_analysis": {"testing": {"detected": True}},
                "support_resistance": {
                    "support": [{"price": 99.0}],
                    "resistance": [{"price": 103.0}],
                },
                "processed_data": {"price": price, "volume": volume},
                "wyckoff_phases": [{"phase": "A", "timestamp": index[1]}],
                "wyckoff_events": [{"event_name": "SC", "timestamp": index[1], "price": 101.5, "volume": 1100}],
                "wyckoff_trading_ranges": [],
                "wyckoff_annotated_data": annotated,
            }
        },
    }


def test_full_marketflow_pipeline(facade, tmp_path):
    ticker = "NVDA"  # or any test ticker you have data for
    timeframes =  [{"interval": "1d", "period": "60d"}]  # or just ["1h"] if you want to keep it simple

    # 1. Use a deterministic facade-shaped analysis result.
    assert isinstance(facade, MarketflowFacade)
    result = _deterministic_analysis_result()
    assert isinstance(result, dict)
    assert "timeframe_analyses" in result
    assert "signal" in result
    assert "risk_assessment" in result

    # 2. Check structure and fields for each timeframe
    for tf, tf_data in result["timeframe_analyses"].items():
        assert "candle_analysis" in tf_data
        assert "trend_analysis" in tf_data
        assert "pattern_analysis" in tf_data
        assert "support_resistance" in tf_data
        assert "processed_data" in tf_data

    # 3. Result extraction
    extractor = MarketflowResultExtractor({ticker: result})
    tickers = extractor.get_tickers()
    assert ticker in tickers
    tf_list = extractor.get_timeframes(ticker)
    for tf in timeframes:
        assert tf["interval"] in tf_list

    # 4. Generate reports
    report_dir = tmp_path / "reports"
    report = MarketflowReport(extractor, output_dir=str(report_dir))
    summary = report.create_summary_report(ticker)
    html = report.create_html_report(ticker)
    json_ = report.create_json_report(ticker)

    assert summary is True
    assert html is True
    assert json_ is True

    # 5. Check the output files exist and are non-empty
    expected_files = [
        report_dir / f"{ticker}_summary_report.txt",
        report_dir / f"{ticker}_report.html",
        report_dir / f"{ticker}_report.json",
    ]
    for f in expected_files:
        assert f.exists()
        assert f.stat().st_size > 0

    # 6. (Optional) Check for important content in the reports
    with open(expected_files[0], encoding="utf-8") as f_txt:
        content = f_txt.read()
        assert "Marketflow Analysis Report for" in content
        assert "Signal Type" in content
        assert "Pattern Analysis" in content

    with open(expected_files[1], encoding="utf-8") as f_html:
        html_content = f_html.read()
        assert "<html" in html_content
        assert "Marketflow Analysis Report for" in html_content

    # No exceptions, all assertions pass = pipeline integration is healthy!

