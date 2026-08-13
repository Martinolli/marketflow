from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import acquisition_generation_chain_candidate_service as candidate


def _candidate() -> dict[str, Any]:
    return candidate.build_acquisition_generation_chain_candidate_v1()


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider call")

    monkeypatch.setattr(
        candidate.authority.readiness.dividend_freeze.approval.review.evidence.execution,
        "execute_dividend_provider_evidence_v1",
        provider_call,
    )
    monkeypatch.setattr(
        candidate.authority.readiness.split_freeze.review.execution,
        "execute_split_provider_evidence_v1",
        provider_call,
    )
    artifact = _candidate()
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made"] is False
    assert artifact["live_provider_transport_enabled"] is False
    assert artifact["market_data_acquisition_performed"] is False


def test_artifact_kind_status_and_candidate_state_are_exact():
    artifact = _candidate()
    assert artifact["artifact_kind"] == candidate.ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE
    assert artifact["candidate_status"] == candidate.ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW
    assert artifact["acquisition_generation_chain_candidate_created"] is True
    assert artifact["acquisition_generation_chain_ready_for_operator_review"] is True
    assert artifact["ready_for_acquisition_generation_chain_candidate"] is True
    assert artifact["acquisition_generation_chain_approved"] is False


def test_all_source_authority_digests_are_bound():
    artifact = _candidate()
    expected = {
        "corporate_action_authority_approval_digest": candidate.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": candidate.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_approval_digest": candidate.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "split_event_authority_freeze_digest": candidate.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": candidate.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": candidate.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_event_authority_freeze_digest": candidate.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": candidate.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_event_evidence_results_review_package_digest": candidate.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": candidate.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": candidate.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": candidate.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": candidate.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
    }
    assert {field: artifact[field] for field in expected} == expected


def test_target_universe_and_authority_prerequisites_are_exact():
    artifact = _candidate()
    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == candidate.TARGET_UNIVERSE
    assert artifact["identity_authority_created"] is True
    assert artifact["identity_authority_frozen"] is True
    assert artifact["corporate_action_authority_created"] is True
    assert artifact["corporate_action_authority_approved"] is True
    assert artifact["corporate_action_authority_scope"] == candidate.authority.CORPORATE_ACTION_AUTHORITY_ONLY
    assert artifact["split_event_authority_created"] is True
    assert artifact["split_event_authority_frozen"] is True
    assert artifact["dividend_event_authority_created"] is True
    assert artifact["dividend_event_authority_frozen"] is True


def test_acquisition_objective_scope_mode_and_authority_status_are_exact():
    artifact = _candidate()
    assert artifact["acquisition_generation_chain_objective"] == candidate.ACQUISITION_GENERATION_CHAIN_OBJECTIVE
    assert artifact["acquisition_generation_chain_scope"] == candidate.ACQUISITION_GENERATION_CHAIN_SCOPE
    assert artifact["acquisition_generation_mode"] == candidate.ACQUISITION_GENERATION_MODE
    assert artifact["acquisition_generation_authority_status"] == candidate.ACQUISITION_GENERATION_AUTHORITY_STATUS


def test_planning_dimensions_future_policy_chain_gates_and_controls_are_exact():
    artifact = _candidate()
    assert artifact["acquisition_planning_dimensions"] == candidate.ACQUISITION_PLANNING_DIMENSIONS
    assert artifact["future_acquisition_provider_request_policy"] == candidate.FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY
    assert artifact["future_acquisition_chain"] == candidate.FUTURE_ACQUISITION_CHAIN
    assert artifact["future_gates"] == candidate.FUTURE_GATES
    assert artifact["risk_controls"] == candidate.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_non_actionable():
    artifact = _candidate()
    outputs = artifact["planned_outputs"]
    assert [row["output_name"] for row in outputs] == candidate.PLANNED_OUTPUT_NAMES
    assert all(row["generation_status"] == candidate.PLANNED_NOT_GENERATED for row in outputs)
    assert all(row["actionability"] == candidate.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)


def test_per_ticker_entries_preserve_classifications_and_digests():
    artifact = _candidate()
    entries = artifact["per_ticker_acquisition_generation_chain_candidates"]
    source = {row["ticker"]: row for row in candidate._source_authority_entries()}
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate.TARGET_UNIVERSE
    for row in entries:
        source_row = source[row["ticker"]]
        assert row["split_event_authority_classification"] == source_row["split_event_authority_classification"]
        assert row["dividend_event_authority_classification"] == source_row["dividend_event_authority_classification"]
        assert row["acquisition_generation_chain_status"] == candidate.PLANNED_READY_FOR_OPERATOR_REVIEW
        assert row["market_data_acquisition_status"] == candidate.MARKET_DATA_ACQUISITION_NOT_EXECUTED
        assert row["acquisition_authorized"] is False
        assert row["acquisition_generation_authorized"] is False
        assert row["acquisition_generation_executed"] is False
        assert row["per_ticker_acquisition_generation_chain_candidate_digest"] == candidate.per_ticker_acquisition_generation_chain_candidate_digest_v1(row)


def test_amzn_tsla_and_no_split_policies_are_preserved():
    entries = {row["ticker"]: row for row in _candidate()["per_ticker_acquisition_generation_chain_candidates"]}
    for ticker in ("AMZN", "TSLA"):
        assert entries[ticker]["dividend_event_count"] == 0
        assert "ZERO_ROW_ABSENCE_POLICY" in entries[ticker]["dividend_event_authority_classification"]
    for ticker in ("META", "JPM", "XOM", "JNJ", "LMT"):
        assert "NO_SPLIT_EVENTS_RETURNED_POLICY" in entries[ticker]["split_event_authority_classification"]


