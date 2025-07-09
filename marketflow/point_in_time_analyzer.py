"""
Point-in-Time Analyzer Module

Analyzes MarketFlow signals at a specific point in time.
"""

import pandas as pd

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.candle_analyzer import CandleAnalyzer
from marketflow.trend_analyzer import TrendAnalyzer
from marketflow.pattern_recognizer import PatternRecognizer
from marketflow.support_resistance_analyzer import SupportResistanceAnalyzer

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