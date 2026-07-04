"""Run registry helpers for saved Historical Walk-Forward Validation artifacts."""

from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any


WALK_FORWARD_RUN_REGISTRY_JSON_KIND = "walk_forward_run_registry_json"
WALK_FORWARD_RUN_REGISTRY_CSV_KIND = "walk_forward_run_registry_csv"
NO_EVENT_FILTER = "NO_EVENT_FILTER"
UNKNOWN_RUN_FILTER = "UNKNOWN_RUN_FILTER"
WALK_FORWARD_COVERAGE_STATUSES = {
    "complete",
    "partial",
    "no_matching_cases",
    "zero_cases",
    "insufficient_data",
    "stale",
    "inactive",
    "missing_results",
    "failed",
    "unknown",
}

REGISTRY_CSV_COLUMNS = [
    "run_id",
    "run_signature",
    "created_at",
    "ticker",
    "timeframe",
    "profile_name",
    "run_event_filter",
    "step",
    "max_cases",
    "require_mature_future",
    "horizon_bars",
    "min_lookback_rows",
    "row_count",
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
    "source_csv_path",
    "source_csv_filename",
    "source_csv_size",
    "source_csv_mtime",
    "source_csv_sha256",
    "summary_csv_path",
    "results_csv_path",
    "cases_csv_path",
    "markdown_path",
    "status",
    "is_stale",
    "is_active",
    "superseded_by",
    "artifact_paths",
    "warnings",
    "errors",
]


def _safe_filename_part(value: str | None) -> str | None:
    if value is None or not str(value).strip():
        return None
    safe = "".join(
        character if character.isalnum() or character in "._-" else "_"
        for character in str(value).strip()
    )
    return safe.strip("._-") or None


def build_walk_forward_run_registry_json_filename(*, ticker: str | None = None) -> str:
    prefix = _safe_filename_part(ticker) or "marketflow"
    return f"{prefix}_walk_forward_run_registry.json"


def build_walk_forward_run_registry_csv_filename(*, ticker: str | None = None) -> str:
    prefix = _safe_filename_part(ticker) or "marketflow"
    return f"{prefix}_walk_forward_run_registry.csv"


def build_source_csv_fingerprint(source_csv_path: str | Path) -> dict[str, Any]:
    path = Path(source_csv_path)
    result = {
        "source_csv_path": str(path),
        "source_csv_filename": path.name,
        "source_csv_exists": False,
        "source_csv_size": None,
        "source_csv_mtime": None,
        "source_csv_sha256": None,
        "warnings": [],
        "errors": [],
    }
    try:
        if not path.exists() or not path.is_file():
            result["warnings"].append(f"Source CSV is missing: {path}")
            return result
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        stat = path.stat()
        result.update(
            {
                "source_csv_exists": True,
                "source_csv_size": stat.st_size,
                "source_csv_mtime": stat.st_mtime,
                "source_csv_sha256": digest.hexdigest(),
            }
        )
    except Exception as exc:
        result["warnings"].append(f"Could not fingerprint source CSV {path}: {type(exc).__name__}: {exc}")
    return result


def normalize_run_event_filter(value: str | None) -> str:
    text = str(value or "").strip()
    if not text or text.upper() == NO_EVENT_FILTER:
        return NO_EVENT_FILTER
    tokens = sorted({token.strip().upper() for token in text.split(",") if token.strip()})
    return ",".join(tokens) if tokens else NO_EVENT_FILTER


def _normalized_string(value: str | None, *, lowercase: bool = False) -> str:
    text = str(value or "").strip()
    return text.lower() if lowercase else text.upper()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _has_messages(value: Any) -> bool:
    if isinstance(value, (list, tuple, set)):
        return any(str(item).strip() for item in value)
    return bool(str(value or "").strip())


def _is_explicit_false(value: Any) -> bool:
    return value is False or str(value).strip().lower() in {"false", "0", "no"}


