""""
Marketflow Analysis Script
This script runs a market analysis for a given ticker symbol using the MarketflowFacade.
It generates reports and saves them in the specified output directory.

Use:
    python /scripts/marketflow_analysis.py AAPL
    python /scripts/marketflow_analysis.py X:BTCUSD

    python /scripts/marketflow_analysis.py AAPL --timeframes 1d 1h 15m

"""
import argparse
import os
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_report import MarketflowReport
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_utils import sanitize_filename

logger = get_logger("marketflow_analysis")
config_manager = create_app_config(logger=logger)

def run_analysis(ticker, output_dir="data", timeframes=None):
    """Run market analysis for a given ticker symbol.

    Args:
        ticker (str): Ticker symbol (e.g., AAPL or X:BTCUSD)
        output_dir (str): Directory to save the reports.
        timeframes (list, optional): List of timeframes to analyze. If None, uses default timeframes.
    """
    facade = MarketflowFacade()
    logger.info(f"Running analysis for ticker: {ticker}")
    # Allow passing specific timeframes if needed (else use default in facade)
    if timeframes:
        results = facade.analyze_ticker(ticker, timeframes=timeframes)
        logger.info(f"Using custom timeframes: {timeframes}")
    else:
        results = facade.analyze_ticker(ticker)
        logger.info("Using default timeframes for analysis.")

    extractor = MarketflowResultExtractor({ticker: results})
    logger.info("Extracting data from results...")
    config = create_app_config()
    report_dir = config.REPORT_DIR
    output_dir = f"{report_dir}/{sanitize_filename(ticker)}"
    logger.info(f"Report directory: {output_dir}")
    report = MarketflowReport(extractor, output_dir=output_dir)
    logger.info("Creating report...")
    success = report.generate_all_reports_for_ticker(ticker)
    if success:
        logger.info(f"Summary report created successfully in {report_dir}")
    else:
        logger.error("Report creation failed.")
    logger.info("MarketflowFacade real data test completed successfully.")

    print(f"✅ Reports for {ticker} saved in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Marketflow analysis for a ticker.")
    parser.add_argument("ticker", type=str, help="Ticker symbol (e.g., AAPL or X:BTCUSD)")
    parser.add_argument("--output", type=str, default="C:\\Users\\Aspire5 15 i7 4G2050\\marketflow\\.marketflow\\reports", help="Output directory for reports")
    parser.add_argument("--timeframes", type=str, nargs="*", default=None,
                        help="List of timeframes (e.g., 1d 4h 1h). If not provided, uses default timeframes.")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    run_analysis(args.ticker, output_dir=args.output, timeframes=args.timeframes)
