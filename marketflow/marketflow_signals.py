"""
Marketflow Signals Module

This module provides signal generation and risk assessment for the Marketflow algorithm.
"""
# Import necessary modules

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

# Import necessary libraries
from enum import Enum, auto

class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NO_ACTION = "NO_ACTION"

class SignalStrength(Enum):
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    NEUTRAL = "NEUTRAL"


class SignalGenerator:
    """Generate trading signals based on VPA analysis"""
    
    def __init__(self, data_parameters=None):

        # Initialize configuration and parameters

        # Initialize logger
        self.logger = get_logger(module_name="MarketflowSignals")

         # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        self.data_parameters = data_parameters or MarketFlowDataParameters()
        self.signal_params = data_parameters.get_signal_parameters()
        self.account_params = data_parameters.get_account_parameters()
        
            
    def generate_signals(self, timeframe_analyses: dict, confirmations: dict) ->dict[str, SignalType | SignalStrength | str]:
        """
        Generate trading signals based on VPA analysis across timeframes
        
        Parameters:
        - timeframe_analyses: Dictionary with analysis results for each timeframe
        - confirmations: Dictionary with confirmation analysis across timeframes
        
        Returns:
        - Dictionary with signal information
        """

        if not timeframe_analyses or not isinstance(timeframe_analyses, dict):
            self.logger.error("Invalid input for timeframe_analyses.")
            return {"type": "NO_ACTION", "strength": "NEUTRAL", "details": "Invalid input."}
    
        self.logger.info("Generating signals...")
        # Check for strong signals
        strong_buy = self.is_strong_buy_signal(timeframe_analyses, confirmations)
        self.logger.info(f"Strong buy signal: {strong_buy}")
        strong_sell = self.is_strong_sell_signal(timeframe_analyses, confirmations)
        self.logger.info(f"Strong sell signal: {strong_sell}")
        
        # Check for moderate signals
        moderate_buy = self.is_moderate_buy_signal(timeframe_analyses, confirmations)
        self.logger.info(f"Moderate buy signal: {moderate_buy}")
        moderate_sell = self.is_moderate_sell_signal(timeframe_analyses, confirmations)
        self.logger.info(f"Moderate sell signal: {moderate_sell}")
        
        # Generate signal
        if strong_buy:
            signal = {
                "type": SignalType.BUY,
                "strength": SignalStrength.STRONG,
                "details": "Strong buy signal confirmed across multiple timeframes"
            }
        elif strong_sell:
            signal = {
                "type": SignalType.SELL,
                "strength": SignalStrength.STRONG,
                "details": "Strong sell signal confirmed across multiple timeframes"
            }
        elif moderate_buy:
            signal = {
                "type": SignalType.BUY,
                "strength": SignalStrength.MODERATE,
                "details": "Moderate buy signal with some timeframe confirmation"
            }
        elif moderate_sell:
            signal = {
                "type": SignalType.SELL,
                "strength": SignalStrength.MODERATE,
                "details": "Moderate sell signal with some timeframe confirmation"
            }
        else:
            signal = {
                "type": SignalType.NO_ACTION,
                "strength": SignalStrength.NEUTRAL,
                "details": "No clear signal detected"
            }
        self.logger.info(f"Generated signal: {signal}")
        
        # Add supporting evidence
        signal["evidence"] = self.gather_signal_evidence(timeframe_analyses, confirmations, signal["type"])
        
        return signal
    
    def is_strong_buy_signal(self, timeframe_analyses: dict, confirmations: dict) -> bool:
        """
        Check if a strong buy signal is present
        
        Parameters:
        - timeframe_analyses: Dictionary with analysis results for each timeframe
        - confirmations: Dictionary with confirmation analysis across timeframes
        
        Returns:
        - Boolean indicating if a strong buy signal is present
        """

        if not timeframe_analyses or not isinstance(timeframe_analyses, dict):
            self.logger.error("Invalid input for timeframe_analyses.")
            return False
        
        # Get parameters from config
        bullish_confirmation_threshold = self.signal_params.get("bullish_confirmation_threshold", 1)
        self.logger.debug(f"Checking for strong buy signal with confirmation threshold: {bullish_confirmation_threshold}")
        
        # Check for bullish patterns
        bullish_patterns = 0
        for tf in timeframe_analyses:
            self.logger.debug(f"Checking for bullish patterns in {tf}")
            patterns = timeframe_analyses[tf]["pattern_analysis"]
            
            # Check for accumulation
            if patterns["accumulation"]["detected"]:
                self.logger.debug("Detected accumulation pattern")
                bullish_patterns += 1
            
            # Check for selling climax
            if patterns["selling_climax"]["detected"]:
                self.logger.debug("Detected selling climax pattern")
                bullish_patterns += 1
            
            # Check for support tests
            if patterns["testing"]["detected"]:
                self.logger.debug("Detected testing pattern")
                for test in patterns["testing"]["tests"]:
                    if test["type"] == "SUPPORT_TEST":
                        bullish_patterns += 1
        
        # Check for bullish candle signals in the primary timeframe
        primary_tf = list(timeframe_analyses.keys())[0]  # Assuming first timeframe is primary
        self.logger.info(f"Checking for bullish candle signals in {primary_tf}")
        candle_analysis = timeframe_analyses[primary_tf]["candle_analysis"]
        trend_analysis = timeframe_analyses[primary_tf]["trend_analysis"]
        
        bullish_candle = candle_analysis["signal_strength"] == "BULLISH"
        bullish_trend = trend_analysis["signal_strength"] == "BULLISH"
        self.logger.debug(f"Strong buy: confirmations={len(confirmations['bullish'])}, patterns={bullish_patterns}, candle={bullish_candle}, trend={bullish_trend}")
        
        # Determine if strong buy signal is present
        return (len(confirmations["bullish"]) >= bullish_confirmation_threshold and 
                bullish_patterns >= 1 and 
                (bullish_candle or bullish_trend))
    
    def is_strong_sell_signal(self, timeframe_analyses: dict, confirmations: dict) -> bool:
        """
        Check if a strong sell signal is present
        
        Parameters:
        - timeframe_analyses: Dictionary with analysis results for each timeframe
        - confirmations: Dictionary with confirmation analysis across timeframes
        
        Returns:
        - Boolean indicating if a strong sell signal is present
        """

        if not timeframe_analyses or not isinstance(timeframe_analyses, dict):
            self.logger.error("Invalid input for timeframe_analyses.")
            return False
    
        # Get parameters from config
        bearish_confirmation_threshold = self.signal_params.get("bearish_confirmation_threshold", 1)
        self.logger.debug(f"Checking for strong sell signal with confirmation threshold: {bearish_confirmation_threshold}")
        
        # Check for bearish patterns
        bearish_patterns = 0
        for tf in timeframe_analyses:
            self.logger.debug(f"Checking for bearish patterns in {tf}")
            patterns = timeframe_analyses[tf]["pattern_analysis"]
            
            # Check for distribution
            if patterns["distribution"]["detected"]:
                self.logger.debug("Detected distribution pattern")
                bearish_patterns += 1
            
            # Check for buying climax
            if patterns["buying_climax"]["detected"]:
                self.logger.debug("Detected buying climax pattern")
                bearish_patterns += 1
            
            # Check for resistance tests
            if patterns["testing"]["detected"]:
                self.logger.debug("Detected testing pattern")
                for test in patterns["testing"]["tests"]:
                    if test["type"] == "RESISTANCE_TEST":
                        bearish_patterns += 1
        
        # Check for bearish candle signals in the primary timeframe
        primary_tf = list(timeframe_analyses.keys())[0]  # Assuming first timeframe is primary
        self.logger.info(f"Checking for bearish candle signals in {primary_tf}")
        candle_analysis = timeframe_analyses[primary_tf]["candle_analysis"]
        trend_analysis = timeframe_analyses[primary_tf]["trend_analysis"]
        
        bearish_candle = candle_analysis["signal_strength"] == "BEARISH"
        bearish_trend = trend_analysis["signal_strength"] == "BEARISH"
        self.logger.debug(f"Strong sell: confirmations={len(confirmations['bearish'])}, patterns={bearish_patterns}, candle={bearish_candle}, trend={bearish_trend}")
        
        
        # Determine if strong sell signal is present
        return (len(confirmations["bearish"]) >= bearish_confirmation_threshold and 
                bearish_patterns >= 1 and 
                (bearish_candle or bearish_trend))
    
    def is_moderate_buy_signal(self, timeframe_analyses: dict, confirmations: dict) -> bool:
        """
        Check if a moderate buy signal is present

        Parameters:
        - timeframe_analyses: Dictionary with analysis results for each timeframe
        - confirmations: Dictionary with confirmation analysis across timeframes

        Returns:
        - Boolean indicating if a moderate buy signal is present
        """
        self.logger.debug("Checking for moderate buy signal...")
        # Check for bullish signals in at least one timeframe
        bullish_candles = 0
        bullish_trends = 0

        for tf in timeframe_analyses:
            candle_analysis = timeframe_analyses[tf]["candle_analysis"]
            trend_analysis = timeframe_analyses[tf]["trend_analysis"]

            if candle_analysis["signal_strength"] == "BULLISH":
                bullish_candles += 1
                self.logger.debug(f"Bullish candle detected in {tf}")
            if trend_analysis["signal_strength"] == "BULLISH":
                bullish_trends += 1
                self.logger.debug(f"Bullish trend detected in {tf}")

        # Get parameters from config
        bullish_candles_threshold = self.signal_params.get("bullish_candles_threshold", 2)
        moderate_bullish_confirmation_threshold = self.signal_params.get("moderate_bullish_confirmation_threshold", 1)
        self.logger.debug(f"Bullish candles threshold: {bullish_candles_threshold}, Moderate bullish confirmation threshold: {moderate_bullish_confirmation_threshold}")

        # Check for bullish patterns
        bullish_patterns = 0
        for tf in timeframe_analyses:
            patterns = timeframe_analyses[tf]["pattern_analysis"]

            # Check for accumulation
            if patterns["accumulation"]["detected"]:
                bullish_patterns += 1
                self.logger.debug(f"Accumulation pattern detected in {tf}")
            # Check for selling climax
            if patterns["selling_climax"]["detected"]:
                bullish_patterns += 1
                self.logger.debug(f"Selling climax pattern detected in {tf}")

        # Check for bullish confirmations
        bullish_confirmations = len(confirmations["bullish"])
        self.logger.debug(f"Bullish candles: {bullish_candles}, Bullish trends: {bullish_trends}, Bullish patterns: {bullish_patterns}, Bullish confirmations: {bullish_confirmations}")

        # Determine if moderate buy signal is present
        result = ((bullish_candles >= bullish_candles_threshold or 
                 bullish_trends >= 1 or 
                 bullish_patterns >= 1) and
                bullish_confirmations >= moderate_bullish_confirmation_threshold)
        self.logger.debug(f"Moderate buy signal result: {result}")
        return result
    
    def is_moderate_sell_signal(self, timeframe_analyses: dict, confirmations: dict) -> bool:
        """
        Check if a moderate sell signal is present
        
        Parameters:
        - timeframe_analyses: Dictionary with analysis results for each timeframe
        - confirmations: Dictionary with confirmation analysis across timeframes
        
        Returns:
        - Boolean indicating if a moderate sell signal is present
        """
        self.logger.debug("Checking for moderate sell signal...")
        # Check for bearish signals in at least one timeframe
        bearish_candles = 0
        bearish_trends = 0
        
        for tf in timeframe_analyses:
            candle_analysis = timeframe_analyses[tf]["candle_analysis"]
            trend_analysis = timeframe_analyses[tf]["trend_analysis"]
            
            if candle_analysis["signal_strength"] == "BEARISH":
                bearish_candles += 1
                self.logger.debug(f"Bearish candle detected in {tf}")
            
            if trend_analysis["signal_strength"] == "BEARISH":
                bearish_trends += 1
                self.logger.debug(f"Bearish trend detected in {tf}")
        
        # Get parameters from config
        bearish_candles_threshold = self.signal_params.get("bearish_candles_threshold", 2)
        moderate_bearish_confirmation_threshold = self.signal_params.get("moderate_bearish_confirmation_threshold", 1)
        self.logger.debug(f"Bearish candles threshold: {bearish_candles_threshold}, Moderate bearish confirmation threshold: {moderate_bearish_confirmation_threshold}")

        # Check for bearish patterns
        bearish_patterns = 0
        for tf in timeframe_analyses:
            patterns = timeframe_analyses[tf]["pattern_analysis"]
            
            # Check for distribution
            if patterns["distribution"]["detected"]:
                bearish_patterns += 1
                self.logger.debug(f"Distribution pattern detected in {tf}")
            
            # Check for buying climax
            if patterns["buying_climax"]["detected"]:
                bearish_patterns += 1
                self.logger.debug(f"Buying climax pattern detected in {tf}")
        
        # Check for bearish confirmations
        bearish_confirmations = len(confirmations["bearish"])
        self.logger.debug(f"Bearish candles: {bearish_candles}, Bearish trends: {bearish_trends}, Bearish patterns: {bearish_patterns}, Bearish confirmations: {bearish_confirmations}")

        # Determine if moderate sell signal is present
        result = ((bearish_candles >= bearish_candles_threshold or 
                bearish_trends >= 1 or 
                bearish_patterns >= 1) and
                bearish_confirmations >= moderate_bearish_confirmation_threshold)
        self.logger.debug(f"Moderate sell signal result: {result}")
        return result
    def gather_signal_evidence(self, timeframe_analyses: dict, confirmations: dict, signal_type: str) -> dict:
        """
        Gather evidence supporting the signal
        
        Parameters:
        - timeframe_analyses: Dictionary with analysis results for each timeframe
        - confirmations: Dictionary with confirmation analysis across timeframes
        - signal_type: Type of signal (BUY, SELL, NO_ACTION)
        
        Returns:
        - Dictionary with supporting evidence
        """
        self.logger.debug(f"Gathering signal evidence for signal_type: {signal_type}")
        evidence = {
            "candle_signals": [],
            "trend_signals": [],
            "pattern_signals": [],
            "timeframe_confirmations": []
        }
        
        # Gather evidence based on signal type
        if signal_type == "BUY":
            # Add bullish candle signals
            for tf in timeframe_analyses:
                candle_analysis = timeframe_analyses[tf]["candle_analysis"]
                if candle_analysis["signal_strength"] == "BULLISH":
                    self.logger.debug(f"Bullish candle detected in {tf}: {candle_analysis['details']}")
                    evidence["candle_signals"].append({
                        "timeframe": tf,
                        "details": candle_analysis["details"]
                    })
            
            # Add bullish trend signals
            for tf in timeframe_analyses:
                trend_analysis = timeframe_analyses[tf]["trend_analysis"]
                if trend_analysis["signal_strength"] == "BULLISH":
                    self.logger.debug(f"Bullish trend detected in {tf}: {trend_analysis['details']}")
                    evidence["trend_signals"].append({
                        "timeframe": tf,
                        "details": trend_analysis["details"]
                    })
            
            # Add bullish pattern signals
            for tf in timeframe_analyses:
                patterns = timeframe_analyses[tf]["pattern_analysis"]
                
                if patterns["accumulation"]["detected"]:
                    self.logger.debug(f"Accumulation pattern detected in {tf}: {patterns['accumulation']['details']}")
                    evidence["pattern_signals"].append({
                        "timeframe": tf,
                        "pattern": "Accumulation",
                        "details": patterns["accumulation"]["details"]
                    })
                
                if patterns["selling_climax"]["detected"]:
                    self.logger.debug(f"Selling climax pattern detected in {tf}: {patterns['selling_climax']['details']}")
                    evidence["pattern_signals"].append({
                        "timeframe": tf,
                        "pattern": "Selling Climax",
                        "details": patterns["selling_climax"]["details"]
                    })
            
            # Add timeframe confirmations
            self.logger.debug(f"Bullish timeframe confirmations: {confirmations['bullish']}")
            evidence["timeframe_confirmations"] = confirmations["bullish"]
        
        elif signal_type == "SELL":
            # Add bearish candle signals
            for tf in timeframe_analyses:
                candle_analysis = timeframe_analyses[tf]["candle_analysis"]
                if candle_analysis["signal_strength"] == "BEARISH":
                    self.logger.debug(f"Bearish candle detected in {tf}: {candle_analysis['details']}")
                    evidence["candle_signals"].append({
                        "timeframe": tf,
                        "details": candle_analysis["details"]
                    })
            
            # Add bearish trend signals
            for tf in timeframe_analyses:
                trend_analysis = timeframe_analyses[tf]["trend_analysis"]
                if trend_analysis["signal_strength"] == "BEARISH":
                    self.logger.debug(f"Bearish trend detected in {tf}: {trend_analysis['details']}")
                    evidence["trend_signals"].append({
                        "timeframe": tf,
                        "details": trend_analysis["details"]
                    })
            
            # Add bearish pattern signals
            for tf in timeframe_analyses:
                patterns = timeframe_analyses[tf]["pattern_analysis"]
                
                if patterns["distribution"]["detected"]:
                    self.logger.debug(f"Distribution pattern detected in {tf}: {patterns['distribution']['details']}")
                    evidence["pattern_signals"].append({
                        "timeframe": tf,
                        "pattern": "Distribution",
                        "details": patterns["distribution"]["details"]
                    })
                
                if patterns["buying_climax"]["detected"]:
                    self.logger.debug(f"Buying climax pattern detected in {tf}: {patterns['buying_climax']['details']}")
                    evidence["pattern_signals"].append({
                        "timeframe": tf,
                        "pattern": "Buying Climax",
                        "details": patterns["buying_climax"]["details"]
                    })
            
            # Add timeframe confirmations
            self.logger.debug(f"Bearish timeframe confirmations: {confirmations['bearish']}")
            evidence["timeframe_confirmations"] = confirmations["bearish"]
        
        self.logger.debug(f"Gathered evidence: {evidence}")
        return evidence

