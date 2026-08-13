from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import acquisition_provider_evidence_execution_service as execution


def _fake_transport(request: dict[str, Any]) -> dict[str, Any]:
    ticker = request["provider_query_ticker"]
    if ticker == "NVDA":
        return {"status": "OK", "results": []}
    return {
        "status": "OK",
        "results": [
            {"t": 1641168000000, "o": 100.0, "h": 102.5, "l": 99.5, "c": 101.25, "v": 1000000.0, "n": 5000},
            {"t": 1641254400000, "o": 101.25, "h": 103.0, "l": 100.5, "c": 102.75, "v": 1100000.0, "n": 5100},
        ],
    }


def _executed(tmp_path: Path) -> dict[str, Any]:
    return execution.execute_acquisition_provider_evidence_v1(
        api_key="fictional-test-key",
        transport=_fake_transport,
        output_root=tmp_path,
        run_timestamp_utc="2026-08-13T00:00:00Z",
    )


def _redigest(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["acquisition_provider_evidence_execution_digest"] = (
        execution.acquisition_provider_evidence_execution_digest_v1(artifact)
    )
    return artifact


def test_execution_blocks_when_live_gate_is_missing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(execution.MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE, raising=False)
    artifact = execution.execute_acquisition_provider_evidence_v1(
        api_key="fictional-test-key",
        run_timestamp_utc="2026-08-13T00:00:00Z",
    )

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_BLOCKED
    assert artifact["execution_status"] == execution.ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING
    assert artifact["blocked_reason"] == "LIVE_GATE_MISSING"
    assert artifact["provider_requests_made"] is False
    assert artifact["acquisition_provider_evidence_execution_digest"] == "NOT_CREATED"


def test_execution_blocks_when_api_key_is_missing_for_real_transport(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(execution.MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE, "1")
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    artifact = execution.execute_acquisition_provider_evidence_v1(run_timestamp_utc="2026-08-13T00:00:00Z")

    assert artifact["execution_status"] == execution.ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING
    assert artifact["blocked_reason"] == "API_KEY_MISSING"
    assert artifact["generated_output_count"] == 0
    assert artifact["market_data_acquisition_performed"] is False


def test_execution_builds_performed_artifact_with_fake_transport(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED
    assert artifact["execution_status"] == execution.ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY
    for field in (
        "acquisition_provider_request_authorized",
        "ready_for_acquisition_provider_evidence_execution",
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "acquisition_provider_evidence_executed",
        "acquisition_provider_evidence_results_created",
    ):
        assert artifact[field] is True
    assert artifact["raw_provider_payloads_committed"] is False
    assert artifact["api_keys_stored_or_printed"] is False


def test_source_digest_chain_is_bound(tmp_path: Path):
    artifact = _executed(tmp_path)
    expected = {
        "acquisition_provider_evidence_request_approval_digest": execution.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_generation_chain_candidate_review_package_digest": execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST,
        "acquisition_generation_chain_candidate_digest": execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": execution.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": execution.EXPECTED_COMBINED_READINESS_REVIEW_DIGEST,
        "split_event_authority_freeze_digest": execution.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": execution.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": execution.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": execution.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
    }

    assert {field: artifact[field] for field in expected} == expected


def test_profile_universe_and_per_ticker_results_are_exact(tmp_path: Path):
    artifact = _executed(tmp_path)
    entries = artifact["per_ticker_acquisition_provider_evidence_results"]

    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == execution.TARGET_UNIVERSE
    assert [item["ticker"] for item in entries] == execution.TARGET_UNIVERSE
    assert artifact["date_range_start"] == "2022-01-01"
    assert artifact["date_range_end"] == "2025-12-31"
    assert artifact["timeframe"] == "1d"
    assert artifact["session_profile"] == "RTH_FULL_SESSION_1D"
    assert entries[0]["historical_bar_count"] == 2
    assert entries[1]["acquisition_provider_evidence_status"] == execution.NO_HISTORICAL_BARS_RETURNED_BY_PROVIDER


def test_digests_exist_without_raw_payload_or_api_key(tmp_path: Path):
    artifact = _executed(tmp_path)
    rendered = json.dumps(artifact, sort_keys=True)

    assert "fictional-test-key" not in rendered
    assert "provider_response_body" not in rendered
    for item in artifact["per_ticker_acquisition_provider_evidence_results"]:
        assert len(item["provider_response_digest"]) == 64
        assert len(item["sanitized_acquisition_evidence_digest"]) == 64
        assert item["raw_response_stored"] is False
        assert item["raw_payload_committed"] is False


def test_generated_outputs_are_seven_sanitized_files(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["generated_output_count"] == 7
    assert [item["filename"] for item in artifact["output_digest_manifest"]] == execution.OUTPUT_FILENAMES
    assert sorted(path.name for path in tmp_path.iterdir()) == sorted(execution.OUTPUT_FILENAMES)
    for filename in execution.OUTPUT_FILENAMES:
        payload = json.loads((tmp_path / filename).read_text(encoding="utf-8"))
        assert payload["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE
        assert payload["evidence_scope"] == execution.READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY
        assert payload["new_ticker_acquisition_authorized"] is False
        assert payload["dataset_generation_authorized"] is False
        assert payload["runtime_use"] == execution.NOT_AUTHORIZED


@pytest.mark.parametrize(
    "field,expected",
    [
        ("new_ticker_acquisition_authorized", False),
        ("acquisition_generation_authorized", False),
        ("acquisition_generation_executed", False),
        ("dataset_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("canonical_dataset_candidate_created", False),
        ("canonical_dataset_frozen", False),
        ("registry_approval_created", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", execution.NOT_ACCEPTED),
        ("profitability", execution.PROFITABILITY_NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_use", execution.NOT_AUTHORIZED),
        ("strategy_use", execution.NOT_AUTHORIZED),
        ("paper_trading", execution.NOT_AUTHORIZED),
        ("broker_execution", execution.NOT_AUTHORIZED),
        ("automatic_stitching", False),
    ],
)
def test_downstream_boundaries_remain_closed(tmp_path: Path, field: str, expected: Any):
    assert _executed(tmp_path)[field] == expected


def test_validator_accepts_valid_performed_artifact(tmp_path: Path):
    validation = execution.validate_acquisition_provider_evidence_executed_v1(_executed(tmp_path))

    assert validation["status"] == "ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_VALID"
    assert validation["failed_checks"] == 0
    assert validation["generated_output_count"] == 7


@pytest.mark.parametrize(
    "field,invalid",
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("acquisition_provider_request_authorized", False),
        ("ready_for_acquisition_provider_evidence_execution", False),
        ("provider_requests_made", False),
        ("live_provider_transport_enabled", False),
        ("market_data_acquisition_performed", False),
        ("acquisition_provider_evidence_executed", False),
        ("acquisition_provider_evidence_results_created", False),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(execution.TARGET_UNIVERSE))),
        ("generated_output_count", 6),
        ("new_ticker_acquisition_authorized", True),
        ("acquisition_generation_authorized", True),
        ("acquisition_generation_executed", True),
        ("dataset_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("canonical_dataset_candidate_created", True),
        ("canonical_dataset_frozen", True),
        ("registry_approval_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("acquisition_provider_evidence_request_approval_digest", None),
        ("acquisition_provider_evidence_execution_digest", None),
    ],
)
def test_validator_rejects_invalid_top_level_fields(tmp_path: Path, field: str, invalid: Any):
    artifact = deepcopy(_executed(tmp_path))
    artifact[field] = invalid
    if field != "acquisition_provider_evidence_execution_digest":
        _redigest(artifact)

    with pytest.raises(execution.AcquisitionProviderEvidenceExecutionError):
        execution.validate_acquisition_provider_evidence_executed_v1(artifact)


def test_validator_rejects_output_label_not_research_only(tmp_path: Path):
    artifact = deepcopy(_executed(tmp_path))
    artifact["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"
    _redigest(artifact)

    with pytest.raises(execution.AcquisitionProviderEvidenceExecutionError, match="output label"):
        execution.validate_acquisition_provider_evidence_executed_v1(artifact)


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_transport(tmp_path: Path):
    first = _executed(tmp_path / "one")
    second = _executed(tmp_path / "two")

    assert first["acquisition_provider_evidence_execution_digest"] == second["acquisition_provider_evidence_execution_digest"]


def test_status_markdown_includes_required_sections_and_boundaries(tmp_path: Path):
    markdown = execution.build_acquisition_provider_evidence_execution_status_markdown_v1(_executed(tmp_path))
    headings = (
        "## Title",
        "## Acquisition Provider Evidence Execution",
        "## Source Acquisition Provider Evidence Request Approval",
        "## Source Corporate-Action Authority Approval",
        "## Target Universe",
        "## Acquisition Profile",
        "## Provider Request Summary",
        "## Per-Ticker Acquisition Evidence Summary",
        "## Output Digest Manifest",
        "## Data Quality Summary",
        "## API Key and Raw Payload Boundary",
        "## Acquisition Authority Boundary",
        "## Dataset Boundary",
        "## Canonical Dataset Boundary",
        "## Registry Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    )

    assert all(heading in markdown for heading in headings)
    assert "fictional-test-key" not in markdown
    assert "NOT_AUTHORIZED" in markdown


def test_blocked_status_markdown_is_sanitized(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(execution.MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE, raising=False)
    artifact = execution.execute_acquisition_provider_evidence_v1(
        api_key="fictional-test-key",
        run_timestamp_utc="2026-08-13T00:00:00Z",
    )
    markdown = execution.build_acquisition_provider_evidence_execution_status_markdown_v1(artifact)

    assert execution.ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING in markdown
    assert "fictional-test-key" not in markdown
    assert "No generated outputs were created" in markdown


def test_public_services_exports_execution_api():
    assert services.execute_acquisition_provider_evidence_v1 is execution.execute_acquisition_provider_evidence_v1
    assert services.validate_acquisition_provider_evidence_executed_v1 is execution.validate_acquisition_provider_evidence_executed_v1
