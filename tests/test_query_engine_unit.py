from __future__ import annotations

from marketflow.enums import QueryIntent
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine


def _engine_without_runtime_dependencies() -> MarketflowLLMQueryEngine:
    engine = MarketflowLLMQueryEngine.__new__(MarketflowLLMQueryEngine)
    engine._initialize_intent_patterns()
    engine._initialize_ticker_patterns()
    return engine


def test_query_engine_validates_input_without_runtime_services():
    engine = _engine_without_runtime_dependencies()

    assert engine.validate_input("Analyze AAPL") == (True, None)
    assert engine.validate_input("   ")[0] is False
    assert engine.validate_input("<script>alert('x')</script>")[0] is False


def test_query_engine_extracts_tickers_without_provider_calls():
    engine = _engine_without_runtime_dependencies()

    assert engine.extract_tickers("Analyze AAPL and MSFT") == ["AAPL", "MSFT"]
    assert engine.extract_tickers("What about DAILY analysis") == []


def test_query_engine_parses_basic_intents_without_provider_calls():
    engine = _engine_without_runtime_dependencies()

    ticker_intent = engine._parse_intent("Analyze AAPL")
    concept_intent = engine._parse_intent("What is a Wyckoff Spring?")
    comparison_intent = engine._parse_intent("Compare AAPL and MSFT")

    assert ticker_intent.intent == QueryIntent.TICKER_ANALYSIS
    assert ticker_intent.parameters["primary_ticker"] == "AAPL"
    assert concept_intent.intent == QueryIntent.CONCEPT_EXPLANATION
    assert comparison_intent.intent == QueryIntent.COMPARISON
    assert comparison_intent.parameters["tickers"] == ["AAPL", "MSFT"]
