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
import numbers
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, List, Dict, Optional, Tuple
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
TARGET_RESOLVED = "TARGET_RESOLVED"
TARGET_NOT_AVAILABLE = "TARGET_NOT_AVAILABLE"
TARGET_INVALID = "TARGET_INVALID"
TARGET_SOURCE_AMBIGUOUS = "TARGET_SOURCE_AMBIGUOUS"
TARGET_SOURCE_UNSAFE = "TARGET_SOURCE_UNSAFE"
TARGET_PROVENANCE_WYCKOFF_TR_HIGH = "WYCKOFF_TR_HIGH"
RR_GATE_PASSED = "RR_GATE_PASSED"
RR_BELOW_MINIMUM = "RR_BELOW_MINIMUM"
RR_INVALID_INPUT = "RR_INVALID_INPUT"
VOLATILITY_RESOLVED = "VOLATILITY_RESOLVED"
VOLATILITY_NOT_AVAILABLE = "VOLATILITY_NOT_AVAILABLE"
VOLATILITY_INVALID = "VOLATILITY_INVALID"
VOLATILITY_SOURCE_UNSAFE = "VOLATILITY_SOURCE_UNSAFE"
VOLATILITY_PROVENANCE_TRUE_RANGE_SIMPLE_ROLLING = "TRUE_RANGE_SIMPLE_ROLLING"
EVENT_CURRENT = "EVENT_CURRENT"
EVENT_STALE = "EVENT_STALE"
EVENT_NOT_AVAILABLE = "EVENT_NOT_AVAILABLE"
EVENT_RECENCY_POLICY_NOT_CONFIGURED = "EVENT_RECENCY_POLICY_NOT_CONFIGURED"
EVENT_SUPERSEDED = "EVENT_SUPERSEDED"
EVENT_SOURCE_UNSAFE = "EVENT_SOURCE_UNSAFE"
EVENT_INVALID = "EVENT_INVALID"
EVENT_PROVENANCE_WYCKOFF_CONFIRMED_EVENT = "WYCKOFF_CONFIRMED_EVENT"
WYCKOFF_CONFIRMED_EVENT_COLUMN = "wyckoff_confirmed_event"
WYCKOFF_CONFIRMED_EVENT_OCCURRENCE_COLUMN = "wyckoff_confirmed_event_occurrence"
COMPONENT_PHASE = "phase"
COMPONENT_EVENT = "event"
COMPONENT_PNF = "pnf"
COMPONENT_POP = "pop"
COMPONENT_TREND = "trend"
EVIDENCE_AVAILABLE = "EVIDENCE_AVAILABLE"
EVIDENCE_DISABLED_BY_CONFIGURATION = "EVIDENCE_DISABLED_BY_CONFIGURATION"
EVIDENCE_NOT_AVAILABLE = "EVIDENCE_NOT_AVAILABLE"
EVIDENCE_INVALID = "EVIDENCE_INVALID"
EVIDENCE_SOURCE_UNSAFE = "EVIDENCE_SOURCE_UNSAFE"
EVIDENCE_NOT_APPLICABLE = "EVIDENCE_NOT_APPLICABLE"
SCORE_COMPLETE = "SCORE_COMPLETE"
SCORE_INCOMPLETE = "SCORE_INCOMPLETE"
SCORE_INVALID = "SCORE_INVALID"
SCORE_PROFILE_UNSAFE = "SCORE_PROFILE_UNSAFE"
SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED = "SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED"
EVIDENCE_COMPONENT_ORDER = (
    COMPONENT_PHASE,
    COMPONENT_EVENT,
    COMPONENT_PNF,
    COMPONENT_POP,
    COMPONENT_TREND,
)
REQUIRED_EVIDENCE_COMPONENTS = (
    COMPONENT_PHASE,
    COMPONENT_EVENT,
    COMPONENT_TREND,
)
COMPONENT_PROVENANCE_PHASE = "WYCKOFF_PHASE"
COMPONENT_PROVENANCE_EVENT_RESOLUTION = "WYCKOFF_EVENT_RESOLUTION"
COMPONENT_PROVENANCE_PNF_SCORE_COLUMN = "PNF_SCORE_COLUMN"
COMPONENT_PROVENANCE_MONTE_CARLO_POP = "MONTE_CARLO_POP"
COMPONENT_PROVENANCE_TREND_ROLLING_MEAN = "TREND_CLOSE_ROLLING_MEAN"
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
    max_event_age_bars: int | None = None

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


@dataclass(frozen=True)
class TargetResolution:
    status: str
    target_price: float | None = None
    provenance: str | None = None
    structural_level_kind: str | None = None
    source_row_index: int | None = None
    reason: str | None = None

    @property
    def success(self) -> bool:
        return self.status == TARGET_RESOLVED and self.target_price is not None


@dataclass(frozen=True)
class VolatilityResolution:
    status: str
    value: float | None = None
    provenance: str | None = None
    window: int | None = None
    reason: str | None = None

    @property
    def success(self) -> bool:
        return self.status == VOLATILITY_RESOLVED and self.value is not None


@dataclass(frozen=True)
class EventResolution:
    status: str
    event: str | None = None
    provenance: str | None = None
    occurrence_row_index: int | None = None
    occurrence_timestamp: str | None = None
    decision_row_index: int | None = None
    event_age_bars: int | None = None
    max_event_age_bars: int | None = None
    scoring_eligible: bool = False
    reason: str | None = None
    superseded_event_count: int = 0


@dataclass(frozen=True)
class EvidenceComponent:
    component: str
    status: str
    score: float | None
    configured_weight: float
    active_weight: float
    provenance: str | None
    reason: str | None = None
    expected_by_profile: bool = True
    scoring_eligible: bool = False


@dataclass(frozen=True)
class CompositeScoreResolution:
    status: str
    composite_score: float | None
    configured_weight_total: float
    active_weight_total: float
    available_weight_total: float
    evidence_coverage: float | None
    active_evidence_profile: str
    missing_components: tuple[str, ...] = ()
    disabled_components: tuple[str, ...] = ()
    invalid_components: tuple[str, ...] = ()
    reason: str | None = None


