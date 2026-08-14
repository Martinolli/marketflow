from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

import marketflow.services as services
from marketflow.services import research_registry_candidate_service as registry


@pytest.fixture(scope="module")
def candidate() -> dict:
    return registry.build_research_registry_candidate_v1()


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        registry.freeze,
        "build_canonical_dataset_frozen_v1",
        lambda *args, **kwargs: pytest.fail("freeze ceremony rebuild was called"),
    )
    built = registry.build_research_registry_candidate_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made"] is False
    assert built["source_freeze_binding_mode"] == registry.SOURCE_BINDING_MODE_COMMITTED_STATUS


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "RESEARCH_REGISTRY_CANDIDATE"),
        ("candidate_status", "RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW"),
        ("canonical_dataset_freeze_digest", registry.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("canonical_dataset_results_review_package_digest", registry.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("canonical_dataset_generation_digest", registry.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
        ("records_digest", registry.EXPECTED_RECORDS_DIGEST),
        ("identity_authority_freeze_digest", registry.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST),
        ("target_universe_count", 12),
        ("target_universe", registry.TARGET_UNIVERSE),
        ("canonical_dataset_generated", True),
        ("canonical_dataset_frozen", True),
        ("ready_for_research_registry_candidate", True),
        ("research_registry_candidate_created", True),
        ("research_registry_candidate_ready_for_operator_review", True),
        ("research_registry_authority_status", "NOT_APPROVED"),
        ("registry_approval_created", False),
        ("research_registry_approved", False),
        ("total_canonical_record_count", 11946),
        ("per_ticker_record_counts", registry.EXPECTED_RECORD_COUNTS),
        ("registry_candidate_metadata", registry.REGISTRY_CANDIDATE_METADATA),
        ("registry_planning_dimensions", registry.REGISTRY_PLANNING_DIMENSIONS),
        ("future_registry_chain", registry.FUTURE_REGISTRY_CHAIN),
        ("future_gates", registry.FUTURE_GATES),
        ("risk_controls", registry.RISK_CONTROLS),
        ("provider_requests_made", False),
        ("live_provider_transport_enabled", False),
        ("market_data_acquisition_performed", False),
        ("dataset_generation_performed", False),
        ("canonical_dataset_regenerated", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_candidate_contract(candidate: dict, field: str, expected: object) -> None:
    assert candidate[field] == expected


def test_meta_and_non_meta_counts_are_preserved(candidate: dict) -> None:
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert all(count == 1003 for ticker, count in candidate["per_ticker_record_counts"].items() if ticker != "META")


def test_registry_metadata_is_complete(candidate: dict) -> None:
    metadata = candidate["registry_candidate_metadata"]
    assert metadata["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert metadata["registry_candidate_label"] == "RESEARCH_ONLY_NON_ACTIONABLE"
    assert metadata["records_digest"] == registry.EXPECTED_RECORDS_DIGEST


def test_per_ticker_entries_and_digests(candidate: dict) -> None:
    entries = candidate["per_ticker_research_registry_candidates"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == registry.TARGET_UNIVERSE
    assert all(len(row["per_ticker_research_registry_candidate_digest"]) == 64 for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True


def test_planned_outputs_are_not_generated_and_are_research_only(candidate: dict) -> None:
    assert [row["planned_output"] for row in candidate["planned_outputs"]] == registry.PLANNED_OUTPUT_NAMES
    assert all(row["generation_status"] == "PLANNED_NOT_GENERATED" for row in candidate["planned_outputs"])
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in candidate["planned_outputs"])


def test_checklist_contains_all_required_ids_and_passes(candidate: dict) -> None:
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == registry.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" and row["severity"] == "BLOCKER" for row in candidate["candidate_checklist"])


def test_summary_counts_are_correct(candidate: dict) -> None:
    summary = candidate["candidate_summary"]
    assert summary["total_checks"] == len(registry.REQUIRED_CHECK_IDS) == 47
    assert summary["passed_checks"] == 47
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_research_registry_approval"] is False


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    repeated = registry.build_research_registry_candidate_v1()
    assert repeated["research_registry_candidate_digest"] == candidate["research_registry_candidate_digest"]


def test_per_ticker_candidate_digests_are_deterministic(candidate: dict) -> None:
    repeated = registry.build_research_registry_candidate_v1()
    assert [row["per_ticker_research_registry_candidate_digest"] for row in repeated["per_ticker_research_registry_candidates"]] == [
        row["per_ticker_research_registry_candidate_digest"] for row in candidate["per_ticker_research_registry_candidates"]
    ]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = registry.validate_research_registry_candidate_v1(candidate)
    assert result["status"] == "RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW"
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(registry.TARGET_UNIVERSE))),
        ("canonical_dataset_generated", False),
        ("canonical_dataset_frozen", False),
        ("ready_for_research_registry_candidate", False),
        ("research_registry_candidate_created", False),
        ("registry_approval_created", True),
        ("research_registry_approved", True),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
        ("provider_requests_made", True),
        ("live_provider_transport_enabled", True),
        ("market_data_acquisition_performed", True),
        ("dataset_generation_performed", True),
        ("canonical_dataset_regenerated", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("canonical_dataset_freeze_digest", None),
        ("registry_candidate_metadata", {}),
        ("registry_planning_dimensions", []),
        ("future_registry_chain", []),
        ("future_gates", []),
        ("risk_controls", []),
        ("planned_outputs", []),
        ("research_registry_candidate_digest", None),
    ],
)
def test_validator_rejects_invalid_contract_fields(
    candidate: dict, field: str, invalid: object
) -> None:
    changed = deepcopy(candidate)
    changed[field] = invalid
    with pytest.raises(registry.ResearchRegistryCandidateError):
        registry.validate_research_registry_candidate_v1(changed)


@pytest.mark.parametrize(("ticker", "count"), [("META", 914), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_count(candidate: dict, ticker: str, count: int) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_record_counts"][ticker] = count
    with pytest.raises(registry.ResearchRegistryCandidateError):
        registry.validate_research_registry_candidate_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_research_registry_candidates"][0].pop("per_ticker_research_registry_candidate_digest")
    with pytest.raises(registry.ResearchRegistryCandidateError):
        registry.validate_research_registry_candidate_v1(changed)


def test_markdown_includes_required_sections(candidate: dict) -> None:
    markdown = registry.build_research_registry_candidate_markdown_v1(candidate)
    required = [
        "Title", "Research Registry Candidate", "Source Frozen Canonical Dataset",
        "Target Universe", "Registry Candidate Metadata", "Per-Ticker Registry Candidate Entries",
        "Future Registry Chain", "Future Gates", "Risk Controls", "Registry Approval Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in required)


def test_writer_writes_once_without_overwrite(candidate: dict, tmp_path: Path) -> None:
    result = registry.write_research_registry_candidate_v1(tmp_path)
    written = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert written["research_registry_candidate_digest"] == candidate["research_registry_candidate_digest"]
    with pytest.raises(registry.ResearchRegistryCandidateError):
        registry.write_research_registry_candidate_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.build_research_registry_candidate_v1 is registry.build_research_registry_candidate_v1
    assert services.validate_research_registry_candidate_v1 is registry.validate_research_registry_candidate_v1
    assert services.write_research_registry_candidate_v1 is registry.write_research_registry_candidate_v1
