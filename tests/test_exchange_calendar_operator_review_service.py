from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from marketflow.services import exchange_calendar_evidence_service as calendar
from marketflow.services import exchange_calendar_operator_review_service as review
from marketflow.services import identity_segment_freeze_service as identity_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CALENDAR_CANDIDATE_DIGEST = "867aa02ad9c9c737eda3d8398eda4e4aad3181cd4bc5505600ccf9647b0d60ee"
EXPECTED_SCHEDULE_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_REVIEW_PACKAGE_DIGEST = "5e7e528068cd161e06a7a3cf6b30c40909023f23eb6b64661abb063363a690cb"


def _package(candidate: dict | None = None) -> dict:
    return review.build_exchange_calendar_evidence_candidate_review_package_v1(candidate)


def _validated(package: dict) -> dict:
    return review.validate_exchange_calendar_evidence_candidate_review_package_v1(package)


def _recompute_digest(package: dict) -> None:
    package["calendar_review_package_semantic_digest"] = review.calendar_review_package_semantic_digest(package)


def _candidate_with(path: tuple[str, ...], value: object) -> dict:
    candidate = calendar.build_exchange_calendar_evidence_candidate_v1()
    target = candidate
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    if path != ("calendar_evidence_candidate_semantic_digest",):
        candidate["calendar_evidence_candidate_semantic_digest"] = calendar.calendar_evidence_candidate_semantic_digest(candidate)
    return candidate


