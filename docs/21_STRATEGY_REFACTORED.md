# Marketflow Strategy Update

- Below is a detailed plan and pseudo-algorithm to: (1) operationalize your a → b → c flow for any given TICKER; (2) modularize plotting like you did for Monte Carlo; and (3) add a long-only “Strategy” that ranks next-trade candidates using outputs from step “a”.

## Context from your repo

Step a (batch/single analysis): scripts/marketflow_batch_analysis.py calls marketflow.marketflow_analysis.run_analysis(ticker), which returns (narrative_text, output_dir). The analysis also saves per-timeframe data via save_timeframe_data into report directories under config.REPORT_DIR/YYYY-MM-DD/TICKER.
Step b (Monte Carlo): marketflow/marketflow_monte_carlo_trade.py exposes class MonteCarloTradeSimulator with simulate_trade_for_csv and optional backtest.
It writes `<timestamp>_mc_summary.json` and plots next to the CSV.
Step c (Plotting): scripts/plot_annotated_features.py generates Wyckoff charts, Volume Profile, and P&F. MC POP overlay now requires an explicit `--mc-summary` path whose `csv` identity matches the plotted CSV.

## Plan overview

Orchestration: Provide a single callable that runs a → b → c for a given ticker+timeframe, with caching to skip recomputation if inputs/params haven’t changed.
Plot module: Move plotting functions from scripts/plot_annotated_features.py into a proper module (marketflow/plotting/annotated_features.py). Keep the script as a thin CLI wrapper.
Strategy module: marketflow/strategy.py reads the annotated CSVs produced by step “a” and uses MC POP only when exactly one requested-timeframe MC summary is available. It produces a long-only ranked list with suggested entry/TP/SL and a score.

### Operationalizing a → b → c (single command for a TICKER)

Inputs: ticker, timeframe, and MC/plot params (defaults via config).
Step a: Call run_analysis(ticker) which returns output_dir such as .marketflow/reports/YYYY-MM-DD/TICKER. Within that folder, select an exact ticker/timeframe CSV identity; do not choose by first match, newest file, or timeframe-only fallback.
Step b: Compute TP/SL (heuristics below), entry=last close, and call MonteCarloTradeSimulator.simulate_trade_for_csv(csv_path, tp, sl, entry, tf, ...). Save outputs in the same folder.
Step c: Call the plotting module to produce Wyckoff/VP/P&F plots. The P&F figure adds a POP gauge only when the caller supplies an explicit matching `--mc-summary`.

### Caching

Maintain a small manifest.json in the same directory as the CSV with:
csv_hash (sha256 of CSV)
mc_hash (hash of MC parameters)
mc_summary_json (explicit MC summary artifact identity)
If hashes match and artifacts exist, skip re-running MC and plotting unless a --force option is set.

### Heuristics for TP/SL (Always Long)

    SL: max(tr_low, recent swing-low, close - k_atr*ATR), with k_atr ≈ 1.5–2.0.
    TP: close + min_rr * (close - SL), with min_rr ≥ 1.5. Optionally cap TP near a resistance or P&F objective.
    If Monte Carlo is available, you can optionally tune k_atr or min_rr to meet a target pop_tp_first threshold (e.g., ≥ 0.55).
    Long-only Strategy design

    Inputs per TICKER (from step “a” directory):
    Annotated CSV (columns such as timestamp, open, high, low, close, volume, wyckoff_phase, wyckoff_event, wyckoff_confirmed_event, tr_low, tr_high)
    Latest *_mc_summary.json for pop_tp_first and t_hit_tp_median (if present)
    Optional P&F sidecar JSON if you persist it (e.g., recent *_pnf_meta.json)
    Filters:
    Always Long: ignore setups that imply short-only conditions.
    Phase: prefer phases C/D/E; allow B if breakout above TR high and not too extended.
    Risk: SL distance ≤ max_sl_atr * ATR; RR ≥ min_rr.
    POP: if MC available, pop_tp_first ≥ min_pop (e.g., 0.55).
    “Not extended”: price within k1*ATR or ≤ m% above breakout (avoid chasing).
    Scoring (weighted sum; tunable):
    Wyckoff phase score (D > C > E > B > A)
    Confirmed bullish events: SOS, JAC, LPS, SPRING
    P&F context: last column X, recent double-top breakout, objective above price
    MC: higher pop_tp_first → higher score
    Simple trend constructiveness (e.g., HH/HL or MA stack)
    Output:
    Ranked list with ticker, tf, entry, sl, tp, rr, pop, context (phase/event), and score.

