"""Aggregate saved walk-forward validation CSV artifacts into campaign reports."""

from __future__ import annotations

from datetime import datetime
import math
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.walk_forward_run_registry_service import (
    build_walk_forward_run_coverage_reason,
    normalize_walk_forward_run_coverage_status,
    read_walk_forward_run_registry,
    refresh_walk_forward_run_registry_staleness,
)


WALK_FORWARD_CAMPAIGN_RESULTS_CSV_KIND = "walk_forward_campaign_results_csv"
WALK_FORWARD_CAMPAIGN_SUMMARY_CSV_KIND = "walk_forward_campaign_summary_csv"
WALK_FORWARD_CAMPAIGN_COVERAGE_CSV_KIND = "walk_forward_campaign_coverage_csv"
WALK_FORWARD_CAMPAIGN_REPORT_MD_KIND = "walk_forward_campaign_report_md"

DEFAULT_CAMPAIGN_GROUP_BY = [
    "ticker",
    "timeframe",
    "profile_name",
    "run_event_filter",
    "wyckoff_event",
]
NORMALIZED_RESULT_COLUMNS = [
    "ticker",
    "timeframe",
    "profile_name",
    "wyckoff_phase",
    "wyckoff_event",
    "trend",
    "outcome",
    "realized_R",
    "future_bars_available",
    "horizon_bars",
    "bars_to_hit",
    "same_bar_hit",
    "backtest_success",
    "run_id",
    "run_signature",
    "run_event_filter",
    "run_step",
    "run_max_cases",
    "run_require_mature_future",
    "source_csv_sha256",
    "is_stale",
    "is_active",
    "registry_mode",
    "source_file",
    "source_path",
]
NUMERIC_RESULT_COLUMNS = ["realized_R", "future_bars_available", "horizon_bars", "bars_to_hit"]
TIMEFRAME_TOKENS = {"1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"}
COVERAGE_COLUMNS = [
    "run_id",
    "ticker",
    "timeframe",
    "profile_name",
    "run_event_filter",
    "step",
    "max_cases",
    "require_mature_future",
    "status",
    "coverage_status",
    "coverage_reason",
    "included_in_campaign",
    "exclusion_reason",
    "is_active",
    "is_stale",
    "source_csv_filename",
    "source_csv_path",
    "source_csv_sha256",
    "summary_csv_path",
    "results_csv_path",
    "cases_csv_path",
    "markdown_path",
    "case_count",
    "evaluated_count",
    "scoreable_count",
    "tp_first_count",
    "sl_first_count",
    "neither_count",
    "invalid_count",
    "ambiguous_count",
    "mean_realized_R",
    "median_realized_R",
    "result_row_count",
    "observed_event_count",
    "observed_events",
    "registry_mode",
    "created_at",
]


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def _safe_filename_part(value: str | None) -> str | None:
    if _is_missing(value):
        return None
    safe = "".join(
        character if character.isalnum() or character in "._-" else "_"
        for character in str(value).strip()
    )
    safe = safe.strip("._-")
    return safe or None


def _timestamp_for_filename(timestamp: str | None = None) -> str:
    return _safe_filename_part(timestamp) or datetime.now().strftime("%Y%m%d_%H%M%S")


def build_walk_forward_campaign_results_filename(
    *, ticker: str | None = None, timestamp: str | None = None
) -> str:
    prefix = _safe_filename_part(ticker) or "marketflow"
    return f"{prefix}_walk_forward_campaign_results_{_timestamp_for_filename(timestamp)}.csv"


def build_walk_forward_campaign_summary_filename(
    *, ticker: str | None = None, timestamp: str | None = None
) -> str:
    prefix = _safe_filename_part(ticker) or "marketflow"
    return f"{prefix}_walk_forward_campaign_summary_{_timestamp_for_filename(timestamp)}.csv"


def build_walk_forward_campaign_report_filename(
    *, ticker: str | None = None, timestamp: str | None = None
) -> str:
    prefix = _safe_filename_part(ticker) or "marketflow"
    return f"{prefix}_walk_forward_campaign_report_{_timestamp_for_filename(timestamp)}.md"


def build_walk_forward_campaign_coverage_filename(
    *, ticker: str | None = None, created_at: str | None = None
) -> str:
    prefix = _safe_filename_part(ticker) or "marketflow"
    return f"{prefix}_walk_forward_campaign_coverage_{_timestamp_for_filename(created_at)}.csv"


def discover_walk_forward_campaign_files(
    root_dir: str | Path, *, recursive: bool = True
) -> dict[str, Any]:
    root = Path(root_dir)
    result = {
        "success": False,
        "root_dir": str(root),
        "summary_csv_paths": [],
        "results_csv_paths": [],
        "summary_count": 0,
        "results_count": 0,
        "warnings": [],
        "errors": [],
    }
    if not root.exists() or not root.is_dir():
        result["warnings"].append(f"Campaign root folder does not exist or is not a directory: {root}")
        return result

    search = root.rglob if recursive else root.glob
    summary_paths = sorted(
        str(path)
        for path in search("*_walk_forward_summary_*.csv")
        if path.is_file() and "_walk_forward_campaign_summary_" not in path.name.lower()
    )
    results_paths = sorted(
        str(path)
        for path in search("*_walk_forward_results_*.csv")
        if path.is_file() and "_walk_forward_campaign_results_" not in path.name.lower()
    )
    result.update(
        {
            "summary_csv_paths": summary_paths,
            "results_csv_paths": results_paths,
            "summary_count": len(summary_paths),
            "results_count": len(results_paths),
        }
    )
    result["success"] = bool(summary_paths or results_paths)
    if not result["success"]:
        result["warnings"].append("No walk-forward summary or results CSV artifacts were found.")
    return result


