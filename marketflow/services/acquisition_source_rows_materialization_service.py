"""Materialize frozen acquisition source rows for downstream canonical datasets."""

from __future__ import annotations

import csv
import json
import os
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_operator_freeze_service as acquisition_freeze
from marketflow.services import acquisition_generation_service as acquisition


ARTIFACT_KIND_ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION = "ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION"
SCHEMA_VERSION_ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_V1 = "acquisition_frozen_source_rows_materialization_v1"
ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED = "ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED"
ACQUISITION_FROZEN_SOURCE_ROWS_ALREADY_AVAILABLE_VERIFIED = "ACQUISITION_FROZEN_SOURCE_ROWS_ALREADY_AVAILABLE_VERIFIED"
ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_REQUIRES_LIVE_PROVIDER_EXECUTION = (
    "ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_REQUIRES_LIVE_PROVIDER_EXECUTION"
)
ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_DIGEST_MISMATCH = (
    "ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_DIGEST_MISMATCH"
)
ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_BLOCKED = "ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_BLOCKED"
ACQUISITION_SOURCE_ROWS_MATERIALIZATION_BLOCKED_MISSING_API_KEY = (
    "ACQUISITION_SOURCE_ROWS_MATERIALIZATION_BLOCKED_MISSING_API_KEY"
)
ACQUISITION_SOURCE_ROWS_MATERIALIZATION_BLOCKED_GATE_NOT_ENABLED = (
    "ACQUISITION_SOURCE_ROWS_MATERIALIZATION_BLOCKED_GATE_NOT_ENABLED"
)
LIVE_RECONSTRUCTION_OF_FROZEN_NORMALIZED_ROWS = "LIVE_RECONSTRUCTION_OF_FROZEN_NORMALIZED_ROWS"
FAKE_TRANSPORT_RECONSTRUCTION_OF_NORMALIZED_ROWS = "FAKE_TRANSPORT_RECONSTRUCTION_OF_NORMALIZED_ROWS"
LOCAL_VERIFIED_FROZEN_SOURCE_ROWS = "LOCAL_VERIFIED_FROZEN_SOURCE_ROWS"

MARKETFLOW_ENABLE_LIVE_ACQUISITION_MATERIALIZATION = "MARKETFLOW_ENABLE_LIVE_ACQUISITION_MATERIALIZATION"
EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST = "df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118"
EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST = acquisition_freeze.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
EXPECTED_MONTHLY_RECONCILIATION_DIGEST = acquisition_freeze.EXPECTED_MONTHLY_RECONCILIATION_DIGEST
DEFAULT_OUTPUT_ROOT = Path(".marketflow") / "frozen_acquisition_sources" / "AAPL" / "2022_2025"
DEFAULT_ROWS_FILENAME = "AAPL_15m_adjusted_2022_2025_normalized_source_rows.csv"
DEFAULT_MANIFEST_FILENAME = "AAPL_15m_adjusted_2022_2025_source_rows_manifest.json"

NORMALIZED_SOURCE_ROW_COLUMNS = [
    "ticker",
    "timestamp_utc",
    "timestamp_source",
    "timestamp_source_timezone",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "vwap",
    "transactions",
    "otc",
    "adjusted",
    "source_interval_minutes",
    "source_row_index",
    "source_chunk_id",
    "source_month",
    "raw_row_digest",
]


class AcquisitionSourceRowsMaterializationError(ValueError):
    """Raised when materialized acquisition source rows violate guardrails."""


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise AcquisitionSourceRowsMaterializationError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise AcquisitionSourceRowsMaterializationError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise AcquisitionSourceRowsMaterializationError(f"{field_name} must be true")


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _authority_digests() -> dict[str, Any]:
    return {
        "identity_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_generation_frozen_digest": EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "acquisition_candidate_digest": acquisition_freeze.EXPECTED_ACQUISITION_CANDIDATE_DIGEST,
        "frozen_monthly_reconciliation_digest": EXPECTED_MONTHLY_RECONCILIATION_DIGEST,
    }


