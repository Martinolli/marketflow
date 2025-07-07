import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from marketflow.marketflow_wyckoff import WyckoffAnalyzer
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.enums import WyckoffPhase, WyckoffEvent

def make_accumulation_data():
    """
    Generate price/volume data that mimics a textbook Accumulation structure:
    - Selling Climax (SC)
    - Automatic Rally (AR)
    - Secondary Test (ST)
    - Spring
    - Sign of Strength (SOS)
    """
    n = 100
    idx = pd.date_range(end=datetime.now(), periods=n, freq="D", tz="UTC")
    price = 100 + np.cumsum(np.concatenate([
        np.full(15, -2),     # Pre-SC down (15)
        [-12],               # SC drop (1)
        [10],                # AR up (1)
        np.full(12, -1),     # Range chop (12)
        [-6],                # ST (1)
        np.full(18, 0.5),    # Range chop (18)
        [-7],                # Spring (shakeout) (1)
        [8],                 # SOS (breakout) (1)
        np.full(50, 1)       # Markup (51) - adjusted to make total 100
    ]))
    high = price + np.random.uniform(0.5, 2, n)
    low = price - np.random.uniform(0.5, 2, n)
    open_ = price + np.random.uniform(-1, 1, n)
    close = price + np.random.uniform(-1, 1, n)
    volume = np.full(n, 1e6)
    # SC, ST, Spring, SOS get volume spikes
    volume[10] = 3e6   # SC
    volume[12] = 1.7e6 # AR
    volume[21] = 2.5e6 # ST
    volume[32] = 2.2e6 # Spring
    volume[33] = 2.5e6 # SOS breakout

    price_df = pd.DataFrame({
        "open": open_, "high": high, "low": low, "close": close
    }, index=idx)
    volume_series = pd.Series(volume, index=idx)
    # Add these print statements
    print("Price DataFrame shape:", price_df.shape)
    print("Volume Series shape:", volume_series.shape)
    print("First few rows of price data:")
    print(price_df.head())
    print("First few volume values:")
    print(volume_series.head())
    
    return {"price": price_df, "volume": volume_series}

def make_distribution_data():
    """
    Generate price/volume data that mimics a textbook Distribution structure:
    - Buying Climax (BC)
    - Automatic Reaction (AUTO_REACTION)
    - Upthrust After Distribution (UTAD)
    - Sign of Weakness (SOW)
    """
    n = 100
    idx = pd.date_range(end=datetime.now(), periods=n, freq="D", tz="UTC")
    price = 200 + np.cumsum(np.concatenate([
        np.full(15, 2),      # Pre-BC up (15)
        [12],                # BC up (1)
        [-9],                # AUTO_REACTION (1)
        np.full(12, 1),      # Range chop (12)
        [5],                 # UTAD (upthrust) (1)
        np.full(18, -0.5),   # Range chop (18)
        [-7],                # SOW (breakdown) (1)
        np.full(51, -1)      # Markdown (51) - adjusted to make total 100
    ]))
    high = price + np.random.uniform(0.5, 2, n)
    low = price - np.random.uniform(0.5, 2, n)
    open_ = price + np.random.uniform(-1, 1, n)
    close = price + np.random.uniform(-1, 1, n)
    volume = np.full(n, 1e6)
    # BC, AR, UTAD, SOW get volume spikes
    volume[10] = 3e6   # BC
    volume[12] = 1.7e6 # AUTO_REACTION
    volume[21] = 2.5e6 # UTAD
    volume[32] = 2.2e6 # SOW

    price_df = pd.DataFrame({
        "open": open_, "high": high, "low": low, "close": close
    }, index=idx)
    volume_series = pd.Series(volume, index=idx)
    return {"price": price_df, "volume": volume_series}

def test_accumulation_phases():
    data = make_accumulation_data()
    params = MarketFlowDataParameters()
    params.set_wyckoff_parameter('climax_vol_multiplier', 1.5)
    params.set_wyckoff_parameter('climax_range_multiplier', 1.2)
    params.set_wyckoff_parameter('swing_point_n', 2)
    analyzer = WyckoffAnalyzer(data, parameters=params)
    phases, events, _ = analyzer.run_analysis()
    # Add these print statements
    print("Detected phases:", phases)
    print("Detected events:", events)
    # Expect phases to progress from UNKNOWN -> A -> B -> C -> D or E
    phase_names = [p['phase_name'] for p in phases]
    assert "A" in phase_names, "Phase A (Accumulation) should be detected"
    assert "C" in phase_names, "Phase C (Spring/Test) should be detected"
    assert "D" in phase_names or "E" in phase_names, "Phase D/E (Markup) should be detected"
    event_names = [e['event_name'] for e in events]
    assert "SC" in event_names, "Selling Climax should be detected"
    assert "SPRING" in event_names, "Spring should be detected"
    assert "SOS" in event_names, "SOS should be detected"

def test_distribution_phases():
    data = make_distribution_data()
    params = MarketFlowDataParameters()
    params.set_wyckoff_parameter('climax_vol_multiplier', 1.5)
    params.set_wyckoff_parameter('climax_range_multiplier', 1.2)
    params.set_wyckoff_parameter('swing_point_n', 2)
    analyzer = WyckoffAnalyzer(data, parameters=params)
    phases, events, _ = analyzer.run_analysis()
    phase_names = [p['phase_name'] for p in phases]
    assert "A" in phase_names, "Phase A (Distribution) should be detected"
    assert "C" in phase_names, "Phase C (UTAD/Test) should be detected"
    assert "D" in phase_names or "E" in phase_names, "Phase D/E (Markdown) should be detected"
    event_names = [e['event_name'] for e in events]
    assert "BC" in event_names, "Buying Climax should be detected"
    assert "UTAD" in event_names, "UTAD should be detected"
    assert "SOW" in event_names, "Sign of Weakness should be detected"

if __name__ == "__main__":
    test_accumulation_phases()
    # test_distribution_phases()
    print("WyckoffAnalyzer phase tests passed.")