def _discover_registry_paths(root: Path, recursive: bool) -> list[str]:
    if not root.exists() or not root.is_dir():
        return []
    search = root.rglob if recursive else root.glob
    return sorted(
        str(path)
        for path in search("*_walk_forward_run_registry.json")
        if path.is_file()
    )


def _registry_run_key(run: dict[str, Any]) -> str:
    return str(
        run.get("run_id")
        or run.get("run_signature")
        or run.get("results_csv_path")
        or run.get("created_at")
        or ""
    )


def _select_registry_campaign_runs(
    root: Path,
    *,
    recursive: bool,
    deduplicate_runs: bool,
    include_stale_runs: bool,
    active_only: bool,
) -> dict[str, Any]:
    registry_paths = _discover_registry_paths(root, recursive)
    result = {
        "success": bool(registry_paths),
        "mode": "run_registry" if registry_paths else "file_discovery",
        "registry_paths": registry_paths,
        "registry_file_count": len(registry_paths),
        "runs": [],
        "selected_runs": [],
        "ignored_runs": [],
        "total_run_count": 0,
        "selected_run_count": 0,
        "active_run_count": 0,
        "stale_run_count": 0,
        "ignored_inactive_count": 0,
        "ignored_stale_count": 0,
        "ignored_duplicate_count": 0,
        "ignored_run_count": 0,
        "warnings": [],
        "errors": [],
    }
    if not registry_paths:
        return result

    runs: list[dict[str, Any]] = []
    for registry_path in registry_paths:
        refresh = refresh_walk_forward_run_registry_staleness(registry_path)
        result["warnings"].extend(refresh.get("warnings") or [])
        result["errors"].extend(refresh.get("errors") or [])
        read_result = read_walk_forward_run_registry(registry_path)
        result["warnings"].extend(read_result.get("warnings") or [])
        result["errors"].extend(read_result.get("errors") or [])
        for run in read_result.get("runs") or []:
            row = dict(run)
            row["registry_path"] = registry_path
            runs.append(row)

    result["runs"] = runs
    result["total_run_count"] = len(runs)
    result["active_run_count"] = sum(bool(run.get("is_active")) for run in runs)
    result["stale_run_count"] = sum(bool(run.get("is_stale")) for run in runs)
    candidates: list[dict[str, Any]] = []
    ignored_runs: list[dict[str, Any]] = []
    ignored_ids: set[int] = set()
    for index, run in enumerate(runs):
        if active_only and not bool(run.get("is_active")):
            result["ignored_inactive_count"] += 1
            ignored_ids.add(index)
            ignored_runs.append({**run, "exclusion_reason": "inactive run excluded"})
            continue
        if not include_stale_runs and bool(run.get("is_stale")):
            result["ignored_stale_count"] += 1
            ignored_ids.add(index)
            ignored_runs.append({**run, "exclusion_reason": "stale run excluded"})
            continue
        candidates.append(run)

    candidates.sort(
        key=lambda run: (str(run.get("created_at") or ""), _registry_run_key(run)),
        reverse=True,
    )
    if deduplicate_runs:
        deduplicated: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        seen_signatures: set[str] = set()
        for run in candidates:
            run_id = str(run.get("run_id") or "").strip()
            signature = str(run.get("run_signature") or "").strip()
            duplicate = (
                (run_id and run_id in seen_ids)
                or (signature and signature in seen_signatures)
            )
            if duplicate:
                result["ignored_duplicate_count"] += 1
                ignored_runs.append({**run, "exclusion_reason": "duplicate run excluded"})
                continue
            if run_id:
                seen_ids.add(run_id)
            if signature:
                seen_signatures.add(signature)
            deduplicated.append(run)
        candidates = deduplicated
    result["selected_runs"] = candidates
    result["ignored_runs"] = ignored_runs
    result["selected_run_count"] = len(candidates)
    result["ignored_run_count"] = (
        len(ignored_ids) + result["ignored_duplicate_count"]
    )
    result["warnings"] = list(dict.fromkeys(result["warnings"]))
    result["errors"] = list(dict.fromkeys(result["errors"]))
    return result


