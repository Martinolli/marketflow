"""
Unified CLI to run: (a) analysis, (b) Monte Carlo, (c) plotting, and (strategy) ranking.

Examples:
  python scripts/mf.py run --ticker PANW --tf 4h
  python scripts/mf.py strategy --tickers AAPL MSFT PANW --tf 4h --top 10
"""
import argparse, json, os
from deprecated_backup.modules.marketflow_orchestrator import run_pipeline_for_ticker
from marketflow.marketflow_strategy import rank_long_candidates, StrategyConfig
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