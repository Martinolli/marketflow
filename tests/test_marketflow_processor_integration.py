import pytest
import pandas as pd
import numpy as np

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_processor import DataProcessor

@pytest.fixture
def dummy_data():
    # Create a dummy OHLCV dataset
    index = pd.date_range(start="2021-01-01", periods=30, freq="D")
    price_data = pd.DataFrame({
        "open": np.linspace(100, 130, 30),
        "high": np.linspace(102, 134, 30),
        "low": np.linspace(98, 128, 30),
        "close": np.linspace(101, 132, 30),
    }, index=index)
    # Add some volume volatility
    volume_data = pd.Series(np.random.randint(9000, 20000, 30), index=index)
    return price_data, volume_data

def test_processor_integration_with_parameters(dummy_data):
    price_data, volume_data = dummy_data

    # Create parameter object and override a threshold
    params = MarketFlowDataParameters()
    params.update_parameters({"volume.very_high_threshold": 1.5})

    # Create processor with parameters
    processor = DataProcessor(parameters=params)
    assert processor.parameters is params

    # Run preprocess
    processed = processor.preprocess_data(price_data, volume_data)

    # --- Output checks ---
    # Main keys
    assert "price" in processed
    assert "volume" in processed
    assert "spread" in processed
    assert "volume_ratio" in processed
    assert "volume_class" in processed
    assert "candle_class" in processed
    assert "price_direction" in processed
    assert "volume_direction" in processed

    # Output types
    assert isinstance(processed["price"], pd.DataFrame)
    assert isinstance(processed["volume"], pd.Series)
    assert isinstance(processed["volume_ratio"], pd.Series)
    assert isinstance(processed["volume_class"], pd.Series)
    assert isinstance(processed["candle_class"], pd.Series)

    # Sanity: all indexes line up
    assert all(processed["price"].index == processed["volume_class"].index)

    # Check that the overridden threshold is respected
    # Example: no value in volume_class should be "VERY_HIGH" if volume_ratio < 1.5
    high_ratio = processed["volume_ratio"] >= 1.5
    if not high_ratio.any():
        assert not (processed["volume_class"] == "VERY_HIGH").any()

def test_processor_threshold_effect(dummy_data):
    price_data, volume_data = dummy_data

    # Set a low threshold to force some "VERY_HIGH" classifications
    params = MarketFlowDataParameters()
    params.update_parameters({"volume.very_high_threshold": 0.5})

    processor = DataProcessor(parameters=params)
    processed = processor.preprocess_data(price_data, volume_data)

    # Now we expect at least some "VERY_HIGH" in the result
    assert (processed["volume_class"] == "VERY_HIGH").any()