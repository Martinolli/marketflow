"""# test_data_provider.py
Unit tests for the PolygonIOProvider class in the Marketflow data provider module.
This module tests the functionality of the PolygonIOProvider class, ensuring it correctly retrieves and processes market data.
"""
# Import necessary modules and classes for testing
import pytest
import pandas as pd
import os
import sys
from types import SimpleNamespace
import warnings

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="polygon")

# It's generally better to install the package in editable mode (`pip install -e .`)
# than to modify sys.path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_config_manager import ConfigManager


# Dummy client to simulate Polygon API responses for testing
# This client will return predefined data instead of making actual API calls.
# It is used to isolate the tests from external dependencies and ensure consistent results.
class DummyClient:
    """A mock client to simulate Polygon.io API responses."""
    def get_aggs(self, ticker, multiplier, timespan, from_, to, limit):
        """Simulates fetching aggregate data, returning a fixed dataset."""
        # This data simulates the structure returned by the Polygon API
        # Each entry corresponds to a daily aggregation with OHLCV data
        return [
            SimpleNamespace(timestamp=1609459200000, open=100, high=105, low=95, close=102, volume=10000), # 2021-01-01
            SimpleNamespace(timestamp=1609545600000, open=102, high=106, low=98, close=104, volume=12000), # 2021-01-02
        ]

@pytest.fixture
def mock_provider(monkeypatch):
    """
    Pytest fixture to create a PolygonIOProvider instance with a mocked API key
    and a dummy client.
    """
    # Mock the ConfigManager to prevent it from needing a real API key
    monkeypatch.setattr(ConfigManager, "get_api_key", lambda self, service: "dummy_key")
    
    # Instantiate the provider. It will now get the "dummy_key" from the mocked config.
    provider = PolygonIOProvider()
    
    # Replace the real RESTClient with our dummy client
    provider.client = DummyClient()
    
    return provider

def test_polygon_provider_get_data_success(mock_provider):
    """
    Test the PolygonIOProvider's get_data method for a successful data fetch.
    Ensures that the returned price DataFrame and volume Series are correct.
    """
    # Use the fixture to get the pre-configured provider
    price_df, volume_series = mock_provider.get_data(
        "AAPL", 
        interval="1d", 
        start_date="2021-01-01", 
        end_date="2021-01-02"
    )

    # 1. Check return types
    assert isinstance(price_df, pd.DataFrame), "price_df should be a DataFrame"
    assert isinstance(volume_series, pd.Series), "volume_series should be a Series"

    # 2. Check DataFrame structure
    expected_columns = {"open", "high", "low", "close"}
    assert set(price_df.columns) == expected_columns, f"Expected columns: {expected_columns}, got: {set(price_df.columns)}"
    assert price_df.shape == (2, 4), f"Expected shape (2, 4), got {price_df.shape}"
    assert not price_df.empty, "price_df should not be empty"

    # 3. Check DataFrame and Series content
    # Use .iloc for integer-based indexing as the index is a DatetimeIndex
    assert price_df.iloc[0]['open'] == 100
    assert price_df.iloc[0]['high'] == 105
    assert price_df.iloc[1]['close'] == 104
    
    assert volume_series.iloc[0] == 10000
    assert volume_series.iloc[1] == 12000
    assert len(volume_series) == 2, "Volume series should have 2 entries"

    # 4. Check index properties
    expected_index = pd.to_datetime(['2021-01-01', '2021-01-02']).tz_localize(tz='UTC')
    assert isinstance(price_df.index, pd.DatetimeIndex), "price_df index should be a DatetimeIndex"
    assert isinstance(volume_series.index, pd.DatetimeIndex), "volume_series index should be a DatetimeIndex"
    pd.testing.assert_index_equal(price_df.index.tz_localize(tz="UTC").normalize(), expected_index)
    pd.testing.assert_index_equal(price_df.index.tz_localize('UTC'), volume_series.index, "Indices of price_df and volume_series should match")
    
def test_polygon_provider_no_data(monkeypatch):
    """
    Test the PolygonIOProvider's get_data method when the API returns no data.
    """
    # Mock the ConfigManager
    monkeypatch.setattr(ConfigManager, "get_api_key", lambda self, service: "dummy_key")
    provider = PolygonIOProvider()

    # Mock the client's get_aggs to return an empty list
    monkeypatch.setattr(provider.client, "get_aggs", lambda *args, **kwargs: [])
    
    result = provider.get_data(
        "NODATA", 
        interval="1d", 
        start_date="2021-01-01", 
        end_date="2021-01-02"
    )
    
    assert result is None, "Expected None when no data is returned"