def _source_metadata() -> dict[str, Any]:
    return {
        "source_ticker": "AAPL",
        "source_range_start": "2022-01-01",
        "source_range_end": "2025-12-31",
        "source_interval_minutes": 15,
        "source_adjusted": True,
        "source_sort": "asc",
        "monthly_chunk_count": 48,
    }


def _empty_result(status: str, *, expected_normalized_source_rows_digest: str, request_timestamp_utc: str | None = None) -> dict[str, Any]:
    result = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION,
        "schema_version": SCHEMA_VERSION_ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_V1,
        "materialization_status": status,
        "created_offline": True,
        "provider_requests_made": False,
        "provider_response_injected": False,
        "source_rows_materialized": False,
        "source_rows_verified_against_frozen_digest": False,
        "expected_normalized_source_rows_digest": expected_normalized_source_rows_digest,
        "actual_normalized_source_rows_digest": None,
        "digest_match": False,
        "row_count": 0,
        "rth_row_count": 0,
        "extended_hours_row_count": 0,
        "unknown_row_count": 0,
        "out_of_calendar_row_count": 0,
        "output_rows_path": None,
        "output_manifest_path": None,
        "rows_file_sha256": None,
        "manifest_file_sha256": None,
        "materialization_chunk_manifest_digest": acquisition.chunk_manifest_digest_v1(acquisition.build_acquisition_month_chunks_v1()),
        "materialization_provider_raw_response_digest": None,
        "materialization_monthly_reconciliation_digest": None,
        "monthly_reconciliation_digest_matches_frozen": False,
        "monthly_reconciliation_digest_mismatch_explanation": None,
        "materialization_receipt_digest": None,
        "materialization_status_digest": None,
        "materialization_mode": None,
        "blocked_reason": None,
        "local_matching_rows_already_available": False,
        "new_acquisition_authority_created": False,
        "frozen_acquisition_digest_replaced": False,
        "api_key_stored": False,
        "raw_provider_payload_stored": False,
        "acquisition_generation_frozen_created": False,
        "swing_canonical_dataset_frozen_created": False,
        "canonical_dataset_approved": False,
        "registry_eligible": False,
        "request_timestamp_utc": request_timestamp_utc,
        **_authority_boundary(),
        **_authority_digests(),
        **_source_metadata(),
    }
    _finalize_digests(result)
    return result


def _receipt_payload(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": result.get("artifact_kind"),
        "materialization_status": result.get("materialization_status"),
        "materialization_mode": result.get("materialization_mode"),
        "expected_normalized_source_rows_digest": result.get("expected_normalized_source_rows_digest"),
        "actual_normalized_source_rows_digest": result.get("actual_normalized_source_rows_digest"),
        "digest_match": result.get("digest_match"),
        "row_count": result.get("row_count"),
        "rth_row_count": result.get("rth_row_count"),
        "extended_hours_row_count": result.get("extended_hours_row_count"),
        "unknown_row_count": result.get("unknown_row_count"),
        "provider_requests_made": result.get("provider_requests_made"),
        "provider_response_injected": result.get("provider_response_injected"),
        "new_acquisition_authority_created": result.get("new_acquisition_authority_created"),
        "frozen_acquisition_digest_replaced": result.get("frozen_acquisition_digest_replaced"),
    }


