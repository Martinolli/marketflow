"""
================================================================================
Monte Carlo Trade Outcome Simulator (v2)
================================================================================
Purpose:
This script simulates the probable outcomes of a financial trade by generating
a large number of possible future price paths. It helps traders and analysts
quantify the probability of a trade hitting its take-profit (TP) level before
its stop-loss (SL) level within a specified time horizon.

The simulation can be run in two modes:
1.  Single-Run Mode: Analyzes a specific trade setup (entry, TP, SL) from the
    most recent data point in a given CSV file.
2.  Backtest Mode: Systematically steps back in time through the historical
    data, running simulations at each point to evaluate the model's
    performance and calibration over time.

Key Features:
-   **Multiple Simulation Models**: Supports three distinct path generation models:
    -   Geometric Brownian Motion (GBM): A standard model assuming log-returns
        are normally distributed with constant drift and volatility.
    -   Block Bootstrap: A non-parametric model that resamples blocks of
        historical returns, preserving some of the observed auto-correlation
        and volatility clustering.
    -   GARCH(1,1): A model that captures volatility clustering, where periods
        of high volatility are followed by more high volatility, and vice-versa.
-   **Statistical Outputs**: Generates a JSON summary file with key metrics,
    including Probability of Profit (POP), median time-to-hit for both TP
    and SL, and statistics on the distribution of returns (R-multiples).
-   **Visualizations**: Produces interactive HTML plots using Plotly:
    -   A fan chart showing the distribution of simulated price paths over time.
    -   A histogram of the median time for trades to hit their targets.

--------------------------------------------------------------------------------
VARIABLES & PARAMETERS
--------------------------------------------------------------------------------

Core Class Parameters (MonteCarloTradeSimulator):
- model_type (str): The default simulation model ('gbm', 'bootstrap', 'garch').
- params (dict): A dictionary for any additional model-specific parameters.

Key Method Parameters (simulate_trade_for_csv):
- csv_path (str): Path to the input OHLCV CSV file. Must contain
                  'timestamp', 'open', 'high', 'low', 'close', 'volume'.
- tp (float): The take-profit price level for the trade.
- sl (float): The stop-loss price level for the trade.
- entry (float | None): The entry price of the trade. If None, the last
                        closing price in the dataset is used.
- tf (str | None): The time frame of the data (e.g., '1h', '4h'). If None,
                   it's inferred from the filename.
- horizon_bars (int): The number of future bars (time steps) to simulate.
- model (str): The simulation model to use for this specific run.
- n_paths (int): The total number of price paths to generate.
- block_len (int): The size of the blocks for the 'bootstrap' model.
- seed (int): A random seed for ensuring reproducibility.
- end_idx (int | None): The index of the historical bar to simulate from. If
                        None, simulation starts from the very last bar.

Backtest Parameters (simulate_backtest_trades):
- TP_pips (float): The take-profit distance from the entry price, in price
                   units (not pips/ticks in the traditional sense).
- SL_pips (float): The stop-loss distance from the entry price.
- step (int): The number of bars to step back between each backtest simulation.
- lookback_windows (int): The total number of past decision points to test.

Command-Line Arguments (via argparse):
- csv (str): Positional argument for the CSV file path.
- --tp (float): Take-profit price (required for single-run mode).
- --sl (float): Stop-loss price (required for single-run mode).
- --entry (float): Optional entry price.
- --tf (str): Optional time frame.
- --horizon (int): Simulation horizon in bars. Default: 20.
- --model (str): Model type ('gbm', 'bootstrap', 'garch'). Default: 'garch'.
- --paths (int): Number of simulation paths. Default: 20000.
- --block (int): Block length for bootstrap. Default: 8.
- --seed (int): RNG seed. Default: 42.
- --nrows (int): Number of recent CSV rows to load. Default: 4000.
- --no-plots (bool): Flag to disable saving HTML plots.
- --simulate-backtest (bool): Flag to enable backtesting mode.
- --bt-tp-pips (float): TP offset for backtesting.
- --bt-sl-pips (float): SL offset for backtesting.
- --bt-step (int): Step size for backtesting. Default: 5.
- --bt-windows (int): Number of windows for backtesting. Default: 40.
- --bt-paths (int): Number of paths per backtest run. Default: 5000.


Outputs per run (saved next to the CSV):
- <timestamp>_mc_summary.json    # metrics (POP, time-to-hit, R stats)
- <timestamp>_mc_paths.html      # fan chart of simulated price paths
- <timestamp>_mc_hits.html       # histogram of time-to-hit for TP-first

Examples
--------
python monte_carlo_trade.py PANW_4h_wyckoff_annotated.csv \
  --tp 206.54 --sl 192.7709 --entry 197.21 \
  --tf 4h --horizon 20 --model bootstrap --paths 20000 --block 8

python monte_carlo_trade.py ERJ_1h_wyckoff_annotated.csv \
  --tp 63.5985 --sl 59.3586 --entry 59.97 \
  --tf 1h --horizon 40 --model gbm --paths 30000

--------
Backtest mode

Single run:
        - py monte_carlo_trade_v1.py .\data\AAPL_1h.csv --tp 210.5 --sl 203.0 --horizon 40 --model bootstrap --paths 20000
Backtest, 40 decision points stepping 5 bars, 5k paths each:
        - py monte_carlo_trade_v1.py .\data\AAPL_1h.csv --simulate-backtest --bt-tp-pips 2.0 --bt-sl-pips 1.0 --bt-windows 40 
        --bt-step 5 --bt-paths 5000 --horizon 40 --block 8 --seed 42 --bt-no-json
Volatility ML-GBM model:
        - python scripts/monte_carlo_trade_v2.py ".marketflow/reports/2025-09-15/PANW/PANW_1d.csv" --tp 206.54 --sl 192.78 
        --entry 197.21 --tf 1d --horizon 40 --model ml_gbm --ml-model ".marketflow/reports/2025-09-15/PANW/volatility_predictor.pkl"
--------------------------------------------------------------------------------
"""

