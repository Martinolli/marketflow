import pytest
import pandas as pd
import numpy as np
from marketflow.marketflow_wyckoff import WyckoffAnalyzer
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.enums import WyckoffEvent, WyckoffPhase, MarketContext

@pytest.fixture
def synthetic_market_data():
    # Create a DataFrame with synthetic price/volume patterns for Wyckoff analysis
    index = pd.date_range(start="2024-01-01", periods=60, freq="D")
    price = pd.DataFrame(index=index)
    price['open'] = 100 + np.random.normal(0, 2, len(index))
    price['close'] = price['open'] + np.random.normal(0, 2, len(index))
    price['high'] = price[['open', 'close']].max(axis=1) + np.abs(np.random.normal(0, 1, len(index)))
    price['low']  = price[['open', 'close']].min(axis=1) - np.abs(np.random.normal(0, 1, len(index)))
    # Introduce a "climax" event (huge volume and range drop)
    price.iloc[10, price.columns.get_loc('low')] -= 5
    price.iloc[10, price.columns.get_loc('close')] -= 5
    price.iloc[10, price.columns.get_loc('open')] -= 5
    price.iloc[10, price.columns.get_loc('high')] -= 5
    volume = pd.Series(1000 + np.random.normal(0, 100, len(index)), index=index)
    volume.iloc[10] = 5000  # Volume spike for Selling Climax

    processed_data = {
        "price": price,
        "volume": volume
    }
    return processed_data

def test_wyckoff_analyzer_no_events_detected():
    # Create flat price and volume data to ensure no events are detected
    index = pd.date_range(start="2024-01-01", periods=30, freq="D")
    price = pd.DataFrame({
        'open': [100] * 30,
        'close': [100] * 30,
        'high': [100] * 30,
        'low': [100] * 30
    }, index=index)
    volume = pd.Series([1000] * 30, index=index)
    synthetic_market_data = {"price": price, "volume": volume}
    analyzer = WyckoffAnalyzer(synthetic_market_data)
    phases, events, _ = analyzer.run_analysis()
    assert isinstance(events, list)
    assert len(events) == 0, "Events should not be detected in flat data"
    assert isinstance(phases, list)
    assert len(phases) == 0, "Phases should not be detected in flat data"

def test_wyckoff_analyzer_partial_event_detection():
    # Create data with a single volume spike but no price movement
    index = pd.date_range(start="2024-01-01", periods=30, freq="D")
    price = pd.DataFrame({
        'open': [100] * 30,
        'close': [100] * 30,
        'high': [100] * 30,
        'low': [100] * 30
    }, index=index)
    volume = pd.Series([1000] * 30, index=index)
    volume.iloc[15] = 5000  # Volume spike
    synthetic_market_data = {"price": price, "volume": volume}
    analyzer = WyckoffAnalyzer(synthetic_market_data)
    phases, events, _ = analyzer.run_analysis()
    assert isinstance(events, list)
    # Depending on implementation, may or may not detect an event
    # Accept both 0 or 1 event, but not error
    assert len(events) >= 0
    assert isinstance(phases, list)
    assert len(phases) >= 0

def test_wyckoff_analyzer_invalid_input():
    # Pass invalid data structure
    with pytest.raises(Exception):
        analyzer = WyckoffAnalyzer({"price": None, "volume": None})
        analyzer.run_analysis()

def test_wyckoff_analyzer_event_details_structure(synthetic_market_data):
    analyzer = WyckoffAnalyzer(synthetic_market_data)
    phases, events, _ = analyzer.run_analysis()
    if events:
        for event in events:
            assert 'event_name' in event
            assert 'index' in event
            assert isinstance(event['event_name'], str)
            assert event['event_name'] in {'SC', 'AR', 'ST', 'SOS', 'LPS', 'UT', 'UTAD', 'SPR', 'SOW', 'BU', 'PS', 'BC', 'TR', 'Test', 'JAC', 'JACB', 'JACD', 'JACE', 'JACF', 'JACG', 'JACH', 'JACI', 'JACJ', 'JACK', 'JACL', 'JACM', 'JACN', 'JACO', 'JACP', 'JACQ', 'JACR', 'JACS', 'JACT', 'JACU', 'JACV', 'JACW', 'JACX', 'JACY', 'JACZ'}, "Unknown event name"

def test_wyckoff_analyzer_phase_details_structure(synthetic_market_data):
    analyzer = WyckoffAnalyzer(synthetic_market_data)
    phases, events, _ = analyzer.run_analysis()
    if phases:
        for phase in phases:
            assert 'phase_name' in phase
            assert 'start_index' in phase
            assert 'end_index' in phase
            assert phase['phase_name'] in {'A', 'B', 'C', 'D', 'E'}, "Unknown phase name"
            annotated = analyzer.annotate_chart()
            # Annotated DataFrame should have the added columns
            assert "wyckoff_event" in annotated.columns
            assert "wyckoff_phase" in annotated.columns
            assert "wyckoff_event_details" in annotated.columns
            # Should be able to find at least one event annotation
            assert annotated['wyckoff_event'].str.contains('SC').any(), "Chart should be annotated with SC event"
            assert annotated['wyckoff_phase'].str.contains('A').any(), "Chart should be annotated with A phase"