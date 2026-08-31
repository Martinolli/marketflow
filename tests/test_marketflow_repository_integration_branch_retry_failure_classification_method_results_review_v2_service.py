import json
from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_service
    as service,
)


@pytest.fixture(scope="module")
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2()


def test_review_builds_offline_from_committed_source_constants(review):
    assert review["created_offline_except_read_only_file_verification"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        (
            "artifact_kind",
            service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2,
        ),
        (
            "review_status",
            service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_READY,
        ),
        (
            "review_scope",
            service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN,
        ),
        ("source_classification_method_execution_v2_digest", service.SOURCE_EXECUTION_V2_DIGEST),
        ("source_classification_method_v2_module_grouping_digest", service.SOURCE_MODULE_GROUPING_DIGEST),
        ("source_classification_method_v2_digest_manifest_digest", service.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("source_classification_method_approval_v2_digest", service.source.SOURCE_APPROVAL_V2_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("module_level_grouping_reviewed", True),
        ("module_summary_reviewed", True),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("failed_or_errored_nodeids_count", 1404),
        ("limitations_reviewed", True),
        ("unsupported_claims_exclusion_reviewed", True),
        ("failure_modules_classified", False),
        ("error_modules_classified", False),
        ("failure_error_separation_claimed", False),
        ("first_failure_identified", False),
        ("first_error_identified", False),
        ("first_order_claim_made", False),
        ("traceback_root_cause_claimed", False),
        ("retry_success_claimed", False),
        ("main_merge_readiness_claimed", False),
        ("planned_outputs_reviewed", True),
        ("classification_method_results_review_v2_created", True),
        ("classification_method_results_review_v2_ready", True),
        ("ready_for_remediation_or_method_candidate_after_v2_review", True),
        ("remediation_or_method_candidate_after_v2_review_created", False),
        ("new_retry_candidate_created", False),
        ("new_retry_executed", False),
        ("new_retry_results_review_created", False),
        ("main_merge_approval_created", False),
        ("retry_rerun_performed", False),
        ("full_pytest_performed", False),
        ("diagnostic_command_executed", False),
        ("diagnostic_output_captured", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("marketflow_outputs_committed", False),
        ("pytest_cache_committed", False),
        ("evidence_regenerated", False),
        ("provider_requests_made_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_review_results_and_boundaries(review, field, expected):
    assert review[field] == expected


def test_retry_failure_counts_are_bound(review):
    assert [review[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [
        24877,
        1292,
        112,
        7,
    ]
    assert review["retry_pytest_first_result_authoritative"] is True
    assert review["root_full_regression_is_retry_evidence"] is False


def test_module_grouping_and_summary_review(review):
    assert review["module_level_grouping_review"] == {
        "source_digest": service.SOURCE_MODULE_GROUPING_DIGEST,
        "failed_or_errored_nodeids": 1404,
        "module_count": 29,
        "deterministic_ordering": ["descending count", "ascending module path"],
        "sample_nodeids_bounded_per_module": 5,
        "review_status": "REVIEWED_MODULE_LEVEL_GROUPING_ONLY",
    }
    assert review["module_summary_review"] == {
        "module_count": 29,
        "total_nodeids": 1404,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
    }


def test_limitations_and_unsupported_claims_are_reviewed(review):
    assert review["limitations_review"]["module_grouping_supported"] is True
    assert all(
        value is False
        for key, value in review["limitations_review"].items()
        if key != "module_grouping_supported"
    )
    assert all(review["unsupported_claims_exclusion_review"].values())


def test_planned_outputs_are_reviewed_without_generating_hints(review):
    assert review["planned_outputs_review"] == service.PLANNED_OUTPUTS_REVIEW
    assert review["planned_outputs_review"]["low_confidence_root_cause_hint_report"] == (
        "REVIEWED_NOT_GENERATED_BY_SELECTED_PACKAGE"
    )


def test_next_chain_and_gates_are_defined(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert len(review["next_chain"]) == 10
    assert review["next_gates"] == service.NEXT_GATES
    assert len(review["next_gates"]) == 10


def test_risk_controls_are_complete(review):
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 47


def test_observations_pass_and_have_required_shape(review):
    assert [row["observation_id"] for row in review["review_observations"]] == service.OBSERVATION_IDS
    assert all(set(row) == {"observation_id", "status", "expected", "actual", "message"} for row in review["review_observations"])
    assert all(row["status"] == "PASS" for row in review["review_observations"])


def test_checklist_passes_and_has_required_shape(review):
    assert [row["check_id"] for row in review["checklist"]] == service.CHECK_IDS
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in review["checklist"]
    )
    assert all(row["status"] == "PASS" for row in review["checklist"])
    assert review["summary"]["total_checks"] == 59
    assert review["summary"]["passed_checks"] == 59
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_review_and_manifest_digests_are_deterministic(review):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2()
    assert rebuilt == review
    assert review["marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest"] == (
        service.marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest_v1(review)
    )
    assert len(review["marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest"]) == 64


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
        review
    )
    assert result["total_checks"] == 59
    assert result["failed_checks"] == 0


_DELETE = object()


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_classification_method_execution_v2_digest", "0" * 64),
        ("source_classification_method_v2_module_grouping_digest", "0" * 64),
        ("source_classification_method_v2_digest_manifest_digest", "0" * 64),
        ("retry_pytest_failed_count", _DELETE),
        ("module_level_grouping_review", _DELETE),
        ("module_summary_review", _DELETE),
        ("module_summary_module_count", 28),
        ("largest_module_nodeid_counts", [136, 131, 122, 112]),
        ("failed_or_errored_nodeids_count", 1403),
        ("limitations_review", _DELETE),
        ("unsupported_claims_exclusion_review", _DELETE),
        ("failure_modules_classified", True),
        ("error_modules_classified", True),
        ("failure_error_separation_claimed", True),
        ("first_failure_identified", True),
        ("first_error_identified", True),
        ("first_order_claim_made", True),
        ("traceback_root_cause_claimed", True),
        ("retry_success_claimed", True),
        ("main_merge_readiness_claimed", True),
        ("classification_method_results_review_v2_created", False),
        ("classification_method_results_review_v2_ready", False),
        ("ready_for_remediation_or_method_candidate_after_v2_review", False),
        ("remediation_or_method_candidate_after_v2_review_created", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("diagnostic_command_executed", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True),
        ("evidence_regenerated", True),
        ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []),
        (
            "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest",
            _DELETE,
        ),
        (
            "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest",
            _DELETE,
        ),
    ],
)
def test_validator_rejects_changed_or_missing_evidence_and_opened_boundaries(review, field, value):
    changed = deepcopy(review)
    if value is _DELETE:
        changed.pop(field, None)
    else:
        changed[field] = value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
            changed
        )


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_markdown_v1(
        review
    )
    for heading in (
        "MarketFlow Repository Integration Branch Retry Failure Classification Method Results Review v2",
        "Source Execution v2",
        "Retry Failure Context",
        "Module-Level Grouping Review",
        "Module Summary Review",
        "Limitations Review",
        "Unsupported Claims Exclusion",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(tmp_path, review):
    result = service.write_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
        tmp_path
    )
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2.json"
    assert result["path"] == str(path)
    assert json.loads(path.read_text(encoding="utf-8")) == review
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error
    ):
        service.write_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
            tmp_path
        )


def test_public_service_exports_are_available():
    for name in (
        "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2",
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_READY",
        "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
        "build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2",
        "validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2",
        "write_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2",
        "build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_markdown_v1",
    ):
        assert getattr(services, name) is getattr(service, name)
