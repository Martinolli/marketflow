"""
MarketFlow CLI entry point

Usage examples:
    python -m marketflow normal AAPL
    python -m marketflow analyze AAPL
    python -m marketflow analyze AAPL --timeframes 1d 4h 1h
"""

import argparse
import contextlib
import json
import sys
from datetime import datetime


def cmd_analyze(ticker: str, timeframes: list[str] | None) -> int:
    from marketflow.marketflow_config_manager import create_app_config
    from marketflow.marketflow_facade import MarketflowFacade
    from marketflow.marketflow_logger import get_logger
    from marketflow.marketflow_report import MarketflowReport
    from marketflow.marketflow_results_extractor import MarketflowResultExtractor
    from marketflow.marketflow_utils import sanitize_filename

    logger = get_logger("marketflow_cli")
    config = create_app_config(logger=logger)
    current_date = datetime.now().strftime("%Y-%m-%d")

    facade = MarketflowFacade()
    if timeframes:
        results = facade.analyze_ticker(ticker, timeframes=timeframes)
    else:
        results = facade.analyze_ticker(ticker)

    if not isinstance(results, dict):
        logger.error("Unexpected results format; aborting.")
        return 1

    extractor = MarketflowResultExtractor({ticker: results})
    report_root = config.REPORT_DIR
    out_dir = f"{report_root}/{current_date}/{sanitize_filename(ticker)}"
    report = MarketflowReport(extractor, output_dir=out_dir)
    ok = report.generate_all_reports_for_ticker(ticker)

    if ok:
        print(f"✅ Reports for {ticker} saved in {out_dir}")
        return 0
    else:
        print("Report generation failed.")
        return 2


def main() -> int:
    parser = argparse.ArgumentParser(prog="marketflow", description="MarketFlow CLI")
    sub = parser.add_subparsers(dest="command")

    p_normal = sub.add_parser("normal", help="Run ticker-only fixed-profile local orchestration")
    p_normal.add_argument("ticker", type=str)

    p_an = sub.add_parser("analyze", help="Run analysis and generate reports")
    p_an.add_argument("ticker", type=str)
    p_an.add_argument("--timeframes", type=str, nargs="*", default=None,
                      help="List of timeframes, e.g. 1d 4h 1h")

    args = parser.parse_args()

    if args.command == "normal":
        try:
            with contextlib.redirect_stdout(sys.stderr):
                from marketflow.fixed_profile_orchestrator import NormalTickerError, run_fixed_profile_orchestrator

                receipt = run_fixed_profile_orchestrator(args.ticker)
        except Exception as exc:
            try:
                from marketflow.fixed_profile_orchestrator import NormalTickerError
            except Exception:
                NormalTickerError = ValueError
            if isinstance(exc, NormalTickerError):
                print(json.dumps({"status": "ORCHESTRATOR_INVALID", "error": str(exc)}, indent=2, sort_keys=True))
                return 2
            print(json.dumps({"status": "ORCHESTRATOR_INVALID", "error_type": type(exc).__name__}, indent=2, sort_keys=True))
            return 3
        else:
            print(json.dumps(receipt, indent=2, sort_keys=True))
            return 0

    if args.command == "analyze":
        return cmd_analyze(args.ticker, args.timeframes)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
