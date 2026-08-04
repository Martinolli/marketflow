from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from marketflow.services import exchange_calendar_evidence_service as calendar_service
from marketflow.services import identity_segment_freeze_service as identity_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDENTITY_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


def _candidate() -> dict:
    return calendar_service.build_exchange_calendar_evidence_candidate_v1()


def _validated(candidate: dict) -> dict:
    return calendar_service.validate_exchange_calendar_evidence_candidate_v1(candidate)


def _recompute_digest(candidate: dict) -> None:
    candidate["calendar_evidence_candidate_semantic_digest"] = calendar_service.calendar_evidence_candidate_semantic_digest(candidate)


def test_candidate_builds_offline_with_no_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(identity_candidate.ident, "TickerOverviewTransport", fail_provider_call)
    monkeypatch.setattr(identity_candidate.tkev, "TickerEventsTransport", fail_provider_call)
    monkeypatch.setattr(identity_candidate.tkev, "validate_accepted_source_identity_evidence", fail_provider_call)

    candidate = _candidate()
    receipt = _validated(candidate)

    assert calls == []
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_artifact_kind_status_and_candidate_only_boundary():
    candidate = _candidate()

    assert candidate["artifact_kind"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE"
    assert candidate["schema_version"] == "exchange_calendar_evidence_candidate_v1"
    assert candidate["candidate_status"] == "EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
    assert candidate["operator_review_required"] is True
    assert candidate["operator_freeze_required"] is True
    assert candidate["calendar_operator_frozen"] is False


def test_identity_segment_frozen_digest_is_bound():
    candidate = _candidate()
    binding = candidate["identity_segment_binding"]

    assert candidate["identity_segment_frozen"] is True
    assert candidate["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert binding["identity_segment_frozen"] is True
    assert binding["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert binding["ticker"] == "AAPL"
    assert binding["composite_figi"] == "BBG000B9XRY4"
    assert binding["share_class_figi"] == "BBG001S5N8V8"
    assert binding["primary_mic"] == "XNAS"
    assert binding["security_type"] == "CS"
    assert binding["segment_start"] == "2022-01-01"
    assert binding["segment_end"] == "2025-12-31"


def test_contract_digest_and_acquisition_source_are_bound():
    contract = _candidate()["acquisition_contract"]

    assert contract["contract"] == "CORE ACQUISITION CONTRACT v2.1"
    assert contract["contract_digest"] == EXPECTED_CONTRACT_DIGEST
    assert contract["fixed_acquisition_range"] == {"start": "2022-01-01", "end": "2025-12-31"}
    assert contract["source"] == {
        "provider": "Massive.com Custom Bars",
        "interval": "15-minute",
        "adjustment": "Adjusted",
        "sort": "Ascending",
        "source_timestamp_semantic": "aggregate-window starts",
        "source_timezone": "America/New_York",
        "canonical_storage_timezone": "UTC",
    }


def test_requested_resolved_calendar_alias_and_source_library_are_bound():
    binding = _candidate()["calendar_binding"]

    assert binding["requested_calendar"] == "XNAS"
    assert binding["resolved_calendar"] == "XNYS"
    assert binding["calendar_alias"] == "XNAS_USES_XNYS_SCHEDULE"
    assert binding["calendar_timezone"] == "America/New_York"
    assert binding["canonical_storage_timezone"] == "UTC"
    assert binding["calendar_source_library"] == "exchange_calendars"
    assert binding["calendar_source_library_version"] == "4.13.2"
    assert binding["calendar_authority_status"] == "NOT_OPERATOR_FROZEN"


def test_candidate_includes_schedule_semantic_digest_and_deterministic_candidate_digest():
    first = _candidate()
    second = _candidate()

    assert first == second
    assert len(first["schedule_semantic_digest"]) == 64
    assert first["schedule_semantic_digest"] == first["schedule_coverage"]["schedule_semantic_digest"]
    assert len(first["calendar_evidence_candidate_semantic_digest"]) == 64
    assert first["calendar_evidence_candidate_semantic_digest"] == calendar_service.calendar_evidence_candidate_semantic_digest(first)


def test_monthly_2025_01_cross_check_matches_accepted_values():
    check = _candidate()["accepted_monthly_cross_check"]

    assert check["ticker"] == "AAPL"
    assert check["month"] == "2025-01"
    assert check["normalized_source_rows"] == 1277
    assert check["extended_hours_rows"] == 757
    assert check["expected_rth_rows"] == 520
    assert check["validated_rth_rows"] == 520
    assert check["rth_reconciliation"] == "RTH_SOURCE_ROWS_RECONCILED"
    assert check["full_ordinary_sessions"] == 20
    assert check["incomplete_ordinary_sessions"] == 0
    assert check["swing_rth_half_session_195m_bars"] == 40
    assert check["position_swing_rth_full_session_1d_bars"] == 20
    assert check["requested_calendar"] == "XNAS"
    assert check["resolved_calendar"] == "XNYS"
    assert check["calendar_alias"] == "XNAS_USES_XNYS_SCHEDULE"
    assert check["calendar_authority"] == "NOT_OPERATOR_FROZEN"


def test_validator_rejects_modified_calendar_alias():
    candidate = _candidate()
    candidate["calendar_binding"]["calendar_alias"] = "XNAS_DIRECT"
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError, match="calendar_binding"):
        _validated(candidate)


def test_validator_rejects_modified_contract_digest():
    candidate = _candidate()
    candidate["acquisition_contract"]["contract_digest"] = "0" * 64
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError, match="contract_digest"):
        _validated(candidate)


def test_validator_rejects_modified_identity_segment_frozen_digest():
    candidate = _candidate()
    candidate["identity_segment_frozen_digest"] = "1" * 64
    candidate["identity_segment_binding"]["identity_segment_frozen_digest"] = "1" * 64
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError, match="identity_segment_frozen_digest"):
        _validated(candidate)