@dataclass(frozen=True)
class LongTradeLevelResolution:
    entry: float | None
    stop_loss: float | None
    target: TargetResolution
    rr: float | None
    rr_status: str
    eligible: bool
    reason: str | None = None
    volatility: VolatilityResolution | None = None

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

def _finite_float(value: object) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not pd.notna(numeric) or numeric in (float("inf"), float("-inf")):
        return None
    return numeric


def _positive_finite_float(value: object) -> float | None:
    numeric = _finite_float(value)
    if numeric is None or numeric <= 0:
        return None
    return numeric


def _single_numeric_column(df: pd.DataFrame, column: str) -> pd.Series | None:
    if column not in df.columns:
        return None
    if list(df.columns).count(column) != 1:
        return None
    series = pd.to_numeric(df[column], errors="coerce")
    if not bool(series.notna().all()):
        return None
    values = [float(value) for value in series.tolist()]
    if any(value in (float("inf"), float("-inf")) for value in values):
        return None
    return pd.Series(values, index=df.index, dtype="float64")


def _timestamp_chronology_is_safe(df: pd.DataFrame) -> bool:
    if "timestamp" not in df.columns:
        return True
    if list(df.columns).count("timestamp") != 1:
        return False
    timestamps = pd.to_datetime(df["timestamp"], errors="coerce")
    if not bool(timestamps.notna().all()):
        return False
    if bool(timestamps.duplicated().any()):
        return False
    return bool(timestamps.is_monotonic_increasing)


def _true_range(df: pd.DataFrame) -> pd.Series | None:
    high = _single_numeric_column(df, "high")
    low = _single_numeric_column(df, "low")
    close = _single_numeric_column(df, "close")
    if high is None or low is None or close is None:
        return None
    if bool((high < low).any()):
        return None

    previous_close = close.shift(1)
    if len(previous_close) > 1 and not bool(previous_close.iloc[1:].notna().all()):
        return None

    high_low = high - low
    high_previous_close = (high - previous_close).abs()
    low_previous_close = (low - previous_close).abs()
    true_range = pd.concat(
        [high_low, high_previous_close, low_previous_close],
        axis=1,
    ).max(axis=1, skipna=True)
    return pd.Series(true_range, index=df.index, dtype="float64")


def _resolve_volatility(df: pd.DataFrame, n: int = 14) -> VolatilityResolution:
    logger.debug(f"Resolving True Range volatility with window: {n}")
    numeric_window = _positive_finite_float(n)
    if numeric_window is None or numeric_window != int(numeric_window):
        return VolatilityResolution(
            status=VOLATILITY_INVALID,
            reason=VOLATILITY_INVALID,
            window=None,
        )
    window = int(numeric_window)
    if df.empty:
        return VolatilityResolution(
            status=VOLATILITY_NOT_AVAILABLE,
            reason=VOLATILITY_NOT_AVAILABLE,
            window=window,
        )
    for column in ("high", "low", "close"):
        if column not in df.columns:
            return VolatilityResolution(
                status=VOLATILITY_NOT_AVAILABLE,
                reason=VOLATILITY_NOT_AVAILABLE,
                window=window,
            )
        if list(df.columns).count(column) != 1:
            return VolatilityResolution(
                status=VOLATILITY_SOURCE_UNSAFE,
                reason=VOLATILITY_SOURCE_UNSAFE,
                window=window,
            )

    if not _timestamp_chronology_is_safe(df):
        return VolatilityResolution(
            status=VOLATILITY_SOURCE_UNSAFE,
            reason=VOLATILITY_SOURCE_UNSAFE,
            window=window,
        )

    true_range = _true_range(df)
    if true_range is None or true_range.empty:
        return VolatilityResolution(
            status=VOLATILITY_INVALID,
            reason=VOLATILITY_INVALID,
            window=window,
        )

    atr = true_range.rolling(window).mean().iloc[-1]
    result = float(atr) if pd.notna(atr) else float(true_range.iloc[-window:].mean())
    if _positive_finite_float(result) is None:
        return VolatilityResolution(
            status=VOLATILITY_INVALID,
            reason=VOLATILITY_INVALID,
            window=window,
        )
    logger.debug(f"True Range volatility result: {result}")
    return VolatilityResolution(
        status=VOLATILITY_RESOLVED,
        value=result,
        provenance=VOLATILITY_PROVENANCE_TRUE_RANGE_SIMPLE_ROLLING,
        window=window,
    )


def _atr(df: pd.DataFrame, n: int = 14) -> float | None:
    resolution = _resolve_volatility(df, n=n)
    return resolution.value


def _rr(close: float, sl: float, tp: float) -> float | None:
    logger.debug(f"Calculating RR: close={close}, sl={sl}, tp={tp}")
    entry = _positive_finite_float(close)
    stop = _positive_finite_float(sl)
    target = _positive_finite_float(tp)
    if entry is None or stop is None or target is None:
        logger.debug("RR input validation failed: non-finite or non-positive value")
        return None
    risk = entry - stop
    reward = target - entry
    if risk <= 0 or reward <= 0:
        logger.debug("RR input validation failed: invalid long risk/reward geometry")
        return None
    rr = reward / risk
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


def _event_text(value: Any) -> str | None:
    if value is None:
        return None
    try:
        missing = pd.isna(value)
    except (TypeError, ValueError):
        missing = False
    if isinstance(missing, bool) and missing:
        return None
    text = str(value).strip()
    return text or None


def _valid_event_age_policy(value: object) -> tuple[int | None, str | None]:
    if value is None:
        return None, None
    if isinstance(value, bool):
        return None, EVENT_INVALID
    if isinstance(value, numbers.Integral):
        age = int(value)
        if age >= 0:
            return age, None
    return None, EVENT_INVALID


