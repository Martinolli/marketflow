"""Candidate snapshot normalization for future backtest calibration workflows."""

from __future__ import annotations

import math
import re
from dataclasses import fields
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.backtesting.schemas import CandidateSnapshot
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_strategy import (
    COMPONENT_EVENT,
    COMPONENT_PHASE,
    COMPONENT_PNF,
    COMPONENT_POP,
    COMPONENT_TREND,
    EVIDENCE_AVAILABLE,
    EVIDENCE_DISABLED_BY_CONFIGURATION,
    EVIDENCE_NOT_AVAILABLE,
    EVENT_NOT_AVAILABLE,
    EVENT_SOURCE_UNSAFE,
    SCORE_INCOMPLETE,
    SCORE_INVALID,
    SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED,
    SCORE_PROFILE_UNSAFE,
    SOURCE_STATUS_EXACT_MATCH,
    _resolve_wyckoff_event,
)


VALIDATION_VALID = "valid"
VALIDATION_MISSING_LEVELS = "missing_levels"
VALIDATION_MISSING_SOURCE_CSV = "missing_source_csv"
VALIDATION_MISSING_SIGNAL_LOCATION = "missing_signal_location"
VALIDATION_INVALID_LEVELS = "invalid_levels"
VALIDATION_UNSUPPORTED_DIRECTION = "unsupported_direction"
LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE = "LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE"

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
CONFIRMED_EVENT_COLUMN_CANDIDATES = (
    "wyckoff_confirmed_event",
    "confirmed_wyckoff_event",
    "confirmed_event",
    "wyckoff_event_confirmed",
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
    "target_status",
    "target_provenance",
    "target_structural_level_kind",
    "rr_status",
    "volatility_status",
    "volatility_provenance",
    "volatility_window",
    "volatility_value",
    "strategy_score",
    "composite_score",
    "score_status",
    "score_reason",
    "active_evidence_profile",
    "configured_weight_total",
    "active_weight_total",
    "available_weight_total",
    "evidence_coverage",
    "missing_components",
    "disabled_components",
    "invalid_components",
    "rank_eligible",
    "score_profile_calibration",
    "phase_evidence_status",
    "phase_evidence_score",
    "phase_evidence_configured_weight",
    "phase_evidence_active_weight",
    "phase_evidence_provenance",
    "phase_evidence_reason",
    "phase_evidence_expected_by_profile",
    "phase_evidence_scoring_eligible",
    "event_evidence_status",
    "event_evidence_score",
    "event_evidence_configured_weight",
    "event_evidence_active_weight",
    "event_evidence_provenance",
    "event_evidence_reason",
    "event_evidence_expected_by_profile",
    "event_evidence_scoring_eligible",
    "pnf_score",
    "pnf_evidence_status",
    "pnf_evidence_score",
    "pnf_evidence_configured_weight",
    "pnf_evidence_active_weight",
    "pnf_evidence_provenance",
    "pnf_evidence_reason",
    "pnf_evidence_expected_by_profile",
    "pnf_evidence_scoring_eligible",
    "pop_evidence_status",
    "pop_evidence_score",
    "pop_evidence_configured_weight",
    "pop_evidence_active_weight",
    "pop_evidence_provenance",
    "pop_evidence_reason",
    "pop_evidence_expected_by_profile",
    "pop_evidence_scoring_eligible",
    "trend_evidence_status",
    "trend_evidence_score",
    "trend_evidence_configured_weight",
    "trend_evidence_active_weight",
    "trend_evidence_provenance",
    "trend_evidence_reason",
    "trend_evidence_expected_by_profile",
    "trend_evidence_scoring_eligible",
    "wyckoff_phase",
    "wyckoff_event",
    "event_status",
    "event_provenance",
    "event_age_bars",
    "event_max_age_bars",
    "event_scoring_eligible",
    "event_occurrence_row_index",
    "event_occurrence_timestamp",
    "event_decision_row_index",
    "event_superseded_count",
    "event_reason",
    "event_resolution_source",
    "trend",
    "candidate_source",
    "report_date",
    "direction",
    "source_report_dir",
    "source_status",
    "source_strategy_rank",
]

