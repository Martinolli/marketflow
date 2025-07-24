"""
This module provides a function to plot market flow features from a CSV file.
It reads the CSV file, extracts specified features, and plots them using matplotlib.

Usage:
    python scripts/plot_annotated_features.py ".marketflow/reports/X_BTCUSD/your_file.csv"
    python scripts/plot_annotated_features.py ".marketflow/reports/X_BTCUSD/your_file.csv" --features close spread volume_class
    python scripts/plot_annotated_features.py ".marketflow/reports/X_BTCUSD/your_file.csv" --nrows 200

    python scripts/plot_annotated_features.py ".marketflow/reports/X_BTCUSD/your_file.csv" --features close spread volume --nrows 200
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import argparse

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("plot_annotated_features")
config_manager = create_app_config(logger=logger)


def plot_features(csv_file, features=None, nrows=100):
    """Plot features from a MarketFlow annotated CSV file.
    Args:
        csv_file (str): Path to the annotated CSV file.
        features (list, optional): List of features/columns to plot. If None, defaults to ['close', 'spread', 'volume'].
        nrows (int): Number of rows to plot from the CSV file.
    """

    logger.info(f"Loading data from {csv_file}...")
    if not os.path.exists(csv_file):
        logger.error(f"File {csv_file} does not exist.")
        return
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    logger.info(f"Data loaded successfully with {len(df)} rows.")

    # Check if the specified features are in the DataFrame
    if features is None:
        # Default: plot close, spread, and volume
        features = ["close", "spread", "volume"]
        logger.info("No features specified, using default: close, spread, volume.")
    else:
        logger.info(f"Features to plot: {features}")

    # Plot the specified features
    plt.figure(figsize=(12, 6))
    for feature in features:
        if feature in df.columns:
            plt.plot(df[feature][:nrows], label=feature)
    plt.xlabel("Index (row)")
    plt.ylabel("Value")
    plt.title(f"MarketFlow Features from {os.path.basename(csv_file)}")
    plt.legend()
    plt.tight_layout()
    plt.savefig("my_output_plot.png", dpi=150)
    logger.info("Plot saved as my_output_plot.png")
    plt.show()

    if "volume_class" in features:
        # Define the order and numeric mapping for volume_class
        categories = ["VERY_LOW", "LOW", "AVERAGE", "HIGH", "VERY_HIGH"]
        cat2num = {cat: i for i, cat in enumerate(categories)}

        # Map to numeric codes
        df['volume_class_code'] = df['volume_class'].map(cat2num)

        fig, ax1 = plt.subplots(figsize=(16,6))
        ax1.plot(df['close'][:nrows], color='gray', alpha=0.6, label="Close Price")
        ax2 = ax1.twinx()
        ax2.plot(df['volume_class_code'][:nrows], color='blue', label="Volume Class (numeric)")
        ax2.set_yticks(range(len(categories)))
        ax2.set_yticklabels(categories)
        ax1.set_xlabel("Index (row)")
        ax1.set_ylabel("Close Price")
        ax2.set_ylabel("Volume Class")
        plt.title("Price and Volume Class Over Time")
        fig.tight_layout()
        plt.savefig("my_output_plot.png", dpi=150)
        logger.info("Volume class plot saved as my_output_plot.png")
        plt.show()

if __name__ == "__main__":
    import os
    parser = argparse.ArgumentParser(description="Plot features from MarketFlow annotated CSV.")
    parser.add_argument("csv", type=str, help="Path to annotated CSV file")
    parser.add_argument("--features", type=str, nargs="*", default=None,
                        help="Features/columns to plot (e.g., close spread volume_class)")
    parser.add_argument("--nrows", type=int, default=100,
                        help="Number of rows to plot (default 100)")
    args = parser.parse_args()
    plot_features(args.csv, args.features, args.nrows)
