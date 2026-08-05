from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from marketflow.services import split_event_audit_service as split
from marketflow.services import split_event_operator_review_service as review


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANDIDATE_DIGEST = "92c0a4b4350be4731501fae3300f528bf5f42e5140f01e587ff9c87014c1f66b"
EXPECTED_RAW_DIGEST = "e8db3f18ca3b441a4ae6436d22f48a5481fe5ab0554c092b7cba4010178974bf"
EXPECTED_TIMELINE_DIGEST = "e73556f686e19eef149a95141718bb6c5ab2f53f4df9e5e3f9520f7c050c5076"
EXPECTED_RECEIPT_DIGEST = "dd09dd19fe091816310ec4896ba1d63579f5e794d2efc4de7a897e9c5b117d91"


def _package(candidate: dict | None = None) -> dict:
    return review.build_split_event_audit_candidate_review_package_v1(candidate)


def _validated(package: dict) -> dict:
    return review.validate_split_event_audit_candidate_review_package_v1(package)


def _recompute_digest(package: dict) -> None:
    package["split_event_review_package_semantic_digest"] = review.split_event_review_package_semantic_digest(package)


def test_review_package_builds_offline_without_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(split, "build_split_event_audit_candidate_from_live_provider_v1", fail_provider_call)

    package = _package()
    receipt = _validated(package)

    assert calls == []
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert receipt["provider_requests_made_in_review"] is False


def test_review_package_artifact_kind_status_and_operator_boundary():
    package = _package()

    assert package["artifact_kind"] == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert package["schema_version"] == "split_event_audit_candidate_review_v1"
    assert package["review_status"] == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert package["operator_decision_required"] is True
    assert package["operator_decision"] is None
    assert package["split_event_audit_frozen"] is False
    assert package["automatic_stitching"] is False
    assert package["reviewed_candidate_kind"] == "SPLIT_EVENT_AUDIT_CANDIDATE"
    assert package["reviewed_candidate_status"] == "SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
    assert package["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert "SPLIT_EVENT_AUDIT_FROZEN" not in {
        package["artifact_kind"],
        package["review_status"],
        package["reviewed_candidate_kind"],
        package["reviewed_candidate_status"],
    }


def test_review_package_binds_recorded_live_evidence_digests_mode_status_and_counts():
    package = _package()

    assert package["live_evidence_binding"]["binding_mode"] == "LIVE_PROVIDER_EVIDENCE_STATUS_BINDING"
    assert package["reviewed_raw_response_digest"] == EXPECTED_RAW_DIGEST
    assert package["reviewed_timeline_digest"] == EXPECTED_TIMELINE_DIGEST
    assert package["reviewed_receipt_digest"] == EXPECTED_RECEIPT_DIGEST
    assert package["reviewed_provider_request_mode"] == "LIVE_PROVIDER_REQUEST"
    assert package["reviewed_provider_response_status"] == "OK"
    assert package["reviewed_provider_response_page_count"] == 1
    assert package["reviewed_provider_raw_row_count"] == 0
    assert package["reviewed_audit_status"] == "SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT"
    assert package["event_counts"] == {
        "split_event_count_total": 0,
        "split_event_count_pre_range": 0,
        "split_event_count_in_range": 0,
        "split_event_count_post_range": 0,
        "split_event_count_unknown": 0,
    }


def test_review_checklist_contains_required_ids_and_all_pass_for_accepted_live_evidence():
    package = _package()
    check_ids = [item["check_id"] for item in package["review_checklist"]]

    assert check_ids == review.REQUIRED_CHECK_IDS
    assert all(item["status"] == "PASS" for item in package["review_checklist"])
    assert {item["severity"] for item in package["review_checklist"]}.issubset({"BLOCKER", "HIGH", "INFO"})


def test_review_summary_counts_total_passed_failed_and_blockers():
    package = _package()
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["operator_decision_required_before_freeze"] is True
    assert summary["software_freeze_authorized"] is False


def test_authority_flags_and_freeze_controls_remain_unapproved():
    package = _package()
    boundary = package["authority_boundary"]

    assert package["identity_segment_frozen"] is True
    assert package["calendar_operator_frozen"] is True
    assert package["split_event_audit_frozen"] is False
    assert package["dividend_event_audit_frozen"] is False
    assert package["canonical_eligibility"] is False
    assert package["registry_eligibility"] is False
    assert package["acquisition_generation_freeze"] is False
    assert package["strategy_runtime_migration"] is False
    assert package["automatic_stitching"] is False
    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"
    assert boundary == package["live_evidence_binding"]["authority_boundary"]
    assert package["operator_freeze_controls"] == {
        "operator_approved_by": None,
        "operator_freeze_timestamp": None,
        "operator_freeze_digest": None,
        "operator_signature": None,
        "freeze_status": None,
    }


