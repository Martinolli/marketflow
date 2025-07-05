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