"""Basic Plotly chart builders for annotated MarketFlow CSV data."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


REQUIRED_OHLC_COLUMNS = ("open", "high", "low", "close")


def _chart_x_values(df: pd.DataFrame) -> pd.Series | pd.Index:
    """Return datetime x-values from timestamp column or DataFrame index."""
    if "timestamp" in df.columns:
        return pd.to_datetime(df["timestamp"], errors="coerce")
    return pd.to_datetime(df.index, errors="coerce")


def _latest_numeric_value(df: pd.DataFrame, column: str) -> float | None:
    """Return the latest numeric value from a column, ignoring missing values."""
    if column not in df.columns:
        return None

    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if values.empty:
        return None
    return float(values.iloc[-1])


def _event_points(df: pd.DataFrame, column: str, x_values: Any) -> pd.DataFrame:
    """Return rows with non-empty event labels for marker rendering."""
    if column not in df.columns:
        return pd.DataFrame()

    event_series = df[column].fillna("").astype(str).str.strip()
    event_series = event_series[event_series.ne("") & event_series.ne("nan")]
    if event_series.empty:
        return pd.DataFrame()

    event_df = df.loc[event_series.index, ["high", "low"]].copy()
    event_df["event_label"] = event_series
    event_df["x"] = pd.Series(x_values, index=df.index).loc[event_series.index]
    return event_df


def build_basic_wyckoff_candlestick_chart(
    df: pd.DataFrame,
    title: str | None = None,
) -> go.Figure:
    """
    Build a basic Plotly candlestick chart from an annotated MarketFlow CSV.

    Expected columns:
    - timestamp, or a datetime-like index
    - open
    - high
    - low
    - close
    - volume, optional

    Optional annotation columns:
    - wyckoff_phase
    - wyckoff_event
    - wyckoff_confirmed_event
    - tr_low
    - tr_high
    """
    if df is None or df.empty:
        raise ValueError("CSV data is empty.")

    missing_columns = [column for column in REQUIRED_OHLC_COLUMNS if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required OHLC column(s): {missing}.")

    chart_df = df.copy()
    x_values = _chart_x_values(chart_df)

    for column in [*REQUIRED_OHLC_COLUMNS, "volume", "tr_low", "tr_high"]:
        if column in chart_df.columns:
            chart_df[column] = pd.to_numeric(chart_df[column], errors="coerce")

    chart_df = chart_df.dropna(subset=list(REQUIRED_OHLC_COLUMNS))
    if chart_df.empty:
        raise ValueError("CSV data has no valid OHLC rows.")

    x_values = pd.Series(x_values, index=df.index).loc[chart_df.index]
    has_volume = "volume" in chart_df.columns and chart_df["volume"].notna().any()
    row_count = 2 if has_volume else 1
    row_heights = [0.72, 0.28] if has_volume else [1.0]

    fig = make_subplots(
        rows=row_count,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=row_heights,
    )

    fig.add_trace(
        go.Candlestick(
            x=x_values,
            open=chart_df["open"],
            high=chart_df["high"],
            low=chart_df["low"],
            close=chart_df["close"],
            name="OHLC",
        ),
        row=1,
        col=1,
    )

    if has_volume:
        fig.add_trace(
            go.Bar(
                x=x_values,
                y=chart_df["volume"],
                name="Volume",
                marker_color="rgba(86, 118, 160, 0.45)",
            ),
            row=2,
            col=1,
        )

    tr_low = _latest_numeric_value(chart_df, "tr_low")
    if tr_low is not None:
        fig.add_hline(
            y=tr_low,
            line_dash="dash",
            line_color="#2ca02c",
            annotation_text="TR low",
            annotation_position="bottom right",
            row=1,
            col=1,
        )

    tr_high = _latest_numeric_value(chart_df, "tr_high")
    if tr_high is not None:
        fig.add_hline(
            y=tr_high,
            line_dash="dash",
            line_color="#d62728",
            annotation_text="TR high",
            annotation_position="top right",
            row=1,
            col=1,
        )

    for column, marker_name, marker_color, marker_symbol in [
        ("wyckoff_event", "Wyckoff event", "#1f77b4", "circle"),
        ("wyckoff_confirmed_event", "Confirmed event", "#9467bd", "diamond"),
    ]:
        events = _event_points(chart_df, column, x_values)
        if events.empty:
            continue

        fig.add_trace(
            go.Scatter(
                x=events["x"],
                y=events["high"],
                mode="markers",
                name=marker_name,
                marker={"size": 8, "color": marker_color, "symbol": marker_symbol},
                text=events["event_label"],
                hovertemplate="%{text}<br>%{x}<br>Price: %{y}<extra></extra>",
            ),
            row=1,
            col=1,
        )

    fig.update_layout(
        title=title or "MarketFlow Annotated Candlestick",
        height=720,
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        xaxis_rangeslider_visible=False,
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    fig.update_yaxes(title_text="Price", row=1, col=1)
    if has_volume:
        fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig

