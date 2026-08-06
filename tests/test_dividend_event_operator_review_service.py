from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from marketflow.services import dividend_event_audit_service as dividend
from marketflow.services import dividend_event_operator_review_service as review


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANDIDATE_DIGEST = "19a6275675c14e4ab06c9785828c60bd6a27274507fcddc60dced2ce82662d50"
EXPECTED_RAW_DIGEST = "3b60a63bf0103c1f6b735efd6b086626605c7e717f45d0299965e8988dee396f"
EXPECTED_TIMELINE_DIGEST = "e5d13b1e203b3106855571299f147d0221d92ebcbed019e4b50e6f8e908c0659"
EXPECTED_RECEIPT_DIGEST = "e8bb85d0ceefbe5f1bad411e333142e7957cca09572d0f7be64612eba4bef9e5"
EXPECTED_IDENTITY_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_CALENDAR_FROZEN_DIGEST = "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
EXPECTED_SCHEDULE_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_SPLIT_FREEZE_DIGEST = "9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae"
EXPECTED_SCAFFOLD_DIGEST = "9f50358696a79496bc14f7c526553072f3026b5df28c1d94e65da4c88791a4c0"
EXPECTED_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


def _package(candidate: dict | None = None) -> dict:
    return review.build_dividend_event_audit_candidate_review_package_v1(candidate)


def _validated(package: dict) -> dict:
    return review.validate_dividend_event_audit_candidate_review_package_v1(package)


def _recompute_digest(package: dict) -> None:
    package["dividend_event_review_package_semantic_digest"] = review.dividend_event_review_package_semantic_digest(package)


def test_review_package_builds_offline_without_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(dividend, "build_dividend_event_audit_candidate_from_live_provider_v1", fail_provider_call)

    package = _package()
    receipt = _validated(package)

    assert calls == []
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert receipt["provider_requests_made_in_review"] is False


