"""
    This script runs batch analysis on a list of stock tickers using the MarketFlow framework.
    It generates individual analysis reports and an enriched summary CSV file.
"""
# marketflow_batch_report.py

import argparse
import os
import json
import csv
from datetime import datetime
from marketflow_analysis import run_analysis, sanitize_filename
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("MarketflowBatchReport")
config_manager = create_app_config(logger=logger)

# Define the headers for our new, improved CSV file.
# This makes it easy to manage and ensures the order is consistent.
CSV_FIELDNAMES = [
    "ticker",
    "current_price",
    "signal_type",
    "signal_strength",
    "trend_1d",
    "wyckoff_context_1d",
    "wyckoff_context_4h",
    "stop_loss",
    "take_profit",
    "risk_reward_ratio",
    "nearest_support_1d",
    "nearest_resistance_1d",
    "narrative_summary"
]

def extract_summary_data(llm_result, ticker):
    """
    Extracts and flattens key information from the detailed JSON analysis 
    into a single dictionary suitable for a CSV row.
    
    Args:
        llm_result (dict): The loaded JSON data from the LLM analysis file.
        ticker (str): The ticker symbol, used as a fallback.

    Returns:
        dict: A dictionary containing the summarized data points.
    """
    # Use .get() extensively with default values to prevent errors if a key is missing.
    vpa_signal = llm_result.get("vpa_signal", {})
    risk_assessment = llm_result.get("risk_assessment", {})
    timeframe_data = llm_result.get("timeframe_data", {})
    
    # Safely get data for the primary timeframe (1d)
    data_1d = timeframe_data.get("1d", {})
    trend_1d = data_1d.get("trend", {})
    wyckoff_1d = data_1d.get("wyckoff", {})
    sr_1d = data_1d.get("support_resistance", {})
    
    # Safely get data for the secondary timeframe (4h) for context
    data_4h = timeframe_data.get("4h", {})
    wyckoff_4h = data_4h.get("wyckoff", {})
    
    # Extract nearest support/resistance, checking if the list exists and is not empty
    support_levels = sr_1d.get("support", [])
    resistance_levels = sr_1d.get("resistance", [])
    nearest_support = f"{support_levels[0]['price']:.2f}" if support_levels else "N/A"
    nearest_resistance = f"{resistance_levels[0]['price']:.2f}" if resistance_levels else "N/A"
    
    # Clean up the narrative for better CSV display (remove newlines and asterisks)
    narrative = llm_result.get("analysis_narrative", "N/A").replace("\n", " ").replace("**", "")

    return {
        "ticker": llm_result.get("ticker", ticker),
        "current_price": llm_result.get("current_price", "N/A"),
        "signal_type": vpa_signal.get("type", "N/A"),
        "signal_strength": vpa_signal.get("strength", "N/A"),
        "trend_1d": trend_1d.get("trend_direction", "N/A"),
        "wyckoff_context_1d": wyckoff_1d.get("context", "N/A"),
        "wyckoff_context_4h": wyckoff_4h.get("context", "N/A"),
        "stop_loss": f"{risk_assessment.get('stop_loss', 0):.2f}",
        "take_profit": f"{risk_assessment.get('take_profit', 0):.2f}",
        "risk_reward_ratio": f"{risk_assessment.get('risk_reward_ratio', 0):.2f}",
        "nearest_support_1d": nearest_support,
        "nearest_resistance_1d": nearest_resistance,
        "narrative_summary": narrative
    }

def run_batch_analysis(tickers, output_dir=".marketflow/batch_reports_data", timeframes=None):
    summary_rows = []
    current_date = datetime.now().strftime("%Y-%m-%d")

    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        # Assuming run_analysis generates the JSON file needed.
        # If it returns the data directly, you can capture it here.
        run_analysis(ticker) 
        logger.info(f"Analysis for {ticker} completed.")

        # Construct the path to the LLM analysis result file
        llm_path = f".marketflow/reports/{current_date}/{sanitize_filename(ticker)}/{sanitize_filename(ticker)}_llm_analysis.json"
        logger.info(f"Looking for LLM analysis file at {llm_path}")

        if os.path.exists(llm_path):
            with open(llm_path, "r") as f:
                llm_result = json.load(f)
            # Use the helper function to create a clean summary row
            summary_row = extract_summary_data(llm_result, ticker)
            summary_rows.append(summary_row)
        else:
            logger.error(f"LLM analysis file not found for {ticker} at {llm_path}")
            # Append an error row to know which ones failed
            summary_rows.append({
                "ticker": ticker,
                "current_price": "N/A",
                "signal_type": "FILE NOT FOUND",
                "signal_strength": "ERROR",
                "trend_1d": "N/A",
                "wyckoff_context_1d": "N/A",
                "wyckoff_context_4h": "N/A",
                "stop_loss": "N/A",
                "take_profit": "N/A",
                "risk_reward_ratio": "N/A",
                "nearest_support_1d": "N/A",
                "nearest_resistance_1d": "N/A",
                "narrative_summary": f"Could not find analysis file at {llm_path}"
            })

    if not summary_rows:
        print("\n⚠️ No analysis results found to generate a summary.")
        return

    # Save the enriched summary to CSV
    summary_path = os.path.join(output_dir, current_date, "batch_summary_enriched.csv")
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    
    with open(summary_path, "w", newline="", encoding='utf-8') as f:
        # Use the predefined fieldnames for the header
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\n✅ Enriched batch summary saved to {summary_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run batch analysis on stock tickers.")
    parser.add_argument(
        "--output", type=str, default=".marketflow/batch_reports_data", help="Output directory for batch reports"
    )
    parser.add_argument(
        "--timeframes", type=str, nargs="*", default=None,
        help="List of timeframes (e.g., 1d 4h 1h). If not provided, uses default timeframes."
    )
    args = parser.parse_args()
    
    # You can load tickers from a file, user input, or define here:
    tickers = ["IMA", "GOOGL", "TSLA", "X:BTCUSD"]

    run_batch_analysis(tickers, output_dir=args.output, timeframes=args.timeframes)