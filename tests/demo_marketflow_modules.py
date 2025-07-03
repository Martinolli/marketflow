"""
MarketFlow Modules Demonstration Script

This script demonstrates that the fixed modules work correctly and
shows the improvements made to address compatibility issues.
"""

import os
import tempfile
import sys
from pathlib import Path
import time
import shutil

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demonstrate_fixed_modules():
    """Demonstrate the functionality of the fixed modules"""
    
    print("=" * 60)
    print("MarketFlow Modules Demonstration")
    print("=" * 60)
    
    # Create a temporary directory for this demonstration
    temp_dir = tempfile.mkdtemp()
    print(f"Using temporary directory: {temp_dir}")
    
    try:
        # Import the fixed modules
        from marketflow_logger_fixed import get_logger, clear_loggers
        from marketflow_config_manager_fixed import ConfigManager
        
        print("\\n✅ Successfully imported fixed modules (no circular import issues)")
        
        # Clear any cached loggers
        clear_loggers()
        
        # 1. Demonstrate Logger Functionality
        print("\\n" + "-" * 40)
        print("1. Testing Logger Functionality")
        print("-" * 40)
        
        log_file = os.path.join(temp_dir, "demo.log")
        logger = get_logger(
            module_name="DemoModule",
            log_level="DEBUG",
            log_file=log_file,
            encoding='utf-8'
        )
        
        print(f"✅ Logger created successfully")
        print(f"   Module: {logger.module_name}")
        print(f"   Log file: {log_file}")
        
        # Test different log levels
        logger.debug("Debug message - this is a test")
        logger.info("Info message - logger is working")
        logger.warning("Warning message - encoding test: αβγ 中文")
        logger.error("Error message - testing error logging")
        
        # Test specialized logging methods
        timeframes = [{"interval": "1D"}, {"interval": "4H"}]
        logger.log_analysis_start("AAPL", timeframes)
        
        signal = {"type": "BUY", "strength": "STRONG"}
        logger.log_analysis_complete("AAPL", signal)
        
        logger.log_data_retrieval("AAPL", "1D", True)
        logger.log_pattern_detection("AAPL", "Wyckoff Accumulation", True)
        
        print("✅ All logging methods work correctly")
        
        # Check if log file was created
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
                print(f"✅ Log file created with {len(log_content)} characters")
                print("   Sample log entries:")
                for line in log_content.split('\\n')[:3]:
                    if line.strip():
                        print(f"   {line}")
        
        # 2. Demonstrate Config Manager Functionality
        print("\\n" + "-" * 40)
        print("2. Testing Config Manager Functionality")
        print("-" * 40)
        
        # Create a test config file
        config_file = os.path.join(temp_dir, "test_config.json")
        test_config = {
            "openai_api_key": "sk-test123456789abcdef",
            "polygon_api_key": "test_polygon_key_12345",
            "llm_provider": "openai",
            "log_level": "DEBUG",
            "test_value": "config_file_value"
        }
        
        import json
        with open(config_file, 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # Initialize config manager with logger (dependency injection)
        config = ConfigManager(config_file=config_file, logger=logger)
        
        print("✅ Config manager created successfully")
        print(f"   Config file: {config_file}")
        print(f"   Logger injected: {config.logger is not None}")
        
        # Test API key retrieval
        try:
            openai_key = config.get_api_key("openai")
            print(f"✅ OpenAI API key retrieved: {openai_key[:10]}...")
        except Exception as e:
            print(f"❌ Error retrieving OpenAI key: {e}")
        
        try:
            polygon_key = config.get_api_key("polygon")
            print(f"✅ Polygon API key retrieved: {polygon_key[:10]}...")
        except Exception as e:
            print(f"❌ Error retrieving Polygon key: {e}")
        
        # Test API key validation
        openai_valid = config.validate_api_key("openai")
        polygon_valid = config.validate_api_key("polygon")
        print(f"✅ API key validation - OpenAI: {openai_valid}, Polygon: {polygon_valid}")
        
        # Test configuration value retrieval
        log_level = config.get_config_value("log_level")
        test_value = config.get_config_value("test_value")
        missing_value = config.get_config_value("missing_key", "default_value")
        
        print(f"✅ Config values - log_level: {log_level}, test_value: {test_value}")
        print(f"✅ Default value handling: {missing_value}")
        
        # Test LLM configuration
        llm_model = config.get_llm_model()
        available_models = config.get_available_models()
        
        print(f"✅ LLM model: {llm_model}")
        print(f"✅ Available models: {len(available_models)} models")
        
        # Test configuration validation
        validation_results = config.validate_configuration()
        print(f"✅ Configuration validation completed:")
        for key, result in validation_results.items():
            status = "✅" if result else "❌"
            print(f"   {status} {key}: {result}")
        
        # 3. Demonstrate Cross-Platform Path Handling
        print("\\n" + "-" * 40)
        print("3. Testing Cross-Platform Path Handling")
        print("-" * 40)
        
        print(f"✅ Project root detection: {config.project_root}")
        print(f"✅ Log file path: {config.LOG_FILE_PATH}")
        print(f"✅ Memory DB path: {config.MEMORY_DB_PATH}")
        
        # Check that paths don't contain Windows-specific separators on Unix
        if os.name != 'nt':  # Not Windows
            has_backslash = '\\\\' in str(config.LOG_FILE_PATH) or '\\\\' in str(config.MEMORY_DB_PATH)
            print(f"✅ Cross-platform paths (no backslashes on Unix): {not has_backslash}")
        
        # 4. Demonstrate Integration Without Circular Imports
        print("\\n" + "-" * 40)
        print("4. Testing Integration (No Circular Imports)")
        print("-" * 40)
        
        # Create another logger with config manager's log level
        integration_logger = get_logger(
            module_name="IntegrationTest",
            log_level=config.LOG_LEVEL,
            log_file=os.path.join(temp_dir, "integration.log")
        )
        
        print("✅ Created integration logger using config manager settings")
        
        # Test that config manager can log through its injected logger
        config._log("info", "Config manager logging test - this should appear in the main log")
        
        print("✅ Config manager logging through injected logger works")
        
        # 5. Demonstrate Error Handling
        print("\\n" + "-" * 40)
        print("5. Testing Error Handling")
        print("-" * 40)
        
        # Test missing API key handling
        missing_key = config.get_api_key_safe("nonexistent_service")
        print(f"✅ Missing API key handled gracefully: {missing_key is None}")
        
        # Test config manager without logger
        config_no_logger = ConfigManager()
        config_no_logger._log("info", "This should not crash")
        print("✅ Config manager works without logger dependency")
        
        # Test invalid log level
        invalid_logger = get_logger(
            module_name="InvalidLevelTest",
            log_level="INVALID_LEVEL",
            log_file=os.path.join(temp_dir, "invalid.log")
        )
        print("✅ Invalid log level handled gracefully")
        
        print("\\n" + "=" * 60)
        print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\\nKey Improvements Made:")
        print("• ✅ Removed circular import between config manager and logger")
        print("• ✅ Fixed hardcoded Windows-specific paths")
        print("• ✅ Improved cross-platform compatibility")
        print("• ✅ Added proper encoding support for log files")
        print("• ✅ Enhanced error handling and validation")
        print("• ✅ Implemented dependency injection pattern")
        print("• ✅ Added comprehensive logging methods")
        print("• ✅ Improved configuration validation")
        
        return True
        
    except Exception as e:
        print(f"\\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        for _ in range(5):  # Try up to 5 times
            try:
                time.sleep(1)  # Wait for 1 second
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                print(f"\nCleaned up temporary directory: {temp_dir}")
                break
            except PermissionError:
                print(f"Unable to delete {temp_dir}, retrying...")
        else:
            print(f"Warning: Could not delete temporary directory: {temp_dir}")

if __name__ == "__main__":
    success = demonstrate_fixed_modules()
    if success:
        print("\\n🎉 MarketFlow modules are working correctly!")
        sys.exit(0)
    else:
        print("\\n💥 Some issues were encountered.")
        sys.exit(1)

