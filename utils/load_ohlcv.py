"""
Utility functions for MarketFlow.

Includes functions to load OHLCV data, infer timeframes, and calibrate parameters.
"""

import os
import pandas as pd
import numpy as np


def load_ohlcv(csv_path: str, nrows: int | None = None) -> pd.DataFrame:
        """
        Load OHLCV data from a CSV file.
        Parameters
        ----------
        csv_path: str
            Path to the CSV file.
        nrows: int | None
            Number of rows to read from the CSV file. If None, read all rows.
        Returns
        -------
        pd.DataFrame
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(csv_path)
        df = pd.read_csv(csv_path)
        for col in ["timestamp", "open", "high", "low", "close", "volume"]:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
        if nrows is not None and len(df) > nrows:
            df = df.tail(nrows)
        df = df.reset_index(drop=True)
        return df