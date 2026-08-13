from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import acquisition_evidence_results_review_service as review


def _base_output() -> dict[str, Any]:
    return {
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": review.READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "runtime_use": review.NOT_AUTHORIZED,
        "strategy_use": review.NOT_AUTHORIZED,
        "paper_trading": review.NOT_AUTHORIZED,
        "broker_execution": review.NOT_AUTHORIZED,
        "predictive_usefulness": review.NOT_ACCEPTED,
        "profitability": review.PROFITABILITY_NOT_ACCEPTED,
    }


def _per_ticker_rows() -> list[dict[str, Any]]:
    rows = []
    for index, ticker in enumerate(review.EXPECTED_TARGET_UNIVERSE):
        status, count = review.EXPECTED_PER_TICKER[ticker]
        rows.append(
            {
                "ticker": ticker,
                "acquisition_provider_evidence_status": status,
                "historical_bar_count": count,
                "date_range_start": "2022-01-03",
                "date_range_end": "2025-12-31",
                "coverage_status": "OBSERVED_BAR_RANGE_RECORDED",
                "ohlc_status": "AVAILABLE",
                "volume_status": "AVAILABLE",
                "calendar_alignment_status": "NOT_EVALUATED_BY_SELECTED_ENDPOINT",
                "session_filter_status": "NOT_EVALUATED_BY_SELECTED_ENDPOINT",
                "adjustment_policy_status": "PROVIDER_ADJUSTED_TRUE_COMBINED_POLICY_NOT_DISAGGREGATED",
                "not_evaluated_fields": [
                    "trading_calendar_alignment_status",
                    "session_filter_status",
                    "split_adjustment_policy_binding",
                    "dividend_adjustment_policy_binding",
                ],
                "provider_response_digest": f"{index:064x}",
                "sanitized_acquisition_evidence_digest": f"{index + 20:064x}",
                "raw_response_stored": False,
                "raw_payload_committed": False,
                "api_key_stored_or_printed": False,
                "new_ticker_acquisition_authorized": False,
                "acquisition_generation_authorized": False,
                "acquisition_generation_executed": False,
                "dataset_generation_authorized": False,
                "canonical_dataset_authorized": False,
                "canonical_dataset_candidate_created": False,
                "canonical_dataset_frozen": False,
                "registry_approval_created": False,
            }
        )
    return rows


def _write_fixture_outputs(root: Path) -> dict[str, str]:
    root.mkdir(parents=True, exist_ok=True)
    base = _base_output()
    summary = {
        "target_count": 12,
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "timeframe": "1d",
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "historical_bar_evidence_collected_count": 12,
        "no_historical_bars_returned_count": 0,
        "not_evaluated_count": 12,
        "generated_output_count": 7,
        "failure_count": 0,
        "warning_count": 12,
    }
    quality = [
        {
            "ticker": ticker,
            "historical_bar_count": review.EXPECTED_PER_TICKER[ticker][1],
            "coverage_status": "OBSERVED_BAR_RANGE_RECORDED",
            "ohlc_status": "AVAILABLE",
            "volume_status": "AVAILABLE",
            "timestamp_status": "AVAILABLE",
            "not_evaluated_fields": ["trading_calendar_alignment_status", "session_filter_status"],
        }
        for ticker in review.EXPECTED_TARGET_UNIVERSE
    ]
    payloads = {
        "acquisition_provider_evidence_run_manifest.json": base | {
            "artifact_kind": review.execution.ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED,
            "execution_status": review.execution.ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
            "selected_endpoint": review.EXPECTED_RESULT_FACTS["endpoint"],
            "acquisition_profile": {
                "date_range_start": "2022-01-01",
                "date_range_end": "2025-12-31",
                "timeframe": "1d",
                "session_profile": "RTH_FULL_SESSION_1D",
            },
            "target_universe": review.EXPECTED_TARGET_UNIVERSE,
            "execution_summary": summary,
        },
        "acquisition_provider_request_receipts_sanitized.json": base | {
            "request_receipts_sanitized": [{"ticker": ticker} for ticker in review.EXPECTED_TARGET_UNIVERSE]
        },
        "acquisition_evidence_results_sanitized.json": base | {
            "per_ticker_acquisition_evidence_results": _per_ticker_rows()
        },
        "acquisition_data_quality_summary.json": base | {"acquisition_data_quality_summary": quality},
        "acquisition_failure_reason_inventory.json": base | {"acquisition_failure_reason_inventory": []},
        "operator_review_summary.json": base | {
            "operator_review_required": True,
            "provider_evidence_is_dataset_authority": False,
            "execution_summary": summary,
        },
    }
    digests: dict[str, str] = {}
    for filename, payload in payloads.items():
        data = canonical_json_bytes(payload)
        (root / filename).write_bytes(data)
        digests[filename] = review.sha256_bytes(data)
    internal_rows = [
        {
            "filename": filename,
            "sha256": digests[filename],
            "semantic_digest": review.semantic_digest(payloads[filename]),
            "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
            "relative_path": filename,
        }
        for filename in review.EXPECTED_OUTPUT_FILENAMES
        if filename != "acquisition_digest_manifest.json"
    ]
    manifest_payload = base | {"output_digests": internal_rows}
    manifest_data = canonical_json_bytes(manifest_payload)
    (root / "acquisition_digest_manifest.json").write_bytes(manifest_data)
    digests["acquisition_digest_manifest.json"] = review.sha256_bytes(manifest_data)
    return {filename: digests[filename] for filename in review.EXPECTED_OUTPUT_FILENAMES}


