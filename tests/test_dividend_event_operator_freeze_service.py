from __future__ import annotations

import ast
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

from marketflow.services import dividend_event_operator_freeze_service as ceremony
from marketflow.services import dividend_event_operator_review_service as review


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REVIEW_DIGEST = "5cfa4b8f86658b84df932afbf8278d431f18a1082014b3df3ad8c15af2d55742"
EXPECTED_LIVE_CANDIDATE_DIGEST = "19a6275675c14e4ab06c9785828c60bd6a27274507fcddc60dced2ce82662d50"
EXPECTED_RAW_DIGEST = "3b60a63bf0103c1f6b735efd6b086626605c7e717f45d0299965e8988dee396f"
EXPECTED_TIMELINE_DIGEST = "e5d13b1e203b3106855571299f147d0221d92ebcbed019e4b50e6f8e908c0659"
EXPECTED_RECEIPT_DIGEST = "e8bb85d0ceefbe5f1bad411e333142e7957cca09572d0f7be64612eba4bef9e5"
EXPECTED_IDENTITY_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_CALENDAR_DIGEST = "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
EXPECTED_SCHEDULE_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_SPLIT_FREEZE_DIGEST = "9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae"
EXPECTED_SCAFFOLD_DIGEST = "9f50358696a79496bc14f7c526553072f3026b5df28c1d94e65da4c88791a4c0"
EXPECTED_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
EXPECTED_IMPLICATION = "ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY"
TEST_TIMESTAMP = "2026-08-06T00:00:00Z"


def _attestation(**overrides: object) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": TEST_TIMESTAMP,
        "operator_attestation_phrase": ceremony.REQUIRED_DIVIDEND_EVENT_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_dividend_review_package_digest": EXPECTED_REVIEW_DIGEST,
        "operator_confirms_live_dividend_candidate_digest": EXPECTED_LIVE_CANDIDATE_DIGEST,
        "operator_confirms_raw_response_digest": EXPECTED_RAW_DIGEST,
        "operator_confirms_timeline_digest": EXPECTED_TIMELINE_DIGEST,
        "operator_confirms_receipt_digest": EXPECTED_RECEIPT_DIGEST,
        "operator_confirms_identity_frozen_digest": EXPECTED_IDENTITY_DIGEST,
        "operator_confirms_calendar_frozen_digest": EXPECTED_CALENDAR_DIGEST,
        "operator_confirms_schedule_digest": EXPECTED_SCHEDULE_DIGEST,
        "operator_confirms_split_event_frozen_digest": EXPECTED_SPLIT_FREEZE_DIGEST,
        "operator_confirms_in_range_dividend_count": 16,
        "operator_confirms_in_range_dividend_implication": True,
        "operator_confirms_no_provider_requests_in_freeze": True,
        "operator_confirms_no_canonical_approval": True,
        "operator_confirms_no_registry_approval": True,
        "operator_confirms_no_acquisition_generation_freeze": True,
        "operator_confirms_no_strategy_runtime_migration": True,
    }
    values.update(overrides)
    return ceremony.build_dividend_event_operator_attestation_v1(**values)


@lru_cache(maxsize=1)
def _cached_frozen() -> dict:
    return ceremony.build_dividend_event_audit_frozen_v1(operator_attestation=_attestation())


def _frozen(**overrides: object) -> dict:
    if not overrides:
        return deepcopy(_cached_frozen())
    values = {"operator_attestation": _attestation()}
    values.update(overrides)
    return ceremony.build_dividend_event_audit_frozen_v1(**values)


