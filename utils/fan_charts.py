"""
Utility functions for creating fan charts from simulated paths.
"""
import numpy as np
import plotly.graph_objects as go

def fan_chart(paths: np.ndarray, title: str) -> go.Figure:
        """
        Compute and plot a fan chart of the simulated paths.
        Parameters
        ----------
        paths: np.ndarray
            The simulated price paths.
        title: str
            The title of the plot.
        """
        q = np.percentile(paths, [5,25,50,75,95], axis=0)
        x = np.arange(paths.shape[1])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=q[2], mode="lines", name="Median", line=dict(width=2)))
        fig.add_trace(go.Scatter(x=x, y=q[3], mode="lines", name="75%", line=dict(width=1)))
        fig.add_trace(go.Scatter(x=x, y=q[1], mode="lines", name="25%", line=dict(width=1), fill='tonexty', fillcolor='rgba(0,150,255,0.15)'))
        fig.add_trace(go.Scatter(x=x, y=q[4], mode="lines", name="95%", line=dict(width=1)))
        fig.add_trace(go.Scatter(x=x, y=q[0], mode="lines", name="5%", line=dict(width=1), fill='tonexty', fillcolor='rgba(0,150,255,0.08)'))
        fig.update_layout(title=title, xaxis_title="Bars ahead", yaxis_title="Price")
        return fig