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

try:
    from marketflow.marketflow_data_provider import MAX_RETRIES
except ImportError:
    MAX_RETRIES = 3

def create_mock_agg(timestamp: int, o: float, h: float, l: float, c: float, v: int):
    return Agg(
        timestamp=timestamp, open=o, high=h, low=l, close=c, volume=v,
        transactions=0, otc=False, vw_avg=0.0, accumulated_volume=0, official_open=0.0, average=0.0,
    )

class TestAsyncDataProvider(unittest.IsolatedAsyncioTestCase):
    @patch('marketflow.marketflow_data_provider.RESTClient')
    async def test_get_multi_timeframe_data_async(self, mock_rest_client_class):
        mock_polygon_client_instance = AsyncMock()
        mock_rest_client_class.return_value = mock_polygon_client_instance

        mock_aggs_1d = [
            create_mock_agg(1672531200000, 150, 155, 149, 152, 10000),
            create_mock_agg(1672617600000, 152, 158, 151, 157, 12000),
        ]
        mock_aggs_4h = [
            create_mock_agg(1672603200000, 151.5, 152.5, 151.0, 152.0, 5000),
        ]

        async def get_aggs_side_effect(*args, **kwargs):
            await asyncio.sleep(0.01)
            if kwargs.get('timespan') == 'day':
                return mock_aggs_1d
            elif kwargs.get('timespan') == 'hour':
                return mock_aggs_4h
            return []

        mock_polygon_client_instance.get_aggs.side_effect = get_aggs_side_effect

        with patch('marketflow.marketflow_data_provider.create_app_config') as mock_create_config:
            mock_config = MagicMock()
            mock_config.get_api_key.return_value = "fake_api_key"
            mock_create_config.return_value = mock_config

            polygon_provider = PolygonIOProvider()
            multi_provider = MultiTimeframeProvider(polygon_provider)

            timeframes_to_fetch = [{'interval': '1d'}, {'interval': '4h'}]
            result = await multi_provider.get_multi_timeframe_data_async("AAPL", timeframes_to_fetch)

            self.assertIn('1d', result, "1d timeframe data should be in the result")
            self.assertIn('4h', result, "4h timeframe data should be in the result")
            self.assertEqual(len(result), 2, "Should have fetched data for 2 timeframes")

            self.assertEqual(len(result['1d']['price_data']), 2)
            self.assertEqual(result['4h']['price_data'].iloc[0]['close'], 152.0)

            mock_polygon_client_instance.get_aggs.assert_any_call(
                ticker='AAPL', multiplier=1, timespan='day', from_=unittest.mock.ANY, to=unittest.mock.ANY, limit=50000
            )
            mock_polygon_client_instance.get_aggs.assert_any_call(
                ticker='AAPL', multiplier=4, timespan='hour', from_=unittest.mock.ANY, to=unittest.mock.ANY, limit=50000
            )
            self.assertEqual(mock_polygon_client_instance.get_aggs.call_count, 2)


    @patch('marketflow.marketflow_data_provider.get_logger')
    @patch('marketflow.marketflow_data_provider.RESTClient')
    async def test_async_fetch_handles_partial_failure(self, mock_rest_client_class, mock_get_logger):
        mock_polygon_client_instance = AsyncMock()
        mock_rest_client_class.return_value = mock_polygon_client_instance

        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        mock_aggs_1d = [create_mock_agg(1672531200000, 150, 155, 149, 152, 10000)]
        async def get_aggs_side_effect(*args, **kwargs):
            await asyncio.sleep(0.01)
            if kwargs.get('timespan') == 'day':
                return mock_aggs_1d
            elif kwargs.get('timespan') == 'hour':
                raise ConnectionError("Simulated network failure for 4h timeframe")
            return []
        mock_polygon_client_instance.get_aggs.side_effect = get_aggs_side_effect

        with patch('marketflow.marketflow_data_provider.create_app_config') as mock_create_config:
            mock_config = MagicMock()
            mock_config.get_api_key.return_value = "fake_api_key"
            mock_create_config.return_value = mock_config

            polygon_provider = PolygonIOProvider()
            multi_provider = MultiTimeframeProvider(polygon_provider)

            timeframes_to_fetch = [{'interval': '1d'}, {'interval': '4h'}]
            result = await multi_provider.get_multi_timeframe_data_async("AAPL", timeframes_to_fetch)

            self.assertIn('1d', result, "Successful '1d' timeframe data should be in the result")
            self.assertNotIn('4h', result, "Failed '4h' timeframe data should NOT be in the result")
            self.assertEqual(len(result), 1, "Result should contain data for only the one successful timeframe")

            # Assertions for the logs:
            # Check for the warning messages during retries (2 warnings for 3 attempts)
            # The error message string includes the exception type, e.g., "ConnectionError('Simulated network failure...')"
            # Now that _handle_error should correctly categorize, the message will start with "Network error..."
            expected_error_part = "Simulated network failure for 4h timeframe"
            expected_warning_prefix = "Network error fetching data for AAPL at 4h timeframe:"

            warning_calls = [
                call_args for call_args in mock_logger.warning.call_args_list
                if len(call_args.args) > 0 and expected_warning_prefix in call_args.args[0] and expected_error_part in call_args.args[0]
            ]
            # Expected 2 warnings from PolygonIOProvider._handle_error + 1 warning from MultiTimeframeProvider
            self.assertEqual(len(warning_calls), 2, "Expected 2 warning calls from _handle_error with the specific message")
            # And then assert the total warning calls
            self.assertEqual(mock_logger.warning.call_count, 3, "Expected 3 total warning calls (2 from provider, 1 from multi-timeframe)")
            mock_logger.warning.assert_any_call("No price data returned for AAPL at 4h timeframe. Skipping.")

            # Check for the final error message from _handle_error
            error_from_handle_error_calls = [
                call_args for call_args in mock_logger.error.call_args_list
                if len(call_args.args) > 0 and expected_warning_prefix in call_args.args[0] and expected_error_part in call_args.args[0]
            ]
            self.assertEqual(len(error_from_handle_error_calls), 1, "Expected 1 error call from _handle_error")

            # Check for the error message from _fetch_data_core's else block
            expected_error_from_fetch_data_core_prefix = "Error fetching data for AAPL at 4h timeframe:"
            error_from_fetch_data_core_calls = [
                call_args for call_args in mock_logger.error.call_args_list
                if len(call_args.args) > 0 and expected_error_from_fetch_data_core_prefix in call_args.args[0] and expected_error_part in call_args.args[0]
            ]
            self.assertEqual(len(error_from_fetch_data_core_calls), 1, "Expected 1 error call from _fetch_data_core else block")

            # Total error calls should be 2
            self.assertEqual(mock_logger.error.call_count, 2)

            # Ensure get_aggs was called for both, even if one failed (3 times for the failing one due to retries)
            # The 1d call + 3 calls for the 4h (initial + 2 retries)
            self.assertEqual(mock_polygon_client_instance.get_aggs.call_count, 1 + MAX_RETRIES)


    @patch('marketflow.marketflow_data_provider.get_logger')
    @patch('marketflow.marketflow_data_provider.RESTClient')
    async def test_async_fetch_returns_empty_when_no_timeframes(self, mock_rest_client_class, mock_get_logger):
        mock_polygon_client_instance = AsyncMock()
        mock_rest_client_class.return_value = mock_polygon_client_instance

        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with patch('marketflow.marketflow_data_provider.create_app_config') as mock_create_config:
            mock_config = MagicMock()
            mock_config.get_api_key.return_value = "fake_api_key"
            mock_create_config.return_value = mock_config

            polygon_provider = PolygonIOProvider()
            multi_provider = MultiTimeframeProvider(polygon_provider)

            result = await multi_provider.get_multi_timeframe_data_async("AAPL", [])
            self.assertEqual(result, {}, "Result should be empty if no timeframes are provided")
            mock_polygon_client_instance.get_aggs.assert_not_called()


    @patch('marketflow.marketflow_data_provider.get_logger')
    @patch('marketflow.marketflow_data_provider.RESTClient')
    async def test_async_fetch_handles_invalid_interval(self, mock_rest_client_class, mock_get_logger):
        mock_polygon_client_instance = AsyncMock()
        mock_rest_client_class.return_value = mock_polygon_client_instance

        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        mock_aggs_1d = [create_mock_agg(1672531200000, 150, 155, 149, 152, 10000)]
        async def get_aggs_side_effect(*args, **kwargs):
            await asyncio.sleep(0.01)
            if kwargs.get('timespan') == 'day':
                return mock_aggs_1d
            return []
        mock_polygon_client_instance.get_aggs.side_effect = get_aggs_side_effect

        with patch('marketflow.marketflow_data_provider.create_app_config') as mock_create_config:
            mock_config = MagicMock()
            mock_config.get_api_key.return_value = "fake_api_key"
            mock_create_config.return_value = mock_config

            polygon_provider = PolygonIOProvider()
            multi_provider = MultiTimeframeProvider(polygon_provider)

            timeframes_to_fetch = [{'interval': '1d'}, {'interval': 'bad'}]
            result = await multi_provider.get_multi_timeframe_data_async("AAPL", timeframes_to_fetch)

            self.assertIn('1d', result, "Valid '1d' timeframe should be in the result")
            self.assertNotIn('bad', result, "Invalid 'bad' timeframe should not be in the result")
            
            # Check that a warning was logged for the unsupported interval format
            # It's logged twice: once by _parse_interval, once by _fetch_data_core
            mock_logger.error.assert_any_call("Unsupported interval format: bad")
            self.assertEqual(mock_logger.error.call_count, 2) # Expect two error calls for the invalid interval
            
            mock_polygon_client_instance.get_aggs.assert_called_once()
            mock_polygon_client_instance.get_aggs.assert_called_with(
                ticker='AAPL', multiplier=1, timespan='day', from_=unittest.mock.ANY, to=unittest.mock.ANY, limit=50000
            )


if __name__ == '__main__':
    unittest.main()
