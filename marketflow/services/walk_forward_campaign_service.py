"""Aggregate saved walk-forward validation CSV artifacts into campaign reports."""

from __future__ import annotations

from datetime import datetime
import math
from pathlib import Path
from typing import Any

import pandas as pd


WALK_FORWARD_CAMPAIGN_RESULTS_CSV_KIND = "walk_forward_campaign_results_csv"
WALK_FORWARD_CAMPAIGN_SUMMARY_CSV_KIND = "walk_forward_campaign_summary_csv"
WALK_FORWARD_CAMPAIGN_REPORT_MD_KIND = "walk_forward_campaign_report_md"

DEFAULT_CAMPAIGN_GROUP_BY = ["ticker", "timeframe", "profile_name", "wyckoff_event"]
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
    "source_file",
    "source_path",
]
NUMERIC_RESULT_COLUMNS = ["realized_R", "future_bars_available", "horizon_bars", "bars_to_hit"]
TIMEFRAME_TOKENS = {"1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m"}


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
        context = _filename_context(row.get("source_file") or row.get("source_path"))
        for column in ("ticker", "timeframe", "profile_name"):
            if _is_missing(row.get(column)) and context.get(column):
                normalized.at[index, column] = context[column]
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
            }
        )
        rows.append(row)

    summary = pd.DataFrame(rows)
    result.update({"success": bool(rows), "dataframe": summary, "rows": _dataframe_rows(summary)})
    return result


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
    summary_rows: list[dict[str, Any]] | None = None,
    result_rows: list[dict[str, Any]] | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    grouped_rows = [dict(row) for row in grouped_summary_rows or []]
    summaries = [dict(row) for row in summary_rows or []]
    results = [dict(row) for row in result_rows or []]
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
        for column in [*DEFAULT_CAMPAIGN_GROUP_BY, "sample_count", "scoreable_count", "win_rate", "mean_realized_R"]
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
    metadata_lines.extend(f"- {key.replace('_', ' ').title()}: {_md_value(value)}" for key, value in meta.items())
    input_lines = [f"- `{path}`" for path in input_paths] or ["_No input paths recorded._"]
    sections = [
        "# MarketFlow Walk-Forward Campaign Report",
        "## Metadata\n\n" + "\n".join(metadata_lines),
        "## Input Files\n\n" + "\n".join(input_lines),
        "## Campaign Summary by Timeframe/Event\n\n" + _markdown_table(grouped_rows, group_columns),
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
    save_report_md: bool = True,
) -> dict[str, Any]:
    root = Path(root_dir)
    destination = Path(output_dir) if output_dir is not None else root
    discovery = discover_walk_forward_campaign_files(root, recursive=recursive)
    summary_load = load_walk_forward_summary_csvs(discovery["summary_csv_paths"])
    results_load = load_walk_forward_results_csvs(discovery["results_csv_paths"])
    normalized = normalize_walk_forward_result_rows(results_load["dataframe"])
    grouped = build_walk_forward_campaign_grouped_summary(normalized, group_by=group_by)
    artifacts: list[dict[str, Any]] = []
    warnings = [
        *discovery["warnings"],
        *summary_load["warnings"],
        *results_load["warnings"],
        *grouped["warnings"],
    ]
    errors = [
        *discovery["errors"],
        *summary_load["errors"],
        *results_load["errors"],
        *grouped["errors"],
    ]
    campaign_result = {
        "success": False,
        "root_dir": str(root),
        "output_dir": str(destination),
        "discovery_result": discovery,
        "summary_load_result": summary_load,
        "results_load_result": results_load,
        "grouped_summary_result": grouped,
        "artifacts": artifacts,
        "results_artifact": None,
        "summary_artifact": None,
        "report_artifact": None,
        "warnings": warnings,
        "errors": errors,
    }
    if not grouped["success"]:
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
    if save_report_md:
        report_artifact = _artifact_result(WALK_FORWARD_CAMPAIGN_REPORT_MD_KIND)
        try:
            path = _collision_safe_path(
                destination,
                build_walk_forward_campaign_report_filename(ticker=ticker, timestamp=timestamp),
            )
            markdown = build_walk_forward_campaign_report_markdown(
                grouped_summary_rows=grouped["rows"],
                summary_rows=summary_load["rows"],
                result_rows=_dataframe_rows(normalized),
                metadata={
                    "root_dir": str(root),
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
