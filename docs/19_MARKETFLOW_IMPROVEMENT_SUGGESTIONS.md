# Integrating ML Volatility Predictor into Monte Carlo Trading Simulator

Nice — I see the volatility_predictor.pkl. Let’s wire it into your MC engine cleanly so you can use model-predicted σ alongside (or blended with) realized σ.

Below is a drop-in patch for monte_carlo_trade_v2.py that:

loads your pickle (assumes it’s a scikit-learn pipeline or estimator),

computes a feature row from your OHLCV,

predicts per-bar σ (or converts from annualized if needed),

blends it with realized σ (safe clamps + fallbacks),

and uses it in GBM / GARCH (as the σ component).

1) CLI additions (place in your argparse section)

    ```bash
    p.add_argument("--vol-model", type=str, default=None,
                help="Path to volatility predictor .pkl (sklearn pipeline or estimator)")
    p.add_argument("--sigma-mode", type=str, default="blend",
                choices=["predicted", "blend", "realized"],
                help="Use model sigma, blended, or realized-only")
    p.add_argument("--sigma-blend", type=float, default=0.35,
                help="Blend weight w in sigma = w*pred + (1-w)*realized (0..1)")
    p.add_argument("--sigma-unit", type=str, default="per_bar",
                choices=["per_bar","annualized","per_sqrt_day"],
                help="Unit that the model predicts; will be converted to per-bar")
    ```

2) Helpers (add near your other utilities)

    ```bash
    import joblib
    import numpy as np
    import pandas as pd

    TF2BARS_PER_DAY = {"1d": 1, "4h": 6, "1h": 24, "30m": 48, "15m": 96, "5m": 288, "1m": 1440}
    TF_DEFAULT = "4h"
    ```

    ```python
        def compute_feature_row(df: pd.DataFrame, tf: str) -> np.ndarray:
            """
            Build a single feature row matching what your predictor expects.
            Adjust this to your training schema:
            - recent realized vol (various windows)
            - returns skew/kurt
            - ATR% and range%
            - volume z-score
            - rolling trend (EMA slopes) etc.
            """
            closes = df["close"].astype(float)
            highs  = df["high"].astype(float)
            lows   = df["low"].astype(float)
            vols   = df["volume"].astype(float)
            r = np.log(closes).diff().dropna()

            def rolled_std(x, n):
                return float(pd.Series(x).rolling(n).std(ddof=1).iloc[-1])

            def rolled_mean(x, n):
                return float(pd.Series(x).rolling(n).mean().iloc[-1])

            atr = (highs - lows)
            price = float(closes.iloc[-1])
            feat = [
                price,
                rolled_std(r, 20), rolled_std(r, 50), rolled_std(r, 100),
                rolled_mean(r, 20), rolled_mean(r, 50),
                float((highs.iloc[-1]-lows.iloc[-1]) / max(1e-9, price)),            # range%
                float(atr.rolling(14).mean().iloc[-1] / max(1e-9, price)),           # ATR%
                float((vols.iloc[-1] - vols.rolling(20).mean().iloc[-1]) / max(1e-9, vols.rolling(20).std(ddof=1).iloc[-1] or 1.0)),  # vol z
            ]
            X = np.array(feat, dtype=float).reshape(1, -1)
            return X
    ```

    ```python
        def load_vol_model(path: str):
            mdl = joblib.load(path)
            # Optional: attach metadata in pickle like mdl.version_ / mdl.unit_
            meta = {
                "version": getattr(mdl, "version_", "unknown"),
                "unit":    getattr(mdl, "unit_",    "per_bar"),
                "name":    mdl.__class__.__name__,
            }
            return mdl, meta

        def convert_sigma_to_per_bar(sig: float, tf: str, unit: str) -> float:
            """
            Convert model's sigma to per-bar log-return std for the given TF.
            unit: 'per_bar' (already per bar), 'per_sqrt_day' (per daily bar),
                'annualized' (per sqrt(year)).
            """
            if not np.isfinite(sig):
                return np.nan
            if unit == "per_bar":
                return float(sig)
            bars_per_day = TF2BARS_PER_DAY.get(tf, 6)  # default 4h: 6 bars/day
            if unit == "per_sqrt_day":
                return float(sig / np.sqrt(bars_per_day))
            if unit == "annualized":
                # 252 trading days/year
                return float(sig / np.sqrt(252 * bars_per_day))
            return float(sig)  # fallback

        def blend_sigma(pred_bar: float, realized_bar: float, mode: str, w: float) -> float:
            """
            Robust blend with sanity clamps and drift toward realized if model outlier.
            """
            # clamps (per-bar log std)
            CLIP_MIN, CLIP_MAX = 1e-5, 0.20
            # handle NaNs
            if not np.isfinite(pred_bar): pred_bar = realized_bar
            # outlier guard: if predicted is wildly off, reduce weight
            if realized_bar > 0:
                z = abs(pred_bar - realized_bar) / max(1e-9, realized_bar)
                if z > 2.0:
                    w = max(0.15, min(w, 0.25))  # dial down trust if big deviation
            if mode == "predicted":
                sig = pred_bar
            elif mode == "realized":
                sig = realized_bar
            else:
                sig = w * pred_bar + (1.0 - w) * realized_bar
            return float(np.clip(sig, CLIP_MIN, CLIP_MAX))
    ```

