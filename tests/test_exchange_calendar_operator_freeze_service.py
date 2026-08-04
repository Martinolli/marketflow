from __future__ import annotations

import ast
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

from marketflow.services import exchange_calendar_evidence_service as calendar
from marketflow.services import exchange_calendar_operator_freeze_service as ceremony
from marketflow.services import exchange_calendar_operator_review_service as review


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CALENDAR_CANDIDATE_DIGEST = "867aa02ad9c9c737eda3d8398eda4e4aad3181cd4bc5505600ccf9647b0d60ee"
EXPECTED_REVIEW_DIGEST = "5e7e528068cd161e06a7a3cf6b30c40909023f23eb6b64661abb063363a690cb"
EXPECTED_SCHEDULE_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_IDENTITY_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
TEST_TIMESTAMP = "2026-08-04T00:00:00Z"


def _attestation(**overrides: object) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": TEST_TIMESTAMP,
        "operator_attestation_phrase": ceremony.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_calendar_candidate_digest": EXPECTED_CALENDAR_CANDIDATE_DIGEST,
        "operator_confirms_calendar_review_package_digest": EXPECTED_REVIEW_DIGEST,
        "operator_confirms_schedule_digest": EXPECTED_SCHEDULE_DIGEST,
        "operator_confirms_identity_segment_frozen_digest": EXPECTED_IDENTITY_FROZEN_DIGEST,
        "operator_confirms_no_provider_requests": True,
        "operator_confirms_no_canonical_approval": True,
        "operator_confirms_no_registry_approval": True,
        "operator_confirms_no_acquisition_generation_freeze": True,
        "operator_confirms_no_strategy_runtime_migration": True,
    }
    values.update(overrides)
    return ceremony.build_exchange_calendar_operator_attestation_v1(**values)


@lru_cache(maxsize=1)
def _cached_frozen() -> dict:
    return ceremony.build_exchange_calendar_frozen_v1(operator_attestation=_attestation())


def _frozen(**overrides: object) -> dict:
    if not overrides:
        return deepcopy(_cached_frozen())
    values = {"operator_attestation": _attestation()}
    values.update(overrides)
    return ceremony.build_exchange_calendar_frozen_v1(**values)


