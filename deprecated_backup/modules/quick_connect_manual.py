from ib_insync import IB, util
util.logToFile('ibkr_api.log')  # writes a local debug log
ib = IB()
print("Connecting…")
try:
    ib.connect('127.0.0.1', 4002, clientId=1001, timeout=20)
    print("Connected:", ib.isConnected())
    print("Server time:", ib.reqCurrentTime())
    print("Acct summary (first 5):", ib.accountSummary()[:5])
except Exception as e:
    print(f"API connection failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    ib.disconnect()