LEGACY_SCORE_FIELDS = (
    "score",
    "strategy_score",
    "composite_score",
    "pnf_score",
    "pop",
    "pop_evidence_score",
)
EVIDENCE_STATUS_FIELDS = (
    "score_status",
    "phase_evidence_status",
    "event_evidence_status",
    "pnf_evidence_status",
    "pop_evidence_status",
    "trend_evidence_status",
)
LEGACY_COMPONENTS = (
    COMPONENT_PHASE,
    COMPONENT_EVENT,
    COMPONENT_PNF,
    COMPONENT_POP,
    COMPONENT_TREND,
)
REQUIRED_LEGACY_COMPONENTS = (
    COMPONENT_PHASE,
    COMPONENT_EVENT,
    COMPONENT_TREND,
)
NON_COMPLETE_SCORE_STATUSES = (
    SCORE_INCOMPLETE,
    SCORE_INVALID,
    SCORE_PROFILE_UNSAFE,
    SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED,
)


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
    if isinstance(value, dict):
        return {str(key): _json_safe_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe_value(item) for item in value]
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


def _has_evidence_status(snapshot: dict[str, Any]) -> bool:
    return any(not _is_missing(snapshot.get(field)) for field in EVIDENCE_STATUS_FIELDS)


def _is_truthy(value: Any) -> bool:
    value = _json_safe_value(value)
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return False


def _component_names(value: Any) -> set[str]:
    value = _json_safe_value(value)
    if isinstance(value, list):
        return {str(item).strip() for item in value if str(item).strip()}
    if isinstance(value, str):
        return {item.strip() for item in value.split(",") if item.strip()}
    return set()


def _has_safe_complete_evidence_diagnostics(snapshot: dict[str, Any]) -> bool:
    if snapshot.get("score_status") != "SCORE_COMPLETE":
        return False
    if _to_float(snapshot.get("composite_score")) is None:
        return False
    active_weight_total = _to_float(snapshot.get("active_weight_total"))
    if active_weight_total is None or active_weight_total <= 0:
        return False
    active_components = _component_names(snapshot.get("active_evidence_profile"))
    if not active_components or not set(REQUIRED_LEGACY_COMPONENTS).issubset(active_components):
        return False

    disabled_components: list[str] = []
    for component in LEGACY_COMPONENTS:
        status = snapshot.get(f"{component}_evidence_status")
        score = _to_float(snapshot.get(f"{component}_evidence_score"))
        scoring_eligible = _is_truthy(snapshot.get(f"{component}_evidence_scoring_eligible"))
        if component in active_components:
            if status != EVIDENCE_AVAILABLE:
                return False
            if score is None:
                return False
            if _is_missing(snapshot.get(f"{component}_evidence_provenance")):
                return False
            if not scoring_eligible:
                return False
            active_weight = _to_float(snapshot.get(f"{component}_evidence_active_weight"))
            if active_weight is None or active_weight <= 0:
                return False
            continue

        disabled_components.append(component)
        if status != EVIDENCE_DISABLED_BY_CONFIGURATION:
            return False
        if score is not None or scoring_eligible:
            return False

    if disabled_components:
        if snapshot.get("score_profile_calibration") != SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED:
            return False
        if _is_truthy(snapshot.get("rank_eligible")):
            return False
    return True


def _has_legacy_score_value(candidate: dict[str, Any], snapshot: dict[str, Any]) -> bool:
    for field in LEGACY_SCORE_FIELDS:
        if _to_float(candidate.get(field)) is not None or _to_float(snapshot.get(field)) is not None:
            return True
    return False


def _clear_non_available_component_scores(snapshot: dict[str, Any]) -> None:
    for component in LEGACY_COMPONENTS:
        if snapshot.get(f"{component}_evidence_status") != EVIDENCE_AVAILABLE:
            snapshot[f"{component}_evidence_score"] = None
            snapshot[f"{component}_evidence_scoring_eligible"] = False


def _mark_non_complete_non_actionable(snapshot: dict[str, Any]) -> None:
    snapshot["rank_eligible"] = False
    snapshot["composite_score"] = None
    _clear_non_available_component_scores(snapshot)


def _mark_missing_legacy_score_incomplete(snapshot: dict[str, Any]) -> None:
    snapshot["score_status"] = SCORE_INCOMPLETE
    snapshot["score_reason"] = LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE
    snapshot["composite_score"] = None
    snapshot["rank_eligible"] = False
    snapshot["missing_components"] = list(LEGACY_COMPONENTS)

    for component in LEGACY_COMPONENTS:
        prefix = f"{component}_evidence"
        snapshot[f"{prefix}_status"] = EVIDENCE_NOT_AVAILABLE
        snapshot[f"{prefix}_score"] = None
        snapshot[f"{prefix}_reason"] = LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE
        snapshot[f"{prefix}_scoring_eligible"] = False

    snapshot["pnf_score"] = None


