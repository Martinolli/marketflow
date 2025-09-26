# scripts/run_full_pipeline.py
"""
Full Marketflow Analysis Pipeline Orchestrator

This script automates the entire 3-step analysis workflow for a given list of tickers:
1.  Runs `marketflow_batch_analysis.py` to generate initial analysis, reports, and data files.
2.  Parses the generated `_report.json` to find the trade setup (entry, TP, SL) and key file paths.
3.  Runs `marketflow_monte_carlo_trade.py` with the extracted parameters to simulate trade outcomes.
4.  (Optional) Runs a plotting script like `plot_annotated_features.py`.

This script centralizes the workflow, making it easy to run a consistent analysis
across multiple stocks.

Use:
    python scripts/run_full_pipeline.py AAPL MSFT NVDA
"""
import argparse
import subprocess
import os
import json
import glob
from datetime import datetime
from pathlib import Path
import sys

# --- Configuration ---
# Adjust these paths to match your project structure
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BATCH_ANALYSIS_SCRIPT = str(PROJECT_ROOT / "scripts" / "marketflow_batch_analysis.py")
MONTE_CARLO_SCRIPT = str(PROJECT_ROOT / "marketflow" / "marketflow_monte_carlo_trade.py")
PLOTTER_SCRIPT = str(PROJECT_ROOT / "scripts" / "plot_annotated_features.py")  # Uncomment if you have this script
REPORT_ROOT_DIR = os.path.join(".marketflow", "reports", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}")


# --- Setup Logging ---
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("PipelineOrchestrator")
config = create_app_config(logger=logger)

def _subproc_env():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    # Ensure UTF-8 I/O in child processes (avoids UnicodeEncodeError on Windows)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env

def find_latest_batch_dir():
    """Finds the most recent batch directory in the report root."""
    list_of_dirs = [d for d in os.listdir(REPORT_ROOT_DIR) if os.path.isdir(os.path.join(REPORT_ROOT_DIR, d)) and d.startswith("batch_")]
    if not list_of_dirs:
        return None
    return os.path.join(REPORT_ROOT_DIR, max(list_of_dirs))

def run_pipeline_for_ticker(ticker: str):
    """Executes the full analysis pipeline for a single ticker."""
    logger.info(f"========== STARTING PIPELINE FOR {ticker} ==========")

    # --- Step 1: Run Batch Analysis ---
    # This step will create a new batch directory
    logger.info(f"[Step 1/3] Running market analysis for {ticker}...")
    try:
        subprocess.run(
            [sys.executable, BATCH_ANALYSIS_SCRIPT, ticker],
            check=True, capture_output=True, text=True,
            cwd=str(PROJECT_ROOT), env=_subproc_env(),
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed during market analysis for {ticker}.")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        return None, None  # Failed step

    # --- Step 1.5: Find Outputs and Extract Trade Parameters ---
    logger.info("Searching for analysis outputs...")
    batch_dir = find_latest_batch_dir()
    if not batch_dir:
        logger.error(f"Could not find any output batch directory after running analysis for {ticker}.")
        return None, None

    # Find the report JSON file for the specific ticker within the latest batch run
    # Using glob to search recursively inside the batch directory
    report_files = glob.glob(os.path.join(batch_dir, '**', f'{ticker}_report.json'), recursive=True)
    if not report_files:
        logger.error(f"Could not find '{ticker}_report.json' in '{batch_dir}'.")
        return None, None
    
    report_path = report_files[0]
    logger.info(f"Found report: {report_path}")

    with open(report_path, 'r') as f:
        report_data = json.load(f)

    trade_setup = report_data.get("trade_setup")
    key_files = report_data.get("key_files")

    if not trade_setup or not key_files:
        logger.warning(f"No 'trade_setup' or 'key_files' section in {report_path} for {ticker}. Skipping Monte Carlo.")
        return None, None

    entry = trade_setup.get("entry_price")
    tp = trade_setup.get("target_price")
    sl = trade_setup.get("stop_loss")
    # We need the clean CSV for the Monte Carlo simulation
    ohlcv_csv_path = key_files.get("clean_csv") 

    if not all([entry, tp, sl, ohlcv_csv_path]):
        logger.warning(f"Missing one of entry/tp/sl/csv_path in trade setup for {ticker}. Skipping Monte Carlo.")
        return None, None

    # --- Step 2: Run Monte Carlo Simulation ---
    logger.info(f"[Step 2/3] Running Monte Carlo simulation for {ticker} with TP={tp}, SL={sl}, Entry={entry}")
    mc_args = [
        "python", MONTE_CARLO_SCRIPT, ohlcv_csv_path,
        "--tp", str(tp),
        "--sl", str(sl),
        "--entry", str(entry),
        "--model", "garch", # Or 'bootstrap', 'ml_gbm'
        "--paths", "10000",
        "--horizon", "30",
        "--no-plots" # Often disabled for batch runs to save time/space
    ]
    try:
        subprocess.run(mc_args, check=True, capture_output=True, text=True,
                       cwd=str(PROJECT_ROOT), env=_subproc_env())
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed during Monte Carlo simulation for {ticker}.")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        return None, None
        
    # Find the generated MC summary file (it's created in the same dir as the input CSV)
    csv_dir = os.path.dirname(ohlcv_csv_path)
    mc_summary_files = sorted(glob.glob(os.path.join(csv_dir, '*_mc_summary.json')))
    if not mc_summary_files:
        logger.error(f"Could not find Monte Carlo summary JSON for {ticker} in {csv_dir}.")
        return None, None
    
    latest_mc_summary_path = mc_summary_files[-1]
    logger.info(f"Monte Carlo analysis complete. Summary at: {latest_mc_summary_path}")

    # --- Step 3: (Optional) Run Plotting ---
    logger.info(f"[Step 3/3] Generating PnF charts and plots for {ticker}...")
    annotated_csv = key_files.get("annotated_csv")
    if PLOTTER_SCRIPT and annotated_csv:
        try:
            plot_args = [sys.executable, PLOTTER_SCRIPT, annotated_csv, "--mc-summary", latest_mc_summary_path]
            subprocess.run(plot_args, check=True, capture_output=True, text=True,
                           cwd=str(PROJECT_ROOT), env=_subproc_env())
            logger.info(f"Successfully generated plots for {ticker}.")
        except Exception as e:
            logger.error(f"Plotting script failed for {ticker}: {e}")

    logger.info(f"========== PIPELINE FOR {ticker} COMPLETED SUCCESSFULLY ==========\n")
    return report_path, latest_mc_summary_path


def main():
    parser = argparse.ArgumentParser(description="Run the full Marketflow analysis pipeline for multiple tickers.")
    parser.add_argument("tickers", nargs='+', help="List of ticker symbols (e.g., AAPL MSFT GOOG)")
    args = parser.parse_args()

    results = {}
    for ticker in args.tickers:
        report_file, mc_summary_file = run_pipeline_for_ticker(ticker)
        if report_file and mc_summary_file:
            results[ticker] = {
                "report_json": report_file,
                "mc_summary_json": mc_summary_file
            }
    
    logger.info("--- Full Pipeline Batch Run Finished ---")
    logger.info("Summary of generated files:")
    for ticker, files in results.items():
        logger.info(f"  {ticker}:")
        logger.info(f"    - Report: {files['report_json']}")
        logger.info(f"    - MC Summary: {files['mc_summary_json']}")

if __name__ == "__main__":
    main()