def test_checklist_and_summary_are_complete_and_passing():
    artifact = _candidate()
    checklist = artifact["candidate_checklist"]
    summary = artifact["candidate_summary"]
    assert [row["check_id"] for row in checklist] == candidate.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == candidate.PASS for row in checklist)
    assert summary["total_checks"] == 57
    assert summary["passed_checks"] == 57
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_acquisition_provider_request_approval"] is False
    assert summary["ready_for_acquisition_generation_approval"] is False
    assert summary["ready_for_acquisition_generation_freeze"] is False
    assert summary["ready_for_canonical_dataset_chain_candidate"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
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
    artifact = _candidate()
    artifact[field] = True
    with pytest.raises(candidate.AcquisitionGenerationChainCandidateError):
        candidate.validate_acquisition_generation_chain_candidate_v1(artifact)


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
    artifact = _candidate()
    artifact[field] = value
    with pytest.raises(candidate.AcquisitionGenerationChainCandidateError):
        candidate.validate_acquisition_generation_chain_candidate_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(candidate.TARGET_UNIVERSE))),
        ("corporate_action_authority_created", False),
        ("corporate_action_authority_approved", False),
        ("corporate_action_authority_scope", "WRONG"),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("dividend_event_authority_created", False),
        ("dividend_event_authority_frozen", False),
        ("ready_for_acquisition_generation_chain_candidate", False),
        ("acquisition_generation_chain_ready_for_operator_review", False),
        ("acquisition_generation_chain_candidate_created", False),
        ("corporate_action_authority_approval_digest", None),
        ("future_acquisition_chain", []),
        ("future_acquisition_provider_request_policy", {}),
        ("future_gates", []),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_core_contract(field: str, value: Any):
    artifact = _candidate()
    artifact[field] = value
    with pytest.raises(candidate.AcquisitionGenerationChainCandidateError):
        candidate.validate_acquisition_generation_chain_candidate_v1(artifact)


def test_validator_accepts_valid_candidate_and_rejects_missing_digest():
    artifact = _candidate()
    validation = candidate.validate_acquisition_generation_chain_candidate_v1(artifact)
    assert validation["status"] == "ACQUISITION_GENERATION_CHAIN_CANDIDATE_VALID"
    assert validation["blocker_count"] == 0
    artifact.pop("acquisition_generation_chain_candidate_digest")
    with pytest.raises(candidate.AcquisitionGenerationChainCandidateError):
        candidate.validate_acquisition_generation_chain_candidate_v1(artifact)


def test_validator_rejects_missing_per_ticker_digest():
    artifact = _candidate()
    artifact["per_ticker_acquisition_generation_chain_candidates"][0].pop(
        "per_ticker_acquisition_generation_chain_candidate_digest"
    )
    with pytest.raises(candidate.AcquisitionGenerationChainCandidateError):
        candidate.validate_acquisition_generation_chain_candidate_v1(artifact)


def test_candidate_and_per_ticker_digests_are_deterministic():
    first = _candidate()
    second = _candidate()
    assert first == second
    assert first["acquisition_generation_chain_candidate_digest"] == second["acquisition_generation_chain_candidate_digest"]
    assert [row["per_ticker_acquisition_generation_chain_candidate_digest"] for row in first["per_ticker_acquisition_generation_chain_candidates"]] == [row["per_ticker_acquisition_generation_chain_candidate_digest"] for row in second["per_ticker_acquisition_generation_chain_candidates"]]


def test_markdown_contains_all_required_sections():
    markdown = candidate.build_acquisition_generation_chain_candidate_markdown_v1(_candidate())
    sections = [
        "Title", "Acquisition Generation Chain Candidate",
        "Source Corporate-Action Authority Approval", "Target Universe",
        "Per-Ticker Acquisition Chain Candidate Entries", "Acquisition Planning Dimensions",
        "Future Provider Request Policy", "Future Acquisition Chain", "Future Gates",
        "Risk Controls", "Acquisition Boundary", "Dataset Boundary",
        "Canonical Dataset Boundary", "Registry Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)


def test_writer_creates_valid_json_and_markdown_without_overwrite(tmp_path: Path):
    result = candidate.write_acquisition_generation_chain_candidate_v1(tmp_path)
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    assert json.loads(json_path.read_text(encoding="utf-8")) == result["candidate"]
    assert "## Guardrails" in markdown_path.read_text(encoding="utf-8")
    with pytest.raises(candidate.AcquisitionGenerationChainCandidateError):
        candidate.write_acquisition_generation_chain_candidate_v1(tmp_path)


def test_service_exports_are_available():
    expected = {
        "ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE",
        "ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW",
        "acquisition_generation_chain_candidate_digest_v1",
        "per_ticker_acquisition_generation_chain_candidate_digest_v1",
        "build_acquisition_generation_chain_candidate_markdown_v1",
        "build_acquisition_generation_chain_candidate_v1",
        "validate_acquisition_generation_chain_candidate_v1",
        "write_acquisition_generation_chain_candidate_v1",
    }
    assert all(name in services.__all__ for name in expected)
    assert all(hasattr(services, name) for name in expected)
