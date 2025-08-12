# scripts/marketflow_risk_placement.py
from ib_insync import IB, Stock, util
import pandas as pd
import math, argparse, math as _math

def atr(bars, n=14):
    df = pd.DataFrame([{"high": b.high, "low": b.low, "close": b.close} for b in bars])
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        (df["high"] - df["low"]).abs(),
        (df["high"] - prev_close).abs(),
        (df["low"]  - prev_close).abs()
    ], axis=1).max(axis=1)
    a = float(tr.rolling(n).mean().iloc[-1])
    # fallback if NaN (too few bars)
    if _math.isnan(a) or a <= 0:
        a = float(df["close"].iloc[-1]) * 0.005  # ~0.5% of price
    return a

def position_size_by_risk(nl, risk_pct, entry, stop):
    per_share = max(0.01, abs(entry - stop))
    qty = math.floor((nl * risk_pct) / per_share)
    return max(0, qty)

def plan_bracket(symbol="AMD", port=4002, risk_pct=0.002, atr_mult=1.5, tp_rr=2.0, client_id=55, dry_run=True):
    ib = IB()
    print(f"Connecting to TWS 127.0.0.1:{port} (clientId={client_id}) …")
    ib.connect('127.0.0.1', port, clientId=client_id, timeout=10)
    assert ib.isConnected(), "Not connected to TWS."

    c = ib.qualifyContracts(Stock(symbol, 'SMART', 'USD'))[0]
    bars = ib.reqHistoricalData(c, endDateTime='', durationStr='2 D', barSizeSetting='5 mins',
                                whatToShow='TRADES', useRTH=False, formatDate=1)
    last = float(bars[-1].close)
    a = atr(bars)
    stop = round(last - atr_mult * a, 2)          # LONG stop
    tp   = round(last + tp_rr * (last - stop), 2) # RR-based TP

    nl = 0.0
    for v in ib.accountSummary():
        if v.tag == 'NetLiquidation':
            nl = float(v.value)
            break
    qty = position_size_by_risk(nl, risk_pct, last, stop)

    print(f"{symbol} last={last:.2f} ATR={a:.2f} stop={stop:.2f} tp={tp:.2f} qty={qty} (NL={nl:.2f})")

    parent, takeProfit, stopLoss = ib.bracketOrder('BUY', qty, None, tp, stop)
    if dry_run:
        print("[DRY] Would place bracket (parent+TP+SL).")
    else:
        ib.placeOrder(c, parent); ib.placeOrder(c, takeProfit); ib.placeOrder(c, stopLoss)
        print("Bracket submitted on PAPER. Check TWS → Orders.")
    ib.disconnect()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="AMD")
    ap.add_argument("--port", type=int, default=4002)     # your working port
    ap.add_argument("--risk-pct", type=float, default=0.002)
    ap.add_argument("--atr-mult", type=float, default=1.5)
    ap.add_argument("--tp-rr", type=float, default=2.0)
    ap.add_argument("--client-id", type=int, default=55)
    ap.add_argument("--live", action="store_true", help="Place a real PAPER order (not dry-run)")
    args = ap.parse_args()
    plan_bracket(symbol=args.symbol, port=args.port, risk_pct=args.risk_pct,
                 atr_mult=args.atr_mult, tp_rr=args.tp_rr, client_id=args.client_id,
                 dry_run=(not args.live))
