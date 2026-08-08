"""Offline POSITION_SWING canonical dataset candidate helpers."""

from __future__ import annotations

import csv
from copy import deepcopy
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import acquisition_source_rows_materialization_service as source_rows_materialization
from marketflow.services import exchange_calendar_evidence_service as calendar_service
from marketflow.services import swing_canonical_dataset_service as swing


ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE = "POSITION_SWING_CANONICAL_DATASET_CANDIDATE"
SCHEMA_VERSION_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_V1 = "position_swing_canonical_dataset_candidate_v1"
POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW = "POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW"
POSITION_SWING_CANONICAL_DATASET_REQUIRES_FROZEN_ACQUISITION_ROWS = (
    "POSITION_SWING_CANONICAL_DATASET_REQUIRES_FROZEN_ACQUISITION_ROWS"
)
POSITION_SWING_CANONICAL_DATASET_SOURCE_ROWS_DIGEST_MISMATCH = (
    "POSITION_SWING_CANONICAL_DATASET_SOURCE_ROWS_DIGEST_MISMATCH"
)

DATASET_PROFILE_POSITION_SWING = "POSITION_SWING"
DATASET_BAR_RULE_RTH_FULL_SESSION_1D = "RTH_FULL_SESSION_1D"
FULL_SESSION_SOURCE_ROW_COUNT = 26
POSITION_SWING_BARS_PER_FULL_SESSION = 1
SOURCE_ROWS_PER_POSITION_SWING_BAR = 26
POSITION_SWING_BAR_DURATION_MINUTES = 390
NOT_AUTHORIZED = "NOT_AUTHORIZED"

EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST = swing.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST
EXPECTED_ACQUISITION_CANDIDATE_DIGEST = swing.EXPECTED_ACQUISITION_CANDIDATE_DIGEST
EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST = swing.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
EXPECTED_MONTHLY_RECONCILIATION_DIGEST = swing.EXPECTED_MONTHLY_RECONCILIATION_DIGEST
EXPECTED_ACQUISITION_RECEIPT_DIGEST = swing.EXPECTED_ACQUISITION_RECEIPT_DIGEST
EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST = swing.EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST
EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST = swing.EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST
EXPECTED_MATERIALIZATION_RECEIPT_DIGEST = swing.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST

DEFAULT_SOURCE_ROWS_SEARCH_ROOT = swing.DEFAULT_SOURCE_ROWS_SEARCH_ROOT
DEFAULT_POSITION_SWING_CANDIDATE_OUTPUT_ROOT = (
    Path(".marketflow") / "canonical_candidates" / "AAPL" / "POSITION_SWING"
)

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


class PositionSwingCanonicalDatasetError(ValueError):
    """Raised when the POSITION_SWING canonical candidate violates its contract."""


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PositionSwingCanonicalDatasetError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PositionSwingCanonicalDatasetError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PositionSwingCanonicalDatasetError(f"{field_name} must be true")


def _special_session_policy() -> dict[str, Any]:
    return {
        "full_ordinary_sessions_only_for_RTH_FULL_SESSION_1D": True,
        "special_sessions_excluded_from_position_swing_bars": True,
        "special_sessions_recorded_in_exclusion_inventory": True,
        "special_session_exclusion_reason": "SPECIAL_SESSION_EXCLUDED_BY_CONSERVATIVE_FULL_SESSION_ONLY_POLICY",
    }


def _authority_bindings() -> dict[str, Any]:
    return {
        "identity_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_generation_frozen_digest": EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "acquisition_candidate_digest": EXPECTED_ACQUISITION_CANDIDATE_DIGEST,
        "normalized_source_rows_digest": EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST,
        "monthly_reconciliation_digest": EXPECTED_MONTHLY_RECONCILIATION_DIGEST,
        "acquisition_receipt_digest": EXPECTED_ACQUISITION_RECEIPT_DIGEST,
        "targeted_diagnostic_receipt_digest": EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST,
        "per_session_diagnostics_digest": EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST,
        "materialization_receipt_digest": EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
    }


def _source_acquisition_metadata() -> dict[str, Any]:
    return {
        "source_ticker": "AAPL",
        "source_range_start": "2022-01-01",
        "source_range_end": "2025-12-31",
        "source_interval_minutes": 15,
        "source_adjusted": True,
        "source_sort": "asc",
        "source_rows_total": 63804,
        "source_rth_rows_total": 25970,
        "source_extended_hours_rows_total": 37834,
        "source_unknown_rows_total": 0,
    }


