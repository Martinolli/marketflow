"""
Marketflow Result Extractor - Refactored
Extracts and organizes VPA analysis results with improved error handling and data validation.
"""

import pandas as pd
from typing import Dict, Any, List, Optional

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

class MarketflowResultExtractor:
    """
    Class for extracting and organizing Marketflow analysis results with improved error handling
    """
    
    def __init__(self, results: Dict[str, Any]):
        """
        Initialize the MarketflowResultExtractor
        
        Parameters:
        - results: Dictionary containing Marketflow analysis results
        - log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        - log_file: Optional path to log file
        - logger: Optional logger instance
        """
        # Validate input
        if not isinstance(results, dict):
            raise TypeError("results must be a dictionary")
        
        self.raw_results = results
        
        # Initialize logger
        # Initialize logger and configuration manager
        self.logger = get_logger(module_name="ResultExtractor")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)
        
        self.logger.info("ResultExtractor initialized")
        self.logger.debug(f"Raw results keys: {list(self.raw_results.keys())}")
        print(f"Raw results keys: {list(self.raw_results.keys())}")
        print(len(self.raw_results))
        print(f"Raw results: {self.raw_results}")
        
        # Extract and validate data
        try:
            self.extracted_data = self._extract_data()
            self.logger.info("Data extraction completed successfully")
        except Exception as e:
            self.logger.error(f"Data extraction failed: {e}")
            self.extracted_data = {}

    def _validate_data_structure(self, data: Any, expected_type: type, default_value: Any) -> Any:
        """Validate data structure and return default if invalid"""
        if isinstance(data, expected_type):
            return data
        else:
            self.logger.warning(f"Expected {expected_type.__name__}, got {type(data).__name__}. Using default.")
            return default_value

    def _safe_dataframe_creation(self, data: Any, context: str = "") -> pd.DataFrame:
        """Safely create DataFrame from various data types"""
        try:
            if data is None or (isinstance(data, dict) and not data):
                self.logger.debug(f"Empty data for DataFrame creation in {context}")
                return pd.DataFrame()
            
            if isinstance(data, pd.DataFrame):
                return data.copy()
            
            if isinstance(data, pd.Series):
                df = data.to_frame()
                self.logger.debug(f"Converted Series to DataFrame with shape {df.shape} in {context}")
                return df
            
            if isinstance(data, dict):
                # Handle nested dictionaries
                if all(isinstance(v, (list, pd.Series)) for v in data.values()):
                    df = pd.DataFrame(data)
                    self.logger.debug(f"Created DataFrame with shape {df.shape} in {context}")
                    return df
                else:
                    # Try to convert to DataFrame anyway
                    try:
                        df = pd.DataFrame([data])
                        self.logger.debug(f"Created single-row DataFrame in {context}")
                        return df
                    except Exception as e:
                        self.logger.warning(f"Could not create DataFrame from dict in {context}: {e}")
                        return pd.DataFrame()
            
            if isinstance(data, list):
                df = pd.DataFrame(data)
                self.logger.debug(f"Created DataFrame from list with shape {df.shape} in {context}")
                return df
            
            self.logger.warning(f"Unexpected data type {type(data)} in {context}")
            return pd.DataFrame()
            
        except Exception as e:
            self.logger.error(f"Error creating DataFrame in {context}: {e}")
            return pd.DataFrame()

    def _extract_data(self) -> Dict[str, Any]:
        """
        Process and structure the raw results with comprehensive error handling

        Parameters: self: Instance of VPAResultExtractor
        Returns: Dictionary with structured data for each ticker and timeframe
        """
        self.logger.info("Starting data extraction from raw results")
        extracted = {}
        
        for ticker, ticker_data in self.raw_results.items():
            try:
                self.logger.debug(f"Processing data for ticker: {ticker}") 
                
                # Validate ticker_data structure
                if not isinstance(ticker_data, dict):
                    self.logger.error(f"Invalid ticker data structure for {ticker}")
                    continue
                
                # Extract basic ticker information
                extracted[ticker] = {
                    'current_price': ticker_data.get('current_price', 0.0),
                    'signal': self._validate_data_structure(ticker_data.get('signal', {}), dict, {}),
                    'risk_assessment': self._validate_data_structure(ticker_data.get('risk_assessment', {}), dict, {}),
                    'timeframes': {}
                }
                
                # Extract timeframe analyses
                timeframe_analyses = ticker_data.get('timeframe_analyses', {})
                if not isinstance(timeframe_analyses, dict):
                    self.logger.warning(f"No valid timeframe_analyses for {ticker}")
                    timeframe_analyses = {}
                
                self.logger.debug(f"Found timeframes for {ticker}: {list(timeframe_analyses.keys())}")
                
                for timeframe, tf_data in timeframe_analyses.items():
                    try:
                        self.logger.debug(f"Extracting {timeframe} data for {ticker}")
                        
                        # Safely extract processed data
                        processed_data = tf_data.get('processed_data', {})
                        price_data = processed_data.get('price', {})
                        volume_data = processed_data.get('volume', {})
                        
                        extracted[ticker]['timeframes'][timeframe] = {
                            'price_data': self._safe_dataframe_creation(price_data, f"{ticker}-{timeframe}-price"),
                            'volume_data': self._safe_dataframe_creation(volume_data, f"{ticker}-{timeframe}-volume"),
                            'wyckoff_phases': self._validate_data_structure(tf_data.get('wyckoff_phases', []), list, []),
                            'wyckoff_events': self._validate_data_structure(tf_data.get('wyckoff_events', []), list, []),
                            'wyckoff_trading_ranges': self._validate_data_structure(tf_data.get('wyckoff_trading_ranges', []), list, []),
                            'candle_analysis': self._validate_data_structure(tf_data.get('candle_analysis', {}), dict, {}),
                            'trend_analysis': self._validate_data_structure(tf_data.get('trend_analysis', {}), dict, {}),
                            'pattern_analysis': self._validate_data_structure(tf_data.get('pattern_analysis', {}), dict, {}),
                            'support_resistance': self._validate_data_structure(tf_data.get('support_resistance', {}), dict, {})
                        }
                        
                        # Log data quality
                        price_df = extracted[ticker]['timeframes'][timeframe]['price_data']
                        volume_df = extracted[ticker]['timeframes'][timeframe]['volume_data']
                        self.logger.debug(f"{ticker}-{timeframe}: Price data shape: {price_df.shape}, Volume data shape: {volume_df.shape}")
                        
                    except Exception as e:
                        self.logger.error(f"Error processing timeframe {timeframe} for {ticker}: {e}")
                        extracted[ticker]['timeframes'][timeframe] = self._get_empty_timeframe_data()
                
            except Exception as e:
                self.logger.error(f"Error processing ticker {ticker}: {e}")
                continue
        
        self.logger.info(f"Data extraction completed. Extracted tickers: {list(extracted.keys())}")
        return extracted

    def _get_empty_timeframe_data(self) -> Dict[str, Any]:
        """Return empty timeframe data structure"""
        return {
            'price_data': pd.DataFrame(),
            'volume_data': pd.DataFrame(),
            'wyckoff_phases': [],
            'wyckoff_events': [],
            'wyckoff_trading_ranges': [],
            'candle_analysis': {},
            'trend_analysis': {},
            'pattern_analysis': {},
            'support_resistance': {}
        }

    # Public API methods with improved error handling
    
    def get_tickers(self) -> List[str]:
        """Get list of available tickers"""
        return list(self.extracted_data.keys())

    def get_ticker_data(self, ticker: str) -> Dict[str, Any]:
        """Get all data for a specific ticker"""
        self.logger.debug(f"Retrieving data for ticker: {ticker}")
        return self.extracted_data.get(ticker, {})

    def get_timeframes(self, ticker: str) -> List[str]:
        """Get available timeframes for a ticker"""
        ticker_data = self.get_ticker_data(ticker)
        timeframes = list(ticker_data.get('timeframes', {}).keys())
        self.logger.debug(f"Available timeframes for {ticker}: {timeframes}")
        return timeframes

    def get_price_data(self, ticker: str, timeframe: str) -> pd.DataFrame:
        """Get price data for ticker and timeframe"""
        self.logger.debug(f"Retrieving price data for {ticker} on {timeframe} timeframe")
        try:
            data = (self.extracted_data
                   .get(ticker, {})
                   .get('timeframes', {})
                   .get(timeframe, {})
                   .get('price_data', pd.DataFrame()))
            
            if data.empty:
                self.logger.warning(f"No price data available for {ticker}-{timeframe}")
            else:
                self.logger.debug(f"Retrieved price data with shape {data.shape} for {ticker}-{timeframe}")
            
            return data
        except Exception as e:
            self.logger.error(f"Error retrieving price data for {ticker}-{timeframe}: {e}")
            return pd.DataFrame()

    def get_volume_data(self, ticker: str, timeframe: str) -> pd.DataFrame:
        """Get volume data for ticker and timeframe"""
        try:
            data = (self.extracted_data
                   .get(ticker, {})
                   .get('timeframes', {})
                   .get(timeframe, {})
                   .get('volume_data', pd.DataFrame()))
            
            if data.empty:
                self.logger.warning(f"No volume data available for {ticker}-{timeframe}")
            
            return data
        except Exception as e:
            self.logger.error(f"Error retrieving volume data for {ticker}-{timeframe}: {e}")
            return pd.DataFrame()

    def get_candle_analysis(self, ticker: str, timeframe: str) -> Dict[str, Any]:
        """Get candle analysis for ticker and timeframe"""
        return (self.extracted_data
               .get(ticker, {})
               .get('timeframes', {})
               .get(timeframe, {})
               .get('candle_analysis', {}))

    def get_trend_analysis(self, ticker: str, timeframe: str) -> Dict[str, Any]:
        """Get trend analysis for ticker and timeframe"""
        return (self.extracted_data
               .get(ticker, {})
               .get('timeframes', {})
               .get(timeframe, {})
               .get('trend_analysis', {}))

    def get_pattern_analysis(self, ticker: str, timeframe: str) -> Dict[str, Any]:
        """Get pattern analysis for ticker and timeframe"""
        return (self.extracted_data
               .get(ticker, {})
               .get('timeframes', {})
               .get(timeframe, {})
               .get('pattern_analysis', {}))

    def get_support_resistance(self, ticker: str, timeframe: str) -> Dict[str, Any]:
        """Get support and resistance levels for ticker and timeframe"""
        return (self.extracted_data
               .get(ticker, {})
               .get('timeframes', {})
               .get(timeframe, {})
               .get('support_resistance', {}))

    def get_signal(self, ticker: str) -> Dict[str, Any]:
        """Get signal information for ticker"""
        self.logger.debug(f"Retrieving signal for ticker: {ticker}")
        return self.extracted_data.get(ticker, {}).get('signal', {})

    def get_signal_evidence(self, ticker: str) -> Dict[str, List]:
        """Get signal evidence for ticker"""
        return self.get_signal(ticker).get('evidence', {})
    
    def get_risk_assessment(self, ticker: str) -> Dict[str, Any]:
        """Get risk assessment for ticker"""
        return self.extracted_data.get(ticker, {}).get('risk_assessment', {})
    
    def get_current_price(self, ticker: str) -> float:
        """Get current price for ticker"""
        return self.extracted_data.get(ticker, {}).get('current_price', 0.0)
    
    def get_wyckoff_phases(self, ticker: str, timeframe: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get Wyckoff phases for ticker and optionally specific timeframe"""
        if timeframe:
            return (self.extracted_data
                   .get(ticker, {})
                   .get('timeframes', {})
                   .get(timeframe, {})
                   .get('wyckoff_phases', []))
        
        # Get all phases across timeframes
        all_phases = []
        ticker_data = self.extracted_data.get(ticker, {})
        for tf_data in ticker_data.get('timeframes', {}).values():
            all_phases.extend(tf_data.get('wyckoff_phases', []))
        return all_phases

    def get_wyckoff_events(self, ticker: str, timeframe: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get Wyckoff events for ticker and optionally specific timeframe"""
        if timeframe:
            return (self.extracted_data
                   .get(ticker, {})
                   .get('timeframes', {})
                   .get(timeframe, {})
                   .get('wyckoff_events', []))
        
        # Get all events across timeframes
        all_events = []
        ticker_data = self.extracted_data.get(ticker, {})
        for tf_data in ticker_data.get('timeframes', {}).values():
            all_events.extend(tf_data.get('wyckoff_events', []))
        return all_events

    def get_wyckoff_trading_ranges(self, ticker: str, timeframe: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get Wyckoff trading ranges for ticker and optionally specific timeframe"""
        if timeframe:
            return (self.extracted_data
                   .get(ticker, {})
                   .get('timeframes', {})
                   .get(timeframe, {})
                   .get('wyckoff_trading_ranges', []))
        
        # Get all trading ranges across timeframes
        all_ranges = []
        ticker_data = self.extracted_data.get(ticker, {})
        for tf_data in ticker_data.get('timeframes', {}).values():
            all_ranges.extend(tf_data.get('wyckoff_trading_ranges', []))
        return all_ranges

    def get_wyckoff_phases_df(self, ticker: str, timeframe: Optional[str] = None) -> pd.DataFrame:
        """Get Wyckoff phases as DataFrame"""
        phases = self.get_wyckoff_phases(ticker, timeframe)
        return pd.DataFrame(phases) if phases else pd.DataFrame()

    def get_wyckoff_events_df(self, ticker: str, timeframe: Optional[str] = None) -> pd.DataFrame:
        """Get Wyckoff events as DataFrame"""
        events = self.get_wyckoff_events(ticker, timeframe)
        return pd.DataFrame(events) if events else pd.DataFrame()

    def get_wyckoff_trading_ranges_df(self, ticker: str, timeframe: Optional[str] = None) -> pd.DataFrame:
        """Get Wyckoff trading ranges as DataFrame"""
        ranges = self.get_wyckoff_trading_ranges(ticker, timeframe)
        return pd.DataFrame(ranges) if ranges else pd.DataFrame()

    def has_data(self, ticker: str, timeframe: Optional[str] = None) -> bool:
        """Check if data exists for ticker and optionally timeframe"""
        if ticker not in self.extracted_data:
            return False
        
        if timeframe is None:
            return bool(self.extracted_data[ticker].get('timeframes'))
        
        tf_data = self.extracted_data[ticker].get('timeframes', {}).get(timeframe, {})
        price_data = tf_data.get('price_data', pd.DataFrame())
        return not price_data.empty

    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of available data"""
        summary = {}
        for ticker in self.get_tickers():
            ticker_summary = {
                'timeframes': self.get_timeframes(ticker),
                'has_signal': bool(self.get_signal(ticker)),
                'has_risk_assessment': bool(self.get_risk_assessment(ticker)),
                'current_price': self.get_current_price(ticker)
            }
            
            # Add data quality info
            for tf in ticker_summary['timeframes']:
                price_data = self.get_price_data(ticker, tf)
                ticker_summary[f'{tf}_price_rows'] = len(price_data)
                ticker_summary[f'{tf}_has_data'] = not price_data.empty
            
            summary[ticker] = ticker_summary
        
        return summary

# Standalone utility function to extract "Testing" pattern signals from results
def extract_testing_signals(results: dict) -> dict:
    """
    Extract 'Testing' pattern information for each ticker and timeframe.
    
    Returns a dictionary like:
    {
        "AAPL": {
            "1d": [ { "type": ..., "price": ..., "index": ... }, ... ],
            "1h": [...],
            ...
        },
        ...
    }
    """
    try:
        logger = get_logger(log_level="INFO", module_name="extract_testing_signals")
    except:
        logger = get_logger(log_level="INFO", module_name="extract_testing_signals")
    
    logger.info("Starting extraction of 'Testing' pattern signals")
    testing_data = {}

    for ticker, ticker_data in results.items():
        try:
            logger.debug(f"Processing 'Testing' patterns for ticker: {ticker}")
            testing_data[ticker] = {}

            timeframes = ticker_data.get("timeframes", {})
            for tf, tf_data in timeframes.items():
                try:
                    # Normalize all keys to lowercase for safety
                    pattern_analysis = {k.lower(): v for k, v in tf_data.get("pattern_analysis", {}).items()}
                    testing_section = pattern_analysis.get("testing", {})

                    if testing_section.get("Detected") and isinstance(testing_section.get("Tests"), list):
                        logger.debug(f"Found 'Testing' patterns for {ticker} on {tf} timeframe")
                        testing_data[ticker][tf] = testing_section["Tests"]
                except Exception as e:
                    logger.error(f"Error processing testing patterns for {ticker}-{tf}: {e}")
                    
        except Exception as e:
            logger.error(f"Error processing testing patterns for {ticker}: {e}")

    logger.info(f"Completed extraction of 'Testing' pattern signals for {len(testing_data)} tickers")
    return testing_data

