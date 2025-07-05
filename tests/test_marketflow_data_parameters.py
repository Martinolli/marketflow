import os
import tempfile
import json
import pytest

from marketflow.marketflow_data_parameters import MarketFlowDataParameters

@pytest.fixture
def params():
    # Fresh instance for each test
    return MarketFlowDataParameters()

def test_default_initialization(params):
    # Test default config structure
    config = params.get_all()
    assert isinstance(config, dict)
    assert "volume" in config
    assert "candle" in config
    assert "wyckoff_config" in config

def test_update_parameters_valid(params):
    # Flat key
    params.update_parameters({"volume.very_high_threshold": 3.0})
    assert params.get_volume_thresholds()["very_high_threshold"] == 3.0
    # Nested key
    params.update_parameters({"pattern.accumulation.high_volume_threshold": 2.0})
    assert params.get_pattern_parameters()["accumulation"]["high_volume_threshold"] == 2.0

def test_update_parameters_invalid(params, caplog):
    # Negative threshold (invalid)
    params.update_parameters({"volume.very_high_threshold": -1.0})
    # Should not update
    assert params.get_volume_thresholds()["very_high_threshold"] != -1.0
    # Check for warning in logs
    assert any("Invalid value" in message for message in caplog.text.splitlines())

def test_save_and_load_parameters(params):
    # Set a custom value
    params.update_parameters({"volume.high_threshold": 1.5})
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    params.save_parameters(config_file=tmp_path)

    # Create a new instance and load from the file
    params2 = MarketFlowDataParameters()
    params2.load_parameters(config_file=tmp_path)
    assert params2.get_volume_thresholds()["high_threshold"] == 1.5

    # Cleanup
    os.remove(tmp_path)

def test_wyckoff_config_get_set(params):
    # Set and get wyckoff parameter
    params.set_wyckoff_parameter("swing_point_n", 10)
    assert params.get_wyckoff_parameter("swing_point_n") == 10

def test_getters(params):
    # Test all getter methods return expected types
    assert isinstance(params.get_volume_thresholds(), dict)
    assert isinstance(params.get_candle_thresholds(), dict)
    assert isinstance(params.get_trend_parameters(), dict)
    assert isinstance(params.get_pattern_parameters(), dict)
    assert isinstance(params.get_signal_parameters(), dict)
    assert isinstance(params.get_risk_parameters(), dict)
    assert isinstance(params.get_timeframes(), list)
    assert isinstance(params.get_account_parameters(), dict)
    assert isinstance(params.get_primary_timeframe(), str)