def _recompute_digest(frozen: dict) -> None:
    frozen["dividend_event_audit_frozen_semantic_digest"] = ceremony.dividend_event_audit_frozen_semantic_digest(frozen)


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == "APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE"
    assert attestation["operator_attestation_phrase"] == ceremony.REQUIRED_DIVIDEND_EVENT_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_attestation_timestamp_utc"] == TEST_TIMESTAMP
    assert attestation["operator_attestation_version"] == "dividend_event_operator_attestation_v1"
    assert attestation["operator_confirms_dividend_review_package_digest"] == EXPECTED_REVIEW_DIGEST
    assert attestation["operator_confirms_live_dividend_candidate_digest"] == EXPECTED_LIVE_CANDIDATE_DIGEST
    assert attestation["operator_confirms_raw_response_digest"] == EXPECTED_RAW_DIGEST
    assert attestation["operator_confirms_timeline_digest"] == EXPECTED_TIMELINE_DIGEST
    assert attestation["operator_confirms_receipt_digest"] == EXPECTED_RECEIPT_DIGEST
    assert attestation["operator_confirms_identity_frozen_digest"] == EXPECTED_IDENTITY_DIGEST
    assert attestation["operator_confirms_calendar_frozen_digest"] == EXPECTED_CALENDAR_DIGEST
    assert attestation["operator_confirms_schedule_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert attestation["operator_confirms_split_event_frozen_digest"] == EXPECTED_SPLIT_FREEZE_DIGEST
    assert attestation["operator_confirms_in_range_dividend_count"] == 16
    assert attestation["operator_confirms_in_range_dividend_implication"] is True
    for field in ceremony.OPERATOR_BOUNDARY_CONFIRMATION_FIELDS:
        assert attestation[field] is True


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch):
    calls: list[str] = []
    source_review = review.build_dividend_event_audit_candidate_review_package_v1()

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(review, "build_dividend_event_audit_candidate_review_package_v1", fail_provider_call)

    frozen = ceremony.build_dividend_event_audit_frozen_v1(
        dividend_review_package=source_review,
        operator_attestation=_attestation(),
    )
    receipt = ceremony.validate_dividend_event_audit_frozen_v1(frozen)

    assert calls == []
    assert frozen["created_offline"] is True
    assert frozen["provider_requests_made_in_freeze"] is False
    assert receipt["provider_requests_made_in_freeze"] is False


def test_artifact_kind_status_and_dividend_freeze_state():
    frozen = _frozen()

    assert frozen["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert frozen["schema_version"] == "dividend_event_audit_operator_freeze_v1"
    assert frozen["freeze_status"] == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert frozen["identity_segment_frozen"] is True
    assert frozen["calendar_operator_frozen"] is True
    assert frozen["split_event_audit_frozen"] is True
    assert frozen["dividend_event_audit_frozen"] is True
    assert frozen["authority_boundary"]["dividend_event_audit_frozen"] is True


def test_source_review_and_live_evidence_digests_are_bound():
    frozen = _frozen()

    assert frozen["source_dividend_review_package_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert frozen["source_dividend_review_status"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert frozen["source_dividend_review_package_semantic_digest"] == EXPECTED_REVIEW_DIGEST
    assert frozen["source_dividend_review_checklist_total"] == 39
    assert frozen["source_dividend_review_checklist_passed"] == 39
    assert frozen["source_dividend_review_checklist_failed"] == 0
    assert frozen["source_dividend_review_blocker_count"] == 0
    assert frozen["source_live_dividend_candidate_digest"] == EXPECTED_LIVE_CANDIDATE_DIGEST
    assert frozen["source_live_raw_response_digest"] == EXPECTED_RAW_DIGEST
    assert frozen["source_live_timeline_digest"] == EXPECTED_TIMELINE_DIGEST
    assert frozen["source_live_receipt_digest"] == EXPECTED_RECEIPT_DIGEST


def test_live_provider_status_counts_and_audit_status_are_frozen():
    frozen = _frozen()

    assert frozen["source_live_provider_request_mode"] == "LIVE_PROVIDER_REQUEST"
    assert frozen["source_live_provider_response_status"] == "OK"
    assert frozen["source_live_raw_row_count"] == 16
    assert frozen["event_counts"] == {
        "dividend_event_count_total": 16,
        "dividend_event_count_pre_range": 0,
        "dividend_event_count_in_range": 16,
        "dividend_event_count_post_range": 0,
        "dividend_event_count_unknown": 0,
    }
    assert frozen["dividend_event_count_total"] == 16
    assert frozen["dividend_event_count_pre_range"] == 0
    assert frozen["dividend_event_count_in_range"] == 16
    assert frozen["dividend_event_count_post_range"] == 0
    assert frozen["dividend_event_count_unknown"] == 0
    assert frozen["source_live_audit_status"] == "DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND"


def test_in_range_dividend_implication_is_frozen_without_acquisition_approval():
    frozen = _frozen()

    assert frozen["in_range_dividends_found"] is True
    assert frozen["in_range_dividend_count"] == 16
    assert frozen["in_range_dividend_implication"] == EXPECTED_IMPLICATION
    assert frozen["acquisition_generation_freeze"] is False
    assert frozen["canonical_eligibility"] is False
    assert frozen["registry_eligibility"] is False


def test_authority_segment_and_contract_bindings_are_preserved():
    frozen = _frozen()
    segment = frozen["identity_segment"]

    assert segment["ticker"] == "AAPL"
    assert segment["composite_figi"] == "BBG000B9XRY4"
    assert segment["share_class_figi"] == "BBG001S5N8V8"
    assert segment["primary_mic"] == "XNAS"
    assert segment["security_type"] == "CS"
    assert segment["segment_start"] == "2022-01-01"
    assert segment["segment_end"] == "2025-12-31"
    assert frozen["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_DIGEST
    assert frozen["exchange_calendar_frozen_digest"] == EXPECTED_CALENDAR_DIGEST
    assert frozen["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert frozen["split_event_audit_frozen_digest"] == EXPECTED_SPLIT_FREEZE_DIGEST
    assert frozen["previous_scaffold_candidate_digest"] == EXPECTED_SCAFFOLD_DIGEST
    assert frozen["acquisition_contract_digest"] == EXPECTED_CONTRACT_DIGEST
    assert frozen["acquisition_contract"]["contract_digest"] == frozen["acquisition_contract_digest"]


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


def test_wrong_operator_attestation_phrase_is_rejected():
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match="operator_attestation_phrase"):
        _frozen(operator_attestation=_attestation(operator_attestation_phrase="wrong phrase"))


def test_wrong_operator_decision_is_rejected():
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match="operator_decision"):
        _frozen(operator_attestation=_attestation(operator_decision="REJECT_DIVIDEND_EVENT_AUDIT_FREEZE"))


@pytest.mark.parametrize(
    ("field", "match"),
    [
        ("operator_confirms_dividend_review_package_digest", "operator_dividend_review_digest"),
        ("operator_confirms_live_dividend_candidate_digest", "operator_live_candidate_digest"),
        ("operator_confirms_raw_response_digest", "operator_raw_digest"),
        ("operator_confirms_timeline_digest", "operator_timeline_digest"),
        ("operator_confirms_receipt_digest", "operator_receipt_digest"),
        ("operator_confirms_identity_frozen_digest", "operator_identity_digest"),
        ("operator_confirms_calendar_frozen_digest", "operator_calendar_digest"),
        ("operator_confirms_schedule_digest", "operator_schedule_digest"),
        ("operator_confirms_split_event_frozen_digest", "operator_split_event_digest"),
    ],
)
def test_wrong_operator_digest_confirmation_is_rejected(field: str, match: str):
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match=match):
        _frozen(operator_attestation=_attestation(**{field: "0" * 64}))


def test_wrong_in_range_dividend_count_confirmation_is_rejected():
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match="operator_confirms_in_range_dividend_count"):
        _frozen(operator_attestation=_attestation(operator_confirms_in_range_dividend_count=15))


