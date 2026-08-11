from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import split_event_evidence_results_review_service as review


def _base_output() -> dict[str, Any]:
    return {
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": review.READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY,
        "split_event_authority_created": False,
        "split_event_authority_frozen": False,
        "corporate_action_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_use": review.NOT_AUTHORIZED,
        "strategy_use": review.NOT_AUTHORIZED,
        "paper_trading": review.NOT_AUTHORIZED,
        "broker_execution": review.NOT_AUTHORIZED,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
    }


def _per_ticker_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    counts = {
        "MSFT": 1,
        "NVDA": 4,
        "AMZN": 1,
        "GOOGL": 1,
        "META": 0,
        "TSLA": 2,
        "JPM": 0,
        "XOM": 0,
        "JNJ": 0,
        "WMT": 1,
        "CAT": 1,
        "LMT": 0,
    }
    for ticker in review.EXPECTED_TARGET_UNIVERSE:
        status = review.EXPECTED_PER_TICKER_STATUS[ticker]
        rows.append(
            {
                "ticker": ticker,
                "split_provider_evidence_status": status,
                "split_event_count": counts[ticker],
                "provider_response_digest": ticker.lower().ljust(64, "0")[:64],
                "sanitized_split_evidence_digest": ticker.lower().ljust(64, "1")[:64],
                "split_absence_policy_status": (
                    review.execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER
                    if counts[ticker] == 0
                    else "NO_SPLIT_EVENT_ABSENCE_POLICY_APPLIED"
                ),
                "raw_payload_committed": False,
                "raw_response_stored": False,
                "api_key_stored_or_printed": False,
                "split_event_authority_status": "NOT_CREATED",
                "split_event_freeze_status": "NOT_FROZEN",
                "dividend_event_authority_status": "NOT_CREATED",
                "corporate_action_authority_created": False,
                "acquisition_authorized": False,
                "dataset_generation_authorized": False,
                "runtime_use": review.NOT_AUTHORIZED,
                "strategy_use": review.NOT_AUTHORIZED,
                "paper_trading": review.NOT_AUTHORIZED,
                "broker_execution": review.NOT_AUTHORIZED,
            }
        )
    return rows


def _write_fixture_outputs(root: Path) -> dict[str, str]:
    root.mkdir(parents=True, exist_ok=True)
    base = _base_output()
    summary = {
        "target_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "split_evidence_collected_count": 7,
        "no_split_events_returned_count": 5,
        "not_evaluated_count": 12,
        "generated_output_count": 6,
        "failure_count": 0,
        "warning_count": 12,
    }
    payloads = {
        "split_provider_evidence_run_manifest.json": base
        | {
            "artifact_kind": "SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED",
            "execution_status": "SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY",
            "selected_endpoint": "/stocks/v1/splits",
            "selected_endpoint_mode": "LIVE_HTTP_TRANSPORT_READ_ONLY",
            "target_universe": review.EXPECTED_TARGET_UNIVERSE,
            "execution_summary": summary,
        },
        "split_provider_request_receipts_sanitized.json": base
        | {"request_receipts_sanitized": [{"ticker": ticker} for ticker in review.EXPECTED_TARGET_UNIVERSE]},
        "split_event_results_sanitized.json": base
        | {"per_ticker_split_evidence_results": _per_ticker_rows()},
        "split_event_absence_inventory.json": base
        | {
            "split_event_absence_inventory": [
                {"ticker": ticker, "split_event_count": 0}
                for ticker, status in review.EXPECTED_PER_TICKER_STATUS.items()
                if status == review.execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER
            ]
        },
        "split_event_failure_reason_inventory.json": base
        | {"split_event_failure_reason_inventory": []},
        "operator_review_summary.json": base
        | {
            "operator_review_required": True,
            "next_task": "SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE",
            "execution_summary": summary,
        },
    }
    expected: dict[str, str] = {}
    for filename, payload in payloads.items():
        data = canonical_json_bytes(payload)
        (root / filename).write_bytes(data)
        expected[filename] = review.sha256_bytes(data)
    return expected


def _package(tmp_path: Path) -> dict[str, Any]:
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    return review.build_split_event_evidence_results_review_package_v1(
        output_root=root,
        expected_output_digests=digests,
    )


def _redigest(package: dict[str, Any]) -> dict[str, Any]:
    package["split_event_evidence_results_review_package_digest"] = (
        review.split_event_evidence_results_review_package_digest_v1(package)
    )
    return package


def test_review_package_builds_offline_without_provider_calls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    def fail_provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider execution must not be called")

    monkeypatch.setattr(review.execution, "execute_split_provider_evidence_v1", fail_provider_call)
    package = _package(tmp_path)

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["split_provider_evidence_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_review"] is False


