"""Offline identity segment candidate evidence freeze helpers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.source_authority import instrument_identity as ident
from marketflow.source_authority import ticker_event_audit as tkev


ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE = "IDENTITY_SEGMENT_CANDIDATE"
SCHEMA_VERSION_IDENTITY_SEGMENT_EVIDENCE_FREEZE_V1 = "identity_segment_evidence_freeze_v1"
IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW = "IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW"
IDENTITY_SEGMENT_FROZEN = "IDENTITY_SEGMENT_FROZEN"

CORE_ACQUISITION_CONTRACT_V2_1 = "CORE ACQUISITION CONTRACT v2.1"
ACQUISITION_CONTRACT_V2_1_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
FIXED_ACQUISITION_START = "2022-01-01"
FIXED_ACQUISITION_END = "2025-12-31"

IDENTITY_RUN_ID = tkev.SOURCE_IDENTITY_RUN_ID
CONTINUITY_ARTIFACT_ID = tkev.SOURCE_CONTINUITY_ARTIFACT_ID
START_SNAPSHOT_SEMANTIC_DIGEST = tkev.SOURCE_START_SNAPSHOT_DIGEST
END_SNAPSHOT_SEMANTIC_DIGEST = tkev.SOURCE_END_SNAPSHOT_DIGEST

TICKER_EVENTS_AUDIT_RUN_ID = "tkev-959a591271874fe49bc8cb34bb29be36"
TICKER_EVENTS_RAW_RESPONSE_ARTIFACT_ID = "tkev-art-5d8ed7c1aa0e451ab1c7b297230dca33"
TICKER_EVENTS_RAW_RESPONSE_SEMANTIC_PAYLOAD_DIGEST = "07082085e9e41c467e020774954c045e83613d9581976ca26e87b74e3bbf15dc"
TICKER_EVENTS_TIMELINE_ARTIFACT_ID = "tkev-art-54a14c247fb2459a9c588dd4695b4358"
TICKER_EVENTS_TIMELINE_SEMANTIC_DIGEST = "36ccff35908df36a7fadb124d6cb846e4ac0cace578830e7591f7edf92bde820"
TICKER_EVENTS_AUDIT_ARTIFACT_ID = "tkev-art-df20d0c474464b74a28a6f4ed451fef6"
TICKER_EVENTS_RECEIPT_ARTIFACT_ID = "tkev-art-2168e3f7caec46d59436ab0e4280d49d"

PROVIDER_IDENTITY_STATUS_PRESENT_MATCHED = "PRESENT_MATCHED"
IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE = (
    tkev.IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE
)
IDENTITY_CONTINUITY_EVIDENCE_SUPPORTED_AS_CANDIDATE = "SUPPORTED_AS_CANDIDATE"
PREDICTIVE_USEFULNESS_NOT_ACCEPTED = "not accepted"
PROFITABILITY_NOT_ACCEPTED = "not accepted"
REFERENCE_ONLY = "REFERENCE_ONLY"
CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN = "NOT_OPERATOR_FROZEN"
RTH_SOURCE_ROWS_RECONCILED = "RTH_SOURCE_ROWS_RECONCILED"
BEFORE_CONTRACT_RANGE = tkev.BEFORE_CONTRACT_RANGE

SEGMENT = {
    "ticker": "AAPL",
    "composite_figi": "BBG000B9XRY4",
    "share_class_figi": "BBG001S5N8V8",
    "primary_mic": "XNAS",
    "security_type": "CS",
    "segment_start": FIXED_ACQUISITION_START,
    "segment_end": FIXED_ACQUISITION_END,
    "acquisition_contract_digest": ACQUISITION_CONTRACT_V2_1_DIGEST,
    "fixed_acquisition_range": {
        "start": FIXED_ACQUISITION_START,
        "end": FIXED_ACQUISITION_END,
    },
}

IDENTITY_EVIDENCE_BINDING = {
    "identity_run_id": IDENTITY_RUN_ID,
    "continuity_artifact_id": CONTINUITY_ARTIFACT_ID,
    "start_snapshot_date": FIXED_ACQUISITION_START,
    "end_snapshot_date": FIXED_ACQUISITION_END,
    "start_snapshot_semantic_digest": START_SNAPSHOT_SEMANTIC_DIGEST,
    "end_snapshot_semantic_digest": END_SNAPSHOT_SEMANTIC_DIGEST,
    "primary_exchange": "XNAS",
    "composite_figi": "BBG000B9XRY4",
    "share_class_figi": "BBG001S5N8V8",
    "security_type": "CS",
    "active_at_both_boundaries": True,
    "continuity_status": ident.IDENTITY_CONTINUITY_SUPPORTED,
    "artifact_inventory": {
        ident.TICKER_OVERVIEW_RAW_RESPONSE: 2,
        ident.TICKER_OVERVIEW_SNAPSHOT: 2,
        ident.IDENTITY_CONTINUITY_CANDIDATE: 1,
        ident.INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT: 1,
    },
    "total_manifests": 6,
}

TICKER_EVENTS_EVIDENCE_BINDING = {
    "ticker_events_audit_run_id": TICKER_EVENTS_AUDIT_RUN_ID,
    "raw_response_artifact_id": TICKER_EVENTS_RAW_RESPONSE_ARTIFACT_ID,
    "raw_response_semantic_payload_digest": TICKER_EVENTS_RAW_RESPONSE_SEMANTIC_PAYLOAD_DIGEST,
    "timeline_artifact_id": TICKER_EVENTS_TIMELINE_ARTIFACT_ID,
    "timeline_semantic_digest": TICKER_EVENTS_TIMELINE_SEMANTIC_DIGEST,
    "audit_artifact_id": TICKER_EVENTS_AUDIT_ARTIFACT_ID,
    "receipt_artifact_id": TICKER_EVENTS_RECEIPT_ARTIFACT_ID,
    "endpoint": tkev.TICKER_EVENTS_EXPERIMENTAL_VX,
    "query_identifier": "Composite FIGI BBG000B9XRY4",
    "provider_composite_figi_status": PROVIDER_IDENTITY_STATUS_PRESENT_MATCHED,
    "provider_cik_status": PROVIDER_IDENTITY_STATUS_PRESENT_MATCHED,
    "returned_event_count": 1,
    "pre_range_events": 1,
    "in_range_events": 0,
    "post_range_events": 0,
    "ticker_events_audit_status": tkev.TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE,
    "combined_identity_candidate_status": IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE,
    "endpoint_stability": tkev.ENDPOINT_STABILITY_EXPERIMENTAL,
    "events": [
        {
            "event_date": "2003-09-10",
            "event_type": tkev.EVENT_TYPE_TICKER_CHANGE,
            "reported_ticker": "AAPL",
            "range_classification": BEFORE_CONTRACT_RANGE,
        }
    ],
}

MONTHLY_SOURCE_EVIDENCE = {
    "ticker": "AAPL",
    "month": "2025-01",
    "normalized_source_rows": 1277,
    "extended_hours_rows": 757,
    "expected_rth_rows": 520,
    "validated_rth_rows": 520,
    "rth_reconciliation": RTH_SOURCE_ROWS_RECONCILED,
    "full_ordinary_sessions": 20,
    "incomplete_ordinary_sessions": 0,
    "swing_rth_half_session_195m_bars": 40,
    "position_swing_rth_full_session_1d_bars": 20,
    "requested_calendar": "XNAS",
    "resolved_calendar": "XNYS",
    "calendar_alias": "XNAS_USES_XNYS_SCHEDULE",
    "calendar_authority": CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN,
}

AUTHORITY_BOUNDARY = {
    "identity_continuity_evidence": IDENTITY_CONTINUITY_EVIDENCE_SUPPORTED_AS_CANDIDATE,
    "identity_segment_frozen": False,
    "calendar_operator_frozen": False,
    "canonical_eligibility": False,
    "registry_eligibility": False,
    "acquisition_generation_freeze": False,
    "strategy_runtime_migration": False,
    "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
    "profitability": PROFITABILITY_NOT_ACCEPTED,
    "automatic_stitching": False,
}

LINEAGE_GUARDRAILS = {
    "binding_mode": REFERENCE_ONLY,
    "raw_source_evidence_copied": False,
    "raw_source_evidence_rewritten": False,
    "provider_requests_made": False,
    "operator_freeze_required": True,
    "next_allowed_operator_ceremony": IDENTITY_SEGMENT_FROZEN,
}

FORBIDDEN_FREEZE_FIELDS = frozenset(
    {
        "operator_approval",
        "operator_approved",
        "operator_approved_by",
        "operator_approval_timestamp",
        "freeze_timestamp",
        "freeze_operator_identity",
        "identity_segment_freeze_digest",
    }
)


class IdentitySegmentFreezeError(ValueError):
    """Raised when an identity segment candidate violates the freeze boundary."""


def _candidate_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("candidate_semantic_digest", None)
    payload.pop("candidate_payload_digest", None)
    return payload


def candidate_semantic_digest(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the candidate itself."""
    return semantic_digest(_candidate_digest_payload(candidate))


