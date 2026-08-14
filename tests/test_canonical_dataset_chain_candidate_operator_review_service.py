from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import canonical_dataset_chain_candidate_operator_review_service as review_service


@pytest.fixture(scope="module")
def review() -> dict:
    return review_service.build_canonical_dataset_chain_candidate_review_package_v1()


def test_review_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        review_service.candidate_service.freeze.approval.evidence_review.execution,
        "execute_acquisition_provider_evidence_v1",
        lambda *args, **kwargs: pytest.fail("provider evidence execution was called"),
    )
    package = review_service.build_canonical_dataset_chain_candidate_review_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["dataset_generation_performed_in_review"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", review_service.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE),
        ("review_status", review_service.CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY),
        ("reviewed_canonical_dataset_chain_candidate_digest", review_service.EXPECTED_REVIEWED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST),
        ("reviewed_canonical_dataset_chain_candidate_blocker_count", 0),
        ("acquisition_generation_freeze_digest", review_service.candidate_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST),
        ("acquisition_generation_approval_digest", review_service.candidate_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST),
        ("acquisition_evidence_results_review_package_digest", review_service.candidate_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("corporate_action_authority_approval_digest", review_service.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST),
        ("identity_authority_freeze_digest", review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST),
        ("target_universe_count", 12),
        ("target_universe", review_service.TARGET_UNIVERSE),
        ("acquisition_generation_frozen", True),
        ("ready_for_canonical_dataset_chain_candidate", True),
        ("canonical_dataset_chain_candidate_created", True),
        ("canonical_dataset_chain_candidate_review_created", True),
        ("canonical_dataset_chain_scope", review_service.candidate_service.CANONICAL_DATASET_CHAIN_SCOPE),
        ("canonical_dataset_authority_status", review_service.candidate_service.CANONICAL_DATASET_AUTHORITY_STATUS),
        ("reviewed_canonical_dataset_planning_dimensions", review_service.candidate_service.CANONICAL_DATASET_PLANNING_DIMENSIONS),
        ("reviewed_canonical_dataset_source_profile", review_service.candidate_service.SOURCE_PROFILE),
        ("reviewed_future_canonical_dataset_chain", review_service.candidate_service.FUTURE_CANONICAL_DATASET_CHAIN),
        ("reviewed_future_gates", review_service.candidate_service.FUTURE_GATES),
        ("reviewed_risk_controls", review_service.candidate_service.RISK_CONTROLS),
        ("planned_output_count", 10),
        ("planned_outputs_status", review_service.candidate_service.PLANNED_NOT_GENERATED),
        ("planned_outputs_label", review_service.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE),
        ("provider_requests_made_in_review", False),
        ("live_provider_transport_enabled_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("dataset_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("canonical_dataset_candidate_created", False),
        ("canonical_dataset_generation_executed", False),
        ("canonical_dataset_frozen", False),
        ("registry_approval_created", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", review_service.NOT_ACCEPTED),
        ("profitability", review_service.PROFITABILITY_NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_use", review_service.NOT_AUTHORIZED),
        ("strategy_use", review_service.NOT_AUTHORIZED),
        ("paper_trading", review_service.NOT_AUTHORIZED),
        ("broker_execution", review_service.NOT_AUTHORIZED),
    ],
)
def test_review_package_fields(review: dict, field: str, expected: object):
    assert review[field] == expected


def test_per_ticker_review_entries_and_meta_are_preserved(review: dict):
    entries = review["reviewed_per_ticker_canonical_dataset_chain_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review_service.TARGET_UNIVERSE
    assert all(row["per_ticker_canonical_dataset_chain_candidate_digest"] for row in entries)
    assert all(row["per_ticker_canonical_dataset_chain_review_digest"] for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_bar_count"] == 913
    assert meta["meta_reduced_bar_count_flag"] is True
    assert all(row["historical_bar_count"] == 1003 for row in entries if row["ticker"] != "META")


def test_checklist_and_summary_are_complete(review: dict):
    assert [row["check_id"] for row in review["review_checklist"]] == review_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == review_service.PASS for row in review["review_checklist"])
    summary = review["review_summary"]
    assert summary["total_checks"] == len(review_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_canonical_dataset_approval"] is False


def test_review_and_per_ticker_digests_are_deterministic():
    first = review_service.build_canonical_dataset_chain_candidate_review_package_v1()
    second = review_service.build_canonical_dataset_chain_candidate_review_package_v1()
    assert first["canonical_dataset_chain_candidate_review_package_digest"] == second["canonical_dataset_chain_candidate_review_package_digest"]
    assert [row["per_ticker_canonical_dataset_chain_review_digest"] for row in first["reviewed_per_ticker_canonical_dataset_chain_entries"]] == [
        row["per_ticker_canonical_dataset_chain_review_digest"] for row in second["reviewed_per_ticker_canonical_dataset_chain_entries"]
    ]


def test_validator_accepts_valid_review(review: dict):
    result = review_service.validate_canonical_dataset_chain_candidate_review_package_v1(review)
    assert result["status"] == review_service.CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_canonical_dataset_chain_candidate_digest", "0" * 64),
        ("reviewed_canonical_dataset_chain_candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review_service.TARGET_UNIVERSE))),
        ("acquisition_generation_frozen", False),
        ("ready_for_canonical_dataset_chain_candidate", False),
        ("canonical_dataset_chain_candidate_created", False),
        ("canonical_dataset_chain_candidate_review_created", False),
        ("dataset_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("canonical_dataset_candidate_created", True),
        ("canonical_dataset_generation_executed", True),
        ("canonical_dataset_frozen", True),
        ("registry_approval_created", True),
        ("provider_requests_made_in_review", True),
        ("live_provider_transport_enabled_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("acquisition_generation_freeze_digest", None),
        ("reviewed_canonical_dataset_planning_dimensions", []),
        ("reviewed_canonical_dataset_source_profile", {}),
        ("reviewed_future_canonical_dataset_chain", []),
        ("reviewed_future_gates", []),
        ("reviewed_risk_controls", []),
        ("canonical_dataset_chain_candidate_review_package_digest", None),
    ],
)
def test_validator_rejects_invalid_review(review: dict, field: str, bad_value: object):
    invalid = deepcopy(review)
    invalid[field] = bad_value
    with pytest.raises(review_service.CanonicalDatasetChainCandidateReviewPackageError):
        review_service.validate_canonical_dataset_chain_candidate_review_package_v1(invalid)


@pytest.mark.parametrize(
    "digest_field",
    [
        "per_ticker_canonical_dataset_chain_candidate_digest",
        "per_ticker_canonical_dataset_chain_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(review: dict, digest_field: str):
    invalid = deepcopy(review)
    invalid["reviewed_per_ticker_canonical_dataset_chain_entries"][0].pop(digest_field)
    with pytest.raises(review_service.CanonicalDatasetChainCandidateReviewPackageError):
        review_service.validate_canonical_dataset_chain_candidate_review_package_v1(invalid)


def test_validator_rejects_changed_meta_count(review: dict):
    invalid = deepcopy(review)
    meta = next(row for row in invalid["reviewed_per_ticker_canonical_dataset_chain_entries"] if row["ticker"] == "META")
    meta["historical_bar_count"] = 1003
    with pytest.raises(review_service.CanonicalDatasetChainCandidateReviewPackageError):
        review_service.validate_canonical_dataset_chain_candidate_review_package_v1(invalid)


def test_markdown_includes_required_sections(review: dict):
    markdown = review_service.build_canonical_dataset_chain_candidate_review_markdown_v1(review)
    for section in (
        "Canonical Dataset Chain Candidate Review Package", "Reviewed Candidate",
        "Source Acquisition Generation Freeze", "Target Universe",
        "Per-Ticker Canonical Dataset Chain Review Entries", "Canonical Dataset Planning Dimensions",
        "Source Profile", "Future Canonical Dataset Chain", "Future Gates", "Risk Controls",
        "Dataset Boundary", "Canonical Dataset Boundary", "Registry Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_uses_isolated_directory_and_refuses_overwrite(tmp_path):
    result = review_service.write_canonical_dataset_chain_candidate_review_package_v1(tmp_path)
    payload = json.loads((tmp_path / "canonical_dataset_chain_candidate_review_package_v1.json").read_text(encoding="utf-8"))
    assert payload["canonical_dataset_chain_candidate_review_package_digest"] == result["canonical_dataset_chain_candidate_review_package_digest"]
    with pytest.raises(review_service.CanonicalDatasetChainCandidateReviewPackageError):
        review_service.write_canonical_dataset_chain_candidate_review_package_v1(tmp_path)


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE == review_service.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE
    assert services.build_canonical_dataset_chain_candidate_review_package_v1 is review_service.build_canonical_dataset_chain_candidate_review_package_v1
    assert services.validate_canonical_dataset_chain_candidate_review_package_v1 is review_service.validate_canonical_dataset_chain_candidate_review_package_v1