def test_review_package_builds_offline_without_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(identity_candidate.ident, "TickerOverviewTransport", fail_provider_call)
    monkeypatch.setattr(identity_candidate.tkev, "TickerEventsTransport", fail_provider_call)
    monkeypatch.setattr(identity_candidate.tkev, "validate_accepted_source_identity_evidence", fail_provider_call)

    package = _package()
    receipt = _validated(package)

    assert calls == []
    assert package["created_offline"] is True
    assert package["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_review_package_kind_status_and_reviewed_digests():
    package = _package()

    assert package["artifact_kind"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE"
    assert package["schema_version"] == "exchange_calendar_evidence_candidate_review_v1"
    assert package["review_status"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY"
    assert package["reviewed_candidate_kind"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE"
    assert package["reviewed_candidate_status"] == "EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
    assert package["reviewed_calendar_candidate_semantic_digest"] == EXPECTED_CALENDAR_CANDIDATE_DIGEST
    assert package["reviewed_schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST


def test_review_checklist_contains_required_ids_and_all_pass_for_accepted_candidate():
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


def test_calendar_operator_frozen_false_and_no_frozen_artifact_status():
    package = _package()

    assert package["calendar_operator_frozen"] is False
    assert package["artifact_kind"] != "EXCHANGE_CALENDAR_FROZEN"
    assert package["review_status"] != "EXCHANGE_CALENDAR_FROZEN"
    assert package["reviewed_candidate_kind"] != "EXCHANGE_CALENDAR_FROZEN"
    assert package["reviewed_candidate_status"] != "EXCHANGE_CALENDAR_FROZEN"
    assert package["candidate_binding"]["guardrails"]["calendar_freeze_created"] is False


def test_operator_decision_and_freeze_controls_remain_unapproved():
    package = _package()

    assert package["operator_decision_required"] is True
    assert package["operator_decision"] is None
    assert package["operator_freeze_controls"] == {
        "operator_approved_by": None,
        "operator_freeze_timestamp": None,
        "operator_freeze_digest": None,
        "operator_signature": None,
        "freeze_status": None,
    }


def test_provider_automatic_canonical_registry_acquisition_and_runtime_flags_remain_false():
    package = _package()
    authority = package["candidate_binding"]["authority_boundary"]

    assert package["provider_requests_made"] is False
    assert package["automatic_stitching"] is False
    assert authority["automatic_stitching"] is False
    assert authority["canonical_eligibility"] is False
    assert authority["registry_eligibility"] is False
    assert authority["acquisition_generation_freeze"] is False
    assert authority["strategy_runtime_migration"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    authority = _package()["candidate_binding"]["authority_boundary"]

    assert authority["predictive_usefulness"] == "not accepted"
    assert authority["profitability"] == "not accepted"


def test_review_package_digest_is_deterministic_across_repeated_builds():
    first = _package()
    second = _package()

    assert first == second
    assert first["calendar_review_package_semantic_digest"] == EXPECTED_REVIEW_PACKAGE_DIGEST
    assert first["calendar_review_package_semantic_digest"] == review.calendar_review_package_semantic_digest(first)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("calendar_evidence_candidate_semantic_digest",), "0" * 64),
        (("schedule_semantic_digest",), "1" * 64),
        (("calendar_binding", "calendar_alias"), "XNAS_DIRECT"),
        (("identity_segment_frozen_digest",), "2" * 64),
        (("identity_segment_binding", "identity_segment_frozen_digest"), "2" * 64),
        (("accepted_monthly_cross_check", "expected_rth_rows"), 519),
        (("calendar_operator_frozen",), True),
        (("authority_boundary", "calendar_operator_frozen"), True),
        (("authority_boundary", "canonical_eligibility"), True),
        (("authority_boundary", "registry_eligibility"), True),
        (("authority_boundary", "acquisition_generation_freeze"), True),
        (("schedule_semantic_digest",), ""),
        (("schedule_coverage", "schedule_semantic_digest"), ""),
        (("authority_boundary", "predictive_usefulness"), "accepted"),
        (("authority_boundary", "profitability"), "accepted"),
    ],
)
def test_validator_rejects_tampered_candidate_review_bindings(path: tuple[str, ...], value: object):
    candidate = _candidate_with(path, value)
    package = _package(candidate)

    with pytest.raises(review.ExchangeCalendarOperatorReviewError):
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

    with pytest.raises(review.ExchangeCalendarOperatorReviewError):
        _validated(package)


def test_validator_rejects_exchange_calendar_frozen_artifact_or_status():
    package = _package()
    package["review_status"] = "EXCHANGE_CALENDAR_FROZEN"
    _recompute_digest(package)

    with pytest.raises(review.ExchangeCalendarOperatorReviewError):
        _validated(package)


def test_builder_records_failed_check_for_modified_calendar_alias():
    candidate = _candidate_with(("calendar_binding", "calendar_alias"), "XNAS_DIRECT")
    package = _package(candidate)
    alias_check = next(item for item in package["review_checklist"] if item["check_id"] == "calendar_alias_matches")

    assert alias_check["status"] == "FAIL"
    assert package["review_summary"]["failed_checks"] >= 1
    with pytest.raises(review.ExchangeCalendarOperatorReviewError):
        _validated(package)


def test_remaining_roadmap_includes_required_future_work():
    tasks = _package()["remaining_required_tasks"]
    rendered = "\n".join(tasks)

    assert "Digest-bound calendar operator freeze ceremony." in tasks
    assert "Split-event audit." in tasks
    assert "Dividend-event audit." in tasks
    assert "Full 2022-2025 acquisition generation." in tasks
    assert "Acquisition-generation freeze." in tasks
    assert "SWING canonical dataset and registry approval." in tasks
    assert "POSITION_SWING canonical dataset and registry approval." in tasks
    assert "Normal runtime migration." in tasks
    assert "Applicability/research campaign." in tasks
    assert "Predictive and profitability evaluation." in tasks
    assert "calendar operator freeze ceremony" in rendered


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = review.build_exchange_calendar_evidence_candidate_review_markdown_v1(_package())

    for heading in (
        "# Exchange Calendar Evidence Candidate Review Package v1",
        "## Reviewed Calendar Candidate",
        "## Frozen Identity Segment Binding",
        "## Calendar Binding",
        "## Schedule Evidence",
        "## 2025-01 Monthly Cross-Check",
        "## Checklist Summary",
        "## Failed Checks",
        "## Authority Boundary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_CALENDAR_CANDIDATE_DIGEST in markdown
    assert EXPECTED_SCHEDULE_DIGEST in markdown
    assert "No provider requests were made." in markdown
    assert "No `EXCHANGE_CALENDAR_FROZEN` artifact or status is created." in markdown


def test_write_review_package_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = review.write_exchange_calendar_evidence_candidate_review_package_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE"
    assert result["review_status"] == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["calendar_review_package_semantic_digest"] == result["calendar_review_package_semantic_digest"]
    assert result["calendar_review_package_payload_digest"] == review.sha256_bytes(path.read_bytes())
    with pytest.raises(review.ExchangeCalendarOperatorReviewError, match="already exists"):
        review.write_exchange_calendar_evidence_candidate_review_package_v1(tmp_path)


def test_source_assurance_review_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "exchange_calendar_operator_review_service.py"
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
    assert "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE" in source
    assert "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY" in source
    assert "EXCHANGE_CALENDAR_FROZEN" in source
    assert "calendar_operator_frozen" in source


def test_service_exports_calendar_review_package_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE"
    assert services.EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY == "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY"
    assert services.build_exchange_calendar_evidence_candidate_review_package_v1 is review.build_exchange_calendar_evidence_candidate_review_package_v1
    assert services.validate_exchange_calendar_evidence_candidate_review_package_v1 is review.validate_exchange_calendar_evidence_candidate_review_package_v1
    assert services.write_exchange_calendar_evidence_candidate_review_package_v1 is review.write_exchange_calendar_evidence_candidate_review_package_v1
    assert services.build_exchange_calendar_evidence_candidate_review_markdown_v1 is review.build_exchange_calendar_evidence_candidate_review_markdown_v1