def build_identity_segment_candidate_v1() -> dict[str, Any]:
    """Build the fixed offline AAPL identity segment candidate."""
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_IDENTITY_SEGMENT_EVIDENCE_FREEZE_V1,
        "candidate_status": IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW,
        "operator_freeze_required": True,
        "identity_segment_frozen": False,
        "created_offline": True,
        "provider_requests_made": False,
        "automatic_stitching": False,
        "acquisition_contract": {
            "contract": CORE_ACQUISITION_CONTRACT_V2_1,
            "contract_digest": ACQUISITION_CONTRACT_V2_1_DIGEST,
            "fixed_acquisition_range": {
                "start": FIXED_ACQUISITION_START,
                "end": FIXED_ACQUISITION_END,
            },
            "source": {
                "provider": "Massive.com Custom Bars",
                "interval": "15-minute",
                "adjustment": "Adjusted",
                "sort": "Ascending",
                "source_timestamp_semantic": "aggregate-window starts",
                "source_timezone": "America/New_York",
                "canonical_storage_timezone": "UTC",
            },
        },
        "segment": deepcopy(SEGMENT),
        "identity_evidence_binding": deepcopy(IDENTITY_EVIDENCE_BINDING),
        "ticker_events_evidence_binding": deepcopy(TICKER_EVENTS_EVIDENCE_BINDING),
        "monthly_source_evidence": deepcopy(MONTHLY_SOURCE_EVIDENCE),
        "authority_boundary": deepcopy(AUTHORITY_BOUNDARY),
        "lineage_guardrails": deepcopy(LINEAGE_GUARDRAILS),
    }
    candidate["candidate_semantic_digest"] = candidate_semantic_digest(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise IdentitySegmentFreezeError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise IdentitySegmentFreezeError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise IdentitySegmentFreezeError(f"{field_name} must be true")


def _reject_forbidden_fields(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key in FORBIDDEN_FREEZE_FIELDS:
            raise IdentitySegmentFreezeError(f"{current_path} is not allowed")
        if key in {"artifact_kind", "candidate_status"} and value == IDENTITY_SEGMENT_FROZEN:
            raise IdentitySegmentFreezeError(f"{current_path} must not be frozen")
        if isinstance(value, dict):
            _reject_forbidden_fields(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_fields(item, path=f"{current_path}[{index}]")


def validate_identity_segment_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate the fixed reference-only candidate and return a receipt."""
    if not isinstance(candidate, dict):
        raise IdentitySegmentFreezeError("candidate must be a JSON object")
    _reject_forbidden_fields(candidate)

    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_IDENTITY_SEGMENT_EVIDENCE_FREEZE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW, "candidate_status")
    _expect_true(candidate.get("operator_freeze_required"), "operator_freeze_required")
    _expect_false(candidate.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(candidate.get("created_offline"), "created_offline")
    _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
    _expect_false(candidate.get("automatic_stitching"), "automatic_stitching")

    _expect(candidate.get("acquisition_contract", {}).get("contract_digest"), ACQUISITION_CONTRACT_V2_1_DIGEST, "acquisition_contract.contract_digest")
    _expect(candidate.get("segment"), SEGMENT, "segment")
    _expect(candidate.get("identity_evidence_binding"), IDENTITY_EVIDENCE_BINDING, "identity_evidence_binding")
    _expect(candidate.get("ticker_events_evidence_binding"), TICKER_EVENTS_EVIDENCE_BINDING, "ticker_events_evidence_binding")
    _expect(candidate.get("monthly_source_evidence"), MONTHLY_SOURCE_EVIDENCE, "monthly_source_evidence")
    _expect(candidate.get("authority_boundary"), AUTHORITY_BOUNDARY, "authority_boundary")
    _expect(candidate.get("lineage_guardrails"), LINEAGE_GUARDRAILS, "lineage_guardrails")

    digest = candidate_semantic_digest(candidate)
    _expect(candidate.get("candidate_semantic_digest"), digest, "candidate_semantic_digest")
    return {
        "status": "IDENTITY_SEGMENT_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE,
        "candidate_status": IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW,
        "candidate_semantic_digest": digest,
        "provider_requests_made": False,
        "identity_segment_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "calendar_operator_frozen": False,
    }


def write_identity_segment_candidate_v1(output_dir: str | Path, *, filename: str | None = None) -> dict[str, Any]:
    """Write the fixed candidate JSON artifact without overwriting existing output."""
    candidate = build_identity_segment_candidate_v1()
    validation = validate_identity_segment_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_identity_segment_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise IdentitySegmentFreezeError("candidate filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise IdentitySegmentFreezeError("identity segment candidate output already exists")
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "candidate_payload_digest": sha256_bytes(payload),
    }
