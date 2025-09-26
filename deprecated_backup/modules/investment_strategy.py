# scripts/investment_strategy.py
"""
Investment Strategy and Stock Screener

This script leverages the full analysis pipeline to screen and rank stocks
based on a defined investment strategy.

Strategy:
1.  Run the full analysis pipeline for a list of candidate stocks.
2.  For each stock, analyze the generated Monte Carlo summary.
3.  Calculate the Risk/Reward Ratio (RRR) from the trade setup.
4.  Extract the Probability of Profit (POP) from the simulation.
5.  Filter out stocks that do not meet the minimum criteria (e.g., RRR > 1.5, POP > 60%).
6.  Rank the qualifying stocks by a composite score (e.g., Score = RRR * POP).
7.  Display the final ranked list of investment opportunities.

Use:
    python scripts/investment_strategy.py --tickers AAPL MSFT NVDA GOOG PANW --min-rrr 1.5 --min-pop 0.6
"""
import argparse
import subprocess
import os
import json
import logging
import glob
import pandas as pd

# --- Configuration ---
PIPELINE_SCRIPT = os.path.join("scripts", "run_full_pipeline.py")
REPORT_ROOT_DIR = os.path.join(".marketflow", "reports")

# --- Strategy Parameters ---
MIN_RRR_DEFAULT = 1.5
MIN_POP_DEFAULT = 0.60 # 60%

# --- Setup Logging ---
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
logger = get_logger("InvestmentStrategy")
config = create_app_config(logger=logger)

def find_latest_run_files(ticker: str):
    """Finds the latest report and mc_summary files for a ticker."""
    # Find latest batch directory
    list_of_dirs = [d for d in os.listdir(REPORT_ROOT_DIR) if os.path.isdir(os.path.join(REPORT_ROOT_DIR, d)) and d.startswith("batch_")]
    if not list_of_dirs:
        return None, None
    latest_batch_dir = os.path.join(REPORT_ROOT_DIR, max(list_of_dirs))

    # Find report and CSV dir inside it
    report_files = glob.glob(os.path.join(latest_batch_dir, '**', f'{ticker}_report.json'), recursive=True)
    if not report_files:
        return None, None
    report_path = report_files[0]
    
    with open(report_path, 'r') as f:
        report_data = json.load(f)
    csv_path = report_data.get("key_files", {}).get("clean_csv")
    if not csv_path:
        return report_path, None
        
    csv_dir = os.path.dirname(csv_path)
    mc_summary_files = sorted(glob.glob(os.path.join(csv_dir, '*_mc_summary.json')))
    
    return report_path, mc_summary_files[-1] if mc_summary_files else None

def analyze_results(ticker: str, report_path: str, mc_summary_path: str):
    """Analyzes the output files against the strategy criteria."""
    try:
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        with open(mc_summary_path, 'r') as f:
            mc_data = json.load(f)

        # Extract data for RRR calculation
        setup = report_data.get("trade_setup", {})
        entry = setup.get("entry_price")
        tp = setup.get("target_price")
        sl = setup.get("stop_loss")

        if not all([entry, tp, sl]):
            logger.warning(f"[{ticker}] Missing trade setup values in report.")
            return None

        reward = abs(tp - entry)
        risk = abs(entry - sl)
        if risk == 0:
            return None
        rrr = reward / risk

        # Extract Probability of Profit from Monte Carlo
        pop = mc_data.get("metrics_from_now", {}).get("pop_tp_first", 0.0)
        
        # Calculate Score
        score = rrr * pop

        return {
            "ticker": ticker,
            "entry": entry,
            "tp": tp,
            "sl": sl,
            "rrr": round(rrr, 2),
            "pop": round(pop, 3),
            "score": round(score, 3)
        }

    except Exception as e:
        logger.error(f"[{ticker}] Failed to analyze results: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Run investment strategy screener.")
    parser.add_argument("--tickers", nargs='+', required=True, help="List of ticker symbols to screen.")
    parser.add_argument("--min-rrr", type=float, default=MIN_RRR_DEFAULT, help="Minimum acceptable Risk/Reward Ratio.")
    parser.add_argument("--min-pop", type=float, default=MIN_POP_DEFAULT, help="Minimum acceptable Probability of Profit.")
    parser.add_argument("--skip-pipeline", action="store_true", help="Skip running the pipeline and analyze existing results.")
    args = parser.parse_args()

    # --- Step 1: Run the pipeline for all tickers ---
    if not args.skip_pipeline:
        logger.info("Running the full analysis pipeline for all candidate tickers...")
        try:
            subprocess.run(
                ["python", PIPELINE_SCRIPT] + args.tickers,
                check=True
            )
        except subprocess.CalledProcessError:
            logger.fatal("The analysis pipeline failed. Aborting strategy execution.")
            return
        logger.info("Pipeline execution finished. Proceeding to strategy analysis.")
    else:
        logger.info("Skipping pipeline run. Analyzing most recent existing data.")

    # --- Step 2: Analyze and Rank the results ---
    all_results = []
    for ticker in args.tickers:
        logger.info(f"--- Analyzing {ticker} ---")
        report_file, mc_summary_file = find_latest_run_files(ticker)

        if not report_file or not mc_summary_file:
            logger.warning(f"Could not find required result files for {ticker}. Skipping.")
            continue
        
        analysis = analyze_results(ticker, report_file, mc_summary_file)
        if analysis:
            all_results.append(analysis)

    if not all_results:
        logger.info("No valid trade setups found after analysis.")
        return

    # Convert to DataFrame for filtering and sorting
    df = pd.DataFrame(all_results)
    
    # Apply strategy filters
    filtered_df = df[
        (df['rrr'] >= args.min_rrr) &
        (df['pop'] >= args.min_pop)
    ].copy()

    # Sort by score
    ranked_df = filtered_df.sort_values(by="score", ascending=False).reset_index(drop=True)

    # --- Step 3: Display the final recommendations ---
    print("\n" + "="*80)
    print(" " * 25 + "INVESTMENT STRATEGY RESULTS")
    print("="*80)
    print(f"Strategy Criteria: RRR >= {args.min_rrr} AND Prob. of Profit >= {args.min_pop:.0%}")
    print(f"Screened {len(args.tickers)} stocks, found {len(ranked_df)} qualifying opportunities.")
    print("-"*80)

    if ranked_df.empty:
        print("No stocks met the investment criteria.")
    else:
        print(ranked_df.to_string())
    
    print("="*80)

if __name__ == "__main__":
    main()