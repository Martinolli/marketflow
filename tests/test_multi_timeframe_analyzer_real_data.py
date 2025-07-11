import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_processor import DataProcessor
from marketflow.marketflow_data_provider import MultiTimeframeProvider
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.multi_timeframe_analyzer import MultiTimeframeAnalyzer

def main():
    # --- Step 1: Get real market data ---
    provider = PolygonIOProvider()
    result = provider.get_data(
        ticker="NVDA",
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
    print(processed_data)
    print()

    # Get Parameters
    parameters = MarketFlowDataParameters()
    timeframes = parameters.get_timeframes()


    # --- Step 3: Get Multi Timeframe Data ---
    print("Multi Timeframe Provider Initialization...")
    multitimeframe_provider = MultiTimeframeProvider(provider)
    timeframe_data =multitimeframe_provider.get_multi_timeframe_data(ticker="NFLX", timeframes=timeframes)
    print("Multi Timeframe Data Done:")
    print()
    print(timeframe_data)

    # --- Step 4: Analyze with Multi Timeframe Analyzer ---
    print("Multi Timeframe Analyzer Initialization...")
    multi_timeframe_analyzer = MultiTimeframeAnalyzer()
    time_frame_analysis, confirmations = multi_timeframe_analyzer.analyze_multiple_timeframes(timeframe_data)
    print("Multi Timeframe Analysis Done:")
    print()
    # Display the analysis results

    print("Multi Timeframe Analysis Results:")
    print("Timeframe Analysis:")
    for time_frame in timeframe_data:
        print(f"Timeframe: {time_frame}")
        analysis = time_frame_analysis.get(time_frame, {})
        for key, value in analysis.items():
            print(f"  {key}: {value}")

    print()
    print("Confirmations:")
    print(confirmations)
    print()

if __name__ == "__main__":
    main()