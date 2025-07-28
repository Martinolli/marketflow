"""
    This script runs batch analysis on a list of stock tickers using the MarketFlow framework.
    It generates individual analysis reports and a summary CSV file.

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

logger = get_logger("MarketflowBatchReport ")
config_manager = create_app_config(logger=logger)

def run_batch_analysis(tickers, output_dir=".marketflow/batch_reports_data", timeframes=None):
    summary_rows = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        run_analysis(ticker)
        logger.info(f"Analysis for {ticker} completed.")

        # Collect LLM analysis results
        llm_result = {}
        llm_path = f".marketflow/reports/{current_date}/{sanitize_filename(ticker)}/{sanitize_filename(ticker)}_llm_analysis.json"
        logger.info(f"Looking for LLM analysis file at {llm_path}")
        if os.path.exists(llm_path):
            with open(llm_path, "r") as f:
                llm_result = json.load(f)
            summary_rows.append({
                "ticker": llm_result.get("ticker", ticker),
                "signal": llm_result.get("overall_signal") or llm_result.get("vpa_signal", {}).get("type", "N/A"),
                "price": llm_result.get("current_price", "N/A"),
                "risk_reward_ratio": llm_result.get("risk_assessment", {}).get("risk_reward_ratio", "N/A"),
                "wyckoff_phase": llm_result.get("timeframe_data", {}).get("1d", {}).get("wyckoff", {}).get("context", "N/A")
            })
        else:
            summary_rows.append({
                "ticker": ticker,
                "signal": "ERROR",
                "price": "N/A",
                "risk_reward_ratio": "N/A",
                "wyckoff_phase": "N/A"
            })
    # Save summary
    summary_path = f"{output_dir}/{current_date}/batch_summary.csv"
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ticker", "signal", "price", "risk_reward_ratio", "wyckoff_phase"])
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)
    print(f"\n✅ Batch summary saved to {summary_path}")

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
    # You can load from file, user input, or define here:
    tickers = ["AAPL"] #, "ACHR", "X:BTCUSD", "X:MATICUSD"]  # add more as needed
    run_batch_analysis(tickers, output_dir=args.output, timeframes=args.timeframes)