def test_missing_in_range_dividend_implication_confirmation_is_rejected():
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match="operator_confirms_in_range_dividend_implication"):
        _frozen(operator_attestation=_attestation(operator_confirms_in_range_dividend_implication=False))


def test_missing_attestation_is_rejected():
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match="operator_attestation"):
        ceremony.build_dividend_event_audit_frozen_v1(operator_attestation=None)


@pytest.mark.parametrize("field", ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"))
def test_empty_attestation_identity_fields_are_rejected(field: str):
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match=field):
        _frozen(operator_attestation=_attestation(**{field: "  "}))


@pytest.mark.parametrize("field", ceremony.OPERATOR_BOUNDARY_CONFIRMATION_FIELDS)
def test_any_false_operator_boundary_confirmation_is_rejected(field: str):
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match=field):
        _frozen(operator_attestation=_attestation(**{field: False}))


def test_review_package_with_blocker_count_is_rejected():
    package = review.build_dividend_event_audit_candidate_review_package_v1()
    package["review_summary"]["blocker_count"] = 1
    package["dividend_event_review_package_semantic_digest"] = review.dividend_event_review_package_semantic_digest(package)

    with pytest.raises(ceremony.DividendEventOperatorFreezeError):
        _frozen(dividend_review_package=package)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("source_dividend_review_package_semantic_digest",), "0" * 64),
        (("source_dividend_review_status",), "NOT_READY"),
        (("source_dividend_review_blocker_count",), 1),
        (("source_live_dividend_candidate_digest",), "1" * 64),
        (("source_live_raw_response_digest",), "2" * 64),
        (("source_live_timeline_digest",), "3" * 64),
        (("source_live_receipt_digest",), "4" * 64),
        (("source_live_provider_request_mode",), "PROVIDER_RESPONSE_INJECTION"),
        (("source_live_provider_response_status",), "ERROR"),
        (("source_live_raw_row_count",), 15),
        (("source_live_audit_status",), "DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND"),
        (("event_counts", "dividend_event_count_total"), 15),
        (("event_counts", "dividend_event_count_pre_range"), 1),
        (("event_counts", "dividend_event_count_in_range"), 15),
        (("event_counts", "dividend_event_count_post_range"), 1),
        (("event_counts", "dividend_event_count_unknown"), 1),
        (("dividend_event_count_total",), 15),
        (("dividend_event_count_in_range",), 15),
        (("in_range_dividends_found",), False),
        (("in_range_dividend_count",), 15),
        (("in_range_dividend_implication",), "IGNORE_DIVIDENDS"),
        (("dividend_event_audit_frozen",), False),
        (("canonical_eligibility",), True),
        (("registry_eligibility",), True),
        (("acquisition_generation_freeze",), True),
        (("strategy_runtime_migration",), True),
        (("automatic_stitching",), True),
        (("provider_requests_made_in_freeze",), True),
        (("predictive_usefulness",), "accepted"),
        (("profitability",), "accepted"),
        (("identity_segment", "composite_figi"), "BBG000B9XRZ5"),
        (("identity_segment", "security_type"), "ETF"),
        (("identity_segment", "segment_start"), "2022-01-02"),
        (("identity_segment", "segment_end"), "2025-12-30"),
        (("acquisition_contract_digest",), "5" * 64),
        (("identity_segment_frozen_digest",), "6" * 64),
        (("exchange_calendar_frozen_digest",), "7" * 64),
        (("schedule_semantic_digest",), "8" * 64),
        (("split_event_audit_frozen_digest",), "9" * 64),
    ],
)
def test_validator_rejects_tampered_frozen_artifact_fields(path: tuple[str, ...], value: object):
    frozen = _frozen()
    target = frozen
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    if path[0] in {
        "dividend_event_audit_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
        "automatic_stitching",
        "predictive_usefulness",
        "profitability",
    }:
        frozen["authority_boundary"][path[0]] = value
    _recompute_digest(frozen)

    with pytest.raises(ceremony.DividendEventOperatorFreezeError):
        ceremony.validate_dividend_event_audit_frozen_v1(frozen)


