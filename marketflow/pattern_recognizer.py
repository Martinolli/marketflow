"""
Pattern Recognizer Module

Handles pattern recognition for MarketFlow, such as accumulation/distribution.
"""

import pandas as pd

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config


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