def test_review_package_artifact_kind_status_and_operator_boundary():
    package = _package()

    assert package["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert package["schema_version"] == "dividend_event_audit_candidate_review_v1"
    assert package["review_status"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert package["operator_decision_required"] is True
    assert package["operator_decision"] is None
    assert package["dividend_event_audit_frozen"] is False
    assert package["automatic_stitching"] is False
    assert package["reviewed_candidate_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE"
    assert package["reviewed_candidate_status"] == "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
    assert package["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert "DIVIDEND_EVENT_AUDIT_FROZEN" not in {
        package["artifact_kind"],
        package["review_status"],
        package["reviewed_candidate_kind"],
        package["reviewed_candidate_status"],
    }


def test_review_package_binds_recorded_live_evidence_digests_mode_status_and_counts():
    package = _package()

    assert package["live_evidence_binding"]["binding_mode"] == "LIVE_PROVIDER_EVIDENCE_STATUS_BINDING"
    assert package["live_evidence_binding"]["raw_provider_payload_present"] is False
    assert package["reviewed_raw_response_digest"] == EXPECTED_RAW_DIGEST
    assert package["reviewed_timeline_digest"] == EXPECTED_TIMELINE_DIGEST
    assert package["reviewed_receipt_digest"] == EXPECTED_RECEIPT_DIGEST
    assert package["reviewed_provider_request_mode"] == "LIVE_PROVIDER_REQUEST"
    assert package["reviewed_provider_response_status"] == "OK"
    assert package["reviewed_provider_response_page_count"] == 1
    assert package["reviewed_provider_raw_row_count"] == 16
    assert package["reviewed_audit_status"] == "DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND"
    assert package["event_counts"] == {
        "dividend_event_count_total": 16,
        "dividend_event_count_pre_range": 0,
        "dividend_event_count_in_range": 16,
        "dividend_event_count_post_range": 0,
        "dividend_event_count_unknown": 0,
    }


def test_in_range_dividend_evidence_is_not_a_blocker_and_sets_policy_implication():
    package = _package()

    assert package["in_range_dividends_found"] is True
    assert package["in_range_dividend_count"] == 16
    assert package["in_range_dividend_implication"] == "ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY"
    assert package["review_summary"]["failed_checks"] == 0
    assert package["review_summary"]["blocker_count"] == 0
    assert package["review_summary"]["ready_for_operator_assessment"] is True


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


def test_authority_bindings_segment_contract_and_freeze_controls_remain_unapproved():
    package = _package()
    binding = package["live_evidence_binding"]

    assert binding["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_FROZEN_DIGEST
    assert binding["exchange_calendar_frozen_digest"] == EXPECTED_CALENDAR_FROZEN_DIGEST
    assert binding["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert binding["split_event_audit_frozen_digest"] == EXPECTED_SPLIT_FREEZE_DIGEST
    assert binding["previous_scaffold_candidate_digest"] == EXPECTED_SCAFFOLD_DIGEST
    assert binding["acquisition_contract"]["contract_digest"] == EXPECTED_CONTRACT_DIGEST
    assert binding["identity_segment"] == {
        "ticker": "AAPL",
        "composite_figi": "BBG000B9XRY4",
        "share_class_figi": "BBG001S5N8V8",
        "primary_mic": "XNAS",
        "security_type": "CS",
        "segment_start": "2022-01-01",
        "segment_end": "2025-12-31",
    }
    assert package["operator_freeze_controls"] == {
        "operator_approved_by": None,
        "operator_freeze_timestamp": None,
        "operator_freeze_digest": None,
        "operator_signature": None,
        "freeze_status": None,
    }


def test_authority_flags_remain_limited_to_prior_frozen_authorities():
    package = _package()
    boundary = package["authority_boundary"]

    assert package["identity_segment_frozen"] is True
    assert package["calendar_operator_frozen"] is True
    assert package["split_event_audit_frozen"] is True
    assert package["dividend_event_audit_frozen"] is False
    assert package["canonical_eligibility"] is False
    assert package["registry_eligibility"] is False
    assert package["acquisition_generation_freeze"] is False
    assert package["strategy_runtime_migration"] is False
    assert package["automatic_stitching"] is False
    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"
    assert boundary == package["live_evidence_binding"]["authority_boundary"]


def test_review_package_digest_is_deterministic_across_repeated_builds():
    first = _package()
    second = _package()

    assert first == second
    assert len(first["dividend_event_review_package_semantic_digest"]) == 64
    assert first["dividend_event_review_package_semantic_digest"] == review.dividend_event_review_package_semantic_digest(first)
    assert first["dividend_event_review_package_semantic_digest"] == second["dividend_event_review_package_semantic_digest"]
    assert first["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST


def test_validator_returns_review_receipt_for_valid_package():
    receipt = _validated(_package())

    assert receipt["status"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert receipt["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert receipt["review_status"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert receipt["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert receipt["reviewed_raw_response_digest"] == EXPECTED_RAW_DIGEST
    assert receipt["reviewed_timeline_digest"] == EXPECTED_TIMELINE_DIGEST
    assert receipt["reviewed_receipt_digest"] == EXPECTED_RECEIPT_DIGEST
    assert receipt["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert receipt["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert receipt["failed_checks"] == 0
    assert receipt["blocker_count"] == 0
    assert receipt["dividend_event_audit_frozen"] is False
    assert receipt["software_freeze_authorized"] is False
    assert receipt["in_range_dividend_count"] == 16


def test_write_review_package_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = review.write_dividend_event_audit_candidate_review_package_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert result["review_status"] == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["dividend_event_review_package_semantic_digest"] == result["dividend_event_review_package_semantic_digest"]
    assert payload["reviewed_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert result["dividend_event_review_package_payload_digest"] == review.sha256_bytes(path.read_bytes())
    with pytest.raises(review.DividendEventOperatorReviewError, match="already exists"):
        review.write_dividend_event_audit_candidate_review_package_v1(tmp_path)


def test_remaining_roadmap_matches_required_future_work_order():
    tasks = _package()["remaining_required_tasks"]

    assert tasks == [
        "Digest-bound dividend-event operator freeze ceremony.",
        "Full 2022-2025 acquisition generation.",
        "Acquisition-generation freeze.",
        "SWING canonical dataset and registry approval.",
        "POSITION_SWING canonical dataset and registry approval.",
        "Normal runtime migration.",
        "Applicability/research campaign.",
        "Predictive and profitability evaluation.",
    ]


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = review.build_dividend_event_audit_candidate_review_markdown_v1(_package())

    for heading in (
        "# Dividend-Event Audit Candidate Review Package v1",
        "## Reviewed Dividend-Event Candidate",
        "## Live Provider Evidence Summary",
        "## In-Range Dividend Implication",
        "## Frozen Identity / Calendar / Split Bindings",
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
    assert "No `DIVIDEND_EVENT_AUDIT_FROZEN` artifact or status is created." in markdown


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("reviewed_candidate_semantic_digest",), "0" * 64),
        (("reviewed_raw_response_digest",), "1" * 64),
        (("reviewed_timeline_digest",), "2" * 64),
        (("reviewed_receipt_digest",), "3" * 64),
        (("reviewed_provider_request_mode",), "PROVIDER_RESPONSE_INJECTION"),
        (("reviewed_provider_response_status",), "ERROR"),
        (("reviewed_provider_raw_row_count",), 15),
        (("reviewed_audit_status",), "DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND"),
        (("event_counts", "dividend_event_count_total"), 15),
        (("event_counts", "dividend_event_count_in_range"), 15),
        (("live_evidence_binding", "reviewed_candidate_semantic_digest"), "0" * 64),
        (("live_evidence_binding", "reviewed_raw_response_digest"), "1" * 64),
        (("live_evidence_binding", "reviewed_timeline_digest"), "2" * 64),
        (("live_evidence_binding", "reviewed_receipt_digest"), "3" * 64),
        (("live_evidence_binding", "event_counts", "dividend_event_count_total"), 15),
        (("live_evidence_binding", "event_counts", "dividend_event_count_in_range"), 15),
        (("live_evidence_binding", "reviewed_provider_response_status"), "ERROR"),
        (("live_evidence_binding", "reviewed_audit_status"), "DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND"),
        (("live_evidence_binding", "identity_segment_frozen_digest"), "4" * 64),
        (("live_evidence_binding", "exchange_calendar_frozen_digest"), "5" * 64),
        (("live_evidence_binding", "schedule_semantic_digest"), "6" * 64),
        (("live_evidence_binding", "split_event_audit_frozen_digest"), "7" * 64),
        (("live_evidence_binding", "previous_scaffold_candidate_digest"), "8" * 64),
        (("live_evidence_binding", "identity_segment", "ticker"), "MSFT"),
        (("live_evidence_binding", "identity_segment", "composite_figi"), "BBG000BPH459"),
        (("live_evidence_binding", "identity_segment", "share_class_figi"), "BBG001S5N8V9"),
        (("live_evidence_binding", "identity_segment", "primary_mic"), "XNYS"),
        (("live_evidence_binding", "identity_segment", "security_type"), "ETF"),
        (("live_evidence_binding", "identity_segment", "segment_start"), "2022-01-02"),
        (("live_evidence_binding", "identity_segment", "segment_end"), "2025-12-30"),
        (("live_evidence_binding", "acquisition_contract", "contract_digest"), "9" * 64),
        (("dividend_event_audit_frozen",), True),
        (("canonical_eligibility",), True),
        (("registry_eligibility",), True),
        (("acquisition_generation_freeze",), True),
        (("strategy_runtime_migration",), True),
        (("automatic_stitching",), True),
        (("provider_requests_made_in_review",), True),
        (("predictive_usefulness",), "accepted"),
        (("profitability",), "accepted"),
        (("in_range_dividend_count",), 0),
        (("in_range_dividend_implication",), "IGNORE_DIVIDENDS"),
    ],
)
def test_validator_rejects_tampered_review_package_fields(path: tuple[str, ...], value: object):
    package = _package()
    target = package
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    _recompute_digest(package)

    with pytest.raises(review.DividendEventOperatorReviewError):
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

    with pytest.raises(review.DividendEventOperatorReviewError):
        _validated(package)


def test_validator_rejects_dividend_event_audit_frozen_artifact_or_status():
    package = _package()
    package["review_status"] = "DIVIDEND_EVENT_AUDIT_FROZEN"
    _recompute_digest(package)

    with pytest.raises(review.DividendEventOperatorReviewError):
        _validated(package)


def test_builder_records_failed_check_for_modified_live_candidate_digest():
    candidate = review._expected_live_evidence_binding()
    candidate["reviewed_candidate_semantic_digest"] = "0" * 64

    package = _package(candidate)
    digest_check = next(item for item in package["review_checklist"] if item["check_id"] == "candidate_digest_matches_recorded_live_evidence")

    assert digest_check["status"] == "FAIL"
    assert package["review_summary"]["failed_checks"] == 1
    with pytest.raises(review.DividendEventOperatorReviewError):
        _validated(package)


def test_builder_records_failed_check_for_modified_in_range_count():
    candidate = review._expected_live_evidence_binding()
    candidate["event_counts"]["dividend_event_count_in_range"] = 15
    candidate["in_range_dividend_count"] = 15

    package = _package(candidate)
    count_check = next(item for item in package["review_checklist"] if item["check_id"] == "event_count_in_range_sixteen")

    assert count_check["status"] == "FAIL"
    assert package["review_summary"]["failed_checks"] == 1
    with pytest.raises(review.DividendEventOperatorReviewError):
        _validated(package)


def test_source_assurance_review_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "dividend_event_operator_review_service.py"
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
    }
    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert {"send", "post", "put", "delete", "request"}.isdisjoint(called_attrs)
    assert "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE" in source
    assert "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY" in source
    assert "fetch_massive_dividend_events_v1" not in source


def test_service_exports_dividend_event_review_package_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
    assert services.DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY == "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert services.build_dividend_event_audit_candidate_review_package_v1 is review.build_dividend_event_audit_candidate_review_package_v1
    assert services.validate_dividend_event_audit_candidate_review_package_v1 is review.validate_dividend_event_audit_candidate_review_package_v1
    assert services.write_dividend_event_audit_candidate_review_package_v1 is review.write_dividend_event_audit_candidate_review_package_v1
    assert services.build_dividend_event_audit_candidate_review_markdown_v1 is review.build_dividend_event_audit_candidate_review_markdown_v1
