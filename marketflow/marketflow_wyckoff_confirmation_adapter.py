"""
Marketflow Wyckoff Confirmation Adapter
--------------------------------------
Adds conservative confirmation and scoring to events created by
`marketflow_wyckoff.WyckoffAnalyzer.annotate_chart()`.

Drop this file into your `marketflow/` package and import the adapter
from the Facade right after you call `WyckoffAnalyzer().annotate_chart()`.

Output:
- Enriched annotated DataFrame with columns:
  * wyckoff_confirmed_event (str; pipe-separated labels added or re-tagged)
  * wyckoff_confidence (float; 0..1 per bar for the most material event)
  * wyckoff_reasons (str; semicolon-joined rationale)
  * tr_low, tr_high (floats; detected TR for the timeframe)
- A compact list of high-confidence events you can store at `timeframe_analyses[tf]['wyckoff_confirmed_events']`

The adapter is self-contained (no external imports from the CLI tool),
but mirrors its logic and thresholds so you can keep one mental model.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import pandas as pd
import numpy as np

# ------------------------------
# Config (mirrors CLI tool defaults)
# ------------------------------
@dataclass
class ConfirmCfg:
    tr_lookback: int = 120
    tr_min_touches: int = 3
    touch_tolerance: float = 0.0025

    spring_undercut_min: float = 0.005
    spring_undercut_max: float = 0.030
    ut_overshoot_min: float = 0.005
    ut_overshoot_max: float = 0.030

    vol_lower_than_prev_n: int = 2
    vol_rel_threshold: float = 0.8
    spread_narrow_vs_ma: float = 0.85

    ndns_vol_rel_max: float = 0.9
    ndns_lower_than_prev_n: int = 2

    mta_align_required: bool = False  # Facade often lacks higher-TF context at this stage
    atr_regime_max_pct: float = 0.08
    loc_quartile_max_for_spring: float = 0.25
    loc_quartile_min_for_ut: float = 0.75

    pass_threshold: float = 0.45

    # higher-TF gate
    use_higher_tf_gate: bool = True
    gate_lookback_bars: int = 40
    gate_require_alignment: bool = True  # if True, we can downgrade to *_WEAK


# ------------------------------
# Small helpers
# ------------------------------

def _require_cols(df: pd.DataFrame):
    need = {"open","high","low","close","volume"}
    missing = need - set(df.columns)
    if missing:
        raise ValueError(f"annotated_df must contain {need}, missing {missing}")


def _prep_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["spread"] = out["high"] - out["low"]
    out["body"] = (out["close"] - out["open"]).abs()
    high_prev_close = (out["high"] - out["close"].shift()).abs()
    low_prev_close = (out["low"] - out["close"].shift()).abs()
    out["tr"] = np.maximum(out["high"] - out["low"], np.maximum(high_prev_close, low_prev_close))
    out["atr14"] = out["tr"].rolling(14).mean()
    out["volma20"] = out["volume"].rolling(20).mean()
    out["volrel20"] = out["volume"] / (out["volma20"] + 1e-9)
    out["spreadma20"] = out["spread"].rolling(20).mean()
    return out


def _detect_tr(df: pd.DataFrame, cfg: ConfirmCfg) -> Tuple[float,float]:
    window = df.tail(cfg.tr_lookback)
    highs = window["high"]; lows = window["low"]
    hi = highs.max(); lo = lows.min()
    upper = np.quantile(highs, 0.95) if len(highs) >= 10 else hi
    lower = np.quantile(lows, 0.05) if len(lows) >= 10 else lo
    tol_u = upper * cfg.touch_tolerance; tol_l = lower * cfg.touch_tolerance
    t_hi = ((highs >= upper - tol_u) | (window["close"] >= upper - tol_u)).sum()
    t_lo = ((lows <= lower + tol_l) | (window["close"] <= lower + tol_l)).sum()
    if t_hi >= cfg.tr_min_touches and t_lo >= cfg.tr_min_touches:
        return float(lower), float(upper)
    return float(lo), float(hi)


def _q(price: float, lo: float, hi: float) -> float:
    if hi <= lo: return 0.5
    return (price - lo) / (hi - lo)

# ------------------------------
# Event logic (mirrors the tool)
# ------------------------------

def _is_no_demand(row, prev, cfg: ConfirmCfg) -> bool:
    upbar = row.close > row.open
    narrow = row.spread < (row.spreadma20 * cfg.spread_narrow_vs_ma)
    vol_ok = row.volume < row.volma20 * cfg.ndns_vol_rel_max
    vol_lower_prev = all(row.volume < prev.iloc[-i].volume for i in range(1, cfg.ndns_lower_than_prev_n+1)) if len(prev) >= cfg.ndns_lower_than_prev_n+1 else False
    close_pos_midlow = row.close <= (row.low + 0.6 * (row.high - row.low))
    return bool(upbar and narrow and vol_ok and vol_lower_prev and close_pos_midlow)


def _is_no_supply(row, prev, cfg: ConfirmCfg) -> bool:
    downbar = row.close < row.open
    narrow = row.spread < (row.spreadma20 * cfg.spread_narrow_vs_ma)
    vol_ok = row.volume < row.volma20 * cfg.ndns_vol_rel_max
    vol_lower_prev = all(row.volume < prev.iloc[-i].volume for i in range(1, cfg.ndns_lower_than_prev_n+1)) if len(prev) >= cfg.ndns_lower_than_prev_n+1 else False
    close_pos_midhigh = row.close >= (row.low + 0.4 * (row.high - row.low))
    return bool(downbar and narrow and vol_ok and vol_lower_prev and close_pos_midhigh)


def _is_spring(row, lo: float, cfg: ConfirmCfg) -> bool:
    if lo <= 0: return False
    undercut = (lo - row.low) / lo
    closes_back = row.close > lo
    return bool((cfg.spring_undercut_min <= undercut <= cfg.spring_undercut_max) and closes_back)


def _is_ut(row, hi: float, cfg: ConfirmCfg) -> bool:
    if hi <= 0: return False
    overshoot = (row.high - hi) / hi
    closes_back = row.close < hi
    return bool((cfg.ut_overshoot_min <= overshoot <= cfg.ut_overshoot_max) and closes_back)


def _is_test_bar(row, prev, cfg: ConfirmCfg) -> bool:
    vol_ok = (row.volume < row.volma20 * cfg.vol_rel_threshold)
    if len(prev) >= cfg.vol_lower_than_prev_n+1:
        vol_ok = vol_ok and all(row.volume < prev.iloc[-i].volume for i in range(1, cfg.vol_lower_than_prev_n+1))
    narrow = row.spread < (row.spreadma20 * cfg.spread_narrow_vs_ma)
    return bool(vol_ok and narrow)


def _er_support(prev: pd.DataFrame, direction: str) -> bool:
    if len(prev) < 3: return False
    last = prev.iloc[-1]
    vol_up = last.volume > prev.volume.rolling(10).mean().iloc[-1]
    if direction == "up":
        result_poor = (last.close - prev.iloc[-2].close) <= 0
    else:
        result_poor = (last.close - prev.iloc[-2].close) >= 0
    return bool(vol_up and result_poor)

# ------------------------------
# Scoring
# ------------------------------

def _vol_penalty(row, cfg: ConfirmCfg) -> float:
    atr_ratio = (row.atr14 / max(row.close, 1e-9)) if pd.notna(row.atr14) else 0.0
    return 0.5 if atr_ratio > cfg.atr_regime_max_pct else 1.0


def _location_gate(row, lo, hi, kind: str, cfg: ConfirmCfg) -> bool:
    qv = _q(row.close, lo, hi)
    if kind == "spring":
        return qv <= cfg.loc_quartile_max_for_spring
    if kind == "ut":
        return qv >= cfg.loc_quartile_min_for_ut
    return True


def _score_event(kind: str, df: pd.DataFrame, i: int, lo: float, hi: float, cfg: ConfirmCfg) -> Tuple[float, List[str]]:
    row = df.iloc[i]
    prev = df.iloc[max(0, i-20):i+1]
    reasons = []
    score = 0.0

    # 1) Location gate
    if not _location_gate(row, lo, hi, kind, cfg):
        reasons.append("location gate failed")
        return 0.2, reasons
    reasons.append("location ok")
    score += 0.2

    # 2) Test bar logic (if this bar is narrow/low vol)
    if _is_test_bar(row, prev, cfg):
        reasons.append("narrow + low-vol test")
        score += 0.25

    # 3) Effort/Result divergence
    direction = "up" if kind == "spring" else "down"
    if _er_support(prev, direction):
        reasons.append("effort/result divergence supportive")
        score += 0.2

    # 4) Volatility penalty
    pen = _vol_penalty(row, cfg)
    if pen < 1.0:
        reasons.append("high ATR regime (downweighted)")
    score *= pen

    return max(min(score,1.0),0.0), reasons

# ------------------------------
# Public adapter
# ------------------------------
class WyckoffConfirmationAdapter:
    def __init__(self, cfg: Optional[ConfirmCfg]=None):
        self.cfg = cfg or ConfirmCfg()

    def score_annotated(self, annotated_df: pd.DataFrame, higher_tf_state: Optional[Dict]=None) -> Tuple[pd.DataFrame, List[Dict]]:

        """Return (enriched_df, confirmed_events_list)."""
        _require_cols(annotated_df)
        df = _prep_df(annotated_df)
        lo, hi = _detect_tr(df, self.cfg)

        df["tr_low"], df["tr_high"] = lo, hi
        df["wyckoff_confirmed_event"] = ""
        df["wyckoff_confidence"] = np.nan
        df["wyckoff_reasons"] = ""

        # Parse existing events per row
        def _parse_events(val: str) -> List[str]:
            if not isinstance(val, str) or not val.strip():
                return []
            return [s.strip().upper() for s in val.split(',') if s.strip()]

        confirmed: List[Dict] = []
        for i in range(len(df)):
            row = df.iloc[i]
            prev = df.iloc[max(0, i-20):i+1]
            existing = _parse_events(annotated_df.loc[row.name, "wyckoff_event"]) if "wyckoff_event" in annotated_df.columns else []

            best_label = None; best_score = 0.0; best_reasons: List[str] = []

            # If the analyzer already flagged SPRING/UTAD/UT, score them conservatively
            if any(e in ("SPRING","SPRING_TEST") for e in existing) or _is_spring(row, lo, self.cfg):
                s, rs = _score_event("spring", df, i, lo, hi, self.cfg)
                if s > best_score:
                    best_label, best_score, best_reasons = ("SPRING_CONFIRMED" if s>=self.cfg.pass_threshold else "SPRING_WEAK"), s, rs

            if any(e in ("UTAD","UT") for e in existing) or _is_ut(row, hi, self.cfg):
                s, rs = _score_event("ut", df, i, lo, hi, self.cfg)
                if s > best_score:
                    best_label, best_score, best_reasons = ("UT_CONFIRMED" if s>=self.cfg.pass_threshold else "UT_WEAK"), s, rs

            # Opportunistically tag ND/NS if present
            if _is_no_demand(row, prev, self.cfg):
                if best_score < 0.5:
                    best_label, best_score, best_reasons = "NO_DEMAND", 0.5, ["narrow up, vol<avg & <prev2, close mid/low"]
            if _is_no_supply(row, prev, self.cfg):
                if best_score < 0.5:
                    best_label, best_score, best_reasons = "NO_SUPPLY", 0.5, ["narrow down, vol<avg & <prev2, close mid/high"]

            if best_label:
                df.at[row.name, "wyckoff_confirmed_event"] = best_label
                df.at[row.name, "wyckoff_confidence"] = round(float(best_score), 3)
                df.at[row.name, "wyckoff_reasons"] = "; ".join(best_reasons)
                if best_score >= self.cfg.pass_threshold:
                    confirmed.append({
                        "timestamp": row.name,
                        "label": best_label,
                        "price": float(row.close),
                        "confidence": float(best_score),
                        "reasons": best_reasons,
                        "tr_low": lo,
                        "tr_high": hi,
                    })

            # ---- higher-TF gate (optional) ----
            if self.cfg.use_higher_tf_gate and higher_tf_state and best_label:
                # normalize flags we care about
                near_lower = bool(higher_tf_state.get("near_lower", False))
                near_upper = bool(higher_tf_state.get("near_upper", False))
                trend     = str(higher_tf_state.get("trend", "flat"))
                sow_recent = bool(higher_tf_state.get("sow_recent", False))
                sos_recent = bool(higher_tf_state.get("sos_recent", False))

                boosted = False
                headwind = False

                if "SPRING" in best_label:
                    # Supportive if higher TF is near lower quartile, not clearly down with SOW
                    if near_lower and not sow_recent:
                        best_score = min(1.0, best_score + 0.15); boosted = True
                    elif trend == "down" and sow_recent:
                        best_score = max(0.0, best_score - 0.15); headwind = True

                elif "UT" in best_label:
                    # Supportive if higher TF is near upper quartile, not clearly up with SOS
                    if near_upper and not sos_recent:
                        best_score = min(1.0, best_score + 0.15); boosted = True
                    elif trend == "up" and sos_recent:
                        best_score = max(0.0, best_score - 0.15); headwind = True

                # annotate reasons and possibly downgrade/upgrade label vs threshold
                if boosted:
                    best_reasons.append("higher-TF supportive")
                if headwind:
                    best_reasons.append("higher-TF headwind")

                if self.cfg.gate_require_alignment:
                    passed = (best_score >= self.cfg.pass_threshold)
                    if "SPRING" in (best_label or ""):
                        best_label = "SPRING_CONFIRMED" if passed else "SPRING_WEAK"
                    elif "UT" in (best_label or ""):
                        best_label = "UT_CONFIRMED" if passed else "UT_WEAK"


        return df, confirmed
    
            
