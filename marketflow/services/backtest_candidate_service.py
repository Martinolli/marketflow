"""Candidate snapshot normalization for future backtest calibration workflows."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.backtesting.schemas import CandidateSnapshot
from marketflow.marketflow_config_manager import create_app_config


VALIDATION_VALID = "valid"
VALIDATION_MISSING_LEVELS = "missing_levels"
VALIDATION_MISSING_SOURCE_CSV = "missing_source_csv"
VALIDATION_MISSING_SIGNAL_LOCATION = "missing_signal_location"
VALIDATION_INVALID_LEVELS = "invalid_levels"
VALIDATION_UNSUPPORTED_DIRECTION = "unsupported_direction"

SUPPORTED_DIRECTIONS = {"long"}
TIMEFRAME_TOKENS = ("15m", "30m", "1m", "5m", "1h", "4h", "1d", "1w")
TIMESTAMP_COLUMN_CANDIDATES = (
    "timestamp",
    "datetime",
    "date",
    "Date",
    "Datetime",
    "Timestamp",
    "time",
)

SNAPSHOT_FIELDS = [
    "ticker",
    "timeframe",
    "source_csv",
    "signal_timestamp",
    "signal_timestamp_source",
    "signal_row_index",
    "entry",
    "stop_loss",
    "take_profit",
    "risk_reward",
    "strategy_score",
    "wyckoff_phase",
    "wyckoff_event",
    "trend",
    "candidate_source",
    "report_date",
    "direction",
    "source_report_dir",
    "source_strategy_rank",
]


def _json_safe_value(value: Any) -> Any:
    """Return a scalar value suitable for JSON serialization."""

    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, ValueError, TypeError):
            pass
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    try:
        is_missing = pd.isna(value)
    except (TypeError, ValueError):
        is_missing = False
    if isinstance(is_missing, bool) and is_missing:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _is_missing(value: Any) -> bool:
    value = _json_safe_value(value)
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _to_float(value: Any) -> float | None:
    value = _json_safe_value(value)
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def _numbers_close(left: Any, right: Any, *, tolerance: float = 1e-6) -> bool:
    left_float = _to_float(left)
    right_float = _to_float(right)
    if left_float is None or right_float is None:
        return False
    return abs(left_float - right_float) <= tolerance


def _to_int(value: Any) -> int | None:
    value = _json_safe_value(value)
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed


def _infer_timeframe_from_text(text: str | None) -> str | None:
    if not text:
        return None
    name = Path(str(text)).name.lower()
    for token in TIMEFRAME_TOKENS:
        pattern = rf"(^|[_\-.]){re.escape(token)}([_\-.]|$)"
        if re.search(pattern, name):
            return token
    return None


def _infer_ticker_from_csv(path: str | Path | None) -> str | None:
    if path is None:
        return None
    stem = Path(str(path)).name
    if not stem:
        return None
    stem = Path(stem).stem
    if not stem:
        return None
    return stem.split("_", 1)[0].upper()


def _first_present(candidate: dict[str, Any], *keys: str) -> tuple[Any, str | None]:
    for key in keys:
        if key in candidate:
            value = _json_safe_value(candidate.get(key))
            if not _is_missing(value):
                return value, key
    return None, None


def _timestamp_column(dataframe: pd.DataFrame) -> str | None:
    for column in TIMESTAMP_COLUMN_CANDIDATES:
        if column in dataframe.columns:
            return column
    return None


def _candidate_source_path(path: str | Path | None, source_report_dir: str | Path | None = None) -> Path | None:
    if _is_missing(path):
        return None

    raw_path = Path(str(path))
    candidates: list[Path] = []
    report_root: Path | None = None
    try:
        report_root = Path(create_app_config().REPORT_DIR)
    except Exception:
        report_root = None

    if source_report_dir:
        report_dir_path = Path(str(source_report_dir))
        scoped_candidates = [report_dir_path / raw_path.name]
        if report_root is not None:
            scoped_candidates.append(report_root / report_dir_path / raw_path.name)
            scoped_candidates.append(report_root / raw_path)
        for candidate in scoped_candidates:
            try:
                if report_root is not None:
                    candidate.resolve(strict=True).relative_to(report_root.resolve(strict=True))
                if candidate.exists() and candidate.is_file():
                    return candidate
            except (OSError, ValueError):
                continue
        return None

    candidates.append(raw_path)

    if report_root is not None and not raw_path.is_absolute():
        candidates.append(report_root / raw_path)

    for candidate in candidates:
        try:
            if candidate.exists() and candidate.is_file():
                return candidate
        except OSError:
            continue
    return raw_path


def _read_source_csv(
    path: str | Path | None,
    source_report_dir: str | Path | None = None,
) -> tuple[pd.DataFrame | None, str | None]:
    if _is_missing(path):
        return None, "Missing source_csv."
    resolved_path = _candidate_source_path(path, source_report_dir)
    if resolved_path is None:
        return None, "Could not read source_csv: source not found inside report root."
    try:
        dataframe = pd.read_csv(Path(str(resolved_path)))
    except Exception as exc:  # pragma: no cover - exact pandas errors vary by platform/version.
        return None, f"Could not read source_csv: {exc}"
    return dataframe, None


def _row_timestamp(dataframe: pd.DataFrame, row_index: int) -> tuple[Any | None, str | None]:
    column = _timestamp_column(dataframe)
    if column is None:
        return None, None
    if row_index < 0 or row_index >= len(dataframe):
        return None, None
    return _json_safe_value(dataframe.iloc[row_index][column]), column


def _first_existing_column(dataframe: pd.DataFrame, *columns: str) -> str | None:
    for column in columns:
        if column in dataframe.columns:
            return column
    return None


def _text_matches(left: Any, right: Any) -> bool:
    if _is_missing(left) or _is_missing(right):
        return False
    return str(left).strip().lower() == str(right).strip().lower()


def _candidate_price(snapshot: dict[str, Any]) -> Any:
    return snapshot.get("entry") if not _is_missing(snapshot.get("entry")) else snapshot.get("close")


def _match_result(
    *,
    matched: bool,
    method: str | None = None,
    row_index: int | None = None,
    timestamp: Any | None = None,
    timestamp_source: str | None = None,
    confidence: str = "none",
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "matched": matched,
        "method": method,
        "row_index": row_index,
        "timestamp": _json_safe_value(timestamp),
        "timestamp_source": timestamp_source,
        "confidence": confidence,
        "warnings": warnings or [],
        "errors": errors or [],
    }


def _computed_risk_reward(entry: float | None, stop_loss: float | None, take_profit: float | None) -> float | None:
    if entry is None or stop_loss is None or take_profit is None:
        return None
    if not (stop_loss < entry < take_profit):
        return None
    risk = entry - stop_loss
    if risk == 0:
        return None
    return (take_profit - entry) / risk


def _locate_by_explicit_row_index(
    snapshot: dict[str, Any],
    dataframe: pd.DataFrame,
) -> dict[str, Any] | None:
    row_index = _to_int(snapshot.get("signal_row_index"))
    if row_index is None:
        return None
    if row_index < 0 or row_index >= len(dataframe):
        return _match_result(
            matched=False,
            warnings=[f"signal_row_index {row_index} is outside source CSV bounds."],
        )

    timestamp = snapshot.get("signal_timestamp")
    timestamp_source = snapshot.get("signal_timestamp_source")
    if _is_missing(timestamp):
        timestamp, timestamp_source = _row_timestamp(dataframe, row_index)

    return _match_result(
        matched=True,
        method="explicit_row_index",
        row_index=row_index,
        timestamp=timestamp,
        timestamp_source=timestamp_source,
        confidence="high",
    )


def _locate_by_explicit_timestamp(
    snapshot: dict[str, Any],
    dataframe: pd.DataFrame,
) -> dict[str, Any] | None:
    if _to_int(snapshot.get("signal_row_index")) is not None:
        return None
    timestamp = snapshot.get("signal_timestamp")
    if _is_missing(timestamp):
        return None

    column = _timestamp_column(dataframe)
    if column is None:
        return _match_result(
            matched=False,
            warnings=["signal_timestamp present but source CSV has no timestamp column."],
        )

    target = str(timestamp).strip()
    matches = [
        int(position)
        for position, value in enumerate(dataframe[column].tolist())
        if str(_json_safe_value(value) or "").strip() == target
    ]
    if len(matches) == 1:
        return _match_result(
            matched=True,
            method="explicit_timestamp",
            row_index=matches[0],
            timestamp=timestamp,
            timestamp_source=column,
            confidence="high",
        )
    if len(matches) > 1:
        return _match_result(
            matched=False,
            warnings=["ambiguous timestamp match in source CSV."],
        )
    return _match_result(
        matched=False,
        warnings=["signal_timestamp did not match source CSV timestamp values."],
    )


def _locate_by_latest_row_assumption(dataframe: pd.DataFrame) -> dict[str, Any]:
    row_index = len(dataframe) - 1
    timestamp, timestamp_source = _row_timestamp(dataframe, row_index)
    return _match_result(
        matched=True,
        method="latest_row_assumption",
        row_index=row_index,
        timestamp=timestamp,
        timestamp_source=timestamp_source,
        confidence="medium",
        warnings=["signal location inferred from latest source row assumption"],
    )


def _locate_by_recent_context_match(
    snapshot: dict[str, Any],
    dataframe: pd.DataFrame,
    *,
    max_recent_rows: int,
) -> dict[str, Any]:
    close_column = _first_existing_column(dataframe, "close", "Close")
    if close_column is None:
        return _match_result(
            matched=False,
            warnings=["recent context match skipped because source CSV has no close column."],
        )

    candidate_price = _candidate_price(snapshot)
    if _is_missing(candidate_price):
        return _match_result(
            matched=False,
            warnings=["recent context match skipped because candidate has no entry/close value."],
        )

    phase_column = _first_existing_column(dataframe, "phase", "wyckoff_phase")
    event_column = _first_existing_column(dataframe, "event", "wyckoff_event", "wyckoff_confirmed_event")
    trend_column = _first_existing_column(dataframe, "trend")
    context_checks = (
        ("wyckoff_phase", phase_column),
        ("wyckoff_event", event_column),
        ("trend", trend_column),
    )

    start = max(0, len(dataframe) - max(1, max_recent_rows))
    matches: list[int] = []
    matched_context_count = 0
    for row_index in range(start, len(dataframe)):
        row = dataframe.iloc[row_index]
        if not _numbers_close(candidate_price, row.get(close_column)):
            continue

        context_matches = 0
        context_failed = False
        for snapshot_key, column in context_checks:
            if column is None or _is_missing(snapshot.get(snapshot_key)):
                continue
            if not _text_matches(snapshot.get(snapshot_key), row.get(column)):
                context_failed = True
                break
            context_matches += 1
        if context_failed:
            continue

        matches.append(row_index)
        matched_context_count = max(matched_context_count, context_matches)

    if len(matches) == 1:
        timestamp, timestamp_source = _row_timestamp(dataframe, matches[0])
        return _match_result(
            matched=True,
            method="recent_context_match",
            row_index=matches[0],
            timestamp=timestamp,
            timestamp_source=timestamp_source,
            confidence="high" if matched_context_count else "medium",
        )
    if len(matches) > 1:
        return _match_result(
            matched=False,
            warnings=["ambiguous recent context match in source CSV."],
        )
    return _match_result(matched=False)


def locate_candidate_in_source_csv(
    snapshot: dict[str, Any],
    *,
    max_recent_rows: int = 20,
    latest_row_fallback: bool = True,
) -> dict[str, Any]:
    """Locate a candidate snapshot row in its source CSV without mutating the snapshot."""

    dataframe, read_error = _read_source_csv(snapshot.get("source_csv"), snapshot.get("source_report_dir"))
    if read_error is not None:
        return _match_result(matched=False, errors=[read_error])
    if dataframe is None or dataframe.empty:
        return _match_result(matched=False, errors=["source_csv is empty."])

    explicit_row_match = _locate_by_explicit_row_index(snapshot, dataframe)
    if explicit_row_match is not None:
        return explicit_row_match

    explicit_timestamp_match = _locate_by_explicit_timestamp(snapshot, dataframe)
    if explicit_timestamp_match is not None:
        return explicit_timestamp_match

    # rank_long_candidates reads each source CSV and builds candidate context from df.iloc[-1].
    # This fallback is therefore allowed, but it stays visible as a validation warning.
    if latest_row_fallback:
        return _locate_by_latest_row_assumption(dataframe)

    recent_match = _locate_by_recent_context_match(
        snapshot,
        dataframe,
        max_recent_rows=max_recent_rows,
    )
    return recent_match


def enrich_candidate_snapshot_signal_location(
    snapshot: dict[str, Any],
    *,
    max_recent_rows: int = 20,
    latest_row_fallback: bool = True,
) -> dict[str, Any]:
    """Return a copy of snapshot enriched with conservative signal location evidence."""

    enriched_snapshot = dict(snapshot)
    match = locate_candidate_in_source_csv(
        enriched_snapshot,
        max_recent_rows=max_recent_rows,
        latest_row_fallback=latest_row_fallback,
    )

    if match["matched"]:
        if match.get("row_index") is not None:
            enriched_snapshot["signal_row_index"] = match["row_index"]
        if not _is_missing(match.get("timestamp")) and _is_missing(enriched_snapshot.get("signal_timestamp")):
            enriched_snapshot["signal_timestamp"] = _json_safe_value(match.get("timestamp"))
        if not _is_missing(match.get("timestamp_source")) and (
            _is_missing(enriched_snapshot.get("signal_timestamp_source"))
            or match.get("method") == "explicit_timestamp"
        ):
            enriched_snapshot["signal_timestamp_source"] = match.get("timestamp_source")

    return {
        "success": bool(match["matched"]),
        "snapshot": {field: _json_safe_value(enriched_snapshot.get(field)) for field in SNAPSHOT_FIELDS},
        "match": match,
    }


def normalize_candidate_snapshot(candidate: dict[str, Any]) -> dict[str, Any]:
    """Normalize a Strategy Ranking style candidate into a frozen snapshot dict."""

    source_csv, _ = _first_present(candidate, "source_csv", "csv")
    ticker, _ = _first_present(candidate, "ticker")
    timeframe, _ = _first_present(candidate, "timeframe", "tf")
    signal_timestamp, signal_timestamp_source = _first_present(
        candidate,
        "signal_timestamp",
        "timestamp",
        "datetime",
        "date",
    )

    entry = _to_float(_first_present(candidate, "entry", "close")[0])
    stop_loss = _to_float(_first_present(candidate, "stop_loss", "sl")[0])
    take_profit = _to_float(_first_present(candidate, "take_profit", "tp")[0])
    risk_reward = _to_float(_first_present(candidate, "risk_reward", "rr")[0])
    if risk_reward is None:
        risk_reward = _computed_risk_reward(entry, stop_loss, take_profit)

    snapshot = {
        "ticker": ticker or _infer_ticker_from_csv(source_csv),
        "timeframe": timeframe or _infer_timeframe_from_text(str(source_csv) if source_csv else None),
        "source_csv": source_csv,
        "signal_timestamp": signal_timestamp,
        "signal_timestamp_source": signal_timestamp_source,
        "signal_row_index": _to_int(
            _first_present(candidate, "signal_row_index", "row_index", "source_row_index", "index")[0]
        ),
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward": risk_reward,
        "strategy_score": _to_float(_first_present(candidate, "strategy_score", "score")[0]),
        "wyckoff_phase": _first_present(candidate, "wyckoff_phase", "phase")[0],
        "wyckoff_event": _first_present(candidate, "wyckoff_event", "event")[0],
        "trend": _first_present(candidate, "trend")[0],
        "candidate_source": _first_present(candidate, "candidate_source", "source")[0] or "strategy_ranking",
        "report_date": _first_present(candidate, "report_date")[0],
        "direction": _first_present(candidate, "direction")[0] or "long",
        "source_report_dir": _first_present(candidate, "source_report_dir")[0],
        "source_strategy_rank": _to_int(_first_present(candidate, "source_strategy_rank", "rank")[0]),
    }
    return {field: _json_safe_value(snapshot.get(field)) for field in SNAPSHOT_FIELDS}


def validate_candidate_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Validate a normalized candidate snapshot without modifying source logic."""

    errors: list[str] = []
    warnings: list[str] = []
    statuses: list[str] = []

    direction = str(snapshot.get("direction") or "").lower()
    if direction not in SUPPORTED_DIRECTIONS:
        statuses.append(VALIDATION_UNSUPPORTED_DIRECTION)
        errors.append("Only long candidate snapshots are supported in this phase.")

    if _is_missing(snapshot.get("source_csv")):
        statuses.append(VALIDATION_MISSING_SOURCE_CSV)
        errors.append("Missing source_csv.")

    entry = _to_float(snapshot.get("entry"))
    stop_loss = _to_float(snapshot.get("stop_loss"))
    take_profit = _to_float(snapshot.get("take_profit"))
    if entry is None or stop_loss is None or take_profit is None:
        statuses.append(VALIDATION_MISSING_LEVELS)
        errors.append("Missing entry, stop_loss, or take_profit.")

    if snapshot.get("signal_row_index") is None and _is_missing(snapshot.get("signal_timestamp")):
        statuses.append(VALIDATION_MISSING_SIGNAL_LOCATION)
        errors.append("Missing signal_row_index or signal_timestamp.")

    if entry is not None and stop_loss is not None and take_profit is not None:
        if stop_loss >= entry or take_profit <= entry or entry == stop_loss:
            statuses.append(VALIDATION_INVALID_LEVELS)
            errors.append("Invalid long levels; expected stop_loss < entry < take_profit.")

    if _is_missing(snapshot.get("ticker")):
        warnings.append("Missing ticker.")
    if _is_missing(snapshot.get("timeframe")):
        warnings.append("Missing timeframe.")
    if _to_float(snapshot.get("risk_reward")) is None:
        warnings.append("risk_reward missing or could not be computed.")
    if not _is_missing(snapshot.get("signal_timestamp")) and _is_missing(snapshot.get("signal_timestamp_source")):
        warnings.append("signal_timestamp present without signal_timestamp_source.")

    priority = [
        VALIDATION_UNSUPPORTED_DIRECTION,
        VALIDATION_MISSING_SOURCE_CSV,
        VALIDATION_MISSING_LEVELS,
        VALIDATION_MISSING_SIGNAL_LOCATION,
        VALIDATION_INVALID_LEVELS,
    ]
    status = VALIDATION_VALID
    for candidate_status in priority:
        if candidate_status in statuses:
            status = candidate_status
            break

    return {"status": status, "errors": errors, "warnings": warnings}


