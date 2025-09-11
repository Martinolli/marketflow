"""
Shared Utility Functions for the Marketflow Project

This module contains common, reusable functions that are shared across different
modules to avoid code duplication and maintain a single source of truth.
"""
import re
from pathlib import Path
import openai
import pandas as pd
from datetime import datetime

def get_project_root() -> Path:
    """Get the project root directory by locating the '.marketflow' marker."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / ".marketflow").exists():
            return parent
    # Fallback to the parent directory of the 'marketflow' package
    return Path(__file__).parent.parent

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def query_llm(prompt: str, model: str = "gpt-4.1", temperature: float = 0.8, system_message: str = "You are a helpful assistant.") -> str:
    """
    Send a prompt to the LLM and return its response.

    This function was corrected to properly handle its parameters. The original version
    ignored the 'prompt' and 'system_message' and used a hardcoded 'narrative' parameter
    that was often None, causing errors.
    """
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    # The user's prompt is added to the messages list.
    messages.append({"role": "user", "content": prompt})
    
    try:
        client = openai.OpenAI()  # Assumes OPENAI_API_KEY is in environment variables
        
        # The 'messages' list that was built is now correctly passed to the API call.
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        
        llm_answer = response.choices[0].message.content
        return llm_answer
    except Exception as e:
        # It's good practice to log the error and return an informative message.
        print(f"Error calling LLM: {e}")
        return "An error occurred while communicating with the LLM."
    
def save_timeframe_data(ticker: str, timeframe_analyses: dict) -> None:
    """
    Save timeframe data to disk. This function has been corrected to handle
    live pandas objects instead of expecting serialized dictionaries.

    Parameters:
    - ticker: Stock symbol (e.g., 'AAPL', 'MSFT')
    - timeframe_analyses: Dictionary with timeframe as key and analysis data as value.
                          The analysis data is expected to contain a 'processed_data' key.
    """
    project_root = get_project_root()
    # Build an absolute path from the project root
    base_path = project_root / f".marketflow/reports/{datetime.now().strftime('%Y-%m-%d')}/{sanitize_filename(ticker)}"

    print(f"Saving timeframe data for {ticker} to absolute path: {base_path}")
    base_path.mkdir(parents=True, exist_ok=True)

    if not timeframe_analyses:
        print(f"Warning: No timeframe analyses available for {ticker}. Skipping save.")
        return

    for timeframe, data in timeframe_analyses.items():
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if not isinstance(data, dict):
            print(f"Data for {ticker} - {timeframe} is not a dictionary. Skipping.")
            continue

        processed_data_dict = data.get("processed_data")
        if not isinstance(processed_data_dict, dict):
            print(f"Warning: 'processed_data' not found or not a dictionary for {timeframe} in {ticker}. Skipping.")
            continue
            
        # --- CORRECTED LOGIC ---
        # Directly use the pandas objects. The original code incorrectly tried to
        # deserialize them from a dict format which they were not in.
        price_data = processed_data_dict.get("price")  # This is a pd.DataFrame
        volume_data = processed_data_dict.get("volume") # This is a pd.Series

        # If volume is a Series, convert it to a DataFrame for merging.
        if isinstance(volume_data, pd.Series):
            volume_data = volume_data.to_frame(name='volume')

        # Validate that we have actual dataframes.
        price_data_valid = isinstance(price_data, pd.DataFrame) and not price_data.empty
        volume_data_valid = isinstance(volume_data, pd.DataFrame) and not volume_data.empty

        # Merge and save logic
        if price_data_valid and volume_data_valid:
            merged_data = pd.merge(price_data, volume_data, left_index=True, right_index=True, how='outer')
            file_path = base_path / f"{ticker}_{timeframe}.csv"
            merged_data.to_csv(file_path)
            print(f"✅ Saved {ticker} - {timeframe} merged data ({merged_data.shape[0]} rows) to {file_path}")
        elif price_data_valid:
            file_path = base_path / f"{ticker}_{timeframe}_price.csv"
            price_data.to_csv(file_path)
            print(f"✅ Saved {ticker} - {timeframe} price data only ({price_data.shape[0]} rows) to {file_path}")
        elif volume_data_valid:
            file_path = base_path / f"{ticker}_{timeframe}_volume_{date_str}.csv"
            volume_data.to_csv(file_path)
            print(f"✅ Saved {ticker} - {timeframe} volume data only ({volume_data.shape[0]} rows) to {file_path}")
        else:
            print(f"No valid price or volume data to save for {ticker} - {timeframe}.")

def make_higher_tf_state(enriched_df, lookback=40):
    df = enriched_df.copy()
    # EMAs for simple trend proxy
    df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    trend = "up" if df["ema20"].iloc[-1] > df["ema50"].iloc[-1] else ("down" if df["ema20"].iloc[-1] < df["ema50"].iloc[-1] else "flat")

    # Quartile on higher TF TR
    lo = float(df["tr_low"].iloc[-1]) if "tr_low" in df.columns else float(df["low"].tail(120).min())
    hi = float(df["tr_high"].iloc[-1]) if "tr_high" in df.columns else float(df["high"].tail(120).max())
    q = 0.5 if hi <= lo else (df["close"].iloc[-1] - lo) / (hi - lo)

    # Recent SOS/SOW on higher TF (either from confirmed or raw events if present)
    tail = df.tail(lookback)
    def _has(label):
        cols = [c for c in ["wyckoff_confirmed_event","wyckoff_event"] if c in tail.columns]
        if not cols: return False
        s = tail[cols[0]].astype(str)
        return s.str.contains(label, case=False, na=False).any()
    return {
        "trend": trend,
        "near_lower": q <= 0.25,
        "near_upper": q >= 0.75,
        "sow_recent": _has("SOW"),
        "sos_recent": _has("SOS"),
    }
