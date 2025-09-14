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

from html import parser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import argparse
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import os, json
import datetime

# Assuming marketflow is a local package or installed
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_data_parameters import MarketFlowDataParameters

logger = get_logger("plot_annotated_features")
config_manager = create_app_config(logger=logger)


def plot_volume_profile(df: pd.DataFrame, output_dir: str, csv_file_name: str) -> None:
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

def add_wyckoff_phase_overlay_pnf(fig: go.Figure, df_with_cols: pd.DataFrame) -> None:
    """
    Overlay Wyckoff phases on a P&F chart that uses integer column indices.
    Expects columns: wyckoff_phase, pnf_column.
    """
    if 'wyckoff_phase' not in df_with_cols.columns or 'pnf_column' not in df_with_cols.columns:
        return
    phase_colors = {
        "A": "rgba(0, 2, 252, 0.4)",  # BLUE
        "B": "rgba(252, 19, 0, 0.5)",  # RED
        "C": "rgba(0, 255, 0, 0.4)",  # GREEN
        "D": "rgba(255, 242, 0, 0.5)",  # YELLOW
        "E": "rgba(163, 0, 255, 0.3)"  # PURPLE
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
# --- P&F helpers -------------------------------------------------------------

from dataclasses import dataclass

@dataclass
class PnFParams:
    box: float
    reversal: int = 3
    method: str = "high_low"  # "close" also allowed

def _compute_box(df: pd.DataFrame, mode="fixed", value=1.0, atr_len=14) -> float:
    """
    mode: "fixed" (points), "percent" (e.g. 0.005 = 0.5%), "atr" (fraction of ATR)
    """
    last = float(df["close"].iloc[-1])
    if mode == "fixed":
        return float(value)
    if mode == "percent":
        return max(1e-6, last * float(value))
    if mode == "atr":
        tr = np.maximum(df["high"]-df["low"],
                        np.maximum(abs(df["high"]-df["close"].shift(1)),
                                   abs(df["low"]-df["close"].shift(1))))
        atr = pd.Series(tr).rolling(int(atr_len), min_periods=int(atr_len)).mean().iloc[-1]
        return max(1e-6, float(value) * float(atr))
    raise ValueError("mode must be fixed|percent|atr")

def _snap(price, box, up=None):
    """Snap to grid. up=True => ceil; up=False => floor; up=None => round."""
    q = price / box
    if up is True:  return np.ceil(q) * box
    if up is False: return np.floor(q) * box
    return np.round(q) * box

def _build_pnf_columns(df: pd.DataFrame, params: PnFParams) -> tuple[list[dict], np.ndarray]:
    """
    Classic high/low P&F with 3-box reversal (default).
    Returns: columns[], row_column_index[]
    Each column: {"type":"X|O", "high":float, "low":float, "boxes":int}
    """
    hi = df["high"].to_numpy()
    lo = df["low"].to_numpy()
    cl = df["close"].to_numpy()

    # Anchor on first close snapped to grid
    anchor = _snap(cl[0], params.box, False)
    columns = []
    
    direction = 0  # 0 unknown, +1 X, -1 O
    col = {"type":"X", "high":anchor, "low":anchor, "boxes":1}  # start with 1-box X anchor
    columns.append(col)

    row_col_idx = np.zeros(len(df), dtype=int)
    col_idx = 0

    for i in range(1, len(df)):
        # bar extremes
        bar_hi = float(hi[i]) if params.method == "high_low" else float(cl[i])
        bar_lo = float(lo[i]) if params.method == "high_low" else float(cl[i])

        col = columns[-1]
        if col["type"] == "X":
            # try to extend up
            while bar_hi >= col["high"] + params.box:
                col["high"] += params.box
                col["boxes"] += 1
            # check reversal: >= reversal boxes below the column high
            if bar_lo <= col["high"] - params.reversal * params.box:
                # finish X column, start O one box below previous high
                new_low = col["high"] - params.box
                boxes = int(np.floor((col["high"] - bar_lo) / params.box))
                boxes = max(1, boxes)  # at least one box prints
                columns.append({"type":"O", "high":new_low, "low":new_low - (boxes-1)*params.box, "boxes":boxes})
                col_idx += 1
        else:
            # current O column: extend down
            while bar_lo <= col["low"] - params.box:
                col["low"] -= params.box
                col["boxes"] += 1
            # check reversal up
            if bar_hi >= col["low"] + params.reversal * params.box:
                new_high = col["low"] + params.box
                boxes = int(np.floor((bar_hi - col["low"]) / params.box))
                boxes = max(1, boxes)
                columns.append({"type":"X", "high":new_high + (boxes-1)*params.box, "low":new_high, "boxes":boxes})
                col_idx += 1

        row_col_idx[i] = col_idx

    return columns, row_col_idx

def _find_breakouts(columns: list[dict], box: float, reversal: float) -> list[dict]:
    brks = []
    tops, bots = [], []
    for i, c in enumerate(columns):
        if c["type"] == "X":
            tops.append((i, c["high"]))
            prev_top = max([h for _, h in tops[:-1]] or [-np.inf])
            if c["high"] >= prev_top:
                kind = "double_top" if [h for _, h in tops[:-1]].count(prev_top) == 1 else "triple_top_or_more"
                brks.append({"i": i, "type": kind, "price": c["high"]})
                # Upthrust: immediate O-column erases ≥ reversal boxes beneath the breakout
                if i + 1 < len(columns) and columns[i + 1]["type"] == "O":
                    if columns[i + 1]["high"] <= c["high"] - reversal * box:
                        brks.append({"i": i + 1, "type": "upthrust", "price": columns[i + 1]["high"], "ref": c["high"]})
        else:
            bots.append((i, c["low"]))
            prev_bot = min([l for _, l in bots[:-1]] or [np.inf])
            if c["low"] <= prev_bot:
                kind = "double_bottom" if [l for _, l in bots[:-1]].count(prev_bot) == 1 else "triple_bottom_or_more"
                brks.append({"i": i, "type": kind, "price": c["low"]})


def _last_congestion_count(columns: list[dict], box: float, reversal: float, direction="up", max_cols=9) -> dict | None:
    """Conservative count over the most recent congestion."""
    if len(columns) < 6:
        return None
    end = len(columns) - 1
    start = max(0, end - max_cols)
    cols_slice = columns[start:end+1]
    ncols = len(cols_slice)
    if direction == "up":
        breakout = max(c["high"] for c in columns if c["type"]=="X")
        objective = breakout + ncols * box * reversal
    else:
        breakout = min(c["low"] for c in columns if c["type"]=="O")
        objective = breakout - ncols * box * reversal
    return {"start":start, "end":end, "columns":ncols, "breakout":breakout, "objective":objective}

# --- MC POP gauge helpers ----------------------------------------------------

def _load_latest_mc_for(csv_path: str, directory: str) -> dict | None:
    """Return the newest MC summary whose 'csv' matches the given CSV (robust name normalization).
    
    Matches case-insensitively and ignores suffixes like '_wyckoff_annotated' or '_annotated'.
    Examples matched as equal:
      - 'PANW_1d_wyckoff_annotated.csv'  <->  'PANW_1d.csv' (or 'PANW_1D.csv')
    """
    def _norm(name: str) -> str:
        b = os.path.basename(name).lower()
        if b.endswith(".csv"):
            b = b[:-4]
        # strip common suffixes added by pipelines
        for suf in ("_wyckoff_annotated", "_annotated", "_wyckoff"):
            if b.endswith(suf):
                b = b[: -len(suf)]
        # collapse double underscores, keep symbol_tf shape
        while "__" in b:
            b = b.replace("__", "_")
        return b  # without .csv

    try:
        files = [f for f in os.listdir(directory) if f.endswith("_mc_summary.json")]
        files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
        want_norm = _norm(csv_path)
        for fn in files:
            try:
                fp = os.path.join(directory, fn)
                with open(fp, "r") as fh:
                    data = json.load(fh)
                mc_csv = data.get("csv")
                if not mc_csv:
                    continue
                if _norm(mc_csv) == want_norm:
                    return data
            except Exception:
                continue
    except Exception:
        pass
    return None

def add_pop_gauge(fig: go.Figure, mc_data: dict | None, corner: str = "br") -> None:
    """Overlay a small POP gauge (TP-first %) and median bars-to-TP on the figure."""
    if not mc_data:
        return
    m = mc_data.get("metrics_from_now", {})
    pop = m.get("pop_tp_first")
    if pop is None:
        return
    # corner placement (domain in paper coords)
    corners = {
        "br": dict(x=[0.80, 0.99], y=[0.03, 0.23]),
        "tr": dict(x=[0.80, 0.99], y=[0.77, 0.97]),
        "bl": dict(x=[0.01, 0.20], y=[0.03, 0.23]),
        "tl": dict(x=[0.01, 0.20], y=[0.77, 0.97]),
    }
    dom = corners.get(corner, corners["br"])

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=round(pop * 100.0, 1),
        number=dict(suffix="% POP", valueformat=".1f"),
        gauge=dict(
            axis=dict(range=[0, 100]),
            bar=dict(thickness=0.7),
            threshold=dict(
                line=dict(width=2),
                value=50  # visual midline
            )
        ),
        domain=dom,
        name="TP-first"
    ))

    t_med = m.get("t_hit_tp_median")
    if t_med is not None:
        # small caption under the gauge
        cx = (dom["x"][0] + dom["x"][1]) / 2
        fig.add_annotation(
            x=cx, y=dom["y"][0] - 0.02, xref="paper", yref="paper",
            text=f"Median bars → TP: {int(t_med)}",
            showarrow=False, font=dict(size=10)
        )

