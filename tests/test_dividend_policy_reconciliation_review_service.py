from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import dividend_policy_reconciliation_review_service as review


def _base_output() -> dict[str, Any]:
    return {
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": review.evidence.READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY,
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


def _evidence_rows() -> list[dict[str, Any]]:
    rows = []
    for ticker in review.EXPECTED_TARGET_UNIVERSE:
        status, count = review.evidence.EXPECTED_PER_TICKER[ticker]
        rows.append({
            "ticker": ticker,
            "dividend_provider_evidence_status": status,
            "dividend_event_count": count,
            "provider_response_digest": (ticker.lower() + "0" * 64)[:64],
            "sanitized_dividend_evidence_digest": (ticker.lower() + "1" * 64)[:64],
            "dividend_absence_policy_status": (
                review.evidence.execution.NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER
                if count == 0 else "NO_DIVIDEND_EVENT_ABSENCE_POLICY_APPLIED"
            ),
            "dividend_policy_reconciliation_status": "REQUIRES_OPERATOR_REVIEW",
            "raw_payload_committed": False,
            "raw_response_stored": False,
            "api_key_stored_or_printed": False,
        })
    return rows


def _write_outputs(root: Path) -> dict[str, str]:
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
    policy_rows = [{
        "ticker": ticker,
        "dividend_policy_reconciliation_status": "REQUIRES_OPERATOR_REVIEW",
        "cash_dividend_adjustment_policy": "REQUIRES_OPERATOR_REVIEW",
        "total_return_assumption": "NOT_ASSUMED",
        "authority_created": False,
    } for ticker in review.EXPECTED_TARGET_UNIVERSE]
    payloads = {
        "dividend_provider_evidence_run_manifest.json": base | {
            "artifact_kind": "DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED",
            "execution_status": "DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY",
            "target_universe": review.EXPECTED_TARGET_UNIVERSE,
            "execution_summary": summary,
        },
        "dividend_provider_request_receipts_sanitized.json": base | {
            "request_receipts_sanitized": [{"ticker": ticker} for ticker in review.EXPECTED_TARGET_UNIVERSE]
        },
        "dividend_event_results_sanitized.json": base | {
            "per_ticker_dividend_evidence_results": _evidence_rows()
        },
        "dividend_event_absence_inventory.json": base | {
            "dividend_event_absence_inventory": [{"ticker": ticker} for ticker in review.ZERO_DIVIDEND_TICKERS]
        },
        "dividend_policy_reconciliation_report.json": base | {
            "dividend_policy_reconciliation_report": policy_rows
        },
        "dividend_event_failure_reason_inventory.json": base | {
            "dividend_event_failure_reason_inventory": []
        },
        "operator_review_summary.json": base | {
            "operator_review_required": True, "execution_summary": summary
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
    digests = _write_outputs(root)
    return review.build_dividend_policy_reconciliation_review_package_v1(
        output_root=root, expected_output_digests=digests
    )


def _redigest(package: dict[str, Any]) -> None:
    package["dividend_policy_reconciliation_review_package_digest"] = (
        review.dividend_policy_reconciliation_review_package_digest_v1(package)
    )


def test_builds_offline_without_provider_calls(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    def fail(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider execution must not be called")

    monkeypatch.setattr(review.evidence.execution, "execute_dividend_provider_evidence_v1", fail)
    package = _package(tmp_path)
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["dividend_provider_evidence_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_review"] is False


def test_artifact_status_and_source_digests_are_bound(tmp_path: Path):
    package = _package(tmp_path)
    assert package["artifact_kind"] == review.ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE
    assert package["review_status"] == review.DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY
    assert package["source_dividend_event_evidence_results_review_package_digest"] == review.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
    assert package["source_dividend_provider_evidence_execution_digest"] == review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST
    assert package["source_dividend_provider_evidence_request_approval_digest"] == review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
    assert package["source_dividend_policy_reconciliation_report_digest"] == package["expected_output_digests"]["dividend_policy_reconciliation_report.json"]
    assert package["dividend_event_authority_candidate_review_package_digest"] == review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    assert package["split_event_authority_freeze_digest"] == review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST


def test_missing_policy_evidence_blocks_without_fabrication(tmp_path: Path):
    package = review.build_dividend_policy_reconciliation_review_package_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == review.DIVIDEND_POLICY_RECONCILIATION_REVIEW_BLOCKED_MISSING_OR_INVALID_EVIDENCE
    assert package["output_file_inspection_performed"] is False
    assert package["policy_evidence_verified"] is False
    assert review.validate_dividend_policy_reconciliation_review_package_v1(package)["status"].endswith("BLOCKED_VALID")


def test_evidence_counts_zero_tickers_and_policy_domains(tmp_path: Path):
    package = _package(tmp_path)
    assert package["target_universe_count"] == 12
    assert package["provider_request_count"] == 12
    assert package["successful_provider_response_count"] == 12
    assert package["failed_provider_response_count"] == 0
    assert package["dividend_evidence_collected_count"] == 10
    assert package["no_dividend_events_returned_count"] == 2
    assert package["zero_dividend_tickers"] == ["AMZN", "TSLA"]
    assert package["policy_domains"] == review.POLICY_DOMAINS


def test_policy_conclusions_and_per_ticker_entries_are_conservative(tmp_path: Path):
    package = _package(tmp_path)
    assert package["total_return_assumed"] is False
    assert package["dividend_reinvestment_assumed"] is False
    assert package["dividend_adjusted_price_policy_approved"] is False
    assert package["dividend_policy_reconciliation_approved"] is False
    assert package["ready_for_dividend_event_authority_freeze"] is False
    assert len(package["per_ticker_policy_review"]) == 12
    for row in package["per_ticker_policy_review"]:
        assert len(row["per_ticker_dividend_policy_reconciliation_review_digest"]) == 64
        assert row["canonical_dataset_impact_status"] == "NOT_AUTHORIZED_FOR_DATASET_GENERATION"
        assert row["predictive_label_impact_status"] == "NOT_AUTHORIZED_FOR_PREDICTIVE_USE"
        expected = "ZERO_ROW_RESPONSE_REQUIRES_OPERATOR_ABSENCE_POLICY_REVIEW" if row["ticker"] in {"AMZN", "TSLA"} else "DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE"
        assert row["dividend_absence_policy_status"] == expected


def test_classification_checklist_summary_limitations_and_next_gates(tmp_path: Path):
    package = _package(tmp_path)
    assert package["dividend_policy_reconciliation_supports_future_dividend_authority_planning"] is True
    assert package["limitations"] == review.LIMITATIONS
    assert package["next_gates"] == review.NEXT_GATES
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == review.PASS for row in package["review_checklist"])
    assert package["review_summary"] == review._summary(package["review_checklist"])
    assert package["review_summary"]["ready_for_dividend_policy_reconciliation_approval"] is True
    assert package["review_summary"]["ready_for_dividend_event_authority_freeze"] is False


@pytest.mark.parametrize("field", [
    "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
    "dividend_provider_evidence_rerun_performed", "dividend_policy_reconciliation_approved",
    "dividend_event_authority_created", "dividend_event_authority_frozen",
    "ready_for_dividend_event_authority_freeze", "split_provider_evidence_rerun_performed",
    "corporate_action_authority_created", "new_ticker_acquisition_authorized",
    "dataset_generation_authorized", "acquisition_generation_authorized",
    "canonical_dataset_authorized", "registry_approval_created",
    "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
    "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
    "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
    "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
    "automatic_stitching", "dividend_reinvestment_assumed", "total_return_assumed",
    "dividend_adjusted_price_policy_approved", "canonical_dataset_impact_authorized",
    "predictive_label_impact_authorized", "dividend_policy_reconciliation_creates_dividend_authority",
    "dividend_policy_reconciliation_creates_corporate_action_authority",
    "dividend_policy_reconciliation_creates_acquisition_authority",
    "dividend_policy_reconciliation_creates_dataset_generation_authority",
])
def test_closed_boolean_boundaries_are_false(tmp_path: Path, field: str):
    assert _package(tmp_path)[field] is False


@pytest.mark.parametrize(("field", "value"), [
    ("artifact_kind", "WRONG"),
    ("source_dividend_event_evidence_results_review_package_digest", "0" * 64),
    ("source_dividend_provider_evidence_execution_digest", "1" * 64),
    ("source_dividend_provider_evidence_request_approval_digest", "2" * 64),
    ("target_universe_count", 11), ("provider_request_count", 11),
    ("successful_provider_response_count", 11), ("failed_provider_response_count", 1),
    ("dividend_evidence_collected_count", 9), ("no_dividend_events_returned_count", 3),
    ("policy_domains", []), ("zero_dividend_tickers", ["AMZN"]),
    ("total_return_assumed", True), ("dividend_reinvestment_assumed", True),
    ("dividend_adjusted_price_policy_approved", True),
    ("dividend_policy_reconciliation_approved", True),
    ("ready_for_dividend_event_authority_freeze", True),
    ("raw_provider_payloads_committed", True), ("api_keys_stored_or_printed", True),
    ("provider_requests_made_in_review", True),
    ("dividend_provider_evidence_rerun_performed", True),
    ("live_provider_transport_enabled_in_review", True),
    ("dividend_event_authority_created", True), ("dividend_event_authority_frozen", True),
    ("split_event_authority_created", False), ("split_event_authority_frozen", False),
    ("split_provider_evidence_rerun_performed", True),
    ("corporate_action_authority_created", True),
    ("new_ticker_acquisition_authorized", True), ("dataset_generation_authorized", True),
    ("acquisition_generation_authorized", True), ("canonical_dataset_authorized", True),
    ("registry_approval_created", True),
    ("additional_predictive_evidence_execution_authorized", True),
    ("additional_predictive_evidence_executed", True),
    ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
    ("runtime_migration_approved", True), ("runtime_use", "AUTHORIZED"),
    ("strategy_use", "AUTHORIZED"), ("paper_trading", "AUTHORIZED"),
    ("broker_execution", "AUTHORIZED"), ("automatic_stitching", True),
    ("dividend_policy_reconciliation_creates_dividend_authority", True),
    ("dividend_policy_reconciliation_creates_corporate_action_authority", True),
    ("dividend_policy_reconciliation_creates_acquisition_authority", True),
    ("dividend_policy_reconciliation_creates_dataset_generation_authority", True),
    ("limitations", []), ("next_gates", []),
    ("dividend_policy_reconciliation_review_package_digest", None),
])
def test_validator_rejects_invalid_package_field(tmp_path: Path, field: str, value: Any):
    package = _package(tmp_path)
    package[field] = value
    if field != "dividend_policy_reconciliation_review_package_digest":
        _redigest(package)
    with pytest.raises(review.DividendPolicyReconciliationReviewError, match=field):
        review.validate_dividend_policy_reconciliation_review_package_v1(package)


def test_validator_rejects_missing_amzn_tsla_absence_policy(tmp_path: Path):
    package = _package(tmp_path)
    package["per_ticker_policy_review"][2]["dividend_absence_policy_status"] = "WRONG"
    package["per_ticker_policy_review"][2]["per_ticker_dividend_policy_reconciliation_review_digest"] = review.per_ticker_dividend_policy_reconciliation_review_digest_v1(package["per_ticker_policy_review"][2])
    _redigest(package)
    with pytest.raises(review.DividendPolicyReconciliationReviewError, match="AMZN.dividend_absence_policy_status"):
        review.validate_dividend_policy_reconciliation_review_package_v1(package)


def test_package_and_per_ticker_digests_are_deterministic(tmp_path: Path):
    first, second = _package(tmp_path), _package(tmp_path)
    assert first["dividend_policy_reconciliation_review_package_digest"] == second["dividend_policy_reconciliation_review_package_digest"]
    assert [row["per_ticker_dividend_policy_reconciliation_review_digest"] for row in first["per_ticker_policy_review"]] == [row["per_ticker_dividend_policy_reconciliation_review_digest"] for row in second["per_ticker_policy_review"]]


def test_validator_accepts_valid_package(tmp_path: Path):
    result = review.validate_dividend_policy_reconciliation_review_package_v1(_package(tmp_path))
    assert result["status"] == "DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_VALID"
    assert result["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert result["blocker_count"] == 0


def test_markdown_contains_required_sections(tmp_path: Path):
    markdown = review.build_dividend_policy_reconciliation_review_markdown_v1(_package(tmp_path))
    for heading in (
        "# MarketFlow Dividend Policy Reconciliation Review Status",
        "## Reviewed Dividend Policy Reconciliation", "## Source Dividend Evidence Results Review",
        "## Target Universe", "## Per-Ticker Dividend Policy Review",
        "## Zero-Dividend Response Absence Policy", "## Adjusted vs Unadjusted Price Policy",
        "## Cash Dividend Treatment Policy", "## Special Dividend Treatment Policy",
        "## Total Return and Reinvestment Boundary", "## Canonical Dataset Impact Boundary",
        "## Predictive Label Impact Boundary", "## Limitations", "## Next Gates",
        "## Dividend Authority Boundary", "## Split Authority Boundary",
        "## Corporate-Action Authority Boundary", "## Acquisition Boundary",
        "## Dataset Boundary", "## Predictive/Profitability Boundary",
        "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert heading in markdown


def test_writer_writes_json_and_refuses_overwrite(tmp_path: Path):
    root = tmp_path / "outputs"
    digests = _write_outputs(root)
    result = review.write_dividend_policy_reconciliation_review_package_v1(
        tmp_path / "review", output_root=root, expected_output_digests=digests
    )
    payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert payload["review_status"] == review.DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY
    with pytest.raises(review.DividendPolicyReconciliationReviewError, match="already exists"):
        review.write_dividend_policy_reconciliation_review_package_v1(
            tmp_path / "review", output_root=root, expected_output_digests=digests
        )


def test_public_services_exports_policy_review_api():
    assert services.build_dividend_policy_reconciliation_review_package_v1 is review.build_dividend_policy_reconciliation_review_package_v1
    assert services.validate_dividend_policy_reconciliation_review_package_v1 is review.validate_dividend_policy_reconciliation_review_package_v1
    assert services.write_dividend_policy_reconciliation_review_package_v1 is review.write_dividend_policy_reconciliation_review_package_v1
