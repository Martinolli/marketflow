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
import json
from datetime import datetime
from enum import Enum
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_report import MarketflowReport
from marketflow.marketflow_snapshot import MarketflowSnapshot, AnalysisType
from marketflow.marketflow_llm_interface import MarketflowLLMInterface
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_utils import sanitize_filename

logger = get_logger("marketflow_analysis_snapshot")
config_manager = create_app_config(logger=logger)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Enum types and other non-serializable objects."""
    
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        # Add other custom type handling as needed
        try:
            return super().default(obj)
        except TypeError:
            # Convert non-serializable objects to string representation
            return str(obj)

def safe_json_dump(data, file_path):
    """Safely dump data to JSON file with custom encoder."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, cls=CustomJSONEncoder, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        # Try to save a simplified version
        try:
            simplified_data = {
                "error": "Original data could not be serialized",
                "error_message": str(e),
                "ticker": data.get("ticker", "unknown") if isinstance(data, dict) else "unknown",
                "timestamp": datetime.now().isoformat()
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(simplified_data, f, indent=4)
            logger.warning(f"Saved simplified error data to {file_path}")
            return False
        except Exception as fallback_error:
            logger.error(f"Failed to save even simplified data: {fallback_error}")
            return False
        
def run_analysis(ticker, output_dir="data", timeframes=None):
    """Run market analysis for a given ticker symbol.

    Args:
        ticker (str): Ticker symbol (e.g., AAPL or X:BTCUSD)
        output_dir (str): Directory to save the reports.
        timeframes (list, optional): List of timeframes to analyze. If None, uses default timeframes.
    """
    # Get current date for logging
    current_date = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Running analysis for {ticker} on {current_date}")

    # Initialize MarketflowFacade
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
    output_dir = f"{report_dir}/{current_date}/{sanitize_filename(ticker)}"
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

    # Create a snapshot of the analysis
    snapshot = MarketflowSnapshot(output_dir=f".marketflow/snapshot_reports/{sanitize_filename(ticker)}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                                  enable_compression=True)
    logger.info("Creating snapshot of the analysis...")
    snapshot_id = snapshot.save_enhanced_snapshot(
        analysis_result=results,
        ticker=ticker,
        analysis_type=AnalysisType.SENTIMENT,
        analyst_notes="Sentiment analysis completed. Review shows prevailing market optimism with moderate risk factors.",
        tags=["sentiment", "market_optimism", "risk_analysis"]
    )
    print(f"Saved snapshot: {snapshot_id}")
    logger.info(f"Snapshot for {ticker} created successfully in {output_dir}")

    # Generate LLM training data
    training_ids = snapshot.generate_llm_training_data(snapshot_id)
    print(f"Generated {len(training_ids)} LLM training records")
    
    # Export training data
    export_path = snapshot.export_llm_training_data(output_format="jsonl")
    print(f"Exported training data to: {export_path}")
    
    # Get statistics
    stats = snapshot.get_training_data_statistics()
    print(f"Training data statistics: {stats}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Marketflow analysis for a ticker.")
    parser.add_argument("ticker", type=str, help="Ticker symbol (e.g., AAPL or X:BTCUSD)")
    parser.add_argument("--output", type=str, default="C:\\Users\\Aspire5 15 i7 4G2050\\marketflow\\.marketflow\\reports", help="Output directory for reports")
    parser.add_argument("--timeframes", type=str, nargs="*", default=None,
                        help="List of timeframes (e.g., 1d 4h 1h). If not provided, uses default timeframes.")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    run_analysis(args.ticker, output_dir=args.output, timeframes=args.timeframes)
