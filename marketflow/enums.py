"""
MarketFlow Enums Module

This module defines shared enumerations used across the MarketFlow project.
Place all global, domain-specific Enums here for easy reuse and type safety.
"""

from enum import Enum

class SignalType(Enum):
    """Enumeration for signal types in MarketFlow."""
    BUY = "BUY"
    SELL = "SELL"
    NO_ACTION = "NO_ACTION"

class SignalStrength(Enum):
    """Enumeration for signal strength in MarketFlow."""
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    NEUTRAL = "NEUTRAL"

class WyckoffEvent(Enum):
    # --- Accumulation Events ---
    SC = "Selling Climax"
    AR = "Automatic Rally"
    ST = "Secondary Test"
    SPRING = "Spring"
    TEST = "Test"
    SOS = "Sign of Strength"
    LPS = "Last Point of Support"
    JAC = "Jump Across the Creek"
    
    # --- Distribution Events ---
    BC = "Buying Climax"
    AUTO_REACTION = "Automatic Reaction" # Renamed from AR for distribution clarity
    ST_DIST = "Secondary Test in Distribution"
    UTAD = "Upthrust After Distribution"
    SOW = "Sign of Weakness"
    LPSY = "Last Point of Supply"
    
    # --- Common Events ---
    UT = "Upthrust"

class WyckoffPhase(Enum):
    A = "Phase A - Stopping Action"
    B = "Phase B - Building a Cause"
    C = "Phase C - Testing"
    D = "Phase D - Markup/Markdown" # Changed to reflect both up and down moves
    E = "Phase E - Trend Continuation" # Changed to be more general
    UNKNOWN = "Unknown Phase"

class MarketContext(Enum):
    ACCUMULATION = "Accumulation"
    DISTRIBUTION = "Distribution"
    UNDEFINED = "Undefined"

class MarketCondition(Enum):
    """Market condition classifications"""
    BULL_MARKET = "bull_market"
    BEAR_MARKET = "bear_market"
    SIDEWAYS = "sideways"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"
    TRENDING = "trending"
    RANGING = "ranging"

class AnalysisType(Enum):
    """Types of analysis performed"""
    TECHNICAL = "technical"
    FUNDAMENTAL = "fundamental"
    SENTIMENT = "sentiment"
    WYCKOFF = "wyckoff"
    VOLUME_PRICE = "volume_price"
    PATTERN_RECOGNITION = "pattern_recognition"

class QueryIntent(Enum):
    """Enumeration of supported query intents"""
    TICKER_ANALYSIS = "ticker_analysis"
    CONCEPT_EXPLANATION = "concept_explanation"
    RAG_QUERY = "rag_query"
    COMPARISON = "comparison"
    HISTORICAL_ANALYSIS = "historical_analysis"
    MULTI_TIMEFRAME = "multi_timeframe"
    UNKNOWN = "unknown"


class QueryConfidence(Enum):
    """Confidence levels for intent classification"""
    HIGH = "high"      # > 0.8
    MEDIUM = "medium"  # 0.5 - 0.8
    LOW = "low"        # < 0.5
    
## --- CHANGE END --- ##