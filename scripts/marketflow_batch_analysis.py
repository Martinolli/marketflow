"""
Marketflow Batch Analysis Orchestrator
This script runs market analysis for multiple tickers, generates reports,
and consolidates all analysis narratives into a single Transient Vector Memory (TVM) store.
This allows the RAG Q&A system to query and compare across all tickers in the batch.

Use:
    python marketflow_batch_analysis.py AAPL MSFT GOOG
"""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from marketflow.marketflow_analysis import run_analysis, embed_fn
from marketflow.operational_artifacts import (
    ArtifactContractError,
    PROFILE_MANUAL_SCENARIO,
    PROFILE_POSITION_SWING,
    PROFILE_SWING,
    WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
    WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
    annotated_dataset_artifact,
    create_run_context,
    ensure_run_context,
)
from marketflow.transient_vector_memory import TransientVectorMemory
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_utils import sanitize_filename
from marketflow.batch_utils import write_batch_summary_csv

def main():
    parser = argparse.ArgumentParser(description="Run batch Marketflow analysis for multiple tickers.")
    parser.add_argument("tickers", nargs='+', help="List of ticker symbols (e.g., AAPL MSFT GOOG)")
    parser.add_argument("--lineage-mode", choices=["legacy", "canonical"], default="legacy")
    parser.add_argument("--lineage-run-root", default=".marketflow/reports/runs")
    parser.add_argument("--lineage-run-id", default=None)
    parser.add_argument(
        "--lineage-workflow",
        choices=[WORKFLOW_MANUAL_SCENARIO_ANALYSIS, WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT],
        default=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
    )
    parser.add_argument(
        "--analysis-profile",
        choices=[PROFILE_SWING, PROFILE_POSITION_SWING, PROFILE_MANUAL_SCENARIO],
        default=PROFILE_SWING,
    )
    parser.add_argument("--lineage-timeframes", nargs="*", default=None)
    args = parser.parse_args()

    logger = get_logger("marketflow_batch_analysis")
    config = create_app_config()
    report_root = config.REPORT_DIR

    lineage_run = None
    if args.lineage_mode == "canonical":
        lineage_run = (
            ensure_run_context(run_root=args.lineage_run_root, run_id=args.lineage_run_id)
            if args.lineage_run_id
            else create_run_context(run_root=args.lineage_run_root)
        )
        run_id = lineage_run["run_id"]
    else:
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
    lineage_receipts = []
    for ticker in args.tickers:
        logger.info(f"--- Processing ticker: {ticker} ---")
        try:
            # We will modify run_analysis to return the narrative text
            narrative, ticker_output_dir = run_analysis(ticker, logger=logger)
            runs.append({"ticker": ticker, "output_dir": ticker_output_dir})
            if lineage_run:
                for timeframe in args.lineage_timeframes or []:
                    csv_path = Path(ticker_output_dir) / f"{sanitize_filename(ticker)}_{timeframe}.csv"
                    artifact = annotated_dataset_artifact(
                        csv_path=csv_path,
                        run_root=args.lineage_run_root,
                        run_id=lineage_run["run_id"],
                        workflow_type=args.lineage_workflow,
                        ticker=ticker,
                        analysis_profile=args.analysis_profile,
                        timeframe=timeframe,
                    )
                    lineage_receipts.append(artifact["receipt"])

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

        except ArtifactContractError:
            if args.lineage_mode == "canonical":
                raise
            logger.exception("Failed to create lineage artifact for %s", ticker)
            continue
        except Exception as e:
            logger.error(f"Failed to process ticker {ticker}: {e}", exc_info=True)
            if args.lineage_mode == "canonical":
                raise
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
    if lineage_receipts:
        print("\nLineage receipts:")
        print(json.dumps(lineage_receipts, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
