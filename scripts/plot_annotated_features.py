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

    # Plot Closed Price over Time
    fig = px.line(df, x='timestamp', y='close',
                  hover_data=['close'],
                  title=f"MarketFlow Closed Price {os.path.basename(csv_file)}",
                  labels={'timestamp': 'Timestamp', 'close': 'Closed Price'},
                  color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(xaxis_title="Timestamp", yaxis_title="Closed Price")
    fig.write_html("my_output_plot.html")
    logger.info("Plot saved as my_output_plot.html")
    fig.update_xaxes(rangeslider_visible=True)
    fig.show()

    # Plot Volume over Time
    fig = px.histogram(df, x= "timestamp", y='volume', nbins=150,
                       title="Volume Distribution Over Time",
                       labels={'timestamp': 'Timestamp', 'volume': 'Volume'},)
    fig.update_layout(xaxis_title="Timestamp", yaxis_title="Volume")
    fig.write_html("volume_distribution_plot.html")
    logger.info("Volume distribution plot saved as volume_distribution_plot.html")
    fig.show()

    # Plot Spread over Time
    fig = px.line(df, x='timestamp', y='spread', color='candle_class',
                  title="Spread Over Time",
                  color_discrete_sequence=px.colors.qualitative.Plotly,
                  hover_data=['spread'],
                  labels={'timestamp': 'Timestamp', 'spread': 'Spread'},)
    fig.update_layout(xaxis_title="Timestamp", yaxis_title="Spread")
    fig.write_html("spread_plot.html")
    logger.info("Spread plot saved as spread_plot.html")
    fig.show()

    if "volume_class" in features:
        fig = px.scatter(df, x='timestamp', y='close',
                      color='volume_class',
                      title="Volume Class Over Time",
                      labels={'timestamp': 'Timestamp', 'close': 'Closed Price'},
                        color_discrete_map={
                            "VERY_LOW": "blue", "LOW": "green", "AVERAGE": "yellow",
                            "HIGH": "orange", "VERY_HIGH": "red"
                        })
        fig.update_layout(xaxis_title="Timestamp", yaxis_title="Volume Class")
        fig.write_html("volume_class_plot.html")
        logger.info("Volume class plot saved as volume_class_plot.html")
        fig.show()

    if "candle_class" in features:
        # Plot the classified candles using Plotly
        fig = px.scatter(df, x='timestamp', y='close', color='candle_class',
                         title="Classified Candles",
                         labels={'Index (row)': 'Index (row)', 'close': 'Closed Price'},
                         color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(legend_title_text='Candle Classification')
        fig.write_html("classified_candles_plot.html")
        logger.info("Classified candles plot saved as classified_candles_plot.html")
        fig.show()

    if "price_direction" in features:
        # Plot the price direction using Plotly
        fig = px.scatter(df, x='timestamp', y='close', color='price_direction',
                         title="Price Direction",
                         labels={'Index (row)': 'Index (row)', 'close': 'Closed Price'},
                         color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(legend_title_text='Price Direction')
        fig.write_html("price_direction_plot.html")
        logger.info("Price direction plot saved as price_direction_plot.html")
        fig.show()

    if "volume_direction" in features:
        # Plot the volume direction using Plotly
        fig = px.scatter(df, x='timestamp', y='close', color='volume_direction',
                         title="Volume Direction",
                         labels={'Index (row)': 'Index (row)', 'close': 'Closed Price'},
                         color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(legend_title_text='Volume Direction')
        fig.write_html("volume_direction_plot.html")
        logger.info("Volume direction plot saved as volume_direction_plot.html")
        fig.show()

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
