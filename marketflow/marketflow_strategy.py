r"""
Refactored strategy module — MC & PnF optional.

Usage examples:
1) After running batch analysis: 
   python MARKETFLOW/marketflow_strategy.py --report-root ./reports --batch latest --tf 1h --tickers AAPL MSFT NVDA

2) Directly against a date folder:
   python MARKETFLOW/marketflow_strategy.py --report-root ./reports --date-glob "2025-09-*" --tf 4h --tickers AAPL MSFT

3) for tf in 1h 4h 30m 1d 1w; do
  python marketflow_strategy_refactored.py ^
    --report-root "C:\Users\Aspire5 15 i7 4G2050\marketflow\.marketflow\reports" --batch latest --tf(s) $tf --tickers AI ATRO DRS FLY KTOS RGR RKLB SPR TATT

Notes
- Does NOT require Monte Carlo (MC) or P&F files. When absent or disabled, it uses neutral defaults and ATR-based SL/TP.
- Compatible with the existing marketflow_batch_analysis.py output layout.
"""

from __future__ import annotations
import argparse, os, json, glob
from dataclasses import dataclass, field
from typing import Iterable, List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("MarketFlowStrategy")
app_cfg = create_app_config(logger=logger)

# -----------------------------
# Config & helpers
# -----------------------------
@dataclass
class StrategyConfig:
    # Core thresholds
    min_rr: float = 1.5                 # target RR (TP/SL)
    max_sl_atr: float = 2.0             # stop = max(tr_low, close - max_sl_atr*ATR)
    atr_len: int = 14

    # Wyckoff preferences
    prefer_phases: Tuple[str, ...] = ("C", "D", "E")

    # Feature toggles
    use_mc: bool = False                # <—— MC optional
    use_pnf: bool = False               # <—— PnF optional

    # POP gates (only applied if use_mc=True AND POP present)
    min_pop: float = 0.55               # main POP ≥ 55%
    min_pop_backup: float = 0.50        # backup POP ≥ 50%

    # Weights for composite score (sum free; normalized internally)
    weights: Dict[str, float] = field(default_factory=lambda: {
        "phase": 2.0, "event": 1.0, "pnf": 1.0, "pop": 2.5, "trend": 1.0
    })

# -----------------------------
# Low-level utilities
# -----------------------------

def _latest_file(dir_: str, suffix: str) -> Optional[str]:
    logger.debug(f"Searching for latest file in {dir_} with suffix '{suffix}'")
    files = [f for f in os.listdir(dir_) if f.endswith(suffix)]
    if not files:
        logger.debug("No matching files found.")
        return None
    files.sort(key=lambda f: os.path.getmtime(os.path.join(dir_, f)), reverse=True)
    latest = os.path.join(dir_, files[0])
    logger.debug(f"Latest file found: {latest}")
    return latest

def _latest_mc(dir_: str) -> Optional[dict]:
    logger.debug(f"Loading latest Monte Carlo summary from {dir_}")
    try:
        path = _latest_file(dir_, "_mc_summary.json")
        if path:
            logger.debug(f"Loading MC summary file: {path}")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.debug("MC summary loaded successfully.")
            return data
        else:
            logger.debug("No MC summary file found.")
            return None
    except Exception as e:
        logger.error(f"Error loading MC summary: {e}")
        return None

def _atr(df: pd.DataFrame, n: int = 14) -> float:
    logger.debug(f"Calculating ATR with window: {n}")
    tr = (df["high"] - df["low"]).clip(lower=0)
    atr = pd.Series(tr).rolling(n).mean().iloc[-1]
    result = float(atr) if pd.notna(atr) else float(tr.iloc[-n:].mean())
    logger.debug(f"ATR result: {result}")
    return result

def _rr(close: float, sl: float, tp: float) -> float:
    logger.debug(f"Calculating RR: close={close}, sl={sl}, tp={tp}")
    risk = max(1e-9, close - sl)
    reward = max(0.0, tp - close)
    rr = reward / risk if risk > 0 else 0.0
    logger.debug(f"RR result: {rr}")
    return rr

