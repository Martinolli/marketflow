"""Plotly chart builders for Point & Figure sidecar data."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go


def _to_float(value: Any) -> float | None:
    """Convert numeric-like values to float, returning None on failure."""
    if value is None or value == "" or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    """Convert numeric-like values to int, returning None on failure."""
    number = _to_float(value)
    if number is None:
        return None
    try:
        return int(number)
    except (TypeError, ValueError, OverflowError):
        return None


def _raw(sidecar: dict[str, Any]) -> dict[str, Any]:
    """Return raw sidecar data if present."""
    raw = sidecar.get("raw") if isinstance(sidecar, dict) else None
    return raw if isinstance(raw, dict) else {}


def _containers(sidecar: dict[str, Any]) -> list[dict[str, Any]]:
    """Return likely sidecar containers to inspect."""
    containers: list[dict[str, Any]] = []
    for item in [sidecar, _raw(sidecar)]:
        if isinstance(item, dict):
            containers.append(item)
            for key in ("pnf", "count", "data", "meta", "summary"):
                child = item.get(key)
                if isinstance(child, dict):
                    containers.append(child)
    return containers


def _first_value(sidecar: dict[str, Any], keys: tuple[str, ...]) -> Any:
    """Return the first non-empty value from normalized fields or raw containers."""
    for container in _containers(sidecar):
        for key in keys:
            value = container.get(key)
            if value is not None and value != "":
                return value
    return None


def _first_float(sidecar: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    """Return the first numeric value from known sidecar fields."""
    for container in _containers(sidecar):
        for key in keys:
            number = _to_float(container.get(key))
            if number is not None:
                return number
    return None


def _direction_marker(value: Any) -> tuple[str, str]:
    """Return text marker and normalized direction from a sidecar direction value."""
    direction = str(value or "").strip().lower()
    if direction in {"o", "down", "falling", "bear", "bearish", "sell"}:
        return "O", "down"
    return "X", "up"


def _numeric_items(values: Any) -> list[float]:
    """Extract numeric price levels from a list-like sidecar value."""
    if not isinstance(values, list):
        return []
    numbers: list[float] = []
    for item in values:
        if isinstance(item, dict):
            number = _to_float(
                item.get("price")
                or item.get("level")
                or item.get("value")
                or item.get("y")
                or item.get("close")
            )
        else:
            number = _to_float(item)
        if number is not None:
            numbers.append(number)
    return numbers


def _levels_from_range(column: dict[str, Any], sidecar: dict[str, Any]) -> list[float]:
    """Build column price levels from high/low/count/box-size fields."""
    high = _to_float(column.get("high") or column.get("top") or column.get("max"))
    low = _to_float(column.get("low") or column.get("bottom") or column.get("min"))
    if high is None or low is None:
        return []
    if low > high:
        low, high = high, low

    box_size = _to_float(column.get("box_size") or column.get("box")) or _first_float(sidecar, ("box_size", "box"))
    if box_size is not None and box_size > 0:
        levels: list[float] = []
        current = low
        while current <= high + (box_size / 2):
            levels.append(round(current, 8))
            current += box_size
        return levels or [low, high]

    count = _to_int(column.get("boxes") or column.get("box_count") or column.get("count"))
    if count and count > 1:
        step = (high - low) / (count - 1)
        return [round(low + step * index, 8) for index in range(count)]
    return [low] if low == high else [low, high]


def _levels_from_column(column: dict[str, Any], sidecar: dict[str, Any]) -> list[float]:
    """Extract price levels for one P&F column."""
    for key in ("prices", "levels", "y", "values"):
        levels = _numeric_items(column.get(key))
        if levels:
            return levels

    boxes_value = column.get("boxes")
    if isinstance(boxes_value, list):
        levels = _numeric_items(boxes_value)
        if levels:
            return levels

    return _levels_from_range(column, sidecar)


def _find_column_list(sidecar: dict[str, Any]) -> list[dict[str, Any]]:
    """Find a list of P&F columns in common sidecar shapes."""
    for container in _containers(sidecar):
        for key in ("columns", "pnf_columns"):
            value = container.get(key)
            if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                return value

        chart = container.get("chart")
        if isinstance(chart, dict):
            for key in ("columns", "pnf_columns"):
                value = chart.get(key)
                if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                    return value
    return []


def _points_from_columns(sidecar: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert P&F column sidecar data into renderable point records."""
    points: list[dict[str, Any]] = []
    for column_index, column in enumerate(_find_column_list(sidecar), start=1):
        marker, direction = _direction_marker(
            column.get("type") or column.get("direction") or column.get("marker")
        )
        for price in _levels_from_column(column, sidecar):
            points.append(
                {
                    "x": column_index,
                    "price": price,
                    "marker": marker,
                    "direction": direction,
                }
            )
    return points