def test_validator_rejects_changed_contract_body_digest():
    frozen = _frozen()
    frozen["acquisition_contract"]["contract_digest"] = "9" * 64
    _recompute_digest(frozen)

    with pytest.raises(ceremony.DividendEventOperatorFreezeError):
        ceremony.validate_dividend_event_audit_frozen_v1(frozen)


def test_frozen_artifact_digest_is_deterministic_for_same_attestation():
    attestation = _attestation()
    first = ceremony.build_dividend_event_audit_frozen_v1(operator_attestation=attestation)
    second = ceremony.build_dividend_event_audit_frozen_v1(operator_attestation=deepcopy(attestation))

    assert first == second
    assert len(first["dividend_event_audit_frozen_semantic_digest"]) == 64
    assert first["dividend_event_audit_frozen_semantic_digest"] == ceremony.dividend_event_audit_frozen_semantic_digest(first)


def test_freeze_checklist_totals_authority_and_review_counts():
    frozen = _frozen()
    summary = frozen["freeze_summary"]

    assert [item["check_id"] for item in frozen["freeze_checklist"]] == ceremony.REQUIRED_FREEZE_CHECK_IDS
    assert summary["total_checks"] == len(ceremony.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["passed_checks"] == len(ceremony.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["dividend_event_audit_freeze_authorized_by_operator"] is True
    assert summary["software_auto_approval"] is False


def test_validator_returns_freeze_receipt_for_valid_artifact():
    receipt = ceremony.validate_dividend_event_audit_frozen_v1(_frozen())

    assert receipt["status"] == "DIVIDEND_EVENT_AUDIT_FROZEN_VALID"
    assert receipt["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert receipt["freeze_status"] == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert receipt["source_dividend_review_package_semantic_digest"] == EXPECTED_REVIEW_DIGEST
    assert receipt["source_live_dividend_candidate_digest"] == EXPECTED_LIVE_CANDIDATE_DIGEST
    assert receipt["source_live_raw_response_digest"] == EXPECTED_RAW_DIGEST
    assert receipt["source_live_timeline_digest"] == EXPECTED_TIMELINE_DIGEST
    assert receipt["source_live_receipt_digest"] == EXPECTED_RECEIPT_DIGEST
    assert receipt["dividend_event_audit_frozen"] is True
    assert receipt["software_auto_approval"] is False
    assert receipt["in_range_dividend_count"] == 16
    assert receipt["in_range_dividend_implication"] == EXPECTED_IMPLICATION


def test_remaining_roadmap_includes_required_future_work_after_dividend_freeze():
    roadmap = _frozen()["remaining_roadmap"]
    rendered = "\n".join(roadmap)

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
    markdown = ceremony.build_dividend_event_audit_frozen_markdown_v1(frozen)

    for heading in (
        "# Dividend-Event Audit Frozen v1",
        "## Frozen Dividend-Event Audit",
        "## Operator Attestation",
        "## Source Dividend Review Package",
        "## Live Provider Evidence",
        "## Frozen Identity / Calendar / Split Bindings",
        "## Event Counts",
        "## In-Range Dividend Interpretation",
        "## Freeze Checklist Summary",
        "## Authority Boundary",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_REVIEW_DIGEST in markdown
    assert EXPECTED_LIVE_CANDIDATE_DIGEST in markdown
    assert EXPECTED_RAW_DIGEST in markdown
    assert EXPECTED_IMPLICATION in markdown
    assert "No provider requests were made during freeze." in markdown
    assert "No canonical or registry eligibility is approved." in markdown
    assert "Predictive usefulness and profitability remain not accepted." in markdown


def test_write_frozen_artifact_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = ceremony.write_dividend_event_audit_frozen_v1(tmp_path, operator_attestation=_attestation())
    path = Path(result["path"])

    assert result["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert result["freeze_status"] == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["dividend_event_audit_frozen_semantic_digest"] == result["dividend_event_audit_frozen_semantic_digest"]
    assert result["frozen_payload_digest"] == ceremony.sha256_bytes(path.read_bytes())
    with pytest.raises(ceremony.DividendEventOperatorFreezeError, match="already exists"):
        ceremony.write_dividend_event_audit_frozen_v1(tmp_path, operator_attestation=_attestation())


def test_source_assurance_freeze_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "dividend_event_operator_freeze_service.py"
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
        "marketflow.services.dividend_event_provider_adapter_service",
        "marketflow.historical_data.massive_transport",
        "marketflow.historical_data.live_month_rth_diagnostic",
        "marketflow.historical_data.monthly_acquisition",
        "marketflow.historical_data.polygon",
    }
    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert {"send", "post", "put", "delete", "request"}.isdisjoint(called_attrs)
    assert "DIVIDEND_EVENT_AUDIT_FROZEN" in source
    assert "APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE" in source
    assert "provider_requests_made_in_freeze" in source
    assert "strategy_runtime_migration" in source
    assert "fetch_massive_dividend_events_v1" not in source


def test_service_exports_freeze_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_FROZEN == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert services.DIVIDEND_EVENT_AUDIT_FROZEN == "DIVIDEND_EVENT_AUDIT_FROZEN"
    assert services.OPERATOR_DECISION_APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE == "APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE"
    assert services.REQUIRED_DIVIDEND_EVENT_OPERATOR_ATTESTATION_PHRASE == ceremony.REQUIRED_DIVIDEND_EVENT_OPERATOR_ATTESTATION_PHRASE
    assert services.build_dividend_event_operator_attestation_v1 is ceremony.build_dividend_event_operator_attestation_v1
    assert services.build_dividend_event_audit_frozen_v1 is ceremony.build_dividend_event_audit_frozen_v1
    assert services.validate_dividend_event_audit_frozen_v1 is ceremony.validate_dividend_event_audit_frozen_v1
    assert services.write_dividend_event_audit_frozen_v1 is ceremony.write_dividend_event_audit_frozen_v1
    assert services.build_dividend_event_audit_frozen_markdown_v1 is ceremony.build_dividend_event_audit_frozen_markdown_v1
    assert services.dividend_event_audit_frozen_semantic_digest is ceremony.dividend_event_audit_frozen_semantic_digest