def _dataframe_rows(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    if dataframe.empty:
        return []
    safe = dataframe.astype(object).where(pd.notna(dataframe), None)
    return safe.to_dict(orient="records")


def _load_walk_forward_csvs(
    paths: list[str | Path], *, coerce_numeric: bool
) -> dict[str, Any]:
    frames: list[pd.DataFrame] = []
    warnings: list[str] = []
    errors: list[str] = []
    for supplied_path in paths or []:
        path = Path(supplied_path)
        try:
            frame = pd.read_csv(path)
            frame["source_file"] = path.name
            frame["source_path"] = str(path)
            if coerce_numeric:
                for column in NUMERIC_RESULT_COLUMNS:
                    if column in frame.columns:
                        frame[column] = pd.to_numeric(frame[column], errors="coerce")
            frames.append(frame)
        except Exception as exc:
            warnings.append(f"Skipped unreadable CSV {path}: {type(exc).__name__}: {exc}")

    dataframe = pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()
    if not frames:
        warnings.append("No readable walk-forward CSV files were loaded.")
    return {
        "success": bool(frames),
        "dataframe": dataframe,
        "rows": _dataframe_rows(dataframe),
        "file_count": len(frames),
        "row_count": len(dataframe),
        "warnings": warnings,
        "errors": errors,
    }


def load_walk_forward_summary_csvs(paths: list[str | Path]) -> dict[str, Any]:
    return _load_walk_forward_csvs(paths, coerce_numeric=False)


def load_walk_forward_results_csvs(paths: list[str | Path]) -> dict[str, Any]:
    return _load_walk_forward_csvs(paths, coerce_numeric=True)


def _filename_context(source_file: Any) -> dict[str, str]:
    if _is_missing(source_file):
        return {}
    stem = Path(str(source_file)).stem
    marker = "_walk_forward_results_"
    marker_index = stem.lower().find(marker)
    if marker_index < 0:
        return {}
    prefix_tokens = [token for token in stem[:marker_index].split("_") if token]
    timeframe_index = next(
        (index for index, token in enumerate(prefix_tokens) if token.lower() in TIMEFRAME_TOKENS),
        None,
    )
    if timeframe_index is None:
        return {}
    context: dict[str, str] = {"timeframe": prefix_tokens[timeframe_index]}
    if timeframe_index > 0:
        ticker = "_".join(prefix_tokens[:timeframe_index])
        if ticker.lower() != "marketflow":
            context["ticker"] = ticker
    profile_tokens = prefix_tokens[timeframe_index + 1 :]
    if profile_tokens:
        context["profile_name"] = "_".join(profile_tokens)
    return context


def normalize_walk_forward_result_rows(dataframe: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(dataframe, pd.DataFrame):
        return pd.DataFrame(columns=NORMALIZED_RESULT_COLUMNS)
    normalized = dataframe.copy()
    for column in NORMALIZED_RESULT_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = None
    for index, row in normalized.iterrows():
        source_value = row.get("source_file")
        if _is_missing(source_value):
            source_value = row.get("source_path")
        context = _filename_context(source_value)
        for column in ("ticker", "timeframe", "profile_name"):
            if _is_missing(row.get(column)) and context.get(column):
                normalized.at[index, column] = context[column]
        if _is_missing(row.get("run_event_filter")):
            normalized.at[index, "run_event_filter"] = "UNKNOWN_RUN_FILTER"
        if _is_missing(row.get("registry_mode")):
            normalized.at[index, "registry_mode"] = "file_discovery"
        if _is_missing(row.get("is_stale")):
            normalized.at[index, "is_stale"] = False
        if _is_missing(row.get("is_active")):
            normalized.at[index, "is_active"] = True
    for column in NUMERIC_RESULT_COLUMNS:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")
    return normalized[NORMALIZED_RESULT_COLUMNS].copy()


def _truthy_count(series: pd.Series) -> int:
    truthy = {"true", "1", "yes", "y", "t"}
    return int(series.map(lambda value: str(value).strip().lower() in truthy if not _is_missing(value) else False).sum())


def _number_or_none(value: Any) -> float | None:
    if _is_missing(value):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _unique_run_count(group: pd.DataFrame, *, stale_only: bool = False) -> int:
    keys: set[str] = set()
    for _, row in group.iterrows():
        if stale_only and not _truthy_count(pd.Series([row.get("is_stale")])):
            continue
        key = ""
        for column in ("run_id", "run_signature", "source_path", "source_file"):
            value = row.get(column)
            if not _is_missing(value):
                key = str(value).strip()
                break
        if key:
            keys.add(key)
    return len(keys)


def build_walk_forward_campaign_grouped_summary(
    results_dataframe: pd.DataFrame, *, group_by: list[str] | None = None
) -> dict[str, Any]:
    groups = list(group_by) if group_by is not None else list(DEFAULT_CAMPAIGN_GROUP_BY)
    result = {
        "success": False,
        "dataframe": pd.DataFrame(),
        "rows": [],
        "group_by": groups,
        "warnings": [],
        "errors": [],
    }
    if not groups:
        result["errors"].append("At least one campaign grouping column is required.")
        return result
    if not isinstance(results_dataframe, pd.DataFrame) or results_dataframe.empty:
        result["warnings"].append("No walk-forward result rows were available for campaign grouping.")
        return result

    frame = results_dataframe.copy()
    for column in groups:
        if column not in frame.columns:
            frame[column] = ""
            result["warnings"].append(f"Missing grouping column was filled with blanks: {column}")
    if "wyckoff_event" in groups:
        frame["wyckoff_event"] = frame["wyckoff_event"].map(
            lambda value: "NO_CONFIRMED_EVENT" if _is_missing(value) else str(value).strip()
        )
    if "run_event_filter" in groups:
        frame["run_event_filter"] = frame["run_event_filter"].map(
            lambda value: "UNKNOWN_RUN_FILTER" if _is_missing(value) else str(value).strip()
        )
    for column in groups:
        if column != "wyckoff_event":
            frame[column] = frame[column].map(lambda value: "" if _is_missing(value) else value)
    if "outcome" not in frame.columns:
        frame["outcome"] = ""
    frame["_outcome"] = frame["outcome"].fillna("").astype(str).str.strip().str.upper()
    if "realized_R" not in frame.columns:
        frame["realized_R"] = None
    frame["_realized_R"] = pd.to_numeric(frame["realized_R"], errors="coerce")

    rows: list[dict[str, Any]] = []
    grouped = frame.groupby(groups, dropna=False, sort=True)
    for keys, group in grouped:
        key_values = keys if isinstance(keys, tuple) else (keys,)
        row = dict(zip(groups, key_values))
        outcomes = group["_outcome"]
        tp_count = int((outcomes == "TP_FIRST").sum())
        sl_count = int((outcomes == "SL_FIRST").sum())
        neither_count = int((outcomes == "NEITHER").sum())
        scoreable_count = tp_count + sl_count + neither_count
        realized = group["_realized_R"].dropna()
        bars = pd.to_numeric(group.get("bars_to_hit"), errors="coerce").dropna() if "bars_to_hit" in group else pd.Series(dtype=float)
        source_file_count = (
            int(group["source_file"].dropna().astype(str).loc[lambda values: values.str.strip() != ""].nunique())
            if "source_file" in group
            else 0
        )
        row.update(
            {
                "sample_count": len(group),
                "scoreable_count": scoreable_count,
                "tp_first_count": tp_count,
                "sl_first_count": sl_count,
                "neither_count": neither_count,
                "invalid_count": int((outcomes == "INVALID").sum()),
                "ambiguous_count": int((outcomes == "AMBIGUOUS").sum()),
                "win_rate": tp_count / scoreable_count if scoreable_count else None,
                "loss_rate": sl_count / scoreable_count if scoreable_count else None,
                "neither_rate": neither_count / scoreable_count if scoreable_count else None,
                "mean_realized_R": _number_or_none(realized.mean()) if not realized.empty else None,
                "median_realized_R": _number_or_none(realized.median()) if not realized.empty else None,
                "min_realized_R": _number_or_none(realized.min()) if not realized.empty else None,
                "max_realized_R": _number_or_none(realized.max()) if not realized.empty else None,
                "same_bar_hit_count": _truthy_count(group["same_bar_hit"]) if "same_bar_hit" in group else 0,
                "mean_bars_to_hit": _number_or_none(bars.mean()) if not bars.empty else None,
                "source_file_count": source_file_count,
                "run_count": _unique_run_count(group),
                "stale_run_count": _unique_run_count(group, stale_only=True),
                "registry_mode": ",".join(
                    sorted(
                        {
                            str(value).strip()
                            for value in group.get("registry_mode", pd.Series(dtype=object)).dropna()
                            if str(value).strip()
                        }
                    )
                ) or "file_discovery",
            }
        )
        rows.append(row)

    summary = pd.DataFrame(rows)
    result.update({"success": bool(rows), "dataframe": summary, "rows": _dataframe_rows(summary)})
    return result


def _coverage_key(run: dict[str, Any]) -> str:
    for field in ("run_id", "run_signature", "results_csv_path", "source_path"):
        value = run.get(field)
        if not _is_missing(value):
            return f"{field}:{value}"
    return ""


def _coverage_results_usable(path: str | None) -> bool:
    if not path or not Path(path).is_file():
        return False
    try:
        pd.read_csv(path, nrows=0)
        return True
    except Exception:
        return False


def _fallback_coverage_runs(result_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    runs: dict[str, dict[str, Any]] = {}
    for row in result_rows:
        source_path = str(row.get("source_path") or "").strip()
        source_file = str(row.get("source_file") or Path(source_path).name).strip()
        key = source_path or source_file
        if not key:
            continue
        context = _filename_context(source_file)
        run = runs.setdefault(
            key,
            {
                "run_id": f"file:{source_file}",
                "ticker": row.get("ticker") or context.get("ticker"),
                "timeframe": row.get("timeframe") or context.get("timeframe"),
                "profile_name": row.get("profile_name") or context.get("profile_name"),
                "run_event_filter": "UNKNOWN_RUN_FILTER",
                "results_csv_path": source_path,
                "case_count": 0,
                "evaluated_count": 0,
                "scoreable_count": 0,
                "status": "complete",
                "is_active": True,
                "is_stale": False,
            },
        )
        run["case_count"] += 1
        run["evaluated_count"] += 1
        if str(row.get("outcome") or "").strip().upper() in {"TP_FIRST", "SL_FIRST", "NEITHER"}:
            run["scoreable_count"] += 1
    return list(runs.values())


def _fallback_coverage_runs_for_paths(
    paths: list[str], result_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    runs = _fallback_coverage_runs(result_rows)
    known_paths = {_path_lookup_key(run.get("results_csv_path")) for run in runs}
    for value in paths:
        if _path_lookup_key(value) in known_paths:
            continue
        path = Path(value)
        context = _filename_context(path.name)
        runs.append(
            {
                "run_id": f"file:{path.name}",
                "ticker": context.get("ticker"),
                "timeframe": context.get("timeframe"),
                "profile_name": context.get("profile_name"),
                "run_event_filter": "UNKNOWN_RUN_FILTER",
                "results_csv_path": str(path),
                "case_count": 0,
                "evaluated_count": 0,
                "scoreable_count": 0,
                "status": "zero_cases",
                "is_active": True,
                "is_stale": False,
            }
        )
    return runs


def build_walk_forward_campaign_coverage_rows(
    *,
    registry_runs: list[dict[str, Any]] | None = None,
    selected_runs: list[dict[str, Any]] | None = None,
    ignored_runs: list[dict[str, Any]] | None = None,
    result_rows: list[dict[str, Any]] | None = None,
    registry_mode: str | None = None,
) -> dict[str, Any]:
    """Build one coverage row per registered run without inventing performance rows."""
    mode = str(registry_mode or "file_discovery")
    results = [dict(row) for row in result_rows or [] if isinstance(row, dict)]
    runs = [dict(run) for run in registry_runs or [] if isinstance(run, dict)]
    warnings: list[str] = []
    if mode != "run_registry":
        if not runs:
            runs = _fallback_coverage_runs(results)
        warnings.append(
            "Campaign coverage is limited because no run registry metadata was available."
        )
    selected = [dict(run) for run in selected_runs or runs if isinstance(run, dict)]
    ignored = [dict(run) for run in ignored_runs or [] if isinstance(run, dict)]
    selected_keys = {_coverage_key(run) for run in selected if _coverage_key(run)}
    ignored_by_key = {
        _coverage_key(run): str(run.get("exclusion_reason") or "run excluded")
        for run in ignored
        if _coverage_key(run)
    }

    rows: list[dict[str, Any]] = []
    for run in runs:
        run_id = str(run.get("run_id") or "").strip()
        registered_results_path = _registered_artifact_path(run, "results_csv_path")
        matched_results: list[dict[str, Any]] = []
        for result_row in results:
            row_run_id = str(result_row.get("run_id") or "").strip()
            if run_id and row_run_id == run_id:
                matched_results.append(result_row)
                continue
            if registered_results_path and _path_lookup_key(result_row.get("source_path")) == _path_lookup_key(registered_results_path):
                matched_results.append(result_row)

        events = sorted(
            {
                "NO_CONFIRMED_EVENT" if _is_missing(row.get("wyckoff_event")) else str(row.get("wyckoff_event")).strip()
                for row in matched_results
            }
        )
        coverage_status = normalize_walk_forward_run_coverage_status(run)
        key = _coverage_key(run)
        selected_run = key in selected_keys
        results_usable = _coverage_results_usable(registered_results_path)
        if not results_usable and coverage_status not in {"inactive", "stale", "failed"}:
            coverage_status = "missing_results"
        included = bool(selected_run and results_usable)
        exclusion_reason = ignored_by_key.get(key, "")
        if not included and not exclusion_reason:
            if not results_usable:
                exclusion_reason = "results CSV missing or unusable"
            elif not selected_run:
                exclusion_reason = "run not selected"
        row = {
            column: run.get(column)
            for column in COVERAGE_COLUMNS
            if column not in {
                "coverage_status",
                "coverage_reason",
                "included_in_campaign",
                "exclusion_reason",
                "result_row_count",
                "observed_event_count",
                "observed_events",
                "registry_mode",
            }
        }
        row.update(
            {
                "run_event_filter": run.get("run_event_filter") or "UNKNOWN_RUN_FILTER",
                "coverage_status": coverage_status,
                "coverage_reason": (
                    "results CSV missing"
                    if coverage_status == "missing_results"
                    else build_walk_forward_run_coverage_reason(run)
                ),
                "included_in_campaign": included,
                "exclusion_reason": exclusion_reason,
                "result_row_count": len(matched_results),
                "observed_event_count": len(events),
                "observed_events": "; ".join(events),
                "registry_mode": mode,
            }
        )
        rows.append({column: row.get(column) for column in COVERAGE_COLUMNS})

    dataframe = pd.DataFrame(rows, columns=COVERAGE_COLUMNS)
    status_counts = {
        status: sum(row.get("coverage_status") == status for row in rows)
        for status in (
            "complete",
            "no_matching_cases",
            "zero_cases",
            "insufficient_data",
            "stale",
            "inactive",
            "missing_results",
            "failed",
        )
    }
    included_count = sum(bool(row.get("included_in_campaign")) for row in rows)
    return {
        "success": bool(rows),
        "rows": _dataframe_rows(dataframe),
        "dataframe": dataframe,
        "total_run_count": len(rows),
        "included_run_count": included_count,
        "excluded_run_count": len(rows) - included_count,
        "complete_count": status_counts["complete"],
        "no_matching_cases_count": status_counts["no_matching_cases"],
        "zero_cases_count": status_counts["zero_cases"],
        "insufficient_data_count": status_counts["insufficient_data"],
        "stale_count": status_counts["stale"],
        "inactive_count": status_counts["inactive"],
        "missing_results_count": status_counts["missing_results"],
        "failed_count": status_counts["failed"],
        "warnings": warnings,
        "errors": [],
    }


def _md_value(value: Any) -> str:
    if _is_missing(value):
        return ""
    if isinstance(value, float):
        value = f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value).replace("|", "\\|").replace("\n", " ")


def _markdown_table(rows: list[dict[str, Any]], columns: list[str], max_rows: int = 20) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(_md_value(row.get(column)) for column in columns) + " |"
        for row in rows[:max_rows]
    ]
    return "\n".join([header, separator, *body])


def build_walk_forward_campaign_report_markdown(
    *,
    grouped_summary_rows: list[dict[str, Any]],
    coverage_rows: list[dict[str, Any]] | None = None,
    coverage_result: dict[str, Any] | None = None,
    summary_rows: list[dict[str, Any]] | None = None,
    result_rows: list[dict[str, Any]] | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    grouped_rows = [dict(row) for row in grouped_summary_rows or []]
    summaries = [dict(row) for row in summary_rows or []]
    results = [dict(row) for row in result_rows or []]
    coverage = [dict(row) for row in coverage_rows or []]
    coverage_summary = dict(coverage_result or {})
    meta = dict(metadata or {})
    input_paths = sorted(
        {
            str(row.get("source_path"))
            for row in [*summaries, *results]
            if not _is_missing(row.get("source_path"))
        }
    )
    numeric_groups = [row for row in grouped_rows if not _is_missing(row.get("mean_realized_R"))]
    best = sorted(numeric_groups, key=lambda row: float(row["mean_realized_R"]), reverse=True)[:5]
    weakest = sorted(numeric_groups, key=lambda row: float(row["mean_realized_R"]))[:5]
    group_columns = [
        column
        for column in [
            *DEFAULT_CAMPAIGN_GROUP_BY,
            "run_count",
            "source_file_count",
            "sample_count",
            "scoreable_count",
            "win_rate",
            "loss_rate",
            "mean_realized_R",
            "median_realized_R",
            "stale_run_count",
            "registry_mode",
        ]
        if any(column in row for row in grouped_rows)
    ]
    outcome_row = {
        key: sum(int(row.get(key) or 0) for row in grouped_rows)
        for key in [
            "sample_count",
            "scoreable_count",
            "tp_first_count",
            "sl_first_count",
            "neither_count",
            "invalid_count",
            "ambiguous_count",
        ]
    }
    metadata_lines = [f"- Created: {_md_value(meta.pop('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))}"]
    if input_paths:
        meta.setdefault("input_files", "; ".join(input_paths))
    metadata_lines.extend(f"- {key.replace('_', ' ').title()}: {_md_value(value)}" for key, value in meta.items())
    coverage_counts = [
        f"- Total Registered Runs: {coverage_summary.get('total_run_count', len(coverage))}",
        f"- Included Runs: {coverage_summary.get('included_run_count', 0)}",
        f"- Excluded Runs: {coverage_summary.get('excluded_run_count', 0)}",
        f"- No Matching Cases: {coverage_summary.get('no_matching_cases_count', 0)}",
        f"- Zero Cases: {coverage_summary.get('zero_cases_count', 0)}",
        f"- Insufficient Data: {coverage_summary.get('insufficient_data_count', 0)}",
        f"- Stale Runs: {coverage_summary.get('stale_count', 0)}",
        f"- Inactive Runs: {coverage_summary.get('inactive_count', 0)}",
        f"- Missing Results: {coverage_summary.get('missing_results_count', 0)}",
        f"- Failed Runs: {coverage_summary.get('failed_count', 0)}",
    ]
    coverage_columns = [
        "ticker",
        "timeframe",
        "profile_name",
        "run_event_filter",
        "coverage_status",
        "included_in_campaign",
        "coverage_reason",
        "case_count",
        "scoreable_count",
        "result_row_count",
        "is_stale",
        "is_active",
        "created_at",
    ]
    sections = [
        "# MarketFlow Walk-Forward Campaign Report",
        "## Metadata\n\n" + "\n".join(metadata_lines),
        "## Campaign Coverage by Registered Run\n\n"
        + "\n".join(coverage_counts)
        + "\n\n"
        + _markdown_table(coverage, coverage_columns, max_rows=100),
        "## Campaign Performance Summary by Result Rows\n\n" + _markdown_table(grouped_rows, group_columns),
        "## Best Groups by Mean R\n\n" + _markdown_table(best, group_columns, max_rows=5),
        "## Weakest Groups by Mean R\n\n" + _markdown_table(weakest, group_columns, max_rows=5),
        "## Outcome Distribution\n\n" + _markdown_table([outcome_row], list(outcome_row)),
        "## Notes / Limitations\n\n"
        "- Aggregates saved artifacts; it does not rerun walk-forward validation.\n"
        "- Missing source columns are retained as blank values where possible.\n"
        "- Event filters and sampled windows can bias results.\n"
        "- Small samples should not be overinterpreted.",
        "## Guardrails\n\n"
        "- Walk-forward campaign aggregation only.\n"
        "- Not financial advice.\n"
        "- Historical validation does not guarantee future performance.\n"
        "- Small samples should not be overinterpreted.\n"
        "- Event filters and sampled windows can bias results.\n"
        "- Candidate quality remains separate from workflow validity.",
        "",
    ]
    return "\n\n".join(sections)


def _collision_safe_path(output_dir: Path, filename: str) -> Path:
    target = output_dir / filename
    if not target.exists():
        return target
    counter = 2
    while True:
        candidate = output_dir / f"{target.stem}_{counter}{target.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def _artifact_result(kind: str) -> dict[str, Any]:
    return {
        "success": False,
        "path": None,
        "filename": None,
        "kind": kind,
        "row_count": 0,
        "errors": [],
        "warnings": [],
    }


def _write_dataframe_artifact(
    dataframe: pd.DataFrame, output_dir: Path, filename: str, kind: str
) -> dict[str, Any]:
    result = _artifact_result(kind)
    try:
        path = _collision_safe_path(output_dir, filename)
        dataframe.to_csv(path, index=False)
        result.update({"success": True, "path": str(path), "filename": path.name, "row_count": len(dataframe)})
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
    return result


def _registered_artifact_path(run: dict[str, Any], field: str) -> str | None:
    value = run.get(field)
    if _is_missing(value):
        return None
    path = Path(str(value))
    if path.exists():
        return str(path)
    registry_path = Path(str(run.get("registry_path") or ""))
    candidates = [registry_path.parent / path, registry_path.parent / path.name]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(path)


def _path_lookup_key(value: Any) -> str:
    if _is_missing(value):
        return ""
    try:
        return str(Path(str(value)).resolve())
    except OSError:
        return str(Path(str(value)))


def _add_registry_metadata_to_results(
    dataframe: pd.DataFrame, runs: list[dict[str, Any]]
) -> pd.DataFrame:
    if dataframe.empty:
        return dataframe
    lookup = {
        _path_lookup_key(_registered_artifact_path(run, "results_csv_path")): run
        for run in runs
        if _registered_artifact_path(run, "results_csv_path")
    }
    enriched = dataframe.copy()
    for index, row in enriched.iterrows():
        run = lookup.get(_path_lookup_key(row.get("source_path")))
        if not run:
            continue
        for target, source in (
            ("run_id", "run_id"),
            ("run_signature", "run_signature"),
            ("run_event_filter", "run_event_filter"),
            ("run_step", "step"),
            ("run_max_cases", "max_cases"),
            ("run_require_mature_future", "require_mature_future"),
            ("source_csv_sha256", "source_csv_sha256"),
            ("is_stale", "is_stale"),
            ("is_active", "is_active"),
        ):
            enriched.at[index, target] = run.get(source)
        enriched.at[index, "registry_mode"] = "run_registry"
    return enriched


def write_walk_forward_campaign_artifacts(
    *,
    root_dir: str | Path,
    output_dir: str | Path | None = None,
    recursive: bool = True,
    ticker: str | None = None,
    timestamp: str | None = None,
    group_by: list[str] | None = None,
    save_results_csv: bool = True,
    save_summary_csv: bool = True,
    save_coverage_csv: bool = True,
    save_report_md: bool = True,
    use_run_registry: bool = True,
    deduplicate_runs: bool = True,
    include_stale_runs: bool = False,
    active_only: bool = True,
) -> dict[str, Any]:
    root = Path(root_dir)
    destination = Path(output_dir) if output_dir is not None else root
    registry_result = _select_registry_campaign_runs(
        root,
        recursive=recursive,
        deduplicate_runs=deduplicate_runs,
        include_stale_runs=include_stale_runs,
        active_only=active_only,
    ) if use_run_registry else {
        "success": False,
        "mode": "file_discovery",
        "registry_paths": [],
        "registry_file_count": 0,
        "runs": [],
        "selected_runs": [],
        "ignored_runs": [],
        "total_run_count": 0,
        "selected_run_count": 0,
        "active_run_count": 0,
        "stale_run_count": 0,
        "ignored_inactive_count": 0,
        "ignored_stale_count": 0,
        "ignored_duplicate_count": 0,
        "ignored_run_count": 0,
        "warnings": [],
        "errors": [],
    }
    registry_mode = bool(use_run_registry and registry_result["registry_file_count"])
    if registry_mode:
        selected_runs = registry_result["selected_runs"]
        summary_paths = list(dict.fromkeys(
            path
            for run in selected_runs
            if (path := _registered_artifact_path(run, "summary_csv_path"))
        ))
        results_paths = list(dict.fromkeys(
            path
            for run in selected_runs
            if (path := _registered_artifact_path(run, "results_csv_path"))
        ))
        discovery = {
            "success": bool(summary_paths or results_paths),
            "root_dir": str(root),
            "summary_csv_paths": summary_paths,
            "results_csv_paths": results_paths,
            "summary_count": len(summary_paths),
            "results_count": len(results_paths),
            "warnings": [],
            "errors": [],
        }
        if not discovery["success"]:
            discovery["warnings"].append(
                "No eligible registry runs referenced walk-forward summary or results CSV artifacts."
            )
    else:
        discovery = discover_walk_forward_campaign_files(root, recursive=recursive)
    summary_load = load_walk_forward_summary_csvs(discovery["summary_csv_paths"])
    results_load = load_walk_forward_results_csvs(discovery["results_csv_paths"])
    source_dataframe = results_load["dataframe"]
    if registry_mode:
        source_dataframe = _add_registry_metadata_to_results(
            source_dataframe, registry_result["selected_runs"]
        )
    normalized = normalize_walk_forward_result_rows(source_dataframe)
    grouped = build_walk_forward_campaign_grouped_summary(normalized, group_by=group_by)
    normalized_rows = _dataframe_rows(normalized)
    if registry_mode:
        coverage_runs = registry_result["runs"]
        coverage_selected_runs = registry_result["selected_runs"]
        coverage_ignored_runs = registry_result["ignored_runs"]
    else:
        coverage_runs = _fallback_coverage_runs_for_paths(
            discovery["results_csv_paths"], normalized_rows
        )
        coverage_selected_runs = coverage_runs
        coverage_ignored_runs = []
    coverage = build_walk_forward_campaign_coverage_rows(
        registry_runs=coverage_runs,
        selected_runs=coverage_selected_runs,
        ignored_runs=coverage_ignored_runs,
        result_rows=normalized_rows,
        registry_mode="run_registry" if registry_mode else "file_discovery",
    )
    artifacts: list[dict[str, Any]] = []
    warnings = [
        *discovery["warnings"],
        *summary_load["warnings"],
        *results_load["warnings"],
        *grouped["warnings"],
        *registry_result["warnings"],
        *coverage["warnings"],
    ]
    errors = [
        *discovery["errors"],
        *summary_load["errors"],
        *results_load["errors"],
        *grouped["errors"],
        *registry_result["errors"],
        *coverage["errors"],
    ]
    campaign_metadata = {
        "registry_mode": "run_registry" if registry_mode else "file_discovery",
        "use_run_registry": bool(use_run_registry),
        "deduplicate_runs": bool(deduplicate_runs),
        "include_stale_runs": bool(include_stale_runs),
        "active_only": bool(active_only),
        "registry_file_count": registry_result["registry_file_count"],
        "selected_run_count": registry_result["selected_run_count"],
        "active_run_count": registry_result["active_run_count"],
        "stale_run_count": registry_result["stale_run_count"],
        "ignored_run_count": registry_result["ignored_run_count"],
        "coverage_row_count": coverage["total_run_count"],
        "included_run_count": coverage["included_run_count"],
        "excluded_run_count": coverage["excluded_run_count"],
        "no_matching_cases_count": coverage["no_matching_cases_count"],
        "zero_cases_count": coverage["zero_cases_count"],
        "insufficient_data_count": coverage["insufficient_data_count"],
        "missing_results_count": coverage["missing_results_count"],
        "failed_count": coverage["failed_count"],
    }
    campaign_result = {
        "success": False,
        "root_dir": str(root),
        "output_dir": str(destination),
        "discovery_result": discovery,
        "summary_load_result": summary_load,
        "results_load_result": results_load,
        "grouped_summary_result": grouped,
        "coverage_result": coverage,
        "registry_result": registry_result,
        "campaign_metadata": campaign_metadata,
        "artifacts": artifacts,
        "results_artifact": None,
        "summary_artifact": None,
        "coverage_artifact": None,
        "report_artifact": None,
        "warnings": warnings,
        "errors": errors,
    }
    if not grouped["success"] and not coverage["success"]:
        return campaign_result
    try:
        destination.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        campaign_result["errors"].append(f"Could not create output folder: {type(exc).__name__}: {exc}")
        return campaign_result

    if save_results_csv:
        campaign_result["results_artifact"] = _write_dataframe_artifact(
            normalized,
            destination,
            build_walk_forward_campaign_results_filename(ticker=ticker, timestamp=timestamp),
            WALK_FORWARD_CAMPAIGN_RESULTS_CSV_KIND,
        )
    if save_summary_csv:
        campaign_result["summary_artifact"] = _write_dataframe_artifact(
            grouped["dataframe"],
            destination,
            build_walk_forward_campaign_summary_filename(ticker=ticker, timestamp=timestamp),
            WALK_FORWARD_CAMPAIGN_SUMMARY_CSV_KIND,
        )
    if save_coverage_csv:
        campaign_result["coverage_artifact"] = _write_dataframe_artifact(
            coverage["dataframe"],
            destination,
            build_walk_forward_campaign_coverage_filename(
                ticker=ticker, created_at=timestamp
            ),
            WALK_FORWARD_CAMPAIGN_COVERAGE_CSV_KIND,
        )
    if save_report_md:
        report_artifact = _artifact_result(WALK_FORWARD_CAMPAIGN_REPORT_MD_KIND)
        try:
            path = _collision_safe_path(
                destination,
                build_walk_forward_campaign_report_filename(ticker=ticker, timestamp=timestamp),
            )
            markdown = build_walk_forward_campaign_report_markdown(
                grouped_summary_rows=grouped["rows"],
                coverage_rows=coverage["rows"],
                coverage_result=coverage,
                summary_rows=summary_load["rows"],
                result_rows=normalized_rows,
                metadata={
                    "root_dir": str(root),
                    **campaign_metadata,
                    "summary_file_count": summary_load["file_count"],
                    "results_file_count": results_load["file_count"],
                    "result_row_count": len(normalized),
                    "group_count": len(grouped["dataframe"]),
                },
            )
            path.write_text(markdown, encoding="utf-8")
            report_artifact.update(
                {"success": True, "path": str(path), "filename": path.name, "row_count": len(grouped["dataframe"])}
            )
        except Exception as exc:
            report_artifact["errors"].append(f"{type(exc).__name__}: {exc}")
        campaign_result["report_artifact"] = report_artifact

    selected = [
        artifact
        for artifact in [
            campaign_result["results_artifact"],
            campaign_result["summary_artifact"],
            campaign_result["coverage_artifact"],
            campaign_result["report_artifact"],
        ]
        if isinstance(artifact, dict)
    ]
    artifacts.extend(artifact for artifact in selected if artifact.get("path"))
    campaign_result["errors"].extend(error for artifact in selected for error in artifact["errors"])
    campaign_result["warnings"].extend(warning for artifact in selected for warning in artifact["warnings"])
    if not selected:
        campaign_result["warnings"].append("No campaign output artifacts were selected.")
    campaign_result["success"] = bool(selected) and all(artifact["success"] for artifact in selected)
    return campaign_result
