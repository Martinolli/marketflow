"""
Orchestrator for running MarketFlow analysis, Monte Carlo trade simulations, and plotting.

"""

from __future__ import annotations
import os, json, hashlib, datetime as dt, glob
import pandas as pd
from marketflow.marketflow_analysis import run_analysis
from marketflow.marketflow_monte_carlo_trade import MonteCarloTradeSimulator

def _sha256_file(path: str) -> str:
    """
    Compute SHA256 hash of a file.
    
    Args:
        path (str): Path to the file.
    Returns:
        str: Hexadecimal SHA256 hash of the file    
    """
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def _select_csv_for_tf(output_dir: str, ticker: str, tf: str) -> str:
    """
    Select the most appropriate CSV file for the given timeframe from the output directory.
    Args:
        output_dir (str): Directory containing CSV files.
        ticker (str): Ticker symbol to filter files.
        tf (str): Timeframe string to filter files.
    Returns:
        str: Path to the selected CSV file.
    
    """
    # Be flexible about suffixes; prefer files containing f"_{tf}" and ".csv"
    cands = sorted(glob.glob(os.path.join(output_dir, f"{ticker}_*{tf}*.csv")))
    if not cands:
        # fallback: any CSV with tf in the name
        cands = sorted(glob.glob(os.path.join(output_dir, f"*{tf}*.csv")))
    if not cands:
        raise FileNotFoundError(f"No CSV for tf={tf} in {output_dir}")
    return cands[-1]

def _atr(df: pd.DataFrame, n=14) -> float:
    """
    Compute the Average True Range (ATR) over the last n periods.
    Args:
        df (pd.DataFrame): DataFrame containing 'high' and 'low' columns.
        n (int): Number of periods to calculate ATR over.
    Returns:
        float: The ATR value.
    
    """
    
    tr = (df["high"]-df["low"]).clip(lower=0)
    return float(pd.Series(tr).rolling(n).mean().iloc[-1])

def derive_tp_sl_long(df: pd.DataFrame, tf_cfg: dict) -> tuple[float, float]:
    """
    Derive take-profit (TP) and stop-loss (SL) levels for a long trade based on ATR and configuration.
    Args:
        df (pd.DataFrame): DataFrame containing price data with 'close' and optionally 'tr_low' columns.
        tf_cfg (dict): Configuration dictionary with keys 'atr_len', 'sl_atr', and 'min_rr'.
    Returns:
        tuple[float, float]: Calculated TP and SL levels.
    
    """
    close = float(df["close"].iloc[-1])
    atr = _atr(df, n=tf_cfg.get("atr_len", 14))
    tr_low = None
    if "tr_low" in df.columns and pd.notna(df["tr_low"].iloc[-1]):
        tr_low = float(df["tr_low"].iloc[-1])
    sl = max(tr_low or -1e9, close - tf_cfg.get("sl_atr", 2.0)*atr)
    risk = max(1e-9, close - sl)
    tp = close + tf_cfg.get("min_rr", 1.5) * risk
    return tp, sl

def run_pipeline_for_ticker(ticker: str, tf: str, cfg: dict, force: bool=False) -> dict:
    """
    Run the full pipeline for a given ticker and timeframe, including analysis, Monte Carlo simulation, and plotting.
    Args:
        ticker (str): Ticker symbol to analyze.
        tf (str): Timeframe string (e.g., '1h', '4h', '1d').
        cfg (dict): Configuration dictionary with keys for 'mc' and 'plots'.
        force (bool): If True, forces re-running the Monte Carlo simulation even if inputs are unchanged.
    Returns:
        dict: Dictionary containing results including 'ticker', 'tf', 'output_dir', 'csv', and 'mc_pop'.
    
    """
    # Step a — analysis; returns output_dir (.marketflow/reports/YYYY-MM-DD/TICKER)
    narrative, output_dir = run_analysis(ticker, timeframes=[tf])
    csv_path = _select_csv_for_tf(output_dir, ticker, tf)

    # caching manifest next to CSV
    manifest_path = os.path.join(output_dir, "manifest.json")
    csv_hash = _sha256_file(csv_path)
    mc_key = {k: cfg["mc"][k] for k in ("model","paths","horizon","block","seed","nrows","mu_shift") if k in cfg.get("mc",{})}
    mc_hash = hashlib.sha256(json.dumps(mc_key, sort_keys=True).encode()).hexdigest()
    manifest = {}
    if os.path.exists(manifest_path):
        try: manifest = json.load(open(manifest_path))
        except: manifest = {}

    # Step b — MC (skip if unchanged)
    mc_out = None
    if (not force) and manifest.get("csv_hash")==csv_hash and manifest.get("mc_hash")==mc_hash and manifest.get("latest_mc_json"):
        mc_fp = os.path.join(output_dir, manifest["latest_mc_json"])
        try: mc_out = json.load(open(mc_fp))
        except: mc_out = None

    if mc_out is None:
        df = pd.read_csv(csv_path); df["timestamp"] = pd.to_datetime(df["timestamp"])
        tp, sl = derive_tp_sl_long(df, cfg.get("strategy", {}))
        entry = float(df["close"].iloc[-1])

        sim = MonteCarloTradeSimulator(model_type=cfg["mc"].get("model","garch"))
        mc_out = sim.simulate_trade_for_csv(
            csv_path=csv_path, tp=tp, sl=sl, entry=entry,
            tf=tf, horizon_bars=cfg["mc"].get("horizon", 20),
            model=cfg["mc"].get("model","garch"), n_paths=cfg["mc"].get("paths", 20000),
            block_len=cfg["mc"].get("block", 8), seed=cfg["mc"].get("seed", 42),
            nrows=cfg["mc"].get("nrows", 4000), save_plots=(not cfg["mc"].get("no_plots", False)),
            ml_model=cfg["mc"].get("ml_model"), mu_shift=cfg["mc"].get("mu_shift", 0.0),
        )
        # capture the just-written MC JSON filename
        latest = max((f for f in os.listdir(output_dir) if f.endswith("_mc_summary.json")),
                    key=lambda f: os.path.getmtime(os.path.join(output_dir, f)))
        manifest.update({"csv_hash": csv_hash, "mc_hash": mc_hash, "latest_mc_json": latest})
        json.dump(manifest, open(manifest_path, "w"), indent=2)

    # Step c — plots (moduleized function; plots read MC POP automatically from same dir)
    if cfg.get("plots", {}).get("enabled", True):
        from deprecated_backup.modules.annotated_features import plot_features
        plot_features(
            csv_path,
            nrows=cfg["plots"].get("nrows", 4000),
            features=cfg["plots"].get("features"),
            box_size=cfg["plots"].get("box_size"),
            reversal=cfg["plots"].get("reversal", 3),
            pnf_scale=cfg["plots"].get("pnf_scale"),
            pnf_scale_value=cfg["plots"].get("pnf_scale_value"),
        )

    return {
        "ticker": ticker, "tf": tf, "output_dir": output_dir, "csv": csv_path,
        "mc_pop": mc_out.get("metrics_from_now", {}).get("pop_tp_first"),
    }