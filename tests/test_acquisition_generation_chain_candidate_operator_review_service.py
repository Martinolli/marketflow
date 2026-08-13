from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import (
    acquisition_generation_chain_candidate_operator_review_service as review,
)


def _package() -> dict[str, Any]:
    return review.build_acquisition_generation_chain_candidate_review_package_v1()


def test_review_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    def provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider call")

    monkeypatch.setattr(
        review.candidate_service.authority.readiness.dividend_freeze.approval.review.evidence.execution,
        "execute_dividend_provider_evidence_v1",
        provider_call,
    )
    monkeypatch.setattr(
        review.candidate_service.authority.readiness.split_freeze.review.execution,
        "execute_split_provider_evidence_v1",
        provider_call,
    )
    package = _package()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["live_provider_transport_enabled_in_review"] is False
    assert package["market_data_acquisition_performed_in_review"] is False


def test_artifact_kind_status_schema_and_review_state_are_exact():
    package = _package()
    assert package["artifact_kind"] == review.ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE
    assert package["schema_version"] == review.SCHEMA_VERSION_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_V1
    assert package["review_status"] == review.ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY
    assert package["acquisition_generation_chain_candidate_created"] is True
    assert package["acquisition_generation_chain_candidate_review_created"] is True
    assert package["acquisition_generation_chain_ready_for_operator_review"] is True


def test_reviewed_candidate_evidence_is_exact_and_zero_blocker():
    package = _package()
    assert package["reviewed_acquisition_generation_chain_candidate_kind"] == review.candidate_service.ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE
    assert package["reviewed_acquisition_generation_chain_candidate_status"] == review.candidate_service.ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW
    assert package["reviewed_acquisition_generation_chain_candidate_digest"] == review.EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST
    assert package["reviewed_acquisition_generation_chain_candidate_checklist_total"] == 57
    assert package["reviewed_acquisition_generation_chain_candidate_checklist_passed"] == 57
    assert package["reviewed_acquisition_generation_chain_candidate_checklist_failed"] == 0
    assert package["reviewed_acquisition_generation_chain_candidate_blocker_count"] == 0


def test_explicit_candidate_object_binding_is_supported():
    source = review.candidate_service.build_acquisition_generation_chain_candidate_v1()
    package = review.build_acquisition_generation_chain_candidate_review_package_v1(source)
    assert package["acquisition_generation_chain_candidate_binding_mode"] == review.ACQUISITION_GENERATION_CHAIN_CANDIDATE_OBJECT_BINDING
    assert package["reviewed_acquisition_generation_chain_candidate_digest"] == source["acquisition_generation_chain_candidate_digest"]


def test_source_authority_digests_are_bound():
    package = _package()
    expected = {
        "corporate_action_authority_approval_digest": review.candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": review.candidate_service.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": review.candidate_service.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": review.candidate_service.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": review.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }
    assert {field: package[field] for field in expected} == expected


def test_target_universe_and_authorities_are_preserved():
    package = _package()
    assert package["target_universe_count"] == 12
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["corporate_action_authority_created"] is True
    assert package["corporate_action_authority_approved"] is True
    assert package["corporate_action_authority_scope"] == review.candidate_service.authority.CORPORATE_ACTION_AUTHORITY_ONLY
    assert package["split_event_authority_created"] is True
    assert package["split_event_authority_frozen"] is True
    assert package["dividend_event_authority_created"] is True
    assert package["dividend_event_authority_frozen"] is True
    assert package["ready_for_acquisition_generation_chain_candidate"] is True


def test_objective_scope_mode_and_authority_status_are_preserved():
    package = _package()
    assert package["acquisition_generation_chain_objective"] == review.candidate_service.ACQUISITION_GENERATION_CHAIN_OBJECTIVE
    assert package["acquisition_generation_chain_scope"] == review.candidate_service.ACQUISITION_GENERATION_CHAIN_SCOPE
    assert package["acquisition_generation_mode"] == review.candidate_service.ACQUISITION_GENERATION_MODE
    assert package["acquisition_generation_authority_status"] == review.candidate_service.ACQUISITION_GENERATION_AUTHORITY_STATUS


