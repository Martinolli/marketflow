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

from rag.embedder_vector_db import embed_batch

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

def embed_fn(text):
    # The model name must match your embedding dimension (1536 for text-embedding-3-small)
    return embed_batch([text], model="text-embedding-3-small")[0]

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
    base_path = project_root / f"data/timeframe_data/{sanitize_filename(ticker)}"

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
            file_path = base_path / f"{timeframe}_{date_str}.csv"
            merged_data.to_csv(file_path)
            print(f"✅ Saved {ticker} - {timeframe} merged data ({merged_data.shape[0]} rows) to {file_path}")
        elif price_data_valid:
            file_path = base_path / f"{timeframe}_price_{date_str}.csv"
            price_data.to_csv(file_path)
            print(f"✅ Saved {ticker} - {timeframe} price data only ({price_data.shape[0]} rows) to {file_path}")
        elif volume_data_valid:
            file_path = base_path / f"{timeframe}_volume_{date_str}.csv"
            volume_data.to_csv(file_path)
            print(f"✅ Saved {ticker} - {timeframe} volume data only ({volume_data.shape[0]} rows) to {file_path}")
        else:
            print(f"No valid price or volume data to save for {ticker} - {timeframe}.")