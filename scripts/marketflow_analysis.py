"""
This script uses the MarketflowFacade with real market data.
It fetches data, performs analysis, retrieves signals, explains them,
generates a report, extracts results, and saves them in a specified output directory.
This script also call marketflow_snapshot.py to save the analysis results.
"""

import pandas as pd
from datetime import datetime
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_report import MarketflowReport
from marketflow.marketflow_snapshot import MarketflowSnapshot
from marketflow.marketflow_config_manager import create_app_config

def main():
    # --- Step 1: Get real market data ---
    ticker = "GSLC"
    print(f"Fetching real market data for {ticker}...")
    provider = PolygonIOProvider()
    result = provider.get_data(
        ticker=ticker
    )
    
    # --- Step 2: Analyze with Candle Analyzer ---
    facade = MarketflowFacade()

    analysis = facade.analyze_ticker(ticker=ticker)

    """

    # --- Step2: Save analysis snapshot ---
    # Save analysis snapshot and DataFrames
    config = create_app_config()
    snapshot_report_dir = config.SNAPSHOT_OUTPUT_DIR
    output_dir = f"{snapshot_report_dir}/{ticker}"
    snapshot_manager = MarketflowSnapshot(output_dir=output_dir, enable_compression=True)
    actual_date = datetime.now().strftime("%Y%m%d")

    saved_paths = snapshot_manager.save_enhanced_snapshot(analysis_result=analysis, ticker="GSLC")

    print(f"Analysis snapshot saved at: {saved_paths['snapshot']}")
    for df_name, df_path in saved_paths['dataframes'].items():
        print(f"DataFrame {df_name} saved at: {df_path}")
"""

    # --- Step 3: Extracting results ---
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