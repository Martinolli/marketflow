from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import canonical_dataset_chain_candidate_service as candidate_service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_canonical_dataset_chain_candidate_v1()


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        candidate_service.freeze.approval.evidence_review.execution,
        "execute_acquisition_provider_evidence_v1",
        lambda *args, **kwargs: pytest.fail("provider evidence execution was called"),
    )
    artifact = candidate_service.build_canonical_dataset_chain_candidate_v1()
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made"] is False
    assert artifact["dataset_generation_performed"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", candidate_service.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE),
        ("candidate_status", candidate_service.CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW),
        ("acquisition_generation_freeze_digest", candidate_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST),
        ("acquisition_generation_approval_digest", candidate_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST),
        ("acquisition_evidence_results_review_package_digest", candidate_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("corporate_action_authority_approval_digest", candidate_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST),
        ("identity_authority_freeze_digest", candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST),
        ("target_universe_count", 12),
        ("target_universe", candidate_service.TARGET_UNIVERSE),
        ("acquisition_generation_frozen", True),
        ("ready_for_canonical_dataset_chain_candidate", True),
        ("canonical_dataset_chain_candidate_created", True),
        ("canonical_dataset_chain_scope", candidate_service.CANONICAL_DATASET_CHAIN_SCOPE),
        ("canonical_dataset_authority_status", candidate_service.CANONICAL_DATASET_AUTHORITY_STATUS),
        ("canonical_dataset_planning_dimensions", candidate_service.CANONICAL_DATASET_PLANNING_DIMENSIONS),
        ("canonical_dataset_source_profile", candidate_service.SOURCE_PROFILE),
        ("future_canonical_dataset_chain", candidate_service.FUTURE_CANONICAL_DATASET_CHAIN),
        ("future_gates", candidate_service.FUTURE_GATES),
        ("risk_controls", candidate_service.RISK_CONTROLS),
        ("provider_requests_made", False),
        ("live_provider_transport_enabled", False),
        ("market_data_acquisition_performed", False),
        ("dataset_generation_performed", False),
        ("dataset_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("canonical_dataset_candidate_created", False),
        ("canonical_dataset_generation_executed", False),
        ("canonical_dataset_frozen", False),
        ("registry_approval_created", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", candidate_service.NOT_ACCEPTED),
        ("profitability", candidate_service.PROFITABILITY_NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_use", candidate_service.NOT_AUTHORIZED),
        ("strategy_use", candidate_service.NOT_AUTHORIZED),
        ("paper_trading", candidate_service.NOT_AUTHORIZED),
        ("broker_execution", candidate_service.NOT_AUTHORIZED),
    ],
)
def test_candidate_fields(candidate: dict, field: str, expected: object):
    assert candidate[field] == expected


def test_per_ticker_entries_and_meta_are_preserved(candidate: dict):
    entries = candidate["per_ticker_canonical_dataset_chain_candidates"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE
    assert all(row["per_ticker_canonical_dataset_chain_candidate_digest"] for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_bar_count"] == 913
    assert meta["meta_reduced_bar_count_flag"] is True
    assert all(row["historical_bar_count"] == 1003 for row in entries if row["ticker"] != "META")


def test_planned_outputs_are_not_generated_and_research_only(candidate: dict):
    assert [row["output_name"] for row in candidate["planned_outputs"]] == candidate_service.PLANNED_OUTPUT_NAMES
    assert all(row["generation_status"] == candidate_service.PLANNED_NOT_GENERATED for row in candidate["planned_outputs"])
    assert all(row["classification"] == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in candidate["planned_outputs"])


def test_checklist_and_summary_are_complete(candidate: dict):
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == candidate_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == candidate_service.PASS for row in candidate["candidate_checklist"])
    summary = candidate["candidate_summary"]
    assert summary["total_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_canonical_dataset_approval"] is False


def test_candidate_and_per_ticker_digests_are_deterministic():
    first = candidate_service.build_canonical_dataset_chain_candidate_v1()
    second = candidate_service.build_canonical_dataset_chain_candidate_v1()
    assert first["canonical_dataset_chain_candidate_digest"] == second["canonical_dataset_chain_candidate_digest"]
    assert [row["per_ticker_canonical_dataset_chain_candidate_digest"] for row in first["per_ticker_canonical_dataset_chain_candidates"]] == [
        row["per_ticker_canonical_dataset_chain_candidate_digest"] for row in second["per_ticker_canonical_dataset_chain_candidates"]
    ]


def test_validator_accepts_valid_candidate(candidate: dict):
    result = candidate_service.validate_canonical_dataset_chain_candidate_v1(candidate)
    assert result["status"] == candidate_service.CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(candidate_service.TARGET_UNIVERSE))),
        ("acquisition_generation_frozen", False),
        ("ready_for_canonical_dataset_chain_candidate", False),
        ("canonical_dataset_chain_candidate_created", False),
        ("dataset_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("canonical_dataset_candidate_created", True),
        ("canonical_dataset_generation_executed", True),
        ("canonical_dataset_frozen", True),
        ("registry_approval_created", True),
        ("provider_requests_made", True),
        ("live_provider_transport_enabled", True),
        ("market_data_acquisition_performed", True),
        ("dataset_generation_performed", True),
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
        ("canonical_dataset_planning_dimensions", []),
        ("canonical_dataset_source_profile", {}),
        ("future_canonical_dataset_chain", []),
        ("future_gates", []),
        ("risk_controls", []),
        ("canonical_dataset_chain_candidate_digest", None),
    ],
)
def test_validator_rejects_invalid_candidate(candidate: dict, field: str, bad_value: object):
    invalid = deepcopy(candidate)
    invalid[field] = bad_value
    with pytest.raises(candidate_service.CanonicalDatasetChainCandidateError):
        candidate_service.validate_canonical_dataset_chain_candidate_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict):
    invalid = deepcopy(candidate)
    invalid["per_ticker_canonical_dataset_chain_candidates"][0].pop(
        "per_ticker_canonical_dataset_chain_candidate_digest"
    )
    with pytest.raises(candidate_service.CanonicalDatasetChainCandidateError):
        candidate_service.validate_canonical_dataset_chain_candidate_v1(invalid)


