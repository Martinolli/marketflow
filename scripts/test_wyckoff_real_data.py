import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_processor import DataProcessor
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_wyckoff import WyckoffAnalyzer

def main():
    # --- Step 1: Get real market data ---
    provider = PolygonIOProvider()
    result = provider.get_data(
        ticker="AAPL",
        interval="1d",
        period="1y"
    )
    if result is None:
        print("Failed to fetch data")
        return
    price_df, volume_series = result
    
    if price_df is None or volume_series is None or price_df.empty:
        print("Failed to fetch real price/volume data!")
        return

    # --- Step 2: Preprocess the data ---
    processor = DataProcessor()
    processed_data = processor.preprocess_data(price_df, volume_series)

    # --- Step 3: Analyze with WyckoffAnalyzer ---
    wyckoff = WyckoffAnalyzer(processed_data)
    phases, events, trading_ranges = wyckoff.run_analysis()

    # --- Step 4: Print results ---
    print("\nWyckoff Events:")
    for event in events:
        print(event)
    print("\nWyckoff Phases:")
    for phase in phases[:10]:  # Print first 10 for brevity
        print(phase)
    print("\nTrading Ranges:")
    for tr in trading_ranges:
        print(tr)

    # Optional: Annotate and inspect the DataFrame
    annotated = wyckoff.annotate_chart()
    print("\nAnnotated Data (last 5 rows):")
    print(annotated.tail())

if __name__ == "__main__":
    main()