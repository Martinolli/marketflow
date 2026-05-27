import json
from enum import Enum
from unittest.mock import Mock, call, mock_open, patch

import pytest

from scripts.marketflow_analysis_llm_interface import (
    CustomJSONEncoder,
    run_analysis,
    safe_json_dump,
)


def _normalized(path: str) -> str:
    return str(path).replace("\\", "/")


def _saved_call(mock_safe_json_dump):
    mock_safe_json_dump.assert_called_once()
    return mock_safe_json_dump.call_args.args


def _assert_saved_path(path: str, *, ticker: str, date: str = "2024-01-15") -> None:
    normalized = _normalized(path)
    assert f"/test/reports/{date}/{ticker}/" in normalized
    assert normalized.endswith(f"{ticker}_llm_analysis.json")


class TestRunAnalysis:
    @pytest.fixture
    def mock_dependencies(self):
        """Setup mocks for all run_analysis dependencies."""
        with patch("scripts.marketflow_analysis_llm_interface.MarketflowFacade") as mock_facade_class, \
             patch("scripts.marketflow_analysis_llm_interface.MarketflowResultExtractor") as mock_extractor_class, \
             patch("scripts.marketflow_analysis_llm_interface.MarketflowReport") as mock_report_class, \
             patch("scripts.marketflow_analysis_llm_interface.MarketflowLLMInterface") as mock_llm_class, \
             patch("scripts.marketflow_analysis_llm_interface.create_app_config") as mock_config_func, \
             patch("scripts.marketflow_analysis_llm_interface.sanitize_filename") as mock_sanitize, \
             patch("scripts.marketflow_analysis_llm_interface.os.makedirs") as mock_makedirs, \
             patch("scripts.marketflow_analysis_llm_interface.safe_json_dump") as mock_safe_json_dump:

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

            mock_sanitize.side_effect = lambda value: value.replace(":", "_")
            mock_safe_json_dump.return_value = True

            yield {
                "facade": mock_facade,
                "extractor_class": mock_extractor_class,
                "extractor": mock_extractor,
                "report_class": mock_report_class,
                "report": mock_report,
                "llm_class": mock_llm_class,
                "llm": mock_llm,
                "config": mock_config,
                "sanitize": mock_sanitize,
                "makedirs": mock_makedirs,
                "safe_json_dump": mock_safe_json_dump,
            }

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_success_default_timeframes(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"

        run_analysis("AAPL")

        mock_dependencies["facade"].analyze_ticker.assert_called_once_with("AAPL")
        mock_dependencies["extractor_class"].assert_called_once_with({"AAPL": {"analysis": "test_data"}})
        mock_dependencies["report"].generate_all_reports_for_ticker.assert_called_once_with("AAPL")
        mock_dependencies["llm"].get_ticker_analysis.assert_called_once_with("AAPL")
        saved_data, saved_path = _saved_call(mock_dependencies["safe_json_dump"])
        assert saved_data == {"llm_analysis": "test_analysis"}
        _assert_saved_path(saved_path, ticker="AAPL")

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_success_custom_timeframes(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        custom_timeframes = ["1d", "4h", "1h"]

        run_analysis("AAPL", timeframes=custom_timeframes)

        mock_dependencies["facade"].analyze_ticker.assert_called_once_with(
            "AAPL",
            timeframes=custom_timeframes,
        )

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_crypto_ticker(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"

        run_analysis("X:BTCUSD")

        mock_dependencies["facade"].analyze_ticker.assert_called_once_with("X:BTCUSD")
        assert mock_dependencies["sanitize"].call_args_list == [
            call("X:BTCUSD"),
            call("X:BTCUSD"),
        ]
        _, saved_path = _saved_call(mock_dependencies["safe_json_dump"])
        _assert_saved_path(saved_path, ticker="X_BTCUSD")

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_report_generation_failure(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_dependencies["report"].generate_all_reports_for_ticker.return_value = False

        run_analysis("AAPL")

        mock_dependencies["llm"].get_ticker_analysis.assert_called_once_with("AAPL")
        mock_dependencies["safe_json_dump"].assert_called_once()

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_llm_falsey_result_saves_error_dict(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_datetime.now.return_value.isoformat.return_value = "2024-01-15T12:00:00"
        mock_dependencies["llm"].get_ticker_analysis.return_value = None

        run_analysis("AAPL")

        saved_data, saved_path = _saved_call(mock_dependencies["safe_json_dump"])
        assert saved_data == {
            "error": "No LLM analysis data returned",
            "ticker": "AAPL",
            "timestamp": "2024-01-15T12:00:00",
        }
        _assert_saved_path(saved_path, ticker="AAPL")

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_llm_exception_saves_error_dict(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_datetime.now.return_value.isoformat.return_value = "2024-01-15T12:00:00"
        mock_dependencies["llm_class"].side_effect = Exception("LLM service unavailable")

        run_analysis("AAPL")

        saved_data, _ = _saved_call(mock_dependencies["safe_json_dump"])
        assert saved_data == {
            "error": "LLM interface error: LLM service unavailable",
            "ticker": "AAPL",
            "timestamp": "2024-01-15T12:00:00",
        }

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_file_operations(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"

        run_analysis("AAPL")

        _, saved_path = _saved_call(mock_dependencies["safe_json_dump"])
        _assert_saved_path(saved_path, ticker="AAPL")
        mock_dependencies["makedirs"].assert_called_once()
        makedirs_path = _normalized(mock_dependencies["makedirs"].call_args.args[0])
        assert makedirs_path.endswith("/test/reports/2024-01-15/AAPL")

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_facade_error(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_dependencies["facade"].analyze_ticker.side_effect = Exception("Facade error")

        with pytest.raises(Exception, match="Facade error"):
            run_analysis("AAPL")

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_with_custom_output_dir_uses_config_report_dir(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"

        run_analysis("AAPL", output_dir="/custom/output")

        _, saved_path = _saved_call(mock_dependencies["safe_json_dump"])
        _assert_saved_path(saved_path, ticker="AAPL")
        assert "/custom/output" not in _normalized(saved_path)

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_save_failure_does_not_raise(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"
        mock_dependencies["safe_json_dump"].return_value = False

        run_analysis("AAPL")

        mock_dependencies["safe_json_dump"].assert_called_once()

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_empty_timeframes_uses_default(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"

        run_analysis("AAPL", timeframes=[])

        mock_dependencies["facade"].analyze_ticker.assert_called_once_with("AAPL")

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_run_analysis_none_timeframes_uses_default(self, mock_datetime, mock_dependencies):
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"

        run_analysis("AAPL", timeframes=None)

        mock_dependencies["facade"].analyze_ticker.assert_called_once_with("AAPL")


class TestSafeJsonDump:
    def test_success_uses_custom_encoder_and_utf8_options(self):
        file_handle = mock_open()
        with patch("builtins.open", file_handle), \
             patch("scripts.marketflow_analysis_llm_interface.json.dump") as mock_json_dump:
            result = safe_json_dump({"ticker": "AAPL"}, "out.json")

        assert result is True
        file_handle.assert_called_once_with("out.json", "w")
        mock_json_dump.assert_called_once()
        args, kwargs = mock_json_dump.call_args
        assert args[0] == {"ticker": "AAPL"}
        assert kwargs["indent"] == 4
        assert kwargs["cls"] is CustomJSONEncoder
        assert kwargs["ensure_ascii"] is False

    def test_custom_encoder_converts_enum_values(self):
        class Mode(Enum):
            ACTIVE = "active"

        assert json.dumps({"mode": Mode.ACTIVE}, cls=CustomJSONEncoder) == '{"mode": "active"}'

    @patch("scripts.marketflow_analysis_llm_interface.datetime")
    def test_fallback_returns_false_when_primary_fails_and_fallback_succeeds(self, mock_datetime):
        mock_datetime.now.return_value.isoformat.return_value = "2024-01-15T12:00:00"
        file_handle = mock_open()
        with patch("builtins.open", file_handle), \
             patch("scripts.marketflow_analysis_llm_interface.json.dump") as mock_json_dump:
            mock_json_dump.side_effect = [TypeError("bad enum"), None]

            result = safe_json_dump({"ticker": "AAPL"}, "out.json")

        assert result is False
        assert mock_json_dump.call_count == 2
        fallback_data = mock_json_dump.call_args_list[1].args[0]
        assert fallback_data == {
            "error": "Original data could not be serialized",
            "error_message": "bad enum",
            "ticker": "AAPL",
            "timestamp": "2024-01-15T12:00:00",
        }

    def test_fallback_returns_false_when_primary_and_fallback_fail(self):
        with patch("builtins.open", side_effect=OSError("permission denied")):
            result = safe_json_dump({"ticker": "AAPL"}, "out.json")

        assert result is False
