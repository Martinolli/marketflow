"""
Monte Carlo simulator for trade outcomes (TP-first vs SL-first) using
either GBM or block bootstrap on OHLCV CSVs you already export.

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
"""
from __future__ import annotations
import os, json, argparse, datetime
import numpy as np
import pandas as pd

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except Exception as e:
    raise SystemExit("Plotly is required: pip install plotly")

# ------------------------------
# Logging (compatible fallback)
# ------------------------------
try:
    from marketflow.marketflow_logger import get_logger  # type: ignore
    logger = get_logger("monte_carlo_trade")
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    logger = logging.getLogger("monte_carlo_trade")

# ------------------------------
# IO helpers
# ------------------------------

def load_ohlcv(csv_path: str, nrows: int | None = None) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)
    df = pd.read_csv(csv_path)
    for col in ["timestamp", "open", "high", "low", "close", "volume"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    if nrows is not None and len(df) > nrows:
        df = df.tail(nrows)
    df = df.reset_index(drop=True)
    return df

TF_MAP = {"1d": 252, "4h": 2*252, "1h": 7*252, "30m": 13*252, "15m": 26*252, "5m": 78*252, "1m": 390*252}

def infer_tf_from_name(name: str) -> str | None:
    s = name.lower()
    for key in ["1d","4h","1h","30m","15m","5m","1m"]:
        if key in s: return key
    return None

# ------------------------------
# Core simulation
# ------------------------------

def calibrate_per_bar(closes: pd.Series, window: int = 400) -> tuple[float,float,np.ndarray]:
    """Return per-bar mu, sigma and recent log-returns (last `window`)."""
    r = np.log(closes).diff().dropna()
    if len(r) < 20:
        raise ValueError("Not enough bars to calibrate; need >= 20")
    r = r.tail(window)
    mu_bar = float(r.mean())
    sigma_bar = float(r.std(ddof=1))
    return mu_bar, sigma_bar, r.values

def simulate_gbm_paths(S0: float, mu_bar: float, sigma_bar: float, steps: int, n: int, rng: np.random.Generator) -> np.ndarray:
    # exact discretization using per-bar parameters (dt=1)
    drift = mu_bar - 0.5 * (sigma_bar ** 2)
    Z = rng.standard_normal((n, steps))
    log_increments = drift + sigma_bar * Z
    paths = np.empty((n, steps+1), dtype=float)
    paths[:,0] = S0
    np.cumprod(np.exp(log_increments), axis=1, out=paths[:,1:])
    paths[:,1:] *= S0
    return paths

def simulate_bootstrap_paths(S0: float, returns: np.ndarray, steps: int, n: int, block_len: int, rng: np.random.Generator) -> np.ndarray:
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

def barrier_stats(paths: np.ndarray, tp: float, sl: float) -> dict:
    n, T = paths.shape
    T -= 1
    hit_tp = np.zeros(n, dtype=bool)
    hit_sl = np.zeros(n, dtype=bool)
    t_tp = np.full(n, T, dtype=int)
    t_sl = np.full(n, T, dtype=int)

    for i in range(n):
        p = paths[i,1:]
        above = np.where(p >= tp)[0]
        below = np.where(p <= sl)[0]
        if above.size:
            hit_tp[i] = True; t_tp[i] = int(above[0])
        if below.size:
            hit_sl[i] = True; t_sl[i] = int(below[0])
        if hit_tp[i] and hit_sl[i]:
            # first passage priority
            if t_sl[i] < t_tp[i]:
                hit_tp[i] = False
            else:
                hit_sl[i] = False
    pop = float(hit_tp.mean())
    psl = float(hit_sl.mean())
    pneither = float(1 - pop - psl)
    last = paths[:,-1]
    S0 = paths[:,0]
    R = np.where(hit_tp, 1.0, np.where(hit_sl, -1.0, (last - S0) / (S0 - sl)))
    out = {
        "pop_tp_first": pop,
        "p_sl_first": psl,
        "p_neither": pneither,
        "t_hit_tp_median": int(np.median(t_tp[hit_tp])) if pop>0 else None,
        "t_hit_sl_median": int(np.median(t_sl[hit_sl])) if psl>0 else None,
        "R_mean": float(np.mean(R)),
        "R_p50": float(np.median(R)),
        "R_p05": float(np.percentile(R,5)),
        "R_p95": float(np.percentile(R,95)),
    }
    return out

# ------------------------------
# Plot helpers (Plotly)
# ------------------------------

def fan_chart(paths: np.ndarray, title: str) -> go.Figure:
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

def hits_histogram(metrics: dict, title: str) -> go.Figure:
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

# ------------------------------
# Runner
# ------------------------------

def simulate_trade_for_csv(csv_path: str, tp: float, sl: float, entry: float | None = None,
                           tf: str | None = None, horizon_bars: int = 20,
                           model: str = "bootstrap", n_paths: int = 20000,
                           block_len: int = 8, seed: int = 42,
                           nrows: int | None = 4000,
                           save_plots: bool = True) -> dict:
    df = load_ohlcv(csv_path, nrows=nrows)
    closes = df["close"]
    S0_now = float(closes.iloc[-1])
    S0 = float(entry) if entry is not None else S0_now

    tf = tf or infer_tf_from_name(os.path.basename(csv_path)) or "4h"

    mu_bar, sigma_bar, r = calibrate_per_bar(closes)
    rng = np.random.default_rng(seed)

    if model == "gbm":
        paths_now = simulate_gbm_paths(S0_now, mu_bar, sigma_bar, horizon_bars, n_paths, rng)
        paths_entry = simulate_gbm_paths(S0,     mu_bar, sigma_bar, horizon_bars, n_paths, rng)
    elif model == "bootstrap":
        paths_now = simulate_bootstrap_paths(S0_now, r, horizon_bars, n_paths, block_len, rng)
        paths_entry = simulate_bootstrap_paths(S0,     r, horizon_bars, n_paths, block_len, rng)
    else:
        raise ValueError("model must be 'gbm' or 'bootstrap'")

    m_now   = barrier_stats(paths_now, tp, sl)
    m_entry = barrier_stats(paths_entry, tp, sl)

    out = {
        "csv": os.path.basename(csv_path),
        "tf": tf,
        "params": {"tp": tp, "sl": sl, "entry": entry, "horizon_bars": horizon_bars, "model": model, "paths": n_paths, "block_len": block_len, "seed": seed},
        "spot": {"S0_now": S0_now, "S0_entry": S0},
        "metrics_from_now": m_now,
        "metrics_from_entry": m_entry,
    }

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.dirname(csv_path) or "."

    # Save JSON
    json_path = os.path.join(out_dir, f"{ts}_mc_summary.json")
    with open(json_path, "w") as fh:
        json.dump(out, fh, indent=2)
    logger.info(f"Monte Carlo summary saved: {json_path}")

    if save_plots:
        # Fan chart (from now)
        fig_fan = fan_chart(paths_now, title=f"MC Fan Chart — {os.path.basename(csv_path)} (from now)")
        fan_path = os.path.join(out_dir, f"{ts}_mc_paths.html")
        fig_fan.write_html(fan_path)
        logger.info(f"Fan chart saved: {fan_path}")

        # Hits histogram (medians)
        fig_hits = hits_histogram(m_now, title="Median bars to TP/SL")
        hits_path = os.path.join(out_dir, f"{ts}_mc_hits.html")
        fig_hits.write_html(hits_path)
        logger.info(f"Hits histogram saved: {hits_path}")

    return out

# ------------------------------
# CLI
# ------------------------------

def main():
    p = argparse.ArgumentParser(description="Monte Carlo trade simulator for OHLCV CSVs")
    p.add_argument("csv", type=str, help="Path to OHLCV CSV (same format as your annotated files)")
    p.add_argument("--tp", type=float, required=True, help="Take-profit price")
    p.add_argument("--sl", type=float, required=True, help="Stop-loss price")
    p.add_argument("--entry", type=float, default=None, help="Entry price (optional; defaults to last close)")
    p.add_argument("--tf", type=str, default=None, choices=["1d","4h","1h","30m","15m","5m","1m"], help="Timeframe (infer from filename if omitted)")
    p.add_argument("--horizon", type=int, default=20, help="Number of bars to simulate ahead")
    p.add_argument("--model", type=str, default="bootstrap", choices=["bootstrap","gbm"], help="Path generator model")
    p.add_argument("--paths", type=int, default=20000, help="Number of simulation paths")
    p.add_argument("--block", type=int, default=8, help="Block length for bootstrap model")
    p.add_argument("--seed", type=int, default=42, help="RNG seed")
    p.add_argument("--nrows", type=int, default=4000, help="Number of most recent rows to load")
    p.add_argument("--no-plots", action="store_true", help="Do not write HTML plots")
    args = p.parse_args()

    res = simulate_trade_for_csv(
        csv_path=args.csv,
        tp=args.tp, sl=args.sl, entry=args.entry,
        tf=args.tf, horizon_bars=args.horizon,
        model=args.model, n_paths=args.paths,
        block_len=args.block, seed=args.seed,
        nrows=args.nrows, save_plots=(not args.no_plots),
    )

    # Pretty print a brief summary to stdout
    now = res["metrics_from_now"]
    ent = res["metrics_from_entry"]
    print("\n=== Monte Carlo (from NOW) ===")
    for k,v in now.items():
        print(f"{k}: {v}")
    print("\n=== Monte Carlo (from ENTRY) ===")
    for k,v in ent.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