def _recompute_digest(frozen: dict) -> None:
    frozen["exchange_calendar_frozen_semantic_digest"] = ceremony.exchange_calendar_frozen_semantic_digest(frozen)


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == "APPROVE_EXCHANGE_CALENDAR_FREEZE"
    assert attestation["operator_attestation_phrase"] == ceremony.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_attestation_timestamp_utc"] == TEST_TIMESTAMP
    assert attestation["operator_attestation_version"] == "exchange_calendar_operator_attestation_v1"
    assert attestation["operator_confirms_calendar_candidate_digest"] == EXPECTED_CALENDAR_CANDIDATE_DIGEST
    assert attestation["operator_confirms_calendar_review_package_digest"] == EXPECTED_REVIEW_DIGEST
    assert attestation["operator_confirms_schedule_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert attestation["operator_confirms_identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    for field in ceremony.OPERATOR_BOUNDARY_CONFIRMATION_FIELDS:
        assert attestation[field] is True


def test_frozen_artifact_builds_offline_without_provider_or_identity_refresh_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(calendar.identity_candidate.ident, "TickerOverviewTransport", fail_provider_call)
    monkeypatch.setattr(calendar.identity_candidate.tkev, "TickerEventsTransport", fail_provider_call)
    monkeypatch.setattr(calendar.identity_candidate.tkev, "validate_accepted_source_identity_evidence", fail_provider_call)

    frozen = ceremony.build_exchange_calendar_frozen_v1(operator_attestation=_attestation())
    receipt = ceremony.validate_exchange_calendar_frozen_v1(frozen)

    assert calls == []
    assert frozen["created_offline"] is True
    assert frozen["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_artifact_kind_status_and_calendar_freeze_state():
    frozen = _frozen()

    assert frozen["artifact_kind"] == "EXCHANGE_CALENDAR_FROZEN"
    assert frozen["schema_version"] == "exchange_calendar_operator_freeze_v1"
    assert frozen["freeze_status"] == "EXCHANGE_CALENDAR_FROZEN"
    assert frozen["identity_segment_frozen"] is True
    assert frozen["calendar_operator_frozen"] is True
    assert frozen["authority_boundary"]["calendar_operator_frozen"] is True


def test_source_candidate_review_identity_and_schedule_digests_are_bound():
    frozen = _frozen()

    assert frozen["source_calendar_candidate_kind"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE"
    assert frozen["source_calendar_candidate_status"] == "EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
    assert frozen["source_calendar_candidate_semantic_digest"] == EXPECTED_CALENDAR_CANDIDATE_DIGEST
    assert frozen["source_calendar_review_package_kind"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE"
    assert frozen["source_calendar_review_status"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY"
    assert frozen["source_calendar_review_package_semantic_digest"] == EXPECTED_REVIEW_DIGEST
    assert frozen["source_identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert frozen["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST


def test_wrong_operator_attestation_phrase_is_rejected():
    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match="operator_attestation_phrase"):
        _frozen(operator_attestation=_attestation(operator_attestation_phrase="wrong phrase"))


def test_wrong_operator_decision_is_rejected():
    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match="operator_decision"):
        _frozen(operator_attestation=_attestation(operator_decision="REJECT_EXCHANGE_CALENDAR_FREEZE"))


@pytest.mark.parametrize(
    ("field", "match"),
    [
        ("operator_confirms_calendar_candidate_digest", "operator_calendar_candidate_digest"),
        ("operator_confirms_calendar_review_package_digest", "operator_calendar_review_digest"),
        ("operator_confirms_schedule_digest", "operator_schedule_digest"),
        ("operator_confirms_identity_segment_frozen_digest", "operator_identity_frozen_digest"),
    ],
)
def test_wrong_operator_digest_confirmation_is_rejected(field: str, match: str):
    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match=match):
        _frozen(operator_attestation=_attestation(**{field: "0" * 64}))


def test_missing_attestation_is_rejected():
    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match="operator_attestation"):
        ceremony.build_exchange_calendar_frozen_v1(operator_attestation=None)


@pytest.mark.parametrize("field", ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"))
def test_empty_attestation_identity_fields_are_rejected(field: str):
    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match=field):
        _frozen(operator_attestation=_attestation(**{field: "  "}))


def test_review_package_with_blocker_count_is_rejected():
    package = review.build_exchange_calendar_evidence_candidate_review_package_v1()
    package["review_summary"]["blocker_count"] = 1
    package["calendar_review_package_semantic_digest"] = review.calendar_review_package_semantic_digest(package)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError):
        _frozen(calendar_review_package=package)


def test_calendar_candidate_digest_drift_is_rejected():
    candidate = calendar.build_exchange_calendar_evidence_candidate_v1()
    candidate["schedule_coverage"]["session_count"] = 1004
    candidate["calendar_evidence_candidate_semantic_digest"] = calendar.calendar_evidence_candidate_semantic_digest(candidate)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError):
        _frozen(calendar_candidate=candidate)


