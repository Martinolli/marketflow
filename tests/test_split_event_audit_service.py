from __future__ import annotations

import ast
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

from marketflow.services import split_event_audit_service as split


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDENTITY_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_CALENDAR_FROZEN_DIGEST = "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
EXPECTED_SCHEDULE_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


@lru_cache(maxsize=1)
def _cached_candidate() -> dict:
    return split.build_split_event_audit_candidate_v1()


def _candidate() -> dict:
    return deepcopy(_cached_candidate())


def _recompute_digest(candidate: dict) -> None:
    candidate["split_event_audit_candidate_semantic_digest"] = split.split_event_audit_candidate_semantic_digest(candidate)


def test_candidate_scaffold_builds_offline_with_no_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(split, "canonical_json_bytes", fail_provider_call)

    candidate = split.build_split_event_audit_candidate_v1()
    receipt = split.validate_split_event_audit_candidate_v1(candidate)

    assert calls == []
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_artifact_kind_is_split_event_audit_candidate():
    assert _candidate()["artifact_kind"] == "SPLIT_EVENT_AUDIT_CANDIDATE"


def test_status_requires_provider_evidence():
    assert _candidate()["candidate_status"] == "SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"


def test_candidate_binds_identity_frozen_digest():
    candidate = _candidate()

    assert candidate["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert candidate["authority_bindings"]["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST


def test_candidate_binds_calendar_frozen_digest():
    candidate = _candidate()

    assert candidate["exchange_calendar_frozen_digest"] == EXPECTED_CALENDAR_FROZEN_DIGEST
    assert candidate["authority_bindings"]["exchange_calendar_frozen_digest"] == EXPECTED_CALENDAR_FROZEN_DIGEST


def test_candidate_binds_schedule_digest():
    candidate = _candidate()

    assert candidate["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert candidate["authority_bindings"]["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST


def test_candidate_binds_contract_digest():
    candidate = _candidate()

    assert candidate["acquisition_contract_digest"] == EXPECTED_CONTRACT_DIGEST
    assert candidate["authority_bindings"]["acquisition_contract_digest"] == EXPECTED_CONTRACT_DIGEST
    assert candidate["acquisition_contract"]["contract_digest"] == EXPECTED_CONTRACT_DIGEST


def test_candidate_does_not_populate_event_counts():
    outline = _candidate()["split_event_audit_outline"]

    assert outline["split_event_count_total"] is None
    assert outline["split_event_count_pre_range"] is None
    assert outline["split_event_count_in_range"] is None
    assert outline["split_event_count_post_range"] is None
    assert outline["split_events"] == []
    assert outline["audit_status"] is None


def test_candidate_does_not_bind_raw_response_artifact_ids():
    status = _candidate()["source_evidence_status"]

    assert status["provider_endpoint"] is None
    assert status["provider_query_identifier"] is None
    assert status["raw_response_artifact_id"] is None
    assert status["raw_response_semantic_digest"] is None
    assert status["event_timeline_artifact_id"] is None
    assert status["event_timeline_semantic_digest"] is None
    assert status["audit_receipt_artifact_id"] is None


def test_provider_requests_made_is_false():
    assert _candidate()["provider_requests_made"] is False


def test_provider_evidence_required_is_true():
    assert _candidate()["source_evidence_status"]["provider_evidence_required"] is True


def test_provider_evidence_status_is_not_bound():
    assert _candidate()["source_evidence_status"]["provider_evidence_status"] == "NOT_BOUND"


def test_split_event_audit_complete_is_false():
    assert _candidate()["split_event_audit_complete"] is False


def test_split_event_audit_frozen_is_false():
    candidate = _candidate()

    assert candidate["split_event_audit_frozen"] is False
    assert candidate["authority_boundary"]["split_event_audit_frozen"] is False


def test_calendar_and_identity_remain_frozen():
    candidate = _candidate()

    assert candidate["identity_segment_frozen"] is True
    assert candidate["calendar_operator_frozen"] is True
    assert candidate["authority_boundary"]["identity_segment_frozen"] is True
    assert candidate["authority_boundary"]["calendar_operator_frozen"] is True


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
    boundary = candidate["authority_boundary"]

    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"
    assert boundary["predictive_usefulness"] == "not accepted"
    assert boundary["profitability"] == "not accepted"


def test_candidate_digest_is_deterministic():
    first = split.build_split_event_audit_candidate_v1()
    second = split.build_split_event_audit_candidate_v1()

    assert first == second
    assert len(first["split_event_audit_candidate_semantic_digest"]) == 64
    assert first["split_event_audit_candidate_semantic_digest"] == split.split_event_audit_candidate_semantic_digest(first)


def test_validator_rejects_provider_requests_made_true():
    candidate = _candidate()
    candidate["provider_requests_made"] = True
    candidate["guardrails"]["provider_requests_made"] = True
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError, match="provider_requests_made"):
        split.validate_split_event_audit_candidate_v1(candidate)


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
def test_validator_rejects_populated_provider_evidence_without_bound_flag(field: str):
    candidate = _candidate()
    candidate["source_evidence_status"][field] = "unexpected-provider-evidence"
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError):
        split.validate_split_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "split_event_count_total",
        "split_event_count_pre_range",
        "split_event_count_in_range",
        "split_event_count_post_range",
    ],
)
def test_validator_rejects_event_counts_populated_without_provider_evidence(field: str):
    candidate = _candidate()
    candidate["split_event_audit_outline"][field] = 0
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_split_events_populated_without_provider_evidence():
    candidate = _candidate()
    candidate["split_event_audit_outline"]["split_events"] = [{"execution_date": "2022-01-01"}]
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_split_event_audit_frozen_true():
    candidate = _candidate()
    candidate["split_event_audit_frozen"] = True
    candidate["authority_boundary"]["split_event_audit_frozen"] = True
    candidate["guardrails"]["split_event_audit_frozen"] = True
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError, match="split_event_audit_frozen"):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_dividend_event_audit_frozen_true():
    candidate = _candidate()
    candidate["authority_boundary"]["dividend_event_audit_frozen"] = True
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_canonical_eligibility_true():
    candidate = _candidate()
    candidate["canonical_eligibility"] = True
    candidate["authority_boundary"]["canonical_eligibility"] = True
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError, match="canonical_eligibility"):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_wrong_identity_frozen_digest():
    candidate = _candidate()
    candidate["identity_segment_frozen_digest"] = "0" * 64
    candidate["authority_bindings"]["identity_segment_frozen_digest"] = "0" * 64
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError, match="identity_segment_frozen_digest"):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_wrong_calendar_frozen_digest():
    candidate = _candidate()
    candidate["exchange_calendar_frozen_digest"] = "1" * 64
    candidate["authority_bindings"]["exchange_calendar_frozen_digest"] = "1" * 64
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError, match="exchange_calendar_frozen_digest"):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_wrong_contract_digest():
    candidate = _candidate()
    candidate["acquisition_contract_digest"] = "2" * 64
    candidate["authority_bindings"]["acquisition_contract_digest"] = "2" * 64
    candidate["acquisition_contract"]["contract_digest"] = "2" * 64
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError, match="acquisition_contract_digest"):
        split.validate_split_event_audit_candidate_v1(candidate)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("composite_figi", "BBG000B9XRZ5"),
        ("share_class_figi", "BBG001S5N8V9"),
        ("primary_mic", "XNYS"),
        ("security_type", "ETF"),
        ("segment_start", "2022-01-02"),
        ("segment_end", "2025-12-30"),
    ],
)
def test_validator_rejects_wrong_figi_date_mic_or_security_type(field: str, value: str):
    candidate = _candidate()
    candidate["identity_segment"][field] = value
    _recompute_digest(candidate)

    with pytest.raises(split.SplitEventAuditError, match="identity_segment"):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("split_event_audit_candidate_semantic_digest")

    with pytest.raises(split.SplitEventAuditError, match="split_event_audit_candidate_semantic_digest"):
        split.validate_split_event_audit_candidate_v1(candidate)


