from __future__ import annotations

import ast
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

from marketflow.services import dividend_event_audit_service as dividend


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDENTITY_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_CALENDAR_FROZEN_DIGEST = "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
EXPECTED_SCHEDULE_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_SPLIT_FREEZE_DIGEST = "9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae"
EXPECTED_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


@lru_cache(maxsize=1)
def _cached_candidate() -> dict:
    return dividend.build_dividend_event_audit_candidate_v1()


def _candidate() -> dict:
    return deepcopy(_cached_candidate())


def _recompute_digest(candidate: dict) -> None:
    candidate["dividend_event_audit_candidate_semantic_digest"] = dividend.dividend_event_audit_candidate_semantic_digest(candidate)


def _provider_event(ex_dividend_date: str | None, **overrides) -> dict:
    event = {
        "ex_dividend_date": ex_dividend_date,
        "declaration_date": "2024-01-25",
        "record_date": "2024-02-12",
        "pay_date": "2024-02-15",
        "cash_amount": 0.24,
        "split_adjusted_cash_amount": 0.24,
        "historical_adjustment_factor": 1,
        "currency": "USD",
        "frequency": 4,
        "distribution_type": "cash",
        "dividend_type": "CD",
        "ticker": "AAPL",
    }
    event.update(overrides)
    return event


def _provider_payload(events: list[dict]) -> dict:
    return {"status": "OK", "results": events}


def _provider_bound_candidate(events: list[dict]) -> dict:
    return dividend.build_dividend_event_audit_provider_bound_candidate_v1(
        _provider_payload(events),
        provider_request_timestamp_utc="2026-08-06T00:00:00Z",
    )


def _fake_live_page(events: list[dict]) -> dict:
    return {"status": "OK", "results": events}


def _fake_live_candidate(events: list[dict]) -> dict:
    return dividend.build_dividend_event_audit_candidate_from_live_provider_v1(
        api_key="fictional-secret-key",
        transport=lambda request: _fake_live_page(events),
        request_timestamp_utc="2026-08-06T00:00:00Z",
    )


