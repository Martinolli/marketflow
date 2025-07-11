import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_processor import DataProcessor
from marketflow.marketflow_facade import VPAFacade

def main():
    # --- Step 1: Get real market data ---
    provider = PolygonIOProvider()
    result = provider.get_data(
        ticker="NFLX",
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
    facade = VPAFacade()

    analysis = facade.analyze_ticker(
        ticker="NVDA",
        timeframes=[{"interval": "1h", "period": "2d"}]
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
    explanation = facade.explain_signal(ticker="NVDA")
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
    point_analysis = facade.analyze_ticker_at_point("NVDA", sliced_data)
    print()
    print("Point Analysis:")
    print(point_analysis)


    # Batch analyze multiple tickers
    print()
    print("Batch analyzing multiple tickers...")
    # Example tickers for batch analysis
    # Note: Ensure these tickers are valid and available in your data source
    tickers = ["MSFT", "GOOGL"]
    batch_results = facade.batch_analyze(tickers, timeframes=[{"interval": "1h", "period": "2d"}])
    print()
    print("Batch Analysis Results:")
    for ticker, result in batch_results.items():
        print(f"{ticker}: {result}")



    # Scan for signals across multiple tickers
    print()
    tickers = ["NVDA"]
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

if __name__ == "__main__":
    main()