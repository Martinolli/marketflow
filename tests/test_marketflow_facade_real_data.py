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
    ticker = "X:BTCUSD"
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
        ticker=ticker
    )

    if analysis is None:
        print("Analysis failed")
        return
    print("Analysis Results:")
    print()
    print(type(analysis))
    print()
    print("--- Step 4: Retrieve Analysis ---")
    print()
    print(analysis)

    for key, value in analysis.items():
        if isinstance(value, pd.DataFrame):
            print(f"DataFrame for {key}:")
            print(value.head())
        elif isinstance(value, pd.Series):
            print(f"Series for {key}:")
            print(value.head())
        else:
            print(f"{key}: {value}")
    print()    

if __name__ == "__main__":
    main()