def _explicit_occurrence_marker(value: Any) -> bool | None:
    if value is None:
        return False
    try:
        missing = pd.isna(value)
    except (TypeError, ValueError):
        missing = False
    if isinstance(missing, bool) and missing:
        return False
    if isinstance(value, bool) or (
        value.__class__.__module__ == "numpy" and value.__class__.__name__ == "bool"
    ):
        return bool(value)
    if isinstance(value, numbers.Integral) and not isinstance(value, bool):
        if int(value) in (0, 1):
            return bool(int(value))
        return None
    if isinstance(value, str):
        text = value.strip().lower()
        if not text:
            return False
        if text in {"true", "1"}:
            return True
        if text in {"false", "0"}:
            return False
    return None


def _timestamp_at_row(df: pd.DataFrame, row_index: int) -> str | None:
    if "timestamp" not in df.columns or list(df.columns).count("timestamp") != 1:
        return None
    if row_index < 0 or row_index >= len(df):
        return None
    value = df.iloc[row_index].get("timestamp")
    text = _event_text(value)
    return text


def _resolve_wyckoff_event(
    df: pd.DataFrame,
    max_event_age_bars: int | None = None,
    *,
    decision_row_index: int | None = None,
    event_column: str = WYCKOFF_CONFIRMED_EVENT_COLUMN,
    occurrence_column: str | None = None,
    provenance: str = EVENT_PROVENANCE_WYCKOFF_CONFIRMED_EVENT,
) -> EventResolution:
    logger.debug(
        f"Resolving Wyckoff event recency: column={event_column}, "
        f"max_event_age_bars={max_event_age_bars}, decision_row_index={decision_row_index}"
    )
    policy, policy_error = _valid_event_age_policy(max_event_age_bars)
    try:
        row_index = len(df) - 1 if decision_row_index is None else int(decision_row_index)
    except (TypeError, ValueError):
        return EventResolution(status=EVENT_INVALID, reason=EVENT_INVALID)
    if df.empty:
        return EventResolution(status=EVENT_NOT_AVAILABLE, reason=EVENT_NOT_AVAILABLE, max_event_age_bars=policy)
    if row_index < 0 or row_index >= len(df):
        return EventResolution(
            status=EVENT_SOURCE_UNSAFE,
            reason=EVENT_SOURCE_UNSAFE,
            decision_row_index=row_index,
            max_event_age_bars=policy,
        )
    if not _timestamp_chronology_is_safe(df.iloc[: row_index + 1]):
        return EventResolution(
            status=EVENT_SOURCE_UNSAFE,
            reason=EVENT_SOURCE_UNSAFE,
            decision_row_index=row_index,
            max_event_age_bars=policy,
        )
    if event_column not in df.columns:
        return EventResolution(
            status=EVENT_NOT_AVAILABLE,
            reason=EVENT_NOT_AVAILABLE,
            decision_row_index=row_index,
            max_event_age_bars=policy,
        )
    if list(df.columns).count(event_column) != 1:
        return EventResolution(
            status=EVENT_SOURCE_UNSAFE,
            reason=EVENT_SOURCE_UNSAFE,
            decision_row_index=row_index,
            max_event_age_bars=policy,
        )

    marker_column = occurrence_column
    if marker_column is None and WYCKOFF_CONFIRMED_EVENT_OCCURRENCE_COLUMN in df.columns:
        marker_column = WYCKOFF_CONFIRMED_EVENT_OCCURRENCE_COLUMN
    if marker_column is not None:
        if marker_column not in df.columns or list(df.columns).count(marker_column) != 1:
            return EventResolution(
                status=EVENT_SOURCE_UNSAFE,
                reason=EVENT_SOURCE_UNSAFE,
                decision_row_index=row_index,
                max_event_age_bars=policy,
            )

    occurrences: list[tuple[int, str]] = []
    series = df[event_column]
    previous_event: str | None = None
    for position in range(row_index + 1):
        event = _event_text(series.iloc[position])
        if marker_column is not None:
            marker = _explicit_occurrence_marker(df[marker_column].iloc[position])
            if marker is None:
                return EventResolution(
                    status=EVENT_SOURCE_UNSAFE,
                    reason=EVENT_SOURCE_UNSAFE,
                    decision_row_index=row_index,
                    max_event_age_bars=policy,
                )
            if marker and event is None:
                return EventResolution(
                    status=EVENT_SOURCE_UNSAFE,
                    reason=EVENT_SOURCE_UNSAFE,
                    decision_row_index=row_index,
                    max_event_age_bars=policy,
                )
            if marker and event is not None:
                occurrences.append((position, event))
            continue
        if event is not None:
            if previous_event == event:
                return EventResolution(
                    status=EVENT_SOURCE_UNSAFE,
                    reason=EVENT_SOURCE_UNSAFE,
                    decision_row_index=row_index,
                    max_event_age_bars=policy,
                )
            occurrences.append((position, event))
        previous_event = event

    if not occurrences:
        return EventResolution(
            status=EVENT_NOT_AVAILABLE,
            reason=EVENT_NOT_AVAILABLE,
            decision_row_index=row_index,
            max_event_age_bars=policy,
        )

    occurrence_row_index, event = occurrences[-1]
    age = row_index - occurrence_row_index
    if age < 0:
        return EventResolution(
            status=EVENT_SOURCE_UNSAFE,
            event=event,
            provenance=provenance,
            occurrence_row_index=occurrence_row_index,
            occurrence_timestamp=_timestamp_at_row(df, occurrence_row_index),
            decision_row_index=row_index,
            event_age_bars=age,
            max_event_age_bars=policy,
            reason=EVENT_SOURCE_UNSAFE,
            superseded_event_count=max(0, len(occurrences) - 1),
        )
    if policy_error is not None:
        return EventResolution(
            status=EVENT_INVALID,
            event=event,
            provenance=provenance,
            occurrence_row_index=occurrence_row_index,
            occurrence_timestamp=_timestamp_at_row(df, occurrence_row_index),
            decision_row_index=row_index,
            event_age_bars=age,
            max_event_age_bars=policy,
            reason=EVENT_INVALID,
            superseded_event_count=max(0, len(occurrences) - 1),
        )
    if age == 0:
        status = EVENT_CURRENT
    elif policy is None:
        status = EVENT_RECENCY_POLICY_NOT_CONFIGURED
    elif age <= policy:
        status = EVENT_CURRENT
    else:
        status = EVENT_STALE

    return EventResolution(
        status=status,
        event=event,
        provenance=provenance,
        occurrence_row_index=occurrence_row_index,
        occurrence_timestamp=_timestamp_at_row(df, occurrence_row_index),
        decision_row_index=row_index,
        event_age_bars=age,
        max_event_age_bars=policy,
        scoring_eligible=status == EVENT_CURRENT,
        reason=None if status == EVENT_CURRENT else status,
        superseded_event_count=max(0, len(occurrences) - 1),
    )


