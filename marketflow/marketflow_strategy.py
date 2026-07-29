r"""
Refactored strategy module — MC & PnF optional.

Usage examples:
1) After running batch analysis: 
   python MARKETFLOW/marketflow_strategy.py --report-root ./reports --batch latest --tf 1h --tickers AAPL MSFT NVDA

2) Directly against a date folder:
   python MARKETFLOW/marketflow_strategy.py --report-root ./reports --date-glob "2025-09-*" --tf 4h --tickers AAPL MSFT

3) for tf in 1h 4h 30m 1d 1w; do
  python marketflow_strategy_refactored.py ^
    --report-root ".marketflow/reports" --batch latest --tf(s) $tf --tickers AI ATRO DRS FLY KTOS RGR RKLB SPR TATT

Notes
- Does NOT require Monte Carlo (MC) or P&F files. When absent or disabled, it uses neutral defaults and ATR-based SL/TP.
- Compatible with the existing marketflow_batch_analysis.py output layout.
"""

from __future__ import annotations
import argparse, os, json, glob, re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd

from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger

logger = get_logger("MarketFlowStrategy")
app_cfg = create_app_config(logger=logger)

SUPPORTED_TIMEFRAME_TOKENS = ("1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m")
SOURCE_STATUS_EXACT_MATCH = "EXACT_MATCH"
SOURCE_REASON_DATASET_NOT_FOUND = "DATASET_NOT_FOUND"
SOURCE_REASON_DATASET_IDENTITY_AMBIGUOUS = "DATASET_IDENTITY_AMBIGUOUS"
SOURCE_REASON_INVALID_REQUEST = "INVALID_DATASET_REQUEST"
SOURCE_REASON_INVALID_SOURCE_ROOT = "INVALID_DATASET_SOURCE_ROOT"
_TICKER_PATTERN = re.compile(r"^[A-Z0-9._:-]+$")
_BATCH_RUN_PATTERN = re.compile(r"^batch_\d{8}_\d{6}$")

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


@dataclass(frozen=True)
class StrategyDatasetIdentity:
    ticker: str
    timeframe: str
    source: Path
    source_kind: str
    status: str = SOURCE_STATUS_EXACT_MATCH


@dataclass(frozen=True)
class StrategySourceResolution:
    requested_ticker: str | None
    requested_timeframe: str | None
    identity: StrategyDatasetIdentity | None
    status: str
    reason: str | None = None
    errors: tuple[str, ...] = ()

    @property
    def source(self) -> Path | None:
        return self.identity.source if self.identity else None

    @property
    def success(self) -> bool:
        return self.identity is not None and self.status == SOURCE_STATUS_EXACT_MATCH

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

def _normalize_tf(value: object) -> str | None:
    """Normalize a timeframe-like value for matching."""
    if value is None:
        return None
    clean = str(value).strip().lower()
    return clean or None


def _canonical_ticker(value: object) -> tuple[str | None, str | None]:
    """Return canonical ticker or a fixed validation reason."""
    if value is None:
        return None, SOURCE_REASON_INVALID_REQUEST
    text = str(value)
    if text != text.strip() or not text:
        return None, SOURCE_REASON_INVALID_REQUEST
    if any(ord(char) < 32 for char in text):
        return None, SOURCE_REASON_INVALID_REQUEST
    if "/" in text or "\\" in text:
        return None, SOURCE_REASON_INVALID_REQUEST
    canonical = text.upper()
    if not _TICKER_PATTERN.fullmatch(canonical):
        return None, SOURCE_REASON_INVALID_REQUEST
    return canonical, None


def _canonical_timeframe(value: object) -> tuple[str | None, str | None]:
    """Return canonical timeframe or a fixed validation reason."""
    if value is None:
        return None, SOURCE_REASON_INVALID_REQUEST
    text = str(value)
    if text != text.strip() or not text:
        return None, SOURCE_REASON_INVALID_REQUEST
    canonical = text.lower()
    if canonical not in SUPPORTED_TIMEFRAME_TOKENS:
        return None, SOURCE_REASON_INVALID_REQUEST
    return canonical, None


