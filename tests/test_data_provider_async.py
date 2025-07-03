"""
Test Suite for Asynchronous Data Provider Functionality

This test suite validates the asynchronous data fetching capabilities of the
marketflow_data_provider module, ensuring concurrent requests work as expected.
"""

import unittest
import asyncio
import pandas as pd
from unittest.mock import patch, AsyncMock, MagicMock

# Add project root to path to allow for module imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketflow.marketflow_data_provider import PolygonIOProvider, MultiTimeframeProvider
from polygon.rest.models import Agg

# Helper to create mock aggregate data, simulating the Polygon client's response
def create_mock_agg(timestamp: int, o: float, h: float, l: float, c: float, v: int) -> MagicMock:
    """Creates a mock Agg object."""
    agg = MagicMock(spec=Agg)
    agg.timestamp = timestamp
    agg.open = o
    agg.high = h
    agg.low = l
    agg.close = c
    agg.volume = v
    return agg

class TestAsyncDataProvider(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for the asynchronous features of the DataProvider.
    Inherits from IsolatedAsyncioTestCase to handle async test methods.
    """

    @patch('marketflow.marketflow_data_provider.RESTClient')
    async def test_get_multi_timeframe_data_async(self, mock_rest_client_class):
        """
        Test that get_multi_timeframe_data_async fetches data concurrently and correctly.
        Note: The test method itself must be declared with `async def`.
        """
        # --- 1. Setup Mocks ---
        # Create separate mocks for the sync and async clients that will be returned
        # by the patched RESTClient constructor.
        mock_sync_client = MagicMock()
        mock_async_client = AsyncMock()

        # This side effect will return the async mock if `use_async=True` is passed
        def client_side_effect(key, use_async=False):
            return mock_async_client if use_async else mock_sync_client
        
        mock_rest_client_class.side_effect = client_side_effect

        # Define the mock data to be returned by the API call
        mock_aggs_1d = [
            create_mock_agg(1672531200000, 150, 155, 149, 152, 10000), # 2023-01-01
            create_mock_agg(1672617600000, 152, 158, 151, 157, 12000), # 2023-01-02
        ]
        mock_aggs_4h = [
            create_mock_agg(1672603200000, 151.5, 152.5, 151.0, 152.0, 5000), # 2023-01-01 20:00
        ]

        # Configure the mock's side_effect to return different data based on the call
        async def get_aggs_side_effect(*args, **kwargs):
            # Simulate a small network delay
            await asyncio.sleep(0.01)
            if kwargs.get('timespan') == 'day':
                return mock_aggs_1d
            elif kwargs.get('timespan') == 'hour':
                return mock_aggs_4h
            return []

        mock_async_client.get_aggs.side_effect = get_aggs_side_effect

        # --- 2. Instantiate Providers ---
        # We patch the config manager to avoid needing real API keys for the test
        with patch('marketflow.marketflow_data_provider.create_app_config') as mock_create_config:
            mock_config = MagicMock()
            mock_config.get_api_key.return_value = "fake_api_key"
            mock_create_config.return_value = mock_config

            polygon_provider = PolygonIOProvider()
            multi_provider = MultiTimeframeProvider(polygon_provider)

            # --- 3. Execute the Asynchronous Call ---
            timeframes_to_fetch = [{'interval': '1d'}, {'interval': '4h'}]
            result = await multi_provider.get_multi_timeframe_data_async("AAPL", timeframes_to_fetch)

            # --- 4. Assertions ---
            self.assertIn('1d', result, "1d timeframe data should be in the result")
            self.assertIn('4h', result, "4h timeframe data should be in the result")
            self.assertEqual(len(result), 2, "Should have fetched data for 2 timeframes")

            # Check the content of the returned dataframes
            self.assertEqual(len(result['1d']['price_data']), 2)
            self.assertEqual(result['4h']['price_data'].iloc[0]['close'], 152.0)

            # Verify that the async API call was made twice (once for each timeframe)
            self.assertEqual(mock_async_client.get_aggs.call_count, 2)

if __name__ == '__main__':
    unittest.main()