def _event_score_for_resolution(resolution: EventResolution) -> float:
    if resolution.status != EVENT_CURRENT or not resolution.scoring_eligible:
        return 0.0
    return _event_score(resolution.event or "")


def _pnf_score_neutral() -> float:
    logger.debug("Returning neutral P&F score (0.5)")
    # Neutral when P&F meta is not used yet
    return 0.5


def _component_weight(cfg: StrategyConfig, component: str) -> float | None:
    weight = _finite_float((cfg.weights or {}).get(component))
    if weight is None or weight < 0:
        return None
    return float(weight)


def _active_profile_components(cfg: StrategyConfig) -> tuple[str, ...]:
    components: list[str] = list(REQUIRED_EVIDENCE_COMPONENTS)
    if cfg.use_pnf:
        components.append(COMPONENT_PNF)
    if cfg.use_mc:
        components.append(COMPONENT_POP)
    return tuple(component for component in EVIDENCE_COMPONENT_ORDER if component in components)


def _component_result(
    *,
    component: str,
    status: str,
    score: float | None,
    configured_weight: float | None,
    active: bool,
    provenance: str | None,
    reason: str | None = None,
) -> EvidenceComponent:
    configured = 0.0 if configured_weight is None else float(configured_weight)
    active_weight = configured if active and configured_weight is not None else 0.0
    if configured_weight is None:
        return EvidenceComponent(
            component=component,
            status=EVIDENCE_INVALID,
            score=None,
            configured_weight=0.0,
            active_weight=0.0,
            provenance=None,
            reason=EVIDENCE_INVALID,
            expected_by_profile=active,
            scoring_eligible=False,
        )
    if status == EVIDENCE_AVAILABLE:
        parsed_score = _finite_float(score)
        if parsed_score is None or parsed_score < 0.0 or parsed_score > 1.0 or not provenance:
            return EvidenceComponent(
                component=component,
                status=EVIDENCE_INVALID,
                score=None,
                configured_weight=configured,
                active_weight=active_weight,
                provenance=None,
                reason=EVIDENCE_INVALID,
                expected_by_profile=active,
                scoring_eligible=False,
            )
        return EvidenceComponent(
            component=component,
            status=EVIDENCE_AVAILABLE,
            score=float(parsed_score),
            configured_weight=configured,
            active_weight=active_weight,
            provenance=provenance,
            reason=reason,
            expected_by_profile=active,
            scoring_eligible=active,
        )
    return EvidenceComponent(
        component=component,
        status=status,
        score=None,
        configured_weight=configured,
        active_weight=active_weight,
        provenance=None,
        reason=reason or status,
        expected_by_profile=active,
        scoring_eligible=False,
    )


def _score_column_value(df: pd.DataFrame, columns: tuple[str, ...]) -> tuple[Any, str | None, str | None]:
    if df.empty:
        return None, None, EVIDENCE_NOT_AVAILABLE
    existing = [column for column in columns if column in df.columns]
    if not existing:
        return None, None, EVIDENCE_NOT_AVAILABLE
    if len(existing) > 1:
        return None, None, EVIDENCE_SOURCE_UNSAFE
    column = existing[0]
    if list(df.columns).count(column) != 1:
        return None, None, EVIDENCE_SOURCE_UNSAFE
    value = df.iloc[-1].get(column)
    try:
        missing = pd.isna(value)
    except (TypeError, ValueError):
        missing = False
    if isinstance(missing, bool) and missing:
        return None, column, EVIDENCE_NOT_AVAILABLE
    return value, column, None


def _resolve_phase_component(ctx: dict[str, Any], cfg: StrategyConfig) -> EvidenceComponent:
    return _component_result(
        component=COMPONENT_PHASE,
        status=EVIDENCE_AVAILABLE,
        score=_phase_score(str(ctx.get("phase") or "UNKNOWN")),
        configured_weight=_component_weight(cfg, COMPONENT_PHASE),
        active=True,
        provenance=COMPONENT_PROVENANCE_PHASE,
    )


def _resolve_event_component(ctx: dict[str, Any], cfg: StrategyConfig) -> EvidenceComponent:
    resolution = ctx.get("event_resolution")
    if isinstance(resolution, EventResolution) and resolution.status == EVENT_INVALID:
        return _component_result(
            component=COMPONENT_EVENT,
            status=EVIDENCE_INVALID,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_EVENT),
            active=True,
            provenance=None,
            reason=EVENT_INVALID,
        )
    if isinstance(resolution, EventResolution) and resolution.status == EVENT_SOURCE_UNSAFE:
        return _component_result(
            component=COMPONENT_EVENT,
            status=EVIDENCE_SOURCE_UNSAFE,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_EVENT),
            active=True,
            provenance=None,
            reason=EVENT_SOURCE_UNSAFE,
        )
    if isinstance(resolution, EventResolution) and resolution.status != EVENT_CURRENT:
        return _component_result(
            component=COMPONENT_EVENT,
            status=EVIDENCE_NOT_AVAILABLE,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_EVENT),
            active=True,
            provenance=None,
            reason=resolution.status,
        )
    return _component_result(
        component=COMPONENT_EVENT,
        status=EVIDENCE_AVAILABLE,
        score=_event_score_for_resolution(resolution) if isinstance(resolution, EventResolution) else 0.0,
        configured_weight=_component_weight(cfg, COMPONENT_EVENT),
        active=True,
        provenance=COMPONENT_PROVENANCE_EVENT_RESOLUTION,
        reason=getattr(resolution, "status", None),
    )


