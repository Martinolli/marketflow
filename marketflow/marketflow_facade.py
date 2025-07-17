"""
Marketflow Facade Module

This module provides a simplified API for Marketflow Analysis.
"""

from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.marketflow_data_provider import PolygonIOProvider, MultiTimeframeProvider
from marketflow.marketflow_processor import DataProcessor
from marketflow.candle_analyzer import CandleAnalyzer
from marketflow.trend_analyzer import TrendAnalyzer
from marketflow.pattern_recognizer import PatternRecognizer
from marketflow.point_in_time_analyzer import PointInTimeAnalyzer
from marketflow.multi_timeframe_analyzer import MultiTimeframeAnalyzer
from marketflow.marketflow_signals import SignalGenerator, RiskAssessor
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_wyckoff import WyckoffAnalyzer

class MarketflowFacade:
    """Simplified API for Marketflow Analysis analysis"""
    
    def __init__(self, parameters=None):
        """
        Initialize the Marketflow Analysis facade
        
        Parameters:
        - log_level: Logging level
        - log_file: Optional path to log file
        - config: Optional Marketflow AnalysisConfig instance (if None, a new one will be created)
        - logger: Optional Marketflow AnalysisLogger instance (if None, a new one will be created)
        """
         # Initialize Logger
        self.logger = get_logger(module_name="MarketflowFacade")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)

        # Load parameters or use default MarketFlowDataParameters
        if parameters is None:
            self.logger.info("Using default MarketFlowFacadeParameters.")
        else:
            self.logger.info("Using provided MarketFlowFacadeParameters.")

        self.parameters = parameters or MarketFlowDataParameters() # 0 - Initialize parameters with default MarketFlowDataParameters
        
        self.data_provider = PolygonIOProvider() # 1 - Initialize data provider with default PolygonIOProvider

        self.multi_tf_provider = MultiTimeframeProvider(self.data_provider) # 2 - Initialize multi-timeframe provider with data provider

        self.multi_tf_analyzer = MultiTimeframeAnalyzer(self.parameters) # 3 - Initialize multi-timeframe analyzer with parameters

        self.signal_generator = SignalGenerator(self.parameters) # 4 - Initialize signal generator with parameters

        self.risk_assessor = RiskAssessor(self.parameters) # 5 - Initialize risk assessor with parameters

        self.processor = DataProcessor(self.parameters) # 6 - Initialize data processor with parameters

        # self.candle_analyzer = CandleAnalyzer(self.parameters) # Initialize candle analyzer with parameters

        # self.trend_analyzer = TrendAnalyzer(self.parameters) # Initialize trend analyzer with parameters

        # self.pattern_recognizer = PatternRecognizer(self.parameters) # Initialize pattern recognizer with parameters

        self.analyzer = PointInTimeAnalyzer(self.parameters) # 7 - Initialize point-in-time analyzer with parameters

    def analyze_ticker(self, ticker: str, timeframes=None) -> dict:
        """
        Analyze a ticker with Marketflow Analysis
        
        Parameters:
        - ticker: Stock symbol (e.g., 'AAPL', 'MSFT')
        - timeframes: Optional list of timeframe dictionaries with 'interval' and 'period' keys
        
        Returns:
        - Dictionary with analysis results
        """
        if timeframes is None:
            timeframes = self.parameters.get_timeframes()
        
        timeframe_data = self.multi_tf_provider.get_multi_timeframe_data(ticker, timeframes) # 8 - Fetch data for multiple timeframes
        
        if not timeframe_data:
            self.logger.error(f"No data fetched for {ticker} across specified timeframes. Aborting analysis.")
            return {
                "ticker": ticker,
                "error": "Failed to fetch market data for any specified timeframe.",
                "timeframe_analyses": {},
                "confirmations": [],
                "signal": {"type": "NO_SIGNAL", "strength": "NONE", "details": "Data unavailable"},
                "risk_assessment": {},
                "current_price": None
            }

        timeframe_analyses, confirmations = self.multi_tf_analyzer.analyze_multiple_timeframes(timeframe_data) # 9 - Analyze multiple timeframes

        signal = self.signal_generator.generate_signals(timeframe_analyses, confirmations) # 10 - Generate trading signals based on analysis
        
        primary_tf_key = list(timeframe_analyses.keys())[0] # 11 - Determine primary timeframe key
        current_price = None
        support_resistance = {}

        # Determine current price and support/resistance from primary timeframe if available
        if timeframe_analyses.get(primary_tf_key) and not timeframe_analyses[primary_tf_key]["processed_data"]["price"]["close"].empty:
            current_price = timeframe_analyses[primary_tf_key]["processed_data"]["price"]["close"].iloc[-1]
            support_resistance = timeframe_analyses[primary_tf_key]["support_resistance"]
        else:
            self.logger.warning(f"Could not determine current price or S/R for {ticker} from primary timeframe {primary_tf_key}.")
            signal["details"] += " (Current price unavailable for full risk assessment)"

        risk_assessment = self.risk_assessor.assess_trade_risk(signal, current_price, support_resistance) # 12 - Assess trade risk based on signal and current price
        
        ## --- Marketflow Analysis FACADE - WYCKOFF INTEGRATION POINT --- ##
        # The following loop integrates the Wyckoff analysis for each timeframe.
        # It is already compatible with the new Wyckoff module's output.
        for tf, tf_analysis_data in timeframe_analyses.items():
            try:
                processed_data = tf_analysis_data.get("processed_data")
                if processed_data and not processed_data.get("price").empty:
                    # Initialize the WyckoffAnalyzer with the necessary data and configuration.
                    # The new analyzer will automatically use the parameterized logic and dual-context detection.
                    wyckoff = WyckoffAnalyzer(
                        processed_data=processed_data,
                    )                                                                                    # 13 - Initialize WyckoffAnalyzer with processed data
                    self.logger.info(f"Running Wyckoff analysis for {ticker} on timeframe {tf}")
                    
                    # The `run_analysis` method from the improved module returns phases, events, and trading_ranges.
                    # This line correctly unpacks all three results.
                    phases, events, trading_ranges = wyckoff.run_analysis()                              # 14 - Run Wyckoff analysis and unpack results      

                    # Add all Wyckoff results to the timeframe analysis dictionary.
                    tf_analysis_data["wyckoff_phases"] = phases or []
                    tf_analysis_data["wyckoff_events"] = events or []
                    tf_analysis_data["wyckoff_trading_ranges"] = trading_ranges or []

                    if phases:
                        self.logger.info(f"Wyckoff phases detected for {ticker} on {tf}: {len(phases)} phases")
                    if events:
                        self.logger.info(f"Wyckoff events detected for {ticker} on {tf}: {len(events)} events (now with added detail)")
                    if trading_ranges:
                        self.logger.info(f"Wyckoff trading ranges detected for {ticker} on {tf}: {len(trading_ranges)} ranges")
                else:
                    tf_analysis_data["wyckoff_phases"] = []
                    tf_analysis_data["wyckoff_events"] = []
                    tf_analysis_data["wyckoff_trading_ranges"] = []

            except Exception as e:
                self.logger.error(f"Error running Wyckoff analysis for {ticker} on timeframe {tf}: {str(e)}")
                self.logger.exception("Detailed error information:")
                tf_analysis_data["wyckoff_phases"] = []
                tf_analysis_data["wyckoff_events"] = []
                tf_analysis_data["wyckoff_trading_ranges"] = []

        for tf, tf_analysis in timeframe_analyses.items():
            price = tf_analysis.get("processed_data", {}).get("price")
            volume = tf_analysis.get("processed_data", {}).get("volume")
            self.logger.debug(f"{ticker}-{tf}: price shape: {getattr(price, 'shape', None)}, volume shape: {getattr(volume, 'shape', None)}")

        results = {
            "ticker": ticker,
            "timeframe_analyses": timeframe_analyses,
            "confirmations": confirmations,
            "signal": signal,
            "risk_assessment": risk_assessment,
            "current_price": current_price
        }
        self.logger.log_analysis_complete(ticker, signal)
        
        return results

    def analyze_ticker_at_point(self, ticker: str, sliced_data_by_timeframe: dict) -> dict:
        """
        Analyze a ticker using only data up to a specific historical point in time.

        Parameters:
        - ticker: Stock symbol
        - sliced_data_by_timeframe: dict with {'1d': df, '1h': df, '15m': df} where df is a pandas DataFrame
                                     containing OHLCV data up to the point of analysis.

        Returns:
        - dict containing signal summary, score, and metadata, or None on error.
        """
        try:
            if self.analyzer is None:
                self.logger.error("CRITICAL: self.analyzer is not initialized in Marketflow Analysis Facade. analyze_ticker_at_point cannot function.")
                raise AttributeError("'Marketflow AnalysisFacade' object has no attribute 'analyzer' that is properly initialized. This must be fixed by initializing self.analyzer in __init__.")

            processed_timeframe_data = {}
            if not sliced_data_by_timeframe:
                self.logger.error(f"No sliced data provided for {ticker} in analyze_ticker_at_point.")
                return None

            for tf, data_slice in sliced_data_by_timeframe.items():
                if data_slice.empty:
                    self.logger.warning(f"Empty data slice for timeframe {tf} for ticker {ticker}. Skipping timeframe.")
                    continue

                required_cols = ['open', 'high', 'low', 'close', 'volume']
                if not all(col in data_slice.columns for col in required_cols):
                    self.logger.error(f"Data slice for {tf} is missing required OHLCV columns. Cannot proceed.")
                    continue

                self.logger.info(f"Processing {ticker} data for point-in-time analysis, timeframe {tf}")
                self.logger.debug(f"Data slice shape: {data_slice.shape}, Columns: {data_slice.columns.tolist()}")

                price_to_process = data_slice[['open', 'high', 'low', 'close']]
                volume_to_process = data_slice['volume']
                processed_timeframe_data[tf] = self.processor.preprocess_data(price_to_process, volume_to_process)
            
            if not processed_timeframe_data:
                self.logger.error(f"No data could be processed for {ticker} in analyze_ticker_at_point after attempting all timeframes.")
                return None

            signals = self.analyzer.analyze_all(processed_timeframe_data)
            
            primary_tf_key_for_pit = self.parameters.get_primary_timeframe()
            if primary_tf_key_for_pit not in processed_timeframe_data:
                if processed_timeframe_data:
                    primary_tf_key_for_pit = list(processed_timeframe_data.keys())[0]
                else:
                    self.logger.error(f"No processed data available to determine primary timeframe for {ticker}.")
                    return None

            rr_info = self.analyzer.compute_risk_reward(processed_timeframe_data[primary_tf_key_for_pit], signals.get(primary_tf_key_for_pit, {}))
            volatility = self.analyzer.compute_volatility(processed_timeframe_data[primary_tf_key_for_pit])
            pattern_summary = signals[primary_tf_key_for_pit].get("pattern_summary", "")
            confidence_score = self.analyzer.compute_confidence_score(signals)

            return {
                "ticker": ticker,
                "timestamp": processed_timeframe_data[primary_tf_key_for_pit]["price"].index[-1].strftime("%Y-%m-%d %H:%M"),
                "signals": signals,
                "risk_reward": rr_info,
                "volatility": volatility,
                "pattern_summary": pattern_summary,
                "confidence_score": confidence_score,
            }

        except AttributeError as ae:
            if 'self.analyzer' in str(ae) or "'NoneType' object has no attribute 'analyze_all'" in str(ae):
                self.logger.error(f"❌ Error in analyze_ticker_at_point for {ticker}: 'self.analyzer' is not defined or initialized in Marketflow AnalysisFacade. This is a known issue from the original function structure. Details: {str(ae)}")
                self.logger.exception("Detailed error information:")
            else:
                self.logger.error(f"❌ AttributeError in analyze_ticker_at_point for {ticker}: {str(ae)}")
                self.logger.exception("Detailed error information:")
            return None
        except Exception as e:
            self.logger.error(f"❌ Error analyzing {ticker} at point-in-time: {str(e)}")
            self.logger.exception("Detailed error information:")
            return None

    def get_signals(self, ticker: str, timeframes=None) -> dict:
        """
        Get trading signals for a ticker
        Parameters:
        - ticker: Stock symbol (e.g., 'AAPL', 'MSFT')
        - timeframes: Optional list of timeframe dictionaries with 'interval' and 'period' keys
        Returns:
        - Dictionary with signal results
        """
        self.logger.info(f"Getting signals for {ticker} with timeframes: {timeframes}")

        results = self.analyze_ticker(ticker, timeframes)
        if "error" in results: 
            return results 
        signal_results = {
            "ticker": ticker,
            "signal": results["signal"],
            "risk_assessment": results["risk_assessment"],
            "current_price": results["current_price"]
        }
        return signal_results
    
    def explain_signal(self, ticker, timeframes=None):
        """
        Generate a detailed explanation of the trading signal for a ticker
        Parameters:
        - ticker: Stock symbol (e.g., 'AAPL', 'MSFT')
        - timeframes: Optional list of timeframe dictionaries with 'interval' and 'period' keys
        Returns:
        - String with detailed explanation of the signal
        """
        self.logger.info(f"Generating explanation for {ticker} with timeframes: {timeframes}")

        # Fetch analysis results for the ticker
        results = self.analyze_ticker(ticker, timeframes)
        if "error" in results: 
            return f"Could not generate explanation for {ticker} due to an error: {results['error']}"

        signal = results["signal"]
        evidence = signal.get("evidence", {}) 
        risk_assessment = results["risk_assessment"]
        current_price = results["current_price"]
        
        explanation = f"Marketflow Analysis Analysis for {ticker}:\n\n"
        explanation += f"Signal: {signal.get('type', 'N/A')} ({signal.get('strength', 'N/A')})\n"
        explanation += f"Details: {signal.get('details', 'N/A')}\n\n"
        explanation += "Supporting Evidence:\n"
        
        if evidence.get("candle_signals"):
            explanation += "- Candle Signals:\n"
            for candle_signal in evidence["candle_signals"]:
                explanation += f"  * {candle_signal.get('timeframe', 'N/A')}: {candle_signal.get('details', 'N/A')}\n"
        
        if evidence.get("trend_signals"):
            explanation += "- Trend Signals:\n"
            for trend_signal in evidence["trend_signals"]:
                explanation += f"  * {trend_signal.get('timeframe', 'N/A')}: {trend_signal.get('details', 'N/A')}\n"
        
        if evidence.get("pattern_signals"):
            explanation += "- Pattern Signals:\n"
            for pattern_signal in evidence["pattern_signals"]:
                explanation += f"  * {pattern_signal.get('timeframe', 'N/A')} - {pattern_signal.get('pattern', 'N/A')}: {pattern_signal.get('details', 'N/A')}\n"
        
        if evidence.get("timeframe_confirmations"):
            explanation += "- Timeframe Confirmations:\n"
            explanation += f"  * Confirmed in timeframes: {', '.join(evidence['timeframe_confirmations'])}\n"
        
        explanation += "\nRisk Assessment:\n"
        
        if isinstance(current_price, (int, float)):
            current_price_str = f"${current_price:.2f}"
        else:
            current_price_str = "N/A"
        explanation += f"- Current Price: {current_price_str}\n"
        
        explanation += f"- Stop Loss: ${risk_assessment.get('stop_loss', 0):.2f}\n"
        explanation += f"- Take Profit: ${risk_assessment.get('take_profit', 0):.2f}\n"
        explanation += f"- Risk-Reward Ratio: {risk_assessment.get('risk_reward_ratio', 0):.2f}\n"
        explanation += f"- Recommended Position Size: {risk_assessment.get('position_size', 0):.2f} shares\n"
        
        self.logger.info(f"Generated explanation for {ticker}")
        self.logger.debug(explanation)
        return explanation
    
    def batch_analyze(self, tickers, timeframes=None) -> dict:
        """
        Batch analyze multiple tickers and return their analysis results
        Parameters:
        - tickers: List of stock symbols (e.g., ['AAPL', 'MSFT'])
        - timeframes: Optional list of timeframe dictionaries with 'interval' and 'period' keys
        Returns:
        - Dictionary with ticker as key and analysis results as value
        """
        self.logger.info(f"Batch analyzing {len(tickers)} tickers with timeframes: {timeframes}")
        results = {}
        for ticker in tickers:
            try:
                ticker_results = self.get_signals(ticker, timeframes)
                results[ticker] = ticker_results
            except Exception as e:
                self.logger.error(f"Error in batch_analyze for {ticker}: {e}", exc_info=True)
                results[ticker] = {
                    "error": str(e)
                }
        return results
    
    def scan_for_signals(self, tickers, signal_type=None, signal_strength=None, timeframes=None) -> dict:
        """
        Scan multiple tickers for specific trading signals
        Parameters:
        - tickers: List of stock symbols (e.g., ['AAPL', 'MSFT'])
        - signal_type: Optional type of signal to filter (e.g., 'BUY', 'SELL')
        - signal_strength: Optional strength of signal to filter (e.g., 'STRONG', 'WEAK')
        - timeframes: Optional list of timeframe dictionaries with 'interval' and 'period' keys
        Returns:
        - Dictionary with ticker as key and analysis results as value
        """

        self.logger.info(f"Scanning {len(tickers)} tickers for signals. Type: {signal_type}, Strength: {signal_strength}")
        all_results = self.batch_analyze(tickers, timeframes)
        filtered_results = {}
        for ticker, result in all_results.items():
            if "error" in result:
                self.logger.warning(f"Error in results for {ticker}: {result['error']}")
                continue
            if signal_type and result.get("signal", {}).get("type") != signal_type:
                continue
            if signal_strength and result.get("signal", {}).get("strength") != signal_strength:
                continue
            filtered_results[ticker] = result
        self.logger.info(f"Found {len(filtered_results)} matching signals")
        return filtered_results