def _run_results_path_exists(run: dict[str, Any]) -> bool:
    value = run.get("results_csv_path")
    if value is None or not str(value).strip():
        return False
    path = Path(str(value))
    if path.is_file():
        return True
    registry_path = Path(str(run.get("registry_path") or ""))
    return any(
        candidate.is_file()
        for candidate in (registry_path.parent / path, registry_path.parent / path.name)
    )


def normalize_walk_forward_run_coverage_status(run: dict[str, Any]) -> str:
    """Return a backward-compatible coverage status for one registered run."""
    source = run if isinstance(run, dict) else {}
    if "is_active" in source and _is_explicit_false(source.get("is_active")):
        return "inactive"
    if bool(source.get("is_stale")):
        return "stale"

    errors_present = _has_messages(source.get("errors"))
    if errors_present:
        return "failed"

    case_count = _optional_int(source.get("case_count"))
    evaluated_count = _optional_int(source.get("evaluated_count")) or 0
    scoreable_count = _optional_int(source.get("scoreable_count")) or 0
    row_count = _optional_int(source.get("row_count"))
    min_lookback = _optional_int(
        source.get("min_lookback_rows") or source.get("minimum_lookback_rows")
    )
    event_filter = str(source.get("run_event_filter") or "").strip().upper()
    event_filtered = event_filter not in {"", NO_EVENT_FILTER, UNKNOWN_RUN_FILTER}

    if "results_csv_path" in source and not _run_results_path_exists(source):
        return "missing_results"
    if (case_count or 0) == 0 and evaluated_count == 0 and scoreable_count == 0:
        if event_filtered:
            return "no_matching_cases"
        if row_count is not None and min_lookback is not None and row_count < min_lookback:
            return "insufficient_data"
        return "zero_cases"

    status = str(source.get("status") or "").strip().lower()
    if status in WALK_FORWARD_COVERAGE_STATUSES:
        return status
    if scoreable_count > 0 or evaluated_count > 0 or (case_count or 0) > 0:
        return "complete"
    return "unknown"


def build_walk_forward_run_coverage_reason(run: dict[str, Any]) -> str:
    """Return a concise explanation for a run's normalized coverage status."""
    status = normalize_walk_forward_run_coverage_status(run)
    reasons = {
        "complete": "result rows available",
        "partial": "run completed with warnings or partial artifacts",
        "no_matching_cases": "no mature rows matched requested event filter",
        "zero_cases": "validation completed with zero cases",
        "insufficient_data": "insufficient source rows for selected profile/lookback",
        "stale": "source CSV changed or is missing",
        "inactive": "run is inactive or superseded",
        "missing_results": "results CSV missing",
        "failed": "validation failed",
        "unknown": "run coverage status is unknown",
    }
    return reasons[status]