from __future__ import annotations
import argparse
import json
import os
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from arch import arch_model
import lightgbm as lgb
import joblib

try:
    from arch import arch_model
    HAVE_ARCH = True
except Exception:
    HAVE_ARCH = False

try:
    import lightgbm as lgb
    HAVE_LGB = True
except Exception:
    HAVE_LGB = False

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from utils.load_ohlcv import load_ohlcv
from utils.infer_tf_from_name import infer_tf_from_name
from utils.calibrate_per_bar import calibrate_per_bar
from utils.create_features import create_features
from utils.barrier_stats import barrier_stats
from utils.fan_charts import fan_chart
from utils.hits_histogram import hits_histogram


class MonteCarloTradeSimulator:
    """A class to simulate trade outcomes using Monte Carlo methods."""

    def __init__(self, model_type: str = "garch", **params):
        """Initialize the simulator with a model type and parameters."""
        self.model_type = model_type
        self.params = params
        self.model = None
        self.returns = None
        self.S0 = None
        self.lgb_model = None  # Placeholder for the ML model
        self.ml_feat_cols = ['atr_14', 'rsi_14', 'volume_change', 'return_MA_10']  # consistent feature set

        self.logger = get_logger("MonteCarloTradeSimulator")
        self.config_manager = create_app_config(logger=self.logger)

    def simulate_ml_gbm_paths(self, S0: float, mu_bar: float,
                            historical_df: pd.DataFrame, # Pass recent data for features
                            steps: int, n: int, rng: np.random.Generator
                            ) -> np.ndarray:
        """Simulate GBM paths using volatility predicted by an ML model."""
        
        # 1. Load your pre-trained model
        if self.lgb_model is None:
            raise ValueError("ML model not initialized. Train it first or load via --ml-model.")

        # 2 Build recent features and select the same columns used for training
        feat_cols = self.ml_feat_cols
        latest_features = create_features(historical_df.tail(120))  # give indicators enough history
        if latest_features.empty or not set(feat_cols).issubset(latest_features.columns):
            raise ValueError("Insufficient latest features for ML prediction.")
        latest_row = latest_features[feat_cols].tail(1).astype(float)

        # 3. Predict volatility
        predicted_sigma_bar = float(self.lgb_model.predict(latest_row)[0])
        predicted_sigma_bar = max(predicted_sigma_bar, 1e-6)  # ensure > 0

        # 4. Simulate paths using predicted volatility
        self.logger.info(f"Using ML-predicted sigma: {predicted_sigma_bar:.6f}")
        return self.simulate_gbm_paths(S0, mu_bar, predicted_sigma_bar, steps, n, rng)
    
    def simulate_gbm_paths(self, 
                           S0: float, mu_bar: float, sigma_bar: float,
                           steps: int, n: int, rng: np.random.Generator
                           ) -> np.ndarray:
        """Simulate GBM paths using exact discretization.
        Parameters
        ----------
        S0: float
            The initial stock price.
        mu_bar: float
            The per-bar drift.
        sigma_bar: float
            The per-bar volatility.
        steps: int
            The number of time steps to simulate.
        n: int
            The number of paths to simulate.
        rng: np.random.Generator
            The random number generator to use.
        Returns
        -------
        np.ndarray
            An array of shape (n, steps+1) containing the simulated price paths.
        """
        # exact discretization using per-bar parameters (dt=1)
        drift = mu_bar - 0.5 * (sigma_bar ** 2)
        Z = rng.standard_normal((n, steps))
        log_increments = drift + sigma_bar * Z
        paths = np.empty((n, steps+1), dtype=float)
        paths[:,0] = S0
        np.cumprod(np.exp(log_increments), axis=1, out=paths[:,1:])
        paths[:,1:] *= S0
        return paths
    
    def simulate_bootstrap_paths(self, S0: float, returns: np.ndarray,
                                 steps: int, n: int, block_len: int,
                                 rng: np.random.Generator
                                 ) -> np.ndarray:

        """Simulate paths using block bootstrap of historical log-returns.
        Parameters
        ----------
        S0: float
            The initial stock price.
        returns: np.ndarray
            The historical log-returns to bootstrap from.
        steps: int
            The number of time steps to simulate.
        n: int
            The number of paths to simulate.
        block_len: int
            The length of each block to sample.
        rng: np.random.Generator
            The random number generator to use.
        Returns
        -------
        np.ndarray
            An array of shape (n, steps+1) containing the simulated price paths.
        """
        if len(returns) < 50:
            raise ValueError("Need >= 50 returns for bootstrap model")
        paths = np.empty((n, steps+1), dtype=float)
        paths[:,0] = S0
        # Precompute blocks start indices
        max_start = max(0, len(returns)-block_len)
        starts = rng.integers(0, max_start+1, size=(n, int(np.ceil(steps/block_len))+2))
        for i in range(n):
            seq = []
            for st in starts[i]:
                seq.extend(returns[st:st+block_len])
                if len(seq) >= steps: break
            seq = np.array(seq[:steps], dtype=float)
            prices = S0 * np.exp(np.cumsum(seq))
            paths[i,1:] = prices
        return paths

    def simulate_garch_paths(self, S0: float, returns: np.ndarray,
                             steps: int, n: int, rng: np.random.Generator
                             ) -> np.ndarray:
        """Simulate price paths using a GARCH(1,1) model.
        Parameters
        ----------
        S0: float
            The initial stock price.
        returns: np.ndarray
            The historical log-returns to fit the GARCH model.
        steps: int
            The number of time steps to simulate.
        n: int
            The number of paths to simulate.
        rng: np.random.Generator
            The random number generator to use.
        Returns
        -------
        np.ndarray
            The simulated price paths.
        """
        am = arch_model(returns * 100, vol='Garch', p=1, q=1, mean='Zero')
        res = am.fit(update_freq=5, disp='off')
        
        # Extract parameters
        omega = float(res.params['omega'])
        alpha = float(res.params['alpha[1]'])
        beta  = float(res.params['beta[1]'])

        # Initial variance and residual from the fitted model
        h0 = float(res.conditional_volatility[-1]) ** 2
        eps0 = float(res.resid[-1])

        paths = np.empty((n, steps + 1), dtype=float)
        paths[:, 0] = S0
        
        # Simulate n paths
        for i in range(n):
            h = h0
            eps = eps0
            rets = np.empty(steps, dtype=float)

            for t in range(steps):
                # GARCH variance update: h_t = omega + alpha*eps_{t-1}^2 + beta*h_{t-1}
                h = omega + alpha * (eps ** 2) + beta * h
                z = rng.standard_normal()
                eps = z * np.sqrt(h)
                rets[t] = eps / 100.0 # zero mean
                eps0 = float(res.resid[-1])  # reset for next path

            prices = S0 * np.exp(np.cumsum(rets))
            paths[i, 1:] = prices
        
        return paths
    
    def simulate_trade_for_csv(self,
        csv_path: str, tp: float, sl: float, entry: float | None = None,
        tf: str | None = None, horizon_bars: int = 20,
        model: str = "garch", n_paths: int = 10000,
        block_len: int = 8, seed: int = 42,
        nrows: int | None = 4000,
        end_idx: int | None = None,
        save_plots: bool = True,
        full_df: pd.DataFrame | None = None,
        save_json: bool = True,
        ml_model: str | None = None,
        mu_shift: float = 0.0,
        ) -> dict:

        """Simulate trade outcomes for a given OHLCV CSV file.
        Parameters
        ----------
        csv_path: str
            Path to the OHLCV CSV file.
        tp: float
            Take-profit level.
        sl: float
            Stop-loss level.
        entry: float | None
            Entry price. If None, use the last close price.
        tf: str | None
            Time frame of the data (e.g., "1d", "4h"). If None, infer from file name.
        horizon_bars: int
            Number of bars to simulate into the future.
        model: str
            Simulation model to use ("gbm", "bootstrap", or "garch").
        n_paths: int
            Number of Monte Carlo paths to simulate.
        block_len: int
            Block length for bootstrap model (ignored for other models).
        seed: int
            Random seed for reproducibility.
        nrows: int | None
            Number of rows to read from the CSV file. If None, read all rows.
        end_idx: int | None
            Index of the last bar to use as "now". If None, use the last bar in the data.
        save_plots: bool
            Whether to save the fan chart and hits histogram plots.
        full_df: pd.DataFrame | None
            Preloaded OHLCV DataFrame. If None, load from CSV.
        save_json: bool
            Whether to save the summary JSON file.
        Returns
        -------
        dict
            A dictionary containing the simulation results and metrics.
        """

        out_dir = os.path.dirname(csv_path) or "."
        
        # Load once (allows caller to pass preloaded DataFrame, e.g., backtest loop)
        if full_df is None:
            full_df = load_ohlcv(csv_path)

        if end_idx is None:
            end_idx = len(full_df) - 1

        if end_idx >= len(full_df):
            raise ValueError(f"end_idx {end_idx} out of range for data with {len(full_df)} rows")
        
        # The data used for calibration and simulation start
        df_history = full_df.iloc[:end_idx+1].copy()
        if nrows is not None and len(df_history) > nrows:
            df_history = df_history.tail(nrows)

        # The actual future data for comparison (not used in simulation)
        df_future = full_df.iloc[end_idx+1:].copy()

        closes = df_history["close"]
        S0_now = float(closes.iloc[-1])  # The price at the 'end_idx'
        S0 = float(entry) if entry is not None else S0_now

        tf = tf or infer_tf_from_name(os.path.basename(csv_path)) or "4h"

        mu_bar, sigma_bar, r = calibrate_per_bar(closes)
        mu_bar += mu_shift
        rng = np.random.default_rng(seed)

        if model == "gbm":
            paths_now = self.simulate_gbm_paths(S0_now, mu_bar, sigma_bar, horizon_bars, n_paths, rng)
        elif model == "bootstrap":
            paths_now = self.simulate_bootstrap_paths(S0_now, r, horizon_bars, n_paths, block_len, rng)
        elif model == "garch":
            paths_now = self.simulate_garch_paths(S0_now, r, horizon_bars, n_paths, rng)
        # NEW OPTION
        elif model == "ml_gbm":
            paths_now = None
            try:
                if self.lgb_model is None:
                    if ml_model is not None and os.path.exists(ml_model):
                        self.lgb_model = joblib.load(ml_model)
                        self.logger.info(f"Loaded ML model from: {ml_model}")
                    else:
                        self.logger.info("Training new ML volatility model from historical data...")
                        # Train a new model
                    feat = create_features(df_history).dropna(subset=['target_vol'])
                    feat_cols = self.ml_feat_cols
                    if not feat.empty and set(feat_cols).issubset(feat.columns):
                        X = feat[feat_cols].astype(float)
                        y = feat['target_vol'].astype(float)
                        if len(X) > 0 and len(y) > 0:
                            self.lgb_model = lgb.LGBMRegressor(
                                objective='regression_l1', n_estimators=200, random_state=seed
                            )
                            self.lgb_model.fit(X, y)
                        else:
                            self.logger.warning("Insufficient ML features/labels; falling back to GBM.")
                    else:
                        self.logger.warning("Not enough data to train ML model; falling back to GBM.")

                if self.lgb_model is not None:
                    paths_now = self.simulate_ml_gbm_paths(S0_now, mu_bar, df_history, horizon_bars, n_paths, rng)

                if paths_now is None:
                    paths_now = self.simulate_gbm_paths(S0_now, mu_bar, sigma_bar, horizon_bars, n_paths, rng)

                if self.lgb_model is not None:
                    # Save the trained model for inspection
                    model_filename = "volatility_predictor.pkl"
                    model_path = os.path.join(out_dir, model_filename)
                    joblib.dump(self.lgb_model, model_path)
                    self.logger.info(f"Saved ML volatility model to: {model_path}")
            except Exception as e:
                self.logger.warning(f"ML GBM failed ({e}); falling back to GBM.")
                paths_now = self.simulate_gbm_paths(S0_now, mu_bar, sigma_bar, horizon_bars, n_paths, rng)
        else:
            raise ValueError(f"Unknown model: {model}")

        m_now   = barrier_stats(paths_now, tp, sl)
        m_entry = None
        if entry is not None and entry != S0_now:
            # Simulate from entry price for reference (not used in main metrics)
            if model == "gbm":
                paths_entry = self.simulate_gbm_paths(float(entry), mu_bar, sigma_bar, horizon_bars, n_paths, rng)
            elif model == "bootstrap":
                paths_entry = self.simulate_bootstrap_paths(float(entry), r, horizon_bars, n_paths, block_len, rng)
            elif model == "garch":
                paths_entry = self.simulate_garch_paths(float(entry), r, horizon_bars, n_paths, rng)
            elif model == "ml_gbm":
                if self.lgb_model is not None:
                    paths_entry = self.simulate_ml_gbm_paths(float(entry), mu_bar, df_history, horizon_bars, n_paths, rng)
                else:
                    paths_entry = self.simulate_gbm_paths(float(entry), mu_bar, sigma_bar, horizon_bars, n_paths, rng)
            else:
                raise ValueError(f"Unknown model: {model}")
            m_entry = barrier_stats(paths_entry, tp, sl)

        # Prepare output
        out = {
            "csv": os.path.basename(csv_path),
            "tf": tf,
            "params": {"tp": tp, "sl": sl, "entry": entry, "horizon_bars": horizon_bars, "model": model, "paths": n_paths, "block_len": block_len, "seed": seed},
            "spot": {"S0_now": S0_now},
            "metrics_from_now": m_now,
            "metrics_from_entry": m_entry,
        }

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Compute actual outcome from future bars
        actual_outcome = {"outcome": "neither", "bars_to_hit": None}
        for i, row in df_future.iterrows():
            if row['high'] >= tp:
                actual_outcome['outcome'] = 'tp_first'
                actual_outcome['bars_to_hit'] = i - end_idx
                break
            if row['low'] <= sl:
                actual_outcome['outcome'] = 'sl_first'
                actual_outcome['bars_to_hit'] = i - end_idx
                break
        out["actual_outcome"] = actual_outcome
        out["calibration"] = {"mu_bar": float(mu_bar), "sigma_bar": float(sigma_bar), "model_used": model}

        # Save JSON (optional in backtests)
        if save_json:
            json_path = os.path.join(out_dir, f"{ts}_mc_summary.json")
            with open(json_path, "w") as fh:
                json.dump(out, fh, indent=2)
            self.logger.info(f"Monte Carlo summary saved: {json_path}")

        if save_plots:
            fig_fan = fan_chart(paths_now, title=f"MC Fan Chart — {os.path.basename(csv_path)} (from now)")
            fan_path = os.path.join(out_dir, f"{ts}_mc_paths.html")
            fig_fan.write_html(fan_path)
            self.logger.info(f"Fan chart saved: {fan_path}")

            fig_hits = hits_histogram(m_now, title="Median bars to TP/SL")
            hits_path = os.path.join(out_dir, f"{ts}_mc_hits.html")
            fig_hits.write_html(hits_path)
            self.logger.info(f"Hits histogram saved: {hits_path}")

        return out
    
    def simulate_backtest_trades(self, csv_path: str,
                             TP_pips: float, SL_pips: float,
                             tf: str | None = None, Horizon: int = 20,
                             step: int = 5, lookback_windows: int = 40,
                             model: str = "bootstrap", paths: int = 5000,
                             block_len: int = 8, seed: int = 42,
                             nrows: int | None = 4000,
                             save_json: bool = False,
                             verbose: bool = True) -> dict:
        """
        Slide back in time and run simulate_trade_for_csv at multiple decision points.
        TP_pips/SL_pips are price offsets from the entry close at each decision point.
        """
        df = load_ohlcv(csv_path, nrows=nrows)
        n = len(df)
        if n < max(50, Horizon + 5):
            raise ValueError("Not enough rows for backtest.")

        start_bar = n - Horizon - 1
        indices = list(range(start_bar, start_bar - step * lookback_windows, -step))
        # Ensure enough bars exist for calibration (>=20 diffs)
        indices = [i for i in indices if i >= 20]
        if not indices:
            raise ValueError("No valid decision points after filtering.")

        results: list[dict] = []

        for i in indices:
            entry_price = float(df['close'].iloc[i])
            tp_price = entry_price + TP_pips
            sl_price = entry_price - SL_pips

            if verbose:
                self.logger.info(f"Backtest @ idx {i}: entry {entry_price:.4f}, tp {tp_price:.4f}, sl {sl_price:.4f}")

            try:
                res = self.simulate_trade_for_csv(
                    csv_path=csv_path,
                    tp=tp_price, sl=sl_price, entry=entry_price,
                    tf=tf, horizon_bars=Horizon,
                    model=model, n_paths=paths, block_len=block_len,
                    seed=seed, nrows=nrows, end_idx=i,
                    save_plots=False, full_df=df, save_json=save_json,
                )
                results.append(res)
            except Exception as e:
                self.logger.warning(f"Skipping idx {i} due to error: {e}")

        summary = {}
        if results:
            predicted_pops = [r['metrics_from_now']['pop_tp_first'] for r in results]
            actual_outcomes = [1 if r['actual_outcome']['outcome'] == 'tp_first' else 0 for r in results]

            df_results = pd.DataFrame({
                'index': indices[:len(predicted_pops)],
                'predicted_pop': predicted_pops,
                'actual_win': actual_outcomes
            })

            # Calibration by buckets
            bins = pd.cut(df_results['predicted_pop'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
            calibration = df_results.groupby(bins, observed=False)['actual_win'].mean().rename("actual_win_rate")

            acc = float(df_results['actual_win'].mean())
            summary = {
                "n_tests": int(len(df_results)),
                "accuracy": acc,
                "predicted_pop_median": float(df_results['predicted_pop'].median()),
                "calibration": calibration.to_dict(),
            }

            if verbose:
                print("\n--- Backtest Summary ---")
                print(df_results)
                print("\n--- Model Calibration ---")
                print("(Avg predicted POP bucket vs actual win rate)")
                print(calibration)

        return {"summary": summary, "results": results}
    
def main():
    p = argparse.ArgumentParser(description="Monte Carlo trade simulator for OHLCV CSVs")
    # Core single-trade simulation
    p.add_argument("csv", type=str, help="Path to OHLCV CSV (same format as your annotated files)")
    p.add_argument("--tp", type=float, help="Take-profit price (single-run mode)")
    p.add_argument("--sl", type=float, help="Stop-loss price (single-run mode)")
    p.add_argument("--entry", type=float, default=None, help="Entry price (optional; defaults to last close)")
    p.add_argument("--tf", type=str, default=None, choices=["1d","4h","1h","30m","15m","5m","1m"], help="Timeframe (infer from filename if omitted)")
    p.add_argument("--horizon", type=int, default=20, help="Number of bars to simulate ahead")
    p.add_argument("--model", type=str, default="garch", choices=["bootstrap", "gbm", "garch","ml_gbm"], help="Path generator model")
    p.add_argument("--paths", type=int, default=20000, help="Number of simulation paths")
    p.add_argument("--block", type=int, default=8, help="Block length for bootstrap model")
    p.add_argument("--seed", type=int, default=42, help="RNG seed")
    p.add_argument("--nrows", type=int, default=4000, help="Number of most recent rows to load")
    p.add_argument("--no-plots", action="store_true", help="Do not write HTML plots")
    p.add_argument("--ml-model", type=str, default=None, help="Path to a pre-trained LightGBM volatility model (.pkl)")
    p.add_argument("--mu-shift", type=float, default=0.0, help="Additive drift per bar applied to GBM/ML-GBM.")


    # Rolling backtest
    p.add_argument("--simulate-backtest", action="store_true", help="Run rolling backtest across decision points.")
    p.add_argument("--bt-tp-pips", type=float, help="Backtest TP offset from entry (price units).")
    p.add_argument("--bt-sl-pips", type=float, help="Backtest SL offset from entry (price units).")
    p.add_argument("--bt-horizon", type=int, default=None, help="Override horizon for backtest (defaults to --horizon).")
    p.add_argument("--bt-step", type=int, default=5, help="Bars between decision points.")
    p.add_argument("--bt-windows", type=int, default=40, help="Number of decision points to test.")
    p.add_argument("--bt-paths", type=int, default=5000, help="Simulation paths per decision point.")
    p.add_argument("--bt-model", type=str, choices=["bootstrap","gbm","ml_gbm"], default=None, help="Override model for backtest.")
    p.add_argument("--bt-no-json", action="store_true", help="Do not save per-window JSON during backtest.")
    args = p.parse_args()

    simulator = MonteCarloTradeSimulator()
    back_test_mode = simulator.simulate_backtest_trades

    if args.model == "garch" and not HAVE_ARCH:
        p.error("GARCH model requested but 'arch' not installed. pip install arch")
    if args.model == "ml_gbm" and not HAVE_LGB:
        p.error("ml_gbm requested but 'lightgbm' not installed. pip install lightgbm")

    if args.ml_model:
        args.ml_model = os.path.abspath(args.ml_model)

    if args.model == "ml_gbm" and args.ml_model:
        if os.path.exists(args.ml_model):
            simulator.lgb_model = joblib.load(args.ml_model)
            simulator.logger.info(f"Loaded ML model from: {args.ml_model}")
        else:
            simulator.logger.warning(f"ML model not found at {args.ml_model}; will train on the fly.")

    if args.simulate_backtest:
        if args.bt_tp_pips is None or args.bt_sl_pips is None:
            p.error("--bt-tp-pips and --bt-sl-pips are required when --simulate-backtest is set.")

        bt_res = back_test_mode(
            csv_path=args.csv,
            TP_pips=args.bt_tp_pips,
            SL_pips=args.bt_sl_pips,
            tf=args.tf,
            Horizon=(args.bt_horizon if args.bt_horizon is not None else args.horizon),
            step=args.bt_step,
            lookback_windows=args.bt_windows,
            model=(args.bt_model if args.bt_model is not None else args.model),
            paths=args.bt_paths,
            block_len=args.block,
            seed=args.seed,
            nrows=args.nrows,
            save_json=(not args.bt_no_json),
        )
        # Brief summary
        s = bt_res.get("summary", {})
        if s:
            print(f"\nBacktest ran {s.get('n_tests', 0)} tests; accuracy: {s.get('accuracy', 0.0):.2%}; median POP: {s.get('predicted_pop_median', 0.0):.2%}")
        return
    if args.tp is None or args.sl is None:
        p.error("In single-run mode you must provide --tp and --sl.")

    res = simulator.simulate_trade_for_csv(
        csv_path=args.csv,
        tp=args.tp, sl=args.sl, entry=args.entry,
        tf=args.tf, horizon_bars=args.horizon,
        model=args.model, n_paths=args.paths,
        block_len=args.block, seed=args.seed,
        nrows=args.nrows, save_plots=(not args.no_plots),
        ml_model=args.ml_model,
        mu_shift=args.mu_shift,
    )

    # Pretty print a brief summary to stdout
    now = res["metrics_from_now"]
    print("\n=== Monte Carlo (from NOW) ===")
    for k,v in now.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()