def test_review_package_digest_is_deterministic_across_repeated_builds():
    first = _package()
    second = _package()

    assert first == second
    assert len(first["split_event_review_package_semantic_digest"]) == 64
    assert first["split_event_review_package_semantic_digest"] == review.split_event_review_package_semantic_digest(first)
    assert first["split_event_review_package_semantic_digest"] == second["split_event_review_package_semantic_digest"]
    assert first["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST


def test_validator_returns_review_receipt_for_valid_package():
    receipt = _validated(_package())

    assert receipt["status"] == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert receipt["artifact_kind"] == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert receipt["review_status"] == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert receipt["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert receipt["reviewed_raw_response_digest"] == EXPECTED_RAW_DIGEST
    assert receipt["reviewed_timeline_digest"] == EXPECTED_TIMELINE_DIGEST
    assert receipt["reviewed_receipt_digest"] == EXPECTED_RECEIPT_DIGEST
    assert receipt["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert receipt["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert receipt["failed_checks"] == 0
    assert receipt["blocker_count"] == 0
    assert receipt["split_event_audit_frozen"] is False
    assert receipt["software_freeze_authorized"] is False


def test_write_review_package_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = review.write_split_event_audit_candidate_review_package_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert result["review_status"] == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["split_event_review_package_semantic_digest"] == result["split_event_review_package_semantic_digest"]
    assert payload["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert result["split_event_review_package_payload_digest"] == review.sha256_bytes(path.read_bytes())
    with pytest.raises(review.SplitEventOperatorReviewError, match="already exists"):
        review.write_split_event_audit_candidate_review_package_v1(tmp_path)


def test_remaining_roadmap_includes_required_future_work():
    tasks = _package()["remaining_required_tasks"]
    rendered = "\n".join(tasks)

    assert "Digest-bound split-event operator freeze ceremony." in tasks
    assert "Dividend-event audit candidate." in tasks
    assert "Dividend-event provider evidence collection." in tasks
    assert "Dividend-event operator review package." in tasks
    assert "Dividend-event operator freeze ceremony." in tasks
    assert "Full 2022-2025 acquisition generation." in tasks
    assert "Acquisition-generation freeze." in tasks
    assert "SWING canonical dataset and registry approval." in tasks
    assert "POSITION_SWING canonical dataset and registry approval." in tasks
    assert "Normal runtime migration." in tasks
    assert "Applicability/research campaign." in tasks
    assert "Predictive and profitability evaluation." in tasks
    assert "split-event operator freeze ceremony" in rendered


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = review.build_split_event_audit_candidate_review_markdown_v1(_package())

    for heading in (
        "# Split-Event Audit Candidate Review Package v1",
        "## Reviewed Split-Event Candidate",
        "## Live Provider Evidence Summary",
        "## Frozen Identity / Calendar Bindings",
        "## Event Counts",
        "## Checklist Summary",
        "## Failed Checks",
        "## Authority Boundary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_CANDIDATE_DIGEST in markdown
    assert EXPECTED_RAW_DIGEST in markdown
    assert "No provider requests were made during review." in markdown
    assert "No `SPLIT_EVENT_AUDIT_FROZEN` artifact or status is created." in markdown


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("reviewed_candidate_semantic_digest",), "0" * 64),
        (("reviewed_raw_response_digest",), "1" * 64),
        (("reviewed_timeline_digest",), "2" * 64),
        (("reviewed_receipt_digest",), "3" * 64),
        (("reviewed_provider_request_mode",), "PROVIDER_RESPONSE_INJECTION"),
        (("reviewed_provider_response_status",), "ERROR"),
        (("reviewed_audit_status",), "SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT"),
        (("event_counts", "split_event_count_in_range"), 1),
        (("live_evidence_binding", "reviewed_candidate_semantic_digest"), "0" * 64),
        (("live_evidence_binding", "reviewed_raw_response_digest"), "1" * 64),
        (("live_evidence_binding", "reviewed_timeline_digest"), "2" * 64),
        (("live_evidence_binding", "reviewed_receipt_digest"), "3" * 64),
        (("live_evidence_binding", "event_counts", "split_event_count_total"), 1),
        (("live_evidence_binding", "event_counts", "split_event_count_in_range"), 1),
        (("live_evidence_binding", "reviewed_provider_response_status"), "ERROR"),
        (("live_evidence_binding", "reviewed_audit_status"), "SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT"),
        (("live_evidence_binding", "identity_segment_frozen_digest"), "4" * 64),
        (("live_evidence_binding", "exchange_calendar_frozen_digest"), "5" * 64),
        (("live_evidence_binding", "schedule_semantic_digest"), "6" * 64),
        (("live_evidence_binding", "previous_scaffold_candidate_digest"), "7" * 64),
        (("live_evidence_binding", "identity_segment", "ticker"), "MSFT"),
        (("live_evidence_binding", "identity_segment", "composite_figi"), "BBG000BPH459"),
        (("live_evidence_binding", "identity_segment", "share_class_figi"), "BBG001S5N8V9"),
        (("live_evidence_binding", "identity_segment", "primary_mic"), "XNYS"),
        (("live_evidence_binding", "identity_segment", "security_type"), "ETF"),
        (("live_evidence_binding", "identity_segment", "segment_start"), "2022-01-02"),
        (("live_evidence_binding", "identity_segment", "segment_end"), "2025-12-30"),
        (("live_evidence_binding", "acquisition_contract", "contract_digest"), "8" * 64),
        (("split_event_audit_frozen",), True),
        (("canonical_eligibility",), True),
        (("registry_eligibility",), True),
        (("acquisition_generation_freeze",), True),
        (("strategy_runtime_migration",), True),
        (("automatic_stitching",), True),
        (("provider_requests_made_in_review",), True),
        (("predictive_usefulness",), "accepted"),
        (("profitability",), "accepted"),
    ],
)
def test_validator_rejects_tampered_review_package_fields(path: tuple[str, ...], value: object):
    package = _package()
    target = package
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    _recompute_digest(package)

    with pytest.raises(review.SplitEventOperatorReviewError):
        _validated(package)


@pytest.mark.parametrize(
    "field",
    [
        "operator_approved_by",
        "operator_freeze_timestamp",
        "operator_freeze_digest",
        "operator_signature",
        "freeze_status",
    ],
)
def test_validator_rejects_populated_freeze_controls(field: str):
    package = _package()
    package["operator_freeze_controls"][field] = "not allowed"
    _recompute_digest(package)

    with pytest.raises(review.SplitEventOperatorReviewError):
        _validated(package)


def test_validator_rejects_split_event_audit_frozen_artifact_or_status():
    package = _package()
    package["review_status"] = "SPLIT_EVENT_AUDIT_FROZEN"
    _recompute_digest(package)

    with pytest.raises(review.SplitEventOperatorReviewError):
        _validated(package)


def test_builder_records_failed_check_for_modified_live_candidate_digest():
    candidate = review._expected_live_evidence_binding()
    candidate["reviewed_candidate_semantic_digest"] = "0" * 64

    package = _package(candidate)
    digest_check = next(item for item in package["review_checklist"] if item["check_id"] == "candidate_digest_matches_recorded_live_evidence")

    assert digest_check["status"] == "FAIL"
    assert package["review_summary"]["failed_checks"] == 1
    with pytest.raises(review.SplitEventOperatorReviewError):
        _validated(package)


def test_builder_records_failed_check_for_modified_in_range_count():
    candidate = review._expected_live_evidence_binding()
    candidate["event_counts"]["split_event_count_in_range"] = 1

    package = _package(candidate)
    count_check = next(item for item in package["review_checklist"] if item["check_id"] == "event_count_in_range_zero")

    assert count_check["status"] == "FAIL"
    assert package["review_summary"]["failed_checks"] == 1
    with pytest.raises(review.SplitEventOperatorReviewError):
        _validated(package)


def test_source_assurance_review_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "split_event_operator_review_service.py"
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
        "marketflow.services.split_event_provider_adapter_service",
        "marketflow.historical_data.massive_transport",
        "marketflow.historical_data.live_month_rth_diagnostic",
        "marketflow.historical_data.monthly_acquisition",
    }
    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert {"send", "post", "put", "delete", "request"}.isdisjoint(called_attrs)
    assert "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE" in source
    assert "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY" in source
    assert "fetch_massive_split_events_v1" not in source


def test_service_exports_split_event_review_package_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert services.SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY == "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert services.build_split_event_audit_candidate_review_package_v1 is review.build_split_event_audit_candidate_review_package_v1
    assert services.validate_split_event_audit_candidate_review_package_v1 is review.validate_split_event_audit_candidate_review_package_v1
    assert services.write_split_event_audit_candidate_review_package_v1 is review.write_split_event_audit_candidate_review_package_v1
    assert services.build_split_event_audit_candidate_review_markdown_v1 is review.build_split_event_audit_candidate_review_markdown_v1