def test_validator_rejects_changed_meta_count(candidate: dict):
    invalid = deepcopy(candidate)
    meta = next(row for row in invalid["per_ticker_canonical_dataset_chain_candidates"] if row["ticker"] == "META")
    meta["historical_bar_count"] = 1003
    with pytest.raises(candidate_service.CanonicalDatasetChainCandidateError):
        candidate_service.validate_canonical_dataset_chain_candidate_v1(invalid)


def test_markdown_includes_required_sections(candidate: dict):
    markdown = candidate_service.build_canonical_dataset_chain_candidate_markdown_v1(candidate)
    for section in (
        "Canonical Dataset Chain Candidate", "Source Acquisition Generation Freeze", "Target Universe",
        "Per-Ticker Canonical Dataset Chain Candidate Entries", "Canonical Dataset Planning Dimensions",
        "Source Profile", "Future Canonical Dataset Chain", "Future Gates", "Risk Controls",
        "Dataset Boundary", "Canonical Dataset Boundary", "Registry Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_uses_isolated_directory_and_refuses_overwrite(tmp_path):
    result = candidate_service.write_canonical_dataset_chain_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / "canonical_dataset_chain_candidate_v1.json").read_text(encoding="utf-8"))
    assert payload["canonical_dataset_chain_candidate_digest"] == result["canonical_dataset_chain_candidate_digest"]
    with pytest.raises(candidate_service.CanonicalDatasetChainCandidateError):
        candidate_service.write_canonical_dataset_chain_candidate_v1(tmp_path)


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE == candidate_service.ARTIFACT_KIND_CANONICAL_DATASET_CHAIN_CANDIDATE
    assert services.build_canonical_dataset_chain_candidate_v1 is candidate_service.build_canonical_dataset_chain_candidate_v1
    assert services.validate_canonical_dataset_chain_candidate_v1 is candidate_service.validate_canonical_dataset_chain_candidate_v1
