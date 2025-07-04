"""
Marketflow Data Provider Module with Enhanced Error Handling and Abstract Base Class

This module provides data access for Marketflow analysis with robust error handling
and a clear, extensible interface for future data providers.
"""

import time
from datetime import datetime, timedelta, timezone
from typing import Coroutine, Dict, List, Tuple, Optional, Any
from pandas.tseries.offsets import DateOffset
from abc import ABC, abstractmethod
import asyncio

import pandas as pd
import numpy as np
from polygon import RESTClient
from polygon.rest.models import Agg

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

# Constants for error handling
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2  # seconds
MAX_RETRY_DELAY = 30  # seconds
REQUEST_TIMEOUT = 30  # seconds

# Error categories
class ErrorCategory:
    NETWORK = "NETWORK_ERROR"
    API = "API_ERROR"
    AUTHENTICATION = "AUTHENTICATION_ERROR"
    RATE_LIMIT = "RATE_LIMIT_ERROR"
    DATA_PROCESSING = "DATA_PROCESSING_ERROR"
    UNKNOWN = "UNKNOWN_ERROR"

class DataProvider(ABC):
    """
    Abstract base class for all Marketflow data providers.
    Enforces implementation of the get_data interface.
    """
    @abstractmethod
    def get_data(self, ticker: str, interval: str = "1d", period: str = "1y",
                 start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Optional[Tuple[pd.DataFrame, pd.Series]]:
        """
        Fetch price and volume data for a ticker.
        Must be implemented by subclasses.
        Returns a tuple of (price_df, volume_series), or None if data could not be fetched.
        """
        pass
    
    @abstractmethod
    async def get_data_async(self, ticker: str, interval: str = "1d", period: str = "1y",
                 start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Optional[Tuple[pd.DataFrame, pd.Series]]:
        """
        Asynchronously fetch price and volume data for a ticker.
        Must be implemented by subclasses that support async operations.
        """
        pass

class PolygonIOProvider(DataProvider):
    """Data provider using Polygon.io API with enhanced error handling"""

    def __init__(self):
        """Initialize the Polygon.io data provider"""

        # Initialize logger and configuration manager
        self.logger = get_logger(module_name="PolygonIOProvider")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)
        
        self.client: Optional[RESTClient] = None
        self.async_client: Optional[RESTClient] = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the Polygon.io REST clients (sync and async) with error handling"""
        try:
            api_key = self.config_manager.get_api_key('polygon')
            if not api_key:
                self.logger.error("Polygon.io API key not found")
                raise ValueError("Polygon.io API key not found")
            self.client = RESTClient(api_key)
            # The async client is instantiated from the same class with a boolean flag
            self.async_client = RESTClient(api_key, True)
            self.logger.debug("Polygon.io clients (sync & async) initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Polygon.io clients: {e}")
            self.client = None
            self.async_client = None
    
    def _validate_client(self) -> bool:
        """Validate that the clients are initialized"""
        if self.client is None or self.async_client is None:
            self.logger.warning("Polygon.io client(s) not initialized, attempting to initialize")
            self._initialize_client()
        return self.client is not None and self.async_client is not None
    
    def _handle_error(self, error: Exception, ticker: str, interval: str, attempt: int = 0) -> Tuple[str, str]:
        """Handle errors with categorization and logging"""
        error_str = str(error)
        error_category = ErrorCategory.UNKNOWN

        # Categorize error
        if "ConnectionError" in error_str or "timeout" in error_str.lower():
            error_category = ErrorCategory.NETWORK
            message = f"Network error fetching data for {ticker} at {interval} timeframe: {error}"
        elif "401" in error_str or "Unauthorized" in error_str:
            error_category = ErrorCategory.AUTHENTICATION
            message = f"Authentication error with Polygon.io API: {error}"
        elif "429" in error_str or "Too Many Requests" in error_str:
            error_category = ErrorCategory.RATE_LIMIT
            message = f"Rate limit exceeded for Polygon.io API: {error}"
        elif "404" in error_str or "Not Found" in error_str:
            error_category = ErrorCategory.API
            message = f"Resource not found for {ticker} at {interval} timeframe: {error}"
        elif "format" in error_str.lower() or "invalid" in error_str.lower():
            error_category = ErrorCategory.DATA_PROCESSING
            message = f"Data format error for {ticker} at {interval} timeframe: {error}"
        else:
            message = f"Unknown error fetching data for {ticker} at {interval} timeframe: {error}"
        
        # Log with appropriate level based on attempt and category
        if attempt < MAX_RETRIES - 1 and error_category in [ErrorCategory.NETWORK, ErrorCategory.RATE_LIMIT]:
            self.logger.warning(message)
        else:
            self.logger.error(message)
            if error_category == ErrorCategory.AUTHENTICATION:
                self.logger.error("Please check your Polygon.io API key")
        return error_category, message

    def _calculate_retry_delay(self, attempt: int, error_category: str) -> float:
        """Calculate retry delay with exponential backoff and jitter"""
        delay = min(INITIAL_RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
        delay = delay * (0.5 + 0.5 * np.random.random())
        if error_category == ErrorCategory.RATE_LIMIT:
            delay = delay * 2
        return delay

    def _should_retry(self, error_category: str, attempt: int) -> bool:
        """Determine if a retry should be attempted"""
        if error_category == ErrorCategory.AUTHENTICATION:
            return False
        if attempt >= MAX_RETRIES - 1:
            return False
        if error_category in [ErrorCategory.NETWORK, ErrorCategory.RATE_LIMIT]:
            return True
        if error_category == ErrorCategory.API and attempt == 0:
            return True
        return False

    def _process_aggregates(self, aggs: List[Agg]) -> Tuple[pd.DataFrame, pd.Series]:
        if not aggs:
            return pd.DataFrame(), pd.Series(dtype=float)
        data = []
        for agg in aggs:
            data.append({
                'timestamp': datetime.fromtimestamp(agg.timestamp / 1000, tz=timezone.utc),
                'open': agg.open,
                'high': agg.high,
                'low': agg.low,
                'close': agg.close,
                'volume': agg.volume
            })
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        price_df = df[['open', 'high', 'low', 'close']]
        volume_series = df['volume']
        return price_df, volume_series

    async def _fetch_data_core(
        self,
        ticker: str,
        interval: str,
        period: str,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Optional[Tuple[pd.DataFrame, pd.Series]]:
        """
        Core asynchronous data fetching logic with retries. Shared by sync and async methods.
        """
        if not self._validate_client() or self.async_client is None:
            self.logger.error("Cannot fetch data: Polygon.io async client not initialized")
            return None

        multiplier, timespan = self._parse_interval(interval)
        if multiplier is None or timespan is None:
            self.logger.error(f"Unsupported interval format: {interval}")
            return None

        # Calculate date range
        if end_date is None:
            end_date_dt = datetime.now()
        elif isinstance(end_date, str):
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        elif isinstance(end_date, pd.Timestamp):
            end_date_dt = end_date.to_pydatetime()
        else:
            end_date_dt = end_date

        if start_date is None:
            start_date_dt = self._calculate_start_date(end_date_dt, period)
        elif isinstance(start_date, str):
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        elif isinstance(start_date, pd.Timestamp):
            start_date_dt = start_date.to_pydatetime()
        else:
            start_date_dt = start_date

        # Fetch data with retry logic
        for attempt in range(MAX_RETRIES):
            try:
                self.logger.debug(f"Fetching data for {ticker} at {interval} timeframe (Attempt {attempt + 1}/{MAX_RETRIES})")
                aggs = await self.async_client.get_aggs(
                    ticker=ticker, multiplier=multiplier, timespan=timespan,
                    from_=start_date_dt.strftime("%Y-%m-%d"), to=end_date_dt.strftime("%Y-%m-%d"),
                    limit=50000
                )
                price_df, volume_series = self._process_aggregates(aggs)
                if price_df.empty:
                    self.logger.warning(f"No data returned for {ticker} at {interval} timeframe")
                    return None
                self.logger.debug(f"Successfully fetched {len(price_df)} data points for {ticker} at {interval} timeframe")
                return price_df, volume_series
            except Exception as e:
                error_category, message = self._handle_error(e, ticker, interval, attempt)
                if self._should_retry(error_category, attempt):
                    delay = self._calculate_retry_delay(attempt, error_category)
                    self.logger.info(f"Retrying in {delay:.2f} seconds (Attempt {attempt + 1}/{MAX_RETRIES})")
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"Error fetching data for {ticker} at {interval} timeframe: {e}")
                    return None
        self.logger.error(f"Failed to fetch data for {ticker} at {interval} timeframe after {MAX_RETRIES} attempts")
        return None
        
    def get_data(
        self,
        ticker: str,
        interval: str = "1d",
        period: str = "1y",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[Tuple[pd.DataFrame, pd.Series]]:
        """
        Get price and volume data for a ticker with robust error handling.
        Returns (price_df, volume_series) or None if data could not be fetched.
        """
        # This is the standard way to call an async function from sync code.
        try:
            return asyncio.run(self._fetch_data_core(ticker, interval, period, start_date, end_date))
        except RuntimeError as e:
            # This handles the case where get_data is called from an already running event loop
            if "cannot run loop while another loop is running" in str(e):
                self.logger.error(
                    "get_data (sync) was called from within an async context. "
                    "Use get_data_async instead. Returning None."
                )
                return None
            raise # Re-raise other RuntimeErrors

    async def get_data_async(
        self,
        ticker: str,
        interval: str = "1d",
        period: str = "1y",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[Tuple[pd.DataFrame, pd.Series]]:
        """
        Asynchronously get price and volume data for a ticker with robust error handling.
        Returns (price_df, volume_series) or None if data could not be fetched.
        """
        return await self._fetch_data_core(ticker, interval, period, start_date, end_date)

    def _parse_interval(self, interval: str) -> Tuple[Optional[int], Optional[str]]:
        """Parse interval string into multiplier and timespan"""
        try:
            if interval.endswith('m'):
                return int(interval[:-1]), 'minute'
            elif interval.endswith('h'):
                return int(interval[:-1]), 'hour'
            elif interval.endswith('d'):
                return int(interval[:-1]), 'day'
            elif interval.endswith('w'):
                return int(interval[:-1]), 'week'
            else:
                self.logger.error(f"Unsupported interval format: {interval}")
                return None, None
        except Exception as e:
            self.logger.error(f"Error parsing interval {interval}: {e}")
            return None, None

    def _calculate_start_date(self, end_date: datetime, period: str) -> datetime:
        """Calculate start date based on end date and period"""
        try:
            if period.endswith('d'):
                days = int(period[:-1])
                return end_date - timedelta(days=days)
            elif period.endswith('w'):
                weeks = int(period[:-1])
                return end_date - timedelta(weeks=weeks)
            elif period.endswith('m'):
                months = int(period[:-1])
                return end_date - DateOffset(months=months)
            elif period.endswith('y'):
                years = int(period[:-1])
                return end_date - DateOffset(years=years)
            else:
                self.logger.warning(f"Unsupported period format: {period}, defaulting to 1 year")
                return end_date - timedelta(days=365)
        except Exception as e:
            self.logger.error(f"Error calculating start date with period {period}: {e}")
            return end_date - timedelta(days=365)

class MultiTimeframeProvider:
    """Provider for multiple timeframes using a DataProvider instance"""

    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.logger = get_logger(module_name="MultiTimeframeProvider")

    def get_multi_timeframe_data(self, ticker: str, timeframes: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        timeframe_data = {}
        for tf_config in timeframes:
            interval = tf_config['interval']
            period = tf_config.get('period', '1y')
            start_date = tf_config.get('start_date')
            end_date = tf_config.get('end_date')
            tf_key = f"{interval}"
            try:
                result = self.data_provider.get_data(
                    ticker,
                    interval=interval,
                    period=period,
                    start_date=start_date,
                    end_date=end_date
                )
                if result is None or result[0].empty:
                    self.logger.warning(f"No price data returned for {ticker} at {interval} timeframe. Skipping.")
                    continue
                price_data, volume_data = result
                timeframe_data[tf_key] = {
                    'price_data': price_data,
                    'volume_data': volume_data
                }
            except Exception as e:
                self.logger.error(f"Error fetching data for {ticker} at {interval} timeframe: {e}", exc_info=True)
        if not timeframe_data:
            self.logger.warning(f"Could not fetch data for any requested timeframe for {ticker}")
        return timeframe_data

    async def get_multi_timeframe_data_async(self, ticker: str, timeframes: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Asynchronously fetches data for multiple timeframes concurrently.
        """
        if not hasattr(self.data_provider, 'get_data_async'):
            self.logger.error("The provided data provider does not support asynchronous fetching.")
            return {}

        tasks: List[Tuple[str, Coroutine[Any, Any, Optional[Tuple[pd.DataFrame, pd.Series]]]]] = []
        for tf_config in timeframes:
            interval = tf_config['interval']
            period = tf_config.get('period', '1y')
            start_date = tf_config.get('start_date')
            end_date = tf_config.get('end_date')
            tf_key = f"{interval}"
            
            coro = self.data_provider.get_data_async(
                ticker, interval=interval, period=period,
                start_date=start_date, end_date=end_date
            )
            tasks.append((tf_key, coro))

        # Gather results from all tasks, returning exceptions to handle them gracefully
        results = await asyncio.gather(*[coro for _, coro in tasks], return_exceptions=True)

        timeframe_data = {}
        for (tf_key, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                self.logger.error(f"Error fetching data for {ticker} at {tf_key} timeframe: {result}", exc_info=True)
                continue
            
            if result is None or result[0].empty:
                self.logger.warning(f"No price data returned for {ticker} at {tf_key} timeframe. Skipping.")
                continue
            
            price_data, volume_data = result
            timeframe_data[tf_key] = {'price_data': price_data, 'volume_data': volume_data}

        if not timeframe_data:
            self.logger.warning(f"Could not fetch data for any requested timeframe for {ticker}")
        return timeframe_data