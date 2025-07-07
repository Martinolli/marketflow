"""
Marketflow Analyzer Module

This module provides analysis and pattern recognition for the Marketflow algorithm.
"""

import pandas as pd
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_processor import DataProcessor

class CandleAnalyzer:
    """Analyze individual candles"""
    
    def __init__(self, parameters=None):
                
        # Initialize Logger
        self.logger = get_logger(module_name="MarketflowAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

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

class PatternRecognizer:
    """Recognize Marketflow patterns"""
    
    def __init__(self, parameters=None):

        # Initialize Logger
        self.logger = get_logger(module_name="PatternRecognizer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)
        
        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()

        self.pattern_params = self.parameters.get_pattern_parameters()
    
    def identify_patterns(self, processed_data: dict, current_idx, lookback=20) -> dict:
        """
        Identify Marketflow patterns in the price and volume data

        Parameters:
        - processed_data: Dictionary with processed data
        - current_idx: Index of the current candle
        - lookback: Number of candles to look back

        Returns:
        - Dictionary with pattern recognition results
        """
        self.logger.info(f"Identifying patterns at index: {current_idx} with lookback: {lookback}")

        # Get indices for the lookback period
        if isinstance(current_idx, str) or isinstance(current_idx, pd.Timestamp):
            indices = processed_data["price"].index.get_loc(current_idx)
            start_idx = max(0, indices - lookback)
            indices = processed_data["price"].index[start_idx:indices+1]
        else:
            start_idx = max(0, current_idx - lookback)
            indices = processed_data["price"].index[start_idx:current_idx+1]

        self.logger.debug(f"Pattern lookback indices: {list(indices)}")

        # Extract data for the lookback period
        price_data = processed_data["price"].loc[indices]
        volume_data = processed_data["volume"].loc[indices]
        volume_class = processed_data["volume_class"].loc[indices]

        self.logger.debug(f"Price data (lookback):\n{price_data}")
        self.logger.debug(f"Volume data (lookback):\n{volume_data}")
        self.logger.debug(f"Volume class (lookback):\n{volume_class}")

        # Initialize pattern results
        patterns = {
            "accumulation": self.detect_accumulation(price_data, volume_data, volume_class),
            "distribution": self.detect_distribution(price_data, volume_data, volume_class),
            "testing": self.detect_testing(price_data, volume_class),
            "buying_climax": self.detect_buying_climax(price_data, volume_data, volume_class),
            "selling_climax": self.detect_selling_climax(price_data, volume_data, volume_class)
        }

        self.logger.info(f"Pattern recognition results: {patterns}")
        self.logger.debug(f"Pattern details: {patterns}")

        return patterns
    
    def detect_accumulation(self, price_data, volume_data, volume_class) -> dict:
        """
        Detect accumulation patterns
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        - volume_class: Series with volume classifications
        
        Returns:
        - Dictionary with accumulation pattern details
        """
        self.logger.info("Detecting accumulation pattern")
        self.logger.debug(f"Price data shape: {price_data.shape}")
        self.logger.debug(f"Volume data shape: {volume_data.shape}")
        self.logger.debug(f"Volume class: {list(volume_class)}")

        # Get parameters from config
        params = self.parameters.pattern_params.get("accumulation", {})
        price_volatility_threshold = params.get("price_volatility_threshold", 0.08)
        high_volume_threshold = params.get("high_volume_threshold", 2)
        support_tests_threshold = params.get("support_tests_threshold", 1)
        
        # Check for sideways price movement with increasing volume
        price_range = price_data["high"].max() - price_data["low"].min()
        avg_price = price_data["close"].mean()
        price_volatility = price_range / avg_price

        self.logger.debug(f"Price range: {price_range}, Avg price: {avg_price}, Price volatility: {price_volatility}")
        
        # Accumulation typically shows sideways price with high volume
        is_sideways = price_volatility < price_volatility_threshold
        high_volume_count = sum(1 for v in volume_class if v in ["HIGH", "VERY_HIGH"])

        self.logger.debug(f"Is sideways: {is_sideways}, High volume count: {high_volume_count}")
        
        # Check for tests of support with decreasing volume
        support_tests = 0
        for i in range(1, len(price_data)):
            if (price_data["low"].iloc[i] < price_data["low"].iloc[i-1] * 1.01 and
                price_data["low"].iloc[i] > price_data["low"].iloc[i-1] * 0.99):
                support_tests += 1

        self.logger.debug(f"Support tests: {support_tests}")
        
        # Determine if accumulation is present
        strength = 0
        if is_sideways:
            strength += 1
        if high_volume_count >= high_volume_threshold:
            strength += 1
        if support_tests >= support_tests_threshold:
            strength += 1

        result = {
            "detected": strength >= 2,
            "strength": strength,
            "details": f"Sideways: {is_sideways}, High volume count: {high_volume_count}, Support tests: {support_tests}"
        }

        self.logger.info(f"Accumulation detection result: {result}")
        self.logger.debug(f"Accumulation details: {result['details']}")
        return result
    def detect_distribution(self, price_data, volume_data, volume_class) -> dict:
        """
        Detect distribution patterns
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        - volume_class: Series with volume classifications
        
        Returns:
        - Dictionary with distribution pattern details
        """
        self.logger.info("Detecting distribution pattern")
        self.logger.debug(f"Price data shape: {price_data.shape}")
        self.logger.debug(f"Volume data shape: {volume_data.shape}")
        self.logger.debug(f"Volume class: {list(volume_class)}")

        # Get parameters from config
        params = self.parameters.pattern_params.get("distribution", {})
        price_volatility_threshold = params.get("price_volatility_threshold", 0.08)
        high_volume_threshold = params.get("high_volume_threshold", 2)
        resistance_tests_threshold = params.get("resistance_tests_threshold", 1)
        
        # Check for sideways price movement with increasing volume
        price_range = price_data["high"].max() - price_data["low"].min()
        avg_price = price_data["close"].mean()
        price_volatility = price_range / avg_price

        self.logger.debug(f"Price range: {price_range}, Avg price: {avg_price}, Price volatility: {price_volatility}")
        
        # Distribution typically shows sideways price with high volume
        is_sideways = price_volatility < price_volatility_threshold
        high_volume_count = sum(1 for v in volume_class if v in ["HIGH", "VERY_HIGH"])

        self.logger.debug(f"Is sideways: {is_sideways}, High volume count: {high_volume_count}")
        
        # Check for tests of resistance with decreasing volume
        resistance_tests = 0
        for i in range(1, len(price_data)):
            if (price_data["high"].iloc[i] > price_data["high"].iloc[i-1] * 0.99 and
                price_data["high"].iloc[i] < price_data["high"].iloc[i-1] * 1.01):
                resistance_tests += 1

        self.logger.debug(f"Resistance tests: {resistance_tests}")
        
        # Determine if distribution is present
        strength = 0
        if is_sideways:
            strength += 1
        if high_volume_count >= high_volume_threshold:
            strength += 1
        if resistance_tests >= resistance_tests_threshold:
            strength += 1
        
        result = {
            "detected": strength >= 2,
            "strength": strength,
            "details": f"Sideways: {is_sideways}, High volume count: {high_volume_count}, Resistance tests: {resistance_tests}"
        }

        self.logger.info(f"Distribution detection result: {result}")
        self.logger.debug(f"Distribution details: {result['details']}")
        return result
    def detect_testing(self, price_data, volume_class) -> dict:
        """
        Detect testing patterns
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_class: Series with volume classifications
        
        Returns:
        - Dictionary with testing pattern details, including a list of individual tests.
        """
        self.logger.info("Detecting testing patterns")
        self.logger.debug(f"Price data shape: {price_data.shape}")
        self.logger.debug(f"Volume class: {list(volume_class)}")

        tests = []
        # Look for tests of support (lows)
        for i in range(1, len(price_data)):
            # Check if current low is near a recent previous low
            is_test_of_low = any(
                abs(price_data["low"].iloc[i] - price_data["low"].iloc[j]) / price_data["low"].iloc[j] < 0.01
                for j in range(max(0, i - 5), i)
            )
            # Successful test occurs on low volume
            if is_test_of_low and volume_class.iloc[i] in ["LOW", "VERY_LOW"]:
                tests.append({
                    "type": "SUPPORT_TEST",
                    "index": price_data.index[i],
                    "price": price_data["low"].iloc[i]
                })

        # Look for tests of resistance (highs)
        for i in range(1, len(price_data)):
            # Check if current high is near a recent previous high
            is_test_of_high = any(
                abs(price_data["high"].iloc[i] - price_data["high"].iloc[j]) / price_data["high"].iloc[j] < 0.01
                for j in range(max(0, i - 5), i)
            )
            # Successful test occurs on low volume
            if is_test_of_high and volume_class.iloc[i] in ["LOW", "VERY_LOW"]:
                tests.append({
                    "type": "RESISTANCE_TEST",
                    "index": price_data.index[i],
                    "price": price_data["high"].iloc[i]
                })

        detected = len(tests) > 0

        self.logger.info(f"Testing pattern detection result: detected={detected}, count={len(tests)}")
        self.logger.debug(f"Testing pattern details: {tests}")

        return {
            "detected": detected,
            "strength": len(tests),
            "details": f"Found {len(tests)} testing patterns.",
            "tests": tests  # This list is what the visualizer expects
        }
    
    def detect_buying_climax(self, price_data, volume_data, volume_class) -> dict:
        """
        Detect buying climax patterns
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        - volume_class: Series with volume classifications
        
        Returns:
        - Dictionary with buying climax pattern details
        """
        self.logger.info("Detecting buying climax pattern")
        self.logger.debug(f"Price data shape: {price_data.shape}")
        self.logger.debug(f"Volume data shape: {volume_data.shape}")
        self.logger.debug(f"Volume class: {list(volume_class)}")

        # Get parameters from config
        params = self.parameters.pattern_params.get("buying_climax", {})
        near_high_threshold = params.get("near_high_threshold", 0.93)
        wide_up_threshold = params.get("wide_up_threshold", 0.6)
        upper_wick_threshold = params.get("upper_wick_threshold", 0.25)
        
        # Buying climax typically shows extremely high volume at market tops
        # with wide spread up candles followed by reversal
        
        # Check if we're near the high of the period
        is_near_high = price_data["close"].iloc[-1] >= price_data["high"].max() * near_high_threshold
        self.logger.debug(f"is_near_high: {is_near_high}")

        # Check for very high volume
        very_high_volume = volume_class.iloc[-1] in ["VERY_HIGH", "HIGH"]
        self.logger.debug(f"very_high_volume: {very_high_volume}")

        # Check for wide spread up candle
        is_wide_up = (price_data["close"].iloc[-1] > price_data["open"].iloc[-1] and
                     (price_data["close"].iloc[-1] - price_data["open"].iloc[-1]) > 
                     (price_data["high"].iloc[-1] - price_data["low"].iloc[-1]) * wide_up_threshold)
        self.logger.debug(f"is_wide_up: {is_wide_up}")

        # Check for upper wick (potential reversal sign)
        has_upper_wick = (price_data["high"].iloc[-1] - price_data["close"].iloc[-1]) > (price_data["close"].iloc[-1] - price_data["open"].iloc[-1]) * upper_wick_threshold
        self.logger.debug(f"has_upper_wick: {has_upper_wick}")

        # Determine if buying climax is present
        strength = 0
        if is_near_high:
            strength += 1
        if very_high_volume:
            strength += 2
        if is_wide_up:
            strength += 1
        if has_upper_wick:
            strength += 1

        result = {
            "detected": strength >= 3,
            "strength": strength,
            "details": f"Near high: {is_near_high}, Very high volume: {very_high_volume}, Wide up candle: {is_wide_up}, Upper wick: {has_upper_wick}"
        }

        self.logger.info(f"Buying climax detection result: {result}")
        self.logger.debug(f"Buying climax details: {result['details']}")
        return result
    def detect_selling_climax(self, price_data, volume_data, volume_class) -> dict:
        """
        Detect selling climax patterns
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        - volume_class: Series with volume classifications
        
        Returns:
        - Dictionary with selling climax pattern details
        """
        self.logger.info("Detecting selling climax pattern")
        self.logger.debug(f"Price data shape: {price_data.shape}")
        self.logger.debug(f"Volume data shape: {volume_data.shape}")
        self.logger.debug(f"Volume class: {list(volume_class)}")

        # Get parameters from config
        params = self.parameters.pattern_params.get("selling_climax", {})
        near_low_threshold = params.get("near_low_threshold", 1.07)
        wide_down_threshold = params.get("wide_down_threshold", 0.6)
        lower_wick_threshold = params.get("lower_wick_threshold", 0.25)
        
        # Selling climax typically shows extremely high volume at market bottoms
        # with wide spread down candles followed by reversal
        
        # Check if we're near the low of the period
        is_near_low = price_data["close"].iloc[-1] <= price_data["low"].min() * near_low_threshold
        self.logger.debug(f"is_near_low: {is_near_low}")

        # Check for very high volume
        very_high_volume = volume_class.iloc[-1] in ["VERY_HIGH", "HIGH"]
        self.logger.debug(f"very_high_volume: {very_high_volume}")

        # Check for wide spread down candle
        is_wide_down = (price_data["close"].iloc[-1] < price_data["open"].iloc[-1] and
                       (price_data["open"].iloc[-1] - price_data["close"].iloc[-1]) > 
                       (price_data["high"].iloc[-1] - price_data["low"].iloc[-1]) * wide_down_threshold)
        self.logger.debug(f"is_wide_down: {is_wide_down}")

        # Check for lower wick (potential reversal sign)
        has_lower_wick = (price_data["close"].iloc[-1] - price_data["low"].iloc[-1]) > (price_data["open"].iloc[-1] - price_data["close"].iloc[-1]) * lower_wick_threshold
        self.logger.debug(f"has_lower_wick: {has_lower_wick}")

        # Determine if selling climax is present
        strength = 0
        if is_near_low:
            strength += 1
        if very_high_volume:
            strength += 2
        if is_wide_down:
            strength += 1
        if has_lower_wick:
            strength += 1
        
        result = {
            "detected": strength >= 3,
            "strength": strength,
            "details": f"Near low: {is_near_low}, Very high volume: {very_high_volume}, Wide down candle: {is_wide_down}, Lower wick: {has_lower_wick}"
        }

        self.logger.info(f"Selling climax detection result: {result}")
        self.logger.debug(f"Selling climax details: {result['details']}")
        return result

class SupportResistanceAnalyzer:
    """Analyze support and resistance levels"""
    
    def __init__(self, parameters=None):
        
        # Initialize Logger
        self.logger = get_logger(module_name="MarketflowAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()
    
    def analyze_support_resistance(self, processed_data: dict, lookback=50) -> dict:
        """
        Identify key support and resistance levels based on price and volume

        Parameters:
        - processed_data: Dictionary with processed data
        - lookback: Number of candles to look back

        Returns:
        - Dictionary with support and resistance levels
        """
        self.logger.info("Analyzing support and resistance levels")
        self.logger.debug(f"Processed data keys: {list(processed_data.keys())}, lookback: {lookback}")

        # Extract data
        price_data = processed_data["price"].iloc[-lookback:]
        volume_data = processed_data["volume"].iloc[-lookback:]

        self.logger.debug(f"Price data shape: {price_data.shape}, Volume data shape: {volume_data.shape}")

        # Find potential support/resistance levels
        support_levels = self.find_support_levels(price_data, volume_data)
        resistance_levels = self.find_resistance_levels(price_data, volume_data)

        self.logger.debug(f"Found {len(support_levels)} support levels, {len(resistance_levels)} resistance levels")

        # Analyze volume at these levels
        volume_at_levels = self.analyze_volume_at_price(price_data, volume_data, support_levels, resistance_levels)

        self.logger.debug(f"Volume at levels: {volume_at_levels}")

        return {
            "support": support_levels,
            "resistance": resistance_levels,
            "volume_at_levels": volume_at_levels
        }

    def find_support_levels(self, price_data, volume_data) -> list:
        """
        Find potential support levels based on price and volume

        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data

        Returns:
        - List of support levels with details
        """
        self.logger.info("Finding support levels")
        self.logger.debug(f"Price data shape: {price_data.shape}, Volume data shape: {volume_data.shape}")

        support_levels = []

        # Find local lows
        for i in range(2, len(price_data) - 2):
            if (price_data["low"].iloc[i] < price_data["low"].iloc[i-1] and
                price_data["low"].iloc[i] < price_data["low"].iloc[i-2] and
                price_data["low"].iloc[i] < price_data["low"].iloc[i+1] and
                price_data["low"].iloc[i] < price_data["low"].iloc[i+2]):

                # Found a local low
                support_level = {
                    "price": price_data["low"].iloc[i],
                    "index": price_data.index[i],
                    "volume": volume_data.iloc[i],
                    "strength": 1
                }

                # Check if volume was high (adds strength)
                if volume_data.iloc[i] > volume_data.iloc[i-1:i+2].mean() * 1.5:
                    support_level["strength"] += 1
                    support_level["high_volume"] = True

                # Check if this level was tested multiple times
                tests = 0
                for j in range(i+1, len(price_data)):
                    if abs(price_data["low"].iloc[j] - support_level["price"]) / support_level["price"] < 0.005:
                        tests += 1
                        support_level["strength"] += 0.5

                support_level["tests"] = tests
                support_levels.append(support_level)
                self.logger.debug(f"Support level found: {support_level}")

        # Sort by strength
        support_levels.sort(key=lambda x: x["strength"], reverse=True)

        # Keep only the strongest levels (avoid too many close levels)
        filtered_levels = []
        for level in support_levels:
            # Check if this level is too close to an already included level
            too_close = False
            for included in filtered_levels:
                if abs(level["price"] - included["price"]) / included["price"] < 0.01:
                    too_close = True
                    break

            if not too_close:
                filtered_levels.append(level)
                self.logger.debug(f"Support level added to filtered: {level}")

        self.logger.info(f"Total filtered support levels: {len(filtered_levels)}")
        return filtered_levels[:5]  # Return top 5 support levels
    def find_resistance_levels(self, price_data, volume_data) -> list:
        """
        Find potential resistance levels based on price and volume
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        
        Returns:
        - List of resistance levels with details
        """
        self.logger.info("Finding resistance levels")
        self.logger.debug(f"Price data shape: {price_data.shape}, Volume data shape: {volume_data.shape}")

        resistance_levels = []
        
        # Find local highs
        for i in range(2, len(price_data) - 2):
            if (price_data["high"].iloc[i] > price_data["high"].iloc[i-1] and
                price_data["high"].iloc[i] > price_data["high"].iloc[i-2] and
                price_data["high"].iloc[i] > price_data["high"].iloc[i+1] and
                price_data["high"].iloc[i] > price_data["high"].iloc[i+2]):
                
                # Found a local high
                resistance_level = {
                    "price": price_data["high"].iloc[i],
                    "index": price_data.index[i],
                    "volume": volume_data.iloc[i],
                    "strength": 1
                }
                
                # Check if volume was high (adds strength)
                if volume_data.iloc[i] > volume_data.iloc[i-1:i+2].mean() * 1.5:
                    resistance_level["strength"] += 1
                    resistance_level["high_volume"] = True
                
                # Check if this level was tested multiple times
                tests = 0
                for j in range(i+1, len(price_data)):
                    if abs(price_data["high"].iloc[j] - resistance_level["price"]) / resistance_level["price"] < 0.005:
                        tests += 1
                        resistance_level["strength"] += 0.5
                
                resistance_level["tests"] = tests
                resistance_levels.append(resistance_level)
                self.logger.debug(f"Resistance level found: {resistance_level}")
        
        # Sort by strength
        resistance_levels.sort(key=lambda x: x["strength"], reverse=True)
        
        # Keep only the strongest levels (avoid too many close levels)
        filtered_levels = []
        for level in resistance_levels:
            # Check if this level is too close to an already included level
            too_close = False
            for included in filtered_levels:
                if abs(level["price"] - included["price"]) / included["price"] < 0.01:
                    too_close = True
                    break
            
            if not too_close:
                filtered_levels.append(level)
                self.logger.debug(f"Resistance level added to filtered: {level}")
        
        self.logger.info(f"Total filtered resistance levels: {len(filtered_levels)}")
        return filtered_levels[:5]  # Return top 5 resistance levels
    def analyze_volume_at_price(self, price_data, volume_data, support_levels: list, resistance_levels: list) -> dict:
        """
        Analyze volume at key price levels
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        - support_levels: List of support levels
        - resistance_levels: List of resistance levels
        
        Returns:
        - Dictionary with volume analysis at key levels
        """
        self.logger.info("Analyzing volume at key price levels")
        self.logger.debug(f"Support levels: {support_levels}")
        self.logger.debug(f"Resistance levels: {resistance_levels}")
        self.logger.debug(f"Price data shape: {price_data.shape}, Volume data shape: {volume_data.shape}")

        # Create price bins
        all_levels = [(level["price"], "support") for level in support_levels]
        all_levels.extend([(level["price"], "resistance") for level in resistance_levels])
        
        # Sort levels by price
        all_levels.sort(key=lambda x: x[0])
        self.logger.debug(f"All levels sorted: {all_levels}")
        
        # Analyze volume at each level
        volume_at_levels = {}
        for price, level_type in all_levels:
            # Find candles that traded at this level
            candles_at_level = []
            for i in range(len(price_data)):
                if price_data["low"].iloc[i] <= price <= price_data["high"].iloc[i]:
                    candles_at_level.append(i)
            
            # Calculate total and average volume at this level
            total_volume = sum(volume_data.iloc[candles_at_level]) if candles_at_level else 0
            avg_volume = total_volume / len(candles_at_level) if candles_at_level else 0
            
            volume_at_levels[price] = {
                "type": level_type,
                "candles_count": len(candles_at_level),
                "total_volume": total_volume,
                "avg_volume": avg_volume
            }
            self.logger.debug(
                f"Level {price} ({level_type}): candles={len(candles_at_level)}, "
                f"total_volume={total_volume}, avg_volume={avg_volume}"
            )
        
        self.logger.info(f"Volume at levels analysis complete: {volume_at_levels}")
        return volume_at_levels

class MultiTimeframeAnalyzer:
    """Analyze data across multiple timeframes"""
    
    def __init__(self, parameters=None):

        # Initialize Logger
        self.logger = get_logger(module_name="MarketflowAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()

        self.candle_analyzer = CandleAnalyzer(self.parameters)
        self.trend_analyzer = TrendAnalyzer(self.parameters)
        self.pattern_recognizer = PatternRecognizer(self.parameters)
        self.sr_analyzer = SupportResistanceAnalyzer(self.parameters)
        self.processor = DataProcessor(self.parameters)
    
    def analyze_multiple_timeframes(self, timeframe_data: dict) -> dict:
        """
        Perform Marketflow analysis across multiple timeframes
        
        Parameters:
        - timeframe_data: Dictionary with price and volume data for each timeframe
        
        Returns:
        - Dictionary with analysis results for each timeframe
        """
        self.logger.info("Starting multi-timeframe analysis")
        self.logger.debug(f"Timeframes received: {list(timeframe_data.keys())}")

        results = {}
        
        for timeframe in timeframe_data:
            self.logger.info(f"Analyzing timeframe: {timeframe}")
            # Get data for this timeframe
            price_data = timeframe_data[timeframe]['price_data']
            volume_data = timeframe_data[timeframe]['volume_data']
            self.logger.debug(f"Price data shape: {getattr(price_data, 'shape', None)}, Volume data shape: {getattr(volume_data, 'shape', None)}")
            
            # Preprocess data
            processed_data = self.processor.preprocess_data(price_data=price_data, volume_data=volume_data)
            self.logger.debug(f"Processed data keys: {list(processed_data.keys())}")
            
            # Perform analysis
            current_idx = processed_data["price"].index[-1]
            candle_analysis = self.candle_analyzer.analyze_candle(current_idx, processed_data)
            trend_analysis = self.trend_analyzer.analyze_trend(processed_data, current_idx)
            pattern_analysis = self.pattern_recognizer.identify_patterns(processed_data, current_idx)
            sr_analysis = self.sr_analyzer.analyze_support_resistance(processed_data)
            
            results[timeframe] = {
                "candle_analysis": candle_analysis,
                "trend_analysis": trend_analysis,
                "pattern_analysis": pattern_analysis,
                "support_resistance": sr_analysis,
                "processed_data": processed_data  # Store processed data for visualization
            }
            self.logger.debug(f"Analysis results for {timeframe}: {results[timeframe]}")
        
        # Look for confirmation across timeframes
        confirmations = self.identify_timeframe_confirmations(results)
        self.logger.info(f"Multi-timeframe confirmations: {confirmations}")
        
        return results, confirmations
    
    def identify_timeframe_confirmations(self, results: dict) -> dict:
        """
        Identify confirmations and divergences across timeframes
        
        Parameters:
        - results: Dictionary with analysis results for each timeframe
        
        Returns:
        - Dictionary with confirmation analysis
        """
        self.logger.info("Identifying confirmations and divergences across timeframes")
        timeframes = list(results.keys())
        self.logger.debug(f"Timeframes for confirmation: {timeframes}")

        confirmations = {
            "bullish": [],
            "bearish": [],
            "divergences": []
        }
        
        # Check for bullish confirmations
        for tf in timeframes:
            candle_signal = results[tf]["candle_analysis"]["signal_strength"]
            trend_signal = results[tf]["trend_analysis"]["signal_strength"]
            self.logger.debug(f"{tf} - Candle: {candle_signal}, Trend: {trend_signal}")
            if candle_signal == "BULLISH" and trend_signal == "BULLISH":
                confirmations["bullish"].append(tf)
        
        # Check for bearish confirmations
        for tf in timeframes:
            candle_signal = results[tf]["candle_analysis"]["signal_strength"]
            trend_signal = results[tf]["trend_analysis"]["signal_strength"]
            self.logger.debug(f"{tf} - Candle: {candle_signal}, Trend: {trend_signal}")
            if candle_signal == "BEARISH" and trend_signal == "BEARISH":
                confirmations["bearish"].append(tf)
        
        # Check for divergences
        for i in range(len(timeframes) - 1):
            for j in range(i + 1, len(timeframes)):
                tf1 = timeframes[i]
                tf2 = timeframes[j]
                
                candle_signal1 = results[tf1]["candle_analysis"]["signal_strength"]
                candle_signal2 = results[tf2]["candle_analysis"]["signal_strength"]
                self.logger.debug(f"Comparing {tf1} ({candle_signal1}) vs {tf2} ({candle_signal2})")
                
                if (candle_signal1 == "BULLISH" and candle_signal2 == "BEARISH") or \
                   (candle_signal1 == "BEARISH" and candle_signal2 == "BULLISH"):
                    confirmations["divergences"].append((tf1, tf2))
        
        self.logger.info(f"Confirmation results: {confirmations}")
        return confirmations

class PointInTimeAnalyzer:
    """Analyze data at a specific point in time for Marketflow signals"""
    
    def __init__(self, parameters=None):
        """
        Initialize the point-in-time analyzer
        
        Parameters:
        - config: MarketflowConfig instance
        - logger: Logger instance
        """
        # Initialize Logger
        self.logger = get_logger(module_name="PointInTimeAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()

        self.candle_analyzer = CandleAnalyzer(self.parameters)
        self.trend_analyzer = TrendAnalyzer(self.parameters)
        self.pattern_recognizer = PatternRecognizer(self.parameters)
        self.sr_analyzer = SupportResistanceAnalyzer(self.parameters)
    
    def analyze_all(self, processed_timeframe_data: dict) -> dict:
        """
        Analyze all timeframes at a specific point in time

        Parameters:
        - processed_timeframe_data: Dictionary with processed data for each timeframe

        Returns:
        - Dictionary with analysis results for each timeframe
        """
        if self.logger:
            self.logger.info("Starting analyze_all for point-in-time analysis")
            self.logger.debug(f"Received timeframes: {list(processed_timeframe_data.keys()) if processed_timeframe_data else []}")

        if not processed_timeframe_data:
            if self.logger:
                self.logger.error("No processed data provided to analyze_all")
            return {}

        signals = {}

        for tf, processed_data in processed_timeframe_data.items():
            try:
                if self.logger:
                    self.logger.info(f"Analyzing timeframe: {tf}")
                    self.logger.debug(f"Processed data keys for {tf}: {list(processed_data.keys()) if processed_data else []}")

                if not processed_data or "price" not in processed_data or processed_data["price"].empty:
                    if self.logger:
                        self.logger.warning(f"Empty or invalid processed data for timeframe {tf}")
                    continue

                # Get the last index (point in time)
                current_idx = processed_data["price"].index[-1]
                if self.logger:
                    self.logger.debug(f"Current index for {tf}: {current_idx}")

                # Analyze candle
                candle_analysis = self.candle_analyzer.analyze_candle(current_idx, processed_data)
                if self.logger:
                    self.logger.debug(f"Candle analysis for {tf}: {candle_analysis}")

                # Analyze trend
                trend_analysis = self.trend_analyzer.analyze_trend(processed_data, current_idx)
                if self.logger:
                    self.logger.debug(f"Trend analysis for {tf}: {trend_analysis}")

                # Identify patterns
                pattern_analysis = self.pattern_recognizer.identify_patterns(processed_data, current_idx)
                if self.logger:
                    self.logger.debug(f"Pattern analysis for {tf}: {pattern_analysis}")

                # Analyze support/resistance
                sr_analysis = self.sr_analyzer.analyze_support_resistance(processed_data)
                if self.logger:
                    self.logger.debug(f"Support/resistance analysis for {tf}: {sr_analysis}")

                # Combine results
                signals[tf] = {
                    "candle": candle_analysis,
                    "trend": trend_analysis,
                    "patterns": pattern_analysis,
                    "support_resistance": sr_analysis,
                    "timestamp": current_idx
                }

                # Add a summary of detected patterns
                pattern_summary = []
                for pattern_name, pattern_data in pattern_analysis.items():
                    if pattern_data.get("detected", False):
                        pattern_summary.append(f"{pattern_name.replace('_', ' ').title()} (Strength: {pattern_data.get('strength', 0)})")

                signals[tf]["pattern_summary"] = ", ".join(pattern_summary) if pattern_summary else "No significant patterns detected"

                if self.logger:
                    self.logger.info(f"Completed analysis for timeframe {tf}")
                    self.logger.debug(f"Signals for {tf}: {signals[tf]}")

            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error analyzing timeframe {tf}: {str(e)}")
                    self.logger.exception("Exception details:")
                else:
                    print(f"Error analyzing timeframe {tf}: {str(e)}")

        if self.logger:
            self.logger.info("Completed analyze_all for all timeframes")
            self.logger.debug(f"Final signals: {signals}")

        return signals
    def compute_risk_reward(self, processed_data: dict, signals: dict) -> dict:
        """
        Compute risk-reward metrics based on analysis

        Parameters:
        - processed_data: Dictionary with processed data
        - signals: Dictionary with analysis signals

        Returns:
        - Dictionary with risk-reward metrics
        """
        if self.logger:
            self.logger.info("Starting compute_risk_reward")
            self.logger.debug(f"Processed data keys: {list(processed_data.keys()) if processed_data else []}")
            self.logger.debug(f"Signals keys: {list(signals.keys()) if signals else []}")

        if not processed_data or "price" not in processed_data or processed_data["price"].empty:
            if self.logger:
                self.logger.warning("Processed data is empty or missing 'price'")
            return {"risk_reward_ratio": 0, "stop_loss": 0, "take_profit": 0}

        # Get current price
        current_price = processed_data["price"]["close"].iloc[-1]
        if self.logger:
            self.logger.debug(f"Current price: {current_price}")

        # Get support/resistance levels
        support_levels = []
        resistance_levels = []

        if "support_resistance" in signals and "support" in signals["support_resistance"]:
            for level in signals["support_resistance"]["support"]:
                support_levels.append(level["price"])
        if "support_resistance" in signals and "resistance" in signals["support_resistance"]:
            for level in signals["support_resistance"]["resistance"]:
                resistance_levels.append(level["price"])

        if self.logger:
            self.logger.debug(f"Support levels: {support_levels}")
            self.logger.debug(f"Resistance levels: {resistance_levels}")

        # Determine signal type
        signal_type = "NEUTRAL"
        if "candle" in signals and "signal_strength" in signals["candle"]:
            signal_type = signals["candle"]["signal_strength"]

        if self.logger:
            self.logger.debug(f"Signal type: {signal_type}")

        # Calculate stop loss and take profit
        stop_loss = current_price
        take_profit = current_price

        if signal_type == "BULLISH":
            # For bullish signals, stop loss is below nearest support, take profit at nearest resistance
            if support_levels:
                nearest_support = max([s for s in support_levels if s < current_price], default=current_price * 0.95)
                stop_loss = nearest_support
            else:
                stop_loss = current_price * 0.95  # Default 5% below current price

            if resistance_levels:
                nearest_resistance = min([r for r in resistance_levels if r > current_price], default=current_price * 1.1)
                take_profit = nearest_resistance
            else:
                take_profit = current_price * 1.1  # Default 10% above current price

        elif signal_type == "BEARISH":
            # For bearish signals, stop loss is above nearest resistance, take profit at nearest support
            if resistance_levels:
                nearest_resistance = min([r for r in resistance_levels if r > current_price], default=current_price * 1.05)
                stop_loss = nearest_resistance
            else:
                stop_loss = current_price * 1.05  # Default 5% above current price

            if support_levels:
                nearest_support = max([s for s in support_levels if s < current_price], default=current_price * 0.9)
                take_profit = nearest_support
            else:
                take_profit = current_price * 0.9  # Default 10% below current price

        # Calculate risk-reward ratio
        risk = abs(current_price - stop_loss)
        reward = abs(take_profit - current_price)
        risk_reward_ratio = reward / risk if risk > 0 else 0

        result = {
            "current_price": current_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk": risk,
            "reward": reward,
            "risk_reward_ratio": risk_reward_ratio
        }

        if self.logger:
            self.logger.info("Completed compute_risk_reward")
            self.logger.debug(f"Risk-reward result: {result}")

        return result
    
    def compute_volatility(self, processed_data: dict, lookback=20) -> dict:
        """
        Compute volatility metrics

        Parameters:
        - processed_data: Dictionary with processed data
        - lookback: Number of candles to look back

        Returns:
        - Dictionary with volatility metrics
        """
        if self.logger:
            self.logger.info("Starting compute_volatility")
            self.logger.debug(f"Processed data keys: {list(processed_data.keys()) if processed_data else []}, lookback: {lookback}")

        if not processed_data or "price" not in processed_data or processed_data["price"].empty:
            if self.logger:
                self.logger.warning("Processed data is empty or missing 'price'")
            return {"atr": 0, "volatility_percent": 0}

        # Get price data for lookback period
        price_data = processed_data["price"].iloc[-lookback:]
        if self.logger:
            self.logger.debug(f"Price data shape: {price_data.shape}")

        # Calculate Average True Range (ATR)
        true_ranges = []
        for i in range(1, len(price_data)):
            high = price_data["high"].iloc[i]
            low = price_data["low"].iloc[i]
            prev_close = price_data["close"].iloc[i-1]

            tr1 = high - low
            tr2 = abs(high - prev_close)
            tr3 = abs(low - prev_close)

            true_range = max(tr1, tr2, tr3)
            true_ranges.append(true_range)
            if self.logger:
                self.logger.debug(f"Index {i}: high={high}, low={low}, prev_close={prev_close}, tr1={tr1}, tr2={tr2}, tr3={tr3}, true_range={true_range}")

        atr = sum(true_ranges) / len(true_ranges) if true_ranges else 0

        # Calculate volatility as percentage of price
        current_price = price_data["close"].iloc[-1]
        volatility_percent = (atr / current_price) * 100 if current_price > 0 else 0

        result = {
            "atr": atr,
            "volatility_percent": volatility_percent,
            "true_ranges": true_ranges
        }

        if self.logger:
            self.logger.info("Completed compute_volatility")
            self.logger.debug(f"Volatility result: {result}")

        return result
    
    def compute_confidence_score(self, signals: dict) -> float:
        """
        Compute confidence score based on signals across timeframes

        Parameters:
        - signals: Dictionary with analysis signals for each timeframe

        Returns:
        - Float confidence score (0-100)
        """
        if self.logger:
            self.logger.info("Starting compute_confidence_score")
            self.logger.debug(f"Signals received: {signals}")

        if not signals:
            if self.logger:
                self.logger.warning("No signals provided to compute_confidence_score")
            return 0

        # Initialize score
        score = 50  # Neutral starting point

        # Count bullish and bearish signals
        bullish_count = 0
        bearish_count = 0
        neutral_count = 0

        # Check candle signals
        for tf, tf_signals in signals.items():
            if "candle" in tf_signals and "signal_strength" in tf_signals["candle"]:
                if tf_signals["candle"]["signal_strength"] == "BULLISH":
                    bullish_count += 1
                elif tf_signals["candle"]["signal_strength"] == "BEARISH":
                    bearish_count += 1
                else:
                    neutral_count += 1

        # Check trend signals
        for tf, tf_signals in signals.items():
            if "trend" in tf_signals and "signal_strength" in tf_signals["trend"]:
                if tf_signals["trend"]["signal_strength"] == "BULLISH":
                    bullish_count += 1
                elif tf_signals["trend"]["signal_strength"] == "BEARISH":
                    bearish_count += 1
                else:
                    neutral_count += 1

        # Check pattern signals
        for tf, tf_signals in signals.items():
            if "patterns" in tf_signals:
                for pattern_name, pattern_data in tf_signals["patterns"].items():
                    if pattern_data.get("detected", False):
                        if "climax" in pattern_name:
                            # Climax patterns are strong signals
                            if "buying" in pattern_name:
                                bearish_count += 2  # Buying climax is bearish
                            elif "selling" in pattern_name:
                                bullish_count += 2  # Selling climax is bullish
                        elif "accumulation" in pattern_name:
                            bullish_count += 1
                        elif "distribution" in pattern_name:
                            bearish_count += 1

        if self.logger:
            self.logger.debug(f"Bullish count: {bullish_count}, Bearish count: {bearish_count}, Neutral count: {neutral_count}")

        # Calculate final score
        total_signals = bullish_count + bearish_count + neutral_count
        if total_signals > 0:
            bullish_weight = bullish_count / total_signals
            bearish_weight = bearish_count / total_signals

            # Adjust score based on signal weights
            score += bullish_weight * 25  # Max +25 points for bullish signals
            score -= bearish_weight * 25  # Max -25 points for bearish signals

        # Ensure score is within 0-100 range
        score = max(0, min(100, score))

        if self.logger:
            self.logger.info("Completed compute_confidence_score")
            self.logger.debug(f"Final confidence score: {score}")

        return score