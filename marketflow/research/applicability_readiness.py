"""No-peek swing applicability readiness inventory and protocol helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import pandas as pd


MANIFEST_SCHEMA_VERSION = "marketflow_swing_dataset_manifest_v1"
PROTOCOL_SCHEMA_VERSION = "marketflow_swing_research_protocol_v1"
TRIAL_LEDGER_SCHEMA_VERSION = "marketflow_trial_ledger_policy_v1"
PROTOCOL_STATUS_PROPOSED_WITH_BLOCKERS = "PROTOCOL_PROPOSED_WITH_BLOCKERS"
ADJUSTMENT_STATUS_UNKNOWN = "CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN"

TARGET_TIMEFRAMES = ("4h", "1d", "1w")
SUPPORTING_TIMEFRAMES = ("1h",)
ALL_RESEARCH_TIMEFRAMES = (*TARGET_TIMEFRAMES, *SUPPORTING_TIMEFRAMES)
TIMEFRAME_BARS_PER_DAY = {"1h": 6.5, "4h": 2.0, "1d": 1.0, "1w": 0.2}
CANONICAL_SUFFIX = "_wyckoff_annotated.csv"
DERIVATIVE_MARKERS = (
    "_pv_eigen.csv",
    "_backtest_candidates",
    "_backtest_results",
    "_walk_forward_cases_",
    "_walk_forward_results_",
    "_walk_forward_summary_",
    "_walk_forward_campaign_",
    "_walk_forward_run_registry",
)
REQUIRED_OHLC = ("open", "high", "low", "close")
VOLUME_COLUMNS = ("volume", "Volume")
TIMESTAMP_COLUMNS = ("timestamp", "datetime", "date", "time", "Date", "Datetime")
WYCKOFF_COLUMNS = ("wyckoff_phase", "phase", "wyckoff_confirmed_event", "confirmed_event")
TR_COLUMNS = ("tr_low", "tr_high")
CONFIRMED_EVENT_MARKER_COLUMNS = (
    "wyckoff_confirmed_event_occurrence",
    "confirmed_event_occurrence",
    "event_occurrence",
)
REQUIRED_TRIAL_FIELDS = (
    "trial_id",
    "protocol_generation",
    "code_commit",
    "data_manifest_digest",
    "candidate_builder_version",
    "strategy_config_digest",
    "profile",
    "universe_split",
    "temporal_split",
    "horizon",
    "baseline_definitions",
    "cost_assumptions",
    "random_seeds",
    "metrics_requested",
    "status",
    "holdout_touched",
    "follow_up_reason",
)

PROFILE_DEFINITIONS = {
    "SWING": {
        "decision_timeframe": "4h",
        "primary_horizon_bars": 10,
        "secondary_horizon_bars": [5, 15],
        "minimum_rows": 360,
        "minimum_split_rows": 120,
        "approximate_holding_period": "several trading days",
    },
    "POSITION_SWING": {
        "decision_timeframe": "1d",
        "primary_horizon_bars": 20,
        "secondary_horizon_bars": [10, 40],
        "minimum_rows": 500,
        "minimum_split_rows": 160,
        "approximate_holding_period": "several days to several weeks",
    },
}


@dataclass(frozen=True)
class DatasetInventoryRow:
    ticker: str
    timeframe: str
    relative_path: str
    earliest_timestamp: str | None
    latest_timestamp: str | None
    total_row_count: int
    valid_ohlcv_row_count: int
    duplicate_timestamp_count: int
    non_monotonic_timestamp_count: int
    missing_required_ohlcv_count: int
    missing_or_invalid_volume_count: int
    invalid_high_low_geometry_count: int
    timezone_awareness: str
    median_observed_interval: str | None
    interval_irregularity_count: int
    volume_available: bool
    wyckoff_annotations_available: bool
    tr_levels_available: bool
    confirmed_event_occurrence_markers_available: bool
    corporate_action_adjustment_status: str
    source_provenance: str | None
    schema_version: str | None
    status: str
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, TypeError, ValueError):
            pass
    if value is None:
        return None
    try:
        missing = pd.isna(value)
    except (TypeError, ValueError):
        missing = False
    if isinstance(missing, bool) and missing:
        return None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if hasattr(value, "isoformat") and not isinstance(value, (str, bytes, bytearray)):
        try:
            return value.isoformat()
        except (AttributeError, TypeError, ValueError):
            pass
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def canonical_json_bytes(payload: dict[str, Any] | list[Any]) -> bytes:
    return json.dumps(_json_safe(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_digest(payload: dict[str, Any] | list[Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def safe_relative_path(path: str | Path, repo_root: str | Path) -> str:
    root = Path(repo_root).resolve()
    resolved = Path(path).resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("path must stay inside repository root") from exc
    return relative.as_posix()


def infer_ticker_timeframe(path: str | Path) -> tuple[str | None, str | None]:
    stem = Path(path).stem.replace("-", "_")
    tokens = [token for token in stem.split("_") if token]
    timeframe_matches = [
        (index, token.lower())
        for index, token in enumerate(tokens)
        if token.lower() in {"1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"}
    ]
    if len(timeframe_matches) > 1:
        first_index = timeframe_matches[0][0]
        ticker = "_".join(tokens[:first_index]).upper() if first_index else None
        return ticker, "ambiguous"
    if len(timeframe_matches) == 1:
        index, timeframe = timeframe_matches[0]
        ticker = "_".join(tokens[:index]).upper() if index else None
        return ticker, timeframe
    return (tokens[0].upper() if tokens else None), None


def _filename_timeframe_tokens(path: str | Path) -> set[str]:
    stem = Path(path).stem.replace("-", "_").lower()
    tokens = {token for token in stem.split("_") if token}
    return tokens.intersection({"1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"})


def _is_inside_repo(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _is_ignored_manifest_output(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    research_root = (root.resolve() / ".marketflow" / "research").resolve()
    try:
        resolved.relative_to(research_root)
        return True
    except ValueError:
        return False


def is_canonical_research_dataset(path: str | Path) -> bool:
    name = Path(path).name.lower()
    return name.endswith(CANONICAL_SUFFIX) and not any(marker in name for marker in DERIVATIVE_MARKERS)


def discover_canonical_datasets(repo_root: str | Path, roots: list[str | Path] | None = None) -> list[Path]:
    root = Path(repo_root).resolve()
    search_roots = roots or [root / ".marketflow" / "reports", root / "data"]
    paths: list[Path] = []
    for search_root in search_roots:
        candidate_root = Path(search_root)
        if not candidate_root.is_absolute():
            candidate_root = root / candidate_root
        candidate_root = candidate_root.resolve()
        try:
            candidate_root.relative_to(root)
        except ValueError as exc:
            raise ValueError("scan root must stay inside repository root") from exc
        if not candidate_root.exists() or not candidate_root.is_dir():
            continue
        for path in candidate_root.rglob("*.csv"):
            if not is_canonical_research_dataset(path):
                continue
            timeframe_tokens = _filename_timeframe_tokens(path)
            if timeframe_tokens.intersection(ALL_RESEARCH_TIMEFRAMES):
                paths.append(path)
    return sorted(paths, key=lambda item: safe_relative_path(item, root))


def _detect_timestamp_column(columns: list[str]) -> str | None:
    for candidate in TIMESTAMP_COLUMNS:
        if candidate in columns:
            return candidate
    lower = {column.lower(): column for column in columns}
    for candidate in TIMESTAMP_COLUMNS:
        match = lower.get(candidate.lower())
        if match:
            return match
    return None


def _first_existing(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    lower = {column.lower(): column for column in columns}
    for candidate in candidates:
        if candidate in columns:
            return candidate
        match = lower.get(candidate.lower())
        if match:
            return match
    return None


def _median_interval_text(timestamps: pd.Series) -> tuple[str | None, int]:
    parsed = pd.to_datetime(timestamps, errors="coerce")
    parsed = parsed.dropna().reset_index(drop=True)
    if len(parsed) < 2:
        return None, 0
    deltas = parsed.diff().dropna()
    if deltas.empty:
        return None, 0
    median = deltas.median()
    irregular = int((deltas != median).sum())
    return str(median), irregular


def inspect_dataset(path: str | Path, repo_root: str | Path) -> DatasetInventoryRow:
    source = Path(path)
    ticker, timeframe = infer_ticker_timeframe(source)
    errors: list[str] = []
    warnings: list[str] = []
    if not ticker:
        errors.append("DATASET_TICKER_IDENTITY_UNKNOWN")
        ticker = "UNKNOWN"
    if timeframe == "ambiguous":
        errors.append("DATASET_IDENTITY_AMBIGUOUS")
    elif timeframe not in ALL_RESEARCH_TIMEFRAMES:
        errors.append("DATASET_TIMEFRAME_NOT_IN_SCOPE")
        timeframe = timeframe or "unknown"
    try:
        relative_path = safe_relative_path(source, repo_root)
    except ValueError:
        relative_path = source.name
        errors.append("DATASET_PATH_OUTSIDE_REPOSITORY")
    try:
        frame = pd.read_csv(source)
    except Exception as exc:
        return DatasetInventoryRow(
            ticker=ticker,
            timeframe=timeframe,
            relative_path=relative_path,
            earliest_timestamp=None,
            latest_timestamp=None,
            total_row_count=0,
            valid_ohlcv_row_count=0,
            duplicate_timestamp_count=0,
            non_monotonic_timestamp_count=0,
            missing_required_ohlcv_count=0,
            missing_or_invalid_volume_count=0,
            invalid_high_low_geometry_count=0,
            timezone_awareness="UNKNOWN",
            median_observed_interval=None,
            interval_irregularity_count=0,
            volume_available=False,
            wyckoff_annotations_available=False,
            tr_levels_available=False,
            confirmed_event_occurrence_markers_available=False,
            corporate_action_adjustment_status=ADJUSTMENT_STATUS_UNKNOWN,
            source_provenance=None,
            schema_version=None,
            status="ineligible",
            errors=(*errors, f"DATASET_READ_FAILED:{type(exc).__name__}"),
            warnings=tuple(warnings),
        )

    columns = [str(column) for column in frame.columns]
    timestamp_column = _detect_timestamp_column(columns)
    parsed_timestamps = pd.Series(dtype="datetime64[ns]")
    earliest = None
    latest = None
    duplicate_count = 0
    non_monotonic_count = 0
    median_interval = None
    irregularity_count = 0
    timezone_awareness = "NO_TIMESTAMP_COLUMN"
    if timestamp_column is None:
        errors.append("TIMESTAMP_COLUMN_MISSING")
    else:
        parsed_timestamps = pd.to_datetime(frame[timestamp_column], errors="coerce")
        valid_timestamps = parsed_timestamps.dropna()
        if valid_timestamps.empty:
            errors.append("TIMESTAMP_VALUES_UNREADABLE")
        else:
            earliest = valid_timestamps.min().isoformat()
            latest = valid_timestamps.max().isoformat()
            duplicate_count = int(valid_timestamps.duplicated().sum())
            non_monotonic_count = int((valid_timestamps.diff().dropna() <= pd.Timedelta(0)).sum())
            median_interval, irregularity_count = _median_interval_text(valid_timestamps)
            timezone_awareness = "timezone_aware" if getattr(valid_timestamps.dt, "tz", None) is not None else "timezone_naive_or_unspecified"

    ohlc_columns = {name: _first_existing(columns, (name, name.capitalize())) for name in REQUIRED_OHLC}
    missing_ohlc_columns = [name for name, column in ohlc_columns.items() if column is None]
    if missing_ohlc_columns:
        errors.append("REQUIRED_OHLC_COLUMNS_MISSING")
    missing_required_ohlcv_count = 0
    missing_or_invalid_volume_count = 0
    invalid_geometry_count = 0
    valid_ohlcv_count = 0
    volume_column = _first_existing(columns, VOLUME_COLUMNS)
    if not missing_ohlc_columns:
        ohlc = frame[[ohlc_columns[name] for name in REQUIRED_OHLC]].apply(pd.to_numeric, errors="coerce")
        missing_required_ohlcv_count = int(ohlc.isna().any(axis=1).sum())
        invalid_geometry = (
            (ohlc[ohlc_columns["high"]] < ohlc[ohlc_columns["low"]])
            | (ohlc[ohlc_columns["open"]] > ohlc[ohlc_columns["high"]])
            | (ohlc[ohlc_columns["open"]] < ohlc[ohlc_columns["low"]])
            | (ohlc[ohlc_columns["close"]] > ohlc[ohlc_columns["high"]])
            | (ohlc[ohlc_columns["close"]] < ohlc[ohlc_columns["low"]])
        )
        invalid_geometry_count = int(invalid_geometry.fillna(True).sum())
        if volume_column is None:
            errors.append("VOLUME_COLUMN_MISSING")
            volume_valid = pd.Series(False, index=frame.index)
            missing_or_invalid_volume_count = int(len(frame))
        else:
            volume_values = pd.to_numeric(frame[volume_column], errors="coerce")
            volume_valid = volume_values.notna() & (volume_values >= 0)
            missing_or_invalid_volume_count = int((~volume_valid).sum())
        valid_ohlcv_count = int((~ohlc.isna().any(axis=1) & ~invalid_geometry.fillna(True) & volume_valid).sum())

    wyckoff_available = any(_first_existing(columns, (column,)) for column in WYCKOFF_COLUMNS)
    tr_available = all(_first_existing(columns, (column,)) for column in TR_COLUMNS)
    marker_available = any(_first_existing(columns, (column,)) for column in CONFIRMED_EVENT_MARKER_COLUMNS)
    explicit_adjustment = _first_existing(columns, ("adjustment_status", "corporate_action_adjustment_status"))
    explicit_provenance = _first_existing(columns, ("source_provenance", "provider", "data_provider"))
    explicit_schema = _first_existing(columns, ("schema_version", "manifest_schema_version"))
    adjustment_status = (
        str(frame[explicit_adjustment].dropna().iloc[0])
        if explicit_adjustment and not frame[explicit_adjustment].dropna().empty
        else ADJUSTMENT_STATUS_UNKNOWN
    )
    source_provenance = (
        str(frame[explicit_provenance].dropna().iloc[0])
        if explicit_provenance and not frame[explicit_provenance].dropna().empty
        else None
    )
    schema_version = (
        str(frame[explicit_schema].dropna().iloc[0])
        if explicit_schema and not frame[explicit_schema].dropna().empty
        else None
    )

    if duplicate_count:
        errors.append("DUPLICATE_TIMESTAMPS")
    if non_monotonic_count:
        errors.append("NON_MONOTONIC_TIMESTAMPS")
    if missing_required_ohlcv_count:
        warnings.append("MISSING_REQUIRED_OHLCV_ROWS")
    if missing_or_invalid_volume_count:
        warnings.append("MISSING_OR_INVALID_VOLUME_ROWS")
    if invalid_geometry_count:
        errors.append("INVALID_HIGH_LOW_GEOMETRY")
    status = "valid"
    if errors:
        status = "ineligible"
    elif len(frame) < 250 or missing_required_ohlcv_count:
        status = "limited"
    return DatasetInventoryRow(
        ticker=ticker,
        timeframe=timeframe,
        relative_path=relative_path,
        earliest_timestamp=earliest,
        latest_timestamp=latest,
        total_row_count=int(len(frame)),
        valid_ohlcv_row_count=valid_ohlcv_count,
        duplicate_timestamp_count=duplicate_count,
        non_monotonic_timestamp_count=non_monotonic_count,
        missing_required_ohlcv_count=missing_required_ohlcv_count,
        missing_or_invalid_volume_count=missing_or_invalid_volume_count,
        invalid_high_low_geometry_count=invalid_geometry_count,
        timezone_awareness=timezone_awareness,
        median_observed_interval=median_interval,
        interval_irregularity_count=irregularity_count,
        volume_available=volume_column is not None,
        wyckoff_annotations_available=wyckoff_available,
        tr_levels_available=tr_available,
        confirmed_event_occurrence_markers_available=marker_available,
        corporate_action_adjustment_status=adjustment_status,
        source_provenance=source_provenance,
        schema_version=schema_version,
        status=status,
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
    )


def build_dataset_manifest(repo_root: str | Path, roots: list[str | Path] | None = None) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    datasets = [inspect_dataset(path, root) for path in discover_canonical_datasets(root, roots)]
    identity_counts: dict[tuple[str, str], int] = {}
    for row in datasets:
        identity = (row.ticker, row.timeframe)
        identity_counts[identity] = identity_counts.get(identity, 0) + 1
    duplicate_identities = [
        {"ticker": ticker, "timeframe": timeframe, "count": count}
        for (ticker, timeframe), count in sorted(identity_counts.items())
        if count > 1
    ]
    manifest_errors = ["DUPLICATE_DATASET_IDENTITY"] if duplicate_identities else []
    rows = [asdict(row) for row in datasets]
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_by": "marketflow.research.applicability_readiness",
        "dataset_count": len(rows),
        "datasets": rows,
        "duplicate_identities": duplicate_identities,
        "status": "ineligible" if manifest_errors else ("valid" if rows else "empty"),
        "errors": manifest_errors,
        "warnings": [],
        "contains_performance": False,
        "contains_candidate_results": False,
    }
    manifest["manifest_digest"] = sha256_digest({key: value for key, value in manifest.items() if key != "manifest_digest"})
    return manifest


def summarize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    rows = list(manifest.get("datasets") or [])
    by_timeframe: dict[str, int] = {}
    by_status: dict[str, int] = {}
    tickers: set[str] = set()
    for row in rows:
        timeframe = str(row.get("timeframe") or "unknown")
        status = str(row.get("status") or "unknown")
        by_timeframe[timeframe] = by_timeframe.get(timeframe, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        if row.get("ticker"):
            tickers.add(str(row["ticker"]))
    return {
        "dataset_count": len(rows),
        "ticker_count": len(tickers),
        "timeframe_counts": dict(sorted(by_timeframe.items())),
        "status_counts": dict(sorted(by_status.items())),
        "duplicate_identity_count": len(manifest.get("duplicate_identities") or []),
        "manifest_status": manifest.get("status"),
    }


def _profile_row_depth_requirement(definition: dict[str, Any]) -> dict[str, int]:
    max_horizon = max([int(definition["primary_horizon_bars"]), *[int(value) for value in definition["secondary_horizon_bars"]]])
    split_floor_rows = 3 * int(definition["minimum_split_rows"])
    purge_embargo_rows = 2 * max_horizon
    structural_minimum_rows = split_floor_rows + purge_embargo_rows
    return {
        "minimum_rows": int(definition["minimum_rows"]),
        "minimum_split_rows": int(definition["minimum_split_rows"]),
        "required_split_count": 3,
        "max_horizon_bars": max_horizon,
        "purge_embargo_rows": purge_embargo_rows,
        "structural_minimum_rows": structural_minimum_rows,
        "required_valid_ohlcv_rows": max(int(definition["minimum_rows"]), structural_minimum_rows),
    }


def assess_profile_feasibility(manifest: dict[str, Any], profile_name: str) -> dict[str, Any]:
    definition = PROFILE_DEFINITIONS[profile_name]
    timeframe = definition["decision_timeframe"]
    rows = [row for row in manifest.get("datasets") or [] if row.get("timeframe") == timeframe]
    usable = [row for row in rows if row.get("status") in {"valid", "limited"}]
    requirement = _profile_row_depth_requirement(definition)
    blockers: list[str] = []
    if manifest.get("duplicate_identities"):
        blockers.append("DUPLICATE_DATASET_IDENTITY")
    if not usable:
        blockers.append("NO_USABLE_DATASETS_FOR_DECISION_TIMEFRAME")
    enough_rows = [
        row for row in usable
        if int(row.get("valid_ohlcv_row_count") or 0) >= requirement["required_valid_ohlcv_rows"]
    ]
    if usable and not enough_rows:
        blockers.append("INSUFFICIENT_ROWS_FOR_MULTIPLE_SEQUENTIAL_SPLITS")
    unique_usable_identities = {
        (str(row.get("ticker")), str(row.get("timeframe")))
        for row in usable
        if row.get("ticker") and row.get("timeframe")
    }
    unique_eligible_identities = {
        (str(row.get("ticker")), str(row.get("timeframe")))
        for row in enough_rows
        if row.get("ticker") and row.get("timeframe")
    }
    if usable and len(unique_eligible_identities) < requirement["required_split_count"]:
        blockers.append("INSUFFICIENT_ELIGIBLE_IDENTITIES_FOR_UNIVERSE_SPLIT")
    status = "READY_FOR_PROTOCOL_FREEZE"
    if blockers:
        status = "BLOCKED"
    return {
        "profile": profile_name,
        "decision_timeframe": timeframe,
        "available_dataset_count": len(rows),
        "usable_dataset_count": len(usable),
        "unique_usable_identity_count": len(unique_usable_identities),
        "eligible_dataset_count": len(enough_rows),
        "unique_eligible_identity_count": len(unique_eligible_identities),
        "minimum_rows": definition["minimum_rows"],
        "minimum_split_rows": definition["minimum_split_rows"],
        "required_split_count": requirement["required_split_count"],
        "max_horizon_bars": requirement["max_horizon_bars"],
        "purge_embargo_rows": requirement["purge_embargo_rows"],
        "required_valid_ohlcv_rows": requirement["required_valid_ohlcv_rows"],
        "primary_horizon_bars": definition["primary_horizon_bars"],
        "secondary_horizon_bars": list(definition["secondary_horizon_bars"]),
        "status": status,
        "blockers": blockers,
    }


def deterministic_universe_partition(tickers: list[str]) -> dict[str, list[str]]:
    unique = sorted({str(ticker).upper() for ticker in tickers if str(ticker).strip()})
    partitions = {"development": [], "validation": [], "locked_holdout": []}
    for index, ticker in enumerate(unique):
        bucket = index % 3
        if bucket == 0:
            partitions["development"].append(ticker)
        elif bucket == 1:
            partitions["validation"].append(ticker)
        else:
            partitions["locked_holdout"].append(ticker)
    return partitions


def propose_temporal_splits(start: str, end: str, *, embargo_bars: int) -> dict[str, Any]:
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    if end_ts <= start_ts:
        raise ValueError("end must be after start")
    span = end_ts - start_ts
    development_end = start_ts + span * 0.6
    validation_end = start_ts + span * 0.8
    return {
        "split_rule": "60/20/20 chronological by timestamp range",
        "development": {"start": start_ts.isoformat(), "end": development_end.isoformat()},
        "validation": {"start": development_end.isoformat(), "end": validation_end.isoformat()},
        "locked_holdout": {"start": validation_end.isoformat(), "end": end_ts.isoformat()},
        "embargo_bars": int(embargo_bars),
        "purge_rule": "exclude candidates whose outcome horizon would cross a split boundary",
    }


def build_protocol_model(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    protocol = {
        "schema_version": PROTOCOL_SCHEMA_VERSION,
        "status": PROTOCOL_STATUS_PROPOSED_WITH_BLOCKERS,
        "profile_definitions": PROFILE_DEFINITIONS,
        "candidate_architecture": "single_timeframe_canonical_point_in_time_builder",
        "higher_timeframe_context": "future_extension_not_active",
        "universe_policy": {
            "ticker_split": "deterministic_sorted_modulo_3",
            "use_case_cohort_allowed": True,
            "performance_based_selection_allowed": False,
        },
        "temporal_split_policy": {
            "rule": "chronological_60_20_20",
            "purge": "candidate horizons purged at split boundaries",
            "embargo": "max approved horizon bars",
        },
        "walk_forward_policy": {
            "design": "rolling_or_expanding_to_be_approved",
            "minimum_candidate_count": "HUMAN_APPROVAL_REQUIRED",
            "zero_candidate_folds": "recorded_not_deleted",
            "incomplete_evidence_candidates": "tracked_separately_non_actionable",
        },
        "outcome_contract": {
            "labels": ["TP_FIRST", "SL_FIRST", "NEITHER", "AMBIGUOUS", "INVALID"],
            "same_bar_policies": ["conservative", "optimistic", "open_proximity", "unknown"],
            "time_exit": "represented_by_NEITHER_with_horizon_diagnostics",
            "gap_semantics": "OHLC bar path limited; executable gap modelling not accepted",
        },
        "baselines": [
            "time_matched_unconditional_long",
            "matched_random_entry_fixed_seed",
            "declared_trend_baseline_if_existing_contract_is_used",
        ],
        "cost_assumptions": {
            "gross_price_path_research": True,
            "fixed_cost_sensitivity": "HUMAN_APPROVAL_REQUIRED",
            "spread_slippage_sensitivity": "HUMAN_APPROVAL_REQUIRED",
            "net_profitability_claim_allowed": False,
        },
        "metric_set": {
            "candidate_generation": [
                "decision_count",
                "candidate_core_count",
                "complete_evidence_count",
                "rank_eligible_count",
                "ineligible_reason_counts",
                "score_band_counts",
            ],
            "future_outcome": [
                "outcome_counts",
                "expectancy_R",
                "median_R",
                "loss_tail_quantiles",
                "MFE_MAE_distributions",
                "hit_timing",
            ],
            "statistical_controls": [
                "block_resampling",
                "confidence_intervals",
                "multiple_testing_trial_count",
                "PBO_or_documented_applicability_assessment",
            ],
        },
        "acceptance_criteria": {
            "minimum_dataset_quality": "HUMAN_APPROVAL_REQUIRED",
            "minimum_fold_coverage": "HUMAN_APPROVAL_REQUIRED",
            "minimum_candidate_count": "HUMAN_APPROVAL_REQUIRED",
            "maximum_single_ticker_concentration": "HUMAN_APPROVAL_REQUIRED",
            "holdout_rule": "no parameter revision after holdout without new trial generation",
        },
        "trial_ledger_policy": TRIAL_LEDGER_SCHEMA_VERSION,
        "data_manifest_digest": manifest.get("manifest_digest") if manifest else None,
    }
    protocol["protocol_digest"] = sha256_digest({key: value for key, value in protocol.items() if key != "protocol_digest"})
    return protocol


def _validate_trial_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    def reject_absolute_paths(value: Any, index: int, key_path: str) -> None:
        if isinstance(value, str):
            if Path(value).is_absolute():
                errors.append(f"TRIAL_ABSOLUTE_PATH_NOT_ALLOWED:{index}:{key_path}")
            return
        if isinstance(value, dict):
            for key, item in value.items():
                reject_absolute_paths(item, index, f"{key_path}.{key}")
            return
        if isinstance(value, list):
            for item_index, item in enumerate(value):
                reject_absolute_paths(item, index, f"{key_path}[{item_index}]")

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"TRIAL_ROW_INVALID:{index}")
            continue
        missing = [field for field in REQUIRED_TRIAL_FIELDS if field not in row]
        if missing:
            errors.append(f"TRIAL_REQUIRED_FIELDS_MISSING:{index}:{','.join(missing)}")
        trial_id = str(row.get("trial_id") or "").strip()
        if not trial_id:
            errors.append(f"TRIAL_ID_MISSING:{index}")
        elif trial_id in seen_ids:
            errors.append(f"TRIAL_ID_DUPLICATE:{trial_id}")
        seen_ids.add(trial_id)
        for key, value in row.items():
            reject_absolute_paths(value, index, str(key))
    return errors


def validate_trial_ledger_append_only(existing: list[dict[str, Any]], proposed: list[dict[str, Any]]) -> dict[str, Any]:
    validation_errors = _validate_trial_rows(proposed)
    if validation_errors:
        return {"success": False, "errors": validation_errors}
    if len(proposed) < len(existing):
        return {"success": False, "errors": ["TRIAL_LEDGER_DELETION_NOT_ALLOWED"]}
    for index, row in enumerate(existing):
        if proposed[index] != row:
            return {"success": False, "errors": ["TRIAL_LEDGER_RETROACTIVE_EDIT_NOT_ALLOWED"]}
    return {"success": True, "errors": []}


def build_trial_ledger_example() -> dict[str, Any]:
    return {
        "schema_version": TRIAL_LEDGER_SCHEMA_VERSION,
        "append_only": True,
        "trials": [
            {
                "trial_id": "TRIAL-YYYYMMDD-001",
                "protocol_generation": "PROTOCOL_PROPOSED_WITH_BLOCKERS",
                "code_commit": "HUMAN_APPROVAL_REQUIRED",
                "data_manifest_digest": "HUMAN_APPROVAL_REQUIRED",
                "candidate_builder_version": "canonical_point_in_time_builder",
                "strategy_config_digest": "HUMAN_APPROVAL_REQUIRED",
                "profile": "SWING",
                "universe_split": "deterministic_sorted_modulo_3",
                "temporal_split": "chronological_60_20_20",
                "horizon": "primary_10_bars",
                "baseline_definitions": ["time_matched_unconditional_long", "matched_random_entry_fixed_seed"],
                "cost_assumptions": "gross_plus_approved_sensitivity",
                "random_seeds": [1009, 2003],
                "metrics_requested": ["outcome_counts", "expectancy_R", "confidence_intervals"],
                "status": "planned",
                "holdout_touched": False,
                "follow_up_reason": None,
            }
        ],
    }


def write_manifest(manifest: dict[str, Any], output_path: str | Path, repo_root: str | Path) -> Path:
    root = Path(repo_root).resolve()
    path = Path(output_path)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    if not _is_inside_repo(path, root):
        raise ValueError("manifest output must stay inside repository root")
    if not _is_ignored_manifest_output(path, root):
        raise ValueError("manifest output must be under .marketflow/research")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(manifest))
    return path


def build_readiness_result(repo_root: str | Path, roots: list[str | Path] | None = None) -> dict[str, Any]:
    manifest = build_dataset_manifest(repo_root, roots)
    protocol = build_protocol_model(manifest)
    feasibility = {
        profile: assess_profile_feasibility(manifest, profile)
        for profile in PROFILE_DEFINITIONS
    }
    tickers = sorted({row["ticker"] for row in manifest.get("datasets") or [] if row.get("ticker")})
    return {
        "manifest": manifest,
        "summary": summarize_manifest(manifest),
        "profile_feasibility": feasibility,
        "universe_partition": deterministic_universe_partition(tickers),
        "protocol": protocol,
        "no_performance_inspected": True,
        "forbidden_operations": {
            "outcome_evaluator_invoked": False,
            "candidate_generation_invoked": False,
            "performance_metrics_calculated": False,
            "network_invoked": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build no-peek MarketFlow swing applicability readiness inventory.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--scan-root", action="append", default=None, help="Relative or absolute dataset root to scan.")
    parser.add_argument("--manifest-output", default=None, help="Optional ignored local manifest output path.")
    args = parser.parse_args(argv)
    result = build_readiness_result(args.repo_root, args.scan_root)
    if args.manifest_output:
        write_manifest(result["manifest"], args.manifest_output, args.repo_root)
    summary = {
        "summary": result["summary"],
        "profile_feasibility": result["profile_feasibility"],
        "protocol_digest": result["protocol"]["protocol_digest"],
        "no_performance_inspected": True,
    }
    print(json.dumps(summary, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