def _mc_json_timeframe(data: dict, field: str) -> str | None:
    """Read a top-level or params timeframe field from MC summary JSON."""
    value = data.get(field)
    if value is None and isinstance(data.get("params"), dict):
        value = data["params"].get(field)
    return _normalize_tf(value)


def _filename_matches_tf(path: str, tf: str | None) -> bool:
    """Return True when the MC filename contains the requested timeframe as a token."""
    clean_tf = _normalize_tf(tf)
    if not clean_tf:
        return False
    stem = os.path.splitext(os.path.basename(path))[0].lower()
    tokens = [token for token in re.split(r"[_\-.]+", stem) if token]
    return clean_tf in tokens


def _is_wyckoff_annotated_csv(path: str) -> bool:
    """Return True only for canonical Wyckoff annotated source CSV files."""
    return os.path.basename(path).lower().endswith("_wyckoff_annotated.csv")


def _is_generated_strategy_artifact_csv(path: str) -> bool:
    """Return True for generated CSV artifacts that should not feed Strategy Ranking."""
    filename = os.path.basename(path).lower()
    if not filename.endswith(".csv"):
        return False
    generated_markers = (
        "_pv_eigen.csv",
        "_backtest_candidates",
        "_backtest_results",
        "_eigen_review_summary",
        "_candidate_decision_summary",
        "_analyst_review_notes",
        "_walk_forward_cases_",
        "_walk_forward_results_",
        "_walk_forward_summary_",
    )
    return any(marker in filename for marker in generated_markers)


def _filename_tokens(path: str) -> list[str]:
    stem = os.path.splitext(os.path.basename(path))[0].lower()
    return [token for token in re.split(r"[_\-.]+", stem) if token]


def _parse_strategy_csv_identity(path: Path) -> StrategyDatasetIdentity | None:
    """Infer immutable dataset identity from a strategy source CSV filename."""
    if path.suffix.lower() != ".csv" or _is_generated_strategy_artifact_csv(str(path)):
        return None

    stem = path.stem
    lowered = stem.lower()
    source_kind = "canonical" if lowered.endswith("_wyckoff_annotated") else "raw"
    core = stem[: -len("_wyckoff_annotated")] if source_kind == "canonical" else stem
    parts = core.split("_")
    if len(parts) < 2:
        return None

    for index, part in enumerate(parts[1:], start=1):
        timeframe, timeframe_error = _canonical_timeframe(part)
        if timeframe_error is not None:
            continue
        ticker_text = "_".join(parts[:index])
        ticker, ticker_error = _canonical_ticker(ticker_text)
        if ticker_error is not None:
            return None
        return StrategyDatasetIdentity(
            ticker=ticker,
            timeframe=timeframe,
            source=path,
            source_kind=source_kind,
        )
    return None


def _csv_matches_timeframe(path: str, ticker: str, tf: str) -> bool:
    """Return True when filename tokens match the requested ticker and timeframe."""
    clean_ticker, ticker_error = _canonical_ticker(ticker)
    clean_tf, timeframe_error = _canonical_timeframe(tf)
    if ticker_error is not None or timeframe_error is not None:
        return False
    identity = _parse_strategy_csv_identity(Path(path))
    return bool(identity and identity.ticker == clean_ticker and identity.timeframe == clean_tf)


def _csv_matches_timeframe_any_ticker(path: str, tf: str) -> bool:
    clean_tf, timeframe_error = _canonical_timeframe(tf)
    if timeframe_error is not None:
        return False
    identity = _parse_strategy_csv_identity(Path(path))
    return bool(identity and identity.timeframe == clean_tf)


def _newest_csv(paths: list[str]) -> str:
    return sorted(
        paths,
        key=lambda path: (os.path.getmtime(path), os.path.basename(path).lower()),
        reverse=True,
    )[0]


def _path_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
        return True
    except (OSError, ValueError):
        return False