def _resolve_pnf_component(df: pd.DataFrame, cfg: StrategyConfig) -> EvidenceComponent:
    active = bool(cfg.use_pnf)
    if not active:
        return _component_result(
            component=COMPONENT_PNF,
            status=EVIDENCE_DISABLED_BY_CONFIGURATION,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_PNF),
            active=False,
            provenance=None,
        )
    value, column, failure = _score_column_value(
        df,
        ("pnf_score", "point_and_figure_score"),
    )
    if failure == EVIDENCE_SOURCE_UNSAFE:
        return _component_result(
            component=COMPONENT_PNF,
            status=EVIDENCE_SOURCE_UNSAFE,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_PNF),
            active=True,
            provenance=None,
        )
    if failure == EVIDENCE_NOT_AVAILABLE:
        return _component_result(
            component=COMPONENT_PNF,
            status=EVIDENCE_NOT_AVAILABLE,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_PNF),
            active=True,
            provenance=None,
            reason=column or EVIDENCE_NOT_AVAILABLE,
        )
    return _component_result(
        component=COMPONENT_PNF,
        status=EVIDENCE_AVAILABLE,
        score=value,
        configured_weight=_component_weight(cfg, COMPONENT_PNF),
        active=True,
        provenance=COMPONENT_PROVENANCE_PNF_SCORE_COLUMN,
        reason=column,
    )


def _resolve_pop_component(pop: Any | None, cfg: StrategyConfig) -> EvidenceComponent:
    active = bool(cfg.use_mc)
    if not active:
        return _component_result(
            component=COMPONENT_POP,
            status=EVIDENCE_DISABLED_BY_CONFIGURATION,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_POP),
            active=False,
            provenance=None,
        )
    if pop is None:
        return _component_result(
            component=COMPONENT_POP,
            status=EVIDENCE_NOT_AVAILABLE,
            score=None,
            configured_weight=_component_weight(cfg, COMPONENT_POP),
            active=True,
            provenance=None,
        )
    return _component_result(
        component=COMPONENT_POP,
        status=EVIDENCE_AVAILABLE,
        score=pop,
        configured_weight=_component_weight(cfg, COMPONENT_POP),
        active=True,
        provenance=COMPONENT_PROVENANCE_MONTE_CARLO_POP,
    )


def _trend_score(trend: str) -> float:
    return 0.75 if trend == "up" else 0.5


def _resolve_trend_component(ctx: dict[str, Any], cfg: StrategyConfig) -> EvidenceComponent:
    return _component_result(
        component=COMPONENT_TREND,
        status=EVIDENCE_AVAILABLE,
        score=_trend_score(str(ctx.get("trend") or "flat")),
        configured_weight=_component_weight(cfg, COMPONENT_TREND),
        active=True,
        provenance=COMPONENT_PROVENANCE_TREND_ROLLING_MEAN,
    )


def _resolve_evidence_components(
    df: pd.DataFrame,
    cfg: StrategyConfig,
    *,
    pop: float | None,
    context: dict[str, Any] | None = None,
    decision_row_index: int | None = None,
) -> tuple[EvidenceComponent, ...]:
    ctx = context if context is not None else _extract_context(df, cfg, decision_row_index=decision_row_index)
    components = {
        COMPONENT_PHASE: _resolve_phase_component(ctx, cfg),
        COMPONENT_EVENT: _resolve_event_component(ctx, cfg),
        COMPONENT_PNF: _resolve_pnf_component(df, cfg),
        COMPONENT_POP: _resolve_pop_component(pop, cfg),
        COMPONENT_TREND: _resolve_trend_component(ctx, cfg),
    }
    return tuple(components[component] for component in EVIDENCE_COMPONENT_ORDER)


def _score_from_evidence(components: Iterable[EvidenceComponent]) -> CompositeScoreResolution:
    component_list = list(components)
    configured_weight_total = sum(component.configured_weight for component in component_list)
    active_components = [
        component
        for component in component_list
        if component.expected_by_profile
    ]
    disabled_components = tuple(
        component.component
        for component in component_list
        if component.status == EVIDENCE_DISABLED_BY_CONFIGURATION
    )
    missing_components = tuple(
        component.component
        for component in active_components
        if component.status == EVIDENCE_NOT_AVAILABLE
    )
    invalid_components = tuple(
        component.component
        for component in active_components
        if component.status in {EVIDENCE_INVALID, EVIDENCE_SOURCE_UNSAFE}
    )
    active_weight_total = sum(component.active_weight for component in active_components)
    available_components = [
        component for component in active_components if component.status == EVIDENCE_AVAILABLE
    ]
    available_weight_total = sum(component.active_weight for component in available_components)
    evidence_coverage = (
        available_weight_total / active_weight_total
        if active_weight_total > 0.0
        else None
    )
    active_evidence_profile = ",".join(component.component for component in active_components)
    if active_weight_total <= 0.0:
        return CompositeScoreResolution(
            status=SCORE_INVALID,
            composite_score=None,
            configured_weight_total=configured_weight_total,
            active_weight_total=active_weight_total,
            available_weight_total=available_weight_total,
            evidence_coverage=evidence_coverage,
            active_evidence_profile=active_evidence_profile,
            missing_components=missing_components,
            disabled_components=disabled_components,
            invalid_components=invalid_components,
            reason=SCORE_INVALID,
        )
    if missing_components or invalid_components:
        return CompositeScoreResolution(
            status=SCORE_INCOMPLETE,
            composite_score=None,
            configured_weight_total=configured_weight_total,
            active_weight_total=active_weight_total,
            available_weight_total=available_weight_total,
            evidence_coverage=evidence_coverage,
            active_evidence_profile=active_evidence_profile,
            missing_components=missing_components,
            disabled_components=disabled_components,
            invalid_components=invalid_components,
            reason=SCORE_INCOMPLETE,
        )
    numerator = sum(
        component.active_weight * float(component.score)
        for component in available_components
        if component.score is not None
    )
    return CompositeScoreResolution(
        status=SCORE_COMPLETE,
        composite_score=numerator / active_weight_total * 100.0,
        configured_weight_total=configured_weight_total,
        active_weight_total=active_weight_total,
        available_weight_total=available_weight_total,
        evidence_coverage=evidence_coverage,
        active_evidence_profile=active_evidence_profile,
        missing_components=missing_components,
        disabled_components=disabled_components,
        invalid_components=invalid_components,
    )