def _status_digest_payload(result: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(result)
    payload.pop("materialization_status_digest", None)
    payload.pop("manifest_file_sha256", None)
    return payload


def _finalize_digests(result: dict[str, Any]) -> None:
    result["materialization_receipt_digest"] = semantic_digest(_receipt_payload(result))
    result["materialization_status_digest"] = semantic_digest(_status_digest_payload(result))


def _to_csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _from_csv_value(field: str, value: str) -> Any:
    if value == "":
        return None
    if field in {"timestamp_source", "transactions", "source_interval_minutes", "source_row_index"}:
        return int(value)
    if field in {"adjusted", "otc"}:
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        raise AcquisitionSourceRowsMaterializationError(f"{field} must be boolean text")
    return value


def _read_rows_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != NORMALIZED_SOURCE_ROW_COLUMNS:
            raise AcquisitionSourceRowsMaterializationError("rows CSV header mismatch")
        return [{field: _from_csv_value(field, row[field]) for field in NORMALIZED_SOURCE_ROW_COLUMNS} for row in reader]


def _write_rows_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=NORMALIZED_SOURCE_ROW_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _to_csv_value(row.get(field)) for field in NORMALIZED_SOURCE_ROW_COLUMNS})


def _row_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    classified = acquisition.classify_normalized_source_rows_v1(rows)
    return {
        "row_count": len(rows),
        "rth_row_count": sum(1 for row in classified if row.get("session_classification") == acquisition.RTH),
        "extended_hours_row_count": sum(1 for row in classified if row.get("session_classification") == acquisition.EXTENDED_HOURS),
        "unknown_row_count": sum(1 for row in classified if row.get("session_classification") == acquisition.UNKNOWN),
        "out_of_calendar_row_count": sum(1 for row in classified if row.get("session_classification") == acquisition.OUT_OF_CALENDAR_RANGE),
    }


def _safe_output_root(output_root: str | Path) -> Path:
    root = Path(output_root)
    if ".marketflow" not in root.parts:
        raise AcquisitionSourceRowsMaterializationError("materialized rows output must be under ignored .marketflow")
    return root


def _manifest_payload(result: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "artifact_kind",
        "schema_version",
        "materialization_status",
        "materialization_mode",
        "source_rows_materialized",
        "source_rows_verified_against_frozen_digest",
        "expected_normalized_source_rows_digest",
        "actual_normalized_source_rows_digest",
        "digest_match",
        "row_count",
        "rth_row_count",
        "extended_hours_row_count",
        "unknown_row_count",
        "out_of_calendar_row_count",
        "output_rows_path",
        "rows_file_sha256",
        "monthly_chunk_count",
        "materialization_chunk_manifest_digest",
        "materialization_provider_raw_response_digest",
        "materialization_monthly_reconciliation_digest",
        "materialization_receipt_digest",
        "new_acquisition_authority_created",
        "frozen_acquisition_digest_replaced",
        "api_key_stored",
        "raw_provider_payload_stored",
        "acquisition_generation_frozen_created",
        "swing_canonical_dataset_frozen_created",
        "canonical_dataset_approved",
        "registry_eligible",
        "identity_frozen_digest",
        "calendar_frozen_digest",
        "schedule_digest",
        "split_event_frozen_digest",
        "dividend_event_frozen_digest",
        "acquisition_generation_frozen_digest",
        "acquisition_candidate_digest",
        "frozen_monthly_reconciliation_digest",
    }
    return {key: deepcopy(result.get(key)) for key in sorted(allowed)}