def plot_point_and_figure(df: pd.DataFrame, output_dir: str, csv_file_name: str, show=True, box_size=None, reversal=3, wyckoff_overlay=False, pnf_scale=None, pnf_scale_value=None) -> dict:
    """
    P&F with symbol-aware auto box sizing, correct column indexing, breakouts and counts.
    Saves HTML and returns a small JSON sidecar for logging.
    """
    logger.info("Generating Point & Figure chart...")

    # --- Auto box size (prefer percent or ATR fraction) ---
    # --- Auto box size (prefer percent or ATR fraction) ---
    if box_size is None:
        cfg_mode = cfg_val = None
        try:
            cfg_mode = getattr(config_manager, "pnf_scale", None)
            cfg_val  = getattr(config_manager, "pnf_scale_value", None)
        except NameError:
            cfg_mode = cfg_val = None

        if cfg_mode is not None or cfg_val is not None:
            mode  = cfg_mode  or "percent"
            value = cfg_val   or 0.005
            box_size = _compute_box(df, mode=mode, value=value)
        elif pnf_scale is not None and pnf_scale_value is not None:
            box_size = _compute_box(df, mode=pnf_scale, value=pnf_scale_value)
        else:
            # filename heuristic...
            name = str(csv_file_name).lower()
            pct_map = {"1d":0.01, "4h":0.005, "1h":0.003, "30m":0.002, "15m":0.0015, "5m":0.001, "1m":0.0005}
            pct = next((v for k,v in pct_map.items() if k in name), 0.005)
            box_size = _compute_box(df, mode="percent", value=pct)

    # Sanity guard (prevents ERJ/PANW scale mix-ups)
    last_price = float(df["close"].iloc[-1])
    if not (8 <= last_price/box_size <= 20000):
        logger.warning(f"Box size {box_size} looks off for price {last_price}. Consider --box-size or percent/ATR mode.")

    params = PnFParams(box=float(box_size), reversal=int(reversal), method="high_low")
    columns, row_column_index = _build_pnf_columns(df, params)

    # Breakouts & count
    brks = _find_breakouts(columns, params.box, params.reversal)

    direction = "up" if columns[-1]["type"] == "X" else "down"
    cnt = _last_congestion_count(columns, params.box, params.reversal, direction=direction)
    cnt_up = _last_congestion_count(columns, params.box, params.reversal, direction="up")
    cnt_dn = _last_congestion_count(columns, params.box, params.reversal, direction="down")

    sidecar = {
        "box": params.box, "reversal": params.reversal, "last_price": last_price,
        "columns": columns, "breakouts": brks,
        "count_up": cnt_up, "count_down": cnt_dn
    }


    # --- Plot ---
    fig = go.Figure()
    for i, c in enumerate(columns):
        # expand y levels for this column
        if c["type"] == "X":
            y_vals = list(np.arange(c["low"], c["high"]+params.box*0.5, params.box))
            fig.add_trace(go.Scatter(x=[i+1]*len(y_vals), y=y_vals, mode='markers',
                                     marker=dict(symbol='x', color='green', size=8),
                                     name='Up Column' if i==0 else '', showlegend=(i==0)))
        else:
            y_vals = list(np.arange(c["high"], c["low"]-params.box*0.5, -params.box))
            fig.add_trace(go.Scatter(x=[i+1]*len(y_vals), y=y_vals, mode='markers',
                                     marker=dict(symbol='circle-open', color='red', size=8, line=dict(width=2)),
                                     name='Down Column' if i==0 else '', showlegend=(i==0)))

    # Wyckoff overlay (now correct, because row_column_index is real)
    if wyckoff_overlay and 'wyckoff_phase' in df.columns:
        df_cols = df.copy()
        df_cols['pnf_column'] = row_column_index
        add_wyckoff_phase_overlay_pnf(fig, df_cols)

    # Draw breakout line & count objective (if available)
    if cnt is not None:
        fig.add_vrect(
            x0=cnt["start"] + 0.5, x1=cnt["end"] + 0.5,
            fillcolor="rgba(46,204,113,0.06)", line_color="rgba(46,204,113,1.0)",
            annotation_text=f"Count: {cnt['columns']} cols", annotation_position="top left"
        )
        fig.add_hline(y=cnt["breakout"],  line_dash="dot",  line_color="dodgerblue",
                    annotation_text=f"Breakout {cnt['breakout']:.2f}", annotation_position="top left")
        fig.add_hline(y=cnt["objective"], line_dash="dash", line_color="seagreen",
                    annotation_text=f"Objective {cnt['objective']:.2f}", annotation_position="bottom left")

    if brks:
        last_up_brk = next((b for b in reversed(brks) if b["type"].startswith("double_top")), None)
        if last_up_brk:
            i = last_up_brk["i"]
            fig.add_vline(x=i+1, line_color="dodgerblue", line_dash="dot",
                        annotation_text=f"{last_up_brk['type']} @ {last_up_brk['price']:.2f}",
                        annotation_position="top right")

    fig.update_layout(
        title=f"Point & Figure Chart — Box: {params.box:.4f}, Reversal: {params.reversal} — {csv_file_name}",
        xaxis_title="P&F Column",
        yaxis_title="Price",
        yaxis=dict(tickformat=".2f", gridwidth=1, gridcolor='LightGrey'),
        xaxis=dict(gridwidth=1, gridcolor='LightGrey', dtick=1),
        showlegend=True
    )

    pnf_path = os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_point_and_figure_plot.html")
    # ... after you finish fig.update_layout(...)
    # Look for latest MC summary saved in the same output dir
    csv_basename = os.path.basename(csv_file_name)
    mc_data = _load_latest_mc_for(csv_basename, directory=output_dir)
    add_pop_gauge(fig, mc_data, corner="br")  # move to "tr"/"tl"/"bl" if it overlaps

    fig.write_html(pnf_path)
    logger.info(f"Point & Figure plot saved as {pnf_path}")
    if show:
        fig.show()

    # Sidecar JSON (handy for logging)
    sidecar = {
        "box": params.box, "reversal": params.reversal, "last_price": last_price,
        "columns": columns, "breakouts": brks, "count": cnt
    }
    with open(os.path.join(output_dir, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_pnf_meta.json"), "w") as fh:
        import json; json.dump(sidecar, fh, indent=2, default=float)

    return {"path": pnf_path, **sidecar}

def plot_wyckoff_candlestick_chart(df: pd.DataFrame, output_dir: str, csv_file_name: str) -> None:
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
        "A": "rgba(255, 165, 0, 0.4)", "B": "rgba(0, 0, 255, 0.4)",
        "C": "rgba(128, 0, 128, 0.4)", "D": "rgba(0, 128, 0, 0.4)",
        "E": "rgba(139, 69, 19, 0.4)", "UNKNOWN": "rgba(128, 128, 128, 0.4)"
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
                           bgcolor="rgba(255,255,141,1.0)",
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

def plot_features(csv_file: str, features: list[str] = None, nrows: int = 4000, box_size: float = None, reversal: int = 3, pnf_scale: str = None, pnf_scale_value: float = None) -> None:
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
    plot_wyckoff_candlestick_chart(df, output_dir, csv_file_name)

    # NEW: Plot Volume Profile
    plot_volume_profile(df.copy(), output_dir, csv_file_name)

    # NEW: Plot Point & Figure Chart
    plot_point_and_figure(
        df.copy(),
        output_dir=output_dir,
        csv_file_name=csv_file_name,
        box_size=box_size,
        reversal=reversal,
        wyckoff_overlay=True,
        pnf_scale=pnf_scale,
        pnf_scale_value=pnf_scale_value,
    )

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
        go.Bar(x=df['timestamp'], y=df['volume'], name='Volume', marker_color='rgba(100,150,255,1.0)'),
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
    parser.add_argument("--pnf-scale", choices=["fixed", "percent", "atr"], default=None)
    parser.add_argument("--pnf-scale-value", type=float, default=None)
    args = parser.parse_args()
    plot_features(
        args.csv,
        args.features,
        args.nrows,
        args.box_size,
        args.reversal,
        pnf_scale=args.pnf_scale,
        pnf_scale_value=args.pnf_scale_value,
    )

if __name__ == "__main__":
    main()