from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import live_ticker_validation_execution_service as execution


FIXED_TIMESTAMP = "2026-08-09T00:00:00Z"
EXPECTED_EXECUTION_DIGEST = ""


def _provider_payload(ticker: str) -> dict[str, Any]:
    return {
        "status": "OK",
        "results": {
            "ticker": ticker,
            "name": f"{ticker} Corporation",
            "market": "stocks",
            "locale": "us",
            "primary_exchange": "XNAS",
            "type": "CS",
            "active": True,
            "currency_name": "usd",
            "composite_figi": f"BBG{ticker}",
            "share_class_figi": f"BBG{ticker}SHARE",
        },
    }


def _transport(request):
    return _provider_payload(request["provider_query_ticker"])


def _executed(tmp_path: Path, **overrides: Any) -> dict[str, Any]:
    values = {
        "api_key": "fictional-secret-key",
        "transport": _transport,
        "output_root": tmp_path / "validation_outputs",
        "run_timestamp_utc": FIXED_TIMESTAMP,
    }
    values.update(overrides)
    return execution.execute_live_ticker_validation_v1(**values)


def _redigest(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["live_ticker_validation_execution_digest"] = (
        execution.live_ticker_validation_execution_digest_v1(artifact)
    )
    return artifact


def test_execution_blocks_when_live_gate_is_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.delenv(execution.provider.LIVE_TICKER_VALIDATION_GATE_ENV, raising=False)
    artifact = execution.execute_live_ticker_validation_v1(
        output_root=tmp_path / "blocked",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == execution.LIVE_TICKER_VALIDATION_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING
    assert artifact["provider_requests_made"] is False
    assert artifact["live_provider_transport_enabled"] is False
    assert artifact["live_ticker_validation_performed"] is False
    assert artifact["live_validation_results_created"] is False


def test_execution_blocks_when_api_key_is_missing_for_real_transport(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv(execution.provider.LIVE_TICKER_VALIDATION_GATE_ENV, "1")
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)

    artifact = execution.execute_live_ticker_validation_v1(
        output_root=tmp_path / "blocked",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == execution.LIVE_TICKER_VALIDATION_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING
    assert artifact["blocker_reason"] == "api key missing"
    assert artifact["provider_requests_made"] is False


def test_execution_builds_performed_artifact_with_fake_transport(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED
    assert artifact["execution_status"] == execution.LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY
    assert artifact["provider_request_authorized"] is True
    assert artifact["provider_requests_made"] is True
    assert artifact["live_provider_transport_enabled"] is True
    assert artifact["live_ticker_validation_authorized"] is True
    assert artifact["live_ticker_validation_performed"] is True
    assert artifact["live_validation_results_created"] is True
    assert artifact["raw_provider_payloads_committed"] is False
    assert artifact["api_keys_stored_or_printed"] is False


def test_source_digests_are_bound(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["live_ticker_validation_approval_digest"] == execution.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
    assert artifact["live_ticker_validation_candidate_digest"] == execution.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
    assert artifact["live_ticker_validation_candidate_review_package_digest"] == (
        execution.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["ticker_universe_selection_approval_digest"] == (
        execution.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_validation_target_universe_is_exact_and_has_results(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["validation_target_universe"] == [
        "MSFT",
        "NVDA",
        "AMZN",
        "GOOGL",
        "META",
        "TSLA",
        "JPM",
        "XOM",
        "JNJ",
        "WMT",
        "CAT",
        "LMT",
    ]
    assert artifact["validation_target_count"] == 12
    assert [item["ticker"] for item in artifact["per_ticker_results"]] == artifact["validation_target_universe"]


def test_per_ticker_results_record_digests_without_raw_payloads(tmp_path: Path):
    artifact = _executed(tmp_path)

    for item in artifact["per_ticker_results"]:
        assert item["provider_request_status"] == execution.PROVIDER_RESPONSE_AVAILABLE
        assert item["live_validation_status"] == execution.VALIDATED_READ_ONLY
        assert len(item["provider_response_digest"]) == 64
        assert len(item["sanitized_validation_digest"]) == 64
        assert item["raw_response_stored"] is False
        assert item["raw_payload_committed"] is False
        assert item["api_key_stored_or_printed"] is False


def test_generated_outputs_and_digest_manifest_are_written(tmp_path: Path):
    output_root = tmp_path / "outputs"
    artifact = _executed(tmp_path, output_root=output_root)

    assert artifact["generated_output_count"] == 6
    assert [item["output_name"] for item in artifact["output_digest_manifest"]] == execution.GENERATED_OUTPUT_NAMES
    for item in artifact["output_digest_manifest"]:
        assert (output_root / item["output_name"]).exists()
        assert item["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE
        assert item["raw_provider_payloads_included"] is False


def test_execution_records_provider_failures_without_fabricated_response_digest(tmp_path: Path):
    def failing_transport(request):
        if request["provider_query_ticker"] == "MSFT":
            return {"status": "ERROR", "results": []}
        return _provider_payload(request["provider_query_ticker"])

    artifact = _executed(tmp_path, transport=failing_transport)

    first = artifact["per_ticker_results"][0]
    assert first["ticker"] == "MSFT"
    assert first["provider_request_status"] == execution.PROVIDER_RESPONSE_FAILED
    assert first["live_validation_status"] == execution.PROVIDER_RESPONSE_UNAVAILABLE
    assert first["provider_response_digest"] is None
    assert first["failure_reason_if_any"]
    assert artifact["failed_provider_response_count"] == 1
    assert artifact["failure_count"] == 1
    assert execution.validate_live_ticker_validation_performed_v1(artifact)["failed_provider_response_count"] == 1


@pytest.mark.parametrize(
    "field",
    [
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_downstream_authority_flags_remain_false(tmp_path: Path, field: str):
    assert _executed(tmp_path)[field] is False


def test_predictive_profitability_runtime_and_execution_boundaries_remain_closed(tmp_path: Path):
    artifact = _executed(tmp_path)

    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_use"] == execution.NOT_AUTHORIZED
    assert artifact["strategy_use"] == execution.NOT_AUTHORIZED
    assert artifact["paper_trading"] == execution.NOT_AUTHORIZED
    assert artifact["broker_execution"] == execution.NOT_AUTHORIZED
    assert artifact["trade_recommendations_generated"] is False


def test_validator_accepts_valid_performed_artifact(tmp_path: Path):
    artifact = _executed(tmp_path)

    validation = execution.validate_live_ticker_validation_performed_v1(artifact)

    assert validation["status"] == "LIVE_TICKER_VALIDATION_PERFORMED_VALID"
    assert validation["provider_request_count"] == 12


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("execution_status", "WRONG", "execution_status"),
        ("provider_request_authorized", False, "provider_request_authorized"),
        ("provider_requests_made", False, "provider_requests_made"),
        ("live_provider_transport_enabled", False, "live_provider_transport_enabled"),
        ("live_ticker_validation_performed", False, "live_ticker_validation_performed"),
        ("live_validation_results_created", False, "live_validation_results_created"),
        ("raw_provider_payloads_committed", True, "raw_provider_payloads_committed"),
        ("api_keys_stored_or_printed", True, "api_keys_stored_or_printed"),
        ("validation_target_count", 11, "validation_target_count"),
        ("validation_target_universe", ["MSFT"], "validation_target_universe"),
        ("generated_output_count", 5, "generated_output_count"),
        ("new_ticker_authority_created", True, "new_ticker_authority_created"),
        ("new_ticker_acquisition_authorized", True, "new_ticker_acquisition_authorized"),
        ("dataset_generation_authorized", True, "dataset_generation_authorized"),
        ("additional_predictive_evidence_execution_authorized", True, "additional_predictive_evidence_execution_authorized"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
    ],
)
def test_validator_rejects_guardrail_violations(tmp_path: Path, field: str, value: Any, match: str):
    artifact = _executed(tmp_path)
    artifact[field] = value

    with pytest.raises(execution.LiveTickerValidationExecutionError, match=match):
        execution.validate_live_ticker_validation_performed_v1(artifact)


def test_validator_rejects_output_labels_not_research_only(tmp_path: Path):
    artifact = _executed(tmp_path)
    artifact["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"
    _redigest(artifact)

    with pytest.raises(execution.LiveTickerValidationExecutionError, match="output labels"):
        execution.validate_live_ticker_validation_performed_v1(artifact)


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_fake_transport(tmp_path: Path):
    output_root = tmp_path / "same"
    first = _executed(tmp_path, output_root=output_root)
    second = _executed(tmp_path, output_root=output_root)

    assert first["live_ticker_validation_execution_digest"] == second["live_ticker_validation_execution_digest"]


def test_status_markdown_includes_required_sections_and_boundaries(tmp_path: Path):
    artifact = _executed(tmp_path)
    markdown = execution.build_live_ticker_validation_execution_status_markdown_v1(artifact)

    assert "## Execution Artifact" in markdown
    assert "## Selected Endpoint And Mode" in markdown
    assert "## API Key / Raw Payload Boundary" in markdown
    assert "## Authority Boundaries" in markdown
    assert "Live ticker validation results operator review package" in markdown
    assert "fictional-secret-key" not in markdown
    assert "raw provider payloads are not included" in markdown


def test_services_package_exports_execution_helpers():
    assert services.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED == (
        execution.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED
    )
    assert services.LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY == (
        execution.LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY
    )
    assert services.execute_live_ticker_validation_v1 is execution.execute_live_ticker_validation_v1
