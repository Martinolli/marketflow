"""
This script generates a CSV file containing summary data from a JSON analysis file.

"""
import os
import json
import csv
from datetime import datetime
from marketflow.marketflow_utils import sanitize_filename


CSV_FIELDNAMES = [
    "ticker", "current_price", "signal_type", "signal_strength", "trend_1d",
    "wyckoff_context_1d", "wyckoff_context_4h", "stop_loss", "take_profit",
    "risk_reward_ratio", "nearest_support_1d", "nearest_resistance_1d", "narrative_summary"
]

def _fmt2(x) -> str:
    """Format numeric-like values to '%.2f' or return 'N/A' on failure."""
    try:
        return f"{float(x):.2f}"
    except Exception:
        return "N/A"

def extract_summary_data(llm_result: dict, ticker: str) -> dict:
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
    if support_levels and isinstance(support_levels[0], dict):
        nearest_support = _fmt2(support_levels[0].get("price"))
    else:
        nearest_support = _fmt2(support_levels[0]) if support_levels else "N/A"
    if resistance_levels and isinstance(resistance_levels[0], dict):
        nearest_resistance = _fmt2(resistance_levels[0].get("price"))
    else:
        nearest_resistance = _fmt2(resistance_levels[0]) if resistance_levels else "N/A"
    
    # Clean up the narrative for better CSV display (remove newlines and asterisks)
    narrative = llm_result.get("analysis_narrative", "N/A").replace("\n", " ").replace("**", "")

    return {
        "ticker": llm_result.get("ticker", ticker),
        "current_price": _fmt2(llm_result.get("current_price")),
        "signal_type": vpa_signal.get("type", "N/A"),
        "signal_strength": vpa_signal.get("strength", "N/A"),
        "trend_1d": trend_1d.get("trend_direction", "N/A"),
        "wyckoff_context_1d": wyckoff_1d.get("context", "N/A"),
        "wyckoff_context_4h": wyckoff_4h.get("context", "N/A"),
        "stop_loss": _fmt2(risk_assessment.get('stop_loss')),
        "take_profit": _fmt2(risk_assessment.get('take_profit')),
        "risk_reward_ratio": _fmt2(risk_assessment.get('risk_reward_ratio')),
        "nearest_support_1d": nearest_support,
        "nearest_resistance_1d": nearest_resistance,
        "narrative_summary": narrative
    }

def write_batch_summary_csv(runs, output_dir, logger):
    """
    Write a CSV summary for a batch of runs.

    Args:
        runs: Iterable of {"ticker": str, "output_dir": str} entries from run_analysis.
        output_dir: Destination directory for the CSV file.
        logger: Logger for status messages.
    """
    summary_rows = []
    for run in runs:
        ticker = run.get("ticker")
        t_dir = run.get("output_dir") or ""
        llm_path = os.path.join(t_dir, f"{sanitize_filename(ticker)}_llm_analysis.json")
        if os.path.exists(llm_path):
            with open(llm_path, "r", encoding="utf-8") as f:
                llm_result = json.load(f)
            summary_row = extract_summary_data(llm_result, ticker)
            summary_rows.append(summary_row)
        else:
            summary_rows.append({
                "ticker": ticker, "current_price": "N/A", "signal_type": "FILE NOT FOUND",
                "signal_strength": "ERROR", "trend_1d": "N/A", "wyckoff_context_1d": "N/A",
                "wyckoff_context_4h": "N/A", "stop_loss": "N/A", "take_profit": "N/A",
                "risk_reward_ratio": "N/A", "nearest_support_1d": "N/A",
                "nearest_resistance_1d": "N/A",
                "narrative_summary": f"Could not find analysis file at {llm_path}"
            })
    if not summary_rows:
        logger.warning("No analysis results found to generate a summary.")
        return None
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    summary_path = os.path.join(output_dir, f"batch_summary_enriched_{date_str}.csv")
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w", newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(summary_rows)
    logger.info(f"Enriched batch summary saved to {summary_path}")
    return summary_path