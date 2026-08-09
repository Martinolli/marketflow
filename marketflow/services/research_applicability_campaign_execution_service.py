"""Offline execution for the research-only applicability campaign."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dataset_file_availability_verification_service as availability
from marketflow.services import read_only_registry_discovery_service as discovery
from marketflow.services import research_applicability_campaign_execution_approval_service as approval
from marketflow.services import research_applicability_campaign_execution_candidate_service as candidate


ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED"
)
SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_V1 = (
    "research_applicability_campaign_executed_v1"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY"
)
RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED = (
    "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED"
)
RESEARCH_ONLY_NON_ACTIONABLE = candidate.RESEARCH_ONLY_NON_ACTIONABLE
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = "RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE"
NOT_AUTHORIZED = candidate.NOT_AUTHORIZED

DEFAULT_OUTPUT_ROOT = Path(candidate.PLANNED_OUTPUT_ROOT)
DEFAULT_BASE_COMMIT = "77a31596ce862ecf25c06beb6586be41171374d9"
DEFAULT_BRANCH = "feature/research-applicability-campaign-execution-v1"
EXPECTED_APPROVAL_DIGEST = (
    "5d6655341899e765b22a6a38a50f2405473a3ec704a3c67209eca45b114cdf37"
)

OUTPUT_NAMES = list(candidate.PLANNED_OUTPUT_NAMES)
DATASET_EXPECTED_ROW_COUNTS = {"SWING": 1988, "POSITION_SWING": 994}
COMMON_REQUIRED_COLUMNS = {
    "ticker",
    "dataset_profile",
    "dataset_bar_rule",
    "session_date",
    "session_type",
    "bar_start_utc",
    "bar_end_utc",
    "bar_start_local",
    "bar_end_local",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "transactions",
    "vwap",
    "source_row_count",
    "source_first_timestamp_utc",
    "source_last_timestamp_utc",
    "source_session_date",
    "source_timeframe",
}
PROFILE_REQUIRED_COLUMNS = {
    "SWING": COMMON_REQUIRED_COLUMNS | {"bar_number_in_session"},
    "POSITION_SWING": COMMON_REQUIRED_COLUMNS,
}
NUMERIC_COLUMNS = {"open", "high", "low", "close", "volume", "transactions", "vwap"}
TIMESTAMP_COLUMNS = {
    "bar_start_utc",
    "bar_end_utc",
    "source_first_timestamp_utc",
    "source_last_timestamp_utc",
}


class ResearchApplicabilityCampaignExecutionError(ValueError):
    """Raised when campaign execution artifacts violate research-only guardrails."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _resolve_root(root: str | Path | None, default: Path) -> Path:
    return default if root is None else Path(root)


