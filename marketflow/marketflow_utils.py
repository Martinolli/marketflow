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
    
def save_timeframe_data(ticker: str, timeframe_data: dict) -> None:
    """
    Save timeframe data to disk.

    Parameters:
    - ticker: Stock symbol (e.g., 'AAPL', 'MSFT')
    - timeframe_data: Dictionary with timeframe as key and DataFrame as value

    Returns:
    - None
    """
    base_path = Path("data/timeframe_data")
    base_path.mkdir(parents=True, exist_ok=True)

    for timeframe, data in timeframe_data.items():
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        price_data = data.get('price_data')
        volume_data = data.get('volume_data')

        if price_data is not None and not price_data.empty:
            file_path = base_path / f"{ticker}_{timeframe}_price_{date_str}.csv"
            price_data.to_csv(file_path)
            print(f"Saved {ticker} - {timeframe} price data to {file_path}")

        if volume_data is not None and not volume_data.empty:
            file_path = base_path / f"{ticker}_{timeframe}_volume_{date_str}.csv"
            volume_data.to_csv(file_path)
            print(f"Saved {ticker} - {timeframe} volume data to {file_path}")