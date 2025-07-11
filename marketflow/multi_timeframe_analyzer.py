"""
Multi-Timeframe Analyzer Module

Manages analysis across multiple timeframes for MarketFlow.
"""

import pandas as pd

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.candle_analyzer import CandleAnalyzer
from marketflow.trend_analyzer import TrendAnalyzer
from marketflow.pattern_recognizer import PatternRecognizer
from marketflow.support_resistance_analyzer import SupportResistanceAnalyzer
from marketflow.marketflow_processor import DataProcessor

class MultiTimeframeAnalyzer:
    """Analyze data across multiple timeframes"""
    
    def __init__(self, parameters=None):

        # Initialize Logger
        self.logger = get_logger(module_name="MultiTimeframeAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        if parameters is None:
            self.logger.info("Using default MultiTimeframeAnalyzer parameters.")
        else:
            self.logger.info("Using provided MultiTimeframeAnalyzer parameters.")
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
