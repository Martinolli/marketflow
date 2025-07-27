import pytest
import os
import json
import tempfile
from unittest.mock import Mock, patch, mock_open, MagicMock
from datetime import datetime
from scripts.marketflow_analysis_llm_interface import run_analysis

class TestRunAnalysis:
    
    @pytest.fixture
    def mock_dependencies(self):
        """Setup mocks for all dependencies."""
        with patch('scripts.marketflow_analysis_llm_interface.MarketflowFacade') as mock_facade_class, \
             patch('scripts.marketflow_analysis_llm_interface.MarketflowResultExtractor') as mock_extractor_class, \
             patch('scripts.marketflow_analysis_llm_interface.MarketflowReport') as mock_report_class, \
             patch('scripts.marketflow_analysis_llm_interface.MarketflowLLMInterface') as mock_llm_class, \
             patch('scripts.marketflow_analysis_llm_interface.create_app_config') as mock_config_func, \
             patch('scripts.marketflow_analysis_llm_interface.get_logger') as mock_logger_func, \
             patch('scripts.marketflow_analysis_llm_interface.sanitize_filename') as mock_sanitize, \
             patch('scripts.marketflow_analysis_llm_interface.os.makedirs') as mock_makedirs:
            
            # Setup mock instances
            mock_facade = Mock()
            mock_facade_class.return_value = mock_facade
            mock_facade.analyze_ticker.return_value = {"analysis": "test_data"}
            
            mock_extractor = Mock()
            mock_extractor_class.return_value = mock_extractor
            
            mock_report = Mock()
            mock_report_class.return_value = mock_report
            mock_report.generate_all_reports_for_ticker.return_value = True
            
            mock_llm = Mock()
            mock_llm_class.return_value = mock_llm
            mock_llm.get_ticker_analysis.return_value = {"llm_analysis": "test_analysis"}
            
            mock_config = Mock()
            mock_config.REPORT_DIR = "/test/reports"
            mock_config_func.return_value = mock_config
            
            mock_logger = Mock()
            mock_logger_func.return_value = mock_logger
            
            mock_sanitize.side_effect = lambda x: x.replace(":", "_")
            
            yield {
                'facade': mock_facade,
                'extractor': mock_extractor,
                'report': mock_report,
                'llm': mock_llm,
                'config': mock_config,
                'logger': mock_logger,
                'sanitize': mock_sanitize,
                'makedirs': mock_makedirs
            }

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_success_default_timeframes(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test successful analysis with default timeframes."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        
        # Execute
        run_analysis("AAPL")
        
        # Verify
        mock_dependencies['facade'].analyze_ticker.assert_called_once_with("AAPL")
        mock_dependencies['report'].generate_all_reports_for_ticker.assert_called_once_with("AAPL")
        mock_dependencies['llm'].get_ticker_analysis.assert_called_once_with("AAPL")
        mock_json_dump.assert_called_once()
        mock_file.assert_called_once()

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_success_custom_timeframes(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test successful analysis with custom timeframes."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        custom_timeframes = ["1d", "4h", "1h"]
        
        # Execute
        run_analysis("AAPL", timeframes=custom_timeframes)
        
        # Verify
        mock_dependencies['facade'].analyze_ticker.assert_called_once_with("AAPL", timeframes=custom_timeframes)

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_crypto_ticker(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test analysis with crypto ticker that needs sanitization."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/X_BTCUSD/2024-01-15_X_BTCUSD_llm_analysis.json"
        
        # Execute
        run_analysis("X:BTCUSD")
        
        # Verify
        mock_dependencies['sanitize'].assert_called_with("X:BTCUSD")
        mock_dependencies['facade'].analyze_ticker.assert_called_once_with("X:BTCUSD")
        mock_file.assert_called_once_with("/test/reports/2024-01-15/X_BTCUSD/2024-01-15_X_BTCUSD_llm_analysis.json", "w")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_report_generation_failure(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test handling when report generation fails."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        mock_dependencies['report'].generate_all_reports_for_ticker.return_value = False
        
        # Execute
        run_analysis("AAPL")
        
        # Verify - should still continue with LLM analysis despite report failure
        mock_dependencies['llm'].get_ticker_analysis.assert_called_once_with("AAPL")
        mock_json_dump.assert_called_once()

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_llm_analysis_failure(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test handling when LLM analysis fails."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        mock_dependencies['llm'].get_ticker_analysis.return_value = None
        
        # Execute
        run_analysis("AAPL")
        
        # Verify - should still try to save the None result
        mock_json_dump.assert_called_once_with(None, mock_file.return_value.__enter__.return_value, indent=4)

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_json_serialization_error(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test handling of JSON serialization errors (like SignalType objects)."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        mock_json_dump.side_effect = TypeError("Object of type SignalType is not JSON serializable")
        
        # Execute & Verify - should raise the TypeError
        with pytest.raises(TypeError, match="Object of type SignalType is not JSON serializable"):
            run_analysis("AAPL")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_file_operations(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test file operations and path handling."""
        # Setup
        test_date = "2024-01-15"
        test_ticker = "AAPL"
        expected_path = f"/test/reports/{test_date}/{test_ticker}/{test_date}_{test_ticker}_llm_analysis.json"
        
        mock_datetime.now.return_value.strftime.return_value = test_date
        mock_path_join.return_value = expected_path
        
        # Execute
        run_analysis(test_ticker)
        
        # Verify
        mock_path_join.assert_called_once_with(f"/test/reports/{test_date}/{test_ticker}", f"{test_date}_{test_ticker}_llm_analysis.json")
        mock_file.assert_called_once_with(expected_path, "w")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    def test_run_analysis_facade_error(self, mock_datetime, mock_dependencies):
        """Test handling when MarketflowFacade raises an exception."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_dependencies['facade'].analyze_ticker.side_effect = Exception("Facade error")
        
        # Execute & Verify
        with pytest.raises(Exception, match="Facade error"):
            run_analysis("AAPL")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_with_custom_output_dir(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test analysis with custom output directory."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        custom_output = "/custom/output"
        
        # Execute
        run_analysis("AAPL", output_dir=custom_output)
        
        # Verify - should still use config REPORT_DIR, not the passed output_dir
        # (based on the code logic where output_dir is overridden)
        mock_dependencies['facade'].analyze_ticker.assert_called_once_with("AAPL")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open')
    def test_run_analysis_file_write_error(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test handling when file write operations fail."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        mock_file.side_effect = IOError("Permission denied")
        
        # Execute & Verify
        with pytest.raises(IOError, match="Permission denied"):
            run_analysis("AAPL")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_empty_timeframes(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test analysis with empty timeframes list."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        
        # Execute
        run_analysis("AAPL", timeframes=[])
        
        # Verify - empty list is falsy in Python, so it uses default behavior
        mock_dependencies['facade'].analyze_ticker.assert_called_once_with("AAPL")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_none_timeframes(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test analysis with None timeframes (explicit test for None)."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        
        # Execute
        run_analysis("AAPL", timeframes=None)
        
        # Verify - None timeframes should use default behavior
        mock_dependencies['facade'].analyze_ticker.assert_called_once_with("AAPL")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_llm_interface_creation_error(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test handling when LLM interface creation fails."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        
        # Mock the LLM interface class to raise an exception on instantiation
        with patch('scripts.marketflow_analysis_llm_interface.MarketflowLLMInterface') as mock_llm_class:
            mock_llm_class.side_effect = Exception("LLM service unavailable")
            
            # Execute & Verify
            with pytest.raises(Exception, match="LLM service unavailable"):
                run_analysis("AAPL")

    @patch('scripts.marketflow_analysis_llm_interface.datetime')
    @patch('scripts.marketflow_analysis_llm_interface.os.path.join')
    @patch('scripts.marketflow_analysis_llm_interface.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_analysis_directory_creation_verification(self, mock_file, mock_json_dump, mock_path_join, mock_datetime, mock_dependencies):
        """Test that the necessary directories exist or are created."""
        # Setup
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_path_join.return_value = "/test/reports/2024-01-15/AAPL/2024-01-15_AAPL_llm_analysis.json"
        
        # Execute
        run_analysis("AAPL")
        
        # Verify that makedirs was called for the output directory
        expected_output_dir = "/test/reports/2024-01-15/AAPL"
        mock_dependencies['makedirs'].assert_called()