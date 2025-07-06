"""
Simple Test Script for MarketFlow Data Provider

This script provides a straightforward way to test the core functionality of the
PolygonIOProvider and MultiTimeframeProvider, ensuring both synchronous and
asynchronous data fetching methods work as expected.

Prerequisites:
1. Make sure you have a `.env` file in the root of the `marketflow` project.
2. The `.env` file must contain your Polygon.io API key, like this:
   POLYGON_API_KEY="your_key_here"

To run:
`python tests/test_data_provider_simple.py`
"""

import asyncio
import os
import sys

# Add project root to path to allow for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketflow.marketflow_data_provider import MultiTimeframeProvider, PolygonIOProvider

def test_sync_get_data():
    """Tests the synchronous get_data method."""
    print("--- Testing synchronous get_data() ---")
    try:
        provider = PolygonIOProvider()
        ticker = "AAPL"

        print(f"Fetching data for {ticker}...")
        result = provider.get_data(ticker=ticker, interval="1d", period="30d")

        if result:
            price_df, volume_series = result
            if not price_df.empty:
                print(f"Successfully fetched {len(price_df)} data points.")
                print("Price Data Head:")
                print(price_df.head())
                print("\nVolume Data Head:")
                print(volume_series.head())
            else:
                print("Data fetch was successful, but no data was returned.")
        else:
            print("Failed to fetch data.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("-" * 40 + "\n")

async def test_async_get_data():
    """Tests the asynchronous get_data_async method."""
    print("--- Testing asynchronous get_data_async() ---")
    try:
        provider = PolygonIOProvider()
        ticker = "MSFT"  # Use a different ticker for variety

        print(f"Fetching data for {ticker}...")
        result = await provider.get_data_async(ticker=ticker, interval="1h", period="7d")

        if result:
            price_df, volume_series = result
            if not price_df.empty:
                print(f"Successfully fetched {len(price_df)} data points.")
                print("Price Data Head:")
                print(price_df.head())
                print("\nVolume Data Head:")
                print(volume_series.head())
            else:
                print("Data fetch was successful, but no data was returned.")
        else:
            print("Failed to fetch data.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("-" * 40 + "\n")

def test_sync_get_multi_timeframe_data():
    """Tests the synchronous get_multi_timeframe_data method."""
    print("--- Testing synchronous get_multi_timeframe_data() ---")
    try:
        polygon_provider = PolygonIOProvider()
        multi_provider = MultiTimeframeProvider(polygon_provider)
        ticker = "GOOGL"
        timeframes = [
            {'interval': '1d', 'period': '30d'},
            {'interval': '4h', 'period': '15d'}
        ]

        print(f"Fetching multi-timeframe data for {ticker}...")
        results = multi_provider.get_multi_timeframe_data(ticker=ticker, timeframes=timeframes)

        if results:
            print(f"Successfully fetched data for {len(results)} timeframes.")
            for tf, data in results.items():
                print(f"\n--- Timeframe: {tf} ---")
                if 'price_data' in data and 'volume_data' in data:
                    price_df, volume_series = data['price_data'], data['volume_data']
                    if not price_df.empty:
                        print(f"Fetched {len(price_df)} data points.")
                        print("Price Data Head:")
                        print(price_df.head())
                        print("\nVolume Data Head:")
                        print(volume_series.head())
                    else:
                        print("Data fetch was successful, but no data was returned for this timeframe.")
                else:
                    print(f"Data for timeframe {tf} is missing 'price_data' or 'volume_data'.")
        else:
            print("Failed to fetch multi-timeframe data.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("-" * 40 + "\n")

async def test_async_get_multi_timeframe_data():
    """Tests the asynchronous get_multi_timeframe_data_async method."""
    print("--- Testing asynchronous get_multi_timeframe_data_async() ---")
    try:
        polygon_provider = PolygonIOProvider()
        multi_provider = MultiTimeframeProvider(polygon_provider)
        ticker = "AMZN"
        timeframes = [
            {'interval': '1d', 'period': '15d'},
            {'interval': '30m', 'period': '5d'}
        ]

        print(f"Fetching multi-timeframe data for {ticker} asynchronously...")
        results = await multi_provider.get_multi_timeframe_data_async(ticker=ticker, timeframes=timeframes)

        if results:
            print(f"Successfully fetched data for {len(results)} timeframes.")
            for tf, data in results.items():
                print(f"\n--- Timeframe: {tf} ---")
                if 'price_data' in data and 'volume_data' in data:
                    price_df, volume_series = data['price_data'], data['volume_data']
                    if not price_df.empty:
                        print(f"Fetched {len(price_df)} data points.")
                        print("Price Data Head:")
                        print(price_df.head())
                        print("\nVolume Data Head:")
                        print(volume_series.head())
                    else:
                        print("Data fetch was successful, but no data was returned for this timeframe.")
                else:
                    print(f"Data for timeframe {tf} is missing 'price_data' or 'volume_data'.")
        else:
            print("Failed to fetch multi-timeframe data.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("-" * 40 + "\n")

def run_sync_tests():
    """Runs all synchronous tests."""
    print("--- Running Synchronous Tests ---")
    test_sync_get_data()
    test_sync_get_multi_timeframe_data()
    print("--- Synchronous Tests Completed ---\n")

async def run_async_tests():
    """Runs all asynchronous tests."""
    print("--- Running Asynchronous Tests ---")
    await test_async_get_data()
    await test_async_get_multi_timeframe_data()
    print("--- Asynchronous Tests Completed ---\n")

if __name__ == "__main__":
    print("Starting MarketFlow Data Provider tests...")
    # Run sync tests first, outside of any event loop
    run_sync_tests()
    # Then, run async tests inside a new event loop
    asyncio.run(run_async_tests())
    print("Tests completed.")