def _evidence_component_by_name(
    components: Iterable[EvidenceComponent],
    component_name: str,
) -> EvidenceComponent:
    for component in components:
        if component.component == component_name:
            return component
    return EvidenceComponent(
        component=component_name,
        status=EVIDENCE_INVALID,
        score=None,
        configured_weight=0.0,
        active_weight=0.0,
        provenance=None,
        reason=EVIDENCE_INVALID,
        expected_by_profile=False,
    )


def _evidence_public_fields(
    components: Iterable[EvidenceComponent],
    score_resolution: CompositeScoreResolution,
) -> dict[str, Any]:
    component_list = list(components)
    fields: dict[str, Any] = {
        "score_status": score_resolution.status,
        "score_reason": score_resolution.reason,
        "active_evidence_profile": score_resolution.active_evidence_profile,
        "configured_weight_total": score_resolution.configured_weight_total,
        "active_weight_total": score_resolution.active_weight_total,
        "available_weight_total": score_resolution.available_weight_total,
        "evidence_coverage": score_resolution.evidence_coverage,
        "missing_components": list(score_resolution.missing_components),
        "disabled_components": list(score_resolution.disabled_components),
        "invalid_components": list(score_resolution.invalid_components),
        "rank_eligible": (
            score_resolution.status == SCORE_COMPLETE
            and not score_resolution.disabled_components
        ),
        "score_profile_calibration": (
            SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED
            if score_resolution.disabled_components
            else None
        ),
    }
    for component in component_list:
        prefix = f"{component.component}_evidence"
        fields[f"{prefix}_status"] = component.status
        fields[f"{prefix}_score"] = component.score
        fields[f"{prefix}_configured_weight"] = component.configured_weight
        fields[f"{prefix}_active_weight"] = component.active_weight
        fields[f"{prefix}_provenance"] = component.provenance
        fields[f"{prefix}_reason"] = component.reason
        fields[f"{prefix}_expected_by_profile"] = component.expected_by_profile
        fields[f"{prefix}_scoring_eligible"] = component.scoring_eligible
    return fields


def _target_values_from_row(row: pd.Series) -> list[float | None]:
    target_columns = [column for column in row.index if str(column) == "tr_high" or re.fullmatch(r"tr_high\.\d+", str(column))]
    if not target_columns:
        return []
    values: list[float | None] = []
    for column in target_columns:
        value = row[column]
        if isinstance(value, pd.Series):
            values.extend(_finite_float(item) for item in value.tolist())
        else:
            values.append(_finite_float(value))
    return values


def _resolve_long_target(
    df: pd.DataFrame,
    *,
    entry: float,
    decision_row_index: int | None = None,
) -> TargetResolution:
    entry_value = _positive_finite_float(entry)
    if entry_value is None:
        return TargetResolution(status=TARGET_INVALID, reason=TARGET_INVALID)
    if df.empty:
        return TargetResolution(status=TARGET_NOT_AVAILABLE, reason=TARGET_NOT_AVAILABLE)

    row_index = len(df) - 1 if decision_row_index is None else int(decision_row_index)
    if row_index < 0 or row_index >= len(df):
        return TargetResolution(status=TARGET_SOURCE_UNSAFE, reason=TARGET_SOURCE_UNSAFE)

    decision_row = df.iloc[row_index]
    values = _target_values_from_row(decision_row)
    if not values:
        return TargetResolution(status=TARGET_NOT_AVAILABLE, reason=TARGET_NOT_AVAILABLE)
    if any(value is None for value in values):
        return TargetResolution(status=TARGET_INVALID, reason=TARGET_INVALID)

    unique_values = sorted(set(float(value) for value in values if value is not None))
    if len(unique_values) != 1:
        return TargetResolution(status=TARGET_SOURCE_AMBIGUOUS, reason=TARGET_SOURCE_AMBIGUOUS)

    target = unique_values[0]
    if target <= entry_value:
        return TargetResolution(status=TARGET_INVALID, reason=TARGET_INVALID)

    return TargetResolution(
        status=TARGET_RESOLVED,
        target_price=target,
        provenance=TARGET_PROVENANCE_WYCKOFF_TR_HIGH,
        structural_level_kind="resistance",
        source_row_index=row_index,
    )


def _valid_minimum_rr(value: object) -> float | None:
    numeric = _positive_finite_float(value)
    return numeric


