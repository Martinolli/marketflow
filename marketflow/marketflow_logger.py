"""
Marketflow Logger Module

This module provides standardized logging functionality for the Marketflow system.
It supports console and file logging, automatic log directory creation,
log rotation, and specialized logging methods for Marketflow operations.

Fixed version addressing compatibility issues:
- Fixed encoding parameter usage
- Fixed logger level validation
- Improved cross-platform path handling
- Better error handling
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any, Union

from .marketflow_utils import get_project_root

# Default log directory - cross-platform compatible
DEFAULT_LOG_DIR = get_project_root() / ".marketflow" / "logs"


def _resolve_log_level(level_name: str | None, default: int = logging.INFO) -> int:
    """Resolve a logging level name to a logging level, falling back safely."""
    if isinstance(level_name, str) and level_name.strip():
        level = getattr(logging, level_name.strip().upper(), None)
        if isinstance(level, int):
            return level
    return default


class MarketflowLogger:
    """Standardized logging framework for Marketflow system"""
    
    def __init__(self, log_level: str = "INFO", log_file: Optional[str] = None, 
                 module_name: Optional[str] = None, enable_rotation: bool = True,
                 max_bytes: int = 10485760, backup_count: int = 5, encoding: str = 'utf-8',
                 console_log_level: str | None = None):
        """
        Initialize the Marketflow logger
        
        Parameters:
        - log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        - console_log_level: Optional console-only level. Defaults to MARKETFLOW_CONSOLE_LOG_LEVEL or log_level
        - log_file: Optional path to log file. If None, a default path will be used
        - module_name: Optional module name for logger identification
        - enable_rotation: Whether to enable log rotation (default: True)
        - max_bytes: Maximum log file size in bytes before rotation (default: 10MB)
        - backup_count: Number of backup files to keep (default: 5)
        - encoding: File encoding for log files (default: utf-8)
        """
        self.module_name = module_name or "Marketflow"
        self.encoding = encoding
        self.file_level = _resolve_log_level(log_level, logging.INFO)
        console_level_name = console_log_level or os.getenv("MARKETFLOW_CONSOLE_LOG_LEVEL") or log_level
        self.console_level = _resolve_log_level(console_level_name, self.file_level)
        
        # If log_file is not specified, create a default one based on module name
        if log_file is None:
            DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = str(DEFAULT_LOG_DIR / f"{self.module_name.lower()}.log")
        
        self.log_file = log_file
        self.enable_rotation = enable_rotation
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # Initialize logger with proper error handling
        try:
            self.logger = self._setup_logger(log_level)
        except Exception as e:
            # Fallback to basic console logging if setup fails
            self.logger = logging.getLogger(self.module_name)
            self.logger.setLevel(min(self.file_level, self.console_level))
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.console_level)
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(console_handler)
            self.logger.error(f"Failed to setup logger properly: {e}")
    
    def _setup_logger(self, log_level: str) -> logging.Logger:
        """
        Set up logger with appropriate configuration
        
        Parameters:
        - log_level: Logging level
        
        Returns:
        - Configured logger
        """
        # Create logger
        logger = logging.getLogger(self.module_name)
        
        # Prevent adding handlers multiple times
        if logger.handlers:
            logger.setLevel(min(self.file_level, self.console_level))
            for handler in logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.setLevel(self.file_level)
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(self.console_level)
            return logger

        logger.setLevel(min(self.file_level, self.console_level))
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.console_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Create file handler if log file specified
        if self.log_file:
            try:
                # Create directory if it doesn't exist
                log_dir = Path(self.log_file).parent
                log_dir.mkdir(parents=True, exist_ok=True)
                
                # Use rotating file handler if enabled
                if self.enable_rotation:
                    file_handler = RotatingFileHandler(
                        self.log_file,
                        maxBytes=self.max_bytes,
                        backupCount=self.backup_count,
                        encoding=self.encoding  # Apply encoding parameter
                    )
                else:
                    file_handler = logging.FileHandler(
                        self.log_file, 
                        encoding=self.encoding  # Apply encoding parameter
                    )
                    
                file_handler.setLevel(self.file_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Failed to create file handler for {self.log_file}: {e}")
        
        return logger
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info=False) -> None:
        """Log error message"""
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """Log exception with traceback"""
        self.logger.exception(message)
    
    def log_analysis_start(self, ticker: str, timeframes: list) -> None:
        """
        Log the start of an analysis
        
        Parameters:
        - ticker: Stock symbol
        - timeframes: List of timeframes
        """
        try:
            if isinstance(timeframes, list) and timeframes:
                if isinstance(timeframes[0], dict):
                    timeframe_str = ", ".join([f"{tf.get('interval', 'unknown')}" for tf in timeframes])
                else:
                    timeframe_str = ", ".join([str(tf) for tf in timeframes])
            else:
                timeframe_str = str(timeframes)
            
            self.info(f"Starting Marketflow analysis for {ticker} on timeframes: {timeframe_str}")
        except Exception as e:
            self.error(f"Error logging analysis start for {ticker}: {e}")
    
    def log_analysis_complete(self, ticker: str, signal: Dict[str, Any]) -> None:
        """
        Log the completion of an analysis
        
        Parameters:
        - ticker: Stock symbol
        - signal: Signal information
        """
        try:
            signal_type = signal.get('type', 'unknown')
            signal_strength = signal.get('strength', 'unknown')
            self.info(f"Completed Marketflow analysis for {ticker}. Signal: {signal_type} ({signal_strength})")
        except Exception as e:
            self.error(f"Error logging analysis completion for {ticker}: {e}")
    
    def log_error(self, ticker: str, error: Union[str, Exception]) -> None:
        """
        Log an error during analysis
        
        Parameters:
        - ticker: Stock symbol
        - error: Error information
        """
        self.error(f"Error analyzing {ticker}: {error}")
    
    def log_data_retrieval(self, ticker: str, timeframe: str, success: bool) -> None:
        """
        Log data retrieval status
        
        Parameters:
        - ticker: Stock symbol
        - timeframe: Timeframe information
        - success: Whether retrieval was successful
        """
        if success:
            self.debug(f"Successfully retrieved {timeframe} data for {ticker}")
        else:
            self.warning(f"Failed to retrieve {timeframe} data for {ticker}")
    
    def log_pattern_detection(self, ticker: str, pattern: str, detected: bool) -> None:
        """
        Log pattern detection
        
        Parameters:
        - ticker: Stock symbol
        - pattern: Pattern name
        - detected: Whether pattern was detected
        """
        if detected:
            self.info(f"Detected {pattern} pattern for {ticker}")
        else:
            self.debug(f"No {pattern} pattern detected for {ticker}")
    
    def log_performance(self, operation: str, start_time: datetime, end_time: Optional[datetime] = None) -> None:
        """
        Log performance metrics
        
        Parameters:
        - operation: Operation name
        - start_time: Start time
        - end_time: Optional end time (defaults to now)
        """
        if end_time is None:
            end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        self.debug(f"Performance: {operation} took {duration:.2f} seconds")


# Create a singleton logger instance for each module
_loggers = {}

def get_logger(module_name: str = "Marketflow", log_level: str = "INFO", 
               log_file: Optional[str] = None, enable_rotation: bool = True,
               encoding: str = 'utf-8', console_log_level: str | None = None) -> MarketflowLogger:
    """
    Get a logger instance for the specified module
    
    Parameters:
    - module_name: Module name for logger identification
    - log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - log_file: Optional path to log file
    - enable_rotation: Whether to enable log rotation
    - encoding: File encoding for log files
    - console_log_level: Optional console-only logging level
    
    Returns:
    - MarketflowLogger instance
    """
    global _loggers
    
    # Create a unique key for the logger configuration
    logger_key = (
        f"{module_name}_{log_level}_{console_log_level}_"
        f"{log_file}_{enable_rotation}_{encoding}"
    )
    
    if logger_key not in _loggers:
        _loggers[logger_key] = MarketflowLogger(
            log_level=log_level,
            log_file=log_file,
            module_name=module_name,
            enable_rotation=enable_rotation,
            encoding=encoding,
            console_log_level=console_log_level,
        )
    
    return _loggers[logger_key]

def clear_loggers():
    """Clear all cached logger instances - useful for testing"""
    global _loggers
    _loggers.clear()