3) Integrate right where you calibrate μ, σ (inside your run function)

    Find where you currently compute mu_bar, sigma_bar, r = calibrate_per_bar(closes) and add the predicted σ logic:

    ```bash

            mu_bar, sigma_bar_realized, r = calibrate_per_bar(closes)
    ```

    --- Optional ML/GARCH volatility predictor ---

    ```bash
    pred_sigma_bar = None
    if args.vol_model:
        try:
            mdl, meta = load_vol_model(args.vol_model)
            X = compute_feature_row(df, tf or TF_DEFAULT)
            # If your pickle is a Pipeline, .predict() should be fine. Otherwise adapt.
            y = mdl.predict(X)
            # Some regressors emit shape (1,), others (1,1)
            y = float(np.ravel(y)[0])
            unit = meta.get("unit", args.sigma_unit)  # prefer model's unit_ if present
            pred_sigma_bar = convert_sigma_to_per_bar(y, tf or TF_DEFAULT, unit)
            logger.info(f"Vol model {meta['name']} v{meta['version']} → sigma_pred({unit})={y:.6f} → per_bar={pred_sigma_bar:.6f}")
        except Exception as e:
            logger.warning(f"Vol model failed, falling back to realized sigma. Error: {e}")

    # Blend per user choice
    sigma_bar = blend_sigma(pred_sigma_bar, sigma_bar_realized, args.sigma_mode, args.sigma_blend) \
                if args.vol_model else sigma_bar_realized
    ```

    Now feed sigma_bar into GBM (or use as the volatility component in your GARCH/ML-GBM path generator when appropriate).

4) Use the blended σ in your simulators

    * For GBM:

    paths_now   = simulate_gbm_paths(S0_now, mu_bar, sigma_bar, horizon_bars, n_paths, rng)
    paths_entry = simulate_gbm_paths(S0,     mu_bar, sigma_bar, horizon_bars, n_paths, rng)

    * For GARCH, you typically don’t override σ directly (you simulate a conditional σ path), but you can damp or
    scale innovations with the ratio (sigma_bar / sigma_bar_realized) if you want the forecast to steer the overall variance:

    scale = (sigma_bar / (sigma_bar_realized or sigma_bar))
    paths_now = simulate_garch_paths(..., rng)  # as patched
    paths_now[:,1:] = S0_now + (paths_now[:,1:] - S0_now) * scale

    * (That scaling is optional; only do it if you want your predictor to bias GARCH’s variance.)

5) Example runs

    Blend predicted with realized (default 35% weight), model outputs annualized σ:

    python monte_carlo_trade_v2.py ./PANW_4h.csv \
    --tp 206.54 --sl 192.7709 --entry 197.21 \
    --tf 4h --horizon 20 --model bootstrap --paths 20000 --block 8 \
    --vol-model volatility_predictor.pkl --sigma-mode blend --sigma-blend 0.35 \
    --sigma-unit annualized

    Use predicted only (per-bar model):

    python monte_carlo_trade_v2.py ./PANW_4h.csv \
    --tp 206.54 --sl 192.7709 --tf 4h --horizon 20 \
    --model gbm --paths 30000 \
    --vol-model volatility_predictor.pkl --sigma-mode predicted --sigma-unit per_bar

6) Sanity checks (do these once)

Log both sigma_bar_realized and pred_sigma_bar each run; ensure units are consistent and magnitudes reasonable (per-bar log σ for 4h will typically be ~0.005–0.03 for a name like PANW).

Quick POP stability: run with --sigma-mode realized vs --sigma-mode blend and confirm POP doesn’t swing wildly (>10–15 pts) unless the predictor is intentionally signaling a regime shift.

If the model is a Pipeline with a StandardScaler, you’re good; if not, make sure the feature engineering matches training (order/scale).

If you want, share a single predict(X) output (just the number and what unit you expect it in), and I’ll tell you exactly
what --sigma-unit and --sigma-blend settings make the most sense for your current model.

## Strategy: Wyckoff–P&F–POP Long Breakout

1) Universe & Prefilters (fast fail)

    Price ≥ $5, Avg daily $ volume ≥ $20M, ADR(20) ≥ 2%, spread ≤ 15 bps.

    Data completeness: ≥ 60 days history on 4h/1h; no missing OHLCV.

    (Optional later) Skip names with earnings or major events inside 5 trading days.

