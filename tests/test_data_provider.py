"""# test_data_provider.py
Unit tests for the PolygonIOProvider class in the Marketflow data provider module.
This module tests the functionality of the PolygonIOProvider class, ensuring it correctly retrieves and processes market data.
"""
import pytest
import pandas as pd
import os
import sys
from types import SimpleNamespace
import warnings

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="polygon")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_config_manager import ConfigManager
from marketflow.marketflow_logger import get_logger

# Initialize logger
logger = get_logger(
            module_name="Test_Config_Manager_Marketflow",
            log_level="DEBUG",
            log_file=r"C:\Users\Aspire5 15 i7 4G2050\marketflow\.marketflow\logs\marketflow_test_data_provider.log"
        )

# Dummy client to simulate Polygon API responses for testing
class DummyClient:
    """A mock client to simulate Polygon.io API responses."""
    def get_aggs(self, ticker, multiplier, timespan, from_, to, limit):
        return [
            SimpleNamespace(timestamp=pd.Timestamp('2021-01-01').timestamp() * 1000, open=100, high=105, low=95, close=102, volume=10000),
            SimpleNamespace(timestamp=pd.Timestamp('2021-01-02').timestamp() * 1000, open=102, high=106, low=98, close=104, volume=12000),
        ]
    logger.info("DummyClient initialized with mock data.")

@pytest.fixture
def mock_provider(monkeypatch):
    """
    Pytest fixture to create a PolygonIOProvider instance with a mocked API key
    and a dummy client.
    """
    monkeypatch.setattr(ConfigManager, "get_api_key", lambda self, service: "dummy_key")
    logger.info("Mocking ConfigManager.get_api_key to return 'dummy_key'")
    # Create a PolygonIOProvider instance with a dummy client
    provider = PolygonIOProvider()
    logger.info("Creating PolygonIOProvider instance for testing.")
    # Assign the dummy client to the provider
    provider.client = DummyClient()
    logger.info("Assigning DummyClient to PolygonIOProvider instance.")
    # Ensure the provider is ready for testing
    assert isinstance(provider, PolygonIOProvider), "Provider should be an instance of PolygonIOProvider"
    logger.info("Mock provider setup complete.")
    return provider

def test_polygon_provider_get_data_success(mock_provider):
    """
    Test the PolygonIOProvider's get_data method for a successful data fetch.
    Ensures that the returned price DataFrame and volume Series are correct.
    """
    price_df, volume_series = mock_provider.get_data(
        "AAPL",
        interval="1d",
        start_date="2021-01-01",
        end_date="2021-01-02"
    )
    logger.info("Testing PolygonIOProvider.get_data for successful data fetch.")
    # Check if the returned data is as expected
    logger.debug("Checking return types and structure of the returned data.")

    # 1. Check return types
    assert isinstance(price_df, pd.DataFrame), "price_df should be a DataFrame"
    logger.debug("price_df is a DataFrame.")
    assert isinstance(volume_series, pd.Series), "volume_series should be a Series"
    logger.debug("volume_series is a Series.")
    assert isinstance(volume_series, pd.Series), "volume_series should be a Series"

    # 2. Check DataFrame structure
    expected_columns = {"open", "high", "low", "close"}
    logger.debug("Checking DataFrame columns and shape.")
    # Ensure the DataFrame has the expected columns and shape
    logger.debug(f"Expected columns: {expected_columns}")
    logger.debug(f"Actual columns: {set(price_df.columns)}")
    assert set(price_df.columns) == expected_columns, f"Expected columns: {expected_columns}, got: {set(price_df.columns)}"
    logger.debug("DataFrame columns match expected columns.")
    # Check the shape of the DataFrame
    logger.debug(f"Expected shape: (2, 4), Actual shape: {price_df.shape}")
    assert price_df.shape == (2, 4), f"Expected shape (2, 4), got {price_df.shape}"
    logger.debug("DataFrame shape matches expected shape.")
    assert not price_df.empty, "price_df should not be empty"

    # 3. Check DataFrame and Series content
    logger.debug("Checking content of price_df and volume_series.")
    # Ensure the first row has the expected values
    logger.debug("Checking first row values in price_df.")
    assert price_df.iloc[0]['open'] == 100
    logger.debug("First row open price is correct.")
    assert price_df.iloc[0]['high'] == 105
    logger.debug("First row high price is correct.")
    assert price_df.iloc[1]['close'] == 104
    logger.debug("Second row close price is correct.")
    # Ensure the volume series has the expected values
    logger.debug("Checking volume_series values.")
    assert volume_series.iloc[0] == 10000
    logger.debug("First volume value is correct.")
    assert volume_series.iloc[1] == 12000
    logger.debug("Second volume value is correct.")
    # Ensure the length of the volume series matches the DataFrame
    logger.debug(f"Volume series length: {len(volume_series)}, expected: 2")
    assert len(volume_series) == 2, "Volume series should have 2 entries"
    logger.debug("Volume series length matches expected length.")

    # 4. Check index properties (robust to named index)
    logger.debug("Checking index properties of price_df and volume_series.")
    expected_index = pd.date_range(start='2021-01-01', end='2021-01-02', freq='D').tz_localize('UTC')
    expected_index.freq = None
    expected_index = expected_index.rename('timestamp')
    logger.debug(f"Expected index: {expected_index}")

    # Ensure the index of the DataFrame matches the expected index
    logger.debug(f"Actual index: {price_df.index}")

    logger.debug("Comparing price_df index with expected index.")
    pd.testing.assert_index_equal(price_df.index, expected_index, check_names=True)
    logger.debug("Price DataFrame index matches expected index.")

    # Update the volume series index check as well
    logger.debug(f"Volume series index: {volume_series.index}")
    pd.testing.assert_index_equal(volume_series.index, expected_index, check_names=True)
    logger.debug("Volume series index matches expected index.")

    # Ensure the indices of price_df and volume_series match
    logger.debug("Asserting indices of price_df and volume_series match.")
    pd.testing.assert_index_equal(price_df.index, volume_series.index)
    logger.debug("Indices of price_df and volume_series match.")

def test_polygon_provider_no_data(monkeypatch):
    """
    Test the PolygonIOProvider's get_data method when the API returns no data.
    """
    logger.info("Testing PolygonIOProvider.get_data with no data returned.")
    # Mock the ConfigManager to return a dummy API key
    monkeypatch.setattr(ConfigManager, "get_api_key", lambda self, service: "dummy_key")
    logger.info("Mocking ConfigManager.get_api_key to return 'dummy_key'")
    provider = PolygonIOProvider()
    logger.debug("Creating PolygonIOProvider instance for testing with no data.")
    provider.client = type("NoDataClient", (), {"get_aggs": lambda *a, **k: []})()
    logger.debug("Assigning NoDataClient to PolygonIOProvider instance.")
    result = provider.get_data(
        "NODATA",
        interval="1d",
        start_date="2021-01-01",
        end_date="2021-01-02"
    )
    logger.debug("Checking if result is None when no data is returned.")
    # Check if the result is None when no data is returned
    logger.debug("Asserting that result is None.")  
    assert result is None, "Expected None when no data is returned"
    logger.debug("Result is None as expected when no data is returned.")