def _safe_date_glob(value: str | None) -> str | None:
    if value is None:
        return None
    text = str(value)
    path = Path(text)
    if path.is_absolute() or any(part == ".." for part in path.parts):
        return None
    return text


def _report_root_dirs(report_root: str, paths: Iterable[str]) -> list[str]:
    root = Path(report_root)
    return [
        str(path)
        for raw_path in paths
        for path in [Path(raw_path)]
        if path.is_dir() and _path_within_root(path, root)
    ]


def resolve_strategy_source_identity(out_dir: str, ticker: str, tf: str) -> StrategySourceResolution:
    """Resolve a Strategy Ranking source only when ticker and timeframe match exactly."""
    requested_ticker, ticker_error = _canonical_ticker(ticker)
    requested_timeframe, timeframe_error = _canonical_timeframe(tf)
    if ticker_error is not None or timeframe_error is not None:
        return StrategySourceResolution(
            requested_ticker=requested_ticker,
            requested_timeframe=requested_timeframe,
            identity=None,
            status=SOURCE_REASON_INVALID_REQUEST,
            reason=SOURCE_REASON_INVALID_REQUEST,
        )

    root = Path(out_dir)
    try:
        root_resolved = root.resolve(strict=True)
    except OSError:
        return StrategySourceResolution(
            requested_ticker=requested_ticker,
            requested_timeframe=requested_timeframe,
            identity=None,
            status=SOURCE_REASON_INVALID_SOURCE_ROOT,
            reason=SOURCE_REASON_INVALID_SOURCE_ROOT,
        )
    if not root_resolved.is_dir():
        return StrategySourceResolution(
            requested_ticker=requested_ticker,
            requested_timeframe=requested_timeframe,
            identity=None,
            status=SOURCE_REASON_INVALID_SOURCE_ROOT,
            reason=SOURCE_REASON_INVALID_SOURCE_ROOT,
        )

    try:
        csv_paths = [
            path
            for path in root.iterdir()
            if path.suffix.lower() == ".csv"
            and path.is_file()
            and _path_within_root(path, root_resolved)
        ]
    except Exception as e:
        logger.error(f"Error listing CSV files in {out_dir}: {e}")
        return StrategySourceResolution(
            requested_ticker=requested_ticker,
            requested_timeframe=requested_timeframe,
            identity=None,
            status=SOURCE_REASON_INVALID_SOURCE_ROOT,
            reason=SOURCE_REASON_INVALID_SOURCE_ROOT,
            errors=(type(e).__name__,),
        )

    logger.info(f"Found CSV candidates for ticker {ticker}: {sorted(str(path) for path in csv_paths)}")
    identities = [
        identity
        for path in csv_paths
        for identity in [_parse_strategy_csv_identity(path)]
        if identity
        and identity.ticker == requested_ticker
        and identity.timeframe == requested_timeframe
    ]
    if len(identities) == 1:
        return StrategySourceResolution(
            requested_ticker=requested_ticker,
            requested_timeframe=requested_timeframe,
            identity=identities[0],
            status=SOURCE_STATUS_EXACT_MATCH,
        )

    if len(identities) > 1:
        logger.warning(
            f"Ambiguous Strategy Ranking CSV identity for {requested_ticker} {requested_timeframe}; "
            "skipping candidate instead of selecting arbitrarily."
        )
        return StrategySourceResolution(
            requested_ticker=requested_ticker,
            requested_timeframe=requested_timeframe,
            identity=None,
            status=SOURCE_REASON_DATASET_IDENTITY_AMBIGUOUS,
            reason=SOURCE_REASON_DATASET_IDENTITY_AMBIGUOUS,
        )

    logger.warning(
        f"No exact Strategy Ranking CSV source found for {requested_ticker} {requested_timeframe} in {out_dir}."
    )
    return StrategySourceResolution(
        requested_ticker=requested_ticker,
        requested_timeframe=requested_timeframe,
        identity=None,
        status=SOURCE_REASON_DATASET_NOT_FOUND,
        reason=SOURCE_REASON_DATASET_NOT_FOUND,
    )


