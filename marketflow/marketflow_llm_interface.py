"""
VPA LLM Interface Module

This module provides an intelligent, narrative-driven interface for LLMs 
to interact with the advanced VPA and Wyckoff analysis engine.
"""

import re
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_wyckoff import WyckoffEvent, WyckoffPhase
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

class MarketflowLLMInterface:
    """
    Intelligent interface for LLM integration with VPA and Wyckoff analysis.
    This class synthesizes raw analysis into a structured, narrative-driven format.
    """
    
    def __init__(self, parameters=None):
        """
        Initialize the VPA LLM interface.
        
        Parameters:
        - config: Optional VPAConfig instance.
        - logger: Optional VPALogger instance.
        """

        # Initialize logging
        self.logger = get_logger(module_name="MarketflowLLMInterface")

        # Initialize configuration manager
        self.config_manager = create_app_config()

        # Initialize configuration
        # Load parameters or use default MarketFlowDataParameters
        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")

        self.parameters = parameters or MarketFlowDataParameters()

        # Initialize the VPA facade with the provided configuration and logger
        self.logger.info("Initializing VPAFacade with the interface's configuration and logger.")
        if not isinstance(self.parameters, MarketFlowDataParameters):
            self.logger.error("Invalid configuration provided. Expected MarketFlowDataParameters instance.")
            raise ValueError("Invalid configuration provided. Expected MarketFlowDataParameters instance.")
        # Pass the interface instance itself, which has a .logger attribute, to the facade.
        self.marketflow = MarketflowFacade()

        # Load concept explanations for VPA and Wyckoff
        self.marketflow_concepts = self._load_vpa_concept_explanations()
        self.wyckoff_concepts = self._load_wyckoff_concept_explanations()

    def _load_vpa_concept_explanations(self):
        """Loads general VPA concepts, based on authors like Anna Coulling."""
        # This remains largely the same, but could be expanded or loaded from a YAML/JSON file.
        return {
            "vpa_overview": """
                Volume Price Analysis (VPA) is a trading methodology that analyzes the relationship 
                between price action and volume to reveal market sentiment and identify trading opportunities.
                
                VPA is based on the work of iconic traders like Charles Dow, Jesse Livermore, and Richard Wyckoff,
                and focuses on how volume confirms or contradicts price movements. The core principle is that
                volume precedes price, meaning significant volume changes often signal upcoming price movements.
                
                Key concepts in VPA include:
                1. Volume confirms price - When price and volume move in the same direction, it validates the move
                2. Volume contradicts price - When price and volume move in opposite directions, it signals potential reversal
                3. Effort vs. Result - Comparing the effort (volume) with the result (price movement)
            """,
            
            "accumulation": """
                Accumulation in VPA refers to a pattern where large operators or institutions are buying
                an asset while trying to keep the price relatively stable to avoid driving it up before
                they complete their buying.
                
                Key characteristics of accumulation:
                1. Sideways price movement with narrowing range
                2. High volume on down days but price doesn't fall much (absorption)
                3. Low volume on up days
                4. Tests of support that hold with decreasing volume
                
                Accumulation typically occurs after a downtrend and precedes an uptrend.
            """,
            
            "distribution": """
                Distribution in VPA refers to a pattern where large operators or institutions are selling
                an asset while trying to keep the price relatively stable to avoid driving it down before
                they complete their selling.
                
                Key characteristics of distribution:
                1. Sideways price movement with narrowing range
                2. High volume on up days but price doesn't rise much (supply)
                3. Low volume on down days
                4. Tests of resistance that fail with decreasing volume
                
                Distribution typically occurs after an uptrend and precedes a downtrend.
            """,
            
            "buying_climax": """
                A buying climax in VPA is a pattern that marks the end of an uptrend, characterized by:
                
                1. Extremely high volume (often the highest in the trend)
                2. Wide range up candle
                3. Price at or near the high of the trend
                4. Often followed by a reversal or significant pullback
                
                A buying climax represents the last surge of buying before smart money begins to distribute.
                It often shows exhaustion of buying pressure and is a bearish signal.
            """,
            
            "selling_climax": """
                A selling climax in VPA is a pattern that marks the end of a downtrend, characterized by:
                
                1. Extremely high volume (often the highest in the trend)
                2. Wide range down candle
                3. Price at or near the low of the trend
                4. Often followed by a reversal or significant bounce
                
                A selling climax represents the last surge of selling before smart money begins to accumulate.
                It often shows exhaustion of selling pressure and is a bullish signal.
            """,
            
            "testing": """
                Testing in VPA refers to price probes of support or resistance levels with specific
                volume characteristics that reveal the strength of these levels.
                
                Key characteristics of testing:
                1. Support test: Price moves below a previous low but with lower volume
                2. Resistance test: Price moves above a previous high but with lower volume
                
                The outcome of these tests provides valuable information:
                - If support holds on low volume, it's strong support
                - If resistance breaks on high volume, it's a valid breakout
                - If resistance fails on low volume, it's a false breakout
            """,
            
            "effort_vs_result": """
                Effort vs. Result is a core concept in VPA that compares the volume (effort)
                with the price movement (result).
                
                Key principles:
                1. High effort (volume) with small result (price movement) indicates potential reversal
                2. Low effort with large result indicates weakness in the move
                3. Equal effort and result indicates a healthy trend
                
                Examples:
                - High volume up day with small price gain: supply is meeting demand (bearish)
                - Low volume down day with large price drop: no support present (bearish)
                - High volume down day with small price drop: demand is meeting supply (bullish)
            """
        }

    def _load_wyckoff_concept_explanations(self):
        """
        Loads detailed Wyckoff event and phase explanations, based on the Wyckoff Methodology.
        This maps directly to the WyckoffEvent and WyckoffPhase enums for dynamic lookup.
        """
        self.logger.debug("Loading Wyckoff concept explanations.")
        return {
            # Accumulation Events
            WyckoffEvent.SC.value: "Selling Climax (SC): A climactic event with high volume and wide price spread that stops a downtrend. It signifies the entry of large interests absorbing selling pressure.",
            WyckoffEvent.AR.value: "Automatic Rally (AR): A sharp rally that follows the Selling Climax. It defines the upper boundary of the subsequent trading range.",
            WyckoffEvent.ST.value: "Secondary Test (ST): A revisit to the price area of the Selling Climax, but on lower volume and narrower spread, confirming that selling pressure is exhausted.",
            WyckoffEvent.SPRING.value: "Spring: A terminal shakeout where price breaks below the support of the trading range, only to quickly reverse and close back inside the range. It is designed to mislead sellers and catch stop-losses. This is a high-quality buying opportunity.",
            WyckoffEvent.SOS.value: "Sign of Strength (SOS): A strong upward move on increasing volume and spread, often breaking the resistance of the trading range (the 'Creek'). It shows buyers are in firm control.",
            WyckoffEvent.LPS.value: "Last Point of Support (LPS): A pullback to a support level (often the old resistance) after a Sign of Strength. The pullback should occur on low volume, offering a lower-risk entry point before the main uptrend.",
            WyckoffEvent.JAC.value: "Jump Across the Creek (JAC): A decisive version of the Sign of Strength, where price clearly and powerfully breaks out of the trading range resistance.",

            # Distribution Events
            WyckoffEvent.BC.value: "Buying Climax (BC): A climactic event with high volume that stops an uptrend, signaling that large interests are distributing (selling) shares to the public.",
            WyckoffEvent.AUTO_REACTION.value: "Automatic Reaction (AR): A sharp decline following the Buying Climax, which establishes the support boundary of the new trading range.",
            WyckoffEvent.UTAD.value: "Upthrust After Distribution (UTAD): A terminal shakeout in a distribution range. Price moves above the resistance, appears bullish, but then fails and turns down, trapping breakout buyers. This is a strong sign of weakness.",
            WyckoffEvent.SOW.value: "Sign of Weakness (SOW): A significant downward move, often on increased spread and volume, that breaks the support of the trading range (the 'Ice'). It shows sellers are in control.",
            WyckoffEvent.LPSY.value: "Last Point of Supply (LPSY): A weak rally attempt after a Sign of Weakness that fails at or near the old support level. It shows a lack of buying demand and is a high-quality shorting opportunity.",

            # Phases
            WyckoffPhase.A.value: "Phase A - Stopping Action: The phase where the previous trend is halted. For accumulation, it's marked by events like SC and AR. For distribution, by BC and AR.",
            WyckoffPhase.B.value: "Phase B - Building a Cause: The longest phase, where large operators build their positions (accumulating or distributing) within a defined trading range.",
            WyckoffPhase.C.value: "Phase C - Testing: The phase containing a decisive test of the remaining supply/demand, typically a Spring (in accumulation) or a UTAD (in distribution).",
            WyckoffPhase.D.value: "Phase D - Markup/Markdown: The phase where price moves out of the trading range, driven by the imbalance created in Phase B and tested in Phase C.",
            WyckoffPhase.E.value: "Phase E - Trend Continuation: The final phase where the new trend is clearly established and continues with market participation."
        }

    def process_query(self, query: str):
        """
        Processes a natural language query. (This can be simplified if using an LLM with function calling)
        """
        self.logger.info(f"Processing query: {query}")
        query_lower = query.lower()
        
        # 1. Check for Ticker Analysis Request
        ticker_keywords = ["analyze", "analysis", "signal", "trade", "vpa for", "wyckoff for"]
        if any(keyword in query_lower for keyword in ticker_keywords):
            potential_tickers = re.findall(r'\b[A-Z]{1,5}\b', query)
            if potential_tickers:
                self.logger.info(f"Detected ticker analysis request for: {potential_tickers[0]}")
                return self.get_ticker_analysis(potential_tickers[0])
        
        # 2. Check for Concept Explanation Request
        for concept, explanation in {**self.marketflow_concepts, **self.wyckoff_concepts}.items():
            # Create search terms from the concept key (e.g., "Selling Climax")
            search_terms = concept.lower().split()
            if all(term in query_lower for term in search_terms):
                self.logger.info(f"Detected concept explanation request for: {concept}")
                return self.explain_concept(concept)

        # 3. Default response
        self.logger.info("No matching query type found. Returning default response.")
        return "I can help with VPA and Wyckoff analysis. Ask me to 'Analyze AAPL' or 'What is a Wyckoff Spring?'"


    def explain_concept(self, concept_name: str):
        """Explains a MarketFlow or Wyckoff concept dynamically, with logging."""
        self.logger.info(f"Explaining concept: {concept_name}")
        all_concepts = {**self.marketflow_concepts, **self.wyckoff_concepts}
        # Find the concept by case-insensitive matching if needed
        for key, explanation in all_concepts.items():
            if key.lower() == concept_name.lower():
                self.logger.info(f"Found explanation for concept: {key}")
                return explanation
        self.logger.warning(f"Concept '{concept_name}' not found.")
        return f"Concept '{concept_name}' not found."
    
    def _generate_analysis_narrative(self, analysis: dict) -> str:
        """
        Synthesizes the VPA and Wyckoff analysis into a coherent narrative story.
        This is the core intelligence of the interface.
        """
        self.logger.info(f"Generating analysis narrative for ticker: {analysis.get('ticker', 'UNKNOWN')}")
        ticker = analysis["ticker"]
        signal = analysis["signal"]
        primary_tf_key = list(analysis["timeframe_analyses"].keys())[0]
        primary_tf_analysis = analysis["timeframe_analyses"][primary_tf_key]
        
        # Extract the latest Wyckoff context
        latest_phase = primary_tf_analysis.get("wyckoff_phases", [])[-1] if primary_tf_analysis.get("wyckoff_phases") else None
        latest_event = primary_tf_analysis.get("wyckoff_events", [])[-1] if primary_tf_analysis.get("wyckoff_events") else None
        
        narrative = f"**Narrative Analysis for {ticker} (Primary Timeframe: {primary_tf_key}):**\n\n"
        
        # 1. Start with the overall VPA Signal
        narrative += f"The primary VPA signal is **{signal['type']} ({signal['strength']})**. "
        narrative += f"Reasoning: {signal['details']}.\n\n"
        
        # 2. Connect to Wyckoff Context
        if latest_phase and latest_event:
            phase_val = latest_phase['phase']
            event_val = latest_event['event']
            narrative += f"This signal is supported by the current Wyckoff context. The market is in **{phase_val}**. "
            narrative += f"The most recent significant event was a **{event_val}** on {latest_event['timestamp']}.\n"
            
            # Add specific narrative based on phase and signal
            if signal['type'] == 'BUY' and latest_phase['phase_name'] in ['D', 'E'] and 'Accumulation' in latest_phase.get('context', ''):
                narrative += f"This is a constructive pattern, suggesting that the accumulation phase has completed and the markup (uptrend) is underway. The {event_val} confirms buyer control.\n"
            elif signal['type'] == 'SELL' and latest_phase['phase_name'] in ['D', 'E'] and 'Distribution' in latest_phase.get('context', ''):
                narrative += f"This is a bearish pattern, suggesting that the distribution phase has completed and the markdown (downtrend) is in progress. The {event_val} confirms seller control.\n"
            elif signal['type'] == 'HOLD' or signal['type'] == 'NO_SIGNAL':
                 narrative += f"The market appears to be in a consolidation or 'cause-building' phase. It's advisable to wait for a clear Sign of Strength (breakout) or Sign of Weakness (breakdown) before considering a new position.\n"
            else:
                # Highlight conflicts
                narrative += f"**Warning:** There is a potential conflict between the VPA signal ({signal['type']}) and the Wyckoff context ({latest_phase.get('context', 'unknown')}). This suggests uncertainty, and caution is advised.\n"

        elif latest_phase:
             narrative += f"The market is currently in **{latest_phase['phase']}** according to Wyckoff analysis, but specific events are unclear. This indicates a period of consolidation.\n"
        else:
            narrative += "Wyckoff analysis did not identify a clear phase or event, suggesting the market is in a random or non-structural state.\n"

        # 3. Discuss Trading Ranges
        if primary_tf_analysis.get("wyckoff_trading_ranges"):
            tr = primary_tf_analysis["wyckoff_trading_ranges"][-1]
            narrative += f"\nA trading range has been identified between **support at ~${tr['support']:.2f}** and **resistance at ~${tr['resistance']:.2f}**. "
            narrative += "This range represents the 'cause' being built for the next trend.\n"

        # 4. Conclude with risk assessment
        risk = analysis['risk_assessment']
        narrative += f"\n**Trade Management:** Based on this analysis, the suggested stop-loss is **${risk.get('stop_loss', 0):.2f}** and the take-profit target is **${risk.get('take_profit', 0):.2f}**, offering a risk-reward ratio of **{risk.get('risk_reward_ratio', 0):.2f}**."

        self.logger.info(f"Generated narrative for {ticker}: {narrative[:200]}...")  # Log first 200 chars
        return narrative.strip()

    def get_ticker_analysis(self, ticker: str):
        """
        Get a complete, synthesized analysis for a ticker in a rich format for an LLM.
        """
        self.logger.info(f"Starting ticker analysis for: {ticker}")
        try:
            analysis = self.marketflow.analyze_ticker(ticker)
            if "error" in analysis:
                self.logger.error(f"Analysis error for {ticker}: {analysis['error']}")
                return analysis

            # Create a rich, structured output for the LLM
            llm_output = {
                "ticker": ticker,
                "current_price": analysis.get("current_price"),
                "vpa_signal": analysis.get("signal"),
                "risk_assessment": analysis.get("risk_assessment"),
                "analysis_narrative": self._generate_analysis_narrative(analysis),
                "timeframe_data": {}
            }
            
            # Populate detailed timeframe data, now including full Wyckoff results
            for tf, tf_data in analysis["timeframe_analyses"].items():
                self.logger.debug(f"Processing timeframe {tf} for {ticker}")
                llm_output["timeframe_data"][tf] = {
                    "trend": tf_data.get("trend_analysis"),
                    "support_resistance": tf_data.get("support_resistance"),
                    "wyckoff": {
                        "context": tf_data.get("wyckoff_trading_ranges", [{}])[-1].get("context", "Undefined"),
                        "phases": tf_data.get("wyckoff_phases", []),
                        "events": tf_data.get("wyckoff_events", []),
                        "trading_ranges": tf_data.get("wyckoff_trading_ranges", []),
                    }
                }

            self.logger.info(f"Completed ticker analysis for: {ticker}")
            return llm_output

        except Exception as e:
            self.logger.error(f"Error in VPALLMInterface get_ticker_analysis for {ticker}: {str(e)}", exc_info=True)
            return {
                "ticker": ticker,
                "error": f"An unexpected error occurred during analysis: {str(e)}"
            }

    # ...existing code...
    def generate_code_example(self, task, ticker="AAPL"):
        """
        Generate code example for a specific VPA task
        
        Parameters:
        - task: Task description (e.g., 'analyze_ticker', 'backtest', 'scan_market')
        - ticker: Example ticker to use
        
        Returns:
        - String with Python code example
        """
        if task == "analyze_ticker":
            return f"""
# Example: Analyze a single ticker with VPA
from vpa_facade import VPAFacade

# Initialize the VPA facade
vpa = VPAFacade()

# Analyze the ticker
results = vpa.analyze_ticker("{ticker}")

# Print the signal
print(f"Signal for {ticker}: {{results['signal']['type']}} ({{results['signal']['strength']}})")
print(f"Details: {{results['signal']['details']}}")

# Print risk assessment
print(f"Stop Loss: ${{results['risk_assessment']['stop_loss']:.2f}}")
print(f"Take Profit: ${{results['risk_assessment']['take_profit']:.2f}}")
print(f"Risk-Reward Ratio: {{results['risk_assessment']['risk_reward_ratio']:.2f}}")
"""
            
        elif task == "backtest":
            return f"""
# Example: Backtest VPA strategy
from vpa_facade import VPAFacade
import pandas as pd
import yfinance as yf

# Initialize the VPA facade
vpa = VPAFacade()

# Define backtest parameters
ticker = "{ticker}"
start_date = "2022-01-01"
end_date = "2023-01-01"
initial_capital = 10000

# Get historical data
data = yf.download(ticker, start=start_date, end=end_date)

# Initialize results tracking
equity = [initial_capital]
position = 0
entry_price = 0

# Loop through each day (excluding first 50 days for lookback)
for i in range(50, len(data)):
    # Get data up to current day
    current_data = data.iloc[:i+1]
    
    # Get current price
    current_price = current_data['Close'].iloc[-1]
    
    # Analyze with VPA (would need to modify facade to accept DataFrame)
    # This is simplified for example purposes
    signal = vpa.get_signals(ticker)
    
    # Execute trades based on signals
    if signal['signal']['type'] == 'BUY' and position == 0:
        # Calculate position size
        position = equity[-1] / current_price
        entry_price = current_price
        print(f"BUY at {{current_price:.2f}}")
    
    elif signal['signal']['type'] == 'SELL' and position > 0:
        # Close position
        equity.append(position * current_price)
        position = 0
        print(f"SELL at {{current_price:.2f}}")
    
    # Update equity if in position
    if position > 0:
        equity.append(position * current_price)
    else:
        equity.append(equity[-1])

# Calculate performance metrics
total_return = (equity[-1] - initial_capital) / initial_capital * 100
print(f"Total Return: {{total_return:.2f}}%")
"""
            
        elif task == "scan_market":
            return """
# Example: Scan market for VPA signals
from vpa_facade import VPAFacade

# Initialize the VPA facade
vpa = VPAFacade()

# Define list of tickers to scan
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "AMD"]

# Scan for strong buy signals
buy_signals = vpa.scan_for_signals(tickers, signal_type="BUY", signal_strength="STRONG")

# Print results
print("Strong Buy Signals:")
for ticker, result in buy_signals.items():
    print(f"{ticker}: {result['signal']['details']}")
    print(f"  Stop Loss: ${result['risk_assessment']['stop_loss']:.2f}")
    print(f"  Take Profit: ${result['risk_assessment']['take_profit']:.2f}")
    print(f"  Risk-Reward: {result['risk_assessment']['risk_reward_ratio']:.2f}")
    print()

# Scan for strong sell signals
sell_signals = vpa.scan_for_signals(tickers, signal_type="SELL", signal_strength="STRONG")

# Print results
print("Strong Sell Signals:")
for ticker, result in sell_signals.items():
    print(f"{ticker}: {result['signal']['details']}")
    print()
"""
        
        else:
            return """
# Basic VPA usage example
from vpa_facade import VPAFacade

# Initialize the VPA facade
vpa = VPAFacade()

# Analyze a ticker
results = vpa.analyze_ticker("AAPL")

# Print the results
print(f"Signal: {results['signal']['type']} ({results['signal']['strength']})")
print(f"Details: {results['signal']['details']}")
"""
