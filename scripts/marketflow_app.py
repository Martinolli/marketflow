"""
VPA Main Application Entry Point - Refactored Version

This script provides the main entry point for the VPA application,
refactored to work with the updated VPA components and configuration system.
It uses the merged configuration manager and updated query engine.
"""

import os
import sys
import logging
import argparse
from typing import Optional, Tuple

from marketflow import marketflow_config_manager
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config, get_marketflow_config_manager
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
from marketflow.marketflow_memory_manager import MemoryManager

# Add the project root to sys.path to ensure modules can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Assuming this script is in a subdirectory
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Global flag for basic mode
BASIC_MODE = False

logger = get_logger(module_name="MarketflowApp")
config_manager = create_app_config(logger=logger)

def setup_logging(config) -> logging.Logger:
    """Set up logging configuration using the config manager."""
    # Create log directory
    log_dir = os.path.dirname(config.LOG_FILE_PATH)
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE_PATH),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("marketflow_app")

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Marketflow Analysis System - Refactored")

    # Model and provider selection arguments
    parser.add_argument(
        "--model", 
        help="LLM model to use (e.g., gpt-3.5-turbo, gpt-4, llama3:instruct)"
    )
    parser.add_argument(
        "--provider",
        choices=['openai', 'ollama'],
        help="LLM provider to use (openai or ollama)"
    )
    parser.add_argument(
        "--list-models", 
        action="store_true",
        help="List available models and exit"
    )
    
    # Query arguments
    parser.add_argument(
        "--query", 
        help="Process a single query and exit"
    )
    parser.add_argument(
        "--ticker", 
        help="Ticker symbol to analyze (e.g., AAPL, MSFT)"
    )
    
    # Configuration arguments
    parser.add_argument(
        "--config", 
        help="Path to configuration file"
    )
    parser.add_argument(
        "--save-config", 
        action="store_true",
        help="Save current configuration to file"
    )
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Validate configuration and exit"
    )
    
    # Debug arguments
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser.parse_args()


def validate_configuration(config) -> bool:
    """
    Validate the configuration and display results.
    
    Parameters:
    - config: Configuration manager instance
    
    Returns:
    - True if configuration is valid, False otherwise
    """
    print("\n=== Configuration Validation ===")
    
    validation_results = config.validate_configuration()
    all_valid = True
    
    for component, is_valid in validation_results.items():
        status = "✓" if is_valid else "✗"
        print(f"{status} {component}: {'Valid' if is_valid else 'Invalid'}")
        if not is_valid:
            all_valid = False
    
    print(f"\nOverall Status: {'✓ Valid' if all_valid else '✗ Issues Found'}")
    
    # Show current configuration
    print(f"\nCurrent Configuration:")
    print(f"  LLM Provider: {config.LLM_PROVIDER}")
    print(f"  OpenAI Model: {config.OPENAI_MODEL_NAME}")
    print(f"  Ollama Model: {config.OLLAMA_MODEL_NAME}")
    print(f"  Ollama URL: {config.OLLAMA_BASE_URL}")
    print(f"  Log Level: {config.LOG_LEVEL}")
    print(f"  Memory DB: {config.MEMORY_DB_PATH}")
    print("=" * 35)
    
    return all_valid


def list_available_models(config) -> None:
    """List available models and exit."""
    print("\n=== Available Models ===")
    print(f"Current provider: {config.LLM_PROVIDER}")
    print(f"Current model: {config.get_llm_model()}")
    
    print("\nConfigured models:")
    models = config.get_available_models()
    for model in models:
        current_marker = " (current)" if model == config.get_llm_model() else ""
        print(f"  - {model}{current_marker}")
    
    print(f"\nTo use a specific model: --model MODEL_NAME")
    print(f"To switch providers: --provider PROVIDER_NAME")
    print("========================\n")


def initialize_vpa_system(config, model_name: Optional[str] = None, provider: Optional[str] = None):
    """
    Initialize the VPA system with the specified configuration.
    
    Parameters:
    - config: Configuration manager instance
    - model_name: Optional model name override
    - provider: Optional provider override
    
    Returns:
    - VPAQueryEngine instance or None if in basic mode
    """
    logger = get_logger("marketflow_app")
    
    if BASIC_MODE:
        logger.warning("Running in basic mode - VPA query engine not available")
        print("⚠ Running in basic mode - full VPA functionality not available")
        return None
    
    # Override configuration if specified
    if provider:
        logger.info(f"Overriding LLM provider to: {provider}")
        config.set_config_value('llm_provider', provider.lower())
    
    if model_name:
        logger.info(f"Overriding LLM model to: {model_name}")
        config.set_llm_model(model_name)
    
    # Create query engine
    logger.info("Creating VPA query engine with updated configuration")
    try:
        query_engine = MarketflowLLMQueryEngine(config=config)
        logger.info(f"VPA query engine initialized successfully")
        return query_engine
    except Exception as e:
        logger.error(f"Failed to initialize VPA query engine: {e}")
        raise


def process_single_query(query: str, ticker: Optional[str] = None, config=None, 
                        model_name: Optional[str] = None, provider: Optional[str] = None) -> None:
    """
    Process a single query and display the result.
    
    Parameters:
    - query: Query string to process
    - ticker: Optional ticker symbol for analysis
    - config: Configuration manager instance
    - model_name: Optional model name to use
    - provider: Optional provider to use
    """
    logger = logging.getLogger("vpa_app")
    
    if BASIC_MODE:
        print(f"\nQuery: {query}")
        print("⚠ Running in basic mode - VPA analysis not available")
        print("This would normally process your query using the VPA system.")
        print("Please ensure all VPA modules are installed for full functionality.\n")
        return
    
    # Initialize VPA system
    query_engine = initialize_vpa_system(config, model_name, provider)
    if query_engine is None:
        return
    
    # If ticker is provided, incorporate it into the query
    if ticker:
        logger.info(f"Adding ticker context: {ticker}")
        if ticker.upper() not in query.upper():
            query = f"{query} for {ticker.upper()}"
    
    # Process query
    logger.info(f"Processing query: {query}")
    print(f"\nQuery: {query}")
    print("Processing...")
    
    try:
        response = query_engine.handle_query(query)
        
        print("\n" + "="*50)
        print("RESPONSE")
        print("="*50)
        
        if isinstance(response, dict):
            # If response is a dictionary, format it nicely
            if 'response' in response:
                print(response['response'])
            elif 'answer' in response:
                print(response['answer'])
            else:
                for key, value in response.items():
                    print(f"{key}: {value}")
        else:
            # Otherwise just print the response
            print(response)
        
        print("="*50 + "\n")
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        print(f"\nError: {e}")
        print("Please check your configuration and try again.\n")


def interactive_mode(config, model_name: Optional[str] = None, provider: Optional[str] = None) -> None:
    """
    Run the VPA system in interactive mode.
    
    Parameters:
    - config: Configuration manager instance
    - model_name: Optional model name to use
    - provider: Optional provider to use
    """
    logger = logging.getLogger("vpa_app")
    
    # Initialize VPA system
    try:
        query_engine = initialize_vpa_system(config, model_name, provider)
    except Exception as e:
        print(f"Failed to initialize VPA system: {e}")
        return
    
    print("\n" + "="*60)
    print("VPA INTERACTIVE MODE - REFACTORED")
    print("="*60)
    print(f"Provider: {config.LLM_PROVIDER}")
    print(f"Model: {config.get_llm_model()}")
    print(f"Memory: {config.MEMORY_DB_PATH}")
    print("\nCommands:")
    print("  'exit' or 'quit' - Exit the application")
    print("  'model NAME' - Switch to a different model")
    print("  'provider NAME' - Switch provider (openai/ollama)")
    print("  'ticker SYMBOL' - Set analysis context")
    print("  'config' - Show current configuration")
    print("  'validate' - Validate current configuration")
    print("  'clear' - Clear conversation memory")
    print("="*60 + "\n")
    
    current_ticker = None
    
    while True:
        # Show prompt with current ticker if set
        if current_ticker:
            prompt = f"[{current_ticker}] VPA> "
        else:
            prompt = "VPA> "
        
        # Get user input
        try:
            user_input = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        
        # Check for exit command
        if user_input.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        
        # Check for model switch command
        if user_input.lower().startswith('model '):
            new_model = user_input[6:].strip()
            if new_model:
                logger.info(f"Switching to model: {new_model}")
                print(f"Switching to model: {new_model}")
                try:
                    query_engine = initialize_vpa_system(config, model_name=new_model)
                    print(f"Now using model: {config.get_llm_model()}")
                except Exception as e:
                    print(f"Error switching model: {e}")
            continue
        
        # Check for provider switch command
        if user_input.lower().startswith('provider '):
            new_provider = user_input[9:].strip().lower()
            if new_provider in ['openai', 'ollama']:
                logger.info(f"Switching to provider: {new_provider}")
                print(f"Switching to provider: {new_provider}")
                try:
                    query_engine = initialize_vpa_system(config, provider=new_provider)
                    print(f"Now using provider: {config.LLM_PROVIDER}")
                except Exception as e:
                    print(f"Error switching provider: {e}")
            else:
                print("Invalid provider. Use 'openai' or 'ollama'")
            continue
        
        # Check for ticker command
        if user_input.lower().startswith('ticker '):
            new_ticker = user_input[7:].strip().upper()
            if new_ticker:
                current_ticker = new_ticker
                logger.info(f"Setting ticker context: {current_ticker}")
                print(f"Context set to ticker: {current_ticker}")
            else:
                current_ticker = None
                print("Ticker context cleared")
            continue
        
        # Check for config command
        if user_input.lower() == 'config':
            status = query_engine.get_configuration_status()
            print("\nCurrent Configuration:")
            for key, value in status.items():
                if key != 'validation_results':
                    print(f"  {key}: {value}")
            continue
        
        # Check for validate command
        if user_input.lower() == 'validate':
            validate_configuration(config)
            continue
        
        # Check for clear command
        if user_input.lower() == 'clear':
            try:
                # Clear memory by reinitializing
                query_engine.memory = MemoryManager(db_path=config.MEMORY_DB_PATH)
                query_engine.memory.add_system_message(
                    "You are a world-class financial analyst specializing in Volume-Price Analysis (VPA) and the Wyckoff Method. "
                    "You provide clear, structured, and insightful analysis. You must use the provided tools to answer user questions. "
                    "When asked to analyze a ticker, use 'get_full_analysis'. When asked to explain a concept, use 'explain_vpa_wyckoff_concept'."
                )
                print("Conversation memory cleared.")
            except Exception as e:
                print(f"Error clearing memory: {e}")
            continue
        
        # Skip empty input
        if not user_input:
            continue
        
        # Process query
        try:
            # Add ticker context to query if set
            if current_ticker and current_ticker.lower() not in user_input.lower():
                query = f"{user_input} for {current_ticker}"
                print(f"Processing: {query}")
            else:
                query = user_input
            
            response = query_engine.handle_query(query)
            
            print("\n" + "-"*50)
            if isinstance(response, dict):
                # If response is a dictionary, format it nicely
                if 'response' in response:
                    print(response['response'])
                elif 'answer' in response:
                    print(response['answer'])
                else:
                    for key, value in response.items():
                        print(f"{key}: {value}")
            else:
                # Otherwise just print the response
                print(response)
            print("-"*50 + "\n")
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"Error: {e}")
            print("Please check your configuration or try a different query.\n")