class RiskAssessor:
    """Assess risk for potential trades"""
    
    def __init__(self, data_parameters=None):

        # Initialize logger
        self.logger = get_logger(module_name="MarketflowRiskAssessor")

         # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        # Initialize configuration and parameters
        self.data_parameters = data_parameters or MarketFlowDataParameters()
        self.risk_params = data_parameters.get_risk_parameters()
        self.account_params = data_parameters.get_account_parameters()
        
    def assess_trade_risk(self, signal, current_price: float, support_resistance: dict) -> dict:
        """
        Assess risk for a potential trade
        
        Parameters:
        - signal: Dictionary with signal information
        - current_price: Current price of the asset
        - support_resistance: Dictionary with support and resistance levels
        
        Returns:
        - Dictionary with risk assessment
        """
        self.logger.debug(f"Assessing trade risk for signal: {signal}, current_price: {current_price}, support_resistance: {support_resistance}")

        # Calculate stop loss and take profit levels
        stop_loss = self.calculate_stop_loss(signal, current_price, support_resistance)
        self.logger.debug(f"Calculated stop_loss: {stop_loss}")

        take_profit = self.calculate_take_profit(signal, current_price, support_resistance)
        self.logger.debug(f"Calculated take_profit: {take_profit}")
        
        # Calculate risk-reward ratio
        if signal["type"] == SignalType.BUY:
            risk = current_price - stop_loss
            reward = take_profit - current_price
        else:  # SELL or NO_ACTION
            risk = stop_loss - current_price
            reward = current_price - take_profit

        self.logger.debug(f"Risk: {risk}, Reward: {reward}")

        risk_reward_ratio = reward / risk if risk > 0 else 0
        self.logger.debug(f"Risk-reward ratio: {risk_reward_ratio}")

        # Determine position size based on risk
        position_size = self.calculate_position_size(current_price, stop_loss)
        self.logger.debug(f"Calculated position_size: {position_size}")

        risk_per_share = abs(current_price - stop_loss)
        self.logger.debug(f"Risk per share: {risk_per_share}")

        return {
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward_ratio": risk_reward_ratio,
            "position_size": position_size,
            "risk_per_share": risk_per_share
        }
    
    def calculate_stop_loss(self, signal: dict, current_price: float, support_resistance: dict) -> float:
        """
        Calculate appropriate stop loss level
        
        Parameters:
        - signal: Dictionary with signal information
        - current_price: Current price of the asset
        - support_resistance: Dictionary with support and resistance levels
        
        Returns:
        - Stop loss price level
        """
        self.logger.debug(f"Calculating stop loss for signal: {signal}, current_price: {current_price}, support_resistance: {support_resistance}")

        # Get parameters from config
        default_stop_loss_percent = self.risk_params.get("default_stop_loss_percent", 0.02)
        support_resistance_buffer = self.risk_params.get("support_resistance_buffer", 0.005)
        self.logger.debug(f"default_stop_loss_percent: {default_stop_loss_percent}, support_resistance_buffer: {support_resistance_buffer}")
        
        if signal["type"] == SignalType.BUY:
            # For buy signals, place stop loss below recent support
            support_levels = support_resistance["support"]
            self.logger.debug(f"Support levels: {support_levels}")
            
            if support_levels:
                # Find closest support level below current price
                valid_supports = [level for level in support_levels if level["price"] < current_price]
                self.logger.debug(f"Valid supports below current price: {valid_supports}")
                
                if valid_supports:
                    # Sort by price (descending) to get closest support below current price
                    valid_supports.sort(key=lambda x: x["price"], reverse=True)
                    stop_level = valid_supports[0]["price"]
                    self.logger.debug(f"Closest support below current price: {stop_level}")
                    
                    # Add buffer below support
                    stop_loss = stop_level * (1 - support_resistance_buffer)
                    self.logger.debug(f"Stop loss set below support with buffer: {stop_loss}")
                else:
                    # No valid support found, use default percentage
                    stop_loss = current_price * (1 - default_stop_loss_percent)
                    self.logger.debug(f"No valid support found, stop loss set by default percent: {stop_loss}")
            else:
                # No support levels found, use default percentage
                stop_loss = current_price * (1 - default_stop_loss_percent)
                self.logger.debug(f"No support levels found, stop loss set by default percent: {stop_loss}")
        
        elif signal["type"] == SignalType.SELL:
            # For sell signals, place stop loss above recent resistance
            resistance_levels = support_resistance["resistance"]
            self.logger.debug(f"Resistance levels: {resistance_levels}")
            
            if resistance_levels:
                # Find closest resistance level above current price
                valid_resistances = [level for level in resistance_levels if level["price"] > current_price]
                self.logger.debug(f"Valid resistances above current price: {valid_resistances}")
                
                if valid_resistances:
                    # Sort by price (ascending) to get closest resistance above current price
                    valid_resistances.sort(key=lambda x: x["price"])
                    stop_level = valid_resistances[0]["price"]
                    self.logger.debug(f"Closest resistance above current price: {stop_level}")
                    
                    # Add buffer above resistance
                    stop_loss = stop_level * (1 + support_resistance_buffer)
                    self.logger.debug(f"Stop loss set above resistance with buffer: {stop_loss}")
                else:
                    # No valid resistance found, use default percentage
                    stop_loss = current_price * (1 + default_stop_loss_percent)
                    self.logger.debug(f"No valid resistance found, stop loss set by default percent: {stop_loss}")
            else:
                # No resistance levels found, use default percentage
                stop_loss = current_price * (1 + default_stop_loss_percent)
                self.logger.debug(f"No resistance levels found, stop loss set by default percent: {stop_loss}")
        
        else:  # NO_ACTION
            # For no action signals, use default percentage
            stop_loss = current_price * (1 - default_stop_loss_percent)
            self.logger.debug(f"NO_ACTION signal, stop loss set by default percent: {stop_loss}")
        
        return stop_loss
    
    def calculate_take_profit(self, signal: dict, current_price: float, support_resistance: dict) -> float:
        """
        Calculate appropriate take profit level
        
        Parameters:
        - signal: Dictionary with signal information
        - current_price: Current price of the asset
        - support_resistance: Dictionary with support and resistance levels
        
        Returns:
        - Take profit price level
        """
        self.logger.debug(f"Calculating take profit for signal: {signal}, current_price: {current_price}, support_resistance: {support_resistance}")

        # Get parameters from config
        default_take_profit_percent = self.risk_params.get("default_take_profit_percent", 0.05)
        support_resistance_buffer = self.risk_params.get("support_resistance_buffer", 0.005)
        self.logger.debug(f"default_take_profit_percent: {default_take_profit_percent}, support_resistance_buffer: {support_resistance_buffer}")
        
        if signal["type"] == SignalType.BUY:
            # For buy signals, place take profit at or above recent resistance
            resistance_levels = support_resistance["resistance"]
            self.logger.debug(f"Resistance levels: {resistance_levels}")
            
            if resistance_levels:
                # Find closest resistance level above current price
                valid_resistances = [level for level in resistance_levels if level["price"] > current_price]
                self.logger.debug(f"Valid resistances above current price: {valid_resistances}")
                
                if valid_resistances:
                    # Sort by price (ascending) to get closest resistance above current price
                    valid_resistances.sort(key=lambda x: x["price"])
                    target_level = valid_resistances[0]["price"]
                    self.logger.debug(f"Closest resistance above current price: {target_level}")
                    
                    # Add buffer above resistance
                    take_profit = target_level * (1 + support_resistance_buffer)
                    self.logger.debug(f"Take profit set above resistance with buffer: {take_profit}")
                else:
                    # No valid resistance found, use default percentage
                    take_profit = current_price * (1 + default_take_profit_percent)
                    self.logger.debug(f"No valid resistance found, take profit set by default percent: {take_profit}")
            else:
                # No resistance levels found, use default percentage
                take_profit = current_price * (1 + default_take_profit_percent)
                self.logger.debug(f"No resistance levels found, take profit set by default percent: {take_profit}")
        
        elif signal["type"] == SignalType.SELL:
            # For sell signals, place take profit at or below recent support
            support_levels = support_resistance["support"]
            self.logger.debug(f"Support levels: {support_levels}")
            
            if support_levels:
                # Find closest support level below current price
                valid_supports = [level for level in support_levels if level["price"] < current_price]
                self.logger.debug(f"Valid supports below current price: {valid_supports}")
                
                if valid_supports:
                    # Sort by price (descending) to get closest support below current price
                    valid_supports.sort(key=lambda x: x["price"], reverse=True)
                    target_level = valid_supports[0]["price"]
                    self.logger.debug(f"Closest support below current price: {target_level}")
                    
                    # Add buffer below support
                    take_profit = target_level * (1 - support_resistance_buffer)
                    self.logger.debug(f"Take profit set below support with buffer: {take_profit}")
                else:
                    # No valid support found, use default percentage
                    take_profit = current_price * (1 - default_take_profit_percent)
                    self.logger.debug(f"No valid support found, take profit set by default percent: {take_profit}")
            else:
                # No support levels found, use default percentage
                take_profit = current_price * (1 - default_take_profit_percent)
                self.logger.debug(f"No support levels found, take profit set by default percent: {take_profit}")
        
        else:  # NO_ACTION
            # For no action signals, use default percentage
            take_profit = current_price * (1 + default_take_profit_percent)
            self.logger.debug(f"NO_ACTION signal, take profit set by default percent: {take_profit}")
        
        return take_profit
    
    def calculate_position_size(self, current_price: float, stop_loss: float) -> float:
        """
        Calculate appropriate position size based on risk
        
        Parameters:
        - current_price: Current price of the asset
        - stop_loss: Stop loss price level
        - risk_per_trade: Percentage of account to risk per trade (default: 1%)
        - account_size: Total account size (default: $10,000)
        
        Returns:
        - Position size (number of shares)
        """
        # Initialize risk per trade and account size
        risk_per_trade = self.account_params.get("risk_per_trade")
        account_size = self.account_params.get("account_size")

        # Calculate dollar risk per trade
        dollar_risk = account_size * risk_per_trade
        
        # Calculate risk per share
        risk_per_share = abs(current_price - stop_loss)
        
        # Calculate position size
        if risk_per_share > 0:
            position_size = dollar_risk / risk_per_share
        else:
            position_size = 0
        
        return position_size