def test_planning_policy_chain_gates_controls_and_outputs_are_reviewed():
    package = _package()
    assert package["acquisition_planning_dimensions"] == review.candidate_service.ACQUISITION_PLANNING_DIMENSIONS
    assert package["future_acquisition_provider_request_policy"] == review.candidate_service.FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY
    assert package["future_acquisition_chain"] == review.candidate_service.FUTURE_ACQUISITION_CHAIN
    assert package["future_gates"] == review.candidate_service.FUTURE_GATES
    assert package["risk_controls"] == review.candidate_service.RISK_CONTROLS
    assert package["planned_output_count"] == 9
    assert all(row["generation_status"] == review.candidate_service.PLANNED_NOT_GENERATED for row in package["planned_outputs"])
    assert all(row["actionability"] == review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in package["planned_outputs"])


def test_per_ticker_review_entries_preserve_candidate_and_policy_evidence():
    package = _package()
    entries = package["per_ticker_acquisition_generation_chain_review_entries"]
    sources = {row["ticker"]: row for row in review.candidate_service._per_ticker_entries()}
    assert package["reviewed_per_ticker_acquisition_generation_chain_candidate_entry_count"] == 12
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review.TARGET_UNIVERSE
    for row in entries:
        source = sources[row["ticker"]]
        assert row["split_event_authority_classification"] == source["split_event_authority_classification"]
        assert row["dividend_event_authority_classification"] == source["dividend_event_authority_classification"]
        assert row["acquisition_generation_chain_review_status"] == review.READY_FOR_OPERATOR_ASSESSMENT
        assert row["source_acquisition_generation_chain_candidate_digest"] == review.EXPECTED_REVIEWED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST
        assert row["per_ticker_acquisition_generation_chain_candidate_digest"] == source["per_ticker_acquisition_generation_chain_candidate_digest"]
        assert row["per_ticker_acquisition_generation_chain_review_digest"] == review.per_ticker_acquisition_generation_chain_review_digest_v1(row)


def test_zero_dividend_and_no_split_policies_remain_exact():
    entries = {row["ticker"]: row for row in _package()["per_ticker_acquisition_generation_chain_review_entries"]}
    for ticker in ("AMZN", "TSLA"):
        assert entries[ticker]["dividend_event_count"] == 0
        assert "ZERO_ROW_ABSENCE_POLICY" in entries[ticker]["dividend_event_authority_classification"]
    for ticker in ("META", "JPM", "XOM", "JNJ", "LMT"):
        assert "NO_SPLIT_EVENTS_RETURNED_POLICY" in entries[ticker]["split_event_authority_classification"]


def test_checklist_and_summary_are_complete_and_passing():
    package = _package()
    checklist = package["review_checklist"]
    summary = package["review_summary"]
    assert [row["check_id"] for row in checklist] == review.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == review.PASS for row in checklist)
    assert summary["total_checks"] == 67
    assert summary["passed_checks"] == 67
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_acquisition_provider_request_approval"] is False
    assert summary["ready_for_acquisition_generation_approval"] is False
    assert summary["ready_for_acquisition_generation_freeze"] is False
    assert summary["ready_for_canonical_dataset_chain_candidate"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "acquisition_generation_chain_approved",
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_executed",
        "acquisition_generation_results_created",
        "acquisition_generation_frozen",
        "dataset_generation_authorized",
        "canonical_dataset_authorized",
        "canonical_dataset_candidate_created",
        "canonical_dataset_frozen",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
    ],
)
def test_validator_rejects_forbidden_true_fields(field: str):
    package = _package()
    package[field] = True
    with pytest.raises(review.AcquisitionGenerationChainCandidateReviewPackageError):
        review.validate_acquisition_generation_chain_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_acceptance_or_runtime_authorization(field: str, value: str):
    package = _package()
    package[field] = value
    with pytest.raises(review.AcquisitionGenerationChainCandidateReviewPackageError):
        review.validate_acquisition_generation_chain_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_acquisition_generation_chain_candidate_digest", "0" * 64),
        ("reviewed_acquisition_generation_chain_candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("corporate_action_authority_created", False),
        ("corporate_action_authority_approved", False),
        ("corporate_action_authority_scope", "WRONG"),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("dividend_event_authority_created", False),
        ("dividend_event_authority_frozen", False),
        ("ready_for_acquisition_generation_chain_candidate", False),
        ("acquisition_generation_chain_candidate_created", False),
        ("acquisition_generation_chain_candidate_review_created", False),
        ("corporate_action_authority_approval_digest", None),
        ("future_acquisition_chain", []),
        ("future_acquisition_provider_request_policy", {}),
        ("future_gates", []),
        ("risk_controls", []),
        ("acquisition_planning_dimensions", []),
    ],
)
def test_validator_rejects_invalid_core_or_missing_evidence(field: str, value: Any):
    package = _package()
    package[field] = value
    with pytest.raises(review.AcquisitionGenerationChainCandidateReviewPackageError):
        review.validate_acquisition_generation_chain_candidate_review_package_v1(package)