def _dividend_implication() -> dict[str, Any]:
    return {
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "source_adjusted_data_used": True,
    }


def _candidate_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("position_swing_candidate_semantic_digest", None)
    return payload


def position_swing_candidate_semantic_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a POSITION_SWING candidate."""
    return semantic_digest(_candidate_digest_payload(candidate))


def dataset_rows_digest_v1(rows: list[dict[str, Any]]) -> str:
    return semantic_digest(rows)


def dataset_manifest_digest_v1(manifest: dict[str, Any]) -> str:
    payload = deepcopy(manifest)
    payload.pop("dataset_manifest_digest", None)
    return semantic_digest(payload)


def candidate_receipt_digest_v1(candidate: dict[str, Any]) -> str:
    return semantic_digest(
        {
            "artifact_kind": candidate.get("artifact_kind"),
            "candidate_status": candidate.get("candidate_status"),
            "dataset_profile": candidate.get("dataset_profile"),
            "dataset_bar_rule": candidate.get("dataset_bar_rule"),
            "acquisition_generation_frozen_digest": candidate.get("acquisition_generation_frozen_digest"),
            "normalized_source_rows_digest": candidate.get("normalized_source_rows_digest"),
            "dataset_rows_digest": candidate.get("dataset_rows_digest"),
            "dataset_manifest_digest": candidate.get("dataset_manifest_digest"),
            "provider_requests_made": candidate.get("provider_requests_made"),
            "canonical_dataset_frozen": candidate.get("canonical_dataset_frozen"),
        }
    )


def _bar_from_rows(rows: list[dict[str, Any]], *, session: dict[str, Any]) -> dict[str, Any]:
    if len(rows) != SOURCE_ROWS_PER_POSITION_SWING_BAR:
        raise PositionSwingCanonicalDatasetError("full ordinary POSITION_SWING bars require exactly 26 source rows")
    volume_sum = sum((swing._decimal(row.get("volume")) or Decimal("0")) for row in rows)
    transactions = [swing._int_or_none(row.get("transactions")) for row in rows]
    vwap_terms: list[Decimal] = []
    if volume_sum > 0 and all(row.get("vwap") not in (None, "") and row.get("volume") not in (None, "") for row in rows):
        for row in rows:
            vwap_terms.append((swing._decimal(row["vwap"]) or Decimal("0")) * (swing._decimal(row["volume"]) or Decimal("0")))
    weighted_vwap = sum(vwap_terms) / volume_sum if vwap_terms else None
    first = rows[0]
    last = rows[-1]
    market_open = swing._parse_utc(session["market_open_utc"])
    market_close = swing._parse_utc(session["market_close_utc"])
    return {
        "ticker": "AAPL",
        "dataset_profile": DATASET_PROFILE_POSITION_SWING,
        "dataset_bar_rule": DATASET_BAR_RULE_RTH_FULL_SESSION_1D,
        "session_date": session["session_date"],
        "session_type": "FULL_ORDINARY_SESSION",
        "bar_start_utc": swing._utc_text(market_open),
        "bar_end_utc": swing._utc_text(market_close),
        "bar_start_local": swing._local_text(market_open),
        "bar_end_local": swing._local_text(market_close),
        "open": swing._decimal_text(swing._decimal(first["open"])),
        "high": swing._decimal_text(max(swing._decimal(row["high"]) or Decimal("0") for row in rows)),
        "low": swing._decimal_text(min(swing._decimal(row["low"]) or Decimal("0") for row in rows)),
        "close": swing._decimal_text(swing._decimal(last["close"])),
        "volume": swing._decimal_text(volume_sum),
        "transactions": sum(item for item in transactions if item is not None) if any(item is not None for item in transactions) else None,
        "vwap": swing._decimal_text(weighted_vwap),
        "source_row_count": len(rows),
        "source_first_timestamp_utc": first["timestamp_utc"],
        "source_last_timestamp_utc": last["timestamp_utc"],
        "source_session_date": session["session_date"],
        "source_timeframe": "15m",
    }


def build_position_swing_bars_from_normalized_source_rows_v1(
    source_rows: list[dict[str, Any]],
    *,
    schedule_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build deterministic POSITION_SWING full-session daily bars from classified RTH rows."""
    schedule = schedule_rows if schedule_rows is not None else calendar_service.build_exchange_calendar_schedule_rows_v1()
    classified_rows = acquisition.classify_normalized_source_rows_v1(deepcopy(source_rows), schedule_rows=schedule)
    rth_rows = sorted(
        [row for row in classified_rows if row.get("session_classification") == acquisition.RTH],
        key=swing._source_row_sort_key,
    )
    rows_by_session: dict[str, list[dict[str, Any]]] = {}
    for row in rth_rows:
        rows_by_session.setdefault(str(row["session_date"]), []).append(row)

    bars: list[dict[str, Any]] = []
    special_exclusions: list[dict[str, Any]] = []
    invalid_sessions: list[dict[str, Any]] = []
    full_sessions_used = 0
    policy = _special_session_policy()
    for session in schedule:
        session_date = session["session_date"]
        session_rows = rows_by_session.get(session_date, [])
        if session.get("is_full_session") is not True:
            if session_rows:
                special_exclusions.append(
                    {
                        "session_date": session_date,
                        "session_minutes": session["session_minutes"],
                        "observed_rth_rows": len(session_rows),
                        "exclusion_reason": policy["special_session_exclusion_reason"],
                    }
                )
            continue
        if not session_rows:
            continue
        if len(session_rows) != FULL_SESSION_SOURCE_ROW_COUNT:
            invalid_sessions.append(
                {
                    "session_date": session_date,
                    "expected_source_rows": FULL_SESSION_SOURCE_ROW_COUNT,
                    "observed_source_rows": len(session_rows),
                    "invalid_reason": "FULL_ORDINARY_SESSION_SOURCE_ROW_COUNT_MISMATCH",
                }
            )
            continue
        bars.append(_bar_from_rows(session_rows, session=session))
        full_sessions_used += 1

    consumed = sum(row["source_row_count"] for row in bars)
    special_session_rows_excluded = sum(item["observed_rth_rows"] for item in special_exclusions)
    january_bars = [bar for bar in bars if bar["session_date"].startswith("2025-01")]
    return {
        "dataset_rows": bars,
        "source_rth_rows_total": len(rth_rows),
        "source_rth_rows_consumed": consumed,
        "source_rth_rows_excluded": len(rth_rows) - consumed,
        "full_sessions_used": full_sessions_used,
        "special_session_exclusion_inventory": special_exclusions,
        "special_session_count": sum(1 for row in schedule if row.get("is_full_session") is not True),
        "special_session_exclusion_count": len(special_exclusions),
        "special_session_rows_excluded": special_session_rows_excluded,
        "invalid_sessions": invalid_sessions,
        "2025_01_position_swing_cross_check": {
            "expected_full_ordinary_sessions": 20,
            "expected_source_rth_rows": 520,
            "expected_position_swing_bars": 20,
            "actual_position_swing_bars": len(january_bars),
            "cross_check_status": "PASSED" if len(january_bars) == 20 else "MISMATCH",
        },
    }