def test_frozen_calendar_binding_sets_only_calendar_authority_to_operator_frozen():
    frozen = _frozen()
    binding = frozen["frozen_calendar_binding"]

    assert binding["requested_calendar"] == "XNAS"
    assert binding["resolved_calendar"] == "XNYS"
    assert binding["calendar_alias"] == "XNAS_USES_XNYS_SCHEDULE"
    assert binding["calendar_timezone"] == "America/New_York"
    assert binding["canonical_storage_timezone"] == "UTC"
    assert binding["calendar_source_library"] == "exchange_calendars"
    assert binding["calendar_source_library_version"] == "4.13.2"
    assert binding["calendar_source_authority"] == "LOCAL_EXCHANGE_CALENDARS_XNYS_ALIAS_CANDIDATE"
    assert binding["calendar_authority_status"] == "OPERATOR_FROZEN"
    assert binding["calendar_operator_frozen"] is True
    assert binding["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST


def test_frozen_identity_segment_binding_and_contract_are_preserved():
    frozen = _frozen()
    identity = frozen["frozen_identity_segment_binding"]

    assert identity["ticker"] == "AAPL"
    assert identity["composite_figi"] == "BBG000B9XRY4"
    assert identity["share_class_figi"] == "BBG001S5N8V8"
    assert identity["primary_mic"] == "XNAS"
    assert identity["security_type"] == "CS"
    assert identity["segment_start"] == "2022-01-01"
    assert identity["segment_end"] == "2025-12-31"
    assert identity["identity_segment_frozen"] is True
    assert identity["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert frozen["acquisition_contract_digest"] == "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
    assert frozen["acquisition_contract"]["contract_digest"] == frozen["acquisition_contract_digest"]


def test_schedule_coverage_is_preserved_from_candidate():
    coverage = _frozen()["schedule_coverage"]

    assert coverage["range_start"] == "2022-01-01"
    assert coverage["range_end"] == "2025-12-31"
    assert coverage["session_count"] == 1003
    assert coverage["full_session_count"] == 994
    assert coverage["half_session_count"] == 9
    assert coverage["special_close_count"] == 9
    assert coverage["special_open_count"] == 0
    assert coverage["first_session"] == "2022-01-03"
    assert coverage["last_session"] == "2025-12-31"
    assert coverage["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST


def test_monthly_2025_01_cross_check_values_are_preserved():
    monthly = _frozen()["accepted_monthly_cross_check"]

    assert monthly["normalized_source_rows"] == 1277
    assert monthly["extended_hours_rows"] == 757
    assert monthly["expected_rth_rows"] == 520
    assert monthly["validated_rth_rows"] == 520
    assert monthly["rth_reconciliation"] == "RTH_SOURCE_ROWS_RECONCILED"
    assert monthly["full_ordinary_sessions"] == 20
    assert monthly["incomplete_ordinary_sessions"] == 0
    assert monthly["swing_rth_half_session_195m_bars"] == 40
    assert monthly["position_swing_rth_full_session_1d_bars"] == 20


def test_canonical_registry_acquisition_runtime_predictive_and_profitability_remain_unaccepted():
    frozen = _frozen()
    boundary = frozen["authority_boundary"]

    for field in (
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        assert frozen[field] is False
        assert boundary[field] is False
    assert frozen["predictive_usefulness"] == "not accepted"
    assert frozen["profitability"] == "not accepted"
    assert boundary["predictive_usefulness"] == "not accepted"
    assert boundary["profitability"] == "not accepted"


@pytest.mark.parametrize("field", ceremony.OPERATOR_BOUNDARY_CONFIRMATION_FIELDS)
def test_any_false_operator_boundary_confirmation_is_rejected(field: str):
    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match=field):
        _frozen(operator_attestation=_attestation(**{field: False}))


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
def test_validator_rejects_boundary_flag_flipped_true(field: str):
    frozen = _frozen()
    frozen[field] = True
    frozen["authority_boundary"][field] = True
    _recompute_digest(frozen)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError):
        ceremony.validate_exchange_calendar_frozen_v1(frozen)


def test_validator_rejects_calendar_operator_frozen_flipped_false():
    frozen = _frozen()
    frozen["calendar_operator_frozen"] = False
    frozen["authority_boundary"]["calendar_operator_frozen"] = False
    _recompute_digest(frozen)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match="calendar_operator_frozen"):
        ceremony.validate_exchange_calendar_frozen_v1(frozen)


def test_validator_rejects_changed_calendar_alias_binding():
    frozen = _frozen()
    frozen["frozen_calendar_binding"]["calendar_alias"] = "XNAS_DIRECT"
    _recompute_digest(frozen)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError):
        ceremony.validate_exchange_calendar_frozen_v1(frozen)


def test_validator_rejects_changed_schedule_digest():
    frozen = _frozen()
    frozen["schedule_semantic_digest"] = "1" * 64
    frozen["frozen_calendar_binding"]["schedule_semantic_digest"] = "1" * 64
    _recompute_digest(frozen)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError):
        ceremony.validate_exchange_calendar_frozen_v1(frozen)


def test_validator_rejects_changed_monthly_cross_check():
    frozen = _frozen()
    frozen["accepted_monthly_cross_check"]["expected_rth_rows"] = 519
    _recompute_digest(frozen)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError):
        ceremony.validate_exchange_calendar_frozen_v1(frozen)


def test_validator_rejects_provider_requests_made_true():
    frozen = _frozen()
    frozen["provider_requests_made"] = True
    frozen["guardrails"]["provider_requests_made"] = True
    _recompute_digest(frozen)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match="provider_requests_made"):
        ceremony.validate_exchange_calendar_frozen_v1(frozen)


def test_validator_rejects_canonical_or_registry_approval_guardrails():
    frozen = _frozen()
    frozen["guardrails"]["canonical_dataset_created"] = True
    frozen["guardrails"]["registry_approval_created"] = True
    _recompute_digest(frozen)

    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError):
        ceremony.validate_exchange_calendar_frozen_v1(frozen)


def test_frozen_artifact_digest_is_deterministic_for_same_attestation():
    attestation = _attestation()
    first = ceremony.build_exchange_calendar_frozen_v1(operator_attestation=attestation)
    second = ceremony.build_exchange_calendar_frozen_v1(operator_attestation=deepcopy(attestation))

    assert first == second
    assert len(first["exchange_calendar_frozen_semantic_digest"]) == 64
    assert first["exchange_calendar_frozen_semantic_digest"] == ceremony.exchange_calendar_frozen_semantic_digest(first)