def _phase_score(phase: str) -> float:
    logger.debug(f"Scoring phase: {phase}")
    order = {"D": 1.0, "C": 0.8, "E": 0.6, "B": 0.4, "A": 0.2, "UNKNOWN": 0.0}
    score = order.get((phase or "UNKNOWN"), 0.0)
    logger.debug(f"Phase score: {score}")
    return score


def _event_score(ev: str) -> float:
    logger.debug(f"Scoring event: {ev}")
    ev = (ev or "").upper()
    keys = ("SOS", "JAC", "LPS", "SPRING")
    score = 1.0 if any(k in ev for k in keys) else 0.0
    logger.debug(f"Event score: {score}")
    return score


def _pnf_score_neutral() -> float:
    logger.debug("Returning neutral P&F score (0.5)")
    # Neutral when P&F meta is not used yet
    return 0.5


def _derive_sl_tp_long(df: pd.DataFrame, cfg: StrategyConfig) -> Tuple[float, float, float]:
    logger.debug("Deriving SL/TP/RR for long candidate")
    close = float(df["close"].iloc[-1])
    atr = _atr(df, n=cfg.atr_len)
    logger.debug(f"Close: {close}, ATR: {atr}")

    tr_low = None
    if "tr_low" in df.columns and pd.notna(df["tr_low"].iloc[-1]):
        tr_low = float(df["tr_low"].iloc[-1])
        logger.debug(f"tr_low found: {tr_low}")

    sl = max(tr_low or -1e12, close - cfg.max_sl_atr * atr)
    tp = close + cfg.min_rr * (close - sl)
    rr = _rr(close, sl, tp)
    logger.debug(f"Derived SL: {sl}, TP: {tp}, RR: {rr}")
    return sl, tp, rr


def _extract_context(df: pd.DataFrame) -> Dict[str, str]:
    logger.debug("Extracting Wyckoff context")
    ctx: Dict[str, str] = {}
    phase = "UNKNOWN"
    if "wyckoff_phase" in df.columns:
        nz = df["wyckoff_phase"].dropna()
        if len(nz):
            phase = str(nz.iloc[-1])
    ctx["phase"] = phase
    logger.debug(f"Extracted phase: {phase}")

    ev = ""
    if "wyckoff_confirmed_event" in df.columns:
        nz = df["wyckoff_confirmed_event"].dropna()
        ev = str(nz.iloc[-1]) if len(nz) else ""
    ctx["event"] = ev
    logger.debug(f"Extracted event: {ev}")

    # Simple direction/trend placeholder (can be replaced with your trend module)
    trend = "up" if df["close"].iloc[-1] >= df["close"].rolling(20).mean().iloc[-1] else "flat"
    ctx["trend"] = trend
    logger.debug(f"Extracted trend: {trend}")
    return ctx

# -----------------------------
# Core ranking logic
# -----------------------------