def _write_verified_outputs(output_root: Path, rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
    rows_path = output_root / DEFAULT_ROWS_FILENAME
    manifest_path = output_root / DEFAULT_MANIFEST_FILENAME
    _write_rows_csv(rows_path, rows)
    result["output_rows_path"] = str(rows_path)
    result["rows_file_sha256"] = sha256_bytes(rows_path.read_bytes())
    result["output_manifest_path"] = str(manifest_path)
    manifest_path.write_bytes(canonical_json_bytes(_manifest_payload(result)))
    result["manifest_file_sha256"] = sha256_bytes(manifest_path.read_bytes())
    _finalize_digests(result)
    manifest_path.write_bytes(canonical_json_bytes(_manifest_payload(result)))
    result["manifest_file_sha256"] = sha256_bytes(manifest_path.read_bytes())


def validate_materialized_frozen_acquisition_source_rows_v1(
    *,
    rows_path: str | Path,
    expected_normalized_source_rows_digest: str,
) -> dict[str, Any]:
    """Validate a row-level normalized acquisition source rows file."""
    path = Path(rows_path)
    rows = _read_rows_csv(path) if path.suffix.lower() == ".csv" else _read_rows_json(path)
    actual_digest = acquisition.normalized_source_rows_digest_v1(rows)
    if actual_digest != expected_normalized_source_rows_digest:
        raise AcquisitionSourceRowsMaterializationError("normalized_source_rows_digest mismatch")
    counts = _row_counts(rows)
    return {
        "status": "ACQUISITION_FROZEN_SOURCE_ROWS_FILE_VALID",
        "rows_path": str(path),
        "expected_normalized_source_rows_digest": expected_normalized_source_rows_digest,
        "actual_normalized_source_rows_digest": actual_digest,
        "digest_match": True,
        "rows_file_sha256": sha256_bytes(path.read_bytes()),
        **counts,
    }


def _read_rows_json(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
        return payload["rows"]
    if isinstance(payload, list):
        return payload
    raise AcquisitionSourceRowsMaterializationError("rows JSON must be a list or object with rows")


def _candidate_row_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if not root.exists():
        return []
    paths: list[Path] = []
    for pattern in ("*normalized_source_rows.csv", "*normalized_source_rows.json", "*source_rows.csv", "*source_rows.json"):
        paths.extend(root.rglob(pattern))
    return sorted(set(paths))


def locate_frozen_acquisition_source_rows_v1(
    *,
    search_root: str | Path | None = None,
    expected_normalized_source_rows_digest: str | None = None,
) -> dict[str, Any]:
    """Locate an ignored row-level source artifact and verify its semantic digest."""
    expected = expected_normalized_source_rows_digest or EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
    root = Path(search_root) if search_root is not None else DEFAULT_OUTPUT_ROOT
    for path in _candidate_row_paths(root):
        try:
            validation = validate_materialized_frozen_acquisition_source_rows_v1(
                rows_path=path,
                expected_normalized_source_rows_digest=expected,
            )
        except (OSError, json.JSONDecodeError, AcquisitionSourceRowsMaterializationError):
            continue
        result = _empty_result(
            ACQUISITION_FROZEN_SOURCE_ROWS_ALREADY_AVAILABLE_VERIFIED,
            expected_normalized_source_rows_digest=expected,
        )
        result.update(
            {
                "materialization_mode": LOCAL_VERIFIED_FROZEN_SOURCE_ROWS,
                "source_rows_materialized": True,
                "source_rows_verified_against_frozen_digest": True,
                "actual_normalized_source_rows_digest": validation["actual_normalized_source_rows_digest"],
                "digest_match": True,
                "output_rows_path": validation["rows_path"],
                "rows_file_sha256": validation["rows_file_sha256"],
                "local_matching_rows_already_available": True,
                **{key: validation[key] for key in ("row_count", "rth_row_count", "extended_hours_row_count", "unknown_row_count")},
                "out_of_calendar_row_count": validation["out_of_calendar_row_count"],
            }
        )
        _finalize_digests(result)
        validate_acquisition_frozen_source_rows_materialization_result_v1(result)
        return result
    return _empty_result(
        ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_REQUIRES_LIVE_PROVIDER_EXECUTION,
        expected_normalized_source_rows_digest=expected,
    )


def _api_key_from_environment() -> str | None:
    return os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")


def materialize_frozen_acquisition_source_rows_v1(
    *,
    output_root: str | Path,
    api_key: str | None = None,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    allow_live: bool = False,
    request_timestamp_utc: str | None = None,
    expected_normalized_source_rows_digest: str | None = None,
    require_monthly_reconciliation_digest_match: bool = True,
) -> dict[str, Any]:
    """Recreate row-level normalized acquisition source rows and verify against the frozen digest."""
    expected = expected_normalized_source_rows_digest or EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
    timestamp = request_timestamp_utc or _utc_now()
    root = _safe_output_root(output_root)
    if transport is None and (
        not allow_live or os.environ.get(MARKETFLOW_ENABLE_LIVE_ACQUISITION_MATERIALIZATION) != "1"
    ):
        result = _empty_result(
            ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_REQUIRES_LIVE_PROVIDER_EXECUTION,
            expected_normalized_source_rows_digest=expected,
            request_timestamp_utc=timestamp,
        )
        result["blocked_reason"] = ACQUISITION_SOURCE_ROWS_MATERIALIZATION_BLOCKED_GATE_NOT_ENABLED
        _finalize_digests(result)
        return result
    key = api_key or _api_key_from_environment()
    if not key:
        result = _empty_result(
            ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_BLOCKED,
            expected_normalized_source_rows_digest=expected,
            request_timestamp_utc=timestamp,
        )
        result["blocked_reason"] = ACQUISITION_SOURCE_ROWS_MATERIALIZATION_BLOCKED_MISSING_API_KEY
        result["materialization_mode"] = LIVE_RECONSTRUCTION_OF_FROZEN_NORMALIZED_ROWS if transport is None else FAKE_TRANSPORT_RECONSTRUCTION_OF_NORMALIZED_ROWS
        _finalize_digests(result)
        return result
    candidate = acquisition.build_acquisition_generation_live_candidate_v1(
        api_key=key,
        transport=transport,
        provider_request_timestamp_utc=timestamp,
    )
    rows = deepcopy(candidate.get("normalized_source_rows") or [])
    actual_digest = acquisition.normalized_source_rows_digest_v1(rows)
    counts = _row_counts(rows)
    monthly_digest = candidate.get("monthly_reconciliation_digest")
    monthly_match = monthly_digest == EXPECTED_MONTHLY_RECONCILIATION_DIGEST
    digest_match = actual_digest == expected
    accepted = digest_match and (monthly_match or not require_monthly_reconciliation_digest_match)
    result = _empty_result(
        ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED if accepted else ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_DIGEST_MISMATCH,
        expected_normalized_source_rows_digest=expected,
        request_timestamp_utc=timestamp,
    )
    result.update(
        {
            "created_offline": transport is not None,
            "provider_requests_made": transport is None,
            "provider_response_injected": transport is not None,
            "source_rows_materialized": accepted,
            "source_rows_verified_against_frozen_digest": accepted,
            "actual_normalized_source_rows_digest": actual_digest,
            "digest_match": digest_match,
            "materialization_mode": LIVE_RECONSTRUCTION_OF_FROZEN_NORMALIZED_ROWS if transport is None else FAKE_TRANSPORT_RECONSTRUCTION_OF_NORMALIZED_ROWS,
            "materialization_provider_raw_response_digest": candidate.get("provider_raw_response_digest"),
            "materialization_monthly_reconciliation_digest": monthly_digest,
            "monthly_reconciliation_digest_matches_frozen": monthly_match,
            "monthly_reconciliation_digest_mismatch_explanation": None
            if monthly_match
            else "MATERIALIZED_MONTHLY_RECONCILIATION_DIGEST_DIFFERS_FROM_FROZEN_DIGEST",
            **counts,
        }
    )
    if accepted:
        _write_verified_outputs(root, rows, result)
    else:
        _finalize_digests(result)
    validate_acquisition_frozen_source_rows_materialization_result_v1(result)
    return result


def validate_acquisition_frozen_source_rows_materialization_result_v1(result: dict[str, Any]) -> dict[str, Any]:
    """Validate materialization status and authority boundaries."""
    if not isinstance(result, dict):
        raise AcquisitionSourceRowsMaterializationError("materialization result must be a JSON object")
    _expect(result.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION, "artifact_kind")
    _expect(result.get("schema_version"), SCHEMA_VERSION_ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_V1, "schema_version")
    if result.get("materialization_status") not in {
        ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED,
        ACQUISITION_FROZEN_SOURCE_ROWS_ALREADY_AVAILABLE_VERIFIED,
        ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_REQUIRES_LIVE_PROVIDER_EXECUTION,
        ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_DIGEST_MISMATCH,
        ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_BLOCKED,
    }:
        raise AcquisitionSourceRowsMaterializationError("materialization_status mismatch")
    for field in ("identity_segment_frozen", "calendar_operator_frozen", "split_event_audit_frozen", "dividend_event_audit_frozen", "acquisition_generation_freeze"):
        _expect_true(result.get(field), field)
    for field in (
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
        "new_acquisition_authority_created",
        "frozen_acquisition_digest_replaced",
        "api_key_stored",
        "raw_provider_payload_stored",
        "acquisition_generation_frozen_created",
        "swing_canonical_dataset_frozen_created",
        "canonical_dataset_approved",
        "registry_eligible",
    ):
        _expect_false(result.get(field), field)
    _expect(result.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(result.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in _authority_digests().items():
        _expect(result.get(field), expected, field)
    if result.get("source_rows_verified_against_frozen_digest") is True:
        _expect_true(result.get("source_rows_materialized"), "source_rows_materialized")
        _expect_true(result.get("digest_match"), "digest_match")
        _expect(result.get("actual_normalized_source_rows_digest"), result.get("expected_normalized_source_rows_digest"), "actual_normalized_source_rows_digest")
        if not result.get("output_rows_path"):
            raise AcquisitionSourceRowsMaterializationError("output_rows_path missing")
    if result.get("digest_match") is False and result.get("materialization_status") in {
        ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED,
        ACQUISITION_FROZEN_SOURCE_ROWS_ALREADY_AVAILABLE_VERIFIED,
    }:
        raise AcquisitionSourceRowsMaterializationError("digest_match must be true for accepted materialization")
    _expect(result.get("materialization_receipt_digest"), semantic_digest(_receipt_payload(result)), "materialization_receipt_digest")
    status_digest = result.get("materialization_status_digest")
    if not isinstance(status_digest, str) or len(status_digest) != 64:
        raise AcquisitionSourceRowsMaterializationError("materialization_status_digest missing")
    _expect(status_digest, semantic_digest(_status_digest_payload(result)), "materialization_status_digest")
    return {
        "status": "ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_VALID",
        "artifact_kind": result["artifact_kind"],
        "materialization_status": result["materialization_status"],
        "expected_normalized_source_rows_digest": result["expected_normalized_source_rows_digest"],
        "actual_normalized_source_rows_digest": result["actual_normalized_source_rows_digest"],
        "digest_match": result["digest_match"],
        "row_count": result["row_count"],
        "rth_row_count": result["rth_row_count"],
        "extended_hours_row_count": result["extended_hours_row_count"],
        "unknown_row_count": result["unknown_row_count"],
        "materialization_receipt_digest": result["materialization_receipt_digest"],
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def build_acquisition_frozen_source_rows_materialization_status_markdown_v1(
    materialization_result: dict[str, Any],
) -> str:
    """Render sanitized materialization status without rows, payloads, or secrets."""
    validate_acquisition_frozen_source_rows_materialization_result_v1(materialization_result)
    lines = [
        "# MarketFlow Acquisition Frozen Source Rows Materialization Status",
        "",
        "## Materialization",
        f"- Artifact kind: `{materialization_result['artifact_kind']}`",
        f"- Materialization status: `{materialization_result['materialization_status']}`",
        f"- Materialization mode: `{materialization_result['materialization_mode']}`",
        f"- Local matching rows already available: `{materialization_result['local_matching_rows_already_available']}`",
        f"- Live materialization ran: `{materialization_result['provider_requests_made']}`",
        f"- Provider response injected: `{materialization_result['provider_response_injected']}`",
        f"- Blocked reason: `{materialization_result['blocked_reason']}`",
        "",
        "## Frozen Acquisition Binding",
        f"- Source acquisition frozen digest: `{materialization_result['acquisition_generation_frozen_digest']}`",
        f"- Acquisition candidate digest: `{materialization_result['acquisition_candidate_digest']}`",
        f"- Expected normalized source rows digest: `{materialization_result['expected_normalized_source_rows_digest']}`",
        f"- Actual normalized source rows digest: `{materialization_result['actual_normalized_source_rows_digest']}`",
        f"- Digest match result: `{materialization_result['digest_match']}`",
        "",
        "## Row Summary",
        f"- Row count: `{materialization_result['row_count']}`",
        f"- RTH row count: `{materialization_result['rth_row_count']}`",
        f"- Extended-hours row count: `{materialization_result['extended_hours_row_count']}`",
        f"- Unknown row count: `{materialization_result['unknown_row_count']}`",
        f"- Out-of-calendar row count: `{materialization_result['out_of_calendar_row_count']}`",
        f"- Materialized rows path: `{materialization_result['output_rows_path']}`",
        f"- Materialization manifest path: `{materialization_result['output_manifest_path']}`",
        "",
        "## Materialization Digests",
        f"- Chunk manifest digest: `{materialization_result['materialization_chunk_manifest_digest']}`",
        f"- Provider raw response digest: `{materialization_result['materialization_provider_raw_response_digest']}`",
        f"- Monthly reconciliation digest: `{materialization_result['materialization_monthly_reconciliation_digest']}`",
        f"- Monthly reconciliation digest matched frozen: `{materialization_result['monthly_reconciliation_digest_matches_frozen']}`",
        f"- Monthly reconciliation mismatch explanation: `{materialization_result['monthly_reconciliation_digest_mismatch_explanation']}`",
        f"- Materialization receipt digest: `{materialization_result['materialization_receipt_digest']}`",
        f"- Materialization status digest: `{materialization_result['materialization_status_digest']}`",
        "",
        "## Authority Boundary",
        f"- identity_segment_frozen: `{materialization_result['identity_segment_frozen']}`",
        f"- calendar_operator_frozen: `{materialization_result['calendar_operator_frozen']}`",
        f"- split_event_audit_frozen: `{materialization_result['split_event_audit_frozen']}`",
        f"- dividend_event_audit_frozen: `{materialization_result['dividend_event_audit_frozen']}`",
        f"- acquisition_generation_freeze: `{materialization_result['acquisition_generation_freeze']}`",
        f"- canonical_eligibility: `{materialization_result['canonical_eligibility']}`",
        f"- registry_eligibility: `{materialization_result['registry_eligibility']}`",
        f"- strategy_runtime_migration: `{materialization_result['strategy_runtime_migration']}`",
        f"- automatic_stitching: `{materialization_result['automatic_stitching']}`",
        f"- predictive_usefulness: `{materialization_result['predictive_usefulness']}`",
        f"- profitability: `{materialization_result['profitability']}`",
        "",
        "## Guardrails",
        f"- API key stored: `{materialization_result['api_key_stored']}`",
        f"- Raw provider payload stored: `{materialization_result['raw_provider_payload_stored']}`",
        f"- New acquisition authority created: `{materialization_result['new_acquisition_authority_created']}`",
        f"- Frozen acquisition digest replaced: `{materialization_result['frozen_acquisition_digest_replaced']}`",
        f"- Acquisition generation frozen created: `{materialization_result['acquisition_generation_frozen_created']}`",
        f"- SWING canonical dataset frozen created: `{materialization_result['swing_canonical_dataset_frozen_created']}`",
        f"- Canonical dataset approved: `{materialization_result['canonical_dataset_approved']}`",
        f"- Registry eligible: `{materialization_result['registry_eligible']}`",
        "- No raw/generated OHLCV rows are included in this document.",
        "",
        "## Next Task Recommendation",
    ]
    if materialization_result["source_rows_verified_against_frozen_digest"]:
        lines.append("- SWING candidate should be rerun using verified materialized frozen source rows.")
    else:
        lines.append("- SWING candidate remains blocked pending digest-correct source rows.")
    lines.append("")
    return "\n".join(lines)
