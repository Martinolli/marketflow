import pandas as pd

from marketflow.enums import MarketContext
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_wyckoff import WyckoffAnalyzer


def _wyckoff_params():
    params = MarketFlowDataParameters()
    params.set_wyckoff_parameter("vol_lookback", 5)
    params.set_wyckoff_parameter("range_lookback", 5)
    params.set_wyckoff_parameter("climax_vol_multiplier", 1.5)
    params.set_wyckoff_parameter("climax_range_multiplier", 1.2)
    params.set_wyckoff_parameter("breakout_vol_multiplier", 1.5)
    params.set_wyckoff_parameter("swing_point_n", 1)
    return params


def _market_data(rows):
    index = pd.date_range("2024-01-01", periods=len(rows), freq="D", tz="UTC")
    price_df = pd.DataFrame(
        [
            {
                "open": row[0],
                "high": row[1],
                "low": row[2],
                "close": row[3],
            }
            for row in rows
        ],
        index=index,
    )
    volume = pd.Series([row[4] for row in rows], index=index)
    return {"price": price_df, "volume": volume}


def make_accumulation_data():
    rows = [(100.0, 101.0, 99.0, 100.0, 1_000_000.0) for _ in range(40)]

    for i in range(5, 10):
        base = 100.0 - (i - 4)
        rows[i] = (base + 0.5, base + 1.0, base - 1.0, base, 1_000_000.0)

    rows[10] = (93.0, 94.0, 78.0, 79.0, 8_000_000.0)  # SC
    rows[11] = (82.0, 86.0, 80.0, 85.0, 1_200_000.0)
    rows[12] = (85.0, 90.0, 84.0, 89.0, 1_100_000.0)
    rows[13] = (90.0, 96.0, 89.0, 95.0, 1_300_000.0)  # AR swing high
    rows[14] = (91.0, 92.0, 86.0, 87.0, 1_100_000.0)
    rows[15] = (86.0, 88.0, 84.0, 85.0, 1_200_000.0)
    rows[16] = (84.0, 86.0, 81.0, 83.0, 900_000.0)
    rows[17] = (84.0, 87.0, 83.0, 86.0, 1_000_000.0)
    rows[18] = (86.0, 89.0, 84.0, 88.0, 1_000_000.0)
    rows[19] = (87.0, 90.0, 85.0, 87.0, 1_000_000.0)
    rows[20] = (84.0, 86.0, 77.0, 82.0, 1_200_000.0)  # Spring
    rows[21] = (83.0, 89.0, 82.0, 88.0, 1_000_000.0)
    rows[22] = (88.0, 92.0, 87.0, 91.0, 1_100_000.0)
    rows[23] = (91.0, 94.0, 90.0, 93.0, 1_100_000.0)
    rows[24] = (94.0, 100.0, 93.0, 98.0, 6_000_000.0)  # SOS/JAC

    for i in range(25, 40):
        base = 98.0 + (i - 24) * 0.5
        rows[i] = (base, base + 1.0, base - 0.8, base + 0.4, 1_000_000.0)

    return _market_data(rows)


def make_distribution_data():
    rows = [(200.0, 201.0, 199.0, 200.0, 1_000_000.0) for _ in range(40)]

    for i in range(5, 10):
        base = 200.0 + (i - 4)
        rows[i] = (base - 0.5, base + 1.0, base - 1.0, base, 1_000_000.0)

    rows[10] = (207.0, 222.0, 206.0, 221.0, 8_000_000.0)  # BC
    rows[11] = (218.0, 220.0, 214.0, 215.0, 1_100_000.0)
    rows[12] = (215.0, 216.0, 208.0, 209.0, 1_200_000.0)
    rows[13] = (210.0, 213.0, 204.0, 205.0, 1_300_000.0)  # Automatic reaction swing low
    rows[14] = (207.0, 214.0, 206.0, 212.0, 1_100_000.0)
    rows[15] = (212.0, 216.0, 210.0, 214.0, 1_100_000.0)
    rows[16] = (214.0, 218.0, 212.0, 216.0, 1_000_000.0)
    rows[17] = (216.0, 220.0, 214.0, 218.0, 1_000_000.0)
    rows[18] = (218.0, 221.0, 216.0, 219.0, 1_000_000.0)
    rows[19] = (219.0, 220.0, 215.0, 216.0, 1_000_000.0)
    rows[20] = (218.0, 224.0, 216.0, 220.0, 1_200_000.0)  # UTAD
    rows[21] = (218.0, 220.0, 212.0, 214.0, 1_000_000.0)
    rows[22] = (214.0, 216.0, 208.0, 210.0, 1_100_000.0)
    rows[23] = (210.0, 212.0, 205.0, 206.0, 1_100_000.0)
    rows[24] = (205.0, 206.0, 198.0, 199.0, 6_000_000.0)  # SOW

    for i in range(25, 40):
        base = 199.0 - (i - 24) * 0.5
        rows[i] = (base, base + 0.8, base - 1.0, base - 0.4, 1_000_000.0)

    return _market_data(rows)


def test_accumulation_phases():
    analyzer = WyckoffAnalyzer(make_accumulation_data(), parameters=_wyckoff_params())

    phases, events, trading_ranges = analyzer.run_analysis()

    phase_names = {phase["phase_name"] for phase in phases}
    event_names = {event["event_name"] for event in events}
    assert {"A", "D"}.issubset(phase_names)
    assert {"SC", "AR", "SPRING", "SOS", "JAC"}.issubset(event_names)
    assert trading_ranges
    assert trading_ranges[0]["context"] == MarketContext.ACCUMULATION.value


def test_distribution_phases():
    analyzer = WyckoffAnalyzer(make_distribution_data(), parameters=_wyckoff_params())

    phases, events, trading_ranges = analyzer.run_analysis()

    phase_names = {phase["phase_name"] for phase in phases}
    event_names = {event["event_name"] for event in events}
    assert {"A", "D"}.issubset(phase_names)
    assert {"BC", "AUTO_REACTION", "UTAD", "SOW"}.issubset(event_names)
    assert trading_ranges
    assert trading_ranges[0]["context"] == MarketContext.DISTRIBUTION.value