def test_artifact_kind_status_and_source_digests_are_bound(tmp_path: Path):
    package = _package(tmp_path)

    assert package["artifact_kind"] == review.ARTIFACT_KIND_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE
    assert package["review_status"] == review.SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
    assert package["source_split_provider_evidence_execution_digest"] == (
        review.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
    )
    assert package["split_provider_evidence_request_approval_digest"] == (
        review.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
    )
    assert package["split_event_authority_candidate_review_package_digest"] == (
        review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["split_event_authority_candidate_digest"] == (
        review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
    )
    assert package["dividend_event_authority_candidate_review_package_digest"] == (
        review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["corporate_action_authority_plan_approval_digest"] == (
        review.approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
    )


def test_review_status_is_blocked_when_outputs_are_missing(tmp_path: Path):
    package = review.build_split_event_evidence_results_review_package_v1(
        output_root=tmp_path / "missing",
        expected_output_digests=review.EXPECTED_OUTPUT_DIGESTS,
    )

    assert package["review_status"] == (
        review.SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    assert package["output_file_inspection_performed"] is False
    assert package["outputs_verified"] is False


def test_result_facts_output_digests_and_per_ticker_summary_are_preserved(tmp_path: Path):
    package = _package(tmp_path)

    assert package["target_universe_count"] == 12
    assert package["target_universe"] == review.EXPECTED_TARGET_UNIVERSE
    assert package["provider_request_count"] == 12
    assert package["successful_provider_response_count"] == 12
    assert package["failed_provider_response_count"] == 0
    assert package["split_evidence_collected_count"] == 7
    assert package["no_split_events_returned_count"] == 5
    assert package["generated_output_count"] == 6
    assert len(package["output_digest_manifest"]) == 6
    assert all(item["output_label"] == review.RESEARCH_ONLY_NON_ACTIONABLE for item in package["output_digest_manifest"])
    assert all(item["evidence_scope"] == review.READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY for item in package["output_digest_manifest"])
    assert {
        item["ticker"]: item["split_provider_evidence_status"]
        for item in package["per_ticker_split_evidence_summary"]
    } == review.EXPECTED_PER_TICKER_STATUS


def test_authority_predictive_profitability_and_runtime_boundaries_remain_closed(tmp_path: Path):
    package = _package(tmp_path)

    assert package["raw_provider_payloads_committed"] is False
    assert package["api_keys_stored_or_printed"] is False
    assert package["split_event_authority_created"] is False
    assert package["split_event_authority_frozen"] is False
    assert package["dividend_provider_evidence_request_authorized"] is False
    assert package["dividend_provider_evidence_executed"] is False
    assert package["dividend_event_authority_created"] is False
    assert package["corporate_action_authority_created"] is False
    assert package["new_ticker_acquisition_authorized"] is False
    assert package["dataset_generation_authorized"] is False
    assert package["additional_predictive_evidence_execution_authorized"] is False
    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"
    assert package["runtime_migration_approved"] is False
    assert package["runtime_use"] == review.NOT_AUTHORIZED
    assert package["strategy_use"] == review.NOT_AUTHORIZED
    assert package["paper_trading"] == review.NOT_AUTHORIZED
    assert package["broker_execution"] == review.NOT_AUTHORIZED


def test_review_classification_limitations_next_gates_and_checklist(tmp_path: Path):
    package = _package(tmp_path)

    assert package["split_evidence_review_supports_future_split_authority_planning"] is True
    assert package["split_evidence_creates_split_authority"] is False
    assert package["split_evidence_creates_corporate_action_authority"] is False
    assert package["split_evidence_creates_acquisition_authority"] is False
    assert package["split_evidence_creates_dataset_generation_authority"] is False
    assert package["limitations"] == review.LIMITATIONS
    assert package["next_gates"] == review.NEXT_GATES
    assert [item["check_id"] for item in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(item["status"] == review.PASS for item in package["review_checklist"])
    assert package["review_summary"]["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert package["review_summary"]["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert package["review_summary"]["failed_checks"] == 0
    assert package["review_summary"]["blocker_count"] == 0
    assert package["review_summary"]["ready_for_operator_review"] is True
    assert package["review_summary"]["ready_for_split_event_authority_freeze"] is False


def test_review_package_digest_is_deterministic(tmp_path: Path):
    first = _package(tmp_path)
    second = _package(tmp_path)

    assert first["split_event_evidence_results_review_package_digest"] == (
        second["split_event_evidence_results_review_package_digest"]
    )


def test_validator_accepts_valid_review_package(tmp_path: Path):
    validation = review.validate_split_event_evidence_results_review_package_v1(
        _package(tmp_path)
    )

    assert validation["status"] == "SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID"
    assert validation["provider_request_count"] == 12
    assert validation["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert validation["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("source_split_provider_evidence_execution_digest", "0" * 64, "source_split_provider_evidence_execution_digest"),
        ("split_provider_evidence_request_approval_digest", "1" * 64, "split_provider_evidence_request_approval_digest"),
        ("target_universe_count", 11, "target_universe_count"),
        ("provider_request_count", 11, "provider_request_count"),
        ("successful_provider_response_count", 11, "successful_provider_response_count"),
        ("failed_provider_response_count", 1, "failed_provider_response_count"),
        ("generated_output_count", 5, "generated_output_count"),
        ("raw_provider_payloads_committed", True, "raw_provider_payloads_committed"),
        ("api_keys_stored_or_printed", True, "api_keys_stored_or_printed"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("split_provider_evidence_rerun_performed", True, "split_provider_evidence_rerun_performed"),
        ("live_provider_transport_enabled_in_review", True, "live_provider_transport_enabled_in_review"),
        ("split_event_authority_created", True, "split_event_authority_created"),
        ("split_event_authority_frozen", True, "split_event_authority_frozen"),
        ("dividend_provider_evidence_request_authorized", True, "dividend_provider_evidence_request_authorized"),
        ("dividend_provider_evidence_executed", True, "dividend_provider_evidence_executed"),
        ("dividend_event_authority_created", True, "dividend_event_authority_created"),
        ("corporate_action_authority_created", True, "corporate_action_authority_created"),
        ("new_ticker_acquisition_authorized", True, "new_ticker_acquisition_authorized"),
        ("dataset_generation_authorized", True, "dataset_generation_authorized"),
        ("acquisition_generation_authorized", True, "acquisition_generation_authorized"),
        ("canonical_dataset_authorized", True, "canonical_dataset_authorized"),
        ("registry_approval_created", True, "registry_approval_created"),
        ("additional_predictive_evidence_execution_authorized", True, "additional_predictive_evidence_execution_authorized"),
        ("additional_predictive_evidence_executed", True, "additional_predictive_evidence_executed"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
        ("split_evidence_creates_split_authority", True, "split_evidence_creates_split_authority"),
        ("split_evidence_creates_corporate_action_authority", True, "split_evidence_creates_corporate_action_authority"),
        ("split_evidence_creates_acquisition_authority", True, "split_evidence_creates_acquisition_authority"),
        ("split_evidence_creates_dataset_generation_authority", True, "split_evidence_creates_dataset_generation_authority"),
        ("limitations", [], "limitations"),
        ("next_gates", [], "next_gates"),
        ("split_event_evidence_results_review_package_digest", None, "split_event_evidence_results_review_package_digest"),
    ],
)
def test_validator_rejects_invalid_review_package_fields(
    tmp_path: Path, field: str, value: Any, match: str
):
    package = _package(tmp_path)
    package[field] = value
    if field != "split_event_evidence_results_review_package_digest":
        _redigest(package)

    with pytest.raises(review.SplitEventEvidenceResultsReviewError, match=match):
        review.validate_split_event_evidence_results_review_package_v1(package)


def test_validator_rejects_output_label_not_research_only(tmp_path: Path):
    package = _package(tmp_path)
    package["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"
    _redigest(package)

    with pytest.raises(review.SplitEventEvidenceResultsReviewError, match="output labels"):
        review.validate_split_event_evidence_results_review_package_v1(package)


def test_markdown_includes_required_sections(tmp_path: Path):
    markdown = review.build_split_event_evidence_results_review_markdown_v1(
        _package(tmp_path)
    )

    for heading in (
        "# MarketFlow Split Event Evidence Results Review Status",
        "## Reviewed Split Provider Evidence Execution",
        "## Source Evidence",
        "## Target Universe",
        "## Provider Request Summary",
        "## Per-Ticker Split Evidence Summary",
        "## Output Digest Manifest",
        "## No-Split Event Policy Summary",
        "## Limitations",
        "## Next Gates",
        "## Split Authority Boundary",
        "## Dividend Boundary",
        "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown
    assert "No provider requests were made in review." in markdown


def test_writer_writes_json_and_refuses_overwrite(tmp_path: Path):
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    package = review.build_split_event_evidence_results_review_package_v1(
        output_root=root,
        expected_output_digests=digests,
    )
    output_dir = tmp_path / "review"

    result = review.write_split_event_evidence_results_review_package_v1(
        output_dir,
        output_root=root,
        expected_output_digests=digests,
    )

    path = Path(result["path"])
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["split_event_evidence_results_review_package_digest"] == (
        package["split_event_evidence_results_review_package_digest"]
    )
    with pytest.raises(review.SplitEventEvidenceResultsReviewError, match="already exists"):
        review.write_split_event_evidence_results_review_package_v1(
            output_dir,
            output_root=root,
            expected_output_digests=digests,
        )


def test_public_services_exports_review_api():
    assert services.build_split_event_evidence_results_review_package_v1 is (
        review.build_split_event_evidence_results_review_package_v1
    )
    assert services.validate_split_event_evidence_results_review_package_v1 is (
        review.validate_split_event_evidence_results_review_package_v1
    )