def _package(tmp_path: Path) -> dict[str, Any]:
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    return review.build_acquisition_evidence_results_review_package_v1(
        output_root=root,
        expected_output_digests=digests,
    )


def _redigest(package: dict[str, Any]) -> None:
    package["acquisition_evidence_results_review_package_digest"] = (
        review.acquisition_evidence_results_review_package_digest_v1(package)
    )


def test_review_builds_offline_without_provider_calls(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    def fail(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider execution must not be called")

    monkeypatch.setattr(review.execution, "execute_acquisition_provider_evidence_v1", fail)
    package = _package(tmp_path)

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["live_provider_transport_enabled_in_review"] is False
    assert package["market_data_acquisition_performed_in_review"] is False
    assert package["acquisition_provider_evidence_rerun_performed"] is False


def test_artifact_status_and_source_digests_are_bound(tmp_path: Path):
    package = _package(tmp_path)
    assert package["artifact_kind"] == review.ARTIFACT_KIND_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE
    assert package["review_status"] == review.ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
    expected = {
        "acquisition_provider_evidence_execution_digest": review.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "acquisition_provider_evidence_request_approval_digest": review.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_generation_chain_candidate_review_package_digest": review.execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST,
        "acquisition_generation_chain_candidate_digest": review.execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": review.execution.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "split_event_authority_freeze_digest": review.execution.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": review.execution.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": review.execution.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }
    assert {field: package[field] for field in expected} == expected


def test_missing_outputs_block_without_fabrication(tmp_path: Path):
    package = review.build_acquisition_evidence_results_review_package_v1(output_root=tmp_path / "missing")

    assert package["review_status"] == review.ACQUISITION_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert package["output_file_inspection_performed"] is False
    assert package["outputs_verified"] is False
    assert package["acquisition_evidence_results_available"] is False
    assert review.validate_acquisition_evidence_results_review_package_v1(package)["status"].endswith("BLOCKED_VALID")


def test_changed_output_digest_blocks(tmp_path: Path):
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    digests["operator_review_summary.json"] = "0" * 64
    package = review.build_acquisition_evidence_results_review_package_v1(
        output_root=root,
        expected_output_digests=digests,
    )

    assert package["review_status"] == review.ACQUISITION_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert "digest mismatch" in package["blocked_reason"]


def test_result_facts_manifest_and_per_ticker_summary_are_preserved(tmp_path: Path):
    package = _package(tmp_path)
    for field, expected in review.EXPECTED_RESULT_FACTS.items():
        if field != "target_count":
            assert package[field] == expected
    assert package["target_universe"] == review.EXPECTED_TARGET_UNIVERSE
    assert len(package["output_digest_manifest"]) == 7
    assert {
        row["ticker"]: (row["acquisition_provider_evidence_status"], row["historical_bar_count"])
        for row in package["per_ticker_acquisition_evidence_summary"]
    } == review.EXPECTED_PER_TICKER
    assert package["meta_reduced_bar_count_recorded"] is True


def test_review_classification_limitations_next_gates_and_summary(tmp_path: Path):
    package = _package(tmp_path)
    for field in (
        "acquisition_evidence_results_available",
        "all_provider_requests_succeeded",
        "historical_bar_evidence_available_for_all_tickers",
        "acquisition_evidence_review_supports_future_acquisition_generation_planning",
        "ready_for_acquisition_generation_approval",
    ):
        assert package[field] is True
    assert package["limitations"] == review.LIMITATIONS
    assert package["next_gates"] == review.NEXT_GATES
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == review.PASS for row in package["review_checklist"])
    assert package["review_summary"]["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert package["review_summary"]["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert package["review_summary"]["failed_checks"] == 0
    assert package["review_summary"]["blocker_count"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "acquisition_provider_evidence_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_executed",
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
        "acquisition_evidence_review_creates_acquisition_authority",
        "acquisition_evidence_review_creates_dataset_generation_authority",
        "acquisition_evidence_review_creates_canonical_dataset_authority",
        "acquisition_evidence_review_creates_registry_approval",
        "acquisition_evidence_review_creates_predictive_evidence_authority",
        "acquisition_evidence_review_creates_runtime_authority",
    ],
)
def test_closed_boolean_boundaries_remain_false(tmp_path: Path, field: str):
    assert _package(tmp_path)[field] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_acquisition_provider_evidence_execution_digest", "0" * 64),
        ("acquisition_provider_evidence_execution_digest", "0" * 64),
        ("acquisition_provider_evidence_request_approval_digest", "1" * 64),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review.EXPECTED_TARGET_UNIVERSE))),
        ("provider_request_count", 11),
        ("successful_provider_response_count", 11),
        ("failed_provider_response_count", 1),
        ("historical_bar_evidence_collected_count", 11),
        ("generated_output_count", 6),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("provider_requests_made_in_review", True),
        ("live_provider_transport_enabled_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("acquisition_provider_evidence_rerun_performed", True),
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
        ("acquisition_evidence_review_creates_acquisition_authority", True),
        ("acquisition_evidence_review_creates_dataset_generation_authority", True),
        ("acquisition_evidence_review_creates_canonical_dataset_authority", True),
        ("acquisition_evidence_review_creates_registry_approval", True),
        ("limitations", []),
        ("next_gates", []),
        ("acquisition_evidence_results_review_package_digest", None),
    ],
)
def test_validator_rejects_invalid_ready_package_fields(
    tmp_path: Path,
    field: str,
    value: Any,
):
    package = deepcopy(_package(tmp_path))
    package[field] = value
    if field != "acquisition_evidence_results_review_package_digest":
        _redigest(package)
    with pytest.raises(review.AcquisitionEvidenceResultsReviewError):
        review.validate_acquisition_evidence_results_review_package_v1(package)