def _points_from_flat_grid(sidecar: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract P&F point records from flat grid/box/point lists."""
    points: list[dict[str, Any]] = []
    for container in _containers(sidecar):
        for key in ("grid", "boxes", "points", "chart"):
            value = container.get(key)
            if not isinstance(value, list):
                continue
            for item in value:
                if not isinstance(item, dict):
                    continue
                price = _to_float(
                    item.get("price")
                    or item.get("level")
                    or item.get("value")
                    or item.get("y")
                )
                if price is None:
                    continue
                x = _to_int(item.get("x") or item.get("column") or item.get("column_index"))
                if x is None:
                    x = len(points) + 1
                marker, direction = _direction_marker(
                    item.get("type") or item.get("direction") or item.get("marker")
                )
                points.append({"x": x, "price": price, "marker": marker, "direction": direction})
    return points


def _build_grid_chart(sidecar: dict[str, Any], points: list[dict[str, Any]]) -> go.Figure:
    """Build a text-marker X/O P&F chart."""
    x_points = [point for point in points if point["marker"] == "X"]
    o_points = [point for point in points if point["marker"] == "O"]
    title = _pnf_title(sidecar, "P&F Sidecar Chart")

    fig = go.Figure()
    for marker_points, name, color in [
        (x_points, "X columns", "#1f77b4"),
        (o_points, "O columns", "#d62728"),
    ]:
        if not marker_points:
            continue
        fig.add_trace(
            go.Scatter(
                x=[point["x"] for point in marker_points],
                y=[point["price"] for point in marker_points],
                mode="text",
                text=[point["marker"] for point in marker_points],
                textfont={"size": 18, "color": color},
                name=name,
                customdata=[point["direction"] for point in marker_points],
                hovertemplate="Column %{x}<br>Direction: %{customdata}<br>Price: %{y}<extra></extra>",
            )
        )

    fig.update_layout(
        title=title,
        height=640,
        margin={"l": 20, "r": 20, "t": 70, "b": 40},
        xaxis={"title": "P&F column", "dtick": 1, "showgrid": True},
        yaxis={"title": "Price", "showgrid": True},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    return fig


def _pnf_title(sidecar: dict[str, Any], prefix: str) -> str:
    """Build a compact P&F chart title."""
    parts = [prefix]
    metadata = {
        "TF": _first_value(sidecar, ("timeframe", "tf", "interval")),
        "Direction": _first_value(sidecar, ("direction", "count_direction", "trend")),
        "Box": _first_float(sidecar, ("box_size", "box")),
        "Rev": _first_value(sidecar, ("reversal", "rev")),
        "Obj R": _first_float(sidecar, ("objective_r_multiple",)),
    }
    details = [f"{label}: {value}" for label, value in metadata.items() if value is not None and value != ""]
    if details:
        parts.append(" | ".join(details))
    filename = sidecar.get("filename") if isinstance(sidecar, dict) else None
    if filename:
        parts.append(str(filename))
    return " - ".join(parts)


def _build_level_chart(sidecar: dict[str, Any]) -> go.Figure:
    """Build fallback horizontal-level chart from P&F metadata."""
    levels = [
        ("Last price", _first_float(sidecar, ("last_price", "spot", "current_price", "close")), "#1f77b4"),
        (
            "Breakout",
            _first_float(sidecar, ("breakout_level", "breakout", "break_level", "breakout_price")),
            "#ff7f0e",
        ),
        (
            "Objective",
            _first_float(sidecar, ("objective", "objective_price", "target", "target_price")),
            "#2ca02c",
        ),
    ]
    usable_levels = [(label, value, color) for label, value, color in levels if value is not None]
    if not usable_levels:
        raise ValueError("P&F sidecar does not contain enough data to render a chart.")

    fig = go.Figure()
    for label, value, color in usable_levels:
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[value, value],
                mode="lines+markers",
                name=label,
                line={"color": color, "width": 2},
                hovertemplate=f"{label}<br>Price: %{{y}}<extra></extra>",
            )
        )
        fig.add_annotation(
            x=1,
            y=value,
            text=f"{label}: {value:.4f}",
            showarrow=False,
            xanchor="left",
            bgcolor="rgba(255,255,255,0.75)",
        )

    fig.update_layout(
        title=_pnf_title(sidecar, "P&F Objective Levels"),
        height=500,
        margin={"l": 20, "r": 120, "t": 80, "b": 30},
        xaxis={"visible": False, "range": [0, 1.25]},
        yaxis={"title": "Price", "showgrid": True},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    return fig


def build_pnf_chart_from_sidecar(sidecar: dict[str, Any]) -> go.Figure:
    """
    Build a simple P&F chart from a normalized or raw P&F sidecar.

    If box/column data is available, render X/O style columns.
    If only metadata/objective data is available, render a simple objective/level chart.
    """
    if not isinstance(sidecar, dict):
        raise ValueError("P&F sidecar does not contain enough data to render a chart.")

    points = _points_from_columns(sidecar)
    if not points:
        points = _points_from_flat_grid(sidecar)
    if points:
        return _build_grid_chart(sidecar, points)

    return _build_level_chart(sidecar)
