"""
This module provides a function to plot market flow features from a CSV file.
It reads the CSV file, extracts specified features, and plots them using matplotlib.

New features include:
- Volume Profile (Volume by Price) chart.
- Point & Figure (P&F) chart.

Usage:
    python plot_annotated_features.py ".marketflow/reports/2025-09-04/AVAV/AVAV_1m_wyckoff_annotated.csv"
    python plot_annotated_features.py ".marketflow/reports/X_BTCUSD/your_file.csv" --features close spread volume_class
    python plot_annotated_features.py ".marketflow/reports/X_BTCUSD/your_file.csv" --nrows 200
    python plot_annotated_features.py ".marketflow/reports/X_BTCUSD/your_file.csv" --features close spread volume --nrows 200

    # P&F Chart Usage
    python plot_annotated_features.py "path/to/your.csv" --nrows 500 --box-size 1.0 --reversal 3

    # Generate all plots for the first 200 rows of the CSV
    # The P&F box size will be auto-calculated
    python plot_annotated_features.py "LLY_5m_wyckoff_annotated.csv" --nrows 200

    # Specify a manual box size and reversal amount for the P&F chart
    # This is useful when you want to analyze with specific P&F parameters
    python plot_annotated_features.py "LLY_5m_wyckoff_annotated.csv" --nrows 200 --box-size 0.5 --reversal 3

    # Use it with other feature flags as before
    python plot_annotated_features.py "LLY_5m_wyckoff_annotated.csv" --nrows 150 --features close volume_class
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import argparse
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import os

# Assuming marketflow is a local package or installed
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("plot_annotated_features")
config_manager = create_app_config(logger=logger)


def plot_volume_profile(df, output_dir):
    """
    Plots a Volume Profile (Volume by Price) chart.

    Args:
        df (pd.DataFrame): The input dataframe with price and volume data.
        output_dir (str): The directory to save the output HTML file.
    """
    logger.info("Generating Volume Profile chart...")
    price_range = df['high'].max() - df['low'].min()
    # Define the number of bins for the price levels
    num_bins = 100
    bin_size = price_range / num_bins
    bins = np.arange(df['low'].min(), df['high'].max(), bin_size)
    
    volume_by_price = pd.Series(index=bins, data=np.zeros(len(bins)))

    # Distribute volume across price bins for each candle
    for _, row in df.iterrows():
        low_price, high_price, volume = row['low'], row['high'], row['volume']
        if volume > 0 and high_price > low_price:
            # Find bins that this candle's range covers
            relevant_bins = volume_by_price.index[(volume_by_price.index >= low_price) & (volume_by_price.index < high_price)]
            if len(relevant_bins) > 0:
                # Distribute volume equally among the covered bins
                volume_per_bin = volume / len(relevant_bins)
                volume_by_price.loc[relevant_bins] += volume_per_bin
    
    # Create the plot
    fig = go.Figure(go.Bar(
        y=volume_by_price.index,
        x=volume_by_price.values,
        orientation='h',
        marker_color='rgba(100,100,100,0.6)'
    ))
    
    fig.update_layout(
        title=f"Volume Profile (Volume by Price) - {os.path.basename(output_dir)}",
        xaxis_title="Volume",
        yaxis_title="Price Level",
        yaxis=dict(tickformat=".2f"),
        bargap=0.01
    )
    
    profile_path = os.path.join(output_dir, "volume_profile_plot.html")
    fig.write_html(profile_path)
    logger.info(f"Volume Profile plot saved as {profile_path}")
    fig.show()


def plot_point_and_figure(df, output_dir, box_size=None, reversal=3):
    """
    Generates and plots a Point & Figure (P&F) chart.

    Args:
        df (pd.DataFrame): Input dataframe with high and low prices.
        output_dir (str): Directory to save the output HTML file.
        box_size (float, optional): The size of each box. If None, it's auto-calculated.
        reversal (int, optional): The reversal amount in boxes (typically 3).
    """
    logger.info("Generating Point & Figure chart...")

    if box_size is None:
        if 'atr14' in df.columns and df['atr14'].iloc[-1] > 0:
            box_size = round(df['atr14'].mean(), 2)
            logger.info(f"Auto-detected box_size based on ATR: {box_size}")
        else:
            box_size = round((df['high'] - df['low']).mean(), 2)
            logger.info(f"Auto-detected box_size based on average candle spread: {box_size}")
        if box_size == 0:
            box_size = 1.0 # Fallback
            logger.warning("Could not determine a valid box_size, falling back to 1.0")


    highs = df['high']
    lows = df['low']
    
    pnf_columns = []
    current_col = []
    direction = 0  # 1 for up (X), -1 for down (O)
    
    start_price = highs.iloc[0]
    box_floor = np.floor(start_price / box_size) * box_size
    box_ceil = box_floor + box_size

    for i in range(1, len(df)):
        high = highs.iloc[i]
        low = lows.iloc[i]

        if direction == 0: # Undetermined trend
            if high >= box_ceil + (reversal - 1) * box_size:
                direction = 1
                current_col.append(box_ceil)
                box_floor = box_ceil
                box_ceil += box_size
            elif low < box_floor - (reversal - 1) * box_size:
                direction = -1
                current_col.append(box_floor)
                box_ceil = box_floor
                box_floor -= box_size
        
        if direction == 1: # Up-trend (X column)
            # Add new boxes if price continues up
            while high >= box_ceil:
                current_col.append(box_ceil)
                box_floor = box_ceil
                box_ceil += box_size
            
            # Check for reversal
            if low < box_floor - (reversal - 1) * box_size:
                pnf_columns.append({'type': 'X', 'values': current_col})
                direction = -1
                start_rev_box = box_floor - box_size
                current_col = [start_rev_box]
                box_ceil = start_rev_box
                box_floor = start_rev_box - box_size
                # Add more boxes if reversal is large
                while low < box_floor:
                    current_col.append(box_floor)
                    box_ceil = box_floor
                    box_floor -= box_size
        
        elif direction == -1: # Down-trend (O column)
            # Add new boxes if price continues down
            while low < box_floor:
                current_col.append(box_floor)
                box_ceil = box_floor
                box_floor -= box_size
            
            # Check for reversal
            if high >= box_ceil + (reversal - 1) * box_size:
                pnf_columns.append({'type': 'O', 'values': current_col})
                direction = 1
                start_rev_box = box_ceil + box_size
                current_col = [start_rev_box]
                box_floor = start_rev_box
                box_ceil = start_rev_box + box_size
                # Add more boxes if reversal is large
                while high >= box_ceil:
                    current_col.append(box_ceil)
                    box_floor = box_ceil
                    box_ceil += box_size

    # Add the last column
    if current_col:
        pnf_columns.append({'type': 'X' if direction == 1 else 'O', 'values': current_col})

    # Prepare data for plotting
    fig = go.Figure()
    for i, col_data in enumerate(pnf_columns):
        x_vals = [i + 1] * len(col_data['values'])
        y_vals = col_data['values']
        
        if col_data['type'] == 'X':
            fig.add_trace(go.Scatter(
                x=x_vals, y=y_vals, mode='markers',
                marker=dict(symbol='x', color='green', size=8),
                name='Up Column' if i == 0 else '', showlegend=(i==0)
            ))
        else:
            fig.add_trace(go.Scatter(
                x=x_vals, y=y_vals, mode='markers',
                marker=dict(symbol='circle-open', color='red', size=8, line=dict(width=2)),
                name='Down Column' if any(c['type'] == 'X' for c in pnf_columns[:i+1]) == False else '', showlegend=(any(c['type'] == 'O' for c in pnf_columns[:i]))==False
            ))
            
    fig.update_layout(
        title=f"Point & Figure Chart (Box Size: {box_size}, Reversal: {reversal}) - {os.path.basename(output_dir)}",
        xaxis_title="Column",
        yaxis_title="Price",
        yaxis=dict(tickformat=".2f", gridwidth=1, gridcolor='LightGrey'),
        xaxis=dict(gridwidth=1, gridcolor='LightGrey', dtick=1)
    )
    
    pnf_path = os.path.join(output_dir, "point_and_figure_plot.html")
    fig.write_html(pnf_path)
    logger.info(f"Point & Figure plot saved as {pnf_path}")
    fig.show()


def plot_features(csv_file, features=None, nrows=4000, box_size=None, reversal=3):
    """Plot features from a MarketFlow annotated CSV file.
    Args:
        csv_file (str): Path to the annotated CSV file.
        features (list, optional): List of features/columns to plot. If None, defaults to ['close', 'spread', 'volume'].
        nrows (int): Number of rows to plot from the CSV file.
        box_size (float, optional): Box size for P&F chart.
        reversal (int, optional): Reversal amount for P&F chart.
    """
    output_dir = os.path.dirname(csv_file)

    logger.info(f"Loading data from {csv_file}...")
    if not os.path.exists(csv_file):
        logger.error(f"File {csv_file} does not exist.")
        return
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    logger.info(f"Data loaded successfully with {len(df)} rows.")
    
    # Limit to nrows
    df = df.tail(nrows)

    # NEW: Plot Volume Profile
    plot_volume_profile(df.copy(), output_dir)

    # NEW: Plot Point & Figure Chart
    plot_point_and_figure(df.copy(), output_dir, box_size=box_size, reversal=reversal)

    # Check if the specified features are in the DataFrame
    if features is None:
        # Default: plot close, spread, and volume
        features = ["close", "spread", "volume"]
        logger.info("No features specified, using default: close, spread, volume.")
    else:
        logger.info(f"Features to plot: {features}")

    # Plot Closed Price and Volume in the same frame (price above, volume below)
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
    fig.update_xaxes(type='date', rangeslider_visible=True, row=2, col=1)
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

def main():
    parser = argparse.ArgumentParser(description="Plot features from MarketFlow annotated CSV.")
    parser.add_argument("csv", type=str, help="Path to annotated CSV file")
    parser.add_argument("--features", type=str, nargs="*", default=None,
                        help="Features/columns to plot (e.g., close spread volume_class)")
    parser.add_argument("--nrows", type=int, default=4000,
                        help="Number of rows to plot (default 4000)")
    # New arguments for Point & Figure Chart
    parser.add_argument("--box-size", type=float, default=None,
                        help="Box size for the Point & Figure chart. Default is auto-calculated.")
    parser.add_argument("--reversal", type=int, default=3,
                        help="Reversal amount in boxes for the P&F chart (default 3)")
    args = parser.parse_args()
    plot_features(args.csv, args.features, args.nrows, args.box_size, args.reversal)

if __name__ == "__main__":
    main()