def _select_strategy_source_csv(out_dir: str, ticker: str, tf: str) -> Optional[str]:
    """Select an exact ticker/timeframe CSV source for Strategy Ranking."""
    resolution = resolve_strategy_source_identity(out_dir, ticker, tf)
    if resolution.success and resolution.source is not None:
        return str(resolution.source)
    return None


def _source_reference(report_root: str, source_path: Path) -> str:
    """Return a non-absolute source reference for normal candidate output."""
    try:
        return source_path.resolve(strict=True).relative_to(Path(report_root).resolve(strict=True)).as_posix()
    except (OSError, ValueError):
        return source_path.name


def _mc_metadata(
    tf: str | None,
    matched_by: str,
    available_count: int,
    candidate_paths: list[str],
    path: str | None = None,
    matched_tf: str | None = None,
) -> dict:
    """Build stable Monte Carlo matching metadata."""
    return {
        "requested_tf": tf,
        "matched_tf": matched_tf,
        "path": path,
        "matched_by": matched_by,
        "available_count": available_count,
        "candidate_paths": candidate_paths,
    }


def _latest_mc_with_metadata(dir_: str, tf: str | None = None) -> tuple[Optional[dict], dict]:
    """
    Load the newest Monte Carlo summary for the requested timeframe when possible.

    Prefer:
    1. MC summary whose JSON field `tf` matches requested tf
    2. MC summary whose JSON field `timeframe` matches requested tf
    3. MC summary whose filename contains requested tf as a token
    4. newest MC summary as fallback, but mark as fallback
    """
    requested_tf = _normalize_tf(tf)
    logger.debug(f"Loading timeframe-aware Monte Carlo summary from {dir_} for tf={requested_tf}")
    try:
        files = [
            os.path.join(dir_, filename)
            for filename in os.listdir(dir_)
            if filename.endswith("_mc_summary.json")
        ]
    except Exception as e:
        logger.error(f"Error listing MC summaries: {e}")
        meta = _mc_metadata(tf, "none", 0, [])
        return None, meta

    files.sort(key=lambda path: os.path.getmtime(path), reverse=True)
    candidate_paths = list(files)
    available_count = len(files)
    if not files:
        logger.debug("No MC summary file found.")
        meta = _mc_metadata(tf, "none", available_count, candidate_paths)
        return None, meta

    loaded: list[tuple[str, dict]] = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                loaded.append((path, data))
            else:
                logger.warning(f"Skipping non-object MC summary: {path}")
        except Exception as e:
            logger.error(f"Error loading MC summary {path}: {e}")

    if not loaded:
        meta = _mc_metadata(tf, "none", available_count, candidate_paths)
        return None, meta

    if requested_tf:
        for path, data in loaded:
            matched_tf = _mc_json_timeframe(data, "tf")
            if matched_tf == requested_tf:
                meta = _mc_metadata(tf, "json_tf", available_count, candidate_paths, path, matched_tf)
                return data, meta

        for path, data in loaded:
            matched_tf = _mc_json_timeframe(data, "timeframe")
            if matched_tf == requested_tf:
                meta = _mc_metadata(tf, "json_timeframe", available_count, candidate_paths, path, matched_tf)
                return data, meta

        for path, data in loaded:
            if _filename_matches_tf(path, requested_tf):
                meta = _mc_metadata(tf, "filename", available_count, candidate_paths, path, requested_tf)
                return data, meta

    path, data = loaded[0]
    matched_tf = _mc_json_timeframe(data, "tf") or _mc_json_timeframe(data, "timeframe")
    meta = _mc_metadata(tf, "fallback_latest", available_count, candidate_paths, path, matched_tf)
    return data, meta