def _resolve_long_trade_levels(
    df: pd.DataFrame,
    cfg: StrategyConfig,
    *,
    decision_row_index: int | None = None,
) -> LongTradeLevelResolution:
    logger.debug("Resolving long trade levels")
    min_rr = _valid_minimum_rr(cfg.min_rr)
    if min_rr is None:
        return LongTradeLevelResolution(
            entry=None,
            stop_loss=None,
            target=TargetResolution(status=TARGET_INVALID, reason=RR_INVALID_INPUT),
            rr=None,
            rr_status=RR_INVALID_INPUT,
            eligible=False,
            reason=RR_INVALID_INPUT,
            volatility=VolatilityResolution(status=VOLATILITY_NOT_AVAILABLE, reason=VOLATILITY_NOT_AVAILABLE),
        )
    if df.empty:
        return LongTradeLevelResolution(
            entry=None,
            stop_loss=None,
            target=TargetResolution(status=TARGET_NOT_AVAILABLE, reason=TARGET_NOT_AVAILABLE),
            rr=None,
            rr_status=TARGET_NOT_AVAILABLE,
            eligible=False,
            reason=TARGET_NOT_AVAILABLE,
            volatility=VolatilityResolution(status=VOLATILITY_NOT_AVAILABLE, reason=VOLATILITY_NOT_AVAILABLE),
        )
    row_index = len(df) - 1 if decision_row_index is None else int(decision_row_index)
    if row_index < 0 or row_index >= len(df):
        return LongTradeLevelResolution(
            entry=None,
            stop_loss=None,
            target=TargetResolution(status=TARGET_SOURCE_UNSAFE, reason=TARGET_SOURCE_UNSAFE),
            rr=None,
            rr_status=TARGET_SOURCE_UNSAFE,
            eligible=False,
            reason=TARGET_SOURCE_UNSAFE,
            volatility=VolatilityResolution(status=VOLATILITY_SOURCE_UNSAFE, reason=VOLATILITY_SOURCE_UNSAFE),
        )
    decision_frame = df.iloc[: row_index + 1]
    volatility = _resolve_volatility(decision_frame, n=cfg.atr_len)
    if not volatility.success:
        return LongTradeLevelResolution(
            entry=None,
            stop_loss=None,
            target=TargetResolution(status=TARGET_INVALID, reason=RR_INVALID_INPUT),
            rr=None,
            rr_status=volatility.status,
            eligible=False,
            reason=volatility.reason or volatility.status,
            volatility=volatility,
        )
    close = _positive_finite_float(decision_frame["close"].iloc[-1] if "close" in decision_frame.columns else None)
    if close is None:
        return LongTradeLevelResolution(
            entry=None,
            stop_loss=None,
            target=TargetResolution(status=TARGET_INVALID, reason=RR_INVALID_INPUT),
            rr=None,
            rr_status=RR_INVALID_INPUT,
            eligible=False,
            reason=RR_INVALID_INPUT,
            volatility=volatility,
        )
    atr = float(volatility.value)
    logger.debug(f"Close: {close}, ATR: {atr}")

    tr_low = None
    if "tr_low" in decision_frame.columns and pd.notna(decision_frame["tr_low"].iloc[-1]):
        tr_low = _positive_finite_float(decision_frame["tr_low"].iloc[-1])
        if tr_low is None:
            return LongTradeLevelResolution(
                entry=close,
                stop_loss=None,
                target=TargetResolution(status=TARGET_INVALID, reason=RR_INVALID_INPUT),
                rr=None,
                rr_status=RR_INVALID_INPUT,
                eligible=False,
                reason=RR_INVALID_INPUT,
                volatility=volatility,
            )
        logger.debug(f"tr_low found: {tr_low}")

    sl = max(tr_low or -1e12, close - cfg.max_sl_atr * atr)
    target = _resolve_long_target(df, entry=close, decision_row_index=row_index)
    if not target.success or target.target_price is None:
        return LongTradeLevelResolution(
            entry=close,
            stop_loss=sl,
            target=target,
            rr=None,
            rr_status=target.status,
            eligible=False,
            reason=target.reason or target.status,
            volatility=volatility,
        )

    rr = _rr(close, sl, target.target_price)
    if rr is None:
        return LongTradeLevelResolution(
            entry=close,
            stop_loss=sl,
            target=target,
            rr=None,
            rr_status=RR_INVALID_INPUT,
            eligible=False,
            reason=RR_INVALID_INPUT,
            volatility=volatility,
        )
    rr_status = RR_GATE_PASSED if rr >= min_rr else RR_BELOW_MINIMUM
    logger.debug(f"Resolved SL: {sl}, TP: {target.target_price}, RR: {rr}, status={rr_status}")
    return LongTradeLevelResolution(
        entry=close,
        stop_loss=sl,
        target=target,
        rr=rr,
        rr_status=rr_status,
        eligible=rr_status == RR_GATE_PASSED,
        reason=None if rr_status == RR_GATE_PASSED else rr_status,
        volatility=volatility,
    )


def _derive_sl_tp_long(df: pd.DataFrame, cfg: StrategyConfig) -> Tuple[float, float | None, float | None]:
    levels = _resolve_long_trade_levels(df, cfg)
    return levels.stop_loss, levels.target.target_price, levels.rr


