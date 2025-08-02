"""
VPA LLM Interface Module

This module provides an intelligent, narrative-driven interface for LLMs 
to interact with the advanced VPA and Wyckoff analysis engine.
"""

import re
import yaml
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_wyckoff import WyckoffEvent, WyckoffPhase
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_llm_narrative import generate_analysis_narrative
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
        self.config_manager = create_app_config(logger=self.logger)

        # Initialize configuration
        # Load parameters or use default MarketFlowDataParameters
        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
            parameters = MarketFlowDataParameters()
        self.parameters = parameters

        # Initialize the VPA facade with the provided configuration and logger
        self.logger.info("Initializing VPAFacade with the interface's configuration and logger.")
        if not isinstance(self.parameters, MarketFlowDataParameters):
            self.logger.error("Invalid configuration provided. Expected MarketFlowDataParameters instance.")
            raise ValueError("Invalid configuration provided. Expected MarketFlowDataParameters instance.")
        # Pass the parameters to the facade.
        self.marketflow = MarketflowFacade(parameters=self.parameters)

        # Load concept explanations for VPA and Wyckoff from YAML files
        self.marketflow_concepts = self._load_concepts_from_yaml('marketflow/concepts/vpa_concepts.yaml')
        self.logger.info(f"Loaded VPA concepts: {len(self.marketflow_concepts)}")
        self.wyckoff_concepts = self._load_concepts_from_yaml('marketflow/concepts/wyckoff_concepts.yaml')
        self.logger.info(f"Loaded Wyckoff concepts: {len(self.wyckoff_concepts)}")

    def _load_concepts_from_yaml(self, file_path):
        """Loads concepts from a specified YAML file."""
        self.logger.debug(f"Loading concepts from {file_path}.")
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
        self.logger.error(f"Failed to load concepts from {file_path}.")

    def process_query(self, query: str) -> str:
        """
        Processes a natural language query. (This can be simplified if using an LLM with function calling)
        Args:
            query (str): The natural language query to process.
        Returns:
            str: A response based on the query, either an analysis or an explanation.
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


    def explain_concept(self, concept_name: str) -> str:
        """
        Explains a MarketFlow or Wyckoff concept dynamically, with logging.
        Args:
            concept_name (str): Name of the concept to explain.
        Returns:
            str: Explanation of the concept.
        
        """
        self.logger.info(f"Explaining concept: {concept_name}")
        all_concepts = {**self.marketflow_concepts, **self.wyckoff_concepts}
        # Find the concept by case-insensitive matching if needed
        for key, explanation in all_concepts.items():
            if key.lower() == concept_name.lower():
                self.logger.info(f"Found explanation for concept: {key}")
                return explanation
        self.logger.warning(f"Concept '{concept_name}' not found.")
        return f"Concept '{concept_name}' not found."

    def get_ticker_analysis(self, ticker: str) -> dict:
        """
        Get a complete, synthesized analysis for a ticker in a rich format for an LLM.
        Args:
            ticker (str): Ticker symbol to analyze.
        Returns:
            dict: Structured analysis data including VPA signals, Wyckoff phases, and narrative.
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
                "analysis_narrative": generate_analysis_narrative(analysis),
                "timeframe_data": {}
            }
            
            # Populate detailed timeframe data, now including full Wyckoff results
            for tf, tf_data in analysis["timeframe_analyses"].items():
                self.logger.debug(f"Processing timeframe {tf} for {ticker}")
                wyckoff_trading_ranges = tf_data.get("wyckoff_trading_ranges", [])
                last_trading_range = wyckoff_trading_ranges[-1] if wyckoff_trading_ranges else {}
                llm_output["timeframe_data"][tf] = {
                    "trend": tf_data.get("trend_analysis"),
                    "support_resistance": tf_data.get("support_resistance"),
                    "wyckoff": {
                        "context": last_trading_range.get("context", "Undefined"),
                        "phases": tf_data.get("wyckoff_phases", []),
                        "events": tf_data.get("wyckoff_events", []),
                        "trading_ranges": wyckoff_trading_ranges,
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
    def generate_code_example(self, task, ticker="AAPL") -> str:
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
