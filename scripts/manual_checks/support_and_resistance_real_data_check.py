import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_processor import DataProcessor
from marketflow.support_resistance_analyzer import SupportResistanceAnalyzer

def main():
    # --- Step 1: Get real market data ---
    provider = PolygonIOProvider()
    result = provider.get_data(
        ticker="NFLX",
        interval="1h",
        period="10d"
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
    print("Processed Data Done:")
    print()

    # --- Step 3: Analyze with Candle Analyzer ---
    print("Support and Resistance Analyzer Initialization...")
    support_resistane = SupportResistanceAnalyzer()
    print("Support and Resistance Analysis...")
    # Assuming processed_data['price'] is a DataFrame and you want to analyze the first candle
    
    print()
    sr_analysis = support_resistane.analyze_support_resistance(processed_data)
    print()
    print(sr_analysis)

    print("Support and Resistance Analysis Done:")

    print()

    print("Support and Resistance Analysis Results:")

    for key, value in sr_analysis.items():
        if isinstance(value, pd.DataFrame):
            print(f"{key}:\n{value.head()}")
            print()
        else:
            print(f"{key}: {value}")
        print("Support and Resistance Analysis Completed.")


if __name__ == "__main__":
    main()