2) Scan & Rank (multi-TF)

    For each ticker (1D/4H/1H + P&F + MC):

    Wyckoff/VPA

    1D in Phase C/D or stepping advance (no clear distribution).

    4H shows absorption (shallow down bars, reduced volume on reactions).

    1H has SOS/JAC attempt (wide up bar on rising vol) or a clean test (narrow down on low vol).

    P&F (reversal=3)

    4H box ~0.5–0.8%, 1H box ~0.25–0.3%.

    Identify nearest DT breakout price B (e.g., 201.2).

    Small-box objective ≥ entry + 1.5R (conservative), and cluster around TP1 (not a single outlier count).

    No immediate upthrust in the last 2–3 columns.

    Monte Carlo (bootstrap, block 6–10) on 4H

    Horizon 20 bars; require POP(TP-first) ≥ 52%, P(SL-first) ≤ 28%, R̄ ≥ +0.15.

    If 45–52%, allow only on backup entry (see below).

    Composite score (0–100)

    POP (MC 4H) 30% weight (map 45–65% → 40–90 score).

    P&F readiness 25% (breakout proximity, no UT, objective ≥1.5R).

    VPA quality 25% (SOS/JAC or successful test).

    R/R to TP1 10% (≥2.0R gets full; <1.5R fails).

    Liquidity 10% (meets prefilters).
    Pick the top 1–2 tickers with score ≥ 70.

3) Entry (choose ONE of the two)

    A. Break-and-Hold (faster):
    1H close ≥ B and next 1–2 bars hold ≥ B − 0.5×box(1H) with hourly volume ≥ 1.2× its 20-bar avg → Enter.

    B. Jump → Backup (higher quality):
    Jump above B, then a light-volume pullback that holds B to B−1×box(1H); enter on the first wide up bar off that backup.

    Upthrust filter (always on): If after breaking B we print a 3-box O back below B within the next column → no entry (or cancel add); wait for a new setup.

4) Risk, Size, and Exits

    Account: $1,000 test. Risk per trade = 1% = $10.

    Stop (initial): lower of
    (i) 4H structural low (last O-column low − 0.5×box(4H)), or
    (ii) B − 3×box(1H) − tick.

    Size: shares = floor( $10 / (entry − stop) ), min 1 share; skip if size = 0.

    Take-profits

    TP1: nearest small-box P&F objective (or first resistance) with ≥2.0R; trim 50–66%.

    After TP1: move stop on remainder to breakeven; trail by 1H swing-low (or 3×box(1H)).

    Runner: only if the break shows easy progress and P&F next objective cluster is within 1–2 ATR.

    Time stops (discipline)

    4H: if +0.5R not reached within 5 bars, or +1R not reached within 10 bars, exit at market.

5) Go/No-Go Checklist (must all be TRUE)

    MC 4H: POP ≥ 52% (or 45–52% if using backup entry).

    P&F: no UT, objective ≥ 1.5R, breakout level B identified.

    VPA: SOS/JAC on 1H or successful test (narrow down on low vol).

    R/R to TP1 ≥ 2.0.

    Size ≥ 1 share at 1% risk.

6) What I need from you to run this scan

    For each candidate ticker:

    1D/4H/1H CSVs (last 90/60/60 days).

    P&F sidecars for 4H(0.5–0.8% box) and 1H(0.25–0.3% box).

    MC summary JSON (4H, 20 bars, bootstrap block 6–10).

    Drop them and I’ll return a ranked table with: Score, B (trigger), Stop, Entry type (A/B), Size, TP1/TP2, Time-stops, and the decision (Go/No-Go).

7) (Optional) Minimal code hooks you can add later

    utils/scoring.py

    score_mc(pop, psl, rbar) -> 0..100

    score_pnf(breakout_ok, ut_flag, obj_R) -> 0..100

    score_vpa(sos_jac, test_ok) -> 0..100

    composite(scores, weights) -> 0..100

    utils/position.py

    compute_stop(breakout, box1h, o_low_4h) -> stop

    position_size(entry, stop, risk_dollars=10) -> shares

    utils/checks.py

    upthrust_filter(pnf_columns, breakout) -> bool

    break_and_hold_ok(closes_1h, vols_1h, B, box1h) -> bool

    backup_ok(...) -> bool

    **Example (numbers you can reuse)**

    * Boxes: 4H 0.59–0.78%, 1H 0.25–0.30%; reversal = 3.

    * Hold band after break: B − 0.5×box(1H).

    * UT fail: 3 boxes back below B within 1 column.

    * MC horizon: 20 bars (4H), paths 20k, block 8.

## 1) target layout (lean)

