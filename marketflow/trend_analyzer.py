"""
Trend Analyzer Module

Analyzes price trends for MarketFlow.
"""
import pandas as pd

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

class TrendAnalyzer:
    """Analyze price trends"""
    
    def __init__(self, parameters=None):

        # Initialize Logger
        self.logger = get_logger(module_name="TrendAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()

        self.trend_params = self.parameters.get_trend_parameters()
    
    def analyze_trend(self, processed_data: dict, current_idx, lookback=None) -> dict:
        """
        Analyze recent candles to identify trend characteristics
        
        Parameters:
        - processed_data: Dictionary with processed data
        - current_idx: Index of the current candle
        - lookback: Number of candles to look back
        
        Returns:
        - Dictionary with trend analysis results
        """
        self.logger.info(f"Analyzing trend at index: {current_idx}")
        result = {"details": ""} # Initialize result dictionary
        # Use config lookback if not specified
        if lookback is None:
            lookback = self.trend_params.get("lookback_period", 5)
        
        # Get indices for the lookback period
        if isinstance(current_idx, str) or isinstance(current_idx, pd.Timestamp):
            indices = processed_data["price"].index.get_loc(current_idx)
            start_idx = max(0, indices - lookback)
            indices = processed_data["price"].index[start_idx:indices+1]
        else:
            start_idx = max(0, current_idx - lookback)
            indices = processed_data["price"].index[start_idx:current_idx+1]
        
        self.logger.debug(f"Trend lookback indices: {list(indices)}")
        
        # Extract data for the lookback period
        price_data = processed_data["price"].loc[indices]
        volume_data = processed_data["volume"].loc[indices]
        volume_class = processed_data["volume_class"].loc[indices]
        
        self.logger.debug(f"Price data (lookback):\n{price_data}")
        self.logger.debug(f"Volume data (lookback):\n{volume_data}")
        self.logger.debug(f"Volume class (lookback):\n{volume_class}")
        
        # Get parameters from config
        params = self.trend_params
        sideways_threshold = params.get("sideways_threshold", 2)
        strong_trend_threshold = params.get("strong_trend_threshold", 5)
        volume_change_threshold = params.get("volume_change_threshold", 10)

        # Calculate percentage price change
        start_price = price_data["close"].iloc[0]
        end_price = price_data["close"].iloc[-1]
        price_change_percent = (end_price - start_price) / start_price * 100

        self.logger.debug(f"Start price: {start_price}, End price: {end_price}, Price change %: {price_change_percent}")

        # Determine trend direction
        if abs(price_change_percent) < sideways_threshold:
            trend_direction = "SIDEWAYS"
        elif price_change_percent > 0:
            trend_direction = "UP" if price_change_percent > strong_trend_threshold else "SLIGHT_UP"
        else:
            trend_direction = "DOWN" if price_change_percent < -strong_trend_threshold else "SLIGHT_DOWN"

        # Analyze volume behavior in trend
        start_volume = volume_data.iloc[0]
        end_volume = volume_data.iloc[-1]
        volume_change_percent = (end_volume - start_volume) / start_volume * 100

        self.logger.debug(f"Start volume: {start_volume}, End volume: {end_volume}, Volume change %: {volume_change_percent}")

        # volume_threshold = self.trend_params.get("volume_change_threshold", 10)  # 10% change
        if abs(volume_change_percent) < volume_change_threshold:
            volume_trend = "FLAT"
        elif volume_change_percent > 0:
            volume_trend = "INCREASING"
        else:
            volume_trend = "DECREASING"

        # Check for trend validation or anomaly
        result = {
            "trend_direction": trend_direction,
            "price_change_percent": round(price_change_percent, 2),
            "volume_trend": volume_trend,
            "volume_change_percent": round(volume_change_percent, 2),
            "signal_type": None,
            "signal_strength": None,
            "details": ""
        }

        self.logger.debug(f"Trend direction: {trend_direction}, Volume trend: {volume_trend}")

        # Apply Marketflow rules for trend validation/anomaly
        if trend_direction in ["UP", "SLIGHT_UP"]:
            if volume_trend == "INCREASING":
                result["signal_type"] = "TREND_VALIDATION"
                result["signal_strength"] = "BULLISH"
                result["details"] = f"Rising price ({result['price_change_percent']}%) with rising volume ({result['volume_change_percent']}%) confirms bullish trend"
            elif volume_trend == "DECREASING":
                result["signal_type"] = "TREND_ANOMALY"
                result["signal_strength"] = "BEARISH"
                result["details"] = f"Rising price ({result['price_change_percent']}%) with falling volume ({result['volume_change_percent']}%) indicates weakening bullish trend"
        
        elif trend_direction in ["DOWN", "SLIGHT_DOWN"]:
            if volume_trend == "INCREASING":
                result["signal_type"] = "TREND_VALIDATION"
                result["signal_strength"] = "BEARISH"
                result["details"] = f"Falling price ({result['price_change_percent']}%) with rising volume ({result['volume_change_percent']}%) confirms bearish trend"
            elif volume_trend == "DECREASING":
                result["signal_type"] = "TREND_ANOMALY"
                result["signal_strength"] = "BULLISH"
                result["details"] = f"Falling price ({result['price_change_percent']}%) with falling volume ({result['volume_change_percent']}%) indicates weakening bearish trend"
        
        else:  # SIDEWAYS
            result["signal_type"] = "CONSOLIDATION"
            result["signal_strength"] = "NEUTRAL"
            result["details"] = f"Sideways price movement ({result['price_change_percent']}%) indicates consolidation"
        
        # Check for climax volume conditions
        high_volume_count = sum(1 for v in volume_class if v in ["HIGH", "VERY_HIGH"])
        if high_volume_count >= 3 and trend_direction == "UP":
            result["details"] += "; Multiple high volume bars in uptrend may indicate buying climax"
            result["signal_strength"] = "BEARISH"
        elif high_volume_count >= 3 and trend_direction == "DOWN":
            result["details"] += "; Multiple high volume bars in downtrend may indicate selling climax"
            result["signal_strength"] = "BULLISH"

        self.logger.info(f"Trend analysis result: {result}")
        self.logger.debug(f"Trend analysis details: {result['details']}")
        return result