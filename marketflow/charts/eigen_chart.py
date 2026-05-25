"""Plotly chart builders for Price-Volume Eigen Analyzer output."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _empty_chart(message: str, title: str | None = None) -> go.Figure:
    """Return a readable empty-state figure."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 14},
    )
    fig.update_layout(
        title=title or "Price-Volume Eigen Chart",
        height=520,
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
    )
    return fig


def _x_values(df: pd.DataFrame) -> pd.Series:
    """Return datetime x-values when available, otherwise row positions."""
    for column in ("timestamp", "datetime", "date"):
        if column not in df.columns:
            continue
        values = pd.to_datetime(df[column], errors="coerce")
        if values.notna().any():
            return values
    return pd.Series(range(len(df)), index=df.index)


def _numeric(df: pd.DataFrame, column: str) -> pd.Series:
    """Return a numeric column with invalid values coerced to NaN."""
    return pd.to_numeric(df[column], errors="coerce")


def _truthy_series(df: pd.DataFrame, column: str) -> pd.Series:
    """Return a boolean series from common CSV boolean encodings."""
    if column not in df.columns:
        return pd.Series(False, index=df.index)
    values = df[column]
    if values.dtype == bool:
        return values.fillna(False)
    normalized = values.fillna(False).astype(str).str.strip().str.lower()
    return normalized.isin({"true", "1", "yes", "y"})


