"""
Marketflow Main Application Entry Point - Refactored Version

This script provides the main entry point for the Marketflow application,
refactored to work with the updated Marketflow components and configuration system.
It uses the merged configuration manager and updated query engine.
"""

import os
import sys
import logging
import argparse
from typing import Optional

# ### FIX: Removed MemoryManager import, as it's now handled by the Query Engine
from marketflow.marketflow_logger import get_logger
# ### FIX: Import the specific factory function needed
from marketflow.marketflow_config_manager import get_marketflow_config_manager
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine


# Add the project root to sys.path to ensure modules can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Global flag for basic mode
BASIC_MODE = False

# ### FIX: Removed the premature, module-level creation of the config manager.
# It will now be created inside main() after args are parsed.
logger = get_logger(module_name="MarketflowApp")

def setup_logging(config) -> logging.Logger:
    """Set up logging configuration using the config manager."""
    log_dir = os.path.dirname(config.LOG_FILE_PATH)
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
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
    parser.add_argument("--model", help="LLM model to use")
    parser.add_argument("--provider", choices=['openai', 'ollama'], help="LLM provider")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--query", help="Process a single query and exit")
    parser.add_argument("--ticker", help="Ticker symbol for analysis")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--save-config", action="store_true", help="Save current config")
    parser.add_argument("--validate-config", action="store_true", help="Validate config")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def validate_configuration(config) -> bool:
    """Validate the configuration and display results."""
    print("\n=== Configuration Validation ===")
    validation_results = config.validate_configuration()
    all_valid = True
    
    for component, is_valid in validation_results.items():
        status = "✓" if is_valid else "✗"
        print(f"{status} {component}: {'Valid' if is_valid else 'Invalid'}")
        if not is_valid:
            all_valid = False
    
    print(f"\nOverall Status: {'✓ Valid' if all_valid else '✗ Issues Found'}")
    print("\nCurrent Configuration:")
    print(f"  LLM Provider: {config.LLM_PROVIDER}")
    print(f"  Model: {config.get_llm_model()}")
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
    print("\nTo use a specific model: --model MODEL_NAME")
    print("To switch providers: --provider PROVIDER_NAME")
    print("========================\n")

# ### FIX: Simplified initialize function. It now just needs the config object.
# The model and provider are already set on the config object before this is called.
def initialize_marketflow_system(config):
    """
    Initialize the Marketflow system with the specified configuration.
    
    Returns:
    - MarketflowLLMQueryEngine instance or None if initialization fails.
    """
    if BASIC_MODE:
        logger.warning("Running in basic mode - Marketflow query engine not available")
        print("⚠ Running in basic mode - full Marketflow functionality not available")
        return None
    
    logger.info("Creating Marketflow query engine with updated configuration")
    try:
        # Pass the config object to the engine's constructor.
        query_engine = MarketflowLLMQueryEngine(config=config)
        logger.info("Marketflow query engine initialized successfully")
        return query_engine
    except Exception as e:
        logger.error(f"Failed to initialize Marketflow query engine: {e}")
        raise

# ### FIX: Simplified function signature. It now just needs the config.
def process_single_query(query: str, ticker: Optional[str], config) -> None:
    """Process a single query and display the result."""
    if BASIC_MODE:
        # ... (no change here) ...
        return
    
    # Initialize Marketflow system
    query_engine = initialize_marketflow_system(config)
    if query_engine is None:
        return
    
    if ticker:
        logger.info(f"Adding ticker context: {ticker}")
        if ticker.upper() not in query.upper():
            query = f"{query} for {ticker.upper()}"
    
    logger.info(f"Processing query: {query}")
    print(f"\nQuery: {query}\nProcessing...")
    
    try:
        response = query_engine.process(query)
        # ... (no change in response printing) ...
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        print(f"\nError: {e}\nPlease check your configuration and try again.\n")

