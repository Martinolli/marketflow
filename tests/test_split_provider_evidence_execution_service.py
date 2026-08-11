from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import split_provider_evidence_execution_service as execution


def _fake_transport(request: dict[str, Any]) -> dict[str, Any]:
    ticker = dict(request["query_parameters"])["ticker"]
    events = []
    if ticker == "MSFT":
        events = [
            {
                "ticker": "MSFT",
                "execution_date": "2003-02-18",
                "split_from": 1,
                "split_to": 2,
                "id": "msft-split-2003",
            }
        ]
    return {"status": "OK", "results": events}


def _executed(tmp_path: Path) -> dict[str, Any]:
    return execution.execute_split_provider_evidence_v1(
        api_key="fictional-test-key",
        transport=_fake_transport,
        output_root=tmp_path,
        run_timestamp_utc="2026-08-11T00:00:00Z",
    )


def _with_digest(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["split_provider_evidence_execution_digest"] = (
        execution.split_provider_evidence_execution_digest_v1(artifact)
    )
    return artifact


def test_execution_blocks_when_live_gate_is_missing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(execution.MARKETFLOW_ENABLE_LIVE_SPLIT_PROVIDER_EVIDENCE, raising=False)
    artifact = execution.execute_split_provider_evidence_v1(
        api_key="fictional-test-key",
        run_timestamp_utc="2026-08-11T00:00:00Z",
    )

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_BLOCKED
    assert artifact["execution_status"] == (
        execution.SPLIT_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING
    )
    assert artifact["provider_requests_made"] is False
    assert artifact["live_provider_transport_enabled"] is False
    assert artifact["split_provider_evidence_execution_digest"] == "NOT_CREATED"


def test_execution_blocks_when_api_key_is_missing_for_real_transport(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(execution.MARKETFLOW_ENABLE_LIVE_SPLIT_PROVIDER_EVIDENCE, "1")
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)

    artifact = execution.execute_split_provider_evidence_v1(
        run_timestamp_utc="2026-08-11T00:00:00Z",
    )

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_BLOCKED
    assert artifact["blocked_reason"] == "API_KEY_MISSING"
    assert artifact["provider_requests_made"] is False


def test_execution_builds_performed_artifact_with_fake_transport(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_EXECUTED
    assert artifact["execution_status"] == execution.SPLIT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY
    assert artifact["split_provider_evidence_request_authorized"] is True
    assert artifact["provider_requests_made"] is True
    assert artifact["live_provider_transport_enabled"] is True
    assert artifact["split_provider_evidence_executed"] is True
    assert artifact["split_provider_evidence_results_created"] is True
    assert artifact["raw_provider_payloads_committed"] is False
    assert artifact["api_keys_stored_or_printed"] is False


def test_source_digest_chain_is_bound(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["split_provider_evidence_request_approval_digest"] == (
        execution.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
    )
    assert artifact["split_event_authority_candidate_review_package_digest"] == (
        execution.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["dividend_event_authority_candidate_review_package_digest"] == (
        execution.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["corporate_action_authority_plan_approval_digest"] == (
        execution.approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
    )


def test_target_universe_and_per_ticker_results_match_approval(tmp_path: Path):
    artifact = _executed(tmp_path)
    entries = artifact["per_ticker_split_provider_evidence_results"]

    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == execution.TARGET_UNIVERSE
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == execution.TARGET_UNIVERSE
    assert entries[0]["ticker"] == "MSFT"
    assert entries[0]["split_provider_evidence_status"] == (
        execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY
    )
    assert entries[0]["split_event_count"] == 1
    assert entries[1]["split_provider_evidence_status"] == (
        execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER
    )


def test_provider_and_sanitized_digests_are_recorded_without_raw_payloads(tmp_path: Path):
    artifact = _executed(tmp_path)
    rendered = json.dumps(artifact, sort_keys=True)

    assert "fictional-test-key" not in rendered
    for entry in artifact["per_ticker_split_provider_evidence_results"]:
        assert entry["raw_response_stored"] is False
        assert entry["raw_payload_committed"] is False
        assert entry["api_key_stored_or_printed"] is False
        assert len(entry["provider_response_digest"]) == 64
        assert len(entry["sanitized_split_evidence_digest"]) == 64


def test_generated_outputs_are_six_research_only_files(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["generated_output_count"] == 6
    assert len(artifact["output_digest_manifest"]) == 6
    assert [item["filename"] for item in artifact["output_digest_manifest"]] == (
        execution.OUTPUT_FILENAMES
    )
    for item in artifact["output_digest_manifest"]:
        path = tmp_path / item["filename"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE
        assert payload["evidence_scope"] == (
            execution.READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY
        )
        assert payload["split_event_authority_created"] is False
        assert payload["corporate_action_authority_created"] is False
        assert payload["new_ticker_acquisition_authorized"] is False
        assert payload["dataset_generation_authorized"] is False
        assert payload["runtime_use"] == execution.NOT_AUTHORIZED
        assert item["sha256"] == execution.sha256_bytes(path.read_bytes())


def test_authority_predictive_profitability_and_runtime_boundaries_remain_closed(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["split_event_authority_created"] is False
    assert artifact["split_event_authority_frozen"] is False
    assert artifact["dividend_provider_evidence_request_authorized"] is False
    assert artifact["dividend_event_authority_created"] is False
    assert artifact["corporate_action_authority_created"] is False
    assert artifact["new_ticker_acquisition_authorized"] is False
    assert artifact["dataset_generation_authorized"] is False
    assert artifact["additional_predictive_evidence_execution_authorized"] is False
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_migration_approved"] is False
    assert artifact["runtime_use"] == execution.NOT_AUTHORIZED
    assert artifact["strategy_use"] == execution.NOT_AUTHORIZED
    assert artifact["paper_trading"] == execution.NOT_AUTHORIZED
    assert artifact["broker_execution"] == execution.NOT_AUTHORIZED


def test_validator_accepts_valid_performed_artifact(tmp_path: Path):
    artifact = _executed(tmp_path)
    validation = execution.validate_split_provider_evidence_executed_v1(artifact)

    assert validation["status"] == "SPLIT_PROVIDER_EVIDENCE_EXECUTED_VALID"
    assert validation["provider_request_count"] == 12
    assert validation["successful_provider_response_count"] == 12
    assert validation["generated_output_count"] == 6
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("execution_status", "WRONG", "execution_status"),
        ("split_provider_evidence_request_authorized", False, "split_provider_evidence_request_authorized"),
        ("provider_requests_made", False, "provider_requests_made"),
        ("live_provider_transport_enabled", False, "live_provider_transport_enabled"),
        ("split_provider_evidence_executed", False, "split_provider_evidence_executed"),
        ("split_provider_evidence_results_created", False, "split_provider_evidence_results_created"),
        ("raw_provider_payloads_committed", True, "raw_provider_payloads_committed"),
        ("api_keys_stored_or_printed", True, "api_keys_stored_or_printed"),
        ("target_universe_count", 11, "target_universe_count"),
        ("target_universe", execution.TARGET_UNIVERSE[:-1], "target_universe"),
        ("generated_output_count", 5, "generated_output_count"),
        ("split_event_authority_created", True, "split_event_authority_created"),
        ("split_event_authority_frozen", True, "split_event_authority_frozen"),
        ("dividend_provider_evidence_request_authorized", True, "dividend_provider_evidence_request_authorized"),
        ("dividend_event_authority_created", True, "dividend_event_authority_created"),
        ("corporate_action_authority_created", True, "corporate_action_authority_created"),
        ("new_ticker_acquisition_authorized", True, "new_ticker_acquisition_authorized"),
        ("dataset_generation_authorized", True, "dataset_generation_authorized"),
        ("additional_predictive_evidence_execution_authorized", True, "additional_predictive_evidence_execution_authorized"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
        ("split_provider_evidence_request_approval_digest", None, "split_provider_evidence_request_approval_digest"),
        ("split_provider_evidence_execution_digest", None, "split_provider_evidence_execution_digest"),
    ],
)
def test_validator_rejects_invalid_top_level_fields(
    tmp_path: Path, field: str, value: Any, match: str
):
    artifact = _executed(tmp_path)
    artifact[field] = value
    if field != "split_provider_evidence_execution_digest":
        _with_digest(artifact)

    with pytest.raises(execution.SplitProviderEvidenceExecutionError, match=match):
        execution.validate_split_provider_evidence_executed_v1(artifact)


def test_validator_rejects_output_label_not_research_only(tmp_path: Path):
    artifact = _executed(tmp_path)
    artifact["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"
    _with_digest(artifact)

    with pytest.raises(execution.SplitProviderEvidenceExecutionError, match="output label"):
        execution.validate_split_provider_evidence_executed_v1(artifact)


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_fake_transport(tmp_path: Path):
    first = _executed(tmp_path)
    second = _executed(tmp_path)

    assert first["split_provider_evidence_execution_digest"] == (
        second["split_provider_evidence_execution_digest"]
    )


def test_status_markdown_includes_required_sections_and_boundaries(tmp_path: Path):
    markdown = execution.build_split_provider_evidence_execution_status_markdown_v1(
        _executed(tmp_path)
    )

    for heading in (
        "# MarketFlow Split Provider Evidence Execution Status",
        "## Execution Artifact",
        "## Source Evidence",
        "## Endpoint And Mode",
        "## Per-Ticker Sanitized Split Evidence Summary",
        "## API Key And Raw Payload Boundary",
        "## Authority Boundaries",
        "## Non-Goals",
        "## Next Task",
    ):
        assert heading in markdown
    assert "split_event_authority_created: `False`" in markdown
    assert "broker_execution: `NOT_AUTHORIZED`" in markdown
    assert "No split authority approval or freeze is created." in markdown


def test_blocked_status_markdown_is_sanitized(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(execution.MARKETFLOW_ENABLE_LIVE_SPLIT_PROVIDER_EVIDENCE, raising=False)
    artifact = execution.execute_split_provider_evidence_v1(
        api_key="fictional-test-key",
        run_timestamp_utc="2026-08-11T00:00:00Z",
    )
    markdown = execution.build_split_provider_evidence_execution_status_markdown_v1(artifact)

    assert execution.SPLIT_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING in markdown
    assert "fictional-test-key" not in markdown
    assert "No generated outputs were created" in markdown


@pytest.mark.skipif(
    os.environ.get(execution.MARKETFLOW_ENABLE_LIVE_SPLIT_PROVIDER_EVIDENCE) != "1"
    or not (os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")),
    reason="live split provider evidence smoke requires explicit gate and provider API key",
)
def test_optional_live_split_provider_evidence_execution_smoke(tmp_path: Path):
    artifact = execution.execute_split_provider_evidence_v1(output_root=tmp_path)

    assert artifact["provider_requests_made"] is True
    assert artifact["split_provider_evidence_executed"] is True
    assert artifact["generated_output_count"] == 6


def test_public_services_exports_execution_api():
    assert services.execute_split_provider_evidence_v1 is execution.execute_split_provider_evidence_v1
    assert services.validate_split_provider_evidence_executed_v1 is (
        execution.validate_split_provider_evidence_executed_v1
    )
