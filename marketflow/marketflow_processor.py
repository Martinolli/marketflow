"""
Marketflow Data Processor Module

This module provides data processing and feature calculation for the Marketflow algorithm.
"""

import pandas as pd
import numpy as np
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config


class DataProcessor:
    """Process raw price and volume data for Marketflow analysis"""
    
    def __init__(self, parameters=None):

        # Initialize Logger
        self.logger = get_logger(module_name="MarketflowDataProcessor")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        # Load parameters or use default MarketFlowDataParameters
        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()

        # Load thresholds from parameters
        self.volume_thresholds = self.parameters.get_volume_thresholds()
        if self.volume_thresholds is None:
            self.logger.warning("Volume thresholds not found in parameters, using default values.")

        # Load candle thresholds from parameters
        self.candle_thresholds = self.parameters.get_candle_thresholds()
        if self.candle_thresholds is None:
            self.logger.warning("Candle thresholds not found in parameters, using default values.")
    
    def preprocess_data(self, price_data, volume_data, lookback_period=None):
        """
        Preprocess price and volume data for Marketflow analysis
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        - lookback_period: Optional override for lookback period
        
        Returns:
        - Dictionary with processed data
        """
        self.logger.info("Preprocessing data...")

        # Use Parameters lookback period if not specified
        if lookback_period is None:
            self.logger.info("Using default lookback period from parameters.")
            lookback_period = self.volume_thresholds.get("lookback_period", 50)
        
        # Align and ensure datetime index
        price_data = price_data.copy()
        self.logger.info("Aligning price data...")
        volume_data = volume_data.copy()
        self.logger.info("Aligning volume data...")
        if price_data is not None and not price_data.empty:
            self.logger.info("Aligning price and volume data...")
        
        # Align both datasets (important if there's any mismatch in timestamps)
        price_data, volume_data = price_data.align(volume_data, join='inner', axis=0)
        self.logger.info("Data alignment complete.")

        # Create dictionary to hold all calculated data
        processed_data = {
            "price": price_data,
            "volume": volume_data
        }
        if volume_data is not None and not volume_data.empty:
            self.logger.info("Volume data is available for processing.")
        else:
            self.logger.warning("Volume data is empty or not available, proceeding with price data only.")

        # Calculate candle properties
        processed_data = self.calculate_candle_properties(processed_data)        
        self.logger.info("Candle properties calculated.")
        
        # Calculate volume metrics
        processed_data = self.calculate_volume_metrics(processed_data, lookback_period)
        self.logger.info("Volume metrics calculated.")
        
        # Classify candles and volume
        processed_data["volume_class"] = self.classify_volume(processed_data["volume_ratio"])
        processed_data["candle_class"] = self.classify_candles(processed_data)
        self.logger.info("Candle classifications calculated.")
        
        # Calculate trend metrics
        processed_data["price_direction"] = self.calculate_price_direction(price_data, lookback_period, threshold_pct=5)
        processed_data["volume_direction"] = self.calculate_volume_direction(price_data, volume_data, lookback_period)

        self.logger.info("Data preprocessing complete.")
        return processed_data
    
    def calculate_candle_properties(self, processed_data):
        """
        Calculate candle properties
        
        Parameters:
        - processed_data: Dictionary with price and volume data
        
        Returns:
        - Updated processed_data dictionary with candle properties
        """
        try:
            self.logger.info("Calculating candle properties...")
            price_data = processed_data["price"]
            
            # Calculate spread (body size)
            processed_data["spread"] = abs(price_data["close"] - price_data["open"])
            
            # Calculate body percentage of total range
            processed_data["body_percent"] = processed_data["spread"] / (price_data["high"] - price_data["low"])
            
            # Calculate upper and lower wicks
            processed_data["upper_wick"] = price_data["high"] - price_data[["open", "close"]].max(axis=1)
            processed_data["lower_wick"] = price_data[["open", "close"]].min(axis=1) - price_data["low"]
            
            self.logger.info("Candle properties calculation complete.")
            return processed_data
        except Exception as e:
            self.logger.error(f"Error calculating candle properties: {e}")
            raise
    def calculate_volume_metrics(self, processed_data, lookback_period):
        """
        Calculate volume metrics
        
        Parameters:
        - processed_data: Dictionary with price and volume data
        - lookback_period: Number of periods to look back for average volume
        
        Returns:
        - Updated processed_data dictionary with volume metrics
        """
        try:
            self.logger.info("Calculating volume metrics...")
            volume_data = processed_data["volume"]
            
            # Calculate average volume
            processed_data["avg_volume"] = volume_data.rolling(window=lookback_period).mean()
            
            # Calculate volume ratio
            processed_data["volume_ratio"] = volume_data / processed_data["avg_volume"]
            
            self.logger.info("Volume metrics calculation complete.")
            return processed_data
        except Exception as e:
            self.logger.error(f"Error calculating volume metrics: {e}")
            raise
    
    def classify_volume(self, volume_ratio):
        """
        Classify volume as VERY_HIGH, HIGH, AVERAGE, LOW, or VERY_LOW
        based on volume ratio.

        Parameters:
        - volume_ratio: Series with volume ratio values

        Returns:
        - Series with volume classifications
        """
        try:
            self.logger.info("Classifying volume levels...")
            # Ensure the index is clean and flat
            volume_ratio = volume_ratio.copy()
            volume_ratio.index = pd.to_datetime(volume_ratio.index)

            # Get thresholds from Parameters
            very_high_threshold = self.volume_thresholds.get("very_high_threshold", 2.0)
            high_threshold = self.volume_thresholds.get("high_threshold", 1.3)
            low_threshold = self.volume_thresholds.get("low_threshold", 0.6)
            very_low_threshold = self.volume_thresholds.get("very_low_threshold", 0.3)

            conditions = [
                volume_ratio >= very_high_threshold,
                volume_ratio >= high_threshold,
                volume_ratio <= very_low_threshold,
                volume_ratio <= low_threshold
            ]
            choices = ["VERY_HIGH", "HIGH", "VERY_LOW", "LOW"]

            volume_class = pd.Series(np.select(conditions, choices, default="AVERAGE"), index=volume_ratio.index)

            self.logger.info("Volume classification complete.")
            return volume_class
        except Exception as e:
            self.logger.error(f"Error classifying volume: {e}")
            raise

    def classify_candles(self, data):
        """
        Classify candles based on spread and wicks
        
        Parameters:
        - data: Dictionary with processed data
        
        Returns:
        - Series with candle classifications
        """
        try:
            self.logger.info("Classifying candles...")
            # Get thresholds from Parameters
            wide_threshold = self.candle_thresholds.get("wide_threshold", 1.3)
            narrow_threshold = self.candle_thresholds.get("narrow_threshold", 0.6)
            wick_threshold = self.candle_thresholds.get("wick_threshold", 1.5)
            
            # Calculate average spread for relative comparison
            avg_spread = data["spread"].rolling(window=20).mean()
            spread_ratio = data["spread"] / avg_spread
            
            conditions = [
                spread_ratio >= wide_threshold,
                spread_ratio <= narrow_threshold,
                (data["upper_wick"] > data["spread"] * wick_threshold) | (data["lower_wick"] > data["spread"] * wick_threshold)
            ]

            choices = ["WIDE", "NARROW", "WICK"]

            candle_class = pd.Series(np.select(conditions, choices, default="NEUTRAL"), index=data["price"].index)

            self.logger.info("Candle classification complete.")
            return candle_class
        except Exception as e:
            self.logger.error(f"Error classifying candles: {e}")
            raise

    def calculate_atr(self, price_data, period=14):
        """
        Calculate Average True Range (ATR)
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - period: Number of periods to consider
        
        Returns:
        - Series with ATR values
        """
        # Calculate true range (TR)
        high = price_data["high"]
        low = price_data["low"]
        close = price_data["close"]
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr

    def calculate_price_direction(self, price_data, lookback_period=10, threshold_pct=5, use_ema=False, strength_levels=False):
        """
        Calculate the direction of price movement
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - lookback_period: Number of periods to consider
        - threshold_pct: Percentage threshold for price movement classification
        - use_ema: Boolean to use EMA instead of simple moving average
        - strength_levels: Boolean to include strength levels in the output
        
        Returns:
        - Series with price direction classifications
        """
        try:
            self.logger.info("Calculating price direction...")
            # Calculate short-term price direction
            if use_ema:
                price_change = price_data["close"] - price_data["close"].ewm(span=lookback_period).mean()
            else:
                price_change = price_data["close"].diff(lookback_period)
            
            # Calculate the threshold based on average true range (ATR)
            atr = self.calculate_atr(price_data, lookback_period)
            smoothed_atr = atr.rolling(window=lookback_period).mean()  # Smoothed ATR
            threshold = smoothed_atr * (threshold_pct / 100)

            # Classify direction based on price change and threshold
            direction = pd.Series(index=price_data.index, data="SIDEWAYS")
            direction[price_change > threshold] = "UP"
            direction[price_change < -threshold] = "DOWN"
            
            # Add strength levels if requested
            if strength_levels:
                strength = abs(price_change) / threshold
                direction = direction + "_" + pd.cut(strength, bins=[0, 1, 2, float('inf')], labels=['WEAK', 'MODERATE', 'STRONG'])
            
            # Handle NaN values
            direction = direction.fillna("UNKNOWN")
            self.logger.info("Price direction calculation complete.")
            return direction
        except Exception as e:
            self.logger.error(f"Error calculating price direction: {e}")
            raise
    
    def calculate_obv(self, price_data, volume_data):
        """
        Calculate On Balance Volume (OBV)
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        
        Returns:
        - Series with OBV values
        """
        close = price_data['close']
        obv = pd.Series(index=close.index, dtype=float)
        obv.iloc[0] = volume_data.iloc[0]
        
        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] + volume_data.iloc[i]
            elif close.iloc[i] < close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] - volume_data.iloc[i]
            else:
                obv.iloc[i] = obv.iloc[i-1]
        
        return obv

    def calculate_volume_direction(self, price_data, volume_data, lookback_period=10, threshold_pct=10):
        """
        Calculate the direction of volume movement using On Balance Volume (OBV)
        
        Parameters:
        - price_data: DataFrame with OHLC data
        - volume_data: Series with volume data
        - lookback_period: Number of periods to consider
        - threshold_pct: Percentage threshold for volume movement classification
        
        Returns:
        - Series with volume direction classifications
        """
        # Calculate On Balance Volume (OBV)
        obv = self.calculate_obv(price_data, volume_data)
        
        # Calculate OBV change
        obv_change = obv.diff(lookback_period)
        
        # Calculate the threshold based on average OBV
        avg_obv = obv.rolling(window=lookback_period).mean()
        threshold = avg_obv * (threshold_pct / 100)

        # Classify direction based on OBV change and threshold
        direction = pd.Series(index=obv.index, data="FLAT")
        direction[obv_change > threshold] = "INCREASING"
        direction[obv_change < -threshold] = "DECREASING"
        
        # Handle NaN values
        direction = direction.fillna("UNKNOWN")
        
        return direction