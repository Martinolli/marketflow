from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import dividend_event_evidence_results_review_service as review


def _base_output() -> dict[str, Any]:
    return {
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": review.READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
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
    rows = []
    for ticker in review.EXPECTED_TARGET_UNIVERSE:
        status, count = review.EXPECTED_PER_TICKER[ticker]
        rows.append(
            {
                "ticker": ticker,
                "dividend_provider_evidence_status": status,
                "dividend_event_count": count,
                "provider_response_digest": (ticker.lower() + "0" * 64)[:64],
                "sanitized_dividend_evidence_digest": (ticker.lower() + "1" * 64)[:64],
                "dividend_absence_policy_status": (
                    review.execution.NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER
                    if count == 0 else "NO_DIVIDEND_EVENT_ABSENCE_POLICY_APPLIED"
                ),
                "dividend_policy_reconciliation_status": "REQUIRES_OPERATOR_REVIEW",
                "raw_payload_committed": False,
                "raw_response_stored": False,
                "api_key_stored_or_printed": False,
                "dividend_event_authority_status": "NOT_CREATED",
                "dividend_event_freeze_status": "NOT_FROZEN",
                "split_event_authority_status": "FROZEN",
                "corporate_action_authority_created": False,
                "acquisition_authorized": False,
                "dataset_generation_authorized": False,
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
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "not_evaluated_count": 12,
        "generated_output_count": 7,
        "failure_count": 0,
        "warning_count": 12,
    }
    policy_rows = [
        {
            "ticker": ticker,
            "dividend_policy_reconciliation_status": "REQUIRES_OPERATOR_REVIEW",
            "cash_dividend_adjustment_policy": "REQUIRES_OPERATOR_REVIEW",
            "total_return_assumption": "NOT_ASSUMED",
            "authority_created": False,
        }
        for ticker in review.EXPECTED_TARGET_UNIVERSE
    ]
    payloads = {
        "dividend_provider_evidence_run_manifest.json": base | {
            "artifact_kind": "DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED",
            "execution_status": "DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY",
            "selected_endpoint": "/stocks/v1/dividends",
            "selected_endpoint_mode": "CURRENT_STOCKS_V1_DIVIDENDS",
            "target_universe": review.EXPECTED_TARGET_UNIVERSE,
            "execution_summary": summary,
        },
        "dividend_provider_request_receipts_sanitized.json": base | {
            "request_receipts_sanitized": [{"ticker": ticker} for ticker in review.EXPECTED_TARGET_UNIVERSE]
        },
        "dividend_event_results_sanitized.json": base | {
            "per_ticker_dividend_evidence_results": _per_ticker_rows()
        },
        "dividend_event_absence_inventory.json": base | {
            "dividend_event_absence_inventory": [
                {"ticker": "AMZN", "dividend_event_count": 0},
                {"ticker": "TSLA", "dividend_event_count": 0},
            ]
        },
        "dividend_policy_reconciliation_report.json": base | {
            "dividend_policy_reconciliation_report": policy_rows
        },
        "dividend_event_failure_reason_inventory.json": base | {
            "dividend_event_failure_reason_inventory": []
        },
        "operator_review_summary.json": base | {
            "operator_review_required": True,
            "next_task": "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE",
            "execution_summary": summary,
        },
    }
    digests = {}
    for filename, payload in payloads.items():
        data = canonical_json_bytes(payload)
        (root / filename).write_bytes(data)
        digests[filename] = review.sha256_bytes(data)
    return digests


def _package(tmp_path: Path) -> dict[str, Any]:
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    return review.build_dividend_event_evidence_results_review_package_v1(
        output_root=root, expected_output_digests=digests
    )


def _redigest(package: dict[str, Any]) -> None:
    package["dividend_event_evidence_results_review_package_digest"] = (
        review.dividend_event_evidence_results_review_package_digest_v1(package)
    )


def test_review_builds_offline_without_provider_calls(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    def fail(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider execution must not be called")

    monkeypatch.setattr(review.execution, "execute_dividend_provider_evidence_v1", fail)
    package = _package(tmp_path)
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["dividend_provider_evidence_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_review"] is False


def test_artifact_status_and_all_source_digests_are_bound(tmp_path: Path):
    package = _package(tmp_path)
    assert package["artifact_kind"] == review.ARTIFACT_KIND_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE
    assert package["review_status"] == review.DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
    expected = {
        "dividend_provider_evidence_execution_digest": review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": review.approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_approval_digest": review.approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": review.approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }
    assert {key: package[key] for key in expected} == expected


def test_missing_or_invalid_outputs_block_without_fabrication(tmp_path: Path):
    package = review.build_dividend_event_evidence_results_review_package_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == review.DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert package["output_file_inspection_performed"] is False
    assert package["outputs_verified"] is False
    assert review.validate_dividend_event_evidence_results_review_package_v1(package)["status"].endswith("BLOCKED_VALID")


def test_result_facts_output_digests_and_per_ticker_summary_are_preserved(tmp_path: Path):
    package = _package(tmp_path)
    for field, expected in review.EXPECTED_RESULT_FACTS.items():
        if field not in {"endpoint", "endpoint_mode", "transport_mode", "target_count"}:
            assert package[field] == expected
    assert package["target_universe"] == review.EXPECTED_TARGET_UNIVERSE
    assert package["zero_dividend_tickers"] == ["AMZN", "TSLA"]
    assert len(package["output_digest_manifest"]) == 7
    assert {
        row["ticker"]: (row["dividend_provider_evidence_status"], row["dividend_event_count"])
        for row in package["per_ticker_dividend_evidence_summary"]
    } == review.EXPECTED_PER_TICKER


def test_review_classification_policy_limitations_next_gates_and_summary(tmp_path: Path):
    package = _package(tmp_path)
    assert package["dividend_evidence_review_supports_future_dividend_authority_planning"] is True
    assert package["dividend_policy_reconciliation_requires_operator_review"] is True
    assert package["dividend_policy_reconciliation_requirements"] == review.DIVIDEND_POLICY_RECONCILIATION_REQUIREMENTS
    assert package["limitations"] == review.LIMITATIONS
    assert package["next_gates"] == review.NEXT_GATES
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == review.PASS for row in package["review_checklist"])
    assert package["review_summary"] == review._summary(package["review_checklist"])
    assert package["review_summary"]["ready_for_dividend_event_authority_freeze"] is False
    assert package["review_summary"]["ready_for_dividend_policy_reconciliation_review"] is True


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "dividend_provider_evidence_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "dividend_event_authority_created",
        "dividend_event_authority_frozen", "split_provider_evidence_rerun_performed",
        "corporate_action_authority_created", "new_ticker_acquisition_authorized",
        "dataset_generation_authorized", "acquisition_generation_authorized",
        "canonical_dataset_authorized", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "automatic_stitching",
        "dividend_evidence_creates_dividend_authority",
        "dividend_evidence_creates_corporate_action_authority",
        "dividend_evidence_creates_acquisition_authority",
        "dividend_evidence_creates_dataset_generation_authority",
    ],
)
def test_closed_boolean_boundaries_remain_false(tmp_path: Path, field: str):
    assert _package(tmp_path)[field] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("source_dividend_provider_evidence_execution_digest", "0" * 64),
        ("dividend_provider_evidence_request_approval_digest", "1" * 64),
        ("target_universe_count", 11),
        ("provider_request_count", 11),
        ("successful_provider_response_count", 11),
        ("failed_provider_response_count", 1),
        ("generated_output_count", 6),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("provider_requests_made_in_review", True),
        ("dividend_provider_evidence_rerun_performed", True),
        ("live_provider_transport_enabled_in_review", True),
        ("dividend_event_authority_created", True),
        ("dividend_event_authority_frozen", True),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("split_provider_evidence_rerun_performed", True),
        ("corporate_action_authority_created", True),
        ("new_ticker_acquisition_authorized", True),
        ("dataset_generation_authorized", True),
        ("acquisition_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("registry_approval_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("dividend_evidence_creates_dividend_authority", True),
        ("dividend_evidence_creates_corporate_action_authority", True),
        ("dividend_evidence_creates_acquisition_authority", True),
        ("dividend_evidence_creates_dataset_generation_authority", True),
        ("dividend_policy_reconciliation_requirements", []),
        ("limitations", []),
        ("next_gates", []),
        ("dividend_event_evidence_results_review_package_digest", None),
    ],
)
def test_validator_rejects_invalid_ready_package_fields(
    tmp_path: Path, field: str, value: Any
):
    package = _package(tmp_path)
    package[field] = value
    if field != "dividend_event_evidence_results_review_package_digest":
        _redigest(package)
    with pytest.raises(review.DividendEventEvidenceResultsReviewError, match=field):
        review.validate_dividend_event_evidence_results_review_package_v1(package)


def test_validator_rejects_bad_output_label_and_changed_output_digest(tmp_path: Path):
    package = _package(tmp_path)
    package["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"
    _redigest(package)
    with pytest.raises(review.DividendEventEvidenceResultsReviewError, match="output labels"):
        review.validate_dividend_event_evidence_results_review_package_v1(package)

    package = _package(tmp_path)
    package["output_digest_manifest"][0]["sha256"] = "0" * 64
    _redigest(package)
    with pytest.raises(review.DividendEventEvidenceResultsReviewError, match="output_digest_manifest"):
        review.validate_dividend_event_evidence_results_review_package_v1(package)


def test_digest_is_deterministic_and_validator_accepts_valid_package(tmp_path: Path):
    first = _package(tmp_path)
    second = _package(tmp_path)
    assert first["dividend_event_evidence_results_review_package_digest"] == second["dividend_event_evidence_results_review_package_digest"]
    result = review.validate_dividend_event_evidence_results_review_package_v1(first)
    assert result["status"] == "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID"
    assert result["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert result["blocker_count"] == 0


def test_markdown_contains_all_required_sections(tmp_path: Path):
    markdown = review.build_dividend_event_evidence_results_review_markdown_v1(_package(tmp_path))
    for heading in (
        "# MarketFlow Dividend Event Evidence Results Review Status",
        "## Reviewed Dividend Provider Evidence Execution", "## Source Evidence",
        "## Target Universe", "## Provider Request Summary",
        "## Per-Ticker Dividend Evidence Summary", "## Output Digest Manifest",
        "## Dividend Absence Policy Summary", "## Dividend Policy Reconciliation Summary",
        "## Limitations", "## Next Gates", "## Dividend Authority Boundary",
        "## Split Authority Boundary", "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary", "## Dataset Boundary",
        "## Predictive/Profitability Boundary", "## Runtime Boundary",
        "## Checklist Summary", "## Guardrails",
    ):
        assert heading in markdown


def test_writer_writes_canonical_json_and_refuses_overwrite(tmp_path: Path):
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    result = review.write_dividend_event_evidence_results_review_package_v1(
        tmp_path / "review", output_root=root, expected_output_digests=digests
    )
    payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert payload["review_status"] == review.DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY
    with pytest.raises(review.DividendEventEvidenceResultsReviewError, match="already exists"):
        review.write_dividend_event_evidence_results_review_package_v1(
            tmp_path / "review", output_root=root, expected_output_digests=digests
        )


def test_public_services_exports_review_api():
    assert services.build_dividend_event_evidence_results_review_package_v1 is review.build_dividend_event_evidence_results_review_package_v1
    assert services.validate_dividend_event_evidence_results_review_package_v1 is review.validate_dividend_event_evidence_results_review_package_v1
    assert services.write_dividend_event_evidence_results_review_package_v1 is review.write_dividend_event_evidence_results_review_package_v1