def _latest_mc(dir_: str, tf: str | None = None) -> Optional[dict]:
    data, _meta = _latest_mc_with_metadata(dir_, tf)
    return data

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
    safe_date_glob = _safe_date_glob(date_glob)
    if date_glob and safe_date_glob is None:
        logger.warning(f"Unsafe Strategy Ranking date_glob rejected: {date_glob}")
        return results

    # Resolve batch folder if requested
    if use_batch_namespace == "latest":
        batch_dirs = _report_root_dirs(
            report_root,
            [
                str(path)
                for path in Path(report_root).glob("batch_*")
                if _BATCH_RUN_PATTERN.fullmatch(path.name)
            ],
        )
        logger.info(f"Found batch directories: {batch_dirs}")
        if batch_dirs:
            safe_date_glob = os.path.basename(sorted(batch_dirs)[-1])  # use latest batch_YYYYMMDD_HHMMSS
            date_glob = safe_date_glob
            logger.info(f"Using latest batch directory: {date_glob}")

    for t in tickers:
        logger.info(f"Processing ticker: {t}")
        source_ticker, ticker_error = _canonical_ticker(t)
        source_tf, timeframe_error = _canonical_timeframe(tf)
        if ticker_error is not None or timeframe_error is not None:
            logger.info(f"Invalid dataset request for ticker {t} timeframe {tf}; skipping.")
            continue

        # Possible layouts:
        #   report_root/date_glob/TICKER
        #   report_root/batch_YYYYMMDD_HHMMSS/TICKER
        dirs = (
            sorted(
                _report_root_dirs(
                    report_root,
                    glob.glob(os.path.join(report_root, safe_date_glob, source_ticker)),
                )
            )
            if safe_date_glob
            else []
        )
        if not dirs:
            # fallback: any folder directly under report_root matching ticker
            dirs = sorted(
                _report_root_dirs(
                    report_root,
                    glob.glob(os.path.join(report_root, "**", source_ticker), recursive=True),
                )
            )
        logger.info(f"Found directories for ticker {source_ticker}: {dirs}")
        if not dirs:
            logger.info(f"No directories found for ticker {source_ticker}, skipping.")
            continue
        out_dir = dirs[-1]
        logger.info(f"Using output directory for ticker {source_ticker}: {out_dir}")

        # Locate canonical source CSV for exact ticker/timeframe identity.
        source_resolution = resolve_strategy_source_identity(out_dir, source_ticker, source_tf)
        if not source_resolution.success or source_resolution.source is None or source_resolution.identity is None:
            logger.info(
                f"Dataset resolution failed for ticker {source_ticker} timeframe {source_tf}: "
                f"{source_resolution.reason or source_resolution.status}; skipping before scoring."
            )
            continue
        source_identity = source_resolution.identity
        csv_path = source_identity.source
        logger.info(f"Using CSV file for ticker {source_identity.ticker}: {csv_path}")

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
        mc_meta: dict = {}
        if cfg.use_mc:
            mc, mc_meta = _latest_mc_with_metadata(out_dir, tf)
            logger.info(f"Monte Carlo summary for ticker {t}: {mc}")
            logger.info(f"Monte Carlo summary match metadata for ticker {t}: {mc_meta}")
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

        result = {
            "ticker": source_identity.ticker,
            "tf": source_identity.timeframe,
            "csv": _source_reference(report_root, csv_path),
            "source_csv_name": csv_path.name,
            "source_report_dir": _source_reference(report_root, csv_path.parent),
            "source_status": source_resolution.status,
            "close": float(df["close"].iloc[-1]),
            "sl": sl, "tp": tp, "rr": _rr(float(df["close"].iloc[-1]), sl, tp),
            "pop": pop,
            "phase": ctx["phase"],
            "event": ctx["event"],
            "trend": ctx["trend"],
            "score": round(score, 2),
        }
        if cfg.use_mc:
            result.update({
                "mc_summary_path": mc_meta.get("path"),
                "mc_matched_by": mc_meta.get("matched_by"),
                "mc_requested_tf": mc_meta.get("requested_tf"),
                "mc_matched_tf": mc_meta.get("matched_tf"),
            })
        results.append(result)

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