def test_validator_rejects_bad_output_label_and_digest(tmp_path: Path):
    package = deepcopy(_package(tmp_path))
    package["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"
    _redigest(package)
    with pytest.raises(review.AcquisitionEvidenceResultsReviewError, match="output labels"):
        review.validate_acquisition_evidence_results_review_package_v1(package)

    package = deepcopy(_package(tmp_path))
    package["output_digest_manifest"][0]["sha256"] = "0" * 64
    _redigest(package)
    with pytest.raises(review.AcquisitionEvidenceResultsReviewError, match="output_digest_manifest"):
        review.validate_acquisition_evidence_results_review_package_v1(package)


def test_digest_is_deterministic_across_output_roots_and_validator_accepts(tmp_path: Path):
    one_root = tmp_path / "one"
    two_root = tmp_path / "two"
    one_digests = _write_fixture_outputs(one_root)
    two_digests = _write_fixture_outputs(two_root)
    one = review.build_acquisition_evidence_results_review_package_v1(
        output_root=one_root, expected_output_digests=one_digests
    )
    two = review.build_acquisition_evidence_results_review_package_v1(
        output_root=two_root, expected_output_digests=two_digests
    )

    assert one["acquisition_evidence_results_review_package_digest"] == two["acquisition_evidence_results_review_package_digest"]
    validation = review.validate_acquisition_evidence_results_review_package_v1(one)
    assert validation["status"] == "ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID"
    assert validation["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert validation["blocker_count"] == 0


def test_markdown_contains_required_sections(tmp_path: Path):
    markdown = review.build_acquisition_evidence_results_review_markdown_v1(_package(tmp_path))
    for heading in (
        "## Title",
        "## Reviewed Acquisition Provider Evidence Execution",
        "## Source Evidence",
        "## Target Universe",
        "## Acquisition Profile",
        "## Provider Request Summary",
        "## Per-Ticker Acquisition Evidence Summary",
        "## Output Digest Manifest",
        "## Data Quality Summary",
        "## Limitations",
        "## Next Gates",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Canonical Dataset Boundary",
        "## Registry Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_writes_canonical_json_and_refuses_overwrite(tmp_path: Path):
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    result = review.write_acquisition_evidence_results_review_package_v1(
        tmp_path / "review",
        output_root=root,
        expected_output_digests=digests,
    )
    payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert payload["review_status"] == review.ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
    with pytest.raises(review.AcquisitionEvidenceResultsReviewError, match="already exists"):
        review.write_acquisition_evidence_results_review_package_v1(
            tmp_path / "review",
            output_root=root,
            expected_output_digests=digests,
        )


def test_public_services_exports_review_api():
    assert services.build_acquisition_evidence_results_review_package_v1 is review.build_acquisition_evidence_results_review_package_v1
    assert services.validate_acquisition_evidence_results_review_package_v1 is review.validate_acquisition_evidence_results_review_package_v1
    assert services.write_acquisition_evidence_results_review_package_v1 is review.write_acquisition_evidence_results_review_package_v1
