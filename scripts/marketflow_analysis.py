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
from marketflow.marketflow_llm_interface import MarketflowLLMInterface
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_utils import sanitize_filename
from marketflow.marketflow_utils import save_timeframe_data

# marketflow_analysis.py (add near the end, after saving reports/LLM analysis)
from marketflow.transient_vector_memory import TransientVectorMemory
from rag.embedder import embed_batch  # your existing embed; ensure it returns fixed-length list

# Ensure the logger is set up correctly
logger = get_logger("marketflow_analysis")
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

def safe_json_dump(data: dict, file_path: str) -> bool:
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
        
def embed_fn(text):
    # The model name must match your embedding dimension (1536 for text-embedding-3-small)
    return embed_batch([text], model="text-embedding-3-small")[0]

def run_analysis(ticker, output_dir="data", timeframes=None):
    """Run market analysis for a given ticker symbol.

    Args:
        ticker (str): Ticker symbol (e.g., AAPL or X:BTCUSD)
        output_dir (str): Directory to save the reports.
        timeframes (list, optional): List of timeframes to analyze. If None, uses default timeframes.
    """

    current_date = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Running analysis for {ticker} on {current_date}")

    facade = MarketflowFacade()
    logger.info(f"Running analysis for ticker: {ticker}")
    # Allow passing specific timeframes if needed (else use default in facade)
    if timeframes:
        results = facade.analyze_ticker(ticker, timeframes=timeframes)
        logger.info(f"Using custom timeframes: {timeframes}")
    else:
        results = facade.analyze_ticker(ticker)
        logger.info("Using default timeframes for analysis.")

    if isinstance(results, dict) and 'timeframe_analyses' in results:
        timeframe_data_to_save = results.get('timeframe_analyses', {})
        if timeframe_data_to_save:
            logger.info(f"Calling save_timeframe_data for {ticker}...")
            save_timeframe_data(ticker, timeframe_data_to_save)
            logger.info(f"Timeframe data save process for {ticker} completed.")
        else:
            logger.warning(f"Timeframe analysis data for {ticker} is empty. Skipping save.")
    else:
        logger.warning(f"Unexpected results format for {ticker} or 'timeframe_analyses' key missing.")

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

    # Create a LLM interface for further analysis
    try:
        llm_interface = MarketflowLLMInterface()
        llm_interface_analysis = llm_interface.get_ticker_analysis(ticker)
        if llm_interface_analysis:
            logger.info(f"LLM analysis for {ticker} retrieved successfully.")
        else:
            logger.error(f"Failed to retrieve LLM analysis for {ticker}.")
            llm_interface_analysis = {
                "error": "No LLM analysis data returned",
                "ticker": ticker,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error creating LLM interface or getting analysis: {e}")
        llm_interface_analysis = {
            "error": f"LLM interface error: {str(e)}",
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }

    logger.info("Creating LLM interface for further analysis...")

    # Save the LLM analysis to a file with safe serialization
    llm_analysis_file = os.path.join(output_dir, f"{sanitize_filename(ticker)}_llm_analysis.json")
    
    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    success = safe_json_dump(llm_interface_analysis, llm_analysis_file)
    if success:
        logger.info(f"LLM analysis saved successfully to {llm_analysis_file}")
    else:
        logger.error(f"Failed to save LLM analysis to {llm_analysis_file}")

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    namespace = f"session:joao:{run_id}:{sanitize_filename(ticker)}"
    logger.info(f"Creating TVM namespace for {ticker}: {namespace}")

    ns_file = os.path.join(output_dir, ".tvm_namespace")
    with open(ns_file, "w", encoding="utf-8") as f:
        f.write(namespace)


    # Build a concise narrative from extractor or report content
    narrative_path = os.path.join(output_dir, f"{sanitize_filename(ticker)}_summary.txt")
    logger.info(f"Building narrative for {ticker}...")
    if os.path.exists(narrative_path):
        with open(narrative_path, "r", encoding="utf-8") as f:
            narrative = f.read()
    else:
        narrative = json.dumps(report.create_summary_report(ticker), ensure_ascii=False, indent=2)

    # init TVM (dim must match your embedding model)
    tvm = TransientVectorMemory(embed_fn=embed_fn, dim=1536, ttl_seconds=24*3600)
    if not tvm:
        logger.error(f"Failed to create TVM for {ticker}.")
    tvm.upsert_text(
        namespace=namespace,
        report_id=f"{sanitize_filename(ticker)}_{run_id}",
        text=narrative,
        meta={"source": "marketflow_facade", "ticker": ticker}
    )
    logger.info(f"Upserted narrative for {ticker} into TVM under namespace {namespace}")

    # OPTIONAL: also upsert llm_interface narrative if useful
    llm_json_path = os.path.join(output_dir, f"{sanitize_filename(ticker)}_llm_analysis.json")
    logger.info(f"Checking for LLM analysis file at {llm_json_path}...")
    if os.path.exists(llm_json_path):
        with open(llm_json_path, "r", encoding="utf-8") as f:
            tvm.upsert_text(namespace, f"{sanitize_filename(ticker)}_{run_id}_llm",
                            text=f.read(), meta={"source": "llm_interface", "ticker": ticker})
            logger.info(f"Upserted LLM analysis for {ticker} into TVM under namespace {namespace}")

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Marketflow analysis for a ticker.")
    parser.add_argument("ticker", type=str, help="Ticker symbol (e.g., AAPL or X:BTCUSD)")
    parser.add_argument("--output", type=str, default="C:\\Users\\Aspire5 15 i7 4G2050\\marketflow\\.marketflow\\reports", help="Output directory for reports")
    parser.add_argument("--timeframes", type=str, nargs="*", default=None,
                        help="List of timeframes (e.g., 1d 4h 1h). If not provided, uses default timeframes.")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    run_analysis(args.ticker, output_dir=args.output, timeframes=args.timeframes)