def _extract_context(
    df: pd.DataFrame,
    cfg: StrategyConfig | None = None,
    *,
    decision_row_index: int | None = None,
) -> Dict[str, Any]:
    logger.debug("Extracting Wyckoff context")
    ctx: Dict[str, Any] = {}
    try:
        row_index = len(df) - 1 if decision_row_index is None else int(decision_row_index)
    except (TypeError, ValueError):
        row_index = len(df) - 1
    context_frame = df.iloc[: row_index + 1] if 0 <= row_index < len(df) else df
    phase = "UNKNOWN"
    if "wyckoff_phase" in context_frame.columns:
        nz = context_frame["wyckoff_phase"].dropna()
        if len(nz):
            phase = str(nz.iloc[-1])
    ctx["phase"] = phase
    logger.debug(f"Extracted phase: {phase}")

    cfg = cfg or StrategyConfig()
    event_resolution = _resolve_wyckoff_event(
        df,
        cfg.max_event_age_bars,
        decision_row_index=row_index,
    )
    ev = event_resolution.event or ""
    ctx["event"] = ev
    ctx["event_status"] = event_resolution.status
    ctx["event_provenance"] = event_resolution.provenance
    ctx["event_age_bars"] = event_resolution.event_age_bars
    ctx["event_max_age_bars"] = event_resolution.max_event_age_bars
    ctx["event_scoring_eligible"] = event_resolution.scoring_eligible
    ctx["event_occurrence_row_index"] = event_resolution.occurrence_row_index
    ctx["event_occurrence_timestamp"] = event_resolution.occurrence_timestamp
    ctx["event_decision_row_index"] = event_resolution.decision_row_index
    ctx["event_superseded_count"] = event_resolution.superseded_event_count
    ctx["event_reason"] = event_resolution.reason
    ctx["event_resolution"] = event_resolution
    logger.debug(f"Extracted event: {ev}; status={event_resolution.status}; age={event_resolution.event_age_bars}")

    # Simple direction/trend placeholder (can be replaced with your trend module)
    trend = "up" if context_frame["close"].iloc[-1] >= context_frame["close"].rolling(20).mean().iloc[-1] else "flat"
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
    - MC/P&F are optional by cfg; missing active evidence is incomplete, while
      explicitly disabled components are diagnostic and uncalibrated.
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

        # Resolve independent target before applying the RR eligibility gate.
        levels = _resolve_long_trade_levels(df, cfg)
        logger.info(
            f"Resolved SL/TP/RR for ticker {t}: SL={levels.stop_loss}, "
            f"TP={levels.target.target_price}, RR={levels.rr}, "
            f"target_status={levels.target.status}, rr_status={levels.rr_status}, "
            f"volatility_status={levels.volatility.status if levels.volatility else None}"
        )
        if not levels.eligible:
            logger.info(
                f"Long level resolution failed for ticker {t}: "
                f"{levels.reason or levels.rr_status}; skipping before scoring."
            )
            continue
        sl = float(levels.stop_loss)
        tp = float(levels.target.target_price)
        rr = float(levels.rr)

        # Extract Wyckoff context
        ctx = _extract_context(df, cfg, decision_row_index=len(df) - 1)
        logger.info(f"Extracted context for ticker {t}: {ctx}")
        if ctx["phase"] not in cfg.prefer_phases and ctx["phase"] != "UNKNOWN":
            # prefer phases C/D/E; allow UNKNOWN to pass (will be penalized by score)
            logger.info(f"Phase {ctx['phase']} not in preferred phases {cfg.prefer_phases} for ticker {t}, skipping.")
            continue

        # Optional: Monte Carlo POP
        pop: Any | None = None
        mc_meta: dict = {}
        if cfg.use_mc:
            mc, mc_meta = _latest_mc_with_metadata(out_dir, tf)
            logger.info(f"Monte Carlo summary for ticker {t}: {mc}")
            logger.info(f"Monte Carlo summary match metadata for ticker {t}: {mc_meta}")
            if mc and isinstance(mc, dict):
                metrics = mc.get("metrics_from_now", {})
                if isinstance(metrics, dict):
                    pop = metrics.get("pop_tp_first")
            # Apply gates only if we found a valid POP figure
            gate_pop = _finite_float(pop)
            if gate_pop is not None and 0.0 <= gate_pop <= 1.0 and (gate_pop < cfg.min_pop and gate_pop < cfg.min_pop_backup):
                logger.info(f"POP {gate_pop} below min_pop {cfg.min_pop} and min_pop_backup {cfg.min_pop_backup} for ticker {t}, skipping.")
                continue

        evidence_components = _resolve_evidence_components(df, cfg, pop=pop, context=ctx, decision_row_index=len(df) - 1)
        score_resolution = _score_from_evidence(evidence_components)
        phase_component = _evidence_component_by_name(evidence_components, COMPONENT_PHASE)
        event_component = _evidence_component_by_name(evidence_components, COMPONENT_EVENT)
        pnf_component = _evidence_component_by_name(evidence_components, COMPONENT_PNF)
        pop_component = _evidence_component_by_name(evidence_components, COMPONENT_POP)
        trend_component = _evidence_component_by_name(evidence_components, COMPONENT_TREND)
        score = score_resolution.composite_score

        logger.info(f"Final score for ticker {t}: {score}")

        result = {
            "ticker": source_identity.ticker,
            "tf": source_identity.timeframe,
            "csv": _source_reference(report_root, csv_path),
            "source_csv_name": csv_path.name,
            "source_report_dir": _source_reference(report_root, csv_path.parent),
            "source_status": source_resolution.status,
            "close": float(levels.entry),
            "sl": sl,
            "tp": tp,
            "rr": rr,
            "target_status": levels.target.status,
            "target_provenance": levels.target.provenance,
            "target_structural_level_kind": levels.target.structural_level_kind,
            "rr_status": levels.rr_status,
            "volatility_status": levels.volatility.status if levels.volatility else None,
            "volatility_provenance": levels.volatility.provenance if levels.volatility else None,
            "volatility_window": levels.volatility.window if levels.volatility else None,
            "volatility_value": levels.volatility.value if levels.volatility else None,
            "pop": pop_component.score,
            "pnf_score": pnf_component.score,
            "phase": ctx["phase"],
            "event": ctx["event"],
            "event_status": ctx["event_status"],
            "event_provenance": ctx["event_provenance"],
            "event_age_bars": ctx["event_age_bars"],
            "event_max_age_bars": ctx["event_max_age_bars"],
            "event_scoring_eligible": ctx["event_scoring_eligible"],
            "event_occurrence_row_index": ctx["event_occurrence_row_index"],
            "event_occurrence_timestamp": ctx["event_occurrence_timestamp"],
            "event_decision_row_index": ctx["event_decision_row_index"],
            "event_superseded_count": ctx["event_superseded_count"],
            "event_reason": ctx["event_reason"],
            "trend": ctx["trend"],
            "score": score,
            "composite_score": score,
        }
        result.update(_evidence_public_fields(evidence_components, score_resolution))
        if cfg.use_mc:
            result.update({
                "mc_summary_path": mc_meta.get("path"),
                "mc_matched_by": mc_meta.get("matched_by"),
                "mc_requested_tf": mc_meta.get("requested_tf"),
                "mc_matched_tf": mc_meta.get("matched_tf"),
            })
        results.append(result)

    results.sort(
        key=lambda r: (
            0 if r.get("score_status") == SCORE_COMPLETE else 1,
            -(float(r["score"]) if r.get("score") is not None else -1.0),
            str(r.get("ticker") or ""),
        )
    )
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
