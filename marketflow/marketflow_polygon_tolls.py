#-------------------------------------------------------------------------------
# VPA Polygon Provider Module 
# This module provides an interface to fetch stock data from Polygon.io
# Date Created: 2025-09-06
#--------------------------------------------------------------------------------

# vpa_polygon_provider.py
from typing import Tuple, Dict, Optional
import os
from dotenv import load_dotenv
import requests
from polygon import RESTClient
from polygon.rest.models import Agg
from datetime import datetime, timedelta

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
#-------------------------------------------------------------------------------
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

# Class to fetch stock data from Polygon.io
class PolygonDataProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
        # Initialize logger and config manager
        self.logger = get_logger(module_name="PolygonTollsProvider")
        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)
    
    def _initialize_client(self) -> None:
        """Initialize the Polygon.io REST client with error handling"""
        try:
            # Get API key from config manager
            api_key = self.config_manager.get_api_key('polygon')
            
            # Validate API key
            if not api_key:
                self.logger.error("Polygon.io API key not found")
                raise ValueError("Polygon.io API key not found")
            
            # Initialize client
            self.client = RESTClient(api_key)
            self.logger.debug("Polygon.io client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Polygon.io client: {e}")
            self.client = None
    
    def _validate_client(self) -> bool:
        """Validate that the client is initialized"""
        if self.client is None:
            self.logger.warning("Polygon.io client not initialized, attempting to initialize")
            self._initialize_client()
        
        return self.client is not None
    
    # Handle errors and retry logic
    def _handle_error(self, error: Exception, ticker: str, interval: str, 
                      attempt: int = 0) -> Tuple[ErrorCategory, str]:
        """
        Handle errors with categorization and logging
        
        Parameters:
        - error: The exception that occurred
        - ticker: Stock symbol
        - interval: Timeframe interval
        - attempt: Current retry attempt
        
        Returns:
        - Tuple of (error_category, error_message)
        """
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

    # 1 - Fetches cutsom bars (OHLCV) for a ticker

    def get_custom_bars(self, ticker: str, multiplier: int, timespan: str, from_date: str, to_date: str, adjusted: bool = "true", sort: str = "asc", limit: int = 120) -> Optional[Dict]:
        """
        Retrieve aggregated historical OHLC (Open, High, Low, Close) and volume data for a specified stock ticker over a custom date range and time
        interval in Eastern Time (ET). Aggregates are constructed exclusively from qualifying trades that meet specific conditions. If no eligible
        trades occur within a given timeframe, no aggregate bar is produced, resulting in an empty interval that indicates a lack of trading activity
        during that period. Users can tailor their data by adjusting the multiplier and timespan parameters (e.g., a 5-minute bar), covering pre-market,
        regular market, and after-hours sessions. This flexibility supports a broad range of analytical and visualization needs.

        Use Cases: Data visualization, technical analysis, backtesting strategies, market research.

        Parameters:
        - stocksticker (string): Stock symbol (e.g., 'AAPL')
        - multiplier (integer): Size of the timespan multiplier (e.g., 1, 5, 15)
        - timespan (enum string): One of 'second', 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'
        - from_date (string): Start date in 'YYYY-MM-DD' format
        - to_date (string): End date in 'YYYY-MM-DD' format
        Query Parameters:
        - adjusted (boolean): Whether to use adjusted data (default: "true")
        - sort (enum string): Sort direction of results "asc" ord "desc" (default: 'asc')
        - limit: Maximum number of bars to return (default: 120)

        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            aggs=[]
            for a in self.client.list_aggs(
                ticker=ticker,
                multiplier=multiplier,
                timespan=timespan,
                from_=from_date,
                to=to_date,
                adjusted=adjusted,
                sort=sort,
                limit=limit,
            ):
                aggs.append(a)
            return {"results": [bar.__dict__ for bar in aggs], "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, f"{multiplier}{timespan}")
            self.logger.error(f"Error fetching custom bars: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None

    # 2 - Get All Tickers

    def get_all_tickers(self, tickers: str) -> Optional[Dict]:
        """
        Retrieve a comprehensive list of ticker symbols supported by Polygon.io across
        various asset classes (e.g., stocks, indices, forex, crypto). Each ticker entry
        provides essential details such as symbol, name, market, currency, and active status.

        Use Cases: Asset discovery, portfolio management, market analysis, and tradingUse Cases:
        Asset discovery, data integration, filtering/selection, and application development.

        parameters:
        - ticker (string): Specify a ticker symbol. Defaults to empty string which queries all tickers.
        - type (enum - string): Specify the type of the tickers. Find the types that we support via our Ticker Types API. Defaults to empty string which queries all types.
        - market (enum - string): stocks, crypto, fx, otc, indices.
        - exchange (string): Specify the primary exchange of the asset in the ISO code format. Find more information about the ISO codes at the ISO org website. Defaults to empty string which queries all exchanges.
        - cusip (string): Specify the CUSIP code of the asset you want to search for. Find more information about CUSIP codes at their website. Defaults to empty string which queries all CUSIPs.
        - cik (string): Specify the CIK of the asset you want to search for. Find more information about CIK codes at their website. Defaults to empty string which queries all CIKs.
        - date (string): Specify a point in time to retrieve tickers available on that date. Defaults to the most recent available date.
        - search (string): Search for terms within the ticker and/or company name.
        - active (bolean): Specify if the tickers returned should be actively traded on the queried date. Default is true.
        - order (enum string): Order results based on the `sort` field.
        - limit (integer): Limit the number of results returned, default is 100 and max is 1000.
        - sort (enum string): Sort field used for ordering - ticker, name, market, locale, primary_exchange, type, currency_symbol, currency_name, base_currency_symbol, base_currency_name, cik, composite_figi, share_class_figi, last_updated_utce, delisted_utc.

        """
        try:
            tickers = []
            for t in self.client.list_tickers(
                market ="stocks",
                active = True,
                order="asc",
                limit="100",
                sort="ticker",
                ):
                tickers.append(t)
            return {"results": [ticker.__dict__ for ticker in tickers], "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, "all", "tickers")
            self.logger.error(f"Error fetching all tickers: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None

#   3 - Get Ticker Overview
    def get_ticker_overview(self, ticker: str) -> Optional[Dict]:
        """
        Retrieve comprehensive details for a single ticker supported by Polygon.io. This endpoint offers a
        deep look into a company’s fundamental attributes, including its primary exchange, standardized identifiers
        (CIK, composite FIGI, share class FIGI), market capitalization, industry classification, and key dates.
        Users also gain access to branding assets (e.g., logos, icons), enabling them to enrich applications and
        analyses with visually consistent, contextually relevant information.

        Use Cases: Company research, data integration, application enhancement, due diligence & compliance.

        Parameters:
        - ticker (string): The stock symbol for which to retrieve details (e.g., 'AAPL').
        Query parameters are optional.
        - date (string): Specify a point in time to get information about the ticker available on that date.
        When retrieving information from SEC filings, we compare this date with the period of report date on the SEC filing.
        For example, consider an SEC filing submitted by AAPL on 2019-07-31, with a period of report date ending on 2019-06-29.
        That means that the filing was submitted on 2019-07-31, but the filing was created based on information from 2019-06-29.
        If you were to query for AAPL details on 2019-06-29, the ticker details would include information from the SEC filing.
        Defaults to the most recent available date.

        """
        try:
            details = self.client.get_ticker_details(ticker)
            return {"results": details.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "overview")
            self.logger.error(f"Error fetching ticker overview: {error_message}")
            return None
        
    # 4 - Get Daily Ticker Summary
    def get_daily_ticker_summary(self, ticker: str, date: str) -> Optional[Dict]:
        """
        Retrieve the opening and closing prices for a specific stock ticker on a given date,
        along with any pre-market and after-hours trade prices. This endpoint provides
        essential daily pricing details, enabling users to evaluate performance, conduct
        historical analysis, and gain insights into trading activity outside regular market
        sessions.

        Use Cases: Daily performance analysis, historical data collection, after-hours insights, portfolio tracking.

        Parameters:
        - stocksticker (string): Specify a case-sensitive ticker symbol. For example, AAPL represents Apple Inc.
        - date (string): Specify a date in 'YYYY-MM-DD' format to retrieve the daily summary for that date.
        Query parameters are optional.
        - adjusted (boolean): Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.

        """
        try:
            summary = self.client.get_daily_open_close_agg(
                ticker=ticker,
                date=date,
                adjusted=True
            )
            return {"results": summary.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "daily_summary")
            self.logger.error(f"Error fetching daily ticker summary: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None

    # 5 - Previous Day Bar (OHLC)
    def get_previous_day_bar(self, ticker: str) -> Optional[Dict]:
        """
        Retrieve the previous trading day's open, high, low, and close (OHLC)
        data for a specified stock ticker. This endpoint provides key pricing
        metrics, including volume, to help users assess recent performance and
        inform trading strategies.

        Use Cases: Baseline comparison, technical analysis, market research, and daily reporting.
        Parameters:
        - stocksticker (string): Specify a case-sensitive ticker symbol. For example, AAPL represents Apple Inc.
        - adjusted (boolean): Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        """
        try:
            aggs = self.client.get_previous_close_agg(
                ticker=ticker,
                adjusted=True
            )
            return {"results": aggs.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "previous_day_bar")
            self.logger.error(f"Error fetching previous day bar: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None
        
    # 6 - Get Trades
    def get_trades(self, ticker: str, from_date: str, limit: int = 1000) -> Optional[Dict]:
        """
        Retrieve comprehensive, tick-level trade data for a specified stock ticker within a defined time
        range. Each record includes price, size, exchange, trade conditions, and precise timestamp
        information. This granular data is foundational for constructing aggregated bars and performing
        in-depth analyses, as it captures every eligible trade that contributes to calculations of open,
        high, low, and close (OHLC) values. By leveraging these trades, users can refine their understanding
        of intraday price movements, test and optimize algorithmic strategies, and ensure compliance by
        maintaining an auditable record of market activity.

        Use Cases: Intraday analysis, algorithmic trading, market microstructure research, data integrity
        and compliance.
        
        Parameters:
        - stocksticker (string): pecify a case-sensitive ticker symbol. For example, AAPL represents Apple Inc.
        Query parameters are optional.
        - timestamp (string): Query by trade timestamp. Either a date with the format YYYY-MM-DD or a nanosecond timestamp.
                - timestamp modifiers: timestamp.gte = Search timestamp for values that are greater than or equal to the given value.
                - timestamp modifiers: timestamp.gt = Search timestamp for values that are greater than the given value.
                - timestamp modifiers: timestamp.lte = Search timestamp for values that are less than or equal to the given value.
                - timestamp modifiers: timestamp.lt = Search timestamp for values that are less than the given value.
        - order (enum string): Order results based on the `sort` field. "asc" or "desc"
        - limit (integer): Limit the number of results returned, default is 1000 and max is 50000.
        - sort (enum string): Sort results based on the `timestamp` field. "asc" or "desc"


        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            trades = self.client.list_trades(
                ticker=ticker,
                timestamp=from_date,
                order="asc",
                limit=limit,
                sort="timestamp",
            )
            return {"results": [trade.__dict__ for trade in trades], "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "trades")
            self.logger.error(f"Error fetching trades: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None
    # 7 - Get Quotes
    def get_quotes(self, ticker: str, from_date: str, limit: int = 1000) -> Optional[Dict]:
        """
        Retrieve National Best Bid and Offer (NBBO) quotes for a specified stock ticker over a
        defined time range. Each record includes the prevailing best bid/ask prices, sizes,
        exchanges, and timestamps, reflecting the top-of-book quote environment at each moment.
        By examining this historical quote data, users can analyze price movements, evaluate
        liquidity at the NBBO level, and enhance trading strategies or research efforts.

        Use Cases: Historical quote analysis, liquidity evaluation, algorithmic backtesting,
        trading strategy refinement.

        Parameters:
        - stocksticker (string): Specify a case-sensitive ticker symbol. For example, AAPL represents Apple Inc.
        Query parameters are optional.
        - timestamp (string): Query by quote timestamp. Either a date with the format YYYY-MM-DD or a nanosecond timestamp.
        - order (enum string): Order results based on the `sort` field. "asc" or "desc"
        - limit (integer): Limit the number of results returned, default is 1000 and max is 50000.
        - sort (enum string): Sort results based on the `timestamp` field. "asc" or "desc"
        
        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            quotes = []
            for t in self.client.list_quotes(
                ticker=ticker,
                order="asc",
                limit=limit,
                timestamp=from_date,
                sort="timestamp",
                ):
                quotes.append(t)
            return {"results": [quote.__dict__ for quote in quotes], "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "quotes")
            self.logger.error(f"Error fetching quotes: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None

    # 8 - Get Last Quote
    def get_last_quote(self, ticker: str) -> Optional[Dict]:
        """
        Retrieve the most recent National Best Bid and Offer (NBBO) quote for a specified
        stock ticker, including the latest bid/ask prices, sizes, exchange details,
        and timestamp. This endpoint supports monitoring current market conditions and
        updating platforms or applications with near-term quote information, allowing
        users to evaluate liquidity, track spreads, and make more informed decisions.

        Use Cases: Price display, spread analysis, market monitoring.

        Parameters:
        - stocksticker (string): Specify a case-sensitive ticker symbol. For example, AAPL represents Apple Inc.
        
        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            quote = self.client.get_last_quote(
                ticker=ticker,
            )
            return {"results": quote.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "last_quote")
            self.logger.error(f"Error fetching last quote: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None        

    # 9 - Simple Moving Average (SMA)

    def get_simple_moving_average(self, ticker: str, timespan: str, series_type: str, order: str, limit: str, window: int = 20) -> Optional[Dict]:
        """
        Retrieve the Simple Moving Average (SMA) for a specified ticker over a defined time range. 
        The SMA calculates the average price across a set number of periods, smoothing price
        fluctuations to reveal underlying trends and potential signals.

        Use Cases: Trend analysis, trading signal generation (e.g., SMA crossovers),
        identifying support/resistance, and refining entry/exit timing.

        Parameters:
        - ticker: Stock symbol (e.g., 'AAPL')
        - timespan: One of 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'
        - series_type: Type of price series to use (e.g., 'close', 'open', 'high', 'low')
        - order: Sort order of results ('asc' or 'desc')
        - limit: Maximum number of results to return
        - window: Number of periods to calculate the SMA (default: 20)
        
        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            sma = self.client.get_sma(
                ticker=ticker,
                timespan=timespan,
                adjusted=True,
                window=window,
                series_type=series_type,
                order=order,
                limit=limit,
            )
            return {"results": sma.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "sma")
            self.logger.error(f"Error fetching simple moving average: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None
        
    # 10 - Exponential Moving Average (EMA)

    def get_exponential_moving_average(self, ticker: str, timestamp: str, timespan: str, series_type: str, order: str, limit: str, window: int = 20) -> Optional[Dict]:
        """
        Retrieve the Exponential Moving Average (EMA) for a specified ticker over a defined time range. The EMA places
        greater weight on recent prices, enabling quicker trend detection and more responsive signals.

        Use Cases: Trend identification, EMA crossover signals, dynamic support/resistance levels, and adjusting
        strategies based on recent market volatility.

        Parameters:
        - ticker: Stock symbol (e.g., 'AAPL')
        - timestamp: Start date in 'YYYY-MM-DD' format
        - timespan: One of 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'
        - adjusted (boolean): Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        - series_type: Type of price series to use (e.g., 'close', 'open', 'high', 'low')
        - order: Sort order of results ('asc' or 'desc')
        - limit (integer): Maximum number of results to return
        - window (integer): Number of periods to calculate the EMA (default: 20)
        - expanded_undelying (boolean): Whether or not to include the aggregates used to calculate this indicator in the response - "true" or "false".

        
        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            ema = self.client.get_ema(
                ticker=ticker,
                timestamp=timestamp,
                timespan=timespan,
                adjusted="true",
                expanded_underlying="true",
                window=window,
                series_type=series_type,
                order=order,
                limit=limit,
            )
            return {"results": ema.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "ema")
            self.logger.error(f"Error fetching exponential moving average: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None

    # 11 Moving Average Convergence Divergence (MACD)

    def get_macd(self, ticker: str, timestamp: str, timespan: str, series_type: str, order: str, short_window: int = 12, long_window: int = 26, signal_window: int = 9, limit=100) -> Optional[Dict]:
        """
        Retrieve the Moving Average Convergence/Divergence (MACD) for a specified ticker over a defined time range.
        MACD is a momentum indicator derived from two moving averages, helping to identify trend strength, direction,
        and potential trading signals.

        Use Cases: Momentum analysis, signal generation (crossover events), spotting overbought/oversold conditions, and confirming trend directions.
        Parameters:
        - stockticker (string): Specify a case-sensitive ticker symbol for which to get moving average convergence/divergence (MACD) data. For example, AAPL represents Apple Inc.
        Query Parameters:
        - timestamp (string): Query by timestamp. Either a date with the format YYYY-MM-DD or a millisecond timestamp.
        - timespan (enum string): One of 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'
        - adjusted (boolean): Whether or not the aggregates used to calculate the MACD are adjusted for splits. By default, aggregates are adjusted. Set this to false to get results that are NOT adjusted for splits.
        - short_window (integer): Number of periods for the fast EMA (default: 12)
        - long_window (integer): Number of periods for the slow EMA (default: 26)
        - signal_window (integer): Number of periods for the signal line EMA (default: 9)
        - series_type (enum string): Type of price series to use (e.g., 'close', 'open', 'high', 'low')
        - expand_underlying (boolean): Whether or not to include the aggregates used to calculate this indicator in the response.
        - order (enum string): Sort order of results ('asc' or 'desc'), The order in which to return the results, ordered by timestamp.
        - limit (integer): Maximum number of results to return, default = 10
        
        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            macd = self.client.get_macd(
                ticker=ticker,
                timestamp=timestamp,
                timespan=timespan,
                adjusted="true",
                short_window=short_window,
                long_window=long_window,
                signal_window=signal_window,
                series_type=series_type,
                expand_underlying="true",
                order=order,
                limit=limit,
            )
            return {"results": macd.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "macd")
            self.logger.error(f"Error fetching MACD: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None

    # 12 Relative Strength Index (RSI)
    def get_relative_strength_index(self, ticker: str, timestamp: str, timespan: str, series_type: str, order: str, limit: str, window: int = 14) -> Optional[Dict]:
        """
        Retrieve the Relative Strength Index (RSI) for a specified ticker over a defined time range. The RSI measures the speed
        and magnitude of price changes, oscillating between 0 and 100 to help identify overbought or oversold conditions.

        Use Cases: Overbought/oversold detection, divergence analysis, trend confirmation, and refining market entry/exit strategies.

        Parameters:
        - ticker: Stock symbol (e.g., 'AAPL')
        - timestamp: Start date in 'YYYY-MM-DD' format
        - timespan: One of 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'
        - series_type: Type of price series to use (e.g., 'close', 'open', 'high', 'low')
        - order: Sort order of results ('asc' or 'desc')
        - limit: Maximum number of results to return
        - window: Number of periods to calculate the RSI (default: 14)
        - adjusted (boolean): Whether or not the aggregates used to calculate the relative strength index are adjusted for splits. By default, aggregates are adjusted. Set this to false to get results that are NOT adjusted for splits.
        - expand_underlying (boolean): Whether or not to include the aggregates used to calculate this indicator in the response.

        Returns:
        - Dictionary containing results and status, or None if an error occurred
        """
        try:
            rsi = self.client.get_rsi(
                ticker=ticker,
                timestamp=timestamp,
                timespan=timespan,
                series_type=series_type,
                adjusted="true",
                expand_underlying="true",
                order=order,
                limit=limit,
                window=window,
            )
            return {"results": rsi.__dict__, "status": "OK"}
        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "rsi")
            self.logger.error(f"Error fetching RSI: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None

    # 13 Get Dividends

    def get_dividens(self, ticker: str, ex_dividend_date: str, record_date: str, declaration_date: str, pay_date: str, frequency: str, cash_amount, dividend_type: str, order: str, sort: str, limit=10) -> Optional[Dict]:
        """
        Retrieve a historical record of cash dividend distributions for a given ticker, including declaration, ex-dividend,
        record, and pay dates, as well as payout amounts and frequency. This endpoint consolidates key dividend information,
        enabling users to account for dividend income in returns, develop dividend-focused strategies, and support tax reporting needs.

        Use Cases: Income analysis, total return calculations, dividend strategies, tax planning.

        Query parameters:
        - ticker (string): Specify a case-sensitive ticker symbol for which to get dividend information. For example, AAPL represents Apple Inc.
        - ex_dividend_date (string): Ex-dividend date in 'YYYY-MM-DD' format
        - record_date (string): Record date in 'YYYY-MM-DD' format
        - declaration_date (string): Declaration date in 'YYYY-MM-DD' format
        - pay_date (string): Pay date in 'YYYY-MM-DD' format
        - frequency (enum integer): Query by the number of times per year the dividend is paid out. Possible values are 0 (one-time), 1 (annually), 2 (bi-annually), 4 (quarterly), 12 (monthly), 24 (bi-monthly), and 52 (weekly).
        - cash_amount (number): Query by the cash amount of the dividend payment.
        - dividend_type (enum string): Query by the type of dividend payment. Possible values are 'CD', 'SC', 'LT', and 'ST'.
        - order (enum string): Sort order of results ('asc' or 'desc')
        - limit (integer): Maximum number of results to return
        - sort (enum string): Sort field used for ordering - 'ex_dividend_date', 'record_date', 'declaration_date', 'pay_date', 'cash_amount', and 'ticker'.       
        """
        try: 
            dividends = self.client.list_dividends(
                ticker=ticker,
                ex_dividend_date=ex_dividend_date,
                record_date=record_date,
                declaration_date=declaration_date,
                pay_date=pay_date,
                frequency=frequency,
                cash_amount=cash_amount,
                dividend_type=dividend_type,
                order=order,
                sort=sort,
                limit=limit,
            )
            return {"results": dividends.__dict__, "status": "OK"}

        except Exception as e:
            error_category, error_message = self._handle_error(e, ticker, "rsi")
            self.logger.error(f"Error fetching RSI: {error_message}")
            self.logger.error(f"Error Category: {error_category}")
            return None
        
if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        print("Error: POLYGON_API_KEY not found in environment variables")
        exit(1)

    poly = PolygonDataProvider(POLYGON_API_KEY)

    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)  # Get data for the last 30 days
    ticker="AAPL"
    # Test Relative Strength Index
    custom_bars = poly.get_custom_bars(
        ticker,
        multiplier=1,
        timespan="day",
        from_date=from_date.strftime("%Y-%m-%d"),
        to_date=to_date.strftime("%Y-%m-%d"),
        adjusted="true",
        sort="asc",
        limit=10
        )
    if custom_bars:
        print(f"\nSuccessfully fetched Custom Bars for {ticker}")
        print("Custom Bars data:")
        print(custom_bars['results'])
    else:
        print(f"Failed to fetch Custom for {ticker}")