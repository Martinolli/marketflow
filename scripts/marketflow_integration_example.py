"""
MarketFlow Integration Example

This module demonstrates how to properly initialize and use both the 
marketflow_logger and marketflow_config_manager modules together without
circular import issues.

This example shows the recommended pattern for dependency injection.
"""

# Import the fixed modules
from marketflow.marketflow_logger import get_logger, MarketflowLogger
from marketflow.marketflow_config_manager import get_config_manager, create_app_config

def initialize_marketflow_system():
    """
    Initialize the MarketFlow system with proper dependency injection.
    
    Returns:
    - Tuple of (logger, config_manager)
    """
    # Step 1: Initialize the logger first (no dependencies)
    logger = get_logger(
        module_name="MarketFlow_System",
        log_level="INFO",
        enable_rotation=True
    )
    
    # Step 2: Initialize the config manager with the logger (dependency injection)
    config_manager = get_config_manager(logger=logger)
    
    # Step 3: Validate the configuration
    validation_results = config_manager.validate_configuration()
    
    # Log validation results
    logger.info("MarketFlow system initialization completed")
    logger.info(f"Configuration validation results: {validation_results}")
    
    # Check for critical issues
    if not validation_results.get('log_file_path', False):
        logger.warning("Log file path validation failed")
    
    if not validation_results.get('openai_api_key', False):
        logger.warning("OpenAI API key not found or invalid")
    
    if not validation_results.get('polygon_api_key', False):
        logger.warning("Polygon API key not found or invalid")
    
    return logger, config_manager

def create_module_specific_logger(module_name: str, config_manager):
    """
    Create a logger for a specific module using configuration from config_manager.
    
    Parameters:
    - module_name: Name of the module
    - config_manager: ConfigManager instance
    
    Returns:
    - MarketflowLogger instance
    """
    return get_logger(
        module_name=module_name,
        log_level=config_manager.LOG_LEVEL,
        enable_rotation=True
    )

def example_usage():
    """Example of how to use the MarketFlow system"""
    
    # Initialize the system
    logger, config_manager = initialize_marketflow_system()
    
    # Create module-specific loggers
    data_logger = create_module_specific_logger("DataProvider", config_manager)
    analyzer_logger = create_module_specific_logger("Analyzer", config_manager)
    
    # Example usage of configuration
    logger.info("=== MarketFlow System Example ===")
    
    # Check API keys
    if config_manager.OPENAI_API_KEY:
        logger.info("OpenAI API key is configured")
    else:
        logger.warning("OpenAI API key is not configured")
    
    if config_manager.POLYGON_API_KEY:
        logger.info("Polygon API key is configured")
    else:
        logger.warning("Polygon API key is not configured")
    
    # Show LLM configuration
    logger.info(f"LLM Provider: {config_manager.LLM_PROVIDER}")
    logger.info(f"LLM Model: {config_manager.get_llm_model()}")
    
    # Example of specialized logging
    data_logger.log_data_retrieval("AAPL", "1D", True)
    analyzer_logger.log_analysis_start("AAPL", [{"interval": "1D"}, {"interval": "4H"}])
    
    # Example of pattern detection logging
    analyzer_logger.log_pattern_detection("AAPL", "Wyckoff Accumulation", True)
    
    # Example of analysis completion
    signal = {
        "type": "BUY",
        "strength": "STRONG",
        "confidence": 0.85
    }
    analyzer_logger.log_analysis_complete("AAPL", signal)
    
    logger.info("=== Example completed successfully ===")
    
    return logger, config_manager

if __name__ == "__main__":
    # Run the example
    try:
        logger, config = example_usage()
        print("\\nMarketFlow system initialized successfully!")
        print(f"Log files are being written to: {config.LOG_FILE_PATH}")
        print(f"Config validation: {config.validate_configuration()}")
    except Exception as e:
        print(f"Error initializing MarketFlow system: {e}")
        import traceback
        traceback.print_exc()