def build_candidate_snapshot_from_strategy_candidate(
    candidate: dict[str, Any],
    *,
    report_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Normalize and validate a selected Strategy Ranking candidate."""

    snapshot = normalize_candidate_snapshot(candidate)
    if report_dir is not None and _is_missing(snapshot.get("source_report_dir")):
        snapshot["source_report_dir"] = str(report_dir)
    enrichment = enrich_candidate_snapshot_signal_location(snapshot)
    snapshot = enrichment["snapshot"]
    validation = validate_candidate_snapshot(snapshot)
    validation["warnings"].extend(enrichment.get("match", {}).get("warnings", []))
    return {
        "success": validation["status"] == VALIDATION_VALID,
        "snapshot": snapshot,
        "validation": validation,
        "signal_location_enrichment": enrichment.get("match"),
    }


def candidate_snapshot_dict_to_dataclass(snapshot: dict[str, Any]) -> CandidateSnapshot:
    """Convert a normalized snapshot dict to the lightweight dataclass schema."""

    return CandidateSnapshot(
        ticker=snapshot.get("ticker"),
        timeframe=snapshot.get("timeframe"),
        source_csv=snapshot.get("source_csv"),
        signal_timestamp=snapshot.get("signal_timestamp"),
        signal_row_index=_to_int(snapshot.get("signal_row_index")),
        entry=_to_float(snapshot.get("entry")),
        stop_loss=_to_float(snapshot.get("stop_loss")),
        take_profit=_to_float(snapshot.get("take_profit")),
        risk_reward=_to_float(snapshot.get("risk_reward")),
        strategy_score=_to_float(snapshot.get("strategy_score")),
        wyckoff_phase=snapshot.get("wyckoff_phase"),
        wyckoff_event=snapshot.get("wyckoff_event"),
        trend=snapshot.get("trend"),
        candidate_source=snapshot.get("candidate_source"),
        report_date=snapshot.get("report_date"),
    )