def test_builder_rejects_changed_candidate_digest():
    source = review.candidate_service.build_acquisition_generation_chain_candidate_v1()
    source["acquisition_generation_chain_candidate_digest"] = "0" * 64
    with pytest.raises(review.candidate_service.AcquisitionGenerationChainCandidateError):
        review.build_acquisition_generation_chain_candidate_review_package_v1(source)


def test_validator_accepts_valid_package_and_rejects_missing_review_digest():
    package = _package()
    validation = review.validate_acquisition_generation_chain_candidate_review_package_v1(package)
    assert validation["status"] == "ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["blocker_count"] == 0
    package.pop("acquisition_generation_chain_candidate_review_package_digest")
    with pytest.raises(review.AcquisitionGenerationChainCandidateReviewPackageError):
        review.validate_acquisition_generation_chain_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    "field",
    [
        "per_ticker_acquisition_generation_chain_candidate_digest",
        "per_ticker_acquisition_generation_chain_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(field: str):
    package = _package()
    package["per_ticker_acquisition_generation_chain_review_entries"][0].pop(field)
    with pytest.raises(review.AcquisitionGenerationChainCandidateReviewPackageError):
        review.validate_acquisition_generation_chain_candidate_review_package_v1(package)


def test_package_and_per_ticker_review_digests_are_deterministic():
    first = _package()
    second = _package()
    assert first == second
    assert first["acquisition_generation_chain_candidate_review_package_digest"] == second["acquisition_generation_chain_candidate_review_package_digest"]
    assert [row["per_ticker_acquisition_generation_chain_review_digest"] for row in first["per_ticker_acquisition_generation_chain_review_entries"]] == [row["per_ticker_acquisition_generation_chain_review_digest"] for row in second["per_ticker_acquisition_generation_chain_review_entries"]]


def test_markdown_contains_all_required_sections():
    markdown = review.build_acquisition_generation_chain_candidate_review_markdown_v1(_package())
    sections = [
        "Title", "Acquisition Generation Chain Candidate Review Package",
        "Reviewed Candidate", "Source Corporate-Action Authority Approval",
        "Target Universe", "Per-Ticker Acquisition Chain Review Entries",
        "Acquisition Planning Dimensions", "Future Provider Request Policy",
        "Future Acquisition Chain", "Future Gates", "Risk Controls",
        "Acquisition Boundary", "Dataset Boundary", "Canonical Dataset Boundary",
        "Registry Boundary", "Predictive/Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)


def test_writer_creates_valid_json_and_markdown_without_overwrite(tmp_path: Path):
    result = review.write_acquisition_generation_chain_candidate_review_package_v1(tmp_path)
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    assert json.loads(json_path.read_text(encoding="utf-8")) == result["review_package"]
    assert "## Guardrails" in markdown_path.read_text(encoding="utf-8")
    with pytest.raises(review.AcquisitionGenerationChainCandidateReviewPackageError):
        review.write_acquisition_generation_chain_candidate_review_package_v1(tmp_path)


def test_service_exports_are_available():
    expected = {
        "ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE",
        "ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY",
        "acquisition_generation_chain_candidate_review_package_digest_v1",
        "per_ticker_acquisition_generation_chain_review_digest_v1",
        "build_acquisition_generation_chain_candidate_review_markdown_v1",
        "build_acquisition_generation_chain_candidate_review_package_v1",
        "validate_acquisition_generation_chain_candidate_review_package_v1",
        "write_acquisition_generation_chain_candidate_review_package_v1",
    }
    assert all(name in services.__all__ for name in expected)
    assert all(hasattr(services, name) for name in expected)
