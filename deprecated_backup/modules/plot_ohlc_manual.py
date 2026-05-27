import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('1d_2025-08-17_10-45-17.csv')

fig = go.Figure(data=go.Ohlc(x=df['timestamp'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']))
fig.show()