def test_validator_rejects_calendar_operator_frozen_true():
    candidate = _candidate()
    candidate["calendar_operator_frozen"] = True
    candidate["authority_boundary"]["calendar_operator_frozen"] = True
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError):
        _validated(candidate)


@pytest.mark.parametrize(
    "field",
    ["canonical_eligibility", "registry_eligibility", "acquisition_generation_freeze"],
)
def test_validator_rejects_canonical_registry_or_acquisition_freeze_flags_true(field: str):
    candidate = _candidate()
    candidate["authority_boundary"][field] = True
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError):
        _validated(candidate)


def test_validator_rejects_provider_requests_made_true():
    candidate = _candidate()
    candidate["provider_requests_made"] = True
    candidate["guardrails"]["provider_requests_made"] = True
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError, match="provider_requests_made"):
        _validated(candidate)


def test_validator_rejects_missing_schedule_digest():
    candidate = _candidate()
    candidate["schedule_semantic_digest"] = ""
    candidate["schedule_coverage"]["schedule_semantic_digest"] = ""
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError, match="schedule_semantic_digest"):
        _validated(candidate)


def test_validator_rejects_automatic_stitching_true():
    candidate = _candidate()
    candidate["authority_boundary"]["automatic_stitching"] = True
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError):
        _validated(candidate)


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_validator_rejects_predictive_or_profitability_accepted(field: str):
    candidate = _candidate()
    candidate["authority_boundary"][field] = "accepted"
    _recompute_digest(candidate)

    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError):
        _validated(candidate)


def test_no_exchange_calendar_frozen_artifact_or_status_is_produced():
    candidate = _candidate()

    assert candidate["artifact_kind"] != "EXCHANGE_CALENDAR_FROZEN"
    assert candidate["candidate_status"] != "EXCHANGE_CALENDAR_FROZEN"
    assert candidate["guardrails"]["calendar_freeze_created"] is False
    assert candidate["calendar_operator_frozen"] is False


def test_schedule_stats_are_internally_consistent():
    coverage = _candidate()["schedule_coverage"]

    assert coverage["session_count"] >= coverage["full_session_count"]
    assert coverage["first_session"] <= coverage["last_session"]
    assert coverage["half_session_count"] >= 0
    assert coverage["session_count"] == coverage["full_session_count"] + coverage["half_session_count"]
    assert coverage["special_close_count"] == coverage["half_session_count"]
    assert coverage["special_open_count"] == 0