def test_freeze_checklist_totals_authority_and_review_counts():
    frozen = _frozen()
    summary = frozen["freeze_summary"]

    assert [item["check_id"] for item in frozen["freeze_checklist"]] == ceremony.REQUIRED_FREEZE_CHECK_IDS
    assert summary["total_checks"] == len(ceremony.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["passed_checks"] == len(ceremony.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["exchange_calendar_freeze_authorized_by_operator"] is True
    assert summary["software_auto_approval"] is False
    assert frozen["source_calendar_review_checklist_total"] == 40
    assert frozen["source_calendar_review_checklist_passed"] == 40
    assert frozen["source_calendar_review_checklist_failed"] == 0
    assert frozen["source_calendar_review_blocker_count"] == 0


def test_remaining_roadmap_includes_required_future_work_after_calendar_freeze():
    roadmap = _frozen()["remaining_roadmap"]
    rendered = "\n".join(roadmap)

    assert "Split-event audit." in roadmap
    assert "Dividend-event audit." in roadmap
    assert "Full 2022-2025 acquisition generation." in roadmap
    assert "Acquisition-generation freeze." in roadmap
    assert "SWING canonical dataset and registry approval." in roadmap
    assert "POSITION_SWING canonical dataset and registry approval." in roadmap
    assert "Normal runtime migration." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap
    assert "canonical dataset" in rendered


def test_markdown_writer_includes_required_sections_and_guardrails():
    frozen = _frozen()
    markdown = ceremony.build_exchange_calendar_frozen_markdown_v1(frozen)

    for heading in (
        "# Exchange Calendar Frozen v1",
        "## Frozen Calendar Evidence",
        "## Operator Attestation",
        "## Source Candidate",
        "## Source Review Package",
        "## Schedule Coverage",
        "## Freeze Checklist Summary",
        "## Authority Boundary",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_CALENDAR_CANDIDATE_DIGEST in markdown
    assert EXPECTED_REVIEW_DIGEST in markdown
    assert EXPECTED_SCHEDULE_DIGEST in markdown
    assert "No provider requests were made." in markdown
    assert "No acquisition bars are generated or frozen." in markdown
    assert "No canonical or registry eligibility is approved." in markdown
    assert "Predictive usefulness and profitability remain not accepted." in markdown


def test_write_frozen_artifact_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = ceremony.write_exchange_calendar_frozen_v1(tmp_path, operator_attestation=_attestation())
    path = Path(result["path"])

    assert result["artifact_kind"] == "EXCHANGE_CALENDAR_FROZEN"
    assert result["freeze_status"] == "EXCHANGE_CALENDAR_FROZEN"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["exchange_calendar_frozen_semantic_digest"] == result["exchange_calendar_frozen_semantic_digest"]
    assert result["frozen_payload_digest"] == ceremony.sha256_bytes(path.read_bytes())
    with pytest.raises(ceremony.ExchangeCalendarOperatorFreezeError, match="already exists"):
        ceremony.write_exchange_calendar_frozen_v1(tmp_path, operator_attestation=_attestation())


def test_source_assurance_freeze_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "exchange_calendar_operator_freeze_service.py"
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
    assert {"send", "post", "put", "delete", "request"}.isdisjoint(called_attrs)
    assert "EXCHANGE_CALENDAR_FROZEN" in source
    assert "APPROVE_EXCHANGE_CALENDAR_FREEZE" in source
    assert "provider_requests_made" in source
    assert "strategy_runtime_migration" in source


def test_service_exports_freeze_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_EXCHANGE_CALENDAR_FROZEN == "EXCHANGE_CALENDAR_FROZEN"
    assert services.EXCHANGE_CALENDAR_FROZEN == "EXCHANGE_CALENDAR_FROZEN"
    assert services.OPERATOR_DECISION_APPROVE_EXCHANGE_CALENDAR_FREEZE == "APPROVE_EXCHANGE_CALENDAR_FREEZE"
    assert (
        services.REQUIRED_EXCHANGE_CALENDAR_OPERATOR_ATTESTATION_PHRASE
        == ceremony.REQUIRED_EXCHANGE_CALENDAR_OPERATOR_ATTESTATION_PHRASE
    )
    assert services.build_exchange_calendar_operator_attestation_v1 is ceremony.build_exchange_calendar_operator_attestation_v1
    assert services.build_exchange_calendar_frozen_v1 is ceremony.build_exchange_calendar_frozen_v1
    assert services.validate_exchange_calendar_frozen_v1 is ceremony.validate_exchange_calendar_frozen_v1
    assert services.write_exchange_calendar_frozen_v1 is ceremony.write_exchange_calendar_frozen_v1
    assert services.build_exchange_calendar_frozen_markdown_v1 is ceremony.build_exchange_calendar_frozen_markdown_v1
    assert services.exchange_calendar_frozen_semantic_digest is ceremony.exchange_calendar_frozen_semantic_digest
