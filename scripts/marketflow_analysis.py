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
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("marketflow_analysis")
config_manager = create_app_config(logger=logger)

def main():
    # --- Step 1: Get real market data ---
    # Technology and Defense industry tickers
    tickers = [
        # Technology
        "AAPL",   # Apple Inc.
        "MSFT",   # Microsoft Corporation
        "GOOGL",  # Alphabet Inc.
        "NVDA",   # NVIDIA Corporation
        "AMD",    # Advanced Micro Devices
        "INTC",   # Intel Corporation
        "CSCO",   # Cisco Systems
        "ORCL",   # Oracle Corporation
        "CRM",    # Salesforce, Inc.
        "ADBE",   # Adobe Inc.
        # Defense
        "LMT",    # Lockheed Martin
        "RTX",    # RTX Corporation (Raytheon)
        "NOC",    # Northrop Grumman
        "GD",     # General Dynamics
        "BA",     # Boeing
        "HII",    # Huntington Ingalls Industries
        "LHX",    # L3Harris Technologies
        "TXT",    # Textron Inc.
        "BWXT",   # BWX Technologies
        "LDOS"    # Leidos Holdings
    ]
    
    # Analyse the tickers and save the results

    for ticker in tickers:
        facade = MarketflowFacade()
        analysis = facade.analyze_ticker(ticker=ticker)
        extractor = MarketflowResultExtractor({ticker: analysis})
        logger.info("Extracting data from results...")
        for key in extractor.get_tickers():
            logger.info(f"Ticker: {key}")
            logger.info(f"Current Price: {extractor.get_ticker_data(key).get('current_price')}")
            logger.info(f"Signal: {extractor.get_signal(key)}")
            logger.info(f"Timeframes: {extractor.get_timeframes(key)}")

        for timeframe in extractor.get_timeframes(key):
            logger.info(f"  Timeframe: {timeframe}")
            price_data = extractor.get_price_data(key, timeframe)
            volume_data = extractor.get_volume_data(key, timeframe)
            logger.info(f"    Price Data:\n{price_data.head()}")
            logger.info(f"    Volume Data:\n{volume_data.head()}")
            logger.info(f"    Candle Analysis: {extractor.get_candle_analysis(key, timeframe)}")
            logger.info(f"    Trend Analysis: {extractor.get_trend_analysis(key, timeframe)}")
            logger.info(f"    Pattern Analysis: {extractor.get_pattern_analysis(key, timeframe)}")
            logger.info(f"    Support/Resistance: {extractor.get_support_resistance(key, timeframe)}")
            logger.info(f"    Wyckoff Phases: {extractor.get_wyckoff_phases(key, timeframe)}")
            logger.info(f"    Volume Events: {extractor.get_wyckoff_events(key, timeframe)}")
        logger.info("Data extraction complete.")
        logger.info("Result Extractor Summary:")
        logger.info(extractor.get_data_summary())
        logger.info("Data extraction and analysis completed successfully.")
        logger.info(f"Extractor type: {type(extractor)}")
        logger.info(f"Extractor object: {extractor}")

        logger.info("Creating report...")
        config = create_app_config()
        report_dir = config.REPORT_DIR
        output_dir = f"{report_dir}/{ticker}"
        report = MarketflowReport(extractor, output_dir)

        # Actually generate the report file
        success = report.generate_all_reports_for_ticker(ticker)
        if success:
            logger.info(f"Summary report created successfully in {report_dir}")
        else:
            logger.error("Report creation failed.")
        logger.info("MarketflowFacade real data test completed successfully.")
   

if __name__ == "__main__":
    main()