def build_price_volume_eigen_chart(
    dataframe: pd.DataFrame,
    *,
    title: str | None = None,
    max_rows: int | None = 500,
) -> go.Figure:
    """
    Build a Plotly chart for Price-Volume Eigen Analyzer output.

    This chart visualizes feature behavior only.
    It does not create trade signals.
    """
    if dataframe is None or dataframe.empty:
        return _empty_chart("No Price-Volume Eigen rows are available.", title)

    chart_df = dataframe.copy()
    if max_rows is not None:
        try:
            chart_df = chart_df.tail(max(int(max_rows), 1))
        except (TypeError, ValueError):
            chart_df = chart_df.tail(500)

    required = ("pv_eigen_residual", "pv_eigen_coupling")
    missing = [column for column in required if column not in chart_df.columns]
    if missing:
        return _empty_chart(
            f"Missing required Eigen column(s): {', '.join(missing)}.",
            title,
        )

    x_values = _x_values(chart_df)
    residual = _numeric(chart_df, "pv_eigen_residual")
    coupling = _numeric(chart_df, "pv_eigen_coupling")
    if residual.notna().sum() == 0 and coupling.notna().sum() == 0:
        return _empty_chart("Eigen residual and coupling columns contain no numeric values.", title)

    has_close = "close" in chart_df.columns and _numeric(chart_df, "close").notna().any()
    row_count = 3 if has_close else 2
    row_heights = [0.44, 0.30, 0.26] if has_close else [0.52, 0.48]
    residual_row = 2 if has_close else 1
    coupling_row = 3 if has_close else 2

    fig = make_subplots(
        rows=row_count,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=row_heights,
        subplot_titles=(
            ("Price Context", "Eigen Residual", "Eigen Coupling")
            if has_close
            else ("Eigen Residual", "Eigen Coupling")
        ),
    )

    divergence = _truthy_series(chart_df, "pv_effort_result_divergence")
    divergence_points = chart_df.loc[divergence].copy()
    divergence_x = x_values.loc[divergence_points.index] if not divergence_points.empty else pd.Series(dtype=object)

    if has_close:
        close = _numeric(chart_df, "close")
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=close,
                mode="lines",
                name="Close",
                line={"color": "#2f5d8c", "width": 1.8},
                hovertemplate="Close: %{y:.4f}<br>%{x}<extra></extra>",
            ),
            row=1,
            col=1,
        )
        if not divergence_points.empty:
            strength = _numeric(divergence_points, "pv_divergence_strength") if "pv_divergence_strength" in divergence_points.columns else pd.Series(1.0, index=divergence_points.index)
            marker_sizes = (strength.fillna(1.0).clip(lower=0.5, upper=6.0) * 4 + 8).tolist()
            fig.add_trace(
                go.Scatter(
                    x=divergence_x,
                    y=close.loc[divergence_points.index],
                    mode="markers",
                    name="Divergence marker",
                    marker={
                        "size": marker_sizes,
                        "color": "#c43b3b",
                        "symbol": "diamond",
                        "line": {"width": 1, "color": "#ffffff"},
                    },
                    customdata=_hover_customdata(divergence_points),
                    hovertemplate=(
                        "Divergence<br>%{x}<br>Close: %{y:.4f}"
                        "<br>Residual: %{customdata[0]:.4f}"
                        "<br>Coupling: %{customdata[1]:.4f}"
                        "<br>Harmony: %{customdata[2]}<extra></extra>"
                    ),
                ),
                row=1,
                col=1,
            )

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=residual,
            mode="lines",
            name="Residual",
            line={"color": "#8a4f9e", "width": 1.8},
            customdata=_hover_customdata(chart_df),
            hovertemplate=(
                "Residual: %{y:.4f}<br>%{x}"
                "<br>Coupling: %{customdata[1]:.4f}"
                "<br>Harmony: %{customdata[2]}<extra></extra>"
            ),
        ),
        row=residual_row,
        col=1,
    )
    if not divergence_points.empty:
        fig.add_trace(
            go.Scatter(
                x=divergence_x,
                y=residual.loc[divergence_points.index],
                mode="markers",
                name="Residual divergence",
                marker={"size": 8, "color": "#c43b3b", "symbol": "circle"},
                hovertemplate="Divergence residual: %{y:.4f}<br>%{x}<extra></extra>",
            ),
            row=residual_row,
            col=1,
        )
    fig.add_hline(
        y=2.0,
        line_dash="dash",
        line_color="#9b6a6a",
        annotation_text="residual 2.0",
        annotation_position="top right",
        row=residual_row,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=coupling,
            mode="lines",
            name="Coupling",
            line={"color": "#2c8c6f", "width": 1.8},
            customdata=_hover_customdata(chart_df),
            hovertemplate=(
                "Coupling: %{y:.4f}<br>%{x}"
                "<br>Residual: %{customdata[0]:.4f}"
                "<br>Harmony: %{customdata[2]}<extra></extra>"
            ),
        ),
        row=coupling_row,
        col=1,
    )
    fig.add_hline(
        y=0.65,
        line_dash="dash",
        line_color="#5f8f7c",
        annotation_text="coupling 0.65",
        annotation_position="bottom right",
        row=coupling_row,
        col=1,
    )

    fig.update_layout(
        title=title or "Price-Volume Eigen Chart",
        height=760,
        margin={"l": 20, "r": 20, "t": 70, "b": 20},
        hovermode="x unified",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    fig.update_xaxes(title_text="Time / Row", row=coupling_row, col=1)
    if has_close:
        fig.update_yaxes(title_text="Close", row=1, col=1)
    fig.update_yaxes(title_text="Residual", row=residual_row, col=1)
    fig.update_yaxes(title_text="Coupling", row=coupling_row, col=1)
    return fig


def _hover_customdata(df: pd.DataFrame) -> list[list[Any]]:
    """Build hover values for residual, coupling, and harmony."""
    residual = _numeric(df, "pv_eigen_residual") if "pv_eigen_residual" in df.columns else pd.Series([None] * len(df), index=df.index)
    coupling = _numeric(df, "pv_eigen_coupling") if "pv_eigen_coupling" in df.columns else pd.Series([None] * len(df), index=df.index)
    harmony = _numeric(df, "pv_eigen_harmony") if "pv_eigen_harmony" in df.columns else pd.Series([None] * len(df), index=df.index)
    return [[residual.loc[index], coupling.loc[index], harmony.loc[index]] for index in df.index]
