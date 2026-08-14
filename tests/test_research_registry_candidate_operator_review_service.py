from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

import marketflow.services as services
from marketflow.services import research_registry_candidate_operator_review_service as review


@pytest.fixture(scope="module")
def package() -> dict:
    return review.build_research_registry_candidate_review_package_v1()


def test_review_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        review.candidate_service.freeze,
        "build_canonical_dataset_frozen_v1",
        lambda *args, **kwargs: pytest.fail("freeze ceremony rebuild was called"),
    )
    built = review.build_research_registry_candidate_review_package_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made_in_review"] is False
    assert built["research_registry_candidate_binding_mode"] == (
        review.RESEARCH_REGISTRY_CANDIDATE_STATUS_BINDING
    )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE"),
        ("schema_version", "research_registry_candidate_review_v1"),
        ("review_status", "RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY"),
        ("reviewed_research_registry_candidate_kind", "RESEARCH_REGISTRY_CANDIDATE"),
        ("reviewed_research_registry_candidate_status", "RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW"),
        ("reviewed_research_registry_candidate_digest", review.EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST),
        ("reviewed_research_registry_candidate_checklist_total", 47),
        ("reviewed_research_registry_candidate_checklist_passed", 47),
        ("reviewed_research_registry_candidate_checklist_failed", 0),
        ("reviewed_research_registry_candidate_blocker_count", 0),
        ("canonical_dataset_freeze_digest", review.candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("canonical_dataset_results_review_package_digest", review.candidate_service.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("canonical_dataset_generation_digest", review.candidate_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
        ("records_digest", review.candidate_service.EXPECTED_RECORDS_DIGEST),
        ("identity_authority_freeze_digest", review.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST),
        ("target_universe_count", 12),
        ("target_universe", review.TARGET_UNIVERSE),
        ("canonical_dataset_generated", True),
        ("canonical_dataset_frozen", True),
        ("ready_for_research_registry_candidate", True),
        ("research_registry_candidate_created", True),
        ("research_registry_candidate_review_created", True),
        ("research_registry_authority_status", "NOT_APPROVED"),
        ("registry_approval_created", False),
        ("research_registry_approved", False),
        ("total_canonical_record_count", 11946),
        ("per_ticker_record_counts", review.EXPECTED_RECORD_COUNTS),
        ("registry_candidate_metadata", review.REGISTRY_CANDIDATE_METADATA),
        ("registry_planning_dimensions", review.REGISTRY_PLANNING_DIMENSIONS),
        ("future_registry_chain", review.FUTURE_REGISTRY_CHAIN),
        ("future_gates", review.FUTURE_GATES),
        ("risk_controls", review.RISK_CONTROLS),
        ("planned_output_count", 6),
        ("planned_outputs_status", "PLANNED_NOT_GENERATED"),
        ("planned_outputs_label", "RESEARCH_ONLY_NON_ACTIONABLE"),
        ("provider_requests_made_in_review", False),
        ("live_provider_transport_enabled_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("canonical_dataset_regenerated_in_review", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("automatic_stitching", False),
    ],
)
def test_review_package_contract(package: dict, field: str, expected: object) -> None:
    assert package[field] == expected


def test_all_source_evidence_digests_are_bound(package: dict) -> None:
    fields = (
        "canonical_dataset_generation_approval_digest",
        "canonical_dataset_chain_candidate_review_package_digest",
        "canonical_dataset_chain_candidate_digest",
        "acquisition_generation_freeze_digest",
        "acquisition_generation_approval_digest",
        "acquisition_evidence_results_review_package_digest",
        "acquisition_provider_evidence_execution_digest",
        "corporate_action_authority_approval_digest",
        "ticker_universe_selection_approval_digest",
    )
    assert all(isinstance(package[field], str) and len(package[field]) == 64 for field in fields)


def test_meta_and_non_meta_counts_are_preserved(package: dict) -> None:
    assert package["per_ticker_record_counts"]["META"] == 913
    assert all(
        count == 1003
        for ticker, count in package["per_ticker_record_counts"].items()
        if ticker != "META"
    )


def test_per_ticker_review_entries_and_digests(package: dict) -> None:
    entries = package["per_ticker_research_registry_review_entries"]
    assert [row["ticker"] for row in entries] == review.TARGET_UNIVERSE
    assert len(entries) == 12
    for row in entries:
        assert row["research_registry_candidate_review_status"] == "READY_FOR_OPERATOR_ASSESSMENT"
        assert row["source_research_registry_candidate_digest"] == review.EXPECTED_REVIEWED_RESEARCH_REGISTRY_CANDIDATE_DIGEST
        assert len(row["per_ticker_research_registry_candidate_digest"]) == 64
        assert len(row["per_ticker_research_registry_review_digest"]) == 64
        assert row["registry_approval_created"] is False
        assert row["research_registry_approved"] is False
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True


def test_planned_outputs_are_preserved_not_generated_and_research_only(package: dict) -> None:
    assert [row["planned_output"] for row in package["planned_outputs"]] == review.PLANNED_OUTPUT_NAMES
    assert all(row["generation_status"] == "PLANNED_NOT_GENERATED" for row in package["planned_outputs"])
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in package["planned_outputs"])


def test_checklist_contains_all_required_ids_and_passes(package: dict) -> None:
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" and row["severity"] == "BLOCKER" for row in package["review_checklist"])


def test_review_summary_counts_and_boundaries_are_correct(package: dict) -> None:
    summary = package["review_summary"]
    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS) == 55
    assert summary["passed_checks"] == 55
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_research_registry_approval"] is False
    assert summary["registry_approval_created"] is False
    assert summary["research_registry_approved"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic(package: dict) -> None:
    repeated = review.build_research_registry_candidate_review_package_v1()
    assert repeated["research_registry_candidate_review_package_digest"] == package[
        "research_registry_candidate_review_package_digest"
    ]
    assert package["research_registry_candidate_review_package_digest"] == (
        review.research_registry_candidate_review_package_digest_v1(package)
    )


def test_per_ticker_review_digests_are_deterministic(package: dict) -> None:
    repeated = review.build_research_registry_candidate_review_package_v1()
    assert [row["per_ticker_research_registry_review_digest"] for row in repeated["per_ticker_research_registry_review_entries"]] == [
        row["per_ticker_research_registry_review_digest"]
        for row in package["per_ticker_research_registry_review_entries"]
    ]


def test_explicit_candidate_uses_validated_object_binding() -> None:
    candidate = review.candidate_service.build_research_registry_candidate_v1()
    built = review.build_research_registry_candidate_review_package_v1(candidate)
    assert built["research_registry_candidate_binding_mode"] == (
        review.RESEARCH_REGISTRY_CANDIDATE_OBJECT_BINDING
    )


def test_validator_accepts_valid_review_package(package: dict) -> None:
    result = review.validate_research_registry_candidate_review_package_v1(package)
    assert result["status"] == "RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY"
    assert result["blocker_count"] == 0
    assert result["ready_for_operator_assessment"] is True
    assert result["ready_for_research_registry_approval"] is False


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_research_registry_candidate_digest", "0" * 64),
        ("reviewed_research_registry_candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("canonical_dataset_generated", False),
        ("canonical_dataset_frozen", False),
        ("ready_for_research_registry_candidate", False),
        ("research_registry_candidate_created", False),
        ("research_registry_candidate_review_created", False),
        ("registry_approval_created", True),
        ("research_registry_approved", True),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
        ("provider_requests_made_in_review", True),
        ("live_provider_transport_enabled_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("reviewed_research_registry_candidate_digest", None),
        ("registry_candidate_metadata", None),
        ("registry_planning_dimensions", None),
        ("future_registry_chain", None),
        ("future_gates", None),
        ("risk_controls", None),
        ("research_registry_candidate_review_package_digest", None),
    ],
)
def test_validator_rejects_invalid_contract_fields(
    package: dict,
    field: str,
    invalid: object,
) -> None:
    changed = deepcopy(package)
    changed[field] = invalid
    with pytest.raises(review.ResearchRegistryCandidateReviewPackageError):
        review.validate_research_registry_candidate_review_package_v1(changed)


@pytest.mark.parametrize(("ticker", "count"), [("META", 914), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_count(
    package: dict,
    ticker: str,
    count: int,
) -> None:
    changed = deepcopy(package)
    changed["per_ticker_record_counts"][ticker] = count
    with pytest.raises(review.ResearchRegistryCandidateReviewPackageError):
        review.validate_research_registry_candidate_review_package_v1(changed)


@pytest.mark.parametrize(
    "digest_field",
    [
        "per_ticker_research_registry_candidate_digest",
        "per_ticker_research_registry_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(
    package: dict,
    digest_field: str,
) -> None:
    changed = deepcopy(package)
    changed["per_ticker_research_registry_review_entries"][0].pop(digest_field)
    with pytest.raises(review.ResearchRegistryCandidateReviewPackageError):
        review.validate_research_registry_candidate_review_package_v1(changed)


def test_builder_rejects_changed_candidate_digest() -> None:
    candidate = review.candidate_service.build_research_registry_candidate_v1()
    candidate["research_registry_candidate_digest"] = "0" * 64
    with pytest.raises(review.ResearchRegistryCandidateReviewPackageError):
        review.build_research_registry_candidate_review_package_v1(candidate)


def test_markdown_includes_required_sections(package: dict) -> None:
    markdown = review.build_research_registry_candidate_review_markdown_v1(package)
    required = [
        "Title",
        "Research Registry Candidate Review Package",
        "Reviewed Candidate",
        "Source Frozen Canonical Dataset",
        "Target Universe",
        "Registry Candidate Metadata",
        "Per-Ticker Registry Review Entries",
        "Future Registry Chain",
        "Future Gates",
        "Risk Controls",
        "Registry Approval Boundary",
        "Predictive/Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in required)


def test_writer_writes_once_without_overwrite(package: dict, tmp_path: Path) -> None:
    result = review.write_research_registry_candidate_review_package_v1(tmp_path)
    written = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert written["research_registry_candidate_review_package_digest"] == package[
        "research_registry_candidate_review_package_digest"
    ]
    with pytest.raises(review.ResearchRegistryCandidateReviewPackageError):
        review.write_research_registry_candidate_review_package_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_research_registry_candidate_review_package_v1 is (
        review.build_research_registry_candidate_review_package_v1
    )
    assert services.validate_research_registry_candidate_review_package_v1 is (
        review.validate_research_registry_candidate_review_package_v1
    )
    assert services.write_research_registry_candidate_review_package_v1 is (
        review.write_research_registry_candidate_review_package_v1
    )
    assert services.build_research_registry_candidate_review_markdown_v1 is (
        review.build_research_registry_candidate_review_markdown_v1
    )
