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
import datetime

# Assuming marketflow is a local package or installed
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("plot_annotated_features")
config_manager = create_app_config(logger=logger)


class PlotAnnotations:
    def __init__(self, df, output_dir, csv_file_name):
        self.df = df
        self.output_dir = output_dir
        self.csv_file_name = csv_file_name

        self.logger = get_logger("plot_annotated_features")
        self.config_manager = create_app_config(logger=self.logger)

    def plot_volume_profile(self, df: pd.DataFrame, output_dir: str, csv_file_name: str) -> None:
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
            marker_color='rgba(252,100,100,100)'
        ))
        
        fig.update_layout(
            title=f"Volume Profile (Volume by Price) - {csv_file_name}",
            xaxis_title="Volume",
            yaxis_title="Price Level",
            yaxis=dict(tickformat=".2f"),
            bargap=0.01
        )

        profile_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_volume_profile_plot.html")
        fig.write_html(profile_path)
        logger.info(f"Volume Profile plot saved as {profile_path}")
        fig.show()

    def add_wyckoff_phase_overlay_pnf(self, fig: go.Figure, df_with_cols: pd.DataFrame) -> None:
        """
        Overlay Wyckoff phases on a P&F chart that uses integer column indices.
        Expects columns: wyckoff_phase, pnf_column.
        """
        if 'wyckoff_phase' not in df_with_cols.columns or 'pnf_column' not in df_with_cols.columns:
            return
        phase_colors = {
            "A": "rgba(0, 2, 252, 1)",  # BLUE
            "B": "rgba(252, 19, 0, 1)",  # RED
            "C": "rgba(0, 255, 0, 1)",  # GREEN
            "D": "rgba(255, 242, 0, 1)",  # YELLOW
            "E": "rgba(163, 0, 255, 1)"  # PURPLE
        }
        for phase, color in phase_colors.items():
            phase_df = df_with_cols[df_with_cols['wyckoff_phase'] == phase]
            if phase_df.empty:
                continue
            x0 = phase_df['pnf_column'].min() - 0.5
            x1 = phase_df['pnf_column'].max() + 0.5
            fig.add_vrect(
                x0=x0, x1=x1,
                fillcolor=color,
                opacity=1.0,
                layer="below",
                line_width=0
            )

    def plot_point_and_figure(self, df: pd.DataFrame, output_dir: str, csv_file_name: str, box_size: float = None, reversal: int = 3, wyckoff_overlay: bool = False) -> None:
        """
        Generates and plots a Point & Figure (P&F) chart.

        Args:
            df (pd.DataFrame): Input dataframe with high and low prices.
            output_dir (str): Directory to save the output HTML file.
            box_size (float, optional): The size of each box. If None, it's auto-calculated.
            reversal (int, optional): The reversal amount in boxes (typically 3).
            wyckoff_overlay (bool): If True and 'wyckoff_phase' present, overlay phases.
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

        # Track which P&F column each row belongs to
        row_column_index = [0] * len(df)
        column_index = 0


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

            row_column_index[i] = column_index

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

        if wyckoff_overlay and 'wyckoff_phase' in df.columns:
            df_cols = df.copy()
            df_cols['pnf_column'] = row_column_index
            self.add_wyckoff_phase_overlay_pnf(fig, df_cols)

        fig.update_layout(
            title=f"Point & Figure Chart - Box Size: {box_size}, Reversal: {reversal} - {csv_file_name}",
            xaxis_title="P&F Column",
            yaxis_title="Price",
            yaxis=dict(tickformat=".2f", gridwidth=1, gridcolor='LightGrey'),
            xaxis=dict(gridwidth=1, gridcolor='LightGrey', dtick=1)
        )

        pnf_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_point_and_figure_plot.html")
        fig.write_html(pnf_path)
        logger.info(f"Point & Figure plot saved as {pnf_path}")
        fig.show()

    def plot_wyckoff_candlestick_chart(self, df: pd.DataFrame, output_dir: str, csv_file_name: str) -> None:
        """
        Generates a comprehensive candlestick chart with Wyckoff phases and event annotations.
        """
        logger.info("Generating annotated Wyckoff Candlestick chart...")

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03,
                            subplot_titles=(f"Wyckoff Analysis: {csv_file_name}", "Volume"),
                            row_heights=[0.7, 0.3])

        # 1. Candlestick chart
        fig.add_trace(go.Ohlc(x=df['timestamp'],
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close'],
                                    name='Price'),
                    row=1, col=1)

        # 2. Volume chart with color coding
        colors = ['green' if row['close'] >= row['open'] else 'red' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(x=df['timestamp'], y=df['volume'],
                            marker_color=colors,
                            name='Volume'),
                    row=2, col=1)

        # 3. Add Wyckoff Phase overlays
        phase_colors = {
            "A": "rgba(255, 165, 0, 0.1)", "B": "rgba(0, 0, 255, 0.1)",
            "C": "rgba(128, 0, 128, 0.1)", "D": "rgba(0, 128, 0, 0.1)",
            "E": "rgba(139, 69, 19, 0.1)", "UNKNOWN": "rgba(128, 128, 128, 0.05)"
        }
        
        df['phase_shifted'] = df['wyckoff_phase'].shift(1)
        phase_changes = df[df['wyckoff_phase'] != df['phase_shifted']]

        for i in range(len(phase_changes)):
            start_date = phase_changes.iloc[i]['timestamp']
            phase = phase_changes.iloc[i]['wyckoff_phase']
            end_date = df.iloc[-1]['timestamp'] if i == len(phase_changes) - 1 else phase_changes.iloc[i+1]['timestamp']
            
            fig.add_vrect(x0=start_date, x1=end_date,
                        fillcolor=phase_colors.get(phase, "rgba(200,200,200,0.1)"),
                        opacity=0.5, layer="below", line_width=0,
                        annotation_text=f"Phase {phase}", annotation_position="top left",
                        row=1, col=1)

        # 4. Add Event Annotations
        df_events = df.dropna(subset=['wyckoff_event', 'wyckoff_confirmed_event'], how='all')
        df_events = df_events[ (df_events['wyckoff_event'] != '') | (df_events['wyckoff_confirmed_event'] != '')]

        for index, row in df_events.iterrows():
            event_text = str(row['wyckoff_event'] or '')
            confirmed_event_text = str(row['wyckoff_confirmed_event'] or '')

            # Combine and prioritize confirmed events
            full_text = f"<b>{confirmed_event_text}</b>" if confirmed_event_text else event_text
            if confirmed_event_text and event_text:
                full_text = f"<b>{confirmed_event_text}</b><br>({event_text})"
            
            # Determine annotation position (above high or below low)
            is_bullish = any(e in full_text for e in ["SPRING", "SOS", "JAC", "LPS", "SC"])
            y_pos = row['low'] - (df['high'].max() - df['low'].min()) * 0.05 if is_bullish else \
                    row['high'] + (df['high'].max() - df['low'].min()) * 0.05
            ay = -40 if is_bullish else 40
            
            fig.add_annotation(x=row['timestamp'], y=y_pos,
                            ax=0, ay=ay,
                            text=full_text,
                            arrowhead=2, arrowsize=1, arrowwidth=2,
                            bordercolor="#c7c7c7", borderwidth=2, borderpad=4,
                            bgcolor="rgba(255,255,141,0.8)",
                            row=1, col=1)

        # 5. Add Trading Range lines
        if 'tr_low' in df.columns and 'tr_high' in df.columns:
            tr_low = df['tr_low'].iloc[-1]
            tr_high = df['tr_high'].iloc[-1]
            if pd.notna(tr_low) and pd.notna(tr_high):
                fig.add_hline(y=tr_low, line_dash="dash", line_color="red",
                                annotation_text=f"TR Support {tr_low:.2f}",
                                annotation_position="bottom right", row=1, col=1)
                fig.add_hline(y=tr_high, line_dash="dash", line_color="green",
                                annotation_text=f"TR Resistance {tr_high:.2f}",
                                annotation_position="top right", row=1, col=1)

        # Final layout updates
        fig.update_layout(
            height=800,
            showlegend=False,
            xaxis_rangeslider_visible=False,
            xaxis2_rangeslider_visible=True,
        )
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        chart_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_wyckoff_candlestick_chart.html")
        fig.write_html(chart_path)
        logger.info(f"Wyckoff candlestick chart saved as {chart_path}")
        fig.show()

    def plot_features(self, csv_file: str, features: list = None, nrows: int = 4000, box_size: float = None, reversal: int = 3) -> None:
        """Plot features from a MarketFlow annotated CSV file.
        Args:
            csv_file (str): Path to the annotated CSV file.
            features (list, optional): List of features/columns to plot. If None, defaults to ['close', 'spread', 'volume'].
            nrows (int): Number of rows to plot from the CSV file.
            box_size (float, optional): Box size for P&F chart.
            reversal (int, optional): Reversal amount for P&F chart.
        """
        output_dir = os.path.dirname(csv_file)
        csv_file_name = os.path.basename(csv_file)

        logger.info(f"Loading data from {csv_file}...")
        if not os.path.exists(csv_file):
            logger.error(f"File {csv_file} does not exist.")
            return
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        # Convert timestamp to datetime object for Plotly
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        logger.info(f"Data loaded successfully with {len(df)} rows.")
        
        # Limit to nrows
        if nrows < len(df):
            df = df.tail(nrows).copy()
        else:
            df = df.copy()

        # Call the new comprehensive chart function
        self.plot_wyckoff_candlestick_chart(df, output_dir, csv_file_name)

        # NEW: Plot Volume Profile
        self.plot_volume_profile(df.copy(), output_dir, csv_file_name)

        # NEW: Plot Point & Figure Chart
        self.plot_point_and_figure(df.copy(), output_dir, csv_file_name, box_size=box_size, reversal=reversal, wyckoff_overlay=True)

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
        price_volume_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_price_volume_combined_plot.html")
        fig.write_html(price_volume_path)
        logger.info(f"Combined price and volume plot saved as {price_volume_path}")
        fig.show()

        # Plot Volume over Time
        fig = px.histogram(df, x= "timestamp", y='volume', nbins=150,
                        title=f"Volume Distribution Over Time {os.path.basename(csv_file)}",
                        labels={'timestamp': 'Timestamp', 'volume': 'Volume'},)
        fig.update_layout(xaxis_title="Timestamp", yaxis_title="Volume")
        fig.update_xaxes(rangeslider_visible=True)
        volume_dist_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_volume_distribution_plot.html")
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
        spread_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_spread_plot.html")
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
            volume_class_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_volume_class_plot.html")
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
            candle_class_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_classified_candles_plot.html")
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
            price_direction_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_price_direction_plot.html")
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
            volume_direction_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_volume_direction_plot.html")
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
    plot = PlotAnnotations(None, None, None)
    plot.plot_features(args.csv, args.features, args.nrows, args.box_size, args.reversal)

if __name__ == "__main__":
    main()