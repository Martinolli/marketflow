import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_processor import DataProcessor
from marketflow.pattern_recognizer import PatternRecognizer

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

    # --- Step 2: Preprocess the data ---
    processor = DataProcessor()
    processed_data = processor.preprocess_data(price_df, volume_series)
    print("Processed Data Done:")
    print()

    # --- Step 3: Pattern Recognizer ---
    print("Pattern Recognizer  Initialization...")
    pattern_recognizer = PatternRecognizer()
    print("Pattern Recognizer...")
    # Assuming processed_data['price'] is a DataFrame and you want to analyze the first candle
    results = []
    for number in range(5):
        current_idx = processed_data["price"].index[-number - 1]  # Get the last 10 candles
        print(f"Trend Analysis at index: {current_idx}")
        result = pattern_recognizer.identify_patterns(processed_data, current_idx)
        results.append(result)
    print("Pattern Recognizer Done:")

    print()
    print("Pattern Recognizer Results:")
    print()
    # Display the results

    for result in results:
        for key, value in result.items():
            if isinstance(value, pd.DataFrame):
                print(f"{key}:\n{value.head()}")
                print()
            else:
                print(f"{key}: {value}")
    print("Pattern Recognizer Completed.")

if __name__ == "__main__":
    main()