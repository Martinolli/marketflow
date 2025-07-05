import pytest
from marketflow.marketflow_signals import SignalGenerator, RiskAssessor
from marketflow.enums import SignalType, SignalStrength

@pytest.fixture
def dummy_params():
    # Use the actual class so config is loaded as in production
    return SignalGenerator().data_parameters

@pytest.fixture
def signal_generator(dummy_params):
    return SignalGenerator(data_parameters=dummy_params)

@pytest.fixture
def risk_assessor(dummy_params):
    return RiskAssessor(data_parameters=dummy_params)

@pytest.fixture
def bullish_timeframe_analyses():
    # Example that should trigger a strong buy
    return {
        "1d": {
            "pattern_analysis": {
                "accumulation": {"detected": True, "details": "Strong base."},
                "selling_climax": {"detected": True, "details": "Capitulation."},
                "testing": {"detected": True, "tests": [{"type": "SUPPORT_TEST"}]},
                "distribution": {"detected": False, "details": ""},
                "buying_climax": {"detected": False, "details": ""}
            },
            "candle_analysis": {"signal_strength": "BULLISH", "details": "Engulfing candle."},
            "trend_analysis": {"signal_strength": "BULLISH", "details": "Upwards trend."}
        }
    }

@pytest.fixture
def bearish_timeframe_analyses():
    return {
        "1d": {
            "pattern_analysis": {
                "accumulation": {"detected": False, "details": ""},
                "selling_climax": {"detected": False, "details": ""},
                "testing": {"detected": True, "tests": [{"type": "RESISTANCE_TEST"}]},
                "distribution": {"detected": True, "details": "Distribution top."},
                "buying_climax": {"detected": True, "details": "Euphoria."}
            },
            "candle_analysis": {"signal_strength": "BEARISH", "details": "Bearish pin bar."},
            "trend_analysis": {"signal_strength": "BEARISH", "details": "Down trend."}
        }
    }

@pytest.fixture
def bullish_confirmations():
    return {"bullish": ["1d"], "bearish": []}

@pytest.fixture
def bearish_confirmations():
    return {"bullish": [], "bearish": ["1d"]}

def test_strong_buy_signal(signal_generator, bullish_timeframe_analyses, bullish_confirmations):
    assert signal_generator.is_strong_buy_signal(bullish_timeframe_analyses, bullish_confirmations) is True

def test_strong_sell_signal(signal_generator, bearish_timeframe_analyses, bearish_confirmations):
    assert signal_generator.is_strong_sell_signal(bearish_timeframe_analyses, bearish_confirmations) is True

def test_generate_signals_buy(signal_generator, bullish_timeframe_analyses, bullish_confirmations):
    result = signal_generator.generate_signals(bullish_timeframe_analyses, bullish_confirmations)
    assert result["type"] == SignalType.BUY
    assert result["strength"] == SignalStrength.STRONG
    assert "evidence" in result

def test_generate_signals_sell(signal_generator, bearish_timeframe_analyses, bearish_confirmations):
    result = signal_generator.generate_signals(bearish_timeframe_analyses, bearish_confirmations)
    assert result["type"] == SignalType.SELL
    assert result["strength"] == SignalStrength.STRONG
    assert "evidence" in result

def test_generate_signals_no_action(signal_generator):
    # Missing or empty analyses should yield NO_ACTION
    result = signal_generator.generate_signals({}, {})
    assert result["type"] == "NO_ACTION" or result["type"] == SignalType.NO_ACTION

def test_risk_assessor_buy(risk_assessor):
    signal = {"type": SignalType.BUY}
    # Provide dummy support/resistance (should pick closest support below price)
    res = risk_assessor.assess_trade_risk(signal, current_price=100, support_resistance={
        "support": [{"price": 95}],
        "resistance": [{"price": 110}]
    })
    assert res["stop_loss"] < 100
    assert res["take_profit"] > 100
    assert res["risk_reward_ratio"] > 0

def test_risk_assessor_sell(risk_assessor):
    signal = {"type": SignalType.SELL}
    res = risk_assessor.assess_trade_risk(signal, current_price=100, support_resistance={
        "support": [{"price": 95}],
        "resistance": [{"price": 110}]
    })
    assert res["stop_loss"] > 100
    assert res["take_profit"] < 100
    assert res["risk_reward_ratio"] > 0

def test_risk_assessor_no_action(risk_assessor):
    signal = {"type": SignalType.NO_ACTION}
    res = risk_assessor.assess_trade_risk(signal, current_price=100, support_resistance={
        "support": [{"price": 95}],
        "resistance": [{"price": 110}]
    })
    # By default, should use basic percentages for stop_loss/take_profit
    assert res["stop_loss"] < 100
    assert res["take_profit"] > 100