def _boundary_fields() -> dict[str, Any]:
    return {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _parse_decimal(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _parse_timestamp(value: Any) -> bool:
    if value in (None, ""):
        return False
    try:
        datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _report(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_name": name,
        **_boundary_fields(),
        **payload,
    }


def _definitions_by_profile() -> dict[str, dict[str, Any]]:
    return {item["dataset_profile"]: item for item in discovery._registry_definitions()}


def _entries_by_profile(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        item.get("dataset_profile"): item
        for item in entries
        if isinstance(item, dict) and item.get("dataset_profile")
    }


def _read_rows_by_profile(search_root: Path, entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    rows_by_profile: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        path = search_root / entry["dataset_path"]
        rows_by_profile[entry["dataset_profile"]] = discovery._read_csv_rows(path)
    return rows_by_profile


def _dataset_load_report(
    entries: list[dict[str, Any]],
    rows_by_profile: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    return _report(
        "dataset_load_report",
        {
            "datasets": [
                {
                    "registry_key": entry["registry_key"],
                    "dataset_profile": entry["dataset_profile"],
                    "dataset_bar_rule": entry["dataset_bar_rule"],
                    "file_exists": entry["dataset_file_exists"],
                    "file_size_bytes": entry["dataset_file_size_bytes"],
                    "row_count": len(rows_by_profile.get(entry["dataset_profile"], [])),
                    "manifest_exists": entry["manifest_file_exists"],
                    "dataset_digest_verified": entry["dataset_rows_digest_match"],
                    "manifest_digest_verified": entry["dataset_manifest_digest_match"],
                    "dataset_rows_digest": entry["dataset_rows_digest_actual"],
                    "dataset_manifest_digest": entry["dataset_manifest_digest_actual"],
                    "runtime_use": NOT_AUTHORIZED,
                    "strategy_use": NOT_AUTHORIZED,
                }
                for entry in entries
            ],
            "dataset_count": len(entries),
            "datasets_loaded_count": len(rows_by_profile),
            "datasets_digest_verified_count": sum(
                1 for item in entries if item.get("dataset_rows_digest_match") is True
            ),
            "manifest_digest_verified_count": sum(
                1 for item in entries if item.get("dataset_manifest_digest_match") is True
            ),
        },
    )


def _schema_validation_report(rows_by_profile: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    datasets = []
    overall = "PASS"
    for profile, rows in sorted(rows_by_profile.items()):
        columns = set(rows[0]) if rows else set()
        required = PROFILE_REQUIRED_COLUMNS[profile]
        missing = sorted(required - columns)
        unexpected = sorted(columns - required)
        timestamp_parseable = {
            column: all(_parse_timestamp(row.get(column)) for row in rows)
            for column in sorted(TIMESTAMP_COLUMNS & columns)
        }
        numeric_parseable = {
            column: all(_parse_decimal(row.get(column)) is not None for row in rows)
            for column in sorted(NUMERIC_COLUMNS & columns)
        }
        status = "PASS" if not missing and all(timestamp_parseable.values()) else "FAIL"
        if status != "PASS":
            overall = "FAIL"
        datasets.append(
            {
                "dataset_profile": profile,
                "required_columns_present": not missing,
                "missing_required_columns": missing,
                "unexpected_columns": unexpected,
                "timestamp_columns_parseable": timestamp_parseable,
                "numeric_columns_parseable": numeric_parseable,
                "column_count": len(columns),
                "row_count": len(rows),
                "status": status,
            }
        )
    return _report("schema_validation_report", {"schema_validation_status": overall, "datasets": datasets})


def _bar_count_report(rows_by_profile: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    datasets = []
    overall = "PASS"
    for profile, expected in DATASET_EXPECTED_ROW_COUNTS.items():
        actual = len(rows_by_profile.get(profile, []))
        match = actual == expected
        if not match:
            overall = "FAIL"
        datasets.append(
            {
                "dataset_profile": profile,
                "expected_row_count": expected,
                "actual_row_count": actual,
                "match": match,
            }
        )
    return _report(
        "bar_count_consistency_report",
        {"bar_count_consistency_status": overall, "datasets": datasets},
    )


def _date_range_report(rows_by_profile: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    datasets = []
    overall = "PASS"
    for profile, rows in sorted(rows_by_profile.items()):
        dates = [str(row.get("session_date")) for row in rows if row.get("session_date")]
        timestamps = [str(row.get("bar_start_utc")) for row in rows if row.get("bar_start_utc")]
        first_date = min(dates) if dates else None
        last_date = max(dates) if dates else None
        status = (
            "PASS"
            if first_date and last_date and first_date >= candidate.DATE_RANGE_START and last_date <= candidate.DATE_RANGE_END
            else "FAIL"
        )
        if status != "PASS":
            overall = "FAIL"
        datasets.append(
            {
                "dataset_profile": profile,
                "expected_start": candidate.DATE_RANGE_START,
                "expected_end": candidate.DATE_RANGE_END,
                "first_session_date_observed": first_date,
                "last_session_date_observed": last_date,
                "first_timestamp_observed": min(timestamps) if timestamps else None,
                "last_timestamp_observed": max(timestamps) if timestamps else None,
                "coverage_status": status,
            }
        )
    return _report(
        "date_range_coverage_report",
        {"date_range_coverage_status": overall, "datasets": datasets},
    )


def _null_summary_report(rows_by_profile: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    datasets = []
    for profile, rows in sorted(rows_by_profile.items()):
        columns = sorted(rows[0]) if rows else []
        fields = {}
        for column in columns:
            null_count = sum(1 for row in rows if row.get(column) in (None, ""))
            fields[column] = {
                "null_count": null_count,
                "null_percentage": "0" if not rows else str((Decimal(null_count) * Decimal(100)) / Decimal(len(rows))),
            }
        datasets.append({"dataset_profile": profile, "row_count": len(rows), "fields": fields})
    return _report("null_field_summary_report", {"null_field_summary_status": "PASS", "datasets": datasets})


def _ohlc_report(rows_by_profile: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    datasets = []
    overall = "PASS"
    for profile, rows in sorted(rows_by_profile.items()):
        violations = []
        for index, row in enumerate(rows, start=1):
            open_value = _parse_decimal(row.get("open"))
            high_value = _parse_decimal(row.get("high"))
            low_value = _parse_decimal(row.get("low"))
            close_value = _parse_decimal(row.get("close"))
            if None in (open_value, high_value, low_value, close_value):
                violations.append({"row_number": index, "violation": "OHLC_NUMERIC_NON_NULL"})
                continue
            assert open_value is not None and high_value is not None and low_value is not None and close_value is not None
            if high_value < max(open_value, close_value):
                violations.append({"row_number": index, "violation": "HIGH_BELOW_OPEN_OR_CLOSE"})
            if low_value > min(open_value, close_value):
                violations.append({"row_number": index, "violation": "LOW_ABOVE_OPEN_OR_CLOSE"})
            if high_value < low_value:
                violations.append({"row_number": index, "violation": "HIGH_BELOW_LOW"})
        if violations:
            overall = "FAIL"
        datasets.append(
            {
                "dataset_profile": profile,
                "row_count": len(rows),
                "violation_count": len(violations),
                "violations": violations[:25],
                "status": "PASS" if not violations else "FAIL",
            }
        )
    return _report("ohlc_consistency_report", {"ohlc_consistency_status": overall, "datasets": datasets})


def _volume_report(rows_by_profile: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    datasets = []
    overall = "PASS"
    for profile, rows in sorted(rows_by_profile.items()):
        violations = []
        for index, row in enumerate(rows, start=1):
            volume = _parse_decimal(row.get("volume"))
            if volume is None:
                violations.append({"row_number": index, "violation": "VOLUME_NUMERIC_NON_NULL"})
            elif volume < 0:
                violations.append({"row_number": index, "violation": "VOLUME_NEGATIVE"})
        if violations:
            overall = "FAIL"
        datasets.append(
            {
                "dataset_profile": profile,
                "row_count": len(rows),
                "violation_count": len(violations),
                "violations": violations[:25],
                "status": "PASS" if not violations else "FAIL",
            }
        )
    return _report("volume_consistency_report", {"volume_consistency_status": overall, "datasets": datasets})


def _mean(values: list[Decimal]) -> Decimal | None:
    if not values:
        return None
    return sum(values, Decimal("0")) / Decimal(len(values))


def _indicator_report(rows_by_profile: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    datasets = []
    for profile, rows in sorted(rows_by_profile.items()):
        closes = [_parse_decimal(row.get("close")) for row in rows]
        volumes = [_parse_decimal(row.get("volume")) for row in rows]
        ranges = []
        returns = []
        previous_close: Decimal | None = None
        for row, close in zip(rows, closes, strict=False):
            high = _parse_decimal(row.get("high"))
            low = _parse_decimal(row.get("low"))
            open_value = _parse_decimal(row.get("open"))
            if high is not None and low is not None and open_value not in (None, Decimal("0")):
                assert open_value is not None
                ranges.append(((high - low) / open_value) * Decimal(100))
            if previous_close not in (None, Decimal("0")) and close is not None:
                assert previous_close is not None
                returns.append(((close - previous_close) / previous_close) * Decimal(100))
            if close is not None:
                previous_close = close
        close_values = [item for item in closes if item is not None]
        volume_values = [item for item in volumes if item is not None]
        datasets.append(
            {
                "dataset_profile": profile,
                "calculation_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
                "bar_return_percentage_observations": len(returns),
                "mean_bar_return_percentage": _mean(returns),
                "rolling_mean_close_window": 5,
                "latest_rolling_mean_close": _mean(close_values[-5:]),
                "rolling_volume_mean_window": 5,
                "latest_rolling_volume_mean": _mean(volume_values[-5:]),
                "range_percentage_observations": len(ranges),
                "mean_range_percentage": _mean(ranges),
                "non_actionable_descriptive_only": True,
            }
        )
    return _report(
        "indicator_calculation_report",
        {
            "indicator_calculation_status": "PASS",
            "indicator_acceptance_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "datasets": datasets,
        },
    )


def _module_compatibility_report() -> dict[str, Any]:
    return _report(
        "module_compatibility_matrix",
        {
            "module_compatibility_status": "RESEARCH_ONLY_COMPATIBILITY_LISTED",
            "modules": [
                {
                    "module": "read_only_registry_discovery_service",
                    "compatibility_status": "COMPATIBLE_READ_ONLY_METADATA",
                    "called_during_execution": False,
                },
                {
                    "module": "dataset_file_availability_verification_service",
                    "compatibility_status": "COMPATIBLE_READ_ONLY_DIGEST_VERIFICATION",
                    "called_during_execution": True,
                },
                {
                    "module": "strategy_service",
                    "compatibility_status": "UNTESTED_RUNTIME_MODULE_NOT_CALLED",
                    "called_during_execution": False,
                },
                {
                    "module": "walk_forward_validation_service",
                    "compatibility_status": "UNTESTED_RESEARCH_MODULE_NOT_CALLED",
                    "called_during_execution": False,
                },
            ],
        },
    )


def _failure_inventory(reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    failures = []
    warnings = []
    schema = reports["schema_validation_report"]
    for dataset in schema["datasets"]:
        if dataset["missing_required_columns"]:
            failures.append(
                {
                    "report": "schema_validation_report",
                    "dataset_profile": dataset["dataset_profile"],
                    "reason": "missing required columns",
                }
            )
        if dataset["unexpected_columns"]:
            warnings.append(
                {
                    "report": "schema_validation_report",
                    "dataset_profile": dataset["dataset_profile"],
                    "reason": "unexpected columns listed for operator review",
                }
            )
    for report_name, status_key in {
        "bar_count_consistency_report": "bar_count_consistency_status",
        "date_range_coverage_report": "date_range_coverage_status",
        "ohlc_consistency_report": "ohlc_consistency_status",
        "volume_consistency_report": "volume_consistency_status",
    }.items():
        if reports[report_name][status_key] != "PASS":
            failures.append({"report": report_name, "reason": reports[report_name][status_key]})
    return _report(
        "failure_reason_inventory",
        {
            "failure_count": len(failures),
            "warning_count": len(warnings),
            "failures": failures,
            "warnings": warnings,
        },
    )


def _operator_review_summary(reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    load_report = reports["dataset_load_report"]
    return _report(
        "operator_review_summary",
        {
            "execution_request_id": candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
            "dataset_count": load_report["dataset_count"],
            "generated_output_count": len(OUTPUT_NAMES),
            "schema_validation_status": reports["schema_validation_report"]["schema_validation_status"],
            "bar_count_consistency_status": reports["bar_count_consistency_report"][
                "bar_count_consistency_status"
            ],
            "date_range_coverage_status": reports["date_range_coverage_report"][
                "date_range_coverage_status"
            ],
            "ohlc_consistency_status": reports["ohlc_consistency_report"]["ohlc_consistency_status"],
            "volume_consistency_status": reports["volume_consistency_report"][
                "volume_consistency_status"
            ],
            "indicator_calculation_status": reports["indicator_calculation_report"][
                "indicator_calculation_status"
            ],
            "module_compatibility_status": reports["module_compatibility_matrix"][
                "module_compatibility_status"
            ],
            "failure_count": reports["failure_reason_inventory"]["failure_count"],
            "warning_count": reports["failure_reason_inventory"]["warning_count"],
            "performance_acceptance": "NOT_ACCEPTED",
            "runtime_authorization": "NOT_AUTHORIZED",
        },
    )


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def _build_reports(
    *,
    entries: list[dict[str, Any]],
    rows_by_profile: dict[str, list[dict[str, Any]]],
    run_timestamp_utc: str,
    output_root: Path,
) -> dict[str, dict[str, Any]]:
    reports: dict[str, dict[str, Any]] = {}
    reports["dataset_load_report"] = _dataset_load_report(entries, rows_by_profile)
    reports["schema_validation_report"] = _schema_validation_report(rows_by_profile)
    reports["bar_count_consistency_report"] = _bar_count_report(rows_by_profile)
    reports["date_range_coverage_report"] = _date_range_report(rows_by_profile)
    reports["null_field_summary_report"] = _null_summary_report(rows_by_profile)
    reports["ohlc_consistency_report"] = _ohlc_report(rows_by_profile)
    reports["volume_consistency_report"] = _volume_report(rows_by_profile)
    reports["indicator_calculation_report"] = _indicator_report(rows_by_profile)
    reports["module_compatibility_matrix"] = _module_compatibility_report()
    reports["failure_reason_inventory"] = _failure_inventory(reports)
    reports["operator_review_summary"] = _operator_review_summary(reports)
    reports["research_campaign_run_manifest"] = _report(
        "research_campaign_run_manifest",
        {
            "run_id": f"AAPL_RESEARCH_APPLICABILITY_EXECUTION_V1_{run_timestamp_utc}",
            "execution_request_id": candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
            "run_timestamp_utc": run_timestamp_utc,
            "source_digests": {
                "research_campaign_execution_approval_digest": EXPECTED_APPROVAL_DIGEST,
                "execution_candidate_digest": approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
                "execution_candidate_review_package_digest": (
                    approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
                ),
                "campaign_plan_digest": (
                    candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST
                ),
                "campaign_plan_review_package_digest": (
                    candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
                ),
                "dataset_availability_review_package_digest": (
                    candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
                ),
            },
            "output_paths": {
                name: str((output_root / f"{name}.json").as_posix()) for name in OUTPUT_NAMES
            },
            "output_digests": {name: None for name in OUTPUT_NAMES},
            "boundary_flags": {
                "provider_requests_made": False,
                "runtime_migration_approved": False,
                "runtime_migration_active": False,
                "strategy_runtime_migration": False,
                "automatic_stitching": False,
            },
        },
    )
    return reports


def _blocked_artifact(
    *,
    entries: list[dict[str, Any]],
    run_timestamp_utc: str,
    output_root: Path,
) -> dict[str, Any]:
    summary = availability._summary(entries)
    return {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_V1,
        "execution_status": RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED,
        "execution_request_id": candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
        "run_timestamp_utc": run_timestamp_utc,
        "output_root_path": str(output_root.as_posix()),
        "campaign_execution_authorized": True,
        "campaign_execution_performed": False,
        "campaign_results_generated": False,
        "research_only": True,
        "provider_requests_made": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "dataset_verification_summary": summary,
        "verification_entries": entries,
    }


def _execution_digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("research_applicability_campaign_execution_digest", None)
    return payload


def research_applicability_campaign_execution_digest_v1(artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for an executed research campaign."""
    return semantic_digest(_execution_digest_payload(artifact))


def build_research_applicability_campaign_execution_run_v1(
    *,
    search_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute the approved read-only research campaign and write ignored report files."""
    timestamp = run_timestamp_utc or _utc_now()
    search_path = _resolve_root(search_root, Path("."))
    output_path = _resolve_root(output_root, DEFAULT_OUTPUT_ROOT)
    entries = availability.verify_research_dataset_files_v1(search_root=search_path)
    verification_summary = availability._summary(entries)
    if not verification_summary["ready_for_research_campaign_planning"]:
        return _blocked_artifact(entries=entries, run_timestamp_utc=timestamp, output_root=output_path)

    rows_by_profile = _read_rows_by_profile(search_path, entries)
    reports = _build_reports(
        entries=entries,
        rows_by_profile=rows_by_profile,
        run_timestamp_utc=timestamp,
        output_root=output_path,
    )
    output_digests: dict[str, str] = {}
    for name in OUTPUT_NAMES:
        if name == "research_campaign_run_manifest":
            continue
        output_digests[name] = _write_json(output_path / f"{name}.json", reports[name])
    reports["research_campaign_run_manifest"]["output_digests"].update(output_digests)
    reports["research_campaign_run_manifest"]["output_digests"][
        "research_campaign_run_manifest"
    ] = sha256_bytes(canonical_json_bytes(reports["research_campaign_run_manifest"]))
    run_manifest_digest = _write_json(
        output_path / "research_campaign_run_manifest.json",
        reports["research_campaign_run_manifest"],
    )
    output_digests["research_campaign_run_manifest"] = run_manifest_digest

    load_report = reports["dataset_load_report"]
    schema_report = reports["schema_validation_report"]
    bar_count_report = reports["bar_count_consistency_report"]
    date_range_report = reports["date_range_coverage_report"]
    ohlc_report = reports["ohlc_consistency_report"]
    volume_report = reports["volume_consistency_report"]
    indicator_report = reports["indicator_calculation_report"]
    module_report = reports["module_compatibility_matrix"]
    failure_report = reports["failure_reason_inventory"]
    by_profile = _entries_by_profile(entries)
    artifact = {
        "artifact_kind": ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED,
        "schema_version": SCHEMA_VERSION_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_V1,
        "execution_status": RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY,
        "execution_request_id": candidate.CAMPAIGN_EXECUTION_REQUEST_ID,
        "campaign_execution_authorized": True,
        "campaign_execution_performed": True,
        "campaign_results_generated": True,
        "research_only": True,
        "created_offline": True,
        "provider_requests_made": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "research_campaign_execution_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "execution_candidate_digest": approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "execution_candidate_review_package_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_plan_digest": candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "campaign_plan_review_package_digest": (
            candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_availability_review_package_digest": (
            candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": by_profile["SWING"]["registry_approval_digest"],
        "position_swing_registry_approval_digest": by_profile["POSITION_SWING"][
            "registry_approval_digest"
        ],
        "swing_dataset_rows_digest": by_profile["SWING"]["dataset_rows_digest_actual"],
        "position_swing_dataset_rows_digest": by_profile["POSITION_SWING"][
            "dataset_rows_digest_actual"
        ],
        "run_timestamp_utc": timestamp,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "output_root_path": str(output_path.as_posix()),
        "dataset_count": 2,
        "datasets_loaded_count": load_report["datasets_loaded_count"],
        "datasets_digest_verified_count": load_report["datasets_digest_verified_count"],
        "planned_output_count": len(OUTPUT_NAMES),
        "generated_output_count": len(output_digests),
        "output_digest_manifest": {name: output_digests[name] for name in sorted(output_digests)},
        "failure_count": failure_report["failure_count"],
        "warning_count": failure_report["warning_count"],
        "research_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "swing_row_count": len(rows_by_profile["SWING"]),
        "position_swing_row_count": len(rows_by_profile["POSITION_SWING"]),
        "swing_expected_row_count": DATASET_EXPECTED_ROW_COUNTS["SWING"],
        "position_swing_expected_row_count": DATASET_EXPECTED_ROW_COUNTS["POSITION_SWING"],
        "schema_validation_status": schema_report["schema_validation_status"],
        "bar_count_consistency_status": bar_count_report["bar_count_consistency_status"],
        "date_range_coverage_status": date_range_report["date_range_coverage_status"],
        "ohlc_consistency_status": ohlc_report["ohlc_consistency_status"],
        "volume_consistency_status": volume_report["volume_consistency_status"],
        "indicator_calculation_status": indicator_report["indicator_calculation_status"],
        "module_compatibility_status": module_report["module_compatibility_status"],
        "reports": {
            name: {
                "path": str((output_path / f"{name}.json").as_posix()),
                "digest": output_digests[name],
                "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            }
            for name in OUTPUT_NAMES
        },
    }
    artifact["research_applicability_campaign_execution_digest"] = (
        research_applicability_campaign_execution_digest_v1(artifact)
    )
    validate_research_applicability_campaign_executed_v1(artifact)
    return artifact


def execute_research_applicability_campaign_v1(
    *,
    search_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Run the research-only applicability campaign using verified local datasets."""
    return build_research_applicability_campaign_execution_run_v1(
        search_root=search_root,
        output_root=output_root,
        run_timestamp_utc=run_timestamp_utc,
    )


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise ResearchApplicabilityCampaignExecutionError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ResearchApplicabilityCampaignExecutionError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ResearchApplicabilityCampaignExecutionError(f"{field_name} must be false")


def validate_research_applicability_campaign_executed_v1(artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate executed campaign artifacts while preserving non-runtime boundaries."""
    if not isinstance(artifact, dict):
        raise ResearchApplicabilityCampaignExecutionError("artifact must be a JSON object")
    _expect(
        artifact.get("artifact_kind"),
        ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED,
        "artifact_kind",
    )
    _expect(
        artifact.get("execution_status"),
        RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY,
        "execution_status",
    )
    for field in (
        "campaign_execution_authorized",
        "campaign_execution_performed",
        "campaign_results_generated",
        "research_only",
    ):
        _expect_true(artifact.get(field), field)
    for field in (
        "provider_requests_made",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    _expect(
        artifact.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(artifact.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "research_campaign_execution_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "execution_candidate_digest": approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "execution_candidate_review_package_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_plan_digest": candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_DIGEST,
        "campaign_plan_review_package_digest": (
            candidate.EXPECTED_RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_availability_review_package_digest": (
            candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
        ),
        "dataset_count": 2,
        "planned_output_count": len(OUTPUT_NAMES),
        "generated_output_count": len(OUTPUT_NAMES),
        "research_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
    }.items():
        _expect(artifact.get(field), expected, field)
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, dict) or sorted(manifest) != sorted(OUTPUT_NAMES):
        raise ResearchApplicabilityCampaignExecutionError("output_digest_manifest missing")
    reports = artifact.get("reports")
    if not isinstance(reports, dict) or sorted(reports) != sorted(OUTPUT_NAMES):
        raise ResearchApplicabilityCampaignExecutionError("reports missing")
    for name, report in reports.items():
        if not isinstance(report, dict):
            raise ResearchApplicabilityCampaignExecutionError("report entry must be object")
        _expect(report.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, f"{name}.output_label")
    digest = artifact.get("research_applicability_campaign_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ResearchApplicabilityCampaignExecutionError(
            "research_applicability_campaign_execution_digest missing"
        )
    _expect(
        digest,
        research_applicability_campaign_execution_digest_v1(artifact),
        "research_applicability_campaign_execution_digest",
    )
    return {
        "status": "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_VALID",
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "execution_request_id": artifact["execution_request_id"],
        "research_applicability_campaign_execution_digest": digest,
        "generated_output_count": artifact["generated_output_count"],
        "failure_count": artifact["failure_count"],
        "warning_count": artifact["warning_count"],
        "campaign_execution_authorized": True,
        "campaign_execution_performed": True,
        "campaign_results_generated": True,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def write_research_applicability_campaign_execution_status_markdown_v1(
    artifact: dict[str, Any],
) -> str:
    """Render a sanitized status document for the research campaign execution."""
    validation = validate_research_applicability_campaign_executed_v1(artifact)
    lines = [
        "# MarketFlow Research Applicability Campaign Execution Status",
        "",
        "## Branch And Commit",
        f"- Branch: `{artifact['branch']}`",
        f"- Base commit: `{artifact['base_commit']}`",
        "- Implementation commit: the commit containing this document.",
        "",
        "## Execution Artifact",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Execution status: `{artifact['execution_status']}`",
        f"- Execution digest: `{validation['research_applicability_campaign_execution_digest']}`",
        f"- Execution request ID: `{artifact['execution_request_id']}`",
        f"- Execution timestamp UTC: `{artifact['run_timestamp_utc']}`",
        "",
        "## Outputs Generated Summary",
        f"- Output root path: `{artifact['output_root_path']}`",
        f"- Planned output count: `{artifact['planned_output_count']}`",
        f"- Generated output count: `{artifact['generated_output_count']}`",
        f"- Research output label: `{artifact['research_outputs_label']}`",
        "",
        "## Output Digest Manifest",
    ]
    lines.extend(f"- `{name}`: `{digest}`" for name, digest in artifact["output_digest_manifest"].items())
    lines.extend(
        [
            "",
            "## Dataset Load Summary",
            f"- Dataset count: `{artifact['dataset_count']}`",
            f"- Datasets loaded count: `{artifact['datasets_loaded_count']}`",
            f"- Dataset digests verified count: `{artifact['datasets_digest_verified_count']}`",
            f"- SWING row count: `{artifact['swing_row_count']}`",
            f"- POSITION_SWING row count: `{artifact['position_swing_row_count']}`",
            "",
            "## Schema Bar Date Null OHLC Volume Indicator Module Summaries",
            f"- Schema validation status: `{artifact['schema_validation_status']}`",
            f"- Bar count consistency status: `{artifact['bar_count_consistency_status']}`",
            f"- Date range coverage status: `{artifact['date_range_coverage_status']}`",
            "- Null field summary report: generated under the ignored output root.",
            f"- OHLC consistency status: `{artifact['ohlc_consistency_status']}`",
            f"- Volume consistency status: `{artifact['volume_consistency_status']}`",
            f"- Indicator calculation status: `{artifact['indicator_calculation_status']}`",
            f"- Module compatibility status: `{artifact['module_compatibility_status']}`",
            "",
            "## Failure Warning Count",
            f"- Failure count: `{artifact['failure_count']}`",
            f"- Warning count: `{artifact['warning_count']}`",
            "",
            "## Runtime Boundary",
            f"- provider_requests_made: `{artifact['provider_requests_made']}`",
            f"- runtime_migration_approved: `{artifact['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{artifact['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{artifact['strategy_runtime_migration']}`",
            f"- runtime_use: `{artifact['runtime_use']}`",
            f"- strategy_use: `{artifact['strategy_use']}`",
            f"- paper_trading: `{artifact['paper_trading']}`",
            f"- broker_execution: `{artifact['broker_execution']}`",
            f"- automatic_stitching: `{artifact['automatic_stitching']}`",
            "",
            "## Predictive Profitability Boundary",
            f"- predictive_usefulness: `{artifact['predictive_usefulness']}`",
            f"- profitability: `{artifact['profitability']}`",
            "- No predictive-usefulness acceptance was created.",
            "- No profitability acceptance was created.",
            "",
            "## Non-Goals",
            "- No Massive.com / Polygon provider request was made.",
            "- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.",
            "- No default runtime dataset source was changed.",
            "- No Strategy runtime behavior was modified.",
            "- No broker or paper trading action was performed.",
            "- No trade recommendations were produced.",
            "- No runtime migration or runtime activation was approved.",
            "",
            "## Next Task",
            "- Research applicability campaign execution results operator review package.",
            "",
        ]
    )
    return "\n".join(lines)