def build_walk_forward_run_signature(
    *,
    ticker: str | None,
    timeframe: str | None,
    profile_name: str | None,
    source_csv_sha256: str | None,
    run_event_filter: str | None,
    step: int | None,
    max_cases: int | None,
    require_mature_future: bool | None,
    horizon_bars: int | None,
    min_lookback_rows: int | None,
) -> str:
    payload = {
        "ticker": _normalized_string(ticker),
        "timeframe": _normalized_string(timeframe, lowercase=True),
        "profile_name": _normalized_string(profile_name, lowercase=True),
        "source_csv_sha256": _normalized_string(source_csv_sha256, lowercase=True),
        "run_event_filter": normalize_run_event_filter(run_event_filter),
        "step": _optional_int(step),
        "max_cases": _optional_int(max_cases),
        "require_mature_future": (
            bool(require_mature_future) if require_mature_future is not None else None
        ),
        "horizon_bars": _optional_int(horizon_bars),
        "min_lookback_rows": _optional_int(min_lookback_rows),
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def build_walk_forward_run_id(run_signature: str) -> str:
    return str(run_signature or "").strip()[:16]


def _result_parts(validation_result: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = validation_result if isinstance(validation_result, dict) else {}
    build = source.get("build_result") if isinstance(source.get("build_result"), dict) else {}
    evaluation = source.get("evaluation_result") if isinstance(source.get("evaluation_result"), dict) else {}
    summary = source.get("summary") if isinstance(source.get("summary"), dict) else {}
    return build, evaluation, summary


def _messages(validation_result: dict[str, Any], key: str) -> list[str]:
    build, evaluation, summary = _result_parts(validation_result)
    messages: list[str] = []
    for source in (validation_result, build, evaluation, summary):
        messages.extend(str(item) for item in source.get(key) or [] if str(item).strip())
    return list(dict.fromkeys(messages))


def _artifact_path(artifacts: list[dict[str, Any]], kind: str) -> str | None:
    for artifact in artifacts:
        if artifact.get("kind") == kind and artifact.get("path"):
            return str(artifact["path"])
    return None


def build_walk_forward_run_metadata(
    *,
    validation_result: dict[str, Any],
    source_csv_path: str | Path,
    run_event_filter: str | None,
    step: int | None,
    max_cases: int | None,
    require_mature_future: bool | None,
    artifacts: list[dict[str, Any]] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    source = validation_result if isinstance(validation_result, dict) else {}
    build, evaluation, summary = _result_parts(source)
    saved_artifacts = [dict(item) for item in artifacts or [] if isinstance(item, dict)]
    fingerprint = build_source_csv_fingerprint(source_csv_path)
    normalized_filter = normalize_run_event_filter(run_event_filter)
    ticker = build.get("ticker") or source.get("ticker")
    timeframe = build.get("timeframe") or source.get("timeframe")
    profile_name = build.get("profile_name") or evaluation.get("profile_name") or source.get("profile_name")
    horizon = build.get("horizon_bars") or evaluation.get("horizon_bars")
    minimum_lookback = build.get("minimum_lookback_rows") or build.get("min_lookback_rows")
    signature = build_walk_forward_run_signature(
        ticker=ticker,
        timeframe=timeframe,
        profile_name=profile_name,
        source_csv_sha256=fingerprint.get("source_csv_sha256"),
        run_event_filter=normalized_filter,
        step=step,
        max_cases=max_cases,
        require_mature_future=require_mature_future,
        horizon_bars=horizon,
        min_lookback_rows=minimum_lookback,
    )
    case_count = _optional_int(build.get("case_count")) or 0
    evaluated_count = _optional_int(evaluation.get("evaluated_count")) or 0
    scoreable_count = _optional_int(summary.get("scoreable_count")) or 0
    row_count = _optional_int(build.get("row_count"))
    min_lookback_rows = _optional_int(minimum_lookback)
    warnings = [*_messages(source, "warnings"), *(fingerprint.get("warnings") or [])]
    errors = _messages(source, "errors")
    for artifact in saved_artifacts:
        warnings.extend(str(item) for item in artifact.get("warnings") or [])
        errors.extend(str(item) for item in artifact.get("errors") or [])
    warnings = list(dict.fromkeys(item for item in warnings if item))
    errors = list(dict.fromkeys(item for item in errors if item))
    validation_success = bool(source.get("success"))
    event_filtered = normalized_filter not in {NO_EVENT_FILTER, UNKNOWN_RUN_FILTER}
    if errors:
        status = "failed"
    elif case_count == 0:
        if event_filtered:
            status = "no_matching_cases"
        elif (
            row_count is not None
            and min_lookback_rows is not None
            and row_count < min_lookback_rows
        ):
            status = "insufficient_data"
        else:
            status = "zero_cases"
    elif not validation_success:
        status = "failed"
    elif saved_artifacts and warnings:
        status = "partial"
    elif scoreable_count > 0 or evaluated_count > 0 or case_count > 0:
        status = "complete"
    else:
        status = "partial"
    artifact_paths = [str(item["path"]) for item in saved_artifacts if item.get("path")]
    return {
        "run_id": build_walk_forward_run_id(signature),
        "run_signature": signature,
        "created_at": created_at or datetime.now().isoformat(timespec="seconds"),
        "ticker": ticker,
        "timeframe": timeframe,
        "profile_name": profile_name,
        **{key: fingerprint.get(key) for key in (
            "source_csv_path",
            "source_csv_filename",
            "source_csv_size",
            "source_csv_mtime",
            "source_csv_sha256",
        )},
        "run_event_filter": normalized_filter,
        "step": _optional_int(step),
        "max_cases": _optional_int(max_cases),
        "require_mature_future": (
            bool(require_mature_future) if require_mature_future is not None else None
        ),
        "horizon_bars": _optional_int(horizon),
        "min_lookback_rows": min_lookback_rows,
        "row_count": row_count,
        "case_count": case_count,
        "evaluated_count": evaluated_count,
        "scoreable_count": scoreable_count,
        "tp_first_count": _optional_int(summary.get("tp_first_count")) or 0,
        "sl_first_count": _optional_int(summary.get("sl_first_count")) or 0,
        "neither_count": _optional_int(summary.get("neither_count")) or 0,
        "invalid_count": _optional_int(summary.get("invalid_count")) or 0,
        "ambiguous_count": _optional_int(summary.get("ambiguous_count")) or 0,
        "mean_realized_R": summary.get("mean_realized_R"),
        "median_realized_R": summary.get("median_realized_R"),
        "summary_csv_path": _artifact_path(saved_artifacts, "walk_forward_summary_csv"),
        "results_csv_path": _artifact_path(saved_artifacts, "walk_forward_results_csv"),
        "cases_csv_path": _artifact_path(saved_artifacts, "walk_forward_cases_csv"),
        "markdown_path": _artifact_path(saved_artifacts, "walk_forward_validation_summary_md"),
        "artifact_paths": artifact_paths,
        "status": status,
        "is_stale": not bool(fingerprint.get("source_csv_exists")),
        "is_active": True,
        "superseded_by": None,
        "warnings": warnings,
        "errors": errors,
    }


def read_walk_forward_run_registry(registry_path: str | Path) -> dict[str, Any]:
    path = Path(registry_path)
    result = {"success": True, "path": str(path), "runs": [], "warnings": [], "errors": []}
    if not path.exists():
        return result
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        runs = payload.get("runs") if isinstance(payload, dict) else payload
        if not isinstance(runs, list):
            raise ValueError("Registry JSON must contain a runs list.")
        result["runs"] = [dict(run) for run in runs if isinstance(run, dict)]
    except Exception as exc:
        result["success"] = False
        result["errors"].append(f"Could not read run registry {path}: {type(exc).__name__}: {exc}")
    return result


def write_walk_forward_run_registry(
    registry_path: str | Path, runs: list[dict[str, Any]]
) -> dict[str, Any]:
    path = Path(registry_path)
    result = {
        "success": False,
        "path": str(path),
        "filename": path.name,
        "kind": WALK_FORWARD_RUN_REGISTRY_JSON_KIND,
        "runs": [],
        "row_count": 0,
        "warnings": [],
        "errors": [],
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        clean_runs = [dict(run) for run in runs or [] if isinstance(run, dict)]
        payload = {"version": 1, "runs": clean_runs}
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, default=str) + "\n",
            encoding="utf-8",
        )
        result.update({"success": True, "runs": clean_runs, "row_count": len(clean_runs)})
    except Exception as exc:
        result["errors"].append(f"Could not write run registry {path}: {type(exc).__name__}: {exc}")
    return result


def upsert_walk_forward_run_registry(
    *, registry_path: str | Path, run_metadata: dict[str, Any]
) -> dict[str, Any]:
    read_result = read_walk_forward_run_registry(registry_path)
    if not read_result["success"]:
        return read_result
    runs = [dict(run) for run in read_result["runs"]]
    new_run = dict(run_metadata or {})
    new_run["is_active"] = True
    new_run.setdefault("is_stale", False)
    new_run["superseded_by"] = None
    run_id = new_run.get("run_id")
    signature = new_run.get("run_signature")
    replaced = False
    for index, existing in enumerate(runs):
        if run_id and existing.get("run_id") == run_id:
            runs[index] = new_run
            replaced = True
            break
    if not replaced:
        for existing in runs:
            if signature and existing.get("run_signature") == signature:
                existing["is_active"] = False
                existing["superseded_by"] = run_id
                existing["status"] = "superseded"
        runs.append(new_run)
    runs.sort(key=lambda run: (str(run.get("created_at") or ""), str(run.get("run_id") or "")))
    write_result = write_walk_forward_run_registry(registry_path, runs)
    write_result["replaced"] = replaced
    return write_result


def _csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple, set)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return value


def write_walk_forward_run_registry_csv(
    *,
    registry_json_path: str | Path,
    registry_csv_path: str | Path | None = None,
) -> dict[str, Any]:
    json_path = Path(registry_json_path)
    csv_path = Path(registry_csv_path) if registry_csv_path is not None else json_path.with_suffix(".csv")
    result = {
        "success": False,
        "path": str(csv_path),
        "filename": csv_path.name,
        "kind": WALK_FORWARD_RUN_REGISTRY_CSV_KIND,
        "row_count": 0,
        "warnings": [],
        "errors": [],
    }
    read_result = read_walk_forward_run_registry(json_path)
    result["warnings"].extend(read_result["warnings"])
    if not read_result["success"]:
        result["errors"].extend(read_result["errors"])
        return result
    try:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=REGISTRY_CSV_COLUMNS)
            writer.writeheader()
            for run in read_result["runs"]:
                writer.writerow({column: _csv_value(run.get(column)) for column in REGISTRY_CSV_COLUMNS})
        result.update({"success": True, "row_count": len(read_result["runs"])})
    except Exception as exc:
        result["errors"].append(f"Could not write registry CSV {csv_path}: {type(exc).__name__}: {exc}")
    return result


