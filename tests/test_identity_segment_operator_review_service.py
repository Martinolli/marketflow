from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from marketflow.services import identity_segment_freeze_service as freeze
from marketflow.services import identity_segment_operator_review_service as review


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANDIDATE_DIGEST = "263902ddc149728d095a4f8bc941c92a82c2d4360e0a038d231e0eac6c70dc57"


def _package(candidate: dict | None = None) -> dict:
    return review.build_identity_segment_candidate_review_package_v1(candidate)


def _validated(package: dict) -> dict:
    return review.validate_identity_segment_candidate_review_package_v1(package)


def _recompute_digest(package: dict) -> None:
    package["review_package_semantic_digest"] = review.review_package_semantic_digest(package)


def test_review_package_builds_offline_without_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(freeze.ident, "TickerOverviewTransport", fail_provider_call)
    monkeypatch.setattr(freeze.tkev, "TickerEventsTransport", fail_provider_call)
    monkeypatch.setattr(freeze.tkev, "validate_accepted_source_identity_evidence", fail_provider_call)

    package = _package()
    receipt = _validated(package)

    assert calls == []
    assert package["created_offline"] is True
    assert package["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_review_package_kind_status_candidate_digest_and_no_operator_decision():
    package = _package()

    assert package["artifact_kind"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE"
    assert package["schema_version"] == "identity_segment_candidate_review_v1"
    assert package["review_status"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert package["operator_decision_required"] is True
    assert package["operator_decision"] is None
    assert package["identity_segment_frozen"] is False
    assert package["automatic_stitching"] is False
    assert package["reviewed_candidate_kind"] == "IDENTITY_SEGMENT_CANDIDATE"
    assert package["reviewed_candidate_status"] == "IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW"
    assert package["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert "IDENTITY_SEGMENT_FROZEN" not in {
        package["artifact_kind"],
        package["review_status"],
        package["reviewed_candidate_kind"],
        package["reviewed_candidate_status"],
    }


def test_review_checklist_contains_required_ids_and_all_pass_for_accepted_candidate():
    package = _package()
    check_ids = [item["check_id"] for item in package["review_checklist"]]

    assert check_ids == review.REQUIRED_CHECK_IDS
    assert all(item["status"] == "PASS" for item in package["review_checklist"])
    assert {item["severity"] for item in package["review_checklist"]}.issubset({"BLOCKER", "HIGH", "INFO"})


def test_review_summary_counts_and_operator_assessment_boundary():
    package = _package()
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["operator_decision_required_before_freeze"] is True
    assert summary["ready_for_freeze_ceremony"] is False
    assert summary["software_freeze_authorized"] is False


def test_authority_flags_and_freeze_controls_remain_unapproved():
    package = _package()
    boundary = package["candidate_binding"]["authority_boundary"]
    controls = package["operator_freeze_controls"]

    assert package["identity_segment_frozen"] is False
    assert package["provider_requests_made"] is False
    assert package["automatic_stitching"] is False
    assert boundary["identity_segment_frozen"] is False
    assert boundary["calendar_operator_frozen"] is False
    assert boundary["canonical_eligibility"] is False
    assert boundary["registry_eligibility"] is False
    assert boundary["acquisition_generation_freeze"] is False
    assert boundary["strategy_runtime_migration"] is False
    assert boundary["predictive_usefulness"] == "not accepted"
    assert boundary["profitability"] == "not accepted"
    assert controls == {
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
    assert len(first["review_package_semantic_digest"]) == 64
    assert first["review_package_semantic_digest"] == review.review_package_semantic_digest(first)
    assert first["review_package_semantic_digest"] == second["review_package_semantic_digest"]
    assert first["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST


def test_validator_returns_digest_and_check_summary_for_valid_package():
    receipt = _validated(_package())

    assert receipt["status"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert receipt["artifact_kind"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE"
    assert receipt["review_status"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert receipt["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert receipt["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert receipt["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert receipt["failed_checks"] == 0
    assert receipt["blocker_count"] == 0
    assert receipt["identity_segment_frozen"] is False
    assert receipt["software_freeze_authorized"] is False


def test_review_package_write_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = review.write_identity_segment_candidate_review_package_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE"
    assert result["review_status"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["review_package_semantic_digest"] == result["review_package_semantic_digest"]
    assert payload["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert result["review_package_payload_digest"] == review.sha256_bytes(path.read_bytes())
    with pytest.raises(review.IdentitySegmentOperatorReviewError, match="already exists"):
        review.write_identity_segment_candidate_review_package_v1(tmp_path)


def test_remaining_roadmap_includes_operator_freeze_and_calendar_split_dividend_acquisition_steps():
    tasks = _package()["remaining_required_tasks"]
    rendered = "\n".join(tasks)

    assert "Digest-bound operator freeze ceremony." in tasks
    assert "Official/operator-frozen exchange-calendar evidence." in tasks
    assert "Split-event audit." in tasks
    assert "Dividend-event audit." in tasks
    assert "Full 2022-2025 acquisition generation." in tasks
    assert "Acquisition-generation freeze." in tasks
    assert "SWING canonical dataset and registry approval." in tasks
    assert "POSITION_SWING canonical dataset and registry approval." in tasks
    assert "Normal runtime migration." in tasks
    assert "Applicability/research campaign." in tasks
    assert "Predictive and profitability evaluation." in tasks
    assert "operator freeze ceremony" in rendered


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = review.build_identity_segment_candidate_review_markdown_v1(_package())

    for heading in (
        "# Identity Segment Candidate Review Package v1",
        "## Reviewed Candidate",
        "## Segment",
        "## Evidence Bound",
        "## Checklist Summary",
        "## Failed Checks",
        "## Authority Boundary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_CANDIDATE_DIGEST in markdown
    assert "No provider requests were made." in markdown
    assert "No `IDENTITY_SEGMENT_FROZEN` artifact or status is created." in markdown


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("reviewed_candidate_semantic_digest",), "0" * 64),
        (("reviewed_candidate_kind",), "IDENTITY_SEGMENT_FROZEN"),
        (("reviewed_candidate_status",), "IDENTITY_SEGMENT_FROZEN"),
        (("candidate_binding", "segment", "composite_figi"), "BBG000B9XRZ5"),
        (("candidate_binding", "segment", "segment_start"), "2022-01-02"),
        (("candidate_binding", "segment", "segment_end"), "2025-12-30"),
        (("candidate_binding", "ticker_events_evidence_binding", "in_range_events"), 1),
        (("identity_segment_frozen",), True),
        (("provider_requests_made",), True),
        (("automatic_stitching",), True),
        (("candidate_binding", "authority_boundary", "identity_segment_frozen"), True),
        (("candidate_binding", "authority_boundary", "calendar_operator_frozen"), True),
        (("candidate_binding", "authority_boundary", "canonical_eligibility"), True),
        (("candidate_binding", "authority_boundary", "registry_eligibility"), True),
        (("candidate_binding", "authority_boundary", "acquisition_generation_freeze"), True),
        (("candidate_binding", "authority_boundary", "strategy_runtime_migration"), True),
    ],
)
def test_validator_rejects_tampered_package_fields(path: tuple[str, ...], value: object):
    package = _package()
    target = package
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    _recompute_digest(package)

    with pytest.raises(review.IdentitySegmentOperatorReviewError):
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

    with pytest.raises(review.IdentitySegmentOperatorReviewError):
        _validated(package)


def test_builder_records_failed_check_for_modified_candidate_digest():
    candidate = freeze.build_identity_segment_candidate_v1()
    candidate["candidate_semantic_digest"] = "0" * 64

    package = _package(candidate)
    digest_check = next(item for item in package["review_checklist"] if item["check_id"] == "candidate_digest_matches_expected")

    assert digest_check["status"] == "FAIL"
    assert package["review_summary"]["failed_checks"] == 1
    with pytest.raises(review.IdentitySegmentOperatorReviewError, match="reviewed_candidate_semantic_digest"):
        _validated(package)


def test_builder_records_failed_check_for_modified_composite_figi():
    candidate = freeze.build_identity_segment_candidate_v1()
    candidate["segment"]["composite_figi"] = "BBG000B9XRZ5"
    candidate["candidate_semantic_digest"] = freeze.candidate_semantic_digest(candidate)

    package = _package(candidate)
    figi_check = next(item for item in package["review_checklist"] if item["check_id"] == "segment_composite_figi_matches")
    digest_check = next(item for item in package["review_checklist"] if item["check_id"] == "candidate_digest_matches_expected")

    assert figi_check["status"] == "FAIL"
    assert digest_check["status"] == "FAIL"
    assert package["review_summary"]["failed_checks"] == 2
    with pytest.raises(review.IdentitySegmentOperatorReviewError):
        _validated(package)


def test_source_assurance_review_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "identity_segment_operator_review_service.py"
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
    assert "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE" in source
    assert "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY" in source
    assert "IDENTITY_SEGMENT_FROZEN" not in {
        review.ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE,
        review.IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY,
    }


def test_service_exports_review_package_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE"
    assert services.IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert services.build_identity_segment_candidate_review_package_v1 is review.build_identity_segment_candidate_review_package_v1
    assert services.validate_identity_segment_candidate_review_package_v1 is review.validate_identity_segment_candidate_review_package_v1
    assert services.write_identity_segment_candidate_review_package_v1 is review.write_identity_segment_candidate_review_package_v1
    assert services.build_identity_segment_candidate_review_markdown_v1 is review.build_identity_segment_candidate_review_markdown_v1