def test_candidate_scaffold_builds_offline_with_no_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(dividend.split, "build_split_event_audit_candidate_from_live_provider_v1", fail_provider_call)

    candidate = dividend.build_dividend_event_audit_candidate_v1()
    receipt = dividend.validate_dividend_event_audit_candidate_v1(candidate)

    assert calls == []
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_artifact_kind_is_dividend_event_audit_candidate():
    assert _candidate()["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE"


def test_status_requires_provider_evidence():
    assert _candidate()["candidate_status"] == "DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"


def test_candidate_binds_identity_calendar_schedule_and_split_freeze_digests():
    candidate = _candidate()

    assert candidate["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert candidate["exchange_calendar_frozen_digest"] == EXPECTED_CALENDAR_FROZEN_DIGEST
    assert candidate["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert candidate["split_event_audit_frozen_digest"] == EXPECTED_SPLIT_FREEZE_DIGEST
    assert candidate["authority_bindings"]["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert candidate["authority_bindings"]["exchange_calendar_frozen_digest"] == EXPECTED_CALENDAR_FROZEN_DIGEST
    assert candidate["authority_bindings"]["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert candidate["authority_bindings"]["split_event_audit_frozen_digest"] == EXPECTED_SPLIT_FREEZE_DIGEST


def test_candidate_binds_split_event_audit_status():
    assert _candidate()["split_event_audit_status"] == "SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT"


def test_candidate_binds_contract_digest():
    candidate = _candidate()

    assert candidate["acquisition_contract_digest"] == EXPECTED_CONTRACT_DIGEST
    assert candidate["authority_bindings"]["acquisition_contract_digest"] == EXPECTED_CONTRACT_DIGEST
    assert candidate["acquisition_contract"]["contract_digest"] == EXPECTED_CONTRACT_DIGEST


def test_candidate_binds_fixed_identity_segment():
    assert _candidate()["identity_segment"] == {
        "ticker": "AAPL",
        "composite_figi": "BBG000B9XRY4",
        "share_class_figi": "BBG001S5N8V8",
        "primary_mic": "XNAS",
        "security_type": "CS",
        "segment_start": "2022-01-01",
        "segment_end": "2025-12-31",
    }


def test_candidate_binds_fixed_acquisition_contract():
    assert _candidate()["acquisition_contract"] == {
        "contract": "CORE ACQUISITION CONTRACT v2.1",
        "contract_digest": EXPECTED_CONTRACT_DIGEST,
        "range_start": "2022-01-01",
        "range_end": "2025-12-31",
        "source": "Massive.com Custom Bars",
        "bar_interval": "15-minute",
        "adjusted": True,
        "ascending": True,
        "source_timestamps_are_aggregate_window_starts": True,
        "source_timezone": "America/New_York",
        "canonical_storage_timezone": "UTC",
    }


def test_candidate_does_not_populate_dividend_event_counts_or_status():
    outline = _candidate()["dividend_event_audit_outline"]

    assert outline["dividend_event_count_total"] is None
    assert outline["dividend_event_count_pre_range"] is None
    assert outline["dividend_event_count_in_range"] is None
    assert outline["dividend_event_count_post_range"] is None
    assert outline["dividend_event_count_unknown"] is None
    assert outline["dividend_events"] == []
    assert outline["audit_status"] is None


def test_candidate_does_not_bind_provider_artifacts():
    status = _candidate()["source_evidence_status"]

    assert status["provider_evidence_required"] is True
    assert status["provider_evidence_status"] == "NOT_BOUND"
    assert status["provider_request_performed_in_this_task"] is False
    assert status["provider_endpoint"] is None
    assert status["provider_query_identifier"] is None
    assert status["raw_response_artifact_id"] is None
    assert status["raw_response_semantic_digest"] is None
    assert status["event_timeline_artifact_id"] is None
    assert status["event_timeline_semantic_digest"] is None
    assert status["audit_receipt_artifact_id"] is None


def test_provider_and_freeze_flags_match_scaffold_boundary():
    candidate = _candidate()

    assert candidate["provider_requests_made"] is False
    assert candidate["dividend_events_provider_evidence_bound"] is False
    assert candidate["dividend_event_audit_complete"] is False
    assert candidate["dividend_event_audit_frozen"] is False
    assert candidate["operator_review_required"] is True
    assert candidate["operator_freeze_required"] is True


def test_authorities_reflect_identity_calendar_and_split_frozen_only():
    candidate = _candidate()
    boundary = candidate["authority_boundary"]

    assert candidate["identity_segment_frozen"] is True
    assert candidate["calendar_operator_frozen"] is True
    assert candidate["split_event_audit_frozen"] is True
    assert boundary["identity_segment_frozen"] is True
    assert boundary["calendar_operator_frozen"] is True
    assert boundary["split_event_audit_frozen"] is True
    assert boundary["dividend_event_audit_frozen"] is False


def test_canonical_registry_acquisition_and_runtime_flags_remain_false():
    candidate = _candidate()
    boundary = candidate["authority_boundary"]

    for field in (
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        assert candidate[field] is False
        assert boundary[field] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"
    assert candidate["authority_boundary"]["predictive_usefulness"] == "not accepted"
    assert candidate["authority_boundary"]["profitability"] == "not accepted"


def test_expected_future_normalized_dividend_event_fields_are_definitions_only():
    candidate = _candidate()

    assert candidate["expected_future_normalized_dividend_event_fields"] == [
        "ex_dividend_date",
        "declaration_date",
        "record_date",
        "pay_date",
        "cash_amount",
        "split_adjusted_cash_amount",
        "historical_adjustment_factor",
        "currency",
        "frequency",
        "distribution_type",
        "dividend_type_if_available",
        "ticker",
        "composite_figi_if_available",
        "raw_event_index",
        "raw_event_digest",
        "event_position",
    ]
    assert candidate["valid_event_positions"] == ["PRE_RANGE", "IN_RANGE", "POST_RANGE", "UNKNOWN"]
    assert candidate["dividend_event_audit_outline"]["dividend_events"] == []


def test_candidate_digest_is_deterministic():
    first = dividend.build_dividend_event_audit_candidate_v1()
    second = dividend.build_dividend_event_audit_candidate_v1()

    assert first == second
    assert len(first["dividend_event_audit_candidate_semantic_digest"]) == 64
    assert first["dividend_event_audit_candidate_semantic_digest"] == dividend.dividend_event_audit_candidate_semantic_digest(first)


def test_validator_accepts_valid_scaffold_candidate():
    receipt = dividend.validate_dividend_event_audit_candidate_v1(_candidate())

    assert receipt["status"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_VALID"
    assert receipt["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE"
    assert receipt["candidate_status"] == "DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
    assert receipt["dividend_events_provider_evidence_bound"] is False
    assert receipt["dividend_event_audit_complete"] is False
    assert receipt["dividend_event_audit_frozen"] is False


@pytest.mark.parametrize(
    ("field", "value"),
        [
            ("artifact_kind", "SPLIT_EVENT_AUDIT_CANDIDATE"),
            ("schema_version", "dividend_event_audit_candidate_v2"),
            ("candidate_status", "DIVIDEND_EVENT_AUDIT_FROZEN"),
        ],
)
def test_validator_rejects_wrong_kind_schema_or_status(field: str, value: str):
    candidate = _candidate()
    candidate[field] = value
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match=field):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_provider_requests_made_true():
    candidate = _candidate()
    candidate["provider_requests_made"] = True
    candidate["guardrails"]["provider_requests_made"] = True
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="provider_requests_made"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_provider_evidence_bound_true():
    candidate = _candidate()
    candidate["dividend_events_provider_evidence_bound"] = True
    candidate["guardrails"]["provider_evidence_bound"] = True
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="dividend_events_provider_evidence_bound"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "provider_endpoint",
        "provider_query_identifier",
        "raw_response_artifact_id",
        "raw_response_semantic_digest",
        "event_timeline_artifact_id",
        "event_timeline_semantic_digest",
        "audit_receipt_artifact_id",
    ],
)
def test_validator_rejects_populated_provider_artifacts(field: str):
    candidate = _candidate()
    candidate["source_evidence_status"][field] = "unexpected-provider-evidence"
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize("field", dividend.DIVIDEND_EVENT_COUNT_FIELDS)
def test_validator_rejects_event_counts_populated_without_provider_evidence(field: str):
    candidate = _candidate()
    candidate["dividend_event_audit_outline"][field] = 0
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_dividend_events_populated_without_provider_evidence():
    candidate = _candidate()
    candidate["dividend_event_audit_outline"]["dividend_events"] = [{"ex_dividend_date": "2024-01-01"}]
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_dividend_audit_status_populated_without_provider_evidence():
    candidate = _candidate()
    candidate["dividend_event_audit_outline"]["audit_status"] = "DIVIDEND_EVENT_AUDIT_COMPLETE"
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="audit_status"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_dividend_event_audit_frozen_true():
    candidate = _candidate()
    candidate["dividend_event_audit_frozen"] = True
    candidate["authority_boundary"]["dividend_event_audit_frozen"] = True
    candidate["guardrails"]["dividend_event_audit_frozen"] = True
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="dividend_event_audit_frozen"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_dividend_event_audit_complete_true():
    candidate = _candidate()
    candidate["dividend_event_audit_complete"] = True
    candidate["guardrails"]["dividend_event_audit_complete"] = True
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="dividend_event_audit_complete"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    ("field", "binding_field", "contract_field"),
    [
        ("identity_segment_frozen_digest", "identity_segment_frozen_digest", None),
        ("exchange_calendar_frozen_digest", "exchange_calendar_frozen_digest", None),
        ("schedule_semantic_digest", "schedule_semantic_digest", None),
        ("split_event_audit_frozen_digest", "split_event_audit_frozen_digest", None),
        ("acquisition_contract_digest", "acquisition_contract_digest", "contract_digest"),
    ],
)
def test_validator_rejects_wrong_authority_digests(field: str, binding_field: str, contract_field: str | None):
    candidate = _candidate()
    candidate[field] = "0" * 64
    candidate["authority_bindings"][binding_field] = "0" * 64
    if contract_field is not None:
        candidate["acquisition_contract"][contract_field] = "0" * 64
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match=field):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("ticker", "MSFT"),
        ("composite_figi", "BBG000BPH459"),
        ("share_class_figi", "BBG001S5TD05"),
        ("primary_mic", "XNYS"),
        ("security_type", "ETF"),
        ("segment_start", "2022-01-02"),
        ("segment_end", "2025-12-30"),
    ],
)
def test_validator_rejects_wrong_identity_segment(field: str, value: str):
    candidate = _candidate()
    candidate["identity_segment"][field] = value
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="identity_segment"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_validator_rejects_authority_flags_true(field: str):
    candidate = _candidate()
    candidate[field] = True
    candidate["authority_boundary"][field] = True
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match=field):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_validator_rejects_predictive_or_profitability_accepted(field: str):
    candidate = _candidate()
    candidate[field] = "accepted"
    candidate["authority_boundary"][field] = "accepted"
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match=field):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_wrong_split_event_audit_status():
    candidate = _candidate()
    candidate["split_event_audit_status"] = "SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT"
    candidate["authority_bindings"]["split_event_audit_status"] = "SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT"
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="split_event_audit_status"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("dividend_event_audit_candidate_semantic_digest")

    with pytest.raises(dividend.DividendEventAuditError, match="dividend_event_audit_candidate_semantic_digest"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_digest_mismatch():
    candidate = _candidate()
    candidate["next_required_task"] = "UNEXPECTED"

    with pytest.raises(dividend.DividendEventAuditError, match="next_required_task"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_checklist_contains_required_check_ids():
    candidate = _candidate()
    summary = candidate["scaffold_summary"]

    assert [item["check_id"] for item in candidate["scaffold_checklist"]] == dividend.REQUIRED_CHECK_IDS
    assert summary["total_checks"] == len(dividend.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(dividend.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_provider_evidence_collection"] is True
    assert summary["dividend_event_audit_complete"] is False
    assert summary["dividend_event_audit_frozen"] is False
    assert summary["software_auto_approval"] is False


def test_remaining_roadmap_names_future_provider_backed_chain():
    assert _candidate()["remaining_roadmap"] == [
        "Dividend-event provider evidence collection.",
        "Dividend-event audit candidate with bound provider evidence.",
        "Dividend-event operator review package.",
        "Dividend-event operator freeze ceremony.",
        "Full 2022-2025 acquisition generation.",
        "Acquisition-generation freeze.",
        "SWING canonical dataset and registry approval.",
        "POSITION_SWING canonical dataset and registry approval.",
        "Normal runtime migration.",
        "Applicability/research campaign.",
        "Predictive and profitability evaluation.",
    ]
    assert _candidate()["next_required_task"] == "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION"


def test_writer_writes_json_and_does_not_freeze(tmp_path: Path):
    result = dividend.write_dividend_event_audit_candidate_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE"
    assert result["candidate_status"] == "DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["dividend_event_audit_frozen"] is False
    assert payload["dividend_events_provider_evidence_bound"] is False
    assert payload["provider_requests_made"] is False
    assert payload["dividend_event_audit_candidate_semantic_digest"] == result["dividend_event_audit_candidate_semantic_digest"]
    assert result["dividend_event_audit_candidate_payload_digest"] == dividend.sha256_bytes(path.read_bytes())
    with pytest.raises(dividend.DividendEventAuditError, match="already exists"):
        dividend.write_dividend_event_audit_candidate_v1(tmp_path)


def test_markdown_includes_required_sections_and_guardrails():
    markdown = dividend.build_dividend_event_audit_candidate_markdown_v1(_candidate())

    for heading in (
        "# Dividend-Event Audit Candidate v1",
        "## Candidate",
        "## Frozen Authority Bindings",
        "## Provider Evidence",
        "## Authority Boundary",
        "## Expected Normalized Fields",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_IDENTITY_FROZEN_DIGEST in markdown
    assert EXPECTED_CALENDAR_FROZEN_DIGEST in markdown
    assert EXPECTED_SCHEDULE_DIGEST in markdown
    assert EXPECTED_SPLIT_FREEZE_DIGEST in markdown
    assert "No provider requests were made." in markdown
    assert "No dividend-event provider evidence is bound." in markdown
    assert "No dividend audit freeze is claimed." in markdown


def test_source_assurance_service_has_no_provider_strategy_runtime_broker_or_dividend_endpoint_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "dividend_event_audit_service.py"
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
        "marketflow.historical_data.polygon",
    }
    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert {"send", "post", "put", "delete", "request", "execute"}.isdisjoint(called_attrs)
    assert "DIVIDEND_EVENT_AUDIT_CANDIDATE" in source
    assert "DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE" in source
    assert "provider_requests_made" in source
    assert "strategy_runtime_migration" in source


def test_service_exports_dividend_event_candidate_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE == "DIVIDEND_EVENT_AUDIT_CANDIDATE"
    assert services.DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE == "DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
    assert services.DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND == "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
    assert services.build_dividend_event_audit_candidate_v1 is dividend.build_dividend_event_audit_candidate_v1
    assert services.build_dividend_event_audit_candidate_from_live_provider_v1 is dividend.build_dividend_event_audit_candidate_from_live_provider_v1
    assert services.build_dividend_event_audit_provider_bound_candidate_v1 is dividend.build_dividend_event_audit_provider_bound_candidate_v1
    assert services.validate_dividend_event_audit_candidate_v1 is dividend.validate_dividend_event_audit_candidate_v1
    assert services.write_dividend_event_audit_candidate_v1 is dividend.write_dividend_event_audit_candidate_v1
    assert services.build_dividend_event_audit_candidate_markdown_v1 is dividend.build_dividend_event_audit_candidate_markdown_v1
    assert services.dividend_event_audit_candidate_semantic_digest is dividend.dividend_event_audit_candidate_semantic_digest


def test_provider_bound_candidate_builds_from_injected_response_without_live_provider_call(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(dividend, "_api_key_from_environment", fail_provider_call)
    candidate = _provider_bound_candidate([])

    assert calls == []
    assert candidate["provider_requests_made"] is False
    assert candidate["provider_response_injected"] is True
    assert candidate["dividend_events_provider_evidence_bound"] is True


def test_provider_bound_candidate_artifact_kind_status_and_freeze_flags():
    candidate = _provider_bound_candidate([])

    assert candidate["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE"
    assert candidate["candidate_status"] == "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
    assert candidate["dividend_event_audit_complete"] is True
    assert candidate["dividend_event_audit_frozen"] is False
    assert candidate["operator_review_required"] is True
    assert candidate["operator_freeze_required"] is True


def test_provider_bound_event_counts_are_derived_from_response_data():
    candidate = _provider_bound_candidate(
        [
            _provider_event("2021-12-31"),
            _provider_event("2024-02-09"),
            _provider_event("2026-01-01"),
            _provider_event("not-a-date"),
        ]
    )
    outline = candidate["dividend_event_audit_outline"]

    assert outline["dividend_event_count_total"] == 4
    assert outline["dividend_event_count_pre_range"] == 1
    assert outline["dividend_event_count_in_range"] == 1
    assert outline["dividend_event_count_post_range"] == 1
    assert outline["dividend_event_count_unknown"] == 1
    assert candidate["provider_evidence"]["provider_raw_response_row_count"] == 4


def test_provider_bound_zero_in_range_count_supports_no_reported_dividend_status():
    candidate = _provider_bound_candidate([_provider_event("2021-12-31"), _provider_event("2026-01-01")])

    assert candidate["dividend_event_audit_outline"]["dividend_event_count_in_range"] == 0
    assert candidate["dividend_event_audit_outline"]["audit_status"] == "DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND"


def test_provider_bound_in_range_count_reports_in_range_dividend_status():
    candidate = _provider_bound_candidate([_provider_event("2024-02-09")])

    assert candidate["dividend_event_audit_outline"]["dividend_event_count_in_range"] == 1
    assert candidate["dividend_event_audit_outline"]["audit_status"] == "DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND"


def test_provider_bound_digests_are_deterministic():
    first = _provider_bound_candidate([_provider_event("2024-02-09")])
    second = _provider_bound_candidate([_provider_event("2024-02-09")])

    assert first == second
    assert len(first["dividend_event_provider_raw_response_digest"]) == 64
    assert len(first["dividend_event_timeline_semantic_digest"]) == 64
    assert len(first["dividend_event_audit_receipt_digest"]) == 64
    assert len(first["dividend_event_audit_candidate_semantic_digest"]) == 64
    assert first["dividend_event_audit_candidate_semantic_digest"] == dividend.dividend_event_audit_candidate_semantic_digest(first)


def test_provider_bound_event_position_classification_handles_pre_in_post_and_unknown():
    events = _provider_bound_candidate(
        [
            _provider_event("2021-12-31"),
            _provider_event("2024-02-09"),
            _provider_event("2026-01-01"),
            _provider_event(None),
        ]
    )["dividend_event_audit_outline"]["dividend_events"]

    assert {event["event_position"] for event in events} == {"PRE_RANGE", "IN_RANGE", "POST_RANGE", "UNKNOWN"}


def test_provider_bound_missing_provider_fields_remain_null():
    event = _provider_bound_candidate([{"ex_dividend_date": "2024-02-09"}])["dividend_event_audit_outline"]["dividend_events"][0]

    assert event["declaration_date"] is None
    assert event["record_date"] is None
    assert event["pay_date"] is None
    assert event["cash_amount"] is None
    assert event["split_adjusted_cash_amount"] is None
    assert event["historical_adjustment_factor"] is None
    assert event["currency"] is None
    assert event["frequency"] is None
    assert event["distribution_type"] is None
    assert event["dividend_type_if_available"] is None
    assert event["ticker"] is None
    assert event["composite_figi_if_available"] is None


def test_validator_accepts_valid_provider_bound_candidate():
    receipt = dividend.validate_dividend_event_audit_candidate_v1(_provider_bound_candidate([_provider_event("2024-02-09")]))

    assert receipt["candidate_status"] == "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
    assert receipt["dividend_events_provider_evidence_bound"] is True
    assert receipt["dividend_event_audit_complete"] is True
    assert receipt["dividend_event_audit_frozen"] is False


def test_validator_rejects_provider_bound_candidate_without_raw_response_digest():
    candidate = _provider_bound_candidate([_provider_event("2024-02-09")])
    candidate["provider_evidence"]["provider_raw_response_digest"] = None
    candidate["source_evidence_status"]["raw_response_semantic_digest"] = None
    candidate["dividend_event_provider_raw_response_digest"] = None
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="provider_raw_response_digest"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_provider_bound_inconsistent_event_counts():
    candidate = _provider_bound_candidate([_provider_event("2024-02-09")])
    candidate["dividend_event_audit_outline"]["dividend_event_count_total"] = 2
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="count totals inconsistent"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_validator_rejects_provider_bound_dividend_event_audit_frozen_true():
    candidate = _provider_bound_candidate([_provider_event("2024-02-09")])
    candidate["dividend_event_audit_frozen"] = True
    candidate["authority_boundary"]["dividend_event_audit_frozen"] = True
    candidate["guardrails"]["dividend_event_audit_frozen"] = True
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match="dividend_event_audit_frozen"):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_validator_rejects_provider_bound_authority_flags_true(field: str):
    candidate = _provider_bound_candidate([_provider_event("2024-02-09")])
    candidate[field] = True
    candidate["authority_boundary"][field] = True
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match=field):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_validator_rejects_provider_bound_predictive_or_profitability_accepted(field: str):
    candidate = _provider_bound_candidate([_provider_event("2024-02-09")])
    candidate[field] = "accepted"
    candidate["authority_boundary"][field] = "accepted"
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match=field):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    ("field", "binding_field", "contract_field"),
    [
        ("identity_segment_frozen_digest", "identity_segment_frozen_digest", None),
        ("exchange_calendar_frozen_digest", "exchange_calendar_frozen_digest", None),
        ("schedule_semantic_digest", "schedule_semantic_digest", None),
        ("split_event_audit_frozen_digest", "split_event_audit_frozen_digest", None),
        ("acquisition_contract_digest", "acquisition_contract_digest", "contract_digest"),
    ],
)
def test_validator_rejects_provider_bound_wrong_authority_digests(field: str, binding_field: str, contract_field: str | None):
    candidate = _provider_bound_candidate([_provider_event("2024-02-09")])
    candidate[field] = "f" * 64
    candidate["authority_bindings"][binding_field] = "f" * 64
    if contract_field is not None:
        candidate["acquisition_contract"][contract_field] = "f" * 64
    _recompute_digest(candidate)

    with pytest.raises(dividend.DividendEventAuditError, match=field):
        dividend.validate_dividend_event_audit_candidate_v1(candidate)


def test_live_provider_builder_is_disabled_without_explicit_gate(monkeypatch):
    monkeypatch.delenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", raising=False)

    result = dividend.build_dividend_event_audit_candidate_from_live_provider_v1(
        api_key="fictional-secret-key",
        transport=lambda request: pytest.fail("transport must not be used"),
        request_timestamp_utc="2026-08-06T00:00:00Z",
    )

    assert result["status"] == "DIVIDEND_EVENT_LIVE_PROVIDER_COLLECTION_DISABLED"
    assert result["provider_requests_made"] is False
    assert result["dividend_event_audit_frozen"] is False


def test_live_provider_builder_requires_api_key_when_gate_enabled(monkeypatch):
    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", "1")
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)

    result = dividend.build_dividend_event_audit_candidate_from_live_provider_v1(
        transport=lambda request: pytest.fail("transport must not be used"),
        request_timestamp_utc="2026-08-06T00:00:00Z",
    )

    assert result["status"] == "DIVIDEND_EVENT_LIVE_PROVIDER_API_KEY_MISSING"
    assert result["provider_requests_made"] is False
    assert result["provider_response_injected"] is False


def test_live_provider_bound_candidate_has_live_flags_and_status(monkeypatch):
    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", "1")
    candidate = _fake_live_candidate([])

    assert candidate["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE"
    assert candidate["candidate_status"] == "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
    assert candidate["provider_requests_made"] is True
    assert candidate["provider_response_injected"] is False
    assert candidate["provider_request_mode"] == "LIVE_PROVIDER_REQUEST"
    assert candidate["dividend_events_provider_evidence_bound"] is True
    assert candidate["dividend_event_audit_complete"] is True
    assert candidate["dividend_event_audit_frozen"] is False


def test_live_provider_empty_response_yields_zero_counts_and_no_reported_dividend_status(monkeypatch):
    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", "1")
    outline = _fake_live_candidate([])["dividend_event_audit_outline"]

    assert outline["dividend_event_count_total"] == 0
    assert outline["dividend_event_count_in_range"] == 0
    assert outline["audit_status"] == "DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND"


def test_live_provider_in_range_response_yields_reported_dividend_status(monkeypatch):
    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", "1")
    candidate = _fake_live_candidate([_provider_event("2024-02-09")])

    assert candidate["dividend_event_audit_outline"]["dividend_event_count_in_range"] == 1
    assert candidate["dividend_event_audit_outline"]["audit_status"] == "DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND"


def test_live_provider_classifies_pre_in_post_and_unknown_dates(monkeypatch):
    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", "1")
    outline = _fake_live_candidate(
        [
            _provider_event("2021-12-31"),
            _provider_event("2024-02-09"),
            _provider_event("2026-01-01"),
            _provider_event("not-a-date"),
        ]
    )["dividend_event_audit_outline"]

    assert outline["dividend_event_count_pre_range"] == 1
    assert outline["dividend_event_count_in_range"] == 1
    assert outline["dividend_event_count_post_range"] == 1
    assert outline["dividend_event_count_unknown"] == 1
    assert {event["event_position"] for event in outline["dividend_events"]} == {"PRE_RANGE", "IN_RANGE", "POST_RANGE", "UNKNOWN"}


def test_live_provider_candidate_does_not_store_api_key(monkeypatch):
    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", "1")
    seen: list[dict] = []

    def fake_transport(request):
        seen.append(dict(request))
        return _fake_live_page([])

    candidate = dividend.build_dividend_event_audit_candidate_from_live_provider_v1(
        api_key="fictional-secret-key",
        transport=fake_transport,
        request_timestamp_utc="2026-08-06T00:00:00Z",
    )
    rendered = json.dumps(candidate, sort_keys=True)
    request_rendered = json.dumps(seen, sort_keys=True)

    assert "fictional-secret-key" not in rendered
    assert "fictional-secret-key" not in request_rendered
    assert "api_key" not in rendered.lower()
    assert "apikey" not in rendered.lower()


def test_validator_accepts_valid_fake_live_provider_bound_candidate(monkeypatch):
    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT", "1")
    receipt = dividend.validate_dividend_event_audit_candidate_v1(_fake_live_candidate([_provider_event("2024-02-09")]))

    assert receipt["candidate_status"] == "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
    assert receipt["provider_requests_made"] is True
    assert receipt["provider_response_injected"] is False
    assert receipt["provider_request_mode"] == "LIVE_PROVIDER_REQUEST"
