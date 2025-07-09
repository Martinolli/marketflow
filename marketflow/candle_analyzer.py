""""
Candle Analyzer Module

This module provides analysis and pattern recognition for the Marketflow algorithm.
Handles individual candle analysis, including identifying bullish and bearish patterns.

"""

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config


class CandleAnalyzer:
    """Analyze individual candles"""
    def __init__(self, parameters=None):

        # Initialize Logger
        self.logger = get_logger(module_name="CandleAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        # Check if parameters are provided, otherwise use default
        self.parameters = parameters or MarketFlowDataParameters()
        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()

    def analyze_candle(self, idx: int, processed_data: dict) -> dict:
        """
        Analyze a single candle and its volume for Marketflow signals

        Parameters:
        - idx: Index of the candle to analyze
        - processed_data: Dictionary with processed data

        Returns:
        - Dictionary with analysis results
        """
        self.logger.info(f"Analyzing candle at index: {idx}")
        self.logger.debug(f"Processed data keys: {list(processed_data.keys())}")

        # Extract data for the current candle
        candle_class = processed_data["candle_class"].loc[idx]
        volume_class = processed_data["volume_class"].loc[idx]
        price_direction = processed_data["price_direction"].loc[idx]

        self.logger.debug(f"Candle class: {candle_class}, Volume class: {volume_class}, Price direction: {price_direction}")

        # Determine if price is up or down
        price_data = processed_data["price"]
        is_up_candle = price_data.loc[idx]["close"] > price_data.loc[idx]["open"]

        self.logger.debug(f"Is up candle: {is_up_candle}")

        # Check for validation or anomaly
        result = {
            "candle_class": candle_class,
            "volume_class": volume_class,
            "is_up_candle": is_up_candle,
            "price_direction": price_direction,
            "signal_type": None,
            "signal_strength": None,
            "details": ""
        }

        # Apply Marketflow rules for validations and anomalies
        if is_up_candle:
            if "WIDE" in candle_class and volume_class in ["HIGH", "VERY_HIGH"]:
                # Wide up candle with high volume = validation (bullish)
                result["signal_type"] = "VALIDATION"
                result["signal_strength"] = "BULLISH"
                result["details"] = "Wide spread up candle with high volume confirms bullish sentiment"

            elif "WIDE" in candle_class and volume_class in ["LOW", "VERY_LOW"]:
                # Wide up candle with low volume = anomaly (potential trap)
                result["signal_type"] = "ANOMALY"
                result["signal_strength"] = "BEARISH"
                result["details"] = "Wide spread up candle with low volume suggests potential trap up move"

            elif "NARROW" in candle_class and volume_class in ["HIGH", "VERY_HIGH"]:
                # Narrow up candle with high volume = anomaly (resistance)
                result["signal_type"] = "ANOMALY"
                result["signal_strength"] = "BEARISH"
                result["details"] = "Narrow spread up candle with high volume shows resistance to higher prices"

            elif "NARROW" in candle_class and volume_class in ["LOW", "VERY_LOW"]:
                # Narrow up candle with low volume = validation (consolidation)
                result["signal_type"] = "VALIDATION"
                result["signal_strength"] = "NEUTRAL"
                result["details"] = "Narrow spread up candle with low volume indicates consolidation"

            # Add more signal detection for NEUTRAL candles
            elif "NEUTRAL" in candle_class and volume_class in ["HIGH", "VERY_HIGH"]:
                result["signal_type"] = "VALIDATION"
                result["signal_strength"] = "BULLISH"
                result["details"] = "Normal up candle with high volume shows buying interest"
        else:
            # Down candle analysis
            if "WIDE" in candle_class and volume_class in ["HIGH", "VERY_HIGH"]:
                # Wide down candle with high volume = validation (bearish)
                result["signal_type"] = "VALIDATION"
                result["signal_strength"] = "BEARISH"
                result["details"] = "Wide spread down candle with high volume confirms bearish sentiment"

            elif "WIDE" in candle_class and volume_class in ["LOW", "VERY_LOW"]:
                # Wide down candle with low volume = anomaly (potential trap)
                result["signal_type"] = "ANOMALY"
                result["signal_strength"] = "BULLISH"
                result["details"] = "Wide spread down candle with low volume suggests potential trap down move"

            elif "NARROW" in candle_class and volume_class in ["HIGH", "VERY_HIGH"]:
                # Narrow down candle with high volume = anomaly (support)
                result["signal_type"] = "ANOMALY"
                result["signal_strength"] = "BULLISH"
                result["details"] = "Narrow spread down candle with high volume shows support at current price level"

            elif "NARROW" in candle_class and volume_class in ["LOW", "VERY_LOW"]:
                # Narrow down candle with low volume = validation (consolidation)
                result["signal_type"] = "VALIDATION"
                result["signal_strength"] = "NEUTRAL"
                result["details"] = "Narrow spread down candle with low volume indicates consolidation"

            # Add more signal detection for NEUTRAL candles
            elif "NEUTRAL" in candle_class and volume_class in ["HIGH", "VERY_HIGH"]:
                result["signal_type"] = "VALIDATION"
                result["signal_strength"] = "BEARISH"
                result["details"] = "Normal down candle with high volume shows selling pressure"

        # Check for significant wicks
        if "_UPPER_WICK" in candle_class:
            if is_up_candle and volume_class in ["HIGH", "VERY_HIGH"]:
                # Up candle with upper wick and high volume = selling pressure at highs
                result["details"] += "; Upper wick with high volume shows selling pressure at highs"
                if result["signal_strength"] == "BULLISH":
                    result["signal_strength"] = "NEUTRAL"

            elif not is_up_candle and volume_class in ["HIGH", "VERY_HIGH"]:
                # Down candle with upper wick and high volume = failed upward breakout
                result["details"] += "; Upper wick with high volume shows failed upward breakout"
                result["signal_strength"] = "BEARISH"

        if "_LOWER_WICK" in candle_class:
            if not is_up_candle and volume_class in ["HIGH", "VERY_HIGH"]:
                # Down candle with lower wick and high volume = buying pressure at lows
                result["details"] += "; Lower wick with high volume shows buying pressure at lows"
                if result["signal_strength"] == "BEARISH":
                    result["signal_strength"] = "NEUTRAL"

            elif is_up_candle and volume_class in ["HIGH", "VERY_HIGH"]:
                # Up candle with lower wick and high volume = failed downward breakout
                result["details"] += "; Lower wick with high volume shows failed downward breakout"
                result["signal_strength"] = "BULLISH"

        self.logger.info(f"Candle analysis result: {result}")
        self.logger.debug(f"Analysis details: {result['details']}")
        return result