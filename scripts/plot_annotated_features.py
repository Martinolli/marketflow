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
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import os

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
    output_dir = os.path.dirname(csv_file)

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

    # Plot Closed Price and Volume in the same frame (price above, volume below)
    # Limit to nrows
    df = df.head(nrows)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.05,
                        subplot_titles=("Closed Price", "Volume"))
    # Price (top)
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Closed Price'),
        row=1, col=1
    )
    # Volume (bottom)
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['volume'], name='Volume', marker_color='rgba(100,150,255,0.6)'),
        row=2, col=1
    )
    fig.update_layout(
        height=700,
        title_text=f"Closed Price and Volume - {os.path.basename(csv_file)}",
        xaxis2_title="Timestamp",
        yaxis_title="Closed Price",
        yaxis2_title="Volume"
    )
    fig.update_xaxes(rangeslider_visible=True, row=2, col=1)
    price_volume_path = os.path.join(output_dir, "price_volume_combined_plot.html")
    fig.write_html(price_volume_path)
    logger.info(f"Combined price and volume plot saved as {price_volume_path}")
    fig.show()

    # Plot Volume over Time
    fig = px.histogram(df, x= "timestamp", y='volume', nbins=150,
                       title=f"Volume Distribution Over Time {os.path.basename(csv_file)}",
                       labels={'timestamp': 'Timestamp', 'volume': 'Volume'},)
    fig.update_layout(xaxis_title="Timestamp", yaxis_title="Volume")
    fig.update_xaxes(rangeslider_visible=True)
    volume_dist_path = os.path.join(output_dir, "volume_distribution_plot.html")
    fig.write_html(volume_dist_path)
    logger.info(f"Volume distribution plot saved as {volume_dist_path}")
    fig.show()

    # Plot Spread over Time
    fig = px.line(df, x='timestamp', y='spread',
                  title=f"Spread Over Time {os.path.basename(csv_file)}",
                  color_discrete_sequence=px.colors.qualitative.Plotly,
                  hover_data=['spread'],
                  labels={'timestamp': 'Timestamp', 'spread': 'Spread'},)
    fig.update_layout(xaxis_title="Timestamp", yaxis_title="Spread")
    fig.update_xaxes(rangeslider_visible=True)
    spread_path = os.path.join(output_dir, "spread_plot.html")
    fig.write_html(spread_path)
    logger.info(f"Spread plot saved as {spread_path}")
    fig.show()

    if "volume_class" in features:
        fig = px.scatter(df, x='timestamp', y='close',
                      color='volume_class',
                      title=f"Volume Class Over Time {os.path.basename(csv_file)}",
                      labels={'timestamp': 'Timestamp', 'close': 'Closed Price'},
                        color_discrete_map={
                            "VERY_LOW": "blue", "LOW": "green", "AVERAGE": "yellow",
                            "HIGH": "orange", "VERY_HIGH": "red"
                        })
        fig.update_layout(xaxis_title="Timestamp", yaxis_title="Volume Class")
        fig.update_xaxes(rangeslider_visible=True)
        volume_class_path = os.path.join(output_dir, "volume_class_plot.html")
        fig.write_html(volume_class_path)
        logger.info(f"Volume class plot saved as {volume_class_path}")
        fig.show()

    if "candle_class" in features:
        # Plot the classified candles using Plotly
        fig = px.scatter(df, x='timestamp', y='close', color='candle_class',
                         title=f"Classified Candles {os.path.basename(csv_file)}",
                         labels={'Index (row)': 'Index (row)', 'close': 'Closed Price'},
                         color_discrete_sequence=px.colors.qualitative.Plotly,
                         hover_data=['candle_class'],
        )
        fig.update_layout(legend_title_text='Candle Classification')
        fig.update_xaxes(rangeslider_visible=True)
        candle_class_path = os.path.join(output_dir, "classified_candles_plot.html")
        fig.write_html(candle_class_path)
        logger.info(f"Classified candles plot saved as {candle_class_path}")
        fig.show()

    if "price_direction" in features:
        # Plot the price direction using Plotly
        fig = px.scatter(df, x='timestamp', y='close', color='price_direction',
                         title=f"Price Direction {os.path.basename(csv_file)}",
                         labels={'Index (row)': 'Index (row)', 'close': 'Closed Price'},
                         color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(legend_title_text='Price Direction')
        fig.update_xaxes(rangeslider_visible=True)
        price_direction_path = os.path.join(output_dir, "price_direction_plot.html")
        fig.write_html(price_direction_path)
        logger.info(f"Price direction plot saved as {price_direction_path}")
        fig.show()

    if "volume_direction" in features:
        # Plot the volume direction using Plotly
        fig = px.scatter(df, x='timestamp', y='close', color='volume_direction',
                         title=f"Volume Direction {os.path.basename(csv_file)}",
                         labels={'Index (row)': 'Index (row)', 'close': 'Closed Price'},
                         color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(legend_title_text='Volume Direction')
        fig.update_xaxes(rangeslider_visible=True)
        volume_direction_path = os.path.join(output_dir, "volume_direction_plot.html")
        fig.write_html(volume_direction_path)
        logger.info(f"Volume direction plot saved as {volume_direction_path}")
        fig.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot features from MarketFlow annotated CSV.")
    parser.add_argument("csv", type=str, help="Path to annotated CSV file")
    parser.add_argument("--features", type=str, nargs="*", default=None,
                        help="Features/columns to plot (e.g., close spread volume_class)")
    parser.add_argument("--nrows", type=int, default=100,
                        help="Number of rows to plot (default 100)")
    args = parser.parse_args()
    plot_features(args.csv, args.features, args.nrows)
