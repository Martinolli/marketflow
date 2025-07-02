"""# test_data_provider.py
Unit tests for the PolygonIOProvider class in the Marketflow data provider module.
This module tests the functionality of the PolygonIOProvider class, ensuring it correctly retrieves and processes market data.
"""
# Import necessary modules and classes for testing
import pytest
import pandas as pd
from marketflow.marketflow_data_provider import PolygonIOProvider
from marketflow.marketflow_logger import get_logger

# Dummy client to simulate Polygon API responses for testing
# This client will return predefined data instead of making actual API calls.
# It is used to isolate the tests from external dependencies and ensure consistent results.
class DummyClient:
    def get_aggs(self, ticker, multiplier, timespan, from_, to, limit):

        self.logger = get_logger(module_name="DummyClient", log_level="DEBUG")
        self.logger.debug(f"Fetching data for {ticker} from {from_} to {to}")
        from types import SimpleNamespace
        return [
            SimpleNamespace(timestamp=1609459200000, open=100, high=105, low=95, close=102, volume=10000),
            SimpleNamespace(timestamp=1609545600000, open=102, high=106, low=98, close=104, volume=12000),
        ]

# Test case for the PolygonIOProvider class
# This test verifies that the provider can successfully retrieve and process market data.
def test_polygon_provider(monkeypatch):
    """
    Test the PolygonIOProvider's get_data method using a DummyClient.
    Ensures that the returned price DataFrame and volume Series are correct and robust.
    """
    logger = get_logger(module_name="Test_Polygon_Provider", log_level="DEBUG")
    logger.debug("Starting test for PolygonIOProvider")
    provider = PolygonIOProvider(api_key="dummy")
    logger.debug("PolygonIOProvider instance created")
    
    provider.client = DummyClient()
    logger.debug("DummyClient assigned to provider")
    price_df, volume_series = provider.get_data("AAPL", "1d", "2021-01-01", "2021-01-02")

    # Check types
    logger.info("Checking types of returned objects")
    assert isinstance(price_df, pd.DataFrame), "price_df should be a DataFrame"
    logger.debug("price_df is a DataFrame")
    assert isinstance(volume_series, pd.Series), "volume_series should be a Series"
    logger.debug("volume_series is a Series")

    # Check DataFrame columns
    expected_columns = {"open", "high", "low", "close"}
    logger.info("Checking DataFrame columns")
    assert isinstance(price_df, pd.DataFrame), "price_df should be a DataFrame"
    logger.debug("price_df is a DataFrame")
    assert set(price_df.columns) == expected_columns, f"Expected columns: {expected_columns}, got: {set(price_df.columns)}"
    logger.debug("DataFrame columns match expected columns")
    assert expected_columns.issubset(price_df.columns), f"Missing columns: {expected_columns - set(price_df.columns)}"

    # Check DataFrame shape
    logger.info("Checking DataFrame shape")
    assert price_df.shape[1] == 4, f"Expected 4 columns, got {price_df.shape[1]}"
    logger.debug("DataFrame has correct number of columns")
    assert price_df.shape[0] > 0, "price_df should not be empty"
    logger.debug("DataFrame is not empty")
    assert len(price_df) == 2, f"Expected 2 rows, got {len(price_df)}"
    assert all(col in price_df.columns for col in expected_columns), "Not all OHLC columns present"

    # Check DataFrame values
    logger.info("Checking DataFrame values")
    assert price_df.loc[0, "open"] == 100
    logger.debug("First row open price is correct")
    assert price_df.loc[0, "high"] == 105
    logger.debug("First row high price is correct")
    assert price_df.loc[1, "close"] == 104

    # Check volume Series
    logger.info("Checking volume Series")
    assert isinstance(volume_series, pd.Series), "volume_series should be a Series"
    logger.debug("volume_series is a Series")
    assert len(volume_series) == 2, "Volume series should have 2 entries"
    assert volume_series.iloc[0] == 10000
    assert volume_series.iloc[1] == 12000

    # Check index alignment
    logger.info("Checking index alignment between price_df and volume_series")
    assert isinstance(price_df.index, pd.DatetimeIndex), "price_df index should be a DatetimeIndex"
    logger.debug("price_df index is a DatetimeIndex")
    assert isinstance(volume_series.index, pd.DatetimeIndex), "volume_series index should be a DatetimeIndex"
    logger.debug("volume_series index is a DatetimeIndex")
    assert all(price_df.index == volume_series.index), "Indices of price_df and volume_series should match"