def test_schedule_row_helper_first_and_last_rows_are_deterministic():
    rows = calendar_service.build_exchange_calendar_schedule_rows_v1()
    first = rows[0]
    last = rows[-1]

    assert first == {
        "session_date": "2022-01-03",
        "market_open_utc": "2022-01-03T14:30:00Z",
        "market_close_utc": "2022-01-03T21:00:00Z",
        "market_open_local": "2022-01-03T09:30:00-05:00",
        "market_close_local": "2022-01-03T16:00:00-05:00",
        "session_minutes": 390,
        "is_full_session": True,
        "is_half_session": False,
    }
    assert last["session_date"] == "2025-12-31"
    assert last["session_minutes"] == 390
    assert last["is_full_session"] is True
    assert last["is_half_session"] is False


def test_authority_boundary_and_guardrails_remain_candidate_only():
    candidate = _candidate()
    authority = candidate["authority_boundary"]
    guardrails = candidate["guardrails"]

    assert authority == {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
    }
    assert guardrails == {
        "binding_mode": "CALENDAR_EVIDENCE_CANDIDATE_ONLY",
        "provider_requests_made": False,
        "calendar_freeze_created": False,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
    }


def test_write_candidate_artifact_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = calendar_service.write_exchange_calendar_evidence_candidate_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE"
    assert result["candidate_status"] == "EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["calendar_evidence_candidate_semantic_digest"] == result["calendar_evidence_candidate_semantic_digest"]
    assert result["calendar_evidence_candidate_payload_digest"] == calendar_service.sha256_bytes(path.read_bytes())
    with pytest.raises(calendar_service.ExchangeCalendarEvidenceError, match="already exists"):
        calendar_service.write_exchange_calendar_evidence_candidate_v1(tmp_path)


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = calendar_service.build_exchange_calendar_evidence_candidate_markdown_v1(_candidate())

    for heading in (
        "# Exchange Calendar Evidence Candidate v1",
        "## Purpose",
        "## Frozen Identity Segment",
        "## Calendar Alias",
        "## Schedule Coverage",
        "## Monthly Cross-Check",
        "## Authority Boundary",
        "## Non-Goals",
        "## Next Steps",
    ):
        assert heading in markdown
    assert EXPECTED_IDENTITY_FROZEN_DIGEST in markdown
    assert "No provider requests were made." in markdown
    assert "No `EXCHANGE_CALENDAR_FROZEN` artifact or status is created." in markdown


def test_source_assurance_calendar_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "exchange_calendar_evidence_service.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    called_attrs = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}

    forbidden_modules = {
        "httpx",
        "requests",
        "socket",
        "urllib",
        "polygon",
        "marketflow.marketflow_strategy",
        "marketflow.marketflow_data_provider",
        "marketflow.historical_data.massive_transport",
        "marketflow.historical_data.live_month_rth_diagnostic",
        "marketflow.historical_data.monthly_acquisition",
    }
    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert {"send", "post", "put", "delete", "request"}.isdisjoint(called_attrs)
    assert "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE" in source
    assert "EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW" in source
    assert "calendar_operator_frozen" in source
    assert "strategy_runtime_migration" in source


def test_service_exports_calendar_candidate_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE"
    assert services.EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW == "EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
    assert services.build_exchange_calendar_evidence_candidate_v1 is calendar_service.build_exchange_calendar_evidence_candidate_v1
    assert services.validate_exchange_calendar_evidence_candidate_v1 is calendar_service.validate_exchange_calendar_evidence_candidate_v1
    assert services.write_exchange_calendar_evidence_candidate_v1 is calendar_service.write_exchange_calendar_evidence_candidate_v1
    assert services.build_exchange_calendar_evidence_candidate_markdown_v1 is calendar_service.build_exchange_calendar_evidence_candidate_markdown_v1
    assert services.build_exchange_calendar_schedule_rows_v1 is calendar_service.build_exchange_calendar_schedule_rows_v1
    assert services.schedule_semantic_digest is calendar_service.schedule_semantic_digest