def test_checklist_contains_required_check_ids():
    candidate = _candidate()
    summary = candidate["scaffold_summary"]

    assert [item["check_id"] for item in candidate["scaffold_checklist"]] == split.REQUIRED_CHECK_IDS
    assert summary["total_checks"] == len(split.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(split.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_provider_evidence_collection"] is True
    assert summary["split_event_audit_complete"] is False
    assert summary["split_event_audit_frozen"] is False
    assert summary["software_auto_approval"] is False


def test_writer_writes_json_and_does_not_freeze(tmp_path: Path):
    result = split.write_split_event_audit_candidate_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "SPLIT_EVENT_AUDIT_CANDIDATE"
    assert result["candidate_status"] == "SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["split_event_audit_frozen"] is False
    assert payload["split_events_provider_evidence_bound"] is False
    assert payload["split_event_audit_candidate_semantic_digest"] == result["split_event_audit_candidate_semantic_digest"]
    assert result["split_event_audit_candidate_payload_digest"] == split.sha256_bytes(path.read_bytes())
    with pytest.raises(split.SplitEventAuditError, match="already exists"):
        split.write_split_event_audit_candidate_v1(tmp_path)


def test_markdown_includes_required_sections_and_guardrails():
    markdown = split.build_split_event_audit_candidate_markdown_v1(_candidate())

    for heading in (
        "# Split-Event Audit Candidate v1",
        "## Scaffold Candidate",
        "## Frozen Authority Bindings",
        "## Provider Evidence",
        "## Scaffold Checklist Summary",
        "## Authority Boundary",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_IDENTITY_FROZEN_DIGEST in markdown
    assert EXPECTED_CALENDAR_FROZEN_DIGEST in markdown
    assert EXPECTED_SCHEDULE_DIGEST in markdown
    assert "No provider requests were made." in markdown
    assert "No split-event provider evidence is bound." in markdown
    assert "No split audit completion or freeze is claimed." in markdown


def test_remaining_roadmap_names_future_provider_backed_chain():
    roadmap = _candidate()["remaining_roadmap"]

    assert roadmap == [
        "Split-event provider evidence collection.",
        "Split-event audit candidate with bound provider evidence.",
        "Split-event operator review package.",
        "Split-event operator freeze ceremony.",
        "Dividend-event audit chain.",
    ]
    assert _candidate()["next_required_task"] == "SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION"


def test_source_assurance_service_has_no_provider_strategy_runtime_or_broker_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "split_event_audit_service.py"
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
    assert "SPLIT_EVENT_AUDIT_CANDIDATE" in source
    assert "SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE" in source
    assert "provider_requests_made" in source
    assert "strategy_runtime_migration" in source


def test_service_exports_split_event_candidate_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE == "SPLIT_EVENT_AUDIT_CANDIDATE"
    assert services.SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE == "SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
    assert services.build_split_event_audit_candidate_v1 is split.build_split_event_audit_candidate_v1
    assert services.validate_split_event_audit_candidate_v1 is split.validate_split_event_audit_candidate_v1
    assert services.write_split_event_audit_candidate_v1 is split.write_split_event_audit_candidate_v1
    assert services.build_split_event_audit_candidate_markdown_v1 is split.build_split_event_audit_candidate_markdown_v1
    assert services.split_event_audit_candidate_semantic_digest is split.split_event_audit_candidate_semantic_digest