```bash
/src
  /utils
    io.py           # load/sanitize OHLCV, timezone, dedupe
    pnf.py          # build P&F cols, breakouts, counts (your fixed code)
    mc.py           # MC runners (gbm, bootstrap, garch optional)
    scoring.py      # VPA/P&F/MC scores + composite
    position.py     # stop, size, R math, time-stops
    checks.py       # break&hold, backup, upthrust filter
  strategy.py       # Wyckoff–P&F–POP long breakout (glue)
  scan.py           # batch over tickers → ranked table + JSON
  decide.py         # prints final Go/No-Go + entry plan
/config
  strategy.yaml     # thresholds/weights
```

## 2) minimal interfaces (copy these signatures)

```python
# utils/io.py
def load_ohlcv(path: str, nrows: int|None=None, tz="Asia/Dubai"):
    ...

# utils/pnf.py
def pnf_features(df, box: float, reversal: int=3) -> dict:
    """return {"breakout":B, "objective":obj, "ut_flag":bool, "o_lows":[...], "x_highs":[...]}"""

# utils/mc.py
def mc_4h_pop(df_4h, tp: float, sl: float, horizon: int=20, paths: int=20000, block:int=8)->dict:
    """return {"pop":float, "p_sl":float, "rbar":float, "t_tp_med":int}"""

# utils/scoring.py
def score_mc(pop, p_sl, rbar) -> float: ...
def score_pnf(obj_R, ut_flag, near_break_ok) -> float: ...
def score_vpa(sos_jac: bool, test_ok: bool) -> float: ...
def composite(scores: dict, weights: dict) -> float: ...

# utils/position.py
def compute_stop(breakout: float, box1h: float, o_low_4h: float) -> float: ...
def position_size(entry: float, stop: float, acct: float=1000, risk_pct: float=0.01) -> int: ...

# utils/checks.py
def break_and_hold_ok(df_1h, B: float, box1h: float) -> bool: ...
def backup_ok(df_30m, B: float, box1h: float) -> bool: ...
def upthrust_after_break(pnf_cols, B: float) -> bool: ...
```

## 3) config you can tweak (strategy.yaml)

```yaml
risk:
  account: 1000
  risk_pct: 0.01

filters:
  min_price: 5
  min_dollar_vol: 2.0e7
  min_adr20: 0.02
  max_spread_bps: 15

pf:
  box_4h_pct: 0.006 # 0.6%
  box_1h_pct: 0.003 # 0.3%
  reversal: 3
  min_obj_R: 1.5

mc:
  horizon_bars: 20
  paths: 20000
  block: 8
  go_pop_min: 0.52
  backup_pop_min: 0.45
  max_p_sl: 0.28
  min_rbar: 0.15

weights:
  mc: 0.30
  pnf: 0.25
  vpa: 0.25
  rr: 0.10
  liq: 0.10
min_score: 70
```

## 4) scan → decide flow (CLI)

```bash
# scan a watchlist and rank
python -m src.scan --tickers AAAU,ACHR,... --out batch_rank.json

# print final plan for top candidates
python -m src.decide --rank batch_rank.json --top 2
```

## 5) decision logic (succinct)

Go if: filters pass AND score ≥ min_score AND obj_R ≥ 1.5 AND
(pop ≥ 0.52 OR (pop ≥ 0.45 AND entry_type == backup)).

Entry A (break&hold): need 1h close ≥ B AND next 1–2 bars hold ≥ B − 0.5×box1h, vol ≥ 1.2× 1h-20.

Entry B (jump→backup): jump above B, then low-vol pullback holding B..B−1×box1h, enter on wide up-bar.

Upthrust filter: 3-box O back below B shortly after break ⇒ no entry.

Stops/size: stop = min(4h O-low − 0.5×box4h, B − 3×box1h − tick); size = floor($risk / (entry−stop)).

TP1: nearest small-box objective with ≥2R; after TP1, stop to BE; trail by 1h swing-low.

## 6) quick tests (so you know it works)

Unit tests (pseudo):

P&F: given synthetic cols, ut_flag true when reversal ≥ 3 boxes under B.

MC: with zero σ, POP = 1 if S0 < TP and > SL; POP = 0 if S0 > SL and < TP.

Sizing: entry 100, stop 98, risk $10 ⇒ size = 5.

Smoke: run scan on 3–5 tickers; ensure ranks, triggers B, and sizes print; no exceptions.

## 7) refactor tips (keep it safe)

Keep I/O + plotting out of core utils; pass DataFrames in, dicts out.

Fix the RNG seed in MC for reproducible comparisons (seed=42).

Respect Asia/Dubai timezone in loaders; localize then convert if needed.

Log config + git hash in outputs so runs are traceable.

When you’re ready with a first prototype, toss me your strategy.yaml and one sample ticker bundle—I’ll do a pass on the scores, triggers, and edge cases before you run the full universe.