### Pseudo-algorithms and skeletons

#### `marketflow\marketflow_orchestrator.py`

    ```python

    from __future__ import annotations
    import os, json, hashlib, datetime as dt, glob
    import pandas as pd
    from marketflow.marketflow_analysis import run_analysis
    from marketflow.marketflow_monte_carlo_trade import MonteCarloTradeSimulator

    def _sha256_file(path: str) -> str:
        import hashlib
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1<<20), b""):
                h.update(chunk)
        return h.hexdigest()

    def _select_csv_for_tf(output_dir: str, ticker: str, tf: str) -> str:
        cands = sorted(glob.glob(os.path.join(output_dir, f"{ticker}_{tf}_wyckoff_annotated.csv")))
        if len(cands) != 1:
            raise FileNotFoundError(f"Expected one exact {ticker}/{tf} CSV in {output_dir}")
        return cands[0]

    def _atr(df: pd.DataFrame, n=14) -> float:
        tr = (df["high"]-df["low"]).clip(lower=0)
        return float(pd.Series(tr).rolling(n).mean().iloc[-1])

    def derive_tp_sl_long(df: pd.DataFrame, tf_cfg: dict) -> tuple[float, float]:
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
        if (not force) and manifest.get("csv_hash")==csv_hash and manifest.get("mc_hash")==mc_hash and manifest.get("mc_summary_json"):
            mc_fp = os.path.join(output_dir, manifest["mc_summary_json"])
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
            # record the explicit MC JSON artifact returned by the runner/service
            mc_summary_json = mc_out.get("summary_path") or mc_out.get("mc_summary_path")
            manifest.update({"csv_hash": csv_hash, "mc_hash": mc_hash, "mc_summary_json": mc_summary_json})
            json.dump(manifest, open(manifest_path, "w"), indent=2)

        # Step c — plots (moduleized function; MC POP requires explicit artifact input)
        if cfg.get("plots", {}).get("enabled", True):
            from marketflow.plotting.annotated_features import plot_features
            plot_features(
                csv_path,
                nrows=cfg["plots"].get("nrows", 4000),
                features=cfg["plots"].get("features"),
                box_size=cfg["plots"].get("box_size"),
                reversal=cfg["plots"].get("reversal", 3),
                pnf_scale=cfg["plots"].get("pnf_scale"),
                pnf_scale_value=cfg["plots"].get("pnf_scale_value"),
                mc_summary_path=mc_summary_json,
            )

        return {
            "ticker": ticker, "tf": tf, "output_dir": output_dir, "csv": csv_path,
            "mc_pop": mc_out.get("metrics_from_now", {}).get("pop_tp_first"),
        }
    ```