def _dataset_manifest(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = {
        "artifact_kind": "POSITION_SWING_CANONICAL_DATASET_MANIFEST",
        "schema_version": "position_swing_canonical_dataset_manifest_v1",
        "dataset_profile": DATASET_PROFILE_POSITION_SWING,
        "dataset_bar_rule": DATASET_BAR_RULE_RTH_FULL_SESSION_1D,
        "row_count": len(rows),
        "dataset_rows_digest": dataset_rows_digest_v1(rows),
        "source_normalized_source_rows_digest": candidate["normalized_source_rows_digest"],
        "canonical_dataset_frozen": False,
        "registry_eligibility": False,
    }
    manifest["dataset_manifest_digest"] = dataset_manifest_digest_v1(manifest)
    return manifest


def _base_candidate() -> dict[str, Any]:
    bindings = _authority_bindings()
    source = _source_acquisition_metadata()
    return {
        "artifact_kind": ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE,
        "schema_version": SCHEMA_VERSION_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_V1,
        "dataset_profile": DATASET_PROFILE_POSITION_SWING,
        "dataset_bar_rule": DATASET_BAR_RULE_RTH_FULL_SESSION_1D,
        "candidate_status": POSITION_SWING_CANONICAL_DATASET_REQUIRES_FROZEN_ACQUISITION_ROWS,
        "created_offline": True,
        "provider_requests_made": False,
        "canonical_dataset_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "operator_review_required": True,
        "operator_freeze_required": True,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": True,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        **bindings,
        **source,
        **_dividend_implication(),
        "calendar": "frozen XNAS -> XNYS schedule",
        "canonical_storage_timezone": swing.CANONICAL_STORAGE_TIMEZONE,
        "special_session_policy": _special_session_policy(),
        "special_session_count": 0,
        "special_session_exclusion_count": 0,
        "special_session_exclusion_reason": _special_session_policy()["special_session_exclusion_reason"],
        "special_session_exclusion_inventory": [],
        "source_row_artifact_available": False,
        "source_row_digest_matched": False,
        "source_row_digest_verified": False,
        "source_row_digest_verification_mode": "MISSING_SOURCE_ROW_ARTIFACT",
        "source_row_artifact_path": None,
        "actual_normalized_source_rows_digest": None,
        "position_swing_bar_count": 0,
        "source_rth_rows_consumed": 0,
        "source_rth_rows_excluded": 25970,
        "full_sessions_used": 0,
        "special_sessions_excluded": 0,
        "special_session_rows_excluded": 0,
        "invalid_sessions": [],
        "first_bar_timestamp_utc": None,
        "last_bar_timestamp_utc": None,
        "dataset_rows_digest": None,
        "dataset_manifest_digest": None,
        "candidate_receipt_digest": None,
        "ignored_output_dataset_path": str(
            DEFAULT_POSITION_SWING_CANDIDATE_OUTPUT_ROOT / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv"
        ),
        "ignored_output_manifest_path": str(
            DEFAULT_POSITION_SWING_CANDIDATE_OUTPUT_ROOT / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json"
        ),
        "dataset_rows": [],
        "dataset_manifest": None,
        "2025_01_position_swing_cross_check": {
            "expected_full_ordinary_sessions": 20,
            "expected_source_rth_rows": 520,
            "expected_position_swing_bars": 20,
            "actual_position_swing_bars": None,
            "cross_check_status": "UNVALIDATED_MISSING_SOURCE_ROWS",
        },
        "next_required_task": "Verify frozen acquisition source rows under ignored .marketflow output, then build POSITION_SWING operator review package.",
    }


def build_position_swing_canonical_dataset_candidate_v1(
    *,
    source_rows: list[dict[str, Any]] | None = None,
    source_rows_digest: str | None = None,
    source_row_artifact_path: str | None = None,
    materialization_receipt_digest: str | None = None,
    fixture_mode: bool = False,
    schedule_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the offline POSITION_SWING canonical dataset candidate."""
    candidate = _base_candidate()
    if source_rows is not None:
        actual_digest = acquisition.normalized_source_rows_digest_v1(source_rows)
        digest_matched = actual_digest == EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
        fixture_digest_matched = fixture_mode and source_rows_digest == EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
        if digest_matched or fixture_digest_matched:
            derived = build_position_swing_bars_from_normalized_source_rows_v1(source_rows, schedule_rows=schedule_rows)
            rows = derived["dataset_rows"]
            cross_check = derived["2025_01_position_swing_cross_check"]
            ready = cross_check["cross_check_status"] == "PASSED"
            manifest = _dataset_manifest(candidate, rows) if ready else None
            supplied_receipt = materialization_receipt_digest or EXPECTED_MATERIALIZATION_RECEIPT_DIGEST
            candidate.update(
                {
                    "candidate_status": POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW
                    if ready
                    else POSITION_SWING_CANONICAL_DATASET_REQUIRES_FROZEN_ACQUISITION_ROWS,
                    "source_row_artifact_available": True,
                    "source_row_digest_matched": True,
                    "source_row_digest_verified": True,
                    "source_row_digest_verification_mode": "MATCHED_FROZEN_DIGEST" if digest_matched else "TEST_FIXTURE_SOURCE_ROWS",
                    "source_row_artifact_path": source_row_artifact_path,
                    "actual_normalized_source_rows_digest": actual_digest if digest_matched else source_rows_digest,
                    "materialization_receipt_digest": supplied_receipt,
                    "position_swing_bar_count": len(rows),
                    "source_rth_rows_consumed": derived["source_rth_rows_consumed"],
                    "source_rth_rows_excluded": derived["source_rth_rows_excluded"],
                    "full_sessions_used": derived["full_sessions_used"],
                    "special_sessions_excluded": derived["special_session_exclusion_count"],
                    "special_session_count": derived["special_session_count"],
                    "special_session_exclusion_count": derived["special_session_exclusion_count"],
                    "special_session_rows_excluded": derived["special_session_rows_excluded"],
                    "special_session_exclusion_inventory": derived["special_session_exclusion_inventory"],
                    "invalid_sessions": derived["invalid_sessions"],
                    "first_bar_timestamp_utc": rows[0]["bar_start_utc"] if rows else None,
                    "last_bar_timestamp_utc": rows[-1]["bar_start_utc"] if rows else None,
                    "dataset_rows_digest": manifest["dataset_rows_digest"] if manifest else None,
                    "dataset_manifest_digest": manifest["dataset_manifest_digest"] if manifest else None,
                    "dataset_rows": rows if ready else [],
                    "dataset_manifest": manifest,
                    "2025_01_position_swing_cross_check": cross_check,
                    "next_required_task": "POSITION_SWING operator review package." if ready else "Resolve POSITION_SWING cross-check before operator review.",
                }
            )
        else:
            candidate.update(
                {
                    "candidate_status": POSITION_SWING_CANONICAL_DATASET_SOURCE_ROWS_DIGEST_MISMATCH,
                    "source_row_artifact_available": True,
                    "source_row_digest_matched": False,
                    "source_row_digest_verified": False,
                    "source_row_digest_verification_mode": "SOURCE_ROWS_DIGEST_MISMATCH",
                    "source_row_artifact_path": source_row_artifact_path,
                    "actual_normalized_source_rows_digest": actual_digest,
                }
            )
    candidate["candidate_receipt_digest"] = candidate_receipt_digest_v1(candidate)
    candidate["position_swing_candidate_semantic_digest"] = position_swing_candidate_semantic_digest_v1(candidate)
    validate_position_swing_canonical_dataset_candidate_v1(candidate)
    return candidate


def find_verified_frozen_acquisition_source_rows_v1(search_root: str | Path = DEFAULT_SOURCE_ROWS_SEARCH_ROOT) -> dict[str, Any] | None:
    """Find a local ignored source-row artifact matching the frozen normalized row digest."""
    return swing.find_verified_frozen_acquisition_source_rows_v1(search_root)


def find_mismatched_frozen_acquisition_source_rows_v1(search_root: str | Path = DEFAULT_SOURCE_ROWS_SEARCH_ROOT) -> dict[str, Any] | None:
    """Find a local source-row artifact that can be read but fails the frozen digest."""
    return swing.find_mismatched_frozen_acquisition_source_rows_v1(search_root)


def build_position_swing_canonical_dataset_candidate_from_local_artifact_v1(
    search_root: str | Path = DEFAULT_SOURCE_ROWS_SEARCH_ROOT,
) -> dict[str, Any]:
    """Build from a verified ignored source-row artifact, or fail closed as blocked."""
    payload = find_verified_frozen_acquisition_source_rows_v1(search_root)
    if payload is None:
        mismatched = find_mismatched_frozen_acquisition_source_rows_v1(search_root)
        if mismatched is not None:
            return build_position_swing_canonical_dataset_candidate_v1(
                source_rows=mismatched["rows"],
                source_rows_digest=mismatched["normalized_source_rows_digest"],
                source_row_artifact_path=mismatched["path"],
            )
        return build_position_swing_canonical_dataset_candidate_v1()
    return build_position_swing_canonical_dataset_candidate_v1(
        source_rows=payload["rows"],
        source_rows_digest=payload["normalized_source_rows_digest"],
        source_row_artifact_path=payload["path"],
        materialization_receipt_digest=payload.get("materialization_receipt_digest"),
    )


def _validation_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("artifact_kind", ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE, candidate.get("artifact_kind")),
        ("canonical_dataset_frozen_false", False, candidate.get("canonical_dataset_frozen")),
        ("canonical_eligibility_false", False, candidate.get("canonical_eligibility")),
        ("registry_eligibility_false", False, candidate.get("registry_eligibility")),
        ("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        ("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        ("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        ("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        ("acquisition_generation_freeze_true", True, candidate.get("acquisition_generation_freeze")),
        ("acquisition_frozen_digest_matches", EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST, candidate.get("acquisition_generation_frozen_digest")),
        ("normalized_source_rows_digest_matches", EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST, candidate.get("normalized_source_rows_digest")),
        ("special_session_policy_present", True, isinstance(candidate.get("special_session_policy"), dict)),
        ("dividend_implication_present", acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, candidate.get("in_range_dividend_implication")),
    ]
    return [
        {
            "check_id": check_id,
            "status": PASS if expected == actual else FAIL,
            "expected": expected,
            "actual": actual,
            "severity": BLOCKER,
        }
        for check_id, expected, actual in checks
    ]


def validate_position_swing_canonical_dataset_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate a POSITION_SWING canonical dataset candidate and downstream guardrails."""
    if not isinstance(candidate, dict):
        raise PositionSwingCanonicalDatasetError("candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_V1, "schema_version")
    if candidate.get("candidate_status") not in {
        POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW,
        POSITION_SWING_CANONICAL_DATASET_REQUIRES_FROZEN_ACQUISITION_ROWS,
        POSITION_SWING_CANONICAL_DATASET_SOURCE_ROWS_DIGEST_MISMATCH,
    }:
        raise PositionSwingCanonicalDatasetError("candidate_status mismatch")
    if candidate.get("candidate_status") != POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW and candidate.get("dataset_rows"):
        raise PositionSwingCanonicalDatasetError("candidate_status not ready when dataset generated")
    for field in (
        "created_offline",
        "identity_segment_frozen",
        "calendar_operator_frozen",
        "split_event_audit_frozen",
        "dividend_event_audit_frozen",
        "acquisition_generation_freeze",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "canonical_dataset_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
    ):
        _expect_false(candidate.get(field), field)
    _expect(candidate.get("runtime_use"), NOT_AUTHORIZED, "runtime_use")
    _expect(candidate.get("strategy_use"), NOT_AUTHORIZED, "strategy_use")
    _expect(candidate.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in _authority_bindings().items():
        _expect(candidate.get(field), expected, field)
    for field, expected in _source_acquisition_metadata().items():
        _expect(candidate.get(field), expected, field)
    for field, expected in _dividend_implication().items():
        _expect(candidate.get(field), expected, field)
    policy = candidate.get("special_session_policy")
    if not isinstance(policy, dict):
        raise PositionSwingCanonicalDatasetError("special_session_policy missing")
    for field, expected in _special_session_policy().items():
        _expect(policy.get(field), expected, f"special_session_policy.{field}")
    if candidate.get("source_rth_rows_consumed", 0) > candidate.get("source_rth_rows_total", 0):
        raise PositionSwingCanonicalDatasetError("source_rth_rows_consumed exceeds source_rth_rows_total")
    if candidate["candidate_status"] == POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW:
        _expect(candidate.get("source_row_digest_matched"), True, "source_row_digest_matched")
        _expect(candidate.get("source_row_digest_verified"), True, "source_row_digest_verified")
        _expect(candidate.get("actual_normalized_source_rows_digest"), EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST, "actual_normalized_source_rows_digest")
        for field in ("dataset_rows_digest", "dataset_manifest_digest", "candidate_receipt_digest"):
            if not isinstance(candidate.get(field), str) or len(candidate[field]) != 64:
                raise PositionSwingCanonicalDatasetError(f"{field} missing")
        cross_check = candidate.get("2025_01_position_swing_cross_check")
        if not isinstance(cross_check, dict) or cross_check.get("actual_position_swing_bars") != 20:
            raise PositionSwingCanonicalDatasetError("2025-01 POSITION_SWING cross-check mismatch")
        if cross_check.get("cross_check_status") != "PASSED":
            raise PositionSwingCanonicalDatasetError("2025-01 POSITION_SWING cross-check mismatch")
        if not candidate.get("special_session_exclusion_inventory") and candidate.get("special_session_exclusion_count"):
            raise PositionSwingCanonicalDatasetError("special_session_exclusion_inventory missing")
        for row in candidate.get("dataset_rows") or []:
            if row.get("session_type") == "FULL_ORDINARY_SESSION" and row.get("source_row_count") != SOURCE_ROWS_PER_POSITION_SWING_BAR:
                raise PositionSwingCanonicalDatasetError("source_row_count mismatch")
            if row.get("session_type") != "FULL_ORDINARY_SESSION" and policy.get("special_sessions_excluded_from_position_swing_bars") is True:
                raise PositionSwingCanonicalDatasetError("special sessions included without explicit policy")
        manifest = candidate.get("dataset_manifest")
        if not isinstance(manifest, dict):
            raise PositionSwingCanonicalDatasetError("dataset_manifest missing")
        _expect(candidate["dataset_rows_digest"], dataset_rows_digest_v1(candidate.get("dataset_rows") or []), "dataset_rows_digest")
        _expect(candidate["dataset_manifest_digest"], dataset_manifest_digest_v1(manifest), "dataset_manifest_digest")
    else:
        _expect(candidate.get("source_row_digest_matched"), False, "source_row_digest_matched")
        _expect(candidate.get("dataset_rows_digest"), None, "dataset_rows_digest")
        _expect(candidate.get("dataset_manifest_digest"), None, "dataset_manifest_digest")
    expected_receipt = candidate_receipt_digest_v1(candidate)
    _expect(candidate.get("candidate_receipt_digest"), expected_receipt, "candidate_receipt_digest")
    digest = candidate.get("position_swing_candidate_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PositionSwingCanonicalDatasetError("position_swing_candidate_semantic_digest missing")
    _expect(digest, position_swing_candidate_semantic_digest_v1(candidate), "position_swing_candidate_semantic_digest")
    checklist = _validation_checklist(candidate)
    failed = [check for check in checklist if check["status"] != PASS]
    return {
        "status": "POSITION_SWING_CANONICAL_DATASET_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "failed_checks": len(failed),
        "blocker_count": sum(1 for check in failed if check["severity"] == BLOCKER),
        "position_swing_candidate_semantic_digest": digest,
        "dataset_rows_digest": candidate.get("dataset_rows_digest"),
        "dataset_manifest_digest": candidate.get("dataset_manifest_digest"),
        "canonical_dataset_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
    }


def build_position_swing_canonical_dataset_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Render a sanitized POSITION_SWING canonical candidate status document."""
    validate_position_swing_canonical_dataset_candidate_v1(candidate)
    cross_check = candidate["2025_01_position_swing_cross_check"]
    lines = [
        "# MarketFlow POSITION_SWING Canonical Dataset Candidate Status",
        "",
        "## Candidate",
        f"- Artifact kind: `{candidate['artifact_kind']}`",
        f"- Candidate status: `{candidate['candidate_status']}`",
        f"- Dataset profile: `{candidate['dataset_profile']}`",
        f"- Dataset bar rule: `{candidate['dataset_bar_rule']}`",
        f"- Candidate digest: `{candidate['position_swing_candidate_semantic_digest']}`",
        f"- Candidate receipt digest: `{candidate['candidate_receipt_digest']}`",
        "",
        "## Source Rows",
        f"- Source row data available: `{candidate['source_row_artifact_available']}`",
        f"- Source row digest verified: `{candidate['source_row_digest_verified']}`",
        f"- Source row digest verification mode: `{candidate['source_row_digest_verification_mode']}`",
        f"- Source rows path: `{candidate['source_row_artifact_path']}`",
        f"- Normalized source rows digest: `{candidate['normalized_source_rows_digest']}`",
        f"- Actual normalized source rows digest: `{candidate['actual_normalized_source_rows_digest']}`",
        f"- Source rows: `{candidate['source_rows_total']} total / {candidate['source_rth_rows_total']} RTH / {candidate['source_extended_hours_rows_total']} extended-hours / {candidate['source_unknown_rows_total']} unknown`",
        "",
        "## Frozen Acquisition Binding",
        f"- Acquisition frozen digest: `{candidate['acquisition_generation_frozen_digest']}`",
        f"- Monthly reconciliation digest: `{candidate['monthly_reconciliation_digest']}`",
        f"- Acquisition receipt digest: `{candidate['acquisition_receipt_digest']}`",
        f"- Materialization receipt digest: `{candidate['materialization_receipt_digest']}`",
        "",
        "## POSITION_SWING Dataset Summary",
        f"- POSITION_SWING bar count: `{candidate['position_swing_bar_count']}`",
        f"- Source RTH rows consumed: `{candidate['source_rth_rows_consumed']}`",
        f"- Source RTH rows excluded: `{candidate['source_rth_rows_excluded']}`",
        f"- Full sessions used: `{candidate['full_sessions_used']}`",
        f"- Special sessions excluded: `{candidate['special_sessions_excluded']}`",
        f"- Special session rows excluded: `{candidate['special_session_rows_excluded']}`",
        f"- Invalid sessions: `{len(candidate['invalid_sessions'])}`",
        f"- Dataset digest: `{candidate['dataset_rows_digest']}`",
        f"- Dataset manifest digest: `{candidate['dataset_manifest_digest']}`",
        f"- Ignored dataset output path: `{candidate['ignored_output_dataset_path']}`",
        f"- Ignored manifest output path: `{candidate['ignored_output_manifest_path']}`",
        "",
        "## 2025-01 POSITION_SWING Cross-Check",
        f"- Expected POSITION_SWING bars: `{cross_check['expected_position_swing_bars']}`",
        f"- Actual POSITION_SWING bars: `{cross_check['actual_position_swing_bars']}`",
        f"- Result: `{cross_check['cross_check_status']}`",
        "",
        "## Special-Session Policy",
        f"- full_ordinary_sessions_only_for_RTH_FULL_SESSION_1D: `{candidate['special_session_policy']['full_ordinary_sessions_only_for_RTH_FULL_SESSION_1D']}`",
        f"- special_sessions_excluded_from_position_swing_bars: `{candidate['special_session_policy']['special_sessions_excluded_from_position_swing_bars']}`",
        f"- special_sessions_recorded_in_exclusion_inventory: `{candidate['special_session_policy']['special_sessions_recorded_in_exclusion_inventory']}`",
        f"- Special-session count: `{candidate['special_session_count']}`",
        f"- Special-session exclusion count: `{candidate['special_session_exclusion_count']}`",
        f"- Special-session exclusion reason: `{candidate['special_session_exclusion_reason']}`",
        "",
        "## Dividend Implication",
        f"- In-range dividends found: `{candidate['in_range_dividends_found']}`",
        f"- In-range dividend count: `{candidate['in_range_dividend_count']}`",
        f"- Implication: `{candidate['in_range_dividend_implication']}`",
        f"- Source adjusted data used: `{candidate['source_adjusted_data_used']}`",
        "",
        "## Authority Boundary",
        f"- identity_segment_frozen: `{candidate['identity_segment_frozen']}`",
        f"- calendar_operator_frozen: `{candidate['calendar_operator_frozen']}`",
        f"- split_event_audit_frozen: `{candidate['split_event_audit_frozen']}`",
        f"- dividend_event_audit_frozen: `{candidate['dividend_event_audit_frozen']}`",
        f"- acquisition_generation_freeze: `{candidate['acquisition_generation_freeze']}`",
        f"- canonical_dataset_frozen: `{candidate['canonical_dataset_frozen']}`",
        f"- canonical_eligibility: `{candidate['canonical_eligibility']}`",
        f"- registry_eligibility: `{candidate['registry_eligibility']}`",
        f"- strategy_runtime_migration: `{candidate['strategy_runtime_migration']}`",
        f"- runtime_use: `{candidate['runtime_use']}`",
        f"- strategy_use: `{candidate['strategy_use']}`",
        f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
        f"- profitability: `{candidate['profitability']}`",
        "",
        "## Guardrails",
        f"- Created offline: `{candidate['created_offline']}`",
        f"- Provider requests made: `{candidate['provider_requests_made']}`",
        "- No canonical freeze, registry approval, runtime migration, predictive acceptance, or profitability acceptance occurred.",
        "",
        "## Next Task Recommendation",
        f"- {candidate['next_required_task']}",
        "",
    ]
    return "\n".join(lines)


def write_position_swing_canonical_dataset_candidate_outputs_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Write ready candidate dataset rows and manifest under ignored .marketflow output."""
    validate_position_swing_canonical_dataset_candidate_v1(candidate)
    output_path = Path(output_dir)
    if ".marketflow" not in output_path.parts:
        raise PositionSwingCanonicalDatasetError("POSITION_SWING dataset output must be under ignored .marketflow")
    output_path.mkdir(parents=True, exist_ok=True)
    manifest_path = output_path / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json"
    candidate_path = output_path / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_candidate.json"
    csv_path = output_path / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv"
    if candidate["candidate_status"] != POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW:
        candidate_path.write_bytes(canonical_json_bytes(candidate))
        return {
            "candidate_path": str(candidate_path),
            "candidate_sha256": sha256_bytes(candidate_path.read_bytes()),
            "dataset_path": None,
            "dataset_sha256": None,
            "manifest_path": None,
            "manifest_sha256": None,
        }
    rows = candidate["dataset_rows"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    manifest_path.write_bytes(canonical_json_bytes(candidate["dataset_manifest"]))
    candidate_path.write_bytes(canonical_json_bytes(candidate))
    return {
        "candidate_path": str(candidate_path),
        "candidate_sha256": sha256_bytes(candidate_path.read_bytes()),
        "dataset_path": str(csv_path),
        "dataset_sha256": sha256_bytes(csv_path.read_bytes()),
        "manifest_path": str(manifest_path),
        "manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
    }