def main() -> int:
    """Main function."""
    # Parse command line arguments first
    args = parse_args()
    logger = get_logger(module_name="MarketflowApp")
    
    # Initialize configuration
    try:
        config = get_marketflow_config_manager(args.config)
    except Exception as e:
        print(f"Error initializing configuration: {e}")
        return 1
    
    # Override log level if debug is enabled
    if args.debug:
        config.set_config_value('log_level', 'DEBUG')
    
    # Set up logging
    logger = setup_logging(config)
    logger.info("Starting Marketflow application (refactored version)")

    # Handle --validate-config
    if args.validate_config:
        is_valid = validate_configuration(config)
        return 0 if is_valid else 1
    
    # Handle --list-models
    if args.list_models:
        list_available_models(config)
        return 0
    
    # If model specified, update configuration
    if args.model:
        logger.info(f"Setting model from command line: {args.model}")
        config.set_llm_model(args.model)
    
    # If provider specified, update configuration
    if args.provider:
        logger.info(f"Setting provider from command line: {args.provider}")
        config.set_config_value('llm_provider', args.provider.lower())
    
    # Handle --save-config
    if args.save_config:
        try:
            logger.info("Saving configuration")
            config.save_config()
            print("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            print(f"Error saving configuration: {e}")
            return 1
    
    # Validate configuration before proceeding
    validation_results = config.validate_configuration()
    critical_issues = []
    
    # Check for critical configuration issues
    if not validation_results.get('llm_provider_config', False):
        critical_issues.append("LLM provider configuration is invalid")
    
    if config.LLM_PROVIDER == 'openai' and not validation_results.get('openai_api_key', False):
        critical_issues.append("OpenAI API key is missing or invalid")
    
    if critical_issues:
        print("Critical configuration issues found:")
        for issue in critical_issues:
            print(f"  ✗ {issue}")
        print("\nPlease fix these issues before proceeding.")
        print("Use --validate-config to check your configuration.")
        return 1
    
    # Handle --query
    if args.query:
        process_single_query(args.query, args.ticker, config, args.model, args.provider)
        return 0
    
    # If no specific command, run in interactive mode
    interactive_mode(config, args.model, args.provider)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