#### `marketflow\marketflow_strategy.py`

    ```python

    from __future__ import annotations
    import os, json, glob
    import pandas as pd
    from dataclasses import dataclass

    @dataclass
    class StrategyConfig:
        min_pop: float = 0.55     # require POP >= 55% when MC is present
        min_rr: float  = 1.5      # target RR
        max_sl_atr: float = 2.0   # SL distance constraint
        atr_len: int = 14
        prefer_phases: tuple[str,...] = ("C","D","E")
        weights: dict | None = None  # {"phase":2.0,"event":1.0,"pnf":1.0,"pop":2.5,"trend":1.0}

    def _unique_mc_for_timeframe(dir_: str, tf: str) -> dict | None:
        matches = []
        for name in os.listdir(dir_):
            if not name.endswith("_mc_summary.json"):
                continue
            data = json.load(open(os.path.join(dir_, name)))
            if data.get("tf") == tf or data.get("timeframe") == tf:
                matches.append(data)
        return matches[0] if len(matches) == 1 else None

    def _atr(df: pd.DataFrame, n=14) -> float:
        tr = (df["high"]-df["low"]).clip(lower=0)
        return float(pd.Series(tr).rolling(n).mean().iloc[-1])

    def _rr(close: float, sl: float, tp: float) -> float:
        risk = max(1e-9, close - sl); reward = max(0.0, tp - close)
        return reward / risk

    def _phase_score(phase: str) -> float:
        order = {"D":1.0, "C":0.8, "E":0.6, "B":0.4, "A":0.2, "UNKNOWN":0.0}
        return order.get(phase, 0.0)

    def _event_score(ev: str) -> float:
        return 1.0 if any(k in (ev or "") for k in ("SOS","JAC","LPS","SPRING")) else 0.0

    def _pnf_score(dir_: str) -> float:
        # optional: read *_pnf_meta.json to refine; neutral default
        return 0.5

    def _derive_sl_tp_long(df: pd.DataFrame, cfg: StrategyConfig) -> tuple[float,float,float]:
        close = float(df["close"].iloc[-1])
        atr = _atr(df, n=cfg.atr_len)
        tr_low = None
        if "tr_low" in df.columns and pd.notna(df["tr_low"].iloc[-1]):
            tr_low = float(df["tr_low"].iloc[-1])
        sl = max(tr_low or -1e9, close - cfg.max_sl_atr*atr)
        tp = close + cfg.min_rr* (close - sl)
        rr = _rr(close, sl, tp)
        return sl, tp, rr

    def _extract_context(df: pd.DataFrame) -> dict:
        ctx = {}
        ctx["phase"] = str(df["wyckoff_phase"].dropna().iloc[-1]) if "wyckoff_phase" in df.columns else "UNKNOWN"
        if "wyckoff_confirmed_event" in df.columns:
            nz = df["wyckoff_confirmed_event"].dropna()
            ctx["event"] = str(nz.iloc[-1]) if len(nz)>0 else ""
        else:
            ctx["event"] = ""
        return ctx

    def rank_long_candidates(report_root: str, date_glob: str, tickers: list[str], tf: str, cfg: StrategyConfig) -> list[dict]:
        results = []
        for t in tickers:
            # Locate exactly one per-ticker directory under the requested run/date glob.
            dirs = sorted(glob.glob(os.path.join(report_root, date_glob, t)))
            if len(dirs) != 1:
                continue
            out_dir = dirs[0]
            # find exactly one CSV for ticker/timeframe identity
            cands = sorted(glob.glob(os.path.join(out_dir, f"{t}_{tf}*_wyckoff_annotated.csv")))
            if len(cands) != 1:
                continue
            csv_path = cands[0]

            df = pd.read_csv(csv_path); df["timestamp"] = pd.to_datetime(df["timestamp"])
            sl, tp, rr = _derive_sl_tp_long(df, cfg)
            if rr < cfg.min_rr: 
                continue

            ctx = _extract_context(df)
            if ctx["phase"] not in cfg.prefer_phases and ctx["phase"] != "UNKNOWN":
                continue

            mc = _unique_mc_for_timeframe(out_dir, tf)
            pop = float(mc["metrics_from_now"]["pop_tp_first"]) if mc and "metrics_from_now" in mc else None
            if pop is not None and pop < cfg.min_pop:
                continue

            w = cfg.weights or {"phase":2.0,"event":1.0,"pnf":1.0,"pop":2.5,"trend":1.0}
            score = (
                w["phase"]*_phase_score(ctx["phase"]) +
                w["event"]*_event_score(ctx["event"]) +
                w["pnf"]*_pnf_score(out_dir) +
                w["pop"]*(pop if pop is not None else 0.5) +
                w["trend"]*0.5  # placeholder trend score
            )

            results.append({
                "ticker": t, "tf": tf, "csv": csv_path,
                "close": float(df["close"].iloc[-1]),
                "sl": sl, "tp": tp, "rr": rr, "pop": pop,
                "phase": ctx["phase"], "event": ctx["event"], "score": score
            })
        results.sort(key=lambda r: r["score"], reverse=True)
        return results
    ```

