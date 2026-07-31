"""Read-only historical dataset remediation governance for MarketFlow."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import tomllib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import pandas as pd


REPORT_SCHEMA_VERSION = "marketflow.data_readiness_remediation_report.v1"
REGISTRY_SCHEMA_VERSION = "marketflow.canonical_dataset_registry.v1"
DECISION_REGISTER_SCHEMA_VERSION = "marketflow.dataset_decision_register.v1"
MODULE_VERSION = "marketflow.research.data_readiness_remediation.v1"

CANONICAL_SUFFIX = "_wyckoff_annotated.csv"
CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN = "CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN"
HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
NOT_ESTABLISHED = "NOT_ESTABLISHED"
REVIEW_REQUIRED = "REVIEW_REQUIRED"
NOT_APPLICABLE = "NOT_APPLICABLE"

FIXED_PROFILE_REQUIREMENTS = {
    "SWING": {"timeframe": "4h", "required_rows": 390},
    "POSITION_SWING": {"timeframe": "1d", "required_rows": 560},
}

SUPPORTED_TIMEFRAMES = ("1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m")
RESEARCH_TIMEFRAMES = ("1d", "1h", "1w", "4h")
TIMESTAMP_COLUMNS = ("timestamp", "datetime", "date", "time", "Date", "Datetime")
OHLCV_COLUMNS = ("open", "high", "low", "close", "volume")
PROVENANCE_COLUMNS = (
    "source_provenance",
    "provider",
    "data_provider",
    "source_provider",
    "schema_version",
    "manifest_schema_version",
)
ADJUSTMENT_COLUMNS = ("adjustment_status", "corporate_action_adjustment_status")
ANNOTATION_FOCUS_COLUMNS = (
    "wyckoff_phase",
    "phase",
    "wyckoff_event",
    "raw_event",
    "wyckoff_confirmed_event",
    "confirmed_event",
    "wyckoff_confirmed_event_occurrence",
    "confirmed_event_occurrence",
    "tr_low",
    "tr_high",
    "true_range",
    "volatility",
    "pnf_signal",
    "pnf_score",
    "pnf_pattern",
)
DERIVATIVE_MARKERS = (
    "_pv_eigen.csv",
    "_backtest_candidates",
    "_backtest_results",
    "_walk_forward_cases_",
    "_walk_forward_results_",
    "_walk_forward_summary_",
    "_walk_forward_campaign_",
    "_walk_forward_run_registry",
    "_mc_summary",
)

EXACT_BYTE_DUPLICATES = "EXACT_BYTE_DUPLICATES"
SEMANTICALLY_IDENTICAL = "SEMANTICALLY_IDENTICAL"
SAME_OHLCV_DIFFERENT_ANNOTATIONS = "SAME_OHLCV_DIFFERENT_ANNOTATIONS"
STRICT_SUPERSET_COMPATIBLE = "STRICT_SUPERSET_COMPATIBLE"
STRICT_SUBSET_COMPATIBLE = "STRICT_SUBSET_COMPATIBLE"
OVERLAPPING_COMPATIBLE = "OVERLAPPING_COMPATIBLE"
OVERLAPPING_CONFLICTING = "OVERLAPPING_CONFLICTING"
DISJOINT_HISTORY_SAME_IDENTITY = "DISJOINT_HISTORY_SAME_IDENTITY"
SCHEMA_DIVERGENT = "SCHEMA_DIVERGENT"
TIMESTAMP_NORMALIZATION_CONFLICT = "TIMESTAMP_NORMALIZATION_CONFLICT"
PROVENANCE_CONFLICT = "PROVENANCE_CONFLICT"
IDENTITY_INVALID = "IDENTITY_INVALID"
UNCLASSIFIED_REVIEW_REQUIRED = "UNCLASSIFIED_REVIEW_REQUIRED"

DUPLICATE_CLASSIFICATIONS = (
    EXACT_BYTE_DUPLICATES,
    SEMANTICALLY_IDENTICAL,
    SAME_OHLCV_DIFFERENT_ANNOTATIONS,
    STRICT_SUPERSET_COMPATIBLE,
    STRICT_SUBSET_COMPATIBLE,
    OVERLAPPING_COMPATIBLE,
    OVERLAPPING_CONFLICTING,
    DISJOINT_HISTORY_SAME_IDENTITY,
    SCHEMA_DIVERGENT,
    TIMESTAMP_NORMALIZATION_CONFLICT,
    PROVENANCE_CONFLICT,
    IDENTITY_INVALID,
    UNCLASSIFIED_REVIEW_REQUIRED,
)

SAFE_REDUNDANCY_REVIEW = "SAFE_REDUNDANCY_REVIEW"
MANUAL_CANONICAL_SELECTION_REQUIRED = "MANUAL_CANONICAL_SELECTION_REQUIRED"
MANUAL_MERGE_REVIEW_REQUIRED = "MANUAL_MERGE_REVIEW_REQUIRED"
REANNOTATION_RECOMMENDED = "REANNOTATION_RECOMMENDED"
SOURCE_REACQUISITION_RECOMMENDED = "SOURCE_REACQUISITION_RECOMMENDED"
PROVENANCE_CONFIRMATION_REQUIRED = "PROVENANCE_CONFIRMATION_REQUIRED"
NO_SAFE_REMEDIATION_IDENTIFIED = "NO_SAFE_REMEDIATION_IDENTIFIED"

REGISTRY_STATUSES = (
    "UNRESOLVED",
    "APPROVED",
    "SUSPENDED",
    "CONFLICT_REVIEW_REQUIRED",
    "REACQUISITION_REQUIRED",
)
DECISION_STATUSES = ("PENDING", "APPROVED", "REJECTED")
DATA_READINESS_STATUSES = (
    "READY_PENDING_CANONICAL_APPROVAL",
    "DUPLICATE_REVIEW_REQUIRED",
    "CONFLICT_REVIEW_REQUIRED",
    "INSUFFICIENT_HISTORY",
    "REANNOTATION_REQUIRED",
    "PROVENANCE_REQUIRED",
    "REACQUISITION_REQUIRED",
    "DATASET_INVALID",
)
FORBIDDEN_RATIONALE_CATEGORIES = {
    "PERFORMANCE",
    "PROFITABILITY",
    "WIN_RATE",
    "EXPECTANCY",
    "SHARPE",
    "DRAWDOWN",
    "OUTCOME",
    "CANDIDATE_SCORE",
}
FORBIDDEN_RATIONALE_FRAGMENTS = (
    "PERFORMANCE",
    "PROFIT",
    "LOSS",
    "WIN_RATE",
    "EXPECTANCY",
    "SHARPE",
    "SORTINO",
    "DRAWDOWN",
    "R_MULTIPLE",
    "R-MULTIPLE",
    "MFE",
    "MAE",
    "OUTCOME",
    "CANDIDATE_SCORE",
    "CANDIDATE-SCORE",
    "BEST_TICKER",
    "BEST_TIMEFRAME",
    "BEST_PERIOD",
    "BEST_SOURCE",
    "OPTIMIZATION",
    "OPTIMISATION",
)

REGISTRY_REQUIRED_FIELDS = {
    "registry_schema_version",
    "canonical_ticker",
    "canonical_timeframe",
    "status",
    "approved_safe_relative_source_reference",
    "approved_file_sha256",
    "approved_semantic_ohlcv_digest",
    "provenance_status",
    "adjustment_status",
    "approval_evidence_category",
    "decision_id",
    "decision_timestamp",
    "superseded_source_references",
    "notes_category",
}
DECISION_REQUIRED_FIELDS = {
    "decision_id",
    "identity",
    "examined_source_digests",
    "duplicate_classification",
    "decision_status",
    "selected_canonical_source",
    "rationale_category",
    "operator_approval_status",
    "evidence_timestamp",
    "code_commit",
    "remediation_action_status",
}
WINDOWS_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


@dataclass(frozen=True)
class SourceInventory:
    canonical_ticker: str
    canonical_timeframe: str
    safe_relative_reference: str
    file_sha256: str
    byte_size: int
    schema_columns: tuple[str, ...]
    row_count: int
    valid_ohlcv_count: int
    earliest_timestamp: str | None
    latest_timestamp: str | None
    timezone_information: str
    duplicate_timestamp_count: int
    non_monotonic_timestamp_count: int
    missing_ohlcv_count: int
    non_finite_ohlcv_count: int
    invalid_high_low_geometry_count: int
    invalid_volume_count: int
    annotation_column_set: tuple[str, ...]
    explicit_provenance_metadata: dict[str, str]
    explicit_corporate_action_adjustment_status: str
    safe_source_classification: str
    median_interval: str | None
    irregular_interval_count: int
    timeframe_interval_compatible: bool
    identity_status: str
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    _ohlcv_by_timestamp: dict[str, tuple[str, str, str, str, str]] = field(default_factory=dict, compare=False, repr=False)
    _annotations_by_timestamp: dict[str, dict[str, str]] = field(default_factory=dict, compare=False, repr=False)

    def public_dict(self) -> dict[str, Any]:
        return {
            "canonical_ticker": self.canonical_ticker,
            "canonical_timeframe": self.canonical_timeframe,
            "safe_relative_reference": self.safe_relative_reference,
            "file_sha256": self.file_sha256,
            "byte_size": self.byte_size,
            "schema_column_sequence": list(self.schema_columns),
            "row_count": self.row_count,
            "valid_ohlcv_count": self.valid_ohlcv_count,
            "earliest_timestamp": self.earliest_timestamp,
            "latest_timestamp": self.latest_timestamp,
            "timezone_information": self.timezone_information,
            "duplicate_timestamp_count": self.duplicate_timestamp_count,
            "non_monotonic_timestamp_count": self.non_monotonic_timestamp_count,
            "missing_ohlcv_count": self.missing_ohlcv_count,
            "non_finite_ohlcv_count": self.non_finite_ohlcv_count,
            "invalid_high_low_geometry_count": self.invalid_high_low_geometry_count,
            "invalid_volume_count": self.invalid_volume_count,
            "annotation_column_set": list(self.annotation_column_set),
            "explicit_provenance_metadata": dict(self.explicit_provenance_metadata),
            "explicit_corporate_action_adjustment_status": self.explicit_corporate_action_adjustment_status,
            "safe_source_classification": self.safe_source_classification,
            "median_interval": self.median_interval,
            "irregular_interval_count": self.irregular_interval_count,
            "timeframe_interval_compatible": self.timeframe_interval_compatible,
            "identity_status": self.identity_status,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def semantic_digest(payload: Any) -> str:
    return sha256_bytes(canonical_json_bytes(payload))


def _repo_root(path: str | Path) -> Path:
    return Path(path).resolve()


def _is_relative_safe_ref(ref: object) -> bool:
    if not isinstance(ref, str) or not ref or "\\" in ref or ":" in ref:
        return False
    candidate = Path(ref)
    if candidate.is_absolute():
        return False
    for part in candidate.parts:
        if part in {"", ".", ".."}:
            return False
        normalized = part.rstrip(" .").split(".")[0].upper()
        if normalized in WINDOWS_DEVICE_NAMES:
            return False
    return True


def safe_relative_reference(path: str | Path, repo_root: str | Path) -> str:
    root = _repo_root(repo_root)
    resolved = Path(path).resolve(strict=True)
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("path must stay inside repository root") from exc
    ref = relative.as_posix()
    if not _is_relative_safe_ref(ref):
        raise ValueError("path cannot be represented as a safe relative reference")
    return ref


def _resolve_safe_ref(repo_root: str | Path, ref: str) -> Path:
    if not _is_relative_safe_ref(ref):
        raise ValueError("source reference must be safe and relative")
    root = _repo_root(repo_root)
    resolved = (root / ref).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("source reference escapes repository root") from exc
    return resolved


def _default_dataset_roots(repo_root: Path) -> tuple[Path, ...]:
    return (repo_root / ".marketflow" / "reports", repo_root / "data")


def _approved_roots(repo_root: str | Path, roots: list[str | Path] | None = None) -> tuple[Path, ...]:
    root = _repo_root(repo_root)
    configured = roots if roots is not None else list(_default_dataset_roots(root))
    approved: list[Path] = []
    for item in configured:
        candidate = Path(item)
        if not candidate.is_absolute():
            candidate = root / candidate
        resolved = candidate.resolve(strict=False)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError("dataset roots must stay inside repository root") from exc
        approved.append(resolved)
    return tuple(approved)


def _is_canonical_dataset_file(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(CANONICAL_SUFFIX) and not any(marker in name for marker in DERIVATIVE_MARKERS)


def parse_source_identity(path: str | Path) -> tuple[str | None, str | None]:
    stem = Path(path).stem
    lowered = stem.lower()
    if not lowered.endswith("_wyckoff_annotated"):
        return None, None
    core = stem[: -len("_wyckoff_annotated")]
    parts = [part for part in core.replace("-", "_").split("_") if part]
    matches = [(index, part.lower()) for index, part in enumerate(parts) if part.lower() in SUPPORTED_TIMEFRAMES]
    if len(matches) != 1:
        return None, None
    index, timeframe = matches[0]
    if index == 0:
        return None, None
    ticker = "_".join(parts[:index]).upper()
    if not ticker or any(separator in ticker for separator in ("/", "\\")):
        return None, None
    return ticker, timeframe


def discover_canonical_sources(repo_root: str | Path, roots: list[str | Path] | None = None) -> list[Path]:
    root = _repo_root(repo_root)
    sources: list[Path] = []
    for search_root in _approved_roots(root, roots):
        if not search_root.exists():
            continue
        if not search_root.is_dir():
            raise ValueError("dataset root must be a directory")
        for path in search_root.rglob("*.csv"):
            if _is_canonical_dataset_file(path):
                ticker, timeframe = parse_source_identity(path)
                if ticker and timeframe in RESEARCH_TIMEFRAMES:
                    sources.append(path)
    return sorted(sources, key=lambda item: safe_relative_reference(item, root))


def _read_csv_text(path: Path) -> tuple[list[str], list[dict[str, str]], list[list[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = [str(column) for column in (reader.fieldnames or [])]
        rows: list[dict[str, str]] = []
        raw_rows: list[list[str]] = []
        handle.seek(0)
        raw_reader = csv.reader(handle)
        next(raw_reader, None)
        for raw in raw_reader:
            raw_rows.append([str(value) for value in raw])
        handle.seek(0)
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({str(key): "" if value is None else str(value) for key, value in row.items() if key is not None})
    return columns, rows, raw_rows


def _column_lookup(columns: tuple[str, ...], name: str) -> str | None:
    lower = {column.lower(): column for column in columns}
    return lower.get(name.lower())


def _first_column(columns: tuple[str, ...], candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        match = _column_lookup(columns, candidate)
        if match:
            return match
    return None


def _timestamp_key(value: str) -> tuple[str | None, str | None]:
    text = str(value).strip()
    if not text:
        return None, None
    try:
        timestamp = pd.Timestamp(text)
    except (TypeError, ValueError):
        return None, None
    if pd.isna(timestamp):
        return None, None
    if timestamp.tzinfo is not None:
        return timestamp.tz_convert("UTC").isoformat(), "timezone_aware_utc_normalized"
    return timestamp.isoformat(), "timezone_naive_or_unspecified"


def _decimal_key(value: str) -> str | None:
    text = str(value).strip()
    if not text:
        return None
    lowered = text.lower()
    if lowered in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}:
        return None
    try:
        decimal = Decimal(text)
    except (InvalidOperation, ValueError):
        return None
    if not decimal.is_finite():
        return None
    if decimal == 0:
        decimal = Decimal("0")
    return format(decimal.normalize(), "f")


def _interval_summary(timestamp_keys: list[str]) -> tuple[str | None, int, bool]:
    timestamps = [pd.Timestamp(key) for key in timestamp_keys]
    if len(timestamps) < 2:
        return None, 0, True
    deltas = [timestamps[index] - timestamps[index - 1] for index in range(1, len(timestamps))]
    positive = [delta for delta in deltas if delta > pd.Timedelta(0)]
    if not positive:
        return None, len(deltas), False
    median = sorted(positive)[len(positive) // 2]
    irregular = sum(1 for delta in deltas if delta != median and delta > pd.Timedelta(0))
    compatible = all(delta > pd.Timedelta(0) for delta in deltas)
    return str(median), int(irregular), compatible


def _metadata_from_columns(rows: list[dict[str, str]], columns: tuple[str, ...]) -> tuple[dict[str, str], str]:
    provenance: dict[str, str] = {}
    for column in PROVENANCE_COLUMNS:
        match = _column_lookup(columns, column)
        if not match:
            continue
        value = next((str(row.get(match, "")).strip() for row in rows if str(row.get(match, "")).strip()), "")
        if value:
            provenance[column] = value
    adjustment = CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN
    for column in ADJUSTMENT_COLUMNS:
        match = _column_lookup(columns, column)
        if not match:
            continue
        value = next((str(row.get(match, "")).strip() for row in rows if str(row.get(match, "")).strip()), "")
        if value:
            adjustment = value
            break
    return provenance, adjustment


def inspect_source(path: str | Path, repo_root: str | Path) -> SourceInventory:
    root = _repo_root(repo_root)
    source = Path(path)
    errors: list[str] = []
    warnings: list[str] = []
    try:
        ref = safe_relative_reference(source, root)
    except (OSError, ValueError):
        ref = source.name
        errors.append("SOURCE_PATH_UNSAFE")
        ticker, timeframe = parse_source_identity(source)
        return SourceInventory(
            canonical_ticker=ticker or "UNKNOWN",
            canonical_timeframe=timeframe or "unknown",
            safe_relative_reference=ref,
            file_sha256="",
            byte_size=0,
            schema_columns=(),
            row_count=0,
            valid_ohlcv_count=0,
            earliest_timestamp=None,
            latest_timestamp=None,
            timezone_information="UNKNOWN",
            duplicate_timestamp_count=0,
            non_monotonic_timestamp_count=0,
            missing_ohlcv_count=0,
            non_finite_ohlcv_count=0,
            invalid_high_low_geometry_count=0,
            invalid_volume_count=0,
            annotation_column_set=(),
            explicit_provenance_metadata={},
            explicit_corporate_action_adjustment_status=CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN,
            safe_source_classification="UNSAFE",
            median_interval=None,
            irregular_interval_count=0,
            timeframe_interval_compatible=False,
            identity_status="INVALID",
            errors=tuple(errors),
        )
    ticker, timeframe = parse_source_identity(source)
    if ticker is None or timeframe is None:
        ticker = ticker or "UNKNOWN"
        timeframe = timeframe or "unknown"
        errors.append("IDENTITY_INVALID")
    try:
        payload = source.read_bytes()
    except OSError:
        payload = b""
        errors.append("SOURCE_READ_FAILED")
    file_digest = sha256_bytes(payload)
    byte_size = len(payload)
    try:
        columns_list, rows, _ = _read_csv_text(source)
    except Exception:
        columns_list, rows = [], []
        errors.append("CSV_PARSE_FAILED")
    columns = tuple(columns_list)
    timestamp_column = _first_column(columns, TIMESTAMP_COLUMNS)
    ohlcv_map = {column: _column_lookup(columns, column) for column in OHLCV_COLUMNS}
    if timestamp_column is None:
        errors.append("TIMESTAMP_COLUMN_MISSING")
    missing_core = [key for key, match in ohlcv_map.items() if match is None]
    if missing_core:
        errors.append("OHLCV_COLUMNS_MISSING")

    timestamp_keys: list[str] = []
    timezone_states: set[str] = set()
    duplicate_timestamp_count = 0
    non_monotonic_timestamp_count = 0
    missing_ohlcv_count = 0
    non_finite_ohlcv_count = 0
    invalid_high_low_count = 0
    invalid_volume_count = 0
    valid_ohlcv_count = 0
    ohlcv_by_timestamp: dict[str, tuple[str, str, str, str, str]] = {}
    annotations_by_timestamp: dict[str, dict[str, str]] = {}

    annotation_columns = tuple(
        column
        for column in columns
        if column in ANNOTATION_FOCUS_COLUMNS or column.lower().startswith(("wyckoff_", "pnf_", "tr_"))
    )
    provenance, adjustment = _metadata_from_columns(rows, columns)

    seen_timestamps: set[str] = set()
    previous_timestamp: pd.Timestamp | None = None
    for row in rows:
        timestamp = None
        timezone_state = None
        if timestamp_column:
            timestamp, timezone_state = _timestamp_key(row.get(timestamp_column, ""))
        if timestamp is None:
            warnings.append("TIMESTAMP_VALUE_INVALID")
        else:
            timestamp_keys.append(timestamp)
            if timezone_state:
                timezone_states.add(timezone_state)
            if timestamp in seen_timestamps:
                duplicate_timestamp_count += 1
            seen_timestamps.add(timestamp)
            current = pd.Timestamp(timestamp)
            if previous_timestamp is not None and current <= previous_timestamp:
                non_monotonic_timestamp_count += 1
            previous_timestamp = current

        numeric_values: dict[str, str] = {}
        row_missing = False
        row_non_finite = False
        for key, column in ohlcv_map.items():
            value = _decimal_key(row.get(column or "", ""))
            if value is None:
                if not str(row.get(column or "", "")).strip():
                    row_missing = True
                else:
                    row_non_finite = True
            else:
                numeric_values[key] = value
        if row_missing:
            missing_ohlcv_count += 1
        if row_non_finite:
            non_finite_ohlcv_count += 1
        geometry_ok = True
        volume_ok = True
        if all(key in numeric_values for key in ("open", "high", "low", "close")):
            high = Decimal(numeric_values["high"])
            low = Decimal(numeric_values["low"])
            open_value = Decimal(numeric_values["open"])
            close = Decimal(numeric_values["close"])
            geometry_ok = high >= low and low <= open_value <= high and low <= close <= high
            if not geometry_ok:
                invalid_high_low_count += 1
        if "volume" in numeric_values:
            volume_ok = Decimal(numeric_values["volume"]) >= 0
            if not volume_ok:
                invalid_volume_count += 1
        elif ohlcv_map.get("volume") is not None:
            invalid_volume_count += 1
            volume_ok = False

        if timestamp and len(numeric_values) == len(OHLCV_COLUMNS) and geometry_ok and volume_ok:
            valid_ohlcv_count += 1
            ohlcv_by_timestamp[timestamp] = tuple(numeric_values[column] for column in OHLCV_COLUMNS)
            annotations_by_timestamp[timestamp] = {
                column: str(row.get(column, "")).strip()
                for column in annotation_columns
                if str(row.get(column, "")).strip()
            }

    timezone_information = "NO_VALID_TIMESTAMPS"
    if len(timezone_states) == 1:
        timezone_information = next(iter(timezone_states))
    elif len(timezone_states) > 1:
        timezone_information = "MIXED_TIMEZONE_AWARENESS"
        errors.append("TIMESTAMP_NORMALIZATION_CONFLICT")
    if duplicate_timestamp_count:
        errors.append("DUPLICATE_TIMESTAMPS")
    if non_monotonic_timestamp_count:
        errors.append("NON_MONOTONIC_TIMESTAMPS")

    median_interval, irregular_interval_count, interval_compatible = _interval_summary(timestamp_keys)
    earliest = min(timestamp_keys) if timestamp_keys else None
    latest = max(timestamp_keys) if timestamp_keys else None
    identity_status = "VALID" if not any(error in errors for error in ("IDENTITY_INVALID", "SOURCE_PATH_UNSAFE")) else "INVALID"
    safe_source_classification = "CANONICAL_ANNOTATED" if _is_canonical_dataset_file(source) else "NON_CANONICAL"
    if adjustment == CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN:
        warnings.append(CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN)

    return SourceInventory(
        canonical_ticker=ticker or "UNKNOWN",
        canonical_timeframe=timeframe or "unknown",
        safe_relative_reference=ref,
        file_sha256=file_digest,
        byte_size=byte_size,
        schema_columns=columns,
        row_count=len(rows),
        valid_ohlcv_count=valid_ohlcv_count,
        earliest_timestamp=earliest,
        latest_timestamp=latest,
        timezone_information=timezone_information,
        duplicate_timestamp_count=duplicate_timestamp_count,
        non_monotonic_timestamp_count=non_monotonic_timestamp_count,
        missing_ohlcv_count=missing_ohlcv_count,
        non_finite_ohlcv_count=non_finite_ohlcv_count,
        invalid_high_low_geometry_count=invalid_high_low_count,
        invalid_volume_count=invalid_volume_count,
        annotation_column_set=tuple(sorted(annotation_columns)),
        explicit_provenance_metadata=dict(sorted(provenance.items())),
        explicit_corporate_action_adjustment_status=adjustment,
        safe_source_classification=safe_source_classification,
        median_interval=median_interval,
        irregular_interval_count=irregular_interval_count,
        timeframe_interval_compatible=interval_compatible,
        identity_status=identity_status,
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
        _ohlcv_by_timestamp=ohlcv_by_timestamp,
        _annotations_by_timestamp=annotations_by_timestamp,
    )


def build_inventory(repo_root: str | Path, roots: list[str | Path] | None = None) -> list[SourceInventory]:
    return [inspect_source(path, repo_root) for path in discover_canonical_sources(repo_root, roots)]


def duplicate_count_summary(sources: list[SourceInventory]) -> dict[str, int]:
    groups: dict[tuple[str, str], int] = {}
    for source in sources:
        identity = (source.canonical_ticker, source.canonical_timeframe)
        groups[identity] = groups.get(identity, 0) + 1
    duplicate_groups = [count for count in groups.values() if count > 1]
    return {
        "total_dataset_file_count": len(sources),
        "unique_ticker_timeframe_identity_count": len(groups),
        "duplicate_identity_count": len(duplicate_groups),
        "total_files_inside_duplicate_groups": sum(duplicate_groups),
        "excess_duplicate_file_count": sum(count - 1 for count in duplicate_groups),
    }


def _core_schema_ok(source: SourceInventory) -> bool:
    if source.errors and any(error in source.errors for error in ("CSV_PARSE_FAILED", "TIMESTAMP_COLUMN_MISSING", "OHLCV_COLUMNS_MISSING")):
        return False
    return all(_column_lookup(source.schema_columns, column) for column in OHLCV_COLUMNS)


def _chronology_error(source: SourceInventory) -> bool:
    return any(
        error in source.errors
        for error in (
            "DUPLICATE_TIMESTAMPS",
            "NON_MONOTONIC_TIMESTAMPS",
            "TIMESTAMP_NORMALIZATION_CONFLICT",
        )
    )


def compare_source_pair(a: SourceInventory, b: SourceInventory) -> dict[str, Any]:
    a_timestamps = set(a._ohlcv_by_timestamp)
    b_timestamps = set(b._ohlcv_by_timestamp)
    shared = sorted(a_timestamps & b_timestamps)
    conflicts = [timestamp for timestamp in shared if a._ohlcv_by_timestamp[timestamp] != b._ohlcv_by_timestamp[timestamp]]
    annotation_diffs = [
        timestamp
        for timestamp in shared
        if a._annotations_by_timestamp.get(timestamp, {}) != b._annotations_by_timestamp.get(timestamp, {})
    ]
    if a_timestamps == b_timestamps:
        coverage = "SAME_COVERAGE"
    elif a_timestamps < b_timestamps:
        coverage = "A_STRICT_SUBSET_OF_B"
    elif a_timestamps > b_timestamps:
        coverage = "A_STRICT_SUPERSET_OF_B"
    elif shared:
        coverage = "OVERLAPPING"
    else:
        coverage = "DISJOINT"
    return {
        "a_ref": a.safe_relative_reference,
        "b_ref": b.safe_relative_reference,
        "exact_byte_duplicate": a.file_sha256 == b.file_sha256,
        "shared_timestamp_count": len(shared),
        "a_only_timestamp_count": len(a_timestamps - b_timestamps),
        "b_only_timestamp_count": len(b_timestamps - a_timestamps),
        "conflicting_shared_ohlcv_row_count": len(conflicts),
        "first_conflicting_timestamp": conflicts[0] if conflicts else None,
        "last_conflicting_timestamp": conflicts[-1] if conflicts else None,
        "common_start": shared[0] if shared else None,
        "common_end": shared[-1] if shared else None,
        "coverage_relationship": coverage,
        "annotation_difference_count": len(annotation_diffs),
    }


def _provenance_conflict(sources: list[SourceInventory]) -> bool:
    metadata = {
        (
            tuple(sorted(source.explicit_provenance_metadata.items())),
            source.explicit_corporate_action_adjustment_status,
        )
        for source in sources
        if source.explicit_provenance_metadata
        or source.explicit_corporate_action_adjustment_status != CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN
    }
    return len(metadata) > 1


def _classification_recommendation(classification: str) -> str:
    if classification in {EXACT_BYTE_DUPLICATES, SEMANTICALLY_IDENTICAL}:
        return SAFE_REDUNDANCY_REVIEW
    if classification == SAME_OHLCV_DIFFERENT_ANNOTATIONS:
        return REANNOTATION_RECOMMENDED
    if classification in {STRICT_SUPERSET_COMPATIBLE, STRICT_SUBSET_COMPATIBLE, OVERLAPPING_COMPATIBLE, DISJOINT_HISTORY_SAME_IDENTITY}:
        return MANUAL_MERGE_REVIEW_REQUIRED
    if classification == PROVENANCE_CONFLICT:
        return PROVENANCE_CONFIRMATION_REQUIRED
    if classification in {SCHEMA_DIVERGENT, TIMESTAMP_NORMALIZATION_CONFLICT, OVERLAPPING_CONFLICTING}:
        return NO_SAFE_REMEDIATION_IDENTIFIED
    return MANUAL_CANONICAL_SELECTION_REQUIRED


def classify_duplicate_group(sources: list[SourceInventory]) -> dict[str, Any]:
    ordered = sorted(sources, key=lambda item: item.safe_relative_reference)
    if len(ordered) < 2:
        return {
            "classification": UNCLASSIFIED_REVIEW_REQUIRED,
            "recommendation": MANUAL_CANONICAL_SELECTION_REQUIRED,
            "pairwise_comparisons": [],
        }
    pairwise = [
        compare_source_pair(ordered[index], ordered[other])
        for index in range(len(ordered))
        for other in range(index + 1, len(ordered))
    ]
    if any(source.identity_status != "VALID" for source in ordered):
        classification = IDENTITY_INVALID
    elif not all(_core_schema_ok(source) for source in ordered):
        classification = SCHEMA_DIVERGENT
    elif any(_chronology_error(source) for source in ordered):
        classification = TIMESTAMP_NORMALIZATION_CONFLICT
    elif all(pair["exact_byte_duplicate"] for pair in pairwise):
        classification = EXACT_BYTE_DUPLICATES
    elif len({source.timezone_information for source in ordered}) > 1:
        classification = TIMESTAMP_NORMALIZATION_CONFLICT
    elif _provenance_conflict(ordered):
        classification = PROVENANCE_CONFLICT
    elif any(pair["conflicting_shared_ohlcv_row_count"] for pair in pairwise):
        classification = OVERLAPPING_CONFLICTING
    elif all(pair["coverage_relationship"] == "SAME_COVERAGE" for pair in pairwise):
        if any(pair["annotation_difference_count"] for pair in pairwise):
            classification = SAME_OHLCV_DIFFERENT_ANNOTATIONS
        else:
            classification = SEMANTICALLY_IDENTICAL
    elif any(pair["coverage_relationship"] == "DISJOINT" for pair in pairwise):
        classification = DISJOINT_HISTORY_SAME_IDENTITY
    elif all(pair["coverage_relationship"] in {"A_STRICT_SUBSET_OF_B", "A_STRICT_SUPERSET_OF_B", "SAME_COVERAGE"} for pair in pairwise):
        relationships = {pair["coverage_relationship"] for pair in pairwise}
        classification = STRICT_SUPERSET_COMPATIBLE if "A_STRICT_SUPERSET_OF_B" in relationships and "A_STRICT_SUBSET_OF_B" not in relationships else STRICT_SUBSET_COMPATIBLE
    elif all(pair["coverage_relationship"] in {"OVERLAPPING", "A_STRICT_SUBSET_OF_B", "A_STRICT_SUPERSET_OF_B", "SAME_COVERAGE"} for pair in pairwise):
        classification = OVERLAPPING_COMPATIBLE
    else:
        classification = UNCLASSIFIED_REVIEW_REQUIRED
    return {
        "classification": classification,
        "recommendation": _classification_recommendation(classification),
        "pairwise_comparisons": pairwise,
    }


def group_sources_by_identity(sources: list[SourceInventory]) -> dict[tuple[str, str], list[SourceInventory]]:
    groups: dict[tuple[str, str], list[SourceInventory]] = {}
    for source in sources:
        groups.setdefault((source.canonical_ticker, source.canonical_timeframe), []).append(source)
    return dict(sorted(groups.items()))


def _compatible_union_rows(sources: list[SourceInventory], classification: str) -> tuple[int | str, bool]:
    if classification not in {
        EXACT_BYTE_DUPLICATES,
        SEMANTICALLY_IDENTICAL,
        SAME_OHLCV_DIFFERENT_ANNOTATIONS,
        STRICT_SUPERSET_COMPATIBLE,
        STRICT_SUBSET_COMPATIBLE,
        OVERLAPPING_COMPATIBLE,
    }:
        return REVIEW_REQUIRED, False
    timestamps: set[str] = set()
    for source in sources:
        timestamps.update(source._ohlcv_by_timestamp)
    requires_merge_review = classification in {STRICT_SUPERSET_COMPATIBLE, STRICT_SUBSET_COMPATIBLE, OVERLAPPING_COMPATIBLE}
    return len(timestamps), requires_merge_review


def analyze_history_depth(sources: list[SourceInventory]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (ticker, timeframe), group in group_sources_by_identity(sources).items():
        duplicate_info = classify_duplicate_group(group) if len(group) > 1 else {
            "classification": "SINGLE_SOURCE",
            "recommendation": MANUAL_CANONICAL_SELECTION_REQUIRED,
            "pairwise_comparisons": [],
        }
        classification = duplicate_info["classification"]
        safe_sources = [source for source in group if not source.errors]
        largest = max((source.valid_ohlcv_count for source in safe_sources), default=0)
        smallest = min((source.valid_ohlcv_count for source in safe_sources), default=0)
        earliest = min((source.earliest_timestamp for source in group if source.earliest_timestamp), default=None)
        latest = max((source.latest_timestamp for source in group if source.latest_timestamp), default=None)
        if len(group) == 1:
            potential_union: int | str = NOT_APPLICABLE
            requires_merge = False
        else:
            potential_union, requires_merge = _compatible_union_rows(safe_sources, classification)
        for profile, requirement in FIXED_PROFILE_REQUIREMENTS.items():
            if timeframe != requirement["timeframe"]:
                continue
            required = int(requirement["required_rows"])
            estimated_shortfall = max(required - largest, 0)
            if isinstance(potential_union, int):
                potential_shortfall: int | str = max(required - potential_union, 0)
            elif len(group) == 1:
                potential_shortfall = NOT_APPLICABLE
            else:
                potential_shortfall = REVIEW_REQUIRED
            status = "READY_PENDING_CANONICAL_APPROVAL"
            if any(source.errors for source in group):
                status = "DATASET_INVALID"
            elif classification in {OVERLAPPING_CONFLICTING, SCHEMA_DIVERGENT, TIMESTAMP_NORMALIZATION_CONFLICT}:
                status = "CONFLICT_REVIEW_REQUIRED"
            elif classification == PROVENANCE_CONFLICT:
                status = "PROVENANCE_REQUIRED"
            elif len(group) > 1:
                status = "DUPLICATE_REVIEW_REQUIRED"
            elif any(source.explicit_corporate_action_adjustment_status == CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN for source in group):
                status = "PROVENANCE_REQUIRED"
            if estimated_shortfall and status == "READY_PENDING_CANONICAL_APPROVAL":
                status = "INSUFFICIENT_HISTORY"
            rows.append(
                {
                    "ticker": ticker,
                    "timeframe": timeframe,
                    "profile": profile,
                    "best_valid_single_source_rows": largest,
                    "approved_canonical_safe_rows": NOT_ESTABLISHED,
                    "largest_valid_row_count_from_one_source": largest,
                    "smallest_valid_row_count": smallest,
                    "earliest_available_timestamp": earliest,
                    "latest_available_timestamp": latest,
                    "potential_compatible_union_rows": potential_union,
                    "compatible_union_requires_manual_merge_review": requires_merge,
                    "required_rows": required,
                    "estimated_shortfall_from_best_single_source": estimated_shortfall,
                    "potential_shortfall_after_approved_union": potential_shortfall,
                    "duplicate_classification": classification,
                    "data_readiness_status": status,
                }
            )
    return sorted(rows, key=lambda item: (item["profile"], item["ticker"], item["timeframe"]))


def build_acquisition_requirements(history_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    requirements: list[dict[str, Any]] = []
    for row in history_rows:
        if int(row["estimated_shortfall_from_best_single_source"]) <= 0:
            continue
        requirements.append(
            {
                "ticker": row["ticker"],
                "timeframe": row["timeframe"],
                "profile": row["profile"],
                "required_minimum_rows": row["required_rows"],
                "best_valid_single_source_rows": row["best_valid_single_source_rows"],
                "approved_canonical_safe_rows": row["approved_canonical_safe_rows"],
                "estimated_shortfall_from_best_single_source": row["estimated_shortfall_from_best_single_source"],
                "earliest_current_timestamp": row["earliest_available_timestamp"],
                "latest_current_timestamp": row["latest_available_timestamp"],
                "adjustment_provenance_requirement": "EXPLICIT_STATUS_REQUIRED",
                "provider_source_provenance_requirement": "EXPLICIT_PROVENANCE_REQUIRED",
                "desired_fixed_end_date_status": HUMAN_APPROVAL_REQUIRED,
                "desired_fixed_start_date_status": HUMAN_APPROVAL_REQUIRED,
                "acquisition_status": HUMAN_APPROVAL_REQUIRED,
                "contract": "ROW_GATED_NOT_PERIOD_STRING_GATED",
            }
        )
    return requirements


def build_reannotation_requirements(sources: list[SourceInventory]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    required_columns = {"wyckoff_phase", "tr_low", "tr_high"}
    for source in sources:
        annotation_columns = set(source.annotation_column_set)
        stale_prevents_use = not required_columns.issubset(annotation_columns)
        rows.append(
            {
                "ticker": source.canonical_ticker,
                "timeframe": source.canonical_timeframe,
                "safe_relative_reference": source.safe_relative_reference,
                "annotation_version": source.explicit_provenance_metadata.get("schema_version", "UNKNOWN"),
                "required_current_columns": sorted(required_columns),
                "current_candidate_builder_compatibility": "REVIEW_REQUIRED",
                "stale_annotations_prevent_canonical_use": stale_prevents_use,
                "deterministic_reannotation_feasible_later": True,
            }
        )
    return rows


def _duplicate_groups_report(sources: list[SourceInventory]) -> list[dict[str, Any]]:
    groups = group_sources_by_identity(sources)
    report: list[dict[str, Any]] = []
    for (ticker, timeframe), group in groups.items():
        if len(group) < 2:
            continue
        classification = classify_duplicate_group(group)
        report.append(
            {
                "ticker": ticker,
                "timeframe": timeframe,
                "file_count": len(group),
                "classification": classification["classification"],
                "recommendation": classification["recommendation"],
                "safe_relative_references": [source.safe_relative_reference for source in sorted(group, key=lambda item: item.safe_relative_reference)],
                "file_sha256_values": [source.file_sha256 for source in sorted(group, key=lambda item: item.safe_relative_reference)],
                "pairwise_comparisons": classification["pairwise_comparisons"],
            }
        )
    return report


def _classification_summary(groups: list[dict[str, Any]]) -> dict[str, int]:
    counts = {classification: 0 for classification in DUPLICATE_CLASSIFICATIONS}
    for group in groups:
        classification = group["classification"]
        counts[classification] = counts.get(classification, 0) + 1
    return {key: value for key, value in counts.items() if value}


def _git_commit(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "UNKNOWN"
    return result.stdout.strip()


def build_remediation_report(
    repo_root: str | Path,
    roots: list[str | Path] | None = None,
    *,
    generated_at: str | None = None,
    code_commit: str | None = None,
) -> dict[str, Any]:
    root = _repo_root(repo_root)
    sources = build_inventory(root, roots)
    duplicate_groups = _duplicate_groups_report(sources)
    history = analyze_history_depth(sources)
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "module_version": MODULE_VERSION,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "code_commit": code_commit or _git_commit(root),
        "count_summary": duplicate_count_summary(sources),
        "source_inventory": [source.public_dict() for source in sorted(sources, key=lambda item: item.safe_relative_reference)],
        "duplicate_groups": duplicate_groups,
        "duplicate_classification_summary": _classification_summary(duplicate_groups),
        "history_depth": history,
        "acquisition_requirements": build_acquisition_requirements(history),
        "reannotation_requirements": build_reannotation_requirements(sources),
        "unresolved_decisions": [
            {
                "ticker": group["ticker"],
                "timeframe": group["timeframe"],
                "decision_status": "PENDING_OPERATOR_REVIEW",
                "duplicate_classification": group["classification"],
            }
            for group in duplicate_groups
        ],
        "blockers": [
            "NO_AUTOMATIC_CANONICAL_SOURCE_SELECTION",
            "HUMAN_DECISION_REGISTER_REQUIRED",
            "PROVENANCE_AND_ADJUSTMENT_REVIEW_REQUIRED",
            "ADDITIONAL_HISTORY_REQUIRED_FOR_BLOCKED_FIXED_PROFILES",
        ],
        "no_performance_inspected": True,
        "forbidden_operations": {
            "source_dataset_modified": False,
            "source_dataset_deleted": False,
            "source_dataset_merged": False,
            "provider_invoked": False,
            "candidate_builder_invoked": False,
            "monte_carlo_invoked": False,
            "outcome_evaluator_invoked": False,
            "performance_metrics_calculated": False,
            "canonical_source_auto_approved": False,
        },
    }
    semantic_payload = {key: value for key, value in report.items() if key not in {"generated_at", "report_semantic_sha256"}}
    report["report_semantic_sha256"] = semantic_digest(semantic_payload)
    return report


def write_report(report: dict[str, Any], output_path: str | Path, repo_root: str | Path) -> Path:
    root = _repo_root(repo_root)
    path = Path(output_path)
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve(strict=False)
    allowed_root = (root / ".marketflow" / "data_readiness").resolve(strict=False)
    try:
        resolved.relative_to(allowed_root)
    except ValueError as exc:
        raise ValueError("data readiness report output must stay under .marketflow/data_readiness") from exc
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_bytes(canonical_json_bytes(report))
    return resolved


def load_registry(path: str | Path) -> dict[str, Any]:
    with Path(path).open("rb") as handle:
        return tomllib.load(handle)


def source_semantic_ohlcv_digest(source: SourceInventory) -> str:
    payload = {
        "canonical_ticker": source.canonical_ticker,
        "canonical_timeframe": source.canonical_timeframe,
        "ohlcv_by_timestamp": [
            {"timestamp": timestamp, "ohlcv": list(values)}
            for timestamp, values in sorted(source._ohlcv_by_timestamp.items())
        ],
    }
    return semantic_digest(payload)


def _is_hex_sha256(value: object) -> bool:
    text = str(value)
    return len(text) == 64 and all(char in "0123456789abcdef" for char in text.lower())


def _is_hex_commit(value: object) -> bool:
    text = str(value)
    return len(text) == 40 and all(char in "0123456789abcdef" for char in text.lower())


def _is_timezone_aware_timestamp(value: object) -> bool:
    try:
        timestamp = pd.Timestamp(str(value))
    except (TypeError, ValueError):
        return False
    return not pd.isna(timestamp) and timestamp.tzinfo is not None


def _pending_or_unknown(value: object) -> bool:
    text = str(value).strip().upper()
    return text in {
        "",
        "UNKNOWN",
        "PENDING",
        "PENDING_REVIEW",
        "HUMAN_APPROVAL_REQUIRED",
        CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN,
    }


def _decision_identity_valid(value: object) -> bool:
    if not isinstance(value, dict) or set(value) != {"ticker", "timeframe"}:
        return False
    ticker = str(value.get("ticker") or "").strip()
    timeframe = str(value.get("timeframe") or "").strip().lower()
    return bool(ticker) and ticker == ticker.upper() and timeframe in SUPPORTED_TIMEFRAMES


def validate_registry(registry: dict[str, Any], repo_root: str | Path) -> dict[str, Any]:
    errors: list[str] = []
    if set(registry) != {"schema_version", "records"}:
        errors.append("REGISTRY_UNKNOWN_OR_MISSING_TOP_LEVEL_FIELD")
    if registry.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        errors.append("REGISTRY_SCHEMA_VERSION_INVALID")
    records = registry.get("records")
    if not isinstance(records, list):
        return {"success": False, "errors": [*errors, "REGISTRY_RECORDS_INVALID"]}
    approved_by_identity: set[tuple[str, str]] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"REGISTRY_RECORD_INVALID:{index}")
            continue
        keys = set(record)
        if keys != REGISTRY_REQUIRED_FIELDS:
            errors.append(f"REGISTRY_RECORD_FIELD_SET_INVALID:{index}")
            continue
        identity = (str(record["canonical_ticker"]).upper(), str(record["canonical_timeframe"]).lower())
        status = record["status"]
        if status not in REGISTRY_STATUSES:
            errors.append(f"REGISTRY_STATUS_INVALID:{index}")
        ref = record["approved_safe_relative_source_reference"]
        if ref and not _is_relative_safe_ref(ref):
            errors.append(f"REGISTRY_SOURCE_REF_UNSAFE:{index}")
        superseded_refs = record["superseded_source_references"]
        if not isinstance(superseded_refs, list):
            errors.append(f"REGISTRY_SUPERSEDED_REFS_INVALID:{index}")
        else:
            for ref_index, superseded_ref in enumerate(superseded_refs):
                if not _is_relative_safe_ref(superseded_ref):
                    errors.append(f"REGISTRY_SUPERSEDED_SOURCE_REF_UNSAFE:{index}:{ref_index}")
        if status == "APPROVED":
            if identity in approved_by_identity:
                errors.append(f"REGISTRY_DUPLICATE_APPROVED_IDENTITY:{identity[0]}:{identity[1]}")
            approved_by_identity.add(identity)
            if _pending_or_unknown(record["provenance_status"]):
                errors.append(f"REGISTRY_APPROVED_PROVENANCE_INCOMPLETE:{index}")
            if _pending_or_unknown(record["adjustment_status"]):
                errors.append(f"REGISTRY_APPROVED_ADJUSTMENT_INCOMPLETE:{index}")
            if _pending_or_unknown(record["approval_evidence_category"]):
                errors.append(f"REGISTRY_APPROVED_EVIDENCE_CATEGORY_INCOMPLETE:{index}")
            if _pending_or_unknown(record["decision_id"]):
                errors.append(f"REGISTRY_APPROVED_DECISION_ID_INCOMPLETE:{index}")
            if not _is_timezone_aware_timestamp(record["decision_timestamp"]):
                errors.append(f"REGISTRY_APPROVED_DECISION_TIMESTAMP_INVALID:{index}")
            digest = record["approved_file_sha256"]
            semantic_ohlcv_digest = record["approved_semantic_ohlcv_digest"]
            if not ref:
                errors.append(f"REGISTRY_APPROVED_SOURCE_REF_MISSING:{index}")
                continue
            if not _is_hex_sha256(digest):
                errors.append(f"REGISTRY_APPROVED_SOURCE_DIGEST_INVALID:{index}")
            if not _is_hex_sha256(semantic_ohlcv_digest):
                errors.append(f"REGISTRY_APPROVED_SEMANTIC_DIGEST_INVALID:{index}")
            try:
                source = _resolve_safe_ref(repo_root, ref)
            except ValueError:
                errors.append(f"REGISTRY_SOURCE_REF_UNSAFE:{index}")
                continue
            if not source.is_file():
                errors.append(f"REGISTRY_APPROVED_SOURCE_MISSING:{index}")
                continue
            actual = sha256_bytes(source.read_bytes())
            if actual != digest:
                errors.append(f"REGISTRY_APPROVED_SOURCE_DIGEST_MISMATCH:{index}")
            inspected = inspect_source(source, repo_root)
            if inspected.errors:
                errors.append(f"REGISTRY_APPROVED_SOURCE_INVALID:{index}")
            elif _is_hex_sha256(semantic_ohlcv_digest) and source_semantic_ohlcv_digest(inspected) != semantic_ohlcv_digest:
                errors.append(f"REGISTRY_APPROVED_SEMANTIC_DIGEST_MISMATCH:{index}")
    return {"success": not errors, "errors": errors}


def _performance_rationale_forbidden(value: object) -> bool:
    text = str(value).upper().replace(" ", "_")
    return text in FORBIDDEN_RATIONALE_CATEGORIES or any(fragment in text for fragment in FORBIDDEN_RATIONALE_FRAGMENTS)


def validate_decision_register_append_only(
    existing: dict[str, Any],
    proposed: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if proposed.get("schema_version") != DECISION_REGISTER_SCHEMA_VERSION:
        errors.append("DECISION_REGISTER_SCHEMA_VERSION_INVALID")
    if set(proposed) != {"schema_version", "decisions"}:
        errors.append("DECISION_REGISTER_FIELD_SET_INVALID")
    existing_rows = existing.get("decisions") or []
    proposed_rows = proposed.get("decisions") or []
    if not isinstance(existing_rows, list) or not isinstance(proposed_rows, list):
        return {"success": False, "errors": [*errors, "DECISION_ROWS_INVALID"]}
    if len(proposed_rows) < len(existing_rows):
        errors.append("DECISION_REGISTER_DELETION_NOT_ALLOWED")
    for index, row in enumerate(existing_rows):
        if index >= len(proposed_rows) or proposed_rows[index] != row:
            errors.append("DECISION_REGISTER_RETROACTIVE_EDIT_NOT_ALLOWED")
            break
    seen_ids: set[str] = set()
    for index, row in enumerate(proposed_rows):
        if not isinstance(row, dict):
            errors.append(f"DECISION_ROW_INVALID:{index}")
            continue
        if set(row) != DECISION_REQUIRED_FIELDS:
            errors.append(f"DECISION_FIELD_SET_INVALID:{index}")
            continue
        decision_id = str(row["decision_id"])
        if not decision_id or decision_id in seen_ids:
            errors.append(f"DECISION_ID_INVALID:{index}")
        seen_ids.add(decision_id)
        if row["decision_status"] not in DECISION_STATUSES:
            errors.append(f"DECISION_STATUS_INVALID:{index}")
        if row["duplicate_classification"] not in DUPLICATE_CLASSIFICATIONS:
            errors.append(f"DECISION_DUPLICATE_CLASSIFICATION_INVALID:{index}")
        if _performance_rationale_forbidden(row["rationale_category"]):
            errors.append(f"DECISION_PERFORMANCE_RATIONALE_FORBIDDEN:{index}")
        selected = row["selected_canonical_source"]
        if selected not in (None, "") and not _is_relative_safe_ref(selected):
            errors.append(f"DECISION_SELECTED_SOURCE_REF_UNSAFE:{index}")
        if row["decision_status"] == "APPROVED":
            if not _decision_identity_valid(row["identity"]):
                errors.append(f"DECISION_APPROVED_IDENTITY_INVALID:{index}")
            source_digests = row["examined_source_digests"]
            if not isinstance(source_digests, list) or not source_digests or not all(_is_hex_sha256(item) for item in source_digests):
                errors.append(f"DECISION_APPROVED_SOURCE_DIGESTS_INVALID:{index}")
            if not _is_timezone_aware_timestamp(row["evidence_timestamp"]):
                errors.append(f"DECISION_APPROVED_EVIDENCE_TIMESTAMP_INVALID:{index}")
            if not _is_hex_commit(row["code_commit"]):
                errors.append(f"DECISION_APPROVED_CODE_COMMIT_INVALID:{index}")
            if selected in (None, ""):
                errors.append(f"DECISION_APPROVED_SOURCE_REQUIRED:{index}")
            if row["operator_approval_status"] != "APPROVED":
                errors.append(f"DECISION_OPERATOR_APPROVAL_REQUIRED:{index}")
    return {"success": not errors, "errors": errors}


def summarize_for_cli(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": report["schema_version"],
        "count_summary": report["count_summary"],
        "duplicate_classification_summary": report["duplicate_classification_summary"],
        "history_depth": report["history_depth"],
        "report_semantic_sha256": report["report_semantic_sha256"],
        "no_performance_inspected": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build read-only MarketFlow data-readiness remediation report.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument(
        "--report-output",
        default=".marketflow/data_readiness/data_readiness_remediation_report.json",
        help="Ignored local report path under .marketflow/data_readiness.",
    )
    args = parser.parse_args(argv)
    report = build_remediation_report(args.repo_root)
    output = write_report(report, args.report_output, args.repo_root)
    summary = summarize_for_cli(report)
    summary["report_ref"] = safe_relative_reference(output, args.repo_root)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
