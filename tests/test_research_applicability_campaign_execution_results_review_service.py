from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    research_applicability_campaign_execution_results_review_service as review,
)


def _boundary(report_name: str) -> dict[str, Any]:
    return {
        "report_name": report_name,
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
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


def _fixture_outputs(output_root: Path) -> dict[str, str]:
    outputs = {
        "dataset_load_report": _boundary("dataset_load_report")
        | {
            "datasets": [
                {"dataset_profile": "SWING", "row_count": 1988},
                {"dataset_profile": "POSITION_SWING", "row_count": 994},
            ],
            "dataset_count": 2,
            "datasets_loaded_count": 2,
            "datasets_digest_verified_count": 2,
        },
        "schema_validation_report": _boundary("schema_validation_report")
        | {"schema_validation_status": "PASS"},
        "bar_count_consistency_report": _boundary("bar_count_consistency_report")
        | {"bar_count_consistency_status": "PASS"},
        "date_range_coverage_report": _boundary("date_range_coverage_report")
        | {"date_range_coverage_status": "PASS"},
        "null_field_summary_report": _boundary("null_field_summary_report")
        | {"null_field_summary_status": "PASS"},
        "ohlc_consistency_report": _boundary("ohlc_consistency_report")
        | {"ohlc_consistency_status": "PASS"},
        "volume_consistency_report": _boundary("volume_consistency_report")
        | {"volume_consistency_status": "PASS"},
        "indicator_calculation_report": _boundary("indicator_calculation_report")
        | {
            "indicator_calculation_status": "PASS",
            "indicator_acceptance_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        },
        "module_compatibility_matrix": _boundary("module_compatibility_matrix")
        | {"module_compatibility_status": "RESEARCH_ONLY_COMPATIBILITY_LISTED"},
        "failure_reason_inventory": _boundary("failure_reason_inventory")
        | {"failure_count": 0, "warning_count": 0, "failures": [], "warnings": []},
        "operator_review_summary": _boundary("operator_review_summary")
        | {
            "execution_request_id": review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
            "generated_output_count": 12,
            "performance_acceptance": "NOT_ACCEPTED",
            "runtime_authorization": "NOT_AUTHORIZED",
        },
    }
    digests = {
        name: _write_json(output_root / f"{name}.json", payload)
        for name, payload in outputs.items()
    }
    run_manifest = _boundary("research_campaign_run_manifest") | {
        "run_id": "AAPL_RESEARCH_APPLICABILITY_EXECUTION_V1_TEST",
        "execution_request_id": review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
        "source_digests": {
            "research_campaign_execution_approval_digest": (
                review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
            ),
            "execution_candidate_digest": review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
            "execution_candidate_review_package_digest": (
                review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
            ),
            "campaign_plan_digest": review.EXPECTED_CAMPAIGN_PLAN_DIGEST,
            "campaign_plan_review_package_digest": (
                review.EXPECTED_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
            ),
            "dataset_availability_review_package_digest": (
                review.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
            ),
        },
        "output_paths": {name: f"outputs/{name}.json" for name in review.EXPECTED_OUTPUT_NAMES},
        "output_digests": digests | {"research_campaign_run_manifest": "SELF_DIGEST_BOUND_SEPARATELY"},
        "boundary_flags": {
            "provider_requests_made": False,
            "runtime_migration_approved": False,
            "runtime_migration_active": False,
            "strategy_runtime_migration": False,
            "automatic_stitching": False,
        },
    }
    digests["research_campaign_run_manifest"] = _write_json(
        output_root / "research_campaign_run_manifest.json",
        run_manifest,
    )
    return digests


def _package(tmp_path: Path) -> dict[str, Any]:
    output_root = tmp_path / "outputs"
    _fixture_outputs(output_root)
    return review.build_research_applicability_campaign_execution_results_review_package_v1(
        output_root=output_root
    )


def _mutated_valid_package(tmp_path: Path, field: str, value: Any) -> dict[str, Any]:
    package = _package(tmp_path)
    package[field] = value
    return package


def test_review_package_builds_offline_without_provider_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package(tmp_path)

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_artifact_kind_is_results_review_package(tmp_path: Path):
    assert _package(tmp_path)["artifact_kind"] == (
        review.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE
    )


def test_review_status_is_ready_when_fixture_outputs_are_present_and_valid(tmp_path: Path):
    assert _package(tmp_path)["review_status"] == (
        review.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY
    )


def test_review_status_is_blocked_when_outputs_are_missing(tmp_path: Path):
    package = review.build_research_applicability_campaign_execution_results_review_package_v1(
        output_root=tmp_path / "missing"
    )

    assert package["review_status"] == (
        review.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS
    )
    assert package["actual_output_count"] == 0


def test_execution_digest_and_request_id_are_bound(tmp_path: Path):
    package = _package(tmp_path)

    assert package["source_execution_digest"] == review.EXPECTED_SOURCE_EXECUTION_DIGEST
    assert package["source_execution_request_id"] == review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID


def test_output_count_and_labels(tmp_path: Path):
    package = _package(tmp_path)

    assert package["actual_output_count"] == 12
    assert package["all_outputs_research_only_non_actionable"] is True


def test_dataset_load_summary_matches_expected_rows(tmp_path: Path):
    summary = _package(tmp_path)["dataset_load_summary"]

    assert summary["swing_row_count"] == 1988
    assert summary["position_swing_row_count"] == 994
    assert summary["datasets_digest_verified_count"] == 2


def test_data_quality_statuses_are_pass(tmp_path: Path):
    package = _package(tmp_path)

    assert package["schema_validation_status"] == "PASS"
    assert package["bar_count_consistency_status"] == "PASS"
    assert package["date_range_coverage_status"] == "PASS"
    assert package["ohlc_consistency_status"] == "PASS"
    assert package["volume_consistency_status"] == "PASS"
    assert package["indicator_calculation_status"] == "PASS"
    assert package["indicator_acceptance_label"] == review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE


def test_module_compatibility_status_is_listed(tmp_path: Path):
    assert _package(tmp_path)["module_compatibility_status"] == "RESEARCH_ONLY_COMPATIBILITY_LISTED"


def test_failure_and_warning_counts_are_zero(tmp_path: Path):
    package = _package(tmp_path)

    assert package["failure_count"] == 0
    assert package["warning_count"] == 0


def test_no_trade_recommendation_or_runtime_authorization_exists(tmp_path: Path):
    package = _package(tmp_path)

    assert package["trade_recommendations_present"] is False
    assert package["runtime_authorization_present_in_outputs"] is False


def test_predictive_and_profitability_remain_not_accepted(tmp_path: Path):
    package = _package(tmp_path)

    assert package["predictive_usefulness"] == review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_provider_review_and_reexecution_flags_remain_false(tmp_path: Path):
    package = _package(tmp_path)

    assert package["provider_requests_made_in_review"] is False
    assert package["campaign_reexecution_performed"] is False


def test_runtime_migration_and_strategy_flags_remain_false(tmp_path: Path):
    package = _package(tmp_path)

    assert package["runtime_migration_approved"] is False
    assert package["runtime_migration_active"] is False
    assert package["strategy_runtime_migration"] is False


def test_runtime_strategy_paper_and_broker_remain_not_authorized(tmp_path: Path):
    package = _package(tmp_path)

    assert package["runtime_use"] == review.NOT_AUTHORIZED
    assert package["strategy_use"] == review.NOT_AUTHORIZED
    assert package["paper_trading"] == review.NOT_AUTHORIZED
    assert package["broker_execution"] == review.NOT_AUTHORIZED


def test_checklist_contains_all_required_check_ids(tmp_path: Path):
    assert [item["check_id"] for item in _package(tmp_path)["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_valid_fixture_outputs(tmp_path: Path):
    assert {item["status"] for item in _package(tmp_path)["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_correctly(tmp_path: Path):
    package = _package(tmp_path)
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_predictive_usefulness_review"] is True


def test_review_package_digest_is_deterministic(tmp_path: Path):
    first = _package(tmp_path)
    second = review.build_research_applicability_campaign_execution_results_review_package_v1(
        output_root=tmp_path / "outputs"
    )

    assert first["research_applicability_campaign_execution_results_review_package_digest"] == second[
        "research_applicability_campaign_execution_results_review_package_digest"
    ]
    assert (
        first["research_applicability_campaign_execution_results_review_package_digest"]
        == review.research_applicability_campaign_execution_results_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_review_package(tmp_path: Path):
    validation = review.validate_research_applicability_campaign_execution_results_review_package_v1(
        _package(tmp_path)
    )

    assert validation["status"] == (
        "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_VALID"
    )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("actual_output_count", 11, "actual_output_count"),
        ("all_outputs_research_only_non_actionable", False, "all_outputs_research_only_non_actionable"),
        ("failure_count", 1, "failure_count"),
        ("warning_count", 1, "warning_count"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("campaign_reexecution_performed", True, "campaign_reexecution_performed"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
    ],
)
def test_validator_rejects_invalid_review_package_mutations(
    tmp_path: Path,
    field: str,
    value,
    match: str,
):
    package = _mutated_valid_package(tmp_path, field, value)

    with pytest.raises(
        review.ResearchApplicabilityCampaignExecutionResultsReviewError,
        match=match,
    ):
        review.validate_research_applicability_campaign_execution_results_review_package_v1(package)


def test_validator_rejects_predictive_and_profitability_accepted(tmp_path: Path):
    for field in ("predictive_usefulness", "profitability"):
        package = _mutated_valid_package(tmp_path, field, "accepted")

        with pytest.raises(
            review.ResearchApplicabilityCampaignExecutionResultsReviewError,
            match=field,
        ):
            review.validate_research_applicability_campaign_execution_results_review_package_v1(
                package
            )


def test_markdown_writer_includes_required_sections(tmp_path: Path):
    markdown = review.build_research_applicability_campaign_execution_results_review_markdown_v1(
        _package(tmp_path)
    )

    for section in (
        "## Title",
        "## Reviewed Research Campaign Execution",
        "## Output Summary",
        "## Data Quality Summary",
        "## Module Compatibility Summary",
        "## Failure Warning Inventory",
        "## Runtime Boundary",
        "## Predictive Profitability Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_results_review_package_writes_json_without_overwrite(tmp_path: Path):
    output_root = tmp_path / "outputs"
    _fixture_outputs(output_root)

    result = review.write_research_applicability_campaign_execution_results_review_package_v1(
        tmp_path / "review",
        output_root=output_root,
    )

    assert result["artifact_kind"] == (
        review.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE
    )
    assert result["payload_sha256"]
    with pytest.raises(
        review.ResearchApplicabilityCampaignExecutionResultsReviewError,
        match="already exists",
    ):
        review.write_research_applicability_campaign_execution_results_review_package_v1(
            tmp_path / "review",
            output_root=output_root,
        )


def test_results_review_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE
    )
    assert services.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY == (
        review.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY
    )
    assert services.build_research_applicability_campaign_execution_results_review_package_v1 is (
        review.build_research_applicability_campaign_execution_results_review_package_v1
    )
    assert services.validate_research_applicability_campaign_execution_results_review_package_v1 is (
        review.validate_research_applicability_campaign_execution_results_review_package_v1
    )
    assert services.write_research_applicability_campaign_execution_results_review_package_v1 is (
        review.write_research_applicability_campaign_execution_results_review_package_v1
    )
    assert services.build_research_applicability_campaign_execution_results_review_markdown_v1 is (
        review.build_research_applicability_campaign_execution_results_review_markdown_v1
    )
