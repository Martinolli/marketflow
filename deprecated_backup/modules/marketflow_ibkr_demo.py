# marketflow_ibkr_demo.py
from ib_insync import IB, Stock, util
import logging

log = logging.getLogger("IBKR")
logging.basicConfig(level=logging.INFO, format="%(message)s")

HOST = "127.0.0.1"
PORT = 4002          # 4002 = paper, 7496 = live
CLIENT_ID = 55
DRY_RUN = False       # start True; flip to False later to actually place paper orders

def main(symbol="AMD"):
    ib = IB()
    log.info(f"Connecting to TWS on {HOST}:{PORT} (clientId={CLIENT_ID}) ...")
    ib.connect(HOST, PORT, clientId=CLIENT_ID, timeout=5)
    assert ib.isConnected(), "Could not connect to TWS — check TWS is open and API enabled."

    # 1) Contract
    contract = Stock(symbol, "SMART", "USD")
    contract = ib.qualifyContracts(contract)[0]

    # 2) Historical bars (delayed if you don’t have real-time data perms)
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='5 mins',
        whatToShow='TRADES',
        useRTH=False,
        formatDate=1
    )
    last = float(bars[-1].close)
    log.info(f"{symbol} last close (5m bar): {last:.2f}")

    # 3) Simple bracket plan
    qty   = 10                       # demo size
    entry = last                     # market entry reference
    tp    = round(entry * 1.02, 2)   # +2% take profit
    sl    = round(entry * 0.99, 2)   # -1% stop loss

    parent, takeProfit, stopLoss = ib.bracketOrder(
        action="BUY", quantity=qty, limitPrice=None,
        takeProfitPrice=tp, stopLossPrice=sl
    )
    log.info(f"[{'DRY' if DRY_RUN else 'LIVE-PAPER'}] BUY {qty} {symbol} @mkt  TP={tp}  SL={sl}")

    if not DRY_RUN:
        # Place the three legs (parent transmits first; children linked)
        ib.placeOrder(contract, parent)
        ib.placeOrder(contract, takeProfit)
        ib.placeOrder(contract, stopLoss)
        log.info("Bracket submitted. Check TWS → Orders/Trades.")

    ib.disconnect()

if __name__ == "__main__":
    main("AMD")
