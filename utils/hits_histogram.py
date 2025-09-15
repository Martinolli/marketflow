"""
Utility functions for plotting histograms of time-to-hit for TP-first trades.

"""

import plotly.graph_objects as go

def hits_histogram(metrics: dict, title: str) -> go.Figure:
        """Plot a histogram of time-to-hit for TP-first trades.
        Parameters
        ----------
        metrics: dict
            The trade outcome statistics.
        title: str
            The title of the plot.
        Returns
        -------
        go.Figure
            The histogram figure.
        """

        # We don't store all hit times; approximate with a simple bar display using medians
        tp_med = metrics.get("t_hit_tp_median")
        sl_med = metrics.get("t_hit_sl_median")
        bars = []
        if tp_med is not None:
            bars.append(("TP median bars", tp_med))
        if sl_med is not None:
            bars.append(("SL median bars", sl_med))
        if not bars:
            bars = [("No barrier hit medians", 0)]
        fig = go.Figure(go.Bar(x=[b[0] for b in bars], y=[b[1] for b in bars]))
        fig.update_layout(title=title, yaxis_title="Bars")
        return fig