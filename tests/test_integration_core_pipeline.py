import os
import pytest
from pathlib import Path
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_report import MarketflowReport

# Optional: Configure your test output directory
TEST_OUTPUT_DIR = Path("test_outputs")
TEST_OUTPUT_DIR.mkdir(exist_ok=True)

@pytest.fixture(scope="module")
def facade():
    # Here, use a mock config or provider for faster, deterministic tests
    # If you have a MockProvider, substitute it in your Facade or config
    return MarketflowFacade()

def test_full_marketflow_pipeline(facade):
    ticker = "NVDA"  # or any test ticker you have data for
    timeframes =  [{"interval": "1d", "period": "60d"}]  # or just ["1h"] if you want to keep it simple

    # 1. Run core analysis pipeline
    result = facade.analyze_ticker(ticker)
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
    report = MarketflowReport(extractor, output_dir=str(TEST_OUTPUT_DIR))
    summary = report.create_summary_report(ticker)
    html = report.create_html_report(ticker)
    json_ = report.create_json_report(ticker)

    assert summary is True
    assert html is True
    assert json_ is True

    # 5. Check the output files exist and are non-empty
    expected_files = [
        TEST_OUTPUT_DIR / f"{ticker}_summary_report.txt",
        TEST_OUTPUT_DIR / f"{ticker}_report.html",
        TEST_OUTPUT_DIR / f"{ticker}_report.json",
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

