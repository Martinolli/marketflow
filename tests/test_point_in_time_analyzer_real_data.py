import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_processor import DataProcessor
from marketflow.marketflow_data_provider import MultiTimeframeProvider
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.point_in_time_analyzer import PointInTimeAnalyzer

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
    print("Processed data structure:", type(processed_data))
    print("Processed data keys:", processed_data.keys())
    print("Processed data shape:", processed_data["price"].shape if "price" in processed_data else "No price data")
    print("Processed data columns:", processed_data["price"].columns.tolist() if "price" in processed_data else "No price data")

    print()
    
    # --- Step 3: Get market flow data parameters ---
    parameters = MarketFlowDataParameters()
    print("Primary timeframe:", parameters.get_primary_timeframe())
    print("All timeframes:", parameters.get_timeframes())

    # --- Step 4: Analyze with Multi Timeframe Analyzer ---
    print("Point in Time Analyzer Initialization...")
    point_in_time_analyzer = PointInTimeAnalyzer()

    sliced_data_by_timeframe = {"1h": processed_data}
    print("Sliced data by timeframe:", {tf: {k: v.shape if isinstance(v, pd.DataFrame) else type(v) for k, v in data.items()} for tf, data in sliced_data_by_timeframe.items()})
    ticker = "NVDA"
    try:
        if point_in_time_analyzer is None:
            print("CRITICAL: self.analyzer is not initialized in VPAFacade. analyze_ticker_at_point cannot function.")

        processed_timeframe_data = {}
        if not sliced_data_by_timeframe:
            print(f"No sliced data provided for {ticker} in analyze_ticker_at_point.")
            return None

        for tf, data_slice in sliced_data_by_timeframe.items():
            print(f"Processing timeframe: {tf}")
            print(f"Data slice keys: {data_slice.keys()}")
            
            if 'price' not in data_slice or not isinstance(data_slice['price'], pd.DataFrame) or data_slice['price'].empty:
                print(f"Empty or invalid price data for timeframe {tf} for ticker {ticker}. Skipping timeframe.")
                continue

            price_data = data_slice['price']
            volume_data = data_slice.get('volume')

            print(f"Price data shape: {price_data.shape}")
            print(f"Price data columns: {price_data.columns.tolist()}")
            print(f"Price data head:\n{price_data.head()}")

            required_cols = ['open', 'high', 'low', 'close']
            if not all(col in price_data.columns for col in required_cols):
                print(f"Price data for {tf} is missing required OHLC columns. Cannot proceed.")
                continue

            if volume_data is None or not isinstance(volume_data, pd.Series):
                print(f"Invalid or missing volume data for timeframe {tf}. Using price data only.")
                processed_timeframe_data[tf] = processor.preprocess_data(price_data)
            else:
                processed_timeframe_data[tf] = processor.preprocess_data(price_data, volume_data)

            print(f"Processed {ticker} data for point-in-time analysis, timeframe {tf}")
            print(f"Processed data shape: {processed_timeframe_data[tf]['price'].shape}, Columns: {processed_timeframe_data[tf]['price'].columns.tolist()}")
        
        if not processed_timeframe_data:
            print(f"No data could be processed for {ticker} in analyze_ticker_at_point after attempting all timeframes.")
            return None

        signals = point_in_time_analyzer.analyze_all(processed_timeframe_data)
        
        primary_tf_key_for_pit = parameters.get_primary_timeframe()
        if primary_tf_key_for_pit not in processed_timeframe_data:
            if processed_timeframe_data:
                primary_tf_key_for_pit = list(processed_timeframe_data.keys())[0]
            else:
                print(f"No processed data available to determine primary timeframe for {ticker}.")
                return None

        rr_info = point_in_time_analyzer.compute_risk_reward(processed_timeframe_data[primary_tf_key_for_pit], signals.get(primary_tf_key_for_pit, {}))
        volatility = point_in_time_analyzer.compute_volatility(processed_timeframe_data[primary_tf_key_for_pit])
        pattern_summary = signals[primary_tf_key_for_pit].get("pattern_summary", "")
        confidence_score = point_in_time_analyzer.compute_confidence_score(signals)

        results = {
            "ticker": ticker,
            "timestamp": processed_timeframe_data[primary_tf_key_for_pit]["price"].index[-1].strftime("%Y-%m-%d %H:%M"),
            "signals": signals,
            "risk_reward": rr_info,
            "volatility": volatility,
            "pattern_summary": pattern_summary,
            "confidence_score": confidence_score,
        }

        for key, value in results.items():
            if isinstance(value, pd.DataFrame):
                print(f"{key} DataFrame shape: {value.shape}, Columns: {value.columns.tolist()}")
            elif isinstance(value, pd.Series):
                print(f"{key} Series length: {len(value)}")
            else:
                print(f"{key}: {value}")

        return results

    except AttributeError as ae:
        if 'self.analyzer' in str(ae) or "'NoneType' object has no attribute 'analyze_all'" in str(ae):
            print(f"❌ Error in analyze_ticker_at_point for {ticker}: 'self.analyzer' is not defined or initialized in VPAFacade. This is a known issue from the original function structure. Details: {str(ae)}")
            print("Detailed error information:")
        else:
            print(f"❌ AttributeError in analyze_ticker_at_point for {ticker}: {str(ae)}")
            print("Detailed error information:")
        return None
    except Exception as e:
        print(f"❌ Error analyzing {ticker} at point-in-time: {str(e)}")
        print("Detailed error information:")
        return None

if __name__ == "__main__":
    main()