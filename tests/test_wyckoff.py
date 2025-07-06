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

def test_wyckoff_analyzer_run_analysis(synthetic_market_data):
    analyzer = WyckoffAnalyzer(synthetic_market_data)
    phases, events, trading_ranges = analyzer.run_analysis()
    # There should be at least one event and phase detected
    assert isinstance(events, list)
    assert len(events) > 0, "No Wyckoff events detected"
    assert isinstance(phases, list)
    assert len(phases) > 0, "No Wyckoff phases detected"
    # Check for at least a Selling Climax event type
    assert any(e['event_name'] == 'SC' for e in events), "Selling Climax event should be detected"
    # Phases should include at least one known Wyckoff phase
    assert any(p['phase_name'] in {'A', 'B', 'C', 'D', 'E'} for p in phases), "At least one Wyckoff phase should be detected"

def test_wyckoff_analyzer_annotation(synthetic_market_data):
    analyzer = WyckoffAnalyzer(synthetic_market_data)
    analyzer.run_analysis()
    annotated = analyzer.annotate_chart()
    # Annotated DataFrame should have the added columns
    assert "wyckoff_event" in annotated.columns
    assert "wyckoff_phase" in annotated.columns
    assert "wyckoff_event_details" in annotated.columns
    # Should be able to find at least one event annotation
    assert annotated['wyckoff_event'].str.contains('SC').any(), "Chart should be annotated with SC event"