#### `marketflow/plotting/annotated_features.py`

    ```python

"""
Module wrapper for plotting annotated features (Wyckoff candlestick, Volume Profile, P&F),
so orchestration can call it programmatically.
You can move functions from scripts/plot_annotated_features.py here
and keep that script as a thin CLI wrapper.
"""
from __future__ import annotations
import os, datetime
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px

def plot_features(csv_file: str, *, nrows: int = 4000, features: list[str] | None = None,
                  box_size: float | None = None, reversal: int = 3,
                  pnf_scale: str | None = None, pnf_scale_value: float | None = None) -> dict:
    df = pd.read_csv(csv_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if len(df) > nrows:
        df = df.tail(nrows).copy()
    output_dir = os.path.dirname(csv_file)
    csv_name = os.path.basename(csv_file)

    # Call the existing functions (migrated here) to generate:
    # - Wyckoff candlestick chart
    # - Volume Profile
    # - Point & Figure with Wyckoff overlay and optional POP gauge from explicit --mc-summary
    # Return a minimal manifest of the generated artifact paths if desired.
    return {"output_dir": output_dir, "csv": csv_name}
    ```

#### `scripts/mf.py`

    ```python

"""
Unified CLI to run: (a) analysis, (b) Monte Carlo, (c) plotting, and (strategy) ranking.

Examples:
  python scripts/mf.py run --ticker PANW --tf 4h
  python scripts/mf.py strategy --tickers AAPL MSFT PANW --tf 4h --top 10
"""
import argparse, json, os
from marketflow.orchestrator import run_pipeline_for_ticker
from marketflow.strategy import rank_long_candidates, StrategyConfig
from marketflow.marketflow_config_manager import create_app_config

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run")
    r.add_argument("--ticker", required=True)
    r.add_argument("--tf", required=True)
    r.add_argument("--force", action="store_true")

    s = sub.add_parser("strategy")
    s.add_argument("--tickers", nargs="+", required=True)
    s.add_argument("--tf", default="4h")
    s.add_argument("--top", type=int, default=10)

    args = p.parse_args()
    cfg = create_app_config()  # pull REPORT_DIR etc.
    app_cfg = {
        "mc": {"model":"garch","horizon":40,"paths":20000,"block":8,"seed":42,"nrows":4000,"mu_shift":0.0},
        "plots": {"enabled": True, "nrows":4000, "pnf_scale":"percent","pnf_scale_value":0.005, "reversal":3},
        "strategy": {"min_rr":1.5, "sl_atr":2.0, "atr_len":14}
    }

    if args.cmd == "run":
        out = run_pipeline_for_ticker(args.ticker, args.tf, app_cfg, force=args.force)
        print(json.dumps(out, indent=2))
    else:
        ranked = rank_long_candidates(cfg.REPORT_DIR, "*", args.tickers, args.tf, StrategyConfig())
        print(json.dumps(ranked[:args.top], indent=2))

if __name__ == "__main__":
    main()

    ```

#### `.marketflow/config.yaml`

    ```yaml
    tickers: []
    timeframes: ["1h","4h","1d"]
    mc:
    model: "garch"      # "bootstrap" | "gbm" | "ml_gbm"
    horizon: 40
    paths: 20000
    block: 8
    seed: 42
    nrows: 4000
    mu_shift: 0.0
    plots:
    enabled: true
    nrows: 4000
    pnf_scale: "percent"
    pnf_scale_value: 0.005
    reversal: 3
    strategy:
    min_pop: 0.55
    min_rr: 1.5
    max_sl_atr: 2.0
    atr_len: 14
    prefer_phases: ["C","D","E"]
    weights: {phase: 2.0, event: 1.0, pnf: 1.0, pop: 2.5, trend: 1.0}
    ```
