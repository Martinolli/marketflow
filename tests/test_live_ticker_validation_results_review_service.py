from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import live_ticker_validation_results_review_service as review


def _boundary(report_name: str) -> dict[str, Any]:
    return {
        "report_name": report_name,
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "validation_scope": review.READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_use": review.NOT_AUTHORIZED,
        "strategy_use": review.NOT_AUTHORIZED,
        "paper_trading": review.NOT_AUTHORIZED,
        "broker_execution": review.NOT_AUTHORIZED,
        "predictive_usefulness": review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": review.acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def _ticker_result(ticker: str) -> dict[str, Any]:
    return {
        "ticker": ticker,
        "provider_request_status": review.PROVIDER_RESPONSE_AVAILABLE,
        "live_validation_status": review.VALIDATED_READ_ONLY,
        "listing_status": review.VALIDATED_READ_ONLY,
        "security_type_status": review.VALIDATED_READ_ONLY,
        "exchange_status": review.VALIDATED_READ_ONLY,
        "active_status": review.VALIDATED_READ_ONLY,
        "delisting_status": review.VALIDATED_READ_ONLY,
        "tradability_status": review.VALIDATED_READ_ONLY,
        "provider_symbol_mapping_status": review.VALIDATED_READ_ONLY,
        "corporate_action_data_availability_status": review.NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "historical_aggregate_data_availability_status": review.NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "identity_authority_status": "NOT_CREATED",
        "split_event_authority_status": "NOT_CREATED",
        "dividend_event_authority_status": "NOT_CREATED",
        "acquisition_authority_status": "NOT_CREATED",
        "canonical_dataset_authority_status": "NOT_CREATED",
        "registry_approval_status": "NOT_CREATED",
        "research_use_status": review.NOT_AUTHORIZED,
        "runtime_use": review.NOT_AUTHORIZED,
        "strategy_use": review.NOT_AUTHORIZED,
        "paper_trading": review.NOT_AUTHORIZED,
        "broker_execution": review.NOT_AUTHORIZED,
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
        "provider_response_digest": "a" * 64,
        "sanitized_validation_digest": "b" * 64,
        "failure_reason_if_any": None,
    }


def _fixture_outputs(output_root: Path) -> dict[str, str]:
    results = [_ticker_result(ticker) for ticker in review.VALIDATION_TARGET_UNIVERSE]
    outputs = {
        "live_ticker_validation_run_manifest.json": _boundary("live_ticker_validation_run_manifest")
        | {
            "schema_version": "live_ticker_validation_performed_v1",
            "run_timestamp_utc": "2026-08-09T19:59:06Z",
            "selected_endpoint": review.provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE,
            "selected_endpoint_mode": review.provider.SELECTED_ENDPOINT_MODE,
            "validation_target_universe": list(review.VALIDATION_TARGET_UNIVERSE),
            "source_approval_digest": review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
            "raw_provider_payloads_included": False,
        },
        "ticker_validation_results.json": _boundary("ticker_validation_results")
        | {"results": results, "raw_provider_payloads_included": False},
        "provider_request_receipts_sanitized.json": _boundary("provider_request_receipts_sanitized")
        | {
            "provider_request_receipts": [
                {
                    "ticker": ticker,
                    "provider_response_status": review.PROVIDER_RESPONSE_AVAILABLE,
                    "raw_response_stored": False,
                    "raw_payload_committed": False,
                    "api_key_stored_or_printed": False,
                }
                for ticker in review.VALIDATION_TARGET_UNIVERSE
            ],
            "raw_provider_payloads_included": False,
        },
        "validation_summary.json": _boundary("validation_summary")
        | {
            "validation_target_count": 12,
            "provider_request_count": 12,
            "successful_provider_response_count": 12,
            "failed_provider_response_count": 0,
            "validated_read_only_count": 12,
            "validation_failed_count": 0,
            "not_evaluated_count": 24,
            "generated_output_root": output_root.as_posix(),
            "generated_output_count": 6,
            "output_digest_manifest": [],
            "failure_count": 0,
            "warning_count": 24,
        },
        "validation_failure_reason_inventory.json": _boundary("validation_failure_reason_inventory")
        | {"failure_count": 0, "failures": []},
        "operator_review_summary.json": _boundary("operator_review_summary")
        | {
            "operator_review_status": "LIVE_TICKER_VALIDATION_RESULTS_REVIEW_REQUIRED",
            "next_task": "live ticker validation results operator review package",
            "predictive_usefulness_acceptance_ready": False,
            "profitability_acceptance_ready": False,
            "runtime_migration_approved": False,
        },
    }
    return {name: _write_json(output_root / name, payload) for name, payload in outputs.items()}


def _package(tmp_path: Path) -> dict[str, Any]:
    output_root = tmp_path / "outputs"
    _fixture_outputs(output_root)
    return review.build_live_ticker_validation_results_review_package_v1(output_root=output_root)


def _mutated_package(tmp_path: Path, field: str, value: Any) -> dict[str, Any]:
    package = _package(tmp_path)
    package[field] = value
    return package


def test_review_package_builds_offline_without_provider_calls(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.provider, "fetch_massive_ticker_details_v1", fail_provider_call)

    package = _package(tmp_path)

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["live_validation_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_review"] is False


def test_artifact_kind_and_ready_status_when_fixture_outputs_are_valid(tmp_path: Path):
    package = _package(tmp_path)

    assert package["artifact_kind"] == review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE
    assert package["review_status"] == review.LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY


def test_review_status_is_blocked_when_outputs_are_missing(tmp_path: Path):
    package = review.build_live_ticker_validation_results_review_package_v1(
        output_root=tmp_path / "missing"
    )

    assert package["review_status"] == review.LIVE_TICKER_VALIDATION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS
    assert package["actual_output_count"] == 0
    assert package["output_file_inspection_performed"] is False


def test_source_digests_are_bound(tmp_path: Path):
    package = _package(tmp_path)

    assert package["source_execution_digest"] == review.EXPECTED_SOURCE_EXECUTION_DIGEST
    assert package["source_execution_approval_digest"] == review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
    assert package["live_ticker_validation_candidate_digest"] == review.EXPECTED_SOURCE_CANDIDATE_DIGEST
    assert package["live_ticker_validation_candidate_review_package_digest"] == (
        review.EXPECTED_SOURCE_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["ticker_universe_selection_approval_digest"] == (
        review.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_endpoint_universe_and_provider_counts_are_recorded(tmp_path: Path):
    package = _package(tmp_path)

    assert package["selected_endpoint"] == review.provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE
    assert package["selected_endpoint_mode"] == review.provider.SELECTED_ENDPOINT_MODE
    assert package["validation_target_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["validation_target_count"] == 12
    assert package["provider_request_count"] == 12
    assert package["successful_provider_response_count"] == 12
    assert package["failed_provider_response_count"] == 0


def test_all_targets_validated_read_only_and_not_evaluated_count_is_24(tmp_path: Path):
    package = _package(tmp_path)

    assert package["all_targets_validated_read_only"] is True
    assert package["validated_read_only_count"] == 12
    assert package["not_evaluated_count"] == 24
    for item in package["per_ticker_validation_summary"]:
        assert item["live_validation_status"] == review.VALIDATED_READ_ONLY
        assert item["corporate_action_data_availability_status"] == (
            review.NOT_EVALUATED_BY_SELECTED_ENDPOINT
        )
        assert item["historical_aggregate_data_availability_status"] == (
            review.NOT_EVALUATED_BY_SELECTED_ENDPOINT
        )


def test_generated_outputs_and_digests_are_bound(tmp_path: Path):
    package = _package(tmp_path)

    assert package["generated_output_count"] == 6
    assert package["actual_output_count"] == 6
    assert [item["output_name"] for item in package["output_digest_manifest"]] == (
        review.EXPECTED_OUTPUT_NAMES
    )
    assert all(item["sha256_digest"] for item in package["output_digest_manifest"])
    assert all(item["semantic_digest"] for item in package["output_digest_manifest"])
    assert package["all_outputs_research_only_non_actionable"] is True
    assert package["all_outputs_scope_read_only"] is True


@pytest.mark.parametrize(
    "field",
    [
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
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
        "validation_creates_new_ticker_authority",
        "validation_creates_acquisition_authority",
        "validation_creates_dataset_generation_authority",
        "validation_creates_predictive_evidence_authority",
    ],
)
def test_closed_boolean_boundaries_remain_false(tmp_path: Path, field: str):
    assert _package(tmp_path)[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed(tmp_path: Path):
    package = _package(tmp_path)

    assert package["predictive_usefulness"] == review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert package["runtime_use"] == review.NOT_AUTHORIZED
    assert package["strategy_use"] == review.NOT_AUTHORIZED
    assert package["paper_trading"] == review.NOT_AUTHORIZED
    assert package["broker_execution"] == review.NOT_AUTHORIZED
    assert package["validation_supports_future_authority_chain_planning"] is True


def test_limitations_next_gates_and_checklist_are_complete(tmp_path: Path):
    package = _package(tmp_path)

    assert package["limitations"] == review.REQUIRED_LIMITATIONS
    assert package["next_gates"] == review.NEXT_GATES
    assert [item["check_id"] for item in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert {item["status"] for item in package["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_and_blockers(tmp_path: Path):
    summary = _package(tmp_path)["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_per_ticker_identity_authority_candidate"] is False
    assert summary["ready_for_acquisition"] is False
    assert summary["ready_for_dataset_generation"] is False
    assert summary["ready_for_additional_predictive_evidence_execution_candidate"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic(tmp_path: Path):
    first = _package(tmp_path)
    second = review.build_live_ticker_validation_results_review_package_v1(
        output_root=tmp_path / "outputs"
    )

    assert first["live_ticker_validation_results_review_package_digest"] == (
        second["live_ticker_validation_results_review_package_digest"]
    )
    assert first["live_ticker_validation_results_review_package_digest"] == (
        review.live_ticker_validation_results_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_review_package(tmp_path: Path):
    validation = review.validate_live_ticker_validation_results_review_package_v1(
        _package(tmp_path)
    )

    assert validation["status"] == "LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_VALID"
    assert validation["review_status"] == review.LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("source_execution_digest", "0" * 64, "source_execution_digest"),
        ("source_execution_approval_digest", "0" * 64, "source_execution_approval_digest"),
        ("validation_target_count", 11, "validation_target_count"),
        ("provider_request_count", 11, "provider_request_count"),
        ("successful_provider_response_count", 11, "successful_provider_response_count"),
        ("failed_provider_response_count", 1, "failed_provider_response_count"),
        ("validated_read_only_count", 11, "validated_read_only_count"),
        ("generated_output_count", 5, "generated_output_count"),
        ("all_outputs_research_only_non_actionable", False, "all_outputs_research_only_non_actionable"),
        ("raw_provider_payloads_committed", True, "raw_provider_payloads_committed"),
        ("api_keys_stored_or_printed", True, "api_keys_stored_or_printed"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("live_validation_rerun_performed", True, "live_validation_rerun_performed"),
        ("live_provider_transport_enabled_in_review", True, "live_provider_transport_enabled_in_review"),
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
        ("validation_creates_new_ticker_authority", True, "validation_creates_new_ticker_authority"),
        ("validation_creates_acquisition_authority", True, "validation_creates_acquisition_authority"),
        ("validation_creates_dataset_generation_authority", True, "validation_creates_dataset_generation_authority"),
        ("validation_creates_predictive_evidence_authority", True, "validation_creates_predictive_evidence_authority"),
        ("limitations", [], "limitations"),
        ("next_gates", [], "next_gates"),
    ],
)
def test_validator_rejects_invalid_review_package_mutations(
    tmp_path: Path,
    field: str,
    value: Any,
    match: str,
):
    package = _mutated_package(tmp_path, field, value)

    with pytest.raises(review.LiveTickerValidationResultsReviewError, match=match):
        review.validate_live_ticker_validation_results_review_package_v1(package)


def test_validator_rejects_missing_review_package_digest(tmp_path: Path):
    package = _package(tmp_path)
    package.pop("live_ticker_validation_results_review_package_digest")

    with pytest.raises(
        review.LiveTickerValidationResultsReviewError,
        match="live_ticker_validation_results_review_package_digest",
    ):
        review.validate_live_ticker_validation_results_review_package_v1(package)


def test_validator_rejects_ready_status_while_outputs_are_missing(tmp_path: Path):
    package = review.build_live_ticker_validation_results_review_package_v1(
        output_root=tmp_path / "missing"
    )
    package["review_status"] = review.LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY

    with pytest.raises(review.LiveTickerValidationResultsReviewError, match="missing_output_count"):
        review.validate_live_ticker_validation_results_review_package_v1(package)


def test_validator_rejects_output_labels_not_research_only(tmp_path: Path):
    package = _package(tmp_path)
    package["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"

    with pytest.raises(review.LiveTickerValidationResultsReviewError, match="output_label"):
        review.validate_live_ticker_validation_results_review_package_v1(package)


def test_markdown_writer_includes_required_sections(tmp_path: Path):
    markdown = review.build_live_ticker_validation_results_review_markdown_v1(_package(tmp_path))

    for section in (
        "## Title",
        "## Reviewed Live Ticker Validation Execution",
        "## Source Evidence",
        "## Validation Target Universe",
        "## Provider Request Summary",
        "## Per-Ticker Validation Summary",
        "## Output Digest Manifest",
        "## Limitations",
        "## Next Gates",
        "## Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_results_review_package_writes_json_without_overwrite(tmp_path: Path):
    output_root = tmp_path / "outputs"
    _fixture_outputs(output_root)

    result = review.write_live_ticker_validation_results_review_package_v1(
        tmp_path / "review",
        output_root=output_root,
    )

    assert result["artifact_kind"] == (
        review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE
    )
    assert result["payload_sha256"]
    written = json.loads((tmp_path / "review" / result["filename"]).read_text(encoding="utf-8"))
    assert written["artifact_kind"] == review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE
    with pytest.raises(review.LiveTickerValidationResultsReviewError, match="already exists"):
        review.write_live_ticker_validation_results_review_package_v1(
            tmp_path / "review",
            output_root=output_root,
        )


def test_services_package_exports_results_review_helpers():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE
    )
    assert services.LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY == (
        review.LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY
    )
    assert services.build_live_ticker_validation_results_review_package_v1 is (
        review.build_live_ticker_validation_results_review_package_v1
    )
    assert services.validate_live_ticker_validation_results_review_package_v1 is (
        review.validate_live_ticker_validation_results_review_package_v1
    )
    assert services.write_live_ticker_validation_results_review_package_v1 is (
        review.write_live_ticker_validation_results_review_package_v1
    )
    assert services.build_live_ticker_validation_results_review_markdown_v1 is (
        review.build_live_ticker_validation_results_review_markdown_v1
    )