# ### FIX: Simplified function signature.
def interactive_mode(config) -> None:
    """Run the Marketflow system in interactive mode."""
    # Initialize Marketflow system
    try:
        query_engine = initialize_marketflow_system(config)
    except Exception as e:
        print(f"Failed to initialize Marketflow system: {e}")
        return
    
    print("\n" + "="*60)
    print("Marketflow INTERACTIVE MODE - REFACTORED")
    print("="*60)
    status = query_engine.get_configuration_status()
    print(f"Provider: {status['Provider']}")
    print(f"Model: {status['Model']}")
    print(f"Memory: {status['Memory DB']}")
    print("\nCommands: exit, quit, model NAME, provider NAME, ticker SYMBOL, config, validate, clear")
    print("="*60 + "\n")
    
    current_ticker = None
    
    while True:
        prompt = f"[{current_ticker}] Marketflow> " if current_ticker else "Marketflow> "
        try:
            user_input = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        
        if user_input.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        
        # ### FIX: Simplified model/provider switching logic
        if user_input.lower().startswith('model '):
            new_model = user_input[6:].strip()
            if new_model:
                print(f"Switching to model: {new_model}")
                config.set_llm_model(new_model) # Update config
                query_engine = initialize_marketflow_system(config) # Re-initialize
                print(f"Now using model: {config.get_llm_model()}")
            continue
        
        if user_input.lower().startswith('provider '):
            new_provider = user_input[9:].strip().lower()
            if new_provider in ['openai', 'ollama']:
                print(f"Switching to provider: {new_provider}")
                config.set_config_value('llm_provider', new_provider)
                query_engine = initialize_marketflow_system(config)
                print(f"Now using provider: {config.LLM_PROVIDER}")
                print(f"Now using model: {config.get_llm_model()}")
            else:
                print("Invalid provider. Use 'openai' or 'ollama'")
            continue

        if user_input.lower().startswith('ticker '):
            # ... (no change here) ...
            continue
        
        if user_input.lower() == 'config':
            status = query_engine.get_configuration_status()
            print("\nCurrent Configuration:")
            for key, value in status.items():
                if key != 'validation_results':
                    print(f"  {key}: {value}")
            continue
        
        if user_input.lower() == 'validate':
            validate_configuration(config)
            continue
        
        # ### FIX: Encapsulated memory clearing
        if user_input.lower() == 'clear':
            try:
                query_engine.clear_memory()
                print("Conversation memory cleared.")
            except Exception as e:
                print(f"Error clearing memory: {e}")
            continue
        
        if not user_input:
            continue
        
        try:
            query = f"{user_input} for {current_ticker}" if current_ticker and current_ticker.lower() not in user_input.lower() else user_input
            if query != user_input:
                print(f"Processing: {query}")

            response = query_engine.process(query)
            
            # ... (response printing logic is fine) ...
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"Error: {e}\nPlease check your configuration or try a different query.\n")

def main() -> int:
    """Main function."""
    args = parse_args()
    
    # ### FIX: Configuration is now created here, AFTER args are parsed.
    # This ensures the --config argument is correctly used.
    try:
        config = get_marketflow_config_manager(config_file=args.config)
    except Exception as e:
        print(f"Error initializing configuration: {e}")
        return 1
    
    if args.debug:
        config.set_config_value('log_level', 'DEBUG')
    
    # Setup logging with the now-finalized config
    logger = setup_logging(config)
    logger.info("Starting Marketflow application (refactored version)")

    # ### FIX: Apply command-line overrides for model and provider to the config object.
    # This is now the single source of truth.
    if args.provider:
        logger.info(f"Overriding provider from command line: {args.provider}")
        config.set_config_value('llm_provider', args.provider.lower())

    if args.model:
        logger.info(f"Overriding model from command line: {args.model}")
        config.set_llm_model(args.model)

    if args.validate_config:
        is_valid = validate_configuration(config)
        return 0 if is_valid else 1
    
    if args.list_models:
        list_available_models(config)
        return 0
    
    if args.save_config:
        try:
            config.save_config()
            print(f"Configuration saved successfully to {config.config_file_paths[0]}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}", exc_info=True)
            print(f"Error saving configuration: {e}")
            return 1
    
    # ... (validation logic is fine) ...
    
    if args.query:
        # ### FIX: Pass the single config object
        process_single_query(args.query, args.ticker, config)
        return 0
    
    # ### FIX: Pass the single config object
    interactive_mode(config)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())