from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import (
    combined_split_dividend_corporate_action_readiness_review_service as review,
)


def _package() -> dict[str, Any]:
    return review.build_combined_split_dividend_corporate_action_readiness_review_package_v1()


def _redigest(package: dict[str, Any]) -> None:
    package[
        "combined_split_dividend_corporate_action_readiness_review_package_digest"
    ] = review.combined_split_dividend_corporate_action_readiness_review_package_digest_v1(
        package
    )


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider call")

    monkeypatch.setattr(
        review.dividend_freeze.approval.review.evidence.execution,
        "execute_dividend_provider_evidence_v1",
        provider_call,
    )
    monkeypatch.setattr(
        review.split_freeze.review.execution,
        "execute_split_provider_evidence_v1",
        provider_call,
    )
    package = _package()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["live_provider_transport_enabled_in_review"] is False
    assert package["split_provider_evidence_rerun_performed"] is False
    assert package["dividend_provider_evidence_rerun_performed"] is False


def test_artifact_kind_status_and_review_readiness_are_exact():
    package = _package()
    assert package["artifact_kind"] == review.ARTIFACT_KIND_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE
    assert package["review_status"] == review.COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY
    assert package["combined_corporate_action_readiness_review_created"] is True
    assert package["combined_corporate_action_readiness_review_ready"] is True
    assert package["ready_for_corporate_action_authority_approval"] is True


def test_all_source_evidence_digests_are_bound():
    package = _package()
    expected = {
        "split_event_authority_freeze_digest": review.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": review.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": review.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": review.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": review.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": review.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_freeze_digest": review.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": review.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_review_package_digest": review.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": review.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": review.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": review.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": review.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": review.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": review.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": review.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
    }
    assert {field: package[field] for field in expected} == expected


def test_target_universe_and_authority_scopes_are_exact():
    package = _package()
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["split_event_authority_created"] is True
    assert package["split_event_authority_frozen"] is True
    assert package["split_event_authority_scope"] == review.split_freeze.SPLIT_EVENT_AUTHORITY_ONLY
    assert package["dividend_event_authority_created"] is True
    assert package["dividend_event_authority_frozen"] is True
    assert package["dividend_event_authority_scope"] == review.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY


def test_per_ticker_combined_readiness_entries_are_complete_and_deterministic():
    entries = _package()["per_ticker_combined_readiness"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review.TARGET_UNIVERSE
    for row in entries:
        assert row["split_event_authority_status"] == "FROZEN"
        assert row["dividend_event_authority_status"] == "FROZEN"
        assert row["combined_corporate_action_readiness_status"] == review.READY_FOR_CORPORATE_ACTION_AUTHORITY_APPROVAL
        assert row["corporate_action_authority_status"] == "NOT_CREATED"
        assert len(row["per_ticker_combined_readiness_review_digest"]) == 64
        assert row["per_ticker_combined_readiness_review_digest"] == review.per_ticker_combined_readiness_review_digest_v1(row)


def test_per_ticker_split_and_dividend_classifications_are_exact():
    entries = {row["ticker"]: row for row in _package()["per_ticker_combined_readiness"]}
    split_evidence_tickers = {"MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "WMT", "CAT"}
    for ticker, row in entries.items():
        expected_split = (
            review.split_freeze.SPLIT_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_SPLIT_EVIDENCE
            if ticker in split_evidence_tickers
            else review.split_freeze.SPLIT_EVENT_AUTHORITY_FROZEN_WITH_NO_SPLIT_EVENTS_RETURNED_POLICY
        )
        assert row["split_event_authority_classification"] == expected_split
        assert row["dividend_event_count"] == review.dividend_freeze.EXPECTED_PER_TICKER[ticker][1]
        expected_dividend = (
            review.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_ZERO_ROW_ABSENCE_POLICY
            if ticker in {"AMZN", "TSLA"}
            else review.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_DIVIDEND_EVIDENCE
        )
        assert row["dividend_event_authority_classification"] == expected_dividend


def test_readiness_conclusion_is_review_only():
    package = _package()
    assert package["combined_split_dividend_authorities_available"] is True
    assert package["split_authority_frozen"] is True
    assert package["dividend_authority_frozen"] is True
    assert package["combined_corporate_action_readiness_review_supports_future_corporate_action_authority_approval"] is True
    assert package["combined_corporate_action_readiness_review_creates_corporate_action_authority"] is False
    assert package["combined_corporate_action_readiness_review_creates_acquisition_authority"] is False
    assert package["combined_corporate_action_readiness_review_creates_dataset_generation_authority"] is False
    assert package["combined_corporate_action_readiness_review_creates_predictive_evidence_authority"] is False


def test_downstream_authority_runtime_and_acceptance_boundaries_remain_closed():
    package = _package()
    false_fields = (
        "corporate_action_authority_created",
        "corporate_action_authority_frozen",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
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
    )
    assert all(package[field] is False for field in false_fields)
    assert package["predictive_usefulness"] == review.NOT_ACCEPTED
    assert package["profitability"] == review.PROFITABILITY_NOT_ACCEPTED
    assert all(package[field] == review.NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_limitations_next_gates_checklist_and_summary_are_complete():
    package = _package()
    assert package["limitations"] == review.LIMITATIONS
    assert package["next_gates"] == review.NEXT_GATES
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_REVIEW_CHECK_IDS
    assert all(row["status"] == review.PASS for row in package["review_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in package["review_checklist"])
    summary = package["review_summary"]
    assert summary["total_checks"] == len(review.REQUIRED_REVIEW_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_REVIEW_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_corporate_action_authority_approval"] is True
    assert summary["corporate_action_authority_authorized"] is False


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("schema_version", "wrong"),
        ("review_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("split_event_authority_scope", "WRONG"),
        ("dividend_event_authority_created", False),
        ("dividend_event_authority_frozen", False),
        ("dividend_event_authority_scope", "WRONG"),
        ("ready_for_corporate_action_authority_approval", False),
        ("corporate_action_authority_created", True),
        ("corporate_action_authority_frozen", True),
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
        ("provider_requests_made_in_review", True),
        ("live_provider_transport_enabled_in_review", True),
        ("split_provider_evidence_rerun_performed", True),
        ("dividend_provider_evidence_rerun_performed", True),
        ("combined_corporate_action_readiness_review_creates_corporate_action_authority", True),
        ("combined_corporate_action_readiness_review_creates_acquisition_authority", True),
        ("combined_corporate_action_readiness_review_creates_dataset_generation_authority", True),
    ],
)
def test_validator_rejects_invalid_readiness_or_boundary(field: str, bad_value: Any):
    package = _package()
    package[field] = bad_value
    _redigest(package)
    with pytest.raises(review.CombinedCorporateActionReadinessReviewError):
        review.validate_combined_split_dividend_corporate_action_readiness_review_package_v1(package)


@pytest.mark.parametrize(
    "field",
    [
        "split_event_authority_freeze_digest",
        "dividend_event_authority_freeze_digest",
        "limitations",
        "next_gates",
        "combined_split_dividend_corporate_action_readiness_review_package_digest",
    ],
)
def test_validator_rejects_missing_required_evidence_or_governance(field: str):
    package = _package()
    package.pop(field)
    if field != "combined_split_dividend_corporate_action_readiness_review_package_digest":
        _redigest(package)
    with pytest.raises(review.CombinedCorporateActionReadinessReviewError):
        review.validate_combined_split_dividend_corporate_action_readiness_review_package_v1(package)


def test_validator_rejects_per_ticker_count_not_twelve():
    package = _package()
    package["per_ticker_combined_readiness"].pop()
    _redigest(package)
    with pytest.raises(review.CombinedCorporateActionReadinessReviewError):
        review.validate_combined_split_dividend_corporate_action_readiness_review_package_v1(package)


def test_validator_rejects_missing_per_ticker_digest():
    package = _package()
    package["per_ticker_combined_readiness"][0].pop(
        "per_ticker_combined_readiness_review_digest"
    )
    _redigest(package)
    with pytest.raises(review.CombinedCorporateActionReadinessReviewError):
        review.validate_combined_split_dividend_corporate_action_readiness_review_package_v1(package)


def test_validator_accepts_valid_package():
    result = review.validate_combined_split_dividend_corporate_action_readiness_review_package_v1(_package())
    assert result["status"] == "COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_VALID"
    assert result["target_universe_count"] == 12
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


def test_package_and_per_ticker_digests_are_deterministic():
    first = _package()
    second = _package()
    digest_field = "combined_split_dividend_corporate_action_readiness_review_package_digest"
    assert first[digest_field] == second[digest_field]
    assert [row["per_ticker_combined_readiness_review_digest"] for row in first["per_ticker_combined_readiness"]] == [row["per_ticker_combined_readiness_review_digest"] for row in second["per_ticker_combined_readiness"]]


def test_markdown_includes_required_sections():
    markdown = review.build_combined_split_dividend_corporate_action_readiness_review_markdown_v1(_package())
    for section in (
        "Combined Split/Dividend Corporate-Action Readiness Review",
        "Source Split Authority Freeze",
        "Source Dividend Authority Freeze",
        "Target Universe",
        "Per-Ticker Combined Readiness Summary",
        "Readiness Conclusion",
        "Limitations",
        "Next Gates",
        "Corporate-Action Authority Boundary",
        "Acquisition Boundary",
        "Dataset Boundary",
        "Predictive/Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_creates_json_and_markdown_without_overwrite(tmp_path: Path):
    result = review.write_combined_split_dividend_corporate_action_readiness_review_package_v1(tmp_path)
    assert Path(result["json_path"]).exists()
    assert Path(result["markdown_path"]).exists()
    payload = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    assert payload["review_status"] == review.COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY
    with pytest.raises(review.CombinedCorporateActionReadinessReviewError):
        review.write_combined_split_dividend_corporate_action_readiness_review_package_v1(tmp_path)


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE == review.ARTIFACT_KIND_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE
    assert services.COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY == review.COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY
    assert services.build_combined_split_dividend_corporate_action_readiness_review_package_v1 is review.build_combined_split_dividend_corporate_action_readiness_review_package_v1
    assert services.validate_combined_split_dividend_corporate_action_readiness_review_package_v1 is review.validate_combined_split_dividend_corporate_action_readiness_review_package_v1
    assert services.write_combined_split_dividend_corporate_action_readiness_review_package_v1 is review.write_combined_split_dividend_corporate_action_readiness_review_package_v1
