"""
Support/Resistance Analyzer Module

Analyzes support and resistance levels for MarketFlow.
"""

import pandas as pd

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

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