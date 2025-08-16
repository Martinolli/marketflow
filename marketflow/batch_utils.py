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

def write_batch_summary_csv(tickers, output_dir, logger):
    summary_rows = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    for ticker in tickers:
        llm_path = f".marketflow/reports/{current_date}/{sanitize_filename(ticker)}/{sanitize_filename(ticker)}_llm_analysis.json"
        if os.path.exists(llm_path):
            with open(llm_path, "r") as f:
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