def _mark_legacy_score_incomplete(candidate: dict[str, Any], snapshot: dict[str, Any]) -> None:
    if snapshot.get("score_status") == "SCORE_COMPLETE":
        if _has_safe_complete_evidence_diagnostics(snapshot):
            return
        _mark_missing_legacy_score_incomplete(snapshot)
        return
    if snapshot.get("score_status") in NON_COMPLETE_SCORE_STATUSES:
        _mark_non_complete_non_actionable(snapshot)
        return
    if not _has_legacy_score_value(candidate, snapshot):
        return
    _mark_missing_legacy_score_incomplete(snapshot)


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


def _snapshot_has_event_diagnostics(snapshot: dict[str, Any]) -> bool:
    return not _is_missing(snapshot.get("event_status"))


def _resolve_snapshot_event_diagnostics(
    snapshot: dict[str, Any],
    *,
    max_event_age_bars: int | None = None,
) -> dict[str, Any]:
    enriched = dict(snapshot)
    if _snapshot_has_event_diagnostics(enriched):
        return enriched

    def _with_event_failure(status: str, resolution_source: str | None = None) -> dict[str, Any]:
        enriched.update(
            {
                "event_status": status,
                "event_provenance": None,
                "event_age_bars": None,
                "event_max_age_bars": max_event_age_bars,
                "event_scoring_eligible": False,
                "event_occurrence_row_index": None,
                "event_occurrence_timestamp": None,
                "event_decision_row_index": _to_int(enriched.get("signal_row_index")),
                "event_superseded_count": 0,
                "event_reason": status,
                "event_resolution_source": resolution_source,
            }
        )
        return {field: _json_safe_value(enriched.get(field)) for field in SNAPSHOT_FIELDS}

    if enriched.get("source_status") != SOURCE_STATUS_EXACT_MATCH:
        return _with_event_failure(EVENT_SOURCE_UNSAFE)
    source_path = _candidate_source_path(enriched.get("source_csv"), enriched.get("source_report_dir"))
    signal_row_index = _to_int(enriched.get("signal_row_index"))
    if source_path is None or signal_row_index is None:
        return _with_event_failure(EVENT_NOT_AVAILABLE)
    try:
        dataframe = pd.read_csv(source_path)
    except Exception:
        return _with_event_failure(EVENT_SOURCE_UNSAFE)
    event_column = _first_existing_column(dataframe, *CONFIRMED_EVENT_COLUMN_CANDIDATES)
    if event_column is None:
        return _with_event_failure(EVENT_NOT_AVAILABLE)
    resolution = _resolve_wyckoff_event(
        dataframe,
        max_event_age_bars,
        decision_row_index=signal_row_index,
        event_column=event_column,
    )
    enriched.update(
        {
            "event_status": resolution.status,
            "event_provenance": resolution.provenance,
            "event_age_bars": resolution.event_age_bars,
            "event_max_age_bars": resolution.max_event_age_bars,
            "event_scoring_eligible": resolution.scoring_eligible,
            "event_occurrence_row_index": resolution.occurrence_row_index,
            "event_occurrence_timestamp": resolution.occurrence_timestamp,
            "event_decision_row_index": resolution.decision_row_index,
            "event_superseded_count": resolution.superseded_event_count,
            "event_reason": resolution.reason,
            "event_resolution_source": event_column,
        }
    )
    if _is_missing(enriched.get("wyckoff_event")) and resolution.event:
        enriched["wyckoff_event"] = resolution.event
    return {field: _json_safe_value(enriched.get(field)) for field in SNAPSHOT_FIELDS}


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
        "target_status": _first_present(candidate, "target_status")[0],
        "target_provenance": _first_present(candidate, "target_provenance")[0],
        "target_structural_level_kind": _first_present(candidate, "target_structural_level_kind")[0],
        "rr_status": _first_present(candidate, "rr_status")[0],
        "volatility_status": _first_present(candidate, "volatility_status")[0],
        "volatility_provenance": _first_present(candidate, "volatility_provenance")[0],
        "volatility_window": _to_int(_first_present(candidate, "volatility_window")[0]),
        "volatility_value": _to_float(_first_present(candidate, "volatility_value")[0]),
        "strategy_score": _to_float(_first_present(candidate, "strategy_score", "score")[0]),
        "wyckoff_phase": _first_present(candidate, "wyckoff_phase", "phase")[0],
        "wyckoff_event": _first_present(candidate, "wyckoff_event", "event")[0],
        "event_status": _first_present(candidate, "event_status")[0],
        "event_provenance": _first_present(candidate, "event_provenance")[0],
        "event_age_bars": _to_int(_first_present(candidate, "event_age_bars")[0]),
        "event_max_age_bars": _to_int(_first_present(candidate, "event_max_age_bars")[0]),
        "event_scoring_eligible": _first_present(candidate, "event_scoring_eligible")[0],
        "event_occurrence_row_index": _to_int(_first_present(candidate, "event_occurrence_row_index")[0]),
        "event_occurrence_timestamp": _first_present(candidate, "event_occurrence_timestamp")[0],
        "event_decision_row_index": _to_int(_first_present(candidate, "event_decision_row_index")[0]),
        "event_superseded_count": _to_int(_first_present(candidate, "event_superseded_count")[0]),
        "event_reason": _first_present(candidate, "event_reason")[0],
        "event_resolution_source": _first_present(candidate, "event_resolution_source")[0],
        "trend": _first_present(candidate, "trend")[0],
        "candidate_source": _first_present(candidate, "candidate_source", "source")[0] or "strategy_ranking",
        "report_date": _first_present(candidate, "report_date")[0],
        "direction": _first_present(candidate, "direction")[0] or "long",
        "source_report_dir": _first_present(candidate, "source_report_dir")[0],
        "source_status": _first_present(candidate, "source_status")[0],
        "source_strategy_rank": _to_int(_first_present(candidate, "source_strategy_rank", "rank")[0]),
    }
    for field in SNAPSHOT_FIELDS:
        if field not in snapshot:
            snapshot[field] = _first_present(candidate, field)[0]
    _mark_legacy_score_incomplete(candidate, snapshot)
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
    max_event_age_bars: int | None = None,
) -> dict[str, Any]:
    """Normalize and validate a selected Strategy Ranking candidate."""

    snapshot = normalize_candidate_snapshot(candidate)
    if report_dir is not None and _is_missing(snapshot.get("source_report_dir")):
        snapshot["source_report_dir"] = str(report_dir)
    enrichment = enrich_candidate_snapshot_signal_location(snapshot)
    snapshot = _resolve_snapshot_event_diagnostics(
        enrichment["snapshot"],
        max_event_age_bars=max_event_age_bars,
    )
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

    normalized = normalize_candidate_snapshot(snapshot)
    numeric_fields = {
        "signal_row_index",
        "entry",
        "stop_loss",
        "take_profit",
        "risk_reward",
        "strategy_score",
        "composite_score",
        "configured_weight_total",
        "active_weight_total",
        "available_weight_total",
        "evidence_coverage",
        "phase_evidence_score",
        "phase_evidence_configured_weight",
        "phase_evidence_active_weight",
        "event_evidence_score",
        "event_evidence_configured_weight",
        "event_evidence_active_weight",
        "pnf_score",
        "pnf_evidence_score",
        "pnf_evidence_configured_weight",
        "pnf_evidence_active_weight",
        "pop_evidence_score",
        "pop_evidence_configured_weight",
        "pop_evidence_active_weight",
        "trend_evidence_score",
        "trend_evidence_configured_weight",
        "trend_evidence_active_weight",
        "event_age_bars",
        "event_max_age_bars",
        "event_occurrence_row_index",
        "event_decision_row_index",
        "event_superseded_count",
        "source_strategy_rank",
    }
    values: dict[str, Any] = {}
    for field in fields(CandidateSnapshot):
        value = normalized.get(field.name)
        values[field.name] = _to_float(value) if field.name in numeric_fields else value
    for field in (
        "signal_row_index",
        "event_age_bars",
        "event_max_age_bars",
        "event_occurrence_row_index",
        "event_decision_row_index",
        "event_superseded_count",
    ):
        if field in values:
            values[field] = _to_int(normalized.get(field))
    return CandidateSnapshot(**values)