def rank_long_candidates(
    report_root: str,
    date_glob: str,
    tickers: Iterable[str],
    tf: str,
    cfg: StrategyConfig,
    use_batch_namespace: Optional[str] = None,
) -> List[Dict]:
    """
    Scan per-ticker report folders and rank long candidates.

    - If use_batch_namespace == "latest", will pick the most recent "batch_*" folder under report_root.
    - If date_glob provided (e.g., "2025-09-*"), it filters under that pattern.
    - MC/P&F are optional and neutral when absent or disabled by cfg.
    """
    logger.info(f"Ranking long candidates: report_root={report_root}, date_glob={date_glob}, tickers={list(tickers)}, tf={tf}, use_batch_namespace={use_batch_namespace}")
    results: List[Dict] = []

    # Resolve batch folder if requested
    if use_batch_namespace == "latest":
        batch_dirs = [d for d in glob.glob(os.path.join(report_root, "batch_*")) if os.path.isdir(d)]
        logger.info(f"Found batch directories: {batch_dirs}")
        if batch_dirs:
            date_glob = os.path.basename(sorted(batch_dirs)[-1])  # use latest batch_YYYYMMDD_HHMMSS
            logger.info(f"Using latest batch directory: {date_glob}")

    for t in tickers:
        logger.info(f"Processing ticker: {t}")
        # Possible layouts:
        #   report_root/date_glob/TICKER
        #   report_root/batch_YYYYMMDD_HHMMSS/TICKER
        dirs = sorted(glob.glob(os.path.join(report_root, date_glob, t))) if date_glob else []
        if not dirs:
            # fallback: any folder directly under report_root matching ticker
            dirs = sorted(glob.glob(os.path.join(report_root, "**", t), recursive=True))
            dirs = [d for d in dirs if os.path.isdir(d)]
        logger.info(f"Found directories for ticker {t}: {dirs}")
        if not dirs:
            logger.info(f"No directories found for ticker {t}, skipping.")
            continue
        out_dir = dirs[-1]
        logger.info(f"Using output directory for ticker {t}: {out_dir}")

        # Locate CSV for timeframe
        cands = sorted(glob.glob(os.path.join(out_dir, f"{t}_*{tf}*.csv")))
        if not cands:
            cands = sorted(glob.glob(os.path.join(out_dir, f"*{tf}*.csv")))
        logger.info(f"Found CSV candidates for ticker {t}: {cands}")
        if not cands:
            logger.info(f"No CSV files found for ticker {t}, skipping.")
            continue
        csv_path = cands[-1]
        logger.info(f"Using CSV file for ticker {t}: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            logger.error(f"Error reading CSV for ticker {t}: {e}")
            continue
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])  # keep for future filters

        # Derive SL/TP/ RR from ATR + tr_low (if present)
        sl, tp, rr = _derive_sl_tp_long(df, cfg)
        logger.info(f"Derived SL/TP/RR for ticker {t}: SL={sl}, TP={tp}, RR={rr}")
        if rr < cfg.min_rr:
            # skip if the natural geometry can't get us ≥ min_rr
            logger.info(f"RR {rr} below min_rr {cfg.min_rr} for ticker {t}, skipping.")
            continue

        # Extract Wyckoff context
        ctx = _extract_context(df)
        logger.info(f"Extracted context for ticker {t}: {ctx}")
        if ctx["phase"] not in cfg.prefer_phases and ctx["phase"] != "UNKNOWN":
            # prefer phases C/D/E; allow UNKNOWN to pass (will be penalized by score)
            logger.info(f"Phase {ctx['phase']} not in preferred phases {cfg.prefer_phases} for ticker {t}, skipping.")
            continue

        # Optional: Monte Carlo POP
        pop: Optional[float] = None
        if cfg.use_mc:
            mc = _latest_mc(out_dir)
            logger.info(f"Monte Carlo summary for ticker {t}: {mc}")
            if mc and isinstance(mc, dict):
                try:
                    pop = float(mc.get("metrics_from_now", {}).get("pop_tp_first", None))
                except Exception:
                    pop = None
            # Apply gates only if we found a POP figure
            if pop is not None and (pop < cfg.min_pop and pop < cfg.min_pop_backup):
                logger.info(f"POP {pop} below min_pop {cfg.min_pop} and min_pop_backup {cfg.min_pop_backup} for ticker {t}, skipping.")
                continue

        # Composite score (normalize weights)
        w = cfg.weights
        wsum = sum(w.values()) if w else 1.0
        norm = {k: (v / wsum) for k, v in w.items()}

        phase_s = _phase_score(ctx["phase"])               # 0…1
        event_s = _event_score(ctx["event"])               # 0 or 1
        pnf_s   = _pnf_score_neutral()                       # neutral 0.5 until we wire P&F
        pop_s   = (pop if pop is not None else 0.5)          # neutral 0.5 when MC off/missing
        trend_s = 0.75 if ctx.get("trend") == "up" else 0.5 # simple placeholder

        score = (
            norm["phase"]*phase_s +
            norm["event"]*event_s +
            norm["pnf"]*pnf_s +
            norm["pop"]*pop_s +
            norm["trend"]*trend_s
        ) * 100.0

        logger.info(f"Final score for ticker {t}: {score}")

        results.append({
            "ticker": t,
            "tf": tf,
            "csv": csv_path,
            "close": float(df["close"].iloc[-1]),
            "sl": sl, "tp": tp, "rr": _rr(float(df["close"].iloc[-1]), sl, tp),
            "pop": pop,
            "phase": ctx["phase"],
            "event": ctx["event"],
            "trend": ctx["trend"],
            "score": round(score, 2),
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    logger.info(f"Total candidates ranked: {len(results)}")
    return results

# -----------------------------
# CLI
# -----------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Rank long candidates from Wyckoff CSV reports (MC/P&F optional)")
    p.add_argument("--report-root", required=True, help="Base reports directory")
    g = p.add_mutually_exclusive_group(required=False)
    g.add_argument("--date-glob", default="*", help="Date folder glob under report-root (e.g., 2025-09-*)")
    g.add_argument("--batch", choices=["latest"], help="Use the latest batch_* folder under report-root")
    p.add_argument("--tf", default="1h", help="Timeframe key to pick CSV (e.g., 1h, 4h, 1d). Can be comma-separated for multiple (e.g., 4h,2h,1h)")
    p.add_argument("--tfs", nargs="+", help="List of timeframes to process (e.g., 1w 1d 4h 2h 1h 30m)")
    p.add_argument("--tickers", nargs="+", help="Symbols to scan")
    p.add_argument("--use-mc", action="store_true", help="Enable Monte Carlo POP gating if available")
    p.add_argument("--use-pnf", action="store_true", help="(Reserved) Enable P&F scoring when wired")
    p.add_argument("--min-rr", type=float, default=1.5)
    p.add_argument("--max-sl-atr", type=float, default=2.0)
    p.add_argument("--prefer-phases", default="C,D,E", help="Comma list (default C,D,E)")
    return p.parse_args()


def main():
    args = _parse_args()
    cfg = StrategyConfig(
        min_rr=args.min_rr,
        max_sl_atr=args.max_sl_atr,
        prefer_phases=tuple([p.strip() for p in args.prefer_phases.split(',') if p.strip()]),
        use_mc=bool(args.use_mc),
        use_pnf=bool(args.use_pnf),
    )

    # Build the list of timeframes to process: prefer --tfs, else --tf (supports comma-separated)
    tfs: List[str] = []
    if args.tfs:
        for item in args.tfs:
            tfs.extend([x.strip() for x in item.split(",") if x.strip()])
    else:
        tfs = [x.strip() for x in str(args.tf).split(",") if x.strip()]

    # Deduplicate while preserving order
    seen = set()
    tfs = [tf for tf in tfs if not (tf in seen or seen.add(tf))]

    all_results: List[Dict] = []
    per_tf_outputs: List[str] = []

    for tf in tfs:
        results = rank_long_candidates(
            report_root=args.report_root,
            date_glob=args.date_glob if not args.batch else "*",
            tickers=args.tickers,
            tf=tf,
            cfg=cfg,
            use_batch_namespace=args.batch,
        )

        print(f"\n=== Timeframe: {tf} ===")
        if not results:
            print("No candidates passed the filters.")
        else:
            cols = ["ticker","tf","close","sl","tp","rr","pop","phase","event","trend","score"]
            df = pd.DataFrame(results)[cols]
            with pd.option_context('display.max_columns', None, 'display.width', 120):
                print(df.to_string(index=False))

        # Save per-timeframe JSON to avoid overwriting
        current_directory = os.getcwd()
        out_path_tf = os.path.join(current_directory,".marketflow/reports/strategy_data", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_strategy_candidates_{tf}.json")
        with open(out_path_tf, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Saved candidates for {tf} to {out_path_tf}")

        per_tf_outputs.append(out_path_tf)
        all_results.extend(results)

    # Also save a consolidated JSON with all timeframes
    current_directory = os.getcwd()
    out_path_all = os.path.join(current_directory, ".marketflow/reports/strategy_data", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_strategy_candidates.json")
    with open(out_path_all, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✅ Saved consolidated candidates to {out_path_all}")
    if per_tf_outputs:
        print("Per-timeframe files:")
        for pth in per_tf_outputs:
            print(f" - {pth}")
    

if __name__ == "__main__":
    main()
