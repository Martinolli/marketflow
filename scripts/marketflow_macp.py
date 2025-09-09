"""Calculate the expected return, beta, and volatility of a portfolio using CAPM and plot the Security Market Line (SML).
Usage:
    python scripts/marketflow_macp.py
Example:   python scripts/marketflow_macp.py
"""

import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from polygon import RESTClient
import datetime

# Step 1: Define your Polygon.io API key
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("MACP_Calculator")
config_manager = create_app_config(logger=logger)
api_key = config_manager.get_api_key('polygon')
if not api_key:
    raise ValueError("Please set the POLYGON_API_KEY environment variable.")

client = RESTClient(api_key)

# Step 2: Define your portfolio and total investment
portfolio = {
    'ERJ': 0.55,
    'PANW': 0.45,
}
total_investment = 1000 # Your total investment amount

# Step 3: Define market parameters
risk_free_rate = 0.042  # 4.2%
market_return = 0.095   # 9.5%

# Step 4: Fetch beta values from Polygon.io (your existing functions are good)

def fetch_close_prices(ticker, from_date, to_date):
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/"
        f"{from_date}/{to_date}?adjusted=true&sort=asc&limit=5000&apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        closes = [item['c'] for item in data.get('results', [])]
        dates = [datetime.datetime.fromtimestamp(item['t']/1000).date() for item in data.get('results', [])]
        return pd.Series(closes, index=dates)
    except Exception as e:
        logger.error(f"Error fetching prices for {ticker}: {e}")
        return pd.Series(dtype=float)

def calculate_beta(stock_returns, market_returns):
    aligned = pd.concat([stock_returns, market_returns], axis=1, join='inner').dropna()
    if aligned.shape[0] < 2:
        return None
    cov = np.cov(aligned.iloc[:,0], aligned.iloc[:,1])[0][1]
    var = np.var(aligned.iloc[:,1])
    if var == 0:
        return None
    return cov / var

def get_beta(ticker, market_ticker="SPY", lookback_days=252):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=lookback_days*1.5)  # extra days for holidays
    stock_prices = fetch_close_prices(ticker, start, end)
    market_prices = fetch_close_prices(market_ticker, start, end)
    if stock_prices.empty or market_prices.empty:
        logger.warning(f"Missing price data for {ticker} or {market_ticker}")
        return None
    stock_returns = stock_prices.pct_change().dropna()
    market_returns = market_prices.pct_change().dropna()
    beta = calculate_beta(stock_returns, market_returns)
    if beta is None:
        logger.warning(f"Could not calculate beta for {ticker}")
    return beta

# New function to get historical volatility (standard deviation of daily returns)
def get_historical_volatility(ticker, lookback_days=252):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=lookback_days*1.5)
    prices = fetch_close_prices(ticker, start_date, end_date)
    if prices.empty or len(prices) < 2:
        logger.warning(f"Not enough price data to calculate volatility for {ticker}")
        return None
    daily_returns = prices.pct_change().dropna()
    # Annualize by multiplying by sqrt(252) for daily data
    return daily_returns.std() * np.sqrt(252) if not daily_returns.empty else None

# Step 5: Build DataFrame with beta, weights, investment, and expected values
data = []
for ticker, weight in portfolio.items():
    beta = get_beta(ticker)
    volatility = get_historical_volatility(ticker) # Fetch volatility
    
    if beta is not None:
        expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
        invested_value = total_investment * weight
        expected_gain_loss = invested_value * expected_return
        data.append({
            'Ticker': ticker,
            'Beta': beta,
            'Volatility': volatility, # Add volatility
            'Weight': weight,
            'Expected Return': expected_return,
            'Invested Value': invested_value,
            'Expected Gain/Loss ($)': expected_gain_loss
        })
    else:
        logger.error(f"Skipping {ticker} due to missing beta.")
    

df = pd.DataFrame(data)
logger.info(f"DataFrame built:\n{df}")

if df.empty or 'Expected Return' not in df.columns or 'Weight' not in df.columns or 'Beta' not in df.columns:
    raise ValueError("DataFrame is missing required data. Check if betas were fetched correctly. See logs for details.")

# Step 6: Compute portfolio expected return, beta, and volatility
portfolio_return = np.dot(df['Expected Return'], df['Weight'])
portfolio_beta = np.dot(df['Beta'], df['Weight'])

# For portfolio volatility, we need the covariance matrix.
# This is a more advanced calculation and might be beyond a simple sum of individual volatilities.
# For simplicity, we can use a weighted average of individual volatilities as a first approximation,
# but note that this ignores correlation benefits.
portfolio_volatility = np.dot(df['Volatility'].fillna(0), df['Weight']) # Handle potential None for volatility

# Calculate total expected gain/loss for the portfolio
total_expected_gain_loss = total_investment * portfolio_return

print("\n--- Portfolio Analysis ---")
print(f"Total Investment: ${total_investment:,.2f}")
print(f"Portfolio Expected Return: {portfolio_return:.2%}")
print(f"Portfolio Beta: {portfolio_beta:.2f}")
print(f"Approximate Portfolio Volatility: {portfolio_volatility:.2%}")
print(f"Total Expected Gain/Loss: ${total_expected_gain_loss:,.2f}")
print("\n--- Individual Stock Details ---")
print(df[['Ticker', 'Weight', 'Invested Value', 'Expected Return', 'Expected Gain/Loss ($)', 'Beta', 'Volatility']].to_string(index=False))


# Step 7: Plot Security Market Line
beta_range = np.linspace(0, 2.5, 100)
sml_returns = risk_free_rate + beta_range * (market_return - risk_free_rate)

fig = go.Figure()

# Security Market Line
fig.add_trace(go.Scatter(x=beta_range, y=sml_returns,
                         mode='lines', name='Security Market Line',
                         line=dict(color='blue', width=2)))

# Individual Stocks
# Add hover text for more details
fig.add_trace(go.Scatter(x=df['Beta'], y=df['Expected Return'],
                         mode='markers+text', name='Stocks',
                         text=df['Ticker'], textposition='top center',
                         hoverinfo='text',
                         hovertext=[
                             f"Ticker: {row['Ticker']}<br>"
                             f"Weight: {row['Weight']:.2%}<br>"
                             f"Invested: ${row['Invested Value']:,.2f}<br>"
                             f"Expected Return: {row['Expected Return']:.2%}<br>"
                             f"Expected Gain/Loss: ${row['Expected Gain/Loss ($)']:,.2f}<br>"
                             f"Beta: {row['Beta']:.2f}<br>"
                             f"Volatility: {row['Volatility']:.2%}"
                             for index, row in df.iterrows()
                         ],
                         marker=dict(size=10, color='green')))

# Portfolio Point
fig.add_trace(go.Scatter(x=[portfolio_beta], y=[portfolio_return],
                         mode='markers+text', name='Portfolio',
                         text=['Portfolio'], textposition='bottom center',
                         hoverinfo='text',
                         hovertext=f"Portfolio<br>Expected Return: {portfolio_return:.2%}<br>Beta: {portfolio_beta:.2f}<br>Total Investment: ${total_investment:,.2f}<br>Total Expected Gain/Loss: ${total_expected_gain_loss:,.2f}",
                         marker=dict(size=12, color='red')))

fig.update_layout(title='CAPM: Security Market Line with Portfolio Analysis',
                  xaxis_title='Beta (Systematic Risk)',
                  yaxis_title='Expected Return',
                  template='plotly_white')

fig.show()