def refresh_walk_forward_run_registry_staleness(registry_path: str | Path) -> dict[str, Any]:
    read_result = read_walk_forward_run_registry(registry_path)
    result = {
        "success": False,
        "path": str(registry_path),
        "runs": [],
        "total_runs": 0,
        "stale_count": 0,
        "active_count": 0,
        "missing_source_count": 0,
        "warnings": list(read_result["warnings"]),
        "errors": list(read_result["errors"]),
    }
    if not read_result["success"]:
        return result
    runs = [dict(run) for run in read_result["runs"]]
    missing_count = 0
    for run in runs:
        fingerprint = build_source_csv_fingerprint(run.get("source_csv_path") or "")
        missing = not fingerprint.get("source_csv_exists")
        stored_hash = str(run.get("source_csv_sha256") or "")
        current_hash = str(fingerprint.get("source_csv_sha256") or "")
        run["is_stale"] = bool(missing or not stored_hash or current_hash != stored_hash)
        if missing:
            missing_count += 1
            warning = f"Run {run.get('run_id') or 'unknown'} source CSV is missing: {run.get('source_csv_path') or ''}"
            result["warnings"].append(warning)
            run_warnings = [str(item) for item in run.get("warnings") or []]
            if warning not in run_warnings:
                run_warnings.append(warning)
            run["warnings"] = run_warnings
    write_result = write_walk_forward_run_registry(registry_path, runs)
    result["errors"].extend(write_result["errors"])
    result.update(
        {
            "success": bool(write_result["success"]),
            "runs": runs,
            "total_runs": len(runs),
            "stale_count": sum(bool(run.get("is_stale")) for run in runs),
            "active_count": sum(bool(run.get("is_active")) for run in runs),
            "missing_source_count": missing_count,
        }
    )
    result["warnings"] = list(dict.fromkeys(result["warnings"]))
    return result
