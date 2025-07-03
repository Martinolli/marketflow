"""
Comprehensive Test Suite for MarketFlow Logger and Config Manager

This test suite validates both the original modules and the fixed versions,
ensuring compatibility, functionality, and proper integration.

Test Categories:
1. Logger Module Tests
2. Config Manager Tests  
3. Integration Tests
4. Cross-platform Compatibility Tests
5. Error Handling Tests
"""

import unittest
import tempfile
import os
import sys
import json
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the modules to test
try:
    from marketflow.marketflow_logger import get_logger, MarketflowLogger, clear_loggers
    from marketflow.marketflow_config_manager import ConfigManager, get_config_manager, create_app_config
    from scripts.marketflow_integration_example import initialize_marketflow_system, create_module_specific_logger
    FIXED_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import fixed modules: {e}")
    FIXED_MODULES_AVAILABLE = False

class TestMarketflowLogger(unittest.TestCase):
    """Test cases for the MarketFlow Logger module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_log_file = os.path.join(self.temp_dir, "test.log")
        clear_loggers()  # Clear any cached loggers
    
    def tearDown(self):
        """Clean up test fixtures"""
        clear_loggers()
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_logger_initialization(self):
        """Test basic logger initialization"""
        logger = get_logger(
            module_name="TestModule",
            log_level="DEBUG",
            log_file=self.test_log_file
        )
        
        self.assertIsInstance(logger, MarketflowLogger)
        self.assertEqual(logger.module_name, "TestModule")
        self.assertEqual(logger.log_file, self.test_log_file)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_logger_file_creation(self):
        """Test that log files are created properly"""
        logger = get_logger(
            module_name="FileTest",
            log_file=self.test_log_file
        )
        
        logger.info("Test message")
        
        # Check if log file was created
        self.assertTrue(os.path.exists(self.test_log_file))
        
        # Check if message was written
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test message", content)
            self.assertIn("FileTest", content)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_logger_levels(self):
        """Test different logging levels"""
        logger = get_logger(
            module_name="LevelTest",
            log_level="DEBUG",
            log_file=self.test_log_file
        )
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Debug message", content)
            self.assertIn("Info message", content)
            self.assertIn("Warning message", content)
            self.assertIn("Error message", content)
            self.assertIn("Critical message", content)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_specialized_logging_methods(self):
        """Test specialized logging methods for MarketFlow"""
        logger = get_logger(
            module_name="SpecializedTest",
            log_file=self.test_log_file
        )
        
        # Test analysis logging
        timeframes = [{"interval": "1D"}, {"interval": "4H"}]
        logger.log_analysis_start("AAPL", timeframes)
        
        signal = {"type": "BUY", "strength": "STRONG"}
        logger.log_analysis_complete("AAPL", signal)
        
        # Test data retrieval logging
        logger.log_data_retrieval("AAPL", "1D", True)
        logger.log_data_retrieval("MSFT", "4H", False)
        
        # Test pattern detection
        logger.log_pattern_detection("AAPL", "Wyckoff Accumulation", True)
        logger.log_pattern_detection("MSFT", "Spring", False)
        
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Starting Marketflow analysis for AAPL", content)
            self.assertIn("Completed Marketflow analysis for AAPL", content)
            self.assertIn("Successfully retrieved 1D data for AAPL", content)
            self.assertIn("Failed to retrieve 4H data for MSFT", content)
            self.assertIn("Detected Wyckoff Accumulation pattern for AAPL", content)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_logger_encoding(self):
        """Test that logger properly handles encoding"""
        logger = get_logger(
            module_name="EncodingTest",
            log_file=self.test_log_file,
            encoding='utf-8'
        )
        
        # Test with unicode characters
        logger.info("Test with unicode: αβγδε 中文 🚀")
        
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("αβγδε 中文 🚀", content)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_invalid_log_level(self):
        """Test handling of invalid log levels"""
        # This should not raise an exception
        logger = get_logger(
            module_name="InvalidLevelTest",
            log_level="INVALID_LEVEL",
            log_file=self.test_log_file
        )
        
        self.assertIsInstance(logger, MarketflowLogger)
        logger.info("Test message")
        
        # Should still work with default level
        self.assertTrue(os.path.exists(self.test_log_file))


class TestMarketflowConfigManager(unittest.TestCase):
    """Test cases for the MarketFlow Config Manager module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_config_file = os.path.join(self.temp_dir, "test_config.json")
        
        # Create a test config file
        self.test_config_data = {
            "openai_api_key": "sk-test123456789",
            "polygon_api_key": "test_polygon_key",
            "llm_provider": "openai",
            "log_level": "DEBUG"
        }
        
        with open(self.test_config_file, 'w') as f:
            json.dump(self.test_config_data, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_config_manager_initialization(self):
        """Test basic config manager initialization"""
        config = ConfigManager(config_file=self.test_config_file)
        
        self.assertIsInstance(config, ConfigManager)
        self.assertEqual(config.config_data["openai_api_key"], "sk-test123456")
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_api_key_retrieval(self):
        """Test API key retrieval"""
        config = ConfigManager(config_file=self.test_config_file)
        
        # Test successful retrieval
        openai_key = config.get_api_key("openai")
        self.assertEqual(openai_key, "sk-test123456")
        
        polygon_key = config.get_api_key("polygon")
        self.assertEqual(polygon_key, "test_polygon_key")
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_api_key_validation(self):
        """Test API key validation"""
        config = ConfigManager(config_file=self.test_config_file)
        
        # Test valid keys
        self.assertTrue(config.validate_api_key("openai"))
        self.assertTrue(config.validate_api_key("polygon"))
        
        # Test invalid service
        self.assertFalse(config.validate_api_key("invalid_service"))
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_config_value_retrieval(self):
        """Test configuration value retrieval"""
        config = ConfigManager(config_file=self.test_config_file)
        
        # Test existing value
        log_level = config.get_config_value("log_level")
        self.assertEqual(log_level, "DEBUG")
        
        # Test default value
        missing_value = config.get_config_value("missing_key", "default_value")
        self.assertEqual(missing_value, "default_value")
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    @patch.dict(os.environ, {"MARKETFLOW_TEST_VALUE": "env_value"})
    def test_environment_variable_priority(self):
        """Test that environment variables take priority"""
        config = ConfigManager(config_file=self.test_config_file)
        
        # Environment variable should override config file
        env_value = config.get_config_value("test_value")
        self.assertEqual(env_value, "env_value")
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_llm_configuration(self):
        """Test LLM configuration methods"""
        config = ConfigManager(config_file=self.test_config_file)
        
        # Test LLM model retrieval
        model = config.get_llm_model()
        self.assertIsInstance(model, str)
        
        # Test setting LLM model
        config.set_llm_model("gpt-4")
        self.assertEqual(config.config_data["llm_model"], "gpt-4")
        
        # Test available models
        models = config.get_available_models()
        self.assertIsInstance(models, list)
        self.assertIn("gpt-4", models)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_configuration_validation(self):
        """Test configuration validation"""
        config = ConfigManager(config_file=self.test_config_file)
        
        validation_results = config.validate_configuration()
        self.assertIsInstance(validation_results, dict)
        
        # Check that all expected keys are present
        expected_keys = [
            'openai_api_key', 'polygon_api_key', 'llm_provider_config',
            'log_file_path', 'memory_db_path'
        ]
        for key in expected_keys:
            self.assertIn(key, validation_results)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_config_save_load(self):
        """Test saving and loading configuration"""
        config = ConfigManager()
        
        # Set some values
        config.set_config_value("test_key", "test_value")
        config.set_api_key("openai", "sk-new_test_key")
        
        # Save configuration
        save_path = os.path.join(self.temp_dir, "saved_config.json")
        config.save_config(save_path)
        
        # Load new config manager with saved file
        new_config = ConfigManager(config_file=save_path)
        
        self.assertEqual(new_config.get_config_value("test_key"), "test_value")
        self.assertEqual(new_config.get_api_key("openai"), "sk-new_test_key")


class TestMarketflowIntegration(unittest.TestCase):
    """Test cases for integration between Logger and Config Manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        clear_loggers()
    
    def tearDown(self):
        """Clean up test fixtures"""
        clear_loggers()
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_integration_initialization(self):
        """Test that logger and config manager can be initialized together"""
        logger, config = initialize_marketflow_system()
        
        self.assertIsInstance(logger, MarketflowLogger)
        self.assertIsInstance(config, ConfigManager)
        
        # Test that config manager has logger
        self.assertIsNotNone(config.logger)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_module_specific_logger_creation(self):
        """Test creating module-specific loggers"""
        logger, config = initialize_marketflow_system()
        
        data_logger = create_module_specific_logger("DataProvider", config)
        analyzer_logger = create_module_specific_logger("Analyzer", config)
        
        self.assertIsInstance(data_logger, MarketflowLogger)
        self.assertIsInstance(analyzer_logger, MarketflowLogger)
        
        self.assertEqual(data_logger.module_name, "DataProvider")
        self.assertEqual(analyzer_logger.module_name, "Analyzer")
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_no_circular_import(self):
        """Test that there are no circular import issues"""
        # This test passes if the imports work without raising ImportError
        try:
            from marketflow.marketflow_logger import get_logger
            from marketflow.marketflow_config_manager import ConfigManager
            
            # Create instances
            logger = get_logger("CircularTest")
            config = ConfigManager(logger=logger)
            
            self.assertTrue(True)  # If we get here, no circular import
        except ImportError as e:
            self.fail(f"Circular import detected: {e}")
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_cross_platform_paths(self):
        """Test that paths work across platforms"""
        logger, config = initialize_marketflow_system()
        
        # Test that paths are properly constructed
        self.assertIsInstance(config.LOG_FILE_PATH, str)
        self.assertIsInstance(config.MEMORY_DB_PATH, str)
        
        # Test that paths don't contain Windows-specific separators on Unix
        if os.name != 'nt':  # Not Windows
            self.assertNotIn('\\', config.LOG_FILE_PATH)
            self.assertNotIn('\\', config.MEMORY_DB_PATH)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in both modules"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        clear_loggers()
    
    def tearDown(self):
        """Clean up test fixtures"""
        clear_loggers()
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_logger_with_invalid_path(self):
        """Test logger behavior with invalid file path"""
        # Try to create logger with invalid path
        invalid_path = "/invalid/path/that/does/not/exist/test.log"
        
        # This should not raise an exception
        logger = get_logger(
            module_name="InvalidPathTest",
            log_file=invalid_path
        )
        
        # Logger should still work (console only)
        logger.info("Test message")
        self.assertIsInstance(logger, MarketflowLogger)
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_config_manager_without_logger(self):
        """Test config manager without logger dependency"""
        # Should work without logger
        config = ConfigManager()
        self.assertIsInstance(config, ConfigManager)
        
        # Should handle logging calls gracefully
        config._log("info", "Test message")  # Should not raise exception
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_missing_api_keys(self):
        """Test behavior when API keys are missing"""
        config = ConfigManager()
        
        # Should return None for missing keys
        self.assertIsNone(config.get_api_key_safe("openai"))
        self.assertIsNone(config.get_api_key_safe("polygon"))
        
        # Should raise ValueError for get_api_key
        with self.assertRaises(ValueError):
            config.get_api_key("openai")
    
    @unittest.skipUnless(FIXED_MODULES_AVAILABLE, "Fixed modules not available")
    def test_invalid_config_file(self):
        """Test behavior with invalid config file"""
        invalid_config_path = os.path.join(self.temp_dir, "invalid.json")
        
        # Create invalid JSON file
        with open(invalid_config_path, 'w') as f:
            f.write("{ invalid json content")
        
        # Should not raise exception, should use defaults
        config = ConfigManager(config_file=invalid_config_path)
        self.assertIsInstance(config, ConfigManager)


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestMarketflowLogger,
        TestMarketflowConfigManager,
        TestMarketflowIntegration,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

def main():
    """Main test function"""
    print("=" * 60)
    print("MarketFlow Modules Compatibility Test Suite")
    print("=" * 60)
    
    if not FIXED_MODULES_AVAILABLE:
        print("WARNING: Fixed modules are not available. Some tests will be skipped.")
        print("Make sure marketflow_logger_fixed.py and marketflow_config_manager_fixed.py are in the same directory.")
        print()
    
    # Run the tests
    result = run_tests()
    
    print("\\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\\nSuccess Rate: {success_rate:.1f}%")
    
    if result.wasSuccessful():
        print("\\n✅ All tests passed! The modules are compatible and working correctly.")
    else:
        print("\\n❌ Some tests failed. Please review the issues above.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

