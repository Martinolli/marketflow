"""
This script tests the MarketflowFacade with real market data.
It fetches data, performs analysis, retrieves signals, explains them,
and generates a report.
"""

import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_report import MarketflowReport
from marketflow.marketflow_config_manager import create_app_config

def main():
    # --- Step 1: Get real market data ---
    ticker = "NFLX"
    print(f"Fetching real market data for {ticker}...")
    provider = PolygonIOProvider()
    result = provider.get_data(
        ticker=ticker,
        interval="1h",
        period="2d"
    )
    if result is None:
        print("Failed to fetch data")
        return
    price_df, volume_series = result
    
    if price_df is None or volume_series is None or price_df.empty:
        print("Failed to fetch real price/volume data!")
        return

    # --- Step 3: Analyze with Candle Analyzer ---
    facade = MarketflowFacade()

    analysis = facade.analyze_ticker(
        ticker=ticker,
    )

    if analysis is None:
        print("Analysis failed")
        return
    print("Analysis Results:")
    print()
    print(type(analysis))
    print(analysis)

    # --- Step 4: Get signals ---
    # Assuming the facade has a method to get signals based on the analysis
    # This is a placeholder; actual implementation may vary
    if not hasattr(facade, 'get_signals'):
        print("Facade does not support signal retrieval")
        return
    signals = facade.get_signals(ticker="NVDA")
    print()
    print("Signals:")
    if signals is None:
        print("No signals found")
        return
    print("Signals:")
    print(signals)


    # Explanation
    print()
    print("Explaining signal for NVDA...")
    explanation = facade.explain_signal(ticker)
    print()
    if explanation is None:
        print("No explanation found")
        return
    print("Explanation:")
    print(explanation)

    # Analyze ticker at a specific point in time
    sliced_data = {
        "1h": price_df,
        "1d": price_df.resample('D').last()  # Example resampling for daily data
    }
    point_analysis = facade.analyze_ticker_at_point(ticker, sliced_data)
    print()
    print("Point Analysis:")
    print(point_analysis)


    # Batch analyze multiple tickers
    print()
    print("Batch analyzing multiple tickers...")
    # Example tickers for batch analysis
    # Note: Ensure these tickers are valid and available in your data source
    tickers = [ticker]
    batch_results = facade.batch_analyze(tickers, timeframes=[{"interval": "1h", "period": "2d"}])
    print()
    print("Batch Analysis Results:")
    for ticker, result in batch_results.items():
        print(f"{ticker}: {result}")



    # Scan for signals across multiple tickers
    print()
    tickers = [ticker]
    print("Scanning for signals across multiple tickers...")
    scan_results = facade.scan_for_signals(tickers, timeframes=[{"interval": "1h", "period": "2d"}])
    print()
    print("Scan Results:")
    for ticker, result in scan_results.items():
        print(f"{ticker}: {result}")
    # Explain a specific signal
    if 'AAPL' in scan_results:
        explanation = facade.explain_signal("AAPL")
        print()
        print("Signal Explanation for AAPL:")
        print(explanation)
    else:
        print("No signal found for AAPL")


    # Extracting results
    print()
    print("Extracting results...")
    extractor = MarketflowResultExtractor({ticker: analysis})
    print("Extracting data from results...")
    for key in extractor.get_tickers():
        print(f"Ticker: {key}")
        print(f"Current Price: {extractor.get_ticker_data(key).get('current_price')}")
        print(f"Signal: {extractor.get_signal(key)}")
        print(f"Timeframes: {extractor.get_timeframes(key)}")

    for timeframe in extractor.get_timeframes(key):
            print(f"  Timeframe: {timeframe}")
            price_data = extractor.get_price_data(key, timeframe)
            volume_data = extractor.get_volume_data(key, timeframe)
            print(f"    Price Data:\n{price_data.head()}")
            print(f"    Volume Data:\n{volume_data.head()}")
            print(f"    Candle Analysis: {extractor.get_candle_analysis(key, timeframe)}")
            print(f"    Trend Analysis: {extractor.get_trend_analysis(key, timeframe)}")
            print(f"    Pattern Analysis: {extractor.get_pattern_analysis(key, timeframe)}")
            print(f"    Support/Resistance: {extractor.get_support_resistance(key, timeframe)}")
            print(f"    Wyckoff Phases: {extractor.get_wyckoff_phases(key, timeframe)}")
            print(f"    Volume Events: {extractor.get_wyckoff_events(key, timeframe)}")


    print("Data extraction complete.")
    print("Result Extractor Summary:")
    print(extractor.get_data_summary())
    print("Data extraction and analysis completed successfully.")

    print(type(extractor))
    print(extractor)

    print("Creating report...")
    config = create_app_config()
    report_dir = config.REPORT_DIR
    output_dir = f"{report_dir}/{ticker}"
    report = MarketflowReport(extractor, output_dir)

    # Actually generate the report file
    success = report.generate_all_reports_for_ticker(ticker)
    if success:
        print(f"Summary report created successfully in {report_dir}")
    else:
        print("Report creation failed.")
    print("MarketflowFacade real data test completed successfully.")

if __name__ == "__main__":
    main()