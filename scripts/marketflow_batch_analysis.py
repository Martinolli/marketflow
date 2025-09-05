"""
Marketflow Batch Analysis Orchestrator
This script runs market analysis for multiple tickers, generates reports,
and consolidates all analysis narratives into a single Transient Vector Memory (TVM) store.
This allows the RAG Q&A system to query and compare across all tickers in the batch.

Use:
    python marketflow_batch_analysis.py AAPL MSFT GOOG
"""
import argparse
import os
from datetime import datetime

from marketflow.marketflow_analysis import run_analysis, embed_fn
from marketflow.transient_vector_memory import TransientVectorMemory
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_utils import sanitize_filename
from marketflow.batch_utils import write_batch_summary_csv

def main():
    parser = argparse.ArgumentParser(description="Run batch Marketflow analysis for multiple tickers.")
    parser.add_argument("tickers", nargs='+', help="List of ticker symbols (e.g., AAPL MSFT GOOG)")
    args = parser.parse_args()

    logger = get_logger("marketflow_batch_analysis")
    config = create_app_config()
    report_root = config.REPORT_DIR

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 1. Define a single, shared namespace for the entire batch
    namespace = f"batch:{run_id}"
    logger.info(f"Starting batch analysis. TVM Namespace: '{namespace}'")

    # 2. Initialize one TVM for the whole batch
    tvm = TransientVectorMemory(embed_fn=embed_fn, dim=1536, ttl_seconds=48*3600)

    # Prepare the directory for this batch run's consolidated TVM store
    # The Q&A app will find this by looking for the most recent .tvm_namespace file
    batch_output_dir = os.path.join(report_root, f"batch_{run_id}")
    os.makedirs(batch_output_dir, exist_ok=True)

    # 3. Loop through tickers and process them
    runs = []  # collect per-ticker output_dir for robust CSV summary
    for ticker in args.tickers:
        logger.info(f"--- Processing ticker: {ticker} ---")
        try:
            # We will modify run_analysis to return the narrative text
            narrative, ticker_output_dir = run_analysis(ticker, logger=logger)
            runs.append({"ticker": ticker, "output_dir": ticker_output_dir})

            if narrative:
                logger.info(f"Upserting narrative for {ticker} into shared namespace.")
                # 4. Upsert the narrative with the ticker in the metadata
                tvm.upsert_text(
                    namespace=namespace,
                    report_id=f"{sanitize_filename(ticker)}_{run_id}",
                    text=narrative,
                    meta={"source": "marketflow_analysis", "ticker": ticker}
                )
            else:
                logger.warning(f"No narrative generated for {ticker}. Skipping TVM upsert.")

        except Exception as e:
            logger.error(f"Failed to process ticker {ticker}: {e}", exc_info=True)
            continue
    
    logger.info("--- Batch processing complete. Saving consolidated TVM store. ---")

    # 5. Save the consolidated TVM store and the namespace file
    tvm_dir = os.path.join(batch_output_dir, ".tvm_store")
    tvm.save_namespace(namespace, tvm_dir)

    ns_file = os.path.join(batch_output_dir, ".tvm_namespace")
    with open(ns_file, "w", encoding="utf-8") as f:
        f.write(namespace)
    
    logger.info(f"Successfully saved TVM data to {tvm_dir}")
    logger.info(f"Namespace '{namespace}' written to {ns_file}")
    print(f"\n✅ Batch analysis complete. Consolidated report data saved in {batch_output_dir}")

    # NEW: Generate CSV summary
    logger.info("Generating batch summary CSV...")
    output_summary_csv_data = os.path.join(report_root, f"batch_csv_{run_id}")
    summary_path = write_batch_summary_csv(runs, output_summary_csv_data, logger)
    if summary_path:
        print(f"\n✅ Enriched batch summary saved to {summary_path}")

if __name__ == "__main__":
    main()
